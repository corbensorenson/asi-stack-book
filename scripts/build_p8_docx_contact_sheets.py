#!/usr/bin/env python3
"""Build complete DOCX page contact sheets and a conservative raster audit."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageOps


def page_number(path: Path) -> int:
    match = re.search(r"(\d+)$", path.stem)
    if not match:
        raise ValueError(f"page number missing from {path.name}")
    return int(match.group(1))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("page_dir", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()

    pages = sorted(args.page_dir.glob("page-*.png"), key=page_number)
    if not pages:
        raise SystemExit("no rendered DOCX page PNGs found")
    args.output_dir.mkdir(parents=True, exist_ok=True)

    per_sheet = 48
    columns = 6
    thumb_width = 150
    thumb_height = 194
    label_height = 18
    rows = per_sheet // columns
    blank_pages: list[int] = []
    low_ink_pages: list[int] = []
    outer_edge_ink_pages: list[int] = []
    records: list[dict[str, object]] = []

    for start in range(0, len(pages), per_sheet):
        batch = pages[start : start + per_sheet]
        sheet = Image.new(
            "RGB",
            (columns * thumb_width, rows * (thumb_height + label_height)),
            "white",
        )
        draw = ImageDraw.Draw(sheet)
        for offset, path in enumerate(batch):
            number = page_number(path)
            with Image.open(path) as source:
                gray = source.convert("L")
                histogram = gray.histogram()
                total = gray.width * gray.height
                ink = sum(histogram[:245])
                ink_fraction = ink / total
                if ink_fraction < 0.0005:
                    blank_pages.append(number)
                if ink_fraction < 0.005:
                    low_ink_pages.append(number)
                border = ImageOps.expand(gray.crop((5, 5, gray.width - 5, gray.height - 5)), border=5, fill=255)
                difference = sum(ImageChops.difference(gray, border).histogram()[1:])
                if difference:
                    outer_edge_ink_pages.append(number)
                records.append(
                    {
                        "page": number,
                        "width": gray.width,
                        "height": gray.height,
                        "ink_fraction": round(ink_fraction, 6),
                    }
                )
                thumb = source.convert("RGB")
                thumb.thumbnail((thumb_width - 8, thumb_height - 8))
                x = (offset % columns) * thumb_width + (thumb_width - thumb.width) // 2
                y = (offset // columns) * (thumb_height + label_height) + 4
                sheet.paste(thumb, (x, y))
                draw.text(
                    ((offset % columns) * thumb_width + 6, y + thumb_height - 4),
                    f"p. {number}",
                    fill="black",
                )
        sheet_path = args.output_dir / f"contact-{start // per_sheet + 1:02d}.png"
        sheet.save(sheet_path, optimize=True)

    report = {
        "schema_version": "asi_stack.p8_docx_raster_audit.v1",
        "page_count": len(pages),
        "contact_sheet_count": (len(pages) + per_sheet - 1) // per_sheet,
        "blank_pages": blank_pages,
        "low_ink_pages": low_ink_pages,
        "outer_edge_ink_pages": sorted(set(outer_edge_ink_pages)),
        "page_records": records,
        "non_claims": [
            "Raster heuristics do not replace visual review.",
            "Absence of outer-edge ink does not prove absence of clipping inside tables or figures.",
            "Contact-sheet review does not establish Microsoft Word behavior or accessibility conformance.",
        ],
    }
    (args.output_dir / "raster_audit.json").write_text(json.dumps(report, indent=2) + "\n")
    print(
        f"Built {report['contact_sheet_count']} contact sheets for {len(pages)} pages; "
        f"blank={len(blank_pages)}, low_ink={len(low_ink_pages)}, "
        f"outer_edge_ink={len(report['outer_edge_ink_pages'])}."
    )


if __name__ == "__main__":
    main()
