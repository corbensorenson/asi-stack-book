#!/usr/bin/env python3
"""Project the vertical Intent-to-Execution refinement into manifest and triage."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STRUCTURE = ROOT / "book_structure.json"
TRIAGE = ROOT / "proofs/proof_triage.json"
TARGETS = {
    "lean:intent_execution.contracts.operational_invariant": "Every accepted edge in the finite vertical transition model preserves the root contract and exact artifact parent, cannot widen authority or apply hidden overrides, and reaches material effect and delivery only through approval, dispatch, observation, artifact, and independent-verification custody.",
    "lean:intent_execution.contracts.failure_blocks_promotion": "The vertical model and concrete-schema consumer reject missing approval, authority widening, hidden override, effect without dispatch, unverified delivery, unsafe release, incomplete rollback custody, residual erasure, and support laundering.",
}


def main() -> None:
    value = json.loads(STRUCTURE.read_text(encoding="utf-8"))
    chapter = next(ch for part in value["parts"] for ch in part["chapters"] if ch["id"] == "intent-to-execution-contracts")
    for target in chapter["proof_targets"]:
        if target["tag"] in TARGETS:
            target["target"] = TARGETS[target["tag"]]
            target["module"] = "AsiStackProofs.IntentExecutionRefinement"
    if not any(test.get("name") == "Executed vertical Intent-to-Execution refinement" for test in chapter["codex_tests"]):
        chapter["codex_tests"].append({
            "name": "Executed vertical Intent-to-Execution refinement",
            "purpose": "Refine the reachable contract-to-delivery model against the complete executed governed repository-change result, including release, pre-effect refusal, exact rollback, failed-rollback quarantine, residual custody, and semantic source mutations.",
            "implementation_status": "implemented",
            "result_status": "passes via `python3 scripts/validate_intent_execution_vertical_refinement.py`: 9 scenarios, 89 events, 3 releases, 3 pre-effect refusals, 2 exact-rollback refusals, 1 failed-rollback quarantine, 6 material effects, 6 independent observations, 2 residual scenarios, and 30/30 rejected mutations; support-state effect none",
            "status": "implemented local concrete-schema refinement; no general semantic equivalence, natural-language intent correctness, deployed authority, natural workload, reproduction, transfer, safety, or chapter-core support claim",
        })
    STRUCTURE.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")

    triage = json.loads(TRIAGE.read_text(encoding="utf-8"))
    for target in triage["records"]:
        if target.get("tag") in TARGETS:
            target["formal_target"] = TARGETS[target["tag"]]
            target["module"] = "AsiStackProofs.IntentExecutionRefinement"
            target["rationale"] = "Replaced the assumption-restating baseline theorem with a reachable partial transition model and an independently implemented refinement over nine executed source scenarios, 89 events, and thirty rejecting source mutations; support-state effect remains none."
    TRIAGE.write_text(json.dumps(triage, indent=2) + "\n", encoding="utf-8")
    print("Integrated two vertical intent-execution proof targets and one executed consumer test.")


if __name__ == "__main__":
    main()
