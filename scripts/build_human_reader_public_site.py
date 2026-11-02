#!/usr/bin/env python3
"""Install and validate the rendered current Human Reader under a Pages site."""

from __future__ import annotations

import argparse
import hashlib
from html.parser import HTMLParser
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import tempfile
from urllib.parse import unquote, urlsplit

from build_human_reader_current import CROSSWALK, EDITION, ROOT
from build_tested_site_bundle import bundle_lock, exchange_directories, install_directory_noreplace, file_rows, sync_directory, sync_stage, tree_sha256
from projection_files import ProjectionFiles


RENDERED = EDITION / "_book"
INSTALL_MANIFEST = "reader-install-manifest.json"
INSTALL_VERSION = "asi_stack.human_reader_install.v1"


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag not in {"a", "link", "script", "img"}:
            return
        target_name = "href" if tag in {"a", "link"} else "src"
        value = dict(attrs).get(target_name)
        if value:
            self.links.append(value)


def internal_link_errors(root: Path, *, site: Path | None = None) -> list[str]:
    errors = []
    for page in sorted(root.rglob("*.html")):
        parser = LinkParser()
        parser.feed(page.read_text(encoding="utf-8", errors="replace"))
        for value in parser.links:
            parsed = urlsplit(value)
            if parsed.scheme or parsed.netloc or value.startswith(("#", "mailto:", "tel:", "javascript:")):
                continue
            relative = Path(unquote(parsed.path))
            if site is None:
                if relative.is_absolute():
                    continue
                target = (page.parent / relative).resolve()
            else:
                # Check a staged reader at its eventual URL depth. Links into
                # the reader resolve against the candidate; technical/source
                # links resolve against the existing surrounding site.
                virtual_page = site / "reader" / page.relative_to(root)
                target = ((site / str(relative).lstrip("/")) if relative.is_absolute()
                          else (virtual_page.parent / relative)).resolve()
                if not target.is_relative_to(site):
                    errors.append(f"{page.relative_to(root)}: internal target escapes rendered site: {value}")
                    continue
                if target.is_relative_to(site / "reader"):
                    target = root / target.relative_to(site / "reader")
            if not target.exists():
                errors.append(f"{page.relative_to(root)}: missing internal target {value}")
    return errors


def route_map(crosswalk: dict) -> dict:
    routes = []
    for unit in crosswalk["units"]:
        reader_path = reader_relative(unit["public_path"]).as_posix()
        for owner in unit["owners"]:
            routes.append(
                {
                    "chapter_id": owner["chapter_id"],
                    "technical_source_file": owner["technical_source_file"],
                    "technical_path": owner["live_technical_path"],
                    "unit_id": unit["unit_id"],
                    "reader_path": reader_path,
                }
            )
    routes.sort(key=lambda row: row["chapter_id"])
    return {
        "schema_version": "asi_stack.human_reader_public_route_map.v1",
        "edition_id": crosswalk["edition_id"],
        "state": "current_html_editorial_projection",
        "default_reader_path": "index.html",
        "route_count": len(routes),
        "routes": routes,
        "support_state_effect": "none",
        "release_effect": "none",
        "non_claims": [
            "A public HTML route is not a major-version reader release.",
            "Route completeness does not transfer support or evidence between editions.",
        ],
    }


def reader_relative(public_path: str) -> PurePosixPath:
    path = PurePosixPath(public_path)
    if (path.is_absolute() or path.as_posix() != public_path or ".." in path.parts
            or "\\" in public_path or not public_path.startswith("reader/")
            or path.suffix != ".html"):
        raise ValueError(f"invalid public reader route: {public_path!r}")
    return path.relative_to("reader")


def validate_render(rendered: Path, crosswalk: dict) -> list[str]:
    errors = []
    if not (rendered / "index.html").is_file():
        errors.append("rendered Human Reader index.html is missing")
    for unit in crosswalk["units"]:
        relative = reader_relative(unit["public_path"])
        page = rendered / relative
        if not page.is_file():
            errors.append(f"rendered Human Reader page is missing: {relative.as_posix()}")
            continue
        text = page.read_text(encoding="utf-8", errors="replace")
        for fragment in (unit["title"], "asi-edition-switch", "AI / researcher", "Human Reader"):
            if fragment not in text:
                errors.append(f"{relative.as_posix()}: missing rendered fragment {fragment!r}")
    return errors


def payload_rows(directory: Path) -> list[dict]:
    return [row for row in file_rows(directory) if row["path"] != INSTALL_MANIFEST]


