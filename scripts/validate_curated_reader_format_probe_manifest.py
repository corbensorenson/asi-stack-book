#!/usr/bin/env python3
"""Validate the tracked curated-reader format probe manifest and summary."""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "editions" / "reader_manuscript" / "v1_0" / "curated_format_probe_manifest.json"
SUMMARY = ROOT / "docs" / "curated_reader_format_artifact_probe.md"
EXPECTED_FORMATS = {"html", "epub", "docx", "pdf"}
REQUIRED_COMMANDS = {
    "python3 scripts/render_curated_reader_formats.py --formats html epub docx --include-pdf",
    "python3 scripts/inspect_curated_reader_format_artifacts.py",
    "python3 scripts/sync_curated_reader_format_probe_manifest.py",
    "python3 scripts/repair_curated_reader_epub_links.py",
    "python3 scripts/repair_curated_reader_docx_links.py",
    "python3 scripts/audit_curated_reader_pdf_layout.py",
    "python3 scripts/audit_curated_reader_pdf_visual_raster.py",
    "python3 scripts/audit_curated_reader_epub_content.py",
    "node scripts/validate_curated_reader_epub_browser_review.js --write-manifest",
    "python3 scripts/audit_curated_reader_docx_content.py",
    "python3 scripts/validate_curated_reader_docx_libreoffice_review.py --write-manifest",
    "python3 scripts/validate_curated_reader_pdf_reading_flow.py --write-manifest",
    "python3 scripts/validate_curated_reader_pdf_viewer_review.py --write-manifest",
}
REQUIRED_BLOCKERS = {
    "format_artifact_not_reviewed",
    "reader_release_record_not_created",
    "full_format_artifact_review_not_completed",
    "app_or_ereader_review_not_completed",
}
SHA_RE = re.compile(r"^[0-9a-f]{64}$")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Curated reader format probe validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


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


def require_int(owner: str, key: str, value: Any, errors: list[str], *, minimum: int = 0) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        errors.append(f"{owner}: {key} must be an integer.")
        return 0
    if value < minimum:
        errors.append(f"{owner}: {key} must be at least {minimum}.")
    return value


