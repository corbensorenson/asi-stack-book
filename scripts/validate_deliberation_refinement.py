#!/usr/bin/env python3
from __future__ import annotations

import argparse, hashlib, json, re, subprocess, sys
from pathlib import Path
from typing import Any
import jsonschema

ROOT=Path(__file__).resolve().parents[1]
LEAN=ROOT/"lean/AsiStackProofs/DeliberationRefinement.lean"
SCHEMA=ROOT/"schemas/deliberation_refinement.schema.json"
RESULT=ROOT/"experiments/deliberation_refinement/results/2026-07-15-local.json"
ADMISSION=ROOT/"experiments/deliberation_admission/results/2026-07-13-local.json"
CAMPAIGN=ROOT/"experiments/post_v2_routing_deliberation/results/2026-07-10-local.json"
REAL_MODEL=ROOT/"experiments/post_v2_1_evidence_program/p2/results/test.json"
OUTCOMES=ROOT/"experiments/post_v2_1_evidence_program/results/2026-07-11-post-v2-1-outcomes.json"
COMMAND="python3 scripts/validate_deliberation_refinement.py"
KINDS={"requested":"bindScope","scoped":"generateCandidates","candidatesReady":"evaluateCandidates","evaluated":"selectCandidate","selected":"stopDeliberation","stopped":"handoffToPlanning","handedOff":"close","closed":"close"}
ACCEPTED={"stop_and_escrow","accept_scope","accept_candidates","accept_evaluation","accept_selection","accept_stop","accept_handoff","accept_closure"}

