#!/usr/bin/env python3
"""Register the cumulative C6 dependency-safe rationalization ledger."""

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
    "lean/AsiStackProofs/BibliographyPlan.lean",
    "proofs/proof_manifest.json",
    "proofs/proof_triage.json",
    "book_structure.json",
    "docs/book_outline.md",
    "chapters/open-research-agenda-and-bibliography-plan.qmd",
    "roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json",
    "docs/post_v2_3_maintenance_transfer_and_publication_roadmap.md",
    "validation/registry.json",
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
            "One immutable 1,370-theorem baseline; three exact, ordered transactions; "
            "the baseline Scalable Oversight and Bibliography Plan modules; one same-model "
            "normalized duplicate pair; two premise-restating projections and their "
            "derived counterexample replacements; the current overlay; frozen historical "
            "registry; and reconciled target, roadmap, and status surfaces."
        ),
        "input_artifacts": ARTIFACTS + [REGISTER],
        "output_contract": (
            "Require immutable baseline and theorem-block digests, exact same-model "
            "statement identity for the duplicate, dependency-and-consumer-safe removals, "
            "two counterexample target migrations, retained target ownership, a "
            "1,367-theorem current estate, an exact 158-action remaining queue, and no "
            "support or release effect."
        ),
        "output_assertions": [
            "baseline commit and artifact digests exact",
            "retired and retained declarations share one authored model",
            "normalized theorem statements exact",
            "retired theorem has no theorem consumer",
            "three retired declarations absent and all replacements live",
            "two bibliography targets migrated to derived counterexample gates",
            "1,367 current theorem declarations",
            "158 rewrite-or-retire actions remain",
            "frozen 1,151-theorem and 298-target registry preserved",
            "12 mutations reject",
            "no support or release effect",
        ],
        "claim_scope": (
            "Three dependency-safe declaration retirements: one exact same-model "
            "duplicate and two premise-restating projections with target migration."
        ),
        "negative_controls": (
            "validator_owned_twelve_baseline_digest_sequence_identity_statement_dependency_"
            "consumer_target_denominator_and_support_mutations"
        ),
        "negative_control_cases": [
            "baseline commit substitution",
            "overlay digest substitution",
            "action deletion or reordering",
            "retired or replacement identity substitution",
            "statement substitution",
            "dependency laundering",
            "consumer laundering",
            "target migration erasure",
            "remaining denominator inflation",
            "support promotion",
        ],
        "prohibited_inference": (
            "This transaction does not strengthen the retained finite-model theorem or "
            "establish reviewer competence, implementation correctness, useful oversight, "
            "deployment, transfer, safety, SOTA, AGI, ASI, or claim support."
        ),
        "contract_precision": "exact_immutable_cumulative_dependency_safe_retirement_ledger",
        "semantic_review_state": "checked_three_c6_retirements_and_two_target_migrations",
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
        f"Registered cumulative proof semantic-rationalization ledger: "
        f"{len(registry['units'])} units, {len(required)} artifacts."
    )


if __name__ == "__main__":
    main()
