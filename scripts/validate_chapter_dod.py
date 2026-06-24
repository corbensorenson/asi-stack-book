#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STRUCTURE = ROOT / "book_structure.json"

REQUIRED_SECTIONS = [
    "## Chapter status",
    "## Drafting guardrail",
    "## Problem",
    "## Why existing approaches are insufficient",
    "## Core Claim",
    "## Mechanism",
    "## Interfaces",
    "## Invariants",
    "## Failure modes",
    "## Minimal implementation",
    "## Codex test plan",
    "## Source crosswalk",
    "## Summary",
]

ALLOWED_SUPPORT_STATES = {
    "unsupported",
    "argument",
    "source-derived",
    "prototype-backed",
    "synthetic-test-backed",
    "empirical-test-backed",
    "external-literature-backed",
    "deprecated",
    "refuted",
}

ALLOWED_CLAIM_LABELS = {
    "Demonstrated",
    "Measured",
    "Mechanized",
    "Hypothesized",
    "Design rationale",
    "Speculative",
}


def read_json(path: Path) -> object:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def flatten_chapters(structure: dict) -> list[dict]:
    chapters: list[dict] = []
    for part in structure.get("parts", []):
        for chapter in part.get("chapters", []):
            merged = dict(chapter)
            merged["_part_id"] = part["id"]
            merged["_part_title"] = part["title"]
            chapters.append(merged)
    return chapters


def frontmatter_value(text: str, key: str) -> str | None:
    match = re.search(rf'^{re.escape(key)}:\s+"([^"]*)"', text, flags=re.MULTILINE)
    return match.group(1) if match else None


def main() -> None:
    structure = read_json(STRUCTURE)
    if not isinstance(structure, dict):
        raise SystemExit("book_structure.json must contain an object.")

    errors: list[str] = []
    for chapter in flatten_chapters(structure):
        path = ROOT / chapter["file"]
        if not path.exists():
            errors.append(f"{chapter['file']}: missing chapter file")
            continue

        text = path.read_text(encoding="utf-8", errors="ignore")
        missing_sections = [section for section in REQUIRED_SECTIONS if section not in text]
        if missing_sections:
            errors.append(f"{chapter['file']}: missing DoD sections: {', '.join(missing_sections)}")

        expected = {
            "chapter_id": chapter["id"],
            "part_id": chapter["_part_id"],
            "status": chapter.get("status", "conceptual"),
            "evidence_level": chapter.get("evidence_level", "argument"),
            "claim_label": chapter.get("claim_label", "Design rationale"),
        }
        for key, value in expected.items():
            actual = frontmatter_value(text, key)
            if actual != value:
                errors.append(f"{chapter['file']}: frontmatter {key!r} is {actual!r}, expected {value!r}")

        support = expected["evidence_level"]
        if support not in ALLOWED_SUPPORT_STATES:
            errors.append(f"{chapter['file']}: invalid evidence_level {support!r}")
        label = expected["claim_label"]
        if label not in ALLOWED_CLAIM_LABELS:
            errors.append(f"{chapter['file']}: invalid claim_label {label!r}")

        for source_id in chapter.get("source_ids", []):
            if f"`{source_id}`" not in text:
                errors.append(f"{chapter['file']}: source crosswalk does not mention `{source_id}`")

        if "| Test | Purpose | Status |" not in text:
            errors.append(f"{chapter['file']}: missing Codex test-plan table")

    if errors:
        print("Chapter Definition of Done validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print(f"Chapter DoD validation passed: {len(flatten_chapters(structure))} chapters.")


if __name__ == "__main__":
    main()
