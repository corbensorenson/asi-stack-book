#!/usr/bin/env python3
"""Validate the curated reader manuscript manifest.

The curated reader manuscript is allowed to become a parallel derivative source
for human prose, but it is not allowed to become an independent evidence source.
This validator keeps that future path explicit while the current status remains
not_graduated.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "editions" / "reader_manuscript" / "v1_0" / "manifest.json"
ALLOWED_STATUS = {"not_graduated", "drafting", "reconciliation", "release_candidate", "released"}
ALLOWED_RECONCILIATION_STATUS = {"not_started", "drafting", "blocked", "reconciled"}
REQUIRED_FIELDS = {
    "schema_version",
    "major_version",
    "status",
    "canonical_relationship",
    "live_sources_of_truth",
    "generated_baseline",
    "overlay_source",
    "allowed_divergence",
    "blocked_divergence",
    "graduation_criteria",
    "chapter_records",
    "reconciliation_report",
    "non_claims",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def flatten_chapters(structure: dict[str, Any]) -> dict[str, dict[str, Any]]:
    chapters: dict[str, dict[str, Any]] = {}
    for part in structure.get("parts", []):
        if not isinstance(part, dict):
            continue
        for chapter in part.get("chapters", []):
            if isinstance(chapter, dict) and isinstance(chapter.get("id"), str):
                chapters[chapter["id"]] = chapter
    return chapters


def require_string_list(owner: str, key: str, value: Any, errors: list[str]) -> list[str]:
    if not isinstance(value, list) or not value:
        errors.append(f"{owner}: {key} must be a non-empty list.")
        return []
    result: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            errors.append(f"{owner}: {key} entries must be non-empty strings.")
        else:
            result.append(item)
    return result


def require_existing_path(owner: str, path_value: str, errors: list[str]) -> None:
    path = ROOT / path_value
    if not path.exists():
        errors.append(f"{owner}: referenced path does not exist: {path_value}")


def validate_manifest(data: dict[str, Any], errors: list[str]) -> None:
    missing = sorted(REQUIRED_FIELDS - set(data))
    if missing:
        errors.append(f"{rel(MANIFEST)} missing required fields: {missing}")
        return

    if data.get("schema_version") != "0.1":
        errors.append("schema_version must be 0.1.")
    if data.get("major_version") != "v1.0":
        errors.append("major_version must be v1.0.")
    if data.get("status") not in ALLOWED_STATUS:
        errors.append(f"status must be one of {sorted(ALLOWED_STATUS)}.")
    if data.get("canonical_relationship") != "parallel_derivative_not_equal_authority":
        errors.append("canonical_relationship must be parallel_derivative_not_equal_authority.")

    for path_value in require_string_list("reader manuscript manifest", "live_sources_of_truth", data.get("live_sources_of_truth"), errors):
        require_existing_path("live_sources_of_truth", path_value, errors)

    baseline = data.get("generated_baseline")
    if not isinstance(baseline, dict):
        errors.append("generated_baseline must be an object.")
    else:
        if baseline.get("command") != "python3 scripts/build_reader_edition.py":
            errors.append("generated_baseline.command must be python3 scripts/build_reader_edition.py.")
        if baseline.get("check_command") != "python3 scripts/build_reader_edition.py --check":
            errors.append("generated_baseline.check_command must be python3 scripts/build_reader_edition.py --check.")
        if baseline.get("baseline_dir") != "build/reader_edition":
            errors.append("generated_baseline.baseline_dir must be build/reader_edition.")

    overlay = data.get("overlay_source")
    if not isinstance(overlay, dict):
        errors.append("overlay_source must be an object.")
    else:
        for key in ("manifest", "asset"):
            value = overlay.get(key)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"overlay_source.{key} must be a non-empty string.")
            else:
                require_existing_path(f"overlay_source.{key}", value, errors)

    allowed = require_string_list("reader manuscript manifest", "allowed_divergence", data.get("allowed_divergence"), errors)
    blocked = require_string_list("reader manuscript manifest", "blocked_divergence", data.get("blocked_divergence"), errors)
    require_string_list("reader manuscript manifest", "graduation_criteria", data.get("graduation_criteria"), errors)
    non_claims = require_string_list("reader manuscript manifest", "non_claims", data.get("non_claims"), errors)

    blocked_text = " ".join(blocked).lower()
    for required_phrase in ("support-state", "source boundary", "proof/test", "release artifact"):
        if required_phrase not in blocked_text:
            errors.append(f"blocked_divergence must mention {required_phrase}.")

    non_claim_text = " ".join(non_claims).lower()
    for required_phrase in ("does not create", "does not promote", "source of truth"):
        if required_phrase not in non_claim_text:
            errors.append(f"non_claims must include boundary phrase: {required_phrase}")

    if "pacing" not in allowed or "section flow" not in allowed:
        errors.append("allowed_divergence must include pacing and section flow.")


def validate_chapter_records(data: dict[str, Any], chapters: dict[str, dict[str, Any]], errors: list[str]) -> None:
    records = data.get("chapter_records")
    if not isinstance(records, list):
        errors.append("chapter_records must be a list.")
        return

    seen: set[str] = set()
    for index, record in enumerate(records):
        owner = f"chapter_records[{index}]"
        if not isinstance(record, dict):
            errors.append(f"{owner} must be an object.")
            continue
        chapter_id = record.get("chapter_id")
        if not isinstance(chapter_id, str) or chapter_id not in chapters:
            errors.append(f"{owner}: chapter_id must reference a manifest chapter.")
            continue
        if chapter_id in seen:
            errors.append(f"{owner}: duplicate chapter_id {chapter_id}.")
        seen.add(chapter_id)

        file_path = record.get("file")
        if not isinstance(file_path, str) or not file_path.startswith("editions/reader_manuscript/v1_0/chapters/"):
            errors.append(f"{owner}: file must be under editions/reader_manuscript/v1_0/chapters/.")
        elif not (ROOT / file_path).exists():
            errors.append(f"{owner}: curated chapter file does not exist: {file_path}")

        status = record.get("reconciliation_status")
        if status not in ALLOWED_RECONCILIATION_STATUS:
            errors.append(f"{owner}: reconciliation_status must be one of {sorted(ALLOWED_RECONCILIATION_STATUS)}.")

        for key in ("generated_baseline_ref", "live_source_ref", "claim_boundary_ref", "implementation_horizon_ref"):
            if not isinstance(record.get(key), str) or not record[key].strip():
                errors.append(f"{owner}: {key} must be a non-empty string.")

    if data.get("status") in {"release_candidate", "released"}:
        missing = sorted(set(chapters) - seen)
        if missing:
            errors.append(f"{data['status']} curated reader manuscript missing chapter records: {missing}")
        unreconciled = [
            record.get("chapter_id")
            for record in records
            if isinstance(record, dict) and record.get("reconciliation_status") != "reconciled"
        ]
        if unreconciled:
            errors.append(f"{data['status']} curated reader manuscript has unreconciled chapters: {unreconciled}")


def validate_reconciliation_report(data: dict[str, Any], errors: list[str]) -> None:
    report = data.get("reconciliation_report")
    if not isinstance(report, dict):
        errors.append("reconciliation_report must be an object.")
        return
    if report.get("required_before_release") is not True:
        errors.append("reconciliation_report.required_before_release must be true.")
    path = report.get("path")
    if not isinstance(path, str) or not path.startswith("editions/reader_manuscript/v1_0/"):
        errors.append("reconciliation_report.path must stay under editions/reader_manuscript/v1_0/.")
    status = report.get("status")
    if status not in ALLOWED_RECONCILIATION_STATUS:
        errors.append(f"reconciliation_report.status must be one of {sorted(ALLOWED_RECONCILIATION_STATUS)}.")
    if data.get("status") in {"release_candidate", "released"} and isinstance(path, str) and not (ROOT / path).exists():
        errors.append(f"release-ready curated reader manuscript requires reconciliation report: {path}")


def validate_docs_reference_manifest(errors: list[str]) -> None:
    required_mentions = {
        ROOT / "editions" / "README.md": "editions/reader_manuscript/",
        ROOT / "docs" / "release_editions_plan.md": "editions/reader_manuscript/v1_0/manifest.json",
        ROOT / "docs" / "major_version_release_runbook.md": "python3 scripts/validate_reader_manuscript_manifest.py",
        ROOT / "README.md": "scripts/validate_reader_manuscript_manifest.py",
    }
    for path, needle in required_mentions.items():
        text = path.read_text(encoding="utf-8", errors="ignore")
        if needle not in text:
            errors.append(f"{rel(path)} must mention {needle}.")


def main() -> None:
    errors: list[str] = []
    data = load_json(MANIFEST)
    if not isinstance(data, dict):
        errors.append(f"{rel(MANIFEST)} must contain an object.")
        data = {}
    structure = load_json(ROOT / "book_structure.json")
    chapters = flatten_chapters(structure if isinstance(structure, dict) else {})

    validate_manifest(data, errors)
    validate_chapter_records(data, chapters, errors)
    validate_reconciliation_report(data, errors)
    validate_docs_reference_manifest(errors)

    if errors:
        print("Reader manuscript manifest validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print(
        "Reader manuscript manifest validation passed: "
        f"{data.get('status')} with {len(data.get('chapter_records', []))} curated chapter record(s)."
    )


if __name__ == "__main__":
    main()
