#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEWS = ROOT / "proofs/proof_rationalization_reviews.json"
PREFIX = "lean/AsiStackProofs/ClaimLedger.lean::"
TARGETS = {
    "lean:claims.ledger.operational_invariant",
    "lean:claims.ledger.failure_blocks_promotion",
    "lean:claims.ledger.revision_lifecycle_route",
    "lean:claims.ledger.semantic_assumption_fixture_bridge",
}
RETIRED_NAMES = {
    "valid_belief_revision_record_preserves_identity_history_and_boundary",
    "revision_request_missing_claim_identity_rejected",
    "missing_support_state_record_requests_support_state_record",
    "promotion_without_evidence_transition_requests_evidence_transition",
    "promotion_without_evidence_refs_requests_evidence_transition",
    "open_contradiction_promotion_is_blocked",
    "open_contradiction_without_promotion_requests_handling",
    "revision_without_history_refs_preserves_history",
    "revision_without_non_overwrite_attestation_preserves_attestation",
    "incomplete_surface_sync_requests_synchronization",
    "split_without_child_history_preserves_split_history",
    "downgrade_without_reason_requests_downgrade_reason",
    "required_residual_without_refs_requests_residual_record",
    "revision_without_non_claim_boundary_preserves_boundary",
    "complete_claim_ledger_revision_accepts",
    "semantic_assumption_fixture_bridge",
}
RETIRED = {PREFIX + name for name in RETIRED_NAMES}
REFS = {
    "countermodel_refs": [
        "lean/AsiStackProofs/ClaimLedgerRefinement.lean#route-countermodels",
        "experiments/claim_ledger_revision/fixtures",
        "experiments/contradiction_revision_lifecycle/fixtures",
    ],
    "mutation_refs": ["scripts/validate_claim_ledger_refinement.py#mutations"],
    "consumer_refs": [
        "docs:claim_ledger_refinement",
        "evidence_quality:model_adequacy_dossiers/claim-ledger-refinement.md",
    ],
    "runtime_consumer_refs": [
        "scripts/validate_claim_ledger_refinement.py",
        "schemas/claim_ledger_refinement.schema.json",
        "experiments/claim_ledger_refinement/results/2026-07-15-local.json",
        "lean/AsiStackProofs/ClaimLedgerRefinement.lean",
    ],
    "replacement_refs": [
        "proof-model:claim-ledger.append-only-evidence-owner-refinement.v1",
        "lean/AsiStackProofs/ClaimLedgerRefinement.lean",
    ],
}


def attach(record: dict) -> None:
    for key, values in REFS.items():
        record[key] = list(dict.fromkeys([*record.get(key, []), *values]))


def main() -> None:
    value = json.loads(REVIEWS.read_text())
    targets, theorems = value["target_reviews"], value["theorem_reviews"]
    if TARGETS - set(targets) or RETIRED - set(theorems):
        raise SystemExit("missing Claim Ledger frozen lineage")
    for target_id in TARGETS:
        record = targets[target_id]
        attach(record)
        record["semantic_role"] = "Reachable append-only revision lifecycle with evidence-owner custody, exact version binding, materialized view, and surface acknowledgment."
        record["assumptions"] = ["Claim identity, event digests, revision fields, evidence-owner receipt, dependency closure, ontology migration, and surface receipts are trusted inside the finite authored model."]
        record["excluded_effects"] = ["Truth, evidence validity, reviewer competence, semantic equivalence, assumption completeness, natural extraction, concurrent persistence, causal usefulness, reproduction, transfer, SOTA, and chapter support are excluded."]
        record["review_rationale"] = "Replace checklist acceptance and support-authority ambiguity with a reachable lifecycle whose ledger can only record an independently authorized decision."
    theorem_ids = [key for key in theorems if key.startswith(PREFIX)]
    for theorem_id in theorem_ids: attach(theorems[theorem_id])
    for theorem_id in RETIRED:
        record = theorems[theorem_id]
        record["review_state"] = "terminally_dispositioned"
        record["disposition"] = "retire_projection_or_assumption_restatement" if theorem_id.endswith(("valid_belief_revision_record_preserves_identity_history_and_boundary", "semantic_assumption_fixture_bridge")) else "replace_with_stronger_model"
        record["review_rationale"] = "Frozen lineage retained; declaration physically retired because it projected authored fields or a finite route already subsumed by the reachable append-only refinement."
    REVIEWS.write_text(json.dumps(value, indent=2) + "\n")
    print(f"Attached Claim Ledger refs to 4 targets and {len(theorem_ids)} frozen theorems; {len(RETIRED)} declarations retired.")


if __name__ == "__main__": main()
