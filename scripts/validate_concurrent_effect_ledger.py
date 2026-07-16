#!/usr/bin/env python3
"""Independently consume the logical-time concurrent effect ledger."""

from __future__ import annotations
import argparse, copy, hashlib, json
from pathlib import Path
from typing import Any
import jsonschema

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "experiments/integrated_reference_trace/concurrent_effect_corpus.json"
RESULT = ROOT / "experiments/integrated_reference_trace/results/2026-07-15-concurrent-effect-ledger.json"
SCHEMA = ROOT / "schemas/concurrent_effect_ledger_result.schema.json"
LEAN = ROOT / "lean/AsiStackProofs/IntegratedReferenceTrace.lean"
KINDS = {"attempt", "observe", "acknowledge", "compensate", "residualize", "revoke"}

def load(path: Path) -> Any: return json.loads(path.read_text(encoding="utf-8"))
def sha(path: Path) -> str: return hashlib.sha256(path.read_bytes()).hexdigest()

def reasons(state: dict[str, Any], event: list[Any]) -> list[str]:
    kind, effect_id, epoch, time, receipt = event
    out=[]
    if kind not in KINDS: return ["unknown_kind"]
    if time < state["logical_time"]: out.append("logical_time_regression")
    terminal=set(state["acknowledged"]+state["compensated"]+state["residualized"])
    if kind=="attempt":
        if effect_id==0: out.append("zero_effect_identity")
        if epoch!=state["authority_epoch"]: out.append("stale_authority_epoch")
        if state["revoked_at"] is not None and time>=state["revoked_at"]: out.append("attempt_at_or_after_revocation")
    elif kind=="observe":
        if effect_id not in state["attempted"]: out.append("observation_without_attempt")
        if effect_id in state["observed"]: out.append("duplicate_observation")
    elif kind in {"acknowledge","compensate","residualize"}:
        if effect_id not in state["observed"]: out.append("terminal_without_observation")
        if effect_id in terminal: out.append("duplicate_terminal_disposition")
        if receipt is not True: out.append("terminal_without_receipt")
    elif kind=="revoke" and epoch!=state["authority_epoch"]:
        out.append("stale_revocation_epoch")
    return out

def apply(state: dict[str, Any], event: list[Any]) -> dict[str, Any]:
    kind,effect_id,_,time,_=event; state=copy.deepcopy(state); state["logical_time"]=time
    if kind=="attempt" and effect_id not in state["attempted"]: state["attempted"].append(effect_id)
    elif kind=="observe": state["observed"].append(effect_id)
    elif kind=="acknowledge": state["acknowledged"].append(effect_id)
    elif kind=="compensate": state["compensated"].append(effect_id)
    elif kind=="residualize": state["residualized"].append(effect_id)
    elif kind=="revoke": state["revoked_at"]=time; state["authority_epoch"]+=1
    return state

def run(initial: dict[str,Any], events: list[list[Any]]) -> dict[str,Any]:
    state=copy.deepcopy(initial)
    for i,event in enumerate(events):
        failed=reasons(state,event)
        if failed: return {"accepted":False,"rejection_index":i,"reasons":failed,"final_state":state}
        state=apply(state,event)
    closed=set(state["acknowledged"]+state["compensated"]+state["residualized"])
    unclosed=sorted(set(state["observed"])-closed)
    if unclosed: return {"accepted":False,"rejection_index":len(events),"reasons":["observed_effect_left_open"],"final_state":state}
    return {"accepted":True,"rejection_index":None,"reasons":[],"final_state":state}

