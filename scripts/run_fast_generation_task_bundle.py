#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "experiments" / "fast_generation_task_bundle" / "results" / "2026-07-02-local.json"

TASKS: list[dict[str, Any]] = [
    {
        "task_id": "fg-task-001",
        "risk_tier": "low",
        "prompt": "Create a public-safe status receipt for a validator-only fast generation task.",
        "required_terms": ["public-safe", "validator", "baseline", "negative-control"],
    },
    {
        "task_id": "fg-task-002",
        "risk_tier": "medium",
        "prompt": "Create an evidence-boundary note for a fast route that must keep fallback visible.",
        "required_terms": ["fallback", "residual", "verifier", "no-promotion"],
    },
    {
        "task_id": "fg-task-003",
        "risk_tier": "medium",
        "prompt": "Create a route-selection note that separates proposed output from accepted output.",
        "required_terms": ["proposed", "accepted", "quality", "cost"],
    },
    {
        "task_id": "fg-task-004",
        "risk_tier": "high",
        "prompt": "Create a high-risk fast-mode note that refuses raw latency-only promotion.",
        "required_terms": ["high-risk", "latency-only", "slow-fallback", "review"],
    },
]

NON_CLAIMS = [
    "Does not prove model generation speed.",
    "Does not prove useful-solution-per-second improvement for an AI model.",
    "Does not reproduce speculative decoding, MTP, diffusion, KV-cache, or serving benchmarks.",
    "Does not promote any chapter core claim or Appendix C support state.",
]


def stable_digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def baseline_output(task: dict[str, Any]) -> dict[str, Any]:
    terms = list(task["required_terms"])
    return {
        "task_id": task["task_id"],
        "route": "autoregressive_reference",
        "risk_tier": task["risk_tier"],
        "accepted_terms": terms,
        "receipt": (
            "public-safe baseline receipt with verifier, baseline, negative-control, "
            "fallback, residual, no-promotion, proposed, accepted, quality, cost, "
            "high-risk, latency-only, slow-fallback, and review boundaries"
        ),
        "support_state_effect": "none",
    }


def fast_verified_output(task: dict[str, Any]) -> dict[str, Any]:
    terms = list(task["required_terms"])
    return {
        "task_id": task["task_id"],
        "route": "fast_template_verified",
        "risk_tier": task["risk_tier"],
        "accepted_terms": terms,
        "receipt": "public-safe verified template: " + ", ".join(terms) + "; no-promotion boundary preserved",
        "support_state_effect": "none",
    }


def latency_only_output(task: dict[str, Any]) -> dict[str, Any]:
    return {
        "task_id": task["task_id"],
        "route": "latency_only_proxy",
        "risk_tier": task["risk_tier"],
        "accepted_terms": [],
        "receipt": "fast text returned without verifier, baseline, fallback, residual, or quality boundary",
        "support_state_effect": "attempted_promotion",
    }


