#!/usr/bin/env python3
"""Generate and validate the Project Theseus static-import status ledger."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "docs" / "v1_0_candidate_status.md"
LEDGER = ROOT / "docs" / "project_theseus_static_import_status_ledger.md"

ARCH_RESULT = ROOT / "experiments" / "theseus_import" / "results" / "2026-06-29-local.json"
ARCH_FIXTURE = ROOT / "experiments" / "theseus_import" / "fixtures" / "valid" / "architecture_gate_public_report.valid.json"
GEN_RESULT = ROOT / "experiments" / "theseus_generation_mode_import" / "results" / "2026-07-01-local.json"
GEN_FIXTURE = ROOT / "experiments" / "theseus_generation_mode_import" / "fixtures" / "valid" / "generation_mode_gate_public_summary.valid.json"
SUPPORT_REPLAY = ROOT / "experiments" / "theseus_support_replay_probe" / "results" / "2026-07-01-local.json"
TASK_RESULT = ROOT / "experiments" / "theseus_public_task_bundle_import" / "results" / "2026-07-03-local.json"
TASK_FIXTURE = ROOT / "experiments" / "theseus_public_task_bundle_import" / "fixtures" / "valid" / "public_task_bundle_import.valid.json"
NO_PROMOTION = ROOT / "evidence_transitions" / "v1_x_measured" / "theseus_public_task_bundle_import_no_change.json"

DOCS = (
    "docs/theseus_report_import_slice.md",
    "docs/theseus_generation_mode_import_slice.md",
    "docs/theseus_support_replay_probe.md",
    "docs/theseus_public_task_bundle_import.md",
)
VALIDATORS = (
    "python3 scripts/validate_theseus_report.py",
    "python3 scripts/validate_theseus_generation_mode_import.py",
    "python3 scripts/run_theseus_support_replay_probe.py --write-result",
    "python3 scripts/validate_theseus_support_replay_probe.py",
    "python3 scripts/validate_theseus_public_task_bundle_import.py",
)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def qmd_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def compact_status_row(metrics: dict[str, Any] | None = None) -> str:
    if metrics is None:
        metrics, errors = collect_metrics()
        if errors:
            raise RuntimeError("; ".join(errors))
    return (
        "| Project Theseus static import lane | "
        f"Project Theseus detail is generated in `docs/project_theseus_static_import_status_ledger.md`: "
        f"{metrics['static_report_imports']} sanitized static report imports, "
        f"{metrics['support_replay_count']} support replay probe, "
        f"{metrics['public_task_count']} metadata-only public tasks, "
        f"{metrics['public_training_rows']} public training rows, "
        f"{metrics['generation_mode_count']} generation modes, "
        f"{metrics['generation_comparison_count']} comparisons, "
        f"{metrics['promotable_comparison_count']} promotable comparisons, "
        f"{metrics['expected_invalid_total']} expected-invalid controls, "
        f"and {metrics['no_promotion_decisions']} accepted no-promotion decision; clean live replay remains unclaimed. "
        "| `docs/project_theseus_static_import_status_ledger.md`; "
        "`docs/theseus_report_import_slice.md`; "
        "`docs/theseus_generation_mode_import_slice.md`; "
        "`docs/theseus_support_replay_probe.md`; "
        "`docs/theseus_public_task_bundle_import.md`; "
        "`evidence_transitions/v1_x_measured/theseus_public_task_bundle_import_no_change.json`; "
        "`python3 scripts/validate_project_theseus_static_import_status_ledger.py` |"
    )


def collect_metrics() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    required = [
        ARCH_RESULT,
        ARCH_FIXTURE,
        GEN_RESULT,
        GEN_FIXTURE,
        SUPPORT_REPLAY,
        TASK_RESULT,
        TASK_FIXTURE,
        NO_PROMOTION,
        *(ROOT / path for path in DOCS),
    ]
    for path in required:
        if not path.exists():
            errors.append(f"required path missing: {rel(path)}")
    if errors:
        return {}, errors

    arch_result = load_json(ARCH_RESULT)
    arch_fixture = load_json(ARCH_FIXTURE)
    gen_result = load_json(GEN_RESULT)
    gen_fixture = load_json(GEN_FIXTURE)
    support_replay = load_json(SUPPORT_REPLAY)
    task_result = load_json(TASK_RESULT)
    task_fixture = load_json(TASK_FIXTURE)
    no_promotion = load_json(NO_PROMOTION)

    if arch_result.get("validation_result") != "pass":
        errors.append("architecture-gate import result must pass.")
    if arch_result.get("accepted_gate_count") != 14 or arch_result.get("accepted_passed_count") != 14:
        errors.append("architecture-gate import must keep 14/14 accepted gates.")
    if arch_result.get("expected_invalid_count") != 3:
        errors.append("architecture-gate import must keep three expected-invalid controls.")
    if arch_result.get("support_state_effect") != "no_chapter_core_claim_promotion":
        errors.append("architecture-gate import support_state_effect drifted.")
    if arch_fixture.get("source_project", {}).get("worktree_state") != "dirty_at_import_review":
        errors.append("architecture-gate import must preserve dirty-at-import boundary.")
    if arch_fixture.get("decision_summary", {}).get("external_inference_calls") != 0:
        errors.append("architecture-gate import must preserve zero external inference calls.")

    if gen_result.get("validation_result") != "pass":
        errors.append("generation-mode import result must pass.")
    if gen_result.get("accepted_mode_count") != 18 or gen_result.get("accepted_comparison_count") != 13:
        errors.append("generation-mode import must keep 18 modes and 13 comparisons.")
    if gen_result.get("accepted_hard_gap_count") != 0 or gen_result.get("accepted_promotable_comparison_count") != 0:
        errors.append("generation-mode import hard-gap/promotable counts drifted.")
    if gen_result.get("accepted_useful_solution_per_second") != 0.0:
        errors.append("generation-mode import useful-solution-per-second must remain 0.0.")
    if gen_result.get("expected_invalid_count") != 6:
        errors.append("generation-mode import must keep six expected-invalid controls.")
    if gen_result.get("support_state_effect") != "no_chapter_core_claim_promotion":
        errors.append("generation-mode import support_state_effect drifted.")
    if gen_fixture.get("source_project", {}).get("worktree_state") != "dirty_at_import_review":
        errors.append("generation-mode import must preserve dirty-at-import boundary.")

    if support_replay.get("pass") is not True:
        errors.append("Theseus support replay probe must record pass true.")
    if len(support_replay.get("replay_commands", [])) != 2:
        errors.append("Theseus support replay probe must keep two replayed validators.")
    if support_replay.get("support_state_effect") != "none":
        errors.append("Theseus support replay support_state_effect must remain none.")
    if support_replay.get("chapter_core_support_effect") != "none":
        errors.append("Theseus support replay chapter_core_support_effect must remain none.")

    public_boundary = task_fixture.get("public_boundary", {})
    operator = task_fixture.get("operator_execution", {})
    task_bundle = task_fixture.get("task_bundle", {})
    benchmark = task_fixture.get("benchmark_result", {})
    quality = task_fixture.get("quality_boundary", {})
    source_project = task_fixture.get("source_project", {})

    if task_result.get("validation_result") != "pass":
        errors.append("Theseus public task-bundle import result must pass.")
    if task_result.get("expected_invalid_count") != 7:
        errors.append("Theseus public task-bundle import must keep seven expected-invalid controls.")
    if task_result.get("source_report_count") != 7 or task_result.get("artifact_gap_count") != 5:
        errors.append("Theseus public task-bundle source report/artifact gap counts drifted.")
    if task_result.get("public_task_count") != 64 or benchmark.get("public_task_count") != 64:
        errors.append("Theseus public task-bundle import must keep 64 public metadata-only tasks.")
    if public_boundary.get("public_training_rows_written") != 0 or task_bundle.get("public_training_rows") != 0:
        errors.append("Theseus public task-bundle import must keep zero public training rows.")
    if public_boundary.get("external_inference_calls") != 0:
        errors.append("Theseus public task-bundle import must keep zero external inference calls.")
    if operator.get("operator_gate_count") != 12 or operator.get("operator_gates_passed") != 12:
        errors.append("Theseus public task-bundle import must keep 12/12 operator gates.")
    if task_result.get("benchmark_gate_count") != 18 or benchmark.get("benchmark_gates_passed") != 18:
        errors.append("Theseus public task-bundle import must keep 18/18 benchmark gates.")
    if task_result.get("residual_count") != 19 or benchmark.get("residual_count") != 19:
        errors.append("Theseus public task-bundle import must keep 19 residuals.")
    if benchmark.get("task_level_regressions_vs_single_stream") != 0:
        errors.append("Theseus public task-bundle import must keep zero task-level regressions.")
    if quality.get("quality_pass_count") != 45:
        errors.append("Theseus public task-bundle import must keep 45 quality-passing candidates.")
    if benchmark.get("student_candidate_count") != 512:
        errors.append("Theseus public task-bundle import must keep 512 student candidates in the public summary.")
    if source_project.get("working_tree_dirty_at_import") is not True or source_project.get("clean_live_replay_claimed") is not False:
        errors.append("Theseus public task-bundle import must preserve dirty-checkout/no-clean-live-replay boundary.")
    if task_result.get("support_state_effect") != "none" or task_result.get("chapter_core_support_effect") != "none":
        errors.append("Theseus public task-bundle import support effects must remain none.")

    if no_promotion.get("review_status") != "accepted":
        errors.append("Theseus public task-bundle no-promotion decision must remain accepted.")
    if no_promotion.get("transition_effect") != "no_change":
        errors.append("Theseus public task-bundle transition_effect must remain no_change.")
    if no_promotion.get("support_state_effect") != "blocks_promotion":
        errors.append("Theseus public task-bundle decision must keep blocks_promotion.")
    no_promotion_text = " ".join(
        [
            str(no_promotion.get("scope_boundary", "")),
            str(no_promotion.get("transition_reason", "")),
            " ".join(str(item) for item in no_promotion.get("non_claims", [])),
        ]
    )
    for fragment in ("clean live", "model quality", "chapter-core"):
        if fragment not in no_promotion_text:
            errors.append(f"Theseus no-promotion decision missing boundary fragment: {fragment}")

    metrics = {
        "static_report_imports": 2,
        "support_replay_count": 1,
        "support_replay_commands": len(support_replay.get("replay_commands", [])),
        "support_replay_tracked_artifacts": len(support_replay.get("tracked_artifacts", [])),
        "architecture_gate_count": arch_result.get("accepted_gate_count"),
        "architecture_gate_passed": arch_result.get("accepted_passed_count"),
        "architecture_expected_invalid": arch_result.get("expected_invalid_count"),
        "architecture_source_sha": arch_result.get("source_artifact_sha256"),
        "architecture_public_sha": arch_result.get("accepted_public_report_sha256"),
        "generation_mode_count": gen_result.get("accepted_mode_count"),
        "generation_comparison_count": gen_result.get("accepted_comparison_count"),
        "generation_hard_gap_count": gen_result.get("accepted_hard_gap_count"),
        "promotable_comparison_count": gen_result.get("accepted_promotable_comparison_count"),
        "useful_solution_per_second": gen_result.get("accepted_useful_solution_per_second"),
        "generation_expected_invalid": gen_result.get("expected_invalid_count"),
        "generation_source_sha": gen_result.get("source_artifact_sha256"),
        "generation_public_sha": gen_result.get("accepted_public_report_sha256"),
        "public_task_count": task_result.get("public_task_count"),
        "public_training_rows": public_boundary.get("public_training_rows_written"),
        "external_inference_calls": public_boundary.get("external_inference_calls"),
        "operator_gate_count": operator.get("operator_gate_count"),
        "operator_gate_passed": operator.get("operator_gates_passed"),
        "benchmark_gate_count": task_result.get("benchmark_gate_count"),
        "benchmark_gate_passed": benchmark.get("benchmark_gates_passed"),
        "residual_count": task_result.get("residual_count"),
        "task_regression_count": benchmark.get("task_level_regressions_vs_single_stream"),
        "artifact_gap_count": task_result.get("artifact_gap_count"),
        "source_report_count": task_result.get("source_report_count"),
        "student_candidate_count": benchmark.get("student_candidate_count"),
        "quality_pass_count": quality.get("quality_pass_count"),
        "public_calibration_pass_rate": benchmark.get("real_public_task_pass_rate"),
        "task_expected_invalid": task_result.get("expected_invalid_count"),
        "expected_invalid_total": arch_result.get("expected_invalid_count", 0)
        + gen_result.get("expected_invalid_count", 0)
        + task_result.get("expected_invalid_count", 0),
        "no_promotion_decisions": 1,
        "source_commit_short": str(source_project.get("commit", ""))[:8],
    }
    return metrics, errors


def build_report(metrics: dict[str, Any], errors: list[str]) -> str:
    validation_lines = ["- None."] if not errors else [f"- {error}" for error in errors]
    return "\n".join(
        [
            "# Project Theseus Static Import Status Ledger",
            "",
            "Generated by `python3 scripts/validate_project_theseus_static_import_status_ledger.py --write`.",
            "",
            "This ledger replaces the former long `Project Theseus static import lane` cell in `docs/v1_0_candidate_status.md`. It records public-safe Project Theseus import evidence, replay probes, and no-promotion boundaries without claiming a clean live Theseus replay, model quality, benchmark superiority, speed, useful-solution-per-second improvement, deployment readiness, self-evolution, or chapter-core support movement.",
            "",
            "## Summary",
            "",
            "| Metric | Value |",
            "|---|---:|",
            f"| Sanitized static report imports | {metrics['static_report_imports']} |",
            f"| Support replay probes | {metrics['support_replay_count']} |",
            f"| Replayed validators in support probe | {metrics['support_replay_commands']} |",
            f"| Support replay tracked artifacts | {metrics['support_replay_tracked_artifacts']} |",
            f"| Architecture gates passed | {metrics['architecture_gate_passed']} / {metrics['architecture_gate_count']} |",
            f"| Generation modes / comparisons | {metrics['generation_mode_count']} / {metrics['generation_comparison_count']} |",
            f"| Promotable comparisons | {metrics['promotable_comparison_count']} |",
            f"| Useful solution per second | {metrics['useful_solution_per_second']} |",
            f"| Metadata-only public tasks | {metrics['public_task_count']} |",
            f"| Public training rows | {metrics['public_training_rows']} |",
            f"| External inference calls | {metrics['external_inference_calls']} |",
            f"| Operator gates passed | {metrics['operator_gate_passed']} / {metrics['operator_gate_count']} |",
            f"| Benchmark gates passed | {metrics['benchmark_gate_passed']} / {metrics['benchmark_gate_count']} |",
            f"| Residuals / artifact gaps | {metrics['residual_count']} / {metrics['artifact_gap_count']} |",
            f"| Expected-invalid controls | {metrics['expected_invalid_total']} |",
            f"| Accepted no-promotion decisions | {metrics['no_promotion_decisions']} |",
            "",
            "## Status-Page Row",
            "",
            compact_status_row(metrics),
            "",
            "## Imported Evidence Surfaces",
            "",
            f"- `docs/theseus_report_import_slice.md` records source commit `{metrics['source_commit_short']}`, a dirty-at-import-review boundary, source SHA-256 `{metrics['architecture_source_sha']}`, public fixture SHA-256 `{metrics['architecture_public_sha']}`, and {metrics['architecture_gate_passed']}/{metrics['architecture_gate_count']} architecture gates passed with {metrics['architecture_expected_invalid']} expected-invalid controls.",
            f"- `docs/theseus_generation_mode_import_slice.md` records source SHA-256 `{metrics['generation_source_sha']}`, public fixture SHA-256 `{metrics['generation_public_sha']}`, {metrics['generation_mode_count']} modes, {metrics['generation_comparison_count']} comparisons, {metrics['generation_hard_gap_count']} hard gaps, {metrics['promotable_comparison_count']} promotable comparisons, {metrics['useful_solution_per_second']} useful-solution-per-second evidence, and {metrics['generation_expected_invalid']} expected-invalid controls.",
            f"- `docs/theseus_support_replay_probe.md` records {metrics['support_replay_commands']} local validator replays and {metrics['support_replay_tracked_artifacts']} tracked artifact hashes with support-state effect `none`.",
            f"- `docs/theseus_public_task_bundle_import.md` records {metrics['source_report_count']} source reports, {metrics['public_task_count']} metadata-only public tasks, {metrics['public_training_rows']} public training rows, {metrics['external_inference_calls']} external inference calls, {metrics['operator_gate_passed']}/{metrics['operator_gate_count']} operator gates, {metrics['benchmark_gate_passed']}/{metrics['benchmark_gate_count']} benchmark gates, {metrics['residual_count']} residuals, {metrics['task_regression_count']} task-level regressions, {metrics['student_candidate_count']} student candidates in the public summary, {metrics['quality_pass_count']} quality-passing candidates, {metrics['artifact_gap_count']} artifact gaps, and {metrics['task_expected_invalid']} expected-invalid controls.",
            f"- `evidence_transitions/v1_x_measured/theseus_public_task_bundle_import_no_change.json` is the accepted no-promotion decision: it blocks clean-live-replay, model-quality, benchmark-superiority, generation-speed, useful-solution-per-second, support-state, deployment, self-evolution, and chapter-core promotion claims.",
            "",
            "## Non-Claim Boundary",
            "",
            "- This ledger does not prove clean live Project Theseus replay.",
            "- This ledger does not prove model quality, benchmark superiority, generation speed, useful-solution-per-second improvement, deployment readiness, self-evolution, transfer, safety, or ASI.",
            "- This ledger does not copy private Project Theseus payloads, prompts, tests, solutions, candidate code, traces, score labels, checkpoints, or training rows into this repository.",
            "- This ledger does not promote any chapter core claim above `argument` and does not create an upward support-state transition.",
            "",
            "## Validation Errors",
            "",
            *validation_lines,
            "",
        ]
    )


def write_status_row(row: str) -> None:
    lines = STATUS.read_text(encoding="utf-8").splitlines()
    matches = [index for index, line in enumerate(lines) if line.startswith("| Project Theseus static import lane |")]
    if len(matches) != 1:
        fail([f"{rel(STATUS)} must contain exactly one Project Theseus static import lane row; found {len(matches)}."])
    lines[matches[0]] = row
    STATUS.write_text("\n".join(lines) + "\n", encoding="utf-8")


def fail(errors: list[str]) -> None:
    print("Project Theseus static import status ledger validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def validate(args: argparse.Namespace) -> list[str]:
    metrics, errors = collect_metrics()
    if not metrics:
        return errors
    report = build_report(metrics, errors)
    row = compact_status_row(metrics)

    if args.write:
        LEDGER.write_text(report, encoding="utf-8")
    if args.write_status_row:
        write_status_row(row)
    if args.write or args.write_status_row:
        return errors

    if not LEDGER.exists():
        errors.append(f"{rel(LEDGER)} is missing; run with --write.")
    elif LEDGER.read_text(encoding="utf-8") != report:
        errors.append(f"{rel(LEDGER)} is out of date; run with --write.")

    status_text = STATUS.read_text(encoding="utf-8")
    if row not in status_text:
        errors.append(f"{rel(STATUS)} is missing the compact Project Theseus static import row.")
    stale_fragments = (
        "The public-safe Project Theseus import lane now records two sanitized static report fixtures",
        "The public task-bundle import records `theseus_public_task_bundle_import_2026_07_03_local`",
    )
    for stale in stale_fragments:
        if stale in status_text:
            errors.append(f"{rel(STATUS)} still contains stale expanded Project Theseus text: {stale}")
    for line in status_text.splitlines():
        if line.startswith("| Project Theseus static import lane |") and len(line) > 1400:
            errors.append(f"{rel(STATUS)} Project Theseus static import row is still too long: {len(line)} characters.")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="rewrite the tracked ledger")
    parser.add_argument("--write-status-row", action="store_true", help="rewrite the compact status row")
    args = parser.parse_args()
    errors = validate(args)
    if errors:
        fail(errors)
    action = "wrote" if args.write or args.write_status_row else "validated"
    metrics, _ = collect_metrics()
    print(
        f"Project Theseus static import status ledger {action}: "
        f"{metrics['static_report_imports']} static imports, "
        f"{metrics['public_task_count']} public tasks, "
        f"{metrics['expected_invalid_total']} expected-invalid controls."
    )


if __name__ == "__main__":
    main()
