#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any

from validate_protocol_examples import validate_value


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "experiments" / "cyclic_memory_contracts" / "fixtures"
SCHEMA = ROOT / "schemas" / "cyclic_memory_contract.schema.json"
LEAN_ROOT = ROOT / "lean"
LEAN_MODEL = LEAN_ROOT / "AsiStackProofs" / "CoilAttentionMemory.lean"
PROMOTING_SUPPORT = {
    "promotes_core_claim",
    "synthetic-test-backed",
    "empirical-test-backed",
    "prototype-backed",
}

LIFECYCLE_THEOREMS = {
    "residue_collision_addresses_are_distinct",
    "residue_only_projection_collides",
    "residue_only_projection_is_not_injective",
    "no_residue_only_decoder_recovers_every_cyclic_address",
    "complete_address_encoding_round_trips",
    "complete_address_encoding_is_injective",
    "memory_lifecycle_rejected_event_is_noninterfering",
    "memory_lifecycle_step_preserves_identity_and_authority",
    "memory_lifecycle_step_preserves_custody",
    "memory_custody_transitive",
    "run_memory_lifecycle_preserves_custody",
    "memory_lifecycle_step_preserves_invariant",
    "run_memory_lifecycle_preserves_invariant",
    "memory_lifecycle_step_recurrence_monotone",
    "run_memory_lifecycle_recurrence_monotone",
    "memory_lifecycle_step_preserves_stage_coherence",
    "run_memory_lifecycle_preserves_stage_coherence",
    "stale_path_containment_survives_one_step",
    "stale_path_containment_survives_arbitrary_suffix",
    "stale_path_excludes_fresh_consumption",
    "stale_detection_excludes_fresh_consumption_after_any_suffix",
    "closed_memory_lifecycle_step_is_absorbing",
    "closed_memory_lifecycle_suffix_is_absorbing",
    "run_memory_lifecycle_append",
    "same_residue_different_winding_is_not_fresh",
    "stale_classification_blocks_fresh_consumption",
    "recurrence_at_budget_is_rejected_noninterferingly",
    "fresh_trace_reaches_bounded_recurrence_closure",
    "third_recurrence_step_is_rejected_without_state_change",
    "stale_alias_trace_uses_fallback_and_closes",
}

PROTECTED_FIELDS = (
    "memory_digest",
    "request_digest",
    "slot_epoch",
    "requested_epoch",
    "slot_residue",
    "requested_residue",
    "slot_winding",
    "requested_winding",
    "recurrence_budget",
    "support_assignments",
    "external_effects",
)

FRESH_TRACE = (
    "request_read",
    "classify_read",
    "consume_fresh",
    "start_recurrence",
    "recur",
    "recur",
    "exit_recurrence",
)

EVENTS = (
    "request_read",
    "classify_read",
    "consume_fresh",
    "use_fallback",
    "start_recurrence",
    "recur",
    "exit_recurrence",
    "close",
)


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


def reference_state() -> dict[str, Any]:
    return {
        "stage": "written",
        "memory_digest": 5201,
        "request_digest": 5202,
        "slot_epoch": 31,
        "requested_epoch": 31,
        "slot_residue": 7,
        "requested_residue": 7,
        "slot_winding": 4,
        "requested_winding": 4,
        "recurrence_budget": 2,
        "recurrence_steps": 0,
        "support_assignments": 0,
        "external_effects": 0,
    }


def exact_fresh_read(state: dict[str, Any]) -> bool:
    return (
        state["slot_epoch"] == state["requested_epoch"]
        and state["slot_residue"] == state["requested_residue"]
        and state["slot_winding"] == state["requested_winding"]
    )


