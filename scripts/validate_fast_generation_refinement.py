#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/AsiStackProofs/FastGenerationRefinement.lean"
SCHEMA = ROOT / "schemas/fast_generation_refinement.schema.json"
RESULT = ROOT / "experiments/fast_generation_refinement/results/2026-07-15-local.json"
TASK_RESULT = ROOT / "experiments/fast_generation_task_bundle/results/2026-07-02-local.json"
THESEUS_RESULT = ROOT / "experiments/theseus_generation_mode_import/results/2026-07-01-local.json"
BASELINE_FIXTURES = ROOT / "experiments/generation_mode_baselines/fixtures"
COMMAND = "python3 scripts/validate_fast_generation_refinement.py"

STAGES = ["requested", "contextBound", "modeSelected", "draftGenerated", "verified", "accounted", "decided", "closed"]
KINDS = {"requested":"bindContext","contextBound":"selectMode","modeSelected":"generateDraft","draftGenerated":"verifyDraft","verified":"accountOutcome","accounted":"decide","decided":"close","closed":"close"}
ACCEPTED = {"select_slow_baseline","activate_fallback","accept_context","accept_fast_selection","accept_generation","accept_verification","accept_accounting","accept_decision","accept_closure"}
TASK_KEYS = {"taskId","taskVersion","contextDigest","taskSetDigest","consumerDigest"}
MODE_KEYS = {"modeDigest","baselineDigest"}
RESULT_KEYS = {"resultDigest","residualDigest"}


def rel(path: Path) -> str: return str(path.relative_to(ROOT))
def load(path: Path) -> Any: return json.loads(path.read_text(encoding="utf-8"))
def sha(path: Path) -> str: return hashlib.sha256(path.read_bytes()).hexdigest()


def packet() -> dict[str, Any]:
    p: dict[str, Any] = {"taskId":3001,"taskVersion":2,"contextDigest":3002,"taskSetDigest":3003,"consumerDigest":3004,"modeDigest":3005,"baselineDigest":3006,"verifierDigest":3007,"resultDigest":3008,"residualDigest":3009,"eventDigest":91}
    true_fields = ["requestWellFormed","contextPacket","taskSet","consumer","deadline","rights","fastModeRequested","generationMode","riskTier","qualityTarget","verifierIdentity","independentEvaluator","acceptancePredicate","matchedBaseline","latencyBudget","computeMemoryBudget","riskOverride","slowFallback","highRiskReview","generator","draftArtifact","proposedOutput","generationCost","searchBound","observedVerification","verificationPassed","fallbackExecutable","fallbackResidual","acceptedOutput","qualityPass","verifierCost","fallbackCost","taskSuccess","baselineResult","usefulDenominator","costMetricSeparation","outputDigest","evidenceTransition","decisionReceipt","decisionNonClaims","consumerAcknowledgment","residualClosure","descendantReferences","resultDigestBound","cleanup"]
    false_fields = ["highRisk","rawSpeedPromotionRequested","supportPromotionRequested","externalEffectRequested"]
    p.update({k:True for k in true_fields}); p.update({k:False for k in false_fields}); return p


def state(stage: str, fallback: int = 0, last: int = 0) -> dict[str, Any]:
    p=packet(); s={k:p[k] for k in TASK_KEYS|MODE_KEYS|RESULT_KEYS|{"verifierDigest"}}; s.update({"fallbackCount":fallback,"lastEventDigest":last}); return s


