#!/usr/bin/env python3
"""Generate and validate the non-infrastructure measured-slice status ledger."""

from __future__ import annotations

import argparse
from collections import Counter
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "docs" / "v1_0_candidate_status.md"
LEDGER = ROOT / "docs" / "non_infrastructure_measured_slice_status_ledger.md"

COSTED_RESULT = ROOT / "experiments" / "costed_route_resource_slice" / "results" / "2026-06-29-local.json"
WORKFLOW_RESULT = ROOT / "experiments" / "resource_workflow_trace" / "results" / "2026-07-01-local.json"
LIVE_PROBE = ROOT / "experiments" / "resource_live_probe" / "results" / "2026-07-01-local.json"
WORKLOAD_QUALITY = ROOT / "experiments" / "resource_workload_quality_probe" / "results" / "2026-07-01-local.json"
LOAD_STABILITY = ROOT / "experiments" / "resource_load_stability_probe" / "results" / "2026-07-01-local.json"
CI_PROFILE = ROOT / "experiments" / "resource_ci_cost_profile" / "results" / "2026-07-04-main.json"

TRANSITIONS = (
    ROOT / "evidence_transitions" / "v1_0_measured" / "costed_route_resource_slice_synthetic_test_backed.json",
    ROOT / "evidence_transitions" / "v1_x_measured" / "resource_load_stability_selector_synthetic_test_backed.json",
    ROOT / "evidence_transitions" / "v1_x_measured" / "resource_workload_quality_selector_empirical_test_backed.json",
)

STATUS_DOCS = (
    "docs/costed_route_resource_slice.md",
    "docs/resource_workflow_trace.md",
    "docs/resource_live_probe.md",
    "docs/resource_workload_quality_probe.md",
    "docs/resource_load_stability_probe.md",
    "docs/resource_ci_cost_profile.md",
)

VALIDATORS = (
    "python3 scripts/validate_costed_route_resource_slice.py",
    "python3 scripts/validate_resource_workflow_trace.py",
    "python3 scripts/validate_resource_live_probe.py",
    "python3 scripts/validate_resource_workload_quality_probe.py",
    "python3 scripts/validate_resource_load_stability_probe.py",
    "python3 scripts/validate_resource_ci_cost_profile.py",
)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def qmd_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def selected_route(routes: list[dict[str, Any]], role: str) -> dict[str, Any]:
    for route in routes:
        if route.get("role") == role:
            return route
    return {}


def status_state_phrase(counter: Counter[str]) -> str:
    return ", ".join(f"{count} `{key}`" for key, count in sorted(counter.items()))


def compact_status_row(metrics: dict[str, Any] | None = None) -> str:
    if metrics is None:
        metrics, errors = collect_metrics()
        if errors:
            raise RuntimeError("; ".join(errors))
    support_phrase = status_state_phrase(metrics["transition_support_states"])
    return (
        "| Non-infrastructure measured slice | "
        f"Resource Economics measured/replayed detail is generated in `docs/non_infrastructure_measured_slice_status_ledger.md`: "
        f"{metrics['accepted_transition_count']} accepted bounded non-core transitions ({support_phrase}), "
        f"{metrics['resource_artifact_count']} local Resource result artifacts, "
        f"{metrics['live_replay_count']} replayed validators, "
        f"{metrics['route_probe_count']} route-selection probes, "
        f"{metrics['ci_run_count']} GitHub Pages runs classified, and all chapter-core/non-claim boundaries preserved. "
        "| `docs/non_infrastructure_measured_slice_status_ledger.md`; "
        "`docs/costed_route_resource_slice.md`; "
        "`docs/resource_workflow_trace.md`; "
        "`docs/resource_live_probe.md`; "
        "`docs/resource_workload_quality_probe.md`; "
        "`docs/resource_load_stability_probe.md`; "
        "`docs/resource_ci_cost_profile.md`; "
        "`lean/AsiStackProofs/ResourceEconomics.lean`; "
        "`evidence_transitions/v1_0_measured/costed_route_resource_slice_synthetic_test_backed.json`; "
        "`evidence_transitions/v1_x_measured/resource_load_stability_selector_synthetic_test_backed.json`; "
        "`evidence_transitions/v1_x_measured/resource_workload_quality_selector_empirical_test_backed.json`; "
        "`python3 scripts/validate_non_infrastructure_measured_slice_status_ledger.py` |"
    )


