#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "experiments" / "planning_scheduler_state" / "results" / "2026-07-02-local.json"
DOC = ROOT / "docs" / "planning_scheduler_state_probe.md"
CHAPTER = ROOT / "chapters" / "planning-as-a-control-layer.qmd"
READER = (
    ROOT
    / "editions"
    / "reader_manuscript"
    / "v1_0"
    / "chapters"
    / "planning-as-a-control-layer.qmd"
)
OUTLINE = ROOT / "docs" / "book_outline.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
CHANGELOG = ROOT / "appendices" / "F_changelog.qmd"
MANIFEST = ROOT / "book_structure.json"
VALIDATION_REGISTRY = ROOT / "validation" / "registry.json"
LEAN_FILE = ROOT / "lean" / "AsiStackProofs" / "Planning.lean"
PLANFORGE_LEAN_FILE = ROOT / "lean" / "AsiStackProofs" / "PlanForge.lean"

COMMAND = "python3 scripts/validate_planning_scheduler_state_probe.py"
PROOF_TAG = "lean:planning.scheduler_state.probe_fixture_bridge"
CODEX_TEST_NAME = "Planning scheduler-state probe"
EXPECTED_PLANNING_THEOREM_COUNT = 53
EXPECTED_PLANFORGE_THEOREM_COUNT = 18
REQUIRED_THEOREMS = [
    "missing_command_contract_blocks_plan_graph_admission",
    "incomplete_decomposition_blocks_plan_graph_admission",
    "cyclic_plan_graph_blocks_admission",
    "unordered_dependencies_block_plan_graph_admission",
    "authority_escalation_blocks_plan_graph_admission",
    "missing_context_demand_blocks_plan_graph_admission",
    "missing_adequacy_contract_blocks_plan_graph_admission",
    "missing_verification_plan_blocks_plan_graph_admission",
    "missing_dispatch_gate_blocks_plan_graph_admission",
    "missing_dispatch_receipt_blocks_plan_graph_admission",
    "replanning_without_authority_preservation_blocks_admission",
    "missing_residual_register_blocks_new_plan_admission",
    "complete_new_plan_graph_routes_to_admissible",
    "complete_replanned_graph_routes_to_admissible",
    "accepted_planning_lifecycle_step_is_admissible",
    "accepted_planning_lifecycle_step_applies_event",
    "apply_planning_lifecycle_event_preserves_invariant",
    "accepted_planning_lifecycle_step_preserves_invariant",
    "planning_lifecycle_run_preserves_invariant",
    "initial_planning_lifecycle_state_satisfies_invariant",
    "complete_planning_lifecycle_trace_reaches_replanned_lowering",
    "planning_lifecycle_denial_is_state_noninterfering",
    "authority_widening_is_rejected_before_plan_admission",
    "incomplete_decomposition_is_rejected_before_plan_admission",
    "missing_context_is_rejected_before_node_readiness",
    "inadequate_selected_route_is_rejected_before_node_readiness",
    "missing_dispatch_receipt_is_rejected_before_job_lowering",
    "blocked_authority_path_is_rejected_before_job_lowering",
    "feedback_before_job_lowering_is_rejected",
    "stop_condition_erasure_is_rejected_before_replan",
    "unscoped_repair_is_rejected_before_replan",
    "missing_replan_residual_is_rejected",
    "hidden_override_is_rejected_before_planning_transition",
    "admitted_plan_event_refines_vertical_lower_plan",
    "lowered_job_event_refines_vertical_lower_job",
    "accepted_graph_bound_plan_admission_preserves_both_models",
    "diamond_graph_bound_admission_reaches_admitted_state",
    "self_dependent_graph_bound_admission_is_rejected",
    "mismatched_graph_artifact_admission_is_rejected",
    "accepted_graph_bound_admission_projects_to_legacy_dispatchable",
]
REQUIRED_PLANFORGE_THEOREMS = [
    "dispatchable_plan_graph_orders_member_edges",
    "dependency_precedence_blocks_self_dependency",
    "verified_plan_graph_member_edge_is_bounded_and_ordered",
    "verified_plan_graph_dependency_paths_strictly_increase",
    "verified_plan_graph_excludes_dependency_cycles",
    "verified_plan_graph_routes_to_admission",
    "diamond_plan_graph_is_verified",
    "diamond_plan_graph_has_reachable_join",
    "self_dependency_graph_is_rejected",
    "reverse_dependency_graph_is_rejected",
    "out_of_bounds_graph_is_rejected",
    "thin_plan_graph_summary_has_admission_collision",
    "no_thin_plan_graph_classifier_recovers_both_decisions",
    "complete_plan_graph_transport_round_trips",
    "complete_plan_graph_transport_is_injective",
    "complete_plan_graph_transport_preserves_admission",
    "verified_plan_graph_projects_to_legacy_dispatchable",
    "failed_quality_predicate_routes_to_escalation_or_residual",
]
REQUIRED_NON_CLAIMS = [
    "does not prove decomposition quality",
    "does not prove context-demand prediction",
    "does not prove selected-tier adequacy",
    "does not prove route quality or scheduler optimality",
    "does not execute a deployed scheduler or runtime replanning loop",
    "does not promote the chapter support state",
]

