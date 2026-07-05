#!/usr/bin/env python3
"""Validate the curated reader human-consumption pre-release gate.

This check rolls up existing reader-format, figure, readability, and
companion-note review evidence into one tracked gate record. It does not
approve any artifact for release.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
READER_MANIFEST = ROOT / "editions" / "reader_manuscript" / "v1_0" / "manifest.json"
COMPANION_ROUTING = ROOT / "editions" / "reader_manuscript" / "v1_0" / "companion_note_routing.json"
ACCESSIBILITY = ROOT / "editions" / "reader_manuscript" / "v1_0" / "accessibility_navigation_manifest.json"
VISUAL_IDENTITY = ROOT / "editions" / "reader_manuscript" / "v1_0" / "visual_identity_manifest.json"
GEOMETRY = ROOT / "editions" / "reader_manuscript" / "v1_0" / "key_figure_geometry_manifest.json"
RASTER = ROOT / "editions" / "reader_manuscript" / "v1_0" / "key_figure_raster_manifest.json"
EPUB_LAYOUT = ROOT / "editions" / "reader_manuscript" / "v1_0" / "key_figure_epub_layout_manifest.json"
PDF_LAYOUT = ROOT / "editions" / "reader_manuscript" / "v1_0" / "key_figure_pdf_layout_manifest.json"
DOCX_LAYOUT = ROOT / "editions" / "reader_manuscript" / "v1_0" / "key_figure_docx_layout_manifest.json"
AUDIO_PROBE = ROOT / "editions" / "reader_manuscript" / "v1_0" / "audio_script_probe_manifest.json"
FINAL_FIGURE_REVIEW = (
    ROOT / "editions" / "reader_manuscript" / "v1_0" / "final_figure_artifact_review_manifest.json"
)
RESULT = ROOT / "editions" / "reader_manuscript" / "v1_0" / "human_consumption_gate_manifest.json"
DOC = ROOT / "docs" / "reader_human_consumption_gate_review.md"
COMMAND = "python3 scripts/validate_reader_human_consumption_gate.py"
RESULT_ID = "reader-human-consumption-gate-2026-07-05"

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
    print("Reader human-consumption gate validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9][A-Za-z0-9'-]*", text)


def pass_status(gate: str, facts: dict[str, Any], limitations: list[str]) -> dict[str, Any]:
    return {
        "status": "pass_pre_release_review",
        "gate": gate,
        "facts": facts,
        "limitations": limitations,
    }


def inspect_readability(reader_manifest: dict[str, Any]) -> dict[str, Any]:
    records = reader_manifest.get("chapter_records", [])
    if not isinstance(records, list):
        fail(["reader manuscript chapter_records must be a list."])

    word_counts: list[int] = []
    paragraph_word_counts: list[int] = []
    chapter_rows: list[dict[str, Any]] = []
    live_marker_hits = 0
    raw_core_claim_hits = 0
    release_blocker_records = 0
    reconciled_records = 0

    for record in records:
        if not isinstance(record, dict):
            fail(["reader manuscript chapter_records entries must be objects."])
        chapter_id = str(record.get("chapter_id", ""))
        file_ref = str(record.get("file", ""))
        path = ROOT / file_ref
        if not path.exists():
            fail([f"{chapter_id}: curated reader chapter file is missing: {file_ref}"])
        text = path.read_text(encoding="utf-8")
        body = re.sub(r"^---.*?---\s*", "", text, flags=re.S)
        chapter_words = len(words(body))
        paragraphs = [item.strip() for item in re.split(r"\n\s*\n", body) if item.strip()]
        paragraph_counts = [len(words(item)) for item in paragraphs]
        max_paragraph_words = max(paragraph_counts) if paragraph_counts else 0
        word_counts.append(chapter_words)
        paragraph_word_counts.extend(paragraph_counts)
        live_hits = [marker for marker in LIVE_ONLY_MARKERS if marker in text]
        live_marker_hits += len(live_hits)
        raw_core_claim_hits += int(bool(RAW_CORE_CLAIM_RE.search(text)))
        blockers = set(record.get("release_blockers", []))
        if {"format_artifact_not_reviewed", "reader_release_record_not_created"}.issubset(blockers):
            release_blocker_records += 1
        if record.get("reconciliation_status") == "reconciled":
            reconciled_records += 1
        chapter_rows.append(
            {
                "chapter_id": chapter_id,
                "word_count": chapter_words,
                "paragraphs": len(paragraphs),
                "max_paragraph_words": max_paragraph_words,
                "paragraphs_over_180_words": sum(1 for value in paragraph_counts if value > 180),
            }
        )

    return {
        "chapter_records": len(records),
        "reconciled_records": reconciled_records,
        "release_blocker_preserved_records": release_blocker_records,
        "minimum_chapter_words": min(word_counts),
        "maximum_chapter_words": max(word_counts),
        "maximum_paragraph_words": max(paragraph_word_counts),
        "paragraphs_over_180_words": sum(1 for value in paragraph_word_counts if value > 180),
        "live_marker_hits": live_marker_hits,
        "raw_core_claim_marker_hits": raw_core_claim_hits,
        "sample_longest_chapters": sorted(chapter_rows, key=lambda row: row["word_count"], reverse=True)[:5],
        "sample_longest_paragraphs": sorted(chapter_rows, key=lambda row: row["max_paragraph_words"], reverse=True)[:5],
    }


def validate_observed(observed: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if observed.get("status") != "passed_human_consumption_pre_release_gate":
        errors.append("status must be passed_human_consumption_pre_release_gate.")
    gates = observed.get("gates", {})
    if not isinstance(gates, dict):
        return ["gates must be an object."]
    for gate_name in (
        "ebook_layout_review",
        "diagram_image_review",
        "bedtime_readability_review",
        "companion_notes_status",
    ):
        gate = gates.get(gate_name, {})
        if not isinstance(gate, dict):
            errors.append(f"{gate_name} must be an object.")
            continue
        if gate.get("status") != "pass_pre_release_review":
            errors.append(f"{gate_name}.status must be pass_pre_release_review.")

    ebook = gates.get("ebook_layout_review", {}).get("facts", {})
    expected_ebook = {
        "epub_key_figure_page_view_pairs": 20,
        "epub_key_figure_failed_pairs": 0,
        "epub_key_figure_max_overflow_px": 0,
        "pdf_key_figure_caption_pages": 10,
        "pdf_key_figure_max_near_edge_ink_percent": 0.0,
        "docx_key_figure_title_pages": 10,
        "docx_key_figure_max_near_edge_ink_percent": 0.0,
    }
    for key, expected in expected_ebook.items():
        if ebook.get(key) != expected:
            errors.append(f"ebook_layout_review.facts.{key} must be {expected!r}.")

    diagram = gates.get("diagram_image_review", {}).get("facts", {})
    expected_diagram = {
        "key_figures": 10,
        "geometry_content_bounds": 10,
        "geometry_text_anchor_bounds": 10,
        "raster_artifacts": 10,
        "raster_standard_dimensions": 10,
        "visual_identity_key_figures": 10,
        "non_neutral_color_families": 5,
        "accessibility_alt_texts": 10,
        "accessibility_figure_boundaries": 10,
    }
    for key, expected in expected_diagram.items():
        if diagram.get(key) != expected:
            errors.append(f"diagram_image_review.facts.{key} must be {expected!r}.")
    if diagram.get("raster_min_luminance_std", 0) < 20:
        errors.append("diagram_image_review.facts.raster_min_luminance_std must be at least 20.")
    if diagram.get("raster_min_quantized_colors", 0) < 100:
        errors.append("diagram_image_review.facts.raster_min_quantized_colors must be at least 100.")
    if diagram.get("visual_identity_min_text_contrast", 0) < 4.5:
        errors.append("diagram_image_review.facts.visual_identity_min_text_contrast must be at least 4.5.")

    bedtime = gates.get("bedtime_readability_review", {}).get("facts", {})
    expected_bedtime = {
        "chapter_records": 44,
        "reconciled_records": 44,
        "release_blocker_preserved_records": 44,
        "paragraphs_over_180_words": 0,
        "live_marker_hits": 0,
        "raw_core_claim_marker_hits": 0,
    }
    for key, expected in expected_bedtime.items():
        if bedtime.get(key) != expected:
            errors.append(f"bedtime_readability_review.facts.{key} must be {expected!r}.")
    if bedtime.get("maximum_paragraph_words", 999) > 160:
        errors.append("bedtime_readability_review.facts.maximum_paragraph_words must be <= 160.")
    if bedtime.get("minimum_chapter_words", 0) < 2000:
        errors.append("bedtime_readability_review.facts.minimum_chapter_words must be >= 2000.")
    if bedtime.get("maximum_chapter_words", 999999) > 6000:
        errors.append("bedtime_readability_review.facts.maximum_chapter_words must be <= 6000.")

    companion = gates.get("companion_notes_status", {}).get("facts", {})
    expected_companion = {
        "routing_records": 12,
        "routing_records_with_existing_notes": 12,
        "drafting_companion_notes": 12,
        "key_figure_companion_note_present": True,
        "key_figure_companion_figure_count": 10,
        "audio_probe_companion_summaries": 10,
    }
    for key, expected in expected_companion.items():
        if companion.get(key) != expected:
            errors.append(f"companion_notes_status.facts.{key} must be {expected!r}.")

    non_claims = " ".join(str(item).lower() for item in observed.get("non_claims", []))
    for phrase in (
        "does not approve",
        "does not approve, publish",
        "does not clear dedicated e-reader",
        "does not promote",
    ):
        if phrase not in non_claims:
            errors.append(f"non_claims missing phrase: {phrase}")
    return errors


def build_observed() -> dict[str, Any]:
    reader_manifest = load_json(READER_MANIFEST)
    companion_routing = load_json(COMPANION_ROUTING)
    accessibility = load_json(ACCESSIBILITY)
    visual_identity = load_json(VISUAL_IDENTITY)
    geometry = load_json(GEOMETRY)
    raster = load_json(RASTER)
    epub_layout = load_json(EPUB_LAYOUT)
    pdf_layout = load_json(PDF_LAYOUT)
    docx_layout = load_json(DOCX_LAYOUT)
    audio_probe = load_json(AUDIO_PROBE)
    final_figure = load_json(FINAL_FIGURE_REVIEW)

    companion_records = companion_routing.get("records", [])
    if not isinstance(companion_records, list):
        fail(["companion_note_routing.records must be a list."])
    existing_companion_notes = 0
    drafting_companion_notes = 0
    for record in companion_records:
        if not isinstance(record, dict):
            fail(["companion_note_routing.records entries must be objects."])
        note_file = record.get("companion_note_file")
        if isinstance(note_file, str) and (ROOT / note_file).exists():
            existing_companion_notes += 1
        if record.get("companion_note_status") == "drafting_not_release_reviewed":
            drafting_companion_notes += 1

    key_figure_companion = audio_probe.get("key_figure_companion_note", {})
    if not isinstance(key_figure_companion, dict):
        key_figure_companion = {}

    readability = inspect_readability(reader_manifest)
    epub_summary = epub_layout.get("summary", {})
    pdf_summary = pdf_layout.get("summary", {})
    docx_summary = docx_layout.get("summary", {})
    geometry_summary = geometry.get("summary", {})
    raster_summary = raster.get("summary", {})
    visual_palette = visual_identity.get("palette_summary", {})
    visual_contrast = visual_identity.get("contrast_summary", {})
    visual_figures = visual_identity.get("figure_source_summary", {})
    accessibility_summary = accessibility.get("summary", {})

    return {
        "schema_version": "asi_stack.reader_human_consumption_gate.v0",
        "result_id": RESULT_ID,
        "status": "passed_human_consumption_pre_release_gate",
        "command": COMMAND,
        "source_refs": [
            rel(READER_MANIFEST),
            rel(COMPANION_ROUTING),
            rel(ACCESSIBILITY),
            rel(VISUAL_IDENTITY),
            rel(GEOMETRY),
            rel(RASTER),
            rel(EPUB_LAYOUT),
            rel(PDF_LAYOUT),
            rel(DOCX_LAYOUT),
            rel(AUDIO_PROBE),
            rel(FINAL_FIGURE_REVIEW),
        ],
        "gates": {
            "ebook_layout_review": pass_status(
                "ebook_layout_review",
                {
                    "epub_key_figure_page_view_pairs": epub_summary.get("page_view_pairs"),
                    "epub_key_figure_failed_pairs": epub_summary.get("failed_page_view_pairs"),
                    "epub_key_figure_max_overflow_px": epub_summary.get("maximum_horizontal_overflow_px"),
                    "epub_key_figure_min_body_text_chars": epub_summary.get("minimum_body_text_chars"),
                    "epub_key_figure_image_failures": epub_summary.get("image_failure_count"),
                    "pdf_key_figure_caption_pages": pdf_summary.get("unique_caption_pages"),
                    "pdf_key_figure_min_caption_margin_pt": pdf_summary.get("minimum_caption_margin_pt"),
                    "pdf_key_figure_max_near_edge_ink_percent": pdf_summary.get("maximum_near_edge_ink_percent"),
                    "docx_key_figure_title_pages": docx_summary.get("unique_title_pages"),
                    "docx_key_figure_min_title_margin_pt": docx_summary.get("minimum_title_margin_pt"),
                    "docx_key_figure_max_near_edge_ink_percent": docx_summary.get("maximum_near_edge_ink_percent"),
                },
                [
                    "This is local layout preparation evidence, not e-reader, Word, PDF, or release approval.",
                    "It does not clear dedicated e-reader/application review, final figure-artifact approval, or reader release approval.",
                ],
            ),
            "diagram_image_review": pass_status(
                "diagram_image_review",
                {
                    "key_figures": visual_figures.get("figure_count"),
                    "geometry_content_bounds": geometry_summary.get("content_bounds_passed_count"),
                    "geometry_text_anchor_bounds": geometry_summary.get("text_anchor_bounds_passed_count"),
                    "geometry_min_edge_margin": geometry_summary.get("minimum_content_edge_margin_px"),
                    "raster_artifacts": raster_summary.get("raster_artifact_count"),
                    "raster_standard_dimensions": raster_summary.get("standard_dimension_count"),
                    "raster_min_luminance_std": raster_summary.get("minimum_luminance_std"),
                    "raster_min_quantized_colors": raster_summary.get("minimum_quantized_color_count"),
                    "visual_identity_key_figures": visual_figures.get("figure_count"),
                    "non_neutral_color_families": visual_palette.get("non_neutral_family_count"),
                    "visual_identity_min_text_contrast": visual_contrast.get("minimum_text_contrast_ratio"),
                    "accessibility_alt_texts": accessibility_summary.get("fig_alt_count"),
                    "accessibility_figure_boundaries": accessibility_summary.get("figure_boundary_count"),
                    "final_figure_review_status": final_figure.get("status"),
                    "final_figure_review_cleared_blockers": len(final_figure.get("cleared_blockers", [])),
                },
                [
                    "This is automated figure readiness evidence, not manual aesthetic review.",
                    "The separate final figure-artifact review clears the current final-figure blocker; this gate does not approve reader release.",
                ],
            ),
            "bedtime_readability_review": pass_status(
                "bedtime_readability_review",
                readability,
                [
                    "This checks source-level relaxed-reading shape only.",
                    "It does not replace human editorial judgment or reader release approval.",
                ],
            ),
            "companion_notes_status": pass_status(
                "companion_notes_status",
                {
                    "routing_records": len(companion_records),
                    "routing_records_with_existing_notes": existing_companion_notes,
                    "drafting_companion_notes": drafting_companion_notes,
                    "key_figure_companion_note_present": (ROOT / "editions/reader_manuscript/v1_0/companion_notes/key-figures.md").exists(),
                    "key_figure_companion_figure_count": key_figure_companion.get("figure_count"),
                    "audio_probe_companion_summaries": key_figure_companion.get("figure_count"),
                },
                [
                    "Companion notes remain drafting support, not released artifacts.",
                    "They do not move meaning-critical caveats out of the reader spine.",
                ],
            ),
        },
        "release_blockers_preserved": [
            "format_artifact_not_reviewed",
            "reader_release_record_not_created",
            "app_or_ereader_review_not_completed",
            "manual_keyboard_only_review_not_completed",
            "screen_reader_review_not_completed",
            "wcag_conformance_review_not_completed",
            "narration_quality_review_not_completed",
            "audio_files_not_generated",
        ],
        "non_claims": [
            "This gate does not approve, publish, tag, or archive any curated reader artifact.",
            "This gate does not clear dedicated e-reader review, e-reader application approval, Word review, LibreOffice GUI review, Google Docs review, manual keyboard-only review, screen-reader review, WCAG conformance review, narration quality review, audio generation, audiobook approval, or reader release approval.",
            "This gate does not promote any chapter core claim or claim support state.",
        ],
    }


def render_doc(observed: dict[str, Any]) -> str:
    gates = observed["gates"]
    ebook = gates["ebook_layout_review"]["facts"]
    diagram = gates["diagram_image_review"]["facts"]
    bedtime = gates["bedtime_readability_review"]["facts"]
    companion = gates["companion_notes_status"]["facts"]
    blockers = ", ".join(f"`{item}`" for item in observed["release_blockers_preserved"])
    return f"""# Reader Human-Consumption Gate Review