def route(stage: str, kind: str, p: dict[str, Any], s: dict[str, Any] | None=None) -> str:
    s=state(stage) if s is None else s
    if kind!=KINDS[stage]: return "reject_wrong_stage"
    if any(p[k]!=s[k] for k in TASK_KEYS): return "reject_task_substitution"
    if any(p[k]!=s[k] for k in MODE_KEYS): return "reject_mode_substitution"
    if p["verifierDigest"]!=s["verifierDigest"]: return "reject_evaluator_substitution"
    if any(p[k]!=s[k] for k in RESULT_KEYS): return "reject_result_substitution"
    if p["eventDigest"]==s["lastEventDigest"]: return "reject_event_replay"
    if p["externalEffectRequested"]: return "reject_authority_leak"
    simple={
      "requested":[("requestWellFormed","reject_malformed_request"),("contextPacket","require_context_packet"),("taskSet","require_task_set"),("consumer","require_consumer"),("deadline","require_deadline"),("rights","require_rights")],
      "modeSelected":[("generator","require_generator"),("draftArtifact","require_draft_artifact"),("proposedOutput","require_proposed_output"),("generationCost","require_generation_cost"),("searchBound","require_search_bound")],
      "decided":[("consumerAcknowledgment","require_consumer_acknowledgment"),("residualClosure","require_residual_closure"),("descendantReferences","require_descendant_references"),("resultDigestBound","require_bound_result_digest"),("cleanup","require_cleanup")],
    }
    if stage in simple:
      for field,outcome in simple[stage]:
        if not p[field]: return outcome
      return {"requested":"accept_context","modeSelected":"accept_generation","decided":"accept_closure"}[stage]
    if stage=="contextBound":
      if not p["fastModeRequested"]: return "select_slow_baseline"
      for field,outcome in [("generationMode","require_generation_mode"),("riskTier","require_risk_tier"),("qualityTarget","require_quality_target"),("verifierIdentity","require_verifier_identity"),("independentEvaluator","require_independent_evaluator"),("acceptancePredicate","require_acceptance_predicate"),("matchedBaseline","require_matched_baseline"),("latencyBudget","require_latency_budget"),("computeMemoryBudget","require_compute_memory_budget")]:
        if not p[field]: return outcome
      if p["highRisk"] and not p["riskOverride"]: return "require_risk_override"
      if p["highRisk"] and not p["slowFallback"]: return "require_slow_fallback"
      if p["highRisk"] and not p["highRiskReview"]: return "require_high_risk_review"
      return "accept_fast_selection"
    if stage=="draftGenerated":
      if not p["observedVerification"]: return "require_observed_verification"
      if not p["verificationPassed"] and not p["fallbackExecutable"]: return "require_executable_fallback"
      if not p["verificationPassed"] and not p["fallbackResidual"]: return "require_fallback_residual"
      if not p["verificationPassed"]: return "activate_fallback"
      if not p["acceptedOutput"]: return "require_accepted_output"
      if not p["qualityPass"]: return "require_quality_pass"
      return "accept_verification"
    if stage=="verified":
      if not p["verifierCost"]: return "require_verifier_cost"
      if s["fallbackCount"]>0 and not p["fallbackCost"]: return "require_fallback_cost"
      for field,outcome in [("taskSuccess","require_task_success"),("baselineResult","require_baseline_result"),("usefulDenominator","require_useful_denominator"),("costMetricSeparation","require_cost_metric_separation"),("outputDigest","require_output_digest")]:
        if not p[field]: return outcome
      return "accept_accounting"
    if stage=="accounted":
      if p["rawSpeedPromotionRequested"] and not (p["acceptedOutput"] and p["taskSuccess"] and p["baselineResult"]): return "block_raw_speed_proxy"
      if p["supportPromotionRequested"] and not p["evidenceTransition"]: return "require_evidence_transition"
      if not p["decisionReceipt"]: return "require_decision_receipt"
      if not p["decisionNonClaims"]: return "require_decision_non_claims"
      return "accept_decision"
    return "reject_wrong_stage"


