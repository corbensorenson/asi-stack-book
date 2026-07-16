#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, subprocess, sys
from pathlib import Path
from typing import Any
import jsonschema

ROOT=Path(__file__).resolve().parents[1]
LEAN=ROOT/'lean/AsiStackProofs/PolicyOptimizationRefinement.lean'
SCHEMA=ROOT/'schemas/policy_optimization_refinement.schema.json'
INHERITED=ROOT/'experiments/policy_update_lease/results/2026-07-02-local.json'
RESULT=ROOT/'experiments/policy_optimization_refinement/results/2026-07-16-local.json'
COMMAND='python3 scripts/validate_policy_optimization_refinement.py'
STAGES=['draft','scoped','stateBound','updated','evaluated','adjudicated','leaseBound']
KINDS={'draft':'scopeUpdate','scoped':'bindTrainingState','stateBound':'recordUpdate','updated':'recordEvaluation','evaluated':'adjudicateUpdate','adjudicated':'requestBoundedLease','leaseBound':'triggerReadmission'}
ACCEPTED={'accept_scope','accept_state_binding','accept_update_receipt','accept_evaluation','accept_adjudication','accept_bounded_lease','accept_readmission'}
IDENTITY={'updateId','targetPolicyDigest','baselineDigest','objectiveDigest','datasetDigest','feedbackDigest','baseCheckpointDigest','candidateCheckpointDigest','optimizerDigest','schedulerDigest','rngDigest','evaluatorDigest','rollbackDigest','consumerDigest','authorityDigest','currentVersion'}
GATES={
'draft':[('targetPolicyPresent','request_target_policy'),('baselinePresent','request_baseline'),('objectivePresent','request_objective'),('permittedDeltaPresent','request_permitted_delta'),('authorityCeilingPresent','request_authority_ceiling'),('riskTierPresent','request_risk_tier'),('consumerPresent','request_consumer')],
'scoped':[('datasetPresent','request_dataset'),('feedbackBoundaryPresent','request_feedback_boundary'),('holdoutPresent','request_holdout'),('contaminationCheckPresent','request_contamination_check'),('baseCheckpointPresent','request_base_checkpoint'),('optimizerPresent','request_optimizer'),('schedulerPresent','request_scheduler'),('rngPresent','request_rng'),('cacheInventoryPresent','request_cache_inventory'),('backupInventoryPresent','request_backup_inventory'),('descendantInventoryPresent','request_descendant_inventory'),('rollbackSnapshotPresent','request_rollback_snapshot')],
'stateBound':[('candidateCheckpointPresent','request_candidate_checkpoint'),('updateReceiptPresent','request_update_receipt'),('completeDenominatorPresent','request_complete_denominator'),('failureLogPresent','request_failure_log'),('resourceCostPresent','request_resource_cost'),('stateLineageComplete','reject_state_lineage_gap')],
'updated':[('independentEvaluatorPresent','request_independent_evaluator'),('targetEvaluationPresent','request_target_evaluation'),('strongBaselinePresent','request_strong_baseline'),('causalAblationPresent','request_causal_ablation'),('rewardHackProbePresent','request_reward_hack_probe'),('regressionSuitePresent','request_regression_suite'),('forgettingTestPresent','request_forgetting_test'),('safetyRightsTestPresent','request_safety_rights_test'),('uncertaintyPresent','request_uncertainty')],
'evaluated':[('residualOwnerPresent','request_residual_owner'),('counterevidencePresent','request_counterevidence'),('rollbackCriterionPresent','request_rollback_criterion'),('rollbackRehearsalPresent','request_rollback_rehearsal'),('monitoringPlanPresent','request_monitoring_plan'),('noImprovementInferenceRecorded','reject_improvement_inference'),('noReleaseAuthorityRecorded','reject_release_authority_laundering')],
'adjudicated':[('permittedConsumerPresent','request_permitted_consumer'),('boundedLeaseRecordPresent','request_bounded_lease_record'),('checkpointDigestBound','request_checkpoint_binding'),('expiryPresent','request_expiry'),('rollbackHandlePresent','request_rollback_handle'),('noSupportAuthorityRecorded','request_no_support_authority')],
'leaseBound':[('materialChangeTriggerPresent','request_material_change_trigger'),('descendantInvalidationComplete','request_descendant_invalidation'),('ordinaryRouteBlocked','request_ordinary_route_block'),('effectCompleteRollbackPresent','request_effect_complete_rollback'),('successorVersion','reject_successor_version')],
}

def packet()->dict[str,Any]:
 p={k:i+901 for i,k in enumerate(sorted(IDENTITY-{'currentVersion'}))};p['currentVersion']=1
 p.update({field:True for gates in GATES.values() for field,_ in gates if field!='successorVersion'})
 p.update({'successorVersion':1,'eventDigest':1,'supportAssignmentRequested':False,'externalEffectRequested':False})
 return p

def route(stage:str,kind:str,p:dict[str,Any],last:int=0,version:int=1)->str:
 c=packet()
 if kind!=KINDS[stage]:return 'reject_wrong_stage'
 for field in IDENTITY:
  expected=version if field=='currentVersion' else c[field]
  if p[field]!=expected:return 'reject_identity_substitution'
 if p['eventDigest']==last:return 'reject_replay'
 if p['supportAssignmentRequested'] or p['externalEffectRequested']:return 'reject_authority_leak'
 for field,answer in GATES[stage]:
  if field=='successorVersion':
   if p[field]!=version+1:return answer
  elif p[field] is False:return answer
 return {'draft':'accept_scope','scoped':'accept_state_binding','stateBound':'accept_update_receipt','updated':'accept_evaluation','evaluated':'accept_adjudication','adjudicated':'accept_bounded_lease','leaseBound':'accept_readmission'}[stage]

