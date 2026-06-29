#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

from validate_protocol_examples import validate_value


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "experiments" / "circle_external_receipt_slice" / "results" / "2026-06-29-local.json"
SUMMARY = ROOT / "docs" / "circle_external_receipt_slice.md"
TRANSITION = (
    ROOT
    / "evidence_transitions"
    / "v1_0_measured"
    / "circle_external_rope_receipt_prototype_backed.json"
)
SCHEMA = ROOT / "schemas" / "evidence_transition_record.schema.json"

EXPECTED_COMMANDS = (
    "lake build Circle",
    "python3 scripts/circle_ai_certify.py rope --model-config examples/circle_ai_model_configs/standard_rope_config.json --requested-margin 1/328459 --format json --require-status proved --require-decision passed --require-assurance mixed_theorem_and_computation --require-passed",
    "PYTHONPATH=. python3 scripts/circle_ai_contract_ready.py --kind rope_position_distinguishability --digest --include-recommendations",
    "PYTHONPATH=. python3 scripts/circle_ai_contract_ready.py --kind rope_position_distinguishability --receipt --format json --field d19_proved_request_status --field d19_proved_first_channel_bank_transfer --field real_phase_dirichlet_witness_guardrail --require-theorem AIRA-T0058 --require-theorem AIRA-T0059 --require-theorem AIRA-T0171 --require-theorem AIRA-T0172 --require-theorem AIRA-T0239 --require-theorem AIRA-T0240 --require-theorem AIRA-T0241 --require-recommendation ROPE-USE-D19-MARGIN-FRONTIER",
    "PYTHONPATH=. python3 -m pytest tests/test_check_circle_ai_receipt.py tests/test_check_circle_ai_certification_bundle.py tests/test_check_circle_ai_receipt_replay.py tests/test_check_circle_ai_contract_runner.py tests/test_downstream_ci_accept_circle_ai_contracts.py tests/test_theseus_hive_ai_contracts.py tests/test_circle_ai_contract_ready_cli.py tests/test_circle_ai_contract_pack.py -q",
)

REQUIRED_THEOREMS = (
    "AIRA-T0058",
    "AIRA-T0059",
    "AIRA-T0171",
    "AIRA-T0172",
    "AIRA-T0239",
    "AIRA-T0240",
    "AIRA-T0241",
)

REQUIRED_NON_CLAIMS = (
    "does not promote any chapter core claim",
    "does not prove model quality, reasoning ability, context length, speed, memory scaling, deployment safety, transfer, or ASI",
    "does not prove deployed proof-contract transport inside The ASI Stack",
)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Circle external receipt slice validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def text_blob(value: Any) -> str:
    if isinstance(value, dict):
        return "\n".join(f"{key}: {child}" for key, child in value.items())
    if isinstance(value, list):
        return "\n".join(str(item) for item in value)
    return str(value)


def validate_result(result: dict[str, Any], errors: list[str]) -> None:
    expected = {
        "schema_version": "0.1",
        "result_id": "2026-06-29-local-circle-external-rope-receipt-slice",
        "slice_id": "circle_external_rope_receipt_slice",
        "claim_id": "circle-calculus.external_rope_receipt_replay",
        "verification_result": "pass",
    }
    for key, value in expected.items():
        if result.get(key) != value:
            errors.append(f"{rel(RESULT)}: {key} must be {value!r}.")

    project = result.get("external_project")
    if not isinstance(project, dict):
        errors.append(f"{rel(RESULT)}: external_project must be an object.")
    else:
        if project.get("git_commit") != "63b0f511":
            errors.append(f"{rel(RESULT)}: external_project.git_commit must be '63b0f511'.")
        if project.get("worktree_state") != "clean_after_commands":
            errors.append(f"{rel(RESULT)}: external_project.worktree_state must record a clean final state.")

    commands = result.get("commands")
    if not isinstance(commands, list) or len(commands) != len(EXPECTED_COMMANDS):
        errors.append(f"{rel(RESULT)}: commands must list exactly {len(EXPECTED_COMMANDS)} accepted commands.")
        commands = []
    observed_commands = [item.get("command") for item in commands if isinstance(item, dict)]
    for command in EXPECTED_COMMANDS:
        if command not in observed_commands:
            errors.append(f"{rel(RESULT)} missing accepted command: {command}")
    for index, item in enumerate(commands):
        if not isinstance(item, dict):
            errors.append(f"{rel(RESULT)}: commands[{index}] must be an object.")
            continue
        if item.get("verification_result") != "pass":
            errors.append(f"{rel(RESULT)}: commands[{index}] must have verification_result pass.")

    result_text = text_blob(result)
    required_fragments = (
        "Build completed successfully (2624 jobs).",
        "status proved",
        "request_passed true",
        "theorem_count 55",
        "ready=True fields=31 missing=0 theorems=75",
        "145 passed in 718.24s (0:11:58)",
        "91b72a6dcf821a9733f21800cd1093a3d0665588022031ba72c94893800330c3",
        "20e68c5f787e267c6611bc57b8d8e98e1cb0f5a74f272379716a5d83e761407d",
        "df673f8a661fc89a26372685986c92f2221aaa617d6738fce5c2a76bd5d0eeae",
        "a0f35d3e89e9b6eac555f0392450f4f75cf7e70f30cff44ec7434f61bd85b468",
        "ROPE-USE-D19-MARGIN-FRONTIER",
    )
    for fragment in required_fragments:
        if fragment not in result_text:
            errors.append(f"{rel(RESULT)} missing required result fragment: {fragment}")
    for theorem_id in REQUIRED_THEOREMS:
        if theorem_id not in result_text:
            errors.append(f"{rel(RESULT)} missing required theorem id: {theorem_id}")

    discarded = result.get("discarded_attempts")
    if not isinstance(discarded, list) or len(discarded) != 2:
        errors.append(f"{rel(RESULT)} must record the two discarded procedural attempts.")
    else:
        discarded_text = text_blob(discarded)
        for fragment in (
            "tests/test_check_circle_ai_contract_pack.py",
            "no tests ran",
            "ModuleNotFoundError",
            "PYTHONPATH=.",
        ):
            if fragment not in discarded_text:
                errors.append(f"{rel(RESULT)} discarded attempts missing fragment: {fragment}")

    support = result.get("support_transition")
    if not isinstance(support, dict):
        errors.append(f"{rel(RESULT)}: support_transition must be an object.")
    else:
        if support.get("old_support_state") != "argument":
            errors.append(f"{rel(RESULT)}: support_transition.old_support_state must be argument.")
        if support.get("new_support_state") != "prototype-backed":
            errors.append(f"{rel(RESULT)}: support_transition.new_support_state must be prototype-backed.")
        if support.get("support_state_effect") != "eligible_for_bounded_evidence_review":
            errors.append(
                f"{rel(RESULT)}: support_transition.support_state_effect must be eligible_for_bounded_evidence_review."
            )

    validate_non_claims(rel(RESULT), result.get("non_claims"), errors)


