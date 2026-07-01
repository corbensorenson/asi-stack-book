#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

from validate_claim_ledger_revision import semantic_errors


ROOT = Path(__file__).resolve().parents[1]
RECORD_DIR = ROOT / "claim_revisions"
BOOK_STRUCTURE = ROOT / "book_structure.json"
NON_CORE_LEDGER = ROOT / "docs" / "non_core_evidence_ledger.md"
CORE_COVERAGE = ROOT / "docs" / "core_claim_transition_coverage.md"

REQUIRED_RECORD = "claim_revisions/v1_x/manifest_core_claim_count_narrowing.json"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def manifest_chapter_count() -> int:
    structure = load_json(BOOK_STRUCTURE)
    if not isinstance(structure, dict):
        raise ValueError("book_structure.json must contain an object.")
    return sum(
        len(part.get("chapters", []))
        for part in structure.get("parts", [])
        if isinstance(part, dict)
    )


def main() -> None:
    errors: list[str] = []
    records = sorted(RECORD_DIR.rglob("*.json")) if RECORD_DIR.exists() else []
    if not records:
        errors.append(f"No live claim revision records found in {rel(RECORD_DIR)}.")

    seen_scenarios: set[str] = set()
    seen_claim_ids: set[str] = set()
    for record_path in records:
        relative = rel(record_path)
        try:
            value = load_json(record_path)
        except Exception as exc:
            errors.append(f"{relative}: invalid JSON: {exc}")
            continue
        if not isinstance(value, dict):
            errors.append(f"{relative}: top-level record must be an object.")
            continue

        errors.extend(semantic_errors(value, relative))

        scenario_id = value.get("scenario_id")
        if isinstance(scenario_id, str):
            if scenario_id in seen_scenarios:
                errors.append(f"{relative}: duplicate scenario_id {scenario_id!r}.")
            seen_scenarios.add(scenario_id)
        record = value.get("claim_ledger_record")
        if isinstance(record, dict):
            claim_id = record.get("claim_id")
            if isinstance(claim_id, str):
                if claim_id in seen_claim_ids:
                    errors.append(f"{relative}: duplicate claim_id {claim_id!r}.")
                seen_claim_ids.add(claim_id)
            if record.get("support_state_before") != record.get("support_state_after"):
                errors.append(f"{relative}: live count/surface revisions must not move support state.")
            if record.get("accepted_evidence_transition_refs"):
                errors.append(f"{relative}: live count/surface revisions must not cite accepted upward transitions.")

    if not (ROOT / REQUIRED_RECORD).exists():
        errors.append(f"Missing required live claim-narrowing record: {REQUIRED_RECORD}.")

    try:
        chapter_count = manifest_chapter_count()
    except Exception as exc:
        chapter_count = -1
        errors.append(str(exc))

    ledger_text = NON_CORE_LEDGER.read_text(encoding="utf-8", errors="ignore")
    coverage_text = CORE_COVERAGE.read_text(encoding="utf-8", errors="ignore")
    required_ledger_fragment = f"All {chapter_count} remain at `argument`."
    required_coverage_fragment = f"| Manifest chapter core claims | {chapter_count} |"
    if required_ledger_fragment not in ledger_text:
        errors.append(
            f"{rel(NON_CORE_LEDGER)} must contain current manifest count fragment: "
            f"{required_ledger_fragment}"
        )
    if required_coverage_fragment not in coverage_text:
        errors.append(
            f"{rel(CORE_COVERAGE)} must contain current manifest count fragment: "
            f"{required_coverage_fragment}"
        )
    for stale in ("All 54 remain at `argument`.", "All 46 chapter core claims"):
        if stale in ledger_text:
            errors.append(f"{rel(NON_CORE_LEDGER)} contains stale count text: {stale}")

    if errors:
        print("Claim revision record validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print(
        "Claim revision record validation passed: "
        f"{len(records)} live revision record(s), {chapter_count} manifest chapter core claims."
    )


if __name__ == "__main__":
    main()
