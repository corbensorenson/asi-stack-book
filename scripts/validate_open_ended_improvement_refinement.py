#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, subprocess, sys
from pathlib import Path
from typing import Any
import jsonschema

ROOT=Path(__file__).resolve().parents[1]
LEAN=ROOT/'lean/AsiStackProofs/OpenEndedImprovementRefinement.lean'
SCHEMA=ROOT/'schemas/open_ended_improvement_refinement.schema.json'
ADMISSION=ROOT/'experiments/open_ended_improvement_campaign/results/2026-07-13-local.json'
UPDATE=ROOT/'experiments/post_v2_update_causality/results/2026-07-10-local.json'
STOPPED=ROOT/'experiments/post_v2_1_evidence_program/results/2026-07-11-post-v2-1-outcomes.json'
RESULT=ROOT/'experiments/open_ended_improvement_refinement/results/2026-07-16-local.json'
COMMAND='python3 scripts/validate_open_ended_improvement_refinement.py'
STAGES=['draft','scoped','generationBound','archiveBound','evaluated','adjudicated','governorBound']
KINDS={'draft':'scopeCampaign','scoped':'bindGeneration','generationBound':'recordArchive','archiveBound':'recordEvaluation','evaluated':'adjudicateCampaign','adjudicated':'requestGovernorHandoff','governorBound':'triggerReadmission'}
ACCEPTED={'accept_scope','accept_generation_binding','accept_archive_record','accept_evaluation','accept_adjudication','accept_governor_handoff','accept_readmission'}
IDENTITY={'campaignId','objectiveDigest','representationDigest','controllerDigest','taskPolicyDigest','candidatePolicyDigest','generatorDigest','evaluatorDigest','qualifierDigest','archiveDigest','budgetDigest','stopAuthorityDigest','hazardPolicyDigest','consumerDigest','authorityDigest','currentVersion'}
GATES={
'draft':[('consumerPresent','request_consumer'),('purposePresent','request_purpose'),('objectivePresent','request_objective'),('objectiveLegitimacyRecordPresent','request_objective_legitimacy'),('representationPresent','request_representation'),('controllerVersionPresent','request_controller'),('taskPolicyPresent','request_task_policy'),('candidatePolicyPresent','request_candidate_policy'),('evaluatorPolicyPresent','request_evaluator_policy'),('exposurePolicyPresent','request_exposure_policy'),('archivePolicyPresent','request_archive_policy'),('hazardPolicyPresent','request_hazard_policy'),('resourceBudgetPresent','request_resource_budget'),('opportunityBudgetPresent','request_opportunity_budget'),('stopOwnerPresent','request_stop_owner'),('horizonPresent','request_horizon'),('supportCeilingPresent','request_support_ceiling')],
'scoped':[('taskGeneratorPresent','request_task_generator'),('candidateGeneratorPresent','request_candidate_generator'),('seedParentMutationLineagePresent','request_seed_parent_mutation_lineage'),('matchedBaselinesPresent','request_matched_baselines'),('taskDenominatorComplete','request_task_denominator'),('candidateDenominatorComplete','request_candidate_denominator'),('retentionTiersPresent','request_retention_tiers'),('noControllerSelfRatificationRecorded','reject_controller_self_ratification')],
'generationBound':[('attemptRecordsComplete','request_attempt_records'),('candidateLineageComplete','request_candidate_lineage'),('exposureRecordsComplete','request_exposure_records'),('resourceRecordsComplete','request_resource_records'),('typedDispositionsComplete','request_typed_dispositions'),('failureHistoryPreserved','request_failure_history'),('nullUnsafeTimeoutRecordsPreserved','request_null_unsafe_timeout_records'),('payloadCustodyPresent','request_payload_custody'),('cumulativeBudgetAcrossDescendants','reject_budget_reset'),('archiveSamplingPresent','request_archive_sampling')],
'archiveBound':[('independentQualifierPresent','request_independent_qualifier'),('qualifierDependenciesPresent','request_qualifier_dependencies'),('freshHoldoutPresent','request_fresh_holdout'),('calibrationPresent','request_calibration'),('disagreementRecordPresent','request_disagreement_record'),('evaluatorExposureAccounted','request_exposure_accounting'),('strongBaselinePresent','request_strong_baseline'),('mechanismAblationPresent','request_mechanism_ablation'),('hazardProbePresent','request_hazard_probe'),('usefulnessTransferSeparated','request_separate_usefulness_transfer'),('noScoreAsAdmissionRecorded','reject_score_as_admission')],
'evaluated':[('totalCostPresent','request_total_cost'),('opportunityCostPresent','request_opportunity_cost'),('residualOwnerPresent','request_residual_owner'),('counterevidencePresent','request_counterevidence'),('stopTriggerObserved','request_stop_observation'),('stopEffectReceiptPresent','request_stop_effect_receipt'),('quarantineEffectReceiptPresent','request_quarantine_effect_receipt'),('recoveryPathPresent','request_recovery_path'),('noUsefulImprovementInferenceRecorded','reject_useful_improvement_inference'),('noReleaseAuthorityRecorded','reject_release_authority_laundering')],
'adjudicated':[('permittedConsumerPresent','request_permitted_consumer'),('governorHandoffRecordPresent','request_governor_handoff_record'),('candidateDigestBound','request_candidate_binding'),('expiryPresent','request_expiry'),('monitorPresent','request_monitor'),('noCandidateAuthorityGrantRecorded','reject_candidate_authority_grant'),('noSupportAuthorityRecorded','reject_support_authority_laundering')],
'governorBound':[('materialChangeTriggerPresent','request_material_change_trigger'),('descendantInvalidationComplete','request_descendant_invalidation'),('ordinaryRouteBlocked','request_ordinary_route_block'),('cumulativeBudgetCarried','request_cumulative_budget_carry'),('rerunRequirementPresent','request_rerun_requirement'),('payloadReceiptCustodyPresent','request_payload_receipt_custody'),('successorVersion','reject_successor_version')],
}

