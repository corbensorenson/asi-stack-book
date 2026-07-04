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
FORMAT_REVIEW_MATRIX = ROOT / "editions" / "reader_manuscript" / "v1_0" / "format_review_matrix.json"
ARTIFACT_INSPECTION = ROOT / "editions" / "reader_manuscript" / "v1_0" / "artifact_inspection_manifest.json"
CURATED_FORMAT_PROBE = ROOT / "editions" / "reader_manuscript" / "v1_0" / "curated_format_probe_manifest.json"
EPUB_PROBE = ROOT / "editions" / "reader_manuscript" / "v1_0" / "epub_probe_manifest.json"
DOCX_PROBE = ROOT / "editions" / "reader_manuscript" / "v1_0" / "docx_probe_manifest.json"
PDF_PROBE = ROOT / "editions" / "reader_manuscript" / "v1_0" / "pdf_probe_manifest.json"
AUDIO_PROBE = ROOT / "editions" / "reader_manuscript" / "v1_0" / "audio_script_probe_manifest.json"
HTML_RELEASE_RECORD = ROOT / "release_records" / "2026-06-29-v1-reader-html-855dc277.json"

REVIEW_DOCS = {
    "reader_html": ROOT / "docs" / "reader_html_artifact_browser_review.md",
    "curated_html": ROOT / "docs" / "curated_reader_html_artifact_browser_review.md",
    "curated_format": ROOT / "docs" / "curated_reader_format_artifact_probe.md",
    "reader_epub": ROOT / "docs" / "reader_epub_probe_manifest.md",
    "reader_docx": ROOT / "docs" / "reader_docx_probe_manifest.md",
    "reader_pdf": ROOT / "docs" / "reader_pdf_probe_manifest.md",
    "reader_audio": ROOT / "docs" / "reader_audio_script_probe_manifest.md",
    "reader_figures": ROOT / "docs" / "reader_key_figure_artifact_review.md",
    "reader_chapter_matrix": ROOT / "docs" / "reader_chapter_review_matrix.md",
    "reader_format_matrix": ROOT / "docs" / "reader_format_review_matrix.md",
}

