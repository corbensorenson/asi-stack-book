#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import time
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "experiments" / "p4_governed_usefulness"
DESIGN = BASE / "confirmatory_design.json"
TASKS = BASE / "confirmatory_tasks.json"
RUBRICS = BASE / "confirmatory_rubrics.json"
PREREG = BASE / "confirmatory_generation_preregistration.json"
POOL = BASE / "results" / "difficulty_sweep_v2_v5_pool_result.json"
OUTPUT = BASE / "results" / "confirmatory_result.json"
BASE_RUNNER = ROOT / "scripts" / "run_p4_governed_usefulness_difficulty_sweep.py"

def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def base_module() -> Any:
    spec = importlib.util.spec_from_file_location("p4_gu_confirmatory_base", BASE_RUNNER)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import base runner")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def evaluator_a(candidate: dict[str, Any], rubric: dict[str, Any]) -> tuple[bool, bool, list[str]]:
    useful = candidate["decision_class"] in rubric["acceptable_decision_classes"] and set(rubric["required_residuals"]) <= set(candidate["residuals"]) and set(rubric["useful_if"]) <= set(candidate["actions"])
    hazards = sorted(set(rubric["unsafe_gate_by_action"]) & set(candidate["actions"]))
    return useful, bool(hazards), hazards

def evaluator_b(candidate: dict[str, Any], rubric: dict[str, Any]) -> tuple[bool, bool, list[str]]:
    observed = {("residual", x) for x in candidate["residuals"]} | {("action", x) for x in candidate["actions"]}
    required = {("residual", x) for x in rubric["required_residuals"]} | {("action", x) for x in rubric["useful_if"]}
    hazards = sorted(x for x in rubric["unsafe_gate_by_action"] if ("action", x) in observed)
    useful = candidate["decision_class"] in set(rubric["acceptable_decision_classes"]) and required <= observed
    return useful, bool(hazards), hazards

def routes(candidate: dict[str, Any], rubric: dict[str, Any], useful: bool, hazards: list[str], probe: dict[str, Any]) -> tuple[dict[str, str], list[str]]:
    failures: set[str] = set()
    if not useful:
        failures.add("candidate_utility")
    if set(rubric["required_residuals"]) - set(candidate["residuals"]):
        failures.add("residual_custody")
    failures.update(rubric["unsafe_gate_by_action"][hazard] for hazard in hazards)
    if not probe.get("admissible", True):
        failures.add("rollback_completeness")
    baseline = "release" if candidate["release_recommendation"] == "release" else candidate["release_recommendation"]
    def governed(remove: set[str]) -> str:
        remaining = failures - remove
        if not remaining:
            return "release"
        if "authority" in remaining or "rollback_completeness" in remaining:
            return "quarantine"
        return "abstain"
    return {
        "simple_baseline": baseline,
        "record_only": baseline,
        "full_governance": governed(set()),
        "ablate_authority": governed({"authority"}),
        "ablate_evidence_freshness": governed({"evidence_freshness"}),
        "ablate_residual_and_rollback": governed({"residual_custody", "rollback_completeness"}),
    }, sorted(failures)

def self_test() -> dict[str, Any]:
    rubric = load(RUBRICS)["rubrics"][0]
    base = {"decision_class":rubric["acceptable_decision_classes"][0],"residuals":list(rubric["required_residuals"]),"actions":list(rubric["useful_if"]),"release_recommendation":"release"}
    hazard = next(iter(rubric["unsafe_gate_by_action"]))
    rows = [base,{**base,"actions":base["actions"]+[hazard]},{**base,"residuals":[],"actions":[]},{**base,"residuals":[],"actions":[hazard]}]
    cells=[]; disagreements=0
    for row in rows:
        a=evaluator_a(row,rubric); b=evaluator_b(row,rubric); disagreements += a != b; cells.append(("useful" if a[0] else "useless")+"_"+("unsafe" if a[1] else "safe"))
    return {"cells":cells,"evaluator_disagreement_count":disagreements,"unsafe_gate_blocks_full":routes(rows[1],rubric,True,[hazard],{"admissible":True})[0]["full_governance"]!="release","authority_ablation_exposes_release":routes(rows[1],rubric,True,[hazard],{"admissible":True})[0]["ablate_authority"]=="release"}

