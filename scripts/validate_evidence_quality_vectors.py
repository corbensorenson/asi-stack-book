#!/usr/bin/env python3
"""Validate evidence-quality vector coverage, vocabularies, and no-aggregation rules."""

from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
from typing import Any

from build_canonical_public_status import validate_against_schema
from build_evidence_quality_vectors import DISPOSITIONS, OUTPUT, POLICY, ROOT, build_registry


SCHEMA = ROOT / "schemas" / "evidence_quality_vector_registry.schema.json"


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def semantic_errors(registry: dict[str, Any], expected: dict[str, Any], policy: dict[str, Any]) -> list[str]:
    errors = validate_against_schema(registry, load(SCHEMA), "evidence_quality_vectors")
    if registry != expected:
        errors.append("tracked evidence-quality vectors differ from generated claim dispositions")
    dimensions = policy["dimension_order"]
    vocab = {row["id"]: set(row["states"]) for row in policy["dimensions"]}
    dispositions = {row["claim_id"]: row for row in load(DISPOSITIONS)["dispositions"]}
    seen: set[str] = set()
    for vector in registry.get("vectors", []):
        claim_id = vector.get("claim_id")
        if claim_id in seen:
            errors.append(f"duplicate vector claim: {claim_id}")
        seen.add(claim_id)
        if claim_id not in dispositions:
            errors.append(f"vector has unknown claim: {claim_id}")
            continue
        if vector.get("summary_support_state") != dispositions[claim_id]["current_support_state"]:
            errors.append(f"{claim_id}: vector summary differs from authoritative disposition")
        if list(vector.get("dimensions", {}).keys()) != dimensions:
            errors.append(f"{claim_id}: dimension order or coverage differs from policy")
        for dimension_id in dimensions:
            record = vector.get("dimensions", {}).get(dimension_id, {})
            if record.get("state") not in vocab[dimension_id]:
                errors.append(f"{claim_id}: invalid {dimension_id} state {record.get('state')!r}")
            for field in ("rationale", "evidence_refs", "residuals"):
                if not record.get(field):
                    errors.append(f"{claim_id}: {dimension_id} missing {field}")
        aggregation = vector.get("aggregation", {})
        if aggregation.get("scalar_score") != "prohibited" or aggregation.get("automatic_support_state_derivation") != "prohibited":
            errors.append(f"{claim_id}: vector attempts scalar or automatic support aggregation")
        if vector.get("support_state_effect") != "none":
            errors.append(f"{claim_id}: vector must not change support state")
    if seen != set(dispositions):
        errors.append(f"vector claim coverage differs from dispositions: {len(seen)} versus {len(dispositions)}")
    if registry.get("summary", {}).get("numeric_aggregate_count") != 0:
        errors.append("registry claims a numeric evidence-quality aggregate")
    return errors


def negative_controls(registry: dict[str, Any], expected: dict[str, Any], policy: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    mutations: list[tuple[str, dict[str, Any]]] = []
    missing = copy.deepcopy(registry)
    del missing["vectors"][0]["dimensions"][policy["dimension_order"][0]]
    mutations.append(("missing dimension", missing))
    scalar = copy.deepcopy(registry)
    scalar["vectors"][0]["aggregation"]["scalar_score"] = 0.82
    mutations.append(("numeric scalar", scalar))
    promoted = copy.deepcopy(registry)
    promoted["vectors"][0]["summary_support_state"] = "empirical-test-backed"
    mutations.append(("support mismatch", promoted))
    effect = copy.deepcopy(registry)
    effect["vectors"][0]["support_state_effect"] = "eligible_for_bounded_evidence_review"
    mutations.append(("automatic promotion effect", effect))
    for label, mutation in mutations:
        if not semantic_errors(mutation, expected, policy):
            failures.append(f"negative control was incorrectly accepted: {label}")
    return failures


def main() -> None:
    registry = load(OUTPUT)
    policy = load(POLICY)
    expected = build_registry()
    errors = semantic_errors(registry, expected, policy)
    errors.extend(negative_controls(registry, expected, policy))
    if errors:
        print("Evidence-quality vector validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)
    print("Evidence-quality vector validation passed: 54 claims, 8 dimensions each, no scalar aggregation, and 4 rejecting negative controls.")


if __name__ == "__main__":
    main()
