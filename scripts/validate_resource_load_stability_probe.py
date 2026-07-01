#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import re
import sys
from typing import Any

from run_resource_load_stability_probe import (
    CAPACITY_LIMIT,
    HORIZON_TICKS,
    NON_CLAIMS,
    PROBE_ID,
    RESIDUALS,
    RESULT,
    RESULT_COMMAND,
    REVIEW_CAPACITY_LIMIT,
    ROOT,
    ROUTES,
    TRACKED_ARTIFACTS,
    WORKLOAD,
    WORKLOAD_ID,
    artifact_stat,
    build_record,
)


DOC = ROOT / "docs" / "resource_load_stability_probe.md"
LEAN_FIXTURE = ROOT / "lean" / "AsiStackProofs" / "ResourceEconomics.lean"
SHA_RE = re.compile(r"^[0-9a-f]{64}$")
REQUIRED_THEOREMS = (
    "resource_load_smoothing_workload_fixture_valid",
    "resource_load_smoothing_workload_reduces_overrun",
    "resource_load_smoothing_workload_rejects_review_erasure",
    "resource_load_smoothing_workload_residualizes_deferrals",
    "resource_load_smoothing_workload_has_no_support_promotion",
)
REQUIRED_NON_CLAIM_TERMS = (
    "does not promote any chapter core claim",
    "does not create a support-state transition",
    "does not prove tokenmana behavior",
    "does not replace production scheduler logs",
)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def text_blob(value: Any) -> str:
    if isinstance(value, dict):
        return "\n".join(f"{key}: {text_blob(child)}" for key, child in value.items()).lower()
    if isinstance(value, list):
        return "\n".join(text_blob(item) for item in value).lower()
    return str(value).lower()


