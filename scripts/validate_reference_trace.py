#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

from validate_protocol_examples import validate_value


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "experiments" / "reference_trace" / "fixtures"
SCHEMA = ROOT / "schemas" / "reference_trace_record.schema.json"

REQUIRED_TRACE_TERMS = {
    "intent",
    "plan",
    "context",
    "route",
    "verification",
    "execution",
    "evidence",
    "scf",
}
NON_PROMOTING_SUPPORT_EFFECTS = {"record_shape_only", "argument_only", "blocks_promotion"}
PROMOTION_TERMS = {"promoted", "promotion", "prototype-backed", "synthetic-test-backed", "empirical-test-backed"}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def nonempty_list(value: Any) -> bool:
    return isinstance(value, list) and bool(value)


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


def require_nonempty_record_list(record: dict[str, Any], field: str, errors: list[str], relative: str) -> list[Any]:
    value = record.get(field)
    if not nonempty_list(value):
        errors.append(f"{relative}: reference_trace_record.{field} must be a non-empty list.")
        return []
    return value


def schema_errors_for_scenario(value: dict[str, Any], schema: dict[str, Any], relative: str) -> list[str]:
    record = value.get("reference_trace_record")
    if not isinstance(record, dict):
        return [f"{relative}: missing reference_trace_record object."]
    return validate_value(record, schema, f"{relative}:reference_trace_record")


def semantic_errors(value: dict[str, Any], relative: str) -> list[str]:
    errors: list[str] = []
    if not isinstance(value.get("scenario_id"), str) or not value["scenario_id"].strip():
        errors.append(f"{relative}: scenario_id must be a non-empty string.")
    top_non_claims = value.get("non_claims")
    if not nonempty_list(top_non_claims):
        errors.append(f"{relative}: non_claims must be a non-empty list.")
    if errors:
        return errors

    record = value["reference_trace_record"]
    parent_artifacts = require_nonempty_record_list(record, "parent_artifact_refs", errors, relative)
    authority_chain = require_nonempty_record_list(record, "authority_chain", errors, relative)
    authority_deltas = require_nonempty_record_list(record, "authority_deltas", errors, relative)
    layer_handoffs = require_nonempty_record_list(record, "layer_handoffs", errors, relative)
    artifacts = require_nonempty_record_list(record, "artifacts", errors, relative)
    evidence_deltas = require_nonempty_record_list(record, "evidence_deltas", errors, relative)
    residual_deltas = require_nonempty_record_list(record, "residual_deltas", errors, relative)
    validation_commands = require_nonempty_record_list(record, "validation_commands", errors, relative)
    source_refs = require_nonempty_record_list(record, "source_refs", errors, relative)
    if errors:
        return errors

    support_effect = str(record["support_state_effect"])
    if support_effect not in NON_PROMOTING_SUPPORT_EFFECTS:
        errors.append(f"{relative}: support_state_effect must remain non-promoting for this harness.")

    trace_text = text_blob(parent_artifacts, authority_chain, authority_deltas, layer_handoffs, artifacts)
    missing_terms = sorted(term for term in REQUIRED_TRACE_TERMS if term not in trace_text)
    if missing_terms:
        errors.append(f"{relative}: integrated trace is missing required layer term(s): {', '.join(missing_terms)}.")

    if len(artifacts) < 6:
        errors.append(f"{relative}: integrated trace must carry at least six artifact refs.")

    if not any(str(command) == "python3 scripts/validate_reference_trace.py" for command in validation_commands):
        errors.append(f"{relative}: validation_commands must include python3 scripts/validate_reference_trace.py.")

    if not any(str(source).startswith("sources/source_notes/") for source in source_refs):
        errors.append(f"{relative}: source_refs must include source-note refs.")

    if str(record["trace_state"]) == "blocked" or support_effect == "blocks_promotion":
        if not nonempty_list(record.get("stop_conditions")):
            errors.append(f"{relative}: blocked traces must record stop_conditions.")
        if not nonempty_list(record.get("promotion_blockers")):
            errors.append(f"{relative}: blocked traces must record promotion_blockers.")
        blocker_text = text_blob(record.get("stop_conditions", []), record.get("promotion_blockers", []))
        if not any(term in blocker_text for term in ("authority", "verification", "residual", "contract", "governance")):
            errors.append(f"{relative}: blocked traces must name a concrete authority, verification, residual, contract, or governance blocker.")

    evidence_text = text_blob(record.get("evidence_updates", []), evidence_deltas)
    if any(term in evidence_text for term in PROMOTION_TERMS) and support_effect != "blocks_promotion":
        errors.append(f"{relative}: promotion-language evidence updates require blocks_promotion support_state_effect.")

    residual_text = text_blob(residual_deltas)
    if "none" in residual_text or "cleared all" in residual_text:
        errors.append(f"{relative}: residual_deltas must not erase residuals in this fixture harness.")

    non_claim_text = text_blob(top_non_claims, record.get("non_claims", []))
    if "does not promote" not in non_claim_text or "support" not in non_claim_text:
        errors.append(f"{relative}: non_claims must state support-state non-promotion.")
    if "does not prove" not in non_claim_text:
        errors.append(f"{relative}: non_claims must deny stronger proof.")
    if "runtime" not in non_claim_text and "deployed" not in non_claim_text:
        errors.append(f"{relative}: non_claims must deny runtime or deployed-system claims.")

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
        raise SystemExit(f"No reference trace fixtures found in {FIXTURE_DIR.relative_to(ROOT)}.")

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

        fixture_errors = schema_errors_for_scenario(value, schema, relative)
        if not fixture_errors:
            fixture_errors.extend(semantic_errors(value, relative))

        if expect_valid:
            valid_count += 1
            errors.extend(fixture_errors)
        else:
            invalid_count += 1
            if not fixture_errors:
                errors.append(f"{relative}: expected invalid fixture passed validation.")

    if errors:
        print("Reference trace harness failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print(
        "Reference trace harness passed: "
        f"{valid_count} valid fixture(s), {invalid_count} expected-invalid fixture(s)."
    )


if __name__ == "__main__":
    main()
