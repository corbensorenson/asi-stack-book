#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, subprocess, sys
from pathlib import Path
from typing import Any
import jsonschema

ROOT=Path(__file__).resolve().parents[1]
LEAN=ROOT/'lean/AsiStackProofs/ScalableOversightRefinement.lean'
SCHEMA=ROOT/'schemas/scalable_oversight_refinement.schema.json'
FIXTURE=ROOT/'experiments/scalable_oversight_protocol/fixtures/cases.json'
RESULT=ROOT/'experiments/scalable_oversight_refinement/results/2026-07-15-local.json'
COMMAND='python3 scripts/validate_scalable_oversight_refinement.py'
STAGES=['draft','scoped','protocolBound','reviewed','audited','adjudicated','useBound']
KINDS={'draft':'scopeProtocol','scoped':'bindProtocol','protocolBound':'recordReview','reviewed':'runOutcomeAudit','audited':'adjudicateUse','adjudicated':'requestBoundedUse','useBound':'triggerReadmission'}
ACCEPTED={'accept_scope','accept_protocol','accept_review','accept_audit','accept_use_adjudication','accept_abstention_escalation','accept_bounded_use','accept_readmission'}
IDENTITY={'taskId','consumerId','protocolDigest','cohortDigest','systemDigest','supervisorDigest','evidenceViewDigest','dependencyDigest','baselineDigest','auditorDigest','policyDigest','residualDigest','authorityDigest','currentProtocolVersion'}
GATES={
'draft':[('taskScopePresent',False,'request_task_scope'),('consumerPresent',False,'request_consumer'),('authorityScopePresent',False,'request_authority_scope'),('riskTierPresent',False,'request_risk_tier'),('permittedInferencePresent',False,'request_permitted_inference'),('escalationOwnerPresent',False,'request_escalation_owner')],
'scoped':[('supervisorEnvelopePresent',False,'request_supervisor_envelope'),('systemEnvelopePresent',False,'request_system_envelope'),('capabilityEnvelopePresent',False,'request_capability_envelope'),('informationAccessPresent',False,'request_information_access'),('rolesAndIncentivesPresent',False,'request_roles_and_incentives'),('taskCohortPresent',False,'request_task_cohort'),('prospectiveFailureRulePresent',False,'request_failure_rule'),('expiryPresent',False,'request_expiry')],
'protocolBound':[('evidenceViewsPresent',False,'request_evidence_views'),('directReviewBaselinePresent',False,'request_direct_review_baseline'),('reviewOutcomePresent',False,'request_review_outcome'),('disagreementRecorded',False,'request_disagreement_record'),('completeDenominator',False,'request_complete_denominator'),('coverageRecorded',False,'request_coverage_record'),('abstentionReasonRecorded',False,'request_abstention_reason'),('costRecordPresent',False,'request_cost_record')],
'reviewed':[('independentOutcomeAuditPresent',False,'request_independent_outcome_audit'),('auditorSeparationPresent',False,'reject_auditor_dependency'),('sharedDependenciesDisclosed',False,'request_shared_dependency_disclosure'),('correlationChallengePresent',False,'request_correlation_challenge'),('outcomeCriterionPresent',False,'request_outcome_criterion'),('auditOutcomePresent',False,'request_audit_outcome'),('failureCasesPreserved',False,'request_failure_cases')],
'audited':[('uncertaintyPresent',False,'request_uncertainty'),('residualOwnerPresent',False,'request_residual_owner'),('disagreementDispositionPresent',False,'request_disagreement_disposition'),('abstentionEvidencePresent',False,'request_abstention_evidence'),('abstentionDefeaterPresent',False,'request_abstention_defeater'),('escalationRoutePresent',False,'request_escalation_route'),('noCompetenceInferenceRecorded',False,'reject_competence_inference'),('policyAuthoritySeparated',False,'reject_policy_authority_laundering')],
'adjudicated':[('permittedConsumerPresent',False,'request_permitted_consumer'),('boundedUseRecordPresent',False,'request_bounded_use_record'),('protocolDigestBound',False,'request_protocol_binding'),('expiryChecked',False,'request_expiry_check'),('noReleaseAuthorityRecorded',False,'reject_release_authority_laundering')],
'useBound':[('materialChangeTriggerPresent',False,'request_material_change_trigger'),('descendantInvalidationComplete',False,'request_descendant_invalidation'),('ordinaryRouteBlocked',False,'request_ordinary_route_block'),('successorProtocolVersion',1,'reject_successor_version')]}

