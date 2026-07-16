#!/usr/bin/env python3
"""Attach shared safety-model countermodel and consumer refs to replaced targets."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REVIEWS = ROOT / "proofs" / "proof_rationalization_reviews.json"

TARGET_CASES = {
    "lean:alignment.constitution.operational_invariant": "reject_alignment_missing_review",
    "lean:alignment.constitution.failure_blocks_promotion": "reject_protected_removal",
    "lean:corrigibility.agency.operational_invariant": "reject_corrigibility_missing_affected_party",
    "lean:corrigibility.agency.failure_blocks_promotion": "reject_corrigibility_missing_affected_party",
    "lean:values.conflict.operational_invariant": "reject_value_conflict_missing_residual",
    "lean:values.conflict.failure_blocks_promotion": "reject_value_conflict_missing_residual",
    "lean:governance.rights.operational_invariant": "reject_governance_missing_exit",
    "lean:governance.rights.failure_blocks_promotion": "reject_protected_removal",
    "lean:self_improvement.boundary.operational_invariant": "reject_self_improvement_self_evaluation",
    "lean:self_improvement.boundary.failure_blocks_promotion": "reject_authority_widening",
}

CONSUMERS = [
    "docs:safety_critical_lifecycle_consumer_trace",
    "evidence_quality:model_adequacy_dossiers/safety-critical-lifecycle.md",
]
RUNTIME_CONSUMERS = [
    "scripts/validate_safety_critical_lifecycle.py",
    "scripts/validate_safety_critical_lifecycle_consumer_trace.py",
    "experiments/safety_critical_lifecycle/results/2026-07-15-consumer-local.json",
]
MUTATIONS = [
    "scripts/validate_safety_critical_lifecycle.py#required-obligation-deletions",
    "scripts/validate_safety_critical_lifecycle_consumer_trace.py#negative-control-errors",
]


def main() -> None:
    value = json.loads(REVIEWS.read_text(encoding="utf-8"))
    reviews = value["target_reviews"]
    missing = sorted(set(TARGET_CASES) - set(reviews))
    if missing:
        raise SystemExit(f"Missing target reviews: {missing}")
    for tag, case_id in TARGET_CASES.items():
        review = reviews[tag]
        if review.get("disposition") != "replace_with_stronger_model":
            raise SystemExit(f"{tag}: expected replace_with_stronger_model")
        review["countermodel_refs"] = [
            f"experiments/safety_critical_lifecycle/trace_corpus.json#{case_id}"
        ]
        review["mutation_refs"] = list(MUTATIONS)
        review["consumer_refs"] = list(CONSUMERS)
        review["runtime_consumer_refs"] = list(RUNTIME_CONSUMERS)
    REVIEWS.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    print(f"Attached safety consumer/refinement refs to {len(TARGET_CASES)} replacement targets.")


if __name__ == "__main__":
    main()
