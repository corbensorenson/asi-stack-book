#!/usr/bin/env python3
"""Validate docs/book_outline.md against book_structure.json.

`book_structure.json` owns ordering. `docs/book_outline.md` owns drafting jobs,
source queues, and Lean proof scope. This guard keeps those two source-of-truth
surfaces aligned without requiring the outline to duplicate every manifest field.
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTLINE = ROOT / "docs" / "book_outline.md"
STRUCTURE = ROOT / "book_structure.json"

HEADING_RE = re.compile(r"^### (.+)$")
PART_RE = re.compile(r"^## Part .+$")
STABLE_ID_RE = re.compile(r"^Stable ID: `([^`]+)`")
CORE_CLAIM_RE = re.compile(r"^Core claim: (.+)$")
SOURCE_ID_RE = re.compile(r"`([A-Za-z0-9_:-]+)`")
PROOF_ROW_RE = re.compile(
    r"^\|\s*`(lean:[^`]+)`\s*\|\s*`([^`]+)`\s*\|\s*(.*?)\s*\|\s*([a-z-]+)\s*\|\s*$"
)


def fail(errors: list[str]) -> None:
    print("Outline consistency validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def load_structure() -> dict:
    value = json.loads(STRUCTURE.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        fail(["book_structure.json must contain an object."])
    return value


def flatten_chapters(structure: dict) -> list[dict]:
    return [chapter for part in structure.get("parts", []) for chapter in part.get("chapters", [])]


def parse_outline_sections() -> list[dict]:
    lines = OUTLINE.read_text(encoding="utf-8").splitlines()
    sections: list[dict] = []
    current: dict | None = None

    for lineno, line in enumerate(lines, start=1):
        heading = HEADING_RE.match(line)
        if heading:
            if current is not None:
                sections.append(current)
            current = {
                "title": heading.group(1),
                "heading_line": lineno,
                "stable_id": None,
                "stable_line": None,
                "lines": [line],
            }
            continue

        if PART_RE.match(line) and current is not None:
            sections.append(current)
            current = None

        if current is None:
            continue

        current["lines"].append(line)
        stable = STABLE_ID_RE.match(line)
        if stable:
            current["stable_id"] = stable.group(1)
            current["stable_line"] = lineno

    if current is not None:
        sections.append(current)

    return [section for section in sections if section.get("stable_id")]


def outline_source_ids(section: dict) -> set[str]:
    text = "\n".join(section["lines"])
    if "Source loading queue:" not in text:
        return set()
    after_queue = text.split("Source loading queue:", 1)[1]
    before_next = after_queue.split("Draft arc:", 1)[0]
    return {item for item in SOURCE_ID_RE.findall(before_next) if not item.startswith("lean:")}


def outline_proofs(section: dict) -> dict[str, dict]:
    proofs: dict[str, dict] = {}
    for line in section["lines"]:
        row = PROOF_ROW_RE.match(line)
        if not row:
            continue
        tag, module, target, status = row.groups()
        proofs[tag] = {
            "module": module,
            "target": target.strip(),
            "status": status,
        }
    return proofs


def outline_core_claim(section: dict) -> str | None:
    for line in section["lines"]:
        match = CORE_CLAIM_RE.match(line)
        if match:
            return match.group(1).strip()
    return None


def main() -> None:
    errors: list[str] = []
    chapters = flatten_chapters(load_structure())
    sections = parse_outline_sections()
    sections_by_id = {section["stable_id"]: section for section in sections}
    manifest_ids = [str(chapter.get("id", "")) for chapter in chapters]
    outline_ids = [str(section.get("stable_id", "")) for section in sections]

    duplicate_outline_ids = sorted(item for item, count in Counter(outline_ids).items() if count > 1)
    if duplicate_outline_ids:
        errors.append(f"Duplicate Stable ID entries in outline: {duplicate_outline_ids}")

    missing = [chapter_id for chapter_id in manifest_ids if chapter_id not in sections_by_id]
    unknown = [chapter_id for chapter_id in outline_ids if chapter_id not in set(manifest_ids)]
    if missing:
        errors.append(f"Manifest chapters missing from outline: {missing}")
    if unknown:
        errors.append(f"Outline contains Stable IDs not in manifest: {unknown}")

    comparable_outline_ids = [chapter_id for chapter_id in outline_ids if chapter_id in set(manifest_ids)]
    if comparable_outline_ids != manifest_ids:
        errors.append("Outline Stable ID order does not match book_structure.json chapter order.")

    for chapter in chapters:
        chapter_id = str(chapter.get("id", ""))
        section = sections_by_id.get(chapter_id)
        if not section:
            continue

        title = str(chapter.get("title", ""))
        if section.get("title") != title:
            errors.append(f"{chapter_id}: outline title {section.get('title')!r} does not match manifest title {title!r}.")

        if "Chapter job:" not in "\n".join(section["lines"]):
            errors.append(f"{chapter_id}: outline section is missing Chapter job.")
        if "Source loading queue:" not in "\n".join(section["lines"]):
            errors.append(f"{chapter_id}: outline section is missing Source loading queue.")
        if "Draft arc:" not in "\n".join(section["lines"]):
            errors.append(f"{chapter_id}: outline section is missing Draft arc.")
        if "Lean proof targets:" not in "\n".join(section["lines"]):
            errors.append(f"{chapter_id}: outline section is missing Lean proof targets.")

        outline_claim = outline_core_claim(section)
        manifest_claim = str(chapter.get("core_claim", "")).strip()
        if outline_claim != manifest_claim:
            errors.append(f"{chapter_id}: outline core claim does not match manifest core_claim.")

        queued_sources = outline_source_ids(section)
        manifest_sources = {str(source_id) for source_id in chapter.get("source_ids", [])}
        missing_sources = sorted(manifest_sources - queued_sources)
        if missing_sources:
            errors.append(f"{chapter_id}: manifest source_ids missing from outline source queue: {missing_sources}")

        outline_target_map = outline_proofs(section)
        manifest_targets = chapter.get("proof_targets", [])
        if not isinstance(manifest_targets, list):
            errors.append(f"{chapter_id}: manifest proof_targets must be a list.")
            continue
        for target in manifest_targets:
            if not isinstance(target, dict):
                errors.append(f"{chapter_id}: manifest proof target is not an object.")
                continue
            tag = str(target.get("tag", ""))
            outline_target = outline_target_map.get(tag)
            if outline_target is None:
                errors.append(f"{chapter_id}: manifest proof target {tag!r} missing from outline.")
                continue
            for field, outline_field in (("module", "module"), ("target", "target"), ("status", "status")):
                manifest_value = str(target.get(field, "")).strip()
                outline_value = str(outline_target.get(outline_field, "")).strip()
                if manifest_value != outline_value:
                    errors.append(
                        f"{chapter_id}: proof target {tag!r} {field} differs "
                        f"(manifest {manifest_value!r}, outline {outline_value!r})."
                    )

    if errors:
        fail(errors)

    print(f"Outline consistency validation passed: {len(chapters)} manifest chapters matched.")


if __name__ == "__main__":
    main()
