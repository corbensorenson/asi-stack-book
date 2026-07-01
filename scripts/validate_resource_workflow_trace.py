#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "experiments" / "resource_workflow_trace" / "fixtures"
RESULT = ROOT / "experiments" / "resource_workflow_trace" / "results" / "2026-07-01-local.json"
SUMMARY = ROOT / "docs" / "resource_workflow_trace.md"
LEAN_FIXTURE = ROOT / "lean" / "AsiStackProofs" / "ResourceEconomics.lean"

HIGH_RISK = {"high", "critical"}
SUPPORTED_TRANSFER_DECISIONS = {"scenario_only", "unit_fixture_only", "bounded_claim_transport"}
SUPPORTED_FIDELITY = {"toy_model", "unit_fixture", "scenario_only"}
NON_CLAIM_TERMS = ("does not promote", "does not prove", "scheduler")
REQUIRED_LEAN_THEOREMS = (
    "resource_workflow_trace_fixture_valid",
    "resource_workflow_trace_fixture_preserves_high_risk_ordering",
    "resource_workflow_trace_fixture_residualizes_displaced_costs",
    "resource_workflow_trace_fixture_rejects_physical_feasibility_overclaim",
    "resource_workflow_trace_fixture_rejects_latency_only_selection",
    "resource_workflow_trace_fixture_has_no_support_promotion",
)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Resource workflow trace validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def text_blob(value: Any) -> str:
    if isinstance(value, dict):
        return "\n".join(f"{key}: {text_blob(child)}" for key, child in value.items()).lower()
    if isinstance(value, list):
        return "\n".join(text_blob(item) for item in value).lower()
    return str(value).lower()


def require_string(record: dict[str, Any], key: str, errors: list[str], owner: str) -> str:
    value = record.get(key)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{owner}: {key} must be a non-empty string.")
        return ""
    return value


def require_list(record: dict[str, Any], key: str, errors: list[str], owner: str) -> list[Any]:
    value = record.get(key)
    if not isinstance(value, list) or not value:
        errors.append(f"{owner}: {key} must be a non-empty list.")
        return []
    return value


def route_cost(route: dict[str, Any]) -> float:
    return round(
        float(route.get("estimated_tokens", 0)) / 1000
        + float(route.get("estimated_seconds", 0)) / 60
        + float(route.get("tool_cost_units", 0)) * 5
        + float(route.get("review_minutes", 0)) * 2
        + float(route.get("verification_minutes", 0)) * 1.5,
        2,
    )


def route_is_eligible(route: dict[str, Any], risk_class: str) -> bool:
    residual_text = text_blob(route.get("residuals", []))
    displaced_text = text_blob(route.get("displaced_costs", []))
    overhead_text = text_blob(route.get("protected_overhead", []))
    non_claim_text = text_blob(route.get("non_claims", []))
    has_displaced_cost = bool(route.get("displaced_costs"))
    displaced_cost_bounded = (
        not has_displaced_cost
        or any(term in residual_text for term in ("bounded", "measured", "residual", "accepted evidence"))
    )
    high_risk_overhead_ok = risk_class not in HIGH_RISK or (
        float(route.get("review_minutes", 0)) > 0
        and float(route.get("verification_minutes", 0)) > 0
        and any(term in overhead_text for term in ("approval", "audit", "rollback", "human review", "security"))
    )
    return (
        route.get("verification_result") == "pass"
        and route.get("quality_result") == "pass"
        and route.get("budget_decision") == "dispatch"
        and bool(route.get("quality_predicate"))
        and bool(route.get("protected_overhead"))
        and displaced_cost_bounded
        and high_risk_overhead_ok
        and all(term in non_claim_text for term in NON_CLAIM_TERMS)
    )


def validate_route_shape(route: dict[str, Any], errors: list[str], owner: str) -> None:
    for key in (
        "route_id",
        "quality_predicate",
        "verification_result",
        "quality_result",
        "budget_decision",
    ):
        require_string(route, key, errors, owner)
    for key in (
        "estimated_tokens",
        "estimated_seconds",
        "tool_cost_units",
        "review_minutes",
        "verification_minutes",
    ):
        value = route.get(key)
        if not isinstance(value, (int, float)) or isinstance(value, bool) or value < 0:
            errors.append(f"{owner}: {key} must be a non-negative number.")
    for key in ("protected_overhead", "displaced_costs", "residuals", "non_claims"):
        value = route.get(key)
        if not isinstance(value, list):
            errors.append(f"{owner}: {key} must be a list.")


