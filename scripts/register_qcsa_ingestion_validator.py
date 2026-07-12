#!/usr/bin/env python3
"""Idempotently register the QCSA ingestion gate and exact contract."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
OVERRIDES = ROOT / "validation/unit_contract_overrides.json"
SCRIPT = "validate_qcsa_ingestion.py"
ARTIFACTS = [
    "scripts/validate_qcsa_ingestion.py",
    "scripts/integrate_qcsa_source.py",
    "sources/source_inventory.json",
    "sources/source_notes/qcsa_whitepaper.md",
    "book_structure.json",
    "chapters",
    "docs/book_outline.md",
    "appendices/A_source_matrix.qmd",
    "appendices/C_claim_evidence_matrix.qmd",
    "appendices/G_corben_source_corpus.qmd",
    "appendices/F_changelog.qmd",
    "evidence_quality/core_claim_vectors.json",
]


def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    if not any(row["script"] == SCRIPT for row in registry["units"]):
        order = len(registry["units"]) + 1
        unit = {
            "id": f"validate_qcsa_ingestion:{order}",
            "order": order,
            "execution_tier": "deep",
            "validation_class": "proof_or_evidence_gate",
            "script": SCRIPT,
            "args": [],
            "input_contract": "One digest-bound Corben-authored QCSA inventory record and source note, nine passage-reviewed existing-chapter mappings, chapter prose/crosswalks, generated source appendices, evidence vectors, and changelog.",
            "input_artifacts": ARTIFACTS,
            "output_contract": "Reject source or target erasure, unreviewed mapping laundering, chapter-core promotion, standalone-chapter invention, or removal of the implementation/benchmark/proof/safety/performance non-claim.",
            "output_assertions": ["one QCSA author source", "nine existing chapter owners", "passage-reviewed mappings", "54 argument-state chapters", "no new chapter", "six rejecting mutations"],
            "claim_scope": "Conservative source ingestion and cross-chapter design-rationale integration for Question-Compiled Semantic Addressing.",
            "negative_controls": "validator_owned",
            "negative_control_cases": ["source erasure", "target erasure", "passage-review laundering", "support promotion", "chapter invention", "non-claim erasure"],
            "prohibited_inference": "Ingestion does not establish a QCSA implementation, benchmark, semantic-correctness proof, novelty, safety, performance advantage, production transfer, AGI, ASI, or chapter-core support promotion.",
            "contract_precision": "exact_high_impact",
            "semantic_review_state": "internal_contract_audit_not_independent",
        }
        registry["units"].append(unit)
        for artifact in ARTIFACTS:
            if artifact not in registry["required_artifacts"]:
                registry["required_artifacts"].append(artifact)
    unit = next(row for row in registry["units"] if row["script"] == SCRIPT and row.get("args", []) == [])
    unit["validation_class"] = "proof_or_evidence_gate"
    registry["summary"] = {"required_artifact_count": len(registry["required_artifacts"]), "unit_count": len(registry["units"])}
    REGISTRY.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    overrides = json.loads(OVERRIDES.read_text(encoding="utf-8"))
    if not any(row["script"] == SCRIPT and row.get("args", []) == [] for row in overrides["contracts"]):
        fields = ["input_contract", "input_artifacts", "output_contract", "output_assertions", "claim_scope", "negative_controls", "negative_control_cases", "prohibited_inference", "contract_precision", "semantic_review_state"]
        overrides["contracts"].append({"script": SCRIPT, "args": [], **{field: unit[field] for field in fields}})
        OVERRIDES.write_text(json.dumps(overrides, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"registered {SCRIPT}: {registry['summary']['unit_count']} units, {registry['summary']['required_artifact_count']} artifacts, exact override bound")


if __name__ == "__main__":
    main()
