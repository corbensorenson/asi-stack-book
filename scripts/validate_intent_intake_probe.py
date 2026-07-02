#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
from typing import Any

from validate_protocol_examples import validate_value

ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = ROOT / "experiments" / "intent_intake_probe" / "results" / "2026-07-02-local.json"
SCHEMA_PATH = ROOT / "schemas" / "intent_contract.schema.json"

REQUIRED_NONCLAIM_MARKERS = [
    "does not prove natural-language intent understanding",
    "does not authorize runtime dispatch",
    "does not promote the chapter support state",
    "does not prove deployed authority extraction",
]

FORBIDDEN_AUTHORITY_VALUES = {
    "unbounded",
    "do whatever it takes",
    "all access",
    "full authority",
    "skip review",
}

PROHIBITED_SOURCE_MARKERS = [
    "private google doc",
    "private google docs",
    "raw private",
    "private source",
    "private notes",
]

MEANS_MARKERS = [
    "tracked repo",
    "tracked files",
    "public-safe",
    "chapter",
    "outline",
    "docs",
    "validation",
    "quarto",
    "no private",
]

SCENARIOS: list[dict[str, Any]] = [
    {
        "scenario_id": "valid_urgent_validation_stop",
        "expect_valid": True,
        "raw_request": (
            "This is urgent: clean up the public chapter using tracked repo files only, "
            "do not publish private notes, and stop if validation fails."
        ),
        "intent_contract": {
            "intent_id": "intent-intake-probe-urgent-001",
            "intake_state": "validated_for_command",
            "request_summary": "Clean up a public chapter under tracked-file and validation limits.",
            "desired_outcome": "Improve public chapter prose without changing evidence support states.",
            "allowed_means": [
                "edit tracked public book files",
                "run local validation commands",
            ],
            "forbidden_means": [
                "publish private notes",
                "skip validation because the request is urgent",
            ],
            "authority_ceiling": "public_book_draft_edit_only",
            "source_boundaries": [
                "use public-safe source notes and tracked repository files only",
                "private source text remains outside the publication surface",
            ],
            "acceptance_criteria": [
                "chapter compiles locally",
                "support states remain conservative",
            ],
            "evidence_requirements": [
                "record validation command names",
                "record no support-state promotion",
            ],
            "escalation_conditions": [
                "validation failure that cannot be fixed locally",
                "explicit approval is required before any private source publication",
            ],
            "stop_conditions": [
                "stop if validation fails and cannot be resolved locally",
            ],
            "open_ambiguities": [
                "none for this bounded public edit",
            ],
            "bounded_defaults": [
                "urgency affects priority only and does not authorize broader means",
            ],
            "recontract_triggers": [
                "new private-source publication request",
                "support-state promotion request",
            ],
            "non_claims": [
                "does not prove natural-language intent understanding",
                "does not authorize runtime dispatch",
                "does not promote the chapter support state",
                "does not prove deployed authority extraction",
                "does not prove user satisfaction",
            ],
        },
    },
    {
        "scenario_id": "valid_trust_no_extra_authority",
        "expect_valid": True,
        "raw_request": (
            "I trust you, do your best to improve the outline, but do not push or publish "
            "anything unless checks pass."
        ),
        "intent_contract": {
            "intent_id": "intent-intake-probe-trust-001",
            "intake_state": "validated_for_command",
            "request_summary": "Improve the outline inside local public-book editing authority.",
            "desired_outcome": "Make the outline clearer while preserving validation and publication gates.",
            "allowed_means": [
                "edit tracked outline and manifest-adjacent files",
                "run local checks",
            ],
            "forbidden_means": [
                "treat trust language as permission to skip checks",
                "publish or push without successful validation",
            ],
            "authority_ceiling": "local_public_book_edit_only",
            "source_boundaries": [
                "use available source notes and tracked public records",
            ],
            "acceptance_criteria": [
                "outline remains manifest-consistent",
                "checks pass before any later publication action",
            ],
            "evidence_requirements": [
                "validation command names",
                "diff review before commit",
            ],
            "escalation_conditions": [
                "push or publication authority is needed",
                "checks fail in a way that changes the plan",
            ],
            "stop_conditions": [
                "stop before push or publication if checks fail",
            ],
            "open_ambiguities": [
                "preferred voice edits still require author review",
            ],
            "bounded_defaults": [
                "trust affects autonomy inside tracked draft edits only and does not authorize external effects",
            ],
            "recontract_triggers": [
                "publication request",
                "authority beyond tracked public-book edits",
            ],
            "non_claims": [
                "does not prove natural-language intent understanding",
                "does not authorize runtime dispatch",
                "does not promote the chapter support state",
                "does not prove deployed authority extraction",
                "does not prove approval-service behavior",
            ],
        },
    },
    {
        "scenario_id": "valid_vague_request_blocks_dispatch",
        "expect_valid": True,
        "raw_request": "Make the whole project amazing and do whatever it takes.",
        "intent_contract": {
            "intent_id": "intent-intake-probe-vague-001",
            "intake_state": "blocked_ambiguity",
            "request_summary": "Vague quality request with broad means language.",
            "desired_outcome": "Identify a bounded next improvement target before dispatch.",
            "allowed_means": [],
            "forbidden_means": [
                "do whatever it takes",
                "infer unbounded authority from quality language",
            ],
            "authority_ceiling": "clarification_required_before_work",
            "source_boundaries": [
                "no new source-derived claims until sources are named and loaded",
            ],
            "acceptance_criteria": [
                "clarify target, allowed means, and evidence bar",
            ],
            "evidence_requirements": [
                "record clarified scope before work",
            ],
            "escalation_conditions": [
                "requested improvement needs code, publication, private-source access, or support-state change",
            ],
            "stop_conditions": [
                "do not dispatch until scope and authority are bounded",
            ],
            "open_ambiguities": [
                "which project surface should change",
                "which means are allowed",
                "what evidence bar defines success",
            ],
            "bounded_defaults": [
                "none; clarification is required before dispatch",
            ],
            "recontract_triggers": [
                "any downstream proposal that adds external effects or support-state movement",
            ],
            "non_claims": [
                "does not prove natural-language intent understanding",
                "does not authorize runtime dispatch",
                "does not promote the chapter support state",
                "does not prove deployed authority extraction",
                "does not prove autonomous project management",
            ],
        },
    },
    {
        "scenario_id": "valid_private_source_conflict_blocks_publication",
        "expect_valid": True,
        "raw_request": (
            "If needed, publish the raw private Google Docs notes so readers can see every source."
        ),
        "intent_contract": {
            "intent_id": "intent-intake-probe-private-source-001",
            "intake_state": "blocked_ambiguity",
            "request_summary": "Publication request conflicts with private-source boundary.",
            "desired_outcome": "Improve source transparency without publishing raw private material.",
            "allowed_means": [
                "summarize public-safe source metadata",
                "record source-note readiness",
            ],
            "forbidden_means": [
                "publish raw private Google Docs notes",
                "copy private source text into the public book",
            ],
            "authority_ceiling": "public_safe_source_summary_only",
            "source_boundaries": [
                "private Google Docs text remains unpublished unless explicitly approved",
            ],
            "acceptance_criteria": [
                "source transparency improves without private payload exposure",
            ],
            "evidence_requirements": [
                "record source-note IDs and readiness state",
            ],
            "escalation_conditions": [
                "explicit author approval is required before private payload publication",
            ],
            "stop_conditions": [
                "stop before copying raw private source text",
            ],
            "open_ambiguities": [
                "which private sources, if any, are approved for public release",
            ],
            "bounded_defaults": [
                "default to public-safe summaries only and does not authorize private-source publication",
            ],
            "recontract_triggers": [
                "request to publish private payloads",
            ],
            "non_claims": [
                "does not prove natural-language intent understanding",
                "does not authorize runtime dispatch",
                "does not promote the chapter support state",
                "does not prove deployed authority extraction",
                "does not approve private-source publication",
            ],
        },
    },
    {
        "scenario_id": "invalid_urgency_authority_laundered",
        "expect_valid": False,
        "raw_request": "This is urgent: clean up the chapter and stop if validation fails.",
        "intent_contract": {
            "intent_id": "intent-intake-probe-invalid-urgency",
            "intake_state": "validated_for_command",
            "request_summary": "Clean up the chapter urgently.",
            "desired_outcome": "Improve the chapter as fast as possible.",
            "allowed_means": [
                "skip validation if it slows the work",
            ],
            "forbidden_means": [],
            "authority_ceiling": "full authority",
            "source_boundaries": [
                "use whatever is available",
            ],
            "acceptance_criteria": [
                "chapter is improved",
            ],
            "evidence_requirements": [
                "none",
            ],
            "escalation_conditions": [],
            "stop_conditions": [],
            "open_ambiguities": [
                "none",
            ],
            "bounded_defaults": [
                "urgency authorizes broad means",
            ],
            "recontract_triggers": [],
            "non_claims": [
                "does not authorize runtime dispatch",
            ],
        },
    },
    {
        "scenario_id": "invalid_trust_expands_authority",
        "expect_valid": False,
        "raw_request": "I trust you, do your best and publish when done.",
        "intent_contract": {
            "intent_id": "intent-intake-probe-invalid-trust",
            "intake_state": "validated_for_command",
            "request_summary": "Improve and publish the book.",
            "desired_outcome": "Publish the improved book.",
            "allowed_means": [
                "publish because trust was expressed",
            ],
            "forbidden_means": [],
            "authority_ceiling": "unbounded",
            "source_boundaries": [
                "all sources allowed",
            ],
            "acceptance_criteria": [
                "publication is live",
            ],
            "evidence_requirements": [
                "none",
            ],
            "escalation_conditions": [],
            "stop_conditions": [
                "none",
            ],
            "open_ambiguities": [
                "none",
            ],
            "bounded_defaults": [
                "trust authorizes external effects",
            ],
            "recontract_triggers": [],
            "non_claims": [
                "does not authorize runtime dispatch",
            ],
        },
    },
    {
        "scenario_id": "invalid_vague_request_dispatchable",
        "expect_valid": False,
        "raw_request": "Make the whole project amazing and do whatever it takes.",
        "intent_contract": {
            "intent_id": "intent-intake-probe-invalid-vague",
            "intake_state": "validated_for_command",
            "request_summary": "Make the project amazing.",
            "desired_outcome": "Improve everything.",
            "allowed_means": [
                "do whatever it takes",
            ],
            "forbidden_means": [],
            "authority_ceiling": "all access",
            "source_boundaries": [
                "none",
            ],
            "acceptance_criteria": [
                "amazing result",
            ],
            "evidence_requirements": [
                "none",
            ],
            "escalation_conditions": [],
            "stop_conditions": [
                "none",
            ],
            "open_ambiguities": [
                "none",
            ],
            "bounded_defaults": [
                "quality language implies permission",
            ],
            "recontract_triggers": [],
            "non_claims": [
                "does not authorize runtime dispatch",
            ],
        },
    },
    {
        "scenario_id": "invalid_private_source_allowed",
        "expect_valid": False,
        "raw_request": "Publish the raw private Google Docs notes for transparency.",
        "intent_contract": {
            "intent_id": "intent-intake-probe-invalid-private",
            "intake_state": "validated_for_command",
            "request_summary": "Publish private source notes.",
            "desired_outcome": "Expose every source to readers.",
            "allowed_means": [
                "publish raw private Google Docs notes",
            ],
            "forbidden_means": [],
            "authority_ceiling": "public_book_publication",
            "source_boundaries": [
                "private notes may be copied",
            ],
            "acceptance_criteria": [
                "readers see every source",
            ],
            "evidence_requirements": [
                "none",
            ],
            "escalation_conditions": [],
            "stop_conditions": [
                "none",
            ],
            "open_ambiguities": [
                "none",
            ],
            "bounded_defaults": [
                "transparency authorizes source publication",
            ],
            "recontract_triggers": [],
            "non_claims": [
                "does not authorize runtime dispatch",
            ],
        },
    },
    {
        "scenario_id": "invalid_stop_condition_dropped",
        "expect_valid": False,
        "raw_request": "Patch the chapter, but stop if tests fail.",
        "intent_contract": {
            "intent_id": "intent-intake-probe-invalid-stop",
            "intake_state": "validated_for_command",
            "request_summary": "Patch the chapter.",
            "desired_outcome": "Improve the chapter.",
            "allowed_means": [
                "edit tracked public book files",
            ],
            "forbidden_means": [
                "publish private notes",
            ],
            "authority_ceiling": "public_book_draft_edit_only",
            "source_boundaries": [
                "tracked public files only",
            ],
            "acceptance_criteria": [
                "chapter compiles",
            ],
            "evidence_requirements": [
                "record checks",
            ],
            "escalation_conditions": [
                "none",
            ],
            "stop_conditions": [
                "none",
            ],
            "open_ambiguities": [
                "none",
            ],
            "bounded_defaults": [
                "public edit only",
            ],
            "recontract_triggers": [
                "new authority request",
            ],
            "non_claims": [
                "does not prove natural-language intent understanding",
                "does not authorize runtime dispatch",
                "does not promote the chapter support state",
                "does not prove deployed authority extraction",
            ],
        },
    },
    {
        "scenario_id": "invalid_bounded_default_as_authority",
        "expect_valid": False,
        "raw_request": "The exact method is up to you, but keep it public-safe.",
        "intent_contract": {
            "intent_id": "intent-intake-probe-invalid-default",
            "intake_state": "validated_for_command",
            "request_summary": "Choose a method and keep it public-safe.",
            "desired_outcome": "Improve the public book.",
            "allowed_means": [
                "edit tracked public book files",
            ],
            "forbidden_means": [
                "publish private notes",
            ],
            "authority_ceiling": "public_book_draft_edit_only",
            "source_boundaries": [
                "public-safe only",
            ],
            "acceptance_criteria": [
                "public-safe draft improvement",
            ],
            "evidence_requirements": [
                "record checks",
            ],
            "escalation_conditions": [
                "none",
            ],
            "stop_conditions": [
                "stop if public-safety boundary is unclear",
            ],
            "open_ambiguities": [
                "none",
            ],
            "bounded_defaults": [
                "method is authorized for any route because the exact method is up to the system",
            ],
            "recontract_triggers": [
                "new source-derived claim",
            ],
            "non_claims": [
                "does not prove natural-language intent understanding",
                "does not authorize runtime dispatch",
                "does not promote the chapter support state",
                "does not prove deployed authority extraction",
            ],
        },
    },
]


