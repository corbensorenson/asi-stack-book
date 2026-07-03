#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "experiments" / "human_oversight_degradation" / "input" / "human_oversight_cases.json"
RESULT = ROOT / "experiments" / "human_oversight_degradation" / "results" / "2026-07-03-local.json"
DOC = ROOT / "docs" / "human_oversight_degradation_fixture.md"
RUNTIME_CHAPTER = ROOT / "chapters" / "runtime-adapters-tool-permissions-and-human-approval.qmd"
RUNTIME_READER = (
    ROOT
    / "editions"
    / "reader_manuscript"
    / "v1_0"
    / "chapters"
    / "runtime-adapters-tool-permissions-and-human-approval.qmd"
)
INTENT_CHAPTER = ROOT / "chapters" / "human-intent-as-a-formal-input.qmd"
EVIDENCE_CHAPTER = ROOT / "chapters" / "evidence-states-and-claim-discipline.qmd"
OUTLINE = ROOT / "docs" / "book_outline.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
CHANGELOG = ROOT / "appendices" / "F_changelog.qmd"
LEDGER_MD = ROOT / "docs" / "contribution_novelty_ledger.md"
LEDGER_JSON = ROOT / "docs" / "contribution_novelty_ledger.json"
VALIDATE_BOOK = ROOT / "scripts" / "validate_book.py"
BOOK_STRUCTURE = ROOT / "book_structure.json"
LEAN_FILE = ROOT / "lean" / "AsiStackProofs" / "RuntimeAdapters.lean"

