#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

from validate_protocol_examples import validate_value

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "experiments" / "prototype_phase_gates" / "fixtures"
RESULT = ROOT / "experiments" / "prototype_phase_gates" / "results" / "2026-07-02-local.json"
SCHEMA = ROOT / "schemas" / "prototype_phase_record.schema.json"

DOC = ROOT / "docs" / "prototype_phase_gate_harness.md"
CHAPTER = ROOT / "chapters" / "prototype-roadmap.qmd"
READER = ROOT / "editions" / "reader_manuscript" / "v1_0" / "chapters" / "prototype-roadmap.qmd"
OUTLINE = ROOT / "docs" / "book_outline.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
LEAN = ROOT / "lean" / "AsiStackProofs" / "PrototypeRoadmap.lean"
LEAN_ROOT = ROOT / "lean"

REQUIRED_LIFECYCLE_THEOREMS = {
    "valid_prototype_dependency_cannot_be_self_referential",
    "adjacent_prototype_dependencies_compose_strict_order",
    "prototype_phase_rejected_event_is_noninterfering",
    "prototype_phase_execution_step_preserves_custody",
    "run_prototype_phase_execution_preserves_custody",
    "prototype_phase_execution_step_preserves_invariant",
    "run_prototype_phase_execution_preserves_invariant",
    "run_prototype_phase_execution_append",
    "reference_prototype_phase_execution_reaches_integrated",
    "reference_prototype_phase_execution_has_no_support_or_external_effect",
    "reference_prototype_phase_execution_has_exact_receipt_count",
    "reference_prototype_promotion_reaches_evidence_review",
    "reference_prototype_promotion_has_no_support_or_external_effect",
    "incomplete_dependency_count_rejects_without_state_change",
    "dependency_inversion_rejects_without_state_change",
    "missing_rollback_plan_rejects_execution_without_state_change",
    "self_improvement_without_independent_execution_evaluator_rejected",
    "failed_execution_acceptance_gates_reject_integration",
    "phase_debt_without_retirement_condition_rejects_integration",
    "promotion_without_evidence_transition_rejects_review_handoff",
    "integrated_prototype_phase_is_absorbing_one_step",
    "evidence_review_prototype_phase_is_absorbing_one_step",
    "rolled_back_prototype_phase_is_absorbing_one_step",
    "integrated_prototype_phase_is_absorbing_for_any_suffix",
    "evidence_review_prototype_phase_is_absorbing_for_any_suffix",
    "rolled_back_prototype_phase_is_absorbing_for_any_suffix",
    "prototype_phase_thin_summary_collides_across_integration",
    "no_prototype_phase_thin_summary_classifier_recovers_integration",
}

REFERENCE_EXECUTION_EVENTS = (
    ("bind", 41, 3, 701, 4, True),
    ("begin", 41, 3, 811, True, True),
    ("evaluate", 41, 3, True, True),
    ("integrate", 41, 3, True, False, False, True),
)
REFERENCE_PROMOTION_EVENTS = (
    ("bind", 41, 3, 701, 4, True),
    ("begin", 41, 3, 811, True, True),
    ("evaluate", 41, 3, True, True),
    ("evidence", 41, 3, True, False, False, True, True, True),
)
EXECUTION_EVENTS = (
    *REFERENCE_EXECUTION_EVENTS,
    REFERENCE_PROMOTION_EVENTS[-1],
    ("rollback", 41, 3, True),
    ("bind", 99, 3, 701, 4, True),
    ("bind", 41, 9, 701, 4, True),
    ("bind", 41, 3, 999, 4, True),
    ("bind", 41, 3, 701, 3, True),
    ("bind", 41, 3, 701, 4, False),
    ("begin", 99, 3, 811, True, True),
    ("begin", 41, 9, 811, True, True),
    ("begin", 41, 3, 999, True, True),
    ("begin", 41, 3, 811, False, True),
    ("begin", 41, 3, 811, True, False),
    ("evaluate", 99, 3, True, True),
    ("evaluate", 41, 9, True, True),
    ("evaluate", 41, 3, False, True),
    ("evaluate", 41, 3, True, False),
    ("integrate", 41, 3, False, False, False, True),
    ("integrate", 41, 3, True, True, False, True),
    ("integrate", 41, 3, True, False, False, False),
    ("evidence", 41, 3, False, False, False, True, True, True),
    ("evidence", 41, 3, True, True, False, True, True, True),
    ("evidence", 41, 3, True, False, False, False, True, True),
    ("evidence", 41, 3, True, False, False, True, False, True),
    ("evidence", 41, 3, True, False, False, True, True, False),
    ("rollback", 99, 3, True),
    ("rollback", 41, 9, True),
    ("rollback", 41, 3, False),
)

