#!/usr/bin/env python3
"""Validate the outcome-aware P5 natural publication-service development trace."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
import json
from pathlib import Path
import sys

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
TRACE = (
    ROOT
    / "experiments/p5_natural_publication_service_trace/results/2026-07-27-development.json"
)
SCHEMA = ROOT / "schemas/p5_natural_publication_service_trace.schema.json"
REPORT = ROOT / "docs/p5_natural_publication_service_development_trace.md"
ROADMAP = ROOT / "docs/post_v2_3_maintenance_transfer_and_publication_roadmap.md"
CHAPTER = ROOT / "chapters/governed-operations-incident-command-and-graceful-degradation.qmd"
OUTLINE = ROOT / "docs/book_outline.md"
STATUS = ROOT / "roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json"
CHANGELOG = ROOT / "appendices/F_changelog.qmd"

SOURCE_SHA = "5575d3cbf5f9dd9edfec8548c4279728b0da3995"
BUILD_RUN = 30287899588
DEPLOY_RUN = 30288922224
ARTIFACT_ID = 8661958792
ARTIFACT_DIGEST = (
    "sha256:84700830e2f110e1b4406dc1dbc3976b0b2cecc9020455040706d128c3741dc2"
)
REQUIRED_STEPS = {
    "Run deep validation tier",
    "Build Lean proofs",
    "Render clean HTML",
    "Build and validate canonical public status",
    "Validate live Human view",
    "Browser-smoke live Human view",
    "Build and verify tested artifact",
    "Upload commit-bound tested artifact",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def seconds(start: str, end: str) -> int:
    return int(
        (
            datetime.fromisoformat(end.replace("Z", "+00:00"))
            - datetime.fromisoformat(start.replace("Z", "+00:00"))
        ).total_seconds()
    )


def validate_trace(trace: dict) -> list[str]:
    failures: list[str] = []
    failures.extend(
        f"schema: {error.message}"
        for error in sorted(
            Draft202012Validator(
                load(SCHEMA), format_checker=FormatChecker()
            ).iter_errors(trace),
            key=lambda error: list(error.path),
        )
    )

    classification = trace.get("classification", {})
    if classification != {
        "natural_operational_work": True,
        "work_authored_to_test_p5": False,
        "outcome_known_before_trace_freeze": True,
        "prospective": False,
        "claim_bearing": False,
        "eligible_for_held_out_denominator": False,
        "eligible_for_support_transition": False,
        "eligible_for_release_decision": False,
    }:
        failures.append("development-only retrospective classification drifted")

    service = trace.get("service", {})
    build = trace.get("build_receipt", {})
    deploy = trace.get("deploy_receipt", {})
    if service.get("source_commit") != SOURCE_SHA:
        failures.append("source commit drifted")
    if build.get("run_id") != BUILD_RUN or deploy.get("run_id") != DEPLOY_RUN:
        failures.append("GitHub Actions run identity drifted")
    if build.get("head_sha") != SOURCE_SHA or deploy.get("head_sha") != SOURCE_SHA:
        failures.append("source/build/deploy SHA join is broken")
    if build.get("conclusion") != "success" or deploy.get("conclusion") != "success":
        failures.append("a workflow receipt is not successful")
    step_names = {
        row.get("name")
        for row in build.get("required_steps", [])
        if isinstance(row, dict)
    }
    if step_names != REQUIRED_STEPS:
        failures.append("required build-step denominator drifted")
    if any(
        row.get("conclusion") != "success"
        for row in build.get("required_steps", [])
        if isinstance(row, dict)
    ):
        failures.append("a required build step is not successful")

    artifact = build.get("artifact", {})
    deploy_job = deploy.get("deploy_job", {})
    if artifact.get("artifact_id") != ARTIFACT_ID:
        failures.append("artifact identity drifted")
    if artifact.get("digest") != ARTIFACT_DIGEST:
        failures.append("artifact digest drifted")
    if SOURCE_SHA not in str(artifact.get("name", "")):
        failures.append("artifact name is not commit-bound")
    if deploy_job.get("downloaded_artifact_from_build_run") != BUILD_RUN:
        failures.append("deploy job no longer consumes the tested build run")
    if deploy_job.get("verified_expected_commit") != SOURCE_SHA:
        failures.append("deploy job expected-commit join drifted")
    if deploy_job.get("rebuilt_site") is not False:
        failures.append("deploy path laundered a rebuild into the tested artifact")

    monitor = deploy.get("post_deploy_monitor", {})
    if monitor.get("conclusion") != "success":
        failures.append("post-deploy monitor is not successful")
    if monitor.get("institutionally_independent") is not False:
        failures.append("separate process was laundered into institutional independence")

    outcome = trace.get("observed_outcome", {})
    expected_durations = {
        "commit_to_deployment_status_seconds": seconds(
            service.get("source_commit_time", ""),
            deploy.get("deployment", {}).get("status_recorded_at", ""),
        ),
        "commit_to_post_deploy_monitor_completion_seconds": seconds(
            service.get("source_commit_time", ""), monitor.get("completed_at", "")
        ),
        "build_job_seconds": seconds(
            build.get("job", {}).get("started_at", ""),
            build.get("job", {}).get("completed_at", ""),
        ),
        "deep_validation_seconds": 424,
        "lean_build_seconds": 71,
        "html_render_seconds": 239,
        "deploy_job_seconds": seconds(
            deploy_job.get("started_at", ""), deploy_job.get("completed_at", "")
        ),
        "post_deploy_monitor_job_seconds": seconds(
            monitor.get("started_at", ""), monitor.get("completed_at", "")
        ),
        "post_deploy_crawl_seconds": seconds(
            monitor.get("crawl_step_started_at", ""),
            monitor.get("crawl_step_completed_at", ""),
        ),
    }
    for key, expected in expected_durations.items():
        if outcome.get(key) != expected:
            failures.append(f"{key} must equal receipt-derived {expected}")

    coverage = trace.get("measurement_coverage", {})
    false_fields = [
        "unsafe_release_rate_measured",
        "false_blocking_rate_measured",
        "user_task_quality_measured",
        "rollback_or_compensation_exercised",
        "incident_or_fault_exercised",
        "replica_or_partition_recovery_exercised",
        "operator_time_measured",
        "hosted_compute_measured",
        "delayed_harm_window_observed",
        "independent_external_reproduction",
    ]
    if any(coverage.get(field) is not False for field in false_fields):
        failures.append("an unmeasured outcome was laundered into measured coverage")
    if trace.get("support_state_effect") != "none":
        failures.append("trace promoted chapter support")
    if trace.get("record_policy_effect") != "none":
        failures.append("trace granted a new release decision")

    non_claims = " ".join(str(row).lower() for row in trace.get("non_claims", []))
    for phrase in (
        "does not establish governed operations efficacy",
        "does not establish effect-complete rollback",
        "does not estimate unsafe release or false blocking",
        "does not supply a held-out natural-task denominator",
        "does not supply a matched baseline or causal comparison",
        "does not count as independent external reproduction",
        "does not create a support-state transition",
        "does not grant a new release decision",
    ):
        if phrase not in non_claims:
            failures.append(f"non-claim boundary missing: {phrase}")
    return failures


def validate_surfaces() -> list[str]:
    failures: list[str] = []
    expected = {
        REPORT: [
            "retrospective natural happy-path development observation",
            str(BUILD_RUN),
            str(DEPLOY_RUN),
            "not a member of its held-out denominator",
        ],
        ROADMAP: [
            "P5 natural publication-service development checkpoint",
            str(BUILD_RUN),
            "outcome-aware",
        ],
        CHAPTER: [
            "Natural publication-service development observation",
            str(BUILD_RUN),
            "outcome-aware",
        ],
        OUTLINE: ["natural publication-service development trace", str(BUILD_RUN)],
        CHANGELOG: ["P5 natural publication-service development trace", str(BUILD_RUN)],
    }
    for path, phrases in expected.items():
        if not path.exists():
            failures.append(f"missing required surface: {path.relative_to(ROOT)}")
            continue
        text = " ".join(
            path.read_text(encoding="utf-8", errors="ignore").split()
        )
        for phrase in phrases:
            if phrase not in text:
                failures.append(
                    f"{path.relative_to(ROOT)} missing required phrase: {phrase}"
                )
    status = load(STATUS)
    status_trace = (
        status.get("p5_effect_complete_reference", {})
        .get("natural_publication_service_development_trace", {})
    )
    if status_trace.get("trace_path") != str(TRACE.relative_to(ROOT)):
        failures.append("roadmap status does not own the natural trace path")
    if status_trace.get("source_commit") != SOURCE_SHA:
        failures.append("roadmap status natural-trace source commit drifted")
    return failures


def mutation_controls(trace: dict) -> list[str]:
    controls = [
        ("source SHA mismatch", ("service", "source_commit"), "0" * 40),
        ("build SHA mismatch", ("build_receipt", "head_sha"), "1" * 40),
        ("deploy SHA mismatch", ("deploy_receipt", "head_sha"), "2" * 40),
        ("failed build", ("build_receipt", "conclusion"), "failure"),
        (
            "wrong artifact digest",
            ("build_receipt", "artifact", "digest"),
            "sha256:" + "3" * 64,
        ),
        ("deploy rebuild", ("deploy_receipt", "deploy_job", "rebuilt_site"), True),
        (
            "missing monitor",
            ("deploy_receipt", "post_deploy_monitor", "conclusion"),
            "failure",
        ),
        (
            "prospective laundering",
            ("classification", "prospective"),
            True,
        ),
        (
            "held-out laundering",
            ("classification", "eligible_for_held_out_denominator"),
            True,
        ),
        (
            "unsafe-release invention",
            ("measurement_coverage", "unsafe_release_rate_measured"),
            True,
        ),
        (
            "institutional-independence laundering",
            (
                "deploy_receipt",
                "post_deploy_monitor",
                "institutionally_independent",
            ),
            True,
        ),
        ("support promotion", ("support_state_effect",), "prototype"),
        ("release-decision promotion", ("record_policy_effect",), "release"),
    ]
    failures: list[str] = []
    for name, path, value in controls:
        mutated = deepcopy(trace)
        cursor = mutated
        for key in path[:-1]:
            cursor = cursor[key]
        cursor[path[-1]] = value
        if not validate_trace(mutated):
            failures.append(f"negative control was accepted: {name}")
    return failures


def main() -> None:
    trace = load(TRACE)
    failures = validate_trace(trace)
    failures.extend(validate_surfaces())
    failures.extend(mutation_controls(trace))
    if failures:
        raise SystemExit(
            "P5 natural publication-service trace validation failed:\n - "
            + "\n - ".join(failures)
        )
    print(
        "P5 natural publication-service trace passed: exact source/build/artifact/"
        "deploy/monitor joins, 13/13 rejecting mutations, and development-only "
        "outcome-aware boundaries."
    )


if __name__ == "__main__":
    main()
