#!/usr/bin/env python3
"""Register the reachable stack-boundary consumer in the validation authority."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_stack_boundary_effect_consumer.py"
ARTIFACTS = [
    "scripts/validate_stack_boundary_effect_consumer.py",
    "schemas/stack_boundary_effect_consumer.schema.json",
    "experiments/stack_boundary_effect/results/2026-07-15-local.json",
    "docs/stack_boundary_effect_consumer.md",
    "evidence_quality/model_adequacy_dossiers/stack-boundary-effect.md",
    "lean/AsiStackProofs/StackBoundaries.lean",
    "experiments/runtime_adapter_effect_probe/results/2026-07-02-local.json",
    "experiments/authority_revocation_trace/results/2026-07-03-local.json",
    "experiments/authority_transitions/fixtures/invalid_allow_over_ceiling.json",
    "experiments/authority_transitions/fixtures/invalid_missing_effect_receipt.json",
    "experiments/authority_transitions/fixtures/invalid_permission_class_collapse.json",
    "experiments/authority_transitions/fixtures/valid_allow_scoped_write.json",
    "experiments/authority_transitions/fixtures/valid_deny_over_ceiling.json",
    "experiments/authority_transitions/fixtures/valid_escalate_approval_required.json",
]


def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    registry["units"] = [row for row in registry["units"] if row.get("script") != SCRIPT]
    order = len(registry["units"]) + 1
    registry["units"].append({
        "id": f"validate_stack_boundary_effect_consumer:{order}",
        "order": order,
        "script": SCRIPT,
        "args": [],
        "execution_tier": "deep",
        "validation_class": "proof_or_evidence_gate",
        "input_contract": "The reachable Lean boundary model, eighteen-case generated layer-contract suite, six tracked authority fixtures, one local effect probe, five-entry revocation trace, schema-bound result, receipt, and model-adequacy dossier.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Reject layer-contract route drift, authority widening, inactive or stale grants, missing target-owner or receipt custody, missing dispatch, observation gaps, false rollback, post-revocation effect, stale source/model digests, and support promotion.",
        "output_assertions": [
            "eighteen matched layer-contract routes",
            "six authority fixtures with three accepted and three rejected",
            "three accepted runtime paths and ten accepted events",
            "one material effect one independent observation and one exact rollback",
            "two no-mutation denials and five revocation entries",
            "twelve rejected semantic mutations",
            "no support-state effect",
        ],
        "claim_scope": "The exact finite reachable boundary model, generated admission routes, synthetic authority fixtures, and one contained local effect path only.",
        "negative_controls": "validator_owned_source_digest_bound_semantic_mutations",
        "negative_control_cases": [
            "zero request or over-ceiling grant",
            "missing target-owner approval or authorization receipt",
            "stale epoch or missing dispatch receipt",
            "effect without custody",
            "missing independent observation",
            "false or receipt-free rollback",
            "post-revocation dispatch and effect",
            "support promotion laundering",
        ],
        "prohibited_inference": "Synthetic fixtures and one local temp-file effect do not establish authentic or deployed authority, complete effect discovery, distributed behavior, security, natural-workload usefulness, reproduction, transfer, safety, or chapter-core support.",
        "contract_precision": "inherited",
        "semantic_review_state": "independently_encoded_source_anchored_finite_consumer_not_deployed",
    })
    required = list(registry["required_artifacts"])
    for artifact in ARTIFACTS:
        if artifact not in required:
            required.append(artifact)
    registry["required_artifacts"] = required
    registry["summary"] = {
        "required_artifact_count": len(required),
        "unit_count": len(registry["units"]),
    }
    REGISTRY.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
    print(f"Registered {SCRIPT}: {len(registry['units'])} units, {len(required)} artifacts.")


if __name__ == "__main__":
    main()
