#!/usr/bin/env python3
"""Audit every page of the exact v2 reader PDF and create contact sheets."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import tempfile
import unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image, ImageDraw
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PDF = ROOT / "editions/reader_manuscript/v2_0/artifacts/asi-stack-curated-reader-v2.0.pdf"
MANIFEST = ROOT / "editions/reader_manuscript/v2_0/manifest.json"
REPORT = ROOT / "editions/reader_manuscript/v2_0/pdf_structural_and_page_inspection.json"
REVIEW_DIR = ROOT / "build/post_v2_3_pdf_review"
LIVE_MARKERS = ("Chapter status", "Drafting guardrail", "Codex test plan", "Source crosswalk", "Formalization hooks")


def run(command: list[str]) -> str:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    if result.returncode:
        raise SystemExit(f"command failed ({result.returncode}): {' '.join(command)}\n{result.stderr[-2000:]}")
    return result.stdout


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).replace("’", "'").replace("–", "-").replace("—", "-")
    return re.sub(r"\s+", " ", text).strip()


def flatten_outline(items: list, rows: list[str]) -> None:
    for item in items:
        if isinstance(item, list):
            flatten_outline(item, rows)
        else:
            title = getattr(item, "title", "")
            if title:
                rows.append(str(title))


def pdf_object_metrics(pdf: Path) -> dict:
    reader = PdfReader(str(pdf))
    outline: list[str] = []
    flatten_outline(reader.outline, outline)
    link_count = external_links = internal_links = unresolved_links = 0
    for page in reader.pages:
        for ref in page.get("/Annots", []):
            annot = ref.get_object()
            if str(annot.get("/Subtype", "")) != "/Link":
                continue
            link_count += 1
            action = annot.get("/A")
            if action and action.get("/URI"):
                external_links += 1
            elif annot.get("/Dest") is not None or (action and action.get("/D") is not None):
                internal_links += 1
            else:
                unresolved_links += 1
    sizes = sorted(
        {
            (round(float(page.mediabox.width), 3), round(float(page.mediabox.height), 3))
            for page in reader.pages
        }
    )
    metadata = reader.metadata or {}
    return {
        "pages": len(reader.pages),
        "encrypted": reader.is_encrypted,
        "page_sizes_points": [list(value) for value in sizes],
        "metadata_title": str(metadata.get("/Title", "")),
        "metadata_author": str(metadata.get("/Author", "")),
        "outline_entries": len(outline),
        "outline_first": outline[:5],
        "outline_last": outline[-5:],
        "link_annotations": link_count,
        "external_links": external_links,
        "internal_links": internal_links,
        "unresolved_link_annotations": unresolved_links,
        "named_destinations": len(reader.named_destinations),
    }


def font_metrics(pdf: Path) -> dict:
    lines = run(["pdffonts", str(pdf)]).splitlines()[2:]
    rows = [re.split(r"\s+", line.strip()) for line in lines if line.strip()]
    return {
        "font_rows": len(rows),
        "embedded_no_rows": sum(1 for row in rows if len(row) >= 8 and row[3].lower() == "no"),
        "subset_no_rows": sum(1 for row in rows if len(row) >= 8 and row[4].lower() == "no"),
        "font_names": sorted({row[0] for row in rows if row}),
        "raw_rows": [" ".join(row) for row in rows],
    }


def bbox_metrics(xml_path: Path) -> tuple[list[dict], int]:
    root = ET.parse(xml_path).getroot()
    rows: list[dict] = []
    total_out = 0
    for page_number, page in enumerate((node for node in root.iter() if node.tag.endswith("page")), start=1):
        width = float(page.attrib["width"])
        height = float(page.attrib["height"])
        words = [node for node in page.iter() if node.tag.endswith("word")]
        out = 0
        for word in words:
            x0, y0 = float(word.attrib["xMin"]), float(word.attrib["yMin"])
            x1, y1 = float(word.attrib["xMax"]), float(word.attrib["yMax"])
            out += int(x0 < 0 or y0 < 0 or x1 > width or y1 > height)
        total_out += out
        rows.append({"page": page_number, "word_boxes": len(words), "out_of_bounds_word_boxes": out})
    return rows, total_out


def page_number(path: Path) -> int:
    return int(re.search(r"-(\d+)\.png$", path.name).group(1))


def raster_metrics(pdf: Path, review_dir: Path) -> tuple[list[dict], list[str]]:
    pages_dir = review_dir / "pages"
    contacts_dir = review_dir / "contact_sheets"
    import shutil
    for generated_dir in (pages_dir, contacts_dir):
        if generated_dir.exists():
            shutil.rmtree(generated_dir)
    pages_dir.mkdir(parents=True)
    contacts_dir.mkdir(parents=True)
    run(["pdftoppm", "-png", "-r", "72", str(pdf), str(pages_dir / "page")])
    paths = sorted(pages_dir.glob("page-*.png"), key=page_number)
    rows: list[dict] = []
    thumbs: list[tuple[int, Image.Image]] = []
    for path in paths:
        number = page_number(path)
        image = Image.open(path).convert("RGB")
        gray = image.convert("L")
        mask = gray.point(lambda value: 255 if value < 245 else 0, mode="L")
        bbox = mask.getbbox()
        histogram = mask.histogram()
        nonwhite = histogram[255]
        if bbox is None:
            margins = None
            near_edge = False
        else:
            left, top, right, bottom = bbox
            margins = [left, top, image.width - right, image.height - bottom]
            near_edge = min(margins) <= 2
        rows.append(
            {
                "page": number,
                "width_px": image.width,
                "height_px": image.height,
                "nonwhite_pixels": nonwhite,
                "blank": bbox is None,
                "low_ink": bbox is not None and nonwhite < 750,
                "near_edge": near_edge,
                "margins_px": margins,
            }
        )
        thumb = image.copy()
        thumb.thumbnail((153, 198), Image.Resampling.LANCZOS)
        thumbs.append((number, thumb))

    contact_paths: list[str] = []
    for sheet_index in range(0, len(thumbs), 20):
        batch = thumbs[sheet_index:sheet_index + 20]
        sheet = Image.new("RGB", (4 * 163, 5 * 218), "#d9d9d9")
        draw = ImageDraw.Draw(sheet)
        for slot, (number, thumb) in enumerate(batch):
            x = (slot % 4) * 163 + 5
            y = (slot // 4) * 218 + 5
            sheet.paste(thumb, (x, y + 15))
            draw.text((x, y), f"p. {number}", fill="black")
        out = contacts_dir / f"contact-{sheet_index // 20 + 1:03d}.png"
        sheet.save(out, optimize=True)
        contact_paths.append(str(out.relative_to(ROOT)))
    return rows, contact_paths


def observe(pdf: Path) -> dict:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    errors: list[str] = []
    objects = pdf_object_metrics(pdf)
    fonts = font_metrics(pdf)
    with tempfile.TemporaryDirectory(prefix="asi-v2-pdf-audit-") as temp:
        temp_dir = Path(temp)
        layout_path = temp_dir / "layout.txt"
        bbox_path = temp_dir / "bbox.html"
        run(["pdftotext", "-layout", str(pdf), str(layout_path)])
        run(["pdftotext", "-bbox", str(pdf), str(bbox_path)])
        text = layout_path.read_text(encoding="utf-8", errors="replace")
        bbox_rows, out_of_bounds = bbox_metrics(bbox_path)
    pages = text.split("\f")
    if pages and not pages[-1].strip():
        pages = pages[:-1]
    page_text_chars = [len(page.strip()) for page in pages]
    normalized_text = normalize(text)
    titles = [record["title"] for record in manifest["chapter_records"]]
    offsets = []
    cursor = 0
    missing_titles = []
    for title in titles:
        offset = normalized_text.find(normalize(title), cursor)
        if offset < 0:
            missing_titles.append(title)
        else:
            offsets.append(offset)
            cursor = offset + len(title)
    raster_rows, contact_sheets = raster_metrics(pdf, REVIEW_DIR)
    if objects["metadata_title"] != "The ASI Stack" or objects["metadata_author"] != "Corben Sorenson":
        errors.append("PDF title or author metadata drift")
    if objects["encrypted"] or objects["page_sizes_points"] != [[612.0, 792.0]]:
        errors.append("PDF encryption or US-letter page-size drift")
    if objects["outline_entries"] < 59:
        errors.append(f"PDF outline is unexpectedly shallow: {objects['outline_entries']}")
    if objects["unresolved_link_annotations"]:
        errors.append(f"unresolved PDF link annotations: {objects['unresolved_link_annotations']}")
    if fonts["embedded_no_rows"]:
        errors.append(f"unembedded PDF font rows: {fonts['embedded_no_rows']}")
    if len(pages) != objects["pages"] or len(bbox_rows) != objects["pages"] or len(raster_rows) != objects["pages"]:
        errors.append("PDF text/bbox/raster page denominators disagree")
    if out_of_bounds:
        errors.append(f"out-of-bounds PDF word boxes: {out_of_bounds}")
    if any(row["blank"] for row in raster_rows):
        errors.append("blank PDF raster pages detected")
    if any(row["near_edge"] for row in raster_rows):
        errors.append("near-edge PDF raster content detected")
    if missing_titles:
        errors.append(f"missing or out-of-order chapter titles: {len(missing_titles)}")
    if text.count("\ufffd"):
        errors.append(f"replacement characters in extracted text: {text.count(chr(0xfffd))}")
    live_hits = [marker for marker in LIVE_MARKERS if marker in text]
    if live_hits:
        errors.append("live-only reader markers leaked into PDF")
    risk_pages = sorted(
        {
            row["page"] for row in raster_rows if row["low_ink"] or row["near_edge"]
        }
        | {index for index, count in enumerate(page_text_chars, start=1) if count < 300}
    )
    return {
        "schema_version": "asi_stack.reader_pdf_structural_page_inspection.v1",
        "edition_id": manifest["edition_id"],
        "state": "passed_automated_page_complete_visual_review_pending" if not errors else "failed_automated",
        "artifact": str(pdf.relative_to(ROOT)),
        "sha256": sha256(pdf),
        "bytes": pdf.stat().st_size,
        "pdf_objects": objects,
        "fonts": fonts,
        "text": {
            "pages_checked": len(pages),
            "characters_checked": len(text),
            "replacement_characters": text.count("\ufffd"),
            "minimum_page_characters": min(page_text_chars, default=0),
            "maximum_page_characters": max(page_text_chars, default=0),
            "pages_under_300_characters": [index for index, count in enumerate(page_text_chars, start=1) if count < 300],
            "chapter_titles_checked_in_order": len(offsets),
            "missing_or_out_of_order_chapter_titles": missing_titles,
            "live_marker_hits": live_hits,
        },
        "bbox": {
            "pages_checked": len(bbox_rows),
            "word_boxes_checked": sum(row["word_boxes"] for row in bbox_rows),
            "out_of_bounds_word_boxes": out_of_bounds,
        },
        "raster": {
            "dpi": 72,
            "pages_checked": len(raster_rows),
            "blank_pages": [row["page"] for row in raster_rows if row["blank"]],
            "low_ink_pages": [row["page"] for row in raster_rows if row["low_ink"]],
            "near_edge_pages": [row["page"] for row in raster_rows if row["near_edge"]],
            "minimum_nonwhite_pixels": min((row["nonwhite_pixels"] for row in raster_rows), default=0),
            "maximum_nonwhite_pixels": max((row["nonwhite_pixels"] for row in raster_rows), default=0),
            "contact_sheets": contact_sheets,
            "risk_pages": risk_pages,
        },
        "errors": errors,
        "visual_review": "pending_contact_sheet_and_preview_risk_page_review",
        "support_state_effect": "none",
        "release_effect": "none",
        "review_boundary": "Every PDF page was text-, bbox-, and raster-processed. Contact sheets and risk pages still require visual review; Preview application review is separate. This is not independent-human, assistive-technology, legal-WCAG, release, or support-state approval."
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", type=Path, default=DEFAULT_PDF)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    pdf = args.pdf if args.pdf.is_absolute() else ROOT / args.pdf
    if not pdf.is_file():
        raise SystemExit(f"missing PDF: {pdf}")
    observed = observe(pdf)
    if args.write:
        REPORT.write_text(json.dumps(observed, indent=2) + "\n", encoding="utf-8")
    elif not REPORT.is_file() or json.loads(REPORT.read_text()) != observed:
        raise SystemExit("PDF inspection report is missing or stale; run with --write")
    if observed["errors"]:
        raise SystemExit("PDF inspection failed:\n - " + "\n - ".join(observed["errors"]))
    print(
        f"PDF automated inspection passed: {observed['pdf_objects']['pages']} pages, "
        f"{observed['bbox']['word_boxes_checked']} word boxes, "
        f"{len(observed['raster']['contact_sheets'])} contact sheets."
    )


if __name__ == "__main__":
    main()
