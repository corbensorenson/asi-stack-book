#!/usr/bin/env python3
"""Validate the v1.0 reader format-review matrix and sync its Markdown summary."""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "editions" / "reader_manuscript" / "v1_0" / "format_review_matrix.json"
SUMMARY = ROOT / "docs" / "reader_format_review_matrix.md"
EXPECTED_FORMATS = ["html", "epub", "docx", "pdf"]
ALLOWED_STATUS = {"pre_release_review_matrix"}
ALLOWED_RELEASE_RECORD_STATUS = {"not_created", "drafting", "created"}
ALLOWED_RENDER_STATUS = {"not_attempted", "rendered_local", "probe_rendered_local", "failed"}
ALLOWED_STRUCTURAL_STATUS = {"not_checked", "partial", "passed", "failed"}
ALLOWED_MANUAL_STATUS = {"not_started", "in_progress", "representative_spot_check", "pass", "fail"}
RELEASE_RECORD_BLOCKER = "reader_release_record_not_created"
FULL_REVIEW_BLOCKER = "full_format_artifact_review_not_completed"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def require_string(owner: str, key: str, value: Any, errors: list[str], *, min_words: int = 1) -> str:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{owner}: {key} must be a non-empty string.")
        return ""
    if len(value.split()) < min_words:
        errors.append(f"{owner}: {key} must contain at least {min_words} words.")
    return value


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


def validate_ref(owner: str, ref: str, errors: list[str]) -> None:
    path_part = ref.split("#", 1)[0]
    if not path_part:
        errors.append(f"{owner}: evidence ref must include a path before any anchor: {ref!r}.")
        return
    path = ROOT / path_part
    if not path.exists():
        errors.append(f"{owner}: evidence ref path does not exist: {path_part}.")