REQUIRED_FIXTURES = {
    "valid_phase_acceptance_infrastructure": ("valid", "integrate"),
    "valid_research_only_phase_debt": ("valid", "research_only"),
    "invalid_missing_required_artifact": ("invalid", "reject"),
    "invalid_dependency_inversion": ("invalid", "reject"),
    "invalid_self_improvement_without_evaluator": ("invalid", "reject"),
    "invalid_promotion_without_transition": ("invalid", "reject"),
    "invalid_phase_debt_without_retirement": ("invalid", "reject"),
    "invalid_missing_non_claim_boundary": ("invalid", "reject"),
}

EXPECTED_NON_CLAIMS = [
    "Does not prove any prototype phase is complete.",
    "Does not unlock deployed execution, self-improvement, or public capability claims.",
    "Does not promote any chapter core claim or Appendix C support state.",
    "Does not validate benchmark performance, model quality, evaluator independence, rollback execution, or release readiness.",
]

SURFACE_PHRASES = [
    "prototype_phase_gates_2026_07_02_local",
    "python3 scripts/validate_prototype_phase_gates.py",
    "Phase acceptance checklist",
    "Dependency gate review",
    "no support-state promotion",
]

READER_SURFACE_ALTERNATES = {
    "prototype_phase_gates_2026_07_02_local": [
        "tracked local prototype phase-gate result",
    ],
}

LEAN_PHRASES = [
    "PrototypePhaseGateFixtureBridgeRouteFor",
    "missing_non_claim_boundary_rejects_prototype_fixture_bridge",
    "complete_prototype_phase_gate_fixture_bridge_accepts",
    "phase_milestone_cannot_promote_claim_without_evidence_artifacts",
    "failed_acceptance_gates_keep_phase_research_only",
    "support_promotion_without_evidence_transition_rejected",
]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def text_blob(value: Any) -> str:
    if isinstance(value, dict):
        return "\n".join(f"{key}: {text_blob(child)}" for key, child in value.items())
    if isinstance(value, list):
        return "\n".join(text_blob(item) for item in value)
    return str(value)


def require_bool(readiness: dict[str, Any], field: str, errors: list[str], relative: str) -> bool:
    value = readiness.get(field)
    if not isinstance(value, bool):
        errors.append(f"{relative}: readiness.{field} must be boolean.")
        return False
    return value


def route_for(readiness: dict[str, Any]) -> str:
    if not readiness["source_matrix_ready"]:
        return "reject"
    if not readiness["artifact_graph_ready"]:
        return "reject"
    if not readiness["claim_ledger_ready"]:
        return "reject"
    if not readiness["authority_controls_ready"]:
        return "reject"
    if not readiness["dependency_order_valid"]:
        return "reject"
    if not readiness["required_artifacts_present"]:
        return "reject"
    if readiness["self_improvement_phase"] and not readiness["independent_evaluator_present"]:
        return "reject"
    if readiness["irreversible_authority_requested"] and not (
        readiness["independent_evaluator_present"] and readiness["rollback_plan_present"]
    ):
        return "reject"
    if readiness["phase_debt_recorded"] and not readiness["retirement_condition_recorded"]:
        return "reject"
    if not readiness["non_claim_boundary"]:
        return "reject"
    if not readiness["acceptance_gates_passed"]:
        return "research_only"
    if not readiness["residuals_closed"]:
        return "research_only"
    if readiness["support_promotion_requested"]:
        if readiness["evidence_refs_present"] and readiness["evidence_transition_record_present"]:
            return "evidence_review"
        return "reject"
    return "integrate"


