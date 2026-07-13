#!/usr/bin/env python3
"""Recompute the bounded model-weight custody lifecycle fixture."""

from __future__ import annotations

import copy
import hashlib
import re
from collections import Counter

from build_canonical_public_status import ROOT, load_json, validate_against_schema

FIXTURE = ROOT / "experiments/model_weight_custody_lifecycle/fixtures/cases.json"
RESULT = ROOT / "experiments/model_weight_custody_lifecycle/results/2026-07-13-local.json"
FIXTURE_SCHEMA = ROOT / "schemas/model_weight_custody_lifecycle_fixture.schema.json"
RESULT_SCHEMA = ROOT / "schemas/model_weight_custody_lifecycle_result.schema.json"
LEAN = ROOT / "lean/AsiStackProofs/ModelWeightCustody.lean"
EXPECTED_IDS = [
    "valid_observed_bounded_load", "invalid_missing_lineage",
    "invalid_missing_policy_digest", "invalid_stale_attestation",
    "invalid_undisclosed_verifier_dependencies", "invalid_unobserved_load",
    "invalid_distribution_authority_laundering",
    "valid_irreversible_distribution_record",
]
EXPECTED_THEOREMS = [
    "required_invalid_attestation_blocks_requested_load",
    "missing_lineage_requires_custody_repair", "complete_observed_load_is_bounded",
    "missing_lineage_blocks_lifecycle", "stale_attestation_requires_refresh",
    "undisclosed_verifier_dependencies_require_review",
    "unobserved_load_requires_observation",
    "distribution_cannot_launder_load_authority",
    "acknowledged_distribution_records_irreversibility",
]


def route(r: dict) -> str:
    if not r["artifact_digest_recorded"]:
        return "retain_as_draft"
    if not r["lineage_recorded"]:
        return "require_lineage_repair"
    if not r["policy_digest_recorded"] or not r["verifier_identity_recorded"] or not r["measurement_recorded"] or not r["recipient_scope_recorded"]:
        return "require_policy_review"
    if not r["expiry_recorded"] or not r["attestation_current"] or not r["attestation_valid"]:
        return "require_fresh_attestation"
    if not r["verifier_dependencies_recorded"]:
        return "require_dependency_review"
    if r["load_requested"] and not r["independent_load_observation_recorded"]:
        return "require_independent_observation"
    if not r["residual_owner_recorded"] or not r["revocation_semantics_recorded"]:
        return "require_policy_review"
    if r["distribution_requested"] and not r["no_authority_grant_recorded"]:
        return "reject_release_laundering"
    if r["distribution_requested"] and r["irreversibility_acknowledged"]:
        return "record_irreversible_release"
    if r["distribution_requested"]:
        return "reject_release_laundering"
    if r["load_requested"]:
        return "admit_bounded_load"
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
        ("wrong route", lambda d: d["fixture"]["cases"][1].__setitem__("expected_route", "admit_bounded_load")),
        ("stale-token laundering", lambda d: d["fixture"]["cases"][3]["record"].__setitem__("attestation_current", True)),
        ("load-observation laundering", lambda d: d["result"]["case_results"][5].__setitem__("actual_route", "admit_bounded_load")),
        ("release-authority laundering", lambda d: d["result"]["case_results"][6].__setitem__("actual_route", "record_irreversible_release")),
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
        raise SystemExit("missing custody lifecycle artifacts: " + ", ".join(missing))
    data = {"fixture": load_json(FIXTURE), "result": load_json(RESULT), "lean": LEAN.read_text(encoding="utf-8")}
    errors = validate_against_schema(data["fixture"], load_json(FIXTURE_SCHEMA), FIXTURE.relative_to(ROOT).as_posix())
    errors.extend(validate_against_schema(data["result"], load_json(RESULT_SCHEMA), RESULT.relative_to(ROOT).as_posix()))
    errors.extend(semantic_errors(data))
    errors.extend(negative_controls(data))
    if errors:
        raise SystemExit("Model-weight custody lifecycle validation failed:\n - " + "\n - ".join(errors))
    print("Model-weight custody lifecycle passed: 8 deterministic routes, 9 Lean theorems, no support movement, and 9 rejecting mutations.")


if __name__ == "__main__":
    main()
