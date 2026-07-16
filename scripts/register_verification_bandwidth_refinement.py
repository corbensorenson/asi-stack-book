#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_verification_bandwidth_refinement.py"
ARTIFACTS = [
    "scripts/validate_verification_bandwidth_refinement.py",
    "schemas/verification_bandwidth_refinement.schema.json",
    "experiments/verification_bandwidth_refinement/results/2026-07-15-local.json",
    "docs/verification_bandwidth_refinement.md",
    "evidence_quality/model_adequacy_dossiers/verification-bandwidth-refinement.md",
    "lean/AsiStackProofs/VerificationBandwidthRefinement.lean",
    "scripts/validate_context_admission_adequacy.py",
    "experiments/context_admission_adequacy/fixtures",
    "scripts/validate_verification_bandwidth_probe.py",
    "experiments/verification_bandwidth/results/2026-07-02-local.json",
    "scripts/validate_verification_bandwidth_capacity_model.py",
    "experiments/verification_bandwidth_capacity/results/2026-07-03-local.json",
]


def main() -> None:
    value = json.loads(REGISTRY.read_text())
    value["units"] = [unit for unit in value["units"] if unit.get("script") != SCRIPT]
    order = len(value["units"]) + 1
    value["units"].append({
        "id": f"validate_verification_bandwidth_refinement:{order}",
        "order": order,
        "script": SCRIPT,
        "args": [],
        "execution_tier": "deep",
        "validation_class": "proof_or_evidence_gate",
        "input_contract": "Reachable Lean verification-plan lifecycle, exact admission/contradiction/capacity validators and results, context-adequacy schema, independent consumer, result schema, receipt, and adequacy dossier.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Reject identity, context, authority, rights, budget, horizon, stop-rule, promotion, disposition, contradiction, evaluator-dependence, negative-search, artifact, residual, and expiry faults before evidence-gate handoff.",
        "output_assertions": [
            "three valid and five invalid admission fixtures",
            "two valid and seven invalid contradiction traces",
            "three valid and five invalid capacity traces",
            "twelve routes and five reachable stages",
            "thirty-one rejected mutations",
            "no support-state effect",
        ],
        "claim_scope": "One finite authored plan/execution lifecycle and three existing bounded synthetic suites only.",
        "negative_controls": "validator_owned_plan_execution_and_route_mutations",
        "negative_control_cases": [
            "claim or packet substitution",
            "missing authority, rights, budget, horizon, or stop rule",
            "direct core promotion request",
            "contradiction or incomplete disposition",
            "correlated high-risk evaluator",
            "missing negative search, artifacts, residuals, or expiry",
        ],
        "prohibited_inference": "Does not establish model verification bandwidth, natural-claim adequacy, contradiction discovery, evaluator competence or independence, a capacity law, deployed ledger or escalation behavior, usefulness, causality, reproduction, transfer, safety, SOTA, AGI, ASI, or chapter-core support.",
        "contract_precision": "inherited",
        "semantic_review_state": "checked_structured_verification_lifecycle_not_model_measured_natural_or_deployed",
    })
    required = list(value["required_artifacts"])
    for artifact in ARTIFACTS:
        if artifact not in required:
            required.append(artifact)
    value["required_artifacts"] = required
    value["summary"] = {"required_artifact_count": len(required), "unit_count": len(value["units"])}
    REGISTRY.write_text(json.dumps(value, indent=2) + "\n")
    print(f"Registered {SCRIPT}: {len(value['units'])} units, {len(required)} artifacts.")


if __name__ == "__main__":
    main()
