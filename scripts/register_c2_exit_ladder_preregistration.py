#!/usr/bin/env python3
"""Register the C2-EL preregistration validator."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_c2_exit_ladder_preregistration.py"
ARTIFACTS = [
    "experiments/c2_exit_ladder/preregistration.json",
    "schemas/c2_exit_ladder_preregistration.schema.json",
    "scripts/validate_c2_exit_ladder_preregistration.py",
]


def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    registry["units"] = [row for row in registry["units"] if row.get("script") != SCRIPT]
    used = {row["order"] for row in registry["units"]}
    order = next(index for index in range(1, len(registry["units"]) + 2) if index not in used)
    registry["units"].append({
        "id": f"validate_c2_exit_ladder_preregistration:{order}",
        "order": order,
        "script": SCRIPT,
        "args": [],
        "execution_tier": "pr",
        "validation_class": "proof_or_evidence_gate",
        "input_contract": "The first post-freeze eligible natural claim-state proposal, three matched routes, one natural path, three claim-state faults, twelve outcomes, fixed dispositions, and closed proposal/protected/support/release state.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Reject outcome-aware proposal selection, route/path/outcome loss, replacement after admission, identity or inference laundering, protected-content opening, and support or release movement before execution.",
        "output_assertions": [
            "first eligible post-freeze claim-state proposal only",
            "three matched route contracts",
            "natural path separated from identity inference and projection faults",
            "success negative and inconclusive dispositions frozen",
            "ten mutations reject",
            "proposal protected support and release states closed",
        ],
        "claim_scope": "Prospective selection and analysis contract for one future public-safe ASI Stack claim-state proposal only.",
        "negative_controls": "proposal_route_path_outcome_replacement_inference_protection_and_support_mutations",
        "negative_control_cases": [
            "proposal preadmitted", "proposal identity preopened", "protected content opened",
            "route removed", "route relabeled", "fault path removed", "outcome removed",
            "replacement allowed", "inference widened", "support promoted",
        ],
        "prohibited_inference": "Preregistration is not execution or evidence and cannot establish transition correctness, evidence quality, editorial quality, human effort, production reliability, safety, transfer, SOTA, AGI, ASI, or chapter-core support.",
        "contract_precision": "exact",
        "semantic_review_state": "prospective_single_natural_claim_state_proposal_with_explicit_injected_controls",
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
