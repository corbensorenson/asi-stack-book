#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

from run_artifact_steward_lifecycle_probe import (
    EXPECTED_INVALID_IDS,
    NON_CLAIMS,
    PROBE_ID,
    RESULT,
    RESULT_COMMAND,
    ROOT,
    VALID_SCENARIO_IDS,
    decision_digest,
)


DOC = ROOT / "docs" / "artifact_steward_lifecycle_probe.md"
STRUCTURE = ROOT / "book_structure.json"
OUTLINE = ROOT / "docs" / "book_outline.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
LIVE_CHAPTER = ROOT / "chapters" / "artifact-steward-agents-and-living-project-governance.qmd"
READER_CHAPTER = (
    ROOT
    / "editions"
    / "reader_manuscript"
    / "v1_0"
    / "chapters"
    / "artifact-steward-agents-and-living-project-governance.qmd"
)
PUBLICATION = ROOT / "docs" / "publication_readiness.md"
STATUS = ROOT / "docs" / "test_harness_status_ledger.md"
LEAN_MODULE = ROOT / "lean" / "AsiStackProofs" / "ArtifactStewardAgents.lean"

SURFACE_FRAGMENTS = (
    "Artifact steward lifecycle probe",
    "valid_bounded_work_dispatch_proposal",
    "23 expected-invalid controls",
    "support-state-promotion claim",
)

READER_SURFACE_FRAGMENTS = (
    "Artifact steward lifecycle probe",
    "clean release-review proposal",
    "sunset-review route",
    "tainted events without review",
    "over-policy treasury spending",
    "contribution governance laundering",
    "unscoped federation contracts",
    "releases without gate evidence",
    "ordinary work mislabeled as sunset criteria",
    "not to claim a working project manager",
    "bounded fixture-route check",
    "no steward-bot, treasury-executor, event-taint-workflow, contributor-ledger, governance-runner, project-federation, release-runner, sunset-protocol, or support-state-promotion claim",
)

REQUIRED_NON_CLAIM_TERMS = (
    "does not promote any chapter core claim",
    "does not create a support-state transition",
    "steward bot",
    "treasury executor",
    "event-taint workflow",
    "governance runner",
    "contributor-ledger service",
    "project federation harness",
    "release runner",
    "sunset protocol",
    "does not move funds",
    "does not copy private source text",
)

EXPECTED_VALID_ROUTES = {
    "valid_bounded_work_dispatch_proposal": "prepare_bounded_work_dispatch",
    "valid_clean_release_review_proposal": "prepare_release_review",
    "valid_sunset_review_route": "open_sunset_review",
}

EXPECTED_INVALID_ROUTES = {
    "invalid_tainted_event_without_review": "quarantine_event",
    "invalid_over_policy_treasury_spend": "request_treasury_approval",
    "invalid_contribution_governance_laundering": "reject_collapsed_governance",
    "invalid_unscoped_federation_contract": "reject_federation_authority_inheritance",
    "invalid_release_without_gate_evidence": "repair_release_evidence",
    "invalid_sunset_criteria_ordinary_work": "open_sunset_review",
    "invalid_work_missing_objective": "repair_work_objective",
    "invalid_work_missing_authority": "repair_work_authority",
    "invalid_work_authority_widening": "refuse_work_authority_widening",
    "invalid_work_missing_tool_boundary": "repair_work_tool_boundary",
    "invalid_work_missing_verification": "repair_work_verification",
    "invalid_work_missing_budget": "repair_work_budget",
    "invalid_work_over_policy_budget": "request_work_budget_approval",
    "invalid_work_missing_rollback": "repair_work_rollback",
    "invalid_work_missing_non_claim_boundary": "repair_work_non_claim_boundary",
    "invalid_release_missing_artifact_binding": "repair_release_artifact_binding",
    "invalid_release_missing_tests": "repair_release_tests",
    "invalid_release_missing_evidence": "repair_release_evidence",
    "invalid_release_missing_changelog": "repair_release_changelog",
    "invalid_release_missing_residuals": "repair_release_residuals",
    "invalid_release_missing_approval": "request_release_approval",
    "invalid_release_support_promotion": "refuse_release_support_promotion",
    "invalid_release_missing_non_claim_boundary": "repair_release_non_claim_boundary",
}