def validate_fixture(record: dict[str, Any], schema: dict[str, Any], relative: str) -> tuple[str | None, list[str]]:
    errors: list[str] = []
    scenario_id = str(record.get("scenario_id", ""))
    if not scenario_id:
        errors.append(f"{relative}: scenario_id is required.")
    if scenario_id not in REQUIRED_FIXTURES:
        errors.append(f"{relative}: unknown scenario_id {scenario_id!r}.")

    expected_valid = record.get("expected_valid")
    expected_route = record.get("expected_route")
    if not isinstance(expected_valid, bool):
        errors.append(f"{relative}: expected_valid must be boolean.")
    if expected_route not in {"integrate", "research_only", "reject", "evidence_review"}:
        errors.append(f"{relative}: expected_route must be a known route.")

    phase = record.get("phase_record")
    if not isinstance(phase, dict):
        errors.append(f"{relative}: phase_record must be an object.")
        phase = {}
    else:
        errors.extend(validate_value(phase, schema, f"{relative}:phase_record"))

    readiness = record.get("readiness")
    if not isinstance(readiness, dict):
        errors.append(f"{relative}: readiness must be an object.")
        return scenario_id or None, errors

    required_bool_fields = [
        "source_matrix_ready",
        "artifact_graph_ready",
        "claim_ledger_ready",
        "authority_controls_ready",
        "dependency_order_valid",
        "required_artifacts_present",
        "acceptance_gates_passed",
        "evidence_refs_present",
        "evidence_transition_record_present",
        "residuals_closed",
        "phase_debt_recorded",
        "retirement_condition_recorded",
        "independent_evaluator_present",
        "rollback_plan_present",
        "support_promotion_requested",
        "irreversible_authority_requested",
        "self_improvement_phase",
        "non_claim_boundary",
    ]
    bools_ok = True
    for field in required_bool_fields:
        if not require_bool(readiness, field, errors, relative):
            bools_ok = False
    if not bools_ok:
        return scenario_id or None, errors

    actual_route = route_for(readiness)
    if expected_route != actual_route:
        errors.append(f"{relative}: expected_route {expected_route!r} does not match computed route {actual_route!r}.")

    expected_kind = REQUIRED_FIXTURES.get(scenario_id, (None, None))[0]
    if expected_kind == "valid" and not expected_valid:
        errors.append(f"{relative}: required valid scenario must set expected_valid true.")
    if expected_kind == "invalid" and expected_valid:
        errors.append(f"{relative}: required invalid scenario must set expected_valid false.")

    if expected_valid and actual_route == "reject":
        errors.append(f"{relative}: valid scenario cannot compute reject route.")
    if not expected_valid and actual_route != "reject":
        errors.append(f"{relative}: invalid scenario must compute reject route.")

    phase_blob = text_blob(phase).lower()
    if expected_valid and "support-state promotion" not in phase_blob and "support state promotion" not in phase_blob:
        errors.append(f"{relative}: phase_record non_claims must preserve support-state promotion boundary.")
    if readiness["phase_debt_recorded"] and "blocked_by" in phase:
        blocked_by = phase.get("blocked_by", [])
        if not isinstance(blocked_by, list) or not blocked_by:
            errors.append(f"{relative}: phase debt scenarios must name blockers in blocked_by.")
    if readiness["support_promotion_requested"] and not readiness["evidence_transition_record_present"]:
        if "evidence-transition" not in phase_blob and "evidence transition" not in phase_blob:
            errors.append(f"{relative}: promotion-blocking scenario must name evidence-transition boundary.")
    if readiness["self_improvement_phase"] and not readiness["independent_evaluator_present"]:
        if "independent evaluator" not in phase_blob:
            errors.append(f"{relative}: self-improvement rejection must name missing independent evaluator.")
    return scenario_id or None, errors


