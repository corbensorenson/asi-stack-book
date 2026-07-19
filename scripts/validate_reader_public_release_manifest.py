#!/usr/bin/env python3
"""Validate the tracked reader-release manifest and optional local assets."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "editions/reader_manuscript/reader_2026_07_18/manifest.json"
SCHEMA = ROOT / "schemas/reader_public_release_manifest.schema.json"
EXPECTED = {
    "pdf": ("the-asi-stack-reader-2026-07-18.pdf", 13022967, "249a7e745fdb302398b532bd03d898b8bc6f07f96fbc6ad3794df69d3d1e1192"),
    "epub": ("the-asi-stack-reader-2026-07-18.epub", 10129904, "c5ea58db02310c966ac0760348cc476ed6fba75446c7527105c0a9c4778a108f"),
    "docx": ("the-asi-stack-reader-2026-07-18.docx", 8622060, "3b446abce2722aed960ce0b8d3cbdc7470486df7b9ba3b56f892acdefd8b4ee8"),
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def semantic_errors(manifest: dict, asset_dir: Path | None = None) -> list[str]:
    errors: list[str] = []
    formats = [row.get("format") for row in manifest.get("artifacts", [])]
    if formats != ["pdf", "epub", "docx"]:
        errors.append("artifact order must be pdf, epub, docx")
    for row in manifest.get("artifacts", []):
        expected = EXPECTED.get(row.get("format"))
        if expected and (row.get("filename"), row.get("bytes"), row.get("sha256")) != expected:
            errors.append(f"frozen artifact identity drift: {row.get('format')}")
    state = manifest.get("release_state")
    expected_artifact_state = state
    if any(row.get("status") != expected_artifact_state for row in manifest.get("artifacts", [])):
        errors.append("artifact status does not match release state")
    if state == "published":
        if not manifest.get("release_commit") or not manifest.get("release_url"):
            errors.append("published release lacks commit or URL")
        if any(not row.get("download_url") for row in manifest.get("artifacts", [])):
            errors.append("published artifact lacks download URL")
    else:
        if manifest.get("release_commit") or manifest.get("release_url"):
            errors.append("candidate release invents public identity")

    source = manifest.get("source_content_commit", "")
    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", source, "HEAD"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if ancestor.returncode != 0:
        errors.append("source content commit is not an ancestor of HEAD")

    if asset_dir is not None:
        for row in manifest.get("artifacts", []):
            path = asset_dir / row["filename"]
            if not path.is_file():
                errors.append(f"missing asset: {path}")
                continue
            if path.stat().st_size != row["bytes"]:
                errors.append(f"byte count drift: {path.name}")
            if sha256(path) != row["sha256"]:
                errors.append(f"SHA-256 drift: {path.name}")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-assets", type=Path)
    args = parser.parse_args()
    manifest = load(MANIFEST)
    schema = load(SCHEMA)
    failures = [
        f"schema:{'.'.join(map(str, error.path))}: {error.message}"
        for error in Draft202012Validator(schema).iter_errors(manifest)
    ]
    failures.extend(semantic_errors(manifest, args.check_assets))

    mutations: list[tuple[str, dict]] = []
    bad_hash = copy.deepcopy(manifest)
    bad_hash["artifacts"][0]["sha256"] = "0" * 64
    mutations.append(("artifact hash drift", bad_hash))
    bad_rights = copy.deepcopy(manifest)
    bad_rights["rights"]["grant"] = "CC-BY"
    mutations.append(("invented rights grant", bad_rights))
    bad_accessibility = copy.deepcopy(manifest)
    bad_accessibility["quality_assurance"]["pdf"]["tagged"] = True
    mutations.append(("invented PDF tagging", bad_accessibility))
    for label, candidate in mutations:
        schema_fail = list(Draft202012Validator(schema).iter_errors(candidate))
        semantic_fail = semantic_errors(candidate)
        if not schema_fail and not semantic_fail:
            failures.append(f"negative mutation accepted: {label}")

    if failures:
        raise SystemExit("Reader public release manifest failed:\n - " + "\n - ".join(failures))
    suffix = " with exact local assets" if args.check_assets else ""
    print(f"Reader public release manifest passed{suffix}: 3 formats, honest rights and accessibility residuals, 3/3 mutations rejected.")


if __name__ == "__main__":
    main()
