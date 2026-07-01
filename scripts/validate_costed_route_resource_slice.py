#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import re
import sys
from typing import Any

from validate_protocol_examples import validate_value


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "experiments" / "costed_route_resource_slice" / "input" / "v1_0_costed_routes.json"
RESULT = ROOT / "experiments" / "costed_route_resource_slice" / "results" / "2026-06-29-local.json"
SUMMARY = ROOT / "docs" / "costed_route_resource_slice.md"
TRANSITION = (
    ROOT
    / "evidence_transitions"
    / "v1_0_measured"
    / "costed_route_resource_slice_synthetic_test_backed.json"
)
ROUTE_SCHEMA = ROOT / "schemas" / "costed_route_record.schema.json"
BUDGET_SCHEMA = ROOT / "schemas" / "resource_budget_record.schema.json"
LEAN_FIXTURE = ROOT / "lean" / "AsiStackProofs" / "ResourceEconomics.lean"

GOOD_OUTCOMES = {"adequate_minimum", "adequate_overkill"}
BAD_HIDDEN_COST_WORDS = {"failed", "missing", "unbounded", "lost"}
EXPECTED_ROUTE_COUNT = 4
EXPECTED_NEGATIVE_CONTROL_IDS = {
    "route://cheap-unverified-transform",
    "route://hidden-residual-auto-merge",
}
REQUIRED_NON_CLAIMS = (
    "does not promote any chapter core claim",
    "does not prove deployed routing",
    "does not measure model quality",
)
ROUTE_ID_TO_LEAN_CONSTRUCTOR = {
    "route://frontier-manual-review": "frontierManualReview",
    "route://bounded-transform-plus-verifier": "boundedTransformPlusVerifier",
    "route://cheap-unverified-transform": "cheapUnverifiedTransform",
    "route://hidden-residual-auto-merge": "hiddenResidualAutoMerge",
}
REQUIRED_LEAN_THEOREMS = (
    "costed_route_fixture_selected_is_eligible",
    "cheap_unverified_transform_rejected_by_fixture",
    "hidden_residual_auto_merge_rejected_by_fixture",
    "selected_route_is_lowest_cost_eligible_in_fixture",
    "costed_route_fixture_trace_selects_lowest_eligible_route",
)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Costed route/resource slice validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def text_blob(value: Any) -> str:
    if isinstance(value, list):
        return "\n".join(str(item) for item in value).lower()
    if isinstance(value, dict):
        return "\n".join(f"{key}: {child}" for key, child in value.items()).lower()
    return str(value).lower()


def total_cost(route_record: dict[str, Any]) -> float:
    accounting = route_record["cost_accounting"]
    return round(
        accounting["estimated_tokens"] / 1000
        + accounting["estimated_time_seconds"] / 60
        + accounting["tool_cost_units"] * 5,
        2,
    )


def route_is_eligible(route_record: dict[str, Any], budget_record: dict[str, Any]) -> bool:
    hidden_cost_text = text_blob(route_record.get("hidden_cost_checks", []))
    return (
        route_record.get("route_state") == "evaluated"
        and route_record.get("verification_result") == "pass"
        and route_record.get("outcome_state") in GOOD_OUTCOMES
        and route_record.get("promotion_candidate") is True
        and route_record.get("support_state_effect") == "eligible_for_bounded_evidence_review"
        and budget_record.get("budget_state") == "dispatchable"
        and budget_record.get("budget_decision") == "dispatch"
        and bool(route_record.get("fallback_route"))
        and bool(route_record.get("residual_obligations"))
        and bool(budget_record.get("residuals"))
        and not any(word in hidden_cost_text for word in BAD_HIDDEN_COST_WORDS)
    )


def rejection_reason(route_record: dict[str, Any], budget_record: dict[str, Any]) -> str:
    reasons: list[str] = []
    for key in ("route_state", "verification_result", "outcome_state", "promotion_candidate"):
        reasons.append(f"{key} {route_record.get(key)}")
    for key in ("budget_state", "budget_decision"):
        reasons.append(f"{key} {budget_record.get(key)}")
    return ", ".join(reasons)


def validate_non_claims(owner: str, non_claims: Any, errors: list[str]) -> None:
    if not isinstance(non_claims, list) or not non_claims:
        errors.append(f"{owner}: non_claims must be a non-empty list.")
        return
    blob = text_blob(non_claims)
    for phrase in REQUIRED_NON_CLAIMS:
        if phrase not in blob:
            errors.append(f"{owner}: non_claims missing boundary phrase {phrase!r}.")


