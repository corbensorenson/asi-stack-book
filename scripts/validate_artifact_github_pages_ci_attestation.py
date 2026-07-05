#!/usr/bin/env python3
"""Validate a bounded GitHub Pages CI attestation record.

The default mode validates a tracked result captured from GitHub Actions. The
write mode is local-only and uses `gh run view` for a named run id. This keeps
CI validation offline while letting the book record an externally hosted
workflow result as bounded record-reality evidence.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "experiments" / "artifact_github_pages_ci_attestation" / "results" / "2026-07-05-local.json"
DOC = ROOT / "docs" / "artifact_github_pages_ci_attestation.md"
TRANSITION = ROOT / "evidence_transitions" / "v1_x_measured" / "artifact_github_pages_ci_attestation_no_change.json"
CHAPTER = ROOT / "chapters" / "artifact-graphs-audit-logs-and-replay.qmd"
READER = ROOT / "editions" / "reader_manuscript" / "v1_0" / "chapters" / "artifact-graphs-audit-logs-and-replay.qmd"
OUTLINE = ROOT / "docs" / "book_outline.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
CHANGELOG = ROOT / "appendices" / "F_changelog.qmd"
LEDGER_MD = ROOT / "docs" / "contribution_novelty_ledger.md"
LEDGER_JSON = ROOT / "docs" / "contribution_novelty_ledger.json"

COMMAND = "python3 scripts/validate_artifact_github_pages_ci_attestation.py"
RESULT_ID = "artifact-github-pages-ci-attestation-2026-07-05"
CLAIM_ID = "artifact-graphs.github_pages_ci_attestation"
WORKFLOW_NAME = "Publish Quarto site"
HEAD_BRANCH = "main"
REQUIRED_BUILD_STEPS = [
    "Check generated scaffold",
    "Validate book source",
    "Build Lean proofs",
    "Render HTML",
    "Validate live Human view",
    "Browser-smoke live Human view",
    "Upload Pages artifact",
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Artifact GitHub Pages CI attestation validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def run_capture(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def gh_run(run_id: str) -> dict[str, Any]:
    fields = "status,conclusion,headSha,headBranch,name,workflowName,url,event,createdAt,updatedAt,displayTitle,databaseId,jobs"
    proc = run_capture(["gh", "run", "view", run_id, "--json", fields])
    if proc.returncode != 0:
        fail([f"gh run view {run_id} failed: {proc.stderr or proc.stdout}"])
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        fail([f"gh run view {run_id} did not return JSON: {exc}"])
    if not isinstance(data, dict):
        fail([f"gh run view {run_id} returned a non-object JSON value."])
    return data


def normalize_job(job: dict[str, Any]) -> dict[str, Any]:
    steps = []
    for step in job.get("steps", []):
        if not isinstance(step, dict):
            continue
        steps.append(
            {
                "name": step.get("name", ""),
                "status": step.get("status", ""),
                "conclusion": step.get("conclusion", ""),
                "started_at": step.get("startedAt", ""),
                "completed_at": step.get("completedAt", ""),
            }
        )
    return {
        "name": job.get("name", ""),
        "database_id": job.get("databaseId"),
        "status": job.get("status", ""),
        "conclusion": job.get("conclusion", ""),
        "url": job.get("url", ""),
        "started_at": job.get("startedAt", ""),
        "completed_at": job.get("completedAt", ""),
        "steps": steps,
    }


def build_result(run: dict[str, Any]) -> dict[str, Any]:
    jobs = [normalize_job(job) for job in run.get("jobs", []) if isinstance(job, dict)]
    build_job = next((job for job in jobs if job.get("name") == "build"), {})
    deploy_job = next((job for job in jobs if job.get("name") == "deploy"), {})
    required_step_results = []
    steps_by_name = {
        str(step.get("name")): step
        for step in build_job.get("steps", [])
        if isinstance(step, dict)
    }
    for step_name in REQUIRED_BUILD_STEPS:
        step = steps_by_name.get(step_name, {})
        required_step_results.append(
            {
                "name": step_name,
                "status": step.get("status", "missing"),
                "conclusion": step.get("conclusion", "missing"),
            }
        )
    return {
        "schema_version": "0.1",
        "result_id": RESULT_ID,
        "claim_id": CLAIM_ID,
        "run_id": int(run.get("databaseId", 0)),
        "run_url": run.get("url", ""),
        "workflow_name": run.get("workflowName", ""),
        "run_name": run.get("name", ""),
        "display_title": run.get("displayTitle", ""),
        "event": run.get("event", ""),
        "head_branch": run.get("headBranch", ""),
        "head_sha": run.get("headSha", ""),
        "status": run.get("status", ""),
        "conclusion": run.get("conclusion", ""),
        "created_at": run.get("createdAt", ""),
        "updated_at": run.get("updatedAt", ""),
        "jobs": jobs,
        "required_build_steps": required_step_results,
        "observation_routes": [
            {
                "route_id": "github_actions_run_api",
                "observer_role": "github_actions_service",
                "accepted": run.get("status") == "completed" and run.get("conclusion") == "success",
            },
            {
                "route_id": "workflow_job_set",
                "observer_role": "github_actions_jobs_api",
                "accepted": bool(build_job) and bool(deploy_job),
            },
            {
                "route_id": "required_step_set",
                "observer_role": "publish_workflow_step_status",
                "accepted": all(
                    row.get("status") == "completed" and row.get("conclusion") == "success"
                    for row in required_step_results
                ),
            },
        ],
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
        "attestation_limits": [
            "GitHub Actions run success attests this workflow execution only.",
            "GitHub Actions is an external CI service, not an independent human reviewer.",
            "A successful Pages workflow does not prove source interpretation, verifier correctness, deployment safety, model quality, or ASI capability.",
            "The run attests the recorded commit, not future commits.",
        ],
        "non_claims": [
            "does not create an upward support-state transition",
            "does not promote any chapter core claim",
            "does not promote the Artifact Graphs chapter core claim",
            "does not prove open-world receipt faithfulness",
            "does not prove deployed attestation behavior",
            "does not create independent external human review",
            "does not approve any reader release artifact",
        ],
    }


def validate_result(result: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    expected = {
        "schema_version": "0.1",
        "result_id": RESULT_ID,
        "claim_id": CLAIM_ID,
        "workflow_name": WORKFLOW_NAME,
        "event": "push",
        "head_branch": HEAD_BRANCH,
        "status": "completed",
        "conclusion": "success",
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
    }
    for key, value in expected.items():
        if result.get(key) != value:
            errors.append(f"{rel(RESULT)} {key} must be {value!r}; found {result.get(key)!r}.")
    if not isinstance(result.get("run_id"), int) or result.get("run_id", 0) <= 0:
        errors.append(f"{rel(RESULT)} run_id must be a positive integer.")
    if not str(result.get("run_url", "")).startswith("https://github.com/corbensorenson/asi-stack-book/actions/runs/"):
        errors.append(f"{rel(RESULT)} run_url must point to the repository Actions run.")
    if not re.fullmatch(r"[0-9a-f]{40}", str(result.get("head_sha", ""))):
        errors.append(f"{rel(RESULT)} head_sha must be a 40-character git SHA.")
    jobs = result.get("jobs")
    if not isinstance(jobs, list):
        errors.append(f"{rel(RESULT)} jobs must be a list.")
        jobs = []
    jobs_by_name = {str(job.get("name")): job for job in jobs if isinstance(job, dict)}
    for job_name in ("build", "deploy"):
        job = jobs_by_name.get(job_name)
        if not isinstance(job, dict):
            errors.append(f"{rel(RESULT)} missing {job_name!r} job.")
            continue
        if job.get("status") != "completed" or job.get("conclusion") != "success":
            errors.append(f"{rel(RESULT)} job {job_name!r} must be completed/success.")
    step_rows = result.get("required_build_steps")
    if not isinstance(step_rows, list) or len(step_rows) != len(REQUIRED_BUILD_STEPS):
        errors.append(f"{rel(RESULT)} required_build_steps must list {len(REQUIRED_BUILD_STEPS)} steps.")
        step_rows = []
    step_by_name = {str(row.get("name")): row for row in step_rows if isinstance(row, dict)}
    for step_name in REQUIRED_BUILD_STEPS:
        row = step_by_name.get(step_name)
        if not row:
            errors.append(f"{rel(RESULT)} missing required build step {step_name!r}.")
            continue
        if row.get("status") != "completed" or row.get("conclusion") != "success":
            errors.append(f"{rel(RESULT)} step {step_name!r} must be completed/success.")
    routes = result.get("observation_routes")
    if not isinstance(routes, list) or len(routes) < 3:
        errors.append(f"{rel(RESULT)} observation_routes must contain at least three routes.")
        routes = []
    if any(not isinstance(route, dict) or route.get("accepted") is not True for route in routes):
        errors.append(f"{rel(RESULT)} every observation route must be accepted.")
    limits = " ".join(str(item).lower() for item in result.get("attestation_limits", []))
    for phrase in ("external ci service", "not an independent human reviewer", "not future commits"):
        if phrase not in limits:
            errors.append(f"{rel(RESULT)} attestation_limits missing phrase: {phrase}")
    non_claims = " ".join(str(item).lower() for item in result.get("non_claims", []))
    for phrase in (
        "does not create an upward support-state transition",
        "does not promote any chapter core claim",
        "does not prove open-world receipt faithfulness",
        "does not create independent external human review",
        "does not approve any reader release artifact",
    ):
        if phrase not in non_claims:
            errors.append(f"{rel(RESULT)} non_claims missing phrase: {phrase}")
    return errors


def validate_surfaces(result: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    expected_refs = [
        (DOC, RESULT_ID),
        (DOC, rel(RESULT)),
        (DOC, rel(TRANSITION)),
        (DOC, "not independent external human review"),
        (CHAPTER, "GitHub Pages CI attestation"),
        (CHAPTER, rel(RESULT)),
        (READER, "GitHub Pages CI attestation"),
        (READER, rel(RESULT)),
        (OUTLINE, "GitHub Pages CI attestation"),
        (ROADMAP, "GitHub Pages CI attestation"),
        (CHANGELOG, "GitHub Pages CI attestation"),
        (LEDGER_MD, "github_pages_ci_attestation_backed_not_external_review"),
        (LEDGER_JSON, "github_pages_ci_attestation_backed_not_external_review"),
        (TRANSITION, RESULT_ID),
    ]
    for path, fragment in expected_refs:
        if not path.exists():
            errors.append(f"missing required surface {rel(path)}.")
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if fragment not in text:
            errors.append(f"{rel(path)} missing required fragment: {fragment}")
    if str(result.get("run_id")) and str(result.get("run_id")) not in DOC.read_text(encoding="utf-8", errors="ignore"):
        errors.append(f"{rel(DOC)} must name captured run id {result.get('run_id')}.")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-result", action="store_true", help="Capture a GitHub Actions run into the tracked result.")
    parser.add_argument("--run-id", help="GitHub Actions run id to capture when --write-result is set.")
    args = parser.parse_args()

    if args.write_result:
        if not args.run_id:
            fail(["--write-result requires --run-id."])
        result = build_result(gh_run(args.run_id))
        errors = validate_result(result)
        if errors:
            fail(errors)
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    else:
        if not RESULT.exists():
            fail([f"{rel(RESULT)} is missing; run {COMMAND} --write-result --run-id <run-id>."])
        result = load_json(RESULT)
        if not isinstance(result, dict):
            fail([f"{rel(RESULT)} must contain a JSON object."])

    errors = validate_result(result)
    errors.extend(validate_surfaces(result))
    if errors:
        fail(errors)
    print(
        "Artifact GitHub Pages CI attestation validation passed: "
        f"run {result['run_id']} at {result['head_sha'][:12]}."
    )


if __name__ == "__main__":
    main()