def cases() -> list[dict[str,Any]]:
    rows=[]
    def add(cid,stage,expected,mutation=None,kind=None,fallback=0,last=0):
      p=packet();p.update(mutation or {});actual=route(stage,kind or KINDS[stage],p,state(stage,fallback,last));rows.append({"case_id":cid,"stage":stage,"expected_route":expected,"actual_route":actual,"accepted":actual in ACCEPTED})
    add("wrong-stage","requested","reject_wrong_stage",kind="selectMode")
    add("task-substitution","requested","reject_task_substitution",{"contextDigest":999})
    add("mode-substitution","requested","reject_mode_substitution",{"modeDigest":999})
    add("evaluator-substitution","requested","reject_evaluator_substitution",{"verifierDigest":999})
    add("result-substitution","requested","reject_result_substitution",{"resultDigest":999})
    add("replay","requested","reject_event_replay",last=91)
    add("authority-leak","requested","reject_authority_leak",{"externalEffectRequested":True})
    simple={"requested":[("requestWellFormed","reject_malformed_request"),("contextPacket","require_context_packet"),("taskSet","require_task_set"),("consumer","require_consumer"),("deadline","require_deadline"),("rights","require_rights")],"modeSelected":[("generator","require_generator"),("draftArtifact","require_draft_artifact"),("proposedOutput","require_proposed_output"),("generationCost","require_generation_cost"),("searchBound","require_search_bound")],"decided":[("consumerAcknowledgment","require_consumer_acknowledgment"),("residualClosure","require_residual_closure"),("descendantReferences","require_descendant_references"),("resultDigestBound","require_bound_result_digest"),("cleanup","require_cleanup")]}
    accepts={"requested":"accept_context","modeSelected":"accept_generation","decided":"accept_closure"}
    for stage,pairs in simple.items():
      for field,outcome in pairs:add(f"{stage}-{field}",stage,outcome,{field:False})
      add(f"{stage}-accepted",stage,accepts[stage])
    add("slow-baseline","contextBound","select_slow_baseline",{"fastModeRequested":False})
    for field,outcome in [("generationMode","require_generation_mode"),("riskTier","require_risk_tier"),("qualityTarget","require_quality_target"),("verifierIdentity","require_verifier_identity"),("independentEvaluator","require_independent_evaluator"),("acceptancePredicate","require_acceptance_predicate"),("matchedBaseline","require_matched_baseline"),("latencyBudget","require_latency_budget"),("computeMemoryBudget","require_compute_memory_budget")]:add(f"context-{field}","contextBound",outcome,{field:False})
    for field,outcome in [("riskOverride","require_risk_override"),("slowFallback","require_slow_fallback"),("highRiskReview","require_high_risk_review")]:add(f"high-risk-{field}","contextBound",outcome,{"highRisk":True,field:False})
    add("fast-selection","contextBound","accept_fast_selection")
    for cid,outcome,mutation in [("observed","require_observed_verification",{"observedVerification":False}),("fallback","require_executable_fallback",{"verificationPassed":False,"fallbackExecutable":False}),("fallback-residual","require_fallback_residual",{"verificationPassed":False,"fallbackResidual":False}),("activate-fallback","activate_fallback",{"verificationPassed":False}),("accepted-output","require_accepted_output",{"acceptedOutput":False}),("quality-pass","require_quality_pass",{"qualityPass":False}),("verification-accepted","accept_verification",{})]:add(cid,"draftGenerated",outcome,mutation)
    add("verifier-cost","verified","require_verifier_cost",{"verifierCost":False})
    add("fallback-cost","verified","require_fallback_cost",{"fallbackCost":False},fallback=1)
    for field,outcome in [("taskSuccess","require_task_success"),("baselineResult","require_baseline_result"),("usefulDenominator","require_useful_denominator"),("costMetricSeparation","require_cost_metric_separation"),("outputDigest","require_output_digest")]:add(f"account-{field}","verified",outcome,{field:False})
    add("accounting-accepted","verified","accept_accounting")
    add("raw-speed-proxy","accounted","block_raw_speed_proxy",{"rawSpeedPromotionRequested":True,"acceptedOutput":False})
    add("evidence-transition","accounted","require_evidence_transition",{"supportPromotionRequested":True,"evidenceTransition":False})
    add("decision-receipt","accounted","require_decision_receipt",{"decisionReceipt":False})
    add("decision-nonclaims","accounted","require_decision_non_claims",{"decisionNonClaims":False})
    add("decision-accepted","accounted","accept_decision")
    return rows


