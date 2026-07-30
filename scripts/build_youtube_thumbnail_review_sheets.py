#!/usr/bin/env python3
"""Build bounded contact sheets for all upload-ready YouTube thumbnails."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "build/visual_edition/thumbnails"
OUT = ROOT / "build/visual_edition/review/thumbnail-sheets"


def chapters() -> list[dict]:
    structure = json.loads((ROOT / "book_structure.json").read_text(encoding="utf-8"))
    return [
        chapter
        for part in structure["parts"]
        for chapter in part["chapters"]
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--columns", type=int, default=3)
    parser.add_argument("--rows", type=int, default=3)
    args = parser.parse_args()
    width, height = 480, 270
    per_sheet = args.columns * args.rows
    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("sheet-*.png"):
        old.unlink()
    index = []
    rows = chapters()
    for sheet_index, start in enumerate(range(0, len(rows), per_sheet), start=1):
        group = rows[start:start + per_sheet]
        sheet = Image.new(
            "RGB",
            (args.columns * width, args.rows * height),
            "#101820",
        )
        for offset, chapter in enumerate(group):
            source = SOURCE / f"{chapter['id']}.png"
            if not source.is_file():
                raise SystemExit(f"Missing upload thumbnail: {source}")
            row, column = divmod(offset, args.columns)
            image = Image.open(source).convert("RGB")
            image.thumbnail((width, height), Image.Resampling.LANCZOS)
            x, y = column * width, row * height
            sheet.paste(image, (x, y))
        path = OUT / f"sheet-{sheet_index:02d}.png"
        sheet.save(path, optimize=True)
        index.append(
            {
                "sheet": str(path.relative_to(ROOT)),
                "chapter_ids": [chapter["id"] for chapter in group],
            }
        )
    (OUT / "index.json").write_text(
        json.dumps({"sheet_count": len(index), "sheets": index}, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Built {len(index)} YouTube-thumbnail review sheets for {len(rows)} chapters.")


if __name__ == "__main__":
    main()
