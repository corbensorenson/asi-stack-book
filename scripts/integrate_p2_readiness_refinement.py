#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; STRUCTURE=ROOT/'book_structure.json';TRIAGE=ROOT/'proofs/proof_triage.json';REVIEWS=ROOT/'proofs/proof_rationalization_reviews.json'
MODULE='AsiStackProofs.ReadinessRefinement'
TARGETS={
'lean:readiness.gates.operational_invariant':'A reachable readiness lifecycle preserves exact capability, implementation, model-state, workload, baseline, evaluator, policy, authority, consumer, fallback, and residual custody from candidate through acknowledged terminal closure while separating ordinary release, quarantine, support, and external effects.',
'lean:readiness.gates.failure_blocks_promotion':'Missing workload, baseline, evaluator, non-claims, fresh shadow evidence, regression floor, residual escrow, fallback, rollback, monitoring, canary outcome accounting, independent evaluation, transfer, delayed outcomes, transitive quarantine, route blocking, or terminal revocation custody blocks lifecycle progress.',
'lean:readiness.gates.lifecycle_probe_bridge':'The independent consumer preserves three exact readiness suites, all forty lifecycle routes, the six-receipt terminal witness, and forty-five rejecting identity, gate, replay, and authority-leak mutations without assigning support or external effects.'}
PREFIX='lean/AsiStackProofs/ReadinessGates.lean::'
RETIRED={PREFIX+n for n in ['promoted_decision_requires_all_required_gates','readiness_lifecycle_transition_must_be_forward_or_terminal','allowed_readiness_transition_requires_core_records','qualified_readiness_requires_regression_floor','default_readiness_requires_regression_authority_and_route','quarantine_transition_blocks_ordinary_and_requires_fallback','supersession_requires_record_and_residual_escrow','retirement_requires_receipt_and_residual_escrow','readiness_lifecycle_probe_fixture_bridge']}
REFS={'countermodel_refs':['lean/AsiStackProofs/ReadinessRefinement.lean#countermodels'],'mutation_refs':['scripts/validate_readiness_refinement.py#mutations'],'consumer_refs':['docs:readiness_refinement','evidence_quality:model_adequacy_dossiers/readiness-refinement.md'],'runtime_consumer_refs':['scripts/validate_readiness_refinement.py','schemas/readiness_refinement.schema.json','experiments/readiness_refinement/results/2026-07-15-local.json','scripts/validate_readiness_residual_gates.py','scripts/validate_readiness_lifecycle_probe.py','scripts/validate_readiness_check_lifecycle.py'],'replacement_refs':['proof-model:readiness-refinement.v1','lean/AsiStackProofs/ReadinessRefinement.lean']}
def attach(row):
 for k,v in REFS.items():row[k]=list(dict.fromkeys([*row.get(k,[]),*v]))
def main():
 s=json.loads(STRUCTURE.read_text());c=next(c for p in s['parts'] for c in p['chapters'] if c['id']=='readiness-gates-residual-escrow-and-quarantine')
 for t in c['proof_targets']:
  if t['tag'] in TARGETS:t['module']=MODULE;t['target']=TARGETS[t['tag']]
 c['lean_module']='AsiStackProofs.ReadinessGates; AsiStackProofs.ReadinessRefinement'
 c['codex_tests']=[x for x in c['codex_tests'] if not(isinstance(x,dict) and x.get('name')=='Readiness candidate-to-terminal refinement')]
 c['codex_tests'].append({'name':'Readiness candidate-to-terminal refinement','implementation_status':'implemented','result_status':'passes three exact suites, 40 routes, seven reachable stages, and 45/45 rejecting mutations; one ordinary release, quarantine, and terminal closure remain separate; support-state effect none; no evaluator adequacy, calibration, natural usefulness, effect-complete rollback, deployed quarantine/revocation, transfer, or support claim'})
 STRUCTURE.write_text(json.dumps(s,indent=2)+'\n')
 t=json.loads(TRIAGE.read_text())
 for row in t['records']:
  if row['tag'] in TARGETS:row['module']=MODULE;row['formal_target']=TARGETS[row['tag']];row['rationale']='Reachable seven-stage readiness lifecycle with exact custody, three bounded suites, 40 routes, 45 rejecting mutations, and no support/effect authority.'
 TRIAGE.write_text(json.dumps(t,indent=2)+'\n')
 r=json.loads(REVIEWS.read_text())
 for target in TARGETS:
  row=r['target_reviews'][target];attach(row);row['semantic_role']='Reachable candidate, shadow, canary, qualified, default, quarantine, and terminal lifecycle with exact custody and separate release/quarantine/effect accounting.';row['assumptions']=['Capability, implementation, model-state, workload, baseline, evaluator, policy, authority, consumer, fallback, residual, evidence, outcome, quarantine, revocation, and acknowledgment fields are trusted inside the finite authored model.'];row['excluded_effects']=['Evidence truth, evaluator competence or independence, threshold calibration, natural usefulness, effect-complete rollback, deployed quarantine/revocation, transfer, safety, SOTA, and chapter-core support are excluded.'];row['review_rationale']='Replace definition unpacking and fixture-summary restatement with a reachable readiness lifecycle, three exact suites, forty routes, and 45 rejecting mutations.'
 ids=[k for k in r['theorem_reviews'] if k.startswith(PREFIX)]
 for k in ids:attach(r['theorem_reviews'][k])
 for k in RETIRED:
  row=r['theorem_reviews'][k];row['review_state']='terminally_dispositioned';row['disposition']='replace_with_stronger_model';row['review_rationale']='Frozen lineage retained; declaration physically retired because it unpacked an assumed predicate or fixture summary now subsumed by the reachable refinement.'
 REVIEWS.write_text(json.dumps(r,indent=2)+'\n');print(f'Integrated Readiness refinement across 3 targets and {len(ids)} frozen declarations; {len(RETIRED)} declarations retired.')
if __name__=='__main__':main()
