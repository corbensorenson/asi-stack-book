#!/usr/bin/env python3
"""Bind historical generation-one scenes to seven paragraph boundaries."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PILOTS = {
    "asi-is-a-stack-not-a-model",
    "capability-replacement-and-rollback",
    "context-transactions-snapshots-mounts-and-taint",
    "replaceable-cognitive-substrates-beyond-transformer-monoculture",
    "living-book-methodology",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stamp(seconds: float) -> str:
    rounded = int(round(seconds))
    return f"{rounded // 60:02d}:{rounded % 60:02d}"


def chapter_ids() -> list[str]:
    structure = json.loads((ROOT / "book_structure.json").read_text(encoding="utf-8"))
    return [
        chapter["id"]
        for part in structure["parts"]
        for chapter in part["chapters"]
        if chapter["id"] not in PILOTS
    ]


def synchronize(slug: str) -> None:
    receipt_path = (
        ROOT / f"build/visual_edition/audio/{slug}-narration-master.receipt.json"
    )
    if not receipt_path.is_file():
        raise FileNotFoundError(f"narration receipt missing: {receipt_path}")
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    elapsed = 0.0
    endpoints: list[float] = []
    for segment in receipt["segments"]:
        elapsed += float(segment["generated_duration_seconds"])
        elapsed += float(segment["following_pause_seconds"])
        if segment["paragraph_end"]:
            endpoints.append(round(elapsed, 6))
    if len(endpoints) != 7:
        raise ValueError(f"{slug}: expected 7 narrated paragraphs, found {len(endpoints)}")
    duration = float(receipt["duration_seconds"])
    if abs(endpoints[-1] - duration) > 0.25:
        raise ValueError(
            f"{slug}: paragraph timing ends at {endpoints[-1]}, audio ends at {duration}"
        )
    endpoints[-1] = round(duration, 6)

    directory = ROOT / "visual_edition/chapters" / slug
    spec_path = directory / "scene_spec.json"
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    spec["timing"] = {
        "basis": "exact_narration_paragraph_boundaries",
        "narration_receipt_sha256": sha256(receipt_path),
        "target_duration_seconds": round(duration, 6),
        "scene_endpoints_seconds": endpoints,
    }
    rendered_spec = json.dumps(spec, indent=2, ensure_ascii=False) + "\n"
    if spec_path.read_text(encoding="utf-8") != rendered_spec:
        spec_path.write_text(rendered_spec, encoding="utf-8")

    starts = [0.0, *endpoints[:-1]]
    replacements = [
        f"{stamp(start)}–{stamp(end)}" for start, end in zip(starts, endpoints)
    ]
    for filename in ("storyboard.md", "transcript.md"):
        path = directory / filename
        value = path.read_text(encoding="utf-8")
        iterator = iter(replacements)
        value, count = re.subn(
            r"\b\d{2}:\d{2}–\d{2}:\d{2}\b",
            lambda _match: next(iterator),
            value,
            count=7,
        )
        if count != 7:
            raise ValueError(f"{slug}: expected 7 time ranges in {filename}, found {count}")
        if filename == "storyboard.md":
            value = re.sub(
                r"Target visual duration: [^.]+\.",
                (
                    f"Target visual duration: {duration:.3f} seconds, bound to the "
                    "exact final narration receipt."
                ),
                value,
                count=1,
            )
        if path.read_text(encoding="utf-8") != value:
            path.write_text(value, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--historical-generation-one",
        action="store_true",
        help="Acknowledge the deprecated seven-paragraph timing model.",
    )
    parser.add_argument("--chapter", action="append", default=[])
    parser.add_argument("--all-non-pilots", action="store_true")
    args = parser.parse_args()
    if not args.historical_generation_one:
        raise SystemExit(
            "Seven-paragraph timing synchronization is generation-one historical "
            "custody only. Use audio-aligned generation-two beat plans instead."
        )
    selected = chapter_ids() if args.all_non_pilots else args.chapter
    if not selected:
        raise SystemExit("Select --chapter or --all-non-pilots")
    failures = []
    for slug in selected:
        try:
            synchronize(slug)
            print(f"{slug}: timing synchronized")
        except Exception as error:
            failures.append(f"{slug}: {error}")
    if failures:
        raise SystemExit("Timing synchronization failures:\n - " + "\n - ".join(failures))


if __name__ == "__main__":
    main()
