#!/usr/bin/env python3
"""Validate synthetic recursive self-improvement transition fixtures."""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

from validate_protocol_examples import validate_value


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "experiments" / "self_improvement_boundaries" / "fixtures"
SCHEMA = ROOT / "schemas" / "self_improvement_transition.schema.json"

AUTHORITY_BAD_TERMS = {
    "all authority",
    "all tools",
    "ambient",
    "any action",
    "any tool",
    "root",
    "unbounded",
    "unrestricted",
    "widens authority",
}
SELF_EVALUATION_BAD_TERMS = {
    "candidate validates itself",
    "same component",
    "self-attested",
    "self-evaluated only",
    "self-judged",
}
WEAKENING_TERMS = {
    "drop protected invariant",
    "drop protected invariants",
    "remove protected invariant",
    "remove protected invariants",
    "weaken protected invariant",
    "weaken protected invariants",
    "weaken invariant",
    "weaken invariants",
}
PROMOTION_BAD_TERMS = {
    "guarantees safety",
    "proves alignment",
    "proves self-improvement safety",
    "support state can be promoted",
    "support state promoted",
}
BOUNDARY_DELTA_BAD_TERMS = {
    "boundary delta not needed",
    "boundary review omitted",
    "hidden authority widening",
    "no boundary review",
    "silently widens",
    "skip boundary review",
}
VERIFICATION_BUDGET_BAD_TERMS = {
    "cut rollback",
    "cut security",
    "cut verification",
    "drop rollback",
    "drop security",
    "drop verification",
    "remove human review",
    "skip human review",
    "skip rollback",
    "skip security",
    "skip verification",
    "verification budget cut",
}
STALE_GATE_BAD_TERMS = {
    "expired gate",
    "old gate",
    "prior architecture",
    "stale gate",
    "without rerun",
}
ROLLBACK_TERMS = {"fallback", "restore", "rollback", "return", "revert"}
REVIEW_TERMS = {"external", "independent", "not allowed to be the sole", "review", "separate"}
MONITOR_TERMS = {"canary", "monitor", "observation", "regression", "watch"}
BOUNDARY_REQUIRED_TERMS = {"authority", "security", "resource", "evaluator", "evidence", "rollback"}
VERIFICATION_REQUIRED_TERMS = {"verification", "security", "rollback", "review"}
GATE_FRESHNESS_TERMS = {"current", "fresh", "rerun", "review", "reject", "stale"}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def as_text(value: Any) -> str:
    if isinstance(value, list):
        return " ".join(as_text(item) for item in value)
    if isinstance(value, dict):
        return " ".join(f"{key} {as_text(child)}" for key, child in value.items())
    return str(value)


def contains_any(text: str, terms: set[str]) -> bool:
    return any(term in text for term in terms)


def nonempty_string_list(record: dict[str, Any], key: str) -> bool:
    value = record.get(key)
    return isinstance(value, list) and bool(value) and all(isinstance(item, str) and item.strip() for item in value)


