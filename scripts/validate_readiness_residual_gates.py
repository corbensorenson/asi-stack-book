#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

from validate_protocol_examples import validate_value

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "experiments" / "readiness_residual_gates" / "fixtures"

SCHEMAS = {
    "readiness_gate_record": ROOT / "schemas" / "readiness_gate_record.schema.json",
    "costed_route_record": ROOT / "schemas" / "costed_route_record.schema.json",
    "replacement_transaction": ROOT / "schemas" / "replacement_transaction.schema.json",
}

AUTHORITY_RANK = {
    "public_read": 1,
    "public_transform": 2,
    "tracked_file_write": 3,
    "external_effect": 4,
    "restricted_source": 5,
    "secret": 6,
}
READY_EVIDENCE_STATES = {"fixture_validated", "locally_reproduced"}
PROMOTING_GATE_DECISIONS = {"canary", "qualify", "default"}
GOOD_ROUTE_OUTCOMES = {"adequate_minimum", "adequate_overkill"}
PROMOTION_ROUTE_EFFECTS = {"eligible_for_bounded_evidence_review"}
BAD_ROUTE_OUTCOMES = {"cheap_brittle", "hidden_cost", "unsafe_saving"}
BAD_RESULT_WORDS = {"fail", "failed", "blocked", "unsafe", "expired", "not_run", "not run"}
WEAK_APPROVALS = {"missing", "none", "not_required", "self_approved"}
WEAK_EVALUATOR_WORDS = {"self-evaluated", "same evaluator", "not independent", "marks its own"}
GATE_TO_REPLACEMENT_DECISIONS = {
    "reject": {"reject"},
    "quarantine": {"quarantine"},
    "shadow": {"reject", "canary"},
    "canary": {"canary"},
    "qualify": {"canary"},
    "default": {"commit"},
    "retire": {"retire"},
    "rerun": {"reject", "quarantine"},
}


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


def authority_rank(value: Any) -> int | None:
    return AUTHORITY_RANK.get(str(value))


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


def contains_bad_result(values: Any) -> bool:
    blob = text_blob(values)
    return any(word in blob for word in BAD_RESULT_WORDS)


def contains_token(values: Any, token: str) -> bool:
    return token in text_blob(values)


def schema_errors_for_scenario(value: dict[str, Any], schemas: dict[str, Any], relative: str) -> list[str]:
    errors: list[str] = []
    for field in ("readiness_gate_record", "costed_route_record", "replacement_transaction"):
        if field not in value:
            errors.append(f"{relative}: missing {field}.")
            continue
        errors.extend(validate_value(value[field], schemas[field], f"{relative}:{field}"))
    return errors


def route_errors(route: dict[str, Any], gate: dict[str, Any], relative: str) -> list[str]:
    errors: list[str] = []
    selected_route = str(route["selected_route"])
    fallback_route = str(route["fallback_route"])
    candidate_routes = {str(item) for item in route.get("candidate_routes", [])}
    allowed_routes = {str(item) for item in gate.get("allowed_routes", [])}
    blocked_routes = {str(item) for item in gate.get("blocked_routes", [])}

    for field in ("candidate_routes", "cost_classes", "hidden_cost_checks", "non_claims"):
        require_nonempty_list(route, field, errors, f"{relative}:costed_route_record")

    if selected_route not in candidate_routes:
        errors.append(f"{relative}: selected_route must be present in candidate_routes.")
    if fallback_route not in candidate_routes:
        errors.append(f"{relative}: fallback_route must be present in candidate_routes.")
    if selected_route in allowed_routes and selected_route in blocked_routes:
        errors.append(f"{relative}: selected_route cannot be both allowed and blocked by the readiness gate.")

    route_ready = (
        route["verification_result"] == "pass"
        and route["outcome_state"] in GOOD_ROUTE_OUTCOMES
        and not contains_bad_result(route.get("hidden_cost_checks", []))
    )
    if route.get("promotion_candidate"):
        if not route_ready:
            errors.append(f"{relative}: promotion_candidate route requires pass verification, adequate outcome, and no failed hidden-cost checks.")
        if route["support_state_effect"] not in PROMOTION_ROUTE_EFFECTS:
            errors.append(f"{relative}: promotion_candidate route requires eligible_for_bounded_evidence_review support_state_effect.")
    if route["verification_result"] in {"fail", "partial", "not_run"} or route["outcome_state"] in BAD_ROUTE_OUTCOMES:
        if route.get("promotion_candidate"):
            errors.append(f"{relative}: failed, partial, not-run, or unsafe route cannot be a promotion_candidate.")
        if gate["decision"] in PROMOTING_GATE_DECISIONS:
            errors.append(f"{relative}: readiness gate cannot promote a failed, partial, not-run, or unsafe route.")

    if gate["decision"] in PROMOTING_GATE_DECISIONS:
        if selected_route not in allowed_routes:
            errors.append(f"{relative}: promoting gate decision requires selected_route in allowed_routes.")
        if selected_route in blocked_routes:
            errors.append(f"{relative}: promoting gate decision cannot use a blocked selected_route.")
    if gate["decision"] == "quarantine":
        if selected_route not in blocked_routes:
            errors.append(f"{relative}: quarantine decision must put selected_route in blocked_routes.")
        if fallback_route not in allowed_routes:
            errors.append(f"{relative}: quarantine decision must keep fallback_route in allowed_routes.")

    return errors


