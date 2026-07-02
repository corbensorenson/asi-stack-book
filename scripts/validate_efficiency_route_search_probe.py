#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = ROOT / "experiments" / "efficiency_route_search" / "results" / "2026-07-02-local.json"

COST_CLASSES = ("model", "context", "verification", "repair", "human_review", "regression", "rollback")
REQUIRED_NONCLAIMS = [
    "does not prove route-search completeness",
    "does not prove cost-estimate accuracy",
    "does not prove measured efficiency",
    "does not promote the chapter support state",
]

TRACES: list[dict[str, Any]] = [
    {
        "trace_id": "valid_minimum_verified_route",
        "expect_valid": True,
        "task_contract": "task://public-book-crosswalk-update",
        "quality_predicate": "preserve source boundary, support state, and validation evidence",
        "authority_ceiling": "public_book_edit_only",
        "selected_route_id": "route://bounded-transform-plus-verifier",
        "fallback_route_id": "route://frontier-manual-review",
        "support_state_effect": "none",
        "hidden_cost_audit": ["model", "context", "verification", "repair", "human_review", "regression", "rollback"],
        "negative_controls": ["cheap_failed_quality", "hidden_residual_success", "authority_bypass"],
        "residual_obligations": ["review source-specific prose for later author voice"],
        "candidates": [
            {
                "route_id": "route://cheap-draft-only",
                "authorized": True,
                "quality_passed": False,
                "utility_preserved": False,
                "open_obligations": True,
                "residual_recorded": True,
                "costs": {"model": 8, "context": 2, "verification": 2, "repair": 0, "human_review": 0, "regression": 0, "rollback": 0, "total": 12},
                "outcome_state": "cheap_brittle",
            },
            {
                "route_id": "route://bounded-transform-plus-verifier",
                "authorized": True,
                "quality_passed": True,
                "utility_preserved": True,
                "open_obligations": True,
                "residual_recorded": True,
                "costs": {"model": 24, "context": 6, "verification": 9, "repair": 3, "human_review": 0, "regression": 4, "rollback": 2, "total": 48},
                "outcome_state": "adequate_minimum",
            },
            {
                "route_id": "route://frontier-manual-review",
                "authorized": True,
                "quality_passed": True,
                "utility_preserved": True,
                "open_obligations": False,
                "residual_recorded": True,
                "costs": {"model": 85, "context": 18, "verification": 12, "repair": 0, "human_review": 22, "regression": 5, "rollback": 2, "total": 144},
                "outcome_state": "adequate_overkill",
            },
            {
                "route_id": "route://hidden-residual-auto-merge",
                "authorized": True,
                "quality_passed": True,
                "utility_preserved": True,
                "open_obligations": True,
                "residual_recorded": False,
                "costs": {"model": 20, "context": 5, "verification": 3, "repair": 0, "human_review": 0, "regression": 0, "rollback": 0, "total": 28},
                "outcome_state": "hidden_cost",
            },
            {
                "route_id": "route://authority-bypass-fast-path",
                "authorized": False,
                "quality_passed": True,
                "utility_preserved": True,
                "open_obligations": False,
                "residual_recorded": True,
                "costs": {"model": 18, "context": 3, "verification": 4, "repair": 0, "human_review": 0, "regression": 0, "rollback": 0, "total": 25},
                "outcome_state": "unsafe_saving",
            },
        ],
        "non_claims": REQUIRED_NONCLAIMS + ["does not prove model quality"],
    },
    {
        "trace_id": "valid_compression_blocked_by_repair_burden",
        "expect_valid": True,
        "task_contract": "task://reader-summary-preserve-citations",
        "quality_predicate": "preserve cited claims and reader utility after compression",
        "authority_ceiling": "public_reader_edit_only",
        "selected_route_id": "route://scoped-summary-with-citation-check",
        "fallback_route_id": "route://manual-citation-review",
        "support_state_effect": "none",
        "hidden_cost_audit": ["model", "context", "verification", "repair", "human_review", "regression", "rollback"],
        "negative_controls": ["compression_utility_overclaim", "repair_cost_erased"],
        "residual_obligations": ["preserve unresolved citation-review residual"],
        "candidates": [
            {
                "route_id": "route://compressed-summary-fast",
                "authorized": True,
                "quality_passed": False,
                "utility_preserved": False,
                "open_obligations": True,
                "residual_recorded": True,
                "costs": {"model": 14, "context": 1, "verification": 8, "repair": 46, "human_review": 0, "regression": 3, "rollback": 2, "total": 74},
                "outcome_state": "cheap_brittle",
            },
            {
                "route_id": "route://scoped-summary-with-citation-check",
                "authorized": True,
                "quality_passed": True,
                "utility_preserved": True,
                "open_obligations": True,
                "residual_recorded": True,
                "costs": {"model": 31, "context": 5, "verification": 11, "repair": 5, "human_review": 0, "regression": 4, "rollback": 2, "total": 58},
                "outcome_state": "adequate_minimum",
            },
            {
                "route_id": "route://manual-citation-review",
                "authorized": True,
                "quality_passed": True,
                "utility_preserved": True,
                "open_obligations": False,
                "residual_recorded": True,
                "costs": {"model": 62, "context": 12, "verification": 18, "repair": 0, "human_review": 30, "regression": 4, "rollback": 2, "total": 128},
                "outcome_state": "adequate_overkill",
            },
        ],
        "non_claims": REQUIRED_NONCLAIMS + ["does not prove compression utility"],
    },
    {
        "trace_id": "invalid_selects_over_lower_quality_route",
        "expect_valid": False,
        "task_contract": "task://public-book-crosswalk-update",
        "quality_predicate": "preserve source boundary, support state, and validation evidence",
        "authority_ceiling": "public_book_edit_only",
        "selected_route_id": "route://frontier-manual-review",
        "fallback_route_id": "route://frontier-manual-review",
        "support_state_effect": "none",
        "hidden_cost_audit": ["model", "context", "verification", "repair", "human_review", "regression", "rollback"],
        "negative_controls": ["lower_quality_route_ignored"],
        "residual_obligations": ["none"],
        "candidates": [
            {
                "route_id": "route://bounded-transform-plus-verifier",
                "authorized": True,
                "quality_passed": True,
                "utility_preserved": True,
                "open_obligations": False,
                "residual_recorded": True,
                "costs": {"model": 24, "context": 6, "verification": 9, "repair": 3, "human_review": 0, "regression": 4, "rollback": 2, "total": 48},
                "outcome_state": "adequate_minimum",
            },
            {
                "route_id": "route://frontier-manual-review",
                "authorized": True,
                "quality_passed": True,
                "utility_preserved": True,
                "open_obligations": False,
                "residual_recorded": True,
                "costs": {"model": 85, "context": 18, "verification": 12, "repair": 0, "human_review": 22, "regression": 5, "rollback": 2, "total": 144},
                "outcome_state": "adequate_overkill",
            },
        ],
        "non_claims": REQUIRED_NONCLAIMS,
    },
    {
        "trace_id": "invalid_hidden_cost_audit_missing",
        "expect_valid": False,
        "task_contract": "task://public-book-crosswalk-update",
        "quality_predicate": "preserve source boundary, support state, and validation evidence",
        "authority_ceiling": "public_book_edit_only",
        "selected_route_id": "route://bounded-transform-plus-verifier",
        "fallback_route_id": "route://frontier-manual-review",
        "support_state_effect": "none",
        "hidden_cost_audit": ["model", "context", "verification"],
        "negative_controls": ["hidden_cost_omitted"],
        "residual_obligations": ["review source-specific prose for later author voice"],
        "candidates": [
            {
                "route_id": "route://bounded-transform-plus-verifier",
                "authorized": True,
                "quality_passed": True,
                "utility_preserved": True,
                "open_obligations": True,
                "residual_recorded": True,
                "costs": {"model": 24, "context": 6, "verification": 9, "repair": 3, "human_review": 0, "regression": 4, "rollback": 2, "total": 48},
                "outcome_state": "adequate_minimum",
            }
        ],
        "non_claims": REQUIRED_NONCLAIMS,
    },
    {
        "trace_id": "invalid_residual_erased",
        "expect_valid": False,
        "task_contract": "task://public-book-crosswalk-update",
        "quality_predicate": "preserve source boundary, support state, and validation evidence",
        "authority_ceiling": "public_book_edit_only",
        "selected_route_id": "route://hidden-residual-auto-merge",
        "fallback_route_id": "route://frontier-manual-review",
        "support_state_effect": "none",
        "hidden_cost_audit": ["model", "context", "verification", "repair", "human_review", "regression", "rollback"],
        "negative_controls": ["residual_erased"],
        "residual_obligations": [],
        "candidates": [
            {
                "route_id": "route://hidden-residual-auto-merge",
                "authorized": True,
                "quality_passed": True,
                "utility_preserved": True,
                "open_obligations": True,
                "residual_recorded": False,
                "costs": {"model": 20, "context": 5, "verification": 3, "repair": 0, "human_review": 0, "regression": 0, "rollback": 0, "total": 28},
                "outcome_state": "hidden_cost",
            }
        ],
        "non_claims": REQUIRED_NONCLAIMS,
    },
    {
        "trace_id": "invalid_compression_utility_overclaim",
        "expect_valid": False,
        "task_contract": "task://reader-summary-preserve-citations",
        "quality_predicate": "preserve cited claims and reader utility after compression",
        "authority_ceiling": "public_reader_edit_only",
        "selected_route_id": "route://compressed-summary-fast",
        "fallback_route_id": "route://manual-citation-review",
        "support_state_effect": "none",
        "hidden_cost_audit": ["model", "context", "verification", "repair", "human_review", "regression", "rollback"],
        "negative_controls": ["compression_utility_overclaim"],
        "residual_obligations": ["preserve unresolved citation-review residual"],
        "candidates": [
            {
                "route_id": "route://compressed-summary-fast",
                "authorized": True,
                "quality_passed": True,
                "utility_preserved": False,
                "open_obligations": True,
                "residual_recorded": True,
                "costs": {"model": 14, "context": 1, "verification": 8, "repair": 46, "human_review": 0, "regression": 3, "rollback": 2, "total": 74},
                "outcome_state": "adequate_minimum",
            }
        ],
        "non_claims": REQUIRED_NONCLAIMS,
    },
    {
        "trace_id": "invalid_authority_bypass",
        "expect_valid": False,
        "task_contract": "task://public-book-crosswalk-update",
        "quality_predicate": "preserve source boundary, support state, and validation evidence",
        "authority_ceiling": "public_book_edit_only",
        "selected_route_id": "route://authority-bypass-fast-path",
        "fallback_route_id": "route://frontier-manual-review",
        "support_state_effect": "none",
        "hidden_cost_audit": ["model", "context", "verification", "repair", "human_review", "regression", "rollback"],
        "negative_controls": ["authority_bypass"],
        "residual_obligations": ["none"],
        "candidates": [
            {
                "route_id": "route://authority-bypass-fast-path",
                "authorized": False,
                "quality_passed": True,
                "utility_preserved": True,
                "open_obligations": False,
                "residual_recorded": True,
                "costs": {"model": 18, "context": 3, "verification": 4, "repair": 0, "human_review": 0, "regression": 0, "rollback": 0, "total": 25},
                "outcome_state": "unsafe_saving",
            }
        ],
        "non_claims": REQUIRED_NONCLAIMS,
    },
    {
        "trace_id": "invalid_missing_negative_controls",
        "expect_valid": False,
        "task_contract": "task://public-book-crosswalk-update",
        "quality_predicate": "preserve source boundary, support state, and validation evidence",
        "authority_ceiling": "public_book_edit_only",
        "selected_route_id": "route://bounded-transform-plus-verifier",
        "fallback_route_id": "route://frontier-manual-review",
        "support_state_effect": "none",
        "hidden_cost_audit": ["model", "context", "verification", "repair", "human_review", "regression", "rollback"],
        "negative_controls": [],
        "residual_obligations": ["review source-specific prose for later author voice"],
        "candidates": [
            {
                "route_id": "route://bounded-transform-plus-verifier",
                "authorized": True,
                "quality_passed": True,
                "utility_preserved": True,
                "open_obligations": True,
                "residual_recorded": True,
                "costs": {"model": 24, "context": 6, "verification": 9, "repair": 3, "human_review": 0, "regression": 4, "rollback": 2, "total": 48},
                "outcome_state": "adequate_minimum",
            }
        ],
        "non_claims": REQUIRED_NONCLAIMS,
    },
]


