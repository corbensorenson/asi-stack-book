#!/usr/bin/env python3
"""Validate synthetic claim-ledger and belief-revision fixtures."""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "experiments" / "claim_ledger_revision" / "fixtures"

SUPPORT_ORDER = {
    "unsupported": 0,
    "argument": 1,
    "source-derived": 2,
    "prototype-backed": 3,
    "synthetic-test-backed": 4,
    "empirical-test-backed": 5,
    "external-literature-backed": 5,
}
CONTRADICTION_ACTIONS = {"downgrade", "quarantine", "split", "residualize", "escalate", "deprecate"}
STATE_CHANGE_ACTIONS = CONTRADICTION_ACTIONS | {"downgrade", "split"}
SEMANTIC_RELATIONS = {"equivalent", "narrower", "broader", "conflicting", "unknown"}
SEMANTIC_REVIEW_STATES = {"accepted_equivalent", "split_required", "escalated", "unknown"}
ASSUMPTION_STATUSES = {"active", "contested", "unsupported", "retired"}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def require_nonempty_string(record: dict[str, Any], key: str, errors: list[str], owner: str) -> str:
    value = record.get(key)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{owner}: {key} must be a non-empty string.")
        return ""
    return value


def require_nonempty_list(record: dict[str, Any], key: str, errors: list[str], owner: str) -> list[Any]:
    value = record.get(key)
    if not isinstance(value, list) or not value:
        errors.append(f"{owner}: {key} must be a non-empty list.")
        return []
    return value


def as_text(value: Any) -> str:
    if isinstance(value, list):
        return " ".join(as_text(item) for item in value)
    if isinstance(value, dict):
        return " ".join(f"{key} {as_text(child)}" for key, child in value.items())
    return str(value)


def contains_any(value: Any, terms: tuple[str, ...]) -> bool:
    lowered = as_text(value).lower()
    return any(term in lowered for term in terms)


def validate_semantic_variants(
    record: dict[str, Any],
    top_non_claims: list[Any],
    errors: list[str],
    owner: str,
) -> None:
    variants = record.get("claim_text_variants")
    review = record.get("semantic_equivalence_review")
    if variants is None and review is None:
        return

    if not isinstance(variants, list) or not variants:
        errors.append(f"{owner}: claim_text_variants must be a non-empty list when semantic_equivalence_review is present.")
        return
    if not isinstance(review, dict):
        errors.append(f"{owner}: semantic_equivalence_review must be an object when claim_text_variants are present.")
        return

    review_owner = f"{owner}:semantic_equivalence_review"
    review_state = require_nonempty_string(review, "review_state", errors, review_owner)
    require_nonempty_string(review, "reviewer", errors, review_owner)
    require_nonempty_list(review, "review_refs", errors, review_owner)
    if review_state and review_state not in SEMANTIC_REVIEW_STATES:
        errors.append(f"{review_owner}: review_state {review_state!r} is not supported.")

    action = str(record.get("revision_action", ""))
    surface_refs = set(str(item) for item in record.get("surface_refs", []))
    scope_risk = False

    for index, variant in enumerate(variants, start=1):
        variant_owner = f"{owner}:claim_text_variants[{index}]"
        if not isinstance(variant, dict):
            errors.append(f"{variant_owner}: variant must be an object.")
            continue
        for key in ("variant_id", "surface_ref", "text", "semantic_relation", "scope_effect", "support_state_effect"):
            require_nonempty_string(variant, key, errors, variant_owner)
        relation = str(variant.get("semantic_relation", ""))
        scope_effect = str(variant.get("scope_effect", ""))
        support_effect = str(variant.get("support_state_effect", ""))
        surface_ref = str(variant.get("surface_ref", ""))
        if relation and relation not in SEMANTIC_RELATIONS:
            errors.append(f"{variant_owner}: unsupported semantic_relation {relation!r}.")
        if surface_ref and surface_ref not in surface_refs:
            errors.append(f"{variant_owner}: surface_ref must also appear in surface_refs.")
        if relation == "equivalent" and scope_effect != "same":
            errors.append(f"{variant_owner}: equivalent variants must preserve same scope_effect.")
        if relation in {"broader", "conflicting", "unknown"} or scope_effect != "same" or support_effect != "none":
            scope_risk = True

    if action == "merge" and scope_risk:
        errors.append(f"{owner}: merge revisions cannot absorb broader, conflicting, unknown, scope-changing, or support-changing variants.")
    if review_state == "accepted_equivalent" and scope_risk:
        errors.append(f"{review_owner}: accepted_equivalent cannot approve scope-changing or support-changing variants.")
    if review_state == "split_required" and action not in {"split", "residualize", "escalate"}:
        errors.append(f"{review_owner}: split_required review must split, residualize, or escalate.")
    if scope_risk and not contains_any(
        [
            record.get("promotion_blockers", []),
            record.get("review_routes", []),
            record.get("residuals", []),
        ],
        ("semantic", "scope", "variant"),
    ):
        errors.append(f"{owner}: semantic scope risks must appear in blockers, review routes, or residuals.")

    non_claim_text = as_text(top_non_claims + record.get("non_claims", [])).lower()
    if "does not prove semantic equivalence" not in non_claim_text:
        errors.append(f"{owner}: semantic fixtures must deny semantic-equivalence proof.")


