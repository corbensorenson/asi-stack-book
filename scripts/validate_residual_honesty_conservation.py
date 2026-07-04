#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "experiments" / "residual_honesty_conservation" / "input" / "residual_conservation_cases.json"
RESULT = ROOT / "experiments" / "residual_honesty_conservation" / "results" / "2026-07-03-local.json"
DOC = ROOT / "docs" / "residual_honesty_conservation.md"
CHAPTER = ROOT / "chapters" / "compact-generative-systems-and-residual-honesty.qmd"
READER = (
    ROOT
    / "editions"
    / "reader_manuscript"
    / "v1_0"
    / "chapters"
    / "compact-generative-systems-and-residual-honesty.qmd"
)
OUTLINE = ROOT / "docs" / "book_outline.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
CHANGELOG = ROOT / "appendices" / "F_changelog.qmd"
LEDGER_MD = ROOT / "docs" / "contribution_novelty_ledger.md"
LEDGER_JSON = ROOT / "docs" / "contribution_novelty_ledger.json"
VALIDATE_BOOK = ROOT / "scripts" / "validate_book.py"
LEAN_FILE = ROOT / "lean" / "AsiStackProofs" / "CompactGenerativeSystems.lean"

COMMAND = "python3 scripts/validate_residual_honesty_conservation.py"
CODEX_TEST_NAME = "Residual honesty conservation fixture"
LEAN_THEOREM = "residual_honesty_conservation_fixture_bridge"
EXPECTED_VALID = {
    "valid_accepted_visible_residual",
    "valid_deferred_owned_residual",
    "valid_discharged_residual_with_receipt",
}
EXPECTED_INVALID = {
    "invalid_hidden_residual_after_metric_gain",
    "invalid_erased_residual_without_discharge",
    "invalid_moved_residual_without_owner",
    "invalid_residual_fixture_support_promotion",
    "invalid_zero_residual_claim_with_remaining_burden",
}
REQUIRED_NON_CLAIMS = [
    "does not prove all residuals are observable",
    "does not prove safety",
    "does not promote any chapter core claim",
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Residual honesty conservation validation failed:")
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


def case_rejection_reasons(case: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    state = str(case.get("residual_state", ""))
    burden = int(case.get("residual_burden_units", 0))
    visible = case.get("residual_visible") is True
    owner = str(case.get("residual_owner", "")).strip()
    remaining_recorded = case.get("remaining_burden_recorded") is True
    metric_gain = case.get("metric_improvement_claimed") is True
    declared_zero = case.get("declared_zero_residual") is True

    if case.get("support_state_effect") != "none":
        reasons.append("support_state_promotion_attempt")

    if burden > 0 and not visible:
        reasons.append("positive_residual_not_visible")
    if burden > 0 and not remaining_recorded:
        reasons.append("remaining_burden_not_recorded")
    if burden > 0 and not owner:
        reasons.append("positive_residual_without_owner")
    if burden > 0 and declared_zero:
        reasons.append("zero_residual_claim_with_remaining_burden")
    if metric_gain and burden > 0 and not visible:
        reasons.append("metric_gain_hides_residual")

    if state == "accepted":
        if burden <= 0:
            reasons.append("accepted_residual_needs_positive_remaining_burden")
        if not str(case.get("evidence_ref", "")).startswith("evidence://"):
            reasons.append("accepted_residual_missing_evidence_ref")
    elif state == "deferred":
        if burden <= 0:
            reasons.append("deferred_residual_needs_positive_remaining_burden")
        if not str(case.get("due_condition", "")).strip():
            reasons.append("deferred_residual_missing_due_condition")
    elif state == "discharged":
        if burden != 0:
            reasons.append("discharged_residual_must_have_zero_remaining_burden")
        if not str(case.get("discharge_artifact_ref", "")).startswith("artifact://"):
            reasons.append("discharged_residual_missing_artifact")
        if case.get("discharge_reviewed") is not True:
            reasons.append("discharged_residual_missing_review")
    elif state == "hidden":
        reasons.append("hidden_residual_rejected")
    elif state == "erased":
        if not str(case.get("discharge_artifact_ref", "")).startswith("artifact://"):
            reasons.append("erased_residual_without_discharge_artifact")
    elif state == "moved":
        if not owner:
            reasons.append("moved_residual_without_owner")
    elif state == "none":
        if burden > 0:
            reasons.append("undeclared_remaining_residual")
    else:
        reasons.append(f"unknown_residual_state={state}")

    non_claim_text = text_blob(case.get("non_claims", []))
    for phrase in REQUIRED_NON_CLAIMS:
        if phrase not in non_claim_text:
            reasons.append(f"missing_non_claim={phrase}")
    return sorted(set(reasons))


def build_result(packet: dict[str, Any], errors: list[str]) -> dict[str, Any]:
    if packet.get("schema_version") != "asi_stack.residual_honesty_conservation.input.v0":
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

    missing_valid = sorted(EXPECTED_VALID - set(by_id))
    missing_invalid = sorted(EXPECTED_INVALID - set(by_id))
    for case_id in missing_valid:
        errors.append(f"{rel(INPUT)} missing expected valid case {case_id}.")
    for case_id in missing_invalid:
        errors.append(f"{rel(INPUT)} missing expected invalid case {case_id}.")

    rows: list[dict[str, Any]] = []
    valid_cases: list[str] = []
    rejected_controls: list[dict[str, Any]] = []
    for case_id, case in sorted(by_id.items()):
        reasons = case_rejection_reasons(case)
        actual_valid = not reasons
        expected_valid = case.get("expect_valid") is True
        if expected_valid and not actual_valid:
            errors.append(f"{case_id}: expected valid but rejected: {', '.join(reasons)}.")
        if not expected_valid and actual_valid:
            errors.append(f"{case_id}: expected invalid but no rejection reason was produced.")
        if expected_valid:
            valid_cases.append(case_id)
        else:
            rejected_controls.append({"case_id": case_id, "rejection_reasons": reasons})
        rows.append(
            {
                "case_id": case_id,
                "residual_state": case.get("residual_state"),
                "expected_valid": expected_valid,
                "actual_valid": actual_valid,
                "residual_burden_units": case.get("residual_burden_units"),
                "rejection_reasons": reasons,
            }
        )

    result = {
        "schema_version": "asi_stack.residual_honesty_conservation.result.v0",
        "result_id": "2026-07-03-residual-honesty-conservation",
        "recorded_date": "2026-07-03",
        "command": COMMAND,
        "input_ref": rel(INPUT),
        "result_kind": "deterministic_synthetic_residual_conservation_fixture",
        "valid_case_count": len(valid_cases),
        "expected_invalid_control_count": len(rejected_controls),
        "case_count": len(rows),
        "valid_cases": sorted(valid_cases),
        "rejected_controls": rejected_controls,
        "case_results": rows,
        "conservation_summary": {
            "accepted_residual_recorded": "valid_accepted_visible_residual" in valid_cases,
            "deferred_residual_owned": "valid_deferred_owned_residual" in valid_cases,
            "discharged_residual_has_receipt": "valid_discharged_residual_with_receipt" in valid_cases,
            "hidden_residual_rejected": "invalid_hidden_residual_after_metric_gain"
            in {row["case_id"] for row in rejected_controls},
            "erased_residual_rejected": "invalid_erased_residual_without_discharge"
            in {row["case_id"] for row in rejected_controls},
            "unowned_moved_residual_rejected": "invalid_moved_residual_without_owner"
            in {row["case_id"] for row in rejected_controls},
            "support_promotion_rejected": "invalid_residual_fixture_support_promotion"
            in {row["case_id"] for row in rejected_controls},
            "zero_residual_overclaim_rejected": "invalid_zero_residual_claim_with_remaining_burden"
            in {row["case_id"] for row in rejected_controls},
        },
        "lean_fixture_alignment": {
            "module": "AsiStackProofs.CompactGenerativeSystems",
            "theorem_refs": [LEAN_THEOREM],
            "expected": {
                "acceptedResidualRecorded": True,
                "deferredResidualOwned": True,
                "dischargedResidualHasReceipt": True,
                "hiddenResidualRejected": True,
                "erasedResidualRejected": True,
                "unownedMovedResidualRejected": True,
                "supportStateEffectNone": True,
                "nonClaimBoundary": True,
            },
        },
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
        "verification_result": "pass",
        "residuals": [
            "Synthetic record-level fixture only; no deployed residual ledger, codec, generator, verifier, fallback service, or semantic graph was measured.",
            "The fixture treats visible residual cases as record obligations and rejects hidden, erased, unowned, and support-promoting controls.",
            "The chapter core claim remains at argument support.",
        ],
        "non_claims": REQUIRED_NON_CLAIMS
        + [
            "does not prove residual conservation for all real systems",
            "does not prove deployed residual detection, model quality, benchmark performance, or compression utility",
        ],
    }
    return result


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
        errors.append(f"{rel(RESULT)}: support_state_effect must be none.")


def validate_lean(errors: list[str]) -> None:
    text = LEAN_FILE.read_text(encoding="utf-8", errors="ignore")
    if not re.search(rf"\btheorem\s+{re.escape(LEAN_THEOREM)}\b", text):
        errors.append(f"{rel(LEAN_FILE)} missing theorem {LEAN_THEOREM}.")
    for field in (
        "acceptedResidualRecorded",
        "deferredResidualOwned",
        "dischargedResidualHasReceipt",
        "hiddenResidualRejected",
        "erasedResidualRejected",
        "unownedMovedResidualRejected",
        "supportStateEffectNone",
        "nonClaimBoundary",
    ):
        if field not in text:
            errors.append(f"{rel(LEAN_FILE)} missing residual-conservation field {field}.")


def require_surface(path: Path, phrases: list[str], errors: list[str]) -> None:
    if not path.exists():
        errors.append(f"Missing {rel(path)}.")
        return
    text = re.sub(r"\s+", " ", path.read_text(encoding="utf-8", errors="ignore"))
    lowered = text.lower()
    for phrase in phrases:
        if re.sub(r"\s+", " ", phrase).lower() not in lowered:
            errors.append(f"{rel(path)} missing required phrase {phrase!r}.")


def validate_surfaces(errors: list[str]) -> None:
    fixture_nonclaim = "does not prove all residuals are observable"
    chapter_nonclaim = "does not establish that all residuals are observable"
    require_surface(
        DOC,
        [
            "Residual Honesty Conservation Fixture",
            COMMAND,
            rel(INPUT),
            rel(RESULT),
            "3 valid residual records",
            "5 expected-invalid controls",
            "hidden residual after a metric gain",
            "support-state promotion attempt",
            LEAN_THEOREM,
            fixture_nonclaim,
        ],
        errors,
    )
    require_surface(
        CHAPTER,
        [
            "Residual honesty conservation fixture",
            COMMAND,
            rel(RESULT),
            "hidden, erased, unowned, and support-promoting residual controls",
            chapter_nonclaim,
        ],
        errors,
    )
    require_surface(
        READER,
        [
            "residual-conservation fixture",
            "three honest residual records",
            "five dishonest controls",
            "not a proof that all residuals can be found",
        ],
        errors,
    )
    require_surface(
        OUTLINE,
        [
            CODEX_TEST_NAME,
            COMMAND,
            rel(RESULT),
        ],
        errors,
    )
    require_surface(
        ROADMAP,
        [
            "Residual honesty conservation fixture",
            rel(RESULT),
            "hidden, erased, unowned, support-promoting, and zero-residual-overclaim controls",
        ],
        errors,
    )
    require_surface(
        CHANGELOG,
        [
            "Residual honesty conservation fixture",
            rel(RESULT),
        ],
        errors,
    )
    require_surface(
        LEDGER_MD,
        [
            "Residual honesty",
            "residual_storage_replay_backed_not_deployed",
            rel(RESULT),
        ],
        errors,
    )
    ledger = load_json(LEDGER_JSON)
    residual_rows = [row for row in ledger.get("records", []) if row.get("idea_id") == "residual_honesty"]
    if len(residual_rows) != 1:
        errors.append(f"{rel(LEDGER_JSON)} must contain one residual_honesty row.")
    else:
        row = residual_rows[0]
        if row.get("confidence_state") != "residual_storage_replay_backed_not_deployed":
            errors.append(f"{rel(LEDGER_JSON)} residual_honesty confidence_state is stale.")
        if rel(RESULT) not in text_blob(row):
            errors.append(f"{rel(LEDGER_JSON)} residual_honesty row must reference {rel(RESULT)}.")
    require_surface(
        VALIDATE_BOOK,
        [
            "scripts/validate_residual_honesty_conservation.py",
            'run_validator("validate_residual_honesty_conservation.py")',
        ],
        errors,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-result", action="store_true")
    args = parser.parse_args()

    errors: list[str] = []
    if not INPUT.exists():
        fail([f"Missing {rel(INPUT)}."])
    packet = load_json(INPUT)
    if not isinstance(packet, dict):
        fail([f"{rel(INPUT)} must contain an object."])
    result = build_result(packet, errors)
    validate_result(result, args.write_result, errors)
    validate_lean(errors)
    if not args.write_result:
        validate_surfaces(errors)
    if errors:
        fail(errors)
    print(
        "Residual honesty conservation validation passed: "
        f"{result['valid_case_count']} valid residual cases, "
        f"{result['expected_invalid_control_count']} expected-invalid controls, "
        "no support-state effect."
    )


if __name__ == "__main__":
    main()
