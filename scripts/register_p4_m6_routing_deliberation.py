#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_p4_m6_routing_deliberation.py"
ARTIFACTS = [
    "scripts/build_p4_m6_routing_deliberation_campaign.py",
    "scripts/build_p4_m6_instrument_repair_v2.py",
    "scripts/run_p4_m6_model_generation.py",
    "scripts/evaluate_p4_m6_routing_deliberation.py",
    "scripts/validate_p4_m6_routing_deliberation.py",
    "experiments/p4_routing_deliberation/design.json",
    "experiments/p4_routing_deliberation/preregistration.json",
    "experiments/p4_routing_deliberation/instrument_repair_v2.json",
    "experiments/p4_routing_deliberation/instrument_qualification_v2.json",
    "experiments/p4_routing_deliberation/tasks.json",
    "experiments/p4_routing_deliberation/labels.json",
    "experiments/p4_routing_deliberation/router_training.json",
    "experiments/p4_routing_deliberation/raw/heldout_candidates.json",
    "experiments/p4_routing_deliberation/results/confirmatory_result.json",
    "evidence_transitions/post_v2_3/routing_deliberation_mixed_no_promotion.json",
]


def main() -> None:
    value = json.loads(REGISTRY.read_text(encoding="utf-8"))
    existing = next((row for row in value["units"] if row.get("script") == SCRIPT), None)
    value["units"] = [row for row in value["units"] if row.get("script") != SCRIPT]
    used = {row["order"] for row in value["units"]}
    preferred = existing.get("order") if existing else None
    order = preferred if preferred and preferred not in used else next(i for i in range(1, len(value["units"]) + 2) if i not in used)
    value["units"].append({
        "id": f"{SCRIPT}:{order}", "order": order, "script": SCRIPT, "args": [], "execution_tier": "pr",
        "validation_class": "proof_or_evidence_gate",
        "input_contract": "Prospectively frozen balanced 32-task held-out corpus, one exact local model snapshot, v1 failed and v2 qualified instrument lineage, shared candidate bytes, eight matched routing policies, four matched-budget stopping policies, two route and two outcome evaluators, a separate effect observer, seventeen active control classes, and fifteen preserved historical harm regressions.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Reject frozen-digest drift, instrument-failure erasure, denominator changes, control omissions, evaluator disagreement, policy or deliberation summary changes, unsafe-tradeoff erasure, harm erasure, denominator reopening, transfer laundering, or support promotion.",
        "output_assertions": [
            "v1 1/4 instrument failure and v2 4/4 qualification both remain visible",
            "32/32 held-out candidates admitted across eight tracks and four ingress modes",
            "all seventeen control classes remain covered and mutated controls are rejected",
            "full reflexive route records 31 route-correct, 21 useful, one wrong-fast, and two unsafe outputs",
            "fixed deliberation records three corruptions and two repairs",
            "all fifteen historical harms remain regression-only without new model calls",
            "mixed safety/usefulness tradeoff yields no support promotion"
        ],
        "claim_scope": "One authored held-out corpus, one quantized local Qwen3-8B snapshot, internally separate deterministic evaluators, and contained local effect probes only.",
        "negative_controls": "validator_owned_seventeen_control_and_five_disposition_mutations",
        "negative_control_cases": ["17 control coverage erasures", "unsafe tradeoff erasure", "useful-outcome inflation", "fixed-harm erasure", "denominator reopening", "transfer laundering"],
        "prohibited_inference": "Does not establish safe or general routing, useful test-time scaling, external evaluator independence, transfer, deployment, SOTA, AGI, ASI, publication, release, a new chapter, or chapter-core support.",
        "contract_precision": "exact",
        "semantic_review_state": "checked_held_out_mixed_routing_effect_and_no_promotion"
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
