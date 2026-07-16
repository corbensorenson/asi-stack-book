#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STRUCTURE = ROOT / "book_structure.json"
TRIAGE = ROOT / "proofs/proof_triage.json"
REVIEWS = ROOT / "proofs/proof_rationalization_reviews.json"
MODULE = "AsiStackProofs.ResourceEconomicsRefinement"
TARGETS = {
    "lean:resources.budgets.operational_invariant": "A reachable allocation lifecycle requires a scoped request, explicit resource inventory and units, direct, displaced, verification, and uncertainty costs, protected floors, bounded capacity, reviewer and verifier capacity, queue policy, observed spend, useful-outcome accounting, verification, reconciliation, and closure.",
    "lean:resources.budgets.failure_blocks_promotion": "Missing protected floors, reviewer capacity, failure retention, or evidence-transition accounting blocks the corresponding allocation stage; raw resource proxies cannot promote support.",
    "lean:resources.costed_route.fixture_bridge": "The stronger lifecycle digest-binds the bounded four-route cost fixture while preserving its two eligible and two rejected routes and its fixture-specific 66.98% arithmetic without inferring economic optimality.",
    "lean:resources.workflow_trace.trace_property_bridge": "The stronger lifecycle digest-binds the three-step workflow result and requires queue policy, high-risk priority, protected overhead, residual ownership, actual spend, verification outcome, variance, incidents, descendants, and closure.",
    "lean:resources.capacity_smoothing.reviewer_trace_bridge": "Reservation and scheduling require capacity, reviewer and verifier capacity, protected overhead, debt expiry, an owner, high-risk priority, tenant isolation, tail policy, fallback, and later variance and opportunity-cost reconciliation.",
    "lean:resources.serving_memory.separation_guard": "Observed resource bills and useful outcomes remain separate, and raw throughput, memory, or cost proxies cannot promote support without verification and evidence-transition accounting.",
    "lean:resource.governance_tax.tradeoff_bridge": "The lifecycle digest-binds the three-scenario governance-tax fixture while keeping its two governed choices and one low-risk shortcut explicitly synthetic, cost-complete only within the fixture, and non-promotional.",
    "lean:simulation.fidelity.operational_invariant": "Transported simulation claims require explicit scope, fidelity, temporal semantics, resource bills, omissions, and a transfer decision before reconciliation.",
    "lean:simulation.fidelity.failure_blocks_promotion": "A simulated claim above its declared fidelity support is blocked before reconciliation, and missing simulation scope, fidelity, temporal semantics, resource bills, omissions, or transfer decisions cannot pass.",
    "lean:resource.simulation_fidelity.theseus_receipt_suite.fixture_bridge": "The lifecycle digest-binds the sanitized five-scenario, six-receipt Theseus simulation result while preserving its seven invalid controls and excluding physical-feasibility, benchmark-transfer, native-parity, deployment, and support claims.",
    "lean:resource.simulation_fidelity.theseus_rlds_minari_trace_export.fixture_bridge": "The lifecycle digest-binds the sanitized one-ready-export, three-format, seven-field Theseus trace result while preserving its seven invalid controls and excluding dataset-quality, replay-success, deployment, and support claims.",
}
RETIRED_TARGETS = {
    "lean:resources.flagship.aggregate_invariant",
    "lean:resources.ci_failure_classification.fixture_bridge",
}
PREFIXES = (
    "lean/AsiStackProofs/ResourceEconomics.lean::",
    "lean/AsiStackProofs/SimulationFidelity.lean::",
)
RETAINED = {
    "required_safety_gate_disabled_rejects_budget_gate_preservation",
    "high_risk_insufficient_budget_dispatch_rejected",
    "serving_memory_throughput_quality_overclaim_rejected",
    "costed_route_fixture_selected_is_eligible",
    "cheap_unverified_transform_rejected_by_fixture",
    "hidden_residual_auto_merge_rejected_by_fixture",
    "selected_route_is_lowest_cost_eligible_in_fixture",
    "costed_route_fixture_trace_selects_lowest_eligible_route",
    "resource_workflow_trace_fixture_events_roll_up_to_summary",
    "resource_workflow_trace_fixture_events_keep_high_risk_first",
    "resource_workflow_trace_fixture_events_preserve_guard_flags",
    "blocked_protected_review_rejects_low_risk_review_dispatch",
    "high_risk_review_without_protected_overhead_rejected",
    "blocked_protected_review_requires_displaced_cost_residual",
    "evidence_use_without_scope_declaration_rejected",
    "promoted_result_above_declared_fidelity_rejected",
    "theseus_simulation_fidelity_receipt_suite_import_core_promotion_rejected",
    "theseus_simulation_fidelity_receipt_suite_import_physical_feasibility_overclaim_rejected",
    "theseus_simulation_fidelity_receipt_suite_import_benchmark_transfer_overclaim_rejected",
    "theseus_simulation_fidelity_receipt_suite_import_native_kv_parity_overclaim_rejected",
    "theseus_rlds_minari_trace_export_import_core_promotion_rejected",
    "theseus_rlds_minari_trace_export_import_dataset_quality_overclaim_rejected",
    "theseus_rlds_minari_trace_export_import_replay_success_overclaim_rejected",
}
REFS = {
    "countermodel_refs": ["lean/AsiStackProofs/ResourceEconomicsRefinement.lean#countermodels"],
    "mutation_refs": ["scripts/validate_resource_economics_refinement.py#route_cases"],
    "consumer_refs": ["docs:resource_economics_refinement", "evidence_quality:model_adequacy_dossiers/resource-economics-refinement.md"],
    "runtime_consumer_refs": [
        "scripts/validate_resource_economics_refinement.py",
        "schemas/resource_economics_refinement.schema.json",
        "experiments/resource_economics_refinement/results/2026-07-15-local.json",
        "scripts/validate_resource_flagship_lane.py",
        "scripts/validate_resource_workload_quality_probe.py",
        "scripts/validate_resource_load_stability_probe.py",
    ],
    "replacement_refs": ["proof-model:resource-economics.request-to-closure-refinement.v1", "lean/AsiStackProofs/ResourceEconomicsRefinement.lean"],
}