def summarize_valid_trace(value: dict[str, Any], errors: list[str], owner: str) -> dict[str, Any]:
    trace_id = require_string(value, "trace_id", errors, owner)
    non_claims = require_list(value, "non_claims", errors, owner)
    non_claim_text = text_blob(non_claims)
    for term in NON_CLAIM_TERMS:
        if term not in non_claim_text:
            errors.append(f"{owner}: top-level non_claims missing {term!r}.")

    workload = value.get("workload")
    if not isinstance(workload, dict):
        errors.append(f"{owner}: workload must be an object.")
        workload = {}
    capacity = workload.get("capacity_budget")
    if not isinstance(capacity, dict):
        errors.append(f"{owner}: workload.capacity_budget must be an object.")
        capacity = {}
    for key in ("tokens", "seconds", "tool_units", "review_minutes", "verification_minutes"):
        if not isinstance(capacity.get(key), (int, float)) or isinstance(capacity.get(key), bool):
            errors.append(f"{owner}: capacity_budget.{key} must be numeric.")

    steps = require_list(value, "steps", errors, owner)
    selected_routes: dict[str, dict[str, Any]] = {}
    route_costs: dict[str, float] = {}
    route_eligibility: dict[str, bool] = {}
    high_risk_steps: set[str] = set()
    totals = {
        "tokens": 0.0,
        "seconds": 0.0,
        "tool_units": 0.0,
        "review_minutes": 0.0,
        "verification_minutes": 0.0,
        "cost_units": 0.0,
    }

    for index, step in enumerate(steps):
        step_owner = f"{owner}:steps[{index}]"
        if not isinstance(step, dict):
            errors.append(f"{step_owner}: step must be an object.")
            continue
        step_id = require_string(step, "step_id", errors, step_owner)
        risk_class = require_string(step, "risk_class", errors, step_owner)
        decision = require_string(step, "scheduler_decision", errors, step_owner)
        selected_route_id = require_string(step, "selected_route", errors, step_owner)
        if risk_class in HIGH_RISK:
            high_risk_steps.add(step_id)
        if decision != "dispatch":
            errors.append(f"{step_owner}: this trace currently supports dispatch decisions only.")
        route_candidates = require_list(step, "route_candidates", errors, step_owner)
        candidates: dict[str, dict[str, Any]] = {}
        for route_index, route in enumerate(route_candidates):
            route_owner = f"{step_owner}:route_candidates[{route_index}]"
            if not isinstance(route, dict):
                errors.append(f"{route_owner}: route must be an object.")
                continue
            validate_route_shape(route, errors, route_owner)
            route_id = str(route.get("route_id", ""))
            candidates[route_id] = route
            route_costs[route_id] = route_cost(route)
            route_eligibility[route_id] = route_is_eligible(route, risk_class)
        selected = candidates.get(selected_route_id)
        if selected is None:
            errors.append(f"{step_owner}: selected_route {selected_route_id!r} is not a candidate.")
            continue
        if not route_is_eligible(selected, risk_class):
            errors.append(f"{step_owner}: selected route {selected_route_id!r} is not eligible.")
        eligible_costs = {
            route_id: route_cost(route)
            for route_id, route in candidates.items()
            if route_is_eligible(route, risk_class)
        }
        if eligible_costs:
            minimum = min(eligible_costs.values())
            if route_cost(selected) != minimum:
                errors.append(
                    f"{step_owner}: selected route {selected_route_id!r} is not the lowest-cost eligible route."
                )
        selected_routes[step_id] = selected
        totals["tokens"] += float(selected.get("estimated_tokens", 0))
        totals["seconds"] += float(selected.get("estimated_seconds", 0))
        totals["tool_units"] += float(selected.get("tool_cost_units", 0))
        totals["review_minutes"] += float(selected.get("review_minutes", 0))
        totals["verification_minutes"] += float(selected.get("verification_minutes", 0))
        totals["cost_units"] += route_cost(selected)

    scheduler_trace = require_list(value, "scheduler_trace", errors, owner)
    seen_steps: set[str] = set()
    low_before_high = False
    high_seen = False
    for index, event in enumerate(scheduler_trace):
        event_owner = f"{owner}:scheduler_trace[{index}]"
        if not isinstance(event, dict):
            errors.append(f"{event_owner}: event must be an object.")
            continue
        step_id = require_string(event, "step_id", errors, event_owner)
        route_id = require_string(event, "selected_route", errors, event_owner)
        seen_steps.add(step_id)
        selected = selected_routes.get(step_id)
        if selected is not None and selected.get("route_id") != route_id:
            errors.append(f"{event_owner}: selected_route does not match step selection.")
        step_risk = next(
            (str(step.get("risk_class")) for step in steps if isinstance(step, dict) and step.get("step_id") == step_id),
            "",
        )
        if step_risk in HIGH_RISK:
            high_seen = True
        elif high_risk_steps and not high_seen:
            low_before_high = True
    expected_steps = {
        str(step.get("step_id"))
        for step in steps
        if isinstance(step, dict) and isinstance(step.get("step_id"), str)
    }
    if seen_steps != expected_steps:
        errors.append(f"{owner}: scheduler_trace does not cover exactly the step set.")
    if value.get("protected_high_risk_first") is True and low_before_high:
        errors.append(f"{owner}: low-risk work is scheduled before protected high-risk work.")

    for key, total in totals.items():
        budget_key = "tool_units" if key == "tool_units" else key
        if key != "cost_units" and total > float(capacity.get(budget_key, 0)):
            errors.append(f"{owner}: selected routes exceed {budget_key} capacity.")
    totals = {key: round(value, 2) for key, value in totals.items()}

    simulation = value.get("simulation_review")
    if not isinstance(simulation, dict):
        errors.append(f"{owner}: simulation_review must be an object.")
        simulation = {}
    fidelity_state = simulation.get("fidelity_state")
    transfer_decision = simulation.get("transfer_decision")
    support_state_effect = simulation.get("support_state_effect")
    if fidelity_state not in SUPPORTED_FIDELITY:
        errors.append(f"{owner}: simulation_review.fidelity_state must be a bounded fixture fidelity.")
    if transfer_decision not in SUPPORTED_TRANSFER_DECISIONS:
        errors.append(f"{owner}: simulation_review.transfer_decision overclaims transfer.")
    if support_state_effect != "none":
        errors.append(f"{owner}: simulation_review.support_state_effect must remain none.")
    for key in ("scope", "resource_bill", "capacity_bottlenecks", "omitted_variables", "instrumentation_effects"):
        if key not in simulation or not simulation[key]:
            errors.append(f"{owner}: simulation_review.{key} must be present and non-empty.")
    simulation_non_claims = text_blob(simulation.get("non_claims", []))
    for term in ("does not promote", "does not prove", "physical feasibility"):
        if term not in simulation_non_claims:
            errors.append(f"{owner}: simulation_review.non_claims missing {term!r}.")
    observed = simulation.get("observed_outputs")
    if not isinstance(observed, dict):
        errors.append(f"{owner}: simulation_review.observed_outputs must be an object.")
        observed = {}
    observed_cost = observed.get("total_cost_units")
    if isinstance(observed_cost, (int, float)) and not isinstance(observed_cost, bool):
        if round(float(observed_cost), 2) != totals["cost_units"]:
            errors.append(f"{owner}: observed total_cost_units does not match recomputed total.")
    else:
        errors.append(f"{owner}: observed total_cost_units must be numeric.")

    return {
        "trace_id": trace_id,
        "step_count": len(steps),
        "selected_route_count": len(selected_routes),
        "total_cost_units": totals["cost_units"],
        "total_tokens": int(totals["tokens"]),
        "review_minutes_used": totals["review_minutes"],
        "verification_minutes_used": totals["verification_minutes"],
        "transfer_decision": transfer_decision,
        "support_state_effect": support_state_effect,
        "selected_routes": [
            selected.get("route_id")
            for _step_id, selected in sorted(selected_routes.items())
        ],
        "rejected_route_count": sum(1 for eligible in route_eligibility.values() if not eligible),
    }


