#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_objective_lease_governance.py"
ARTIFACTS = [
    "scripts/validate_objective_lease_governance.py",
    "lean/AsiStackProofs/ObjectiveLeaseGovernance.lean",
    "tests/fixtures/proof_models/objective_lease_dossier.json",
    "evidence_quality/proof_model_dossiers/governed-objective-formation-value-learning-and-goal-integrity.md",
    "chapters/governed-objective-formation-value-learning-and-goal-integrity.qmd",
    "proofs/proof_manifest.json",
    "proofs/proof_triage.json",
    "docs/book_outline.md",
]


def main() -> None:
    value = json.loads(REGISTRY.read_text(encoding="utf-8"))
    existing = next((row for row in value["units"] if row.get("script") == SCRIPT), None)
    value["units"] = [row for row in value["units"] if row.get("script") != SCRIPT]
    used = {row["order"] for row in value["units"]}
    preferred = existing.get("order") if existing else None
    order = preferred if preferred and preferred not in used else next(i for i in range(1, len(value["units"]) + 2) if i not in used)
    value["units"].append({
        "id": f"{SCRIPT}:{order}", "order": order, "script": SCRIPT, "args": [],
        "execution_tier": "pr", "validation_class": "proof_or_evidence_gate",
        "input_contract": "Canonical objective-lease Lean model, independent 46-axis fixture, chapter proof boundary, proof dossier, manifest, triage, and outline binding.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Reject lifecycle, exact-repair, typed-ratification, lease-scope, finite-retirement, collision-witness, consumer-bridge, canonical-binding, and no-promotion drift.",
        "output_assertions": [
            "seven-stage review reaches only Project Theseus objective-registry-study eligibility",
            "46/46 admission-axis mutations reject readiness and receive exact repair or refusal dispositions",
            "optimizer, reward-model, and evaluator roles cannot ratify an objective in the encoded authority type",
            "consumer transfer, expiry, ontology drift, and authority drift invalidate lease use",
            "retireAll closes every member of an arbitrary finite descendant-binding list",
            "proxy observations cannot recover target movement and preference predictions cannot recover authority",
            "the learned-objective consumer receives only bounded packet fields and no certainty, support, or external-authority claim",
            "27 exact Lean declarations move no chapter support, release, transfer, or external-effect state",
        ],
        "claim_scope": "Bounded authored-record review, typed authority, finite lease checks, inductive finite retirement, consumer refinement, and finite non-identifiability only.",
        "negative_controls": "validator_owned_46_axis_authority_lease_retirement_collision_consumer_and_binding_mutations",
        "negative_control_cases": ["optimizer self-ratification", "proxy-target laundering", "preference-authority laundering", "consumer transfer", "ontology drift", "incomplete retirement", "support promotion laundering"],
        "prohibited_inference": "Does not establish correct values, consent, moral truth, political legitimacy, corrigibility, preference accuracy, target truth, behavioral goal alignment, complete external retirement, safe optimization, transfer, SOTA, AGI, or ASI.",
        "contract_precision": "exact", "semantic_review_state": "checked_bounded_formal_model_and_independent_consumer_no_support_effect",
    })
    required = list(value["required_artifacts"])
    for artifact in ARTIFACTS:
        if artifact not in required: required.append(artifact)
    value["units"].sort(key=lambda row: row["order"])
    value["required_artifacts"] = required
    value["summary"] = {"required_artifact_count": len(required), "unit_count": len(value["units"])}
    REGISTRY.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    print(f"Registered {SCRIPT}: {len(value['units'])} units, {len(required)} artifacts.")


if __name__ == "__main__":
    main()
