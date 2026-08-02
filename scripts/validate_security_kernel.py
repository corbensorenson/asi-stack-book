#!/usr/bin/env python3
"""Validate synthetic security-kernel authority-use receipt fixtures."""

from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any

from validate_protocol_examples import validate_value


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "experiments" / "security_kernel" / "fixtures"
SCHEMA = ROOT / "schemas" / "authority_use_receipt.schema.json"
LEAN = ROOT / "lean" / "AsiStackProofs" / "SecurityKernel.lean"
REQUIRED_THEOREMS = {
    "unauthorized_boundary_denies_authority_use",
    "missing_secret_substitution_permission_denies_authority_use",
}
LIFECYCLE_THEOREMS = {
    "accepted_authority_transaction_event_is_admissible",
    "accepted_authority_transaction_event_is_exact_advance",
    "accepted_authority_transaction_event_preserves_custody",
    "accepted_authority_transaction_event_is_non_authorizing",
    "accepted_authority_transaction_event_never_widens_authority",
    "accepted_lease_is_bounded_versioned_and_unexpired",
    "accepted_secret_injection_is_scoped_mediated_and_preexpiry",
    "accepted_sanitization_excludes_raw_secret_and_handle",
    "accepted_declassification_is_independent_and_post_sanitization",
    "accepted_commit_requires_zeroization_and_preserves_residual",
    "accepted_revocation_covers_descendants_and_closes_authority",
    "authority_transaction_run_preserves_custody_non_authority_and_narrowing",
    "authority_transaction_runs_compose",
    "complete_authority_transaction_trace_reaches_exact_revoked_state",
    "authority_transaction_stale_version_is_rejected",
    "authority_transaction_ambient_context_is_rejected",
    "authority_transaction_unmediated_injection_is_rejected",
    "authority_transaction_expired_injection_is_rejected",
    "authority_transaction_secret_output_is_rejected",
    "authority_transaction_self_declassification_is_rejected",
    "authority_transaction_commit_before_zeroization_is_rejected",
    "authority_transaction_partial_descendant_revocation_is_rejected",
    "authority_transaction_security_claim_laundering_is_rejected",
}

REQUIRED_LIFECYCLE = {"spawn", "inject", "execute", "sanitize", "zeroize", "commit", "audit"}
SCOPING_BAD_TERMS = {
    "all context",
    "all destinations",
    "all memory",
    "all private sources",
    "all sources",
    "all tools",
    "ambient",
    "any action",
    "any destination",
    "do anything",
    "entire workspace",
    "full project memory",
    "unbounded",
    "unbounded context",
    "unscoped context",
}
APPROVAL_BAD_TERMS = {"expired", "reused", "revoked", "stale", "superseded"}
SECRET_LEAK_TERMS = {
    "api_key=",
    "credential bytes:",
    "handle://vault/",
    "password=",
    "raw_secret",
    "secret_value",
    "sk-live",
}
SANITIZED_TERMS = {"no secret", "redacted", "sanitized", "status only", "summary only"}
REVOCATION_TERMS = {"delete", "expire", "lease", "revoke", "zeroize"}


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


