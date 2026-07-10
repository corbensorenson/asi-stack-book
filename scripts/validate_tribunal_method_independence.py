#!/usr/bin/env python3
from __future__ import annotations
from copy import deepcopy
import json
from pathlib import Path
from typing import Any
from validate_protocol_examples import validate_value
ROOT=Path(__file__).resolve().parents[1]; SCHEMA=ROOT/'schemas/tribunal_method_independence_record.schema.json'; VALID=ROOT/'tests/fixtures/protocol_records/tribunal_method_independence_record.valid.json'; MUTATIONS=ROOT/'experiments/tribunal_method_independence/fixtures'
SOURCES={"cca_project","moecot_manifest_project","beastbrain_project","bugbrain_project","corbens_best_model_possible_project"}; LABELS={"formal_proof","citation_check","procedural_replay","adversarial_probe","falsification","abstention"}
def load(p:Path)->Any:return json.loads(p.read_text())
def errs(r:dict[str,Any])->list[str]:
 e=[]; ms=r.get('methods',[]); ids={m.get('method_id') for m in ms}
 if set(r.get('source_ids',[]))!=SOURCES:e.append('tribunal lineage must name the five historical-project sources exactly')
 if {m.get('method_label') for m in ms}!=LABELS:e.append('tribunal must label proof citation replay adversarial falsification and abstention methods exactly')
 groups=[m.get('independence_group') for m in ms]
 if len(groups)!=len(set(groups)):e.append('independent tribunal methods cannot share an independence group')
 edges=r.get('independence_edges',[])
 if any(x.get('from') not in ids or x.get('to') not in ids for x in edges):e.append('independence graph edges must bind declared methods')
 dep={(x.get('from'),x.get('to')) for x in edges if x.get('relation')=='depends_on'}
 if any((b,a) in dep for a,b in dep):e.append('independence dependency graph cannot contain a two-node cycle')
 if r.get('verdict',{}).get('independent_group_count')!=len(set(groups)):e.append('verdict independent-group count must match the method graph')
 empty=[c for c in r.get('case_results',[]) if c.get('case_kind')=='empty_case']
 if not empty or any(c.get('evidence_present') or c.get('verdict')=='accept' for c in empty):e.append('empty or vacuous cases must abstain or block rather than accept')
 fals=[m for m in ms if m.get('method_label')=='falsification']
 if not fals or not fals[0].get('evidence_refs') or fals[0].get('result')=='pass':e.append('tribunal requires a substantive falsification attempt and preserves failure')
 abst=[m for m in ms if m.get('method_label')=='abstention']
 if not abst or abst[0].get('result')!='abstain' or abst[0].get('vote')!='abstain':e.append('abstention must remain an explicit non-approval result')
 dissent=r.get('dissent',{}); veto=[m for m in ms if m.get('veto_exercised')]
 if veto and (not dissent.get('present') or not dissent.get('preserved_in_verdict') or any(m.get('method_id') not in dissent.get('method_ids',[]) or not m.get('veto_reason') for m in veto)):e.append('every veto and dissent must be visible and preserved in the verdict')
 v=r.get('verdict',{}); d=r.get('decision',{})
 if v.get('default_approval_used'):e.append('tribunal verdict cannot use default approval')
 if dissent.get('present') and (v.get('state')=='accept' or not v.get('unresolved_refs')):e.append('unresolved dissent cannot silently yield acceptance')
 if d.get('ordinary_promotion_allowed') or d.get('support_state_effect')=='eligible_for_bounded_evidence_review':e.append('hand-authored tribunal fixture cannot promote support')
 return e
def mutate(v,m):
 x=deepcopy(v); y=x
 for s in m['path'][:-1]:y=y[s]
 y[m['path'][-1]]=m['value']; return x
def main():
 s=load(SCHEMA); v=load(VALID); found=validate_value(v,s,str(VALID.relative_to(ROOT)))+errs(v)
 if found:raise SystemExit('Valid tribunal method record failed:\n - '+'\n - '.join(found))
 ms=sorted(MUTATIONS.glob('invalid_*.json'))
 for p in ms:
  m=load(p); c=mutate(v,m); found=validate_value(c,s,str(p.relative_to(ROOT)))+errs(c)
  if not any(m['expected_error'] in z for z in found):raise SystemExit(f'{p.relative_to(ROOT)} did not produce {m["expected_error"]!r}: {found}')
 print(f'Tribunal method/independence harness passed: 1 bounded five-project record and {len(ms)} expected-invalid mutations.')
if __name__=='__main__':main()
