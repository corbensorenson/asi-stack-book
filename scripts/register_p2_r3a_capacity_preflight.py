#!/usr/bin/env python3
"""Register the P2-R3a capacity and Docker preflight validator."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_p2_r3a_capacity_preflight.py"
ARTIFACTS = [
    "experiments/p2_governed_repository_admission/infrastructure_materialization/attempts/2026-07-26-r3a-001/result.json",
    "schemas/p2_r3a_capacity_preflight.schema.json",
    "docs/p2_r3a_capacity_and_docker_preflight_2026_07_26.md",
    "scripts/run_p2_r3a_capacity_preflight.py",
    "scripts/validate_p2_r3a_capacity_preflight.py",
    "scripts/register_p2_r3a_capacity_preflight.py",
    "evidence_quality/p2_resource_ceiling.json",
    "experiments/p2_governed_repository_admission/corpus/replacement_queue.json",
]


def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    registry["units"] = [
        row for row in registry["units"] if row.get("script") != SCRIPT
    ]
    used = {row["order"] for row in registry["units"]}
    order = next(
        index for index in range(1, len(registry["units"]) + 2) if index not in used
    )
    registry["units"].append(
        {
            "id": f"{SCRIPT}:{order}",
            "order": order,
            "script": SCRIPT,
            "args": [],
            "execution_tier": "pr",
            "validation_class": "proof_or_evidence_gate",
            "input_contract": "Exact host-free-byte and Docker-daemon diagnostics bound to the frozen 30-candidate queue and 50 GiB resource floor before protected content opens.",
            "input_artifacts": ARTIFACTS,
            "output_contract": "Admit pool materialization only when host and daemon gates both pass; otherwise retain an immutable N0 receipt with no candidate, support, or release effect.",
            "output_assertions": [
                "30-candidate denominator retained",
                "50 GiB floor derived from frozen resource ceiling",
                "four exact command receipts digest-bound",
                "no image pull or dependency materialization",
                "no protected content or outcome opened",
                "N0 and no support/release movement",
                "ten mutations reject",
            ],
            "claim_scope": "Infrastructure entry competence only; the receipt neither materializes the pool nor tests governed repository admission.",
            "negative_controls": "validator_owned_floor_shortfall_entry_materialization_content_inference_support_command_queue_and_docker_knowledge_mutations",
            "negative_control_cases": [
                "floor pass forged",
                "shortfall forged",
                "entry pass forged",
                "materialization forged",
                "content opened",
                "N-level inflated",
                "support promoted",
                "command output edited",
                "queue shrank",
                "Docker knowledge forged",
            ],
            "prohibited_inference": "Capacity or daemon failure does not establish or refute model competence, governed admission, usefulness, safety, transfer, SOTA, AGI, or ASI.",
            "contract_precision": "exact",
            "semantic_review_state": "capacity_daemon_queue_custody_and_noninference_boundaries_reviewed",
        }
    )
    for artifact in ARTIFACTS:
        if artifact not in registry["required_artifacts"]:
            registry["required_artifacts"].append(artifact)
    registry["units"].sort(key=lambda row: row["order"])
    registry["summary"] = {
        "required_artifact_count": len(registry["required_artifacts"]),
        "unit_count": len(registry["units"]),
    }
    REGISTRY.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
    print(
        f"Registered {SCRIPT}: {registry['summary']['unit_count']} units, "
        f"{registry['summary']['required_artifact_count']} artifacts."
    )


if __name__ == "__main__":
    main()
