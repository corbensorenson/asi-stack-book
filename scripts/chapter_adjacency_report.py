#!/usr/bin/env python3
"""Report manifest chapter adjacency and handoff repair targets."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
STRUCTURE_PATH = ROOT / "book_structure.json"


def load_structure() -> dict:
    value = json.loads(STRUCTURE_PATH.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError("book_structure.json must contain an object")
    return value


def flatten_chapters(structure: dict) -> list[dict[str, object]]:
    chapters: list[dict[str, object]] = []
    for part_index, part in enumerate(structure.get("parts", []), start=1):
        if not isinstance(part, dict):
            continue
        for chapter_index, chapter in enumerate(part.get("chapters", []), start=1):
            if not isinstance(chapter, dict):
                continue
            merged = dict(chapter)
            merged["_book_index"] = len(chapters) + 1
            merged["_part_index"] = part_index
            merged["_chapter_index_in_part"] = chapter_index
            merged["_part_id"] = part.get("id", "")
            merged["_part_title"] = part.get("title", "")
            chapters.append(merged)
    return chapters


def ref(chapter: dict[str, object] | None) -> dict[str, object] | None:
    if chapter is None:
        return None
    return {
        "id": chapter.get("id", ""),
        "title": chapter.get("title", ""),
        "file": chapter.get("file", ""),
        "book_index": chapter.get("_book_index", 0),
        "part_id": chapter.get("_part_id", ""),
        "part_title": chapter.get("_part_title", ""),
    }


def adjacency_records(chapters: list[dict[str, object]]) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for index, chapter in enumerate(chapters):
        previous_chapter = chapters[index - 1] if index > 0 else None
        next_chapter = chapters[index + 1] if index + 1 < len(chapters) else None
        next_title = str(next_chapter.get("title", "")).strip() if next_chapter else ""
        records.append(
            {
                "id": chapter.get("id", ""),
                "title": chapter.get("title", ""),
                "file": chapter.get("file", ""),
                "book_index": chapter.get("_book_index", 0),
                "part_id": chapter.get("_part_id", ""),
                "part_title": chapter.get("_part_title", ""),
                "previous": ref(previous_chapter),
                "next": ref(next_chapter),
                "handoff_rule": (
                    f"Current chapter Handoff should name {next_title!r}."
                    if next_chapter
                    else "Current chapter Handoff should close the book-level arc."
                ),
                "previous_handoff_repair": (
                    f"Previous chapter Handoff in {previous_chapter.get('file')} should name "
                    f"{chapter.get('title')!r}."
                    if previous_chapter
                    else "No previous chapter Handoff repair; this is the first manifest chapter."
                ),
            }
        )
    return records


def select_records(
    records: list[dict[str, object]],
    chapter_ids: list[str],
) -> list[dict[str, object]]:
    if not chapter_ids:
        return records
    wanted = set(chapter_ids)
    selected = [record for record in records if str(record.get("id", "")) in wanted]
    found = {str(record.get("id", "")) for record in selected}
    missing = sorted(wanted - found)
    if missing:
        raise SystemExit(f"Unknown chapter id(s): {', '.join(missing)}")
    return selected


def removal_record(records: list[dict[str, object]], chapter_id: str) -> dict[str, object]:
    matches = [record for record in records if record.get("id") == chapter_id]
    if not matches:
        raise SystemExit(f"Unknown chapter id: {chapter_id}")
    record = matches[0]
    previous_chapter = record.get("previous")
    next_chapter = record.get("next")
    if previous_chapter and next_chapter:
        repair = (
            f"If removing or merging {record.get('title')!r}, update the previous chapter Handoff "
            f"in {previous_chapter.get('file')} to name {next_chapter.get('title')!r}."
        )
    elif previous_chapter:
        repair = (
            f"If removing or merging final chapter {record.get('title')!r}, update the previous "
            f"chapter Handoff in {previous_chapter.get('file')} to close the book-level arc."
        )
    elif next_chapter:
        repair = (
            f"If removing first chapter {record.get('title')!r}, no previous Handoff exists; "
            f"confirm {next_chapter.get('title')!r} is now the intended opening chapter."
        )
    else:
        repair = "This is the only manifest chapter; removal would leave no chapter spine."
    return {
        "removed_chapter": record,
        "repair": repair,
        "validation": [
            "python3 scripts/sync_scaffold.py",
            "python3 scripts/validate_chapter_handoffs.py",
            "python3 scripts/validate_outline_consistency.py",
            "python3 scripts/validate_book.py",
        ],
    }


def print_text(records: list[dict[str, object]], removal: dict[str, object] | None) -> None:
    if removal:
        removed = removal["removed_chapter"]
        print(f"Removal or merge repair for {removed['id']} ({removed['title']}):")
        print(f"- {removal['repair']}")
        print("- Then run:")
        for command in removal["validation"]:
            print(f"  - {command}")
        return

    print("Chapter adjacency report from book_structure.json")
    for record in records:
        previous_chapter = record.get("previous")
        next_chapter = record.get("next")
        previous_label = (
            f"{previous_chapter['title']} ({previous_chapter['id']})"
            if previous_chapter
            else "none"
        )
        next_label = f"{next_chapter['title']} ({next_chapter['id']})" if next_chapter else "none"
        print(f"- {record['book_index']:02}. {record['title']} ({record['id']})")
        print(f"  file: {record['file']}")
        print(f"  previous: {previous_label}")
        print(f"  next: {next_label}")
        print(f"  current rule: {record['handoff_rule']}")
        print(f"  adjacent repair: {record['previous_handoff_repair']}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chapter", action="append", default=[], help="Chapter ID to report. Repeatable.")
    parser.add_argument("--if-removing", help="Show the predecessor Handoff repair if this chapter is removed or merged.")
    parser.add_argument("--json", action="store_true", help="Write machine-readable JSON instead of text.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.chapter and args.if_removing:
        raise SystemExit("Use either --chapter or --if-removing, not both.")

    records = adjacency_records(flatten_chapters(load_structure()))
    removal = removal_record(records, args.if_removing) if args.if_removing else None
    selected = select_records(records, args.chapter)

    if args.json:
        payload: object = removal if removal else {"chapters": selected}
        json.dump(payload, sys.stdout, indent=2)
        print()
        return

    print_text(selected, removal)


if __name__ == "__main__":
    main()
