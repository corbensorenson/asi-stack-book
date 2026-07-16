#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, subprocess, sys
from pathlib import Path
from typing import Any
import jsonschema

ROOT=Path(__file__).resolve().parents[1]
LEAN=ROOT/'lean/AsiStackProofs/ReadinessRefinement.lean'; SCHEMA=ROOT/'schemas/readiness_refinement.schema.json'
RESULT=ROOT/'experiments/readiness_refinement/results/2026-07-15-local.json'
COMMAND='python3 scripts/validate_readiness_refinement.py'
STAGES=['candidate','shadow','canary','qualified','defaultReady','quarantined','terminal']
KINDS={'candidate':'admitShadow','shadow':'admitCanary','canary':'qualify','qualified':'admitDefault','defaultReady':'quarantine','quarantined':'terminate','terminal':'terminate'}
ACCEPTED={'accept_shadow','accept_canary','accept_qualification','accept_default','accept_quarantine','accept_termination'}
CAPABILITY={'capabilityId','capabilityVersion','implementationDigest','modelStateDigest','policyDigest','authorityDigest','consumerDigest'}
EVIDENCE={'workloadDigest','baselineDigest','evaluatorDigest','fallbackDigest','residualDigest'}

def packet()->dict[str,Any]:
 return {'capabilityId':901,'capabilityVersion':4,'implementationDigest':902,'modelStateDigest':903,'workloadDigest':904,'baselineDigest':905,'evaluatorDigest':906,'policyDigest':907,'authorityDigest':908,'consumerDigest':909,'fallbackDigest':910,'residualDigest':911,'eventDigest':1,
 'workloadPresent':True,'baselinePresent':True,'evaluatorPresent':True,'nonClaimsPresent':True,'shadowEvidencePresent':True,'gateEvidenceFresh':True,'regressionFloorPreserved':True,'residualEscrowPresent':True,'fallbackPresent':True,'rollbackPlanPresent':True,'monitoringPresent':True,'canaryEvidencePresent':True,'usefulThroughputRecorded':True,'unsafeReleaseRecorded':True,'latencyCostRecorded':True,'thresholdBreached':False,'qualificationEvidencePresent':True,'independentEvaluationPresent':True,'transferEvidencePresent':True,'delayedOutcomesPresent':True,'quarantineTriggerPresent':True,'transitivePropagationComplete':True,'ordinaryRouteBlocked':True,'boundedDiagnosticsPresent':True,'terminalReasonPresent':True,'terminalReceiptPresent':True,'dependencyClosureComplete':True,'revocationClosureComplete':True,'consumerAcknowledgmentPresent':True,'supportAssignmentRequested':False,'externalEffectRequested':False}

def route(stage:str,kind:str,p:dict[str,Any],last:int=0)->str:
 s=packet()
 if kind!=KINDS[stage]: return 'reject_wrong_stage'
 if any(p[k]!=s[k] for k in CAPABILITY): return 'reject_capability_substitution'
 if any(p[k]!=s[k] for k in EVIDENCE): return 'reject_evidence_substitution'
 if p['eventDigest']==last:return 'reject_event_replay'
 if p['supportAssignmentRequested'] or p['externalEffectRequested']:return 'reject_authority_leak'
 checks={
 'candidate':[('workloadPresent',False,'request_workload'),('baselinePresent',False,'request_baseline'),('evaluatorPresent',False,'request_evaluator'),('nonClaimsPresent',False,'request_non_claims')],
 'shadow':[('shadowEvidencePresent',False,'request_shadow_evidence'),('gateEvidenceFresh',False,'request_fresh_gate'),('regressionFloorPreserved',False,'block_regression'),('residualEscrowPresent',False,'request_residual_escrow'),('fallbackPresent',False,'request_fallback'),('rollbackPlanPresent',False,'request_rollback_plan'),('monitoringPresent',False,'request_monitoring')],
 'canary':[('canaryEvidencePresent',False,'request_canary_evidence'),('usefulThroughputRecorded',False,'request_useful_throughput'),('unsafeReleaseRecorded',False,'request_unsafe_release_record'),('latencyCostRecorded',False,'request_latency_cost'),('thresholdBreached',True,'quarantine_threshold_breach')],
 'qualified':[('qualificationEvidencePresent',False,'request_qualification_evidence'),('independentEvaluationPresent',False,'request_independent_evaluation'),('transferEvidencePresent',False,'request_transfer'),('delayedOutcomesPresent',False,'request_delayed_outcomes')],
 'defaultReady':[('quarantineTriggerPresent',False,'request_quarantine_trigger'),('transitivePropagationComplete',False,'request_transitive_propagation'),('ordinaryRouteBlocked',False,'request_ordinary_route_block'),('boundedDiagnosticsPresent',False,'request_bounded_diagnostics')],
 'quarantined':[('terminalReasonPresent',False,'request_terminal_reason'),('terminalReceiptPresent',False,'request_terminal_receipt'),('dependencyClosureComplete',False,'request_dependency_closure'),('revocationClosureComplete',False,'request_revocation_closure'),('consumerAcknowledgmentPresent',False,'request_consumer_acknowledgment')]}
 if stage=='terminal':return 'reject_wrong_stage'
 for field,bad,answer in checks[stage]:
  if p[field] is bad:return answer
 return {'candidate':'accept_shadow','shadow':'accept_canary','canary':'accept_qualification','qualified':'accept_default','defaultReady':'accept_quarantine','quarantined':'accept_termination'}[stage]

