#!/usr/bin/env python3
"""Attach the reachable stack-boundary model and consumer to frozen P2 lineage."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REVIEWS = ROOT / "proofs/proof_rationalization_reviews.json"
TARGETS = {
    "lean:stack.layer_boundaries.operational_invariant",
    "lean:stack.layer_boundaries.failure_blocks_promotion",
    "lean:stack.layer_contract.admission_lifecycle_route",
}
RETAINED_THEOREMS = {
    "lean/AsiStackProofs/StackBoundaries.lean::layer_without_external_authority_requires_authorized_handoff",
    "lean/AsiStackProofs/StackBoundaries.lean::valid_stack_trace_rejects_unauthorized_external_handoff",
    "lean/AsiStackProofs/StackBoundaries.lean::handoff_exceeding_caller_ceiling_rejected",
}
RETIRED_THEOREMS = {
    "lean/AsiStackProofs/StackBoundaries.lean::no_layer_contract_request_stays_idle",
    "lean/AsiStackProofs/StackBoundaries.lean::missing_layer_identity_requests_identity",
    "lean/AsiStackProofs/StackBoundaries.lean::missing_lifecycle_state_requests_lifecycle",
    "lean/AsiStackProofs/StackBoundaries.lean::missing_owner_requests_owner",
    "lean/AsiStackProofs/StackBoundaries.lean::missing_responsibility_requests_responsibility",
    "lean/AsiStackProofs/StackBoundaries.lean::missing_input_artifacts_requests_input_artifacts",
    "lean/AsiStackProofs/StackBoundaries.lean::missing_output_artifacts_requests_output_artifacts",
    "lean/AsiStackProofs/StackBoundaries.lean::missing_authority_ceiling_requests_ceiling",
    "lean/AsiStackProofs/StackBoundaries.lean::missing_handoff_protocol_requests_protocol",
    "lean/AsiStackProofs/StackBoundaries.lean::missing_invariant_requests_invariant",
    "lean/AsiStackProofs/StackBoundaries.lean::missing_failure_mode_requests_failure_mode",
    "lean/AsiStackProofs/StackBoundaries.lean::missing_evidence_gate_requests_evidence_gate",
    "lean/AsiStackProofs/StackBoundaries.lean::possible_external_action_without_authority_or_handoff_blocks_contract",
    "lean/AsiStackProofs/StackBoundaries.lean::missing_source_mapping_requests_mapping",
    "lean/AsiStackProofs/StackBoundaries.lean::missing_support_state_effect_requests_boundary",
    "lean/AsiStackProofs/StackBoundaries.lean::promotion_request_without_stack_evidence_transition_requests_transition",
    "lean/AsiStackProofs/StackBoundaries.lean::layer_contract_without_nonclaim_boundary_preserves_boundary",
    "lean/AsiStackProofs/StackBoundaries.lean::complete_layer_contract_admission_allows_contract",
}
COUNTERMODELS = [
    "experiments/authority_transitions/fixtures/invalid_allow_over_ceiling.json",
    "experiments/authority_transitions/fixtures/invalid_missing_effect_receipt.json",
    "experiments/authority_transitions/fixtures/invalid_permission_class_collapse.json",
    "experiments/stack_boundary_effect/results/2026-07-15-local.json#runtime_receipts",
]
MUTATIONS = ["scripts/validate_stack_boundary_effect_consumer.py#mutations"]
CONSUMERS = [
    "chapter:asi-is-a-stack-not-a-model#formalization-hooks",
    "docs:stack_boundary_effect_consumer",
    "evidence_quality:model_adequacy_dossiers/stack-boundary-effect.md",
]
RUNTIME = [
    "scripts/validate_stack_boundary_effect_consumer.py",
    "schemas/stack_boundary_effect_consumer.schema.json",
    "experiments/stack_boundary_effect/results/2026-07-15-local.json",
    "experiments/runtime_adapter_effect_probe/results/2026-07-02-local.json",
    "experiments/authority_revocation_trace/results/2026-07-03-local.json",
    "lean/AsiStackProofs/StackBoundaries.lean",
]
REPLACEMENTS = [
    "proof-model:stack-boundaries.reachable-handoff-effect-trace.v1",
    "lean/AsiStackProofs/StackBoundaries.lean",
]


def merged(existing: list[str], additions: list[str]) -> list[str]:
    return list(dict.fromkeys([*existing, *additions]))


def attach(review: dict[str, object]) -> None:
    review["countermodel_refs"] = merged(review.get("countermodel_refs", []), COUNTERMODELS)  # type: ignore[arg-type]
    review["mutation_refs"] = merged(review.get("mutation_refs", []), MUTATIONS)  # type: ignore[arg-type]
    review["consumer_refs"] = merged(review.get("consumer_refs", []), CONSUMERS)  # type: ignore[arg-type]
    review["runtime_consumer_refs"] = merged(review.get("runtime_consumer_refs", []), RUNTIME)  # type: ignore[arg-type]
    review["replacement_refs"] = merged(review.get("replacement_refs", []), REPLACEMENTS)  # type: ignore[arg-type]


def main() -> None:
    value = json.loads(REVIEWS.read_text(encoding="utf-8"))
    targets = value["target_reviews"]
    theorems = value["theorem_reviews"]
    missing_targets = sorted(TARGETS - set(targets))
    missing_theorems = sorted((RETAINED_THEOREMS | RETIRED_THEOREMS) - set(theorems))
    if missing_targets or missing_theorems:
        raise SystemExit(f"Missing targets={missing_targets}, theorems={missing_theorems}")

    roles = {
        "lean:stack.layer_boundaries.operational_invariant":
            "Reachable finite transition model requires every accepted material effect to carry a live same-epoch grant within the caller ceiling and a prior dispatch receipt; the source-anchored nominal path reaches independent observation and exact local rollback.",
        "lean:stack.layer_boundaries.failure_blocks_promotion":
            "Lean countermodels and an independent consumer reject over-ceiling authorization, missing-owner or receipt custody, missing dispatch, stale epochs, and post-revocation effects.",
        "lean:stack.layer_contract.admission_lifecycle_route":
            "Frozen theorem-per-record lineage is retired from the live proof surface; generated traceability checks and the reachable authority/effect consumer own the narrower route, mutation, and no-promotion obligations.",
    }
    for target_id in TARGETS:
        review = targets[target_id]
        attach(review)
        review["semantic_role"] = roles[target_id]
        review["assumptions"] = [
            "Authority fixture fields, runtime receipts, logical time, target-owner approval, observation, revocation, and exact-rollback declarations are authoritative only inside the declared finite model."
        ]
        review["excluded_effects"] = [
            "Authentic or deployed authority, complete effect discovery, distributed clocks or partitions, irreversible effects, security, natural-workload usefulness, reproduction, transfer, and chapter-core support are excluded."
        ]
        review["review_rationale"] = (
            "Preserve the frozen target ID while resolving live evidence to the reachable grant-dispatch-effect-observation-rollback model and its independent source-anchored consumer; support-state effect remains none."
        )

    for theorem_id in RETAINED_THEOREMS:
        review = theorems[theorem_id]
        attach(review)
        review["review_rationale"] = (
            "Retain this genuine bounded lemma as a reusable local consequence and consume it only through the stronger reachable boundary model and finite independent consumer."
        )

    for theorem_id in RETIRED_THEOREMS:
        review = theorems[theorem_id]
        attach(review)
        review["review_rationale"] = (
            "Frozen lineage retained, but the theorem-per-record normalization is physically retired from the live Lean surface and replaced by generated route checks, semantic mutations, and the reachable boundary consumer."
        )

    REVIEWS.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    print(
        f"Attached stack-boundary refs to {len(TARGETS)} targets, "
        f"{len(RETAINED_THEOREMS)} retained theorems, and {len(RETIRED_THEOREMS)} retired theorems."
    )


if __name__ == "__main__":
    main()
