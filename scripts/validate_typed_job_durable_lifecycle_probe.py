#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "experiments" / "typed_job_durable_lifecycle" / "results" / "2026-07-02-local.json"
DOC = ROOT / "docs" / "typed_job_durable_lifecycle_probe.md"
CHAPTER = ROOT / "chapters" / "labor-os-and-typed-jobs.qmd"
READER = ROOT / "editions" / "reader_manuscript" / "v1_0" / "chapters" / "labor-os-and-typed-jobs.qmd"
OUTLINE = ROOT / "docs" / "book_outline.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
CHANGELOG = ROOT / "appendices" / "F_changelog.qmd"
MANIFEST = ROOT / "book_structure.json"
VALIDATION_REGISTRY = ROOT / "validation" / "registry.json"
LEAN_FILE = ROOT / "lean" / "AsiStackProofs" / "TypedJobs.lean"

COMMAND = "python3 scripts/validate_typed_job_durable_lifecycle_probe.py"
PROOF_TAG = "lean:jobs.lifecycle.durable_lifecycle_probe_bridge"
CODEX_TEST_NAME = "Typed job durable lifecycle probe"
REQUIRED_THEOREMS = [
    "durable_retry_without_idempotency_rejected",
    "durable_retry_authority_widening_rejected",
    "durable_retry_permission_overreach_rejected",
    "durable_expired_lease_dispatch_rejected",
    "durable_evidence_ready_missing_completion_receipt_rejected",
    "durable_evidence_ready_missing_replay_ref_rejected",
    "durable_blocked_without_residual_owner_rejected",
    "durable_missing_non_claim_boundary_rejected",
    "durable_support_promotion_rejected",
    "durable_retry_complete_trace_accepted",
    "durable_expired_lease_blocked_trace_accepted",
    "typed_job_durable_lifecycle_probe_fixture_bridge",
]
REQUIRED_NON_CLAIMS = [
    "does not execute a deployed scheduler",
    "does not prove durable workflow recovery",
    "does not prove permission enforcement",
    "does not prove approval-service behavior",
    "does not prove replay correctness",
    "does not promote the chapter support state",
]

ALLOWED_STATES = {
    "locked",
    "dispatchable",
    "running",
    "failed",
    "blocked",
    "adjudicating",
    "delivered",
    "evidence_ready",
}
ALLOWED_TRANSITIONS = {
    ("locked", "dispatchable"),
    ("dispatchable", "running"),
    ("dispatchable", "blocked"),
    ("running", "failed"),
    ("running", "blocked"),
    ("running", "adjudicating"),
    ("adjudicating", "delivered"),
    ("delivered", "evidence_ready"),
    ("failed", "dispatchable"),
}