REQUIRED_PROFILE_IDS = {"live_book", "research_release", "reader_release", "audio_release"}
REQUIRED_CURATED_BLOCKERS = {
    "curated_reconciliation_not_approved",
    "format_artifact_not_reviewed",
    "reader_release_record_not_created",
}
REQUIRED_FORMAT_BLOCKERS = {
    "full_format_artifact_review_not_completed",
    "app_or_ereader_review_not_completed",
    "full_pdf_layout_review_not_completed",
}
REQUIRED_AUDIO_BLOCKERS = {
    "reviewed_reader_release_record_not_created_for_audio",
    "narration_script_not_reviewed",
    "audio_files_not_generated",
    "audio_spot_check_not_performed",
    "chapter_markers_not_timecoded",
    "audio_metadata_not_reviewed",
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
        FORMAT_REVIEW_MATRIX,
        ARTIFACT_INSPECTION,
        CURATED_FORMAT_PROBE,
        EPUB_PROBE,
        DOCX_PROBE,
        PDF_PROBE,
        AUDIO_PROBE,
        HTML_RELEASE_RECORD,
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
    format_matrix = load_json(FORMAT_REVIEW_MATRIX)
    artifact_inspection = load_json(ARTIFACT_INSPECTION)
    curated_format = load_json(CURATED_FORMAT_PROBE)
    epub_probe = load_json(EPUB_PROBE)
    docx_probe = load_json(DOCX_PROBE)
    pdf_probe = load_json(PDF_PROBE)
    audio_probe = load_json(AUDIO_PROBE)

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

    curated_inspection = curated_format.get("inspection_summary", {})
    reader_inspection = artifact_inspection.get("inspection_summary", {})
    epub_summary = epub_probe.get("epub_container_summary", {})
    docx_conversion = docx_probe.get("conversion_summary", {})
    pdf_info = pdf_probe.get("pdfinfo_summary", {})
    audio_workspace = audio_probe.get("script_workspace_summary", {})
    audio_targets = audio_probe.get("target_artifact_status", {})
    if set(audio_targets.values()) != {"target_not_generated"}:
        errors.append("audio target artifacts must remain target_not_generated until audio release artifacts exist.")
    missing_audio_blockers = sorted(REQUIRED_AUDIO_BLOCKERS - set(audio_probe.get("release_blockers_preserved", [])))
    if missing_audio_blockers:
        errors.append(f"audio probe missing blockers: {missing_audio_blockers}")

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
            "b75f54d27856b63e9e6bdea4f8a8d3e073c2c76ab700b3e6c1c51425d021a9eb",
            "newer local viability",
            "EPUB, DOCX, PDF, e-reader, MP3, M4B, and audio-embedded EPUB artifacts remain",
        ],
        "curated_format": [
            "This does not clear release blockers.",
            "EPUB still needs real e-reader or app",
            "PDF still needs page-layout and reading-flow review",
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
            "final figure-artifact approval, or evidence that audio files exist.",
            "This manifest does not approve EPUB, DOCX, PDF, HTML, e-reader, document, audio, MP3, M4B, or audio-embedded EPUB artifacts",
        ],
        "reader_figures": [
            "not a release approval and not final figure-artifact review",
            "does not approve final figure art, EPUB, DOCX, PDF, e-reader",
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

    metrics: dict[str, Any] = {
        "profile_count": len(profile_ids),
        "profile_ids": sorted(profile_ids),
        "reader_manifest_status": reader_manifest.get("status"),
        "curated_record_count": len(chapter_records),
        "curated_reconciliation_counts": reconciliation_counts,
        "missing_curated_files": len(missing_curated_files),
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
        "generated_html_pages": generated_html_pages,
        "generated_html_pairs": generated_html_pairs,
        "generated_html_failures": generated_html_failures,
        "curated_html_pages": curated_html_pages,
        "curated_html_pairs": curated_html_pairs,
        "curated_html_failures": curated_html_failures,
        "curated_key_figure_pairs": curated_key_figure_pairs,
        "curated_key_figure_failures": curated_key_figure_failures,
        "curated_html_digest": "b75f54d27856b63e9e6bdea4f8a8d3e073c2c76ab700b3e6c1c51425d021a9eb",
        "curated_html_files": curated_inspection.get("html", {}).get("html_files"),
        "curated_epub_xhtml": curated_inspection.get("epub", {}).get("xhtml_entries"),
        "curated_docx_png": curated_inspection.get("docx", {}).get("png_media_entries"),
        "curated_docx_svg": curated_inspection.get("docx", {}).get("svg_media_entries"),
        "curated_pdf_pages": curated_inspection.get("pdf", {}).get("pages"),
        "reader_html_files": reader_inspection.get("html", {}).get("html_files"),
        "reader_epub_bytes": epub_summary.get("file_size_bytes"),
        "reader_epub_language": epub_probe.get("metadata_summary", {}).get("language"),
        "reader_docx_pages": docx_conversion.get("pages"),
        "reader_docx_bytes": docx_conversion.get("file_size_bytes"),
        "reader_pdf_pages": pdf_info.get("pages"),
        "reader_pdf_bytes": pdf_info.get("file_size_bytes"),
        "audio_script_files": audio_workspace.get("script_files"),
        "audio_targets": audio_targets,
        "release_record": rel(HTML_RELEASE_RECORD),
    }
    return metrics, errors


def compact_status_row(metrics: dict[str, Any] | None = None) -> str:
    if metrics is None:
        metrics, errors = collect_metrics()
        if errors:
            fail(errors)
    reconciliation_counts: Counter[str] = metrics["curated_reconciliation_counts"]
    disposition_counts: Counter[str] = metrics["disposition_counts"]
    return (
        "| Release surfaces | Live, research, reader, and audio profiles exist. "
        "Detailed release-surface state is generated in `docs/release_surface_status_ledger.md`: "
        "generated-reader HTML remains the only release-approved reader artifact; "
        f"the tracked curated reader manuscript is `{metrics['reader_manifest_status']}` with "
        f"{metrics['curated_record_count']} records "
        f"({reconciliation_counts.get('drafting', 0)} drafting, {reconciliation_counts.get('reconciled', 0)} reconciled) "
        "and no release approval; "
        f"the synced chapter review matrix records {metrics['chapter_review_count']} reviewed rows, "
        f"{disposition_counts.get('reader_overlay_active', 0)} active-overlay chapters, "
        f"{metrics['overlay_operation_count']} overlay operations, "
        f"{disposition_counts.get('companion_note_candidate', 0)} companion-note candidates, and "
        f"{disposition_counts.get('curated_manuscript_candidate', 0)} curated-manuscript candidates; "
        "current curated HTML/EPUB/DOCX/PDF and reader EPUB/DOCX/PDF/audio records are probe evidence only, "
        "with EPUB, DOCX, PDF, e-reader, audio, refreshed reader HTML, and final figure-artifact review still unapproved. | "
        "`docs/release_surface_status_ledger.md`; `editions/release_profiles.json`; "
        "`editions/reader_overlays/v1_0/manifest.json`; `editions/reader_manuscript/v1_0/manifest.json`; "
        "`editions/reader_manuscript/v1_0/chapter_review_matrix.json`; "
        "`editions/reader_manuscript/v1_0/format_review_matrix.json`; "
        "`docs/reader_chapter_review_matrix.md`; `docs/reader_format_review_matrix.md`; "
        "`docs/reader_html_artifact_browser_review.md`; `docs/curated_reader_html_artifact_browser_review.md`; "
        "`docs/curated_reader_format_artifact_probe.md`; `docs/reader_epub_probe_manifest.md`; "
        "`docs/reader_docx_probe_manifest.md`; `docs/reader_pdf_probe_manifest.md`; "
        "`docs/reader_audio_script_probe_manifest.md`; `release_records/2026-06-29-v1-reader-html-855dc277.json`; "
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
            "It records release-profile, reader-manuscript, format-probe, and artifact-review state only; it does not create release approval, final figure approval, audiobook approval, e-reader approval, or claim-support movement.",
            "",
            "## Summary",
            "",
            "| Metric | Value |",
            "|---|---:|",
            f"| Release profiles present | {metrics['profile_count']} |",
            f"| Curated reader chapter records | {metrics['curated_record_count']} |",
            f"| Curated reconciliation states | {qmd_escape(counter_phrase(reconciliation_counts))} |",
            f"| Missing curated chapter files | {metrics['missing_curated_files']} |",
            f"| Reader review rows | {metrics['chapter_review_count']} |",
            f"| Reader review states | {qmd_escape(counter_phrase(review_counts))} |",
            f"| Active-overlay chapters | {disposition_counts.get('reader_overlay_active', 0)} |",
            f"| Active overlay operations | {metrics['overlay_operation_count']} |",
            f"| No-immediate-action decisions | {disposition_counts.get('no_immediate_action', 0)} |",
            f"| Companion-note candidates | {disposition_counts.get('companion_note_candidate', 0)} |",
            f"| Curated-manuscript candidates | {disposition_counts.get('curated_manuscript_candidate', 0)} |",
            f"| Key-figure targets | {metrics['key_figure_target_count']} |",
            f"| Signature ideas | {metrics['signature_idea_count']} |",
            f"| Voice-pass slots preserved as author-enrichment queue context | {metrics['voice_slot_count']} |",
            f"| Release-approved reader formats | {qmd_escape(', '.join(metrics['format_approved']))} |",
            f"| Reader formats still carrying blockers | {qmd_escape(', '.join(metrics['format_blocked']))} |",
            f"| Format blocker counts | {qmd_escape(counter_phrase(blocker_counts))} |",
            "",
            "## Status-Page Row",
            "",
            compact_status_row(metrics),
            "",
            "## Reader Manuscript And Chapter Review",
            "",
            f"- `editions/release_profiles.json` keeps the live, research, reader, and audio profiles present: {', '.join(metrics['profile_ids'])}.",
            f"- `editions/reader_manuscript/v1_0/manifest.json` remains `{metrics['reader_manifest_status']}` with {metrics['curated_record_count']} curated chapter records, {reconciliation_counts.get('reconciled', 0)} reconciled records, and {metrics['missing_curated_files']} missing curated chapter files.",
            f"- The reader handoff contract carries {metrics['part_arc_count']} part arcs, {metrics['signature_idea_count']} signature ideas, {metrics['key_figure_target_count']} key-figure targets, and {metrics['voice_slot_count']} voice-pass slots without release approval.",
            f"- `editions/reader_manuscript/v1_0/chapter_review_matrix.json` records {metrics['chapter_review_count']} reviewed rows, {disposition_counts.get('reader_overlay_active', 0)} active-overlay chapters, {metrics['overlay_operation_count']} active overlay operations, {disposition_counts.get('no_immediate_action', 0)} no-immediate-action decisions, {disposition_counts.get('companion_note_candidate', 0)} companion-note candidates, and {disposition_counts.get('curated_manuscript_candidate', 0)} curated-manuscript candidates.",
            "- Chapter-level release blockers remain active until future final reader-manuscript packaging, format review, and an edition release record explicitly clear them.",
            "",
            "## Format And Artifact Review",
            "",
            f"- Generated reader HTML is the only release-approved reader format row, backed by `{metrics['release_record']}`. That approval does not extend to current curated reader HTML, EPUB, DOCX, PDF, e-reader, audio, or figure-artifact review.",
            f"- `docs/reader_html_artifact_browser_review.md` records {metrics['generated_html_pages']} generated reader HTML pages, {metrics['generated_html_pairs']} page-view pairs, and {metrics['generated_html_failures']} failed page-view pairs.",
            f"- `docs/curated_reader_html_artifact_browser_review.md` records {metrics['curated_html_pages']} curated reader HTML pages, {metrics['curated_html_pairs']} page-view pairs, {metrics['curated_html_failures']} failed page-view pairs, {metrics['curated_key_figure_pairs']} key-figure page-view pairs, {metrics['curated_key_figure_failures']} key-figure failures, and ignored snapshot digest `{metrics['curated_html_digest']}`.",
            f"- `docs/curated_reader_format_artifact_probe.md` records the tracked curated-reader structural probe: {metrics['curated_html_files']} HTML files, {metrics['curated_epub_xhtml']} EPUB XHTML entries, {metrics['curated_docx_png']} DOCX PNG media entries, {metrics['curated_docx_svg']} DOCX SVG media entries, and {metrics['curated_pdf_pages']} PDF pages. It preserves release blockers.",
            f"- `docs/reader_epub_probe_manifest.md` records the generated reader EPUB probe: {metrics['reader_epub_bytes']:,} bytes and `{metrics['reader_epub_language']}` language metadata, with the e-reader/application blocker still active.",
            f"- `docs/reader_docx_probe_manifest.md` records the generated reader DOCX conversion probe: {metrics['reader_docx_pages']} pages and {metrics['reader_docx_bytes']:,} bytes, with full-format review still active.",
            f"- `docs/reader_pdf_probe_manifest.md` records the generated reader PDF probe: {metrics['reader_pdf_pages']} pages and {metrics['reader_pdf_bytes']:,} bytes, with full PDF layout review still active.",
            f"- `docs/reader_audio_script_probe_manifest.md` records {metrics['audio_script_files']} audio-script workspace files; target artifact states remain {qmd_escape(', '.join(f'{key}: {value}' for key, value in sorted(audio_targets.items())))}.",
            "- `docs/reader_key_figure_artifact_review.md` keeps the ten key figures as draft reader aids, not final figure-artifact approval.",
            "",
            "## Non-Claim Boundary",
            "",
            "- This ledger does not publish a new reader, research, ebook, document, PDF, e-reader, audio, or audio-embedded EPUB artifact.",
            "- This ledger does not approve curated reader HTML, EPUB, DOCX, PDF, e-reader, audio, or final figure artifacts.",
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