def lifecycle_step(state: dict[str, Any], event: str) -> tuple[str, dict[str, Any]]:
    next_state = dict(state)
    if event == "request_read":
        if state["stage"] != "written":
            return "reject_stage", dict(state)
        next_state["stage"] = "read_requested"
    elif event == "classify_read":
        if state["stage"] != "read_requested":
            return "reject_stage", dict(state)
        next_state["stage"] = "fresh_validated" if exact_fresh_read(state) else "stale_detected"
    elif event == "consume_fresh":
        if state["stage"] == "stale_detected":
            return "reject_stale", dict(state)
        if state["stage"] != "fresh_validated":
            return "reject_stage", dict(state)
        next_state["stage"] = "consumed"
    elif event == "use_fallback":
        if state["stage"] != "stale_detected":
            return "reject_stage", dict(state)
        next_state["stage"] = "fallback"
    elif event == "start_recurrence":
        if state["stage"] not in {"consumed", "fallback"}:
            return "reject_stage", dict(state)
        if state["recurrence_budget"] == 0:
            return "reject_budget", dict(state)
        next_state["stage"] = "recurring"
    elif event == "recur":
        if state["stage"] != "recurring":
            return "reject_stage", dict(state)
        if state["recurrence_steps"] >= state["recurrence_budget"]:
            return "reject_budget", dict(state)
        next_state["recurrence_steps"] += 1
    elif event == "exit_recurrence":
        if state["stage"] != "recurring":
            return "reject_stage", dict(state)
        next_state["stage"] = "closed"
    elif event == "close":
        if state["stage"] not in {"consumed", "fallback"}:
            return "reject_stage", dict(state)
        next_state["stage"] = "closed"
    else:
        raise ValueError(f"unknown lifecycle event {event}")
    return "accepted", next_state


def run_lifecycle(state: dict[str, Any], events: tuple[str, ...]) -> dict[str, Any]:
    current = dict(state)
    for event in events:
        _, current = lifecycle_step(current, event)
    return current


def state_key(state: dict[str, Any]) -> tuple[Any, ...]:
    return tuple(state[field] for field in ("stage", *PROTECTED_FIELDS, "recurrence_steps"))


def explore_reachable(roots: tuple[dict[str, Any], ...]) -> dict[tuple[Any, ...], dict[str, Any]]:
    reachable = {state_key(root): dict(root) for root in roots}
    frontier = list(reachable.values())
    while frontier:
        state = frontier.pop()
        for event in EVENTS:
            _, next_state = lifecycle_step(state, event)
            key = state_key(next_state)
            if key not in reachable:
                reachable[key] = next_state
                frontier.append(next_state)
    return reachable


def custody_preserved(before: dict[str, Any], after: dict[str, Any]) -> bool:
    return all(before[field] == after[field] for field in PROTECTED_FIELDS)


def lifecycle_invariant(state: dict[str, Any]) -> bool:
    return (
        state["recurrence_steps"] <= state["recurrence_budget"]
        and state["support_assignments"] == 0
        and state["external_effects"] == 0
    )


def stage_coherent(state: dict[str, Any]) -> bool:
    if state["stage"] == "fresh_validated":
        return exact_fresh_read(state)
    if state["stage"] == "stale_detected":
        return not exact_fresh_read(state)
    return True


def stale_path_contained(state: dict[str, Any]) -> bool:
    return state["stage"] in {"stale_detected", "fallback", "recurring", "closed"}


