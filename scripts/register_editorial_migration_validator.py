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
    "chapters/security-kernel-and-digital-scifs.qmd",
    "chapters/adversarial-machine-learning-and-model-attack-surface.qmd",
    "chapters/privacy-data-rights-and-information-flow-governance.qmd",
    "chapters/confidential-and-verifiable-ai-computation.qmd",
    "chapters/model-weight-custody-and-hardware-roots-of-trust.qmd",
    "chapters/ai-supply-chain-integrity-and-lifecycle-provenance.qmd",
    "chapters/open-weight-release-and-post-release-control.qmd",
    "evidence_quality/claim_reviews/security-kernel-and-digital-scifs.json",
    "evidence_quality/claim_reviews/adversarial-machine-learning-and-model-attack-surface.json",
    "evidence_quality/claim_reviews/model-weight-custody-and-hardware-roots-of-trust.json",
    "evidence_quality/claim_reviews/ai-supply-chain-integrity-and-lifecycle-provenance.json",
    "chapters/adversarial-evaluation-sandbagging-and-training-time-deception.qmd",
    "chapters/white-box-evidence-interpretability-and-activation-governance.qmd",
    "evidence_quality/claim_reviews/adversarial-evaluation-sandbagging-and-training-time-deception.json",
    "chapters/human-factors-and-meaningful-control-in-oversight.qmd",
    "chapters/human-ai-communication-persuasion-and-epistemic-security.qmd",
    "chapters/constitutional-alignment-substrate.qmd",
    "chapters/moral-uncertainty-and-value-conflict.qmd",
    "chapters/institutions-international-coordination-and-public-legitimacy.qmd",
    "chapters/societal-resilience-and-misuse-defense.qmd",
    "chapters/intent-to-execution-contracts.qmd",
    "chapters/human-intent-as-a-formal-input.qmd",
    "evidence_quality/claim_reviews/human-ai-communication-persuasion-and-epistemic-security.json",
    "evidence_quality/claim_reviews/constitutional-alignment-substrate.json",
    "evidence_quality/claim_reviews/moral-uncertainty-and-value-conflict.json",
    "evidence_quality/claim_reviews/institutions-international-coordination-and-public-legitimacy.json",
    "evidence_quality/claim_reviews/intent-to-execution-contracts.json",
    "evidence_quality/claim_reviews/human-intent-as-a-formal-input.json",
    "chapters/virtual-context-abi.qmd",
    "chapters/context-transactions-snapshots-mounts-and-taint.qmd",
    "chapters/ai-work-surfaces-agent-harnesses-and-organizational-absorption.qmd",
    "chapters/human-ai-organizations-delegation-and-accountability.qmd",
    "chapters/inter-stack-protocols-identity-and-economic-exchange.qmd",
    "chapters/multi-agent-dynamics-collective-intelligence-and-systemic-risk.qmd",
    "evidence_quality/claim_reviews/virtual-context-abi.json",
    "evidence_quality/claim_reviews/context-transactions-snapshots-mounts-and-taint.json",
    "evidence_quality/claim_reviews/inter-stack-protocols-identity-and-economic-exchange.json",
]
STALE_POST_ACTIVATION_CLAIM_REVIEWS = {
    "evidence_quality/claim_reviews/human-factors-and-meaningful-control-in-oversight.json",
    "evidence_quality/claim_reviews/societal-resilience-and-misuse-defense.json",
}


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
        "input_contract": "The canonical 87-owner graph, reviewed 54+2/18/7/5/1 publication disposition, exact 26-unit owner route, and the five completed no-cutover EM2 composition packages.",
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
            "13 semantic mutations reject",
            "support and release effects none",
        ],
        "claim_scope": "Publication classification, legacy identity preservation, Human Reader routing, and five evidence-preserving EM2 composition packages without public cutover.",
        "negative_controls": "validator_owned_support_parent_route_and_composition_mutations",
        "negative_control_cases": ["support promotion", "owner reroute", "parent erasure", "method-detail composition-boundary erasure", "security-custody composition-boundary erasure", "white-box composition-boundary erasure", "human-control/communication boundary erasure", "constitution/moral-conflict boundary erasure", "institution/resilience boundary erasure", "intent/command boundary erasure", "context static/dynamic boundary erasure", "work-surface/organization boundary erasure", "protocol/population boundary erasure"],
        "prohibited_inference": "Composition does not transfer technical ownership or support, complete the remaining publication nests or semantic merge, authorize public cutover or release, or establish safety, readiness, AGI, or ASI.",
        "contract_precision": "exact_high_impact",
        "semantic_review_state": "checked_five_no_cutover_composition_packages",
    }
    unit.update(contract)
    referenced = {
        artifact
        for row in registry["units"]
        for artifact in row.get("input_artifacts", [])
    }
    registry["required_artifacts"] = [
        artifact
        for artifact in registry["required_artifacts"]
        if artifact not in STALE_POST_ACTIVATION_CLAIM_REVIEWS or artifact in referenced
    ]
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
