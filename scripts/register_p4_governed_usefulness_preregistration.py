#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation" / "registry.json"
SCRIPT = "validate_p4_governed_usefulness_preregistration.py"
ARTIFACTS = [
    "scripts/validate_p4_governed_usefulness_preregistration.py",
    "scripts/evaluate_p4_governed_usefulness_preflight.py",
    "experiments/p4_governed_usefulness/preregistration.json",
    "experiments/p4_governed_usefulness/strong_model_access_preflight.json",
    "experiments/p4_governed_usefulness/strong_model_sacrificial_prompt.md",
    "experiments/p4_governed_usefulness/sacrificial_labels.json",
    "experiments/p4_governed_usefulness/raw/strong_model_sacrificial_preflight_v1.json",
    "experiments/p4_governed_usefulness/results/strong_model_sacrificial_preflight.json",
    "experiments/research_foundation/task_corpus.json",
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
        "input_contract": "Frozen P4/M5 public-safe strong-model sacrificial prompt and digests, evaluator-only labels, exact Chat Pro raw/result lineage, prospective adequacy thresholds, candidate-before-label scoring path, and closed downstream gates.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Reject v1 result erasure or laundering, label leakage, corpus drift, weak preflight floors, inferred claim attempts, premature tuning/confirmatory opening, privacy drift, or authorization expansion.",
        "output_assertions": [
            "six exact sacrificial tasks inherited from the frozen research foundation",
            "5/6 schema-admissibility floor and four semantically correct admissible decisions",
            "zero evaluator disagreement and no outcome-aware retry",
            "difficulty-sweep and confirmatory denominators remain closed",
            "one Chat Pro / GPT-5.6 Sol response with 6/6 schema-admissible, 1/6 exact, terminal instrument failure, and no account identifier",
        ],
        "claim_scope": "P4/M5 v1 answer-channel instrument failure only; no governance/usefulness claim result.",
        "negative_controls": "validator_owned_support_heldout_floor_claim_confirmatory_and_authority_mutations",
        "negative_control_cases": ["support laundering", "held-out opening", "weak adequacy floor", "claim-attempt laundering", "premature confirmatory opening", "invented submission authority"],
        "prohibited_inference": "Does not establish model identity beyond the displayed UI label, model capability, usefulness, safety, governance efficacy, rollback completeness, causality, transfer, SOTA, AGI, ASI, chapter support, publication, or release authority.",
        "contract_precision": "exact",
        "semantic_review_state": "checked_terminal_v1_instrument_failure_not_claim_evidence",
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
