#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES_DIR = ROOT / "sources" / "source_notes"
MANIFEST = NOTES_DIR / "backbone_manifest.json"
STRUCTURE = ROOT / "book_structure.json"
SOURCE_INVENTORY = ROOT / "sources" / "source_inventory.json"

REQUIRED_SECTIONS = [
    "## Thesis",
    "## Mechanisms",
    "## Evidence",
    "## Failure Modes",
    "## Book Chapters Supported",
    "## Claims To Add Or Update",
    "## Open Questions",
]

SUPPORT_REQUIRING_NOTES = {
    "source-derived",
    "prototype-backed",
    "synthetic-test-backed",
    "empirical-test-backed",
    "external-literature-backed",
}


def read_json(path: Path) -> object:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def frontmatter_field(text: str, label: str) -> str | None:
    pattern = rf"\|\s*{re.escape(label)}\s*\|\s*([^|]+?)\s*\|"
    match = re.search(pattern, text)
    return match.group(1).strip() if match else None


def flatten_chapters(structure: dict) -> list[dict]:
    chapters: list[dict] = []
    for part in structure.get("parts", []):
        chapters.extend(part.get("chapters", []))
    return chapters


def assigned_source_ids(structure: dict) -> set[str]:
    source_ids: set[str] = set()
    for chapter in flatten_chapters(structure):
        for source_id in chapter.get("source_ids", []):
            if isinstance(source_id, str):
                source_ids.add(source_id)
    return source_ids


def inventory_source_ids() -> set[str]:
    if not SOURCE_INVENTORY.exists():
        return set()
    inventory = read_json(SOURCE_INVENTORY)
    if not isinstance(inventory, list):
        return set()
    return {str(record.get("id", "")) for record in inventory if isinstance(record, dict) and record.get("id")}


def validate_note(source_id: str, errors: list[str]) -> None:
    path = NOTES_DIR / f"{source_id}.md"
    if not path.exists():
        errors.append(f"`{source_id}`: missing {path.relative_to(ROOT)}")
        return
    text = path.read_text(encoding="utf-8", errors="ignore")
    for section in REQUIRED_SECTIONS:
        if section not in text:
            errors.append(f"`{source_id}`: missing section {section}")
    actual_id = frontmatter_field(text, "Source ID")
    if actual_id != f"`{source_id}`":
        errors.append(f"`{source_id}`: Source ID field is {actual_id!r}")
    if "TBD" in text:
        errors.append(f"`{source_id}`: source note still contains TBD")
    if "Do not fill this until" in text:
        errors.append(f"`{source_id}`: source note still contains template guard text")


def main() -> None:
    if not MANIFEST.exists():
        raise SystemExit("Missing sources/source_notes/backbone_manifest.json.")
    manifest = read_json(MANIFEST)
    if not isinstance(manifest, dict):
        raise SystemExit("sources/source_notes/backbone_manifest.json must contain an object.")

    required = manifest.get("note_required_for", [])
    if not isinstance(required, list) or not all(isinstance(item, str) for item in required):
        raise SystemExit("note_required_for must be a list of source IDs.")

    structure = read_json(STRUCTURE)
    if not isinstance(structure, dict):
        raise SystemExit("book_structure.json must contain an object.")

    assigned = assigned_source_ids(structure)
    inventory_ids = inventory_source_ids()
    required_set = set(required)
    notes_to_validate = required_set | assigned

    errors: list[str] = []
    missing_inventory = sorted(source_id for source_id in assigned if source_id not in inventory_ids)
    for source_id in missing_inventory:
        errors.append(f"`{source_id}`: assigned in book_structure.json but missing from sources/source_inventory.json")

    for source_id in sorted(notes_to_validate):
        validate_note(source_id, errors)

    for path in sorted(NOTES_DIR.glob("*.md")):
        if path.name in {"README.md", "_template.md"}:
            continue
        validate_note(path.stem, errors)

    for chapter in flatten_chapters(structure):
        if chapter.get("evidence_level") in SUPPORT_REQUIRING_NOTES:
            missing = [source_id for source_id in chapter.get("source_ids", []) if not (NOTES_DIR / f"{source_id}.md").exists()]
            if missing:
                errors.append(
                    f"{chapter.get('id')}: evidence_level {chapter.get('evidence_level')!r} requires source notes for {', '.join(missing)}"
                )

    if errors:
        print("Source-note validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    checked = len(
        {
            path.stem
            for path in NOTES_DIR.glob("*.md")
            if path.name not in {"README.md", "_template.md"}
        }
        | notes_to_validate
    )
    print(f"Source-note validation passed: {len(required)} required backbone notes, {len(assigned)} assigned source notes, {checked} total notes checked.")


if __name__ == "__main__":
    main()
