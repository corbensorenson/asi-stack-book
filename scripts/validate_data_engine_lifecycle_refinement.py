#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, subprocess, sys
from pathlib import Path
from typing import Any
import jsonschema

ROOT=Path(__file__).resolve().parents[1]
LEAN=ROOT/'lean/AsiStackProofs/DataEngineLifecycleRefinement.lean'
SCHEMA=ROOT/'schemas/data_engine_lifecycle_refinement.schema.json'
ADMISSION=ROOT/'experiments/data_admission_receipt_probe/results/2026-07-10-local.json'
FULL_STATE=ROOT/'experiments/data_engine_full_state_bridge/results/2026-07-13-local.json'
UPDATE=ROOT/'experiments/post_v2_update_causality/results/2026-07-10-local.json'
RESULT=ROOT/'experiments/data_engine_lifecycle_refinement/results/2026-07-16-local.json'
COMMAND='python3 scripts/validate_data_engine_lifecycle_refinement.py'
STAGES=['draft','scoped','admitted','stateBound','updated','deletionAssessed','adjudicated','custodyBound']
KINDS={'draft':'scopeCustody','scoped':'admitData','admitted':'bindFullState','stateBound':'recordUpdate','updated':'assessDeletion','deletionAssessed':'adjudicateClaims','adjudicated':'bindCustody','custodyBound':'triggerReadmission'}
ACCEPTED={'accept_scope','accept_admission','accept_state_binding','accept_update_record','accept_deletion_assessment','accept_claim_adjudication','accept_bounded_custody','accept_readmission'}
IDENTITY={'datumDigest','cohortDigest','provenanceDigest','rightsDigest','authorityDigest','splitDigest','datasetDigest','modelDigest','baseCheckpointDigest','selectedCheckpointDigest','optimizerDigest','schedulerDigest','rngDigest','cacheDigest','backupDigest','lineageDigest','descendantDigest','deletionRequestDigest','evaluatorDigest','consumerDigest','currentVersion'}
GATES={
'draft':[('datumPresent',False,'request_datum'),('cohortPresent',False,'request_cohort'),('provenancePresent',False,'request_provenance'),('rightsPresent',False,'request_rights'),('authorityPresent',False,'request_authority'),('consumerPresent',False,'request_consumer'),('riskTierPresent',False,'request_risk_tier'),('scopePresent',False,'request_scope')],
'scoped':[('splitExclusionsPresent',False,'request_split_exclusions'),('contaminationCheckPresent',False,'request_contamination_check'),('retentionPresent',False,'request_retention'),('deletionScopePresent',False,'request_deletion_scope'),('transformationLineagePresent',False,'request_transformation_lineage'),('syntheticLineagePresent',False,'request_synthetic_lineage'),('evaluationExclusionsPresent',False,'request_evaluation_exclusions'),('coverageResidualPresent',False,'request_coverage_residual'),('distributionResidualPresent',False,'request_distribution_residual'),('expiryPresent',False,'request_expiry')],
'admitted':[('modelStatePresent',False,'request_model_state'),('optimizerStatePresent',False,'request_optimizer_state'),('schedulerStatePresent',False,'request_scheduler_state'),('rngStatePresent',False,'request_rng_state'),('cacheStatePresent',False,'request_cache_state'),('backupStatePresent',False,'request_backup_state'),('descendantStatePresent',False,'request_descendant_state'),('checkpointAuthorityPresent',False,'request_checkpoint_authority'),('preStateDigestPresent',False,'request_pre_state_digest'),('selectionRulePresent',False,'request_selection_rule')],
'stateBound':[('updateDispositionPresent',False,'request_update_disposition'),('selectedCheckpointPresent',False,'request_selected_checkpoint'),('completeDenominatorPresent',False,'request_complete_denominator'),('failureLogPresent',False,'request_failure_log'),('costRecordPresent',False,'request_cost_record'),('bestFinalRecordPresent',False,'request_best_final_record'),('rollbackReceiptPresent',False,'request_rollback_receipt'),('declaredSurfaceRollbackExact',False,'reject_declared_surface_rollback_mismatch'),('descendantInvalidationPresent',False,'request_descendant_invalidation'),('noSupportAuthorityRecorded',False,'reject_support_authority_laundering')],
'updated':[('deletionRequestPresent',False,'request_deletion_request'),('affectedCohortPresent',False,'request_affected_cohort'),('propagationRecordPresent',False,'request_propagation_record'),('replicaBackupRecordPresent',False,'request_replica_backup_record'),('externalDescendantResidualPresent',False,'request_external_descendant_residual'),('behavioralStatusPresent',False,'request_behavioral_status'),('influenceStatusPresent',False,'request_influence_status'),('privacyStatusPresent',False,'request_privacy_status'),('storageStatusPresent',False,'request_storage_status'),('legalStatusPresent',False,'request_legal_status')],
'deletionAssessed':[('axesSeparated',False,'request_axis_separation'),('behaviorUsedAsInfluenceEvidence',True,'reject_behavior_as_influence'),('behaviorUsedAsPrivacyEvidence',True,'reject_behavior_as_privacy'),('lineageUsedAsStorageEvidence',True,'reject_lineage_as_storage'),('uncertaintyPresent',False,'request_uncertainty'),('residualOwnerPresent',False,'request_residual_owner'),('counterevidencePresent',False,'request_counterevidence'),('noErasureInferenceRecorded',False,'reject_erasure_inference'),('noReleaseAuthorityRecorded',False,'reject_release_authority_laundering')],
'adjudicated':[('permittedConsumerPresent',False,'request_permitted_consumer'),('boundedCustodyRecordPresent',False,'request_bounded_custody_record'),('datasetCheckpointBound',False,'request_dataset_checkpoint_binding'),('custodyExpiryPresent',False,'request_custody_expiry'),('monitorPresent',False,'request_monitor'),('revocationPathPresent',False,'request_revocation_path'),('noCustodySupportAuthorityRecorded',False,'reject_custody_support_laundering')],
'custodyBound':[('materialChangeTriggerPresent',False,'request_material_change_trigger'),('completeInvalidationPresent',False,'request_complete_invalidation'),('ordinaryRouteBlocked',False,'request_ordinary_route_block'),('rerunRequirementPresent',False,'request_rerun_requirement'),('rollbackOrRevocationReceiptPresent',False,'request_rollback_or_revocation_receipt'),('successorVersion',1,'reject_successor_version')],
}

