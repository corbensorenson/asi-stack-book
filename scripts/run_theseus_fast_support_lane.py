#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import shlex
import subprocess
import sys
import time
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "experiments" / "theseus_fast_support_lane" / "results" / "2026-07-03-local.json"
RESULT_COMMAND = "python3 scripts/run_theseus_fast_support_lane.py --write-result"
LANE_ID = "theseus-fast-support-lane-2026-07-03-local"

REPLAY_COMMANDS = [
    {
        "id": "theseus_generation_mode_import",
        "command": "python3 scripts/validate_theseus_generation_mode_import.py",
        "evidence_surface": "Project Theseus public-safe generation-mode import plus Fast Generation Lean bridge",
    },
    {
        "id": "theseus_support_replay_probe",
        "command": "python3 scripts/validate_theseus_support_replay_probe.py",
        "evidence_surface": "ASI-side replay of the two Project Theseus static import validators",
    },
    {
        "id": "theseus_public_task_bundle_import",
        "command": "python3 scripts/validate_theseus_public_task_bundle_import.py",
        "evidence_surface": "bounded Project Theseus public task-bundle import and no-promotion decision",
    },
    {
        "id": "fast_generation_task_bundle",
        "command": "python3 scripts/validate_fast_generation_task_bundle.py",
        "evidence_surface": "local Fast Generation public-safe task bundle and no-promotion decision",
    },
]

TRACKED_ARTIFACTS = [
    "docs/theseus_generation_mode_import_slice.md",
    "docs/theseus_support_replay_probe.md",
    "docs/theseus_public_task_bundle_import.md",
    "docs/fast_generation_task_bundle.md",
    "experiments/theseus_generation_mode_import/results/2026-07-01-local.json",
    "experiments/theseus_support_replay_probe/results/2026-07-01-local.json",
    "experiments/theseus_public_task_bundle_import/results/2026-07-03-local.json",
    "experiments/fast_generation_task_bundle/results/2026-07-02-local.json",
    "evidence_transitions/v1_x_measured/theseus_public_task_bundle_import_no_change.json",
    "evidence_transitions/v1_x_measured/fast_generation_task_bundle_no_change.json",
    "lean/AsiStackProofs/FastGenerationRefinement.lean",
    "lean/AsiStackProofs/TheseusReference.lean",
    "scripts/validate_theseus_generation_mode_import.py",
    "scripts/validate_theseus_support_replay_probe.py",
    "scripts/validate_theseus_public_task_bundle_import.py",
    "scripts/validate_fast_generation_task_bundle.py",
]

NON_CLAIMS = [
    "This support-lane aggregate does not prove clean live Project Theseus replay.",
    "This support-lane aggregate does not prove model quality, benchmark superiority, generation speed, useful-solution-per-second improvement, routing quality, safety, alignment, transfer, or ASI.",
    "This support-lane aggregate does not copy private Project Theseus payloads, public prompts, tests, solutions, traces, scores, candidate code, training rows, checkpoints, or benchmark payloads into this repository.",
    "This support-lane aggregate does not promote any chapter core claim above argument and does not create an upward support-state transition.",
]


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def load_json(relative: str) -> Any:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def command_argv(command: str) -> list[str]:
    parts = shlex.split(command)
    if parts and parts[0] == "python3":
        return [sys.executable, *parts[1:]]
    return parts


