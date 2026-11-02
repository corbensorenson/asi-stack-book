#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re

from projection_files import ProjectionFiles

ROOT = Path(__file__).resolve().parents[1]
STRUCTURE_PATH = ROOT / "book_structure.json"
INVENTORY_PATH = ROOT / "sources/source_inventory.json"


def slugify(value: str) -> str:
    text = value.lower().replace("&", " and ")
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-")


def load_structure() -> dict:
    with STRUCTURE_PATH.open(encoding="utf-8") as f:
        return json.load(f)


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
    parser = argparse.ArgumentParser(description="Prepare a validated chapter proposal without admitting an incomplete canonical owner.")
    parser.add_argument("--part", required=True, help="Part ID to insert the chapter into.")
    parser.add_argument("--title", required=True, help="Chapter title.")
    parser.add_argument("--id", help="Stable chapter ID. Defaults to a slug from the title.")
    parser.add_argument("--after", help="Insert after this chapter ID within the same part.")
    parser.add_argument("--before", help="Insert before this chapter ID within the same part.")
    parser.add_argument("--source", action="append", default=[], help="Source ID to assign. Repeatable.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--proposal-output", type=Path, help="Optional owned JSON proposal below ignored build/; canonical files are never written")
    args = parser.parse_args()

    if args.after and args.before:
        raise SystemExit("Use only one of --after or --before.")

    structure = load_structure()
    all_ids = {chapter.get("id") for part in structure.get("parts", []) for chapter in part.get("chapters", [])}
    title = args.title.strip()
    if not title or any(ord(character) < 32 for character in title):
        parser.error("title must be nonempty and contain no control characters")
    chapter_id = args.id if args.id is not None else slugify(title)
    if not re.fullmatch(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*", chapter_id):
        parser.error("chapter ID must be a nonempty lowercase ASCII slug starting with a letter; supply --id when the title cannot produce one")
    if chapter_id in all_ids:
        raise SystemExit(f"Chapter already exists: {chapter_id}")
    chapter_path = ROOT / f"chapters/{chapter_id}.qmd"
    if chapter_path.exists() or chapter_path.is_symlink():
        parser.error("proposed chapter file already exists; reconcile its existing owner before admission")
    records = json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))
    known_sources = {record["id"] for record in records}
    unknown = sorted(set(args.source) - known_sources)
    if unknown:
        parser.error(f"unknown source IDs: {unknown}; perform source intake before chapter admission")

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
        "title": title,
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

    proposal = {
        "schema_version": "asi_stack.chapter_proposal.v1",
        "admission_state": "not_admitted",
        "manifest_sha256": hashlib.sha256(STRUCTURE_PATH.read_bytes()).hexdigest(),
        "source_inventory_sha256": hashlib.sha256(INVENTORY_PATH.read_bytes()).hexdigest(),
        "part_id": args.part,
        "insert_at": insert_at,
        "chapter": chapter,
        "required_before_admission": [
            "Complete authored manifest fields and substantive chapter prose",
            "Valid source intake, chapter/concept/claim ownership and birth artifacts",
            "Repair both adjacent handoffs and review the reader route",
            "Inspect the current dependency plan, rebuild applicable projections and pass admission checks",
            "Install a complete staged transaction; this proposal is not an admission command",
        ],
        "support_state_effect": "none",
    }
    body = json.dumps(proposal, indent=2, ensure_ascii=False) + "\n"
    if args.proposal_output:
        if args.proposal_output.is_symlink() or any(parent.is_symlink() for parent in args.proposal_output.parents):
            parser.error("--proposal-output must not traverse a symlink")
        output = args.proposal_output.resolve()
        if not output.is_relative_to(ROOT / "build") or output.suffix != ".json":
            parser.error("--proposal-output must be a JSON path below ignored build/")
        if output.exists():
            try:
                previous = json.loads(output.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                parser.error("proposal output contains unrecognized content; choose a fresh path")
            if not isinstance(previous, dict) or previous.get("schema_version") != proposal["schema_version"]:
                parser.error("proposal output is not owned by this proposal format; choose a fresh path")
        ProjectionFiles().write(output, body)
        print(f"Wrote non-admitted proposal: {output.relative_to(ROOT)}")
    else:
        print(body, end="")
    print_handoff_repair_notes(structure, chapter_id)


if __name__ == "__main__":
    main()
