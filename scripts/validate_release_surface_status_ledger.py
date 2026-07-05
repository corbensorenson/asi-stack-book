#!/usr/bin/env python3
"""Generate and validate the v1.0 release-surface status ledger.

The v1.0 candidate status page should stay readable. This ledger carries the
long reader/release artifact state that used to live inside one status-table
cell while preserving release blockers and non-claim boundaries.
"""

from __future__ import annotations

import argparse
from collections import Counter
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "release_surface_status_ledger.md"
STATUS = ROOT / "docs" / "v1_0_candidate_status.md"

RELEASE_PROFILES = ROOT / "editions" / "release_profiles.json"
READER_OVERLAY_MANIFEST = ROOT / "editions" / "reader_overlays" / "v1_0" / "manifest.json"
READER_MANIFEST = ROOT / "editions" / "reader_manuscript" / "v1_0" / "manifest.json"
CHAPTER_REVIEW_MATRIX = ROOT / "editions" / "reader_manuscript" / "v1_0" / "chapter_review_matrix.json"
CHAPTER_RECONCILIATION_APPROVAL = (
    ROOT / "editions" / "reader_manuscript" / "v1_0" / "chapter_reconciliation_approval_manifest.json"
)
FORMAT_REVIEW_MATRIX = ROOT / "editions" / "reader_manuscript" / "v1_0" / "format_review_matrix.json"
ARTIFACT_INSPECTION = ROOT / "editions" / "reader_manuscript" / "v1_0" / "artifact_inspection_manifest.json"
CURATED_FORMAT_PROBE = ROOT / "editions" / "reader_manuscript" / "v1_0" / "curated_format_probe_manifest.json"
EPUB_PROBE = ROOT / "editions" / "reader_manuscript" / "v1_0" / "epub_probe_manifest.json"
DOCX_PROBE = ROOT / "editions" / "reader_manuscript" / "v1_0" / "docx_probe_manifest.json"
PDF_PROBE = ROOT / "editions" / "reader_manuscript" / "v1_0" / "pdf_probe_manifest.json"
AUDIO_PROBE = ROOT / "editions" / "reader_manuscript" / "v1_0" / "audio_script_probe_manifest.json"
AUDIO_NARRATION_TREATMENT_REVIEW = (
    ROOT / "editions" / "reader_manuscript" / "v1_0" / "audio_narration_treatment_review_manifest.json"
)
AUDIO_METADATA_REVIEW = ROOT / "editions" / "reader_manuscript" / "v1_0" / "audio_metadata_review_manifest.json"
HUMAN_CONSUMPTION_GATE = (
    ROOT / "editions" / "reader_manuscript" / "v1_0" / "human_consumption_gate_manifest.json"
)
PDF_PAGE_REVIEW = ROOT / "editions" / "reader_manuscript" / "v1_0" / "pdf_page_review_manifest.json"
FINAL_FIGURE_REVIEW = (
    ROOT / "editions" / "reader_manuscript" / "v1_0" / "final_figure_artifact_review_manifest.json"
)
KEY_FIGURE_FORMAT_PROBE = (
    ROOT / "editions" / "reader_manuscript" / "v1_0" / "key_figure_format_probe_manifest.json"
)
KEY_FIGURE_GEOMETRY = ROOT / "editions" / "reader_manuscript" / "v1_0" / "key_figure_geometry_manifest.json"
VISUAL_IDENTITY = ROOT / "editions" / "reader_manuscript" / "v1_0" / "visual_identity_manifest.json"
ACCESSIBILITY_NAVIGATION = (
    ROOT / "editions" / "reader_manuscript" / "v1_0" / "accessibility_navigation_manifest.json"
)
KEYBOARD_NAVIGATION = ROOT / "editions" / "reader_manuscript" / "v1_0" / "keyboard_navigation_manifest.json"
KEYBOARD_ONLY_DECISION = (
    ROOT / "editions" / "reader_manuscript" / "v1_0" / "keyboard_only_decision_manifest.json"
)
ACCESSIBILITY_TREE = ROOT / "editions" / "reader_manuscript" / "v1_0" / "accessibility_tree_manifest.json"
WCAG_PREPARATION = ROOT / "editions" / "reader_manuscript" / "v1_0" / "wcag_preparation_manifest.json"
KEY_FIGURE_RASTER = ROOT / "editions" / "reader_manuscript" / "v1_0" / "key_figure_raster_manifest.json"
KEY_FIGURE_EPUB_LAYOUT = (
    ROOT / "editions" / "reader_manuscript" / "v1_0" / "key_figure_epub_layout_manifest.json"
)
KEY_FIGURE_PDF_LAYOUT = (
    ROOT / "editions" / "reader_manuscript" / "v1_0" / "key_figure_pdf_layout_manifest.json"
)
KEY_FIGURE_DOCX_LAYOUT = (
    ROOT / "editions" / "reader_manuscript" / "v1_0" / "key_figure_docx_layout_manifest.json"
)
EPUB_APP_REVIEW = ROOT / "editions" / "reader_manuscript" / "v1_0" / "epub_apple_books_review_manifest.json"
DOCX_APPLICATION_DECISION = (
    ROOT / "editions" / "reader_manuscript" / "v1_0" / "docx_application_decision_manifest.json"
)
HTML_RELEASE_RECORD = ROOT / "release_records" / "2026-06-29-v1-reader-html-855dc277.json"
CURATED_BLOCKED_RECORD = ROOT / "release_records" / "2026-07-05-v1-curated-reader-blocked-3e59bde3.json"

REVIEW_DOCS = {
    "reader_html": ROOT / "docs" / "reader_html_artifact_browser_review.md",
    "curated_html": ROOT / "docs" / "curated_reader_html_artifact_browser_review.md",
    "curated_format": ROOT / "docs" / "curated_reader_format_artifact_probe.md",
    "reader_epub": ROOT / "docs" / "reader_epub_probe_manifest.md",
    "reader_docx": ROOT / "docs" / "reader_docx_probe_manifest.md",
    "reader_pdf": ROOT / "docs" / "reader_pdf_probe_manifest.md",
    "reader_audio": ROOT / "docs" / "reader_audio_script_probe_manifest.md",
    "reader_audio_narration_treatment": ROOT / "docs" / "reader_audio_narration_treatment_review.md",
    "reader_audio_metadata": ROOT / "docs" / "reader_audio_metadata_review.md",
    "reader_human_consumption": ROOT / "docs" / "reader_human_consumption_gate_review.md",
    "curated_pdf_page_review": ROOT / "docs" / "curated_reader_pdf_page_review.md",
    "reader_final_figure_artifact_review": ROOT / "docs" / "reader_final_figure_artifact_review.md",
    "reader_chapter_reconciliation": ROOT / "docs" / "reader_chapter_reconciliation_approval.md",
    "reader_figures": ROOT / "docs" / "reader_key_figure_artifact_review.md",
    "reader_figure_format": ROOT / "docs" / "reader_key_figure_format_probe.md",
    "reader_figure_geometry": ROOT / "docs" / "reader_key_figure_geometry_review.md",
    "reader_visual_identity": ROOT / "docs" / "reader_visual_identity_review.md",
    "reader_accessibility_navigation": ROOT / "docs" / "reader_accessibility_navigation_review.md",
    "reader_keyboard_navigation": ROOT / "docs" / "reader_keyboard_navigation_review.md",
    "reader_keyboard_only_decision": ROOT / "docs" / "reader_keyboard_only_decision.md",
    "reader_accessibility_tree": ROOT / "docs" / "reader_accessibility_tree_review.md",
    "reader_wcag_preparation": ROOT / "docs" / "reader_wcag_preparation_review.md",
    "reader_figure_raster": ROOT / "docs" / "reader_key_figure_raster_review.md",
    "reader_figure_epub_layout": ROOT / "docs" / "reader_key_figure_epub_layout_review.md",
    "reader_epub_apple_books": ROOT / "docs" / "reader_epub_apple_books_review.md",
    "reader_docx_application_decision": ROOT / "docs" / "reader_docx_application_decision.md",
    "reader_figure_pdf_layout": ROOT / "docs" / "reader_key_figure_pdf_layout_review.md",
    "reader_figure_docx_layout": ROOT / "docs" / "reader_key_figure_docx_layout_review.md",
    "reader_chapter_matrix": ROOT / "docs" / "reader_chapter_review_matrix.md",
    "reader_format_matrix": ROOT / "docs" / "reader_format_review_matrix.md",
}
AUDIO_NARRATION_TREATMENT_STATUS = "accepted_audio_script_narration_treatment_for_release_preparation"
AUDIO_NARRATION_TREATMENT_CLEARED = ["narration_quality_review_not_completed"]
AUDIO_NARRATION_TREATMENT_PRESERVED = [
    "reviewed_reader_release_record_not_created_for_audio",
    "audio_files_not_generated",
    "audio_spot_check_not_performed",
    "chapter_markers_not_timecoded",
    "audio_metadata_not_reviewed",
    "audio_embedded_epub_not_packaged_or_checked",
    "audio_edition_release_record_not_created",
]
AUDIO_METADATA_STATUS = "accepted_audio_metadata_for_release_preparation"
AUDIO_METADATA_CLEARED = ["audio_metadata_not_reviewed"]
AUDIO_METADATA_PRESERVED = [
    "reviewed_reader_release_record_not_created_for_audio",
    "audio_files_not_generated",
    "audio_spot_check_not_performed",
    "chapter_markers_not_timecoded",
    "audio_embedded_epub_not_packaged_or_checked",
    "audio_edition_release_record_not_created",
]

REQUIRED_PROFILE_IDS = {"live_book", "research_release", "reader_release", "audio_release"}
REQUIRED_CURATED_BLOCKERS = {
    "format_artifact_not_reviewed",
    "reader_release_record_not_created",
}
REQUIRED_FORMAT_BLOCKERS = {
    "full_format_artifact_review_not_completed",
    "app_or_ereader_review_not_completed",
}
REQUIRED_AUDIO_BLOCKERS = {
    "reviewed_reader_release_record_not_created_for_audio",
    "narration_script_not_reviewed",
    "audio_files_not_generated",
    "audio_spot_check_not_performed",
    "chapter_markers_not_timecoded",
    "audio_embedded_epub_not_packaged_or_checked",
    "audio_edition_release_record_not_created",
}


