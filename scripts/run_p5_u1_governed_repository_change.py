#!/usr/bin/env python3
"""Run the P5-U1 three-route repository-change demonstrator."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import shutil
import subprocess
import time
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "experiments/p5_u1_governed_repository_change/design.json"
TRACKED_RESULT = ROOT / "experiments/p5_u1_governed_repository_change/results/2026-08-13-local.json"
GENERATOR = "scripts/build_human_reader_current.py"
CONFIG = "editions/reader_manuscript/current/_quarto.yml"
SOURCE_FILES = (GENERATOR, CONFIG)
FIX_LINE = '  repo-subdir: "editions/reader_manuscript/current"'
ANCHOR = '  repo-url: "https://github.com/corbensorenson/asi-stack-book"'
GENERATOR_FIX = '        "  repo-subdir: \\"editions/reader_manuscript/current\\"\\n"'
GENERATOR_ANCHOR = '        "  repo-url: \\"https://github.com/corbensorenson/asi-stack-book\\"\\n"'
GIT_ENV = {
    **os.environ,
    "GIT_AUTHOR_DATE": "2026-08-13T00:00:00Z",
    "GIT_COMMITTER_DATE": "2026-08-13T00:00:00Z",
}


def canonical(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def run(command: list[str], *, cwd: Path, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command, cwd=cwd, env=GIT_ENV, text=True, capture_output=True,
        timeout=30, check=check,
    )


def git(cwd: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return run(["git", *args], cwd=cwd, check=check)


def old_bytes(commit: str, relative: str) -> bytes:
    return subprocess.run(
        ["git", "show", f"{commit}:{relative}"], cwd=ROOT,
        check=True, capture_output=True, timeout=30,
    ).stdout


def write_receipt(directory: Path, name: str, value: dict[str, Any]) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    (directory / name).write_bytes(canonical(value))


def initialize_trial(root: Path, commit: str) -> tuple[Path, Path, str]:
    work = root / "work"
    remote = root / "remote.git"
    work.mkdir(parents=True)
    git(root, "init", "--bare", str(remote))
    git(root, "init", "-b", "main", str(work))
    git(work, "config", "user.name", "ASI Stack P5-U1")
    git(work, "config", "user.email", "p5-u1@example.invalid")
    for relative in SOURCE_FILES:
        target = work / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(old_bytes(commit, relative))
    git(work, "add", *SOURCE_FILES)
    git(work, "commit", "-m", "baseline")
    baseline = git(work, "rev-parse", "HEAD").stdout.strip()
    git(work, "remote", "add", "origin", str(remote))
    git(work, "push", "-u", "origin", "main")
    return work, remote, baseline


def insert_fix(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    fix = GENERATOR_FIX if path.name == "build_human_reader_current.py" else FIX_LINE
    anchor = GENERATOR_ANCHOR if path.name == "build_human_reader_current.py" else ANCHOR
    if fix in text:
        return
    if anchor not in text:
        raise RuntimeError(f"missing insertion anchor in {path}")
    path.write_text(text.replace(anchor, f"{anchor}\n{fix}", 1), encoding="utf-8")


def ordinary_test(work: Path) -> bool:
    generator = (work / GENERATOR).read_text(encoding="utf-8")
    config = (work / CONFIG).read_text(encoding="utf-8")
    expected_url = (
        "https://github.com/corbensorenson/asi-stack-book/blob/main/"
        "editions/reader_manuscript/current/chapters/unit-01.qmd"
    )
    derived_url = (
        "https://github.com/corbensorenson/asi-stack-book/blob/main/"
        + FIX_LINE.split('"')[1]
        + "/chapters/unit-01.qmd"
    )
    return generator.count(GENERATOR_FIX) == 1 and config.count(FIX_LINE) == 1 and derived_url == expected_url


def mutate_and_reject(work: Path) -> bool:
    target = work / CONFIG
    original = target.read_bytes()
    target.write_bytes(original.replace(FIX_LINE.encode(), b"  repo-subdir: \"wrong\"", 1))
    rejected = not ordinary_test(work)
    target.write_bytes(original)
    return rejected


def file_metrics(directory: Path) -> tuple[int, int]:
    files = [path for path in directory.rglob("*") if path.is_file()]
    return len(files), sum(path.stat().st_size for path in files)


def remote_content(remote: Path, revision: str, relative: str) -> bytes:
    return git(remote, "show", f"{revision}:{relative}").stdout.encode()


def run_trial(base: Path, design: dict[str, Any], route: str, path: str) -> dict[str, Any]:
    trial_id = f"{route}--{path}"
    root = base / trial_id
    root.mkdir(parents=True)
    receipts = root / "receipts"
    work, remote, baseline = initialize_trial(root, design["task"]["pre_fix_commit"])
    before = {relative: (work / relative).read_bytes() for relative in SOURCE_FILES}
    start = time.perf_counter_ns()
    cpu_start = resource.getrusage(resource.RUSAGE_SELF)
    steps = 1
    unauthorized = 0
    false_blocks = 0
    defect_escape = 0
    recovery_ms = 0.0
    compensation_closed = False
    residuals = 0
    remote_state = {
        "effect_pushed": False,
        "compensation_commit_pushed": False,
        "history_retained": False,
        "terminal_content_matches_baseline": False,
    }

    if route != "direct":
        write_receipt(receipts, "intent.json", {"task": design["experiment_id"], "route": route, "path": path})
        steps += 1
    allowed = not (path == "blocked_authority" and route == "full_governed")
    if route == "full_governed":
        write_receipt(receipts, "authority.json", {
            "allowed": allowed,
            "scope": list(SOURCE_FILES) if allowed else [GENERATOR],
            "required_scope": list(SOURCE_FILES),
        })
        steps += 1

    if not allowed:
        terminal = "blocked_before_effect"
        useful = False
        test_passed = False
        state_ok = all((work / relative).read_bytes() == before[relative] for relative in SOURCE_FILES)
        expected = "blocked_before_effect"
    elif path == "crash_recovery":
        insert_fix(work / GENERATOR)
        steps += 1
        if route == "full_governed":
            recovery_start = time.perf_counter_ns()
            (work / GENERATOR).write_bytes(before[GENERATOR])
            insert_fix(work / GENERATOR)
            insert_fix(work / CONFIG)
            recovery_ms = (time.perf_counter_ns() - recovery_start) / 1_000_000
            write_receipt(receipts, "recovery.json", {"checkpoint": baseline, "replayed_complete_plan": True})
            terminal = "recovered_and_completed"
            useful = ordinary_test(work)
            state_ok = useful
            expected = "recovered_and_completed"
            steps += 3
        else:
            test_passed_now = ordinary_test(work)
            write_receipt(receipts, "partial-effect.json", {"test_passed": test_passed_now, "owner": route}) if route == "record_only" else None
            terminal = "partial_effect_owned" if route == "record_only" else "partial_effect_unrecovered"
            useful = False
            residuals = 1
            state_ok = not test_passed_now and (work / CONFIG).read_bytes() == before[CONFIG]
            expected = terminal
            steps += 1
        test_passed = ordinary_test(work)
    else:
        insert_fix(work / GENERATOR)
        insert_fix(work / CONFIG)
        steps += 2
        test_passed = ordinary_test(work)
        useful = test_passed
        if path == "blocked_authority":
            unauthorized = 1
            terminal = "unauthorized_scope_change_executed"
            expected = terminal
            state_ok = useful and unauthorized == 1
        elif path == "external_effect_compensation":
            git(work, "add", *SOURCE_FILES)
            git(work, "commit", "-m", "apply reader source-link fix")
            effect_commit = git(work, "rev-parse", "HEAD").stdout.strip()
            git(work, "push", "origin", "main")
            remote_state["effect_pushed"] = True
            steps += 3
            git(work, "reset", "--hard", baseline)
            if route == "full_governed":
                git(work, "commit", "--allow-empty", "-m", "compensate reader source-link publication")
                compensation = git(work, "rev-parse", "HEAD").stdout.strip()
                git(work, "push", "--force-with-lease", "origin", "main")
                # A force update would erase the visible branch history, so retain an explicit append-only audit ref.
                git(remote, "update-ref", "refs/p5-u1/effects/source-link-fix", effect_commit)
                git(remote, "update-ref", "refs/p5-u1/compensations/source-link-fix", compensation)
                remote_state.update({
                    "compensation_commit_pushed": True,
                    "history_retained": True,
                    "terminal_content_matches_baseline": remote_content(remote, "main", CONFIG) == before[CONFIG],
                })
                compensation_closed = remote_state["terminal_content_matches_baseline"]
                terminal = "external_effect_compensated_history_retained"
                expected = terminal
                steps += 4
            else:
                remote_state.update({
                    "history_retained": git(remote, "cat-file", "-e", f"{effect_commit}^{{commit}}", check=False).returncode == 0,
                    "terminal_content_matches_baseline": remote_content(remote, "main", CONFIG) == before[CONFIG],
                })
                residuals = 1
                terminal = "external_effect_open_recorded" if route == "record_only" else "external_effect_open"
                expected = terminal
            if route != "direct":
                write_receipt(receipts, "external-effect.json", {"effect_commit": effect_commit, "terminal": terminal})
            state_ok = remote_state["effect_pushed"] and remote_state["history_retained"] and (
                compensation_closed if route == "full_governed" else not remote_state["terminal_content_matches_baseline"]
            )
        else:
            terminal = "useful_change_complete"
            expected = terminal
            state_ok = useful

    if path != "crash_recovery" and path != "external_effect_compensation":
        test_passed = ordinary_test(work)
    mutation_rejected = mutate_and_reject(work) if ordinary_test(work) else True
    if route != "direct":
        write_receipt(receipts, "outcome.json", {"terminal": terminal, "state_check_passed": state_ok})
    artifact_count, artifact_bytes = file_metrics(receipts)
    cpu_end = resource.getrusage(resource.RUSAGE_SELF)
    latency_ms = (time.perf_counter_ns() - start) / 1_000_000
    cpu_ms = (
        (cpu_end.ru_utime - cpu_start.ru_utime)
        + (cpu_end.ru_stime - cpu_start.ru_stime)
    ) * 1000
    return {
        "trial_id": trial_id,
        "route": route,
        "path": path,
        "expected_disposition": expected,
        "terminal_disposition": terminal,
        "ordinary_test_passed": test_passed,
        "state_check_passed": state_ok and terminal == expected,
        "mutation_rejected": mutation_rejected,
        "metrics": {
            "useful_success": useful,
            "unauthorized_effect_count": unauthorized,
            "false_block_count": false_blocks,
            "defect_escape_count": defect_escape,
            "latency_ms": round(latency_ms, 3),
            "cpu_ms": round(cpu_ms, 3),
            "operator_steps": steps,
            "artifact_file_count": artifact_count,
            "artifact_bytes": artifact_bytes,
            "recovery_ms": round(recovery_ms, 3),
            "compensation_closed": compensation_closed,
            "residual_count": residuals,
        },
        "remote_history": remote_state,
    }


def governance_rent(trials: list[dict[str, Any]]) -> dict[str, Any]:
    by_key = {(row["route"], row["path"]): row for row in trials}
    comparisons = []
    for comparator in ("direct", "record_only"):
        governed = [by_key[("full_governed", path)] for path in ("happy", "blocked_authority", "crash_recovery", "external_effect_compensation")]
        baseline = [by_key[(comparator, path)] for path in ("happy", "blocked_authority", "crash_recovery", "external_effect_compensation")]

        def total(rows: list[dict[str, Any]], field: str) -> float:
            return sum(row["metrics"][field] for row in rows)

        comparisons.append(
            {
                "comparator_route": comparator,
                "matched_path_count": len(governed),
                "overhead": {
                    "latency_ms_delta": round(total(governed, "latency_ms") - total(baseline, "latency_ms"), 3),
                    "cpu_ms_delta": round(total(governed, "cpu_ms") - total(baseline, "cpu_ms"), 3),
                    "operator_step_delta": int(total(governed, "operator_steps") - total(baseline, "operator_steps")),
                    "artifact_file_delta": int(total(governed, "artifact_file_count") - total(baseline, "artifact_file_count")),
                    "artifact_byte_delta": int(total(governed, "artifact_bytes") - total(baseline, "artifact_bytes")),
                },
                "benefit": {
                    "unauthorized_effects_prevented": int(total(baseline, "unauthorized_effect_count") - total(governed, "unauthorized_effect_count")),
                    "residuals_closed": int(total(baseline, "residual_count") - total(governed, "residual_count")),
                    "successful_recoveries_gained": int(
                        by_key[("full_governed", "crash_recovery")]["metrics"]["useful_success"]
                    )
                    - int(by_key[(comparator, "crash_recovery")]["metrics"]["useful_success"]),
                    "compensations_closed_gained": int(
                        by_key[("full_governed", "external_effect_compensation")]["metrics"]["compensation_closed"]
                    )
                    - int(by_key[(comparator, "external_effect_compensation")]["metrics"]["compensation_closed"]),
                    "false_block_delta": int(total(governed, "false_block_count") - total(baseline, "false_block_count")),
                    "defect_escape_delta": int(total(governed, "defect_escape_count") - total(baseline, "defect_escape_count")),
                },
            }
        )
    return {
        "measurement_scope": "matched_four_path_retrospective_local_replay",
        "operator_burden_measure": "operator_steps_proxy",
        "operator_active_time_observed": False,
        "host_timing_is_diagnostic": True,
        "comparisons": comparisons,
    }


def execute(workspace: Path) -> dict[str, Any]:
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    commit = design["task"]["pre_fix_commit"]
    pre_fix_match = all(old_bytes(commit, relative) for relative in SOURCE_FILES)
    current_fix = (
        GENERATOR_FIX in (ROOT / GENERATOR).read_text(encoding="utf-8")
        and FIX_LINE in (ROOT / CONFIG).read_text(encoding="utf-8")
    )
    if workspace.exists():
        shutil.rmtree(workspace)
    workspace.mkdir(parents=True)
    trials = [
        run_trial(workspace, design, route, path)
        for route in design["routes"]
        for path in design["paths"]
    ]
    return {
        "schema_version": "asi_stack.p5_u1_result.v1",
        "result_id": "p5-u1-human-reader-source-link-repair-local",
        "design_sha256": sha256(DESIGN.read_bytes()),
        "task": {
            "classification": design["task"]["classification"],
            "pre_fix_commit": commit,
            "pre_fix_files_match_git": pre_fix_match,
            "current_fix_present": current_fix,
            "outcome_known_before_route_replay": True,
        },
        "route_count": 3,
        "path_count": 4,
        "trial_count": len(trials),
        "trials": trials,
        "governance_rent": governance_rent(trials),
        "aggregate": {
            "trial_count": len(trials),
            "state_checks_passed": sum(row["state_check_passed"] for row in trials),
            "mutations_rejected": sum(row["mutation_rejected"] for row in trials),
            "governed_authority_blocks": sum(row["route"] == "full_governed" and row["path"] == "blocked_authority" and row["terminal_disposition"] == "blocked_before_effect" for row in trials),
            "governed_crash_recoveries": sum(row["route"] == "full_governed" and row["terminal_disposition"] == "recovered_and_completed" for row in trials),
            "governed_compensations": sum(row["route"] == "full_governed" and row["metrics"]["compensation_closed"] for row in trials),
            "direct_or_record_only_unauthorized_effects": sum(row["metrics"]["unauthorized_effect_count"] for row in trials),
            "support_state_effect": "none",
        },
        "support_state_effect": "none",
        "release_effect": "none",
        "maximum_inference": "This retrospective local replay demonstrates route-distinct authority, record, recovery, compensation, and cost behavior for one naturally arising repository defect; it is not a prospective utility estimate.",
        "non_claims": [
            "The task outcome was known before route replay.",
            "The local bare remote is a separate Git effect boundary, not a production hosting service.",
            "One repository repair does not estimate general usefulness or safety.",
            "Measured latency and CPU values are host-specific diagnostics.",
            "The route comparison is not randomized, blinded, independent, or held out.",
            "No chapter-core claim, support state, publication decision, SOTA, AGI, or ASI claim moves.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", type=Path, default=ROOT / "build/p5_u1/latest")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--write-tracked-result", action="store_true")
    args = parser.parse_args()
    output = TRACKED_RESULT if args.write_tracked_result else (args.output or args.workspace / "result.json")
    result = execute(args.workspace)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"P5-U1 completed {result['trial_count']} trials; result: {output}")


if __name__ == "__main__":
    main()