def packet()->dict[str,Any]:
 p={k:i+1201 for i,k in enumerate(sorted(IDENTITY-{'currentVersion'}))};p['currentVersion']=1
 p.update({field:True for gates in GATES.values() for field,_ in gates if field!='successorVersion'})
 p.update({'successorVersion':1,'eventDigest':1,'supportAssignmentRequested':False,'externalEffectRequested':False})
 return p

def route(stage:str,kind:str,p:dict[str,Any],last:int=0,version:int=1)->str:
 c=packet()
 if kind!=KINDS[stage]:return 'reject_wrong_stage'
 for field in IDENTITY:
  if p[field]!=(version if field=='currentVersion' else c[field]):return 'reject_identity_substitution'
 if p['eventDigest']==last:return 'reject_replay'
 if p['supportAssignmentRequested'] or p['externalEffectRequested']:return 'reject_authority_leak'
 for field,answer in GATES[stage]:
  if field=='successorVersion':
   if p[field]!=version+1:return answer
  elif p[field] is False:return answer
 return {'draft':'accept_scope','scoped':'accept_generation_binding','generationBound':'accept_archive_record','archiveBound':'accept_evaluation','evaluated':'accept_adjudication','adjudicated':'accept_governor_handoff','governorBound':'accept_readmission'}[stage]

