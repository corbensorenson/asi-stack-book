#!/usr/bin/env python3
"""Qualify one opened sequential replacement under the frozen offline contract."""

from __future__ import annotations

import __future__
import argparse
import gzip
import hashlib
import json
import shutil
import sys
import time
import types
import uuid
from datetime import datetime, timezone
from pathlib import Path

from run_p2_gold_preflight import execute_arm, load_selected_rows, run, run_monitored_container, sha256_file, sha256_text
from run_p2_sequential_candidate_image_preflight import stabilize, virtual_upper


ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path("/tmp/swe-rebench-v2.parquet")
HARNESS = Path("/tmp/swe-rebench-v2-code.7ixeFl")
SOURCE_SHA = "0e0bf9355f892ad74ae98d4e1c404f39fd6654a8e351ee3e6ab162e4a64cd3ad"
HARNESS_COMMIT = "c71902a8cf8d2b725f63d51f199f4d3e56f68d2d"
CALIBRATION = ROOT / "evidence_quality/p2_independent_test_log_evaluator_calibration.json"
RESOURCE = ROOT / "evidence_quality/p2_resource_ceiling.json"
OUT_ROOT = ROOT / "experiments/p2_governed_repository_admission/sequential_qualification/attempts"


def write_gzip(path: Path, text: str) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(path, "wt", encoding="utf-8", compresslevel=9) as handle:
        handle.write(text)
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dependency_command(spec: dict) -> str:
    parser = spec["install_config"]["log_parser"]
    if parser == "parse_log_cargo":
        return "cargo fetch --locked --offline"
    if parser == "parse_log_gotest":
        prefix = "cd github && " if spec["instance_id"] == "google__go-github-3619" else ""
        return prefix + "GOPROXY=off go mod download && GOPROXY=off go mod verify"
    if parser == "parse_java_mvn":
        return "./mvnw -o --no-transfer-progress -DskipTests dependency:go-offline && ./mvnw -o --no-transfer-progress -DskipTests test-compile"
    raise ValueError(f"unsupported parser: {parser}")


