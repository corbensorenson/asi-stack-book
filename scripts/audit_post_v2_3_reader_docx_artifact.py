#!/usr/bin/env python3
"""Audit the exact v2 reader DOCX package and its page-complete office render."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import posixpath
import re
import subprocess
import unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path
from zipfile import BadZipFile, ZipFile

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DOCX = ROOT / "editions/reader_manuscript/v2_0/artifacts/asi-stack-curated-reader-v2.0.docx"
DEFAULT_RENDER_DIR = ROOT / "build/post_v2_3_docx_review/rendered_exact"
MANIFEST = ROOT / "editions/reader_manuscript/v2_0/manifest.json"
REPORT = ROOT / "editions/reader_manuscript/v2_0/docx_package_and_page_inspection.json"
REVIEW_DIR = ROOT / "build/post_v2_3_docx_review"
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
WP = "{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}"
M = "{http://schemas.openxmlformats.org/officeDocument/2006/math}"
PKG_REL = "{http://schemas.openxmlformats.org/package/2006/relationships}"
CORE = {
    "title": "{http://purl.org/dc/elements/1.1/}title",
    "creator": "{http://purl.org/dc/elements/1.1/}creator",
    "language": "{http://purl.org/dc/elements/1.1/}language",
    "created": "{http://purl.org/dc/terms/}created",
    "modified": "{http://purl.org/dc/terms/}modified",
}
LIVE_MARKERS = ("Chapter status", "Drafting guardrail", "Codex test plan", "Source crosswalk", "Formalization hooks")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).replace("’", "'").replace("–", "-").replace("—", "-")
    return re.sub(r"\s+", " ", text).strip()


def run(command: list[str]) -> str:
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    if completed.returncode:
        raise RuntimeError(
            f"command failed ({completed.returncode}): {' '.join(command)}\n{completed.stderr[-2000:]}"
        )
    return completed.stdout


def paragraph_text(paragraph: ET.Element) -> str:
    return "".join(node.text or "" for node in paragraph.findall(f".//{W}t"))


def relationship_base(name: str) -> str:
    if name == "_rels/.rels":
        return ""
    parent = posixpath.dirname(name)
    if not parent.endswith("/_rels"):
        return ""
    return parent[:-6]


def inspect_package(docx: Path, manifest: dict) -> tuple[dict, list[str]]:
    errors: list[str] = []
    try:
        with ZipFile(docx) as archive:
            names = archive.namelist()
            name_set = set(names)
            if len(names) != len(name_set):
                errors.append("duplicate OOXML member names")
            unsafe = [name for name in names if name.startswith("/") or ".." in Path(name).parts]
            if unsafe:
                errors.append(f"unsafe OOXML member paths: {len(unsafe)}")
            xml_names = [name for name in names if name.endswith(".xml") or name.endswith(".rels")]
            roots: dict[str, ET.Element] = {}
            for name in xml_names:
                try:
                    roots[name] = ET.fromstring(archive.read(name))
                except ET.ParseError as exc:
                    errors.append(f"malformed XML member {name}: {exc}")
            required = {
                "[Content_Types].xml",
                "_rels/.rels",
                "docProps/core.xml",
                "docProps/app.xml",
                "word/document.xml",
                "word/styles.xml",
                "word/numbering.xml",
                "word/settings.xml",
                "word/_rels/document.xml.rels",
            }
            missing_required = sorted(required - name_set)
            if missing_required:
                errors.append(f"missing required OOXML members: {missing_required}")
            unresolved_targets: list[str] = []
            external_relationships = 0
            relationship_count = 0
            for name, root in roots.items():
                if not name.endswith(".rels"):
                    continue
                base = relationship_base(name)
                for relationship in root.findall(f".//{PKG_REL}Relationship"):
                    relationship_count += 1
                    target = relationship.get("Target", "")
                    if relationship.get("TargetMode") == "External":
                        external_relationships += 1
                        continue
                    resolved = posixpath.normpath(posixpath.join(base, target))
                    if resolved not in name_set:
                        unresolved_targets.append(f"{name}:{target}->{resolved}")
            if unresolved_targets:
                errors.append(f"unresolved OOXML relationship targets: {len(unresolved_targets)}")

            document = roots.get("word/document.xml", ET.Element("missing"))
            styles = roots.get("word/styles.xml", ET.Element("missing"))
            core = roots.get("docProps/core.xml", ET.Element("missing"))
            document_rels = roots.get("word/_rels/document.xml.rels", ET.Element("missing"))
            paragraphs = document.findall(f".//{W}p")
            style_counts: Counter[str] = Counter()
            text_rows: list[str] = []
            heading_levels: list[int] = []
            for paragraph in paragraphs:
                style = paragraph.find(f"./{W}pPr/{W}pStyle")
                style_name = style.get(f"{W}val", "") if style is not None else ""
                style_counts[style_name] += 1
                text_rows.append(paragraph_text(paragraph))
                match = re.fullmatch(r"Heading([1-9])", style_name)
                if match:
                    heading_levels.append(int(match.group(1)))
            heading_jumps = sum(
                1 for previous, current in zip(heading_levels, heading_levels[1:]) if current > previous + 1
            )
            full_text = "\n".join(text_rows)
            normalized_text = normalize(full_text)
            cursor = 0
            missing_titles: list[str] = []
            for record in manifest["chapter_records"]:
                title = normalize(record["title"])
                offset = normalized_text.find(title, cursor)
                if offset < 0:
                    missing_titles.append(record["title"])
                else:
                    cursor = offset + len(title)

            doc_pr = document.findall(f".//{WP}docPr")
            missing_alt = [node.get("id", "") for node in doc_pr if not (node.get("descr") or "").strip()]
            media = [name for name in names if name.startswith("word/media/")]
            png_media = [name for name in media if name.lower().endswith(".png")]
            non_png_media = sorted(set(media) - set(png_media))
            hyperlinks = document.findall(f".//{W}hyperlink")
            external_doc_relationships = sum(
                1 for node in document_rels.findall(f".//{PKG_REL}Relationship")
                if node.get("TargetMode") == "External"
            )
            section_rows = []
            for section in document.findall(f".//{W}sectPr"):
                size = section.find(f"./{W}pgSz")
                margins = section.find(f"./{W}pgMar")
                section_rows.append(
                    {
                        "page_width_twips": int(size.get(f"{W}w", "0")) if size is not None else 0,
                        "page_height_twips": int(size.get(f"{W}h", "0")) if size is not None else 0,
                        "margins_twips": {
                            key: int(margins.get(f"{W}{key}", "0")) if margins is not None else 0
                            for key in ("top", "right", "bottom", "left")
                        },
                    }
                )
            core_values = {
                key: (core.find(tag).text or "") if core.find(tag) is not None else ""
                for key, tag in CORE.items()
            }
            style_languages = sorted(
                {node.get(f"{W}val", "") for node in styles.findall(f".//{W}lang") if node.get(f"{W}val")}
            )
    except BadZipFile as exc:
        return {}, [f"invalid DOCX ZIP container: {exc}"]

    expected_core = {
        "title": "The ASI Stack",
        "creator": "Corben Sorenson",
        "language": "en-US",
        "created": "2026-07-13T00:00:00Z",
        "modified": "2026-07-13T00:00:00Z",
    }
    if core_values != expected_core:
        errors.append("DOCX core metadata or canonical dates drifted")
    if missing_alt:
        errors.append(f"DOCX drawings without image descriptions: {len(missing_alt)}")
    if non_png_media:
        errors.append(f"DOCX contains non-PNG media: {non_png_media}")
    if missing_titles:
        errors.append(f"missing or out-of-order chapter titles: {len(missing_titles)}")
    if heading_jumps:
        errors.append(f"heading-level jumps: {heading_jumps}")
    if any(marker in full_text for marker in LIVE_MARKERS):
        errors.append("live-only reader markers leaked into DOCX")
    if section_rows != [{
        "page_width_twips": 12240,
        "page_height_twips": 15840,
        "margins_twips": {"top": 1440, "right": 1440, "bottom": 1440, "left": 1440},
    }]:
        errors.append("DOCX page size, section count, or margins drifted")
    return {
        "zip_members": len(names),
        "xml_members_parsed": len(xml_names),
        "required_members": sorted(required),
        "missing_required_members": missing_required,
        "relationship_count": relationship_count,
        "external_relationships": external_relationships,
        "unresolved_relationship_targets": unresolved_targets,
        "core_properties": core_values,
        "style_definitions": len(styles.findall(f".//{W}style")),
        "style_languages": style_languages,
        "paragraphs": len(paragraphs),
        "paragraph_style_counts": dict(sorted(style_counts.items())),
        "heading_level_jumps": heading_jumps,
        "chapter_titles_checked_in_order": len(manifest["chapter_records"]) - len(missing_titles),
        "missing_or_out_of_order_chapter_titles": missing_titles,
        "sections": section_rows,
        "list_paragraphs": len(document.findall(f".//{W}numPr")),
        "tables": len(document.findall(f".//{W}tbl")),
        "drawings": len(document.findall(f".//{W}drawing")),
        "drawing_descriptions": len(doc_pr) - len(missing_alt),
        "missing_drawing_descriptions": missing_alt,
        "media_entries": len(media),
        "png_media_entries": len(png_media),
        "non_png_media_entries": non_png_media,
        "hyperlinks": len(hyperlinks),
        "external_hyperlink_relationships": external_doc_relationships,
        "internal_anchor_hyperlinks": sum(1 for node in hyperlinks if node.get(f"{W}anchor")),
        "bookmarks": len(document.findall(f".//{W}bookmarkStart")),
        "native_omml_equations": len(document.findall(f".//{M}oMath")),
        "math_representation_boundary": "source mathematical notation is preserved as document text; zero native OMML equations are claimed",
        "text_characters": len(full_text),
        "live_marker_hits": [marker for marker in LIVE_MARKERS if marker in full_text],
    }, errors


def pdf_info(pdf: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in run(["pdfinfo", str(pdf)]).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            values[key.strip()] = value.strip()
    return values


def page_number(path: Path) -> int:
    match = re.search(r"page-(\d+)\.png$", path.name)
    if not match:
        raise RuntimeError(f"cannot parse rendered page number: {path.name}")
    return int(match.group(1))


def inspect_rasters(render_dir: Path) -> tuple[dict, list[str]]:
    errors: list[str] = []
    pages = sorted(render_dir.glob("page-*.png"), key=page_number)
    contacts_dir = REVIEW_DIR / "contact_sheets"
    contacts_dir.mkdir(parents=True, exist_ok=True)
    for old in contacts_dir.glob("contact-*.png"):
        old.unlink()
    rows = []
    thumbnails: list[tuple[int, Image.Image]] = []
    for path in pages:
        number = page_number(path)
        image = Image.open(path).convert("RGB")
        gray = image.convert("L")
        mask = gray.point(lambda value: 255 if value < 245 else 0, mode="L")
        bbox = mask.getbbox()
        nonwhite = mask.histogram()[255]
        if bbox is None:
            margins = None
            near_edge = False
        else:
            left, top, right, bottom = bbox
            margins = [left, top, image.width - right, image.height - bottom]
            near_edge = min(margins) <= 2
        rows.append({
            "page": number,
            "width_px": image.width,
            "height_px": image.height,
            "nonwhite_pixels": nonwhite,
            "blank": bbox is None,
            "low_ink": bbox is not None and nonwhite < 750,
            "near_edge": near_edge,
            "margins_px": margins,
        })
        thumb = image.copy()
        thumb.thumbnail((153, 198), Image.Resampling.LANCZOS)
        thumbnails.append((number, thumb))
    contact_paths = []
    for offset in range(0, len(thumbnails), 20):
        batch = thumbnails[offset:offset + 20]
        sheet = Image.new("RGB", (4 * 163, 5 * 218), "#d9d9d9")
        draw = ImageDraw.Draw(sheet)
        for slot, (number, thumb) in enumerate(batch):
            x = (slot % 4) * 163 + 5
            y = (slot // 4) * 218 + 5
            sheet.paste(thumb, (x, y + 15))
            draw.text((x, y), f"p. {number}", fill="black")
        output = contacts_dir / f"contact-{offset // 20 + 1:03d}.png"
        sheet.save(output, optimize=True)
        contact_paths.append(str(output.relative_to(ROOT)))
    if any(row["blank"] for row in rows):
        errors.append("blank DOCX-rendered pages detected")
    if any(row["near_edge"] for row in rows):
        errors.append("near-edge DOCX-rendered page content detected")
    return {
        "dpi": 72,
        "pages_checked": len(rows),
        "blank_pages": [row["page"] for row in rows if row["blank"]],
        "low_ink_pages": [row["page"] for row in rows if row["low_ink"]],
        "near_edge_pages": [row["page"] for row in rows if row["near_edge"]],
        "minimum_nonwhite_pixels": min((row["nonwhite_pixels"] for row in rows), default=0),
        "maximum_nonwhite_pixels": max((row["nonwhite_pixels"] for row in rows), default=0),
        "contact_sheets": contact_paths,
    }, errors


def observe(docx: Path, render_dir: Path) -> dict:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    package, errors = inspect_package(docx, manifest)
    # The documents-skill renderer preserves the exact input artifact stem.
    # Derive the expected PDF name from the audited DOCX instead of assuming
    # Quarto's pre-canonicalization output name.
    pdf = render_dir / f"{docx.stem}.pdf"
    if not pdf.is_file():
        errors.append("missing LibreOffice-rendered PDF")
        info = {}
        text = ""
    else:
        info = pdf_info(pdf)
        text = run(["pdftotext", "-layout", str(pdf), "-"])
    raster, raster_errors = inspect_rasters(render_dir)
    errors.extend(raster_errors)
    pages = text.split("\f")
    if pages and not pages[-1].strip():
        pages = pages[:-1]
    normalized_text = normalize(text)
    cursor = 0
    missing_titles = []
    for record in manifest["chapter_records"]:
        title = normalize(record["title"])
        offset = normalized_text.find(title, cursor)
        if offset < 0:
            missing_titles.append(record["title"])
        else:
            cursor = offset + len(title)
    if missing_titles:
        errors.append(f"converted PDF missing or reorders chapter titles: {len(missing_titles)}")
    if text.count("\ufffd"):
        errors.append(f"converted PDF replacement characters: {text.count(chr(0xfffd))}")
    if len(pages) != raster.get("pages_checked") or int(info.get("Pages", "0")) != len(pages):
        errors.append("converted PDF text/raster/pageinfo denominators disagree")
    if info.get("Page size") != "612 x 792 pts (letter)":
        errors.append("LibreOffice conversion page size drifted")
    if info.get("Encrypted") != "no" or info.get("Tagged") != "yes":
        errors.append("LibreOffice conversion encryption or tagging drifted")
    return {
        "schema_version": "asi_stack.reader_docx_package_page_inspection.v1",
        "edition_id": manifest["edition_id"],
        "state": "passed_package_and_page_automation_visual_review_pending" if not errors else "failed_automated",
        "artifact": str(docx.relative_to(ROOT)),
        "sha256": sha256(docx),
        "bytes": docx.stat().st_size,
        "package": package,
        "libreoffice_conversion": {
            "application": "LibreOfficeDev Writer headless PDF export",
            "version": info.get("Producer", ""),
            "title": info.get("Title", ""),
            "author": info.get("Author", ""),
            "tagged": info.get("Tagged", ""),
            "encrypted": info.get("Encrypted", ""),
            "pages": int(info.get("Pages", "0")) if info else 0,
            "page_size": info.get("Page size", ""),
            "text_characters_checked": len(text),
            "replacement_characters": text.count("\ufffd"),
            "chapter_titles_checked_in_order": len(manifest["chapter_records"]) - len(missing_titles),
            "missing_or_out_of_order_chapter_titles": missing_titles,
            "live_marker_hits": [marker for marker in LIVE_MARKERS if marker in text],
        },
        "raster": raster,
        "errors": errors,
        "visual_review": "pending_contact_sheet_review",
        "support_state_effect": "none",
        "release_effect": "none",
        "review_boundary": "OOXML structure and every LibreOffice-rendered page were processed. Contact sheets still require internal visual review. This is not Microsoft Word, LibreOffice GUI, Google Docs, assistive-technology, independent-human, legal-WCAG, publication, or support-state approval."
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--docx", type=Path, default=DEFAULT_DOCX)
    parser.add_argument("--render-dir", type=Path, default=DEFAULT_RENDER_DIR)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    docx = args.docx if args.docx.is_absolute() else ROOT / args.docx
    render_dir = args.render_dir if args.render_dir.is_absolute() else ROOT / args.render_dir
    observed = observe(docx, render_dir)
    if args.write:
        REPORT.write_text(json.dumps(observed, indent=2) + "\n", encoding="utf-8")
    elif not REPORT.is_file() or json.loads(REPORT.read_text(encoding="utf-8")) != observed:
        raise SystemExit("DOCX inspection report is missing or stale; run with --write")
    if observed["errors"]:
        raise SystemExit("DOCX inspection failed:\n - " + "\n - ".join(observed["errors"]))
    print(
        f"DOCX automated inspection passed: {observed['package']['zip_members']} OOXML members, "
        f"{observed['package']['drawings']} described drawings, "
        f"{observed['raster']['pages_checked']} LibreOffice-rendered pages, "
        f"{len(observed['raster']['contact_sheets'])} contact sheets."
    )


if __name__ == "__main__":
    main()
