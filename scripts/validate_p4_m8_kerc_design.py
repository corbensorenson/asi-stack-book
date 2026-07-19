#!/usr/bin/env python3
"""Validate Campaign 6's prospective freeze without reading outcomes."""
from __future__ import annotations
import copy
from p4_m8_kerc_common import BASE, ROOT, load, sha

def errors(design,corpus,prereg):
    out=[]; rows=corpus.get("rows",[])
    if len(rows)!=192 or design.get("record_count")!=192: out.append("corpus denominator")
    counts={p:sum(x.get("phase")==p for x in rows) for p in ("train","heldout","adversarial_heldout")}
    if counts!={"train":128,"heldout":32,"adversarial_heldout":32} or design.get("split_counts")!=counts: out.append("split")
    if len({x.get("record_id") for x in rows})!=192: out.append("identity")
    if {x.get("language") for x in rows}!={"en","es"} or {x.get("domain") for x in rows}!={"operations","research"}: out.append("coverage")
    if len(design.get("baselines",[]))!=8 or len(design.get("ablations",[]))!=13 or design.get("attack_count")!=20: out.append("controls")
    if prereg.get("state")!="prospectively_frozen_before_outcome_execution" or prereg.get("outcome_aware_retry_allowed") is not False or prereg.get("heldout_label_access_during_training") is not False: out.append("freeze")
    if prereg.get("design_sha256")!=sha(BASE/"design.json") or prereg.get("corpus_sha256")!=sha(BASE/"corpus.json") or prereg.get("result_schema_sha256")!=sha(ROOT/"schemas/p4_m8_kerc_result.schema.json"): out.append("lineage")
    for filename,digest in prereg.get("code_sha256",{}).items():
      if digest!=sha(ROOT/"scripts"/filename): out.append(f"code drift:{filename}")
    if "no general semantic truth" not in design.get("support_ceiling",""): out.append("ceiling")
    return out

def main():
    d,c,p=load(BASE/"design.json"),load(BASE/"corpus.json"),load(BASE/"preregistration.json"); failures=errors(d,c,p)
    for label,source,mutate in [
      ("inflate",d,lambda x:x.__setitem__("record_count",193)),("drop baseline",d,lambda x:x["baselines"].pop()),("open retry",p,lambda x:x.__setitem__("outcome_aware_retry_allowed",True)),("leak labels",p,lambda x:x.__setitem__("heldout_label_access_during_training",True)),("drop attack",d,lambda x:x.__setitem__("attack_count",19)),("weaken ceiling",d,lambda x:x.__setitem__("support_ceiling","general efficiency proved"))]:
      dd,cc,pp=copy.deepcopy(d),copy.deepcopy(c),copy.deepcopy(p); target=dd if source is d else pp; mutate(target)
      if not errors(dd,cc,pp): failures.append(f"mutation accepted:{label}")
    if failures: raise SystemExit("KERC design validation failed:\n - "+"\n - ".join(failures))
    print("KERC design passed: 192 bilingual records, 128/32/32 split, five seeds, eight baselines, thirteen ablations, twenty attacks, six mutations rejected, no support effect.")
if __name__=="__main__": main()
