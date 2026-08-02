#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, re, subprocess, sys
from pathlib import Path
from typing import Any
import jsonschema
ROOT=Path(__file__).resolve().parents[1]
LEAN=ROOT/"lean/AsiStackProofs/ResourceEconomicsRefinement.lean";SCHEMA=ROOT/"schemas/resource_economics_refinement.schema.json";RESULT=ROOT/"experiments/resource_economics_refinement/results/2026-07-15-local.json"
COMMAND="python3 scripts/validate_resource_economics_refinement.py"
SOURCES={
"budget":ROOT/"experiments/resource_budget_ledgers/results/2026-07-01-local.md","costed":ROOT/"experiments/costed_route_resource_slice/results/2026-06-29-local.json","workflow":ROOT/"experiments/resource_workflow_trace/results/2026-07-01-local.json","capacity":ROOT/"experiments/capacity_smoothing/results/2026-07-01-local.md","flagship":ROOT/"experiments/resource_flagship_lane/results/2026-07-01-local.json","ci":ROOT/"experiments/resource_ci_cost_profile/results/2026-07-04-main.json","governance":ROOT/"experiments/resource_governance_tax_tradeoff/results/2026-07-03-local.json","simulation":ROOT/"experiments/simulation_transfer_boundaries/results/2026-06-30-local.md","theseus_sim":ROOT/"experiments/theseus_simulation_fidelity_receipt_suite_import/results/2026-07-05-local.json","theseus_export":ROOT/"experiments/theseus_rlds_minari_trace_export_import/results/2026-07-05-local.json","workload":ROOT/"experiments/resource_workload_quality_probe/results/2026-07-01-local.json","load":ROOT/"experiments/resource_load_stability_probe/results/2026-07-01-local.json"}
KINDS={"requested":"bindRequest","budgeted":"declareBudget","reserved":"reserveCapacity","scheduled":"scheduleWork","executed":"recordExecution","verified":"verifyOutcome","transferred":"transportClaim","reconciled":"reconcileSpend","closed":"close"}
ACCEPTED={"acceptBudgeting","acceptReservation","acceptSchedule","acceptExecution","acceptVerification","acceptTransfer","acceptReconciliation","acceptClosure","acceptClosed"}
STAGES=tuple(KINDS)
LIVE_STAGES=STAGES[:-1]
NEXT_STAGE=dict(zip(STAGES[:-1],STAGES[1:]))
IDENTITY_KEYS=("requestDigest","consumerDigest","taskDigest","policyDigest","rightsDigest","resourceDigest","evaluatorDigest","simulationDigest","resultDigest")
THEOREMS=(
 "authority_request_never_accepts","missing_protected_floor_blocks_reservation",
 "missing_reviewer_capacity_blocks_schedule","raw_proxy_cannot_promote_executed_work",
 "simulated_claim_without_fidelity_blocks_transfer","simulated_claim_above_fidelity_blocks_transfer",
 "missing_failure_retention_blocks_verification",
 "complete_resource_lifecycle_reaches_closed_without_support_or_effect_authority",
 "complete_simulation_transport_reaches_reconciliation_without_promotion",
 "accepted_step_is_accepted","accepted_step_applies_event","apply_event_preserves_full_identity",
 "rejected_apply_event_preserves_state","accepted_step_preserves_full_identity",
 "accepted_step_preserves_non_authority","accepted_step_adds_exactly_one_receipt",
 "accepted_step_advances_stage","apply_event_resource_bill_count_monotone",
 "apply_event_reconciliation_count_monotone","accepted_run_preserves_full_identity",
 "accepted_run_preserves_support","accepted_run_preserves_external_effect",
 "accepted_run_accounts_exact_receipts","accepted_run_resource_bill_count_monotone",
 "accepted_run_reconciliation_count_monotone","accepted_run_has_accepted_trace",
 "resource_run_append","closed_state_accepts_no_event",
 "complete_resource_run_reaches_closed_with_exact_receipts")
