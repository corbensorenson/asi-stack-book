#!/usr/bin/env python3
"""Recompute the bounded open-ended-improvement campaign fixture."""

from __future__ import annotations

import copy
import hashlib
import re
from collections import Counter

from build_canonical_public_status import ROOT, load_json, validate_against_schema

FIXTURE = ROOT / "experiments/open_ended_improvement_campaign/fixtures/cases.json"
RESULT = ROOT / "experiments/open_ended_improvement_campaign/results/2026-07-13-local.json"
FIXTURE_SCHEMA = ROOT / "schemas/open_ended_improvement_campaign_fixture.schema.json"
RESULT_SCHEMA = ROOT / "schemas/open_ended_improvement_campaign_result.schema.json"
LEAN = ROOT / "lean/AsiStackProofs/OpenEndedImprovement.lean"
EXPECTED_IDS = [
    "valid_candidate_to_governor_review",
    "invalid_missing_independent_qualification",
    "invalid_budget_exhausted",
    "invalid_missing_stop_authority",
    "invalid_erased_failure_history",
    "invalid_missing_residual_owner",
    "invalid_candidate_authority_laundering",
]
EXPECTED_THEOREMS = [
    "complete_candidate_reaches_governor_review",
    "missing_independent_qualification_requires_separation",
    "exhausted_budget_requires_repair",
    "missing_stop_authority_blocks_admission",
    "erased_failure_history_requires_archive_repair",
    "missing_residual_owner_blocks_admission",
    "candidate_cannot_launder_admission_authority",
]


def route(r: dict) -> str:
    if not r["objective_digest_recorded"] or not r["task_policy_digest_recorded"] or not r["generator_identity_recorded"]:
        return "retain_as_draft"
    if not r["evaluator_identity_recorded"] or not r["evaluator_dependencies_recorded"] or not r["independent_qualification_recorded"]:
        return "require_evaluator_separation"
    if not r["resource_bill_recorded"] or not r["within_registered_budget"]:
        return "require_budget_repair"
    if not r["stop_authority_recorded"]:
        return "require_stop_authority"
    if not r["failure_history_preserved"] or not r["archive_disposition_recorded"]:
        return "require_archive_repair"
    if not r["residual_owner_recorded"]:
        return "require_residual_owner"
    if not r["permitted_consumer_recorded"]:
        return "retain_as_draft"
    if r["admission_requested"] and not r["no_authority_grant_recorded"]:
        return "reject_authority_laundering"
    if r["admission_requested"]:
        return "release_to_governor_review"
    return "retain_as_draft"


def semantic_errors(data: dict) -> list[str]:
    fixture, result = data["fixture"], data["result"]
    errors: list[str] = []
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
    if result.get("route_counts") != dict(Counter(row["actual_route"] for row in computed)):
        errors.append("route counts disagree with recomputation")
    if result.get("fixture_sha256") != hashlib.sha256(FIXTURE.read_bytes()).hexdigest():
        errors.append("fixture digest disagrees with tracked bytes")
    if result.get("lean_bridge", {}).get("theorems") != EXPECTED_THEOREMS:
        errors.append("Lean bridge theorem list drifted")
    for theorem in EXPECTED_THEOREMS:
        if not re.search(rf"^theorem\s+{re.escape(theorem)}\b", data["lean"], re.M):
            errors.append(f"Lean theorem absent: {theorem}")
    if fixture.get("support_state_effect") != "none" or result.get("support_state_effect") != "none":
        errors.append("fixture or result invents support-state movement")
    if len(fixture.get("non_claims", [])) < 5 or len(result.get("non_claims", [])) < 5:
        errors.append("non-claim boundary was erased")
    return errors


def negative_controls(base: dict) -> list[str]:
    mutations: list[tuple[str, dict]] = []
    for label, mutator in [
        ("missing case", lambda d: d["fixture"].__setitem__("cases", d["fixture"]["cases"][:-1])),
        ("wrong route", lambda d: d["fixture"]["cases"][1].__setitem__("expected_route", "release_to_governor_review")),
        ("qualification laundering", lambda d: d["fixture"]["cases"][1]["record"].__setitem__("independent_qualification_recorded", True)),
        ("budget laundering", lambda d: d["result"]["case_results"][2].__setitem__("actual_route", "release_to_governor_review")),
        ("stop laundering", lambda d: d["result"]["case_results"][3].__setitem__("actual_route", "release_to_governor_review")),
        ("authority laundering", lambda d: d["result"]["case_results"][6].__setitem__("actual_route", "release_to_governor_review")),
        ("support promotion", lambda d: d["result"].__setitem__("support_state_effect", "prototype-backed")),
        ("digest mismatch", lambda d: d["result"].__setitem__("fixture_sha256", "0" * 64)),
        ("theorem erasure", lambda d: d["result"]["lean_bridge"].__setitem__("theorems", d["result"]["lean_bridge"]["theorems"][:-1])),
        ("non-claim erasure", lambda d: d["result"].__setitem__("non_claims", [])),
    ]:
        mutated = copy.deepcopy(base)
        mutator(mutated)
        mutations.append((label, mutated))
    return [f"negative control was accepted: {label}" for label, mutated in mutations if not semantic_errors(mutated)]


def main() -> None:
    required = [FIXTURE, RESULT, FIXTURE_SCHEMA, RESULT_SCHEMA, LEAN]
    missing = [path.relative_to(ROOT).as_posix() for path in required if not path.is_file()]
    if missing:
        raise SystemExit("missing open-ended campaign artifacts: " + ", ".join(missing))
    data = {"fixture": load_json(FIXTURE), "result": load_json(RESULT), "lean": LEAN.read_text(encoding="utf-8")}
    errors = validate_against_schema(data["fixture"], load_json(FIXTURE_SCHEMA), FIXTURE.relative_to(ROOT).as_posix())
    errors.extend(validate_against_schema(data["result"], load_json(RESULT_SCHEMA), RESULT.relative_to(ROOT).as_posix()))
    errors.extend(semantic_errors(data))
    errors.extend(negative_controls(data))
    if errors:
        raise SystemExit("Open-ended improvement campaign validation failed:\n - " + "\n - ".join(errors))
    print("Open-ended improvement campaign passed: 7 deterministic routes, 7 owned Lean theorems, no support movement, and 10 rejecting mutations.")


if __name__ == "__main__":
    main()