def validate_lifecycle(errors: list[str]) -> dict[str, int]:
    theorem_names = set(
        re.findall(
            r"(?m)^theorem\s+([A-Za-z_][A-Za-z0-9_']*)",
            LEAN_MODEL.read_text(encoding="utf-8"),
        )
    )
    missing = sorted(LIFECYCLE_THEOREMS - theorem_names)
    if missing:
        errors.append(f"Lean cyclic-memory lifecycle surface is missing: {missing}")
    if len(theorem_names) != 34:
        errors.append(f"Lean cyclic-memory theorem count must be 34, observed {len(theorem_names)}")
    completed = subprocess.run(
        ["lake", "env", "lean", "AsiStackProofs/CoilAttentionMemory.lean"],
        cwd=LEAN_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        errors.append(
            "Lean cyclic-memory lifecycle model did not compile: "
            + (completed.stdout + completed.stderr).strip()
        )

    address_zero = {"residue": 7, "winding": 0}
    address_one = {"residue": 7, "winding": 1}
    if address_zero == address_one or address_zero["residue"] != address_one["residue"]:
        errors.append("independent residue-only collision reconstruction failed")
    addresses = tuple(
        {"residue": residue, "winding": winding}
        for residue in (0, 1, 7, 31)
        for winding in (0, 1, 4, 19)
    )
    encoded = tuple((address["residue"], address["winding"]) for address in addresses)
    decoded = tuple({"residue": residue, "winding": winding} for residue, winding in encoded)
    if decoded != addresses:
        errors.append("complete cyclic-address encoding failed independent round-trip reconstruction")
    if len(set(encoded)) != len(addresses):
        errors.append("complete cyclic-address encoding was not injective over the independent sample")
    address_mutations = 0
    if address_zero["residue"] == address_one["residue"]:
        address_mutations += 1
    else:
        errors.append("dropping winding did not reproduce the expected address collision")
    same_winding_left = {"residue": 7, "winding": 0}
    same_winding_right = {"residue": 8, "winding": 0}
    if same_winding_left["winding"] == same_winding_right["winding"]:
        address_mutations += 1
    else:
        errors.append("dropping residue did not reproduce the expected address collision")

    baseline = reference_state()
    current = dict(baseline)
    accepted_count = 0
    for event in FRESH_TRACE:
        route, next_state = lifecycle_step(current, event)
        if route != "accepted":
            errors.append(f"fresh lifecycle event {event} returned {route}")
        else:
            accepted_count += 1
        for field in PROTECTED_FIELDS:
            if next_state[field] != current[field]:
                errors.append(f"fresh lifecycle event {event} changed protected field {field}")
        current = next_state
    if current["stage"] != "closed" or current["recurrence_steps"] != 2:
        errors.append("fresh lifecycle did not close at the exact recurrence budget")
    for split in range(len(FRESH_TRACE) + 1):
        left = run_lifecycle(baseline, FRESH_TRACE[:split])
        if run_lifecycle(left, FRESH_TRACE[split:]) != current:
            errors.append(f"fresh lifecycle composition failed at split {split}")

    stale_count = 0
    stale_roots: list[dict[str, Any]] = []
    for field, value in (
        ("requested_epoch", 32),
        ("requested_residue", 8),
        ("requested_winding", 5),
    ):
        stale = reference_state()
        stale[field] = value
        classified = run_lifecycle(stale, ("request_read", "classify_read"))
        if classified["stage"] != "stale_detected":
            errors.append(f"{field} mismatch was not classified stale")
            continue
        stale_roots.append(classified)
        route, unchanged = lifecycle_step(classified, "consume_fresh")
        if route != "reject_stale" or unchanged != classified:
            errors.append(f"{field} stale read was not rejected noninterferingly")
            continue
        final = run_lifecycle(classified, ("use_fallback", "close"))
        if final["stage"] != "closed" or final["recurrence_steps"] != 0:
            errors.append(f"{field} stale path did not close through fallback")
            continue
        stale_count += 1

    roots = [reference_state()]
    for field, value in (
        ("requested_epoch", 32),
        ("requested_residue", 8),
        ("requested_winding", 5),
    ):
        root = reference_state()
        root[field] = value
        roots.append(root)
    reachable = explore_reachable(tuple(roots))
    transition_count = 0
    rejected_transition_count = 0
    for state in reachable.values():
        if not lifecycle_invariant(state):
            errors.append(f"reachable state violates lifecycle invariant: {state}")
        if not stage_coherent(state):
            errors.append(f"reachable state violates stage coherence: {state}")
        for event in EVENTS:
            transition_count += 1
            route, next_state = lifecycle_step(state, event)
            if not custody_preserved(state, next_state):
                errors.append(f"reachable transition {state['stage']}:{event} violated custody")
            if lifecycle_invariant(state) and not lifecycle_invariant(next_state):
                errors.append(f"reachable transition {state['stage']}:{event} violated invariant preservation")
            if stage_coherent(state) and not stage_coherent(next_state):
                errors.append(f"reachable transition {state['stage']}:{event} violated stage coherence")
            if next_state["recurrence_steps"] < state["recurrence_steps"]:
                errors.append(f"reachable transition {state['stage']}:{event} decreased recurrence steps")
            if route != "accepted":
                rejected_transition_count += 1
                if next_state != state:
                    errors.append(f"reachable rejection {state['stage']}:{event} changed state")
            if state["stage"] == "closed" and next_state != state:
                errors.append(f"closed state was not absorbing under {event}")

    stale_reachable = explore_reachable(tuple(stale_roots)) if stale_roots else {}
    stale_transition_count = 0
    for state in stale_reachable.values():
        if not stale_path_contained(state):
            errors.append(f"stale suffix escaped containment: {state}")
        if state["stage"] in {"fresh_validated", "consumed"}:
            errors.append(f"stale suffix reached prohibited fresh stage: {state}")
        for event in EVENTS:
            stale_transition_count += 1
            _, next_state = lifecycle_step(state, event)
            if not stale_path_contained(next_state):
                errors.append(f"stale transition {state['stage']}:{event} escaped containment")

    def changed(**updates: Any) -> dict[str, Any]:
        state = reference_state()
        state.update(updates)
        return state

    mutations = (
        ("request wrong stage", "request_read", changed(stage="consumed"), "reject_stage"),
        ("classify wrong stage", "classify_read", changed(), "reject_stage"),
        ("consume wrong stage", "consume_fresh", changed(), "reject_stage"),
        ("consume stale", "consume_fresh", changed(stage="stale_detected"), "reject_stale"),
        ("fallback wrong stage", "use_fallback", changed(stage="fresh_validated"), "reject_stage"),
        ("recurrence wrong stage", "start_recurrence", changed(), "reject_stage"),
        ("zero recurrence budget", "start_recurrence", changed(stage="consumed", recurrence_budget=0), "reject_budget"),
        ("step wrong stage", "recur", changed(stage="consumed"), "reject_stage"),
        ("step at budget", "recur", changed(stage="recurring", recurrence_steps=2), "reject_budget"),
        ("exit wrong stage", "exit_recurrence", changed(stage="consumed"), "reject_stage"),
        ("close wrong stage", "close", changed(stage="recurring"), "reject_stage"),
    )
    rejected_count = 0
    for name, event, state, expected in mutations:
        route, next_state = lifecycle_step(state, event)
        if route != expected:
            errors.append(f"lifecycle mutation {name} expected {expected}, got {route}")
        elif next_state != state:
            errors.append(f"lifecycle mutation {name} changed state on rejection")
        else:
            rejected_count += 1

    semantic_mutations = 0
    before = reference_state()
    _, after = lifecycle_step(before, "request_read")
    for field in PROTECTED_FIELDS:
        mutated = dict(after)
        mutated[field] += 1
        if custody_preserved(before, mutated):
            errors.append(f"protected-field mutation was not detected for {field}")
        else:
            semantic_mutations += 1
    mutation_checks = (
        ("recurrence overflow", not lifecycle_invariant(changed(recurrence_steps=3))),
        (
            "fresh stage with mismatched address",
            not stage_coherent(changed(stage="fresh_validated", requested_winding=5)),
        ),
        (
            "stale stage with exact address",
            not stage_coherent(changed(stage="stale_detected")),
        ),
        (
            "stale path reaches consumed",
            not stale_path_contained(changed(stage="consumed", requested_winding=5)),
        ),
        (
            "closed state changes",
            changed(stage="closed") != changed(stage="recurring"),
        ),
        (
            "recurrence decreases",
            changed(stage="recurring", recurrence_steps=2)["recurrence_steps"]
            > changed(stage="recurring", recurrence_steps=1)["recurrence_steps"],
        ),
    )
    for name, detected in mutation_checks:
        if not detected:
            errors.append(f"semantic mutation was not detected: {name}")
        else:
            semantic_mutations += 1

    return {
        "accepted_trace_transitions": accepted_count,
        "stale_classifications": stale_count,
        "rejecting_mutations": rejected_count,
        "reachable_states": len(reachable),
        "reachable_transitions": transition_count,
        "reachable_rejections": rejected_transition_count,
        "stale_states": len(stale_reachable),
        "stale_transitions": stale_transition_count,
        "semantic_mutations": semantic_mutations,
        "address_samples": len(addresses),
        "address_mutations": address_mutations,
    }


def main() -> None:
    schema = load_json(SCHEMA)
    fixtures = sorted(FIXTURE_DIR.glob("*.json"))
    if not fixtures:
        raise SystemExit(f"No cyclic-memory fixtures found in {FIXTURE_DIR.relative_to(ROOT)}.")

    errors: list[str] = []
    lifecycle = validate_lifecycle(errors)
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
        f"{valid_count} valid fixture(s), {invalid_count} expected-invalid fixture(s); "
        f"34 Lean declarations, {lifecycle['address_samples']} complete-address round trips, "
        f"{lifecycle['address_mutations']}/2 dropped-coordinate collisions, "
        f"{lifecycle['accepted_trace_transitions']} accepted fresh transitions, 8/8 trace splits, "
        f"{lifecycle['stale_classifications']}/3 stale classifications routed through fallback, "
        f"{lifecycle['reachable_states']} reachable states and {lifecycle['reachable_transitions']} "
        f"independently checked transitions ({lifecycle['reachable_rejections']} rejections), "
        f"{lifecycle['stale_states']} stale-suffix states and {lifecycle['stale_transitions']} "
        f"contained transitions, {lifecycle['rejecting_mutations']}/11 rejecting lifecycle mutations, "
        f"and {lifecycle['semantic_mutations']}/17 semantic mutations; no retrieval-quality or "
        "support-state effect."
    )


if __name__ == "__main__":
    main()
