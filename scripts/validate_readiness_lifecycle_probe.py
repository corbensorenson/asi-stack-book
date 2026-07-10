#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "experiments" / "readiness_lifecycle_probe" / "results" / "2026-07-02-local.json"
DOC = ROOT / "docs" / "readiness_lifecycle_probe.md"
CHAPTER = ROOT / "chapters" / "readiness-gates-residual-escrow-and-quarantine.qmd"
READER = (
    ROOT
    / "editions"
    / "reader_manuscript"
    / "v1_0"
    / "chapters"
    / "readiness-gates-residual-escrow-and-quarantine.qmd"
)
OUTLINE = ROOT / "docs" / "book_outline.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
CHANGELOG = ROOT / "appendices" / "F_changelog.qmd"
MANIFEST = ROOT / "book_structure.json"
VALIDATION_REGISTRY = ROOT / "validation" / "registry.json"
LEAN_FILE = ROOT / "lean" / "AsiStackProofs" / "ReadinessGates.lean"

COMMAND = "python3 scripts/validate_readiness_lifecycle_probe.py"
PROOF_TAG = "lean:readiness.gates.lifecycle_probe_bridge"
CODEX_TEST_NAME = "Readiness lifecycle probe"
REQUIRED_THEOREMS = [
    "readiness_lifecycle_transition_must_be_forward_or_terminal",
    "allowed_readiness_transition_requires_core_records",
    "default_readiness_requires_regression_authority_and_route",
    "default_readiness_without_regression_floor_rejected",
    "default_readiness_without_authority_scope_rejected",
    "quarantine_transition_blocks_ordinary_and_requires_fallback",
    "quarantined_lifecycle_transition_with_ordinary_route_rejected",
    "supersession_without_record_rejected",
    "retirement_without_receipt_rejected",
    "retired_readiness_state_cannot_transition",
    "readiness_lifecycle_probe_fixture_bridge",
]
REQUIRED_NON_CLAIMS = [
    "does not execute a deployed readiness engine",
    "does not prove residual-ledger storage",
    "does not prove live quarantine routing",
    "does not prove benchmark quality",
    "does not prove MoECOT replay",
    "does not promote the chapter support state",
]

FORWARD_OR_TERMINAL_TRANSITIONS = {
    ("candidate", "shadow"),
    ("shadow", "canary"),
    ("canary", "qualified"),
    ("qualified", "default_ready"),
}
TERMINAL_TO_STATES = {"quarantined", "superseded", "retired"}
ALLOWED_STATES = {
    "candidate",
    "shadow",
    "canary",
    "qualified",
    "default_ready",
    "quarantined",
    "retired",
    "superseded",
}


def transition_record(**overrides: Any) -> dict[str, Any]:
    record: dict[str, Any] = {
        "transition_id": "transition://readiness/base",
        "expect_valid": True,
        "target_id": "module://bounded-specialist",
        "field_id": "field://public-transform",
        "from_state": "candidate",
        "to_state": "shadow",
        "gate_evidence_fresh": True,
        "residual_escrow_carried": True,
        "fallback_path_present": True,
        "expiry_recorded": True,
        "regression_floor_preserved": True,
        "authority_scope_preserved": True,
        "ordinary_route_allowed": False,
        "diagnostic_route_allowed": True,
        "supersession_record_present": False,
        "retirement_receipt_present": False,
        "evidence_refs": ["evidence://fresh-gate", "regression://floor-pass"],
        "residual_refs": ["residual://known-tail"],
        "fallback_route": "route://safe-baseline",
        "expiry_ref": "expiry://2026-07-09",
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    }
    record.update(overrides)
    return record