def validate_summary(expected_result: dict[str, Any], errors: list[str]) -> None:
    if not SUMMARY.exists():
        errors.append(f"Missing {rel(SUMMARY)}.")
        return
    text = SUMMARY.read_text(encoding="utf-8")
    required_fragments = [
        "Costed Route Resource Slice",
        "resource-economics.costed_route_budget_slice",
        "Support transition: `argument` to `synthetic-test-backed`",
        "`route://bounded-transform-plus-verifier` | selected candidate | 14.2 | eligible",
        "`route://frontier-manual-review` | adequate overkill baseline | 43.0 | eligible",
        "`route://cheap-unverified-transform` | negative control | 2.3 | rejected",
        "`route://hidden-residual-auto-merge` | hidden-residual control | 8.2 | rejected",
        "66.98 percent cheaper",
        "Lean Fixture Bridge",
        "The command also checks that the finite Lean fixture in",
        "`AsiStackProofs.ResourceEconomics` matches the tracked JSON route costs",
        "selected route, rejection controls, and eligibility fields",
        "Does not promote any chapter core claim above `argument`.",
        "Does not prove deployed routing",
    ]
    for fragment in required_fragments:
        if fragment not in text:
            errors.append(f"{rel(SUMMARY)} missing required fragment: {fragment}")
    if expected_result["selected_route"] not in text:
        errors.append(f"{rel(SUMMARY)} does not name selected route {expected_result['selected_route']}.")


def validate_transition(expected_result: dict[str, Any], errors: list[str]) -> None:
    if not TRANSITION.exists():
        errors.append(f"Missing {rel(TRANSITION)}.")
        return
    value = load_json(TRANSITION)
    if not isinstance(value, dict):
        errors.append(f"{rel(TRANSITION)} must contain an object.")
        return
    expected = {
        "claim_id": "resource-economics.costed_route_budget_slice",
        "old_support_state": "argument",
        "new_support_state": "synthetic-test-backed",
        "transition_effect": "upward",
        "transition_validity_state": "review_accepted",
        "verification_result": "pass",
        "review_status": "accepted",
        "support_state_effect": "eligible_for_bounded_evidence_review",
    }
    for key, expected_value in expected.items():
        if value.get(key) != expected_value:
            errors.append(f"{rel(TRANSITION)}: {key} must be {expected_value!r}.")
    for ref in (rel(INPUT), rel(RESULT), rel(SUMMARY), "scripts/validate_costed_route_resource_slice.py"):
        refs = value.get("artifact_refs", []) + value.get("evidence_packet_refs", []) + value.get("claim_surface_refs", [])
        if ref not in refs:
            errors.append(f"{rel(TRANSITION)} must reference {ref}.")
    refs = value.get("artifact_refs", []) + value.get("evidence_packet_refs", []) + value.get("claim_record_refs", [])
    if rel(LEAN_FIXTURE) not in refs:
        errors.append(f"{rel(TRANSITION)} must reference {rel(LEAN_FIXTURE)}.")
    if expected_result["selected_route"] not in value.get("transition_reason", ""):
        errors.append(f"{rel(TRANSITION)} transition_reason must name selected route.")
    validate_non_claims(rel(TRANSITION), value.get("non_claims"), errors)


def lean_bool(value: bool) -> str:
    return "true" if value else "false"


