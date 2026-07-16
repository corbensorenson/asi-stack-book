#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

from validate_protocol_examples import validate_value


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "experiments" / "context_transaction_memory_store" / "fixtures"
SCHEMA = ROOT / "schemas" / "context_transaction_record.schema.json"
LEAN_FILE = ROOT / "lean" / "AsiStackProofs" / "ContextTransactionRefinement.lean"
RESULT_DOC = ROOT / "experiments" / "context_transaction_memory_store" / "results" / "2026-07-01-local.md"

VALID_STATES = {"shape_validated", "store_validated", "replay_validated"}
SUPPORT_PROMOTION_EFFECTS = {
    "eligible_for_bounded_evidence_review",
    "synthetic-test-backed",
    "empirical-test-backed",
    "prototype-backed",
}

EXPECTED_LEAN_BRIDGE_TERMS = (
    "structure TransactionState",
    "def TransactionRun",
    "theorem accepted_snapshot_read_preserves_snapshot_branch_mount_and_version",
    "theorem accepted_untainted_derivation_from_tainted_source_requires_declassification",
    "theorem accepted_materialization_preserves_transaction_custody",
    "theorem exact_transaction_trace_materializes",
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


def event_key(event: dict[str, Any]) -> str:
    return f"{event.get('cell_id')}@{event.get('snapshot_id')}"


def semantic_errors(value: dict[str, Any], relative: str) -> list[str]:
    errors: list[str] = []
    if not isinstance(value.get("scenario_id"), str) or not value["scenario_id"].strip():
        errors.append(f"{relative}: scenario_id must be a non-empty string.")
    memory_events = value.get("memory_events")
    if not isinstance(memory_events, list):
        errors.append(f"{relative}: memory_events must be a list.")
    transactions = value.get("context_transactions")
    if not isinstance(transactions, list):
        errors.append(f"{relative}: context_transactions must be a list.")
    store_review = value.get("store_review")
    if not isinstance(store_review, dict):
        errors.append(f"{relative}: store_review must be an object.")
    artifact_replay_refs = require_nonempty_list(value, "artifact_replay_refs", errors, relative)
    non_claims = require_nonempty_list(value, "non_claims", errors, relative)
    if errors:
        return errors

    for field in (
        "read_visibility_checked",
        "branch_isolation_checked",
        "mount_visibility_checked",
        "deletion_closure_checked",
        "taint_propagation_checked",
        "replay_boundary_recorded",
        "support_promotion_requested",
        "deployed_store_claim_requested",
    ):
        require_bool(store_review, field, errors, f"{relative}:store_review")
    if errors:
        return errors

    required_checks = [
        "read_visibility_checked",
        "branch_isolation_checked",
        "mount_visibility_checked",
        "deletion_closure_checked",
        "taint_propagation_checked",
        "replay_boundary_recorded",
    ]
    for field in required_checks:
        if not store_review[field]:
            errors.append(f"{relative}: bounded memory-store fixture must record {field}.")

    if store_review["support_promotion_requested"]:
        errors.append(f"{relative}: memory-store fixtures cannot request support-state promotion.")
    if store_review["deployed_store_claim_requested"]:
        errors.append(f"{relative}: bounded fixture cannot claim deployed memory-store behavior.")

    non_claim_text = text_blob(non_claims)
    for term in ("synthetic", "deployed memory", "support"):
        if term not in non_claim_text:
            errors.append(f"{relative}: non_claims must mention {term}.")

    event_by_cell_snapshot: dict[str, dict[str, Any]] = {}
    events_by_cell: dict[str, list[dict[str, Any]]] = {}
    deleted_cells: set[str] = set()
    for index, event in enumerate(memory_events):
        prefix = f"{relative}:memory_events[{index}]"
        if not isinstance(event, dict):
            errors.append(f"{prefix}: event must be an object.")
            continue
        for field in ("event_id", "cell_id", "snapshot_id", "mount"):
            if not isinstance(event.get(field), str) or not event[field].strip():
                errors.append(f"{prefix}: {field} must be a non-empty string.")
        for field in ("committed", "deleted"):
            if not isinstance(event.get(field), bool):
                errors.append(f"{prefix}: {field} must be a boolean.")
        for field in ("visible_in_snapshots", "taint_labels", "derivative_of"):
            if not isinstance(event.get(field), list):
                errors.append(f"{prefix}: {field} must be a list.")
        if errors:
            continue
        key = event_key(event)
        if key in event_by_cell_snapshot:
            errors.append(f"{prefix}: duplicate cell/snapshot event {key}.")
        event_by_cell_snapshot[key] = event
        events_by_cell.setdefault(str(event["cell_id"]), []).append(event)
        if event["deleted"]:
            deleted_cells.add(str(event["cell_id"]))

    if errors:
        return errors

    allowed_mounts = set(str(item) for item in value.get("allowed_mounts", []))
    if not allowed_mounts:
        errors.append(f"{relative}: allowed_mounts must be a non-empty list.")

    validated_transaction_count = 0
    for index, transaction in enumerate(transactions):
        prefix = f"{relative}:context_transactions[{index}]"
        if not isinstance(transaction, dict):
            errors.append(f"{prefix}: transaction must be an object.")
            continue
        if transaction.get("transaction_validity_state") in VALID_STATES:
            validated_transaction_count += 1
        if transaction.get("support_state_effect") in SUPPORT_PROMOTION_EFFECTS:
            errors.append(f"{prefix}: transaction cannot promote support state.")
        if str(transaction.get("replay_boundary", "")).lower() in {"", "none", "unrecorded"}:
            errors.append(f"{prefix}: replay_boundary must be recorded.")
        if not transaction.get("audit_refs"):
            errors.append(f"{prefix}: audit_refs must preserve the fixture replay boundary.")

        unauthorized_mounts = sorted(set(str(item) for item in transaction.get("mounts", [])) - allowed_mounts)
        if unauthorized_mounts:
            if transaction.get("transaction_state") != "faulted":
                errors.append(f"{prefix}: unauthorized mounts {unauthorized_mounts} must fault the transaction.")
            if transaction.get("materialization_state") not in {"faulted", "blocked", "not_materialized"}:
                errors.append(f"{prefix}: unauthorized mount transaction cannot materialize.")
            if not transaction.get("faults"):
                errors.append(f"{prefix}: unauthorized mount transaction requires a typed fault.")

        if transaction.get("operation") == "read":
            for cell_id in transaction.get("read_set", []):
                matching_events = [
                    event
                    for event in events_by_cell.get(str(cell_id), [])
                    if event.get("committed")
                    and not event.get("deleted")
                    and transaction.get("snapshot_id") in event.get("visible_in_snapshots", [])
                ]
                if not matching_events:
                    errors.append(
                        f"{prefix}: read cell {cell_id!r} has no committed non-deleted event visible in snapshot "
                        f"{transaction.get('snapshot_id')!r}."
                    )

        if transaction.get("operation") in {"write", "commit"}:
            for cell_id in transaction.get("write_set", []):
                key = f"{cell_id}@{transaction.get('snapshot_id')}"
                event = event_by_cell_snapshot.get(key)
                if event is None or not event.get("committed"):
                    errors.append(f"{prefix}: write_set cell {cell_id!r} must have a committed memory event in its snapshot.")

        if transaction.get("isolation_state") == "leaked":
            if transaction.get("materialization_state") == "materializable":
                errors.append(f"{prefix}: leaked branch isolation cannot be materializable.")
            if not transaction.get("promotion_blockers") and not transaction.get("faults"):
                errors.append(f"{prefix}: leaked branch isolation requires promotion blockers or faults.")

        has_deletion_obligation = bool(transaction.get("deletion_obligations"))
        reads_deleted_source = any(str(cell_id) in deleted_cells for cell_id in transaction.get("read_set", []))
        derives_deleted_source = any(str(cell_id) in deleted_cells for cell_id in transaction.get("derivative_refs", []))
        if has_deletion_obligation or reads_deleted_source or derives_deleted_source:
            if transaction.get("closure_state") != "satisfied":
                if transaction.get("materialization_state") == "materializable":
                    errors.append(f"{prefix}: open deletion obligation cannot be materializable.")
                if not transaction.get("promotion_blockers") and not transaction.get("faults"):
                    errors.append(f"{prefix}: open deletion obligation requires blockers or faults.")

        has_taint = bool(transaction.get("taint_labels"))
        if has_taint and transaction.get("taint_propagation") == "propagated":
            if not transaction.get("declassification_refs") and transaction.get("materialization_state") == "materializable":
                errors.append(f"{prefix}: propagated taint without declassification cannot be materializable.")
            if not transaction.get("declassification_refs") and not transaction.get("promotion_blockers"):
                errors.append(f"{prefix}: propagated taint without declassification requires promotion blockers.")

        if transaction.get("materialization_state") == "materializable":
            if transaction.get("transaction_state") != "committed":
                errors.append(f"{prefix}: materializable transaction must be committed.")
            if transaction.get("transaction_validity_state") not in VALID_STATES:
                errors.append(f"{prefix}: materializable transaction requires store or replay validation.")
            if transaction.get("faults"):
                errors.append(f"{prefix}: materializable transaction cannot carry open faults.")

    if validated_transaction_count == 0:
        errors.append(f"{relative}: at least one transaction must be shape/store/replay validated.")

    replay_text = text_blob(artifact_replay_refs, store_review.get("replay_boundary_note", ""))
    if store_review["replay_boundary_recorded"] and "artifact" not in replay_text:
        errors.append(f"{relative}: replay boundary must name an artifact replay reference.")

    return errors


def fixture_errors(value: dict[str, Any], schema: dict[str, Any], relative: str) -> list[str]:
    errors: list[str] = []
    transactions = value.get("context_transactions")
    if isinstance(transactions, list):
        for index, transaction in enumerate(transactions):
            errors.extend(
                validate_value(
                    transaction,
                    schema,
                    f"{relative}:context_transactions[{index}]",
                )
            )
    else:
        errors.append(f"{relative}: context_transactions must be a list.")
    if not errors:
        errors.extend(semantic_errors(value, relative))
    return errors


def main() -> None:
    schema = load_json(SCHEMA)
    fixtures = sorted(FIXTURE_DIR.glob("*.json"))
    if not fixtures:
        raise SystemExit(f"No context-transaction memory-store fixtures found in {FIXTURE_DIR.relative_to(ROOT)}.")

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

        current_errors = fixture_errors(value, schema, relative)
        if expect_valid:
            valid_count += 1
            errors.extend(current_errors)
        else:
            invalid_count += 1
            if not current_errors:
                errors.append(f"{relative}: expected invalid fixture passed validation.")

    if not LEAN_FILE.exists():
        errors.append(f"{LEAN_FILE.relative_to(ROOT)}: missing Lean bridge module.")
    else:
        lean_text = LEAN_FILE.read_text(encoding="utf-8")
        for term in EXPECTED_LEAN_BRIDGE_TERMS:
            if term not in lean_text:
                errors.append(f"{LEAN_FILE.relative_to(ROOT)}: missing Lean bridge term {term!r}.")

    if RESULT_DOC.exists():
        result_text = RESULT_DOC.read_text(encoding="utf-8")
        for term in (
            "3 valid fixture(s), 6 expected-invalid fixture(s)",
            "support-state non-promotion",
            "does not implement a deployed memory store",
        ):
            if term not in result_text:
                errors.append(f"{RESULT_DOC.relative_to(ROOT)}: missing result boundary term {term!r}.")

    if valid_count != 3:
        errors.append(f"Expected 3 valid context memory-store fixtures, found {valid_count}.")
    if invalid_count != 6:
        errors.append(f"Expected 6 expected-invalid context memory-store fixtures, found {invalid_count}.")

    if errors:
        print("Context transaction memory-store harness failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print(
        "Context transaction memory-store harness passed: "
        f"{valid_count} valid fixture(s), {invalid_count} expected-invalid fixture(s)."
    )


if __name__ == "__main__":
    main()
