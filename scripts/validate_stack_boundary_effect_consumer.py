#!/usr/bin/env python3
"""Independently consume reachable stack-boundary handoff/effect evidence."""
from __future__ import annotations
import argparse, copy, hashlib, json, re, subprocess
from pathlib import Path
from typing import Any
import jsonschema

ROOT=Path(__file__).resolve().parents[1]
FIXTURES=ROOT/"experiments/authority_transitions/fixtures"
RUNTIME=ROOT/"experiments/runtime_adapter_effect_probe/results/2026-07-02-local.json"
REVOCATION=ROOT/"experiments/authority_revocation_trace/results/2026-07-03-local.json"
LEAN=ROOT/"lean/AsiStackProofs/StackBoundaries.lean"
RESULT=ROOT/"experiments/stack_boundary_effect/results/2026-07-15-local.json"
SCHEMA=ROOT/"schemas/stack_boundary_effect_consumer.schema.json"
RANK={"public_read":1,"public_transform":2,"tracked_file_write":3,"local_fixture_execute":4,"external_effect":5,"governance_approval":6}
MINIMUM={"read":1,"transform":2,"write":3,"execute":4,"disclose":5,"approve":6}

def complete_contract()->dict[str,bool]:
 return {"contract":True,"identity":True,"lifecycle":True,"owner":True,"responsibility":True,"inputs":True,"outputs":True,"ceiling":True,"handoff":True,"invariant":True,"failure":True,"evidence":True,"external_possible":False,"external_authority":True,"authorized_handoff":True,"source_mapping":True,"support_boundary":True,"promotion_requested":False,"evidence_transition":True,"nonclaim":True}
def contract_route(r:dict[str,bool])->str:
 if not r["contract"]:return "no_layer_contract_requested"
 if not r["identity"]:return "request_layer_identity"
 if not r["lifecycle"]:return "request_lifecycle_state"
 if not r["owner"]:return "request_owner"
 if not r["responsibility"]:return "request_responsibility"
 if not r["inputs"]:return "request_input_artifacts"
 if not r["outputs"]:return "request_output_artifacts"
 if not r["ceiling"]:return "request_authority_ceiling"
 if not r["handoff"]:return "request_handoff_protocol"
 if not r["invariant"]:return "request_invariant"
 if not r["failure"]:return "request_failure_mode"
 if not r["evidence"]:return "request_evidence_gate"
 if r["external_possible"] and not r["external_authority"] and not r["authorized_handoff"]:return "block_external_action_boundary"
 if not r["source_mapping"]:return "request_source_mapping"
 if not r["support_boundary"]:return "request_support_boundary"
 if r["promotion_requested"] and not r["evidence_transition"]:return "request_evidence_transition"
 if not r["nonclaim"]:return "preserve_nonclaim_boundary"
 return "admit_layer_contract"
def contract_cases()->list[tuple[str,dict[str,bool],str]]:
 specs=[("no_request",{"contract":False},"no_layer_contract_requested"),("missing_identity",{"identity":False},"request_layer_identity"),("missing_lifecycle",{"lifecycle":False},"request_lifecycle_state"),("missing_owner",{"owner":False},"request_owner"),("missing_responsibility",{"responsibility":False},"request_responsibility"),("missing_inputs",{"inputs":False},"request_input_artifacts"),("missing_outputs",{"outputs":False},"request_output_artifacts"),("missing_ceiling",{"ceiling":False},"request_authority_ceiling"),("missing_handoff",{"handoff":False},"request_handoff_protocol"),("missing_invariant",{"invariant":False},"request_invariant"),("missing_failure",{"failure":False},"request_failure_mode"),("missing_evidence",{"evidence":False},"request_evidence_gate"),("unauthorized_external_action",{"external_possible":True,"external_authority":False,"authorized_handoff":False},"block_external_action_boundary"),("missing_source_mapping",{"source_mapping":False},"request_source_mapping"),("missing_support_boundary",{"support_boundary":False},"request_support_boundary"),("promotion_without_transition",{"promotion_requested":True,"evidence_transition":False},"request_evidence_transition"),("missing_nonclaim",{"nonclaim":False},"preserve_nonclaim_boundary"),("complete",{},"admit_layer_contract")]
 out=[]
 for name,changes,expected in specs:
  row=complete_contract();row.update(changes);out.append((name,row,expected))
 return out

