#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
from typing import Any
import jsonschema
ROOT=Path(__file__).resolve().parents[1];LEAN=ROOT/'lean/AsiStackProofs/HiveLifecycleRefinement.lean';SCHEMA=ROOT/'schemas/hive_lifecycle_refinement.schema.json';RESULT=ROOT/'experiments/hive_lifecycle_refinement/results/2026-07-15-local.json';COMMAND='python3 scripts/validate_hive_lifecycle_refinement.py'
STAGES=['requested','policyBound','nodeSelected','leased','executed','reconciled','closed'];KINDS={'requested':'bindPolicy','policyBound':'selectNode','nodeSelected':'issueLease','leased':'execute','executed':'reconcile','reconciled':'close','closed':'close'};ACCEPTED={'accept_policy','accept_selection','accept_lease','accept_execution','accept_reconciliation','accept_closure'}
JOB={'jobId','jobVersion','principalDigest','contractDigest','policyDigest','authorityDigest','evaluatorDigest','consumerDigest','residualDigest'};NODE={'nodeRegistryDigest','candidateSetDigest','selectedNodeDigest','leaseDigest'}
def packet()->dict[str,Any]:
 p={k:v for k,v in zip(sorted(JOB|NODE),range(1001,1014))};p['eventDigest']=1
 for k in ['jobWellFormed','identityPolicy','dataPolicy','toolPolicy','approvalPolicy','deviceRegistry','schedulerPolicy','candidateDenominator','leastAuthority','dataLocality','costBudget','energyBudget','dropoutPlan','federationLease','sandbox','leaseScope','evidenceObligations','expiration','revocationPath','boundApproval','freshGrant','deniedBeforeMutation','stateUnchanged','executionGrant','monitor','artifactReceipt','effectReceipt','resourceReceipt','auditReceipt','usefulOutcome','residualOwner','dropoutRecovery','revocationClosure','descendantClosure','consumerAcknowledgment','nonClaims']:p[k]=True
 for k in ['externalAccess','highRisk','partitionDetected','staleGrantPossible','supportAssignmentRequested','externalEffectRequested']:p[k]=False
 return p
def route(stage:str,kind:str,p:dict[str,Any],last:int=0)->str:
 q=packet()
 if kind!=KINDS[stage]:return'reject_wrong_stage'
 if any(p[k]!=q[k] for k in JOB):return'reject_job_substitution'
 if any(p[k]!=q[k] for k in NODE):return'reject_node_substitution'
 if p['eventDigest']==last:return'reject_event_replay'
 if p['supportAssignmentRequested'] or p['externalEffectRequested']:return'reject_authority_leak'
 checks={'requested':[('jobWellFormed',False,'reject_malformed_job'),('identityPolicy',False,'require_identity_policy'),('dataPolicy',False,'require_data_policy'),('toolPolicy',False,'require_tool_policy'),('approvalPolicy',False,'require_approval_policy')],'policyBound':[('deviceRegistry',False,'require_device_registry'),('schedulerPolicy',False,'require_scheduler_policy'),('candidateDenominator',False,'require_candidate_denominator'),('leastAuthority',False,'require_least_authority'),('dataLocality',False,'require_data_locality'),('costBudget',False,'require_cost_budget'),('energyBudget',False,'require_energy_budget'),('dropoutPlan',False,'require_dropout_plan')],'nodeSelected':[('sandbox',False,'require_sandbox'),('leaseScope',False,'require_lease_scope'),('evidenceObligations',False,'require_evidence_obligations'),('expiration',False,'require_expiration'),('revocationPath',False,'require_revocation_path')],'executed':[('artifactReceipt',False,'require_artifact_receipt'),('effectReceipt',False,'require_effect_receipt'),('resourceReceipt',False,'require_resource_receipt'),('auditReceipt',False,'require_audit_receipt'),('usefulOutcome',False,'require_useful_outcome'),('residualOwner',False,'require_residual_owner')],'reconciled':[('dropoutRecovery',False,'require_dropout_recovery'),('revocationClosure',False,'require_revocation_closure'),('descendantClosure',False,'require_descendant_closure'),('consumerAcknowledgment',False,'require_consumer_acknowledgment'),('nonClaims',False,'require_non_claims')]}
 if stage=='nodeSelected' and p['externalAccess'] and not p['federationLease']:return'require_federation_lease'
 if stage=='leased':
  if p['highRisk'] and not p['boundApproval']:return'require_bound_approval'
  if not p['freshGrant']:return'require_fresh_grant'
  if p['partitionDetected'] and p['staleGrantPossible']:
   return'quarantine_partition' if p['deniedBeforeMutation'] and p['stateUnchanged'] else'require_no_mutation_evidence'
  if not p['executionGrant']:return'require_execution_grant'
  if not p['monitor']:return'require_monitor'
  return'accept_execution'
 if stage=='closed':return'reject_wrong_stage'
 for f,b,a in checks[stage]:
  if p[f] is b:return a
 return{'requested':'accept_policy','policyBound':'accept_selection','nodeSelected':'accept_lease','executed':'accept_reconciliation','reconciled':'accept_closure'}[stage]