def resource_gates(row: dict, ceiling: dict) -> dict:
    monitor = row["resource_monitor"]
    duration = row["duration_seconds"]
    return {
        "arm_wall_within_seconds": duration <= ceiling["arm_wall_seconds"],
        "monitor_sample_present_when_required": duration < 3 or monitor["sample_count"] >= 1,
        "monitor_error_free": monitor.get("monitor_error_count", 0) == 0,
        "not_timed_out": not monitor["timed_out"],
        "peak_memory_within_bytes": monitor["peak_memory_bytes"] <= ceiling["peak_memory_bytes"],
        "max_cpu_within_percent": monitor["max_cpu_percent"] <= ceiling["max_cpu_percent"],
        "integrated_cpu_estimate_within_seconds": monitor["integrated_cpu_seconds_estimate"] <= ceiling["integrated_cpu_seconds_estimate"],
        "peak_pids_within_count": monitor["peak_pids"] <= ceiling["peak_pids"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--opening", required=True)
    parser.add_argument("--provenance", required=True)
    parser.add_argument("--attempt-id", required=True)
    args = parser.parse_args()
    out = OUT_ROOT / args.attempt_id
    if out.exists():
        raise SystemExit(f"immutable attempt exists: {out}")
    out.mkdir(parents=True)

    opening = json.loads((ROOT / args.opening).read_text())
    provenance = json.loads((ROOT / args.provenance).read_text())
    calibration = json.loads(CALIBRATION.read_text())
    resource = json.loads(RESOURCE.read_text())
    ceiling = resource["task_acceptance_ceilings"]
    selected = opening["candidate"]
    receipt = provenance["candidate"]
    if opening["state"] != "task_spec_opened_outcome_unopened" or not opening["opening_gates"]["source_queue_digests_match"]:
        raise SystemExit("task-opening gate failed")
    if receipt["instance_id"] != selected["instance_id"] or receipt["image_manifest"]["digest"] != selected["image_manifest_digest"]:
        raise SystemExit("opening/provenance identity drift")
    if calibration["state"] != "passed" or calibration["exact_agreement_count"] != calibration["total_case_count"]:
        raise SystemExit("independent evaluator is not calibrated")
    if sha256_file(SOURCE) != SOURCE_SHA or run("git", "-C", str(HARNESS), "rev-parse", "HEAD").stdout.strip() != HARNESS_COMMIT:
        raise SystemExit("source or harness drift")

    spec = load_selected_rows(SOURCE, {selected["instance_id"]})[selected["instance_id"]]
    if (
        sha256_text(spec["problem_statement"] or "") != selected["problem_statement_sha256"]
        or sha256_text(spec["patch"] or "") != selected["solution_patch_sha256"]
        or sha256_text(spec["test_patch"] or "") != selected["test_patch_sha256"]
    ):
        raise SystemExit("opened task digest drift")

    sys.path.insert(0, str(HARNESS))
    sys.path.insert(0, str(HARNESS / "lib"))
    parser_source = HARNESS / "lib/agent/log_parsers.py"
    upstream = types.ModuleType("p2_sequential_qualification_upstream")
    upstream.__file__ = str(parser_source)
    exec(compile(parser_source.read_text(), str(parser_source), "exec", flags=__future__.annotations.compiler_flag), upstream.__dict__)
    parser_fn = upstream.NAME_TO_PARSER[spec["install_config"]["log_parser"]]

    image = receipt["image_manifest"]["image"]
    digest = receipt["image_manifest"]["digest"]
    image_ref = image.split(":", 1)[0] + "@" + digest
    host_before = shutil.disk_usage("/").free
    result = {
        "schema_version": "asi_stack.p2_sequential_candidate_qualification.v1",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "attempt_id": args.attempt_id,
        "opening_path": args.opening,
        "provenance_path": args.provenance,
        "resource_ceiling_path": "evidence_quality/p2_resource_ceiling.json",
        "instance_id": selected["instance_id"],
        "slot": selected["slot"],
        "rank": selected["rank"],
        "source_parquet_sha256": SOURCE_SHA,
        "upstream_harness_commit": HARNESS_COMMIT,
        "independent_evaluator_sha256": calibration["independent_evaluator_sha256"],
        "image_ref": image_ref,
        "manifest_digest": digest,
        "host_free_before_bytes": host_before,
        "runtime_network": "none",
        "dependency_network": "none",
        "repetitions_per_arm": 2,
        "runs": [],
        "task_content_opened": True,
        "candidate_outcome_opened": False,
        "final_pool_selected": False,
        "final_pool_opened": False,
        "support_state_effect": "none",
        "release_effect": "none",
    }
    active_containers = set()
    pulled = False
    terminal = ["n0_instrument_failure", "runner_did_not_complete", "runner did not reach a classified terminal state"]

    def set_terminal(state: str, code: str, detail: str) -> None:
        terminal[:] = [state, code, detail]

    try:
        if host_before < ceiling["minimum_host_free_bytes_before_task"]:
            set_terminal("n0_resource_failure", "host_free_below_minimum", "image pull not attempted")
            return
        pull_started = time.monotonic()
        pull = run("docker", "pull", "--platform", "linux/amd64", image_ref, timeout=ceiling["image_pull_seconds"])
        pull_wall = time.monotonic() - pull_started
        pull_log = out / "pull.log.gz"
        result["pull"] = {
            "exit_code": pull.returncode,
            "wall_seconds": round(pull_wall, 6),
            "log_path": pull_log.relative_to(ROOT).as_posix(),
            "log_sha256": write_gzip(pull_log, (pull.stdout or "") + (pull.stderr or "")),
        }
        pulled = pull.returncode == 0
        if pull.returncode or pull_wall > ceiling["image_pull_seconds"]:
            set_terminal("n0_resource_failure", "image_pull_failure_or_ceiling", "exact image unavailable within frozen ceiling")
            return

        inspect = run("docker", "image", "inspect", image_ref, "--format", "{{json .}}")
        info = json.loads(inspect.stdout) if inspect.returncode == 0 else {}
        display, upper = virtual_upper(info.get("Id", ""))
        image_gates = {
            "inspect_exit_zero": inspect.returncode == 0,
            "manifest_digest_present": any(value.endswith("@" + digest) for value in info.get("RepoDigests", [])),
            "linux_amd64": info.get("Os") == "linux" and info.get("Architecture") == "amd64",
            "engine_content_within_ceiling": info.get("Size", 10**30) <= ceiling["engine_content_size_bytes"],
            "virtual_size_within_ceiling": upper is not None and upper <= ceiling["virtual_size_conservative_upper_bound_bytes"],
        }
        result["image_measurement"] = {
            "engine_content_size_bytes": info.get("Size"),
            "virtual_size_display": display,
            "virtual_size_conservative_upper_bound_bytes": upper,
            "gates": image_gates,
        }
        if not all(image_gates.values()):
            set_terminal("n0_resource_failure", "image_measurement_gate_failure", "exact image failed repeated prospective measurement")
            return

        repo_dir = spec["repo"].split("/", 1)[1]
        setup_name = f"p2-seq-deps-{uuid.uuid4().hex[:10]}"
        active_containers.add(setup_name)
        setup_cmd = dependency_command(spec)
        setup_args = [
            "docker", "run", "--name", setup_name, "--network", "none", "--platform", "linux/amd64",
            "--cap-drop", "ALL", "--security-opt", "no-new-privileges", "--pids-limit", "2048",
            "--memory", "8g", "--cpus", "6", "--tmpfs", "/tmp:rw,nosuid,nodev,exec,size=2g",
            "-w", f"/{repo_dir}", image_ref, "/bin/bash", "-lc", "set -e\ngit reset --hard HEAD\n" + setup_cmd,
        ]
        started = time.monotonic()
        setup, setup_monitor = run_monitored_container(setup_args, container_name=setup_name, timeout=ceiling["dependency_materialization_seconds"])
        setup_wall = time.monotonic() - started
        removal = run("docker", "rm", "-f", setup_name)
        active_containers.discard(setup_name)
        setup_log = out / "dependency_setup.log.gz"
        setup_gates = {
            "exit_zero": setup.returncode == 0,
            "within_seconds": setup_wall <= ceiling["dependency_materialization_seconds"],
            "not_timed_out": not setup_monitor["timed_out"],
            "monitor_error_free": setup_monitor.get("monitor_error_count", 0) == 0,
            "peak_memory_within_bytes": setup_monitor["peak_memory_bytes"] <= ceiling["peak_memory_bytes"],
            "peak_pids_within_count": setup_monitor["peak_pids"] <= ceiling["peak_pids"],
            "container_cleanup_exit_zero": removal.returncode == 0,
        }
        result["dependency_setup"] = {
            "command": setup_cmd,
            "network": "none",
            "task_patch_applied": False,
            "exit_code": setup.returncode,
            "wall_seconds": round(setup_wall, 6),
            "resource_monitor": setup_monitor,
            "container_cleanup_exit_code": removal.returncode,
            "log_path": setup_log.relative_to(ROOT).as_posix(),
            "log_sha256": write_gzip(setup_log, (setup.stdout or "") + (setup.stderr or "")),
            "gates": setup_gates,
        }
        if not all(setup_gates.values()):
            set_terminal("n0_dependency_failure", "offline_dependency_gate_failure", "unpatched offline dependency setup failed before candidate execution")
            return

        for repetition in (1, 2):
            for arm, solution in (("baseline_test_patch_only", None), ("human_gold_plus_test_patch", spec["patch"])):
                row = execute_arm(
                    spec=spec, image_ref=image_ref, parser=parser_fn, solution_patch=solution,
                    test_patch=spec["test_patch"], arm=arm, repetition=repetition,
                    timeout_seconds=ceiling["arm_wall_seconds"], write_logs=True,
                    log_subdir=f"sequential_qualification/attempts/{args.attempt_id}/logs",
                    independent_parser_name=spec["install_config"]["log_parser"],
                )
                row["resource_gates"] = resource_gates(row, ceiling)
                row["resource_gate_pass"] = all(row["resource_gates"].values())
                row["compressed_log_sha256"] = sha256_file(ROOT / row["compressed_log_path"])
                result["runs"].append(row)
                (out / "checkpoint.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
        passed = len(result["runs"]) == 4 and all(
            row["pass"] and row["dual_evaluator_exact_agreement"] and row["resource_gate_pass"]
            for row in result["runs"]
        )
        set_terminal(
            "qualified" if passed else "n0_construct_instrument_or_resource_failure",
            "all_gates_passed" if passed else "paired_outcome_gate_failure",
            "two baseline and two human-gold arms completed under dual evaluation",
        )
    except Exception as exc:
        set_terminal("n0_instrument_failure", "unhandled_runner_exception", f"{type(exc).__name__}: {exc}")
    finally:
        container_cleanup = []
        for name in sorted(active_containers):
            proc = run("docker", "rm", "-f", name)
            container_cleanup.append({"name": name, "exit_code": proc.returncode, "output_sha256": sha256_text((proc.stdout or "") + (proc.stderr or ""))})
        image_cleanup = None
        if pulled:
            proc = run("docker", "image", "rm", "-f", image_ref)
            image_cleanup = {"ref": image_ref, "exit_code": proc.returncode, "output_sha256": sha256_text((proc.stdout or "") + (proc.stderr or ""))}
        stabilization = stabilize(host_before, ceiling)
        result["cleanup"] = {"container_removals": container_cleanup, "image_removal": image_cleanup, "stabilization": stabilization}
        state, code, detail = terminal
        cleanup_nonzero = any(row["exit_code"] for row in container_cleanup) or (image_cleanup is not None and image_cleanup["exit_code"] != 0)
        if state == "qualified" and (
            cleanup_nonzero or not stabilization["stable"]
            or stabilization["host_free_byte_loss"] > ceiling["maximum_post_cleanup_host_free_byte_loss"]
        ):
            state, code, detail = "n0_resource_failure", "cleanup_stabilization_or_residual_failure", "paired arms passed but cleanup gate failed"
        all_runs_pass = len(result["runs"]) == 4 and all(
            row.get("pass") and row.get("dual_evaluator_exact_agreement") and row.get("resource_gate_pass")
            for row in result["runs"]
        )
        result.update({
            "state": state,
            "terminal_code": code,
            "terminal_detail": detail,
            "host_free_after_bytes": stabilization["host_free_after_bytes"],
            "host_free_byte_loss": stabilization["host_free_byte_loss"],
            "candidate_outcome_opened": bool(result["runs"]),
            "all_runs_pass": all_runs_pass,
            "qualified_replacement": state == "qualified" and all_runs_pass,
        })
        (out / "result.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
        print(f"{selected['instance_id']}: {state} {code}", flush=True)


if __name__ == "__main__":
    main()
