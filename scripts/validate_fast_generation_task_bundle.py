#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from run_fast_generation_task_bundle import build_result

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "experiments" / "fast_generation_task_bundle" / "results" / "2026-07-02-local.json"
DECISION = ROOT / "evidence_transitions" / "v1_x_measured" / "fast_generation_task_bundle_no_change.json"
DOC = ROOT / "docs" / "fast_generation_task_bundle.md"
CHAPTER = ROOT / "chapters" / "fast-generation-architectures.qmd"
READER = ROOT / "editions" / "reader_manuscript" / "v1_0" / "chapters" / "fast-generation-architectures.qmd"
OUTLINE = ROOT / "docs" / "book_outline.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
LEAN = ROOT / "lean" / "AsiStackProofs" / "FastGeneration.lean"

EXPECTED_NON_CLAIMS = [
    "Does not prove model generation speed.",
    "Does not prove useful-solution-per-second improvement for an AI model.",
    "Does not reproduce speculative decoding, MTP, diffusion, KV-cache, or serving benchmarks.",
    "Does not promote any chapter core claim or Appendix C support state.",
]

EXPECTED_SURFACE_PHRASES = [
    "fast_generation_task_bundle_2026_07_02_local",
    "evidence_transitions/v1_x_measured/fast_generation_task_bundle_no_change.json",
    "route://fast-template-verified",
    "route://latency-only-proxy",
    "no model-speed or deployment claim",
]

EXPECTED_READER_SURFACE_PHRASES = [
    "fast_generation_task_bundle_2026_07_02_local",
    "no-promotion decision",
    "fast-generation task bundle",
    "route://fast-template-verified",
    "route://latency-only-proxy",
    "no model-speed or deployment claim",
]

EXPECTED_LEAN_THEOREMS = [
    "fast_generation_task_bundle_candidate_preserves_quality",
    "fast_generation_task_bundle_candidate_improves_cost_accounting",
    "fast_generation_task_bundle_latency_only_proxy_rejected",
    "fast_generation_task_bundle_blocks_support_promotion",
]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def text_blob(value: Any) -> str:
    if isinstance(value, dict):
        return "\n".join(f"{key}: {text_blob(child)}" for key, child in value.items())
    if isinstance(value, list):
        return "\n".join(text_blob(item) for item in value)
    return str(value)


def route_by_id(result: dict[str, Any]) -> dict[str, dict[str, Any]]:
    routes = result.get("route_summary")
    if not isinstance(routes, list):
        return {}
    return {
        str(route.get("route_id")): route
        for route in routes
        if isinstance(route, dict)
    }


def compare_deterministic_fields(actual: dict[str, Any], expected: dict[str, Any], errors: list[str]) -> None:
    actual_routes = route_by_id(actual)
    expected_routes = route_by_id(expected)
    if set(actual_routes) != set(expected_routes):
        errors.append("route_summary route ids do not match the deterministic runner output.")
        return
    deterministic_fields = [
        "task_count",
        "tasks_passed",
        "tasks_failed",
        "quality_result",
        "promotion_decision",
        "fallback_recorded",
        "residuals_recorded",
        "outputs_digest",
        "generation_cost_units",
        "verifier_cost_units",
        "fallback_cost_units",
        "total_cost_units",
        "useful_solution_per_1000_cost_units",
    ]
    for route_id, expected_route in expected_routes.items():
        actual_route = actual_routes[route_id]
        for field in deterministic_fields:
            if actual_route.get(field) != expected_route.get(field):
                errors.append(f"{route_id}: field {field} is {actual_route.get(field)!r}, expected {expected_route.get(field)!r}.")
        elapsed = actual_route.get("observed_elapsed_ms")
        useful_per_second = actual_route.get("useful_solution_per_second_observed")
        if not isinstance(elapsed, (int, float)) or elapsed <= 0:
            errors.append(f"{route_id}: observed_elapsed_ms must be positive run metadata.")
        if not isinstance(useful_per_second, (int, float)) or useful_per_second < 0:
            errors.append(f"{route_id}: useful_solution_per_second_observed must be nonnegative run metadata.")


