#!/usr/bin/env python3
"""Attach the stronger integrated trace model and consumer to frozen P2 lineage."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REVIEWS = ROOT / "proofs/proof_rationalization_reviews.json"
TARGETS = {
    "lean:reference_architecture.trace.operational_invariant",
    "lean:reference_architecture.trace.failure_blocks_promotion",
    "lean:reference_architecture.governed_trace.four_invariants",
}
REPLACED_THEOREMS = {
    "lean/AsiStackProofs/ReferenceArchitecture.lean::end_to_end_trace_contains_required_artifacts_for_layer_handoff",
    "lean/AsiStackProofs/ReferenceArchitecture.lean::trace_with_missing_governance_gate_cannot_be_marked_valid",
    "lean/AsiStackProofs/GovernedRepositoryTrace.lean::governed_fixture_authority_monotone",
    "lean/AsiStackProofs/GovernedRepositoryTrace.lean::authority_widening_negative_rejected",
    "lean/AsiStackProofs/GovernedRepositoryTrace.lean::governed_fixture_revocation_before_effect",
    "lean/AsiStackProofs/GovernedRepositoryTrace.lean::effect_at_revocation_time_negative_rejected",
    "lean/AsiStackProofs/GovernedRepositoryTrace.lean::governed_fixture_evidence_integrity",
    "lean/AsiStackProofs/GovernedRepositoryTrace.lean::unrecorded_promotion_negative_rejected",
    "lean/AsiStackProofs/GovernedRepositoryTrace.lean::governed_fixture_residual_conserved",
    "lean/AsiStackProofs/GovernedRepositoryTrace.lean::erased_open_residual_negative_rejected",
    "lean/AsiStackProofs/GovernedRepositoryTrace.lean::governed_repository_trace_four_invariants",
}
RETAINED_ROUTE_THEOREMS = {
    "lean/AsiStackProofs/ReferenceArchitecture.lean::trace_missing_parent_artifacts_routes_to_parentage_repair",
    "lean/AsiStackProofs/ReferenceArchitecture.lean::trace_missing_authority_deltas_routes_to_authority_repair",
    "lean/AsiStackProofs/ReferenceArchitecture.lean::trace_missing_residual_deltas_routes_to_residual_preservation",
    "lean/AsiStackProofs/ReferenceArchitecture.lean::trace_missing_required_governance_gate_blocks_trace",
    "lean/AsiStackProofs/ReferenceArchitecture.lean::trace_missing_validation_command_requires_validation",
}
COUNTERMODELS = [
    "experiments/integrated_reference_trace/corpus/2026-07-15.json#cases",
]
MUTATIONS = [
    "scripts/validate_integrated_reference_trace_consumer.py#MUTATIONS",
]
CONSUMERS = [
    "chapter:integrated-reference-architecture#integrated-transition-consumer",
    "docs:integrated_reference_trace_consumer",
    "evidence_quality:model_adequacy_dossiers/integrated-reference-trace.md",
]
RUNTIME = [
    "scripts/validate_integrated_reference_trace_consumer.py",
    "experiments/integrated_reference_trace/corpus/2026-07-15.json",
    "experiments/integrated_reference_trace/results/2026-07-15-local.json",
    "experiments/governed_repository_change_slice/results/2026-07-10-local.json",
    "lean/AsiStackProofs/IntegratedReferenceTrace.lean",
]
REPLACEMENT = [
    "proof-model:integrated-reference-trace.partial-transition.v1",
    "lean/AsiStackProofs/IntegratedReferenceTrace.lean",
]


def merged(existing: list[str], additions: list[str]) -> list[str]:
    return list(dict.fromkeys([*existing, *additions]))


def main() -> None:
    value = json.loads(REVIEWS.read_text(encoding="utf-8"))
    target_reviews = value["target_reviews"]
    theorem_reviews = value["theorem_reviews"]
    missing_targets = sorted(TARGETS - set(target_reviews))
    missing_theorems = sorted((REPLACED_THEOREMS | RETAINED_ROUTE_THEOREMS) - set(theorem_reviews))
    if missing_targets or missing_theorems:
        raise SystemExit(f"Missing targets={missing_targets}, theorems={missing_theorems}")

    target_roles = {
        "lean:reference_architecture.trace.operational_invariant":
            "Partial cross-layer transition model proves accepted-step artifact/state joins, authority-ceiling preservation, arbitrary accepted-trace authority non-widening, and trace composition; independent consumer covers accepted, contained, rejected, and mutated paths.",
        "lean:reference_architecture.trace.failure_blocks_promotion":
            "Partial transition model and consumer reject or contain parent/state forks, authority widening, gate deletion, revocation-time effects, acknowledgement gaps, residual erasure, self-evaluation, promotion laundering, missing receipts, and incomplete rollback.",
        "lean:reference_architecture.governed_trace.four_invariants":
            "Source-anchored independent consumer replays 18 finite cases with four accepted outcome paths, fourteen rejections, thirty-five accepted events, effect/acknowledgement/residual/receipt accounting, and fifteen rejected mutations.",
    }
    for tag in TARGETS:
        review = target_reviews[tag]
        review["semantic_role"] = target_roles[tag]
        review["assumptions"] = [
            "The finite event schema, abstract artifact/state identities, sequential atomic execution, and source-event mapping are authoritative only inside the declared model."
        ]
        review["excluded_effects"] = [
            "No checked live-schema encoding, payload semantic equivalence, distributed/concurrent execution, deployed authority or rollback service, evaluator independence, residual completeness, safety, reproduction, transfer, or chapter-core promotion."
        ]
        review["countermodel_refs"] = list(COUNTERMODELS)
        review["mutation_refs"] = list(MUTATIONS)
        review["consumer_refs"] = merged(review.get("consumer_refs", []), CONSUMERS)
        review["runtime_consumer_refs"] = merged(review.get("runtime_consumer_refs", []), RUNTIME)
        review["replacement_refs"] = merged(review.get("replacement_refs", []), REPLACEMENT)
        review["review_rationale"] = (
            "Preserve the frozen target ID while resolving its live implementation to the stronger partial transition model and independent consumer; keep the result bounded to finite source-anchored trace semantics."
        )

    for theorem_id in REPLACED_THEOREMS:
        review = theorem_reviews[theorem_id]
        review["countermodel_refs"] = merged(review.get("countermodel_refs", []), COUNTERMODELS)
        review["mutation_refs"] = merged(review.get("mutation_refs", []), MUTATIONS)
        review["consumer_refs"] = merged(review.get("consumer_refs", []), CONSUMERS)
        review["runtime_consumer_refs"] = merged(review.get("runtime_consumer_refs", []), RUNTIME)
        review["replacement_refs"] = merged(review.get("replacement_refs", []), REPLACEMENT)
        review["review_rationale"] = (
            "Frozen lineage retained; the unconsumed projection or theorem-per-fixture normalization is replaced by the integrated partial transition model, countermodel corpus, and independent consumer."
        )

    for theorem_id in RETAINED_ROUTE_THEOREMS:
        review = theorem_reviews[theorem_id]
        review["countermodel_refs"] = merged(review.get("countermodel_refs", []), COUNTERMODELS)
        review["mutation_refs"] = merged(review.get("mutation_refs", []), MUTATIONS)
        review["consumer_refs"] = merged(review.get("consumer_refs", []), CONSUMERS)
        review["runtime_consumer_refs"] = merged(review.get("runtime_consumer_refs", []), RUNTIME)
        review["replacement_refs"] = merged(review.get("replacement_refs", []), REPLACEMENT)

    REVIEWS.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    print(
        f"Attached integrated trace refs to {len(TARGETS)} frozen targets, "
        f"{len(REPLACED_THEOREMS)} replaced theorems, and {len(RETAINED_ROUTE_THEOREMS)} retained routes."
    )


if __name__ == "__main__":
    main()
