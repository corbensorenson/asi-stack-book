#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "experiments" / "typed_job_delivery" / "results" / "2026-07-02-local.json"
DOC = ROOT / "docs" / "typed_job_delivery_probe.md"
CHAPTER = ROOT / "chapters" / "labor-os-and-typed-jobs.qmd"
READER = ROOT / "editions" / "reader_manuscript" / "v1_0" / "chapters" / "labor-os-and-typed-jobs.qmd"
OUTLINE = ROOT / "docs" / "book_outline.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
CHANGELOG = ROOT / "appendices" / "F_changelog.qmd"
MANIFEST = ROOT / "book_structure.json"
VALIDATE_BOOK = ROOT / "scripts" / "validate_book.py"
LEAN_FILE = ROOT / "lean" / "AsiStackProofs" / "TypedJobs.lean"

COMMAND = "python3 scripts/validate_typed_job_delivery_probe.py"
PROOF_TAG = "lean:jobs.lifecycle.delivery_probe_fixture_bridge"
CODEX_TEST_NAME = "Typed job delivery and evidence-readiness probe"
REQUIRED_THEOREMS = ["typed_job_delivery_probe_fixture_bridge"]
REQUIRED_NON_CLAIMS = [
    "does not execute a deployed scheduler",
    "does not prove permission enforcement",
    "does not prove approval-service behavior",
    "does not execute a runtime adapter",
    "does not prove replay correctness",
    "does not promote the chapter support state",
]


