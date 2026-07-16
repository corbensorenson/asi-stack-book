#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_tribunal_refinement.py"
ARTIFACTS = [
    "scripts/validate_tribunal_refinement.py",
    "schemas/tribunal_refinement.schema.json",
    "experiments/tribunal_refinement/results/2026-07-15-local.json",
    "docs/tribunal_refinement.md",
    "evidence_quality/model_adequacy_dossiers/tribunal-refinement.md",
    "lean/AsiStackProofs/TribunalRefinement.lean",
    "scripts/validate_tribunal_review.py",
    "schemas/tribunal_review_record.schema.json",
    "experiments/tribunal_review/fixtures",
    "scripts/validate_tribunal_method_independence.py",
    "schemas/tribunal_method_independence_record.schema.json",
    "tests/fixtures/protocol_records/tribunal_method_independence_record.valid.json",
    "experiments/tribunal_method_independence/fixtures",
]


def main() -> None:
    value = json.loads(REGISTRY.read_text())
    value["units"] = [unit for unit in value["units"] if unit.get("script") != SCRIPT]
    order = len(value["units"]) + 1
    value["units"].append({
        "id": f"{SCRIPT}:{order}", "order": order, "script": SCRIPT, "args": [],
        "execution_tier": "deep", "validation_class": "proof_or_evidence_gate",
        "input_contract": "Reachable Lean Tribunal lifecycle, exact 3/5 review and 1/11 method-independence suites, independent consumer, result schema, receipt, and model-adequacy dossier.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Reject case/evidence/verdict/event substitution, replay, authority leakage, missing high-risk or independence discipline, default approval, changed-evidence reuse, erased abstention/veto/dissent, missing actions/constraints/residual/appeal/owner handoff/consumer acknowledgment, and unresolved requested appeal.",
        "output_assertions": ["three valid and five invalid Tribunal review fixtures", "one valid and eleven invalid method-independence records", "twenty-eight routes and seven reachable stages", "forty-five rejected lifecycle mutations", "no support-state effect"],
        "claim_scope": "One finite authored versioned Tribunal lifecycle plus two existing bounded synthetic suites only.",
        "negative_controls": "validator_owned_case_evidence_panel_verdict_appeal_authority_mutations",
        "negative_control_cases": ["case, evidence, verdict, or event substitution and replay", "missing high-risk probe, panel, independence graph, or falsification", "erased abstention, veto, or dissent", "changed-evidence reuse or default approval", "missing actions, constraints, residual, appeal, owner handoff, consumer acknowledgment, or appeal resolution", "support assignment or external effect authority leak"],
        "prohibited_inference": "Does not establish reviewer competence, independence in fact, evidence truth, probe/falsification quality, verdict correctness, legitimacy, fairness, action/appeal efficacy, claim truth, support, effects, usefulness, causality, safety, deployment, reproduction, transfer, SOTA, AGI, ASI, or chapter-core support.",
        "contract_precision": "inherited",
        "semantic_review_state": "checked_structured_versioned_verdict_appeal_lifecycle_not_competence_correctness_natural_deployed_or_support_authority",
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