def collect_metrics() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    required_paths = [
        COSTED_RESULT,
        WORKFLOW_RESULT,
        LIVE_PROBE,
        WORKLOAD_QUALITY,
        LOAD_STABILITY,
        CI_PROFILE,
        *TRANSITIONS,
        *(ROOT / path for path in STATUS_DOCS),
    ]
    for path in required_paths:
        if not path.exists():
            errors.append(f"required path missing: {rel(path)}")
    if errors:
        return {}, errors

    costed = load_json(COSTED_RESULT)
    workflow = load_json(WORKFLOW_RESULT)
    live = load_json(LIVE_PROBE)
    workload_quality = load_json(WORKLOAD_QUALITY)
    load_stability = load_json(LOAD_STABILITY)
    ci_profile = load_json(CI_PROFILE)
    transitions = [load_json(path) for path in TRANSITIONS]

    if costed.get("verification_result") != "pass":
        errors.append("costed route/resource slice must record verification_result pass.")
    if costed.get("selected_route") != "route://bounded-transform-plus-verifier":
        errors.append("costed route/resource slice selected route drifted.")
    if costed.get("cost_reduction_vs_baseline_percent") != 66.98:
        errors.append("costed route/resource slice reduction must remain 66.98 percent.")
    if costed.get("support_state_effect") != "eligible_for_bounded_evidence_review":
        errors.append("costed route/resource support_state_effect drifted.")

    if workflow.get("step_count") != 3 or workflow.get("total_cost_units") != 119.7:
        errors.append("resource workflow trace must remain a three-step, 119.7-cost-unit trace.")
    if workflow.get("expected_invalid_fixture_count") != 5:
        errors.append("resource workflow trace must keep five expected-invalid controls.")
    if workflow.get("support_state_effect") != "none":
        errors.append("resource workflow trace support_state_effect must remain none.")

    if live.get("pass") is not True:
        errors.append("resource live probe must record pass true.")
    live_replays = live.get("replay_commands", [])
    live_artifacts = live.get("tracked_artifacts", [])
    if len(live_replays) != 5:
        errors.append("resource live probe must record five replayed validators.")
    if live.get("support_state_effect") != "none":
        errors.append("resource live probe support_state_effect must remain none.")

    workload_routes = workload_quality.get("routes", [])
    workload_selected = selected_route(workload_routes, "selected")
    if workload_quality.get("pass") is not True:
        errors.append("resource workload-quality probe must record pass true.")
    if len(workload_routes) != 3:
        errors.append("resource workload-quality probe must keep three route candidates.")
    if workload_selected.get("sample_count") != 5:
        errors.append("resource workload-quality selected route must keep five measured samples.")
    if workload_quality.get("selected_route_id") != "route://selected-scoped-workflow-trace-validator":
        errors.append("resource workload-quality selected route drifted.")
    if workload_quality.get("negative_control_rejected") is not True:
        errors.append("resource workload-quality negative control must remain rejected.")
    if workload_quality.get("support_state_effect") != "none":
        errors.append("resource workload-quality support_state_effect must remain none.")

    load_routes = load_stability.get("routes", [])
    load_selected = selected_route(load_routes, "selected")
    if load_stability.get("pass") is not True:
        errors.append("resource load-stability probe must record pass true.")
    if len(load_stability.get("workload", [])) != 10:
        errors.append("resource load-stability workload must keep ten tasks.")
    if load_stability.get("selected_route_id") != "route://selected-protected-capacity-smoothing":
        errors.append("resource load-stability selected route drifted.")
    if load_stability.get("selected_vs_baseline_instability_reduction_percent") != 100.0:
        errors.append("resource load-stability reduction must remain 100.0 percent.")
    if load_selected.get("residualized_deferred_task_ticks") != 7:
        errors.append("resource load-stability selected route must keep seven residualized deferrals.")
    if load_stability.get("negative_control_rejected") is not True:
        errors.append("resource load-stability negative control must remain rejected.")
    if load_stability.get("support_state_effect") != "none":
        errors.append("resource load-stability support_state_effect must remain none.")

    ci_metrics = ci_profile.get("metrics", {})
    if ci_metrics.get("run_count") != 8 or ci_metrics.get("completed_run_count") != 8:
        errors.append("resource CI profile must keep eight completed Pages runs.")
    if ci_metrics.get("success_count") != 5 or ci_metrics.get("failure_count") != 3:
        errors.append("resource CI profile success/failure counts drifted.")
    if ci_profile.get("support_state_effect") != "none":
        errors.append("resource CI profile support_state_effect must remain none.")

    transition_support_states: Counter[str] = Counter()
    transition_claims: list[str] = []
    for transition in transitions:
        if transition.get("review_status") != "accepted":
            errors.append(f"transition {transition.get('transition_id')} must remain accepted.")
        if transition.get("transition_effect") != "upward":
            errors.append(f"transition {transition.get('transition_id')} must remain an upward bounded transition.")
        if transition.get("support_state_effect") != "eligible_for_bounded_evidence_review":
            errors.append(f"transition {transition.get('transition_id')} support_state_effect drifted.")
        transition_support_states[transition.get("new_support_state", "missing")] += 1
        transition_claims.append(transition.get("claim_id", "missing"))
        transition_text = " ".join(
            [
                str(transition.get("scope_boundary", "")),
                str(transition.get("transition_reason", "")),
                " ".join(str(item) for item in transition.get("non_claims", [])),
            ]
        )
        if "chapter core" not in transition_text and "chapter-core" not in transition_text:
            errors.append(f"transition {transition.get('transition_id')} must preserve chapter-core boundary.")

    metrics = {
        "accepted_transition_count": len(transitions),
        "transition_support_states": transition_support_states,
        "transition_claims": transition_claims,
        "resource_artifact_count": 6,
        "route_probe_count": 3,
        "costed_selected_route": costed.get("selected_route"),
        "costed_baseline_route": costed.get("baseline_route"),
        "costed_negative_controls": costed.get("negative_control_routes", []),
        "costed_reduction": costed.get("cost_reduction_vs_baseline_percent"),
        "workflow_steps": workflow.get("step_count"),
        "workflow_cost_units": workflow.get("total_cost_units"),
        "workflow_expected_invalid": workflow.get("expected_invalid_fixture_count"),
        "live_replay_count": len(live_replays),
        "live_tracked_artifact_count": len(live_artifacts),
        "workload_quality_route_count": len(workload_routes),
        "workload_quality_sample_count": workload_selected.get("sample_count"),
        "workload_quality_selected_route": workload_quality.get("selected_route_id"),
        "workload_quality_reduction": workload_quality.get("observed_selected_vs_baseline_elapsed_reduction_percent"),
        "load_stability_workload_count": len(load_stability.get("workload", [])),
        "load_stability_selected_route": load_stability.get("selected_route_id"),
        "load_stability_reduction": load_stability.get("selected_vs_baseline_instability_reduction_percent"),
        "load_stability_residualized_deferrals": load_selected.get("residualized_deferred_task_ticks"),
        "ci_run_count": ci_metrics.get("run_count"),
        "ci_completed_run_count": ci_metrics.get("completed_run_count"),
        "ci_success_count": ci_metrics.get("success_count"),
        "ci_failure_count": ci_metrics.get("failure_count"),
        "ci_median_duration": ci_metrics.get("completed_duration_seconds_median"),
        "ci_repair_events": len(ci_profile.get("repair_events", [])),
    }
    return metrics, errors


