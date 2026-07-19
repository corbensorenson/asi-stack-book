#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_p4_m7_update_unlearning_v3.py"
ARTIFACTS = [
    "scripts/build_p4_m7_update_unlearning_campaign.py",
    "scripts/run_p4_m7_update_unlearning.py",
    "scripts/evaluate_p4_m7_update_unlearning.py",
    "scripts/validate_p4_m7_update_unlearning.py",
    "experiments/p4_update_unlearning/v1_failure_diagnosis.json",
    "scripts/build_p4_m7_update_unlearning_v2_campaign.py",
    "scripts/run_p4_m7_update_unlearning_v2.py",
    "scripts/validate_p4_m7_update_unlearning_v2_design.py",
    "experiments/p4_update_unlearning_v2/preflight_failure_diagnosis.json",
    "scripts/validate_p4_m7_update_unlearning_failure_lineage.py",
    "scripts/build_p4_m7_update_unlearning_v3_campaign.py",
    "scripts/run_p4_m7_update_unlearning_v3.py",
    "scripts/evaluate_p4_m7_update_unlearning_v3.py",
    "scripts/validate_p4_m7_update_unlearning_v3.py",
    "experiments/p4_update_unlearning_v3/preregistration.json",
    "experiments/p4_update_unlearning_v3/results/confirmatory_result.json",
    "evidence_transitions/post_v2_3/update_unlearning_claim_narrowed_after_full_attempt.json",
    "docs/p4_update_unlearning_campaign.md",
]


def main() -> None:
    value = json.loads(REGISTRY.read_text(encoding="utf-8"))
    existing = next((row for row in value["units"] if row.get("script") == SCRIPT), None)
    value["units"] = [row for row in value["units"] if row.get("script") != SCRIPT]
    used = {row["order"] for row in value["units"]}; preferred = existing.get("order") if existing else None
    order = preferred if preferred and preferred not in used else next(i for i in range(1, len(value["units"]) + 2) if i not in used)
    value["units"].append({
        "id": f"{SCRIPT}:{order}", "order": order, "script": SCRIPT, "args": [], "execution_tier": "pr",
        "validation_class": "proof_or_evidence_gate",
        "input_contract": "Two preserved instrument failures followed by one terminal prospectively frozen 870-record structured-fusion campaign over five seeds, seven arms, eight nonfungible claim axes, 24 declared state surfaces, sequential deletion, closed checkpoints, internal evaluator separation, local storage probes, and remote/external residuals.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Reject failure erasure, frozen-lineage drift, denominator changes, target inadequacy, axis merging, state truncation, false rollback, total-erasure laundering, remote or external closure invention, language-model-unlearning inflation, or chapter-core promotion.",
        "output_assertions": [
            "v1 held-out instrument failure and v2 unopened preflight failure remain visible",
            "terminal deletion-aware retraining exceeds the frozen 0.80 deletion target floor",
            "five seeds and seven arms preserve best/final authority and sequential deletion",
            "all 24 declared local surfaces restore exactly in every arm/seed transaction",
            "all eight claim axes have separate terminal dispositions",
            "retained research evidence and unresolved remote/external surfaces block total erasure",
            "claim outcome is narrowed after full attempt with no core promotion"
        ],
        "claim_scope": "One authored custody corpus, one frozen local Qwen representation snapshot, one structured nonlinear head, local serialized state and deletion probes, and internal evaluator separation only.",
        "negative_controls": "validator_owned_eight_axis_and_seven_terminal_mutations_plus_design_controls",
        "negative_control_cases": ["axis deletion", "failure-lineage erasure", "state truncation", "false rollback", "total erasure", "external erasure", "core promotion", "language-model laundering"],
        "prohibited_inference": "Does not establish language-model unlearning, zero influence, privacy, legal compliance, complete erasure, transfer, production rollback, SOTA, AGI, ASI, release, publication, or chapter-core support.",
        "contract_precision": "exact",
        "semantic_review_state": "checked_terminal_m7_claim_narrowing_and_failure_lineage"
    })
    required = list(value["required_artifacts"])
    for artifact in ARTIFACTS:
        if artifact not in required: required.append(artifact)
    value["units"].sort(key=lambda row: row["order"]); value["required_artifacts"] = required; value["summary"] = {"required_artifact_count": len(required), "unit_count": len(value["units"])}
    REGISTRY.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    print(f"Registered {SCRIPT}: {len(value['units'])} units, {len(required)} artifacts.")


if __name__ == "__main__": main()
