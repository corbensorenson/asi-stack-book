#!/usr/bin/env python3
"""Recompute the bounded scalable-oversight fixture and reject laundering."""

from __future__ import annotations

import copy
import hashlib
import re
from collections import Counter
from pathlib import Path

from build_canonical_public_status import ROOT, load_json, validate_against_schema


FIXTURE = ROOT / "experiments/scalable_oversight_protocol/fixtures/cases.json"
RESULT = ROOT / "experiments/scalable_oversight_protocol/results/2026-07-13-local.json"
FIXTURE_SCHEMA = ROOT / "schemas/scalable_oversight_protocol_fixture.schema.json"
RESULT_SCHEMA = ROOT / "schemas/scalable_oversight_protocol_result.schema.json"
LEAN = ROOT / "lean/AsiStackProofs/ScalableOversight.lean"
EXPECTED_IDS = [
    "valid_bounded_use",
    "invalid_missing_evidence_views",
    "invalid_undisclosed_shared_dependencies",
    "invalid_missing_direct_baseline",
    "invalid_high_risk_missing_outcome_audit",
    "invalid_unjustified_abstention",
    "invalid_authority_laundering",
]
EXPECTED_THEOREMS = [
    "missing_outcome_audit_blocks_high_risk_admission",
    "missing_baseline_requires_protocol_redesign",
    "complete_bounded_use_is_admitted",
    "missing_evidence_views_requires_access_repair",
    "undisclosed_shared_dependencies_require_review",
    "high_risk_use_without_outcome_audit_requires_audit",
    "unjustified_abstention_requires_evidence",
    "downstream_use_cannot_launder_authority",
]


def route(record: dict) -> str:
    if not record["protocol_digest_recorded"] or not record["task_cohort_recorded"]:
        return "retain_as_draft"
    if not record["capability_envelopes_recorded"] or not record["evidence_views_recorded"]:
        return "require_access_repair"
    if not record["shared_dependencies_recorded"]:
        return "require_dependency_review"
    if not record["direct_review_baseline_recorded"]:
        return "require_protocol_redesign"
    if record["high_risk_use"] and not record["independent_outcome_audit_recorded"]:
        return "require_outcome_audit"
    if not record["residual_recorded"]:
        return "require_dependency_review"
    if not record["permitted_consumer_recorded"] or not record["expiry_recorded"]:
        return "retain_as_draft"
    if record["downstream_use_requested"] and not record["no_authority_grant_recorded"]:
        return "reject_authority_laundering"
    if record["abstention_requested"] and (not record["abstention_evidence_recorded"] or not record["abstention_defeater_recorded"]):
        return "require_abstention_evidence"
    if record["downstream_use_requested"]:
        return "admit_bounded_use"
    return "retain_as_draft"


def semantic_errors(data: dict) -> list[str]:
    errors: list[str] = []
    fixture = data["fixture"]
    result = data["result"]
    cases = fixture.get("cases", [])
    if [case.get("id") for case in cases] != EXPECTED_IDS:
        errors.append("case identity/order drifted")
    computed = []
    for case in cases:
        actual = route(case["record"])
        computed.append({"id": case["id"], "expected_route": case["expected_route"], "actual_route": actual, "passed": actual == case["expected_route"]})
        if actual != case["expected_route"]:
            errors.append(f"{case['id']}: expected {case['expected_route']}, recomputed {actual}")
    if result.get("case_results") != computed:
        errors.append("tracked result does not equal deterministic recomputation")
    counts = dict(Counter(row["actual_route"] for row in computed))
    if result.get("route_counts") != counts:
        errors.append("route counts disagree with recomputation")
    digest = hashlib.sha256(FIXTURE.read_bytes()).hexdigest()
    if result.get("fixture_sha256") != digest:
        errors.append("fixture digest disagrees with tracked bytes")
    lean_text = data["lean"]
    if result.get("lean_bridge", {}).get("theorems") != EXPECTED_THEOREMS:
        errors.append("Lean bridge theorem list drifted")
    for theorem in EXPECTED_THEOREMS:
        if not re.search(rf"^theorem\s+{re.escape(theorem)}\b", lean_text, re.M):
            errors.append(f"Lean theorem absent: {theorem}")
    if fixture.get("support_state_effect") != "none" or result.get("support_state_effect") != "none":
        errors.append("fixture or result invents support-state movement")
    if len(fixture.get("non_claims", [])) < 5 or len(result.get("non_claims", [])) < 5:
        errors.append("non-claim boundary was erased")
    return errors


def negative_controls(base: dict) -> list[str]:
    failures: list[str] = []
    mutations: list[tuple[str, dict]] = []
    missing = copy.deepcopy(base)
    missing["fixture"]["cases"] = missing["fixture"]["cases"][:-1]
    mutations.append(("missing case", missing))
    wrong_route = copy.deepcopy(base)
    wrong_route["fixture"]["cases"][1]["expected_route"] = "admit_bounded_use"
    mutations.append(("wrong route", wrong_route))
    audit_laundering = copy.deepcopy(base)
    audit_laundering["fixture"]["cases"][4]["record"]["independent_outcome_audit_recorded"] = True
    mutations.append(("audit laundering", audit_laundering))
    authority_laundering = copy.deepcopy(base)
    authority_laundering["result"]["case_results"][-1]["actual_route"] = "admit_bounded_use"
    mutations.append(("authority laundering", authority_laundering))
    support = copy.deepcopy(base)
    support["result"]["support_state_effect"] = "prototype-backed"
    mutations.append(("support promotion", support))
    digest = copy.deepcopy(base)
    digest["result"]["fixture_sha256"] = "0" * 64
    mutations.append(("digest mismatch", digest))
    theorem = copy.deepcopy(base)
    theorem["result"]["lean_bridge"]["theorems"] = theorem["result"]["lean_bridge"]["theorems"][:-1]
    mutations.append(("theorem erasure", theorem))
    nonclaims = copy.deepcopy(base)
    nonclaims["result"]["non_claims"] = []
    mutations.append(("non-claim erasure", nonclaims))
    for label, mutated in mutations:
        if not semantic_errors(mutated):
            failures.append(f"negative control was accepted: {label}")
    return failures


def main() -> None:
    required = [FIXTURE, RESULT, FIXTURE_SCHEMA, RESULT_SCHEMA, LEAN]
    missing = [path.relative_to(ROOT).as_posix() for path in required if not path.is_file()]
    if missing:
        raise SystemExit("missing scalable-oversight artifacts: " + ", ".join(missing))
    data = {"fixture": load_json(FIXTURE), "result": load_json(RESULT), "lean": LEAN.read_text(encoding="utf-8")}
    errors = validate_against_schema(data["fixture"], load_json(FIXTURE_SCHEMA), FIXTURE.relative_to(ROOT).as_posix())
    errors.extend(validate_against_schema(data["result"], load_json(RESULT_SCHEMA), RESULT.relative_to(ROOT).as_posix()))
    errors.extend(semantic_errors(data))
    errors.extend(negative_controls(data))
    if errors:
        raise SystemExit("Scalable oversight protocol validation failed:\n - " + "\n - ".join(errors))
    print("Scalable oversight protocol passed: 7 deterministic routes, 8 Lean theorems, no support movement, and 8 rejecting mutations.")


if __name__ == "__main__":
    main()