def gate_errors(gate: dict[str, Any], route: dict[str, Any], replacement: dict[str, Any], relative: str) -> list[str]:
    errors: list[str] = []
    for field in (
        "gate_evidence",
        "floor_evidence",
        "regression_results",
        "allowed_routes",
        "diagnostic_permissions",
        "closure_conditions",
        "review_refs",
        "non_claims",
    ):
        require_nonempty_list(gate, field, errors, f"{relative}:readiness_gate_record")

    if gate["field_id"] != replacement["field_id"]:
        errors.append(f"{relative}: readiness gate field_id must match replacement transaction field_id.")
    if gate["target_kind"] == "field_implementation" and gate["target_id"] != replacement["candidate_implementation"]:
        errors.append(f"{relative}: field_implementation target_id must match replacement candidate_implementation.")

    gate_auth = authority_rank(gate["authority_scope"])
    route_auth = authority_rank(route["authority_ceiling"])
    if gate_auth is None:
        errors.append(f"{relative}: readiness gate authority_scope {gate['authority_scope']!r} is not one of {sorted(AUTHORITY_RANK)}.")
    if route_auth is None:
        errors.append(f"{relative}: route authority_ceiling {route['authority_ceiling']!r} is not one of {sorted(AUTHORITY_RANK)}.")
    if gate_auth is not None and route_auth is not None and route_auth > gate_auth:
        errors.append(f"{relative}: route authority_ceiling exceeds readiness gate authority_scope.")

    evidence_surface = text_blob(gate.get("gate_evidence", []), gate.get("review_refs", []), replacement.get("qualification_evidence", []))
    if str(route["task_id"]) not in evidence_surface:
        errors.append(f"{relative}: route task_id must be referenced by gate evidence, review refs, or replacement qualification evidence.")

    residual_obligations = {str(item) for item in route.get("residual_obligations", [])}
    inherited_residuals = {str(item) for item in gate.get("inherited_residuals", [])}
    gate_escrow = {str(item) for item in gate.get("residual_escrow", [])}
    replacement_escrow = {str(item) for item in replacement.get("residual_escrow", [])}
    promotion_blockers = {str(item) for item in gate.get("promotion_blockers", [])}
    escrow_or_blockers = gate_escrow | replacement_escrow | promotion_blockers
    missing_route_residuals = sorted(residual_obligations - escrow_or_blockers)
    if missing_route_residuals:
        errors.append(f"{relative}: route residual obligations are not covered by gate/replacement escrow or promotion blockers: {missing_route_residuals}.")
    missing_inherited_residuals = sorted(inherited_residuals - (gate_escrow | replacement_escrow))
    if missing_inherited_residuals and gate["decision"] in PROMOTING_GATE_DECISIONS:
        errors.append(f"{relative}: promoting gate decision must carry inherited residuals into escrow: {missing_inherited_residuals}.")

    if gate["decision"] in PROMOTING_GATE_DECISIONS:
        if gate["evidence_state"] not in READY_EVIDENCE_STATES:
            errors.append(f"{relative}: promoting gate decision requires fixture_validated or locally_reproduced evidence_state.")
        if contains_bad_result(gate.get("floor_evidence", [])) or contains_bad_result(gate.get("regression_results", [])):
            errors.append(f"{relative}: promoting gate decision cannot carry failed floor or regression evidence.")
        if contains_token([gate["freshness_window"], gate["expiry"]], "expired") or contains_token([gate["freshness_window"], gate["expiry"]], "stale"):
            errors.append(f"{relative}: promoting gate decision cannot rely on expired or stale freshness/expiry text.")
        if residual_obligations and not gate.get("residual_escrow"):
            errors.append(f"{relative}: promoting gate decision with route residuals requires residual_escrow.")
        if gate["promotion_blockers"] and gate["decision"] in {"qualify", "default"}:
            errors.append(f"{relative}: qualify/default decision cannot carry promotion_blockers.")
        if gate["decision"] == "default":
            if gate["candidate_state"] != "default":
                errors.append(f"{relative}: default decision requires candidate_state == default.")
            if gate["promotion_blockers"]:
                errors.append(f"{relative}: default decision cannot carry promotion_blockers.")
            require_nonempty_list(gate, "frontier_evidence", errors, f"{relative}:readiness_gate_record")
    if gate["evidence_state"] in {"not_run", "source_reported", "expired", "blocked"} and gate["decision"] in PROMOTING_GATE_DECISIONS:
        errors.append(f"{relative}: non-ready evidence_state cannot support canary, qualify, or default decisions.")
    if gate["decision"] == "quarantine":
        if gate["candidate_state"] != "quarantined":
            errors.append(f"{relative}: quarantine decision requires candidate_state == quarantined.")
        require_nonempty_list(gate, "quarantine_conditions", errors, f"{relative}:readiness_gate_record")
    if gate["decision"] == "rerun" and gate["evidence_state"] not in {"expired", "not_run", "blocked", "source_reported"}:
        errors.append(f"{relative}: rerun decision should preserve expired, not_run, blocked, or source_reported evidence_state.")

    return errors


