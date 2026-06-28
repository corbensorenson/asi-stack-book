#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

from validate_protocol_examples import validate_value

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "experiments" / "plan_execution_contracts" / "fixtures"

SCHEMAS = {
    "command_contract": ROOT / "schemas" / "command_contract.schema.json",
    "plan_graph": ROOT / "schemas" / "plan_graph.schema.json",
    "planforge_dag": ROOT / "schemas" / "planforge_dag.schema.json",
    "typed_job": ROOT / "schemas" / "typed_job.schema.json",
    "semantic_atom": ROOT / "schemas" / "semantic_atom.schema.json",
}

ACTIVE_JOB_STATES = {"dispatchable", "running", "delivered", "adjudicating"}
APPROVAL_MEANINGFUL_NONE = {"none", "none for public-safe local draft edits", "not_required"}
BAD_OBLIGATION_STATES = {"deferred", "rejected", "unknown", "blocked"}


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


def parse_edges(values: list[Any], field: str, errors: list[str], relative: str) -> list[tuple[str, str]]:
    edges: list[tuple[str, str]] = []
    for value in values:
        if not isinstance(value, str) or "->" not in value:
            errors.append(f"{relative}: {field} entry {value!r} must use 'from -> to'.")
            continue
        left, right = [part.strip() for part in value.split("->", 1)]
        if not left or not right:
            errors.append(f"{relative}: {field} entry {value!r} has an empty endpoint.")
            continue
        edges.append((left, right))
    return edges


def graph_errors(nodes: list[str], edges: list[tuple[str, str]], name: str, relative: str) -> list[str]:
    errors: list[str] = []
    node_set = set(nodes)
    if len(node_set) != len(nodes):
        errors.append(f"{relative}: {name} nodes must be unique.")
    for left, right in edges:
        if left not in node_set:
            errors.append(f"{relative}: {name} edge source {left!r} is not a node.")
        if right not in node_set:
            errors.append(f"{relative}: {name} edge target {right!r} is not a node.")

    adjacency = {node: [] for node in nodes}
    for left, right in edges:
        if left in adjacency:
            adjacency[left].append(right)

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str, stack: list[str]) -> None:
        if node in visiting:
            cycle = " -> ".join(stack + [node])
            errors.append(f"{relative}: {name} contains a cycle: {cycle}.")
            return
        if node in visited:
            return
        visiting.add(node)
        for child in adjacency.get(node, []):
            if child in node_set:
                visit(child, stack + [node])
        visiting.remove(node)
        visited.add(node)

    for node in nodes:
        visit(node, [])

    order = {node: index for index, node in enumerate(nodes)}
    for left, right in edges:
        if left in order and right in order and order[left] >= order[right]:
            errors.append(
                f"{relative}: {name} edge {left!r} -> {right!r} violates declared node order."
            )

    return errors


def meaningful_approval_required(required_approvals: list[Any]) -> bool:
    if not required_approvals:
        return False
    normalized = {str(item).strip().lower() for item in required_approvals}
    return not normalized.issubset(APPROVAL_MEANINGFUL_NONE)


def schema_errors_for_scenario(value: dict[str, Any], schemas: dict[str, Any], relative: str) -> list[str]:
    errors: list[str] = []
    for field in ("command_contract", "plan_graph", "planforge_dag"):
        if field not in value:
            errors.append(f"{relative}: missing {field}.")
            continue
        errors.extend(validate_value(value[field], schemas[field], f"{relative}:{field}"))
    for index, job in enumerate(value.get("typed_jobs", [])):
        errors.extend(validate_value(job, schemas["typed_job"], f"{relative}:typed_jobs[{index}]"))
    for index, atom in enumerate(value.get("semantic_atoms", [])):
        errors.extend(validate_value(atom, schemas["semantic_atom"], f"{relative}:semantic_atoms[{index}]"))
    return errors


