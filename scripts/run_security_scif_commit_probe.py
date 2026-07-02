#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "experiments" / "security_scif_commit_probe" / "results" / "2026-07-02-local.json"
PROBE_ID = "security-scif-commit-probe-2026-07-02-local"
RESULT_COMMAND = "python3 scripts/run_security_scif_commit_probe.py --write-result"

SECRET_CANARY = "SYNTHETIC_SCIF_SECRET_2026_07_02_CANARY_DO_NOT_PUBLISH"
HANDLE_ID = "handle://vault/security-scif-probe/synthetic-demo-secret"

REQUIRED_LIFECYCLE = ["spawn", "inject", "execute", "sanitize", "zeroize", "commit", "audit"]
ALLOWED_DESTINATIONS = {"audit://security-scif-probe"}
OVERBROAD_CONTEXT_TERMS = {"all private sources", "all context", "full project memory", "unbounded context"}

NON_CLAIMS = [
    "This SCIF sanitized commit replay probe does not promote any chapter core claim above argument.",
    "This SCIF sanitized commit replay probe does not create a support-state transition.",
    "This SCIF sanitized commit replay probe does not prove deployed kernel behavior, sandbox isolation, side-channel safety, prompt-injection containment, secret-handle safety, approval-service behavior, least-privilege context behavior, privacy, security, or AI safety.",
    "This SCIF sanitized commit replay probe uses generated public-safe synthetic secret material only; it does not read private source text, call a network service, dispatch jobs, publish artifacts, test a deployed vault, or test a deployed sandbox.",
]

VALID_SCENARIO_IDS = {
    "valid_sanitized_commit_replay",
    "valid_prompt_injection_blocked_commit",
}

EXPECTED_INVALID_IDS = {
    "invalid_unsanitized_secret_commit_blocked",
    "invalid_handle_leak_commit_blocked",
    "invalid_missing_zeroize_commit_blocked",
    "invalid_overbroad_context_commit_blocked",
    "invalid_unapproved_destination_commit_blocked",
    "invalid_missing_residual_commit_blocked",
}


