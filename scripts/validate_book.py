#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "_quarto.yml",
    "index.qmd",
    "preface.qmd",
    "sources/source_inventory.json",
    "sources/source_inventory.md",
    "scripts/sync_scaffold.py",
    "scripts/build_source_matrix.py",
    "chapters/01_asi_is_a_stack.qmd",
    "chapters/06_planning_and_control.qmd",
    "chapters/16_living_book_methodology.qmd",
    "appendices/A_source_matrix.qmd",
    "appendices/C_claim_evidence_matrix.qmd",
    "appendices/E_codex_test_specs.qmd",
    "appendices/F_changelog.qmd",
]

BAD_PHRASES = [
    "solves ASI",
    "guarantees safety",
    "proves alignment",
    "obviously safe",
    "replaces all existing methods",
]

ALLOWED_SUPPORT_STATES = {
    "unsupported",
    "argument",
    "source-derived",
    "prototype-backed",
    "synthetic-test-backed",
    "empirical-test-backed",
    "external-literature-backed",
}


def fail(message: str) -> None:
    print(message)
    sys.exit(1)


def validate_required_files() -> None:
    missing = [path for path in REQUIRED if not (ROOT / path).exists()]
    if missing:
        print("Missing required files:")
        for path in missing:
            print(f" - {path}")
        sys.exit(1)


def validate_inventory() -> None:
    inventory_path = ROOT / "sources" / "source_inventory.json"
    with inventory_path.open(encoding="utf-8") as f:
        records = json.load(f)
    if not isinstance(records, list):
        fail("sources/source_inventory.json must contain a list.")
    required_keys = {"id", "title", "priority", "layer", "chapter_targets", "url", "notes"}
    bad_records = []
    seen = set()
    duplicates = set()
    for index, record in enumerate(records):
        if not isinstance(record, dict) or not required_keys.issubset(record):
            bad_records.append(index)
            continue
        source_id = record["id"]
        if source_id in seen:
            duplicates.add(source_id)
        seen.add(source_id)
    if bad_records:
        fail(f"Source inventory records missing required keys: {bad_records}")
    if duplicates:
        fail(f"Duplicate source IDs: {sorted(duplicates)}")


def validate_chapter_frontmatter() -> None:
    chapters = sorted((ROOT / "chapters").glob("*.qmd"))
    if len(chapters) != 16:
        fail(f"Expected 16 chapter files, found {len(chapters)}.")
    stale = []
    for chapter in chapters:
        text = chapter.read_text(encoding="utf-8", errors="ignore")
        if 'last_updated: "YYYY-MM-DD"' in text:
            stale.append(chapter.relative_to(ROOT))
        if "Source records assigned; source texts not yet ingested." not in text:
            stale.append(chapter.relative_to(ROOT))
    if stale:
        print("Chapter files need scaffold status updates:")
        for path in stale:
            print(f" - {path}")
        sys.exit(1)


def validate_overclaims() -> None:
    violations = []
    targets = list((ROOT / "chapters").glob("*.qmd")) + list((ROOT / "appendices").glob("*.qmd"))
    for path in targets:
        text = path.read_text(encoding="utf-8", errors="ignore").lower()
        for phrase in BAD_PHRASES:
            if phrase.lower() in text:
                violations.append((path.relative_to(ROOT), phrase))
    if violations:
        print("Potential overclaim phrases found:")
        for path, phrase in violations:
            print(f" - {path}: {phrase}")
        sys.exit(2)


def validate_claim_states() -> None:
    text = (ROOT / "appendices" / "C_claim_evidence_matrix.qmd").read_text(encoding="utf-8", errors="ignore")
    missing = [state for state in ALLOWED_SUPPORT_STATES if state not in text]
    if missing:
        fail(f"Claim/evidence matrix is missing support-state definitions: {sorted(missing)}")


def main() -> None:
    validate_required_files()
    validate_inventory()
    validate_chapter_frontmatter()
    validate_overclaims()
    validate_claim_states()
    print("Book validation passed.")


if __name__ == "__main__":
    main()
