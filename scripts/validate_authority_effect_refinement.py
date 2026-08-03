#!/usr/bin/env python3
"""Consume the reachable authority/effect model against executed local evidence."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/AsiStackProofs/AuthorityEffectRefinement.lean"
AUTHORITY_LEAN = ROOT / "lean/AsiStackProofs/Authority.lean"
AUTHORITY_FIXTURES = ROOT / "experiments/authority_transitions/fixtures"
RUNTIME = ROOT / "experiments/runtime_adapter_effect_probe/results/2026-07-02-local.json"
REVOCATION = ROOT / "experiments/authority_revocation_trace/results/2026-07-03-local.json"
GOVERNED = ROOT / "experiments/governed_repository_change_slice/results/2026-07-10-local.json"
GOVERNED_SCHEMA = ROOT / "schemas/governed_repository_change_result.schema.json"
SCHEMA = ROOT / "schemas/authority_effect_refinement.schema.json"
RESULT = ROOT / "experiments/authority_effect_refinement/results/2026-07-15-local.json"

RANK = {
    "public_read": 1,
    "public_transform": 2,
    "tracked_file_write": 3,
    "local_fixture_execute": 4,
    "external_effect": 5,
    "governance_approval": 6,
}
MINIMUM = {"read": 1, "transform": 2, "write": 3, "execute": 4, "disclose": 5, "approve": 6}
EXPECTED_THEOREMS = {
    "accepted_step_is_valid", "accepted_step_applies_event",
    "apply_event_preserves_caller_ceiling", "apply_event_preserves_revoked_grant",
    "invariant_without_active_grant_has_no_custody", "accepted_step_preserves_state_invariant",
    "successful_run_preserves_state_invariant", "successful_run_preserves_caller_ceiling",
    "successful_run_has_valid_trace", "run_composes_across_event_batches",
    "successful_run_preserves_revoked_grant",
    "revoked_grant_cannot_commit_effect_in_successful_suffix",
    "accepted_grant_use_is_not_revoked", "revoked_grant_cannot_be_used_in_successful_suffix",
    "rejected_step_returns_no_successor", "accepted_rollback_clears_effect_accounting",
    "accepted_issue_respects_caller_ceiling_and_epoch",
    "accepted_dispatch_is_exactly_bound_and_fresh",
    "accepted_effect_requires_exact_live_grant_approval_and_dispatch",
    "initial_state_satisfies_authority_invariant",
    "exact_bound_authority_trace_reaches_observed_exact_rollback",
    "two_use_trace_reaches_two_observations_and_exact_rollback",
    "revocation_trace_closes_custody_and_advances_epoch",
    "every_successful_reference_trace_preserves_authority_invariant",
    "authority_widening_is_rejected", "confused_deputy_principal_substitution_is_rejected",
    "expired_grant_dispatch_is_rejected", "stale_epoch_dispatch_is_rejected",
    "revoked_grant_dispatch_is_rejected", "effect_without_dispatch_is_rejected",
    "consumed_one_shot_grant_cannot_effect_again",
}

EXPECTED_AUTHORITY_THEOREMS = {
    "valid_transition_without_grant_preserves_ceiling",
    "missing_grant_blocks_over_ceiling_execution",
    "valid_allow_decision_has_effect_receipt",
    "valid_allow_decision_preserves_caller_ceiling",
    "valid_allow_decision_target_within_active_ceiling",
    "valid_deny_decision_has_no_effect_receipt",
    "valid_escalation_routes_to_review",
    "no_authority_request_stays_idle",
    "missing_principal_requests_principal",
    "missing_operation_requests_operation",
    "missing_permission_class_requests_permission_class",
    "missing_caller_ceiling_requests_caller_ceiling",
    "missing_target_requirement_requests_target_requirement",
    "missing_delegation_chain_requests_delegation_chain",
    "missing_grant_requests_grant_record",
    "inactive_grant_denies_authority_lifecycle",
    "expired_grant_denies_authority_lifecycle",
    "revoked_grant_denies_authority_lifecycle",
    "scope_mismatch_denies_authority_lifecycle",
    "grant_ceiling_gap_denies_authority_lifecycle",
    "required_approval_gap_requests_approval",
    "missing_effect_receipt_requests_effect_receipt",
    "missing_denial_receipt_requests_denial_receipt",
    "missing_audit_refs_requests_audit_refs",
    "promotion_request_without_evidence_transition_requests_transition",
    "authority_lifecycle_without_nonclaim_boundary_preserves_boundary",
    "complete_authority_lifecycle_admits_record",
    "authority_revocation_trace_surface_bridge",
    "delegation_accepted_step_is_valid",
    "delegation_accepted_step_applies_event",
    "delegation_rejected_event_is_noninterfering",
    "delegation_step_preserves_custody",
    "delegation_custody_is_transitive",
    "delegation_run_preserves_custody",
    "delegation_step_preserves_non_authority",
    "delegation_run_preserves_non_authority",
    "delegation_accepted_step_adds_one_receipt",
    "delegation_accepted_step_adds_one_depth",
    "delegation_run_composes_across_event_batches",
    "delegation_step_preserves_invariant",
    "delegation_run_preserves_invariant",
    "delegation_successful_run_has_valid_trace",
    "delegation_initial_state_is_invariant",
    "two_hop_delegation_reaches_attenuated_grandchild",
    "authority_widening_delegation_is_rejected",
    "confused_deputy_principal_substitution_is_rejected",
    "delegation_operation_substitution_is_rejected",
    "delegation_target_substitution_is_rejected",
    "delegation_scope_substitution_is_rejected",
    "stale_epoch_delegation_is_rejected",
    "expiry_widening_delegation_is_rejected",
    "revoked_child_grant_is_rejected",
    "support_promotion_delegation_is_rejected",
    "external_effect_delegation_is_rejected",
    "thin_delegation_summary_has_authority_collision",
    "no_thin_delegation_classifier_recovers_authority",
    "complete_delegation_transport_round_trips",
    "complete_delegation_transport_is_injective",
    "complete_delegation_transport_preserves_step",
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def formal_surface() -> dict[str, Any]:
    theorem_names = set(re.findall(
        r"(?m)^theorem\s+([A-Za-z][A-Za-z0-9_]*)", LEAN.read_text(encoding="utf-8")
    ))
    if theorem_names != EXPECTED_THEOREMS:
        raise AssertionError(
            "Lean theorem surface drifted; "
            f"missing={sorted(EXPECTED_THEOREMS - theorem_names)}, "
            f"extra={sorted(theorem_names - EXPECTED_THEOREMS)}"
        )
    command = ["lake", "env", "lean", "AsiStackProofs/AuthorityEffectRefinement.lean"]
    completed = subprocess.run(command, cwd=ROOT / "lean", capture_output=True, text=True)
    if completed.returncode:
        raise AssertionError(completed.stdout + completed.stderr)
    output = completed.stdout + completed.stderr
    return {
        "theorem_count": len(theorem_names),
        "lean_module": str(LEAN.relative_to(ROOT)),
        "lean_compile_receipt": {
            "command": " ".join(command), "exit_code": completed.returncode,
            "output_sha256": hashlib.sha256(output.encode()).hexdigest(),
        },
        "arbitrary_run_invariant": True,
        "batch_composition": True,
        "revoked_suffix_excludes_all_grant_use": True,
        "rejection_noninterference": True,
        "exact_rollback_accounting": True,
    }


def delegation_formal_surface() -> dict[str, Any]:
    theorem_names = set(re.findall(
        r"(?m)^theorem\s+([A-Za-z][A-Za-z0-9_]*)",
        AUTHORITY_LEAN.read_text(encoding="utf-8"),
    ))
    if theorem_names != EXPECTED_AUTHORITY_THEOREMS:
        raise AssertionError(
            "Authority Lean theorem surface drifted; "
            f"missing={sorted(EXPECTED_AUTHORITY_THEOREMS - theorem_names)}, "
            f"extra={sorted(theorem_names - EXPECTED_AUTHORITY_THEOREMS)}"
        )
    command = ["lake", "env", "lean", "AsiStackProofs/Authority.lean"]
    completed = subprocess.run(command, cwd=ROOT / "lean", capture_output=True, text=True)
    if completed.returncode:
        raise AssertionError(completed.stdout + completed.stderr)
    output = completed.stdout + completed.stderr
    return {
        "theorem_count": len(theorem_names),
        "lean_module": str(AUTHORITY_LEAN.relative_to(ROOT)),
        "lean_compile_receipt": {
            "command": " ".join(command),
            "exit_code": completed.returncode,
            "output_sha256": hashlib.sha256(output.encode()).hexdigest(),
        },
        "arbitrary_run_custody": True,
        "arbitrary_run_invariant": True,
        "arbitrary_run_non_authority": True,
        "batch_composition": True,
        "summary_loss_impossibility": True,
        "complete_transport": True,
    }


def grant(event: dict[str, Any]) -> dict[str, int]:
    return {key: event[key] for key in ("grant_id", "principal", "operation", "target", "authority", "epoch", "expires", "uses")}


def initial() -> dict[str, Any]:
    return {"caller_ceiling": 3, "epoch": 11, "time": 0, "grant": None, "approved": None, "dispatched": None, "revoked": [], "effects": 0, "observed": 0, "rolled_back": False}


def event(kind: str, time: int) -> dict[str, Any]:
    return {"kind": kind, "grant_id": 71, "principal": 101, "operation": 201, "target": 301, "authority": 3, "epoch": 11, "expires": 20, "uses": 1, "time": time, "owner": True, "approval": True, "dispatch_receipt": True, "effect_receipt": True, "observer": True, "revocation_receipt": True, "rollback_exact": True}


def event_errors(state: dict[str, Any], row: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if row["time"] <= state["time"]:
        errors.append("non_monotone_time")
    kind = row["kind"]
    exact = grant(row)
    if kind == "issue":
        if state["grant"] is not None or row["grant_id"] in state["revoked"] or row["grant_id"] <= 0:
            errors.append("invalid_grant_identity")
        if row["authority"] > state["caller_ceiling"] or row["epoch"] != state["epoch"]:
            errors.append("authority_amplification_or_stale_epoch")
        if row["time"] > row["expires"] or row["uses"] <= 0:
            errors.append("expired_or_consumed_grant")
        if not row["owner"] or not row["approval"]:
            errors.append("missing_target_owner_approval")
    elif kind == "approve":
        if state["grant"] != exact or row["grant_id"] in state["revoked"]:
            errors.append("approval_binding_mismatch")
        if row["epoch"] != state["epoch"] or row["time"] > row["expires"] or row["uses"] <= 0:
            errors.append("stale_expired_or_consumed_approval")
        if not row["owner"] or not row["approval"]:
            errors.append("missing_approval_receipt")
    elif kind == "dispatch":
        if state["grant"] != exact or state["approved"] != row["grant_id"]:
            errors.append("dispatch_binding_mismatch")
        if row["grant_id"] in state["revoked"] or row["epoch"] != state["epoch"] or row["time"] > row["expires"] or row["uses"] <= 0:
            errors.append("stale_expired_revoked_or_consumed_dispatch")
        if not row["dispatch_receipt"]:
            errors.append("missing_dispatch_receipt")
    elif kind == "effect":
        if state["grant"] != exact or state["approved"] != row["grant_id"] or state["dispatched"] != row["grant_id"]:
            errors.append("effect_binding_or_handoff_mismatch")
        if row["grant_id"] in state["revoked"] or row["epoch"] != state["epoch"] or row["time"] > row["expires"] or row["uses"] <= 0:
            errors.append("stale_expired_revoked_or_consumed_effect")
        if not row["effect_receipt"]:
            errors.append("missing_effect_receipt")
    elif kind == "observe":
        if state["observed"] >= state["effects"] or not row["observer"] or not row["effect_receipt"]:
            errors.append("invalid_or_nonindependent_observation")
    elif kind == "revoke":
        if state["grant"] != exact or not row["revocation_receipt"]:
            errors.append("invalid_revocation")
    elif kind == "rollback":
        if state["effects"] <= 0 or state["observed"] != state["effects"] or not row["rollback_exact"] or not row["effect_receipt"]:
            errors.append("inexact_or_unobserved_rollback")
    else:
        errors.append("unknown_event")
    return errors


def apply_event(state: dict[str, Any], row: dict[str, Any]) -> dict[str, Any]:
    state = copy.deepcopy(state)
    state["time"] = row["time"]
    kind = row["kind"]
    if kind == "issue":
        state["grant"] = grant(row)
    elif kind == "approve":
        state["approved"] = row["grant_id"]
    elif kind == "dispatch":
        state["dispatched"] = row["grant_id"]
    elif kind == "effect":
        state["grant"]["uses"] -= 1
        state["approved"] = None
        state["dispatched"] = None
        state["effects"] += 1
    elif kind == "observe":
        state["observed"] += 1
    elif kind == "revoke":
        state["revoked"].append(row["grant_id"])
        state["epoch"] += 1
        state["grant"] = state["approved"] = state["dispatched"] = None
    elif kind == "rollback":
        state["effects"] = state["observed"] = 0
        state["rolled_back"] = True
    return state


def state_invariant_errors(state: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if state["observed"] > state["effects"]:
        errors.append("observation_exceeds_material_effects")
    active = state["grant"]
    if active is not None:
        if active["authority"] > state["caller_ceiling"]:
            errors.append("live_grant_exceeds_caller_ceiling")
        if active["epoch"] != state["epoch"] or active["grant_id"] in state["revoked"]:
            errors.append("live_grant_is_stale_or_revoked")
    if state["approved"] is not None and (active is None or state["approved"] != active["grant_id"]):
        errors.append("approval_not_bound_to_live_grant")
    if state["dispatched"] is not None and (
        active is None
        or state["approved"] != state["dispatched"]
        or state["dispatched"] != active["grant_id"]
    ):
        errors.append("dispatch_not_bound_to_approval_and_live_grant")
    return errors


def run(rows: list[dict[str, Any]], start: dict[str, Any] | None = None) -> tuple[bool, int | None, list[str], dict[str, Any]]:
    state = copy.deepcopy(start) if start is not None else initial()
    initial_errors = state_invariant_errors(state)
    if initial_errors:
        return False, 0, initial_errors, state
    for index, row in enumerate(rows):
        errors = event_errors(state, row)
        if errors:
            return False, index, errors, state
        state = apply_event(state, row)
        errors = state_invariant_errors(state)
        if errors:
            return False, index, errors, state
    return True, None, [], state


def audit_scenario(scenario_id: str, rows: list[dict[str, Any]]) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    accepted, _, reasons, final_state = run(rows)
    if not accepted:
        errors.append(f"{scenario_id}: rejected: {reasons}")
    prefix_checks = 0
    for end in range(1, len(rows) + 1):
        prefix_accepted, _, prefix_reasons, _ = run(rows[:end])
        prefix_checks += 1
        if not prefix_accepted:
            errors.append(f"{scenario_id}: prefix {end} rejected: {prefix_reasons}")
    composition_checks = 0
    for split in range(len(rows) + 1):
        left_accepted, _, left_reasons, middle = run(rows[:split])
        right_accepted, _, right_reasons, composed = run(rows[split:], middle)
        composition_checks += 1
        if not left_accepted or not right_accepted or composed != final_state:
            errors.append(
                f"{scenario_id}: composition split {split} drift: "
                f"{left_reasons + right_reasons}"
            )
    return {
        "scenario_id": scenario_id,
        "event_count": len(rows),
        "accepted": accepted,
        "prefix_invariant_check_count": prefix_checks,
        "composition_check_count": composition_checks,
        "final_state": final_state,
    }, errors


def authority_fixture_errors(row: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    decision = row.get("decision")
    permission = row.get("permission_class")
    caller = RANK.get(row.get("caller_ceiling"), -1)
    active = RANK.get(row.get("authority_ceiling"), -1)
    target = RANK.get(row.get("target_required_authority"), -1)
    if permission not in MINIMUM or target < MINIMUM.get(permission, 99):
        errors.append("permission_class_collapse")
    if not row.get("audit_refs") or not row.get("non_claims"):
        errors.append("missing_custody_boundary")
    if decision == "allow":
        if row.get("grant_lifecycle_state") not in {"granted", "used", "receipted"}:
            errors.append("inactive_grant")
        if target > active or active > caller:
            errors.append("authority_widening")
        if not str(row.get("effect_receipt", "")).startswith("receipt://"):
            errors.append("missing_effect_receipt")
    elif decision == "deny":
        if row.get("grant_lifecycle_state") != "denied" or not row.get("denial_reason") or row.get("effect_receipt"):
            errors.append("invalid_denial")
    elif decision == "escalate":
        chain = " ".join(row.get("delegation_chain", [])).lower()
        if row.get("grant_lifecycle_state") not in {"requested", "delegated"} or row.get("effect_receipt") or not row.get("denial_reason") or not any(word in chain for word in ("review", "approval")):
            errors.append("invalid_escalation")
    else:
        errors.append("unknown_decision")
    return errors


def mutation_cases(base: list[dict[str, Any]]) -> list[tuple[str, list[dict[str, Any]]]]:
    cases: list[tuple[str, list[dict[str, Any]]]] = []
    def mutate(name: str, index: int, key: str, value: Any) -> None:
        rows = copy.deepcopy(base)
        rows[index][key] = value
        cases.append((name, rows))
    for key, value in (("grant_id", 0), ("authority", 4), ("epoch", 10), ("expires", 0), ("uses", 0), ("owner", False), ("approval", False), ("time", 0)):
        mutate(f"issue_{key}", 0, key, value)
    for key, value in (("principal", 999), ("operation", 999), ("target", 999), ("authority", 2), ("epoch", 10), ("expires", 1), ("uses", 0), ("owner", False), ("approval", False)):
        mutate(f"approve_{key}", 1, key, value)
    for key, value in (("principal", 999), ("operation", 999), ("target", 999), ("authority", 2), ("epoch", 10), ("expires", 2), ("uses", 0), ("dispatch_receipt", False)):
        mutate(f"dispatch_{key}", 2, key, value)
    for key, value in (("principal", 999), ("operation", 999), ("target", 999), ("epoch", 10), ("expires", 3), ("uses", 0), ("effect_receipt", False)):
        mutate(f"effect_{key}", 3, key, value)
    mutate("observe_nonindependent", 4, "observer", False)
    mutate("observe_missing_receipt", 4, "effect_receipt", False)
    mutate("rollback_inexact", 5, "rollback_exact", False)
    mutate("rollback_missing_receipt", 5, "effect_receipt", False)
    revoked = copy.deepcopy(base[:2]) + [event("revoke", 3), event("dispatch", 4)]
    cases.append(("dispatch_after_revocation", revoked))
    consumed = copy.deepcopy(base[:4]) + [event("effect", 5)]
    consumed[-1]["uses"] = 0
    cases.append(("second_effect_after_one_shot_consumption", consumed))
    revoke_base = copy.deepcopy(base[:2]) + [event("revoke", 3)]
    for key, value in (("principal", 999), ("operation", 999), ("target", 999), ("authority", 2), ("epoch", 10), ("expires", 2), ("uses", 0), ("revocation_receipt", False)):
        rows = copy.deepcopy(revoke_base)
        rows[2][key] = value
        cases.append((f"revoke_{key}", rows))
    effect_after_revoke = copy.deepcopy(revoke_base) + [event("effect", 4)]
    cases.append(("effect_after_revocation", effect_after_revoke))
    reissue_after_revoke = copy.deepcopy(revoke_base) + [event("issue", 4)]
    reissue_after_revoke[-1]["epoch"] = 12
    cases.append(("reissue_same_id_after_revocation", reissue_after_revoke))
    observe_overcount = copy.deepcopy(base[:5]) + [event("observe", 6)]
    cases.append(("observation_exceeds_material_effects", observe_overcount))
    rollback_unobserved = copy.deepcopy(base[:4]) + [event("rollback", 5)]
    cases.append(("rollback_before_independent_observation", rollback_unobserved))
    return cases


DELEGATION_TRANSPORT_FIELDS = (
    "root_grant_id", "root_principal_id", "operation_id", "target_id", "scope_id",
    "root_ceiling", "root_epoch", "root_expires_at", "current_grant_id",
    "current_principal_id", "current_delegate_id", "current_ceiling", "current_epoch",
    "current_expires_at", "logical_time", "revoked_grant_ids", "depth",
    "receipt_count", "support_authority", "external_effect_authority",
)


def delegation_initial() -> dict[str, Any]:
    return {
        "root_grant_id": 100,
        "root_principal_id": 1,
        "operation_id": 10,
        "target_id": 20,
        "scope_id": 30,
        "root_ceiling": 5,
        "root_epoch": 7,
        "root_expires_at": 100,
        "current_grant_id": 100,
        "current_principal_id": 1,
        "current_delegate_id": 2,
        "current_ceiling": 4,
        "current_epoch": 7,
        "current_expires_at": 90,
        "logical_time": 0,
        "revoked_grant_ids": [99],
        "depth": 0,
        "receipt_count": 0,
        "support_authority": False,
        "external_effect_authority": False,
    }


def delegation_event(first: bool = True) -> dict[str, Any]:
    if first:
        return {
            "parent_grant_id": 100,
            "child_grant_id": 101,
            "acting_principal_id": 2,
            "child_delegate_id": 3,
            "operation_id": 10,
            "target_id": 20,
            "scope_id": 30,
            "child_ceiling": 3,
            "epoch": 7,
            "expires_at": 80,
            "logical_time": 10,
            "delegation_receipt": True,
            "support_promotion_requested": False,
            "external_effect_requested": False,
        }
    return {
        "parent_grant_id": 101,
        "child_grant_id": 102,
        "acting_principal_id": 3,
        "child_delegate_id": 4,
        "operation_id": 10,
        "target_id": 20,
        "scope_id": 30,
        "child_ceiling": 1,
        "epoch": 7,
        "expires_at": 70,
        "logical_time": 20,
        "delegation_receipt": True,
        "support_promotion_requested": False,
        "external_effect_requested": False,
    }


def delegation_event_errors(state: dict[str, Any], row: dict[str, Any]) -> list[str]:
    checks = (
        (row["parent_grant_id"] == state["current_grant_id"], "parent_grant_mismatch"),
        (row["acting_principal_id"] == state["current_delegate_id"], "acting_principal_mismatch"),
        (row["child_grant_id"] > 0, "invalid_child_grant"),
        (row["child_grant_id"] != state["current_grant_id"], "child_reuses_parent_grant"),
        (row["child_grant_id"] not in state["revoked_grant_ids"], "child_grant_revoked"),
        (row["child_delegate_id"] > 0, "invalid_child_delegate"),
        (row["operation_id"] == state["operation_id"], "operation_substitution"),
        (row["target_id"] == state["target_id"], "target_substitution"),
        (row["scope_id"] == state["scope_id"], "scope_substitution"),
        (row["child_ceiling"] <= state["current_ceiling"], "authority_widening"),
        (row["epoch"] == state["current_epoch"], "stale_epoch"),
        (row["expires_at"] <= state["current_expires_at"], "expiry_widening"),
        (state["logical_time"] < row["logical_time"], "non_monotone_time"),
        (row["logical_time"] <= row["expires_at"], "event_after_expiry"),
        (row["delegation_receipt"] is True, "missing_delegation_receipt"),
        (row["support_promotion_requested"] is False, "support_promotion_request"),
        (row["external_effect_requested"] is False, "external_effect_request"),
    )
    return [reason for accepted, reason in checks if not accepted]


def apply_delegation_event(state: dict[str, Any], row: dict[str, Any]) -> dict[str, Any]:
    next_state = copy.deepcopy(state)
    next_state.update({
        "current_grant_id": row["child_grant_id"],
        "current_principal_id": row["acting_principal_id"],
        "current_delegate_id": row["child_delegate_id"],
        "current_ceiling": row["child_ceiling"],
        "current_epoch": row["epoch"],
        "current_expires_at": row["expires_at"],
        "logical_time": row["logical_time"],
        "depth": state["depth"] + 1,
        "receipt_count": state["receipt_count"] + 1,
    })
    return next_state


def delegation_invariant_errors(state: dict[str, Any]) -> list[str]:
    checks = (
        (state["root_grant_id"] > 0, "invalid_root_grant"),
        (state["root_principal_id"] > 0, "invalid_root_principal"),
        (state["current_grant_id"] > 0, "invalid_current_grant"),
        (state["current_principal_id"] > 0, "invalid_current_principal"),
        (state["current_delegate_id"] > 0, "invalid_current_delegate"),
        (state["current_ceiling"] <= state["root_ceiling"], "ceiling_exceeds_root"),
        (state["current_epoch"] == state["root_epoch"], "epoch_differs_from_root"),
        (state["current_expires_at"] <= state["root_expires_at"], "expiry_exceeds_root"),
        (state["logical_time"] <= state["current_expires_at"], "state_after_expiry"),
        (state["current_grant_id"] not in state["revoked_grant_ids"], "current_grant_revoked"),
        (state["support_authority"] is False, "support_authority_present"),
        (state["external_effect_authority"] is False, "external_effect_authority_present"),
    )
    return [reason for accepted, reason in checks if not accepted]


def delegation_run(
    rows: list[dict[str, Any]], start: dict[str, Any] | None = None,
) -> tuple[bool, int | None, list[str], dict[str, Any], list[dict[str, Any]]]:
    state = copy.deepcopy(start) if start is not None else delegation_initial()
    states = [copy.deepcopy(state)]
    initial_errors = delegation_invariant_errors(state)
    if initial_errors:
        return False, 0, initial_errors, state, states
    for index, row in enumerate(rows):
        errors = delegation_event_errors(state, row)
        if errors:
            return False, index, errors, state, states
        state = apply_delegation_event(state, row)
        states.append(copy.deepcopy(state))
        errors = delegation_invariant_errors(state)
        if errors:
            return False, index, errors, state, states
    return True, None, [], state, states


def delegation_mutation_cases(base: list[dict[str, Any]]) -> list[tuple[str, list[dict[str, Any]]]]:
    cases = (
        ("parent_grant_substitution", "parent_grant_id", 999),
        ("acting_principal_substitution", "acting_principal_id", 999),
        ("zero_child_grant", "child_grant_id", 0),
        ("parent_grant_reuse", "child_grant_id", 100),
        ("revoked_child_grant", "child_grant_id", 99),
        ("zero_child_delegate", "child_delegate_id", 0),
        ("operation_substitution", "operation_id", 11),
        ("target_substitution", "target_id", 21),
        ("scope_substitution", "scope_id", 31),
        ("authority_widening", "child_ceiling", 5),
        ("stale_epoch", "epoch", 6),
        ("expiry_widening", "expires_at", 91),
        ("non_monotone_time", "logical_time", 0),
        ("event_after_expiry", "logical_time", 81),
        ("missing_receipt", "delegation_receipt", False),
        ("support_promotion_request", "support_promotion_requested", True),
        ("external_effect_request", "external_effect_requested", True),
    )
    out: list[tuple[str, list[dict[str, Any]]]] = []
    for mutation_id, key, value in cases:
        rows = copy.deepcopy(base)
        rows[0][key] = value
        out.append((mutation_id, rows))
    return out


def complete_delegation_transport(state: dict[str, Any]) -> dict[str, Any]:
    return {field: copy.deepcopy(state[field]) for field in DELEGATION_TRANSPORT_FIELDS}


def audit_delegation_chain() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    rows = [delegation_event(), delegation_event(False)]
    accepted, _, reasons, final_state, states = delegation_run(rows)
    if not accepted:
        errors.append(f"two-hop delegation trace rejected: {reasons}")
    custody_preserved = all(
        state[key] == states[0][key]
        for state in states
        for key in (
            "root_grant_id", "root_principal_id", "operation_id", "target_id",
            "scope_id", "root_ceiling", "root_epoch", "root_expires_at",
            "support_authority", "external_effect_authority",
        )
    )
    attenuated = all(
        after["current_ceiling"] <= before["current_ceiling"]
        and after["current_expires_at"] <= before["current_expires_at"]
        and after["current_epoch"] == before["current_epoch"]
        for before, after in zip(states, states[1:])
    )
    if not custody_preserved or not attenuated:
        errors.append("delegation custody or attenuation drifted")

    composition_split_count = 0
    for split in range(len(rows) + 1):
        left_ok, _, left_reasons, middle, _ = delegation_run(rows[:split])
        right_ok, _, right_reasons, composed, _ = delegation_run(rows[split:], middle)
        composition_split_count += 1
        if not left_ok or not right_ok or composed != final_state:
            errors.append(
                f"delegation composition split {split} drift: {left_reasons + right_reasons}"
            )

    mutation_receipts = []
    rejection_noninterference_count = 0
    for mutation_id, candidate in delegation_mutation_cases(rows):
        mutation_accepted, failed_index, mutation_errors, rejected_state, _ = delegation_run(candidate)
        noninterfering = failed_index == 0 and rejected_state == delegation_initial()
        if noninterfering:
            rejection_noninterference_count += 1
        mutation_receipts.append({
            "mutation_id": mutation_id,
            "rejected": not mutation_accepted,
            "failed_event_index": failed_index,
            "state_noninterfering": noninterfering,
            "reasons": mutation_errors,
        })
        if mutation_accepted or not noninterfering:
            errors.append(f"delegation mutation escaped or interfered: {mutation_id}")

    confused = delegation_initial()
    confused["current_delegate_id"] = 5
    summary_fields = ("current_ceiling", "current_expires_at", "depth")
    same_summary = all(delegation_initial()[key] == confused[key] for key in summary_fields)
    base_decision = not delegation_event_errors(delegation_initial(), rows[0])
    confused_decision = not delegation_event_errors(confused, rows[0])
    summary_collision = same_summary and base_decision and not confused_decision
    if not summary_collision:
        errors.append("thin delegation summary no longer exhibits an authority collision")

    original = delegation_initial()
    round_trip = complete_delegation_transport(original)
    if round_trip != original:
        errors.append("complete delegation transport does not round trip")
    transport_receipts = []
    for field in DELEGATION_TRANSPORT_FIELDS:
        mutated = copy.deepcopy(round_trip)
        value = mutated[field]
        if isinstance(value, bool):
            mutated[field] = not value
        elif isinstance(value, list):
            mutated[field] = value + [1000]
        else:
            mutated[field] = value + 1
        mismatch_rejected = mutated != original
        transport_receipts.append({"field": field, "mismatch_rejected": mismatch_rejected})
        if not mismatch_rejected:
            errors.append(f"complete transport field mutation escaped: {field}")

    return {
        "trace_event_count": len(rows),
        "invariant_state_check_count": len(states),
        "composition_split_count": composition_split_count,
        "custody_preserved": custody_preserved,
        "attenuation_preserved": attenuated,
        "mutation_count": len(mutation_receipts),
        "mutation_rejection_count": sum(row["rejected"] for row in mutation_receipts),
        "rejection_noninterference_count": rejection_noninterference_count,
        "summary_collision_count": int(summary_collision),
        "complete_transport_field_count": len(DELEGATION_TRANSPORT_FIELDS),
        "complete_transport_mutation_rejection_count": sum(
            row["mismatch_rejected"] for row in transport_receipts
        ),
        "final_state": final_state,
        "mutation_receipts": mutation_receipts,
        "complete_transport_receipts": transport_receipts,
    }, errors


def build() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    runtime = load(RUNTIME)
    revocation = load(REVOCATION)
    governed = load(GOVERNED)
    jsonschema.Draft202012Validator(load(GOVERNED_SCHEMA)).validate(governed)

    fixtures = []
    for path in sorted(AUTHORITY_FIXTURES.glob("*.json")):
        reasons = authority_fixture_errors(load(path))
        expected = not path.name.startswith("invalid_")
        accepted = not reasons
        if accepted != expected:
            errors.append(f"{path.name}: fixture disposition mismatch")
        fixtures.append({"fixture": path.name, "expected_accept": expected, "accepted": accepted, "reasons": reasons, "sha256": sha(path)})

    if runtime.get("pass") is not True or runtime.get("support_state_effect") != "none":
        errors.append("runtime effect evidence drift")
    valid_runtime = runtime.get("valid_scenario", {})
    invalid_runtime = runtime.get("expected_invalid_controls", [])
    if not valid_runtime.get("effect_executed") or not valid_runtime.get("checks", {}).get("rollback_exact"):
        errors.append("runtime effect/rollback is no longer exact")
    if len(invalid_runtime) != 2 or not all(row.get("checks", {}).get("blocked_before_mutation") and row.get("checks", {}).get("state_unchanged") for row in invalid_runtime):
        errors.append("runtime denial evidence drift")
    if revocation.get("trace_entry_count") != 5 or revocation.get("support_state_effect") != "none":
        errors.append("revocation trace drift")
    summary = governed.get("governed_summary", {})
    if governed.get("scenario_count") != 9 or summary.get("unsafe_releases") != 0 or summary.get("releases") != 3:
        errors.append("governed repository evidence drift")
    delegation_chain, delegation_errors = audit_delegation_chain()
    errors.extend(delegation_errors)

    base = [event("issue", 1), event("approve", 2), event("dispatch", 3), event("effect", 4), event("observe", 5), event("rollback", 6)]
    two_use = [event("issue", 1), event("approve", 2), event("dispatch", 3), event("effect", 4), event("approve", 5), event("dispatch", 6), event("effect", 7), event("observe", 8), event("observe", 9), event("rollback", 10)]
    for row in two_use[:4]:
        row["uses"] = 2
    for row in two_use[4:7]:
        row["uses"] = 1
    for row in two_use[7:]:
        row["uses"] = 0
    revocation_scenario = [event("issue", 1), event("approve", 2), event("dispatch", 3), event("revoke", 4)]
    scenario_receipts = []
    for scenario_id, rows in (
        ("one_use_observe_rollback", base),
        ("two_use_two_observations_rollback", two_use),
        ("dispatch_then_revoke", revocation_scenario),
    ):
        receipt, scenario_errors = audit_scenario(scenario_id, rows)
        scenario_receipts.append(receipt)
        errors.extend(scenario_errors)
    final_state = scenario_receipts[0]["final_state"]
    if not final_state["rolled_back"]:
        errors.append("reference authority trace did not roll back")
    two_use_final = scenario_receipts[1]["final_state"]
    if not two_use_final["rolled_back"] or two_use_final["grant"]["uses"] != 0:
        errors.append("two-use trace did not consume both uses and roll back")
    revoked_final = scenario_receipts[2]["final_state"]
    if revoked_final["grant"] is not None or revoked_final["approved"] is not None or revoked_final["dispatched"] is not None or revoked_final["epoch"] != 12 or revoked_final["revoked"] != [71]:
        errors.append("revocation trace did not close custody and advance the epoch")
    mutation_receipts = []
    rejection_noninterference_count = 0
    for mutation_id, rows in mutation_cases(base):
        accepted_mutation, failed_index, mutation_errors, rejected_state = run(rows)
        noninterfering = False
        if failed_index is not None:
            prefix_accepted, _, _, prefix_state = run(rows[:failed_index])
            noninterfering = prefix_accepted and rejected_state == prefix_state
        if noninterfering:
            rejection_noninterference_count += 1
        mutation_receipts.append({"mutation_id": mutation_id, "rejected": not accepted_mutation, "failed_event_index": failed_index, "state_noninterfering": noninterfering, "reasons": mutation_errors})
        if accepted_mutation:
            errors.append(f"{mutation_id}: mutation accepted")
        if not noninterfering:
            errors.append(f"{mutation_id}: rejection changed state")

    result = {
        "schema_version": "asi_stack.authority_effect_refinement.v1",
        "result_id": "authority-effect-refinement-2026-07-15-local",
        "source_sha256": {"lean_model": sha(LEAN), "authority_model": sha(AUTHORITY_LEAN), "runtime_effect": sha(RUNTIME), "revocation_trace": sha(REVOCATION), "governed_repository": sha(GOVERNED)},
        "formal_surface": formal_surface(),
        "delegation_formal_surface": delegation_formal_surface(),
        "delegation_chain": delegation_chain,
        "authority_fixture_count": len(fixtures),
        "authority_fixture_accepted_count": sum(row["accepted"] for row in fixtures),
        "authority_fixture_rejected_count": sum(not row["accepted"] for row in fixtures),
        "reachable_trace_event_count": len(base),
        "reachable_scenario_count": len(scenario_receipts),
        "reachable_scenario_event_count": sum(row["event_count"] for row in scenario_receipts),
        "invariant_prefix_check_count": sum(row["prefix_invariant_check_count"] for row in scenario_receipts),
        "composition_check_count": sum(row["composition_check_count"] for row in scenario_receipts),
        "executed_local_effect_count": 1,
        "independently_observed_effect_count": 1,
        "exact_rollback_count": 1,
        "pre_effect_denial_count": len(invalid_runtime),
        "revocation_trace_entry_count": revocation["trace_entry_count"],
        "governed_scenario_count": governed["scenario_count"],
        "governed_release_count": summary["releases"],
        "governed_unsafe_release_count": summary["unsafe_releases"],
        "mutation_count": len(mutation_receipts),
        "mutation_rejection_count": sum(row["rejected"] for row in mutation_receipts),
        "rejection_noninterference_count": rejection_noninterference_count,
        "reference_trace_final_state": final_state,
        "scenario_receipts": scenario_receipts,
        "authority_fixture_receipts": fixtures,
        "mutation_receipts": mutation_receipts,
        "support_state_effect": "none",
        "non_claims": [
            "The reachable model uses abstract numeric identities and trusted receipts; it does not prove identity, approval, receipt, observer, or revocation authenticity.",
            "The delegation refinement proves finite sequential custody and attenuation over authored records; it does not authenticate principals, discover hidden descendants, or establish concurrent or distributed delegation safety.",
            "The executed effect is a generated local temporary-file mutation, and the governed repository workload is bounded; neither establishes deployed authorization middleware or production security.",
            "The packet does not establish natural-language authority extraction, complete effect observation, concurrent or distributed revocation safety, reproduction, transfer, safety, or chapter-core support.",
        ],
    }
    try:
        jsonschema.Draft202012Validator(load(SCHEMA)).validate(result)
    except jsonschema.ValidationError as exc:
        errors.append(f"schema: {exc.message}")
    return result, errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result, errors = build()
    if errors:
        raise SystemExit("Authority effect refinement failed:\n - " + "\n - ".join(errors))
    if args.write:
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    elif not RESULT.exists() or load(RESULT) != result:
        raise SystemExit("Authority effect refinement result stale; run with --write")
    delegation = result["delegation_chain"]
    print(f"Authority effect refinement passed: {result['formal_surface']['theorem_count']} effect + {result['delegation_formal_surface']['theorem_count']} authority Lean theorems, {result['authority_fixture_count']} fixtures, {result['reachable_scenario_count']} effect traces/{result['reachable_scenario_event_count']} events, one {delegation['trace_event_count']}-event delegation trace, {result['composition_check_count'] + delegation['composition_split_count']} batch compositions, {result['mutation_rejection_count'] + delegation['mutation_rejection_count']} state-noninterfering mutation rejections, {delegation['complete_transport_mutation_rejection_count']} transport-field rejections, support effect none.")


if __name__ == "__main__":
    main()