def validate_non_claims(owner: str, value: Any, errors: list[str]) -> None:
    blob = text_blob(value)
    if not isinstance(value, list) or not value:
        errors.append(f"{owner}: non_claims must be a non-empty list.")
        return
    for phrase in REQUIRED_NON_CLAIMS:
        if phrase not in blob:
            errors.append(f"{owner}: non_claims missing boundary phrase {phrase!r}.")


def validate_summary(errors: list[str]) -> None:
    if not SUMMARY.exists():
        errors.append(f"Missing {rel(SUMMARY)}.")
        return
    text = SUMMARY.read_text(encoding="utf-8")
    required_fragments = (
        "Circle External Receipt Slice",
        "circle-calculus.external_rope_receipt_replay",
        "Support transition: `argument` to `prototype-backed`",
        "External checkout commit: `63b0f511`",
        "Build completed successfully (2624 jobs).",
        "ready=True",
        "fields=31 missing=0 theorems=75",
        "AIRA-T0058",
        "AIRA-T0241",
        "ROPE-USE-D19-MARGIN-FRONTIER",
        "145 passed in 718.24s (0:11:58)",
        "procedural command-selection error, not evidence",
        "ModuleNotFoundError",
        "Does not promote any chapter core claim above `argument`.",
        "Does not prove model quality, reasoning ability, context length, speed",
    )
    for fragment in required_fragments:
        if fragment not in text:
            errors.append(f"{rel(SUMMARY)} missing required fragment: {fragment}")


def validate_transition(errors: list[str]) -> None:
    if not TRANSITION.exists():
        errors.append(f"Missing {rel(TRANSITION)}.")
        return
    value = load_json(TRANSITION)
    if not isinstance(value, dict):
        errors.append(f"{rel(TRANSITION)} must contain an object.")
        return
    schema = load_json(SCHEMA)
    errors.extend(validate_value(value, schema, rel(TRANSITION)))
    expected = {
        "transition_id": "v1_0_measured.circle_external_rope_receipt.prototype_backed",
        "claim_id": "circle-calculus.external_rope_receipt_replay",
        "old_support_state": "argument",
        "new_support_state": "prototype-backed",
        "transition_effect": "upward",
        "transition_validity_state": "review_accepted",
        "verification_result": "pass",
        "review_status": "accepted",
        "support_state_effect": "eligible_for_bounded_evidence_review",
    }
    for key, expected_value in expected.items():
        if value.get(key) != expected_value:
            errors.append(f"{rel(TRANSITION)}: {key} must be {expected_value!r}.")
    refs = (
        value.get("artifact_refs", [])
        + value.get("evidence_packet_refs", [])
        + value.get("claim_surface_refs", [])
        + value.get("claim_record_refs", [])
    )
    for ref in (rel(RESULT), rel(SUMMARY), "scripts/validate_circle_external_receipt_slice.py"):
        if ref not in refs:
            errors.append(f"{rel(TRANSITION)} must reference {ref}.")
    if value.get("acceptance_blockers"):
        errors.append(f"{rel(TRANSITION)} must not list acceptance blockers.")
    if not value.get("negative_results"):
        errors.append(f"{rel(TRANSITION)} must record negative_results.")
    transition_text = text_blob(value)
    for fragment in ("63b0f511", "CC-AI-CONTRACT-ROPE-001", "145 passing tests", "not vendored"):
        if fragment not in transition_text:
            errors.append(f"{rel(TRANSITION)} missing scoped transition fragment: {fragment}")
    validate_non_claims(rel(TRANSITION), value.get("non_claims"), errors)


def main() -> None:
    errors: list[str] = []
    if not RESULT.exists():
        fail([f"Missing {rel(RESULT)}."])
    result = load_json(RESULT)
    if not isinstance(result, dict):
        fail([f"{rel(RESULT)} must contain an object."])
    validate_result(result, errors)
    validate_summary(errors)
    validate_transition(errors)
    if errors:
        fail(errors)
    print("Circle external receipt slice validation passed.")


if __name__ == "__main__":
    main()
