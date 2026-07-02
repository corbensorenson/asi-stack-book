#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from validate_capability_replacement import SCHEMA, semantic_errors
from validate_protocol_examples import validate_value


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "experiments" / "capability_replacement_trace" / "results" / "2026-07-02-local.json"
DOC = ROOT / "docs" / "capability_replacement_trace_probe.md"
CHAPTER = ROOT / "chapters" / "capability-replacement-and-rollback.qmd"
READER = (
    ROOT
    / "editions"
    / "reader_manuscript"
    / "v1_0"
    / "chapters"
    / "capability-replacement-and-rollback.qmd"
)
OUTLINE = ROOT / "docs" / "book_outline.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
CHANGELOG = ROOT / "appendices" / "F_changelog.qmd"
MANIFEST = ROOT / "book_structure.json"
VALIDATE_BOOK = ROOT / "scripts" / "validate_book.py"
LEAN_FILE = ROOT / "lean" / "AsiStackProofs" / "Replacement.lean"

COMMAND = "python3 scripts/validate_capability_replacement_trace_probe.py"
PROOF_TAG = "lean:replacement.transaction.trace_probe_bridge"
CODEX_TEST_NAME = "Capability replacement trace probe"
REQUIRED_THEOREMS = [
    "replacement_trace_probe_fixture_valid",
    "replacement_trace_probe_rejects_authority_widening",
    "replacement_trace_probe_preserves_no_promotion_boundary",
]
REQUIRED_NON_CLAIMS = [
    "does not execute deployed or runtime replacement behavior",
    "does not prove regression-suite quality or monitor quality",
    "does not execute production rollback",
    "does not promote the Capability Replacement chapter core claim",
    "does not create a support-state transition",
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Capability replacement trace probe validation failed:")
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


def canary_transaction() -> dict[str, Any]:
    return {
        "transaction_id": "replacement://trace-probe-router-canary-2026-07-02",
        "transaction_state": "canary",
        "field_id": "field://bounded-router-capability",
        "prior_implementation": "impl://bounded-router-v0-stable",
        "candidate_implementation": "impl://bounded-router-v1-canary",
        "identity_preservation": "same field identity and unchanged external authority envelope",
        "precheck_results": [
            "data validation passed for synthetic trace inputs",
            "schema validation passed for replacement transaction record",
            "model identity check not applicable; route policy artifact hash recorded",
            "serving integration not run; canary scope is fixture-only",
        ],
        "qualification_evidence": [
            "evidence://trace-probe-shadow-run",
            "evidence://baseline regression floor preserved in synthetic trace",
        ],
        "regression_results": [
            "baseline regression floor preserved for permission, logging, context, human review, and export/fork obligations",
        ],
        "authority_check": "candidate remains within same authority boundary and does not expand route permissions",
        "evaluator_independence": "separate fixture validator reviews candidate evidence; candidate does not self-attest",
        "residual_escrow": [
            "residual: no real regression suite, deployed route, or production monitor exists",
            "residual: default promotion blocked until live monitor and rollback evidence exist",
        ],
        "rollback_plan": "restore impl://bounded-router-v0-stable through fixture rollback handle",
        "rollback_receipt": {
            "prior_artifact": "impl://bounded-router-v0-stable",
            "state_migration_status": "reversible fixture state only",
            "reversible_fields": ["route_table", "permission_envelope", "audit_policy"],
            "irreversible_effects": [],
            "dry_run_status": "pass",
            "trigger_conditions": ["monitor regression", "authority widening", "schema drift"],
            "owner": "reviewer://replacement-trace-fixture",
        },
        "approval_record": "human-review-required-before-default",
        "canary_scope": "synthetic canary over replacement trace fixture only",
        "monitor_window": "synthetic six-step trace monitor",
        "monitor_status": "active",
        "decision": "canary",
        "promotion_blockers": [
            "default promotion blocked until monitor pass and independent review",
            "chapter support-state remains unchanged",
        ],
        "source_refs": [
            "docs/capability_replacement_trace_probe.md",
            "experiments/capability_replacement_trace/results/2026-07-02-local.json",
        ],
        "support_state_effect": "eligible_for_canary_review",
        "non_claims": REQUIRED_NON_CLAIMS,
    }


def rollback_transaction() -> dict[str, Any]:
    return {
        "transaction_id": "replacement://trace-probe-router-rollback-2026-07-02",
        "transaction_state": "rolled_back",
        "field_id": "field://bounded-router-capability",
        "prior_implementation": "impl://bounded-router-v0-stable",
        "candidate_implementation": "impl://bounded-router-v1-canary",
        "identity_preservation": "same field identity restored after monitor trigger",
        "precheck_results": [
            "data validation passed for synthetic trace inputs",
            "schema validation passed for rollback transaction record",
            "serving integration not run; rollback is fixture-only",
            "monitor trigger coverage recorded for regression event",
        ],
        "qualification_evidence": [
            "evidence://trace-probe-monitor-trigger",
            "evidence://rollback-handle-dry-run-pass",
        ],
        "regression_results": [
            "baseline regression floor failure detected in synthetic monitor; candidate blocked from default",
        ],
        "authority_check": "rollback restores same authority boundary and does not expand route permissions",
        "evaluator_independence": "separate fixture validator reviews rollback trigger and receipt",
        "residual_escrow": [
            "residual: monitor quality and deployed rollback behavior remain untested",
            "residual: support-state effect remains none for chapter core claim",
        ],
        "rollback_plan": "rollback restores impl://bounded-router-v0-stable after monitor trigger",
        "rollback_receipt": {
            "prior_artifact": "impl://bounded-router-v0-stable",
            "state_migration_status": "reversible fixture state restored",
            "reversible_fields": ["route_table", "permission_envelope", "audit_policy"],
            "irreversible_effects": [],
            "dry_run_status": "pass",
            "trigger_conditions": ["monitor regression", "baseline floor failure"],
            "owner": "reviewer://replacement-trace-fixture",
        },
        "approval_record": "rollback://fixture-monitor-trigger",
        "canary_scope": "synthetic canary over replacement trace fixture only",
        "monitor_window": "synthetic six-step trace monitor",
        "monitor_status": "fail",
        "decision": "rollback",
        "promotion_blockers": [
            "monitor trigger requires rollback",
            "candidate cannot become default in this trace",
        ],
        "source_refs": [
            "docs/capability_replacement_trace_probe.md",
            "experiments/capability_replacement_trace/results/2026-07-02-local.json",
        ],
        "support_state_effect": "blocks_promotion",
        "non_claims": REQUIRED_NON_CLAIMS,
    }


def control_is_rejected(control: dict[str, Any]) -> bool:
    return not (
        control["authority_within_field"]
        and control["regression_floor_preserved"]
        and control["rollback_dry_run_passed"]
        and control["residual_owner_present"]
    )


def build_expected_result() -> dict[str, Any]:
    transactions = [canary_transaction(), rollback_transaction()]
    negative_controls = [
        {
            "control_id": "replacement-control://authority-widening",
            "authority_within_field": False,
            "regression_floor_preserved": True,
            "rollback_dry_run_passed": True,
            "residual_owner_present": True,
        },
        {
            "control_id": "replacement-control://failed-regression",
            "authority_within_field": True,
            "regression_floor_preserved": False,
            "rollback_dry_run_passed": True,
            "residual_owner_present": True,
        },
        {
            "control_id": "replacement-control://missing-rollback",
            "authority_within_field": True,
            "regression_floor_preserved": True,
            "rollback_dry_run_passed": False,
            "residual_owner_present": True,
        },
    ]
    return {
        "schema_version": "asi_stack.capability_replacement_trace_probe.v0",
        "result_id": "2026-07-02-capability-replacement-trace-probe",
        "recorded_date": "2026-07-02",
        "command": COMMAND,
        "result_kind": "deterministic_synthetic_replacement_trace",
        "trace_step_count": 6,
        "trace_steps": [
            "proposal",
            "shadow_run",
            "canary_with_regression_floor",
            "monitor_trigger",
            "rollback_dry_run",
            "residual_and_no_promotion_record",
        ],
        "baseline_implementation": "impl://bounded-router-v0-stable",
        "candidate_implementation": "impl://bounded-router-v1-canary",
        "valid_trace_transaction_count": len(transactions),
        "replacement_transactions": transactions,
        "negative_control_count": len(negative_controls),
        "negative_controls": [
            {**control, "rejected": control_is_rejected(control)}
            for control in negative_controls
        ],
        "trace_assertions": {
            "canary_kept_non_default": True,
            "monitor_trigger_routes_to_rollback": True,
            "rollback_dry_run_present": True,
            "residuals_recorded": True,
            "authority_widening_rejected": True,
            "failed_regression_rejected": True,
            "missing_rollback_rejected": True,
            "support_state_effect_none": True,
            "non_claim_boundary": True,
        },
        "lean_fixture_alignment": {
            "module": "AsiStackProofs.Replacement",
            "proof_tag": PROOF_TAG,
            "theorem_refs": REQUIRED_THEOREMS,
            "expected": {
                "step_count": 6,
                "trace_transaction_count": 2,
                "negative_control_count": 3,
                "canary_kept_non_default": True,
                "monitor_trigger_rollback_present": True,
                "rollback_dry_run_present": True,
                "authority_widening_rejected": True,
                "failed_regression_rejected": True,
                "missing_rollback_rejected": True,
                "residuals_recorded": True,
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


def validate_transactions(result: dict[str, Any], errors: list[str]) -> None:
    schema = load_json(SCHEMA)
    transactions = result.get("replacement_transactions", [])
    if not isinstance(transactions, list) or len(transactions) != 2:
        errors.append(f"{rel(RESULT)}: replacement_transactions must contain two records.")
        return
    for index, record in enumerate(transactions):
        if not isinstance(record, dict):
            errors.append(f"{rel(RESULT)}: replacement_transactions[{index}] must be an object.")
            continue
        owner = f"replacement_transactions[{index}]"
        errors.extend(validate_value(record, schema, owner))
        errors.extend(semantic_errors(record, owner))


def validate_result(expected: dict[str, Any], write_result: bool, errors: list[str]) -> None:
    serialized = json.dumps(expected, indent=2) + "\n"
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
    validate_transactions(value, errors)
    non_claim_text = text_blob(value.get("non_claims", []))
    for phrase in REQUIRED_NON_CLAIMS:
        if phrase.lower() not in non_claim_text:
            errors.append(f"{rel(RESULT)} non_claims missing {phrase!r}.")


def validate_manifest(errors: list[str]) -> None:
    value = load_json(MANIFEST)
    chapter = None
    for part in value.get("parts", []):
        for candidate in part.get("chapters", []):
            if candidate.get("id") == "capability-replacement-and-rollback":
                chapter = candidate
                break
    if chapter is None:
        errors.append("book_structure.json: missing capability replacement chapter.")
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
        "traceStepCount",
        "traceTransactionCount",
        "negativeControlCount",
        "canaryKeptNonDefault",
        "monitorTriggerRollbackPresent",
        "rollbackDryRunPresent",
        "supportStateEffectNone",
        "nonClaimBoundary",
    ):
        if field not in text:
            errors.append(f"{rel(LEAN_FILE)} missing fixture field {field}.")


def validate_surfaces(errors: list[str]) -> None:
    required = {
        DOC: [
            "Capability replacement trace probe",
            rel(RESULT),
            "two valid synthetic replacement transactions",
            "three expected-invalid controls",
            "no support-state transition",
        ],
        CHAPTER: [
            "Capability replacement trace probe",
            rel(RESULT),
            "no deployed replacement execution",
        ],
        READER: [
            "capability replacement trace probe",
            "not a deployed replacement",
            "not a support-state transition",
        ],
        OUTLINE: [CODEX_TEST_NAME, PROOF_TAG, rel(RESULT)],
        ROADMAP: [
            "Capability replacement trace probe",
            "deterministic replacement trace",
            "no support-state promotion",
        ],
        CHANGELOG: ["Capability replacement trace probe", rel(RESULT)],
        VALIDATE_BOOK: [
            "scripts/validate_capability_replacement_trace_probe.py",
            "docs/capability_replacement_trace_probe.md",
            "experiments/capability_replacement_trace/results/2026-07-02-local.json",
            'run_validator("validate_capability_replacement_trace_probe.py")',
        ],
    }
    for path, phrases in required.items():
        if not path.exists():
            errors.append(f"Missing required capability replacement trace surface {rel(path)}.")
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
    validate_transactions(expected, errors)
    controls = expected["negative_controls"]
    if not all(control.get("rejected") is True for control in controls):
        errors.append("All replacement trace negative controls must be rejected.")
    assertions = expected["trace_assertions"]
    for key in (
        "canary_kept_non_default",
        "monitor_trigger_routes_to_rollback",
        "rollback_dry_run_present",
        "residuals_recorded",
        "support_state_effect_none",
        "non_claim_boundary",
    ):
        if assertions.get(key) is not True:
            errors.append(f"trace_assertions.{key} must be true.")
    validate_result(expected, args.write_result, errors)
    validate_manifest(errors)
    validate_lean(errors)
    validate_surfaces(errors)
    if errors:
        fail(errors)
    print("Capability replacement trace probe validation passed.")


if __name__ == "__main__":
    main()
