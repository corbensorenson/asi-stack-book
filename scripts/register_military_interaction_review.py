#!/usr/bin/env python3
"""Register the non-operational military-interaction proof consumer."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation" / "registry.json"
SCRIPT = "validate_military_interaction_review.py"
ARTIFACTS = [
    "lean/AsiStackProofs/MilitaryInteractionReview.lean",
    "scripts/validate_military_interaction_review.py",
    "scripts/register_military_interaction_review.py",
    "tests/fixtures/proof_models/military_interaction_dossier.json",
    "chapters/military-ai-autonomous-weapons-and-strategic-stability.qmd",
    "evidence_quality/proof_model_dossiers/military-ai-autonomous-weapons-and-strategic-stability.md",
    "proofs/proof_manifest.json",
    "proofs/proof_triage.json",
]


def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    registry["units"] = [unit for unit in registry["units"] if unit.get("script") != SCRIPT]
    used = {unit["order"] for unit in registry["units"]}
    order = next(value for value in range(1, len(registry["units"]) + 2) if value not in used)
    registry["units"].append({
        "id": f"{SCRIPT}:{order}",
        "order": order,
        "script": SCRIPT,
        "args": [],
        "execution_tier": "pr",
        "validation_class": "proof_or_evidence_gate",
        "input_contract": "The eight-step public-safe military-interaction lifecycle, 45 admission axes, three monotonic rejection laws, two non-identifiability witness pairs, exact chapter boundary, generated proof manifest, and reviewed triage record.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Independently derive the complete public-safe simulation route, mutate all 45 admission axes, require exact repair or refusal dispositions, check expiry, decision-time, and off-ramp monotonicity, reconstruct both impossibility collisions, verify all 24 Lean declarations and canonical bindings, and reject weapon, lawful-use, control, or stability overclaims.",
        "output_assertions": [
            "complete dossier routes only to Project Theseus public-safe simulation eligibility",
            "45/45 admission-axis mutations reject readiness and simulation eligibility",
            "all 45 mutations receive exact repair or refusal dispositions",
            "three arithmetic monotonicity controls pass",
            "same human-interface presence can require opposite meaningful-judgment decisions",
            "identical component evidence can require opposite strategic-interaction reviews",
            "24 exact Lean declarations exist",
            "zero weapon-authorization, lawful-use, meaningful-control, escalation-reduction, strategic-stability, safety, support, release, transfer, or external-effect claim",
        ],
        "claim_scope": "Finite authored non-operational dossier review semantics, arithmetic order properties, and two bounded non-identifiability results only.",
        "negative_controls": "validator_owned_forty_five_admission_axis_mutations_three_monotonicity_controls_and_two_collision_pairs",
        "negative_control_cases": [
            "missing public-safe scope, mission, role, population, or legal boundary",
            "missing accountable authority or effect envelope, or requested authority expansion",
            "ceremonial interface lacking time, information, competence, attention, intervention, alternatives, or independent judgment",
            "missing provenance, dependency, uncertainty, corroboration, abstention, degraded posture, or suspension fields",
            "missing adversary, doctrine, reciprocal-effect, off-ramp, or proliferation-residual fields",
            "missing independent review, restricted custody, currentness, public inference, remedy, decommission, residual, or non-claim boundary",
            "requested weapon authorization, lawful-use or stability claim, support, release, or operational-detail publication",
            "worsened expiry, decision-time, or off-ramp shortfall",
            "same-interface and same-component-evidence collisions with opposite decisions",
        ],
        "prohibited_inference": "No theorem or consumer authorizes a weapon or establishes lawful use, meaningful human control in practice, escalation reduction, strategic stability, safety, support transition, release, transfer, external effect, deployment, AGI, or ASI.",
        "contract_precision": "exact",
        "semantic_review_state": "manual_staged_non_operational_dossier_mutation_monotonicity_two_impossibility_and_no_authorization_boundary_reviewed",
    })
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
