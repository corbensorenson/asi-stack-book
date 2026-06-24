#!/usr/bin/env python3
"""Generate the proof manifest from proof tags in docs/book_outline.md."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTLINE = ROOT / "docs" / "book_outline.md"
STRUCTURE = ROOT / "book_structure.json"
MANIFEST = ROOT / "proofs" / "proof_manifest.json"

ALLOWED_STATUSES = {"planned", "scaffolded", "implemented", "blocked", "retired"}

STABLE_ID_RE = re.compile(r"^Stable ID: `([^`]+)`")
HEADING_RE = re.compile(r"^### (.+)$")
PROOF_ROW_RE = re.compile(
    r"^\|\s*`(lean:[^`]+)`\s*\|\s*`([^`]+)`\s*\|\s*(.*?)\s*\|\s*([a-z-]+)\s*\|\s*$"
)


def read_json(path: Path) -> object:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def flatten_chapters(structure: dict) -> list[dict]:
    chapters: list[dict] = []
    for part in structure.get("parts", []):
        for chapter in part.get("chapters", []):
            chapters.append(chapter)
    return chapters


def module_path(module: str) -> Path:
    prefix = "AsiStackProofs"
    if module == prefix:
        return ROOT / "lean" / "AsiStackProofs.lean"
    if not module.startswith(prefix + "."):
        return ROOT / "lean" / (module.replace(".", "/") + ".lean")
    rest = module[len(prefix) + 1 :].replace(".", "/")
    return ROOT / "lean" / "AsiStackProofs" / f"{rest}.lean"


def parse_outline() -> list[dict]:
    records: list[dict] = []
    current_title: str | None = None
    current_chapter: str | None = None
    for lineno, line in enumerate(OUTLINE.read_text(encoding="utf-8").splitlines(), start=1):
        heading = HEADING_RE.match(line)
        if heading:
            current_title = heading.group(1)
            current_chapter = None
            continue

        stable = STABLE_ID_RE.match(line)
        if stable:
            current_chapter = stable.group(1)
            continue

        row = PROOF_ROW_RE.match(line)
        if not row:
            continue
        if current_chapter is None or current_title is None:
            raise ValueError(f"Proof row outside a chapter at {OUTLINE}:{lineno}")
        tag, module, target, status = row.groups()
        records.append(
            {
                "chapter_id": current_chapter,
                "chapter_title": current_title,
                "tag": tag,
                "module": module,
                "formal_target": target.strip(),
                "status": status,
                "outline_line": lineno,
                "module_path": str(module_path(module).relative_to(ROOT)),
            }
        )
    return records


def validate_records(records: list[dict]) -> None:
    structure = read_json(STRUCTURE)
    if not isinstance(structure, dict):
        raise ValueError("book_structure.json must contain an object")

    chapters = flatten_chapters(structure)
    known_chapters = {chapter["id"] for chapter in chapters}
    expected_chapters = [chapter["id"] for chapter in chapters]
    by_chapter = Counter(record["chapter_id"] for record in records)
    tags = [record["tag"] for record in records]
    duplicate_tags = sorted(tag for tag, count in Counter(tags).items() if count > 1)

    errors: list[str] = []
    missing = [chapter_id for chapter_id in expected_chapters if by_chapter[chapter_id] == 0]
    if missing:
        errors.append(f"Missing Lean proof targets for chapters: {', '.join(missing)}")
    unknown = sorted(set(by_chapter) - known_chapters)
    if unknown:
        errors.append(f"Unknown chapter IDs in proof tags: {', '.join(unknown)}")
    if duplicate_tags:
        errors.append(f"Duplicate proof tags: {', '.join(duplicate_tags)}")

    for record in records:
        if record["status"] not in ALLOWED_STATUSES:
            errors.append(f"{record['tag']} has invalid status {record['status']!r}")
        if not record["module"].startswith("AsiStackProofs"):
            errors.append(f"{record['tag']} module must start with AsiStackProofs")
        if record["status"] == "implemented" and not (ROOT / record["module_path"]).exists():
            errors.append(f"{record['tag']} is implemented but {record['module_path']} does not exist")

    if errors:
        raise ValueError("\n".join(errors))


def build_manifest(records: list[dict]) -> dict:
    status_counts = Counter(record["status"] for record in records)
    chapter_counts = Counter(record["chapter_id"] for record in records)
    return {
        "generated_from": str(OUTLINE.relative_to(ROOT)),
        "note": "Generated from Lean proof target tables in docs/book_outline.md. Edit the outline, not this file.",
        "proof_target_count": len(records),
        "status_counts": dict(sorted(status_counts.items())),
        "chapter_counts": dict(sorted(chapter_counts.items())),
        "records": records,
    }


def write_manifest(manifest: dict, check: bool) -> None:
    serialized = json.dumps(manifest, indent=2, sort_keys=False) + "\n"
    if check:
        if not MANIFEST.exists():
            raise ValueError(f"{MANIFEST.relative_to(ROOT)} does not exist")
        current = MANIFEST.read_text(encoding="utf-8")
        if current != serialized:
            raise ValueError(f"{MANIFEST.relative_to(ROOT)} is out of date; run scripts/sync_proof_manifest.py")
        return
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(serialized, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Fail if proofs/proof_manifest.json is not current.")
    args = parser.parse_args()

    try:
        records = parse_outline()
        validate_records(records)
        manifest = build_manifest(records)
        write_manifest(manifest, check=args.check)
    except ValueError as exc:
        print(exc)
        sys.exit(1)

    action = "validated" if args.check else "wrote"
    print(f"Proof manifest {action}: {len(records)} targets.")


if __name__ == "__main__":
    main()
