#!/usr/bin/env python3
"""Validate latest mirroring and immutable-release truth boundaries."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any

from build_canonical_public_status import ROOT, load_json, validate_against_schema
from build_release_channels import INDEX_REL, POLICY, STATUS_REL, build_index


POLICY_SCHEMA = ROOT / "schemas" / "versioned_release_policy.schema.json"
INDEX_SCHEMA = ROOT / "schemas" / "versioned_release_index.schema.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def file_map(root: Path, excluded: set[str] | None = None) -> dict[str, str]:
    excluded = excluded or set()
    return {
        path.relative_to(root).as_posix(): digest(path)
        for path in sorted(candidate for candidate in root.rglob("*") if candidate.is_file())
        if path.relative_to(root).parts[0] not in excluded
    }


def validate_policy(policy: dict[str, Any]) -> list[str]:
    errors = validate_against_schema(policy, load_json(POLICY_SCHEMA), "versioned_release_policy")
    immutable = policy.get("immutable_channel", {})
    for field in (
        "candidate_manifest_schema",
        "candidate_builder",
        "candidate_validator",
        "publication_transaction_doc",
    ):
        command_or_path = str(immutable.get(field, ""))
        relative = command_or_path.split()[0] if command_or_path else ""
        if not relative or not (ROOT / relative).is_file():
            errors.append(f"immutable release policy references missing {field}: {command_or_path!r}")
    versions: set[str] = set()
    for row in policy.get("known_releases", []):
        version = row.get("version", "")
        if version in versions:
            errors.append(f"duplicate immutable release version: {version}")
        versions.add(version)
        if not re.fullmatch(policy["immutable_channel"]["tag_pattern"], version):
            errors.append(f"release version does not satisfy tag policy: {version}")
        record = ROOT / row.get("release_record", "")
        if not record.exists():
            errors.append(f"immutable release row has missing record: {row.get('release_record')}")
        elif load_json(record).get("source_commit") != row.get("source_commit"):
            errors.append(f"{version}: release-record commit mismatch")
        elif row.get("site_artifact_state") == "not_published":
            record_text = record.read_text(encoding="utf-8", errors="ignore")
            if "no full immutable rendered-site bundle" not in record_text:
                errors.append(f"{version}: release record does not disclose the absent immutable site bundle")
        published = row.get("site_artifact_state") == "published"
        has_url = bool(row.get("site_artifact_url"))
        has_digest = bool(re.fullmatch(r"[0-9a-f]{64}", row.get("site_artifact_sha256", "")))
        if published != (has_url and has_digest):
            errors.append(f"{version}: published state requires exact site artifact URL and SHA-256")
        if not published and (has_url or row.get("site_artifact_sha256")):
            errors.append(f"{version}: unpublished site artifact must not carry URL or digest")
        if row.get("archive_backfill_decision") == "declined_historical_render_not_available" and published:
            errors.append(f"{version}: declined historical backfill cannot claim a published site artifact")
    return errors


def validate_index(index: dict[str, Any], expected: dict[str, Any]) -> list[str]:
    errors = validate_against_schema(index, load_json(INDEX_SCHEMA), "versioned_release_index")
    if index != expected:
        errors.append("versioned release index differs from canonical status plus policy")
    return errors


def validate_mirror(root_files: dict[str, str], latest_files: dict[str, str]) -> list[str]:
    if root_files == latest_files:
        return []
    missing = sorted(set(root_files) - set(latest_files))
    extra = sorted(set(latest_files) - set(root_files))
    changed = sorted(path for path in set(root_files) & set(latest_files) if root_files[path] != latest_files[path])
    return [f"latest mirror differs from tested root: missing={missing[:3]}, extra={extra[:3]}, changed={changed[:3]}"]


def negative_controls(policy: dict[str, Any], expected_index: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    bad_policy = copy.deepcopy(policy)
    bad_policy["known_releases"][0]["site_artifact_state"] = "published"
    bad_index = copy.deepcopy(expected_index)
    bad_index["latest"]["source_commit"] = "f" * 40
    backfill_policy = copy.deepcopy(policy)
    backfill_policy["known_releases"][0]["site_artifact_state"] = "published"
    backfill_policy["known_releases"][0]["site_artifact_url"] = "https://example.invalid/fabricated.tar.gz"
    backfill_policy["known_releases"][0]["site_artifact_sha256"] = "a" * 64
    controls = (
        ("unbacked immutable artifact claim", validate_policy(bad_policy)),
        ("wrong latest commit", validate_index(bad_index, expected_index)),
        ("changed latest file", validate_mirror({"index.html": "a"}, {"index.html": "b"})),
        ("fabricated declined backfill", validate_policy(backfill_policy)),
    )
    for label, errors in controls:
        if not errors:
            failures.append(f"negative control was incorrectly accepted: {label}")
    return failures


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", type=Path)
    parser.add_argument("--require-clean", action="store_true")
    args = parser.parse_args()
    policy = load_json(POLICY)
    errors = validate_policy(policy)
    if args.site:
        site = args.site if args.site.is_absolute() else ROOT / args.site
        status = load_json(site / STATUS_REL)
    else:
        from build_canonical_public_status import build_status
        status = build_status(timestamp="2000-01-01T00:00:00Z")
        site = None
    expected_index = build_index(status, policy)
    if site:
        index_path = site / INDEX_REL
        if not index_path.exists():
            errors.append(f"rendered site missing {INDEX_REL}")
        else:
            errors.extend(validate_index(load_json(index_path), expected_index))
        latest = site / "latest"
        if not latest.is_dir():
            errors.append("rendered site missing full latest/ mirror")
        else:
            errors.extend(validate_mirror(file_map(site, {"latest", "versions"}), file_map(latest)))
        if args.require_clean and (
            status.get("source_tree_state") != "clean" or status.get("build_context") != "tested_commit"
        ):
            errors.append("release channels require clean tested-commit canonical status")
    errors.extend(negative_controls(policy, expected_index))
    if errors:
        print("Release-channel validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)
    print(
        "Release-channel validation passed: full moving latest mirror, "
        f"{len(policy['known_releases'])} honest immutable-release row(s), and 4 rejecting negative controls."
    )


if __name__ == "__main__":
    main()