def build_report(metrics: dict[str, Any], errors: list[str]) -> str:
    validation_lines = ["- None."] if not errors else [f"- {error}" for error in errors]
    return "\n".join(
        [
            "# Non-Infrastructure Measured Slice Status Ledger",
            "",
            "Generated by `python3 scripts/validate_non_infrastructure_measured_slice_status_ledger.py --write`.",
            "",
            "This ledger replaces the former long `Non-infrastructure measured slice` cell in `docs/v1_0_candidate_status.md`. It records the Resource Economics measured/replayed evidence lane without turning bounded local selectors, probes, or CI metadata into broader Resource Economics, scheduler, benchmark, model-quality, safety, or chapter-core claims.",
            "",
            "## Summary",
            "",
            "| Metric | Value |",
            "|---|---:|",
            f"| Accepted bounded non-core transitions | {metrics['accepted_transition_count']} |",
            f"| Transition support states | {qmd_escape(status_state_phrase(metrics['transition_support_states']))} |",
            f"| Local Resource result artifacts | {metrics['resource_artifact_count']} |",
            f"| Replayed validators in live probe | {metrics['live_replay_count']} |",
            f"| Route-selection probes | {metrics['route_probe_count']} |",
            f"| GitHub Pages runs classified | {metrics['ci_run_count']} |",
            f"| GitHub Pages completed runs | {metrics['ci_completed_run_count']} |",
            f"| GitHub Pages success/failure split | {metrics['ci_success_count']} / {metrics['ci_failure_count']} |",
            "",
            "## Status-Page Row",
            "",
            compact_status_row(metrics),
            "",
            "## Accepted Narrow Transitions",
            "",
            "| Claim | New support state | Boundary |",
            "|---|---|---|",
            "| `resource-economics.costed_route_budget_slice` | `synthetic-test-backed` | Four costed route/resource records; cheaper failed-verification and hidden-residual controls rejected; no chapter-core promotion. |",
            "| `resource-economics.finite_burst_load_smoothing_selector` | `synthetic-test-backed` | Ten-task synthetic burst-review selector; review-erasure negative control rejected; no real load-stability or scheduler claim. |",
            "| `resource-economics.scoped_workflow_trace_route_selector` | `empirical-test-backed` | Local five-sample scoped repository-task selector; no stable-speedup, production, benchmark, or chapter-core claim. |",
            "",
            "## Resource Evidence Lane",
            "",
            f"- `docs/costed_route_resource_slice.md` records selected route `{metrics['costed_selected_route']}`, baseline `{metrics['costed_baseline_route']}`, {metrics['costed_reduction']} percent synthetic cost reduction, and rejected negative controls {qmd_escape(', '.join(metrics['costed_negative_controls']))}.",
            f"- `docs/resource_workflow_trace.md` records a {metrics['workflow_steps']}-step deterministic workflow trace with {metrics['workflow_cost_units']} cost units and {metrics['workflow_expected_invalid']} expected-invalid controls.",
            f"- `docs/resource_live_probe.md` records {metrics['live_replay_count']} local validator replays and {metrics['live_tracked_artifact_count']} tracked artifact digests with support-state effect `none`.",
            f"- `docs/resource_workload_quality_probe.md` records {metrics['workload_quality_route_count']} local route candidates, {metrics['workload_quality_sample_count']} samples per route for the selected route, selected route `{metrics['workload_quality_selected_route']}`, and {metrics['workload_quality_reduction']} percent observed selected-vs-baseline elapsed reduction for the scoped local task.",
            f"- `docs/resource_load_stability_probe.md` records a {metrics['load_stability_workload_count']}-task synthetic burst-review workload, selected route `{metrics['load_stability_selected_route']}`, {metrics['load_stability_reduction']} percent finite instability reduction, and {metrics['load_stability_residualized_deferrals']} residualized deferred task-ticks.",
            f"- `docs/resource_ci_cost_profile.md` records {metrics['ci_run_count']} GitHub Pages runs, {metrics['ci_completed_run_count']} completed runs, {metrics['ci_success_count']} successful completed runs, {metrics['ci_failure_count']} classified deploy-service failures, median completed duration {metrics['ci_median_duration']} seconds, and {metrics['ci_repair_events']} repair-event records as publication-pipeline metadata only.",
            "",
            "## Non-Claim Boundary",
            "",
            "- This ledger does not promote the Resource Economics chapter core claim.",
            "- This ledger does not prove deployed routing, production scheduling, stable speedup, real load stability, model quality, benchmark quality, safety, economic outcome, physical feasibility, or source-interpretation adequacy.",
            "- CI cost-profile rows are publication-pipeline metadata, not chapter evidence results.",
            "- Broader Resource Economics claims still require separate live or externally reviewable workload traces, hidden-cost audits, residual/displaced-cost accounting, baseline controls, and independent review where relevant.",
            "",
            "## Validation Errors",
            "",
            *validation_lines,
            "",
        ]
    )


