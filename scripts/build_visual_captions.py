#!/usr/bin/env python3
"""Build deterministic WebVTT cues from a paragraph-timed narration script."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def timestamp(seconds: float) -> str:
    milliseconds = round(seconds * 1000)
    hours, remainder = divmod(milliseconds, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, millis = divmod(remainder, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"


def chunks(paragraph: str, maximum_words: int) -> list[str]:
    words = paragraph.split()
    result = []
    start = 0
    while start < len(words):
        end = min(start + maximum_words, len(words))
        if end < len(words):
            for candidate in range(end, max(start + 5, end - 4), -1):
                if re.search(r"[,;:.!?]$", words[candidate - 1]):
                    end = candidate
                    break
        result.append(" ".join(words[start:end]))
        start = end
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--narration", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--windows", required=True, help="Comma-separated scene end times in seconds")
    parser.add_argument("--maximum-words", type=int, default=11)
    args = parser.parse_args()
    narration = ROOT / args.narration
    output = ROOT / args.output
    paragraphs = [
        re.sub(r"\s+", " ", paragraph.strip())
        for paragraph in re.split(r"\n\s*\n", narration.read_text(encoding="utf-8"))
        if paragraph.strip()
    ]
    ends = [float(value) for value in args.windows.split(",")]
    if len(paragraphs) != len(ends):
        raise SystemExit(f"Paragraph/window mismatch: {len(paragraphs)} paragraphs, {len(ends)} windows")
    starts = [0.0, *ends[:-1]]
    cues = []
    cue_id = 1
    for paragraph, scene_start, scene_end in zip(paragraphs, starts, ends):
        scene_chunks = chunks(paragraph, args.maximum_words)
        weights = [max(1, len(chunk.split())) for chunk in scene_chunks]
        total = sum(weights)
        cursor = scene_start + 0.2
        usable = max(0.1, scene_end - scene_start - 0.5)
        for chunk, weight in zip(scene_chunks, weights):
            duration = usable * weight / total
            cue_end = min(scene_end - 0.1, cursor + duration)
            cues.append((cue_id, cursor, cue_end, chunk))
            cue_id += 1
            cursor = cue_end
    lines = [
        "WEBVTT",
        "",
        "NOTE",
        "Canonical narration text; deterministic paragraph-window timing.",
        "Text and terminology reviewed against the chapter packet on 2026-07-29.",
        "Publication still requires final listening review against the authorized narration master.",
        "",
    ]
    for cue_id, start, end, chunk in cues:
        lines.extend([
            str(cue_id),
            f"{timestamp(start)} --> {timestamp(end)}",
            chunk,
            "",
        ])
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")
    print(f"Built {len(cues)} WebVTT cues across {len(paragraphs)} timed scenes.")


if __name__ == "__main__":
    main()
