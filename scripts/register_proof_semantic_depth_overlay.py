#!/usr/bin/env python3
"""Register the current C6 proof semantic-depth overlay validator."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = "validate_proof_semantic_depth_overlay.py"
REGISTER = "scripts/register_proof_semantic_depth_overlay.py"
ARTIFACTS = [
    "scripts/build_proof_semantic_depth_overlay.py",
    "scripts/validate_proof_semantic_depth_overlay.py",
    "schemas/proof_semantic_depth_overlay.schema.json",
    "proofs/proof_semantic_depth_overlay.json",
    "docs/proof_semantic_depth_overlay.md",
    "proofs/proof_manifest.json",
    "proofs/proof_rationalization_registry.json",
    "proofs/semantic_cluster_audits",
    "lean/AsiStackProofs",
    "validation/registry.json",
    "book_structure.json",
]


def main() -> None:
    path = ROOT / "validation" / "registry.json"
    registry = json.loads(path.read_text(encoding="utf-8"))
    existing_order = next(
        (row["order"] for row in registry["units"] if row.get("script") == SCRIPT),
        None,
    )
    registry["units"] = [
        row for row in registry["units"] if row.get("script") != SCRIPT
    ]
    order = (
        existing_order
        if existing_order is not None
        else max(row["order"] for row in registry["units"]) + 1
    )
    registry["units"].append({
        "id": f"{SCRIPT}:{order}",
        "order": order,
        "script": SCRIPT,
        "args": [],
        "execution_tier": "pr",
        "validation_class": "proof_or_evidence_gate",
        "input_contract": (
            "Every theorem declaration in the live Lean estate, the frozen historical "
            "rationalization registry, all current proof targets and semantic-cluster "
            "audits, active chapter ownership, and registered validator/artifact bindings."
        ),
        "input_artifacts": ARTIFACTS + [REGISTER],
        "output_contract": (
            "Require exact live-theorem coverage with P0-P6 semantic kind, assumptions, "
            "active owners, consumers, witness or explicit absence, implementation binding, "
            "mutation evidence, maximum inference, and retain/rewrite/retire disposition; "
            "preserve the frozen 1,151-theorem/298-target baseline and reject eleven overclaim "
            "or custody mutations."
        ),
        "output_assertions": [
            "all live theorem declarations covered exactly once",
            "P0-P6 semantic kinds are separate from tactic-shape classes",
            "P2 requires a bounded witness",
            "P3-P6 require validator-and-artifact binding",
            "P6 requires a named empirical observation contract",
            "every theorem names mutation coverage and an active semantic owner",
            "rewrite/retire queue is nonempty",
            "frozen 1151-theorem and 298-target baseline preserved",
            "11 mutations reject",
            "no support-state effect",
        ],
        "claim_scope": (
            "Current formal-estate meaning, dependency, binding, and rationalization "
            "custody only."
        ),
        "negative_controls": (
            "validator_owned_eleven_coverage_owner_assumption_mutation_witness_binding_"
            "observation_consumer_support_duplicate_lineage_and_cross_model_mutations"
        ),
        "negative_control_cases": [
            "theorem deletion",
            "owner laundering",
            "assumption erasure",
            "mutation evidence erasure",
            "unwitnessed P2",
            "unbound P4",
            "observation-free P6",
            "consumer-free retention",
            "support promotion",
            "duplicate without canonical theorem",
            "cross-module literal duplicate laundering",
        ],
        "prohibited_inference": (
            "The overlay does not prove model truth, implementation correctness, deployment "
            "enforcement, empirical validity, transfer, SOTA, AGI, ASI, or any claim promotion."
        ),
        "contract_precision": (
            "exact_live_theorem_semantic_depth_and_rationalization_contract"
        ),
        "semantic_review_state": (
            "current_c6_overlay_with_inherited_reviews_cluster_reviews_and_validator_contracts"
        ),
    })
    required = registry["required_artifacts"]
    for artifact in ARTIFACTS + [REGISTER]:
        if artifact not in required:
            required.append(artifact)
    registry["units"].sort(key=lambda row: row["order"])
    registry["summary"] = {
        "required_artifact_count": len(required),
        "unit_count": len(registry["units"]),
    }
    path.write_text(
        json.dumps(registry, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(
        f"Registered proof semantic-depth overlay: "
        f"{len(registry['units'])} units, {len(required)} artifacts."
    )


if __name__ == "__main__":
    main()
