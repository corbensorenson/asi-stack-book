#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "experiments" / "claim_state_transition_bridge" / "results" / "2026-07-04-local.json"
DOC = ROOT / "docs" / "claim_state_transition_bridge.md"
CHAPTER = ROOT / "chapters" / "evidence-states-and-claim-discipline.qmd"
READER = (
    ROOT
    / "editions"
    / "reader_manuscript"
    / "v1_0"
    / "chapters"
    / "evidence-states-and-claim-discipline.qmd"
)
OUTLINE = ROOT / "docs" / "book_outline.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
CHANGELOG = ROOT / "appendices" / "F_changelog.qmd"
MANIFEST = ROOT / "book_structure.json"
VALIDATION_REGISTRY = ROOT / "validation" / "registry.json"
LEAN_FILE = ROOT / "lean" / "AsiStackProofs" / "EvidenceStates.lean"

COMMAND = "python3 scripts/validate_claim_state_transition_bridge.py"
CODEX_TEST_NAME = "Claim-state transition bridge"
PROOF_TAG = "lean:evidence.claim_state.transition_bridge"
LEAN_THEOREMS = [
    "claim_state_transition_bridge_fixture_valid",
    "claim_state_transition_bridge_requires_negative_evidence",
    "claim_state_transition_bridge_preserves_no_live_claim_movement",
    "claim_state_transition_bridge_preserves_nonclaim_boundary",
]

REQUIRED_NON_CLAIMS = [
    "does not demote, deprecate, or refute any live chapter core claim",
    "does not prove source interpretation adequacy",
    "does not prove reviewer correctness",
    "does not create a support-state promotion",
    "does not prove deployed belief-revision behavior",
]

