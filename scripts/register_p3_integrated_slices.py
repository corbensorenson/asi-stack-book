#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation" / "registry.json"
SCRIPT = "validate_p3_integrated_slices.py"
ARTIFACTS = [
    "scripts/validate_p3_integrated_slices.py",
    "experiments/p3_integrated_slices/results/2026-07-16-local.json",
    "docs/p3_integrated_executable_slices.md",
    "evidence_transitions/post_v2_3/instrument_failure_supersession.json",
    "experiments/post_v2_governed_work_flagship/results/2026-07-10-local.json",
    "experiments/post_v2_governed_work_flagship/artifacts/model_outputs/t01_clamp_budget-seed-17.py",
    "experiments/post_v2_governed_work_flagship/artifacts/model_outputs/t01_clamp_budget-seed-17.raw.txt",
    "experiments/post_v2_update_causality/results/2026-07-10-local.json",
    "experiments/post_v2_update_causality/checkpoints/seed-17-base-final.pt",
    "experiments/post_v2_update_causality/checkpoints/seed-17-bounded_finetune-best.pt",
    "experiments/safety_case_assurance/results/2026-07-13-local.json",
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
        "id": f"{SCRIPT}:{order}", "order": order, "script": SCRIPT, "args": [], "execution_tier": "deep", "validation_class": "behavioral_fixture",
        "input_contract": "One versioned interface over retained real governed-work model outputs, real trained checkpoint bytes, safety-case routes, temporary local effects, an observation/interpretation/belief trace, and a sealed quiescent epoch.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Replay and reject identity, status, effect-observation, rollback, epistemic-lineage, in-flight, mutation, injection-escape, support, and instrument-supersession laundering.",
        "output_assertions": [
            "twelve cases cover all ten required lifecycle statuses across three slices",
            "six actual local effects are independently observed, including three exact rollbacks, one residualized partial effect, and one quarantine",
            "twenty of twenty named boundary failure injections remain contained",
            "one raw observation preserves competing interpretations through a belief decision and sealed full-state quiescent epoch",
            "two 2026-07-13 instrument-limited transitions have immutable superseding protocol lineage",
            "eleven negative mutations reject with no support or external-action authority",
        ],
        "claim_scope": "Bounded local interoperability, effect accounting, epistemic lineage, and one-process stabilization only.",
        "negative_controls": "validator_owned_source_status_effect_rollback_observation_interpretation_memory_inflight_mutation_injection_and_support_controls",
        "negative_control_cases": ["source substitution","status omission","unobserved effect","rollback-count laundering","mutable observation","interpretation collapse","memory-lineage erasure","in-flight laundering","undeclared mutation","failure injection escape","support promotion"],
        "prohibited_inference": "Does not establish fresh model quality, evaluator validity, open-world effect completeness, deployed rollback, distributed stabilization, useful throughput, safety, reproduction, transfer, SOTA, AGI, ASI, release, publication, or chapter-core support.",
        "contract_precision": "exact", "semantic_review_state": "checked_bounded_integrated_real_output_local_effect_replay_not_deployed_or_support_authority"
    })
    required = list(value["required_artifacts"])
    for artifact in ARTIFACTS:
        if artifact not in required: required.append(artifact)
    value["units"].sort(key=lambda row: row["order"])
    value["required_artifacts"] = required
    value["summary"] = {"required_artifact_count":len(required),"unit_count":len(value["units"])}
    REGISTRY.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    print(f"Registered {SCRIPT}: {len(value['units'])} units, {len(required)} artifacts.")


if __name__ == "__main__": main()
