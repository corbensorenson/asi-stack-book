#!/usr/bin/env python3
"""Sync the v1.0 human-reader chapter review matrix.

The matrix is a review-control surface for the normal reader manuscript. It is
allowed to track reader-only prose decisions, but it must stay manifest-aligned
and subordinate to the live AI/research book for claims, support states, source
boundaries, proof/test status, implementation horizons, and release records.
"""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import date
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "editions" / "reader_manuscript" / "v1_0" / "chapter_review_matrix.json"
DOC_PATH = ROOT / "docs" / "reader_chapter_review_matrix.md"
STRUCTURE_PATH = ROOT / "book_structure.json"
OVERLAY_CHAPTER_DIR = ROOT / "editions" / "reader_overlays" / "v1_0" / "chapters"
MANUSCRIPT_REVIEW = ROOT / "docs" / "reader_manuscript_review.md"
CONTINUITY_REVIEW = ROOT / "docs" / "reader_continuity_review.md"

ALLOWED_REVIEW_STATUS = {
    "not_started",
    "spot_checked",
    "reviewed",
    "blocked",
}
ALLOWED_REVIEW_DEPTH = {
    "none",
    "representative_spot_check",
    "medium_priority_manual_review",
    "full_chapter_review",
}
ALLOWED_DISPOSITIONS = {
    "none",
    "no_immediate_action",
    "reader_overlay_active",
    "reader_overlay_needed",
    "canonical_edit_needed",
    "companion_note_candidate",
    "curated_manuscript_candidate",
}
ALLOWED_RELEASE_BLOCKERS = {
    "full_chapter_review_not_recorded",
    "reader_release_record_not_created",
    "curated_reconciliation_not_recorded",
    "format_artifact_not_reviewed",
}

SPECIAL_REVIEW_DEFAULTS = {
    "executable-specifications-and-lean-proof-envelope": {
        "review_status": "spot_checked",
        "review_depth": "medium_priority_manual_review",
        "dispositions": ["reader_overlay_active", "companion_note_candidate", "no_immediate_action"],
        "review_refs": ["docs/reader_continuity_review.md#medium-priority-queue-decisions"],
        "review_notes": (
            "Medium-priority density row read; no additional overlay now. Future "
            "reader release work may route proof-envelope vocabulary through "
            "companion notes or glossary treatment."
        ),
    },
    "circle-calculus-and-proof-carrying-ai-contracts": {
        "review_status": "spot_checked",
        "review_depth": "medium_priority_manual_review",
        "dispositions": ["reader_overlay_active", "companion_note_candidate", "no_immediate_action"],
        "review_refs": ["docs/reader_continuity_review.md#medium-priority-queue-decisions"],
        "review_notes": (
            "Medium-priority density row read; no additional overlay now. The "
            "theorem-linked receipt boundary should stay visible, with possible "
            "companion-note or glossary treatment later."
        ),
    },
    "artifact-steward-agents-and-living-project-governance": {
        "review_status": "spot_checked",
        "review_depth": "medium_priority_manual_review",
        "dispositions": [
            "reader_overlay_active",
            "companion_note_candidate",
            "curated_manuscript_candidate",
            "no_immediate_action",
        ],
        "review_refs": ["docs/reader_continuity_review.md#medium-priority-queue-decisions"],
        "review_notes": (
            "Medium-priority length row read; retained for now because the "
            "governance, treasury, worker-federation, contribution-ledger, "
            "event-taint, and sunset concepts are central. Future curated reader "
            "work may compress examples or move the implementation ladder to "
            "companion material."
        ),
    },
}


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def flatten_manifest() -> list[dict[str, str]]:
    structure = load_json(STRUCTURE_PATH, {})
    if not isinstance(structure, dict):
        raise SystemExit("book_structure.json must contain an object.")
    rows: list[dict[str, str]] = []
    for part in structure.get("parts", []):
        if not isinstance(part, dict):
            continue
        part_id = str(part.get("id", ""))
        part_title = str(part.get("title", ""))
        for chapter in part.get("chapters", []):
            if not isinstance(chapter, dict):
                continue
            chapter_id = chapter.get("id")
            title = chapter.get("title")
            file_path = chapter.get("file")
            if not all(isinstance(value, str) and value for value in (chapter_id, title, file_path)):
                raise SystemExit(f"Invalid chapter record in {part_id}: {chapter!r}")
            rows.append(
                {
                    "part_id": part_id,
                    "part_title": part_title,
                    "chapter_id": chapter_id,
                    "title": title,
                    "live_file": file_path,
                    "generated_reader_file": f"build/reader_edition/{file_path}",
                }
            )
    return rows


