#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_routing_refinement.py"
ARTIFACTS = [
    "scripts/validate_routing_refinement.py", "schemas/routing_refinement.schema.json",
    "experiments/routing_refinement/results/2026-07-15-local.json", "docs/routing_refinement.md",
    "evidence_quality/model_adequacy_dossiers/routing-refinement.md",
    "lean/AsiStackProofs/RoutingRefinement.lean", "scripts/validate_routing_decision_lease.py",
    "experiments/routing_decision_lease/fixtures", "scripts/validate_readiness_residual_gates.py",
    "experiments/readiness_residual_gates/fixtures", "scripts/validate_post_v2_routing_deliberation.py",
    "experiments/post_v2_routing_deliberation/results/2026-07-10-local.json",
]


def main() -> None:
    registry = json.loads(REGISTRY.read_text())
    registry["units"] = [unit for unit in registry["units"] if unit.get("script") != SCRIPT]
    order = len(registry["units"]) + 1
    registry["units"].append({
        "id": f"{SCRIPT}:{order}", "order": order, "script": SCRIPT, "args": [],
        "execution_tier": "deep", "validation_class": "proof_or_evidence_gate",
        "input_contract": "Reachable Lean routing lifecycle, three exact bounded suites, independent consumer, result schema, receipt, and model-adequacy dossier.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Reject identity substitution, label leakage, incomplete denominators, missing authority/readiness/leases/selective action/runtime/replay evidence, dispatch isolation gaps, outcome conflation, incomplete revocation closure, and support/effect leakage.",
        "output_assertions": ["three exact bounded suites", "forty-two routes and seven reachable stages", "forty-seven rejected mutations", "separate route and answer outcomes", "no support-state or external-effect authority"],
        "claim_scope": "One finite authored routing lifecycle plus three existing bounded suites only.",
        "negative_controls": "validator_owned_identity_registry_lease_dispatch_outcome_revocation_authority_mutations",
        "negative_control_cases": ["task, registry, candidate, specialist, lease, evaluator, policy, consumer, or event substitution", "held-out label leak or incomplete candidate denominator", "missing readiness fallback/residual ownership, selective action, runtime/replay evidence, dispatch grant, or isolation", "conflated or missing route/answer/unsafe/cost outcomes and incomplete revocation closure", "support assignment or external-effect authority leak"],
        "prohibited_inference": "Does not establish natural routing utility, model-scale transfer, answer correctness, evaluator independence, deployed routing or MoECOT runtime/replay correctness, substrate superiority, autonomous architecture search, RSI, SOTA, AGI, ASI, or chapter-core support.",
        "contract_precision": "inherited",
        "semantic_review_state": "checked_structured_architecture_neutral_routing_lifecycle_not_natural_deployed_answer_correct_or_support_authority",
    })
    required = list(registry["required_artifacts"])
    for artifact in ARTIFACTS:
        if artifact not in required: required.append(artifact)
    registry["required_artifacts"] = required
    registry["summary"] = {"required_artifact_count": len(required), "unit_count": len(registry["units"])}
    REGISTRY.write_text(json.dumps(registry, indent=2) + "\n")
    print(f"Registered {SCRIPT}: {len(registry['units'])} units, {len(required)} artifacts.")


if __name__ == "__main__": main()
