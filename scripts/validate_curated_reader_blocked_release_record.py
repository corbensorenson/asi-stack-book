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
KEY_FIGURE_FORMAT = ROOT / "editions" / "reader_manuscript" / "v1_0" / "key_figure_format_probe_manifest.json"
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
    "python3 scripts/sync_curated_reader_format_probe_manifest.py",
    "python3 scripts/repair_curated_reader_epub_links.py",
    "python3 scripts/repair_curated_reader_docx_links.py",
    "python3 scripts/audit_curated_reader_pdf_layout.py",
    "python3 scripts/audit_curated_reader_pdf_visual_raster.py",
    "python3 scripts/audit_curated_reader_epub_content.py",
    "python3 scripts/audit_curated_reader_docx_content.py",
    "node scripts/validate_reader_html_artifact_browser.js --strict --site build/curated_reader_edition/format_artifacts/html/_reader_site --manifest build/curated_reader_edition/reader_manifest.json --report build/curated_reader_edition/curated_reader_html_browser_report.json",
    "python3 scripts/validate_curated_reader_format_probe_manifest.py",
    "python3 scripts/validate_reader_key_figure_format_probe.py",
    "python3 scripts/validate_reader_audio_script_probe_manifest.py",
    "python3 scripts/validate_release_surface_status_ledger.py",
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
    for path in (RECORD, CURATED_FORMAT, KEY_FIGURE_FORMAT, READER_MANIFEST, HTML_REVIEW):
        if not path.exists():
            errors.append(f"required path missing: {rel(path)}")
    if errors:
        fail(errors)

    record = load_json(RECORD)
    curated = load_json(CURATED_FORMAT)
    key_figures = load_json(KEY_FIGURE_FORMAT)
    reader_manifest = load_json(READER_MANIFEST)
    html_review = HTML_REVIEW.read_text(encoding="utf-8")
    if not isinstance(record, dict):
        fail([f"{rel(RECORD)} must contain a JSON object."])
    if not isinstance(curated, dict):
        fail([f"{rel(CURATED_FORMAT)} must contain a JSON object."])
    if not isinstance(key_figures, dict):
        fail([f"{rel(KEY_FIGURE_FORMAT)} must contain a JSON object."])
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
        "curated_reader_epub": ("epub", "8027d8e9104ef0357424703dbcec50c2e43d22a574eff76a2c0947c47fd8b9fc"),
        "curated_reader_docx": ("docx", "16eb7643a79b41680897491014d71ed0964a25db28703ba4258f498953368ea9"),
        "curated_reader_pdf": ("pdf", "dd2babdcffa867584537761249357492a2151af7eec5b1d385266af7ef0c6342"),
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

    epub_audit = curated.get("epub_content_audit", {})
    docx_audit = curated.get("docx_content_audit", {})
    pdf_raster = curated.get("pdf_visual_raster_audit", {})
    pdf_layout = curated.get("pdf_layout_audit", {})
    if not isinstance(epub_audit, dict):
        errors.append("curated format epub_content_audit must be an object.")
        epub_audit = {}
    if not isinstance(docx_audit, dict):
        errors.append("curated format docx_content_audit must be an object.")
        docx_audit = {}
    if not isinstance(pdf_raster, dict):
        errors.append("curated format pdf_visual_raster_audit must be an object.")
        pdf_raster = {}
    if not isinstance(pdf_layout, dict):
        errors.append("curated format pdf_layout_audit must be an object.")
        pdf_layout = {}

    key_figure_expected = {
        ("epub", "matched_source_svg_titles"): 10,
        ("docx", "matched_figure_stems"): 10,
        ("pdf", "matched_caption_titles"): 10,
    }
    for (section, key), expected in key_figure_expected.items():
        section_obj = key_figures.get(section, {})
        observed = section_obj.get(key) if isinstance(section_obj, dict) else None
        if observed != expected:
            errors.append(f"key-figure format probe {section}.{key} must be {expected}; found {observed}.")

    closure = record.get("format_probe_closure")
    if not isinstance(closure, dict):
        errors.append("format_probe_closure must be present and must be an object.")
        closure = {}
    expected_closure = {
        "status": "automated_probe_passed_release_blocked",
        "curated_format_probe_manifest": "editions/reader_manuscript/v1_0/curated_format_probe_manifest.json",
        "key_figure_format_probe_manifest": "editions/reader_manuscript/v1_0/key_figure_format_probe_manifest.json",
        "epub_repaired_package_sha256": epub_audit.get("source_sha256"),
        "epub_content_xhtml_entries_checked": epub_audit.get("content_xhtml_entries_checked"),
        "epub_unresolved_internal_hrefs": epub_audit.get("unresolved_internal_hrefs"),
        "docx_repaired_package_sha256": docx_audit.get("source_sha256"),
        "docx_raw_qmd_relationship_targets": docx_audit.get("raw_qmd_relationship_targets"),
        "pdf_pages_raster_rendered": pdf_raster.get("pages_rendered"),
        "pdf_blank_raster_pages": pdf_raster.get("blank_pages"),
        "pdf_near_edge_raster_pages": pdf_raster.get("near_edge_content_pages"),
        "key_figure_epub_matched_titles": 10,
        "key_figure_docx_matched_stems": 10,
        "key_figure_pdf_matched_captions": 10,
    }
    for key, expected in expected_closure.items():
        if closure.get(key) != expected:
            errors.append(f"format_probe_closure.{key} must be {expected!r}; found {closure.get(key)!r}.")
    release_boundary = str(closure.get("release_boundary", "")).lower()
    for fragment in ("automated package", "do not approve epub", "final figure art", "curated reader edition"):
        if fragment not in release_boundary:
            errors.append(f"format_probe_closure.release_boundary missing {fragment!r}.")

    epub_note = str(artifacts.get("curated_reader_epub", {}).get("notes", ""))
    for fragment in (
        str(epub_audit.get("source_sha256", "")),
        "49 packaged content XHTML entries checked",
        "0 unresolved internal hrefs",
        "10 matched key-figure SVG titles",
    ):
        if fragment and fragment not in epub_note:
            errors.append(f"curated_reader_epub notes missing repaired-audit fragment: {fragment}")

    docx_note = str(artifacts.get("curated_reader_docx", {}).get("notes", ""))
    for fragment in (
        str(docx_audit.get("source_sha256", "")),
        "17,354 paragraphs",
        "286 relationships",
        "0 raw .qmd relationship targets",
        "10 matched key-figure stems",
    ):
        if fragment and fragment not in docx_note:
            errors.append(f"curated_reader_docx notes missing repaired-audit fragment: {fragment}")

    pdf_note = str(artifacts.get("curated_reader_pdf", {}).get("notes", ""))
    for fragment in (
        f"{pdf_layout.get('word_boxes_checked'):,} word boxes",
        "0 out-of-bounds word boxes",
        "505 rendered pages",
        "0 blank pages",
        "0 near-edge pages",
        "10 matched key-figure captions",
    ):
        if fragment and fragment not in pdf_note:
            errors.append(f"curated_reader_pdf notes missing PDF audit fragment: {fragment}")

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
