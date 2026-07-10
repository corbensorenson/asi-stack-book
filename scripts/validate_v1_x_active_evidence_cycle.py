#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "v1_x_active_evidence_cycle.md"
STRUCTURE = ROOT / "book_structure.json"

MIN_SELECTED = 1
MAX_SELECTED = 3
EXPECTED_SELECTED = {
    "resource-economics-and-token-budgets",
    "project-theseus-as-report-first-implementation-reference",
    "fast-generation-architectures",
}
STATIC_REQUIRED_FRAGMENTS = (
    "Last updated: 2026-07-09",
    "Selected chapter lanes | 3",
    "Lane cap | 1 flagship measured lane plus at most 2 direct support lanes per v1.x cycle",
    "Flagship measured lane | `resource-economics-and-token-budgets`",
    "Direct support lanes | `project-theseus-as-report-first-implementation-reference`; `fast-generation-architectures`",
    "No chapter core promotion",
    "does not promote any chapter core claim above `argument`",
    "docs/costed_route_resource_slice.md",
    "docs/resource_workflow_trace.md",
    "docs/resource_live_probe.md",
    "docs/resource_ci_cost_profile.md",
    "finite CI failure-classification summary",
    "resourceCICostProfileFixture",
    "eight completed runs",
    "five successful completed runs",
    "three classified GitHub Pages deploy-service failures",
    "131-second recovery boundary",
    "docs/resource_flagship_lane_run.md",
    "evidence_transitions/v1_x_measured/resource_workflow_trace_no_change.json",
    "evidence_transitions/v1_x_measured/resource_live_probe_no_change.json",
    "evidence_transitions/v1_x_measured/resource_workload_quality_selector_empirical_test_backed.json",
    "evidence_transitions/v1_x_measured/resource_workload_quality_probe_no_change.json",
    "evidence_transitions/v1_x_measured/resource_load_stability_probe_no_change.json",
    "evidence_transitions/v1_x_measured/resource_ci_cost_profile_no_change.json",
    "docs/simulation_transfer_boundary_harness.md",
    "docs/theseus_report_import_slice.md",
    "docs/theseus_generation_mode_import_slice.md",
    "docs/theseus_support_replay_probe.md",
    "docs/fast_generation_task_bundle.md",
    "evidence_transitions/v1_x_measured/fast_generation_task_bundle_no_change.json",
    "evidence_transitions/v1_x_measured/theseus_public_task_bundle_import_no_change.json",
    "lean/AsiStackProofs/FastGeneration.lean",
)


