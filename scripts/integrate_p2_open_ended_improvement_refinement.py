#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];STRUCTURE=ROOT/'book_structure.json';TRIAGE=ROOT/'proofs/proof_triage.json';REVIEWS=ROOT/'proofs/proof_rationalization_reviews.json'
CHAPTER='open-ended-improvement-engines';MODULE='AsiStackProofs.OpenEndedImprovementRefinement'
TARGETS={
'lean:open_ended_improvement.campaign.complete_candidate_to_governor_review':'A complete bounded campaign trace reaches only a governor-review handoff and grants neither admission, support, nor live authority.',
'lean:open_ended_improvement.campaign.missing_independent_qualification':'Missing independent qualification blocks evaluation in the reachable campaign lifecycle.',
'lean:open_ended_improvement.campaign.exhausted_budget':'Missing cumulative budget custody or attempted reset across descendants blocks archive progression.',
'lean:open_ended_improvement.campaign.missing_stop_authority':'Missing stop ownership, observation, or effect receipt blocks campaign adjudication.',
'lean:open_ended_improvement.campaign.erased_failure_history':'Incomplete attempt, failure, null, unsafe, timeout, or archive history blocks archive progression.',
'lean:open_ended_improvement.campaign.missing_residual_owner':'Missing residual ownership blocks campaign adjudication before governor review.',
'lean:open_ended_improvement.campaign.authority_laundering':'Score, candidate, release, support, or self-ratified controller authority cannot be laundered through the campaign lifecycle.'}
PREFIX='lean/AsiStackProofs/OpenEndedImprovement.lean::'
REFS={'countermodel_refs':['lean/AsiStackProofs/OpenEndedImprovementRefinement.lean#open_ended_improvement_lifecycle_routes'],'mutation_refs':['scripts/validate_open_ended_improvement_refinement.py#mutations'],'consumer_refs':['docs:open_ended_improvement_refinement','evidence_quality:model_adequacy_dossiers/open-ended-improvement-refinement.md'],'runtime_consumer_refs':['scripts/validate_open_ended_improvement_refinement.py','schemas/open_ended_improvement_refinement.schema.json','experiments/open_ended_improvement_refinement/results/2026-07-16-local.json','scripts/validate_open_ended_improvement_campaign.py','scripts/validate_post_v2_update_causality.py','scripts/validate_post_v2_1_outcomes.py'],'replacement_refs':['proof-model:open-ended-improvement-refinement.v1','lean/AsiStackProofs/OpenEndedImprovementRefinement.lean']}
def attach(row):
 for k,v in REFS.items():row[k]=list(dict.fromkeys([*row.get(k,[]),*v]))
def main():
 s=json.loads(STRUCTURE.read_text());c=next(c for p in s['parts'] for c in p['chapters'] if c['id']==CHAPTER)
 for t in c['proof_targets']:
  if t['tag'] in TARGETS:t['module']=MODULE;t['target']=TARGETS[t['tag']]
 c['lean_module']='AsiStackProofs.OpenEndedImprovement; AsiStackProofs.OpenEndedImprovementRefinement'
 c['minimal_implementation']='The exact current minimum preserves seven legacy campaign-admission route theorems, the seven-case/ten-control admission fixture, the three-seed/four-arm fixed update result, and the three-seed/five-arm post-v2.1 stopped result inside a seven-stage, 81-route campaign-to-governor lifecycle with 91/91 rejecting mutations, one governor-review handoff, and one protocol-version-2 readmission witness. The stopped campaigns retain four no-change claim dispositions, zero of nine eligible post-v2.1 challenger seed-arms meeting the 0.05 gain threshold, and no support effect. No adaptive task/candidate generator, evolving archive, objective-legitimacy result, evaluator-independence result, semantic novelty, useful improvement, deployed stop/quarantine, transfer, chapter-core transition, or SOTA result exists.'
 c['open_evidence_gaps']=['No preregistered natural adaptive campaign has compared no-search, fixed-task, conventional-search, human-authored, generated-task, and strongest source-system arms under matched task, model, tool, data, compute, latency, and human budgets.','No real adaptive generator/evaluator/archive system has measured semantic novelty, useful transfer, evaluator exposure and independence, complete denominators, hazard custody, cumulative budgets, opportunity cost, stop/quarantine effects, recursive depth, or cross-campaign contamination.','The seven-stage lifecycle, 81-route consumer, and 91 rejecting mutations establish only finite authored campaign custody; all objectives, legitimacy records, denominators, evaluator records, costs, hazards, stop effects, residuals, and invalidations remain trusted inputs.','No independent implementation or transfer site has reproduced an adaptive campaign, qualified a candidate, observed a live stop or quarantine, or established that generated-task search improves the joint usefulness/cost/safety frontier.']
 c['codex_tests']=[x for x in c['codex_tests'] if not(isinstance(x,dict) and x.get('name')=='Open-ended improvement campaign-to-governor lifecycle refinement')]
 c['codex_tests'].append({'name':'Open-ended improvement campaign-to-governor lifecycle refinement','implementation_status':'implemented','result_status':'passes three inherited result suites, 81 routes, seven reachable stages, and 91/91 rejecting mutations; one governor-review handoff returns to scoped generation only through version-2 readmission; support/effect none; no adaptive search, novelty, usefulness, evaluator-independence, safety, release, transfer, or support claim'})
 STRUCTURE.write_text(json.dumps(s,indent=2)+'\n')
 t=json.loads(TRIAGE.read_text())
 for row in t['records']:
  if row['tag'] in TARGETS:row['module']=MODULE;row['formal_target']=TARGETS[row['tag']];row['rationale']='Reachable bounded-campaign lifecycle with prospective scope, generator and denominator binding, append-only archive custody, independent qualification, observed stopping, governor-only handoff, successor-version readmission, 81 routes, 91 rejecting mutations, and no support/effect authority.'
 TRIAGE.write_text(json.dumps(t,indent=2)+'\n')
 r=json.loads(REVIEWS.read_text())
 for target in TARGETS:
  row=r['target_reviews'][target];attach(row);row['semantic_role']='Reachable scope-to-generation-to-archive-to-evaluation-to-adjudication-to-governor-handoff lifecycle with exact identity, denominator, budget, stop-effect, authority, and successor-version boundaries.';row['assumptions']=['All campaign/objective/representation/controller/policy/generator/evaluator/qualifier/archive/budget/stop/hazard/consumer/authority identities, legitimacy records, denominators, lineage, exposures, costs, hazards, dispositions, effect receipts, residuals, monitors, invalidations, and versions are trusted inside the finite authored model.'];row['excluded_effects']=['Objective legitimacy, evaluator correctness or independence, adaptive-search quality, semantic novelty, useful improvement, hazard-control efficacy, autonomous discovery, transfer, safe self-improvement, capability, safety, readiness, release, deployment, SOTA, AGI, ASI, and chapter-core support are excluded.'];row['review_rationale']='Join seven disconnected admission routes and three bounded result suites into a reachable versioned campaign-to-governor lifecycle, independent replay, eighty-one routes, and 91 rejecting mutations.'
 ids=[k for k in r['theorem_reviews'] if k.startswith(PREFIX)]
 for k in ids:attach(r['theorem_reviews'][k])
 REVIEWS.write_text(json.dumps(r,indent=2)+'\n');print(f'Integrated Open-Ended Improvement refinement across {len(TARGETS)} targets and {len(ids)} frozen declarations.')
if __name__=='__main__':main()
