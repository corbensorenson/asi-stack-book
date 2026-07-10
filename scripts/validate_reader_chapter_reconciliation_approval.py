#!/usr/bin/env python3
"""Validate the curated reader chapter-reconciliation approval record."""

from __future__ import annotations

import argparse
from collections import Counter
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STRUCTURE = ROOT / "book_structure.json"
READER_MANIFEST = ROOT / "editions" / "reader_manuscript" / "v1_0" / "manifest.json"
CHAPTER_MATRIX = ROOT / "editions" / "reader_manuscript" / "v1_0" / "chapter_review_matrix.json"
RECONCILIATION_REPORT = ROOT / "editions" / "reader_manuscript" / "v1_0" / "reconciliation_report.md"
RESULT = ROOT / "editions" / "reader_manuscript" / "v1_0" / "chapter_reconciliation_approval_manifest.json"
DOC = ROOT / "docs" / "reader_chapter_reconciliation_approval.md"
COMMAND = "python3 scripts/validate_reader_chapter_reconciliation_approval.py"
RESULT_ID = "reader-chapter-reconciliation-approval-2026-07-05"

EXPECTED_CHAPTERS = 44
CHAPTER_RELEASE_BLOCKERS = {
    "format_artifact_not_reviewed",
    "reader_release_record_not_created",
}
CLEARED_BLOCKERS = ["curated_reconciliation_not_approved"]
PRESERVED_BLOCKERS = [
    "format_artifact_not_reviewed",
    "reader_release_record_not_created",
    "reader_release_approval_not_created",
    "app_or_ereader_review_not_completed",
    "docx_application_review_not_completed",
    "manual_keyboard_only_review_not_completed",
    "screen_reader_review_not_completed",
    "wcag_conformance_review_not_completed",
    "narration_quality_review_not_completed",
    "audio_files_not_generated",
]
LIVE_ONLY_MARKERS = (
    "Chapter status",
    "Drafting guardrail",
    "Codex test plan",
    "Source crosswalk",
    "Claim-source mapping status",
    "Formalization hooks",
)
RAW_CORE_CLAIM_RE = re.compile(r"\[[A-Za-z0-9_-]+\.core,\s*label:")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Reader chapter reconciliation approval validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def flatten_chapters(structure: dict[str, Any]) -> list[dict[str, Any]]:
    chapters: list[dict[str, Any]] = []
    for part in structure.get("parts", []):
        if not isinstance(part, dict):
            continue
        for chapter in part.get("chapters", []):
            if isinstance(chapter, dict):
                chapters.append(chapter)
    return chapters


def historical_reader_chapters(
    structure: dict[str, Any], reader_manifest: dict[str, Any]
) -> list[dict[str, Any]]:
    """Resolve the frozen v1.0 reader review set without inheriting new chapters."""

    chapters = flatten_chapters(structure)
    if reader_manifest.get("edition_scope") != "historical_release_snapshot":
        return chapters
    snapshot = reader_manifest.get("historical_spine_snapshot")
    if not isinstance(snapshot, dict):
        fail(["historical reader manuscript is missing historical_spine_snapshot."])
    chapter_ids = snapshot.get("chapter_ids")
    if not isinstance(chapter_ids, list) or not all(isinstance(value, str) for value in chapter_ids):
        fail(["historical reader snapshot chapter_ids must be a string list."])
    by_chapter_id = {str(chapter.get("id", "")): chapter for chapter in chapters}
    missing = [chapter_id for chapter_id in chapter_ids if chapter_id not in by_chapter_id]
    if missing:
        fail([f"historical reader snapshot chapter(s) missing from active manifest: {missing}"])
    return [by_chapter_id[chapter_id] for chapter_id in chapter_ids]


def by_id(rows: list[Any], key: str) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for row in rows:
        if not isinstance(row, dict):
            continue
        value = row.get(key)
        if isinstance(value, str) and value:
            result[value] = row
    return result


