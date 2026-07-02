#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import re
import sys
from typing import Any

from run_reference_trace_replay import (
    BLOCKED_FIXTURE,
    NON_CLAIMS,
    REPLAY_COMMAND,
    RESULT,
    RESULT_COMMAND,
    ROOT,
    RUN_ID,
    TRACKED_ARTIFACTS,
    artifact_stat,
    run_command,
)
from validate_reference_trace import schema_errors_for_scenario, semantic_errors


DOC = ROOT / "docs" / "reference_trace_harness.md"
CHAPTER = ROOT / "chapters" / "integrated-reference-architecture.qmd"
SHA_RE = re.compile(r"^[0-9a-f]{64}$")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Reference trace replay validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_shape(value: dict[str, Any], errors: list[str]) -> None:
    expected = {
        "schema_version": "0.1",
        "replay_id": RUN_ID,
        "record_kind": "reference_trace_replay",
        "command": RESULT_COMMAND,
        "replay_command": REPLAY_COMMAND,
        "local_only": True,
        "public_safe": True,
        "pass": True,
        "support_state_effect": "record_shape_only",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
        "blocked_path_fixture_ref": BLOCKED_FIXTURE,
        "non_claims": NON_CLAIMS,
    }
    for key, expected_value in expected.items():
        if value.get(key) != expected_value:
            errors.append(f"{rel(RESULT)}: {key} must be {expected_value!r}.")
    timestamp = value.get("recorded_at_utc")
    if not isinstance(timestamp, str) or not timestamp.endswith("Z"):
        errors.append(f"{rel(RESULT)}: recorded_at_utc must be a UTC timestamp ending in Z.")


def validate_trace_record(value: dict[str, Any], errors: list[str]) -> None:
    scenario = {
        "scenario_id": "valid-actual-command-reference-trace-replay",
        "reference_trace_record": value.get("reference_trace_record"),
        "non_claims": value.get("non_claims"),
    }
    if not isinstance(scenario["reference_trace_record"], dict):
        errors.append(f"{rel(RESULT)}: reference_trace_record must be an object.")
        return
    errors.extend(schema_errors_for_scenario(scenario, load_json(ROOT / "schemas/reference_trace_record.schema.json"), rel(RESULT)))
    errors.extend(semantic_errors(scenario, rel(RESULT)))
    trace = scenario["reference_trace_record"]
    if trace.get("trace_state") != "replayed":
        errors.append(f"{rel(RESULT)}: reference_trace_record.trace_state must be replayed.")
    if trace.get("execution_boundary") != "replay":
        errors.append(f"{rel(RESULT)}: reference_trace_record.execution_boundary must be replay.")
    if trace.get("support_state_effect") != "record_shape_only":
        errors.append(f"{rel(RESULT)}: reference_trace_record.support_state_effect must remain record_shape_only.")


def validate_actual_command(value: dict[str, Any], errors: list[str]) -> None:
    recorded = value.get("actual_command_record")
    if not isinstance(recorded, dict):
        errors.append(f"{rel(RESULT)}: actual_command_record must be an object.")
        return
    if recorded.get("command") != REPLAY_COMMAND:
        errors.append(f"{rel(RESULT)}: actual_command_record.command must be {REPLAY_COMMAND!r}.")
    if recorded.get("exit_code") != 0:
        errors.append(f"{rel(RESULT)}: actual command exit_code must be 0.")
    digest = recorded.get("output_sha256")
    if not isinstance(digest, str) or not SHA_RE.match(digest):
        errors.append(f"{rel(RESULT)}: actual command output_sha256 must be a SHA-256 digest.")
    if not isinstance(recorded.get("output_excerpt"), list) or not recorded["output_excerpt"]:
        errors.append(f"{rel(RESULT)}: actual command output_excerpt must be non-empty.")
    replayed = run_command(REPLAY_COMMAND)
    if replayed["exit_code"] != 0:
        errors.append(f"{rel(RESULT)}: current replay of {REPLAY_COMMAND} failed.")
    if replayed["output_sha256"] != digest:
        errors.append(f"{rel(RESULT)}: current replay output digest differs from recorded digest.")


