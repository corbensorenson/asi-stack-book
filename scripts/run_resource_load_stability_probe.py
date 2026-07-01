#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "experiments" / "resource_load_stability_probe" / "results" / "2026-07-01-local.json"
PROBE_ID = "resource-load-stability-probe-2026-07-01-local"
RESULT_COMMAND = "python3 scripts/run_resource_load_stability_probe.py --write-result"
WORKLOAD_ID = "resource-burst-review-workload-v1"
CAPACITY_LIMIT = 7
REVIEW_CAPACITY_LIMIT = 5
HORIZON_TICKS = 6

RISK_PRIORITY = {"critical": 0, "high": 1, "medium": 2, "low": 3}

WORKLOAD = [
    {
        "task_id": "release-gate-audit",
        "arrival_tick": 0,
        "risk": "critical",
        "capacity_cost": 4,
        "review_minutes": 3,
        "value_points": 90,
    },
    {
        "task_id": "source-crosswalk-refresh",
        "arrival_tick": 0,
        "risk": "medium",
        "capacity_cost": 3,
        "review_minutes": 2,
        "value_points": 45,
    },
    {
        "task_id": "appendix-link-fix",
        "arrival_tick": 0,
        "risk": "low",
        "capacity_cost": 2,
        "review_minutes": 0,
        "value_points": 15,
    },
    {
        "task_id": "security-kernel-receipt",
        "arrival_tick": 1,
        "risk": "high",
        "capacity_cost": 4,
        "review_minutes": 3,
        "value_points": 80,
    },
    {
        "task_id": "ci-metadata-refresh",
        "arrival_tick": 1,
        "risk": "medium",
        "capacity_cost": 3,
        "review_minutes": 1,
        "value_points": 40,
    },
    {
        "task_id": "reader-overlay-polish",
        "arrival_tick": 1,
        "risk": "low",
        "capacity_cost": 2,
        "review_minutes": 1,
        "value_points": 20,
    },
    {
        "task_id": "evidence-transition-review",
        "arrival_tick": 2,
        "risk": "high",
        "capacity_cost": 4,
        "review_minutes": 3,
        "value_points": 85,
    },
    {
        "task_id": "index-cleanup",
        "arrival_tick": 2,
        "risk": "low",
        "capacity_cost": 2,
        "review_minutes": 0,
        "value_points": 10,
    },
    {
        "task_id": "visual-alt-text-pass",
        "arrival_tick": 2,
        "risk": "low",
        "capacity_cost": 2,
        "review_minutes": 1,
        "value_points": 20,
    },
    {
        "task_id": "external-source-note",
        "arrival_tick": 3,
        "risk": "medium",
        "capacity_cost": 3,
        "review_minutes": 2,
        "value_points": 35,
    },
]

ROUTES = [
    {
        "route_id": "route://baseline-admit-arrivals",
        "role": "baseline",
        "strategy": "admit_arrivals",
        "quality_scope": "Admit every arriving task immediately with protected review intact, exposing burst overload.",
    },
    {
        "route_id": "route://selected-protected-capacity-smoothing",
        "role": "selected",
        "strategy": "protected_capacity_smoothing",
        "quality_scope": "Admit high-risk work first within capacity, defer low-risk work with residual ownership, and preserve protected review.",
    },
    {
        "route_id": "route://negative-latency-only-review-erasure",
        "role": "negative_control",
        "strategy": "latency_only_review_erasure",
        "quality_scope": "Invalid shortcut that keeps capacity low by erasing protected review and hidden deferrals.",
    },
]

TRACKED_ARTIFACTS = [
    "scripts/run_resource_load_stability_probe.py",
    "lean/AsiStackProofs/ResourceEconomics.lean",
]

NON_CLAIMS = [
    "This load-stability probe does not promote any chapter core claim above argument.",
    "This load-stability probe does not create a support-state transition.",
    "This load-stability probe does not prove TokenMana behavior, PlanForge behavior, deployed scheduler behavior, production queue behavior, real load stability, human productivity, model quality, economic outcomes, physical feasibility, simulator adequacy, or workload-quality improvement outside this local synthetic repository workload.",
    "The selected route is scoped to this finite burst-review workload only and does not replace production scheduler logs, live workload-quality review, human-repair measurement, external review, or the full book gate.",
]