def inspect_chapter(
    chapter: dict[str, Any],
    record: dict[str, Any] | None,
    matrix_row: dict[str, Any] | None,
    errors: list[str],
) -> dict[str, Any]:
    chapter_id = str(chapter.get("id", ""))
    title = str(chapter.get("title", ""))
    file_ref = str(record.get("file", "")) if isinstance(record, dict) else ""
    path = ROOT / file_ref if file_ref else None
    text = path.read_text(encoding="utf-8") if path and path.exists() else ""
    blockers = set(record.get("release_blockers", [])) if isinstance(record, dict) else set()
    matrix_blockers = set(matrix_row.get("release_blockers", [])) if isinstance(matrix_row, dict) else set()
    live_marker_hits = [marker for marker in LIVE_ONLY_MARKERS if marker in text]
    raw_claim_marker = RAW_CORE_CLAIM_RE.search(text) is not None

    row_errors: list[str] = []
    if record is None:
        row_errors.append("missing reader-manuscript chapter record")
    if matrix_row is None:
        row_errors.append("missing chapter-review matrix row")
    if path is None or not path.exists():
        row_errors.append(f"missing curated reader chapter file: {file_ref}")
    if isinstance(record, dict) and record.get("title") != title:
        row_errors.append("reader-manuscript record title does not match book_structure.json")
    if isinstance(record, dict) and record.get("reconciliation_status") != "reconciled":
        row_errors.append("reader-manuscript reconciliation_status is not reconciled")
    if isinstance(record, dict) and record.get("canonical_change_required") is not False:
        row_errors.append("canonical_change_required is not false")
    if CLEARED_BLOCKERS[0] in blockers:
        row_errors.append("cleared reconciliation blocker is still present on reader-manuscript record")
    missing_blockers = sorted(CHAPTER_RELEASE_BLOCKERS - blockers)
    if missing_blockers:
        row_errors.append(f"reader-manuscript release_blockers missing {missing_blockers}")
    if isinstance(matrix_row, dict) and matrix_row.get("review_status") != "reviewed":
        row_errors.append("chapter-review matrix row is not reviewed")
    if isinstance(matrix_row, dict) and matrix_row.get("review_depth") != "full_chapter_review":
        row_errors.append("chapter-review matrix row is not full_chapter_review")
    if isinstance(matrix_row, dict) and "curated_manuscript_candidate" not in matrix_row.get("dispositions", []):
        row_errors.append("chapter-review matrix row is not marked curated_manuscript_candidate")
    missing_matrix_blockers = sorted(CHAPTER_RELEASE_BLOCKERS - matrix_blockers)
    if missing_matrix_blockers:
        row_errors.append(f"chapter-review matrix release_blockers missing {missing_matrix_blockers}")
    if live_marker_hits:
        row_errors.append(f"curated source has live-only marker leaks: {live_marker_hits}")
    if raw_claim_marker:
        row_errors.append("curated source has raw core-claim marker leakage")

    for error in row_errors:
        errors.append(f"{chapter_id}: {error}.")

    return {
        "chapter_id": chapter_id,
        "title": title,
        "file": file_ref,
        "record_present": record is not None,
        "matrix_row_present": matrix_row is not None,
        "curated_file_exists": bool(path and path.exists()),
        "reconciliation_status": record.get("reconciliation_status") if isinstance(record, dict) else "",
        "matrix_review_status": matrix_row.get("review_status") if isinstance(matrix_row, dict) else "",
        "matrix_review_depth": matrix_row.get("review_depth") if isinstance(matrix_row, dict) else "",
        "chapter_release_blockers": sorted(str(item) for item in blockers),
        "matrix_release_blockers": sorted(str(item) for item in matrix_blockers),
        "live_marker_hits": live_marker_hits,
        "raw_core_claim_marker_leak": raw_claim_marker,
        "passed": not row_errors,
    }


