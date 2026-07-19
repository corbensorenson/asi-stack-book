#!/usr/bin/env python3
"""Run paired baseline/gold P2 development-task executions.

The final held-out pool is never selected or accessed.  This runner imports the
pinned upstream log parsers, binds images by manifest digest, disables runtime
network access, rejects solution/test path collisions, and retains compressed
raw logs plus exact resource and cleanup receipts.
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
import threading
import time
import types
import uuid
from pathlib import Path

import pyarrow.parquet as pq


ROOT = Path(__file__).resolve().parents[1]
POOL = ROOT / "experiments/p2_governed_repository_admission/corpus/development_pool.json"
IMAGES = ROOT / "experiments/p2_governed_repository_admission/corpus/image_manifest_receipts.json"
OUT_DIR = ROOT / "experiments/p2_governed_repository_admission/gold_preflight"
RESULT = OUT_DIR / "result.json"
EXPECTED_SOURCE_SHA = "0e0bf9355f892ad74ae98d4e1c404f39fd6654a8e351ee3e6ab162e4a64cd3ad"
EXPECTED_HARNESS_COMMIT = "c71902a8cf8d2b725f63d51f199f4d3e56f68d2d"

TIMING_PATTERNS = [
    re.compile(r"\s*\[\s*\d+(?:\.\d+)?\s*(?:ms|s)\s*\]\s*$", re.I),
    re.compile(r"\s+in\s+\d+(?:\.\d+)?\s+(?:msec|sec)\b", re.I),
    re.compile(r"\s*\(\s*\d+(?:\.\d+)?\s*(?:ms|s)\s*\)\s*$", re.I),
]


def normalize_name(value: str) -> str:
    for pattern in TIMING_PATTERNS:
        value = pattern.sub("", value)
    return value.strip()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def diff_paths(diff: str | None) -> set[str]:
    return {
        path
        for match in re.finditer(r"^diff --git a/(.+?) b/(.+)$", diff or "", re.MULTILINE)
        for path in match.groups()
    }


def load_selected_rows(source: Path, ids: set[str]) -> dict[str, dict]:
    parquet = pq.ParquetFile(source)
    rows: dict[str, dict] = {}
    for group in range(parquet.num_row_groups):
        identifiers = parquet.read_row_group(group, columns=["instance_id"])["instance_id"].to_pylist()
        if not ids.intersection(identifiers):
            continue
        for row in parquet.read_row_group(group).to_pylist():
            if row["instance_id"] in ids:
                rows[row["instance_id"]] = row
    if set(rows) != ids:
        raise RuntimeError(f"source rows missing: {sorted(ids - set(rows))}")
    return rows


def run(*args: str, timeout: int | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, capture_output=True, text=True, check=False, timeout=timeout)


def parse_docker_size(value: str) -> int:
    match = re.fullmatch(r"\s*([0-9]+(?:\.[0-9]+)?)\s*([kmgt]?i?b)\s*", value, re.I)
    if not match:
        raise ValueError(f"unrecognized Docker size: {value}")
    number = float(match.group(1))
    unit = match.group(2).lower()
    factors = {
        "b": 1,
        "kb": 1000,
        "mb": 1000**2,
        "gb": 1000**3,
        "tb": 1000**4,
        "kib": 1024,
        "mib": 1024**2,
        "gib": 1024**3,
        "tib": 1024**4,
    }
    return int(number * factors[unit])


def run_monitored_container(args: list[str], *, container_name: str, timeout: int) -> tuple[subprocess.CompletedProcess[str], dict]:
    """Run one container while sampling Docker CPU, memory, and process state."""
    samples: list[dict] = []
    monitor_errors: list[dict] = []
    stop = threading.Event()
    interval = 1.0

    def monitor() -> None:
        while not stop.wait(interval):
            observed = time.monotonic()
            try:
                stats = run(
                    "docker", "stats", "--no-stream",
                    "--format", "{{.CPUPerc}}|{{.MemUsage}}|{{.PIDs}}",
                    container_name,
                    timeout=10,
                )
            except subprocess.TimeoutExpired:
                monitor_errors.append({"kind": "docker_stats_timeout", "observed_monotonic_seconds": observed})
                continue
            if stats.returncode or not stats.stdout.strip():
                monitor_errors.append({"kind": "docker_stats_non_observation", "observed_monotonic_seconds": observed, "return_code": stats.returncode})
                continue
            try:
                cpu_text, memory_text, pids_text = stats.stdout.strip().split("|", 2)
                memory_used = memory_text.split("/", 1)[0].strip()
                samples.append({
                    "monotonic_seconds": observed,
                    "cpu_percent": float(cpu_text.strip().removesuffix("%")),
                    "memory_bytes": parse_docker_size(memory_used),
                    "pids": int(pids_text.strip()),
                })
            except (ValueError, IndexError) as exc:
                monitor_errors.append({"kind": "docker_stats_parse_failure", "observed_monotonic_seconds": observed, "detail": str(exc)})
                continue

    thread = threading.Thread(target=monitor, name=f"monitor-{container_name}", daemon=True)
    thread.start()
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    timed_out = False
    try:
        stdout, stderr = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        run("docker", "rm", "-f", container_name, timeout=30)
        try:
            stdout, stderr = proc.communicate(timeout=30)
        except subprocess.TimeoutExpired:
            proc.kill()
            stdout, stderr = proc.communicate()
    finally:
        stop.set()
        thread.join(timeout=15)
    cpu_seconds = 0.0
    for index, sample in enumerate(samples):
        if index == 0:
            delta = interval
        else:
            delta = max(0.0, sample["monotonic_seconds"] - samples[index - 1]["monotonic_seconds"])
        cpu_seconds += sample["cpu_percent"] / 100.0 * delta
    summary = {
        "sample_interval_seconds": interval,
        "sample_count": len(samples),
        "peak_memory_bytes": max((row["memory_bytes"] for row in samples), default=0),
        "max_cpu_percent": round(max((row["cpu_percent"] for row in samples), default=0.0), 6),
        "integrated_cpu_seconds_estimate": round(cpu_seconds, 6),
        "peak_pids": max((row["pids"] for row in samples), default=0),
        "timed_out": timed_out,
        "monitor_error_count": len(monitor_errors),
        "monitor_errors": monitor_errors,
        "monitor_errors_fail_claim_gate": True,
    }
    return subprocess.CompletedProcess(args, proc.returncode, stdout, stderr), summary


def statuses(parser, output: str) -> dict[str, str]:
    return {normalize_name(name): value for name, value in parser(output).items()}


def execute_arm(
    *, spec: dict, image_ref: str, parser, solution_patch: str | None,
    test_patch: str, arm: str, repetition: int, timeout_seconds: int,
    write_logs: bool, log_subdir: str = "gold_preflight/logs",
    independent_parser_name: str | None = None,
) -> dict:
    repo_name = spec["repo"].split("/", 1)[1]
    test_cmd = spec["install_config"]["test_cmd"]
    if isinstance(test_cmd, list):
        test_commands = [value for value in test_cmd if value.strip()]
    else:
        test_commands = [test_cmd]
    with tempfile.TemporaryDirectory(prefix="p2_gold_") as temp:
        patch_dir = Path(temp)
        (patch_dir / "test_patch.diff").write_text(test_patch, encoding="utf-8")
        lines = ["set -e", "git reset --hard HEAD"]
        if solution_patch is not None:
            (patch_dir / "solution_patch.diff").write_text(solution_patch, encoding="utf-8")
            lines.append("git apply -v --3way --recount --ignore-space-change --whitespace=nowarn /patches/solution_patch.diff")
        lines.extend([
            "git apply -v --3way --recount --ignore-space-change --whitespace=nowarn /patches/test_patch.diff",
            "echo __P2_PATCH_APPLIED__",
            "echo __P2_TEST_STARTED__",
            *test_commands,
            "echo __P2_TEST_COMPLETED__",
        ])
        started = time.monotonic()
        container_name = f"p2-arm-{uuid.uuid4().hex[:12]}"
        docker_args = [
            "docker", "run", "--rm", "--name", container_name,
            "--network", "none", "--platform", "linux/amd64",
            "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
            "--pids-limit", "2048", "--memory", "8g", "--cpus", "6",
            "--tmpfs", "/tmp:rw,nosuid,nodev,exec,size=2g",
            "-e", "_JAVA_OPTIONS=-Djava.net.preferIPv6Addresses=false",
            "-v", f"{patch_dir}:/patches:ro", "-w", f"/{repo_name}",
            image_ref, "/bin/bash", "-c", "\n".join(lines),
        ]
        proc, resource_monitor = run_monitored_container(
            docker_args, container_name=container_name, timeout=timeout_seconds
        )
        duration = time.monotonic() - started
    output = (proc.stdout or "") + (proc.stderr or "")
    parsed = statuses(parser, output)
    independent = None
    dual_evaluator_agreement = True
    if independent_parser_name is not None:
        from p2_independent_test_log_evaluator import evaluate
        independent = evaluate(output, independent_parser_name, proc.returncode)
        dual_evaluator_agreement = parsed == independent["statuses"]
    passed = sorted(name for name, value in parsed.items() if value == "PASSED")
    failed = sorted(name for name, value in parsed.items() if value == "FAILED")
    f2p = {normalize_name(name) for name in spec.get("FAIL_TO_PASS", [])}
    p2p = {normalize_name(name) for name in spec.get("PASS_TO_PASS", [])}
    if arm == "baseline_test_patch_only":
        expected_passed = p2p
        required_failed = f2p
        arm_pass = dual_evaluator_agreement and (
            "__P2_PATCH_APPLIED__" in output
            and "__P2_TEST_STARTED__" in output
            and proc.returncode != 0
            and set(passed) == expected_passed
            and required_failed.issubset(failed)
            and set(failed).issubset(required_failed)
        )
    else:
        expected_passed = p2p | f2p
        required_failed = set()
        arm_pass = dual_evaluator_agreement and (
            "__P2_PATCH_APPLIED__" in output
            and "__P2_TEST_STARTED__" in output
            and "__P2_TEST_COMPLETED__" in output
            and proc.returncode == 0
            and set(passed) == expected_passed
            and not failed
        )
    if Path(log_subdir).is_absolute() or ".." in Path(log_subdir).parts:
        raise ValueError("log_subdir must be a repository-relative descendant")
    log_rel = f"experiments/p2_governed_repository_admission/{log_subdir}/{spec['instance_id']}.{arm}.r{repetition}.log.gz"
    if write_logs:
        log_path = ROOT / log_rel
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with gzip.open(log_path, "wt", encoding="utf-8", compresslevel=9) as handle:
            handle.write(output)
    return {
        "arm": arm,
        "repetition": repetition,
        "pass": arm_pass,
        "exit_code": proc.returncode,
        "duration_seconds": round(duration, 6),
        "resource_monitor": resource_monitor,
        "patch_applied_marker": "__P2_PATCH_APPLIED__" in output,
        "test_started_marker": "__P2_TEST_STARTED__" in output,
        "test_completed_marker": "__P2_TEST_COMPLETED__" in output,
        "expected_passed": sorted(expected_passed),
        "required_failed": sorted(required_failed),
        "passed_actual": passed,
        "failed_actual": failed,
        "independent_evaluator": independent,
        "dual_evaluator_exact_agreement": dual_evaluator_agreement,
        "output_sha256": sha256_text(output),
        "output_bytes": len(output.encode()),
        "compressed_log_path": log_rel if write_logs else None,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-parquet", type=Path, required=True)
    parser.add_argument("--harness-repo", type=Path, required=True)
    parser.add_argument("--instance-ids", default="")
    parser.add_argument("--repetitions", type=int, default=2)
    parser.add_argument("--timeout-seconds", type=int, default=1200)
    parser.add_argument("--write-result", action="store_true")
    parser.add_argument("--result-subdir", default="gold_preflight")
    args = parser.parse_args()
    if args.repetitions < 1:
        raise SystemExit("repetitions must be positive")
    result_subdir = Path(args.result_subdir)
    if result_subdir.is_absolute() or ".." in result_subdir.parts:
        raise SystemExit("result-subdir must be a repository-relative descendant")
    out_dir = ROOT / "experiments/p2_governed_repository_admission" / result_subdir
    result_path = out_dir / "result.json"
    log_subdir = f"{result_subdir.as_posix()}/logs"
    if sha256_file(args.source_parquet) != EXPECTED_SOURCE_SHA:
        raise SystemExit("source parquet digest mismatch")
    head = run("git", "-C", str(args.harness_repo), "rev-parse", "HEAD")
    if head.returncode or head.stdout.strip() != EXPECTED_HARNESS_COMMIT:
        raise SystemExit("upstream harness commit mismatch")
    sys.path.insert(0, str(args.harness_repo))
    sys.path.insert(0, str(args.harness_repo / "lib"))
    parser_source = args.harness_repo / "lib/agent/log_parsers.py"
    log_parsers = types.ModuleType("p2_upstream_log_parsers")
    log_parsers.__file__ = str(parser_source)
    exec(
        compile(
            parser_source.read_text(encoding="utf-8"), str(parser_source), "exec",
            flags=__future__.annotations.compiler_flag,
        ),
        log_parsers.__dict__,
    )

    pool = json.loads(POOL.read_text(encoding="utf-8"))
    image_receipts = json.loads(IMAGES.read_text(encoding="utf-8"))
    selected = [value for value in args.instance_ids.split(",") if value] if args.instance_ids else [row["instance_id"] for row in pool["rows"]]
    pool_by_id = {row["instance_id"]: row for row in pool["rows"]}
    receipt_by_id = {row["instance_id"]: row for row in image_receipts["receipts"]}
    if not set(selected).issubset(pool_by_id):
        raise SystemExit("requested IDs are outside the development pool")
    specs = load_selected_rows(args.source_parquet, set(selected))
    host_before = shutil.disk_usage("/").free
    results = []
    for instance_id in selected:
        spec = specs[instance_id]
        custody = pool_by_id[instance_id]
        if sha256_text(spec["problem_statement"] or "") != custody["problem_statement_sha256"]:
            raise SystemExit(f"problem statement digest drift: {instance_id}")
        if sha256_text(spec["patch"] or "") != custody["solution_patch_sha256"]:
            raise SystemExit(f"solution patch digest drift: {instance_id}")
        if sha256_text(spec["test_patch"] or "") != custody["test_patch_sha256"]:
            raise SystemExit(f"test patch digest drift: {instance_id}")
        overlap = sorted(diff_paths(spec["patch"]) & diff_paths(spec["test_patch"]))
        if overlap:
            raise SystemExit(f"solution/test path collision: {instance_id}: {overlap}")
        receipt = receipt_by_id[instance_id]
        image_ref = f"{spec['image_name'].split(':', 1)[0]}@{receipt['manifest_digest']}"
        free_before = shutil.disk_usage("/").free
        pull_started = time.monotonic()
        pull = run("docker", "pull", "--platform", "linux/amd64", image_ref, timeout=args.timeout_seconds)
        pull_seconds = time.monotonic() - pull_started
        if pull.returncode:
            raise SystemExit(f"image pull failed: {instance_id}: {pull.stderr[-1000:]}")
        inspect = run("docker", "image", "inspect", image_ref, "--format", "{{.Id}} {{.Size}}")
        if inspect.returncode:
            raise SystemExit(f"image inspect failed: {instance_id}")
        image_id, expanded_size = inspect.stdout.strip().split()
        free_after_pull = shutil.disk_usage("/").free
        task_runs = []
        try:
            parser_fn = log_parsers.NAME_TO_PARSER.get(spec["install_config"]["log_parser"])
            if parser_fn is None:
                parser_fn = getattr(log_parsers, spec["install_config"]["log_parser"])
            for repetition in range(1, args.repetitions + 1):
                task_runs.append(execute_arm(
                    spec=spec, image_ref=image_ref, parser=parser_fn,
                    solution_patch=None, test_patch=spec["test_patch"],
                    arm="baseline_test_patch_only", repetition=repetition,
                    timeout_seconds=args.timeout_seconds, write_logs=args.write_result,
                    log_subdir=log_subdir,
                ))
                task_runs.append(execute_arm(
                    spec=spec, image_ref=image_ref, parser=parser_fn,
                    solution_patch=spec["patch"], test_patch=spec["test_patch"],
                    arm="human_gold_plus_test_patch", repetition=repetition,
                    timeout_seconds=args.timeout_seconds, write_logs=args.write_result,
                    log_subdir=log_subdir,
                ))
        finally:
            cleanup_started = time.monotonic()
            cleanup = run("docker", "image", "rm", "-f", image_ref)
            cleanup_seconds = time.monotonic() - cleanup_started
        results.append({
            "instance_id": instance_id,
            "repo": spec["repo"],
            "base_commit": spec["base_commit"],
            "language": spec["language"],
            "license": spec["license"],
            "image_ref": image_ref,
            "image_id": image_id,
            "manifest_digest": receipt["manifest_digest"],
            "pull_seconds": round(pull_seconds, 6),
            "expanded_image_size_bytes": int(expanded_size),
            "host_free_bytes_before_pull": free_before,
            "host_free_bytes_after_pull": free_after_pull,
            "host_free_bytes_after_cleanup": shutil.disk_usage("/").free,
            "cleanup_exit_code": cleanup.returncode,
            "cleanup_seconds": round(cleanup_seconds, 6),
            "cleanup_output_sha256": sha256_text((cleanup.stdout or "") + (cleanup.stderr or "")),
            "all_runs_pass": all(row["pass"] for row in task_runs),
            "runs": task_runs,
        })
        print(f"{instance_id}: {'PASS' if results[-1]['all_runs_pass'] else 'FAIL'} ({len(task_runs)} paired-arm runs)", flush=True)

    result = {
        "schema_version": "asi_stack.p2_gold_preflight.v1",
        "recorded_date": "2026-07-17",
        "state": "passed" if all(row["all_runs_pass"] for row in results) else "instrument_failure",
        "claim_id": "p2.governed_natural_repository_change_admission_joint_frontier",
        "scope": "development_only_gold_oracle_and_harness_preflight",
        "source_parquet_sha256": EXPECTED_SOURCE_SHA,
        "upstream_harness_commit": EXPECTED_HARNESS_COMMIT,
        "runtime_network": "none",
        "container_platform": "linux/amd64",
        "host_platform": "Apple M1 arm64",
        "repetitions_per_arm": args.repetitions,
        "task_count": len(results),
        "passed_task_count": sum(row["all_runs_pass"] for row in results),
        "all_tasks_pass": all(row["all_runs_pass"] for row in results),
        "host_free_bytes_before": host_before,
        "host_free_bytes_after": shutil.disk_usage("/").free,
        "final_pool_selected": False,
        "final_pool_opened": False,
        "construct_gate_effect": "gold_execution_subgate_only_independent_task_review_still_required",
        "resource_gate_effect": "development_measurement_only_final_ceiling_still_pending",
        "support_state_effect": "none",
        "release_effect": "none",
        "tasks": results,
        "non_claims": [
            "Human-gold execution calibrates the harness; it is not model-generated task success.",
            "Development-task pass does not establish independent evaluator, policy-arm, sensitivity, rescue, or final-heldout competence.",
            "Successful tests do not establish authority, rollback, residual, safety, transfer, SOTA, AGI, or ASI.",
        ],
    }
    if args.write_result:
        out_dir.mkdir(parents=True, exist_ok=True)
        result_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"P2 gold preflight {result['state']}: {result['passed_task_count']}/{result['task_count']} tasks; final pool closed.")
    if not result["all_tasks_pass"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
