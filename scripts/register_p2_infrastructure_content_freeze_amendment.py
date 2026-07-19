#!/usr/bin/env python3
"""Register the P2 infrastructure/content freeze amendment validator."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_p2_infrastructure_content_freeze_amendment.py"
ARTIFACTS = [
    "evidence_quality/p2_infrastructure_content_freeze_amendment.json",
    "schemas/p2_infrastructure_content_freeze_amendment.schema.json",
    "docs/p2_infrastructure_materialization_and_content_freeze_amendment.md",
    "scripts/validate_p2_infrastructure_content_freeze_amendment.py",
    "scripts/register_p2_infrastructure_content_freeze_amendment.py",
    "evidence_quality/p2_slot1_rank4_task_opening.json",
    "evidence_quality/p2_slot1_rank5_image_preflight_diagnosis.json"
]


def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    registry["units"] = [row for row in registry["units"] if row.get("script") != SCRIPT]
    order = len(registry["units"]) + 1
    registry["units"].append({
        "id": f"{SCRIPT}:{order}", "order": order, "script": SCRIPT, "args": [],
        "execution_tier": "pr", "validation_class": "proof_or_evidence_gate",
        "input_contract": "Frozen 30-candidate metadata queue, immutable rank-4/rank-5 history, bounded pre-content infrastructure retries, exact protected-content boundary, current capacity receipt, and post-commit custody rule.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Permit bounded logged infrastructure retries before protected content, prohibit rank advancement on setup weather, and make no-rerun absolute at first protected-content exposure.",
        "output_assertions": ["three attempts per exact setup failure class", "whole-pool infrastructure gate before unopened ranks", "rank 4 remains irreversible", "rank 5 returns to setup-pending", "rank 6 remains closed", "pool capacity is not falsely claimed", "campaign evidence requires commit custody", "eight mutations reject"],
        "claim_scope": "P2 setup and content-exposure governance only; no natural-task outcome or empirical support follows.",
        "negative_controls": "validator_owned_retry_selection_rank_boundary_capacity_custody_and_support_mutations",
        "negative_control_cases": ["unbounded retry", "pull-speed selection", "rank burn", "post-content rerun", "rank-6 opening", "fake pool pass", "optional custody", "support promotion"],
        "prohibited_inference": "Does not establish P2 completion, task validity, model capability, governance benefit, safety, transfer, SOTA, release, AGI, ASI, or chapter-core support.",
        "contract_precision": "exact",
        "semantic_review_state": "checked_infrastructure_retry_content_irreversibility_capacity_and_commit_custody_boundary"
    })
    for artifact in ARTIFACTS:
        if artifact not in registry["required_artifacts"]:
            registry["required_artifacts"].append(artifact)
    registry["summary"] = {"required_artifact_count": len(registry["required_artifacts"]), "unit_count": len(registry["units"])}
    REGISTRY.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
    print(f"Registered {SCRIPT}: order {order}.")


if __name__ == "__main__":
    main()
