#!/usr/bin/env python3
from __future__ import annotations
from copy import deepcopy
import json
from pathlib import Path
from typing import Any
from validate_protocol_examples import validate_value
ROOT=Path(__file__).resolve().parents[1]; SCHEMA=ROOT/'schemas/context_restart_recovery_record.schema.json'; VALID=ROOT/'tests/fixtures/protocol_records/context_restart_recovery_record.valid.json'; MUTATIONS=ROOT/'experiments/context_restart_recovery/fixtures'
EXPECTED_SOURCES={"cca_project","moecot_manifest_project","beastbrain_project","bugbrain_project","corbens_best_model_possible_project"}; OPS=["freeze","thaw","rebalance","promote","compact","partial_write_recovery","restart"]
def load(p:Path)->Any:return json.loads(p.read_text())
def semantic_errors(r:dict[str,Any])->list[str]:
 e=[]; ts=r.get('transitions',[])
 if set(r.get('source_ids',[]))!=EXPECTED_SOURCES:e.append('restart lineage must name the five historical-project sources exactly')
 if [t.get('operation') for t in ts]!=OPS:e.append('restart lifecycle operations must appear exactly once in canonical order')
 for i,t in enumerate(ts):
  pre=t.get('pre_state',{}); post=t.get('post_state',{})
  if i and pre.get('state_ref')!=ts[i-1].get('post_state',{}).get('state_ref'):e.append('transition state references must form one causal chain')
  if not t.get('effect_observed') or not t.get('acknowledged'):e.append('every material transition requires observed effect and acknowledgement')
  if t.get('no_loss_required') and set(pre.get('item_ids',[]))!=set(post.get('item_ids',[])):e.append('no-loss transition must preserve every authoritative item identity')
  if t.get('operation')!='partial_write_recovery' and post.get('index_epoch')!=post.get('content_epoch'):e.append('ordinary committed states require atomic index/content epochs')
 by={t.get('operation'):t for t in ts}
 if by.get('freeze',{}).get('post_state',{}).get('lifecycle')!='frozen':e.append('freeze must produce a frozen post-state')
 if by.get('thaw',{}).get('post_state',{}).get('lifecycle')!='active':e.append('thaw must produce an active post-state')
 if by.get('promote',{}).get('post_state',{}).get('tier')!='hot':e.append('promotion must produce an acknowledged hot-tier state')
 p=by.get('partial_write_recovery',{})
 if not p.get('partial_write_detected') or p.get('ordinary_commit_allowed') or p.get('post_state',{}).get('index_epoch')!=p.get('post_state',{}).get('content_epoch'):e.append('partial-write recovery must detect divergence, block ordinary commit, and restore one atomic epoch')
 last=ts[-1].get('post_state',{}) if ts else {}; obs=r.get('restart_observation',{})
 if set(obs.get('visible_item_ids',[]))!=set(last.get('item_ids',[])) or obs.get('index_epoch')!=last.get('index_epoch') or obs.get('content_epoch')!=last.get('content_epoch') or obs.get('recovered_generation')!=last.get('generation'):e.append('restart observation must match the recovered committed state exactly')
 if r.get('decision',{}).get('support_state_effect')=='eligible_for_bounded_evidence_review':e.append('hand-authored restart fixtures cannot promote support')
 return e
def mutate(base,m):
 v=deepcopy(base); x=v
 for s in m['path'][:-1]:x=x[s]
 x[m['path'][-1]]=m['value']; return v
def main():
 s=load(SCHEMA); v=load(VALID); errs=validate_value(v,s,str(VALID.relative_to(ROOT)))+semantic_errors(v)
 if errs:raise SystemExit('Valid context restart record failed:\n - '+'\n - '.join(errs))
 ms=sorted(MUTATIONS.glob('invalid_*.json'))
 for p in ms:
  m=load(p); found=validate_value(mutate(v,m),s,str(p.relative_to(ROOT)))+semantic_errors(mutate(v,m))
  if not any(m['expected_error'] in x for x in found):raise SystemExit(f'{p.relative_to(ROOT)} did not produce {m["expected_error"]!r}: {found}')
 print(f'Context restart/recovery harness passed: 1 bounded five-project lifecycle and {len(ms)} expected-invalid mutations.')
if __name__=='__main__':main()