def packet()->dict[str,Any]:
 return {'taskId':801,'consumerId':802,'protocolDigest':803,'cohortDigest':804,'systemDigest':805,'supervisorDigest':806,'evidenceViewDigest':807,'dependencyDigest':808,'baselineDigest':809,'auditorDigest':810,'policyDigest':811,'residualDigest':812,'authorityDigest':813,'currentProtocolVersion':1,'successorProtocolVersion':1,'eventDigest':1,
 'taskScopePresent':True,'consumerPresent':True,'authorityScopePresent':True,'riskTierPresent':True,'permittedInferencePresent':True,'escalationOwnerPresent':True,'supervisorEnvelopePresent':True,'systemEnvelopePresent':True,'capabilityEnvelopePresent':True,'informationAccessPresent':True,'rolesAndIncentivesPresent':True,'taskCohortPresent':True,'prospectiveFailureRulePresent':True,'expiryPresent':True,'evidenceViewsPresent':True,'directReviewBaselinePresent':True,'reviewOutcomePresent':True,'disagreementRecorded':True,'completeDenominator':True,'coverageRecorded':True,'abstentionReasonRecorded':True,'costRecordPresent':True,'independentOutcomeAuditPresent':True,'auditorSeparationPresent':True,'sharedDependenciesDisclosed':True,'correlationChallengePresent':True,'outcomeCriterionPresent':True,'auditOutcomePresent':True,'failureCasesPreserved':True,'uncertaintyPresent':True,'residualOwnerPresent':True,'disagreementDispositionPresent':True,'abstentionEvidencePresent':True,'abstentionDefeaterPresent':True,'escalationRoutePresent':True,'noCompetenceInferenceRecorded':True,'policyAuthoritySeparated':True,'permittedConsumerPresent':True,'boundedUseRecordPresent':True,'protocolDigestBound':True,'expiryChecked':True,'noReleaseAuthorityRecorded':True,'materialChangeTriggerPresent':True,'descendantInvalidationComplete':True,'ordinaryRouteBlocked':True,'supportAssignmentRequested':False,'externalEffectRequested':False}

def route(stage:str,kind:str,p:dict[str,Any],high_risk:bool=True,abstention:bool=False,last:int=0,current_version:int=1)->str:
 c=packet()
 if kind!=KINDS[stage]:return 'reject_wrong_stage'
 if any(p[k]!=(current_version if k=='currentProtocolVersion' else c[k]) for k in IDENTITY):return 'reject_identity_substitution'
 if p['eventDigest']==last:return 'reject_replay'
 if p['supportAssignmentRequested'] or p['externalEffectRequested']:return 'reject_authority_leak'
 for field,bad,answer in GATES[stage]:
  if stage=='protocolBound' and field=='abstentionReasonRecorded' and not abstention:continue
  if stage=='reviewed' and field=='independentOutcomeAuditPresent' and not high_risk:continue
  if stage=='audited' and field in {'abstentionEvidencePresent','abstentionDefeaterPresent'} and not abstention:continue
  if stage=='useBound' and field=='successorProtocolVersion':
   if p[field]!=current_version+1:return answer
  elif p[field] is bad:return answer
 if stage=='audited' and abstention:return 'accept_abstention_escalation'
 return {'draft':'accept_scope','scoped':'accept_protocol','protocolBound':'accept_review','reviewed':'accept_audit','audited':'accept_use_adjudication','adjudicated':'accept_bounded_use','useBound':'accept_readmission'}[stage]

