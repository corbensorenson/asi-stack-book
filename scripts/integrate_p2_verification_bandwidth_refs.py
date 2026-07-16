#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEWS = ROOT / "proofs/proof_rationalization_reviews.json"
PREFIX = "lean/AsiStackProofs/VerificationBandwidth.lean::"
TARGETS = {
    "lean:verification_bandwidth.adequacy.operational_invariant",
    "lean:verification_bandwidth.adequacy.failure_blocks_promotion",
    "lean:verification_bandwidth.adequacy.route_envelope",
    "lean:verification_bandwidth.contradiction_probe_fixture_bridge",
}
RETIRED = {
    PREFIX + "high_risk_claim_with_inadequate_context_cannot_receive_verified_support",
    PREFIX + "complete_verified_review_allows_verified_support",
    PREFIX + "verification_bandwidth_contradiction_probe_fixture_bridge",
    PREFIX + "verification_bandwidth_capacity_model_fixture_bridge",
}
REFS = {
    "countermodel_refs": [
        "lean/AsiStackProofs/VerificationBandwidthRefinement.lean#route-countermodels",
        "experiments/context_admission_adequacy/fixtures",
        "experiments/verification_bandwidth/results/2026-07-02-local.json",
        "experiments/verification_bandwidth_capacity/results/2026-07-03-local.json",
    ],
    "mutation_refs": ["scripts/validate_verification_bandwidth_refinement.py#mutations"],
    "consumer_refs": [
        "docs:verification_bandwidth_refinement",
        "evidence_quality:model_adequacy_dossiers/verification-bandwidth-refinement.md",
    ],
    "runtime_consumer_refs": [
        "scripts/validate_verification_bandwidth_refinement.py",
        "schemas/verification_bandwidth_refinement.schema.json",
        "experiments/verification_bandwidth_refinement/results/2026-07-15-local.json",
        "lean/AsiStackProofs/VerificationBandwidthRefinement.lean",
    ],
    "replacement_refs": [
        "proof-model:verification-bandwidth.reachable-evidence-gate-refinement.v1",
        "lean/AsiStackProofs/VerificationBandwidthRefinement.lean",
    ],
}


def attach(record: dict) -> None:
    for key, values in REFS.items():
        record[key] = list(dict.fromkeys([*record.get(key, []), *values]))


def main() -> None:
    value = json.loads(REVIEWS.read_text())
    targets = value["target_reviews"]
    theorems = value["theorem_reviews"]
    if TARGETS - set(targets) or RETIRED - set(theorems):
        raise SystemExit("missing Verification Bandwidth lineage")
    for target_id in TARGETS:
        record = targets[target_id]
        attach(record)
        record["semantic_role"] = "Reachable prospective verification plan, exact execution binding, exhaustive disposition accounting, route priority, and authority-separated evidence-gate handoff."
        record["assumptions"] = ["Claim, context, risk, authority, rights, obligation decomposition, evaluator separation, artifacts, costs, outcomes, and dispositions are trusted inside the finite authored model."]
        record["excluded_effects"] = ["Model verification capacity, natural-claim adequacy, contradiction discovery, evaluator competence or causal independence, usefulness, safety, deployed support enforcement, reproduction, transfer, SOTA, and core support are excluded."]
        record["review_rationale"] = "Replace support-assignment and copied-summary ownership with a reachable lifecycle whose strongest result is handoff to an independent evidence gate."
    theorem_ids = [key for key in theorems if key.startswith(PREFIX)]
    for theorem_id in theorem_ids:
        attach(theorems[theorem_id])
    for theorem_id in RETIRED:
        record = theorems[theorem_id]
        record["review_state"] = "terminally_dispositioned"
        record["disposition"] = "retire_projection_or_assumption_restatement"
        record["review_rationale"] = "Frozen lineage retained; declaration physically retired because it projected an assumption, copied validator summary fields, or mislabeled adequacy as authority to assign verified support. Superseded by the reachable evidence-gate refinement."
    REVIEWS.write_text(json.dumps(value, indent=2) + "\n")
    print(f"Attached Verification Bandwidth refs to 4 targets and {len(theorem_ids)} theorems; 4 declarations retired.")


if __name__ == "__main__":
    main()
