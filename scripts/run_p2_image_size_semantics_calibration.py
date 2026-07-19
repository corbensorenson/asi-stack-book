#!/usr/bin/env python3
"""Calibrate compressed/content/virtual-size semantics before freezing P2 v2 ceilings."""

from __future__ import annotations

import json,math,re,shutil,subprocess,time
from datetime import datetime,timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PROV=ROOT/'evidence_quality/p2_replacement_provenance_preflight.json'
OUT=ROOT/'experiments/p2_governed_repository_admission/image_size_semantics_calibration/2026-07-17-rank-one-r1/result.json'
FORMULA='ceil_to_next_1GB(max_conservative_virtual_upper_bound_bytes * 1.25), minimum 6GB, maximum admissible 8GB'

def cmd(*args,timeout=300):return subprocess.run(args,capture_output=True,text=True,timeout=timeout)
def parse_upper(value:str)->int:
 m=re.fullmatch(r'([0-9]+(?:\.([0-9]+))?)([kMGT]?B)',value)
 if not m:raise ValueError(value)
 number=float(m.group(1));digits=len(m.group(2) or '')
 factor={'B':1,'kB':1000,'MB':1000**2,'GB':1000**3,'TB':1000**4}[m.group(3)]
 half=0 if digits==0 else 0.5*10**(-digits)
 return math.ceil((number+half)*factor)

def main():
 if OUT.exists():raise SystemExit('immutable result exists')
 prov=json.loads(PROV.read_text());OUT.parent.mkdir(parents=True)
 before=shutil.disk_usage('/').free;rows=[]
 for candidate in prov['candidates']:
  image=candidate['image_manifest']['image'];digest=candidate['image_manifest']['digest'];ref=image.split(':',1)[0]+'@'+digest;free_before=shutil.disk_usage('/').free
  start=time.monotonic();pull=cmd('docker','pull','--platform','linux/amd64',ref,timeout=300);wall=time.monotonic()-start
  inspect=cmd('docker','image','inspect',ref,'--format','{{json .}}',timeout=30);info=json.loads(inspect.stdout) if inspect.returncode==0 else {}
  df=cmd('docker','system','df','-v','--format','{{json .}}',timeout=30);dfdata=json.loads(df.stdout) if df.returncode==0 else {};images=dfdata.get('Images',[]);match=next((x for x in images if x.get('ID')==info.get('Id')),None)
  display=match.get('Size') if match else None;upper=parse_upper(display) if display else None
  history=cmd('docker','history','--no-trunc','--format','{{json .}}',info.get('Id','missing'),timeout=30);history_rows=[json.loads(x) for x in history.stdout.splitlines() if x.strip()] if history.returncode==0 else []
  cleanup=cmd('docker','image','rm','-f',ref,timeout=120);time.sleep(1);after=shutil.disk_usage('/').free
  rows.append({'slot':candidate['slot'],'instance_id':candidate['instance_id'],'manifest_digest':digest,'registry_compressed_layer_bytes':candidate['image_manifest']['compressed_layer_bytes'],'pull_exit_code':pull.returncode,'pull_wall_seconds':round(wall,6),'engine_inspect_size_bytes':info.get('Size'),'engine_inspect_size_semantics':'registry_content_bytes_close_to_compressed_layer_sum_not_virtual_or_expanded_size','docker_system_df_virtual_size_display':display,'docker_system_df_virtual_size_fidelity':'rounded_decimal_display','docker_system_df_virtual_size_conservative_upper_bound_bytes':upper,'history_layer_count':len(history_rows),'history_size_displays':[x.get('Size') for x in history_rows],'host_free_before_bytes':free_before,'host_free_after_cleanup_bytes':after,'post_cleanup_host_free_byte_loss':max(0,free_before-after),'cleanup_exit_code':cleanup.returncode})
 max_upper=max(r['docker_system_df_virtual_size_conservative_upper_bound_bytes'] for r in rows);proposed=max(6_000_000_000,math.ceil(max_upper*1.25/1_000_000_000)*1_000_000_000)
 result={'schema_version':'asi_stack.p2_image_size_semantics_calibration.v1','recorded_at_utc':datetime.now(timezone.utc).isoformat(),'state':'passed' if all(r['pull_exit_code']==r['cleanup_exit_code']==0 for r in rows) and proposed<=8_000_000_000 else 'failed','formula_frozen_before_remaining_measurements':FORMULA,'candidate_count':len(rows),'rows':rows,'max_conservative_virtual_upper_bound_bytes':max_upper,'proposed_virtual_size_ceiling_bytes':proposed,'maximum_admissible_virtual_size_ceiling_bytes':8_000_000_000,'campaign_host_free_before_bytes':before,'campaign_host_free_after_bytes':shutil.disk_usage('/').free,'campaign_host_free_byte_loss':max(0,before-shutil.disk_usage('/').free),'prior_resource_record_effect':'engine_inspect_size_values_preserved_but_expanded_size_label_and_pass_invalidated','candidate_test_outcome_opened':False,'final_pool_selected':False,'final_pool_opened':False,'support_state_effect':'none','release_effect':'none'}
 OUT.write_text(json.dumps(result,indent=2)+'\n');print(f"P2 size semantics calibration {result['state']}: max upper {max_upper}, proposed ceiling {proposed}.")

if __name__=='__main__':main()
