#!/usr/bin/env python3
"""Register the bounded open-weight release proof consumer."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_open_weight_release_review.py"
ARTIFACTS = [
    "lean/AsiStackProofs/OpenWeightReleaseReview.lean",
    "scripts/validate_open_weight_release_review.py",
    "scripts/register_open_weight_release_review.py",
    "tests/fixtures/proof_models/open_weight_release_dossier.json",
    "chapters/open-weight-release-and-post-release-control.qmd",
    "evidence_quality/proof_model_dossiers/open-weight-release-and-post-release-control.md",
    "proofs/proof_manifest.json",
    "proofs/proof_triage.json",
]


def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    registry["units"] = [unit for unit in registry["units"] if unit.get("script") != SCRIPT]
    used = {unit["order"] for unit in registry["units"]}
    order = next(value for value in range(1, len(registry["units"]) + 2) if value not in used)
    registry["units"].append({
        "id": f"{SCRIPT}:{order}", "order": order, "script": SCRIPT, "args": [],
        "execution_tier": "pr", "validation_class": "proof_or_evidence_gate",
        "input_contract": "One six-step authored open-weight review, 36 admission axes, two monotonicity laws, two non-identifiability witness pairs, and exact canonical bindings.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Independently re-encode all dossier predicates and repairs, reject 36 mutations, check frontier and public-copy monotonicity, reconstruct both information-loss collisions, and preserve the no-release boundary.",
        "output_assertions": ["36/36 exact repairs", "19 Lean declarations", "frontier expiry remains rejecting", "positive public copies remain incompatible with universal recall", "official lineage cannot recover copy control", "default evaluation cannot recover derivative safeguard state", "support effect none"],
        "claim_scope": "Finite authored release-review semantics, two arithmetic order properties, and two bounded non-identifiability results only.",
        "negative_controls": "validator_owned_thirty_six_admission_mutations_two_monotonicity_controls_and_two_collision_pairs",
        "negative_control_cases": ["artifact omission", "comparator or frontier omission", "derivative-test omission", "distribution omission", "false recall or telemetry claim", "release or support request", "lineage collision", "default-evaluation collision"],
        "prohibited_inference": "No theorem authorizes release or establishes recall, telemetry, copy erasure, license enforcement, derivative safety, benefit, risk, support, transfer, deployment, AGI, or ASI.",
        "contract_precision": "exact",
        "semantic_review_state": "manual_staged_open_weight_lifecycle_mutation_monotonicity_impossibility_and_no_release_boundary_reviewed",
    })
    for artifact in ARTIFACTS:
        if artifact not in registry["required_artifacts"]: registry["required_artifacts"].append(artifact)
    registry["units"].sort(key=lambda unit: unit["order"])
    registry["summary"] = {"required_artifact_count": len(registry["required_artifacts"]), "unit_count": len(registry["units"])}
    REGISTRY.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
    print(f"Registered {SCRIPT}: {registry['summary']['unit_count']} units, {registry['summary']['required_artifact_count']} artifacts.")


if __name__ == "__main__": main()