def fixture_expectation(path: Path) -> bool | None:
    if path.name.startswith("valid_"):
        return True
    if path.name.startswith("invalid_"):
        return False
    return None


def validate_result(
    expected: dict[str, Any],
    valid_count: int,
    invalid_count: int,
    expected_alignment: dict[str, Any],
    errors: list[str],
) -> None:
    if not RESULT.exists():
        errors.append(f"Missing {rel(RESULT)}.")
        return
    value = load_json(RESULT)
    if not isinstance(value, dict):
        errors.append(f"{rel(RESULT)} must contain an object.")
        return
    expected_pairs = {
        "command": "python3 scripts/validate_resource_workflow_trace.py",
        "valid_fixture_count": valid_count,
        "expected_invalid_fixture_count": invalid_count,
        "trace_id": expected["trace_id"],
        "step_count": expected["step_count"],
        "total_cost_units": expected["total_cost_units"],
        "total_tokens": expected["total_tokens"],
        "review_minutes_used": expected["review_minutes_used"],
        "verification_minutes_used": expected["verification_minutes_used"],
        "transfer_decision": expected["transfer_decision"],
        "support_state_effect": expected["support_state_effect"],
    }
    for key, expected_value in expected_pairs.items():
        if value.get(key) != expected_value:
            errors.append(f"{rel(RESULT)}: {key} must be {expected_value!r}.")
    if value.get("selected_routes") != expected["selected_routes"]:
        errors.append(f"{rel(RESULT)}: selected_routes mismatch.")
    if value.get("lean_fixture_alignment") != expected_alignment:
        errors.append(f"{rel(RESULT)}: lean_fixture_alignment must equal {expected_alignment!r}.")
    result_non_claims = text_blob(value.get("non_claims", []))
    for term in ("does not promote", "does not prove", "does not create"):
        if term not in result_non_claims:
            errors.append(f"{rel(RESULT)}: non_claims missing {term!r}.")