TRACES: list[dict[str, Any]] = [
    {
        "trace_id": "valid_retry_resumes_under_same_contract",
        "expect_valid": True,
        "job_id": "job://durable-retry-report",
        "parent_contract_id": "contract://cmd-durable-report",
        "plan_node_id": "plan://node-durable-report",
        "actor_kind": "typed_job",
        "lifecycle_path": [
            "locked",
            "dispatchable",
            "running",
            "failed",
            "dispatchable",
            "running",
            "adjudicating",
            "delivered",
            "evidence_ready",
        ],
        "retry_attempted": True,
        "attempt_count": 2,
        "idempotency_key": "idem://durable-retry-report",
        "retry_reason": "transient adapter timeout; same contract and same authority envelope",
        "retry_within_policy": True,
        "authority_unchanged": True,
        "permissions_satisfied": True,
        "approval_required": True,
        "approval_recorded": True,
        "lease_active": True,
        "dispatch_requested": True,
        "output_delivered": True,
        "evidence_state": "evidence_ready",
        "completion_receipt_ref": "receipt://durable-retry-report",
        "artifact_refs": ["artifact://durable-report"],
        "audit_event_refs": [
            "audit://durable-report-attempt-1",
            "audit://durable-report-retry",
            "audit://durable-report-attempt-2",
        ],
        "replay_ref": "replay://durable-report",
        "blocked_reason": "",
        "residual_owner": "owner://labor-os-reviewer",
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "valid_lease_expiry_blocks_dispatch",
        "expect_valid": True,
        "job_id": "job://expired-lease-block",
        "parent_contract_id": "contract://cmd-expired-lease-block",
        "plan_node_id": "plan://node-expired-lease-block",
        "actor_kind": "typed_job",
        "lifecycle_path": ["locked", "dispatchable", "blocked"],
        "retry_attempted": False,
        "attempt_count": 1,
        "idempotency_key": "",
        "retry_reason": "",
        "retry_within_policy": False,
        "authority_unchanged": True,
        "permissions_satisfied": True,
        "approval_required": False,
        "approval_recorded": False,
        "lease_active": False,
        "dispatch_requested": False,
        "output_delivered": False,
        "evidence_state": "blocked",
        "completion_receipt_ref": "",
        "artifact_refs": [],
        "audit_event_refs": ["audit://expired-lease-block"],
        "replay_ref": "",
        "blocked_reason": "lease expired before dispatch; block and assign residual owner",
        "residual_owner": "owner://labor-os-reviewer",
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "invalid_retry_without_idempotency_key",
        "expect_valid": False,
        "job_id": "job://missing-idempotency",
        "parent_contract_id": "contract://cmd-missing-idempotency",
        "plan_node_id": "plan://node-missing-idempotency",
        "actor_kind": "typed_job",
        "lifecycle_path": ["locked", "dispatchable", "running", "failed", "dispatchable"],
        "retry_attempted": True,
        "attempt_count": 2,
        "idempotency_key": "",
        "retry_reason": "transient adapter timeout",
        "retry_within_policy": True,
        "authority_unchanged": True,
        "permissions_satisfied": True,
        "approval_required": False,
        "approval_recorded": False,
        "lease_active": True,
        "dispatch_requested": True,
        "output_delivered": False,
        "evidence_state": "blocked",
        "completion_receipt_ref": "",
        "artifact_refs": [],
        "audit_event_refs": ["audit://missing-idempotency"],
        "replay_ref": "",
        "blocked_reason": "retry lacks idempotency key",
        "residual_owner": "owner://labor-os-reviewer",
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "invalid_authority_widening_on_retry",
        "expect_valid": False,
        "job_id": "job://authority-widening-retry",
        "parent_contract_id": "contract://cmd-authority-widening",
        "plan_node_id": "plan://node-authority-widening",
        "actor_kind": "typed_job",
        "lifecycle_path": ["locked", "dispatchable", "running", "failed", "dispatchable"],
        "retry_attempted": True,
        "attempt_count": 2,
        "idempotency_key": "idem://authority-widening",
        "retry_reason": "retry requests broader tool authority",
        "retry_within_policy": True,
        "authority_unchanged": False,
        "permissions_satisfied": True,
        "approval_required": False,
        "approval_recorded": False,
        "lease_active": True,
        "dispatch_requested": True,
        "output_delivered": False,
        "evidence_state": "blocked",
        "completion_receipt_ref": "",
        "artifact_refs": [],
        "audit_event_refs": ["audit://authority-widening"],
        "replay_ref": "",
        "blocked_reason": "retry widens authority",
        "residual_owner": "owner://labor-os-reviewer",
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "invalid_permission_overreach_after_resume",
        "expect_valid": False,
        "job_id": "job://permission-overreach-resume",
        "parent_contract_id": "contract://cmd-permission-overreach-resume",
        "plan_node_id": "plan://node-permission-overreach-resume",
        "actor_kind": "typed_job",
        "lifecycle_path": ["locked", "dispatchable", "running", "failed", "dispatchable"],
        "retry_attempted": True,
        "attempt_count": 2,
        "idempotency_key": "idem://permission-overreach-resume",
        "retry_reason": "resume with undeclared adapter capability",
        "retry_within_policy": True,
        "authority_unchanged": True,
        "permissions_satisfied": False,
        "approval_required": False,
        "approval_recorded": False,
        "lease_active": True,
        "dispatch_requested": True,
        "output_delivered": False,
        "evidence_state": "blocked",
        "completion_receipt_ref": "",
        "artifact_refs": [],
        "audit_event_refs": ["audit://permission-overreach-resume"],
        "replay_ref": "",
        "blocked_reason": "permissions no longer satisfy adapter capability",
        "residual_owner": "owner://labor-os-reviewer",
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "invalid_lease_expired_dispatch",
        "expect_valid": False,
        "job_id": "job://expired-lease-dispatch",
        "parent_contract_id": "contract://cmd-expired-lease-dispatch",
        "plan_node_id": "plan://node-expired-lease-dispatch",
        "actor_kind": "typed_job",
        "lifecycle_path": ["locked", "dispatchable", "running"],
        "retry_attempted": False,
        "attempt_count": 1,
        "idempotency_key": "",
        "retry_reason": "",
        "retry_within_policy": False,
        "authority_unchanged": True,
        "permissions_satisfied": True,
        "approval_required": False,
        "approval_recorded": False,
        "lease_active": False,
        "dispatch_requested": True,
        "output_delivered": False,
        "evidence_state": "running",
        "completion_receipt_ref": "",
        "artifact_refs": [],
        "audit_event_refs": ["audit://expired-lease-dispatch"],
        "replay_ref": "",
        "blocked_reason": "",
        "residual_owner": "",
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "invalid_missing_completion_receipt",
        "expect_valid": False,
        "job_id": "job://missing-completion-receipt",
        "parent_contract_id": "contract://cmd-missing-completion-receipt",
        "plan_node_id": "plan://node-missing-completion-receipt",
        "actor_kind": "typed_job",
        "lifecycle_path": ["locked", "dispatchable", "running", "adjudicating", "delivered", "evidence_ready"],
        "retry_attempted": False,
        "attempt_count": 1,
        "idempotency_key": "",
        "retry_reason": "",
        "retry_within_policy": False,
        "authority_unchanged": True,
        "permissions_satisfied": True,
        "approval_required": False,
        "approval_recorded": False,
        "lease_active": True,
        "dispatch_requested": True,
        "output_delivered": True,
        "evidence_state": "evidence_ready",
        "completion_receipt_ref": "",
        "artifact_refs": ["artifact://missing-receipt-output"],
        "audit_event_refs": ["audit://missing-receipt"],
        "replay_ref": "replay://missing-receipt",
        "blocked_reason": "",
        "residual_owner": "owner://labor-os-reviewer",
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "invalid_missing_replay_ref_for_evidence_ready",
        "expect_valid": False,
        "job_id": "job://missing-replay-ref",
        "parent_contract_id": "contract://cmd-missing-replay-ref",
        "plan_node_id": "plan://node-missing-replay-ref",
        "actor_kind": "typed_job",
        "lifecycle_path": ["locked", "dispatchable", "running", "adjudicating", "delivered", "evidence_ready"],
        "retry_attempted": False,
        "attempt_count": 1,
        "idempotency_key": "",
        "retry_reason": "",
        "retry_within_policy": False,
        "authority_unchanged": True,
        "permissions_satisfied": True,
        "approval_required": False,
        "approval_recorded": False,
        "lease_active": True,
        "dispatch_requested": True,
        "output_delivered": True,
        "evidence_state": "evidence_ready",
        "completion_receipt_ref": "receipt://missing-replay-ref",
        "artifact_refs": ["artifact://missing-replay-output"],
        "audit_event_refs": ["audit://missing-replay"],
        "replay_ref": "",
        "blocked_reason": "",
        "residual_owner": "owner://labor-os-reviewer",
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "invalid_missing_residual_owner_on_block",
        "expect_valid": False,
        "job_id": "job://missing-residual-owner",
        "parent_contract_id": "contract://cmd-missing-residual-owner",
        "plan_node_id": "plan://node-missing-residual-owner",
        "actor_kind": "typed_job",
        "lifecycle_path": ["locked", "dispatchable", "blocked"],
        "retry_attempted": False,
        "attempt_count": 1,
        "idempotency_key": "",
        "retry_reason": "",
        "retry_within_policy": False,
        "authority_unchanged": True,
        "permissions_satisfied": True,
        "approval_required": False,
        "approval_recorded": False,
        "lease_active": False,
        "dispatch_requested": False,
        "output_delivered": False,
        "evidence_state": "blocked",
        "completion_receipt_ref": "",
        "artifact_refs": [],
        "audit_event_refs": ["audit://missing-residual-owner"],
        "replay_ref": "",
        "blocked_reason": "lease expired before dispatch",
        "residual_owner": "",
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "invalid_missing_non_claim_boundary",
        "expect_valid": False,
        "job_id": "job://missing-non-claim-boundary",
        "parent_contract_id": "contract://cmd-missing-non-claim-boundary",
        "plan_node_id": "plan://node-missing-non-claim-boundary",
        "actor_kind": "typed_job",
        "lifecycle_path": ["locked", "dispatchable", "running", "adjudicating", "delivered", "evidence_ready"],
        "retry_attempted": False,
        "attempt_count": 1,
        "idempotency_key": "",
        "retry_reason": "",
        "retry_within_policy": False,
        "authority_unchanged": True,
        "permissions_satisfied": True,
        "approval_required": False,
        "approval_recorded": False,
        "lease_active": True,
        "dispatch_requested": True,
        "output_delivered": True,
        "evidence_state": "evidence_ready",
        "completion_receipt_ref": "receipt://missing-non-claim-boundary",
        "artifact_refs": ["artifact://missing-non-claim-boundary"],
        "audit_event_refs": ["audit://missing-non-claim-boundary"],
        "replay_ref": "replay://missing-non-claim-boundary",
        "blocked_reason": "",
        "residual_owner": "owner://labor-os-reviewer",
        "support_state_effect": "none",
        "non_claims": [],
    },
    {
        "trace_id": "invalid_support_state_promotion",
        "expect_valid": False,
        "job_id": "job://durable-lifecycle-promotion",
        "parent_contract_id": "contract://cmd-durable-lifecycle-promotion",
        "plan_node_id": "plan://node-durable-lifecycle-promotion",
        "actor_kind": "typed_job",
        "lifecycle_path": ["locked", "dispatchable", "running", "adjudicating", "delivered", "evidence_ready"],
        "retry_attempted": False,
        "attempt_count": 1,
        "idempotency_key": "",
        "retry_reason": "",
        "retry_within_policy": False,
        "authority_unchanged": True,
        "permissions_satisfied": True,
        "approval_required": False,
        "approval_recorded": False,
        "lease_active": True,
        "dispatch_requested": True,
        "output_delivered": True,
        "evidence_state": "evidence_ready",
        "completion_receipt_ref": "receipt://durable-lifecycle-promotion",
        "artifact_refs": ["artifact://durable-lifecycle-promotion"],
        "audit_event_refs": ["audit://durable-lifecycle-promotion"],
        "replay_ref": "replay://durable-lifecycle-promotion",
        "blocked_reason": "",
        "residual_owner": "owner://labor-os-reviewer",
        "support_state_effect": "promote_chapter_core",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Typed job durable lifecycle probe validation failed:")
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


def trace_errors(trace: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    trace_id = str(trace.get("trace_id", "<missing>"))
    if not isinstance(trace.get("job_id"), str) or not trace["job_id"].startswith("job://"):
        errors.append(f"{trace_id}: job_id must use job://.")
    if not isinstance(trace.get("parent_contract_id"), str) or not trace["parent_contract_id"].startswith("contract://"):
        errors.append(f"{trace_id}: parent_contract_id must use contract://.")
    if not isinstance(trace.get("plan_node_id"), str) or not trace["plan_node_id"].startswith("plan://"):
        errors.append(f"{trace_id}: plan_node_id must use plan://.")
    if trace.get("actor_kind") != "typed_job":
        errors.append(f"{trace_id}: actor_kind must be typed_job, not ambient agent.")
    if trace.get("support_state_effect") != "none":
        errors.append(f"{trace_id}: support_state_effect must remain none.")

    path = trace.get("lifecycle_path")
    if not isinstance(path, list) or len(path) < 2:
        errors.append(f"{trace_id}: lifecycle_path must include at least two states.")
    else:
        for state in path:
            if state not in ALLOWED_STATES:
                errors.append(f"{trace_id}: lifecycle state {state!r} is not allowed.")
        for left, right in zip(path, path[1:]):
            if (left, right) not in ALLOWED_TRANSITIONS:
                errors.append(f"{trace_id}: invalid lifecycle transition {left!r}->{right!r}.")

    if trace.get("approval_required") is True and trace.get("approval_recorded") is not True:
        errors.append(f"{trace_id}: approval-required durable jobs need an approval record.")
    if trace.get("permissions_satisfied") is not True:
        errors.append(f"{trace_id}: permissions must satisfy requested adapter capabilities.")

    retry_attempted = trace.get("retry_attempted") is True
    if retry_attempted:
        if not isinstance(trace.get("attempt_count"), int) or trace["attempt_count"] < 2:
            errors.append(f"{trace_id}: retry traces need at least two attempts.")
        if not isinstance(trace.get("idempotency_key"), str) or not trace["idempotency_key"].startswith("idem://"):
            errors.append(f"{trace_id}: retry traces need an idempotency key.")
        if trace.get("retry_within_policy") is not True:
            errors.append(f"{trace_id}: retry must remain within policy.")
        if trace.get("authority_unchanged") is not True:
            errors.append(f"{trace_id}: retry must not widen authority.")
        if not str(trace.get("retry_reason", "")).strip():
            errors.append(f"{trace_id}: retry traces need a retry_reason.")

    if trace.get("dispatch_requested") is True and trace.get("lease_active") is not True:
        errors.append(f"{trace_id}: dispatch requires an active lease.")

    evidence_ready = trace.get("evidence_state") == "evidence_ready"
    if evidence_ready:
        if trace.get("output_delivered") is not True:
            errors.append(f"{trace_id}: evidence-ready durable jobs must be delivered.")
        if not isinstance(trace.get("completion_receipt_ref"), str) or not trace["completion_receipt_ref"].startswith("receipt://"):
            errors.append(f"{trace_id}: evidence-ready durable jobs need a completion receipt.")
        if not isinstance(trace.get("replay_ref"), str) or not trace["replay_ref"].startswith("replay://"):
            errors.append(f"{trace_id}: evidence-ready durable jobs need a replay ref.")
        if not isinstance(trace.get("artifact_refs"), list) or not trace["artifact_refs"]:
            errors.append(f"{trace_id}: evidence-ready durable jobs need artifact refs.")
        if not isinstance(trace.get("audit_event_refs"), list) or not trace["audit_event_refs"]:
            errors.append(f"{trace_id}: evidence-ready durable jobs need audit event refs.")

    if trace.get("evidence_state") == "blocked" or "blocked" in trace.get("lifecycle_path", []):
        if not str(trace.get("blocked_reason", "")).strip():
            errors.append(f"{trace_id}: blocked durable traces need a blocked_reason.")
        if not isinstance(trace.get("residual_owner"), str) or not trace["residual_owner"].startswith("owner://"):
            errors.append(f"{trace_id}: blocked durable traces need a residual owner.")

    non_claim_text = text_blob(trace.get("non_claims", []))
    for phrase in REQUIRED_NON_CLAIMS:
        if phrase.lower() not in non_claim_text:
            errors.append(f"{trace_id}: non_claims missing {phrase!r}.")
    return errors


def build_expected_result(valid_count: int, invalid_count: int) -> dict[str, Any]:
    return {
        "schema_version": "asi_stack.typed_job_durable_lifecycle_probe.v0",
        "result_id": "2026-07-02-typed-job-durable-lifecycle-probe",
        "recorded_date": "2026-07-02",
        "command": COMMAND,
        "result_kind": "deterministic_synthetic_typed_job_durable_lifecycle_probe",
        "valid_trace_count": valid_count,
        "expected_invalid_control_count": invalid_count,
        "trace_count": len(TRACES),
        "negative_controls": {
            "retry_without_idempotency_rejected": True,
            "authority_widening_on_retry_rejected": True,
            "permission_overreach_after_resume_rejected": True,
            "expired_lease_dispatch_rejected": True,
            "missing_completion_receipt_rejected": True,
            "missing_replay_ref_rejected": True,
            "missing_residual_owner_rejected": True,
            "missing_non_claim_boundary_rejected": True,
            "support_state_promotion_rejected": True,
        },
        "transition_coverage": {
            "retry_resume_same_contract": True,
            "idempotency_required_for_retry": True,
            "authority_unchanged_on_retry": True,
            "permission_basis_required_after_resume": True,
            "active_lease_required_for_dispatch": True,
            "expired_lease_can_block_with_residual_owner": True,
            "completion_receipt_required_for_evidence_ready": True,
            "replay_ref_required_for_evidence_ready": True,
            "support_state_no_promotion": True,
        },
        "lean_fixture_alignment": {
            "module": "AsiStackProofs.TypedJobs",
            "proof_tag": PROOF_TAG,
            "theorem_refs": REQUIRED_THEOREMS,
            "expected": {
                "retryResumeTracePresent": True,
                "expiredLeaseBlockTracePresent": True,
                "negativeControlsRejected": True,
                "completionAndReplayBoundaries": True,
                "supportStateEffectNone": True,
                "nonClaimBoundary": True,
            },
        },
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
        "verification_result": "pass",
        "residuals": [
            "Synthetic typed-job durable lifecycle fixture only; no scheduler, durable workflow engine, approval service, permission service, runtime adapter, replay engine, or deployed Labor OS was executed.",
            "The Labor OS chapter core claim remains at argument support.",
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


def validate_manifest(errors: list[str]) -> None:
    value = load_json(MANIFEST)
    chapter = None
    for part in value.get("parts", []):
        for candidate in part.get("chapters", []):
            if candidate.get("id") == "labor-os-and-typed-jobs":
                chapter = candidate
                break
    if chapter is None:
        errors.append("book_structure.json: missing Labor OS chapter.")
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
        "retryResumeTracePresent",
        "expiredLeaseBlockTracePresent",
        "negativeControlsRejected",
        "completionAndReplayBoundaries",
        "supportStateEffectNone",
        "nonClaimBoundary",
    ):
        if field not in text:
            errors.append(f"{rel(LEAN_FILE)} missing fixture field {field}.")


def validate_surfaces(errors: list[str]) -> None:
    required = {
        DOC: [
            "Typed Job Durable Lifecycle Probe",
            rel(RESULT),
            "two valid synthetic durable lifecycle traces",
            "nine expected-invalid controls",
            "no support-state transition",
        ],
        CHAPTER: [
            "Typed job durable lifecycle probe",
            rel(RESULT),
            "two valid synthetic durable lifecycle traces",
            "nine expected-invalid controls",
        ],
        READER: [
            "typed job durable lifecycle probe",
            "two synthetic durable lifecycle traces",
            "not a deployed Labor OS result",
        ],
        OUTLINE: [CODEX_TEST_NAME, PROOF_TAG, rel(RESULT)],
        ROADMAP: [
            "Typed job durable lifecycle probe",
            "deterministic synthetic durable lifecycle fixture",
            "no support-state promotion",
        ],
        CHANGELOG: ["Typed job durable lifecycle probe", rel(RESULT)],
        VALIDATION_REGISTRY: [
            "scripts/validate_typed_job_durable_lifecycle_probe.py",
            "docs/typed_job_durable_lifecycle_probe.md",
            "experiments/typed_job_durable_lifecycle/results/2026-07-02-local.json",
            '"script": "validate_typed_job_durable_lifecycle_probe.py"',
        ],
    }
    for path, phrases in required.items():
        if not path.exists():
            errors.append(f"Missing required durable lifecycle surface {rel(path)}.")
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
    for trace in TRACES:
        expect_valid = bool(trace.get("expect_valid"))
        current_errors = trace_errors(trace)
        if expect_valid:
            valid_count += 1
            errors.extend(current_errors)
        else:
            invalid_count += 1
            if not current_errors:
                errors.append(f"{trace.get('trace_id', '<missing>')}: expected-invalid control unexpectedly passed.")

    if valid_count != 2:
        errors.append("Expected exactly two valid synthetic durable lifecycle traces.")
    if invalid_count != 9:
        errors.append("Expected exactly nine expected-invalid controls.")

    expected = build_expected_result(valid_count, invalid_count)
    validate_result(expected, args.write_result, errors)
    validate_manifest(errors)
    validate_lean(errors)
    validate_surfaces(errors)

    if errors:
        fail(errors)
    print("Typed job durable lifecycle probe validation passed.")


if __name__ == "__main__":
    main()