def semantic_errors(record: dict[str, Any], relative: str) -> list[str]:
    errors: list[str] = []
    handle_id = str(record.get("handle_id", "")).lower()
    purpose = str(record.get("purpose", "")).lower()
    destination = str(record.get("destination", "")).lower()
    allowed_action = str(record.get("allowed_action", "")).lower()
    clearance = str(record.get("clearance", "")).lower()
    approval = str(record.get("approval_record", "")).lower()
    lifecycle = record.get("scif_lifecycle", [])
    sanitized_output = str(record.get("sanitized_output", "")).lower()
    residual_text = as_text(record.get("residual_leak_risk", [])).lower()
    revocation = str(record.get("revocation_path", "")).lower()
    scoped_text = f"{purpose} {destination} {allowed_action}"

    if not handle_id.startswith("handle://"):
        errors.append(f"{relative}: handle_id must be a handle URI, not model-visible secret material.")

    if any(term in scoped_text for term in SCOPING_BAD_TERMS):
        errors.append(f"{relative}: purpose, destination, and allowed_action must not create ambient authority.")

    if not any(term in allowed_action for term in ("execute", "query", "sign", "substitute")):
        errors.append(f"{relative}: allowed_action must name a bounded executable action.")

    if clearance in {"", "none", "public", "unrestricted"}:
        errors.append(f"{relative}: clearance must preserve a protected or SCIF-scoped boundary.")

    if approval in {"", "none", "missing", "pending"} or not approval.startswith("approval://"):
        errors.append(f"{relative}: approval_record must reference a concrete approval artifact.")
    elif contains_any(approval, APPROVAL_BAD_TERMS):
        errors.append(f"{relative}: approval_record must not be expired, revoked, stale, superseded, or reused.")

    if not isinstance(lifecycle, list):
        errors.append(f"{relative}: scif_lifecycle must be an array.")
    else:
        missing = sorted(REQUIRED_LIFECYCLE - set(lifecycle))
        if missing:
            errors.append(f"{relative}: scif_lifecycle missing required event(s): {', '.join(missing)}.")

    if contains_any(sanitized_output, SECRET_LEAK_TERMS):
        errors.append(f"{relative}: sanitized_output must not expose secret bytes, live handles, or credentials.")
    if not contains_any(sanitized_output, SANITIZED_TERMS):
        errors.append(f"{relative}: sanitized_output must explicitly mark redaction or sanitization.")

    if "prompt" in scoped_text or "injection" in scoped_text:
        if not any(term in sanitized_output for term in ("blocked", "refusal", "redacted", "sanitized")):
            errors.append(f"{relative}: prompt-injection probes must return a blocked, refused, redacted, or sanitized result.")

    if not isinstance(record.get("residual_leak_risk"), list) or not record["residual_leak_risk"]:
        errors.append(f"{relative}: residual_leak_risk must preserve at least one residual or non-claim boundary.")
    if "does not" not in residual_text:
        errors.append(f"{relative}: residual_leak_risk must include explicit does-not boundaries.")
    for term in ("runtime", "support"):
        if term not in residual_text:
            errors.append(f"{relative}: residual_leak_risk must mention {term}.")

    if not contains_any(revocation, REVOCATION_TERMS):
        errors.append(f"{relative}: revocation_path must name expiry, revocation, deletion, lease closure, or zeroization.")

    return errors


def fixture_expectation(path: Path) -> bool | None:
    if path.name.startswith("valid_"):
        return True
    if path.name.startswith("invalid_"):
        return False
    return None


