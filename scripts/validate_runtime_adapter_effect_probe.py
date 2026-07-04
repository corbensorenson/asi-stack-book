#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

from run_runtime_adapter_effect_probe import (
    NON_CLAIMS,
    PROBE_ID,
    RESULT,
    RESULT_COMMAND,
    ROOT,
    appended_bytes,
    initial_bytes,
    sha256_bytes,
)


DOC = ROOT / "docs" / "runtime_adapter_effect_probe.md"
STRUCTURE = ROOT / "book_structure.json"
OUTLINE = ROOT / "docs" / "book_outline.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
LIVE_CHAPTER = ROOT / "chapters" / "runtime-adapters-tool-permissions-and-human-approval.qmd"
READER_CHAPTER = (
    ROOT
    / "editions"
    / "reader_manuscript"
    / "v1_0"
    / "chapters"
    / "runtime-adapters-tool-permissions-and-human-approval.qmd"
)
README = ROOT / "README.md"
PUBLICATION = ROOT / "docs" / "publication_readiness.md"
STATUS = ROOT / "docs" / "test_harness_status_ledger.md"

SURFACE_FRAGMENTS = (
    "Runtime adapter effect replay probe",
    "valid_low_impact_local_write_effect_replay",
    "invalid_missing_permission_no_mutation",
    "invalid_expired_approval_no_mutation",
    "rollback-exact",
    "support-state",
)

REQUIRED_NON_CLAIM_TERMS = (
    "does not promote any chapter core claim",
    "does not create a support-state transition",
    "deployed adapter behavior",
    "sandbox isolation",
    "approval-service behavior",
    "secret-handle safety",
    "rollback-service behavior",
    "policy-enforcement correctness",
    "benchmark performance",
    "does not copy file contents",
)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def text_blob(value: Any) -> str:
    if isinstance(value, dict):
        return "\n".join(f"{key}: {text_blob(child)}" for key, child in value.items())
    if isinstance(value, list):
        return "\n".join(text_blob(item) for item in value)
    return str(value)


def normalize(text: str) -> str:
    return " ".join(text.lower().split())


def require_fragments(owner: str, text: str, fragments: tuple[str, ...], errors: list[str]) -> None:
    normalized = normalize(text)
    for fragment in fragments:
        if normalize(fragment) not in normalized:
            errors.append(f"{owner} missing required fragment: {fragment}")


def chapter_record(structure: dict[str, Any], chapter_id: str) -> dict[str, Any]:
    for part in structure.get("parts", []):
        if not isinstance(part, dict):
            continue
        for chapter in part.get("chapters", []):
            if isinstance(chapter, dict) and chapter.get("id") == chapter_id:
                return chapter
    return {}


def fail(errors: list[str]) -> None:
    print("Runtime adapter effect replay probe validation failed:", file=sys.stderr)
    for error in errors:
        print(f" - {error}", file=sys.stderr)
    raise SystemExit(1)


def require_sha(value: Any, owner: str, errors: list[str]) -> None:
    if not re.fullmatch(r"[0-9a-f]{64}", str(value)):
        errors.append(f"{owner} must be a SHA-256 hex digest.")


