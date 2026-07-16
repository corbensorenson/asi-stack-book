#!/usr/bin/env python3
"""Attach the reachable Human Intent refinement to frozen P2 lineage."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];REVIEWS=ROOT/"proofs/proof_rationalization_reviews.json"
TARGETS={"lean:intent.contract.operational_invariant","lean:intent.contract.failure_blocks_promotion","lean:intent.resolution.route_envelope","lean:intent.intake.probe_fixture_bridge"}
PREFIX="lean/AsiStackProofs/IntentContracts.lean::"
RETIRED={PREFIX+x for x in ["compiled_intent_contract_preserves_declared_constraints_and_stop_conditions","contract_missing_required_authority_cannot_compile_to_executable_job","intent_intake_probe_fixture_valid","intent_intake_probe_rejects_request_pressure","intent_intake_probe_preserves_no_promotion_boundary"]}
COUNTER=["lean/AsiStackProofs/IntentResolutionRefinement.lean#countermodels","experiments/intent_recontract_probe/results/2026-07-02-local.json#expected_invalid_controls","experiments/plan_execution_contracts/fixtures"]
MUT=["scripts/validate_intent_resolution_refinement.py#mutations"]
CONS=["chapter:human-intent-as-a-formal-input#formalization-hooks","docs:intent_resolution_refinement","evidence_quality:model_adequacy_dossiers/intent-resolution-refinement.md"]
RUN=["scripts/validate_intent_resolution_refinement.py","schemas/intent_resolution_refinement.schema.json","experiments/intent_resolution_refinement/results/2026-07-15-local.json","experiments/intent_intake_probe/results/2026-07-02-local.json","experiments/intent_recontract_probe/results/2026-07-02-local.json","experiments/plan_execution_contracts/fixtures","lean/AsiStackProofs/IntentResolutionRefinement.lean"]
REPL=["proof-model:intent.reachable-resolution-contract-refinement.v1","lean/AsiStackProofs/IntentResolutionRefinement.lean"]
def merge(a,b):return list(dict.fromkeys([*a,*b]))
def attach(r):
 for k,v in (("countermodel_refs",COUNTER),("mutation_refs",MUT),("consumer_refs",CONS),("runtime_consumer_refs",RUN),("replacement_refs",REPL)):r[k]=merge(r.get(k,[]),v)
def main():
 v=json.loads(REVIEWS.read_text());ts=v["target_reviews"];ths=v["theorem_reviews"]
 if TARGETS-set(ts) or RETIRED-set(ths):raise SystemExit("missing frozen intent lineage")
 roles={"lean:intent.contract.operational_invariant":"Reachable request-to-contract compilation preserves exact root, versioned constraint/stop hashes, and approved authority before acceptance.","lean:intent.contract.failure_blocks_promotion":"Countermodels and thirty mutations reject missing payload, prohibition, hidden override, authority widening, semantic-token substitution, silent material deltas, and unreceipted re-contract.","lean:intent.resolution.route_envelope":"Twenty finite resolution/admission branches remain bounded negative cases consumed alongside the reachable model and fixed local fixture inventories.","lean:intent.intake.probe_fixture_bridge":"The four-valid/six-invalid intake surface is digest-bound to the new consumer alongside nine re-contract scenarios and thirteen plan fixtures rather than normalized into literal Lean summary theorems."}
 for tid in TARGETS:
  r=ts[tid];attach(r);r["semantic_role"]=roles[tid];r["assumptions"]=["Structured hashes, authority, receipts, scenario labels, and finite local records are trusted only within the declared bounded model."];r["excluded_effects"]=["Natural-language understanding, semantic completeness, authentic authority extraction, prompt-injection containment, deployed dispatch/effects, natural workloads, reproduction, transfer, safety, SOTA, and chapter-core support are excluded."];r["review_rationale"]="Resolve frozen Human Intent lineage to a reachable request-to-contract model and independently encoded local-record consumer without support promotion."
 ids=[x for x in ths if x.startswith(PREFIX)]
 for x in ids:attach(ths[x])
 for x in RETIRED:ths[x]["review_rationale"]="Frozen lineage retained; the assumption/literal-summary declaration is physically retired and superseded by the reachable model, consumer, countermodels, and thirty mutations."
 REVIEWS.write_text(json.dumps(v,indent=2)+"\n");print(f"Attached intent-resolution refs to {len(TARGETS)} targets and {len(ids)} theorems; {len(RETIRED)} declarations retired.")
if __name__=="__main__":main()