def fail(errors: list[str]) -> None:
    print("v1.x active evidence-cycle validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def manifest_chapter_ids() -> list[str]:
    value = json.loads(STRUCTURE.read_text(encoding="utf-8"))
    return [
        str(chapter["id"])
        for part in value.get("parts", [])
        for chapter in part.get("chapters", [])
    ]


def section(text: str, start: str, end: str | None = None) -> str:
    start_marker = f"## {start}"
    start_index = text.find(start_marker)
    if start_index < 0:
        return ""
    if end is None:
        return text[start_index:]
    end_marker = f"## {end}"
    end_index = text.find(end_marker, start_index + len(start_marker))
    if end_index < 0:
        return text[start_index:]
    return text[start_index:end_index]


def main() -> None:
    errors: list[str] = []
    text = DOC.read_text(encoding="utf-8")
    all_ids = set(manifest_chapter_ids())
    selected_section = section(text, "Selected Lanes", "Planned-Only Lanes")
    planned_section = section(text, "Planned-Only Lanes", "Non-Claims")

    selected_ids = {
        match.group(1)
        for match in re.finditer(r"^\|\s*`([^`]+)`\s*\|", selected_section, re.MULTILINE)
    }
    planned_ids = {
        match.group(1)
        for match in re.finditer(r"^-\s*`([^`]+)`\s*$", planned_section, re.MULTILINE)
    }

    if selected_ids != EXPECTED_SELECTED:
        errors.append(f"Selected lane set mismatch: {sorted(selected_ids)}")
    if not (MIN_SELECTED <= len(selected_ids) <= MAX_SELECTED):
        errors.append(f"Selected lane count {len(selected_ids)} is outside {MIN_SELECTED}-{MAX_SELECTED}.")
    if selected_ids & planned_ids:
        errors.append(f"Chapter IDs listed as both selected and planned-only: {sorted(selected_ids & planned_ids)}")
    if selected_ids | planned_ids != all_ids:
        missing = sorted(all_ids - (selected_ids | planned_ids))
        extra = sorted((selected_ids | planned_ids) - all_ids)
        if missing:
            errors.append(f"Missing manifest chapter IDs: {missing}")
        if extra:
            errors.append(f"Unknown chapter IDs: {extra}")
    expected_planned = len(all_ids) - len(selected_ids)
    if len(planned_ids) != expected_planned:
        errors.append(f"Planned-only lane count {len(planned_ids)} does not match manifest remainder.")
    dynamic_required_fragments = (
        f"Planned-only chapter lanes | {expected_planned}",
        f"No {len(all_ids)}-lane fixture sweep is claimed or implied.",
        f"all {len(all_ids)} chapter core claims remain `argument`",
    )
    for fragment in STATIC_REQUIRED_FRAGMENTS + dynamic_required_fragments:
        if fragment not in text:
            errors.append(f"Missing required fragment: {fragment}")

    referenced_paths = (
        "docs/costed_route_resource_slice.md",
        "experiments/costed_route_resource_slice/results/2026-06-29-local.json",
        "lean/AsiStackProofs/ResourceEconomics.lean",
        "evidence_transitions/v1_0_measured/costed_route_resource_slice_synthetic_test_backed.json",
        "docs/resource_workflow_trace.md",
        "experiments/resource_workflow_trace/results/2026-07-01-local.json",
        "scripts/validate_resource_workflow_trace.py",
        "docs/resource_live_probe.md",
        "experiments/resource_live_probe/results/2026-07-01-local.json",
        "scripts/validate_resource_live_probe.py",
        "docs/resource_ci_cost_profile.md",
        "experiments/resource_ci_cost_profile/results/2026-07-04-main.json",
        "scripts/validate_resource_ci_cost_profile.py",
        "docs/resource_flagship_lane_run.md",
        "experiments/resource_flagship_lane/results/2026-07-01-local.json",
        "scripts/run_resource_flagship_lane.py",
        "scripts/validate_resource_flagship_lane.py",
        "evidence_transitions/v1_x_measured/resource_workflow_trace_no_change.json",
        "evidence_transitions/v1_x_measured/resource_live_probe_no_change.json",
        "evidence_transitions/v1_x_measured/resource_workload_quality_selector_empirical_test_backed.json",
        "evidence_transitions/v1_x_measured/resource_workload_quality_probe_no_change.json",
        "evidence_transitions/v1_x_measured/resource_load_stability_probe_no_change.json",
        "evidence_transitions/v1_x_measured/resource_ci_cost_profile_no_change.json",
        "schemas/simulation_contract_record.schema.json",
        "docs/simulation_transfer_boundary_harness.md",
        "experiments/simulation_transfer_boundaries/results/2026-06-30-local.md",
        "docs/theseus_report_import_slice.md",
        "experiments/theseus_import/results/2026-06-29-local.json",
        "scripts/validate_theseus_report.py",
        "docs/theseus_generation_mode_import_slice.md",
        "experiments/theseus_generation_mode_import/results/2026-07-01-local.json",
        "lean/AsiStackProofs/FastGeneration.lean",
        "scripts/validate_theseus_generation_mode_import.py",
        "docs/theseus_support_replay_probe.md",
        "experiments/theseus_support_replay_probe/results/2026-07-01-local.json",
        "scripts/run_theseus_support_replay_probe.py",
        "scripts/validate_theseus_support_replay_probe.py",
        "docs/fast_generation_task_bundle.md",
        "experiments/fast_generation_task_bundle/results/2026-07-02-local.json",
        "scripts/validate_fast_generation_task_bundle.py",
        "evidence_transitions/v1_x_measured/fast_generation_task_bundle_no_change.json",
        "evidence_transitions/v1_x_measured/theseus_public_task_bundle_import_no_change.json",
    )
    for relative in referenced_paths:
        if relative not in text:
            errors.append(f"Document does not reference required artifact {relative}.")
        if not (ROOT / relative).exists():
            errors.append(f"Referenced artifact does not exist: {relative}")

    if errors:
        fail(errors)

    print(
        "v1.x active evidence-cycle validation passed: "
        f"{len(selected_ids)} selected lanes, {len(planned_ids)} planned-only lanes."
    )


if __name__ == "__main__":
    main()
