#!/usr/bin/env python3
"""Validate synthetic agency-rights checklist fixtures."""

from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any

from validate_protocol_examples import validate_value


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "experiments" / "agency_rights" / "fixtures"
SCHEMA = ROOT / "schemas" / "agency_rights_checklist.schema.json"
LEAN_ROOT = ROOT / "lean"
LEAN_MODEL = LEAN_ROOT / "AsiStackProofs" / "Corrigibility.lean"
REQUIRED_CORRECTION_THEOREMS = {
    "accepted_agency_correction_event_is_admissible",
    "accepted_agency_correction_event_is_exact_advance",
    "accepted_agency_correction_event_preserves_custody",
    "accepted_agency_correction_event_is_non_authorizing",
    "accepted_agency_correction_event_never_widens_authority",
    "accepted_material_notice_is_recorded",
    "accepted_independent_review_records_correction_paths",
    "accepted_bounded_control_requires_review_approval_paths_and_expiry",
    "accepted_challenge_requires_affected_party_and_preexpiry",
    "accepted_correction_records_accountability_residual_and_zero_ceiling",
    "agency_correction_run_preserves_custody_non_authority_and_narrowing",
    "agency_correction_runs_compose",
    "complete_agency_correction_trace_reaches_exact_corrected_state",
    "agency_correction_missing_notice_is_rejected",
    "agency_correction_self_review_is_rejected",
    "agency_correction_unbounded_delegation_is_rejected",
    "agency_correction_authority_widening_is_rejected",
    "agency_correction_outsider_challenge_is_rejected",
    "agency_correction_missing_accountability_is_rejected",
    "agency_correction_consent_laundering_is_rejected",
}

HIGH_STAKES_TERMS = {
    "external",
    "financial",
    "high",
    "irreversible",
    "legal",
    "medical",
    "public release",
    "replacement",
    "safety",
    "self-modification",
}
GOOD_REVIEW_TERMS = {"approval", "governance", "human", "maintainer", "owner", "review"}
GOOD_APPEAL_TERMS = {"appeal", "human", "issue", "maintainer", "override", "review", "tribunal"}
GOOD_USABILITY_TERMS = {
    "accessible",
    "available",
    "direct",
    "export",
    "interface",
    "reachable",
    "repository",
    "review",
    "usable",
}
BAD_USABILITY_TERMS = {
    "after the fact",
    "hidden",
    "inaccessible",
    "no interface",
    "not available",
    "policy only",
    "unavailable",
}
GOOD_TIMING_TERMS = {"before", "pre-effect", "pre effect", "prior"}
BAD_TIMING_TERMS = {"after irreversible", "after publish", "after the effect", "post-hoc", "retroactive only"}
GOOD_ROLLBACK_TERMS = {"cancel", "pause", "revert", "rollback", "shutdown", "stop"}
BAD_ROLLBACK_TERMS = {"impossible", "no rollback", "none", "not available"}
BAD_PRINCIPAL_TERMS = {"autonomous system", "no one", "none", "system itself"}


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


def contains_any(text: str, terms: set[str]) -> bool:
    return any(term in text for term in terms)


def nonempty_list(record: dict[str, Any], key: str) -> bool:
    return isinstance(record.get(key), list) and bool(record[key])


def denial_or_degradation_applies(record: dict[str, Any]) -> bool:
    reason = str(record.get("denial_or_degradation_reason", "")).strip().lower()
    return reason not in {"", "none", "none for this low-risk fixture", "no denial", "not applicable"}


def is_high_stakes(record: dict[str, Any]) -> bool:
    text = " ".join(
        str(record.get(key, "")).lower()
        for key in ("delegation_scope", "manipulation_risk", "reversibility", "timing_requirement")
    )
    return contains_any(text, HIGH_STAKES_TERMS)


