#!/usr/bin/env python3
"""Build canonical WebVTT captions from an exact local narration receipt."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def timestamp(seconds: float) -> str:
    milliseconds = round(seconds * 1000)
    hours, remainder = divmod(milliseconds, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, millis = divmod(remainder, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"


def chunks(text: str, maximum_words: int, minimum_final_words: int = 4) -> list[str]:
    words = text.split()
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
    if len(result) > 1:
        final_words = result[-1].split()
        previous_words = result[-2].split()
        if len(final_words) < minimum_final_words:
            move = min(minimum_final_words - len(final_words), len(previous_words) - 5)
            if move > 0:
                result[-2] = " ".join(previous_words[:-move])
                result[-1] = " ".join(previous_words[-move:] + final_words)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--maximum-words", type=int, default=11)
    args = parser.parse_args()

    receipt_path = ROOT / args.receipt
    output_path = ROOT / args.output
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    cue_id = 1
    cursor = 0.0
    cues: list[tuple[int, float, float, str]] = []
    for segment in receipt["segments"]:
        written = segment["written_text"]
        duration = float(segment["generated_duration_seconds"])
        segment_chunks = chunks(written, args.maximum_words)
        weights = [max(1, len(chunk.split())) for chunk in segment_chunks]
        total_weight = sum(weights)
        cue_cursor = cursor + 0.06
        usable = max(0.1, duration - 0.12)
        for chunk, weight in zip(segment_chunks, weights):
            cue_end = min(cursor + duration - 0.03, cue_cursor + usable * weight / total_weight)
            cues.append((cue_id, cue_cursor, cue_end, chunk))
            cue_id += 1
            cue_cursor = cue_end
        cursor += duration + float(segment["following_pause_seconds"])

    if abs(cursor - float(receipt["duration_seconds"])) > 0.01:
        raise SystemExit(
            f"Receipt segment timing drift: {cursor:.6f} != "
            f"{receipt['duration_seconds']:.6f}"
        )

    lines = [
        "WEBVTT",
        "",
        "NOTE",
        "Canonical written narration timed from the exact local narration render receipt.",
        "Pronunciation-only substitutions are intentionally absent from caption text.",
        "",
    ]
    for number, start, end, text in cues:
        lines.extend(
            [
                str(number),
                f"{timestamp(start)} --> {timestamp(end)}",
                text,
                "",
            ]
        )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Built {len(cues)} exact-receipt cues spanning {cursor:.3f}s.")


if __name__ == "__main__":
    main()
