#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "editions" / "reader_manuscript" / "v1_0" / "manifest.json"
ASSET_README = ROOT / "assets" / "diagrams" / "README.md"
REVIEW = ROOT / "docs" / "reader_key_figure_artifact_review.md"
COMPANION_NOTE = ROOT / "editions" / "reader_manuscript" / "v1_0" / "companion_notes" / "key-figures.md"
FORMAT_PROBE_MANIFEST = ROOT / "editions" / "reader_manuscript" / "v1_0" / "key_figure_format_probe_manifest.json"
FORMAT_PROBE_DOC = ROOT / "docs" / "reader_key_figure_format_probe.md"
RASTER_PROBE_MANIFEST = ROOT / "editions" / "reader_manuscript" / "v1_0" / "key_figure_raster_manifest.json"
RASTER_PROBE_DOC = ROOT / "docs" / "reader_key_figure_raster_review.md"
EPUB_LAYOUT_MANIFEST = ROOT / "editions" / "reader_manuscript" / "v1_0" / "key_figure_epub_layout_manifest.json"
EPUB_LAYOUT_DOC = ROOT / "docs" / "reader_key_figure_epub_layout_review.md"
PDF_LAYOUT_MANIFEST = ROOT / "editions" / "reader_manuscript" / "v1_0" / "key_figure_pdf_layout_manifest.json"
PDF_LAYOUT_DOC = ROOT / "docs" / "reader_key_figure_pdf_layout_review.md"
DOCX_LAYOUT_MANIFEST = ROOT / "editions" / "reader_manuscript" / "v1_0" / "key_figure_docx_layout_manifest.json"
DOCX_LAYOUT_DOC = ROOT / "docs" / "reader_key_figure_docx_layout_review.md"

