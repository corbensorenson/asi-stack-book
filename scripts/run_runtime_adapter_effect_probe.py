#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "experiments" / "runtime_adapter_effect_probe" / "results" / "2026-07-02-local.json"
PROBE_ID = "runtime-adapter-effect-replay-2026-07-02-local"
RESULT_COMMAND = "python3 scripts/run_runtime_adapter_effect_probe.py --write-result"
FIXTURE_TEMPLATE = ROOT / "experiments" / "runtime_adapter_permissions" / "fixtures" / "valid_low_impact_local_write.json"

NON_CLAIMS = [
    "This runtime adapter effect replay probe does not promote any chapter core claim above argument.",
    "This runtime adapter effect replay probe does not create a support-state transition.",
    "This runtime adapter effect replay probe does not prove deployed adapter behavior, sandbox isolation, approval-service behavior, secret-handle safety, revocation propagation, policy-enforcement correctness, rollback-service behavior, benchmark performance, or any AI safety property.",
    "This runtime adapter effect replay probe writes only a generated public-safe temporary file outside the repository, records hashes and gate decisions, and does not copy file contents, private source text, private keys, local absolute paths, or secret payloads into the repository.",
]


def initial_bytes() -> bytes:
    return (
        "Runtime adapter effect replay public-safe draft\n"
        "authority: handle://runtime-effect-probe/local-write-001\n"
        "lease: lease://runtime-effect-probe/local-write-001\n"
        "state: before-effect\n"
    ).encode("utf-8")


def appended_bytes() -> bytes:
    return (
        "state: after-effect\n"
        "effect: append bounded review note\n"
        "receipt: receipt://runtime-effect-probe/local-write-001\n"
    ).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def no_path_payload(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: no_path_payload(child) for key, child in value.items()}
    if isinstance(value, list):
        return [no_path_payload(child) for child in value]
    if isinstance(value, str):
        return value.replace(str(ROOT), "<REPO>")
    return value


def decision_for(gate: dict[str, Any]) -> tuple[str, str]:
    capability = gate["requested_capability"]
    permissions = set(gate["parent_permissions"])
    if capability not in permissions:
        return "deny", "missing_parent_permission"
    if gate["approval_required"] and str(gate["approval_expiry"]).startswith("expired"):
        return "deny", "expired_approval"
    if gate["approval_required"] and not str(gate["approval_record"]).startswith("approval://"):
        return "deny", "missing_approval_record"
    return "dispatch", "all_local_probe_gates_satisfied"


def state_record(kind: str, payload: bytes) -> dict[str, Any]:
    return {
        "kind": kind,
        "logical_ref": f"state://runtime-effect-probe/{kind}",
        "bytes": len(payload),
        "sha256": sha256_bytes(payload),
    }


def execute_valid_scenario(temp_dir: Path) -> dict[str, Any]:
    gate = {
        "parent_job": "job://runtime-effect-probe/local-write-001",
        "adapter_id": "adapter://local-filesystem",
        "target_type": "local_temp_file",
        "requested_capability": "filesystem.write",
        "parent_permissions": ["filesystem.write", "repo_write"],
        "approval_required": False,
        "approval_record": "not_required",
        "approval_scope": "not_required",
        "approval_expiry": "not_required",
        "effect_lease": "lease://runtime-effect-probe/local-write-001",
        "authority_handle": "handle://runtime-effect-probe/local-write-001",
        "sandbox_mode": "python_tempdir_workspace",
        "impact_class": "low_impact",
        "risk_tier": "low",
    }
    decision, reason = decision_for(gate)
    draft_path = temp_dir / "runtime_effect_probe_draft.txt"
    before = initial_bytes()
    append = appended_bytes()
    draft_path.write_bytes(before)
    pre_payload = draft_path.read_bytes()

    started = time.perf_counter()
    effect_executed = False
    rollback_executed = False
    if decision == "dispatch":
        draft_path.write_bytes(pre_payload + append)
        effect_executed = True
        post_payload = draft_path.read_bytes()
        draft_path.write_bytes(pre_payload)
        rollback_executed = True
        rollback_payload = draft_path.read_bytes()
    else:
        post_payload = draft_path.read_bytes()
        rollback_payload = post_payload
    elapsed_ms = round((time.perf_counter() - started) * 1000, 3)

    return {
        "scenario_id": "valid_low_impact_local_write_effect_replay",
        "fixture_template_ref": "experiments/runtime_adapter_permissions/fixtures/valid_low_impact_local_write.json",
        "decision": decision,
        "decision_reason": reason,
        "effect_executed": effect_executed,
        "rollback_executed": rollback_executed,
        "elapsed_ms": elapsed_ms,
        "gate": gate,
        "receipt": {
            "effect_receipt": "receipt://runtime-effect-probe/local-write-001",
            "rollback_handle": "rollback://runtime-effect-probe/restore-pre-state",
            "verification_refs": [
                "check://runtime-effect-probe/pre-post-digest-change",
                "check://runtime-effect-probe/rollback-digest-restored",
            ],
            "audit_refs": ["audit://runtime-effect-probe/local-write-001"],
            "support_state_effect": "none",
            "chapter_core_support_effect": "none",
        },
        "states": {
            "pre": state_record("pre", pre_payload),
            "post": state_record("post", post_payload),
            "rollback": state_record("rollback", rollback_payload),
        },
        "checks": {
            "post_changed": sha256_bytes(pre_payload) != sha256_bytes(post_payload),
            "rollback_exact": rollback_payload == pre_payload,
            "repo_write": False,
            "network_used": False,
        },
    }


