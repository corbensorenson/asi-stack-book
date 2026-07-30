#!/usr/bin/env python3
"""Render non-pilot Manim release visuals with bounded CPU parallelism."""

from __future__ import annotations

import argparse
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIM = ROOT / "build/visual_edition/venv/bin/manim"
PILOTS = {
    "asi-is-a-stack-not-a-model",
    "capability-replacement-and-rollback",
    "context-transactions-snapshots-mounts-and-taint",
    "replaceable-cognitive-substrates-beyond-transformer-monoculture",
    "living-book-methodology",
}


def chapters(timed_only: bool = False) -> list[str]:
    structure = json.loads((ROOT / "book_structure.json").read_text(encoding="utf-8"))
    selected = [
        chapter["id"]
        for part in structure["parts"]
        for chapter in part["chapters"]
        if chapter["id"] not in PILOTS
    ]
    if timed_only:
        selected = [
            slug
            for slug in selected
            if "timing" in json.loads(
                (
                    ROOT / f"visual_edition/chapters/{slug}/scene_spec.json"
                ).read_text(encoding="utf-8")
            )
        ]
    return selected


def render(slug: str, force: bool) -> tuple[str, str]:
    directory = ROOT / "build/visual_edition/render" / slug
    output = directory / "videos/scene/1080p30/ChapterVisualAbstract.mp4"
    inputs = [
        ROOT / f"visual_edition/chapters/{slug}/scene.py",
        ROOT / f"visual_edition/chapters/{slug}/scene_spec.json",
        ROOT / "visual_edition/lib/chapter_scene.py",
        ROOT / "visual_edition/lib/asi_visuals.py",
        ROOT / "visual_edition/manim.cfg",
    ]
    current = (
        output.is_file()
        and output.stat().st_mtime >= max(path.stat().st_mtime for path in inputs)
    )
    if current and not force:
        return slug, "current"
    directory.mkdir(parents=True, exist_ok=True)
    with (directory / "manim.log").open("w", encoding="utf-8") as log:
        subprocess.run(
            [
                str(MANIM),
                "--config_file", "visual_edition/manim.cfg",
                "--disable_caching",
                f"visual_edition/chapters/{slug}/scene.py",
                "ChapterVisualAbstract",
                "--media_dir", f"build/visual_edition/render/{slug}",
            ],
            cwd=ROOT,
            check=True,
            stdout=log,
            stderr=subprocess.STDOUT,
        )
    if not output.is_file():
        raise RuntimeError(f"render output missing: {slug}")
    return slug, "rendered"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--force", action="store_true")
    parser.add_argument(
        "--timed-only",
        action="store_true",
        help="Render only chapters already bound to exact narration timing.",
    )
    args = parser.parse_args()
    selected = chapters(args.timed_only)
    failures = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(render, slug, args.force): slug for slug in selected}
        completed = 0
        for future in as_completed(futures):
            slug = futures[future]
            completed += 1
            try:
                _, state = future.result()
                print(f"[{completed}/{len(selected)}] {slug}: {state}", flush=True)
            except Exception as error:
                failures.append(f"{slug}: {error}")
                print(f"[{completed}/{len(selected)}] {slug}: FAILED {error}", flush=True)
    if failures:
        raise SystemExit("Visual render failures:\n - " + "\n - ".join(failures))


if __name__ == "__main__":
    main()
