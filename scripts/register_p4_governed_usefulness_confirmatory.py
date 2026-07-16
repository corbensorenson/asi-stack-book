#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REGISTRY=ROOT/"validation"/"registry.json"
SCRIPT="validate_p4_governed_usefulness_confirmatory.py"
ARTIFACTS=[
    "scripts/validate_p4_governed_usefulness_confirmatory.py",
    "scripts/run_p4_governed_usefulness_confirmatory.py",
    "scripts/evaluate_p4_governed_usefulness_tuning_pool.py",
    "experiments/p4_governed_usefulness/difficulty_sweep_v2_v5_pool_preregistration.json",
    "experiments/p4_governed_usefulness/results/difficulty_sweep_v2_v5_pool_result.json",
    "experiments/p4_governed_usefulness/confirmatory_design.json",
    "experiments/p4_governed_usefulness/confirmatory_tasks.json",
    "experiments/p4_governed_usefulness/confirmatory_rubrics.json",
    "experiments/p4_governed_usefulness/confirmatory_generation_preregistration.json",
    "experiments/p4_governed_usefulness/raw/confirmatory_qwen3_8b_run_001_candidates.json",
    "experiments/p4_governed_usefulness/results/confirmatory_result.json",
    "evidence_transitions/post_v2_3/governed_usefulness_held_out_local_promote.json",
    "docs/p4_governed_usefulness_campaign.md",
    "docs/non_core_evidence_ledger.md",
    "appendices/C_claim_evidence_matrix.qmd",
    "roadmap_records/post_v2_3_claim_proof_and_sota_challenge_status.json",
]

def main()->None:
    value=json.loads(REGISTRY.read_text(encoding="utf-8")); existing=next((r for r in value["units"] if r.get("script")==SCRIPT),None)
    value["units"]=[r for r in value["units"] if r.get("script")!=SCRIPT]; used={r["order"] for r in value["units"]}; preferred=existing.get("order") if existing else None
    order=preferred if preferred and preferred not in used else next(i for i in range(1,len(value["units"])+2) if i not in used)
    value["units"].append({"id":f"{SCRIPT}:{order}","order":order,"script":SCRIPT,"args":[],"execution_tier":"pr","validation_class":"proof_or_evidence_gate","input_contract":"Prospectively pooled tuning gate, disjoint fixed held-out corpus, one identity-pinned local model run, shared policy candidates, two evaluator implementations, effect probes, co-primary gate, and bounded evidence transition.","input_artifacts":ARTIFACTS,"output_contract":"Reject tuning-pool drift, held-out reuse, digest or ordering drift, evaluator disagreement, arm-summary inflation, unsafe-ablation erasure, denominator reopening, transfer laundering, chapter-core promotion, or roadmap mismatch.","output_assertions":["32/40 pooled tuning candidates pass every frozen operating-range gate","16 held-out tasks are identity and scenario/request disjoint from tuning","15/16 confirmatory candidates are admitted with zero evaluator disagreement","full governance releases 9 useful and 0 unsafe candidates","evidence-freshness ablation exposes one useful-unsafe release","all six co-primary gates pass","one bounded non-core synthetic-test-backed transition is reconciled while every chapter core remains argument","M5 is terminal and M6 is active"],"claim_scope":"One authored held-out local corpus, one quantized Qwen3-8B run, and one frozen policy implementation only.","negative_controls":"validator_owned_denominator_arm_ceiling_and_transfer_mutations","negative_control_cases":["exclusion erasure","useful-release inflation","unsafe-ablation erasure","transfer laundering","denominator reopening","evaluator four-cell canaries","authority-ablation canary"],"prohibited_inference":"Does not establish model/workload transfer, deployed policy behavior, general safety, effect-complete rollback, external independence, acceptable governance cost, SOTA, AGI, ASI, publication, release, or any chapter-core promotion.","contract_precision":"exact","semantic_review_state":"checked_held_out_confirmatory_terminal_bounded_non_core_support"})
    required=list(value["required_artifacts"])
    for artifact in ARTIFACTS:
        if artifact not in required: required.append(artifact)
    value["units"].sort(key=lambda r:r["order"]); value["required_artifacts"]=required; value["summary"]={"required_artifact_count":len(required),"unit_count":len(value["units"])}
    REGISTRY.write_text(json.dumps(value,indent=2)+"\n",encoding="utf-8"); print(f"Registered {SCRIPT}: {len(value['units'])} units, {len(required)} artifacts.")

if __name__=="__main__": main()