def rel(p:Path)->str:return str(p.relative_to(ROOT))
def load(p:Path)->Any:return json.loads(p.read_text())
def sha(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()

def packet()->dict[str,Any]:
 p={"requestId":4001,"requestVersion":3,"consumerDigest":4002,"taskDigest":4003,"policyDigest":4004,"budgetDigest":4005,"verifierDigest":4006,"evaluatorDigest":4007,"resultDigest":4008,"residualDigest":4009,"eventDigest":91}
 for k in ["requestWellFormed","consumer","taskContract","rights","riskClass","expiry","modePolicy","budget","candidateLimit","stopRule","firstCandidateCapture","candidateHistory","tracePrivacy","completeAttemptDenominator","evaluationObligations","verifierIdentity","evidenceView","dependenceRecord","calibrationRecord","abstentionRule","falseDecisionBounds","independentHighRiskReview","candidateResults","firstCorrectness","corruptionAccounting","repairAccounting","faithfulnessAxes","completeCostAccounting","failureRetention","matchedBaseline","usefulMetric","verifiedCandidate","selectionReceipt","selectionNonClaims","residualRecord","stopReceipt","consumerAcknowledgment","residualClosure","descendantReferences","resultDigestBound","cleanup"]:p[k]=True
 for k in ["highRisk","rawScorePromotionRequested","budgetExhausted","disputed","executionRequested","externalEffectRequested"]:p[k]=False
 return p

def state(stage:str,last:int=0)->dict[str,Any]:
 p=packet();return {k:p[k] for k in ["requestId","requestVersion","consumerDigest","taskDigest","policyDigest","budgetDigest","verifierDigest","evaluatorDigest","resultDigest","residualDigest"]}|{"lastEventDigest":last}

def route(stage:str,kind:str,p:dict[str,Any],s:dict[str,Any]|None=None)->str:
 s=state(stage) if s is None else s
 if kind!=KINDS[stage]:return "reject_wrong_stage"
 if any(p[k]!=s[k] for k in ["requestId","requestVersion","consumerDigest","taskDigest"]):return "reject_request_substitution"
 if any(p[k]!=s[k] for k in ["policyDigest","budgetDigest"]):return "reject_policy_substitution"
 if any(p[k]!=s[k] for k in ["verifierDigest","evaluatorDigest"]):return "reject_evaluator_substitution"
 if any(p[k]!=s[k] for k in ["resultDigest","residualDigest"]):return "reject_result_substitution"
 if p["eventDigest"]==s["lastEventDigest"]:return "reject_event_replay"
 if p["externalEffectRequested"]:return "reject_authority_leak"
 simple={
 "requested":[("requestWellFormed","reject_malformed_request"),("consumer","require_consumer"),("taskContract","require_task_contract"),("rights","require_rights"),("riskClass","require_risk_class"),("expiry","require_expiry")],
 "scoped":[("modePolicy","require_mode_policy"),("budget","require_budget"),("candidateLimit","require_candidate_limit"),("stopRule","require_stop_rule"),("firstCandidateCapture","require_first_candidate_capture"),("candidateHistory","require_candidate_history"),("tracePrivacy","require_trace_privacy"),("completeAttemptDenominator","require_complete_attempt_denominator")],
 "evaluated":[("firstCorrectness","require_first_correctness"),("corruptionAccounting","require_corruption_accounting"),("repairAccounting","require_repair_accounting"),("faithfulnessAxes","require_faithfulness_axes"),("completeCostAccounting","require_complete_cost_accounting"),("failureRetention","require_failure_retention"),("matchedBaseline","require_matched_baseline"),("usefulMetric","require_useful_metric")],
 "handedOff":[("consumerAcknowledgment","require_consumer_acknowledgment"),("residualClosure","require_residual_closure"),("descendantReferences","require_descendant_references"),("resultDigestBound","require_bound_result_digest"),("cleanup","require_cleanup")]}
 if stage in simple:
  if stage=="handedOff" and p["executionRequested"]:return "reject_execution_authority"
  for field,outcome in simple[stage]:
   if not p[field]:return outcome
  return {"requested":"accept_scope","scoped":"accept_candidates","evaluated":"accept_selection","handedOff":"accept_closure"}[stage]
 if stage=="candidatesReady":
  for field,outcome in [("evaluationObligations","require_evaluation_obligations"),("verifierIdentity","require_verifier_identity"),("evidenceView","require_evidence_view"),("dependenceRecord","require_dependence_record"),("calibrationRecord","require_calibration_record"),("abstentionRule","require_abstention_rule"),("falseDecisionBounds","require_false_decision_bounds")]:
   if not p[field]:return outcome
  if p["highRisk"] and not p["independentHighRiskReview"]:return "require_independent_high_risk_review"
  if not p["candidateResults"]:return "require_candidate_results"
  return "accept_evaluation"
 if stage=="selected":
  if not p["verifiedCandidate"]:return "stop_and_escrow"
  if p["rawScorePromotionRequested"]:return "block_raw_score_promotion"
  if not p["selectionReceipt"]:return "require_selection_receipt"
  if not p["selectionNonClaims"]:return "require_selection_non_claims"
  return "accept_stop"
 if stage=="stopped":
  if p["budgetExhausted"] and not p["residualRecord"]:return "require_budget_residual"
  if p["disputed"] and not p["residualRecord"]:return "require_dispute_residual"
  if p["highRisk"] and not p["independentHighRiskReview"]:return "require_high_risk_review"
  if not p["stopReceipt"]:return "require_stop_receipt"
  return "accept_handoff"
 return "reject_wrong_stage"

def cases()->list[dict[str,Any]]:
 rows=[]
 def add(cid,stage,expected,mutation=None,kind=None,last=0):
  p=packet();p.update(mutation or {});actual=route(stage,kind or KINDS[stage],p,state(stage,last));rows.append({"case_id":cid,"stage":stage,"expected_route":expected,"actual_route":actual,"accepted":actual in ACCEPTED})
 add("wrong-stage","requested","reject_wrong_stage",kind="generateCandidates")
 for cid,key,out in [("request-substitution","requestId","reject_request_substitution"),("policy-substitution","policyDigest","reject_policy_substitution"),("evaluator-substitution","verifierDigest","reject_evaluator_substitution"),("result-substitution","resultDigest","reject_result_substitution")]:add(cid,"requested",out,{key:999})
 add("event-replay","requested","reject_event_replay",last=91);add("authority-leak","requested","reject_authority_leak",{"externalEffectRequested":True})
 simple={"requested":[("requestWellFormed","reject_malformed_request"),("consumer","require_consumer"),("taskContract","require_task_contract"),("rights","require_rights"),("riskClass","require_risk_class"),("expiry","require_expiry")],"scoped":[("modePolicy","require_mode_policy"),("budget","require_budget"),("candidateLimit","require_candidate_limit"),("stopRule","require_stop_rule"),("firstCandidateCapture","require_first_candidate_capture"),("candidateHistory","require_candidate_history"),("tracePrivacy","require_trace_privacy"),("completeAttemptDenominator","require_complete_attempt_denominator")],"evaluated":[("firstCorrectness","require_first_correctness"),("corruptionAccounting","require_corruption_accounting"),("repairAccounting","require_repair_accounting"),("faithfulnessAxes","require_faithfulness_axes"),("completeCostAccounting","require_complete_cost_accounting"),("failureRetention","require_failure_retention"),("matchedBaseline","require_matched_baseline"),("usefulMetric","require_useful_metric")],"handedOff":[("consumerAcknowledgment","require_consumer_acknowledgment"),("residualClosure","require_residual_closure"),("descendantReferences","require_descendant_references"),("resultDigestBound","require_bound_result_digest"),("cleanup","require_cleanup")]}
 accepts={"requested":"accept_scope","scoped":"accept_candidates","evaluated":"accept_selection","handedOff":"accept_closure"}
 for stage,pairs in simple.items():
  if stage=="handedOff":add("execution-authority",stage,"reject_execution_authority",{"executionRequested":True})
  for field,out in pairs:add(f"{stage}-{field}",stage,out,{field:False})
  add(f"{stage}-accepted",stage,accepts[stage])
 for field,out in [("evaluationObligations","require_evaluation_obligations"),("verifierIdentity","require_verifier_identity"),("evidenceView","require_evidence_view"),("dependenceRecord","require_dependence_record"),("calibrationRecord","require_calibration_record"),("abstentionRule","require_abstention_rule"),("falseDecisionBounds","require_false_decision_bounds")]:add(f"evaluate-{field}","candidatesReady",out,{field:False})
 add("evaluate-high-risk","candidatesReady","require_independent_high_risk_review",{"highRisk":True,"independentHighRiskReview":False});add("evaluate-results","candidatesReady","require_candidate_results",{"candidateResults":False});add("evaluate-accepted","candidatesReady","accept_evaluation")
 add("selected-no-verified","selected","stop_and_escrow",{"verifiedCandidate":False});add("selected-raw-score","selected","block_raw_score_promotion",{"rawScorePromotionRequested":True});add("selected-receipt","selected","require_selection_receipt",{"selectionReceipt":False});add("selected-nonclaims","selected","require_selection_non_claims",{"selectionNonClaims":False});add("selected-accepted","selected","accept_stop")
 add("stopped-budget","stopped","require_budget_residual",{"budgetExhausted":True,"residualRecord":False});add("stopped-dispute","stopped","require_dispute_residual",{"disputed":True,"residualRecord":False});add("stopped-high-risk","stopped","require_high_risk_review",{"highRisk":True,"independentHighRiskReview":False});add("stopped-receipt","stopped","require_stop_receipt",{"stopReceipt":False});add("stopped-accepted","stopped","accept_handoff")
 return rows

def run(cmd:list[str],cwd:Path=ROOT)->dict[str,Any]:
 p=subprocess.run(cmd,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 if p.returncode:raise RuntimeError(p.stdout)
 return {"command":" ".join(cmd),"exit_code":0,"output_sha256":hashlib.sha256(p.stdout.encode()).hexdigest()}

def source_results(errors:list[str])->dict[str,Any]:
 a=load(ADMISSION);c=load(CAMPAIGN);rm=load(REAL_MODEL);o=load(OUTCOMES);p2=o["P2"];dr=c["deliberation"]["records"];rr=c["routing"]["records"]
 arms=p2["deliberation"]
 counts={"admission_case_count":len(a["case_results"]),"admission_review_count":a["route_counts"].get("require_independent_review"),"admission_escrow_count":a["route_counts"].get("stop_and_escrow_residual"),"admission_harm_count":a["known_extra_compute_harms_preserved"],"seed_count":len(c["seeds"]),"routing_record_count":len(rr),"deliberation_record_count":len(dr),"interference_record_count":len(c["routing"]["interference_counterfactuals"]),"fixed_extra_compute_harm_count":sum(bool(x["extra_compute_harm"]) for x in dr if x["arm"]=="fixed_three_step"),"fallback_activation_count":sum(bool(x["fallback_used"]) for x in rr if x["arm"]=="fallback_abstention"),"disposition_count":len(c["claim_dispositions"]),"real_model_request_count":p2["test_requests"],"real_model_call_count":rm["model_calls"],"real_model_candidate_evaluation_count":p2["candidate_evaluation"]["evaluations"],"real_model_arm_count":len(arms),"real_model_final_correct_count":sum(x["final_correct"] for x in arms.values()),"real_model_initial_correct_count":sum(x["initial_correct"] for x in arms.values()),"real_model_candidate_operation_count":sum(x["candidate_operations"] for x in arms.values()),"real_model_known_harm_regression_count":p2["known_harm_regression"]["case_count"],"real_model_deliberation_disposition":p2["deliberation_disposition"],"real_model_support_state_effect":p2["support_state_effect"]}
 expected={"admission_case_count":10,"admission_review_count":8,"admission_escrow_count":1,"admission_harm_count":15,"seed_count":3,"routing_record_count":900,"deliberation_record_count":540,"interference_record_count":180,"fixed_extra_compute_harm_count":15,"fallback_activation_count":0,"disposition_count":2,"real_model_request_count":60,"real_model_call_count":240,"real_model_candidate_evaluation_count":360,"real_model_arm_count":5,"real_model_final_correct_count":0,"real_model_initial_correct_count":0,"real_model_candidate_operation_count":1140,"real_model_known_harm_regression_count":15,"real_model_deliberation_disposition":"no_change","real_model_support_state_effect":"no_core_promotion"}
 if counts!=expected:errors.append(f"source result counts drifted: {counts}")
 return {"counts":counts,"sha256":{rel(ADMISSION):sha(ADMISSION),rel(CAMPAIGN):sha(CAMPAIGN),rel(REAL_MODEL):sha(REAL_MODEL),rel(OUTCOMES):sha(OUTCOMES)},"validator_runs":[run(["python3","scripts/validate_deliberation_admission.py"]),run(["python3","scripts/validate_post_v2_routing_deliberation.py"]),run(["python3","scripts/validate_post_v2_1_outcomes.py"])]}

def build(errors:list[str])->dict[str,Any]:
 rows=cases()
 for row in rows:
  if row["actual_route"]!=row["expected_route"]:errors.append(f"{row['case_id']} expected {row['expected_route']}, got {row['actual_route']}")
 text=LEAN.read_text();body=re.search(r"inductive Route where(?P<body>.*?)deriving DecidableEq",text,re.S).group("body");declared=set(re.findall(r"\|\s+([A-Za-z][A-Za-z0-9]*)",body));reached={r["actual_route"] for r in rows};negative=[r for r in rows if not r["accepted"]]
 if (len(declared),len(reached),len(rows),len(negative))!=(59,59,59,51):errors.append(f"route coverage expected 59/59/59/51, got {len(declared)}/{len(reached)}/{len(rows)}/{len(negative)}")
 return {"schema_version":"asi_stack.deliberation_refinement.result.v1","result_id":"2026-07-15-deliberation-refinement","recorded_date":"2026-07-15","command":COMMAND,"model":{"lean_module":rel(LEAN),"stage_count":8,"route_count":len(declared),"reached_route_count":len(reached),"route_case_count":len(rows),"rejected_mutation_count":len(negative),"residual_escrow_route_reached":"stop_and_escrow" in reached,"planning_handoff_route_reached":"accept_handoff" in reached,"support_assignment_count":0,"external_effect_count":0},"source_result_refinement":source_results(errors),"route_cases":rows,"lean_verification":run(["lake","env","lean","AsiStackProofs/DeliberationRefinement.lean"],ROOT/"lean"),"support_state_effect":"none","external_effect":"none","residuals":["Finite authored lifecycle only; no language-model candidate, natural workload, evaluator, or planning execution ran.","The post-v2 campaign is deterministic synthetic evidence with zero fallback activation and fifteen fixed-step harms.","Verifier independence, correctness, calibration, trace faithfulness, useful metrics, costs, and residual fields are authored gates or inherited bounded records.","Digest binding establishes artifact identity, not source truth, empirical adequacy, or transfer."],"non_claims":["no reasoning quality, useful-throughput, verifier, faithfulness, safety, deployment, transfer, SOTA, AGI, or ASI claim","no execution authority or chapter-core support transition","no inference from route coverage, synthetic accuracy, or green validators to empirical adequacy"]}

def main()->None:
 parser=argparse.ArgumentParser();parser.add_argument("--write-result",action="store_true");args=parser.parse_args();errors=[];result=build(errors);jsonschema.validate(result,load(SCHEMA));serialized=json.dumps(result,indent=2)+"\n"
 if args.write_result:RESULT.parent.mkdir(parents=True,exist_ok=True);RESULT.write_text(serialized)
 elif not RESULT.exists() or RESULT.read_text()!=serialized:errors.append(f"{rel(RESULT)} missing or stale; run {COMMAND} --write-result")
 if errors:
  print("Deliberation refinement failed:");[print(f" - {e}") for e in errors];sys.exit(1)
 print("Deliberation refinement passed: 8 stages, 59 routes, 51/51 mutations rejected; 10-case admission, 3-seed/1,440-record campaign, and real-model 0/60 no-change result digest-bound; support/effect none.")

if __name__=="__main__":main()
