#!/usr/bin/env python3
"""Idempotently register the exact QCSA cross-book reconciliation gate."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
OVERRIDES = ROOT / "validation/unit_contract_overrides.json"
SCRIPT = "validate_qcsa_book_reconciliation.py"
OWNERS = [
    "cognitive-compilation-and-semantic-ir", "virtual-context-abi",
    "claim-ledgers-and-belief-revision", "runtime-adapters-tool-permissions-and-human-approval",
    "inter-stack-protocols-identity-and-economic-exchange", "routing-heads-and-specialist-cores",
    "compact-generative-systems-and-residual-honesty", "data-engines-continual-learning-and-unlearning",
    "integrated-reference-architecture",
]
ARTIFACTS = [
    "scripts/validate_qcsa_book_reconciliation.py",
    "scripts/register_qcsa_book_reconciliation_validator.py",
    "docs/qcsa_implementation_evidence_reconciliation.md",
    "sources/source_notes/qcsa_whitepaper.md",
    "appendices/C_claim_evidence_matrix.qmd",
    "docs/per_chapter_evidence_plan.md",
    "docs/post_v2_residual_ledger.md",
    "appendices/F_changelog.qmd",
    "evidence_quality/core_claim_vectors.json",
    "claim_decisions/qcsa_reference_evaluation_dispositions.json",
    "experiments/qcsa_reference/results/evaluation_results.json",
    "experiments/qcsa_vertical_reference/results/vertical_result.json",
    *[f"chapters/{owner}.qmd" for owner in OWNERS],
]


def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    unit = next((row for row in registry["units"] if row["script"] == SCRIPT and row.get("args", []) == []), None)
    if unit is None:
        order = len(registry["units"]) + 1
        unit = {"id": f"qcsa_book_reconciliation:{order}", "order": order, "script": SCRIPT, "args": []}
        registry["units"].append(unit)
    unit.update({
        "execution_tier": "deep",
        "validation_class": "proof_or_evidence_gate",
        "input_contract": "The exact QCSA implementation/evaluation/vertical outcomes, ten non-core dispositions, nine core no-change decisions, nine existing chapter owners, source-versus-repository boundary, Appendix C overlay, evidence-plan overlay, non-aggregating quality vectors, eight residuals, changelog transaction, and 54-chapter manifest.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Validate that all nine existing owners expose the bounded mixed result and argument-state boundary; exact matched/resource/active-question negatives remain visible; five promote recommendations remain review inputs rather than automatic transitions; all vectors preserve internal validity and unestablished transfer; eight residuals remain; no QCSA chapter or core promotion exists; reject fifteen cross-surface mutations.",
        "output_assertions": ["nine existing chapter owners", "five bounded review candidates", "two narrowed claims", "two exact refutations", "one no-change transfer boundary", "eight explicit residuals", "54 core claims at argument", "no automatic transition", "no new chapter", "fifteen rejecting mutations"],
        "claim_scope": "Cross-book consistency of the bounded internally authored QCSA implementation, synthetic evaluation, and one local governed vertical replay.",
        "negative_controls": "validator_owned_and_surface_bound",
        "negative_control_cases": ["chapter evidence erasure", "stale crosswalk", "resource failure erasure", "active-question null erasure", "core promotion", "automatic transition", "advantage promotion", "resource promotion", "question result rewrite", "rollback erasure", "Appendix C erasure", "evidence-plan owner erasure", "residual erasure", "transfer promotion", "new QCSA chapter"],
        "prohibited_inference": "The reconciliation does not establish natural-task quality, learned routing, external independence, production transfer, safety, privacy, security, universal grounding, AGI, ASI, a chapter-core promotion, or a reason to add a QCSA chapter.",
        "contract_precision": "exact_high_impact",
        "semantic_review_state": "internal_cross_surface_audit_not_independent",
    })
    for artifact in ARTIFACTS:
        if artifact not in registry["required_artifacts"]:
            registry["required_artifacts"].append(artifact)
    registry["summary"] = {"required_artifact_count": len(registry["required_artifacts"]), "unit_count": len(registry["units"])}
    REGISTRY.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    overrides = json.loads(OVERRIDES.read_text(encoding="utf-8"))
    fields = ["input_contract", "input_artifacts", "output_contract", "output_assertions", "claim_scope", "negative_controls", "negative_control_cases", "prohibited_inference", "contract_precision", "semantic_review_state"]
    record = {"script": SCRIPT, "args": [], **{field: unit[field] for field in fields}}
    override = next((row for row in overrides["contracts"] if row["script"] == SCRIPT and row.get("args", []) == []), None)
    if override is None:
        overrides["contracts"].append(record)
    else:
        override.clear()
        override.update(record)
    OVERRIDES.write_text(json.dumps(overrides, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"registered {SCRIPT}: {registry['summary']['unit_count']} units, {registry['summary']['required_artifact_count']} artifacts")


if __name__ == "__main__":
    main()
