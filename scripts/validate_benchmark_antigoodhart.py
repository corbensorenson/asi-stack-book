#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

from validate_protocol_examples import validate_value

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "experiments" / "benchmark_antigoodhart" / "fixtures"

SCHEMAS = {
    "benchmark_ratchet_record": ROOT / "schemas" / "benchmark_ratchet_record.schema.json",
    "policy_optimization_record": ROOT / "schemas" / "policy_optimization_record.schema.json",
    "steward_action_decision": ROOT / "schemas" / "steward_action_decision.schema.json",
}

PROMOTION_EFFECT = "eligible_for_bounded_evidence_review"
BLOCKING_EFFECTS = {"blocks_promotion", "argument_only", "record_shape_only", "none"}
PROMOTING_POLICY_STATES = {"canary", "promoted"}
RELEASE_ACTIONS = {"schedule_release", "open_pr"}
GOODHART_REQUIRED_CHECKS = ("holdout", "contamination")
GOODHART_REQUIRED_ONE_OF = ("mutation", "transfer")
BAD_CHECK_WORDS = {"failed", "contaminated", "leaked", "missing", "unchecked", "bypassed"}
BAD_REWARD_BOUNDARY_PHRASES = {
    "reward is truth",
    "reward equals truth",
    "score is truth",
    "score equals truth",
    "sole evidence",
    "only evidence",
    "stand in for authority",
    "stand in for truth",
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


def contains_all(blob: str, needles: tuple[str, ...]) -> bool:
    return all(needle in blob for needle in needles)


def schema_errors_for_scenario(value: dict[str, Any], schemas: dict[str, Any], relative: str) -> list[str]:
    errors: list[str] = []
    for field in ("benchmark_ratchet_record", "policy_optimization_record", "steward_action_decision"):
        if field not in value:
            errors.append(f"{relative}: missing {field}.")
            continue
        errors.extend(validate_value(value[field], schemas[field], f"{relative}:{field}"))
    return errors


def ratchet_is_promotion_ready(ratchet: dict[str, Any]) -> bool:
    checks = text_blob(ratchet.get("anti_goodhart_checks", []))
    bad_checks = any(word in checks for word in BAD_CHECK_WORDS)
    return (
        ratchet["promotion_decision"] == "promote"
        and ratchet["benchmark_state"] == "active"
        and ratchet["saturation_state"] == "not_saturated"
        and bool(ratchet.get("run_refs"))
        and bool(ratchet.get("baseline_refs"))
        and bool(ratchet.get("regression_refs"))
        and bool(ratchet.get("negative_results"))
        and ratchet["support_state_effect"] == PROMOTION_EFFECT
        and contains_all(checks, GOODHART_REQUIRED_CHECKS)
        and any(word in checks for word in GOODHART_REQUIRED_ONE_OF)
        and not bad_checks
    )


def ratchet_errors(ratchet: dict[str, Any], relative: str) -> list[str]:
    errors: list[str] = []
    for field in ("baseline_refs", "anti_goodhart_checks", "residual_escrow"):
        require_nonempty_list(ratchet, field, errors, f"{relative}:benchmark_ratchet_record")

    promoting = ratchet["promotion_decision"] == "promote"
    checks = text_blob(ratchet.get("anti_goodhart_checks", []))
    if promoting:
        if not ratchet_is_promotion_ready(ratchet):
            errors.append(
                f"{relative}: benchmark promotion requires active/not_saturated state, run refs, baselines, "
                "regression refs, negative-result retention, eligible support effect, holdout and "
                "contamination checks, a mutation or transfer check, and no failed anti-Goodhart checks."
            )
    if ratchet["saturation_state"] in {"saturated", "suspected", "unknown"} and promoting:
        errors.append(f"{relative}: saturated, suspected, or unknown saturation state cannot promote a benchmark claim.")
    if ratchet["benchmark_state"] in {"blocked", "retired"} and promoting:
        errors.append(f"{relative}: blocked or retired benchmark cannot promote a claim.")
    if any(word in checks for word in BAD_CHECK_WORDS) and promoting:
        errors.append(f"{relative}: failed or contaminated anti-Goodhart checks must block promotion.")
    if ratchet["promotion_decision"] == "regression_only":
        if ratchet["saturation_state"] != "saturated":
            errors.append(f"{relative}: regression_only decision requires saturation_state == saturated.")
        require_nonempty_list(ratchet, "regression_refs", errors, f"{relative}:benchmark_ratchet_record")
        if ratchet["support_state_effect"] == PROMOTION_EFFECT:
            errors.append(f"{relative}: regression_only benchmark cannot use eligible_for_bounded_evidence_review.")
    if ratchet["promotion_decision"] in {"block", "quarantine", "rerun"}:
        if ratchet["support_state_effect"] == PROMOTION_EFFECT:
            errors.append(f"{relative}: blocked, quarantined, or rerun benchmark cannot use promotion support effect.")
    return errors


def policy_errors(policy: dict[str, Any], ratchet: dict[str, Any], relative: str) -> list[str]:
    errors: list[str] = []
    for field in ("verifier_refs", "reward_hacking_probes", "holdout_refs", "regression_refs", "evaluation_refs", "governance_gate_refs", "residuals", "non_claims"):
        require_nonempty_list(policy, field, errors, f"{relative}:policy_optimization_record")

    ratchet_id = str(ratchet["ratchet_id"])
    policy_promotes = policy["promotion_decision"] == "promote" or policy["update_state"] in PROMOTING_POLICY_STATES
    if policy_promotes:
        if not ratchet_is_promotion_ready(ratchet):
            errors.append(f"{relative}: policy promotion requires a promotion-ready benchmark ratchet.")
        if ratchet_id not in {str(item) for item in policy.get("evidence_packet_refs", [])}:
            errors.append(f"{relative}: policy promotion requires evidence_packet_refs to include the benchmark ratchet id.")
        if policy["measurement_status"] != "run":
            errors.append(f"{relative}: policy promotion requires measurement_status == run.")
        if policy["training_mode"] == "not_run":
            errors.append(f"{relative}: policy promotion requires a training or update mode other than not_run.")
        if policy["feedback_admissibility"] not in {"admissible_for_training", "admissible_for_canary"}:
            errors.append(f"{relative}: policy promotion requires training/canary-admissible feedback.")
        if policy["authority_effect"] in {"blocked", "not_evaluated"}:
            errors.append(f"{relative}: policy promotion cannot have blocked or not_evaluated authority_effect.")
        if policy["support_state_effect"] != PROMOTION_EFFECT:
            errors.append(f"{relative}: policy promotion requires eligible_for_bounded_evidence_review support_state_effect.")

    reward_boundary = text_blob(policy["reward_boundary"])
    if any(phrase in reward_boundary for phrase in BAD_REWARD_BOUNDARY_PHRASES) and policy_promotes:
        errors.append(f"{relative}: policy promotion cannot treat reward or score as truth, sole evidence, or authority.")
    if policy["support_state_effect"] == PROMOTION_EFFECT and not policy_promotes:
        errors.append(f"{relative}: eligible support effect must be tied to canary/promoted policy state.")
    if ratchet["promotion_decision"] in {"block", "quarantine", "regression_only", "rerun"} and policy["promotion_decision"] == "promote":
        errors.append(f"{relative}: policy cannot promote from blocked, quarantined, rerun, or regression-only ratchet evidence.")
    return errors


def steward_errors(steward: dict[str, Any], ratchet: dict[str, Any], policy: dict[str, Any], relative: str) -> list[str]:
    errors: list[str] = []
    for field in ("inputs", "evidence_refs", "affected_artifacts", "residuals", "non_claims"):
        require_nonempty_list(steward, field, errors, f"{relative}:steward_action_decision")

    ratchet_ready = ratchet_is_promotion_ready(ratchet)
    policy_promotes = policy["promotion_decision"] == "promote" or policy["update_state"] in PROMOTING_POLICY_STATES
    execution_status = steward["execution_status"]
    action_type = steward["action_type"]
    evidence_refs = {str(item) for item in steward.get("evidence_refs", [])}
    required_approvals = [str(item).strip() for item in steward.get("required_approvals", []) if str(item).strip()]
    approval_refs = [str(item).strip() for item in steward.get("approval_refs", []) if str(item).strip()]

    if action_type in RELEASE_ACTIONS and execution_status in {"approved", "executed"}:
        if not (ratchet_ready and policy_promotes):
            errors.append(f"{relative}: approved/executed release action requires promotion-ready ratchet and policy records.")
        if str(ratchet["ratchet_id"]) not in evidence_refs:
            errors.append(f"{relative}: release action evidence_refs must include benchmark ratchet id.")
        if str(policy["update_id"]) not in evidence_refs:
            errors.append(f"{relative}: release action evidence_refs must include policy update id.")
        if required_approvals and not approval_refs:
            errors.append(f"{relative}: approved/executed release action requires approval_refs when approvals are required.")
    if execution_status == "executed" and required_approvals and not approval_refs:
        errors.append(f"{relative}: executed steward action requires approval_refs when required_approvals are declared.")
    if action_type == "block_merge" and str(ratchet["ratchet_id"]) not in evidence_refs:
        errors.append(f"{relative}: block_merge decision must reference the benchmark ratchet evidence.")
    if action_type == "block_merge" and execution_status not in {"approved", "executed", "blocked"}:
        errors.append(f"{relative}: block_merge decision should be approved, executed, or blocked.")
    return errors


def semantic_errors(value: dict[str, Any], relative: str) -> list[str]:
    errors: list[str] = []
    if not isinstance(value.get("scenario_id"), str) or not value["scenario_id"].strip():
        errors.append(f"{relative}: scenario_id must be a non-empty string.")
    require_nonempty_list(value, "non_claims", errors, relative)
    if errors:
        return errors

    ratchet = value["benchmark_ratchet_record"]
    policy = value["policy_optimization_record"]
    steward = value["steward_action_decision"]
    errors.extend(ratchet_errors(ratchet, relative))
    errors.extend(policy_errors(policy, ratchet, relative))
    errors.extend(steward_errors(steward, ratchet, policy, relative))
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
        raise SystemExit(f"No benchmark anti-Goodhart fixtures found in {FIXTURE_DIR.relative_to(ROOT)}.")

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
                errors.append(f"{relative}: invalid fixture unexpectedly passed benchmark anti-Goodhart checks.")

    if errors:
        print("Benchmark anti-Goodhart harness failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print(
        "Benchmark anti-Goodhart harness passed: "
        f"{valid_count} valid fixture(s), {invalid_count} expected-invalid fixture(s)."
    )


if __name__ == "__main__":
    main()
