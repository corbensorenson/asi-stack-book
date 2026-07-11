#!/usr/bin/env python3
"""Validate the active post-v2.1 roadmap, status sidecar, and residual ownership."""

from __future__ import annotations

import copy
from collections import Counter
from pathlib import Path

from build_canonical_public_status import ROOT, load_json, validate_against_schema


ROADMAP = ROOT / "docs/post_v2_1_residual_and_transfer_roadmap.md"
STATUS = ROOT / "roadmap_records/post_v2_1_residual_and_transfer_status.json"
SCHEMA = ROOT / "schemas/post_v2_1_residual_transfer_status.schema.json"
RESIDUALS = ROOT / "docs/post_v2_residual_ledger.md"
STRUCTURE = ROOT / "book_structure.json"
VECTORS = ROOT / "evidence_quality/core_claim_vectors.json"
README = ROOT / "README.md"
PREDECESSOR = ROOT / "docs/post_v2_evidence_roadmap.md"
COMPLETION = ROOT / "docs/v2_1_completion_declaration.md"

EXPECTED_PRIORITY_RESIDUALS = {
    "P0": [],
    "P1": ["GW-01", "GW-02", "GW-03"],
    "P2": ["RD-01", "RD-02", "RD-03", "RD-04"],
    "P3": ["UU-01", "UU-02", "UU-03", "UU-04"],
}
EXPECTED_RESIDUAL_KEYWORDS = {
    "GW-01": "sabotaged rollback cases",
    "GW-02": "zero useful releases",
    "GW-03": "Observer separation",
    "RD-01": "were indistinguishable",
    "RD-02": "Fallback and abstention activated zero times",
    "RD-03": "deterministic task recomputation",
    "RD-04": "15 initially correct answers",
    "UU-01": "reduced retained-base accuracy",
    "UU-02": "62 test decisions",
    "UU-03": "did not prove influence or storage erasure",
    "UU-04": "not optimizer state, caches, backups",
}
EXPECTED_CONDITIONAL = ["COND-01", "COND-02", "COND-03"]
ROADMAP_SECTIONS = (
    "## Truth-source hierarchy and change control",
    "## P0 — Public truth reconciliation",
    "## P1 — Governed usefulness and effect-complete rollback",
    "## P2 — Ambiguous routing and real-model deliberation",
    "## P3 — Full-state update and unlearning causality",
    "### Statistical and decision discipline",
    "### Reproducibility and numeric portability",
    "### Security, privacy, and data governance",
    "### Global resource and retention budgets",
    "## Risk register",
    "## Definition of done",
)


def current_baseline() -> dict[str, int | str]:
    structure = load_json(STRUCTURE)
    chapters = [chapter for part in structure["parts"] for chapter in part["chapters"]]
    vectors = load_json(VECTORS)["vectors"]
    reproduction = Counter(row["dimensions"]["reproducibility"]["state"] for row in vectors)
    support = Counter(row["summary_support_state"] for row in vectors)
    return {
        "latest_immutable_release": "v2.1.0",
        "active_chapter_count": len(chapters),
        "core_claim_count": len(vectors),
        "core_argument_count": support["argument"],
        "adjacent_local_replay_count": reproduction["adjacent_local_replay"],
        "no_claim_specific_replay_count": reproduction["not_demonstrated_for_claim"],
        "actionable_residual_count": len(EXPECTED_RESIDUAL_KEYWORDS),
        "conditional_residual_count": len(EXPECTED_CONDITIONAL),
        "priority_count": len(EXPECTED_PRIORITY_RESIDUALS),
        "active_empirical_program_count": 3,
    }


