#!/usr/bin/env python3
from __future__ import annotations
import copy,hashlib,re
from collections import Counter
from build_canonical_public_status import ROOT,load_json,validate_against_schema
F=ROOT/"experiments/adversarial_evaluation_integrity/fixtures/cases.json";R=ROOT/"experiments/adversarial_evaluation_integrity/results/2026-07-13-local.json";FS=ROOT/"schemas/adversarial_evaluation_integrity_fixture.schema.json";RS=ROOT/"schemas/adversarial_evaluation_integrity_result.schema.json";L=ROOT/"lean/AsiStackProofs/AdversarialEvaluation.lean"
IDS=["valid_to_promotion_review","invalid_missing_selection_context","invalid_missing_reward_provenance","invalid_missing_monitor_provenance","invalid_missing_independent_evaluation","invalid_missing_cross_context_probe","invalid_unresolved_discrepancy","invalid_intent_laundering"]
TH=["complete_integrity_record_reaches_promotion_review","missing_selection_context_requires_repair","missing_reward_provenance_requires_repair","missing_monitor_provenance_requires_repair","missing_independent_evaluation_blocks_review","missing_cross_context_probe_blocks_review","unresolved_discrepancy_routes_to_quarantine","observation_cannot_launder_intent_inference"]
def route(x):
  if not x["model_task_identity_recorded"]:return "retain_as_draft"
  if not x["elicitation_context_recorded"] or not x["selection_context_recorded"] or not x["reward_provenance_recorded"] or not x["monitor_provenance_recorded"]:return "require_context_repair"
  if not x["independent_evaluation_recorded"] or not x["cross_context_probe_recorded"]:return "require_independent_evaluation"
  if x["unresolved_integrity_discrepancy"]:return "quarantine_discrepancy"
  if not x["residual_owner_recorded"]:return "require_residual_owner"
  if x["promotion_requested"] and not x["no_intent_inference_recorded"]:return "reject_intent_laundering"
  return "release_to_promotion_review" if x["promotion_requested"] else "retain_as_draft"
def errs(d):
  f,o,l=d["f"],d["r"],d["l"];e=[];cs=f.get("cases",[])
  if [c.get("id") for c in cs]!=IDS:e.append("case order drift")
  got=[{"id":c["id"],"expected_route":c["expected_route"],"actual_route":route(c["record"]),"passed":route(c["record"])==c["expected_route"]} for c in cs]
  if o.get("case_results")!=got:e.append("result drift")
  if o.get("route_counts")!=dict(Counter(x["actual_route"] for x in got)):e.append("count drift")
  if o.get("fixture_sha256")!=hashlib.sha256(F.read_bytes()).hexdigest():e.append("digest drift")
  if o.get("lean_bridge",{}).get("theorems")!=TH:e.append("theorem list drift")
  for t in TH:
    if not re.search(rf"^theorem\s+{re.escape(t)}\b",l,re.M):e.append("missing theorem "+t)
  if f.get("support_state_effect")!="none" or o.get("support_state_effect")!="none":e.append("support promotion")
  if len(f.get("non_claims",[]))<6 or len(o.get("non_claims",[]))<6:e.append("nonclaims erased")
  return e
def main():
  d={"f":load_json(F),"r":load_json(R),"l":L.read_text()};e=validate_against_schema(d["f"],load_json(FS),str(F.relative_to(ROOT)))+validate_against_schema(d["r"],load_json(RS),str(R.relative_to(ROOT)))+errs(d)
  for m in [lambda q:q["f"].__setitem__("cases",q["f"]["cases"][:-1]),lambda q:q["r"].__setitem__("fixture_sha256","0"*64),lambda q:q["r"].__setitem__("support_state_effect","prototype-backed"),lambda q:q["r"]["lean_bridge"].__setitem__("theorems",q["r"]["lean_bridge"]["theorems"][:-1]),lambda q:q["r"].__setitem__("non_claims",[])]:
    q=copy.deepcopy(d);m(q)
    if not errs(q):e.append("negative mutation accepted")
  if e:raise SystemExit("Adversarial evaluation validation failed:\n - "+"\n - ".join(e))
  print("Adversarial evaluation integrity passed: 8 routes, 8 owned Lean theorems, no support movement, and 5 rejecting mutations.")
if __name__=="__main__":main()
