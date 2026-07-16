#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STRUCTURE = ROOT / "book_structure.json"
TRIAGE = ROOT / "proofs/proof_triage.json"
REVIEWS = ROOT / "proofs/proof_rationalization_reviews.json"
MODULE = "AsiStackProofs.RoutingRefinement"
TARGETS = {
    "lean:routing.specialists.operational_invariant": "A reachable routing lifecycle preserves exact task, request, registry, candidate-set, selected-specialist, authority, readiness, lease, evaluator, policy, and consumer custody from request binding through consumer-acknowledged closure while keeping route and answer outcomes distinct and assigning no support or external effects.",
    "lean:routing.specialists.failure_blocks_promotion": "Missing authority, readiness, fresh leases, selective handling, fallback or residual ownership, dispatch isolation, observed route/answer/unsafe/cost outcomes, lifecycle currentness, revocation closure, or consumer acknowledgment blocks lifecycle progress.",
    "lean:routing.specialists.decision_lifecycle_route": "The independent consumer preserves all forty-two routing outcomes, including label-leak rejection, complete candidate denominators, least-capable-adequate selection, ambiguity-triggered selective action, fallback/residual routes, and separate dispatch, observation, and closure stages.",
    "lean:moecot.runtime.operational_invariant": "A runtime-backed route cannot qualify until inspected source state, concrete runtime evidence, replay evidence, task-local dispatch authority, and isolation are bound to the same routing lease.",
    "lean:moecot.runtime.failure_blocks_promotion": "Unavailable or source-only runtime material, missing replay evidence, or unobserved route and answer outcomes cannot be laundered into runtime, routing-quality, support, or deployment claims.",
}
ROUTING_PREFIX = "lean/AsiStackProofs/Routing.lean::"
MOECOT_PREFIX = "lean/AsiStackProofs/MoECOTRuntime.lean::"
RETIRED = {
    *(ROUTING_PREFIX + name for name in [
        "selected_specialist_satisfies_authority_and_readiness", "no_route_request_stays_no_route",
        "missing_capability_request_rejects_route", "missing_specialist_registry_requests_registry",
        "authority_mismatch_blocks_route_selection", "readiness_failure_with_fallback_routes_to_fallback",
        "readiness_failure_without_fallback_or_residual_owner_requests_owner",
        "readiness_failure_without_fallback_residualizes_when_owner_present",
        "missing_fresh_lease_requests_lease", "missing_cost_quality_record_requests_record",
        "overprivileged_selection_requests_least_capable_justification",
        "missing_rejected_candidate_evidence_requests_evidence",
        "route_without_nonclaim_boundary_preserves_boundary", "complete_routing_decision_selects_specialist",
    ]),
    MOECOT_PREFIX + "runtime_core_promotion_requires_readiness_regression_and_replay_evidence",
    MOECOT_PREFIX + "runtime_claim_from_unavailable_text_only_cannot_promote_above_argument",
}
REFS = {
    "countermodel_refs": ["lean/AsiStackProofs/RoutingRefinement.lean#countermodels"],
    "mutation_refs": ["scripts/validate_routing_refinement.py#mutations"],
    "consumer_refs": ["docs:routing_refinement", "evidence_quality:model_adequacy_dossiers/routing-refinement.md"],
    "runtime_consumer_refs": [
        "scripts/validate_routing_refinement.py", "schemas/routing_refinement.schema.json",
        "experiments/routing_refinement/results/2026-07-15-local.json",
        "scripts/validate_routing_decision_lease.py", "scripts/validate_readiness_residual_gates.py",
        "scripts/validate_post_v2_routing_deliberation.py",
    ],
    "replacement_refs": ["proof-model:routing-refinement.v1", "lean/AsiStackProofs/RoutingRefinement.lean"],
}


def attach(row: dict) -> None:
    for key, values in REFS.items():
        row[key] = list(dict.fromkeys([*row.get(key, []), *values]))


def main() -> None:
    structure = json.loads(STRUCTURE.read_text())
    chapter = next(c for p in structure["parts"] for c in p["chapters"] if c["id"] == "routing-heads-and-specialist-cores")
    for target in chapter["proof_targets"]:
        if target["tag"] in TARGETS:
            target["module"] = MODULE; target["target"] = TARGETS[target["tag"]]
    chapter["lean_module"] = "AsiStackProofs.Routing; AsiStackProofs.MoECOTRuntime; AsiStackProofs.RoutingRefinement"
    chapter["codex_tests"] = [row for row in chapter["codex_tests"] if not (isinstance(row, dict) and row.get("name") == "Routing and replaceable-substrate lifecycle refinement")]
    chapter["codex_tests"].append({
        "name": "Routing and replaceable-substrate lifecycle refinement", "implementation_status": "implemented",
        "result_status": "passes three exact suites, 42 routes, seven reachable stages, and 47/47 rejecting mutations; route and answer outcomes remain distinct; support-state effect none; no natural useful-routing, strong-model transfer, deployed runtime/replay correctness, substrate superiority, RSI, or support claim",
    })
    STRUCTURE.write_text(json.dumps(structure, indent=2) + "\n")

    triage = json.loads(TRIAGE.read_text())
    for row in triage["records"]:
        if row["tag"] in TARGETS:
            row["module"] = MODULE; row["formal_target"] = TARGETS[row["tag"]]
            row["rationale"] = "Reachable seven-stage routing lifecycle with exact request/registry/lease custody, three bounded suites, 42 routes, 47 rejecting mutations, distinct route/answer outcomes, and no support or effect authority."
    TRIAGE.write_text(json.dumps(triage, indent=2) + "\n")

    reviews = json.loads(REVIEWS.read_text())
    for target in TARGETS:
        row = reviews["target_reviews"][target]; attach(row)
        row["semantic_role"] = "Reachable request, registry, lease, dispatch, observation, and revocation-aware closure lifecycle for architecture-neutral specialist routing."
        row["assumptions"] = ["Task, registry, candidate, specialist, authority, readiness, lease, evaluator, policy, consumer, runtime-reference, replay-reference, and outcome fields are trusted inside the finite authored model."]
        row["excluded_effects"] = ["Natural-task utility, semantic route fit, answer correctness, evaluator independence, runtime execution, replay fidelity, deployed authority, substrate superiority, autonomous architecture search, RSI, safety, reproduction, transfer, SOTA, and chapter-core support are excluded."]
        row["review_rationale"] = "Replace assumption projections and fixture admissions with a reachable architecture-neutral routing lifecycle, three exact suites, forty-two routes, and 47 rejecting mutations."
    theorem_ids = [key for key in reviews["theorem_reviews"] if key.startswith(ROUTING_PREFIX) or key.startswith(MOECOT_PREFIX)]
    for key in theorem_ids: attach(reviews["theorem_reviews"][key])
    for key in RETIRED:
        row = reviews["theorem_reviews"][key]
        row["review_state"] = "terminally_dispositioned"; row["disposition"] = "replace_with_stronger_model"
        row["review_rationale"] = "Frozen lineage retained; declaration physically retired because it projected an assumption or normalized an authored fixture admission now subsumed by the reachable routing refinement."
    REVIEWS.write_text(json.dumps(reviews, indent=2) + "\n")
    print(f"Integrated Routing/MoECOT refinement across 5 targets and {len(theorem_ids)} frozen declarations; {len(RETIRED)} declarations retired.")


if __name__ == "__main__": main()
