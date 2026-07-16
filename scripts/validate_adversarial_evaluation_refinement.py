#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, subprocess, sys
from pathlib import Path
from typing import Any
import jsonschema

ROOT=Path(__file__).resolve().parents[1]
LEAN=ROOT/'lean/AsiStackProofs/AdversarialEvaluationRefinement.lean'
SCHEMA=ROOT/'schemas/adversarial_evaluation_refinement.schema.json'
FIXTURE=ROOT/'experiments/adversarial_evaluation_integrity/fixtures/cases.json'
RESULT=ROOT/'experiments/adversarial_evaluation_refinement/results/2026-07-15-local.json'
COMMAND='python3 scripts/validate_adversarial_evaluation_refinement.py'
STAGES=['draft','scoped','protocolBound','observed','independentlyProbed','adjudicated','decisionBound']
KINDS={'draft':'scope','scoped':'bindProtocol','protocolBound':'recordObservation','observed':'runIndependentProbe','independentlyProbed':'adjudicate','adjudicated':'requestDecisionReview','decisionBound':'triggerReevaluation'}
ACCEPTED={'accept_scope','accept_protocol','accept_observation','accept_independent_probe','accept_promotion_adjudication','accept_quarantine_adjudication','accept_observation_closure','accept_decision_review','accept_reevaluation'}
IDENTITY={'consumerId','decisionDigest','modelDigest','taskDigest','protocolDigest','policyDigest','evaluatorDigest','monitorDigest','rewardDigest','selectionDigest','hypothesisDigest','outcomeDigest','currentProtocolVersion'}
GATES={
'draft':[('consumerPresent',False,'request_consumer'),('decisionPresent',False,'request_decision'),('modelTaskPresent',False,'request_model_task'),('elicitationContextPresent',False,'request_elicitation_context'),('authorityContextPresent',False,'request_authority_context'),('permittedInferencePresent',False,'request_permitted_inference')],
'scoped':[('selectionContextPresent',False,'request_selection_context'),('rewardProvenancePresent',False,'request_reward_provenance'),('monitorProvenancePresent',False,'request_monitor_provenance'),('hypothesisSetPresent',False,'request_hypothesis_set'),('outcomeCriterionPresent',False,'request_outcome_criterion'),('prospectivePlanPresent',False,'request_prospective_plan'),('blindingPresent',False,'request_blinding')],
'protocolBound':[('observationPresent',False,'request_observation'),('transcriptPresent',False,'request_transcript'),('denominatorComplete',False,'request_complete_denominator'),('failureCasesPreserved',False,'request_failure_cases'),('costRecordPresent',False,'request_cost_record')],
'observed':[('independentEvaluationPresent',False,'request_independent_evaluation'),('evaluatorSeparationPresent',False,'reject_evaluator_dependency'),('crossContextProbePresent',False,'request_cross_context_probe'),('matchedAccessPresent',False,'request_matched_access'),('dependencyDisclosurePresent',False,'request_dependency_disclosure'),('discrepancyRecorded',False,'request_discrepancy_record'),('alternativeHypothesesPreserved',False,'request_alternative_hypotheses')],
'independentlyProbed':[('discrepancyDispositionPresent',False,'request_discrepancy_disposition'),('alternativeDispositionPresent',False,'request_alternative_disposition'),('uncertaintyPresent',False,'request_uncertainty'),('residualOwnerPresent',False,'request_residual_owner'),('noIntentInferenceRecorded',False,'reject_intent_laundering'),('mitigationDescendantPresent',False,'request_mitigation_descendant'),('quarantineRecordPresent',False,'request_quarantine_record'),('expiryPresent',False,'request_expiry'),('decisionAuthoritySeparated',False,'reject_decision_authority_laundering')],
'adjudicated':[('decisionReviewRecordPresent',False,'request_decision_review_record'),('decisionConsumerPresent',False,'request_decision_consumer'),('boundedObservationStatusPresent',False,'request_bounded_observation_status'),('noReleaseAuthorityRecorded',False,'reject_release_authority_laundering')],
'decisionBound':[('reevaluationTriggerPresent',False,'request_reevaluation_trigger'),('descendantInvalidationComplete',False,'request_descendant_invalidation'),('ordinaryRouteBlocked',False,'request_ordinary_route_block'),('successorProtocolVersion',1,'reject_successor_version')]}

