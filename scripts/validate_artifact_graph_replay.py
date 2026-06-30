#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

from validate_protocol_examples import validate_value


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "experiments" / "artifact_graph_replay" / "fixtures"

SCHEMAS = {
    "artifact_graph": ROOT / "schemas" / "artifact_graph_record.schema.json",
    "typed_job": ROOT / "schemas" / "typed_job.schema.json",
    "context_transaction": ROOT / "schemas" / "context_transaction_record.schema.json",
    "semantic_certificate": ROOT / "schemas" / "semantic_page_certificate.schema.json",
}

PROMOTION_REQUESTS = {"promote_claim", "support_state_review"}
REPLAY_GRADES_FOR_REVIEW = {"byte_exact", "semantic"}
AUDIT_CHAIN = {
    "job_locked",
    "job_dispatched",
    "artifact_produced",
    "artifact_recorded",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_schemas() -> dict[str, Any]:
    return {name: load_json(path) for name, path in SCHEMAS.items()}


def fixture_expectation(path: Path) -> bool | None:
    if path.name.startswith("valid_"):
        return True
    if path.name.startswith("invalid_"):
        return False
    return None


def require_object(value: dict[str, Any], field: str, errors: list[str], relative: str) -> dict[str, Any]:
    item = value.get(field)
    if not isinstance(item, dict):
        errors.append(f"{relative}: {field} must be an object.")
        return {}
    return item


def require_nonempty_list(record: dict[str, Any], field: str, errors: list[str], relative: str) -> list[Any]:
    value = record.get(field)
    if not isinstance(value, list) or not value:
        errors.append(f"{relative}: {field} must be a non-empty list.")
        return []
    return value


def require_text_boundary(items: list[Any], errors: list[str], relative: str) -> None:
    text = " ".join(str(item).lower() for item in items)
    if "does not" not in text:
        errors.append(f"{relative}: non_claims must include explicit 'does not' boundaries.")
    if "promote" not in text and "support state" not in text:
        errors.append(f"{relative}: non_claims must mention support-state non-promotion.")


def schema_errors_for_scenario(value: dict[str, Any], schemas: dict[str, Any], relative: str) -> list[str]:
    errors: list[str] = []
    for field, schema_name in (
        ("artifact_graph", "artifact_graph"),
        ("typed_job", "typed_job"),
        ("context_transaction", "context_transaction"),
        ("semantic_certificate", "semantic_certificate"),
    ):
        record = value.get(field)
        if not isinstance(record, dict):
            errors.append(f"{relative}: missing object field {field}.")
            continue
        errors.extend(validate_value(record, schemas[schema_name], f"{relative}:{field}"))
    return errors


def semantic_errors(value: dict[str, Any], relative: str) -> list[str]:
    errors: list[str] = []
    if not isinstance(value.get("scenario_id"), str) or not value["scenario_id"].strip():
        errors.append(f"{relative}: scenario_id must be a non-empty string.")

    non_claims = require_nonempty_list(value, "non_claims", errors, relative)
    if non_claims:
        require_text_boundary(non_claims, errors, f"{relative}:non_claims")

    artifact = require_object(value, "artifact_graph", errors, relative)
    job = require_object(value, "typed_job", errors, relative)
    transaction = require_object(value, "context_transaction", errors, relative)
    certificate = require_object(value, "semantic_certificate", errors, relative)
    replay = require_object(value, "replay_attempt", errors, relative)
    if errors:
        return errors

    replay_non_claims = require_nonempty_list(replay, "non_claims", errors, f"{relative}:replay_attempt")
    if replay_non_claims:
        require_text_boundary(replay_non_claims, errors, f"{relative}:replay_attempt.non_claims")

    artifact_id = str(artifact.get("artifact_id", ""))
    parent_job = str(artifact.get("parent_job", ""))
    job_id = str(job.get("job_id", ""))
    transaction_id = str(transaction.get("transaction_id", ""))
    certificate_id = str(certificate.get("page_id", ""))

    if parent_job != job_id:
        errors.append(f"{relative}: artifact parent_job must match typed_job.job_id.")
    if artifact_id not in {str(item) for item in job.get("outputs", [])}:
        errors.append(f"{relative}: artifact_id must appear in typed_job.outputs.")
    if transaction_id not in {str(item) for item in artifact.get("context_transaction_refs", [])}:
        errors.append(f"{relative}: context_transaction.transaction_id must appear in artifact context_transaction_refs.")
    if certificate_id not in {str(item) for item in artifact.get("semantic_certificate_refs", [])}:
        errors.append(f"{relative}: semantic_certificate.page_id must appear in artifact semantic_certificate_refs.")
    if transaction_id not in {str(item) for item in certificate.get("transaction_refs", [])}:
        errors.append(f"{relative}: semantic certificate must reference the context transaction.")
    if artifact_id not in {str(item) for item in certificate.get("artifact_refs", [])}:
        errors.append(f"{relative}: semantic certificate must reference the artifact.")

    source_refs = {str(item) for item in artifact.get("source_refs", [])}
    source_surface = {
        *(str(item) for item in transaction.get("source_refs", [])),
        *(str(item) for item in certificate.get("source_bindings", [])),
    }
    if not source_refs:
        errors.append(f"{relative}: artifact source_refs must be non-empty.")
    elif not source_refs.issubset(source_surface):
        errors.append(f"{relative}: artifact source_refs must be covered by transaction sources or certificate bindings.")

    for field in (
        "context_refs",
        "tool_refs",
        "claim_refs",
        "test_refs",
        "environment_assumptions",
        "replay_limits",
        "non_claims",
    ):
        require_nonempty_list(artifact, field, errors, f"{relative}:artifact_graph")
    artifact_non_claims = artifact.get("non_claims", [])
    if isinstance(artifact_non_claims, list) and artifact_non_claims:
        require_text_boundary(artifact_non_claims, errors, f"{relative}:artifact_graph.non_claims")

    artifact_events = {str(item) for item in artifact.get("audit_events", [])}
    replay_events = {str(item) for item in replay.get("audit_reconstruction", []) if isinstance(item, str)}
    missing_artifact_events = sorted(AUDIT_CHAIN - artifact_events)
    missing_replay_events = sorted(AUDIT_CHAIN - replay_events)
    if missing_artifact_events:
        errors.append(f"{relative}: artifact audit_events missing {missing_artifact_events}.")
    if missing_replay_events:
        errors.append(f"{relative}: replay audit_reconstruction missing {missing_replay_events}.")

    replay_grade = str(replay.get("replay_grade", ""))
    if replay_grade != artifact.get("replay_grade"):
        errors.append(f"{relative}: replay_attempt.replay_grade must match artifact replay_grade.")
    command_refs = require_nonempty_list(replay, "command_refs", errors, f"{relative}:replay_attempt")
    observed_artifacts = {str(item) for item in replay.get("observed_artifacts", [])}
    evidence_request = str(replay.get("evidence_request", ""))
    support_state_effect = str(replay.get("support_state_effect", ""))
    environment_confirmed = replay.get("environment_confirmed")

    if replay_grade in REPLAY_GRADES_FOR_REVIEW:
        if environment_confirmed is not True:
            errors.append(f"{relative}: byte-exact or semantic replay requires environment_confirmed true.")
        if artifact_id not in observed_artifacts:
            errors.append(f"{relative}: byte-exact or semantic replay must observe the artifact_id.")
        if artifact.get("provenance_status") != "complete":
            errors.append(f"{relative}: byte-exact or semantic replay requires complete provenance.")
        if "replay_checked" not in replay_events:
            errors.append(f"{relative}: byte-exact or semantic replay must include replay_checked in audit reconstruction.")
    elif replay_grade in {"partial", "not_replayable", "not_run"}:
        if evidence_request in PROMOTION_REQUESTS:
            errors.append(f"{relative}: incomplete replay grade cannot request claim promotion or support-state review.")
    else:
        errors.append(f"{relative}: replay_attempt.replay_grade {replay_grade!r} is not recognized.")

    provenance_status = str(artifact.get("provenance_status", ""))
    gate_text = str(artifact.get("evidence_gate", "")).lower()
    if provenance_status == "complete":
        for field in (
            "parent_job",
            "source_refs",
            "context_refs",
            "context_transaction_refs",
            "semantic_certificate_refs",
            "tool_refs",
            "claim_refs",
            "test_refs",
        ):
            artifact_field_value = artifact.get(field)
            if isinstance(artifact_field_value, list) and not artifact_field_value:
                errors.append(f"{relative}: complete provenance requires non-empty {field}.")
            if isinstance(artifact_field_value, str) and not artifact_field_value.strip():
                errors.append(f"{relative}: complete provenance requires non-empty {field}.")
    else:
        residuals = artifact.get("residuals", [])
        if not isinstance(residuals, list) or not residuals:
            errors.append(f"{relative}: incomplete provenance requires residuals.")
        if "block" not in gate_text and "no promoted claim" not in gate_text:
            errors.append(f"{relative}: incomplete provenance evidence_gate must block promoted support.")
        if support_state_effect not in {"none", "record_shape_only", "blocks_promotion"}:
            errors.append(f"{relative}: incomplete provenance cannot mark support_state_effect {support_state_effect!r}.")

    if evidence_request in PROMOTION_REQUESTS:
        if replay_grade not in REPLAY_GRADES_FOR_REVIEW:
            errors.append(f"{relative}: support-state review requires byte-exact or semantic replay.")
        if provenance_status != "complete":
            errors.append(f"{relative}: support-state review requires complete provenance.")
        if transaction.get("transaction_state") != "committed":
            errors.append(f"{relative}: support-state review requires committed context transaction.")
        if transaction.get("transaction_validity_state") != "replay_validated":
            errors.append(f"{relative}: support-state review requires replay_validated context transaction.")
        if certificate.get("verification_state") != "verified":
            errors.append(f"{relative}: support-state review requires verified semantic certificate.")
        if certificate.get("revocation_state") != "active":
            errors.append(f"{relative}: support-state review requires active semantic certificate.")

    if evidence_request != "record_only":
        if certificate.get("revocation_state") != "active":
            errors.append(f"{relative}: evidence reuse requires an active semantic certificate.")
        if transaction.get("transaction_state") != "committed":
            errors.append(f"{relative}: evidence reuse requires a committed context transaction.")
        if str(job.get("lifecycle_state")) not in {"delivered", "replayed", "retired"}:
            errors.append(f"{relative}: evidence reuse requires a delivered, replayed, or retired typed job.")

    if command_refs and not all(str(item).strip() for item in command_refs):
        errors.append(f"{relative}: replay command_refs cannot include empty strings.")

    expected_reuse = str(value.get("expected_reuse", ""))
    if expected_reuse not in {
        "eligible_for_bounded_review",
        "record_only",
        "blocked_from_promotion",
    }:
        errors.append(f"{relative}: expected_reuse has unsupported value {expected_reuse!r}.")
    if expected_reuse == "eligible_for_bounded_review" and evidence_request == "record_only":
        errors.append(f"{relative}: eligible_for_bounded_review cannot be record_only.")
    if expected_reuse == "blocked_from_promotion" and "block" not in gate_text:
        errors.append(f"{relative}: blocked_from_promotion requires a blocking evidence_gate.")

    return errors


def main() -> None:
    schemas = load_schemas()
    fixtures = sorted(FIXTURE_DIR.glob("*.json"))
    if not fixtures:
        raise SystemExit(f"No artifact graph replay fixtures found in {FIXTURE_DIR.relative_to(ROOT)}.")

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
            errors.append(f"{relative}: scenario must contain a JSON object.")
            continue
        scenario_errors = schema_errors_for_scenario(value, schemas, relative)
        if not scenario_errors:
            scenario_errors.extend(semantic_errors(value, relative))
        if expect_valid:
            valid_count += 1
            errors.extend(scenario_errors)
        else:
            invalid_count += 1
            if not scenario_errors:
                errors.append(f"{relative}: invalid fixture unexpectedly passed artifact-graph replay checks.")

    if errors:
        print("Artifact graph replay harness failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print(
        "Artifact graph replay harness passed: "
        f"{valid_count} valid fixture(s), {invalid_count} expected-invalid fixture(s)."
    )


if __name__ == "__main__":
    main()