SCENARIOS: list[dict[str, Any]] = [
    {
        "scenario_id": "valid_scope_narrowing_after_failed_mapping",
        "expect_valid": True,
        "transition_kind": "claim_narrowing",
        "old_support_state": "argument",
        "new_support_state": "argument",
        "support_state_effect": "none",
        "claim_revision_ref": "claim_revisions/synthetic/narrowing_failed_mapping.json",
        "negative_evidence_refs": ["negative_evidence/synthetic/failed_source_mapping.json"],
        "downgrade_triggers": [],
        "terminal_effect_recorded": False,
        "review_status": "accepted",
        "reviewer_refs": ["review/synthetic/evidence-chair"],
        "changelog_ref": "appendices/F_changelog.qmd#synthetic-claim-state-bridge",
        "non_claim_boundary": True,
        "live_claim_effect": "synthetic_fixture_only",
    },
    {
        "scenario_id": "valid_downgrade_after_failed_replay",
        "expect_valid": True,
        "transition_kind": "support_downgrade",
        "old_support_state": "synthetic-test-backed",
        "new_support_state": "argument",
        "support_state_effect": "blocks_promotion",
        "claim_revision_ref": "claim_revisions/synthetic/downgrade_failed_replay.json",
        "negative_evidence_refs": ["negative_evidence/synthetic/failed_replay.json"],
        "downgrade_triggers": ["failed_replay"],
        "terminal_effect_recorded": False,
        "review_status": "accepted",
        "reviewer_refs": ["review/synthetic/evidence-chair"],
        "changelog_ref": "appendices/F_changelog.qmd#synthetic-claim-state-bridge",
        "non_claim_boundary": True,
        "live_claim_effect": "synthetic_fixture_only",
    },
    {
        "scenario_id": "valid_terminal_refutation_after_counterexample",
        "expect_valid": True,
        "transition_kind": "terminal_refutation",
        "old_support_state": "argument",
        "new_support_state": "refuted",
        "support_state_effect": "blocks_promotion",
        "claim_revision_ref": "claim_revisions/synthetic/refutation_counterexample.json",
        "negative_evidence_refs": ["negative_evidence/synthetic/counterexample.json"],
        "downgrade_triggers": ["counterexample"],
        "terminal_effect_recorded": True,
        "review_status": "accepted",
        "reviewer_refs": ["review/synthetic/evidence-chair"],
        "changelog_ref": "appendices/F_changelog.qmd#synthetic-claim-state-bridge",
        "non_claim_boundary": True,
        "live_claim_effect": "synthetic_fixture_only",
    },
    {
        "scenario_id": "invalid_narrowing_without_negative_evidence",
        "expect_valid": False,
        "transition_kind": "claim_narrowing",
        "old_support_state": "argument",
        "new_support_state": "argument",
        "support_state_effect": "none",
        "claim_revision_ref": "claim_revisions/synthetic/narrowing_missing_negative_evidence.json",
        "negative_evidence_refs": [],
        "downgrade_triggers": [],
        "terminal_effect_recorded": False,
        "review_status": "accepted",
        "reviewer_refs": ["review/synthetic/evidence-chair"],
        "changelog_ref": "appendices/F_changelog.qmd#synthetic-claim-state-bridge",
        "non_claim_boundary": True,
        "live_claim_effect": "synthetic_fixture_only",
    },
    {
        "scenario_id": "invalid_downgrade_without_trigger",
        "expect_valid": False,
        "transition_kind": "support_downgrade",
        "old_support_state": "synthetic-test-backed",
        "new_support_state": "argument",
        "support_state_effect": "blocks_promotion",
        "claim_revision_ref": "claim_revisions/synthetic/downgrade_missing_trigger.json",
        "negative_evidence_refs": ["negative_evidence/synthetic/failed_replay.json"],
        "downgrade_triggers": [],
        "terminal_effect_recorded": False,
        "review_status": "accepted",
        "reviewer_refs": ["review/synthetic/evidence-chair"],
        "changelog_ref": "appendices/F_changelog.qmd#synthetic-claim-state-bridge",
        "non_claim_boundary": True,
        "live_claim_effect": "synthetic_fixture_only",
    },
    {
        "scenario_id": "invalid_refutation_without_terminal_effect",
        "expect_valid": False,
        "transition_kind": "terminal_refutation",
        "old_support_state": "argument",
        "new_support_state": "refuted",
        "support_state_effect": "blocks_promotion",
        "claim_revision_ref": "claim_revisions/synthetic/refutation_missing_terminal_effect.json",
        "negative_evidence_refs": ["negative_evidence/synthetic/counterexample.json"],
        "downgrade_triggers": ["counterexample"],
        "terminal_effect_recorded": False,
        "review_status": "accepted",
        "reviewer_refs": ["review/synthetic/evidence-chair"],
        "changelog_ref": "appendices/F_changelog.qmd#synthetic-claim-state-bridge",
        "non_claim_boundary": True,
        "live_claim_effect": "synthetic_fixture_only",
    },
    {
        "scenario_id": "invalid_support_promotion_laundered_as_narrowing",
        "expect_valid": False,
        "transition_kind": "claim_narrowing",
        "old_support_state": "argument",
        "new_support_state": "source-derived",
        "support_state_effect": "eligible_for_bounded_evidence_review",
        "claim_revision_ref": "claim_revisions/synthetic/narrowing_laundered_promotion.json",
        "negative_evidence_refs": ["negative_evidence/synthetic/failed_source_mapping.json"],
        "downgrade_triggers": [],
        "terminal_effect_recorded": False,
        "review_status": "accepted",
        "reviewer_refs": ["review/synthetic/evidence-chair"],
        "changelog_ref": "appendices/F_changelog.qmd#synthetic-claim-state-bridge",
        "non_claim_boundary": True,
        "live_claim_effect": "synthetic_fixture_only",
    },
    {
        "scenario_id": "invalid_missing_nonclaim_boundary",
        "expect_valid": False,
        "transition_kind": "support_downgrade",
        "old_support_state": "synthetic-test-backed",
        "new_support_state": "argument",
        "support_state_effect": "blocks_promotion",
        "claim_revision_ref": "claim_revisions/synthetic/downgrade_missing_nonclaim.json",
        "negative_evidence_refs": ["negative_evidence/synthetic/failed_replay.json"],
        "downgrade_triggers": ["failed_replay"],
        "terminal_effect_recorded": False,
        "review_status": "accepted",
        "reviewer_refs": ["review/synthetic/evidence-chair"],
        "changelog_ref": "appendices/F_changelog.qmd#synthetic-claim-state-bridge",
        "non_claim_boundary": False,
        "live_claim_effect": "synthetic_fixture_only",
    },
    {
        "scenario_id": "invalid_live_claim_movement_claimed",
        "expect_valid": False,
        "transition_kind": "claim_narrowing",
        "old_support_state": "argument",
        "new_support_state": "argument",
        "support_state_effect": "none",
        "claim_revision_ref": "claim_revisions/synthetic/narrowing_live_claim_movement.json",
        "negative_evidence_refs": ["negative_evidence/synthetic/failed_source_mapping.json"],
        "downgrade_triggers": [],
        "terminal_effect_recorded": False,
        "review_status": "accepted",
        "reviewer_refs": ["review/synthetic/evidence-chair"],
        "changelog_ref": "appendices/F_changelog.qmd#synthetic-claim-state-bridge",
        "non_claim_boundary": True,
        "live_claim_effect": "live_core_claim_moved",
    },
]

