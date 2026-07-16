#!/usr/bin/env python3
"""Project the reachable stack-boundary result into the book manifest and triage."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STRUCTURE = ROOT / "book_structure.json"
TRIAGE = ROOT / "proofs/proof_triage.json"

TARGETS = {
    "lean:stack.layer_boundaries.operational_invariant": (
        "Every accepted material effect in the finite boundary transition model requires a live same-epoch grant within the caller ceiling and a prior dispatch receipt; the source-anchored nominal path reaches independent observation and exact local rollback."
    ),
    "lean:stack.layer_boundaries.failure_blocks_promotion": (
        "The finite boundary model rejects over-ceiling authorization, effect without a dispatch receipt, and post-revocation effect."
    ),
    "lean:stack.layer_contract.admission_lifecycle_route": (
        "An independently implemented generated suite matches all eighteen priority-ordered layer-contract admission routes after the theorem-per-record normalizations are retired from the live proof surface."
    ),
}


def chapter(value: dict[str, object]) -> dict[str, object]:
    for part in value["parts"]:  # type: ignore[index]
        for row in part.get("chapters", []):
            if row.get("id") == "asi-is-a-stack-not-a-model":
                return row
    raise SystemExit("Missing asi-is-a-stack-not-a-model")


def main() -> None:
    structure = json.loads(STRUCTURE.read_text(encoding="utf-8"))
    row = chapter(structure)
    for target in row["proof_targets"]:
        target["target"] = TARGETS[target["tag"]]

    tests = row["codex_tests"]
    for test in tests:
        if test.get("name") == "Layer-contract admission lifecycle route":
            test["purpose"] = (
                "Check all eighteen priority-ordered layer-contract admission outcomes through a generated independent route suite while preserving frozen lineage for the retired theorem-per-record normalizations."
            )
            test["result_status"] = (
                "passes 18/18 generated route cases via `python3 scripts/validate_stack_boundary_effect_consumer.py`; no deployed layer enforcement, complete source-to-layer traceability, whole-system safety, or support-state promotion claim"
            )
            test["status"] = (
                "implemented by the independent stack-boundary consumer; retired Lean normalizations remain frozen in the rationalization registry"
            )
    if not any(test.get("name") == "Reachable stack-boundary authority/effect consumer" for test in tests):
        tests.insert(1, {
            "name": "Reachable stack-boundary authority/effect consumer",
            "purpose": "Check request, within-ceiling authorization, receipt-bound dispatch, material effect, independent observation, revocation, denial, and exact rollback against source-anchored local evidence and targeted semantic mutations.",
            "implementation_status": "implemented",
            "result_status": "passes via `python3 scripts/validate_stack_boundary_effect_consumer.py`: 6 authority fixtures, 3 runtime paths, 10 accepted events, 1 effect, 1 observation, 1 exact rollback, 2 no-mutation denials, 5 revocation entries, and 12/12 rejected mutations; support-state effect none",
            "status": "implemented in `AsiStackProofs.StackBoundaries` plus an independent consumer; synthetic fixtures and one local temp-file effect do not establish deployed authority, complete effects, safety, reproduction, transfer, or chapter-core support",
        })
    STRUCTURE.write_text(json.dumps(structure, indent=2) + "\n", encoding="utf-8")

    triage = json.loads(TRIAGE.read_text(encoding="utf-8"))
    rationales = {
        "lean:stack.layer_boundaries.operational_invariant": "Implemented as a reachable finite state transition model plus an independent source-anchored consumer; establishes only live-grant/dispatch custody and one observed exact local rollback path under trusted input fields.",
        "lean:stack.layer_boundaries.failure_blocks_promotion": "Implemented with Lean countermodels and twelve independently checked semantic mutations covering authority widening, missing custody, stale epochs, missing observation, false rollback, and post-revocation effect.",
        "lean:stack.layer_contract.admission_lifecycle_route": "The eighteen theorem-per-record normalizations are retired from the live Lean surface; a generated independent suite checks all eighteen priority-ordered route outcomes, while frozen proof lineage is preserved in the rationalization registry.",
    }
    for target in triage["records"]:
        tag = target.get("tag")
        if tag in TARGETS:
            target["formal_target"] = TARGETS[tag]
            target["rationale"] = rationales[tag]
    TRIAGE.write_text(json.dumps(triage, indent=2) + "\n", encoding="utf-8")
    print("Integrated three reachable stack-boundary targets and two consumer test contracts.")


if __name__ == "__main__":
    main()