def build_observed() -> dict[str, Any]:
    errors: list[str] = []
    structure = load_json(STRUCTURE)
    reader_manifest = load_json(READER_MANIFEST)
    chapter_matrix = load_json(CHAPTER_MATRIX)
    if not isinstance(structure, dict):
        fail([f"{rel(STRUCTURE)} must contain an object."])
    if not isinstance(reader_manifest, dict):
        fail([f"{rel(READER_MANIFEST)} must contain an object."])
    if not isinstance(chapter_matrix, dict):
        fail([f"{rel(CHAPTER_MATRIX)} must contain an object."])

    chapters = historical_reader_chapters(structure, reader_manifest)
    records = reader_manifest.get("chapter_records", [])
    matrix_rows = chapter_matrix.get("chapters", [])
    if not isinstance(records, list):
        fail(["reader manuscript chapter_records must be a list."])
    if not isinstance(matrix_rows, list):
        fail(["chapter review matrix chapters must be a list."])

    record_map = by_id(records, "chapter_id")
    matrix_map = by_id(matrix_rows, "chapter_id")
    rows = [
        inspect_chapter(chapter, record_map.get(str(chapter.get("id", ""))), matrix_map.get(str(chapter.get("id", ""))), errors)
        for chapter in chapters
    ]
    blocker_counter: Counter[str] = Counter()
    for row in rows:
        for blocker in row["chapter_release_blockers"]:
            blocker_counter[blocker] += 1

    report_text = RECONCILIATION_REPORT.read_text(encoding="utf-8", errors="ignore") if RECONCILIATION_REPORT.exists() else ""
    for phrase in (
        "not a reader release record",
        "not a support-state promotion",
        "chapter_review_matrix.json",
        "generated reader source",
        "release blockers",
    ):
        if phrase not in report_text.lower():
            errors.append(f"{rel(RECONCILIATION_REPORT)} missing required boundary phrase: {phrase}.")

    summary = {
        "chapter_count": len(chapters),
        "reader_manifest_records": len(records),
        "chapter_review_matrix_rows": len(matrix_rows),
        "reconciled_records": sum(1 for row in rows if row["reconciliation_status"] == "reconciled"),
        "reviewed_matrix_rows": sum(1 for row in rows if row["matrix_review_status"] == "reviewed"),
        "full_chapter_review_rows": sum(1 for row in rows if row["matrix_review_depth"] == "full_chapter_review"),
        "curated_files_present": sum(1 for row in rows if row["curated_file_exists"] is True),
        "passed_rows": sum(1 for row in rows if row["passed"] is True),
        "live_marker_hits": sum(len(row["live_marker_hits"]) for row in rows),
        "raw_core_claim_marker_hits": sum(1 for row in rows if row["raw_core_claim_marker_leak"] is True),
        "remaining_chapter_release_blocker_counts": dict(sorted(blocker_counter.items())),
    }
    status = "passed_curated_chapter_reconciliation_approval" if not errors else "failed_curated_chapter_reconciliation_approval"
    return {
        "schema_version": "asi_stack.reader_chapter_reconciliation_approval.v0",
        "result_id": RESULT_ID,
        "status": status,
        "command": COMMAND,
        "source_refs": [
            rel(STRUCTURE),
            rel(READER_MANIFEST),
            rel(CHAPTER_MATRIX),
            rel(RECONCILIATION_REPORT),
        ],
        "summary": summary,
        "chapters": rows,
        "cleared_blockers": CLEARED_BLOCKERS,
        "release_blockers_preserved": PRESERVED_BLOCKERS,
        "review_decision": (
            "The tracked curated reader manuscript has 44 reconciled chapter records, 44 full-review "
            "chapter-matrix rows, 44 existing curated chapter files, no live-scaffold marker leakage, "
            "and no raw core-claim marker leakage. This source-level approval clears only the "
            "curated_reconciliation_not_approved blocker."
        ),
        "review_boundary": (
            "This is a chapter-reconciliation approval for the curated reader source, not a reader "
            "release record. It does not approve HTML, EPUB, DOCX, PDF, e-reader, audio, or "
            "audio-embedded EPUB artifacts; does not clear format review; does not clear reader "
            "release approval; does not certify accessibility; and does not promote any claim "
            "support state."
        ),
        "non_claims": [
            "does not approve, publish, tag, or archive any reader artifact",
            "does not clear format artifact review or reader release approval",
            "does not clear dedicated e-reader, DOCX application, manual keyboard-only, screen-reader, WCAG, narration, audio, or audio-embedded EPUB review",
            "does not promote any chapter core claim or Appendix C support state",
            "does not make the curated reader manuscript equal authority beside the live AI/research book",
        ],
        "errors": errors,
    }


def validate_result(result: dict[str, Any]) -> list[str]:
    errors = list(result.get("errors", []))
    if result.get("schema_version") != "asi_stack.reader_chapter_reconciliation_approval.v0":
        errors.append("schema_version must be asi_stack.reader_chapter_reconciliation_approval.v0.")
    if result.get("status") != "passed_curated_chapter_reconciliation_approval":
        errors.append("status must be passed_curated_chapter_reconciliation_approval.")
    summary = result.get("summary", {})
    if not isinstance(summary, dict):
        return errors + ["summary must be an object."]
    exact = {
        "chapter_count": EXPECTED_CHAPTERS,
        "reader_manifest_records": EXPECTED_CHAPTERS,
        "chapter_review_matrix_rows": EXPECTED_CHAPTERS,
        "reconciled_records": EXPECTED_CHAPTERS,
        "reviewed_matrix_rows": EXPECTED_CHAPTERS,
        "full_chapter_review_rows": EXPECTED_CHAPTERS,
        "curated_files_present": EXPECTED_CHAPTERS,
        "passed_rows": EXPECTED_CHAPTERS,
        "live_marker_hits": 0,
        "raw_core_claim_marker_hits": 0,
    }
    for key, expected in exact.items():
        if summary.get(key) != expected:
            errors.append(f"summary.{key} must be {expected!r}; found {summary.get(key)!r}.")
    blocker_counts = summary.get("remaining_chapter_release_blocker_counts", {})
    if blocker_counts != {
        "format_artifact_not_reviewed": EXPECTED_CHAPTERS,
        "reader_release_record_not_created": EXPECTED_CHAPTERS,
    }:
        errors.append("remaining_chapter_release_blocker_counts must preserve only format and release-record blockers for all chapters.")
    if result.get("cleared_blockers") != CLEARED_BLOCKERS:
        errors.append("cleared_blockers must contain only curated_reconciliation_not_approved.")
    preserved = set(result.get("release_blockers_preserved", []))
    for blocker in PRESERVED_BLOCKERS:
        if blocker not in preserved:
            errors.append(f"release_blockers_preserved missing {blocker}.")
    boundary = str(result.get("review_boundary", "")).lower()
    for phrase in (
        "not a reader release record",
        "does not approve html",
        "does not clear format review",
        "does not clear reader release approval",
        "does not certify accessibility",
        "does not promote any claim support state",
    ):
        if phrase not in boundary:
            errors.append(f"review_boundary missing {phrase!r}.")
    non_claim_text = " ".join(str(item) for item in result.get("non_claims", [])).lower()
    for phrase in (
        "does not approve",
        "does not clear format artifact review",
        "does not clear dedicated e-reader",
        "does not promote any chapter core claim",
        "does not make the curated reader manuscript equal authority",
    ):
        if phrase not in non_claim_text:
            errors.append(f"non_claims missing {phrase!r}.")
    return errors


