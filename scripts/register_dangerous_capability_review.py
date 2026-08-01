#!/usr/bin/env python3
"""Register the dangerous-capability dossier proof consumer."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation" / "registry.json"
SCRIPT = "validate_dangerous_capability_review.py"
ARTIFACTS = [
    "lean/AsiStackProofs/DangerousCapabilityReview.lean",
    "scripts/validate_dangerous_capability_review.py",
    "scripts/register_dangerous_capability_review.py",
    "tests/fixtures/proof_models/dangerous_capability_dossier.json",
    "chapters/dangerous-capability-domains-and-misuse-uplift.qmd",
    "evidence_quality/proof_model_dossiers/dangerous-capability-domains-and-misuse-uplift.md",
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
        "input_contract": "The seven-stage finite dossier model, 29 admission axes, two monotonic rejection laws, aggregate-score collision, exact chapter boundary, generated proof manifest, and reviewed triage record.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Independently derive the complete harmless-analogue route, mutate all 29 admission axes, require exact repair or refusal routes, check expiry and denominator monotonicity, reconstruct the scalar collision, verify all 20 Lean declarations and canonical bindings, and reject dangerous-capability or safety overclaims.",
        "output_assertions": [
            "complete dossier routes only to Project Theseus harmless-analogue campaign eligibility",
            "29/29 admission-axis mutations reject readiness",
            "all 29 mutations reach exact repair or refusal routes",
            "two arithmetic monotonicity controls pass",
            "equal scalar totals require opposite component-sensitive review decisions",
            "20 exact Lean declarations exist",
            "zero dangerous-capability, uplift, safeguard-efficacy, harm, safety, support, release, transfer, or external-effect claim",
        ],
        "claim_scope": "Finite authored pre-campaign dossier review semantics, arithmetic order properties, and aggregate-score non-identifiability only.",
        "negative_controls": "validator_owned_twenty_nine_admission_axis_mutations_two_monotonicity_controls_and_scalar_collision",
        "negative_control_cases": [
            "missing model/checkpoint/scaffold/tool identity",
            "stale threat model or collapsed domains",
            "missing cohort, expertise, safeguard, or baseline binding",
            "failed elicitation, control, validity, attempt, axis-separation, or evaluator gate",
            "missing information-hazard custody, uncertainty, currentness, maximum inference, residual, or non-claim boundary",
            "requested support assignment, release authority, or operational-detail publication",
            "worsened expiry or attempt-retention shortfall",
            "equal aggregate score with opposite component-sensitive decisions",
        ],
        "prohibited_inference": "No theorem or consumer establishes dangerous capability, actor uplift, safeguard efficacy, realized harm, safety, a threshold crossing, support transition, release, transfer, external effect, deployment, AGI, or ASI.",
        "contract_precision": "exact",
        "semantic_review_state": "manual_staged_dossier_mutation_monotonicity_scalar_impossibility_and_no_capability_boundary_reviewed",
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