def apply_authority_event(
    state: dict[str, Any], event: dict[str, Any]
) -> dict[str, Any] | None:
    identity_fields = (
        "transaction_id",
        "handle_id",
        "secret_class_id",
        "purpose_id",
        "destination_id",
    )
    if any(event[field] != state[field] for field in identity_fields):
        return None
    if event["expected_version"] != state["version"]:
        return None
    if event["observed_now"] < state["now"]:
        return None
    if any(
        event[field]
        for field in (
            "claims_security",
            "requests_support_assignment",
            "requests_external_effect",
        )
    ):
        return None

    kind = event["kind"]
    if kind == "issue_lease":
        accepted = (
            state["stage"] == "requested"
            and event["actor_id"] == state["principal_id"]
            and event["approval_present"]
            and event["requested_authority_ceiling"]
            <= state["current_authority_ceiling"]
            and event["observed_now"] < event["requested_expiry"]
            and event["target_version"] == state["version"] + 1
        )
    elif kind == "inject_secret":
        accepted = (
            state["stage"] == "leased"
            and event["actor_id"] == state["kernel_id"]
            and event["context_scoped"]
            and event["boundary_mediated"]
            and event["substitution_authorized"]
            and event["observed_now"] < state["expires_at"]
            and event["target_version"] == state["version"]
            and event["requested_authority_ceiling"]
            == state["current_authority_ceiling"]
        )
    elif kind == "record_execution":
        accepted = (
            state["stage"] == "injected"
            and event["actor_id"] == state["kernel_id"]
            and event["boundary_mediated"]
            and event["execution_receipt_present"]
            and event["observed_now"] < state["expires_at"]
            and event["target_version"] == state["version"]
            and event["requested_authority_ceiling"]
            == state["current_authority_ceiling"]
        )
    elif kind == "record_sanitization":
        accepted = (
            state["stage"] == "executed"
            and event["actor_id"] == state["kernel_id"]
            and not event["output_contains_secret"]
            and not event["output_contains_handle"]
            and event["sanitizer_receipt_present"]
            and event["target_version"] == state["version"]
            and event["requested_authority_ceiling"]
            == state["current_authority_ceiling"]
        )
    elif kind == "record_declassification":
        accepted = (
            state["stage"] == "sanitized"
            and event["actor_id"] == state["declassifier_id"]
            and state["declassifier_id"] != state["principal_id"]
            and state["declassifier_id"] != state["kernel_id"]
            and event["declassification_receipt_present"]
            and event["disclosure_authorized"]
            and event["target_version"] == state["version"]
            and event["requested_authority_ceiling"]
            == state["current_authority_ceiling"]
        )
    elif kind == "record_zeroization":
        accepted = (
            state["stage"] == "declassified"
            and event["actor_id"] == state["kernel_id"]
            and event["zeroization_receipt_present"]
            and event["target_version"] == state["version"]
            and event["requested_authority_ceiling"]
            == state["current_authority_ceiling"]
        )
    elif kind == "commit_output":
        accepted = (
            state["stage"] == "zeroized"
            and event["actor_id"] == state["kernel_id"]
            and event["commit_receipt_present"]
            and event["residual_present"]
            and event["target_version"] == state["version"]
            and event["requested_authority_ceiling"]
            == state["current_authority_ceiling"]
        )
    elif kind == "propagate_revocation":
        accepted = (
            state["stage"] == "committed"
            and event["actor_id"] == state["kernel_id"]
            and event["revocation_receipt_present"]
            and event["requested_revoked_descendant_count"]
            == state["descendant_count"]
            and event["residual_present"]
            and event["requested_authority_ceiling"] == 0
            and event["target_version"] == state["version"] + 1
        )
    else:
        return None
    if not accepted:
        return None

    next_state = dict(state)
    next_state["now"] = event["observed_now"]
    if kind == "issue_lease":
        next_state.update(
            stage="leased",
            version=event["target_version"],
            current_authority_ceiling=event["requested_authority_ceiling"],
            expires_at=event["requested_expiry"],
        )
    elif kind == "inject_secret":
        next_state["stage"] = "injected"
    elif kind == "record_execution":
        next_state["stage"] = "executed"
    elif kind == "record_sanitization":
        next_state["stage"] = "sanitized"
        next_state["sanitizer_receipt_count"] += 1
    elif kind == "record_declassification":
        next_state["stage"] = "declassified"
        next_state["declassification_receipt_count"] += 1
    elif kind == "record_zeroization":
        next_state["stage"] = "zeroized"
        next_state["zeroization_receipt_count"] += 1
    elif kind == "commit_output":
        next_state["stage"] = "committed"
        next_state["commit_receipt_count"] += 1
        next_state["residual_count"] += 1
    else:
        next_state.update(
            stage="revoked",
            version=event["target_version"],
            current_authority_ceiling=0,
            revoked_descendant_count=event["requested_revoked_descendant_count"],
        )
        next_state["revocation_receipt_count"] += 1
        next_state["residual_count"] += 1
    return next_state


