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
  if e["from"]!="received" or e["to"]!="parsed" or e["source_constraint"]<=0 or e["source_stop"]<=0 or e["prohibited"] or e["hidden"]:out.append("invalid_parse")
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
 else:out.append("unknown_event")
 return out
def apply(s,e):
 s=copy.deepcopy(s);s["stage"]=e["to"];s["time"]=e["time"];s["version"]=e["output_version"]
 if e["output_constraint"]:s["constraint"]=e["output_constraint"]
 if e["output_stop"]:s["stop"]=e["output_stop"]
 if e["authority_receipt"]:s["approved"]=e["authority"]
 s["accepted"]=e["to"]=="accepted";s["recontract"]=e["to"]=="recontract_required";return s
def run(rows):
 s=initial()
 for i,e in enumerate(rows):
  x=errors(s,e)
  if x:return False,i,x,s
  s=apply(s,e)
 return True,None,[],s
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
 for k,v in (("authority",4),("authority_receipt",False),("from","received"),("root",999),("time",1)):m("authority_"+k,1,k,v)
 for k,v in (("source_constraint",999),("source_stop",999),("output_constraint",999),("output_stop",999),("authority",2),("hidden",True),("prohibited",True),("ambiguity",True),("input_version",2)):m("compile_"+k,2,k,v)
 x=copy.deepcopy(base);x[3].update({"means":False,"authority_expanded":False,"evidence":False,"stop_dropped":False,"parties":False,"promotion":False});out.append(("delta_no_material_change",x))
 m("delta_wrong_target",3,"to","accepted");m("delta_silent_continue",3,"kind","continue")
 for k,v in (("recontract_receipt",False),("output_version",1),("output_constraint",0),("output_stop",0),("authority",4),("from","accepted"),("time",4)):m("recontract_"+k,4,k,v)
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
 base=base_trace();ok,_,_,final=run(base)
 if not ok or final["version"]!=2 or not final["accepted"]:issues.append("reference trace rejected")
 receipts=[]
 for mid,rows in mutations(base):
  accepted,index,reasons,_=run(rows);receipts.append({"mutation_id":mid,"rejected":not accepted,"failed_event_index":index,"reasons":reasons})
  if accepted:issues.append(mid+": mutation accepted")
 result={"schema_version":"asi_stack.intent_resolution_refinement.v1","result_id":"intent-resolution-refinement-2026-07-15-local","source_sha256":{"lean_model":sha(LEAN),"intake_result":sha(INTAKE),"recontract_result":sha(RECONTRACT)},"intake_valid_scenario_count":4,"intake_invalid_control_count":6,"intake_signal_count":6,"recontract_valid_scenario_count":2,"recontract_invalid_control_count":7,"plan_fixture_count":13,"plan_valid_fixture_count":3,"plan_invalid_fixture_count":10,"reachable_trace_event_count":5,"accepted_contract_version":2,"mutation_count":len(receipts),"mutation_rejection_count":sum(x["rejected"] for x in receipts),"reference_trace_final_state":final,"mutation_receipts":receipts,"support_state_effect":"none","non_claims":["The consumer reads structured bounded records and does not establish natural-language intent understanding or semantic completeness.","Numeric hashes, authority and receipts are trusted inputs; the packet does not establish authentic authority extraction, prompt-injection containment, or deployed dispatch.","Passing does not establish user satisfaction, natural-workload usefulness, reproduction, transfer, safety, SOTA, AGI, ASI, or chapter-core support."]}
 try:jsonschema.Draft202012Validator(load(SCHEMA)).validate(result)
 except jsonschema.ValidationError as e:issues.append("schema: "+e.message)
 return result,issues
def main():
 p=argparse.ArgumentParser();p.add_argument("--write",action="store_true");a=p.parse_args();r,e=build()
 if e:raise SystemExit("Intent resolution refinement failed:\n - "+"\n - ".join(e))
 if a.write:RESULT.parent.mkdir(parents=True,exist_ok=True);RESULT.write_text(json.dumps(r,indent=2)+"\n",encoding="utf-8")
 elif not RESULT.exists() or load(RESULT)!=r:raise SystemExit("Intent resolution result stale; run --write")
 print(f"Intent resolution refinement passed: {r['intake_valid_scenario_count']} intake scenarios, {r['recontract_valid_scenario_count']+r['recontract_invalid_control_count']} recontract scenarios, {r['plan_fixture_count']} plan fixtures, {r['mutation_rejection_count']} mutations rejected, support effect none.")
if __name__=="__main__":main()
