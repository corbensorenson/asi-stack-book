#!/usr/bin/env python3
"""Register the first C6 dependency-safe semantic-rationalization transaction."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = "validate_proof_semantic_rationalization_ledger.py"
REGISTER = "scripts/register_proof_semantic_rationalization_ledger.py"
ARTIFACTS = [
    "scripts/validate_proof_semantic_rationalization_ledger.py",
    "schemas/proof_semantic_rationalization_ledger.schema.json",
    "proofs/proof_semantic_rationalization_ledger.json",
    "proofs/proof_semantic_depth_overlay.json",
    "proofs/proof_rationalization_registry.json",
    "lean/AsiStackProofs/ScalableOversightRefinement.lean",
    "roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json",
    "docs/post_v2_3_maintenance_transfer_and_publication_roadmap.md",
    "validation/registry.json",
]


def main() -> None:
    path = ROOT / "validation" / "registry.json"
    registry = json.loads(path.read_text(encoding="utf-8"))
    registry["units"] = [
        row for row in registry["units"] if row.get("script") != SCRIPT
    ]
    order = max(row["order"] for row in registry["units"]) + 1
    registry["units"].append({
        "id": f"{SCRIPT}:{order}",
        "order": order,
        "script": SCRIPT,
        "args": [],
        "execution_tier": "pr",
        "validation_class": "proof_or_evidence_gate",
        "input_contract": (
            "One immutable 1,370-theorem baseline, its exact Scalable Oversight module, "
            "one same-model normalized duplicate pair, current overlay, frozen historical "
            "registry, and reconciled roadmap/status surfaces."
        ),
        "input_artifacts": ARTIFACTS + [REGISTER],
        "output_contract": (
            "Require immutable baseline digests, exact same-model statement identity, "
            "dependency-and-consumer-safe removal, retained canonical target ownership, "
            "a 1,369-theorem current estate, an exact 160-action remaining queue, and no "
            "support or release effect."
        ),
        "output_assertions": [
            "baseline commit and artifact digests exact",
            "retired and retained declarations share one authored model",
            "normalized theorem statements exact",
            "retired theorem has no theorem consumer",
            "retired declaration absent and canonical declaration live",
            "1,369 current theorem declarations",
            "160 rewrite-or-retire actions remain",
            "frozen 1,151-theorem and 298-target registry preserved",
            "10 mutations reject",
            "no support or release effect",
        ],
        "claim_scope": (
            "One dependency-safe redundant-declaration retirement transaction only."
        ),
        "negative_controls": (
            "validator_owned_ten_baseline_digest_identity_statement_dependency_consumer_"
            "denominator_and_support_mutations"
        ),
        "negative_control_cases": [
            "baseline commit substitution",
            "overlay digest substitution",
            "module digest substitution",
            "retired or retained identity substitution",
            "normalized statement substitution",
            "dependency or consumer laundering",
            "remaining denominator inflation",
            "support promotion",
        ],
        "prohibited_inference": (
            "This transaction does not strengthen the retained finite-model theorem or "
            "establish reviewer competence, implementation correctness, useful oversight, "
            "deployment, transfer, safety, SOTA, AGI, ASI, or claim support."
        ),
        "contract_precision": "exact_immutable_same_model_duplicate_retirement_transaction",
        "semantic_review_state": "checked_dependency_safe_first_c6_retirement",
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
        f"Registered proof semantic-rationalization ledger: "
        f"{len(registry['units'])} units, {len(required)} artifacts."
    )


if __name__ == "__main__":
    main()
