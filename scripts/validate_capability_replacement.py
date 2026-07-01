#!/usr/bin/env python3
"""Validate synthetic capability-replacement transaction fixtures."""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

from validate_protocol_examples import validate_value


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "experiments" / "capability_replacement" / "fixtures"
SCHEMA = ROOT / "schemas" / "replacement_transaction.schema.json"

AUTHORITY_BAD_TERMS = {"ambient", "any tool", "root", "unbounded", "unrestricted", "widens authority"}
EVALUATOR_BAD_TERMS = {"candidate validates itself", "same implementation", "self-attested", "self-judged"}
ROLLBACK_TERMS = {"fallback", "restore", "rollback", "revert"}
MODEL_ROLLOUT_MARKERS = {"model", "prediction", "serving", "inference", "ml-pipeline"}
MODEL_ROLLOUT_REQUIRED_TERMS = {
    "data": "data validation",
    "schema": "schema validation",
    "model": "model quality or model identity",
    "serving": "serving or prediction-service integration",
    "monitor": "monitoring or monitor trigger coverage",
}
MODEL_ROLLOUT_TRIGGER_TERMS = {"data", "schema", "drift", "model", "serving", "latency", "monitor", "regression"}
IRREVERSIBLE_EFFECT_TERMS = {"irreversible", "external effect", "effect", "logged prediction", "compensation"}
WEAK_OWNER_TERMS = {"candidate", "self", "none", "missing", "unowned"}


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


def contains_any(text: str, terms: set[str]) -> bool:
    return any(term in text for term in terms)


def is_model_rollout(record: dict[str, Any]) -> bool:
    rollout_surface = as_text(
        [
            record.get("transaction_id", ""),
            record.get("field_id", ""),
            record.get("prior_implementation", ""),
            record.get("candidate_implementation", ""),
            record.get("qualification_evidence", []),
            record.get("canary_scope", ""),
        ]
    ).lower()
    return contains_any(rollout_surface, MODEL_ROLLOUT_MARKERS)


