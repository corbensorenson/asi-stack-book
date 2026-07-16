#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];P=ROOT/"proofs/proof_rationalization_reviews.json";PREFIX="lean/AsiStackProofs/ContextTransactions.lean::"
TARGETS={"lean:vcm.transactions.operational_invariant","lean:vcm.transactions.failure_blocks_promotion","lean:vcm.transactions.memory_store_fixture_bridge","lean:vcm.transactions.sequence_fixture_bridge"}
RETIRED={PREFIX+n for n in ["snapshot_read_sees_committed_event_in_declared_view","tainted_source_taints_derivative_without_declassification","current_memory_store_harness_summary_accepted","accepted_memory_store_harness_summary_requires_invalid_controls","current_context_transaction_sequence_summary_accepted","accepted_context_transaction_sequence_summary_requires_order"]}
REFS={"countermodel_refs":["lean/AsiStackProofs/ContextTransactionRefinement.lean#countermodels","experiments/context_transaction_memory_store/fixtures","experiments/context_transaction_sequence_bridge/fixtures"],"mutation_refs":["scripts/validate_context_transaction_refinement.py#mutations"],"consumer_refs":["docs:context_transaction_refinement","evidence_quality:model_adequacy_dossiers/context-transaction-refinement.md"],"runtime_consumer_refs":["scripts/validate_context_transaction_refinement.py","schemas/context_transaction_refinement.schema.json","experiments/context_transaction_refinement/results/2026-07-15-local.json","scripts/validate_context_transaction_memory_store.py","scripts/validate_context_transaction_sequence_bridge.py","lean/AsiStackProofs/ContextTransactionRefinement.lean"],"replacement_refs":["proof-model:vcm-transactions.reachable-snapshot-store-refinement.v1","lean/AsiStackProofs/ContextTransactionRefinement.lean"]}
def attach(r):
 for k,v in REFS.items():r[k]=list(dict.fromkeys([*r.get(k,[]),*v]))
def main():
 v=json.loads(P.read_text());ts=v["target_reviews"];ths=v["theorem_reviews"]
 if TARGETS-set(ts) or RETIRED-set(ths):raise SystemExit("missing transaction lineage")
 for t in TARGETS:
  r=ts[t];attach(r);r["semantic_role"]="Reachable snapshot/write/commit/read/derive/materialize semantics with exact identity, version, taint, deletion, replay, audit, and receipt custody.";r["assumptions"]=["Identifiers, policies, taint/deletion facts, epochs, receipts, and local fixtures are trusted inside the finite sequential model."];r["excluded_effects"]=["Concurrency, distributed isolation, crash recovery, replay determinism, deployed storage, erasure, side channels, natural workloads, reproduction, transfer, safety, SOTA, and core support are excluded."];r["review_rationale"]="Replace copied/projection ownership with reachable transaction semantics and an independent exact-suite consumer without support promotion."
 ids=[k for k in ths if k.startswith(PREFIX)]
 for k in ids:attach(ths[k])
 for k in RETIRED:ths[k]["review_rationale"]="Frozen lineage retained; declaration physically retired and superseded by reachable transaction semantics, exact fixture-suite consumption, and 78 mutations."
 P.write_text(json.dumps(v,indent=2)+"\n");print(f"Attached transaction refs to 4 targets and {len(ids)} theorems; 6 declarations retired.")
if __name__=="__main__":main()