def write_status_row(row: str) -> None:
    lines = STATUS.read_text(encoding="utf-8").splitlines()
    matches = [index for index, line in enumerate(lines) if line.startswith("| Non-infrastructure measured slice |")]
    if len(matches) != 1:
        fail([f"{rel(STATUS)} must contain exactly one Non-infrastructure measured slice row; found {len(matches)}."])
    lines[matches[0]] = row
    STATUS.write_text("\n".join(lines) + "\n", encoding="utf-8")


def fail(errors: list[str]) -> None:
    print("Non-infrastructure measured slice status ledger validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def validate(args: argparse.Namespace) -> list[str]:
    metrics, errors = collect_metrics()
    if not metrics:
        return errors
    report = build_report(metrics, errors)
    row = compact_status_row(metrics)

    if args.write:
        LEDGER.write_text(report, encoding="utf-8")
    if args.write_status_row:
        write_status_row(row)
    if args.write or args.write_status_row:
        return errors

    if not LEDGER.exists():
        errors.append(f"{rel(LEDGER)} is missing; run with --write.")
    elif LEDGER.read_text(encoding="utf-8") != report:
        errors.append(f"{rel(LEDGER)} is out of date; run with --write.")

    status_text = STATUS.read_text(encoding="utf-8")
    if row not in status_text:
        errors.append(f"{rel(STATUS)} is missing the compact non-infrastructure measured-slice row.")
    stale_fragments = (
        "The first bounded non-infrastructure measured/replayed slice checks four Costed Route Records",
        "The Resource CI cost profile records eight actual GitHub Pages runs",
    )
    for stale in stale_fragments:
        if stale in status_text:
            errors.append(f"{rel(STATUS)} still contains stale expanded measured-slice text: {stale}")
    for line in status_text.splitlines():
        if line.startswith("| Non-infrastructure measured slice |") and len(line) > 1200:
            errors.append(f"{rel(STATUS)} Non-infrastructure measured slice row is still too long: {len(line)} characters.")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="rewrite the tracked ledger")
    parser.add_argument("--write-status-row", action="store_true", help="rewrite the compact status row")
    args = parser.parse_args()
    errors = validate(args)
    if errors:
        fail(errors)
    action = "wrote" if args.write or args.write_status_row else "validated"
    metrics, _ = collect_metrics()
    print(
        f"Non-infrastructure measured slice status ledger {action}: "
        f"{metrics['accepted_transition_count']} transitions, "
        f"{metrics['live_replay_count']} replayed validators, "
        f"{metrics['ci_run_count']} CI runs."
    )


if __name__ == "__main__":
    main()
