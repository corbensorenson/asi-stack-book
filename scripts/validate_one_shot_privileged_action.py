#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
from datetime import datetime
import json
from pathlib import Path
from typing import Any

from validate_protocol_examples import validate_value

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "one_shot_privileged_action_record.schema.json"
VALID = ROOT / "tests" / "fixtures" / "protocol_records" / "one_shot_privileged_action_record.valid.json"
MUTATIONS = ROOT / "experiments" / "one_shot_privileged_action" / "fixtures"
EXPECTED_SOURCES = {"cca_project", "moecot_manifest_project", "beastbrain_project", "bugbrain_project", "corbens_best_model_possible_project"}
HAPPY_PATH = ["requested", "resolved", "approved", "dispatched", "effect_observed", "consumed"]


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def instant(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def semantic_errors(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if set(record.get("source_ids", [])) != EXPECTED_SOURCES:
        errors.append("one-shot action lineage must name the five historical-project sources exactly")
    approval = record.get("approval", {})
    observation = record.get("execution_observation", {})
    decision = record.get("decision", {})
    if approval.get("approval_kind") in {"scenario_acknowledgement", "test_fixture_acknowledgement"} and decision.get("privileged_effect_authorized"):
        errors.append("scenario or fixture acknowledgement cannot authorize a privileged effect")
    issued = instant(approval["issued_at"])
    expires = instant(approval["expires_at"])
    dispatched = instant(observation["dispatched_at"])
    if expires <= issued:
        errors.append("approval TTL must end after issuance")
    if decision.get("privileged_effect_authorized") and not (issued <= dispatched < expires):
        errors.append("privileged dispatch must occur inside the approval TTL")
    bindings = {
        "principal": (approval.get("principal_id"), observation.get("principal_id")),
        "operation": (approval.get("operation"), observation.get("operation")),
        "target": (approval.get("target_id"), observation.get("target_id")),
        "target-state digest": (approval.get("target_state_digest"), observation.get("pre_state_digest")),
        "parameter digest": (approval.get("parameter_digest"), observation.get("parameter_digest")),
        "policy version": (approval.get("policy_version"), observation.get("policy_version")),
        "nonce": (approval.get("nonce"), observation.get("nonce")),
    }
    for name, pair in bindings.items():
        if pair[0] != pair[1]:
            errors.append(f"approval {name} must match the observed execution")
    states = [row.get("state") for row in record.get("state_history", [])]
    if decision.get("state") == "consumed" and states != HAPPY_PATH:
        errors.append("consumed privileged action must follow the one-shot state sequence exactly")
    observed_times = [instant(row["observed_at"]) for row in record.get("state_history", [])]
    if observed_times != sorted(observed_times):
        errors.append("one-shot state transitions must be temporally monotone")
    if decision.get("state") == "consumed":
        if not observation.get("effect_observed") or not observation.get("effect_receipt_ref") or not observation.get("post_state_digest"):
            errors.append("consumed privileged action requires independently recorded effect and post-state")
    replay = record.get("replay_control", {})
    nonce = approval.get("nonce")
    if decision.get("state") == "consumed":
        if not replay.get("single_use") or nonce not in replay.get("consumed_nonce_refs", []):
            errors.append("consumed approval nonce must be recorded as single-use")
        if replay.get("replay_attempts", 0) > 0 and replay.get("replay_decision") != "denied":
            errors.append("replay of a consumed one-shot approval must be denied")
    if decision.get("support_state_effect") == "eligible_for_bounded_evidence_review":
        errors.append("hand-authored privileged-action fixtures cannot promote support")
    if not record.get("promotion_blockers") or not record.get("non_claims"):
        errors.append("one-shot action record must preserve blockers and non-claims")
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
        raise SystemExit("Valid one-shot privileged-action record failed:\n - " + "\n - ".join(errors))
    mutations = sorted(MUTATIONS.glob("invalid_*.json"))
    if not mutations:
        raise SystemExit("No one-shot privileged-action mutations found.")
    for path in mutations:
        mutation = load(path)
        candidate = apply_mutation(valid, mutation)
        found = validate_value(candidate, schema, str(path.relative_to(ROOT))) + semantic_errors(candidate)
        if not any(mutation["expected_error"] in error for error in found):
            raise SystemExit(f"{path.relative_to(ROOT)} did not produce {mutation['expected_error']!r}: {found}")
    print(f"One-shot privileged-action harness passed: 1 consumed five-project record and {len(mutations)} expected-invalid mutations.")


if __name__ == "__main__":
    main()
