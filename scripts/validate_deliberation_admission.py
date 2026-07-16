#!/usr/bin/env python3
"""Recompute the bounded deliberation-admission fixture."""

from __future__ import annotations
import copy, hashlib, re
from collections import Counter
from build_canonical_public_status import ROOT, load_json, validate_against_schema

FIXTURE = ROOT / "experiments/deliberation_admission/fixtures/cases.json"
RESULT = ROOT / "experiments/deliberation_admission/results/2026-07-13-local.json"
FS = ROOT / "schemas/deliberation_admission_fixture.schema.json"
RS = ROOT / "schemas/deliberation_admission_result.schema.json"
LEAN = ROOT / "lean/AsiStackProofs/DeliberationRefinement.lean"
IDS = ["valid_high_risk_to_planning", "invalid_missing_budget_record", "invalid_missing_search_mode", "invalid_missing_verifier_scope", "invalid_missing_candidate_history", "invalid_missing_stop_condition", "invalid_missing_residual_owner", "invalid_trace_authority_laundering", "invalid_budget_exhausted", "invalid_high_risk_missing_independent_verifier"]
THEOREMS = ["high_risk_without_independent_review_blocks_evaluation", "budget_exhaustion_without_residual_blocks_handoff", "raw_score_cannot_promote_selected_candidate", "execution_authority_cannot_cross_planning_handoff", "verified_deliberation_lifecycle_reaches_closed_without_support_or_effect_authority"]

def route(r):
    if not r["request_recorded"]: return "retain_as_draft"
    if not r["think_budget_recorded"] or not r["search_mode_recorded"] or not r["verifier_scope_recorded"] or not r["candidate_history_recorded"] or not r["stop_condition_recorded"] or not r["residual_owner_recorded"] or not r["trace_authority_separated"]: return "require_independent_review"
    if r["budget_exhausted"]: return "stop_and_escrow_residual"
    if r["execution_requested"] and r["high_risk_request"] and not r["independent_verifier_recorded"]: return "require_independent_review"
    return "release_to_planning" if r["execution_requested"] else "retain_as_draft"

def errors(data):
    f, out, lean = data["fixture"], data["result"], data["lean"]
    e=[]; cases=f.get("cases",[])
    if [c.get("id") for c in cases] != IDS: e.append("case identity/order drifted")
    computed=[]
    for c in cases:
        actual=route(c["record"]); computed.append({"id":c["id"],"expected_route":c["expected_route"],"actual_route":actual,"passed":actual==c["expected_route"]})
        if actual != c["expected_route"]: e.append(f"{c['id']}: route mismatch")
    if out.get("case_results") != computed: e.append("result differs from recomputation")
    if out.get("route_counts") != dict(Counter(x["actual_route"] for x in computed)): e.append("route counts drifted")
    if out.get("fixture_sha256") != hashlib.sha256(FIXTURE.read_bytes()).hexdigest(): e.append("digest drifted")
    if out.get("lean_bridge",{}).get("theorems") != THEOREMS: e.append("theorem list drifted")
    for theorem in THEOREMS:
        if not re.search(rf"^theorem\s+{re.escape(theorem)}\b", lean, re.M): e.append(f"missing theorem {theorem}")
    if f.get("known_extra_compute_harms_preserved") != 15 or out.get("known_extra_compute_harms_preserved") != 15: e.append("fifteen-harm regression boundary lost")
    if f.get("support_state_effect") != "none" or out.get("support_state_effect") != "none": e.append("support promotion invented")
    if len(f.get("non_claims",[])) < 6 or len(out.get("non_claims",[])) < 6: e.append("non-claim boundary erased")
    return e

def negative_controls(base):
    controls=[("missing case",lambda d:d["fixture"].__setitem__("cases",d["fixture"]["cases"][:-1])),("wrong route",lambda d:d["fixture"]["cases"][1].__setitem__("expected_route","release_to_planning")),("history laundering",lambda d:d["fixture"]["cases"][4]["record"].__setitem__("candidate_history_recorded",True)),("trace laundering",lambda d:d["result"]["case_results"][7].__setitem__("actual_route","release_to_planning")),("budget laundering",lambda d:d["result"]["case_results"][8].__setitem__("actual_route","release_to_planning")),("verifier laundering",lambda d:d["result"]["case_results"][9].__setitem__("actual_route","release_to_planning")),("harm erasure",lambda d:d["result"].__setitem__("known_extra_compute_harms_preserved",0)),("support promotion",lambda d:d["result"].__setitem__("support_state_effect","prototype-backed")),("digest mismatch",lambda d:d["result"].__setitem__("fixture_sha256","0"*64)),("theorem erasure",lambda d:d["result"]["lean_bridge"].__setitem__("theorems",d["result"]["lean_bridge"]["theorems"][:-1])),("nonclaim erasure",lambda d:d["result"].__setitem__("non_claims",[]))]
    bad=[]
    for label,mutate in controls:
        d=copy.deepcopy(base);mutate(d)
        if not errors(d): bad.append(f"negative control accepted: {label}")
    return bad

def main():
    missing=[p.relative_to(ROOT).as_posix() for p in [FIXTURE,RESULT,FS,RS,LEAN] if not p.is_file()]
    if missing: raise SystemExit("missing deliberation artifacts: "+", ".join(missing))
    d={"fixture":load_json(FIXTURE),"result":load_json(RESULT),"lean":LEAN.read_text()}
    e=validate_against_schema(d["fixture"],load_json(FS),FIXTURE.relative_to(ROOT).as_posix())+validate_against_schema(d["result"],load_json(RS),RESULT.relative_to(ROOT).as_posix())+errors(d)+negative_controls(d)
    if e: raise SystemExit("Deliberation admission validation failed:\n - "+"\n - ".join(e))
    print("Deliberation admission passed: 10 routes, 5 refinement-policy Lean theorems, 15 harms preserved, no support movement, and 11 rejecting mutations.")

if __name__ == "__main__": main()
