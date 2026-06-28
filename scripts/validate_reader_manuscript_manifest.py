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
ALLOWED_ROUTING_STATUS = {
    "retain_in_reader_spine_with_companion_note",
    "future_curated_review_with_companion_note",
}
REQUIRED_ROUTING_RELEASE_BLOCKERS = {
    "reader_release_record_not_created",
    "format_artifact_not_reviewed",
    "companion_note_not_release_reviewed",
    "audio_script_not_reviewed",
}
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
    "companion_note_routing",
    "chapter_review_matrix",
    "format_review_matrix",
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

    routing = data.get("companion_note_routing")
    if not isinstance(routing, dict):
        errors.append("companion_note_routing must be an object.")
    else:
        if routing.get("path") != "editions/reader_manuscript/v1_0/companion_note_routing.json":
            errors.append(
                "companion_note_routing.path must be "
                "editions/reader_manuscript/v1_0/companion_note_routing.json."
            )
        if routing.get("review") != "docs/reader_companion_note_routing_review.md":
            errors.append("companion_note_routing.review must be docs/reader_companion_note_routing_review.md.")
        policy = routing.get("policy")
        if not isinstance(policy, str) or "reader spine" not in policy or "audio" not in policy:
            errors.append("companion_note_routing.policy must mention reader spine and audio.")
        for key in ("path", "review"):
            value = routing.get(key)
            if isinstance(value, str):
                require_existing_path(f"companion_note_routing.{key}", value, errors)

    matrix = data.get("chapter_review_matrix")
    if not isinstance(matrix, dict):
        errors.append("chapter_review_matrix must be an object.")
    else:
        expected = {
            "path": "editions/reader_manuscript/v1_0/chapter_review_matrix.json",
            "summary": "docs/reader_chapter_review_matrix.md",
            "sync_command": "python3 scripts/sync_reader_chapter_review_matrix.py --write",
            "check_command": "python3 scripts/sync_reader_chapter_review_matrix.py --check",
        }
        for key, expected_value in expected.items():
            if matrix.get(key) != expected_value:
                errors.append(f"chapter_review_matrix.{key} must be {expected_value}.")
        for key in ("path", "summary"):
            value = matrix.get(key)
            if isinstance(value, str):
                require_existing_path(f"chapter_review_matrix.{key}", value, errors)
        policy = matrix.get("policy")
        if not isinstance(policy, str) or "book_structure.json" not in policy or "release blockers" not in policy:
            errors.append("chapter_review_matrix.policy must mention book_structure.json and release blockers.")

    format_matrix = data.get("format_review_matrix")
    if not isinstance(format_matrix, dict):
        errors.append("format_review_matrix must be an object.")
    else:
        expected = {
            "path": "editions/reader_manuscript/v1_0/format_review_matrix.json",
            "summary": "docs/reader_format_review_matrix.md",
            "sync_command": "python3 scripts/sync_reader_format_review_matrix.py --write",
            "check_command": "python3 scripts/sync_reader_format_review_matrix.py --check",
        }
        for key, expected_value in expected.items():
            if format_matrix.get(key) != expected_value:
                errors.append(f"format_review_matrix.{key} must be {expected_value}.")
        for key in ("path", "summary"):
            value = format_matrix.get(key)
            if isinstance(value, str):
                require_existing_path(f"format_review_matrix.{key}", value, errors)
        policy = format_matrix.get("policy")
        if (
            not isinstance(policy, str)
            or "format artifact" not in policy
            or "edition release record" not in policy
        ):
            errors.append("format_review_matrix.policy must mention format artifact and edition release record.")


