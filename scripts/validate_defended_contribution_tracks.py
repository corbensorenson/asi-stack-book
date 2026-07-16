#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "defended_contribution_tracks.md"
ACTIVE_CYCLE = ROOT / "docs" / "v1_x_active_evidence_cycle.md"
SCORECARD = ROOT / "docs" / "a_plus_quality_scorecard.md"

EXPECTED_TRACKS = {
    "living-evidence-book-methodology",
    "claim-support-states-and-evidence-laundering-prevention",
    "governed-self-improvement-boundary",
    "proof-carrying-claims-and-ai-contracts",
    "costed-routing-residual-accounting-resource-discipline",
}
EXPECTED_DEEP_WORK = {
    "living-evidence-book-methodology",
    "governed-self-improvement-boundary",
    "proof-carrying-claims-and-ai-contracts",
}
MAX_DEEP_WORK = 3
MIN_TRACKS = 3
MAX_TRACKS = 5
REQUIRED_FRAGMENTS = (
    "Selected subordinate work tracks | 5",
    "Program-level defended contributions | 3",
    "Deep-work tracks this cycle | 3",
    "Deep-work cap | At most 3 tracks per v1.x cycle",
    "3 selected chapter lanes, 51 planned-only lanes",
    "all 54 chapter core claims remain `argument`",
    "three program-level defended contributions",
    "five subordinate work tracks",
    "products/contribution_focus_contract.json",
    "does not promote any chapter core claim above `argument`",
    "does not claim selected tracks are complete at A+ depth",
    "docs/v1_x_active_evidence_cycle.md",
    "docs/per_chapter_evidence_plan.md",
    "docs/non_core_evidence_ledger.md",
    "docs/defended_contribution_prior_art_positioning.md",
    "docs/theseus_report_import_slice.md",
    "docs/theseus_generation_mode_import_slice.md",
    "docs/theseus_support_replay_probe.md",
    "docs/circle_public_replay_consumer_gate.md",
    "docs/costed_route_resource_slice.md",
    "docs/resource_workflow_trace.md",
    "external_reviews/request_updates/consolidation_review_request_2026-06-29.json",
)


def fail(errors: list[str]) -> None:
    print("Defended contribution track validation failed:")
    for error in errors:
        print(f" - {error}")
    raise SystemExit(1)


def main() -> None:
    errors: list[str] = []
    if not DOC.exists():
        fail([f"Missing {DOC.relative_to(ROOT)}"])

    text = DOC.read_text(encoding="utf-8")
    active_cycle_text = ACTIVE_CYCLE.read_text(encoding="utf-8")
    scorecard_text = SCORECARD.read_text(encoding="utf-8")

    track_rows = re.findall(r"^\|\s*`([^`]+)`\s*\|[^|]*\|\s*([^|]+?)\s*\|", text, re.MULTILINE)
    track_ids = {track_id for track_id, _status in track_rows}
    deep_work = {track_id for track_id, status in track_rows if status.strip() == "deep-work"}

    if track_ids != EXPECTED_TRACKS:
        errors.append(f"Track set mismatch: {sorted(track_ids)}")
    if not (MIN_TRACKS <= len(track_ids) <= MAX_TRACKS):
        errors.append(f"Selected track count {len(track_ids)} is outside {MIN_TRACKS}-{MAX_TRACKS}.")
    if deep_work != EXPECTED_DEEP_WORK:
        errors.append(f"Deep-work track set mismatch: {sorted(deep_work)}")
    if len(deep_work) > MAX_DEEP_WORK:
        errors.append(f"Deep-work count {len(deep_work)} exceeds {MAX_DEEP_WORK}.")

    for fragment in REQUIRED_FRAGMENTS:
        if fragment not in text:
            errors.append(f"Missing required fragment: {fragment}")

    for title in [
        "Living evidence book methodology",
        "Claim support states and evidence laundering prevention",
        "Governed self-improvement boundary",
        "Proof-carrying claims and proof-carrying AI contracts",
        "Costed routing, residual accounting, and resource discipline",
    ]:
        if title not in scorecard_text:
            errors.append(f"Scorecard does not contain selected track title: {title}")
        if title not in text:
            errors.append(f"Selection record does not contain selected track title: {title}")

    for lane in [
        "resource-economics-and-token-budgets",
        "project-theseus-as-report-first-implementation-reference",
        "fast-generation-architectures",
    ]:
        if f"`{lane}`" not in active_cycle_text:
            errors.append(f"Active evidence cycle missing lane `{lane}`.")
        if f"`{lane}`" not in text:
            errors.append(f"Selection record missing lane `{lane}`.")

    for relative in [
        "docs/non_core_evidence_ledger.md",
        "docs/phase5_harness_runner.md",
        "docs/external_review_status.md",
        "docs/defended_contribution_prior_art_positioning.md",
        "docs/v1_0_release_gate_audit.md",
        "docs/theseus_report_import_slice.md",
        "docs/theseus_generation_mode_import_slice.md",
        "docs/theseus_support_replay_probe.md",
        "experiments/theseus_support_replay_probe/results/2026-07-01-local.json",
        "lean/AsiStackProofs/FastGenerationRefinement.lean",
        "docs/circle_public_replay_consumer_gate.md",
        "docs/costed_route_resource_slice.md",
        "docs/resource_workflow_trace.md",
        "experiments/resource_workflow_trace/results/2026-07-01-local.json",
        "docs/readiness_residual_harness.md",
    ]:
        if not (ROOT / relative).exists():
            errors.append(f"Referenced artifact does not exist: {relative}")
        if relative not in text:
            errors.append(f"Selection record does not reference {relative}.")

    if errors:
        fail(errors)

    print(
        "Defended contribution track validation passed: "
        f"{len(track_ids)} selected tracks, {len(deep_work)} deep-work tracks."
    )


if __name__ == "__main__":
    main()
