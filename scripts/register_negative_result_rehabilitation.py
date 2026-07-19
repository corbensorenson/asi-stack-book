#!/usr/bin/env python3
"""Register retrospective N0-N5 negative-result rehabilitation validation."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_negative_result_rehabilitation.py"
ARTIFACTS = [
    "evidence_quality/negative_result_rehabilitation.json",
    "schemas/negative_result_rehabilitation.schema.json",
    "docs/negative_result_rehabilitation.md",
    "scripts/build_negative_result_rehabilitation.py",
    "scripts/validate_negative_result_rehabilitation.py",
    "scripts/register_negative_result_rehabilitation.py",
    "evidence_quality/claim_identity_graph.json",
    "docs/claim_bearing_experiment_competence_standard.md",
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
        "input_contract": "The exact 90 accepted no-change/refuted transition denominator; immutable transition digests and raw outcomes; complete canonical identity graph; N0-N5 experiment-competence contract; and an explicit manually reviewed classification table.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Assign every accepted historical negative/no-change transition exactly one conservative N0-N5 level without inventing missing competence evidence, reopening heldout data, rewriting raw outcomes, or allowing N0-N2 results to refute target mechanisms, architectures, canonical parents, or chapter cores.",
        "output_assertions": [
            "90 of 90 accepted negative/no-change transitions classified",
            "one N0 instrument failure",
            "fifteen N1 implementation failures",
            "seventy-four N2 proxy/regime failures",
            "zero N3-N5 results",
            "zero broad or chapter-core negative inference",
            "twelve mutations reject"
        ],
        "claim_scope": "Retrospective maximum-negative-inference classification for accepted transition records only.",
        "negative_controls": "validator_owned_twelve_history_competence_and_inference_mutations",
        "negative_control_cases": [
            "negative record deletion", "historical label rewrite", "transition digest rewrite",
            "N0 inference widening", "N1 inference widening", "N2 inference widening",
            "N3 invention", "broad inference escape", "heldout reopen",
            "posthoc evidence invention", "raw limitation deletion", "support promotion"
        ],
        "prohibited_inference": "N0-N2 rehabilitation does not prove an idea false or true, establish implementation competence, promote support, validate an evaluator, create reproduction or transfer, or establish safety, SOTA, AGI, ASI, publication, deployment, or release readiness.",
        "contract_precision": "exact",
        "semantic_review_state": "manual_transition_identity_scope_artifact_limit_and_competence_review_with_immutable_history"
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
