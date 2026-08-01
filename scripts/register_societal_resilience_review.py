#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_societal_resilience_review.py"
ARTIFACTS = [
    "scripts/validate_societal_resilience_review.py",
    "lean/AsiStackProofs/SocietalResilienceReview.lean",
    "tests/fixtures/proof_models/societal_resilience_dossier.json",
    "evidence_quality/proof_model_dossiers/societal-resilience-and-misuse-defense.md",
    "chapters/societal-resilience-and-misuse-defense.qmd",
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
        "input_contract": "Canonical societal-resilience Lean review, independent 45-axis fixture, chapter proof boundary, dossier, manifest, triage, and outline binding.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Reject lifecycle, exact-repair, evidence-substitution, authority, incident-path, receipt, monotonicity, collision, consumer, binding, and no-promotion drift.",
        "output_assertions": [
            "eight-transition review reaches only Project Theseus synthetic resilience-exercise eligibility",
            "45/45 admission-axis mutations reject readiness and receive exact repair or refusal dispositions",
            "provider actions, exercises, speed, local safeguards, population resilience, recovery, remedy, and cross-organization defense remain separate",
            "one organization cannot inherit another organization's response mandate",
            "finite incident-path closure covers every listed path",
            "incident, population, jurisdiction, protocol, expiry, and adverse shortfalls remain scoped",
            "provider signals cannot recover population resilience and response speed cannot recover equitable remedy",
            "the institutional consumer rejects an incomplete participant census",
            "32 exact Lean declarations move no chapter support, deployment, release, transfer, or external-effect state",
        ],
        "claim_scope": "Bounded authored societal-resilience review, evidence-role separation, organization authority, finite path accounting, receipt invalidation, consumer rejection, and non-identifiability only.",
        "negative_controls": "validator_owned_45_axis_identity_coordination_defense_recovery_remedy_adaptation_receipt_collision_consumer_and_binding_mutations",
        "negative_control_cases": ["provider-metric laundering", "tabletop laundering", "cross-organization authority", "uncovered population", "unrepaired path", "unequal remedy", "support promotion"],
        "prohibited_inference": "Does not establish population resilience, lawful authority, cross-organization cooperation, recovery, remedy efficacy, acceptable residual harm, deployment, transfer, SOTA, AGI, or ASI.",
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
