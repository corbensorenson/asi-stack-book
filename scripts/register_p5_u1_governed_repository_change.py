#!/usr/bin/env python3
"""Register the P5-U1 governed repository-change validator."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_p5_u1_governed_repository_change.py"
ARTIFACTS = [
    "experiments/p5_u1_governed_repository_change/design.json",
    "experiments/p5_u1_governed_repository_change/results/2026-08-13-local.json",
    "schemas/p5_u1_governed_repository_change_result.schema.json",
    "scripts/run_p5_u1_governed_repository_change.py",
    "scripts/validate_p5_u1_governed_repository_change.py",
    "docs/p5_effect_complete_reference_report.md",
]


def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    registry["units"] = [unit for unit in registry["units"] if unit.get("script") != SCRIPT]
    order = len(registry["units"]) + 1
    registry["units"].append(
        {
            "id": f"validate_p5_u1_governed_repository_change:{order}",
            "order": order,
            "script": SCRIPT,
            "args": [],
            "execution_tier": "deep",
            "validation_class": "behavioral_fixture",
            "input_contract": "A real Human Reader source-link defect, its pre-fix Git identity, three frozen execution routes, four lifecycle paths, local Git repositories and bare remotes, tracked result, schema, and bounded report.",
            "input_artifacts": ARTIFACTS,
            "output_contract": "Replay the 3x4 route/path matrix in a fresh workspace and reject route loss, authority laundering, false state checks, false compensation, prospective-task laundering, or support movement.",
            "output_assertions": [
                "twelve of twelve state-checkable route/path trials pass",
                "full governance blocks the out-of-scope mutation before effect",
                "full governance recovers the partial repository change",
                "full governance compensates the external Git effect while retaining history",
                "direct and record-only routes expose the expected unauthorized and residual effects",
                "seven record mutations reject",
                "retrospective task identity and no-promotion boundary remain explicit",
            ],
            "claim_scope": "The retrospective local replay of one naturally arising Human Reader source-link repair only.",
            "negative_controls": "fresh_replay_plus_route_authority_state_compensation_classification_and_support_mutations",
            "negative_control_cases": [
                "route loss",
                "route-label laundering",
                "false state-check pass",
                "unauthorized-effect laundering",
                "false compensation closure",
                "support-state laundering",
                "retrospective-to-prospective laundering",
            ],
            "prohibited_inference": "This outcome-aware replay is not a prospective, randomized, held-out, independent, human-operator, production, general-utility, safety, transfer, SOTA, AGI, or ASI result and changes no support or release state.",
            "contract_precision": "exact",
            "semantic_review_state": "retrospective_natural_defect_replay_with_real_local_git_effect_boundary",
        }
    )
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
    print(f"Registered {SCRIPT}: {len(registry['units'])} units.")


if __name__ == "__main__":
    main()