def expected_manifest(rendered_rows: list[dict], crosswalk_bytes: bytes, routes_bytes: bytes, edition_id: str) -> dict:
    reserved = {INSTALL_MANIFEST, "route-map.json", "conclusion-claim-crosswalk.json"}
    if any(row["path"] in reserved for row in rendered_rows):
        raise ValueError("rendered source collides with reader installer metadata")
    rows = [*rendered_rows]
    for name, body in (("route-map.json", routes_bytes), ("conclusion-claim-crosswalk.json", crosswalk_bytes)):
        rows.append({"path": name, "size": len(body), "sha256": hashlib.sha256(body).hexdigest()})
    rows.sort(key=lambda row: row["path"])
    return {"schema_version": INSTALL_VERSION, "edition_id": edition_id,
            "rendered_source_tree_sha256": tree_sha256(rendered_rows),
            "crosswalk_sha256": hashlib.sha256(crosswalk_bytes).hexdigest(),
            "payload_tree_sha256": tree_sha256(rows), "files": rows,
            "support_state_effect": "none", "release_effect": "none"}


def previous_is_owned(destination: Path, expected: dict) -> bool:
    if not destination.exists():
        return False
    if not destination.is_dir() or destination.is_symlink():
        raise ValueError("refusing to replace an unrecognized reader destination")
    rows = file_rows(destination)
    manifest_path = destination / INSTALL_MANIFEST
    if manifest_path.exists():
        recorded = json.loads(manifest_path.read_bytes())
        payload = [row for row in rows if row["path"] != INSTALL_MANIFEST]
        if (not isinstance(recorded, dict) or recorded.get("schema_version") != INSTALL_VERSION
                or set(recorded) != set(expected)
                or not isinstance(recorded.get("edition_id"), str) or not recorded["edition_id"]
                or any(not isinstance(recorded.get(key), str) or not re.fullmatch(r"[a-f0-9]{64}", recorded[key])
                       for key in ("rendered_source_tree_sha256", "crosswalk_sha256", "payload_tree_sha256"))
                or recorded.get("support_state_effect") != "none" or recorded.get("release_effect") != "none"
                or recorded.get("files") != payload or recorded.get("payload_tree_sha256") != tree_sha256(payload)):
            raise ValueError("previous reader integrity failed; preserve it and use a fresh site")
        prior_crosswalk = (destination / "conclusion-claim-crosswalk.json").read_bytes()
        prior_canonical = json.loads(prior_crosswalk)
        prior_render = [row for row in payload if row["path"] not in {"route-map.json", "conclusion-claim-crosswalk.json"}]
        if (recorded["crosswalk_sha256"] != hashlib.sha256(prior_crosswalk).hexdigest()
                or recorded["rendered_source_tree_sha256"] != tree_sha256(prior_render)
                or recorded["edition_id"] != prior_canonical.get("edition_id")
                or json.loads((destination / "route-map.json").read_bytes()) != route_map(prior_canonical)):
            raise ValueError("previous reader input/route identity failed; preserve it and use a fresh site")
    elif rows != expected["files"]:
        # Automatic legacy adoption is limited to an exact match with the
        # current source and two existing generated metadata files. It cannot
        # erase arbitrary files or bless an unknown older snapshot.
        raise ValueError("legacy reader is not an exact known current payload; preserve it and use a fresh site")
    return True


def ordinary(path: Path) -> None:
    if path.is_symlink() or any(parent.is_symlink() for parent in path.parents):
        raise ValueError(f"reader installation must not traverse a symlink: {path}")


def installation_paths(site: Path) -> tuple[Path, Path]:
    """Reject unsafe ancestry before a CLI caller creates any directories."""
    for path in (site, RENDERED, CROSSWALK):
        ordinary(path)
    site = site.resolve()
    rendered = RENDERED.resolve()
    if (site == rendered or site in rendered.parents or rendered in site.parents
            or site == CROSSWALK.parent.resolve() or site in CROSSWALK.resolve().parents):
        raise ValueError("rendered source, crosswalk and public site must not overlap")
    return site, rendered