Generated by `{COMMAND} --write-result`.

This review rolls up the current curated reader manuscript's pre-release
human-consumption evidence. It records four gate reviews as passed for release
preparation only: ebook layout, diagram/image readiness, bedtime readability,
and companion-note routing.

It is not a reader release record, not e-reader approval, not DOCX/PDF
application approval, not audiobook approval, and not a support-state
transition.

## Summary

| Gate | Status | Key facts |
|---|---|---|
| Ebook layout | `{gates['ebook_layout_review']['status']}` | EPUB key figures: {ebook['epub_key_figure_page_view_pairs']} page-view pairs, {ebook['epub_key_figure_failed_pairs']} failed pairs, {ebook['epub_key_figure_max_overflow_px']} px max overflow; PDF key figures: {ebook['pdf_key_figure_caption_pages']} caption pages, {ebook['pdf_key_figure_max_near_edge_ink_percent']}% near-edge ink; DOCX key figures: {ebook['docx_key_figure_title_pages']} title pages, {ebook['docx_key_figure_max_near_edge_ink_percent']}% near-edge ink. |
| Diagram/image readiness | `{gates['diagram_image_review']['status']}` | {diagram['key_figures']} key figures, {diagram['geometry_content_bounds']} content-bound checks, {diagram['raster_artifacts']} raster fallbacks, {diagram['raster_min_luminance_std']} minimum luminance std, {diagram['raster_min_quantized_colors']} minimum quantized colors, {diagram['non_neutral_color_families']} non-neutral color families, {diagram['accessibility_alt_texts']} alt texts, final figure-artifact review `{diagram['final_figure_review_status']}`. |
| Bedtime readability | `{gates['bedtime_readability_review']['status']}` | {bedtime['chapter_records']} curated chapters, {bedtime['reconciled_records']} reconciled, {bedtime['minimum_chapter_words']} to {bedtime['maximum_chapter_words']} words per chapter, {bedtime['maximum_paragraph_words']} maximum paragraph words, {bedtime['paragraphs_over_180_words']} paragraphs over 180 words, {bedtime['live_marker_hits']} live marker hits. |
| Companion notes | `{gates['companion_notes_status']['status']}` | {companion['routing_records']} routing records, {companion['routing_records_with_existing_notes']} existing chapter companion notes, key-figure companion note present: {companion['key_figure_companion_note_present']}, {companion['audio_probe_companion_summaries']} figure spoken summaries routed. |