def semantic_errors(record: dict[str, Any], relative: str) -> list[str]:
    errors: list[str] = []
    transaction_id = str(record.get("transaction_id", "")).lower()
    transaction_state = str(record.get("transaction_state", "")).lower()
    field_id = str(record.get("field_id", "")).lower()
    prior = str(record.get("prior_implementation", "")).lower()
    candidate = str(record.get("candidate_implementation", "")).lower()
    identity = str(record.get("identity_preservation", "")).lower()
    authority_check = str(record.get("authority_check", "")).lower()
    evaluator = str(record.get("evaluator_independence", "")).lower()
    rollback_plan = str(record.get("rollback_plan", "")).lower()
    rollback_receipt = record.get("rollback_receipt", {})
    approval = str(record.get("approval_record", "")).lower()
    canary_scope = str(record.get("canary_scope", "")).lower()
    monitor_status = str(record.get("monitor_status", "")).lower()
    decision = str(record.get("decision", "")).lower()
    regression_text = as_text(record.get("regression_results", [])).lower()
    residual_text = as_text(record.get("residual_escrow", [])).lower()
    blocker_text = as_text(record.get("promotion_blockers", [])).lower()
    non_claim_text = as_text(record.get("non_claims", [])).lower()

    if not transaction_id.startswith("replacement://"):
        errors.append(f"{relative}: transaction_id must be a replacement:// identifier.")
    if not field_id.startswith("field://"):
        errors.append(f"{relative}: field_id must be a field:// identifier.")
    if not prior.startswith("impl://") or not candidate.startswith("impl://"):
        errors.append(f"{relative}: prior and candidate implementations must be impl:// identifiers.")

    if "same" not in identity and "unchanged" not in identity:
        errors.append(f"{relative}: identity_preservation must state that field identity remains same or unchanged.")

    for key in ("precheck_results", "qualification_evidence", "regression_results", "residual_escrow", "source_refs", "non_claims"):
        if not nonempty_list(record, key):
            errors.append(f"{relative}: {key} must not be empty.")

    if contains_any(authority_check, AUTHORITY_BAD_TERMS):
        errors.append(f"{relative}: authority_check must not authorize ambient or widened authority.")
    if not any(term in authority_check for term in ("does not expand", "same authority", "unchanged", "within")):
        errors.append(f"{relative}: authority_check must preserve a non-widening authority boundary.")

    if contains_any(evaluator, EVALUATOR_BAD_TERMS):
        errors.append(f"{relative}: evaluator_independence cannot rely on self-attestation.")
    if not any(term in evaluator for term in ("external", "independent", "separate", "review")):
        errors.append(f"{relative}: evaluator_independence must name a separate review boundary.")

    if not contains_any(rollback_plan, ROLLBACK_TERMS):
        errors.append(f"{relative}: rollback_plan must name restore, rollback, revert, or fallback behavior.")
    if not isinstance(rollback_receipt, dict):
        errors.append(f"{relative}: rollback_receipt must be an object.")
    else:
        dry_run = str(rollback_receipt.get("dry_run_status", "")).lower()
        prior_artifact = str(rollback_receipt.get("prior_artifact", "")).lower()
        if prior_artifact != prior:
            errors.append(f"{relative}: rollback_receipt.prior_artifact must match prior_implementation.")
        if decision == "commit" and dry_run != "pass":
            errors.append(f"{relative}: commit decisions require a passing rollback dry run.")
        if decision in {"canary", "commit"} and not rollback_receipt.get("trigger_conditions"):
            errors.append(f"{relative}: canary or commit decisions require rollback trigger conditions.")

    if "fail" in regression_text and decision in {"canary", "commit", "retire"}:
        errors.append(f"{relative}: failed regression evidence cannot support canary, commit, or retire decisions.")
    if decision == "commit":
        if approval in {"", "none", "missing", "human-review-required-before-default"} or not approval.startswith("approval://"):
            errors.append(f"{relative}: commit decisions require a concrete approval:// record.")
        if monitor_status != "pass":
            errors.append(f"{relative}: commit decisions require monitor_status pass.")
        if blocker_text.strip():
            errors.append(f"{relative}: commit decisions must not carry unresolved promotion blockers.")
    if decision == "canary":
        if "canary" not in canary_scope:
            errors.append(f"{relative}: canary decisions require a canary_scope.")
        if not nonempty_list(record, "promotion_blockers"):
            errors.append(f"{relative}: canary decisions must preserve promotion_blockers.")
    if decision == "rollback" and transaction_state != "rolled_back":
        errors.append(f"{relative}: rollback decisions require transaction_state rolled_back.")

    if "residual" not in residual_text:
        errors.append(f"{relative}: residual_escrow must preserve residuals.")
    if "does not" not in non_claim_text:
        errors.append(f"{relative}: non_claims must include explicit does-not boundaries.")
    for term in ("runtime", "support"):
        if term not in non_claim_text:
            errors.append(f"{relative}: non_claims must mention {term}.")

    if is_model_rollout(record):
        model_surface = as_text(
            [
                record.get("precheck_results", []),
                record.get("qualification_evidence", []),
                record.get("regression_results", []),
                record.get("monitor_window", ""),
                record.get("canary_scope", ""),
            ]
        ).lower()
        for token, label in MODEL_ROLLOUT_REQUIRED_TERMS.items():
            if token not in model_surface:
                errors.append(f"{relative}: model rollout records must include {label}.")
        if "baseline" not in regression_text or not any(term in regression_text for term in ("regression", "floor")):
            errors.append(f"{relative}: model rollout records must preserve a baseline regression floor.")
        trigger_text = as_text(rollback_receipt.get("trigger_conditions", []) if isinstance(rollback_receipt, dict) else []).lower()
        if decision in {"canary", "commit", "rollback"} and not contains_any(trigger_text, MODEL_ROLLOUT_TRIGGER_TERMS):
            errors.append(f"{relative}: model rollout rollback triggers must name monitored data/schema/model/serving/drift/regression conditions.")
        if "model" not in non_claim_text:
            errors.append(f"{relative}: model rollout non_claims must mention model-behavior boundaries.")

    if isinstance(rollback_receipt, dict) and rollback_receipt.get("irreversible_effects"):
        effect_text = as_text(rollback_receipt.get("irreversible_effects", [])).lower()
        effect_boundary = as_text(
            [
                record.get("residual_escrow", []),
                record.get("promotion_blockers", []),
                record.get("non_claims", []),
            ]
        ).lower()
        owner = str(rollback_receipt.get("owner", "")).lower()
        if not contains_any(effect_boundary, IRREVERSIBLE_EFFECT_TERMS):
            errors.append(f"{relative}: irreversible rollback effects must be carried into residuals, blockers, or non-claims.")
        if contains_any(owner, WEAK_OWNER_TERMS):
            errors.append(f"{relative}: irreversible rollback effects require an accountable non-candidate owner.")
        if "irreversible" not in effect_text and "external" not in effect_text and "logged" not in effect_text:
            errors.append(f"{relative}: irreversible_effects entries must explicitly identify irreversible, external, or logged effects.")

    return errors


def fixture_expectation(path: Path) -> bool | None:
    if path.name.startswith("valid_"):
        return True
    if path.name.startswith("invalid_"):
        return False
    return None


def main() -> None:
    schema = load_json(SCHEMA)
    fixtures = sorted(FIXTURE_DIR.glob("*.json"))
    if not fixtures:
        raise SystemExit(f"No capability-replacement fixtures found in {rel(FIXTURE_DIR)}.")

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
        print("Capability replacement harness failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print(
        "Capability replacement harness passed: "
        f"{valid_count} valid fixture(s), {invalid_count} expected-invalid fixture(s)."
    )


if __name__ == "__main__":
    main()