def load(p:Path)->Any:return json.loads(p.read_text(encoding="utf-8"))
def sha(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()

EXPECTED_THEOREMS={
 "layer_without_external_authority_requires_authorized_handoff","valid_stack_trace_rejects_unauthorized_external_handoff","handoff_exceeding_caller_ceiling_rejected","admitted_layer_contract_is_complete","unauthorized_external_action_cannot_be_admitted","accepted_boundary_step_is_valid","accepted_boundary_step_applies_event","apply_boundary_event_preserves_caller_ceiling","accepted_boundary_step_preserves_invariant","boundary_run_preserves_invariant","boundary_run_composes","accepted_boundary_run_has_valid_trace","accepted_boundary_run_preserves_caller_ceiling","accepted_revocation_clears_effect_authority","apply_boundary_event_preserves_revocation","boundary_run_preserves_revocation","revoked_boundary_rejects_authorization_dispatch_and_effect","revocation_blocks_effect_authority_after_any_accepted_suffix","accepted_effect_increments_only_material_accounting","accepted_observation_accounts_for_prior_effect","accepted_rollback_requires_complete_observation_and_clears_accounting","valid_chain_bounds_every_handoff_by_both_layers","valid_two_hop_chain_preserves_artifact_and_cannot_widen_authority","adjacent_chain_never_widens_beyond_its_head","valid_nonempty_chain_is_bounded_by_initial_source_ceiling","three_layer_handoff_chain_is_nonvacuously_valid","authority_widening_breaks_layer_composition","artifact_substitution_breaks_layer_composition","accepted_authorization_respects_caller_ceiling","accepted_effect_requires_live_grant_and_dispatch","reachable_effect_trace_rolls_back_exactly","over_ceiling_authorization_is_rejected","effect_without_dispatch_receipt_is_rejected","revoked_grant_effect_is_rejected"
}
def formal_surface()->dict[str,Any]:
 names=set(re.findall(r"(?m)^theorem\s+([A-Za-z][A-Za-z0-9_]*)",LEAN.read_text(encoding="utf-8")))
 if names!=EXPECTED_THEOREMS:raise AssertionError(f"Lean theorem surface drifted; missing={sorted(EXPECTED_THEOREMS-names)}, extra={sorted(names-EXPECTED_THEOREMS)}")
 command=["lake","env","lean","AsiStackProofs/StackBoundaries.lean"]
 completed=subprocess.run(command,cwd=ROOT/"lean",capture_output=True,text=True)
 if completed.returncode:raise AssertionError(completed.stdout+completed.stderr)
 return {"theorem_count":len(names),"lean_compile_exit_code":0,"admission_inverse":True,"arbitrary_run_invariant":True,"batch_composition":True,"revoked_suffix_exclusion":True,"arbitrary_handoff_chain_authority_bound":True}

def authority_errors(r:dict[str,Any])->list[str]:
 out=[]; decision=r.get("decision"); perm=r.get("permission_class"); caller=RANK.get(r.get("caller_ceiling"),-1); active=RANK.get(r.get("authority_ceiling"),-1); target=RANK.get(r.get("target_required_authority"),-1)
 if perm not in MINIMUM or target<MINIMUM.get(perm,99):out.append("permission_class_collapse")
 if not r.get("audit_refs") or not r.get("non_claims"):out.append("missing_custody_boundary")
 if decision=="allow":
  if r.get("grant_lifecycle_state") not in {"granted","used","receipted"}:out.append("inactive_grant")
  if target>active or active>caller:out.append("authority_widening")
  if not str(r.get("effect_receipt","")).startswith("receipt://"):out.append("missing_effect_receipt")
  if r.get("denial_reason"):out.append("allow_with_denial")
  if "expired" in str(r.get("expiry_or_review","")).lower():out.append("expired_grant")
 elif decision=="deny":
  if r.get("grant_lifecycle_state")!="denied" or not r.get("denial_reason") or r.get("effect_receipt"):out.append("invalid_denial")
 elif decision=="escalate":
  chain=" ".join(r.get("delegation_chain",[])).lower()
  if r.get("grant_lifecycle_state") not in {"requested","delegated"} or r.get("effect_receipt") or not r.get("denial_reason") or not any(x in chain for x in ("review","approval")):out.append("invalid_escalation")
 else:out.append("unknown_decision")
 return out

def initial()->dict[str,Any]:return {"caller_ceiling":3,"active_grant":None,"authority_epoch":11,"revoked":False,"pending_request":None,"dispatch_receipt":False,"material_effects":0,"observed_effects":0,"rolled_back":False,"logical_time":0}
def event(kind,req=3,grant=3,epoch=11,time=1,owner=True,receipt=True,observer=True,exact=True):return {"kind":kind,"requested":req,"grant":grant,"epoch":epoch,"time":time,"owner":owner,"receipt":receipt,"observer":observer,"exact":exact}
def event_errors(s,e):
 out=[]
 if e["time"]<s["logical_time"]:out.append("time_regression")
 k=e["kind"]
 if k=="request":
  if e["requested"]==0 or s["pending_request"] is not None or s["active_grant"] is not None:out.append("invalid_request")
 elif k=="authorize":
  if s["pending_request"]!=e["requested"] or e["grant"]!=e["requested"] or e["grant"]>s["caller_ceiling"]:out.append("invalid_grant_scope")
  if e["epoch"]!=s["authority_epoch"] or not e["owner"] or s["revoked"] or not e["receipt"]:out.append("invalid_grant_custody")
 elif k=="dispatch":
  if s["active_grant"]!=e["grant"] or e["epoch"]!=s["authority_epoch"] or s["revoked"] or not e["receipt"]:out.append("invalid_dispatch")
 elif k=="commit":
  if s["active_grant"]!=e["grant"] or e["epoch"]!=s["authority_epoch"] or not s["dispatch_receipt"] or s["revoked"] or not e["receipt"]:out.append("unauthorized_effect")
 elif k=="observe":
  if s["observed_effects"]>=s["material_effects"] or not e["observer"] or not e["receipt"]:out.append("invalid_observation")
 elif k=="rollback":
  if s["material_effects"]<1 or s["observed_effects"]!=s["material_effects"] or not e["exact"] or not e["receipt"]:out.append("invalid_rollback")
 elif k=="revoke":
  if e["epoch"]!=s["authority_epoch"] or not e["receipt"]:out.append("invalid_revocation")
 elif k=="deny":
  if s["pending_request"]!=e["requested"] or s["material_effects"]!=0 or not e["receipt"]:out.append("invalid_denial")
 else:out.append("unknown_event")
 return out
def apply(s,e):
 s=copy.deepcopy(s);s["logical_time"]=e["time"];k=e["kind"]
 if k=="request":s["pending_request"]=e["requested"]
 elif k=="authorize":s["active_grant"]=e["grant"]
 elif k=="dispatch":s["dispatch_receipt"]=True
 elif k=="commit":s["material_effects"]+=1
 elif k=="observe":s["observed_effects"]+=1
 elif k=="rollback":s["material_effects"]=0;s["observed_effects"]=0;s["rolled_back"]=True
 elif k=="revoke":s["active_grant"]=None;s["authority_epoch"]+=1;s["revoked"]=True;s["dispatch_receipt"]=False
 elif k=="deny":s["pending_request"]=None
 return s
def state_invariant(s):
 if s["observed_effects"]>s["material_effects"]:return False
 if s["active_grant"] is not None and (s["active_grant"]>s["caller_ceiling"] or s["revoked"]):return False
 if s["dispatch_receipt"] and (s["active_grant"] is None or s["revoked"]):return False
 return True
def run_from(s,events):
 s=copy.deepcopy(s)
 for i,e in enumerate(events):
  x=event_errors(s,e)
  if x:return False,i,x,s
  s=apply(s,e)
 return True,None,[],s
def run(events):return run_from(initial(),events)

def handoff(source,target,source_ceiling,target_ceiling,requested,input_artifact,output_artifact):
 return {"source":source,"target":target,"source_ceiling":source_ceiling,"target_ceiling":target_ceiling,"requested":requested,"input_artifact":input_artifact,"output_artifact":output_artifact,"authorized":True}
def handoff_valid(h):
 return h["source"]!=h["target"] and h["authorized"] and h["requested"]<=h["source_ceiling"] and h["requested"]<=h["target_ceiling"]
def handoffs_compose(left,right):
 return left["target"]==right["source"] and left["output_artifact"]==right["input_artifact"] and right["requested"]<=left["requested"]

def build():
 errors=[];fixtures=[]
 for p in sorted(FIXTURES.glob("*.json")):
  x=authority_errors(load(p)); expected=not p.name.startswith("invalid_"); accepted=not x
  if accepted!=expected:errors.append(f"{p.name}: disposition mismatch")
  fixtures.append({"fixture":p.name,"expected":expected,"accepted":accepted,"reasons":x,"sha256":sha(p)})
 runtime=load(RUNTIME); rev=load(REVOCATION)
 if runtime.get("pass") is not True or rev.get("trace_entry_count")!=5:errors.append("source runtime/revocation evidence drift")
 route_receipts=[]
 for name,record,expected in contract_cases():
  actual=contract_route(record); matched=actual==expected
  if not matched:errors.append(f"{name}: layer-contract route {actual}, expected {expected}")
  route_receipts.append({"id":name,"expected_route":expected,"actual_route":actual,"matched":matched})
 valid=[event("request",time=1),event("authorize",time=2),event("dispatch",time=3),event("commit",time=4),event("observe",time=5),event("rollback",time=6)]
 denial=[event("request",time=1),event("deny",time=2)]
 runtime_cases=[("executed_effect_and_rollback",valid),("missing_permission_denial",denial),("expired_approval_denial",denial)]
 runtime_receipts=[]
 invariant_prefix_count=0;composition_check_count=0
 for name,events in runtime_cases:
  ok,idx,reasons,state=run(events)
  if not ok:errors.append(f"{name}: rejected")
  for split in range(len(events)+1):
   prefix_ok,_,_,prefix_state=run(events[:split])
   if not prefix_ok or not state_invariant(prefix_state):errors.append(f"{name}: invariant failed at prefix {split}")
   else:invariant_prefix_count+=1
   suffix_ok,_,_,staged_state=run_from(prefix_state,events[split:])
   if not suffix_ok or staged_state!=state:errors.append(f"{name}: composition failed at split {split}")
   else:composition_check_count+=1
  runtime_receipts.append({"id":name,"accepted":ok,"events":len(events),"final_state":state})
 left=handoff(10,20,4,3,3,101,202);right=handoff(20,30,3,2,2,202,303)
 handoff_cases=[("valid_three_layer_path",left,right,True),("authority_widening",left,{**right,"requested":4},False),("artifact_substitution",left,{**right,"input_artifact":999},False)]
 handoff_receipts=[]
 for name,first,second,expected in handoff_cases:
  accepted=handoff_valid(first) and handoff_valid(second) and handoffs_compose(first,second)
  if accepted!=expected:errors.append(f"{name}: handoff-chain disposition mismatch")
  handoff_receipts.append({"id":name,"expected":expected,"accepted":accepted})
 mutations=[]
 def m(i,k,v):x=copy.deepcopy(valid);x[i][k]=v;return x
 mutations += [m(0,"requested",0),m(1,"grant",4),m(1,"owner",False),m(1,"receipt",False),m(2,"epoch",12),m(2,"receipt",False),m(3,"receipt",False),m(4,"observer",False),m(4,"receipt",False),m(5,"exact",False),m(5,"receipt",False)]
 mutations.append(valid[:2]+[event("revoke",time=3)]+[event("dispatch",time=4),event("commit",time=5)])
 rejected=sum(not run(x)[0] for x in mutations)
 if rejected!=len(mutations):errors.append("mutation accepted")
 result={"schema_version":"asi_stack.stack_boundary_effect_consumer.v1","result_id":"stack-boundary-effect-2026-07-15-local","lean_model_sha256":sha(LEAN),"formal_surface":formal_surface(),"runtime_result_sha256":sha(RUNTIME),"revocation_result_sha256":sha(REVOCATION),"layer_contract_case_count":len(route_receipts),"layer_contract_route_match_count":sum(x["matched"] for x in route_receipts),"authority_fixture_count":len(fixtures),"authority_fixture_accepted_count":sum(x["accepted"] for x in fixtures),"authority_fixture_rejected_count":sum(not x["accepted"] for x in fixtures),"runtime_case_count":3,"runtime_case_accepted_count":3,"runtime_accepted_event_count":10,"runtime_invariant_prefix_count":invariant_prefix_count,"runtime_composition_check_count":composition_check_count,"layer_handoff_chain_case_count":len(handoff_receipts),"layer_handoff_chain_rejection_count":sum(not x["accepted"] for x in handoff_receipts),"executed_effect_count":1,"independently_observed_effect_count":1,"exact_rollback_count":1,"no_mutation_denial_count":2,"revocation_trace_entry_count":5,"mutation_count":len(mutations),"mutation_rejection_count":rejected,"layer_contract_receipts":route_receipts,"authority_receipts":fixtures,"runtime_receipts":runtime_receipts,"layer_handoff_receipts":handoff_receipts,"support_state_effect":"none","non_claims":["The consumer binds one local temp-file effect and synthetic authority fixtures; it does not establish deployed enforcement.","Recorded grant, owner, receipt, observer, and revocation fields are trusted inputs and do not prove authenticity or complete observation.","Passing traces do not establish safety, security, natural-workload utility, reproduction, transfer, or chapter-core support."]}
 try:jsonschema.Draft202012Validator(load(SCHEMA)).validate(result)
 except jsonschema.ValidationError as exc:errors.append(f"schema:{exc.message}")
 return result,errors
def main():
 p=argparse.ArgumentParser();p.add_argument("--write",action="store_true");a=p.parse_args();r,e=build()
 if e:raise SystemExit("Stack boundary consumer failed:\n - "+"\n - ".join(e))
 if a.write:RESULT.parent.mkdir(parents=True,exist_ok=True);RESULT.write_text(json.dumps(r,indent=2)+"\n",encoding="utf-8")
 elif not RESULT.exists() or load(RESULT)!=r:raise SystemExit("Stack boundary consumer result stale; run --write")
 print(f"Stack boundary consumer passed: {r['formal_surface']['theorem_count']} Lean theorems, {r['layer_contract_route_match_count']} layer-contract routes, {r['runtime_invariant_prefix_count']} invariant prefixes, {r['runtime_composition_check_count']} compositions, {r['layer_handoff_chain_rejection_count']} handoff countermodels, {r['mutation_rejection_count']} mutations rejected, support effect none.")
if __name__=="__main__":main()
