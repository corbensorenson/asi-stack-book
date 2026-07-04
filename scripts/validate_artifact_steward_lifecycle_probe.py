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
README = ROOT / "README.md"
PUBLICATION = ROOT / "docs" / "publication_readiness.md"
STATUS = ROOT / "docs" / "test_harness_status_ledger.md"

SURFACE_FRAGMENTS = (
    "Artifact steward lifecycle probe",
    "valid_clean_release_review_proposal",
    "valid_sunset_review_route",
    "invalid_tainted_event_without_review",
    "invalid_over_policy_treasury_spend",
    "invalid_contribution_governance_laundering",
    "invalid_unscoped_federation_contract",
    "invalid_release_without_gate_evidence",
    "invalid_sunset_criteria_ordinary_work",
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
    "valid_clean_release_review_proposal": "prepare_release_review",
    "valid_sunset_review_route": "open_sunset_review",
}

EXPECTED_INVALID_ROUTES = {
    "invalid_tainted_event_without_review": "quarantine_event",
    "invalid_over_policy_treasury_spend": "request_treasury_approval",
    "invalid_contribution_governance_laundering": "reject_collapsed_governance",
    "invalid_unscoped_federation_contract": "reject_federation_authority_inheritance",
    "invalid_release_without_gate_evidence": "block_release_evidence_gate",
    "invalid_sunset_criteria_ordinary_work": "open_sunset_review",
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


def main() -> None:
    errors: list[str] = []
    paths = (RESULT, DOC, STRUCTURE, OUTLINE, ROADMAP, LIVE_CHAPTER, READER_CHAPTER, README, PUBLICATION, STATUS)
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
    if not isinstance(valid, list) or len(valid) != 2:
        errors.append(f"{rel(RESULT)}: expected two valid scenarios.")
        valid = []
    if not isinstance(invalid, list) or len(invalid) != 6:
        errors.append(f"{rel(RESULT)}: expected six invalid controls.")
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
        if scenario_id == "valid_clean_release_review_proposal":
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
        if scenario_id == "invalid_contribution_governance_laundering":
            if scenario.get("outcome", {}).get("governance_effect_allowed") is not False:
                errors.append(f"{owner}: collapsed governance contribution must be denied.")
        if scenario_id == "invalid_sunset_criteria_ordinary_work":
            if scenario.get("outcome", {}).get("ordinary_work_allowed") is not False:
                errors.append(f"{owner}: ordinary work must be blocked.")

    summary = result.get("summary", {})
    if summary.get("valid_scenarios") != 2:
        errors.append(f"{rel(RESULT)}: summary.valid_scenarios must be 2.")
    if summary.get("expected_invalid_controls") != 6:
        errors.append(f"{rel(RESULT)}: summary.expected_invalid_controls must be 6.")
    expected_digest = decision_digest(valid, invalid)
    if summary.get("decision_digest") != expected_digest:
        errors.append(f"{rel(RESULT)}: decision_digest mismatch.")
    require_sha(summary.get("decision_digest"), f"{rel(RESULT)} summary.decision_digest", errors)

    if result.get("non_claims") != NON_CLAIMS:
        errors.append(f"{rel(RESULT)}: non_claims must match runner boundaries.")
    require_fragments(rel(RESULT), text_blob(result.get("non_claims", [])), REQUIRED_NON_CLAIM_TERMS, errors)

    for owner, path in (
        (rel(DOC), DOC),
        (rel(OUTLINE), OUTLINE),
        (rel(ROADMAP), ROADMAP),
        (rel(LIVE_CHAPTER), LIVE_CHAPTER),
        (rel(READER_CHAPTER), READER_CHAPTER),
        (rel(README), README),
        (rel(PUBLICATION), PUBLICATION),
        (rel(STATUS), STATUS),
    ):
        require_fragments(owner, path.read_text(encoding="utf-8"), SURFACE_FRAGMENTS, errors)

    record = chapter_record(structure, "artifact-steward-agents-and-living-project-governance")
    if record.get("evidence_level") != "argument":
        errors.append("artifact-steward-agents-and-living-project-governance: evidence_level must remain argument.")
    require_fragments(
        "book_structure artifact steward tests",
        text_blob(record.get("codex_tests", [])),
        (
            "Artifact steward lifecycle probe",
            "valid_clean_release_review_proposal",
            "valid_sunset_review_route",
            "six expected-invalid controls",
            "no steward-bot, treasury-executor, event-taint-workflow, contributor-ledger, governance-runner, project-federation, release-runner, sunset-protocol, or support-state-promotion claim",
        ),
        errors,
    )

    if errors:
        fail(errors)
    print(
        "Artifact steward lifecycle probe validation passed: "
        "2 valid routes and 6 expected-invalid controls checked with no steward execution or support-state movement."
    )


if __name__ == "__main__":
    main()
