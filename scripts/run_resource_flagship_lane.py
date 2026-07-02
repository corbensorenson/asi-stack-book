#!/usr/bin/env python3
"""Run the Resource Economics flagship evidence lane as one command.

This runner composes existing, narrower Resource Economics evidence artifacts.
It does not create a new chapter-core support transition. It records that the
selected flagship lane can be replayed from one command, that the existing
bounded costed-route slice has its accepted non-core transition, and that the
chapter-core claim remains covered by the explicit no-change decision.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shlex
import subprocess
import sys
import time
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "experiments" / "resource_flagship_lane" / "results" / "2026-07-01-local.json"
RUN_ID = "resource-flagship-lane-2026-07-01-local"
RESULT_COMMAND = "python3 scripts/run_resource_flagship_lane.py --write-result"

COMMANDS = [
    {
        "id": "costed_route_resource_slice",
        "command": "python3 scripts/validate_costed_route_resource_slice.py",
        "role": "accepted_bounded_transition",
    },
    {
        "id": "resource_workflow_trace",
        "command": "python3 scripts/validate_resource_workflow_trace.py",
        "role": "trace_property_fixture_bridge",
    },
    {
        "id": "resource_budget_ledgers",
        "command": "python3 scripts/validate_resource_budget_ledgers.py",
        "role": "budget_record_discipline",
    },
    {
        "id": "capacity_smoothing",
        "command": "python3 scripts/validate_capacity_smoothing.py",
        "role": "bounded_capacity_trace",
    },
    {
        "id": "resource_live_probe",
        "command": "python3 scripts/validate_resource_live_probe.py",
        "role": "local_replay_digest_probe",
    },
    {
        "id": "resource_workload_quality_probe",
        "command": "python3 scripts/validate_resource_workload_quality_probe.py",
        "role": "local_measured_workload_quality_probe",
    },
    {
        "id": "resource_load_stability_probe",
        "command": "python3 scripts/validate_resource_load_stability_probe.py",
        "role": "local_synthetic_load_stability_probe",
    },
    {
        "id": "resource_ci_cost_profile",
        "command": "python3 scripts/validate_resource_ci_cost_profile.py",
        "role": "publication_pipeline_cost_profile",
    },
    {
        "id": "simulation_transfer_boundaries",
        "command": "python3 scripts/validate_simulation_transfer_boundaries.py",
        "role": "folded_simulation_transfer_boundary",
    },
    {
        "id": "evidence_transitions",
        "command": "python3 scripts/validate_evidence_transitions.py",
        "role": "support_state_transition_boundary",
    },
]

TRACKED_ARTIFACTS = [
    "docs/costed_route_resource_slice.md",
    "docs/resource_workflow_trace.md",
    "docs/resource_live_probe.md",
    "docs/resource_workload_quality_probe.md",
    "docs/resource_load_stability_probe.md",
    "docs/resource_ci_cost_profile.md",
    "docs/simulation_transfer_boundary_harness.md",
    "docs/v1_x_active_evidence_cycle.md",
    "evidence_transitions/v1_0_measured/costed_route_resource_slice_synthetic_test_backed.json",
    "evidence_transitions/v1_0_pilot/resource_economics_no_change.json",
    "evidence_transitions/v1_x_measured/resource_workflow_trace_no_change.json",
    "evidence_transitions/v1_x_measured/resource_live_probe_no_change.json",
    "evidence_transitions/v1_x_measured/resource_workload_quality_probe_no_change.json",
    "evidence_transitions/v1_x_measured/resource_load_stability_probe_no_change.json",
    "evidence_transitions/v1_x_measured/resource_ci_cost_profile_no_change.json",
    "experiments/costed_route_resource_slice/results/2026-06-29-local.json",
    "experiments/resource_workflow_trace/results/2026-07-01-local.json",
    "experiments/resource_live_probe/results/2026-07-01-local.json",
    "experiments/resource_workload_quality_probe/results/2026-07-01-local.json",
    "experiments/resource_load_stability_probe/results/2026-07-01-local.json",
    "experiments/resource_ci_cost_profile/results/2026-07-01-main.json",
    "experiments/simulation_transfer_boundaries/results/2026-06-30-local.md",
    "lean/AsiStackProofs/ResourceEconomics.lean",
    "lean/AsiStackProofs/SimulationFidelity.lean",
]

SUBLANE_NO_PROMOTION_DECISION_REFS = [
    "evidence_transitions/v1_x_measured/resource_workflow_trace_no_change.json",
    "evidence_transitions/v1_x_measured/resource_live_probe_no_change.json",
    "evidence_transitions/v1_x_measured/resource_workload_quality_probe_no_change.json",
    "evidence_transitions/v1_x_measured/resource_load_stability_probe_no_change.json",
    "evidence_transitions/v1_x_measured/resource_ci_cost_profile_no_change.json",
]

NO_PROMOTION_DECISION_REFS = [
    "evidence_transitions/v1_0_pilot/resource_economics_no_change.json",
    *SUBLANE_NO_PROMOTION_DECISION_REFS,
]

NON_CLAIMS = [
    "This flagship lane runner does not promote the Resource Economics chapter core claim above argument.",
    "This flagship lane runner does not create a new support-state transition.",
    "This flagship lane runner does not prove deployed scheduler behavior, production queue behavior, TokenMana behavior, PlanForge behavior, KV-cache behavior, simulator adequacy, model quality, benchmark performance, safety outcomes, human productivity, or economic outcomes.",
    "This flagship lane runner is a local repository replay over tracked public-safe artifacts, not external review, live workload review, production scheduler logs, or artifact approval.",
]

RESIDUALS = [
    "The accepted upward transition remains scoped to resource-economics.costed_route_budget_slice, not the chapter core claim.",
    "Workload-quality timing is a local repository-task measurement and remains machine-load sensitive.",
    "Load-stability evidence is a finite synthetic burst-review workload with residualized deferrals, not a production queue trace.",
    "CI cost evidence is publication-pipeline metadata, not a scheduler or economic-result measurement.",
    "Simulation-transfer evidence is record discipline over declared contracts, not simulator adequacy or physical-feasibility validation.",
]


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def command_argv(command: str) -> list[str]:
    parts = shlex.split(command)
    if parts and parts[0] == "python3":
        return [sys.executable, *parts[1:]]
    return parts


def run_command(record: dict[str, str]) -> dict[str, Any]:
    started = time.perf_counter()
    result = subprocess.run(
        command_argv(record["command"]),
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    elapsed_ms = round((time.perf_counter() - started) * 1000, 3)
    combined = result.stdout + result.stderr
    excerpt = [line for line in combined.strip().splitlines() if line][:6]
    return {
        "id": record["id"],
        "command": record["command"],
        "role": record["role"],
        "exit_code": result.returncode,
        "elapsed_ms": elapsed_ms,
        "output_sha256": sha256_text(combined),
        "output_excerpt": excerpt,
    }


def load_json(relative: str) -> Any:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


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


def route_by_role(routes: list[dict[str, Any]], role: str) -> dict[str, Any]:
    matches = [route for route in routes if route.get("role") == role]
    return matches[0] if len(matches) == 1 else {}


def build_component_summary() -> dict[str, Any]:
    costed = load_json("experiments/costed_route_resource_slice/results/2026-06-29-local.json")
    transition = load_json(
        "evidence_transitions/v1_0_measured/costed_route_resource_slice_synthetic_test_backed.json"
    )
    no_change = load_json("evidence_transitions/v1_0_pilot/resource_economics_no_change.json")
    workflow = load_json("experiments/resource_workflow_trace/results/2026-07-01-local.json")
    live = load_json("experiments/resource_live_probe/results/2026-07-01-local.json")
    workload = load_json("experiments/resource_workload_quality_probe/results/2026-07-01-local.json")
    load_stability = load_json("experiments/resource_load_stability_probe/results/2026-07-01-local.json")
    ci_profile = load_json("experiments/resource_ci_cost_profile/results/2026-07-01-main.json")
    sublane_decisions = {
        Path(ref).stem: load_json(ref) for ref in SUBLANE_NO_PROMOTION_DECISION_REFS
    }

    workload_baseline = route_by_role(workload.get("routes", []), "baseline")
    workload_selected = route_by_role(workload.get("routes", []), "selected")
    workload_negative = route_by_role(workload.get("routes", []), "negative_control")
    load_baseline = route_by_role(load_stability.get("routes", []), "baseline")
    load_selected = route_by_role(load_stability.get("routes", []), "selected")
    load_negative = route_by_role(load_stability.get("routes", []), "negative_control")

    return {
        "accepted_non_core_transition": {
            "claim_id": transition.get("claim_id"),
            "new_support_state": transition.get("new_support_state"),
            "transition_validity_state": transition.get("transition_validity_state"),
            "selected_route": costed.get("selected_route"),
            "baseline_route": costed.get("baseline_route"),
            "negative_control_routes": costed.get("negative_control_routes"),
            "cost_reduction_vs_baseline_percent": costed.get("cost_reduction_vs_baseline_percent"),
            "support_state_effect": costed.get("support_state_effect"),
        },
        "chapter_core_decision": {
            "claim_id": no_change.get("claim_id"),
            "transition_effect": no_change.get("transition_effect"),
            "support_state_effect": no_change.get("support_state_effect"),
            "transition_validity_state": no_change.get("transition_validity_state"),
        },
        "workflow_trace": {
            "trace_id": workflow.get("trace_id"),
            "step_count": workflow.get("step_count"),
            "selected_route_count": len(workflow.get("selected_routes", [])),
            "expected_invalid_fixture_count": workflow.get("expected_invalid_fixture_count"),
            "support_state_effect": workflow.get("support_state_effect"),
            "lean_bridge": workflow.get("lean_fixture_alignment", {}).get("proof_bridge_type"),
        },
        "local_live_probe": {
            "probe_id": live.get("probe_id"),
            "replay_command_count": len(live.get("replay_commands", [])),
            "support_state_effect": live.get("support_state_effect"),
            "chapter_core_support_effect": live.get("chapter_core_support_effect"),
        },
        "workload_quality_probe": {
            "probe_id": workload.get("probe_id"),
            "baseline_route_id": workload.get("baseline_route_id"),
            "selected_route_id": workload.get("selected_route_id"),
            "negative_control_route_id": workload.get("negative_control_route_id"),
            "baseline_elapsed_ms": workload_baseline.get("elapsed_ms"),
            "selected_elapsed_ms": workload_selected.get("elapsed_ms"),
            "negative_control_elapsed_ms": workload_negative.get("elapsed_ms"),
            "observed_selected_vs_baseline_elapsed_reduction_percent": workload.get(
                "observed_selected_vs_baseline_elapsed_reduction_percent"
            ),
            "negative_control_rejected": workload.get("negative_control_rejected"),
            "support_state_effect": workload.get("support_state_effect"),
        },
        "load_stability_probe": {
            "probe_id": load_stability.get("probe_id"),
            "baseline_route_id": load_stability.get("baseline_route_id"),
            "selected_route_id": load_stability.get("selected_route_id"),
            "negative_control_route_id": load_stability.get("negative_control_route_id"),
            "baseline_load_instability_units": load_baseline.get("load_instability_units"),
            "selected_load_instability_units": load_selected.get("load_instability_units"),
            "selected_residualized_deferred_task_ticks": load_selected.get(
                "residualized_deferred_task_ticks"
            ),
            "negative_protected_review_violation_count": load_negative.get(
                "protected_review_violation_count"
            ),
            "negative_hidden_deferred_task_ticks": load_negative.get(
                "total_hidden_deferred_task_ticks"
            ),
            "selected_vs_baseline_instability_reduction_percent": load_stability.get(
                "selected_vs_baseline_instability_reduction_percent"
            ),
            "support_state_effect": load_stability.get("support_state_effect"),
        },
        "ci_cost_profile": {
            "profile_id": ci_profile.get("profile_id"),
            "workflow": ci_profile.get("workflow"),
            "metrics": ci_profile.get("metrics"),
            "support_state_effect": ci_profile.get("support_state_effect"),
        },
        "sublane_no_promotion_decisions": {
            decision_id: {
                "claim_id": decision.get("claim_id"),
                "transition_effect": decision.get("transition_effect"),
                "support_state_effect": decision.get("support_state_effect"),
                "verification_result": decision.get("verification_result"),
                "transition_validity_state": decision.get("transition_validity_state"),
            }
            for decision_id, decision in sorted(sublane_decisions.items())
        },
    }


def build_record() -> dict[str, Any]:
    command_records = [run_command(command) for command in COMMANDS]
    passed = all(record["exit_code"] == 0 for record in command_records)
    return {
        "schema_version": "0.1",
        "run_id": RUN_ID,
        "record_kind": "resource_flagship_lane_replay",
        "recorded_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "command": RESULT_COMMAND,
        "local_only": True,
        "public_safe": True,
        "pass": passed,
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
        "accepted_transition_refs": [
            "evidence_transitions/v1_0_measured/costed_route_resource_slice_synthetic_test_backed.json",
        ],
        "no_promotion_decision_refs": NO_PROMOTION_DECISION_REFS,
        "summary": (
            "One-command Resource Economics flagship lane replay over tracked public-safe evidence artifacts: "
            "bounded costed-route transition, workflow trace, budget ledgers, capacity smoothing, live replay, "
            "workload-quality, load-stability, CI cost, simulation-transfer, and transition-boundary checks."
        ),
        "command_records": command_records,
        "component_summary": build_component_summary(),
        "residuals": RESIDUALS,
        "non_claims": NON_CLAIMS,
        "artifact_refs": [*TRACKED_ARTIFACTS, str(RESULT.relative_to(ROOT))],
        "tracked_artifacts": [artifact_stat(path) for path in TRACKED_ARTIFACTS],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Resource Economics flagship evidence lane.")
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