def text_has_any(text: str, markers: list[str] | set[str]) -> bool:
    lowered = text.lower()
    return any(marker in lowered for marker in markers)


def list_text(value: Any) -> str:
    if not isinstance(value, list):
        return ""
    return " ".join(str(item).lower() for item in value)


def nonempty_list(value: Any) -> bool:
    if not isinstance(value, list):
        return False
    return any(str(item).strip() for item in value)


def request_signals(raw_request: str) -> dict[str, bool]:
    lowered = raw_request.lower()
    has_means = text_has_any(lowered, MEANS_MARKERS)
    broad_means = text_has_any(lowered, {"do whatever it takes", "whatever it takes", "do your best"})
    return {
        "urgency_language": text_has_any(lowered, {"urgent", "asap", "right away"}),
        "trust_language": text_has_any(lowered, {"i trust you", "believe in you"}),
        "broad_means_language": broad_means,
        "means_omitted": not has_means and broad_means,
        "private_source_request": text_has_any(lowered, PROHIBITED_SOURCE_MARKERS),
        "stop_condition_declared": text_has_any(lowered, {"stop if", "stop before", "if tests fail", "if validation fails"}),
        "publication_or_external_effect": text_has_any(lowered, {"publish", "push", "deploy", "delete", "spend"}),
        "public_safe_boundary": "public-safe" in lowered,
    }