def verify_output(task: dict[str, Any], output: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    receipt = str(output.get("receipt", "")).lower()
    accepted_terms = output.get("accepted_terms")
    if output.get("task_id") != task["task_id"]:
        errors.append("task_id mismatch")
    if output.get("support_state_effect") != "none":
        errors.append("support_state_effect must remain none")
    if not isinstance(accepted_terms, list):
        errors.append("accepted_terms must be a list")
        accepted_terms = []
    for term in task["required_terms"]:
        if term not in accepted_terms and term.lower() not in receipt:
            errors.append(f"missing required term {term}")
    for boundary in ("public-safe", "no-promotion"):
        if boundary not in receipt:
            errors.append(f"missing boundary {boundary}")
    return errors


def route_cost_units(route_id: str, outputs: list[dict[str, Any]], verifier_errors: list[list[str]]) -> dict[str, int]:
    task_count = len(outputs)
    accepted_count = sum(1 for errors in verifier_errors if not errors)
    rejected_count = task_count - accepted_count
    if route_id == "route://autoregressive-reference":
        generation_cost = sum(len(str(output["receipt"]).split()) * 7 for output in outputs)
        verifier_cost = task_count * 18
        fallback_cost = rejected_count * 35
    elif route_id == "route://fast-template-verified":
        generation_cost = sum(len(output.get("accepted_terms", [])) * 8 + 16 for output in outputs)
        verifier_cost = task_count * 18
        fallback_cost = rejected_count * 35
    else:
        generation_cost = task_count * 5
        verifier_cost = task_count * 4
        fallback_cost = rejected_count * 35
    return {
        "generation_cost_units": generation_cost,
        "verifier_cost_units": verifier_cost,
        "fallback_cost_units": fallback_cost,
        "total_cost_units": generation_cost + verifier_cost + fallback_cost,
    }


def execute_route(
    route_id: str,
    mode_family: str,
    builder: Callable[[dict[str, Any]], dict[str, Any]],
    promotion_decision: str,
) -> dict[str, Any]:
    start = time.perf_counter_ns()
    outputs = [builder(task) for task in TASKS]
    verifier_errors = [verify_output(task, output) for task, output in zip(TASKS, outputs)]
    elapsed_ns = max(time.perf_counter_ns() - start, 1)
    passed = sum(1 for errors in verifier_errors if not errors)
    cost = route_cost_units(route_id, outputs, verifier_errors)
    useful_per_1000_cost = round((passed * 1000.0) / cost["total_cost_units"], 6)
    useful_per_second = round(passed / (elapsed_ns / 1_000_000_000), 6)
    return {
        "route_id": route_id,
        "mode_family": mode_family,
        "task_count": len(TASKS),
        "tasks_passed": passed,
        "tasks_failed": len(TASKS) - passed,
        "observed_elapsed_ms": round(elapsed_ns / 1_000_000, 6),
        "useful_solution_per_second_observed": useful_per_second,
        "useful_solution_per_1000_cost_units": useful_per_1000_cost,
        "quality_result": "pass" if passed == len(TASKS) else "fail",
        "promotion_decision": promotion_decision,
        "fallback_recorded": route_id != "route://latency-only-proxy",
        "residuals_recorded": route_id != "route://latency-only-proxy",
        "outputs_digest": stable_digest(outputs),
        "verifier_errors": verifier_errors,
        **cost,
    }


def build_result() -> dict[str, Any]:
    routes = [
        execute_route(
            "route://autoregressive-reference",
            "autoregressive_reference",
            baseline_output,
            "baseline_only",
        ),
        execute_route(
            "route://fast-template-verified",
            "fast_template_verified",
            fast_verified_output,
            "keep_experimental",
        ),
        execute_route(
            "route://latency-only-proxy",
            "latency_only_proxy",
            latency_only_output,
            "reject",
        ),
    ]
    route_by_id = {route["route_id"]: route for route in routes}
    selected_route_id = "route://fast-template-verified"
    return {
        "result_id": "fast_generation_task_bundle_2026_07_02_local",
        "generated_at": "2026-07-02",
        "task_bundle_id": "fg-public-safe-task-bundle-001",
        "task_count": len(TASKS),
        "measurement_policy": (
            "Deterministic cost-unit selection with local elapsed milliseconds recorded as run metadata; "
            "no model-speed or deployment claim."
        ),
        "selected_route_id": selected_route_id,
        "baseline_route_id": "route://autoregressive-reference",
        "negative_control_route_id": "route://latency-only-proxy",
        "route_summary": routes,
        "selection_rationale": (
            "The selected route passed the same four public-safe tasks as the baseline at lower deterministic "
            "cost units; the cheaper latency-only proxy failed verifier, fallback, residual, and support-state "
            "boundaries."
        ),
        "negative_control_rejected": (
            route_by_id["route://latency-only-proxy"]["promotion_decision"] == "reject"
            and route_by_id["route://latency-only-proxy"]["quality_result"] == "fail"
        ),
        "support_state_effect": "none",
        "evidence_refs": [
            "run:python3 scripts/run_fast_generation_task_bundle.py --write-result",
            "validator:python3 scripts/validate_fast_generation_task_bundle.py",
            "baseline:route://autoregressive-reference",
            "negative_control:route://latency-only-proxy",
        ],
        "non_claims": NON_CLAIMS,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-result", action="store_true", help=f"Write {RESULT.relative_to(ROOT)}.")
    args = parser.parse_args()
    result = build_result()
    if args.write_result:
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"Wrote {RESULT.relative_to(ROOT)}")
    else:
        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
