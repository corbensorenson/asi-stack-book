#!/usr/bin/env python3
"""Recompute the bounded inter-stack exchange-contract fixture."""

from __future__ import annotations

import copy
import hashlib
import re
from collections import Counter

from build_canonical_public_status import ROOT, load_json, validate_against_schema

FIXTURE = ROOT / "experiments/inter_stack_exchange_contract/fixtures/cases.json"
RESULT = ROOT / "experiments/inter_stack_exchange_contract/results/2026-07-13-local.json"
FIXTURE_SCHEMA = ROOT / "schemas/inter_stack_exchange_contract_fixture.schema.json"
RESULT_SCHEMA = ROOT / "schemas/inter_stack_exchange_contract_result.schema.json"
LEAN = ROOT / "lean/AsiStackProofs/InterStackProtocols.lean"
EXPECTED_IDS = ["valid_complete_local_dispatch", "invalid_missing_sender_identity", "invalid_audience_scope_mismatch", "invalid_expired_request", "invalid_required_credential", "invalid_revoked_credential", "invalid_missing_reserved_budget", "invalid_disputed_receipt", "invalid_missing_residual_owner"]
EXPECTED_THEOREMS = ["invalid_credential_blocks_dispatch", "missing_reserved_budget_blocks_economic_dispatch", "complete_exchange_reaches_local_dispatch", "missing_sender_requires_identity_repair", "audience_mismatch_denies_dispatch", "expired_request_denies_dispatch", "revoked_credential_denies_dispatch", "disputed_receipt_requires_review", "missing_residual_owner_requires_review"]


def route(r: dict) -> str:
    if not r["protocol_version_recorded"]:
        return "retain_as_exchange_draft"
    if not r["endpoint_capability_recorded"]:
        return "require_accountable_review"
    if not r["sender_identity_recorded"] or not r["receiver_identity_recorded"] or not r["principal_recorded"]:
        return "require_identity_repair"
    if not r["delegated_authority_recorded"]:
        return "require_accountable_review"
    if not r["audience_scope_bound"] or not r["request_expiry_current"]:
        return "deny_dispatch"
    if r["credential_required"] and not r["credential_verified"]:
        return "deny_dispatch"
    if not r["credential_current"]:
        return "deny_dispatch"
    if not r["revocation_path_recorded"]:
        return "require_accountable_review"
    if r["value_bearing_request"] and not r["budget_reserved"]:
        return "require_budget_repair"
    if not r["expected_receipt_recorded"] or r["receipt_disputed"] or not r["residual_owner_recorded"]:
        return "require_accountable_review"
    return "release_to_local_dispatch" if r["dispatch_requested"] else "retain_as_exchange_draft"


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
        errors.append("support-state movement invented")
    if len(fixture.get("non_claims", [])) < 6 or len(result.get("non_claims", [])) < 6:
        errors.append("non-claim boundary erased")
    return errors


def negative_controls(base: dict) -> list[str]:
    controls = [
        ("missing case", lambda d: d["fixture"].__setitem__("cases", d["fixture"]["cases"][:-1])),
        ("wrong route", lambda d: d["fixture"]["cases"][2].__setitem__("expected_route", "release_to_local_dispatch")),
        ("identity laundering", lambda d: d["fixture"]["cases"][1]["record"].__setitem__("sender_identity_recorded", True)),
        ("audience laundering", lambda d: d["result"]["case_results"][2].__setitem__("actual_route", "release_to_local_dispatch")),
        ("revocation laundering", lambda d: d["result"]["case_results"][5].__setitem__("actual_route", "release_to_local_dispatch")),
        ("budget laundering", lambda d: d["result"]["case_results"][6].__setitem__("actual_route", "release_to_local_dispatch")),
        ("dispute laundering", lambda d: d["result"]["case_results"][7].__setitem__("actual_route", "release_to_local_dispatch")),
        ("support promotion", lambda d: d["result"].__setitem__("support_state_effect", "prototype-backed")),
        ("digest mismatch", lambda d: d["result"].__setitem__("fixture_sha256", "0" * 64)),
        ("theorem erasure", lambda d: d["result"]["lean_bridge"].__setitem__("theorems", d["result"]["lean_bridge"]["theorems"][:-1])),
        ("non-claim erasure", lambda d: d["result"].__setitem__("non_claims", [])),
    ]
    failures = []
    for label, mutate in controls:
        candidate = copy.deepcopy(base)
        mutate(candidate)
        if not semantic_errors(candidate):
            failures.append(f"negative control was accepted: {label}")
    return failures


def main() -> None:
    required = [FIXTURE, RESULT, FIXTURE_SCHEMA, RESULT_SCHEMA, LEAN]
    missing = [path.relative_to(ROOT).as_posix() for path in required if not path.is_file()]
    if missing:
        raise SystemExit("missing inter-stack artifacts: " + ", ".join(missing))
    data = {"fixture": load_json(FIXTURE), "result": load_json(RESULT), "lean": LEAN.read_text(encoding="utf-8")}
    errors = validate_against_schema(data["fixture"], load_json(FIXTURE_SCHEMA), FIXTURE.relative_to(ROOT).as_posix())
    errors.extend(validate_against_schema(data["result"], load_json(RESULT_SCHEMA), RESULT.relative_to(ROOT).as_posix()))
    errors.extend(semantic_errors(data))
    errors.extend(negative_controls(data))
    if errors:
        raise SystemExit("Inter-stack exchange validation failed:\n - " + "\n - ".join(errors))
    print("Inter-stack exchange contract passed: 9 deterministic routes, 9 owned Lean theorems, no support movement, and 11 rejecting mutations.")


if __name__ == "__main__":
    main()
