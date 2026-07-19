#!/usr/bin/env python3
"""Pull rank-one replacement images by digest, measure, and clean up."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROVENANCE = ROOT / "evidence_quality/p2_replacement_provenance_preflight.json"
RESOURCE = ROOT / "evidence_quality/p2_resource_ceiling.json"
OUT_ROOT = ROOT / "experiments/p2_governed_repository_admission/replacement_resource_preflight/attempts"
ATTEMPT_ID = "2026-07-17-rank-one-r2"


def run(command: list[str], *, timeout: int) -> tuple[int, str, float, bool]:
    started = time.monotonic()
    try:
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=timeout)
        return result.returncode, result.stdout + result.stderr, time.monotonic() - started, False
    except subprocess.TimeoutExpired as exc:
        out = (exc.stdout or "") + (exc.stderr or "")
        if isinstance(out, bytes): out = out.decode(errors="replace")
        return 124, out, time.monotonic() - started, True


def free_bytes() -> int:
    return shutil.disk_usage("/").free


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    provenance = json.loads(PROVENANCE.read_text(encoding="utf-8"))
    resource = json.loads(RESOURCE.read_text(encoding="utf-8"))
    if provenance["custody"]["image_pulled"] or provenance["custody"]["replacement_qualification_started"]:
        raise SystemExit("preflight custody is not at the pre-pull boundary")
    if not resource["qualification_state"]["ceiling_frozen"]:
        raise SystemExit("resource ceiling is not frozen")
    ceilings = resource["task_acceptance_ceilings"]
    attempt = OUT_ROOT / ATTEMPT_ID
    if attempt.exists():
        raise SystemExit(f"immutable attempt already exists: {attempt}")
    attempt.mkdir(parents=True)
    campaign_before = free_bytes()
    rows = []
    for candidate in provenance["candidates"]:
        image = candidate["image_manifest"]["image"]
        digest = candidate["image_manifest"]["digest"]
        immutable_ref = image.split(":", 1)[0] + "@" + digest
        before = free_bytes()
        row = {
            "slot": candidate["slot"], "rank": candidate["rank"], "instance_id": candidate["instance_id"],
            "image": image, "immutable_ref": immutable_ref, "manifest_digest": digest,
            "host_free_before_bytes": before, "minimum_host_free_gate_pass": before >= ceilings["minimum_host_free_bytes_before_task"]
        }
        log_path = attempt / f"slot_{candidate['slot']}_pull.log"
        if not row["minimum_host_free_gate_pass"]:
            log_path.write_text("pull not attempted: host free-space gate failed\n", encoding="utf-8")
            row.update({"pull_attempted": False, "pull_exit_code": None, "pull_timeout": False, "pull_wall_seconds": 0.0, "inspect_exit_code": None, "expanded_image_size_bytes": None, "cleanup_exit_code": None, "host_free_after_cleanup_bytes": before, "post_cleanup_host_free_byte_loss": 0, "resource_gate_pass": False, "failure_code": "host_free_space_below_frozen_minimum"})
            rows.append(row); continue
        code, output, wall, timed_out = run(["docker", "pull", immutable_ref], timeout=ceilings["image_pull_seconds"])
        log_path.write_text(output, encoding="utf-8")
        row.update({"pull_attempted": True, "pull_exit_code": code, "pull_timeout": timed_out, "pull_wall_seconds": round(wall, 6)})
        inspect_code, inspect_output, _, _ = run(["docker", "image", "inspect", immutable_ref, "--format", "{{json .}}"], timeout=30)
        row["inspect_exit_code"] = inspect_code
        if inspect_code == 0:
            data = json.loads(inspect_output)
            row.update({"expanded_image_size_bytes": data.get("Size"), "image_architecture": data.get("Architecture"), "image_os": data.get("Os"), "repo_digests": data.get("RepoDigests", [])})
        else:
            row.update({"expanded_image_size_bytes": None, "image_architecture": None, "image_os": None, "repo_digests": []})
        cleanup_code, cleanup_output, cleanup_wall, _ = run(["docker", "image", "rm", "-f", immutable_ref], timeout=120)
        cleanup_log = attempt / f"slot_{candidate['slot']}_cleanup.log"
        cleanup_log.write_text(cleanup_output, encoding="utf-8")
        time.sleep(1)
        after = free_bytes()
        loss = max(0, before - after)
        row.update({"cleanup_exit_code": cleanup_code, "cleanup_wall_seconds": round(cleanup_wall, 6), "host_free_after_cleanup_bytes": after, "post_cleanup_host_free_byte_loss": loss, "pull_log_path": log_path.relative_to(ROOT).as_posix(), "pull_log_sha256": sha256(log_path), "cleanup_log_path": cleanup_log.relative_to(ROOT).as_posix(), "cleanup_log_sha256": sha256(cleanup_log)})
        gates = {
            "pull_exit_zero": code == 0,
            "pull_within_seconds": wall <= ceilings["image_pull_seconds"],
            "pull_not_timed_out": not timed_out,
            "inspect_exit_zero": inspect_code == 0,
            "manifest_digest_present": digest in row.get("repo_digests", [""])[0] if row.get("repo_digests") else False,
            "linux_amd64": row.get("image_os") == "linux" and row.get("image_architecture") == "amd64",
            "expanded_size_within_bytes": row.get("expanded_image_size_bytes") is not None and row["expanded_image_size_bytes"] <= ceilings["expanded_image_bytes"],
            "cleanup_exit_zero": cleanup_code == 0,
            "post_cleanup_loss_within_bytes": loss <= ceilings["maximum_post_cleanup_host_free_byte_loss"]
        }
        row["gates"] = gates
        row["resource_gate_pass"] = all(gates.values())
        row["failure_code"] = None if row["resource_gate_pass"] else "rank_one_image_resource_gate_failure"
        rows.append(row)
    campaign_after = free_bytes()
    result = {
        "schema_version": "asi_stack.p2_replacement_image_resource_preflight.v1",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "attempt_id": ATTEMPT_ID,
        "state": "complete",
        "scope": "rank_one_image_pull_expanded_size_cleanup_and_host_residual_only",
        "resource_ceiling_path": "evidence_quality/p2_resource_ceiling.json",
        "provenance_preflight_path": "evidence_quality/p2_replacement_provenance_preflight.json",
        "candidate_count": len(rows),
        "passed_candidate_count": sum(row["resource_gate_pass"] for row in rows),
        "failed_candidate_count": sum(not row["resource_gate_pass"] for row in rows),
        "campaign_host_free_before_bytes": campaign_before,
        "campaign_host_free_after_bytes": campaign_after,
        "campaign_post_cleanup_host_free_byte_loss": max(0, campaign_before - campaign_after),
        "campaign_residual_gate_pass": max(0, campaign_before - campaign_after) <= resource["campaign_ceilings"]["maximum_cumulative_host_free_byte_loss"],
        "candidates": rows,
        "task_content_opened": False,
        "candidate_outcome_opened": False,
        "replacement_qualification_started": False,
        "final_pool_selected": False,
        "final_pool_opened": False,
        "support_state_effect": "none",
        "release_effect": "none"
    }
    (attempt / "result.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"P2 rank-one image resource preflight: {result['passed_candidate_count']}/{result['candidate_count']} passed; campaign residual {result['campaign_post_cleanup_host_free_byte_loss']} bytes.")


if __name__ == "__main__": main()