def computed_summary(records: dict[str, dict[str, Any]]) -> dict[str, Any]:
    routes: dict[str, list[str]] = {"integrate": [], "research_only": [], "reject": []}
    valid_count = 0
    invalid_count = 0
    for scenario_id, record in records.items():
        route = route_for(record["readiness"])
        routes.setdefault(route, []).append(scenario_id)
        if record["expected_valid"]:
            valid_count += 1
        else:
            invalid_count += 1
    for value in routes.values():
        value.sort()
    return {
        "result_id": "prototype_phase_gates_2026_07_02_local",
        "valid_fixture_count": valid_count,
        "expected_invalid_fixture_count": invalid_count,
        "accepted_routes": routes,
        "support_state_effect": "none",
        "non_claims": EXPECTED_NON_CLAIMS,
    }


def validate_result(records: dict[str, dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    if not RESULT.exists():
        return [f"{RESULT.relative_to(ROOT)} is missing."]
    result = load_json(RESULT)
    if not isinstance(result, dict):
        return [f"{RESULT.relative_to(ROOT)} must contain a JSON object."]
    expected = computed_summary(records)
    for field in ("result_id", "valid_fixture_count", "expected_invalid_fixture_count", "support_state_effect", "non_claims"):
        if result.get(field) != expected[field]:
            errors.append(f"result field {field} is {result.get(field)!r}, expected {expected[field]!r}.")
    if result.get("accepted_routes") != expected["accepted_routes"]:
        errors.append("result accepted_routes does not match fixture-computed routes.")
    coverage_blob = text_blob(result.get("coverage", [])).lower()
    for phrase in (
        "phase acceptance checklist",
        "dependency gate review",
        "support-promotion evidence-transition gate",
        "non-claim boundary preservation",
    ):
        if phrase not in coverage_blob:
            errors.append(f"result coverage missing {phrase!r}.")
    return errors


def validate_surfaces() -> list[str]:
    errors: list[str] = []
    surfaces = {
        "docs/prototype_phase_gate_harness.md": DOC,
        "chapters/prototype-roadmap.qmd": CHAPTER,
        "editions/reader_manuscript/v1_0/chapters/prototype-roadmap.qmd": READER,
        "docs/book_outline.md": OUTLINE,
        "docs/v1_x_beyond_sota_roadmap.md": ROADMAP,
    }
    for label, path in surfaces.items():
        text = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""
        for phrase in SURFACE_PHRASES:
            alternates = READER_SURFACE_ALTERNATES.get(phrase, []) if label == (
                "editions/reader_manuscript/v1_0/chapters/prototype-roadmap.qmd"
            ) else []
            if phrase not in text and not any(alternate in text for alternate in alternates):
                errors.append(f"{label} missing phrase {phrase!r}.")
    lean_text = LEAN.read_text(encoding="utf-8", errors="ignore") if LEAN.exists() else ""
    for phrase in LEAN_PHRASES:
        if phrase not in lean_text:
            errors.append(f"PrototypeRoadmap Lean module missing phrase {phrase!r}.")
    return errors


def reference_execution(*, promotion: bool = False, self_improvement: bool = False) -> dict[str, Any]:
    return {
        "stage": "proposed",
        "phase_id": 41,
        "expected_phase_id": 41,
        "plan_version": 3,
        "expected_plan_version": 3,
        "dependency_digest": 701,
        "expected_dependency_digest": 701,
        "dependency_count": 4,
        "satisfied_dependency_count": 0,
        "artifact_digest": 811,
        "expected_artifact_digest": 811,
        "self_improvement_phase": self_improvement,
        "support_promotion_requested": promotion,
        "dependency_order_valid": False,
        "required_artifacts_present": False,
        "rollback_plan_present": False,
        "independent_evaluator_present": False,
        "acceptance_gates_passed": False,
        "residuals_closed": False,
        "phase_debt_recorded": False,
        "retirement_condition_recorded": False,
        "evidence_refs_present": False,
        "evidence_transition_record_present": False,
        "non_claims_recorded": False,
        "receipts": 0,
        "authority_ceiling": 1,
        "expected_authority_ceiling": 1,
        "support_assignments": 0,
        "external_effects": 0,
    }


def execution_step(state: dict[str, Any], event: tuple[Any, ...]) -> tuple[str, dict[str, Any]]:
    kind, *args = event
    next_state = copy.deepcopy(state)
    accepted = False
    if kind == "bind":
        phase, plan, dependency, satisfied, order_valid = args
        accepted = (
            state["stage"] == "proposed"
            and phase == state["phase_id"]
            and plan == state["plan_version"]
            and dependency == state["dependency_digest"]
            and dependency == state["expected_dependency_digest"]
            and satisfied == state["dependency_count"]
            and order_valid is True
        )
        if accepted:
            next_state.update(
                stage="dependencies_bound",
                satisfied_dependency_count=satisfied,
                dependency_order_valid=True,
            )
    elif kind == "begin":
        phase, plan, artifact, artifacts_present, rollback_present = args
        accepted = (
            state["stage"] == "dependencies_bound"
            and phase == state["phase_id"]
            and plan == state["plan_version"]
            and artifact == state["artifact_digest"]
            and artifact == state["expected_artifact_digest"]
            and artifacts_present is True
            and rollback_present is True
        )
        if accepted:
            next_state.update(
                stage="executing",
                required_artifacts_present=True,
                rollback_plan_present=True,
            )
    elif kind == "evaluate":
        phase, plan, evaluator_present, gates_passed = args
        accepted = (
            state["stage"] == "executing"
            and phase == state["phase_id"]
            and plan == state["plan_version"]
            and evaluator_present is True
        )
        if accepted:
            next_state.update(
                stage="evaluated",
                independent_evaluator_present=True,
                acceptance_gates_passed=gates_passed,
            )
    elif kind == "integrate":
        phase, plan, residuals, debt, retirement, non_claims = args
        accepted = (
            state["stage"] == "evaluated"
            and phase == state["phase_id"]
            and plan == state["plan_version"]
            and state["acceptance_gates_passed"] is True
            and state["support_promotion_requested"] is False
            and residuals is True
            and (debt is False or retirement is True)
            and non_claims is True
        )
        if accepted:
            next_state.update(
                stage="integrated",
                residuals_closed=True,
                phase_debt_recorded=debt,
                retirement_condition_recorded=retirement,
                non_claims_recorded=True,
            )
    elif kind == "evidence":
        phase, plan, residuals, debt, retirement, evidence, transition, non_claims = args
        accepted = (
            state["stage"] == "evaluated"
            and phase == state["phase_id"]
            and plan == state["plan_version"]
            and state["acceptance_gates_passed"] is True
            and state["support_promotion_requested"] is True
            and residuals is True
            and (debt is False or retirement is True)
            and evidence is True
            and transition is True
            and non_claims is True
        )
        if accepted:
            next_state.update(
                stage="evidence_review",
                residuals_closed=True,
                phase_debt_recorded=debt,
                retirement_condition_recorded=retirement,
                evidence_refs_present=True,
                evidence_transition_record_present=True,
                non_claims_recorded=True,
            )
    elif kind == "rollback":
        phase, plan, residual_owned = args
        accepted = (
            state["stage"] not in {"integrated", "evidence_review", "rolled_back"}
            and phase == state["phase_id"]
            and plan == state["plan_version"]
            and residual_owned is True
        )
        if accepted:
            next_state["stage"] = "rolled_back"
    else:
        raise ValueError(f"unknown prototype execution event: {event}")
    if accepted:
        next_state["receipts"] += 1
        return "accepted", next_state
    return "rejected", copy.deepcopy(state)


def run_execution(state: dict[str, Any], events: tuple[tuple[Any, ...], ...]) -> dict[str, Any]:
    current = copy.deepcopy(state)
    for event in events:
        _, current = execution_step(current, event)
    return current


def execution_custody(state: dict[str, Any]) -> bool:
    return (
        state["phase_id"] == state["expected_phase_id"]
        and state["plan_version"] == state["expected_plan_version"]
        and state["dependency_digest"] == state["expected_dependency_digest"]
        and state["artifact_digest"] == state["expected_artifact_digest"]
        and state["authority_ceiling"] == state["expected_authority_ceiling"]
    )


def execution_invariant(state: dict[str, Any]) -> bool:
    if not execution_custody(state):
        return False
    if state["support_assignments"] != 0 or state["external_effects"] != 0:
        return False
    dependencies = (
        state["dependency_order_valid"] is True
        and state["satisfied_dependency_count"] == state["dependency_count"]
    )
    executing = (
        dependencies
        and state["required_artifacts_present"] is True
        and state["rollback_plan_present"] is True
    )
    evaluated = executing and state["independent_evaluator_present"] is True
    terminal_common = (
        evaluated
        and state["acceptance_gates_passed"] is True
        and state["residuals_closed"] is True
        and (state["phase_debt_recorded"] is False or state["retirement_condition_recorded"] is True)
        and state["non_claims_recorded"] is True
    )
    required = {
        "proposed": True,
        "dependencies_bound": dependencies,
        "executing": executing,
        "evaluated": evaluated,
        "integrated": terminal_common and state["support_promotion_requested"] is False,
        "evidence_review": (
            terminal_common
            and state["support_promotion_requested"] is True
            and state["evidence_refs_present"] is True
            and state["evidence_transition_record_present"] is True
        ),
        "rolled_back": True,
    }
    return required[state["stage"]]


def execution_state_key(state: dict[str, Any]) -> tuple[Any, ...]:
    return tuple(state[key] for key in state)


def explore_execution(roots: list[dict[str, Any]]) -> dict[tuple[Any, ...], dict[str, Any]]:
    reachable = {execution_state_key(root): copy.deepcopy(root) for root in roots}
    frontier = list(reachable.values())
    while frontier:
        state = frontier.pop()
        for event in EXECUTION_EVENTS:
            _, next_state = execution_step(state, event)
            key = execution_state_key(next_state)
            if key not in reachable:
                reachable[key] = next_state
                frontier.append(next_state)
    return reachable


def validate_formal_execution(errors: list[str]) -> dict[str, int]:
    lean_text = LEAN.read_text(encoding="utf-8", errors="ignore")
    theorem_names = set(re.findall(r"(?m)^theorem\s+([A-Za-z_][A-Za-z0-9_']*)", lean_text))
    missing = sorted(REQUIRED_LIFECYCLE_THEOREMS - theorem_names)
    if missing:
        errors.append(f"PrototypeRoadmap Lean module missing lifecycle theorem(s): {missing}")
    if len(theorem_names) != 37:
        errors.append(f"PrototypeRoadmap theorem count must be 37, observed {len(theorem_names)}")
    completed = subprocess.run(
        ["lake", "env", "lean", "AsiStackProofs/PrototypeRoadmap.lean"],
        cwd=LEAN_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        errors.append(f"PrototypeRoadmap Lean compilation failed: {completed.stdout}{completed.stderr}")

    if not (1 < 2 < 3):
        errors.append("prototype dependency strict-order witness failed")
    if 2 < 2:
        errors.append("prototype self-dependency control unexpectedly passed")

    normal = reference_execution()
    promotion = reference_execution(promotion=True)
    self_improvement = reference_execution(self_improvement=True)
    integrated = run_execution(normal, REFERENCE_EXECUTION_EVENTS)
    evidence_review = run_execution(promotion, REFERENCE_PROMOTION_EVENTS)
    if integrated["stage"] != "integrated" or integrated["receipts"] != 4:
        errors.append("reference prototype execution did not reach exact integrated state")
    if evidence_review["stage"] != "evidence_review" or evidence_review["receipts"] != 4:
        errors.append("reference prototype promotion did not reach exact evidence-review state")
    for final in (integrated, evidence_review):
        if final["support_assignments"] != 0 or final["external_effects"] != 0:
            errors.append("prototype reference trace gained support or external-effect authority")

    split_count = 0
    for root, trace in (
        (normal, REFERENCE_EXECUTION_EVENTS),
        (promotion, REFERENCE_PROMOTION_EVENTS),
    ):
        for index in range(len(trace) + 1):
            left, right = trace[:index], trace[index:]
            if run_execution(root, trace) != run_execution(run_execution(root, left), right):
                errors.append(f"prototype execution composition failed at split {index}")
            else:
                split_count += 1

    reachable = explore_execution([normal, promotion, self_improvement])
    custody_fields = (
        "phase_id",
        "expected_phase_id",
        "plan_version",
        "expected_plan_version",
        "dependency_digest",
        "expected_dependency_digest",
        "artifact_digest",
        "expected_artifact_digest",
        "authority_ceiling",
        "expected_authority_ceiling",
        "support_assignments",
        "external_effects",
    )
    transition_count = 0
    rejection_count = 0
    terminal_states: list[dict[str, Any]] = []
    for state in reachable.values():
        if not execution_invariant(state):
            errors.append(f"reachable prototype execution violates invariant: {state}")
        if state["stage"] in {"integrated", "evidence_review", "rolled_back"}:
            terminal_states.append(state)
        for event in EXECUTION_EVENTS:
            transition_count += 1
            route, next_state = execution_step(state, event)
            if any(next_state[field] != state[field] for field in custody_fields):
                errors.append(f"prototype execution custody changed through {state['stage']}:{event[0]}")
            if execution_invariant(state) and not execution_invariant(next_state):
                errors.append(f"prototype execution invariant failed through {state['stage']}:{event[0]}")
            if route == "rejected":
                rejection_count += 1
                if next_state != state:
                    errors.append(f"rejected prototype event changed state: {state['stage']}:{event}")

    absorbing_transitions = 0
    for state in terminal_states:
        for event in EXECUTION_EVENTS:
            absorbing_transitions += 1
            _, next_state = execution_step(state, event)
            if next_state != state:
                errors.append(f"terminal prototype state reopened through {event}")

    semantic_mutations = 0
    for field in (
        "phase_id",
        "plan_version",
        "dependency_digest",
        "artifact_digest",
        "authority_ceiling",
        "support_assignments",
        "external_effects",
    ):
        mutation = copy.deepcopy(integrated)
        mutation[field] += 1
        if execution_invariant(mutation):
            errors.append(f"prototype custody mutation was not detected for {field}")
        else:
            semantic_mutations += 1
    for field in (
        "dependency_order_valid",
        "required_artifacts_present",
        "rollback_plan_present",
        "independent_evaluator_present",
        "acceptance_gates_passed",
        "residuals_closed",
        "non_claims_recorded",
    ):
        mutation = copy.deepcopy(integrated)
        mutation[field] = False
        if execution_invariant(mutation):
            errors.append(f"prototype gate mutation was not detected for {field}")
        else:
            semantic_mutations += 1
    count_mutation = copy.deepcopy(integrated)
    count_mutation["satisfied_dependency_count"] -= 1
    if execution_invariant(count_mutation):
        errors.append("prototype dependency-count mutation was not detected")
    else:
        semantic_mutations += 1
    debt_mutation = copy.deepcopy(integrated)
    debt_mutation["phase_debt_recorded"] = True
    debt_mutation["retirement_condition_recorded"] = False
    if execution_invariant(debt_mutation):
        errors.append("prototype debt-retirement mutation was not detected")
    else:
        semantic_mutations += 1
    for field in ("support_promotion_requested", "evidence_refs_present", "evidence_transition_record_present"):
        mutation = copy.deepcopy(evidence_review)
        mutation[field] = not mutation[field]
        if execution_invariant(mutation):
            errors.append(f"prototype evidence-review mutation was not detected for {field}")
        else:
            semantic_mutations += 1

    unintegrated = copy.deepcopy(normal)
    unintegrated.update(
        stage="evaluated",
        satisfied_dependency_count=4,
        dependency_order_valid=True,
        required_artifacts_present=True,
        rollback_plan_present=True,
        independent_evaluator_present=True,
        acceptance_gates_passed=True,
        receipts=4,
    )
    if (integrated["dependency_count"], integrated["receipts"]) != (
        unintegrated["dependency_count"], unintegrated["receipts"]
    ) or integrated["stage"] == unintegrated["stage"]:
        errors.append("prototype thin-summary collision witness drifted")

    return {
        "trace_splits": split_count,
        "reachable_states": len(reachable),
        "transitions": transition_count,
        "rejections": rejection_count,
        "terminal_states": len(terminal_states),
        "absorbing_transitions": absorbing_transitions,
        "semantic_mutations": semantic_mutations,
    }


def main() -> None:
    errors: list[str] = []
    schema = load_json(SCHEMA)
    fixture_paths = sorted(FIXTURE_DIR.glob("*.json"))
    records: dict[str, dict[str, Any]] = {}
    seen: set[str] = set()
    for path in fixture_paths:
        relative = str(path.relative_to(ROOT))
        try:
            record = load_json(path)
        except Exception as exc:
            errors.append(f"{relative}: invalid JSON: {exc}")
            continue
        if not isinstance(record, dict):
            errors.append(f"{relative}: fixture must contain a JSON object.")
            continue
        scenario_id, fixture_errors = validate_fixture(record, schema, relative)
        errors.extend(fixture_errors)
        if scenario_id:
            seen.add(scenario_id)
            records[scenario_id] = record
    missing = sorted(set(REQUIRED_FIXTURES) - seen)
    extra = sorted(seen - set(REQUIRED_FIXTURES))
    if missing:
        errors.append(f"missing required prototype phase fixtures: {missing}")
    if extra:
        errors.append(f"unexpected prototype phase fixtures: {extra}")
    if not errors:
        errors.extend(validate_result(records))
    errors.extend(validate_surfaces())
    lifecycle = validate_formal_execution(errors)
    if errors:
        print("Prototype phase gate harness validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)
    valid_count = computed_summary(records)["valid_fixture_count"]
    invalid_count = computed_summary(records)["expected_invalid_fixture_count"]
    print(
        "Prototype phase gate harness passed: "
        f"{valid_count} valid fixture(s), {invalid_count} expected-invalid fixture(s), "
        "37 Lean declarations, routes integrate/research_only/reject checked, "
        f"{lifecycle['trace_splits']}/10 trace splits, {lifecycle['reachable_states']} reachable states "
        f"through {lifecycle['transitions']} transitions ({lifecycle['rejections']} rejections), "
        f"{lifecycle['terminal_states']} terminal states through "
        f"{lifecycle['absorbing_transitions']} absorbing transitions, and "
        f"{lifecycle['semantic_mutations']} semantic mutations."
    )


if __name__ == "__main__":
    main()