def parse_lean_costed_route_fixture(errors: list[str]) -> tuple[set[str], str, dict[str, dict[str, str]]]:
    if not LEAN_FIXTURE.exists():
        errors.append(f"Missing {rel(LEAN_FIXTURE)}.")
        return set(), "", {}
    text = LEAN_FIXTURE.read_text(encoding="utf-8")

    constructor_match = re.search(
        r"inductive\s+CostedRoute\s+where(?P<body>.*?)deriving\s+DecidableEq",
        text,
        re.DOTALL,
    )
    if not constructor_match:
        errors.append(f"{rel(LEAN_FIXTURE)} is missing CostedRoute constructors.")
        constructors: set[str] = set()
    else:
        constructors = set(re.findall(r"^\s*\|\s+(\w+)\s*$", constructor_match.group("body"), re.MULTILINE))

    selected_match = re.search(
        r"def\s+CostedRouteFixtureSelected\s*:\s*CostedRoute\s*:=\s*\n\s*\.(\w+)",
        text,
    )
    selected_constructor = selected_match.group(1) if selected_match else ""
    if not selected_constructor:
        errors.append(f"{rel(LEAN_FIXTURE)} is missing CostedRouteFixtureSelected.")

    expected_theorem_set = set(REQUIRED_LEAN_THEOREMS)
    declared_theorem_set = set(re.findall(r"^theorem\s+(\w+)\b", text, re.MULTILINE))
    missing_theorems = sorted(expected_theorem_set - declared_theorem_set)
    for theorem in missing_theorems:
        errors.append(f"{rel(LEAN_FIXTURE)} missing theorem {theorem}.")

    fixture_match = re.search(
        r"def\s+costedRouteFixtureAssessment\s*:\s*CostedRoute\s*->\s*CostedRouteAssessment(?P<body>.*?)\n\ndef\s+CostedRouteFixtureSelected",
        text,
        re.DOTALL,
    )
    assessments: dict[str, dict[str, str]] = {}
    if not fixture_match:
        errors.append(f"{rel(LEAN_FIXTURE)} is missing costedRouteFixtureAssessment.")
        return constructors, selected_constructor, assessments

    for match in re.finditer(
        r"^\s*\|\s+\.(?P<constructor>\w+)\s*=>\s*\{(?P<body>.*?)(?=^\s*\|\s+\.|\Z)",
        fixture_match.group("body"),
        re.MULTILINE | re.DOTALL,
    ):
        body = match.group("body")
        fields = {
            field_match.group("field"): field_match.group("value").strip()
            for field_match in re.finditer(
                r"^\s*(?P<field>\w+)\s*:=\s*(?P<value>[^,\n}]+)",
                body,
                re.MULTILINE,
            )
        }
        assessments[match.group("constructor")] = fields
    return constructors, selected_constructor, assessments


def expected_lean_assessment(wrapper: dict[str, Any], computed_cost: float) -> dict[str, str]:
    route_id = wrapper["route_id"]
    route_record = wrapper["costed_route_record"]
    budget_record = wrapper["resource_budget_record"]
    hidden_cost_text = text_blob(route_record.get("hidden_cost_checks", []))
    hidden_residual_displaced = any(
        phrase in hidden_cost_text
        for phrase in ("missing residual ownership", "lost reviewer handoff")
    )
    residual_owned = (
        bool(route_record.get("residual_obligations"))
        and bool(budget_record.get("residuals"))
        and not hidden_residual_displaced
    )
    non_claim_text = text_blob(route_record.get("non_claims", []))
    return {
        "route": f".{ROUTE_ID_TO_LEAN_CONSTRUCTOR[route_id]}",
        "costTenths": str(int(round(computed_cost * 10))),
        "verificationPassed": lean_bool(route_record.get("verification_result") == "pass"),
        "adequateOutcome": lean_bool(route_record.get("outcome_state") in GOOD_OUTCOMES),
        "promotionCandidate": lean_bool(route_record.get("promotion_candidate") is True),
        "budgetDispatchable": lean_bool(
            budget_record.get("budget_state") == "dispatchable"
            and budget_record.get("budget_decision") == "dispatch"
        ),
        "residualOwned": lean_bool(residual_owned),
        "hiddenCostDisplaced": lean_bool(hidden_residual_displaced),
        "fallbackVisible": lean_bool(bool(route_record.get("fallback_route"))),
        "nonClaimBoundary": lean_bool(all(phrase in non_claim_text for phrase in REQUIRED_NON_CLAIMS)),
    }