def execute_denied_control(temp_dir: Path, scenario_id: str, gate: dict[str, Any]) -> dict[str, Any]:
    decision, reason = decision_for(gate)
    draft_path = temp_dir / f"{scenario_id}.txt"
    before = initial_bytes()
    draft_path.write_bytes(before)
    pre_payload = draft_path.read_bytes()
    effect_executed = False
    if decision == "dispatch":
        draft_path.write_bytes(pre_payload + appended_bytes())
        effect_executed = True
    post_payload = draft_path.read_bytes()
    return {
        "scenario_id": scenario_id,
        "decision": decision,
        "decision_reason": reason,
        "effect_executed": effect_executed,
        "gate": gate,
        "states": {
            "pre": state_record("pre", pre_payload),
            "post": state_record("post", post_payload),
        },
        "checks": {
            "blocked_before_mutation": decision == "deny" and not effect_executed,
            "state_unchanged": pre_payload == post_payload,
            "repo_write": False,
            "network_used": False,
        },
    }


def build_record() -> dict[str, Any]:
    if not FIXTURE_TEMPLATE.exists():
        raise SystemExit(f"Missing fixture template: {FIXTURE_TEMPLATE.relative_to(ROOT)}")

    with tempfile.TemporaryDirectory(prefix="runtime_adapter_effect_probe_") as temp:
        temp_dir = Path(temp)
        valid = execute_valid_scenario(temp_dir)
        controls = [
            execute_denied_control(
                temp_dir,
                "invalid_missing_permission_no_mutation",
                {
                    "parent_job": "job://runtime-effect-probe/missing-permission-001",
                    "adapter_id": "adapter://local-filesystem",
                    "target_type": "local_temp_file",
                    "requested_capability": "filesystem.write",
                    "parent_permissions": ["repo_read"],
                    "approval_required": False,
                    "approval_record": "not_required",
                    "approval_scope": "not_required",
                    "approval_expiry": "not_required",
                    "effect_lease": "lease://runtime-effect-probe/missing-permission-001",
                    "authority_handle": "handle://runtime-effect-probe/missing-permission-001",
                    "sandbox_mode": "python_tempdir_workspace",
                    "impact_class": "low_impact",
                    "risk_tier": "low",
                },
            ),
            execute_denied_control(
                temp_dir,
                "invalid_expired_approval_no_mutation",
                {
                    "parent_job": "job://runtime-effect-probe/expired-approval-001",
                    "adapter_id": "adapter://local-filesystem",
                    "target_type": "deployment_preview",
                    "requested_capability": "filesystem.write",
                    "parent_permissions": ["filesystem.write"],
                    "approval_required": True,
                    "approval_record": "approval://runtime-effect-probe/expired-preview",
                    "approval_scope": "deployment_preview:synthetic-only",
                    "approval_expiry": "expired:2026-07-01T00:00:00Z",
                    "effect_lease": "lease://runtime-effect-probe/expired-approval-001",
                    "authority_handle": "handle://runtime-effect-probe/expired-approval-001",
                    "sandbox_mode": "python_tempdir_workspace",
                    "impact_class": "high_impact",
                    "risk_tier": "high",
                },
            ),
        ]

    pass_state = (
        valid["decision"] == "dispatch"
        and valid["effect_executed"] is True
        and valid["rollback_executed"] is True
        and valid["checks"]["post_changed"] is True
        and valid["checks"]["rollback_exact"] is True
        and all(control["decision"] == "deny" for control in controls)
        and all(control["checks"]["blocked_before_mutation"] for control in controls)
        and all(control["checks"]["state_unchanged"] for control in controls)
    )
    return no_path_payload(
        {
            "schema_version": "0.1",
            "probe_id": PROBE_ID,
            "record_kind": "runtime_adapter_effect_replay_probe",
            "recorded_at_utc": datetime.now(timezone.utc)
            .replace(microsecond=0)
            .isoformat()
            .replace("+00:00", "Z"),
            "command": RESULT_COMMAND,
            "local_only": True,
            "public_safety_boundary": "Generated public-safe temp-file bytes only; no repository file, network target, secret, private source, or external service is mutated.",
            "support_state_effect": "none",
            "chapter_core_support_effect": "none",
            "evidence_transition_created": False,
            "pass": pass_state,
            "input_generator": "scripts/run_runtime_adapter_effect_probe.py::initial_bytes/appended_bytes",
            "fixture_template_ref": "experiments/runtime_adapter_permissions/fixtures/valid_low_impact_local_write.json",
            "valid_scenario": valid,
            "expected_invalid_controls": controls,
            "non_claims": NON_CLAIMS,
        }
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a public-safe runtime-adapter temp-file effect replay probe.")
    parser.add_argument("--write-result", action="store_true", help=f"write {RESULT.relative_to(ROOT)}")
    args = parser.parse_args()

    record = build_record()
    text = json.dumps(record, indent=2, sort_keys=True, ensure_ascii=True) + "\n"
    if args.write_result:
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(text, encoding="utf-8")
        print(f"Wrote {RESULT.relative_to(ROOT)}")
    else:
        print(text, end="")
    if not record.get("pass"):
        sys.exit(1)


if __name__ == "__main__":
    main()
