#!/usr/bin/env python3
"""Independently replay the safety-critical lifecycle trace corpus."""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "experiments" / "safety_critical_lifecycle" / "trace_corpus.json"
LEAN = ROOT / "lean" / "AsiStackProofs" / "SafetyCriticalLifecycle.lean"

DOMAINS = {
    "alignment",
    "corrigibility",
    "value_conflict",
    "governance_rights",
    "self_improvement",
}
REQUIREMENTS = {
    "protected_predicate",
    "operational_test",
    "affected_party",
    "material_notice",
    "pre_effect_review",
    "current_approval",
    "bounded_delegation",
    "correction_path",
    "rollback_path",
    "residual_record",
    "accountable_principal",
    "audit_material",
    "appeal_path",
    "exit_export",
    "fork_safety_review",
    "fork_obligations",
    "dissent_payload",
    "durable_receipt",
    "independent_evaluator",
    "monitor_window",
    "evidence_transition",
    "non_claim_boundary",
}
EXPECTED_CASE_IDS = {
    "valid_alignment_effect",
    "valid_corrigibility_effect",
    "valid_value_conflict_effect",
    "valid_governance_rights_effect",
    "valid_self_improvement_effect",
    "valid_support_promotion",
    "valid_effect_rollback",
    "valid_narrow_then_revoke",
    "reject_alignment_missing_review",
    "reject_corrigibility_missing_affected_party",
    "reject_value_conflict_missing_residual",
    "reject_governance_missing_exit",
    "reject_self_improvement_self_evaluation",
    "reject_protected_removal",
    "reject_authority_widening",
    "reject_support_promotion_without_receipt",
}


def initial_state(domain: str) -> dict[str, Any]:
    return {
        "domain": domain,
        "phase": "proposed",
        "evidence": {name: name == "protected_predicate" for name in REQUIREMENTS},
        "high_impact": False,
        "support_promotion_requested": False,
        "authority": 3,
        "authority_ceiling": 3,
    }


def step(
    state: dict[str, Any], event: str, domain_requirements: dict[str, list[str]]
) -> dict[str, Any] | None:
    next_state = deepcopy(state)
    if event.startswith("record:"):
        requirement = event.split(":", 1)[1]
        if requirement not in REQUIREMENTS:
            return None
        next_state["evidence"][requirement] = True
        return next_state
    if event == "declare_high_impact":
        next_state["high_impact"] = True
        return next_state
    if event == "request_support_promotion":
        next_state["support_promotion_requested"] = True
        return next_state
    if event == "commit_effect":
        required = domain_requirements[state["domain"]]
        ready = all(state["evidence"][name] for name in required)
        if not ready or state["authority"] > state["authority_ceiling"]:
            return None
        next_state["phase"] = "effect_committed"
        return next_state
    if event == "promote_support":
        ready = (
            state["phase"] == "effect_committed"
            and state["support_promotion_requested"]
            and state["evidence"]["evidence_transition"]
            and state["evidence"]["non_claim_boundary"]
            and state["evidence"]["durable_receipt"]
        )
        if not ready:
            return None
        next_state["phase"] = "promoted"
        return next_state
    if event.startswith("narrow_authority:"):
        new_scope = int(event.split(":", 1)[1])
        if new_scope > state["authority"]:
            return None
        next_state["authority"] = new_scope
        return next_state
    if event.startswith("widen_authority:"):
        new_scope = int(event.split(":", 1)[1])
        if new_scope > state["authority"]:
            return None
        next_state["authority"] = new_scope
        return next_state
    if event == "remove_protected_predicate":
        return None
    if event == "rollback":
        if not state["evidence"]["rollback_path"] or state["phase"] not in {
            "effect_committed",
            "promoted",
        }:
            return None
        next_state["phase"] = "rolled_back"
        return next_state
    if event == "revoke":
        next_state["authority"] = 0
        next_state["phase"] = "revoked"
        return next_state
    return None


def replay(
    case: dict[str, Any], domain_requirements: dict[str, list[str]]
) -> tuple[dict[str, Any] | None, int | None]:
    state = initial_state(case["domain"])
    for index, event in enumerate(case["events"]):
        next_state = step(state, event, domain_requirements)
        if next_state is None:
            return None, index
        if not next_state["evidence"]["protected_predicate"]:
            raise AssertionError(f"{case['id']}: accepted step removed protected predicate")
        if next_state["authority"] > state["authority"]:
            raise AssertionError(f"{case['id']}: accepted step widened authority")
        state = next_state
    return state, None


