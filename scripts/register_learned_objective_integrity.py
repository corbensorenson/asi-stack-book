#!/usr/bin/env python3
"""Register the learned-objective integrity proof consumer."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_learned_objective_integrity.py"
ARTIFACTS = [
    "lean/AsiStackProofs/LearnedObjectiveIntegrity.lean",
    "scripts/validate_learned_objective_integrity.py",
    "scripts/register_learned_objective_integrity.py",
    "chapters/inner-alignment-mesa-optimization-and-learned-objective-integrity.qmd",
    "evidence_quality/proof_model_dossiers/inner-alignment-mesa-optimization-and-learned-objective-integrity.md",
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
        "input_contract": "The bounded learned-objective non-identification witness, eight-stage integrity lifecycle, exact chapter proof boundary, generated proof manifest, and reviewed triage record.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Reproduce the equal-compliant-trace counterexample and all seven accepted lifecycle transitions independently; reject wrong-stage, identity, replay, objective-certainty, missing-evidence, mitigation, use, and descendant-invalidation mutations with exact state preservation.",
        "output_assertions": [
            "two equal compliant traces have distinct authored objective hypotheses",
            "a separating opportunity yields different actions",
            "eight lifecycle stages and seven accepted transitions",
            "59 exact-state mutations reject",
            "14 Lean declarations exist",
            "zero support or external-authority effect",
        ],
        "claim_scope": "Finite non-identification and authored learned-objective integrity record discipline only.",
        "negative_controls": "validator_owned_fifty_nine_identity_lifecycle_and_overclaim_mutations",
        "negative_control_cases": [
            "wrong-stage transitions", "identity substitution", "event replay",
            "support or authority laundering", "objective certainty laundering",
            "missing plural hypotheses", "missing independent evidence lanes",
            "unsealed or opportunity-free intervention", "missing concealment review",
            "missing residual hypothesis", "unbounded or unowned use",
            "stale descendants after material change",
        ],
        "prohibited_inference": "No theorem or consumer identifies a model objective, detects mesa-optimization or deception, proves evaluator competence, mitigation efficacy, alignment, safety, readiness, release authority, transfer, SOTA, AGI, or ASI.",
        "contract_precision": "exact",
        "semantic_review_state": "manual_nonidentification_lifecycle_consumer_and_no_promotion_boundary_reviewed",
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
