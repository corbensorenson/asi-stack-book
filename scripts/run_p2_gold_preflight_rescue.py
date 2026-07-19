#!/usr/bin/env python3
"""Rescue P2 development-only gold preflight instrument failures.

This runner never opens or selects the final pool.  It addresses two diagnosed
instrument defects from the fixed 12-task preflight:

1. four official images require dependency downloads after test start; this
   runner materializes only package-manager dependencies under recorded network
   access, seals a derived image, and then repeats both arms with no network;
2. the pinned upstream JavaScript parser does not recognize AVA's
   ``✘ [fail]:`` records; this runner independently re-scores the already
   retained immutable logs.

The output remains a development-harness qualification, never claim evidence.
"""

from __future__ import annotations

import argparse
import __future__
import gzip
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
import types
import uuid
from pathlib import Path

import pyarrow.parquet as pq

import run_p2_gold_preflight as v1


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "experiments/p2_governed_repository_admission/gold_preflight_rescue"
RESULT = OUT / "result.json"
V1_RESULT = ROOT / "experiments/p2_governed_repository_admission/gold_preflight/result.json"

NETWORK_RESCUES = {
    "aleph-alpha__ts-rs-422": {
        "reason": "cargo_registry_not_materialized_in_official_image",
        "prepare": 'export PATH="/root/.cargo/bin:$PATH"; cargo fetch',
    },
    "compose-spec__compose-go-792": {
        "reason": "go_module_cache_not_materialized_in_official_image",
        "prepare": (
            "export PATH=/usr/local/go/bin:$PATH; export HOME=/root; "
            "export GOCACHE=$HOME/.cache/go-build; export GOPATH=$HOME/go; "
            "export GOMODCACHE=$GOPATH/pkg/mod; mkdir -p $GOCACHE $GOMODCACHE; "
            "go mod download"
        ),
    },
    "gitleaks__gitleaks-1845": {
        "reason": "go_module_cache_not_materialized_in_official_image",
        "prepare": (
            "export PATH=/usr/local/go/bin:$PATH; export GOPATH=$HOME/go; "
            "export GOMODCACHE=$GOPATH/pkg/mod; export GOCACHE=$HOME/.cache/go-build; "
            "export XDG_CACHE_HOME=$HOME/.cache; mkdir -p $GOMODCACHE $GOCACHE; "
            "go mod download"
        ),
    },
    "thealgorithms__java-6333": {
        "reason": "maven_repository_not_materialized_in_official_image",
        "prepare": (
            "mvn --batch-mode -DskipTests dependency:go-offline; "
            "mvn --batch-mode dependency:get "
            "-Dartifact=org.apache.maven.surefire:surefire-junit-platform:3.5.3"
        ),
    },
}

AVA_RESCUE_ID = "keithamus__sort-package-json-361"


def run(*args: str, timeout: int | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, capture_output=True, text=True, check=False, timeout=timeout)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def load_log(path: Path) -> str:
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        return handle.read()


def independent_ava_statuses(output: str) -> dict[str, str]:
    """Parse the AVA status grammar absent from the pinned upstream parser."""
    statuses: dict[str, str] = {}
    passed = re.compile(r"^\s*✔\s+(.*?)\s*$")
    failed = re.compile(r"^\s*✘\s+\[fail\]:\s+(.*?)\s*$")
    for line in output.splitlines():
        match = failed.match(line)
        if match:
            statuses[v1.normalize_name(match.group(1))] = "FAILED"
            continue
        match = passed.match(line)
        if match:
            statuses.setdefault(v1.normalize_name(match.group(1)), "PASSED")
    return statuses


def ava_rescue(spec: dict, v1_task: dict) -> dict:
    runs = []
    for prior in v1_task["runs"]:
        log_path = ROOT / prior["compressed_log_path"]
        output = load_log(log_path)
        if sha256_text(output) != prior["output_sha256"]:
            raise RuntimeError(f"retained log digest mismatch: {log_path}")
        statuses = independent_ava_statuses(output)
        passed = {name for name, value in statuses.items() if value == "PASSED"}
        failed = {name for name, value in statuses.items() if value == "FAILED"}
        f2p = {v1.normalize_name(name) for name in spec["FAIL_TO_PASS"]}
        p2p = {v1.normalize_name(name) for name in spec["PASS_TO_PASS"]}
        if prior["arm"] == "baseline_test_patch_only":
            accepted = passed == p2p and failed == f2p and "21 tests failed" in output
        else:
            accepted = passed == p2p | f2p and not failed and "__P2_TEST_COMPLETED__" in output
        runs.append({
            "arm": prior["arm"],
            "repetition": prior["repetition"],
            "pass": accepted,
            "source_log": prior["compressed_log_path"],
            "source_log_sha256": prior["output_sha256"],
            "upstream_parser_pass": prior["pass"],
            "independent_passed_count": len(passed),
            "independent_failed_count": len(failed),
            "expected_passed_count": len(p2p) if prior["arm"] == "baseline_test_patch_only" else len(p2p | f2p),
            "expected_failed_count": len(f2p) if prior["arm"] == "baseline_test_patch_only" else 0,
        })
    return {
        "instance_id": AVA_RESCUE_ID,
        "rescue_type": "independent_immutable_log_rescore",
        "diagnosis": "upstream_parser_missing_ava_fail_grammar",
        "all_runs_pass": all(row["pass"] for row in runs),
        "runs": runs,
    }


