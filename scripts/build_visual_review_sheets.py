#!/usr/bin/env python3
"""Build bounded contact sheets for seven-scene release visual review."""

from __future__ import annotations

import argparse
import json
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "build/visual_edition/review/generated"
OUT = ROOT / "build/visual_edition/review/sheets"
PILOTS = {
    "asi-is-a-stack-not-a-model",
    "capability-replacement-and-rollback",
    "context-transactions-snapshots-mounts-and-taint",
    "replaceable-cognitive-substrates-beyond-transformer-monoculture",
    "living-book-methodology",
}
BACKGROUND = "#101820"
INK = "#F5F8FA"
MUTED = "#B8C4CC"
ACCENT = "#58B7D3"


def font(size: int):
    candidates = (
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    )
    for candidate in candidates:
        if Path(candidate).is_file():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def chapters(include_pilots: bool = False) -> list[dict]:
    structure = json.loads((ROOT / "book_structure.json").read_text(encoding="utf-8"))
    return [
        chapter
        for part in structure["parts"]
        for chapter in part["chapters"]
        if include_pilots or chapter["id"] not in PILOTS
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", type=int, default=4)
    parser.add_argument("--all-chapters", action="store_true")
    args = parser.parse_args()
    rows = chapters(include_pilots=args.all_chapters)
    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("sheet-*.png"):
        old.unlink()
    scene_width, scene_height = 320, 180
    label_width = 430
    width = label_width + 7 * scene_width
    made = 0
    index = []
    for start in range(0, len(rows), args.rows):
        group = rows[start:start + args.rows]
        sheet = Image.new("RGB", (width, len(group) * scene_height), BACKGROUND)
        draw = ImageDraw.Draw(sheet)
        for row_index, chapter in enumerate(group):
            y = row_index * scene_height
            draw.rectangle((0, y, label_width, y + scene_height), fill="#182630")
            draw.text((20, y + 16), f"{start + row_index + 1:02d}", fill=ACCENT, font=font(25))
            title = "\n".join(textwrap.wrap(chapter["title"], width=31))
            draw.multiline_text((65, y + 15), title, fill=INK, font=font(21), spacing=3)
            draw.text((65, y + 135), chapter["id"], fill=MUTED, font=font(12))
            directory = REVIEW / chapter["id"]
            for scene_index in range(1, 8):
                source = directory / f"{scene_index:02d}.png"
                if not source.is_file():
                    raise SystemExit(f"Missing review frame: {source}")
                image = Image.open(source).convert("RGB")
                image.thumbnail((scene_width, scene_height), Image.Resampling.LANCZOS)
                x = label_width + (scene_index - 1) * scene_width
                sheet.paste(image, (x, y))
        made += 1
        path = OUT / f"sheet-{made:02d}.png"
        sheet.save(path, optimize=True)
        index.append({
            "sheet": str(path.relative_to(ROOT)),
            "chapter_ids": [chapter["id"] for chapter in group],
        })
    (OUT / "index.json").write_text(
        json.dumps({"sheet_count": made, "sheets": index}, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Built {made} review sheets for {len(rows)} chapters.")


if __name__ == "__main__":
    main()
