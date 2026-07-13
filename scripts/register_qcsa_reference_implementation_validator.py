#!/usr/bin/env python3
"""Idempotently register the twelve-lane QCSA implementation gate."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
OVERRIDES = ROOT / "validation/unit_contract_overrides.json"
SCRIPT = "validate_qcsa_reference_implementation.py"
ARTIFACTS = [
    "scripts/validate_qcsa_reference_implementation.py",
    "scripts/build_qcsa_reference_implementation.py",
    "scripts/qcsa_independent_evaluator.py",
    "experiments/qcsa_reference/package_manifest.json",
    "experiments/qcsa_reference/results/implementation_result.json",
] + [f"experiments/qcsa_reference/qcsa_ref/{name}.py" for name in [
    "__init__", "canonical", "identity", "evidence_graph", "atlas", "certificate", "questions", "routes",
    "migration", "adversarial", "grounding", "round_trip", "ledger", "manifest",
]] + [f"experiments/qcsa_reference/artifacts/QI-{index:02d}.json" for index in range(1, 13)]


def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    matches = [row for row in registry["units"] if row["script"] == SCRIPT and row.get("args", []) == []]
    if matches:
        unit = matches[0]
    else:
        order = len(registry["units"]) + 1
        unit = {"id": f"validate_qcsa_reference_implementation:{order}", "order": order, "script": SCRIPT, "args": []}
        registry["units"].append(unit)
    unit.update({
        "execution_tier": "deep",
        "validation_class": "behavioral_fixture",
        "input_contract": "The frozen standard-library QCSA package plus twelve generated lane artifacts, one behavioral negative control per lane, the independent structural evaluator, resource ledger, and descendant manifest before held-out access.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Rebuild twice byte-identically; validate every envelope, frozen lane field contract, identity/evidence/address/authority boundary, migration/rollback inventory, adversarial and grounding residual, independent-evaluator disagreement, governance ledger, and content-addressed descendant; reject fifteen semantic mutations.",
        "output_assertions": ["twelve deterministic lane artifacts", "eight identity kinds", "typed evidence contradiction", "candidate versus authoritative atlas", "separate authority and receipts", "migration rollback inventory", "nine adversarial controls", "bounded grounding residuals", "independent evaluator disagreement", "governance ledger", "descendant replay", "twelve lane controls", "fifteen rejecting mutations", "held-out outcomes unopened"],
        "claim_scope": "Deterministic local implementation behavior for the exact bounded QCSA fixtures and file-backed artifact bundle.",
        "negative_controls": "validator_owned_and_result_bound",
        "negative_control_cases": ["digest tampering", "object-kind collapse", "dangling evidence", "candidate epoch authority", "signature laundering", "question drift", "missing receipt", "silent retarget", "adversarial miss", "grounding residual erasure", "evaluator self-confirmation", "negative ledger", "descendant mutation", "failed lane control", "opened outcomes"],
        "prohibited_inference": "The deterministic fixture implementation does not establish semantic correctness, learned routing quality, matched advantage, safety, security, privacy, universal grounding, complete unlearning, production transfer, external independence, AGI, ASI, or chapter-core support promotion.",
        "contract_precision": "exact_high_impact",
        "semantic_review_state": "internal_behavioral_audit_not_independent",
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
