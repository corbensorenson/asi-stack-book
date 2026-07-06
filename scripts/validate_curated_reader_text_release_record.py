#!/usr/bin/env python3
"""Validate the current blocked curated-reader text-edition release record."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "release_records" / "2026-07-06-v1-curated-reader-text-blocked-923108ee.json"
CURATED_FORMAT = ROOT / "editions" / "reader_manuscript" / "v1_0" / "curated_format_probe_manifest.json"
PDF_PAGE_REVIEW = ROOT / "editions" / "reader_manuscript" / "v1_0" / "pdf_page_review_manifest.json"
EPUB_APP_REVIEW = ROOT / "editions" / "reader_manuscript" / "v1_0" / "epub_apple_books_review_manifest.json"
DOCX_APPLICATION_DECISION = (
    ROOT / "editions" / "reader_manuscript" / "v1_0" / "docx_application_decision_manifest.json"
)
KEYBOARD_NAVIGATION = ROOT / "editions" / "reader_manuscript" / "v1_0" / "keyboard_navigation_manifest.json"
ACCESSIBILITY_TREE = ROOT / "editions" / "reader_manuscript" / "v1_0" / "accessibility_tree_manifest.json"
WCAG_PREPARATION = ROOT / "editions" / "reader_manuscript" / "v1_0" / "wcag_preparation_manifest.json"
HUMAN_CONSUMPTION_GATE = (
    ROOT / "editions" / "reader_manuscript" / "v1_0" / "human_consumption_gate_manifest.json"
)

EXPECTED_RELEASE_ID = "2026-07-06-v1-curated-reader-text-blocked-923108ee"
EXPECTED_SOURCE_COMMIT = "923108ee0e15d4f6c755e060efeb0904f47dcad1"
EXPECTED_ARTIFACTS = {
    "curated_reader_html",
    "curated_reader_epub",
    "curated_reader_docx",
    "curated_reader_pdf",
    "ereader_application_review",
    "audio_deferred",
}


def fail(errors: list[str]) -> None:
    print("Curated reader text-edition release record validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def artifact_by_format(record: dict[str, Any]) -> dict[str, dict[str, Any]]:
    artifacts: dict[str, dict[str, Any]] = {}
    for artifact in record.get("artifact_formats", []):
        if isinstance(artifact, dict) and isinstance(artifact.get("format"), str):
            artifacts[artifact["format"]] = artifact
    return artifacts


def require_fragments(owner: str, text: str, fragments: list[object], errors: list[str]) -> None:
    for fragment in fragments:
        variants = [str(fragment)]
        if isinstance(fragment, int):
            variants.append(f"{fragment:,}")
        if not any(variant in text for variant in variants):
            errors.append(f"{owner} missing required fragment: {variants[0]}")


def main() -> None:
    errors: list[str] = []
    for path in (
        RECORD,
        CURATED_FORMAT,
        PDF_PAGE_REVIEW,
        EPUB_APP_REVIEW,
        DOCX_APPLICATION_DECISION,
        KEYBOARD_NAVIGATION,
        ACCESSIBILITY_TREE,
        WCAG_PREPARATION,
        HUMAN_CONSUMPTION_GATE,
    ):
        if not path.exists():
            errors.append(f"required path missing: {rel(path)}")
    if errors:
        fail(errors)

    record = load_json(RECORD)
    curated = load_json(CURATED_FORMAT)
    pdf_page_review = load_json(PDF_PAGE_REVIEW)
    epub_app_review = load_json(EPUB_APP_REVIEW)
    docx_decision = load_json(DOCX_APPLICATION_DECISION)
    keyboard = load_json(KEYBOARD_NAVIGATION)
    accessibility_tree = load_json(ACCESSIBILITY_TREE)
    wcag = load_json(WCAG_PREPARATION)
    human_gate = load_json(HUMAN_CONSUMPTION_GATE)

    if not isinstance(record, dict):
        fail([f"{rel(RECORD)} must contain a JSON object."])

    if record.get("record_type") != "edition_release":
        errors.append("record_type must be edition_release.")
    if record.get("release_id") != EXPECTED_RELEASE_ID:
        errors.append(f"release_id must be {EXPECTED_RELEASE_ID}.")
    if record.get("source_commit") != EXPECTED_SOURCE_COMMIT:
        errors.append(f"source_commit must be {EXPECTED_SOURCE_COMMIT}.")
    if record.get("source_tag") != "not_tagged_curated_reader_text_blocked_candidate_2026-07-06":
        errors.append("source_tag must remain explicit not_tagged text candidate.")
    if record.get("edition_profile") != "reader_release":
        errors.append("edition_profile must be reader_release.")
    if record.get("validation_status") != "partial":
        errors.append("validation_status must be partial for this blocked decision.")

    derivation = str(record.get("derivation_source", "")).lower()
    for fragment in ("text-edition", "audio is explicitly deferred", "not part of this text-edition"):
        if fragment not in derivation:
            errors.append(f"derivation_source missing boundary fragment: {fragment}")

    artifacts = artifact_by_format(record)
    if set(artifacts) != EXPECTED_ARTIFACTS:
        errors.append(f"artifact_formats must be {sorted(EXPECTED_ARTIFACTS)}, found {sorted(artifacts)}.")
    for fmt in EXPECTED_ARTIFACTS - {"audio_deferred"}:
        if artifacts.get(fmt, {}).get("status") not in {"rendered", "reviewed"}:
            errors.append(f"{fmt} must be rendered or reviewed.")
    if artifacts.get("audio_deferred", {}).get("status") != "not_applicable":
        errors.append("audio_deferred must be not_applicable.")

    curated_inspection = curated.get("inspection_summary", {})
    epub_audit = curated.get("epub_content_audit", {})
    epub_browser = curated.get("epub_browser_review", {})
    docx_audit = curated.get("docx_content_audit", {})
    docx_libreoffice = curated.get("docx_libreoffice_review", {})
    pdf_layout = curated.get("pdf_layout_audit", {})
    pdf_raster = curated.get("pdf_visual_raster_audit", {})
    pdf_flow = curated.get("pdf_reading_flow_review", {})
    pdf_viewer = curated.get("pdf_viewer_review", {})
    pdf_page_summary = pdf_page_review.get("summary", {})
    keyboard_summary = keyboard.get("summary", {})
    accessibility_summary = accessibility_tree.get("summary", {})
    wcag_summary = wcag.get("summary", {})

    html_note = str(artifacts.get("curated_reader_html", {}).get("notes", ""))
    require_fragments(
        "curated_reader_html notes",
        html_note,
        [
            curated_inspection.get("html", {}).get("html_files"),
            "98 of 98",
            "2ca82608207741a56a861da7d32f4d8c7e7a25dc390df3836dca11560b19ce34",
            keyboard_summary.get("page_view_pairs"),
            keyboard_summary.get("keyboard_trap_candidates"),
            accessibility_summary.get("accessibility_tree_pairs"),
            accessibility_summary.get("unnamed_interactive_elements"),
            wcag_summary.get("text_contrast_samples"),
            wcag_summary.get("minimum_contrast_ratio"),
            "not screen-reader reviewed",
        ],
        errors,
    )

    epub_note = str(artifacts.get("curated_reader_epub", {}).get("notes", ""))
    require_fragments(
        "curated_reader_epub notes",
        epub_note,
        [
            curated_inspection.get("epub", {}).get("bytes"),
            curated_inspection.get("epub", {}).get("sha256"),
            epub_audit.get("source_sha256"),
            epub_audit.get("xhtml_entries_checked"),
            epub_audit.get("content_xhtml_entries_checked"),
            epub_browser.get("page_view_pairs"),
            epub_browser.get("max_horizontal_overflow_px"),
            epub_app_review.get("source_sha256"),
            "Apple Books",
            "not release-approved",
        ],
        errors,
    )

    docx_note = str(artifacts.get("curated_reader_docx", {}).get("notes", ""))
    require_fragments(
        "curated_reader_docx notes",
        docx_note,
        [
            curated_inspection.get("docx", {}).get("bytes"),
            curated_inspection.get("docx", {}).get("sha256"),
            docx_audit.get("source_sha256"),
            docx_audit.get("paragraph_markers"),
            docx_audit.get("relationship_count"),
            docx_libreoffice.get("converted_pdf_pages"),
            docx_libreoffice.get("text_characters_checked"),
            docx_decision.get("status"),
            "not release-approved",
        ],
        errors,
    )

    pdf_note = str(artifacts.get("curated_reader_pdf", {}).get("notes", ""))
    require_fragments(
        "curated_reader_pdf notes",
        pdf_note,
        [
            curated_inspection.get("pdf", {}).get("bytes"),
            curated_inspection.get("pdf", {}).get("sha256"),
            curated_inspection.get("pdf", {}).get("pages"),
            pdf_layout.get("word_boxes_checked"),
            pdf_layout.get("out_of_bounds_word_boxes"),
            pdf_raster.get("pages_rendered"),
            pdf_raster.get("blank_pages"),
            pdf_raster.get("near_edge_content_pages"),
            pdf_flow.get("text_characters_checked"),
            pdf_flow.get("word_tokens_checked"),
            pdf_flow.get("chapter_headings_checked"),
            pdf_flow.get("appendix_headings_checked"),
            pdf_page_summary.get("page_review_rows"),
            f"{len(pdf_page_summary.get('failed_pages', []))} failed pages",
            pdf_page_summary.get("low_ink_pages", [""])[0],
            pdf_viewer.get("page_down_changed_pixel_percent"),
            "not release-approved",
        ],
        errors,
    )

    ereader_note = str(artifacts.get("ereader_application_review", {}).get("notes", ""))
    require_fragments(
        "ereader_application_review notes",
        ereader_note,
        [epub_app_review.get("source_sha256"), "clears only app_or_ereader_review_not_completed", "not EPUB publication approval"],
        errors,
    )

    audio_note = str(artifacts.get("audio_deferred", {}).get("notes", "")).lower()
    for fragment in ("out of scope", "separate future audio_release", "does not imply that any audio artifact exists"):
        if fragment not in audio_note:
            errors.append(f"audio_deferred notes missing {fragment!r}.")

    review_status = record.get("review_status", {})
    if review_status.get("audio_script_review") != "not_required":
        errors.append("review_status.audio_script_review must be not_required.")
    audiobook_gate = record.get("audiobook_gate", {})
    if audiobook_gate.get("status") != "not_required":
        errors.append("audiobook_gate.status must be not_required.")
    for key in ("script_review", "spoken_treatment_review", "metadata_review", "chapter_marker_review", "audio_spot_check", "embedded_epub_check"):
        if audiobook_gate.get(key) != "not_required":
            errors.append(f"audiobook_gate.{key} must be not_required.")

    human_records = human_gate.get("gates", {})
    human_statuses = {
        "reader_spine_review": "pass",
        "ebook_layout_review": human_records.get("ebook_layout_review", {}).get("status"),
        "diagram_image_review": human_records.get("diagram_image_review", {}).get("status"),
        "bedtime_readability_review": human_records.get("bedtime_readability_review", {}).get("status"),
        "companion_notes_status": human_records.get("companion_notes_status", {}).get("status"),
    }
    for key, expected in human_statuses.items():
        if record.get("human_consumption_gate", {}).get(key) != expected:
            errors.append(f"human_consumption_gate.{key} must be {expected!r}.")

    required_commands = {
        "python3 scripts/validate_curated_reader_text_release_record.py",
        "python3 scripts/sync_reader_format_review_matrix.py --check",
        "python3 scripts/validate_release_surface_status_ledger.py",
    }
    commands = set(record.get("validation_commands", []))
    missing_commands = sorted(required_commands - commands)
    if missing_commands:
        errors.append(f"validation_commands missing required command(s): {missing_commands}")

    residual_text = " ".join(str(item) for item in record.get("residuals", [])).lower()
    non_claim_text = " ".join(str(item) for item in record.get("non_claims", [])).lower()
    for fragment in (
        "reader_release_approval_not_created",
        "screen_reader_review_not_completed",
        "deferred to a separate future audio_release",
    ):
        if fragment not in residual_text:
            errors.append(f"residuals missing {fragment!r}.")
    for fragment in (
        "does not approve",
        "does not publish",
        "does not perform screen-reader review",
        "does not promote",
        "does not prove asi capability",
    ):
        if fragment not in non_claim_text:
            errors.append(f"non_claims missing {fragment!r}.")

    if errors:
        fail(errors)
    print("Curated reader text-edition release record validation passed: partial text decision, audio deferred.")


if __name__ == "__main__":
    main()