REQUIRED_LEDGER_FIELDS = {
    "model",
    "context",
    "verification",
    "repair",
    "human_review",
    "failed_attempt",
    "residual",
}
READY_STATES = {"ready", "dispatchable", "running", "merged"}
BLOCKED_STATES = {"blocked_context", "blocked_authority", "blocked_dependency", "blocked_verification"}

PLAN_GRAPH_CASES = [
    {
        "case_id": "diamond_graph",
        "expect_valid": True,
        "graph_id": 1003,
        "node_count": 4,
        "declared_acyclic": True,
        "declared_dependencies_ordered": True,
        "edges": [(0, 1), (0, 2), (1, 3), (2, 3)],
    },
    {
        "case_id": "self_dependency_graph",
        "expect_valid": False,
        "graph_id": 1003,
        "node_count": 4,
        "declared_acyclic": True,
        "declared_dependencies_ordered": True,
        "edges": [(0, 1), (0, 2), (1, 1), (2, 3)],
    },
    {
        "case_id": "reverse_dependency_graph",
        "expect_valid": False,
        "graph_id": 1003,
        "node_count": 4,
        "declared_acyclic": True,
        "declared_dependencies_ordered": True,
        "edges": [(2, 1)],
    },
    {
        "case_id": "out_of_bounds_graph",
        "expect_valid": False,
        "graph_id": 1003,
        "node_count": 4,
        "declared_acyclic": True,
        "declared_dependencies_ordered": True,
        "edges": [(3, 4)],
    },
]