def validate_assumption_contexts(
    record: dict[str, Any],
    top_non_claims: list[Any],
    errors: list[str],
    owner: str,
) -> None:
    contexts = record.get("assumption_contexts")
    refs = record.get("assumption_context_refs")
    if contexts is None and refs is None:
        return

    if not isinstance(contexts, list) or not contexts:
        errors.append(f"{owner}: assumption_contexts must be a non-empty list when assumption_context_refs are present.")
        return
    if not isinstance(refs, list) or not refs:
        errors.append(f"{owner}: assumption_context_refs must be a non-empty list when assumption_contexts are present.")
        return

    referenced_ids = {str(item) for item in refs}
    risky_context = False
    for index, context in enumerate(contexts, start=1):
        context_owner = f"{owner}:assumption_contexts[{index}]"
        if not isinstance(context, dict):
            errors.append(f"{context_owner}: context must be an object.")
            continue
        assumption_id = require_nonempty_string(context, "assumption_id", errors, context_owner)
        require_nonempty_string(context, "text", errors, context_owner)
        require_nonempty_string(context, "evidence_ref", errors, context_owner)
        status = require_nonempty_string(context, "status", errors, context_owner)
        require_nonempty_list(context, "dependent_claim_ids", errors, context_owner)
        require_nonempty_list(context, "surface_refs", errors, context_owner)
        if assumption_id and assumption_id not in referenced_ids:
            errors.append(f"{context_owner}: assumption_id must appear in assumption_context_refs.")
        if status and status not in ASSUMPTION_STATUSES:
            errors.append(f"{context_owner}: unsupported status {status!r}.")
        if status in {"contested", "unsupported"}:
            risky_context = True

    action = str(record.get("revision_action", ""))
    if risky_context:
        if action not in {"split", "downgrade", "residualize", "escalate", "quarantine"}:
            errors.append(f"{owner}: contested or unsupported assumption contexts must split, downgrade, residualize, escalate, or quarantine.")
        if not contains_any(
            [
                record.get("contradiction_refs", []),
                record.get("promotion_blockers", []),
                record.get("review_routes", []),
                record.get("residuals", []),
            ],
            ("assumption", "context"),
        ):
            errors.append(f"{owner}: assumption-context risks must remain visible in contradiction refs, blockers, review routes, or residuals.")

    non_claim_text = as_text(top_non_claims + record.get("non_claims", [])).lower()
    if "does not prove assumption-context completeness" not in non_claim_text:
        errors.append(f"{owner}: assumption-context fixtures must deny assumption-context completeness.")


