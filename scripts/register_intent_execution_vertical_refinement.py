#!/usr/bin/env python3
"""Register the executed Intent-to-Execution vertical refinement."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_intent_execution_vertical_refinement.py"
ARTIFACTS = [
    "scripts/validate_intent_execution_vertical_refinement.py",
    "schemas/intent_execution_vertical_refinement.schema.json",
    "experiments/intent_execution_vertical_refinement/results/2026-07-15-local.json",
    "docs/intent_execution_vertical_refinement.md",
    "evidence_quality/model_adequacy_dossiers/intent-execution-vertical-refinement.md",
    "lean/AsiStackProofs/IntentExecutionRefinement.lean",
    "experiments/governed_repository_change_slice/results/2026-07-10-local.json",
    "schemas/governed_repository_change_result.schema.json",
    "experiments/intent_execution_handoff/results/2026-07-02-local.json",
]


def main() -> None:
    value = json.loads(REGISTRY.read_text(encoding="utf-8"))
    value["units"] = [row for row in value["units"] if row.get("script") != SCRIPT]
    order = len(value["units"]) + 1
    value["units"].append({
        "id": f"validate_intent_execution_vertical_refinement:{order}",
        "order": order,
        "script": SCRIPT,
        "args": [],
        "execution_tier": "deep",
        "validation_class": "proof_or_evidence_gate",
        "input_contract": "The reachable Lean vertical model, complete schema-validated executed governed repository-change result, prior synthetic handoff probe, result schema, receipt, and adequacy dossier.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Reject missing or reordered intent/authority/plan/context/route lineage, approval or dispatch bypass, unobserved effects, artifact or verifier mismatch, unsafe release, incomplete rollback/quarantine/residual custody, source drift, and support promotion.",
        "output_assertions": ["nine executed scenarios", "eighty-nine governed events", "three releases", "three pre-effect refusals", "two exact-rollback refusals", "one failed-rollback quarantine", "six material and independently observed effects", "two residual scenarios", "thirty rejected concrete source mutations", "no support-state effect"],
        "claim_scope": "One fixed executed local repository-change task and its exact versioned result schema only.",
        "negative_controls": "validator_owned_concrete_source_field_mutations_and_digest_binding",
        "negative_control_cases": ["lineage event deletion or reordering", "authority and approval bypass", "untrusted instruction not quarantined", "unauthorized artifact path or digest mismatch", "correlated verifier or missing observation", "rollback or residual laundering", "unsafe release", "support promotion"],
        "prohibited_inference": "The finite fixed-task refinement does not establish natural-language intent correctness, general semantic equivalence, authentic deployed authority, complete effects, natural-workload usefulness, reproduction, transfer, safety, SOTA, AGI, ASI, or chapter-core support.",
        "contract_precision": "inherited",
        "semantic_review_state": "checked_single_executed_schema_vertical_refinement_not_general_external_or_deployed",
    })
    required = list(value["required_artifacts"])
    for artifact in ARTIFACTS:
        if artifact not in required:
            required.append(artifact)
    value["required_artifacts"] = required
    value["summary"] = {"required_artifact_count": len(required), "unit_count": len(value["units"])}
    REGISTRY.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    print(f"Registered {SCRIPT}: {len(value['units'])} units, {len(required)} artifacts.")


if __name__ == "__main__":
    main()
