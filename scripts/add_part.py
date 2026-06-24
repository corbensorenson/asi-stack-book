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


def main() -> None:
    parser = argparse.ArgumentParser(description="Add a part to book_structure.json.")
    parser.add_argument("--title", required=True, help="Part title as it should appear in the rendered book.")
    parser.add_argument("--id", help="Stable part ID. Defaults to a slug from the title.")
    parser.add_argument("--after", help="Insert after this existing part ID.")
    parser.add_argument("--before", help="Insert before this existing part ID.")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.after and args.before:
        raise SystemExit("Use only one of --after or --before.")

    structure = load_structure()
    part_id = args.id or slugify(args.title)
    parts = structure.setdefault("parts", [])
    if any(part.get("id") == part_id for part in parts):
        raise SystemExit(f"Part already exists: {part_id}")

    insert_at = len(parts)
    if args.after:
        matches = [index for index, part in enumerate(parts) if part.get("id") == args.after]
        if not matches:
            raise SystemExit(f"No part found for --after {args.after}")
        insert_at = matches[0] + 1
    if args.before:
        matches = [index for index, part in enumerate(parts) if part.get("id") == args.before]
        if not matches:
            raise SystemExit(f"No part found for --before {args.before}")
        insert_at = matches[0]

    part = {"id": part_id, "title": args.title, "chapters": []}
    parts.insert(insert_at, part)

    if args.dry_run:
        print(json.dumps(part, indent=2))
        return

    save_structure(structure)
    print(f"Added part {part_id}. Run: python3 scripts/sync_scaffold.py")


if __name__ == "__main__":
    main()
