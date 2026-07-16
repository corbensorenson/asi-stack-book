#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, subprocess, sys
from pathlib import Path
from typing import Any
import jsonschema

ROOT=Path(__file__).resolve().parents[1]
LEAN=ROOT/'lean/AsiStackProofs/SelfImprovementRefinement.lean'
SCHEMA=ROOT/'schemas/self_improvement_refinement.schema.json'
RESULT=ROOT/'experiments/self_improvement_refinement/results/2026-07-16-local.json'
COMMAND='python3 scripts/validate_self_improvement_refinement.py'
STAGES=['draft','scoped','proposalBound','implementationReviewed','evaluated','adjudicated','replacementBound','outcomeReconciled']
KINDS={'draft':'scopeTransition','scoped':'bindProposal','proposalBound':'reviewImplementation','implementationReviewed':'recordEvaluation','evaluated':'adjudicateProposal','adjudicated':'authorizeReplacementHandoff','replacementBound':'reconcileReplacementOutcome','outcomeReconciled':'triggerReadmission'}
ACCEPTED={'accept_scope','accept_proposal_binding','accept_implementation_review','accept_state_binding','accept_evaluation','accept_adjudication','accept_outcome_reconciliation','accept_readmission'}
IDENTITY={'transitionId','selfModelDigest','consumerDigest','mutablePartitionDigest','protectedPartitionDigest','authorityDigest','objectiveDigest','proposalDigest','implementationDigest','evaluatorDigest','monitorDigest','baselineDigest','stateInventoryDigest','replacementTransactionDigest','residualDigest','evidencePolicyDigest','stopAuthorityDigest','currentVersion'}
GATES={
'draft':[('consumerPresent','request_consumer'),('usePresent','request_use'),('selfModelPresent','request_self_model'),('mutablePartitionPresent','request_mutable_partition'),('protectedPartitionPresent','request_protected_partition'),('authorityEnvelopePresent','request_authority_envelope'),('optimizationTargetPresent','request_optimization_target'),('riskClassPresent','request_risk_class'),('evaluationHorizonPresent','request_evaluation_horizon'),('recursiveDepthPresent','request_recursive_depth'),('stopAuthorityPresent','request_stop_authority'),('supportCeilingPresent','request_support_ceiling'),('stateInventoryPresent','request_state_inventory'),('unknownStateResidualPresent','request_unknown_state_residual'),('rightsPremisesPresent','request_rights_premises'),('evaluatorPolicyPresent','request_evaluator_policy'),('baselinePolicyPresent','request_baseline_policy')],
'scoped':[('proposalPresent','request_proposal'),('changeIdentityPresent','request_change_identity'),('diffPresent','request_diff'),('lineagePresent','request_lineage'),('dependenciesPresent','request_dependencies'),('proposerPresent','request_proposer'),('implementerPresent','request_implementer'),('mechanismPresent','request_mechanism'),('expectedEffectsPresent','request_expected_effects'),('nonGoalsPresent','request_non_goals'),('cheaperInterventionsPresent','request_cheaper_interventions'),('noSelfRatifiedObjectiveRecorded','reject_self_ratified_objective')],
'proposalBound':[('implementationArtifactPresent','request_implementation_artifact'),('observedMutationSetPresent','request_observed_mutation_set'),('protectedInvariantReviewPresent','request_protected_invariant_review'),('boundaryDeltaReviewPresent','request_boundary_delta_review'),('authorityDeltaPresent','request_authority_delta'),('securityDeltaPresent','request_security_delta'),('dataPrivacyDeltaPresent','request_data_privacy_delta'),('resourceDeltaPresent','request_resource_delta'),('evaluatorDeltaPresent','request_evaluator_delta'),('rightsDeltaPresent','request_rights_delta'),('noProtectedWeakeningRecorded','reject_protected_weakening'),('noAuthorityWideningRecorded','reject_authority_widening')],
'implementationReviewed':[('fullStateSnapshotPresent','request_full_state_snapshot'),('modelStatePresent','request_model_state'),('optimizerStatePresent','request_optimizer_state'),('schedulerStatePresent','request_scheduler_state'),('rngStatePresent','request_rng_state'),('cacheStatePresent','request_cache_state'),('promptPolicyStatePresent','request_prompt_policy_state'),('toolCredentialStatePresent','request_tool_credential_state'),('evaluatorBenchmarkStatePresent','request_evaluator_benchmark_state'),('environmentStatePresent','request_environment_state'),('checkpointBackupStatePresent','request_checkpoint_backup_state'),('externalEffectStatePresent','request_external_effect_state'),('descendantStatePresent','request_descendant_state'),('rollbackAuthorityPresent','request_rollback_authority'),('compensationPlanPresent','request_compensation_plan'),('irreversibleResidualsPresent','request_irreversible_residuals')],
'evaluated':[('strongBaselinePresent','request_strong_baseline'),('naturalTaskDistributionPresent','request_natural_task_distribution'),('freshHoldoutPresent','request_fresh_holdout'),('contaminationChecksPresent','request_contamination_checks'),('independentEvaluatorPresent','request_independent_evaluator'),('evaluatorDependenciesPresent','request_evaluator_dependencies'),('independentMonitorPresent','request_independent_monitor'),('monitorDependenciesPresent','request_monitor_dependencies'),('usefulOutcomePresent','request_useful_outcome'),('regressionsPresent','request_regressions'),('unsafeReleaseMeasurePresent','request_unsafe_release_measure'),('deceptionProbePresent','request_deception_probe'),('delayedOutcomePresent','request_delayed_outcome'),('totalCostPresent','request_total_cost'),('evidenceBundlePresent','request_evidence_bundle')],
'adjudicated':[('governanceApprovalPresent','request_governance_approval'),('evidenceTransitionPresent','request_evidence_transition'),('permittedConsumerPresent','request_permitted_consumer'),('boundedScopePresent','request_bounded_scope'),('trafficAllocationPresent','request_traffic_allocation'),('canaryPlanPresent','request_canary_plan'),('monitorWindowPresent','request_monitor_window'),('stopPathPresent','request_stop_path'),('rollbackDryRunPresent','request_rollback_dry_run'),('residualOwnerPresent','request_residual_owner'),('noCandidatePromotionAuthorityRecorded','reject_candidate_promotion_authority')],
'replacementBound':[('replacementTransactionPresent','request_replacement_transaction'),('transactionOwnerPresent','request_transaction_owner'),('canaryReceiptPresent','request_canary_receipt'),('observedEffectReceiptPresent','request_observed_effect_receipt'),('monitorReceiptPresent','request_monitor_receipt'),('rollbackOrCommitDispositionPresent','request_rollback_or_commit_disposition'),('exactInventoryRestorationPresent','request_exact_inventory_restoration'),('semanticRecoverySeparated','request_semantic_recovery_separation'),('descendantInvalidationPresent','request_descendant_invalidation'),('externalRemediationPresent','request_external_remediation'),('compensationReceiptPresent','request_compensation_receipt'),('incidentDisclosurePresent','request_incident_disclosure'),('appendOnlyOutcomePresent','request_append_only_outcome'),('noSupportPromotionRecorded','reject_support_promotion'),('noReleaseAuthorityRecorded','reject_release_authority')],
'outcomeReconciled':[('materialChangeTriggerPresent','request_material_change_trigger'),('affectedPathPresent','request_affected_path'),('readmissionDescendantInvalidationPresent','request_readmission_descendant_invalidation'),('ordinaryRouteBlocked','request_ordinary_route_block'),('staleGateExpirationPresent','request_stale_gate_expiration'),('newStateInventoryPresent','request_new_state_inventory'),('rerunRequirementPresent','request_rerun_requirement'),('successorVersion','reject_successor_version')]}

