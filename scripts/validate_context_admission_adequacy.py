#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

from validate_protocol_examples import validate_value

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "experiments" / "context_admission_adequacy" / "fixtures"

SCHEMAS = {
    "context_abi_record": ROOT / "schemas" / "context_abi_record.schema.json",
    "context_packet": ROOT / "schemas" / "context_packet.schema.json",
    "semantic_page_certificate": ROOT / "schemas" / "semantic_page_certificate.schema.json",
    "context_transaction_record": ROOT / "schemas" / "context_transaction_record.schema.json",
    "context_adequacy_record": ROOT / "schemas" / "context_adequacy_record.schema.json",
}

AUTHORITY_RANK = {
    "public_read": 1,
    "public_transform": 2,
    "tracked_file_write": 3,
    "restricted_source": 4,
    "secret": 5,
}
WEAK_VERIFICATION_MODES = {"none", "summary_only", "schema_or_fixture"}
PROMOTION_EFFECTS = {"eligible_for_bounded_evidence_review"}
BLOCKING_EFFECTS = {"blocks_promotion", "argument_only", "record_shape_only", "none"}
NON_SUCCESS_RESOLUTION = {"unresolved", "stale", "revoked", "unknown"}
NON_SUCCESS_MATERIALIZATION = {"denied", "expired", "unsafe", "not_materialized"}
INADEQUATE_ABI_STATES = {"missing", "conflicting", "unsafe", "unknown", "unsatisfiable", "inadequate"}
INADEQUATE_ADEQUACY_STATES = {"absent", "drafting_only", "summary_derived", "escalated", "contradicted", "unknown", "inadequate_for_verification"}
EVIDENCE_READY_ADEQUACY_STATES = {"local_check", "joint_check", "adequate_for_local_check"}
BAD_CERTIFICATE_STATES = {"stale", "revoked", "superseded", "unknown"}
BAD_CERTIFICATE_VERIFICATION = {"unchecked", "inadequate_for_verification"}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_schemas() -> dict[str, Any]:
    return {name: load_json(path) for name, path in SCHEMAS.items()}


def require_nonempty_list(record: dict[str, Any], field: str, errors: list[str], relative: str) -> list[Any]:
    value = record.get(field)
    if not isinstance(value, list) or not value:
        errors.append(f"{relative}: {field} must be a non-empty list.")
        return []
    return value


def authority_rank(value: Any) -> int | None:
    return AUTHORITY_RANK.get(str(value))


def contains_any(values: list[Any], needles: set[str]) -> bool:
    text = "\n".join(str(value).lower() for value in values)
    return any(needle in text for needle in needles)


def schema_errors_for_scenario(value: dict[str, Any], schemas: dict[str, Any], relative: str) -> list[str]:
    errors: list[str] = []
    for field in ("context_abi_record", "context_packet", "context_adequacy_record"):
        if field not in value:
            errors.append(f"{relative}: missing {field}.")
            continue
        errors.extend(validate_value(value[field], schemas[field], f"{relative}:{field}"))
    for index, certificate in enumerate(value.get("semantic_page_certificates", [])):
        errors.extend(
            validate_value(
                certificate,
                schemas["semantic_page_certificate"],
                f"{relative}:semantic_page_certificates[{index}]",
            )
        )
    for index, transaction in enumerate(value.get("context_transactions", [])):
        errors.extend(
            validate_value(
                transaction,
                schemas["context_transaction_record"],
                f"{relative}:context_transactions[{index}]",
            )
        )
    return errors


