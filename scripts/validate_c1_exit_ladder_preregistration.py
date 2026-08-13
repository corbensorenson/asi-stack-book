#!/usr/bin/env python3
"""Validate the prospective C1-EL governed-cognition preregistration."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "experiments/c1_exit_ladder/preregistration.json"
SCHEMA = ROOT / "schemas/c1_exit_ladder_preregistration.schema.json"
ADMISSION = ROOT / "experiments/c1_exit_ladder/admission.json"
ADMISSION_SCHEMA = ROOT / "schemas/c1_exit_ladder_admission.schema.json"
DESIGN = ROOT / "experiments/c1_exit_ladder/design.json"
RUNNER = ROOT / "scripts/run_c1_exit_ladder.py"
RESULT = ROOT / "experiments/c1_exit_ladder/results/2026-08-13-local.json"
FAILURE = ROOT / "experiments/c1_exit_ladder/results/2026-08-13-instrument-failure.json"
FAILURE_SCHEMA = ROOT / "schemas/c1_exit_ladder_instrument_failure.schema.json"
EXPECTED_ROUTES = ["direct", "record_only", "full_governed"]
EXPECTED_OUTCOMES = {
    "useful_success", "unauthorized_effect_count", "false_block_count",
    "defect_escape_count", "latency_ms", "cpu_ms", "operator_step_proxy",
    "artifact_file_count", "artifact_bytes", "recovery_ms",
    "compensation_closed", "residual_count",
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def failures(protocol: dict) -> list[str]:
    out = [
        f"schema: {error.message}"
        for error in Draft202012Validator(load(SCHEMA)).iter_errors(protocol)
    ]
    routes = [row.get("id") for row in protocol.get("routes", [])]
    if routes != EXPECTED_ROUTES or len(routes) != len(set(routes)):
        out.append("three-route identity or order drifted")
    if set(protocol.get("outcomes", [])) != EXPECTED_OUTCOMES:
        out.append("joint outcome surface drifted")
    selection = protocol.get("task_selection", {})
    joined = " ".join(selection.get("eligible", []) + selection.get("excluded", [])).lower()
    for phrase in ("solution", "protected", "invented", "identical source", "acceptance"):
        if phrase not in joined:
            out.append(f"task chronology or matching boundary missing: {phrase}")
    if not selection.get("replacement_policy", "").startswith("No replacement after"):
        out.append("post-admission replacement prohibition drifted")
    inference = protocol.get("dispositions", {}).get("maximum_inference", "").lower()
    for phrase in ("one prospectively selected", "cannot estimate general utility", "cannot promote a chapter core"):
        if phrase not in inference:
            out.append(f"maximum-inference boundary missing: {phrase}")
    if (
        protocol.get("task_admitted") is not False
        or protocol.get("task_identity") is not None
        or protocol.get("protected_content_opened") is not False
        or protocol.get("support_state_effect") != "none"
        or protocol.get("release_effect") != "none"
    ):
        out.append("freeze opened a task, protected content, support, or release state")
    return out


def admission_failures(admission: dict) -> list[str]:
    out = [
        f"admission schema: {error.message}"
        for error in Draft202012Validator(load(ADMISSION_SCHEMA)).iter_errors(admission)
    ]
    chronology = admission.get("chronology", {})
    eligibility = admission.get("eligibility", {})
    if chronology.get("task_solution_known_at_admission") is not False:
        out.append("task solution was open at admission")
    if chronology.get("route_outcomes_known_at_admission") is not False:
        out.append("route outcomes were open at admission")
    if not all(
        eligibility.get(field) is True
        for field in (
            "independently_necessary", "public_safe", "machine_detectable",
            "disposable_git_workspace_compatible", "matched_route_inputs_possible",
        )
    ):
        out.append("admitted task lost a positive eligibility gate")
    if any(
        eligibility.get(field) is True
        for field in (
            "private_credential_required", "protected_task_content", "video_work",
            "invented_for_protocol",
        )
    ):
        out.append("admitted task crossed an exclusion boundary")
    if admission.get("freeze_commit") != admission.get("source_commit"):
        out.append("admitted task source does not match the freeze commit")
    if admission.get("support_state_effect") != "none" or admission.get("release_effect") != "none":
        out.append("task admission moved support or release state")
    return out


def terminal_failures(failure: dict, design: dict, runner_source: str) -> list[str]:
    out = [
        f"failure schema: {error.message}"
        for error in Draft202012Validator(load(FAILURE_SCHEMA)).iter_errors(failure)
    ]
    if RESULT.exists():
        out.append("a replacement success/negative result exists after terminal instrument failure")
    if failure.get("disposition") != "inconclusive":
        out.append("instrument failure disposition drifted")
    if failure.get("replacement_or_rerun_allowed_for_this_prospective_task") is not False:
        out.append("terminal failed attempt permits replacement or rerun")
    if failure.get("trial_outcome_claimed") is not False:
        out.append("instrument failure claims route outcomes")
    if design.get("source_commit") != failure.get("source_commit"):
        out.append("design and terminal failure source identities differ")
    if design.get("repair", {}).get("source_change_required") is not False:
        out.append("design invents a source change for the operational cache defect")
    try:
        compile(runner_source, str(RUNNER), "exec")
    except SyntaxError as exc:
        out.append(f"corrected runner does not compile: {exc}")
    if '"independent_external_observer": False' not in runner_source:
        out.append("future-consumer runner correction is absent")
    return out


def main() -> None:
    protocol = load(PROTOCOL)
    admission = load(ADMISSION)
    design = load(DESIGN)
    failure = load(FAILURE)
    runner_source = RUNNER.read_text(encoding="utf-8")
    out = (
        failures(protocol)
        + admission_failures(admission)
        + terminal_failures(failure, design, runner_source)
    )
    mutations = [
        ("task preadmitted", lambda value: value.__setitem__("task_admitted", True)),
        ("protected content opened", lambda value: value.__setitem__("protected_content_opened", True)),
        ("route removed", lambda value: value["routes"].pop()),
        ("baseline relabeled", lambda value: value["routes"][0].__setitem__("id", "full_governed")),
        ("outcome removed", lambda value: value["outcomes"].pop()),
        ("replacement allowed", lambda value: value["task_selection"].__setitem__("replacement_policy", "Replace a failed task.")),
        ("inference widened", lambda value: value["dispositions"].__setitem__("maximum_inference", "The architecture is generally useful.")),
        ("support promoted", lambda value: value.__setitem__("support_state_effect", "synthetic-test-backed")),
    ]
    for label, mutate in mutations:
        candidate = deepcopy(protocol)
        mutate(candidate)
        if not failures(candidate):
            out.append(f"negative control accepted: {label}")
    admission_mutations = [
        ("solution preopened", lambda value: value["chronology"].__setitem__("task_solution_known_at_admission", True)),
        ("route outcomes preopened", lambda value: value["chronology"].__setitem__("route_outcomes_known_at_admission", True)),
        ("task invented", lambda value: value["eligibility"].__setitem__("invented_for_protocol", True)),
        ("freeze source changed", lambda value: value.__setitem__("source_commit", "0" * 40)),
    ]
    for label, mutate in admission_mutations:
        candidate = deepcopy(admission)
        mutate(candidate)
        if not admission_failures(candidate):
            out.append(f"admission negative control accepted: {label}")
    terminal_mutations = [
        ("rerun allowed", lambda value: value.__setitem__("replacement_or_rerun_allowed_for_this_prospective_task", True)),
        ("route outcome claimed", lambda value: value.__setitem__("trial_outcome_claimed", True)),
        ("failure promoted", lambda value: value.__setitem__("support_state_effect", "synthetic-test-backed")),
    ]
    for label, mutate in terminal_mutations:
        candidate = deepcopy(failure)
        mutate(candidate)
        if not terminal_failures(candidate, design, runner_source):
            out.append(f"terminal negative control accepted: {label}")
    if out:
        raise SystemExit("C1-EL preregistration failed:\n - " + "\n - ".join(out))
    print(
        "C1-EL preregistration passed: first eligible post-freeze natural task, "
        "3 matched routes, 1 natural plus 3 injected paths, 12 outcomes, "
        "task admitted before solution inspection, terminal instrument failure retained, "
        "15 mutations rejected, protected/support/release state closed."
    )


if __name__ == "__main__":
    main()
