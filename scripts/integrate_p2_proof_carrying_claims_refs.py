#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEWS = ROOT / "proofs/proof_rationalization_reviews.json"
PREFIX = "lean/AsiStackProofs/ProofCarryingClaims.lean::"
TARGETS = {
    "lean:spinoza.proof_carrying.operational_invariant",
    "lean:spinoza.proof_carrying.failure_blocks_promotion",
    "lean:spinoza.adversarial_review.dossier_probe_bridge",
}
RETIRED_NAMES = {
    "formal_support_tier_requires_valid_justification_artifact",
    "failed_verifier_result_downgrades_or_blocks_claim_promotion",
    "valid_proof_carrying_claim_record_preserves_mapping_scope_limits_and_boundary",
    "adversarial_review_dossier_probe_bridge",
}
RETIRED = {PREFIX + name for name in RETIRED_NAMES}
REFS = {
    "countermodel_refs": [
        "lean/AsiStackProofs/ProofCarryingClaimsRefinement.lean#route-countermodels",
        "experiments/proof_carrying_claims/fixtures",
        "experiments/adversarial_review_dossier/results/2026-07-02-local.json",
    ],
    "mutation_refs": ["scripts/validate_proof_carrying_claims_refinement.py#mutation_sequences"],
    "consumer_refs": [
        "docs:proof_carrying_claims_refinement",
        "evidence_quality:model_adequacy_dossiers/proof-carrying-claims-refinement.md",
    ],
    "runtime_consumer_refs": [
        "scripts/validate_proof_carrying_claims_refinement.py",
        "schemas/proof_carrying_claims_refinement.schema.json",
        "experiments/proof_carrying_claims_refinement/results/2026-07-15-local.json",
        "lean/AsiStackProofs/ProofCarryingClaimsRefinement.lean",
    ],
    "replacement_refs": [
        "proof-model:proof-carrying-claims.target-artifact-writeback-refinement.v1",
        "lean/AsiStackProofs/ProofCarryingClaimsRefinement.lean",
    ],
}


def attach(record: dict) -> None:
    for key, values in REFS.items():
        record[key] = list(dict.fromkeys([*record.get(key, []), *values]))


def main() -> None:
    value = json.loads(REVIEWS.read_text())
    targets, theorems = value["target_reviews"], value["theorem_reviews"]
    if TARGETS - set(targets) or RETIRED - set(theorems):
        raise SystemExit("missing Proof-Carrying Claims frozen lineage")
    for target_id in TARGETS:
        record = targets[target_id]
        attach(record)
        record["semantic_role"] = "Reachable target-freeze, artifact-bind, verifier-execute, adjudicate, and owner-writeback lifecycle with explicit semantic and authority separation."
        record["assumptions"] = ["Claim, target, interpretation, scope, artifact, verifier, trusted-base, dossier, dissent, limitation, residual, and owner-receipt fields are trusted inside the finite authored model."]
        record["excluded_effects"] = ["Target meaning, artifact truth, verifier soundness, reviewer competence, claim truth, evidence adequacy, support, action, usefulness, causality, safety, deployment, reproduction, transfer, and SOTA are excluded."]
        record["review_rationale"] = "Replace assumed-validity and fixture-summary projection with a reachable lifecycle that distinguishes verifier pass from semantic review and can only hand a bounded proposal to owning gates."
    theorem_ids = [key for key in theorems if key.startswith(PREFIX)]
    for theorem_id in theorem_ids:
        attach(theorems[theorem_id])
    for theorem_id in RETIRED:
        record = theorems[theorem_id]
        record["review_state"] = "terminally_dispositioned"
        record["disposition"] = "retire_projection_or_assumption_restatement"
        record["review_rationale"] = "Frozen lineage retained; declaration physically retired because it projected an assumed predicate or authored dossier summary now subsumed by the reachable target-to-writeback refinement."
    REVIEWS.write_text(json.dumps(value, indent=2) + "\n")
    print(f"Attached Proof-Carrying Claims refs to 3 targets and {len(theorem_ids)} frozen theorems; 4 declarations retired.")


if __name__ == "__main__":
    main()