def active_overlay_counts() -> Counter[str]:
    counts: Counter[str] = Counter()
    for path in sorted(OVERLAY_CHAPTER_DIR.glob("*.json")):
        data = load_json(path, {})
        if not isinstance(data, dict):
            continue
        target = data.get("target_file")
        if not isinstance(target, str):
            continue
        for operation in data.get("operations", []):
            if isinstance(operation, dict) and operation.get("status") == "active":
                counts[target] += 1
    return counts


def initial_review_defaults(row: dict[str, str], overlay_count: int) -> dict[str, object]:
    chapter_id = row["chapter_id"]
    if chapter_id in SPECIAL_REVIEW_DEFAULTS:
        special = dict(SPECIAL_REVIEW_DEFAULTS[chapter_id])
        special["release_blockers"] = [
            "full_chapter_review_not_recorded",
            "reader_release_record_not_created",
            "format_artifact_not_reviewed",
        ]
        return special

    manuscript_text = read_text(MANUSCRIPT_REVIEW)
    generated_path = row["generated_reader_file"]
    spot_checked = generated_path in manuscript_text
    dispositions = ["reader_overlay_active"] if overlay_count else ["none"]
    return {
        "review_status": "spot_checked" if spot_checked else "not_started",
        "review_depth": "representative_spot_check" if spot_checked else "none",
        "dispositions": dispositions,
        "review_refs": ["docs/reader_manuscript_review.md#generated-baseline"] if spot_checked else [],
        "review_notes": (
            "Representative generated-reader spot check recorded; still needs full chapter review."
            if spot_checked
            else "Awaiting full human-reader continuity review."
        ),
        "release_blockers": [
            "full_chapter_review_not_recorded",
            "reader_release_record_not_created",
            "format_artifact_not_reviewed",
        ],
    }


def merge_row(
    row: dict[str, str],
    existing_by_id: dict[str, dict[str, object]],
    overlay_count: int,
) -> dict[str, object]:
    existing = existing_by_id.get(row["chapter_id"], {})
    defaults = initial_review_defaults(row, overlay_count)

    dispositions = existing.get("dispositions", defaults["dispositions"])
    if isinstance(dispositions, list):
        dispositions = [str(item) for item in dispositions]
    else:
        dispositions = list(defaults["dispositions"])
    if overlay_count and "reader_overlay_active" not in dispositions:
        if dispositions == ["none"]:
            dispositions = []
        dispositions.insert(0, "reader_overlay_active")
    if not dispositions:
        dispositions = ["none"]

    review_refs = existing.get("review_refs", defaults["review_refs"])
    if not isinstance(review_refs, list):
        review_refs = list(defaults["review_refs"])

    release_blockers = existing.get("release_blockers", defaults["release_blockers"])
    if not isinstance(release_blockers, list):
        release_blockers = list(defaults["release_blockers"])

    synced: dict[str, object] = {
        **row,
        "overlay_operation_count": overlay_count,
        "review_status": existing.get("review_status", defaults["review_status"]),
        "review_depth": existing.get("review_depth", defaults["review_depth"]),
        "dispositions": dispositions,
        "review_refs": review_refs,
        "review_notes": existing.get("review_notes", defaults["review_notes"]),
        "release_blockers": release_blockers,
    }
    return synced


def build_matrix() -> dict[str, object]:
    manifest_rows = flatten_manifest()
    existing = load_json(MATRIX_PATH, {})
    existing_rows: list[dict[str, object]] = []
    if isinstance(existing, dict) and isinstance(existing.get("chapters"), list):
        existing_rows = [row for row in existing["chapters"] if isinstance(row, dict)]
    existing_by_id = {
        str(row.get("chapter_id")): row
        for row in existing_rows
        if isinstance(row.get("chapter_id"), str)
    }

    overlay_counts = active_overlay_counts()
    chapters = [
        merge_row(row, existing_by_id, overlay_counts[row["live_file"]])
        for row in manifest_rows
    ]

    status_counts = Counter(str(row["review_status"]) for row in chapters)
    disposition_counts: Counter[str] = Counter()
    for row in chapters:
        for disposition in row["dispositions"]:
            disposition_counts[str(disposition)] += 1

    last_updated = "2026-06-28"
    if isinstance(existing, dict) and isinstance(existing.get("last_updated"), str):
        last_updated = existing["last_updated"]
    elif MATRIX_PATH.exists():
        last_updated = date.today().isoformat()

    return {
        "schema_version": "0.1",
        "major_version": "v1.0",
        "status": "active_review_queue",
        "last_updated": last_updated,
        "source_of_truth": "book_structure.json",
        "generated_reader_baseline": {
            "command": "python3 scripts/build_reader_edition.py",
            "workspace": "build/reader_edition",
            "policy": "Review generated reader source and overlays before graduating any curated reader manuscript chapter.",
        },
        "review_status_counts": dict(sorted(status_counts.items())),
        "disposition_counts": dict(sorted(disposition_counts.items())),
        "release_rule": (
            "No reader, ebook, document, PDF, audio, or curated manuscript release "
            "can use a chapter until its review status and blockers are reconciled "
            "in a release record."
        ),
        "chapters": chapters,
        "non_claims": [
            "This matrix is a reader-review queue, not a reviewed reader release.",
            "This matrix does not create EPUB, PDF, DOCX, HTML, audio, or audio-embedded EPUB artifacts.",
            "This matrix does not promote any claim support state.",
            "This matrix does not supersede the live Quarto book for claims, source boundaries, proof/test status, implementation horizons, or release records.",
        ],
    }


