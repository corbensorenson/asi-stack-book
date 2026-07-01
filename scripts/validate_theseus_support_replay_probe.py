#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import re
import sys
from typing import Any

from run_theseus_support_replay_probe import (
    NON_CLAIMS,
    PROBE_ID,
    REPLAY_COMMANDS,
    RESULT,
    RESULT_COMMAND,
    ROOT,
    TRACKED_ARTIFACTS,
    artifact_stat,
    run_replay_command,
)


DOC = ROOT / "docs" / "theseus_support_replay_probe.md"
SHA_RE = re.compile(r"^[0-9a-f]{64}$")
REQUIRED_NON_CLAIM_TERMS = (
    "does not promote any chapter core claim",
    "does not create a support-state transition",
    "does not rerun project theseus",
    "public-safe static imports only",
)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Theseus support replay probe validation failed:")
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


def validate_record_shape(value: dict[str, Any], errors: list[str]) -> None:
    expected_scalars = {
        "probe_id": PROBE_ID,
        "record_kind": "theseus_support_replay_probe",
        "command": RESULT_COMMAND,
        "local_only": True,
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
        "pass": True,
    }
    for key, expected in expected_scalars.items():
        if value.get(key) != expected:
            errors.append(f"{rel(RESULT)}: {key} must be {expected!r}.")

    if not isinstance(value.get("recorded_at_utc"), str) or not value["recorded_at_utc"].endswith("Z"):
        errors.append(f"{rel(RESULT)}: recorded_at_utc must be a UTC timestamp ending in Z.")

    summary = value.get("summary")
    if not isinstance(summary, str) or "architecture-gate import and generation-mode import validators" not in summary:
        errors.append(f"{rel(RESULT)}: summary must describe the two public-safe Theseus validator replays.")

    artifact_refs = value.get("artifact_refs")
    if not isinstance(artifact_refs, list):
        errors.append(f"{rel(RESULT)}: artifact_refs must be a list.")
        artifact_refs = []
    expected_refs = [*TRACKED_ARTIFACTS, rel(RESULT)]
    if artifact_refs != expected_refs:
        errors.append(f"{rel(RESULT)}: artifact_refs must match the tracked Theseus support replay surface.")
    for relative in expected_refs:
        if not (ROOT / relative).exists():
            errors.append(f"{rel(RESULT)}: referenced artifact does not exist: {relative}")

    non_claims = value.get("non_claims")
    if non_claims != NON_CLAIMS:
        errors.append(f"{rel(RESULT)}: non_claims must match the runner's explicit non-claim boundaries.")
    non_claim_text = text_blob(non_claims)
    for term in REQUIRED_NON_CLAIM_TERMS:
        if term not in non_claim_text:
            errors.append(f"{rel(RESULT)}: non_claims missing boundary phrase {term!r}.")


def validate_replay_commands(value: dict[str, Any], errors: list[str]) -> None:
    commands = value.get("replay_commands")
    if not isinstance(commands, list):
        errors.append(f"{rel(RESULT)}: replay_commands must be a list.")
        return
    if len(commands) != len(REPLAY_COMMANDS):
        errors.append(f"{rel(RESULT)}: expected {len(REPLAY_COMMANDS)} replay commands, found {len(commands)}.")
        return

    for index, (expected, recorded) in enumerate(zip(REPLAY_COMMANDS, commands)):
        owner = f"{rel(RESULT)}:replay_commands[{index}]"
        if not isinstance(recorded, dict):
            errors.append(f"{owner}: command record must be an object.")
            continue
        for key in ("id", "command", "evidence_surface"):
            if recorded.get(key) != expected[key]:
                errors.append(f"{owner}: {key} must be {expected[key]!r}.")
        if recorded.get("exit_code") != 0:
            errors.append(f"{owner}: exit_code must be 0.")
        if not isinstance(recorded.get("elapsed_ms"), (int, float)) or recorded["elapsed_ms"] <= 0:
            errors.append(f"{owner}: elapsed_ms must be a positive measured number.")
        if not isinstance(recorded.get("output_sha256"), str) or not SHA_RE.match(recorded["output_sha256"]):
            errors.append(f"{owner}: output_sha256 must be a SHA-256 hex digest.")
        excerpt = recorded.get("output_excerpt")
        if not isinstance(excerpt, list) or not excerpt:
            errors.append(f"{owner}: output_excerpt must be a non-empty list.")
        replayed = run_replay_command(expected)
        if replayed["exit_code"] != 0:
            errors.append(f"{owner}: current replay of {expected['command']} failed.")
        if replayed["output_sha256"] != recorded.get("output_sha256"):
            errors.append(
                f"{owner}: current replay output digest differs from recorded digest for {expected['command']}."
            )


def validate_tracked_artifacts(value: dict[str, Any], errors: list[str]) -> None:
    tracked = value.get("tracked_artifacts")
    if not isinstance(tracked, list):
        errors.append(f"{rel(RESULT)}: tracked_artifacts must be a list.")
        return
    if len(tracked) != len(TRACKED_ARTIFACTS):
        errors.append(f"{rel(RESULT)}: expected {len(TRACKED_ARTIFACTS)} tracked artifact stats, found {len(tracked)}.")
        return

    for index, (relative, recorded) in enumerate(zip(TRACKED_ARTIFACTS, tracked)):
        owner = f"{rel(RESULT)}:tracked_artifacts[{index}]"
        if not isinstance(recorded, dict):
            errors.append(f"{owner}: artifact stat must be an object.")
            continue
        current = artifact_stat(relative)
        for key, expected in current.items():
            if recorded.get(key) != expected:
                errors.append(f"{owner}: {key} must match current {relative} value {expected!r}.")
        if not SHA_RE.match(str(recorded.get("sha256", ""))):
            errors.append(f"{owner}: sha256 must be a SHA-256 hex digest.")


def validate_doc(errors: list[str]) -> None:
    if not DOC.exists():
        errors.append(f"Missing {rel(DOC)}.")
        return
    text = DOC.read_text(encoding="utf-8")
    normalized_text = re.sub(r"\s+", " ", text)
    required = [
        "Theseus Support Replay Probe",
        RESULT_COMMAND,
        rel(RESULT),
        "two public-safe Project Theseus validators",
        "Support-state effect | `none`",
        "Chapter-core support effect | `none`",
        "This is not a clean live Theseus replay",
        "does not promote any chapter core claim above `argument`",
    ]
    for fragment in required:
        haystack = normalized_text if " " in fragment else text
        if fragment not in haystack:
            errors.append(f"{rel(DOC)} missing required fragment: {fragment}")


def main() -> None:
    errors: list[str] = []
    if not RESULT.exists():
        fail([f"Missing {rel(RESULT)}. Run `{RESULT_COMMAND}` first."])
    value = load_json(RESULT)
    if not isinstance(value, dict):
        fail([f"{rel(RESULT)} must contain a JSON object."])

    validate_record_shape(value, errors)
    validate_replay_commands(value, errors)
    validate_tracked_artifacts(value, errors)
    validate_doc(errors)

    if errors:
        fail(errors)
    print(
        "Theseus support replay probe validation passed: "
        f"{len(REPLAY_COMMANDS)} local command replay(s), "
        f"{len(TRACKED_ARTIFACTS)} tracked artifact digest(s), support-state effect none."
    )


if __name__ == "__main__":
    main()
