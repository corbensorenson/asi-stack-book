#!/usr/bin/env python3
"""Execute the admitted C1-EL Quarto render comparison."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import resource
import shutil
import subprocess
import tempfile
import time


ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "experiments/c1_exit_ladder/design.json"
ADMISSION = ROOT / "experiments/c1_exit_ladder/admission.json"
DEFAULT_OUTPUT = ROOT / "experiments/c1_exit_ladder/results/2026-08-13-local.json"
ROUTES = ("direct", "record_only", "full_governed")
PATHS = (
    "natural_happy",
    "injected_blocked_authority",
    "injected_partial_effect_crash",
    "injected_external_effect",
)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run(
    argv: list[str],
    *,
    cwd: Path,
    env: dict[str, str] | None = None,
    timeout: int = 1800,
) -> dict:
    before = resource.getrusage(resource.RUSAGE_CHILDREN)
    started = datetime.now(timezone.utc)
    wall_start = time.monotonic()
    timed_out = False
    try:
        completed = subprocess.run(
            argv,
            cwd=cwd,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            check=False,
        )
        exit_code = completed.returncode
        stdout = completed.stdout
        stderr = completed.stderr
    except subprocess.TimeoutExpired as exc:
        timed_out = True
        exit_code = 124
        stdout = exc.stdout or ""
        stderr = exc.stderr or ""
        if isinstance(stdout, bytes):
            stdout = stdout.decode("utf-8", errors="replace")
        if isinstance(stderr, bytes):
            stderr = stderr.decode("utf-8", errors="replace")
    ended = datetime.now(timezone.utc)
    after = resource.getrusage(resource.RUSAGE_CHILDREN)
    return {
        "argv": argv,
        "started_at_utc": started.isoformat(),
        "ended_at_utc": ended.isoformat(),
        "wall_ms": round((time.monotonic() - wall_start) * 1000, 3),
        "cpu_ms": round(
            (
                (after.ru_utime - before.ru_utime)
                + (after.ru_stime - before.ru_stime)
            )
            * 1000,
            3,
        ),
        "timeout_seconds": timeout,
        "timed_out": timed_out,
        "exit_code": exit_code,
        "stdout_sha256": hashlib.sha256(stdout.encode()).hexdigest(),
        "stderr_sha256": hashlib.sha256(stderr.encode()).hexdigest(),
        "stdout_tail": stdout[-1600:],
        "stderr_tail": stderr[-1600:],
    }


def git(cwd: Path, *args: str, timeout: int = 180) -> dict:
    receipt = run(["git", *args], cwd=cwd, timeout=timeout)
    if receipt["exit_code"] != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {receipt['stderr_tail']}")
    return receipt


def write_artifact(directory: Path, name: str, value: dict) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    (directory / name).write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def artifact_inventory(directory: Path) -> tuple[int, int]:
    paths = [path for path in directory.rglob("*") if path.is_file()]
    return len(paths), sum(path.stat().st_size for path in paths)


def render_observation(clone: Path) -> dict:
    site = clone / "_site"
    html = sorted(site.rglob("*.html")) if site.is_dir() else []
    landing = site / "index.html"
    return {
        "rendered_html_count": len(html),
        "landing_page_present": landing.is_file(),
        "landing_page_sha256": sha256(landing) if landing.is_file() else None,
    }


def render_env(home: Path) -> dict[str, str]:
    env = os.environ.copy()
    env.update({"HOME": str(home), "LANG": "en_US.UTF-8", "LC_ALL": "en_US.UTF-8"})
    return env


def prepare_clone(temp: Path, source_commit: str) -> Path:
    clone = temp / "source"
    receipt = run(
        ["git", "clone", "--shared", "--no-checkout", str(ROOT), str(clone)],
        cwd=temp,
        timeout=300,
    )
    if receipt["exit_code"] != 0:
        raise RuntimeError(f"clone failed: {receipt['stderr_tail']}")
    git(clone, "checkout", "--detach", source_commit)
    observed = git(clone, "rev-parse", "HEAD")["stdout_tail"].strip()
    if observed != source_commit:
        raise RuntimeError(f"source identity mismatch: {observed}")
    return clone


def create_external_effect(temp: Path, digest: str) -> tuple[Path, str]:
    remote = temp / "effect.git"
    source = temp / "effect-source"
    git(temp, "init", "--bare", str(remote))
    git(temp, "init", str(source))
    git(source, "config", "user.name", "ASI Stack C1-EL")
    git(source, "config", "user.email", "c1-el@invalid.local")
    (source / "render.sha256").write_text(digest + "\n", encoding="utf-8")
    git(source, "add", "render.sha256")
    git(source, "commit", "-m", "Record C1 render effect")
    commit = git(source, "rev-parse", "HEAD")["stdout_tail"].strip()
    git(source, "remote", "add", "effect", str(remote))
    git(source, "push", "effect", "HEAD:refs/heads/render-effect")
    return remote, commit


def remote_state(remote: Path, commit: str) -> dict:
    branch = run(
        ["git", "--git-dir", str(remote), "show-ref", "--verify", "--quiet", "refs/heads/render-effect"],
        cwd=remote.parent,
        timeout=30,
    )
    history = run(
        ["git", "--git-dir", str(remote), "cat-file", "-e", f"{commit}^{{commit}}"],
        cwd=remote.parent,
        timeout=30,
    )
    return {
        "visible_branch_present": branch["exit_code"] == 0,
        "effect_commit_object_present": history["exit_code"] == 0,
    }


def execute_trial(route: str, path_id: str, design: dict) -> dict:
    source_commit = design["source_commit"]
    timeout = design["matched_inputs"]["wall_time_ceiling_seconds_per_trial"]
    with tempfile.TemporaryDirectory(prefix=f"asi-stack-c1-{route}-{path_id}-", dir="/private/tmp") as raw:
        temp = Path(raw)
        clone = prepare_clone(temp, source_commit)
        home = temp / "home"
        home.mkdir()
        artifacts = temp / "route-artifacts"
        env = render_env(home)
        render_receipts: list[dict] = []
        forbidden = temp / "outside-admitted-scope.txt"
        external_state = None
        partial_site_present_after_crash = False
        recovery_performed = False
        authority_blocked = False

        if route in {"record_only", "full_governed"}:
            write_artifact(artifacts, "intent.json", {"route": route, "path": path_id, "source_commit": source_commit})

        if path_id == "natural_happy":
            render_receipts.append(run(["quarto", "render", "--to", "html"], cwd=clone, env=env, timeout=timeout))

        elif path_id == "injected_blocked_authority":
            if route == "full_governed":
                authority_blocked = True
                write_artifact(artifacts, "authority.json", {"decision": "reject_before_effect", "path": str(forbidden)})
            else:
                forbidden.write_text("unauthorized effect\n", encoding="utf-8")
                render_receipts.append(run(["quarto", "render", "--to", "html"], cwd=clone, env=env, timeout=timeout))

        elif path_id == "injected_partial_effect_crash":
            partial = run(["quarto", "render", "index.qmd", "--to", "html"], cwd=clone, env=env, timeout=timeout)
            render_receipts.append(partial)
            partial_site_present_after_crash = (clone / "_site/index.html").is_file()
            if route == "full_governed":
                shutil.rmtree(clone / "_site", ignore_errors=True)
                recovery_performed = True
                render_receipts.append(run(["quarto", "render", "--to", "html"], cwd=clone, env=env, timeout=timeout))
                write_artifact(artifacts, "recovery.json", {"partial_observed": partial_site_present_after_crash, "complete_rerender": True})

        elif path_id == "injected_external_effect":
            complete = run(["quarto", "render", "--to", "html"], cwd=clone, env=env, timeout=timeout)
            render_receipts.append(complete)
            observation = render_observation(clone)
            digest = observation["landing_page_sha256"] or "0" * 64
            remote, commit = create_external_effect(temp, digest)
            if route == "full_governed":
                run(
                    ["git", "--git-dir", str(remote), "update-ref", "-d", "refs/heads/render-effect"],
                    cwd=temp,
                    timeout=30,
                )
                write_artifact(artifacts, "compensation.json", {"deleted_visible_branch": True, "effect_commit": commit})
            external_state = remote_state(remote, commit)
        else:
            raise ValueError(path_id)

        observation = render_observation(clone)
        complete_render_passed = bool(render_receipts) and render_receipts[-1]["exit_code"] == 0 and observation["rendered_html_count"] >= design["repair"]["required_document_count"]
        forbidden_present = forbidden.is_file()
        partial_residual = path_id == "injected_partial_effect_crash" and route != "full_governed" and partial_site_present_after_crash
        external_residual = bool(external_state and external_state["visible_branch_present"])
        residual_count = int(partial_residual) + int(external_residual)
        compensation_closed = None
        if path_id == "injected_external_effect":
            compensation_closed = bool(
                external_state
                and not external_state["visible_branch_present"]
                and external_state["effect_commit_object_present"]
            )
        unauthorized_effect_count = int(forbidden_present)
        defect_escape_count = int(partial_residual)
        useful_success = complete_render_passed
        if path_id == "injected_blocked_authority" and route == "full_governed":
            useful_success = False
        state_check_passed = {
            "natural_happy": complete_render_passed,
            "injected_blocked_authority": (
                authority_blocked and not forbidden_present and not render_receipts
                if route == "full_governed"
                else forbidden_present and complete_render_passed
            ),
            "injected_partial_effect_crash": (
                partial_site_present_after_crash and recovery_performed and complete_render_passed and residual_count == 0
                if route == "full_governed"
                else partial_site_present_after_crash and residual_count == 1 and not complete_render_passed
            ),
            "injected_external_effect": (
                bool(compensation_closed) and residual_count == 0
                if route == "full_governed"
                else external_residual and residual_count == 1 and compensation_closed is False
            ),
        }[path_id]

        if route in {"record_only", "full_governed"}:
            write_artifact(
                artifacts,
                "outcome.json",
                {
                    "state_check_passed": state_check_passed,
                    "unauthorized_effect_count": unauthorized_effect_count,
                    "residual_count": residual_count,
                },
            )
        artifact_file_count, artifact_bytes = artifact_inventory(artifacts)
        wall_ms = round(sum(row["wall_ms"] for row in render_receipts), 3)
        cpu_ms = round(sum(row["cpu_ms"] for row in render_receipts), 3)
        operator_steps = 1 + (2 if route == "record_only" else 5 if route == "full_governed" else 0)
        operator_steps += int(recovery_performed) + int(path_id == "injected_external_effect" and route == "full_governed")
        return {
            "trial_id": f"{route}:{path_id}",
            "route": route,
            "path": path_id,
            "source_commit": source_commit,
            "matched_home_contract": "empty_route_owned_writable_directory",
            "render_receipts": render_receipts,
            "observation": observation,
            "authority_blocked": authority_blocked,
            "forbidden_effect_present": forbidden_present,
            "partial_site_present_after_crash": partial_site_present_after_crash,
            "recovery_performed": recovery_performed,
            "external_state": external_state,
            "state_check_passed": state_check_passed,
            "outcomes": {
                "useful_success": useful_success,
                "unauthorized_effect_count": unauthorized_effect_count,
                "false_block_count": 0,
                "defect_escape_count": defect_escape_count,
                "latency_ms": wall_ms,
                "cpu_ms": cpu_ms,
                "operator_step_proxy": operator_steps,
                "artifact_file_count": artifact_file_count,
                "artifact_bytes": artifact_bytes,
                "recovery_ms": wall_ms if recovery_performed else 0.0,
                "compensation_closed": compensation_closed,
                "residual_count": residual_count,
            },
        }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    design = load(DESIGN)
    admission = load(ADMISSION)
    started = datetime.now(timezone.utc)
    trials = [execute_trial(route, path_id, design) for path_id in PATHS for route in ROUTES]
    all_checks = all(row["state_check_passed"] for row in trials)
    natural = [row for row in trials if row["path"] == "natural_happy"]
    full = {row["path"]: row for row in trials if row["route"] == "full_governed"}
    distinctive = (
        all(row["outcomes"]["useful_success"] for row in natural)
        and full["injected_blocked_authority"]["authority_blocked"]
        and full["injected_partial_effect_crash"]["recovery_performed"]
        and full["injected_external_effect"]["outcomes"]["compensation_closed"] is True
    )
    disposition = "bounded_positive_no_support_transition" if all_checks and distinctive else "negative"
    result = {
        "schema_version": "asi_stack.c1_exit_ladder_result.v1",
        "result_id": "c1-el-quarto-render-db-open-001-local",
        "protocol_id": design["protocol_id"],
        "admission_id": admission["admission_id"],
        "source_commit": design["source_commit"],
        "executed_at_utc": started.isoformat(),
        "completed_at_utc": datetime.now(timezone.utc).isoformat(),
        "quarto_version": run(["quarto", "--version"], cwd=ROOT, timeout=30)["stdout_tail"].strip(),
        "route_count": 3,
        "path_count": 4,
        "trial_count": len(trials),
        "trials": trials,
        "all_state_checks_passed": all_checks,
        "distinctive_mechanisms_observed": distinctive,
        "disposition": disposition,
        "maximum_inference": design["disposition_rules"]["support_ceiling"],
        "independent_external_observer": False,
        "protected_content_opened": false,
        "support_state_effect": "none",
        "release_effect": "none",
    }
    output = args.output if args.output.is_absolute() else ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"C1-EL executed {len(trials)} trials; disposition={disposition}; result={output}")


if __name__ == "__main__":
    main()