SUPPORT_RANK = {
    "unsupported": 0,
    "argument": 1,
    "source-derived": 2,
    "external-literature-backed": 2,
    "prototype-backed": 3,
    "synthetic-test-backed": 4,
    "empirical-test-backed": 5,
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Claim-state transition bridge validation failed:")
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


def nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def nonempty_list(value: Any) -> bool:
    return isinstance(value, list) and bool(value)


def scenario_rejection_reasons(scenario: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    transition_kind = scenario.get("transition_kind")
    old_state = scenario.get("old_support_state")
    new_state = scenario.get("new_support_state")
    support_effect = scenario.get("support_state_effect")

    if transition_kind not in {"claim_narrowing", "support_downgrade", "terminal_refutation"}:
        reasons.append("unknown_transition_kind")
    if not nonempty_string(scenario.get("claim_revision_ref")):
        reasons.append("missing_claim_revision_ref")
    if not nonempty_list(scenario.get("negative_evidence_refs")):
        reasons.append("missing_negative_evidence")
    if scenario.get("review_status") != "accepted":
        reasons.append("missing_accepted_review")
    if not nonempty_list(scenario.get("reviewer_refs")):
        reasons.append("missing_reviewer_refs")
    if not nonempty_string(scenario.get("changelog_ref")):
        reasons.append("missing_changelog_ref")
    if scenario.get("non_claim_boundary") is not True:
        reasons.append("missing_non_claim_boundary")
    if scenario.get("live_claim_effect") != "synthetic_fixture_only":
        reasons.append("live_claim_movement_claimed")

    if transition_kind == "claim_narrowing":
        if old_state != new_state:
            reasons.append("narrowing_changed_support_state")
        if support_effect != "none":
            reasons.append("narrowing_changed_support_effect")
    if transition_kind == "support_downgrade":
        if old_state not in SUPPORT_RANK or new_state not in SUPPORT_RANK:
            reasons.append("downgrade_uses_unknown_ranked_state")
        elif SUPPORT_RANK[new_state] >= SUPPORT_RANK[old_state]:
            reasons.append("downgrade_did_not_lower_rank")
        if support_effect != "blocks_promotion":
            reasons.append("downgrade_must_block_promotion")
        if not nonempty_list(scenario.get("downgrade_triggers")):
            reasons.append("missing_downgrade_trigger")
        if scenario.get("terminal_effect_recorded") is True:
            reasons.append("downgrade_cannot_record_terminal_effect")
    if transition_kind == "terminal_refutation":
        if new_state != "refuted":
            reasons.append("refutation_must_end_refuted")
        if support_effect != "blocks_promotion":
            reasons.append("refutation_must_block_promotion")
        if not nonempty_list(scenario.get("downgrade_triggers")):
            reasons.append("missing_refutation_trigger")
        if scenario.get("terminal_effect_recorded") is not True:
            reasons.append("missing_terminal_effect")

    if support_effect == "eligible_for_bounded_evidence_review":
        reasons.append("support_promotion_laundering_attempt")

    return sorted(set(reasons))


def build_result(errors: list[str]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    valid_scenarios: list[str] = []
    rejected_controls: list[dict[str, Any]] = []

    for scenario in SCENARIOS:
        reasons = scenario_rejection_reasons(scenario)
        actual_valid = not reasons
        expected_valid = scenario.get("expect_valid") is True
        scenario_id = str(scenario.get("scenario_id", ""))
        if expected_valid and not actual_valid:
            errors.append(f"{scenario_id}: expected valid but rejected: {', '.join(reasons)}.")
        if not expected_valid and actual_valid:
            errors.append(f"{scenario_id}: expected invalid but no rejection reason was produced.")
        if expected_valid:
            valid_scenarios.append(scenario_id)
        else:
            rejected_controls.append({"scenario_id": scenario_id, "rejection_reasons": reasons})
        rows.append(
            {
                "scenario_id": scenario_id,
                "expected_valid": expected_valid,
                "actual_valid": actual_valid,
                "transition_kind": scenario.get("transition_kind"),
                "old_support_state": scenario.get("old_support_state"),
                "new_support_state": scenario.get("new_support_state"),
                "support_state_effect": scenario.get("support_state_effect"),
                "rejection_reasons": reasons,
            }
        )

    kinds = {row["transition_kind"] for row in rows if row["actual_valid"]}
    assertions = {
        "narrowing_case_present": "claim_narrowing" in kinds,
        "downgrade_case_present": "support_downgrade" in kinds,
        "refutation_case_present": "terminal_refutation" in kinds,
        "negative_evidence_required": any(
            row["scenario_id"] == "invalid_narrowing_without_negative_evidence"
            and "missing_negative_evidence" in row["rejection_reasons"]
            for row in rows
        ),
        "downgrade_trigger_required": any(
            row["scenario_id"] == "invalid_downgrade_without_trigger"
            and "missing_downgrade_trigger" in row["rejection_reasons"]
            for row in rows
        ),
        "terminal_effect_required": any(
            row["scenario_id"] == "invalid_refutation_without_terminal_effect"
            and "missing_terminal_effect" in row["rejection_reasons"]
            for row in rows
        ),
        "support_promotion_laundering_rejected": any(
            row["scenario_id"] == "invalid_support_promotion_laundered_as_narrowing"
            and "support_promotion_laundering_attempt" in row["rejection_reasons"]
            for row in rows
        ),
        "no_live_claim_movement": any(
            row["scenario_id"] == "invalid_live_claim_movement_claimed"
            and "live_claim_movement_claimed" in row["rejection_reasons"]
            for row in rows
        )
        and all(scenario.get("live_claim_effect") == "synthetic_fixture_only" for scenario in SCENARIOS if scenario.get("expect_valid")),
        "non_claim_boundary": any(
            row["scenario_id"] == "invalid_missing_nonclaim_boundary"
            and "missing_non_claim_boundary" in row["rejection_reasons"]
            for row in rows
        ),
        "support_state_effect_bounded": all(
            row["support_state_effect"] in {"none", "blocks_promotion"} for row in rows if row["actual_valid"]
        ),
    }
    for key, value in assertions.items():
        if value is not True:
            errors.append(f"bridge_assertions.{key} must be true.")

    return {
        "schema_version": "asi_stack.claim_state_transition_bridge.v0",
        "result_id": "2026-07-04-claim-state-transition-bridge",
        "recorded_date": "2026-07-04",
        "command": COMMAND,
        "result_kind": "deterministic_synthetic_claim_state_transition_bridge",
        "valid_scenario_count": len(valid_scenarios),
        "expected_invalid_control_count": len(rejected_controls),
        "valid_scenarios": sorted(valid_scenarios),
        "rejected_controls": rejected_controls,
        "scenario_results": rows,
        "bridge_assertions": assertions,
        "lean_fixture_alignment": {
            "proof_tag": PROOF_TAG,
            "valid_scenario_count": 3,
            "expected_invalid_control_count": 6,
            "negative_evidence_required": True,
            "support_state_effect_bounded": True,
            "no_live_claim_movement": True,
            "theorem_refs": LEAN_THEOREMS,
        },
        "weakening_condition": (
            "The support-state ladder soundness argument weakens if failed evidence "
            "cannot produce a recorded narrowing, downgrade, or refutation without "
            "also allowing support promotion, live-claim movement, or erased non-claims."
        ),
        "non_claims": REQUIRED_NON_CLAIMS,
    }


def validate_record(record: dict[str, Any], errors: list[str]) -> None:
    if record.get("schema_version") != "asi_stack.claim_state_transition_bridge.v0":
        errors.append(f"{rel(RESULT)} schema_version mismatch.")
    if record.get("result_id") != "2026-07-04-claim-state-transition-bridge":
        errors.append(f"{rel(RESULT)} result_id mismatch.")
    if record.get("recorded_date") != "2026-07-04":
        errors.append(f"{rel(RESULT)} recorded_date mismatch.")
    if record.get("command") != COMMAND:
        errors.append(f"{rel(RESULT)} command mismatch.")
    if record.get("valid_scenario_count") != 3:
        errors.append(f"{rel(RESULT)} valid_scenario_count must be 3.")
    if record.get("expected_invalid_control_count") != 6:
        errors.append(f"{rel(RESULT)} expected_invalid_control_count must be 6.")
    assertions = record.get("bridge_assertions")
    if not isinstance(assertions, dict) or not all(value is True for value in assertions.values()):
        errors.append(f"{rel(RESULT)} bridge_assertions must all be true.")
    alignment = record.get("lean_fixture_alignment")
    if not isinstance(alignment, dict):
        errors.append(f"{rel(RESULT)} lean_fixture_alignment must be an object.")
    else:
        if alignment.get("proof_tag") != PROOF_TAG:
            errors.append(f"{rel(RESULT)} lean proof tag mismatch.")
        if alignment.get("theorem_refs") != LEAN_THEOREMS:
            errors.append(f"{rel(RESULT)} theorem refs mismatch.")
    non_claim_text = text_blob(record.get("non_claims"))
    for phrase in REQUIRED_NON_CLAIMS:
        if phrase.lower() not in non_claim_text:
            errors.append(f"{rel(RESULT)} non_claims missing {phrase!r}.")


def require_text(path: Path, phrases: list[str], errors: list[str]) -> None:
    if not path.exists():
        errors.append(f"{rel(path)} missing.")
        return
    text = path.read_text(encoding="utf-8")
    normalized = " ".join(text.lower().split())
    for phrase in phrases:
        if " ".join(phrase.lower().split()) not in normalized:
            errors.append(f"{rel(path)} missing required phrase: {phrase}")


def validate_surfaces(errors: list[str]) -> None:
    require_text(
        LEAN_FILE,
        [
            "ClaimStateTransitionBridgeSummary",
            "claimStateTransitionBridgeFixture",
            *LEAN_THEOREMS,
        ],
        errors,
    )
    require_text(
        DOC,
        [
            "Claim-State Transition Bridge",
            COMMAND,
            "valid_scope_narrowing_after_failed_mapping",
            "valid_downgrade_after_failed_replay",
            "valid_terminal_refutation_after_counterexample",
            "invalid_support_promotion_laundered_as_narrowing",
            "does not demote, deprecate, or refute any live chapter core claim",
        ],
        errors,
    )
    require_text(
        CHAPTER,
        [
            CODEX_TEST_NAME,
            COMMAND,
            PROOF_TAG,
            "claim narrowing",
            "does not demote, deprecate, or refute any live chapter core claim",
        ],
        errors,
    )
    require_text(
        READER,
        [
            "claim-state transition bridge",
            "narrowed, downgraded, or refuted",
            "does not demote, deprecate, or refute any live chapter core claim",
        ],
        errors,
    )
    require_text(
        OUTLINE,
        [
            CODEX_TEST_NAME,
            COMMAND,
            PROOF_TAG,
            "claim narrowing, support downgrade, terminal refutation",
        ],
        errors,
    )
    require_text(
        ROADMAP,
        [
            "claim-state transition bridge",
            "true demotion/refutation/narrowing",
            "support-state ladder / evidence-state soundness",
        ],
        errors,
    )
    require_text(
        CHANGELOG,
        [
            "Claim-state transition bridge",
            COMMAND,
            PROOF_TAG,
        ],
        errors,
    )
    require_text(
        VALIDATION_REGISTRY,
        [
            "scripts/validate_claim_state_transition_bridge.py",
            "docs/claim_state_transition_bridge.md",
            "experiments/claim_state_transition_bridge/results/2026-07-04-local.json",
            '"script": "validate_claim_state_transition_bridge.py"',
        ],
        errors,
    )

    manifest = load_json(MANIFEST)
    manifest_text = text_blob(manifest)
    for phrase in [CODEX_TEST_NAME.lower(), PROOF_TAG.lower(), COMMAND.lower()]:
        if phrase not in manifest_text:
            errors.append(f"{rel(MANIFEST)} missing {phrase}.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-result", action="store_true")
    args = parser.parse_args()

    errors: list[str] = []
    built = build_result(errors)
    if errors:
        fail(errors)
    if args.write_result:
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(json.dumps(built, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if not RESULT.exists():
        errors.append(f"{rel(RESULT)} missing; run {COMMAND} --write-result.")
    else:
        recorded = load_json(RESULT)
        validate_record(recorded, errors)
        if recorded != built:
            errors.append(f"{rel(RESULT)} is stale; rerun {COMMAND} --write-result.")

    validate_surfaces(errors)
    if errors:
        fail(errors)
    print("Claim-state transition bridge validation passed.")


if __name__ == "__main__":
    main()
