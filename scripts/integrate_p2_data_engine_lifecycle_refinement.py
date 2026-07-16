#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];STRUCTURE=ROOT/'book_structure.json';TRIAGE=ROOT/'proofs/proof_triage.json';REVIEWS=ROOT/'proofs/proof_rationalization_reviews.json'
CHAPTER='data-engines-continual-learning-and-unlearning';MODULE='AsiStackProofs.DataEngineLifecycleRefinement'
TARGETS={
'lean:data_engines.provenance_authority.failure_blocks_admission':'Missing bound provenance, rights, or authority blocks the reachable custody lifecycle before data admission.',
'lean:data_engines.contamination.failure_routes':'Missing split exclusions or a contamination-check record blocks the reachable custody lifecycle before admission.',
'lean:data_engines.complete_receipt.eligibility_invariant':'A complete admission record advances only to full-state binding and does not establish data quality, training, deletion, or support.',
'lean:data_engines.full_state.complete_reaches_evidence_review':'Complete declared full-state custody and a prospectively fixed selection rule advance only to an update receipt, not promotion.',
'lean:data_engines.full_state.missing_optimizer_requires_repair':'Missing optimizer state blocks full-state binding.',
'lean:data_engines.full_state.missing_scheduler_requires_repair':'Missing scheduler state blocks full-state binding.',
'lean:data_engines.full_state.missing_rng_requires_repair':'Missing RNG state blocks full-state binding.',
'lean:data_engines.full_state.missing_cache_requires_repair':'Missing cache state blocks full-state binding.',
'lean:data_engines.full_state.missing_backup_requires_repair':'Missing backup state blocks full-state binding.',
'lean:data_engines.full_state.missing_descendant_requires_repair':'Missing descendant state blocks full-state binding.',
'lean:data_engines.full_state.missing_checkpoint_authority_requires_repair':'Missing prospective checkpoint authority or selection rule blocks full-state binding.',
'lean:data_engines.full_state.rollback_mismatch_requires_repair':'A declared-surface rollback mismatch blocks the update record and cannot be generalized to semantic or production recovery.',
'lean:data_engines.unlearning.behavior_cannot_launder_influence':'Behavioral cohort change cannot serve as evidence of causal influence reduction in deletion-claim adjudication.',
'lean:data_engines.unlearning.behavior_cannot_launder_privacy':'Behavioral cohort change cannot serve as evidence of privacy protection or erasure in deletion-claim adjudication.',
'lean:data_engines.unlearning.lineage_cannot_launder_storage':'Lineage propagation or invalidation cannot serve as evidence of physical storage or backup erasure in deletion-claim adjudication.'}
PREFIX='lean/AsiStackProofs/DataEngines.lean::'
REFS={'countermodel_refs':['lean/AsiStackProofs/DataEngineLifecycleRefinement.lean#data_engine_lifecycle_routes'],'mutation_refs':['scripts/validate_data_engine_lifecycle_refinement.py#mutations'],'consumer_refs':['docs:data_engine_lifecycle_refinement','evidence_quality:model_adequacy_dossiers/data-engine-lifecycle-refinement.md'],'runtime_consumer_refs':['scripts/validate_data_engine_lifecycle_refinement.py','schemas/data_engine_lifecycle_refinement.schema.json','experiments/data_engine_lifecycle_refinement/results/2026-07-16-local.json','scripts/validate_data_admission_receipt_probe.py','scripts/validate_data_engine_full_state_bridge.py','scripts/validate_post_v2_update_causality.py'],'replacement_refs':['proof-model:data-engine-lifecycle-refinement.v1','lean/AsiStackProofs/DataEngineLifecycleRefinement.lean']}
def attach(row):
 for k,v in REFS.items():row[k]=list(dict.fromkeys([*row.get(k,[]),*v]))
