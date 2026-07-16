#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "experiments" / "verification_bandwidth" / "results" / "2026-07-02-local.json"
DOC = ROOT / "docs" / "verification_bandwidth_probe.md"
CHAPTER = ROOT / "chapters" / "verification-bandwidth-and-context-adequacy.qmd"
READER = (
    ROOT
    / "editions"
    / "reader_manuscript"
    / "v1_0"
    / "chapters"
    / "verification-bandwidth-and-context-adequacy.qmd"
)
OUTLINE = ROOT / "docs" / "book_outline.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
CHANGELOG = ROOT / "appendices" / "F_changelog.qmd"
MANIFEST = ROOT / "book_structure.json"
VALIDATION_REGISTRY = ROOT / "validation" / "registry.json"
LEAN_FILE = ROOT / "lean" / "AsiStackProofs" / "VerificationBandwidthRefinement.lean"

COMMAND = "python3 scripts/validate_verification_bandwidth_probe.py"
PROOF_TAG = "lean:verification_bandwidth.contradiction_probe_fixture_bridge"
CODEX_TEST_NAME = "Verification bandwidth contradiction probe"
REQUIRED_THEOREMS = [
    "contradiction_blocks_evidence_handoff",
]
REQUIRED_NON_CLAIMS = [
    "does not measure model verification bandwidth",
    "does not prove contradiction-rate performance",
    "does not prove distractor resistance",
    "does not validate an adequacy classifier",
    "does not execute a deployed claim ledger or escalation service",
    "does not promote the chapter support state",
]

VERIFIED_LABELS = {"verified", "promoted", "synthetic-test-backed"}
BLOCKED_LABELS = {"draft_only", "blocked", "escalated", "residual"}


