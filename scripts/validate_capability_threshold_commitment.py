#!/usr/bin/env python3
from __future__ import annotations
import copy,hashlib,re
from collections import Counter
from build_canonical_public_status import ROOT,load_json,validate_against_schema
F=ROOT/"experiments/capability_threshold_commitment/fixtures/cases.json";R=ROOT/"experiments/capability_threshold_commitment/results/2026-07-13-local.json";FS=ROOT/"schemas/capability_threshold_commitment_fixture.schema.json";RS=ROOT/"schemas/capability_threshold_commitment_result.schema.json";L=ROOT/"lean/AsiStackProofs/CapabilityThresholds.lean"
IDS=["valid_crossed_to_readiness","valid_non_crossing_to_readiness","invalid_missing_evaluation_envelope","invalid_missing_baseline","invalid_missing_uncertainty","invalid_missing_residual_owner","invalid_crossed_missing_safeguards","invalid_crossed_unverified_safeguards"]
TH=["crossed_threshold_without_verified_safeguards_blocks_release","missing_evaluation_envelope_requires_reevaluation","complete_crossed_threshold_reaches_readiness_review","complete_non_crossing_reaches_readiness_review","missing_baseline_requires_reevaluation","missing_uncertainty_requires_reevaluation","missing_residual_owner_requires_accountable_exception","crossed_threshold_without_safeguard_record_blocks_release"]
def route(x):
  if not x["capability_domain_recorded"]:return "retain_as_assessment_draft"
  if not x["threat_model_recorded"] or not x["evaluation_envelope_recorded"] or not x["elicitation_recorded"] or not x["threshold_definition_recorded"] or not x["coverage_date_recorded"] or not x["baseline_recorded"] or not x["uncertainty_recorded"]:return "require_reevaluation"
  if not x["residual_owner_recorded"]:return "require_accountable_exception"
  if x["threshold_crossed"] and (not x["required_safeguards_recorded"] or not x["safeguards_verified"]):return "block_affected_release"
  return "release_to_readiness_review" if x["release_decision_requested"] else "retain_as_assessment_draft"
def errs(d):
  f,o,l=d["f"],d["r"],d["l"];e=[];cs=f.get("cases",[])
  if [c.get("id") for c in cs]!=IDS:e.append("case order drift")
  got=[{"id":c["id"],"expected_route":c["expected_route"],"actual_route":route(c["record"]),"passed":route(c["record"])==c["expected_route"]} for c in cs]
  if o.get("case_results")!=got:e.append("result drift")
  if o.get("route_counts")!=dict(Counter(x["actual_route"] for x in got)):e.append("counts drift")
  if o.get("fixture_sha256")!=hashlib.sha256(F.read_bytes()).hexdigest():e.append("digest drift")
  if o.get("lean_bridge",{}).get("theorems")!=TH:e.append("theorem list drift")
  for t in TH:
    if not re.search(rf"^theorem\s+{re.escape(t)}\b",l,re.M):e.append("missing theorem "+t)
  if f.get("support_state_effect")!="none" or o.get("support_state_effect")!="none":e.append("support promotion")
  if len(f.get("non_claims",[]))<6 or len(o.get("non_claims",[]))<6:e.append("nonclaims erased")
  return e
def main():
  d={"f":load_json(F),"r":load_json(R),"l":L.read_text()};e=validate_against_schema(d["f"],load_json(FS),str(F.relative_to(ROOT)))+validate_against_schema(d["r"],load_json(RS),str(R.relative_to(ROOT)))+errs(d)
  controls=[lambda x:x["f"].__setitem__("cases",x["f"]["cases"][:-1]),lambda x:x["r"].__setitem__("fixture_sha256","0"*64),lambda x:x["r"].__setitem__("support_state_effect","prototype-backed"),lambda x:x["r"]["lean_bridge"].__setitem__("theorems",x["r"]["lean_bridge"]["theorems"][:-1]),lambda x:x["r"].__setitem__("non_claims",[])]
  for m in controls:
    q=copy.deepcopy(d);m(q)
    if not errs(q):e.append("negative mutation accepted")
  if e:raise SystemExit("Capability threshold validation failed:\n - "+"\n - ".join(e))
  print("Capability threshold commitment passed: 8 routes, 8 Lean theorems, no support movement, and 5 rejecting mutations.")
if __name__=="__main__":main()