def attach(record: dict) -> None:
    for key, refs in REFS.items():
        record[key] = list(dict.fromkeys([*record.get(key, []), *refs]))


def main() -> None:
    structure = json.loads(STRUCTURE.read_text())
    chapter = next(c for p in structure["parts"] for c in p["chapters"] if c["id"] == "resource-economics-and-token-budgets")
    for target in chapter["proof_targets"]:
        if target["tag"] in TARGETS:
            target["module"] = MODULE
            target["target"] = TARGETS[target["tag"]]
    chapter["lean_module"] = "AsiStackProofs.ResourceEconomics; AsiStackProofs.SimulationFidelity; AsiStackProofs.ResourceEconomicsRefinement"
    chapter["minimal_implementation"] = "Twenty-three retained countermodels and bounded computations plus an eight-declaration, nine-stage, 66-route allocation, execution, simulation-transport, reconciliation, and closure lifecycle; an independently implemented consumer rejects 57/57 non-accepting mutations and digest-binds twelve bounded source families. Thirty-five assumption projections and copied fixture summaries are retired. The model separates useful outcomes from raw resource proxies, blocks fidelity overclaims, requires failure and unsafe-release accounting, and grants no support or external-effect authority. This is bounded policy/conformance evidence over synthetic fixtures, repository replays, local timing, historical CI, and sanitized imports—not economic optimality, deployed scheduling, useful-throughput improvement, simulation adequacy, physical feasibility, transfer, or SOTA evidence."
    chapter["codex_tests"] = [x for x in chapter["codex_tests"] if not (isinstance(x, dict) and x.get("name") == "Resource Economics request-to-closure refinement")]
    chapter["codex_tests"].append({
        "name": "Resource Economics request-to-closure refinement",
        "implementation_status": "implemented",
        "result_status": "passes nine stages, all 66 routes, 57/57 non-accepting mutations, twelve digest-bound bounded source families, resource/simulation separation, reconciliation and closure, support/effect none; no economic-optimality, useful-throughput, deployment, simulation-adequacy, transfer, or support claim",
    })
    STRUCTURE.write_text(json.dumps(structure, indent=2) + "\n")

    triage = json.loads(TRIAGE.read_text())
    triage["records"] = [record for record in triage["records"] if record["tag"] not in RETIRED_TARGETS]
    for record in triage["records"]:
        if record["tag"] in TARGETS:
            record["module"] = MODULE
            record["formal_target"] = TARGETS[record["tag"]]
            record["rationale"] = "Reachable nine-stage allocation-and-simulation-transport lifecycle, 66 routes, 57 rejecting mutations, twelve digest-bound bounded source families, and no support/effect authority."
    triage["record_count"] = len(triage["records"])
    TRIAGE.write_text(json.dumps(triage, indent=2) + "\n")

    reviews = json.loads(REVIEWS.read_text())
    for tag in TARGETS:
        record = reviews["target_reviews"][tag]
        attach(record)
        record["semantic_role"] = "Reachable request, budgeting, reservation, scheduling, execution, verification, simulation transport, reconciliation, and closure lifecycle."
        record["assumptions"] = ["All identities, authored policy fields, resource facts, costs, capacity, outcome, evaluator, simulation, incident, descendant, and closure facts are trusted inside the finite model."]
        record["excluded_effects"] = ["Economic optimality, real useful throughput, model quality, real reviewer or verifier capacity, deployed scheduling, simulation adequacy, physical feasibility, transfer, SOTA, and support are excluded."]
        record["review_rationale"] = "Replace copied record summaries and direct implications with a reachable lifecycle and independently implemented digest-bound consumer."
    theorem_ids = [key for key in reviews["theorem_reviews"] if key.startswith(PREFIXES)]
    retired = 0
    for key in theorem_ids:
        record = reviews["theorem_reviews"][key]
        attach(record)
        if key.rsplit("::", 1)[1] not in RETAINED:
            retired += 1
            record["review_state"] = "terminally_dispositioned"
            record["disposition"] = "replace_with_stronger_model"
            record["review_rationale"] = "Frozen lineage retained; declaration physically retired because the assumption projection or copied summary is subsumed by reachable identity, allocation, verification, simulation, reconciliation, closure, support, and effect semantics."
    REVIEWS.write_text(json.dumps(reviews, indent=2) + "\n")
    print(f"Integrated Resource Economics refinement across {len(TARGETS)} targets and {len(theorem_ids)} frozen declarations; {retired} retired and {len(RETAINED)} retained.")


if __name__ == "__main__":
    main()
