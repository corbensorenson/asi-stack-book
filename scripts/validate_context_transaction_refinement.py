#!/usr/bin/env python3
"""Independently consume reachable Context Transaction semantics."""
from __future__ import annotations
import argparse, copy, hashlib, json, subprocess
from pathlib import Path
from typing import Any
import jsonschema

ROOT=Path(__file__).resolve().parents[1]
LEAN=ROOT/"lean/AsiStackProofs/ContextTransactionRefinement.lean"
STORE=ROOT/"experiments/context_transaction_memory_store/fixtures"
SEQUENCES=ROOT/"experiments/context_transaction_sequence_bridge/fixtures"
STORE_VALIDATOR=ROOT/"scripts/validate_context_transaction_memory_store.py"
SEQUENCE_VALIDATOR=ROOT/"scripts/validate_context_transaction_sequence_bridge.py"
TX_SCHEMA=ROOT/"schemas/context_transaction_record.schema.json"
SCHEMA=ROOT/"schemas/context_transaction_refinement.schema.json"
RESULT=ROOT/"experiments/context_transaction_refinement/results/2026-07-15-local.json"
IDS=("transaction_id","snapshot_id","snapshot_epoch","branch_id","mount_id","authority_epoch")

def load(p:Path)->Any:return json.loads(p.read_text())
def sha(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()
def inv(paths:list[Path])->str:return hashlib.sha256(("\n".join(f"{p.name}:{sha(p)}" for p in paths)+"\n").encode()).hexdigest()
def initial()->dict[str,Any]:return {"stage":"raw","transaction_id":0,"snapshot_id":0,"snapshot_epoch":0,"branch_id":0,"mount_id":0,"cell_id":0,"authority_epoch":0,"committed_version":0,"visible_version":0,"source_tainted":False,"derived_tainted":False,"declassification_authorized":False,"deletion_obligation_open":False,"deletion_closure_receipt":False,"snapshot_receipt":False,"write_receipt":False,"commit_receipt":False,"read_receipt":False,"derivation_receipt":False,"replay_receipt":False,"audit_receipt":False,"materialization_receipt":False,"evidence_transition_receipt":False,"materialized":False,"logical_time":0}
def event(k:str,a:str,b:str,t:int)->dict[str,Any]:return {"kind":k,"from_stage":a,"to_stage":b,"transaction_id":101,"snapshot_id":201,"snapshot_epoch":1,"branch_id":301,"mount_id":401,"cell_id":501,"authority_epoch":1,"input_version":0,"output_version":0,"snapshot_present":True,"snapshot_current":True,"branch_matches":True,"mount_permitted":True,"write_committed":False,"read_visible":False,"source_tainted":False,"derived_tainted":False,"declassification_authorized":False,"declassification_receipt":False,"deletion_obligation_open":False,"deletion_closure_receipt":False,"snapshot_receipt":False,"write_receipt":False,"commit_receipt":False,"read_receipt":False,"derivation_receipt":False,"replay_receipt":False,"audit_receipt":False,"materialization_receipt":False,"support_promotion_requested":False,"evidence_transition_receipt":False,"materialized":False,"logical_time":t}
def trace()->list[dict[str,Any]]:
 r=[event("bind","raw","snapshot_bound",1),event("stage","snapshot_bound","write_staged",2),event("commit","write_staged","committed",3),event("read","committed","read_visible",4),event("derive","read_visible","derived",5),event("materialize","derived","materialized",6)]
 r[0].update(snapshot_receipt=True,replay_receipt=True,audit_receipt=True);r[1]["write_receipt"]=True;r[2].update(output_version=1,write_committed=True,commit_receipt=True,audit_receipt=True);r[3].update(input_version=1,write_committed=True,read_visible=True,read_receipt=True,replay_receipt=True);r[4].update(input_version=1,derivation_receipt=True);r[5].update(input_version=1,materialization_receipt=True,materialized=True);return r
def snap(s:dict,r:dict)->bool:return all(r[k]==s[k] for k in IDS)
def cell(s:dict,r:dict)->bool:return snap(s,r) and r["cell_id"]==s["cell_id"]
def errors(s:dict,r:dict)->list[str]:
 o=[]
 if s["stage"]!=r["from_stage"]:o.append("stage")
 if s["logical_time"]>=r["logical_time"]:o.append("time")
 k=r["kind"]
 if k=="bind":
  if any(r[x]<=0 for x in IDS):o.append("identity")
  if not all(r[x] for x in ("snapshot_present","snapshot_current","branch_matches","mount_permitted","snapshot_receipt","replay_receipt","audit_receipt")):o.append("snapshot_custody")
 elif k=="stage":
  if not snap(s,r):o.append("snapshot_substitution")
  if r["cell_id"]<=0 or r["input_version"]!=s["committed_version"]:o.append("write_identity")
  if not r["write_receipt"] or not r["branch_matches"] or not r["mount_permitted"]:o.append("write_policy")
 elif k=="commit":
  if not cell(s,r):o.append("cell_substitution")
  if r["input_version"]!=s["committed_version"] or r["output_version"]!=s["committed_version"]+1:o.append("commit_version")
  if not r["write_committed"] or not r["commit_receipt"] or not r["audit_receipt"]:o.append("commit_custody")
 elif k=="read":
  if not cell(s,r):o.append("cell_substitution")
  if r["input_version"]!=s["committed_version"]:o.append("read_version")
  if not all(r[x] for x in ("write_committed","read_visible","read_receipt","replay_receipt","branch_matches","mount_permitted")):o.append("read_custody")
 elif k=="derive":
  if not cell(s,r):o.append("cell_substitution")
  if r["input_version"]!=s["visible_version"] or r["source_tainted"]!=s["source_tainted"]:o.append("derivation_source")
  if r["source_tainted"] and not r["derived_tainted"] and not (r["declassification_authorized"] and r["declassification_receipt"]):o.append("taint_laundering")
  if r["deletion_obligation_open"]!=s["deletion_obligation_open"] or (r["deletion_obligation_open"] and not r["deletion_closure_receipt"]):o.append("deletion_gap")
  if not r["derivation_receipt"]:o.append("derivation_receipt")
 elif k=="materialize":
  if not cell(s,r) or r["input_version"]!=s["visible_version"]:o.append("materialization_substitution")
  if not all(s[x] for x in ("snapshot_receipt","write_receipt","commit_receipt","read_receipt","derivation_receipt","replay_receipt","audit_receipt")):o.append("prior_custody")
  if s["source_tainted"] and not s["derived_tainted"] and not s["declassification_authorized"]:o.append("taint_open")
  if s["deletion_obligation_open"] and not s["deletion_closure_receipt"]:o.append("deletion_open")
  if r["support_promotion_requested"] and not r["evidence_transition_receipt"]:o.append("support_laundering")
  if not r["materialization_receipt"] or not r["materialized"]:o.append("materialization_receipt")
 else:o.append("unknown")
 return o
def apply(s:dict,r:dict)->dict:
 n=copy.deepcopy(s);n["stage"]=r["to_stage"]
 if r["kind"]=="bind":
  for k in IDS:n[k]=r[k]
 if r["kind"]=="stage":n["cell_id"]=r["cell_id"];n["source_tainted"]=r["source_tainted"];n["deletion_obligation_open"]=r["deletion_obligation_open"]
 if r["kind"]=="commit":n["committed_version"]=r["output_version"]
 if r["kind"]=="read":n["visible_version"]=r["input_version"]
 for k in ("derived_tainted","declassification_authorized","deletion_closure_receipt","snapshot_receipt","write_receipt","commit_receipt","read_receipt","derivation_receipt","replay_receipt","audit_receipt","materialization_receipt","evidence_transition_receipt","materialized"):n[k]=n[k] or r[k]
 n["logical_time"]=r["logical_time"];return n
def run(rows:list[dict])->tuple[bool,int|None,list[str],dict]:
 s=initial()
 for i,r in enumerate(rows):
  e=errors(s,r)
  if e:return False,i,e,s
  s=apply(s,r)
 return True,None,[],s
def mutations(base:list[dict])->list[tuple[str,list[dict]]]:
 out=[]
 def m(name,i,k,v):rows=copy.deepcopy(base);rows[i][k]=v;out.append((name,rows))
 for k in IDS:m("bind_"+k,0,k,0)
 for k in ("snapshot_present","snapshot_current","branch_matches","mount_permitted","snapshot_receipt","replay_receipt","audit_receipt"):m("bind_"+k,0,k,False)
 m("bind_time",0,"logical_time",0)
 for i,prefix in ((1,"stage"),(2,"commit"),(3,"read"),(4,"derive"),(5,"materialize")):
  for k in IDS:m(prefix+"_"+k,i,k,999)
 for name,i,k,v in [("stage_cell",1,"cell_id",0),("stage_version",1,"input_version",1),("stage_receipt",1,"write_receipt",False),("stage_branch",1,"branch_matches",False),("stage_mount",1,"mount_permitted",False),("stage_time",1,"logical_time",1),("commit_cell",2,"cell_id",999),("commit_input",2,"input_version",1),("commit_output",2,"output_version",2),("commit_flag",2,"write_committed",False),("commit_receipt",2,"commit_receipt",False),("commit_audit",2,"audit_receipt",False),("commit_time",2,"logical_time",2),("read_cell",3,"cell_id",999),("read_version",3,"input_version",0),("read_commit",3,"write_committed",False),("read_visible",3,"read_visible",False),("read_receipt",3,"read_receipt",False),("read_replay",3,"replay_receipt",False),("read_branch",3,"branch_matches",False),("read_mount",3,"mount_permitted",False),("read_time",3,"logical_time",3),("derive_cell",4,"cell_id",999),("derive_version",4,"input_version",0),("derive_source",4,"source_tainted",True),("derive_deletion",4,"deletion_obligation_open",True),("derive_receipt",4,"derivation_receipt",False),("derive_time",4,"logical_time",4),("materialize_cell",5,"cell_id",999),("materialize_version",5,"input_version",0),("materialize_support",5,"support_promotion_requested",True),("materialize_receipt",5,"materialization_receipt",False),("materialize_flag",5,"materialized",False),("materialize_time",5,"logical_time",5)]:m(name,i,k,v)
 return out
def suite(path:Path,validator:Path,valid:int,invalid:int,issues:list[str])->dict:
 paths=sorted(path.glob("*.json"));v=sum(p.name.startswith("valid_") for p in paths);iv=sum(p.name.startswith("invalid_") for p in paths);runp=subprocess.run(["python3",str(validator)],cwd=ROOT,text=True,capture_output=True)
 if (v,iv)!=(valid,invalid) or runp.returncode:issues.append(f"{path.name} suite drift: {runp.stdout}{runp.stderr}")
 return {"fixture_count":len(paths),"valid_count":v,"invalid_count":iv,"suite_passed":runp.returncode==0,"inventory_sha256":inv(paths)}
def build()->tuple[dict,list[str]]:
 issues=[];store=suite(STORE,STORE_VALIDATOR,3,6,issues);seq=suite(SEQUENCES,SEQUENCE_VALIDATOR,2,4,issues);base=trace();ok,_,_,final=run(base)
 if not ok or not final["materialized"]:issues.append("reference trace rejected")
 receipts=[]
 for mid,rows in mutations(base):
  accepted,index,why,_=run(rows);receipts.append({"mutation_id":mid,"rejected":not accepted,"failed_event_index":index,"reasons":why})
  if accepted:issues.append(mid+": accepted")
 result={"schema_version":"asi_stack.context_transaction_refinement.v1","result_id":"context-transaction-refinement-2026-07-15-local","source_sha256":{"lean_model":sha(LEAN),"transaction_schema":sha(TX_SCHEMA),"store_validator":sha(STORE_VALIDATOR),"sequence_validator":sha(SEQUENCE_VALIDATOR)},"store_suite":store,"sequence_suite":seq,"reachable_trace_event_count":len(base),"reference_trace_final_state":final,"mutation_count":len(receipts),"mutation_rejection_count":sum(x["rejected"] for x in receipts),"mutation_receipts":receipts,"support_state_effect":"none","non_claims":["This finite sequential model does not establish serializability, linearizability, distributed isolation, crash recovery, or a deployed store.","Fixture-suite validity is consumed at its exact hand-authored boundary and does not establish natural-workload usefulness or transfer.","Numeric identities, policy decisions, taint/deletion facts, authority epochs, and receipts are trusted; no source truth, erasure, side-channel safety, reproduction, SOTA, AGI, ASI, or chapter-core support follows."]}
 try:jsonschema.Draft202012Validator(load(SCHEMA)).validate(result)
 except jsonschema.ValidationError as e:issues.append("schema: "+e.message)
 return result,issues
def main():
 p=argparse.ArgumentParser();p.add_argument("--write",action="store_true");a=p.parse_args();r,e=build()
 if e:raise SystemExit("Context transaction refinement failed:\n - "+"\n - ".join(e))
 if a.write:RESULT.parent.mkdir(parents=True,exist_ok=True);RESULT.write_text(json.dumps(r,indent=2)+"\n")
 elif not RESULT.exists() or load(RESULT)!=r:raise SystemExit("Context transaction refinement result stale; run --write")
 print(f"Context transaction refinement passed: 3/6 store fixtures, 2/4 sequence fixtures, 6 events, {r['mutation_rejection_count']} mutations rejected, support effect none.")
if __name__=="__main__":main()
