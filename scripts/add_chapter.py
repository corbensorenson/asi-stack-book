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
        "source_ids": list(dict.fromkeys(args.source)),
        "problem": "TBD.",
        "insufficient": "TBD.",
        "core_claim": "TBD.",
        "mechanism": [],
        "interfaces": [],
        "invariants": [],
        "failure_modes": [],
        "minimal_implementation": "TBD.",
        "codex_tests": ["TBD"],
    }
    chapters.insert(insert_at, chapter)

    if args.dry_run:
        print(json.dumps(chapter, indent=2))
        return

    save_structure(structure)
    print(f"Added chapter {chapter_id}. Run: python3 scripts/sync_scaffold.py")


if __name__ == "__main__":
    main()
