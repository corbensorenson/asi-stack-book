#!/usr/bin/env python3
"""Validate the v1.0 Phase 5 harness registry.

The registry is a traceability gate for the executable harness set. It
checks wiring, fixture counts, result records, and public docs. It does not run
the harness commands and does not promote support states.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "experiments" / "phase5_harness_registry.json"
REQUIRED_FIELDS = {
    "id",
    "name",
    "command",
    "script",
    "doc",
    "experiment_dir",
    "fixture_dir",
    "result_record",
    "expected_valid_fixtures",
    "expected_invalid_fixtures",
    "result_summary",
    "primary_chapters",
    "non_claims",
}
PUBLIC_SURFACES = [
    ROOT / "docs" / "test_harness_status_ledger.md",
    ROOT / "docs" / "v1_0_roadmap.md",
    ROOT / "README.md",
]
STATUS = ROOT / "docs" / "v1_0_candidate_status.md"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def flatten_chapters(structure: dict[str, Any]) -> set[str]:
    chapter_ids: set[str] = set()
    for part in structure.get("parts", []):
        if not isinstance(part, dict):
            continue
        for chapter in part.get("chapters", []):
            if isinstance(chapter, dict) and isinstance(chapter.get("id"), str):
                chapter_ids.add(chapter["id"])
    return chapter_ids


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def count_fixtures(path: Path, prefix: str) -> int:
    return len([item for item in path.glob("*.json") if item.name.startswith(prefix)])


def require_text(path: Path, needles: list[str], errors: list[str]) -> None:
    if not path.exists():
        errors.append(f"Missing required file: {rel(path)}")
        return
    text = path.read_text(encoding="utf-8", errors="ignore")
    for needle in needles:
        if needle not in text:
            errors.append(f"{rel(path)} missing required text: {needle}")


def validate_entry(entry: dict[str, Any], chapter_ids: set[str], shared_text: dict[Path, str], errors: list[str]) -> None:
    entry_id = str(entry.get("id", "<missing>"))
    missing = sorted(REQUIRED_FIELDS - set(entry))
    if missing:
        errors.append(f"{entry_id}: missing required fields: {missing}")
        return

    for field in ("id", "name", "command", "script", "doc", "experiment_dir", "fixture_dir", "result_record", "result_summary"):
        if not isinstance(entry.get(field), str) or not entry[field].strip():
            errors.append(f"{entry_id}: {field} must be a non-empty string.")

    for field in ("expected_valid_fixtures", "expected_invalid_fixtures"):
        if not isinstance(entry.get(field), int) or entry[field] < 0:
            errors.append(f"{entry_id}: {field} must be a non-negative integer.")

    for field in ("primary_chapters", "non_claims"):
        if not isinstance(entry.get(field), list) or not entry[field]:
            errors.append(f"{entry_id}: {field} must be a non-empty list.")

    script = ROOT / entry["script"]
    doc = ROOT / entry["doc"]
    experiment_dir = ROOT / entry["experiment_dir"]
    fixture_dir = ROOT / entry["fixture_dir"]
    result_record = ROOT / entry["result_record"]

    for path in (script, doc, experiment_dir, fixture_dir, result_record):
        if not path.exists():
            errors.append(f"{entry_id}: missing path {rel(path)}")

    if fixture_dir.exists():
        valid_count = count_fixtures(fixture_dir, "valid_")
        invalid_count = count_fixtures(fixture_dir, "invalid_")
        if valid_count != entry["expected_valid_fixtures"]:
            errors.append(f"{entry_id}: expected {entry['expected_valid_fixtures']} valid fixture(s), found {valid_count}.")
        if invalid_count != entry["expected_invalid_fixtures"]:
            errors.append(
                f"{entry_id}: expected {entry['expected_invalid_fixtures']} expected-invalid fixture(s), found {invalid_count}."
            )

    require_text(doc, [entry["command"], entry["result_record"], entry["result_summary"], "Boundary"], errors)
    require_text(result_record, [entry["command"], entry["result_summary"], "Non-claims"], errors)

    validate_book_text = shared_text[ROOT / "scripts" / "validate_book.py"]
    if Path(entry["script"]).name not in validate_book_text:
        errors.append(f"{entry_id}: {entry['script']} is not wired into scripts/validate_book.py.")

    appendix_text = shared_text[ROOT / "appendices" / "E_codex_test_specs.qmd"]
    if entry["command"] not in appendix_text:
        errors.append(f"{entry_id}: {entry['command']} is missing from Appendix E.")

    for surface in PUBLIC_SURFACES:
        if entry["command"] not in shared_text[surface]:
            errors.append(f"{entry_id}: {entry['command']} is missing from {rel(surface)}.")

    for chapter_id in entry.get("primary_chapters", []):
        if chapter_id not in chapter_ids:
            errors.append(f"{entry_id}: unknown primary chapter {chapter_id!r}.")

    non_claims = " ".join(str(item).lower() for item in entry.get("non_claims", []))
    if "does not" not in non_claims:
        errors.append(f"{entry_id}: non_claims must include explicit non-claim boundaries.")
    if "promote" not in non_claims and "support state" not in non_claims:
        errors.append(f"{entry_id}: non_claims must mention support-state non-promotion.")


def main() -> None:
    errors: list[str] = []
    registry = load_json(REGISTRY)
    if not isinstance(registry, list) or not registry:
        errors.append("experiments/phase5_harness_registry.json must contain a non-empty list.")
        registry = []

    ids = [entry.get("id") for entry in registry if isinstance(entry, dict)]
    duplicates = sorted({item for item in ids if ids.count(item) > 1})
    if duplicates:
        errors.append(f"Duplicate registry IDs: {duplicates}")

    structure = load_json(ROOT / "book_structure.json")
    chapter_ids = flatten_chapters(structure if isinstance(structure, dict) else {})
    shared_paths = [
        ROOT / "scripts" / "validate_book.py",
        ROOT / "appendices" / "E_codex_test_specs.qmd",
        STATUS,
        *PUBLIC_SURFACES,
    ]
    shared_text = {path: path.read_text(encoding="utf-8", errors="ignore") for path in shared_paths}

    status_text = shared_text[STATUS]
    for fragment in (
        "docs/test_harness_status_ledger.md",
        "60 wired checks",
        "22 Phase 5 registry harnesses",
        "38 chapter-specific/support book-gate checks",
    ):
        if fragment not in status_text:
            errors.append(f"{rel(STATUS)} missing compact harness-ledger fragment: {fragment}")

    for entry in registry:
        if not isinstance(entry, dict):
            errors.append("Every registry entry must be an object.")
            continue
        validate_entry(entry, chapter_ids, shared_text, errors)

    if errors:
        print("Phase 5 harness registry validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print(f"Phase 5 harness registry passed: {len(registry)} registered harness(es).")


if __name__ == "__main__":
    main()
