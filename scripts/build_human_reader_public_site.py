#!/usr/bin/env python3
"""Install and validate the rendered current Human Reader under a Pages site."""

from __future__ import annotations

import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
import shutil
from urllib.parse import unquote, urlsplit

from build_human_reader_current import CROSSWALK, EDITION, ROOT


RENDERED = EDITION / "_book"


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


def internal_link_errors(root: Path) -> list[str]:
    errors = []
    for page in sorted(root.rglob("*.html")):
        parser = LinkParser()
        parser.feed(page.read_text(encoding="utf-8", errors="replace"))
        for value in parser.links:
            parsed = urlsplit(value)
            if parsed.scheme or parsed.netloc or value.startswith(("#", "mailto:", "tel:", "javascript:")):
                continue
            relative = Path(unquote(parsed.path))
            if relative.is_absolute():
                continue
            target = (page.parent / relative).resolve()
            if not target.exists():
                errors.append(f"{page.relative_to(root)}: missing internal target {value}")
    return errors


def route_map(crosswalk: dict) -> dict:
    routes = []
    for unit in crosswalk["units"]:
        reader_path = unit["public_path"].removeprefix("reader/")
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


def validate_render(rendered: Path, crosswalk: dict) -> list[str]:
    errors = []
    if not (rendered / "index.html").is_file():
        errors.append("rendered Human Reader index.html is missing")
    for unit in crosswalk["units"]:
        relative = Path(unit["public_path"].removeprefix("reader/"))
        page = rendered / relative
        if not page.is_file():
            errors.append(f"rendered Human Reader page is missing: {relative.as_posix()}")
            continue
        text = page.read_text(encoding="utf-8", errors="replace")
        for fragment in (unit["title"], "asi-edition-switch", "AI / researcher", "Human Reader"):
            if fragment not in text:
                errors.append(f"{relative.as_posix()}: missing rendered fragment {fragment!r}")
    return errors


def install(site: Path) -> dict:
    crosswalk = json.loads(CROSSWALK.read_text(encoding="utf-8"))
    errors = validate_render(RENDERED, crosswalk)
    if errors:
        raise ValueError("; ".join(errors))
    destination = site / "reader"
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(RENDERED, destination)
    routes = route_map(crosswalk)
    (destination / "route-map.json").write_text(
        json.dumps(routes, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    shutil.copy2(CROSSWALK, destination / "conclusion-claim-crosswalk.json")
    errors = validate_render(destination, crosswalk)
    errors.extend(internal_link_errors(destination))
    if errors:
        raise ValueError("; ".join(errors))
    installed_routes = json.loads((destination / "route-map.json").read_text(encoding="utf-8"))
    if installed_routes != routes:
        raise ValueError("installed Human Reader route map differs from canonical derivation")
    return routes


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", type=Path, default=Path("_site"))
    args = parser.parse_args()
    site = args.site if args.site.is_absolute() else ROOT / args.site
    site.mkdir(parents=True, exist_ok=True)
    try:
        routes = install(site)
    except ValueError as exc:
        raise SystemExit(f"Human Reader public-site build failed: {exc}") from exc
    print(
        f"Installed Human Reader public site: 26 units, {routes['route_count']} owner routes, "
        "support/release effects none."
    )


if __name__ == "__main__":
    main()
