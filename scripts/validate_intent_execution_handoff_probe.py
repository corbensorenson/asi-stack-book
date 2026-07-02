#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "experiments" / "intent_execution_handoff" / "results" / "2026-07-02-local.json"
DOC = ROOT / "docs" / "intent_execution_handoff_probe.md"
CHAPTER = ROOT / "chapters" / "intent-to-execution-contracts.qmd"
READER = (
    ROOT
    / "editions"
    / "reader_manuscript"
    / "v1_0"
    / "chapters"
    / "intent-to-execution-contracts.qmd"
)
OUTLINE = ROOT / "docs" / "book_outline.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
CHANGELOG = ROOT / "appendices" / "F_changelog.qmd"
MANIFEST = ROOT / "book_structure.json"
VALIDATE_BOOK = ROOT / "scripts" / "validate_book.py"
LEAN_FILE = ROOT / "lean" / "AsiStackProofs" / "IntentToExecution.lean"

COMMAND = "python3 scripts/validate_intent_execution_handoff_probe.py"
PROOF_TAG = "lean:intent_execution.handoff_trace.probe_fixture_bridge"
CODEX_TEST_NAME = "Intent-to-execution handoff probe"
REQUIRED_THEOREMS = [
    "intent_execution_handoff_probe_fixture_bridge",
]
REQUIRED_NON_CLAIMS = [
    "does not parse natural-language intent",
    "does not execute a deployed dispatcher or runtime adapter",
    "does not prove approval-service enforcement",
    "does not prove artifact satisfaction",
    "does not promote the chapter support state",
    "does not create a support-state transition",
]

ACTIVE_DISPATCH_STATES = {"dispatch_ready", "running", "delivered", "verified"}
BLOCK_STATES = {"blocked_missing_approval", "blocked_missing_authority", "blocked_residual", "blocked_recontract"}
ACCEPTED_HIDDEN_OVERRIDE_DISPOSITIONS = {"rejected", "quarantined", "ignored"}


