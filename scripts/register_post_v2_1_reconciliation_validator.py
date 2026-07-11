#!/usr/bin/env python3
"""Idempotently register the post-v2.1 reconciliation gate and exact contract."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
OVERRIDES = ROOT / "validation/unit_contract_overrides.json"
SCRIPT = "validate_post_v2_1_empirical_reconciliation.py"
ARTIFACTS = [
    "scripts/validate_post_v2_1_empirical_reconciliation.py",
    "scripts/integrate_post_v2_1_manifest_sources.py",
    "scripts/build_post_v2_1_empirical_dispositions.py",
    "claim_decisions/post_v2_1_empirical_dispositions.json",
    "schemas/post_v2_1_empirical_dispositions.schema.json",
    "evidence_transitions/post_v2_1",
    "docs/post_v2_1_empirical_reconciliation.md",
    "docs/post_v2_1_empirical_results.md",
    "docs/post_v2_residual_ledger.md",
    "docs/per_chapter_evidence_plan.md",
    "roadmap_records/post_v2_1_residual_and_transfer_status.json",
    "book_structure.json", "chapters", "sources/source_inventory.json",
    "appendices/C_claim_evidence_matrix.qmd", "appendices/H_external_sources.qmd",
    "appendices/F_changelog.qmd", "evidence_quality/core_claim_vectors.json",
    "proofs/proof_manifest.json",
]


def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    if not any(row["script"] == SCRIPT for row in registry["units"]):
        order = len(registry["units"]) + 1
        registry["units"].append({
            "id": f"validate_post_v2_1_empirical_reconciliation:{order}", "order": order,
            "execution_tier": "deep", "validation_class": "proof_or_evidence_gate",
            "script": SCRIPT, "args": [],
            "input_contract": "Exact outcome ledger, six accepted component transitions, fourteen core decisions/chapter owners, source manifest/inventory/notes, Appendix C/H, quality vectors, eleven residuals, evidence plan, proof manifest, roadmap status, reconciliation report, and changelog.",
            "input_artifacts": ARTIFACTS,
            "output_contract": "Reject missing or positive dispositions, new chapter/proof invention, chapter/result drift, vector promotion or false independence/transfer, residual laundering, source-route erasure, generated appendix drift, or reconciliation/changelog omission.",
            "output_assertions": ["six bounded transitions", "fourteen core no-change decisions and chapter owners", "eleven exact residual dispositions", "nineteen current external-source routes", "54 argument-state vectors", "no new chapter or Lean target", "M4 reconciliation surfaces agree"],
            "claim_scope": "Repository-wide reconciliation of the completed post-v2.1 finite local results without chapter-core support movement.",
            "negative_controls": "validator_owned",
            "negative_control_cases": ["core promotion", "decision erasure", "transition promotion", "chapter addition", "chapter-result erasure", "vector promotion", "false independence", "residual laundering", "source-target erasure", "Appendix H erasure", "proof invention", "changelog erasure"],
            "prohibited_inference": "Reconciliation does not establish population validity, external independence, production transfer, generated-answer utility, influence/privacy/storage erasure, external-system rollback, optional-format approval, or chapter-core promotion.",
            "contract_precision": "exact_high_impact", "semantic_review_state": "internal_contract_audit_not_independent",
        })
        for artifact in ARTIFACTS:
            if artifact not in registry["required_artifacts"]:
                registry["required_artifacts"].append(artifact)
    registry["summary"] = {"required_artifact_count": len(registry["required_artifacts"]), "unit_count": len(registry["units"])}
    REGISTRY.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    unit = next(row for row in registry["units"] if row["script"] == SCRIPT and row["args"] == [])
    overrides = json.loads(OVERRIDES.read_text(encoding="utf-8"))
    if not any(row["script"] == SCRIPT and row.get("args", []) == [] for row in overrides["contracts"]):
        fields = ["input_contract", "input_artifacts", "output_contract", "output_assertions", "claim_scope", "negative_controls", "negative_control_cases", "prohibited_inference", "contract_precision", "semantic_review_state"]
        overrides["contracts"].append({"script": SCRIPT, "args": [], **{field: unit[field] for field in fields}})
        OVERRIDES.write_text(json.dumps(overrides, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"registered {SCRIPT}: {registry['summary']['unit_count']} units, {registry['summary']['required_artifact_count']} artifacts, exact override bound")


if __name__ == "__main__":
    main()