RESIDUALS = [
    "The workload is a deterministic local synthetic burst of repository-review tasks, not a production queue trace.",
    "The selected route reduces overload in the finite workload by deferring lower-risk work, but those deferrals are residual costs rather than free savings.",
    "The negative control shows that lower review minutes are invalid when protected high-risk review is erased or deferred work is hidden.",
]


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def task_sort_key(task: dict[str, Any]) -> tuple[int, int, str]:
    return (RISK_PRIORITY[str(task["risk"])], int(task["arrival_tick"]), str(task["task_id"]))


def arrived_tasks(tick: int) -> list[dict[str, Any]]:
    return [task for task in WORKLOAD if int(task["arrival_tick"]) == tick]


def task_ids(tasks: list[dict[str, Any]]) -> list[str]:
    return [str(task["task_id"]) for task in tasks]


def simulate_admit_arrivals() -> dict[str, Any]:
    events: list[dict[str, Any]] = []
    completed: list[dict[str, Any]] = []
    for tick in range(HORIZON_TICKS):
        admitted = arrived_tasks(tick)
        completed.extend(admitted)
        capacity_used = sum(int(task["capacity_cost"]) for task in admitted)
        review_used = sum(int(task["review_minutes"]) for task in admitted)
        events.append(
            {
                "tick": tick,
                "admitted_task_ids": task_ids(admitted),
                "deferred_task_ids": [],
                "capacity_used": capacity_used,
                "review_minutes_used": review_used,
                "capacity_overrun": max(0, capacity_used - CAPACITY_LIMIT),
                "review_overrun": max(0, review_used - REVIEW_CAPACITY_LIMIT),
                "protected_review_erased_task_ids": [],
                "hidden_deferred_task_ids": [],
                "residual_refs": [],
            }
        )
    return route_summary("baseline", events, completed)


def simulate_protected_capacity_smoothing() -> dict[str, Any]:
    events: list[dict[str, Any]] = []
    pending: list[dict[str, Any]] = []
    completed: list[dict[str, Any]] = []
    residual_refs: list[str] = []

    for tick in range(HORIZON_TICKS):
        pending.extend(arrived_tasks(tick))
        capacity_remaining = CAPACITY_LIMIT
        review_remaining = REVIEW_CAPACITY_LIMIT
        admitted: list[dict[str, Any]] = []
        deferred: list[dict[str, Any]] = []

        for task in sorted(pending, key=task_sort_key):
            cost = int(task["capacity_cost"])
            review = int(task["review_minutes"])
            if cost <= capacity_remaining and review <= review_remaining:
                admitted.append(task)
                completed.append(task)
                capacity_remaining -= cost
                review_remaining -= review
            else:
                deferred.append(task)

        pending = deferred
        residual_refs_for_tick = [
            f"residual://{WORKLOAD_ID}/deferred/{tick}/{task['task_id']}"
            for task in deferred
        ]
        residual_refs.extend(residual_refs_for_tick)
        events.append(
            {
                "tick": tick,
                "admitted_task_ids": task_ids(admitted),
                "deferred_task_ids": task_ids(deferred),
                "capacity_used": CAPACITY_LIMIT - capacity_remaining,
                "review_minutes_used": REVIEW_CAPACITY_LIMIT - review_remaining,
                "capacity_overrun": 0,
                "review_overrun": 0,
                "protected_review_erased_task_ids": [],
                "hidden_deferred_task_ids": [],
                "residual_refs": residual_refs_for_tick,
            }
        )

    return route_summary("selected", events, completed, residual_refs=residual_refs)