def validate_lean_fixture_alignment(
    routes: list[dict[str, Any]],
    result: dict[str, Any],
    computed_costs: dict[str, float],
    errors: list[str],
) -> dict[str, Any]:
    constructors, selected_constructor, assessments = parse_lean_costed_route_fixture(errors)
    expected_constructors = set(ROUTE_ID_TO_LEAN_CONSTRUCTOR.values())
    if constructors != expected_constructors:
        errors.append(
            f"{rel(LEAN_FIXTURE)} CostedRoute constructors must be {sorted(expected_constructors)!r}, got {sorted(constructors)!r}."
        )
    expected_selected_constructor = ROUTE_ID_TO_LEAN_CONSTRUCTOR.get(result.get("selected_route"))
    if selected_constructor != expected_selected_constructor:
        errors.append(
            f"{rel(LEAN_FIXTURE)} selected constructor must be {expected_selected_constructor!r}, got {selected_constructor!r}."
        )

    for wrapper in routes:
        if not isinstance(wrapper, dict):
            continue
        route_id = wrapper.get("route_id")
        if route_id not in ROUTE_ID_TO_LEAN_CONSTRUCTOR:
            continue
        if not isinstance(wrapper.get("costed_route_record"), dict) or not isinstance(
            wrapper.get("resource_budget_record"), dict
        ):
            continue
        constructor = ROUTE_ID_TO_LEAN_CONSTRUCTOR[route_id]
        fields = assessments.get(constructor)
        if fields is None:
            errors.append(f"{rel(LEAN_FIXTURE)} missing fixture assessment for .{constructor}.")
            continue
        expected_fields = expected_lean_assessment(wrapper, computed_costs[route_id])
        for field, expected_value in expected_fields.items():
            if fields.get(field) != expected_value:
                errors.append(
                    f"{rel(LEAN_FIXTURE)} .{constructor}.{field} must be {expected_value!r}, got {fields.get(field)!r}."
                )

    expected_alignment = {
        "lean_module": rel(LEAN_FIXTURE),
        "checked_constructor_count": EXPECTED_ROUTE_COUNT,
        "selected_constructor": expected_selected_constructor,
        "route_constructors": dict(sorted(ROUTE_ID_TO_LEAN_CONSTRUCTOR.items())),
        "checked_theorem_names": list(REQUIRED_LEAN_THEOREMS),
    }
    if result.get("lean_fixture_alignment") != expected_alignment:
        errors.append(f"{rel(RESULT)}: lean_fixture_alignment must equal {expected_alignment!r}.")
    return expected_alignment