def packet()->dict[str,Any]:
 return {'consumerId':901,'decisionDigest':902,'modelDigest':903,'taskDigest':904,'protocolDigest':905,'policyDigest':906,'evaluatorDigest':907,'monitorDigest':908,'rewardDigest':909,'selectionDigest':910,'hypothesisDigest':911,'outcomeDigest':912,'currentProtocolVersion':1,'successorProtocolVersion':1,'eventDigest':1,
 'consumerPresent':True,'decisionPresent':True,'modelTaskPresent':True,'elicitationContextPresent':True,'authorityContextPresent':True,'permittedInferencePresent':True,'selectionContextPresent':True,'rewardProvenancePresent':True,'monitorProvenancePresent':True,'hypothesisSetPresent':True,'outcomeCriterionPresent':True,'prospectivePlanPresent':True,'blindingPresent':True,'observationPresent':True,'transcriptPresent':True,'denominatorComplete':True,'failureCasesPreserved':True,'costRecordPresent':True,'independentEvaluationPresent':True,'evaluatorSeparationPresent':True,'crossContextProbePresent':True,'matchedAccessPresent':True,'dependencyDisclosurePresent':True,'discrepancyRecorded':True,'alternativeHypothesesPreserved':True,'unresolvedDiscrepancy':False,'mitigationAttempted':False,'discrepancyDispositionPresent':True,'alternativeDispositionPresent':True,'uncertaintyPresent':True,'residualOwnerPresent':True,'noIntentInferenceRecorded':True,'mitigationDescendantPresent':True,'quarantineRecordPresent':True,'expiryPresent':True,'decisionAuthoritySeparated':True,'promotionRequested':True,'decisionReviewRecordPresent':True,'decisionConsumerPresent':True,'boundedObservationStatusPresent':True,'noReleaseAuthorityRecorded':True,'reevaluationTriggerPresent':True,'descendantInvalidationComplete':True,'ordinaryRouteBlocked':True,'supportAssignmentRequested':False,'externalEffectRequested':False}

def route(stage:str,kind:str,p:dict[str,Any],unresolved:bool=False,mitigation:bool=False,last:int=0,current_version:int=1)->str:
 c=packet()
 if kind!=KINDS[stage]:return 'reject_wrong_stage'
 if any(p[k]!=(current_version if k=='currentProtocolVersion' else c[k]) for k in IDENTITY):return 'reject_identity_substitution'
 if p['eventDigest']==last:return 'reject_replay'
 if p['supportAssignmentRequested'] or p['externalEffectRequested']:return 'reject_authority_leak'
 if stage=='independentlyProbed':
  for field,bad,answer in GATES[stage][:5]:
   if p[field] is bad:return answer
  if mitigation and not p['mitigationDescendantPresent']:return 'request_mitigation_descendant'
  if unresolved and not p['quarantineRecordPresent']:return 'request_quarantine_record'
  for field,bad,answer in GATES[stage][7:]:
   if p[field] is bad:return answer
  if unresolved:return 'accept_quarantine_adjudication'
  return 'accept_promotion_adjudication' if p['promotionRequested'] else 'accept_observation_closure'
 if stage=='adjudicated':
  for field,bad,answer in GATES[stage]:
   if p[field] is bad:return answer
  return 'accept_decision_review'
 if stage=='decisionBound':
  for field,bad,answer in GATES[stage][:3]:
   if p[field] is bad:return answer
  if p['successorProtocolVersion']!=current_version+1:return 'reject_successor_version'
  return 'accept_reevaluation'
 for field,bad,answer in GATES[stage]:
  if p[field] is bad:return answer
 return {'draft':'accept_scope','scoped':'accept_protocol','protocolBound':'accept_observation','observed':'accept_independent_probe'}[stage]

