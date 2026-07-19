#!/usr/bin/env python3
"""Sequentially qualify one opened P2 replacement task without network setup."""

from __future__ import annotations

import __future__
import argparse
import gzip
import hashlib
import json
import shutil
import sys
import time
import types
import uuid
from datetime import datetime, timezone
from pathlib import Path

from run_p2_gold_preflight import execute_arm, load_selected_rows, run, run_monitored_container, sha256_file, sha256_text


ROOT=Path(__file__).resolve().parents[1]
SOURCE=Path('/tmp/swe-rebench-v2.parquet');HARNESS=Path('/tmp/swe-rebench-v2-code.7ixeFl')
SOURCE_SHA='0e0bf9355f892ad74ae98d4e1c404f39fd6654a8e351ee3e6ab162e4a64cd3ad';HARNESS_COMMIT='c71902a8cf8d2b725f63d51f199f4d3e56f68d2d'
OPENING=ROOT/'evidence_quality/p2_replacement_task_opening.json';PROVENANCE=ROOT/'evidence_quality/p2_replacement_provenance_preflight.json';CAL=ROOT/'evidence_quality/p2_independent_test_log_evaluator_calibration.json';RESOURCE=ROOT/'evidence_quality/p2_resource_ceiling.json'

def write_gzip(path:Path,text:str)->str:
 path.parent.mkdir(parents=True,exist_ok=True)
 with gzip.open(path,'wt',encoding='utf-8',compresslevel=9) as h:h.write(text)
 return hashlib.sha256(path.read_bytes()).hexdigest()

def dependency_command(spec:dict)->str:
 parser=spec['install_config']['log_parser'];repo=spec['repo'].split('/',1)[1]
 if parser=='parse_log_cargo':return 'cargo fetch --locked --offline'
 if parser=='parse_log_gotest':
  prefix='cd github && ' if spec['instance_id']=='google__go-github-3619' else ''
  return prefix+'GOPROXY=off go mod download && GOPROXY=off go mod verify'
 if parser=='parse_java_mvn':return './mvnw -o --no-transfer-progress -DskipTests dependency:go-offline && ./mvnw -o --no-transfer-progress -DskipTests test-compile'
 raise ValueError(f'unsupported parser {parser}')

