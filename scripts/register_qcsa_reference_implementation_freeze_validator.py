#!/usr/bin/env python3
"""Idempotently register the pre-outcome QCSA implementation freeze gate."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
OVERRIDES = ROOT / "validation/unit_contract_overrides.json"
SCRIPT = "validate_qcsa_reference_implementation_freeze.py"
ARTIFACTS = [
    "scripts/validate_qcsa_reference_implementation_freeze.py",
    "docs/qcsa_reference_architecture_decision.md",
    "roadmap_records/qcsa_reference_implementation_freeze.json",
    "schemas/qcsa_reference_freeze.schema.json",
    "experiments/qcsa_reference/package_manifest.json",
    "schemas/qcsa_reference_package_manifest.schema.json",
    "experiments/qcsa_reference/budgets.json",
    "schemas/qcsa_reference_budget.schema.json",
    "experiments/qcsa_reference/test_plan.json",
    "schemas/qcsa_reference_test_plan.schema.json",
    "schemas/qcsa_reference_artifact.schema.json",
    "schemas/qcsa_reference_fixture_bundle.schema.json",
    "experiments/qcsa_reference/fixtures/envelope_examples.valid.json",
    "experiments/qcsa_reference/fixtures/envelope_examples.expected_invalid.json",
    "docs/post_v2_2_implementation_completion_roadmap.md",
    "roadmap_records/post_v2_2_implementation_completion_status.json",
]


def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    matches = [row for row in registry["units"] if row["script"] == SCRIPT and row.get("args", []) == []]
    if matches:
        unit = matches[0]
    else:
        order = len(registry["units"]) + 1
        unit = {"id": f"validate_qcsa_reference_implementation_freeze:{order}", "order": order, "script": SCRIPT, "args": []}
        registry["units"].append(unit)
    unit.update({
        "execution_tier": "deep",
        "validation_class": "proof_or_evidence_gate",
        "input_contract": "A pre-outcome QCSA architecture decision, package manifest, common artifact envelope, representative valid/invalid fixtures, zero-service budget, six-family 180-case protocol with 60 held out, matched baselines/ablations, separated evaluator, and twelve frozen unimplemented lanes.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Reject missing lanes, label-bearing IDs, opened outcomes, budget/split drift, evaluator self-confirmation, erased authority separation, premature implementation claims, weakened migration contracts, missing negative fixtures, or support promotion.",
        "output_assertions": ["twelve frozen unimplemented lanes", "six workload families", "72/48/60 split", "seven matched baselines", "five ablations", "three seeds", "zero network and service spend", "independent evaluator boundary", "ten rejecting mutations", "outcomes unopened"],
        "claim_scope": "Pre-outcome implementation and evaluation contract freeze for the bounded QCSA reference package.",
        "negative_controls": "validator_owned",
        "negative_control_cases": ["missing lane", "label leakage", "outcomes opened", "held-out budget drift", "evaluator self-confirmation", "authority adapter erased", "premature implementation", "migration rollback field erased", "negative fixtures erased", "support promotion"],
        "prohibited_inference": "A frozen plan, schema-valid envelope, or rejecting mutation does not establish QCSA implementation, semantic correctness, usefulness, efficiency, safety, privacy, migration success, production transfer, external independence, AGI, ASI, or chapter-core support movement.",
        "contract_precision": "exact_high_impact",
        "semantic_review_state": "internal_contract_audit_not_independent",
    })
    for artifact in ARTIFACTS:
        if artifact not in registry["required_artifacts"]:
            registry["required_artifacts"].append(artifact)
    registry["summary"] = {"required_artifact_count": len(registry["required_artifacts"]), "unit_count": len(registry["units"])}
    REGISTRY.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    overrides = json.loads(OVERRIDES.read_text(encoding="utf-8"))
    fields = ["input_contract", "input_artifacts", "output_contract", "output_assertions", "claim_scope", "negative_controls", "negative_control_cases", "prohibited_inference", "contract_precision", "semantic_review_state"]
    override = next((row for row in overrides["contracts"] if row["script"] == SCRIPT and row.get("args", []) == []), None)
    record = {"script": SCRIPT, "args": [], **{field: unit[field] for field in fields}}
    if override is None:
        overrides["contracts"].append(record)
    else:
        override.clear()
        override.update(record)
    OVERRIDES.write_text(json.dumps(overrides, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"registered {SCRIPT}: {registry['summary']['unit_count']} units, {registry['summary']['required_artifact_count']} artifacts")


if __name__ == "__main__":
    main()
