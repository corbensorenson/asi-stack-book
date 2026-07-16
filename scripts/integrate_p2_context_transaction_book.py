#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];S=ROOT/"book_structure.json";T=ROOT/"proofs/proof_triage.json"
TARGETS={"lean:vcm.transactions.operational_invariant":"Accepted reads preserve exact snapshot, branch, mount, cell, committed version, and replay custody before materialization.","lean:vcm.transactions.failure_blocks_promotion":"Taint removal requires represented declassification authority and receipt; open deletion or support promotion without its receipt blocks materialization.","lean:vcm.transactions.memory_store_fixture_bridge":"The reachable model is consumed alongside the exact 3-valid/6-invalid memory-store suite and 78-mutation independent checker.","lean:vcm.transactions.sequence_fixture_bridge":"The six-event ordered witness is consumed alongside the exact 2-valid/4-invalid sequence suite and rejects read-before-write and missing-replay faults."}
def main():
 v=json.loads(S.read_text());c=next(c for p in v["parts"] for c in p["chapters"] if c["id"]=="context-transactions-snapshots-mounts-and-taint")
 for x in c["proof_targets"]:
  if x["tag"] in TARGETS:x["target"]=TARGETS[x["tag"]];x["module"]="AsiStackProofs.ContextTransactionRefinement"
 name="Executed snapshot transaction and taint/deletion refinement"
 if not any(x.get("name")==name for x in c["codex_tests"]):c["codex_tests"].append({"name":name,"purpose":"Refine snapshot/write/commit/read/derive/materialize order and custody against both transaction fixture families.","implementation_status":"implemented","result_status":"passes via `python3 scripts/validate_context_transaction_refinement.py`: 3/6 store fixtures, 2/4 sequences, 6 events, 78/78 rejected mutations; support effect none","status":"bounded sequential model; no concurrency, distributed isolation, crash recovery, deployed storage, erasure, reproduction, transfer, safety, or core-support claim"})
 S.write_text(json.dumps(v,indent=2)+"\n");q=json.loads(T.read_text())
 for r in q["records"]:
  if r.get("tag") in TARGETS:r["formal_target"]=TARGETS[r["tag"]];r["module"]="AsiStackProofs.ContextTransactionRefinement";r["rationale"]="Reachable transaction model plus exact 3/6 store, 2/4 sequence, and 78-mutation consumer; support effect none."
 T.write_text(json.dumps(q,indent=2)+"\n");print("Integrated four Context Transaction targets.")
if __name__=="__main__":main()