def run(cmd: list[str], cwd: Path = ROOT) -> dict[str,Any]:
    p=subprocess.run(cmd,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    if p.returncode: raise RuntimeError(p.stdout)
    return {"command":" ".join(cmd),"exit_code":0,"output_sha256":hashlib.sha256(p.stdout.encode()).hexdigest()}


def source_results(errors:list[str])->dict[str,Any]:
    task=load(TASK_RESULT); theseus=load(THESEUS_RESULT); routes={r["route_id"]:r for r in task["route_summary"]}
    counts={"baseline_valid_count":len(list(BASELINE_FIXTURES.glob("valid_*.json"))),"baseline_invalid_count":len(list(BASELINE_FIXTURES.glob("invalid_*.json"))),"task_route_count":len(routes),"task_count":task.get("task_count"),"baseline_tasks_passed":routes["route://autoregressive-reference"]["tasks_passed"],"candidate_tasks_passed":routes["route://fast-template-verified"]["tasks_passed"],"proxy_tasks_passed":routes["route://latency-only-proxy"]["tasks_passed"],"baseline_cost_units":routes["route://autoregressive-reference"]["total_cost_units"],"candidate_cost_units":routes["route://fast-template-verified"]["total_cost_units"],"proxy_cost_units":routes["route://latency-only-proxy"]["total_cost_units"],"theseus_valid_count":theseus.get("valid_report_count"),"theseus_invalid_count":theseus.get("expected_invalid_count"),"theseus_promotable_count":theseus.get("accepted_promotable_comparison_count")}
    expected={"baseline_valid_count":2,"baseline_invalid_count":4,"task_route_count":3,"task_count":4,"baseline_tasks_passed":4,"candidate_tasks_passed":4,"proxy_tasks_passed":0,"baseline_cost_units":632,"candidate_cost_units":264,"proxy_cost_units":176,"theseus_valid_count":1,"theseus_invalid_count":6,"theseus_promotable_count":0}
    if counts!=expected:errors.append(f"source result counts drifted: {counts}")
    paths=[*sorted(BASELINE_FIXTURES.glob("*.json")),TASK_RESULT,THESEUS_RESULT]
    return {"counts":counts,"sha256":{rel(p):sha(p) for p in paths},"validator_runs":[run(["python3","scripts/validate_generation_mode_baselines.py"]),run(["python3","scripts/validate_fast_generation_task_bundle.py"]),run(["python3","scripts/validate_theseus_generation_mode_import.py"])]}


def build(errors:list[str])->dict[str,Any]:
    rows=cases()
    for row in rows:
      if row["actual_route"]!=row["expected_route"]:errors.append(f"{row['case_id']} expected {row['expected_route']}, got {row['actual_route']}")
    text=LEAN.read_text();body=re.search(r"inductive Route where(?P<body>.*?)deriving DecidableEq",text,re.S).group("body");declared=set(re.findall(r"\|\s+([A-Za-z][A-Za-z0-9]*)",body));reached={r["actual_route"] for r in rows};negative=[r for r in rows if not r["accepted"]]
    if len(declared)!=60 or len(reached)!=60 or len(rows)!=60 or len(negative)!=51:errors.append(f"route coverage expected 60/60/60/51, got {len(declared)}/{len(reached)}/{len(rows)}/{len(negative)}")
    return {"schema_version":"asi_stack.fast_generation_refinement.result.v1","result_id":"2026-07-15-fast-generation-refinement","recorded_date":"2026-07-15","command":COMMAND,"model":{"lean_module":rel(LEAN),"stage_count":8,"route_count":len(declared),"reached_route_count":len(reached),"route_case_count":len(rows),"rejected_mutation_count":len(negative),"fallback_route_reached":"activate_fallback" in reached,"slow_baseline_route_reached":"select_slow_baseline" in reached,"support_assignment_count":0,"external_effect_count":0},"source_result_refinement":source_results(errors),"route_cases":rows,"lean_verification":run(["lake","env","lean","AsiStackProofs/FastGenerationRefinement.lean"], ROOT / "lean"),"support_state_effect":"none","external_effect":"none","residuals":["Finite authored policy lifecycle only; no model generation or wall-clock speed result.","The baseline, task-bundle, and Theseus suites remain bounded local/static evidence.","Fallback and useful-outcome fields are modeled transitions or authored inputs, not deployed effects or natural-workload utility.","Digest binding establishes artifact identity, not source truth, evaluator adequacy, or result generality."],"non_claims":["no model-speed, useful-throughput, quality, safety, deployment, transfer, SOTA, AGI, or ASI claim","no chapter-core support transition","no inference from route coverage or green validators to empirical adequacy"]}


def main()->None:
    parser=argparse.ArgumentParser();parser.add_argument("--write-result",action="store_true");args=parser.parse_args();errors=[];result=build(errors);jsonschema.validate(result,load(SCHEMA));serialized=json.dumps(result,indent=2)+"\n"
    if args.write_result:RESULT.parent.mkdir(parents=True,exist_ok=True);RESULT.write_text(serialized)
    elif not RESULT.exists() or RESULT.read_text()!=serialized:errors.append(f"{rel(RESULT)} missing or stale; run {COMMAND} --write-result")
    if errors:
      print("Fast generation refinement failed:");[print(f" - {e}") for e in errors];sys.exit(1)
    print("Fast generation refinement passed: 8 stages, 60 routes, 51/51 mutations rejected, 2/4 baseline, 3-route task, and 1/6 Theseus suites digest-bound, support/effect none.")


if __name__=="__main__":main()