def fail(errors: list[str]) -> None:
    print("Release surface status ledger validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def table_metric(text: str, name: str) -> str | None:
    match = re.search(rf"^\|\s*{re.escape(name)}\s*\|\s*(.*?)\s*\|$", text, re.MULTILINE)
    return match.group(1).strip() if match else None


def int_metric(text: str, name: str) -> int:
    value = table_metric(text, name)
    if value is None:
        return 0
    digits = re.sub(r"[^0-9]", "", value)
    return int(digits) if digits else 0


def qmd_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def counter_phrase(counter: Counter[str]) -> str:
    if not counter:
        return "none"
    return ", ".join(f"{counter[key]} `{key}`" for key in sorted(counter))


def collect_metrics() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    required_paths = [
        RELEASE_PROFILES,
        READER_OVERLAY_MANIFEST,
        READER_MANIFEST,
        CHAPTER_REVIEW_MATRIX,
        CHAPTER_RECONCILIATION_APPROVAL,
        FORMAT_REVIEW_MATRIX,
        ARTIFACT_INSPECTION,
        CURATED_FORMAT_PROBE,
        EPUB_PROBE,
        DOCX_PROBE,
        PDF_PROBE,
        AUDIO_PROBE,
        AUDIO_NARRATION_TREATMENT_REVIEW,
        AUDIO_METADATA_REVIEW,
        HUMAN_CONSUMPTION_GATE,
        PDF_PAGE_REVIEW,
        FINAL_FIGURE_REVIEW,
        KEY_FIGURE_FORMAT_PROBE,
        KEY_FIGURE_GEOMETRY,
        VISUAL_IDENTITY,
        ACCESSIBILITY_NAVIGATION,
        KEYBOARD_NAVIGATION,
        KEYBOARD_ONLY_DECISION,
        ACCESSIBILITY_TREE,
        KEY_FIGURE_RASTER,
        KEY_FIGURE_EPUB_LAYOUT,
        KEY_FIGURE_PDF_LAYOUT,
        KEY_FIGURE_DOCX_LAYOUT,
        EPUB_APP_REVIEW,
        DOCX_APPLICATION_DECISION,
        HTML_RELEASE_RECORD,
        CURATED_BLOCKED_RECORD,
        *REVIEW_DOCS.values(),
    ]
    for path in required_paths:
        if not path.exists():
            errors.append(f"required path is missing: {rel(path)}")
    if errors:
        return {}, errors

    release_profiles = load_json(RELEASE_PROFILES)
    overlay_manifest = load_json(READER_OVERLAY_MANIFEST)
    reader_manifest = load_json(READER_MANIFEST)
    chapter_matrix = load_json(CHAPTER_REVIEW_MATRIX)
    chapter_reconciliation_approval = load_json(CHAPTER_RECONCILIATION_APPROVAL)
    format_matrix = load_json(FORMAT_REVIEW_MATRIX)
    artifact_inspection = load_json(ARTIFACT_INSPECTION)
    curated_format = load_json(CURATED_FORMAT_PROBE)
    epub_probe = load_json(EPUB_PROBE)
    docx_probe = load_json(DOCX_PROBE)
    pdf_probe = load_json(PDF_PROBE)
    audio_probe = load_json(AUDIO_PROBE)
    audio_narration_treatment_review = load_json(AUDIO_NARRATION_TREATMENT_REVIEW)
    audio_metadata_review = load_json(AUDIO_METADATA_REVIEW)
    human_consumption_gate = load_json(HUMAN_CONSUMPTION_GATE)
    pdf_page_review = load_json(PDF_PAGE_REVIEW)
    final_figure_review = load_json(FINAL_FIGURE_REVIEW)
    key_figure_format_probe = load_json(KEY_FIGURE_FORMAT_PROBE)
    key_figure_geometry = load_json(KEY_FIGURE_GEOMETRY)
    visual_identity = load_json(VISUAL_IDENTITY)
    accessibility_navigation = load_json(ACCESSIBILITY_NAVIGATION)
    keyboard_navigation = load_json(KEYBOARD_NAVIGATION)
    keyboard_only_decision = load_json(KEYBOARD_ONLY_DECISION)
    accessibility_tree = load_json(ACCESSIBILITY_TREE)
    wcag_preparation = load_json(WCAG_PREPARATION)
    key_figure_raster = load_json(KEY_FIGURE_RASTER)
    key_figure_epub_layout = load_json(KEY_FIGURE_EPUB_LAYOUT)
    key_figure_pdf_layout = load_json(KEY_FIGURE_PDF_LAYOUT)
    key_figure_docx_layout = load_json(KEY_FIGURE_DOCX_LAYOUT)
    epub_app_review = load_json(EPUB_APP_REVIEW)
    docx_application_decision = load_json(DOCX_APPLICATION_DECISION)
    curated_blocked_record = load_json(CURATED_BLOCKED_RECORD)

    profile_ids = {profile.get("id") for profile in release_profiles.get("profiles", []) if isinstance(profile, dict)}
    missing_profiles = sorted(REQUIRED_PROFILE_IDS - profile_ids)
    if missing_profiles:
        errors.append(f"release profiles missing required profile ids: {missing_profiles}")

    if overlay_manifest.get("status") != "active":
        errors.append("reader overlay manifest status must remain active.")
    if reader_manifest.get("status") != "drafting":
        errors.append("reader manuscript manifest status must remain drafting until release approval exists.")

    chapter_records = reader_manifest.get("chapter_records", [])
    if not isinstance(chapter_records, list):
        errors.append("reader manuscript chapter_records must be a list.")
        chapter_records = []
    reconciliation_counts: Counter[str] = Counter(
        record.get("reconciliation_status", "missing") for record in chapter_records if isinstance(record, dict)
    )
    missing_curated_files = [
        record.get("file", "")
        for record in chapter_records
        if isinstance(record, dict) and record.get("file") and not (ROOT / record["file"]).exists()
    ]
    if missing_curated_files:
        errors.append(f"curated reader chapter files are missing: {missing_curated_files[:5]}")
    unreconciled = [
        record.get("chapter_id", "")
        for record in chapter_records
        if isinstance(record, dict) and record.get("reconciliation_status") != "reconciled"
    ]
    if unreconciled:
        errors.append(f"curated reader records not reconciled: {unreconciled[:5]}")
    missing_curated_blockers = [
        record.get("chapter_id", "")
        for record in chapter_records
        if isinstance(record, dict)
        and not REQUIRED_CURATED_BLOCKERS.issubset(set(record.get("release_blockers", [])))
    ]
    if missing_curated_blockers:
        errors.append(f"curated reader records missing release blockers: {missing_curated_blockers[:5]}")

    handoff = reader_manifest.get("reader_handoff_contract", {})
    if not isinstance(handoff, dict):
        errors.append("reader_handoff_contract must be an object.")
        handoff = {}
    if len(handoff.get("key_figure_targets", [])) != 10:
        errors.append("reader handoff contract must keep ten key-figure targets.")
    if len(handoff.get("signature_ideas", [])) != 10:
        errors.append("reader handoff contract must keep ten signature ideas.")
    if len(handoff.get("part_arcs", [])) != 4:
        errors.append("reader handoff contract must keep four part arcs.")

    if chapter_reconciliation_approval.get("status") != "passed_curated_chapter_reconciliation_approval":
        errors.append(
            "chapter reconciliation approval manifest must remain passed_curated_chapter_reconciliation_approval."
        )
    reconciliation_approval_summary = chapter_reconciliation_approval.get("summary", {})
    if not isinstance(reconciliation_approval_summary, dict):
        errors.append("chapter reconciliation approval summary must be an object.")
        reconciliation_approval_summary = {}
    expected_reconciliation_approval = {
        "chapter_count": 44,
        "reader_manifest_records": 44,
        "chapter_review_matrix_rows": 44,
        "reconciled_records": 44,
        "reviewed_matrix_rows": 44,
        "full_chapter_review_rows": 44,
        "curated_files_present": 44,
        "passed_rows": 44,
        "live_marker_hits": 0,
        "raw_core_claim_marker_hits": 0,
    }
    for key, expected in expected_reconciliation_approval.items():
        observed = reconciliation_approval_summary.get(key)
        if observed != expected:
            errors.append(
                f"chapter reconciliation approval summary.{key} must be {expected!r}; found {observed!r}."
            )
    if chapter_reconciliation_approval.get("cleared_blockers") != ["curated_reconciliation_not_approved"]:
        errors.append("chapter reconciliation approval must clear only curated_reconciliation_not_approved.")
    missing_reconciliation_preserved = sorted(
        (
            REQUIRED_CURATED_BLOCKERS
            | {
                "reader_release_approval_not_created",
                "app_or_ereader_review_not_completed",
                "docx_application_review_not_completed",
                "manual_keyboard_only_review_not_completed",
                "screen_reader_review_not_completed",
                "wcag_conformance_review_not_completed",
                "audio_files_not_generated",
            }
        )
        - set(chapter_reconciliation_approval.get("release_blockers_preserved", []))
    )
    if missing_reconciliation_preserved:
        errors.append(
            "chapter reconciliation approval manifest missing preserved blockers: "
            f"{missing_reconciliation_preserved}"
        )

    chapters = chapter_matrix.get("chapters", [])
    if not isinstance(chapters, list):
        errors.append("chapter review matrix must contain chapters list.")
        chapters = []
    review_counts: Counter[str] = Counter(record.get("review_status", "missing") for record in chapters if isinstance(record, dict))
    disposition_counts: Counter[str] = Counter()
    overlay_operation_count = 0
    for record in chapters:
        if not isinstance(record, dict):
            continue
        overlay_operation_count += int(record.get("overlay_operation_count", 0))
        for disposition in record.get("dispositions", []):
            disposition_counts[disposition] += 1
    matrix_review_counts = chapter_matrix.get("review_status_counts", {})
    if matrix_review_counts.get("reviewed") != review_counts.get("reviewed"):
        errors.append("chapter review matrix reviewed count does not match chapter rows.")
    matrix_disposition_counts = chapter_matrix.get("disposition_counts", {})
    for key in ("reader_overlay_active", "no_immediate_action", "companion_note_candidate", "curated_manuscript_candidate"):
        if matrix_disposition_counts.get(key) != disposition_counts.get(key):
            errors.append(f"chapter review matrix disposition count mismatch for {key}.")

    format_records = format_matrix.get("records", [])
    if not isinstance(format_records, list):
        errors.append("format review matrix must contain records list.")
        format_records = []
    approved_formats = sorted(record.get("format") for record in format_records if record.get("release_approved") is True)
    blocked_formats = sorted(record.get("format") for record in format_records if record.get("release_blockers"))
    blocker_counts: Counter[str] = Counter()
    for record in format_records:
        if isinstance(record, dict):
            blocker_counts.update(record.get("release_blockers", []))
    if approved_formats != ["html"]:
        errors.append(f"only generated reader HTML may be release-approved in this ledger; found {approved_formats}.")
    for blocker in REQUIRED_FORMAT_BLOCKERS:
        if blocker not in blocker_counts:
            errors.append(f"format review matrix missing blocker: {blocker}")
    if "edition release record" not in format_matrix.get("release_rule", ""):
        errors.append("format review matrix release rule must mention edition release record.")
    curated_candidate = format_matrix.get("current_curated_candidate", {})
    if not isinstance(curated_candidate, dict):
        errors.append("format review matrix must carry current_curated_candidate.")
        curated_candidate = {}
    curated_candidate_records = curated_candidate.get("records", [])
    if not isinstance(curated_candidate_records, list):
        errors.append("format review matrix current_curated_candidate.records must be a list.")
        curated_candidate_records = []
    curated_candidate_approved = sorted(
        record.get("format")
        for record in curated_candidate_records
        if isinstance(record, dict) and record.get("release_approved") is True
    )
    if curated_candidate_approved:
        errors.append(f"curated candidate rows must not be release-approved; found {curated_candidate_approved}.")
    curated_candidate_blocker_counts: Counter[str] = Counter()
    for record in curated_candidate_records:
        if isinstance(record, dict):
            curated_candidate_blocker_counts.update(record.get("release_blockers", []))
    if curated_candidate.get("status") != "partial_release_candidate_blocked":
        errors.append("current curated candidate status must remain partial_release_candidate_blocked.")
    if len(curated_candidate_records) != 6:
        errors.append("current curated candidate must track exactly six rows.")
    if curated_candidate.get("release_blocker_counts") != dict(sorted(curated_candidate_blocker_counts.items())):
        errors.append("current curated candidate blocker counts drifted from candidate rows.")

    if curated_blocked_record.get("record_type") != "edition_release":
        errors.append("curated blocked release-candidate record must use record_type edition_release.")
    if curated_blocked_record.get("release_id") != "2026-07-05-v1-curated-reader-blocked-3e59bde3":
        errors.append("curated blocked release-candidate record release_id drifted.")
    if curated_blocked_record.get("validation_status") != "partial":
        errors.append("curated blocked release-candidate record must remain validation_status partial.")
    blocked_non_claim_text = " ".join(str(item) for item in curated_blocked_record.get("non_claims", [])).lower()
    for fragment in ("does not approve", "does not publish", "does not promote"):
        if fragment not in blocked_non_claim_text:
            errors.append(f"curated blocked release-candidate record non_claims missing {fragment!r}.")
    blocked_artifacts = {
        artifact.get("format"): artifact
        for artifact in curated_blocked_record.get("artifact_formats", [])
        if isinstance(artifact, dict)
    }
    required_blocked_formats = {
        "curated_reader_html",
        "curated_reader_epub",
        "curated_reader_docx",
        "curated_reader_pdf",
        "ereader_application_review",
        "audio",
    }
    if set(blocked_artifacts) != required_blocked_formats:
        errors.append(
            "curated blocked release-candidate record must name exactly the current curated HTML/EPUB/DOCX/PDF, e-reader, and audio blockers."
        )
    if any(artifact.get("status") == "published" for artifact in blocked_artifacts.values()):
        errors.append("curated blocked release-candidate artifacts must not be published.")
    blocked_probe_closure = curated_blocked_record.get("format_probe_closure", {})
    if not isinstance(blocked_probe_closure, dict):
        errors.append("curated blocked release-candidate record must carry format_probe_closure.")
        blocked_probe_closure = {}
    if blocked_probe_closure.get("status") != "automated_probe_passed_release_blocked":
        errors.append("curated blocked release-candidate format_probe_closure status must remain automated_probe_passed_release_blocked.")
    release_boundary = str(blocked_probe_closure.get("release_boundary", "")).lower()
    for fragment in (
        "automated package",
        "epub key-figure layout",
        "do not approve epub",
        "final figure-artifact review",
        "clears the current final-figure blocker",
        "docx application-evidence decision",
        "docx_application_review_not_completed",
        "keyboard-only evidence decision",
        "manual_keyboard_only_review_not_completed",
        "accessibility-tree release-preparation probe",
        "audio narration treatment review",
        "narration_quality_review_not_completed",
        "audio metadata review",
        "audio_metadata_not_reviewed",
        "audio file generation",
        "chapter timecoding",
        "audio publication-rights approval",
        "curated reader edition",
    ):
        if fragment not in release_boundary:
            errors.append(f"curated blocked release-candidate format_probe_closure boundary missing {fragment!r}.")
    if docx_application_decision.get("status") != "accepted_docx_application_evidence_for_release_preparation":
        errors.append("DOCX application decision status must remain accepted_docx_application_evidence_for_release_preparation.")
    if docx_application_decision.get("cleared_blockers") != ["docx_application_review_not_completed"]:
        errors.append("DOCX application decision must clear only docx_application_review_not_completed.")
    required_docx_decision_preserved = {
        "reader_release_approval_not_created",
        "manual_keyboard_only_review_not_completed",
        "screen_reader_review_not_completed",
        "wcag_conformance_review_not_completed",
        "audio_files_not_generated",
    }
    missing_docx_decision_preserved = sorted(
        required_docx_decision_preserved - set(docx_application_decision.get("preserved_blockers", []))
    )
    if missing_docx_decision_preserved:
        errors.append(f"DOCX application decision missing preserved blockers: {missing_docx_decision_preserved}")

    curated_inspection = curated_format.get("inspection_summary", {})
    curated_epub_content_audit = curated_format.get("epub_content_audit", {})
    curated_epub_browser_review = curated_format.get("epub_browser_review", {})
    curated_docx_content_audit = curated_format.get("docx_content_audit", {})
    curated_docx_libreoffice_review = curated_format.get("docx_libreoffice_review", {})
    curated_pdf_visual_raster_audit = curated_format.get("pdf_visual_raster_audit", {})
    curated_pdf_reading_flow_review = curated_format.get("pdf_reading_flow_review", {})
    curated_pdf_viewer_review = curated_format.get("pdf_viewer_review", {})
    reader_inspection = artifact_inspection.get("inspection_summary", {})
    epub_summary = epub_probe.get("epub_container_summary", {})
    docx_conversion = docx_probe.get("conversion_summary", {})
    pdf_info = pdf_probe.get("pdfinfo_summary", {})
    audio_workspace = audio_probe.get("script_workspace_summary", {})
    audio_targets = audio_probe.get("target_artifact_status", {})
    audio_key_figures = audio_probe.get("key_figure_companion_note", {})
    audio_reading_flow = audio_probe.get("audio_script_reading_flow_review", {})
    human_gate_records = human_consumption_gate.get("gates", {})
    if epub_app_review.get("status") != "passed_apple_books_epub_application_review":
        errors.append("EPUB Apple Books review manifest must remain passed_apple_books_epub_application_review.")
    if epub_app_review.get("source_sha256") != curated_epub_content_audit.get("source_sha256"):
        errors.append("EPUB Apple Books review source_sha256 must match the repaired EPUB content audit.")
    if epub_app_review.get("cleared_blockers") != ["app_or_ereader_review_not_completed"]:
        errors.append("EPUB Apple Books review must clear only app_or_ereader_review_not_completed.")
    if len(epub_app_review.get("observations", [])) != 4:
        errors.append("EPUB Apple Books review must preserve four application observations.")
    if human_consumption_gate.get("status") != "passed_human_consumption_pre_release_gate":
        errors.append("human-consumption gate manifest must remain passed_human_consumption_pre_release_gate.")
    if not isinstance(human_gate_records, dict):
        errors.append("human-consumption gate manifest gates must be an object.")
        human_gate_records = {}
    human_gate_statuses: dict[str, str] = {}
    for gate_name in (
        "ebook_layout_review",
        "diagram_image_review",
        "bedtime_readability_review",
        "companion_notes_status",
    ):
        gate = human_gate_records.get(gate_name, {})
        if not isinstance(gate, dict):
            errors.append(f"human-consumption gate {gate_name} must be an object.")
            continue
        status = gate.get("status")
        human_gate_statuses[gate_name] = str(status)
        if status != "pass_pre_release_review":
            errors.append(f"human-consumption gate {gate_name} must remain pass_pre_release_review.")
    human_gate_required_blockers = REQUIRED_CURATED_BLOCKERS | {
        "app_or_ereader_review_not_completed",
        "manual_keyboard_only_review_not_completed",
        "screen_reader_review_not_completed",
        "wcag_conformance_review_not_completed",
        "narration_quality_review_not_completed",
        "audio_files_not_generated",
    }
    missing_human_gate_blockers = sorted(
        human_gate_required_blockers - set(human_consumption_gate.get("release_blockers_preserved", []))
    )
    if missing_human_gate_blockers:
        errors.append(f"human-consumption gate manifest missing blockers: {missing_human_gate_blockers}")
    if pdf_page_review.get("status") != "passed_pdf_page_by_page_release_preparation_review":
        errors.append("PDF page-review manifest must remain passed_pdf_page_by_page_release_preparation_review.")
    pdf_page_summary = pdf_page_review.get("summary", {})
    if not isinstance(pdf_page_summary, dict):
        errors.append("PDF page-review manifest summary must be an object.")
        pdf_page_summary = {}
    expected_pdf_page_review = {
        "pdf_pages": 511,
        "page_review_rows": 511,
        "text_pages_checked": 511,
        "bbox_pages_checked": 511,
        "raster_pages_checked": 511,
        "pages_with_text": 511,
        "pages_with_word_boxes": 511,
        "pages_with_raster_content": 511,
        "failed_pages": [],
        "blank_pages": [],
        "near_edge_pages": [],
        "out_of_bounds_word_box_pages": [],
        "low_ink_pages": [24],
    }
    for key, expected in expected_pdf_page_review.items():
        observed = pdf_page_summary.get(key)
        if observed != expected:
            errors.append(f"PDF page-review summary.{key} must be {expected!r}; found {observed!r}.")
    if pdf_page_review.get("cleared_blockers") != ["manual_pdf_page_by_page_review_not_completed"]:
        errors.append("PDF page-review manifest must clear only manual_pdf_page_by_page_review_not_completed.")
    missing_pdf_page_preserved = sorted(
        {
            "final_figure_artifact_review_not_completed",
            "reader_release_approval_not_created",
        }
        - set(pdf_page_review.get("release_blockers_preserved", []))
    )
    if missing_pdf_page_preserved:
        errors.append(f"PDF page-review manifest missing preserved blockers: {missing_pdf_page_preserved}")
    if final_figure_review.get("status") != "passed_final_figure_artifact_release_preparation_review":
        errors.append("final figure-artifact review manifest must remain passed_final_figure_artifact_release_preparation_review.")
    final_figure_summary = final_figure_review.get("summary", {})
    if not isinstance(final_figure_summary, dict):
        errors.append("final figure-artifact review summary must be an object.")
        final_figure_summary = {}
    expected_final_figure_summary = {
        "figure_count": 10,
        "source_geometry_status": "passed_source_geometry_review",
        "source_visual_identity_status": "passed_source_level_visual_identity_review",
        "source_accessibility_status": "passed_source_accessibility_navigation_review",
        "contrast_all_figures_passed": True,
        "geometry_content_bounds_passed": 10,
        "geometry_text_anchor_bounds_passed": 10,
        "accessibility_alt_texts": 10,
        "accessibility_figure_boundaries": 10,
        "raster_artifacts": 10,
        "raster_standard_dimensions": 10,
        "epub_layout_page_view_pairs": 20,
        "epub_layout_failed_pairs": 0,
        "epub_layout_image_failures": 0,
        "pdf_layout_caption_pages": 10,
        "pdf_layout_raster_pages": 10,
        "docx_layout_title_pages": 10,
        "docx_layout_raster_pages": 10,
    }
    for key, expected in expected_final_figure_summary.items():
        observed = final_figure_summary.get(key)
        if observed != expected:
            errors.append(f"final figure-artifact review summary.{key} must be {expected!r}; found {observed!r}.")
    if final_figure_review.get("cleared_blockers") != ["final_figure_artifact_review_not_completed"]:
        errors.append("final figure-artifact review must clear only final_figure_artifact_review_not_completed.")
    missing_final_figure_preserved = sorted(
        {
            "reader_release_approval_not_created",
            "app_or_ereader_review_not_completed",
            "docx_application_review_not_completed",
            "manual_keyboard_only_review_not_completed",
            "screen_reader_review_not_completed",
            "wcag_conformance_review_not_completed",
            "audio_files_not_generated",
        }
        - set(final_figure_review.get("release_blockers_preserved", []))
    )
    if missing_final_figure_preserved:
        errors.append(f"final figure-artifact review manifest missing preserved blockers: {missing_final_figure_preserved}")
    if set(audio_targets.values()) != {"target_not_generated"}:
        errors.append("audio target artifacts must remain target_not_generated until audio release artifacts exist.")
    missing_audio_blockers = sorted(REQUIRED_AUDIO_BLOCKERS - set(audio_probe.get("release_blockers_preserved", [])))
    if missing_audio_blockers:
        errors.append(f"audio probe missing blockers: {missing_audio_blockers}")
    if audio_key_figures.get("figure_count") != 10:
        errors.append("audio probe key_figure_companion_note.figure_count must remain 10.")
    if audio_key_figures.get("has_audio_treatment") is not True:
        errors.append("audio probe key_figure_companion_note.has_audio_treatment must remain true.")
    if audio_key_figures.get("has_e_reader_treatment") is not True:
        errors.append("audio probe key_figure_companion_note.has_e_reader_treatment must remain true.")
    expected_audio_reading_flow = {
        "status": "passed_audio_script_reading_flow_review",
        "script_files_checked": 49,
        "chapter_marker_rows": 49,
        "chapter_marker_tbd_rows": 49,
        "narration_note_count": 66,
        "text_characters_checked": 1089681,
        "target_artifact_status": {
            "mp3": "target_not_generated",
            "m4b": "target_not_generated",
            "audio-embedded-epub": "target_not_generated",
        },
    }
    for key, expected in expected_audio_reading_flow.items():
        if audio_reading_flow.get(key) != expected:
            errors.append(f"audio_script_reading_flow_review.{key} must be {expected!r}.")
    expected_audio_narration_treatment = {
        "status": AUDIO_NARRATION_TREATMENT_STATUS,
        "source_audio_probe_manifest": "editions/reader_manuscript/v1_0/audio_script_probe_manifest.json",
        "reading_flow_status": audio_reading_flow.get("status"),
        "combined_script_sha256": audio_reading_flow.get("combined_script_sha256"),
        "script_files_checked": audio_reading_flow.get("script_files_checked"),
        "chapter_scripts_checked": audio_reading_flow.get("chapter_scripts_checked"),
        "appendix_scripts_checked": audio_reading_flow.get("appendix_scripts_checked"),
        "chapter_marker_rows": audio_reading_flow.get("chapter_marker_rows"),
        "chapter_marker_tbd_rows": audio_reading_flow.get("chapter_marker_tbd_rows"),
        "narration_note_count": audio_reading_flow.get("narration_note_count"),
        "text_characters_checked": audio_reading_flow.get("text_characters_checked"),
        "word_tokens_checked": audio_reading_flow.get("word_tokens_checked"),
        "live_marker_hits": audio_reading_flow.get("live_marker_hits"),
        "raw_core_claim_marker_hits": audio_reading_flow.get("raw_core_claim_marker_hits"),
        "replacement_character_count": audio_reading_flow.get("replacement_character_count"),
        "target_artifact_status": {
            "mp3": "target_not_generated",
            "m4b": "target_not_generated",
            "audio-embedded-epub": "target_not_generated",
        },
        "key_figure_spoken_summaries": 10,
    }
    for key, expected in expected_audio_narration_treatment.items():
        if audio_narration_treatment_review.get(key) != expected:
            errors.append(f"audio_narration_treatment_review.{key} must be {expected!r}.")
    if audio_narration_treatment_review.get("cleared_blockers") != AUDIO_NARRATION_TREATMENT_CLEARED:
        errors.append("audio narration treatment review must clear only narration_quality_review_not_completed.")
    if audio_narration_treatment_review.get("preserved_blockers") != AUDIO_NARRATION_TREATMENT_PRESERVED:
        errors.append("audio narration treatment review preserved blockers drifted.")
    if blocked_probe_closure.get("audio_narration_treatment_review_status") != AUDIO_NARRATION_TREATMENT_STATUS:
        errors.append("blocked release closure must record the audio narration treatment review status.")
    if blocked_probe_closure.get("audio_narration_treatment_cleared_blockers") != 1:
        errors.append("blocked release closure must record one cleared audio narration blocker.")
    if blocked_probe_closure.get("audio_narration_treatment_preserved_blockers") != 7:
        errors.append("blocked release closure must record seven preserved audio blockers.")
    expected_audio_metadata = {
        "schema_version": "asi_stack.reader_audio_metadata_review.v0",
        "status": AUDIO_METADATA_STATUS,
        "decision_date": "2026-07-05",
        "source_audio_probe_manifest": "editions/reader_manuscript/v1_0/audio_script_probe_manifest.json",
        "source_release_profiles": "editions/release_profiles.json",
        "source_blocked_release_record": "release_records/2026-07-05-v1-curated-reader-blocked-3e59bde3.json",
        "source_candidate_release_id": curated_blocked_record.get("release_id"),
        "source_candidate_commit": curated_blocked_record.get("source_commit"),
        "source_candidate_tag": curated_blocked_record.get("source_tag"),
        "source_audio_script_sha256": audio_reading_flow.get("combined_script_sha256"),
        "script_files_checked": audio_reading_flow.get("script_files_checked"),
        "chapter_scripts_checked": audio_reading_flow.get("chapter_scripts_checked"),
        "chapter_marker_rows": audio_reading_flow.get("chapter_marker_rows"),
        "audio_profile": "audio_release",
    }
    for key, expected in expected_audio_metadata.items():
        if audio_metadata_review.get(key) != expected:
            errors.append(f"audio_metadata_review.{key} must be {expected!r}.")
    expected_audio_metadata_fields = {
        "title": "The ASI Stack",
        "subtitle": "A Systems Architecture for Governed, Efficient, Self-Improving AI",
        "author": "Corben Sorenson",
        "major_version": "v1.0",
        "language": "en-US",
        "source_commit": curated_blocked_record.get("source_commit"),
        "source_tag": curated_blocked_record.get("source_tag"),
        "script_digest": audio_reading_flow.get("combined_script_sha256"),
    }
    metadata_fields = audio_metadata_review.get("metadata_fields", {})
    if not isinstance(metadata_fields, dict):
        errors.append("audio_metadata_review.metadata_fields must be an object.")
        metadata_fields = {}
    for key, expected in expected_audio_metadata_fields.items():
        if metadata_fields.get(key) != expected:
            errors.append(f"audio_metadata_review.metadata_fields.{key} must be {expected!r}.")
    metadata_boundary_text = " ".join(
        [
            str(metadata_fields.get("narrator_or_tooling_note", "")),
            str(metadata_fields.get("rights_statement", "")),
            str(audio_metadata_review.get("decision", "")),
            str(audio_metadata_review.get("release_boundary", "")),
            " ".join(str(item) for item in audio_metadata_review.get("non_claims", [])),
        ]
    ).lower()
    for fragment in (
        "no narrator",
        "no audio publication",
        "does not create mp3",
        "does not timecode chapter markers",
        "does not approve audio publication rights",
        "does not approve an audiobook",
    ):
        if fragment not in metadata_boundary_text:
            errors.append(f"audio metadata review boundary missing {fragment!r}.")
    if audio_metadata_review.get("cleared_blockers") != AUDIO_METADATA_CLEARED:
        errors.append("audio metadata review must clear only audio_metadata_not_reviewed.")
    if audio_metadata_review.get("preserved_blockers") != AUDIO_METADATA_PRESERVED:
        errors.append("audio metadata review preserved blockers drifted.")
    if blocked_probe_closure.get("audio_metadata_review_status") != AUDIO_METADATA_STATUS:
        errors.append("blocked release closure must record the audio metadata review status.")
    if blocked_probe_closure.get("audio_metadata_review_cleared_blockers") != 1:
        errors.append("blocked release closure must record one cleared audio metadata blocker.")
    if blocked_probe_closure.get("audio_metadata_review_preserved_blockers") != 6:
        errors.append("blocked release closure must record six preserved audio blockers after metadata review.")

    if key_figure_format_probe.get("status") != "passed_local_format_package_probe":
        errors.append("key-figure format probe must remain passed_local_format_package_probe.")
    expected_key_figure_metrics = {
        ("epub", "svg_entries"): 10,
        ("epub", "matched_source_svg_titles"): 10,
        ("epub", "figure_boundary_paragraphs"): 10,
        ("docx", "matched_figure_stems"): 10,
        ("docx", "figure_boundary_paragraphs"): 10,
        ("pdf", "matched_caption_titles"): 10,
        ("pdf", "figure_boundary_paragraphs"): 10,
    }
    for (section, key), expected in expected_key_figure_metrics.items():
        observed = key_figure_format_probe.get(section, {}).get(key)
        if observed != expected:
            errors.append(f"key-figure format probe {section}.{key} must be {expected}; found {observed}.")
    required_key_figure_blockers = {
        "final_figure_artifact_review_not_completed",
        "epub_e_reader_review_not_completed",
        "docx_application_review_not_completed",
        "pdf_page_layout_review_not_completed",
        "reader_edition_release_record_not_created",
    }
    missing_key_figure_blockers = sorted(
        required_key_figure_blockers - set(key_figure_format_probe.get("release_blockers_preserved", []))
    )
    if missing_key_figure_blockers:
        errors.append(f"key-figure format probe missing blockers: {missing_key_figure_blockers}")

    if key_figure_geometry.get("status") != "passed_source_geometry_review":
        errors.append("key-figure geometry manifest must remain passed_source_geometry_review.")
    geometry_summary = key_figure_geometry.get("summary", {})
    expected_geometry_metrics = {
        "figure_count": 10,
        "standard_viewbox_count": 10,
        "content_bounds_passed_count": 10,
        "text_anchor_bounds_passed_count": 10,
        "minimum_visible_text_nodes": 25,
        "minimum_visible_rects": 8,
        "minimum_visible_connector_paths": 8,
        "minimum_content_edge_margin_px": 22.0,
        "maximum_text_anchor_x": 1064.0,
        "maximum_text_anchor_y": 738.0,
    }
    for key, expected in expected_geometry_metrics.items():
        observed = geometry_summary.get(key)
        if observed != expected:
            errors.append(f"key-figure geometry summary.{key} must be {expected!r}; found {observed!r}.")
    geometry_boundary = str(key_figure_geometry.get("review_boundary", ""))
    for fragment in (
        "not raster review",
        "not manual aesthetic review",
        "not e-reader visual review",
        "not DOCX/PDF application review",
        "not final figure-artifact approval",
        "not reader release approval",
    ):
        if fragment not in geometry_boundary:
            errors.append(f"key-figure geometry review_boundary missing {fragment!r}.")

    if visual_identity.get("status") != "passed_source_level_visual_identity_review":
        errors.append("reader visual identity manifest must remain passed_source_level_visual_identity_review.")
    visual_palette = visual_identity.get("palette_summary", {})
    visual_figures = visual_identity.get("figure_source_summary", {})
    visual_contrast = visual_identity.get("contrast_summary", {})
    expected_visual_metrics = {
        ("palette_summary", "combined_hex_color_count"): 67,
        ("palette_summary", "non_neutral_family_count"): 5,
        ("figure_source_summary", "figure_count"): 10,
        ("figure_source_summary", "standard_viewbox_count"): 10,
        ("figure_source_summary", "role_img_count"): 10,
        ("figure_source_summary", "title_id_count"): 10,
        ("figure_source_summary", "desc_id_count"): 10,
        ("contrast_summary", "minimum_text_contrast_ratio"): 5.19,
        ("contrast_summary", "minimum_flow_line_contrast_ratio"): 3.96,
        ("contrast_summary", "minimum_marker_contrast_ratio"): 3.96,
    }
    visual_sections = {
        "palette_summary": visual_palette,
        "figure_source_summary": visual_figures,
        "contrast_summary": visual_contrast,
    }
    for (section, key), expected in expected_visual_metrics.items():
        observed = visual_sections.get(section, {}).get(key)
        if observed != expected:
            errors.append(f"reader visual identity manifest {section}.{key} must be {expected!r}; found {observed!r}.")
    visual_boundary = str(visual_identity.get("review_boundary", ""))
    for fragment in (
        "not manual aesthetic review",
        "not e-reader visual review",
        "not DOCX/PDF application review",
        "not final figure-artifact approval",
        "not reader release approval",
    ):
        if fragment not in visual_boundary:
            errors.append(f"reader visual identity review_boundary missing {fragment!r}.")
    visual_non_claims = " ".join(str(item) for item in visual_identity.get("non_claims", [])).lower()
    for fragment in ("does not approve final figure art", "does not approve epub", "does not prove visual quality"):
        if fragment not in visual_non_claims:
            errors.append(f"reader visual identity non_claims missing {fragment!r}.")

    if accessibility_navigation.get("status") != "passed_source_accessibility_navigation_review":
        errors.append(
            "reader accessibility/navigation manifest must remain passed_source_accessibility_navigation_review."
        )
    access_summary = accessibility_navigation.get("summary", {})
    expected_accessibility_metrics = {
        "chapter_records": 44,
        "existing_chapter_files": 44,
        "reconciled_records": 44,
        "release_blocker_preserved_records": 44,
        "chapters_with_one_h1": 44,
        "skipped_heading_count": 0,
        "duplicate_heading_slug_count": 0,
        "handoff_sections": 44,
        "image_count": 10,
        "fig_alt_count": 10,
        "figure_boundary_count": 10,
        "live_marker_leak_count": 0,
        "raw_core_claim_marker_leak_count": 0,
        "key_figure_targets": 10,
        "key_figure_assets_present": 10,
        "key_figure_reader_refs_present": 10,
        "key_figure_fig_alts_present": 10,
        "key_figure_boundaries_present": 10,
    }
    for key, expected in expected_accessibility_metrics.items():
        observed = access_summary.get(key)
        if observed != expected:
            errors.append(
                f"reader accessibility/navigation manifest summary.{key} must be {expected!r}; found {observed!r}."
            )
    access_boundary = str(accessibility_navigation.get("review_boundary", ""))
    for fragment in (
        "not rendered browser review",
        "not keyboard-only review",
        "not screen-reader review",
        "not WCAG conformance",
        "not e-reader review",
        "not audiobook review",
        "not reader release approval",
    ):
        if fragment not in access_boundary:
            errors.append(f"reader accessibility/navigation review_boundary missing {fragment!r}.")
    access_non_claims = " ".join(str(item) for item in accessibility_navigation.get("non_claims", [])).lower()
    for fragment in ("does not certify wcag", "does not approve epub", "does not promote any chapter core claim"):
        if fragment not in access_non_claims:
            errors.append(f"reader accessibility/navigation non_claims missing {fragment!r}.")

    if keyboard_navigation.get("status") != "passed_automated_keyboard_traversal_review":
        errors.append("reader keyboard navigation manifest must remain passed_automated_keyboard_traversal_review.")
    keyboard_summary = keyboard_navigation.get("summary", {})
    if not isinstance(keyboard_summary, dict):
        errors.append("reader keyboard navigation summary must be an object.")
        keyboard_summary = {}
    expected_keyboard_metrics = {
        "pages_checked": 49,
        "expected_pages": 49,
        "viewport_count": 2,
        "page_view_pairs": 98,
        "chapter_page_view_pairs": 88,
        "tab_steps_per_page_view": 80,
        "failed_page_view_pairs": 0,
        "skip_link_reached_pairs": 98,
        "skip_link_activated_pairs": 98,
        "main_content_route_available_pairs": 98,
        "navigation_focus_reached_pairs": 98,
        "search_focus_reached_pairs": 98,
        "keyboard_trap_candidates": 0,
    }
    for key, expected in expected_keyboard_metrics.items():
        observed = keyboard_summary.get(key)
        if observed != expected:
            errors.append(f"reader keyboard navigation summary.{key} must be {expected!r}; found {observed!r}.")
    for key, minimum in {
        "minimum_focusable_elements": 5,
        "minimum_unique_focus_targets": 5,
    }.items():
        observed = keyboard_summary.get(key)
        if not isinstance(observed, (int, float)) or observed < minimum:
            errors.append(f"reader keyboard navigation summary.{key} must be at least {minimum}; found {observed!r}.")
    keyboard_boundary = str(keyboard_navigation.get("review_boundary", ""))
    for fragment in (
        "not manual keyboard-only review",
        "not screen-reader review",
        "not WCAG conformance",
        "not e-reader review",
        "not audiobook review",
        "not reader release approval",
    ):
        if fragment not in keyboard_boundary:
            errors.append(f"reader keyboard navigation review_boundary missing {fragment!r}.")
    keyboard_non_claims = " ".join(str(item) for item in keyboard_navigation.get("non_claims", [])).lower()
    for fragment in ("does not certify wcag", "does not perform screen-reader review", "does not approve epub"):
        if fragment not in keyboard_non_claims:
            errors.append(f"reader keyboard navigation non_claims missing {fragment!r}.")

    expected_keyboard_only_decision = {
        "status": "accepted_keyboard_only_evidence_for_release_preparation",
        "html_review_digest": "2ca82608207741a56a861da7d32f4d8c7e7a25dc390df3836dca11560b19ce34",
        "keyboard_navigation_status": keyboard_navigation.get("status"),
        "keyboard_page_view_pairs": keyboard_summary.get("page_view_pairs"),
        "keyboard_failed_pairs": keyboard_summary.get("failed_page_view_pairs"),
        "keyboard_skip_link_activated_pairs": keyboard_summary.get("skip_link_activated_pairs"),
        "keyboard_main_route_pairs": keyboard_summary.get("main_content_route_available_pairs"),
        "keyboard_navigation_pairs": keyboard_summary.get("navigation_focus_reached_pairs"),
        "keyboard_search_pairs": keyboard_summary.get("search_focus_reached_pairs"),
        "keyboard_trap_candidates": keyboard_summary.get("keyboard_trap_candidates"),
        "accessibility_tree_status": "passed_accessibility_tree_release_preparation_probe",
        "cleared_blockers": ["manual_keyboard_only_review_not_completed"],
    }
    for key, expected in expected_keyboard_only_decision.items():
        observed = keyboard_only_decision.get(key)
        if observed != expected:
            errors.append(f"reader keyboard-only decision {key} must be {expected!r}; found {observed!r}.")
    for fragment in (
        "screen_reader_review_not_completed",
        "wcag_conformance_review_not_completed",
        "reader_release_approval_not_created",
    ):
        if fragment not in keyboard_only_decision.get("preserved_blockers", []):
            errors.append(f"reader keyboard-only decision preserved_blockers missing {fragment!r}.")
    keyboard_only_boundary = str(keyboard_only_decision.get("release_boundary", ""))
    for fragment in (
        "clears only `manual_keyboard_only_review_not_completed`",
        "does not perform screen-reader review",
        "does not certify WCAG conformance",
        "does not approve reader release",
    ):
        if fragment not in keyboard_only_boundary:
            errors.append(f"reader keyboard-only decision release_boundary missing {fragment!r}.")

    if accessibility_tree.get("status") != "passed_accessibility_tree_release_preparation_probe":
        errors.append("reader accessibility-tree manifest must remain passed_accessibility_tree_release_preparation_probe.")
    accessibility_tree_summary = accessibility_tree.get("summary", {})
    if not isinstance(accessibility_tree_summary, dict):
        errors.append("reader accessibility-tree summary must be an object.")
        accessibility_tree_summary = {}
    expected_accessibility_tree_metrics = {
        "pages_checked": 49,
        "expected_pages": 49,
        "viewport_count": 2,
        "page_view_pairs": 98,
        "chapter_page_view_pairs": 88,
        "failed_page_view_pairs": 0,
        "lang_en_us_pairs": 98,
        "titled_pairs": 98,
        "one_h1_pairs": 98,
        "main_landmark_pairs": 98,
        "navigation_landmark_pairs": 98,
        "skip_link_pairs": 98,
        "focus_visible_rule_pairs": 98,
        "accessibility_tree_pairs": 98,
        "unnamed_interactive_elements": 0,
        "image_alt_failures": 0,
        "table_header_failures": 0,
        "duplicate_id_page_views": 0,
        "live_marker_leak_pairs": 0,
        "raw_core_claim_marker_leak_pairs": 0,
    }
    for key, expected in expected_accessibility_tree_metrics.items():
        observed = accessibility_tree_summary.get(key)
        if observed != expected:
            errors.append(f"reader accessibility-tree summary.{key} must be {expected!r}; found {observed!r}.")
    for key, minimum in {
        "minimum_accessibility_tree_nodes": 20,
        "minimum_named_accessibility_nodes": 10,
        "visible_interactive_elements": 1,
    }.items():
        observed = accessibility_tree_summary.get(key)
        if not isinstance(observed, (int, float)) or observed < minimum:
            errors.append(f"reader accessibility-tree summary.{key} must be at least {minimum}; found {observed!r}.")
    accessibility_tree_boundary = str(accessibility_tree.get("review_boundary", ""))
    for fragment in (
        "not manual keyboard-only review",
        "not screen-reader review",
        "not WCAG conformance",
        "not e-reader review",
        "not audiobook review",
        "not reader release approval",
    ):
        if fragment not in accessibility_tree_boundary:
            errors.append(f"reader accessibility-tree review_boundary missing {fragment!r}.")
    accessibility_tree_non_claims = " ".join(str(item) for item in accessibility_tree.get("non_claims", [])).lower()
    for fragment in ("does not certify wcag", "does not perform screen-reader review", "does not approve epub"):
        if fragment not in accessibility_tree_non_claims:
            errors.append(f"reader accessibility-tree non_claims missing {fragment!r}.")

    if wcag_preparation.get("status") != "accepted_wcag_automation_evidence_for_release_preparation":
        errors.append("reader WCAG-preparation manifest must remain accepted_wcag_automation_evidence_for_release_preparation.")
    if wcag_preparation.get("cleared_blockers") != ["wcag_conformance_review_not_completed"]:
        errors.append("reader WCAG-preparation manifest must clear only wcag_conformance_review_not_completed.")
    wcag_summary = wcag_preparation.get("summary", {})
    if not isinstance(wcag_summary, dict):
        errors.append("reader WCAG-preparation summary must be an object.")
        wcag_summary = {}
    expected_wcag_metrics = {
        "pages_checked": 49,
        "page_view_pairs": 98,
        "failed_page_view_pairs": 0,
        "focus_visible_rule_pairs": 98,
        "unnamed_interactive_elements": 0,
        "image_alt_failures": 0,
        "table_header_failures": 0,
        "duplicate_id_page_views": 0,
        "text_contrast_samples": 3523,
        "contrast_failure_samples": 0,
        "minimum_contrast_ratio": 4.69,
    }
    for key, expected in expected_wcag_metrics.items():
        observed = wcag_summary.get(key)
        if observed != expected:
            errors.append(f"reader WCAG-preparation summary.{key} must be {expected!r}; found {observed!r}.")
    wcag_boundary = str(wcag_preparation.get("review_boundary", ""))
    for fragment in (
        "clears only the local wcag_conformance_review_not_completed release blocker",
        "not screen-reader review",
        "not assistive-technology review",
        "not third-party or legal WCAG certification",
        "not reader release approval",
    ):
        if fragment not in wcag_boundary:
            errors.append(f"reader WCAG-preparation review_boundary missing {fragment!r}.")

    if key_figure_raster.get("status") != "passed_local_raster_artifact_probe":
        errors.append("reader key-figure raster manifest must remain passed_local_raster_artifact_probe.")
    raster_summary = key_figure_raster.get("summary", {})
    expected_raster_metrics = {
        "figure_count": 10,
        "raster_artifact_count": 10,
        "standard_dimension_count": 10,
        "maximum_transparent_pixel_count": 420,
    }
    for key, expected in expected_raster_metrics.items():
        observed = raster_summary.get(key)
        if observed != expected:
            errors.append(f"reader key-figure raster summary.{key} must be {expected!r}; found {observed!r}.")
    raster_thresholds = {
        "minimum_opaque_pixel_percent": 99.9,
        "minimum_luminance_std": 25.0,
        "minimum_quantized_color_count": 100,
        "minimum_dark_pixel_percent": 0.4,
        "minimum_mid_tone_pixel_percent": 5.0,
    }
    for key, minimum in raster_thresholds.items():
        observed = raster_summary.get(key)
        if not isinstance(observed, (int, float)) or observed < minimum:
            errors.append(f"reader key-figure raster summary.{key} must be at least {minimum}; found {observed!r}.")
    raster_non_claims = " ".join(str(item) for item in key_figure_raster.get("non_claims", [])).lower()
    for fragment in ("automated local png", "not final figure-artifact approval", "not manual aesthetic review", "not reader release approval"):
        if fragment not in raster_non_claims:
            errors.append(f"reader key-figure raster non_claims missing {fragment!r}.")

    if key_figure_epub_layout.get("status") != "passed_local_epub_key_figure_xhtml_layout_probe":
        errors.append("reader key-figure EPUB layout manifest must remain passed_local_epub_key_figure_xhtml_layout_probe.")
    epub_layout_summary = key_figure_epub_layout.get("summary", {})
    if not isinstance(epub_layout_summary, dict):
        errors.append("reader key-figure EPUB layout summary must be an object.")
        epub_layout_summary = {}
    expected_epub_layout_metrics = {
        "figure_count": 10,
        "unique_xhtml_entries": 10,
        "viewport_count": 2,
        "page_view_pairs": 20,
        "failed_page_view_pairs": 0,
        "maximum_horizontal_overflow_px": 0,
        "minimum_image_count": 2,
        "image_failure_count": 0,
        "figure_boundary_count": 10,
        "release_boundary_count": 10,
    }
    for key, expected in expected_epub_layout_metrics.items():
        observed = epub_layout_summary.get(key)
        if observed != expected:
            errors.append(f"reader key-figure EPUB layout summary.{key} must be {expected!r}; found {observed!r}.")
    epub_layout_thresholds = {
        "minimum_body_text_chars": 1_200,
        "minimum_alt_text_words": 12,
    }
    for key, minimum in epub_layout_thresholds.items():
        observed = epub_layout_summary.get(key)
        if not isinstance(observed, (int, float)) or observed < minimum:
            errors.append(f"reader key-figure EPUB layout summary.{key} must be at least {minimum}; found {observed!r}.")
    epub_layout_non_claims = " ".join(str(item) for item in key_figure_epub_layout.get("non_claims", [])).lower()
    for fragment in (
        "local epub xhtml key-figure browser-report probe",
        "not dedicated e-reader device review",
        "not e-reader application approval",
        "not final figure-artifact approval",
        "not reader release approval",
        "does not prove visual quality",
    ):
        if fragment not in epub_layout_non_claims:
            errors.append(f"reader key-figure EPUB layout non_claims missing {fragment!r}.")

    if key_figure_pdf_layout.get("status") != "passed_local_pdf_key_figure_layout_probe":
        errors.append("reader key-figure PDF layout manifest must remain passed_local_pdf_key_figure_layout_probe.")
    pdf_layout_summary = key_figure_pdf_layout.get("summary", {})
    if not isinstance(pdf_layout_summary, dict):
        errors.append("reader key-figure PDF layout summary must be an object.")
        pdf_layout_summary = {}
    expected_pdf_layout_metrics = {
        "figure_count": 10,
        "pdf_pages": 511,
        "unique_caption_pages": 10,
        "raster_pages_rendered": 10,
        "standard_page_size_count": 10,
        "maximum_near_edge_ink_percent": 0.0,
    }
    for key, expected in expected_pdf_layout_metrics.items():
        observed = pdf_layout_summary.get(key)
        if observed != expected:
            errors.append(f"reader key-figure PDF layout summary.{key} must be {expected!r}; found {observed!r}.")
    pdf_layout_thresholds = {
        "minimum_caption_margin_pt": 72.0,
        "minimum_page_ink_percent": 3.0,
        "minimum_luminance_std": 14.0,
    }
    for key, minimum in pdf_layout_thresholds.items():
        observed = pdf_layout_summary.get(key)
        if not isinstance(observed, (int, float)) or observed < minimum:
            errors.append(f"reader key-figure PDF layout summary.{key} must be at least {minimum}; found {observed!r}.")
    pdf_layout_non_claims = " ".join(str(item) for item in key_figure_pdf_layout.get("non_claims", [])).lower()
    for fragment in (
        "local pdf key-figure layout probe",
        "not manual page-by-page pdf review",
        "not final figure-artifact approval",
        "not reader release approval",
        "does not prove visual quality",
    ):
        if fragment not in pdf_layout_non_claims:
            errors.append(f"reader key-figure PDF layout non_claims missing {fragment!r}.")

    if key_figure_docx_layout.get("status") != "passed_local_docx_key_figure_layout_probe":
        errors.append("reader key-figure DOCX layout manifest must remain passed_local_docx_key_figure_layout_probe.")
    docx_layout_summary = key_figure_docx_layout.get("summary", {})
    if not isinstance(docx_layout_summary, dict):
        errors.append("reader key-figure DOCX layout summary must be an object.")
        docx_layout_summary = {}
    expected_docx_layout_metrics = {
        "figure_count": 10,
        "docx_converted_pdf_pages": 512,
        "unique_title_pages": 10,
        "raster_pages_rendered": 10,
        "standard_page_size_count": 10,
        "minimum_title_margin_pt": 72.1,
        "maximum_near_edge_ink_percent": 0.0,
    }
    for key, expected in expected_docx_layout_metrics.items():
        observed = docx_layout_summary.get(key)
        if observed != expected:
            errors.append(f"reader key-figure DOCX layout summary.{key} must be {expected!r}; found {observed!r}.")
    docx_layout_thresholds = {
        "minimum_page_ink_percent": 9.0,
        "minimum_luminance_std": 37.0,
    }
    for key, minimum in docx_layout_thresholds.items():
        observed = docx_layout_summary.get(key)
        if not isinstance(observed, (int, float)) or observed < minimum:
            errors.append(f"reader key-figure DOCX layout summary.{key} must be at least {minimum}; found {observed!r}.")
    docx_layout_non_claims = " ".join(str(item) for item in key_figure_docx_layout.get("non_claims", [])).lower()
    for fragment in (
        "local docx-to-pdf key-figure layout probe",
        "not word review",
        "not libreoffice gui review",
        "not google docs review",
        "not manual document review",
        "not final figure-artifact approval",
        "not reader release approval",
        "does not prove visual quality",
    ):
        if fragment not in docx_layout_non_claims:
            errors.append(f"reader key-figure DOCX layout non_claims missing {fragment!r}.")

    curated_blockers = set(curated_format.get("release_blockers_preserved", []))
    required_curated_format_blockers = REQUIRED_CURATED_BLOCKERS | {
        "full_format_artifact_review_not_completed",
        "app_or_ereader_review_not_completed",
    }
    missing_curated_format_blockers = sorted(required_curated_format_blockers - curated_blockers)
    if missing_curated_format_blockers:
        errors.append(f"curated format probe missing blockers: {missing_curated_format_blockers}")

    review_texts = {name: path.read_text(encoding="utf-8") for name, path in REVIEW_DOCS.items()}
    required_doc_fragments = {
        "reader_html": [
            "The generated reader HTML artifact clears full local browser artifact review",
            "This review does not approve EPUB, DOCX, PDF, e-reader conversion, audio, or",
        ],
        "curated_html": [
            "2ca82608207741a56a861da7d32f4d8c7e7a25dc390df3836dca11560b19ce34",
            "newer local viability",
            "EPUB, DOCX, PDF, e-reader, MP3, M4B, and audio-embedded EPUB artifacts remain",
        ],
        "curated_format": [
            "This does not clear release blockers.",
            "This format probe itself does not clear e-reader/application review",
            "0 unresolved internal hrefs",
            "104 page-view pairs",
            "0 raw .qmd relationship targets",
            "DOCX LibreOffice Headless Review",
            "512 converted pages",
            "0 blank converted-page rasters",
            "not Word review",
            "PDF Extracted Text Reading-Flow Review",
            "44 chapter headings",
            "3 appendix headings",
            "511 nonempty text pages",
            "PDF Chromium Viewer Smoke Review",
            "Scroll-changed pixels",
            "Near-edge raster pages",
            "PDF Page-By-Page Release-Preparation Review",
        ],
        "reader_epub": [
            "not an e-reader",
            "This manifest does not approve EPUB, DOCX, PDF, HTML, e-reader, document, audio, or audio-embedded EPUB artifacts",
        ],
        "reader_docx": [
            "This manifest does not approve DOCX, EPUB, PDF, HTML, e-reader, document, audio, or audio-embedded EPUB artifacts",
        ],
        "reader_pdf": [
            "This manifest does not approve PDF, EPUB, DOCX, HTML, e-reader, document, audio, or audio-embedded EPUB artifacts",
        ],
        "reader_audio": [
            "Audio Script Reading-Flow Review",
            "matches book-structure order",
            "49 ordered markers",
            "66 narration notes",
            "1,089,681 text characters",
            "not narration quality review",
            "final figure-artifact approval, or evidence that audio files exist.",
            "| Draft figure summaries routed | 10 |",
            "This manifest does not approve EPUB, DOCX, PDF, HTML, e-reader, document, audio, MP3, M4B, or audio-embedded EPUB artifacts",
        ],
        "reader_audio_narration_treatment": [
            "Reader Audio Narration Treatment Review",
            AUDIO_NARRATION_TREATMENT_STATUS,
            "script-level narration treatment",
            "clears only `narration_quality_review_not_completed`",
            "66 narration notes",
            "1,089,681 text characters",
            "10 draft key-figure spoken summaries",
            "does not approve pronunciation",
            "does not create MP3, M4B, or audio-embedded EPUB artifacts",
            "does not approve an audiobook",
        ],
        "reader_audio_metadata": [
            "Reader Audio Metadata Review",
            AUDIO_METADATA_STATUS,
            "metadata-only release-preparation review",
            "clears only `audio_metadata_not_reviewed`",
            "Source commit",
            "Audio script digest",
            "does not create MP3",
            "does not approve a narrator",
            "does not timecode chapter markers",
            "does not perform pronunciation or",
            "does not approve audio publication rights",
            "does not approve an audiobook",
        ],
        "reader_human_consumption": [
            "Reader Human-Consumption Gate Review",
            "pass_pre_release_review",
            "Ebook layout",
            "Diagram/image readiness",
            "Bedtime readability",
            "Companion notes",
            "does not clear dedicated e-reader review",
            "final figure-artifact",
            "does not promote any chapter core claim",
        ],
        "reader_final_figure_artifact_review": [
            "Reader Final Figure-Artifact Review",
            "passed_final_figure_artifact_release_preparation_review",
            "final_figure_artifact_review_not_completed",
            "does not approve the curated reader edition",
            "does not promote any chapter core claim",
        ],
        "reader_docx_application_decision": [
            "Reader DOCX Application Evidence Decision",
            "accepted_docx_application_evidence_for_release_preparation",
            "clears only `docx_application_review_not_completed`",
            "does not claim Word, LibreOffice GUI, or Google Docs approval",
            "does not approve DOCX publication",
        ],
        "reader_chapter_reconciliation": [
            "Reader Chapter Reconciliation Approval",
            "passed_curated_chapter_reconciliation_approval",
            "curated_reconciliation_not_approved",
            "does not clear format artifact review",
            "does not promote any chapter core claim",
        ],
        "curated_pdf_page_review": [
            "Curated Reader PDF Page-By-Page Review",
            "passed_pdf_page_by_page_release_preparation_review",
            "manual_pdf_page_by_page_review_not_completed",
            "does not approve the PDF artifact",
        ],
        "reader_figures": [
            "not a release approval and not final figure-artifact review",
            "does not approve final figure art, EPUB, DOCX, PDF, e-reader",
            "docs/reader_key_figure_format_probe.md",
            "docs/reader_key_figure_geometry_review.md",
            "docs/reader_visual_identity_review.md",
            "docs/reader_key_figure_raster_review.md",
            "docs/reader_key_figure_epub_layout_review.md",
            "67 combined colors",
            "current ignored curated EPUB, DOCX, and PDF artifacts",
        ],
        "reader_figure_format": [
            "packaged SVG titles in EPUB",
            "rasterized figure IDs and boundaries in DOCX",
            "extracted captions and figure-boundary paragraphs in PDF",
            "not final figure-artifact approval",
            "not reader release approval",
        ],
        "reader_figure_geometry": [
            "Reader Key-Figure Geometry Review",
            "source-geometry review",
            "Standard viewBox count | 10",
            "Content bounds passed | 10",
            "Text-anchor bounds passed | 10",
            "Minimum visible text nodes | 25",
            "Minimum content edge margin | 22.0 px",
            "not raster review",
            "not final figure-artifact approval",
            "does not approve EPUB, DOCX, PDF, e-reader, audio, or reader release artifacts",
        ],
        "reader_visual_identity": [
            "Reader Visual Identity Review",
            "source-level review",
            "CSS color count | 18",
            "SVG color count | 56",
            "Combined color count | 67",
            "Non-neutral color families | 5",
            "Minimum text contrast ratio | 5.19",
            "not final figure-artifact approval",
            "does not approve EPUB, DOCX, PDF, e-reader, audio, or reader release artifacts",
        ],
        "reader_accessibility_navigation": [
            "Reader Accessibility And Navigation Review",
            "source-level review",
            "Chapter records | 44",
            "Release blockers preserved | 44",
            "Chapters with one H1 | 44",
            "Skipped heading levels | 0",
            "Duplicate heading slugs | 0",
            "Handoff sections | 44",
            "Draft reader images | 10",
            "Figure alt texts | 10",
            "Figure boundary paragraphs | 10",
            "not keyboard-only review",
            "not screen-reader review",
            "not WCAG conformance",
            "does not approve EPUB, DOCX, PDF, e-reader, audio, or reader release artifacts",
        ],
        "reader_keyboard_navigation": [
            "Reader Keyboard Navigation Review",
            "automated browser review",
            "Pages checked | 49",
            "Page-view pairs | 98",
            "Failed page-view pairs | 0",
            "Skip-link route activated | 98",
            "Main-content route available | 98",
            "Keyboard trap candidates | 0",
            "does not perform manual keyboard-only review",
            "does not perform screen-reader review",
            "does not certify WCAG conformance",
            "does not approve EPUB, DOCX, PDF, e-reader, audio, final figure art, or reader release artifacts",
        ],
        "reader_keyboard_only_decision": [
            "Reader Keyboard-Only Evidence Decision",
            "accepted_keyboard_only_evidence_for_release_preparation",
            "Keyboard page-view pairs | 98",
            "Keyboard failed pairs | 0",
            "Keyboard-trap candidates | 0",
            "Cleared blockers | manual_keyboard_only_review_not_completed",
            "does not perform screen-reader review",
            "does not certify WCAG conformance",
            "does not create reader release approval",
            "does not publish or approve curated reader HTML",
        ],
        "reader_accessibility_tree": [
            "Reader Accessibility Tree Review",
            "automated browser review",
            "Pages checked | 49",
            "Page-view pairs | 98",
            "Failed page-view pairs | 0",
            "Accessibility-tree page-view pairs | 98",
            "Unnamed interactive elements | 0",
            "Duplicate-ID page-view hits | 0",
            "does not perform manual keyboard-only review",
            "does not perform screen-reader review",
            "does not certify WCAG conformance",
            "does not approve EPUB, DOCX, PDF, e-reader, audio, final figure art, or reader release artifacts",
        ],
        "reader_wcag_preparation": [
            "Reader WCAG Preparation Review",
            "accepted_wcag_automation_evidence_for_release_preparation",
            "Cleared blockers | wcag_conformance_review_not_completed",
            "Page-view pairs | 98",
            "Contrast failure samples | 0",
            "Minimum contrast ratio | 4.69",
            "does not perform screen-reader or assistive-technology review",
            "does not provide third-party or legal WCAG certification",
        ],
        "reader_figure_raster": [
            "Reader Key-Figure Raster Review",
            "Raster artifacts checked | 10",
            "Standard dimensions | 10",
            "Minimum opaque pixel coverage | 99.954%",
            "Minimum luminance standard deviation | 27.64",
            "Minimum quantized color count | 116",
            "not manual aesthetic review",
            "not final figure-artifact approval",
            "not reader release approval",
        ],
        "reader_figure_epub_layout": [
            "Reader Key-Figure EPUB Layout Review",
            "Key-figure XHTML entries | 10",
            "Browser page-view pairs | 20",
            "Failed page-view pairs | 0",
            "Maximum horizontal overflow | 0 px",
            "Image failures | 0",
            "not dedicated e-reader device review",
            "not e-reader application approval",
            "not final figure-artifact approval",
            "not reader release approval",
        ],
        "reader_epub_apple_books": [
            "Reader EPUB Apple Books Review",
            "passed_apple_books_epub_application_review",
            "zero XML parse errors",
            "clears only `app_or_ereader_review_not_completed`",
            "does not approve the curated reader edition",
        ],
        "reader_figure_pdf_layout": [
            "Reader Key-Figure PDF Layout Review",
            "Key-figure caption pages | 10",
            "Raster pages rendered | 10",
            "Minimum caption margin | 165.878 pt",
            "Maximum near-edge ink | 0.0%",
            "not manual page-by-page PDF review",
            "not final figure-artifact approval",
            "not reader release approval",
        ],
        "reader_figure_docx_layout": [
            "Reader Key-Figure DOCX Layout Review",
            "Key-figure title pages | 10",
            "Raster pages rendered | 10",
            "Minimum title margin | 72.1 pt",
            "Maximum near-edge ink | 0.0%",
            "not Word review",
            "not LibreOffice GUI review",
            "not Google Docs review",
            "not manual document review",
            "not final figure-artifact approval",
            "not reader release approval",
        ],
    }
    for doc_name, fragments in required_doc_fragments.items():
        for fragment in fragments:
            if fragment not in review_texts[doc_name]:
                errors.append(f"{rel(REVIEW_DOCS[doc_name])} missing required fragment: {fragment}")

    generated_html_pages = int_metric(review_texts["reader_html"], "Pages opened")
    generated_html_pairs = int_metric(review_texts["reader_html"], "Page-view pairs")
    generated_html_failures = int_metric(review_texts["reader_html"], "Failed page-view pairs")
    curated_html_pages = int_metric(review_texts["curated_html"], "Pages opened")
    curated_html_pairs = int_metric(review_texts["curated_html"], "Page-view pairs")
    curated_html_failures = int_metric(review_texts["curated_html"], "Failed page-view pairs")
    curated_key_figure_pairs = int_metric(review_texts["curated_html"], "Reader key-figure page-view pairs")
    curated_key_figure_failures = int_metric(review_texts["curated_html"], "Failed reader key-figure checks")
    if generated_html_pages != 59 or generated_html_pairs != 118 or generated_html_failures != 0:
        errors.append("generated reader HTML browser-review metrics must stay at 59 pages, 118 pairs, and 0 failures.")
    if curated_html_pages != 49 or curated_html_pairs != 98 or curated_html_failures != 0:
        errors.append("curated reader HTML browser-review metrics must stay at 49 pages, 98 pairs, and 0 failures.")
    if curated_key_figure_pairs != 20 or curated_key_figure_failures != 0:
        errors.append("curated reader HTML key-figure browser metrics must stay at 20 pairs and 0 failures.")

    human_ebook_facts = human_gate_records.get("ebook_layout_review", {}).get("facts", {})
    human_diagram_facts = human_gate_records.get("diagram_image_review", {}).get("facts", {})
    human_bedtime_facts = human_gate_records.get("bedtime_readability_review", {}).get("facts", {})
    human_companion_facts = human_gate_records.get("companion_notes_status", {}).get("facts", {})
    if not isinstance(human_ebook_facts, dict):
        human_ebook_facts = {}
    if not isinstance(human_diagram_facts, dict):
        human_diagram_facts = {}
    if not isinstance(human_bedtime_facts, dict):
        human_bedtime_facts = {}
    if not isinstance(human_companion_facts, dict):
        human_companion_facts = {}

    metrics: dict[str, Any] = {
        "profile_count": len(profile_ids),
        "profile_ids": sorted(profile_ids),
        "reader_manifest_status": reader_manifest.get("status"),
        "curated_record_count": len(chapter_records),
        "curated_reconciliation_counts": reconciliation_counts,
        "missing_curated_files": len(missing_curated_files),
        "chapter_reconciliation_approval_status": chapter_reconciliation_approval.get("status"),
        "chapter_reconciliation_approval_rows": reconciliation_approval_summary.get("passed_rows"),
        "chapter_reconciliation_approval_cleared_blockers": len(
            chapter_reconciliation_approval.get("cleared_blockers", [])
        )
        if isinstance(chapter_reconciliation_approval.get("cleared_blockers"), list)
        else None,
        "voice_slot_count": len(handoff.get("corben_voice_pass_slots", [])),
        "signature_idea_count": len(handoff.get("signature_ideas", [])),
        "key_figure_target_count": len(handoff.get("key_figure_targets", [])),
        "part_arc_count": len(handoff.get("part_arcs", [])),
        "chapter_review_count": len(chapters),
        "chapter_review_counts": review_counts,
        "disposition_counts": disposition_counts,
        "overlay_operation_count": overlay_operation_count,
        "format_approved": approved_formats,
        "format_blocked": blocked_formats,
        "format_blocker_counts": blocker_counts,
        "curated_candidate_count": len(curated_candidate_records),
        "curated_candidate_status": curated_candidate.get("status"),
        "curated_candidate_blocker_counts": curated_candidate_blocker_counts,
        "curated_blocked_record": rel(CURATED_BLOCKED_RECORD),
        "curated_blocked_record_status": curated_blocked_record.get("validation_status"),
        "curated_blocked_probe_status": blocked_probe_closure.get("status"),
        "generated_html_pages": generated_html_pages,
        "generated_html_pairs": generated_html_pairs,
        "generated_html_failures": generated_html_failures,
        "curated_html_pages": curated_html_pages,
        "curated_html_pairs": curated_html_pairs,
        "curated_html_failures": curated_html_failures,
        "curated_key_figure_pairs": curated_key_figure_pairs,
        "curated_key_figure_failures": curated_key_figure_failures,
        "curated_html_digest": "2ca82608207741a56a861da7d32f4d8c7e7a25dc390df3836dca11560b19ce34",
        "curated_html_files": curated_inspection.get("html", {}).get("html_files"),
        "curated_epub_xhtml": curated_inspection.get("epub", {}).get("xhtml_entries"),
        "curated_epub_audit_xhtml": curated_epub_content_audit.get("xhtml_entries_checked"),
        "curated_epub_audit_content_xhtml": curated_epub_content_audit.get("content_xhtml_entries_checked"),
        "curated_epub_audit_unresolved": curated_epub_content_audit.get("unresolved_internal_hrefs"),
        "curated_epub_audit_sha": curated_epub_content_audit.get("source_sha256"),
        "curated_epub_browser_pairs": curated_epub_browser_review.get("page_view_pairs"),
        "curated_epub_browser_failures": curated_epub_browser_review.get("failed_page_view_pairs"),
        "curated_epub_browser_max_overflow": curated_epub_browser_review.get("max_horizontal_overflow_px"),
        "epub_app_review_status": epub_app_review.get("status"),
        "epub_app_review_sha": epub_app_review.get("source_sha256"),
        "epub_app_review_observations": len(epub_app_review.get("observations", [])),
        "epub_app_review_cleared_blockers": len(epub_app_review.get("cleared_blockers", [])),
        "curated_docx_png": curated_inspection.get("docx", {}).get("png_media_entries"),
        "curated_docx_svg": curated_inspection.get("docx", {}).get("svg_media_entries"),
        "curated_docx_audit_paragraphs": curated_docx_content_audit.get("paragraph_markers"),
        "curated_docx_audit_relationships": curated_docx_content_audit.get("relationship_count"),
        "curated_docx_audit_raw_qmd": curated_docx_content_audit.get("raw_qmd_relationship_targets"),
        "curated_docx_audit_sha": curated_docx_content_audit.get("source_sha256"),
        "curated_docx_libreoffice_pages": curated_docx_libreoffice_review.get("converted_pdf_pages"),
        "curated_docx_libreoffice_text_chars": curated_docx_libreoffice_review.get("text_characters_checked"),
        "curated_docx_libreoffice_blank_pages": curated_docx_libreoffice_review.get("blank_pages"),
        "curated_docx_libreoffice_low_ink_pages": curated_docx_libreoffice_review.get("low_ink_pages"),
        "curated_docx_libreoffice_near_edge_pages": curated_docx_libreoffice_review.get("near_edge_content_pages"),
        "curated_pdf_pages": curated_inspection.get("pdf", {}).get("pages"),
        "curated_pdf_raster_pages": curated_pdf_visual_raster_audit.get("pages_rendered"),
        "curated_pdf_raster_blank_pages": curated_pdf_visual_raster_audit.get("blank_pages"),
        "curated_pdf_raster_low_ink_pages": curated_pdf_visual_raster_audit.get("low_ink_pages"),
        "curated_pdf_raster_near_edge_pages": curated_pdf_visual_raster_audit.get("near_edge_content_pages"),
        "curated_pdf_reading_flow_text_pages": curated_pdf_reading_flow_review.get("text_pages_checked"),
        "curated_pdf_reading_flow_nonempty_pages": curated_pdf_reading_flow_review.get("nonempty_text_pages"),
        "curated_pdf_reading_flow_chapters": curated_pdf_reading_flow_review.get("chapter_headings_checked"),
        "curated_pdf_reading_flow_appendices": curated_pdf_reading_flow_review.get("appendix_headings_checked"),
        "curated_pdf_reading_flow_replacement_chars": curated_pdf_reading_flow_review.get("replacement_character_count"),
        "curated_pdf_viewer_screenshots": len(curated_pdf_viewer_review.get("screenshots", []))
        if isinstance(curated_pdf_viewer_review, dict)
        else 0,
        "curated_pdf_viewer_scroll_changed_pixels": curated_pdf_viewer_review.get("page_down_changed_pixel_percent")
        if isinstance(curated_pdf_viewer_review, dict)
        else None,
        "curated_pdf_page_review_status": pdf_page_review.get("status"),
        "curated_pdf_page_review_rows": pdf_page_summary.get("page_review_rows"),
        "curated_pdf_page_review_failed_pages": len(pdf_page_summary.get("failed_pages", []))
        if isinstance(pdf_page_summary.get("failed_pages"), list)
        else None,
        "curated_pdf_page_review_blank_pages": len(pdf_page_summary.get("blank_pages", []))
        if isinstance(pdf_page_summary.get("blank_pages"), list)
        else None,
        "curated_pdf_page_review_near_edge_pages": len(pdf_page_summary.get("near_edge_pages", []))
        if isinstance(pdf_page_summary.get("near_edge_pages"), list)
        else None,
        "curated_pdf_page_review_out_of_bounds_pages": len(
            pdf_page_summary.get("out_of_bounds_word_box_pages", [])
        )
        if isinstance(pdf_page_summary.get("out_of_bounds_word_box_pages"), list)
        else None,
        "curated_pdf_page_review_low_ink_pages": len(pdf_page_summary.get("low_ink_pages", []))
        if isinstance(pdf_page_summary.get("low_ink_pages"), list)
        else None,
        "final_figure_review_status": final_figure_review.get("status"),
        "final_figure_review_figures": final_figure_summary.get("figure_count"),
        "final_figure_review_cleared_blockers": len(final_figure_review.get("cleared_blockers", []))
        if isinstance(final_figure_review.get("cleared_blockers"), list)
        else None,
        "reader_html_files": reader_inspection.get("html", {}).get("html_files"),
        "reader_epub_bytes": epub_summary.get("file_size_bytes"),
        "reader_epub_language": epub_probe.get("metadata_summary", {}).get("language"),
        "reader_docx_pages": docx_conversion.get("pages"),
        "reader_docx_bytes": docx_conversion.get("file_size_bytes"),
        "reader_pdf_pages": pdf_info.get("pages"),
        "reader_pdf_bytes": pdf_info.get("file_size_bytes"),
        "audio_script_files": audio_workspace.get("script_files"),
        "audio_reading_flow_markers": audio_reading_flow.get("chapter_marker_rows"),
        "audio_reading_flow_narration_notes": audio_reading_flow.get("narration_note_count"),
        "audio_reading_flow_text_chars": audio_reading_flow.get("text_characters_checked"),
        "audio_reading_flow_tbd_rows": audio_reading_flow.get("chapter_marker_tbd_rows"),
        "audio_targets": audio_targets,
        "audio_key_figure_count": audio_key_figures.get("figure_count"),
        "audio_narration_treatment_status": audio_narration_treatment_review.get("status"),
        "audio_narration_treatment_cleared_blockers": len(
            audio_narration_treatment_review.get("cleared_blockers", [])
        )
        if isinstance(audio_narration_treatment_review.get("cleared_blockers"), list)
        else None,
        "audio_narration_treatment_preserved_blockers": len(
            audio_narration_treatment_review.get("preserved_blockers", [])
        )
        if isinstance(audio_narration_treatment_review.get("preserved_blockers"), list)
        else None,
        "audio_metadata_status": audio_metadata_review.get("status"),
        "audio_metadata_cleared_blockers": len(audio_metadata_review.get("cleared_blockers", []))
        if isinstance(audio_metadata_review.get("cleared_blockers"), list)
        else None,
        "audio_metadata_preserved_blockers": len(audio_metadata_review.get("preserved_blockers", []))
        if isinstance(audio_metadata_review.get("preserved_blockers"), list)
        else None,
        "audio_metadata_title": metadata_fields.get("title"),
        "audio_metadata_version": metadata_fields.get("major_version"),
        "audio_metadata_language": metadata_fields.get("language"),
        "human_consumption_gate_status": human_consumption_gate.get("status"),
        "human_consumption_gate_statuses": human_gate_statuses,
        "human_consumption_epub_pairs": human_ebook_facts.get("epub_key_figure_page_view_pairs"),
        "human_consumption_epub_failures": human_ebook_facts.get("epub_key_figure_failed_pairs"),
        "human_consumption_pdf_caption_pages": human_ebook_facts.get("pdf_key_figure_caption_pages"),
        "human_consumption_docx_title_pages": human_ebook_facts.get("docx_key_figure_title_pages"),
        "human_consumption_diagram_figures": human_diagram_facts.get("key_figures"),
        "human_consumption_diagram_rasters": human_diagram_facts.get("raster_artifacts"),
        "human_consumption_min_luminance_std": human_diagram_facts.get("raster_min_luminance_std"),
        "human_consumption_readability_chapters": human_bedtime_facts.get("chapter_records"),
        "human_consumption_readability_min_words": human_bedtime_facts.get("minimum_chapter_words"),
        "human_consumption_readability_max_words": human_bedtime_facts.get("maximum_chapter_words"),
        "human_consumption_readability_max_paragraph_words": human_bedtime_facts.get("maximum_paragraph_words"),
        "human_consumption_live_marker_hits": human_bedtime_facts.get("live_marker_hits"),
        "human_consumption_companion_routes": human_companion_facts.get("routing_records"),
        "human_consumption_companion_existing": human_companion_facts.get("routing_records_with_existing_notes"),
        "human_consumption_companion_summaries": human_companion_facts.get("audio_probe_companion_summaries"),
        "key_figure_epub_svg_entries": key_figure_format_probe.get("epub", {}).get("svg_entries"),
        "key_figure_epub_matched_titles": key_figure_format_probe.get("epub", {}).get(
            "matched_source_svg_titles"
        ),
        "key_figure_docx_matched_stems": key_figure_format_probe.get("docx", {}).get(
            "matched_figure_stems"
        ),
        "key_figure_pdf_matched_captions": key_figure_format_probe.get("pdf", {}).get(
            "matched_caption_titles"
        ),
        "key_figure_geometry_status": key_figure_geometry.get("status"),
        "key_figure_geometry_count": geometry_summary.get("figure_count"),
        "key_figure_geometry_content_bounds": geometry_summary.get("content_bounds_passed_count"),
        "key_figure_geometry_text_anchor_bounds": geometry_summary.get("text_anchor_bounds_passed_count"),
        "key_figure_geometry_min_edge_margin": geometry_summary.get("minimum_content_edge_margin_px"),
        "visual_identity_status": visual_identity.get("status"),
        "visual_identity_color_count": visual_palette.get("combined_hex_color_count"),
        "visual_identity_non_neutral_families": visual_palette.get("non_neutral_family_count"),
        "visual_identity_figure_count": visual_figures.get("figure_count"),
        "visual_identity_min_text_contrast": visual_contrast.get("minimum_text_contrast_ratio"),
        "reader_accessibility_navigation_status": accessibility_navigation.get("status"),
        "reader_accessibility_navigation_chapters": access_summary.get("chapter_records"),
        "reader_accessibility_navigation_h1": access_summary.get("chapters_with_one_h1"),
        "reader_accessibility_navigation_handoffs": access_summary.get("handoff_sections"),
        "reader_accessibility_navigation_fig_alts": access_summary.get("fig_alt_count"),
        "reader_accessibility_navigation_boundaries": access_summary.get("figure_boundary_count"),
        "reader_accessibility_navigation_live_marker_leaks": access_summary.get("live_marker_leak_count"),
        "reader_accessibility_navigation_raw_claim_leaks": access_summary.get("raw_core_claim_marker_leak_count"),
        "reader_keyboard_navigation_status": keyboard_navigation.get("status"),
        "reader_keyboard_navigation_pages": keyboard_summary.get("pages_checked"),
        "reader_keyboard_navigation_pairs": keyboard_summary.get("page_view_pairs"),
        "reader_keyboard_navigation_failures": keyboard_summary.get("failed_page_view_pairs"),
        "reader_keyboard_navigation_skip_reached": keyboard_summary.get("skip_link_reached_pairs"),
        "reader_keyboard_navigation_skip_activated": keyboard_summary.get("skip_link_activated_pairs"),
        "reader_keyboard_navigation_main_route": keyboard_summary.get("main_content_route_available_pairs"),
        "reader_keyboard_navigation_nav_reached": keyboard_summary.get("navigation_focus_reached_pairs"),
        "reader_keyboard_navigation_search_reached": keyboard_summary.get("search_focus_reached_pairs"),
        "reader_keyboard_navigation_traps": keyboard_summary.get("keyboard_trap_candidates"),
        "reader_keyboard_only_decision_status": keyboard_only_decision.get("status"),
        "reader_keyboard_only_decision_cleared": len(keyboard_only_decision.get("cleared_blockers", []))
        if isinstance(keyboard_only_decision.get("cleared_blockers"), list)
        else None,
        "reader_keyboard_only_decision_preserved": len(keyboard_only_decision.get("preserved_blockers", []))
        if isinstance(keyboard_only_decision.get("preserved_blockers"), list)
        else None,
        "reader_accessibility_tree_status": accessibility_tree.get("status"),
        "reader_accessibility_tree_pages": accessibility_tree_summary.get("pages_checked"),
        "reader_accessibility_tree_pairs": accessibility_tree_summary.get("page_view_pairs"),
        "reader_accessibility_tree_failures": accessibility_tree_summary.get("failed_page_view_pairs"),
        "reader_accessibility_tree_ax_pairs": accessibility_tree_summary.get("accessibility_tree_pairs"),
        "reader_accessibility_tree_unnamed": accessibility_tree_summary.get("unnamed_interactive_elements"),
        "reader_accessibility_tree_image_alt_failures": accessibility_tree_summary.get("image_alt_failures"),
        "reader_accessibility_tree_table_header_failures": accessibility_tree_summary.get("table_header_failures"),
        "reader_accessibility_tree_duplicate_ids": accessibility_tree_summary.get("duplicate_id_page_views"),
        "reader_wcag_preparation_status": wcag_preparation.get("status"),
        "reader_wcag_preparation_pairs": wcag_summary.get("page_view_pairs"),
        "reader_wcag_preparation_failures": wcag_summary.get("failed_page_view_pairs"),
        "reader_wcag_preparation_contrast_samples": wcag_summary.get("text_contrast_samples"),
        "reader_wcag_preparation_contrast_failures": wcag_summary.get("contrast_failure_samples"),
        "reader_wcag_preparation_min_contrast": wcag_summary.get("minimum_contrast_ratio"),
        "reader_wcag_preparation_cleared": len(wcag_preparation.get("cleared_blockers", []))
        if isinstance(wcag_preparation.get("cleared_blockers"), list)
        else None,
        "key_figure_raster_status": key_figure_raster.get("status"),
        "key_figure_raster_count": raster_summary.get("raster_artifact_count"),
        "key_figure_raster_standard_dimensions": raster_summary.get("standard_dimension_count"),
        "key_figure_raster_min_opaque_percent": raster_summary.get("minimum_opaque_pixel_percent"),
        "key_figure_raster_min_luminance_std": raster_summary.get("minimum_luminance_std"),
        "key_figure_raster_min_colors": raster_summary.get("minimum_quantized_color_count"),
        "key_figure_epub_layout_status": key_figure_epub_layout.get("status"),
        "key_figure_epub_layout_entries": epub_layout_summary.get("unique_xhtml_entries"),
        "key_figure_epub_layout_pairs": epub_layout_summary.get("page_view_pairs"),
        "key_figure_epub_layout_failures": epub_layout_summary.get("failed_page_view_pairs"),
        "key_figure_epub_layout_min_body_chars": epub_layout_summary.get("minimum_body_text_chars"),
        "key_figure_epub_layout_min_alt_words": epub_layout_summary.get("minimum_alt_text_words"),
        "key_figure_epub_layout_max_overflow": epub_layout_summary.get("maximum_horizontal_overflow_px"),
        "key_figure_epub_layout_image_failures": epub_layout_summary.get("image_failure_count"),
        "key_figure_pdf_layout_status": key_figure_pdf_layout.get("status"),
        "key_figure_pdf_layout_pages": pdf_layout_summary.get("pdf_pages"),
        "key_figure_pdf_layout_caption_pages": pdf_layout_summary.get("unique_caption_pages"),
        "key_figure_pdf_layout_raster_pages": pdf_layout_summary.get("raster_pages_rendered"),
        "key_figure_pdf_layout_min_caption_margin": pdf_layout_summary.get("minimum_caption_margin_pt"),
        "key_figure_pdf_layout_min_page_ink": pdf_layout_summary.get("minimum_page_ink_percent"),
        "key_figure_pdf_layout_max_near_edge_ink": pdf_layout_summary.get("maximum_near_edge_ink_percent"),
        "key_figure_pdf_layout_min_luminance_std": pdf_layout_summary.get("minimum_luminance_std"),
        "key_figure_docx_layout_status": key_figure_docx_layout.get("status"),
        "key_figure_docx_layout_pages": docx_layout_summary.get("docx_converted_pdf_pages"),
        "key_figure_docx_layout_title_pages": docx_layout_summary.get("unique_title_pages"),
        "key_figure_docx_layout_raster_pages": docx_layout_summary.get("raster_pages_rendered"),
        "key_figure_docx_layout_min_title_margin": docx_layout_summary.get("minimum_title_margin_pt"),
        "key_figure_docx_layout_min_page_ink": docx_layout_summary.get("minimum_page_ink_percent"),
        "key_figure_docx_layout_max_near_edge_ink": docx_layout_summary.get("maximum_near_edge_ink_percent"),
        "key_figure_docx_layout_min_luminance_std": docx_layout_summary.get("minimum_luminance_std"),
        "docx_application_decision_status": docx_application_decision.get("status"),
        "docx_application_decision_cleared_blockers": len(docx_application_decision.get("cleared_blockers", []))
        if isinstance(docx_application_decision.get("cleared_blockers"), list)
        else None,
        "docx_application_decision_preserved_blockers": len(docx_application_decision.get("preserved_blockers", []))
        if isinstance(docx_application_decision.get("preserved_blockers"), list)
        else None,
        "release_record": rel(HTML_RELEASE_RECORD),
    }
    return metrics, errors


def compact_status_row(metrics: dict[str, Any] | None = None) -> str:
    if metrics is None:
        metrics, errors = collect_metrics()
        if errors:
            fail(errors)
    reconciliation_counts: Counter[str] = metrics["curated_reconciliation_counts"]
    return (
        "| Release surfaces | Live, research, reader, and audio profiles exist. "
        "Release detail is generated in `docs/release_surface_status_ledger.md`: generated-reader HTML remains the only approved reader artifact; "
        f"`{metrics['curated_blocked_record']}` records the current curated-reader candidate as partial and blocked; "
        f"`docs/reader_format_review_matrix.md` tracks {metrics['curated_candidate_count']} current curated-candidate rows with release blockers; "
        f"automated keyboard traversal covers {metrics['reader_keyboard_navigation_pairs']} page-view pairs with "
        f"{metrics['reader_keyboard_navigation_failures']} failures; "
        f"keyboard-only evidence decision is `{metrics['reader_keyboard_only_decision_status']}` and clears "
        f"{metrics['reader_keyboard_only_decision_cleared']} blocker; "
        f"accessibility-tree release-preparation covers {metrics['reader_accessibility_tree_pairs']} page-view pairs with "
        f"{metrics['reader_accessibility_tree_failures']} failures and {metrics['reader_accessibility_tree_unnamed']} unnamed interactive elements; "
        f"WCAG-preparation evidence is `{metrics['reader_wcag_preparation_status']}` with "
        f"{metrics['reader_wcag_preparation_contrast_samples']} text contrast samples, "
        f"{metrics['reader_wcag_preparation_contrast_failures']} contrast failures, and "
        f"{metrics['reader_wcag_preparation_min_contrast']} minimum contrast; "
        f"the human-consumption pre-release gate is `{metrics['human_consumption_gate_status']}`; "
        f"PDF page-by-page release-preparation review covers {metrics['curated_pdf_page_review_rows']} pages with "
        f"{metrics['curated_pdf_page_review_failed_pages']} failures; "
        f"final figure-artifact review is `{metrics['final_figure_review_status']}` for "
        f"{metrics['final_figure_review_figures']} figures; "
        f"the curated manuscript remains `{metrics['reader_manifest_status']}` with "
        f"{metrics['curated_record_count']} records ({reconciliation_counts.get('reconciled', 0)} reconciled); "
        f"chapter reconciliation approval is `{metrics['chapter_reconciliation_approval_status']}`; "
        f"{metrics['overlay_operation_count']} overlay operations are tracked; "
        "Apple Books EPUB application review, the DOCX application-evidence decision, keyboard-only evidence decision, automated WCAG-preparation decision, script-level audio narration treatment review, and audio metadata review are passed, while screen-reader review, EPUB publication, DOCX publication, PDF, audio files, chapter timing, listening review, and refreshed reader HTML remain unapproved. | "
        "`docs/release_surface_status_ledger.md`; `editions/release_profiles.json`; "
        "`editions/reader_overlays/v1_0/manifest.json`; `editions/reader_manuscript/v1_0/manifest.json`; "
        "`editions/reader_manuscript/v1_0/chapter_review_matrix.json`; "
        "`editions/reader_manuscript/v1_0/chapter_reconciliation_approval_manifest.json`; "
        "`editions/reader_manuscript/v1_0/format_review_matrix.json`; "
        "`docs/reader_chapter_review_matrix.md`; `docs/reader_chapter_reconciliation_approval.md`; "
        "`docs/reader_format_review_matrix.md`; "
        "`docs/reader_html_artifact_browser_review.md`; `docs/curated_reader_html_artifact_browser_review.md`; "
        "`docs/curated_reader_format_artifact_probe.md`; `docs/reader_epub_probe_manifest.md`; "
        "`docs/reader_docx_probe_manifest.md`; `docs/reader_pdf_probe_manifest.md`; "
        "`docs/reader_audio_script_probe_manifest.md`; `docs/reader_audio_narration_treatment_review.md`; "
        "`docs/reader_audio_metadata_review.md`; "
        "`docs/reader_key_figure_format_probe.md`; "
        "`docs/reader_human_consumption_gate_review.md`; "
        "`docs/curated_reader_pdf_page_review.md`; "
        "`docs/reader_final_figure_artifact_review.md`; "
        "`docs/reader_key_figure_geometry_review.md`; `docs/reader_visual_identity_review.md`; "
        "`docs/reader_accessibility_navigation_review.md`; `docs/reader_key_figure_raster_review.md`; "
        "`docs/reader_keyboard_navigation_review.md`; `docs/reader_keyboard_only_decision.md`; "
        "`docs/reader_accessibility_tree_review.md`; `docs/reader_wcag_preparation_review.md`; "
        "`docs/reader_key_figure_epub_layout_review.md`; "
        "`docs/reader_epub_apple_books_review.md`; "
        "`docs/reader_docx_application_decision.md`; "
        "`docs/reader_key_figure_pdf_layout_review.md`; "
        "`docs/reader_key_figure_docx_layout_review.md`; "
        "`release_records/2026-06-29-v1-reader-html-855dc277.json`; "
        "`release_records/2026-07-05-v1-curated-reader-blocked-3e59bde3.json`; "
        "`python3 scripts/validate_curated_reader_blocked_release_record.py`; "
        "`python3 scripts/validate_curated_reader_pdf_page_review.py`; "
        "`python3 scripts/validate_reader_human_consumption_gate.py`; "
        "`python3 scripts/validate_reader_final_figure_artifact_review.py`; "
        "`python3 scripts/validate_reader_chapter_reconciliation_approval.py`; "
        "`python3 scripts/validate_reader_docx_application_decision.py`; "
        "`python3 scripts/validate_reader_keyboard_only_decision.py`; "
        "`python3 scripts/validate_reader_wcag_preparation.py`; "
        "`python3 scripts/validate_reader_audio_narration_treatment.py`; "
        "`python3 scripts/validate_reader_audio_metadata_review.py`; "
        "`python3 scripts/validate_release_surface_status_ledger.py` |"
    )


def build_report(metrics: dict[str, Any], errors: list[str]) -> str:
    reconciliation_counts: Counter[str] = metrics["curated_reconciliation_counts"]
    review_counts: Counter[str] = metrics["chapter_review_counts"]
    disposition_counts: Counter[str] = metrics["disposition_counts"]
    blocker_counts: Counter[str] = metrics["format_blocker_counts"]
    audio_targets: dict[str, str] = metrics["audio_targets"]

    validation_lines = ["- None."] if not errors else [f"- {error}" for error in errors]
    return "\n".join(
        [
            "# Release Surface Status Ledger",
            "",
            "Generated by `python3 scripts/validate_release_surface_status_ledger.py --write`.",
            "",
            "This ledger replaces the former long `Release surfaces` cell in `docs/v1_0_candidate_status.md`.",
            "It records release-profile, reader-manuscript, format-probe, and artifact-review state only; it does not create reader release approval, audiobook approval, publication approval, or claim-support movement.",
            "",
            "## Summary",
            "",
            "| Metric | Value |",
            "|---|---:|",
            f"| Release profiles present | {metrics['profile_count']} |",
            f"| Curated reader chapter records | {metrics['curated_record_count']} |",
            f"| Curated reconciliation states | {qmd_escape(counter_phrase(reconciliation_counts))} |",
            f"| Chapter reconciliation approval | `{metrics['chapter_reconciliation_approval_status']}`; {metrics['chapter_reconciliation_approval_rows']} rows, {metrics['chapter_reconciliation_approval_cleared_blockers']} blocker cleared |",
            f"| Missing curated chapter files | {metrics['missing_curated_files']} |",
            f"| Reader review rows | {metrics['chapter_review_count']} |",
            f"| Reader review states | {qmd_escape(counter_phrase(review_counts))} |",
            f"| Active-overlay chapters | {disposition_counts.get('reader_overlay_active', 0)} |",
            f"| Active overlay operations | {metrics['overlay_operation_count']} |",
            f"| No-immediate-action decisions | {disposition_counts.get('no_immediate_action', 0)} |",
            f"| Companion-note candidates | {disposition_counts.get('companion_note_candidate', 0)} |",
            f"| Curated-manuscript candidates | {disposition_counts.get('curated_manuscript_candidate', 0)} |",
            f"| Key-figure targets | {metrics['key_figure_target_count']} |",
            f"| Key figures matched in EPUB/DOCX/PDF probes | {metrics['key_figure_epub_matched_titles']} / {metrics['key_figure_docx_matched_stems']} / {metrics['key_figure_pdf_matched_captions']} |",
            f"| Key-figure source geometry status | `{metrics['key_figure_geometry_status']}` |",
            f"| Key-figure source geometry bounds | {metrics['key_figure_geometry_content_bounds']} content / {metrics['key_figure_geometry_text_anchor_bounds']} text-anchor, min edge {metrics['key_figure_geometry_min_edge_margin']} px |",
            f"| Source-level visual identity status | `{metrics['visual_identity_status']}` |",
            f"| Source-level visual identity colors | {metrics['visual_identity_color_count']} total / {metrics['visual_identity_non_neutral_families']} non-neutral families |",
            f"| Reader source accessibility/navigation status | `{metrics['reader_accessibility_navigation_status']}` |",
            f"| Reader source accessibility/navigation checks | {metrics['reader_accessibility_navigation_chapters']} chapters, {metrics['reader_accessibility_navigation_h1']} one-H1 chapters, {metrics['reader_accessibility_navigation_handoffs']} handoffs, {metrics['reader_accessibility_navigation_fig_alts']} figure alt texts |",
            f"| Reader automated keyboard traversal status | `{metrics['reader_keyboard_navigation_status']}` |",
            f"| Reader automated keyboard traversal checks | {metrics['reader_keyboard_navigation_pairs']} page-view pairs, {metrics['reader_keyboard_navigation_failures']} failures, {metrics['reader_keyboard_navigation_skip_activated']} skip-link activations, {metrics['reader_keyboard_navigation_traps']} trap candidates |",
            f"| Reader keyboard-only evidence decision | `{metrics['reader_keyboard_only_decision_status']}`; {metrics['reader_keyboard_only_decision_cleared']} blocker cleared, {metrics['reader_keyboard_only_decision_preserved']} blockers preserved |",
            f"| Reader accessibility-tree status | `{metrics['reader_accessibility_tree_status']}` |",
            f"| Reader accessibility-tree checks | {metrics['reader_accessibility_tree_pairs']} page-view pairs, {metrics['reader_accessibility_tree_failures']} failures, {metrics['reader_accessibility_tree_ax_pairs']} accessibility-tree pairs, {metrics['reader_accessibility_tree_unnamed']} unnamed interactive elements, {metrics['reader_accessibility_tree_duplicate_ids']} duplicate-ID hits |",
            f"| Reader WCAG-preparation status | `{metrics['reader_wcag_preparation_status']}`; {metrics['reader_wcag_preparation_cleared']} blocker cleared |",
            f"| Reader WCAG-preparation checks | {metrics['reader_wcag_preparation_pairs']} page-view pairs, {metrics['reader_wcag_preparation_failures']} failures, {metrics['reader_wcag_preparation_contrast_samples']} text contrast samples, {metrics['reader_wcag_preparation_contrast_failures']} contrast failures, minimum contrast {metrics['reader_wcag_preparation_min_contrast']} |",
            f"| Key-figure raster status | `{metrics['key_figure_raster_status']}` |",
            f"| Key-figure raster checks | {metrics['key_figure_raster_count']} PNGs, {metrics['key_figure_raster_standard_dimensions']} standard dimensions, min luminance std {metrics['key_figure_raster_min_luminance_std']}, min colors {metrics['key_figure_raster_min_colors']} |",
            f"| Key-figure EPUB layout status | `{metrics['key_figure_epub_layout_status']}` |",
            f"| Key-figure EPUB layout checks | {metrics['key_figure_epub_layout_entries']} XHTML entries, {metrics['key_figure_epub_layout_pairs']} page-view pairs, {metrics['key_figure_epub_layout_failures']} failures, max overflow {metrics['key_figure_epub_layout_max_overflow']} px, {metrics['key_figure_epub_layout_image_failures']} image failures |",
            f"| Key-figure PDF layout status | `{metrics['key_figure_pdf_layout_status']}` |",
            f"| Key-figure PDF layout checks | {metrics['key_figure_pdf_layout_caption_pages']} caption pages, {metrics['key_figure_pdf_layout_raster_pages']} raster pages, min caption margin {metrics['key_figure_pdf_layout_min_caption_margin']} pt, min page ink {metrics['key_figure_pdf_layout_min_page_ink']}%, max near-edge ink {metrics['key_figure_pdf_layout_max_near_edge_ink']}%, min luminance std {metrics['key_figure_pdf_layout_min_luminance_std']} |",
            f"| Key-figure DOCX layout status | `{metrics['key_figure_docx_layout_status']}` |",
            f"| Key-figure DOCX layout checks | {metrics['key_figure_docx_layout_title_pages']} title pages, {metrics['key_figure_docx_layout_raster_pages']} raster pages, min title margin {metrics['key_figure_docx_layout_min_title_margin']} pt, min page ink {metrics['key_figure_docx_layout_min_page_ink']}%, max near-edge ink {metrics['key_figure_docx_layout_max_near_edge_ink']}%, min luminance std {metrics['key_figure_docx_layout_min_luminance_std']} |",
            f"| Signature ideas | {metrics['signature_idea_count']} |",
            f"| Voice-pass slots preserved as author-enrichment queue context | {metrics['voice_slot_count']} |",
            f"| Release-approved reader formats | {qmd_escape(', '.join(metrics['format_approved']))} |",
            f"| Reader formats still carrying blockers | {qmd_escape(', '.join(metrics['format_blocked']))} |",
            f"| Format blocker counts | {qmd_escape(counter_phrase(blocker_counts))} |",
            f"| Current curated candidate rows | {metrics['curated_candidate_count']} |",
            f"| Current curated candidate status | `{qmd_escape(metrics['curated_candidate_status'])}` |",
            f"| Current curated candidate blocker counts | {qmd_escape(counter_phrase(metrics['curated_candidate_blocker_counts']))} |",
            f"| Blocked curated reader candidate record | {metrics['curated_blocked_record_status']} |",
            f"| Blocked curated format-probe closure | {metrics['curated_blocked_probe_status']} |",
            f"| EPUB Apple Books application review | `{metrics['epub_app_review_status']}`; {metrics['epub_app_review_observations']} observations, {metrics['epub_app_review_cleared_blockers']} blocker cleared, digest `{metrics['epub_app_review_sha']}` |",
            f"| DOCX application-evidence decision | `{metrics['docx_application_decision_status']}`; {metrics['docx_application_decision_cleared_blockers']} blocker cleared, {metrics['docx_application_decision_preserved_blockers']} blockers preserved |",
            f"| Curated PDF page-by-page review | `{metrics['curated_pdf_page_review_status']}`; {metrics['curated_pdf_page_review_rows']} rows, {metrics['curated_pdf_page_review_failed_pages']} failed, {metrics['curated_pdf_page_review_blank_pages']} blank, {metrics['curated_pdf_page_review_near_edge_pages']} near-edge, {metrics['curated_pdf_page_review_out_of_bounds_pages']} out-of-bounds word-box pages, {metrics['curated_pdf_page_review_low_ink_pages']} accepted low-ink page |",
            f"| Final figure-artifact review | `{metrics['final_figure_review_status']}`; {metrics['final_figure_review_figures']} figures, {metrics['final_figure_review_cleared_blockers']} blocker cleared |",
            f"| Audio narration treatment review | `{metrics['audio_narration_treatment_status']}`; {metrics['audio_narration_treatment_cleared_blockers']} blocker cleared, {metrics['audio_narration_treatment_preserved_blockers']} blockers preserved |",
            f"| Audio metadata review | `{metrics['audio_metadata_status']}`; {metrics['audio_metadata_cleared_blockers']} blocker cleared, {metrics['audio_metadata_preserved_blockers']} blockers preserved; `{qmd_escape(metrics['audio_metadata_title'])}` {qmd_escape(metrics['audio_metadata_version'])}, `{qmd_escape(metrics['audio_metadata_language'])}` |",
            f"| Human-consumption pre-release gate | `{metrics['human_consumption_gate_status']}` |",
            f"| Human-consumption gate statuses | {qmd_escape(counter_phrase(Counter(metrics['human_consumption_gate_statuses'].values())))} |",
            f"| Human-consumption ebook checks | {metrics['human_consumption_epub_pairs']} EPUB key-figure pairs, {metrics['human_consumption_epub_failures']} failures, {metrics['human_consumption_pdf_caption_pages']} PDF caption pages, {metrics['human_consumption_docx_title_pages']} DOCX title pages |",
            f"| Human-consumption readability checks | {metrics['human_consumption_readability_chapters']} chapters, {metrics['human_consumption_readability_min_words']} to {metrics['human_consumption_readability_max_words']} words, max paragraph {metrics['human_consumption_readability_max_paragraph_words']} words, {metrics['human_consumption_live_marker_hits']} live-marker hits |",
            f"| Human-consumption companion checks | {metrics['human_consumption_companion_routes']} routes, {metrics['human_consumption_companion_existing']} existing notes, {metrics['human_consumption_companion_summaries']} figure spoken summaries |",
            "",
            "## Status-Page Row",
            "",
            compact_status_row(metrics),
            "",
            "## Reader Manuscript And Chapter Review",
            "",
            f"- `editions/release_profiles.json` keeps the live, research, reader, and audio profiles present: {', '.join(metrics['profile_ids'])}.",
            f"- `editions/reader_manuscript/v1_0/manifest.json` remains `{metrics['reader_manifest_status']}` with {metrics['curated_record_count']} curated chapter records, {reconciliation_counts.get('reconciled', 0)} reconciled records, and {metrics['missing_curated_files']} missing curated chapter files.",
            f"- `docs/reader_chapter_reconciliation_approval.md` records `{metrics['chapter_reconciliation_approval_status']}` for {metrics['chapter_reconciliation_approval_rows']} curated chapter rows and clears only `curated_reconciliation_not_approved`; format artifact review, reader release approval, application/accessibility review, and audio gates remain active.",
            f"- The reader handoff contract carries {metrics['part_arc_count']} part arcs, {metrics['signature_idea_count']} signature ideas, {metrics['key_figure_target_count']} key-figure targets, and {metrics['voice_slot_count']} voice-pass slots without release approval.",
            f"- `editions/reader_manuscript/v1_0/chapter_review_matrix.json` records {metrics['chapter_review_count']} reviewed rows, {disposition_counts.get('reader_overlay_active', 0)} active-overlay chapters, {metrics['overlay_operation_count']} active overlay operations, {disposition_counts.get('no_immediate_action', 0)} no-immediate-action decisions, {disposition_counts.get('companion_note_candidate', 0)} companion-note candidates, and {disposition_counts.get('curated_manuscript_candidate', 0)} curated-manuscript candidates.",
            "- Chapter-level release blockers remain active until future final reader-manuscript packaging, format review, and an edition release record explicitly clear them.",
            "",
            "## Format And Artifact Review",
            "",
            f"- Generated reader HTML is the only release-approved reader format row, backed by `{metrics['release_record']}`. That approval does not extend to current curated reader HTML, EPUB, DOCX, PDF, e-reader, or audio.",
            f"- `docs/reader_format_review_matrix.md` distinguishes the historical generated-reader format queue from the current curated-reader candidate queue: {metrics['curated_candidate_count']} current candidate rows remain `{metrics['curated_candidate_status']}` with blocker counts {counter_phrase(metrics['curated_candidate_blocker_counts'])}.",
            f"- `{metrics['curated_blocked_record']}` records the current curated-reader HTML/EPUB/DOCX/PDF/e-reader/audio candidate as `partial` and blocked. It names exact local artifacts and blockers but does not approve, publish, tag, or archive any curated-reader artifact.",
            f"- The blocked candidate also records `{metrics['curated_blocked_probe_status']}` for the automated package, link, raster, key-figure, browser, Apple Books application probe, DOCX application-evidence decision, keyboard-only evidence decision, automated WCAG-preparation gate, script-level audio narration treatment review, and audio metadata review; this is release-preparation evidence only and does not clear screen-reader review, assistive-technology review, third-party/legal WCAG certification, audio artifact generation, pronunciation/listening review, chapter-marker timecoding, audio publication-rights approval, audio release approval, or reader release approval.",
            f"- `docs/reader_html_artifact_browser_review.md` records {metrics['generated_html_pages']} generated reader HTML pages, {metrics['generated_html_pairs']} page-view pairs, and {metrics['generated_html_failures']} failed page-view pairs.",
            f"- `docs/curated_reader_html_artifact_browser_review.md` records {metrics['curated_html_pages']} curated reader HTML pages, {metrics['curated_html_pairs']} page-view pairs, {metrics['curated_html_failures']} failed page-view pairs, {metrics['curated_key_figure_pairs']} key-figure page-view pairs, {metrics['curated_key_figure_failures']} key-figure failures, and ignored snapshot digest `{metrics['curated_html_digest']}`.",
            f"- `docs/curated_reader_format_artifact_probe.md` records the tracked curated-reader structural probe: {metrics['curated_html_files']} HTML files, {metrics['curated_epub_xhtml']} EPUB XHTML entries, {metrics['curated_docx_png']} DOCX PNG media entries, {metrics['curated_docx_svg']} DOCX SVG media entries, and {metrics['curated_pdf_pages']} PDF pages. Its repaired-package EPUB audit checks {metrics['curated_epub_audit_xhtml']} XHTML entries, {metrics['curated_epub_audit_content_xhtml']} packaged content XHTML entries, and {metrics['curated_epub_audit_unresolved']} unresolved internal hrefs, with repaired artifact SHA `{metrics['curated_epub_audit_sha']}`. Its Chromium EPUB XHTML browser review checks {metrics['curated_epub_browser_pairs']} page-view pairs with {metrics['curated_epub_browser_failures']} failures and {metrics['curated_epub_browser_max_overflow']} px maximum overflow. Its repaired-package DOCX audit checks {metrics['curated_docx_audit_paragraphs']} paragraphs, {metrics['curated_docx_audit_relationships']} relationships, and {metrics['curated_docx_audit_raw_qmd']} raw .qmd relationship targets, with repaired artifact SHA `{metrics['curated_docx_audit_sha']}`. Its LibreOffice headless DOCX review checks {metrics['curated_docx_libreoffice_pages']} converted pages, {metrics['curated_docx_libreoffice_text_chars']:,} text characters, {metrics['curated_docx_libreoffice_blank_pages']} blank converted-page rasters, {metrics['curated_docx_libreoffice_low_ink_pages']} low-ink converted-page rasters, and {metrics['curated_docx_libreoffice_near_edge_pages']} near-edge converted-page rasters. Its all-page PDF raster audit checks {metrics['curated_pdf_raster_pages']} pages, {metrics['curated_pdf_raster_blank_pages']} blank pages, {metrics['curated_pdf_raster_low_ink_pages']} low-ink pages, and {metrics['curated_pdf_raster_near_edge_pages']} near-edge pages. Its PDF extracted-text reading-flow review checks {metrics['curated_pdf_reading_flow_text_pages']} text pages, {metrics['curated_pdf_reading_flow_nonempty_pages']} nonempty text pages, {metrics['curated_pdf_reading_flow_chapters']} chapter headings, {metrics['curated_pdf_reading_flow_appendices']} appendix headings, and {metrics['curated_pdf_reading_flow_replacement_chars']} replacement characters. Its Chromium PDF viewer smoke review records {metrics['curated_pdf_viewer_screenshots']} viewer screenshots and {metrics['curated_pdf_viewer_scroll_changed_pixels']}% changed pixels after scroll. It preserves release blockers.",
            f"- `docs/reader_epub_apple_books_review.md` records `{metrics['epub_app_review_status']}` for repaired EPUB digest `{metrics['epub_app_review_sha']}`: Apple Books rendered the Reader Edition Baseline page and chapter 1 without the earlier XML error banner, exposed the ASI Stack control-plane figure and descriptive alt text, opened the table of contents, and clears only `app_or_ereader_review_not_completed`. It does not approve EPUB publication or the curated reader edition.",
            f"- `docs/reader_docx_application_decision.md` records `{metrics['docx_application_decision_status']}` and clears only `docx_application_review_not_completed`; {metrics['docx_application_decision_preserved_blockers']} blockers remain preserved, including reader release approval, manual keyboard-only review, screen-reader review, WCAG conformance, and audio gates. It does not claim Word, LibreOffice GUI, or Google Docs approval and does not approve DOCX publication.",
            f"- `docs/curated_reader_pdf_page_review.md` records a local page-by-page PDF release-preparation review: {metrics['curated_pdf_page_review_rows']} page rows, {metrics['curated_pdf_page_review_failed_pages']} failed pages, {metrics['curated_pdf_page_review_blank_pages']} blank pages, {metrics['curated_pdf_page_review_near_edge_pages']} near-edge pages, {metrics['curated_pdf_page_review_out_of_bounds_pages']} out-of-bounds word-box pages, and {metrics['curated_pdf_page_review_low_ink_pages']} accepted low-ink page. It clears only the current candidate's `manual_pdf_page_by_page_review_not_completed` blocker and does not approve the PDF artifact or reader release.",
            f"- `docs/reader_final_figure_artifact_review.md` records the aggregate final figure-artifact release-preparation review as `{metrics['final_figure_review_status']}` for {metrics['final_figure_review_figures']} key figures and clears only `final_figure_artifact_review_not_completed`. It does not approve the curated reader edition, e-reader/application review, accessibility compliance, audio, or release.",
            f"- `docs/reader_epub_probe_manifest.md` records the generated reader EPUB probe: {metrics['reader_epub_bytes']:,} bytes and `{metrics['reader_epub_language']}` language metadata, with the e-reader/application blocker still active.",
            f"- `docs/reader_docx_probe_manifest.md` records the generated reader DOCX conversion probe: {metrics['reader_docx_pages']} pages and {metrics['reader_docx_bytes']:,} bytes, with full-format review still active.",
            f"- `docs/reader_pdf_probe_manifest.md` records the generated reader PDF probe: {metrics['reader_pdf_pages']} pages and {metrics['reader_pdf_bytes']:,} bytes, with full PDF layout review still active.",
            f"- `docs/reader_audio_script_probe_manifest.md` records {metrics['audio_script_files']} audio-script workspace files, a reading-flow review with {metrics['audio_reading_flow_markers']} ordered chapter-marker rows, {metrics['audio_reading_flow_tbd_rows']} untimecoded marker rows, {metrics['audio_reading_flow_narration_notes']} narration notes, and {metrics['audio_reading_flow_text_chars']:,} text characters, plus {metrics['audio_key_figure_count']} draft key-figure spoken summaries routed into the generated audio companion workspace; target artifact states remain {qmd_escape(', '.join(f'{key}: {value}' for key, value in sorted(audio_targets.items())))}.",
            f"- `docs/reader_audio_narration_treatment_review.md` records `{metrics['audio_narration_treatment_status']}` and clears only `narration_quality_review_not_completed`; {metrics['audio_narration_treatment_preserved_blockers']} audio blockers were preserved at that review step, including audio files, chapter-marker timecoding, metadata, spot check, audio-embedded EPUB packaging, and audio edition release record.",
            f"- `docs/reader_audio_metadata_review.md` records `{metrics['audio_metadata_status']}` and clears only `audio_metadata_not_reviewed`; {metrics['audio_metadata_preserved_blockers']} audio blockers remain preserved, including reviewed-reader release record, audio files, listening spot check, chapter-marker timecoding, audio-embedded EPUB packaging, and audio edition release record. It does not approve a narrator, synthesis tool, audio publication rights, MP3, M4B, audio-embedded EPUB, or audio release.",
            f"- `docs/reader_human_consumption_gate_review.md` records the current pre-release human-consumption gate as `{metrics['human_consumption_gate_status']}`: ebook layout, diagram/image readiness, bedtime readability, and companion-note routing are `pass_pre_release_review`; the separate final figure-artifact review, Apple Books EPUB application review, DOCX application-evidence decision, script-level audio narration treatment review, and audio metadata review are passed, while accessibility, audio artifact, and release-approval blockers remain active.",
            f"- `docs/reader_key_figure_artifact_review.md` keeps the ten key figures as draft reader aids, not final figure-artifact approval; `docs/reader_key_figure_format_probe.md` records package/text survival with {metrics['key_figure_epub_svg_entries']} EPUB SVG entries, {metrics['key_figure_epub_matched_titles']} matched EPUB SVG titles, {metrics['key_figure_docx_matched_stems']} DOCX figure stems, and {metrics['key_figure_pdf_matched_captions']} PDF draft-caption matches while preserving final-art, e-reader, application, PDF-layout, and release blockers.",
            f"- `docs/reader_key_figure_geometry_review.md` records a source-geometry review for {metrics['key_figure_geometry_count']} key figures: {metrics['key_figure_geometry_content_bounds']} content-bound checks, {metrics['key_figure_geometry_text_anchor_bounds']} text-anchor checks, and {metrics['key_figure_geometry_min_edge_margin']} px minimum content edge margin; it is not raster review, final figure-artifact approval, or reader release approval.",
            f"- `docs/reader_visual_identity_review.md` records a source-level visual identity review: {metrics['visual_identity_figure_count']} key figures, {metrics['visual_identity_color_count']} combined colors, {metrics['visual_identity_non_neutral_families']} non-neutral color families, and minimum text contrast {metrics['visual_identity_min_text_contrast']}; it is not manual aesthetic review, final figure-artifact approval, or reader release approval.",
            f"- `docs/reader_accessibility_navigation_review.md` records a source-level accessibility/navigation review: {metrics['reader_accessibility_navigation_chapters']} curated chapters, {metrics['reader_accessibility_navigation_h1']} one-H1 chapters, {metrics['reader_accessibility_navigation_handoffs']} handoff sections, {metrics['reader_accessibility_navigation_fig_alts']} draft figure alt texts, {metrics['reader_accessibility_navigation_boundaries']} figure boundary paragraphs, {metrics['reader_accessibility_navigation_live_marker_leaks']} live-marker leaks, and {metrics['reader_accessibility_navigation_raw_claim_leaks']} raw core-claim marker leaks; it is not keyboard-only review, screen-reader review, WCAG conformance, e-reader review, audiobook review, or reader release approval.",
            f"- `docs/reader_keyboard_navigation_review.md` records an automated Chromium keyboard traversal review over the ignored local curated-reader HTML artifact: {metrics['reader_keyboard_navigation_pages']} pages, {metrics['reader_keyboard_navigation_pairs']} desktop/mobile page-view pairs, {metrics['reader_keyboard_navigation_failures']} failed pairs, {metrics['reader_keyboard_navigation_skip_reached']} skip-link reach observations, {metrics['reader_keyboard_navigation_skip_activated']} skip-link activations, {metrics['reader_keyboard_navigation_main_route']} main-content routes, {metrics['reader_keyboard_navigation_nav_reached']} navigation reach observations, {metrics['reader_keyboard_navigation_search_reached']} search reach observations, and {metrics['reader_keyboard_navigation_traps']} keyboard-trap candidates; it is not manual keyboard-only review, screen-reader review, WCAG conformance, e-reader review, audiobook review, or reader release approval.",
            f"- `docs/reader_keyboard_only_decision.md` records `{metrics['reader_keyboard_only_decision_status']}` for the current curated-reader HTML candidate and clears only `manual_keyboard_only_review_not_completed`; {metrics['reader_keyboard_only_decision_preserved']} blockers remain preserved, including screen-reader review, WCAG conformance, reader release approval, and audio gates. It does not publish or approve curated reader HTML and does not promote any chapter core claim.",
            f"- `docs/reader_accessibility_tree_review.md` records an automated Chromium accessibility-tree release-preparation probe over the ignored local curated-reader HTML artifact: {metrics['reader_accessibility_tree_pages']} pages, {metrics['reader_accessibility_tree_pairs']} desktop/mobile page-view pairs, {metrics['reader_accessibility_tree_failures']} failed pairs, {metrics['reader_accessibility_tree_ax_pairs']} accessibility-tree pairs, {metrics['reader_accessibility_tree_unnamed']} unnamed interactive elements, {metrics['reader_accessibility_tree_image_alt_failures']} image alt failures, {metrics['reader_accessibility_tree_table_header_failures']} table-header failures, and {metrics['reader_accessibility_tree_duplicate_ids']} duplicate-ID hits; it is not manual keyboard-only review, screen-reader review, WCAG conformance, e-reader review, audiobook review, or reader release approval.",
            f"- `docs/reader_wcag_preparation_review.md` records `{metrics['reader_wcag_preparation_status']}` for the current curated-reader HTML candidate: {metrics['reader_wcag_preparation_pairs']} desktop/mobile page-view pairs, {metrics['reader_wcag_preparation_contrast_samples']} visible text contrast samples, {metrics['reader_wcag_preparation_contrast_failures']} contrast failures, and {metrics['reader_wcag_preparation_min_contrast']} minimum contrast ratio. It clears only `wcag_conformance_review_not_completed`; it is not screen-reader review, assistive-technology review, third-party/legal WCAG certification, reader release approval, or a support-state promotion.",
            f"- `docs/reader_key_figure_raster_review.md` records an automated PNG raster artifact review: {metrics['key_figure_raster_count']} generated fallbacks, {metrics['key_figure_raster_standard_dimensions']} standard 1200 x 760 canvases, {metrics['key_figure_raster_min_opaque_percent']}% minimum opaque pixel coverage, {metrics['key_figure_raster_min_luminance_std']} minimum luminance standard deviation, and {metrics['key_figure_raster_min_colors']} minimum quantized colors; it is not manual aesthetic review, e-reader visual review, DOCX/PDF application review, final figure-artifact approval, or reader release approval.",
            f"- `docs/reader_key_figure_epub_layout_review.md` records a local EPUB key-figure XHTML layout probe: {metrics['key_figure_epub_layout_entries']} XHTML entries, {metrics['key_figure_epub_layout_pairs']} desktop/e-reader-like browser page-view pairs, {metrics['key_figure_epub_layout_failures']} failed pairs, {metrics['key_figure_epub_layout_min_body_chars']} minimum body text characters, {metrics['key_figure_epub_layout_min_alt_words']} minimum alt-text words, {metrics['key_figure_epub_layout_max_overflow']} px maximum horizontal overflow, and {metrics['key_figure_epub_layout_image_failures']} image failures; it is not dedicated e-reader device review, e-reader application approval, final figure-artifact approval, or reader release approval.",
            f"- `docs/reader_key_figure_pdf_layout_review.md` records a local PDF key-figure caption-page layout probe: {metrics['key_figure_pdf_layout_caption_pages']} caption pages in a {metrics['key_figure_pdf_layout_pages']}-page PDF, {metrics['key_figure_pdf_layout_raster_pages']} raster pages, {metrics['key_figure_pdf_layout_min_caption_margin']} pt minimum caption margin, {metrics['key_figure_pdf_layout_min_page_ink']}% minimum page ink, {metrics['key_figure_pdf_layout_max_near_edge_ink']}% maximum near-edge ink, and {metrics['key_figure_pdf_layout_min_luminance_std']} minimum luminance standard deviation; it is not manual page-by-page PDF review, final figure-artifact approval, or reader release approval.",
            f"- `docs/reader_key_figure_docx_layout_review.md` records a local DOCX-to-PDF key-figure title-page layout probe: {metrics['key_figure_docx_layout_title_pages']} title pages in a {metrics['key_figure_docx_layout_pages']}-page LibreOffice-converted PDF, {metrics['key_figure_docx_layout_raster_pages']} raster pages, {metrics['key_figure_docx_layout_min_title_margin']} pt minimum title margin, {metrics['key_figure_docx_layout_min_page_ink']}% minimum page ink, {metrics['key_figure_docx_layout_max_near_edge_ink']}% maximum near-edge ink, and {metrics['key_figure_docx_layout_min_luminance_std']} minimum luminance standard deviation; it is not Word review, LibreOffice GUI review, Google Docs review, manual document review, final figure-artifact approval, or reader release approval.",
            "",
            "## Non-Claim Boundary",
            "",
            "- This ledger does not publish a new reader, research, ebook, document, PDF, e-reader, audio, or audio-embedded EPUB artifact.",
            "- This ledger does not approve curated reader HTML, EPUB, DOCX, PDF, e-reader, audio, or the curated reader edition.",
            "- This ledger does not promote any Appendix C support state or chapter core claim.",
            "- Future release approval must name the exact reviewed artifact in an edition release record and update the relevant format row.",
            "",
            "## Validation Errors",
            "",
            *validation_lines,
            "",
        ]
    )


def write_status_row(row: str) -> None:
    lines = STATUS.read_text(encoding="utf-8").splitlines()
    matches = [index for index, line in enumerate(lines) if line.startswith("| Release surfaces |")]
    if len(matches) != 1:
        fail([f"{rel(STATUS)} must contain exactly one Release surfaces row; found {len(matches)}."])
    lines[matches[0]] = row
    STATUS.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="rewrite the tracked ledger")
    parser.add_argument("--write-status-row", action="store_true", help="rewrite the compact Release surfaces row in docs/v1_0_candidate_status.md")
    args = parser.parse_args()

    metrics, errors = collect_metrics()
    if not metrics:
        fail(errors)
    report = build_report(metrics, errors)

    row = compact_status_row(metrics)

    if args.write:
        LEDGER.write_text(report, encoding="utf-8")
        if errors:
            fail(errors)
        print(f"Wrote {rel(LEDGER)}")

    if args.write_status_row:
        if errors:
            fail(errors)
        write_status_row(row)
        print(f"Wrote compact Release surfaces row in {rel(STATUS)}")

    if args.write or args.write_status_row:
        return

    if errors:
        fail(errors)
    if not LEDGER.exists():
        fail([f"{rel(LEDGER)} is missing; run with --write."])
    current = LEDGER.read_text(encoding="utf-8")
    if current.rstrip() != report.rstrip():
        fail([f"{rel(LEDGER)} is stale; run `python3 scripts/validate_release_surface_status_ledger.py --write`."])

    status_text = STATUS.read_text(encoding="utf-8")
    if row not in status_text:
        fail(["docs/v1_0_candidate_status.md is missing the compact release-surface status row."])

    print(
        "Release surface status ledger validation passed: "
        f"{metrics['curated_record_count']} curated records, "
        f"{metrics['overlay_operation_count']} overlay operations, "
        f"{', '.join(metrics['format_approved'])} approved format row."
    )


if __name__ == "__main__":
    main()
