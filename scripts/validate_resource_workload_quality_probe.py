#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import re
import sys
from typing import Any

from run_resource_workload_quality_probe import (
    NON_CLAIMS,
    PROBE_ID,
    RESIDUALS,
    RESULT,
    RESULT_COMMAND,
    ROUTES,
    SCOPED_TASK,
    TRACKED_ARTIFACTS,
    ROOT,
    artifact_stat,
    run_route,
)


DOC = ROOT / "docs" / "resource_workload_quality_probe.md"
SHA_RE = re.compile(r"^[0-9a-f]{64}$")
REQUIRED_NON_CLAIM_TERMS = (
    "does not promote any chapter core claim",
    "does not create a support-state transition",
    "does not prove stable speedup",
    "does not replace the full book gate",
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
    print("Resource workload-quality probe validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def route_by_role(routes: list[dict[str, Any]], role: str) -> dict[str, Any]:
    matches = [route for route in routes if route.get("role") == role]
    if len(matches) != 1:
        return {}
    return matches[0]


def validate_record_shape(value: dict[str, Any], errors: list[str]) -> None:
    expected_scalars = {
        "probe_id": PROBE_ID,
        "record_kind": "resource_workload_quality_probe",
        "command": RESULT_COMMAND,
        "scoped_task": SCOPED_TASK,
        "local_only": True,
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
    if not isinstance(summary, str) or "scoped workflow-trace validator" not in summary:
        errors.append(f"{rel(RESULT)}: summary must describe the scoped workflow-trace selection.")

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
        errors.append(f"{rel(RESULT)}: artifact_refs must match the tracked workload-quality surface.")
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
        for key in ("route_id", "role", "command", "required_output", "quality_scope"):
            if recorded.get(key) != expected[key]:
                errors.append(f"{owner}: {key} must be {expected[key]!r}.")
        if recorded.get("exit_code") != 0:
            errors.append(f"{owner}: route command must exit 0 so quality is not confused with process failure.")
        if not isinstance(recorded.get("elapsed_ms"), (int, float)) or recorded["elapsed_ms"] <= 0:
            errors.append(f"{owner}: elapsed_ms must be a positive measured number.")
        if not isinstance(recorded.get("output_sha256"), str) or not SHA_RE.match(recorded["output_sha256"]):
            errors.append(f"{owner}: output_sha256 must be a SHA-256 hex digest.")
        excerpt = recorded.get("output_excerpt")
        if not isinstance(excerpt, list) or not excerpt:
            errors.append(f"{owner}: output_excerpt must be a non-empty list.")
        replayed = run_route(expected)
        if replayed["exit_code"] != 0:
            errors.append(f"{owner}: current replay of {expected['command']} failed.")
        if replayed["output_sha256"] != recorded.get("output_sha256"):
            errors.append(f"{owner}: current replay output digest differs from recorded digest.")
        if replayed["quality_pass"] != recorded.get("quality_pass"):
            errors.append(f"{owner}: current replay quality result differs from recorded quality result.")

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
        errors.append(f"{rel(RESULT)}: baseline route must pass quality.")
    if not selected.get("quality_pass"):
        errors.append(f"{rel(RESULT)}: selected route must pass quality.")
    if negative.get("quality_pass"):
        errors.append(f"{rel(RESULT)}: negative no-op route must fail quality despite exiting 0.")
    if not value.get("negative_control_rejected"):
        errors.append(f"{rel(RESULT)}: negative_control_rejected must be true.")
    if not value.get("selected_is_cheaper_than_baseline"):
        errors.append(f"{rel(RESULT)}: selected_is_cheaper_than_baseline must be true for this recorded local run.")
    if selected.get("elapsed_ms", 0) >= baseline.get("elapsed_ms", 0):
        errors.append(f"{rel(RESULT)}: selected route elapsed_ms must be lower than baseline elapsed_ms.")
    if not value.get("negative_control_is_cheaper_than_selected"):
        errors.append(f"{rel(RESULT)}: negative_control_is_cheaper_than_selected must be true.")
    if negative.get("elapsed_ms", 0) >= selected.get("elapsed_ms", 0):
        errors.append(f"{rel(RESULT)}: negative control should remain the cheaper but rejected route.")
    reduction = value.get("observed_selected_vs_baseline_elapsed_reduction_percent")
    if not isinstance(reduction, (int, float)) or reduction <= 0:
        errors.append(f"{rel(RESULT)}: observed reduction percent must be positive.")


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
        "Resource Workload-Quality Probe",
        RESULT_COMMAND,
        rel(RESULT),
        "route://baseline-full-resource-lane-replay",
        "route://selected-scoped-workflow-trace-validator",
        "route://negative-no-op-success-text",
        "Support-state effect | `none`",
        "Chapter-core support effect | `none`",
        "does not prove stable speedup",
        "does not replace the full book gate",
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

    validate_record_shape(value, errors)
    validate_routes(value, errors)
    validate_tracked_artifacts(value, errors)
    validate_doc(errors)

    if errors:
        fail(errors)
    routes = value["routes"]
    print(
        "Resource workload-quality probe validation passed: "
        f"{len(routes)} measured route(s), selected {value['selected_route_id']}, "
        f"negative control rejected, support-state effect none."
    )


if __name__ == "__main__":
    main()