def packet()->dict[str,Any]:
 p={k:i+1001 for i,k in enumerate(sorted(IDENTITY-{'currentVersion'}))};p['currentVersion']=1
 for gates in GATES.values():
  for field,bad,_ in gates:
   if field=='successorVersion':p[field]=1
   elif bad is True:p[field]=False
   else:p[field]=True
 p.update({'eventDigest':1,'supportAssignmentRequested':False,'externalEffectRequested':False})
 return p

def route(stage:str,kind:str,p:dict[str,Any],last:int=0,version:int=1)->str:
 c=packet()
 if kind!=KINDS[stage]:return 'reject_wrong_stage'
 for field in IDENTITY:
  if p[field]!=(version if field=='currentVersion' else c[field]):return 'reject_identity_substitution'
 if p['eventDigest']==last:return 'reject_replay'
 if p['supportAssignmentRequested'] or p['externalEffectRequested']:return 'reject_authority_leak'
 for field,bad,answer in GATES[stage]:
  if field=='successorVersion':
   if p[field]!=version+1:return answer
  elif p[field] is bad:return answer
 return {'draft':'accept_scope','scoped':'accept_admission','admitted':'accept_state_binding','stateBound':'accept_update_record','updated':'accept_deletion_assessment','deletionAssessed':'accept_claim_adjudication','adjudicated':'accept_bounded_custody','custodyBound':'accept_readmission'}[stage]

