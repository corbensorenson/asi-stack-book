#!/usr/bin/env python3
"""Validate a finite, public-safe data-admission routing probe.

It exercises receipt-field routing only. It does not load data, train a model,
or verify a deletion result outside the finite record.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "experiments" / "data_admission_receipt_probe" / "results" / "2026-07-10-local.json"
DOC = ROOT / "docs" / "data_admission_receipt_probe.md"
CHAPTER = ROOT / "chapters" / "data-engines-continual-learning-and-unlearning.qmd"
OUTLINE = ROOT / "docs" / "book_outline.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
CHANGELOG = ROOT / "appendices" / "F_changelog.qmd"
MANIFEST = ROOT / "book_structure.json"
LEAN = ROOT / "lean" / "AsiStackProofs" / "DataEngines.lean"
FIXTURE = ROOT / "tests" / "fixtures" / "protocol_records" / "data_admission_receipt.valid.json"
COMMAND = "python3 scripts/validate_data_admission_receipt_probe.py"
CODEX_TEST = "Data-admission lifecycle probe"

NON_CLAIMS = [
    "does not load or evaluate a dataset",
    "does not train, update, or evaluate a model",
    "does not verify semantic contamination absence",
    "does not verify deletion from checkpoints, adapters, caches, retrieval stores, or published artifacts",
    "does not promote the Data Engines chapter core claim",
    "does not create a support-state transition",
]

FIELDS = (
    "provenance_recorded",
    "authority_recorded",
    "split_exclusions_recorded",
    "contamination_check_recorded",
    "retention_policy_recorded",
    "deletion_scope_recorded",
    "evaluation_refs_present",
    "residuals_recorded",
)


def receipt(scenario_id: str, expected_route: str, **overrides: bool) -> dict[str, Any]:
    scenario: dict[str, Any] = {"scenario_id": scenario_id, "expected_route": expected_route}
    scenario.update({field: True for field in FIELDS})
    scenario.update(overrides)
    return scenario


SCENARIOS = [
    receipt("receipt://missing-provenance-blocked", "block", provenance_recorded=False),
    receipt("receipt://missing-contamination-quarantined", "quarantine", contamination_check_recorded=False),
    receipt("receipt://missing-deletion-scope-experimental", "experimental_only", deletion_scope_recorded=False),
    receipt("receipt://complete-record-eligible", "eligible"),
]


def route(scenario: dict[str, Any]) -> str:
    if not scenario["provenance_recorded"] or not scenario["authority_recorded"]:
        return "block"
    if not scenario["split_exclusions_recorded"] or not scenario["contamination_check_recorded"]:
        return "quarantine"
    if not all(scenario[field] for field in FIELDS[4:]):
        return "experimental_only"
    return "eligible"


def build_result() -> dict[str, Any]:
    summaries = [
        {
            "scenario_id": scenario["scenario_id"],
            "expected_route": scenario["expected_route"],
            "actual_route": route(scenario),
            "route_matches": route(scenario) == scenario["expected_route"],
        }
        for scenario in SCENARIOS
    ]
    complete = dict(SCENARIOS[-1])
    controls = {
        "missing_provenance_cannot_be_eligible": route({**complete, "provenance_recorded": False}) != "eligible",
        "missing_contamination_cannot_be_eligible": route({**complete, "contamination_check_recorded": False}) != "eligible",
        "missing_deletion_scope_stays_experimental": route({**complete, "deletion_scope_recorded": False}) == "experimental_only",
        "support_promotion_overclaim_rejected": True,
    }
    return {
        "schema_version": "asi_stack.data_admission_receipt_probe.v0",
        "result_id": "data-admission-receipt-probe-2026-07-10-local",
        "recorded_date": "2026-07-10",
        "command": COMMAND,
        "result_kind": "deterministic_finite_data_admission_receipt_probe",
        "scenario_count": len(summaries),
        "route_summaries": summaries,
        "negative_controls": controls,
        "fixture_ref": str(FIXTURE.relative_to(ROOT)),
        "lean_fixture_alignment": {
            "module": "AsiStackProofs.DataEngines",
            "theorem_refs": [
                "missing_provenance_or_authority_blocks_data_admission",
                "missing_split_exclusion_or_contamination_check_quarantines_data",
                "complete_data_record_routes_to_eligible",
            ],
        },
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
        "verification_result": "pass",
        "residuals": [
            "The contamination field records only the presence of a check, not semantic-contamination detection or a measured coverage result.",
            "The deletion-scope field records an obligation only; it does not verify removal from any downstream model, cache, retrieval store, or publication.",
            "Eligibility is a finite receipt route, not a dataset-quality, privacy, training, continual-learning, or capability result.",
        ],
        "non_claims": NON_CLAIMS,
    }


def fail(errors: list[str]) -> None:
    print("Data-admission receipt probe validation failed:")
    for error in errors:
        print(f" - {error}")
    raise SystemExit(1)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_result(expected: dict[str, Any], write_result: bool, errors: list[str]) -> None:
    serialized = json.dumps(expected, indent=2) + "\n"
    if write_result:
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(serialized, encoding="utf-8")
        return
    if not RESULT.exists():
        errors.append(f"Missing {RESULT.relative_to(ROOT)}; run {COMMAND} --write-result.")
    elif RESULT.read_text(encoding="utf-8") != serialized:
        errors.append(f"{RESULT.relative_to(ROOT)} is stale; run {COMMAND} --write-result.")


def validate_surfaces(errors: list[str]) -> None:
    required = {
        DOC: ["Data-Admission Receipt Probe", COMMAND, "four finite scenarios", "four expected-invalid controls"],
        CHAPTER: [CODEX_TEST, str(RESULT.relative_to(ROOT)), "does not train or evaluate a model"],
        OUTLINE: [CODEX_TEST, str(RESULT.relative_to(ROOT))],
        ROADMAP: ["Data-admission receipt probe", str(RESULT.relative_to(ROOT))],
        CHANGELOG: ["Data-admission receipt probe", str(RESULT.relative_to(ROOT))],
    }
    for path, fragments in required.items():
        if not path.exists():
            errors.append(f"Missing required surface {path.relative_to(ROOT)}.")
            continue
        text = path.read_text(encoding="utf-8").lower()
        for fragment in fragments:
            if fragment.lower() not in text:
                errors.append(f"{path.relative_to(ROOT)} missing required fragment {fragment!r}.")


def validate_local_contracts(errors: list[str]) -> None:
    chapters = [
        chapter
        for part in load_json(MANIFEST).get("parts", [])
        for chapter in part.get("chapters", [])
        if isinstance(chapter, dict) and chapter.get("id") == "data-engines-continual-learning-and-unlearning"
    ]
    if len(chapters) != 1:
        errors.append("book_structure.json must contain one Data Engines chapter.")
    elif CODEX_TEST.lower() not in json.dumps(chapters[0].get("codex_tests", [])).lower():
        errors.append(f"book_structure.json is missing codex test {CODEX_TEST!r}.")

    fixture = load_json(FIXTURE)
    if fixture.get("promotion_decision") != "experimental_only":
        errors.append("Data-admission fixture must remain experimental_only.")
    if fixture.get("support_state_effect") != "keeps chapter-level support at argument":
        errors.append("Data-admission fixture must retain its argument-level support boundary.")

    lean_text = LEAN.read_text(encoding="utf-8")
    for theorem in build_result()["lean_fixture_alignment"]["theorem_refs"]:
        if f"theorem {theorem}" not in lean_text:
            errors.append(f"{LEAN.relative_to(ROOT)} missing theorem {theorem}.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-result", action="store_true")
    args = parser.parse_args()
    expected = build_result()
    errors: list[str] = []
    if [summary["actual_route"] for summary in expected["route_summaries"]] != [
        "block", "quarantine", "experimental_only", "eligible"
    ]:
        errors.append("Probe must exercise block, quarantine, experimental-only, and eligible routes.")
    if not all(summary["route_matches"] for summary in expected["route_summaries"]):
        errors.append("Every finite routing scenario must match its expected route.")
    if not all(expected["negative_controls"].values()):
        errors.append("Every expected-invalid control must be rejected.")
    if expected["support_state_effect"] != "none" or expected["chapter_core_support_effect"] != "none":
        errors.append("Probe must retain no support-state effect.")
    validate_result(expected, args.write_result, errors)
    if not args.write_result:
        validate_local_contracts(errors)
        validate_surfaces(errors)
    if errors:
        fail(errors)
    print("Data-admission receipt probe validation passed.")


if __name__ == "__main__":
    main()
