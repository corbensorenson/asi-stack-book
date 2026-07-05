#!/usr/bin/env python3
"""Validate the curated-reader DOCX application-evidence decision record."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "editions" / "reader_manuscript" / "v1_0" / "docx_application_decision_manifest.json"
DOC = ROOT / "docs" / "reader_docx_application_decision.md"
FORMAT_PROBE = ROOT / "editions" / "reader_manuscript" / "v1_0" / "curated_format_probe_manifest.json"
DOCX_LAYOUT = ROOT / "editions" / "reader_manuscript" / "v1_0" / "key_figure_docx_layout_manifest.json"
FINAL_FIGURE_REVIEW = (
    ROOT / "editions" / "reader_manuscript" / "v1_0" / "final_figure_artifact_review_manifest.json"
)
TEXT_FALLBACK = ROOT / "editions" / "reader_manuscript" / "v1_0" / "docx_text_fallback_manifest.json"

EXPECTED_STATUS = "accepted_docx_application_evidence_for_release_preparation"
EXPECTED_CLEARED = ["docx_application_review_not_completed"]
EXPECTED_PRESERVED = [
    "reader_release_approval_not_created",
    "manual_keyboard_only_review_not_completed",
    "screen_reader_review_not_completed",
    "wcag_conformance_review_not_completed",
    "reviewed_reader_release_record_not_created_for_audio",
    "narration_quality_review_not_completed",
    "audio_files_not_generated",
    "chapter_markers_not_timecoded",
    "audio_edition_release_record_not_created",
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Reader DOCX application decision validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def require_dict(owner: str, value: Any, errors: list[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        errors.append(f"{owner} must be an object.")
        return {}
    return value


def require_text(owner: str, value: Any, errors: list[str], *, min_words: int = 1) -> str:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{owner} must be a non-empty string.")
        return ""
    if len(value.split()) < min_words:
        errors.append(f"{owner} must contain at least {min_words} words.")
    return value


def validate() -> list[str]:
    errors: list[str] = []
    for path in (MANIFEST, DOC, FORMAT_PROBE, DOCX_LAYOUT, FINAL_FIGURE_REVIEW, TEXT_FALLBACK):
        if not path.exists():
            errors.append(f"required path missing: {rel(path)}")
    if errors:
        return errors

    manifest = require_dict(rel(MANIFEST), load_json(MANIFEST), errors)
    format_probe = require_dict(rel(FORMAT_PROBE), load_json(FORMAT_PROBE), errors)
    docx_layout = require_dict(rel(DOCX_LAYOUT), load_json(DOCX_LAYOUT), errors)
    final_figure = require_dict(rel(FINAL_FIGURE_REVIEW), load_json(FINAL_FIGURE_REVIEW), errors)
    text_fallback = require_dict(rel(TEXT_FALLBACK), load_json(TEXT_FALLBACK), errors)
    doc_text = DOC.read_text(encoding="utf-8")

    if manifest.get("schema_version") != "asi_stack.reader_docx_application_decision.v0":
        errors.append("schema_version must be asi_stack.reader_docx_application_decision.v0.")
    if manifest.get("status") != EXPECTED_STATUS:
        errors.append(f"status must be {EXPECTED_STATUS}.")
    if manifest.get("decision_date") != "2026-07-05":
        errors.append("decision_date must remain 2026-07-05 for this recorded decision.")

    docx_inspection = require_dict("format_probe.inspection_summary.docx", format_probe.get("inspection_summary", {}).get("docx"), errors)
    docx_audit = require_dict("format_probe.docx_content_audit", format_probe.get("docx_content_audit"), errors)
    docx_libreoffice = require_dict(
        "format_probe.docx_libreoffice_review", format_probe.get("docx_libreoffice_review"), errors
    )
    docx_layout_summary = require_dict("docx_layout.summary", docx_layout.get("summary"), errors)
    final_summary = require_dict("final_figure.summary", final_figure.get("summary"), errors)
    fallback_pages = require_dict(
        "text_fallback.pages_application_review", text_fallback.get("pages_application_review"), errors
    )

    expected_top_level = {
        "source_artifact": "build/curated_reader_edition/format_artifacts/docx/_reader_site/The-ASI-Stack.docx",
        "source_docx_sha256": "71ed95b7ded6f85ea94652d7c139cd1f68ed929632822d66d2db0f1b924797b8",
        "repaired_docx_sha256": "12a33e1eb31b5e0147bc18c586b9b73b8d0b4f7bb3936aaf75dc471db78d4a14",
        "docx_content_audit_status": "passed_docx_document_xml_relationship_probe",
        "docx_libreoffice_review_status": "passed_docx_libreoffice_headless_pdf_review",
        "key_figure_docx_layout_status": "passed_local_docx_key_figure_layout_probe",
        "final_figure_review_status": "passed_final_figure_artifact_release_preparation_review",
        "text_fallback_status": "passed_textutil_docx_text_fallback_probe",
        "pages_text_fallback_status": "passed_pages_open_text_fallback_probe",
    }
    for key, expected in expected_top_level.items():
        if manifest.get(key) != expected:
            errors.append(f"{key} must be {expected!r}; found {manifest.get(key)!r}.")

    cross_checks = {
        "source_docx_sha256": docx_inspection.get("sha256"),
        "repaired_docx_sha256": docx_audit.get("source_sha256"),
        "docx_content_audit_status": docx_audit.get("status"),
        "docx_libreoffice_review_status": docx_libreoffice.get("status"),
        "key_figure_docx_layout_status": docx_layout.get("status"),
        "final_figure_review_status": final_figure.get("status"),
        "text_fallback_status": text_fallback.get("status"),
        "pages_text_fallback_status": fallback_pages.get("status"),
    }
    for key, observed in cross_checks.items():
        if manifest.get(key) != observed:
            errors.append(f"{key} must match tracked source evidence; found {manifest.get(key)!r} vs {observed!r}.")

    evidence = require_dict("evidence", manifest.get("evidence"), errors)
    expected_evidence = {
        ("document_xml_relationship_probe", "paragraph_markers"): docx_audit.get("paragraph_markers"),
        ("document_xml_relationship_probe", "relationship_count"): docx_audit.get("relationship_count"),
        ("document_xml_relationship_probe", "raw_qmd_relationship_targets"): 0,
        ("document_xml_relationship_probe", "unresolved_internal_relationship_targets"): 0,
        ("document_xml_relationship_probe", "live_marker_hits"): 0,
        ("document_xml_relationship_probe", "raw_core_claim_marker_hits"): 0,
        ("libreoffice_headless_writer_review", "converted_pdf_pages"): 506,
        ("libreoffice_headless_writer_review", "text_characters_checked"): 1030310,
        ("libreoffice_headless_writer_review", "blank_pages"): 0,
        ("libreoffice_headless_writer_review", "low_ink_pages"): 0,
        ("libreoffice_headless_writer_review", "near_edge_content_pages"): 0,
        ("docx_key_figure_layout_review", "title_pages"): 10,
        ("docx_key_figure_layout_review", "raster_pages_rendered"): 10,
        ("docx_key_figure_layout_review", "minimum_title_margin_pt"): 72.1,
        ("docx_key_figure_layout_review", "maximum_near_edge_ink_percent"): 0.0,
        ("final_figure_artifact_review", "figure_count"): 10,
        ("final_figure_artifact_review", "cleared_blockers"): 1,
        ("pages_text_fallback_probe", "text_characters_checked"): 1107976,
        ("pages_text_fallback_probe", "media_entries"): 0,
        ("pages_text_fallback_probe", "live_marker_hits"): 0,
        ("pages_text_fallback_probe", "raw_core_claim_marker_hits"): 0,
    }
    for (section, key), expected in expected_evidence.items():
        section_obj = require_dict(f"evidence.{section}", evidence.get(section), errors)
        if section_obj.get(key) != expected:
            errors.append(f"evidence.{section}.{key} must be {expected!r}; found {section_obj.get(key)!r}.")

    if evidence.get("libreoffice_headless_writer_review", {}).get("converted_pdf_pages") != docx_libreoffice.get(
        "converted_pdf_pages"
    ):
        errors.append("LibreOffice page count must match the tracked format probe.")
    if evidence.get("docx_key_figure_layout_review", {}).get("title_pages") != docx_layout_summary.get(
        "unique_title_pages"
    ):
        errors.append("DOCX key-figure title-page count must match the tracked layout manifest.")
    if evidence.get("final_figure_artifact_review", {}).get("figure_count") != final_summary.get("figure_count"):
        errors.append("final figure count must match the tracked final-figure review.")

    if manifest.get("cleared_blockers") != EXPECTED_CLEARED:
        errors.append(f"cleared_blockers must be {EXPECTED_CLEARED}.")
    preserved = manifest.get("preserved_blockers", [])
    if preserved != EXPECTED_PRESERVED:
        errors.append(f"preserved_blockers must be {EXPECTED_PRESERVED}.")

    decision = require_text("decision", manifest.get("decision"), errors, min_words=28)
    for fragment in (
        "accepting the available local application-engine evidence",
        "does not claim Word, LibreOffice GUI, or Google Docs approval",
        "does not approve the curated reader DOCX for publication",
    ):
        if fragment not in decision:
            errors.append(f"decision missing required fragment: {fragment!r}.")

    boundary = require_text("release_boundary", manifest.get("release_boundary"), errors, min_words=28)
    for fragment in (
        "clears only `docx_application_review_not_completed`",
        "does not approve DOCX publication",
        "does not create reader release approval",
        "does not promote any claim support state",
    ):
        if fragment not in boundary:
            errors.append(f"release_boundary missing required fragment: {fragment!r}.")

    non_claim_text = " ".join(str(item) for item in manifest.get("non_claims", [])).lower()
    for phrase in (
        "does not claim word approval",
        "does not claim libreoffice gui approval",
        "does not claim google docs approval",
        "does not approve the curated reader docx for publication",
        "does not publish",
        "does not promote any chapter core claim",
    ):
        if phrase not in non_claim_text:
            errors.append(f"non_claims missing boundary phrase: {phrase}")

    for fragment in (
        "Reader DOCX Application Evidence Decision",
        EXPECTED_STATUS,
        "clears only `docx_application_review_not_completed`",
        "506-page PDF",
        "1,030,310 text characters",
        "10 key-figure title pages",
        "Pages-readable text fallback",
        "does not claim Word, LibreOffice GUI, or Google Docs approval",
        "does not approve DOCX publication",
    ):
        if fragment not in doc_text:
            errors.append(f"{rel(DOC)} missing required fragment: {fragment}")
    return errors


def main() -> None:
    errors = validate()
    if errors:
        fail(errors)
    print("Reader DOCX application decision validation passed.")


if __name__ == "__main__":
    main()
