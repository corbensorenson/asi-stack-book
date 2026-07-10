#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from typing import Any

from validate_protocol_examples import validate_value

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "authority_tuple_lifecycle_record.schema.json"
VALID = ROOT / "tests" / "fixtures" / "protocol_records" / "authority_tuple_lifecycle_record.valid.json"
MUTATIONS = ROOT / "experiments" / "authority_tuple_lifecycle" / "fixtures"
EXPECTED_SOURCES = {
    "cca_project", "moecot_manifest_project", "beastbrain_project",
    "bugbrain_project", "corbens_trainer_project", "corbens_best_model_possible_project",
}
IDENTITY_FIELDS = {
    "principal_id", "execution_domain_id", "operation", "target_ref", "permission_class",
    "scope", "budget_account_id", "trace_id", "replay_identity", "grant_id",
    "policy_version", "revocation_epoch", "expires_at",
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def replay_identity(authority: dict[str, Any]) -> str:
    trace = str(authority.get("trace_id", "")).split("://")[-1]
    grant = str(authority.get("grant_id", "")).split("://")[-1]
    return f"replay://{trace}@{grant}@epoch-{authority.get('revocation_epoch')}"


def semantic_errors(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if set(record.get("source_ids", [])) != EXPECTED_SOURCES:
        errors.append("authority tuple lineage must name the six historical-project sources exactly")
    authority = record.get("authority_tuple", {})
    missing = sorted(IDENTITY_FIELDS - set(authority))
    if missing:
        errors.append("authority tuple is missing unified identity fields")
    ownership = record.get("domain_ownership", {})
    if ownership.get("execution_domain_id") != authority.get("execution_domain_id"):
        errors.append("execution-domain ownership must bind the authority tuple domain")
    delegation = record.get("delegation", {})
    if delegation.get("parent_grant_id") != authority.get("grant_id"):
        errors.append("delegation must bind the parent grant")
    if not set(delegation.get("delegated_scope", [])).issubset(set(authority.get("scope", []))):
        errors.append("delegation cannot widen the authority scope")
    if delegation.get("delegated_budget_account_id") != authority.get("budget_account_id"):
        errors.append("delegation cannot swap the budget account identity")
    if delegation.get("delegated_trace_id") != authority.get("trace_id"):
        errors.append("delegation cannot fork the authority trace identity")
    if delegation.get("delegated_revocation_epoch") != authority.get("revocation_epoch"):
        errors.append("delegation must inherit the active revocation epoch")
    if authority.get("replay_identity") != replay_identity(authority):
        errors.append("replay identity must bind trace, grant, and revocation epoch")
    for event in record.get("lifecycle_events", []):
        if event.get("execution_domain_id") != authority.get("execution_domain_id"):
            errors.append("lifecycle event crossed an unbound execution domain")
        if event.get("grant_id") != authority.get("grant_id") or event.get("trace_id") != authority.get("trace_id"):
            errors.append("lifecycle event must preserve grant and trace identity")
        if event.get("revocation_epoch") != authority.get("revocation_epoch"):
            errors.append("lifecycle event must preserve revocation identity")
        if event.get("state") in {"revoked", "expired", "denied"} and event.get("effect_permitted") is True:
            errors.append("revoked, expired, or denied authority cannot permit an effect")
    handoff = record.get("cross_domain_handoff", {})
    if handoff.get("source_domain_id") != authority.get("execution_domain_id"):
        errors.append("cross-domain handoff must originate in the bound execution domain")
    if handoff.get("decision") == "allow" and not handoff.get("target_owner_approval_ref"):
        errors.append("cross-domain allow requires target-domain owner approval")
    security = record.get("security_boundary", {})
    if security.get("hardware_root_claim_allowed") is True and (
        security.get("hardware_root_state") != "attested" or not security.get("hardware_root_evidence_refs")
    ):
        errors.append("protocol security controls cannot be promoted into a hardware-root claim")
    decision = record.get("decision", {})
    if decision.get("outcome") == "allow" and not decision.get("effect_receipt_ref"):
        errors.append("allowed authority use requires an effect receipt")
    if decision.get("support_state_effect") == "eligible_for_bounded_evidence_review":
        errors.append("fixture-only authority lifecycle cannot promote support")
    if not record.get("promotion_blockers") or not record.get("non_claims"):
        errors.append("authority tuple lifecycle must preserve blockers and non-claims")
    return errors


def apply_mutation(base: dict[str, Any], mutation: dict[str, Any]) -> dict[str, Any]:
    value = deepcopy(base)
    target: Any = value
    for segment in mutation["path"][:-1]:
        target = target[segment]
    leaf = mutation["path"][-1]
    if mutation["operation"] == "set":
        target[leaf] = mutation["value"]
    elif mutation["operation"] == "merge":
        target[leaf].update(mutation["value"])
    elif mutation["operation"] == "delete":
        del target[leaf]
    else:
        raise ValueError(f"unsupported mutation operation {mutation['operation']!r}")
    return value


def main() -> None:
    schema = load(SCHEMA)
    valid = load(VALID)
    errors = validate_value(valid, schema, str(VALID.relative_to(ROOT))) + semantic_errors(valid)
    if errors:
        raise SystemExit("Valid authority tuple lifecycle failed:\n - " + "\n - ".join(errors))
    mutations = sorted(MUTATIONS.glob("invalid_*.json"))
    if not mutations:
        raise SystemExit("No expected-invalid authority tuple mutations found.")
    for path in mutations:
        mutation = load(path)
        candidate = apply_mutation(valid, mutation)
        found = validate_value(candidate, schema, str(path.relative_to(ROOT))) + semantic_errors(candidate)
        if not any(mutation["expected_error"] in error for error in found):
            raise SystemExit(f"{path.relative_to(ROOT)} did not produce expected error {mutation['expected_error']!r}: {found}")
    print(f"Authority tuple lifecycle harness passed: 1 blocked six-project lineage record and {len(mutations)} expected-invalid mutations.")


if __name__ == "__main__":
    main()
