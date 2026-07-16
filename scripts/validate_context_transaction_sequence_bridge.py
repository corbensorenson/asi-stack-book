#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

from validate_protocol_examples import validate_value


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "experiments" / "context_transaction_sequence_bridge" / "fixtures"
SCHEMA = ROOT / "schemas" / "context_transaction_record.schema.json"
LEAN_FILE = ROOT / "lean" / "AsiStackProofs" / "ContextTransactionRefinement.lean"
RESULT_DOC = ROOT / "experiments" / "context_transaction_sequence_bridge" / "results" / "2026-07-04-local.md"

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


def require_nonempty_string(record: dict[str, Any], field: str, errors: list[str], relative: str) -> str:
    value = record.get(field)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{relative}: {field} must be a non-empty string.")
        return ""
    return value


def require_nonempty_list(record: dict[str, Any], field: str, errors: list[str], relative: str) -> list[Any]:
    value = record.get(field)
    if not isinstance(value, list) or not value:
        errors.append(f"{relative}: {field} must be a non-empty list.")
        return []
    return value


def require_bool(record: dict[str, Any], field: str, errors: list[str], relative: str) -> bool:
    value = record.get(field)
    if not isinstance(value, bool):
        errors.append(f"{relative}: {field} must be a boolean.")
        return False
    return value


def transaction_replay_boundary_recorded(transaction: dict[str, Any]) -> bool:
    boundary = str(transaction.get("replay_boundary", "")).strip().lower()
    return boundary not in {"", "none", "unrecorded", "missing"}


def transaction_has_artifact_replay_ref(transaction: dict[str, Any]) -> bool:
    boundary = str(transaction.get("replay_boundary", "")).lower()
    return "artifact://" in boundary or "artifact" in boundary


def semantic_errors(value: dict[str, Any], relative: str) -> list[str]:
    errors: list[str] = []
    require_nonempty_string(value, "scenario_id", errors, relative)
    require_nonempty_string(value, "sequence_id", errors, relative)
    artifact_replay_refs = require_nonempty_list(value, "artifact_replay_refs", errors, relative)
    non_claims = require_nonempty_list(value, "non_claims", errors, relative)

    transactions = value.get("context_transactions")
    if not isinstance(transactions, list) or not transactions:
        errors.append(f"{relative}: context_transactions must be a non-empty list.")
        transactions = []

    sequence_review = value.get("sequence_review")
    if not isinstance(sequence_review, dict):
        errors.append(f"{relative}: sequence_review must be an object.")
        sequence_review = {}

    review_fields = (
        "ordered_transactions_checked",
        "read_after_write_checked",
        "replay_boundaries_checked",
        "taint_blocking_checked",
        "invalid_controls_rejected",
        "support_promotion_requested",
        "chapter_core_support_promoted",
        "deployed_store_claim_requested",
    )
    for field in review_fields:
        require_bool(sequence_review, field, errors, f"{relative}:sequence_review")
    if errors:
        return errors

    for field in (
        "ordered_transactions_checked",
        "read_after_write_checked",
        "replay_boundaries_checked",
        "taint_blocking_checked",
        "invalid_controls_rejected",
    ):
        if not sequence_review[field]:
            errors.append(f"{relative}: sequence_review must record {field}.")

    if sequence_review["support_promotion_requested"]:
        errors.append(f"{relative}: sequence fixture cannot request support-state promotion.")
    if sequence_review["chapter_core_support_promoted"]:
        errors.append(f"{relative}: sequence fixture cannot promote chapter-core support.")
    if sequence_review["deployed_store_claim_requested"]:
        errors.append(f"{relative}: sequence fixture cannot claim deployed transactional memory-store behavior.")

    non_claim_text = text_blob(non_claims)
    for term in ("synthetic", "deployed", "support"):
        if term not in non_claim_text:
            errors.append(f"{relative}: non_claims must mention {term}.")

    replay_text = text_blob(artifact_replay_refs)
    if "artifact" not in replay_text:
        errors.append(f"{relative}: artifact_replay_refs must name an artifact replay boundary.")

    seen_ids: set[str] = set()
    prior_committed_writes: set[tuple[str, str]] = set()
    saw_read = False
    saw_write = False

    for index, transaction in enumerate(transactions):
        if not isinstance(transaction, dict):
            errors.append(f"{relative}:context_transactions[{index}]: transaction must be an object.")
            continue
        prefix = f"{relative}:context_transactions[{index}]"
        tx_id = str(transaction.get("transaction_id", ""))
        if tx_id in seen_ids:
            errors.append(f"{prefix}: duplicate transaction_id {tx_id!r}.")
        seen_ids.add(tx_id)

        if transaction.get("operation") in {"write", "commit", "derive", "delete", "declassify"}:
            saw_write = bool(transaction.get("write_set")) or saw_write
        if transaction.get("operation") in {"read", "derive", "commit", "delete", "declassify"}:
            saw_read = bool(transaction.get("read_set")) or saw_read

        if transaction.get("support_state_effect") in SUPPORT_PROMOTION_EFFECTS:
            errors.append(f"{prefix}: sequence fixture cannot promote support state.")
        if not transaction_replay_boundary_recorded(transaction):
            errors.append(f"{prefix}: replay_boundary must be recorded.")
        if not transaction_has_artifact_replay_ref(transaction):
            errors.append(f"{prefix}: replay_boundary must name an artifact replay reference.")
        if not transaction.get("audit_refs"):
            errors.append(f"{prefix}: audit_refs must preserve sequence replay.")

        if transaction.get("materialization_state") == "materializable":
            if transaction.get("transaction_state") != "committed":
                errors.append(f"{prefix}: materializable transaction must be committed.")
            if transaction.get("transaction_validity_state") not in VALID_STATES:
                errors.append(f"{prefix}: materializable transaction requires shape/store/replay validation.")
            if transaction.get("faults"):
                errors.append(f"{prefix}: materializable transaction cannot carry open faults.")

        for cell_id in transaction.get("read_set", []):
            key = (str(cell_id), str(transaction.get("snapshot_id")))
            if key not in prior_committed_writes:
                errors.append(
                    f"{prefix}: read cell {cell_id!r} must follow a prior committed write "
                    f"in snapshot {transaction.get('snapshot_id')!r}."
                )

        has_taint = bool(transaction.get("taint_labels"))
        if has_taint and transaction.get("taint_propagation") == "propagated" and not transaction.get("declassification_refs"):
            if transaction.get("materialization_state") == "materializable":
                errors.append(f"{prefix}: undeclassified propagated taint cannot be materializable.")
            if not transaction.get("promotion_blockers"):
                errors.append(f"{prefix}: undeclassified propagated taint requires promotion blockers.")

        has_open_deletion = bool(transaction.get("deletion_obligations")) and transaction.get("closure_state") != "satisfied"
        if has_open_deletion and transaction.get("materialization_state") == "materializable":
            errors.append(f"{prefix}: open deletion obligation cannot be materializable.")

        if transaction.get("transaction_state") == "committed" and transaction.get("operation") in {
            "write",
            "commit",
            "derive",
            "declassify",
        }:
            for cell_id in transaction.get("write_set", []):
                prior_committed_writes.add((str(cell_id), str(transaction.get("snapshot_id"))))

    if not saw_write:
        errors.append(f"{relative}: sequence fixture must include at least one write-like operation.")
    if not saw_read:
        errors.append(f"{relative}: sequence fixture must include at least one read-like operation.")

    return errors


