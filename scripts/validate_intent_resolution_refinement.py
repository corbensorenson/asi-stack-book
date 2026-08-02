#!/usr/bin/env python3
"""Consume the reachable intent-resolution model against bounded local evidence."""
from __future__ import annotations
import argparse, copy, hashlib, json
from pathlib import Path
from typing import Any
import jsonschema

ROOT=Path(__file__).resolve().parents[1]
LEAN=ROOT/"lean/AsiStackProofs/IntentResolutionRefinement.lean"
INTAKE=ROOT/"experiments/intent_intake_probe/results/2026-07-02-local.json"
RECONTRACT=ROOT/"experiments/intent_recontract_probe/results/2026-07-02-local.json"
PLAN_FIXTURES=ROOT/"experiments/plan_execution_contracts/fixtures"
RESULT=ROOT/"experiments/intent_resolution_refinement/results/2026-07-15-local.json"
SCHEMA=ROOT/"schemas/intent_resolution_refinement.schema.json"

def load(p:Path)->Any:return json.loads(p.read_text(encoding="utf-8"))
def sha(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()
def initial():return {"stage":"received","root":101,"version":1,"constraint":0,"stop":0,"ceiling":3,"approved":0,"ambiguity":False,"accepted":False,"recontract":False,"blocked":False,"time":0}
def event(kind,from_stage,to_stage,time):return {"kind":kind,"from":from_stage,"to":to_stage,"root":101,"input_version":1,"output_version":1,"source_constraint":501,"source_stop":601,"output_constraint":501,"output_stop":601,"authority":3,"prohibited":False,"hidden":False,"ambiguity":False,"clarification":False,"authority_receipt":False,"means":False,"authority_expanded":False,"evidence":False,"stop_dropped":False,"parties":False,"promotion":False,"recontract_receipt":False,"block":False,"time":time}
def material(e):return any(e[k] for k in ("means","authority_expanded","evidence","stop_dropped","parties","promotion"))
def errors(s,e):
 out=[]
 if s["stage"]!=e["from"] or s["root"]!=e["root"] or s["version"]!=e["input_version"] or s["time"]>=e["time"]:out.append("lineage_or_time_mismatch")
 k=e["kind"]
 if k=="parse":
  if e["from"]!="received" or e["to"]!="parsed" or e["source_constraint"]<=0 or e["source_stop"]<=0 or e["output_version"]!=e["input_version"] or e["output_constraint"]!=e["source_constraint"] or e["output_stop"]!=e["source_stop"] or e["prohibited"] or e["hidden"]:out.append("invalid_parse")
 elif k=="clarify":
  if e["from"]!="parsed" or e["to"]!="clarified" or not s["ambiguity"] or not e["ambiguity"] or not e["clarification"]:out.append("invalid_clarification")
 elif k=="authority":
  if e["from"] not in {"parsed","clarified"} or e["to"]!="authority_reviewed" or s["ambiguity"] or not e["authority_receipt"] or e["authority"]>s["ceiling"]:out.append("invalid_authority_review")
 elif k=="compile":
  if e["from"]!="authority_reviewed" or e["to"]!="accepted" or e["source_constraint"]!=s["constraint"] or e["source_stop"]!=s["stop"] or e["output_constraint"]!=s["constraint"] or e["output_stop"]!=s["stop"] or e["authority"]!=s["approved"] or e["hidden"] or e["prohibited"] or e["ambiguity"]:out.append("invalid_compile")
 elif k=="delta":
  if e["from"]!="accepted" or e["to"]!="recontract_required" or not material(e):out.append("material_delta_not_custodied")
 elif k=="continue":
  if e["from"]!="accepted" or e["to"]!="accepted" or material(e) or s["recontract"]:out.append("silent_material_delta")
 elif k=="recontract":
  if e["from"]!="recontract_required" or e["to"]!="accepted" or not s["recontract"] or not e["recontract_receipt"] or e["output_version"]<=s["version"] or e["output_constraint"]<=0 or e["output_stop"]<=0 or e["authority"]>s["ceiling"]:out.append("invalid_recontract")
 elif k=="reject":
  if e["to"]!="rejected" or not e["block"]:out.append("invalid_rejection")
 else:out.append("unknown_event")
 return out
def apply(s,e):
 s=copy.deepcopy(s);s["stage"]=e["to"];s["time"]=e["time"]
 if e["kind"]=="parse":s["constraint"]=e["output_constraint"];s["stop"]=e["output_stop"];s["ambiguity"]=e["ambiguity"]
 elif e["kind"]=="clarify":s["ambiguity"]=False
 elif e["kind"]=="authority":s["approved"]=e["authority"]
 elif e["kind"]=="recontract":s["version"]=e["output_version"];s["constraint"]=e["output_constraint"];s["stop"]=e["output_stop"];s["approved"]=e["authority"]
 elif e["kind"]=="reject":s["blocked"]=True
 s["accepted"]=e["to"]=="accepted";s["recontract"]=e["to"]=="recontract_required";return s
def invariant_errors(s):
 out=[]
 if s["approved"]>s["ceiling"]:out.append("approved_authority_exceeds_ceiling")
 if s["stage"]!="received" and s["stage"]!="rejected" and (s["constraint"]<=0 or s["stop"]<=0):out.append("materialized_contract_missing_payload")
 if s["accepted"]!=(s["stage"]=="accepted"):out.append("accepted_stage_flag_mismatch")
 if s["recontract"]!=(s["stage"]=="recontract_required"):out.append("recontract_stage_flag_mismatch")
 return out
def run(rows,start=None):
 s=copy.deepcopy(start) if start is not None else initial()
 for i,e in enumerate(rows):
  x=errors(s,e)
  if x:return False,i,x,s
  s=apply(s,e)
  x=invariant_errors(s)
  if x:return False,i,x,s
 return True,None,[],s
def audit_scenario(sid,rows):
 issues=[];ok,_,reasons,final=run(rows)
 if not ok:issues.append(f"{sid}: rejected {reasons}")
 for end in range(1,len(rows)+1):
  if not run(rows[:end])[0]:issues.append(f"{sid}: prefix {end} rejected")
 for split in range(len(rows)+1):
  left=run(rows[:split]);right=run(rows[split:],left[3])
  if not left[0] or not right[0] or right[3]!=final:issues.append(f"{sid}: split {split} drift")
 return {"scenario_id":sid,"event_count":len(rows),"accepted":ok,"prefix_invariant_check_count":len(rows),"composition_check_count":len(rows)+1,"final_state":final},issues
def base_trace():
 p=event("parse","received","parsed",1)
 a=event("authority","parsed","authority_reviewed",2);a["authority_receipt"]=True
 c=event("compile","authority_reviewed","accepted",3)
 d=event("delta","accepted","recontract_required",4);d["means"]=True
 r=event("recontract","recontract_required","accepted",5);r["output_version"]=2;r["recontract_receipt"]=True
 return [p,a,c,d,r]
def mutations(base):
 out=[]
 def m(name,i,k,v):x=copy.deepcopy(base);x[i][k]=v;out.append((name,x))
 for k,v in (("source_constraint",0),("source_stop",0),("prohibited",True),("hidden",True),("time",0),("root",999)):m("parse_"+k,0,k,v)
 for k,v in (("output_version",2),("output_constraint",999),("output_stop",999)):m("parse_"+k,0,k,v)
 for k,v in (("authority",4),("authority_receipt",False),("from","received"),("root",999),("time",1)):m("authority_"+k,1,k,v)
 for k,v in (("source_constraint",999),("source_stop",999),("output_constraint",999),("output_stop",999),("authority",2),("hidden",True),("prohibited",True),("ambiguity",True),("input_version",2)):m("compile_"+k,2,k,v)
 x=copy.deepcopy(base);x[3].update({"means":False,"authority_expanded":False,"evidence":False,"stop_dropped":False,"parties":False,"promotion":False});out.append(("delta_no_material_change",x))
 m("delta_wrong_target",3,"to","accepted");m("delta_silent_continue",3,"kind","continue")
 for k,v in (("recontract_receipt",False),("output_version",1),("output_constraint",0),("output_stop",0),("authority",4),("from","accepted"),("time",4)):m("recontract_"+k,4,k,v)
 clarify=[copy.deepcopy(base[0]),event("clarify","parsed","clarified",2)]
 clarify[0]["ambiguity"]=True;clarify[1]["ambiguity"]=True;clarify[1]["clarification"]=True
 for k,v in (("clarification",False),("ambiguity",False),("to","accepted")):
  x=copy.deepcopy(clarify);x[1][k]=v;out.append(("clarify_"+k,x))
 reject=[event("reject","received","rejected",1)];reject[0]["block"]=True
 for k,v in (("block",False),("to","accepted")):
  x=copy.deepcopy(reject);x[0][k]=v;out.append(("reject_"+k,x))
 for key in ("evidence","stop_dropped"):
  x=copy.deepcopy(base[:3])+[event("continue","accepted","accepted",4)];x[-1][key]=True;out.append(("continue_"+key,x))
 return out
def build():
 issues=[]; intake=load(INTAKE); recontract=load(RECONTRACT)
 if intake.get("valid_scenarios")!=4 or intake.get("expected_invalid_controls")!=6 or intake.get("support_state_effect")!="none":issues.append("intake drift")
 signals=intake.get("signal_coverage",{})
 if len(signals)!=6 or not all(signals.values()):issues.append("intake signals drift")
 if recontract.get("summary",{}).get("valid_scenarios")!=2 or recontract.get("summary",{}).get("expected_invalid_controls")!=7 or recontract.get("support_state_effect")!="none":issues.append("recontract drift")
 scenarios=[*recontract.get("valid_scenarios",[]),*recontract.get("expected_invalid_controls",[])]
 if len(scenarios)!=9 or not all(x.get("scenario_pass") for x in scenarios):issues.append("recontract scenarios drift")
 fixtures=sorted(PLAN_FIXTURES.glob("*.json")); valid=sum(not p.name.startswith("invalid_") for p in fixtures)
 if len(fixtures)!=13 or valid!=3:issues.append("plan fixture drift")
 base=base_trace()
 direct=base[:3]
 clarify=[copy.deepcopy(base[0]),event("clarify","parsed","clarified",2),event("authority","clarified","authority_reviewed",3),event("compile","authority_reviewed","accepted",4)];clarify[0]["ambiguity"]=True;clarify[1]["ambiguity"]=True;clarify[1]["clarification"]=True;clarify[2]["authority_receipt"]=True
 continued=copy.deepcopy(direct)+[event("continue","accepted","accepted",4)]
 rejected=[event("reject","received","rejected",1)];rejected[0]["block"]=True
 scenario_receipts=[]
 for sid,rows in (("recontract",base),("clarified",clarify),("continued",continued),("rejected",rejected)):
  receipt,errs=audit_scenario(sid,rows);scenario_receipts.append(receipt);issues.extend(errs)
 final=scenario_receipts[0]["final_state"]
 if final["version"]!=2 or not final["accepted"]:issues.append("reference trace rejected")
 receipts=[]
 noninterference=0
 for mid,rows in mutations(base):
  accepted,index,reasons,rejected_state=run(rows);same=False
  if index is not None:same=run(rows[:index])[0] and run(rows[:index])[3]==rejected_state
  if same:noninterference+=1
  receipts.append({"mutation_id":mid,"rejected":not accepted,"failed_event_index":index,"state_noninterfering":same,"reasons":reasons})
  if accepted:issues.append(mid+": mutation accepted")
  if not same:issues.append(mid+": rejection changed state")
 result={"schema_version":"asi_stack.intent_resolution_refinement.v1","result_id":"intent-resolution-refinement-2026-07-15-local","source_sha256":{"lean_model":sha(LEAN),"intake_result":sha(INTAKE),"recontract_result":sha(RECONTRACT)},"intake_valid_scenario_count":4,"intake_invalid_control_count":6,"intake_signal_count":6,"recontract_valid_scenario_count":2,"recontract_invalid_control_count":7,"plan_fixture_count":13,"plan_valid_fixture_count":3,"plan_invalid_fixture_count":10,"reachable_trace_event_count":5,"reachable_scenario_count":4,"reachable_scenario_event_count":14,"invariant_prefix_check_count":14,"composition_check_count":18,"accepted_contract_version":2,"mutation_count":len(receipts),"mutation_rejection_count":sum(x["rejected"] for x in receipts),"rejection_noninterference_count":noninterference,"reference_trace_final_state":final,"scenario_receipts":scenario_receipts,"mutation_receipts":receipts,"support_state_effect":"none","non_claims":["The consumer reads structured bounded records and does not establish natural-language intent understanding or semantic completeness.","Numeric hashes, authority and receipts are trusted inputs; the packet does not establish authentic authority extraction, prompt-injection containment, or deployed dispatch.","Passing does not establish user satisfaction, natural-workload usefulness, reproduction, transfer, safety, SOTA, AGI, ASI, or chapter-core support."]}
 try:jsonschema.Draft202012Validator(load(SCHEMA)).validate(result)
 except jsonschema.ValidationError as e:issues.append("schema: "+e.message)
 return result,issues
def main():
 p=argparse.ArgumentParser();p.add_argument("--write",action="store_true");a=p.parse_args();r,e=build()
 if e:raise SystemExit("Intent resolution refinement failed:\n - "+"\n - ".join(e))
 if a.write:RESULT.parent.mkdir(parents=True,exist_ok=True);RESULT.write_text(json.dumps(r,indent=2)+"\n",encoding="utf-8")
 elif not RESULT.exists() or load(RESULT)!=r:raise SystemExit("Intent resolution result stale; run --write")
 print(f"Intent resolution refinement passed: {r['reachable_scenario_count']} traces/{r['reachable_scenario_event_count']} events, {r['invariant_prefix_check_count']} invariant prefixes, {r['composition_check_count']} compositions, {r['mutation_rejection_count']} state-noninterfering mutations rejected, support effect none.")
if __name__=="__main__":main()