def validate_manifest(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if manifest.get("schema_version") != "0.1":
        errors.append("schema_version must be 0.1.")
    if manifest.get("major_version") != "v1.0":
        errors.append("major_version must be v1.0.")
    if manifest.get("status") != "curated_local_structural_inspection_record":
        errors.append("status must be curated_local_structural_inspection_record.")
    if manifest.get("source_mode") != "tracked_curated_reader_manuscript":
        errors.append("source_mode must be tracked_curated_reader_manuscript.")
    require_string("manifest", "purpose", manifest.get("purpose"), errors, min_words=12)
    review_decision = require_string("manifest", "review_decision", manifest.get("review_decision"), errors, min_words=20)
    for phrase in (
        "renders locally to HTML, EPUB, DOCX, and PDF",
        "PDF extracted-text reading-flow review checks 506 text pages",
        "headed Chromium PDF viewer smoke review records 2 nonblank viewer screenshots",
        "remain unapproved",
    ):
        if phrase not in review_decision:
            errors.append(f"review_decision missing required phrase: {phrase}")
    if "PDF reading-flow review, and an edition release record do not yet exist" in review_decision:
        errors.append("review_decision must not say the automated PDF reading-flow review is missing.")

    commands = set(require_string_list("manifest", "source_commands", manifest.get("source_commands"), errors))
    missing_commands = sorted(REQUIRED_COMMANDS - commands)
    if missing_commands:
        errors.append(f"source_commands missing required command(s): {missing_commands}")

    for ref in require_string_list("manifest", "local_report_refs", manifest.get("local_report_refs"), errors):
        if not ref.startswith("build/curated_reader_edition/"):
            errors.append(f"local_report_refs should point to ignored curated-reader build reports: {ref}")

    for ref in require_string_list("manifest", "tracked_evidence_refs", manifest.get("tracked_evidence_refs"), errors):
        if not (ROOT / ref).exists():
            errors.append(f"tracked_evidence_refs path does not exist: {ref}")

    render_summary = manifest.get("render_summary")
    inspection_summary = manifest.get("inspection_summary")
    pdf_layout_audit = manifest.get("pdf_layout_audit")
    pdf_visual_raster_audit = manifest.get("pdf_visual_raster_audit")
    pdf_reading_flow_review = manifest.get("pdf_reading_flow_review")
    pdf_viewer_review = manifest.get("pdf_viewer_review")
    epub_content_audit = manifest.get("epub_content_audit")
    epub_browser_review = manifest.get("epub_browser_review")
    docx_content_audit = manifest.get("docx_content_audit")
    docx_libreoffice_review = manifest.get("docx_libreoffice_review")
    if not isinstance(render_summary, dict):
        errors.append("render_summary must be an object.")
        render_summary = {}
    if not isinstance(inspection_summary, dict):
        errors.append("inspection_summary must be an object.")
        inspection_summary = {}
    if not isinstance(pdf_layout_audit, dict):
        errors.append("pdf_layout_audit must be an object.")
        pdf_layout_audit = {}
    if not isinstance(pdf_visual_raster_audit, dict):
        errors.append("pdf_visual_raster_audit must be an object.")
        pdf_visual_raster_audit = {}
    if not isinstance(pdf_reading_flow_review, dict):
        errors.append("pdf_reading_flow_review must be an object.")
        pdf_reading_flow_review = {}
    if not isinstance(pdf_viewer_review, dict):
        errors.append("pdf_viewer_review must be an object.")
        pdf_viewer_review = {}
    if not isinstance(epub_content_audit, dict):
        errors.append("epub_content_audit must be an object.")
        epub_content_audit = {}
    if not isinstance(epub_browser_review, dict):
        errors.append("epub_browser_review must be an object.")
        epub_browser_review = {}
    if not isinstance(docx_content_audit, dict):
        errors.append("docx_content_audit must be an object.")
        docx_content_audit = {}
    if not isinstance(docx_libreoffice_review, dict):
        errors.append("docx_libreoffice_review must be an object.")
        docx_libreoffice_review = {}
    if set(render_summary) != EXPECTED_FORMATS:
        errors.append(f"render_summary must contain exactly {sorted(EXPECTED_FORMATS)}.")
    if set(inspection_summary) != EXPECTED_FORMATS:
        errors.append(f"inspection_summary must contain exactly {sorted(EXPECTED_FORMATS)}.")

    expected_render = {
        "html": {"artifacts_observed": 49, "preserved_artifacts": 81, "warning_count": 0, "svg_conversion_warning_count": 0},
        "epub": {"artifacts_observed": 1, "preserved_artifacts": 1, "warning_count": 0, "svg_conversion_warning_count": 0},
        "docx": {"artifacts_observed": 1, "preserved_artifacts": 1, "warning_count": 0, "svg_conversion_warning_count": 0},
        "pdf": {"artifacts_observed": 1, "preserved_artifacts": 1, "warning_count": 0, "svg_conversion_warning_count": 0},
    }
    for fmt, expected in expected_render.items():
        render = render_summary.get(fmt, {})
        if not isinstance(render, dict):
            errors.append(f"render_summary.{fmt} must be an object.")
            continue
        if render.get("status") != "rendered":
            errors.append(f"render_summary.{fmt}.status must be rendered.")
        for key, expected_value in expected.items():
            if render.get(key) != expected_value:
                errors.append(f"render_summary.{fmt}.{key} must be {expected_value}.")
        if fmt in {"docx", "pdf"}:
            if render.get("png_fallback_count") != 10:
                errors.append(f"render_summary.{fmt}.png_fallback_count must be 10.")
            if render.get("png_fallback_converter") not in {"sips", "rsvg-convert"}:
                errors.append(f"render_summary.{fmt}.png_fallback_converter must be sips or rsvg-convert.")
        if fmt == "pdf":
            if render.get("pdf_mermaid_fallback_count") != 50:
                errors.append("render_summary.pdf.pdf_mermaid_fallback_count must be 50.")
            if render.get("pdf_mermaid_fallback_converter") != "chrome-screenshot":
                errors.append("render_summary.pdf.pdf_mermaid_fallback_converter must be chrome-screenshot.")
            if render.get("pdf_mermaid_rewritten_files") != 44:
                errors.append("render_summary.pdf.pdf_mermaid_rewritten_files must be 44.")

    html = inspection_summary.get("html", {}) if isinstance(inspection_summary, dict) else {}
    if isinstance(html, dict):
        if html.get("status") != "passed":
            errors.append("inspection_summary.html.status must be passed.")
        if html.get("html_files") != 49:
            errors.append("inspection_summary.html.html_files must be 49.")
        if html.get("site_html_files") != 49:
            errors.append("inspection_summary.html.site_html_files must be 49.")
        if html.get("chapter_files") != 44:
            errors.append("inspection_summary.html.chapter_files must be 44.")
        if html.get("live_marker_leaks") != 0:
            errors.append("inspection_summary.html.live_marker_leaks must be 0.")
        if html.get("raw_core_claim_marker_leaks") != 0:
            errors.append("inspection_summary.html.raw_core_claim_marker_leaks must be 0.")

    epub = inspection_summary.get("epub", {}) if isinstance(inspection_summary, dict) else {}
    if isinstance(epub, dict):
        if epub.get("status") != "passed":
            errors.append("inspection_summary.epub.status must be passed.")
        require_int("inspection_summary.epub", "bytes", epub.get("bytes"), errors, minimum=1_000_000)
        require_int("inspection_summary.epub", "xhtml_entries", epub.get("xhtml_entries"), errors, minimum=49)
        require_int("inspection_summary.epub", "image_entries", epub.get("image_entries"), errors, minimum=44)
        if epub.get("opf_title") != "The ASI Stack":
            errors.append("inspection_summary.epub.opf_title must be The ASI Stack.")
        if epub.get("opf_creator") != "Corben Sorenson":
            errors.append("inspection_summary.epub.opf_creator must be Corben Sorenson.")
        if epub.get("opf_language") != "en-US":
            errors.append("inspection_summary.epub.opf_language must be en-US.")
        if not SHA_RE.match(str(epub.get("sha256", ""))):
            errors.append("inspection_summary.epub.sha256 must be a SHA-256 digest.")
        required = set(require_string_list("inspection_summary.epub", "required_entries_present", epub.get("required_entries_present"), errors))
        for entry in {"mimetype", "META-INF/container.xml", "EPUB/content.opf", "EPUB/nav.xhtml", "EPUB/toc.ncx"}:
            if entry not in required:
                errors.append(f"inspection_summary.epub.required_entries_present missing {entry}.")

    docx = inspection_summary.get("docx", {}) if isinstance(inspection_summary, dict) else {}
    if isinstance(docx, dict):
        if docx.get("status") != "passed":
            errors.append("inspection_summary.docx.status must be passed.")
        require_int("inspection_summary.docx", "bytes", docx.get("bytes"), errors, minimum=1_000_000)
        require_int("inspection_summary.docx", "media_entries", docx.get("media_entries"), errors, minimum=44)
        require_int("inspection_summary.docx", "png_media_entries", docx.get("png_media_entries"), errors, minimum=44)
        if docx.get("svg_media_entries") != 0:
            errors.append("inspection_summary.docx.svg_media_entries must be 0.")
        require_int("inspection_summary.docx", "paragraph_markers", docx.get("paragraph_markers"), errors, minimum=1000)
        if not SHA_RE.match(str(docx.get("sha256", ""))):
            errors.append("inspection_summary.docx.sha256 must be a SHA-256 digest.")
        required = set(require_string_list("inspection_summary.docx", "required_entries_present", docx.get("required_entries_present"), errors))
        for entry in {"[Content_Types].xml", "_rels/.rels", "word/document.xml", "word/styles.xml", "word/_rels/document.xml.rels"}:
            if entry not in required:
                errors.append(f"inspection_summary.docx.required_entries_present missing {entry}.")

    pdf = inspection_summary.get("pdf", {}) if isinstance(inspection_summary, dict) else {}
    if isinstance(pdf, dict):
        if pdf.get("status") != "passed":
            errors.append("inspection_summary.pdf.status must be passed.")
        require_int("inspection_summary.pdf", "bytes", pdf.get("bytes"), errors, minimum=1_000_000)
        if not SHA_RE.match(str(pdf.get("sha256", ""))):
            errors.append("inspection_summary.pdf.sha256 must be a SHA-256 digest.")
        if pdf.get("pages") != 506:
            errors.append("inspection_summary.pdf.pages must be 506.")
        if pdf.get("title") != "The ASI Stack":
            errors.append("inspection_summary.pdf.title must be The ASI Stack.")
        if pdf.get("author") != "Corben Sorenson":
            errors.append("inspection_summary.pdf.author must be Corben Sorenson.")
        if pdf.get("encrypted") != "no":
            errors.append("inspection_summary.pdf.encrypted must be no.")
        if "612 x 792" not in str(pdf.get("page_size", "")):
            errors.append("inspection_summary.pdf.page_size must describe letter pages.")
        sample_pages = pdf.get("sample_pages")
        if sample_pages != [1, 2, 25, 300, 500]:
            errors.append("inspection_summary.pdf.sample_pages must be [1, 2, 25, 300, 500].")
        sample_pngs = require_string_list("inspection_summary.pdf", "sample_page_pngs", pdf.get("sample_page_pngs"), errors)
        if len(sample_pngs) != 5:
            errors.append("inspection_summary.pdf.sample_page_pngs must contain five rendered sample pages.")
        markers = set(require_string_list("inspection_summary.pdf", "required_text_markers", pdf.get("required_text_markers"), errors))
        for marker in {"The ASI Stack", "Reader Edition Draft", "evidence boundary", "Reader Source List", "External Citation Policy"}:
            if marker not in markers:
                errors.append(f"inspection_summary.pdf.required_text_markers missing {marker}.")

    if pdf_layout_audit:
        if pdf_layout_audit.get("status") != "passed_full_text_bbox_probe":
            errors.append("pdf_layout_audit.status must be passed_full_text_bbox_probe.")
        if pdf_layout_audit.get("source_artifact") != "build/curated_reader_edition/format_artifacts/pdf/_reader_site/The-ASI-Stack.pdf":
            errors.append("pdf_layout_audit.source_artifact must point to the curated reader PDF.")
        if pdf_layout_audit.get("source_sha256") != pdf.get("sha256"):
            errors.append("pdf_layout_audit.source_sha256 must match inspection_summary.pdf.sha256.")
        if pdf_layout_audit.get("pages_checked") != 506:
            errors.append("pdf_layout_audit.pages_checked must be 506.")
        if pdf_layout_audit.get("word_boxes_checked") != 170036:
            errors.append("pdf_layout_audit.word_boxes_checked must be 170036.")
        if pdf_layout_audit.get("textless_pages") != 0:
            errors.append("pdf_layout_audit.textless_pages must be 0.")
        if pdf_layout_audit.get("out_of_bounds_word_boxes") != 0:
            errors.append("pdf_layout_audit.out_of_bounds_word_boxes must be 0.")
        if pdf_layout_audit.get("long_layout_lines_over_160_chars") != 0:
            errors.append("pdf_layout_audit.long_layout_lines_over_160_chars must be 0.")
        if pdf_layout_audit.get("min_word_box_height") != 14.531:
            errors.append("pdf_layout_audit.min_word_box_height must be 14.531.")
        if pdf_layout_audit.get("max_word_box_height") != 35.47:
            errors.append("pdf_layout_audit.max_word_box_height must be 35.47.")
        markers = set(require_string_list("pdf_layout_audit", "required_text_markers_present", pdf_layout_audit.get("required_text_markers_present"), errors))
        for marker in {"The ASI Stack", "Reader Edition Draft", "evidence boundary", "Reader Source List", "External Citation Policy"}:
            if marker not in markers:
                errors.append(f"pdf_layout_audit.required_text_markers_present missing {marker}.")
        boundary = require_string("pdf_layout_audit", "review_boundary", pdf_layout_audit.get("review_boundary"), errors, min_words=18)
        if "not manual PDF page-by-page review" not in boundary or "does not approve the PDF artifact" not in boundary:
            errors.append("pdf_layout_audit.review_boundary must preserve manual-review and release-approval boundaries.")

    if pdf_visual_raster_audit:
        if pdf_visual_raster_audit.get("status") != "passed_all_page_pdf_raster_probe":
            errors.append("pdf_visual_raster_audit.status must be passed_all_page_pdf_raster_probe.")
        if pdf_visual_raster_audit.get("source_artifact") != "build/curated_reader_edition/format_artifacts/pdf/_reader_site/The-ASI-Stack.pdf":
            errors.append("pdf_visual_raster_audit.source_artifact must point to the curated reader PDF.")
        if pdf_visual_raster_audit.get("source_sha256") != pdf.get("sha256"):
            errors.append("pdf_visual_raster_audit.source_sha256 must match inspection_summary.pdf.sha256.")
        expected_values = {
            "raster_dpi": 72,
            "nonwhite_threshold": 245,
            "edge_margin_px": 2,
            "low_ink_threshold": 1000,
            "pages_rendered": 506,
            "page_width_pixels": [612],
            "page_height_pixels": [792],
            "blank_pages": 0,
            "low_ink_pages": 1,
            "near_edge_content_pages": 0,
            "min_nonwhite_pixels": 695,
            "max_nonwhite_pixels": 105553,
            "min_left_margin_px": 82,
            "min_top_margin_px": 71,
            "min_right_margin_px": 4,
            "min_bottom_margin_px": 92,
            "sample_low_ink_pages": [24],
            "sample_near_edge_pages": [],
        }
        for key, expected_value in expected_values.items():
            if pdf_visual_raster_audit.get(key) != expected_value:
                errors.append(f"pdf_visual_raster_audit.{key} must be {expected_value!r}.")
        boundary = require_string("pdf_visual_raster_audit", "review_boundary", pdf_visual_raster_audit.get("review_boundary"), errors, min_words=18)
        if "not manual PDF page-by-page review" not in boundary or "does not approve the PDF artifact" not in boundary:
            errors.append("pdf_visual_raster_audit.review_boundary must preserve manual-review and release-approval boundaries.")

    if pdf_reading_flow_review:
        if pdf_reading_flow_review.get("status") != "passed_pdf_extracted_text_reading_flow_review":
            errors.append("pdf_reading_flow_review.status must be passed_pdf_extracted_text_reading_flow_review.")
        if pdf_reading_flow_review.get("source_artifact") != "build/curated_reader_edition/format_artifacts/pdf/_reader_site/The-ASI-Stack.pdf":
            errors.append("pdf_reading_flow_review.source_artifact must point to the curated reader PDF.")
        if not SHA_RE.match(str(pdf_reading_flow_review.get("source_sha256", ""))):
            errors.append("pdf_reading_flow_review.source_sha256 must be a SHA-256 digest.")
        if pdf and pdf_reading_flow_review.get("source_sha256") != pdf.get("sha256"):
            errors.append("pdf_reading_flow_review.source_sha256 must match inspection_summary.pdf.sha256.")
        expected_values = {
            "pdfinfo_pages": 506,
            "pdfinfo_title": "The ASI Stack",
            "pdfinfo_author": "Corben Sorenson",
            "pdfinfo_encrypted": "no",
            "pdfinfo_page_size": "612 x 792 pts (letter)",
            "text_characters_checked": 1104355,
            "word_tokens_checked": 169502,
            "form_feed_count": 506,
            "text_pages_checked": 506,
            "nonempty_text_pages": 506,
            "min_page_text_characters": 44,
            "max_page_text_characters": 3828,
            "pages_under_300_text_characters": 17,
            "max_word_characters": 83,
            "replacement_character_count": 0,
            "live_marker_hits": 0,
            "raw_core_claim_marker_hits": 0,
            "chapter_headings_checked": 44,
            "chapter_heading_errors": [],
            "first_chapter_pdf_text_page_index": 28,
            "last_chapter_pdf_text_page_index": 412,
            "appendix_headings_checked": 3,
            "appendix_heading_errors": [],
        }
        for key, expected_value in expected_values.items():
            if pdf_reading_flow_review.get(key) != expected_value:
                errors.append(f"pdf_reading_flow_review.{key} must be {expected_value!r}.")
        markers = set(require_string_list("pdf_reading_flow_review", "required_text_markers_present", pdf_reading_flow_review.get("required_text_markers_present"), errors))
        for marker in {"The ASI Stack", "Reader Edition Draft", "evidence boundary", "Reader Source List", "External Citation Policy"}:
            if marker not in markers:
                errors.append(f"pdf_reading_flow_review.required_text_markers_present missing {marker}.")
        samples = pdf_reading_flow_review.get("chapter_heading_samples", [])
        if not isinstance(samples, list) or len(samples) != 6:
            errors.append("pdf_reading_flow_review.chapter_heading_samples must carry first/last three chapter headings.")
        appendix_samples = pdf_reading_flow_review.get("appendix_heading_samples", [])
        if not isinstance(appendix_samples, list) or len(appendix_samples) != 3:
            errors.append("pdf_reading_flow_review.appendix_heading_samples must carry three appendix headings.")
        boundary = require_string("pdf_reading_flow_review", "review_boundary", pdf_reading_flow_review.get("review_boundary"), errors, min_words=24)
        if "not manual PDF page-by-page reading-flow review" not in boundary or "does not approve the PDF artifact" not in boundary:
            errors.append("pdf_reading_flow_review.review_boundary must preserve manual-review and release-approval boundaries.")
        non_claim_text = " ".join(require_string_list("pdf_reading_flow_review", "non_claims", pdf_reading_flow_review.get("non_claims"), errors)).lower()
        for phrase in ("does not approve the pdf artifact", "does not replace manual pdf page-by-page reading-flow review", "does not promote any chapter core claim"):
            if phrase not in non_claim_text:
                errors.append(f"pdf_reading_flow_review.non_claims missing boundary phrase: {phrase}")

    if pdf_viewer_review:
        if pdf_viewer_review.get("status") != "passed_chromium_pdf_viewer_smoke_review":
            errors.append("pdf_viewer_review.status must be passed_chromium_pdf_viewer_smoke_review.")
        if pdf_viewer_review.get("source_artifact") != "build/curated_reader_edition/format_artifacts/pdf/_reader_site/The-ASI-Stack.pdf":
            errors.append("pdf_viewer_review.source_artifact must point to the curated reader PDF.")
        if not SHA_RE.match(str(pdf_viewer_review.get("source_sha256", ""))):
            errors.append("pdf_viewer_review.source_sha256 must be a SHA-256 digest.")
        if pdf and pdf_viewer_review.get("source_sha256") != pdf.get("sha256"):
            errors.append("pdf_viewer_review.source_sha256 must match inspection_summary.pdf.sha256.")
        expected_values = {
            "renderer": "Google Chrome PDF viewer through headed Playwright",
            "viewport_width": 1280,
            "viewport_height": 900,
            "pdfinfo_pages": 506,
            "viewer_url_scheme": "file",
            "viewer_shell_detected": True,
            "viewer_dom_body_text_characters": 0,
            "viewer_html_shell_characters": 159,
            "page_down_changed_pixel_percent": 4.434,
        }
        for key, expected_value in expected_values.items():
            if pdf_viewer_review.get(key) != expected_value:
                errors.append(f"pdf_viewer_review.{key} must be {expected_value!r}.")
        screenshots = pdf_viewer_review.get("screenshots", [])
        if not isinstance(screenshots, list) or len(screenshots) != 2:
            errors.append("pdf_viewer_review.screenshots must contain two rows.")
            screenshots = []
        for index, row in enumerate(screenshots):
            if not isinstance(row, dict):
                errors.append("pdf_viewer_review screenshot rows must be objects.")
                continue
            if row.get("width") != 1280 or row.get("height") != 900:
                errors.append(f"pdf_viewer_review.screenshots[{index}] dimensions must be 1280 x 900.")
            require_int(f"pdf_viewer_review.screenshots[{index}]", "bytes", row.get("bytes"), errors, minimum=20_000)
            if row.get("dark_pixel_percent", 0) < 10:
                errors.append(f"pdf_viewer_review.screenshots[{index}] must include dark viewer chrome.")
            if row.get("white_pixel_percent", 0) < 20:
                errors.append(f"pdf_viewer_review.screenshots[{index}] must include a white page region.")
            if row.get("luminance_variation_proxy", 0) < 40:
                errors.append(f"pdf_viewer_review.screenshots[{index}] must be visibly nonblank.")
        boundary = require_string("pdf_viewer_review", "review_boundary", pdf_viewer_review.get("review_boundary"), errors, min_words=24)
        if "not manual page-by-page PDF review" not in boundary or "does not approve the PDF artifact" not in boundary:
            errors.append("pdf_viewer_review.review_boundary must preserve manual-review and release-approval boundaries.")
        non_claim_text = " ".join(require_string_list("pdf_viewer_review", "non_claims", pdf_viewer_review.get("non_claims"), errors)).lower()
        for phrase in ("does not approve the pdf artifact", "does not replace manual pdf page-by-page", "does not promote any chapter core claim"):
            if phrase not in non_claim_text:
                errors.append(f"pdf_viewer_review.non_claims missing boundary phrase: {phrase}")

    if epub_content_audit:
        if epub_content_audit.get("status") != "passed_epub_package_content_navigation_probe":
            errors.append("epub_content_audit.status must be passed_epub_package_content_navigation_probe.")
        if epub_content_audit.get("source_artifact") != "build/curated_reader_edition/format_artifacts/epub/_reader_site/The-ASI-Stack.epub":
            errors.append("epub_content_audit.source_artifact must point to the curated reader EPUB.")
        if not SHA_RE.match(str(epub_content_audit.get("source_sha256", ""))):
            errors.append("epub_content_audit.source_sha256 must be a SHA-256 digest.")
        if epub_content_audit.get("xhtml_entries_checked") != 52:
            errors.append("epub_content_audit.xhtml_entries_checked must be 52.")
        if epub_content_audit.get("content_xhtml_entries_checked") != 49:
            errors.append("epub_content_audit.content_xhtml_entries_checked must be 49.")
        require_int("epub_content_audit", "total_text_characters_checked", epub_content_audit.get("total_text_characters_checked"), errors, minimum=500_000)
        if epub_content_audit.get("nav_href_count") != epub.get("nav_href_count"):
            errors.append("epub_content_audit.nav_href_count must match inspection_summary.epub.nav_href_count.")
        if epub_content_audit.get("opf_item_count") != epub.get("opf_item_count"):
            errors.append("epub_content_audit.opf_item_count must match inspection_summary.epub.opf_item_count.")
        if epub_content_audit.get("opf_itemref_count") != epub.get("opf_itemref_count"):
            errors.append("epub_content_audit.opf_itemref_count must match inspection_summary.epub.opf_itemref_count.")
        for zero_key in (
            "empty_xhtml_entries",
            "live_marker_hits",
            "raw_core_claim_marker_hits",
            "unresolved_internal_hrefs",
            "bare_class_attribute_hits",
            "figure_paragraph_wrapper_hits",
            "xml_parse_errors",
        ):
            if epub_content_audit.get(zero_key) != 0:
                errors.append(f"epub_content_audit.{zero_key} must be 0.")
        markers = set(require_string_list("epub_content_audit", "required_text_markers_present", epub_content_audit.get("required_text_markers_present"), errors))
        for marker in {"The ASI Stack", "Reader Edition Draft", "evidence boundary", "Reader Source List", "External Citation Policy"}:
            if marker not in markers:
                errors.append(f"epub_content_audit.required_text_markers_present missing {marker}.")
        boundary = require_string("epub_content_audit", "review_boundary", epub_content_audit.get("review_boundary"), errors, min_words=18)
        if "not e-reader application review" not in boundary or "does not approve the EPUB artifact" not in boundary:
            errors.append("epub_content_audit.review_boundary must preserve e-reader and release-approval boundaries.")

    if epub_browser_review:
        if epub_browser_review.get("status") != "passed_browser_xhtml_application_review":
            errors.append("epub_browser_review.status must be passed_browser_xhtml_application_review.")
        if epub_browser_review.get("source_artifact") != "build/curated_reader_edition/format_artifacts/epub/_reader_site/The-ASI-Stack.epub":
            errors.append("epub_browser_review.source_artifact must point to the curated reader EPUB.")
        if not SHA_RE.match(str(epub_browser_review.get("source_sha256", ""))):
            errors.append("epub_browser_review.source_sha256 must be a SHA-256 digest.")
        if epub_content_audit and epub_browser_review.get("source_sha256") != epub_content_audit.get("source_sha256"):
            errors.append("epub_browser_review.source_sha256 must match epub_content_audit.source_sha256.")
        expected_values = {
            "spine_entries_checked": 52,
            "content_xhtml_entries_checked": 49,
            "viewport_count": 2,
            "page_view_pairs": 104,
            "failed_page_view_pairs": 0,
            "image_load_failures": 0,
            "live_marker_hits": 0,
            "raw_core_claim_marker_hits": 0,
        }
        for key, expected_value in expected_values.items():
            if epub_browser_review.get(key) != expected_value:
                errors.append(f"epub_browser_review.{key} must be {expected_value}.")
        require_int("epub_browser_review", "rendered_image_count", epub_browser_review.get("rendered_image_count"), errors, minimum=10)
        require_int("epub_browser_review", "max_horizontal_overflow_px", epub_browser_review.get("max_horizontal_overflow_px"), errors, minimum=0)
        require_int("epub_browser_review", "min_body_text_chars", epub_browser_review.get("min_body_text_chars"), errors, minimum=0)
        require_int("epub_browser_review", "min_content_body_text_chars", epub_browser_review.get("min_content_body_text_chars"), errors, minimum=500)
        markers = set(require_string_list("epub_browser_review", "required_text_markers_present", epub_browser_review.get("required_text_markers_present"), errors))
        for marker in {"The ASI Stack", "Reader Edition Draft", "evidence boundary", "Reader Source List", "External Citation Policy"}:
            if marker not in markers:
                errors.append(f"epub_browser_review.required_text_markers_present missing {marker}.")
        boundary = require_string("epub_browser_review", "review_boundary", epub_browser_review.get("review_boundary"), errors, min_words=20)
        if "not dedicated e-reader" not in boundary or "does not approve the EPUB artifact" not in boundary:
            errors.append("epub_browser_review.review_boundary must preserve e-reader and release-approval boundaries.")
        non_claim_text = " ".join(require_string_list("epub_browser_review", "non_claims", epub_browser_review.get("non_claims"), errors)).lower()
        for phrase in ("does not approve the epub artifact", "does not replace dedicated e-reader", "does not promote any chapter core claim"):
            if phrase not in non_claim_text:
                errors.append(f"epub_browser_review.non_claims missing boundary phrase: {phrase}")

    if docx_content_audit:
        if docx_content_audit.get("status") != "passed_docx_document_xml_relationship_probe":
            errors.append("docx_content_audit.status must be passed_docx_document_xml_relationship_probe.")
        if docx_content_audit.get("source_artifact") != "build/curated_reader_edition/format_artifacts/docx/_reader_site/The-ASI-Stack.docx":
            errors.append("docx_content_audit.source_artifact must point to the curated reader DOCX.")
        if not SHA_RE.match(str(docx_content_audit.get("source_sha256", ""))):
            errors.append("docx_content_audit.source_sha256 must be a SHA-256 digest.")
        expected_values = {
            "zip_entries": 77,
            "paragraph_markers": 17369,
            "image_relationships": 61,
            "media_entries": 61,
            "png_media_entries": 61,
            "svg_media_entries": 0,
            "raw_qmd_relationship_targets": 0,
            "unresolved_internal_relationship_targets": 0,
            "live_marker_hits": 0,
            "raw_core_claim_marker_hits": 0,
        }
        for key, expected_value in expected_values.items():
            if docx_content_audit.get(key) != expected_value:
                errors.append(f"docx_content_audit.{key} must be {expected_value}.")
        require_int("docx_content_audit", "document_xml_characters", docx_content_audit.get("document_xml_characters"), errors, minimum=2_000_000)
        require_int("docx_content_audit", "text_characters_checked", docx_content_audit.get("text_characters_checked"), errors, minimum=1_000_000)
        require_int("docx_content_audit", "relationship_count", docx_content_audit.get("relationship_count"), errors, minimum=250)
        require_int("docx_content_audit", "external_hyperlink_relationships", docx_content_audit.get("external_hyperlink_relationships"), errors, minimum=200)
        markers = set(require_string_list("docx_content_audit", "required_text_markers_present", docx_content_audit.get("required_text_markers_present"), errors))
        for marker in {"The ASI Stack", "Reader Edition Draft", "evidence boundary", "Reader Source List", "External Citation Policy"}:
            if marker not in markers:
                errors.append(f"docx_content_audit.required_text_markers_present missing {marker}.")
        boundary = require_string("docx_content_audit", "review_boundary", docx_content_audit.get("review_boundary"), errors, min_words=18)
        if "not Word, LibreOffice GUI, or Google Docs application review" not in boundary or "does not approve the DOCX artifact" not in boundary:
            errors.append("docx_content_audit.review_boundary must preserve application-review and release-approval boundaries.")

    if docx_libreoffice_review:
        if docx_libreoffice_review.get("status") != "passed_docx_libreoffice_headless_pdf_review":
            errors.append("docx_libreoffice_review.status must be passed_docx_libreoffice_headless_pdf_review.")
        if docx_libreoffice_review.get("source_artifact") != "build/curated_reader_edition/format_artifacts/docx/_reader_site/The-ASI-Stack.docx":
            errors.append("docx_libreoffice_review.source_artifact must point to the curated reader DOCX.")
        if not SHA_RE.match(str(docx_libreoffice_review.get("source_sha256", ""))):
            errors.append("docx_libreoffice_review.source_sha256 must be a SHA-256 digest.")
        if docx_content_audit and docx_libreoffice_review.get("source_sha256") != docx_content_audit.get("source_sha256"):
            errors.append("docx_libreoffice_review.source_sha256 must match docx_content_audit.source_sha256.")
        expected_values = {
            "converted_pdf_pages": 504,
            "converted_pdf_title": "The ASI Stack",
            "converted_pdf_author": "Corben Sorenson",
            "converted_pdf_creator": "Writer",
            "converted_pdf_tagged": "yes",
            "converted_pdf_encrypted": "no",
            "converted_pdf_page_size": "612 x 792 pts (letter)",
            "raster_dpi": 72,
            "nonwhite_threshold": 245,
            "edge_margin_px": 2,
            "low_ink_threshold": 1000,
            "pages_raster_rendered": 504,
            "page_width_pixels": [612],
            "page_height_pixels": [792],
            "blank_pages": 0,
            "low_ink_pages": 0,
            "near_edge_content_pages": 0,
            "min_nonwhite_pixels": 10476,
            "max_nonwhite_pixels": 103397,
            "min_left_margin_px": 66,
            "min_top_margin_px": 72,
            "min_right_margin_px": 72,
            "min_bottom_margin_px": 72,
            "sample_blank_pages": [],
            "sample_low_ink_pages": [],
            "sample_near_edge_pages": [],
            "live_marker_hits": 0,
            "raw_core_claim_marker_hits": 0,
        }
        for key, expected_value in expected_values.items():
            if docx_libreoffice_review.get(key) != expected_value:
                errors.append(f"docx_libreoffice_review.{key} must be {expected_value!r}.")
        require_int("docx_libreoffice_review", "converted_pdf_file_size_bytes", docx_libreoffice_review.get("converted_pdf_file_size_bytes"), errors, minimum=8_000_000)
        require_int("docx_libreoffice_review", "text_characters_checked", docx_libreoffice_review.get("text_characters_checked"), errors, minimum=1_000_000)
        if "LibreOffice" not in str(docx_libreoffice_review.get("converted_pdf_producer", "")):
            errors.append("docx_libreoffice_review.converted_pdf_producer must identify LibreOffice.")
        markers = set(require_string_list("docx_libreoffice_review", "required_text_markers_present", docx_libreoffice_review.get("required_text_markers_present"), errors))
        for marker in {"The ASI Stack", "Reader Edition Draft", "evidence boundary", "Reader Source List", "External Citation Policy"}:
            if marker not in markers:
                errors.append(f"docx_libreoffice_review.required_text_markers_present missing {marker}.")
        boundary = require_string("docx_libreoffice_review", "review_boundary", docx_libreoffice_review.get("review_boundary"), errors, min_words=22)
        if "not Word review" not in boundary or "not LibreOffice GUI review" not in boundary or "does not approve the DOCX artifact" not in boundary:
            errors.append("docx_libreoffice_review.review_boundary must preserve Word/GUI/Docs and release-approval boundaries.")
        non_claim_text = " ".join(require_string_list("docx_libreoffice_review", "non_claims", docx_libreoffice_review.get("non_claims"), errors)).lower()
        for phrase in ("does not approve the docx artifact", "does not replace word, libreoffice gui, or google docs", "does not promote any chapter core claim"):
            if phrase not in non_claim_text:
                errors.append(f"docx_libreoffice_review.non_claims missing boundary phrase: {phrase}")

    blockers = set(require_string_list("manifest", "release_blockers_preserved", manifest.get("release_blockers_preserved"), errors))
    missing_blockers = sorted(REQUIRED_BLOCKERS - blockers)
    if missing_blockers:
        errors.append(f"release_blockers_preserved missing {missing_blockers}.")

    non_claims = require_string_list("manifest", "non_claims", manifest.get("non_claims"), errors)
    non_claim_text = " ".join(non_claims).lower()
    for phrase in ("not a reader release", "does not approve", "does not check full editorial quality", "does not promote"):
        if phrase not in non_claim_text:
            errors.append(f"non_claims must include boundary phrase: {phrase}")
    return errors


def validate_summary(errors: list[str]) -> None:
    if not SUMMARY.exists():
        errors.append(f"Missing {rel(SUMMARY)}.")
        return
    text = SUMMARY.read_text(encoding="utf-8")
    required_fragments = [
        "Curated Reader Format Artifact Probe",
        "python3 scripts/render_curated_reader_formats.py --formats html epub docx --include-pdf",
        "python3 scripts/inspect_curated_reader_format_artifacts.py",
        "python3 scripts/sync_curated_reader_format_probe_manifest.py",
        "python3 scripts/repair_curated_reader_epub_links.py",
        "python3 scripts/repair_curated_reader_docx_links.py",
        "python3 scripts/audit_curated_reader_pdf_layout.py",
        "python3 scripts/audit_curated_reader_pdf_visual_raster.py",
        "python3 scripts/audit_curated_reader_epub_content.py",
        "node scripts/validate_curated_reader_epub_browser_review.js --write-manifest",
        "python3 scripts/audit_curated_reader_docx_content.py",
        "python3 scripts/validate_curated_reader_docx_libreoffice_review.py --write-manifest",
        "python3 scripts/validate_curated_reader_pdf_reading_flow.py --write-manifest",
        "python3 scripts/validate_curated_reader_pdf_viewer_review.py --write-manifest",
        "| html | rendered | 49 | 81 | 0 | 0 |",
        "| epub | rendered | 1 | 1 | 0 | 0 |",
        "| docx | rendered | 1 | 1 | 0 | 0 |",
        "| pdf | rendered | 1 | 1 | 0 | 0 |",
        "ten temporary PNG fallbacks",
        "50 temporary Chrome-screenshot Mermaid fallbacks",
        "zero SVG conversion warnings",
        "0 live-marker leaks",
        "0 raw core-claim marker leaks",
        "SHA-256 `049df485288e8f513d36212dc9c458e3815565677a62b1ba7ef61525359473d4`",
        "repaired EPUB package SHA-256 `0cde00ffdb070b12884ae1d7400c4e7dcc4321e0141956c5d9d89b434463fbda`",
        "SHA-256 `b6b719feeaf2e8195880b5ef89f355fb122d83b6c584d0b11242c67e669ed2f3`",
        "repaired DOCX package SHA-256 `d18fff6310c71b5a55ad97fcad1a8357d7d1c50480cb15d40f435d2e5e65309e`",
        "SHA-256 `491113418d68c6a830d6d194d4b0263a47f9dc994196cd62bb342773fc6f7078`",
        "506 pages",
        "sample pages 1, 2, 25, 300, and 500",
        "| Pages checked | 506 |",
        "| Word boxes checked | 170,036 |",
        "| Textless pages | 0 |",
        "| Out-of-bounds word boxes | 0 |",
        "| Layout lines over 160 characters | 0 |",
        "| Pages raster-rendered | 506 |",
        "| Blank raster pages | 0 |",
        "| Low-ink raster pages | 1 |",
        "| Near-edge raster pages | 0 |",
        "not manual PDF page-by-page review",
        "PDF Extracted Text Reading-Flow Review",
        "44 chapter headings",
        "3 appendix headings",
        "506 nonempty text pages",
        "1,104,355 text characters",
        "PDF Chromium Viewer Smoke Review",
        "Scroll-changed pixels",
        "4.434%",
        "not manual PDF page-by-page reading-flow review",
        "52 XHTML entries",
        "49 packaged content XHTML entries",
        "0 unresolved internal hrefs",
        "| XML parse errors | 0 |",
        "| Bare class attribute hits | 0 |",
        "| Paragraph-wrapped figure tag hits | 0 |",
        "EPUB Browser XHTML Application Review",
        "104 page-view pairs",
        "not dedicated e-reader device/app approval",
        "not e-reader application review",
        "17,369 paragraphs",
        "0 raw .qmd relationship targets",
        "not Word, LibreOffice GUI, or Google Docs application review",
        "DOCX LibreOffice Headless Review",
        "504 converted pages",
        "1,026,949 text characters",
        "0 blank converted-page rasters",
        "not Word review, not LibreOffice GUI review, not Google Docs review",
        "does not clear release blockers",
        "does not promote any claim support state",
    ]
    for fragment in required_fragments:
        if fragment not in text:
            errors.append(f"{rel(SUMMARY)} missing required fragment: {fragment}")


def main() -> None:
    manifest = load_json(MANIFEST)
    if not isinstance(manifest, dict):
        fail([f"{rel(MANIFEST)} must contain an object."])
    errors = validate_manifest(manifest)
    validate_summary(errors)
    if errors:
        fail(errors)
    print(
        "Curated reader format probe validation passed: html, epub, docx, pdf structural evidence recorded "
        "with raster PNG fallbacks, DOCX LibreOffice review, PDF extracted-text reading-flow review, "
        "and Chromium PDF viewer smoke review."
    )


if __name__ == "__main__":
    main()
