#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "experiments" / "epistemic_tcb" / "input" / "epistemic_tcb_cases.json"
RESULT = ROOT / "experiments" / "epistemic_tcb" / "results" / "2026-07-03-local.json"
DOC = ROOT / "docs" / "epistemic_trusted_computing_base_fixture.md"
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
LEAN_FILE = ROOT / "lean" / "AsiStackProofs" / "ArtifactGraph.lean"

COMMAND = "python3 scripts/validate_epistemic_trusted_computing_base.py"
CODEX_TEST_NAME = "Epistemic trusted computing base fixture"
LEAN_THEOREM = "epistemic_tcb_fixture_bridge"
EXPECTED_VALID = {
    "valid_minimal_epistemic_tcb_record",
    "valid_delegated_verifier_record_only",
    "valid_outside_tcb_blocked_record",
}
EXPECTED_INVALID = {
    "invalid_missing_root_of_trust",
    "invalid_self_verifier_laundering",
    "invalid_unbounded_trust_propagation",
    "invalid_no_recursion_stop_condition",
    "invalid_outside_tcb_residual_erased",
    "invalid_support_promotion_from_tcb_shape",
}
ALLOWED_RULES = {"root_to_delegated_verifier", "consumer_checked_policy"}
REQUIRED_NON_CLAIMS = [
    "does not prove verifier correctness",
    "does not prove deployed trust base behavior",
    "does not promote any chapter core claim",
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Epistemic trusted computing base validation failed:")
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
    request = str(case.get("evidence_request", ""))
    support_effect = str(case.get("support_state_effect", ""))
    tcb_declared = case.get("tcb_declared") is True
    tcb_scope = str(case.get("tcb_scope", ""))
    components = case.get("trusted_core_components")
    roots = case.get("root_of_trust_refs")
    rule = str(case.get("trust_propagation_rule", ""))
    stop = str(case.get("recursion_stop_condition", "")).strip().lower()
    independence = str(case.get("verifier_independence_state", ""))
    self_check = case.get("same_component_self_check") is True
    residuals = case.get("outside_tcb_residuals")

    if request not in {"support_review", "record_only", "blocked_from_promotion"}:
        reasons.append(f"unsupported_evidence_request={request}")
    if support_effect != "none":
        reasons.append("support_state_promotion_attempt")
    if not tcb_declared:
        reasons.append("tcb_not_declared")
    if tcb_scope != "bounded":
        reasons.append("tcb_scope_unbounded")
    if not isinstance(components, list) or len(components) < 3:
        reasons.append("trusted_core_too_small_or_missing")
    if not isinstance(roots, list) or not roots:
        reasons.append("root_of_trust_refs_missing")
    if rule not in ALLOWED_RULES:
        reasons.append("trust_propagation_rule_not_bounded")
    if not stop:
        reasons.append("recursion_stop_condition_missing")
    elif "trust all" in stop or "accepted" == stop:
        reasons.append("recursion_stop_condition_ambient")
    if not isinstance(residuals, list) or not residuals:
        reasons.append("outside_tcb_residuals_missing")

    non_claim_text = text_blob(case.get("non_claims", []))
    for phrase in REQUIRED_NON_CLAIMS:
        if phrase not in non_claim_text:
            reasons.append(f"missing_non_claim={phrase}")

    if request == "support_review":
        if independence != "independent":
            reasons.append("support_review_requires_independent_verifier")
        if self_check:
            reasons.append("support_review_rejects_same_component_self_check")
    elif request == "record_only":
        if self_check:
            reasons.append("record_only_cannot_launder_same_component_self_check")
    elif request == "blocked_from_promotion":
        if not isinstance(residuals, list) or not any("blocked" in str(item).lower() for item in residuals):
            reasons.append("blocked_record_requires_blocking_residual")

    return sorted(set(reasons))


def build_result(packet: dict[str, Any], errors: list[str]) -> dict[str, Any]:
    if packet.get("schema_version") != "asi_stack.epistemic_tcb.input.v0":
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
        rows.append(
            {
                "case_id": case_id,
                "expected_valid": expected_valid,
                "actual_valid": actual_valid,
                "evidence_request": case.get("evidence_request"),
                "verifier_independence_state": case.get("verifier_independence_state"),
                "rejection_reasons": reasons,
            }
        )
        if expected_valid:
            accepted_records.append(case_id)
        else:
            rejected_controls.append({"case_id": case_id, "rejection_reasons": reasons})

    accepted_ids = set(accepted_records)
    rejected_ids = {row["case_id"] for row in rejected_controls}
    summary = {
        "minimalTrustBaseAccepted": "valid_minimal_epistemic_tcb_record" in accepted_ids,
        "delegatedVerifierRecordOnlyAccepted": "valid_delegated_verifier_record_only" in accepted_ids,
        "outsideTcbBlockedRecordAccepted": "valid_outside_tcb_blocked_record" in accepted_ids,
        "missingRootOfTrustRejected": "invalid_missing_root_of_trust" in rejected_ids,
        "selfVerifierLaunderingRejected": "invalid_self_verifier_laundering" in rejected_ids,
        "unboundedTrustPropagationRejected": "invalid_unbounded_trust_propagation" in rejected_ids,
        "recursionStopRequired": "invalid_no_recursion_stop_condition" in rejected_ids,
        "outsideTcbResidualsRequired": "invalid_outside_tcb_residual_erased" in rejected_ids,
        "supportPromotionFromTcbShapeRejected": "invalid_support_promotion_from_tcb_shape"
        in rejected_ids,
        "supportStateEffectNone": True,
        "nonClaimBoundary": True,
    }

    return {
        "schema_version": "asi_stack.epistemic_tcb.result.v0",
        "result_id": "2026-07-03-epistemic-trusted-computing-base-fixture",
        "recorded_date": "2026-07-03",
        "command": COMMAND,
        "input_ref": rel(INPUT),
        "result_kind": "deterministic_epistemic_trusted_computing_base_fixture",
        "valid_case_count": len(accepted_records),
        "expected_invalid_control_count": len(rejected_controls),
        "case_count": len(rows),
        "accepted_records": sorted(accepted_records),
        "rejected_controls": rejected_controls,
        "case_results": rows,
        "trace_summary": summary,
        "lean_fixture_alignment": {
            "module": "AsiStackProofs.ArtifactGraph",
            "theorem_refs": [LEAN_THEOREM],
            "expected": summary,
        },
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
        "verification_result": "pass",
        "residuals": [
            "The fixture checks trust-base routing only in finite synthetic records.",
            "The fixture names where verification trust bottoms out but does not prove the root policy, verifier, or audit log are correct.",
            "The fixture rejects verifier-trust laundering, ambient trust, missing recursion stops, erased outside-TCB residuals, and support promotion from trust-base shape.",
        ],
        "non_claims": REQUIRED_NON_CLAIMS
        + [
            "does not prove an open-world epistemic trusted computing base",
            "does not prove audit-log durability, policy correctness, or verifier independence outside the finite records",
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
                "Epistemic Trusted Computing Base Fixture",
                COMMAND,
                rel(RESULT),
                "verifier-trust laundering",
                "recursion stops",
                "no support-state promotion",
            ],
        ),
        rel(ARTIFACT_CHAPTER): (
            ARTIFACT_CHAPTER,
            [
                "epistemic trusted computing base",
                COMMAND,
                rel(RESULT),
                "verifier-trust laundering",
            ],
        ),
        rel(ARTIFACT_READER): (
            ARTIFACT_READER,
            [
                "epistemic trusted computing base",
                "same component",
            ],
        ),
        rel(EVIDENCE_CHAPTER): (
            EVIDENCE_CHAPTER,
            [
                "epistemic trusted computing base",
                rel(RESULT),
            ],
        ),
        rel(PROOF_CLAIMS_CHAPTER): (
            PROOF_CLAIMS_CHAPTER,
            [
                "epistemic trusted computing base",
                "verifier-trust laundering",
            ],
        ),
        rel(INTEGRATED_CHAPTER): (
            INTEGRATED_CHAPTER,
            [
                "epistemic trusted computing base",
                "recursion stop",
            ],
        ),
        rel(OUTLINE): (
            OUTLINE,
            [
                "Implemented epistemic-TCB fixture",
                COMMAND,
                rel(RESULT),
                LEAN_THEOREM,
            ],
        ),
        rel(ROADMAP): (
            ROADMAP,
            [
                "epistemic trusted computing base",
                rel(RESULT),
                "verifier-trust laundering",
            ],
        ),
        rel(CHANGELOG): (
            CHANGELOG,
            [
                "Add epistemic trusted computing base fixture",
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
                "epistemic trusted computing base",
            ],
        ),
        rel(VALIDATION_REGISTRY): (
            VALIDATION_REGISTRY,
            [
                "scripts/validate_epistemic_trusted_computing_base.py",
                "docs/epistemic_trusted_computing_base_fixture.md",
                rel(RESULT),
                '"script": "validate_epistemic_trusted_computing_base.py"',
            ],
        ),
        rel(LEAN_FILE): (
            LEAN_FILE,
            [
                "EpistemicTcbFixtureSummary",
                "epistemicTcbFixtureSummary",
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
        "verifier-trust laundering",
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
    blob = text_blob(matches[0])
    for phrase in (
        rel(RESULT),
        "epistemic trusted computing base",
        "does not prove verifier correctness",
    ):
        if phrase not in blob:
            errors.append(f"{rel(LEDGER_JSON)} receipt_faithfulness_gap row missing {phrase!r}.")


def validate_lean_shape(errors: list[str]) -> None:
    text = LEAN_FILE.read_text(encoding="utf-8")
    if not re.search(rf"theorem\s+{re.escape(LEAN_THEOREM)}\b", text):
        errors.append(f"{rel(LEAN_FILE)} missing theorem {LEAN_THEOREM}.")
    for field in (
        "minimalTrustBaseAccepted",
        "delegatedVerifierRecordOnlyAccepted",
        "outsideTcbBlockedRecordAccepted",
        "missingRootOfTrustRejected",
        "selfVerifierLaunderingRejected",
        "unboundedTrustPropagationRejected",
        "recursionStopRequired",
        "outsideTcbResidualsRequired",
        "supportPromotionFromTcbShapeRejected",
        "supportStateEffectNone",
        "nonClaimBoundary",
    ):
        if field not in text:
            errors.append(f"{rel(LEAN_FILE)} missing epistemic-TCB field {field}.")


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
        "Epistemic trusted computing base validation passed: "
        f"{expected['valid_case_count']} valid records, "
        f"{expected['expected_invalid_control_count']} expected-invalid controls, "
        "verifier-trust laundering rejected, no support-state effect."
    )


if __name__ == "__main__":
    main()