REQUIRED_LEAN_THEOREMS = {
    "dispatch_ready_requires_complete_work_contract",
    "steward_dispatch_step_preserves_contract_safety",
    "steward_dispatch_run_ready_requires_complete_contract",
    "complete_work_contract_reaches_dispatch_ready",
    "missing_work_objective_reaches_repair",
    "missing_work_authority_reaches_repair",
    "widened_work_authority_reaches_refusal",
    "missing_work_tool_boundary_reaches_repair",
    "missing_work_verification_reaches_repair",
    "missing_work_budget_reaches_repair",
    "over_policy_work_budget_reaches_approval",
    "missing_work_rollback_reaches_repair",
    "missing_work_non_claim_boundary_reaches_repair",
    "release_review_ready_requires_complete_packet",
    "steward_release_step_preserves_packet_safety",
    "steward_release_run_ready_requires_complete_packet",
    "complete_release_packet_reaches_external_review_ready",
    "missing_release_artifact_binding_reaches_repair",
    "missing_release_tests_reaches_repair",
    "missing_release_evidence_reaches_repair",
    "missing_release_changelog_reaches_repair",
    "missing_release_residuals_reaches_repair",
    "missing_release_approval_reaches_approval_request",
    "release_support_promotion_reaches_refusal",
    "missing_release_non_claim_boundary_reaches_repair",
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def text_blob(value: Any) -> str:
    if isinstance(value, dict):
        return "\n".join(f"{key}: {text_blob(child)}" for key, child in value.items())
    if isinstance(value, list):
        return "\n".join(text_blob(item) for item in value)
    return str(value)


def normalize(text: str) -> str:
    return " ".join(text.lower().split())


def require_fragments(owner: str, text: str, fragments: tuple[str, ...], errors: list[str]) -> None:
    normalized = normalize(text)
    for fragment in fragments:
        if normalize(fragment) not in normalized:
            errors.append(f"{owner} missing required fragment: {fragment}")


def chapter_record(structure: dict[str, Any], chapter_id: str) -> dict[str, Any]:
    for part in structure.get("parts", []):
        if not isinstance(part, dict):
            continue
        for chapter in part.get("chapters", []):
            if isinstance(chapter, dict) and chapter.get("id") == chapter_id:
                return chapter
    return {}


def fail(errors: list[str]) -> None:
    print("Artifact steward lifecycle probe validation failed:", file=sys.stderr)
    for error in errors:
        print(f" - {error}", file=sys.stderr)
    raise SystemExit(1)


def require_sha(value: Any, owner: str, errors: list[str]) -> None:
    if not re.fullmatch(r"[0-9a-f]{64}", str(value)):
        errors.append(f"{owner} must be a SHA-256 hex digest.")


def require_no_effects(scenario: dict[str, Any], owner: str, errors: list[str]) -> None:
    outcome = scenario.get("outcome", {})
    for key in (
        "release_published",
        "spend_executed",
        "external_worker_dispatched",
        "worker_authority_inherited",
    ):
        if outcome.get(key) is not False:
            errors.append(f"{owner}: outcome.{key} must be false.")
    if outcome.get("support_state_effect") != "none":
        errors.append(f"{owner}: support_state_effect must be none.")
    if outcome.get("chapter_core_support_effect") != "none":
        errors.append(f"{owner}: chapter_core_support_effect must be none.")


def classify_work_contract(contract: dict[str, Any]) -> str:
    if not contract.get("work_requested"):
        return "refuse_no_work_request"
    if not contract.get("objective_present"):
        return "repair_work_objective"
    if not contract.get("authority_basis_present"):
        return "repair_work_authority"
    if not contract.get("authority_within_charter"):
        return "refuse_work_authority_widening"
    if not contract.get("allowed_tools_recorded") or not contract.get("forbidden_tools_recorded"):
        return "repair_work_tool_boundary"
    if not contract.get("verification_plan_present"):
        return "repair_work_verification"
    if not contract.get("budget_present"):
        return "repair_work_budget"
    if not contract.get("budget_within_policy"):
        return "request_work_budget_approval"
    if not contract.get("rollback_plan_present"):
        return "repair_work_rollback"
    if not contract.get("non_claim_boundary_present"):
        return "repair_work_non_claim_boundary"
    return "prepare_bounded_work_dispatch"


def classify_release_review(review: dict[str, Any]) -> str:
    if not review.get("release_candidate_requested"):
        return "refuse_no_release_candidate"
    if not review.get("artifact_binding_present"):
        return "repair_release_artifact_binding"
    if not review.get("tests_recorded"):
        return "repair_release_tests"
    if not review.get("evidence_recorded"):
        return "repair_release_evidence"
    if not review.get("changelog_recorded"):
        return "repair_release_changelog"
    if not review.get("residuals_recorded"):
        return "repair_release_residuals"
    if not review.get("approval_recorded"):
        return "request_release_approval"
    if not review.get("support_state_effect_none") or not review.get("chapter_core_effect_none"):
        return "refuse_release_support_promotion"
    if not review.get("non_claim_boundary_present"):
        return "repair_release_non_claim_boundary"
    return "prepare_release_review"


def validate_independent_mutations(errors: list[str]) -> None:
    work = {
        "work_requested": True,
        "objective_present": True,
        "authority_basis_present": True,
        "authority_within_charter": True,
        "allowed_tools_recorded": True,
        "forbidden_tools_recorded": True,
        "verification_plan_present": True,
        "budget_present": True,
        "budget_within_policy": True,
        "rollback_plan_present": True,
        "non_claim_boundary_present": True,
    }
    work_mutations = {
        "objective_present": "repair_work_objective",
        "authority_basis_present": "repair_work_authority",
        "authority_within_charter": "refuse_work_authority_widening",
        "forbidden_tools_recorded": "repair_work_tool_boundary",
        "verification_plan_present": "repair_work_verification",
        "budget_present": "repair_work_budget",
        "budget_within_policy": "request_work_budget_approval",
        "rollback_plan_present": "repair_work_rollback",
        "non_claim_boundary_present": "repair_work_non_claim_boundary",
    }
    if classify_work_contract(work) != "prepare_bounded_work_dispatch":
        errors.append("Independent complete work-contract route must reach bounded dispatch review.")
    for field, expected in work_mutations.items():
        mutated = dict(work)
        mutated[field] = False
        if classify_work_contract(mutated) != expected:
            errors.append(f"Independent work-contract mutation {field} did not reach {expected}.")

    release = {
        "release_candidate_requested": True,
        "artifact_binding_present": True,
        "tests_recorded": True,
        "evidence_recorded": True,
        "changelog_recorded": True,
        "residuals_recorded": True,
        "approval_recorded": True,
        "support_state_effect_none": True,
        "chapter_core_effect_none": True,
        "non_claim_boundary_present": True,
    }
    release_mutations = {
        "artifact_binding_present": "repair_release_artifact_binding",
        "tests_recorded": "repair_release_tests",
        "evidence_recorded": "repair_release_evidence",
        "changelog_recorded": "repair_release_changelog",
        "residuals_recorded": "repair_release_residuals",
        "approval_recorded": "request_release_approval",
        "support_state_effect_none": "refuse_release_support_promotion",
        "non_claim_boundary_present": "repair_release_non_claim_boundary",
    }
    if classify_release_review(release) != "prepare_release_review":
        errors.append("Independent complete release packet must reach external review readiness.")
    for field, expected in release_mutations.items():
        mutated = dict(release)
        mutated[field] = False
        if classify_release_review(mutated) != expected:
            errors.append(f"Independent release mutation {field} did not reach {expected}.")


def main() -> None:
    errors: list[str] = []
    paths = (
        RESULT,
        DOC,
        STRUCTURE,
        OUTLINE,
        ROADMAP,
        LIVE_CHAPTER,
        READER_CHAPTER,
        PUBLICATION,
        STATUS,
        LEAN_MODULE,
    )
    for path in paths:
        if not path.exists():
            errors.append(f"Missing {rel(path)}.")
    if errors:
        fail(errors)

    result = load_json(RESULT)
    structure = load_json(STRUCTURE)
    blob = text_blob(result)
    if "/Users/" in blob or "/var/folders/" in blob:
        errors.append(f"{rel(RESULT)} must not publish local absolute paths.")

    expected_scalars = {
        "probe_id": PROBE_ID,
        "record_kind": "artifact_steward_lifecycle_probe",
        "command": RESULT_COMMAND,
        "local_only": True,
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
        "pass": True,
    }
    for key, expected in expected_scalars.items():
        if result.get(key) != expected:
            errors.append(f"{rel(RESULT)}: {key} must be {expected!r}.")
    if not isinstance(result.get("recorded_at_utc"), str) or not result["recorded_at_utc"].endswith("Z"):
        errors.append(f"{rel(RESULT)}: recorded_at_utc must end with Z.")

    fixture_summary = result.get("fixture_summary", {})
    for fixture_name, fixture in fixture_summary.items():
        if not isinstance(fixture, dict):
            errors.append(f"{rel(RESULT)}: fixture_summary.{fixture_name} must be an object.")
            continue
        ref = ROOT / str(fixture.get("ref", ""))
        if not ref.exists():
            errors.append(f"{rel(RESULT)}: fixture ref missing: {fixture.get('ref')!r}.")
        require_sha(fixture.get("sha256"), f"{rel(RESULT)} fixture_summary.{fixture_name}.sha256", errors)
        if not isinstance(fixture.get("top_level_keys"), list) or not fixture["top_level_keys"]:
            errors.append(f"{rel(RESULT)}: fixture_summary.{fixture_name}.top_level_keys must be non-empty.")

    valid = result.get("valid_scenarios", [])
    invalid = result.get("expected_invalid_controls", [])
    if not isinstance(valid, list) or len(valid) != 3:
        errors.append(f"{rel(RESULT)}: expected three valid scenarios.")
        valid = []
    if not isinstance(invalid, list) or len(invalid) != 23:
        errors.append(f"{rel(RESULT)}: expected 23 invalid controls.")
        invalid = []

    seen_valid = {scenario.get("scenario_id") for scenario in valid if isinstance(scenario, dict)}
    seen_invalid = {scenario.get("scenario_id") for scenario in invalid if isinstance(scenario, dict)}
    if seen_valid != VALID_SCENARIO_IDS:
        errors.append(f"{rel(RESULT)}: valid scenario ids mismatch: {sorted(seen_valid)}.")
    if seen_invalid != EXPECTED_INVALID_IDS:
        errors.append(f"{rel(RESULT)}: invalid control ids mismatch: {sorted(seen_invalid)}.")

    for scenario in valid:
        scenario_id = scenario.get("scenario_id")
        owner = f"{rel(RESULT)} {scenario_id}"
        if scenario.get("expected_valid") is not True:
            errors.append(f"{owner}: expected_valid must be true.")
        if scenario.get("actual_route") != EXPECTED_VALID_ROUTES.get(scenario_id):
            errors.append(f"{owner}: route mismatch.")
        if scenario.get("scenario_pass") is not True:
            errors.append(f"{owner}: scenario_pass must be true.")
        require_no_effects(scenario, owner, errors)
        summary_input = scenario.get("input_summary", {})
        if scenario_id == "valid_bounded_work_dispatch_proposal":
            if classify_work_contract(summary_input.get("work_contract_review", {})) != scenario.get("actual_route"):
                errors.append(f"{owner}: independent work-contract route mismatch.")
        if scenario_id == "valid_clean_release_review_proposal":
            if classify_release_review(summary_input.get("release_review", {})) != scenario.get("actual_route"):
                errors.append(f"{owner}: independent release-review route mismatch.")
            if scenario.get("outcome", {}).get("protected_action_allowed") is not True:
                errors.append(f"{owner}: release review proposal should be allowed as proposal-only.")
        if scenario_id == "valid_sunset_review_route":
            if scenario.get("outcome", {}).get("ordinary_work_allowed") is not False:
                errors.append(f"{owner}: sunset route must not allow ordinary work.")

    for scenario in invalid:
        scenario_id = scenario.get("scenario_id")
        owner = f"{rel(RESULT)} {scenario_id}"
        if scenario.get("expected_valid") is not False:
            errors.append(f"{owner}: expected_valid must be false.")
        if scenario.get("actual_route") != EXPECTED_INVALID_ROUTES.get(scenario_id):
            errors.append(f"{owner}: route mismatch.")
        if scenario.get("scenario_pass") is not True:
            errors.append(f"{owner}: scenario_pass must be true.")
        require_no_effects(scenario, owner, errors)
        summary_input = scenario.get("input_summary", {})
        if str(scenario_id).startswith("invalid_work_"):
            if classify_work_contract(summary_input.get("work_contract_review", {})) != scenario.get("actual_route"):
                errors.append(f"{owner}: independent work-contract route mismatch.")
        if str(scenario_id).startswith("invalid_release_"):
            if classify_release_review(summary_input.get("release_review", {})) != scenario.get("actual_route"):
                errors.append(f"{owner}: independent release-review route mismatch.")
        if scenario_id == "invalid_contribution_governance_laundering":
            if scenario.get("outcome", {}).get("governance_effect_allowed") is not False:
                errors.append(f"{owner}: collapsed governance contribution must be denied.")
        if scenario_id == "invalid_sunset_criteria_ordinary_work":
            if scenario.get("outcome", {}).get("ordinary_work_allowed") is not False:
                errors.append(f"{owner}: ordinary work must be blocked.")

    summary = result.get("summary", {})
    if summary.get("valid_scenarios") != 3:
        errors.append(f"{rel(RESULT)}: summary.valid_scenarios must be 3.")
    if summary.get("expected_invalid_controls") != 23:
        errors.append(f"{rel(RESULT)}: summary.expected_invalid_controls must be 23.")
    expected_digest = decision_digest(valid, invalid)
    if summary.get("decision_digest") != expected_digest:
        errors.append(f"{rel(RESULT)}: decision_digest mismatch.")
    require_sha(summary.get("decision_digest"), f"{rel(RESULT)} summary.decision_digest", errors)
    validate_independent_mutations(errors)

    lean_text = LEAN_MODULE.read_text(encoding="utf-8")
    lean_theorems = set(re.findall(r"(?m)^theorem\s+([A-Za-z0-9_']+)", lean_text))
    if len(lean_theorems) != 37:
        errors.append(f"{rel(LEAN_MODULE)} must expose exactly 37 theorem declarations, found {len(lean_theorems)}.")
    missing_theorems = sorted(REQUIRED_LEAN_THEOREMS - lean_theorems)
    if missing_theorems:
        errors.append(f"{rel(LEAN_MODULE)} missing reachable-model theorems: {missing_theorems}.")
    for retired_surface in (
        "dispatched_steward_contract_records_required_boundary",
        "stewarded_release_publication_requires_test_evidence_changelog_residual_and_approval_records",
    ):
        if retired_surface in lean_text:
            errors.append(f"{rel(LEAN_MODULE)} restored retired assumption surface {retired_surface}.")

    if result.get("non_claims") != NON_CLAIMS:
        errors.append(f"{rel(RESULT)}: non_claims must match runner boundaries.")
    require_fragments(rel(RESULT), text_blob(result.get("non_claims", [])), REQUIRED_NON_CLAIM_TERMS, errors)

    for owner, path in (
        (rel(DOC), DOC),
        (rel(OUTLINE), OUTLINE),
        (rel(ROADMAP), ROADMAP),
        (rel(LIVE_CHAPTER), LIVE_CHAPTER),
        (rel(PUBLICATION), PUBLICATION),
        (rel(STATUS), STATUS),
    ):
        require_fragments(owner, path.read_text(encoding="utf-8"), SURFACE_FRAGMENTS, errors)
    require_fragments(rel(READER_CHAPTER), READER_CHAPTER.read_text(encoding="utf-8"), READER_SURFACE_FRAGMENTS, errors)

    record = chapter_record(structure, "artifact-steward-agents-and-living-project-governance")
    if record.get("evidence_level") != "argument":
        errors.append("artifact-steward-agents-and-living-project-governance: evidence_level must remain argument.")
    require_fragments(
        "book_structure artifact steward tests",
        text_blob(record.get("codex_tests", [])),
        (
            "Artifact steward lifecycle probe",
            "valid_clean_release_review_proposal",
            "valid_bounded_work_dispatch_proposal",
            "valid_sunset_review_route",
            "23 expected-invalid controls",
            "no steward-bot, treasury-executor, event-taint-workflow, contributor-ledger, governance-runner, project-federation, release-runner, sunset-protocol, or support-state-promotion claim",
        ),
        errors,
    )

    if errors:
        fail(errors)
    print(
        "Artifact steward lifecycle probe validation passed: "
        "3 valid routes, 23 expected-invalid controls, 17 independent route mutations, "
        "and 37 exact Lean declarations checked with no steward execution or support-state movement."
    )


if __name__ == "__main__":
    main()
