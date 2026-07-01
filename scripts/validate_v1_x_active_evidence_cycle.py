#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "v1_x_active_evidence_cycle.md"
STRUCTURE = ROOT / "book_structure.json"

MIN_SELECTED = 5
MAX_SELECTED = 8
EXPECTED_SELECTED = {
    "evidence-states-and-claim-discipline",
    "recursive-self-improvement-boundaries",
    "resource-economics-and-token-budgets",
    "circle-calculus-and-proof-carrying-ai-contracts",
    "coil-attention-cyclic-memory-and-recurrence-contracts",
    "executable-specifications-and-lean-proof-envelope",
    "project-theseus-as-report-first-implementation-reference",
    "living-book-methodology",
}
STATIC_REQUIRED_FRAGMENTS = (
    "Selected chapter lanes | 8",
    "Lane cap | 5-8 selected lanes per v1.x cycle",
    "No chapter core promotion",
    "does not promote any chapter core claim above `argument`",
    "docs/non_core_evidence_ledger.md",
    "docs/costed_route_resource_slice.md",
    "docs/simulation_transfer_boundary_harness.md",
    "docs/circle_external_receipt_slice.md",
    "docs/circle_public_replay_consumer_gate.md",
    "docs/cyclic_memory_contract_harness.md",
    "docs/theseus_report_import_slice.md",
    "docs/phase5_harness_runner.md",
    "docs/proof_depth_classification.md",
)


def fail(errors: list[str]) -> None:
    print("v1.x active evidence-cycle validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def manifest_chapter_ids() -> list[str]:
    value = json.loads(STRUCTURE.read_text(encoding="utf-8"))
    return [
        str(chapter["id"])
        for part in value.get("parts", [])
        for chapter in part.get("chapters", [])
    ]


def section(text: str, start: str, end: str | None = None) -> str:
    start_marker = f"## {start}"
    start_index = text.find(start_marker)
    if start_index < 0:
        return ""
    if end is None:
        return text[start_index:]
    end_marker = f"## {end}"
    end_index = text.find(end_marker, start_index + len(start_marker))
    if end_index < 0:
        return text[start_index:]
    return text[start_index:end_index]


def main() -> None:
    errors: list[str] = []
    text = DOC.read_text(encoding="utf-8")
    all_ids = set(manifest_chapter_ids())
    selected_section = section(text, "Selected Lanes", "Planned-Only Lanes")
    planned_section = section(text, "Planned-Only Lanes", "Non-Claims")

    selected_ids = {
        match.group(1)
        for match in re.finditer(r"^\|\s*`([^`]+)`\s*\|", selected_section, re.MULTILINE)
    }
    planned_ids = {
        match.group(1)
        for match in re.finditer(r"^-\s*`([^`]+)`\s*$", planned_section, re.MULTILINE)
    }

    if selected_ids != EXPECTED_SELECTED:
        errors.append(f"Selected lane set mismatch: {sorted(selected_ids)}")
    if not (MIN_SELECTED <= len(selected_ids) <= MAX_SELECTED):
        errors.append(f"Selected lane count {len(selected_ids)} is outside {MIN_SELECTED}-{MAX_SELECTED}.")
    if selected_ids & planned_ids:
        errors.append(f"Chapter IDs listed as both selected and planned-only: {sorted(selected_ids & planned_ids)}")
    if selected_ids | planned_ids != all_ids:
        missing = sorted(all_ids - (selected_ids | planned_ids))
        extra = sorted((selected_ids | planned_ids) - all_ids)
        if missing:
            errors.append(f"Missing manifest chapter IDs: {missing}")
        if extra:
            errors.append(f"Unknown chapter IDs: {extra}")
    expected_planned = len(all_ids) - len(selected_ids)
    if len(planned_ids) != expected_planned:
        errors.append(f"Planned-only lane count {len(planned_ids)} does not match manifest remainder.")
    dynamic_required_fragments = (
        f"Planned-only chapter lanes | {expected_planned}",
        f"No {len(all_ids)}-lane fixture sweep is claimed or implied.",
        f"all {len(all_ids)} chapter core claims remain `argument`",
    )
    for fragment in STATIC_REQUIRED_FRAGMENTS + dynamic_required_fragments:
        if fragment not in text:
            errors.append(f"Missing required fragment: {fragment}")

    referenced_paths = (
        "docs/non_core_evidence_ledger.md",
        "docs/core_claim_transition_coverage.md",
        "claim_decisions/v1_0_core_claim_no_promotion.json",
        "docs/proof_depth_classification.md",
        "docs/theseus_report_import_slice.md",
        "docs/costed_route_resource_slice.md",
        "experiments/costed_route_resource_slice/results/2026-06-29-local.json",
        "docs/simulation_transfer_boundary_harness.md",
        "experiments/simulation_transfer_boundaries/results/2026-06-30-local.md",
        "docs/circle_external_receipt_slice.md",
        "docs/circle_public_replay_consumer_gate.md",
        "experiments/circle_public_replay/results/2026-06-29-local.json",
        "docs/cyclic_memory_contract_harness.md",
        "experiments/cyclic_memory_contracts/results/2026-06-30-local.md",
        "docs/proof_adequacy_review.md",
        "docs/proof_artifact_audit.md",
        "experiments/theseus_import/results/2026-06-29-local.json",
        "scripts/validate_theseus_report.py",
        "docs/phase5_harness_runner.md",
        "experiments/phase5_harness_registry.json",
    )
    for relative in referenced_paths:
        if relative not in text:
            errors.append(f"Document does not reference required artifact {relative}.")
        if not (ROOT / relative).exists():
            errors.append(f"Referenced artifact does not exist: {relative}")

    if errors:
        fail(errors)

    print(
        "v1.x active evidence-cycle validation passed: "
        f"{len(selected_ids)} selected lanes, {len(planned_ids)} planned-only lanes."
    )


if __name__ == "__main__":
    main()
