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


def main() -> None:
    protocol = load(PROTOCOL)
    out = failures(protocol)
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
    if out:
        raise SystemExit("C1-EL preregistration failed:\n - " + "\n - ".join(out))
    print(
        "C1-EL preregistration passed: first eligible post-freeze natural task, "
        "3 matched routes, 1 natural plus 3 injected paths, 12 outcomes, "
        "8 mutations rejected, task/protected/support/release state closed."
    )


if __name__ == "__main__":
    main()