TRACES: list[dict[str, Any]] = [
    {
        "trace_id": "valid_scheduler_state_fixture",
        "expect_valid": True,
        "accepted_command_ref": "command://public-reader-planning-pass",
        "support_state_effect": "none",
        "graph_acyclic": True,
        "dependencies_ordered": True,
        "cost_quality_ledger_fields": sorted(REQUIRED_LEDGER_FIELDS),
        "nodes": [
            {
                "node_id": "node://ready-source-map",
                "state": "dispatchable",
                "context_present": True,
                "authority_within_parent": True,
                "adequacy_contract_present": True,
                "quality_predicate_passed": True,
                "verification_present": True,
                "dispatch_receipt_ref": "dispatch://ready-source-map",
                "residual_recorded": False,
            },
            {
                "node_id": "node://blocked-context",
                "state": "blocked_context",
                "context_present": False,
                "authority_within_parent": True,
                "adequacy_contract_present": True,
                "quality_predicate_passed": False,
                "verification_present": True,
                "dispatch_receipt_ref": "",
                "residual_recorded": True,
            },
        ],
        "candidate_routes": [
            {
                "route_id": "route://cheap-contextless-summary",
                "selected": False,
                "adequacy_predicate_passed": False,
                "verification_present": True,
                "residual_recorded": True,
            },
            {
                "route_id": "route://scoped-source-plus-verifier",
                "selected": True,
                "adequacy_predicate_passed": True,
                "verification_present": True,
                "residual_recorded": True,
            },
        ],
        "merge_attempted": True,
        "assumption_conflict": True,
        "merge_accepted": False,
        "merge_residual_recorded": True,
        "replan_attempted": False,
        "replan_preserves_authority": True,
        "replan_preserves_stop_conditions": True,
        "affected_subgraph_only": True,
        "replan_residual_recorded": True,
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "valid_local_repair_fixture",
        "expect_valid": True,
        "accepted_command_ref": "command://public-reader-planning-pass",
        "support_state_effect": "none",
        "graph_acyclic": True,
        "dependencies_ordered": True,
        "cost_quality_ledger_fields": sorted(REQUIRED_LEDGER_FIELDS),
        "nodes": [
            {
                "node_id": "node://stale-source-repair",
                "state": "replanned",
                "context_present": True,
                "authority_within_parent": True,
                "adequacy_contract_present": True,
                "quality_predicate_passed": True,
                "verification_present": True,
                "dispatch_receipt_ref": "dispatch://stale-source-repair",
                "residual_recorded": True,
            },
            {
                "node_id": "node://unaffected-summary",
                "state": "ready",
                "context_present": True,
                "authority_within_parent": True,
                "adequacy_contract_present": True,
                "quality_predicate_passed": True,
                "verification_present": True,
                "dispatch_receipt_ref": "dispatch://unaffected-summary",
                "residual_recorded": False,
            },
        ],
        "candidate_routes": [
            {
                "route_id": "route://local-repair-with-dependent-rerun",
                "selected": True,
                "adequacy_predicate_passed": True,
                "verification_present": True,
                "residual_recorded": True,
            }
        ],
        "merge_attempted": False,
        "assumption_conflict": False,
        "merge_accepted": False,
        "merge_residual_recorded": True,
        "replan_attempted": True,
        "replan_preserves_authority": True,
        "replan_preserves_stop_conditions": True,
        "affected_subgraph_only": True,
        "replan_residual_recorded": True,
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "invalid_blocked_node_dispatched",
        "expect_valid": False,
        "accepted_command_ref": "command://bad-blocked-dispatch",
        "support_state_effect": "none",
        "graph_acyclic": True,
        "dependencies_ordered": True,
        "cost_quality_ledger_fields": sorted(REQUIRED_LEDGER_FIELDS),
        "nodes": [
            {
                "node_id": "node://blocked-context-dispatched",
                "state": "blocked_context",
                "context_present": False,
                "authority_within_parent": True,
                "adequacy_contract_present": True,
                "quality_predicate_passed": False,
                "verification_present": True,
                "dispatch_receipt_ref": "dispatch://blocked-context-dispatched",
                "residual_recorded": True,
            }
        ],
        "candidate_routes": [],
        "merge_attempted": False,
        "assumption_conflict": False,
        "merge_accepted": False,
        "merge_residual_recorded": True,
        "replan_attempted": False,
        "replan_preserves_authority": True,
        "replan_preserves_stop_conditions": True,
        "affected_subgraph_only": True,
        "replan_residual_recorded": True,
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "invalid_ready_without_context",
        "expect_valid": False,
        "accepted_command_ref": "command://bad-ready-context",
        "support_state_effect": "none",
        "graph_acyclic": True,
        "dependencies_ordered": True,
        "cost_quality_ledger_fields": sorted(REQUIRED_LEDGER_FIELDS),
        "nodes": [
            {
                "node_id": "node://ready-without-context",
                "state": "ready",
                "context_present": False,
                "authority_within_parent": True,
                "adequacy_contract_present": True,
                "quality_predicate_passed": True,
                "verification_present": True,
                "dispatch_receipt_ref": "dispatch://ready-without-context",
                "residual_recorded": False,
            }
        ],
        "candidate_routes": [],
        "merge_attempted": False,
        "assumption_conflict": False,
        "merge_accepted": False,
        "merge_residual_recorded": True,
        "replan_attempted": False,
        "replan_preserves_authority": True,
        "replan_preserves_stop_conditions": True,
        "affected_subgraph_only": True,
        "replan_residual_recorded": True,
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "invalid_failed_adequacy_route_selected",
        "expect_valid": False,
        "accepted_command_ref": "command://bad-route-selection",
        "support_state_effect": "none",
        "graph_acyclic": True,
        "dependencies_ordered": True,
        "cost_quality_ledger_fields": sorted(REQUIRED_LEDGER_FIELDS),
        "nodes": [],
        "candidate_routes": [
            {
                "route_id": "route://cheap-contextless-summary",
                "selected": True,
                "adequacy_predicate_passed": False,
                "verification_present": True,
                "residual_recorded": False,
            }
        ],
        "merge_attempted": False,
        "assumption_conflict": False,
        "merge_accepted": False,
        "merge_residual_recorded": True,
        "replan_attempted": False,
        "replan_preserves_authority": True,
        "replan_preserves_stop_conditions": True,
        "affected_subgraph_only": True,
        "replan_residual_recorded": True,
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "invalid_conflicting_merge_accepted",
        "expect_valid": False,
        "accepted_command_ref": "command://bad-merge",
        "support_state_effect": "none",
        "graph_acyclic": True,
        "dependencies_ordered": True,
        "cost_quality_ledger_fields": sorted(REQUIRED_LEDGER_FIELDS),
        "nodes": [],
        "candidate_routes": [],
        "merge_attempted": True,
        "assumption_conflict": True,
        "merge_accepted": True,
        "merge_residual_recorded": False,
        "replan_attempted": False,
        "replan_preserves_authority": True,
        "replan_preserves_stop_conditions": True,
        "affected_subgraph_only": True,
        "replan_residual_recorded": True,
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "invalid_replan_erases_authority_delta",
        "expect_valid": False,
        "accepted_command_ref": "command://bad-replan-authority",
        "support_state_effect": "none",
        "graph_acyclic": True,
        "dependencies_ordered": True,
        "cost_quality_ledger_fields": sorted(REQUIRED_LEDGER_FIELDS),
        "nodes": [],
        "candidate_routes": [],
        "merge_attempted": False,
        "assumption_conflict": False,
        "merge_accepted": False,
        "merge_residual_recorded": True,
        "replan_attempted": True,
        "replan_preserves_authority": False,
        "replan_preserves_stop_conditions": True,
        "affected_subgraph_only": True,
        "replan_residual_recorded": True,
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "invalid_dependency_cycle_accepted",
        "expect_valid": False,
        "accepted_command_ref": "command://bad-cycle",
        "support_state_effect": "none",
        "graph_acyclic": False,
        "dependencies_ordered": True,
        "cost_quality_ledger_fields": sorted(REQUIRED_LEDGER_FIELDS),
        "nodes": [],
        "candidate_routes": [],
        "merge_attempted": False,
        "assumption_conflict": False,
        "merge_accepted": False,
        "merge_residual_recorded": True,
        "replan_attempted": False,
        "replan_preserves_authority": True,
        "replan_preserves_stop_conditions": True,
        "affected_subgraph_only": True,
        "replan_residual_recorded": True,
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "invalid_cost_ledger_erases_repair",
        "expect_valid": False,
        "accepted_command_ref": "command://bad-cost-ledger",
        "support_state_effect": "none",
        "graph_acyclic": True,
        "dependencies_ordered": True,
        "cost_quality_ledger_fields": ["model", "context", "verification"],
        "nodes": [],
        "candidate_routes": [],
        "merge_attempted": False,
        "assumption_conflict": False,
        "merge_accepted": False,
        "merge_residual_recorded": True,
        "replan_attempted": False,
        "replan_preserves_authority": True,
        "replan_preserves_stop_conditions": True,
        "affected_subgraph_only": True,
        "replan_residual_recorded": True,
        "non_claims": REQUIRED_NON_CLAIMS,
    },
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Planning scheduler-state probe validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def text_blob(value: Any) -> str:
    if isinstance(value, dict):
        return "\n".join(f"{key}: {text_blob(child)}" for key, child in value.items()).lower()
    if isinstance(value, list):
        return "\n".join(text_blob(item) for item in value).lower()
    return str(value).lower()


def trace_errors(trace: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    trace_id = str(trace.get("trace_id", "<missing>"))
    if not isinstance(trace.get("accepted_command_ref"), str) or not trace["accepted_command_ref"].startswith("command://"):
        errors.append(f"{trace_id}: accepted_command_ref must use command://.")
    if trace.get("support_state_effect") != "none":
        errors.append(f"{trace_id}: support_state_effect must be none.")
    if trace.get("graph_acyclic") is not True:
        errors.append(f"{trace_id}: graph must carry an acyclicity boundary.")
    if trace.get("dependencies_ordered") is not True:
        errors.append(f"{trace_id}: dependencies must be ordered before dispatch.")

    ledger_fields = set(trace.get("cost_quality_ledger_fields", []))
    if ledger_fields != REQUIRED_LEDGER_FIELDS:
        errors.append(f"{trace_id}: cost_quality_ledger_fields must include {sorted(REQUIRED_LEDGER_FIELDS)}.")

    nodes = trace.get("nodes", [])
    if not isinstance(nodes, list):
        errors.append(f"{trace_id}: nodes must be a list.")
        nodes = []
    for index, node in enumerate(nodes):
        if not isinstance(node, dict):
            errors.append(f"{trace_id}: nodes[{index}] must be an object.")
            continue
        node_id = str(node.get("node_id", f"nodes[{index}]"))
        state = str(node.get("state", ""))
        dispatch_receipt = str(node.get("dispatch_receipt_ref", "")).strip()
        if state in READY_STATES:
            for field in ("context_present", "authority_within_parent", "adequacy_contract_present", "quality_predicate_passed", "verification_present"):
                if node.get(field) is not True:
                    errors.append(f"{trace_id}:{node_id}: ready/dispatchable node missing {field}.")
            if not dispatch_receipt.startswith("dispatch://"):
                errors.append(f"{trace_id}:{node_id}: ready/dispatchable node requires dispatch receipt.")
        if state in BLOCKED_STATES:
            if dispatch_receipt:
                errors.append(f"{trace_id}:{node_id}: blocked node cannot carry a dispatch receipt.")
            if node.get("residual_recorded") is not True:
                errors.append(f"{trace_id}:{node_id}: blocked node must record residuals.")
        if node.get("authority_within_parent") is not True and dispatch_receipt:
            errors.append(f"{trace_id}:{node_id}: authority-widening node cannot dispatch.")

    candidate_routes = trace.get("candidate_routes", [])
    if not isinstance(candidate_routes, list):
        errors.append(f"{trace_id}: candidate_routes must be a list.")
        candidate_routes = []
    for index, route in enumerate(candidate_routes):
        if not isinstance(route, dict):
            errors.append(f"{trace_id}: candidate_routes[{index}] must be an object.")
            continue
        route_id = str(route.get("route_id", f"candidate_routes[{index}]"))
        if route.get("selected") is True:
            if route.get("adequacy_predicate_passed") is not True:
                errors.append(f"{trace_id}:{route_id}: selected route must pass adequacy predicate.")
            if route.get("verification_present") is not True:
                errors.append(f"{trace_id}:{route_id}: selected route requires verification.")
        if route.get("adequacy_predicate_passed") is False and route.get("residual_recorded") is not True:
            errors.append(f"{trace_id}:{route_id}: failed adequacy predicate must record residual.")

    if trace.get("merge_attempted") is True and trace.get("assumption_conflict") is True:
        if trace.get("merge_accepted") is True:
            errors.append(f"{trace_id}: conflicting assumptions must block merge acceptance.")
        if trace.get("merge_residual_recorded") is not True:
            errors.append(f"{trace_id}: conflicting merge must record residual.")

    if trace.get("replan_attempted") is True:
        if trace.get("replan_preserves_authority") is not True:
            errors.append(f"{trace_id}: replanning must preserve authority.")
        if trace.get("replan_preserves_stop_conditions") is not True:
            errors.append(f"{trace_id}: replanning must preserve stop conditions.")
        if trace.get("affected_subgraph_only") is not True:
            errors.append(f"{trace_id}: replanning must be local to the affected subgraph.")
        if trace.get("replan_residual_recorded") is not True:
            errors.append(f"{trace_id}: replanning must record residuals.")

    non_claim_text = text_blob(trace.get("non_claims", []))
    for phrase in REQUIRED_NON_CLAIMS:
        if phrase.lower() not in non_claim_text:
            errors.append(f"{trace_id}: non_claims missing {phrase!r}.")

    return errors


def graph_verified(graph: dict[str, Any]) -> bool:
    node_count = graph["node_count"]
    return (
        graph["declared_acyclic"] is True
        and graph["declared_dependencies_ordered"] is True
        and node_count > 0
        and all(0 <= dependency < dependent < node_count for dependency, dependent in graph["edges"])
    )


def thin_graph_summary(graph: dict[str, Any]) -> tuple[Any, ...]:
    return (
        graph["graph_id"],
        graph["node_count"],
        len(graph["edges"]),
        graph["declared_acyclic"],
        graph["declared_dependencies_ordered"],
    )


def complete_graph_transport(graph: dict[str, Any]) -> tuple[Any, ...]:
    return (
        graph["graph_id"],
        graph["node_count"],
        tuple(graph["edges"]),
        graph["declared_acyclic"],
        graph["declared_dependencies_ordered"],
    )


def dependency_reachability(graph: dict[str, Any]) -> set[tuple[int, int]]:
    reachable = set(graph["edges"])
    changed = True
    while changed:
        changed = False
        for start, middle in tuple(reachable):
            for next_middle, finish in tuple(reachable):
                if middle == next_middle and (start, finish) not in reachable:
                    reachable.add((start, finish))
                    changed = True
    return reachable


def validate_planforge_graph_cases(errors: list[str]) -> dict[str, int]:
    valid_count = 0
    rejected_count = 0
    for graph in PLAN_GRAPH_CASES:
        actual = graph_verified(graph)
        if actual is bool(graph["expect_valid"]):
            if actual:
                valid_count += 1
            else:
                rejected_count += 1
        else:
            errors.append(f"{graph['case_id']}: graph-verifier decision drifted.")

    diamond, self_dependent = PLAN_GRAPH_CASES[:2]
    thin_collision_count = int(
        diamond != self_dependent
        and thin_graph_summary(diamond) == thin_graph_summary(self_dependent)
        and graph_verified(diamond) != graph_verified(self_dependent)
    )
    if thin_collision_count != 1:
        errors.append("PlanForge thin graph summary failed to expose its admission collision.")

    reachable = dependency_reachability(diamond)
    if (0, 3) not in reachable:
        errors.append("PlanForge diamond graph did not reconstruct the 0-to-3 dependency path.")
    if any(start == finish for start, finish in reachable):
        errors.append("PlanForge verified graph admitted a dependency cycle.")

    complete_transport_rejections = 0
    mutations: list[dict[str, Any]] = []
    for field in ("graph_id", "node_count", "declared_acyclic", "declared_dependencies_ordered"):
        changed = copy.deepcopy(diamond)
        if isinstance(changed[field], bool):
            changed[field] = not changed[field]
        else:
            changed[field] += 1
        mutations.append(changed)
    for index in range(len(diamond["edges"])):
        for endpoint in (0, 1):
            changed = copy.deepcopy(diamond)
            edge = list(changed["edges"][index])
            edge[endpoint] += 10
            changed["edges"][index] = tuple(edge)
            mutations.append(changed)
    for changed in mutations:
        if complete_graph_transport(changed) != complete_graph_transport(diamond):
            complete_transport_rejections += 1
        else:
            errors.append("PlanForge complete graph transport accepted a field mutation.")

    return {
        "graph_case_count": len(PLAN_GRAPH_CASES),
        "valid_graph_count": valid_count,
        "rejected_graph_count": rejected_count,
        "reachable_pair_count": len(reachable),
        "thin_summary_collision_count": thin_collision_count,
        "complete_transport_mutation_rejection_count": complete_transport_rejections,
    }


def build_expected_result(
    valid_count: int, invalid_count: int, graph_metrics: dict[str, int]
) -> dict[str, Any]:
    return {
        "schema_version": "asi_stack.planning_scheduler_state_probe.v0",
        "result_id": "2026-07-02-planning-scheduler-state-probe",
        "recorded_date": "2026-07-02",
        "command": COMMAND,
        "result_kind": "deterministic_synthetic_planning_scheduler_state_probe",
        "valid_trace_count": valid_count,
        "expected_invalid_control_count": invalid_count,
        "trace_count": len(TRACES),
        "negative_controls": {
            "blocked_node_dispatch_rejected": True,
            "ready_without_context_rejected": True,
            "failed_adequacy_route_rejected": True,
            "conflicting_merge_rejected": True,
            "replan_authority_erasure_rejected": True,
            "dependency_cycle_rejected": True,
            "cost_ledger_repair_erasure_rejected": True,
        },
        "transition_coverage": {
            "ready_node_dispatch_receipt": True,
            "blocked_context_residual": True,
            "failed_cheap_route_rejection": True,
            "merge_conflict_block": True,
            "local_repair_replan_delta": True,
            "cost_quality_ledger_hidden_costs": True,
        },
        "lean_fixture_alignment": {
            "module": "AsiStackProofs.Planning",
            "proof_tag": PROOF_TAG,
            "theorem_refs": REQUIRED_THEOREMS,
            "expected": {
                "valid_scheduler_trace_present": True,
                "local_repair_trace_present": True,
                "negative_controls_rejected": True,
                "cost_quality_ledger_present": True,
                "support_state_effect_none": True,
                "non_claim_boundary": True,
            },
        },
        "planforge_graph_alignment": {
            "module": "AsiStackProofs.PlanForge",
            "proof_tag": "lean:planforge.dag.operational_invariant",
            "planning_bridge_module": "AsiStackProofs.Planning",
            "theorem_count": EXPECTED_PLANFORGE_THEOREM_COUNT,
            "theorem_refs": REQUIRED_PLANFORGE_THEOREMS,
            "planning_bridge_theorem_refs": [
                "accepted_graph_bound_plan_admission_preserves_both_models",
                "diamond_graph_bound_admission_reaches_admitted_state",
                "self_dependent_graph_bound_admission_is_rejected",
                "mismatched_graph_artifact_admission_is_rejected",
                "accepted_graph_bound_admission_projects_to_legacy_dispatchable",
            ],
            **graph_metrics,
        },
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
        "verification_result": "pass",
        "residuals": [
            "Synthetic scheduler-state fixture only; no deployed planner, scheduler, route-quality evaluator, or runtime replanning loop was exercised.",
            "The chapter core claim remains at argument support.",
        ],
        "non_claims": REQUIRED_NON_CLAIMS,
    }


def validate_result(expected: dict[str, Any], write_result: bool, errors: list[str]) -> None:
    serialized = json.dumps(expected, indent=2, sort_keys=True) + "\n"
    if write_result:
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(serialized, encoding="utf-8")
        return
    if not RESULT.exists():
        errors.append(f"Missing {rel(RESULT)}; run {COMMAND} --write-result.")
        return
    current = RESULT.read_text(encoding="utf-8")
    if current != serialized:
        errors.append(f"{rel(RESULT)} is stale; run {COMMAND} --write-result.")
    value = load_json(RESULT)
    if value.get("verification_result") != "pass":
        errors.append(f"{rel(RESULT)}: verification_result must be pass.")
    if value.get("support_state_effect") != "none":
        errors.append(f"{rel(RESULT)}: support_state_effect must remain none.")
    if value.get("evidence_transition_created") is not False:
        errors.append(f"{rel(RESULT)}: evidence_transition_created must remain false.")


def validate_manifest(errors: list[str]) -> None:
    value = load_json(MANIFEST)
    chapter = None
    for part in value.get("parts", []):
        for candidate in part.get("chapters", []):
            if candidate.get("id") == "planning-as-a-control-layer":
                chapter = candidate
                break
    if chapter is None:
        errors.append("book_structure.json: missing planning chapter.")
        return
    codex_blob = text_blob(chapter.get("codex_tests", []))
    if CODEX_TEST_NAME.lower() not in codex_blob:
        errors.append(f"book_structure.json: codex_tests missing {CODEX_TEST_NAME!r}.")
    proof_tags = {target.get("tag") for target in chapter.get("proof_targets", []) if isinstance(target, dict)}
    if PROOF_TAG not in proof_tags:
        errors.append(f"book_structure.json: proof_targets missing {PROOF_TAG!r}.")


def validate_lean(errors: list[str]) -> None:
    text = LEAN_FILE.read_text(encoding="utf-8", errors="ignore")
    theorem_count = len(re.findall(r"(?m)^theorem\s+[A-Za-z_][A-Za-z0-9_']*", text))
    if theorem_count != EXPECTED_PLANNING_THEOREM_COUNT:
        errors.append(
            f"{rel(LEAN_FILE)} has {theorem_count} theorem declarations; "
            f"expected exactly {EXPECTED_PLANNING_THEOREM_COUNT}."
        )
    for theorem in REQUIRED_THEOREMS:
        if not re.search(rf"\btheorem\s+{re.escape(theorem)}\b", text):
            errors.append(f"{rel(LEAN_FILE)} missing theorem {theorem}.")
    for label, pattern in (
        ("sorry", r"\bsorry\b"),
        ("admit", r"\badmit\b"),
        ("axiom declaration", r"(?m)^\s*axiom\s"),
    ):
        if re.search(pattern, text):
            errors.append(f"{rel(LEAN_FILE)} contains forbidden {label}.")
    for field in (
        "validSchedulerTracePresent",
        "localRepairTracePresent",
        "negativeControlsRejected",
        "costQualityLedgerPresent",
        "supportStateEffectNone",
        "nonClaimBoundary",
    ):
        if field not in text:
            errors.append(f"{rel(LEAN_FILE)} missing fixture field {field}.")

    planforge_text = PLANFORGE_LEAN_FILE.read_text(encoding="utf-8", errors="ignore")
    planforge_theorem_count = len(
        re.findall(r"(?m)^theorem\s+[A-Za-z_][A-Za-z0-9_']*", planforge_text)
    )
    if planforge_theorem_count != EXPECTED_PLANFORGE_THEOREM_COUNT:
        errors.append(
            f"{rel(PLANFORGE_LEAN_FILE)} has {planforge_theorem_count} theorem declarations; "
            f"expected exactly {EXPECTED_PLANFORGE_THEOREM_COUNT}."
        )
    for theorem in REQUIRED_PLANFORGE_THEOREMS:
        if not re.search(rf"\btheorem\s+{re.escape(theorem)}\b", planforge_text):
            errors.append(f"{rel(PLANFORGE_LEAN_FILE)} missing theorem {theorem}.")

    dependency_build = subprocess.run(
        ["lake", "build", "AsiStackProofs"],
        cwd=ROOT / "lean",
        capture_output=True,
        text=True,
    )
    if dependency_build.returncode:
        errors.append(
            "Lean dependency build failed before planning source checks:\n"
            f"{dependency_build.stdout}{dependency_build.stderr}"
        )
        return

    for path in (PLANFORGE_LEAN_FILE, LEAN_FILE):
        completed = subprocess.run(
            ["lake", "env", "lean", str(path.relative_to(ROOT / "lean"))],
            cwd=ROOT / "lean",
            capture_output=True,
            text=True,
        )
        if completed.returncode:
            errors.append(
                f"{rel(path)} did not compile:\n{completed.stdout}{completed.stderr}"
            )


def validate_surfaces(errors: list[str]) -> None:
    required = {
        DOC: [
            "Planning Scheduler-State Probe",
            rel(RESULT),
            "two valid synthetic scheduler traces",
            "seven expected-invalid controls",
            "no support-state transition",
        ],
        CHAPTER: [
            "Planning scheduler-state probe",
            rel(RESULT),
            "two valid synthetic scheduler traces",
            "seven expected-invalid controls",
        ],
        READER: [
            "planning scheduler-state probe",
            "two synthetic scheduler traces",
            "not a deployed scheduler result",
        ],
        OUTLINE: [
            CODEX_TEST_NAME,
            PROOF_TAG,
            rel(RESULT),
        ],
        ROADMAP: [
            "Planning scheduler-state probe",
            "deterministic synthetic scheduler-state fixture",
            "no support-state promotion",
        ],
        CHANGELOG: [
            "Planning scheduler-state probe",
            rel(RESULT),
        ],
        VALIDATION_REGISTRY: [
            "scripts/validate_planning_scheduler_state_probe.py",
            "docs/planning_scheduler_state_probe.md",
            "experiments/planning_scheduler_state/results/2026-07-02-local.json",
            '"script": "validate_planning_scheduler_state_probe.py"',
        ],
    }
    for path, phrases in required.items():
        if not path.exists():
            errors.append(f"Missing required planning scheduler surface {rel(path)}.")
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        lowered = text.lower()
        for phrase in phrases:
            if phrase.lower() not in lowered:
                errors.append(f"{rel(path)} missing required phrase {phrase!r}.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-result", action="store_true")
    args = parser.parse_args()

    errors: list[str] = []
    valid_count = 0
    invalid_count = 0
    for trace in TRACES:
        expect_valid = bool(trace.get("expect_valid"))
        trace_id = str(trace.get("trace_id", "<missing>"))
        current_errors = trace_errors(trace)
        if expect_valid:
            valid_count += 1
            errors.extend(current_errors)
        else:
            invalid_count += 1
            if not current_errors:
                errors.append(f"{trace_id}: expected-invalid control unexpectedly passed.")

    if valid_count != 2:
        errors.append("Expected exactly two valid synthetic scheduler traces.")
    if invalid_count != 7:
        errors.append("Expected exactly seven expected-invalid controls.")

    graph_metrics = validate_planforge_graph_cases(errors)
    expected = build_expected_result(valid_count, invalid_count, graph_metrics)
    validate_result(expected, args.write_result, errors)
    validate_manifest(errors)
    validate_lean(errors)
    validate_surfaces(errors)

    if errors:
        fail(errors)
    print("Planning scheduler-state probe validation passed.")


if __name__ == "__main__":
    main()
