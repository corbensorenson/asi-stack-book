#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];STRUCTURE=ROOT/'book_structure.json';TRIAGE=ROOT/'proofs/proof_triage.json';REVIEWS=ROOT/'proofs/proof_rationalization_reviews.json'
CHAPTER='policy-optimization-and-learning-from-feedback';MODULE='AsiStackProofs.PolicyOptimizationRefinement'
TARGETS={
'lean:policy_optimization.update.operational_invariant':'A versioned governed-update lifecycle binds target, baseline, objective, data, feedback, full optimizer/checkpoint/RNG and descendant state, evaluation, adjudication, bounded consumption, rollback, and readmission without assigning support or an external effect.',
'lean:policy_optimization.reward_boundary.failure_blocks_promotion':'Missing target evaluation, causal ablation, reward-hacking probes, regression, forgetting, safety/rights, uncertainty, or independent evaluation blocks a policy update before bounded-lease adjudication.',
'lean:policy_optimization.promotion_route.failure_routes':'All finite update-lifecycle routes reject or redirect incomplete scope, state, update, evaluation, adjudication, lease, rollback, or readmission records before bounded use.',
'lean:policy_optimization.lease_probe_fixture_bridge':'The independently consumed six-sample/five-candidate lease probe and the reachable lifecycle preserve three rejected controls, experimental-only use, versioned readmission, and no support or external-effect authority.'}
PREFIX='lean/AsiStackProofs/PolicyOptimization.lean::'
REFS={'countermodel_refs':['lean/AsiStackProofs/PolicyOptimizationRefinement.lean#policy_update_lifecycle_routes'],'mutation_refs':['scripts/validate_policy_optimization_refinement.py#mutations'],'consumer_refs':['docs:policy_optimization_refinement','evidence_quality:model_adequacy_dossiers/policy-optimization-refinement.md'],'runtime_consumer_refs':['scripts/validate_policy_optimization_refinement.py','schemas/policy_optimization_refinement.schema.json','experiments/policy_optimization_refinement/results/2026-07-16-local.json','scripts/validate_policy_update_lease_probe.py'],'replacement_refs':['proof-model:policy-optimization-refinement.v1','lean/AsiStackProofs/PolicyOptimizationRefinement.lean']}
def attach(row):
 for k,v in REFS.items():row[k]=list(dict.fromkeys([*row.get(k,[]),*v]))
def main():
 s=json.loads(STRUCTURE.read_text());c=next(c for p in s['parts'] for c in p['chapters'] if c['id']==CHAPTER)
 for t in c['proof_targets']:
  if t['tag'] in TARGETS:t['module']=MODULE;t['target']=TARGETS[t['tag']]
 c['lean_module']='AsiStackProofs.PolicyOptimization; AsiStackProofs.PolicyOptimizationRefinement'
 c['minimal_implementation']='The exact current minimum preserves eleven inherited contradiction/guard theorems and the deterministic six-sample, two-holdout, five-candidate lease probe inside a seven-stage, 63-route governed-update lifecycle with 73/73 rejecting mutations, one bounded lease, and one protocol-version-2 readmission witness. It runs no optimizer, model, trainer, preference dataset, reward model, natural workload, real policy update, deployed canary, live rollback, independent reproduction, transfer, chapter-core transition, or SOTA comparison.'
 c['open_evidence_gaps']=['No ASI Stack model, optimizer, trainer, natural planner/router/context/execution workload, preference or reward dataset, reward model, policy update, real checkpoint, deployed canary, live rollback, independent reproduction, or heterogeneous transfer has run.','No local result establishes reward or preference validity, evaluator validity, causal target improvement, retained capability, forgetting control, effect-complete runtime rollback, monitor efficacy, useful throughput, safety, alignment, readiness, release, or SOTA.','The seven-stage lifecycle, 63-route consumer, and 73 rejecting mutations establish only finite authored record consequences; all digests, inventories, evaluations, causal checks, rollback assertions, monitors, invalidations, and authority fields remain trusted.','Run the prospectively frozen natural multi-layer campaign with matched no-update and strong method baselines, real training-state capture, independent evaluation, reward attacks, causal ablations, forgetting tests, effect-complete rollback, post-update monitoring, joint utility/safety/rights/resource accounting, reproduction, and transfer before considering empirical support movement.']
 c['codex_tests']=[x for x in c['codex_tests'] if not(isinstance(x,dict) and x.get('name')=='Policy-optimization update-lifecycle refinement')]
 c['codex_tests'].append({'name':'Policy-optimization update-lifecycle refinement','implementation_status':'implemented','result_status':'passes the inherited six-sample/five-candidate lease, 63 routes, seven reachable stages, and 73/73 rejecting mutations; one bounded lease returns to scoped full-state binding only through version-2 readmission; support/effect none; no learning, reward-validity, causal, forgetting, rollback-efficacy, safety, release, transfer, or support claim'})
 STRUCTURE.write_text(json.dumps(s,indent=2)+'\n')
 t=json.loads(TRIAGE.read_text())
 for row in t['records']:
  if row['tag'] in TARGETS:row['module']=MODULE;row['formal_target']=TARGETS[row['tag']];row['rationale']='Reachable governed policy-update lifecycle with prospective scope, full optimizer/checkpoint/RNG and descendant custody, update receipt, independent evaluation, adjudication, bounded lease, effect-complete rollback, successor-version readmission, 63 routes, 73 rejecting mutations, and no support/effect authority.'
 TRIAGE.write_text(json.dumps(t,indent=2)+'\n')
 r=json.loads(REVIEWS.read_text())
 for target in TARGETS:
  row=r['target_reviews'][target];attach(row);row['semantic_role']='Reachable scope-to-full-state-to-update-to-evaluation-to-adjudication-to-bounded-lease lifecycle with exact identity, causal, rollback, invalidation, authority, and successor-version boundaries.';row['assumptions']=['All target, baseline, objective, data, feedback, checkpoint, optimizer, scheduler, RNG, cache, backup, descendant, evaluator, causal, rollback, monitor, invalidation, consumer, authority, and version records are trusted inside the finite authored model.'];row['excluded_effects']=['Learning, reward/evaluator validity, causal improvement, retained capability, forgetting control, rollback/monitor efficacy, useful throughput, safety, alignment, readiness, release, reproduction, transfer, SOTA, and chapter-core support are excluded.'];row['review_rationale']='Replace projection headlines and disconnected promotion routes with a reachable versioned update lifecycle, independent replay, sixty-three routes, and 73 rejecting mutations.'
 ids=[k for k in r['theorem_reviews'] if k.startswith(PREFIX)]
 for k in ids:attach(r['theorem_reviews'][k])
 REVIEWS.write_text(json.dumps(r,indent=2)+'\n');print(f'Integrated Policy Optimization refinement across {len(TARGETS)} targets and {len(ids)} frozen declarations.')
if __name__=='__main__':main()
