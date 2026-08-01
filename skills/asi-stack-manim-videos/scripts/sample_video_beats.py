#!/usr/bin/env python3
"""Extract start/middle/end frames for every beat and build an HTML review sheet."""

from __future__ import annotations

import argparse
import html
import json
import shutil
import subprocess
import sys
from pathlib import Path


def sample_times(start: float, end: float) -> list[tuple[str, float]]:
    duration = end - start
    inset = min(0.15, max(0.01, duration * 0.05))
    return [
        ("start", start + inset),
        ("middle", start + duration / 2),
        ("end", max(start + inset, end - inset)),
    ]


def self_test() -> None:
    values = sample_times(10.0, 14.0)
    expected = [("start", 10.15), ("middle", 12.0), ("end", 13.85)]
    if any(label != want_label or abs(value - want_value) > 1e-6 for (label, value), (want_label, want_value) in zip(values, expected)):
        raise AssertionError(f"unexpected sample times: {values}")
    print("Self-test passed.")


def extract(video: Path, time_seconds: float, output: Path) -> None:
    command = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-ss",
        f"{time_seconds:.3f}",
        "-i",
        str(video),
        "-frames:v",
        "1",
        "-vf",
        "scale=640:-2:flags=lanczos",
        "-y",
        str(output),
    ]
    process = subprocess.run(command, capture_output=True, text=True, check=False)
    if process.returncode:
        raise RuntimeError(process.stderr.strip() or "ffmpeg frame extraction failed")


def build(video: Path, plan_path: Path, output_dir: Path) -> tuple[Path, int]:
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    beats = plan.get("beats")
    if not isinstance(beats, list) or not beats:
        raise ValueError("beat plan has no beats")
    output_dir.mkdir(parents=True, exist_ok=True)
    cards: list[str] = []
    image_count = 0
    for index, beat in enumerate(beats):
        if not isinstance(beat, dict):
            raise ValueError(f"beat[{index}] is not an object")
        beat_id = str(beat.get("id") or f"beat-{index + 1:03d}")
        start = beat.get("start_seconds")
        end = beat.get("end_seconds")
        if not isinstance(start, (int, float)) or not isinstance(end, (int, float)) or end <= start:
            raise ValueError(f"{beat_id} has invalid timing")
        figures: list[str] = []
        for position, timestamp in sample_times(float(start), float(end)):
            # PNG avoids FFmpeg 8's refusal to emit non-full-range JPEG frames
            # from the usual limited-range H.264 YouTube/Manim source. Review
            # sheets are diagnostic artifacts, so predictable extraction is
            # more valuable than JPEG's smaller files.
            filename = f"{index + 1:03d}_{beat_id}_{position}.png"
            extract(video, timestamp, output_dir / filename)
            image_count += 1
            figures.append(
                f'<figure><img src="{html.escape(filename)}" alt="{html.escape(beat_id)} {position} frame">'
                f'<figcaption>{position} · {timestamp:.2f}s</figcaption></figure>'
            )
        narration = html.escape(str(beat.get("narration", "")))
        target = html.escape(str(beat.get("attention_target", "")))
        purpose = html.escape(str(beat.get("visual_purpose", "")))
        cards.append(
            f'<section><h2>{html.escape(beat_id)} · {html.escape(str(beat.get("story_function", "")))}</h2>'
            f'<p><strong>Attention:</strong> {target}</p><p><strong>Purpose:</strong> {purpose}</p>'
            f'<p><strong>Narration:</strong> {narration}</p><div class="frames">{"".join(figures)}</div></section>'
        )
    style = """
body{margin:0;background:#101820;color:#f4f6f7;font:16px system-ui,sans-serif}main{max-width:1500px;margin:auto;padding:32px}
section{background:#182630;border:1px solid #36505e;border-radius:16px;margin:24px 0;padding:20px}h1,h2{margin:.2em 0 .5em}p{color:#d9e1e5}
.frames{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}figure{margin:0}img{width:100%;border-radius:8px;background:#000}figcaption{color:#aebbc2;margin-top:6px}
@media(max-width:800px){.frames{grid-template-columns:1fr}main{padding:14px}}
"""
    title = html.escape(str(plan.get("chapter_id", "chapter")))
    document = f"<!doctype html><meta charset='utf-8'><title>{title} beat review</title><style>{style}</style><main><h1>{title} · beat review</h1>{''.join(cards)}</main>"
    index_path = output_dir / "index.html"
    index_path.write_text(document, encoding="utf-8")
    return index_path, image_count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("video", type=Path, nargs="?")
    parser.add_argument("plan", type=Path, nargs="?")
    parser.add_argument("output_dir", type=Path, nargs="?")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    if args.video is None or args.plan is None or args.output_dir is None:
        parser.error("video, plan, and output_dir are required unless --self-test is used")
    if shutil.which("ffmpeg") is None:
        raise SystemExit("required executable is unavailable: ffmpeg")
    try:
        index_path, image_count = build(args.video, args.plan, args.output_dir)
    except (OSError, ValueError, json.JSONDecodeError, RuntimeError) as exc:
        raise SystemExit(f"Unable to build beat review sheet: {exc}") from exc
    print(f"Wrote {image_count} samples and {index_path}")


if __name__ == "__main__":
    main()