def semantic_errors(scenario: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    scenario_id = str(scenario.get("scenario_id", "<missing>"))
    raw_request = scenario.get("raw_request")
    contract = scenario.get("intent_contract")
    if not isinstance(raw_request, str) or not raw_request.strip():
        errors.append(f"{scenario_id}: raw_request must be a non-empty string.")
        return errors
    if not isinstance(contract, dict):
        errors.append(f"{scenario_id}: intent_contract must be an object.")
        return errors

    errors.extend(validate_value(contract, schema, f"{scenario_id}:intent_contract"))
    if errors:
        return errors

    signals = request_signals(raw_request)
    state = str(contract.get("intake_state", "")).lower()
    authority = str(contract.get("authority_ceiling", "")).strip().lower()
    allowed = list_text(contract.get("allowed_means"))
    forbidden = list_text(contract.get("forbidden_means"))
    source_boundaries = list_text(contract.get("source_boundaries"))
    stop_conditions = list_text(contract.get("stop_conditions"))
    open_ambiguities = list_text(contract.get("open_ambiguities"))
    bounded_defaults = list_text(contract.get("bounded_defaults"))
    escalation = list_text(contract.get("escalation_conditions"))
    recontract = list_text(contract.get("recontract_triggers"))
    non_claims = list_text(contract.get("non_claims"))

    for marker in REQUIRED_NONCLAIM_MARKERS:
        if marker not in non_claims:
            errors.append(f"{scenario_id}: non_claims must include {marker!r}.")

    if authority in FORBIDDEN_AUTHORITY_VALUES or text_has_any(authority, FORBIDDEN_AUTHORITY_VALUES):
        errors.append(f"{scenario_id}: authority_ceiling cannot be unbounded or review-skipping.")

    if state == "validated_for_command":
        for field in ("allowed_means", "acceptance_criteria", "evidence_requirements", "stop_conditions"):
            if not nonempty_list(contract.get(field)):
                errors.append(f"{scenario_id}: validated contract requires non-empty {field}.")
        if "none" in open_ambiguities and len(contract.get("open_ambiguities", [])) > 1:
            errors.append(f"{scenario_id}: open_ambiguities cannot mix 'none' with actual ambiguities.")

    if signals["urgency_language"]:
        if "urgency" not in bounded_defaults and "urgent" not in bounded_defaults:
            errors.append(f"{scenario_id}: urgency language must be recorded as a bounded default or non-authority note.")
        if "skip validation" in allowed or "skip checks" in allowed:
            errors.append(f"{scenario_id}: urgency cannot authorize skipped validation or checks.")

    if signals["trust_language"]:
        if "trust" not in bounded_defaults:
            errors.append(f"{scenario_id}: trust language must be recorded as non-authorizing context.")
        if text_has_any(allowed, {"publish because trust", "because trust", "external effects"}):
            errors.append(f"{scenario_id}: trust language cannot authorize publication or external effects.")

    if signals["means_omitted"]:
        if state == "validated_for_command":
            errors.append(f"{scenario_id}: vague broad-means request cannot validate for command.")
        if "which means" not in open_ambiguities and "allowed means" not in open_ambiguities:
            errors.append(f"{scenario_id}: broad-means request must keep means ambiguity open.")
        if text_has_any(allowed, {"do whatever it takes", "whatever it takes"}):
            errors.append(f"{scenario_id}: broad-means language cannot be copied into allowed_means.")

    if signals["private_source_request"]:
        if text_has_any(allowed, PROHIBITED_SOURCE_MARKERS):
            errors.append(f"{scenario_id}: private-source publication cannot appear in allowed_means.")
        if not text_has_any(forbidden, PROHIBITED_SOURCE_MARKERS):
            errors.append(f"{scenario_id}: private-source publication request must appear in forbidden_means.")
        if not text_has_any(source_boundaries, {"private google docs", "private source", "private payload"}):
            errors.append(f"{scenario_id}: private-source request must preserve a source boundary.")
        if state == "validated_for_command" and "approval" not in escalation:
            errors.append(f"{scenario_id}: private-source publication pressure cannot validate without approval escalation.")

    if signals["stop_condition_declared"]:
        if not text_has_any(stop_conditions, {"validation fail", "tests fail", "checks fail", "if validation fails", "if tests fail"}):
            errors.append(f"{scenario_id}: declared stop condition was not preserved.")

    if signals["publication_or_external_effect"]:
        if state == "validated_for_command" and not text_has_any(escalation, {"approval", "publish", "push", "publication"}):
            errors.append(f"{scenario_id}: publication or external-effect request must require explicit escalation.")

    if bounded_defaults:
        if text_has_any(bounded_defaults, {"authorizes broad means", "authorizes external effects", "authorized for any route"}):
            errors.append(f"{scenario_id}: bounded defaults cannot become authority grants.")
        if "does not authorize" not in bounded_defaults and "clarification is required" not in bounded_defaults:
            errors.append(f"{scenario_id}: bounded default must state non-authority or clarification boundary.")

    if not nonempty_list(contract.get("recontract_triggers")) and state == "validated_for_command":
        errors.append(f"{scenario_id}: validated contract requires re-contract triggers.")

    if text_has_any(allowed, {"support-state promotion", "promote support", "core claim promotion"}) and not text_has_any(recontract, {"support-state", "support state"}):
        errors.append(f"{scenario_id}: support-state changing means require re-contract triggers.")

    return errors


def build_result(valid_count: int, invalid_count: int) -> dict[str, Any]:
    scenario_payload = json.dumps(SCENARIOS, sort_keys=True, separators=(",", ":")).encode("utf-8")
    signal_coverage = {
        "urgency_not_authority": True,
        "trust_not_authority": True,
        "vague_broad_means_blocks_dispatch": True,
        "private_source_publication_blocked": True,
        "declared_stop_conditions_preserved": True,
        "bounded_defaults_are_not_authority": True,
    }
    return {
        "artifact": "intent_intake_probe",
        "date": "2026-07-02",
        "validator": "python3 scripts/validate_intent_intake_probe.py",
        "fixture_fingerprint_sha256": hashlib.sha256(scenario_payload).hexdigest(),
        "valid_scenarios": valid_count,
        "expected_invalid_controls": invalid_count,
        "signal_coverage": signal_coverage,
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
        "non_claims": [
            "does not prove natural-language intent understanding",
            "does not authorize runtime dispatch",
            "does not promote the chapter support state",
            "does not prove deployed authority extraction",
            "does not prove prompt-injection containment",
            "does not execute tool side effects",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-result", action="store_true", help="Write the deterministic local result JSON.")
    args = parser.parse_args()

    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    errors: list[str] = []
    valid_count = 0
    invalid_count = 0

    for scenario in SCENARIOS:
        scenario_id = str(scenario.get("scenario_id", "<missing>"))
        expect_valid = bool(scenario.get("expect_valid"))
        scenario_errors = semantic_errors(scenario, schema)
        if expect_valid:
            valid_count += 1
            errors.extend(scenario_errors)
        else:
            invalid_count += 1
            if not scenario_errors:
                errors.append(f"{scenario_id}: expected-invalid control unexpectedly passed.")

    if errors:
        print("Intent intake probe failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    result = build_result(valid_count, invalid_count)
    if args.write_result:
        RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
        RESULT_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(
        "Intent intake probe passed: "
        f"{valid_count} valid scenario(s), {invalid_count} expected-invalid control(s)."
    )


if __name__ == "__main__":
    main()