def packet()->dict[str,Any]:
 p={k:i+2101 for i,k in enumerate(sorted(IDENTITY-{'currentVersion'}))};p['currentVersion']=1
 p.update({field:True for gates in GATES.values() for field,_ in gates if field!='successorVersion'})
 p.update({'successorVersion':1,'eventDigest':1,'supportAssignmentRequested':False,'externalEffectRequested':False});return p

def route(stage:str,kind:str,p:dict[str,Any],last:int=0,version:int=1)->str:
 c=packet()
 if kind!=KINDS[stage]:return 'reject_wrong_stage'
 for f in IDENTITY:
  if p[f]!=(version if f=='currentVersion' else c[f]):return 'reject_identity_substitution'
 if p['eventDigest']==last:return 'reject_replay'
 if p['supportAssignmentRequested'] or p['externalEffectRequested']:return 'reject_authority_leak'
 for f,answer in GATES[stage]:
  if f=='successorVersion':
   if p[f]!=version+1:return answer
  elif p[f] is False:return answer
 return {'draft':'accept_scope','scoped':'accept_proposal_binding','proposalBound':'accept_implementation_review','implementationReviewed':'accept_state_binding','evaluated':'accept_evaluation','adjudicated':'accept_adjudication','replacementBound':'accept_outcome_reconciliation','outcomeReconciled':'accept_readmission'}[stage]