def validate_shape(value: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["trace corpus must be an object"]
    if value.get("schema_version") != "asi_stack.safety_critical_trace_corpus.v1":
        errors.append("wrong schema_version")
    if value.get("model_version") != "safety-critical-lifecycle.v1":
        errors.append("wrong model_version")
    if value.get("lean_module") != "AsiStackProofs.SafetyCriticalLifecycle":
        errors.append("wrong lean_module")
    if value.get("support_state_effect") != "none":
        errors.append("support_state_effect must remain none")
    non_claims = value.get("non_claims")
    if not isinstance(non_claims, list) or len(non_claims) < 3:
        errors.append("at least three explicit non_claims are required")
    requirements = value.get("domain_requirements")
    if not isinstance(requirements, dict) or set(requirements) != DOMAINS:
        errors.append("domain_requirements must cover exactly five domains")
    else:
        for domain, names in requirements.items():
            if not isinstance(names, list) or not names or len(names) != len(set(names)):
                errors.append(f"{domain}: requirements must be a non-empty unique list")
            elif not set(names) <= REQUIREMENTS:
                errors.append(f"{domain}: unknown requirement")
    cases = value.get("cases")
    if not isinstance(cases, list):
        return errors + ["cases must be a list"]
    ids = [case.get("id") for case in cases if isinstance(case, dict)]
    if len(ids) != len(cases) or len(ids) != len(set(ids)):
        errors.append("case IDs must be present and unique")
    if set(ids) != EXPECTED_CASE_IDS:
        errors.append("case inventory differs from the required positive and negative controls")
    return errors


def validate_cases(value: dict[str, Any]) -> tuple[list[str], int, int, int]:
    errors: list[str] = []
    accepted_count = 0
    rejected_count = 0
    deletion_countermodels = 0
    requirements = value["domain_requirements"]
    by_id = {case["id"]: case for case in value["cases"]}

    for case in value["cases"]:
        if case.get("domain") not in DOMAINS:
            errors.append(f"{case.get('id')}: unknown domain")
            continue
        if not isinstance(case.get("events"), list) or not all(
            isinstance(event, str) for event in case["events"]
        ):
            errors.append(f"{case['id']}: events must be strings")
            continue
        try:
            final, rejected_at = replay(case, requirements)
        except (AssertionError, ValueError) as exc:
            errors.append(str(exc))
            continue
        if case.get("expected") == "accepted":
            accepted_count += 1
            if final is None:
                errors.append(f"{case['id']}: expected acceptance, rejected at {rejected_at}")
                continue
            snapshot = case.get("expected_final")
            actual = {"phase": final["phase"], "authority": final["authority"]}
            if snapshot != actual:
                errors.append(f"{case['id']}: final snapshot {actual!r} != {snapshot!r}")
        elif case.get("expected") == "rejected":
            rejected_count += 1
            if final is not None:
                errors.append(f"{case['id']}: expected rejection, trace was accepted")
            elif case.get("rejected_at") != rejected_at:
                errors.append(
                    f"{case['id']}: rejected_at {rejected_at} != {case.get('rejected_at')}"
                )
        else:
            errors.append(f"{case['id']}: expected must be accepted or rejected")

    for domain in sorted(DOMAINS):
        case = deepcopy(by_id[f"valid_{domain}_effect"])
        for requirement in requirements[domain]:
            if requirement == "protected_predicate":
                # The protected predicate is initial-state authority, not a record event.
                state = initial_state(domain)
                state["evidence"]["protected_predicate"] = False
                events = case["events"]
                rejected = False
                for event in events:
                    state = step(state, event, requirements)
                    if state is None:
                        rejected = True
                        break
                if not rejected:
                    errors.append(f"{domain}: deleting initial {requirement} did not reject effect")
                deletion_countermodels += 1
                continue
            target = f"record:{requirement}"
            if target not in case["events"]:
                errors.append(f"{domain}: valid case lacks required event {target}")
                continue
            case["events"] = [event for event in case["events"] if event != target]
            final, _ = replay(case, requirements)
            if final is not None:
                errors.append(f"{domain}: deleting {target} did not reject effect")
            deletion_countermodels += 1
            case = deepcopy(by_id[f"valid_{domain}_effect"])

    return errors, accepted_count, rejected_count, deletion_countermodels


def validate_digest() -> list[str]:
    digest = hashlib.sha256(CORPUS.read_bytes()).hexdigest()
    lean_text = LEAN.read_text(encoding="utf-8")
    match = re.search(
        r'def\s+traceCorpusSha256\s*:\s*String\s*:=\s*"([0-9a-f]{64})"',
        lean_text,
    )
    if not match:
        return ["Lean module lacks traceCorpusSha256 digest binding"]
    if match.group(1) != digest:
        return [f"Lean corpus digest {match.group(1)} != actual {digest}"]
    return []


def main() -> None:
    try:
        value = json.loads(CORPUS.read_text(encoding="utf-8"))
    except Exception as exc:
        raise SystemExit(f"Could not load {CORPUS.relative_to(ROOT)}: {exc}") from exc

    errors = validate_shape(value)
    accepted_count = rejected_count = deletion_countermodels = 0
    if not errors:
        case_errors, accepted_count, rejected_count, deletion_countermodels = validate_cases(value)
        errors.extend(case_errors)
    errors.extend(validate_digest())
    if errors:
        print("Safety-critical lifecycle validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    digest = hashlib.sha256(CORPUS.read_bytes()).hexdigest()
    print(
        "Safety-critical lifecycle validation passed: "
        f"{accepted_count} accepted traces, {rejected_count} rejected traces, "
        f"{deletion_countermodels} required-obligation deletion countermodels, "
        f"5 domains, corpus sha256 {digest}. Support-state effect: none."
    )


if __name__ == "__main__":
    main()