def semantic_errors(value: dict[str, Any], relative: str) -> list[str]:
    errors: list[str] = []
    if not isinstance(value.get("scenario_id"), str) or not value["scenario_id"].strip():
        errors.append(f"{relative}: scenario_id must be a non-empty string.")
    if not isinstance(value.get("typed_jobs"), list):
        errors.append(f"{relative}: typed_jobs must be a list.")
    if not isinstance(value.get("semantic_atoms"), list):
        errors.append(f"{relative}: semantic_atoms must be a list.")
    require_nonempty_list(value, "non_claims", errors, relative)
    if errors:
        return errors

    command = value["command_contract"]
    plan = value["plan_graph"]
    dag = value["planforge_dag"]
    typed_jobs = value.get("typed_jobs", [])
    semantic_atoms = value.get("semantic_atoms", [])

    contract_id = str(command["contract_id"])
    plan_id = str(plan["plan_id"])
    if plan["command_contract"] != contract_id:
        errors.append(f"{relative}: plan_graph.command_contract must match command_contract.contract_id.")
    if dag["parent_plan"] != plan_id:
        errors.append(f"{relative}: planforge_dag.parent_plan must match plan_graph.plan_id.")

    command_required_fields = [
        "constraints",
        "procedure",
        "allowed_means",
        "forbidden_means",
        "verification",
        "failure_behavior",
        "expected_artifacts",
        "non_claims",
    ]
    for field in command_required_fields:
        require_nonempty_list(command, field, errors, f"{relative}:command_contract")

    plan_nodes = list(plan.get("nodes", []))
    dag_nodes = list(dag.get("nodes", []))
    if set(plan_nodes) != set(dag_nodes):
        errors.append(f"{relative}: plan_graph and planforge_dag must name the same node set.")
    plan_edges = parse_edges(plan.get("dependencies", []), "dependencies", errors, relative)
    dag_edges = parse_edges(dag.get("edges", []), "edges", errors, relative)
    if set(plan_edges) != set(dag_edges):
        errors.append(f"{relative}: plan_graph dependencies and planforge_dag edges must match.")
    errors.extend(graph_errors(plan_nodes, plan_edges, "plan_graph", relative))
    errors.extend(graph_errors(dag_nodes, dag_edges, "planforge_dag", relative))

    dispatch_state = str(plan.get("dispatch_state", ""))
    if dispatch_state in {"dispatchable", "running", "complete"}:
        if command.get("validation_state") != "validated_for_planning":
            errors.append(f"{relative}: dispatchable/running/complete plan requires validated command contract.")
        if plan.get("blocked_nodes"):
            errors.append(f"{relative}: dispatchable/running/complete plan cannot have blocked_nodes.")
        require_nonempty_list(plan, "dispatch_receipts", errors, f"{relative}:plan_graph")
    if dispatch_state == "blocked":
        require_nonempty_list(plan, "blocked_nodes", errors, f"{relative}:plan_graph")
        if plan.get("dispatch_receipts"):
            errors.append(f"{relative}: blocked plan must not carry dispatch_receipts.")

    for field in ("context_requests", "tool_requirements", "authority_requirements", "verification_plan", "stop_conditions", "non_claims"):
        require_nonempty_list(plan, field, errors, f"{relative}:plan_graph")
    for field in ("quality_predicates", "verification_requirements", "route_assignments", "non_claims"):
        require_nonempty_list(dag, field, errors, f"{relative}:planforge_dag")

    authority_requirements = {str(item) for item in plan.get("authority_requirements", [])}
    if str(command.get("authority_ceiling")) not in authority_requirements:
        errors.append(f"{relative}: plan authority_requirements must include the command authority_ceiling.")

    receipts_text = "\n".join(str(item) for item in plan.get("dispatch_receipts", []))
    required_approval = meaningful_approval_required(command.get("required_approvals", []))
    job_outputs: set[str] = set()
    for index, job in enumerate(typed_jobs):
        job_prefix = f"{relative}:typed_jobs[{index}]"
        if job.get("contract_id") != contract_id:
            errors.append(f"{job_prefix}: contract_id must match command_contract.contract_id.")
        lifecycle = str(job.get("lifecycle_state", ""))
        if lifecycle in ACTIVE_JOB_STATES and str(job.get("job_id")) not in receipts_text:
            errors.append(f"{job_prefix}: active job must be represented in plan dispatch_receipts.")
        if lifecycle in ACTIVE_JOB_STATES and job.get("approval_state") in {"denied", "expired"}:
            errors.append(f"{job_prefix}: active job cannot have denied or expired approval_state.")
        if required_approval and lifecycle in ACTIVE_JOB_STATES and job.get("approval_state") != "approved":
            errors.append(f"{job_prefix}: active job requires approved approval_state.")
        forbidden_text = " ".join(str(item).lower() for item in command.get("forbidden_means", []))
        for permission in job.get("permissions", []):
            if str(permission).lower() in forbidden_text:
                errors.append(f"{job_prefix}: permission {permission!r} appears in forbidden_means.")
        job_outputs.update(str(item) for item in job.get("outputs", []))

    command_constraints = {str(item) for item in command.get("constraints", [])}
    atom_constraints: set[str] = set()
    atom_artifacts: set[str] = set()
    for index, atom in enumerate(semantic_atoms):
        atom_prefix = f"{relative}:semantic_atoms[{index}]"
        if atom.get("source_plan_ref") != plan_id:
            errors.append(f"{atom_prefix}: source_plan_ref must match plan_graph.plan_id.")
        obligation_refs = {str(item) for item in atom.get("obligation_refs", [])}
        status_by_ref = {
            str(item.get("obligation_ref")): str(item.get("status"))
            for item in atom.get("obligation_status", [])
            if isinstance(item, dict)
        }
        missing_obligations = obligation_refs - set(status_by_ref)
        if missing_obligations:
            errors.append(f"{atom_prefix}: obligation_status missing refs {sorted(missing_obligations)}.")
        bad_status = sorted(ref for ref, status in status_by_ref.items() if status in BAD_OBLIGATION_STATES)
        if dispatch_state in {"dispatchable", "running", "complete"} and bad_status:
            errors.append(f"{atom_prefix}: dispatchable plan cannot have unresolved obligations {bad_status}.")
        if set(str(item) for item in atom.get("authority_required", [])) - authority_requirements:
            errors.append(f"{atom_prefix}: authority_required must be covered by plan authority_requirements.")
        if atom.get("lowering_state") in {"lowered", "validated"}:
            if atom.get("ir_validity_state") != "well_formed":
                errors.append(f"{atom_prefix}: lowered atom requires ir_validity_state == well_formed.")
            if atom.get("validator_status") != "passed":
                errors.append(f"{atom_prefix}: lowered atom requires validator_status == passed.")
        if not str(atom.get("lowering_receipt", "")).startswith("receipt://"):
            errors.append(f"{atom_prefix}: lowering_receipt must use receipt://.")
        atom_constraints.update(str(item) for item in atom.get("constraints", []))
        atom_artifacts.add(str(atom.get("target_artifact_ref", "")))

    if not command_constraints.issubset(atom_constraints):
        errors.append(
            f"{relative}: semantic atoms must preserve command constraints; missing "
            f"{sorted(command_constraints - atom_constraints)}."
        )

    artifact_surface = job_outputs | atom_artifacts
    missing_artifacts = [artifact for artifact in command.get("expected_artifacts", []) if str(artifact) not in artifact_surface]
    if missing_artifacts:
        errors.append(f"{relative}: expected_artifacts are not traceable to job outputs or atom targets: {missing_artifacts}.")

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
        raise SystemExit(f"No plan-execution contract fixtures found in {FIXTURE_DIR.relative_to(ROOT)}.")

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
                errors.append(f"{relative}: invalid fixture unexpectedly passed plan-execution checks.")

    if errors:
        print("Plan-execution contract harness failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print(
        "Plan-execution contract harness passed: "
        f"{valid_count} valid fixture(s), {invalid_count} expected-invalid fixture(s)."
    )


if __name__ == "__main__":
    main()