def main():
 s=json.loads(STRUCTURE.read_text());c=next(c for p in s['parts'] for c in p['chapters'] if c['id']==CHAPTER)
 for t in c['proof_targets']:
  if t['tag'] in TARGETS:t['module']=MODULE;t['target']=TARGETS[t['tag']]
 c['lean_module']='AsiStackProofs.DataEngines; AsiStackProofs.DataEngineLifecycleRefinement'
 c['minimal_implementation']='The exact current minimum preserves all fifteen legacy data-admission, full-state, and unlearning-claim route theorems; the four-scenario admission probe; the 24-surface/15-transaction full-state bridge; and the three-seed/twelve-arm small-model update result inside an eight-stage, 82-route custody/update/deletion lifecycle with two checked lifecycle-composition theorems, 96/96 route mutations, 3/3 cross-stage mutations, one bounded custody handoff, and one protocol-version-2 readmission witness. Influence remains unestablished, storage erasure remains zero, all four affected claims remain no-change, and no source/rights truth, semantic contamination, foundation-model learning, privacy/legal/backup/external-descendant erasure, production rollback, transfer, chapter-core transition, or SOTA result exists.'
 c['open_evidence_gaps']=['No natural heterogeneous data and deletion campaign has frozen complete partitions and denominators, compared strong matched replacement, accumulation, replay, reweighting, synthetic, quarantine, retraining, sharding, fine-tuning, and no-change policies, or prevented outcome-aware protocol change.','No real campaign jointly establishes coverage, semantic leakage, contamination, poisoning, privacy, rights, full-state restoration, effect-complete rollback, sequential deletion, replica and backup erasure, regrowth control, external-descendant closure, and complete cost accounting.','The eight-stage lifecycle, 82-route consumer, and 96 rejecting mutations establish only finite authored custody consequences; all digests, rights, inventories, checks, rollback receipts, deletion statuses, monitors, and invalidations remain trusted.','No independent trainer, custodian, privacy evaluator, storage verifier, institution, or transfer site has reproduced the bounded local results or adjudicated the separate behavioral, influence, privacy, lineage, legal, storage, backup, and external-descendant claim axes.']
 c['codex_tests']=[x for x in c['codex_tests'] if not(isinstance(x,dict) and x.get('name')=='Data-engine custody/update/deletion lifecycle refinement')]
 c['codex_tests'].append({'name':'Data-engine custody/update/deletion lifecycle refinement','implementation_status':'implemented','result_status':'passes three inherited result suites, two composed Lean traces, 82 routes, 96/96 route mutations, and 3/3 cross-stage mutations; one bounded custody handoff returns to scoped admission only through version-2 readmission; support/effect none; no source-truth, learning, influence, forgetting, privacy/legal/storage erasure, production rollback, release, transfer, or support claim'})
 STRUCTURE.write_text(json.dumps(s,indent=2)+'\n')
 t=json.loads(TRIAGE.read_text())
 for row in t['records']:
  if row['tag'] in TARGETS:row['module']=MODULE;row['formal_target']=TARGETS[row['tag']];row['rationale']='Reachable Data-and-Descendant Custody lifecycle with prospective scope, admission, full-state binding, update receipt, deletion assessment, separated claim axes, bounded custody, successor-version readmission, 82 routes, 96 rejecting mutations, and no support/effect authority.'
 TRIAGE.write_text(json.dumps(t,indent=2)+'\n')
 r=json.loads(REVIEWS.read_text())
 for target in TARGETS:
  row=r['target_reviews'][target];attach(row);row['semantic_role']='Reachable scope-to-admission-to-full-state-to-update-to-deletion-assessment-to-claim-adjudication-to-bounded-custody lifecycle with exact identity, rollback, claim-axis, invalidation, authority, and successor-version boundaries.';row['assumptions']=['All datum/cohort/provenance/rights/authority/split/dataset/model/checkpoint/optimizer/scheduler/RNG/cache/backup/lineage/descendant/deletion/evaluator/consumer identities, checks, statuses, rollback receipts, monitors, invalidations, and version records are trusted inside the finite authored model.'];row['excluded_effects']=['Source/rights truth, semantic contamination control, data quality, language-model learning, influence removal, forgetting, privacy/legal/storage/backup erasure, semantic/production recovery, capability, safety, readiness, release, reproduction, transfer, SOTA, and chapter-core support are excluded.'];row['review_rationale']='Join fifteen disconnected finite routes and three bounded result suites into a reachable versioned custody lifecycle, independent replay, eighty-two routes, and 96 rejecting mutations.'
 ids=[k for k in r['theorem_reviews'] if k.startswith(PREFIX)]
 for k in ids:attach(r['theorem_reviews'][k])
 REVIEWS.write_text(json.dumps(r,indent=2)+'\n');print(f'Integrated Data Engine refinement across {len(TARGETS)} targets and {len(ids)} frozen declarations.')
if __name__=='__main__':main()