def main() -> None:
    errors: list[str] = []
    paths = (RESULT, DOC, STRUCTURE, OUTLINE, ROADMAP, LIVE_CHAPTER, READER_CHAPTER, README, PUBLICATION, STATUS)
    for path in paths:
        if not path.exists():
            errors.append(f"Missing {rel(path)}.")
    if errors:
        fail(errors)

    result = load_json(RESULT)
    structure = load_json(STRUCTURE)
    blob = text_blob(result)
    if "/Users/" in blob or "/var/folders/" in blob:
        errors.append(f"{rel(RESULT)} must not publish local absolute paths.")

    expected_before = initial_bytes()
    expected_append = appended_bytes()
    expected_after = expected_before + expected_append

    expected_scalars = {
        "probe_id": PROBE_ID,
        "record_kind": "runtime_adapter_effect_replay_probe",
        "command": RESULT_COMMAND,
        "local_only": True,
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
        "pass": True,
    }
    for key, expected in expected_scalars.items():
        if result.get(key) != expected:
            errors.append(f"{rel(RESULT)}: {key} must be {expected!r}.")
    if not isinstance(result.get("recorded_at_utc"), str) or not result["recorded_at_utc"].endswith("Z"):
        errors.append(f"{rel(RESULT)}: recorded_at_utc must end with Z.")

    valid = result.get("valid_scenario", {})
    if valid.get("scenario_id") != "valid_low_impact_local_write_effect_replay":
        errors.append(f"{rel(RESULT)}: valid scenario id mismatch.")
    if valid.get("decision") != "dispatch" or valid.get("effect_executed") is not True:
        errors.append(f"{rel(RESULT)}: valid scenario must dispatch and execute the temp-file effect.")
    if valid.get("rollback_executed") is not True:
        errors.append(f"{rel(RESULT)}: valid scenario must execute rollback.")
    checks = valid.get("checks", {})
    if checks.get("post_changed") is not True or checks.get("rollback_exact") is not True:
        errors.append(f"{rel(RESULT)}: valid scenario must record post_changed and rollback_exact.")
    if checks.get("repo_write") is not False or checks.get("network_used") is not False:
        errors.append(f"{rel(RESULT)}: valid scenario must not write the repo or use network.")
    states = valid.get("states", {})
    for state_name, payload in (("pre", expected_before), ("post", expected_after), ("rollback", expected_before)):
        state = states.get(state_name, {})
        if state.get("bytes") != len(payload):
            errors.append(f"{rel(RESULT)}: valid {state_name} byte count mismatch.")
        if state.get("sha256") != sha256_bytes(payload):
            errors.append(f"{rel(RESULT)}: valid {state_name} digest mismatch.")
        require_sha(state.get("sha256"), f"{rel(RESULT)} valid {state_name}.sha256", errors)
    receipt = valid.get("receipt", {})
    if not str(receipt.get("effect_receipt", "")).startswith("receipt://"):
        errors.append(f"{rel(RESULT)}: valid scenario must record receipt:// effect_receipt.")
    if not str(receipt.get("rollback_handle", "")).startswith("rollback://"):
        errors.append(f"{rel(RESULT)}: valid scenario must record rollback:// rollback_handle.")
    if receipt.get("support_state_effect") != "none" or receipt.get("chapter_core_support_effect") != "none":
        errors.append(f"{rel(RESULT)}: receipt must keep support effects at none.")

    controls = result.get("expected_invalid_controls", [])
    if not isinstance(controls, list) or len(controls) != 2:
        errors.append(f"{rel(RESULT)}: expected two invalid controls.")
        controls = []
    expected_control_reasons = {
        "invalid_missing_permission_no_mutation": "missing_parent_permission",
        "invalid_expired_approval_no_mutation": "expired_approval",
    }
    for control in controls:
        scenario_id = control.get("scenario_id")
        if scenario_id not in expected_control_reasons:
            errors.append(f"{rel(RESULT)}: unexpected control {scenario_id!r}.")
            continue
        if control.get("decision") != "deny":
            errors.append(f"{rel(RESULT)}: {scenario_id} must deny.")
        if control.get("decision_reason") != expected_control_reasons[scenario_id]:
            errors.append(f"{rel(RESULT)}: {scenario_id} reason mismatch.")
        if control.get("effect_executed") is not False:
            errors.append(f"{rel(RESULT)}: {scenario_id} must not execute effect.")
        control_checks = control.get("checks", {})
        if control_checks.get("blocked_before_mutation") is not True or control_checks.get("state_unchanged") is not True:
            errors.append(f"{rel(RESULT)}: {scenario_id} must block before mutation and preserve state.")
        if control_checks.get("repo_write") is not False or control_checks.get("network_used") is not False:
            errors.append(f"{rel(RESULT)}: {scenario_id} must not write the repo or use network.")
        control_states = control.get("states", {})
        for state_name in ("pre", "post"):
            state = control_states.get(state_name, {})
            if state.get("bytes") != len(expected_before):
                errors.append(f"{rel(RESULT)}: {scenario_id} {state_name} byte count mismatch.")
            if state.get("sha256") != sha256_bytes(expected_before):
                errors.append(f"{rel(RESULT)}: {scenario_id} {state_name} digest mismatch.")

    if result.get("non_claims") != NON_CLAIMS:
        errors.append(f"{rel(RESULT)}: non_claims must match runner boundaries.")
    require_fragments(rel(RESULT), text_blob(result.get("non_claims", [])), REQUIRED_NON_CLAIM_TERMS, errors)

    for owner, path in (
        (rel(DOC), DOC),
        (rel(OUTLINE), OUTLINE),
        (rel(ROADMAP), ROADMAP),
        (rel(LIVE_CHAPTER), LIVE_CHAPTER),
        (rel(READER_CHAPTER), READER_CHAPTER),
        (rel(README), README),
        (rel(PUBLICATION), PUBLICATION),
        (rel(STATUS), STATUS),
    ):
        require_fragments(owner, path.read_text(encoding="utf-8"), SURFACE_FRAGMENTS, errors)

    record = chapter_record(structure, "runtime-adapters-tool-permissions-and-human-approval")
    if record.get("evidence_level") != "argument":
        errors.append("runtime-adapters-tool-permissions-and-human-approval: evidence_level must remain argument.")
    require_fragments(
        "book_structure runtime adapter tests",
        text_blob(record.get("codex_tests", [])),
        (
            "Runtime adapter effect replay probe",
            "valid_low_impact_local_write_effect_replay",
            "missing-permission and expired-approval no-mutation controls",
            "no deployed-adapter, sandbox, approval-service, secret-handle, rollback-service, policy-enforcement, benchmark, or support-state-promotion claim",
        ),
        errors,
    )

    if errors:
        fail(errors)
    print(
        "Runtime adapter effect replay probe validation passed: "
        "temp-file write, rollback-exact restoration, missing-permission denial, and expired-approval denial checked."
    )


if __name__ == "__main__":
    main()