def resource_gates(runrow:dict,ceilings:dict)->dict:
 monitor=runrow['resource_monitor'];duration=runrow['duration_seconds']
 return {
  'arm_wall_within_seconds':duration<=ceilings['arm_wall_seconds'],
  'monitor_sample_present_when_required':duration<3 or monitor['sample_count']>=1,
  'monitor_error_free':monitor.get('monitor_error_count',0)==0,
  'not_timed_out':not monitor['timed_out'],
  'peak_memory_within_bytes':monitor['peak_memory_bytes']<=ceilings['peak_memory_bytes'],
  'max_cpu_within_percent':monitor['max_cpu_percent']<=ceilings['max_cpu_percent'],
  'integrated_cpu_estimate_within_seconds':monitor['integrated_cpu_seconds_estimate']<=ceilings['integrated_cpu_seconds_estimate'],
  'peak_pids_within_count':monitor['peak_pids']<=ceilings['peak_pids'],
 }

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--instance-id',required=True);ap.add_argument('--attempt-id',required=True);args=ap.parse_args()
 attempt=ROOT/'experiments/p2_governed_repository_admission/replacement_qualification/attempts'/args.attempt_id
 if attempt.exists():raise SystemExit(f'immutable attempt exists: {attempt}')
 attempt.mkdir(parents=True)
 opening=json.loads(OPENING.read_text());provenance=json.loads(PROVENANCE.read_text());cal=json.loads(CAL.read_text());resource=json.loads(RESOURCE.read_text());ceilings=resource['task_acceptance_ceilings']
 selected=next((r for r in opening['candidates'] if r['instance_id']==args.instance_id),None)
 receipt=next((r for r in provenance['candidates'] if r['instance_id']==args.instance_id),None)
 if selected is None or receipt is None or selected['rank']!=1:raise SystemExit('instance is not an opened rank-one candidate')
 if cal['state']!='passed' or cal['exact_agreement_count']!=cal['total_case_count']:raise SystemExit('independent evaluator not calibrated')
 if sha256_file(SOURCE)!=SOURCE_SHA:raise SystemExit('source digest drift')
 if run('git','-C',str(HARNESS),'rev-parse','HEAD').stdout.strip()!=HARNESS_COMMIT:raise SystemExit('harness commit drift')
 spec=load_selected_rows(SOURCE,{args.instance_id})[args.instance_id]
 if sha256_text(spec['problem_statement'] or '')!=selected['problem_statement_sha256'] or sha256_text(spec['patch'] or '')!=selected['solution_patch_sha256'] or sha256_text(spec['test_patch'] or '')!=selected['test_patch_sha256']:raise SystemExit('opened task digest drift')
 sys.path.insert(0,str(HARNESS));sys.path.insert(0,str(HARNESS/'lib'));src=HARNESS/'lib/agent/log_parsers.py';upstream=types.ModuleType('p2_qualification_upstream');upstream.__file__=str(src);exec(compile(src.read_text(),str(src),'exec',flags=__future__.annotations.compiler_flag),upstream.__dict__)
 parser_fn=upstream.NAME_TO_PARSER[spec['install_config']['log_parser']]
 image=receipt['image_manifest']['image'];digest=receipt['image_manifest']['digest'];image_ref=image.split(':',1)[0]+'@'+digest
 host_before=shutil.disk_usage('/').free; result={"schema_version":"asi_stack.p2_replacement_task_qualification.v1","recorded_at_utc":datetime.now(timezone.utc).isoformat(),"attempt_id":args.attempt_id,"instance_id":args.instance_id,"slot":selected['slot'],"rank":1,"state":"running","source_parquet_sha256":SOURCE_SHA,"upstream_harness_commit":HARNESS_COMMIT,"independent_evaluator_sha256":cal['independent_evaluator_sha256'],"image_ref":image_ref,"manifest_digest":digest,"host_free_before_bytes":host_before,"runtime_network":"none","dependency_network":"none","repetitions_per_arm":2,"runs":[],"task_content_opened":True,"candidate_outcome_opened":False,"final_pool_selected":False,"final_pool_opened":False,"support_state_effect":"none","release_effect":"none"}
 def finish(state,code,detail):
  result.update({"state":state,"terminal_code":code,"terminal_detail":detail,"host_free_after_bytes":shutil.disk_usage('/').free,"host_free_byte_loss":max(0,host_before-shutil.disk_usage('/').free),"candidate_outcome_opened":bool(result['runs']),"all_runs_pass":len(result['runs'])==4 and all(r.get('pass') and r.get('dual_evaluator_exact_agreement') and r.get('resource_gate_pass') for r in result['runs']),"qualified_replacement":False})
  result['qualified_replacement']=result['all_runs_pass'] and state=='qualified'
  (attempt/'result.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n');print(f"{args.instance_id}: {state} {code}",flush=True)
 if host_before<ceilings['minimum_host_free_bytes_before_task']:finish('n0_resource_failure','host_free_below_minimum','pull not attempted');return
 pull_start=time.monotonic();pull=run('docker','pull','--platform','linux/amd64',image_ref,timeout=ceilings['image_pull_seconds']);pull_wall=time.monotonic()-pull_start;pull_text=(pull.stdout or '')+(pull.stderr or '');pull_path=attempt/'pull.log.gz';result['pull']={"exit_code":pull.returncode,"wall_seconds":round(pull_wall,6),"log_path":pull_path.relative_to(ROOT).as_posix(),"log_sha256":write_gzip(pull_path,pull_text)}
 if pull.returncode or pull_wall>ceilings['image_pull_seconds']:finish('n0_resource_failure','image_pull_failure_or_ceiling',pull_text[-1000:]);return
 inspect=run('docker','image','inspect',image_ref,'--format','{{json .}}');info=json.loads(inspect.stdout) if inspect.returncode==0 else {};result['image_inspect']={"exit_code":inspect.returncode,"size_bytes":info.get('Size'),"architecture":info.get('Architecture'),"os":info.get('Os'),"repo_digests":info.get('RepoDigests',[])}
 if inspect.returncode or info.get('Size',10**30)>ceilings['expanded_image_bytes'] or info.get('Architecture')!='amd64' or info.get('Os')!='linux':
  cleanup=run('docker','image','rm','-f',image_ref);result['cleanup']={"exit_code":cleanup.returncode,"output_sha256":sha256_text((cleanup.stdout or '')+(cleanup.stderr or ''))};finish('n0_resource_failure','image_inspect_or_size_gate_failure','image inspect/size/platform gate failed');return
 repo=spec['repo'].split('/',1)[1];setup_name=f"p2-deps-{uuid.uuid4().hex[:12]}";setup_cmd=dependency_command(spec);setup_args=['docker','run','--name',setup_name,'--network','none','--platform','linux/amd64','--cap-drop','ALL','--security-opt','no-new-privileges','--pids-limit','2048','--memory','8g','--cpus','6','--tmpfs','/tmp:rw,nosuid,nodev,exec,size=2g','-w',f'/{repo}',image_ref,'/bin/bash','-lc','set -e\ngit reset --hard HEAD\n'+setup_cmd]
 setup_start=time.monotonic();setup_proc,setup_monitor=run_monitored_container(setup_args,container_name=setup_name,timeout=ceilings['dependency_materialization_seconds']);setup_wall=time.monotonic()-setup_start;setup_text=(setup_proc.stdout or '')+(setup_proc.stderr or '');setup_log=attempt/'dependency_setup.log.gz';setup_cleanup=run('docker','rm','-f',setup_name)
 result['dependency_setup']={"command":setup_cmd,"network":"none","task_patch_applied":False,"exit_code":setup_proc.returncode,"wall_seconds":round(setup_wall,6),"resource_monitor":setup_monitor,"container_cleanup_exit_code":setup_cleanup.returncode,"log_path":setup_log.relative_to(ROOT).as_posix(),"log_sha256":write_gzip(setup_log,setup_text)}
 setup_gates={"exit_zero":setup_proc.returncode==0,"within_seconds":setup_wall<=ceilings['dependency_materialization_seconds'],"not_timed_out":not setup_monitor['timed_out'],"peak_memory_within_bytes":setup_monitor['peak_memory_bytes']<=ceilings['peak_memory_bytes'],"peak_pids_within_count":setup_monitor['peak_pids']<=ceilings['peak_pids']};result['dependency_setup']['gates']=setup_gates
 if not all(setup_gates.values()):
  cleanup=run('docker','image','rm','-f',image_ref);result['cleanup']={"exit_code":cleanup.returncode,"output_sha256":sha256_text((cleanup.stdout or '')+(cleanup.stderr or ''))};finish('n0_dependency_failure','offline_dependency_gate_failure','offline unpatched dependency setup failed');return
 try:
  for repetition in [1,2]:
   for arm,solution in [('baseline_test_patch_only',None),('human_gold_plus_test_patch',spec['patch'])]:
    row=execute_arm(spec=spec,image_ref=image_ref,parser=parser_fn,solution_patch=solution,test_patch=spec['test_patch'],arm=arm,repetition=repetition,timeout_seconds=ceilings['arm_wall_seconds'],write_logs=True,log_subdir=f"replacement_qualification/attempts/{args.attempt_id}/logs",independent_parser_name=spec['install_config']['log_parser'])
    row['resource_gates']=resource_gates(row,ceilings);row['resource_gate_pass']=all(row['resource_gates'].values());row['compressed_log_sha256']=sha256_file(ROOT/row['compressed_log_path']);result['runs'].append(row);(attempt/'checkpoint.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
 finally:
  cleanup=run('docker','image','rm','-f',image_ref);cleanup_text=(cleanup.stdout or '')+(cleanup.stderr or '');cleanup_log=attempt/'cleanup.log.gz';result['cleanup']={"exit_code":cleanup.returncode,"log_path":cleanup_log.relative_to(ROOT).as_posix(),"log_sha256":write_gzip(cleanup_log,cleanup_text)}
 all_pass=len(result['runs'])==4 and all(r['pass'] and r['dual_evaluator_exact_agreement'] and r['resource_gate_pass'] for r in result['runs']) and result['cleanup']['exit_code']==0
 finish('qualified' if all_pass else 'n0_construct_instrument_or_resource_failure','all_gates_passed' if all_pass else 'one_or_more_qualification_gates_failed','two paired repetitions completed')

if __name__=='__main__':main()