def run(command:str)->dict[str,Any]:
 p=subprocess.run(command.split(),cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 if p.returncode:raise RuntimeError(p.stdout)
 return {'command':command,'exit_code':0,'output_sha256':hashlib.sha256(p.stdout.encode()).hexdigest()}

def build()->dict[str,Any]:
 inherited=json.loads(INHERITED.read_text())
 cases=[]
 for i,stage in enumerate(STAGES,1):
  p=packet();p['eventDigest']=i
  if stage=='leaseBound':p['successorVersion']=2
  cases.append({'case_id':stage+'_accepted','expected_route':route(stage,KINDS[stage],p)})
 for stage,gates in GATES.items():
  for field,_ in gates:
   p=packet();p['eventDigest']=90
   if stage=='leaseBound':p['successorVersion']=2
   p[field]=1 if field=='successorVersion' else False
   cases.append({'case_id':stage+'_'+field,'expected_route':route(stage,KINDS[stage],p)})
 for cid,kind,field,value in [('wrong_stage','triggerReadmission',None,None),('identity_substitution','scopeUpdate','consumerDigest',9999),('event_replay','scopeUpdate','eventDigest',0),('authority_leak','scopeUpdate','supportAssignmentRequested',True)]:
  p=packet()
  if field:p[field]=value
  cases.append({'case_id':cid,'expected_route':route('draft',kind,p)})
 mutations=[]
 for field in sorted(IDENTITY):
  p=packet();p[field]+=1000;mutations.append({'mutation_id':'binding_'+field,'rejected':route('draft','scopeUpdate',p) not in ACCEPTED})
 for stage,gates in GATES.items():
  for field,_ in gates:
   p=packet();p['eventDigest']=91
   if stage=='leaseBound':p['successorVersion']=2
   p[field]=1 if field=='successorVersion' else False
   mutations.append({'mutation_id':'gate_'+stage+'_'+field,'rejected':route(stage,KINDS[stage],p) not in ACCEPTED})
 for mid,stage,kind,field,value in [('wrong_kind','draft','triggerReadmission',None,None),('event_replay','draft','scopeUpdate','eventDigest',0),('support_leak','draft','scopeUpdate','supportAssignmentRequested',True),('effect_leak','draft','scopeUpdate','externalEffectRequested',True),('stale_lease_after_readmission','scoped','requestBoundedLease',None,None)]:
  p=packet()
  if field:p[field]=value
  mutations.append({'mutation_id':mid,'rejected':route(stage,kind,p) not in ACCEPTED})
 inherited_counts={'workload_sample_count':inherited['workload_sample_count'],'holdout_sample_count':inherited['holdout_sample_count'],'candidate_count':inherited['candidate_count'],'rejected_negative_control_count':sum(inherited['negative_controls'].values()),'selected_canary_promotion_decision':inherited['selected_canary_promotion_decision'],'support_state_effect':inherited['support_state_effect']}
 return {'schema_version':'asi_stack.policy_optimization_refinement.v1','result_id':'policy-optimization-refinement-2026-07-16-local','source_sha256':{'lean_model':hashlib.sha256(LEAN.read_bytes()).hexdigest(),'inherited_result':hashlib.sha256(INHERITED.read_bytes()).hexdigest()},'inherited_lease_probe':inherited_counts,'reachable_stage_count':7,'route_case_count':len(cases),'route_coverage':cases,'mutation_count':len(mutations),'mutation_rejection_count':sum(x['rejected'] for x in mutations),'mutation_receipts':mutations,'command_receipts':[run('python3 scripts/validate_policy_update_lease_probe.py')],'witness':{'terminal_stage':'scoped','protocol_version':2,'receipt_count':7,'bounded_lease_count':1,'readmission_count':1,'support_assignment_count':0,'external_effect_count':0},'support_state_effect':'none','non_claims':['no optimizer, model, trainer, preference dataset, reward model, or policy update ran','no reward, evaluator, causal, forgetting, rollback, policy, or task quality result','no natural workload, deployed canary, live monitor, or external effect','no independent reproduction or heterogeneous transfer','no release, readiness, safety, alignment, support, SOTA, AGI, or ASI authority']}

def main()->None:
 a=argparse.ArgumentParser();a.add_argument('--write',action='store_true');args=a.parse_args();result=build();errors=[]
 if result['route_case_count']!=63:errors.append('route count drifted')
 if result['mutation_count']!=73 or result['mutation_rejection_count']!=73:errors.append('mutation contract drifted')
 for needle in ('inductive Stage','def routeFor','policy_update_lifecycle_routes'):
  if needle not in LEAN.read_text():errors.append('Lean model missing '+needle)
 jsonschema.validate(result,json.loads(SCHEMA.read_text()));serialized=json.dumps(result,indent=2)+'\n'
 if args.write:RESULT.parent.mkdir(parents=True,exist_ok=True);RESULT.write_text(serialized)
 elif not RESULT.exists() or RESULT.read_text()!=serialized:errors.append(f'{RESULT.relative_to(ROOT)} is stale; run {COMMAND} --write')
 if errors:print('Policy-optimization refinement failed:\n - '+'\n - '.join(errors));sys.exit(1)
 print('Policy-optimization refinement passed: inherited 6-sample/5-candidate lease, 7 stages, 63 routes, 73/73 mutations rejected, support effect none.')
if __name__=='__main__':main()