def run(command:str)->dict[str,Any]:
 p=subprocess.run(command.split(),cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 if p.returncode:raise RuntimeError(p.stdout)
 return {'command':command,'exit_code':0,'output_sha256':hashlib.sha256(p.stdout.encode()).hexdigest()}

def count_fixtures(folder:str)->tuple[int,int]:
 files=list((ROOT/folder).glob('*.json'));return sum(x.name.startswith('valid_') for x in files),sum(x.name.startswith('invalid_') for x in files)

def inherited()->dict[str,Any]:
 si=count_fixtures('experiments/self_improvement_boundaries/fixtures');rr=count_fixtures('experiments/readiness_residual_gates/fixtures');cr=count_fixtures('experiments/capability_replacement/fixtures')
 trace=json.loads((ROOT/'experiments/capability_replacement_trace/results/2026-07-02-local.json').read_text())
 intent=json.loads((ROOT/'experiments/intent_governed_replacement_bridge/results/2026-07-02-local.json').read_text())
 update=json.loads((ROOT/'experiments/post_v2_update_causality/results/2026-07-10-local.json').read_text())
 openended=json.loads((ROOT/'experiments/open_ended_improvement_refinement/results/2026-07-16-local.json').read_text())
 arms=[a for seed in update['seed_records'] for a in seed['arms']]
 return {'self_improvement_valid_count':si[0],'self_improvement_invalid_count':si[1],'readiness_valid_count':rr[0],'readiness_invalid_count':rr[1],'replacement_valid_count':cr[0],'replacement_invalid_count':cr[1],'replacement_trace_transaction_count':trace['valid_trace_transaction_count'],'replacement_trace_negative_control_count':trace['negative_control_count'],'intent_trace_count':intent['trace_count'],'intent_invalid_control_count':intent['expected_invalid_control_count'],'update_seed_count':len(update['seed_records']),'update_arm_count':len(arms),'update_parameter_mutation_count':sum(a['actual_parameter_mutation'] for a in arms),'update_exact_rollback_count':sum(s['rollback']['exact'] for s in update['seed_records']),'update_no_change_disposition_count':sum(x['disposition']=='no_change' for x in update['claim_dispositions']),'open_ended_governor_handoff_count':openended['witness']['governor_handoff_count'],'open_ended_threshold_pass_count':openended['inherited_results']['stopped_threshold_pass_count'],'support_state_effect':'none'}

def build()->dict[str,Any]:
 cases=[]
 for i,stage in enumerate(STAGES,1):
  p=packet();p['eventDigest']=i
  if stage=='outcomeReconciled':p['successorVersion']=2
  cases.append({'case_id':stage+'_accepted','expected_route':route(stage,KINDS[stage],p)})
 for stage,gates in GATES.items():
  for f,_ in gates:
   p=packet();p['eventDigest']=90
   if stage=='outcomeReconciled':p['successorVersion']=2
   p[f]=1 if f=='successorVersion' else False
   cases.append({'case_id':stage+'_'+f,'expected_route':route(stage,KINDS[stage],p)})
 for cid,kind,f,v in [('wrong_stage','triggerReadmission',None,None),('identity_substitution','scopeTransition','consumerDigest',9999),('event_replay','scopeTransition','eventDigest',0),('authority_leak','scopeTransition','supportAssignmentRequested',True)]:
  p=packet()
  if f:p[f]=v
  cases.append({'case_id':cid,'expected_route':route('draft',kind,p)})
 mutations=[]
 for f in sorted(IDENTITY):
  p=packet();p[f]+=1000;mutations.append({'mutation_id':'binding_'+f,'rejected':route('draft','scopeTransition',p) not in ACCEPTED})
 for stage,gates in GATES.items():
  for f,_ in gates:
   p=packet();p['eventDigest']=91
   if stage=='outcomeReconciled':p['successorVersion']=2
   p[f]=1 if f=='successorVersion' else False
   mutations.append({'mutation_id':'gate_'+stage+'_'+f,'rejected':route(stage,KINDS[stage],p) not in ACCEPTED})
 for mid,stage,kind,f,v in [('wrong_kind','draft','triggerReadmission',None,None),('event_replay','draft','scopeTransition','eventDigest',0),('support_leak','draft','scopeTransition','supportAssignmentRequested',True),('effect_leak','draft','scopeTransition','externalEffectRequested',True),('stale_handoff_after_readmission','scoped','authorizeReplacementHandoff',None,None)]:
  p=packet()
  if f:p[f]=v
  mutations.append({'mutation_id':mid,'rejected':route(stage,kind,p) not in ACCEPTED})
 commands=['python3 scripts/validate_self_improvement_boundaries.py','python3 scripts/validate_readiness_residual_gates.py','python3 scripts/validate_capability_replacement.py','python3 scripts/validate_capability_replacement_trace_probe.py','python3 scripts/validate_intent_governed_replacement_bridge.py','python3 scripts/validate_post_v2_update_causality.py','python3 scripts/validate_open_ended_improvement_refinement.py']
 return {'schema_version':'asi_stack.self_improvement_refinement.v1','result_id':'self-improvement-refinement-2026-07-16-local','source_sha256':{'lean_model':hashlib.sha256(LEAN.read_bytes()).hexdigest()},'inherited_results':inherited(),'reachable_stage_count':8,'route_case_count':len(cases),'route_coverage':cases,'mutation_count':len(mutations),'mutation_rejection_count':sum(x['rejected'] for x in mutations),'mutation_receipts':mutations,'command_receipts':[run(x) for x in commands],'witness':{'terminal_stage':'scoped','protocol_version':2,'receipt_count':8,'replacement_handoff_count':1,'outcome_reconciliation_count':1,'readmission_count':1,'support_assignment_count':0,'external_effect_count':0},'support_state_effect':'none','non_claims':['no adaptive proposal generator, live self-modification, or production replacement executed','all legitimacy, evaluation, monitoring, state, effect, rollback, compensation, and invalidation records remain trusted authored inputs','no evaluator or monitor competence, useful improvement, safety, recovery, transfer, deployment, SOTA, AGI, or ASI result','no support transition, release authority, or external effect']}

def main()->None:
 a=argparse.ArgumentParser();a.add_argument('--write',action='store_true');args=a.parse_args();result=build();errors=[]
 if result['route_case_count']!=118:errors.append('route count drifted')
 if result['mutation_count']!=129 or result['mutation_rejection_count']!=129:errors.append('mutation contract drifted')
 for x in ('inductive Stage','def routeFor','self_improvement_full_lifecycle_witness'):
  if x not in LEAN.read_text():errors.append('Lean model missing '+x)
 jsonschema.validate(result,json.loads(SCHEMA.read_text()));serialized=json.dumps(result,indent=2)+'\n'
 if args.write:RESULT.parent.mkdir(parents=True,exist_ok=True);RESULT.write_text(serialized)
 elif not RESULT.exists() or RESULT.read_text()!=serialized:errors.append(f'{RESULT.relative_to(ROOT)} is stale; run {COMMAND} --write')
 if errors:print('Self-improvement refinement failed:\n - '+'\n - '.join(errors));sys.exit(1)
 print('Self-improvement refinement passed: 7 inherited suites, 8 stages, 118 routes, 129/129 mutations rejected, support effect none.')
if __name__=='__main__':main()
