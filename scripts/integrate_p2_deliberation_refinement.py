#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
STRUCTURE=ROOT/"book_structure.json";TRIAGE=ROOT/"proofs/proof_triage.json";REVIEWS=ROOT/"proofs/proof_rationalization_reviews.json"
MODULE="AsiStackProofs.DeliberationRefinement"
TARGETS={
"lean:deliberation.high_risk.missing_independent_verifier_blocks_execution":"High-risk evaluation without an independent-enough review record is blocked before selection or planning handoff.",
"lean:deliberation.budget_exhausted.escrows_residual":"Budget or dispute exhaustion requires an owned residual before bounded planning handoff.",
"lean:deliberation.complete_high_risk.reaches_planning":"A complete seven-receipt lifecycle reaches a bounded planning handoff and closure without execution, support, or external-effect authority.",
"lean:deliberation.missing_budget.requires_review":"Candidate generation requires a prospectively bound budget and budget identity.",
"lean:deliberation.missing_search_mode.requires_review":"Candidate generation requires a registered deliberation mode policy.",
"lean:deliberation.missing_verifier_scope.requires_review":"Evaluation requires explicit obligations, verifier identity, evidence view, dependence, calibration, abstention, and false-decision boundaries.",
"lean:deliberation.missing_candidate_history.requires_review":"Candidate generation requires first-candidate capture, complete history, trace privacy, and the complete attempt denominator.",
"lean:deliberation.missing_stop_condition.requires_review":"Candidate generation and handoff require prospectively bound stop rules and a stop receipt.",
"lean:deliberation.missing_residual_owner.requires_review":"No verified candidate, exhausted budget, or unresolved dispute routes through residual escrow and closure.",
"lean:deliberation.trace_authority_laundering.requires_review":"Raw scores, traces, and a planning handoff cannot grant support or execution authority."
}
PREFIX="lean/AsiStackProofs/Deliberation.lean::"
RETAINED={"missing_independent_verifier_blocks_high_risk_execution","trace_cannot_launder_execution_authority"}
REFS={"countermodel_refs":["lean/AsiStackProofs/DeliberationRefinement.lean#countermodels"],"mutation_refs":["scripts/validate_deliberation_refinement.py#route_cases"],"consumer_refs":["docs:deliberation_refinement","evidence_quality:model_adequacy_dossiers/deliberation-refinement.md"],"runtime_consumer_refs":["scripts/validate_deliberation_refinement.py","schemas/deliberation_refinement.schema.json","experiments/deliberation_refinement/results/2026-07-15-local.json","scripts/validate_deliberation_admission.py","scripts/validate_post_v2_routing_deliberation.py","scripts/validate_post_v2_1_outcomes.py","experiments/post_v2_1_evidence_program/p2/results/test.json","experiments/post_v2_1_evidence_program/results/2026-07-11-post-v2-1-outcomes.json"],"replacement_refs":["proof-model:deliberation.request-to-closure-refinement.v1","lean/AsiStackProofs/DeliberationRefinement.lean"]}

def attach(r:dict)->None:
 for k,refs in REFS.items():r[k]=list(dict.fromkeys([*r.get(k,[]),*refs]))

def main()->None:
 s=json.loads(STRUCTURE.read_text());c=next(c for p in s["parts"] for c in p["chapters"] if c["id"]=="governed-deliberation-and-test-time-scaling")
 for t in c["proof_targets"]:
  if t["tag"] in TARGETS:t["module"]=MODULE;t["target"]=TARGETS[t["tag"]]
 c["lean_module"]="AsiStackProofs.Deliberation; AsiStackProofs.DeliberationRefinement"
 c["minimal_implementation"]="The current minimum contains two retained general countermodels plus an eleven-declaration, eight-stage, 59-route request-to-closure lifecycle; an independent consumer rejecting 51/51 non-accepting mutations and digest-binding the ten-case admission, three-seed post-v2 routing/deliberation result, and later actual-model 0/60 no-change result; one reachable residual-escrow route and one bounded planning handoff; fifteen preserved fixed-step harms, zero observed synthetic fallback activations, and no support or external effect. Eight flat route consequences are retired. This is bounded policy/conformance evidence plus a failed actual-model attempt, not useful language-model reasoning, natural-workload usefulness, verifier adequacy, trace faithfulness, calibrated routing or abstention, planning execution, transfer, or SOTA evidence."
 retired={"High-risk independent-verifier admission fixture","Budget-exhaustion residual fixture"}
 c["codex_tests"]=[x for x in c["codex_tests"] if not(isinstance(x,dict) and x.get("name") in retired)]
 c["codex_tests"].append({"name":"Governed Deliberation request-to-closure refinement","implementation_status":"implemented","result_status":"passes eight stages, all 59 routes, 51/51 non-accepting mutations, three digest-bound source families including the actual-model 0/60 no-change result, fifteen preserved harms, zero synthetic fallback activations, residual escrow and bounded planning handoff, support/effect none; no useful-language-model, natural-usefulness, verifier, faithfulness, deployment, transfer, or support claim"})
 STRUCTURE.write_text(json.dumps(s,indent=2)+"\n")
 tri=json.loads(TRIAGE.read_text())
 for r in tri["records"]:
  if r["tag"] in TARGETS:r["module"]=MODULE;r["formal_target"]=TARGETS[r["tag"]];r["rationale"]="Reachable eight-stage request-to-closure lifecycle, 59 routes, 51 rejecting mutations, two digest-bound bounded results, and no execution/support/effect authority."
 TRIAGE.write_text(json.dumps(tri,indent=2)+"\n")
 rev=json.loads(REVIEWS.read_text())
 for tag in TARGETS:
  r=rev["target_reviews"][tag];attach(r);r["semantic_role"]="Reachable request scope, candidate custody, evaluation, corruption/repair/faithfulness accounting, selection, stop, residual, bounded planning handoff, and closure lifecycle.";r["assumptions"]=["All identities, policy gates, candidate/evaluator facts, verifier dependence, corruption, repair, faithfulness, cost, useful-metric, stop, residual, and acknowledgment fields are trusted inside the finite authored model."];r["excluded_effects"]=["Language-model reasoning, evaluator competence, real independence, trace faithfulness, useful throughput, calibrated routing/abstention, execution, safety, transfer, SOTA, and support are excluded."];r["review_rationale"]="Replace a flat admission predicate and copied fixture expectations with a reachable lifecycle and independently implemented digest-bound consumer."
 ids=[k for k in rev["theorem_reviews"] if k.startswith(PREFIX)];retired_count=0
 for k in ids:
  r=rev["theorem_reviews"][k];attach(r)
  if k.rsplit("::",1)[1] not in RETAINED:retired_count+=1;r["review_state"]="terminally_dispositioned";r["disposition"]="replace_with_stronger_model";r["review_rationale"]="Frozen lineage retained; declaration physically retired because the flat route consequence is subsumed by reachable stage, identity, custody, stop, residual, handoff, support, and effect semantics."
 REVIEWS.write_text(json.dumps(rev,indent=2)+"\n")
 print(f"Integrated Deliberation refinement across {len(TARGETS)} targets and {len(ids)} frozen declarations; {retired_count} retired and {len(RETAINED)} retained.")

if __name__=="__main__":main()
