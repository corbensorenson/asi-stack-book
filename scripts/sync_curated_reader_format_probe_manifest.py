#!/usr/bin/env python3
"""Refresh the curated-reader format probe manifest from local render reports."""

from __future__ import annotations

from datetime import date
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "editions" / "reader_manuscript" / "v1_0" / "curated_format_probe_manifest.json"
RENDER_REPORT = ROOT / "build" / "curated_reader_edition" / "curated_reader_render_report.json"
INSPECTION_REPORT = ROOT / "build" / "curated_reader_edition" / "curated_reader_artifact_inspection_report.json"
SYNC_COMMAND = "python3 scripts/sync_curated_reader_format_probe_manifest.py"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def render_summary(report: dict[str, Any]) -> dict[str, Any]:
    summary: dict[str, Any] = {}
    for record in report.get("format_results", []):
        if not isinstance(record, dict):
            continue
        fmt = record.get("format")
        if not isinstance(fmt, str):
            continue
        row: dict[str, Any] = {
            "status": record.get("status"),
            "artifacts_observed": len(record.get("artifacts", [])),
            "preserved_artifacts": len(record.get("preserved_artifacts", [])),
            "warning_count": record.get("warning_count"),
            "svg_conversion_warning_count": record.get("svg_conversion_warning_count"),
        }
        raster = record.get("raster_diagram_fallbacks", {})
        if isinstance(raster, dict) and raster.get("applied"):
            row["png_fallback_count"] = raster.get("fallback_count")
            row["png_fallback_converter"] = raster.get("converter")
        mermaid = record.get("pdf_mermaid_static_fallbacks", {})
        if fmt == "pdf" and isinstance(mermaid, dict) and mermaid.get("applied"):
            row["pdf_mermaid_fallback_count"] = mermaid.get("fallback_count")
            row["pdf_mermaid_fallback_converter"] = mermaid.get("converter")
            row["pdf_mermaid_rewritten_files"] = mermaid.get("rewritten_files")
        summary[fmt] = row
    return summary


def inspection_summary(report: dict[str, Any]) -> dict[str, Any]:
    formats = report.get("formats", {})
    if not isinstance(formats, dict):
        return {}
    summary: dict[str, Any] = {}
    html = formats.get("html", {})
    if isinstance(html, dict):
        summary["html"] = {
            "status": html.get("status"),
            "html_files": html.get("html_files"),
            "site_html_files": html.get("site_html_files"),
            "chapter_files": html.get("chapter_files"),
            "checked_files_for_live_marker_leaks": html.get("checked_files_for_live_marker_leaks"),
            "live_marker_leaks": html.get("live_marker_leaks"),
            "raw_core_claim_marker_leaks": html.get("raw_core_claim_marker_leaks"),
        }
    epub = formats.get("epub", {})
    if isinstance(epub, dict):
        summary["epub"] = {
            "status": epub.get("status"),
            "bytes": epub.get("bytes"),
            "sha256": epub.get("sha256"),
            "entries": epub.get("entries"),
            "xhtml_entries": epub.get("xhtml_entries"),
            "image_entries": epub.get("image_entries"),
            "opf_title": epub.get("opf_title"),
            "opf_creator": epub.get("opf_creator"),
            "opf_language": epub.get("opf_language"),
            "opf_item_count": epub.get("opf_item_count"),
            "opf_itemref_count": epub.get("opf_itemref_count"),
            "nav_href_count": epub.get("nav_href_count"),
            "required_entries_present": epub.get("required_entries"),
        }
    docx = formats.get("docx", {})
    if isinstance(docx, dict):
        summary["docx"] = {
            "status": docx.get("status"),
            "bytes": docx.get("bytes"),
            "sha256": docx.get("sha256"),
            "entries": docx.get("entries"),
            "media_entries": docx.get("media_entries"),
            "png_media_entries": docx.get("png_media_entries"),
            "svg_media_entries": docx.get("svg_media_entries"),
            "paragraph_markers": docx.get("paragraph_markers"),
            "required_entries_present": docx.get("required_entries"),
        }
    pdf = formats.get("pdf", {})
    if isinstance(pdf, dict):
        summary["pdf"] = {
            "status": pdf.get("status"),
            "bytes": pdf.get("bytes"),
            "sha256": pdf.get("sha256"),
            "pages": pdf.get("pages"),
            "title": pdf.get("title"),
            "author": pdf.get("author"),
            "producer": pdf.get("producer"),
            "page_size": pdf.get("page_size"),
            "encrypted": pdf.get("encrypted"),
            "sample_pages": pdf.get("sample_pages"),
            "sample_page_pngs": pdf.get("sample_page_pngs"),
            "required_text_markers": pdf.get("required_text_markers"),
        }
    return summary


def main() -> None:
    for path in (MANIFEST, RENDER_REPORT, INSPECTION_REPORT):
        if not path.exists():
            raise SystemExit(f"Missing required file: {path.relative_to(ROOT)}")

    manifest = load_json(MANIFEST)
    render_report = load_json(RENDER_REPORT)
    inspection_report = load_json(INSPECTION_REPORT)
    if not isinstance(manifest, dict) or not isinstance(render_report, dict) or not isinstance(inspection_report, dict):
        raise SystemExit("Manifest and local reports must contain JSON objects.")

    manifest["last_updated"] = date.today().isoformat()
    source_commands = manifest.setdefault("source_commands", [])
    if isinstance(source_commands, list) and SYNC_COMMAND not in source_commands:
        source_commands.insert(2, SYNC_COMMAND)
    manifest["render_summary"] = render_summary(render_report)
    manifest["inspection_summary"] = inspection_summary(inspection_report)

    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(
        "Curated reader format probe manifest synced: "
        f"{len(manifest['render_summary'])} render formats, "
        f"{len(manifest['inspection_summary'])} inspection formats."
    )


if __name__ == "__main__":
    main()
