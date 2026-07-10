#!/usr/bin/env python3
"""Validate a tested Pages bundle, exact file inventory, and commit binding."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
import sys
from typing import Any

from build_canonical_public_status import ROOT, load_json, validate_against_schema
from build_tested_site_bundle import MANIFEST_NAME, build_manifest


SCHEMA = ROOT / "schemas" / "tested_site_bundle.schema.json"


def compare(expected: dict[str, Any], actual: dict[str, Any], expected_commit: str | None) -> list[str]:
    errors: list[str] = []
    schema = load_json(SCHEMA)
    errors.extend(validate_against_schema(expected, schema, MANIFEST_NAME))
    if expected_commit and expected.get("source_commit") != expected_commit.lower():
        errors.append(
            f"bundle source commit {expected.get('source_commit')!r} does not match requested {expected_commit.lower()!r}"
        )
    for field in ("source_commit", "source_tree_state", "build_context", "canonical_status", "site"):
        if expected.get(field) != actual.get(field):
            errors.append(f"bundle {field} differs from recomputed site content")
    if expected.get("artifact_name") != f"asi-stack-pages-{expected.get('source_commit')}":
        errors.append("bundle artifact_name is not commit-bound")
    return errors


def negative_controls(manifest: dict[str, Any], actual: dict[str, Any]) -> list[str]:
    """Prove digest, commit, and inventory mutations are rejected."""
    failures: list[str] = []
    digest_mutation = copy.deepcopy(manifest)
    digest_mutation["site"]["files"][0]["sha256"] = "0" * 64
    controls = [
        ("file digest mutation", digest_mutation, actual, manifest["source_commit"]),
        ("wrong expected commit", manifest, actual, "f" * 40),
    ]
    missing_file = copy.deepcopy(actual)
    missing_file["site"]["files"] = missing_file["site"]["files"][:-1]
    missing_file["site"]["file_count"] -= 1
    controls.append(("missing site file", manifest, missing_file, manifest["source_commit"]))
    for label, candidate, recomputed, commit in controls:
        if not compare(candidate, recomputed, commit):
            failures.append(f"negative control was incorrectly accepted: {label}")
    return failures


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bundle", type=Path, default=Path("build/pages-tested"))
    parser.add_argument("--expected-commit")
    parser.add_argument("--allow-local", action="store_true")
    args = parser.parse_args()
    bundle = args.bundle if args.bundle.is_absolute() else ROOT / args.bundle
    manifest_path = bundle / MANIFEST_NAME
    site = bundle / "site"
    errors: list[str] = []
    if not manifest_path.exists() or not site.is_dir():
        raise SystemExit(f"bundle must contain {MANIFEST_NAME} and site/: {bundle}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    try:
        actual = build_manifest(site, allow_local=args.allow_local)
    except (TypeError, ValueError) as exc:
        raise SystemExit(f"could not recompute tested site bundle: {exc}") from exc
    errors.extend(compare(manifest, actual, args.expected_commit))
    errors.extend(negative_controls(manifest, actual))
    if not args.allow_local and (
        manifest.get("source_tree_state") != "clean" or manifest.get("build_context") != "tested_commit"
    ):
        errors.append("deployable bundle must report a clean tested commit")
    if errors:
        print("Tested site bundle validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)
    print(
        f"Tested site bundle validation passed: {manifest['site']['file_count']} files, "
        f"commit {manifest['source_commit'][:12]}, 3 rejecting negative controls."
    )


if __name__ == "__main__":
    main()