def mutation_suite(base: dict[str,Any]) -> list[tuple[str,list[list[Any]]]]:
    e=base["events"]
    def changed(index:int, field:int, value:Any):
        x=copy.deepcopy(e); x[index][field]=value; return x
    return [
      ("zero id",changed(0,1,0)), ("stale epoch",changed(0,2,6)),
      ("time regression",changed(3,3,0)), ("unknown observation",changed(2,1,99)),
      ("duplicate observation",copy.deepcopy(e[:3])+[copy.deepcopy(e[2])]),
      ("ack wrong effect",changed(4,1,2)), ("ack missing receipt",changed(4,4,False)),
      ("residual missing receipt",changed(5,4,False)),
      ("double terminal",copy.deepcopy(e)+[["compensate",1,7,4,True]]),
      ("remove acknowledgement",copy.deepcopy(e[:4])+copy.deepcopy(e[5:])),
      ("remove residual custody",copy.deepcopy(e[:5])),
      ("revoke then retry",copy.deepcopy(e)+[["revoke",0,7,4,True],["attempt",1,7,4,False]])
    ]

def build() -> tuple[dict[str,Any],list[str]]:
    corpus=load(CORPUS); errors=[]
    source=ROOT/corpus["source_result_ref"]
    if sha(source)!=corpus["source_result_sha256"]: errors.append("source digest drift")
    source_data=load(source)
    if len(source_data.get("revocation_effect_attempts",[]))!=3 or len(source_data.get("residual_deltas",[]))!=2:
        errors.append("source concurrency/residual anchors drifted")
    receipts=[]
    for case in corpus["cases"]:
        outcome=run(corpus["initial_state"],case["events"])
        if outcome["accepted"]!=case["expected"]: errors.append(f"{case['id']}: expected {case['expected']}")
        receipts.append({"id":case["id"],"expected":case["expected"],"accepted":outcome["accepted"],"rejection_index":outcome["rejection_index"],"reasons":outcome["reasons"],"final_state":outcome["final_state"]})
    accepted=[r for r in receipts if r["accepted"]]
    mutations=mutation_suite(corpus["cases"][0]); rejected=sum(not run(corpus["initial_state"],events)["accepted"] for _,events in mutations)
    if rejected!=len(mutations): errors.append("one or more semantic mutations accepted")
    result={
      "schema_version":"asi_stack.concurrent_effect_ledger_result.v1","result_id":"concurrent-effect-ledger-2026-07-15-local",
      "corpus_sha256":sha(CORPUS),"source_result_sha256":sha(source),"lean_model_sha256":sha(LEAN),
      "case_count":len(receipts),"accepted_case_count":len(accepted),"rejected_case_count":len(receipts)-len(accepted),
      "accepted_event_count":sum(len(c["events"]) for c in corpus["cases"] if c["expected"]),
      "unique_effect_attempt_count":sum(len(set(r["final_state"]["attempted"])) for r in accepted),
      "acknowledged_effect_count":sum(len(r["final_state"]["acknowledged"]) for r in accepted),
      "compensated_effect_count":sum(len(r["final_state"]["compensated"]) for r in accepted),
      "residualized_effect_count":sum(len(r["final_state"]["residualized"]) for r in accepted),
      "revocation_count":sum(r["final_state"]["authority_epoch"]>7 for r in accepted),
      "mutation_count":len(mutations),"mutation_rejection_count":rejected,"receipts":receipts,
      "support_state_effect":"none","non_claims":["Finite logical-time interleavings do not establish distributed-clock or network-partition behavior.","Effect identity is treated as an idempotency key; real adapter enforcement and complete effect discovery are not established.","Source anchoring and mutation rejection do not establish deployment, safety, reproduction, transfer, or chapter-core support."]}
    try: jsonschema.Draft202012Validator(load(SCHEMA)).validate(result)
    except jsonschema.ValidationError as exc: errors.append(f"schema:{exc.message}")
    return result,errors

def main():
    p=argparse.ArgumentParser(); p.add_argument("--write",action="store_true"); a=p.parse_args(); result,errors=build()
    if errors: raise SystemExit("Concurrent effect ledger failed:\n - "+"\n - ".join(errors))
    if a.write: RESULT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    elif not RESULT.exists() or load(RESULT)!=result: raise SystemExit("Concurrent effect ledger result stale; run --write")
    print(f"Concurrent effect ledger passed: {result['case_count']} cases ({result['accepted_case_count']} accepted, {result['rejected_case_count']} rejected), {result['mutation_rejection_count']} mutations rejected, support effect none.")
if __name__=="__main__": main()
