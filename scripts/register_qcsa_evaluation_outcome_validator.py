#!/usr/bin/env python3
"""Idempotently register the exact QCSA held-out outcome gate."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
OVERRIDES = ROOT / "validation/unit_contract_overrides.json"
SCRIPT = "validate_qcsa_evaluation.py"
ARTIFACTS = [
    "scripts/validate_qcsa_evaluation.py", "scripts/run_qcsa_evaluation_predictions.py",
    "scripts/qcsa_evaluation_observer.py", "schemas/qcsa_evaluation_predictions.schema.json",
    "schemas/qcsa_evaluation_results.schema.json", "schemas/qcsa_evaluation_dispositions.schema.json",
    "roadmap_records/qcsa_evaluation_execution_authorization.json",
    "experiments/qcsa_reference/results/evaluation_predictions.json",
    "experiments/qcsa_reference/results/evaluation_results.json",
    "claim_decisions/qcsa_reference_evaluation_dispositions.json",
    "docs/qcsa_reference_evaluation_report.md"
]


def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    unit = next((row for row in registry["units"] if row["script"] == SCRIPT and row.get("args", []) == []), None)
    if unit is None:
        order = len(registry["units"]) + 1
        unit = {"id": f"qcsa_evaluation:{order}", "order": order, "script": SCRIPT, "args": []}
        registry["units"].append(unit)
    unit.update({
        "execution_tier": "deep", "validation_class": "proof_or_evidence_gate",
        "input_contract": "The attested QCSA setup authorization, exact 2340 held-out predictions over 60 cases, 13 systems and three seeds, separately implemented observer output, six-family metrics and Pareto frontiers, 10000-resample paired task intervals, bounded gate decisions, ten non-core dispositions, nine chapter-core no-change decisions, and explicit report limitations.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Validate schemas, authorization/build/deploy bindings, exact seed/system/case coverage and record digests, runner label isolation, observer implementation separation, descendant digests, aggregate/family/seed metrics, ablation failures, Pareto/bootstrap decisions, failed advantage/resource gates, disposition counts, core no-change boundary, and two byte-identical end-to-end replays; reject fifteen outcome mutations.",
        "output_assertions": ["2340 exact predictions", "60 held out", "13 systems", "three seeds", "label-isolated runner", "separate observer", "10000 paired resamples", "six-family Pareto frontiers", "failed advantage gate", "failed resource gate", "bounded authority/migration/calibration gates", "ten non-core dispositions", "nine core no-change decisions", "fifteen rejecting mutations"],
        "claim_scope": "Deterministic behavior, comparisons, costs, ablations, and disposition rules for the exact internally authored synthetic QCSA evaluation.",
        "negative_controls": "validator_owned_and_result_bound",
        "negative_control_cases": ["missing system", "missing seed", "missing case", "record digest tamper", "atomic erasure", "bootstrap drift", "blended score", "unsafe release hidden", "mechanism regression erased", "evaluator disagreement hidden", "migration failure hidden", "advantage promotion", "core promotion", "runner label leak", "observer self-confirmation"],
        "prohibited_inference": "This exact synthetic result does not establish a matched-resource advantage, natural-task quality, learned routing, universal semantic preservation, safety, security, privacy, external independence, production latency or transfer, AGI, ASI, or any chapter-core support promotion.",
        "contract_precision": "exact_high_impact", "semantic_review_state": "internal_behavioral_audit_not_independent"
    })
    for artifact in ARTIFACTS:
        if artifact not in registry["required_artifacts"]:
            registry["required_artifacts"].append(artifact)
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
