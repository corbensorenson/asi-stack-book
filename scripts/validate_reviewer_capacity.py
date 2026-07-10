#!/usr/bin/env python3
"""Validate reviewer competence, independence, load, fallback, and quality records."""

from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
from typing import Any

from build_canonical_public_status import validate_against_schema


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "governance" / "reviewer_capacity_registry.json"
SCHEMA = ROOT / "schemas" / "reviewer_capacity_registry.schema.json"
REQUIRED_ROLES = {"program_owner", "formal_methods_reviewer", "safety_governance_reviewer", "systems_editorial_reviewer"}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def semantic_errors(registry: dict[str, Any]) -> list[str]:
    errors = validate_against_schema(registry, load(SCHEMA), "reviewer_capacity_registry")
    records = registry.get("records", [])
    by_role = {row.get("role_id"): row for row in records}
    if set(by_role) != REQUIRED_ROLES or len(records) != len(REQUIRED_ROLES):
        errors.append(f"reviewer role set must be exactly {sorted(REQUIRED_ROLES)}")
    for role_id, row in by_role.items():
        assigned = row.get("assignment_state", "").startswith("assigned_")
        if assigned != bool(row.get("principal_ref")):
            errors.append(f"{role_id}: assignment state and principal_ref disagree")
        for section in ("competence", "independence", "conflicts", "load", "response", "escalation_substitute", "review_quality"):
            if not isinstance(row.get(section), dict) or not row[section]:
                errors.append(f"{role_id}: missing {section} record")
        load_record = row.get("load", {})
        if load_record.get("within_limit") == "yes" and load_record.get("measurement_state") not in {"measured", "continuously_measured"}:
            errors.append(f"{role_id}: cannot claim capacity without measured load")
        quality = row.get("review_quality", {})
        if quality.get("measurement_state") == "measured" and (
            quality.get("sample_count", 0) <= 0 or quality.get("method") in {"", "none"}
        ):
            errors.append(f"{role_id}: measured review quality lacks samples or method")
        independence = row.get("independence", {})
        if independence.get("class") == "independent_external" and row.get("conflicts", {}).get("items"):
            errors.append(f"{role_id}: independent_external claim conflicts with disclosed conflicts")
        substitute = row.get("escalation_substitute", {}).get("role_id")
        if substitute not in REQUIRED_ROLES or substitute == role_id:
            errors.append(f"{role_id}: invalid escalation substitute {substitute!r}")
        if row.get("support_state_effect") != "none":
            errors.append(f"{role_id}: capacity record must not promote support")
    for role_id in REQUIRED_ROLES - {"program_owner"}:
        if by_role.get(role_id, {}).get("assignment_state") != "deferred_postpublication":
            errors.append(f"{role_id}: author policy requires deferred_postpublication until completion")
    return errors


def negative_controls(registry: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    mutations: list[tuple[str, dict[str, Any]]] = []
    assigned = copy.deepcopy(registry)
    assigned["records"][1]["assignment_state"] = "assigned_external"
    mutations.append(("assigned without principal", assigned))
    capacity = copy.deepcopy(registry)
    capacity["records"][0]["load"]["within_limit"] = "yes"
    mutations.append(("unmeasured capacity claim", capacity))
    measured = copy.deepcopy(registry)
    measured["records"][0]["review_quality"]["measurement_state"] = "measured"
    mutations.append(("quality claim without sample", measured))
    missing_substitute = copy.deepcopy(registry)
    missing_substitute["records"][0]["escalation_substitute"]["role_id"] = ""
    mutations.append(("missing escalation substitute", missing_substitute))
    for label, mutation in mutations:
        if not semantic_errors(mutation):
            failures.append(f"negative control was incorrectly accepted: {label}")
    return failures


def main() -> None:
    registry = load(REGISTRY)
    errors = semantic_errors(registry)
    errors.extend(negative_controls(registry))
    if errors:
        print("Reviewer-capacity validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)
    print("Reviewer-capacity validation passed: 4 roles, 3 external roles deferred until post-publication, and 4 rejecting negative controls.")


if __name__ == "__main__":
    main()