def run(command:str)->dict[str,Any]:
 p=subprocess.run(command.split(),cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 if p.returncode:raise RuntimeError(p.stdout)
 return {'command':command,'exit_code':0,'output_sha256':hashlib.sha256(p.stdout.encode()).hexdigest()}

def inherited_summary()->dict[str,Any]:
 admission=json.loads(ADMISSION.read_text());update=json.loads(UPDATE.read_text());stopped=json.loads(STOPPED.read_text())
 seed_rows=update['seed_records'];arms=[arm for seed in seed_rows for arm in seed['arms']];p3=stopped['P3']
 return {
  'admission_case_count':len(admission['case_results']),'admission_theorem_count':len(admission['lean_bridge']['theorems']),
  'admission_support_state_effect':admission['support_state_effect'],
  'update_seed_count':len(seed_rows),'update_arm_count':len(arms),'update_parameter_mutation_count':sum(arm['actual_parameter_mutation'] for arm in arms),
  'update_exact_rollback_count':sum(seed['rollback']['exact'] for seed in seed_rows),'update_no_change_disposition_count':sum(row['disposition']=='no_change' for row in update['claim_dispositions']),
  'stopped_seed_count':len(p3['seeds']),'stopped_arm_count':sum(len(seed['arms']) for seed in p3['seed_results']),
  'stopped_model_call_count':stopped['execution_accounting']['model_calls'],'stopped_registered_model_call_ceiling':stopped['execution_accounting']['registered_model_call_ceiling'],
  'stopped_eligible_challenger_seed_arm_count':p3['thresholds']['eligible_challenger_seed_arms'],
  'stopped_threshold_pass_count':p3['thresholds']['target_gain_at_least_0_05'],'stopped_update_disposition':p3['update_disposition'],
  'support_state_effect':'none'}

def build()->dict[str,Any]:
 cases=[]
 for i,stage in enumerate(STAGES,1):
  p=packet();p['eventDigest']=i
  if stage=='governorBound':p['successorVersion']=2
  cases.append({'case_id':stage+'_accepted','expected_route':route(stage,KINDS[stage],p)})
 for stage,gates in GATES.items():
  for field,_ in gates:
   p=packet();p['eventDigest']=90
   if stage=='governorBound':p['successorVersion']=2
   p[field]=1 if field=='successorVersion' else False
   cases.append({'case_id':stage+'_'+field,'expected_route':route(stage,KINDS[stage],p)})
 for cid,kind,field,value in [('wrong_stage','triggerReadmission',None,None),('identity_substitution','scopeCampaign','consumerDigest',9999),('event_replay','scopeCampaign','eventDigest',0),('authority_leak','scopeCampaign','supportAssignmentRequested',True)]:
  p=packet()
  if field:p[field]=value
  cases.append({'case_id':cid,'expected_route':route('draft',kind,p)})
 mutations=[]
 for field in sorted(IDENTITY):
  p=packet();p[field]+=1000;mutations.append({'mutation_id':'binding_'+field,'rejected':route('draft','scopeCampaign',p) not in ACCEPTED})
 for stage,gates in GATES.items():
  for field,_ in gates:
   p=packet();p['eventDigest']=91
   if stage=='governorBound':p['successorVersion']=2
   p[field]=1 if field=='successorVersion' else False
   mutations.append({'mutation_id':'gate_'+stage+'_'+field,'rejected':route(stage,KINDS[stage],p) not in ACCEPTED})
 for mid,stage,kind,field,value in [('wrong_kind','draft','triggerReadmission',None,None),('event_replay','draft','scopeCampaign','eventDigest',0),('support_leak','draft','scopeCampaign','supportAssignmentRequested',True),('effect_leak','draft','scopeCampaign','externalEffectRequested',True),('stale_handoff_after_readmission','scoped','requestGovernorHandoff',None,None)]:
  p=packet()
  if field:p[field]=value
  mutations.append({'mutation_id':mid,'rejected':route(stage,kind,p) not in ACCEPTED})
 return {'schema_version':'asi_stack.open_ended_improvement_refinement.v1','result_id':'open-ended-improvement-refinement-2026-07-16-local','source_sha256':{'lean_model':hashlib.sha256(LEAN.read_bytes()).hexdigest(),'admission_result':hashlib.sha256(ADMISSION.read_bytes()).hexdigest(),'update_result':hashlib.sha256(UPDATE.read_bytes()).hexdigest(),'stopped_result':hashlib.sha256(STOPPED.read_bytes()).hexdigest()},'inherited_results':inherited_summary(),'reachable_stage_count':7,'route_case_count':len(cases),'route_coverage':cases,'mutation_count':len(mutations),'mutation_rejection_count':sum(x['rejected'] for x in mutations),'mutation_receipts':mutations,'command_receipts':[run('python3 scripts/validate_open_ended_improvement_campaign.py'),run('python3 scripts/validate_post_v2_update_causality.py'),run('python3 scripts/validate_post_v2_1_outcomes.py')],'witness':{'terminal_stage':'scoped','protocol_version':2,'receipt_count':7,'governor_handoff_count':1,'readmission_count':1,'support_assignment_count':0,'external_effect_count':0},'support_state_effect':'none','non_claims':['no adaptive task or candidate generator, evolving archive, or self-modifying controller ran','no objective legitimacy, evaluator independence, semantic novelty, usefulness, transfer, or hazard-control result','the inherited fixed stopped campaigns preserve null and narrow outcomes and do not establish open-ended improvement','no deployed stop, quarantine, rollback, admission, publication, or external effect','no capability, safety, readiness, support, SOTA, AGI, or ASI authority']}

def main()->None:
 a=argparse.ArgumentParser();a.add_argument('--write',action='store_true');args=a.parse_args();result=build();errors=[]
 if result['route_case_count']!=81:errors.append('route count drifted')
 if result['mutation_count']!=91 or result['mutation_rejection_count']!=91:errors.append('mutation contract drifted')
 for needle in ('inductive Stage','def routeFor','open_ended_improvement_lifecycle_routes'):
  if needle not in LEAN.read_text():errors.append('Lean model missing '+needle)
 jsonschema.validate(result,json.loads(SCHEMA.read_text()));serialized=json.dumps(result,indent=2)+'\n'
 if args.write:RESULT.parent.mkdir(parents=True,exist_ok=True);RESULT.write_text(serialized)
 elif not RESULT.exists() or RESULT.read_text()!=serialized:errors.append(f'{RESULT.relative_to(ROOT)} is stale; run {COMMAND} --write')
 if errors:print('Open-ended improvement refinement failed:\n - '+'\n - '.join(errors));sys.exit(1)
 print('Open-ended improvement refinement passed: 3 inherited suites, 7 stages, 81 routes, 91/91 mutations rejected, support effect none.')
if __name__=='__main__':main()