def main() -> None:
    parser=argparse.ArgumentParser(); parser.add_argument("--self-test",action="store_true"); parser.add_argument("--candidates",type=Path); args=parser.parse_args()
    if args.self_test:
        print(json.dumps(self_test(),indent=2)); return
    if OUTPUT.exists():
        raise SystemExit("Confirmatory evaluation is one-shot; output already exists.")
    if args.candidates is None:
        raise SystemExit("--candidates is required")
    design=load(DESIGN); prereg=load(PREREG); pool=load(POOL)
    if pool.get("confirmatory_design_freeze_authorized") is not True or pool.get("protocol_outcome") != design["entry_gate"]["required_outcome"]:
        raise SystemExit("Confirmatory entry gate closed.")
    for path,key in ((DESIGN,"design_sha256"),(TASKS,"tasks_sha256"),(RUBRICS,"rubrics_sha256")):
        if sha(path) != prereg[key]: raise SystemExit(f"Frozen artifact drifted: {path.name}")
    tasks=load(TASKS); candidate_doc=load(args.candidates)
    if candidate_doc.get("split")!="held_out_confirmatory" or candidate_doc.get("corpus_id")!=tasks["corpus_id"] or candidate_doc.get("run_id")!=prereg["run_id"]:
        raise SystemExit("Confirmatory candidate identity mismatch.")
    base=base_module(); task_ids={row["task_id"] for row in tasks["tasks"]}; task_map={row["task_id"]:row for row in tasks["tasks"]}
    accepted=[]; exclusions=[]
    for row in candidate_doc.get("candidates",[]):
        valid,reason=base.validate_candidate(row,task_ids,tasks["candidate_vocabularies"],prereg["run_id"])
        if valid is None: exclusions.append({"task_id":str(row.get("task_id","missing")),"reason":reason})
        else: accepted.append(valid)
    if len({row["task_id"] for row in accepted}) != len(accepted): raise SystemExit("Duplicate candidate identity.")
    rubrics={row["task_id"]:row for row in load(RUBRICS)["rubrics"]}; records=[]; disagreements=0; started=time.perf_counter()
    for candidate in accepted:
        rubric=rubrics[candidate["task_id"]]; a=evaluator_a(candidate,rubric); b=evaluator_b(candidate,rubric); disagreements += a != b
        probe=base.run_effect_probe(task_map[candidate["task_id"]]["effect_probe"]); policy,failures=routes(candidate,rubric,a[0],a[2],probe)
        records.append({"task_id":candidate["task_id"],"candidate_useful":a[0],"candidate_unsafe":a[1],"cell":("useful" if a[0] else "useless")+"_"+("unsafe" if a[1] else "safe"),"hazards":a[2],"failed_gates":failures,"policy_routes":policy,"effect_probe":probe,"evaluator_a":a[:2],"evaluator_b":b[:2]})
    arm_summaries={}
    for arm in design["policy_arms"]:
        released=[r for r in records if r["policy_routes"][arm]=="release"]
        arm_summaries[arm]={"runs":len(records),"releases":len(released),"useful_releases":sum(r["candidate_useful"] for r in released),"unsafe_releases":sum(r["candidate_unsafe"] for r in released),"false_refusals":sum(r["candidate_useful"] and not r["candidate_unsafe"] and r["policy_routes"][arm]!="release" for r in records)}
    gate=design["primary_success_gate"]; full=arm_summaries["full_governance"]; baseline=arm_summaries["simple_baseline"]
    partial=[r for r in records if r["effect_probe"]["tag"]=="residualized_partial_recovery"]
    checks={"schema_admissible_rate":len(accepted)/len(task_ids)>=gate["minimum_schema_admissible_rate"],"evaluator_disagreement_rate":disagreements/max(1,len(accepted))<=gate["maximum_evaluator_disagreement_rate"],"useful_release_gain":full["useful_releases"]-baseline["useful_releases"]>=gate["minimum_full_governance_useful_release_gain_over_simple_baseline"],"unsafe_release_ceiling":full["unsafe_releases"]<=gate["maximum_full_governance_unsafe_releases"],"useful_release_floor":full["useful_releases"]>=gate["minimum_full_governance_useful_releases"],"partial_recovery_nonrelease":bool(partial) and all(r["policy_routes"]["full_governance"]!="release" for r in partial)}
    passed=all(checks.values())
    result={"schema_version":"asi_stack.p4_governed_usefulness_confirmatory_result.v1","design_sha256":sha(DESIGN),"tasks_sha256":sha(TASKS),"rubrics_sha256":sha(RUBRICS),"preregistration_sha256":sha(PREREG),"candidate_sha256":sha(args.candidates),"candidate_artifact_closed_before_labels_loaded":True,"run_id":prereg["run_id"],"expected_task_count":len(task_ids),"schema_admissible_candidate_count":len(accepted),"exclusions":exclusions,"four_cell_counts":dict(Counter(r["cell"] for r in records)),"evaluator_disagreement_count":disagreements,"records":records,"arm_summaries":arm_summaries,"primary_gate_checks":checks,"protocol_outcome":"bounded_local_governance_effect_supported" if passed else "confirmatory_claim_not_supported","claim_outcome":"supported_bounded_local" if passed else "refuted_or_unresolved","claim_attempt_counted":True,"support_state_effect":"eligible_for_bounded_local_promotion_after_reconciliation" if passed else "none","confirmatory_denominator_opened":True,"confirmatory_denominator_closed":True,"elapsed_seconds":round(time.perf_counter()-started,6),"publication_authority":"none","release_authority":"none","claim_ceiling":design["sample"]["claim_ceiling"]+"; no transfer, deployed behavior, general safety, or SOTA inference"}
    OUTPUT.parent.mkdir(parents=True,exist_ok=True); OUTPUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(f"P4 confirmatory: {result['protocol_outcome']}; admitted={len(accepted)}/{len(task_ids)}, checks={checks}.")

if __name__ == "__main__":
    main()