def run_replay_command(record: dict[str, str]) -> dict[str, Any]:
    started = time.perf_counter()
    result = subprocess.run(
        command_argv(record["command"]),
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    elapsed_ms = round((time.perf_counter() - started) * 1000, 3)
    combined_output = result.stdout + result.stderr
    excerpt_lines = [line for line in combined_output.strip().splitlines() if line][:6]
    return {
        "id": record["id"],
        "command": record["command"],
        "evidence_surface": record["evidence_surface"],
        "exit_code": result.returncode,
        "elapsed_ms": elapsed_ms,
        "output_sha256": sha256_text(combined_output),
        "output_excerpt": excerpt_lines,
    }


def artifact_stat(relative: str) -> dict[str, Any]:
    path = ROOT / relative
    raw = path.read_bytes()
    text = raw.decode("utf-8", errors="ignore")
    return {
        "path": relative,
        "bytes": len(raw),
        "lines": text.count("\n") + (0 if text.endswith("\n") or not text else 1),
        "sha256": sha256_bytes(raw),
    }


def aggregate_summary() -> dict[str, Any]:
    generation = load_json("experiments/theseus_generation_mode_import/results/2026-07-01-local.json")
    support = load_json("experiments/theseus_support_replay_probe/results/2026-07-01-local.json")
    theseus_bundle = load_json("experiments/theseus_public_task_bundle_import/results/2026-07-03-local.json")
    fast_bundle = load_json("experiments/fast_generation_task_bundle/results/2026-07-02-local.json")

    fast_negative_rejected = bool(fast_bundle.get("negative_control_rejected"))
    expected_invalid_or_rejected = (
        int(generation.get("expected_invalid_count", 0))
        + int(theseus_bundle.get("expected_invalid_count", 0))
        + (1 if fast_negative_rejected else 0)
    )
    public_task_count = int(theseus_bundle.get("public_task_count", 0)) + int(fast_bundle.get("task_count", 0))

    return {
        "support_lane_count": 2,
        "command_replay_count": len(REPLAY_COMMANDS),
        "nested_support_replay_command_count": len(support.get("replay_commands", [])),
        "tracked_artifact_count": len(TRACKED_ARTIFACTS),
        "public_task_count": public_task_count,
        "expected_invalid_or_rejected_control_count": expected_invalid_or_rejected,
        "accepted_no_promotion_decision_count": 2,
        "generation_mode_import_included": True,
        "support_replay_probe_included": True,
        "theseus_public_task_bundle_included": True,
        "fast_generation_task_bundle_included": True,
        "clean_live_replay_claimed": False,
        "model_quality_claimed": False,
        "generation_speed_claimed": False,
        "useful_solution_model_claimed": False,
        "chapter_core_promotion_claimed": False,
        "support_state_promotion_claimed": False,
        "non_claim_boundary_recorded": True,
    }


def build_record() -> dict[str, Any]:
    command_records = [run_replay_command(command) for command in REPLAY_COMMANDS]
    passed = all(record["exit_code"] == 0 for record in command_records)
    aggregate = aggregate_summary()
    return {
        "lane_id": LANE_ID,
        "record_kind": "theseus_fast_support_lane",
        "recorded_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "command": RESULT_COMMAND,
        "selected_support_lanes": [
            "project-theseus-as-report-first-implementation-reference",
            "fast-generation-architectures",
        ],
        "local_only": True,
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
        "pass": passed,
        "summary": "Aggregate support-lane replay for the selected Project Theseus and Fast Generation v1.x lanes.",
        "replay_commands": command_records,
        "artifact_refs": [*TRACKED_ARTIFACTS, str(RESULT.relative_to(ROOT))],
        "tracked_artifacts": [artifact_stat(path) for path in TRACKED_ARTIFACTS],
        "aggregate_lean_alignment": {
            "lean_module": "lean/AsiStackProofs/TheseusReference.lean",
            "fixture_def": "theseusFastSupportAggregateFixture",
            "proof_tag": "lean:theseus.reference.fast_support_aggregate.fixture_bridge",
            "checked_theorem_names": [
                "theseus_fast_support_aggregate_fixture_valid",
                "theseus_fast_support_aggregate_preserves_no_promotion",
                "theseus_fast_support_aggregate_carries_task_and_control_counts",
                "theseus_fast_support_aggregate_clean_replay_overclaim_rejected",
            ],
            **aggregate,
        },
        "non_claims": NON_CLAIMS,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Theseus/Fast selected support-lane aggregate.")
    parser.add_argument("--write-result", action="store_true", help=f"write {RESULT.relative_to(ROOT)}")
    args = parser.parse_args()

    record = build_record()
    text = json.dumps(record, indent=2, sort_keys=True) + "\n"
    if args.write_result:
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(text, encoding="utf-8")
        print(f"Wrote {RESULT.relative_to(ROOT)}")
    else:
        print(text, end="")
    if not record["pass"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
