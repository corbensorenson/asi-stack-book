#!/usr/bin/env python3
"""Idempotently register the governed QCSA vertical reference gate."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
OVERRIDES = ROOT / "validation/unit_contract_overrides.json"
SCRIPT = "validate_qcsa_vertical_reference.py"
ARTIFACTS = [
    "scripts/build_qcsa_vertical_reference.py", "scripts/validate_qcsa_vertical_reference.py",
    "schemas/qcsa_vertical_reference_result.schema.json", "schemas/qcsa_vertical_reference_manifest.schema.json",
    "experiments/qcsa_vertical_reference/task.json",
    "experiments/qcsa_vertical_reference/results/vertical_result.json",
    "experiments/qcsa_vertical_reference/results/artifact_manifest.json",
    "docs/qcsa_governed_vertical_reference_report.md"
]


def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    unit = next((row for row in registry["units"] if row["script"] == SCRIPT and row.get("args", []) == []), None)
    if unit is None:
        order = len(registry["units"]) + 1
        unit = {"id": f"qcsa_vertical_reference:{order}", "order": order, "script": SCRIPT, "args": []}
        registry["units"].append(unit)
    unit.update({
        "execution_tier": "deep", "validation_class": "behavioral_fixture",
        "input_contract": "One public-safe QCSA task crossing intent, semantic IR, SOID/SVA resolution, typed evidence, question compilation, context materialization, route planning, separate authority, a real temporary filesystem effect, independent byte observation, receipt/artifact graph, same-identity migration, and rollback, with ten adversarial paths and eight residuals.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Validate thirteen ordered stages, identity/address/evidence/authority separation, exact effect observation, complete receipts, same-SOID migration, descendant inventory, byte-exact rollback with no hidden path, zero network/model/external-human accounting, ten fail-closed adversarial paths, open residuals, content-addressed descendants, and two byte-identical replays; reject fifteen mutations.",
        "output_assertions": ["thirteen ordered stages", "stable SOID and plural address", "truth/address separation", "separate authority decision", "one real temporary effect", "independent byte observation", "complete receipt graph", "same-identity migration", "byte-exact rollback", "ten rejected adversarial paths", "eight open residuals", "fifteen rejecting mutations"],
        "claim_scope": "Deterministic composition and effect/rollback behavior of one exact public-safe temporary-filesystem reference trace.",
        "negative_controls": "validator_owned_and_result_bound",
        "negative_control_cases": ["stage erasure", "stage order drift", "truth laundering", "authority laundering", "unobserved effect", "missing receipt", "migration retarget", "rollback mismatch", "hidden effect", "attack erasure", "attack release", "network use", "residual erasure", "support promotion", "descendant mutation"],
        "prohibited_inference": "One bounded vertical trace does not establish natural-task quality, learned routing, production authority, effect-complete rollback in open systems, distributed migration, storage erasure, safety, privacy, security, external independence, AGI, ASI, or chapter-core support promotion.",
        "contract_precision": "exact_high_impact", "semantic_review_state": "internal_behavioral_audit_not_independent"
    })
    for artifact in ARTIFACTS:
        if artifact not in registry["required_artifacts"]: registry["required_artifacts"].append(artifact)
    registry["summary"] = {"required_artifact_count": len(registry["required_artifacts"]), "unit_count": len(registry["units"])}
    REGISTRY.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    overrides = json.loads(OVERRIDES.read_text(encoding="utf-8"))
    fields = ["input_contract", "input_artifacts", "output_contract", "output_assertions", "claim_scope", "negative_controls", "negative_control_cases", "prohibited_inference", "contract_precision", "semantic_review_state"]
    record = {"script": SCRIPT, "args": [], **{field: unit[field] for field in fields}}
    override = next((row for row in overrides["contracts"] if row["script"] == SCRIPT and row.get("args", []) == []), None)
    if override is None: overrides["contracts"].append(record)
    else: override.clear(); override.update(record)
    OVERRIDES.write_text(json.dumps(overrides, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"registered {SCRIPT}: {registry['summary']['unit_count']} units, {registry['summary']['required_artifact_count']} artifacts")


if __name__ == "__main__":
    main()