TRACES: list[dict[str, Any]] = [
    {
        "trace_id": "valid_pairwise_contradiction_block",
        "expect_valid": True,
        "claim_id": "claim://cross-document-safety-comparison",
        "risk_tier": "high",
        "context_admitted": True,
        "semantic_units_identified": True,
        "decisive_unit_present": True,
        "dominant_distractor_present": True,
        "pairwise_check_complete": True,
        "contradiction_present": True,
        "contradiction_detected": True,
        "negative_evidence_open": True,
        "verification_mode": "pairwise_semantic_unit_check",
        "adequacy_state": "contradicted",
        "support_label": "escalated",
        "required_escalation": "tribunal_or_human_review",
        "residual_recorded": True,
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "valid_drafting_only_inadequate_context",
        "expect_valid": True,
        "claim_id": "claim://chapter-orientation-summary",
        "risk_tier": "low",
        "context_admitted": True,
        "semantic_units_identified": True,
        "decisive_unit_present": False,
        "dominant_distractor_present": False,
        "pairwise_check_complete": False,
        "contradiction_present": False,
        "contradiction_detected": False,
        "negative_evidence_open": False,
        "verification_mode": "summary_only_review",
        "adequacy_state": "drafting_only",
        "support_label": "draft_only",
        "required_escalation": "none",
        "residual_recorded": True,
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "invalid_summary_promoted_as_verified",
        "expect_valid": False,
        "claim_id": "claim://summary-derived-safety-claim",
        "risk_tier": "high",
        "context_admitted": True,
        "semantic_units_identified": True,
        "decisive_unit_present": False,
        "dominant_distractor_present": False,
        "pairwise_check_complete": False,
        "contradiction_present": False,
        "contradiction_detected": False,
        "negative_evidence_open": False,
        "verification_mode": "summary_only_review",
        "adequacy_state": "summary_derived",
        "support_label": "verified",
        "required_escalation": "none",
        "residual_recorded": False,
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "invalid_distractor_misses_decisive_contradiction",
        "expect_valid": False,
        "claim_id": "claim://dominant-distractor-comparison",
        "risk_tier": "high",
        "context_admitted": True,
        "semantic_units_identified": True,
        "decisive_unit_present": True,
        "dominant_distractor_present": True,
        "pairwise_check_complete": False,
        "contradiction_present": True,
        "contradiction_detected": False,
        "negative_evidence_open": True,
        "verification_mode": "long_context_draft",
        "adequacy_state": "joint_check",
        "support_label": "verified",
        "required_escalation": "none",
        "residual_recorded": False,
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "invalid_high_risk_no_escalation",
        "expect_valid": False,
        "claim_id": "claim://high-risk-inadequate-context",
        "risk_tier": "high",
        "context_admitted": True,
        "semantic_units_identified": True,
        "decisive_unit_present": False,
        "dominant_distractor_present": False,
        "pairwise_check_complete": False,
        "contradiction_present": False,
        "contradiction_detected": False,
        "negative_evidence_open": False,
        "verification_mode": "summary_only_review",
        "adequacy_state": "drafting_only",
        "support_label": "draft_only",
        "required_escalation": "none",
        "residual_recorded": True,
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "invalid_schema_mode_empirical_support",
        "expect_valid": False,
        "claim_id": "claim://empirical-runtime-claim",
        "risk_tier": "medium",
        "context_admitted": True,
        "semantic_units_identified": True,
        "decisive_unit_present": True,
        "dominant_distractor_present": False,
        "pairwise_check_complete": False,
        "contradiction_present": False,
        "contradiction_detected": False,
        "negative_evidence_open": False,
        "verification_mode": "schema_validation",
        "empirical_claim": True,
        "adequacy_state": "local_check",
        "support_label": "verified",
        "required_escalation": "none",
        "residual_recorded": False,
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "invalid_negative_evidence_ignored",
        "expect_valid": False,
        "claim_id": "claim://negative-evidence-open",
        "risk_tier": "medium",
        "context_admitted": True,
        "semantic_units_identified": True,
        "decisive_unit_present": True,
        "dominant_distractor_present": False,
        "pairwise_check_complete": True,
        "contradiction_present": False,
        "contradiction_detected": False,
        "negative_evidence_open": True,
        "verification_mode": "pairwise_semantic_unit_check",
        "adequacy_state": "joint_check",
        "support_label": "verified",
        "required_escalation": "none",
        "residual_recorded": False,
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "invalid_unidentified_units_verified",
        "expect_valid": False,
        "claim_id": "claim://unidentified-semantic-units",
        "risk_tier": "medium",
        "context_admitted": True,
        "semantic_units_identified": False,
        "decisive_unit_present": True,
        "dominant_distractor_present": False,
        "pairwise_check_complete": True,
        "contradiction_present": False,
        "contradiction_detected": False,
        "negative_evidence_open": False,
        "verification_mode": "pairwise_semantic_unit_check",
        "adequacy_state": "joint_check",
        "support_label": "verified",
        "required_escalation": "none",
        "residual_recorded": False,
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "invalid_support_state_promotion",
        "expect_valid": False,
        "claim_id": "claim://overpromoted-adequacy-fixture",
        "risk_tier": "low",
        "context_admitted": True,
        "semantic_units_identified": True,
        "decisive_unit_present": True,
        "dominant_distractor_present": False,
        "pairwise_check_complete": True,
        "contradiction_present": False,
        "contradiction_detected": False,
        "negative_evidence_open": False,
        "verification_mode": "pairwise_semantic_unit_check",
        "adequacy_state": "joint_check",
        "support_label": "verified",
        "required_escalation": "none",
        "residual_recorded": True,
        "support_state_effect": "promote_chapter_core",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Verification bandwidth probe validation failed:")
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


def trace_errors(trace: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    trace_id = str(trace.get("trace_id", "<missing>"))
    support_label = str(trace.get("support_label", ""))
    adequacy_state = str(trace.get("adequacy_state", ""))
    verification_mode = str(trace.get("verification_mode", ""))
    risk_tier = str(trace.get("risk_tier", ""))
    escalation = str(trace.get("required_escalation", ""))

    if not isinstance(trace.get("claim_id"), str) or not trace["claim_id"].startswith("claim://"):
        errors.append(f"{trace_id}: claim_id must use claim://.")
    if trace.get("support_state_effect") != "none":
        errors.append(f"{trace_id}: support_state_effect must be none.")
    if trace.get("context_admitted") is not True:
        errors.append(f"{trace_id}: context must be admitted before adequacy review.")
    if trace.get("semantic_units_identified") is not True and support_label in VERIFIED_LABELS:
        errors.append(f"{trace_id}: unidentified semantic units cannot support verified labels.")
    if trace.get("pairwise_check_complete") is not True and adequacy_state == "joint_check":
        errors.append(f"{trace_id}: joint_check adequacy requires complete pairwise check.")
    if trace.get("contradiction_present") is True:
        if trace.get("pairwise_check_complete") is True and trace.get("contradiction_detected") is not True:
            errors.append(f"{trace_id}: completed pairwise check must detect planted contradiction.")
        if support_label in VERIFIED_LABELS:
            errors.append(f"{trace_id}: contradiction-present trace cannot receive verified support.")
        if trace.get("residual_recorded") is not True:
            errors.append(f"{trace_id}: contradiction-present trace must record residual.")
    if trace.get("negative_evidence_open") is True:
        if support_label in VERIFIED_LABELS:
            errors.append(f"{trace_id}: open negative evidence blocks verified support.")
        if escalation == "none":
            errors.append(f"{trace_id}: open negative evidence requires escalation.")
    if risk_tier == "high" and adequacy_state not in {"joint_check", "contradicted", "escalated"}:
        if escalation == "none":
            errors.append(f"{trace_id}: high-risk inadequate context requires escalation.")
        if support_label in VERIFIED_LABELS:
            errors.append(f"{trace_id}: high-risk inadequate context blocks verified support.")
    if verification_mode == "summary_only_review" and support_label in VERIFIED_LABELS:
        errors.append(f"{trace_id}: summary-only review cannot support verified labels.")
    if verification_mode == "schema_validation" and trace.get("empirical_claim") is True and support_label in VERIFIED_LABELS:
        errors.append(f"{trace_id}: schema validation cannot verify empirical runtime claims.")
    if trace.get("dominant_distractor_present") is True and trace.get("pairwise_check_complete") is not True:
        if support_label in VERIFIED_LABELS:
            errors.append(f"{trace_id}: dominant distractor without pairwise check blocks verified support.")

    non_claim_text = text_blob(trace.get("non_claims", []))
    for phrase in REQUIRED_NON_CLAIMS:
        if phrase.lower() not in non_claim_text:
            errors.append(f"{trace_id}: non_claims missing {phrase!r}.")

    return errors


def build_expected_result(valid_count: int, invalid_count: int) -> dict[str, Any]:
    return {
        "schema_version": "asi_stack.verification_bandwidth_probe.v0",
        "result_id": "2026-07-02-verification-bandwidth-probe",
        "recorded_date": "2026-07-02",
        "command": COMMAND,
        "result_kind": "deterministic_synthetic_verification_bandwidth_probe",
        "valid_trace_count": valid_count,
        "expected_invalid_control_count": invalid_count,
        "trace_count": len(TRACES),
        "negative_controls": {
            "summary_promotion_rejected": True,
            "distractor_missed_contradiction_rejected": True,
            "high_risk_no_escalation_rejected": True,
            "schema_mode_empirical_support_rejected": True,
            "negative_evidence_ignored_rejected": True,
            "unidentified_units_verified_rejected": True,
            "support_state_promotion_rejected": True,
        },
        "transition_coverage": {
            "pairwise_contradiction_block": True,
            "drafting_only_inadequacy": True,
            "summary_ceiling_preserved": True,
            "distractor_pairwise_requirement": True,
            "mode_confusion_rejection": True,
            "support_state_no_promotion": True,
        },
        "lean_fixture_alignment": {
            "module": "AsiStackProofs.VerificationBandwidthRefinement",
            "proof_tag": PROOF_TAG,
            "theorem_refs": REQUIRED_THEOREMS,
            "expected": {
                "valid_contradiction_trace_present": True,
                "drafting_only_trace_present": True,
                "negative_controls_rejected": True,
                "support_state_effect_none": True,
                "non_claim_boundary": True,
            },
        },
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
        "verification_result": "pass",
        "residuals": [
            "Synthetic contradiction/adequacy fixture only; no model, context window, deployed claim ledger, or escalation service was measured.",
            "The chapter core claim remains at argument support.",
        ],
        "non_claims": REQUIRED_NON_CLAIMS,
    }


def validate_result(expected: dict[str, Any], write_result: bool, errors: list[str]) -> None:
    serialized = json.dumps(expected, indent=2, sort_keys=True) + "\n"
    if write_result:
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(serialized, encoding="utf-8")
        return
    if not RESULT.exists():
        errors.append(f"Missing {rel(RESULT)}; run {COMMAND} --write-result.")
        return
    current = RESULT.read_text(encoding="utf-8")
    if current != serialized:
        errors.append(f"{rel(RESULT)} is stale; run {COMMAND} --write-result.")
    value = load_json(RESULT)
    if value.get("verification_result") != "pass":
        errors.append(f"{rel(RESULT)}: verification_result must be pass.")
    if value.get("support_state_effect") != "none":
        errors.append(f"{rel(RESULT)}: support_state_effect must remain none.")


def validate_manifest(errors: list[str]) -> None:
    value = load_json(MANIFEST)
    chapter = None
    for part in value.get("parts", []):
        for candidate in part.get("chapters", []):
            if candidate.get("id") == "verification-bandwidth-and-context-adequacy":
                chapter = candidate
                break
    if chapter is None:
        errors.append("book_structure.json: missing verification-bandwidth chapter.")
        return
    codex_blob = text_blob(chapter.get("codex_tests", []))
    if CODEX_TEST_NAME.lower() not in codex_blob:
        errors.append(f"book_structure.json: codex_tests missing {CODEX_TEST_NAME!r}.")
    proof_tags = {target.get("tag") for target in chapter.get("proof_targets", []) if isinstance(target, dict)}
    if PROOF_TAG not in proof_tags:
        errors.append(f"book_structure.json: proof_targets missing {PROOF_TAG!r}.")


def validate_lean(errors: list[str]) -> None:
    text = LEAN_FILE.read_text(encoding="utf-8", errors="ignore")
    for theorem in REQUIRED_THEOREMS:
        if not re.search(rf"\btheorem\s+{re.escape(theorem)}\b", text):
            errors.append(f"{rel(LEAN_FILE)} missing theorem {theorem}.")
    for field in (
        "contradicted",
        "negativeSearchAttempted",
        "independentEvaluator",
        "verificationArtifactsPresent",
        "requestedEffect",
    ):
        if field not in text:
            errors.append(f"{rel(LEAN_FILE)} missing fixture field {field}.")


def validate_surfaces(errors: list[str]) -> None:
    required = {
        DOC: [
            "Verification Bandwidth Probe",
            rel(RESULT),
            "two valid synthetic adequacy traces",
            "seven expected-invalid controls",
            "no support-state transition",
        ],
        CHAPTER: [
            "Verification bandwidth contradiction probe",
            rel(RESULT),
            "two valid synthetic adequacy traces",
            "seven expected-invalid controls",
        ],
        READER: [
            "verification bandwidth contradiction probe",
            "two synthetic adequacy traces",
            "not a model benchmark result",
        ],
        OUTLINE: [
            CODEX_TEST_NAME,
            PROOF_TAG,
            rel(RESULT),
        ],
        ROADMAP: [
            "Verification bandwidth contradiction probe",
            "deterministic synthetic contradiction and adequacy fixture",
            "no support-state promotion",
        ],
        CHANGELOG: [
            "Verification bandwidth contradiction probe",
            rel(RESULT),
        ],
        VALIDATION_REGISTRY: [
            "scripts/validate_verification_bandwidth_probe.py",
            "docs/verification_bandwidth_probe.md",
            "experiments/verification_bandwidth/results/2026-07-02-local.json",
            '"script": "validate_verification_bandwidth_probe.py"',
        ],
    }
    for path, phrases in required.items():
        if not path.exists():
            errors.append(f"Missing required verification bandwidth surface {rel(path)}.")
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        lowered = text.lower()
        for phrase in phrases:
            if phrase.lower() not in lowered:
                errors.append(f"{rel(path)} missing required phrase {phrase!r}.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-result", action="store_true")
    args = parser.parse_args()

    errors: list[str] = []
    valid_count = 0
    invalid_count = 0
    for trace in TRACES:
        expect_valid = bool(trace.get("expect_valid"))
        trace_id = str(trace.get("trace_id", "<missing>"))
        current_errors = trace_errors(trace)
        if expect_valid:
            valid_count += 1
            errors.extend(current_errors)
        else:
            invalid_count += 1
            if not current_errors:
                errors.append(f"{trace_id}: expected-invalid control unexpectedly passed.")

    if valid_count != 2:
        errors.append("Expected exactly two valid synthetic adequacy traces.")
    if invalid_count != 7:
        errors.append("Expected exactly seven expected-invalid controls.")

    expected = build_expected_result(valid_count, invalid_count)
    validate_result(expected, args.write_result, errors)
    validate_manifest(errors)
    validate_lean(errors)
    validate_surfaces(errors)

    if errors:
        fail(errors)
    print("Verification bandwidth probe validation passed.")


if __name__ == "__main__":
    main()
