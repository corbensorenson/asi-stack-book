#!/usr/bin/env python3
"""Validate per-chapter Human Reading Path blocks.

The live book uses `.asi-human-only` fenced divs to provide interested-human
orientation while keeping the default AI/research view dense and auditable.
Every manifest chapter should have exactly one Human Reading Path block, and
reader-edition generation should unwrap that block into ordinary prose.
"""

from __future__ import annotations

import json
import re
import sys
import tempfile
from pathlib import Path

import build_reader_edition

ROOT = Path(__file__).resolve().parents[1]
HUMAN_CLASS = "asi-human-only"
HUMAN_HEADING = "## Human Reading Path"
MIN_BRIDGE_WORDS = 65
MAX_BRIDGE_WORDS = 180
WORD_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9'_-]*")
OPEN_RE = re.compile(r"^(:{3,})\s+\{([^}]*)\}\s*$")
CLOSE_RE = re.compile(r"^(:{3,})\s*$")
BANNED_BRIDGE_PHRASES = (
    "For a human reader",
    "For the reader",
)


def load_structure() -> dict:
    value = json.loads((ROOT / "book_structure.json").read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError("book_structure.json must contain an object")
    return value


def flatten_chapters(structure: dict) -> list[dict]:
    chapters: list[dict] = []
    for part in structure.get("parts", []):
        if not isinstance(part, dict):
            continue
        for chapter in part.get("chapters", []):
            if isinstance(chapter, dict):
                merged = dict(chapter)
                merged["_part_id"] = part.get("id", "")
                chapters.append(merged)
    return chapters


def fenced_div_classes(attributes: str) -> set[str]:
    return {match.group(1) for match in re.finditer(r"\.([A-Za-z0-9_-]+)", attributes)}


def extract_human_blocks(text: str) -> list[dict[str, object]]:
    lines = text.splitlines()
    blocks: list[dict[str, object]] = []
    active: dict[str, object] | None = None

    for index, line in enumerate(lines, start=1):
        if active is None:
            open_match = OPEN_RE.match(line)
            if not open_match:
                continue
            if HUMAN_CLASS not in fenced_div_classes(open_match.group(2)):
                continue
            active = {
                "start": index,
                "fence": len(open_match.group(1)),
                "lines": [],
            }
            continue

        close_match = CLOSE_RE.match(line)
        if close_match and len(close_match.group(1)) >= int(active["fence"]):
            blocks.append(
                {
                    "start": active["start"],
                    "end": index,
                    "text": "\n".join(active["lines"]),
                }
            )
            active = None
            continue

        active["lines"].append(line)  # type: ignore[index]

    if active is not None:
        blocks.append(
            {
                "start": active["start"],
                "end": None,
                "text": "\n".join(active["lines"]),  # type: ignore[index]
            }
        )

    return blocks


def word_count(text: str) -> int:
    return len(WORD_RE.findall(re.sub(r"```.*?```", " ", text, flags=re.DOTALL)))


def heading_line(text: str, heading: str) -> int | None:
    for index, line in enumerate(text.splitlines(), start=1):
        if line.strip() == heading:
            return index
    return None


def heading_order_ok(text: str, block: dict[str, object]) -> bool:
    drafting = heading_line(text, "## Drafting guardrail")
    problem = heading_line(text, "## Problem")
    start_line = int(block["start"])
    return drafting is not None and problem is not None and drafting < start_line < problem


def validate_source_chapters(chapters: list[dict]) -> tuple[list[dict[str, object]], list[str]]:
    records: list[dict[str, object]] = []
    errors: list[str] = []
    for chapter in chapters:
        chapter_id = str(chapter.get("id", ""))
        relative = str(chapter.get("file", ""))
        path = ROOT / relative
        text = path.read_text(encoding="utf-8", errors="ignore")
        blocks = extract_human_blocks(text)

        if len(blocks) != 1:
            errors.append(f"{relative}: expected exactly one .{HUMAN_CLASS} block, found {len(blocks)}.")
            continue

        block = blocks[0]
        block_text = str(block["text"])
        words = word_count(block_text)
        record = {
            "chapter_id": chapter_id,
            "file": relative,
            "start_line": block["start"],
            "word_count": words,
        }
        records.append(record)

        if block["end"] is None:
            errors.append(f"{relative}: .{HUMAN_CLASS} block is not closed.")
        if HUMAN_HEADING not in block_text:
            errors.append(f"{relative}: .{HUMAN_CLASS} block must contain {HUMAN_HEADING!r}.")
        if not heading_order_ok(text, block):
            errors.append(f"{relative}: Human Reading Path must appear after Drafting guardrail and before Problem.")
        if words < MIN_BRIDGE_WORDS:
            errors.append(f"{relative}: Human Reading Path has {words} words; minimum is {MIN_BRIDGE_WORDS}.")
        if words > MAX_BRIDGE_WORDS:
            errors.append(f"{relative}: Human Reading Path has {words} words; maximum is {MAX_BRIDGE_WORDS}.")
        if "::: " in block_text or f".{HUMAN_CLASS}" in block_text:
            errors.append(f"{relative}: Human Reading Path text contains a nested fenced-div marker.")
        for phrase in BANNED_BRIDGE_PHRASES:
            if phrase in block_text:
                errors.append(f"{relative}: Human Reading Path uses meta-reader phrase {phrase!r}.")
        for forbidden in ("## Chapter status", "## Drafting guardrail", "## Codex test plan", "## Source crosswalk"):
            if forbidden in block_text:
                errors.append(f"{relative}: Human Reading Path contains live-only heading {forbidden!r}.")

    return records, errors


def validate_generated_reader(chapters: list[dict]) -> list[str]:
    errors: list[str] = []
    with tempfile.TemporaryDirectory(prefix="asi-human-reader-paths-") as temp_dir:
        output_dir = Path(temp_dir)
        build_reader_edition.generate(output_dir, "reader_release")
        for chapter in chapters:
            relative = str(chapter.get("file", ""))
            path = output_dir / relative
            if not path.exists():
                errors.append(f"{relative}: generated reader chapter missing.")
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            heading_count = text.count(HUMAN_HEADING)
            if heading_count != 1:
                errors.append(f"{relative}: generated reader chapter has {heading_count} Human Reading Path headings.")
            if f".{HUMAN_CLASS}" in text:
                errors.append(f"{relative}: generated reader chapter still contains .{HUMAN_CLASS} marker.")
    return errors


def main() -> None:
    chapters = flatten_chapters(load_structure())
    records, errors = validate_source_chapters(chapters)
    errors.extend(validate_generated_reader(chapters))

    if errors:
        print("Human Reading Path validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    min_words = min((int(record["word_count"]) for record in records), default=0)
    print(
        "Human Reading Path validation passed: "
        f"{len(records)} chapters, minimum bridge words {min_words}."
    )


if __name__ == "__main__":
    main()