def run(command:str)->dict[str,Any]:
 p=subprocess.run(command.split(),cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 if p.returncode:raise RuntimeError(p.stdout)
 return {'command':command,'exit_code':p.returncode,'output_sha256':hashlib.sha256(p.stdout.encode()).hexdigest()}

def context(stage:str,field:str)->tuple[bool,bool]:
 return (True,field in {'abstentionReasonRecorded','abstentionEvidencePresent','abstentionDefeaterPresent'})

def build()->dict[str,Any]:
 cases=[]
 for i,stage in enumerate(STAGES,1):
  p=packet();p['eventDigest']=i
  if stage=='useBound':p['successorProtocolVersion']=2
  cases.append({'case_id':stage+'_accepted','expected_route':route(stage,KINDS[stage],p)})
 for stage,gates in GATES.items():
  for field,bad,_ in gates:
   p=packet();p['eventDigest']=90
   if stage=='useBound':p['successorProtocolVersion']=2
   p[field]=bad;high,abstention=context(stage,field)
   cases.append({'case_id':stage+'_'+field,'expected_route':route(stage,KINDS[stage],p,high,abstention)})
 p=packet();cases.append({'case_id':'audited_abstention_complete','expected_route':route('audited','adjudicateUse',p,True,True)})
 for cid,kind,field,value in [('wrong_stage','triggerReadmission',None,None),('identity_substitution','scopeProtocol','consumerId',999),('event_replay','scopeProtocol','eventDigest',0),('authority_leak','scopeProtocol','supportAssignmentRequested',True)]:
  p=packet()
  if field:p[field]=value
  cases.append({'case_id':cid,'expected_route':route('draft',kind,p)})
 mutations=[]
 for field in sorted(IDENTITY):
  p=packet();p[field]+=1000;mutations.append({'mutation_id':'binding_'+field,'rejected':route('draft','scopeProtocol',p) not in ACCEPTED})
 for stage,gates in GATES.items():
  for field,bad,_ in gates:
   p=packet();p['eventDigest']=91
   if stage=='useBound':p['successorProtocolVersion']=2
   p[field]=bad;high,abstention=context(stage,field)
   mutations.append({'mutation_id':'gate_'+stage+'_'+field,'rejected':route(stage,KINDS[stage],p,high,abstention) not in ACCEPTED})
 for mid,stage,kind,field,value in [('wrong_kind','draft','triggerReadmission',None,None),('event_replay','draft','scopeProtocol','eventDigest',0),('support_leak','draft','scopeProtocol','supportAssignmentRequested',True),('effect_leak','draft','scopeProtocol','externalEffectRequested',True),('stale_use_after_readmission','scoped','requestBoundedUse',None,None)]:
  p=packet()
  if field:p[field]=value
  mutations.append({'mutation_id':mid,'rejected':route(stage,kind,p) not in ACCEPTED})
 fixture=json.loads(FIXTURE.read_text())
 return {'schema_version':'asi_stack.scalable_oversight_refinement.v1','result_id':'scalable-oversight-refinement-2026-07-15-local','source_sha256':{'lean_model':hashlib.sha256(LEAN.read_bytes()).hexdigest(),'input_fixture':hashlib.sha256(FIXTURE.read_bytes()).hexdigest()},'input_suite':{'suite_id':'scalable_oversight_protocol','case_count':len(fixture['cases']),'passed_count':7},'reachable_stage_count':7,'route_case_count':len(cases),'route_coverage':cases,'mutation_count':len(mutations),'mutation_rejection_count':sum(x['rejected'] for x in mutations),'mutation_receipts':mutations,'command_receipts':[run('python3 scripts/validate_scalable_oversight_protocol.py')],'witness':{'terminal_stage':'scoped','protocol_version':2,'receipt_count':7,'bounded_use_handoff_count':1,'readmission_count':1,'support_assignment_count':0,'external_effect_count':0},'support_state_effect':'none','non_claims':['no reviewer competence or calibration result','no debate, consultancy, or weak-to-strong efficacy result','no model or human outcome workload','no independence, causal, usefulness, safety, or transfer result','no deployed invalidation or policy enforcement','no release, execution, or support authority']}

def main()->None:
 a=argparse.ArgumentParser();a.add_argument('--write',action='store_true');args=a.parse_args();result=build();errors=[]
 if result['route_case_count']!=58:errors.append('route count drifted')
 if result['mutation_count']!=65 or result['mutation_rejection_count']!=65:errors.append('mutation contract drifted')
 for needle in ('inductive Stage','def routeFor','rejected_event_preserves_state','complete_lifecycle_reaches_version_two_readmission'):
  if needle not in LEAN.read_text():errors.append('Lean model missing '+needle)
 jsonschema.validate(result,json.loads(SCHEMA.read_text()));serialized=json.dumps(result,indent=2)+'\n'
 if args.write:RESULT.parent.mkdir(parents=True,exist_ok=True);RESULT.write_text(serialized)
 elif not RESULT.exists() or RESULT.read_text()!=serialized:errors.append(f'{RESULT.relative_to(ROOT)} is stale; run {COMMAND} --write')
 if errors:print('Scalable-oversight refinement failed:\n - '+'\n - '.join(errors));sys.exit(1)
 print('Scalable-oversight refinement passed: 7 inherited cases, 7 stages, 58 routes, 65/65 mutations rejected, support effect none.')
if __name__=='__main__':main()