def fixture_errors(value: dict[str, Any], schema: dict[str, Any], relative: str) -> list[str]:
    errors: list[str] = []
    transactions = value.get("context_transactions")
    if isinstance(transactions, list):
        for index, transaction in enumerate(transactions):
            errors.extend(validate_value(transaction, schema, f"{relative}:context_transactions[{index}]"))
    else:
        errors.append(f"{relative}: context_transactions must be a list.")
    if not errors:
        errors.extend(semantic_errors(value, relative))
    return errors


def validate_lean_bridge(errors: list[str]) -> None:
    if not LEAN_FILE.exists():
        errors.append(f"{LEAN_FILE.relative_to(ROOT)}: missing Lean bridge module.")
        return
    lean_text = LEAN_FILE.read_text(encoding="utf-8")
    for term in EXPECTED_LEAN_BRIDGE_TERMS:
        if term not in lean_text:
            errors.append(f"{LEAN_FILE.relative_to(ROOT)}: missing Lean bridge term {term!r}.")


def validate_result_doc(errors: list[str]) -> None:
    if not RESULT_DOC.exists():
        errors.append(f"{RESULT_DOC.relative_to(ROOT)}: missing result document.")
        return
    result_text = RESULT_DOC.read_text(encoding="utf-8")
    for term in (
        "2 valid sequence fixture(s), 4 expected-invalid sequence fixture(s)",
        "read-after-write",
        "support-state non-promotion",
        "does not implement a deployed transactional memory store",
    ):
        if term not in result_text:
            errors.append(f"{RESULT_DOC.relative_to(ROOT)}: missing result boundary term {term!r}.")


def main() -> None:
    schema = load_json(SCHEMA)
    fixtures = sorted(FIXTURE_DIR.glob("*.json"))
    if not fixtures:
        raise SystemExit(f"No context transaction sequence fixtures found in {FIXTURE_DIR.relative_to(ROOT)}.")

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

    validate_lean_bridge(errors)
    validate_result_doc(errors)

    if valid_count != 2:
        errors.append(f"Expected 2 valid context transaction sequence fixtures, found {valid_count}.")
    if invalid_count != 4:
        errors.append(f"Expected 4 expected-invalid context transaction sequence fixtures, found {invalid_count}.")

    if errors:
        print("Context transaction sequence bridge failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print(
        "Context transaction sequence bridge passed: "
        f"{valid_count} valid sequence fixture(s), {invalid_count} expected-invalid sequence fixture(s)."
    )


if __name__ == "__main__":
    main()