def load(p:Path)->Any:return json.loads(p.read_text())
def rel(p:Path)->str:return str(p.relative_to(ROOT))
def sha(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()
def run(cmd:list[str],cwd:Path=ROOT)->dict[str,Any]:
 p=subprocess.run(cmd,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 if p.returncode:raise RuntimeError(p.stdout)
 return {"command":" ".join(cmd),"exit_code":0,"output_sha256":hashlib.sha256(p.stdout.encode()).hexdigest()}
def packet()->dict[str,Any]:
 p={"requestDigest":6001,"consumerDigest":6002,"taskDigest":6003,"policyDigest":6004,"rightsDigest":6005,"resourceDigest":6006,"evaluatorDigest":6007,"simulationDigest":6008,"resultDigest":6009,"eventDigest":111,"claimedSupportLevel":1,"fidelitySupportLevel":1}
 for k in ["consumer","task","risk","rights","horizon","nonClaims","resourceInventory","units","directCost","displacedCost","verificationCost","uncertainty","protectedFloors","capacity","reviewerCapacity","verifierCapacity","protectedOverhead","debtExpiry","capacityOwner","queuePolicy","highRiskPriority","tailPolicy","tenantIsolation","fallback","actualSpend","failureRetention","unsafeReleaseAccounting","usefulOutcome","resourceBill","verifierOutcome","evaluatorBoundary","falseDecisionAccounting","residuals","recovery","simulationScope","simulationFidelity","temporalSemantics","simulationResourceBill","simulationOmissions","transferDecision","variance","opportunityCost","incidents","descendants","evidenceTransition","acknowledgment","resultDigestBound","cleanup"]:p[k]=True
 for k in ["rawProxyPromotion","simulated","supportPromotionRequested","externalEffectRequested"]:p[k]=False
 return p
def state(stage,last=0):
 p=packet();return {k:p[k] for k in IDENTITY_KEYS}|{"stage":stage,"lastEventDigest":last,"receiptCount":0,"resourceBillReceiptCount":0,"reconciliationReceiptCount":0,"supportAssigned":False,"externalEffectCommitted":False}
def route(stage,kind,p,s):
 if kind!=KINDS[stage]:return "rejectWrongStage"
 if any(p[k]!=s[k] for k in ["requestDigest","consumerDigest","taskDigest"]):return "rejectRequestSubstitution"
 if any(p[k]!=s[k] for k in ["policyDigest","rightsDigest"]):return "rejectPolicySubstitution"
 if p["resourceDigest"]!=s["resourceDigest"]:return "rejectResourceSubstitution"
 if any(p[k]!=s[k] for k in ["evaluatorDigest","simulationDigest","resultDigest"]):return "rejectEvidenceSubstitution"
 if p["eventDigest"]==s["lastEventDigest"]:return "rejectEventReplay"
 if p["supportPromotionRequested"] or p["externalEffectRequested"]:return "rejectAuthorityLeak"
 simple={"requested":[("consumer","requestConsumer"),("task","requestTask"),("risk","requestRisk"),("rights","requestRights"),("horizon","requestHorizon"),("nonClaims","requestNonClaims")],"budgeted":[("resourceInventory","requestResourceInventory"),("units","requestUnits"),("directCost","requestDirectCost"),("displacedCost","requestDisplacedCost"),("verificationCost","requestVerificationCost"),("uncertainty","requestUncertainty"),("protectedFloors","requestProtectedFloors")],"reserved":[("capacity","requestCapacity"),("reviewerCapacity","requestReviewerCapacity"),("verifierCapacity","requestVerifierCapacity"),("protectedOverhead","requestProtectedOverhead"),("debtExpiry","requestDebtExpiry"),("capacityOwner","requestCapacityOwner")],"scheduled":[("queuePolicy","requestQueuePolicy"),("highRiskPriority","requestHighRiskPriority"),("tailPolicy","requestTailPolicy"),("tenantIsolation","requestTenantIsolation"),("fallback","requestFallback")],"executed":[("actualSpend","requestActualSpend"),("failureRetention","requestFailureRetention"),("unsafeReleaseAccounting","requestUnsafeReleaseAccounting"),("usefulOutcome","requestUsefulOutcome"),("resourceBill","requestResourceBill")],"verified":[("verifierOutcome","requestVerifierOutcome"),("evaluatorBoundary","requestEvaluatorBoundary"),("falseDecisionAccounting","requestFalseDecisionAccounting"),("residuals","requestResiduals"),("recovery","requestRecovery")],"reconciled":[("variance","requestVariance"),("opportunityCost","requestOpportunityCost"),("incidents","requestIncidents"),("descendants","requestDescendants"),("evidenceTransition","requestEvidenceTransition")],"closed":[("acknowledgment","requestAcknowledgment"),("resultDigestBound","requestResultDigest"),("cleanup","requestCleanup")]}
 accepts={"requested":"acceptBudgeting","budgeted":"acceptReservation","reserved":"acceptSchedule","scheduled":"acceptExecution","executed":"acceptVerification","verified":"acceptTransfer","reconciled":"acceptClosure","closed":"acceptClosed"}
 if stage in simple:
  for f,o in simple[stage]:
   if not p[f]:return o
  if stage=="executed" and p["rawProxyPromotion"]:return "blockRawProxyPromotion"
  return accepts[stage]
 if stage=="transferred":
  if p["simulated"]:
   for f,o in [("simulationScope","requestSimulationScope"),("simulationFidelity","requestSimulationFidelity"),("temporalSemantics","requestTemporalSemantics"),("simulationResourceBill","requestSimulationResourceBill"),("simulationOmissions","requestSimulationOmissions"),("transferDecision","requestTransferDecision")]:
    if not p[f]:return o
   if p["fidelitySupportLevel"]<p["claimedSupportLevel"]:return "blockFidelityOverclaim"
  return "acceptReconciliation"
 raise AssertionError(stage)
def step(s:dict[str,Any],kind:str,p:dict[str,Any])->dict[str,Any]|None:
 if s["stage"]=="closed":return None
 selected=route(s["stage"],kind,p,s)
 if selected not in ACCEPTED:return None
 out=dict(s);out["stage"]=NEXT_STAGE[s["stage"]];out["lastEventDigest"]=p["eventDigest"];out["receiptCount"]+=1
 if selected=="acceptVerification":out["resourceBillReceiptCount"]+=1
 if selected=="acceptClosure":out["reconciliationReceiptCount"]+=1
 return out
def lifecycle_events()->list[tuple[str,dict[str,Any]]]:
 rows=[]
 for index,stage_name in enumerate(LIVE_STAGES,start=1):
  p=packet();p["eventDigest"]=index;rows.append((KINDS[stage_name],p))
 return rows
def run_states(initial:dict[str,Any],events:list[tuple[str,dict[str,Any]]])->list[dict[str,Any]]|None:
 states=[dict(initial)];current=dict(initial)
 for kind,p in events:
  nxt=step(current,kind,p)
  if nxt is None:return None
  states.append(nxt);current=nxt
 return states
def cases():
 rows=[]
 def add(cid,stage,expected,mutation=None,kind=None,last=0):
  p=packet();p.update(mutation or {});actual=route(stage,kind or KINDS[stage],p,state(stage,last));rows.append({"case_id":cid,"stage":stage,"expected_route":expected,"actual_route":actual,"accepted":actual in ACCEPTED})
 add("wrong-stage","requested","rejectWrongStage",kind="declareBudget")
 for cid,key,out in [("request-substitution","requestDigest","rejectRequestSubstitution"),("policy-substitution","policyDigest","rejectPolicySubstitution"),("resource-substitution","resourceDigest","rejectResourceSubstitution"),("evidence-substitution","evaluatorDigest","rejectEvidenceSubstitution")]:add(cid,"requested",out,{key:999})
 add("event-replay","requested","rejectEventReplay",last=111);add("authority-leak","requested","rejectAuthorityLeak",{"supportPromotionRequested":True})
 simple={"requested":[("consumer","requestConsumer"),("task","requestTask"),("risk","requestRisk"),("rights","requestRights"),("horizon","requestHorizon"),("nonClaims","requestNonClaims")],"budgeted":[("resourceInventory","requestResourceInventory"),("units","requestUnits"),("directCost","requestDirectCost"),("displacedCost","requestDisplacedCost"),("verificationCost","requestVerificationCost"),("uncertainty","requestUncertainty"),("protectedFloors","requestProtectedFloors")],"reserved":[("capacity","requestCapacity"),("reviewerCapacity","requestReviewerCapacity"),("verifierCapacity","requestVerifierCapacity"),("protectedOverhead","requestProtectedOverhead"),("debtExpiry","requestDebtExpiry"),("capacityOwner","requestCapacityOwner")],"scheduled":[("queuePolicy","requestQueuePolicy"),("highRiskPriority","requestHighRiskPriority"),("tailPolicy","requestTailPolicy"),("tenantIsolation","requestTenantIsolation"),("fallback","requestFallback")],"executed":[("actualSpend","requestActualSpend"),("failureRetention","requestFailureRetention"),("unsafeReleaseAccounting","requestUnsafeReleaseAccounting"),("usefulOutcome","requestUsefulOutcome"),("resourceBill","requestResourceBill")],"verified":[("verifierOutcome","requestVerifierOutcome"),("evaluatorBoundary","requestEvaluatorBoundary"),("falseDecisionAccounting","requestFalseDecisionAccounting"),("residuals","requestResiduals"),("recovery","requestRecovery")],"reconciled":[("variance","requestVariance"),("opportunityCost","requestOpportunityCost"),("incidents","requestIncidents"),("descendants","requestDescendants"),("evidenceTransition","requestEvidenceTransition")],"closed":[("acknowledgment","requestAcknowledgment"),("resultDigestBound","requestResultDigest"),("cleanup","requestCleanup")]}
 accepts={"requested":"acceptBudgeting","budgeted":"acceptReservation","reserved":"acceptSchedule","scheduled":"acceptExecution","executed":"acceptVerification","verified":"acceptTransfer","reconciled":"acceptClosure","closed":"acceptClosed"}
 for stage,pairs in simple.items():
  for f,o in pairs:add(f"{stage}-{f}",stage,o,{f:False})
  if stage=="executed":add("executed-raw-proxy",stage,"blockRawProxyPromotion",{"rawProxyPromotion":True})
  add(f"{stage}-accepted",stage,accepts[stage])
 for f,o in [("simulationScope","requestSimulationScope"),("simulationFidelity","requestSimulationFidelity"),("temporalSemantics","requestTemporalSemantics"),("simulationResourceBill","requestSimulationResourceBill"),("simulationOmissions","requestSimulationOmissions"),("transferDecision","requestTransferDecision")]:add(f"transferred-{f}","transferred",o,{"simulated":True,f:False})
 add("transferred-overclaim","transferred","blockFidelityOverclaim",{"simulated":True,"claimedSupportLevel":2,"fidelitySupportLevel":1});add("transferred-accepted","transferred","acceptReconciliation",{"simulated":True})
 return rows
def source_results(errors):
 c=load(SOURCES["costed"]);w=load(SOURCES["workflow"]);f=load(SOURCES["flagship"]);ci=load(SOURCES["ci"]);g=load(SOURCES["governance"]);ts=load(SOURCES["theseus_sim"]);te=load(SOURCES["theseus_export"]);wl=load(SOURCES["workload"]);ld=load(SOURCES["load"])
 counts={"budget_valid_count":len(list((ROOT/"experiments/resource_budget_ledgers/fixtures").glob("valid_*.json"))),"budget_invalid_count":len(list((ROOT/"experiments/resource_budget_ledgers/fixtures").glob("invalid_*.json"))),"costed_eligible_count":len(c["eligible_routes"]),"costed_rejected_count":len(c["rejected_routes"]),"workflow_valid_count":w["valid_fixture_count"],"workflow_invalid_count":w["expected_invalid_fixture_count"],"workflow_step_count":w["step_count"],"capacity_valid_count":len(list((ROOT/"experiments/capacity_smoothing/fixtures").glob("valid_*.json"))),"capacity_invalid_count":len(list((ROOT/"experiments/capacity_smoothing/fixtures").glob("invalid_*.json"))),"flagship_command_count":len(f["command_records"]),"flagship_artifact_count":len(f["tracked_artifacts"]),"ci_run_count":len(ci["runs"]),"ci_failure_count":len(ci["failure_events"]),"governance_valid_count":g["valid_scenario_count"],"governance_invalid_count":g["expected_invalid_control_count"],"governed_selection_count":sum(x["selected_route"]=="governed" for x in g["scenario_results"] if x["actual_valid"]),"low_risk_shortcut_count":sum(x["selected_route"]=="ungoverned_shortcut" for x in g["scenario_results"] if x["actual_valid"]),"simulation_valid_count":len(list((ROOT/"experiments/simulation_transfer_boundaries/fixtures").glob("valid_*.json"))),"simulation_invalid_count":len(list((ROOT/"experiments/simulation_transfer_boundaries/fixtures").glob("invalid_*.json"))),"theseus_sim_scenario_count":ts["fixture_scenario_count"],"theseus_sim_receipt_count":ts["world_adapter_receipt_count"],"theseus_sim_invalid_count":ts["expected_invalid_count"],"theseus_export_ready_count":te["ready_count"],"theseus_export_format_count":te["format_count"],"theseus_export_field_count":te["field_count"],"theseus_export_invalid_count":te["expected_invalid_control_count"],"workload_probe_pass_count":int(wl["pass"]),"load_probe_pass_count":int(ld["pass"])}
 expected={"budget_valid_count":6,"budget_invalid_count":7,"costed_eligible_count":2,"costed_rejected_count":2,"workflow_valid_count":1,"workflow_invalid_count":5,"workflow_step_count":3,"capacity_valid_count":3,"capacity_invalid_count":6,"flagship_command_count":10,"flagship_artifact_count":26,"ci_run_count":8,"ci_failure_count":3,"governance_valid_count":3,"governance_invalid_count":5,"governed_selection_count":2,"low_risk_shortcut_count":1,"simulation_valid_count":3,"simulation_invalid_count":6,"theseus_sim_scenario_count":5,"theseus_sim_receipt_count":6,"theseus_sim_invalid_count":7,"theseus_export_ready_count":1,"theseus_export_format_count":3,"theseus_export_field_count":7,"theseus_export_invalid_count":7,"workload_probe_pass_count":1,"load_probe_pass_count":1}
 if counts!=expected:errors.append(f"source counts drifted: {counts}")
 validators=["validate_resource_budget_ledgers.py","validate_costed_route_resource_slice.py","validate_resource_workflow_trace.py","validate_capacity_smoothing.py","validate_resource_flagship_lane.py","validate_resource_ci_cost_profile.py","validate_resource_governance_tax_tradeoff.py","validate_simulation_transfer_boundaries.py","validate_theseus_simulation_fidelity_receipt_suite_import.py","validate_theseus_rlds_minari_trace_export_import.py","validate_resource_workload_quality_probe.py","validate_resource_load_stability_probe.py"]
 return {"counts":counts,"sha256":{rel(p):sha(p) for p in SOURCES.values()},"validator_runs":[run(["python3",f"scripts/{v}"]) for v in validators]}
def lifecycle_checks(errors:list[str])->dict[str,Any]:
 initial=state("requested");events=lifecycle_events();states=run_states(initial,events)
 if states is None:errors.append("canonical lifecycle failed");return {}
 final=states[-1]
 expected={"stage":"closed","lastEventDigest":8,"receiptCount":8,"resourceBillReceiptCount":1,"reconciliationReceiptCount":1,"supportAssigned":False,"externalEffectCommitted":False}
 for key,value in expected.items():
  if final.get(key)!=value:errors.append(f"terminal witness drifted: {key}")
 split_checks=0
 for split in range(len(events)+1):
  prefix=run_states(initial,events[:split])
  if prefix is None:errors.append(f"trace prefix {split} failed");continue
  suffix=run_states(prefix[-1],events[split:])
  if suffix is None or suffix[-1]!=final:errors.append(f"trace composition split {split} failed")
  split_checks+=1
 identity_checks=sum(all(s[k]==initial[k] for k in IDENTITY_KEYS) for s in states)
 nonauthority_checks=sum(not s["supportAssigned"] and not s["externalEffectCommitted"] for s in states)
 bill_monotonicity_checks=sum(a["resourceBillReceiptCount"]<=b["resourceBillReceiptCount"] for a,b in zip(states,states[1:]))
 reconciliation_monotonicity_checks=sum(a["reconciliationReceiptCount"]<=b["reconciliationReceiptCount"] for a,b in zip(states,states[1:]))
 terminal_rejections=sum(step(final,kind,{**packet(),"eventDigest":900+i}) is None for i,kind in enumerate(KINDS.values()))
 return {"states":states,"trace_event_count":len(events),"trace_composition_split_count":split_checks,"identity_preservation_check_count":identity_checks,"non_authority_preservation_check_count":nonauthority_checks,"resource_bill_monotonicity_check_count":bill_monotonicity_checks,"reconciliation_monotonicity_check_count":reconciliation_monotonicity_checks,"terminal_rejection_count":terminal_rejections,"final":final}
def mutation_checks()->list[dict[str,Any]]:
 receipts=[]
 for row in cases():
  if not row["accepted"]:receipts.append({"mutation_id":f"route:{row['case_id']}","rejected":True})
 for stage_index,stage_name in enumerate(LIVE_STAGES):
  for key in IDENTITY_KEYS:
   p=packet();p["eventDigest"]=200+stage_index;p[key]=999999
   receipts.append({"mutation_id":f"identity:{stage_name}:{key}","rejected":step(state(stage_name),KINDS[stage_name],p) is None})
  wrong_kind=KINDS[LIVE_STAGES[(stage_index+1)%len(LIVE_STAGES)]]
  p=packet();p["eventDigest"]=300+stage_index
  receipts.append({"mutation_id":f"wrong-kind:{stage_name}","rejected":step(state(stage_name),wrong_kind,p) is None})
  p=packet();p["eventDigest"]=400+stage_index
  receipts.append({"mutation_id":f"replay:{stage_name}","rejected":step(state(stage_name,last=p["eventDigest"]),KINDS[stage_name],p) is None})
  p=packet();p["eventDigest"]=500+stage_index;p["supportPromotionRequested"]=True
  receipts.append({"mutation_id":f"support:{stage_name}","rejected":step(state(stage_name),KINDS[stage_name],p) is None})
  p=packet();p["eventDigest"]=600+stage_index;p["externalEffectRequested"]=True
  receipts.append({"mutation_id":f"effect:{stage_name}","rejected":step(state(stage_name),KINDS[stage_name],p) is None})
 closed=state("closed")
 for index,kind in enumerate(KINDS.values()):
  p=packet();p["eventDigest"]=700+index
  receipts.append({"mutation_id":f"terminal:{kind}","rejected":step(closed,kind,p) is None})
 return receipts
def build(errors):
 rows=cases();text=LEAN.read_text();body=re.search(r"inductive Route where(?P<body>.*?)deriving DecidableEq",text,re.S).group("body");declared=set(re.findall(r"\|\s+([A-Za-z][A-Za-z0-9]*)",body));reached={x["actual_route"] for x in rows};negative=[x for x in rows if not x["accepted"]];theorem_surface=tuple(re.findall(r"^theorem\s+([A-Za-z0-9_]+)",text,re.M));checks=lifecycle_checks(errors);mutations=mutation_checks()
 for x in rows:
  if x["actual_route"]!=x["expected_route"]:errors.append(f"{x['case_id']}: {x['actual_route']} != {x['expected_route']}")
 if (len(declared),len(reached),len(rows),len(negative))!=(66,66,66,57):errors.append(f"route coverage drifted: {len(declared)}/{len(reached)}/{len(rows)}/{len(negative)}")
 if theorem_surface!=THEOREMS:errors.append(f"theorem surface drifted: {theorem_surface}")
 if re.search(r"\b(sorry|axiom)\b",text):errors.append("Lean placeholder detected")
 if len(mutations)!=170 or not all(x["rejected"] for x in mutations):errors.append(f"mutation coverage drifted: {sum(x['rejected'] for x in mutations)}/{len(mutations)}")
 expected_checks={"trace_event_count":8,"trace_composition_split_count":9,"identity_preservation_check_count":9,"non_authority_preservation_check_count":9,"resource_bill_monotonicity_check_count":8,"reconciliation_monotonicity_check_count":8,"terminal_rejection_count":9}
 for key,value in expected_checks.items():
  if checks.get(key)!=value:errors.append(f"lifecycle check drifted: {key}")
 model={"lean_module":rel(LEAN),"stage_count":9,"lean_theorem_count":len(theorem_surface),"lean_theorem_surface":list(theorem_surface),"route_count":len(declared),"reached_route_count":len(reached),"route_case_count":len(rows),**expected_checks,"identity_field_count":len(IDENTITY_KEYS),"mutation_count":len(mutations),"rejected_mutation_count":sum(x["rejected"] for x in mutations),"simulation_transfer_route_reached":"acceptReconciliation" in reached,"closed_route_reached":"acceptClosed" in reached,"support_assignment_count":0,"external_effect_count":0}
 final=checks.get("final",{});witness={"terminal_stage":final.get("stage"),"receipt_count":final.get("receiptCount"),"resource_bill_receipt_count":final.get("resourceBillReceiptCount"),"reconciliation_receipt_count":final.get("reconciliationReceiptCount"),"support_assigned":final.get("supportAssigned"),"external_effect_committed":final.get("externalEffectCommitted")}
 return {"schema_version":"asi_stack.resource_economics_refinement.result.v2","result_id":"2026-07-15-resource-economics-refinement","recorded_date":"2026-07-15","command":COMMAND,"model":model,"source_result_refinement":source_results(errors),"route_cases":rows,"mutation_receipts":mutations,"witness":witness,"lean_verification":run(["lake","env","lean","AsiStackProofs/ResourceEconomicsRefinement.lean"],ROOT/"lean"),"support_state_effect":"none","external_effect":"none","residuals":["Finite authored allocation-and-claim-transport lifecycle only; no deployed scheduler, market, serving system, reviewer pool, or simulator ran.","Source suites combine synthetic fixtures, repository replays, local timing, historical CI records, and sanitized imports with different evidence meanings.","The costed-route 66.98% result and governance-pays scenarios are fixture-specific and do not establish economic optimality or general savings.","Simulation scope, fidelity, temporal semantics, omissions, resource bills, and support levels are authored gates or bounded records, not calibrated world-model measurements."],"non_claims":["no economic optimality, useful-throughput, model quality, safety, deployed scheduling, simulation adequacy, physical feasibility, transfer, SOTA, AGI, ASI, or support claim","no inference from cost arithmetic, repository replay, CI timing, route coverage, mutation rejection, or green validators to real-world resource benefit","no support assignment or external effect"]}
def main():
 a=argparse.ArgumentParser();a.add_argument("--write-result",action="store_true");args=a.parse_args();errors=[];result=build(errors);jsonschema.validate(result,load(SCHEMA));serialized=json.dumps(result,indent=2)+"\n"
 if args.write_result:RESULT.parent.mkdir(parents=True,exist_ok=True);RESULT.write_text(serialized)
 elif not RESULT.exists() or RESULT.read_text()!=serialized:errors.append(f"{rel(RESULT)} stale; run {COMMAND} --write-result")
 if errors:print("Resource Economics refinement failed:\n - "+"\n - ".join(errors));sys.exit(1)
 print("Resource Economics refinement passed: 29 Lean theorems, 9 stages, 9 trace splits, 66 routes, 170/170 mutations rejected; twelve bounded resource/simulation results digest-bound; support/effect none.")
if __name__=="__main__":main()
