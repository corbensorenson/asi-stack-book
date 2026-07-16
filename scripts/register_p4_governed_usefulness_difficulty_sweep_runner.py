#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation" / "registry.json"
SCRIPT = "validate_p4_governed_usefulness_difficulty_sweep_runner.py"
ARTIFACTS = [
    "scripts/run_p4_governed_usefulness_difficulty_sweep.py",
    "scripts/validate_p4_governed_usefulness_difficulty_sweep_runner.py",
    "experiments/p4_governed_usefulness/difficulty_sweep_design.json",
    "experiments/p4_governed_usefulness/difficulty_sweep_tasks_draft.json",
    "experiments/p4_governed_usefulness/difficulty_sweep_rubrics_draft.json",
    "experiments/p4_governed_usefulness/difficulty_sweep_candidate_prompt_template.md",
    "experiments/p4_governed_usefulness/preregistration_v2.json",
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
        "input_contract": "Hard-gated tuning runner, candidate-only prompt/vocabularies, candidate-before-rubric closure, matched policy routing, four-cell evaluator self-test, and temporary effect probes.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Reject normal execution without passing v2 plus a post-v2 frozen tuning design, malformed or out-of-vocabulary candidates, non-shared policy candidates, evaluator leakage, incomplete effect probes, confirmatory reuse, or support movement.",
        "output_assertions": [
            "the first tuning identity is terminally closed after its non-estimable result",
            "candidate prompt is tuning-only and withholds evaluator rubrics",
            "self-test spans all four usefulness/safety cells with zero evaluator disagreement",
            "five local effect probes include one retained partial-recovery residual",
            "six malformed-candidate mutations reject and matched policy routing isolates authority ablation",
            "the first difficulty-sweep result remains non-estimable and non-evidentiary",
        ],
        "claim_scope": "P4/M5 first-tuning execution-harness and terminal non-estimable-result integrity only; self-tests and tuning remain non-evidentiary.",
        "negative_controls": "validator_owned_run_enum_vocabulary_duplicate_type_key_and_gate_controls",
        "negative_control_cases": ["missing v2 gate", "wrong run", "bad enum", "out of vocabulary", "duplicate token", "nonboolean completion", "missing key", "matched authority ablation"],
        "prohibited_inference": "Does not establish task difficulty, model capability, operating-range occupancy, evaluator validity beyond canaries, governance usefulness, safety, rollback completeness beyond temporary probes, causality, transfer, chapter support, publication, or release authority.",
        "contract_precision": "exact",
        "semantic_review_state": "checked_self_tested_first_tuning_runner_terminally_closed_after_non_estimable_result",
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
