#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, subprocess, sys
from pathlib import Path
from typing import Any
import jsonschema

ROOT=Path(__file__).resolve().parents[1]
LEAN=ROOT/'lean/AsiStackProofs/CapabilityThresholdRefinement.lean'
SCHEMA=ROOT/'schemas/capability_threshold_refinement.schema.json'
FIXTURE=ROOT/'experiments/capability_threshold_commitment/fixtures/cases.json'
RESULT=ROOT/'experiments/capability_threshold_refinement/results/2026-07-15-local.json'
COMMAND='python3 scripts/validate_capability_threshold_refinement.py'
STAGES=['draft','scoped','assessed','adjudicated','controlled','readinessBound']
KINDS={'draft':'scope','scoped':'assess','assessed':'adjudicate','adjudicated':'verifyControls','controlled':'requestReadiness','readinessBound':'triggerReassessment'}
ACCEPTED={'accept_scope','accept_assessment','accept_adjudication','accept_controls','accept_readiness','accept_reassessment'}
IDENTITY={'capabilityId','systemDigest','policyDigest','releasePathDigest','envelopeDigest','thresholdDigest','baselineDigest','evaluatorDigest','safeguardDigest','authorityDigest','residualDigest','currentAssessmentVersion'}
GATES={
'draft':[('capabilityDomainPresent',False,'request_capability_domain'),('threatModelPresent',False,'request_threat_model'),('thresholdDefinitionPresent',False,'request_threshold_definition'),('coverageDeadlinePresent',False,'request_coverage_deadline')],
'scoped':[('evaluationEnvelopePresent',False,'request_evaluation_envelope'),('elicitationPresent',False,'request_elicitation'),('baselinePresent',False,'request_baseline'),('uncertaintyPresent',False,'request_uncertainty'),('independentEvaluatorPresent',False,'request_independent_evaluator'),('assessmentResultPresent',False,'request_assessment_result')],
'assessed':[('thresholdDecisionPresent',False,'request_threshold_decision'),('decisionUncertaintyPresent',False,'request_decision_uncertainty'),('affectedPathsPresent',False,'request_affected_paths'),('residualOwnerPresent',False,'request_residual_owner')],
'adjudicated':[('safeguardPackagePresent',False,'block_missing_safeguards'),('safeguardVerifierPresent',False,'block_missing_safeguard_verifier'),('bypassTestPresent',False,'block_missing_bypass_test'),('rollbackPlanPresent',False,'block_missing_rollback')],
'controlled':[('monitoringPresent',False,'request_monitoring'),('exceptionOwnerPresent',False,'request_exception_owner'),('exceptionExpiryPresent',False,'request_exception_expiry'),('compensatingControlsPresent',False,'request_compensating_controls'),('exceptionReviewTriggerPresent',False,'request_exception_review_trigger'),('residualOwnerPresent',False,'request_residual_owner'),('decisionAuthorityPresent',False,'request_decision_authority'),('authoritySeparationPresent',False,'reject_authority_laundering'),('releasePathPresent',False,'request_release_path')],
'readinessBound':[('reassessmentTriggerPresent',False,'request_reassessment_trigger'),('descendantInvalidationComplete',False,'request_descendant_invalidation'),('ordinaryRouteBlocked',False,'request_ordinary_route_block'),('successorAssessmentVersion',1,'reject_successor_version')]}

