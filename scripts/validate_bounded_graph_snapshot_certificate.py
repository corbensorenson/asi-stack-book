#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
from datetime import datetime
import json
from pathlib import Path
from typing import Any

from validate_protocol_examples import validate_value

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "bounded_graph_snapshot_certificate.schema.json"
VALID = ROOT / "tests" / "fixtures" / "protocol_records" / "bounded_graph_snapshot_certificate.valid.json"
MUTATIONS = ROOT / "experiments" / "bounded_graph_snapshot_certificate" / "fixtures"
EXPECTED_SOURCES = {"cca_project", "moecot_manifest_project", "beastbrain_project", "bugbrain_project"}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def instant(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def semantic_errors(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if set(record.get("source_ids", [])) != EXPECTED_SOURCES:
        errors.append("bounded graph snapshot lineage must name CCA, MoECOT, BeastBrain, and BugBrain exactly")
    memory = record.get("durable_memory", {})
    graph = record.get("graph_snapshot", {})
    selection = record.get("bounded_selection", {})
    handle = record.get("context_handle", {})
    revalidation = record.get("revalidation", {})
    materialization = record.get("context_materialization", {})
    decision = record.get("decision", {})

    nodes = graph.get("nodes", [])
    node_ids = [node.get("node_id") for node in nodes]
    node_set = set(node_ids)
    if len(node_ids) != len(node_set):
        errors.append("graph snapshot node identities must be unique")
    if graph.get("node_count") != len(nodes) or graph.get("edge_count") != len(graph.get("edges", [])):
        errors.append("graph snapshot counts must match declared nodes and edges")
    for edge in graph.get("edges", []):
        if edge.get("from") not in node_set or edge.get("to") not in node_set:
            errors.append("every graph edge endpoint must bind a declared node")

    selected = set(selection.get("selected_node_ids", []))
    omitted = set(selection.get("omitted_frontier_node_ids", []))
    if selection.get("root_node_id") not in selected or not selected.issubset(node_set):
        errors.append("bounded selection must include its declared root and only declared nodes")
    if len(selected) > selection.get("node_budget", 0):
        errors.append("bounded selection cannot exceed its node budget")
    selected_depths = [node.get("depth", 0) for node in nodes if node.get("node_id") in selected]
    if any(depth > selection.get("max_depth", -1) for depth in selected_depths):
        errors.append("bounded selection cannot include nodes beyond max depth")
    if omitted != node_set - selected:
        errors.append("omitted frontier must disclose every unselected snapshot node exactly")

    if handle.get("bound_snapshot_id") != memory.get("snapshot_id") or materialization.get("derived_from_snapshot_id") != memory.get("snapshot_id"):
        errors.append("handle and materialized context must bind the durable snapshot identity")
    if handle.get("bound_snapshot_digest") != memory.get("snapshot_digest") or revalidation.get("snapshot_digest") != memory.get("snapshot_digest"):
        errors.append("handle and revalidation must bind the durable snapshot digest")
    if handle.get("generation") != memory.get("generation"):
        errors.append("context handle generation must equal the durable snapshot generation")
    if handle.get("policy_version") != selection.get("selection_policy") or revalidation.get("policy_version") != handle.get("policy_version"):
        errors.append("selection, handle, and revalidation policy versions must match")
    if handle.get("revocation_epoch") != memory.get("revocation_epoch"):
        errors.append("context handle revocation epoch must match the durable snapshot epoch")
    if handle.get("revocation_state") != "active":
        errors.append("revoked, stale, or unknown context handles cannot be admitted")
    if not handle.get("provenance_refs"):
        errors.append("bounded context handle requires provenance references")
    if handle.get("revalidation_required"):
        if revalidation.get("state") != "passed" or not revalidation.get("evidence_refs"):
            errors.append("required handle revalidation must pass with evidence")
    try:
        if not (instant(handle["issued_at"]) <= instant(revalidation["checked_at"]) <= instant(record["recorded_at"]) < instant(handle["expires_at"])):
            errors.append("handle issuance, revalidation, recording, and expiry must be temporally ordered")
    except (KeyError, TypeError, ValueError):
        errors.append("handle lifecycle timestamps must be parseable")

    if materialization.get("materialization_ref") == memory.get("memory_object_ref") or materialization.get("durable_write_authorized"):
        errors.append("bounded context materialization must remain distinct from durable memory and cannot authorize a durable write")
    if decision.get("state") == "admitted_for_bounded_context" and (not decision.get("ordinary_use_allowed") or materialization.get("state") != "materialized_bounded_context"):
        errors.append("admitted bounded context requires a bounded materialization and explicit use decision")
    if decision.get("support_state_effect") == "eligible_for_bounded_evidence_review":
        errors.append("hand-authored graph snapshot fixtures cannot promote support")
    if not record.get("promotion_blockers") or not record.get("non_claims"):
        errors.append("bounded graph snapshot must preserve blockers and non-claims")
    return errors


def apply_mutation(base: dict[str, Any], mutation: dict[str, Any]) -> dict[str, Any]:
    value = deepcopy(base)
    target: Any = value
    for segment in mutation["path"][:-1]:
        target = target[segment]
    target[mutation["path"][-1]] = mutation["value"]
    return value


def main() -> None:
    schema = load(SCHEMA)
    valid = load(VALID)
    errors = validate_value(valid, schema, str(VALID.relative_to(ROOT))) + semantic_errors(valid)
    if errors:
        raise SystemExit("Valid bounded graph snapshot certificate failed:\n - " + "\n - ".join(errors))
    mutations = sorted(MUTATIONS.glob("invalid_*.json"))
    if not mutations:
        raise SystemExit("No bounded graph snapshot mutations found.")
    for path in mutations:
        mutation = load(path)
        candidate = apply_mutation(valid, mutation)
        found = validate_value(candidate, schema, str(path.relative_to(ROOT))) + semantic_errors(candidate)
        if not any(mutation["expected_error"] in error for error in found):
            raise SystemExit(f"{path.relative_to(ROOT)} did not produce {mutation['expected_error']!r}: {found}")
    print(f"Bounded graph snapshot certificate harness passed: 1 bounded four-project record and {len(mutations)} expected-invalid mutations.")


if __name__ == "__main__":
    main()
