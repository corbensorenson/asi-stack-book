#!/usr/bin/env python3
"""Register the finite embodied control-lease proof consumer."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_embodied_physical_safety.py"
ARTIFACTS = [
    "lean/AsiStackProofs/EmbodiedPhysicalSafety.lean",
    "scripts/validate_embodied_physical_safety.py",
    "scripts/register_embodied_physical_safety.py",
    "tests/fixtures/proof_models/embodied_control_lease.json",
    "chapters/embodied-agency-real-time-control-and-physical-safety.qmd",
    "evidence_quality/proof_model_dossiers/embodied-agency-real-time-control-and-physical-safety.md",
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
        "input_contract": "The finite control-lease model, 13 admission axes, three arithmetic monotonicity laws, exact chapter boundary, generated proof manifest, and reviewed triage record.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Independently derive the complete trial route, mutate all 13 admission axes, require exact repair routes, check three monotonicity controls, verify all 22 Lean declarations and canonical bindings, and reject plant or safety overclaims.",
        "output_assertions": [
            "complete lease routes only to Project Theseus closed-loop trial eligibility",
            "13/13 admission-axis mutations reject readiness",
            "all 13 mutations reach exact repair routes",
            "three arithmetic monotonicity controls pass",
            "22 exact Lean declarations exist",
            "zero plant-truth, physical/human-safety, deadline, safe-set, fallback-effectiveness, recovery, support, release, transfer, or external-effect claim",
        ],
        "claim_scope": "Finite authored control-lease admission semantics and arithmetic order properties only.",
        "negative_controls": "validator_owned_thirteen_admission_axis_mutations_and_three_monotonicity_controls",
        "negative_control_cases": [
            "missing command request", "missing plant identity", "stale lease version",
            "expired lease", "stale observation", "state-envelope violation",
            "timing-budget violation", "actuator-envelope violation",
            "unreachable fallback", "missing independent stop",
            "missing effect observation", "missing residual custody",
            "missing non-claim boundary", "worsened state or fallback bounds",
        ],
        "prohibited_inference": "No theorem or consumer establishes plant truth, physical or human safety, real deadline satisfaction, safe-set validity, fallback effectiveness, recovery, support transition, release, transfer, external effect, deployment, AGI, or ASI.",
        "contract_precision": "exact",
        "semantic_review_state": "manual_derived_control_lease_mutation_monotonicity_and_no_physical_safety_boundary_reviewed",
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
