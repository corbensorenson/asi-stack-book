#!/usr/bin/env python3
"""Idempotently register the post-v2.2 implementation-roadmap gate."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
OVERRIDES = ROOT / "validation/unit_contract_overrides.json"
SCRIPT = "validate_post_v2_2_implementation_completion_roadmap.py"
ARTIFACTS = [
    "scripts/validate_post_v2_2_implementation_completion_roadmap.py",
    "docs/post_v2_2_implementation_completion_roadmap.md",
    "roadmap_records/post_v2_2_implementation_completion_status.json",
    "schemas/post_v2_2_implementation_completion_status.schema.json",
    "docs/post_v2_1_residual_and_transfer_roadmap.md",
    "docs/v2_2_completion_declaration.md",
    "sources/source_notes/qcsa_whitepaper.md",
    "book_structure.json",
    "sources/source_inventory.json",
    "evidence_quality/core_claim_vectors.json",
    "README.md",
    "index.qmd",
]


def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    matches = [row for row in registry["units"] if row["script"] == SCRIPT and row.get("args", []) == []]
    if matches:
        unit = matches[0]
    else:
        order = len(registry["units"]) + 1
        unit = {"id": f"validate_post_v2_2_implementation_completion_roadmap:{order}", "order": order, "script": SCRIPT, "args": []}
        registry["units"].append(unit)
    unit.update({
        "execution_tier": "deep",
        "validation_class": "proof_or_evidence_gate",
        "input_contract": "One active post-v2.2 implementation-completion roadmap, schema-bound status record, exact v2.2 baseline, twelve QCSA lanes, nine existing chapter owners, and current public pointers.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Reject stale release or roadmap identity, QCSA lane/owner erasure, premature chapter invention, core support promotion, false completion, or activation of optional formats.",
        "output_assertions": ["one active successor", "six priorities", "eight milestones", "twelve QCSA lanes", "nine existing owners", "54 argument-state core claims", "no new chapter or format effect", "eight rejecting mutations"],
        "claim_scope": "Planning-authority installation for a bounded QCSA-first implementation and book-completion cycle.",
        "negative_controls": "validator_owned",
        "negative_control_cases": ["stale release", "missing lane", "wrong owner", "support promotion", "chapter invention", "duplicate active roadmap", "stale public pointer", "false terminal state"],
        "prohibited_inference": "Roadmap activation does not establish QCSA implementation, semantic correctness, benchmark advantage, safety, production transfer, independent review, AGI, ASI, chapter-core promotion, or optional-format approval.",
        "contract_precision": "exact_high_impact",
        "semantic_review_state": "internal_contract_audit_not_independent",
    })
    for artifact in ARTIFACTS:
        if artifact not in registry["required_artifacts"]:
            registry["required_artifacts"].append(artifact)
    registry["summary"] = {"required_artifact_count": len(registry["required_artifacts"]), "unit_count": len(registry["units"])}
    REGISTRY.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    overrides = json.loads(OVERRIDES.read_text(encoding="utf-8"))
    fields = ["input_contract", "input_artifacts", "output_contract", "output_assertions", "claim_scope", "negative_controls", "negative_control_cases", "prohibited_inference", "contract_precision", "semantic_review_state"]
    override = next((row for row in overrides["contracts"] if row["script"] == SCRIPT and row.get("args", []) == []), None)
    record = {"script": SCRIPT, "args": [], **{field: unit[field] for field in fields}}
    if override is None:
        overrides["contracts"].append(record)
    else:
        override.clear()
        override.update(record)
    OVERRIDES.write_text(json.dumps(overrides, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"registered {SCRIPT}: {registry['summary']['unit_count']} units, {registry['summary']['required_artifact_count']} artifacts")


if __name__ == "__main__":
    main()
