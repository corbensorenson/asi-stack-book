#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_durable_semantic_memory_review.py"
ARTIFACTS = [
    "scripts/validate_durable_semantic_memory_review.py",
    "lean/AsiStackProofs/DurableSemanticMemoryReview.lean",
    "tests/fixtures/proof_models/durable_semantic_memory_dossier.json",
    "evidence_quality/proof_model_dossiers/durable-semantic-memory-and-knowledge-lattices.md",
    "chapters/durable-semantic-memory-and-knowledge-lattices.qmd",
    "proofs/proof_manifest.json", "proofs/proof_triage.json", "docs/book_outline.md",
]


def main() -> None:
    value = json.loads(REGISTRY.read_text(encoding="utf-8"))
    existing = next((row for row in value["units"] if row.get("script") == SCRIPT), None)
    value["units"] = [row for row in value["units"] if row.get("script") != SCRIPT]
    used = {row["order"] for row in value["units"]}
    preferred = existing.get("order") if existing else None
    order = preferred if preferred and preferred not in used else next(
        i for i in range(1, len(value["units"]) + 2) if i not in used
    )
    value["units"].append({
        "id": f"{SCRIPT}:{order}", "order": order, "script": SCRIPT, "args": [],
        "execution_tier": "pr", "validation_class": "proof_or_evidence_gate",
        "input_contract": "Canonical durable-semantic-memory Lean review, independent 38-axis fixture, chapter proof boundary, dossier, manifest, triage, and outline binding.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Reject lifecycle, exact-repair, identity, provenance, authority, migration, retrieval, replay, receipt, collision, consumer, binding, and no-promotion drift.",
        "output_assertions": [
            "seven-transition review reaches only Project Theseus memory replay and retrieval-campaign eligibility",
            "38/38 admission-axis mutations reject readiness and receive exact repair or refusal dispositions",
            "representation rebuilds preserve object identity while aliases do not determine referent equality",
            "finite parent induction preserves provenance and prevents derived purpose-authority broadening",
            "lossy ontology migration requires affected-consumer invalidation",
            "every used retrieval object retains provenance, support, rights, contradiction, and retraction custody",
            "event-log replay composes exactly across concatenated event sequences",
            "object, ontology, evidence epoch, and consumer purpose changes invalidate receipts",
            "summaries cannot recover contradiction state and storage deletion cannot recover learned influence",
            "open deletion duty blocks Context Transactions materialization",
            "35 exact Lean declarations move no chapter support, deployment, release, transfer, or external-effect state",
        ],
        "claim_scope": "Bounded authored semantic-memory review, identity/revision/migration/retrieval/replay custody, receipt invalidation, consumer rejection, and non-identifiability only.",
        "negative_controls": "validator_owned_38_axis_identity_revision_migration_retrieval_retention_receipt_collision_consumer_and_binding_mutations",
        "negative_control_cases": ["alias identity collapse", "provenance loss", "authority broadening", "lossy migration", "unreceipted retrieval", "deletion laundering", "support promotion"],
        "prohibited_inference": "Does not establish semantic truth, retrieval utility, complete memory, semantic restart equivalence, behavioral forgetting, deployment, transfer, SOTA, AGI, or ASI.",
        "contract_precision": "exact",
        "semantic_review_state": "checked_bounded_formal_model_and_independent_consumer_no_support_effect",
    })
    required = list(value["required_artifacts"])
    for artifact in ARTIFACTS:
        if artifact not in required:
            required.append(artifact)
    value["units"].sort(key=lambda row: row["order"])
    value["required_artifacts"] = required
    value["summary"] = {"required_artifact_count": len(required), "unit_count": len(value["units"])}
    REGISTRY.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    print(f"Registered {SCRIPT}: {len(value['units'])} units, {len(required)} artifacts.")


if __name__ == "__main__":
    main()
