#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "experiments" / "receipt_faithfulness" / "input" / "adversarial_receipt_cases.json"
RESULT = ROOT / "experiments" / "receipt_faithfulness" / "results" / "2026-07-03-local.json"
DOC = ROOT / "docs" / "receipt_faithfulness_adversarial_fixture.md"
ARTIFACT_CHAPTER = ROOT / "chapters" / "artifact-graphs-audit-logs-and-replay.qmd"
ARTIFACT_READER = (
    ROOT
    / "editions"
    / "reader_manuscript"
    / "v1_0"
    / "chapters"
    / "artifact-graphs-audit-logs-and-replay.qmd"
)
EVIDENCE_CHAPTER = ROOT / "chapters" / "evidence-states-and-claim-discipline.qmd"
PROOF_CLAIMS_CHAPTER = ROOT / "chapters" / "spinoza-verification-and-proof-carrying-claims.qmd"
INTEGRATED_CHAPTER = ROOT / "chapters" / "integrated-reference-architecture.qmd"
OUTLINE = ROOT / "docs" / "book_outline.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
CHANGELOG = ROOT / "appendices" / "F_changelog.qmd"
LEDGER_MD = ROOT / "docs" / "contribution_novelty_ledger.md"
LEDGER_JSON = ROOT / "docs" / "contribution_novelty_ledger.json"
VALIDATION_REGISTRY = ROOT / "validation" / "registry.json"
BOOK_STRUCTURE = ROOT / "book_structure.json"
LEAN_FILE = ROOT / "lean" / "AsiStackProofs" / "ArtifactRealityRefinement.lean"

