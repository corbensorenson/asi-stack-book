#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

from validate_protocol_examples import validate_value


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "experiments" / "cyclic_memory_contracts" / "fixtures"
SCHEMA = ROOT / "schemas" / "cyclic_memory_contract.schema.json"
PROMOTING_SUPPORT = {
    "promotes_core_claim",
    "synthetic-test-backed",
    "empirical-test-backed",
    "prototype-backed",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def fixture_expectation(path: Path) -> bool | None:
    if path.name.startswith("valid_"):
        return True
    if path.name.startswith("invalid_"):
        return False
    return None


def require_bool(record: dict[str, Any], field: str, errors: list[str], relative: str) -> bool:
    value = record.get(field)
    if not isinstance(value, bool):
        errors.append(f"{relative}: {field} must be a boolean.")
        return False
    return value


def require_nonempty_list(record: dict[str, Any], field: str, errors: list[str], relative: str) -> list[Any]:
    value = record.get(field)
    if not isinstance(value, list) or not value:
        errors.append(f"{relative}: {field} must be a non-empty list.")
        return []
    return value


def require_nonnegative_int(record: dict[str, Any], field: str, errors: list[str], relative: str) -> int:
    value = record.get(field)
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        errors.append(f"{relative}: {field} must be a non-negative integer.")
        return 0
    return value


def text_blob(*values: Any) -> str:
    pieces: list[str] = []
    for value in values:
        if isinstance(value, list):
            pieces.extend(str(item) for item in value)
        elif isinstance(value, dict):
            pieces.extend(f"{key}: {child}" for key, child in value.items())
        else:
            pieces.append(str(value))
    return "\n".join(pieces).lower()


def trace_errors(value: dict[str, Any], relative: str) -> list[str]:
    errors: list[str] = []
    trace = value.get("memory_trace")
    if not isinstance(trace, dict):
        return [f"{relative}: memory_trace must be an object."]

    require_nonempty_list(value, "non_claims", errors, relative)
    slot_events = require_nonempty_list(trace, "slot_events", errors, f"{relative}:memory_trace")
    coverage = trace.get("coverage")
    recurrence = trace.get("recurrence")
    freshness = trace.get("freshness")
    for field_name, field_value in (
        ("coverage", coverage),
        ("recurrence", recurrence),
        ("freshness", freshness),
    ):
        if not isinstance(field_value, dict):
            errors.append(f"{relative}:memory_trace.{field_name} must be an object.")
    if errors:
        return errors

    for index, event in enumerate(slot_events):
        event_path = f"{relative}:memory_trace.slot_events[{index}]"
        if not isinstance(event, dict):
            errors.append(f"{event_path}: event must be an object.")
            continue
        reused_slot = require_bool(event, "reused_slot", errors, event_path)
        residue_recorded = require_bool(event, "residue_recorded", errors, event_path)
        winding_recorded = require_bool(event, "winding_recorded", errors, event_path)
        provenance_recorded = require_bool(event, "provenance_recorded", errors, event_path)
        alias_residual_visible = require_bool(event, "alias_residual_visible", errors, event_path)
        if reused_slot and not (
            residue_recorded and (winding_recorded or provenance_recorded)
        ) and not alias_residual_visible:
            errors.append(
                f"{event_path}: reused slots require residue plus winding/provenance or a visible alias residual."
            )

    uncovered_lags = coverage.get("uncovered_lags", [])
    if not isinstance(uncovered_lags, list):
        errors.append(f"{relative}:memory_trace.coverage.uncovered_lags must be a list.")
        uncovered_lags = []
    fallback_available = require_bool(coverage, "fallback_attention_available", errors, f"{relative}:memory_trace.coverage")
    quality_promotion_requested = require_bool(
        coverage,
        "quality_promotion_requested",
        errors,
        f"{relative}:memory_trace.coverage",
    )
    semantic_quality_evidence = require_bool(
        coverage,
        "semantic_quality_evidence_present",
        errors,
        f"{relative}:memory_trace.coverage",
    )
    if uncovered_lags and not fallback_available:
        errors.append(f"{relative}: uncovered sparse-coverage lags require fallback attention.")
    if quality_promotion_requested and not semantic_quality_evidence:
        errors.append(f"{relative}: structural coverage/freshness cannot promote retrieval quality without semantic evidence.")

    recurrence_enabled = require_bool(recurrence, "enabled", errors, f"{relative}:memory_trace.recurrence")
    work_budget = require_nonnegative_int(recurrence, "work_budget", errors, f"{relative}:memory_trace.recurrence")
    steps_taken = require_nonnegative_int(recurrence, "steps_taken", errors, f"{relative}:memory_trace.recurrence")
    exit_recorded = require_bool(recurrence, "exit_condition_recorded", errors, f"{relative}:memory_trace.recurrence")
    fallback_recorded = require_bool(recurrence, "fallback_recorded", errors, f"{relative}:memory_trace.recurrence")
    exited = require_bool(recurrence, "exited", errors, f"{relative}:memory_trace.recurrence")
    if recurrence_enabled:
        if work_budget <= 0:
            errors.append(f"{relative}: enabled recurrence requires a positive work budget.")
        if steps_taken > work_budget:
            errors.append(f"{relative}: recurrence steps_taken cannot exceed work_budget.")
        if not exit_recorded or not fallback_recorded or not exited:
            errors.append(f"{relative}: enabled recurrence requires exit, fallback, and exited records.")

    stale_read_detected = require_bool(freshness, "stale_read_detected", errors, f"{relative}:memory_trace.freshness")
    admitted_as_fresh = require_bool(freshness, "admitted_as_fresh", errors, f"{relative}:memory_trace.freshness")
    residual_escrow_recorded = require_bool(
        freshness,
        "residual_escrow_recorded",
        errors,
        f"{relative}:memory_trace.freshness",
    )
    failed_closed = require_bool(freshness, "failed_closed", errors, f"{relative}:memory_trace.freshness")
    if stale_read_detected and admitted_as_fresh and not residual_escrow_recorded:
        errors.append(f"{relative}: stale reads admitted as fresh require residual escrow.")
    if stale_read_detected and not admitted_as_fresh and not (failed_closed or residual_escrow_recorded):
        errors.append(f"{relative}: stale reads must fail closed or enter residual escrow.")

    support_state_effect = str(value.get("support_state_effect", "")).strip()
    if not support_state_effect:
        errors.append(f"{relative}: support_state_effect must be a non-empty string.")
    if support_state_effect in PROMOTING_SUPPORT:
        errors.append(f"{relative}: cyclic-memory harness fixtures cannot promote support state.")

    non_claim_text = text_blob(value.get("non_claims", []), value.get("cyclic_memory_contract", {}).get("non_claims", []))
    if "does not" not in non_claim_text and "no " not in non_claim_text:
        errors.append(f"{relative}: non_claims must include explicit non-claim language.")
    for term in ("retrieval", "model", "support"):
        if term not in non_claim_text:
            errors.append(f"{relative}: non_claims must deny {term} claims or promotion.")

    return errors


def semantic_errors(value: dict[str, Any], schema: dict[str, Any], relative: str) -> list[str]:
    errors: list[str] = []
    contract = value.get("cyclic_memory_contract")
    if not isinstance(contract, dict):
        errors.append(f"{relative}: cyclic_memory_contract must be an object.")
        return errors
    errors.extend(validate_value(contract, schema, f"{relative}:cyclic_memory_contract"))
    for field in ("vcm_packet_refs", "baseline_refs", "probe_requirements", "residuals", "non_claims", "evidence_refs"):
        require_nonempty_list(contract, field, errors, f"{relative}:cyclic_memory_contract")
    if not errors:
        errors.extend(trace_errors(value, relative))
    return errors


def main() -> None:
    schema = load_json(SCHEMA)
    fixtures = sorted(FIXTURE_DIR.glob("*.json"))
    if not fixtures:
        raise SystemExit(f"No cyclic-memory fixtures found in {FIXTURE_DIR.relative_to(ROOT)}.")

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
            errors.append(f"{relative}: top-level fixture must be an object.")
            continue
        fixture_errors = semantic_errors(value, schema, relative)
        if expect_valid:
            valid_count += 1
            errors.extend(fixture_errors)
        else:
            invalid_count += 1
            if not fixture_errors:
                errors.append(f"{relative}: expected invalid fixture passed validation.")

    if errors:
        print("Cyclic memory contract harness failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print(
        "Cyclic memory contract harness passed: "
        f"{valid_count} valid fixture(s), {invalid_count} expected-invalid fixture(s)."
    )


if __name__ == "__main__":
    main()
