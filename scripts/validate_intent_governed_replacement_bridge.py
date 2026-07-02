#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "experiments" / "intent_governed_replacement_bridge" / "results" / "2026-07-02-local.json"
DOC = ROOT / "docs" / "intent_governed_replacement_bridge.md"
CHAPTER_INTENT = ROOT / "chapters" / "intent-to-execution-contracts.qmd"
CHAPTER_REPLACEMENT = ROOT / "chapters" / "capability-replacement-and-rollback.qmd"
READER_INTENT = ROOT / "editions" / "reader_manuscript" / "v1_0" / "chapters" / "intent-to-execution-contracts.qmd"
READER_REPLACEMENT = ROOT / "editions" / "reader_manuscript" / "v1_0" / "chapters" / "capability-replacement-and-rollback.qmd"
OUTLINE = ROOT / "docs" / "book_outline.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
CHANGELOG = ROOT / "appendices" / "F_changelog.qmd"
MANIFEST = ROOT / "book_structure.json"
VALIDATE_BOOK = ROOT / "scripts" / "validate_book.py"
LEAN_FILE = ROOT / "lean" / "AsiStackProofs" / "Replacement.lean"

COMMAND = "python3 scripts/validate_intent_governed_replacement_bridge.py"
PROOF_TAG = "lean:replacement.intent_governed.bridge"
CODEX_TEST_NAME = "Intent-governed replacement bridge"
REQUIRED_THEOREMS = [
    "intent_governed_replacement_bridge_fixture_valid",
    "intent_governed_replacement_bridge_rejects_authority_widening",
    "intent_governed_replacement_bridge_preserves_no_promotion_boundary",
]
REQUIRED_NON_CLAIMS = [
    "does not parse natural-language intent",
    "does not execute deployed replacement behavior",
    "does not prove approval-service enforcement",
    "does not prove regression-suite quality or monitor quality",
    "does not execute production rollback",
    "does not promote any chapter core claim",
    "does not create a support-state transition",
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Intent-governed replacement bridge validation failed:")
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


def trace(
    trace_id: str,
    *,
    expect_valid: bool,
    decision: str,
    intent_ref_present: bool = True,
    command_ref_present: bool = True,
    authority_within_intent: bool = True,
    stop_conditions_preserved: bool = True,
    forbidden_means_preserved: bool = True,
    evidence_requirements_preserved: bool = True,
    default_promotion_requested: bool = False,
    approval_receipt_present: bool = False,
    replacement_precheck_present: bool = True,
    canary_scope_declared: bool = True,
    monitor_window_declared: bool = True,
    rollback_owner_present: bool = True,
    rollback_dry_run_present: bool = True,
    residuals_preserved: bool = True,
    support_state_effect: str = "none",
) -> dict[str, Any]:
    authority_ceiling = "bounded_router_policy_canary_only"
    return {
        "trace_id": trace_id,
        "expect_valid": expect_valid,
        "intent_contract_ref": "intent://replace-router-policy-public" if intent_ref_present else "",
        "command_contract_ref": "command://replace-router-policy-public" if command_ref_present else "",
        "replacement_transaction_ref": f"replacement://{trace_id}",
        "intent_authority_ceiling": authority_ceiling,
        "replacement_authority_ceiling": (
            authority_ceiling if authority_within_intent else "external_tool_publication_and_default_rollout"
        ),
        "authority_within_intent": authority_within_intent,
        "stop_conditions_preserved": stop_conditions_preserved,
        "forbidden_means_preserved": forbidden_means_preserved,
        "evidence_requirements_preserved": evidence_requirements_preserved,
        "default_promotion_requested": default_promotion_requested,
        "approval_required_for_default": True,
        "approval_receipt_present": approval_receipt_present,
        "replacement_precheck_present": replacement_precheck_present,
        "canary_scope_declared": canary_scope_declared,
        "monitor_window_declared": monitor_window_declared,
        "rollback_owner_present": rollback_owner_present,
        "rollback_dry_run_present": rollback_dry_run_present,
        "residuals": [
            "synthetic bridge only; no deployed parser, dispatcher, replacement runner, monitor, or rollback service exists",
            "chapter core support states remain unchanged",
        ],
        "residuals_preserved": residuals_preserved,
        "decision": decision,
        "support_state_effect": support_state_effect,
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
        "non_claims": REQUIRED_NON_CLAIMS,
    }


TRACES: list[dict[str, Any]] = [
    trace(
        "valid_command_to_canary_replacement",
        expect_valid=True,
        decision="canary_only",
        default_promotion_requested=False,
        approval_receipt_present=False,
    ),
    trace(
        "valid_default_request_blocked_without_approval",
        expect_valid=True,
        decision="default_blocked",
        default_promotion_requested=True,
        approval_receipt_present=False,
    ),
    trace("invalid_missing_intent_reference", expect_valid=False, decision="canary_only", intent_ref_present=False),
    trace("invalid_authority_widening_from_intent", expect_valid=False, decision="canary_only", authority_within_intent=False),
    trace("invalid_stop_condition_erasure", expect_valid=False, decision="canary_only", stop_conditions_preserved=False),
    trace(
        "invalid_default_without_approval_but_promoted",
        expect_valid=False,
        decision="default_promoted",
        default_promotion_requested=True,
        approval_receipt_present=False,
    ),
    trace("invalid_missing_rollback_owner", expect_valid=False, decision="canary_only", rollback_owner_present=False),
    trace(
        "invalid_support_promotion_overclaim",
        expect_valid=False,
        decision="canary_only",
        support_state_effect="synthetic-test-backed",
    ),
]


def nonempty_ref(record: dict[str, Any], field: str, prefix: str, errors: list[str]) -> None:
    trace_id = str(record.get("trace_id", "<missing>"))
    value = record.get(field)
    if not isinstance(value, str) or not value.startswith(prefix):
        errors.append(f"{trace_id}: {field} must be a non-empty {prefix} ref.")


def trace_errors(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    trace_id = str(record.get("trace_id", "<missing>"))
    nonempty_ref(record, "intent_contract_ref", "intent://", errors)
    nonempty_ref(record, "command_contract_ref", "command://", errors)
    nonempty_ref(record, "replacement_transaction_ref", "replacement://", errors)

    if record.get("support_state_effect") != "none":
        errors.append(f"{trace_id}: support_state_effect must remain none.")
    if record.get("chapter_core_support_effect") != "none":
        errors.append(f"{trace_id}: chapter_core_support_effect must remain none.")
    if record.get("evidence_transition_created") is not False:
        errors.append(f"{trace_id}: evidence_transition_created must remain false.")
    if record.get("authority_within_intent") is not True:
        errors.append(f"{trace_id}: replacement authority must stay within the intent authority ceiling.")
    if record.get("intent_authority_ceiling") != record.get("replacement_authority_ceiling"):
        errors.append(f"{trace_id}: replacement_authority_ceiling must match intent_authority_ceiling.")
    if record.get("stop_conditions_preserved") is not True:
        errors.append(f"{trace_id}: stop conditions must be preserved into the replacement transaction.")
    if record.get("forbidden_means_preserved") is not True:
        errors.append(f"{trace_id}: forbidden means must be preserved into the replacement transaction.")
    if record.get("evidence_requirements_preserved") is not True:
        errors.append(f"{trace_id}: evidence requirements must be preserved into the replacement transaction.")

    for field in (
        "replacement_precheck_present",
        "canary_scope_declared",
        "monitor_window_declared",
        "rollback_owner_present",
        "rollback_dry_run_present",
        "residuals_preserved",
    ):
        if record.get(field) is not True:
            errors.append(f"{trace_id}: {field} must be true.")

    decision = str(record.get("decision", ""))
    if decision not in {"canary_only", "default_blocked"}:
        errors.append(f"{trace_id}: decision must be canary_only or default_blocked.")
    if record.get("default_promotion_requested") is True:
        if record.get("approval_required_for_default") is not True:
            errors.append(f"{trace_id}: default replacement requests must require approval.")
        if record.get("approval_receipt_present") is not True and decision != "default_blocked":
            errors.append(f"{trace_id}: default request without approval must be blocked.")

    residuals = record.get("residuals")
    if not isinstance(residuals, list) or not residuals:
        errors.append(f"{trace_id}: residuals must be recorded.")
    non_claim_text = text_blob(record.get("non_claims", []))
    for phrase in REQUIRED_NON_CLAIMS:
        if phrase.lower() not in non_claim_text:
            errors.append(f"{trace_id}: non_claims missing {phrase!r}.")
    return errors


def build_expected_result() -> dict[str, Any]:
    valid_count = sum(1 for record in TRACES if record["expect_valid"])
    invalid_count = len(TRACES) - valid_count
    return {
        "schema_version": "asi_stack.intent_governed_replacement_bridge.v0",
        "result_id": "2026-07-02-intent-governed-replacement-bridge",
        "recorded_date": "2026-07-02",
        "command": COMMAND,
        "result_kind": "deterministic_synthetic_intent_governed_replacement_bridge",
        "valid_trace_count": valid_count,
        "expected_invalid_control_count": invalid_count,
        "trace_count": len(TRACES),
        "traces": TRACES,
        "bridge_assertions": {
            "intent_ref_required": True,
            "command_ref_required": True,
            "authority_widening_rejected": True,
            "stop_condition_erasure_rejected": True,
            "default_without_approval_blocked": True,
            "rollback_owner_required": True,
            "support_promotion_overclaim_rejected": True,
            "support_state_effect_none": True,
            "chapter_core_support_effect_none": True,
            "evidence_transition_created": False,
            "non_claim_boundary": True,
        },
        "lean_fixture_alignment": {
            "module": "AsiStackProofs.Replacement",
            "proof_tag": PROOF_TAG,
            "theorem_refs": REQUIRED_THEOREMS,
            "expected": {
                "valid_trace_count": valid_count,
                "expected_invalid_control_count": invalid_count,
                "authority_widening_rejected": True,
                "stop_condition_erasure_rejected": True,
                "default_without_approval_blocked": True,
                "rollback_owner_required": True,
                "support_state_effect_none": True,
                "non_claim_boundary": True,
            },
        },
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
        "verification_result": "pass",
        "non_claims": REQUIRED_NON_CLAIMS,
    }


def validate_traces(errors: list[str]) -> None:
    for record in TRACES:
        observed = trace_errors(record)
        if record["expect_valid"] and observed:
            errors.extend(observed)
        if not record["expect_valid"] and not observed:
            errors.append(f"{record['trace_id']}: expected-invalid control passed validation.")


def validate_result(expected: dict[str, Any], write_result: bool, errors: list[str]) -> None:
    serialized = json.dumps(expected, indent=2, sort_keys=True) + "\n"
    if write_result:
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(serialized, encoding="utf-8")
        return
    if not RESULT.exists():
        errors.append(f"Missing {rel(RESULT)}; run {COMMAND} --write-result.")
        return
    if RESULT.read_text(encoding="utf-8") != serialized:
        errors.append(f"{rel(RESULT)} is stale; run {COMMAND} --write-result.")
    value = load_json(RESULT)
    if value.get("verification_result") != "pass":
        errors.append(f"{rel(RESULT)}: verification_result must be pass.")
    if value.get("support_state_effect") != "none":
        errors.append(f"{rel(RESULT)}: support_state_effect must remain none.")
    if value.get("chapter_core_support_effect") != "none":
        errors.append(f"{rel(RESULT)}: chapter_core_support_effect must remain none.")
    if value.get("evidence_transition_created") is not False:
        errors.append(f"{rel(RESULT)}: evidence_transition_created must remain false.")


def validate_manifest(errors: list[str]) -> None:
    value = load_json(MANIFEST)
    replacement_chapter = None
    intent_chapter = None
    for part in value.get("parts", []):
        for chapter in part.get("chapters", []):
            if chapter.get("id") == "capability-replacement-and-rollback":
                replacement_chapter = chapter
            if chapter.get("id") == "intent-to-execution-contracts":
                intent_chapter = chapter
    if replacement_chapter is None:
        errors.append("book_structure.json: missing capability replacement chapter.")
    else:
        if CODEX_TEST_NAME.lower() not in text_blob(replacement_chapter.get("codex_tests", [])):
            errors.append(f"book_structure.json: replacement codex_tests missing {CODEX_TEST_NAME!r}.")
        proof_tags = {
            target.get("tag")
            for target in replacement_chapter.get("proof_targets", [])
            if isinstance(target, dict)
        }
        if PROOF_TAG not in proof_tags:
            errors.append(f"book_structure.json: replacement proof_targets missing {PROOF_TAG!r}.")
    if intent_chapter is None:
        errors.append("book_structure.json: missing intent-to-execution chapter.")
    elif CODEX_TEST_NAME.lower() not in text_blob(intent_chapter.get("codex_tests", [])):
        errors.append(f"book_structure.json: intent codex_tests missing {CODEX_TEST_NAME!r}.")


def validate_lean(errors: list[str]) -> None:
    text = LEAN_FILE.read_text(encoding="utf-8", errors="ignore")
    for theorem in REQUIRED_THEOREMS:
        if not re.search(rf"\btheorem\s+{re.escape(theorem)}\b", text):
            errors.append(f"{rel(LEAN_FILE)} missing theorem {theorem}.")
    for field in (
        "validTraceCount",
        "expectedInvalidControlCount",
        "authorityWideningRejected",
        "stopConditionErasureRejected",
        "defaultWithoutApprovalBlocked",
        "rollbackOwnerRequired",
        "supportStateEffectNone",
        "nonClaimBoundary",
    ):
        if field not in text:
            errors.append(f"{rel(LEAN_FILE)} missing bridge field {field}.")


def validate_surfaces(errors: list[str]) -> None:
    required = {
        DOC: [
            "Intent-Governed Replacement Bridge",
            rel(RESULT),
            "two valid synthetic bridge traces",
            "six expected-invalid controls",
            "no support-state transition",
        ],
        CHAPTER_INTENT: [
            "Intent-governed replacement bridge",
            rel(RESULT),
            "does not parse natural-language intent",
        ],
        CHAPTER_REPLACEMENT: [
            "Intent-governed replacement bridge",
            rel(RESULT),
            "no deployed replacement execution",
        ],
        READER_INTENT: [
            "intent-governed replacement bridge",
            "not a parser result",
            "not a support-state transition",
        ],
        READER_REPLACEMENT: [
            "intent-governed replacement bridge",
            "not a deployed replacement",
            "not a support-state transition",
        ],
        OUTLINE: [CODEX_TEST_NAME, PROOF_TAG, rel(RESULT)],
        ROADMAP: [
            "Intent-governed replacement bridge",
            "command authority into replacement admission",
            "no support-state promotion",
        ],
        CHANGELOG: ["Intent-governed replacement bridge", rel(RESULT)],
        VALIDATE_BOOK: [
            "scripts/validate_intent_governed_replacement_bridge.py",
            "docs/intent_governed_replacement_bridge.md",
            "experiments/intent_governed_replacement_bridge/results/2026-07-02-local.json",
            'run_validator("validate_intent_governed_replacement_bridge.py")',
        ],
    }
    for path, phrases in required.items():
        if not path.exists():
            errors.append(f"Missing required intent-governed replacement bridge surface {rel(path)}.")
            continue
        lowered = re.sub(r"\s+", " ", path.read_text(encoding="utf-8", errors="ignore")).lower()
        for phrase in phrases:
            normalized = re.sub(r"\s+", " ", phrase).lower()
            if normalized not in lowered:
                errors.append(f"{rel(path)} missing required phrase {phrase!r}.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-result", action="store_true")
    args = parser.parse_args()

    errors: list[str] = []
    expected = build_expected_result()
    validate_traces(errors)
    assertions = expected["bridge_assertions"]
    for key in (
        "intent_ref_required",
        "command_ref_required",
        "authority_widening_rejected",
        "stop_condition_erasure_rejected",
        "default_without_approval_blocked",
        "rollback_owner_required",
        "support_promotion_overclaim_rejected",
        "support_state_effect_none",
        "non_claim_boundary",
    ):
        if assertions.get(key) is not True:
            errors.append(f"bridge_assertions.{key} must be true.")
    validate_result(expected, args.write_result, errors)
    validate_manifest(errors)
    validate_lean(errors)
    validate_surfaces(errors)
    if errors:
        fail(errors)
    print("Intent-governed replacement bridge validation passed.")


if __name__ == "__main__":
    main()
