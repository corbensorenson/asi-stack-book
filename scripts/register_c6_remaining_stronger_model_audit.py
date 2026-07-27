#!/usr/bin/env python3
"""Register the C6 remaining stronger-model audit validator."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_c6_remaining_stronger_model_audit.py"
ARTIFACTS = [
    "proofs/c6_remaining_stronger_model_audit.json",
    "docs/c6_remaining_stronger_model_audit_2026_07_26.md",
    "schemas/c6_remaining_stronger_model_audit.schema.json",
    "scripts/build_c6_remaining_stronger_model_audit.py",
    "scripts/validate_c6_remaining_stronger_model_audit.py",
    "scripts/register_c6_remaining_stronger_model_audit.py",
    "proofs/proof_semantic_depth_overlay.json",
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
            "input_contract": "All current rewrite_with_stronger_model declarations from the digest-bound semantic overlay, with exact Lean dependency, theorem-consumer, executable-consumer, owner, level, and inference metadata.",
            "input_artifacts": ARTIFACTS,
            "output_contract": "Terminally triage every remaining action without theorem-count incentives: retire summary mirrors, preserve independent evidence at its own scope, and authorize only one smallest inverse route property.",
            "output_assertions": [
                "54 exact actions",
                "53 retire without replacement",
                "one inverse route rewrite",
                "43 Theseus mirrors",
                "zero Lean dependencies",
                "zero theorem consumers",
                "historical results immutable",
                "no support or release movement",
                "twelve mutations reject",
            ],
            "claim_scope": "Proof-estate triage only; physical execution remains pending and creates no empirical evidence.",
            "negative_controls": "validator_owned_coverage_identity_dependency_consumer_replacement_support_release_inverse_theseus_digest_and_count_mutations",
            "negative_control_cases": [
                "drop action",
                "duplicate identity",
                "hide dependency",
                "hide consumer",
                "replacement bloat",
                "support promotion",
                "packet promotion",
                "release effect",
                "wrong inverse",
                "wrong Theseus action",
                "overlay digest drift",
                "count drift",
            ],
            "prohibited_inference": "The audit does not retire proofs, validate implementations, establish empirical evidence, or move support, release, SOTA, AGI, or ASI claims.",
            "contract_precision": "exact",
            "semantic_review_state": "all_remaining_stronger_model_actions_dependency_consumer_and_scope_reviewed",
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
