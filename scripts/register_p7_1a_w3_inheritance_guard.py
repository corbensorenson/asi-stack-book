#!/usr/bin/env python3
"""Register the P7.1a-W3 admission-template inheritance guard."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_p7_1a_w3_inheritance_guard.py"
ARTIFACTS = [
    "evidence_quality/p7_1a_w3_inheritance_guard.json",
    "schemas/p7_1a_w3_inheritance_guard.schema.json",
    "docs/p7_1a_w3_inheritance_guard.md",
    "scripts/build_p7_1a_w3_inheritance_guard.py",
    "scripts/validate_p7_1a_w3_inheritance_guard.py",
    "scripts/register_p7_1a_w3_inheritance_guard.py",
    "tests/fixtures/p7_1a_w3_inheritance_guard/copied_scaffold.qmd",
    "tests/fixtures/p7_1a_w3_inheritance_guard/distinct_chapter.qmd",
    "chapters/living-book-methodology.qmd",
    "book_structure.json",
    "evidence_quality/claim_atom_registry.json",
    "evidence_quality/prose_claim_candidate_queue.json",
    "evidence_quality/claim_atom_reviews.json",
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
            "input_contract": "Exact 84-chapter manifest at immutable pre-edit commit 99457770390a4af4848b9e43656907cfe099fd75 and current worktree; NFKC tokenization; raw, editorial, diagram, and Codex-test projections; ten semantic-diff reviews; copied and distinct fixtures.",
            "input_artifacts": ARTIFACTS,
            "output_contract": "Centralize shared lifecycle prose once, preserve chapter-specific claims/sources/boundaries/evidence plans, report generated projections separately, and reject future copied chapter scaffolds.",
            "output_assertions": [
                "84 exact manifest chapters before and after",
                "editorial repeated 12-grams at spread eight fall 812 to zero",
                "copied diagram and Codex-test maximum spread fall ten to zero",
                "ten chapter-specific repairs retain meaning custody",
                "241 inherited prose IDs retire into 177 reviewed domain-specific replacements with 4,067 atoms unchanged and zero pending candidates",
                "copied fixture rejects and distinct fixture accepts",
                "eighteen mutations reject",
                "support, release, and publication effects none"
            ],
            "claim_scope": "Editorial ownership, distinctness, and admission-time inheritance control only.",
            "negative_controls": "tracked_copied_scaffold_fixture_plus_validator_owned_eighteen_mutations",
            "negative_control_cases": [
                "copied lifecycle diagram and generic disposition table",
                "missing unique claim, sources, boundary, evidence plan, diagram, tests, or handoff",
                "threshold, denominator, fingerprint, custody, support, or publication mutation"
            ],
            "prohibited_inference": "Reduced repetition and schema-valid distinctness do not establish claim truth, empirical evidence, formal proof, implementation efficacy, safety, transfer, SOTA, AGI, ASI, release, or publication.",
            "contract_precision": "exact",
            "semantic_review_state": "manual_ten_chapter_claim_source_boundary_and_support_preservation_review"
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