def fail(errors: list[str]) -> None:
    print("Resource load-stability probe validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def route_by_role(routes: list[dict[str, Any]], role: str) -> dict[str, Any]:
    matches = [route for route in routes if route.get("role") == role]
    if len(matches) != 1:
        return {}
    return matches[0]


def comparable_record(value: dict[str, Any]) -> dict[str, Any]:
    copy = dict(value)
    copy.pop("recorded_at_utc", None)
    return copy


def validate_record_shape(value: dict[str, Any], errors: list[str]) -> None:
    expected_scalars = {
        "probe_id": PROBE_ID,
        "record_kind": "resource_load_stability_probe",
        "command": RESULT_COMMAND,
        "workload_id": WORKLOAD_ID,
        "capacity_limit": CAPACITY_LIMIT,
        "review_capacity_limit": REVIEW_CAPACITY_LIMIT,
        "horizon_ticks": HORIZON_TICKS,
        "local_only": True,
        "synthetic_only": True,
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
        "pass": True,
    }
    for key, expected in expected_scalars.items():
        if value.get(key) != expected:
            errors.append(f"{rel(RESULT)}: {key} must be {expected!r}.")

    timestamp = value.get("recorded_at_utc")
    if not isinstance(timestamp, str) or not timestamp.endswith("Z"):
        errors.append(f"{rel(RESULT)}: recorded_at_utc must be a UTC timestamp ending in Z.")

    summary = value.get("summary")
    if not isinstance(summary, str) or "Local synthetic Resource Economics load-stability probe" not in summary:
        errors.append(f"{rel(RESULT)}: summary must describe the local synthetic load-stability probe.")

    if value.get("workload") != WORKLOAD:
        errors.append(f"{rel(RESULT)}: workload must match the runner workload.")
    if value.get("residuals") != RESIDUALS:
        errors.append(f"{rel(RESULT)}: residuals must match the runner residual list.")
    if value.get("non_claims") != NON_CLAIMS:
        errors.append(f"{rel(RESULT)}: non_claims must match the runner non-claim list.")
    non_claim_text = text_blob(value.get("non_claims"))
    for term in REQUIRED_NON_CLAIM_TERMS:
        if term not in non_claim_text:
            errors.append(f"{rel(RESULT)}: non_claims missing boundary phrase {term!r}.")

    artifact_refs = value.get("artifact_refs")
    expected_refs = [*TRACKED_ARTIFACTS, rel(RESULT)]
    if artifact_refs != expected_refs:
        errors.append(f"{rel(RESULT)}: artifact_refs must match the tracked load-stability surface.")
    for relative in expected_refs:
        if not (ROOT / relative).exists():
            errors.append(f"{rel(RESULT)}: referenced artifact does not exist: {relative}.")


def validate_routes(value: dict[str, Any], errors: list[str]) -> None:
    routes = value.get("routes")
    if not isinstance(routes, list):
        errors.append(f"{rel(RESULT)}: routes must be a list.")
        return
    if len(routes) != len(ROUTES):
        errors.append(f"{rel(RESULT)}: expected {len(ROUTES)} routes, found {len(routes)}.")
        return

    for index, (expected, recorded) in enumerate(zip(ROUTES, routes)):
        owner = f"{rel(RESULT)}:routes[{index}]"
        if not isinstance(recorded, dict):
            errors.append(f"{owner}: route record must be an object.")
            continue
        for key in ("route_id", "role", "strategy", "quality_scope"):
            if recorded.get(key) != expected[key]:
                errors.append(f"{owner}: {key} must be {expected[key]!r}.")
        for field in (
            "completed_task_count",
            "total_value_points_completed",
            "total_capacity_used",
            "total_review_minutes_used",
            "total_capacity_overrun",
            "total_review_overrun",
            "peak_capacity_overrun",
            "peak_review_overrun",
            "load_instability_units",
            "total_deferred_task_ticks",
            "total_hidden_deferred_task_ticks",
            "protected_review_violation_count",
            "residualized_deferred_task_ticks",
        ):
            item = recorded.get(field)
            if not isinstance(item, int) or isinstance(item, bool) or item < 0:
                errors.append(f"{owner}: {field} must be a non-negative integer.")
        if recorded.get("all_tasks_completed") is not True:
            errors.append(f"{owner}: all_tasks_completed must be true for this finite workload replay.")
        if len(recorded.get("events", [])) != HORIZON_TICKS:
            errors.append(f"{owner}: events must contain {HORIZON_TICKS} ticks.")

    baseline = route_by_role(routes, "baseline")
    selected = route_by_role(routes, "selected")
    negative = route_by_role(routes, "negative_control")
    if not baseline or not selected or not negative:
        errors.append(f"{rel(RESULT)}: routes must include exactly one baseline, selected route, and negative control.")
        return

    if value.get("baseline_route_id") != baseline.get("route_id"):
        errors.append(f"{rel(RESULT)}: baseline_route_id must match the baseline route.")
    if value.get("selected_route_id") != selected.get("route_id"):
        errors.append(f"{rel(RESULT)}: selected_route_id must match the selected route.")
    if value.get("negative_control_route_id") != negative.get("route_id"):
        errors.append(f"{rel(RESULT)}: negative_control_route_id must match the negative route.")
    if not baseline.get("quality_pass"):
        errors.append(f"{rel(RESULT)}: baseline route must pass quality despite overload.")
    if not selected.get("quality_pass"):
        errors.append(f"{rel(RESULT)}: selected route must pass quality.")
    if negative.get("quality_pass"):
        errors.append(f"{rel(RESULT)}: review-erasure negative control must fail quality.")
    if not value.get("negative_control_rejected"):
        errors.append(f"{rel(RESULT)}: negative_control_rejected must be true.")
    if not value.get("negative_control_uses_less_review_than_selected"):
        errors.append(f"{rel(RESULT)}: negative control should use less review than selected by erasing review.")
    if not value.get("selected_has_no_capacity_or_review_overrun"):
        errors.append(f"{rel(RESULT)}: selected route must have no capacity or review overrun.")
    if not value.get("selected_residualized_all_deferrals"):
        errors.append(f"{rel(RESULT)}: selected route must residualize every deferred task tick.")
    if selected.get("load_instability_units", 0) >= baseline.get("load_instability_units", 0):
        errors.append(f"{rel(RESULT)}: selected route must reduce load_instability_units below baseline.")
    reduction = value.get("selected_vs_baseline_instability_reduction_percent")
    if not isinstance(reduction, (int, float)) or reduction <= 0:
        errors.append(f"{rel(RESULT)}: selected-vs-baseline instability reduction must be positive.")
    if selected.get("total_deferred_task_ticks") != selected.get("residualized_deferred_task_ticks"):
        errors.append(f"{rel(RESULT)}: selected deferrals must be exactly residualized.")
    if negative.get("protected_review_violation_count", 0) <= 0:
        errors.append(f"{rel(RESULT)}: negative control must expose protected review erasure.")
    if negative.get("total_hidden_deferred_task_ticks", 0) <= 0:
        errors.append(f"{rel(RESULT)}: negative control must expose hidden deferrals.")


def validate_lean_alignment(value: dict[str, Any], errors: list[str]) -> None:
    alignment = value.get("lean_fixture_alignment")
    if not isinstance(alignment, dict):
        errors.append(f"{rel(RESULT)}: lean_fixture_alignment must be an object.")
        return
    if alignment.get("module") != "AsiStackProofs.ResourceEconomics":
        errors.append(f"{rel(RESULT)}: lean_fixture_alignment.module must be AsiStackProofs.ResourceEconomics.")
    theorem_refs = alignment.get("theorem_refs")
    if theorem_refs != list(REQUIRED_THEOREMS):
        errors.append(f"{rel(RESULT)}: lean_fixture_alignment.theorem_refs must list the required load-smoothing theorems.")
    expected = alignment.get("expected")
    if not isinstance(expected, dict):
        errors.append(f"{rel(RESULT)}: lean_fixture_alignment.expected must be an object.")
        return
    routes = value.get("routes", [])
    baseline = route_by_role(routes, "baseline")
    selected = route_by_role(routes, "selected")
    negative = route_by_role(routes, "negative_control")
    expected_values = {
        "task_count": len(WORKLOAD),
        "route_count": len(ROUTES),
        "baseline_peak_capacity_overrun": baseline.get("peak_capacity_overrun"),
        "baseline_total_overrun": baseline.get("load_instability_units"),
        "selected_peak_capacity_overrun": selected.get("peak_capacity_overrun"),
        "selected_total_overrun": selected.get("load_instability_units"),
        "selected_deferred_task_ticks": selected.get("total_deferred_task_ticks"),
        "selected_residualized_deferred_task_ticks": selected.get("residualized_deferred_task_ticks"),
        "negative_protected_review_violations": negative.get("protected_review_violation_count"),
    }
    for key, expected_value in expected_values.items():
        if expected.get(key) != expected_value:
            errors.append(f"{rel(RESULT)}: lean_fixture_alignment.expected.{key} must be {expected_value!r}.")

    lean_text = LEAN_FIXTURE.read_text(encoding="utf-8", errors="ignore")
    for theorem in REQUIRED_THEOREMS:
        if theorem not in lean_text:
            errors.append(f"{rel(LEAN_FIXTURE)} is missing theorem {theorem}.")


def validate_tracked_artifacts(value: dict[str, Any], errors: list[str]) -> None:
    tracked = value.get("tracked_artifacts")
    if not isinstance(tracked, list):
        errors.append(f"{rel(RESULT)}: tracked_artifacts must be a list.")
        return
    if len(tracked) != len(TRACKED_ARTIFACTS):
        errors.append(f"{rel(RESULT)}: expected {len(TRACKED_ARTIFACTS)} tracked artifact stats, found {len(tracked)}.")
        return
    for index, (relative, recorded) in enumerate(zip(TRACKED_ARTIFACTS, tracked)):
        owner = f"{rel(RESULT)}:tracked_artifacts[{index}]"
        if not isinstance(recorded, dict):
            errors.append(f"{owner}: artifact stat must be an object.")
            continue
        current = artifact_stat(relative)
        for key, expected in current.items():
            if recorded.get(key) != expected:
                errors.append(f"{owner}: {key} must match current {relative} value {expected!r}.")
        if not SHA_RE.match(str(recorded.get("sha256", ""))):
            errors.append(f"{owner}: sha256 must be a SHA-256 hex digest.")


def validate_doc(errors: list[str]) -> None:
    if not DOC.exists():
        errors.append(f"Missing {rel(DOC)}.")
        return
    text = DOC.read_text(encoding="utf-8")
    normalized = re.sub(r"\s+", " ", text)
    required = [
        "Resource Load-Stability Probe",
        RESULT_COMMAND,
        rel(RESULT),
        "route://baseline-admit-arrivals",
        "route://selected-protected-capacity-smoothing",
        "route://negative-latency-only-review-erasure",
        "Support-state effect | `none`",
        "Chapter-core support effect | `none`",
        "does not prove TokenMana behavior",
        "does not replace production scheduler logs",
    ]
    for fragment in required:
        haystack = normalized if " " in fragment else text
        if fragment not in haystack:
            errors.append(f"{rel(DOC)} missing required fragment: {fragment}")


def main() -> None:
    errors: list[str] = []
    if not RESULT.exists():
        fail([f"Missing {rel(RESULT)}. Run `{RESULT_COMMAND}` first."])
    value = load_json(RESULT)
    if not isinstance(value, dict):
        fail([f"{rel(RESULT)} must contain a JSON object."])

    expected = build_record()
    if comparable_record(value) != comparable_record(expected):
        errors.append(f"{rel(RESULT)}: recorded deterministic fields differ from current runner output.")

    validate_record_shape(value, errors)
    validate_routes(value, errors)
    validate_lean_alignment(value, errors)
    validate_tracked_artifacts(value, errors)
    validate_doc(errors)

    if errors:
        fail(errors)
    print(
        "Resource load-stability probe validation passed: "
        f"{len(value['routes'])} route(s), selected {value['selected_route_id']}, "
        "review-erasure negative control rejected, support-state effect none."
    )


if __name__ == "__main__":
    main()
