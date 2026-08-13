#!/usr/bin/env python3
"""Register the C1-EL preregistration validator."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_c1_exit_ladder_preregistration.py"
ARTIFACTS = [
    "experiments/c1_exit_ladder/preregistration.json",
    "experiments/c1_exit_ladder/admission.json",
    "experiments/c1_exit_ladder/design.json",
    "experiments/c1_exit_ladder/results/2026-08-13-instrument-failure.json",
    "schemas/c1_exit_ladder_preregistration.schema.json",
    "schemas/c1_exit_ladder_admission.schema.json",
    "schemas/c1_exit_ladder_instrument_failure.schema.json",
    "schemas/c1_exit_ladder_result.schema.json",
    "scripts/run_c1_exit_ladder.py",
    "scripts/validate_c1_exit_ladder_preregistration.py",
]


def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    registry["units"] = [row for row in registry["units"] if row.get("script") != SCRIPT]
    used = {row["order"] for row in registry["units"]}
    order = next(index for index in range(1, len(registry["units"]) + 2) if index not in used)
    registry["units"].append({
        "id": f"validate_c1_exit_ladder_preregistration:{order}",
        "order": order,
        "script": SCRIPT,
        "args": [],
        "execution_tier": "pr",
        "validation_class": "proof_or_evidence_gate",
        "input_contract": "The prospectively frozen protocol plus the first post-freeze eligible natural maintenance defect admitted before solution inspection, three matched routes, one natural happy path, three explicit injected controls, twelve joint outcomes, fixed dispositions, and closed protected/support/release state.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Reject outcome-aware task selection, route or outcome loss, replacement after admission or terminal instrument failure, support laundering, protected-content opening, a fabricated result, or inference beyond the retained inconclusive attempt.",
        "output_assertions": [
            "first eligible post-freeze task only",
            "task admission precedes solution and route-outcome inspection",
            "three matched route contracts",
            "natural happy path separated from injected faults",
            "success negative and inconclusive dispositions frozen",
            "terminal instrument failure retained without rerun or result recovery",
            "fifteen mutations reject",
            "protected support and release states closed",
        ],
        "claim_scope": "Prospective selection and analysis contract for one future public-safe ASI Stack maintenance defect only.",
        "negative_controls": "task_route_outcome_replacement_inference_protection_and_support_mutations",
        "negative_control_cases": [
            "task preadmitted", "protected content opened", "route removed",
            "baseline relabeled", "outcome removed", "replacement allowed",
            "inference widened", "support promoted", "solution preopened",
            "route outcomes preopened", "task invented", "freeze source changed",
            "rerun allowed", "route outcome claimed", "failure promoted",
        ],
        "prohibited_inference": "Preregistration is not execution or evidence and cannot establish utility, human effort, production reliability, safety, transfer, SOTA, AGI, ASI, or chapter-core support.",
        "contract_precision": "exact",
        "semantic_review_state": "terminal_inconclusive_instrument_failure_no_replacement_or_support_effect",
    })
    registry["units"].sort(key=lambda row: row["order"])
    for artifact in ARTIFACTS:
        if artifact not in registry["required_artifacts"]:
            registry["required_artifacts"].append(artifact)
    registry["summary"] = {
        "required_artifact_count": len(registry["required_artifacts"]),
        "unit_count": len(registry["units"]),
    }
    REGISTRY.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
    print(f"Registered {SCRIPT}: {len(registry['units'])} units.")


if __name__ == "__main__":
    main()