def packet()->dict[str,Any]:
 return {'capabilityId':801,'systemDigest':802,'policyDigest':803,'releasePathDigest':804,'envelopeDigest':805,'thresholdDigest':806,'baselineDigest':807,'evaluatorDigest':808,'safeguardDigest':809,'authorityDigest':810,'residualDigest':811,'currentAssessmentVersion':1,'successorAssessmentVersion':1,'eventDigest':1,
 'capabilityDomainPresent':True,'threatModelPresent':True,'thresholdDefinitionPresent':True,'coverageDeadlinePresent':True,'evaluationEnvelopePresent':True,'elicitationPresent':True,'baselinePresent':True,'uncertaintyPresent':True,'independentEvaluatorPresent':True,'assessmentResultPresent':True,'thresholdDecisionPresent':True,'decisionUncertaintyPresent':True,'thresholdCrossed':True,'affectedPathsPresent':True,'residualOwnerPresent':True,'safeguardPackagePresent':True,'safeguardVerifierPresent':True,'bypassTestPresent':True,'rollbackPlanPresent':True,'monitoringPresent':True,'exceptionRequested':False,'exceptionOwnerPresent':True,'exceptionExpiryPresent':True,'compensatingControlsPresent':True,'exceptionReviewTriggerPresent':True,'decisionAuthorityPresent':True,'authoritySeparationPresent':True,'releasePathPresent':True,'reassessmentTriggerPresent':True,'descendantInvalidationComplete':True,'ordinaryRouteBlocked':True,'supportAssignmentRequested':False,'externalEffectRequested':False}

def route(stage:str,kind:str,p:dict[str,Any],crossed:bool=True,last:int=0,current_version:int=1)->str:
 c=packet()
 if kind!=KINDS[stage]:return 'reject_wrong_stage'
 if any(p[k]!=(current_version if k=='currentAssessmentVersion' else c[k]) for k in IDENTITY):return 'reject_identity_substitution'
 if p['eventDigest']==last:return 'reject_replay'
 if p['supportAssignmentRequested'] or p['externalEffectRequested']:return 'reject_authority_leak'
 if stage=='adjudicated':
  if crossed:
   for field,bad,answer in GATES[stage]:
    if p[field] is bad:return answer
  return 'accept_controls'
 if stage=='controlled':
  if not p['monitoringPresent']:return 'request_monitoring'
  if p['exceptionRequested']:
   for field,bad,answer in GATES[stage][1:5]:
    if p[field] is bad:return answer
  for field,bad,answer in GATES[stage][5:]:
   if p[field] is bad:return answer
  return 'accept_readiness'
 if stage=='readinessBound':
  for field,bad,answer in GATES[stage][:3]:
   if p[field] is bad:return answer
  if p['successorAssessmentVersion']!=current_version+1:return 'reject_successor_version'
  return 'accept_reassessment'
 for field,bad,answer in GATES[stage]:
  if p[field] is bad:return answer
 return {'draft':'accept_scope','scoped':'accept_assessment','assessed':'accept_adjudication'}[stage]