EXPECTED_COUNT = 10
BOUNDARY_PHRASES = (
    "does not prove",
    "not proof",
    "not deployed",
    "not an accepted",
    "not epub",
    "not release",
    "not a release",
    "not evidence",
    "does not promote",
    "no deployed",
    "no support-state",
)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9][A-Za-z0-9'-]*", text)


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def text_near_asset(text: str, asset_name: str, chars: int = 1500) -> str:
    index = text.find(asset_name)
    if index < 0:
        return ""
    start = max(0, index - 400)
    end = min(len(text), index + chars)
    return text[start:end]


def heading_anchor(path: Path, anchor: str) -> bool:
    text = path.read_text(encoding="utf-8", errors="ignore")
    for line in text.splitlines():
        if not line.startswith("#"):
            continue
        heading = line.lstrip("#").strip()
        slug = re.sub(r"[^a-z0-9 -]", "", heading.lower())
        slug = re.sub(r"\s+", "-", slug).strip("-")
        if slug == anchor:
            return True
    return False


def validate_svg(path: Path, owner: str, errors: list[str]) -> None:
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        errors.append(f"{owner}: {rel(path)} is not parseable SVG: {exc}.")
        return
    if not root.tag.endswith("svg"):
        errors.append(f"{owner}: {rel(path)} root is not svg.")
    if root.attrib.get("role") != "img":
        errors.append(f"{owner}: {rel(path)} must declare role='img'.")
    aria = root.attrib.get("aria-labelledby", "")
    if "title" not in aria or "desc" not in aria:
        errors.append(f"{owner}: {rel(path)} must aria-label title and desc.")
    view_box = root.attrib.get("viewBox")
    if not view_box or len(view_box.split()) != 4:
        errors.append(f"{owner}: {rel(path)} must carry a four-value viewBox.")

    title = root.find("{http://www.w3.org/2000/svg}title")
    desc = root.find("{http://www.w3.org/2000/svg}desc")
    title_text = normalize(title.text or "") if title is not None else ""
    desc_text = normalize(desc.text or "") if desc is not None else ""
    if len(words(title_text)) < 4 or "draft figure" not in title_text.lower():
        errors.append(f"{owner}: {rel(path)} title must be a substantive draft-figure title.")
    if len(words(desc_text)) < 15:
        errors.append(f"{owner}: {rel(path)} desc must be a substantive text equivalent.")
    visible_text = " ".join((node.text or "") for node in root.iter())
    if "Draft key figure" not in visible_text:
        errors.append(f"{owner}: {rel(path)} must visibly label itself as a draft key figure.")
    if "release-approved" in visible_text.lower():
        errors.append(f"{owner}: {rel(path)} must not claim release approval.")


def validate_live_surface(
    figure: dict[str, Any],
    owner: str,
    asset_name: str,
    errors: list[str],
) -> None:
    ref = figure.get("text_equivalent_ref")
    if not isinstance(ref, str) or "#" not in ref:
        errors.append(f"{owner}: text_equivalent_ref must include a path and anchor.")
        return
    text_path, anchor = ref.split("#", 1)
    path = ROOT / text_path
    if not path.exists():
        errors.append(f"{owner}: text_equivalent_ref path missing: {text_path}.")
        return
    if not heading_anchor(path, anchor):
        errors.append(f"{owner}: text_equivalent_ref anchor missing: {ref}.")
    text = path.read_text(encoding="utf-8", errors="ignore")
    if asset_name not in text:
        errors.append(f"{owner}: live chapter does not embed {asset_name}.")
        return
    window = text_near_asset(text, asset_name).lower()
    for phrase in ("fig-alt=", "how to read", "draft reader aid"):
        if phrase not in window:
            errors.append(f"{owner}: live chapter figure block missing {phrase!r}.")
    if not any(phrase in window for phrase in BOUNDARY_PHRASES):
        errors.append(f"{owner}: live chapter figure block lacks a visible non-claim boundary.")


def validate_reader_surface(
    figure: dict[str, Any],
    owner: str,
    asset_name: str,
    errors: list[str],
) -> None:
    ref = figure.get("reader_manuscript_ref")
    if not isinstance(ref, str) or "#" not in ref:
        errors.append(f"{owner}: reader_manuscript_ref must include a path and anchor.")
        return
    reader_path, anchor = ref.split("#", 1)
    path = ROOT / reader_path
    if not path.exists():
        errors.append(f"{owner}: reader_manuscript_ref path missing: {reader_path}.")
        return
    text = path.read_text(encoding="utf-8", errors="ignore")
    if f"#{anchor}" not in text:
        errors.append(f"{owner}: reader figure anchor missing: {ref}.")
    if asset_name not in text:
        errors.append(f"{owner}: reader manuscript does not embed {asset_name}.")
        return
    window = text_near_asset(text, asset_name).lower()
    for phrase in ("fig-alt=", "figure boundary:", "draft reader aid"):
        if phrase not in window:
            errors.append(f"{owner}: reader figure block missing {phrase!r}.")
    if not any(phrase in window for phrase in BOUNDARY_PHRASES):
        errors.append(f"{owner}: reader figure block lacks a visible non-claim boundary.")


def validate_review_doc(figures: list[dict[str, Any]], errors: list[str]) -> None:
    if not REVIEW.exists():
        errors.append(f"Missing {rel(REVIEW)}.")
        return
    text = REVIEW.read_text(encoding="utf-8", errors="ignore")
    required = [
        "python3 scripts/validate_reader_key_figures.py",
        "python3 scripts/validate_reader_key_figure_format_probe.py --write-manifest --write-doc",
        "python3 scripts/validate_reader_key_figure_raster_probe.py --write-manifest --write-doc",
        "python3 scripts/validate_reader_key_figure_epub_layout.py --write-manifest --write-doc",
        "python3 scripts/validate_reader_key_figure_pdf_layout.py --write-manifest --write-doc",
        "python3 scripts/validate_reader_key_figure_docx_layout.py --write-manifest --write-doc",
        "not a release approval",
        "not final figure-artifact review",
        "EPUB",
        "DOCX",
        "PDF",
        "audio",
    ]
    for phrase in required:
        if phrase not in text:
            errors.append(f"{rel(REVIEW)} missing required phrase {phrase!r}.")
    for figure in figures:
        asset = str(figure.get("draft_asset_path", ""))
        if asset and asset not in text:
            errors.append(f"{rel(REVIEW)} missing figure asset {asset}.")


def validate_format_probe(figures: list[dict[str, Any]], errors: list[str]) -> None:
    if not FORMAT_PROBE_MANIFEST.exists():
        errors.append(f"Missing {rel(FORMAT_PROBE_MANIFEST)}.")
        return
    if not FORMAT_PROBE_DOC.exists():
        errors.append(f"Missing {rel(FORMAT_PROBE_DOC)}.")
        return
    manifest = load_json(FORMAT_PROBE_MANIFEST)
    if manifest.get("schema_version") != "asi_stack.reader_key_figure_format_probe.v0":
        errors.append(f"{rel(FORMAT_PROBE_MANIFEST)} schema_version drifted.")
    if manifest.get("status") != "passed_local_format_package_probe":
        errors.append(f"{rel(FORMAT_PROBE_MANIFEST)} status must be passed_local_format_package_probe.")
    if manifest.get("figure_count") != len(figures):
        errors.append(f"{rel(FORMAT_PROBE_MANIFEST)} figure_count must match key_figure_targets.")
    expected = {
        ("epub", "svg_entries"): 10,
        ("epub", "matched_source_svg_titles"): 10,
        ("epub", "figure_boundary_paragraphs"): 10,
        ("docx", "matched_figure_stems"): 10,
        ("docx", "figure_boundary_paragraphs"): 10,
        ("pdf", "figure_boundary_paragraphs"): 10,
        ("pdf", "matched_caption_titles"): 10,
    }
    for (section, key), value in expected.items():
        observed = manifest.get(section, {}).get(key)
        if observed != value:
            errors.append(f"{rel(FORMAT_PROBE_MANIFEST)} {section}.{key} must be {value}, found {observed}.")
    blockers = set(manifest.get("release_blockers_preserved", []))
    for blocker in (
        "final_figure_artifact_review_not_completed",
        "epub_e_reader_review_not_completed",
        "docx_application_review_not_completed",
        "pdf_page_layout_review_not_completed",
        "reader_edition_release_record_not_created",
    ):
        if blocker not in blockers:
            errors.append(f"{rel(FORMAT_PROBE_MANIFEST)} missing blocker {blocker}.")
    doc_text = FORMAT_PROBE_DOC.read_text(encoding="utf-8", errors="ignore")
    for phrase in (
        "not final figure-artifact approval",
        "EPUB still needs real e-reader",
        "DOCX still needs Word",
        "PDF still needs manual page-level layout",
        "does not approve final figure art",
    ):
        if phrase not in doc_text:
            errors.append(f"{rel(FORMAT_PROBE_DOC)} missing required phrase {phrase!r}.")


def validate_raster_probe(figures: list[dict[str, Any]], errors: list[str]) -> None:
    if not RASTER_PROBE_MANIFEST.exists():
        errors.append(f"Missing {rel(RASTER_PROBE_MANIFEST)}.")
        return
    if not RASTER_PROBE_DOC.exists():
        errors.append(f"Missing {rel(RASTER_PROBE_DOC)}.")
        return
    manifest = load_json(RASTER_PROBE_MANIFEST)
    if manifest.get("schema_version") != "asi_stack.reader_key_figure_raster_probe.v0":
        errors.append(f"{rel(RASTER_PROBE_MANIFEST)} schema_version drifted.")
    if manifest.get("status") != "passed_local_raster_artifact_probe":
        errors.append(f"{rel(RASTER_PROBE_MANIFEST)} status must be passed_local_raster_artifact_probe.")
    summary = manifest.get("summary", {})
    if not isinstance(summary, dict):
        errors.append(f"{rel(RASTER_PROBE_MANIFEST)} summary must be an object.")
        summary = {}
    expected = {
        "figure_count": len(figures),
        "raster_artifact_count": 10,
        "standard_dimension_count": 10,
        "maximum_transparent_pixel_count": 420,
    }
    for key, value in expected.items():
        observed = summary.get(key)
        if observed != value:
            errors.append(f"{rel(RASTER_PROBE_MANIFEST)} summary.{key} must be {value}, found {observed}.")
    thresholds = {
        "minimum_opaque_pixel_percent": 99.9,
        "minimum_luminance_std": 25.0,
        "minimum_quantized_color_count": 100,
        "minimum_dark_pixel_percent": 0.4,
        "minimum_mid_tone_pixel_percent": 5.0,
    }
    for key, threshold in thresholds.items():
        observed = summary.get(key)
        if not isinstance(observed, (int, float)) or observed < threshold:
            errors.append(f"{rel(RASTER_PROBE_MANIFEST)} summary.{key} must be at least {threshold}.")
    doc_text = RASTER_PROBE_DOC.read_text(encoding="utf-8", errors="ignore")
    for phrase in (
        "Reader Key-Figure Raster Review",
        "| Raster artifacts checked | 10 |",
        "| Standard dimensions | 10 |",
        "not manual aesthetic review",
        "not final figure-artifact approval",
        "not reader release approval",
    ):
        if phrase not in doc_text:
            errors.append(f"{rel(RASTER_PROBE_DOC)} missing required phrase {phrase!r}.")


def validate_pdf_layout_probe(figures: list[dict[str, Any]], errors: list[str]) -> None:
    if not PDF_LAYOUT_MANIFEST.exists():
        errors.append(f"Missing {rel(PDF_LAYOUT_MANIFEST)}.")
        return
    if not PDF_LAYOUT_DOC.exists():
        errors.append(f"Missing {rel(PDF_LAYOUT_DOC)}.")
        return
    manifest = load_json(PDF_LAYOUT_MANIFEST)
    if manifest.get("schema_version") != "asi_stack.reader_key_figure_pdf_layout.v0":
        errors.append(f"{rel(PDF_LAYOUT_MANIFEST)} schema_version drifted.")
    if manifest.get("status") != "passed_local_pdf_key_figure_layout_probe":
        errors.append(f"{rel(PDF_LAYOUT_MANIFEST)} status must be passed_local_pdf_key_figure_layout_probe.")
    summary = manifest.get("summary", {})
    if not isinstance(summary, dict):
        errors.append(f"{rel(PDF_LAYOUT_MANIFEST)} summary must be an object.")
        summary = {}
    expected = {
        "figure_count": len(figures),
        "pdf_pages": 506,
        "unique_caption_pages": 10,
        "raster_pages_rendered": 10,
        "standard_page_size_count": 10,
        "maximum_near_edge_ink_percent": 0.0,
    }
    for key, value in expected.items():
        observed = summary.get(key)
        if observed != value:
            errors.append(f"{rel(PDF_LAYOUT_MANIFEST)} summary.{key} must be {value}, found {observed}.")
    thresholds = {
        "minimum_caption_margin_pt": 72.0,
        "minimum_page_ink_percent": 3.0,
        "minimum_luminance_std": 14.0,
    }
    for key, threshold in thresholds.items():
        observed = summary.get(key)
        if not isinstance(observed, (int, float)) or observed < threshold:
            errors.append(f"{rel(PDF_LAYOUT_MANIFEST)} summary.{key} must be at least {threshold}.")
    doc_text = PDF_LAYOUT_DOC.read_text(encoding="utf-8", errors="ignore")
    for phrase in (
        "Reader Key-Figure PDF Layout Review",
        "| Key-figure caption pages | 10 |",
        "| Raster pages rendered | 10 |",
        "not manual page-by-page PDF review",
        "not final figure-artifact approval",
        "not reader release approval",
    ):
        if phrase not in doc_text:
            errors.append(f"{rel(PDF_LAYOUT_DOC)} missing required phrase {phrase!r}.")


def validate_epub_layout_probe(figures: list[dict[str, Any]], errors: list[str]) -> None:
    if not EPUB_LAYOUT_MANIFEST.exists():
        errors.append(f"Missing {rel(EPUB_LAYOUT_MANIFEST)}.")
        return
    if not EPUB_LAYOUT_DOC.exists():
        errors.append(f"Missing {rel(EPUB_LAYOUT_DOC)}.")
        return
    manifest = load_json(EPUB_LAYOUT_MANIFEST)
    if manifest.get("schema_version") != "asi_stack.reader_key_figure_epub_layout.v0":
        errors.append(f"{rel(EPUB_LAYOUT_MANIFEST)} schema_version drifted.")
    if manifest.get("status") != "passed_local_epub_key_figure_xhtml_layout_probe":
        errors.append(f"{rel(EPUB_LAYOUT_MANIFEST)} status must be passed_local_epub_key_figure_xhtml_layout_probe.")
    summary = manifest.get("summary", {})
    if not isinstance(summary, dict):
        errors.append(f"{rel(EPUB_LAYOUT_MANIFEST)} summary must be an object.")
        summary = {}
    expected = {
        "figure_count": len(figures),
        "unique_xhtml_entries": 10,
        "viewport_count": 2,
        "page_view_pairs": 20,
        "failed_page_view_pairs": 0,
        "maximum_horizontal_overflow_px": 10,
        "minimum_image_count": 1,
        "image_failure_count": 0,
        "figure_boundary_count": 10,
        "release_boundary_count": 10,
    }
    for key, value in expected.items():
        observed = summary.get(key)
        if observed != value:
            errors.append(f"{rel(EPUB_LAYOUT_MANIFEST)} summary.{key} must be {value}, found {observed}.")
    thresholds = {
        "minimum_body_text_chars": 1_200,
        "minimum_alt_text_words": 12,
    }
    for key, threshold in thresholds.items():
        observed = summary.get(key)
        if not isinstance(observed, (int, float)) or observed < threshold:
            errors.append(f"{rel(EPUB_LAYOUT_MANIFEST)} summary.{key} must be at least {threshold}.")
    doc_text = EPUB_LAYOUT_DOC.read_text(encoding="utf-8", errors="ignore")
    for phrase in (
        "Reader Key-Figure EPUB Layout Review",
        "| Key-figure XHTML entries | 10 |",
        "| Browser page-view pairs | 20 |",
        "| Failed page-view pairs | 0 |",
        "not dedicated e-reader device review",
        "not e-reader application approval",
        "not final figure-artifact approval",
        "not reader release approval",
    ):
        if phrase not in doc_text:
            errors.append(f"{rel(EPUB_LAYOUT_DOC)} missing required phrase {phrase!r}.")


def validate_docx_layout_probe(figures: list[dict[str, Any]], errors: list[str]) -> None:
    if not DOCX_LAYOUT_MANIFEST.exists():
        errors.append(f"Missing {rel(DOCX_LAYOUT_MANIFEST)}.")
        return
    if not DOCX_LAYOUT_DOC.exists():
        errors.append(f"Missing {rel(DOCX_LAYOUT_DOC)}.")
        return
    manifest = load_json(DOCX_LAYOUT_MANIFEST)
    if manifest.get("schema_version") != "asi_stack.reader_key_figure_docx_layout.v0":
        errors.append(f"{rel(DOCX_LAYOUT_MANIFEST)} schema_version drifted.")
    if manifest.get("status") != "passed_local_docx_key_figure_layout_probe":
        errors.append(f"{rel(DOCX_LAYOUT_MANIFEST)} status must be passed_local_docx_key_figure_layout_probe.")
    summary = manifest.get("summary", {})
    if not isinstance(summary, dict):
        errors.append(f"{rel(DOCX_LAYOUT_MANIFEST)} summary must be an object.")
        summary = {}
    expected = {
        "figure_count": len(figures),
        "docx_converted_pdf_pages": 504,
        "unique_title_pages": 10,
        "raster_pages_rendered": 10,
        "standard_page_size_count": 10,
        "minimum_title_margin_pt": 72.1,
        "maximum_near_edge_ink_percent": 0.0,
    }
    for key, value in expected.items():
        observed = summary.get(key)
        if observed != value:
            errors.append(f"{rel(DOCX_LAYOUT_MANIFEST)} summary.{key} must be {value}, found {observed}.")
    thresholds = {
        "minimum_page_ink_percent": 9.0,
        "minimum_luminance_std": 37.0,
    }
    for key, threshold in thresholds.items():
        observed = summary.get(key)
        if not isinstance(observed, (int, float)) or observed < threshold:
            errors.append(f"{rel(DOCX_LAYOUT_MANIFEST)} summary.{key} must be at least {threshold}.")
    doc_text = DOCX_LAYOUT_DOC.read_text(encoding="utf-8", errors="ignore")
    for phrase in (
        "Reader Key-Figure DOCX Layout Review",
        "| Key-figure title pages | 10 |",
        "| Raster pages rendered | 10 |",
        "not Word review",
        "not LibreOffice GUI review",
        "not Google Docs review",
        "not manual document review",
        "not final figure-artifact approval",
        "not reader release approval",
    ):
        if phrase not in doc_text:
            errors.append(f"{rel(DOCX_LAYOUT_DOC)} missing required phrase {phrase!r}.")


def validate_companion_note(figures: list[dict[str, Any]], errors: list[str]) -> None:
    if not COMPANION_NOTE.exists():
        errors.append(f"Missing {rel(COMPANION_NOTE)}.")
        return
    text = COMPANION_NOTE.read_text(encoding="utf-8", errors="ignore")
    lower = text.lower()
    required = [
        "Status: drafting companion note, not release reviewed.",
        "## Spoken Figure Summaries",
        "## Audio Treatment",
        "## E-Reader Treatment",
        "not final figure-artifact approval",
        "not EPUB, DOCX, PDF, HTML, e-reader, MP3, M4B, or",
        "does not promote any chapter core claim",
    ]
    for phrase in required:
        if phrase not in text:
            errors.append(f"{rel(COMPANION_NOTE)} missing required phrase {phrase!r}.")
    for figure in figures:
        asset = str(figure.get("draft_asset_path", ""))
        title = str(figure.get("working_title", ""))
        if asset and asset not in text:
            errors.append(f"{rel(COMPANION_NOTE)} missing figure asset {asset}.")
        if title and title not in text:
            errors.append(f"{rel(COMPANION_NOTE)} missing figure title {title!r}.")
    if lower.count("does not prove") < 6:
        errors.append(f"{rel(COMPANION_NOTE)} must preserve repeated non-proof boundaries.")


def main() -> None:
    errors: list[str] = []
    manifest = load_json(MANIFEST)
    figures = manifest.get("reader_handoff_contract", {}).get("key_figure_targets")
    if not isinstance(figures, list) or len(figures) != EXPECTED_COUNT:
        errors.append(
            f"reader_handoff_contract.key_figure_targets must contain exactly {EXPECTED_COUNT} records."
        )
        figures = []

    asset_readme = ASSET_README.read_text(encoding="utf-8", errors="ignore") if ASSET_README.exists() else ""
    seen: set[str] = set()
    for index, figure in enumerate(figures):
        owner = f"key_figure_targets[{index}]"
        if not isinstance(figure, dict):
            errors.append(f"{owner}: figure record must be an object.")
            continue
        figure_id = figure.get("id")
        if not isinstance(figure_id, str) or not figure_id:
            errors.append(f"{owner}: id must be non-empty.")
        elif figure_id in seen:
            errors.append(f"{owner}: duplicate figure id {figure_id}.")
        else:
            seen.add(figure_id)
        if figure.get("status") != "target_defined_not_final_art":
            errors.append(f"{owner}: status must remain target_defined_not_final_art.")
        if figure.get("draft_artifact_state") != "draft_not_release_reviewed":
            errors.append(f"{owner}: draft_artifact_state must remain draft_not_release_reviewed.")
        boundary = str(figure.get("release_boundary", "")).lower()
        if "not a completed figure" not in boundary or "not reviewed as a release artifact" not in boundary:
            errors.append(f"{owner}: release_boundary must preserve no-release-review boundary.")
        asset = figure.get("draft_asset_path")
        if not isinstance(asset, str) or not asset.startswith("assets/diagrams/") or not asset.endswith(".svg"):
            errors.append(f"{owner}: draft_asset_path must be an assets/diagrams/*.svg path.")
            continue
        path = ROOT / asset
        asset_name = Path(asset).name
        if not path.exists():
            errors.append(f"{owner}: draft SVG missing: {asset}.")
            continue
        if asset not in asset_readme:
            errors.append(f"{owner}: {asset} missing from {rel(ASSET_README)}.")
        validate_svg(path, owner, errors)
        validate_live_surface(figure, owner, asset_name, errors)
        validate_reader_surface(figure, owner, asset_name, errors)

    validate_review_doc(figures, errors)
    validate_format_probe(figures, errors)
    validate_raster_probe(figures, errors)
    validate_epub_layout_probe(figures, errors)
    validate_pdf_layout_probe(figures, errors)
    validate_docx_layout_probe(figures, errors)
    validate_companion_note(figures, errors)
    if errors:
        print("Reader key-figure validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)
    print(
        "Reader key-figure validation passed: "
        f"{len(figures)} draft SVG assets checked for metadata, live placement, "
        "reader placement, alt text, captions, and non-claim boundaries."
    )


if __name__ == "__main__":
    main()