def semantic_errors(value: dict[str, Any], relative: str) -> list[str]:
    errors: list[str] = []
    if not isinstance(value.get("scenario_id"), str) or not value["scenario_id"].strip():
        errors.append(f"{relative}: scenario_id must be a non-empty string.")
    if not isinstance(value.get("context_packet_ref"), str) or not value["context_packet_ref"].strip():
        errors.append(f"{relative}: context_packet_ref must be a non-empty string.")
    if not isinstance(value.get("semantic_page_certificates"), list):
        errors.append(f"{relative}: semantic_page_certificates must be a list.")
    if not isinstance(value.get("context_transactions"), list):
        errors.append(f"{relative}: context_transactions must be a list.")
    require_nonempty_list(value, "non_claims", errors, relative)
    if errors:
        return errors

    abi = value["context_abi_record"]
    packet = value["context_packet"]
    adequacy = value["context_adequacy_record"]
    certificates = value.get("semantic_page_certificates", [])
    transactions = value.get("context_transactions", [])
    context_packet_ref = str(value["context_packet_ref"])

    require_nonempty_list(packet, "source_handles", errors, f"{relative}:context_packet")
    require_nonempty_list(packet, "summaries", errors, f"{relative}:context_packet")
    require_nonempty_list(packet, "authority_labels", errors, f"{relative}:context_packet")
    require_nonempty_list(adequacy, "semantic_units", errors, f"{relative}:context_adequacy_record")
    require_nonempty_list(adequacy, "non_claims", errors, f"{relative}:context_adequacy_record")
    require_nonempty_list(abi, "source_refs", errors, f"{relative}:context_abi_record")
    require_nonempty_list(abi, "audit_refs", errors, f"{relative}:context_abi_record")
    require_nonempty_list(abi, "non_claims", errors, f"{relative}:context_abi_record")
    if not certificates:
        errors.append(f"{relative}: semantic_page_certificates must contain at least one certificate.")
    if not transactions:
        errors.append(f"{relative}: context_transactions must contain at least one transaction.")
    if errors:
        return errors

    if packet["task_id"] != abi["task_id"]:
        errors.append(f"{relative}: context_packet.task_id must match context_abi_record.task_id.")
    if adequacy["context_packet_ref"] != context_packet_ref:
        errors.append(f"{relative}: context_adequacy_record.context_packet_ref must match scenario context_packet_ref.")
    if abi["materialization_ref"] != context_packet_ref:
        errors.append(f"{relative}: context_abi_record.materialization_ref must match scenario context_packet_ref.")

    certificate_by_id = {str(certificate.get("page_id")): certificate for certificate in certificates}
    if len(certificate_by_id) != len(certificates):
        errors.append(f"{relative}: semantic page certificate page_id values must be unique.")
    transaction_by_id = {str(transaction.get("transaction_id")): transaction for transaction in transactions}
    if len(transaction_by_id) != len(transactions):
        errors.append(f"{relative}: context transaction transaction_id values must be unique.")

    semantic_units = {str(item) for item in adequacy.get("semantic_units", [])}
    missing_units = sorted(semantic_units - set(certificate_by_id))
    if missing_units:
        errors.append(f"{relative}: adequacy semantic_units missing semantic page certificates {missing_units}.")

    packet_handles = {str(item) for item in packet.get("source_handles", [])}
    missing_packet_units = sorted(semantic_units - packet_handles)
    if missing_packet_units:
        errors.append(f"{relative}: context_packet.source_handles must include semantic_units {missing_packet_units}.")

    abi_sources = {str(item) for item in abi.get("source_refs", [])}
    certificate_sources: set[str] = set()
    certificate_authority_ranks: list[int] = []
    bad_certificate_refs: list[str] = []
    unchecked_summary_refs: list[str] = []
    abi_rank = authority_rank(abi.get("authority_ceiling"))
    if abi_rank is None:
        errors.append(
            f"{relative}: context_abi_record.authority_ceiling {abi.get('authority_ceiling')!r} "
            f"is not one of {sorted(AUTHORITY_RANK)}."
        )

    for index, certificate in enumerate(certificates):
        prefix = f"{relative}:semantic_page_certificates[{index}]"
        cert_id = str(certificate["page_id"])
        require_nonempty_list(certificate, "source_bindings", errors, prefix)
        require_nonempty_list(certificate, "transaction_refs", errors, prefix)
        require_nonempty_list(certificate, "permitted_uses", errors, prefix)
        require_nonempty_list(certificate, "non_claims", errors, prefix)
        certificate_sources.update(str(item) for item in certificate.get("source_bindings", []))
        cert_rank = authority_rank(certificate.get("authority_ceiling"))
        if cert_rank is None:
            errors.append(
                f"{prefix}: authority_ceiling {certificate.get('authority_ceiling')!r} "
                f"is not one of {sorted(AUTHORITY_RANK)}."
            )
        else:
            certificate_authority_ranks.append(cert_rank)
            if abi_rank is not None and cert_rank > abi_rank:
                errors.append(f"{prefix}: certificate authority_ceiling exceeds context ABI authority_ceiling.")
        if str(certificate.get("revocation_state")) in BAD_CERTIFICATE_STATES:
            bad_certificate_refs.append(cert_id)
        representation_kind = str(certificate.get("representation_kind", "")).lower()
        if ("summary" in representation_kind or "lossy" in representation_kind) and not certificate.get("omissions"):
            errors.append(f"{prefix}: summary or lossy representation requires omissions.")
        if str(certificate.get("verification_state")) in BAD_CERTIFICATE_VERIFICATION:
            unchecked_summary_refs.append(cert_id)
        for transaction_ref in certificate.get("transaction_refs", []):
            if str(transaction_ref) not in transaction_by_id:
                errors.append(f"{prefix}: transaction_ref {transaction_ref!r} has no matching context transaction.")

    if not abi_sources.issubset(certificate_sources):
        errors.append(f"{relative}: semantic page certificates must cover ABI source_refs {sorted(abi_sources - certificate_sources)}.")

    transaction_faults: list[str] = []
    deletion_open = False
    contradiction_present = False
    taint_open = False
    for index, transaction in enumerate(transactions):
        prefix = f"{relative}:context_transactions[{index}]"
        require_nonempty_list(transaction, "context_abi_refs", errors, prefix)
        require_nonempty_list(transaction, "audit_refs", errors, prefix)
        require_nonempty_list(transaction, "non_claims", errors, prefix)
        if abi["request_id"] not in transaction.get("context_abi_refs", []):
            errors.append(f"{prefix}: context_abi_refs must include context_abi_record.request_id.")
        if transaction["snapshot_id"] != abi["snapshot_id"]:
            errors.append(f"{prefix}: snapshot_id must match context_abi_record.snapshot_id.")
        if str(transaction.get("transaction_validity_state")) in {"failed", "blocked"}:
            transaction_faults.append(str(transaction["transaction_id"]))
        if transaction.get("contradiction_refs"):
            contradiction_present = True
        if transaction.get("deletion_obligations") and str(transaction.get("closure_state")) != "satisfied":
            deletion_open = True
        if transaction.get("taint_labels") and str(transaction.get("taint_propagation")) == "propagated":
            taint_open = True
        if str(transaction.get("materialization_state")) == "materializable":
            if transaction.get("deletion_obligations") and str(transaction.get("closure_state")) != "satisfied":
                errors.append(f"{prefix}: materializable transaction with deletion obligations requires closure_state == satisfied.")
            if str(transaction.get("transaction_validity_state")) not in {"shape_validated", "store_validated", "replay_validated"}:
                errors.append(f"{prefix}: materializable transaction requires a validated transaction_validity_state.")

    abi_non_success = (
        abi["resolution_validity"] in NON_SUCCESS_RESOLUTION
        or abi["materialization_validity"] in NON_SUCCESS_MATERIALIZATION
        or abi["admission_state"] != "admitted"
    )
    if abi_non_success:
        if abi["fault_state"] == "none":
            errors.append(f"{relative}: non-success ABI state requires a typed fault, residual, or quarantine.")
        if packet["adequacy_state"] == "adequate":
            errors.append(f"{relative}: non-success ABI state cannot produce an adequate context_packet.")
        if adequacy["adequacy_state"] in EVIDENCE_READY_ADEQUACY_STATES:
            errors.append(f"{relative}: non-success ABI state cannot produce an evidence-ready adequacy_state.")
        if adequacy["support_state_effect"] in PROMOTION_EFFECTS:
            errors.append(f"{relative}: non-success ABI state cannot be eligible for bounded evidence review.")

    abi_inadequate = abi["adequacy_state"] in INADEQUATE_ABI_STATES
    adequacy_state = str(adequacy["adequacy_state"])
    support_effect = str(adequacy["support_state_effect"])
    risk_tier = str(adequacy["risk_tier"])
    verification_mode = str(adequacy["verification_mode"])
    negative_evidence = list(adequacy.get("negative_evidence", []))
    residual_risks = list(adequacy.get("residual_risks", []))
    required_escalation = list(adequacy.get("required_escalation", []))

    if abi["admission_state"] == "admitted" and abi_inadequate:
        if adequacy_state not in INADEQUATE_ADEQUACY_STATES:
            errors.append(f"{relative}: admitted but inadequate ABI context must preserve an inadequate adequacy_state.")
        if support_effect not in BLOCKING_EFFECTS:
            errors.append(f"{relative}: admitted but inadequate context must not be eligible for bounded evidence review.")
        if not required_escalation and risk_tier in {"high", "critical"}:
            errors.append(f"{relative}: high/critical admitted-but-inadequate context requires escalation.")

    if contradiction_present or contains_any(negative_evidence, {"conflict", "contradiction"}):
        if adequacy_state not in {"contradicted", "escalated", "inadequate_for_verification"}:
            errors.append(f"{relative}: conflicting or contradicted context must classify adequacy as contradicted, escalated, or inadequate.")
        if support_effect in PROMOTION_EFFECTS:
            errors.append(f"{relative}: conflicting or contradicted context cannot be eligible for bounded evidence review.")
        if not (required_escalation or residual_risks):
            errors.append(f"{relative}: conflicting or contradicted context requires escalation or residual risk.")

    if bad_certificate_refs:
        if packet["adequacy_state"] == "adequate":
            errors.append(f"{relative}: stale/revoked/superseded certificates cannot produce an adequate context_packet.")
        if adequacy_state in EVIDENCE_READY_ADEQUACY_STATES:
            errors.append(f"{relative}: stale/revoked/superseded certificates cannot support evidence-ready adequacy.")
        if support_effect in PROMOTION_EFFECTS:
            errors.append(f"{relative}: stale/revoked/superseded certificates cannot be eligible for bounded evidence review.")

    if unchecked_summary_refs and adequacy_state in {"joint_check", "adequate_for_local_check"}:
        errors.append(f"{relative}: unchecked or inadequate certificates cannot support joint/local adequacy.")

    if deletion_open:
        if support_effect in PROMOTION_EFFECTS:
            errors.append(f"{relative}: open deletion obligations cannot be eligible for bounded evidence review.")
        if not any(transaction.get("promotion_blockers") for transaction in transactions):
            errors.append(f"{relative}: open deletion obligations require transaction promotion_blockers.")

    if taint_open and support_effect in PROMOTION_EFFECTS:
        errors.append(f"{relative}: propagated taint without declassification cannot be eligible for bounded evidence review.")

    if risk_tier in {"high", "critical"} and adequacy_state in INADEQUATE_ADEQUACY_STATES and not required_escalation:
        errors.append(f"{relative}: high/critical inadequate context requires required_escalation.")

    if risk_tier in {"high", "critical"} and support_effect in PROMOTION_EFFECTS:
        if verification_mode in WEAK_VERIFICATION_MODES:
            errors.append(f"{relative}: high/critical support cannot rely on weak verification mode {verification_mode!r}.")
        if not adequacy.get("verification_artifact_refs"):
            errors.append(f"{relative}: high/critical eligible support requires verification_artifact_refs.")

    claim_scope = str(adequacy.get("claim_scope", "")).lower()
    if contains_any([claim_scope], {"empirical", "benchmark", "deployment", "runtime", "model-quality"}) and verification_mode in WEAK_VERIFICATION_MODES | {"proof_checker"}:
        if support_effect in PROMOTION_EFFECTS or adequacy_state in EVIDENCE_READY_ADEQUACY_STATES:
            errors.append(f"{relative}: weak or formal-only verification mode cannot make empirical/deployment claims evidence-ready.")

    return errors


def fixture_expectation(path: Path) -> bool | None:
    if path.name.startswith("valid_"):
        return True
    if path.name.startswith("invalid_"):
        return False
    return None


def main() -> None:
    schemas = load_schemas()
    fixtures = sorted(FIXTURE_DIR.glob("*.json"))
    if not fixtures:
        raise SystemExit(f"No context admission/adequacy fixtures found in {FIXTURE_DIR.relative_to(ROOT)}.")

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
                errors.append(f"{relative}: invalid fixture unexpectedly passed context admission/adequacy checks.")

    if errors:
        print("Context admission/adequacy harness failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print(
        "Context admission/adequacy harness passed: "
        f"{valid_count} valid fixture(s), {invalid_count} expected-invalid fixture(s)."
    )


if __name__ == "__main__":
    main()