def replacement_errors(replacement: dict[str, Any], gate: dict[str, Any], route: dict[str, Any], relative: str) -> list[str]:
    errors: list[str] = []
    for field in ("precheck_results", "qualification_evidence", "regression_results", "source_refs", "non_claims"):
        require_nonempty_list(replacement, field, errors, f"{relative}:replacement_transaction")

    allowed_decisions = GATE_TO_REPLACEMENT_DECISIONS[gate["decision"]]
    if replacement["decision"] not in allowed_decisions:
        errors.append(
            f"{relative}: replacement decision {replacement['decision']!r} is inconsistent with gate decision "
            f"{gate['decision']!r}; expected one of {sorted(allowed_decisions)}."
        )

    if str(gate["gate_id"]) not in text_blob(replacement.get("qualification_evidence", []), replacement.get("source_refs", [])):
        errors.append(f"{relative}: replacement qualification evidence or source refs must reference the readiness gate id.")
    if contains_bad_result(replacement.get("regression_results", [])) and replacement["decision"] in {"canary", "commit"}:
        errors.append(f"{relative}: replacement cannot canary or commit with failed regression results.")
    if any(word in text_blob(replacement["evaluator_independence"]) for word in WEAK_EVALUATOR_WORDS) and replacement["decision"] in {"canary", "commit"}:
        errors.append(f"{relative}: replacement canary/commit requires independent evaluator wording.")

    dry_run_status = replacement["rollback_receipt"]["dry_run_status"]
    if replacement["decision"] == "commit":
        if replacement["transaction_state"] != "committed":
            errors.append(f"{relative}: commit decision requires transaction_state == committed.")
        if dry_run_status != "pass":
            errors.append(f"{relative}: commit decision requires rollback dry_run_status == pass.")
        if replacement["monitor_status"] != "pass":
            errors.append(f"{relative}: commit decision requires monitor_status == pass.")
        if replacement["approval_record"].strip().lower() in WEAK_APPROVALS:
            errors.append(f"{relative}: commit decision requires a meaningful approval_record.")
        if replacement["promotion_blockers"]:
            errors.append(f"{relative}: commit decision cannot carry promotion_blockers.")
        if replacement["support_state_effect"] != "eligible_for_default_review":
            errors.append(f"{relative}: commit decision requires eligible_for_default_review support_state_effect.")
    if replacement["decision"] == "canary":
        if replacement["transaction_state"] not in {"canary", "default_candidate"}:
            errors.append(f"{relative}: canary decision requires transaction_state canary or default_candidate.")
        if dry_run_status != "pass":
            errors.append(f"{relative}: canary decision requires rollback dry_run_status == pass.")
        if replacement["monitor_status"] not in {"active", "pass"}:
            errors.append(f"{relative}: canary decision requires active or passing monitor_status.")
        if replacement["support_state_effect"] != "eligible_for_canary_review":
            errors.append(f"{relative}: canary decision requires eligible_for_canary_review support_state_effect.")
    if replacement["decision"] == "quarantine" and replacement["transaction_state"] != "quarantined":
        errors.append(f"{relative}: quarantine decision requires transaction_state == quarantined.")
    if replacement["decision"] == "reject" and replacement["transaction_state"] not in {"proposed", "precheck", "blocked"}:
        errors.append(f"{relative}: reject decision should remain proposed, precheck, or blocked.")

    if gate["decision"] in PROMOTING_GATE_DECISIONS:
        required_escrow = {str(item) for item in gate.get("residual_escrow", [])} | {str(item) for item in route.get("residual_obligations", [])}
        missing = sorted(required_escrow - {str(item) for item in replacement.get("residual_escrow", [])})
        if missing:
            errors.append(f"{relative}: promoting replacement must inherit gate and route residual escrow: {missing}.")

    return errors


def semantic_errors(value: dict[str, Any], relative: str) -> list[str]:
    errors: list[str] = []
    if not isinstance(value.get("scenario_id"), str) or not value["scenario_id"].strip():
        errors.append(f"{relative}: scenario_id must be a non-empty string.")
    require_nonempty_list(value, "non_claims", errors, relative)
    if errors:
        return errors

    gate = value["readiness_gate_record"]
    route = value["costed_route_record"]
    replacement = value["replacement_transaction"]

    errors.extend(route_errors(route, gate, relative))
    errors.extend(gate_errors(gate, route, replacement, relative))
    errors.extend(replacement_errors(replacement, gate, route, relative))
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
        raise SystemExit(f"No readiness/residual gate fixtures found in {FIXTURE_DIR.relative_to(ROOT)}.")

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
                errors.append(f"{relative}: invalid fixture unexpectedly passed readiness/residual gate checks.")

    if errors:
        print("Readiness/residual gate harness failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print(
        "Readiness/residual gate harness passed: "
        f"{valid_count} valid fixture(s), {invalid_count} expected-invalid fixture(s)."
    )


if __name__ == "__main__":
    main()
