#!/usr/bin/env python3
"""Synchronize manifest-only source assignments into outline source queues.

Named primary/supporting/comparator rows remain authored prose. This adds one
generated reconciliation row only when a manifest assignment is absent from
those rows, so dynamic source intake cannot silently drift from the outline.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTLINE = ROOT / "docs" / "book_outline.md"
STRUCTURE = ROOT / "book_structure.json"
SECTION_RE = re.compile(r"(?m)^### .+$")
STABLE_ID_RE = re.compile(r"(?m)^Stable ID: `([^`]+)`$")
SOURCE_ID_RE = re.compile(r"`([A-Za-z0-9_:-]+)`")
RECONCILIATION_RE = re.compile(r"(?m)^\| Manifest assignment reconciliation \|[^\n]*\n?")


def manifest_sources() -> dict[str, list[str]]:
    structure = json.loads(STRUCTURE.read_text(encoding="utf-8"))
    if not isinstance(structure, dict):
        raise TypeError("book_structure.json must contain an object")
    result: dict[str, list[str]] = {}
    for part in structure.get("parts", []):
        if not isinstance(part, dict):
            continue
        for chapter in part.get("chapters", []):
            if not isinstance(chapter, dict):
                continue
            chapter_id = chapter.get("id")
            source_ids = chapter.get("source_ids", [])
            if isinstance(chapter_id, str) and isinstance(source_ids, list):
                result[chapter_id] = [source_id for source_id in source_ids if isinstance(source_id, str)]
    return result


def reconciliation_row(source_ids: list[str]) -> str:
    sources = ", ".join(f"`{source_id}`" for source_id in source_ids)
    return (
        "| Manifest assignment reconciliation | "
        f"{sources} | Generated from `book_structure.json`: read these assigned "
        "source notes after the authored queue rows; they add drafting context "
        "only and do not promote claim support. |"
    )


def synchronize_outline_source_queues(write: bool = False) -> int:
    expected = manifest_sources()
    text = OUTLINE.read_text(encoding="utf-8")
    starts = [match.start() for match in SECTION_RE.finditer(text)]
    replacements: list[tuple[int, int, str]] = []

    for index, start in enumerate(starts):
        end = starts[index + 1] if index + 1 < len(starts) else len(text)
        section = text[start:end]
        stable_match = STABLE_ID_RE.search(section)
        if not stable_match:
            continue
        source_ids = expected.get(stable_match.group(1), [])
        queue_start = section.find("Source loading queue:")
        draft_start = section.find("Draft arc:", queue_start)
        if queue_start < 0 or draft_start < 0:
            continue

        queue = section[queue_start:draft_start]
        generated = RECONCILIATION_RE.search(queue)
        authored_queue = RECONCILIATION_RE.sub("", queue)
        authored_ids = set(SOURCE_ID_RE.findall(authored_queue))
        supplemental = [source_id for source_id in source_ids if source_id not in authored_ids]

        if generated:
            replacement = reconciliation_row(supplemental) + "\n" if supplemental else ""
            replacements.append((start + queue_start + generated.start(), start + queue_start + generated.end(), replacement))
        elif supplemental:
            insertion = "\n" + reconciliation_row(supplemental) + "\n"
            replacements.append((start + draft_start, start + draft_start, insertion))

    if not replacements:
        return 0

    for start, end, replacement in reversed(replacements):
        text = text[:start] + replacement + text[end:]
    if write:
        OUTLINE.write_text(text, encoding="utf-8")
    return len(replacements)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="Write synchronized outline source-queue rows.")
    args = parser.parse_args()
    changed = synchronize_outline_source_queues(write=args.write)
    action = "wrote" if args.write else "would write"
    print(f"Outline source-queue synchronization {action}: {changed} chapter row(s).")


if __name__ == "__main__":
    main()
