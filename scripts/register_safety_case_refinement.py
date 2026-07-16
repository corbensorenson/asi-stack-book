#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_safety_case_refinement.py"
ARTIFACTS = [
    "scripts/validate_safety_case_refinement.py",
    "schemas/safety_case_refinement.schema.json",
    "experiments/safety_case_refinement/results/2026-07-15-local.json",
    "docs/safety_case_refinement.md",
    "evidence_quality/model_adequacy_dossiers/safety-case-refinement.md",
    "lean/AsiStackProofs/SafetyCaseRefinement.lean",
    "scripts/validate_safety_case_assurance.py",
    "experiments/safety_case_assurance/fixtures/cases.json",
    "experiments/safety_case_assurance/results/2026-07-13-local.json",
]


def main() -> None:
    value = json.loads(REGISTRY.read_text())
    value["units"] = [unit for unit in value["units"] if unit.get("script") != SCRIPT]
    order = len(value["units"]) + 1
    value["units"].append({
        "id": f"{SCRIPT}:{order}", "order": order, "script": SCRIPT, "args": [],
        "execution_tier": "deep", "validation_class": "proof_or_evidence_gate",
        "input_contract": "Reachable Lean safety-case lifecycle, exact inherited eight-case suite, independent consumer, result schema, receipt, and model-adequacy dossier.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Reject identity substitution, missing scope/evidence/challenge/review/authority/invalidation custody, replay, authority laundering, and support/effect leakage.",
        "output_assertions": ["eight exact inherited cases", "thirty routes and six reachable stages", "thirty-five rejected mutations", "readiness handoff followed by descendant-aware invalidation", "no support-state or external-effect authority"],
        "claim_scope": "One finite authored safety-case record lifecycle plus the existing eight-case fixture only.",
        "negative_controls": "validator_owned_identity_lifecycle_defeater_review_invalidation_authority_mutations",
        "negative_control_cases": ["case, version, context, claim, hazard, evidence, countercase, reviewer, authority, or residual substitution", "missing or stale scope, evidence, assumptions, countercase, defeater, review, acceptance, residual, or authority records", "review conflict, unresolved defeater, authority laundering, or incomplete descendant invalidation", "wrong stage, replay, support assignment, or external-effect request"],
        "prohibited_inference": "Does not establish argument truth, hazard completeness, evidence adequacy, reviewer independence, control effectiveness, safety, readiness, release authority, deployed invalidation, transfer, AGI, ASI, or chapter-core support.",
        "contract_precision": "inherited",
        "semantic_review_state": "checked_structured_safety_case_lifecycle_not_truth_deployed_or_support_authority",
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