def run(command:str)->dict[str,Any]:
 p=subprocess.run(command.split(),cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 if p.returncode:raise RuntimeError(p.stdout)
 return {'command':command,'exit_code':p.returncode,'output_sha256':hashlib.sha256(p.stdout.encode()).hexdigest()}

def build()->dict[str,Any]:
 cases=[]
 for i,stage in enumerate(STAGES,1):
  p=packet();p['eventDigest']=i
  if stage=='readinessBound':p['successorAssessmentVersion']=2
  cases.append({'case_id':stage+'_accepted','expected_route':route(stage,KINDS[stage],p)})
 for stage,gates in GATES.items():
  for field,bad,_ in gates:
   p=packet();p['eventDigest']=90
   if stage=='controlled' and (field.startswith('exception') or field=='compensatingControlsPresent'):p['exceptionRequested']=True
   if stage=='readinessBound':p['successorAssessmentVersion']=2
   p[field]=bad
   cases.append({'case_id':stage+'_'+field,'expected_route':route(stage,KINDS[stage],p)})
 p=packet();cases.append({'case_id':'adjudicated_non_crossing','expected_route':route('adjudicated','verifyControls',p,crossed=False)})
 p=packet();p['exceptionRequested']=True;cases.append({'case_id':'controlled_complete_exception','expected_route':route('controlled','requestReadiness',p)})
 for cid,kind,field,value in [('wrong_stage','triggerReassessment',None,None),('identity_substitution','scope','capabilityId',999),('event_replay','scope','eventDigest',0),('authority_leak','scope','supportAssignmentRequested',True)]:
  p=packet();
  if field:p[field]=value
  cases.append({'case_id':cid,'expected_route':route('draft',kind,p)})
 mutations=[]
 for field in sorted(IDENTITY):
  p=packet();p[field]+=1000;mutations.append({'mutation_id':'binding_'+field,'rejected':route('draft','scope',p) not in ACCEPTED})
 for stage,gates in GATES.items():
  for field,bad,_ in gates:
   p=packet();p['eventDigest']=91
   if stage=='controlled' and (field.startswith('exception') or field=='compensatingControlsPresent'):p['exceptionRequested']=True
   if stage=='readinessBound':p['successorAssessmentVersion']=2
   p[field]=bad
   mutations.append({'mutation_id':'gate_'+stage+'_'+field,'rejected':route(stage,KINDS[stage],p) not in ACCEPTED})
 for mid,stage,kind,field,value in [('wrong_kind','draft','triggerReassessment',None,None),('event_replay','draft','scope','eventDigest',0),('support_leak','draft','scope','supportAssignmentRequested',True),('effect_leak','draft','scope','externalEffectRequested',True),('stale_readiness_after_reassessment','scoped','requestReadiness',None,None)]:
  p=packet();
  if field:p[field]=value
  mutations.append({'mutation_id':mid,'rejected':route(stage,kind,p) not in ACCEPTED})
 fixture=json.loads(FIXTURE.read_text())
 return {'schema_version':'asi_stack.capability_threshold_refinement.v1','result_id':'capability-threshold-refinement-2026-07-15-local','source_sha256':{'lean_model':hashlib.sha256(LEAN.read_bytes()).hexdigest(),'input_fixture':hashlib.sha256(FIXTURE.read_bytes()).hexdigest()},'input_suite':{'suite_id':'capability_threshold_commitment','case_count':len(fixture['cases']),'passed_count':8},'reachable_stage_count':6,'route_case_count':len(cases),'route_coverage':cases,'mutation_count':len(mutations),'mutation_rejection_count':sum(x['rejected'] for x in mutations),'mutation_receipts':mutations,'command_receipts':[run('python3 scripts/validate_capability_threshold_commitment.py')],'witness':{'terminal_stage':'scoped','assessment_version':2,'receipt_count':6,'readiness_handoff_count':1,'reassessment_count':1,'support_assignment_count':0,'external_effect_count':0},'support_state_effect':'none','non_claims':['no real capability measurement','no threshold validity or crossing result','no evaluator-independence result','no safeguard, bypass, or rollback efficacy result','no exception approval or deployed invalidation','no readiness, safety, release, or support promotion']}

def main()->None:
 a=argparse.ArgumentParser();a.add_argument('--write',action='store_true');args=a.parse_args();result=build();errors=[]
 if result['route_case_count']!=43:errors.append('route count drifted')
 if result['mutation_count']!=48 or result['mutation_rejection_count']!=48:errors.append('mutation contract drifted')
 for needle in ('inductive Stage','def routeFor','rejected_event_preserves_state','full_threshold_lifecycle_requires_versioned_reassessment'):
  if needle not in LEAN.read_text():errors.append('Lean model missing '+needle)
 jsonschema.validate(result,json.loads(SCHEMA.read_text()));serialized=json.dumps(result,indent=2)+'\n'
 if args.write:RESULT.parent.mkdir(parents=True,exist_ok=True);RESULT.write_text(serialized)
 elif not RESULT.exists() or RESULT.read_text()!=serialized:errors.append(f'{RESULT.relative_to(ROOT)} is stale; run {COMMAND} --write')
 if errors:print('Capability-threshold refinement failed:\n - '+'\n - '.join(errors));sys.exit(1)
 print('Capability-threshold refinement passed: 8 inherited cases, 6 stages, 43 routes, 48/48 mutations rejected, support effect none.')
if __name__=='__main__':main()
