#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BOOK_STRUCTURE = ROOT / "book_structure.json"
TRANSITION_DIR = ROOT / "evidence_transitions"
DECISION_LEDGER = ROOT / "claim_decisions" / "v1_0_core_claim_no_promotion.json"
REPORT = ROOT / "docs" / "core_claim_transition_coverage.md"

REQUIRED_LEDGER_KEYS = {
    "decision_set_id",
    "date",
    "scope_boundary",
    "review_status",
    "reviewer_refs",
    "reviewer_independence",
    "source_refs",
    "global_promotion_burden",
    "decisions",
}

REQUIRED_DECISION_KEYS = {
    "claim_id",
    "chapter_id",
    "chapter_title",
    "decision",
    "current_support_state",
    "support_state_effect",
    "decision_reason",
    "required_evidence",
    "blockers",
    "non_claims",
    "refs",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def fail(errors: list[str]) -> None:
    print("Core claim decision validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def flatten_chapters(structure: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        chapter
        for part in structure.get("parts", [])
        for chapter in part.get("chapters", [])
        if isinstance(chapter, dict)
    ]


def nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def nonempty_string_list(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(nonempty_string(item) for item in value)


def accepted_core_transitions(core_claim_ids: set[str]) -> dict[str, dict[str, Any]]:
    accepted: dict[str, dict[str, Any]] = {}
    for path in sorted(TRANSITION_DIR.rglob("*.json")):
        data = load_json(path)
        if not isinstance(data, dict):
            continue
        claim_id = data.get("claim_id")
        if claim_id not in core_claim_ids:
            continue
        if data.get("review_status") != "accepted":
            continue
        if data.get("transition_validity_state") != "review_accepted":
            continue
        if claim_id in accepted:
            raise ValueError(f"duplicate accepted core transition for {claim_id}")
        accepted[str(claim_id)] = {
            "path": str(path.relative_to(ROOT)),
            "transition_effect": data.get("transition_effect"),
            "new_support_state": data.get("new_support_state"),
            "support_state_effect": data.get("support_state_effect"),
        }
    return accepted


def validate_ledger(
    ledger: Any,
    chapters_by_id: dict[str, dict[str, Any]],
    transition_claim_ids: set[str],
) -> tuple[dict[str, dict[str, Any]], list[str]]:
    errors: list[str] = []
    decisions: dict[str, dict[str, Any]] = {}

    if not isinstance(ledger, dict):
        return decisions, ["decision ledger must contain an object."]

    missing_keys = sorted(REQUIRED_LEDGER_KEYS - set(ledger))
    if missing_keys:
        errors.append(f"{DECISION_LEDGER.relative_to(ROOT)} missing keys: {missing_keys}")
    if ledger.get("decision_set_id") != "v1_0.core_claim_no_promotion":
        errors.append("decision_set_id must be v1_0.core_claim_no_promotion.")
    if ledger.get("review_status") != "accepted":
        errors.append("no-promotion decision set must have accepted review_status.")
    for key in ("scope_boundary", "reviewer_independence", "global_promotion_burden"):
        if not nonempty_string(ledger.get(key)):
            errors.append(f"{key} must be a non-empty string.")
    for key in ("reviewer_refs", "source_refs"):
        if not nonempty_string_list(ledger.get(key)):
            errors.append(f"{key} must be a non-empty string list.")

    rows = ledger.get("decisions")
    if not isinstance(rows, list):
        errors.append("decisions must be a list.")
        return decisions, errors

    seen: set[str] = set()
    for index, row in enumerate(rows):
        label = f"decisions[{index}]"
        if not isinstance(row, dict):
            errors.append(f"{label} must be an object.")
            continue
        missing_row_keys = sorted(REQUIRED_DECISION_KEYS - set(row))
        if missing_row_keys:
            errors.append(f"{label} missing keys: {missing_row_keys}")
        claim_id = row.get("claim_id")
        chapter_id = row.get("chapter_id")
        if not isinstance(claim_id, str):
            errors.append(f"{label}.claim_id must be a string.")
            continue
        if not isinstance(chapter_id, str):
            errors.append(f"{label}.chapter_id must be a string.")
            continue
        if claim_id in seen:
            errors.append(f"{label}: duplicate no-promotion decision for {claim_id}.")
        seen.add(claim_id)
        if claim_id in transition_claim_ids:
            errors.append(
                f"{label}: {claim_id} already has an accepted evidence-transition record; "
                "remove it from the no-promotion ledger or replace the transition."
            )
        chapter = chapters_by_id.get(chapter_id)
        if chapter is None:
            errors.append(f"{label}: unknown chapter_id {chapter_id!r}.")
            continue
        expected_claim_id = f"{chapter_id}.core"
        if claim_id != expected_claim_id:
            errors.append(f"{label}: claim_id must be {expected_claim_id!r}.")
        if row.get("chapter_title") != chapter.get("title"):
            errors.append(f"{label}: chapter_title does not match book_structure.json.")
        if chapter.get("evidence_level") != "argument":
            errors.append(
                f"{label}: no-promotion decisions currently require manifest evidence_level argument."
            )
        if row.get("decision") != "no_promotion":
            errors.append(f"{label}: decision must be no_promotion.")
        if row.get("current_support_state") != "argument":
            errors.append(f"{label}: current_support_state must be argument.")
        if row.get("support_state_effect") != "argument_only":
            errors.append(f"{label}: support_state_effect must be argument_only.")
        for key in ("decision_reason",):
            if not nonempty_string(row.get(key)):
                errors.append(f"{label}.{key} must be a non-empty string.")
        for key in ("required_evidence", "blockers", "non_claims", "refs"):
            if not nonempty_string_list(row.get(key)):
                errors.append(f"{label}.{key} must be a non-empty string list.")
        decisions[claim_id] = row

    return decisions, errors


def build_report(
    chapters: list[dict[str, Any]],
    transitions: dict[str, dict[str, Any]],
    decisions: dict[str, dict[str, Any]],
    missing: list[str],
) -> str:
    lines = [
        "# Core Claim Transition Coverage",
        "",
        "Last updated: 2026-06-29",
        "",
        "This report is generated by `python3 scripts/validate_core_claim_decisions.py --write-report`.",
        "It checks the v1.0 claim-state gate: every manifest chapter core claim must have either an accepted evidence-transition record or an accepted explicit no-promotion decision.",
        "",
        "## Summary",
        "",
        "| Metric | Count |",
        "|---|---:|",
        f"| Manifest chapter core claims | {len(chapters)} |",
        f"| Accepted core evidence-transition records | {len(transitions)} |",
        f"| Accepted explicit no-promotion decisions | {len(decisions)} |",
        f"| Missing core-claim coverage | {len(missing)} |",
        "",
        "All chapter core support states remain `argument`. The separate measured transition for `living-book-methodology.phase5_harness_registry_runner` is not a chapter core claim and is not counted in this coverage table.",
        "",
        "## Accepted Core Evidence-Transition Records",
        "",
        "| Claim ID | Effect | New support state | Record |",
        "|---|---|---|---|",
    ]
    for claim_id in sorted(transitions):
        record = transitions[claim_id]
        lines.append(
            f"| `{claim_id}` | `{record['transition_effect']}` | "
            f"`{record['new_support_state']}` | `{record['path']}` |"
        )
    lines.extend(
        [
            "",
            "## Explicit No-Promotion Decisions",
            "",
            "| Claim ID | Chapter | Decision | Primary blockers |",
            "|---|---|---|---|",
        ]
    )
    for claim_id in sorted(decisions):
        row = decisions[claim_id]
        blockers = "; ".join(row.get("blockers", []))
        lines.append(
            f"| `{claim_id}` | {row['chapter_title']} | `argument_only` | {blockers} |"
        )
    lines.extend(
        [
            "",
            "## Non-Claims",
            "",
            "- This report does not promote any chapter core claim above `argument`.",
            "- This report does not claim ASI capability, deployed safety, runtime behavior, benchmark performance, source-interpretation adequacy, or model-quality improvement.",
            "- This report does not replace future accepted evidence-transition records for narrowed claims.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    write_report = "--write-report" in sys.argv
    structure = load_json(BOOK_STRUCTURE)
    if not isinstance(structure, dict):
        fail(["book_structure.json must contain an object."])
    chapters = flatten_chapters(structure)
    chapters_by_id = {str(chapter.get("id")): chapter for chapter in chapters}
    core_claim_ids = {f"{chapter_id}.core" for chapter_id in chapters_by_id}

    errors: list[str] = []
    try:
        transitions = accepted_core_transitions(core_claim_ids)
    except ValueError as exc:
        transitions = {}
        errors.append(str(exc))

    ledger = load_json(DECISION_LEDGER)
    decisions, ledger_errors = validate_ledger(ledger, chapters_by_id, set(transitions))
    errors.extend(ledger_errors)

    covered = set(transitions) | set(decisions)
    missing = sorted(core_claim_ids - covered)
    unknown = sorted(set(decisions) - core_claim_ids)
    if missing:
        errors.append(f"Missing core-claim transition/no-promotion coverage: {missing}")
    if unknown:
        errors.append(f"No-promotion ledger names unknown core claims: {unknown}")

    expected_report = build_report(chapters, transitions, decisions, missing)
    if write_report:
        REPORT.write_text(expected_report, encoding="utf-8")
    elif REPORT.exists():
        current_report = REPORT.read_text(encoding="utf-8")
        if current_report != expected_report:
            errors.append(
                f"{REPORT.relative_to(ROOT)} is stale; run "
                "`python3 scripts/validate_core_claim_decisions.py --write-report`."
            )
    else:
        errors.append(
            f"{REPORT.relative_to(ROOT)} is missing; run "
            "`python3 scripts/validate_core_claim_decisions.py --write-report`."
        )

    if errors:
        fail(errors)

    print(
        "Core claim decision validation passed: "
        f"{len(chapters)} core claims, {len(transitions)} accepted transition record(s), "
        f"{len(decisions)} explicit no-promotion decision(s), {len(missing)} missing."
    )


if __name__ == "__main__":
    main()
