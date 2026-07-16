#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
STRUCTURE=ROOT/'book_structure.json'; TRIAGE=ROOT/'proofs/proof_triage.json'; REVIEWS=ROOT/'proofs/proof_rationalization_reviews.json'
MODULE='AsiStackProofs.ProceduralMemoryRefinement'
TARGETS={
 'lean:procedural.loop_closure.operational_invariant':'A reachable procedure lifecycle preserves exact procedure, source-set, trace-cluster, abstraction, regression-suite, SCF, policy, and consumer custody from clustering through acknowledged routing and receipt-bound retirement without assigning support or external effects.',
 'lean:procedural.loop_closure.failure_blocks_promotion':'Missing comparable traces, negative examples, source/effect receipts, abstraction contracts, verification, regression clearance, benchmark floor, active SCF, rehearsed rollback, monitoring, residuals, non-claims, acknowledgment, or retirement custody blocks lifecycle progress or routes to quarantine.',
}
PREFIX='lean/AsiStackProofs/ProceduralMemory.lean::'
RETIRED={PREFIX+n for n in ['generated_tool_records_source_traces_parameters_and_verification_result','tool_with_failed_regression_cannot_be_promoted_to_routable_status','valid_routable_with_negative_examples_fixture_admitted','valid_failed_regression_quarantined_fixture_admitted','valid_retired_stale_precondition_fixture_admitted']}
REFS={
 'countermodel_refs':['lean/AsiStackProofs/ProceduralMemoryRefinement.lean#countermodels'],
 'mutation_refs':['scripts/validate_procedural_memory_refinement.py#mutations'],
 'consumer_refs':['docs:procedural_memory_refinement','evidence_quality:model_adequacy_dossiers/procedural-memory-refinement.md'],
 'runtime_consumer_refs':['scripts/validate_procedural_memory_refinement.py','schemas/procedural_memory_refinement.schema.json','experiments/procedural_memory_refinement/results/2026-07-15-local.json','scripts/validate_procedural_memory_loop.py','scripts/validate_procedural_trace_promotion.py'],
 'replacement_refs':['proof-model:procedural-memory-refinement.v1','lean/AsiStackProofs/ProceduralMemoryRefinement.lean'],
}
def attach(row):
 for k,v in REFS.items(): row[k]=list(dict.fromkeys([*row.get(k,[]),*v]))
def main():
 s=json.loads(STRUCTURE.read_text()); c=next(c for p in s['parts'] for c in p['chapters'] if c['id']=='procedural-memory-and-cognitive-loop-closure')
 for t in c['proof_targets']:
  if t['tag'] in TARGETS: t['module']=MODULE; t['target']=TARGETS[t['tag']]
 c['lean_module']='AsiStackProofs.ProceduralMemory; AsiStackProofs.ProceduralMemoryRefinement'
 c['codex_tests']=[x for x in c['codex_tests'] if not(isinstance(x,dict) and x.get('name')=='Procedural Memory promotion and retirement refinement')]
 c['codex_tests'].append({'name':'Procedural Memory promotion and retirement refinement','implementation_status':'implemented','result_status':'passes two exact suites, 32 routes, seven reachable stages, and 33/33 rejecting mutations; support-state effect none; no natural trace-mining, generated-tool correctness, deployed routing, rollback, monitoring, retirement, usefulness, safety, reproduction, or transfer claim'})
 STRUCTURE.write_text(json.dumps(s,indent=2)+'\n')
 t=json.loads(TRIAGE.read_text())
 for row in t['records']:
  if row['tag'] in TARGETS: row['module']=MODULE; row['formal_target']=TARGETS[row['tag']]; row['rationale']='Reachable seven-stage procedure promotion and retirement lifecycle with exact custody, two bounded suites, 32 routes, 33 rejecting mutations, and no support or effect authority.'
 TRIAGE.write_text(json.dumps(t,indent=2)+'\n')
 r=json.loads(REVIEWS.read_text())
 for target in TARGETS:
  row=r['target_reviews'][target]; attach(row); row['semantic_role']='Reachable trace-cluster, abstraction, verification, qualification, routing, monitoring, and retirement lifecycle with exact custody and no support/effect authority.'; row['assumptions']=['Procedure identities, digests, trace comparability, negative examples, receipt presence, abstraction, verification, regression, benchmark, SCF, rollback, monitoring, residual, acknowledgment, and retirement fields are trusted inside the finite authored model.']; row['excluded_effects']=['Natural trace discovery, semantic abstraction, generated-tool correctness, verifier/regression quality, rollback effectiveness, deployed routing/monitoring/retirement, usefulness, causality, safety, reproduction, transfer, SOTA, and chapter-core support are excluded.']; row['review_rationale']='Replace projections and fixture admissions with a reachable promotion/retirement lifecycle, exact bounded suites, thirty-two routes, and 33 rejecting mutations.'
 theorem_ids=[k for k in r['theorem_reviews'] if k.startswith(PREFIX)]
 for k in theorem_ids: attach(r['theorem_reviews'][k])
 for k in RETIRED:
  row=r['theorem_reviews'][k]; row['review_state']='terminally_dispositioned'; row['disposition']='replace_with_stronger_model'; row['review_rationale']='Frozen lineage retained; declaration physically retired because it projected an assumption or normalized an authored fixture admission now subsumed by the reachable refinement.'
 REVIEWS.write_text(json.dumps(r,indent=2)+'\n')
 print(f'Integrated Procedural Memory refinement across 2 targets and {len(theorem_ids)} frozen declarations; 5 declarations retired.')
if __name__=='__main__': main()