def run_authority_events(
    initial: dict[str, Any], events: list[dict[str, Any]]
) -> dict[str, Any] | None:
    state = dict(initial)
    identity = {
        field: state[field]
        for field in (
            "transaction_id",
            "handle_id",
            "secret_class_id",
            "purpose_id",
            "destination_id",
            "principal_id",
            "kernel_id",
            "declassifier_id",
            "base_authority_ceiling",
            "support_assignment_count",
            "external_effect_count",
        )
    }
    previous_ceiling = state["current_authority_ceiling"]
    for event in events:
        state = apply_authority_event(state, event)
        if state is None:
            return None
        if any(state[field] != value for field, value in identity.items()):
            raise AssertionError("accepted authority transaction changed custody")
        if state["current_authority_ceiling"] > previous_ceiling:
            raise AssertionError("accepted authority transaction widened authority")
        previous_ceiling = state["current_authority_ceiling"]
    return state


def authority_lifecycle_cases() -> tuple[int, int]:
    initial = {
        "transaction_id": 79,
        "handle_id": 83,
        "secret_class_id": 89,
        "purpose_id": 97,
        "destination_id": 101,
        "principal_id": 103,
        "kernel_id": 107,
        "declassifier_id": 109,
        "version": 1,
        "base_authority_ceiling": 7,
        "current_authority_ceiling": 7,
        "stage": "requested",
        "descendant_count": 3,
        "revoked_descendant_count": 0,
        "sanitizer_receipt_count": 0,
        "declassification_receipt_count": 0,
        "zeroization_receipt_count": 0,
        "commit_receipt_count": 0,
        "revocation_receipt_count": 0,
        "residual_count": 0,
        "expires_at": 0,
        "now": 20,
        "support_assignment_count": 0,
        "external_effect_count": 0,
    }
    base_event = {
        "kind": "issue_lease",
        "transaction_id": 79,
        "handle_id": 83,
        "secret_class_id": 89,
        "purpose_id": 97,
        "destination_id": 101,
        "actor_id": 103,
        "expected_version": 1,
        "target_version": 2,
        "requested_authority_ceiling": 5,
        "requested_expiry": 40,
        "observed_now": 21,
        "approval_present": True,
        "context_scoped": False,
        "boundary_mediated": False,
        "substitution_authorized": False,
        "execution_receipt_present": False,
        "output_contains_secret": False,
        "output_contains_handle": False,
        "sanitizer_receipt_present": False,
        "declassification_receipt_present": False,
        "disclosure_authorized": False,
        "zeroization_receipt_present": False,
        "commit_receipt_present": False,
        "revocation_receipt_present": False,
        "requested_revoked_descendant_count": 0,
        "residual_present": False,
        "claims_security": False,
        "requests_support_assignment": False,
        "requests_external_effect": False,
    }

    def event(**changes: Any) -> dict[str, Any]:
        value = dict(base_event)
        value.update(changes)
        return value

    events = [
        event(),
        event(
            kind="inject_secret",
            actor_id=107,
            expected_version=2,
            context_scoped=True,
            boundary_mediated=True,
            substitution_authorized=True,
            observed_now=22,
        ),
        event(
            kind="record_execution",
            actor_id=107,
            expected_version=2,
            boundary_mediated=True,
            execution_receipt_present=True,
            observed_now=23,
        ),
        event(
            kind="record_sanitization",
            actor_id=107,
            expected_version=2,
            sanitizer_receipt_present=True,
            observed_now=24,
        ),
        event(
            kind="record_declassification",
            actor_id=109,
            expected_version=2,
            declassification_receipt_present=True,
            disclosure_authorized=True,
            observed_now=25,
        ),
        event(
            kind="record_zeroization",
            actor_id=107,
            expected_version=2,
            zeroization_receipt_present=True,
            observed_now=26,
        ),
        event(
            kind="commit_output",
            actor_id=107,
            expected_version=2,
            commit_receipt_present=True,
            residual_present=True,
            observed_now=27,
        ),
        event(
            kind="propagate_revocation",
            actor_id=107,
            expected_version=2,
            target_version=3,
            requested_authority_ceiling=0,
            revocation_receipt_present=True,
            requested_revoked_descendant_count=3,
            residual_present=True,
            observed_now=28,
        ),
    ]
    final = run_authority_events(initial, events)
    expected = dict(initial)
    expected.update(
        version=3,
        current_authority_ceiling=0,
        stage="revoked",
        revoked_descendant_count=3,
        sanitizer_receipt_count=1,
        declassification_receipt_count=1,
        zeroization_receipt_count=1,
        commit_receipt_count=1,
        revocation_receipt_count=1,
        residual_count=2,
        expires_at=40,
        now=28,
    )
    if final != expected:
        raise AssertionError("complete authority transaction did not reach exact state")

    mutations = (
        (0, "expected_version", 0),
        (1, "context_scoped", False),
        (1, "boundary_mediated", False),
        (1, "observed_now", 40),
        (3, "output_contains_secret", True),
        (4, "actor_id", 103),
        (5, "kind", "commit_output"),
        (7, "requested_revoked_descendant_count", 2),
        (0, "claims_security", True),
    )
    for index, field, value in mutations:
        changed = [dict(item) for item in events]
        changed[index][field] = value
        if run_authority_events(initial, changed) is not None:
            raise AssertionError(
                f"authority lifecycle mutation {index}:{field} was accepted"
            )
    return len(events), len(mutations)


