#!/usr/bin/env python3
"""Validate the final key-figure artifact release-preparation review.

This validator consumes the tracked key-figure source, accessibility, raster,
format, and layout review manifests. It does not rerun ignored build-output
probes. The review clears only the project-defined final-figure blocker for
the current curated reader candidate; it does not approve the reader release or
downstream application/e-reader/audio gates.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
READER_MANIFEST = ROOT / "editions" / "reader_manuscript" / "v1_0" / "manifest.json"
ACCESSIBILITY = ROOT / "editions" / "reader_manuscript" / "v1_0" / "accessibility_navigation_manifest.json"
CONTRAST = ROOT / "editions" / "reader_manuscript" / "v1_0" / "key_figure_contrast_manifest.json"
GEOMETRY = ROOT / "editions" / "reader_manuscript" / "v1_0" / "key_figure_geometry_manifest.json"
VISUAL_IDENTITY = ROOT / "editions" / "reader_manuscript" / "v1_0" / "visual_identity_manifest.json"
RASTER = ROOT / "editions" / "reader_manuscript" / "v1_0" / "key_figure_raster_manifest.json"
FORMAT = ROOT / "editions" / "reader_manuscript" / "v1_0" / "key_figure_format_probe_manifest.json"
EPUB_LAYOUT = ROOT / "editions" / "reader_manuscript" / "v1_0" / "key_figure_epub_layout_manifest.json"
PDF_LAYOUT = ROOT / "editions" / "reader_manuscript" / "v1_0" / "key_figure_pdf_layout_manifest.json"
DOCX_LAYOUT = ROOT / "editions" / "reader_manuscript" / "v1_0" / "key_figure_docx_layout_manifest.json"
RESULT = ROOT / "editions" / "reader_manuscript" / "v1_0" / "final_figure_artifact_review_manifest.json"
DOC = ROOT / "docs" / "reader_final_figure_artifact_review.md"
COMMAND = "python3 scripts/validate_reader_final_figure_artifact_review.py"
EXPECTED_COUNT = 10


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Reader final figure-artifact review validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def require_metric(
    owner: str,
    observed: Any,
    expected: Any,
    errors: list[str],
) -> None:
    if observed != expected:
        errors.append(f"{owner} must be {expected!r}; found {observed!r}.")


def require_minimum(owner: str, observed: Any, minimum: float, errors: list[str]) -> None:
    if not isinstance(observed, (int, float)) or observed < minimum:
        errors.append(f"{owner} must be at least {minimum}; found {observed!r}.")


def key_figures(reader_manifest: dict[str, Any]) -> list[dict[str, Any]]:
    figures = reader_manifest.get("reader_handoff_contract", {}).get("key_figure_targets", [])
    if not isinstance(figures, list):
        return []
    return [figure for figure in figures if isinstance(figure, dict)]


def build_observed() -> dict[str, Any]:
    reader_manifest = load_json(READER_MANIFEST)
    accessibility = load_json(ACCESSIBILITY)
    contrast = load_json(CONTRAST)
    geometry = load_json(GEOMETRY)
    visual = load_json(VISUAL_IDENTITY)
    raster = load_json(RASTER)
    format_probe = load_json(FORMAT)
    epub = load_json(EPUB_LAYOUT)
    pdf = load_json(PDF_LAYOUT)
    docx = load_json(DOCX_LAYOUT)

    figures = key_figures(reader_manifest)
    geometry_summary = geometry.get("summary", {}) if isinstance(geometry, dict) else {}
    contrast_summary = contrast.get("summary", {}) if isinstance(contrast, dict) else {}
    visual_palette = visual.get("palette_summary", {}) if isinstance(visual, dict) else {}
    visual_contrast = visual.get("contrast_summary", {}) if isinstance(visual, dict) else {}
    accessibility_summary = accessibility.get("summary", {}) if isinstance(accessibility, dict) else {}
    raster_summary = raster.get("summary", {}) if isinstance(raster, dict) else {}
    epub_summary = epub.get("summary", {}) if isinstance(epub, dict) else {}
    pdf_summary = pdf.get("summary", {}) if isinstance(pdf, dict) else {}
    docx_summary = docx.get("summary", {}) if isinstance(docx, dict) else {}

    return {
        "schema_version": "asi_stack.reader_final_figure_artifact_review.v0",
        "result_id": "reader-final-figure-artifact-review-2026-07-05",
        "status": "passed_final_figure_artifact_release_preparation_review",
        "command": COMMAND,
        "source_refs": [
            rel(READER_MANIFEST),
            rel(ACCESSIBILITY),
            rel(CONTRAST),
            rel(GEOMETRY),
            rel(VISUAL_IDENTITY),
            rel(RASTER),
            rel(FORMAT),
            rel(EPUB_LAYOUT),
            rel(PDF_LAYOUT),
            rel(DOCX_LAYOUT),
        ],
        "summary": {
            "figure_count": len(figures),
            "source_geometry_status": geometry.get("status"),
            "source_visual_identity_status": visual.get("status"),
            "source_accessibility_status": accessibility.get("status"),
            "contrast_all_figures_passed": contrast.get("all_figures_passed"),
            "minimum_text_contrast_ratio": contrast_summary.get("minimum_text_contrast_ratio"),
            "minimum_flow_line_contrast_ratio": contrast_summary.get("minimum_flow_line_contrast_ratio"),
            "minimum_marker_contrast_ratio": contrast_summary.get("minimum_marker_contrast_ratio"),
            "minimum_font_size_px": contrast_summary.get("minimum_font_size_px"),
            "geometry_content_bounds_passed": geometry_summary.get("content_bounds_passed_count"),
            "geometry_text_anchor_bounds_passed": geometry_summary.get("text_anchor_bounds_passed_count"),
            "geometry_minimum_content_edge_margin_px": geometry_summary.get("minimum_content_edge_margin_px"),
            "visual_identity_color_count": visual_palette.get("combined_hex_color_count"),
            "visual_identity_non_neutral_families": visual_palette.get("non_neutral_family_count"),
            "visual_identity_minimum_text_contrast_ratio": visual_contrast.get("minimum_text_contrast_ratio"),
            "accessibility_alt_texts": accessibility_summary.get("fig_alt_count"),
            "accessibility_figure_boundaries": accessibility_summary.get("figure_boundary_count"),
            "raster_status": raster.get("status"),
            "raster_artifacts": raster_summary.get("raster_artifact_count"),
            "raster_standard_dimensions": raster_summary.get("standard_dimension_count"),
            "raster_minimum_luminance_std": raster_summary.get("minimum_luminance_std"),
            "raster_minimum_quantized_colors": raster_summary.get("minimum_quantized_color_count"),
            "format_probe_status": format_probe.get("status"),
            "epub_layout_status": epub.get("status"),
            "epub_layout_page_view_pairs": epub_summary.get("page_view_pairs"),
            "epub_layout_failed_pairs": epub_summary.get("failed_page_view_pairs"),
            "epub_layout_image_failures": epub_summary.get("image_failure_count"),
            "pdf_layout_status": pdf.get("status"),
            "pdf_layout_caption_pages": pdf_summary.get("unique_caption_pages"),
            "pdf_layout_raster_pages": pdf_summary.get("raster_pages_rendered"),
            "pdf_layout_maximum_near_edge_ink_percent": pdf_summary.get("maximum_near_edge_ink_percent"),
            "docx_layout_status": docx.get("status"),
            "docx_layout_title_pages": docx_summary.get("unique_title_pages"),
            "docx_layout_raster_pages": docx_summary.get("raster_pages_rendered"),
            "docx_layout_maximum_near_edge_ink_percent": docx_summary.get("maximum_near_edge_ink_percent"),
        },
        "cleared_blockers": [
            "final_figure_artifact_review_not_completed",
        ],
        "release_blockers_preserved": [
            "reader_release_approval_not_created",
            "app_or_ereader_review_not_completed",
            "docx_application_review_not_completed",
            "manual_keyboard_only_review_not_completed",
            "screen_reader_review_not_completed",
            "wcag_conformance_review_not_completed",
            "reviewed_reader_release_record_not_created_for_audio",
            "narration_quality_review_not_completed",
            "audio_files_not_generated",
            "chapter_markers_not_timecoded",
            "audio_edition_release_record_not_created",
        ],
        "review_decision": (
            "The ten current key figures pass the project-defined final figure-artifact "
            "release-preparation gate across source accessibility, contrast, geometry, visual identity, "
            "PNG raster fallback health, EPUB package/layout survival, PDF caption-page layout, and "
            "DOCX converted title-page layout."
        ),
        "review_boundary": (
            "This clears the current curated reader candidate's final figure-artifact review blocker only. "
            "It is not reader release approval, not e-reader device/application approval, not Word/LibreOffice "
            "GUI/Google Docs review, not manual keyboard-only review, not screen-reader review, not WCAG "
            "conformance, not audiobook approval, and not a support-state transition."
        ),
        "non_claims": [
            "does not approve the curated reader edition for release",
            "does not publish, tag, archive, or distribute any reader artifact",
            "does not clear dedicated e-reader or application review",
            "does not clear Word, LibreOffice GUI, or Google Docs DOCX review",
            "does not clear manual keyboard-only review, screen-reader review, or WCAG conformance review",
            "does not generate or approve audio artifacts",
            "does not promote any chapter core claim or support state",
        ],
    }


def validate_result(result: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if result.get("schema_version") != "asi_stack.reader_final_figure_artifact_review.v0":
        errors.append("schema_version must be asi_stack.reader_final_figure_artifact_review.v0.")
    if result.get("status") != "passed_final_figure_artifact_release_preparation_review":
        errors.append("status must be passed_final_figure_artifact_release_preparation_review.")
    summary = result.get("summary", {})
    if not isinstance(summary, dict):
        errors.append("summary must be an object.")
        summary = {}

    exact_expectations = {
        "figure_count": EXPECTED_COUNT,
        "source_geometry_status": "passed_source_geometry_review",
        "source_visual_identity_status": "passed_source_level_visual_identity_review",
        "source_accessibility_status": "passed_source_accessibility_navigation_review",
        "contrast_all_figures_passed": True,
        "geometry_content_bounds_passed": EXPECTED_COUNT,
        "geometry_text_anchor_bounds_passed": EXPECTED_COUNT,
        "accessibility_alt_texts": EXPECTED_COUNT,
        "accessibility_figure_boundaries": EXPECTED_COUNT,
        "raster_status": "passed_local_raster_artifact_probe",
        "raster_artifacts": EXPECTED_COUNT,
        "raster_standard_dimensions": EXPECTED_COUNT,
        "format_probe_status": "passed_local_format_package_probe",
        "epub_layout_status": "passed_local_epub_key_figure_xhtml_layout_probe",
        "epub_layout_page_view_pairs": 20,
        "epub_layout_failed_pairs": 0,
        "epub_layout_image_failures": 0,
        "pdf_layout_status": "passed_local_pdf_key_figure_layout_probe",
        "pdf_layout_caption_pages": EXPECTED_COUNT,
        "pdf_layout_raster_pages": EXPECTED_COUNT,
        "pdf_layout_maximum_near_edge_ink_percent": 0.0,
        "docx_layout_status": "passed_local_docx_key_figure_layout_probe",
        "docx_layout_title_pages": EXPECTED_COUNT,
        "docx_layout_raster_pages": EXPECTED_COUNT,
        "docx_layout_maximum_near_edge_ink_percent": 0.0,
    }
    for key, expected in exact_expectations.items():
        require_metric(f"summary.{key}", summary.get(key), expected, errors)

    thresholds = {
        "minimum_text_contrast_ratio": 4.5,
        "minimum_flow_line_contrast_ratio": 3.0,
        "minimum_marker_contrast_ratio": 3.0,
        "minimum_font_size_px": 15.0,
        "geometry_minimum_content_edge_margin_px": 20.0,
        "visual_identity_color_count": 40,
        "visual_identity_non_neutral_families": 4,
        "visual_identity_minimum_text_contrast_ratio": 4.5,
        "raster_minimum_luminance_std": 25.0,
        "raster_minimum_quantized_colors": 100,
    }
    for key, minimum in thresholds.items():
        require_minimum(f"summary.{key}", summary.get(key), minimum, errors)

    if result.get("cleared_blockers") != ["final_figure_artifact_review_not_completed"]:
        errors.append("cleared_blockers must contain only final_figure_artifact_review_not_completed.")
    preserved = set(result.get("release_blockers_preserved", []))
    for blocker in (
        "reader_release_approval_not_created",
        "app_or_ereader_review_not_completed",
        "docx_application_review_not_completed",
        "manual_keyboard_only_review_not_completed",
        "screen_reader_review_not_completed",
        "wcag_conformance_review_not_completed",
        "audio_files_not_generated",
    ):
        if blocker not in preserved:
            errors.append(f"release_blockers_preserved missing {blocker}.")
    boundary = str(result.get("review_boundary", "")).lower()
    for phrase in (
        "final figure-artifact review blocker only",
        "not reader release approval",
        "not e-reader",
        "not word",
        "not screen-reader",
        "not wcag",
        "not audiobook",
        "not a support-state transition",
    ):
        if phrase not in boundary:
            errors.append(f"review_boundary missing {phrase!r}.")
    non_claim_text = " ".join(str(item) for item in result.get("non_claims", [])).lower()
    for phrase in (
        "does not approve the curated reader edition",
        "does not clear dedicated e-reader",
        "does not clear word",
        "does not clear manual keyboard-only",
        "does not generate or approve audio",
        "does not promote any chapter core claim",
    ):
        if phrase not in non_claim_text:
            errors.append(f"non_claims missing {phrase!r}.")
    return errors


def render_doc(result: dict[str, Any]) -> str:
    summary = result["summary"]
    preserved = ", ".join(f"`{item}`" for item in result["release_blockers_preserved"])
    cleared = ", ".join(f"`{item}`" for item in result["cleared_blockers"])
    return "\n".join(
        [
            "# Reader Final Figure-Artifact Review",
            "",
            f"Generated by `{COMMAND} --write-result`.",
            "",
            "This review aggregates the tracked source, accessibility, visual-identity, raster, package, and layout evidence for the ten key figures in the current curated reader candidate.",
            "",
            "## Summary",
            "",
            "| Metric | Value |",
            "|---|---:|",
            f"| Status | `{result['status']}` |",
            f"| Figure count | {summary['figure_count']} |",
            f"| Contrast gate | {summary['contrast_all_figures_passed']} |",
            f"| Minimum text contrast ratio | {summary['minimum_text_contrast_ratio']} |",
            f"| Minimum flow-line contrast ratio | {summary['minimum_flow_line_contrast_ratio']} |",
            f"| Minimum marker contrast ratio | {summary['minimum_marker_contrast_ratio']} |",
            f"| Minimum SVG text size | {summary['minimum_font_size_px']} px |",
            f"| Geometry content/text-anchor checks | {summary['geometry_content_bounds_passed']} / {summary['geometry_text_anchor_bounds_passed']} |",
            f"| Minimum content edge margin | {summary['geometry_minimum_content_edge_margin_px']} px |",
            f"| Visual identity colors | {summary['visual_identity_color_count']} total / {summary['visual_identity_non_neutral_families']} non-neutral families |",
            f"| Accessibility alt texts / boundaries | {summary['accessibility_alt_texts']} / {summary['accessibility_figure_boundaries']} |",
            f"| Raster artifacts / standard dimensions | {summary['raster_artifacts']} / {summary['raster_standard_dimensions']} |",
            f"| Raster minimum luminance std | {summary['raster_minimum_luminance_std']} |",
            f"| Raster minimum quantized colors | {summary['raster_minimum_quantized_colors']} |",
            f"| EPUB layout pairs / failures / image failures | {summary['epub_layout_page_view_pairs']} / {summary['epub_layout_failed_pairs']} / {summary['epub_layout_image_failures']} |",
            f"| PDF caption/raster pages | {summary['pdf_layout_caption_pages']} / {summary['pdf_layout_raster_pages']} |",
            f"| DOCX title/raster pages | {summary['docx_layout_title_pages']} / {summary['docx_layout_raster_pages']} |",
            "",
            "## Blocker Decision",
            "",
            f"Cleared blocker for the current curated reader candidate: {cleared}.",
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
            "- This review does not approve the curated reader edition for release.",
            "- This review does not publish, tag, archive, or distribute any reader artifact.",
            "- This review does not clear dedicated e-reader or application review.",
            "- This review does not clear Word, LibreOffice GUI, or Google Docs DOCX review.",
            "- This review does not clear manual keyboard-only review, screen-reader review, or WCAG conformance review.",
            "- This review does not generate or approve audio artifacts.",
            "- This review does not promote any chapter core claim or support state.",
            "",
        ]
    )


def validate_doc(result: dict[str, Any], errors: list[str]) -> None:
    if not DOC.exists():
        errors.append(f"{rel(DOC)} is missing; run with --write-result.")
        return
    expected = render_doc(result)
    current = DOC.read_text(encoding="utf-8")
    if current != expected:
        errors.append(f"{rel(DOC)} is stale; run with --write-result.")
    for fragment in (
        "Reader Final Figure-Artifact Review",
        "passed_final_figure_artifact_release_preparation_review",
        "final_figure_artifact_review_not_completed",
        "does not approve the curated reader edition",
        "does not promote any chapter core claim",
    ):
        if fragment not in current:
            errors.append(f"{rel(DOC)} missing required fragment: {fragment}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-result", action="store_true")
    args = parser.parse_args()

    for path in (
        READER_MANIFEST,
        ACCESSIBILITY,
        CONTRAST,
        GEOMETRY,
        VISUAL_IDENTITY,
        RASTER,
        FORMAT,
        EPUB_LAYOUT,
        PDF_LAYOUT,
        DOCX_LAYOUT,
    ):
        if not path.exists():
            fail([f"required path missing: {rel(path)}"])

    observed = build_observed()
    errors = validate_result(observed)
    if args.write_result:
        if errors:
            fail(errors)
        RESULT.write_text(json.dumps(observed, indent=2) + "\n", encoding="utf-8")
        DOC.write_text(render_doc(observed), encoding="utf-8")
    else:
        if not RESULT.exists():
            fail([f"{rel(RESULT)} is missing; run with --write-result."])
        current = load_json(RESULT)
        if not isinstance(current, dict):
            fail([f"{rel(RESULT)} must contain a JSON object."])
        errors = validate_result(current)
        validate_doc(current, errors)
        if errors:
            fail(errors)
        observed = current

    print(
        "Reader final figure-artifact review passed: "
        f"{observed['summary']['figure_count']} figures, "
        f"cleared {', '.join(observed['cleared_blockers'])}."
    )


if __name__ == "__main__":
    main()