def render_doc(result: dict[str, Any]) -> str:
    summary = result["summary"]
    cleared = ", ".join(f"`{item}`" for item in result["cleared_blockers"])
    preserved = ", ".join(f"`{item}`" for item in result["release_blockers_preserved"])
    return "\n".join(
        [
            "# Reader Chapter Reconciliation Approval",
            "",
            f"Generated by `{COMMAND} --write-result`.",
            "",
            "This review approves the current source-level reconciliation state for the tracked curated reader manuscript. It is not a reader release record and does not approve any rendered artifact.",
            "",
            "## Summary",
            "",
            "| Metric | Value |",
            "|---|---:|",
            f"| Status | `{result['status']}` |",
            f"| Book chapters | {summary['chapter_count']} |",
            f"| Reader manifest records | {summary['reader_manifest_records']} |",
            f"| Chapter review matrix rows | {summary['chapter_review_matrix_rows']} |",
            f"| Reconciled records | {summary['reconciled_records']} |",
            f"| Full chapter review rows | {summary['full_chapter_review_rows']} |",
            f"| Curated files present | {summary['curated_files_present']} |",
            f"| Passed rows | {summary['passed_rows']} |",
            f"| Live-marker hits | {summary['live_marker_hits']} |",
            f"| Raw core-claim marker hits | {summary['raw_core_claim_marker_hits']} |",
            "",
            "## Blocker Decision",
            "",
            f"Cleared blocker for the current curated reader source: {cleared}.",
            "",
            f"Preserved blockers: {preserved}.",
            "",
            result["review_decision"],
            "",
            "## Boundary",
            "",
            result["review_boundary"],
            "",
            "## Non-Claims",
            "",
            "- This review does not approve, publish, tag, or archive any reader artifact.",
            "- This review does not clear format artifact review or reader release approval.",
            "- This review does not clear dedicated e-reader, DOCX application, manual keyboard-only, screen-reader, WCAG, narration, audio, or audio-embedded EPUB review.",
            "- This review does not promote any chapter core claim or Appendix C support state.",
            "- This review does not make the curated reader manuscript equal authority beside the live AI/research book.",
            "",
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-result", action="store_true")
    args = parser.parse_args()

    for path in (STRUCTURE, READER_MANIFEST, CHAPTER_MATRIX, RECONCILIATION_REPORT):
        if not path.exists():
            fail([f"required path missing: {rel(path)}"])

    observed = build_observed()
    errors = validate_result(observed)
    doc = render_doc(observed)
    if args.write_result:
        RESULT.write_text(json.dumps(observed, indent=2) + "\n", encoding="utf-8")
        DOC.write_text(doc, encoding="utf-8")
    else:
        if not RESULT.exists():
            errors.append(f"{rel(RESULT)} is missing; run with --write-result.")
        elif load_json(RESULT) != observed:
            errors.append(f"{rel(RESULT)} is stale; run with --write-result.")
        if not DOC.exists():
            errors.append(f"{rel(DOC)} is missing; run with --write-result.")
        elif DOC.read_text(encoding="utf-8") != doc:
            errors.append(f"{rel(DOC)} is stale; run with --write-result.")
    if errors:
        fail(errors)
    print(
        "Reader chapter reconciliation approval passed: "
        f"{observed['summary']['passed_rows']} curated chapters reconciled."
    )


if __name__ == "__main__":
    main()