def semantic_errors(
    status: dict,
    roadmap: str,
    residuals: str,
    readme: str,
    predecessor: str,
    completion: str,
) -> list[str]:
    errors: list[str] = []
    if status.get("baseline") != current_baseline():
        errors.append("machine roadmap baseline differs from current project evidence")

    priorities = status.get("priorities", [])
    if [row.get("id") for row in priorities] != ["P0", "P1", "P2", "P3"]:
        errors.append("priority order must be exactly P0, P1, P2, P3")
    by_priority = {row.get("id"): row for row in priorities}
    for priority_id, expected in EXPECTED_PRIORITY_RESIDUALS.items():
        row = by_priority.get(priority_id, {})
        if row.get("residual_ids") != expected:
            errors.append(f"{priority_id}: residual ownership differs from the canonical mapping")
        expected_kind = "publication_gate" if priority_id == "P0" else "empirical_program"
        if row.get("kind") != expected_kind:
            errors.append(f"{priority_id}: priority kind is wrong")
        if row.get("state") != "pending" and not row.get("evidence_refs"):
            errors.append(f"{priority_id}: non-pending state lacks evidence references")

    residual_rows = status.get("residuals", [])
    residual_ids = [row.get("id") for row in residual_rows]
    if len(residual_ids) != len(set(residual_ids)) or set(residual_ids) != set(EXPECTED_RESIDUAL_KEYWORDS):
        errors.append("actionable residual IDs must be unique and complete")
    expected_owner = {
        residual_id: priority
        for priority, residual_ids_for_priority in EXPECTED_PRIORITY_RESIDUALS.items()
        for residual_id in residual_ids_for_priority
    }
    for row in residual_rows:
        if row.get("priority") != expected_owner.get(row.get("id")):
            errors.append(f"{row.get('id')}: residual priority owner is wrong")
        if row.get("state") != "actionable_open" and not row.get("evidence_refs"):
            errors.append(f"{row.get('id')}: changed residual state lacks evidence")
    residual_state = {row.get("id"): row.get("state") for row in residual_rows}
    for priority_id in ("P1", "P2", "P3"):
        priority = by_priority.get(priority_id, {})
        if priority.get("state") == "completed" and any(
            residual_state.get(residual_id) == "actionable_open"
            for residual_id in EXPECTED_PRIORITY_RESIDUALS[priority_id]
        ):
            errors.append(f"{priority_id}: completed while owned residuals remain actionable_open")

    conditional = status.get("conditional_lanes", [])
    if [row.get("id") for row in conditional] != EXPECTED_CONDITIONAL:
        errors.append("conditional residual IDs or order differ")
    if any(row.get("state") != "activation_absent" for row in conditional):
        errors.append("conditional lanes cannot activate without a registered activation record")

    milestones = status.get("milestones", [])
    if [row.get("id") for row in milestones] != ["M0", "M1", "M2", "M3", "M4", "M5"]:
        errors.append("milestone order must be exactly M0 through M5")
    for row in milestones:
        if row.get("state") != "pending" and not row.get("evidence_refs"):
            errors.append(f"{row.get('id')}: non-pending milestone lacks evidence references")
    if milestones and milestones[0].get("state") != "completed":
        errors.append("M0 must record the installed machine authority and validator")

    for heading in ROADMAP_SECTIONS:
        if roadmap.count(heading) != 1:
            errors.append(f"roadmap must contain exactly one required section: {heading}")
    for phrase in (
        "unfinished work only",
        "eleven actionable v2.1 residuals",
        "External humans are not required",
        "do not choose the next version number before results",
        "roadmap_records/post_v2_1_residual_and_transfer_status.json",
        "No chapter-core support state moves automatically",
        "The v2.1 cross-CPU reduction failure is a permanent regression case",
    ):
        if phrase not in roadmap:
            errors.append(f"roadmap missing governing boundary: {phrase}")

    for residual_id, keyword in EXPECTED_RESIDUAL_KEYWORDS.items():
        if residuals.count(f"`{residual_id}`") != 1 or keyword not in residuals:
            errors.append(f"residual ledger missing stable identity or fact: {residual_id}")
        if f"`{residual_id}`" not in roadmap:
            errors.append(f"active roadmap does not own residual: {residual_id}")
    for residual_id in EXPECTED_CONDITIONAL:
        if residuals.count(f"`{residual_id}`") != 1 or f"`{residual_id}`" not in roadmap:
            errors.append(f"conditional residual identity is missing: {residual_id}")

    path = "docs/post_v2_1_residual_and_transfer_roadmap.md"
    if path not in readme or "Current work is governed by" not in readme:
        errors.append("README does not identify the active successor roadmap")
    if f"Active successor: `{path}`" not in predecessor:
        errors.append("completed predecessor does not identify the active successor")
    if path not in completion or "active successor" not in completion.lower():
        errors.append("v2.1 completion declaration does not identify the successor")
    if "Status: completed 2026-07-10" not in predecessor:
        errors.append("predecessor roadmap is not preserved as completed")
    if status.get("support_state_effect") != "none":
        errors.append("roadmap activation cannot change a support state")
    return errors