def validate_blocked_path(value: dict[str, Any], errors: list[str]) -> None:
    fixture = load_json(ROOT / BLOCKED_FIXTURE)
    expected_stops = fixture["reference_trace_record"].get("stop_conditions", [])
    if value.get("blocked_path_stop_conditions") != expected_stops:
        errors.append(f"{rel(RESULT)}: blocked_path_stop_conditions must match {BLOCKED_FIXTURE}.")
    trace_stops = value.get("reference_trace_record", {}).get("stop_conditions", [])
    for stop in expected_stops:
        if stop not in trace_stops:
            errors.append(f"{rel(RESULT)}: replay trace missing blocked stop condition {stop!r}.")


def validate_artifacts(value: dict[str, Any], errors: list[str]) -> None:
    expected_refs = [*TRACKED_ARTIFACTS, rel(RESULT)]
    if value.get("artifact_refs") != expected_refs:
        errors.append(f"{rel(RESULT)}: artifact_refs must match tracked artifact list.")
    for relative in expected_refs:
        if not (ROOT / relative).exists():
            errors.append(f"{rel(RESULT)}: referenced artifact does not exist: {relative}.")

    tracked = value.get("tracked_artifacts")
    if not isinstance(tracked, list) or len(tracked) != len(TRACKED_ARTIFACTS):
        errors.append(f"{rel(RESULT)}: tracked_artifacts must include {len(TRACKED_ARTIFACTS)} records.")
        return
    for index, (relative, recorded) in enumerate(zip(TRACKED_ARTIFACTS, tracked)):
        owner = f"{rel(RESULT)}:tracked_artifacts[{index}]"
        if not isinstance(recorded, dict):
            errors.append(f"{owner}: tracked artifact record must be an object.")
            continue
        current = artifact_stat(relative)
        if recorded != current:
            errors.append(f"{owner}: artifact stat must match current {relative}.")
        if not SHA_RE.match(str(recorded.get("sha256", ""))):
            errors.append(f"{owner}: sha256 must be a SHA-256 digest.")


def validate_docs(errors: list[str]) -> None:
    doc_text = DOC.read_text(encoding="utf-8")
    chapter_text = CHAPTER.read_text(encoding="utf-8")
    required_doc = [
        "Reference Trace Replay",
        RESULT_COMMAND,
        rel(RESULT),
        REPLAY_COMMAND,
        "blocked-authority fixture",
    ]
    for fragment in required_doc:
        if fragment not in doc_text:
            errors.append(f"{rel(DOC)} missing required fragment: {fragment}")
    required_chapter = [
        "actual Resource flagship lane validator replay",
        rel(RESULT),
        "does not prove a deployed runtime",
    ]
    for fragment in required_chapter:
        if fragment not in chapter_text:
            errors.append(f"{rel(CHAPTER)} missing required fragment: {fragment}")


def main() -> None:
    if not RESULT.exists():
        fail([f"Missing {rel(RESULT)}. Run `{RESULT_COMMAND}` first."])
    value = load_json(RESULT)
    if not isinstance(value, dict):
        fail([f"{rel(RESULT)} must contain a JSON object."])

    errors: list[str] = []
    validate_shape(value, errors)
    validate_trace_record(value, errors)
    validate_actual_command(value, errors)
    validate_blocked_path(value, errors)
    validate_artifacts(value, errors)
    validate_docs(errors)

    if errors:
        fail(errors)
    print(
        "Reference trace replay validation passed: "
        f"{REPLAY_COMMAND}, {len(TRACKED_ARTIFACTS)} tracked artifact digest(s), support-state effect record_shape_only."
    )


if __name__ == "__main__":
    main()
