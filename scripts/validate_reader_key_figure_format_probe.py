#!/usr/bin/env python3
"""Validate key-figure survival across curated reader EPUB, DOCX, and PDF probes."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
READER_MANIFEST = ROOT / "editions" / "reader_manuscript" / "v1_0" / "manifest.json"
FORMAT_PROBE = ROOT / "editions" / "reader_manuscript" / "v1_0" / "curated_format_probe_manifest.json"
RESULT = ROOT / "editions" / "reader_manuscript" / "v1_0" / "key_figure_format_probe_manifest.json"
DOC = ROOT / "docs" / "reader_key_figure_format_probe.md"
EPUB = ROOT / "build" / "curated_reader_edition" / "format_artifacts" / "epub" / "_reader_site" / "The-ASI-Stack.epub"
DOCX = ROOT / "build" / "curated_reader_edition" / "format_artifacts" / "docx" / "_reader_site" / "The-ASI-Stack.docx"
PDF = ROOT / "build" / "curated_reader_edition" / "format_artifacts" / "pdf" / "_reader_site" / "The-ASI-Stack.pdf"
EXPECTED_COUNT = 10
SHA_RE = re.compile(r"^[0-9a-f]{64}$")
WORD_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9'-]*")
DOCX_REL_RE = re.compile(r"""<Relationship\b([^>]*)/>""")
DOCX_ATTR_RE = re.compile(r"""([A-Za-z_:]+)=["']([^"']*)["']""")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Reader key-figure format probe validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def words(text: str) -> list[str]:
    return WORD_RE.findall(text)


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().casefold()


def normalize_words(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.casefold()).strip()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def extract_svg_title_desc(path: Path) -> tuple[str, str]:
    root = ET.parse(path).getroot()
    ns = "{http://www.w3.org/2000/svg}"
    title = root.find(ns + "title")
    desc = root.find(ns + "desc")
    return (
        re.sub(r"\s+", " ", title.text or "").strip() if title is not None else "",
        re.sub(r"\s+", " ", desc.text or "").strip() if desc is not None else "",
    )


def key_figures() -> list[dict[str, Any]]:
    manifest = load_json(READER_MANIFEST)
    figures = manifest.get("reader_handoff_contract", {}).get("key_figure_targets", [])
    if not isinstance(figures, list) or len(figures) != EXPECTED_COUNT:
        fail(["reader_handoff_contract.key_figure_targets must contain exactly 10 records."])
    rows: list[dict[str, Any]] = []
    for figure in figures:
        if not isinstance(figure, dict):
            fail(["key_figure_targets entries must be objects."])
        asset = str(figure.get("draft_asset_path", ""))
        path = ROOT / asset
        if not path.exists():
            fail([f"missing key-figure asset: {asset}"])
        title, desc = extract_svg_title_desc(path)
        rows.append(
            {
                "id": figure.get("id"),
                "asset": asset,
                "asset_name": path.name,
                "asset_stem": path.stem,
                "source_svg_title": title,
                "source_svg_desc_words": len(words(desc)),
                "pdf_caption_title": re.sub(r"\s+draft figure$", "", title, flags=re.IGNORECASE),
            }
        )
    return rows


def strip_xml(text: str) -> str:
    return re.sub(r"<[^>]+>", " ", text)


def docx_relationships(rels_xml: str) -> list[dict[str, str]]:
    return [dict(DOCX_ATTR_RE.findall(match.group(1))) for match in DOCX_REL_RE.finditer(rels_xml)]


def inspect_epub(figures: list[dict[str, Any]]) -> dict[str, Any]:
    if not EPUB.exists():
        fail([f"missing EPUB artifact: {rel(EPUB)}"])
    with ZipFile(EPUB) as archive:
        names = archive.namelist()
        svg_entries = sorted(name for name in names if name.endswith(".svg"))
        xhtml_text = "\n".join(
            archive.read(name).decode("utf-8", errors="replace")
            for name in names
            if name.endswith(".xhtml")
        )
        packaged_titles: dict[str, dict[str, Any]] = {}
        for name in svg_entries:
            text = archive.read(name).decode("utf-8", errors="replace")
            try:
                root = ET.fromstring(text)
            except ET.ParseError:
                continue
            ns = "{http://www.w3.org/2000/svg}"
            title = root.find(ns + "title")
            desc = root.find(ns + "desc")
            title_text = re.sub(r"\s+", " ", title.text or "").strip() if title is not None else ""
            desc_text = re.sub(r"\s+", " ", desc.text or "").strip() if desc is not None else ""
            packaged_titles[normalize(title_text)] = {
                "entry": name,
                "title": title_text,
                "desc_words": len(words(desc_text)),
            }

    per_figure: list[dict[str, Any]] = []
    for figure in figures:
        packaged = packaged_titles.get(normalize(str(figure["source_svg_title"])))
        per_figure.append(
            {
                "id": figure["id"],
                "source_svg_title": figure["source_svg_title"],
                "packaged_svg_entry": packaged.get("entry") if packaged else "",
                "packaged_desc_words": packaged.get("desc_words", 0) if packaged else 0,
                "matched": packaged is not None,
            }
        )
    return {
        "artifact": rel(EPUB),
        "sha256": sha256_file(EPUB),
        "svg_entries": len(svg_entries),
        "matched_source_svg_titles": sum(1 for row in per_figure if row["matched"]),
        "min_packaged_desc_words": min(row["packaged_desc_words"] for row in per_figure),
        "figure_boundary_paragraphs": xhtml_text.count("Figure boundary"),
        "draft_reader_aid_mentions": xhtml_text.lower().count("draft reader aid"),
        "per_figure": per_figure,
    }


def inspect_docx(figures: list[dict[str, Any]]) -> dict[str, Any]:
    if not DOCX.exists():
        fail([f"missing DOCX artifact: {rel(DOCX)}"])
    with ZipFile(DOCX) as archive:
        names = archive.namelist()
        document_xml = archive.read("word/document.xml").decode("utf-8", errors="replace")
        rels_xml = archive.read("word/_rels/document.xml.rels").decode("utf-8", errors="replace")
        relationships = docx_relationships(rels_xml)
        media = [name for name in names if name.startswith("word/media/")]
    per_figure = [
        {
            "id": figure["id"],
            "asset_stem": figure["asset_stem"],
            "stem_in_document_xml": figure["asset_stem"] in document_xml,
        }
        for figure in figures
    ]
    return {
        "artifact": rel(DOCX),
        "sha256": sha256_file(DOCX),
        "media_entries": len(media),
        "png_media_entries": sum(1 for name in media if name.lower().endswith(".png")),
        "svg_media_entries": sum(1 for name in media if name.lower().endswith(".svg")),
        "relationship_count": len(relationships),
        "raw_qmd_relationship_targets": sum(1 for row in relationships if ".qmd" in row.get("Target", "")),
        "matched_figure_stems": sum(1 for row in per_figure if row["stem_in_document_xml"]),
        "figure_boundary_paragraphs": document_xml.count("Figure boundary"),
        "draft_reader_aid_mentions": document_xml.lower().count("draft reader aid"),
        "per_figure": per_figure,
    }


def inspect_pdf(figures: list[dict[str, Any]]) -> dict[str, Any]:
    if not PDF.exists():
        fail([f"missing PDF artifact: {rel(PDF)}"])
    result = subprocess.run(["pdftotext", str(PDF), "-"], check=True, text=True, stdout=subprocess.PIPE)
    text = result.stdout
    normalized_text = normalize_words(text)
    per_figure = [
        {
            "id": figure["id"],
            "caption_title": figure["pdf_caption_title"],
            "caption_title_present": normalize_words(f"Draft {figure['pdf_caption_title']}") in normalized_text,
        }
        for figure in figures
    ]
    return {
        "artifact": rel(PDF),
        "sha256": sha256_file(PDF),
        "figure_boundary_paragraphs": text.count("Figure boundary"),
        "draft_caption_count": len(re.findall(r"Figure \d+\.\d+: Draft", text)),
        "matched_caption_titles": sum(1 for row in per_figure if row["caption_title_present"]),
        "does_not_prove_mentions": text.count("does not prove"),
        "per_figure": per_figure,
    }


def observe() -> dict[str, Any]:
    figures = key_figures()
    return {
        "schema_version": "asi_stack.reader_key_figure_format_probe.v0",
        "status": "passed_local_format_package_probe",
        "source_manifest": rel(READER_MANIFEST),
        "format_probe_manifest": rel(FORMAT_PROBE),
        "figure_count": len(figures),
        "epub": inspect_epub(figures),
        "docx": inspect_docx(figures),
        "pdf": inspect_pdf(figures),
        "release_blockers_preserved": [
            "final_figure_artifact_review_not_completed",
            "epub_e_reader_review_not_completed",
            "docx_application_review_not_completed",
            "pdf_page_layout_review_not_completed",
            "reader_edition_release_record_not_created",
        ],
        "non_claims": [
            "This is a local package/text probe for draft key figures only.",
            "This probe is not final figure-artifact approval.",
            "This probe is not EPUB approval, not DOCX approval, not PDF approval, not e-reader approval, not audio approval, not HTML approval, and not reader release approval.",
            "This probe does not prove visual quality, accessibility adequacy, narration quality, model behavior, deployed runtime behavior, evidence transitions, or support-state promotion.",
        ],
    }


def validate_result(result: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if result.get("schema_version") != "asi_stack.reader_key_figure_format_probe.v0":
        errors.append("schema_version must be asi_stack.reader_key_figure_format_probe.v0.")
    if result.get("status") != "passed_local_format_package_probe":
        errors.append("status must be passed_local_format_package_probe.")
    if result.get("figure_count") != 10:
        errors.append("figure_count must be 10.")

    epub = result.get("epub", {})
    if not isinstance(epub, dict):
        errors.append("epub must be an object.")
        epub = {}
    expected_epub = {
        "svg_entries": 10,
        "matched_source_svg_titles": 10,
        "figure_boundary_paragraphs": 10,
        "draft_reader_aid_mentions": 10,
    }
    for key, value in expected_epub.items():
        if epub.get(key) != value:
            errors.append(f"epub.{key} must be {value}.")
    if int(epub.get("min_packaged_desc_words", 0)) < 15:
        errors.append("epub.min_packaged_desc_words must be at least 15.")
    if not SHA_RE.match(str(epub.get("sha256", ""))):
        errors.append("epub.sha256 must be a SHA-256 digest.")
    for row in epub.get("per_figure", []):
        if not row.get("matched") or not row.get("packaged_svg_entry"):
            errors.append(f"epub figure row did not match packaged SVG: {row}")

    docx = result.get("docx", {})
    if not isinstance(docx, dict):
        errors.append("docx must be an object.")
        docx = {}
    expected_docx = {
        "media_entries": 61,
        "png_media_entries": 61,
        "svg_media_entries": 0,
        "raw_qmd_relationship_targets": 0,
        "matched_figure_stems": 10,
        "figure_boundary_paragraphs": 10,
        "draft_reader_aid_mentions": 10,
    }
    for key, value in expected_docx.items():
        if docx.get(key) != value:
            errors.append(f"docx.{key} must be {value}.")
    if int(docx.get("relationship_count", 0)) < 250:
        errors.append("docx.relationship_count must be at least 250.")
    if not SHA_RE.match(str(docx.get("sha256", ""))):
        errors.append("docx.sha256 must be a SHA-256 digest.")
    for row in docx.get("per_figure", []):
        if not row.get("stem_in_document_xml"):
            errors.append(f"docx figure row missing stem in document XML: {row}")

    pdf = result.get("pdf", {})
    if not isinstance(pdf, dict):
        errors.append("pdf must be an object.")
        pdf = {}
    expected_pdf = {
        "figure_boundary_paragraphs": 10,
        "draft_caption_count": 10,
        "matched_caption_titles": 10,
    }
    for key, value in expected_pdf.items():
        if pdf.get(key) != value:
            errors.append(f"pdf.{key} must be {value}.")
    if int(pdf.get("does_not_prove_mentions", 0)) < 10:
        errors.append("pdf.does_not_prove_mentions must be at least 10.")
    if not SHA_RE.match(str(pdf.get("sha256", ""))):
        errors.append("pdf.sha256 must be a SHA-256 digest.")
    for row in pdf.get("per_figure", []):
        if not row.get("caption_title_present"):
            errors.append(f"pdf figure row missing caption title: {row}")

    blockers = set(result.get("release_blockers_preserved", []))
    for blocker in {
        "final_figure_artifact_review_not_completed",
        "epub_e_reader_review_not_completed",
        "docx_application_review_not_completed",
        "pdf_page_layout_review_not_completed",
        "reader_edition_release_record_not_created",
    }:
        if blocker not in blockers:
            errors.append(f"release_blockers_preserved missing {blocker}.")
    non_claim_text = " ".join(str(item) for item in result.get("non_claims", [])).lower()
    for phrase in ("not final figure-artifact approval", "not epub", "not docx", "not pdf", "does not prove"):
        if phrase not in non_claim_text:
            errors.append(f"non_claims missing boundary phrase: {phrase}")
    return errors


def write_doc(result: dict[str, Any]) -> None:
    lines = [
        "# Reader Key-Figure Format Probe",
        "",
        "Last checked: 2026-07-04",
        "",
        "Command:",
        "",
        "```bash",
        "python3 scripts/validate_reader_key_figure_format_probe.py --write-manifest --write-doc",
        "```",
        "",
        "This probe inspects the current ignored curated-reader EPUB, DOCX, and PDF artifacts for the ten draft key figures. It checks package/text survival only: packaged SVG titles in EPUB, rasterized figure IDs and boundaries in DOCX, and extracted captions and figure-boundary paragraphs in PDF. It is not final figure-artifact approval, not e-reader review, not application review, not manual PDF review, and not reader release approval.",
        "",
        "## Summary",
        "",
        "| Format | Checks | Result |",
        "|---|---|---:|",
        f"| EPUB | packaged SVG entries | {result['epub']['svg_entries']} |",
        f"| EPUB | matched source SVG titles | {result['epub']['matched_source_svg_titles']} |",
        f"| EPUB | figure-boundary paragraphs | {result['epub']['figure_boundary_paragraphs']} |",
        f"| DOCX | PNG media entries | {result['docx']['png_media_entries']} |",
        f"| DOCX | matched figure stems | {result['docx']['matched_figure_stems']} |",
        f"| DOCX | raw `.qmd` relationship targets | {result['docx']['raw_qmd_relationship_targets']} |",
        f"| PDF | figure-boundary paragraphs | {result['pdf']['figure_boundary_paragraphs']} |",
        f"| PDF | matched draft caption titles | {result['pdf']['matched_caption_titles']} |",
        "",
        "## Per-Figure Crosswalk",
        "",
        "| Figure | EPUB SVG entry | DOCX stem | PDF caption title |",
        "|---|---|---|---|",
    ]
    epub_rows = {row["id"]: row for row in result["epub"]["per_figure"]}
    docx_rows = {row["id"]: row for row in result["docx"]["per_figure"]}
    pdf_rows = {row["id"]: row for row in result["pdf"]["per_figure"]}
    for figure_id in sorted(epub_rows):
        epub_row = epub_rows[figure_id]
        docx_row = docx_rows[figure_id]
        pdf_row = pdf_rows[figure_id]
        lines.append(
            f"| `{figure_id}` | `{epub_row['packaged_svg_entry']}` | `{docx_row['asset_stem']}` | {pdf_row['caption_title']} |"
        )
    lines.extend(
        [
            "",
            "## Residuals",
            "",
            "- EPUB still needs real e-reader or application inspection for image sizing, fallback behavior, navigation, and reading flow.",
            "- DOCX still needs Word, LibreOffice GUI, or Google Docs review for image anchoring, page breaks, and caption flow.",
            "- PDF still needs manual page-level layout and reading-flow review for figure scale, caption placement, and near-edge content.",
            "- Audio still needs reviewed spoken treatment; the companion summaries are drafting notes, not narration approval.",
            "- This probe does not approve final figure art, release any format artifact, create a reader edition release record, or promote any chapter core claim.",
            "",
        ]
    )
    DOC.write_text("\n".join(lines), encoding="utf-8")


def validate_doc(errors: list[str]) -> None:
    if not DOC.exists():
        errors.append(f"{rel(DOC)} is missing.")
        return
    text = DOC.read_text(encoding="utf-8")
    required = [
        "Reader Key-Figure Format Probe",
        "python3 scripts/validate_reader_key_figure_format_probe.py --write-manifest --write-doc",
        "| EPUB | packaged SVG entries | 10 |",
        "| DOCX | PNG media entries | 61 |",
        "| PDF | figure-boundary paragraphs | 10 |",
        "not final figure-artifact approval",
        "EPUB still needs real e-reader",
        "DOCX still needs Word",
        "PDF still needs manual page-level layout",
        "does not approve final figure art",
    ]
    for fragment in required:
        if fragment not in text:
            errors.append(f"{rel(DOC)} missing required fragment: {fragment}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-manifest", action="store_true", help="write observed probe to the tracked manifest")
    parser.add_argument("--write-doc", action="store_true", help="rewrite the tracked markdown review doc from the manifest/result")
    args = parser.parse_args()

    if args.write_manifest:
        result = observe()
        errors = validate_result(result)
        if errors:
            fail(errors)
        RESULT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    else:
        if not RESULT.exists():
            fail([f"{rel(RESULT)} is missing; run with --write-manifest."])
        result = load_json(RESULT)
        errors = validate_result(result)
        if errors:
            fail(errors)

    if args.write_doc:
        write_doc(result)

    errors = validate_result(result)
    validate_doc(errors)
    if errors:
        fail(errors)
    print(
        "Reader key-figure format probe validation passed: "
        f"{result['figure_count']} figures across EPUB/DOCX/PDF package probes."
    )


if __name__ == "__main__":
    main()