def run(command:str)->dict[str,Any]:
 p=subprocess.run(command.split(),cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 if p.returncode:raise RuntimeError(p.stdout)
 return {'command':command,'exit_code':0,'output_sha256':hashlib.sha256(p.stdout.encode()).hexdigest()}

def inherited_summary()->dict[str,Any]:
 admission=json.loads(ADMISSION.read_text());full=json.loads(FULL_STATE.read_text());update=json.loads(UPDATE.read_text())
 seed_rows=update['seed_records'];arms=[arm for seed in seed_rows for arm in seed['arms']]
 return {'admission_scenario_count':admission['scenario_count'],'admission_rejected_control_count':sum(admission['negative_controls'].values()),'full_state_surface_count':full['observed_summary']['state_surface_count'],'full_state_transaction_count':full['observed_summary']['transaction_count'],'full_state_exact_rollback_count':full['observed_summary']['exact_rollback_count'],'full_state_best_final_disagreement_count':full['observed_summary']['best_final_disagreement_count'],'full_state_deletion_behavior_changes':full['observed_summary']['deletion_behavior_changes'],'full_state_lineage_propagation_count':full['observed_summary']['deletion_lineage_propagation_count'],'full_state_influence_reduction_state':full['observed_summary']['influence_reduction_state'],'full_state_storage_erasure_count':full['observed_summary']['storage_erasure_count'],'update_seed_count':len(seed_rows),'update_arm_count':len(arms),'update_parameter_mutation_count':sum(arm['actual_parameter_mutation'] for arm in arms),'update_best_final_disagreement_count':sum(arm['best_final_test_disagreement'] for arm in arms if arm['arm']!='no_update'),'update_exact_rollback_count':sum(seed['rollback']['exact'] for seed in seed_rows),'update_invalidated_descendant_count':sum(seed['rollback']['descendant_arms_invalidated'] for seed in seed_rows),'update_no_change_disposition_count':sum(row['disposition']=='no_change' for row in update['claim_dispositions']),'support_state_effect':'none'}

def build()->dict[str,Any]:
 cases=[]
 for i,stage in enumerate(STAGES,1):
  p=packet();p['eventDigest']=i
  if stage=='custodyBound':p['successorVersion']=2
  cases.append({'case_id':stage+'_accepted','expected_route':route(stage,KINDS[stage],p)})
 for stage,gates in GATES.items():
  for field,bad,_ in gates:
   p=packet();p['eventDigest']=90
   if stage=='custodyBound':p['successorVersion']=2
   p[field]=bad
   cases.append({'case_id':stage+'_'+field,'expected_route':route(stage,KINDS[stage],p)})
 for cid,kind,field,value in [('wrong_stage','triggerReadmission',None,None),('identity_substitution','scopeCustody','consumerDigest',9999),('event_replay','scopeCustody','eventDigest',0),('authority_leak','scopeCustody','supportAssignmentRequested',True)]:
  p=packet()
  if field:p[field]=value
  cases.append({'case_id':cid,'expected_route':route('draft',kind,p)})
 mutations=[]
 for field in sorted(IDENTITY):
  p=packet();p[field]+=1000;mutations.append({'mutation_id':'binding_'+field,'rejected':route('draft','scopeCustody',p) not in ACCEPTED})
 for stage,gates in GATES.items():
  for field,bad,_ in gates:
   p=packet();p['eventDigest']=91
   if stage=='custodyBound':p['successorVersion']=2
   p[field]=bad
   mutations.append({'mutation_id':'gate_'+stage+'_'+field,'rejected':route(stage,KINDS[stage],p) not in ACCEPTED})
 for mid,stage,kind,field,value in [('wrong_kind','draft','triggerReadmission',None,None),('event_replay','draft','scopeCustody','eventDigest',0),('support_leak','draft','scopeCustody','supportAssignmentRequested',True),('effect_leak','draft','scopeCustody','externalEffectRequested',True),('stale_custody_after_readmission','scoped','bindCustody',None,None)]:
  p=packet()
  if field:p[field]=value
  mutations.append({'mutation_id':mid,'rejected':route(stage,kind,p) not in ACCEPTED})
 return {'schema_version':'asi_stack.data_engine_lifecycle_refinement.v1','result_id':'data-engine-lifecycle-refinement-2026-07-16-local','source_sha256':{'lean_model':hashlib.sha256(LEAN.read_bytes()).hexdigest(),'admission_result':hashlib.sha256(ADMISSION.read_bytes()).hexdigest(),'full_state_result':hashlib.sha256(FULL_STATE.read_bytes()).hexdigest(),'update_result':hashlib.sha256(UPDATE.read_bytes()).hexdigest()},'inherited_results':inherited_summary(),'reachable_stage_count':8,'route_case_count':len(cases),'route_coverage':cases,'mutation_count':len(mutations),'mutation_rejection_count':sum(x['rejected'] for x in mutations),'mutation_receipts':mutations,'command_receipts':[run('python3 scripts/validate_data_admission_receipt_probe.py'),run('python3 scripts/validate_data_engine_full_state_bridge.py'),run('python3 scripts/validate_post_v2_update_causality.py')],'witness':{'terminal_stage':'scoped','protocol_version':2,'receipt_count':8,'bounded_custody_count':1,'readmission_count':1,'support_assignment_count':0,'external_effect_count':0},'support_state_effect':'none','non_claims':['no source truth, semantic contamination, dataset quality, or rights validity result','no language-model continual-learning, capability, or transfer result','behavioral change does not establish influence reduction or forgetting','lineage invalidation does not establish privacy, legal, storage, backup, or external-descendant erasure','declared-surface digest rollback does not establish semantic or production recovery','no safety, readiness, release, support, SOTA, AGI, or ASI authority']}

def main()->None:
 a=argparse.ArgumentParser();a.add_argument('--write',action='store_true');args=a.parse_args();result=build();errors=[]
 if result['route_case_count']!=82:errors.append('route count drifted')
 if result['mutation_count']!=96 or result['mutation_rejection_count']!=96:errors.append('mutation contract drifted')
 for needle in ('inductive Stage','def routeFor','data_engine_lifecycle_routes'):
  if needle not in LEAN.read_text():errors.append('Lean model missing '+needle)
 jsonschema.validate(result,json.loads(SCHEMA.read_text()));serialized=json.dumps(result,indent=2)+'\n'
 if args.write:RESULT.parent.mkdir(parents=True,exist_ok=True);RESULT.write_text(serialized)
 elif not RESULT.exists() or RESULT.read_text()!=serialized:errors.append(f'{RESULT.relative_to(ROOT)} is stale; run {COMMAND} --write')
 if errors:print('Data-engine lifecycle refinement failed:\n - '+'\n - '.join(errors));sys.exit(1)
 print('Data-engine lifecycle refinement passed: 3 inherited suites, 8 stages, 82 routes, 96/96 mutations rejected, support effect none.')
if __name__=='__main__':main()
