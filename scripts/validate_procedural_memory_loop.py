#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

from validate_protocol_examples import validate_value


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "experiments" / "procedural_memory_loop" / "fixtures"
SCHEMA = ROOT / "schemas" / "procedural_tool_record.schema.json"

ROUTABLE_REQUESTS = {"make_routable", "keep_routable"}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def fixture_expectation(path: Path) -> bool | None:
    if path.name.startswith("valid_"):
        return True
    if path.name.startswith("invalid_"):
        return False
    return None


def require_object(value: dict[str, Any], field: str, errors: list[str], relative: str) -> dict[str, Any]:
    item = value.get(field)
    if not isinstance(item, dict):
        errors.append(f"{relative}: {field} must be an object.")
        return {}
    return item


def require_nonempty_list(record: dict[str, Any], field: str, errors: list[str], relative: str) -> list[Any]:
    value = record.get(field)
    if not isinstance(value, list) or not value:
        errors.append(f"{relative}: {field} must be a non-empty list.")
        return []
    return value


def require_boundary(items: list[Any], errors: list[str], relative: str) -> None:
    text = " ".join(str(item).lower() for item in items)
    if "does not" not in text:
        errors.append(f"{relative}: non_claims must include explicit 'does not' boundaries.")
    if "promote" not in text and "support state" not in text:
        errors.append(f"{relative}: non_claims must mention support-state non-promotion.")


def schema_errors(value: dict[str, Any], schema: dict[str, Any], relative: str) -> list[str]:
    tool = value.get("procedural_tool")
    if not isinstance(tool, dict):
        return [f"{relative}: procedural_tool must be an object."]
    return validate_value(tool, schema, f"{relative}:procedural_tool")


def trace_ids(traces: list[Any]) -> set[str]:
    return {
        str(trace.get("trace_id"))
        for trace in traces
        if isinstance(trace, dict) and trace.get("trace_id")
    }