def load_parsers(harness_repo: Path):
    sys.path.insert(0, str(harness_repo))
    sys.path.insert(0, str(harness_repo / "lib"))
    source = harness_repo / "lib/agent/log_parsers.py"
    module = types.ModuleType("p2_rescue_upstream_log_parsers")
    module.__file__ = str(source)
    exec(
        compile(source.read_text(encoding="utf-8"), str(source), "exec", flags=__future__.annotations.compiler_flag),
        module.__dict__,
    )
    return module


def network_rescue(*, spec: dict, custody: dict, receipt: dict, parser_fn,
                   repetitions: int, timeout_seconds: int, attempt_id: str) -> dict:
    instance_id = spec["instance_id"]
    config = NETWORK_RESCUES[instance_id]
    repo_name = spec["repo"].split("/", 1)[1]
    base_ref = f"{spec['image_name'].split(':', 1)[0]}@{receipt['manifest_digest']}"
    token = uuid.uuid4().hex[:12]
    container_name = f"p2-mat-{token}"
    derived_ref = f"local/p2-gold-{token}:dev"
    log_subdir = f"gold_preflight_rescue/attempts/{attempt_id}/logs"
    prep_log_rel = f"experiments/p2_governed_repository_admission/{log_subdir}/{instance_id}.dependency_materialization.log.gz"
    free_before = shutil.disk_usage("/").free
    pull_started = time.monotonic()
    pull = run("docker", "pull", "--platform", "linux/amd64", base_ref, timeout=timeout_seconds)
    pull_seconds = time.monotonic() - pull_started
    if pull.returncode:
        raise RuntimeError(f"base image pull failed for {instance_id}: {pull.stderr[-1000:]}")
    prep_script = "\n".join([
        "set -euo pipefail",
        f"cd /{repo_name}",
        "git reset --hard HEAD",
        config["prepare"],
        "git reset --hard HEAD",
        "git clean -fd",
        "test -z \"$(git status --porcelain)\"",
        "echo __P2_DEPENDENCIES_MATERIALIZED__",
    ])
    prep_started = time.monotonic()
    prep = run(
        "docker", "run", "--name", container_name, "--network", "bridge",
        "--platform", "linux/amd64", "--cap-drop", "ALL",
        "--security-opt", "no-new-privileges", "--pids-limit", "2048",
        "--memory", "8g", "--cpus", "6",
        "-e", "_JAVA_OPTIONS=-Djava.net.preferIPv6Addresses=false",
        "-w", f"/{repo_name}",
        base_ref, "/bin/bash", "-c", prep_script, timeout=timeout_seconds,
    )
    prep_seconds = time.monotonic() - prep_started
    prep_output = (prep.stdout or "") + (prep.stderr or "")
    log_path = ROOT / prep_log_rel
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(log_path, "wt", encoding="utf-8", compresslevel=9) as handle:
        handle.write(prep_output)
    derived_id = None
    derived_size = None
    task_runs = []
    cleanup = []
    try:
        if prep.returncode or "__P2_DEPENDENCIES_MATERIALIZED__" not in prep_output:
            raise RuntimeError(f"dependency materialization failed for {instance_id}")
        commit = run("docker", "commit", container_name, derived_ref, timeout=timeout_seconds)
        if commit.returncode:
            raise RuntimeError(f"derived image commit failed for {instance_id}: {commit.stderr[-1000:]}")
        inspect = run("docker", "image", "inspect", derived_ref, "--format", "{{.Id}} {{.Size}}")
        if inspect.returncode:
            raise RuntimeError(f"derived image inspect failed for {instance_id}")
        derived_id, derived_size_text = inspect.stdout.strip().split()
        derived_size = int(derived_size_text)
        for repetition in range(1, repetitions + 1):
            task_runs.append(v1.execute_arm(
                spec=spec, image_ref=derived_ref, parser=parser_fn,
                solution_patch=None, test_patch=spec["test_patch"],
                arm="baseline_test_patch_only", repetition=repetition,
                timeout_seconds=timeout_seconds, write_logs=True,
                log_subdir=log_subdir,
            ))
            task_runs.append(v1.execute_arm(
                spec=spec, image_ref=derived_ref, parser=parser_fn,
                solution_patch=spec["patch"], test_patch=spec["test_patch"],
                arm="human_gold_plus_test_patch", repetition=repetition,
                timeout_seconds=timeout_seconds, write_logs=True,
                log_subdir=log_subdir,
            ))
    finally:
        for command in [
            ("docker", "rm", "-f", container_name),
            ("docker", "image", "rm", "-f", derived_ref),
            ("docker", "image", "rm", "-f", base_ref),
        ]:
            proc = run(*command)
            cleanup.append({"command": " ".join(command[:3]), "exit_code": proc.returncode})
    return {
        "instance_id": instance_id,
        "rescue_type": "recorded_network_dependency_materialization_then_offline_execution",
        "diagnosis": config["reason"],
        "base_image_ref": base_ref,
        "dependency_prepare_command_sha256": sha256_text(config["prepare"]),
        "dependency_materialization_network": "docker_bridge_development_only",
        "claim_bearing_network_policy_pass": False,
        "preparation_exit_code": prep.returncode,
        "preparation_seconds": round(prep_seconds, 6),
        "preparation_log": prep_log_rel,
        "preparation_log_sha256": sha256_text(prep_output),
        "base_pull_seconds": round(pull_seconds, 6),
        "derived_image_id": derived_id,
        "derived_image_size_bytes": derived_size,
        "runtime_network": "none",
        "all_runs_pass": bool(task_runs) and all(row["pass"] for row in task_runs),
        "runs": task_runs,
        "cleanup": cleanup,
        "host_free_bytes_before": free_before,
        "host_free_bytes_after": shutil.disk_usage("/").free,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-parquet", type=Path, required=True)
    parser.add_argument("--harness-repo", type=Path, required=True)
    parser.add_argument("--repetitions", type=int, default=2)
    parser.add_argument("--timeout-seconds", type=int, default=1200)
    parser.add_argument("--instance-ids", default=",".join(NETWORK_RESCUES))
    parser.add_argument("--attempt-id", default="")
    args = parser.parse_args()
    attempt_id = args.attempt_id or f"2026-07-17-{uuid.uuid4().hex[:12]}"
    if not re.fullmatch(r"[a-zA-Z0-9._-]+", attempt_id):
        raise SystemExit("attempt ID contains unsafe characters")
    attempt_dir = OUT / "attempts" / attempt_id
    checkpoint = attempt_dir / "checkpoint.json"
    attempt_result = attempt_dir / "result.json"
    if v1.sha256_file(args.source_parquet) != v1.EXPECTED_SOURCE_SHA:
        raise SystemExit("source parquet digest mismatch")
    head = run("git", "-C", str(args.harness_repo), "rev-parse", "HEAD")
    if head.returncode or head.stdout.strip() != v1.EXPECTED_HARNESS_COMMIT:
        raise SystemExit("upstream harness commit mismatch")
    prior = json.loads(V1_RESULT.read_text(encoding="utf-8"))
    prior_by_id = {row["instance_id"]: row for row in prior["tasks"]}
    pool = json.loads(v1.POOL.read_text(encoding="utf-8"))
    images = json.loads(v1.IMAGES.read_text(encoding="utf-8"))
    pool_by_id = {row["instance_id"]: row for row in pool["rows"]}
    receipt_by_id = {row["instance_id"]: row for row in images["receipts"]}
    selected = [value for value in args.instance_ids.split(",") if value]
    if not set(selected).issubset(NETWORK_RESCUES):
        raise SystemExit("rescue requested outside the four diagnosed dependency failures")
    ids = set(selected) | {AVA_RESCUE_ID}
    specs = v1.load_selected_rows(args.source_parquet, ids)
    parser_module = load_parsers(args.harness_repo)
    results = [ava_rescue(specs[AVA_RESCUE_ID], prior_by_id[AVA_RESCUE_ID])]
    attempt_dir.mkdir(parents=True, exist_ok=False)
    checkpoint.write_text(json.dumps({
        "schema_version": "asi_stack.p2_gold_preflight_rescue_checkpoint.v1",
        "recorded_date": "2026-07-17",
        "attempt_id": attempt_id,
        "state": "running",
        "completed_rescues": results,
        "final_pool_selected": False,
        "final_pool_opened": False,
        "support_state_effect": "none",
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for instance_id in selected:
        spec = specs[instance_id]
        custody = pool_by_id[instance_id]
        if v1.sha256_text(spec["patch"] or "") != custody["solution_patch_sha256"]:
            raise SystemExit(f"solution patch digest drift: {instance_id}")
        if v1.sha256_text(spec["test_patch"] or "") != custody["test_patch_sha256"]:
            raise SystemExit(f"test patch digest drift: {instance_id}")
        if v1.diff_paths(spec["patch"]) & v1.diff_paths(spec["test_patch"]):
            raise SystemExit(f"solution/test path collision: {instance_id}")
        parser_fn = parser_module.NAME_TO_PARSER.get(spec["install_config"]["log_parser"])
        if parser_fn is None:
            parser_fn = getattr(parser_module, spec["install_config"]["log_parser"])
        try:
            rescued = network_rescue(
                spec=spec, custody=custody, receipt=receipt_by_id[instance_id], parser_fn=parser_fn,
                repetitions=args.repetitions, timeout_seconds=args.timeout_seconds,
                attempt_id=attempt_id,
            )
        except Exception as error:
            rescued = {
                "instance_id": instance_id,
                "rescue_type": "recorded_network_dependency_materialization_then_offline_execution",
                "diagnosis": NETWORK_RESCUES[instance_id]["reason"],
                "all_runs_pass": False,
                "rescue_exception_type": type(error).__name__,
                "rescue_exception": str(error),
                "support_state_effect": "none",
            }
        results.append(rescued)
        checkpoint.write_text(json.dumps({
            "schema_version": "asi_stack.p2_gold_preflight_rescue_checkpoint.v1",
            "recorded_date": "2026-07-17",
            "attempt_id": attempt_id,
            "state": "running",
            "completed_rescues": results,
            "final_pool_selected": False,
            "final_pool_opened": False,
            "support_state_effect": "none",
        }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"{instance_id}: {'PASS' if rescued['all_runs_pass'] else 'FAIL'}", flush=True)
    fixed_denominator = []
    rescue_by_id = {row["instance_id"]: row for row in results}
    for task in prior["tasks"]:
        fixed_denominator.append({
            "instance_id": task["instance_id"],
            "original_pass": task["all_runs_pass"],
            "rescued": task["instance_id"] in rescue_by_id,
            "final_development_preflight_pass": (
                rescue_by_id[task["instance_id"]]["all_runs_pass"]
                if task["instance_id"] in rescue_by_id else task["all_runs_pass"]
            ),
        })
    output = {
        "schema_version": "asi_stack.p2_gold_preflight_rescue.v1",
        "recorded_date": "2026-07-17",
        "attempt_id": attempt_id,
        "state": "passed" if all(row["final_development_preflight_pass"] for row in fixed_denominator) else "instrument_failure",
        "claim_id": prior["claim_id"],
        "scope": "development_only_instrument_rescue",
        "source_parquet_sha256": v1.EXPECTED_SOURCE_SHA,
        "upstream_harness_commit": v1.EXPECTED_HARNESS_COMMIT,
        "original_result": "experiments/p2_governed_repository_admission/gold_preflight/result.json",
        "original_state": prior["state"],
        "original_passed_task_count": prior["passed_task_count"],
        "original_task_count": prior["task_count"],
        "rescue_results": results,
        "fixed_denominator": fixed_denominator,
        "passed_task_count_after_rescue": sum(row["final_development_preflight_pass"] for row in fixed_denominator),
        "task_count": len(fixed_denominator),
        "all_tasks_pass_after_rescue": all(row["final_development_preflight_pass"] for row in fixed_denominator),
        "final_pool_selected": False,
        "final_pool_opened": False,
        "support_state_effect": "none",
        "release_effect": "none",
        "construct_gate_effect": "gold_oracle_subgate_only",
        "remaining_gates": [
            "network_allowlisted_or_hermetic_dependency_snapshot_for_claim_bearing_execution",
            "independent_task_specification_review",
            "candidate_test_path_collision_guard",
            "policy_arm_implementation_and_mechanism_activation",
            "independent_evaluator_calibration",
            "prospective_power_and_sensitivity",
            "frozen_fair_rescue_ladder",
            "resource_ceiling",
        ],
        "non_claims": [
            "Instrument rescue is not a model, governance, safety, coding, transfer, SOTA, release, AGI, or ASI result.",
            "Unrestricted dependency-materialization egress is development-only and does not pass the claim-bearing network policy.",
            "The final pool remains unselected and unopened.",
        ],
    }
    serialized = json.dumps(output, indent=2, ensure_ascii=False) + "\n"
    attempt_result.write_text(serialized, encoding="utf-8")
    RESULT.write_text(serialized, encoding="utf-8")
    checkpoint.write_text(json.dumps({
        "schema_version": "asi_stack.p2_gold_preflight_rescue_checkpoint.v1",
        "recorded_date": "2026-07-17",
        "attempt_id": attempt_id,
        "state": "complete",
        "completed_rescues": results,
        "final_result": f"experiments/p2_governed_repository_admission/gold_preflight_rescue/attempts/{attempt_id}/result.json",
        "final_pool_selected": False,
        "final_pool_opened": False,
        "support_state_effect": "none",
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"P2 rescue {output['state']}: {output['passed_task_count_after_rescue']}/{output['task_count']}; final pool closed.")
    if output["state"] != "passed":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
