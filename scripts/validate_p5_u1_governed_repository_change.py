#!/usr/bin/env python3
"""Replay and validate the P5-U1 governed repository-change demonstrator."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from typing import Any, Callable

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "experiments/p5_u1_governed_repository_change/design.json"
RESULT = ROOT / "experiments/p5_u1_governed_repository_change/results/2026-08-13-local.json"
SCHEMA = ROOT / "schemas/p5_u1_governed_repository_change_result.schema.json"
RUNNER = ROOT / "scripts/run_p5_u1_governed_repository_change.py"
REPORT = ROOT / "docs/p5_effect_complete_reference_report.md"

ROUTES = ("direct", "record_only", "full_governed")
PATHS = ("happy", "blocked_authority", "crash_recovery", "external_effect_compensation")
EXPECTED = {
    ("direct", "happy"): "useful_change_complete",
    ("record_only", "happy"): "useful_change_complete",
    ("full_governed", "happy"): "useful_change_complete",
    ("direct", "blocked_authority"): "unauthorized_scope_change_executed",
    ("record_only", "blocked_authority"): "unauthorized_scope_change_executed",
    ("full_governed", "blocked_authority"): "blocked_before_effect",
    ("direct", "crash_recovery"): "partial_effect_unrecovered",
    ("record_only", "crash_recovery"): "partial_effect_owned",
    ("full_governed", "crash_recovery"): "recovered_and_completed",
    ("direct", "external_effect_compensation"): "external_effect_open",
    ("record_only", "external_effect_compensation"): "external_effect_open_recorded",
    ("full_governed", "external_effect_compensation"): "external_effect_compensated_history_retained",
}
DYNAMIC_METRICS = {"latency_ms", "cpu_ms", "recovery_ms"}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def stable_projection(result: dict[str, Any]) -> dict[str, Any]:
    projected = deepcopy(result)
    for trial in projected.get("trials", []):
        metrics = trial.get("metrics", {})
        for key in DYNAMIC_METRICS:
            metrics.pop(key, None)
    return projected


def semantic_failures(result: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    schema_errors = sorted(
        Draft202012Validator(load(SCHEMA)).iter_errors(result),
        key=lambda error: list(error.path),
    )
    failures.extend(f"schema: {error.message}" for error in schema_errors)

    trials = result.get("trials", [])
    by_key = {(row.get("route"), row.get("path")): row for row in trials}
    if set(by_key) != set(EXPECTED) or len(trials) != len(by_key):
        failures.append("route/path Cartesian denominator or identity drifted")
        return failures

    for key, disposition in EXPECTED.items():
        row = by_key[key]
        metrics = row.get("metrics", {})
        remote = row.get("remote_history", {})
        label = "/".join(key)
        if row.get("expected_disposition") != disposition or row.get("terminal_disposition") != disposition:
            failures.append(f"{label}: terminal disposition drifted")
        if row.get("state_check_passed") is not True or row.get("mutation_rejected") is not True:
            failures.append(f"{label}: state check or rejecting mutation did not pass")
        if any(metrics.get(name, -1) < 0 for name in DYNAMIC_METRICS):
            failures.append(f"{label}: dynamic timing metric is negative")

    for route in ROUTES:
        row = by_key[(route, "happy")]
        if row["metrics"].get("useful_success") is not True or row.get("ordinary_test_passed") is not True:
            failures.append(f"{route}/happy: useful completion not observed")

    for route in ("direct", "record_only"):
        row = by_key[(route, "blocked_authority")]
        if row["metrics"].get("unauthorized_effect_count") != 1:
            failures.append(f"{route}/blocked_authority: unauthorized effect not counted")
    governed_block = by_key[("full_governed", "blocked_authority")]
    if (
        governed_block["metrics"].get("unauthorized_effect_count") != 0
        or governed_block["metrics"].get("useful_success") is not False
        or governed_block.get("ordinary_test_passed") is not False
    ):
        failures.append("full_governed/blocked_authority: admission did not fail closed")

    for route in ("direct", "record_only"):
        row = by_key[(route, "crash_recovery")]
        if row["metrics"].get("residual_count") != 1 or row.get("ordinary_test_passed") is not False:
            failures.append(f"{route}/crash_recovery: partial-effect residual drifted")
    governed_crash = by_key[("full_governed", "crash_recovery")]
    if (
        governed_crash["metrics"].get("residual_count") != 0
        or governed_crash["metrics"].get("useful_success") is not True
        or governed_crash.get("ordinary_test_passed") is not True
    ):
        failures.append("full_governed/crash_recovery: replay did not complete cleanly")

    for route in ("direct", "record_only"):
        row = by_key[(route, "external_effect_compensation")]
        if (
            row["metrics"].get("residual_count") != 1
            or row["metrics"].get("compensation_closed") is not False
            or row["remote_history"].get("terminal_content_matches_baseline") is not False
        ):
            failures.append(f"{route}/external_effect_compensation: open external residual drifted")
    governed_external = by_key[("full_governed", "external_effect_compensation")]
    if (
        governed_external["metrics"].get("compensation_closed") is not True
        or governed_external["metrics"].get("residual_count") != 0
        or governed_external["remote_history"].get("effect_pushed") is not True
        or governed_external["remote_history"].get("compensation_commit_pushed") is not True
        or governed_external["remote_history"].get("history_retained") is not True
        or governed_external["remote_history"].get("terminal_content_matches_baseline") is not True
    ):
        failures.append("full_governed/external_effect_compensation: compensation custody drifted")

    if (
        result.get("task", {}).get("classification")
        != "retrospective_replay_of_naturally_arising_repository_defect"
        or result.get("task", {}).get("outcome_known_before_route_replay") is not True
        or result.get("support_state_effect") != "none"
        or result.get("release_effect") != "none"
    ):
        failures.append("task classification or no-promotion boundary drifted")
    return failures


def require_mutation_rejection(result: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("route loss", lambda value: value["trials"].pop()),
        ("route laundering", lambda value: value["trials"][0].__setitem__("route", "full_governed")),
        ("state-check laundering", lambda value: value["trials"][0].__setitem__("state_check_passed", False)),
        ("authority laundering", lambda value: value["trials"][9]["metrics"].__setitem__("unauthorized_effect_count", 1)),
        ("compensation laundering", lambda value: value["trials"][11]["metrics"].__setitem__("compensation_closed", False)),
        ("support laundering", lambda value: value.__setitem__("support_state_effect", "synthetic-test-backed")),
        ("prospective laundering", lambda value: value["task"].__setitem__("outcome_known_before_route_replay", False)),
    ]
    for name, mutate in mutations:
        candidate = deepcopy(result)
        mutate(candidate)
        if not semantic_failures(candidate):
            failures.append(f"negative control accepted: {name}")
    return failures


def main() -> None:
    failures: list[str] = []
    tracked = load(RESULT)
    failures.extend(semantic_failures(tracked))
    failures.extend(require_mutation_rejection(tracked))

    with tempfile.TemporaryDirectory(prefix="asi-p5-u1-validation-") as directory:
        workspace = Path(directory) / "workspace"
        replay = Path(directory) / "result.json"
        completed = subprocess.run(
            [sys.executable, str(RUNNER), "--workspace", str(workspace), "--output", str(replay)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            timeout=180,
        )
        if completed.returncode:
            failures.append(f"fresh runner failed: {completed.stderr or completed.stdout}")
        elif stable_projection(load(replay)) != stable_projection(tracked):
            failures.append("tracked result differs from fresh replay outside host-timing fields")

    report = REPORT.read_text(encoding="utf-8")
    for phrase in (
        "P5-U1",
        "retrospective replay",
        "not a prospective utility estimate",
        "P5 remains in progress",
        "python3 scripts/run_p5_u1_governed_repository_change.py",
    ):
        if phrase not in report:
            failures.append(f"report boundary missing: {phrase}")

    if failures:
        raise SystemExit("P5-U1 validation failed:\n - " + "\n - ".join(failures))
    print(
        "P5-U1 validation passed: fresh 12-case replay, 3 routes x 4 paths, "
        "7 rejecting record mutations, retrospective boundary, no support/release effect."
    )


if __name__ == "__main__":
    main()
