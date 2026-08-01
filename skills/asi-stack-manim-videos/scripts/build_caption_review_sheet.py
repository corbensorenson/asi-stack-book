#!/usr/bin/env python3
"""Render representative captions over their exact video frames for visual QA."""

from __future__ import annotations

import argparse
import io
import math
import re
import subprocess
import textwrap
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


TIMESTAMP = re.compile(
    r"(?P<sh>\d{2}):(?P<sm>\d{2}):(?P<ss>\d{2})\.(?P<sms>\d{3})\s+-->\s+"
    r"(?P<eh>\d{2}):(?P<em>\d{2}):(?P<es>\d{2})\.(?P<ems>\d{3})"
)


@dataclass(frozen=True)
class Cue:
    start: float
    end: float
    text: str


def seconds(groups: dict[str, str], prefix: str) -> float:
    return (
        int(groups[f"{prefix}h"]) * 3600
        + int(groups[f"{prefix}m"]) * 60
        + int(groups[f"{prefix}s"])
        + int(groups[f"{prefix}ms"]) / 1000
    )


def parse_vtt(path: Path) -> list[Cue]:
    blocks = re.split(r"\n\s*\n", path.read_text(encoding="utf-8").strip())
    cues: list[Cue] = []
    for block in blocks:
        lines = block.splitlines()
        timing_index = next((i for i, line in enumerate(lines) if "-->" in line), None)
        if timing_index is None:
            continue
        match = TIMESTAMP.fullmatch(lines[timing_index].strip())
        if not match:
            raise ValueError(f"unsupported VTT timestamp: {lines[timing_index]}")
        text = " ".join(line.strip() for line in lines[timing_index + 1 :] if line.strip())
        if text:
            cues.append(Cue(seconds(match.groupdict(), "s"), seconds(match.groupdict(), "e"), text))
    if not cues:
        raise ValueError("no caption cues found")
    return cues


def sample_indices(count: int, requested: int) -> list[int]:
    if requested >= count:
        return list(range(count))
    return sorted({round(i * (count - 1) / (requested - 1)) for i in range(requested)})


def video_frame(video: Path, at_seconds: float) -> Image.Image:
    command = [
        "ffmpeg", "-v", "error", "-ss", f"{at_seconds:.3f}", "-i", str(video),
        "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"
    ]
    return Image.open(io.BytesIO(subprocess.check_output(command))).convert("RGB")


def font(size: int) -> ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).is_file():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def captioned_tile(video: Path, cue: Cue, cue_number: int) -> Image.Image:
    tile = video_frame(video, (cue.start + cue.end) / 2).resize((640, 360), Image.Resampling.LANCZOS)
    draw = ImageDraw.Draw(tile, "RGBA")
    lines = textwrap.wrap(cue.text, width=54, break_long_words=False, break_on_hyphens=False)
    caption_font = font(21)
    metadata_font = font(15)
    line_height = 27
    caption_height = max(1, len(lines)) * line_height + 24
    y0 = 360 - caption_height - 22
    draw.rounded_rectangle((24, y0, 616, 338), radius=10, fill=(8, 14, 19, 220), outline=(88, 183, 211, 210), width=2)
    y = y0 + 11
    for line in lines:
        box = draw.textbbox((0, 0), line, font=caption_font)
        draw.text(((640 - (box[2] - box[0])) / 2, y), line, font=caption_font, fill=(245, 248, 250, 255))
        y += line_height
    stamp = f"cue {cue_number:02d} · {cue.start:06.2f}–{cue.end:06.2f}s"
    draw.rounded_rectangle((12, 10, 205, 34), radius=6, fill=(8, 14, 19, 210))
    draw.text((20, 14), stamp, font=metadata_font, fill=(184, 196, 204, 255))
    return tile


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("video", type=Path)
    parser.add_argument("captions", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--samples", type=int, default=12)
    args = parser.parse_args()
    if args.samples < 2:
        raise SystemExit("--samples must be at least 2")

    cues = parse_vtt(args.captions)
    errors: list[str] = []
    for index, cue in enumerate(cues):
        if cue.end <= cue.start:
            errors.append(f"cue {index + 1}: non-positive duration")
        if index and cue.start < cues[index - 1].end:
            errors.append(f"cue {index + 1}: overlaps cue {index}")
        if len(cue.text) > 84:
            errors.append(f"cue {index + 1}: {len(cue.text)} characters exceeds 84")
        if cue.end - cue.start < 0.32:
            errors.append(f"cue {index + 1}: duration below 0.32 seconds")
    if errors:
        raise SystemExit("Caption audit failed:\n - " + "\n - ".join(errors))

    indices = sample_indices(len(cues), min(args.samples, len(cues)))
    tiles = [captioned_tile(args.video, cues[index], index + 1) for index in indices]
    columns = 3
    rows = math.ceil(len(tiles) / columns)
    sheet = Image.new("RGB", (columns * 640, rows * 360), "#101820")
    for index, tile in enumerate(tiles):
        sheet.paste(tile, ((index % columns) * 640, (index // columns) * 360))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(args.output)
    print(f"Caption audit passed: {len(cues)} cues; wrote {len(tiles)} representative frames to {args.output}")


if __name__ == "__main__":
    main()
