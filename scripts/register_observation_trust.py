#!/usr/bin/env python3
"""Register the observation-trust proof consumer."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_observation_trust.py"
ARTIFACTS = [
    "lean/AsiStackProofs/ObservationTrust.lean",
    "scripts/validate_observation_trust.py",
    "scripts/register_observation_trust.py",
    "chapters/perception-sensor-fusion-and-observation-trust.qmd",
    "evidence_quality/proof_model_dossiers/perception-sensor-fusion-and-observation-trust.md",
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
        "input_contract": "The bounded pair-classification model, seven-stage observation lifecycle, exact chapter proof boundary, generated proof manifest, and reviewed triage record.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Reproduce correlated, independent, and disagreement branches plus all six accepted lifecycle transitions independently; reject pair-eligibility, stage, identity, replay, evidence-inflation, authority, use, and descendant-invalidation mutations.",
        "output_assertions": [
            "correlated agreement counts one independent item",
            "independent agreement counts two independent items",
            "disagreement remains a distinct non-promotion branch",
            "seven lifecycle stages and six accepted transitions",
            "46 exact-state lifecycle mutations reject",
            "13 pair-classification controls pass",
            "16 Lean declarations exist",
            "zero support or external-authority effect",
        ],
        "claim_scope": "Finite declared-dependence accounting and authored observation-record custody only.",
        "negative_controls": "validator_owned_forty_six_lifecycle_mutations_and_thirteen_pair_controls",
        "negative_control_cases": [
            "ineligible channel fields", "dependence-root mutation",
            "hypothesis mutation", "wrong-stage transitions",
            "identity substitution", "event replay",
            "support or authority laundering", "environmental-truth overclaim",
            "correlated count inflation", "erased disagreement",
            "unbounded use", "stale descendants after material change",
        ],
        "prohibited_inference": "No theorem or consumer discovers real sensor dependence, establishes calibration, synchronization, environmental truth, causal grounding, fusion quality, robustness, physical safety, readiness, release authority, transfer, SOTA, AGI, or ASI.",
        "contract_precision": "exact",
        "semantic_review_state": "manual_pair_nonpromotion_lifecycle_consumer_and_no_promotion_boundary_reviewed",
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