def semantic_errors(record: dict[str, Any], relative: str) -> list[str]:
    errors: list[str] = []
    transition_id = str(record.get("transition_id", "")).lower()
    field_id = str(record.get("field_id", "")).lower()
    proposal = str(record.get("proposal", "")).lower()
    trigger = str(record.get("trigger_residual", "")).lower()
    cheaper = as_text(record.get("cheaper_interventions_tried", [])).lower()
    invariants = as_text(record.get("protected_invariants", [])).lower()
    boundary_delta = str(record.get("boundary_delta_review", "")).lower()
    verification_budget = str(record.get("verification_budget_preservation", "")).lower()
    gate_freshness = str(record.get("gate_freshness", "")).lower()
    evaluator = str(record.get("evaluator_independence", "")).lower()
    replacement = str(record.get("replacement_transaction", "")).lower()
    approval = str(record.get("governance_approval", "")).lower()
    monitor = str(record.get("monitor_window", "")).lower()
    rollback = str(record.get("rollback_path", "")).lower()
    outcome = str(record.get("outcome_state", "")).lower()
    combined = " ".join([
        trigger,
        proposal,
        cheaper,
        invariants,
        boundary_delta,
        verification_budget,
        gate_freshness,
        evaluator,
        replacement,
        approval,
        monitor,
        rollback,
    ])

    advancing_outcomes = {"canary", "promoted", "retired"}
    non_advancing_outcomes = {"rejected", "quarantined", "rolled_back"}

    if not transition_id.startswith("self-improvement://"):
        errors.append(f"{relative}: transition_id must be a self-improvement:// identifier.")
    if not field_id.startswith("field://"):
        errors.append(f"{relative}: field_id must be a field:// identifier.")
    if not replacement.startswith("replacement://"):
        errors.append(f"{relative}: replacement_transaction must be a replacement:// identifier.")

    if not nonempty_string_list(record, "cheaper_interventions_tried"):
        errors.append(f"{relative}: cheaper_interventions_tried must record at least one prior cheaper intervention.")
    if not nonempty_string_list(record, "protected_invariants"):
        errors.append(f"{relative}: protected_invariants must name at least one invariant.")
    if not contains_any(boundary_delta, BOUNDARY_REQUIRED_TERMS):
        errors.append(f"{relative}: boundary_delta_review must mention authority, security, resource, evaluator, evidence, or rollback deltas.")
    if not contains_any(verification_budget, VERIFICATION_REQUIRED_TERMS):
        errors.append(f"{relative}: verification_budget_preservation must mention verification, security, rollback, or review budget preservation.")
    if not contains_any(gate_freshness, GATE_FRESHNESS_TERMS):
        errors.append(f"{relative}: gate_freshness must mention current, fresh, rerun, review, reject, or stale gate status.")

    if contains_any(evaluator, SELF_EVALUATION_BAD_TERMS):
        errors.append(f"{relative}: evaluator_independence cannot rely on self-evaluation by the candidate or replaced component.")
    if not contains_any(evaluator, REVIEW_TERMS):
        errors.append(f"{relative}: evaluator_independence must name an independent, separate, external, or review boundary.")

    if outcome in advancing_outcomes and contains_any(combined, AUTHORITY_BAD_TERMS):
        errors.append(f"{relative}: advancing transitions must not widen authority or grant ambient/root access.")
    if outcome in advancing_outcomes and contains_any(combined, WEAKENING_TERMS):
        errors.append(f"{relative}: advancing transitions must not weaken protected invariants.")
    if outcome in advancing_outcomes and contains_any(combined, PROMOTION_BAD_TERMS):
        errors.append(f"{relative}: advancing transitions must not claim broad safety proof or support-state promotion.")
    if outcome in advancing_outcomes and contains_any(boundary_delta, BOUNDARY_DELTA_BAD_TERMS):
        errors.append(f"{relative}: advancing transitions require explicit boundary-delta review.")
    if outcome in advancing_outcomes and contains_any(verification_budget, VERIFICATION_BUDGET_BAD_TERMS):
        errors.append(f"{relative}: advancing transitions must preserve verification, security, rollback, and human-review budgets unless separately governed.")
    if outcome in advancing_outcomes and contains_any(gate_freshness, STALE_GATE_BAD_TERMS):
        errors.append(f"{relative}: advancing transitions cannot rely on stale gates without rerun or rejection.")

    if contains_any(proposal, WEAKENING_TERMS) and outcome not in non_advancing_outcomes:
        errors.append(f"{relative}: proposals that weaken protected invariants must be rejected, quarantined, or rolled back.")
    if contains_any(combined, PROMOTION_BAD_TERMS):
        errors.append(f"{relative}: transition records cannot claim support-state promotion or broad ASI safety proof.")

    if not contains_any(rollback, ROLLBACK_TERMS):
        errors.append(f"{relative}: rollback_path must name fallback, restore, rollback, return, or revert behavior.")

    if outcome in {"canary", "promoted"}:
        if approval in {"", "none", "missing", "auto", "automatic"}:
            errors.append(f"{relative}: canary or promoted outcomes require review or approval text.")
        if "review" not in approval and not approval.startswith("approval://"):
            errors.append(f"{relative}: canary or promoted outcomes must route through review or a concrete approval:// record.")
        if not contains_any(monitor, MONITOR_TERMS):
            errors.append(f"{relative}: canary or promoted outcomes require a monitor, canary, observation, or regression window.")

    if outcome == "canary" and "canary" not in monitor:
        errors.append(f"{relative}: canary outcomes require a canary monitor window.")
    if outcome == "promoted":
        if not approval.startswith("approval://"):
            errors.append(f"{relative}: promoted outcomes require a concrete approval:// record.")
        if not any(term in monitor for term in ("pass", "passed", "clean")):
            errors.append(f"{relative}: promoted outcomes require a passing or clean monitor result.")
    if outcome == "rolled_back" and not any(term in monitor for term in ("fail", "breach", "violation", "regression")):
        errors.append(f"{relative}: rolled_back outcomes must name the monitor failure, breach, violation, or regression.")
    if outcome in {"rejected", "quarantined"} and not any(term in combined for term in ("block", "reject", "quarantine", "violation", "weak")):
        errors.append(f"{relative}: rejected or quarantined outcomes must preserve the blocking reason.")

    return errors


def fixture_expectation(path: Path) -> bool | None:
    if path.name.startswith("valid_"):
        return True
    if path.name.startswith("invalid_"):
        return False
    return None


def main() -> None:
    schema = load_json(SCHEMA)
    fixtures = sorted(FIXTURE_DIR.glob("*.json"))
    if not fixtures:
        raise SystemExit(f"No self-improvement-boundary fixtures found in {rel(FIXTURE_DIR)}.")

    errors: list[str] = []
    valid_count = 0
    invalid_count = 0
    for fixture in fixtures:
        relative = rel(fixture)
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
            errors.append(f"{relative}: top-level fixture must be an object.")
            continue

        fixture_errors = validate_value(value, schema, relative) + semantic_errors(value, relative)
        if expect_valid:
            valid_count += 1
            errors.extend(fixture_errors)
        else:
            invalid_count += 1
            if not fixture_errors:
                errors.append(f"{relative}: expected invalid fixture passed validation.")

    if errors:
        print("Self-improvement boundary harness failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print(
        "Self-improvement boundary harness passed: "
        f"{valid_count} valid fixture(s), {invalid_count} expected-invalid fixture(s)."
    )


if __name__ == "__main__":
    main()
