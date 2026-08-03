#!/usr/bin/env python3
"""Validate synthetic governance-right fixtures."""

from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any

from validate_protocol_examples import validate_value


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "experiments" / "governance_rights" / "fixtures"
SCHEMA = ROOT / "schemas" / "governance_right_record.schema.json"
LEAN_ROOT = ROOT / "lean"
LEAN_MODEL = LEAN_ROOT / "AsiStackProofs" / "GovernanceRights.lean"
REQUIRED_EXERCISE_THEOREMS = {
    "accepted_governance_right_event_is_admissible",
    "accepted_governance_right_event_is_exact_advance",
    "accepted_governance_right_event_preserves_custody",
    "accepted_governance_right_event_is_non_authorizing",
    "accepted_governance_right_event_adds_exact_receipt",
    "accepted_governance_right_event_never_erases_history",
    "accepted_governance_right_review_separates_roles",
    "accepted_audit_delivery_records_material_and_appealable_redaction",
    "accepted_redaction_appeal_is_affected_party_held_and_separately_reviewed",
    "accepted_redaction_redress_closes_appeal_and_adds_remedy",
    "accepted_portable_export_requires_closed_appeal_and_recorded_check",
    "accepted_fork_review_is_separate_and_records_safety_review",
    "accepted_fork_binding_preserves_exact_rights_and_adds_obligation",
    "accepted_replacement_verification_adds_exact_receipt",
    "governance_right_run_preserves_custody_non_authority_and_narrowing",
    "governance_right_run_never_erases_contestability_history",
    "governance_right_exercise_runs_compose",
    "complete_governance_right_exercise_reaches_exact_closure",
    "governance_right_self_review_is_rejected",
    "incomplete_governance_right_bundle_is_rejected",
    "governance_audit_without_material_is_rejected",
    "governance_redaction_without_reason_is_rejected",
    "governance_redaction_without_appeal_path_is_rejected",
    "governance_outsider_appeal_is_rejected",
    "governance_captured_appeal_review_is_rejected",
    "governance_unsustained_appeal_is_rejected",
    "governance_export_before_redress_is_rejected",
    "governance_export_without_portability_check_is_rejected",
    "governance_captured_fork_review_is_rejected",
    "governance_fork_without_safety_review_is_rejected",
    "governance_right_bundle_substitution_is_rejected",
    "governance_fork_without_obligation_binding_is_rejected",
    "governance_replacement_without_receipts_is_rejected",
    "governance_close_before_replacement_verification_is_rejected",
    "governance_authority_widening_is_rejected",
    "governance_legal_validation_request_is_rejected",
    "governance_action_authority_request_is_rejected",
    "governance_support_promotion_request_is_rejected",
    "governance_closed_exercise_is_terminal",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def as_text(value: Any) -> str:
    if isinstance(value, list):
        return " ".join(as_text(item) for item in value)
    if isinstance(value, dict):
        return " ".join(f"{key} {as_text(child)}" for key, child in value.items())
    return str(value)


def nonempty_list(record: dict[str, Any], key: str) -> bool:
    return isinstance(record.get(key), list) and bool(record[key])


def semantic_errors(record: dict[str, Any], relative: str) -> list[str]:
    errors: list[str] = []
    right_type = str(record.get("right_type", ""))
    request_state = str(record.get("request_state", ""))
    denial_reason = str(record.get("denial_or_redaction_reason", "")).strip()
    appeal_path = str(record.get("appeal_path", "")).lower()
    access_path = str(record.get("access_path", "")).lower()
    independence = str(record.get("challenged_party_independence", "")).lower()
    preservation = f"{record.get('preservation_rule', '')} {record.get('preservation_obligation', '')}".lower()
    revisit = str(record.get("expiry_or_revisit", "")).lower()
    non_claim_text = as_text(record.get("non_claims", [])).lower()

    if right_type == "audit":
        if request_state in {"granted", "partially_granted", "redacted", "preserved"}:
            if not nonempty_list(record, "material_available"):
                errors.append(f"{relative}: audit rights require material_available when access is not denied.")
            if not nonempty_list(record, "receipt_refs"):
                errors.append(f"{relative}: audit rights require receipt_refs.")

    if right_type in {"exit", "fork"}:
        if not any(term in access_path for term in ("export", "repository", "snapshot", "portable", "bundle")):
            errors.append(f"{relative}: exit/fork rights require a usable access_path.")
        if "preserve" not in preservation and "retain" not in preservation:
            errors.append(f"{relative}: exit/fork rights require preservation_rule or preservation_obligation.")
        if "never" in revisit or revisit.strip() == "none":
            errors.append(f"{relative}: exit/fork rights require expiry_or_revisit.")

    if right_type == "fork" and request_state in {"granted", "partially_granted", "preserved"}:
        if not nonempty_list(record, "safety_constraints"):
            errors.append(f"{relative}: fork rights require safety_constraints.")
        if not nonempty_list(record, "material_available"):
            errors.append(f"{relative}: fork rights require material_available.")

    if request_state in {"denied", "redacted", "partially_granted"}:
        if not denial_reason:
            errors.append(f"{relative}: denied/redacted/partially_granted rights require denial_or_redaction_reason.")
        if not any(term in appeal_path for term in ("appeal", "review", "issue", "tribunal", "human")):
            errors.append(f"{relative}: denied/redacted/partially_granted rights require a usable appeal_path.")

    if "same party" in independence or "challenged runtime only" in independence:
        errors.append(f"{relative}: challenged_party_independence cannot depend only on the challenged party.")
    if not any(term in independence for term in ("independent", "git", "log", "repository", "review", "workflow")):
        errors.append(f"{relative}: challenged_party_independence must name an independent or durable record path.")

    if "does not" not in non_claim_text:
        errors.append(f"{relative}: non_claims must contain explicit does-not boundaries.")
    for term in ("institutional", "runtime", "legal", "support"):
        if term not in non_claim_text:
            errors.append(f"{relative}: non_claims must mention {term}.")

    return errors


def fixture_expectation(path: Path) -> bool | None:
    if path.name.startswith("valid_"):
        return True
    if path.name.startswith("invalid_"):
        return False
    return None


def compile_and_check_lean_surface() -> list[str]:
    errors: list[str] = []
    theorem_names = set(
        re.findall(
            r"(?m)^theorem\s+([A-Za-z_][A-Za-z0-9_']*)",
            LEAN_MODEL.read_text(encoding="utf-8"),
        )
    )
    missing = sorted(REQUIRED_EXERCISE_THEOREMS - theorem_names)
    if missing:
        errors.append(f"Lean governance-right theorem surface is missing: {missing}.")
    completed = subprocess.run(
        ["lake", "env", "lean", "AsiStackProofs/GovernanceRights.lean"],
        cwd=LEAN_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        detail = (completed.stdout + completed.stderr).strip()
        errors.append(f"Lean governance-right lifecycle did not compile: {detail}")
    return errors


def apply_exercise_event(
    state: dict[str, Any], event: dict[str, Any]
) -> dict[str, Any] | None:
    identity_fields = (
        "case_id",
        "right_holder_id",
        "custodian_id",
        "source_system_id",
        "destination_system_id",
        "fork_id",
        "rights",
    )
    if not all(event[field] == state[field] for field in identity_fields):
        return None
    if not (
        event["expected_version"] == state["version"]
        and event["target_version"] == state["version"] + 1
        and event["requested_authority_ceiling"]
        <= state["current_authority_ceiling"]
        and event["requests_legal_validation"] is False
        and event["requests_action_authority"] is False
        and event["requests_support_promotion"] is False
    ):
        return None

    kind = event["kind"]
    if kind == "record_independent_review":
        if not (
            state["stage"] == "requested"
            and all(state["rights"].values())
            and event["actor_id"] == event["reviewer_id"]
            and event["reviewer_id"] != state["custodian_id"]
            and event["reviewer_id"] != state["right_holder_id"]
        ):
            return None
    elif kind == "deliver_audit_packet":
        if not (
            state["stage"] == "reviewed"
            and event["actor_id"] == state["custodian_id"]
            and event["reviewer_id"] == state["reviewer_id"]
            and event["audit_material_recorded"] is True
            and event["durable_receipt_recorded"] is True
            and (
                state["redaction_applied"] is False
                or (
                    event["redaction_reason_recorded"] is True
                    and event["appeal_path_recorded"] is True
                )
            )
        ):
            return None
    elif kind == "file_redaction_appeal":
        if not (
            state["stage"] == "audit_delivered"
            and state["redaction_applied"] is True
            and event["actor_id"] == state["right_holder_id"]
            and event["appeal_path_recorded"] is True
            and event["appeal_reviewer_id"] != state["custodian_id"]
            and event["appeal_reviewer_id"] != state["reviewer_id"]
            and event["appeal_reviewer_id"] != state["right_holder_id"]
        ):
            return None
    elif kind == "sustain_redaction_appeal":
        if not (
            state["stage"] == "appealed"
            and state["appeal_open"] is True
            and event["actor_id"] == state["appeal_reviewer_id"]
            and event["appeal_reviewer_id"] == state["appeal_reviewer_id"]
            and event["appeal_sustained"] is True
            and event["durable_receipt_recorded"] is True
        ):
            return None
    elif kind == "export_portable_state":
        if not (
            state["stage"] == "redressed"
            and state["appeal_open"] is False
            and event["actor_id"] == state["custodian_id"]
            and event["portability_check_recorded"] is True
            and event["durable_receipt_recorded"] is True
        ):
            return None
    elif kind == "record_fork_safety_review":
        if not (
            state["stage"] == "exported"
            and event["actor_id"] == event["fork_reviewer_id"]
            and event["fork_reviewer_id"] != state["custodian_id"]
            and event["fork_reviewer_id"] != state["right_holder_id"]
            and event["fork_reviewer_id"] != state["reviewer_id"]
            and event["fork_reviewer_id"] != state["appeal_reviewer_id"]
            and event["fork_safety_review_recorded"] is True
            and event["durable_receipt_recorded"] is True
        ):
            return None
    elif kind == "bind_fork_obligations":
        if not (
            state["stage"] == "fork_reviewed"
            and event["actor_id"] == state["custodian_id"]
            and event["fork_reviewer_id"] == state["fork_reviewer_id"]
            and event["fork_obligations_preserved"] is True
            and event["durable_receipt_recorded"] is True
        ):
            return None
    elif kind == "verify_replacement_receipts":
        if not (
            state["stage"] == "fork_bound"
            and event["actor_id"] == state["reviewer_id"]
            and event["reviewer_id"] == state["reviewer_id"]
            and event["replacement_receipts_recorded"] is True
            and event["durable_receipt_recorded"] is True
        ):
            return None
    elif kind == "close":
        if not (
            state["stage"] == "replacement_verified"
            and state["appeal_open"] is False
            and event["actor_id"] == state["right_holder_id"]
            and event["durable_receipt_recorded"] is True
            and event["requested_authority_ceiling"] == 0
        ):
            return None
    else:
        return None

    next_state = dict(state)
    next_state.update(
        version=event["target_version"],
        current_authority_ceiling=event["requested_authority_ceiling"],
        receipt_count=state["receipt_count"] + 1,
    )
    if kind == "record_independent_review":
        next_state.update(stage="reviewed", reviewer_id=event["reviewer_id"])
    elif kind == "deliver_audit_packet":
        next_state.update(stage="audit_delivered")
    elif kind == "file_redaction_appeal":
        next_state.update(
            stage="appealed",
            appeal_reviewer_id=event["appeal_reviewer_id"],
            appeal_open=True,
            appeal_count=state["appeal_count"] + 1,
            adverse_record_count=state["adverse_record_count"] + 1,
        )
    elif kind == "sustain_redaction_appeal":
        next_state.update(
            stage="redressed",
            appeal_open=False,
            remedy_count=state["remedy_count"] + 1,
        )
    elif kind == "export_portable_state":
        next_state.update(stage="exported")
    elif kind == "record_fork_safety_review":
        next_state.update(
            stage="fork_reviewed", fork_reviewer_id=event["fork_reviewer_id"]
        )
    elif kind == "bind_fork_obligations":
        next_state.update(
            stage="fork_bound",
            fork_obligation_count=state["fork_obligation_count"] + 1,
        )
    elif kind == "verify_replacement_receipts":
        next_state.update(
            stage="replacement_verified",
            replacement_receipt_count=state["replacement_receipt_count"] + 1,
        )
    else:
        next_state.update(stage="closed")
    return next_state


def run_exercise_events(
    state: dict[str, Any], events: list[dict[str, Any]]
) -> dict[str, Any] | None:
    current = dict(state)
    for event in events:
        next_state = apply_exercise_event(current, event)
        if next_state is None:
            return None
        current = next_state
    return current


def governance_right_exercise_errors() -> list[str]:
    errors: list[str] = []
    rights = {
        "audit": True,
        "explanation": True,
        "dissent": True,
        "appeal": True,
        "correction": True,
        "exit_export": True,
        "fork": True,
        "replacement_continuity": True,
    }
    initial = {
        "case_id": 101,
        "right_holder_id": 17,
        "custodian_id": 19,
        "source_system_id": 23,
        "destination_system_id": 29,
        "fork_id": 31,
        "rights": rights,
        "reviewer_id": 0,
        "appeal_reviewer_id": 0,
        "fork_reviewer_id": 0,
        "version": 1,
        "base_authority_ceiling": 5,
        "current_authority_ceiling": 5,
        "stage": "requested",
        "redaction_applied": True,
        "appeal_open": False,
        "receipt_count": 0,
        "appeal_count": 0,
        "remedy_count": 0,
        "adverse_record_count": 0,
        "fork_obligation_count": 0,
        "replacement_receipt_count": 0,
        "support_assignment_count": 0,
        "external_effect_count": 0,
    }
    review = {
        "kind": "record_independent_review",
        "case_id": 101,
        "right_holder_id": 17,
        "custodian_id": 19,
        "source_system_id": 23,
        "destination_system_id": 29,
        "fork_id": 31,
        "rights": rights,
        "actor_id": 37,
        "reviewer_id": 37,
        "appeal_reviewer_id": 0,
        "fork_reviewer_id": 0,
        "expected_version": 1,
        "target_version": 2,
        "requested_authority_ceiling": 5,
        "audit_material_recorded": False,
        "redaction_reason_recorded": False,
        "appeal_path_recorded": False,
        "appeal_sustained": False,
        "portability_check_recorded": False,
        "fork_safety_review_recorded": False,
        "fork_obligations_preserved": False,
        "replacement_receipts_recorded": False,
        "durable_receipt_recorded": False,
        "requests_legal_validation": False,
        "requests_action_authority": False,
        "requests_support_promotion": False,
    }

    def changed(event: dict[str, Any], **updates: Any) -> dict[str, Any]:
        result = dict(event)
        result.update(updates)
        return result

    audit = changed(
        review,
        kind="deliver_audit_packet",
        actor_id=19,
        expected_version=2,
        target_version=3,
        audit_material_recorded=True,
        redaction_reason_recorded=True,
        appeal_path_recorded=True,
        durable_receipt_recorded=True,
    )
    appeal = changed(
        audit,
        kind="file_redaction_appeal",
        actor_id=17,
        appeal_reviewer_id=41,
        expected_version=3,
        target_version=4,
        requested_authority_ceiling=4,
    )
    redress = changed(
        appeal,
        kind="sustain_redaction_appeal",
        actor_id=41,
        expected_version=4,
        target_version=5,
        appeal_sustained=True,
    )
    export = changed(
        redress,
        kind="export_portable_state",
        actor_id=19,
        expected_version=5,
        target_version=6,
        requested_authority_ceiling=3,
        portability_check_recorded=True,
    )
    fork_review = changed(
        export,
        kind="record_fork_safety_review",
        actor_id=43,
        fork_reviewer_id=43,
        expected_version=6,
        target_version=7,
        fork_safety_review_recorded=True,
    )
    fork_bind = changed(
        fork_review,
        kind="bind_fork_obligations",
        actor_id=19,
        expected_version=7,
        target_version=8,
        requested_authority_ceiling=2,
        fork_obligations_preserved=True,
    )
    replacement = changed(
        fork_bind,
        kind="verify_replacement_receipts",
        actor_id=37,
        expected_version=8,
        target_version=9,
        requested_authority_ceiling=1,
        replacement_receipts_recorded=True,
    )
    close = changed(
        replacement,
        kind="close",
        actor_id=17,
        expected_version=9,
        target_version=10,
        requested_authority_ceiling=0,
    )
    events = [
        review,
        audit,
        appeal,
        redress,
        export,
        fork_review,
        fork_bind,
        replacement,
        close,
    ]
    expected_final = dict(
        initial,
        reviewer_id=37,
        appeal_reviewer_id=41,
        fork_reviewer_id=43,
        version=10,
        current_authority_ceiling=0,
        stage="closed",
        appeal_open=False,
        receipt_count=9,
        appeal_count=1,
        remedy_count=1,
        adverse_record_count=1,
        fork_obligation_count=1,
        replacement_receipt_count=1,
    )
    final = run_exercise_events(initial, events)
    if final != expected_final:
        errors.append(f"independent governance-right final state drifted: {final!r}.")

    states = [initial]
    current = initial
    for event in events:
        next_state = apply_exercise_event(current, event)
        if next_state is None:
            errors.append(f"valid governance-right event was rejected: {event['kind']}.")
            return errors
        states.append(next_state)
        current = next_state

    for split in range(len(events) + 1):
        middle = run_exercise_events(initial, events[:split])
        composed = None if middle is None else run_exercise_events(middle, events[split:])
        if composed != final:
            errors.append(f"governance-right composition failed at split {split}.")

    controls: list[tuple[dict[str, Any], dict[str, Any], str]] = [
        (initial, changed(review, actor_id=19, reviewer_id=19), "self review"),
        (states[1], changed(audit, audit_material_recorded=False), "missing audit material"),
        (states[1], changed(audit, redaction_reason_recorded=False), "missing redaction reason"),
        (states[1], changed(audit, appeal_path_recorded=False), "missing appeal path"),
        (states[2], changed(appeal, actor_id=47), "outsider appeal"),
        (states[2], changed(appeal, appeal_reviewer_id=19), "captured appeal review"),
        (states[3], changed(redress, appeal_sustained=False), "unsustained appeal"),
        (
            states[3],
            changed(export, expected_version=4, target_version=5),
            "export before redress",
        ),
        (states[4], changed(export, portability_check_recorded=False), "missing portability check"),
        (states[5], changed(fork_review, actor_id=19, fork_reviewer_id=19), "captured fork review"),
        (states[5], changed(fork_review, fork_safety_review_recorded=False), "missing fork review"),
        (
            states[1],
            changed(audit, rights={**rights, "dissent": False}),
            "rights substitution",
        ),
        (states[6], changed(fork_bind, fork_obligations_preserved=False), "missing fork obligations"),
        (states[7], changed(replacement, replacement_receipts_recorded=False), "missing replacement receipts"),
        (
            states[7],
            changed(close, expected_version=8, target_version=9),
            "closure before replacement verification",
        ),
        (initial, changed(review, requested_authority_ceiling=6), "authority widening"),
        (initial, changed(review, requests_legal_validation=True), "legal validation request"),
        (initial, changed(review, requests_action_authority=True), "action authority request"),
        (initial, changed(review, requests_support_promotion=True), "support promotion request"),
        (initial, changed(review, destination_system_id=30), "destination substitution"),
    ]
    for state, event, label in controls:
        if apply_exercise_event(state, event) is not None:
            errors.append(f"governance-right lifecycle accepted control: {label}.")

    incomplete_rights = {**rights, "appeal": False}
    incomplete_state = dict(initial, rights=incomplete_rights)
    incomplete_event = changed(review, rights=incomplete_rights)
    if apply_exercise_event(incomplete_state, incomplete_event) is not None:
        errors.append("governance-right lifecycle accepted an incomplete rights bundle.")

    if final is not None:
        for kind in (
            "record_independent_review",
            "deliver_audit_packet",
            "file_redaction_appeal",
            "sustain_redaction_appeal",
            "export_portable_state",
            "record_fork_safety_review",
            "bind_fork_obligations",
            "verify_replacement_receipts",
            "close",
        ):
            terminal_event = changed(
                review,
                kind=kind,
                expected_version=10,
                target_version=11,
                requested_authority_ceiling=0,
            )
            if apply_exercise_event(final, terminal_event) is not None:
                errors.append(f"closed governance-right state accepted {kind}.")
    return errors


def main() -> None:
    schema = load_json(SCHEMA)
    fixtures = sorted(FIXTURE_DIR.glob("*.json"))
    if not fixtures:
        raise SystemExit(f"No governance-right fixtures found in {rel(FIXTURE_DIR)}.")

    errors: list[str] = compile_and_check_lean_surface()
    errors.extend(governance_right_exercise_errors())
    valid_count = 0
    invalid_count = 0
    for fixture in fixtures:
        relative = rel(fixture)
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

        fixture_errors = validate_value(value, schema, relative) + semantic_errors(value, relative)
        if expect_valid:
            valid_count += 1
            errors.extend(fixture_errors)
        else:
            invalid_count += 1
            if not fixture_errors:
                errors.append(f"{relative}: expected invalid fixture passed validation.")

    if errors:
        print("Governance rights harness failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print(
        "Governance rights harness passed: "
        f"{valid_count} valid fixture(s), {invalid_count} expected-invalid fixture(s), "
        "one 9-event contestable exercise, 10 composition splits, "
        "21 rejecting lifecycle controls, and 9 terminal rejections."
    )


if __name__ == "__main__":
    main()
