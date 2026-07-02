#!/usr/bin/env python3
from __future__ import annotations

import json
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

LEAN_PHRASES = [
    "PrototypePhaseGateFixtureBridgeRouteFor",
    "missing_non_claim_boundary_rejects_prototype_fixture_bridge",
    "complete_prototype_phase_gate_fixture_bridge_accepts",
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
            if phrase not in text:
                errors.append(f"{label} missing phrase {phrase!r}.")
    lean_text = LEAN.read_text(encoding="utf-8", errors="ignore") if LEAN.exists() else ""
    for phrase in LEAN_PHRASES:
        if phrase not in lean_text:
            errors.append(f"PrototypeRoadmap Lean module missing phrase {phrase!r}.")
    return errors


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
        "routes integrate/research_only/reject checked."
    )


if __name__ == "__main__":
    main()
