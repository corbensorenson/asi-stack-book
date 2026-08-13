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
    "schemas/c1_exit_ladder_preregistration.schema.json",
    "scripts/validate_c1_exit_ladder_preregistration.py",
]


def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    registry["units"] = [row for row in registry["units"] if row.get("script") != SCRIPT]
    order = len(registry["units"]) + 1
    registry["units"].append({
        "id": f"validate_c1_exit_ladder_preregistration:{order}",
        "order": order,
        "script": SCRIPT,
        "args": [],
        "execution_tier": "pr",
        "validation_class": "proof_or_evidence_gate",
        "input_contract": "The first post-freeze eligible natural maintenance defect, three matched routes, one natural happy path, three explicit injected controls, twelve joint outcomes, fixed dispositions, and closed task/protected/support/release state.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Reject outcome-aware task selection, route or outcome loss, replacement after admission, support laundering, protected-content opening, or inference beyond one local prospective case.",
        "output_assertions": [
            "first eligible post-freeze task only",
            "three matched route contracts",
            "natural happy path separated from injected faults",
            "success negative and inconclusive dispositions frozen",
            "eight mutations reject",
            "task protected support and release states closed",
        ],
        "claim_scope": "Prospective selection and analysis contract for one future public-safe ASI Stack maintenance defect only.",
        "negative_controls": "task_route_outcome_replacement_inference_protection_and_support_mutations",
        "negative_control_cases": [
            "task preadmitted", "protected content opened", "route removed",
            "baseline relabeled", "outcome removed", "replacement allowed",
            "inference widened", "support promoted",
        ],
        "prohibited_inference": "Preregistration is not execution or evidence and cannot establish utility, human effort, production reliability, safety, transfer, SOTA, AGI, ASI, or chapter-core support.",
        "contract_precision": "exact",
        "semantic_review_state": "prospective_single_natural_task_with_explicit_injected_controls",
    })
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