TRACES: list[dict[str, Any]] = [
    {
        "trace_id": "valid_evidence_ready_delivery",
        "expect_valid": True,
        "job_id": "job://verified-delivery",
        "parent_contract_id": "contract://cmd-verified-delivery",
        "plan_node_id": "plan://node-build-report",
        "contract_locked": True,
        "lifecycle_valid": True,
        "approval_required": True,
        "approval_recorded": True,
        "permissions_satisfied": True,
        "output_delivered": True,
        "verification_passed": True,
        "artifact_refs": ["artifact://report"],
        "audit_event_refs": ["audit://job-start", "audit://job-finish"],
        "residuals": ["none"],
        "replay_or_non_replay_reason": "replayable from artifact and audit refs",
        "delivery_state": "delivered",
        "evidence_state": "evidence_ready",
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "valid_delivered_not_evidence_ready",
        "expect_valid": True,
        "job_id": "job://delivered-pending-verification",
        "parent_contract_id": "contract://cmd-reader-summary",
        "plan_node_id": "plan://node-draft-summary",
        "contract_locked": True,
        "lifecycle_valid": True,
        "approval_required": False,
        "approval_recorded": False,
        "permissions_satisfied": True,
        "output_delivered": True,
        "verification_passed": False,
        "artifact_refs": ["artifact://draft-summary"],
        "audit_event_refs": ["audit://draft-start", "audit://draft-output"],
        "residuals": ["verification pending; delivery is not evidence-ready"],
        "replay_or_non_replay_reason": "non-replayable until verification receipt exists",
        "delivery_state": "delivered",
        "evidence_state": "adjudicating",
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "invalid_missing_parent_contract",
        "expect_valid": False,
        "job_id": "job://orphan-output",
        "parent_contract_id": "",
        "plan_node_id": "plan://node-orphan",
        "contract_locked": True,
        "lifecycle_valid": True,
        "approval_required": False,
        "approval_recorded": False,
        "permissions_satisfied": True,
        "output_delivered": True,
        "verification_passed": True,
        "artifact_refs": ["artifact://orphan"],
        "audit_event_refs": ["audit://orphan"],
        "residuals": ["none"],
        "replay_or_non_replay_reason": "replayable",
        "delivery_state": "delivered",
        "evidence_state": "evidence_ready",
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "invalid_approval_bypass",
        "expect_valid": False,
        "job_id": "job://approval-bypass",
        "parent_contract_id": "contract://cmd-high-impact",
        "plan_node_id": "plan://node-high-impact",
        "contract_locked": True,
        "lifecycle_valid": True,
        "approval_required": True,
        "approval_recorded": False,
        "permissions_satisfied": True,
        "output_delivered": True,
        "verification_passed": True,
        "artifact_refs": ["artifact://high-impact-output"],
        "audit_event_refs": ["audit://high-impact"],
        "residuals": ["approval missing"],
        "replay_or_non_replay_reason": "replayable",
        "delivery_state": "delivered",
        "evidence_state": "evidence_ready",
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "invalid_permission_overreach",
        "expect_valid": False,
        "job_id": "job://permission-overreach",
        "parent_contract_id": "contract://cmd-tool-use",
        "plan_node_id": "plan://node-tool-use",
        "contract_locked": True,
        "lifecycle_valid": True,
        "approval_required": False,
        "approval_recorded": False,
        "permissions_satisfied": False,
        "output_delivered": True,
        "verification_passed": True,
        "artifact_refs": ["artifact://tool-output"],
        "audit_event_refs": ["audit://tool-output"],
        "residuals": ["permission overreach"],
        "replay_or_non_replay_reason": "replayable",
        "delivery_state": "delivered",
        "evidence_state": "evidence_ready",
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "invalid_delivery_laundered_as_evidence_ready",
        "expect_valid": False,
        "job_id": "job://delivery-laundered",
        "parent_contract_id": "contract://cmd-draft",
        "plan_node_id": "plan://node-draft",
        "contract_locked": True,
        "lifecycle_valid": True,
        "approval_required": False,
        "approval_recorded": False,
        "permissions_satisfied": True,
        "output_delivered": True,
        "verification_passed": False,
        "artifact_refs": ["artifact://draft"],
        "audit_event_refs": ["audit://draft"],
        "residuals": ["verification missing"],
        "replay_or_non_replay_reason": "non-replayable until verified",
        "delivery_state": "delivered",
        "evidence_state": "evidence_ready",
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "invalid_missing_artifact_refs",
        "expect_valid": False,
        "job_id": "job://missing-artifact",
        "parent_contract_id": "contract://cmd-artifact",
        "plan_node_id": "plan://node-artifact",
        "contract_locked": True,
        "lifecycle_valid": True,
        "approval_required": False,
        "approval_recorded": False,
        "permissions_satisfied": True,
        "output_delivered": True,
        "verification_passed": True,
        "artifact_refs": [],
        "audit_event_refs": ["audit://artifact"],
        "residuals": ["artifact missing"],
        "replay_or_non_replay_reason": "replayable",
        "delivery_state": "delivered",
        "evidence_state": "evidence_ready",
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "invalid_missing_audit_events",
        "expect_valid": False,
        "job_id": "job://missing-audit",
        "parent_contract_id": "contract://cmd-audit",
        "plan_node_id": "plan://node-audit",
        "contract_locked": True,
        "lifecycle_valid": True,
        "approval_required": False,
        "approval_recorded": False,
        "permissions_satisfied": True,
        "output_delivered": True,
        "verification_passed": True,
        "artifact_refs": ["artifact://audit-output"],
        "audit_event_refs": [],
        "residuals": ["audit missing"],
        "replay_or_non_replay_reason": "replayable",
        "delivery_state": "delivered",
        "evidence_state": "evidence_ready",
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "invalid_support_state_promotion",
        "expect_valid": False,
        "job_id": "job://fixture-promotion",
        "parent_contract_id": "contract://cmd-fixture-promotion",
        "plan_node_id": "plan://node-fixture-promotion",
        "contract_locked": True,
        "lifecycle_valid": True,
        "approval_required": False,
        "approval_recorded": False,
        "permissions_satisfied": True,
        "output_delivered": True,
        "verification_passed": True,
        "artifact_refs": ["artifact://fixture-output"],
        "audit_event_refs": ["audit://fixture"],
        "residuals": ["none"],
        "replay_or_non_replay_reason": "replayable",
        "delivery_state": "delivered",
        "evidence_state": "evidence_ready",
        "support_state_effect": "promote_chapter_core",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Typed job delivery probe validation failed:")
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
    if trace.get("contract_locked") is not True:
        errors.append(f"{trace_id}: contract must be locked before delivery.")
    if trace.get("lifecycle_valid") is not True:
        errors.append(f"{trace_id}: lifecycle transition must be valid.")
    if trace.get("approval_required") is True and trace.get("approval_recorded") is not True:
        errors.append(f"{trace_id}: approval-required jobs need an approval record.")
    if trace.get("permissions_satisfied") is not True:
        errors.append(f"{trace_id}: permissions must satisfy requested adapter capabilities.")
    if trace.get("support_state_effect") != "none":
        errors.append(f"{trace_id}: support_state_effect must remain none.")

    artifact_refs = trace.get("artifact_refs")
    audit_refs = trace.get("audit_event_refs")
    residuals = trace.get("residuals")
    replay_reason = str(trace.get("replay_or_non_replay_reason", ""))
    evidence_ready = trace.get("evidence_state") == "evidence_ready"
    if evidence_ready:
        if trace.get("output_delivered") is not True:
            errors.append(f"{trace_id}: evidence-ready jobs must be delivered.")
        if trace.get("verification_passed") is not True:
            errors.append(f"{trace_id}: evidence-ready jobs require verification_passed.")
        if not isinstance(artifact_refs, list) or not artifact_refs:
            errors.append(f"{trace_id}: evidence-ready jobs require artifact_refs.")
        if not isinstance(audit_refs, list) or not audit_refs:
            errors.append(f"{trace_id}: evidence-ready jobs require audit_event_refs.")
        if not isinstance(residuals, list) or not residuals:
            errors.append(f"{trace_id}: evidence-ready jobs require residuals, even if none.")
        if not replay_reason.strip():
            errors.append(f"{trace_id}: evidence-ready jobs require replay_or_non_replay_reason.")
    if trace.get("output_delivered") is True and trace.get("verification_passed") is False:
        if evidence_ready:
            errors.append(f"{trace_id}: delivered but unverified output cannot be evidence-ready.")
        if not isinstance(residuals, list) or not residuals:
            errors.append(f"{trace_id}: delivered but unverified output needs residuals.")

    non_claim_text = text_blob(trace.get("non_claims", []))
    for phrase in REQUIRED_NON_CLAIMS:
        if phrase.lower() not in non_claim_text:
            errors.append(f"{trace_id}: non_claims missing {phrase!r}.")
    return errors


def build_expected_result(valid_count: int, invalid_count: int) -> dict[str, Any]:
    return {
        "schema_version": "asi_stack.typed_job_delivery_probe.v0",
        "result_id": "2026-07-02-typed-job-delivery-probe",
        "recorded_date": "2026-07-02",
        "command": COMMAND,
        "result_kind": "deterministic_synthetic_typed_job_delivery_probe",
        "valid_trace_count": valid_count,
        "expected_invalid_control_count": invalid_count,
        "trace_count": len(TRACES),
        "negative_controls": {
            "missing_parent_contract_rejected": True,
            "approval_bypass_rejected": True,
            "permission_overreach_rejected": True,
            "delivery_laundering_rejected": True,
            "missing_artifact_refs_rejected": True,
            "missing_audit_events_rejected": True,
            "support_state_promotion_rejected": True,
        },
        "transition_coverage": {
            "verified_delivery_evidence_ready": True,
            "delivered_not_evidence_ready": True,
            "parentage_required": True,
            "approval_required": True,
            "permissions_required": True,
            "artifact_and_audit_required": True,
            "support_state_no_promotion": True,
        },
        "lean_fixture_alignment": {
            "module": "AsiStackProofs.TypedJobs",
            "proof_tag": PROOF_TAG,
            "theorem_refs": REQUIRED_THEOREMS,
            "expected": {
                "verified_delivery_trace_present": True,
                "delivered_not_evidence_ready_trace_present": True,
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
            "Synthetic typed-job delivery fixture only; no scheduler, approval service, permission service, runtime adapter, replay engine, or deployed Labor OS was executed.",
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
        "verifiedDeliveryTracePresent",
        "deliveredNotEvidenceReadyTracePresent",
        "negativeControlsRejected",
        "supportStateEffectNone",
        "nonClaimBoundary",
    ):
        if field not in text:
            errors.append(f"{rel(LEAN_FILE)} missing fixture field {field}.")


def validate_surfaces(errors: list[str]) -> None:
    required = {
        DOC: [
            "Typed Job Delivery Probe",
            rel(RESULT),
            "two valid synthetic typed-job traces",
            "seven expected-invalid controls",
            "no support-state transition",
        ],
        CHAPTER: [
            "Typed job delivery and evidence-readiness probe",
            rel(RESULT),
            "two valid synthetic typed-job traces",
            "seven expected-invalid controls",
        ],
        READER: [
            "typed job delivery and evidence-readiness probe",
            "two synthetic typed-job traces",
            "not a deployed Labor OS result",
        ],
        OUTLINE: [CODEX_TEST_NAME, PROOF_TAG, rel(RESULT)],
        ROADMAP: [
            "Typed job delivery and evidence-readiness probe",
            "deterministic synthetic typed-job delivery fixture",
            "no support-state promotion",
        ],
        CHANGELOG: ["Typed job delivery and evidence-readiness probe", rel(RESULT)],
        VALIDATE_BOOK: [
            "scripts/validate_typed_job_delivery_probe.py",
            "docs/typed_job_delivery_probe.md",
            "experiments/typed_job_delivery/results/2026-07-02-local.json",
            'run_validator("validate_typed_job_delivery_probe.py")',
        ],
    }
    for path, phrases in required.items():
        if not path.exists():
            errors.append(f"Missing required typed-job delivery surface {rel(path)}.")
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
        errors.append("Expected exactly two valid synthetic typed-job traces.")
    if invalid_count != 7:
        errors.append("Expected exactly seven expected-invalid controls.")

    expected = build_expected_result(valid_count, invalid_count)
    validate_result(expected, args.write_result, errors)
    validate_manifest(errors)
    validate_lean(errors)
    validate_surfaces(errors)

    if errors:
        fail(errors)
    print("Typed job delivery probe validation passed.")


if __name__ == "__main__":
    main()
