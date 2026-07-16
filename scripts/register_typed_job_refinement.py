#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_typed_job_refinement.py"
ARTIFACTS = [
    "scripts/validate_typed_job_refinement.py", "schemas/typed_job_refinement.schema.json",
    "experiments/typed_job_refinement/results/2026-07-15-local.json", "docs/typed_job_refinement.md",
    "evidence_quality/model_adequacy_dossiers/typed-job-refinement.md", "lean/AsiStackProofs/TypedJobRefinement.lean",
    "scripts/validate_typed_job_delivery_probe.py", "experiments/typed_job_delivery/results/2026-07-02-local.json",
    "docs/typed_job_delivery_probe.md", "scripts/validate_typed_job_durable_lifecycle_probe.py",
    "experiments/typed_job_durable_lifecycle/results/2026-07-02-local.json", "docs/typed_job_durable_lifecycle_probe.md",
]


def main() -> None:
    value = json.loads(REGISTRY.read_text())
    value["units"] = [unit for unit in value["units"] if unit.get("script") != SCRIPT]
    order = len(value["units"]) + 1
    value["units"].append({
        "id": f"{SCRIPT}:{order}", "order": order, "script": SCRIPT, "args": [],
        "execution_tier": "deep", "validation_class": "proof_or_evidence_gate",
        "input_contract": "Reachable Lean typed-job lifecycle, exact 2/7 delivery and 2/9 durable suites, independent consumer, result schema, receipt, and model-adequacy dossier.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Reject identity substitution, replay, authority leakage, unlocked contracts, approval/permission/lease/scheduler/dispatch gaps, retry/cancellation faults, missing artifacts/audit/verification/completion/replay/residual/acknowledgment, support assignment, and external-effect requests.",
        "output_assertions": ["two valid and seven invalid delivery traces", "two valid and nine invalid durable traces", "twenty-eight routes and seven reachable stages", "forty-two rejected lifecycle mutations", "no support-state or external-effect authority"],
        "claim_scope": "One finite authored versioned typed-job lifecycle plus two existing bounded synthetic suites only.",
        "negative_controls": "validator_owned_identity_sequence_authority_retry_cancellation_delivery_closure_mutations",
        "negative_control_cases": ["job, contract, plan, authority, permission, lease, scheduler, consumer, or event substitution", "approval, permission, lease, scheduler, or dispatch gap", "retry without idempotency or with widened authority", "unacknowledged cancellation or post-cancellation output", "missing output, artifact, audit, verification, completion, replay, residual owner, or consumer acknowledgment", "support assignment or external-effect authority leak"],
        "prohibited_inference": "Does not establish scheduler quality, worker/model capability, task success, output truth, verification soundness, idempotence/enforcement in fact, recovery, cancellation efficacy, receipt/replay truth, usefulness, causality, safety, deployment, reproduction, transfer, SOTA, AGI, ASI, or chapter-core support.",
        "contract_precision": "inherited",
        "semantic_review_state": "checked_structured_versioned_typed_job_execution_closure_not_task_success_truth_enforcement_deployed_or_support_authority",
    })
    required = list(value["required_artifacts"])
    for artifact in ARTIFACTS:
        if artifact not in required: required.append(artifact)
    value["required_artifacts"] = required
    value["summary"] = {"required_artifact_count": len(required), "unit_count": len(value["units"])}
    REGISTRY.write_text(json.dumps(value, indent=2) + "\n")
    print(f"Registered {SCRIPT}: {len(value['units'])} units, {len(required)} artifacts.")


if __name__ == "__main__": main()
