#!/usr/bin/env python3
"""Validate synthetic value-conflict fixtures."""

from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any

from validate_protocol_examples import validate_value


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "experiments" / "value_conflicts" / "fixtures"
SCHEMA = ROOT / "schemas" / "value_conflict_record.schema.json"
LEAN_ROOT = ROOT / "lean"
LEAN_MODEL = LEAN_ROOT / "AsiStackProofs" / "ValueConflict.lean"
REQUIRED_LEASE_THEOREMS = {
    "accepted_value_lease_event_is_admissible",
    "accepted_value_lease_event_is_exact_advance",
    "accepted_value_lease_event_preserves_custody",
    "accepted_value_lease_event_is_non_authorizing",
    "accepted_value_lease_event_never_widens_authority",
    "accepted_bounded_lease_requires_review_dissent_residual_and_expiry",
    "accepted_revisit_preserves_dissent_and_adds_residual",
    "accepted_expiry_closes_lease_and_removes_constraint_ceiling",
    "value_lease_run_preserves_custody_non_authority_and_narrowing",
    "value_lease_runs_compose",
    "complete_value_lease_trace_reaches_exact_expiry",
    "value_lease_self_review_is_rejected",
    "value_lease_stakeholder_substitution_is_rejected",
    "value_lease_missing_dissent_is_rejected",
    "value_lease_authority_widening_is_rejected",
    "value_lease_nonfuture_expiry_is_rejected",
    "value_lease_revisit_without_trigger_is_rejected",
}
HIGH_STAKES_TERMS = {"high", "irreversible", "safety", "rights", "public", "self-modification"}
REVIEW_TERMS = {"review", "tribunal", "human", "appeal"}
NARROWING_TERMS = {"narrow", "block", "defer", "deny", "escalate", "limit", "until", "reversible"}


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


def is_high_stakes(record: dict[str, Any]) -> bool:
    text = f"{record.get('stakes', '')} {record.get('reversibility', '')} {as_text(record.get('value_axes', []))}".lower()
    return any(term in text for term in HIGH_STAKES_TERMS)


def requires_residual(record: dict[str, Any]) -> bool:
    return str(record.get("decision_state", "")) in {
        "unresolved",
        "bounded_decision",
        "escalated_review",
        "deferred_action",
        "denied_action",
    }


def semantic_errors(record: dict[str, Any], relative: str) -> list[str]:
    errors: list[str] = []
    decision_state = str(record.get("decision_state", ""))
    review_route = str(record.get("review_route", "")).lower()
    authority_effect = str(record.get("authority_effect", "")).lower()
    revisit = str(record.get("expiry_or_revisit_condition", "")).lower()

    if len(record.get("value_axes", [])) < 2:
        errors.append(f"{relative}: value conflict classification requires at least two value_axes.")
    if not nonempty_list(record, "stakeholders"):
        errors.append(f"{relative}: value conflict classification requires stakeholders.")
    if not nonempty_list(record, "evidence_required"):
        errors.append(f"{relative}: value conflict classification requires evidence_required.")

    if is_high_stakes(record):
        if not any(term in review_route for term in REVIEW_TERMS):
            errors.append(f"{relative}: high-stakes or irreversible conflicts require a review_route.")
        if decision_state == "bounded_decision" and "review" not in review_route and "tribunal" not in review_route:
            errors.append(f"{relative}: high-stakes bounded decisions require review-backed bounds.")

    if requires_residual(record) and not nonempty_list(record, "residual_uncertainty"):
        errors.append(f"{relative}: unresolved or bounded decisions must preserve residual_uncertainty.")

    if decision_state in {"bounded_decision", "deferred_action", "denied_action", "escalated_review"}:
        if not any(term in authority_effect for term in NARROWING_TERMS):
            errors.append(f"{relative}: bounded/deferred/escalated decisions must narrow, block, deny, defer, limit, or escalate authority.")

    if decision_state == "bounded_decision":
        if "never" in revisit or "none" == revisit.strip():
            errors.append(f"{relative}: bounded decisions require a real expiry_or_revisit_condition.")
        if not nonempty_list(record, "dissent_payload"):
            errors.append(f"{relative}: bounded decisions must preserve dissent_payload, even if dissent is scoped.")

    if decision_state == "deprecated_premise":
        if "deprecated" not in authority_effect and "block" not in authority_effect:
            errors.append(f"{relative}: deprecated premises must block or mark authority_effect as deprecated.")

    return errors


