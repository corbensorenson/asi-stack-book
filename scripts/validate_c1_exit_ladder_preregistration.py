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


def main() -> None:
    protocol = load(PROTOCOL)
    admission = load(ADMISSION)
    out = failures(protocol) + admission_failures(admission)
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
    if out:
        raise SystemExit("C1-EL preregistration failed:\n - " + "\n - ".join(out))
    print(
        "C1-EL preregistration passed: first eligible post-freeze natural task, "
        "3 matched routes, 1 natural plus 3 injected paths, 12 outcomes, "
        "task admitted before solution inspection, 12 mutations rejected, "
        "protected/support/release state closed."
    )


if __name__ == "__main__":
    main()
