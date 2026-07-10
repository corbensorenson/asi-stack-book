#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
from datetime import datetime
import json
from pathlib import Path
from typing import Any

from validate_protocol_examples import validate_value

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "supply_chain_affected_path_record.schema.json"
VALID = ROOT / "tests" / "fixtures" / "protocol_records" / "supply_chain_affected_path_record.valid.json"
MUTATIONS = ROOT / "experiments" / "supply_chain_affected_paths" / "fixtures"
EXPECTED_SOURCES = {"cca_project", "moecot_manifest_project", "corbens_trainer_project"}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def instant(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def reachable(subject: str, edges: list[dict[str, Any]]) -> set[str]:
    adjacency: dict[str, set[str]] = {}
    for edge in edges:
        adjacency.setdefault(edge.get("from_node", ""), set()).add(edge.get("to_node", ""))
    closure = {subject}
    frontier = [subject]
    while frontier:
        node = frontier.pop()
        for descendant in adjacency.get(node, set()):
            if descendant not in closure:
                closure.add(descendant)
                frontier.append(descendant)
    return closure


def semantic_errors(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if set(record.get("source_ids", [])) != EXPECTED_SOURCES:
        errors.append("supply-chain lineage must name the three historical-project sources exactly")

    nodes = record.get("nodes", [])
    node_ids = [row.get("node_id") for row in nodes]
    if len(node_ids) != len(set(node_ids)):
        errors.append("supply-chain node identities must be unique")
    node_map = {row.get("node_id"): row for row in nodes}
    requested = record.get("requested_artifact", {})
    requested_node = node_map.get(requested.get("node_id"))
    if not requested_node or requested_node.get("digest") != requested.get("digest") or requested_node.get("declared_name") != requested.get("declared_name"):
        errors.append("requested artifact name and digest must bind to one graph node")

    for edge in record.get("edges", []):
        if edge.get("from_node") not in node_map or edge.get("to_node") not in node_map:
            errors.append("every supply-chain edge must bind two declared nodes")
    for reference in record.get("assurance_references", []):
        if reference.get("subject_node") not in node_map:
            errors.append("every assurance reference must bind a declared node")
        if instant(reference["expires_at"]) <= instant(reference["observed_at"]):
            errors.append("assurance references must expire after observation")
        if not reference.get("limitations"):
            errors.append("assurance references must preserve bounded limitations")

    event = record.get("invalidation_event", {})
    if event.get("event_id") == event.get("prior_event_ref"):
        errors.append("invalidation must append a distinct event rather than overwrite history")
    subject = event.get("subject_node")
    if subject not in node_map:
        errors.append("invalidation subject must bind a declared node")
    expected_closure = reachable(subject, record.get("edges", [])) if subject in node_map else set()
    declared_closure = set(record.get("declared_affected_closure", []))
    if declared_closure != expected_closure:
        errors.append("declared affected closure must equal the full reachable downstream path")

    routes = record.get("response_routes", [])
    route_ids = [row.get("node_id") for row in routes]
    if len(route_ids) != len(set(route_ids)) or set(route_ids) != declared_closure:
        errors.append("every affected node must have exactly one owned response route")
    if any(row.get("ordinary_use_allowed") for row in routes):
        errors.append("invalidated affected paths cannot retain ordinary use")

    admission = record.get("admission", {})
    if event.get("invalidates_admission"):
        if admission.get("decision") not in {"repair", "review", "quarantined", "blocked"}:
            errors.append("an invalidating event cannot remain eligible for custody review")
        if admission.get("custody_review_allowed") or admission.get("readiness_review_allowed"):
            errors.append("invalidating affected paths must block custody and readiness review")
    bad_refs = [ref for ref in record.get("assurance_references", []) if ref.get("state") in {"unverified", "stale", "revoked", "unresolved"}]
    if bad_refs and (admission.get("custody_review_allowed") or admission.get("decision") == "eligible_for_custody_review"):
        errors.append("stale, unverified, revoked, or unresolved assurances cannot pass admission")
    if node_map.get(subject, {}).get("state") in {"invalidated", "revoked"} and admission.get("decision") != "quarantined":
        errors.append("a revoked or invalidated subject must quarantine the requested path")
    if admission.get("support_state_effect") == "eligible_for_bounded_evidence_review":
        errors.append("hand-authored supply-chain fixtures cannot promote support")

    closure = record.get("lifecycle_closure", {})
    if not all(closure.get(field) for field in ("residual_owner_ref", "retention_until", "disposal_or_retirement_ref", "next_review_trigger")):
        errors.append("lifecycle closure requires residual owner, retention, disposal, and re-review trigger")
    if instant(closure["retention_until"]) <= instant(event["observed_at"]):
        errors.append("retention must extend beyond the invalidation observation")
    if not record.get("promotion_blockers") or not record.get("non_claims"):
        errors.append("supply-chain record must preserve blockers and non-claims")
    return errors


def apply_mutation(base: dict[str, Any], mutation: dict[str, Any]) -> dict[str, Any]:
    value = deepcopy(base)
    if mutation["operation"] == "batch_set":
        for change in mutation["changes"]:
            target: Any = value
            for segment in change["path"][:-1]:
                target = target[segment]
            target[change["path"][-1]] = change["value"]
        return value
    target: Any = value
    for segment in mutation["path"][:-1]:
        target = target[segment]
    leaf = mutation["path"][-1]
    operation = mutation["operation"]
    if operation == "set":
        target[leaf] = mutation["value"]
    elif operation == "delete":
        del target[leaf]
    elif operation == "append":
        target[leaf].append(mutation["value"])
    else:
        raise ValueError(f"unsupported mutation operation {operation!r}")
    return value


def main() -> None:
    schema = load(SCHEMA)
    valid = load(VALID)
    errors = validate_value(valid, schema, str(VALID.relative_to(ROOT))) + semantic_errors(valid)
    if errors:
        raise SystemExit("Valid supply-chain affected-path record failed:\n - " + "\n - ".join(errors))
    mutations = sorted(MUTATIONS.glob("invalid_*.json"))
    if not mutations:
        raise SystemExit("No supply-chain affected-path mutations found.")
    for path in mutations:
        mutation = load(path)
        candidate = apply_mutation(valid, mutation)
        found = validate_value(candidate, schema, str(path.relative_to(ROOT))) + semantic_errors(candidate)
        if not any(mutation["expected_error"] in error for error in found):
            raise SystemExit(f"{path.relative_to(ROOT)} did not produce {mutation['expected_error']!r}: {found}")
    print(f"Supply-chain affected-path harness passed: 1 quarantined three-project record and {len(mutations)} expected-invalid mutations.")


if __name__ == "__main__":
    main()
