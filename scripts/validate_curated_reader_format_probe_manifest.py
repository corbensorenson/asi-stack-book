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
    "python3 scripts/render_curated_reader_formats.py --formats html epub docx pdf",
    "python3 scripts/inspect_curated_reader_format_artifacts.py",
}
REQUIRED_BLOCKERS = {
    "curated_reconciliation_not_approved",
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
    require_string("manifest", "review_decision", manifest.get("review_decision"), errors, min_words=20)

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
    if not isinstance(render_summary, dict):
        errors.append("render_summary must be an object.")
        render_summary = {}
    if not isinstance(inspection_summary, dict):
        errors.append("inspection_summary must be an object.")
        inspection_summary = {}
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
        if pdf.get("pages") != 519:
            errors.append("inspection_summary.pdf.pages must be 519.")
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
        "python3 scripts/render_curated_reader_formats.py --formats html epub docx pdf",
        "python3 scripts/inspect_curated_reader_format_artifacts.py",
        "| html | rendered | 49 | 81 | 0 | 0 |",
        "| epub | rendered | 1 | 1 | 0 | 0 |",
        "| docx | rendered | 1 | 1 | 0 | 0 |",
        "| pdf | rendered | 1 | 1 | 0 | 0 |",
        "ten temporary PNG fallbacks",
        "zero SVG conversion warnings",
        "0 live-marker leaks",
        "0 raw core-claim marker leaks",
        "SHA-256 `7e6904651c2d0eda7df0305ded9e91c790ab02a88574b8bd2183cf5f562cf7d5`",
        "SHA-256 `e34b3bdcdc0fa61059258b517a8aa52743dc0f92be4d77e29bc316ae63d7de92`",
        "SHA-256 `99ab0aa1fdf1d7b999bc85b5832889cc7265e052f8b8e5fecefbf4c0eb3e909d`",
        "519 pages",
        "sample pages 1, 2, 25, 300, and 500",
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
    print("Curated reader format probe validation passed: html, epub, docx, pdf structural evidence recorded with raster PNG fallbacks.")


if __name__ == "__main__":
    main()
