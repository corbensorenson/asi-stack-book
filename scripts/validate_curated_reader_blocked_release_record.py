#!/usr/bin/env python3
"""Validate the blocked curated-reader release-candidate record.

This check keeps the record useful as exact release evidence without allowing it
to drift into artifact approval. It intentionally validates against tracked
manifests and review docs, not ignored build outputs.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "release_records" / "2026-07-04-v1-curated-reader-blocked-5dc1cd46.json"
CURATED_FORMAT = ROOT / "editions" / "reader_manuscript" / "v1_0" / "curated_format_probe_manifest.json"
READER_MANIFEST = ROOT / "editions" / "reader_manuscript" / "v1_0" / "manifest.json"
HTML_REVIEW = ROOT / "docs" / "curated_reader_html_artifact_browser_review.md"
HTML_DIGEST_RE = re.compile(r"`([0-9a-f]{64})`")

EXPECTED_RELEASE_ID = "2026-07-04-v1-curated-reader-blocked-5dc1cd46"
EXPECTED_SOURCE_COMMIT = "5dc1cd467543edc97b1517901529347a6ef40052"
REQUIRED_BLOCKERS = {
    "curated_reconciliation_not_approved",
    "format_artifact_not_reviewed",
    "reader_release_record_not_created",
    "full_format_artifact_review_not_completed",
    "app_or_ereader_review_not_completed",
    "full_pdf_layout_review_not_completed",
}
REQUIRED_COMMANDS = {
    "python3 scripts/render_curated_reader_formats.py --formats html epub docx --include-pdf",
    "python3 scripts/inspect_curated_reader_format_artifacts.py",
    "python3 scripts/audit_curated_reader_pdf_layout.py",
    "node scripts/validate_reader_html_artifact_browser.js --strict --site build/curated_reader_edition/format_artifacts/html/_reader_site --manifest build/curated_reader_edition/reader_manifest.json --report build/curated_reader_edition/curated_reader_html_browser_report.json",
    "python3 scripts/validate_curated_reader_format_probe_manifest.py",
}


def fail(errors: list[str]) -> None:
    print("Blocked curated-reader release record validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def artifact_by_format(record: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    artifacts = record.get("artifact_formats", [])
    if isinstance(artifacts, list):
        for artifact in artifacts:
            if isinstance(artifact, dict) and isinstance(artifact.get("format"), str):
                result[artifact["format"]] = artifact
    return result


def text_contains_all(owner: str, text: str, fragments: list[str], errors: list[str]) -> None:
    lower = text.lower()
    for fragment in fragments:
        if fragment.lower() not in lower:
            errors.append(f"{owner} missing required fragment: {fragment}")


def main() -> None:
    errors: list[str] = []
    for path in (RECORD, CURATED_FORMAT, READER_MANIFEST, HTML_REVIEW):
        if not path.exists():
            errors.append(f"required path missing: {rel(path)}")
    if errors:
        fail(errors)

    record = load_json(RECORD)
    curated = load_json(CURATED_FORMAT)
    reader_manifest = load_json(READER_MANIFEST)
    html_review = HTML_REVIEW.read_text(encoding="utf-8")
    if not isinstance(record, dict):
        fail([f"{rel(RECORD)} must contain a JSON object."])
    if not isinstance(curated, dict):
        fail([f"{rel(CURATED_FORMAT)} must contain a JSON object."])
    if not isinstance(reader_manifest, dict):
        fail([f"{rel(READER_MANIFEST)} must contain a JSON object."])

    if record.get("record_type") != "edition_release":
        errors.append("record_type must be edition_release.")
    if record.get("release_id") != EXPECTED_RELEASE_ID:
        errors.append(f"release_id must be {EXPECTED_RELEASE_ID}.")
    if record.get("source_commit") != EXPECTED_SOURCE_COMMIT:
        errors.append(f"source_commit must remain {EXPECTED_SOURCE_COMMIT}.")
    if record.get("source_tag") != "not_tagged_curated_reader_blocked_candidate_2026-07-04":
        errors.append("source_tag must explicitly remain not tagged.")
    if record.get("edition_profile") != "reader_release":
        errors.append("edition_profile must be reader_release.")
    if record.get("validation_status") != "partial":
        errors.append("validation_status must remain partial for the blocked candidate.")

    commands = set(record.get("validation_commands", []))
    missing_commands = sorted(REQUIRED_COMMANDS - commands)
    if missing_commands:
        errors.append(f"validation_commands missing required command(s): {missing_commands}")

    artifacts = artifact_by_format(record)
    expected_formats = {
        "curated_reader_html",
        "curated_reader_epub",
        "curated_reader_docx",
        "curated_reader_pdf",
        "ereader_application_review",
        "audio",
    }
    if set(artifacts) != expected_formats:
        errors.append(f"artifact formats must be {sorted(expected_formats)}, found {sorted(artifacts)}.")
    for fmt, artifact in artifacts.items():
        if artifact.get("status") == "published":
            errors.append(f"{fmt} must not be published in a blocked candidate record.")
        text_contains_all(fmt, str(artifact.get("notes", "")), ["blocked"], errors)

    digest_matches = HTML_DIGEST_RE.findall(html_review)
    html_digest = digest_matches[0] if digest_matches else ""
    if html_digest != "4d6851d11bcb1097925956c216937ebb65e1b51af9174009d0488b0eb36d955a":
        errors.append("curated HTML review digest changed or is missing.")
    html_note = str(artifacts.get("curated_reader_html", {}).get("notes", ""))
    for fragment in (html_digest, "49 pages", "98 of 98", "not release-approved"):
        if fragment and fragment not in html_note:
            errors.append(f"curated_reader_html notes missing {fragment!r}.")

    inspection = curated.get("inspection_summary", {})
    if not isinstance(inspection, dict):
        errors.append("curated format inspection_summary must be an object.")
        inspection = {}
    expected_artifacts = {
        "curated_reader_epub": ("epub", "1507dc1658969e081ce9a80b000f28b367a32474fef02932eccf3b00494803e4"),
        "curated_reader_docx": ("docx", "9ac3b9de5b994e411cd17f4cff4bb6ffdf05abbb7de0b9b9b2329e44ddb0013c"),
        "curated_reader_pdf": ("pdf", "f39001097c0d8289980034a681d261ac737905b5840e231e2a0dba6ad8a41f2a"),
    }
    for record_format, (manifest_format, expected_sha) in expected_artifacts.items():
        manifest_row = inspection.get(manifest_format, {})
        if not isinstance(manifest_row, dict):
            errors.append(f"inspection_summary.{manifest_format} must be an object.")
            continue
        actual_sha = manifest_row.get("sha256")
        if actual_sha != expected_sha:
            errors.append(f"inspection_summary.{manifest_format}.sha256 drifted: {actual_sha}")
        note = str(artifacts.get(record_format, {}).get("notes", ""))
        if expected_sha not in note:
            errors.append(f"{record_format} notes missing tracked SHA-256 {expected_sha}.")
        byte_count = manifest_row.get("bytes")
        byte_forms = {str(byte_count), f"{byte_count:,}"} if isinstance(byte_count, int) else {str(byte_count)}
        if not any(form in note for form in byte_forms):
            errors.append(f"{record_format} notes missing tracked byte count {manifest_row.get('bytes')}.")

    residual_text = " ".join(str(item) for item in record.get("residuals", []))
    missing_blockers = sorted(REQUIRED_BLOCKERS - {blocker for blocker in REQUIRED_BLOCKERS if blocker in residual_text})
    if missing_blockers:
        errors.append(f"residuals must preserve blockers: {missing_blockers}")

    non_claim_text = " ".join(str(item) for item in record.get("non_claims", [])).lower()
    for fragment in (
        "does not approve",
        "does not publish",
        "does not create a source tag",
        "does not promote any chapter core claim",
        "does not prove asi capability",
    ):
        if fragment not in non_claim_text:
            errors.append(f"non_claims missing boundary fragment: {fragment}")

    if reader_manifest.get("status") != "drafting":
        errors.append("curated reader manifest must remain drafting until approval exists.")
    chapter_records = reader_manifest.get("chapter_records", [])
    if not isinstance(chapter_records, list) or len(chapter_records) != 44:
        errors.append("curated reader manifest must keep 44 chapter records.")
    else:
        blocker_rows = [
            record
            for record in chapter_records
            if isinstance(record, dict)
            and {"curated_reconciliation_not_approved", "format_artifact_not_reviewed", "reader_release_record_not_created"}.issubset(
                set(record.get("release_blockers", []))
            )
        ]
        if len(blocker_rows) != 44:
            errors.append("all 44 curated chapter records must preserve release blockers.")

    if errors:
        fail(errors)

    print(
        "Blocked curated-reader release record validation passed: "
        "partial candidate with HTML/EPUB/DOCX/PDF/audio blockers preserved."
    )


if __name__ == "__main__":
    main()
