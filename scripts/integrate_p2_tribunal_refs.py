#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEWS = ROOT / "proofs/proof_rationalization_reviews.json"
PREFIX = "lean/AsiStackProofs/Tribunal.lean::"
TARGETS = {
    "lean:tribunal.review.operational_invariant",
    "lean:tribunal.review.failure_blocks_promotion",
}
RETIRED_NAMES = {
    "tribunal_verdict_includes_roles_evidence_and_unresolved_dissent",
    "high_risk_artifact_without_required_tribunal_review_cannot_be_accepted",
    "tribunal_route_missing_review_rejects",
    "high_risk_without_probe_routes_to_adversarial_probe",
    "high_risk_without_independent_reviewer_routes_to_independent_review",
    "changed_evidence_blocks_prior_review_reuse",
    "unrecorded_dissent_routes_to_dissent_preservation",
    "action_verdict_without_constraints_routes_to_action_constraints",
    "support_change_without_evidence_transition_routes_to_evidence_review",
    "complete_bounded_tribunal_review_accepts",
}
RETIRED = {PREFIX + name for name in RETIRED_NAMES}
REFS = {
    "countermodel_refs": [
        "lean/AsiStackProofs/TribunalRefinement.lean#route-countermodels",
        "experiments/tribunal_review/fixtures",
        "experiments/tribunal_method_independence/fixtures",
    ],
    "mutation_refs": ["scripts/validate_tribunal_refinement.py#mutations"],
    "consumer_refs": [
        "docs:tribunal_refinement",
        "evidence_quality:model_adequacy_dossiers/tribunal-refinement.md",
    ],
    "runtime_consumer_refs": [
        "scripts/validate_tribunal_refinement.py",
        "schemas/tribunal_refinement.schema.json",
        "experiments/tribunal_refinement/results/2026-07-15-local.json",
        "lean/AsiStackProofs/TribunalRefinement.lean",
        "scripts/validate_tribunal_review.py",
        "scripts/validate_tribunal_method_independence.py",
    ],
    "replacement_refs": [
        "proof-model:tribunal.versioned-verdict-appeal-refinement.v1",
        "lean/AsiStackProofs/TribunalRefinement.lean",
    ],
}


def attach(record: dict) -> None:
    for key, values in REFS.items():
        record[key] = list(dict.fromkeys([*record.get(key, []), *values]))


def main() -> None:
    value = json.loads(REVIEWS.read_text())
    targets, theorems = value["target_reviews"], value["theorem_reviews"]
    if TARGETS - set(targets) or RETIRED - set(theorems):
        raise SystemExit("missing Tribunal frozen lineage")
    for target_id in TARGETS:
        record = targets[target_id]
        attach(record)
        record["semantic_role"] = "Reachable versioned review-request, dossier, panel, verdict, consumer-acknowledgment, and appeal lifecycle with exact custody and no support/effect authority."
        record["assumptions"] = ["Case, evidence, dossier, panel, policy, consumer, method, reviewer, independence, falsification, dissent, action, residual, appeal, handoff, acknowledgment, and digest fields are trusted inside the finite authored model."]
        record["excluded_effects"] = ["Reviewer competence, independence in fact, evidence truth, probe quality, verdict correctness, legitimacy, fairness, action or appeal efficacy, claim truth, support, effects, usefulness, causality, safety, deployment, reproduction, transfer, and SOTA are excluded."]
        record["review_rationale"] = "Replace assumed policy and literal-route declarations with a reachable lifecycle, exact legacy suites, twenty-eight route cases, forty-five rejecting mutations, and explicit owner/consumer/appeal custody."
    theorem_ids = [key for key in theorems if key.startswith(PREFIX)]
    for theorem_id in theorem_ids:
        attach(theorems[theorem_id])
    for theorem_id in RETIRED:
        record = theorems[theorem_id]
        record["review_state"] = "terminally_dispositioned"
        if record.get("disposition") not in {"retire_projection_or_assumption_restatement", "replace_with_stronger_model"}:
            record["disposition"] = "replace_with_stronger_model"
        record["review_rationale"] = "Frozen lineage retained; declaration physically retired because it was an assumption restatement or literal finite normalization now subsumed by the reachable versioned-verdict and appeal refinement."
    REVIEWS.write_text(json.dumps(value, indent=2) + "\n")
    print(f"Attached Tribunal refs to 2 targets and {len(theorem_ids)} frozen theorems; 10 declarations retired.")


if __name__ == "__main__":
    main()
