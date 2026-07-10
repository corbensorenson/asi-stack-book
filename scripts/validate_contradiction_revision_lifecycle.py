#!/usr/bin/env python3
from __future__ import annotations
from copy import deepcopy
import json
from pathlib import Path
from typing import Any
from validate_protocol_examples import validate_value
ROOT=Path(__file__).resolve().parents[1]; SCHEMA=ROOT/'schemas/contradiction_revision_lifecycle_record.schema.json'; VALID=ROOT/'tests/fixtures/protocol_records/contradiction_revision_lifecycle_record.valid.json'; MUTATIONS=ROOT/'experiments/contradiction_revision_lifecycle/fixtures'
SOURCES={"cca_project","moecot_manifest_project","beastbrain_project","bugbrain_project","corbens_best_model_possible_project"}
def load(p:Path)->Any:return json.loads(p.read_text())
def errors(r:dict[str,Any])->list[str]:
 e=[]
 if set(r.get('source_ids',[]))!=SOURCES:e.append('contradiction lifecycle must name the five historical-project sources exactly')
 s=r.get('separated_states',{})
 if not s.get('justification_refs'):e.append('justification state requires explicit justification references')
 if len({s.get('justification_state'),s.get('lifecycle_state'),s.get('commitment_state'),s.get('authority_state')})<4:e.append('justification lifecycle commitment and authority states must remain distinct')
 seq=r.get('contradiction_sequence',[])
 if [(x.get('strength'),x.get('strength_rank')) for x in seq]!=[('weak',1),('medium',2),('strong',3)]:e.append('contradiction strength must progress weak medium strong monotonically')
 ranks=[x.get('response_rank') for x in seq]
 if ranks!=sorted(ranks) or ranks!=[1,2,3]:e.append('contradiction response must never weaken as evidence strength rises')
 if seq and seq[-1].get('response')!='downgrade_or_split':e.append('strong contradiction must downgrade or split the claim')
 rev=r.get('revision',{}); identity=r.get('claim_identity',{})
 if rev.get('superseded_claim_id')!=identity.get('claim_id') or not rev.get('successor_claim_ids'):e.append('supersession must bind the replaced claim and named successors')
 residuals={x.get('unresolved_residual_ref') for x in seq}; recorded=set(rev.get('unresolved_residual_refs',[]))
 if residuals!=recorded:e.append('every contradiction residual must survive the revision exactly')
 repair=r.get('dependency_repair',{}); declared=set(repair.get('declared_affected_claim_ids',[])); repaired=set(repair.get('repaired_claim_ids',[]))
 if repaired!=declared:e.append('bounded dependency repair must cover the declared affected closure exactly')
 if repair.get('repair_count')!=len(repaired) or repair.get('repair_count',0)>repair.get('repair_budget',0):e.append('dependency repair count must remain inside its declared budget')
 mig=r.get('ontology_migration',{})
 if mig.get('new_version')!=identity.get('ontology_version') or mig.get('prior_version')==mig.get('new_version') or not mig.get('migration_ref') or not mig.get('identity_preserved'):e.append('ontology version change requires a binding migration that preserves claim identity')
 p=r.get('restart_persistence',{})
 if not set(rev.get('successor_claim_ids',[])).issubset(set(p.get('visible_claim_ids',[]))) or rev.get('revision_id') not in p.get('visible_revision_ids',[]) or not recorded.issubset(set(p.get('visible_residual_refs',[]))):e.append('restart persistence must retain successors revision and unresolved residuals')
 d=r.get('decision',{})
 if d.get('promotion_allowed') or d.get('support_state_effect')=='eligible_for_bounded_evidence_review':e.append('unresolved hand-authored contradiction lifecycle cannot promote support')
 return e
def mutate(v,m):
 x=deepcopy(v); y=x
 for s in m['path'][:-1]:y=y[s]
 y[m['path'][-1]]=m['value']; return x
def main():
 s=load(SCHEMA); v=load(VALID); found=validate_value(v,s,str(VALID.relative_to(ROOT)))+errors(v)
 if found:raise SystemExit('Valid contradiction lifecycle failed:\n - '+'\n - '.join(found))
 ms=sorted(MUTATIONS.glob('invalid_*.json'))
 for p in ms:
  m=load(p); c=mutate(v,m); found=validate_value(c,s,str(p.relative_to(ROOT)))+errors(c)
  if not any(m['expected_error'] in z for z in found):raise SystemExit(f'{p.relative_to(ROOT)} did not produce {m["expected_error"]!r}: {found}')
 print(f'Contradiction/revision lifecycle harness passed: 1 bounded five-project record and {len(ms)} expected-invalid mutations.')
if __name__=='__main__':main()
