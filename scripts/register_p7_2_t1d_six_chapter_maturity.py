#!/usr/bin/env python3
"""Register the P7.2-T1D manuscript-maturity validation unit."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_p7_2_t1d_six_chapter_maturity.py"
ARTIFACTS = [
    "evidence_quality/p7_2_t1d_six_chapter_maturity.json",
    "schemas/p7_2_t1d_six_chapter_maturity.schema.json",
    "docs/p7_2_t1d_six_chapter_maturity_and_source_role_review_2026_07_26.md",
    "scripts/build_p7_2_t1d_six_chapter_maturity.py",
    "scripts/validate_p7_2_t1d_six_chapter_maturity.py",
    "scripts/register_p7_2_t1d_six_chapter_maturity.py",
    "book_structure.json",
    "sources/source_inventory.json",
    "appendices/C_claim_evidence_matrix.qmd",
    "appendices/H_external_sources.qmd",
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
            "input_contract": "Six exact current chapters, their six-condition manuscript-maturity locations, passage-reviewed source roles, applicable claim identities, four existing-owner repairs, reader projections, and chapter-specific prose anchors.",
            "input_artifacts": ARTIFACTS,
            "output_contract": "Record manuscript maturity for competent implementation and a fair test while preserving residuals, noninheritance, current-reader follow-up, and zero support movement.",
            "output_assertions": [
                "6 of 6 chapter maturity records complete",
                "36 of 36 condition decisions passed for manuscript maturity",
                "12 of 12 chapter-specific anchors have one corpus owner",
                "4 of 4 existing-owner repairs present",
                "5 of 5 White-Box source receipts current",
                "10 applicable atom identities reconciled",
                "18 mutations reject",
                "zero support, release, or publication movement"
            ],
            "claim_scope": "Idea placement, source-role engagement, reader organization, and future implementation/test specification only.",
            "negative_controls": "validator_owned_eighteen_scope_source_identity_reader_residual_and_authority_mutations",
            "prohibited_inference": "Manuscript maturity is not proof, empirical evidence, reproduction, mechanism success or failure, transfer, safety, readiness, release, SOTA, AGI, or ASI.",
            "contract_precision": "exact",
            "semantic_review_state": "manual_six_chapter_field_challenge_mechanism_failure_source_and_reader_review"
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