def validate_companion_note_routing(
    data: dict[str, Any],
    chapters: dict[str, dict[str, Any]],
    errors: list[str],
) -> None:
    routing_ref = data.get("companion_note_routing")
    if not isinstance(routing_ref, dict) or not isinstance(routing_ref.get("path"), str):
        return

    routing_path = ROOT / routing_ref["path"]
    if not routing_path.exists():
        return
    routing = load_json(routing_path)
    if not isinstance(routing, dict):
        errors.append(f"{rel(routing_path)} must contain an object.")
        return

    if routing.get("schema_version") != "0.1":
        errors.append(f"{rel(routing_path)} schema_version must be 0.1.")
    if routing.get("major_version") != "v1.0":
        errors.append(f"{rel(routing_path)} major_version must be v1.0.")
    if routing.get("status") != "active_review_routing":
        errors.append(f"{rel(routing_path)} status must be active_review_routing.")
    purpose = routing.get("purpose")
    if not isinstance(purpose, str) or "reader spine" not in purpose or "companion" not in purpose:
        errors.append(f"{rel(routing_path)} purpose must mention reader spine and companion routing.")

    source_refs = require_string_list("companion-note routing", "source_review_refs", routing.get("source_review_refs"), errors)
    for ref in source_refs:
        path = ref.split("#", 1)[0]
        if path and not (ROOT / path).exists():
            errors.append(f"companion-note routing source_review_refs path does not exist: {path}")

    non_claims = require_string_list("companion-note routing", "non_claims", routing.get("non_claims"), errors)
    non_claim_text = " ".join(non_claims).lower()
    for phrase in ("not a reader release", "does not move meaning-critical uncertainty", "does not promote"):
        if phrase not in non_claim_text:
            errors.append(f"companion-note routing non_claims must include boundary phrase: {phrase}")

    matrix_path = ROOT / "editions" / "reader_manuscript" / "v1_0" / "chapter_review_matrix.json"
    matrix = load_json(matrix_path) if matrix_path.exists() else {}
    matrix_rows = matrix.get("chapters", []) if isinstance(matrix, dict) else []
    companion_candidates = {
        str(row.get("chapter_id"))
        for row in matrix_rows
        if isinstance(row, dict)
        and "companion_note_candidate" in [str(item) for item in row.get("dispositions", [])]
    }

    records = routing.get("records")
    if not isinstance(records, list) or not records:
        errors.append("companion-note routing records must be a non-empty list.")
        return

    seen: set[str] = set()
    for index, record in enumerate(records):
        owner = f"companion_note_routing.records[{index}]"
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
        if chapter_id not in companion_candidates:
            errors.append(f"{owner}: {chapter_id} is not marked companion_note_candidate in the review matrix.")

        expected_title = chapters[chapter_id].get("title")
        if record.get("title") != expected_title:
            errors.append(f"{owner}: title must match book_structure.json title {expected_title!r}.")
        if record.get("routing_decision") not in ALLOWED_ROUTING_STATUS:
            errors.append(f"{owner}: routing_decision must be one of {sorted(ALLOWED_ROUTING_STATUS)}.")

        for key in ("reader_treatment", "companion_treatment", "audio_treatment"):
            value = record.get(key)
            if not isinstance(value, str) or len(value.split()) < 8:
                errors.append(f"{owner}: {key} must be a substantive sentence.")

        for key in ("dense_material", "must_remain_in_reader", "companion_note_material", "release_blockers", "non_claims"):
            require_string_list(owner, key, record.get(key), errors)

        blockers = {str(item) for item in record.get("release_blockers", []) if isinstance(item, str)}
        missing_blockers = REQUIRED_ROUTING_RELEASE_BLOCKERS - blockers
        if missing_blockers:
            errors.append(f"{owner}: release_blockers missing {sorted(missing_blockers)}.")

        reader_boundary = " ".join(str(item) for item in record.get("must_remain_in_reader", [])).lower()
        if not any(term in reader_boundary for term in ("claim", "authority", "support", "boundary", "approval")):
            errors.append(f"{owner}: must_remain_in_reader must preserve a claim, authority, support, or approval boundary.")

    missing_routes = companion_candidates - seen
    extra_routes = seen - companion_candidates
    if missing_routes:
        errors.append(f"companion-note routing missing matrix candidates: {sorted(missing_routes)}")
    if extra_routes:
        errors.append(f"companion-note routing has non-candidate records: {sorted(extra_routes)}")


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
    if isinstance(path, str):
        report_path = ROOT / path
        if report_path.exists():
            text = report_path.read_text(encoding="utf-8", errors="ignore").lower()
            for phrase in (
                "not a reader release record",
                "not a support-state promotion",
                "live ai/research book",
                "chapter_review_matrix.json",
                "generated reader source",
                "proof/test status",
                "implementation horizons",
                "release blockers",
            ):
                if phrase not in text:
                    errors.append(f"{path} must include reconciliation boundary phrase: {phrase}")
        elif data.get("status") in {"release_candidate", "released"}:
            errors.append(f"release-ready curated reader manuscript requires reconciliation report: {path}")


def validate_docs_reference_manifest(errors: list[str]) -> None:
    required_mentions = {
        ROOT / "editions" / "README.md": "editions/reader_manuscript/",
        ROOT / "docs" / "release_editions_plan.md": "editions/reader_manuscript/v1_0/manifest.json",
        ROOT / "docs" / "major_version_release_runbook.md": "python3 scripts/validate_reader_manuscript_manifest.py",
        ROOT / "README.md": "scripts/validate_reader_manuscript_manifest.py",
        ROOT / "docs" / "repository_map.md": "scripts/sync_reader_chapter_review_matrix.py --check",
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
    validate_companion_note_routing(data, chapters, errors)
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