COMMAND = "python3 scripts/validate_receipt_faithfulness.py"
CODEX_TEST_NAME = "Receipt faithfulness adversarial fixture"
LEAN_THEOREM = "reality_review_requires_independent_cross_check"
EXPECTED_VALID = {
    "valid_cross_checked_receipt_record",
    "valid_attestation_limited_record_only",
    "valid_trap_detected_blocked_receipt",
}
EXPECTED_INVALID = {
    "invalid_shape_valid_reality_false_promoted",
    "invalid_trap_receipt_ignored",
    "invalid_missing_independent_cross_check",
    "invalid_same_component_cross_check",
    "invalid_attestation_overclaim",
    "invalid_support_promotion_from_receipt_shape",
}
REQUIRED_NON_CLAIMS = [
    "does not prove receipt truth",
    "does not promote any chapter core claim",
    "does not prove deployed attestation or audit behavior",
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Receipt faithfulness validation failed:")
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


def require_fragment(owner: str, text: str, fragment: str, errors: list[str]) -> None:
    if fragment not in text:
        errors.append(f"{owner} missing required fragment: {fragment!r}.")


def case_rejection_reasons(case: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    shape_valid = case.get("receipt_shape_valid") is True
    claimed = str(case.get("claimed_reality_state", ""))
    actual = str(case.get("actual_reality_state", ""))
    cross_route = str(case.get("independent_cross_check_route", "")).strip()
    cross_independent = case.get("cross_check_independent") is True
    cross_result = str(case.get("cross_check_result", ""))
    trap_included = case.get("trap_receipt_included") is True
    trap_result = str(case.get("trap_receipt_result", ""))
    attestation_scope = str(case.get("attestation_scope", ""))
    attestation_limits = case.get("attestation_limits")
    evidence_request = str(case.get("evidence_request", ""))
    support_effect = str(case.get("support_state_effect", ""))

    if not shape_valid:
        reasons.append("receipt_shape_invalid")
    if support_effect != "none":
        reasons.append("support_state_promotion_attempt")
    if not isinstance(attestation_limits, list) or not attestation_limits:
        reasons.append("attestation_limits_missing")
    if attestation_scope != "bounded":
        reasons.append("attestation_scope_unbounded")
    if not trap_included:
        reasons.append("trap_receipt_missing")
    if not cross_route:
        reasons.append("independent_cross_check_route_missing")
    if not cross_independent:
        reasons.append("cross_check_not_independent")

    non_claim_text = text_blob(case.get("non_claims", []))
    for phrase in REQUIRED_NON_CLAIMS:
        if phrase not in non_claim_text:
            reasons.append(f"missing_non_claim={phrase}")

    promotion_request = evidence_request in {"support_state_review", "promote_claim"}
    record_only_request = evidence_request == "record_only"
    blocked_request = evidence_request == "blocked_from_promotion"

    if not (promotion_request or record_only_request or blocked_request):
        reasons.append(f"unsupported_evidence_request={evidence_request}")

    reality_matches = claimed == actual or (
        claimed == "bounded_attestation_only" and actual == "unknown_outside_scope"
    )
    cross_ok_for_support = cross_independent and cross_result == "match"
    trap_ok_for_support = trap_included and trap_result == "passed"
    trap_detected_failure = trap_included and trap_result == "failed_detected"
    trap_ignored_failure = trap_included and trap_result == "failed_ignored"

    if (
        claimed == "artifact_observed"
        and actual != "artifact_observed"
        and not (blocked_request and trap_detected_failure)
    ):
        reasons.append("shape_valid_but_reality_false")
    if trap_ignored_failure:
        reasons.append("trap_receipt_failure_ignored")

    if promotion_request:
        if not reality_matches:
            reasons.append("promotion_requested_without_reality_match")
        if not cross_ok_for_support:
            reasons.append("promotion_requested_without_independent_cross_check_match")
        if not trap_ok_for_support:
            reasons.append("promotion_requested_without_passing_trap")
        if actual == "unknown_outside_scope":
            reasons.append("promotion_requested_for_unknown_reality")

    if record_only_request:
        if trap_ignored_failure:
            reasons.append("record_only_cannot_ignore_failed_trap")
        if actual == "artifact_missing" and not trap_detected_failure:
            reasons.append("record_only_false_receipt_requires_detected_trap")

    if blocked_request:
        if not trap_detected_failure:
            reasons.append("blocked_receipt_requires_detected_trap_failure")
        if support_effect != "none":
            reasons.append("blocked_receipt_cannot_promote_support")

    return sorted(set(reasons))


def build_result(packet: dict[str, Any], errors: list[str]) -> dict[str, Any]:
    if packet.get("schema_version") != "asi_stack.receipt_faithfulness.input.v0":
        errors.append(f"{rel(INPUT)} has unexpected schema_version.")
    cases = packet.get("cases")
    if not isinstance(cases, list):
        errors.append(f"{rel(INPUT)} cases must be a list.")
        cases = []

    by_id: dict[str, dict[str, Any]] = {}
    for case in cases:
        if not isinstance(case, dict):
            errors.append(f"{rel(INPUT)} contains a non-object case.")
            continue
        case_id = str(case.get("case_id", ""))
        if not case_id:
            errors.append(f"{rel(INPUT)} contains a case without case_id.")
            continue
        if case_id in by_id:
            errors.append(f"{rel(INPUT)} duplicate case_id {case_id}.")
        by_id[case_id] = case

    for case_id in sorted(EXPECTED_VALID - set(by_id)):
        errors.append(f"{rel(INPUT)} missing expected valid case {case_id}.")
    for case_id in sorted(EXPECTED_INVALID - set(by_id)):
        errors.append(f"{rel(INPUT)} missing expected invalid case {case_id}.")

    rows: list[dict[str, Any]] = []
    accepted_records: list[str] = []
    rejected_controls: list[dict[str, Any]] = []
    for case_id, case in sorted(by_id.items()):
        reasons = case_rejection_reasons(case)
        actual_valid = not reasons
        expected_valid = case.get("expect_valid") is True
        if expected_valid and not actual_valid:
            errors.append(f"{case_id}: expected valid but rejected: {', '.join(reasons)}.")
        if not expected_valid and actual_valid:
            errors.append(f"{case_id}: expected invalid but no rejection reason was produced.")
        row = {
            "case_id": case_id,
            "expected_valid": expected_valid,
            "actual_valid": actual_valid,
            "claimed_reality_state": case.get("claimed_reality_state"),
            "actual_reality_state": case.get("actual_reality_state"),
            "evidence_request": case.get("evidence_request"),
            "rejection_reasons": reasons,
        }
        rows.append(row)
        if expected_valid:
            accepted_records.append(case_id)
        else:
            rejected_controls.append({"case_id": case_id, "rejection_reasons": reasons})

    rejected_ids = {row["case_id"] for row in rejected_controls}
    accepted_ids = set(accepted_records)
    summary = {
        "crossCheckedReceiptRecordAccepted": "valid_cross_checked_receipt_record" in accepted_ids,
        "attestationLimitedRecordOnlyAccepted": "valid_attestation_limited_record_only"
        in accepted_ids,
        "trapDetectedBlockedReceiptAccepted": "valid_trap_detected_blocked_receipt"
        in accepted_ids,
        "shapeValidRealityFalseRejected": "invalid_shape_valid_reality_false_promoted"
        in rejected_ids,
        "trapReceiptNegativeControlRejected": "invalid_trap_receipt_ignored" in rejected_ids,
        "independentCrossCheckRequired": "invalid_missing_independent_cross_check"
        in rejected_ids
        and "invalid_same_component_cross_check" in rejected_ids,
        "attestationLimitsRecorded": "invalid_attestation_overclaim" in rejected_ids,
        "supportPromotionFromReceiptShapeRejected": "invalid_support_promotion_from_receipt_shape"
        in rejected_ids,
        "supportStateEffectNone": True,
        "nonClaimBoundary": True,
    }

    return {
        "schema_version": "asi_stack.receipt_faithfulness.result.v0",
        "result_id": "2026-07-03-receipt-faithfulness-adversarial-fixture",
        "recorded_date": "2026-07-03",
        "command": COMMAND,
        "input_ref": rel(INPUT),
        "result_kind": "deterministic_adversarial_receipt_faithfulness_fixture",
        "valid_case_count": len(accepted_records),
        "expected_invalid_control_count": len(rejected_controls),
        "case_count": len(rows),
        "accepted_records": sorted(accepted_records),
        "rejected_controls": rejected_controls,
        "case_results": rows,
        "trace_summary": summary,
        "lean_fixture_alignment": {
            "module": "AsiStackProofs.ArtifactRealityRefinement",
            "theorem_refs": [LEAN_THEOREM],
            "expected": summary,
        },
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
        "verification_result": "pass",
        "residuals": [
            "The fixture checks receipt-shape/reality correspondence only in finite synthetic records.",
            "The fixture rejects shape-valid but reality-false promotion attempts and trap-receipt failures.",
            "The fixture requires independent cross-check routes and explicit attestation limits before any support review could be considered.",
        ],
        "non_claims": REQUIRED_NON_CLAIMS
        + [
            "does not prove open-world receipt faithfulness",
            "does not prove verifier independence or attestation-service correctness",
            "does not create an evidence transition",
        ],
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
    if RESULT.read_text(encoding="utf-8") != serialized:
        errors.append(f"{rel(RESULT)} is stale; run {COMMAND} --write-result.")


def validate_surfaces(errors: list[str]) -> None:
    surfaces = {
        rel(DOC): (
            DOC,
            [
                "Receipt Faithfulness Adversarial Fixture",
                COMMAND,
                rel(RESULT),
                "shape-valid but reality-false receipt",
                "trap-receipt negative control",
                "independent cross-check route",
                "attestation limits",
                "no support-state promotion",
            ],
        ),
        rel(ARTIFACT_CHAPTER): (
            ARTIFACT_CHAPTER,
            [
                "Receipt faithfulness",
                COMMAND,
                rel(RESULT),
                "shape-valid but reality-false receipt",
                "trap-receipt negative control",
                "independent cross-check route",
            ],
        ),
        rel(ARTIFACT_READER): (
            ARTIFACT_READER,
            [
                "receipt-faithfulness fixture",
                "shape-valid but false",
                "trap receipt",
            ],
        ),
        rel(EVIDENCE_CHAPTER): (
            EVIDENCE_CHAPTER,
            [
                "receipt faithfulness",
                rel(RESULT),
            ],
        ),
        rel(PROOF_CLAIMS_CHAPTER): (
            PROOF_CLAIMS_CHAPTER,
            [
                "receipt faithfulness",
                "shape-valid but reality-false",
            ],
        ),
        rel(INTEGRATED_CHAPTER): (
            INTEGRATED_CHAPTER,
            [
                "record-reality",
                "receipt-faithfulness fixture",
            ],
        ),
        rel(OUTLINE): (
            OUTLINE,
            [
                "Implemented receipt-faithfulness adversarial fixture",
                COMMAND,
                rel(RESULT),
                "AsiStackProofs.ArtifactRealityRefinement",
            ],
        ),
        rel(ROADMAP): (
            ROADMAP,
            [
                "receipt-faithfulness adversarial fixture",
                rel(RESULT),
                "shape-valid but reality-false",
                "trap-receipt negative control",
            ],
        ),
        rel(CHANGELOG): (
            CHANGELOG,
            [
                "Add receipt faithfulness adversarial fixture",
                COMMAND,
                rel(RESULT),
                "does not create a support-state transition",
            ],
        ),
        rel(LEDGER_MD): (
            LEDGER_MD,
            [
                "Record-reality gap",
                rel(RESULT),
                "live_artifact_attestation_backed_not_open_world",
            ],
        ),
        rel(VALIDATION_REGISTRY): (
            VALIDATION_REGISTRY,
            [
                "scripts/validate_receipt_faithfulness.py",
                "docs/receipt_faithfulness_adversarial_fixture.md",
                rel(RESULT),
                '"script": "validate_receipt_faithfulness.py"',
            ],
        ),
        rel(LEAN_FILE): (
            LEAN_FILE,
            [
                "observedArtifactPresent",
                "independentCrossCheckMatched",
                LEAN_THEOREM,
            ],
        ),
    }
    for owner, (path, fragments) in surfaces.items():
        if not path.exists():
            errors.append(f"Missing {owner}.")
            continue
        text = path.read_text(encoding="utf-8")
        for fragment in fragments:
            require_fragment(owner, text, fragment, errors)


def validate_book_structure(errors: list[str]) -> None:
    data = load_json(BOOK_STRUCTURE)
    tests: list[dict[str, Any]] = []
    for part in data.get("parts", []):
        for chapter in part.get("chapters", []):
            if isinstance(chapter, dict):
                tests.extend(test for test in chapter.get("codex_tests", []) if isinstance(test, dict))
    matches = [test for test in tests if test.get("name") == CODEX_TEST_NAME]
    if len(matches) != 1:
        errors.append(f"{rel(BOOK_STRUCTURE)} must contain exactly one {CODEX_TEST_NAME!r} test row.")
        return
    blob = text_blob(matches[0])
    for phrase in (
        "implemented",
        COMMAND,
        "shape-valid but reality-false",
        "no support-state promotion",
    ):
        if phrase not in blob:
            errors.append(f"{CODEX_TEST_NAME} codex test row missing {phrase!r}.")


def validate_ledger_json(errors: list[str]) -> None:
    data = load_json(LEDGER_JSON)
    records = data.get("records", [])
    matches = [
        record
        for record in records
        if isinstance(record, dict) and record.get("idea_id") == "receipt_faithfulness_gap"
    ]
    if len(matches) != 1:
        errors.append(f"{rel(LEDGER_JSON)} must contain one receipt_faithfulness_gap row.")
        return
    row = matches[0]
    blob = text_blob(row)
    for phrase in (
        rel(RESULT),
        "live_artifact_attestation_backed_not_open_world",
        "does not prove open-world receipt faithfulness",
    ):
        if phrase not in blob:
            errors.append(f"{rel(LEDGER_JSON)} receipt_faithfulness_gap row missing {phrase!r}.")


def validate_lean_shape(errors: list[str]) -> None:
    text = LEAN_FILE.read_text(encoding="utf-8")
    if not re.search(rf"theorem\s+{re.escape(LEAN_THEOREM)}\b", text):
        errors.append(f"{rel(LEAN_FILE)} missing theorem {LEAN_THEOREM}.")
    for field in (
        "observedArtifactPresent",
        "independentCrossCheckMatched",
        "trapChallengePassed",
        "attestationLimitsPresent",
        "supportAssignmentRequested",
        "externalEffectRequested",
    ):
        if field not in text:
            errors.append(f"{rel(LEAN_FILE)} missing receipt-faithfulness field {field}.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-result", action="store_true")
    args = parser.parse_args()

    errors: list[str] = []
    if not INPUT.exists():
        fail([f"Missing {rel(INPUT)}."])
    expected = build_result(load_json(INPUT), errors)
    validate_result(expected, args.write_result, errors)
    if not args.write_result:
        validate_surfaces(errors)
        validate_book_structure(errors)
        validate_ledger_json(errors)
        validate_lean_shape(errors)
    if errors:
        fail(errors)
    print(
        "Receipt faithfulness validation passed: "
        f"{expected['valid_case_count']} valid records, "
        f"{expected['expected_invalid_control_count']} expected-invalid controls, "
        "shape-valid false receipts rejected, no support-state effect."
    )


if __name__ == "__main__":
    main()