def validate_summary(expected: dict[str, Any], valid_count: int, invalid_count: int, errors: list[str]) -> None:
    if not SUMMARY.exists():
        errors.append(f"Missing {rel(SUMMARY)}.")
        return
    text = SUMMARY.read_text(encoding="utf-8")
    required = (
        "Resource Workflow Trace",
        "python3 scripts/validate_resource_workflow_trace.py",
        f"{valid_count} valid fixture",
        f"{invalid_count} expected-invalid",
        f"`{expected['trace_id']}`",
        f"{expected['total_cost_units']} cost units",
        "does not promote any chapter core claim",
        "does not prove deployed scheduler behavior",
        "does not prove physical feasibility",
        "`AsiStackProofs.ResourceEconomics`",
    )
    for fragment in required:
        if fragment not in text:
            errors.append(f"{rel(SUMMARY)} missing required fragment: {fragment}")


def parse_lean_fixture(errors: list[str]) -> dict[str, str]:
    if not LEAN_FIXTURE.exists():
        errors.append(f"Missing {rel(LEAN_FIXTURE)}.")
        return {}
    text = LEAN_FIXTURE.read_text(encoding="utf-8")
    declared_theorems = set(re.findall(r"^theorem\s+(\w+)\b", text, re.MULTILINE))
    for theorem in REQUIRED_LEAN_THEOREMS:
        if theorem not in declared_theorems:
            errors.append(f"{rel(LEAN_FIXTURE)} missing theorem {theorem}.")
    fixture_match = re.search(
        r"def\s+resourceWorkflowTraceFixture\s*:\s*WorkflowTraceSummary\s*:=\s*\{(?P<body>.*?)\}",
        text,
        re.DOTALL,
    )
    if not fixture_match:
        errors.append(f"{rel(LEAN_FIXTURE)} missing resourceWorkflowTraceFixture.")
        return {}
    return {
        field_match.group("field"): field_match.group("value").strip()
        for field_match in re.finditer(
            r"^\s*(?P<field>\w+)\s*:=\s*(?P<value>[^,\n}]+)",
            fixture_match.group("body"),
            re.MULTILINE,
        )
    }


