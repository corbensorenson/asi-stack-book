#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];STRUCTURE=ROOT/'book_structure.json';TRIAGE=ROOT/'proofs/proof_triage.json';REVIEWS=ROOT/'proofs/proof_rationalization_reviews.json'
CHAPTER='capability-thresholds-and-deployment-commitments';MODULE='AsiStackProofs.CapabilityThresholdRefinement'
TARGETS={
'lean:capability_thresholds.crossed.missing_verified_safeguards_blocks_release':'A crossed-threshold lifecycle cannot reach control completion without a safeguard package, verifier, bypass test, and rollback plan.',
'lean:capability_thresholds.missing_evaluation_envelope.requires_reevaluation':'Missing evaluation envelope, elicitation, baseline, uncertainty, independent-evaluator, or assessment-result custody blocks assessment.',
'lean:capability_thresholds.complete_crossed.reaches_readiness_review':'A fully recorded crossed-threshold assessment can emit only a readiness handoff after control, monitoring, residual, authority, and release-path custody.',
'lean:capability_thresholds.complete_non_crossing.reaches_readiness_review':'A recorded non-crossing may bypass crossed-only safeguard gates but still requires monitoring, residual, authority, and release-path custody before readiness review.',
'lean:capability_thresholds.missing_baseline.requires_reevaluation':'Missing baseline blocks the scoped-to-assessed transition without mutating threshold state.',
'lean:capability_thresholds.missing_uncertainty.requires_reevaluation':'Missing assessment or decision uncertainty blocks lifecycle progress without converting absence into a non-crossing.',
'lean:capability_thresholds.missing_residual_owner.requires_exception':'Missing residual ownership blocks adjudication or readiness; an exception additionally requires owner, expiry, compensating controls, and a review trigger.',
'lean:capability_thresholds.crossed.missing_safeguard_record.blocks_release':'A crossed threshold without the complete safeguard-verification envelope remains blocked, while later envelope change requires descendant invalidation and a successor assessment version.'}
PREFIX='lean/AsiStackProofs/CapabilityThresholds.lean::'
REFS={'countermodel_refs':['lean/AsiStackProofs/CapabilityThresholdRefinement.lean#countermodels'],'mutation_refs':['scripts/validate_capability_threshold_refinement.py#mutations'],'consumer_refs':['docs:capability_threshold_refinement','evidence_quality:model_adequacy_dossiers/capability-threshold-refinement.md'],'runtime_consumer_refs':['scripts/validate_capability_threshold_refinement.py','schemas/capability_threshold_refinement.schema.json','experiments/capability_threshold_refinement/results/2026-07-15-local.json','scripts/validate_capability_threshold_commitment.py'],'replacement_refs':['proof-model:capability-threshold-refinement.v1','lean/AsiStackProofs/CapabilityThresholdRefinement.lean']}
def attach(row):
 for k,v in REFS.items():row[k]=list(dict.fromkeys([*row.get(k,[]),*v]))
def main():
 s=json.loads(STRUCTURE.read_text());c=next(c for p in s['parts'] for c in p['chapters'] if c['id']==CHAPTER)
 for t in c['proof_targets']:
  if t['tag'] in TARGETS:t['module']=MODULE;t['target']=TARGETS[t['tag']]
 c['lean_module']='AsiStackProofs.CapabilityThresholds; AsiStackProofs.CapabilityThresholdRefinement'
 c['codex_tests']=[x for x in c['codex_tests'] if not(isinstance(x,dict) and x.get('name')=='Capability-threshold repeated-assessment refinement')]
 c['codex_tests'].append({'name':'Capability-threshold repeated-assessment refinement','implementation_status':'implemented','result_status':'passes the exact eight-case suite, 43 routes, six reachable stages, and 48/48 rejecting mutations; one readiness handoff returns to scoped assessment only through version-2 reassessment; support/effect none; no capability, threshold-validity, evaluator-independence, safeguard-efficacy, exception, readiness, deployed-invalidation, transfer, or support claim'})
 STRUCTURE.write_text(json.dumps(s,indent=2)+'\n')
 t=json.loads(TRIAGE.read_text())
 for row in t['records']:
  if row['tag'] in TARGETS:row['module']=MODULE;row['formal_target']=TARGETS[row['tag']];row['rationale']='Reachable repeated-assessment lifecycle with exact custody, safeguard/exception boundaries, successor-version reassessment, 43 routes, 48 rejecting mutations, and no support/effect authority.'
 TRIAGE.write_text(json.dumps(t,indent=2)+'\n')
 r=json.loads(REVIEWS.read_text())
 for target in TARGETS:
  row=r['target_reviews'][target];attach(row);row['semantic_role']='Reachable draft-to-readiness threshold lifecycle with explicit safeguard, exception, authority, invalidation, and successor-version reassessment boundaries.';row['assumptions']=['Capability/system/policy/release-path, envelope, threshold, baseline, evaluator, safeguard, authority, residual, crossing, invalidation, and assessment-version records are trusted inside the finite authored model.'];row['excluded_effects']=['Capability measurement, threshold validity or crossing, evaluator competence or independence, safeguard/bypass/rollback efficacy, exception validity, readiness, safety, release execution, deployed invalidation, transfer, and chapter-core support are excluded.'];row['review_rationale']='Strengthen isolated route reductions with a reachable repeated-assessment lifecycle, independent replay, forty-three routes, and 48 rejecting mutations.'
 ids=[k for k in r['theorem_reviews'] if k.startswith(PREFIX)]
 for k in ids:attach(r['theorem_reviews'][k])
 REVIEWS.write_text(json.dumps(r,indent=2)+'\n');print(f'Integrated Capability Threshold refinement across {len(TARGETS)} targets and {len(ids)} frozen declarations.')
if __name__=='__main__':main()