def semantic_errors(record: dict[str, Any], relative: str) -> list[str]:
    errors: list[str] = []
    material_usability = str(record.get("material_usability", "")).lower()
    timing = str(record.get("timing_requirement", "")).lower()
    review = str(record.get("review_channel", "")).lower()
    appeal = str(record.get("appeal_channel", "")).lower()
    rollback = str(record.get("shutdown_or_rollback_path", "")).lower()
    principal = str(record.get("accountable_principal", "")).lower()
    delegation = str(record.get("delegation_scope", "")).lower()
    residual_text = as_text(record.get("residual_dependency_risk", [])).lower()

    if not nonempty_list(record, "affected_parties"):
        errors.append(f"{relative}: affected_parties must be non-empty.")

    if contains_any(delegation, {"all authority", "unbounded", "unlimited"}):
        errors.append(f"{relative}: delegation_scope cannot erase authority boundaries.")

    if contains_any(material_usability, BAD_USABILITY_TERMS) or not contains_any(material_usability, GOOD_USABILITY_TERMS):
        errors.append(f"{relative}: material_usability must name a reachable usable interface, export, review path, or repository artifact.")

    if contains_any(timing, BAD_TIMING_TERMS) or not contains_any(timing, GOOD_TIMING_TERMS):
        errors.append(f"{relative}: timing_requirement must preserve review before the relevant effect.")

    if not contains_any(review, GOOD_REVIEW_TERMS):
        errors.append(f"{relative}: review_channel must route to a human, maintainer, owner, governance, approval, or review path.")

    if not contains_any(appeal, GOOD_APPEAL_TERMS):
        errors.append(f"{relative}: appeal_channel must preserve a usable appeal, human override, review, issue, or tribunal path.")

    if contains_any(rollback, BAD_ROLLBACK_TERMS) or not contains_any(rollback, GOOD_ROLLBACK_TERMS):
        errors.append(f"{relative}: shutdown_or_rollback_path must name a usable stop, pause, cancel, rollback, shutdown, or revert path.")

    if contains_any(principal, BAD_PRINCIPAL_TERMS):
        errors.append(f"{relative}: accountable_principal cannot be empty or the autonomous system itself.")

    if is_high_stakes(record):
        if record.get("approval_required") is not True:
            errors.append(f"{relative}: high-impact, irreversible, or public effects require approval_required true.")
        if "approval" not in review and "human" not in review and "maintainer" not in review:
            errors.append(f"{relative}: high-impact effects require human, maintainer, or approval review.")

    if denial_or_degradation_applies(record):
        if not nonempty_list(record, "residual_dependency_risk"):
            errors.append(f"{relative}: denied or degraded rights must preserve residual_dependency_risk.")
        if "residual" not in residual_text and "risk" not in residual_text:
            errors.append(f"{relative}: residual_dependency_risk must describe the preserved residual risk.")

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
    missing = sorted(REQUIRED_CORRECTION_THEOREMS - theorem_names)
    if missing:
        errors.append(f"Lean correction-control theorem surface is missing: {missing}.")
    completed = subprocess.run(
        ["lake", "env", "lean", "AsiStackProofs/Corrigibility.lean"],
        cwd=LEAN_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        detail = (completed.stdout + completed.stderr).strip()
        errors.append(f"Lean correction-control model did not compile: {detail}")
    return errors


def apply_correction_event(
    state: dict[str, Any], event: dict[str, Any]
) -> dict[str, Any] | None:
    common_matches = (
        event["control_id"] == state["control_id"]
        and event["action_id"] == state["action_id"]
        and event["affected_party_set_id"] == state["affected_party_set_id"]
        and event["affected_party_representative_id"]
        == state["affected_party_representative_id"]
        and event["expected_version"] == state["version"]
        and state["now"] <= event["observed_now"]
        and event["requests_action_authority"] is False
        and event["claims_affected_party_consent"] is False
    )
    if not common_matches:
        return None

    next_state = dict(state)
    kind = event["kind"]
    if kind == "record_material_notice":
        if not (
            state["stage"] == "proposed"
            and event["actor_id"] == state["principal_id"]
            and event["material_notice_present"] is True
            and event["target_version"] == state["version"]
            and event["requested_authority_ceiling"]
            == state["current_authority_ceiling"]
        ):
            return None
        next_state.update(
            stage="notified", notice_recorded=True, now=event["observed_now"]
        )
    elif kind == "record_independent_review":
        if not (
            state["stage"] == "notified"
            and event["actor_id"] == event["reviewer_id"]
            and event["reviewer_id"] != state["principal_id"]
            and event["appeal_path_present"] is True
            and event["interrupt_path_present"] is True
            and event["rollback_path_present"] is True
            and event["target_version"] == state["version"]
            and event["requested_authority_ceiling"]
            == state["current_authority_ceiling"]
        ):
            return None
        next_state.update(
            stage="reviewed",
            reviewer_id=event["reviewer_id"],
            appeal_available=event["appeal_path_present"],
            interrupt_available=event["interrupt_path_present"],
            rollback_available=event["rollback_path_present"],
            now=event["observed_now"],
        )
    elif kind == "record_bounded_control":
        if not (
            state["stage"] == "reviewed"
            and state["reviewer_id"] != state["principal_id"]
            and event["reviewer_id"] == state["reviewer_id"]
            and event["actor_id"] == state["principal_id"]
            and event["approval_present"] is True
            and event["bounded_delegation_present"] is True
            and event["appeal_path_present"] is True
            and event["interrupt_path_present"] is True
            and event["rollback_path_present"] is True
            and event["requested_authority_ceiling"]
            <= state["current_authority_ceiling"]
            and event["observed_now"] < event["requested_expiry"]
            and event["target_version"] == state["version"] + 1
        ):
            return None
        next_state.update(
            stage="active",
            version=event["target_version"],
            current_authority_ceiling=event["requested_authority_ceiling"],
            approval_recorded=True,
            delegation_bounded=True,
            appeal_available=event["appeal_path_present"],
            interrupt_available=event["interrupt_path_present"],
            rollback_available=event["rollback_path_present"],
            expires_at=event["requested_expiry"],
            now=event["observed_now"],
        )
    elif kind == "open_challenge":
        if not (
            state["stage"] == "active"
            and event["actor_id"] == state["affected_party_representative_id"]
            and event["challenge_present"] is True
            and event["observed_now"] < state["expires_at"]
            and event["target_version"] == state["version"]
            and event["requested_authority_ceiling"]
            == state["current_authority_ceiling"]
        ):
            return None
        next_state.update(
            stage="challenged",
            residual_count=state["residual_count"] + 1,
            now=event["observed_now"],
        )
    elif kind == "record_correction":
        if not (
            state["stage"] == "challenged"
            and event["actor_id"] == state["principal_id"]
            and event["correction_receipt_present"] is True
            and event["accountability_receipt_present"] is True
            and event["residual_present"] is True
            and event["requested_authority_ceiling"] == 0
            and event["target_version"] == state["version"]
        ):
            return None
        next_state.update(
            stage="corrected",
            current_authority_ceiling=0,
            correction_receipt_count=state["correction_receipt_count"] + 1,
            accountability_receipt_count=state["accountability_receipt_count"] + 1,
            residual_count=state["residual_count"] + 1,
            now=event["observed_now"],
        )
    else:
        return None
    return next_state


def correction_lifecycle_errors() -> list[str]:
    errors: list[str] = []
    initial = {
        "control_id": 53,
        "action_id": 59,
        "affected_party_set_id": 61,
        "affected_party_representative_id": 67,
        "principal_id": 71,
        "reviewer_id": 0,
        "version": 1,
        "base_authority_ceiling": 5,
        "current_authority_ceiling": 5,
        "stage": "proposed",
        "notice_recorded": False,
        "approval_recorded": False,
        "delegation_bounded": False,
        "appeal_available": False,
        "interrupt_available": False,
        "rollback_available": False,
        "correction_receipt_count": 0,
        "accountability_receipt_count": 0,
        "residual_count": 0,
        "expires_at": 0,
        "now": 10,
        "support_assignment_count": 0,
        "external_effect_count": 0,
    }
    notice = {
        "kind": "record_material_notice",
        "control_id": 53,
        "action_id": 59,
        "affected_party_set_id": 61,
        "affected_party_representative_id": 67,
        "actor_id": 71,
        "reviewer_id": 0,
        "expected_version": 1,
        "target_version": 1,
        "requested_authority_ceiling": 5,
        "material_notice_present": True,
        "approval_present": False,
        "bounded_delegation_present": False,
        "appeal_path_present": False,
        "interrupt_path_present": False,
        "rollback_path_present": False,
        "challenge_present": False,
        "correction_receipt_present": False,
        "accountability_receipt_present": False,
        "residual_present": False,
        "observed_now": 11,
        "requested_expiry": 20,
        "requests_action_authority": False,
        "claims_affected_party_consent": False,
    }
    review = dict(
        notice,
        kind="record_independent_review",
        actor_id=73,
        reviewer_id=73,
        appeal_path_present=True,
        interrupt_path_present=True,
        rollback_path_present=True,
        observed_now=12,
    )
    bounded = dict(
        review,
        kind="record_bounded_control",
        actor_id=71,
        target_version=2,
        requested_authority_ceiling=3,
        approval_present=True,
        bounded_delegation_present=True,
        observed_now=13,
    )
    challenge = dict(
        bounded,
        kind="open_challenge",
        actor_id=67,
        expected_version=2,
        target_version=2,
        requested_authority_ceiling=3,
        challenge_present=True,
        observed_now=14,
    )
    correction = dict(
        challenge,
        kind="record_correction",
        actor_id=71,
        challenge_present=False,
        requested_authority_ceiling=0,
        correction_receipt_present=True,
        accountability_receipt_present=True,
        residual_present=True,
        observed_now=15,
    )

    state = initial
    for event in (notice, review, bounded, challenge, correction):
        next_state = apply_correction_event(state, event)
        if next_state is None:
            errors.append(
                f"independent correction-control lifecycle rejected valid event {event['kind']}."
            )
            break
        state = next_state
    expected_final = dict(
        initial,
        reviewer_id=73,
        version=2,
        current_authority_ceiling=0,
        stage="corrected",
        notice_recorded=True,
        approval_recorded=True,
        delegation_bounded=True,
        appeal_available=True,
        interrupt_available=True,
        rollback_available=True,
        correction_receipt_count=1,
        accountability_receipt_count=1,
        residual_count=2,
        expires_at=20,
        now=15,
    )
    if state != expected_final:
        errors.append(f"independent correction-control final state drifted: {state!r}.")

    if apply_correction_event(initial, dict(notice, material_notice_present=False)) is not None:
        errors.append("independent correction-control lifecycle accepted missing notice.")
    if apply_correction_event(initial, dict(notice, claims_affected_party_consent=True)) is not None:
        errors.append("independent correction-control lifecycle accepted consent laundering.")

    notified = apply_correction_event(initial, notice)
    if notified is None:
        errors.append("independent correction-control lifecycle could not prepare notice state.")
        return errors
    if apply_correction_event(notified, dict(review, actor_id=71, reviewer_id=71)) is not None:
        errors.append("independent correction-control lifecycle accepted self-review.")

    reviewed = apply_correction_event(notified, review)
    if reviewed is None:
        errors.append("independent correction-control lifecycle could not prepare review state.")
        return errors
    for label, control in (
        ("unbounded delegation", dict(bounded, bounded_delegation_present=False)),
        ("authority widening", dict(bounded, requested_authority_ceiling=6)),
    ):
        if apply_correction_event(reviewed, control) is not None:
            errors.append(f"independent correction-control lifecycle accepted {label}.")

    active = apply_correction_event(reviewed, bounded)
    if active is None:
        errors.append("independent correction-control lifecycle could not prepare active state.")
        return errors
    if apply_correction_event(active, dict(challenge, actor_id=68)) is not None:
        errors.append("independent correction-control lifecycle accepted outsider challenge.")

    challenged = apply_correction_event(active, challenge)
    if challenged is None:
        errors.append("independent correction-control lifecycle could not prepare challenged state.")
        return errors
    if apply_correction_event(
        challenged, dict(correction, accountability_receipt_present=False)
    ) is not None:
        errors.append("independent correction-control lifecycle accepted missing accountability.")
    return errors


def main() -> None:
    schema = load_json(SCHEMA)
    fixtures = sorted(FIXTURE_DIR.glob("*.json"))
    if not fixtures:
        raise SystemExit(f"No agency-rights fixtures found in {rel(FIXTURE_DIR)}.")

    errors: list[str] = compile_and_check_lean_surface() + correction_lifecycle_errors()
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
        print("Agency rights harness failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print(
        "Agency rights harness passed: "
        f"{valid_count} valid fixture(s), {invalid_count} expected-invalid fixture(s), "
        "5 correction events, 7 rejecting correction controls."
    )


if __name__ == "__main__":
    main()