def public_lean_alignment(fields: dict[str, str]) -> dict[str, Any]:
    def bool_value(field: str) -> bool:
        return fields[field] == "true"

    return {
        "step_count": int(fields["stepCount"]),
        "selected_route_count": int(fields["selectedRouteCount"]),
        "total_cost_tenths": int(fields["totalCostTenths"]),
        "expected_invalid_control_count": int(fields["expectedInvalidControlCount"]),
        "high_risk_first": bool_value("highRiskFirst"),
        "displaced_costs_residualized": bool_value("displacedCostsResidualized"),
        "physical_feasibility_overclaim_rejected": bool_value("physicalFeasibilityOverclaimRejected"),
        "latency_only_selection_rejected": bool_value("latencyOnlySelectionRejected"),
        "support_state_effect_none": bool_value("supportStateEffectNone"),
        "non_claim_boundary": bool_value("nonClaimBoundary"),
    }


def validate_lean_fixture(expected: dict[str, Any], invalid_count: int, errors: list[str]) -> dict[str, Any]:
    fields = parse_lean_fixture(errors)
    expected_fields = {
        "stepCount": str(expected["step_count"]),
        "selectedRouteCount": str(expected["selected_route_count"]),
        "totalCostTenths": str(int(round(float(expected["total_cost_units"]) * 10))),
        "expectedInvalidControlCount": str(invalid_count),
        "highRiskFirst": "true",
        "displacedCostsResidualized": "true",
        "physicalFeasibilityOverclaimRejected": "true",
        "latencyOnlySelectionRejected": "true",
        "supportStateEffectNone": "true",
        "nonClaimBoundary": "true",
    }
    for field, expected_value in expected_fields.items():
        if fields.get(field) != expected_value:
            errors.append(
                f"{rel(LEAN_FIXTURE)} resourceWorkflowTraceFixture.{field} "
                f"must be {expected_value!r}, got {fields.get(field)!r}."
            )
    if set(expected_fields) - set(fields):
        return {}
    return {
        "proof_bridge_type": "summary-level Python/Lean fixture equivalence",
        "lean_module": rel(LEAN_FIXTURE),
        "checked_theorem_names": list(REQUIRED_LEAN_THEOREMS),
        "field_alignment": public_lean_alignment(expected_fields),
    }


def main() -> None:
    fixtures = sorted(FIXTURE_DIR.glob("*.json"))
    if not fixtures:
        raise SystemExit(f"No resource workflow trace fixtures found in {rel(FIXTURE_DIR)}.")

    errors: list[str] = []
    valid_count = 0
    invalid_count = 0
    valid_summaries: list[dict[str, Any]] = []
    for fixture in fixtures:
        relative = rel(fixture)
        expect_valid = fixture_expectation(fixture)
        if expect_valid is None:
            errors.append(f"{relative}: fixture name must start with valid_ or invalid_.")
            continue
        try:
            value = load_json(fixture)
        except Exception as exc:
            errors.append(f"{relative}: invalid JSON: {exc}")
            continue
        if not isinstance(value, dict):
            errors.append(f"{relative}: top-level fixture must be an object.")
            continue
        fixture_errors: list[str] = []
        summary = summarize_valid_trace(value, fixture_errors, relative)
        if expect_valid:
            valid_count += 1
            errors.extend(fixture_errors)
            if not fixture_errors:
                valid_summaries.append(summary)
        else:
            invalid_count += 1
            if not fixture_errors:
                errors.append(f"{relative}: expected invalid fixture passed validation.")

    if len(valid_summaries) != 1:
        errors.append("Exactly one valid public workflow trace is expected for this narrow slice.")
    else:
        expected_alignment = validate_lean_fixture(valid_summaries[0], invalid_count, errors)
        validate_result(valid_summaries[0], valid_count, invalid_count, expected_alignment, errors)
        validate_summary(valid_summaries[0], valid_count, invalid_count, errors)

    if errors:
        fail(errors)

    summary = valid_summaries[0]
    print(
        "Resource workflow trace validation passed: "
        f"{valid_count} valid fixture(s), {invalid_count} expected-invalid fixture(s), "
        f"{summary['step_count']} step(s), {summary['total_cost_units']} cost units."
    )


if __name__ == "__main__":
    main()