COMMAND = "python3 scripts/validate_human_oversight_degradation.py"
CODEX_TEST_NAME = "Human oversight degradation fixture"
LEAN_THEOREM = "human_oversight_degradation_fixture_bridge"
EXPECTED_VALID = {
    "valid_scoped_restored_reviewer_approval",
    "valid_fatigue_routed_to_reviewer_rotation",
    "valid_automation_bias_blocked_record",
}
EXPECTED_INVALID = {
    "invalid_missing_reviewer_qualification",
    "invalid_fatigued_reviewer_accepted",
    "invalid_rubber_stamp_approval_accepted",
    "invalid_automation_bias_contradiction_ignored",
    "invalid_alarm_fatigue_ordinary_approval",
    "invalid_support_promotion_from_human_approval",
    "invalid_missing_non_claim_boundary",
}
REQUIRED_NON_CLAIMS = [
    "does not prove approval-service quality",
    "does not prove deployed human-factors behavior",
    "does not promote any chapter core claim",
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Human oversight degradation validation failed:")
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


def route_for(case: dict[str, Any]) -> str:
    non_claim_text = text_blob(case.get("non_claims", []))
    if str(case.get("support_state_effect", "")) != "none":
        return "block_support_promotion"
    if any(phrase not in non_claim_text for phrase in REQUIRED_NON_CLAIMS):
        return "request_non_claim_boundary"
    if case.get("reviewer_qualified") is not True:
        return "reject_unqualified_reviewer"
    if (
        float(case.get("alert_false_positive_rate", 0.0)) >= 0.75
        and int(case.get("alert_load_count", 0)) >= 8
    ):
        return "escalate_alarm_fatigue"
    if float(case.get("approval_load_index", 0.0)) >= 0.8 or int(case.get("consecutive_approvals", 0)) >= 8:
        return "rotate_or_delay_review"
    if (
        case.get("automation_recommendation_present") is True
        and case.get("contradictory_evidence_visible") is True
        and case.get("independent_evidence_checked") is not True
    ):
        return "block_automation_bias"
    if (
        str(case.get("decision", "")) == "approve"
        and (
            int(case.get("review_duration_seconds", 0)) < 30
            or str(case.get("rationale_quality", "")) in {"empty", "template_only"}
        )
    ):
        return "block_rubber_stamp"
    if case.get("high_impact") is True and str(case.get("approval_scope", "")) != "scoped":
        return "request_scoped_approval"
    if (
        case.get("approval_recorded") is True
        and str(case.get("approval_expiry_state", "")) == "active"
        and str(case.get("decision", "")) == "approve"
    ):
        return "accept_scoped_human_approval"
    return "request_review_completion"


def build_result(packet: dict[str, Any], errors: list[str]) -> dict[str, Any]:
    if packet.get("schema_version") != "asi_stack.human_oversight_degradation.input.v0":
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
        actual_route = route_for(case)
        expected_valid = case.get("expect_valid") is True
        if expected_valid:
            expected_route = str(case.get("expected_route", ""))
            if actual_route != expected_route:
                errors.append(f"{case_id}: expected route {expected_route}, got {actual_route}.")
            accepted_records.append(case_id)
        else:
            forbidden_route = str(case.get("forbidden_route", "accept_scoped_human_approval"))
            if actual_route == forbidden_route:
                errors.append(f"{case_id}: invalid control reached forbidden route {forbidden_route}.")
            rejected_controls.append({"case_id": case_id, "actual_route": actual_route})
        rows.append(
            {
                "case_id": case_id,
                "expected_valid": expected_valid,
                "actual_route": actual_route,
                "decision": case.get("decision"),
                "support_state_effect": case.get("support_state_effect"),
            }
        )

    accepted_ids = set(accepted_records)
    rejected_ids = {row["case_id"] for row in rejected_controls}
    summary = {
        "scopedApprovalAccepted": "valid_scoped_restored_reviewer_approval" in accepted_ids,
        "fatigueRoutedToRotation": "valid_fatigue_routed_to_reviewer_rotation" in accepted_ids,
        "automationBiasBlocked": "valid_automation_bias_blocked_record" in accepted_ids,
        "missingQualificationRejected": "invalid_missing_reviewer_qualification" in rejected_ids,
        "fatiguedApprovalRejected": "invalid_fatigued_reviewer_accepted" in rejected_ids,
        "rubberStampRejected": "invalid_rubber_stamp_approval_accepted" in rejected_ids,
        "automationBiasContradictionRejected": "invalid_automation_bias_contradiction_ignored" in rejected_ids,
        "alarmFatigueEscalated": "invalid_alarm_fatigue_ordinary_approval" in rejected_ids,
        "supportPromotionRejected": "invalid_support_promotion_from_human_approval" in rejected_ids,
        "nonClaimBoundaryRequired": "invalid_missing_non_claim_boundary" in rejected_ids,
        "supportStateEffectNone": True,
        "chapterCoreSupportEffectNone": True,
    }

    return {
        "schema_version": "asi_stack.human_oversight_degradation.result.v0",
        "result_id": "2026-07-03-human-oversight-degradation-fixture",
        "recorded_date": "2026-07-03",
        "command": COMMAND,
        "input_ref": rel(INPUT),
        "result_kind": "deterministic_human_oversight_degradation_fixture",
        "valid_case_count": len(accepted_records),
        "expected_invalid_control_count": len(rejected_controls),
        "case_count": len(rows),
        "accepted_records": sorted(accepted_records),
        "rejected_controls": sorted(rejected_controls, key=lambda row: row["case_id"]),
        "case_results": rows,
        "trace_summary": summary,
        "lean_fixture_alignment": {
            "module": "AsiStackProofs.RuntimeAdapters",
            "theorem_refs": [LEAN_THEOREM],
            "expected": summary,
        },
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
        "verification_result": "pass",
        "residuals": [
            "The fixture checks human-oversight degradation only in finite synthetic records.",
            "The fixture treats reviewer fatigue, rubber-stamping, alarm fatigue, and automation bias as route-changing component failure modes.",
            "The fixture rejects support promotion from approval shape and preserves explicit non-claims.",
        ],
        "non_claims": REQUIRED_NON_CLAIMS
        + [
            "does not prove reviewer correctness",
            "does not prove that human oversight cannot be manipulated",
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
    source_notes = [
        ROOT / "sources" / "source_notes" / "ext_humans_automation_1997.md",
        ROOT / "sources" / "source_notes" / "ext_ironies_automation_1983.md",
        ROOT / "sources" / "source_notes" / "ext_levels_automation_2000.md",
        ROOT / "sources" / "source_notes" / "ext_complacency_bias_automation_2010.md",
    ]
    surfaces = {
        rel(DOC): (
            DOC,
            [
                "Human Oversight Degradation Fixture",
                COMMAND,
                rel(RESULT),
                "approval laundering",
                "no support-state promotion",
            ],
        ),
        rel(RUNTIME_CHAPTER): (
            RUNTIME_CHAPTER,
            [
                "human oversight degradation",
                COMMAND,
                rel(RESULT),
                "approval fatigue",
                "automation bias",
            ],
        ),
        rel(RUNTIME_READER): (
            RUNTIME_READER,
            [
                "human oversight degradation",
                "rubber-stamping",
                "automation bias",
            ],
        ),
        rel(INTENT_CHAPTER): (
            INTENT_CHAPTER,
            [
                "approval fatigue",
                "human oversight degradation",
            ],
        ),
        rel(EVIDENCE_CHAPTER): (
            EVIDENCE_CHAPTER,
            [
                "reviewer degradation",
                rel(RESULT),
            ],
        ),
        rel(OUTLINE): (
            OUTLINE,
            [
                "Implemented human-oversight degradation fixture",
                COMMAND,
                rel(RESULT),
                LEAN_THEOREM,
            ],
        ),
        rel(ROADMAP): (
            ROADMAP,
            [
                "human oversight degradation",
                rel(RESULT),
                "rubber-stamping",
            ],
        ),
        rel(CHANGELOG): (
            CHANGELOG,
            [
                "Add human oversight degradation fixture",
                COMMAND,
                rel(RESULT),
                "does not create a support-state transition",
            ],
        ),
        rel(LEDGER_MD): (
            LEDGER_MD,
            [
                "Human oversight degradation",
                rel(RESULT),
                "approval fatigue",
            ],
        ),
        rel(VALIDATE_BOOK): (
            VALIDATE_BOOK,
            [
                "scripts/validate_human_oversight_degradation.py",
                "docs/human_oversight_degradation_fixture.md",
                rel(RESULT),
                'run_validator("validate_human_oversight_degradation.py")',
            ],
        ),
        rel(LEAN_FILE): (
            LEAN_FILE,
            [
                "HumanOversightDegradationFixtureSummary",
                "humanOversightDegradationFixtureSummary",
                LEAN_THEOREM,
            ],
        ),
    }
    for note in source_notes:
        surfaces[rel(note)] = (
            note,
            [
                "Human oversight degradation",
                "Book Chapters Supported",
                "Open Questions",
            ],
        )
    for owner, (path, fragments) in surfaces.items():
        if not path.exists():
            errors.append(f"Missing {owner}.")
            continue
        text = path.read_text(encoding="utf-8")
        for fragment in fragments:
            require_fragment(owner, text, fragment, errors)


def validate_book_structure(errors: list[str]) -> None:
    data = load_json(BOOK_STRUCTURE)
    runtime_chapter: dict[str, Any] | None = None
    tests: list[dict[str, Any]] = []
    for part in data.get("parts", []):
        for chapter in part.get("chapters", []):
            if isinstance(chapter, dict):
                if chapter.get("id") == "runtime-adapters-tool-permissions-and-human-approval":
                    runtime_chapter = chapter
                tests.extend(test for test in chapter.get("codex_tests", []) if isinstance(test, dict))
    if not runtime_chapter:
        errors.append(f"{rel(BOOK_STRUCTURE)} missing runtime-adapters chapter.")
        return
    source_ids = set(runtime_chapter.get("source_ids", []))
    for source_id in (
        "ext_humans_automation_1997",
        "ext_ironies_automation_1983",
        "ext_levels_automation_2000",
        "ext_complacency_bias_automation_2010",
    ):
        if source_id not in source_ids:
            errors.append(f"{rel(BOOK_STRUCTURE)} runtime chapter missing source id {source_id}.")
    proof_tags = {target.get("tag") for target in runtime_chapter.get("proof_targets", []) if isinstance(target, dict)}
    if "lean:runtime.adapters.human_oversight_degradation_fixture_bridge" not in proof_tags:
        errors.append(f"{rel(BOOK_STRUCTURE)} runtime chapter missing human oversight proof target.")
    matches = [test for test in tests if test.get("name") == CODEX_TEST_NAME]
    if len(matches) != 1:
        errors.append(f"{rel(BOOK_STRUCTURE)} must contain exactly one {CODEX_TEST_NAME!r} test row.")
        return
    blob = text_blob(matches[0])
    for phrase in (
        "implemented",
        COMMAND,
        "rubber-stamping",
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
        if isinstance(record, dict) and record.get("idea_id") == "human_oversight_degradation"
    ]
    if len(matches) != 1:
        errors.append(f"{rel(LEDGER_JSON)} must contain one human_oversight_degradation row.")
        return
    blob = text_blob(matches[0])
    for phrase in (
        rel(RESULT),
        "approval fatigue",
        "does not prove approval-service quality",
    ):
        if phrase not in blob:
            errors.append(f"{rel(LEDGER_JSON)} human_oversight_degradation row missing {phrase!r}.")


def validate_lean_shape(errors: list[str]) -> None:
    text = LEAN_FILE.read_text(encoding="utf-8")
    if not re.search(rf"theorem\s+{re.escape(LEAN_THEOREM)}\b", text):
        errors.append(f"{rel(LEAN_FILE)} missing theorem {LEAN_THEOREM}.")
    for field in (
        "scopedApprovalAccepted",
        "fatigueRoutedToRotation",
        "automationBiasBlocked",
        "missingQualificationRejected",
        "fatiguedApprovalRejected",
        "rubberStampRejected",
        "alarmFatigueEscalated",
        "supportPromotionRejected",
        "nonClaimBoundaryRequired",
        "supportStateEffectNone",
        "chapterCoreSupportEffectNone",
    ):
        if field not in text:
            errors.append(f"{rel(LEAN_FILE)} missing human-oversight field {field}.")


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
        "Human oversight degradation validation passed: "
        f"{expected['valid_case_count']} valid records, "
        f"{expected['expected_invalid_control_count']} expected-invalid controls, "
        "fatigue/rubber-stamp/automation-bias controls routed, no support-state effect."
    )


if __name__ == "__main__":
    main()