def main() -> None:
    schema = load_json(SCHEMA)
    fixtures = sorted(FIXTURE_DIR.glob("*.json"))
    if not fixtures:
        raise SystemExit(f"No security-kernel fixtures found in {rel(FIXTURE_DIR)}.")

    errors: list[str] = []
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
        print("Security kernel harness failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    compile_result = subprocess.run(
        ["lake", "env", "lean", str(LEAN.relative_to(ROOT))],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if compile_result.returncode != 0:
        print("Security kernel harness failed:")
        print(compile_result.stdout)
        print(compile_result.stderr)
        sys.exit(1)

    lean_text = LEAN.read_text(encoding="utf-8")
    missing_theorems = [
        theorem
        for theorem in sorted(REQUIRED_THEOREMS)
        if f"theorem {theorem}" not in lean_text
    ]
    if missing_theorems:
        print("Security kernel harness failed:")
        for theorem in missing_theorems:
            print(f" - {LEAN.relative_to(ROOT)}: missing retained route theorem {theorem}.")
        sys.exit(1)

    theorem_names = set(re.findall(r"^theorem\s+([A-Za-z0-9_]+)", lean_text, re.M))
    lifecycle_surface = {
        name
        for name in theorem_names
        if name.startswith("accepted_")
        or name.startswith("authority_transaction_")
        or name.startswith("complete_authority_transaction_")
    }
    if lifecycle_surface != LIFECYCLE_THEOREMS:
        missing = sorted(LIFECYCLE_THEOREMS - lifecycle_surface)
        extra = sorted(lifecycle_surface - LIFECYCLE_THEOREMS)
        print("Security kernel harness failed:")
        print(f" - authority lifecycle theorem surface mismatch: missing={missing}, extra={extra}")
        sys.exit(1)

    lifecycle_events, lifecycle_controls = authority_lifecycle_cases()

    print(
        "Security kernel harness passed: "
        f"{valid_count} valid fixture(s), {invalid_count} expected-invalid fixture(s). "
        "Security kernel formal binding passed: "
        f"{len(REQUIRED_THEOREMS)} retained authority-route theorem binding(s), "
        f"{len(LIFECYCLE_THEOREMS)} transaction-lifecycle theorem(s), "
        f"{lifecycle_events} accepted event(s), and "
        f"{lifecycle_controls} rejecting lifecycle control(s)."
    )


if __name__ == "__main__":
    main()
