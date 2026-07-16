#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];STRUCTURE=ROOT/'book_structure.json';TRIAGE=ROOT/'proofs/proof_triage.json';REVIEWS=ROOT/'proofs/proof_rationalization_reviews.json'
CHAPTER='scalable-oversight-and-adversarial-ai-control';MODULE='AsiStackProofs.ScalableOversightRefinement'
TARGETS={
'lean:scalable_oversight.high_risk.missing_outcome_audit_blocks_admission':'A reachable high-risk review lifecycle without an independent outcome-audit record blocks bounded-use adjudication without mutating lifecycle state or inferring reviewer competence.',
'lean:scalable_oversight.use.complete_bounded_admission':'A complete versioned review lifecycle emits only one bounded-use handoff to its named consumer and assigns neither support nor an external effect.',
'lean:scalable_oversight.use.missing_evidence_views_requires_repair':'Missing bound evidence views block review recording without mutating lifecycle state.',
'lean:scalable_oversight.use.undisclosed_dependencies_require_review':'Missing shared-dependency disclosure blocks independent outcome-audit admission without treating role separation as reviewer independence.',
'lean:scalable_oversight.use.missing_outcome_audit_requires_audit':'A high-risk reviewed record without an independent outcome audit cannot advance to use adjudication.',
'lean:scalable_oversight.use.unjustified_abstention_requires_evidence':'An abstention request without evidence and a defeater cannot advance to its accountable escalation disposition.',
'lean:scalable_oversight.use.authority_laundering_rejected':'A bounded-use request without preserved release- and policy-authority separation is rejected and cannot assign support or an external effect.'}
PREFIX='lean/AsiStackProofs/ScalableOversight.lean::'
REFS={'countermodel_refs':['lean/AsiStackProofs/ScalableOversightRefinement.lean#countermodels'],'mutation_refs':['scripts/validate_scalable_oversight_refinement.py#mutations'],'consumer_refs':['docs:scalable_oversight_refinement','evidence_quality:model_adequacy_dossiers/scalable-oversight-refinement.md'],'runtime_consumer_refs':['scripts/validate_scalable_oversight_refinement.py','schemas/scalable_oversight_refinement.schema.json','experiments/scalable_oversight_refinement/results/2026-07-15-local.json','scripts/validate_scalable_oversight_protocol.py'],'replacement_refs':['proof-model:scalable-oversight-refinement.v1','lean/AsiStackProofs/ScalableOversightRefinement.lean']}
def attach(row):
 for k,v in REFS.items():row[k]=list(dict.fromkeys([*row.get(k,[]),*v]))
def main():
 s=json.loads(STRUCTURE.read_text());c=next(c for p in s['parts'] for c in p['chapters'] if c['id']==CHAPTER)
 for t in c['proof_targets']:
  if t['tag'] in TARGETS:t['module']=MODULE;t['target']=TARGETS[t['tag']]
 c['lean_module']='AsiStackProofs.ScalableOversight; AsiStackProofs.ScalableOversightRefinement'
 c['minimal_implementation']='The exact current minimum preserves the seven inherited oversight cases in a seven-stage, 58-route oversight-review lifecycle with 65/65 rejecting mutations, twelve ScalableOversightRefinement declarations, one bounded-use handoff, and one protocol-version-2 readmission witness. It runs no model, reviewer, human, debate, consultancy, weak-to-strong learner, natural task, outcome workload, causal intervention, release, deployment, reproduction, transfer, chapter-core transition, or SOTA comparison.'
 c['open_evidence_gaps']=['No ASI Stack model, natural task cohort, human reviewer, AI judge, debater, consultant, weak-to-strong learner, outcome workload, causal intervention, release, incident, reproduction, or transfer has run.','No local result establishes reviewer competence, independence, calibration, outcome truth, protocol efficacy, debate or consultancy value, weak-to-strong generalization, causal usefulness, readiness, safety, or deployment authority.','The seven-stage lifecycle, 58-route consumer, and 65 rejecting mutations establish only structured oversight-review record consequences; all identities, protocol fields, review outcomes, audits, disagreements, abstentions, invalidation assertions, and authority fields remain trusted.','Run the prospectively frozen matched direct/assisted/adversarial review campaign with independent outcomes, correlated-reviewer negatives, natural and ambiguous tasks, causal ablations, heterogeneous transfer, and operator-cost reporting before considering empirical support movement.']
 c['codex_tests']=[x for x in c['codex_tests'] if not(isinstance(x,dict) and x.get('name')=='Scalable-oversight review-lifecycle refinement')]
 c['codex_tests'].append({'name':'Scalable-oversight review-lifecycle refinement','implementation_status':'implemented','result_status':'passes the exact seven-case suite, 58 routes, seven reachable stages, and 65/65 rejecting mutations; one bounded-use handoff returns to scoped protocol binding only through version-2 readmission; support/effect none; no reviewer-competence, independence, calibration, outcome-validity, efficacy, release, transfer, or support claim'})
 STRUCTURE.write_text(json.dumps(s,indent=2)+'\n')
 t=json.loads(TRIAGE.read_text())
 for row in t['records']:
  if row['tag'] in TARGETS:row['module']=MODULE;row['formal_target']=TARGETS[row['tag']];row['rationale']='Reachable oversight-review lifecycle with prospective scope/protocol custody, review, independent-audit, adjudication, bounded-use handoff, and successor-version readmission boundaries, 58 routes, 65 rejecting mutations, and no support/effect authority.'
 TRIAGE.write_text(json.dumps(t,indent=2)+'\n')
 r=json.loads(REVIEWS.read_text())
 for target in TARGETS:
  row=r['target_reviews'][target];attach(row);row['semantic_role']='Reachable scope-to-protocol-to-review-to-audit-to-adjudication-to-bounded-use lifecycle with exact identity, abstention, authority, invalidation, and successor-version boundaries.';row['assumptions']=['Task/consumer/protocol/cohort/system/supervisor/evidence/dependency/baseline/auditor/policy/residual/authority, review, outcome, abstention, invalidation, and protocol-version records are trusted inside the finite authored model.'];row['excluded_effects']=['Reviewer competence, independence, calibration, outcome truth, protocol efficacy, debate/consultancy/weak-to-strong value, causal usefulness, readiness, safety, release execution, deployed invalidation, transfer, and chapter-core support are excluded.'];row['review_rationale']='Strengthen disconnected route reductions with a reachable versioned review lifecycle, independent replay, fifty-eight routes, and 65 rejecting mutations.'
 ids=[k for k in r['theorem_reviews'] if k.startswith(PREFIX)]
 for k in ids:attach(r['theorem_reviews'][k])
 REVIEWS.write_text(json.dumps(r,indent=2)+'\n');print(f'Integrated Scalable Oversight refinement across {len(TARGETS)} targets and {len(ids)} frozen declarations.')
if __name__=='__main__':main()