TRACES: list[dict[str, Any]] = [
    {
        "trace_id": "valid_contract_to_artifact_handoff",
        "expect_valid": True,
        "intent_contract_ref": "intent://public-book-maintenance-request",
        "command_contract_ref": "command://intent-execution-handoff-probe-001",
        "plan_graph_ref": "plan://intent-execution-handoff-probe-001",
        "typed_job_ref": "job://intent-execution-handoff-probe-001",
        "parent_authority_ceiling": "public_book_edit_only",
        "job_authority_ceiling": "public_book_edit_only",
        "authority_within_parent": True,
        "command_validation_state": "validated_for_planning",
        "dispatch_state": "verified",
        "required_approval": False,
        "approval_present": True,
        "approval_receipt_ref": "approval://not-required-public-safe-draft",
        "hidden_override_detected": False,
        "hidden_override_disposition": "ignored",
        "context_override_applied": False,
        "handoff_receipt_refs": [
            "handoff://intent-to-command-001",
            "handoff://command-to-plan-001",
            "handoff://plan-to-job-001",
        ],
        "dispatch_receipt_ref": "dispatch://plan-to-job-001",
        "runtime_adapter_receipt_ref": "adapter://synthetic-local-dry-run-001",
        "side_effects": [
            {
                "effect_ref": "effect://synthetic-local-file-dry-run",
                "authorized": True,
                "adapter_receipt_ref": "adapter://synthetic-local-dry-run-001",
            }
        ],
        "artifact_refs": [
            "artifact://intent-execution-handoff-probe-result",
        ],
        "artifact_parent_links_present": True,
        "verification_refs": [
            "validator://validate_intent_execution_handoff_probe",
        ],
        "feedback_refs": [
            "feedback://intent-execution-handoff-probe-no-promotion",
        ],
        "residual_known": True,
        "residuals": [
            "No parser, real dispatcher, approval service, deployed runtime, or artifact acceptance path was exercised.",
        ],
        "residuals_preserved": True,
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "valid_missing_approval_blocks_dispatch",
        "expect_valid": True,
        "intent_contract_ref": "intent://approval-required-tool-request",
        "command_contract_ref": "command://intent-execution-approval-block-001",
        "plan_graph_ref": "plan://intent-execution-approval-block-001",
        "typed_job_ref": "job://intent-execution-approval-block-001",
        "parent_authority_ceiling": "human_approval_required_before_tool_effect",
        "job_authority_ceiling": "human_approval_required_before_tool_effect",
        "authority_within_parent": True,
        "command_validation_state": "dispatch_blocked",
        "dispatch_state": "blocked_missing_approval",
        "required_approval": True,
        "approval_present": False,
        "approval_receipt_ref": "",
        "hidden_override_detected": False,
        "hidden_override_disposition": "ignored",
        "context_override_applied": False,
        "handoff_receipt_refs": [
            "handoff://intent-to-command-approval-block",
            "handoff://command-to-plan-approval-block",
        ],
        "dispatch_receipt_ref": "",
        "block_receipt_ref": "block://approval-required-before-dispatch-001",
        "runtime_adapter_receipt_ref": "",
        "side_effects": [],
        "artifact_refs": [],
        "artifact_parent_links_present": True,
        "verification_refs": [
            "validator://approval-block-record-shape",
        ],
        "feedback_refs": [
            "feedback://approval-block-residual",
        ],
        "residual_known": True,
        "residuals": [
            "Human approval is required before any runtime adapter or tool effect can run.",
        ],
        "residuals_preserved": True,
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "invalid_dispatch_without_approval",
        "expect_valid": False,
        "intent_contract_ref": "intent://approval-required-tool-request",
        "command_contract_ref": "command://invalid-approval-bypass",
        "plan_graph_ref": "plan://invalid-approval-bypass",
        "typed_job_ref": "job://invalid-approval-bypass",
        "parent_authority_ceiling": "human_approval_required_before_tool_effect",
        "job_authority_ceiling": "human_approval_required_before_tool_effect",
        "authority_within_parent": True,
        "command_validation_state": "validated_for_planning",
        "dispatch_state": "running",
        "required_approval": True,
        "approval_present": False,
        "approval_receipt_ref": "",
        "hidden_override_detected": False,
        "hidden_override_disposition": "ignored",
        "context_override_applied": False,
        "handoff_receipt_refs": ["handoff://invalid-approval-bypass"],
        "dispatch_receipt_ref": "dispatch://invalid-approval-bypass",
        "runtime_adapter_receipt_ref": "adapter://invalid-approval-bypass",
        "side_effects": [],
        "artifact_refs": ["artifact://invalid-approval-bypass"],
        "artifact_parent_links_present": True,
        "verification_refs": ["validator://invalid-approval-bypass"],
        "feedback_refs": ["feedback://invalid-approval-bypass"],
        "residual_known": True,
        "residuals": ["Approval was missing but dispatch ran."],
        "residuals_preserved": True,
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "invalid_authority_widening_job",
        "expect_valid": False,
        "intent_contract_ref": "intent://public-book-maintenance-request",
        "command_contract_ref": "command://invalid-authority-widening",
        "plan_graph_ref": "plan://invalid-authority-widening",
        "typed_job_ref": "job://invalid-authority-widening",
        "parent_authority_ceiling": "public_book_edit_only",
        "job_authority_ceiling": "external_publication_and_email",
        "authority_within_parent": False,
        "command_validation_state": "validated_for_planning",
        "dispatch_state": "dispatch_ready",
        "required_approval": False,
        "approval_present": True,
        "approval_receipt_ref": "approval://not-required-public-safe-draft",
        "hidden_override_detected": False,
        "hidden_override_disposition": "ignored",
        "context_override_applied": False,
        "handoff_receipt_refs": ["handoff://invalid-authority-widening"],
        "dispatch_receipt_ref": "dispatch://invalid-authority-widening",
        "runtime_adapter_receipt_ref": "",
        "side_effects": [],
        "artifact_refs": ["artifact://invalid-authority-widening"],
        "artifact_parent_links_present": True,
        "verification_refs": ["validator://invalid-authority-widening"],
        "feedback_refs": ["feedback://invalid-authority-widening"],
        "residual_known": False,
        "residuals": [],
        "residuals_preserved": True,
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "invalid_hidden_override_applied",
        "expect_valid": False,
        "intent_contract_ref": "intent://public-book-maintenance-request",
        "command_contract_ref": "command://invalid-hidden-override",
        "plan_graph_ref": "plan://invalid-hidden-override",
        "typed_job_ref": "job://invalid-hidden-override",
        "parent_authority_ceiling": "public_book_edit_only",
        "job_authority_ceiling": "public_book_edit_only",
        "authority_within_parent": True,
        "command_validation_state": "validated_for_planning",
        "dispatch_state": "running",
        "required_approval": False,
        "approval_present": True,
        "approval_receipt_ref": "approval://not-required-public-safe-draft",
        "hidden_override_detected": True,
        "hidden_override_disposition": "applied",
        "context_override_applied": True,
        "handoff_receipt_refs": ["handoff://invalid-hidden-override"],
        "dispatch_receipt_ref": "dispatch://invalid-hidden-override",
        "runtime_adapter_receipt_ref": "adapter://invalid-hidden-override",
        "side_effects": [],
        "artifact_refs": ["artifact://invalid-hidden-override"],
        "artifact_parent_links_present": True,
        "verification_refs": ["validator://invalid-hidden-override"],
        "feedback_refs": ["feedback://invalid-hidden-override"],
        "residual_known": True,
        "residuals": ["Hidden override was applied."],
        "residuals_preserved": True,
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "invalid_missing_dispatch_receipt",
        "expect_valid": False,
        "intent_contract_ref": "intent://public-book-maintenance-request",
        "command_contract_ref": "command://invalid-missing-dispatch-receipt",
        "plan_graph_ref": "plan://invalid-missing-dispatch-receipt",
        "typed_job_ref": "job://invalid-missing-dispatch-receipt",
        "parent_authority_ceiling": "public_book_edit_only",
        "job_authority_ceiling": "public_book_edit_only",
        "authority_within_parent": True,
        "command_validation_state": "validated_for_planning",
        "dispatch_state": "running",
        "required_approval": False,
        "approval_present": True,
        "approval_receipt_ref": "approval://not-required-public-safe-draft",
        "hidden_override_detected": False,
        "hidden_override_disposition": "ignored",
        "context_override_applied": False,
        "handoff_receipt_refs": ["handoff://invalid-missing-dispatch-receipt"],
        "dispatch_receipt_ref": "",
        "runtime_adapter_receipt_ref": "adapter://invalid-missing-dispatch-receipt",
        "side_effects": [],
        "artifact_refs": ["artifact://invalid-missing-dispatch-receipt"],
        "artifact_parent_links_present": True,
        "verification_refs": ["validator://invalid-missing-dispatch-receipt"],
        "feedback_refs": ["feedback://invalid-missing-dispatch-receipt"],
        "residual_known": False,
        "residuals": [],
        "residuals_preserved": True,
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "invalid_side_effect_without_adapter_receipt",
        "expect_valid": False,
        "intent_contract_ref": "intent://public-book-maintenance-request",
        "command_contract_ref": "command://invalid-side-effect-no-receipt",
        "plan_graph_ref": "plan://invalid-side-effect-no-receipt",
        "typed_job_ref": "job://invalid-side-effect-no-receipt",
        "parent_authority_ceiling": "public_book_edit_only",
        "job_authority_ceiling": "public_book_edit_only",
        "authority_within_parent": True,
        "command_validation_state": "validated_for_planning",
        "dispatch_state": "running",
        "required_approval": False,
        "approval_present": True,
        "approval_receipt_ref": "approval://not-required-public-safe-draft",
        "hidden_override_detected": False,
        "hidden_override_disposition": "ignored",
        "context_override_applied": False,
        "handoff_receipt_refs": ["handoff://invalid-side-effect-no-receipt"],
        "dispatch_receipt_ref": "dispatch://invalid-side-effect-no-receipt",
        "runtime_adapter_receipt_ref": "",
        "side_effects": [
            {
                "effect_ref": "effect://invalid-side-effect-no-receipt",
                "authorized": True,
                "adapter_receipt_ref": "",
            }
        ],
        "artifact_refs": ["artifact://invalid-side-effect-no-receipt"],
        "artifact_parent_links_present": True,
        "verification_refs": ["validator://invalid-side-effect-no-receipt"],
        "feedback_refs": ["feedback://invalid-side-effect-no-receipt"],
        "residual_known": False,
        "residuals": [],
        "residuals_preserved": True,
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "invalid_residual_erased",
        "expect_valid": False,
        "intent_contract_ref": "intent://public-book-maintenance-request",
        "command_contract_ref": "command://invalid-residual-erased",
        "plan_graph_ref": "plan://invalid-residual-erased",
        "typed_job_ref": "job://invalid-residual-erased",
        "parent_authority_ceiling": "public_book_edit_only",
        "job_authority_ceiling": "public_book_edit_only",
        "authority_within_parent": True,
        "command_validation_state": "validated_for_planning",
        "dispatch_state": "verified",
        "required_approval": False,
        "approval_present": True,
        "approval_receipt_ref": "approval://not-required-public-safe-draft",
        "hidden_override_detected": False,
        "hidden_override_disposition": "ignored",
        "context_override_applied": False,
        "handoff_receipt_refs": ["handoff://invalid-residual-erased"],
        "dispatch_receipt_ref": "dispatch://invalid-residual-erased",
        "runtime_adapter_receipt_ref": "adapter://invalid-residual-erased",
        "side_effects": [],
        "artifact_refs": ["artifact://invalid-residual-erased"],
        "artifact_parent_links_present": True,
        "verification_refs": ["validator://invalid-residual-erased"],
        "feedback_refs": ["feedback://invalid-residual-erased"],
        "residual_known": True,
        "residuals": [],
        "residuals_preserved": False,
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "invalid_artifact_parent_link_missing",
        "expect_valid": False,
        "intent_contract_ref": "intent://public-book-maintenance-request",
        "command_contract_ref": "command://invalid-artifact-link",
        "plan_graph_ref": "plan://invalid-artifact-link",
        "typed_job_ref": "job://invalid-artifact-link",
        "parent_authority_ceiling": "public_book_edit_only",
        "job_authority_ceiling": "public_book_edit_only",
        "authority_within_parent": True,
        "command_validation_state": "validated_for_planning",
        "dispatch_state": "verified",
        "required_approval": False,
        "approval_present": True,
        "approval_receipt_ref": "approval://not-required-public-safe-draft",
        "hidden_override_detected": False,
        "hidden_override_disposition": "ignored",
        "context_override_applied": False,
        "handoff_receipt_refs": ["handoff://invalid-artifact-link"],
        "dispatch_receipt_ref": "dispatch://invalid-artifact-link",
        "runtime_adapter_receipt_ref": "adapter://invalid-artifact-link",
        "side_effects": [],
        "artifact_refs": ["artifact://invalid-artifact-link"],
        "artifact_parent_links_present": False,
        "verification_refs": ["validator://invalid-artifact-link"],
        "feedback_refs": ["feedback://invalid-artifact-link"],
        "residual_known": False,
        "residuals": [],
        "residuals_preserved": True,
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Intent-to-execution handoff probe validation failed:")
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


def nonempty_string(trace: dict[str, Any], field: str, errors: list[str]) -> None:
    trace_id = str(trace.get("trace_id", "<missing>"))
    value = trace.get(field)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{trace_id}: {field} must be a non-empty string.")


def nonempty_list(trace: dict[str, Any], field: str, errors: list[str]) -> list[Any]:
    trace_id = str(trace.get("trace_id", "<missing>"))
    value = trace.get(field)
    if not isinstance(value, list) or not value:
        errors.append(f"{trace_id}: {field} must be a non-empty list.")
        return []
    return value


def trace_errors(trace: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    trace_id = str(trace.get("trace_id", "<missing>"))
    dispatch_state = str(trace.get("dispatch_state", ""))
    active_dispatch = dispatch_state in ACTIVE_DISPATCH_STATES
    blocked_dispatch = dispatch_state in BLOCK_STATES

    for field in (
        "intent_contract_ref",
        "command_contract_ref",
        "plan_graph_ref",
        "typed_job_ref",
        "parent_authority_ceiling",
        "job_authority_ceiling",
        "command_validation_state",
        "dispatch_state",
    ):
        nonempty_string(trace, field, errors)

    handoff_receipts = nonempty_list(trace, "handoff_receipt_refs", errors)
    if any(not isinstance(item, str) or not item.startswith("handoff://") for item in handoff_receipts):
        errors.append(f"{trace_id}: handoff_receipt_refs must use handoff:// refs.")

    if trace.get("support_state_effect") != "none":
        errors.append(f"{trace_id}: support_state_effect must be none.")

    if trace.get("authority_within_parent") is not True:
        errors.append(f"{trace_id}: job authority must stay within the parent contract ceiling.")
    if trace.get("job_authority_ceiling") != trace.get("parent_authority_ceiling"):
        errors.append(f"{trace_id}: job_authority_ceiling must preserve the parent_authority_ceiling.")

    required_approval = trace.get("required_approval") is True
    approval_present = trace.get("approval_present") is True
    if required_approval and not approval_present and active_dispatch:
        errors.append(f"{trace_id}: active dispatch requires the required approval receipt.")
    if required_approval and approval_present:
        nonempty_string(trace, "approval_receipt_ref", errors)
    if required_approval and not approval_present and blocked_dispatch:
        nonempty_string(trace, "block_receipt_ref", errors)
    if required_approval and not approval_present and trace.get("side_effects"):
        errors.append(f"{trace_id}: missing approval cannot have side effects.")

    if trace.get("hidden_override_detected") is True:
        disposition = str(trace.get("hidden_override_disposition", "")).strip().lower()
        if disposition not in ACCEPTED_HIDDEN_OVERRIDE_DISPOSITIONS:
            errors.append(f"{trace_id}: hidden override must be rejected, quarantined, or ignored.")
        if active_dispatch:
            errors.append(f"{trace_id}: active dispatch cannot continue with a detected hidden override.")
    if trace.get("context_override_applied") is True:
        errors.append(f"{trace_id}: context override cannot be applied to command fields.")

    dispatch_receipt_ref = str(trace.get("dispatch_receipt_ref", "")).strip()
    if active_dispatch and not dispatch_receipt_ref:
        errors.append(f"{trace_id}: active dispatch requires a dispatch_receipt_ref.")
    if dispatch_receipt_ref and not dispatch_receipt_ref.startswith("dispatch://"):
        errors.append(f"{trace_id}: dispatch_receipt_ref must use dispatch://.")

    side_effects = trace.get("side_effects")
    if not isinstance(side_effects, list):
        errors.append(f"{trace_id}: side_effects must be a list.")
        side_effects = []
    runtime_adapter_receipt_ref = str(trace.get("runtime_adapter_receipt_ref", "")).strip()
    for index, effect in enumerate(side_effects):
        if not isinstance(effect, dict):
            errors.append(f"{trace_id}: side_effects[{index}] must be an object.")
            continue
        if effect.get("authorized") is not True:
            errors.append(f"{trace_id}: side_effects[{index}] must be explicitly authorized.")
        adapter_ref = str(effect.get("adapter_receipt_ref", "")).strip()
        if not runtime_adapter_receipt_ref or not adapter_ref:
            errors.append(f"{trace_id}: side effects require runtime adapter receipts.")
        elif adapter_ref != runtime_adapter_receipt_ref:
            errors.append(f"{trace_id}: side effect adapter receipt must match runtime_adapter_receipt_ref.")

    artifact_refs = trace.get("artifact_refs")
    if active_dispatch and not isinstance(artifact_refs, list):
        errors.append(f"{trace_id}: artifact_refs must be a list.")
    if active_dispatch and dispatch_state in {"delivered", "verified"}:
        if not artifact_refs:
            errors.append(f"{trace_id}: delivered/verified dispatch requires artifact_refs.")
        if trace.get("artifact_parent_links_present") is not True:
            errors.append(f"{trace_id}: artifacts must link back to the parent intent contract.")

    if active_dispatch and dispatch_state == "verified":
        verification_refs = nonempty_list(trace, "verification_refs", errors)
        if any(not isinstance(item, str) or not item.startswith("validator://") for item in verification_refs):
            errors.append(f"{trace_id}: verification_refs must use validator:// refs.")

    if trace.get("residual_known") is True:
        residuals = trace.get("residuals")
        if not isinstance(residuals, list) or not residuals:
            errors.append(f"{trace_id}: known residuals must be recorded.")
        if trace.get("residuals_preserved") is not True:
            errors.append(f"{trace_id}: known residuals must be preserved.")

    non_claim_text = text_blob(trace.get("non_claims", []))
    for phrase in REQUIRED_NON_CLAIMS:
        if phrase.lower() not in non_claim_text:
            errors.append(f"{trace_id}: non_claims missing {phrase!r}.")

    return errors


def build_expected_result(valid_count: int, invalid_count: int) -> dict[str, Any]:
    return {
        "schema_version": "asi_stack.intent_execution_handoff_probe.v0",
        "result_id": "2026-07-02-intent-execution-handoff-probe",
        "recorded_date": "2026-07-02",
        "command": COMMAND,
        "result_kind": "deterministic_synthetic_intent_execution_handoff_probe",
        "valid_trace_count": valid_count,
        "expected_invalid_control_count": invalid_count,
        "trace_count": len(TRACES),
        "accepted_handoff_path_count": 1,
        "blocked_handoff_path_count": 1,
        "negative_controls": {
            "dispatch_without_approval_rejected": True,
            "authority_widening_rejected": True,
            "hidden_override_application_rejected": True,
            "missing_dispatch_receipt_rejected": True,
            "side_effect_without_adapter_receipt_rejected": True,
            "residual_erasure_rejected": True,
            "artifact_parent_link_missing_rejected": True,
        },
        "transition_coverage": {
            "intent_to_command_handoff": True,
            "command_to_plan_handoff": True,
            "plan_to_job_handoff": True,
            "dispatch_receipt_required": True,
            "approval_block_receipt_required": True,
            "adapter_receipt_required_for_side_effects": True,
            "artifact_parent_link_required": True,
            "residual_preservation_required": True,
        },
        "lean_fixture_alignment": {
            "module": "AsiStackProofs.IntentToExecution",
            "proof_tag": PROOF_TAG,
            "theorem_refs": REQUIRED_THEOREMS,
            "expected": {
                "valid_handoff_path_present": True,
                "blocked_approval_path_present": True,
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
            "Synthetic record replay only; no natural-language parser, deployed dispatcher, approval service, runtime adapter, or artifact acceptance path was exercised.",
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
    if value.get("evidence_transition_created") is not False:
        errors.append(f"{rel(RESULT)}: evidence_transition_created must remain false.")
    non_claim_text = text_blob(value.get("non_claims", []))
    for phrase in REQUIRED_NON_CLAIMS:
        if phrase.lower() not in non_claim_text:
            errors.append(f"{rel(RESULT)} non_claims missing {phrase!r}.")


def validate_manifest(errors: list[str]) -> None:
    value = load_json(MANIFEST)
    chapter = None
    for part in value.get("parts", []):
        for candidate in part.get("chapters", []):
            if candidate.get("id") == "intent-to-execution-contracts":
                chapter = candidate
                break
    if chapter is None:
        errors.append("book_structure.json: missing intent-to-execution chapter.")
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
        "validHandoffPathPresent",
        "blockedApprovalPathPresent",
        "negativeControlsRejected",
        "supportStateEffectNone",
        "nonClaimBoundary",
    ):
        if field not in text:
            errors.append(f"{rel(LEAN_FILE)} missing fixture field {field}.")


def validate_surfaces(errors: list[str]) -> None:
    required = {
        DOC: [
            "Intent-to-Execution Handoff Probe",
            rel(RESULT),
            "two valid synthetic handoff traces",
            "seven expected-invalid controls",
            "no support-state transition",
        ],
        CHAPTER: [
            "Intent-to-execution handoff probe",
            rel(RESULT),
            "two valid synthetic handoff traces",
            "seven expected-invalid controls",
        ],
        READER: [
            "intent-to-execution handoff probe",
            "two synthetic traces",
            "not a deployed runtime result",
        ],
        OUTLINE: [
            CODEX_TEST_NAME,
            PROOF_TAG,
            rel(RESULT),
        ],
        ROADMAP: [
            "Intent-to-execution handoff probe",
            "deterministic synthetic vertical handoff fixture",
            "no support-state promotion",
        ],
        CHANGELOG: [
            "Intent-to-execution handoff probe",
            rel(RESULT),
        ],
        VALIDATE_BOOK: [
            "scripts/validate_intent_execution_handoff_probe.py",
            "docs/intent_execution_handoff_probe.md",
            "experiments/intent_execution_handoff/results/2026-07-02-local.json",
            'run_validator("validate_intent_execution_handoff_probe.py")',
        ],
    }
    for path, phrases in required.items():
        if not path.exists():
            errors.append(f"Missing required intent handoff surface {rel(path)}.")
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
        errors.append("Expected exactly two valid synthetic handoff traces.")
    if invalid_count != 7:
        errors.append("Expected exactly seven expected-invalid controls.")

    expected = build_expected_result(valid_count, invalid_count)
    validate_result(expected, args.write_result, errors)
    validate_manifest(errors)
    validate_lean(errors)
    validate_surfaces(errors)

    if errors:
        fail(errors)
    print("Intent-to-execution handoff probe validation passed.")


if __name__ == "__main__":
    main()