def semantic_errors(value: dict[str, Any], relative: str) -> list[str]:
    errors: list[str] = []
    require_nonempty_string(value, "scenario_id", errors, relative)
    top_non_claims = require_nonempty_list(value, "non_claims", errors, relative)

    record = value.get("claim_ledger_record")
    if not isinstance(record, dict):
        errors.append(f"{relative}: claim_ledger_record must be an object.")
        return errors

    owner = f"{relative}:claim_ledger_record"
    for key in ("claim_id", "claim_text", "revision_action", "support_state_before", "support_state_after"):
        require_nonempty_string(record, key, errors, owner)
    for key in (
        "prior_evidence_refs",
        "evidence_refs",
        "revision_history",
        "surface_refs",
        "affected_surfaces",
        "promotion_blockers",
        "review_routes",
        "residuals",
    ):
        require_nonempty_list(record, key, errors, owner)
    if errors:
        return errors

    before = str(record["support_state_before"])
    after = str(record["support_state_after"])
    action = str(record["revision_action"])
    contradiction_refs = record.get("contradiction_refs", [])
    accepted_transition_refs = record.get("accepted_evidence_transition_refs", [])

    if before not in SUPPORT_ORDER:
        errors.append(f"{owner}: unsupported support_state_before {before!r}.")
    if after not in SUPPORT_ORDER:
        errors.append(f"{owner}: unsupported support_state_after {after!r}.")
    if before in SUPPORT_ORDER and after in SUPPORT_ORDER:
        moved_up = SUPPORT_ORDER[after] > SUPPORT_ORDER[before]
        if moved_up and not accepted_transition_refs:
            errors.append(f"{owner}: upward support-state movement requires accepted_evidence_transition_refs.")
        if moved_up and contradiction_refs:
            errors.append(f"{owner}: a contradicted claim cannot move upward in the same revision.")

    if contradiction_refs:
        if action not in CONTRADICTION_ACTIONS:
            errors.append(f"{owner}: contradiction_refs require a downgrade, quarantine, split, residualize, escalate, or deprecate action.")
        if not record.get("promotion_blockers"):
            errors.append(f"{owner}: contradicted revisions must preserve promotion_blockers.")
        if not record.get("review_routes"):
            errors.append(f"{owner}: contradicted revisions must route review.")
        residual_text = as_text(record.get("residuals", [])).lower()
        if "contradiction" not in residual_text and "residual" not in residual_text:
            errors.append(f"{owner}: contradicted revisions must name the contradiction or residual in residuals.")

    if action in STATE_CHANGE_ACTIONS or before != after or contradiction_refs:
        if not record.get("prior_evidence_refs"):
            errors.append(f"{owner}: state-changing revisions must preserve prior_evidence_refs.")
        if not record.get("affected_surfaces"):
            errors.append(f"{owner}: state-changing revisions must name affected_surfaces.")
        if not record.get("surface_refs"):
            errors.append(f"{owner}: state-changing revisions must name surface_refs.")

    revision_history = record.get("revision_history", [])
    if isinstance(revision_history, list):
        for index, revision in enumerate(revision_history, start=1):
            if not isinstance(revision, dict):
                errors.append(f"{owner}: revision_history[{index}] must be an object.")
                continue
            for key in ("revision_id", "reason", "previous_support_state", "new_support_state", "evidence_refs"):
                if key == "evidence_refs":
                    require_nonempty_list(revision, key, errors, f"{owner}:revision_history[{index}]")
                else:
                    require_nonempty_string(revision, key, errors, f"{owner}:revision_history[{index}]")

    non_claim_text = as_text(top_non_claims + record.get("non_claims", [])).lower()
    if "does not promote" not in non_claim_text or "support" not in non_claim_text:
        errors.append(f"{relative}: non_claims must state support-state non-promotion.")
    if "does not prove" not in non_claim_text:
        errors.append(f"{relative}: non_claims must deny stronger proof.")
    for term in ("source interpretation", "runtime", "verifier"):
        if term not in non_claim_text:
            errors.append(f"{relative}: non_claims must deny {term} claims.")

    validate_semantic_variants(record, top_non_claims, errors, owner)
    validate_assumption_contexts(record, top_non_claims, errors, owner)

    return errors


def fixture_expectation(path: Path) -> bool | None:
    if path.name.startswith("valid_"):
        return True
    if path.name.startswith("invalid_"):
        return False
    return None


def main() -> None:
    fixtures = sorted(FIXTURE_DIR.glob("*.json"))
    if not fixtures:
        raise SystemExit(f"No claim-ledger revision fixtures found in {rel(FIXTURE_DIR)}.")

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

        fixture_errors = semantic_errors(value, relative)
        if expect_valid:
            valid_count += 1
            errors.extend(fixture_errors)
        else:
            invalid_count += 1
            if not fixture_errors:
                errors.append(f"{relative}: expected invalid fixture passed validation.")

    if errors:
        print("Claim ledger revision harness failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print(
        "Claim ledger revision harness passed: "
        f"{valid_count} valid fixture(s), {invalid_count} expected-invalid fixture(s)."
    )


if __name__ == "__main__":
    main()
