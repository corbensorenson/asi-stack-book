#!/usr/bin/env python3
"""Rasterize tracked SVG chapter thumbnails into upload-ready PNG derivatives."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "build/visual_edition/thumbnails"
RSVG = Path("/opt/homebrew/bin/rsvg-convert")
WIDTH = 3840
HEIGHT = 2160
MAX_API_BYTES = 2_000_000


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def chapter_ids() -> list[str]:
    structure = json.loads((ROOT / "book_structure.json").read_text(encoding="utf-8"))
    return [
        chapter["id"]
        for part in structure["parts"]
        for chapter in part["chapters"]
    ]


def render(slug: str) -> dict:
    source = ROOT / f"visual_edition/chapters/{slug}/thumbnail.svg"
    output = OUT / f"{slug}.png"
    if not source.is_file():
        raise SystemExit(f"Missing tracked thumbnail source: {source}")
    subprocess.run(
        [
            str(RSVG),
            "--width", str(WIDTH),
            "--height", str(HEIGHT),
            "--keep-aspect-ratio",
            "--output", str(output),
            str(source),
        ],
        cwd=ROOT,
        check=True,
    )
    with Image.open(output) as image:
        if image.format != "PNG" or image.size != (WIDTH, HEIGHT):
            raise SystemExit(
                f"Invalid thumbnail raster for {slug}: {image.format} {image.size}"
            )
        image.convert("RGB").save(output, format="PNG", optimize=True)
    size = output.stat().st_size
    if size > MAX_API_BYTES:
        raise SystemExit(
            f"Thumbnail exceeds YouTube Data API's 2 MB limit: {slug} ({size} bytes)"
        )
    return {
        "chapter_id": slug,
        "source_path": str(source.relative_to(ROOT)),
        "source_sha256": sha256(source),
        "output_path": str(output.relative_to(ROOT)),
        "output_sha256": sha256(output),
        "width": WIDTH,
        "height": HEIGHT,
        "format": "png",
        "size_bytes": size,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--all-chapters", action="store_true")
    parser.add_argument("--chapter", action="append", default=[])
    args = parser.parse_args()
    selected = chapter_ids() if args.all_chapters else args.chapter
    if not selected:
        raise SystemExit("Select --all-chapters or at least one --chapter")
    if not RSVG.is_file():
        raise SystemExit(f"Pinned SVG rasterizer is missing: {RSVG}")
    OUT.mkdir(parents=True, exist_ok=True)
    entries = []
    for index, slug in enumerate(selected, start=1):
        entries.append(render(slug))
        print(f"[{index}/{len(selected)}] {slug}: upload thumbnail ready", flush=True)
    version = subprocess.run(
        [str(RSVG), "--version"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    receipt = {
        "schema_version": "asi_stack.local_youtube_thumbnail_batch.v1",
        "generated_at_utc": datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
        "renderer": str(RSVG),
        "renderer_version": version,
        "script_sha256": sha256(Path(__file__)),
        "width": WIDTH,
        "height": HEIGHT,
        "maximum_bytes": MAX_API_BYTES,
        "entry_count": len(entries),
        "entries": entries,
    }
    (OUT / "manifest.json").write_text(
        json.dumps(receipt, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Rendered and validated {len(entries)} upload-ready PNG thumbnails.")


if __name__ == "__main__":
    main()