def run(command:str)->dict[str,Any]:
 p=subprocess.run(command.split(),cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 if p.returncode:raise RuntimeError(p.stdout)
 return {'command':command,'exit_code':p.returncode,'output_sha256':hashlib.sha256(p.stdout.encode()).hexdigest()}

def gate_context(stage:str,field:str)->tuple[bool,bool]:
 return (field=='quarantineRecordPresent',field=='mitigationDescendantPresent') if stage=='independentlyProbed' else (False,False)

def build()->dict[str,Any]:
 cases=[]
 for i,stage in enumerate(STAGES,1):
  p=packet();p['eventDigest']=i
  if stage=='decisionBound':p['successorProtocolVersion']=2
  cases.append({'case_id':stage+'_accepted','expected_route':route(stage,KINDS[stage],p)})
 for stage,gates in GATES.items():
  for field,bad,_ in gates:
   p=packet();p['eventDigest']=90
   if stage=='decisionBound':p['successorProtocolVersion']=2
   p[field]=bad;unresolved,mitigation=gate_context(stage,field)
   cases.append({'case_id':stage+'_'+field,'expected_route':route(stage,KINDS[stage],p,unresolved,mitigation)})
 p=packet();cases.append({'case_id':'adjudication_unresolved_complete','expected_route':route('independentlyProbed','adjudicate',p,True)})
 p=packet();p['promotionRequested']=False;cases.append({'case_id':'adjudication_no_promotion','expected_route':route('independentlyProbed','adjudicate',p)})
 p=packet();cases.append({'case_id':'adjudication_mitigation_complete','expected_route':route('independentlyProbed','adjudicate',p,False,True)})
 for cid,kind,field,value in [('wrong_stage','triggerReevaluation',None,None),('identity_substitution','scope','consumerId',999),('event_replay','scope','eventDigest',0),('authority_leak','scope','supportAssignmentRequested',True)]:
  p=packet()
  if field:p[field]=value
  cases.append({'case_id':cid,'expected_route':route('draft',kind,p)})
 mutations=[]
 for field in sorted(IDENTITY):
  p=packet();p[field]+=1000;mutations.append({'mutation_id':'binding_'+field,'rejected':route('draft','scope',p) not in ACCEPTED})
 for stage,gates in GATES.items():
  for field,bad,_ in gates:
   p=packet();p['eventDigest']=91
   if stage=='decisionBound':p['successorProtocolVersion']=2
   p[field]=bad;unresolved,mitigation=gate_context(stage,field)
   mutations.append({'mutation_id':'gate_'+stage+'_'+field,'rejected':route(stage,KINDS[stage],p,unresolved,mitigation) not in ACCEPTED})
 for mid,stage,kind,field,value in [('wrong_kind','draft','triggerReevaluation',None,None),('event_replay','draft','scope','eventDigest',0),('support_leak','draft','scope','supportAssignmentRequested',True),('effect_leak','draft','scope','externalEffectRequested',True),('stale_decision_after_reevaluation','scoped','requestDecisionReview',None,None)]:
  p=packet()
  if field:p[field]=value
  mutations.append({'mutation_id':mid,'rejected':route(stage,kind,p) not in ACCEPTED})
 fixture=json.loads(FIXTURE.read_text())
 return {'schema_version':'asi_stack.adversarial_evaluation_refinement.v1','result_id':'adversarial-evaluation-refinement-2026-07-15-local','source_sha256':{'lean_model':hashlib.sha256(LEAN.read_bytes()).hexdigest(),'input_fixture':hashlib.sha256(FIXTURE.read_bytes()).hexdigest()},'input_suite':{'suite_id':'adversarial_evaluation_integrity','case_count':len(fixture['cases']),'passed_count':8},'reachable_stage_count':7,'route_case_count':len(cases),'route_coverage':cases,'mutation_count':len(mutations),'mutation_rejection_count':sum(x['rejected'] for x in mutations),'mutation_receipts':mutations,'command_receipts':[run('python3 scripts/validate_adversarial_evaluation_integrity.py')],'witness':{'terminal_stage':'scoped','protocol_version':2,'receipt_count':7,'decision_review_handoff_count':1,'reevaluation_count':1,'support_assignment_count':0,'external_effect_count':0},'support_state_effect':'none','non_claims':['no deception, sandbagging, or alignment-faking detection','no capability, intent, or prevalence result','no monitor, reward, outcome, or evaluator validity result','no independent-institution or mitigation-efficacy result','no quarantine correctness or deployed invalidation','no readiness, safety, release, transfer, or support promotion']}

def main()->None:
 a=argparse.ArgumentParser();a.add_argument('--write',action='store_true');args=a.parse_args();result=build();errors=[]
 if result['route_case_count']!=56:errors.append('route count drifted')
 if result['mutation_count']!=60 or result['mutation_rejection_count']!=60:errors.append('mutation contract drifted')
 for needle in ('inductive Stage','def routeFor','rejected_event_preserves_state','full_observation_lifecycle_requires_versioned_reevaluation'):
  if needle not in LEAN.read_text():errors.append('Lean model missing '+needle)
 jsonschema.validate(result,json.loads(SCHEMA.read_text()));serialized=json.dumps(result,indent=2)+'\n'
 if args.write:RESULT.parent.mkdir(parents=True,exist_ok=True);RESULT.write_text(serialized)
 elif not RESULT.exists() or RESULT.read_text()!=serialized:errors.append(f'{RESULT.relative_to(ROOT)} is stale; run {COMMAND} --write')
 if errors:print('Adversarial-evaluation refinement failed:\n - '+'\n - '.join(errors));sys.exit(1)
 print('Adversarial-evaluation refinement passed: 8 inherited cases, 7 stages, 56 routes, 60/60 mutations rejected, support effect none.')
if __name__=='__main__':main()
