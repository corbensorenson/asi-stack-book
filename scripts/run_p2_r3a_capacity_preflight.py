#!/usr/bin/env python3
"""Record the P2-R3a host-capacity and Docker-daemon entry preflight.

This runner never pulls an image and never reads protected task content.  It
only decides whether the frozen materialization protocol is allowed to start.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shlex
import shutil
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESOURCE = ROOT / "evidence_quality/p2_resource_ceiling.json"
QUEUE = ROOT / "experiments/p2_governed_repository_admission/corpus/replacement_queue.json"
OUT_ROOT = (
    ROOT
    / "experiments/p2_governed_repository_admission/infrastructure_materialization/attempts"
)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def capture(command: list[str], *, timeout: int = 30) -> dict:
    started = datetime.now(timezone.utc)
    monotonic_start = time.monotonic()
    timed_out = False
    try:
        result = subprocess.run(
            command,
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        exit_code = result.returncode
        stdout = result.stdout
        stderr = result.stderr
    except subprocess.TimeoutExpired as exc:
        timed_out = True
        exit_code = 124
        stdout = exc.stdout or ""
        stderr = exc.stderr or ""
        if isinstance(stdout, bytes):
            stdout = stdout.decode(errors="replace")
        if isinstance(stderr, bytes):
            stderr = stderr.decode(errors="replace")
    ended = datetime.now(timezone.utc)
    return {
        "argv": command,
        "shell_display": shlex.join(command),
        "started_at_utc": started.isoformat(),
        "ended_at_utc": ended.isoformat(),
        "wall_seconds": round(time.monotonic() - monotonic_start, 6),
        "timeout_seconds": timeout,
        "timed_out": timed_out,
        "exit_code": exit_code,
        "stdout": stdout,
        "stderr": stderr,
        "stdout_sha256": sha256_bytes(stdout.encode()),
        "stderr_sha256": sha256_bytes(stderr.encode()),
    }


def git_commit() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--attempt-id",
        required=True,
        help="Immutable identifier such as 2026-07-26-r3a-001.",
    )
    args = parser.parse_args()

    attempt_dir = OUT_ROOT / args.attempt_id
    if attempt_dir.exists():
        raise SystemExit(f"immutable attempt already exists: {attempt_dir}")

    resource = json.loads(RESOURCE.read_text(encoding="utf-8"))
    queue = json.loads(QUEUE.read_text(encoding="utf-8"))
    floor = resource["task_acceptance_ceilings"][
        "minimum_host_free_bytes_before_task"
    ]
    candidate_count = queue["candidate_count"]
    if candidate_count != 30:
        raise SystemExit(f"frozen queue must contain 30 candidates, found {candidate_count}")

    recorded_at = datetime.now(timezone.utc)
    disk = shutil.disk_usage(ROOT)
    command_receipts = [
        capture(["df", "-k", str(ROOT)]),
        capture(["docker", "version", "--format", "{{json .}}"]),
        capture(["docker", "info", "--format", "{{json .}}"]),
        capture(["docker", "system", "df", "--format", "{{json .}}"]),
    ]
    docker_commands = command_receipts[1:]
    docker_daemon_reachable = all(row["exit_code"] == 0 for row in docker_commands)
    host_floor_pass = disk.free >= floor
    entry_gate_pass = host_floor_pass and docker_daemon_reachable
    if entry_gate_pass:
        state = "entry_gate_pass_materialization_not_started"
        blockers: list[str] = []
    else:
        state = "blocked_before_materialization"
        blockers = []
        if not host_floor_pass:
            blockers.append("host_free_bytes_below_frozen_50_gib_floor")
        if not docker_daemon_reachable:
            blockers.append("docker_daemon_unreachable")

    record = {
        "schema_version": "asi_stack.p2_r3a_capacity_preflight.v1",
        "attempt_id": args.attempt_id,
        "recorded_at_utc": recorded_at.isoformat(),
        "state": state,
        "claim_id": "p2.governed_natural_repository_change_admission_joint_frontier",
        "scope": "host_capacity_and_docker_daemon_entry_preflight_only",
        "source_commit": git_commit(),
        "inputs": {
            "resource_ceiling_path": RESOURCE.relative_to(ROOT).as_posix(),
            "resource_ceiling_sha256": sha256_file(RESOURCE),
            "replacement_queue_path": QUEUE.relative_to(ROOT).as_posix(),
            "replacement_queue_sha256": sha256_file(QUEUE),
            "frozen_candidate_count": candidate_count,
        },
        "host_capacity": {
            "measured_path": str(ROOT),
            "total_bytes": disk.total,
            "used_bytes": disk.used,
            "available_bytes": disk.free,
            "minimum_required_bytes": floor,
            "shortfall_bytes": max(0, floor - disk.free),
            "floor_pass": host_floor_pass,
        },
        "docker": {
            "daemon_reachable": docker_daemon_reachable,
            "all_diagnostic_commands_exit_zero": docker_daemon_reachable,
            "reclaimable_bytes_known": docker_daemon_reachable,
            "reclamation_attempted": False,
            "reclamation_authorized_scope": "docker_objects_only",
        },
        "command_receipts": command_receipts,
        "decision": {
            "entry_gate_pass": entry_gate_pass,
            "blockers": blockers,
            "pool_materialization_started": False,
            "candidate_image_pull_started": False,
            "dependency_materialization_started": False,
            "protected_task_content_opened": False,
            "candidate_outcome_opened": False,
            "next_legal_action": (
                "run_content_sealed_sequential_materializer"
                if entry_gate_pass
                else "restore_frozen_capacity_floor_and_live_docker_daemon_then_record_new_immutable_preflight"
            ),
        },
        "negative_inference_level": "N0",
        "support_state_effect": "none",
        "release_effect": "none",
        "non_claims": [
            "A failed capacity or Docker preflight is not evidence against governed repository admission.",
            "No task problem, patch, test identity, command, label, model output, evaluator judgment, or outcome was opened.",
            "This receipt does not materialize the thirty-candidate pool or qualify a replacement.",
            "No non-Docker user data may be deleted by this protocol.",
        ],
    }

    attempt_dir.mkdir(parents=True)
    output = attempt_dir / "result.json"
    output.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(
        f"P2-R3a {args.attempt_id}: state={state}; "
        f"available={disk.free}; required={floor}; "
        f"docker_daemon_reachable={docker_daemon_reachable}; "
        "protected_content_opened=false."
    )


if __name__ == "__main__":
    main()
