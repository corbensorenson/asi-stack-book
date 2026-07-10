#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import sys
from typing import Any

from validate_protocol_examples import validate_value

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "artifact_projection_revocation_record.schema.json"
VALID_PATH = ROOT / "tests" / "fixtures" / "protocol_records" / "artifact_projection_revocation_record.valid.json"
MUTATION_DIR = ROOT / "experiments" / "artifact_projection_revocation" / "fixtures"


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def semantic_errors(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    canonical = record.get("canonical_artifact", {})
    canonical_id = canonical.get("artifact_id")
    canonical_digest = canonical.get("content_digest")
    projection_ids: set[str] = set()
    for projection in record.get("projections", []):
        projection_ids.add(str(projection.get("projection_id")))
        if projection.get("source_artifact_id") != canonical_id:
            errors.append("projection source artifact must match the canonical artifact id")
        if projection.get("source_digest") != canonical_digest:
            errors.append("projection source digest must match the canonical artifact digest")

    dependency_downstreams = {str(row.get("downstream_id")) for row in record.get("dependencies", [])}
    quarantine = record.get("quarantine_event", {})
    if quarantine.get("upstream_id") != canonical_id:
        errors.append("quarantine upstream must identify the canonical artifact")
    required = {str(value) for value in quarantine.get("required_downstream_ids", [])}
    invalidated = {str(value) for value in quarantine.get("invalidated_downstream_ids", [])}
    alternates = {str(value) for value in quarantine.get("alternate_derivation_ids", [])}
    unresolved = {str(value) for value in quarantine.get("unresolved_ids", [])}
    if not required.issubset(dependency_downstreams | projection_ids):
        errors.append("quarantine closure names a downstream id absent from dependencies")
    if not required.issubset(invalidated | alternates | unresolved):
        errors.append("quarantine event does not close over required downstream ids")
    if unresolved and record.get("support_state_effect") == "eligible_for_bounded_evidence_review":
        errors.append("unresolved quarantine closure blocks bounded evidence review")

    replay = record.get("replay_classification", {})
    grade = replay.get("grade")
    if grade in {"deterministic_reexecution", "partial_reexecution"}:
        for field in ("environment_ref", "observed_output_ref", "comparison_or_semantic_validator_ref"):
            if not replay.get(field):
                errors.append(f"deterministic re-execution requires {field}")
    if grade == "semantic_replay" and not replay.get("comparison_or_semantic_validator_ref"):
        errors.append("semantic replay requires a semantic validator reference")

    completion = record.get("async_completion", {})
    if completion.get("terminal_state") in {"completed", "failed", "cancelled"} and not completion.get("terminal_receipt_ref"):
        errors.append("terminal asynchronous state requires a terminal receipt")

    relocation = record.get("relocation_identity", {})
    if relocation.get("identity_authority") == "path":
        errors.append("relocation-safe identity cannot use path as authority")
    if relocation.get("content_digest") != canonical_digest:
        errors.append("relocation digest must match the canonical artifact digest")
    if relocation.get("digest_verified") is not True:
        errors.append("relocation-safe identity requires digest verification")

    eligible = record.get("support_state_effect") == "eligible_for_bounded_evidence_review"
    if eligible and (
        grade not in {"deterministic_reexecution", "semantic_replay"}
        or completion.get("terminal_state") == "unknown"
        or record.get("promotion_blockers")
    ):
        errors.append("playback, unresolved async completion, or open blockers cannot be eligible for bounded evidence review")
    if not record.get("promotion_blockers") or not record.get("non_claims"):
        errors.append("artifact projection/revocation record must preserve blockers and non-claims")
    return errors


def apply_mutation(base: dict[str, Any], mutation: dict[str, Any]) -> dict[str, Any]:
    value = deepcopy(base)
    target: Any = value
    path = mutation["path"]
    for segment in path[:-1]:
        target = target[segment]
    leaf = path[-1]
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
    schema = load(SCHEMA_PATH)
    valid = load(VALID_PATH)
    errors = validate_value(valid, schema, str(VALID_PATH.relative_to(ROOT)))
    errors.extend(semantic_errors(valid))
    if errors:
        print("Artifact projection/revocation valid fixture failed:")
        for error in errors:
            print(f" - {error}")
        raise SystemExit(1)

    mutations = sorted(MUTATION_DIR.glob("invalid_*.json"))
    if not mutations:
        raise SystemExit("No expected-invalid artifact projection/revocation mutations found.")
    for path in mutations:
        mutation = load(path)
        candidate = apply_mutation(valid, mutation)
        candidate_errors = validate_value(candidate, schema, str(path.relative_to(ROOT)))
        candidate_errors.extend(semantic_errors(candidate))
        expected = mutation["expected_error"]
        if not any(expected in error for error in candidate_errors):
            print(f"{path.relative_to(ROOT)} did not produce expected error: {expected}")
            for error in candidate_errors:
                print(f" - {error}")
            raise SystemExit(1)

    print(f"Artifact projection/revocation harness passed: 1 valid blocked record and {len(mutations)} expected-invalid mutations.")


if __name__ == "__main__":
    main()
