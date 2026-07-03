#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESULT = (
    ROOT
    / "experiments"
    / "verification_bandwidth_capacity"
    / "results"
    / "2026-07-03-local.json"
)
DOC = ROOT / "docs" / "verification_bandwidth_capacity_model.md"
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
LEDGER = ROOT / "docs" / "contribution_novelty_ledger.md"
VALIDATE_BOOK = ROOT / "scripts" / "validate_book.py"
LEAN_FILE = ROOT / "lean" / "AsiStackProofs" / "VerificationBandwidth.lean"

COMMAND = "python3 scripts/validate_verification_bandwidth_capacity_model.py"
CODEX_TEST_NAME = "Verification bandwidth capacity model"
LEAN_THEOREM = "verification_bandwidth_capacity_model_fixture_bridge"

REQUIRED_NON_CLAIMS = [
    "does not prove a model verification bandwidth law",
    "does not measure contradiction-rate performance",
    "does not validate an adequacy classifier",
    "does not prove long-context failure in deployed systems",
    "does not promote the chapter support state",
]
ADEQUATE_DECISIONS = {"adequate", "adequate_under_named_decomposition"}

TRACES: list[dict[str, Any]] = [
    {
        "trace_id": "valid_small_joint_check_budget_sufficient",
        "expect_valid": True,
        "claim_id": "claim://local-four-unit-comparison",
        "trace_type": "all_pairwise",
        "semantic_units_identified": True,
        "semantic_unit_count": 4,
        "linear_context_slots": 4,
        "pairwise_obligations": 6,
        "verification_budget_checks": 6,
        "checked_obligations": 6,
        "residual_obligations": 0,
        "capacity_decision": "adequate",
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "valid_long_context_theater_gap",
        "expect_valid": True,
        "claim_id": "claim://twelve-unit-cross-document-safety-comparison",
        "trace_type": "all_pairwise",
        "semantic_units_identified": True,
        "semantic_unit_count": 12,
        "linear_context_slots": 12,
        "pairwise_obligations": 66,
        "verification_budget_checks": 18,
        "checked_obligations": 18,
        "residual_obligations": 48,
        "capacity_decision": "inadequate_split_or_escalate",
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "valid_decomposed_review_names_boundary_checks",
        "expect_valid": True,
        "claim_id": "claim://decomposed-twelve-unit-review",
        "trace_type": "decomposed",
        "semantic_units_identified": True,
        "semantic_unit_count": 12,
        "linear_context_slots": 12,
        "clusters": [4, 4, 4],
        "internal_pairwise_obligations": 18,
        "boundary_obligations": 6,
        "modeled_obligations": 24,
        "full_pairwise_obligations": 66,
        "boundary_checks_named": True,
        "verification_budget_checks": 24,
        "checked_obligations": 24,
        "residual_obligations": 0,
        "capacity_decision": "adequate_under_named_decomposition",
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "invalid_linear_slots_treated_as_pairwise_capacity",
        "expect_valid": False,
        "claim_id": "claim://linear-context-overclaim",
        "trace_type": "all_pairwise",
        "semantic_units_identified": True,
        "semantic_unit_count": 12,
        "linear_context_slots": 12,
        "pairwise_obligations": 66,
        "verification_budget_checks": 12,
        "checked_obligations": 12,
        "residual_obligations": 54,
        "capacity_decision": "adequate",
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "invalid_decomposition_hides_boundary_checks",
        "expect_valid": False,
        "claim_id": "claim://decomposition-without-boundary-checks",
        "trace_type": "decomposed",
        "semantic_units_identified": True,
        "semantic_unit_count": 12,
        "linear_context_slots": 12,
        "clusters": [4, 4, 4],
        "internal_pairwise_obligations": 18,
        "boundary_obligations": 6,
        "modeled_obligations": 24,
        "full_pairwise_obligations": 66,
        "boundary_checks_named": False,
        "verification_budget_checks": 18,
        "checked_obligations": 18,
        "residual_obligations": 0,
        "capacity_decision": "adequate_under_named_decomposition",
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "invalid_hidden_residual_gap",
        "expect_valid": False,
        "claim_id": "claim://hidden-capacity-residual",
        "trace_type": "all_pairwise",
        "semantic_units_identified": True,
        "semantic_unit_count": 12,
        "linear_context_slots": 12,
        "pairwise_obligations": 66,
        "verification_budget_checks": 60,
        "checked_obligations": 60,
        "residual_obligations": 0,
        "capacity_decision": "inadequate_split_or_escalate",
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "invalid_unidentified_units_adequate",
        "expect_valid": False,
        "claim_id": "claim://unidentified-units-capacity-overclaim",
        "trace_type": "all_pairwise",
        "semantic_units_identified": False,
        "semantic_unit_count": 6,
        "linear_context_slots": 6,
        "pairwise_obligations": 15,
        "verification_budget_checks": 15,
        "checked_obligations": 15,
        "residual_obligations": 0,
        "capacity_decision": "adequate",
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "invalid_support_state_promotion",
        "expect_valid": False,
        "claim_id": "claim://capacity-fixture-support-promotion",
        "trace_type": "all_pairwise",
        "semantic_units_identified": True,
        "semantic_unit_count": 4,
        "linear_context_slots": 4,
        "pairwise_obligations": 6,
        "verification_budget_checks": 6,
        "checked_obligations": 6,
        "residual_obligations": 0,
        "capacity_decision": "adequate",
        "support_state_effect": "promote_chapter_core",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Verification bandwidth capacity-model validation failed:")
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


def pairwise_obligations(unit_count: int) -> int:
    return unit_count * (unit_count - 1) // 2


def modeled_obligation_count(trace: dict[str, Any], errors: list[str]) -> int:
    trace_id = str(trace.get("trace_id", "<missing>"))
    trace_type = str(trace.get("trace_type", ""))
    unit_count = int(trace.get("semantic_unit_count", 0))
    if unit_count < 2:
        errors.append(f"{trace_id}: semantic_unit_count must be at least 2.")
    if trace.get("linear_context_slots") != unit_count:
        errors.append(f"{trace_id}: linear_context_slots must equal semantic_unit_count.")

    if trace_type == "all_pairwise":
        expected = pairwise_obligations(unit_count)
        if trace.get("pairwise_obligations") != expected:
            errors.append(f"{trace_id}: pairwise_obligations must equal n*(n-1)/2 = {expected}.")
        return expected

    if trace_type == "decomposed":
        clusters = trace.get("clusters")
        if not isinstance(clusters, list) or not clusters:
            errors.append(f"{trace_id}: decomposed traces need non-empty clusters.")
            clusters = []
        if sum(int(cluster) for cluster in clusters) != unit_count:
            errors.append(f"{trace_id}: decomposition clusters must sum to semantic_unit_count.")
        internal = sum(pairwise_obligations(int(cluster)) for cluster in clusters)
        boundary = int(trace.get("boundary_obligations", 0))
        modeled = internal + boundary
        if trace.get("internal_pairwise_obligations") != internal:
            errors.append(f"{trace_id}: internal_pairwise_obligations must equal {internal}.")
        if trace.get("modeled_obligations") != modeled:
            errors.append(f"{trace_id}: modeled_obligations must equal internal + boundary = {modeled}.")
        if trace.get("full_pairwise_obligations") != pairwise_obligations(unit_count):
            errors.append(f"{trace_id}: full_pairwise_obligations must equal all-pairwise count.")
        if trace.get("boundary_checks_named") is not True:
            errors.append(f"{trace_id}: decomposed adequacy requires named boundary checks.")
        return modeled

    errors.append(f"{trace_id}: unknown trace_type {trace_type!r}.")
    return 0


def trace_errors(trace: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    trace_id = str(trace.get("trace_id", "<missing>"))
    if not isinstance(trace.get("claim_id"), str) or not trace["claim_id"].startswith("claim://"):
        errors.append(f"{trace_id}: claim_id must use claim://.")
    if trace.get("support_state_effect") != "none":
        errors.append(f"{trace_id}: support_state_effect must be none.")
    if trace.get("semantic_units_identified") is not True and trace.get("capacity_decision") in ADEQUATE_DECISIONS:
        errors.append(f"{trace_id}: unidentified semantic units cannot support capacity adequacy.")

    modeled = modeled_obligation_count(trace, errors)
    checked = int(trace.get("checked_obligations", -1))
    budget = int(trace.get("verification_budget_checks", -1))
    residual = int(trace.get("residual_obligations", -1))
    decision = str(trace.get("capacity_decision", ""))
    expected_residual = max(modeled - checked, 0)

    if checked > budget:
        errors.append(f"{trace_id}: checked_obligations cannot exceed verification_budget_checks.")
    if residual != expected_residual:
        errors.append(f"{trace_id}: residual_obligations must equal modeled minus checked ({expected_residual}).")
    if decision in ADEQUATE_DECISIONS and checked < modeled:
        errors.append(f"{trace_id}: adequate capacity decision requires checked obligations to cover modeled obligations.")
    if decision in ADEQUATE_DECISIONS and budget < modeled:
        errors.append(f"{trace_id}: adequate capacity decision requires enough verification budget.")
    if decision in ADEQUATE_DECISIONS and residual != 0:
        errors.append(f"{trace_id}: adequate capacity decision requires zero residual obligations.")
    if decision not in ADEQUATE_DECISIONS and checked < modeled and residual <= 0:
        errors.append(f"{trace_id}: inadequate capacity decisions with missing checks must record residual obligations.")

    non_claim_text = text_blob(trace.get("non_claims", []))
    for phrase in REQUIRED_NON_CLAIMS:
        if phrase.lower() not in non_claim_text:
            errors.append(f"{trace_id}: non_claims missing {phrase!r}.")
    return errors


def build_expected_result(valid_count: int, invalid_count: int) -> dict[str, Any]:
    return {
        "schema_version": "asi_stack.verification_bandwidth_capacity_model.v0",
        "result_id": "2026-07-03-verification-bandwidth-capacity-model",
        "recorded_date": "2026-07-03",
        "command": COMMAND,
        "result_kind": "deterministic_synthetic_verification_capacity_model",
        "valid_trace_count": valid_count,
        "expected_invalid_control_count": invalid_count,
        "trace_count": len(TRACES),
        "capacity_model_summary": {
            "long_context_semantic_units": 12,
            "linear_context_slots": 12,
            "all_pairwise_obligations": 66,
            "verification_budget_checks": 18,
            "checked_obligations": 18,
            "residual_obligations": 48,
            "pairwise_minus_linear_context_gap": 54,
            "decomposed_modeled_obligations": 24,
            "decomposition_boundary_obligations": 6,
            "decomposition_obligation_reduction_vs_all_pairwise": 42,
        },
        "negative_controls": {
            "linear_context_slots_not_pairwise_capacity_rejected": True,
            "decomposition_without_boundary_checks_rejected": True,
            "hidden_residual_gap_rejected": True,
            "unidentified_units_adequacy_rejected": True,
            "support_state_promotion_rejected": True,
        },
        "lean_fixture_alignment": {
            "module": "AsiStackProofs.VerificationBandwidth",
            "theorem_refs": [LEAN_THEOREM],
            "expected": {
                "long_context_capacity_gap_recorded": True,
                "decomposition_trace_present": True,
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
            "Synthetic record-level capacity model only; no model, context window, deployed claim ledger, or escalation service was measured.",
            "The all-pairwise trace is a conservative worst-case obligation model, not a universal theorem about every verifier or decomposition strategy.",
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
    if RESULT.read_text(encoding="utf-8") != serialized:
        errors.append(f"{rel(RESULT)} is stale; run {COMMAND} --write-result.")
    value = load_json(RESULT)
    if value.get("verification_result") != "pass":
        errors.append(f"{rel(RESULT)}: verification_result must be pass.")
    if value.get("support_state_effect") != "none":
        errors.append(f"{rel(RESULT)}: support_state_effect must remain none.")


def validate_lean(errors: list[str]) -> None:
    text = LEAN_FILE.read_text(encoding="utf-8", errors="ignore")
    if not re.search(rf"\btheorem\s+{re.escape(LEAN_THEOREM)}\b", text):
        errors.append(f"{rel(LEAN_FILE)} missing theorem {LEAN_THEOREM}.")
    for field in (
        "longContextCapacityGapRecorded",
        "decompositionTracePresent",
        "negativeControlsRejected",
        "supportStateEffectNone",
        "nonClaimBoundary",
    ):
        if field not in text:
            errors.append(f"{rel(LEAN_FILE)} missing capacity-model field {field}.")


def validate_surfaces(errors: list[str]) -> None:
    required = {
        DOC: [
            "Verification Bandwidth Capacity Model",
            rel(RESULT),
            "12 semantic units",
            "66 all-pairwise obligations",
            "48 residual obligations",
            "no support-state transition",
        ],
        CHAPTER: [
            "Verification bandwidth capacity model",
            rel(RESULT),
            "66 all-pairwise obligations",
            "48 residual obligations",
            "does not prove a model verification bandwidth law",
        ],
        READER: [
            "capacity model",
            "66 comparison obligations",
            "48 residual obligations",
            "not a model benchmark",
        ],
        OUTLINE: [
            CODEX_TEST_NAME,
            rel(RESULT),
            "66 all-pairwise obligations",
        ],
        ROADMAP: [
            "Verification bandwidth capacity model",
            rel(RESULT),
            "48 residual obligations",
            "no support-state promotion",
        ],
        CHANGELOG: [
            "Verification bandwidth capacity model",
            rel(RESULT),
        ],
        LEDGER: [
            "Verification bandwidth",
            "record-level capacity model",
            "contradiction-rate",
        ],
        VALIDATE_BOOK: [
            "scripts/validate_verification_bandwidth_capacity_model.py",
            "docs/verification_bandwidth_capacity_model.md",
            "experiments/verification_bandwidth_capacity/results/2026-07-03-local.json",
            'run_validator("validate_verification_bandwidth_capacity_model.py")',
        ],
    }
    for path, phrases in required.items():
        if not path.exists():
            errors.append(f"Missing required verification capacity surface {rel(path)}.")
            continue
        lowered = re.sub(r"\s+", " ", path.read_text(encoding="utf-8", errors="ignore")).lower()
        for phrase in phrases:
            if re.sub(r"\s+", " ", phrase).lower() not in lowered:
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

    if valid_count != 3:
        errors.append("Expected exactly three valid capacity-model traces.")
    if invalid_count != 5:
        errors.append("Expected exactly five expected-invalid controls.")

    expected = build_expected_result(valid_count, invalid_count)
    validate_result(expected, args.write_result, errors)
    validate_lean(errors)
    validate_surfaces(errors)

    if errors:
        fail(errors)
    print("Verification bandwidth capacity-model validation passed.")


if __name__ == "__main__":
    main()
