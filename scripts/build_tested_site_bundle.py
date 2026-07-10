#!/usr/bin/env python3
"""Copy a rendered site into a commit-bound, content-addressed deployment bundle."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
from typing import Any

from build_canonical_public_status import ROOT, load_json


MANIFEST_NAME = "tested-site-bundle.json"
STATUS_PATH = PurePosixPath("status/canonical-public-status.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_rows(site: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in sorted(candidate for candidate in site.rglob("*") if candidate.is_file()):
        if path.is_symlink():
            raise ValueError(f"site bundle refuses symlinked file: {path.relative_to(site)}")
        relative = path.relative_to(site).as_posix()
        if relative.startswith("../") or relative.startswith("/"):
            raise ValueError(f"site bundle path escapes root: {relative}")
        rows.append({"path": relative, "size": path.stat().st_size, "sha256": sha256_file(path)})
    return rows


def tree_sha256(rows: list[dict[str, Any]]) -> str:
    digest = hashlib.sha256()
    for row in rows:
        digest.update(f"{row['path']}\0{row['size']}\0{row['sha256']}\n".encode("utf-8"))
    return digest.hexdigest()


def build_manifest(site: Path, *, allow_local: bool) -> dict[str, Any]:
    status_file = site / STATUS_PATH
    if not status_file.exists():
        raise ValueError(f"rendered site is missing {STATUS_PATH}")
    status = load_json(status_file)
    if not isinstance(status, dict):
        raise TypeError("rendered canonical status must be an object")
    if not allow_local:
        if status.get("source_tree_state") != "clean" or status.get("build_context") != "tested_commit":
            raise ValueError("deployment bundle requires canonical status from a clean tested commit")
    commit = str(status.get("source_commit", ""))
    if len(commit) != 40 or any(ch not in "0123456789abcdef" for ch in commit):
        raise ValueError("canonical status source_commit must be a full lowercase SHA")
    rows = file_rows(site)
    return {
        "schema_version": "asi_stack.tested_site_bundle.v0",
        "artifact_name": f"asi-stack-pages-{commit}",
        "source_commit": commit,
        "source_tree_state": status.get("source_tree_state"),
        "build_context": status.get("build_context"),
        "canonical_status": {
            "path": str(STATUS_PATH),
            "status_id": str(status.get("status_id", "")),
            "sha256": sha256_file(status_file),
        },
        "site": {
            "file_count": len(rows),
            "total_bytes": sum(int(row["size"]) for row in rows),
            "tree_sha256": tree_sha256(rows),
            "files": rows,
        },
        "non_claims": [
            "Bundle integrity identifies the tested files; it does not prove chapter claims, model quality, safety, or security.",
            "A successful deployment still requires independent post-deployment attestation.",
            "A local-worktree bundle produced with --allow-local is diagnostic and is not deployable.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", type=Path, default=Path("_site"))
    parser.add_argument("--output", type=Path, default=Path("build/pages-tested"))
    parser.add_argument("--allow-local", action="store_true")
    args = parser.parse_args()
    site = args.site if args.site.is_absolute() else ROOT / args.site
    output = args.output if args.output.is_absolute() else ROOT / args.output
    if not site.is_dir():
        raise SystemExit(f"rendered site directory does not exist: {site}")
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    copied_site = output / "site"
    shutil.copytree(site, copied_site)
    manifest = build_manifest(copied_site, allow_local=args.allow_local)
    (output / MANIFEST_NAME).write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(
        f"Built {manifest['artifact_name']}: {manifest['site']['file_count']} files, "
        f"{manifest['site']['total_bytes']} bytes, tree {manifest['site']['tree_sha256'][:16]}."
    )


if __name__ == "__main__":
    main()
