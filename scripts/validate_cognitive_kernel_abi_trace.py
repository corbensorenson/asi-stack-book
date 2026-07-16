#!/usr/bin/env python3
"""Independently execute the finite Cognitive Kernel ABI trace contract.

The checker deliberately reimplements the transition relation in Python. It
does not parse or call Lean, and therefore supplies a bounded differential
consumer rather than a second view of the same implementation.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "experiments/cognitive_kernel_abi/corpus/2026-07-15.json"
RESULT = ROOT / "experiments/cognitive_kernel_abi/results/2026-07-15-local.json"
LEAN_MODEL = ROOT / "lean/AsiStackProofs/ReplaceableCognitiveSubstrates.lean"
SCHEMA = ROOT / "schemas/cognitive_kernel_abi_trace.schema.json"

FAMILIES = {
    "transformer",
    "selective_state_space",
    "recurrent",
    "kan",
    "program_synthesizer",
}
KINDS = {"propose", "commit", "migrate", "revoke"}
COMMON_CUSTODY = (
    "fallback_ready",
    "evaluator_independent",
    "assistance_declared",
    "lifecycle_cost_declared",
    "residual_owner_present",
    "rollback_ready",
)
EVENT_MUTATIONS = (
    (0, "effect_observed", True),
    (0, "requested_authority", 3),
    (0, "checkpoint_digest", 9999),
    (0, "fallback_ready", False),
    (0, "evaluator_independent", False),
    (0, "assistance_declared", False),
    (0, "lifecycle_cost_declared", False),
    (0, "residual_owner_present", False),
    (0, "rollback_ready", False),
    (1, "migration_compatible", False),
    (3, "effect_receipt_present", False),
    (3, "evidence_transition_present", False),
)


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def expand_events(base: dict[str, Any], patches: list[dict[str, Any]]) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for patch in patches:
        event = copy.deepcopy(base)
        event.update(patch)
        events.append(event)
    return events


def rejection_reasons(state: dict[str, Any], event: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    kind = event.get("kind")
    if kind not in KINDS:
        return ["unknown_event_kind"]
    if event.get("target_family") not in FAMILIES or event.get("fallback_family") not in FAMILIES:
        reasons.append("unknown_kernel_family")
    if event.get("actor_kernel") != state.get("active_kernel"):
        reasons.append("actor_not_active")
    if state.get("revoked_kernel") == event.get("actor_kernel"):
        reasons.append("actor_revoked")
    if event.get("requested_authority", -1) > state.get("authority_ceiling", -1):
        reasons.append("authority_widening")
    if event.get("checkpoint_schema") != state.get("checkpoint_schema"):
        reasons.append("checkpoint_schema_mismatch")
    if event.get("checkpoint_digest") != state.get("checkpoint_digest"):
        reasons.append("checkpoint_digest_mismatch")
    for field in COMMON_CUSTODY:
        if event.get(field) is not True:
            reasons.append(f"missing_{field}")

    if kind == "propose":
        if state.get("revoked_kernel") == event.get("target_kernel"):
            reasons.append("target_revoked")
        if event.get("proposal_only") is not True:
            reasons.append("proposal_not_declared")
        if event.get("effect_observed") is not False:
            reasons.append("proposal_observed_effect")
        if event.get("effect_receipt_present") is not False:
            reasons.append("proposal_carries_effect_receipt")
    elif kind == "commit":
        if state.get("pending_kernel") != event.get("actor_kernel"):
            reasons.append("missing_matching_proposal")
        if event.get("target_kernel") != event.get("actor_kernel"):
            reasons.append("commit_target_mismatch")
        if event.get("proposal_only") is not False:
            reasons.append("commit_marked_proposal_only")
        if event.get("effect_observed") is not True:
            reasons.append("commit_without_observed_effect")
        if event.get("effect_receipt_present") is not True:
            reasons.append("commit_without_receipt")
        if event.get("evidence_transition_present") is not True:
            reasons.append("commit_without_evidence_transition")
    elif kind == "migrate":
        if state.get("pending_kernel") != event.get("target_kernel"):
            reasons.append("migration_without_matching_proposal")
        if state.get("revoked_kernel") == event.get("target_kernel"):
            reasons.append("migration_target_revoked")
        if event.get("migration_compatible") is not True:
            reasons.append("incompatible_migration")
        if event.get("target_kernel") == event.get("actor_kernel"):
            reasons.append("migration_not_a_replacement")
        if event.get("proposal_only") is not True or event.get("effect_observed") is not False:
            reasons.append("migration_has_material_effect")
        if event.get("effect_receipt_present") is not False:
            reasons.append("migration_carries_effect_receipt")
    elif kind == "revoke":
        if event.get("target_kernel") != event.get("fallback_kernel"):
            reasons.append("fallback_target_mismatch")
        if event.get("fallback_kernel") == event.get("actor_kernel"):
            reasons.append("revocation_to_self")
        if state.get("revoked_kernel") == event.get("fallback_kernel"):
            reasons.append("fallback_revoked")
        if event.get("proposal_only") is not True or event.get("effect_observed") is not False:
            reasons.append("revocation_has_material_effect")
        if event.get("effect_receipt_present") is not False:
            reasons.append("revocation_carries_effect_receipt")
    return reasons


def apply_event(state: dict[str, Any], event: dict[str, Any]) -> dict[str, Any]:
    next_state = copy.deepcopy(state)
    kind = event["kind"]
    if kind == "propose":
        next_state["pending_kernel"] = event["target_kernel"]
    elif kind == "commit":
        next_state["pending_kernel"] = None
        next_state["committed_effects"] += 1
    elif kind == "migrate":
        next_state["active_kernel"] = event["target_kernel"]
        next_state["active_family"] = event["target_family"]
        next_state["pending_kernel"] = None
    elif kind == "revoke":
        next_state["revoked_kernel"] = event["actor_kernel"]
        next_state["active_kernel"] = event["fallback_kernel"]
        next_state["active_family"] = event["fallback_family"]
        next_state["pending_kernel"] = None
    return next_state


def run_trace(initial: dict[str, Any], events: list[dict[str, Any]]) -> dict[str, Any]:
    state = copy.deepcopy(initial)
    states = [copy.deepcopy(state)]
    proposal_effect_count = 0
    for index, event in enumerate(events):
        before_effects = state["committed_effects"]
        reasons = rejection_reasons(state, event)
        if reasons:
            return {
                "accepted": False,
                "rejection_index": index,
                "reasons": reasons,
                "final_state": state,
                "states": states,
                "proposal_effect_count": proposal_effect_count,
            }
        state = apply_event(state, event)
        if event["kind"] == "propose" and state["committed_effects"] != before_effects:
            proposal_effect_count += 1
        states.append(copy.deepcopy(state))
    return {
        "accepted": True,
        "rejection_index": None,
        "reasons": [],
        "final_state": state,
        "states": states,
        "proposal_effect_count": proposal_effect_count,
    }


def validate_result_shape(result: dict[str, Any]) -> list[str]:
    schema = load(SCHEMA)
    errors: list[str] = []
    required = set(schema["required"])
    missing = sorted(required - set(result))
    extra = sorted(set(result) - set(schema["properties"]))
    if missing:
        errors.append(f"result missing fields: {missing}")
    if extra:
        errors.append(f"result has unexpected fields: {extra}")
    if result.get("status") not in {"passed", "failed"}:
        errors.append("invalid result status")
    if result.get("support_state_effect") != "none":
        errors.append("support-state effect must remain none")
    if not isinstance(result.get("non_claims"), list) or len(result.get("non_claims", [])) < 3:
        errors.append("at least three non-claims are required")
    for field in (
        "case_count", "accepted_case_count", "rejected_case_count",
        "accepted_event_count", "committed_effect_count", "proposal_effect_count",
        "mutation_count", "mutation_rejection_count",
    ):
        if not isinstance(result.get(field), int) or isinstance(result.get(field), bool):
            errors.append(f"{field} must be an integer")
    return errors


def build_result() -> tuple[dict[str, Any], list[str]]:
    corpus = load(CORPUS)
    errors: list[str] = []
    base = corpus["base_event"]
    initial = corpus["initial_state"]
    accepted_cases = 0
    rejected_cases = 0
    accepted_event_count = 0
    committed_effect_count = 0
    proposal_effect_count = 0
    family_route: list[str] = []
    accepted_events: list[dict[str, Any]] | None = None

    for case in corpus["cases"]:
        events = expand_events(base, case["patches"])
        observed = run_trace(initial, events)
        expected_accepted = case["expected"] == "accepted"
        if observed["accepted"] != expected_accepted:
            errors.append(
                f"{case['id']}: expected {case['expected']}, observed "
                f"{'accepted' if observed['accepted'] else 'rejected'} at "
                f"{observed['rejection_index']} ({observed['reasons']})"
            )
            continue
        if expected_accepted:
            accepted_cases += 1
            accepted_events = events
            if observed["final_state"] != case.get("expected_final"):
                errors.append(f"{case['id']}: final state differs from expected_final")
            accepted_event_count += len(events)
            committed_effect_count += observed["final_state"]["committed_effects"]
            proposal_effect_count += observed["proposal_effect_count"]
            for state in observed["states"]:
                family = state["active_family"]
                if not family_route or family_route[-1] != family:
                    family_route.append(family)
        else:
            rejected_cases += 1

    mutation_rejections = 0
    if accepted_events is None:
        errors.append("corpus has no accepted reference trace")
    else:
        for index, field, value in EVENT_MUTATIONS:
            mutated = copy.deepcopy(accepted_events)
            mutated[index][field] = value
            if not run_trace(initial, mutated)["accepted"]:
                mutation_rejections += 1
            else:
                errors.append(f"event mutation accepted: event {index} {field}={value!r}")

    result = {
        "schema_version": "0.1",
        "experiment_id": corpus["corpus_id"],
        "status": "passed" if not errors else "failed",
        "corpus_sha256": sha256(CORPUS),
        "lean_model_sha256": sha256(LEAN_MODEL),
        "case_count": len(corpus["cases"]),
        "accepted_case_count": accepted_cases,
        "rejected_case_count": rejected_cases,
        "accepted_event_count": accepted_event_count,
        "committed_effect_count": committed_effect_count,
        "proposal_effect_count": proposal_effect_count,
        "family_route": family_route,
        "mutation_count": len(EVENT_MUTATIONS),
        "mutation_rejection_count": mutation_rejections,
        "support_state_effect": "none",
        "non_claims": corpus["non_claims"],
    }
    errors.extend(validate_result_shape(result))
    if result["case_count"] != result["accepted_case_count"] + result["rejected_case_count"]:
        errors.append("case count does not reconcile")
    if result["proposal_effect_count"] != 0:
        errors.append("proposal event changed the committed-effect count")
    if result["mutation_rejection_count"] != result["mutation_count"]:
        errors.append("not every event mutation was rejected")
    if result["family_route"] != ["transformer", "selective_state_space", "kan", "selective_state_space"]:
        errors.append(f"unexpected family route: {result['family_route']}")
    return result, errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result, errors = build_result()
    if args.write:
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    elif not RESULT.exists():
        errors.append(f"missing {RESULT.relative_to(ROOT)}; run with --write")
    else:
        stored = load(RESULT)
        errors.extend(validate_result_shape(stored))
        if stored != result:
            errors.append("stored result is stale; run with --write")

    # Result-record controls are separate from the event-level mutation suite.
    for label, mutation in (
        ("support promotion", {"support_state_effect": "promotion"}),
        ("inflated accepted cases", {"accepted_case_count": result["accepted_case_count"] + 1}),
        ("missing non-claims", {"non_claims": []}),
    ):
        candidate = copy.deepcopy(result)
        candidate.update(mutation)
        shape_errors = validate_result_shape(candidate)
        reconciles = candidate.get("case_count") == candidate.get("accepted_case_count", 0) + candidate.get("rejected_case_count", 0)
        if not shape_errors and reconciles:
            errors.append(f"result-record negative control accepted: {label}")

    if errors:
        print("Cognitive Kernel ABI trace validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)
    print(
        "Cognitive Kernel ABI trace passed: "
        f"{result['case_count']} cases ({result['accepted_case_count']} accepted, "
        f"{result['rejected_case_count']} rejected), {result['accepted_event_count']} accepted events, "
        f"{result['committed_effect_count']} committed effects, "
        f"{result['mutation_rejection_count']} event mutations rejected, support effect none."
    )


if __name__ == "__main__":
    main()
