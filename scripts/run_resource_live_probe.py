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
RESULT = ROOT / "experiments" / "resource_live_probe" / "results" / "2026-07-01-local.json"
PROBE_ID = "resource-live-probe-2026-07-01-local"
RESULT_COMMAND = "python3 scripts/run_resource_live_probe.py --write-result"

REPLAY_COMMANDS = [
    {
        "id": "costed_route_resource_slice",
        "command": "python3 scripts/validate_costed_route_resource_slice.py",
        "evidence_surface": "non-core synthetic-test-backed costed-route/resource-budget slice",
    },
    {
        "id": "resource_workflow_trace",
        "command": "python3 scripts/validate_resource_workflow_trace.py",
        "evidence_surface": "deterministic multi-step Resource Economics workflow trace",
    },
    {
        "id": "resource_budget_ledgers",
        "command": "python3 scripts/validate_resource_budget_ledgers.py",
        "evidence_surface": "Resource Budget Record fixture decisions",
    },
    {
        "id": "capacity_smoothing",
        "command": "python3 scripts/validate_capacity_smoothing.py",
        "evidence_surface": "bounded-capacity toy trace fixtures",
    },
    {
        "id": "simulation_transfer_boundaries",
        "command": "python3 scripts/validate_simulation_transfer_boundaries.py",
        "evidence_surface": "simulation-transfer boundary fixtures folded into Resource Economics",
    },
]

TRACKED_ARTIFACTS = [
    "docs/costed_route_resource_slice.md",
    "docs/resource_workflow_trace.md",
    "docs/resource_live_probe.md",
    "scripts/validate_costed_route_resource_slice.py",
    "scripts/validate_resource_workflow_trace.py",
    "scripts/validate_resource_budget_ledgers.py",
    "scripts/validate_capacity_smoothing.py",
    "scripts/validate_simulation_transfer_boundaries.py",
    "lean/AsiStackProofs/ResourceEconomics.lean",
    "lean/AsiStackProofs/SimulationFidelity.lean",
    "experiments/costed_route_resource_slice/results/2026-06-29-local.json",
    "experiments/resource_workflow_trace/results/2026-07-01-local.json",
    "experiments/resource_budget_ledgers/results/2026-07-01-local.md",
    "experiments/capacity_smoothing/results/2026-06-28-local.md",
    "experiments/simulation_transfer_boundaries/results/2026-06-30-local.md",
]

NON_CLAIMS = [
    "This local replay probe does not promote any chapter core claim above argument.",
    "This local replay probe does not create a support-state transition.",
    "This local replay probe does not prove deployed scheduler behavior, runtime budget enforcement, TokenMana behavior, PlanForge behavior, model quality, economic outcomes, physical feasibility, simulator adequacy, or open-world transfer.",
    "This local replay probe records repository command execution only; it is not a live workload quality review, production scheduler log, human-repair measurement, or external physical-feasibility review.",
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
        "record_kind": "resource_live_probe",
        "recorded_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "command": RESULT_COMMAND,
        "local_only": True,
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
        "pass": passed,
        "summary": "Resource live probe replayed five local Resource Economics validators and recorded command-output digests plus tracked artifact hashes without creating a support-state transition.",
        "replay_commands": command_records,
        "artifact_refs": [*TRACKED_ARTIFACTS, str(RESULT.relative_to(ROOT))],
        "tracked_artifacts": [artifact_stat(path) for path in TRACKED_ARTIFACTS],
        "non_claims": NON_CLAIMS,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Resource Economics local live replay probe.")
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