def simulate_latency_only_review_erasure() -> dict[str, Any]:
    events: list[dict[str, Any]] = []
    pending: list[dict[str, Any]] = []
    completed: list[dict[str, Any]] = []
    hidden_deferrals: list[str] = []
    protected_review_erased: list[str] = []

    for tick in range(HORIZON_TICKS):
        pending.extend(arrived_tasks(tick))
        capacity_remaining = CAPACITY_LIMIT
        admitted: list[dict[str, Any]] = []
        deferred: list[dict[str, Any]] = []

        for task in sorted(pending, key=task_sort_key):
            cost = int(task["capacity_cost"])
            if cost <= capacity_remaining:
                admitted.append(task)
                completed.append(task)
                capacity_remaining -= cost
                if str(task["risk"]) in {"critical", "high"} and int(task["review_minutes"]) > 0:
                    protected_review_erased.append(str(task["task_id"]))
            else:
                deferred.append(task)

        hidden_deferrals.extend(task_ids(deferred))
        pending = deferred
        events.append(
            {
                "tick": tick,
                "admitted_task_ids": task_ids(admitted),
                "deferred_task_ids": [],
                "capacity_used": CAPACITY_LIMIT - capacity_remaining,
                "review_minutes_used": 0,
                "capacity_overrun": 0,
                "review_overrun": 0,
                "protected_review_erased_task_ids": [
                    str(task["task_id"])
                    for task in admitted
                    if str(task["risk"]) in {"critical", "high"} and int(task["review_minutes"]) > 0
                ],
                "hidden_deferred_task_ids": task_ids(deferred),
                "residual_refs": [],
            }
        )

    return route_summary(
        "negative_control",
        events,
        completed,
        hidden_deferrals=hidden_deferrals,
        protected_review_erased=protected_review_erased,
    )


def route_summary(
    role: str,
    events: list[dict[str, Any]],
    completed: list[dict[str, Any]],
    *,
    residual_refs: list[str] | None = None,
    hidden_deferrals: list[str] | None = None,
    protected_review_erased: list[str] | None = None,
) -> dict[str, Any]:
    residual_refs = residual_refs or []
    hidden_deferrals = hidden_deferrals or []
    protected_review_erased = protected_review_erased or []
    completed_ids = task_ids(completed)
    all_completed = sorted(completed_ids) == sorted(task_ids(WORKLOAD))
    total_capacity_overrun = sum(int(event["capacity_overrun"]) for event in events)
    total_review_overrun = sum(int(event["review_overrun"]) for event in events)
    peak_capacity_overrun = max(int(event["capacity_overrun"]) for event in events)
    peak_review_overrun = max(int(event["review_overrun"]) for event in events)
    total_deferred_task_ticks = sum(len(event["deferred_task_ids"]) for event in events)
    total_hidden_deferred_task_ticks = sum(len(event["hidden_deferred_task_ids"]) for event in events)
    protected_review_violation_count = len(protected_review_erased)
    quality_pass = (
        all_completed
        and protected_review_violation_count == 0
        and total_hidden_deferred_task_ticks == 0
        and (role != "selected" or total_deferred_task_ticks == len(residual_refs))
    )
    load_instability_units = total_capacity_overrun + total_review_overrun
    return {
        "completed_task_count": len(set(completed_ids)),
        "all_tasks_completed": all_completed,
        "completed_task_ids": sorted(set(completed_ids)),
        "total_value_points_completed": sum(int(task["value_points"]) for task in completed),
        "total_capacity_used": sum(int(event["capacity_used"]) for event in events),
        "total_review_minutes_used": sum(int(event["review_minutes_used"]) for event in events),
        "total_capacity_overrun": total_capacity_overrun,
        "total_review_overrun": total_review_overrun,
        "peak_capacity_overrun": peak_capacity_overrun,
        "peak_review_overrun": peak_review_overrun,
        "load_instability_units": load_instability_units,
        "total_deferred_task_ticks": total_deferred_task_ticks,
        "total_hidden_deferred_task_ticks": total_hidden_deferred_task_ticks,
        "protected_review_violation_count": protected_review_violation_count,
        "protected_review_erased_task_ids": sorted(set(protected_review_erased)),
        "residualized_deferred_task_ticks": len(residual_refs),
        "hidden_deferred_task_ids": sorted(set(hidden_deferrals)),
        "quality_pass": quality_pass,
        "events": events,
    }


def run_route(route: dict[str, str]) -> dict[str, Any]:
    if route["strategy"] == "admit_arrivals":
        metrics = simulate_admit_arrivals()
    elif route["strategy"] == "protected_capacity_smoothing":
        metrics = simulate_protected_capacity_smoothing()
    elif route["strategy"] == "latency_only_review_erasure":
        metrics = simulate_latency_only_review_erasure()
    else:
        raise ValueError(f"Unknown strategy: {route['strategy']}")
    return {
        "route_id": route["route_id"],
        "role": route["role"],
        "strategy": route["strategy"],
        "quality_scope": route["quality_scope"],
        "eligible": bool(metrics["quality_pass"]),
        **metrics,
    }


