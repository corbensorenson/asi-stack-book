#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
STRUCTURE_PATH = ROOT / "book_structure.json"


def slugify(value: str) -> str:
    text = value.lower().replace("&", " and ")
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-")


def load_structure() -> dict:
    with STRUCTURE_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def save_structure(structure: dict) -> None:
    STRUCTURE_PATH.write_text(json.dumps(structure, indent=2) + "\n", encoding="utf-8")


def find_part(structure: dict, part_id: str) -> dict:
    for part in structure.get("parts", []):
        if part.get("id") == part_id:
            return part
    raise SystemExit(f"No part found: {part_id}")


def flatten_chapters(structure: dict) -> list[dict]:
    chapters = []
    for part in structure.get("parts", []):
        for chapter in part.get("chapters", []):
            merged = dict(chapter)
            merged["_part_id"] = part.get("id", "")
            merged["_part_title"] = part.get("title", "")
            chapters.append(merged)
    return chapters


def print_handoff_repair_notes(structure: dict, chapter_id: str) -> None:
    chapters = flatten_chapters(structure)
    matches = [index for index, chapter in enumerate(chapters) if chapter.get("id") == chapter_id]
    if not matches:
        return
    index = matches[0]
    chapter = chapters[index]
    previous_chapter = chapters[index - 1] if index > 0 else None
    next_chapter = chapters[index + 1] if index + 1 < len(chapters) else None

    print("Handoff repair notes:")
    if previous_chapter:
        print(
            f"- Update `{previous_chapter['file']}` so its `## Handoff` names "
            f"`{chapter['title']}`."
        )
    else:
        print("- No previous chapter Handoff exists because this is now the first manifest chapter.")
    if next_chapter:
        print(
            f"- Draft `{chapter['file']}` with a `## Handoff` after `## Summary` naming "
            f"`{next_chapter['title']}`."
        )
    else:
        print(f"- Draft `{chapter['file']}` with a final `## Handoff` that closes the book-level arc.")
    print(f"- Inspect adjacency with: python3 scripts/chapter_adjacency_report.py --chapter {chapter_id}")
    print("- Validate with: python3 scripts/validate_chapter_handoffs.py")


def main() -> None:
    parser = argparse.ArgumentParser(description="Add a chapter entry to book_structure.json.")
    parser.add_argument("--part", required=True, help="Part ID to insert the chapter into.")
    parser.add_argument("--title", required=True, help="Chapter title.")
    parser.add_argument("--id", help="Stable chapter ID. Defaults to a slug from the title.")
    parser.add_argument("--after", help="Insert after this chapter ID within the same part.")
    parser.add_argument("--before", help="Insert before this chapter ID within the same part.")
    parser.add_argument("--source", action="append", default=[], help="Source ID to assign. Repeatable.")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.after and args.before:
        raise SystemExit("Use only one of --after or --before.")

    structure = load_structure()
    all_ids = {chapter.get("id") for part in structure.get("parts", []) for chapter in part.get("chapters", [])}
    chapter_id = args.id or slugify(args.title)
    if chapter_id in all_ids:
        raise SystemExit(f"Chapter already exists: {chapter_id}")

    part = find_part(structure, args.part)
    chapters = part.setdefault("chapters", [])
    insert_at = len(chapters)
    if args.after:
        matches = [index for index, chapter in enumerate(chapters) if chapter.get("id") == args.after]
        if not matches:
            raise SystemExit(f"No chapter found for --after {args.after} in part {args.part}")
        insert_at = matches[0] + 1
    if args.before:
        matches = [index for index, chapter in enumerate(chapters) if chapter.get("id") == args.before]
        if not matches:
            raise SystemExit(f"No chapter found for --before {args.before} in part {args.part}")
        insert_at = matches[0]

    chapter = {
        "id": chapter_id,
        "title": args.title,
        "file": f"chapters/{chapter_id}.qmd",
        "status": "conceptual",
        "evidence_level": "argument",
        "claim_label": "Design rationale",
        "source_ids": list(dict.fromkeys(args.source)),
        "problem": "No manifest problem statement declared yet.",
        "insufficient": "No manifest insufficiency statement declared yet.",
        "core_claim": "No manifest core claim declared yet.",
        "mechanism": [],
        "interfaces": [],
        "invariants": [],
        "failure_modes": [],
        "minimal_implementation": "No manifest minimal implementation statement declared yet.",
        "beyond_state_of_art": "No manifest beyond-state-of-the-art statement declared yet.",
        "codex_tests": ["Layer claim falsification test"],
    }
    chapters.insert(insert_at, chapter)

    if args.dry_run:
        print(json.dumps(chapter, indent=2))
        print_handoff_repair_notes(structure, chapter_id)
        return

    save_structure(structure)
    print(f"Added chapter {chapter_id}. Run: python3 scripts/sync_scaffold.py")
    print_handoff_repair_notes(structure, chapter_id)


if __name__ == "__main__":
    main()