def validate_matrix(matrix: dict[str, object]) -> list[str]:
    errors: list[str] = []
    manifest_rows = flatten_manifest()
    manifest_ids = [row["chapter_id"] for row in manifest_rows]
    manifest_by_id = {row["chapter_id"]: row for row in manifest_rows}
    overlay_counts = active_overlay_counts()

    if matrix.get("schema_version") != "0.1":
        errors.append("chapter_review_matrix.schema_version must be 0.1.")
    if matrix.get("major_version") != "v1.0":
        errors.append("chapter_review_matrix.major_version must be v1.0.")
    if matrix.get("status") != "active_review_queue":
        errors.append("chapter_review_matrix.status must be active_review_queue.")
    if matrix.get("source_of_truth") != "book_structure.json":
        errors.append("chapter_review_matrix.source_of_truth must be book_structure.json.")
    for phrase in ("does not promote", "does not supersede", "does not create"):
        if phrase not in " ".join(str(item) for item in matrix.get("non_claims", [])).lower():
            errors.append(f"chapter_review_matrix.non_claims must include phrase: {phrase}")

    chapters = matrix.get("chapters")
    if not isinstance(chapters, list):
        errors.append("chapter_review_matrix.chapters must be a list.")
        return errors

    ids = [row.get("chapter_id") for row in chapters if isinstance(row, dict)]
    if ids != manifest_ids:
        errors.append("chapter_review_matrix chapter order must exactly match book_structure.json.")
    if len(ids) != len(set(ids)):
        errors.append("chapter_review_matrix has duplicate chapter_id values.")

    for index, row in enumerate(chapters):
        owner = f"chapters[{index}]"
        if not isinstance(row, dict):
            errors.append(f"{owner} must be an object.")
            continue
        chapter_id = row.get("chapter_id")
        if not isinstance(chapter_id, str) or chapter_id not in manifest_by_id:
            errors.append(f"{owner}.chapter_id must reference a manifest chapter.")
            continue
        manifest_row = manifest_by_id[chapter_id]
        for key in ("part_id", "part_title", "title", "live_file", "generated_reader_file"):
            if row.get(key) != manifest_row[key]:
                errors.append(f"{owner}.{key} must match book_structure.json-derived value.")
        expected_overlay_count = overlay_counts[manifest_row["live_file"]]
        if row.get("overlay_operation_count") != expected_overlay_count:
            errors.append(f"{owner}.overlay_operation_count must be {expected_overlay_count}.")
        if row.get("review_status") not in ALLOWED_REVIEW_STATUS:
            errors.append(f"{owner}.review_status must be one of {sorted(ALLOWED_REVIEW_STATUS)}.")
        if row.get("review_depth") not in ALLOWED_REVIEW_DEPTH:
            errors.append(f"{owner}.review_depth must be one of {sorted(ALLOWED_REVIEW_DEPTH)}.")
        dispositions = row.get("dispositions")
        if not isinstance(dispositions, list) or not dispositions:
            errors.append(f"{owner}.dispositions must be a non-empty list.")
        else:
            unknown = sorted(set(str(item) for item in dispositions) - ALLOWED_DISPOSITIONS)
            if unknown:
                errors.append(f"{owner}.dispositions has unknown values: {unknown}")
            if "none" in dispositions and len(dispositions) > 1:
                errors.append(f"{owner}.dispositions cannot combine none with other dispositions.")
            if expected_overlay_count and "reader_overlay_active" not in dispositions:
                errors.append(f"{owner}.dispositions must include reader_overlay_active.")
        for list_key in ("review_refs", "release_blockers"):
            values = row.get(list_key)
            if not isinstance(values, list):
                errors.append(f"{owner}.{list_key} must be a list.")
                continue
            if list_key == "release_blockers":
                unknown = sorted(set(str(item) for item in values) - ALLOWED_RELEASE_BLOCKERS)
                if unknown:
                    errors.append(f"{owner}.release_blockers has unknown values: {unknown}")
        notes = row.get("review_notes")
        if not isinstance(notes, str) or not notes.strip():
            errors.append(f"{owner}.review_notes must be a non-empty string.")
        if row.get("review_status") == "reviewed" and "full_chapter_review_not_recorded" in row.get("release_blockers", []):
            errors.append(f"{owner} cannot be reviewed while full_chapter_review_not_recorded remains.")

    return errors