def validate_result(result: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    expected = build_result()
    for field in ("result_id", "task_bundle_id", "task_count", "baseline_route_id", "negative_control_route_id"):
        if result.get(field) != expected.get(field):
            errors.append(f"{field} is {result.get(field)!r}, expected {expected.get(field)!r}.")
    compare_deterministic_fields(result, expected, errors)

    routes = route_by_id(result)
    baseline = routes.get("route://autoregressive-reference", {})
    candidate = routes.get("route://fast-template-verified", {})
    negative = routes.get("route://latency-only-proxy", {})

    if result.get("selected_route_id") != "route://fast-template-verified":
        errors.append("selected_route_id must remain the verified fast-template route.")
    if baseline.get("tasks_passed") != result.get("task_count"):
        errors.append("baseline route must pass every task.")
    if candidate.get("tasks_passed") != result.get("task_count"):
        errors.append("candidate route must pass every task.")
    if candidate.get("total_cost_units", 0) >= baseline.get("total_cost_units", 0):
        errors.append("candidate route must have lower deterministic cost units than the baseline.")
    if candidate.get("useful_solution_per_1000_cost_units", 0) <= baseline.get("useful_solution_per_1000_cost_units", 0):
        errors.append("candidate route must improve deterministic useful-solution-per-cost accounting.")
    if negative.get("quality_result") != "fail" or negative.get("promotion_decision") != "reject":
        errors.append("latency-only negative control must fail quality and reject promotion.")
    if negative.get("total_cost_units", 10**9) >= candidate.get("total_cost_units", 0):
        errors.append("latency-only negative control should remain cheaper but invalid.")
    if result.get("negative_control_rejected") is not True:
        errors.append("negative_control_rejected must be true.")
    if result.get("support_state_effect") != "none":
        errors.append("support_state_effect must remain none.")

    non_claims = result.get("non_claims")
    if non_claims != EXPECTED_NON_CLAIMS:
        errors.append("non_claims must exactly preserve the expected no-promotion and no-model-speed boundaries.")
    evidence_refs = result.get("evidence_refs", [])
    evidence_blob = text_blob(evidence_refs)
    for prefix in ("run:", "validator:", "baseline:", "negative_control:"):
        if prefix not in evidence_blob:
            errors.append(f"evidence_refs missing {prefix} reference.")

    public_blob = text_blob(result)
    for forbidden in ("private payload", "support_state_effect\": \"promote", "chapter core promotion"):
        if forbidden in public_blob.lower():
            errors.append(f"result contains forbidden overclaim/private phrase: {forbidden}")
    return errors


def validate_decision() -> list[str]:
    errors: list[str] = []
    if not DECISION.exists():
        return [f"{DECISION.relative_to(ROOT)} is missing."]
    try:
        decision = load_json(DECISION)
    except Exception as exc:
        return [f"{DECISION.relative_to(ROOT)} is not valid JSON: {exc}"]
    expected = {
        "transition_id": "v1_x_measured.fast_generation_task_bundle.no_change",
        "claim_id": "fast-generation-architectures.public_safe_task_bundle_accounting",
        "old_support_state": "argument",
        "new_support_state": "argument",
        "transition_effect": "no_change",
        "transition_validity_state": "review_accepted",
        "review_status": "accepted",
        "support_state_effect": "blocks_promotion",
        "verification_result": "pass",
    }
    for field, expected_value in expected.items():
        if decision.get(field) != expected_value:
            errors.append(f"{DECISION.relative_to(ROOT)}: {field} is {decision.get(field)!r}, expected {expected_value!r}.")
    for field, phrase in (
        ("artifact_refs", "experiments/fast_generation_task_bundle/results/2026-07-02-local.json"),
        ("artifact_refs", "scripts/validate_fast_generation_task_bundle.py"),
        ("negative_results", "latency-only proxy is cheaper but rejected"),
        ("downgrade_triggers", "latency-only negative control accepted"),
        ("non_claims", "does not promote the Fast Generation chapter core claim"),
    ):
        if phrase.lower() not in text_blob(decision.get(field, [])).lower():
            errors.append(f"{DECISION.relative_to(ROOT)}: {field} missing {phrase!r}.")
    if "model-speed" not in str(decision.get("transition_reason", "")).lower():
        errors.append(f"{DECISION.relative_to(ROOT)}: transition_reason must preserve the model-speed non-claim.")
    return errors


def validate_surfaces() -> list[str]:
    errors: list[str] = []
    surfaces = {
        "docs/fast_generation_task_bundle.md": DOC,
        "chapters/fast-generation-architectures.qmd": CHAPTER,
        "editions/reader_manuscript/v1_0/chapters/fast-generation-architectures.qmd": READER,
        "docs/book_outline.md": OUTLINE,
        "docs/v1_x_beyond_sota_roadmap.md": ROADMAP,
    }
    for label, path in surfaces.items():
        text = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""
        phrases = EXPECTED_READER_SURFACE_PHRASES if path == READER else EXPECTED_SURFACE_PHRASES
        for phrase in phrases:
            if phrase not in text:
                errors.append(f"{label} missing phrase {phrase!r}.")
    lean_text = LEAN.read_text(encoding="utf-8", errors="ignore") if LEAN.exists() else ""
    for theorem in EXPECTED_LEAN_THEOREMS:
        if theorem not in lean_text:
            errors.append(f"FastGeneration Lean module missing theorem {theorem}.")
    return errors


def main() -> None:
    errors: list[str] = []
    if not RESULT.exists():
        errors.append(f"{RESULT.relative_to(ROOT)} is missing; run scripts/run_fast_generation_task_bundle.py --write-result.")
    else:
        try:
            result = load_json(RESULT)
        except Exception as exc:
            errors.append(f"{RESULT.relative_to(ROOT)} is not valid JSON: {exc}")
        else:
            if not isinstance(result, dict):
                errors.append(f"{RESULT.relative_to(ROOT)} must contain a JSON object.")
            else:
                errors.extend(validate_result(result))
    errors.extend(validate_decision())
    errors.extend(validate_surfaces())
    if errors:
        print("Fast generation task-bundle validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)
    routes = route_by_id(load_json(RESULT))
    candidate = routes["route://fast-template-verified"]
    baseline = routes["route://autoregressive-reference"]
    negative = routes["route://latency-only-proxy"]
    print(
        "Fast generation task-bundle validation passed: "
        f"candidate {candidate['tasks_passed']}/{candidate['task_count']} tasks at "
        f"{candidate['total_cost_units']} cost units vs baseline {baseline['total_cost_units']}; "
        f"latency-only negative rejected at {negative['total_cost_units']} cost units."
    )


if __name__ == "__main__":
    main()
