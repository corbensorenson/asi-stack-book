#!/usr/bin/env python3
from __future__ import annotations
import copy,hashlib,re
from collections import Counter
from build_canonical_public_status import ROOT,load_json,validate_against_schema
F=ROOT/"experiments/safety_case_assurance/fixtures/cases.json";R=ROOT/"experiments/safety_case_assurance/results/2026-07-13-local.json";FS=ROOT/"schemas/safety_case_assurance_fixture.schema.json";RS=ROOT/"schemas/safety_case_assurance_result.schema.json";L=ROOT/"lean/AsiStackProofs/SafetyCases.lean"
IDS=["valid_to_readiness_review","invalid_missing_deployment_context","invalid_missing_hazard_model","invalid_stale_evidence_dependency","invalid_missing_countercase_review","invalid_missing_independent_review","invalid_unresolved_defeater","invalid_authority_laundering"]
TH=["complete_case_reaches_readiness_review","missing_deployment_context_retains_draft","missing_hazard_model_requires_case_repair","stale_evidence_dependency_requires_repair","missing_countercase_review_requires_review","missing_independent_review_requires_review","unresolved_defeater_requires_accountable_review","case_cannot_launder_release_authority"]
def route(x):
  if not x["deployment_context_recorded"]:return "retain_as_case_draft"
  if not x["top_claim_scoped"] or not x["hazard_model_recorded"] or not x["argument_strategies_recorded"] or not x["evidence_references_recorded"]:return "require_case_repair"
  if not x["evidence_dependencies_current"]:return "require_evidence_repair"
  if not x["assumptions_recorded"]:return "require_case_repair"
  if not x["countercase_review_recorded"]:return "require_countercase_review"
  if not x["independent_review_recorded"]:return "require_independent_review"
  if x["unresolved_defeater_present"]:return "require_accountable_review"
  if not x["acceptance_criterion_recorded"] or not x["residual_owner_recorded"]:return "require_case_repair"
  if not x["decision_authority_recorded"]:return "require_accountable_review"
  if not x["authority_separation_recorded"]:return "reject_authority_laundering"
  return "release_to_readiness_review" if x["affected_release_requested"] else "retain_as_case_draft"
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
  if e:raise SystemExit("Safety case assurance validation failed:\n - "+"\n - ".join(e))
  print("Safety case assurance passed: 8 routes, 8 owned Lean theorems, no support movement, and 5 rejecting mutations.")
if __name__=="__main__":main()
