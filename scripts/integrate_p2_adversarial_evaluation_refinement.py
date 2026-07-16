#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];STRUCTURE=ROOT/'book_structure.json';TRIAGE=ROOT/'proofs/proof_triage.json';REVIEWS=ROOT/'proofs/proof_rationalization_reviews.json'
CHAPTER='adversarial-evaluation-sandbagging-and-training-time-deception';MODULE='AsiStackProofs.AdversarialEvaluationRefinement'
TARGETS={
'lean:adversarial_evaluation.integrity.complete_to_promotion_review':'A reachable, prospectively bound observation lifecycle can emit only a bounded decision-review handoff after complete observation, independent-probe, alternative-hypothesis, discrepancy, uncertainty, residual, expiry, and authority-separation custody.',
'lean:adversarial_evaluation.integrity.missing_selection_context':'Missing selection context blocks observation admission without mutating lifecycle state.',
'lean:adversarial_evaluation.integrity.missing_reward_provenance':'Missing reward provenance blocks observation admission without converting absence into behavioral evidence.',
'lean:adversarial_evaluation.integrity.missing_monitor_provenance':'Missing monitor provenance blocks observation admission without treating an unobserved trace as negative evidence.',
'lean:adversarial_evaluation.integrity.missing_independent_evaluation':'Missing independent evaluation or evaluator separation blocks adjudication.',
'lean:adversarial_evaluation.integrity.missing_cross_context_probe':'Missing cross-context or matched-access comparison blocks adjudication.',
'lean:adversarial_evaluation.integrity.unresolved_discrepancy':'An unresolved discrepancy requires explicit quarantine custody and cannot take the favorable promotion-review route.',
'lean:adversarial_evaluation.integrity.intent_laundering':'An observation lifecycle rejects intent inference and cannot assign support or an external decision effect.'}
PREFIX='lean/AsiStackProofs/AdversarialEvaluation.lean::'
REFS={'countermodel_refs':['lean/AsiStackProofs/AdversarialEvaluationRefinement.lean#countermodels'],'mutation_refs':['scripts/validate_adversarial_evaluation_refinement.py#mutations'],'consumer_refs':['docs:adversarial_evaluation_refinement','evidence_quality:model_adequacy_dossiers/adversarial-evaluation-refinement.md'],'runtime_consumer_refs':['scripts/validate_adversarial_evaluation_refinement.py','schemas/adversarial_evaluation_refinement.schema.json','experiments/adversarial_evaluation_refinement/results/2026-07-15-local.json','scripts/validate_adversarial_evaluation_integrity.py'],'replacement_refs':['proof-model:adversarial-evaluation-refinement.v1','lean/AsiStackProofs/AdversarialEvaluationRefinement.lean']}
def attach(row):
 for k,v in REFS.items():row[k]=list(dict.fromkeys([*row.get(k,[]),*v]))
def main():
 s=json.loads(STRUCTURE.read_text());c=next(c for p in s['parts'] for c in p['chapters'] if c['id']==CHAPTER)
 for t in c['proof_targets']:
  if t['tag'] in TARGETS:t['module']=MODULE;t['target']=TARGETS[t['tag']]
 c['lean_module']='AsiStackProofs.AdversarialEvaluation; AsiStackProofs.AdversarialEvaluationRefinement'
 c['minimal_implementation']='The exact current minimum preserves the eight digest-bound integrity cases in a seven-stage, 56-route evaluation-observation lifecycle with 60/60 rejecting mutations, twelve AdversarialEvaluationRefinement declarations, one bounded decision-review handoff, and one protocol-version-2 re-evaluation witness. It runs no model, natural or deceptive cross-context workload, monitor or reward process, evaluator ensemble, detector, mitigation, attack, quarantine service, threshold decision, release, deployment, reproduction, transfer, chapter-core transition, or SOTA comparison.'
 c['open_evidence_gaps']=['No ASI Stack model, natural or deceptive cross-context workload, monitor, reward process, evaluator ensemble, detector, mitigation, attack, decision, release, incident, reproduction, or transfer has run.','No local result establishes deception, sandbagging, alignment faking, reward hacking, capability, intent, prevalence, monitor/reward fidelity, outcome validity, evaluator independence, mitigation efficacy, quarantine correctness, readiness, safety, or deployment authority.','The seven-stage lifecycle, 56-route consumer, and 60 rejecting mutations establish only structured observation-record consequences; all input identities, provenance, observations, outcomes, discrepancies, hypotheses, invalidation assertions, and authority fields remain trusted.','Run the prospectively frozen natural/adversarial cross-context, causal-ablation, mitigation, independent-institution, and heterogeneous-transfer campaign before considering empirical support movement.']
 c['codex_tests']=[x for x in c['codex_tests'] if not(isinstance(x,dict) and x.get('name')=='Adversarial-evaluation observation-lifecycle refinement')]
 c['codex_tests'].append({'name':'Adversarial-evaluation observation-lifecycle refinement','implementation_status':'implemented','result_status':'passes the exact eight-case suite, 56 routes, seven reachable stages, and 60/60 rejecting mutations; one decision-review handoff returns to scoped protocol binding only through version-2 re-evaluation; support/effect none; no deception, capability, intent, prevalence, evaluator-validity, mitigation-efficacy, quarantine-correctness, release, transfer, or support claim'})
 STRUCTURE.write_text(json.dumps(s,indent=2)+'\n')
 t=json.loads(TRIAGE.read_text())
 for row in t['records']:
  if row['tag'] in TARGETS:row['module']=MODULE;row['formal_target']=TARGETS[row['tag']];row['rationale']='Reachable observation lifecycle with prospective scope/protocol custody, independent-probe, adjudication, decision-handoff, and successor-version re-evaluation boundaries, 56 routes, 60 rejecting mutations, and no support/effect authority.'
 TRIAGE.write_text(json.dumps(t,indent=2)+'\n')
 r=json.loads(REVIEWS.read_text())
 for target in TARGETS:
  row=r['target_reviews'][target];attach(row);row['semantic_role']='Reachable scope-to-protocol-to-observation-to-independent-probe-to-adjudication-to-decision lifecycle with explicit hypothesis, discrepancy, mitigation, quarantine, authority, invalidation, and successor-version boundaries.';row['assumptions']=['Consumer/decision/model/task/protocol/policy/evaluator/monitor/reward/selection/hypothesis/outcome, observation, discrepancy, mitigation, quarantine, authority, invalidation, and protocol-version records are trusted inside the finite authored model.'];row['excluded_effects']=['Deception or sandbagging detection, capability or intent inference, prevalence, monitor/reward/outcome/evaluator validity, mitigation efficacy, quarantine correctness, readiness, safety, release execution, deployed invalidation, transfer, and chapter-core support are excluded.'];row['review_rationale']='Strengthen isolated route reductions with a reachable versioned observation lifecycle, independent replay, fifty-six routes, and 60 rejecting mutations.'
 ids=[k for k in r['theorem_reviews'] if k.startswith(PREFIX)]
 for k in ids:attach(r['theorem_reviews'][k])
 REVIEWS.write_text(json.dumps(r,indent=2)+'\n');print(f'Integrated Adversarial Evaluation refinement across {len(TARGETS)} targets and {len(ids)} frozen declarations.')
if __name__=='__main__':main()
