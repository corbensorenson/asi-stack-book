#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
from datetime import datetime
import json
from pathlib import Path
from typing import Any

from validate_protocol_examples import validate_value

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "readiness_check_lifecycle_record.schema.json"
VALID = ROOT / "tests" / "fixtures" / "protocol_records" / "readiness_check_lifecycle_record.valid.json"
MUTATIONS = ROOT / "experiments" / "readiness_check_lifecycle" / "fixtures"
EXPECTED_SOURCES = {
    "cca_project", "moecot_manifest_project", "beastbrain_project",
    "bugbrain_project", "corbens_trainer_project", "corbens_best_model_possible_project",
}
CONTAINMENT_RANK = {"open": 0, "limited": 1, "quarantined": 2, "retired": 3}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def instant(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def semantic_errors(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if set(record.get("source_ids", [])) != EXPECTED_SOURCES:
        errors.append("readiness check lineage must name the six historical-project sources exactly")
    gate = record.get("gate_identity", {})
    evaluated = instant(gate.get("evaluated_at"))
    gate_expiry = instant(gate.get("expires_at"))
    if evaluated and gate_expiry and gate_expiry <= evaluated:
        errors.append("readiness gate must expire after its evaluation time")

    ready = record.get("decision", {}).get("state") == "ready"
    for check in record.get("checks", []):
        applicability = check.get("applicability")
        required = check.get("required")
        attempt = check.get("attempt")
        result = check.get("result")
        if applicability == "not_applicable":
            if required or attempt != "not_attempted" or result != "not_applicable":
                errors.append("not-applicable checks must be optional, unattempted, and explicitly not applicable")
        if applicability == "unknown" and result == "pass":
            errors.append("unknown applicability cannot be recorded as pass")
        if applicability == "unknown" and ready:
            errors.append("unknown applicability cannot be treated as ready")
        if applicability == "applicable" and required and ready:
            if attempt != "attempted" or result != "pass":
                errors.append("every applicable required check must be attempted and pass before readiness")
        if applicability == "applicable" and required and result == "pass" and check.get("waiver_ref"):
            errors.append("a waiver cannot substitute for a passing required check")
        if result == "pass":
            if attempt != "attempted":
                errors.append("skipped or unattempted checks cannot be recorded as passed")
            if not check.get("evidence_refs") or not check.get("observed_at") or not check.get("expires_at"):
                errors.append("passing checks require evidence identity, observation time, and expiry")
            expiry = instant(check.get("expires_at"))
            if ready and evaluated and expiry and expiry <= evaluated:
                errors.append("expired check evidence cannot support readiness")

    dependencies = record.get("stale_dependencies", [])
    invalidating = [row for row in dependencies if row.get("state") in {"stale", "quarantined", "revoked", "unknown"} and row.get("invalidates_promotion")]
    if ready and invalidating:
        errors.append("stale or quarantined dependencies must invalidate promotion")

    containment = record.get("containment", {})
    previous_state = containment.get("previous_state")
    next_state = containment.get("next_state")
    if previous_state in CONTAINMENT_RANK and next_state in CONTAINMENT_RANK:
        if invalidating and CONTAINMENT_RANK[next_state] < CONTAINMENT_RANK[previous_state]:
            errors.append("containment cannot weaken while an invalidating dependency remains")
    previous_routes = set(containment.get("previous_allowed_routes", []))
    next_routes = set(containment.get("next_allowed_routes", []))
    if invalidating and not next_routes.issubset(previous_routes):
        errors.append("containment cannot add routes while an invalidating dependency remains")

    quarantine = record.get("quarantine", {})
    if quarantine.get("active"):
        if not quarantine.get("reason_refs") or not quarantine.get("owner_ref") or not quarantine.get("affected_descendant_refs") or not quarantine.get("disposition_ref"):
            errors.append("active quarantine requires reasons, owner, affected descendants, and disposition")
        if record.get("decision", {}).get("ordinary_routing_allowed"):
            errors.append("active quarantine cannot allow ordinary routing")
        if record.get("decision", {}).get("state") != "quarantined":
            errors.append("active quarantine must produce a quarantined decision state")
    decision = record.get("decision", {})
    if decision.get("support_state_effect") == "eligible_for_bounded_evidence_review":
        errors.append("fixture-only readiness checks cannot promote support")
    if not record.get("promotion_blockers") or not record.get("non_claims"):
        errors.append("readiness check lifecycle must preserve blockers and non-claims")
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
        raise SystemExit("Valid readiness check lifecycle failed:\n - " + "\n - ".join(errors))
    mutations = sorted(MUTATIONS.glob("invalid_*.json"))
    if not mutations:
        raise SystemExit("No readiness check lifecycle mutations found.")
    for path in mutations:
        mutation = load(path)
        candidate = apply_mutation(valid, mutation)
        found = validate_value(candidate, schema, str(path.relative_to(ROOT))) + semantic_errors(candidate)
        if not any(mutation["expected_error"] in error for error in found):
            raise SystemExit(f"{path.relative_to(ROOT)} did not produce {mutation['expected_error']!r}: {found}")
    print(
        "Readiness check lifecycle harness passed: 1 quarantined six-project record and "
        f"{len(mutations)} expected-invalid mutations."
    )


if __name__ == "__main__":
    main()