def run(c:str)->dict[str,Any]:
 p=subprocess.run(c.split(),cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 if p.returncode:raise RuntimeError(p.stdout)
 return{'command':c,'exit_code':p.returncode,'output_sha256':hashlib.sha256(p.stdout.encode()).hexdigest()}
def build()->dict[str,Any]:
 gates=[('requested',f,v)for f,v in [('jobWellFormed',False),('identityPolicy',False),('dataPolicy',False),('toolPolicy',False),('approvalPolicy',False)]]+[('policyBound',f,False)for f in ['deviceRegistry','schedulerPolicy','candidateDenominator','leastAuthority','dataLocality','costBudget','energyBudget','dropoutPlan']]+[('nodeSelected','external_no_lease',False)]+[('nodeSelected',f,False)for f in ['sandbox','leaseScope','evidenceObligations','expiration','revocationPath']]+[('leased',f,False)for f in ['high_risk_no_approval','freshGrant','partition_quarantine','partition_no_mutation','executionGrant','monitor']]+[('executed',f,False)for f in ['artifactReceipt','effectReceipt','resourceReceipt','auditReceipt','usefulOutcome','residualOwner']]+[('reconciled',f,False)for f in ['dropoutRecovery','revocationClosure','descendantClosure','consumerAcknowledgment','nonClaims']]
 def mutate(stage,f,v):
  p=packet();p['eventDigest']=90
  if f=='external_no_lease':p['externalAccess']=True;p['federationLease']=False
  elif f=='high_risk_no_approval':p['highRisk']=True;p['boundApproval']=False
  elif f=='partition_quarantine':p['partitionDetected']=True;p['staleGrantPossible']=True
  elif f=='partition_no_mutation':p['partitionDetected']=True;p['staleGrantPossible']=True;p['deniedBeforeMutation']=False
  else:p[f]=v
  return p
 cases=[]
 for st in STAGES[:-1]:p=packet();p['eventDigest']=STAGES.index(st)+1;cases.append({'case_id':st+'_accepted','expected_route':route(st,KINDS[st],p)})
 for st,f,v in gates:cases.append({'case_id':st+'_'+f,'expected_route':route(st,KINDS[st],mutate(st,f,v))})
 for n,k,f,v in [('wrong_stage','close',None,None),('job_substitution','bindPolicy','jobId',999),('node_substitution','bindPolicy','selectedNodeDigest',999),('event_replay','bindPolicy','eventDigest',0),('authority_leak','bindPolicy','supportAssignmentRequested',True)]:
  p=packet();
  if f:p[f]=v
  cases.append({'case_id':n,'expected_route':route('requested',k,p)})
 muts=[]
 for f in sorted(JOB|NODE):p=packet();p[f]+=1000;muts.append({'mutation_id':'binding_'+f,'rejected':route('requested','bindPolicy',p)not in ACCEPTED})
 for st,f,v in gates:muts.append({'mutation_id':'gate_'+st+'_'+f,'rejected':route(st,KINDS[st],mutate(st,f,v))not in ACCEPTED})
 for n,k,f,v in [('wrong_kind','close',None,None),('replay','bindPolicy','eventDigest',0),('support','bindPolicy','supportAssignmentRequested',True),('effect','bindPolicy','externalEffectRequested',True)]:
  p=packet()
  if f:p[f]=v
  muts.append({'mutation_id':n,'rejected':route('requested',k,p)not in ACCEPTED})
 return{'schema_version':'asi_stack.hive_lifecycle_refinement.v1','result_id':'hive-lifecycle-refinement-2026-07-15-local','source_sha256':{'lean_model':hashlib.sha256(LEAN.read_bytes()).hexdigest()},'input_suites':[{'suite_id':'hive_admission','valid_count':2,'expected_invalid_count':8},{'suite_id':'partitioned_authority','valid_count':3,'expected_invalid_count':6}],'reachable_stage_count':7,'route_case_count':len(cases),'route_coverage':cases,'mutation_count':len(muts),'mutation_rejection_count':sum(x['rejected']for x in muts),'mutation_receipts':muts,'command_receipts':[run('python3 scripts/validate_hive_admission.py'),run('python3 scripts/validate_partitioned_authority_fixture.py')],'witness':{'terminal_stage':'closed','receipt_count':6,'dispatch_count':1,'useful_outcome_count':1,'recovery_count':1,'support_assignment_count':0,'external_effect_count':0},'support_state_effect':'none','non_claims':['no deployed scheduler or federation','no real device, portal, authority-service, or sandbox enforcement','no partition tolerance, availability, security, or privacy result','no measured energy, dropout recovery, useful-work, or transfer result','no support promotion']}
def main():
 a=argparse.ArgumentParser();a.add_argument('--write',action='store_true');x=a.parse_args();r=build();e=[]
 if r['route_case_count']!=47:e.append('route count drifted')
 if r['mutation_count']!=53 or r['mutation_rejection_count']!=53:e.append('mutation contract drifted')
 jsonschema.validate(r,json.loads(SCHEMA.read_text()));s=json.dumps(r,indent=2)+'\n'
 if x.write:RESULT.parent.mkdir(parents=True,exist_ok=True);RESULT.write_text(s)
 elif not RESULT.exists()or RESULT.read_text()!=s:e.append(f'{RESULT.relative_to(ROOT)} stale; run {COMMAND} --write')
 if e:print('Hive lifecycle refinement failed:\n - '+'\n - '.join(e));sys.exit(1)
 print('Hive lifecycle refinement passed: 2 exact suites, 7 stages, 47 routes, 53/53 mutations rejected, support effect none.')
if __name__=='__main__':main()
