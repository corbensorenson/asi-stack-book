#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

from run_intent_recontract_probe import (
    EXPECTED_INVALID_IDS,
    NON_CLAIMS,
    PROBE_ID,
    RESULT,
    RESULT_COMMAND,
    ROOT,
    VALID_SCENARIO_IDS,
    decision_digest,
)


DOC = ROOT / "docs" / "intent_recontract_probe.md"
STRUCTURE = ROOT / "book_structure.json"
OUTLINE = ROOT / "docs" / "book_outline.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
LIVE_CHAPTER = ROOT / "chapters" / "human-intent-as-a-formal-input.qmd"
READER_CHAPTER = ROOT / "editions" / "reader_manuscript" / "v1_0" / "chapters" / "human-intent-as-a-formal-input.qmd"
README = ROOT / "README.md"
PUBLICATION = ROOT / "docs" / "publication_readiness.md"
STATUS = ROOT / "docs" / "test_harness_status_ledger.md"

SURFACE_FRAGMENTS = (
    "Intent re-contract trigger probe",
    "valid_no_material_delta_continue",
    "valid_publication_surface_delta_recontracts",
    "invalid_authority_delta_without_recontract",
    "invalid_private_source_delta_without_recontract",
    "invalid_stop_condition_erasure_without_recontract",
    "invalid_evidence_bar_weakening_without_recontract",
    "invalid_affected_party_widening_without_recontract",
    "invalid_means_expansion_without_recontract",
    "invalid_support_state_promotion_without_recontract",
    "no natural-language-intent-understanding, deployed-parser-quality, deployed-authority-extraction, prompt-injection-containment, runtime-dispatch, approval-service, user-satisfaction, or support-state-promotion claim",
)

READER_SURFACE_FRAGMENTS = (
    "Intent re-contract trigger probe",
    "One valid case keeps work under the accepted contract when nothing material changes",
    "another routes a changed publication surface back through re-contracting before dispatch",
    "authority widening",
    "private-source publication pressure",
    "stop-condition erasure",
    "weaker evidence bars",
    "affected-party changes",
    "means expansion",
    "support-state promotion",
    "not a claim that the system understands intent",
    "extracts hidden authority",
    "contains prompt injection",
    "runs an approval service",
    "satisfies users",
    "can promote support states",
)

REQUIRED_NON_CLAIM_TERMS = (
    "does not promote any chapter core claim",
    "does not create a support-state transition",
    "natural-language intent understanding",
    "deployed parser quality",
    "deployed authority extraction",
    "prompt-injection containment",
    "runtime dispatch",
    "approval-service behavior",
    "user satisfaction",
    "does not read private source text",
)

EXPECTED_VALID_ROUTES = {
    "valid_no_material_delta_continue": "continue_under_existing_contract",
    "valid_publication_surface_delta_recontracts": "require_recontract",
}

EXPECTED_INVALID_ROUTES = {
    "invalid_authority_delta_without_recontract": "block_delta_until_recontract",
    "invalid_private_source_delta_without_recontract": "block_delta_until_recontract",
    "invalid_stop_condition_erasure_without_recontract": "block_delta_until_recontract",
    "invalid_evidence_bar_weakening_without_recontract": "block_delta_until_recontract",
    "invalid_affected_party_widening_without_recontract": "block_delta_until_recontract",
    "invalid_means_expansion_without_recontract": "block_delta_until_recontract",
    "invalid_support_state_promotion_without_recontract": "block_delta_until_recontract",
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
    print("Intent re-contract trigger probe validation failed:", file=sys.stderr)
    for error in errors:
        print(f" - {error}", file=sys.stderr)
    raise SystemExit(1)


def require_sha(value: Any, owner: str, errors: list[str]) -> None:
    if not re.fullmatch(r"[0-9a-f]{64}", str(value)):
        errors.append(f"{owner} must be a SHA-256 hex digest.")


def require_no_effects(scenario: dict[str, Any], owner: str, errors: list[str]) -> None:
    outcome = scenario.get("outcome", {})
    for key in ("private_source_read", "network_used", "job_dispatched", "publication_performed"):
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
        "record_kind": "intent_recontract_probe",
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
    trigger_fields = result.get("trigger_fields", [])
    for field in (
        "allowed_means",
        "authority_ceiling",
        "affected_parties",
        "evidence_bar",
        "publication_surface",
        "source_boundary",
        "stop_conditions",
        "support_state_effect",
    ):
        if field not in trigger_fields:
            errors.append(f"{rel(RESULT)}: trigger_fields missing {field}.")

    valid = result.get("valid_scenarios", [])
    invalid = result.get("expected_invalid_controls", [])
    if not isinstance(valid, list) or len(valid) != 2:
        errors.append(f"{rel(RESULT)}: expected two valid scenarios.")
        valid = []
    if not isinstance(invalid, list) or len(invalid) != 7:
        errors.append(f"{rel(RESULT)}: expected seven invalid controls.")
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
        if scenario_id == "valid_publication_surface_delta_recontracts":
            if scenario.get("outcome", {}).get("recontract_required") is not True:
                errors.append(f"{owner}: recontract_required must be true.")

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
        outcome = scenario.get("outcome", {})
        if outcome.get("blocked_before_dispatch") is not True:
            errors.append(f"{owner}: blocked_before_dispatch must be true.")
        if outcome.get("dispatch_allowed") is not False:
            errors.append(f"{owner}: dispatch_allowed must be false.")
        changed = scenario.get("input_summary", {}).get("changed_trigger_fields", [])
        if not changed:
            errors.append(f"{owner}: invalid control must record changed trigger fields.")

    summary = result.get("summary", {})
    if summary.get("valid_scenarios") != 2:
        errors.append(f"{rel(RESULT)}: summary.valid_scenarios must be 2.")
    if summary.get("expected_invalid_controls") != 7:
        errors.append(f"{rel(RESULT)}: summary.expected_invalid_controls must be 7.")
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
        (rel(README), README),
        (rel(PUBLICATION), PUBLICATION),
        (rel(STATUS), STATUS),
    ):
        require_fragments(owner, path.read_text(encoding="utf-8"), SURFACE_FRAGMENTS, errors)
    require_fragments(rel(READER_CHAPTER), READER_CHAPTER.read_text(encoding="utf-8"), READER_SURFACE_FRAGMENTS, errors)

    record = chapter_record(structure, "human-intent-as-a-formal-input")
    if record.get("evidence_level") != "argument":
        errors.append("human-intent-as-a-formal-input: evidence_level must remain argument.")
    require_fragments(
        "book_structure human-intent tests",
        text_blob(record.get("codex_tests", [])),
        (
            "Intent re-contract trigger probe",
            "valid_no_material_delta_continue",
            "valid_publication_surface_delta_recontracts",
            "seven expected-invalid controls",
            "no natural-language-intent-understanding, deployed-parser-quality, deployed-authority-extraction, prompt-injection-containment, runtime-dispatch, approval-service, user-satisfaction, or support-state-promotion claim",
        ),
        errors,
    )

    if errors:
        fail(errors)
    print(
        "Intent re-contract trigger probe validation passed: "
        "2 valid routes and 7 expected-invalid controls checked with no dispatch or support-state movement."
    )


if __name__ == "__main__":
    main()
