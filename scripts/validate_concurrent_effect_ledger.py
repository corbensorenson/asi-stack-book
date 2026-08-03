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

def run(initial: dict[str,Any], events: list[list[Any]], require_closed: bool = True) -> dict[str,Any]:
    state=copy.deepcopy(initial)
    for i,event in enumerate(events):
        failed=reasons(state,event)
        if failed: return {"accepted":False,"rejection_index":i,"reasons":failed,"final_state":state}
        state=apply(state,event)
    closed=set(state["acknowledged"]+state["compensated"]+state["residualized"])
    unclosed=sorted(set(state["observed"])-closed)
    if require_closed and unclosed: return {"accepted":False,"rejection_index":len(events),"reasons":["observed_effect_left_open"],"final_state":state}
    return {"accepted":True,"rejection_index":None,"reasons":[],"final_state":state}

def mutation_suite(cases: list[dict[str,Any]]) -> list[tuple[str,list[list[Any]]]]:
    mutations: list[tuple[str,list[list[Any]]]] = []
    for case in cases:
        events = case["events"]
        for index, event in enumerate(events):
            for field, value, label in ((0, "unknown", "kind"), (3, -1, "time")):
                changed = copy.deepcopy(events)
                changed[index][field] = value
                mutations.append((f"{case['id']}:{index}:{label}", changed))
            kind = event[0]
            controls: list[tuple[int, Any, str]] = []
            if kind == "attempt":
                controls = [(1, 0, "zero-id"), (2, 6, "stale-epoch")]
            elif kind == "observe":
                controls = [(1, 99, "unknown-effect")]
            elif kind in {"acknowledge", "compensate", "residualize"}:
                controls = [(1, 99, "unknown-effect"), (4, False, "missing-receipt")]
            elif kind == "revoke":
                controls = [(2, 6, "stale-epoch")]
            for field, value, label in controls:
                changed = copy.deepcopy(events)
                changed[index][field] = value
                mutations.append((f"{case['id']}:{index}:{label}", changed))
    return mutations

def build() -> tuple[dict[str,Any],list[str]]:
    corpus=load(CORPUS); errors=[]
    source=ROOT/corpus["source_result_ref"]
    if sha(source)!=corpus["source_result_sha256"]: errors.append("source digest drift")
    source_data=load(source)
    if len(source_data.get("revocation_effect_attempts",[]))!=3 or len(source_data.get("residual_deltas",[]))!=2:
        errors.append("source concurrency/residual anchors drifted")
    receipts=[]
    accepted_cases=[]
    for case in corpus["cases"]:
        outcome=run(corpus["initial_state"],case["events"])
        if outcome["accepted"]!=case["expected"]: errors.append(f"{case['id']}: expected {case['expected']}")
        if case["expected"]:
            accepted_cases.append(case)
        receipts.append({"id":case["id"],"expected":case["expected"],"accepted":outcome["accepted"],"rejection_index":outcome["rejection_index"],"reasons":outcome["reasons"],"final_state":outcome["final_state"]})
    accepted=[r for r in receipts if r["accepted"]]
    prefix_checks=0; composition_checks=0; logical_time_checks=0; authority_epoch_checks=0; closure_checks=0
    for case in accepted_cases:
        state=copy.deepcopy(corpus["initial_state"]); states=[copy.deepcopy(state)]
        for index,event in enumerate(case["events"]):
            failed=reasons(state,event)
            if failed:
                errors.append(f"{case['id']}: accepted prefix {index} rejected: {failed}")
                break
            next_state=apply(state,event)
            if next_state["logical_time"]<state["logical_time"]: errors.append(f"{case['id']}: logical time regressed at {index}")
            if next_state["authority_epoch"]<state["authority_epoch"]: errors.append(f"{case['id']}: authority epoch regressed at {index}")
            logical_time_checks+=1; authority_epoch_checks+=1
            state=next_state; states.append(copy.deepcopy(state))
        prefix_checks+=len(states)
        closed=set(state["acknowledged"]+state["compensated"]+state["residualized"])
        if set(state["observed"]).issubset(closed): closure_checks+=1
        else: errors.append(f"{case['id']}: terminal disposition closure failed")
        expected_final=state
        for split in range(len(case["events"])+1):
            prefix=run(corpus["initial_state"],case["events"][:split],require_closed=False)
            suffix=run(prefix["final_state"],case["events"][split:]) if prefix["accepted"] else {"accepted":False}
            if prefix["accepted"] and suffix["accepted"] and suffix["final_state"]==expected_final: composition_checks+=1
            else: errors.append(f"{case['id']}: composition mismatch at split {split}")

    authored_one_effect=[["attempt",1,7,1,False],["observe",1,7,2,False],["acknowledge",1,7,3,True]]
    projection=run(corpus["initial_state"],authored_one_effect)
    projection_witness_checks=int(
        projection["accepted"] and len(projection["final_state"]["attempted"])==1 and
        len(projection["final_state"]["acknowledged"])==1 and
        len(projection["final_state"]["residualized"])==0
    )
    if projection_witness_checks!=1: errors.append("authored one-effect projection witness failed")

    mutations=mutation_suite(accepted_cases); rejected=sum(not run(corpus["initial_state"],events)["accepted"] for _,events in mutations)
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
      "lifecycle_prefix_check_count":prefix_checks,"composition_split_count":composition_checks,
      "logical_time_check_count":logical_time_checks,"authority_epoch_check_count":authority_epoch_checks,
      "terminal_disposition_check_count":closure_checks,"projection_witness_check_count":projection_witness_checks,
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
