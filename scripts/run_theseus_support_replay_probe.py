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
RESULT = ROOT / "experiments" / "theseus_support_replay_probe" / "results" / "2026-07-01-local.json"
PROBE_ID = "theseus-support-replay-probe-2026-07-01-local"
RESULT_COMMAND = "python3 scripts/run_theseus_support_replay_probe.py --write-result"

REPLAY_COMMANDS = [
    {
        "id": "theseus_architecture_gate_import",
        "command": "python3 scripts/validate_theseus_report.py",
        "evidence_surface": "public-safe static Project Theseus architecture-gate import",
    },
    {
        "id": "theseus_generation_mode_import",
        "command": "python3 scripts/validate_theseus_generation_mode_import.py",
        "evidence_surface": "public-safe static Project Theseus generation-mode import plus Fast Generation Lean bridge",
    },
]

TRACKED_ARTIFACTS = [
    "docs/theseus_report_import_slice.md",
    "docs/theseus_generation_mode_import_slice.md",
    "docs/theseus_support_replay_probe.md",
    "scripts/validate_theseus_report.py",
    "scripts/validate_theseus_generation_mode_import.py",
    "lean/AsiStackProofs/FastGenerationRefinement.lean",
    "experiments/theseus_import/fixtures/valid/architecture_gate_public_report.valid.json",
    "experiments/theseus_import/results/2026-06-29-local.json",
    "experiments/theseus_generation_mode_import/fixtures/valid/generation_mode_gate_public_summary.valid.json",
    "experiments/theseus_generation_mode_import/results/2026-07-01-local.json",
]

NON_CLAIMS = [
    "This Theseus support replay probe does not promote any chapter core claim above argument.",
    "This Theseus support replay probe does not create a support-state transition.",
    "This Theseus support replay probe does not rerun Project Theseus, prove deployed Theseus runtime behavior, prove generation speed, prove useful-solution-per-second improvement, prove model quality, prove routing quality, prove benchmark quality, prove safety, prove alignment, prove transfer, or prove ASI.",
    "This Theseus support replay probe records repository command execution over public-safe static imports only; it is not a clean live Theseus replay, public task-bundle run, production dashboard record, or external review.",
]


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


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


def build_record() -> dict[str, Any]:
    command_records = [run_replay_command(command) for command in REPLAY_COMMANDS]
    passed = all(record["exit_code"] == 0 for record in command_records)
    return {
        "probe_id": PROBE_ID,
        "record_kind": "theseus_support_replay_probe",
        "recorded_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "command": RESULT_COMMAND,
        "local_only": True,
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
        "pass": passed,
        "summary": "Theseus support replay probe replayed the public-safe architecture-gate import and generation-mode import validators, then recorded command-output digests and tracked artifact hashes without creating a support-state transition.",
        "replay_commands": command_records,
        "artifact_refs": [*TRACKED_ARTIFACTS, str(RESULT.relative_to(ROOT))],
        "tracked_artifacts": [artifact_stat(path) for path in TRACKED_ARTIFACTS],
        "non_claims": NON_CLAIMS,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Project Theseus support replay probe.")
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
