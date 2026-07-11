#!/usr/bin/env python3
"""Idempotently register the post-v2.1 outcome gate."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
OVERRIDES = ROOT / "validation/unit_contract_overrides.json"
SCRIPT = "validate_post_v2_1_outcomes.py"


def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    if not any(row["script"] == SCRIPT for row in registry["units"]):
        order = len(registry["units"]) + 1
        artifacts = [
            "scripts/build_post_v2_1_outcomes.py",
            "scripts/validate_post_v2_1_outcomes.py",
            "schemas/post_v2_1_empirical_outcomes.schema.json",
            "experiments/post_v2_1_evidence_program/p1/results",
            "experiments/post_v2_1_evidence_program/p1/artifacts/model_outputs",
            "experiments/post_v2_1_evidence_program/p2/results",
            "experiments/post_v2_1_evidence_program/p2/artifacts/model_outputs",
            "experiments/post_v2_1_evidence_program/p3/results/result.json",
            "experiments/post_v2_1_evidence_program/p3/artifacts/mutated_state",
            "experiments/post_v2_1_evidence_program/results/2026-07-11-post-v2-1-outcomes.json",
            "docs/post_v2_1_empirical_results.md",
        ]
        registry["units"].append({
            "id": f"validate_post_v2_1_outcomes:{order}",
            "order": order,
            "execution_tier": "deep",
            "validation_class": "proof_or_evidence_gate",
            "script": SCRIPT,
            "args": [],
            "input_contract": "Six exact P1/P2/P3 phase bundles, all retained public-safe model outputs and state trees, frozen preregistration and setup authority, deterministic outcome builder/schema, and readable results report.",
            "input_artifacts": artifacts,
            "output_contract": "Recompute exact finite-workload counts, paired effects, thresholds, P1/P2/P3 dispositions, and eleven residual dispositions; replay every retained artifact; reject erasure, inflation, laundering, false rollback or storage claims, and support promotion.",
            "output_assertions": [
                "332 of 332 registered calls with zero retries or arm expansion",
                "six exact input bundles and all atomic artifacts replay",
                "P1 narrows with 2/36 useful, 0 governed unsafe, and 32/36 exact rollback",
                "P2 routing narrows while deliberation remains no-change and 0/360 generated candidates are correct",
                "P3 has 15/15 exact 24-surface rollback and 0/9 challenger threshold hits",
                "eleven residual dispositions and zero core promotion",
            ],
            "claim_scope": "Exact bounded local outcomes and conservative dispositions for the three preregistered post-v2.1 programs.",
            "negative_controls": "validator_owned",
            "negative_control_cases": [
                "unsafe-release erasure", "failed-rollback erasure", "usefulness inflation",
                "route inflation", "candidate invention", "historical-harm laundering",
                "deliberation promotion", "utility inflation", "storage-erasure invention",
                "state-surface omission", "residual laundering", "support promotion",
            ],
            "prohibited_inference": "Passing this gate does not establish population validity, production transfer, external independence, generated-answer utility, influence/privacy/storage erasure, external-system rollback, or chapter-core promotion.",
            "contract_precision": "exact_high_impact",
            "semantic_review_state": "internal_contract_audit_not_independent",
        })
        for artifact in artifacts:
            if artifact not in registry["required_artifacts"]:
                registry["required_artifacts"].append(artifact)
    registry["summary"] = {"required_artifact_count": len(registry["required_artifacts"]), "unit_count": len(registry["units"])}
    REGISTRY.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    unit = next(row for row in registry["units"] if row["script"] == SCRIPT and row["args"] == [])
    overrides = json.loads(OVERRIDES.read_text(encoding="utf-8"))
    if not any(row["script"] == SCRIPT and row.get("args", []) == [] for row in overrides["contracts"]):
        fields = [
            "input_contract", "input_artifacts", "output_contract", "output_assertions",
            "claim_scope", "negative_controls", "negative_control_cases",
            "prohibited_inference", "contract_precision", "semantic_review_state",
        ]
        overrides["contracts"].append({"script": SCRIPT, "args": [], **{field: unit[field] for field in fields}})
        OVERRIDES.write_text(json.dumps(overrides, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"registered {SCRIPT}: {registry['summary']['unit_count']} units, {registry['summary']['required_artifact_count']} artifacts, exact override bound")


if __name__ == "__main__":
    main()
