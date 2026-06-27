#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STRUCTURE = ROOT / "book_structure.json"

HANDOFF_REQUIRED_PARTS = {
    "foundations-alignment-governance",
    "planning-memory-reasoning-execution",
    "routing-compression-representation-substrates",
    "evidence-implementation-living-book",
}
HANDOFF_HEADING_RE = re.compile(r"^## Handoff\s*$", re.MULTILINE)
SUMMARY_HEADING_RE = re.compile(r"^## Summary\s*$", re.MULTILINE)
NEXT_HEADING_RE = re.compile(r"^##\s+", re.MULTILINE)
WORD_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9'_-]*")
NUMBERED_CHAPTER_RE = re.compile(r"\bchapter\s+\d+\b", re.IGNORECASE)

MIN_HANDOFF_WORDS = 45


def fail(errors: list[str]) -> None:
    print("Chapter handoff validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def flatten_chapters(structure: dict) -> list[dict]:
    chapters: list[dict] = []
    for part in structure.get("parts", []):
        for chapter in part.get("chapters", []):
            merged = dict(chapter)
            merged["_part_id"] = part.get("id", "")
            merged["_part_title"] = part.get("title", "")
            chapters.append(merged)
    return chapters


def section_body_after(text: str, match: re.Match[str]) -> str:
    tail = text[match.end() :]
    next_heading = NEXT_HEADING_RE.search(tail)
    if next_heading:
        return tail[: next_heading.start()].strip()
    return tail.strip()


def main() -> None:
    structure = json.loads(STRUCTURE.read_text(encoding="utf-8"))
    if not isinstance(structure, dict):
        fail(["book_structure.json must contain an object."])
    chapters = flatten_chapters(structure)
    errors: list[str] = []
    checked = 0

    for index, chapter in enumerate(chapters):
        if chapter.get("_part_id") not in HANDOFF_REQUIRED_PARTS:
            continue
        checked += 1
        next_chapter = chapters[index + 1] if index + 1 < len(chapters) else None
        path = ROOT / str(chapter.get("file", ""))
        text = path.read_text(encoding="utf-8", errors="ignore")

        handoff_matches = list(HANDOFF_HEADING_RE.finditer(text))
        if len(handoff_matches) != 1:
            errors.append(f"{chapter['file']}: expected exactly one ## Handoff section, found {len(handoff_matches)}.")
            continue

        summary_match = SUMMARY_HEADING_RE.search(text)
        if not summary_match:
            errors.append(f"{chapter['file']}: missing ## Summary before ## Handoff.")
        elif handoff_matches[0].start() < summary_match.start():
            errors.append(f"{chapter['file']}: ## Handoff must appear after ## Summary.")

        body = section_body_after(text, handoff_matches[0])
        words = len(WORD_RE.findall(body))
        if words < MIN_HANDOFF_WORDS:
            errors.append(
                f"{chapter['file']}: ## Handoff has {words} words; expected at least {MIN_HANDOFF_WORDS}."
            )
        if NUMBERED_CHAPTER_RE.search(body):
            errors.append(f"{chapter['file']}: ## Handoff uses a numbered chapter reference.")
        if next_chapter is None:
            if "book" not in body.lower():
                errors.append(f"{chapter['file']}: final handoff should close the book-level arc.")
        else:
            next_title = str(next_chapter.get("title", "")).strip()
            if next_title and next_title not in body:
                errors.append(
                    f"{chapter['file']}: ## Handoff must name next manifest chapter title {next_title!r}."
                )

    if errors:
        fail(errors)

    print(
        "Chapter handoff validation passed: "
        f"{checked} ratcheted chapters checked across {len(HANDOFF_REQUIRED_PARTS)} part(s)."
    )


if __name__ == "__main__":
    main()
