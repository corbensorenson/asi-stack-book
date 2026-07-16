#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "validation/registry.json"
SCRIPT = "validate_resource_economics_refinement.py"
ARTIFACTS = [
    "scripts/validate_resource_economics_refinement.py",
    "schemas/resource_economics_refinement.schema.json",
    "experiments/resource_economics_refinement/results/2026-07-15-local.json",
    "docs/resource_economics_refinement.md",
    "evidence_quality/model_adequacy_dossiers/resource-economics-refinement.md",
    "lean/AsiStackProofs/ResourceEconomicsRefinement.lean",
    "experiments/resource_budget_ledgers/results/2026-07-01-local.md",
    "experiments/costed_route_resource_slice/results/2026-06-29-local.json",
    "experiments/resource_workflow_trace/results/2026-07-01-local.json",
    "experiments/capacity_smoothing/results/2026-07-01-local.md",
    "experiments/resource_flagship_lane/results/2026-07-01-local.json",
    "experiments/resource_ci_cost_profile/results/2026-07-04-main.json",
    "experiments/resource_governance_tax_tradeoff/results/2026-07-03-local.json",
    "experiments/simulation_transfer_boundaries/results/2026-06-30-local.md",
    "experiments/theseus_simulation_fidelity_receipt_suite_import/results/2026-07-05-local.json",
    "experiments/theseus_rlds_minari_trace_export_import/results/2026-07-05-local.json",
    "experiments/resource_workload_quality_probe/results/2026-07-01-local.json",
    "experiments/resource_load_stability_probe/results/2026-07-01-local.json",
]

registry = json.loads(PATH.read_text())
registry["units"] = [unit for unit in registry["units"] if unit.get("script") != SCRIPT]
order = len(registry["units"]) + 1
registry["units"].append({
    "id": f"{SCRIPT}:{order}",
    "order": order,
    "script": SCRIPT,
    "args": [],
    "execution_tier": "deep",
    "validation_class": "proof_or_evidence_gate",
    "input_contract": "Reachable allocation, execution, simulation-transport, reconciliation, and closure lifecycle; twelve bounded resource/simulation source families; independent route consumer; schema; result; and adequacy dossier.",
    "input_artifacts": ARTIFACTS,
    "output_contract": "Reject identity, rights, resource, event, budget, protected-floor, capacity, queue, observed-spend, verification, simulation-fidelity, reconciliation, closure, support, and effect failures.",
    "output_assertions": ["nine reachable stages", "66 routes", "57 rejected non-accepting mutations", "twelve SHA-256-bound source results", "support and external effect none"],
    "claim_scope": "One finite authored allocation-and-simulation-transport policy plus exact bounded fixture, repository-replay, local-timing, historical-CI, and sanitized-import identities.",
    "negative_controls": "validator_owned_resource_economics_route_mutations",
    "negative_control_cases": ["identity, policy, rights, resource, evidence, event, or authority substitution", "missing budgets, protected floors, capacity, reviewer/verifier capacity, queue, spend, verification, simulation, reconciliation, or closure fields", "raw-proxy, fidelity, support, or effect laundering"],
    "prohibited_inference": "No economic optimality, useful throughput, model quality, safety, deployed scheduling, reviewer productivity, simulation adequacy, physical feasibility, transfer, SOTA, AGI, ASI, or support.",
    "contract_precision": "inherited",
    "semantic_review_state": "checked_allocation_and_simulation_transport_lifecycle_not_economic_or_simulation_benefit_or_support_authority",
})
required = list(registry["required_artifacts"])
for artifact in ARTIFACTS:
    if artifact not in required:
        required.append(artifact)
registry["required_artifacts"] = required
registry["summary"] = {"required_artifact_count": len(required), "unit_count": len(registry["units"])}
PATH.write_text(json.dumps(registry, indent=2) + "\n")
print(f"Registered {SCRIPT}: {len(registry['units'])} units, {len(required)} artifacts.")
