#!/usr/bin/env python3
"""Idempotently register the metadata-first editorial migration gate."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
OVERRIDES = ROOT / "validation/unit_contract_overrides.json"
SCRIPT = "validate_editorial_migration.py"
ARTIFACTS = [
    "scripts/validate_editorial_migration.py",
    "scripts/build_editorial_migration_preview.py",
    "scripts/register_editorial_migration_validator.py",
    "scripts/reconcile_editorial_migration_claim_reviews.py",
    "schemas/book_structure.schema.json",
    "book_structure.json",
    "products/editorial_migration_preview.json",
    "products/narrative_product_spine.json",
    "products/narrative_unit_crosswalk.json",
    "docs/human_reader_26_unit_outline.md",
    "docs/book_outline.md",
    "roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json",
    "schemas/post_v2_3_maintenance_transfer_and_publication_status.schema.json",
    "evidence_quality/prose_claim_candidate_queue.json",
    "evidence_quality/claim_reviews/compact-generative-systems-and-residual-honesty.json",
    "evidence_quality/claim_reviews/governed-deliberation-and-test-time-scaling.json",
    "evidence_quality/claim_reviews/rankfold-neuralfold-and-artifact-compression.json",
    "evidence_quality/claim_reviews/resource-economics-and-token-budgets.json",
]


def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    unit = next(
        (row for row in registry["units"] if row["script"] == SCRIPT and row.get("args", []) == []),
        None,
    )
    if unit is None:
        order = max(row["order"] for row in registry["units"]) + 1
        unit = {"id": f"{SCRIPT}:{order}", "order": order, "script": SCRIPT, "args": []}
        registry["units"].append(unit)
    contract = {
        "execution_tier": "pr",
        "validation_class": "proof_or_evidence_gate",
        "input_contract": "The canonical 87-owner graph, reviewed 54+2/18/7/5/1 publication disposition, exact 26-unit owner route, and metadata-only EM0/EM1 state.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Require disjoint owner roles, exact parents and legacy routes, local claim ownership, one Human Reader route per owner, a canonical preview, and no prose, support, release, or public-route cutover.",
        "output_assertions": [
            "87 canonical technical owners",
            "54 primary architecture owners",
            "2 implementation/method owners",
            "15 publication nests",
            "2 method-detail nests",
            "1 gated semantic-merge candidate",
            "7 deployment profiles",
            "5 dossier owners",
            "1 back-matter owner",
            "26 Human Reader units",
            "4 semantic mutations reject",
            "support and release effects none",
        ],
        "claim_scope": "Metadata-only publication classification, legacy identity preservation, and Human Reader routing for EM0/EM1.",
        "negative_controls": "validator_owned_support_parent_route_and_composition_mutations",
        "negative_control_cases": ["support promotion", "owner reroute", "parent erasure", "composition-boundary erasure"],
        "prohibited_inference": "Metadata classification does not complete publication composition, the semantic merge, Human Reader prose, public cutover, release, safety, readiness, AGI, or ASI.",
        "contract_precision": "exact_high_impact",
        "semantic_review_state": "checked_metadata_only_editorial_migration",
    }
    unit.update(contract)
    for artifact in ARTIFACTS:
        if artifact not in registry["required_artifacts"]:
            registry["required_artifacts"].append(artifact)
    registry["units"].sort(key=lambda row: row["order"])
    registry["summary"] = {
        "required_artifact_count": len(registry["required_artifacts"]),
        "unit_count": len(registry["units"]),
    }
    REGISTRY.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    overrides = json.loads(OVERRIDES.read_text(encoding="utf-8"))
    fields = [key for key in contract if key != "execution_tier" and key != "validation_class"]
    record = {"script": SCRIPT, "args": [], **{key: contract[key] for key in fields}}
    existing = next(
        (row for row in overrides["contracts"] if row["script"] == SCRIPT and row.get("args", []) == []),
        None,
    )
    if existing is None:
        overrides["contracts"].append(record)
    else:
        existing.clear()
        existing.update(record)
    OVERRIDES.write_text(json.dumps(overrides, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(
        f"Registered {SCRIPT}: {registry['summary']['unit_count']} units, "
        f"{registry['summary']['required_artifact_count']} artifacts."
    )


if __name__ == "__main__":
    main()