TRANSITIONS: list[dict[str, Any]] = [
    transition_record(
        transition_id="valid_candidate_to_shadow_evidence_ready",
        from_state="candidate",
        to_state="shadow",
    ),
    transition_record(
        transition_id="valid_shadow_to_canary_with_residual_escrow",
        from_state="shadow",
        to_state="canary",
    ),
    transition_record(
        transition_id="valid_qualified_to_default_ready",
        from_state="qualified",
        to_state="default_ready",
        ordinary_route_allowed=True,
        diagnostic_route_allowed=True,
    ),
    transition_record(
        transition_id="valid_quarantine_failed_floor_with_fallback",
        from_state="canary",
        to_state="quarantined",
        ordinary_route_allowed=False,
        diagnostic_route_allowed=True,
        fallback_path_present=True,
        evidence_refs=["evidence://failed-floor"],
    ),
    transition_record(
        transition_id="valid_supersession_carries_residual",
        from_state="qualified",
        to_state="superseded",
        supersession_record_present=True,
        ordinary_route_allowed=False,
    ),
    transition_record(
        transition_id="valid_retirement_receipt_with_residual",
        from_state="superseded",
        to_state="retired",
        retirement_receipt_present=True,
        ordinary_route_allowed=False,
    ),
    transition_record(
        transition_id="invalid_non_forward_jump_shadow_to_default",
        expect_valid=False,
        from_state="shadow",
        to_state="default_ready",
        ordinary_route_allowed=True,
    ),
    transition_record(
        transition_id="invalid_missing_fresh_gate_evidence",
        expect_valid=False,
        gate_evidence_fresh=False,
    ),
    transition_record(
        transition_id="invalid_missing_residual_escrow",
        expect_valid=False,
        residual_escrow_carried=False,
        residual_refs=[],
    ),
    transition_record(
        transition_id="invalid_default_without_regression_floor",
        expect_valid=False,
        from_state="qualified",
        to_state="default_ready",
        regression_floor_preserved=False,
        ordinary_route_allowed=True,
    ),
    transition_record(
        transition_id="invalid_default_without_authority_scope",
        expect_valid=False,
        from_state="qualified",
        to_state="default_ready",
        authority_scope_preserved=False,
        ordinary_route_allowed=True,
    ),
    transition_record(
        transition_id="invalid_quarantine_ordinary_route_allowed",
        expect_valid=False,
        from_state="canary",
        to_state="quarantined",
        ordinary_route_allowed=True,
        diagnostic_route_allowed=True,
    ),
    transition_record(
        transition_id="invalid_quarantine_without_diagnostic_fallback",
        expect_valid=False,
        from_state="canary",
        to_state="quarantined",
        ordinary_route_allowed=False,
        diagnostic_route_allowed=True,
        fallback_path_present=False,
    ),
    transition_record(
        transition_id="invalid_supersession_without_record",
        expect_valid=False,
        from_state="qualified",
        to_state="superseded",
        supersession_record_present=False,
    ),
    transition_record(
        transition_id="invalid_retirement_without_receipt",
        expect_valid=False,
        from_state="superseded",
        to_state="retired",
        retirement_receipt_present=False,
    ),
    transition_record(
        transition_id="invalid_transition_from_retired",
        expect_valid=False,
        from_state="retired",
        to_state="shadow",
    ),
    transition_record(
        transition_id="invalid_missing_non_claim_boundary",
        expect_valid=False,
        non_claims=[],
    ),
    transition_record(
        transition_id="invalid_support_state_promotion",
        expect_valid=False,
        support_state_effect="promote_chapter_core",
    ),
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Readiness lifecycle probe validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def text_blob(value: Any) -> str:
    if isinstance(value, dict):
        return "\n".join(f"{key}: {text_blob(child)}" for key, child in value.items()).lower()
    if isinstance(value, list):
        return "\n".join(text_blob(item) for item in value).lower()
    return str(value).lower()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def is_forward_or_terminal(record: dict[str, Any]) -> bool:
    pair = (record["from_state"], record["to_state"])
    return pair in FORWARD_OR_TERMINAL_TRANSITIONS or record["to_state"] in TERMINAL_TO_STATES


def transition_errors(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    transition_id = str(record.get("transition_id", "<missing>"))
    for field in ("target_id", "field_id", "fallback_route", "expiry_ref"):
        if not isinstance(record.get(field), str) or not record[field].strip():
            errors.append(f"{transition_id}: {field} must be a non-empty string.")
    for field in ("from_state", "to_state"):
        if record.get(field) not in ALLOWED_STATES:
            errors.append(f"{transition_id}: {field} {record.get(field)!r} is not an allowed readiness state.")
    for field in (
        "gate_evidence_fresh",
        "residual_escrow_carried",
        "fallback_path_present",
        "expiry_recorded",
        "regression_floor_preserved",
        "authority_scope_preserved",
        "ordinary_route_allowed",
        "diagnostic_route_allowed",
        "supersession_record_present",
        "retirement_receipt_present",
    ):
        if not isinstance(record.get(field), bool):
            errors.append(f"{transition_id}: {field} must be boolean.")

    if record.get("from_state") == "retired":
        errors.append(f"{transition_id}: retired readiness states cannot transition.")
    if not is_forward_or_terminal(record):
        errors.append(f"{transition_id}: transition is not a forward step or terminal route.")
    for field in ("gate_evidence_fresh", "residual_escrow_carried", "fallback_path_present", "expiry_recorded"):
        if record.get(field) is not True:
            errors.append(f"{transition_id}: {field} is required for allowed lifecycle transitions.")
    if record.get("to_state") == "qualified" and record.get("regression_floor_preserved") is not True:
        errors.append(f"{transition_id}: qualified transitions require regression_floor_preserved.")
    if record.get("to_state") == "default_ready":
        if record.get("regression_floor_preserved") is not True:
            errors.append(f"{transition_id}: default_ready transitions require regression_floor_preserved.")
        if record.get("authority_scope_preserved") is not True:
            errors.append(f"{transition_id}: default_ready transitions require authority_scope_preserved.")
        if record.get("ordinary_route_allowed") is not True:
            errors.append(f"{transition_id}: default_ready transitions require an ordinary route.")
    if record.get("to_state") == "quarantined":
        if record.get("ordinary_route_allowed") is not False:
            errors.append(f"{transition_id}: quarantined transitions must block ordinary routing.")
        if record.get("diagnostic_route_allowed") is not True:
            errors.append(f"{transition_id}: quarantined transitions should preserve diagnostic routing.")
        if record.get("fallback_path_present") is not True:
            errors.append(f"{transition_id}: quarantined transitions require fallback_path_present.")
    if record.get("to_state") == "superseded" and record.get("supersession_record_present") is not True:
        errors.append(f"{transition_id}: superseded transitions require a supersession record.")
    if record.get("to_state") == "retired" and record.get("retirement_receipt_present") is not True:
        errors.append(f"{transition_id}: retired transitions require a retirement receipt.")
    if record.get("residual_escrow_carried") is True:
        if not isinstance(record.get("residual_refs"), list) or not record["residual_refs"]:
            errors.append(f"{transition_id}: carried residual escrow requires residual_refs.")
    if record.get("gate_evidence_fresh") is True:
        if not isinstance(record.get("evidence_refs"), list) or not record["evidence_refs"]:
            errors.append(f"{transition_id}: fresh gate evidence requires evidence_refs.")
    if record.get("support_state_effect") != "none":
        errors.append(f"{transition_id}: support_state_effect must remain none.")

    non_claim_text = text_blob(record.get("non_claims", []))
    for phrase in REQUIRED_NON_CLAIMS:
        if phrase.lower() not in non_claim_text:
            errors.append(f"{transition_id}: non_claims missing {phrase!r}.")
    return errors


def build_expected_result(valid_count: int, invalid_count: int) -> dict[str, Any]:
    return {
        "schema_version": "asi_stack.readiness_lifecycle_probe.v0",
        "result_id": "2026-07-02-readiness-lifecycle-probe",
        "recorded_date": "2026-07-02",
        "command": COMMAND,
        "result_kind": "deterministic_synthetic_readiness_lifecycle_probe",
        "valid_transition_count": valid_count,
        "expected_invalid_control_count": invalid_count,
        "transition_count": len(TRANSITIONS),
        "negative_controls": {
            "non_forward_jump_rejected": True,
            "missing_fresh_gate_evidence_rejected": True,
            "missing_residual_escrow_rejected": True,
            "default_missing_regression_rejected": True,
            "default_missing_authority_rejected": True,
            "quarantine_ordinary_route_rejected": True,
            "quarantine_missing_fallback_rejected": True,
            "supersession_missing_record_rejected": True,
            "retirement_missing_receipt_rejected": True,
            "transition_from_retired_rejected": True,
            "missing_non_claim_boundary_rejected": True,
            "support_state_promotion_rejected": True,
        },
        "transition_coverage": {
            "candidate_to_shadow": True,
            "shadow_to_canary": True,
            "qualified_to_default_ready": True,
            "quarantine_with_fallback": True,
            "supersession_with_residual": True,
            "retirement_with_receipt": True,
            "ordinary_route_blocked_in_quarantine": True,
            "support_state_no_promotion": True,
        },
        "lean_fixture_alignment": {
            "module": "AsiStackProofs.ReadinessGates",
            "proof_tag": PROOF_TAG,
            "theorem_refs": REQUIRED_THEOREMS,
            "expected": {
                "candidateToShadowAccepted": True,
                "shadowToCanaryAccepted": True,
                "defaultReadyAccepted": True,
                "quarantineWithFallbackAccepted": True,
                "supersessionWithResidualAccepted": True,
                "retirementWithReceiptAccepted": True,
                "negativeControlsRejected": True,
                "supportStateEffectNone": True,
                "nonClaimBoundary": True,
            },
        },
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
        "verification_result": "pass",
        "residuals": [
            "Synthetic readiness lifecycle fixture only; no readiness engine, router, residual ledger, benchmark harness, rollback executor, runtime monitor, MoECOT replay path, or deployed module was executed.",
            "The Readiness Gates chapter core claim remains at argument support.",
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


def validate_manifest(errors: list[str]) -> None:
    value = load_json(MANIFEST)
    chapter = None
    for part in value.get("parts", []):
        for candidate in part.get("chapters", []):
            if candidate.get("id") == "readiness-gates-residual-escrow-and-quarantine":
                chapter = candidate
                break
    if chapter is None:
        errors.append("book_structure.json: missing Readiness Gates chapter.")
        return
    if CODEX_TEST_NAME.lower() not in text_blob(chapter.get("codex_tests", [])):
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
        "candidateToShadowAccepted",
        "shadowToCanaryAccepted",
        "defaultReadyAccepted",
        "quarantineWithFallbackAccepted",
        "supersessionWithResidualAccepted",
        "retirementWithReceiptAccepted",
        "negativeControlsRejected",
        "supportStateEffectNone",
        "nonClaimBoundary",
    ):
        if field not in text:
            errors.append(f"{rel(LEAN_FILE)} missing fixture field {field}.")


def validate_surfaces(errors: list[str]) -> None:
    required = {
        DOC: [
            "Readiness Lifecycle Probe",
            rel(RESULT),
            "six valid synthetic readiness lifecycle transitions",
            "twelve expected-invalid controls",
            "no support-state transition",
        ],
        CHAPTER: [
            "Readiness lifecycle probe",
            rel(RESULT),
            "six valid synthetic readiness lifecycle transitions",
            "twelve expected-invalid controls",
        ],
        READER: [
            "readiness lifecycle probe",
            "six synthetic lifecycle transitions",
            "not a deployed readiness engine",
        ],
        OUTLINE: [CODEX_TEST_NAME, PROOF_TAG, rel(RESULT)],
        ROADMAP: [
            "Readiness lifecycle probe",
            "deterministic synthetic readiness lifecycle fixture",
            "no support-state promotion",
        ],
        CHANGELOG: ["Readiness lifecycle probe", rel(RESULT)],
        VALIDATION_REGISTRY: [
            "scripts/validate_readiness_lifecycle_probe.py",
            "docs/readiness_lifecycle_probe.md",
            "experiments/readiness_lifecycle_probe/results/2026-07-02-local.json",
            '"script": "validate_readiness_lifecycle_probe.py"',
        ],
    }
    for path, phrases in required.items():
        if not path.exists():
            errors.append(f"Missing required readiness lifecycle surface {rel(path)}.")
            continue
        text = path.read_text(encoding="utf-8", errors="ignore").lower()
        for phrase in phrases:
            if phrase.lower() not in text:
                errors.append(f"{rel(path)} missing required phrase {phrase!r}.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-result", action="store_true")
    args = parser.parse_args()

    errors: list[str] = []
    valid_count = 0
    invalid_count = 0
    for record in TRANSITIONS:
        expect_valid = bool(record.get("expect_valid"))
        current_errors = transition_errors(record)
        if expect_valid:
            valid_count += 1
            errors.extend(current_errors)
        else:
            invalid_count += 1
            if not current_errors:
                errors.append(f"{record.get('transition_id', '<missing>')}: expected-invalid control unexpectedly passed.")

    if valid_count != 6:
        errors.append("Expected exactly six valid synthetic readiness lifecycle transitions.")
    if invalid_count != 12:
        errors.append("Expected exactly twelve expected-invalid controls.")

    expected = build_expected_result(valid_count, invalid_count)
    validate_result(expected, args.write_result, errors)
    validate_manifest(errors)
    validate_lean(errors)
    validate_surfaces(errors)

    if errors:
        fail(errors)
    print("Readiness lifecycle probe validation passed.")


if __name__ == "__main__":
    main()
