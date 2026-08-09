#!/usr/bin/env python3
"""Mux and validate historical generation-one chapter masters."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

from produce_visual_chapter import ROOT, chapter_ids, mux, validate_master, visual


PILOT_VISUALS = {
    "asi-is-a-stack-not-a-model": (
        "build/visual_edition/pilot_outputs/"
        "asi-is-a-stack-not-a-model-local-review.mp4"
    ),
    "capability-replacement-and-rollback": (
        "build/visual_edition/review/"
        "capability-replacement-and-rollback-local-review.mp4"
    ),
    "context-transactions-snapshots-mounts-and-taint": (
        "build/visual_edition/review/"
        "context-transactions-snapshots-mounts-and-taint-local-review.mp4"
    ),
    "replaceable-cognitive-substrates-beyond-transformer-monoculture": (
        "build/visual_edition/review/"
        "replaceable-cognitive-substrates-beyond-transformer-monoculture-local-review.mp4"
    ),
    "living-book-methodology": (
        "build/visual_edition/review/living-book-methodology-local-review.mp4"
    ),
}

PILOT_VISUAL_ENDPOINTS = {
    "asi-is-a-stack-not-a-model": [39, 78, 116, 164, 201, 237, 285],
    "capability-replacement-and-rollback": [39, 78, 118, 162, 200, 244, 285],
    "context-transactions-snapshots-mounts-and-taint": [42, 84, 125, 170, 212, 258, 300],
    "replaceable-cognitive-substrates-beyond-transformer-monoculture": [42, 84, 127, 170, 214, 258, 300],
    "living-book-methodology": [42, 84, 127, 170, 214, 258, 300],
}


def finish(slug: str):
    visual_path = (
        ROOT / PILOT_VISUALS[slug]
        if slug in PILOT_VISUALS
        else visual(slug, False)
    )
    final = mux(slug, visual_path, PILOT_VISUAL_ENDPOINTS.get(slug))
    validate_master(slug, final)
    return slug


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--historical-generation-one",
        action="store_true",
        help="Acknowledge that this bulk mux operates on deprecated generation-one masters.",
    )
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--chapter", action="append", default=[])
    parser.add_argument("--all-chapters", action="store_true")
    args = parser.parse_args()
    if not args.historical_generation_one:
        raise SystemExit(
            "This bulk mux is generation-one historical custody only. "
            "Use generation-two release receipts for current videos."
        )
    selected = (
        chapter_ids(include_pilots=True)
        if args.all_chapters
        else args.chapter or chapter_ids()
    )
    failures = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(finish, slug): slug for slug in selected}
        complete = 0
        for future in as_completed(futures):
            slug = futures[future]
            complete += 1
            try:
                future.result()
                print(f"[{complete}/{len(selected)}] {slug}: validated final master", flush=True)
            except Exception as error:
                failures.append(f"{slug}: {error}")
                print(f"[{complete}/{len(selected)}] {slug}: FAILED {error}", flush=True)
    if failures:
        raise SystemExit("Final-master failures:\n - " + "\n - ".join(failures))


if __name__ == "__main__":
    main()