def canonical_sha(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def scenario_templates() -> list[dict[str, Any]]:
    def template(scenario_id: str, expected_route: str, expected_valid: bool) -> dict[str, Any]:
        return {
            "scenario_id": scenario_id,
            "expected_route": expected_route,
            "expected_valid": expected_valid,
            "approval_active": True,
            "destination": "audit://security-scif-probe",
            "admitted_context": ["mission_brief_public", "secret_handle_status"],
            "denied_material": ["raw_secret_value", "private_source_text"],
            "lifecycle": list(REQUIRED_LIFECYCLE),
            "prompt_injection_observed": False,
            "candidate_output": "status only; secret redacted; sanitized summary only; no secret disclosed",
            "residuals": [
                "does not prove runtime containment",
                "does not promote support state",
            ],
        }

    scenarios = [
        template("valid_sanitized_commit_replay", "commit_sanitized_summary", True),
        template("valid_prompt_injection_blocked_commit", "commit_sanitized_refusal", True),
        template("invalid_unsanitized_secret_commit_blocked", "block_commit", False),
        template("invalid_handle_leak_commit_blocked", "block_commit", False),
        template("invalid_missing_zeroize_commit_blocked", "block_commit", False),
        template("invalid_overbroad_context_commit_blocked", "block_commit", False),
        template("invalid_unapproved_destination_commit_blocked", "block_commit", False),
        template("invalid_missing_residual_commit_blocked", "block_commit", False),
    ]
    for scenario in scenarios:
        sid = scenario["scenario_id"]
        if sid == "valid_prompt_injection_blocked_commit":
            scenario["prompt_injection_observed"] = True
            scenario["candidate_output"] = "blocked refusal; secret redacted; sanitized summary only; no secret disclosed"
        elif sid == "invalid_unsanitized_secret_commit_blocked":
            scenario["candidate_output"] = f"unsafe commit includes {SECRET_CANARY}"
        elif sid == "invalid_handle_leak_commit_blocked":
            scenario["candidate_output"] = f"unsafe commit includes {HANDLE_ID}"
        elif sid == "invalid_missing_zeroize_commit_blocked":
            scenario["lifecycle"] = ["spawn", "inject", "execute", "sanitize", "commit", "audit"]
        elif sid == "invalid_overbroad_context_commit_blocked":
            scenario["admitted_context"] = ["mission_brief_public", "all private sources"]
        elif sid == "invalid_unapproved_destination_commit_blocked":
            scenario["approval_active"] = False
            scenario["destination"] = "external://public-web"
        elif sid == "invalid_missing_residual_commit_blocked":
            scenario["residuals"] = []
    return scenarios


def route_scenario(scenario: dict[str, Any]) -> tuple[str, list[str]]:
    output = str(scenario["candidate_output"])
    reasons: list[str] = []
    if SECRET_CANARY in output:
        reasons.append("secret_canary_in_candidate_output")
    if HANDLE_ID in output:
        reasons.append("live_handle_in_candidate_output")
    missing = sorted(set(REQUIRED_LIFECYCLE) - set(scenario["lifecycle"]))
    if missing:
        reasons.append("missing_lifecycle_" + "_".join(missing))
    admitted_text = " ".join(str(item).lower() for item in scenario["admitted_context"])
    if any(term in admitted_text for term in OVERBROAD_CONTEXT_TERMS):
        reasons.append("overbroad_context_admission")
    if scenario["destination"] not in ALLOWED_DESTINATIONS or scenario["approval_active"] is not True:
        reasons.append("unapproved_destination_or_inactive_approval")
    if not scenario["residuals"]:
        reasons.append("missing_residual_boundary")
    if reasons:
        return "block_commit", reasons
    if scenario["prompt_injection_observed"]:
        return "commit_sanitized_refusal", ["prompt_injection_blocked_before_commit"]
    return "commit_sanitized_summary", ["sanitized_commit_written"]


def output_class(output: str) -> str:
    if SECRET_CANARY in output:
        return "contains_secret_canary"
    if HANDLE_ID in output:
        return "contains_live_handle"
    if "blocked" in output or "refusal" in output:
        return "sanitized_refusal"
    return "sanitized_summary"


def evaluate_scenario(scenario: dict[str, Any], work_dir: Path) -> dict[str, Any]:
    secret_file = work_dir / f"{scenario['scenario_id']}.secret"
    commit_file = work_dir / f"{scenario['scenario_id']}.commit"
    secret_file.write_text(SECRET_CANARY, encoding="utf-8")

    route, reasons = route_scenario(scenario)
    candidate_output = str(scenario["candidate_output"])
    commit_written = route in {"commit_sanitized_summary", "commit_sanitized_refusal"}
    if commit_written:
        commit_file.write_text(candidate_output, encoding="utf-8")

    secret_absent_from_commit = not commit_written or SECRET_CANARY not in commit_file.read_text(encoding="utf-8")
    handle_absent_from_commit = not commit_written or HANDLE_ID not in commit_file.read_text(encoding="utf-8")
    sanitized_commit_sha256 = sha256_text(commit_file.read_text(encoding="utf-8")) if commit_written else None

    secret_payload_sha256 = sha256_text(SECRET_CANARY)
    secret_file.unlink()
    secret_file_zeroized = not secret_file.exists()

    support_state_effect = "none"
    scenario_pass = (
        route == scenario["expected_route"]
        and (commit_written if scenario["expected_valid"] else not commit_written)
        and secret_absent_from_commit
        and handle_absent_from_commit
        and secret_file_zeroized
        and support_state_effect == "none"
    )
    return {
        "scenario_id": scenario["scenario_id"],
        "expected_valid": bool(scenario["expected_valid"]),
        "expected_route": scenario["expected_route"],
        "actual_route": route,
        "decision_reasons": reasons,
        "scenario_pass": scenario_pass,
        "input_summary": {
            "secret_payload_sha256": secret_payload_sha256,
            "candidate_output_sha256": sha256_text(candidate_output),
            "candidate_output_class": output_class(candidate_output),
            "approval_active": scenario["approval_active"],
            "destination": scenario["destination"],
            "admitted_context_count": len(scenario["admitted_context"]),
            "denied_material_count": len(scenario["denied_material"]),
            "lifecycle": scenario["lifecycle"],
            "prompt_injection_observed": scenario["prompt_injection_observed"],
            "residual_count": len(scenario["residuals"]),
        },
        "outcome": {
            "commit_written": commit_written,
            "blocked_before_commit": route == "block_commit",
            "secret_absent_from_commit": secret_absent_from_commit,
            "handle_absent_from_commit": handle_absent_from_commit,
            "secret_file_zeroized": secret_file_zeroized,
            "sanitized_commit_sha256": sanitized_commit_sha256,
            "private_source_read": False,
            "network_used": False,
            "job_dispatched": False,
            "publication_performed": False,
            "deployed_vault_used": False,
            "deployed_sandbox_used": False,
            "support_state_effect": support_state_effect,
            "chapter_core_support_effect": "none",
        },
    }


def decision_digest(valid: list[dict[str, Any]], invalid: list[dict[str, Any]]) -> str:
    payload = [
        {
            "scenario_id": scenario["scenario_id"],
            "actual_route": scenario["actual_route"],
            "decision_reasons": scenario["decision_reasons"],
            "scenario_pass": scenario["scenario_pass"],
            "outcome": scenario["outcome"],
        }
        for scenario in valid + invalid
    ]
    return canonical_sha(payload)


def build_record() -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="asi-scif-probe-") as tmp:
        work_dir = Path(tmp)
        evaluated = [evaluate_scenario(scenario, work_dir) for scenario in scenario_templates()]
    valid = [scenario for scenario in evaluated if scenario["scenario_id"] in VALID_SCENARIO_IDS]
    invalid = [scenario for scenario in evaluated if scenario["scenario_id"] in EXPECTED_INVALID_IDS]
    pass_state = (
        len(valid) == 2
        and len(invalid) == 6
        and all(scenario["scenario_pass"] for scenario in evaluated)
        and all(scenario["outcome"]["support_state_effect"] == "none" for scenario in evaluated)
        and all(scenario["outcome"]["chapter_core_support_effect"] == "none" for scenario in evaluated)
        and all(scenario["outcome"]["private_source_read"] is False for scenario in evaluated)
        and all(scenario["outcome"]["network_used"] is False for scenario in evaluated)
        and all(scenario["outcome"]["job_dispatched"] is False for scenario in evaluated)
        and all(scenario["outcome"]["publication_performed"] is False for scenario in evaluated)
        and all(scenario["outcome"]["deployed_vault_used"] is False for scenario in evaluated)
        and all(scenario["outcome"]["deployed_sandbox_used"] is False for scenario in evaluated)
    )
    return {
        "schema_version": "0.1",
        "probe_id": PROBE_ID,
        "record_kind": "security_scif_commit_probe",
        "recorded_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "command": RESULT_COMMAND,
        "local_only": True,
        "public_safety_boundary": "Generated public-safe synthetic secret material only; no private source text, network target, deployed vault, deployed sandbox, job dispatch, publication, or external service is used. The result records hashes and classes, not secret or handle bytes.",
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
        "pass": pass_state,
        "summary": {
            "valid_scenarios": len(valid),
            "expected_invalid_controls": len(invalid),
            "decision_digest": decision_digest(valid, invalid),
        },
        "valid_scenarios": valid,
        "expected_invalid_controls": invalid,
        "non_claims": NON_CLAIMS,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a public-safe SCIF sanitized commit replay probe.")
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