def artifact_stat(relative: str) -> dict[str, Any]:
    path = ROOT / relative
    raw = path.read_bytes()
    text = raw.decode("utf-8", errors="ignore")
    return {
        "path": relative,
        "bytes": len(raw),
        "lines": text.count("\n") + (0 if text.endswith("\n") or not text else 1),
        "sha256": sha256_bytes(raw),
    }


def build_record() -> dict[str, Any]:
    route_records = [run_route(route) for route in ROUTES]
    baseline = next(route for route in route_records if route["role"] == "baseline")
    selected = next(route for route in route_records if route["role"] == "selected")
    negative = next(route for route in route_records if route["role"] == "negative_control")
    baseline_instability = int(baseline["load_instability_units"])
    selected_instability = int(selected["load_instability_units"])
    observed_reduction = (
        round((1 - (selected_instability / baseline_instability)) * 100, 3)
        if baseline_instability > 0
        else 0.0
    )
    accepted = (
        baseline["quality_pass"]
        and selected["quality_pass"]
        and not negative["quality_pass"]
        and selected_instability < baseline_instability
        and selected["protected_review_violation_count"] == 0
        and selected["total_capacity_overrun"] == 0
        and selected["total_review_overrun"] == 0
    )
    lean_expected = {
        "task_count": len(WORKLOAD),
        "route_count": len(ROUTES),
        "baseline_peak_capacity_overrun": baseline["peak_capacity_overrun"],
        "baseline_total_overrun": baseline_instability,
        "selected_peak_capacity_overrun": selected["peak_capacity_overrun"],
        "selected_total_overrun": selected_instability,
        "selected_deferred_task_ticks": selected["total_deferred_task_ticks"],
        "selected_residualized_deferred_task_ticks": selected["residualized_deferred_task_ticks"],
        "negative_protected_review_violations": negative["protected_review_violation_count"],
    }
    return {
        "probe_id": PROBE_ID,
        "record_kind": "resource_load_stability_probe",
        "recorded_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
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
        "pass": accepted,
        "selected_route_id": selected["route_id"],
        "baseline_route_id": baseline["route_id"],
        "negative_control_route_id": negative["route_id"],
        "selected_vs_baseline_instability_reduction_percent": observed_reduction,
        "selected_has_no_capacity_or_review_overrun": selected["total_capacity_overrun"] == 0 and selected["total_review_overrun"] == 0,
        "selected_residualized_all_deferrals": selected["total_deferred_task_ticks"] == selected["residualized_deferred_task_ticks"],
        "negative_control_rejected": not negative["quality_pass"],
        "negative_control_uses_less_review_than_selected": negative["total_review_minutes_used"] < selected["total_review_minutes_used"],
        "summary": "Local synthetic Resource Economics load-stability probe selected protected capacity smoothing over admit-arrivals baseline by reducing finite workload overload while rejecting a cheaper review-erasure route.",
        "workload": WORKLOAD,
        "routes": route_records,
        "lean_fixture_alignment": {
            "module": "AsiStackProofs.ResourceEconomics",
            "theorem_refs": [
                "resource_load_smoothing_workload_fixture_valid",
                "resource_load_smoothing_workload_reduces_overrun",
                "resource_load_smoothing_workload_rejects_review_erasure",
                "resource_load_smoothing_workload_residualizes_deferrals",
                "resource_load_smoothing_workload_has_no_support_promotion",
            ],
            "expected": lean_expected,
        },
        "residuals": RESIDUALS,
        "non_claims": NON_CLAIMS,
        "artifact_refs": [*TRACKED_ARTIFACTS, str(RESULT.relative_to(ROOT))],
        "tracked_artifacts": [artifact_stat(path) for path in TRACKED_ARTIFACTS],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Resource Economics load-stability probe.")
    parser.add_argument("--write-result", action="store_true", help=f"write {RESULT.relative_to(ROOT)}")
    args = parser.parse_args()

    record = build_record()
    text = json.dumps(record, indent=2, sort_keys=True) + "\n"
    if args.write_result:
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(text, encoding="utf-8")
        print(f"Wrote {RESULT.relative_to(ROOT)}")
    else:
        print(text, end="")
    if not record["pass"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