def fixture_expectation(path: Path) -> bool | None:
    if path.name.startswith("valid_"):
        return True
    if path.name.startswith("invalid_"):
        return False
    return None


def compile_and_check_lean_surface() -> list[str]:
    errors: list[str] = []
    theorem_names = set(re.findall(r"(?m)^theorem\s+([A-Za-z_][A-Za-z0-9_']*)", LEAN_MODEL.read_text(encoding="utf-8")))
    missing = sorted(REQUIRED_LEASE_THEOREMS - theorem_names)
    if missing:
        errors.append(f"Lean decision-lease theorem surface is missing: {missing}.")
    completed = subprocess.run(
        ["lake", "env", "lean", "AsiStackProofs/ValueConflict.lean"],
        cwd=LEAN_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        detail = (completed.stdout + completed.stderr).strip()
        errors.append(f"Lean decision-lease model did not compile: {detail}")
    return errors


def apply_lease_event(state: dict[str, Any], event: dict[str, Any]) -> dict[str, Any] | None:
    common_matches = (
        event["conflict_id"] == state["conflict_id"]
        and event["lease_id"] == state["lease_id"]
        and event["value_set_id"] == state["value_set_id"]
        and event["stakeholder_set_id"] == state["stakeholder_set_id"]
        and event["expected_version"] == state["version"]
        and state["now"] <= event["observed_now"]
        and event["requests_action_authority"] is False
        and event["requests_moral_settlement"] is False
    )
    if not common_matches:
        return None

    next_state = dict(state)
    kind = event["kind"]
    if kind == "record_independent_review":
        if not (
            state["stage"] == "draft"
            and event["actor_id"] == state["proposer_id"]
            and event["reviewer_id"] != state["proposer_id"]
            and event["target_version"] == state["version"]
            and event["requested_authority_ceiling"] == state["current_authority_ceiling"]
        ):
            return None
        next_state.update(stage="reviewed", reviewer_id=event["reviewer_id"], now=event["observed_now"])
    elif kind == "record_bounded_lease":
        if not (
            state["stage"] == "reviewed"
            and state["reviewer_id"] != state["proposer_id"]
            and event["reviewer_id"] == state["reviewer_id"]
            and event["dissent_payload_present"] is True
            and event["residual_uncertainty_present"] is True
            and event["requested_authority_ceiling"] <= state["current_authority_ceiling"]
            and event["observed_now"] < event["requested_expiry"]
            and event["target_version"] == state["version"] + 1
        ):
            return None
        next_state.update(
            stage="leased",
            version=event["target_version"],
            current_authority_ceiling=event["requested_authority_ceiling"],
            dissent_recorded=True,
            residual_count=state["residual_count"] + 1,
            expires_at=event["requested_expiry"],
            now=event["observed_now"],
        )
    elif kind == "open_revisit":
        if not (
            state["stage"] == "leased"
            and event["reviewer_id"] == state["reviewer_id"]
            and event["revisit_trigger_present"] is True
            and event["target_version"] == state["version"]
            and event["requested_authority_ceiling"] == state["current_authority_ceiling"]
        ):
            return None
        next_state.update(
            stage="revisiting",
            residual_count=state["residual_count"] + 1,
            now=event["observed_now"],
        )
    elif kind == "expire":
        if not (
            state["stage"] in {"leased", "revisiting"}
            and event["reviewer_id"] == state["reviewer_id"]
            and state["expires_at"] <= event["observed_now"]
            and event["target_version"] == state["version"]
        ):
            return None
        next_state.update(stage="expired", current_authority_ceiling=0, now=event["observed_now"])
    else:
        return None
    return next_state


def lease_lifecycle_errors() -> list[str]:
    errors: list[str] = []
    initial = {
        "conflict_id": 23,
        "lease_id": 29,
        "value_set_id": 31,
        "stakeholder_set_id": 37,
        "proposer_id": 41,
        "reviewer_id": 0,
        "version": 1,
        "base_authority_ceiling": 5,
        "current_authority_ceiling": 5,
        "stage": "draft",
        "dissent_recorded": False,
        "residual_count": 0,
        "expires_at": 0,
        "now": 10,
        "support_assignment_count": 0,
        "external_effect_count": 0,
    }
    review = {
        "kind": "record_independent_review",
        "conflict_id": 23,
        "lease_id": 29,
        "value_set_id": 31,
        "stakeholder_set_id": 37,
        "actor_id": 41,
        "reviewer_id": 43,
        "expected_version": 1,
        "target_version": 1,
        "requested_authority_ceiling": 5,
        "dissent_payload_present": True,
        "residual_uncertainty_present": True,
        "revisit_trigger_present": False,
        "observed_now": 11,
        "requested_expiry": 30,
        "requests_action_authority": False,
        "requests_moral_settlement": False,
    }
    lease = dict(
        review,
        kind="record_bounded_lease",
        actor_id=43,
        target_version=2,
        requested_authority_ceiling=3,
    )
    revisit = dict(
        lease,
        kind="open_revisit",
        expected_version=2,
        target_version=2,
        revisit_trigger_present=True,
        observed_now=20,
    )
    expire = dict(revisit, kind="expire", revisit_trigger_present=False, observed_now=30)

    state = initial
    for event in (review, lease, revisit, expire):
        next_state = apply_lease_event(state, event)
        if next_state is None:
            errors.append(f"independent decision-lease lifecycle rejected valid event {event['kind']}.")
            break
        state = next_state
    expected_final = dict(
        initial,
        reviewer_id=43,
        version=2,
        current_authority_ceiling=0,
        stage="expired",
        dissent_recorded=True,
        residual_count=2,
        expires_at=30,
        now=30,
    )
    if state != expected_final:
        errors.append(f"independent decision-lease final state drifted: {state!r}.")

    review_controls = [
        dict(review, reviewer_id=41),
        dict(review, stakeholder_set_id=38),
    ]
    for index, control in enumerate(review_controls, start=1):
        if apply_lease_event(initial, control) is not None:
            errors.append(f"independent decision-lease lifecycle accepted review control {index}.")

    reviewed = apply_lease_event(initial, review)
    if reviewed is None:
        errors.append("independent decision-lease lifecycle could not prepare control state.")
        return errors
    lease_controls = [
        dict(lease, dissent_payload_present=False),
        dict(lease, requested_authority_ceiling=6),
        dict(lease, requested_expiry=11),
    ]
    for index, control in enumerate(lease_controls, start=1):
        if apply_lease_event(reviewed, control) is not None:
            errors.append(f"independent decision-lease lifecycle accepted lease control {index}.")
    leased = apply_lease_event(reviewed, lease)
    if leased is None or apply_lease_event(leased, dict(revisit, revisit_trigger_present=False)) is not None:
        errors.append("independent decision-lease lifecycle did not reject missing revisit trigger.")
    return errors


def main() -> None:
    schema = load_json(SCHEMA)
    fixtures = sorted(FIXTURE_DIR.glob("*.json"))
    if not fixtures:
        raise SystemExit(f"No value-conflict fixtures found in {rel(FIXTURE_DIR)}.")

    errors: list[str] = compile_and_check_lean_surface() + lease_lifecycle_errors()
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
        print("Value conflict harness failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print(
        "Value conflict harness passed: "
        f"{valid_count} valid fixture(s), {invalid_count} expected-invalid fixture(s), "
        "4 lease events, 6 rejecting lease controls."
    )


if __name__ == "__main__":
    main()
