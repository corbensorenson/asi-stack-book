#!/usr/bin/env python3
"""Validate synthetic proof-carrying-claim fixtures."""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

from validate_protocol_examples import validate_value


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "experiments" / "proof_carrying_claims" / "fixtures"
SCHEMA = ROOT / "schemas" / "proof_carrying_claim.schema.json"

NEGATIVE_RESULTS = {"fail", "timeout", "mismatch"}
NON_PROMOTIONAL_EFFECTS = {"no_change", "downgrade", "block", "escalate"}
POSITIVE_ARTIFACT_STATES = {"passed", "narrow_pass"}
POSITIVE_ADEQUACY = {"adequate", "narrow"}


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


def semantic_errors(record: dict[str, Any], relative: str) -> list[str]:
    errors: list[str] = []
    verifier_result = str(record.get("verifier_result", ""))
    claim_effect = str(record.get("claim_validity_effect", ""))
    support_effect = str(record.get("support_state_effect", ""))
    artifact_state = str(record.get("artifact_validity_state", ""))
    semantic_adequacy = str(record.get("semantic_adequacy", ""))
    required_tier = str(record.get("required_tier", ""))
    justification_type = str(record.get("justification_type", ""))
    interpretation_confidence = str(record.get("interpretation_confidence", ""))

    if required_tier == "formal" and justification_type != "formal_proof":
        errors.append(f"{relative}: formal required_tier must use formal_proof justification_type.")
    if required_tier == "citation" and justification_type not in {"citation_dossier", "tribunal_review"}:
        errors.append(f"{relative}: citation required_tier must use citation_dossier or tribunal_review justification.")
    if required_tier == "procedure" and justification_type not in {"procedure_log", "schema_fixture"}:
        errors.append(f"{relative}: procedure required_tier must use procedure_log or schema_fixture justification.")

    if verifier_result == "pass":
        if not nonempty_list(record, "verifier_artifact_refs"):
            errors.append(f"{relative}: passed verifier_result requires verifier_artifact_refs.")
        if artifact_state not in POSITIVE_ARTIFACT_STATES:
            errors.append(f"{relative}: passed verifier_result requires passed or narrow_pass artifact_validity_state.")
        if semantic_adequacy not in POSITIVE_ADEQUACY:
            errors.append(f"{relative}: passed verifier_result requires adequate or narrow semantic_adequacy.")
    if verifier_result in NEGATIVE_RESULTS:
        if claim_effect not in NON_PROMOTIONAL_EFFECTS:
            errors.append(f"{relative}: negative verifier_result must not promote within scope.")
        if support_effect not in {"argument_only", "blocks_promotion", "record_shape_only"}:
            errors.append(f"{relative}: negative verifier_result must keep support_state_effect non-promotional.")
        if not nonempty_list(record, "failed_attempt_refs"):
            errors.append(f"{relative}: negative verifier_result requires failed_attempt_refs.")
        ledger_text = str(record.get("ledger_update", "")).lower()
        if not any(term in ledger_text for term in ("block", "downgrade", "no support", "no promotion", "escalat")):
            errors.append(f"{relative}: negative verifier_result must record a blocking, downgrade, no-promotion, or escalation ledger_update.")

    if claim_effect == "promote_within_scope":
        if verifier_result != "pass":
            errors.append(f"{relative}: promote_within_scope requires passed verifier_result.")
        if support_effect != "eligible_for_bounded_evidence_review":
            errors.append(f"{relative}: promote_within_scope requires eligible_for_bounded_evidence_review support_state_effect.")
        if semantic_adequacy not in POSITIVE_ADEQUACY:
            errors.append(f"{relative}: promote_within_scope requires adequate or narrow semantic_adequacy.")
        if not nonempty_list(record, "consumer_requirements"):
            errors.append(f"{relative}: promote_within_scope requires consumer_requirements.")
        if not nonempty_list(record, "limitations"):
            errors.append(f"{relative}: promote_within_scope requires limitations.")

    if interpretation_confidence == "mismatch":
        if verifier_result != "mismatch" and semantic_adequacy != "inadequate":
            errors.append(f"{relative}: interpretation_confidence mismatch must be paired with verifier mismatch or inadequate semantic adequacy.")
        if claim_effect == "promote_within_scope":
            errors.append(f"{relative}: interpretation mismatch cannot promote within scope.")

    scope_text = as_text([record.get("formal_scope", ""), record.get("limitations", []), record.get("non_claims", [])]).lower()
    if "arbitrary" in scope_text and claim_effect == "promote_within_scope":
        errors.append(f"{relative}: promote_within_scope cannot be paired with arbitrary-scope language.")

    non_claim_text = as_text(record.get("non_claims", [])).lower()
    if "does not" not in non_claim_text:
        errors.append(f"{relative}: non_claims must contain explicit does-not boundaries.")
    for term in ("semantic", "verifier", "runtime", "support"):
        if term not in non_claim_text:
            errors.append(f"{relative}: non_claims must mention {term} boundary.")

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
        raise SystemExit(f"No proof-carrying-claim fixtures found in {rel(FIXTURE_DIR)}.")

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
        print("Proof-carrying claim harness failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print(
        "Proof-carrying claim harness passed: "
        f"{valid_count} valid fixture(s), {invalid_count} expected-invalid fixture(s)."
    )


if __name__ == "__main__":
    main()