def install(site: Path, *, check: bool = False) -> dict:
    site, rendered = installation_paths(site)
    if not site.is_dir() or not CROSSWALK.is_file():
        raise ValueError("reader installation requires an existing site and regular crosswalk")
    source_rows = file_rows(rendered)
    crosswalk_bytes = CROSSWALK.read_bytes()
    crosswalk = json.loads(crosswalk_bytes)
    routes = route_map(crosswalk)
    routes_text = json.dumps(routes, indent=2, ensure_ascii=False) + "\n"
    expected = expected_manifest(source_rows, crosswalk_bytes, routes_text.encode(), crosswalk["edition_id"])
    errors = validate_render(rendered, crosswalk)
    if errors:
        raise ValueError("; ".join(errors))
    destination = site / "reader"
    ordinary(destination)
    def check_inputs() -> None:
        ordinary(CROSSWALK)
        if file_rows(rendered) != source_rows or CROSSWALK.read_bytes() != crosswalk_bytes:
            raise ValueError("rendered reader or crosswalk changed before installation")
    if check:
        observed_rows = file_rows(destination) if destination.exists() else None
        previous_is_owned(destination, expected)
        if not destination.is_dir() or not (destination / INSTALL_MANIFEST).is_file() or json.loads((destination / INSTALL_MANIFEST).read_bytes()) != expected:
            raise ValueError("reader projection is stale; run build_human_reader_public_site.py --site <site>")
        errors = validate_render(destination, crosswalk) + internal_link_errors(destination, site=site)
        if errors:
            raise ValueError("; ".join(errors))
        check_inputs()
        if file_rows(destination) != observed_rows or payload_rows(destination) != expected["files"]:
            raise ValueError("installed reader changed during its read-only check")
        return routes
    # The stable lock and staging container stay outside the publishable site.
    # Share the rendered-site lock with channel installation so the two
    # generators cannot replace each other's observed root simultaneously.
    with bundle_lock(site):
        prior_rows = file_rows(destination) if destination.exists() else None
        existed = previous_is_owned(destination, expected)
        if (file_rows(destination) if destination.exists() else None) != prior_rows:
            raise ValueError("installed reader changed during ownership inspection")
        if existed and (destination / INSTALL_MANIFEST).is_file() and json.loads((destination / INSTALL_MANIFEST).read_bytes()) == expected:
            errors = validate_render(destination, crosswalk) + internal_link_errors(destination, site=site)
            if errors:
                raise ValueError("; ".join(errors))
            check_inputs()
            if file_rows(destination) != prior_rows or payload_rows(destination) != expected["files"]:
                raise ValueError("installed reader changed during no-op installation")
            return routes
        container = Path(tempfile.mkdtemp(prefix=f".{site.name}-reader-stage-", dir=site.parent))
        stage = container / "reader"
        state = {"schema_version": "asi_stack.reader_install_stage.v1", "state": "incomplete",
                 "destination": str(destination), "expected_payload_tree_sha256": expected["payload_tree_sha256"],
                 "prior_payload_tree_sha256": tree_sha256(prior_rows) if prior_rows is not None else None}
        files = ProjectionFiles()
        files.write(container / "staging.json", json.dumps(state, indent=2) + "\n")
        sync_directory(container)
        attempted = installed = False
        durable = False
        try:
            shutil.copytree(rendered, stage, symlinks=True)
            if file_rows(stage) != source_rows:
                raise ValueError("rendered reader changed while copying")
            files.write(stage / "route-map.json", routes_text)
            # Install the exact already inspected bytes, never re-read a moving
            # crosswalk and then certify its new hash as the inspected input.
            with (stage / "conclusion-claim-crosswalk.json").open("xb") as stream:
                stream.write(crosswalk_bytes)
            files.write(stage / INSTALL_MANIFEST, json.dumps(expected, indent=2, ensure_ascii=False) + "\n")
            if payload_rows(stage) != expected["files"]:
                raise ValueError("staged reader payload differs from inspected inputs")
            staged_rows = file_rows(stage)
            errors = validate_render(stage, crosswalk) + internal_link_errors(stage, site=site)
            if errors:
                raise ValueError("; ".join(errors))
            sync_stage(stage)
            state["state"] = "prepared"
            files.write(container / "staging.json", json.dumps(state, indent=2) + "\n")
            sync_directory(container)
            check_inputs()
            ordinary(destination)
            if (file_rows(destination) if destination.exists() else None) != prior_rows:
                raise ValueError("previous reader changed before installation; preserving concurrent edits")
            state["state"] = "installation_attempted"
            files.write(container / "staging.json", json.dumps(state, indent=2) + "\n")
            sync_directory(container)
            attempted = True
            if existed:
                exchange_directories(stage, destination)
            else:
                install_directory_noreplace(stage, destination)
            installed = True
            if existed and file_rows(stage) != prior_rows:
                raise ValueError("changed prior reader is retained for inspection")
            if file_rows(destination) != staged_rows:
                raise ValueError("installed reader changed before acceptance")
            check_inputs()
            sync_directory(site)
            durable = True
            return routes
        finally:
            if attempted and not durable:
                # A successful namespace exchange followed by failed fsync is
                # uncertain durability, not a failed pre-install copy. Keep the
                # complete prior tree and diagnostic rather than erase custody.
                state["state"] = ("installed_durability_unconfirmed" if installed
                                  else "installation_outcome_unconfirmed")
                files.write(container / "staging.json", json.dumps(state, indent=2) + "\n")
            else:
                shutil.rmtree(container)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", type=Path, default=Path("_site"))
    parser.add_argument("--check", action="store_true", help="Check current installed bytes and routes without writing")
    args = parser.parse_args()
    site = args.site if args.site.is_absolute() else ROOT / args.site
    try:
        site, _ = installation_paths(site)
        if not args.check:
            site.mkdir(parents=True, exist_ok=True)
        routes = install(site, check=args.check)
    except (ValueError, OSError) as exc:
        raise SystemExit(f"Human Reader public-site build failed: {exc}") from exc
    print(
        f"{'Checked' if args.check else 'Installed'} Human Reader public site: {routes['route_count']} owner routes, "
        "support/release effects none."
    )


if __name__ == "__main__":
    main()
