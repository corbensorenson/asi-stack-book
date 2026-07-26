#!/usr/bin/env python3
"""Register the R16-A six-chapter claim-organization validation unit."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_post_activation_six_chapter_claim_atom_addendum.py"
ARTIFACTS = [
    "evidence_quality/post_activation_six_chapter_claim_atom_addendum.json",
    "schemas/post_activation_six_chapter_claim_atom_addendum.schema.json",
    "scripts/build_post_activation_six_chapter_claim_atom_addendum.py",
    "scripts/validate_post_activation_six_chapter_claim_atom_addendum.py",
    "scripts/register_post_activation_six_chapter_claim_atom_addendum.py",
    "book_structure.json",
    "docs/per_chapter_evidence_plan.md",
    "appendices/C_claim_evidence_matrix.qmd",
]


def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    registry["units"] = [unit for unit in registry["units"] if unit.get("script") != SCRIPT]
    used = {unit["order"] for unit in registry["units"]}
    order = next(value for value in range(1, len(registry["units"]) + 2) if value not in used)
    registry["units"].append(
        {
            "id": f"{SCRIPT}:{order}",
            "order": order,
            "script": SCRIPT,
            "args": [],
            "execution_tier": "pr",
            "validation_class": "proof_or_evidence_gate",
            "input_contract": "Six exact current manifest chapters; each chapter's core claim, ownership boundary, mechanism, failure/noninheritance rule, argument-exit target, evidence-plan route, and digest-bound semantic review receipt; immutable historical atom denominators.",
            "input_artifacts": ARTIFACTS,
            "output_contract": "Keep exactly five reviewed claim roles per chapter with stable owner, proposition, scope, falsifier, acceptance criterion, promotion ceiling, evidence route, chapter anchor, and non-claims while preserving argument support and historical denominators.",
            "output_assertions": [
                "6 of 6 chapter reviews complete",
                "30 of 30 atoms reviewed",
                "one core, boundary, mechanism, failure boundary, and argument-exit atom per chapter",
                "exact manifest core propositions",
                "zero support or release movement",
                "fourteen mutations reject",
            ],
            "claim_scope": "Claim organization, ownership, falsification boundaries, and future evidence routing only.",
            "negative_controls": "validator_owned_fourteen_identity_review_support_and_denominator_mutations",
            "negative_control_cases": [
                "chapter receipt deletion",
                "atom deletion",
                "duplicate atom identity",
                "wrong owner",
                "core proposition rewrite",
                "chapter digest rewrite",
                "support promotion",
                "support movement",
                "falsifier deletion",
                "acceptance deletion",
                "evidence route deletion",
                "nonclaim deletion",
                "historical denominator rewrite",
                "review atom mismatch",
            ],
            "prohibited_inference": "Claim organization is not claim truth, proof, empirical evidence, implementation evidence, source-derived support, reproduction, transfer, safety, release, SOTA, AGI, or ASI.",
            "contract_precision": "exact",
            "semantic_review_state": "manual_six_chapter_core_boundary_mechanism_failure_and_argument_exit_review",
        }
    )
    for artifact in ARTIFACTS:
        if artifact not in registry["required_artifacts"]:
            registry["required_artifacts"].append(artifact)
    registry["units"].sort(key=lambda unit: unit["order"])
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
