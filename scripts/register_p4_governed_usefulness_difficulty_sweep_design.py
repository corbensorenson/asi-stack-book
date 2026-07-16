#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation" / "registry.json"
SCRIPT = "validate_p4_governed_usefulness_difficulty_sweep_design.py"
ARTIFACTS = [
    "scripts/validate_p4_governed_usefulness_difficulty_sweep_design.py",
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
        "input_contract": "V2-blocked draft operating-range corpus, evaluator-only rubrics, shared-candidate policy arms, four-cell evaluator canaries, effect-complete local probes, joint metrics, and confirmatory freeze boundary.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Reject task/rubric drift or leakage, candidate non-reuse, missing matched arms, weak four-cell floors, non-estimable laundering, incomplete rollback surfaces, real external effects, premature held-out work, support movement, or invented authority.",
        "output_assertions": [
            "16 draft tuning tasks across eight families and an explicit difficulty ladder",
            "shared candidate reused across baseline, record-only, full-governance, and three ablation arms",
            "two evaluator implementations agree on canaries spanning useful-safe, useful-unsafe, useless-safe, and useless-unsafe",
            "validator-owned ten-surface exact rollback plus residualized partial-recovery and omission detection",
            "held-out corpus, sample size, minimum effect, outcome denominator, support, publication, and release remain unopened",
        ],
        "claim_scope": "P4/M5 non-evidentiary difficulty-sweep design readiness only; no model output or governance/usefulness estimate.",
        "negative_controls": "validator_owned_gate_arm_reuse_cell_heldout_external_effect_and_support_mutations",
        "negative_control_cases": ["open v2 gate", "drop record-only arm", "candidate non-reuse", "weak cell floor", "premature held-out", "real external effects", "support laundering"],
        "prohibited_inference": "Does not establish actual task difficulty, four-cell occupancy, evaluator validity beyond canaries, governance usefulness, safety, rollback completeness outside validator probes, causality, transfer, SOTA, chapter support, publication, or release authority.",
        "contract_precision": "exact",
        "semantic_review_state": "checked_non_evidentiary_design_waiting_v2_instrument_adequacy",
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