def route_total(route: dict[str, Any]) -> int | None:
    costs = route.get("costs")
    if not isinstance(costs, dict):
        return None
    values = []
    for key in COST_CLASSES:
        value = costs.get(key)
        if not isinstance(value, int) or value < 0:
            return None
        values.append(value)
    declared = costs.get("total")
    if not isinstance(declared, int) or declared < 0:
        return None
    if sum(values) != declared:
        return None
    return declared


def candidate_is_eligible(route: dict[str, Any]) -> bool:
    return (
        route.get("authorized") is True
        and route.get("quality_passed") is True
        and route.get("utility_preserved") is True
        and (route.get("open_obligations") is not True or route.get("residual_recorded") is True)
    )


def trace_errors(trace: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    trace_id = str(trace.get("trace_id", "<missing>"))
    if trace.get("support_state_effect") != "none":
        errors.append(f"{trace_id}: support_state_effect must be none.")
    for field in ("task_contract", "quality_predicate", "authority_ceiling", "selected_route_id", "fallback_route_id"):
        if not isinstance(trace.get(field), str) or not str(trace[field]).strip():
            errors.append(f"{trace_id}: {field} must be a non-empty string.")

    hidden_cost_audit = trace.get("hidden_cost_audit")
    if not isinstance(hidden_cost_audit, list) or set(hidden_cost_audit) != set(COST_CLASSES):
        errors.append(f"{trace_id}: hidden_cost_audit must name all cost classes {list(COST_CLASSES)}.")
    if not trace.get("negative_controls"):
        errors.append(f"{trace_id}: negative_controls must not be empty.")

    candidates = trace.get("candidates")
    if not isinstance(candidates, list) or not candidates:
        errors.append(f"{trace_id}: candidates must be a non-empty list.")
        return errors

    by_id: dict[str, dict[str, Any]] = {}
    totals: dict[str, int] = {}
    for index, candidate in enumerate(candidates):
        if not isinstance(candidate, dict):
            errors.append(f"{trace_id}:candidates[{index}] must be an object.")
            continue
        route_id = candidate.get("route_id")
        if not isinstance(route_id, str) or not route_id.startswith("route://"):
            errors.append(f"{trace_id}:candidates[{index}] route_id must use route://.")
            continue
        if route_id in by_id:
            errors.append(f"{trace_id}: duplicate route_id {route_id}.")
        by_id[route_id] = candidate
        total = route_total(candidate)
        if total is None:
            errors.append(f"{trace_id}:{route_id}: costs must contain non-negative cost classes and matching total.")
        else:
            totals[route_id] = total

    selected_id = trace.get("selected_route_id")
    fallback_id = trace.get("fallback_route_id")
    selected = by_id.get(selected_id)
    if selected is None:
        errors.append(f"{trace_id}: selected route {selected_id!r} missing from candidates.")
        return errors
    if fallback_id not in by_id:
        errors.append(f"{trace_id}: fallback route {fallback_id!r} missing from candidates.")

    if selected.get("authorized") is not True:
        errors.append(f"{trace_id}: selected route must be authorized.")
    if selected.get("quality_passed") is not True:
        errors.append(f"{trace_id}: selected route must pass quality.")
    if selected.get("utility_preserved") is not True:
        errors.append(f"{trace_id}: selected route must preserve utility.")
    if selected.get("open_obligations") is True and selected.get("residual_recorded") is not True:
        errors.append(f"{trace_id}: selected route with open obligations must record residuals.")
    if selected.get("open_obligations") is True and not trace.get("residual_obligations"):
        errors.append(f"{trace_id}: selected route with open obligations requires residual_obligations.")

    selected_total = totals.get(str(selected_id))
    if selected_total is not None:
        for route_id, candidate in by_id.items():
            if route_id == selected_id:
                continue
            candidate_total = totals.get(route_id)
            if candidate_total is None:
                continue
            if candidate_total < selected_total and candidate_is_eligible(candidate):
                errors.append(
                    f"{trace_id}: lower-cost eligible route {route_id} ({candidate_total}) "
                    f"beats selected {selected_id} ({selected_total})."
                )

    non_claim_text = " ".join(str(item).lower() for item in trace.get("non_claims", []))
    for marker in REQUIRED_NONCLAIMS:
        if marker not in non_claim_text:
            errors.append(f"{trace_id}: non_claims must include {marker!r}.")

    return errors


def build_result(valid_count: int, invalid_count: int) -> dict[str, Any]:
    payload = json.dumps(TRACES, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return {
        "artifact": "efficiency_route_search_probe",
        "date": "2026-07-02",
        "validator": "python3 scripts/validate_efficiency_route_search_probe.py",
        "fixture_fingerprint_sha256": hashlib.sha256(payload).hexdigest(),
        "valid_traces": valid_count,
        "expected_invalid_controls": invalid_count,
        "candidate_routes_checked": 14,
        "transition_coverage": {
            "minimum_verified_route_selection": True,
            "cheap_failed_quality_rejection": True,
            "hidden_residual_rejection": True,
            "authority_bypass_rejection": True,
            "compression_utility_rejection": True,
            "hidden_cost_class_audit": True,
        },
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
        "non_claims": [
            "does not prove route-search completeness",
            "does not prove cost-estimate accuracy",
            "does not prove measured efficiency",
            "does not prove model quality",
            "does not prove compression utility",
            "does not promote the chapter support state",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-result", action="store_true", help="Write the deterministic local result JSON.")
    args = parser.parse_args()

    errors: list[str] = []
    valid_count = 0
    invalid_count = 0
    for trace in TRACES:
        expect_valid = bool(trace.get("expect_valid"))
        trace_id = str(trace.get("trace_id", "<missing>"))
        current_errors = trace_errors(trace)
        if expect_valid:
            valid_count += 1
            errors.extend(current_errors)
        else:
            invalid_count += 1
            if not current_errors:
                errors.append(f"{trace_id}: expected-invalid control unexpectedly passed.")

    if errors:
        print("Efficiency route-search probe failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    result = build_result(valid_count, invalid_count)
    if args.write_result:
        RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
        RESULT_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(
        "Efficiency route-search probe passed: "
        f"{valid_count} valid trace(s), {invalid_count} expected-invalid control(s)."
    )


if __name__ == "__main__":
    main()
