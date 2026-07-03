#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import re
import sys
from typing import Any

from run_theseus_fast_support_lane import (
    LANE_ID,
    NON_CLAIMS,
    REPLAY_COMMANDS,
    RESULT,
    RESULT_COMMAND,
    ROOT,
    TRACKED_ARTIFACTS,
    aggregate_summary,
    artifact_stat,
    run_replay_command,
)


DOC = ROOT / "docs" / "theseus_fast_support_lane_run.md"
ACTIVE_CYCLE = ROOT / "docs" / "v1_x_active_evidence_cycle.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
OUTLINE = ROOT / "docs" / "book_outline.md"
FAST_CHAPTER = ROOT / "chapters" / "fast-generation-architectures.qmd"
THESEUS_CHAPTER = ROOT / "chapters" / "project-theseus-as-report-first-implementation-reference.qmd"
FAST_READER = ROOT / "editions" / "reader_manuscript" / "v1_0" / "chapters" / "fast-generation-architectures.qmd"
THESEUS_READER = ROOT / "editions" / "reader_manuscript" / "v1_0" / "chapters" / "project-theseus-as-report-first-implementation-reference.qmd"
LEAN = ROOT / "lean" / "AsiStackProofs" / "TheseusReference.lean"

SHA_RE = re.compile(r"^[0-9a-f]{64}$")
LEAN_THEOREMS = [
    "theseus_fast_support_aggregate_fixture_valid",
    "theseus_fast_support_aggregate_preserves_no_promotion",
    "theseus_fast_support_aggregate_carries_task_and_control_counts",
    "theseus_fast_support_aggregate_clean_replay_overclaim_rejected",
]
SURFACE_PHRASES = [
    LANE_ID,
    "python3 scripts/validate_theseus_fast_support_lane.py",
    "theseusFastSupportAggregateFixture",
    "68 public task records",
    "14 expected-invalid or rejected controls",
    "does not prove clean live Project Theseus replay",
    "does not prove model quality",
    "does not promote any chapter core claim",
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Theseus/Fast support-lane validation failed:")
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


def validate_record_shape(record: dict[str, Any], errors: list[str]) -> None:
    expected = {
        "lane_id": LANE_ID,
        "record_kind": "theseus_fast_support_lane",
        "command": RESULT_COMMAND,
        "local_only": True,
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
        "pass": True,
    }
    for key, value in expected.items():
        if record.get(key) != value:
            errors.append(f"{rel(RESULT)}: {key} must be {value!r}.")
    if not isinstance(record.get("recorded_at_utc"), str) or not record["recorded_at_utc"].endswith("Z"):
        errors.append(f"{rel(RESULT)}: recorded_at_utc must be a UTC timestamp ending in Z.")
    if record.get("selected_support_lanes") != [
        "project-theseus-as-report-first-implementation-reference",
        "fast-generation-architectures",
    ]:
        errors.append(f"{rel(RESULT)}: selected_support_lanes must name exactly the current two support lanes.")
    if record.get("non_claims") != NON_CLAIMS:
        errors.append(f"{rel(RESULT)}: non_claims must match the runner boundaries.")
    non_claim_text = text_blob(record.get("non_claims", []))
    for phrase in (
        "does not prove clean live project theseus replay",
        "does not prove model quality",
        "does not promote any chapter core claim above argument",
    ):
        if phrase not in non_claim_text:
            errors.append(f"{rel(RESULT)}: non_claims missing phrase {phrase!r}.")


def validate_replay_commands(record: dict[str, Any], errors: list[str]) -> None:
    commands = record.get("replay_commands")
    if not isinstance(commands, list):
        errors.append(f"{rel(RESULT)}: replay_commands must be a list.")
        return
    if len(commands) != len(REPLAY_COMMANDS):
        errors.append(f"{rel(RESULT)}: expected {len(REPLAY_COMMANDS)} replay commands, found {len(commands)}.")
        return
    for index, (expected, observed) in enumerate(zip(REPLAY_COMMANDS, commands)):
        owner = f"{rel(RESULT)}:replay_commands[{index}]"
        if not isinstance(observed, dict):
            errors.append(f"{owner}: command record must be an object.")
            continue
        for key in ("id", "command", "evidence_surface"):
            if observed.get(key) != expected[key]:
                errors.append(f"{owner}: {key} must be {expected[key]!r}.")
        if observed.get("exit_code") != 0:
            errors.append(f"{owner}: exit_code must be 0.")
        if not isinstance(observed.get("elapsed_ms"), (int, float)) or observed["elapsed_ms"] <= 0:
            errors.append(f"{owner}: elapsed_ms must be positive.")
        if not isinstance(observed.get("output_sha256"), str) or not SHA_RE.match(observed["output_sha256"]):
            errors.append(f"{owner}: output_sha256 must be a SHA-256 hex digest.")
        replayed = run_replay_command(expected)
        if replayed["exit_code"] != 0:
            errors.append(f"{owner}: current replay of {expected['command']} failed.")
        if replayed["output_sha256"] != observed.get("output_sha256"):
            errors.append(f"{owner}: current replay output digest differs for {expected['command']}.")


def validate_tracked_artifacts(record: dict[str, Any], errors: list[str]) -> None:
    refs = record.get("artifact_refs")
    expected_refs = [*TRACKED_ARTIFACTS, rel(RESULT)]
    if refs != expected_refs:
        errors.append(f"{rel(RESULT)}: artifact_refs must match tracked support-lane artifacts.")
    tracked = record.get("tracked_artifacts")
    if not isinstance(tracked, list):
        errors.append(f"{rel(RESULT)}: tracked_artifacts must be a list.")
        return
    if len(tracked) != len(TRACKED_ARTIFACTS):
        errors.append(f"{rel(RESULT)}: expected {len(TRACKED_ARTIFACTS)} tracked artifacts, found {len(tracked)}.")
        return
    for index, (relative, observed) in enumerate(zip(TRACKED_ARTIFACTS, tracked)):
        owner = f"{rel(RESULT)}:tracked_artifacts[{index}]"
        if not isinstance(observed, dict):
            errors.append(f"{owner}: artifact stat must be an object.")
            continue
        current = artifact_stat(relative)
        for key, value in current.items():
            if observed.get(key) != value:
                errors.append(f"{owner}: {key} must match current {relative} value {value!r}.")
        if not SHA_RE.match(str(observed.get("sha256", ""))):
            errors.append(f"{owner}: sha256 must be a SHA-256 hex digest.")


def validate_lean_alignment(record: dict[str, Any], errors: list[str]) -> None:
    alignment = record.get("aggregate_lean_alignment")
    if not isinstance(alignment, dict):
        errors.append(f"{rel(RESULT)}: aggregate_lean_alignment must be an object.")
        return
    expected = {
        "lean_module": "lean/AsiStackProofs/TheseusReference.lean",
        "fixture_def": "theseusFastSupportAggregateFixture",
        "proof_tag": "lean:theseus.reference.fast_support_aggregate.fixture_bridge",
        "checked_theorem_names": LEAN_THEOREMS,
        **aggregate_summary(),
    }
    for key, value in expected.items():
        if alignment.get(key) != value:
            errors.append(f"{rel(RESULT)}: aggregate_lean_alignment.{key} must be {value!r}.")
    lean_text = LEAN.read_text(encoding="utf-8", errors="ignore")
    for fragment in (
        "structure TheseusFastSupportAggregateSummary",
        "def theseusFastSupportAggregateFixture",
        "supportLaneCount := 2",
        "commandReplayCount := 4",
        "trackedArtifactCount := 16",
        "publicTaskCount := 68",
        "expectedInvalidOrRejectedControlCount := 14",
        "noPromotionDecisionCount := 2",
    ):
        if fragment not in lean_text:
            errors.append(f"{rel(LEAN)} missing Lean aggregate fragment {fragment!r}.")
    for theorem in LEAN_THEOREMS:
        if theorem not in lean_text:
            errors.append(f"{rel(LEAN)} missing theorem {theorem}.")


def validate_surfaces(errors: list[str]) -> None:
    surfaces = {
        rel(DOC): DOC,
        rel(ACTIVE_CYCLE): ACTIVE_CYCLE,
        rel(ROADMAP): ROADMAP,
        rel(OUTLINE): OUTLINE,
        rel(FAST_CHAPTER): FAST_CHAPTER,
        rel(THESEUS_CHAPTER): THESEUS_CHAPTER,
        rel(FAST_READER): FAST_READER,
        rel(THESEUS_READER): THESEUS_READER,
    }
    for label, path in surfaces.items():
        text = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""
        normalized = re.sub(r"\s+", " ", text)
        for phrase in SURFACE_PHRASES:
            haystack = normalized if " " in phrase else text
            if phrase not in haystack:
                errors.append(f"{label} missing phrase {phrase!r}.")


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
    validate_lean_alignment(value, errors)
    validate_surfaces(errors)
    if errors:
        fail(errors)
    alignment = value["aggregate_lean_alignment"]
    print(
        "Theseus/Fast support-lane validation passed: "
        f"{alignment['command_replay_count']} command replay(s), "
        f"{alignment['tracked_artifact_count']} tracked artifact digest(s), "
        f"{alignment['public_task_count']} public task records, support-state effect none."
    )


if __name__ == "__main__":
    main()