def validate_matrix(matrix: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if matrix.get("schema_version") != "0.1":
        errors.append("schema_version must be 0.1.")
    if matrix.get("major_version") != "v1.0":
        errors.append("major_version must be v1.0.")
    if matrix.get("status") not in ALLOWED_STATUS:
        errors.append(f"status must be one of {sorted(ALLOWED_STATUS)}.")
    if matrix.get("release_record_status") not in ALLOWED_RELEASE_RECORD_STATUS:
        errors.append(f"release_record_status must be one of {sorted(ALLOWED_RELEASE_RECORD_STATUS)}.")

    require_string("format review matrix", "purpose", matrix.get("purpose"), errors, min_words=8)
    release_rule = require_string("format review matrix", "release_rule", matrix.get("release_rule"), errors, min_words=14)
    if release_rule and ("release-approved" not in release_rule or "edition release record" not in release_rule):
        errors.append("release_rule must mention release-approved status and an edition release record.")

    for ref in require_string_list("format review matrix", "source_docs", matrix.get("source_docs"), errors):
        validate_ref("format review matrix source_docs", ref, errors)

    non_claims = require_string_list("format review matrix", "non_claims", matrix.get("non_claims"), errors)
    non_claim_text = " ".join(non_claims).lower()
    for phrase in ("not an edition release record", "does not publish", "does not promote", "live ai/research book"):
        if phrase not in non_claim_text:
            errors.append(f"format review matrix non_claims must include boundary phrase: {phrase}")

    release_record_path = matrix.get("release_record_path")
    if matrix.get("release_record_status") == "created":
        if not isinstance(release_record_path, str) or not release_record_path:
            errors.append("created release_record_status requires release_record_path.")
        elif not (ROOT / release_record_path).exists():
            errors.append(f"release_record_path does not exist: {release_record_path}")
    elif release_record_path not in ("", None):
        errors.append("release_record_path must stay empty until release_record_status is created.")

    records = matrix.get("records")
    if not isinstance(records, list) or not records:
        errors.append("records must be a non-empty list.")
        return errors

    seen: set[str] = set()
    blocker_counts: Counter[str] = Counter()
    for index, record in enumerate(records):
        owner = f"records[{index}]"
        if not isinstance(record, dict):
            errors.append(f"{owner} must be an object.")
            continue

        fmt = record.get("format")
        if not isinstance(fmt, str) or not fmt:
            errors.append(f"{owner}: format must be a non-empty string.")
            continue
        if fmt in seen:
            errors.append(f"{owner}: duplicate format {fmt}.")
        seen.add(fmt)

        if record.get("render_status") not in ALLOWED_RENDER_STATUS:
            errors.append(f"{owner}: render_status must be one of {sorted(ALLOWED_RENDER_STATUS)}.")
        if record.get("structural_inspection_status") not in ALLOWED_STRUCTURAL_STATUS:
            errors.append(f"{owner}: structural_inspection_status must be one of {sorted(ALLOWED_STRUCTURAL_STATUS)}.")
        if record.get("manual_layout_review_status") not in ALLOWED_MANUAL_STATUS:
            errors.append(f"{owner}: manual_layout_review_status must be one of {sorted(ALLOWED_MANUAL_STATUS)}.")
        if not isinstance(record.get("release_approved"), bool):
            errors.append(f"{owner}: release_approved must be a boolean.")

        require_string(owner, "artifact_scope", record.get("artifact_scope"), errors, min_words=6)
        require_string(owner, "notes", record.get("notes"), errors, min_words=14)
        for ref in require_string_list(owner, "evidence_refs", record.get("evidence_refs"), errors):
            validate_ref(f"{owner}.evidence_refs", ref, errors)

        raw_blockers = record.get("release_blockers")
        if not isinstance(raw_blockers, list):
            errors.append(f"{owner}: release_blockers must be a list.")
            blockers = []
        elif record.get("release_approved") is False and not raw_blockers:
            errors.append(f"{owner}: unapproved format must have at least one release_blocker.")
            blockers = []
        else:
            blockers = []
            for blocker in raw_blockers:
                if not isinstance(blocker, str) or not blocker.strip():
                    errors.append(f"{owner}: release_blockers entries must be non-empty strings.")
                else:
                    blockers.append(blocker)
        for blocker in blockers:
            blocker_counts[blocker] += 1
        if (
            matrix.get("release_record_status") != "created"
            and record.get("release_approved") is False
            and RELEASE_RECORD_BLOCKER not in blockers
        ):
            errors.append(f"{owner}: unapproved format missing blocker {RELEASE_RECORD_BLOCKER!r}.")
        if matrix.get("release_record_status") == "created" and RELEASE_RECORD_BLOCKER in blockers:
            errors.append(f"{owner}: release record exists, so blocker {RELEASE_RECORD_BLOCKER!r} should be removed.")
        full_review_passed = (
            record.get("render_status") in {"rendered_local", "probe_rendered_local"}
            and record.get("structural_inspection_status") == "passed"
            and record.get("manual_layout_review_status") == "pass"
        )
        if record.get("release_approved") is False and not full_review_passed and FULL_REVIEW_BLOCKER not in blockers:
            errors.append(f"{owner}: format without full review pass must keep blocker {FULL_REVIEW_BLOCKER!r}.")
        if full_review_passed and FULL_REVIEW_BLOCKER in blockers:
            errors.append(f"{owner}: full review passed, so blocker {FULL_REVIEW_BLOCKER!r} should be removed.")
        if record.get("release_approved") is True and blockers:
            errors.append(f"{owner}: release_approved true requires no release_blockers.")

        row_non_claims = require_string_list(owner, "non_claims", record.get("non_claims"), errors)
        row_non_claim_text = " ".join(row_non_claims).lower()
        for phrase in ("not a release record", "does not approve", "does not promote"):
            if phrase not in row_non_claim_text:
                errors.append(f"{owner}: non_claims must include boundary phrase: {phrase}")

    missing_formats = sorted(set(EXPECTED_FORMATS) - seen)
    extra_formats = sorted(seen - set(EXPECTED_FORMATS))
    if missing_formats:
        errors.append(f"records missing expected format(s): {missing_formats}")
    if extra_formats:
        errors.append(f"records contain unexpected format(s): {extra_formats}")

    expected_counts = dict(sorted(blocker_counts.items()))
    if matrix.get("release_blocker_counts") != expected_counts:
        errors.append(f"release_blocker_counts must equal {expected_counts}.")

    return errors


def markdown_table(matrix: dict[str, Any]) -> str:
    records = matrix.get("records", [])
    counts = matrix.get("release_blocker_counts", {})
    lines = [
        "# Reader Format Review Matrix",
        "",
        f"Last updated: {matrix.get('last_updated', '')}",
        "",
        "This generated summary is synced from `editions/reader_manuscript/v1_0/format_review_matrix.json`. It records local reader-format review evidence and blockers. It is not itself an edition release record, artifact approval, or support-state promotion.",
        "",
        "## Counts",
        "",
        "| Metric | Count |",
        "|---|---:|",
    ]
    if isinstance(records, list):
        lines.append(f"| format rows | {len(records)} |")
    if isinstance(counts, dict):
        for key, value in sorted(counts.items()):
            lines.append(f"| release_blocker:{key} | {value} |")

    lines.extend(
        [
            "",
            "## Format Queue",
            "",
            "| Format | Render status | Structural status | Manual review | Release approved | Blockers | Evidence refs |",
            "|---|---|---|---|---:|---|---|",
        ]
    )

    if isinstance(records, list):
        for record in records:
            if not isinstance(record, dict):
                continue
            blockers = ", ".join(str(item) for item in record.get("release_blockers", []))
            refs = ", ".join(str(item) for item in record.get("evidence_refs", []))
            lines.append(
                "| "
                + " | ".join(
                    [
                        str(record.get("format", "")),
                        str(record.get("render_status", "")),
                        str(record.get("structural_inspection_status", "")),
                        str(record.get("manual_layout_review_status", "")),
                        "yes" if record.get("release_approved") is True else "no",
                        blockers,
                        refs,
                    ]
                )
                + " |"
            )

    lines.extend(
        [
            "",
            "## Release Rule",
            "",
            str(matrix.get("release_rule", "")),
            "",
            "## Non-Claims",
            "",
        ]
    )
    for item in matrix.get("non_claims", []):
        lines.append(f"- {item}")
    lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="write docs/reader_format_review_matrix.md")
    parser.add_argument("--check", action="store_true", help="validate the matrix and summary without writing")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    matrix = load_json(MATRIX)
    if not isinstance(matrix, dict):
        raise SystemExit(f"{rel(MATRIX)} must contain an object.")
    errors = validate_matrix(matrix)
    if errors:
        print("Reader format review matrix validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    expected_summary = markdown_table(matrix)
    if args.write:
        SUMMARY.write_text(expected_summary, encoding="utf-8")
    elif SUMMARY.exists():
        current = SUMMARY.read_text(encoding="utf-8")
        if current != expected_summary:
            raise SystemExit(
                "Reader format review matrix summary is stale. "
                "Run `python3 scripts/sync_reader_format_review_matrix.py --write`."
            )
    else:
        raise SystemExit(
            f"Missing {rel(SUMMARY)}. "
            "Run `python3 scripts/sync_reader_format_review_matrix.py --write`."
        )

    print(
        "Reader format review matrix validation passed: "
        f"{len(matrix.get('records', []))} formats, {matrix.get('release_record_status')} release record."
    )


if __name__ == "__main__":
    main()