## Preserved Blockers

The following blockers remain active after this gate: {blockers}.

## Non-Claims

- This review does not approve, publish, tag, or archive any curated reader
  HTML, EPUB, DOCX, PDF, e-reader, audio, MP3, M4B, or audio-embedded EPUB
  artifact.
- This review does not clear dedicated e-reader review, e-reader application
  approval, Word review, LibreOffice GUI review, Google Docs review,
  manual keyboard-only review, screen-reader review, WCAG conformance review, narration quality
  review, audio generation, audiobook approval, or reader release approval.
- This review does not promote any chapter core claim or claim support state.
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-result", action="store_true")
    args = parser.parse_args()

    for path in (
        READER_MANIFEST,
        COMPANION_ROUTING,
        ACCESSIBILITY,
        VISUAL_IDENTITY,
        GEOMETRY,
        RASTER,
        EPUB_LAYOUT,
        PDF_LAYOUT,
        DOCX_LAYOUT,
        AUDIO_PROBE,
        FINAL_FIGURE_REVIEW,
    ):
        if not path.exists():
            fail([f"required path missing: {rel(path)}"])

    observed = build_observed()
    errors = validate_observed(observed)
    if errors:
        fail(errors)

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
        "Reader human-consumption gate passed: "
        "ebook layout, diagram image, bedtime readability, and companion notes "
        "reviewed for release preparation."
    )


if __name__ == "__main__":
    main()