def main() -> None:
    route_schema = load_json(ROUTE_SCHEMA)
    budget_schema = load_json(BUDGET_SCHEMA)
    data = load_json(INPUT)
    result = load_json(RESULT)
    errors: list[str] = []

    if not isinstance(data, dict):
        fail([f"{rel(INPUT)} must contain an object."])
    if not isinstance(result, dict):
        fail([f"{rel(RESULT)} must contain an object."])

    routes = data.get("routes")
    if not isinstance(routes, list) or len(routes) != EXPECTED_ROUTE_COUNT:
        errors.append(f"{rel(INPUT)}: routes must contain exactly {EXPECTED_ROUTE_COUNT} records.")
        routes = []

    route_ids: list[str] = []
    computed_costs: dict[str, float] = {}
    eligible_routes: list[str] = []
    rejected_routes: list[dict[str, str]] = []

    for index, wrapper in enumerate(routes):
        owner = f"{rel(INPUT)}:routes[{index}]"
        if not isinstance(wrapper, dict):
            errors.append(f"{owner} must be an object.")
            continue
        route_id = wrapper.get("route_id")
        route_record = wrapper.get("costed_route_record")
        budget_record = wrapper.get("resource_budget_record")
        if not isinstance(route_id, str) or not route_id:
            errors.append(f"{owner}: route_id must be a non-empty string.")
            continue
        if route_id in route_ids:
            errors.append(f"{owner}: duplicate route_id {route_id}.")
        route_ids.append(route_id)
        if not isinstance(route_record, dict):
            errors.append(f"{owner}: costed_route_record must be an object.")
            continue
        if not isinstance(budget_record, dict):
            errors.append(f"{owner}: resource_budget_record must be an object.")
            continue
        errors.extend(validate_value(route_record, route_schema, f"{owner}.costed_route_record"))
        errors.extend(validate_value(budget_record, budget_schema, f"{owner}.resource_budget_record"))
        if route_record.get("selected_route") != route_id:
            errors.append(f"{owner}: selected_route must match route_id.")
        if budget_record.get("task_id") != route_id:
            errors.append(f"{owner}: resource_budget_record.task_id must match route_id.")
        validate_non_claims(f"{owner}.costed_route_record", route_record.get("non_claims"), errors)
        computed_costs[route_id] = total_cost(route_record)
        if route_is_eligible(route_record, budget_record):
            eligible_routes.append(route_id)
        else:
            rejected_routes.append({"route_id": route_id, "reason": rejection_reason(route_record, budget_record)})

    expected_route_set = set(route_ids)
    for wrapper in routes:
        if not isinstance(wrapper, dict) or not isinstance(wrapper.get("costed_route_record"), dict):
            continue
        candidate_routes = set(str(item) for item in wrapper["costed_route_record"].get("candidate_routes", []))
        if candidate_routes != expected_route_set:
            errors.append(f"{wrapper.get('route_id')}: candidate_routes must list exactly all slice route ids.")

    expected_selected = data.get("expected_selected_route")
    baseline = data.get("baseline_route_id")
    negative_control = data.get("negative_control_route_id")
    negative_controls = data.get("negative_control_route_ids")
    if not isinstance(expected_selected, str) or expected_selected not in computed_costs:
        errors.append("expected_selected_route must name one route.")
    if not isinstance(baseline, str) or baseline not in computed_costs:
        errors.append("baseline_route_id must name one route.")
    if not isinstance(negative_control, str) or negative_control not in computed_costs:
        errors.append("negative_control_route_id must name one route.")
    if not isinstance(negative_controls, list) or set(negative_controls) != EXPECTED_NEGATIVE_CONTROL_IDS:
        errors.append(
            "negative_control_route_ids must name the cheap failed and hidden-residual negative controls."
        )
        negative_controls = []
    else:
        for route_id in negative_controls:
            if route_id not in computed_costs:
                errors.append(f"negative_control_route_ids includes unknown route {route_id}.")

    if eligible_routes:
        selected = min(eligible_routes, key=lambda route_id: (computed_costs[route_id], route_id))
    else:
        selected = ""
        errors.append("At least one route must be eligible.")

    eligible_routes_sorted = sorted(eligible_routes)
    rejected_routes_sorted = sorted(rejected_routes, key=lambda row: row["route_id"])
    if selected != expected_selected:
        errors.append(f"Selected route {selected!r} does not match expected_selected_route {expected_selected!r}.")
    if baseline and baseline not in eligible_routes:
        errors.append("Baseline route must remain eligible so the slice has an adequate overkill comparison.")
    if negative_control and negative_control not in {row["route_id"] for row in rejected_routes}:
        errors.append("Negative control route must be rejected.")
    rejected_route_ids = {row["route_id"] for row in rejected_routes}
    for route_id in negative_controls:
        if route_id not in rejected_route_ids:
            errors.append(f"Negative control route {route_id} must be rejected.")
    if selected and baseline:
        reduction = round(((computed_costs[baseline] - computed_costs[selected]) / computed_costs[baseline]) * 100, 2)
    else:
        reduction = 0.0
    if reduction < 50:
        errors.append("Selected route must be at least 50 percent cheaper than baseline in this slice.")

    expected_result = {
        "selected_route": selected,
        "baseline_route": baseline,
        "negative_control_route": negative_control,
        "negative_control_routes": sorted(str(route_id) for route_id in negative_controls),
        "eligible_routes": eligible_routes_sorted,
        "rejected_routes": rejected_routes_sorted,
        "computed_cost_units": dict(sorted(computed_costs.items())),
        "cost_reduction_vs_baseline_percent": reduction,
    }
    validate_lean_fixture_alignment(routes, result, computed_costs, errors)

    for key, expected_value in expected_result.items():
        if result.get(key) != expected_value:
            errors.append(f"{rel(RESULT)}: {key} must equal {expected_value!r}.")
    if result.get("slice_id") != data.get("slice_id"):
        errors.append(f"{rel(RESULT)}: slice_id must match input.")
    if result.get("input_ref") != rel(INPUT):
        errors.append(f"{rel(RESULT)}: input_ref must be {rel(INPUT)!r}.")
    if result.get("verification_result") != "pass":
        errors.append(f"{rel(RESULT)}: verification_result must be pass.")
    if result.get("support_state_effect") != "eligible_for_bounded_evidence_review":
        errors.append(f"{rel(RESULT)}: support_state_effect must be eligible_for_bounded_evidence_review.")
    validate_non_claims(rel(INPUT), data.get("non_claims"), errors)
    validate_non_claims(rel(RESULT), result.get("non_claims"), errors)

    validate_summary(result, errors)
    validate_transition(result, errors)

    if errors:
        fail(errors)

    print(
        "Costed route/resource slice validation passed: "
        f"selected {selected}, baseline {baseline}, negative controls {', '.join(expected_result['negative_control_routes'])}, "
        f"{reduction:.2f}% synthetic cost reduction; Lean fixture aligned."
    )


if __name__ == "__main__":
    main()