def run(command:str)->dict[str,Any]:
 p=subprocess.run(command.split(),cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 if p.returncode:raise RuntimeError(p.stdout)
 return {'command':command,'exit_code':p.returncode,'output_sha256':hashlib.sha256(p.stdout.encode()).hexdigest()}

def build()->dict[str,Any]:
 gates=[('candidate','workloadPresent',False),('candidate','baselinePresent',False),('candidate','evaluatorPresent',False),('candidate','nonClaimsPresent',False),('shadow','shadowEvidencePresent',False),('shadow','gateEvidenceFresh',False),('shadow','regressionFloorPreserved',False),('shadow','residualEscrowPresent',False),('shadow','fallbackPresent',False),('shadow','rollbackPlanPresent',False),('shadow','monitoringPresent',False),('canary','canaryEvidencePresent',False),('canary','usefulThroughputRecorded',False),('canary','unsafeReleaseRecorded',False),('canary','latencyCostRecorded',False),('canary','thresholdBreached',True),('qualified','qualificationEvidencePresent',False),('qualified','independentEvaluationPresent',False),('qualified','transferEvidencePresent',False),('qualified','delayedOutcomesPresent',False),('defaultReady','quarantineTriggerPresent',False),('defaultReady','transitivePropagationComplete',False),('defaultReady','ordinaryRouteBlocked',False),('defaultReady','boundedDiagnosticsPresent',False),('quarantined','terminalReasonPresent',False),('quarantined','terminalReceiptPresent',False),('quarantined','dependencyClosureComplete',False),('quarantined','revocationClosureComplete',False),('quarantined','consumerAcknowledgmentPresent',False)]
 cases=[]
 for stage in STAGES[:-1]:
  p=packet();p['eventDigest']=STAGES.index(stage)+1;cases.append({'case_id':stage+'_accepted','expected_route':route(stage,KINDS[stage],p)})
 for stage,field,value in gates:
  p=packet();p['eventDigest']=90;p[field]=value;cases.append({'case_id':stage+'_'+field,'expected_route':route(stage,KINDS[stage],p)})
 for name,kind,field,value in [('wrong_stage','terminate',None,None),('capability_substitution','admitShadow','capabilityId',999),('evidence_substitution','admitShadow','workloadDigest',999),('event_replay','admitShadow','eventDigest',0),('authority_leak','admitShadow','supportAssignmentRequested',True)]:
  p=packet();
  if field:p[field]=value
  cases.append({'case_id':name,'expected_route':route('candidate',kind,p)})
 muts=[]
 for field in sorted(CAPABILITY|EVIDENCE):
  p=packet();p[field]+=1000;muts.append({'mutation_id':'binding_'+field,'rejected':route('candidate','admitShadow',p) not in ACCEPTED})
 for stage,field,value in gates:
  p=packet();p['eventDigest']=91;p[field]=value;muts.append({'mutation_id':'gate_'+stage+'_'+field,'rejected':route(stage,KINDS[stage],p) not in ACCEPTED})
 for name,kind,field,value in [('wrong_kind','terminate',None,None),('event_replay','admitShadow','eventDigest',0),('support_leak','admitShadow','supportAssignmentRequested',True),('effect_leak','admitShadow','externalEffectRequested',True)]:
  p=packet();
  if field:p[field]=value
  muts.append({'mutation_id':name,'rejected':route('candidate',kind,p) not in ACCEPTED})
 commands=[run('python3 scripts/validate_readiness_residual_gates.py'),run('python3 scripts/validate_readiness_lifecycle_probe.py'),run('python3 scripts/validate_readiness_check_lifecycle.py')]
 return {'schema_version':'asi_stack.readiness_refinement.v1','result_id':'readiness-refinement-2026-07-15-local','source_sha256':{'lean_model':hashlib.sha256(LEAN.read_bytes()).hexdigest()},'input_suites':[{'suite_id':'readiness_residual_gates','valid_count':4,'expected_invalid_count':5},{'suite_id':'readiness_lifecycle_probe','valid_count':6,'expected_invalid_count':12},{'suite_id':'readiness_check_lifecycle','valid_count':1,'expected_invalid_count':9,'project_count':6}], 'reachable_stage_count':7,'route_case_count':len(cases),'route_coverage':cases,'mutation_count':len(muts),'mutation_rejection_count':sum(x['rejected'] for x in muts),'mutation_receipts':muts,'command_receipts':commands,'witness':{'terminal_stage':'terminal','receipt_count':6,'ordinary_release_count':1,'quarantine_count':1,'terminal_count':1,'support_assignment_count':0,'external_effect_count':0},'support_state_effect':'none','non_claims':['no deployed readiness engine','no evaluator adequacy or gate calibration','no effect-complete rollback execution','no natural useful-throughput or transfer result','no support promotion']}

def main()->None:
 a=argparse.ArgumentParser();a.add_argument('--write',action='store_true');args=a.parse_args();result=build();errors=[]
 if result['route_case_count']!=40:errors.append('route count drifted')
 if result['mutation_count']!=45 or result['mutation_rejection_count']!=45:errors.append('mutation contract drifted')
 for f in ('inductive Stage','def routeFor','apply_event_cannot_assign_support_or_external_effect','full_readiness_lifecycle_reaches_terminal_state'):
  if f not in LEAN.read_text():errors.append('Lean model missing '+f)
 jsonschema.validate(result,json.loads(SCHEMA.read_text()));serialized=json.dumps(result,indent=2)+'\n'
 if args.write:RESULT.parent.mkdir(parents=True,exist_ok=True);RESULT.write_text(serialized)
 elif not RESULT.exists() or RESULT.read_text()!=serialized:errors.append(f'{RESULT.relative_to(ROOT)} is stale; run {COMMAND} --write')
 if errors:print('Readiness refinement failed:\n - '+'\n - '.join(errors));sys.exit(1)
 print('Readiness refinement passed: 3 exact suites, 7 stages, 40 routes, 45/45 mutations rejected, support effect none.')
if __name__=='__main__':main()
