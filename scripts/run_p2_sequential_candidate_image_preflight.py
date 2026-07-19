#!/usr/bin/env python3
"""Measure one sequential replacement image before opening task content."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import shutil
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESOURCE = ROOT / "evidence_quality/p2_resource_ceiling.json"
OUT_ROOT = ROOT / "experiments/p2_governed_repository_admission/sequential_image_preflight/attempts"


def run(*args: str, timeout: int = 300) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, capture_output=True, text=True, check=False, timeout=timeout)


def sha_text(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def virtual_upper(image_id: str) -> tuple[str | None, int | None]:
    proc = run("docker", "system", "df", "-v", "--format", "{{json .}}", timeout=30)
    data = json.loads(proc.stdout) if proc.returncode == 0 else {}
    row = next((item for item in data.get("Images", []) if item.get("ID") == image_id), None)
    if not row:
        return None, None
    display = row["Size"]
    match = re.fullmatch(r"([0-9]+(?:\.([0-9]+))?)([kMGT]?B)", display)
    if not match:
        return display, None
    digits = len(match.group(2) or "")
    factor = {"B": 1, "kB": 1000, "MB": 1000**2, "GB": 1000**3, "TB": 1000**4}[match.group(3)]
    half_unit = 0 if digits == 0 else 0.5 * 10 ** (-digits)
    return display, math.ceil((float(match.group(1)) + half_unit) * factor)


def stabilize(host_before: int, ceiling: dict) -> dict:
    samples = []
    deadline = time.monotonic() + ceiling["cleanup_stabilization_timeout_seconds"]
    stable = False
    while True:
        free = shutil.disk_usage("/").free
        proc = run("docker", "system", "df", "--format", "{{json .}}", timeout=30)
        rows = [json.loads(line) for line in proc.stdout.splitlines() if line.strip()] if proc.returncode == 0 else []
        docker_zero = bool(rows) and all(str(row.get("Size")) == "0B" and str(row.get("TotalCount")) == "0" for row in rows)
        samples.append({"free_bytes": free, "docker_zero": docker_zero})
        recent = samples[-ceiling["cleanup_stabilization_required_consecutive_samples"] :]
        if (
            len(recent) == ceiling["cleanup_stabilization_required_consecutive_samples"]
            and all(row["docker_zero"] for row in recent)
            and max(row["free_bytes"] for row in recent) - min(row["free_bytes"] for row in recent)
            <= ceiling["cleanup_stabilization_max_sample_delta_bytes"]
        ):
            stable = True
            break
        if time.monotonic() >= deadline:
            break
        time.sleep(ceiling["cleanup_stabilization_sample_interval_seconds"])
    final = samples[-1]["free_bytes"]
    return {"stable": stable, "samples": samples, "host_free_after_bytes": final, "host_free_byte_loss": max(0, host_before - final)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--provenance", required=True)
    parser.add_argument("--attempt-id", required=True)
    args = parser.parse_args()
    provenance_path = ROOT / args.provenance
    out = OUT_ROOT / args.attempt_id
    if out.exists():
        raise SystemExit(f"immutable attempt exists: {out}")
    out.mkdir(parents=True)

    provenance = json.loads(provenance_path.read_text())
    resource = json.loads(RESOURCE.read_text())
    ceiling = resource["task_acceptance_ceilings"]
    candidate = provenance["candidate"]
    if provenance["state"] != "passed_before_task_content_opened" or provenance["custody"]["candidate_task_content_opened"]:
        raise SystemExit("provenance/custody gate failed")
    manifest = candidate["image_manifest"]
    ref = manifest["image"].split(":", 1)[0] + "@" + manifest["digest"]
    before = shutil.disk_usage("/").free
    result = {
        "schema_version": "asi_stack.p2_sequential_candidate_image_preflight.v1",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "attempt_id": args.attempt_id,
        "claim_id": provenance["claim_id"],
        "provenance_path": args.provenance,
        "resource_ceiling_path": "evidence_quality/p2_resource_ceiling.json",
        "slot": candidate["slot"],
        "rank": candidate["rank"],
        "instance_id": candidate["instance_id"],
        "image_ref": ref,
        "manifest_digest": manifest["digest"],
        "host_free_before_bytes": before,
        "task_content_opened": False,
        "candidate_outcome_opened": False,
        "final_pool_selected": False,
        "final_pool_opened": False,
        "support_state_effect": "none",
        "release_effect": "none",
    }
    state = "n0_instrument_failure"
    code = "runner_did_not_complete"
    detail = "image preflight did not reach a classified terminal state"
    cleanup = None
    try:
        if before < ceiling["minimum_host_free_bytes_before_task"]:
            state, code, detail = "n0_resource_failure", "host_free_below_minimum", "image pull not attempted"
        else:
            started = time.monotonic()
            pull = run("docker", "pull", "--platform", "linux/amd64", ref, timeout=ceiling["image_pull_seconds"])
            elapsed = time.monotonic() - started
            pull_text = (pull.stdout or "") + (pull.stderr or "")
            result["pull"] = {"exit_code": pull.returncode, "wall_seconds": round(elapsed, 6), "output_sha256": sha_text(pull_text)}
            if pull.returncode or elapsed > ceiling["image_pull_seconds"]:
                state, code, detail = "n0_resource_failure", "pull_failure_or_timeout", "exact image was unavailable within the frozen pull ceiling"
            else:
                inspect = run("docker", "image", "inspect", ref, "--format", "{{json .}}", timeout=30)
                info = json.loads(inspect.stdout) if inspect.returncode == 0 else {}
                display, upper = virtual_upper(info.get("Id", ""))
                gates = {
                    "inspect_exit_zero": inspect.returncode == 0,
                    "manifest_digest_present": any(value.endswith("@" + manifest["digest"]) for value in info.get("RepoDigests", [])),
                    "linux_amd64": info.get("Os") == "linux" and info.get("Architecture") == "amd64",
                    "engine_content_within_ceiling": info.get("Size", 10**30) <= ceiling["engine_content_size_bytes"],
                    "virtual_size_within_ceiling": upper is not None and upper <= ceiling["virtual_size_conservative_upper_bound_bytes"],
                }
                result["measurement"] = {
                    "image_id": info.get("Id"),
                    "repo_digests": info.get("RepoDigests", []),
                    "os": info.get("Os"),
                    "architecture": info.get("Architecture"),
                    "engine_content_size_bytes": info.get("Size"),
                    "virtual_size_display": display,
                    "virtual_size_conservative_upper_bound_bytes": upper,
                    "gates": gates,
                }
                if all(gates.values()):
                    state, code, detail = "measurement_pass_pending_cleanup", "measurement_gates_passed", "exact image passed prospective pull/content/virtual/platform gates"
                else:
                    state, code, detail = "n0_resource_failure", "one_or_more_measurement_gates_failed", "exact image failed at least one prospective image gate"
    except subprocess.TimeoutExpired as exc:
        state, code, detail = "n0_resource_failure", "pull_or_measurement_timeout", f"{type(exc).__name__}: {exc}"
    except Exception as exc:
        state, code, detail = "n0_instrument_failure", "unhandled_runner_exception", f"{type(exc).__name__}: {exc}"
    finally:
        removal = run("docker", "image", "rm", "-f", ref, timeout=120)
        prune = run("docker", "image", "prune", "-f", timeout=120)
        stabilization = stabilize(before, ceiling)
        cleanup = {
            "image_removal_exit_code": removal.returncode,
            "image_removal_output_sha256": sha_text((removal.stdout or "") + (removal.stderr or "")),
            "partial_layer_prune_exit_code": prune.returncode,
            "partial_layer_prune_output_sha256": sha_text((prune.stdout or "") + (prune.stderr or "")),
            "stabilization": stabilization,
        }
        cleanup_pass = (
            removal.returncode == 0
            and prune.returncode == 0
            and stabilization["stable"]
            and stabilization["host_free_byte_loss"] <= ceiling["maximum_post_cleanup_host_free_byte_loss"]
        )
        if state == "measurement_pass_pending_cleanup" and cleanup_pass:
            state, code, detail = "passed", "all_image_and_cleanup_gates_passed", "candidate may proceed to task opening"
        elif state == "measurement_pass_pending_cleanup":
            state, code, detail = "n0_resource_failure", "cleanup_gate_failed", "measurement passed but frozen cleanup gate failed"
        result.update({
            "state": state,
            "terminal_code": code,
            "terminal_detail": detail,
            "cleanup": cleanup,
            "image_resource_gate_passed": state == "passed",
        })
        (out / "result.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
        print(f"{candidate['instance_id']}: {state} {code}", flush=True)


if __name__ == "__main__":
    main()
