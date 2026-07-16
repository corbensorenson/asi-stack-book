#!/usr/bin/env python3
"""Attach the vertical Intent-to-Execution refinement to frozen P2 lineage."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REVIEWS = ROOT / "proofs/proof_rationalization_reviews.json"
TARGETS = {
    "lean:intent_execution.contracts.operational_invariant",
    "lean:intent_execution.contracts.failure_blocks_promotion",
    "lean:intent_execution.contracts.dispatch_route_envelope",
    "lean:intent_execution.handoff_trace.probe_fixture_bridge",
}
RETIRED = {
    "lean/AsiStackProofs/IntentToExecution.lean::compiled_execution_job_preserves_parent_contract_constraints",
    "lean/AsiStackProofs/IntentToExecution.lean::execution_job_without_required_approval_cannot_transition_to_running",
}
RETAINED = {
    "lean/AsiStackProofs/IntentToExecution.lean::missing_contract_rejects_execution_dispatch",
    "lean/AsiStackProofs/IntentToExecution.lean::missing_objective_requests_execution_clarification",
    "lean/AsiStackProofs/IntentToExecution.lean::authority_widening_blocks_execution_dispatch",
    "lean/AsiStackProofs/IntentToExecution.lean::hidden_override_blocks_execution_dispatch",
    "lean/AsiStackProofs/IntentToExecution.lean::required_approval_missing_routes_to_approval",
    "lean/AsiStackProofs/IntentToExecution.lean::missing_artifacts_request_execution_clarification",
    "lean/AsiStackProofs/IntentToExecution.lean::missing_verification_plan_routes_to_verification",
    "lean/AsiStackProofs/IntentToExecution.lean::known_residual_records_execution_residual",
    "lean/AsiStackProofs/IntentToExecution.lean::complete_dispatch_review_is_ready",
    "lean/AsiStackProofs/IntentToExecution.lean::intent_execution_handoff_probe_fixture_bridge",
}
COUNTERMODELS = [
    "experiments/governed_repository_change_slice/results/2026-07-10-local.json#scenario_results",
    "experiments/intent_execution_handoff/results/2026-07-02-local.json#negative_controls",
]
MUTATIONS = ["scripts/validate_intent_execution_vertical_refinement.py#mutations"]
CONSUMERS = [
    "chapter:intent-to-execution-contracts#formalization-hooks",
    "docs:intent_execution_vertical_refinement",
    "evidence_quality:model_adequacy_dossiers/intent-execution-vertical-refinement.md",
]
RUNTIME = [
    "scripts/validate_intent_execution_vertical_refinement.py",
    "schemas/intent_execution_vertical_refinement.schema.json",
    "experiments/intent_execution_vertical_refinement/results/2026-07-15-local.json",
    "experiments/governed_repository_change_slice/results/2026-07-10-local.json",
    "schemas/governed_repository_change_result.schema.json",
    "scripts/validate_intent_execution_handoff_probe.py",
    "experiments/intent_execution_handoff/results/2026-07-02-local.json",
    "lean/AsiStackProofs/IntentExecutionRefinement.lean",
]
REPLACEMENTS = [
    "proof-model:intent-execution.vertical-trace-refinement.v1",
    "lean/AsiStackProofs/IntentExecutionRefinement.lean",
]


def merged(old: list[str], new: list[str]) -> list[str]:
    return list(dict.fromkeys([*old, *new]))


def attach(review: dict[str, object]) -> None:
    for key, values in (("countermodel_refs", COUNTERMODELS), ("mutation_refs", MUTATIONS), ("consumer_refs", CONSUMERS), ("runtime_consumer_refs", RUNTIME), ("replacement_refs", REPLACEMENTS)):
        review[key] = merged(review.get(key, []), values)  # type: ignore[arg-type]


def main() -> None:
    value = json.loads(REVIEWS.read_text(encoding="utf-8"))
    targets = value["target_reviews"]; theorems = value["theorem_reviews"]
    missing_targets = sorted(TARGETS - set(targets)); missing_theorems = sorted((RETIRED | RETAINED) - set(theorems))
    if missing_targets or missing_theorems:
        raise SystemExit(f"Missing targets={missing_targets}, theorems={missing_theorems}")
    roles = {
        "lean:intent_execution.contracts.operational_invariant": "Reachable vertical transition model preserves exact root-contract and artifact parentage, non-widening authority, dispatch/effect custody, observation, verification, delivery, rollback, quarantine, and residual boundaries; executable refinement checks nine executed scenarios and 89 events.",
        "lean:intent_execution.contracts.failure_blocks_promotion": "Lean countermodels and thirty concrete source mutations reject missing approval, authority widening, hidden override, effect without dispatch, unverified delivery, unsafe release, incomplete rollback custody, residual erasure, and support laundering.",
        "lean:intent_execution.contracts.dispatch_route_envelope": "Finite priority route lemmas remain reusable local branches and are consumed alongside executed release, refusal, rollback, and quarantine outcomes by the vertical refinement.",
        "lean:intent_execution.handoff_trace.probe_fixture_bridge": "The earlier two-valid/seven-invalid synthetic probe remains lineage and negative-control evidence; the stronger consumer now refines the complete executed nine-scenario governed-result schema.",
    }
    for target_id in TARGETS:
        review = targets[target_id]; attach(review)
        review["semantic_role"] = roles[target_id]
        review["assumptions"] = ["The versioned source schema, event labels, expected dispositions, authority and receipt fields, effect observations, verifier identity, and rollback/residual fields are authoritative only within the declared finite local result."]
        review["excluded_effects"] = ["Human-intent correctness, general semantic equivalence, authentic authority, complete effects, natural workloads, distributed behavior, deployment, reproduction, transfer, safety, SOTA, and chapter-core support are excluded."]
        review["review_rationale"] = "Resolve frozen target lineage to the reachable vertical model and independently implemented concrete-schema refinement while preserving exact no-promotion boundaries."
    for theorem_id in RETIRED:
        review = theorems[theorem_id]; attach(review)
        review["review_rationale"] = "Frozen lineage retained, but the assumption-restating theorem and its local record scaffolding are physically retired and replaced by a reachable transition model, executed source refinement, countermodels, and thirty source-field mutations."
    for theorem_id in RETAINED:
        review = theorems[theorem_id]; attach(review)
    REVIEWS.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    print(f"Attached vertical intent-execution refs to {len(TARGETS)} targets, {len(RETIRED)} retired theorems, and {len(RETAINED)} retained theorems.")


if __name__ == "__main__":
    main()
