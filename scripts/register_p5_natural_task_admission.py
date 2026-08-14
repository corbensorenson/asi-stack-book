#!/usr/bin/env python3
"""Register the P5 natural-task admission validator."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_p5_natural_task_admission.py"
ARTIFACTS = [
    "experiments/governed_operations_argument_exit/preregistration.json",
    "experiments/governed_operations_argument_exit/intake_custody.json",
    "schemas/p5_natural_task_candidate.schema.json",
    "schemas/p5_natural_task_admission.schema.json",
    "schemas/p5_natural_task_intake_custody.schema.json",
    "scripts/admit_p5_natural_task.py",
    "scripts/validate_p5_natural_task_admission.py",
    "scripts/register_p5_natural_task_admission.py",
    "schemas/post_v2_3_maintenance_transfer_and_publication_status.schema.json",
    "scripts/validate_post_v2_3_maintenance_transfer_and_publication_roadmap.py",
    "docs/post_v2_3_maintenance_transfer_and_publication_roadmap.md",
    "roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json",
    "docs/repository_map.md",
    "appendices/F_changelog.qmd",
]


def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    registry["units"] = [unit for unit in registry["units"] if unit.get("script") != SCRIPT]
    order = len(registry["units"]) + 1
    registry["units"].append(
        {
            "id": f"validate_p5_natural_task_admission:{order}",
            "order": order,
            "script": SCRIPT,
            "args": [],
            "execution_tier": "pr",
            "validation_class": "proof_or_evidence_gate",
            "input_contract": "The frozen five-family P5 natural-service population, empty canonical intake custody, one external public-safe candidate envelope, a clean content-addressed source snapshot, pre-outcome acceptance checks, and fixed five-arm/fault assignment authority.",
            "input_artifacts": ARTIFACTS,
            "output_contract": "Admit only independently necessary unsolved tasks before solution or outcome inspection; allocate exactly three development and eight heldout slots per family by frozen seed; redact heldout content; bind all arms to one task/fault; update custody atomically enough to fail closed on partial reconciliation; and require campaign requalification before execution.",
            "output_assertions": [
                "canonical task and outcome custody remains closed",
                "five families allocate to 15 development and 40 heldout slots",
                "heldout admission records expose digests but no task content",
                "development records preserve the frozen task and acceptance contract",
                "all five arms receive one deterministic fault and execution order",
                "eighteen admission mutations reject",
                "support and release effects remain none",
            ],
            "claim_scope": "Prospective task identity, allocation, redaction, and custody mechanics for the frozen P5 campaign only; no canonical task is admitted by this implementation packet.",
            "negative_controls": "validator_owned_naturality_chronology_safety_overlap_snapshot_digest_duplicate_redaction_and_outcome_mutations",
            "negative_control_cases": [
                "invented task",
                "already solved task",
                "solution investigated",
                "outcome inspected",
                "late acceptance contract",
                "private task",
                "human dependency",
                "uncontrolled public effect",
                "P2 overlap",
                "prior campaign exposure",
                "subjective preference dependency",
                "false necessity",
                "source commit drift",
                "source surface drift",
                "discovery evidence drift",
                "duplicate admission",
                "orphan admission receipt",
                "custody identity without admission receipt",
            ],
            "prohibited_inference": "An admission gate, authored allocation fixtures, or operator eligibility attestations do not establish that a task is natural, that any arm is useful or safe, that an outcome occurred, or that support, release, transfer, SOTA, AGI, or ASI is warranted.",
            "contract_precision": "exact",
            "semantic_review_state": "executable_prospective_admission_with_canonical_task_and_outcome_custody_closed",
        }
    )
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
