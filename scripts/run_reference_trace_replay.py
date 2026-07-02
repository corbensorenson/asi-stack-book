#!/usr/bin/env python3
"""Record a replayed Integrated Reference Architecture trace.

This runner turns one actual repository command into a Reference Trace Record.
It is intentionally narrower than a deployed runtime trace: the command is a
local validator replay, and the blocked path is anchored to the existing
blocked-authority fixture.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shlex
import subprocess
import sys
import time
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "experiments" / "reference_trace" / "replay_results" / "2026-07-02-resource-flagship.json"
RUN_ID = "reference-trace-replay-2026-07-02-resource-flagship"
RESULT_COMMAND = "python3 scripts/run_reference_trace_replay.py --write-result"
REPLAY_COMMAND = "python3 scripts/validate_resource_flagship_lane.py"
BLOCKED_FIXTURE = "experiments/reference_trace/fixtures/valid_blocked_authority_trace.json"

TRACKED_ARTIFACTS = [
    "docs/reference_trace_harness.md",
    "docs/resource_flagship_lane_run.md",
    "experiments/resource_flagship_lane/results/2026-07-01-local.json",
    "scripts/validate_resource_flagship_lane.py",
    "scripts/run_resource_flagship_lane.py",
    "scripts/validate_reference_trace.py",
    "scripts/validate_reference_trace_replay.py",
    BLOCKED_FIXTURE,
    "evidence_transitions/v1_0_measured/costed_route_resource_slice_synthetic_test_backed.json",
    "evidence_transitions/v1_0_pilot/resource_economics_no_change.json",
    "evidence_transitions/v1_x_measured/resource_workload_quality_probe_no_change.json",
    "evidence_transitions/v1_x_measured/resource_load_stability_probe_no_change.json",
    "chapters/integrated-reference-architecture.qmd",
]

NON_CLAIMS = [
    "This replay does not promote any chapter core support state.",
    "This replay does not prove an integrated ASI Stack runtime or deployed layer behavior.",
    "This replay does not prove authority-stop enforcement beyond the referenced blocked fixture.",
    "This replay does not prove scheduler behavior, model quality, benchmark quality, safety, or economic outcomes.",
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


def run_command(command: str) -> dict[str, Any]:
    started = time.perf_counter()
    result = subprocess.run(
        command_argv(command),
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    elapsed_ms = round((time.perf_counter() - started) * 1000, 3)
    combined = result.stdout + result.stderr
    excerpt = [line for line in combined.strip().splitlines() if line][:8]
    return {
        "command": command,
        "exit_code": result.returncode,
        "elapsed_ms": elapsed_ms,
        "output_sha256": sha256_text(combined),
        "output_excerpt": excerpt,
    }


def load_json(relative: str) -> Any:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


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


def build_reference_trace(command_record: dict[str, Any], blocked_fixture: dict[str, Any]) -> dict[str, Any]:
    blocked = blocked_fixture["reference_trace_record"]
    return {
        "trace_id": RUN_ID,
        "trace_state": "replayed",
        "execution_boundary": "replay",
        "intent_ref": "intent://resource-flagship-no-promotion-replay",
        "parent_artifact_refs": [
            "command://validate-resource-flagship-lane",
            "result://resource-flagship-lane-2026-07-01-local",
            "fixture://valid-blocked-authority-trace"
        ],
        "authority_chain": [
            "repo maintenance authority permits local validator replay",
            "no runtime execution authority is granted",
            "blocked authority fixture remains the stop-condition reference",
            "SCF promotion authority remains withheld"
        ],
        "authority_deltas": [
            "actual command authority is limited to local validation",
            "blocked path authority is denied by the fixture governance gate",
            "support-state promotion authority is not granted"
        ],
        "layer_handoffs": [
            "intent -> command contract for local replay",
            "command contract -> plan for Resource flagship validation",
            "plan -> context artifact bundle",
            "context -> route through Resource flagship validator",
            "route -> verification command output",
            "verification -> execution replay record",
            "execution -> evidence-transition boundary check",
            "evidence -> SCF no-promotion decision"
        ],
        "artifacts": [
            "command://validate-resource-flagship-lane",
            "artifact://docs-resource-flagship-lane-run",
            "artifact://resource-flagship-result-json",
            "artifact://resource-sublane-no-promotion-records",
            "audit://actual-command-output-digest",
            "evidence://evidence-transition-validation-pass",
            "blocked://valid-blocked-authority-stop-conditions",
            "scf://no-promotion-boundary"
        ],
        "evidence_updates": [
            f"actual command exited {command_record['exit_code']}",
            "Resource flagship lane validator passed as a local replay",
            "blocked authority fixture stop conditions remain attached"
        ],
        "evidence_deltas": [
            "reference trace replay record added",
            "support state remains argument",
            "no new evidence transition created"
        ],
        "residual_deltas": [
            "runtime integration trace remains unimplemented",
            "artifact continuity remains local-replay scoped",
            "authority-stop behavior remains fixture-backed rather than deployed"
        ],
        "stop_conditions": [
            "no deployed runtime trace",
            "no external workload review",
            *blocked.get("stop_conditions", [])
        ],
        "missing_contracts": [
            "deployed runtime contract missing",
            "production artifact-continuity service missing",
            *blocked.get("missing_contracts", [])
        ],
        "validation_commands": [
            "python3 scripts/validate_reference_trace.py",
            "python3 scripts/validate_reference_trace_replay.py",
            REPLAY_COMMAND
        ],
        "promotion_blockers": [
            "local replay only",
            "no integrated runtime replay",
            *blocked.get("promotion_blockers", [])
        ],
        "source_refs": [
            "sources/source_notes/viea.md",
            "sources/source_notes/scf.md",
            "sources/source_notes/talos.md",
            "sources/source_notes/moecot.md"
        ],
        "support_state_effect": "record_shape_only",
        "non_claims": NON_CLAIMS
    }


def build_record() -> dict[str, Any]:
    command_record = run_command(REPLAY_COMMAND)
    blocked_fixture = load_json(BLOCKED_FIXTURE)
    trace = build_reference_trace(command_record, blocked_fixture)
    return {
        "schema_version": "0.1",
        "replay_id": RUN_ID,
        "record_kind": "reference_trace_replay",
        "recorded_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "command": RESULT_COMMAND,
        "replay_command": REPLAY_COMMAND,
        "local_only": True,
        "public_safe": True,
        "pass": command_record["exit_code"] == 0,
        "support_state_effect": "record_shape_only",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
        "reference_trace_record": trace,
        "actual_command_record": command_record,
        "blocked_path_fixture_ref": BLOCKED_FIXTURE,
        "blocked_path_stop_conditions": blocked_fixture["reference_trace_record"].get("stop_conditions", []),
        "artifact_refs": [*TRACKED_ARTIFACTS, str(RESULT.relative_to(ROOT))],
        "tracked_artifacts": [artifact_stat(path) for path in TRACKED_ARTIFACTS],
        "non_claims": NON_CLAIMS
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
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
