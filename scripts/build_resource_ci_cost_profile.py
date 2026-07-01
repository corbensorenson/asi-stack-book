#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import statistics
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "experiments" / "resource_ci_cost_profile" / "results" / "2026-07-01-main.json"
PROFILE_ID = "resource-ci-cost-profile-2026-07-01-main"
WORKFLOW = "Publish Quarto site"
BRANCH = "main"
RUN_LIMIT = 8
BUILD_COMMAND = "python3 scripts/build_resource_ci_cost_profile.py --write-result"

NON_CLAIMS = [
    "This CI cost profile does not promote any chapter core claim above argument.",
    "This CI cost profile does not create a support-state transition.",
    "This CI cost profile does not prove deployed scheduler behavior, runtime budget enforcement, model quality, economic outcomes, physical feasibility, simulator adequacy, or workload-quality improvement.",
    "This CI cost profile records GitHub Actions publication-pipeline metadata only; it is not a production workload trace or external review.",
]


def run_command(args: list[str]) -> str:
    result = subprocess.run(args, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        sys.stderr.write(result.stdout)
        sys.stderr.write(result.stderr)
        raise SystemExit(result.returncode)
    return result.stdout


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def seconds_between(start: str, end: str) -> int:
    return int((parse_time(end) - parse_time(start)).total_seconds())


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def summarize_log(log_text: str) -> dict[str, Any]:
    lines = [line for line in log_text.splitlines() if line.strip()]
    interesting = [
        line
        for line in lines
        if any(
            fragment in line
            for fragment in (
                "git diff --exit-code",
                "appendices/E_codex_test_specs.qmd",
                "Resource workflow trace harness",
                "Process completed with exit code 1",
            )
        )
    ]
    return {
        "sha256": sha256_text(log_text),
        "excerpt": interesting[:8],
    }


def normalize_run(raw: dict[str, Any]) -> dict[str, Any]:
    created_at = str(raw["createdAt"])
    updated_at = str(raw["updatedAt"])
    status = str(raw["status"])
    conclusion = str(raw.get("conclusion") or "")
    duration_seconds = seconds_between(created_at, updated_at)
    return {
        "run_id": int(raw["databaseId"]),
        "title": str(raw["displayTitle"]),
        "head_sha": str(raw["headSha"]),
        "status": status,
        "conclusion": conclusion,
        "event": str(raw["event"]),
        "workflow": str(raw["workflowName"]),
        "created_at": created_at,
        "updated_at": updated_at,
        "duration_seconds": duration_seconds,
        "url": str(raw["url"]),
    }


def metric_summary(runs: list[dict[str, Any]]) -> dict[str, Any]:
    completed = [run for run in runs if run["status"] == "completed"]
    success = [run for run in completed if run["conclusion"] == "success"]
    failure = [run for run in completed if run["conclusion"] == "failure"]
    in_progress = [run for run in runs if run["status"] != "completed"]
    durations = [int(run["duration_seconds"]) for run in completed]
    success_durations = [int(run["duration_seconds"]) for run in success]
    return {
        "run_count": len(runs),
        "completed_run_count": len(completed),
        "success_count": len(success),
        "failure_count": len(failure),
        "in_progress_count": len(in_progress),
        "completed_duration_seconds_total": sum(durations),
        "completed_duration_seconds_median": int(statistics.median(durations)) if durations else 0,
        "completed_duration_seconds_mean": round(sum(durations) / len(durations), 3) if durations else 0,
        "success_duration_seconds_mean": round(sum(success_durations) / len(success_durations), 3)
        if success_durations
        else 0,
    }


def build_record() -> dict[str, Any]:
    list_command = [
        "gh",
        "run",
        "list",
        "--workflow",
        WORKFLOW,
        "--branch",
        BRANCH,
        "--limit",
        str(RUN_LIMIT),
        "--json",
        "databaseId,displayTitle,headSha,status,conclusion,createdAt,updatedAt,event,workflowName,url",
    ]
    raw_runs = json.loads(run_command(list_command))
    runs = [normalize_run(raw) for raw in raw_runs]
    failure_events = []
    for run in runs:
        if run["status"] == "completed" and run["conclusion"] == "failure":
            log_command = ["gh", "run", "view", str(run["run_id"]), "--log-failed"]
            log_text = run_command(log_command)
            failure_events.append(
                {
                    "run_id": run["run_id"],
                    "title": run["title"],
                    "failure_stage": "Check generated scaffold",
                    "failure_type": "generated_scaffold_drift",
                    "log_command": " ".join(log_command),
                    "log_summary": summarize_log(log_text),
                }
            )

    repair_events = []
    for failure in failure_events:
        later_success = next(
            (
                run
                for run in runs
                if run["status"] == "completed"
                and run["conclusion"] == "success"
                and parse_time(run["created_at"]) > parse_time(
                    next(item["created_at"] for item in runs if item["run_id"] == failure["run_id"])
                )
            ),
            None,
        )
        if later_success is not None:
            repair_events.append(
                {
                    "failed_run_id": failure["run_id"],
                    "repair_run_id": later_success["run_id"],
                    "repair_title": later_success["title"],
                    "repair_conclusion": later_success["conclusion"],
                    "repair_duration_seconds": later_success["duration_seconds"],
                    "repair_boundary": "The next completed successful Pages run demonstrates that the publication gate recovered; it does not prove the underlying chapter claim.",
                }
            )

    return {
        "profile_id": PROFILE_ID,
        "record_kind": "resource_ci_cost_profile",
        "recorded_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "command": BUILD_COMMAND,
        "workflow": WORKFLOW,
        "branch": BRANCH,
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
        "source_commands": [
            " ".join(list_command),
            "gh run view <failed-run-id> --log-failed",
        ],
        "metrics": metric_summary(runs),
        "runs": runs,
        "failure_events": failure_events,
        "repair_events": repair_events,
        "non_claims": NON_CLAIMS,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the Resource Economics CI cost profile.")
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


if __name__ == "__main__":
    main()
