#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter
from datetime import datetime
from pathlib import Path
import re
import statistics
import sys
from typing import Any

from build_resource_ci_cost_profile import (
    BRANCH,
    BUILD_COMMAND,
    NON_CLAIMS,
    PROFILE_ID,
    RESULT,
    ROOT,
    WORKFLOW,
    LEAN_THEOREMS,
)


DOC = ROOT / "docs" / "resource_ci_cost_profile.md"
LEAN_FIXTURE = ROOT / "lean" / "AsiStackProofs" / "ResourceEconomics.lean"
SHA_RE = re.compile(r"^[0-9a-f]{64}$")
KNOWN_FAILURE_TYPES = {
    "generated_scaffold_drift",
    "github_pages_deploy_service_failure",
    "unclassified_workflow_failure",
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Resource CI cost profile validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def seconds_between(start: str, end: str) -> int:
    return int((parse_time(end) - parse_time(start)).total_seconds())


def text_blob(value: Any) -> str:
    if isinstance(value, dict):
        return "\n".join(f"{key}: {text_blob(child)}" for key, child in value.items()).lower()
    if isinstance(value, list):
        return "\n".join(text_blob(item) for item in value).lower()
    return str(value).lower()


def validate_shape(value: dict[str, Any], errors: list[str]) -> None:
    expected = {
        "profile_id": PROFILE_ID,
        "record_kind": "resource_ci_cost_profile",
        "command": BUILD_COMMAND,
        "workflow": WORKFLOW,
        "branch": BRANCH,
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
    }
    for key, expected_value in expected.items():
        if value.get(key) != expected_value:
            errors.append(f"{rel(RESULT)}: {key} must be {expected_value!r}.")
    if not isinstance(value.get("recorded_at_utc"), str) or not value["recorded_at_utc"].endswith("Z"):
        errors.append(f"{rel(RESULT)}: recorded_at_utc must be a UTC timestamp ending in Z.")
    source_commands = value.get("source_commands")
    if not isinstance(source_commands, list) or "gh run list" not in text_blob(source_commands):
        errors.append(f"{rel(RESULT)}: source_commands must include the gh run list command.")
    if value.get("non_claims") != NON_CLAIMS:
        errors.append(f"{rel(RESULT)}: non_claims must match the builder's explicit non-claims.")
    non_claim_text = text_blob(value.get("non_claims"))
    for phrase in (
        "does not promote any chapter core claim",
        "does not create a support-state transition",
        "does not prove deployed scheduler behavior",
        "github actions publication-pipeline metadata only",
    ):
        if phrase not in non_claim_text:
            errors.append(f"{rel(RESULT)}: non_claims missing phrase {phrase!r}.")


def validate_runs(value: dict[str, Any], errors: list[str]) -> None:
    runs = value.get("runs")
    if not isinstance(runs, list) or len(runs) < 7:
        errors.append(f"{rel(RESULT)}: runs must contain at least seven recent workflow runs.")
        return
    seen_ids: set[int] = set()
    completed_durations: list[int] = []
    success_durations: list[int] = []
    success_count = 0
    failure_count = 0
    in_progress_count = 0

    for index, run in enumerate(runs):
        owner = f"{rel(RESULT)}:runs[{index}]"
        if not isinstance(run, dict):
            errors.append(f"{owner}: run must be an object.")
            continue
        for key in ("run_id", "title", "head_sha", "status", "event", "workflow", "created_at", "updated_at", "url"):
            if key not in run:
                errors.append(f"{owner}: missing {key}.")
        run_id = run.get("run_id")
        if not isinstance(run_id, int):
            errors.append(f"{owner}: run_id must be an integer.")
        elif run_id in seen_ids:
            errors.append(f"{owner}: duplicate run_id {run_id}.")
        else:
            seen_ids.add(run_id)
        if run.get("workflow") != WORKFLOW:
            errors.append(f"{owner}: workflow must be {WORKFLOW!r}.")
        if not str(run.get("url", "")).startswith("https://github.com/corbensorenson/asi-stack-book/actions/runs/"):
            errors.append(f"{owner}: url must point to the public GitHub Actions run.")
        duration = seconds_between(str(run.get("created_at", "")), str(run.get("updated_at", "")))
        if run.get("duration_seconds") != duration:
            errors.append(f"{owner}: duration_seconds must equal timestamp delta {duration}.")
        if run.get("status") == "completed":
            completed_durations.append(duration)
            if run.get("conclusion") == "success":
                success_count += 1
                success_durations.append(duration)
            elif run.get("conclusion") == "failure":
                failure_count += 1
            else:
                errors.append(f"{owner}: completed run must have success or failure conclusion.")
        else:
            in_progress_count += 1

    metrics = value.get("metrics")
    if not isinstance(metrics, dict):
        errors.append(f"{rel(RESULT)}: metrics must be an object.")
        return
    expected_metrics = {
        "run_count": len(runs),
        "completed_run_count": len(completed_durations),
        "success_count": success_count,
        "failure_count": failure_count,
        "in_progress_count": in_progress_count,
        "completed_duration_seconds_total": sum(completed_durations),
        "completed_duration_seconds_median": int(statistics.median(completed_durations)) if completed_durations else 0,
        "completed_duration_seconds_mean": round(sum(completed_durations) / len(completed_durations), 3)
        if completed_durations
        else 0,
        "success_duration_seconds_mean": round(sum(success_durations) / len(success_durations), 3)
        if success_durations
        else 0,
    }
    for key, expected_value in expected_metrics.items():
        if metrics.get(key) != expected_value:
            errors.append(f"{rel(RESULT)}: metrics.{key} must be {expected_value!r}.")
    if failure_count < 1:
        errors.append(f"{rel(RESULT)}: profile must include at least one completed failure for failure-cost accounting.")
    if success_count < 1:
        errors.append(f"{rel(RESULT)}: profile must include at least one completed success for recovery-cost accounting.")


def validate_failure_and_repair(value: dict[str, Any], errors: list[str]) -> None:
    failures = value.get("failure_events")
    repairs = value.get("repair_events")
    if not isinstance(failures, list) or not failures:
        errors.append(f"{rel(RESULT)}: failure_events must be a non-empty list.")
        return
    if not isinstance(repairs, list) or not repairs:
        errors.append(f"{rel(RESULT)}: repair_events must be a non-empty list.")
        return
    for failure in failures:
        if not isinstance(failure, dict):
            continue
        failure_type = failure.get("failure_type")
        if failure_type not in KNOWN_FAILURE_TYPES:
            errors.append(f"{rel(RESULT)}: failure_type must be one of {sorted(KNOWN_FAILURE_TYPES)}.")
        if not isinstance(failure.get("failure_stage"), str) or not failure["failure_stage"].strip():
            errors.append(f"{rel(RESULT)}: failure_stage must be a non-empty string.")
        boundary = str(failure.get("classification_boundary", "")).lower()
        if "publication-pipeline" not in boundary and "not a chapter evidence result" not in boundary:
            errors.append(f"{rel(RESULT)}: failure classification must preserve a non-evidence boundary.")
        digest = str(failure.get("log_summary", {}).get("sha256", ""))
        if not SHA_RE.match(digest):
            errors.append(f"{rel(RESULT)}: failure event log summary must include a SHA-256 digest.")
        log_text = text_blob(failure.get("log_summary", {}))
        if failure_type == "generated_scaffold_drift":
            for phrase in ("git diff --exit-code", "check generated scaffold"):
                if phrase not in log_text:
                    errors.append(f"{rel(RESULT)}: generated scaffold failure missing {phrase!r}.")
        if failure_type == "github_pages_deploy_service_failure":
            for phrase in ("deploy to github pages", "deployment failed"):
                if phrase not in log_text:
                    errors.append(f"{rel(RESULT)}: Pages deploy failure missing {phrase!r}.")
    repair_text = text_blob(repairs)
    if "repair_boundary" not in repair_text or "does not prove the underlying chapter claim" not in repair_text:
        errors.append(f"{rel(RESULT)}: repair_events must preserve the no-claim repair boundary.")


def validate_lean_alignment(value: dict[str, Any], errors: list[str]) -> None:
    alignment = value.get("lean_fixture_alignment")
    if not isinstance(alignment, dict):
        errors.append(f"{rel(RESULT)}: lean_fixture_alignment must be an object.")
        return

    metrics = value.get("metrics")
    failures = value.get("failure_events")
    repairs = value.get("repair_events")
    if not isinstance(metrics, dict) or not isinstance(failures, list) or not isinstance(repairs, list):
        errors.append(f"{rel(RESULT)}: metrics, failure_events, and repair_events are required for Lean alignment.")
        return

    failure_type_counts = Counter(str(failure.get("failure_type", "")) for failure in failures if isinstance(failure, dict))
    repair_durations = [
        int(repair["repair_duration_seconds"])
        for repair in repairs
        if isinstance(repair, dict) and isinstance(repair.get("repair_duration_seconds"), int)
    ]
    expected = {
        "proof_bridge_type": "finite CI failure-classification summary",
        "lean_module": "AsiStackProofs.ResourceEconomics",
        "lean_fixture": "resourceCICostProfileFixture",
        "lean_theorem_names": LEAN_THEOREMS,
        "run_count": metrics.get("run_count"),
        "completed_run_count": metrics.get("completed_run_count"),
        "success_count": metrics.get("success_count"),
        "failure_count": metrics.get("failure_count"),
        "in_progress_count": metrics.get("in_progress_count"),
        "deploy_service_failure_count": failure_type_counts.get("github_pages_deploy_service_failure", 0),
        "classified_failure_count": len(failures),
        "recovery_run_seconds": min(repair_durations) if repair_durations else 0,
        "support_state_effect_none": value.get("support_state_effect") == "none",
        "chapter_core_support_effect_none": value.get("chapter_core_support_effect") == "none",
        "evidence_transition_created": value.get("evidence_transition_created"),
        "publication_metadata_only": True,
        "classified_failures": len(failures) == metrics.get("failure_count"),
        "deploy_service_failures_match_failures": failure_type_counts.get("github_pages_deploy_service_failure", 0)
        == metrics.get("failure_count"),
        "non_evidence_boundary": all(
            "not a chapter evidence result" in str(failure.get("classification_boundary", "")).lower()
            or "publication-pipeline" in str(failure.get("classification_boundary", "")).lower()
            for failure in failures
            if isinstance(failure, dict)
        ),
        "non_claim_boundary": "does not prove deployed scheduler behavior" in text_blob(value.get("non_claims")),
    }
    for key, expected_value in expected.items():
        if alignment.get(key) != expected_value:
            errors.append(f"{rel(RESULT)}: lean_fixture_alignment.{key} must be {expected_value!r}.")

    non_claims = alignment.get("non_claims")
    non_claim_text = text_blob(non_claims)
    for term in ("finite metadata classification", "does not prove deployed scheduler behavior", "chapter-core support-state promotion"):
        if term not in non_claim_text:
            errors.append(f"{rel(RESULT)}: lean_fixture_alignment non_claims missing {term!r}.")

    if not LEAN_FIXTURE.exists():
        errors.append(f"Missing {rel(LEAN_FIXTURE)}.")
        return
    lean_text = LEAN_FIXTURE.read_text(encoding="utf-8")
    for theorem in LEAN_THEOREMS:
        if not re.search(rf"^theorem\s+{re.escape(theorem)}\b", lean_text, flags=re.MULTILINE):
            errors.append(f"{rel(LEAN_FIXTURE)} missing theorem {theorem}.")
    for fragment in (
        "structure ResourceCICostProfileSummary",
        "def resourceCICostProfileFixture",
        f"runCount := {alignment.get('run_count')}",
        f"completedRunCount := {alignment.get('completed_run_count')}",
        f"successCount := {alignment.get('success_count')}",
        f"failureCount := {alignment.get('failure_count')}",
        f"inProgressCount := {alignment.get('in_progress_count')}",
        f"deployServiceFailureCount := {alignment.get('deploy_service_failure_count')}",
        f"classifiedFailureCount := {alignment.get('classified_failure_count')}",
        f"recoveryRunSeconds := {alignment.get('recovery_run_seconds')}",
        "publicationMetadataOnly := true",
        "supportStateEffectNone := true",
        "chapterCoreSupportEffectNone := true",
        "evidenceTransitionCreated := false",
        "nonClaimBoundary := true",
    ):
        if fragment not in lean_text:
            errors.append(f"{rel(LEAN_FIXTURE)} missing CI fixture fragment {fragment!r}.")


def validate_doc(errors: list[str]) -> None:
    if not DOC.exists():
        errors.append(f"Missing {rel(DOC)}.")
        return
    text = DOC.read_text(encoding="utf-8")
    normalized_text = re.sub(r"\s+", " ", text)
    required = [
        "Resource CI Cost Profile",
        BUILD_COMMAND,
        rel(RESULT),
        "GitHub Actions publication-pipeline metadata only",
        "failure classification",
        "Finite Lean Alignment",
        "finite CI failure-classification summary",
        "resourceCICostProfileFixture",
        "Support-state effect | `none`",
        "does not promote any chapter core claim above `argument`",
    ]
    for fragment in required:
        haystack = normalized_text if " " in fragment else text
        if fragment not in haystack:
            errors.append(f"{rel(DOC)} missing required fragment: {fragment}")


def main() -> None:
    errors: list[str] = []
    if not RESULT.exists():
        fail([f"Missing {rel(RESULT)}. Run `{BUILD_COMMAND}` first."])
    value = load_json(RESULT)
    if not isinstance(value, dict):
        fail([f"{rel(RESULT)} must contain a JSON object."])
    validate_shape(value, errors)
    validate_runs(value, errors)
    validate_failure_and_repair(value, errors)
    validate_lean_alignment(value, errors)
    validate_doc(errors)
    if errors:
        fail(errors)
    print(
        "Resource CI cost profile validation passed: "
        f"{value['metrics']['run_count']} run(s), "
        f"{value['metrics']['completed_run_count']} completed, "
        f"{value['metrics']['failure_count']} failure event(s), support-state effect none."
    )


if __name__ == "__main__":
    main()