def negative_control_errors(
    status: dict,
    roadmap: str,
    residuals: str,
    readme: str,
    predecessor: str,
    completion: str,
) -> list[str]:
    failures: list[str] = []
    mutations: list[tuple[str, dict, str, str, str, str, str]] = []

    bad_count = copy.deepcopy(status)
    bad_count["baseline"]["actionable_residual_count"] = 10
    mutations.append(("residual count drift", bad_count, roadmap, residuals, readme, predecessor, completion))

    duplicate = copy.deepcopy(status)
    duplicate["residuals"][1]["id"] = duplicate["residuals"][0]["id"]
    mutations.append(("duplicate residual identity", duplicate, roadmap, residuals, readme, predecessor, completion))

    wrong_owner = copy.deepcopy(status)
    wrong_owner["residuals"][0]["priority"] = "P2"
    mutations.append(("wrong residual owner", wrong_owner, roadmap, residuals, readme, predecessor, completion))

    false_complete = copy.deepcopy(status)
    false_complete["priorities"][1]["state"] = "completed"
    mutations.append(("completion without evidence", false_complete, roadmap, residuals, readme, predecessor, completion))

    missing_conditional = copy.deepcopy(status)
    missing_conditional["conditional_lanes"] = missing_conditional["conditional_lanes"][:-1]
    mutations.append(("conditional erasure", missing_conditional, roadmap, residuals, readme, predecessor, completion))

    stale_pointer = readme.replace("Current work is governed by", "Historical work was once governed by")
    mutations.append(("stale active pointer", status, roadmap, residuals, stale_pointer, predecessor, completion))

    for label, mutation, roadmap_text, residual_text, readme_text, predecessor_text, completion_text in mutations:
        if not semantic_errors(
            mutation,
            roadmap_text,
            residual_text,
            readme_text,
            predecessor_text,
            completion_text,
        ):
            failures.append(f"negative control was accepted: {label}")
    return failures


def main() -> None:
    required = (ROADMAP, STATUS, SCHEMA, RESIDUALS, STRUCTURE, VECTORS, README, PREDECESSOR, COMPLETION)
    missing = [path.relative_to(ROOT).as_posix() for path in required if not path.is_file()]
    if missing:
        raise SystemExit("missing post-v2.1 roadmap artifacts: " + ", ".join(missing))

    status = load_json(STATUS)
    roadmap = ROADMAP.read_text(encoding="utf-8")
    residuals = RESIDUALS.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")
    predecessor = PREDECESSOR.read_text(encoding="utf-8")
    completion = COMPLETION.read_text(encoding="utf-8")
    errors = validate_against_schema(status, load_json(SCHEMA), STATUS.relative_to(ROOT).as_posix())
    errors.extend(semantic_errors(status, roadmap, residuals, readme, predecessor, completion))
    errors.extend(negative_control_errors(status, roadmap, residuals, readme, predecessor, completion))
    if errors:
        raise SystemExit("Post-v2.1 roadmap validation failed:\n - " + "\n - ".join(errors))
    print(
        "Post-v2.1 roadmap validation passed: one active successor, 4 priorities, "
        "3 empirical programs, 11 uniquely owned actionable residuals, 3 activation-absent "
        "conditional lanes, current 54-claim evidence baseline, M0 machine authority, "
        "and 6 rejecting mutations."
    )


if __name__ == "__main__":
    main()
