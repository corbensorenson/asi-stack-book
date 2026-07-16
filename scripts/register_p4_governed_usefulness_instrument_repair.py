#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation" / "registry.json"
SCRIPT = "validate_p4_governed_usefulness_instrument_repair.py"
ARTIFACTS = [
    "scripts/validate_p4_governed_usefulness_instrument_repair.py",
    "scripts/evaluate_p4_governed_usefulness_preflight_v2.py",
    "experiments/p4_governed_usefulness/raw/strong_model_sacrificial_preflight_v1.json",
    "experiments/p4_governed_usefulness/results/strong_model_sacrificial_preflight.json",
    "experiments/p4_governed_usefulness/v1_failure_diagnosis.json",
    "experiments/p4_governed_usefulness/preregistration_v2.json",
    "experiments/p4_governed_usefulness/strong_model_sacrificial_prompt_v2.md",
    "experiments/p4_governed_usefulness/sacrificial_labels_v2.json",
    "docs/p4_governed_usefulness_campaign.md",
    "roadmap_records/post_v2_3_claim_proof_and_sota_challenge_status.json",
]


def main() -> None:
    value = json.loads(REGISTRY.read_text(encoding="utf-8"))
    existing = next((row for row in value["units"] if row.get("script") == SCRIPT), None)
    value["units"] = [row for row in value["units"] if row.get("script") != SCRIPT]
    used = {row["order"] for row in value["units"]}
    preferred = existing.get("order") if existing else None
    order = preferred if preferred and preferred not in used else next(index for index in range(1, len(value["units"]) + 2) if index not in used)
    value["units"].append({
        "id": f"{SCRIPT}:{order}",
        "order": order,
        "script": SCRIPT,
        "args": [],
        "execution_tier": "pr",
        "validation_class": "proof_or_evidence_gate",
        "input_contract": "Immutable v1 Chat Pro raw/result lineage plus a prospectively frozen v2 canonical-decision repair with evaluator-only task mappings.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Reject v1 rescoring or erasure, same-identity retry, weak v2 floors, free-text exact-match scoring, premature outcome denominators, or invented submission/support authority.",
        "output_assertions": [
            "v1 remains 6/6 schema-admissible, 1/6 exact, and instrument_inadequate_recampaign_required",
            "v2 uses a new protocol identity and frozen six-class decision/seven-class residual taxonomy",
            "v2 requires 5/6 schema-admissible and 5/6 exact canonical decisions with zero evaluator disagreement",
            "difficulty sweep and confirmatory denominator remain closed",
            "no retrospective rescore, claim attempt, support, publication, or release authority",
        ],
        "claim_scope": "P4/M5 instrument-failure lineage and prospective repair only; no governance/usefulness result.",
        "negative_controls": "validator_owned_rescore_identity_floor_freetext_sweep_and_authority_mutations",
        "negative_control_cases": ["retrospective rescore", "same protocol identity", "weak semantic floor", "free-text route scoring", "premature sweep", "invented v2 authority"],
        "prohibited_inference": "Does not establish model capability, usefulness, safety, governance efficacy, rollback, causality, transfer, SOTA, AGI, ASI, chapter support, publication, or release authority.",
        "contract_precision": "exact",
        "semantic_review_state": "checked_v1_instrument_failure_and_prospective_v2_repair_not_claim_evidence",
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
