#!/usr/bin/env python3
"""Re-execute and validate the governed repository-change vertical slice."""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

from build_canonical_public_status import validate_against_schema
from run_governed_repository_change_slice import (
    RESULT,
    ROOT,
    WORKLOAD,
    deterministic_projection,
    execute_suite,
)


SCHEMA = ROOT / "schemas" / "governed_repository_change_result.schema.json"
DOC = ROOT / "docs" / "governed_repository_change_slice.md"
CHAPTER = ROOT / "chapters" / "integrated-reference-architecture.qmd"
REMEDIATION = ROOT / "docs" / "external_ai_review_remediation_program.md"
EXPECTED_SCENARIOS = {
    "nominal_valid_change",
    "retrieved_context_prompt_injection",
    "stale_authorization",
    "revocation_during_execution",
    "forged_mismatched_receipt",
    "correlated_proposer_verifier",
    "hidden_residual_cost",
    "failed_rollback",
    "cheaper_route_violates_safety_constraint",
}
EXPECTED_ATTACKS = EXPECTED_SCENARIOS - {"nominal_valid_change"}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def text_has(path: Path, fragments: list[str], errors: list[str]) -> None:
    if not path.exists():
        errors.append(f"missing required artifact: {path.relative_to(ROOT)}")
        return
    text = path.read_text(encoding="utf-8", errors="ignore")
    for fragment in fragments:
        if fragment not in text:
            errors.append(f"{path.relative_to(ROOT)} missing required fragment: {fragment!r}")


def main() -> None:
    errors: list[str] = []
    for path in (WORKLOAD, RESULT, SCHEMA, DOC, CHAPTER, REMEDIATION):
        if not path.exists():
            errors.append(f"missing required artifact: {path.relative_to(ROOT)}")
    if errors:
        fail(errors)

    workload = load_json(WORKLOAD)
    tracked = load_json(RESULT)
    schema = load_json(SCHEMA)
    errors.extend(validate_against_schema(tracked, schema, str(RESULT.relative_to(ROOT))))
    fresh = execute_suite(workload)
    if deterministic_projection(tracked) != deterministic_projection(fresh):
        errors.append(
            f"{RESULT.relative_to(ROOT)} is stale or not reproducible; run "
            "python3 scripts/run_governed_repository_change_slice.py --write-result"
        )

    rows = tracked.get("scenario_results", [])
    by_id = {row.get("scenario_id"): row for row in rows if isinstance(row, dict)}
    if set(by_id) != EXPECTED_SCENARIOS:
        errors.append(f"scenario IDs differ from required set: {sorted(set(by_id) ^ EXPECTED_SCENARIOS)}")
    baseline = tracked.get("baseline_summary", {})
    governed = tracked.get("governed_summary", {})
    expected_baseline = {
        "false_accepts": 8,
        "unsafe_releases": 8,
        "correct_dispositions": 1,
        "releases": 9,
    }
    expected_governed = {
        "false_accepts": 0,
        "false_rejects": 0,
        "unsafe_releases": 0,
        "correct_dispositions": 9,
        "releases": 3,
        "refusals": 5,
        "quarantines": 1,
        "rollback_attempts": 3,
        "exact_rollbacks": 2,
        "failed_rollbacks": 1,
    }
    for key, expected in expected_baseline.items():
        if baseline.get(key) != expected:
            errors.append(f"baseline_summary.{key} expected {expected}, got {baseline.get(key)!r}")
    for key, expected in expected_governed.items():
        if governed.get(key) != expected:
            errors.append(f"governed_summary.{key} expected {expected}, got {governed.get(key)!r}")
    if governed.get("cost_units", 0) <= baseline.get("cost_units", 0):
        errors.append("governed route must expose its additional deterministic cost units")
    if governed.get("operator_review_steps") != 9 or baseline.get("operator_review_steps") != 0:
        errors.append("matched comparison must expose governed operator burden against the zero-review baseline")
    if tracked.get("support_state_effect") != "none" or tracked.get("evidence_transition_created") is not False:
        errors.append("slice must preserve no support-state effect and create no evidence transition")
    if tracked.get("non_claims") != workload.get("required_non_claims"):
        errors.append("tracked non-claims must exactly match the workload contract")
    if not all(tracked.get("trace_invariants", {}).values()):
        errors.append("every declared trace invariant must pass")

    for scenario_id in EXPECTED_ATTACKS:
        row = by_id.get(scenario_id, {})
        governed_row = row.get("governed", {})
        if not governed_row.get("correct_disposition"):
            errors.append(f"{scenario_id}: governed disposition did not match the expected outcome")
        if governed_row.get("unsafe_release"):
            errors.append(f"{scenario_id}: governed path produced an unsafe release")
    for scenario_id in ("stale_authorization", "revocation_during_execution"):
        if not by_id.get(scenario_id, {}).get("governed", {}).get("authorization_blocked_before_effect"):
            errors.append(f"{scenario_id}: authority failure was not blocked before effect")
    forged = by_id.get("forged_mismatched_receipt", {}).get("governed", {})
    if forged.get("verification", {}).get("receipt_matches_observed_artifact") is not False:
        errors.append("forged receipt negative control was not detected by observed artifact digest")
    failed = by_id.get("failed_rollback", {}).get("governed", {})
    if failed.get("decision") != "quarantine" or failed.get("rollback_exact") is not False:
        errors.append("failed rollback must remain quarantined with rollback_exact false")
    cheaper = by_id.get("cheaper_route_violates_safety_constraint", {}).get("governed", {})
    if cheaper.get("route_id") != workload.get("safe_route", {}).get("route_id"):
        errors.append("cheaper safety-ineligible route was not rejected")

    text_has(
        DOC,
        [
            "eight named adversarial cases",
            "## Matched Comparison",
            "## Record/Reality Controls",
            "## Evidence Boundary",
            "failed rollback",
            "scripts/validate_governed_repository_change_slice.py",
        ],
        errors,
    )
    text_has(
        CHAPTER,
        [
            "Governed repository-change slice",
            "scripts/validate_governed_repository_change_slice.py",
            "no chapter-core support-state transition",
        ],
        errors,
    )
    text_has(
        REMEDIATION,
        [
            "governed_repository_change_slice",
            "eight baseline false accepts",
            "three rollback attempts",
        ],
        errors,
    )
    fail(errors)
    print(
        "Governed repository-change slice validation passed: "
        "9 executed scenarios, 8 named attacks, baseline 8 false accepts, "
        "governed 0 false accepts and 0 unsafe releases, 3 rollback attempts."
    )


def fail(errors: list[str]) -> None:
    if not errors:
        return
    print("Governed repository-change slice validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


if __name__ == "__main__":
    main()