def markdown_table(matrix: dict[str, object]) -> str:
    chapters = matrix.get("chapters", [])
    status_counts = matrix.get("review_status_counts", {})
    disposition_counts = matrix.get("disposition_counts", {})
    lines = [
        "# Reader Chapter Review Matrix",
        "",
        f"Last updated: {matrix.get('last_updated')}",
        "",
        "This document is generated from `editions/reader_manuscript/v1_0/chapter_review_matrix.json` by `python3 scripts/sync_reader_chapter_review_matrix.py --write`.",
        "",
        "It is a Phase 2 review-control surface for the normal human-reader manuscript. It is not a reader release, not an ebook/document/PDF/audio release, and not a support-state promotion.",
        "",
        "## Counts",
        "",
        "| Kind | Count |",
        "|---|---:|",
    ]
    if isinstance(status_counts, dict):
        for key, value in sorted(status_counts.items()):
            lines.append(f"| review_status:{key} | {value} |")
    if isinstance(disposition_counts, dict):
        for key, value in sorted(disposition_counts.items()):
            lines.append(f"| disposition:{key} | {value} |")

    lines.extend(
        [
            "",
            "## Chapter Queue",
            "",
            "| Part | Chapter | Review status | Depth | Overlays | Dispositions | Release blockers |",
            "|---|---|---|---|---:|---|---|",
        ]
    )
    for row in chapters if isinstance(chapters, list) else []:
        if not isinstance(row, dict):
            continue
        dispositions = ", ".join(str(item) for item in row.get("dispositions", []))
        blockers = ", ".join(str(item) for item in row.get("release_blockers", []))
        lines.append(
            "| "
            f"{row.get('part_title')} | "
            f"`{row.get('chapter_id')}` | "
            f"{row.get('review_status')} | "
            f"{row.get('review_depth')} | "
            f"{row.get('overlay_operation_count')} | "
            f"{dispositions} | "
            f"{blockers} |"
        )

    lines.extend(
        [
            "",
            "## Non-Claims",
            "",
        ]
    )
    for item in matrix.get("non_claims", []):
        lines.append(f"- {item}")
    lines.append("")
    return "\n".join(lines)


def write_outputs(matrix: dict[str, object]) -> None:
    MATRIX_PATH.parent.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)
    MATRIX_PATH.write_text(json.dumps(matrix, indent=2) + "\n", encoding="utf-8")
    DOC_PATH.write_text(markdown_table(matrix), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="write synced JSON and Markdown outputs")
    parser.add_argument("--check", action="store_true", help="fail if synced outputs differ")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.write and args.check:
        raise SystemExit("Use either --write or --check, not both.")
    matrix = build_matrix()
    errors = validate_matrix(matrix)
    if errors:
        print("Reader chapter review matrix validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    if args.write:
        write_outputs(matrix)
        print(
            "Reader chapter review matrix synced: "
            f"{len(matrix['chapters'])} chapters, "
            f"{matrix['review_status_counts']}"
        )
        return

    if args.check:
        current_matrix = MATRIX_PATH.read_text(encoding="utf-8") if MATRIX_PATH.exists() else ""
        expected_matrix = json.dumps(matrix, indent=2) + "\n"
        current_doc = DOC_PATH.read_text(encoding="utf-8") if DOC_PATH.exists() else ""
        expected_doc = markdown_table(matrix)
        if current_matrix != expected_matrix or current_doc != expected_doc:
            print("Reader chapter review matrix is out of sync. Run:")
            print("  python3 scripts/sync_reader_chapter_review_matrix.py --write")
            sys.exit(1)
        print(
            "Reader chapter review matrix validation passed: "
            f"{len(matrix['chapters'])} chapters, "
            f"{matrix['review_status_counts']}"
        )
        return

    print(json.dumps(matrix, indent=2))


if __name__ == "__main__":
    main()