def semantic_errors(value: dict[str, Any], relative: str) -> list[str]:
    errors: list[str] = []
    if not isinstance(value.get("scenario_id"), str) or not value["scenario_id"].strip():
        errors.append(f"{relative}: scenario_id must be a non-empty string.")
    non_claims = require_nonempty_list(value, "non_claims", errors, relative)
    if non_claims:
        require_boundary(non_claims, errors, f"{relative}:non_claims")

    tool = require_object(value, "procedural_tool", errors, relative)
    qualification = require_object(value, "qualification_packet", errors, relative)
    regression = require_object(value, "regression_review", errors, relative)
    if errors:
        return errors

    traces = qualification.get("candidate_traces")
    if not isinstance(traces, list) or not traces:
        errors.append(f"{relative}: qualification_packet.candidate_traces must be a non-empty list.")
        traces = []
    negative_examples = qualification.get("negative_examples")
    if not isinstance(negative_examples, list):
        errors.append(f"{relative}: qualification_packet.negative_examples must be a list.")
        negative_examples = []
    near_misses = qualification.get("near_misses")
    if not isinstance(near_misses, list):
        errors.append(f"{relative}: qualification_packet.near_misses must be a list.")
        near_misses = []

    abstraction = require_object(qualification, "abstraction", errors, f"{relative}:qualification_packet")
    for field in ("parameters", "preconditions", "postconditions"):
        require_nonempty_list(abstraction, field, errors, f"{relative}:qualification_packet.abstraction")
        require_nonempty_list(tool, field, errors, f"{relative}:procedural_tool")
    if not str(abstraction.get("invariant_structure", "")).strip():
        errors.append(f"{relative}: abstraction invariant_structure must be non-empty.")
    if abstraction.get("invariant_structure") != tool.get("invariant_structure"):
        errors.append(f"{relative}: abstraction invariant_structure must match procedural_tool.invariant_structure.")

    all_trace_ids = trace_ids(traces)
    tool_trace_ids = {str(item) for item in tool.get("source_traces", [])}
    missing_traces = sorted(all_trace_ids - tool_trace_ids)
    if missing_traces:
        errors.append(f"{relative}: procedural_tool.source_traces missing candidate traces {missing_traces}.")

    outcomes = [str(trace.get("outcome")) for trace in traces if isinstance(trace, dict)]
    success_count = outcomes.count("success")
    failure_count = outcomes.count("failure")
    near_miss_count = outcomes.count("near_miss")
    loop_keys = {
        str(trace.get("loop_key"))
        for trace in traces
        if isinstance(trace, dict) and trace.get("loop_key")
    }
    if len(loop_keys) != 1:
        errors.append(f"{relative}: candidate traces must share exactly one loop_key.")

    promotion_request = str(regression.get("promotion_request", ""))
    expected_route = str(value.get("expected_route", ""))
    lifecycle = str(tool.get("lifecycle_state", ""))
    verification = str(tool.get("verification_result", ""))
    failed_tests = regression.get("failed_tests")
    if not isinstance(failed_tests, list):
        errors.append(f"{relative}: regression_review.failed_tests must be a list.")
        failed_tests = []

    if promotion_request in ROUTABLE_REQUESTS or expected_route == "routable" or lifecycle == "routable":
        if success_count < 3:
            errors.append(f"{relative}: routable tool requires at least three comparable success traces.")
        if failure_count + near_miss_count < 1 or not negative_examples:
            errors.append(f"{relative}: routable tool requires near misses or failures plus preserved negative examples.")
        if verification != "pass":
            errors.append(f"{relative}: routable tool requires verification_result pass.")
        if failed_tests:
            errors.append(f"{relative}: routable tool cannot have failed regression tests.")
        if regression.get("benchmark_floor_passed") is not True:
            errors.append(f"{relative}: routable tool requires benchmark_floor_passed true.")
        if regression.get("scf_active") is not True:
            errors.append(f"{relative}: routable tool requires active SCF target.")
        if regression.get("retirement_triggered") is True:
            errors.append(f"{relative}: routable tool cannot ignore an active retirement trigger.")

    if verification == "fail" or failed_tests:
        if lifecycle == "routable" or expected_route == "routable":
            errors.append(f"{relative}: failed regression must route to quarantine or retired, not routable.")
        if expected_route not in {"quarantined", "retired"}:
            errors.append(f"{relative}: failed regression requires quarantined or retired expected_route.")

    if regression.get("retirement_triggered") is True:
        if lifecycle != "retired" and expected_route != "retired":
            errors.append(f"{relative}: retirement trigger requires retired lifecycle or retired expected_route.")
        require_nonempty_list(tool, "retirement_criteria", errors, f"{relative}:procedural_tool")

    allowed_routes = {"candidate", "verified", "routable", "quarantined", "retired"}
    if expected_route not in allowed_routes:
        errors.append(f"{relative}: expected_route must be one of {sorted(allowed_routes)}.")
    if expected_route == "routable" and lifecycle not in {"verified", "routable"}:
        errors.append(f"{relative}: routable expected_route requires verified or routable lifecycle.")
    if expected_route == "quarantined" and lifecycle not in {"candidate", "quarantined"}:
        errors.append(f"{relative}: quarantined expected_route requires candidate or quarantined lifecycle.")
    if expected_route == "retired" and lifecycle != "retired":
        errors.append(f"{relative}: retired expected_route requires retired lifecycle.")

    if not require_nonempty_list(regression, "tests", errors, f"{relative}:regression_review"):
        pass
    if not require_nonempty_list(tool, "regressions", errors, f"{relative}:procedural_tool"):
        pass
    if not require_nonempty_list(tool, "residuals", errors, f"{relative}:procedural_tool"):
        pass

    packet_non_claims = qualification.get("non_claims")
    if not isinstance(packet_non_claims, list) or not packet_non_claims:
        errors.append(f"{relative}: qualification_packet.non_claims must be a non-empty list.")
    else:
        require_boundary(packet_non_claims, errors, f"{relative}:qualification_packet.non_claims")

    return errors


def main() -> None:
    schema = load_json(SCHEMA)
    fixtures = sorted(FIXTURE_DIR.glob("*.json"))
    if not fixtures:
        raise SystemExit(f"No procedural-memory loop fixtures found in {FIXTURE_DIR.relative_to(ROOT)}.")

    errors: list[str] = []
    valid_count = 0
    invalid_count = 0
    for fixture in fixtures:
        relative = str(fixture.relative_to(ROOT))
        expect_valid = fixture_expectation(fixture)
        if expect_valid is None:
            errors.append(f"{relative}: fixture name must start with valid_ or invalid_.")
            continue
        try:
            value = load_json(fixture)
        except Exception as exc:
            errors.append(f"{relative}: invalid JSON: {exc}")
            continue
        if not isinstance(value, dict):
            errors.append(f"{relative}: scenario must contain a JSON object.")
            continue
        scenario_errors = schema_errors(value, schema, relative)
        if not scenario_errors:
            scenario_errors.extend(semantic_errors(value, relative))
        if expect_valid:
            valid_count += 1
            errors.extend(scenario_errors)
        else:
            invalid_count += 1
            if not scenario_errors:
                errors.append(f"{relative}: invalid fixture unexpectedly passed procedural-memory loop checks.")

    if errors:
        print("Procedural memory loop harness failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print(
        "Procedural memory loop harness passed: "
        f"{valid_count} valid fixture(s), {invalid_count} expected-invalid fixture(s)."
    )


if __name__ == "__main__":
    main()
