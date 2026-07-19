#!/usr/bin/env python3
"""Register the post-commit evidence-custody release gate."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_evidence_git_custody.py"
ARTIFACTS = [
    "scripts/validate_evidence_git_custody.py",
    "scripts/register_evidence_git_custody.py",
]


def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    registry["units"] = [row for row in registry["units"] if row.get("script") != SCRIPT]
    order = len(registry["units"]) + 1
    registry["units"].append({
        "id": f"{SCRIPT}:{order}",
        "order": order,
        "script": SCRIPT,
        "args": [],
        "execution_tier": "release",
        "validation_class": "proof_or_evidence_gate",
        "input_contract": "Git porcelain state for evidence_transitions, evidence_quality, and release_records at the exact tested commit.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Reject release or attestation while any claim-bearing evidence transition, evidence-quality record, or release record is modified, staged, or untracked.",
        "output_assertions": [
            "all three protected roots are clean relative to HEAD",
            "modified evidence rejects",
            "staged evidence rejects",
            "untracked release records reject",
        ],
        "claim_scope": "Repository durability and release-gate custody only; a clean commit does not validate evidence truth.",
        "negative_controls": "validator_owned_modified_staged_and_untracked_porcelain_rows",
        "negative_control_cases": ["modified evidence", "staged transition", "untracked release record"],
        "prohibited_inference": "Committed custody does not establish result validity, independence, reproduction, transfer, safety, publication merit, or chapter-core support.",
        "contract_precision": "exact",
        "semantic_review_state": "checked_post_commit_evidence_durability_gate",
    })
    for artifact in ARTIFACTS:
        if artifact not in registry["required_artifacts"]:
            registry["required_artifacts"].append(artifact)
    registry["summary"] = {
        "required_artifact_count": len(registry["required_artifacts"]),
        "unit_count": len(registry["units"]),
    }
    REGISTRY.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
    print(f"Registered {SCRIPT}: release tier order {order}.")


if __name__ == "__main__":
    main()
