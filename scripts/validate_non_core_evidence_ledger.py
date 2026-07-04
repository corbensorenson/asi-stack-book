#!/usr/bin/env python3
"""Validate the public non-core evidence ledger.

The ledger is intentionally narrow: it makes accepted non-core transitions
visible without letting them read as chapter-core support-state promotions.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "non_core_evidence_ledger.md"
CLAIM_REVISION = ROOT / "claim_revisions" / "v1_x" / "manifest_core_claim_count_narrowing.json"
APPENDIX_C = ROOT / "appendices" / "C_claim_evidence_matrix.qmd"
README = ROOT / "README.md"
INDEX = ROOT / "index.qmd"

EXPECTED = {
    "living-book-methodology.phase5_harness_registry_runner": {
        "state": "synthetic-test-backed",
        "transition": "evidence_transitions/v1_0_measured/phase5_harness_runner_synthetic_test_backed.json",
    },
    "resource-economics.costed_route_budget_slice": {
        "state": "synthetic-test-backed",
        "transition": "evidence_transitions/v1_0_measured/costed_route_resource_slice_synthetic_test_backed.json",
    },
    "resource-economics.finite_burst_load_smoothing_selector": {
        "state": "synthetic-test-backed",
        "transition": "evidence_transitions/v1_x_measured/resource_load_stability_selector_synthetic_test_backed.json",
    },
    "resource-economics.scoped_workflow_trace_route_selector": {
        "state": "empirical-test-backed",
        "transition": "evidence_transitions/v1_x_measured/resource_workload_quality_selector_empirical_test_backed.json",
    },
    "circle-calculus.external_rope_receipt_replay": {
        "state": "prototype-backed",
        "transition": "evidence_transitions/v1_0_measured/circle_external_rope_receipt_prototype_backed.json",
    },
    "compact-generative-systems.compact_gvr_receipt_slice": {
        "state": "synthetic-test-backed",
        "transition": "evidence_transitions/v1_x_measured/compact_gvr_slice_synthetic_test_backed.json",
    },
}

NO_PROMOTION_DIR = ROOT / "evidence_transitions" / "v1_x_measured"

REQUIRED_LEDGER_STRINGS = [
    "All 44 remain at `argument`.",
    "Accepted non-core upward transitions | 6 narrow transitions.",
    "Accepted live claim-surface narrowing records | 1 count-surface correction; no support-state movement.",
    "claim_revisions/v1_x/manifest_core_claim_count_narrowing.json",
    "Accepted No-Promotion Side-Lane Decisions",
    "Chapter-core promotion effect | None.",
    "no independent external human review record yet.",
    "does not promote any chapter core claim above `argument`",
    "does not demote, deprecate, or refute any chapter core claim",
]

FORBIDDEN_LEDGER_STRINGS = [
    "chapter core claims are synthetic-test-backed",
    "chapter core claims are prototype-backed",
    "chapter core claims are external-literature-backed",
    "proves ASI",
    "guarantees safety",
    "proves alignment",
]


def fail(errors: list[str]) -> None:
    print("Non-core evidence ledger validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def load_transition(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail([f"missing transition record: {path.relative_to(ROOT)}"])
    if not isinstance(data, dict):
        fail([f"transition record must be an object: {path.relative_to(ROOT)}"])
    return data


def accepted_no_promotion_records(errors: list[str]) -> dict[str, dict[str, object]]:
    records: dict[str, dict[str, object]] = {}
    for path in sorted(NO_PROMOTION_DIR.glob("*.json")):
        record = load_transition(path)
        if (
            record.get("transition_effect") == "no_change"
            and record.get("support_state_effect") == "blocks_promotion"
        ):
            claim_id = record.get("claim_id")
            if not isinstance(claim_id, str) or not claim_id:
                errors.append(f"{path.relative_to(ROOT)} missing non-empty claim_id")
                continue
            relative = str(path.relative_to(ROOT))
            if claim_id in records:
                errors.append(f"duplicate no-promotion claim_id {claim_id!r}")
            records[claim_id] = {"transition": relative, "record": record}
    if not records:
        errors.append("no accepted blocks_promotion records found under evidence_transitions/v1_x_measured")
    return records


def main() -> None:
    errors: list[str] = []
    ledger = LEDGER.read_text(encoding="utf-8", errors="ignore")
    appendix_c = APPENDIX_C.read_text(encoding="utf-8", errors="ignore")
    readme = README.read_text(encoding="utf-8", errors="ignore")
    index = INDEX.read_text(encoding="utf-8", errors="ignore")
    no_promotion_expected = accepted_no_promotion_records(errors)

    dynamic_required_ledger_strings = [
        (
            "Accepted no-promotion side-lane decisions | "
            f"{len(no_promotion_expected)} accepted `blocks_promotion` decisions; "
            "no support-state movement."
        )
    ]

    for required in REQUIRED_LEDGER_STRINGS + dynamic_required_ledger_strings:
        if required not in ledger:
            errors.append(f"ledger missing required boundary text: {required}")
    for forbidden in FORBIDDEN_LEDGER_STRINGS:
        if forbidden in ledger:
            errors.append(f"ledger contains forbidden overclaim: {forbidden}")

    revision = load_transition(CLAIM_REVISION)
    revision_record = revision.get("claim_ledger_record") if isinstance(revision, dict) else None
    if not isinstance(revision_record, dict):
        errors.append(f"{CLAIM_REVISION.relative_to(ROOT)} missing claim_ledger_record")
    else:
        if revision_record.get("claim_id") != "non-core-evidence-ledger.chapter-core-count-surface":
            errors.append(f"{CLAIM_REVISION.relative_to(ROOT)} has unexpected claim_id")
        if revision_record.get("support_state_before") != revision_record.get("support_state_after"):
            errors.append(f"{CLAIM_REVISION.relative_to(ROOT)} must not move support state")
        if revision_record.get("accepted_evidence_transition_refs"):
            errors.append(f"{CLAIM_REVISION.relative_to(ROOT)} must not cite accepted transitions")

    for claim_id, expected in EXPECTED.items():
        record_path = ROOT / expected["transition"]
        record = load_transition(record_path)
        if record.get("claim_id") != claim_id:
            errors.append(
                f"{record_path.relative_to(ROOT)} claim_id {record.get('claim_id')!r} "
                f"does not match {claim_id!r}"
            )
        if record.get("new_support_state") != expected["state"]:
            errors.append(
                f"{record_path.relative_to(ROOT)} support state "
                f"{record.get('new_support_state')!r} does not match {expected['state']!r}"
            )
        if record.get("transition_validity_state") != "review_accepted":
            errors.append(f"{record_path.relative_to(ROOT)} is not review_accepted")
        non_claims = " ".join(str(item) for item in record.get("non_claims", []))
        limitations = " ".join(str(item) for item in record.get("limitations", []))
        if "does not promote any chapter core claim" not in f"{non_claims} {limitations}":
            errors.append(f"{record_path.relative_to(ROOT)} lacks chapter-core non-claim text")

        if claim_id not in ledger:
            errors.append(f"ledger does not list claim id {claim_id}")
        if expected["state"] not in ledger:
            errors.append(f"ledger does not list support state {expected['state']}")
        if expected["transition"] not in ledger:
            errors.append(f"ledger does not link transition record {expected['transition']}")

    for claim_id, expected in no_promotion_expected.items():
        transition = str(expected["transition"])
        record_path = ROOT / transition
        record = expected["record"]
        if not isinstance(record, dict):
            errors.append(f"{transition} did not load as a transition record")
            continue
        if record.get("claim_id") != claim_id:
            errors.append(
                f"{record_path.relative_to(ROOT)} claim_id {record.get('claim_id')!r} "
                f"does not match {claim_id!r}"
            )
        if record.get("old_support_state") != "argument" or record.get("new_support_state") != "argument":
            errors.append(f"{record_path.relative_to(ROOT)} must keep support state at argument")
        if record.get("transition_effect") != "no_change":
            errors.append(f"{record_path.relative_to(ROOT)} must be a no_change transition")
        if record.get("transition_validity_state") != "review_accepted":
            errors.append(f"{record_path.relative_to(ROOT)} is not review_accepted")
        if record.get("review_status") != "accepted":
            errors.append(f"{record_path.relative_to(ROOT)} review_status is not accepted")
        if record.get("support_state_effect") != "blocks_promotion":
            errors.append(f"{record_path.relative_to(ROOT)} must block promotion")
        boundary_text = " ".join(
            str(item)
            for item in (
                list(record.get("non_claims", []))
                + list(record.get("limitations", []))
                + [
                    record.get("scope_boundary", ""),
                    record.get("transition_reason", ""),
                    record.get("promotion_burden", ""),
                ]
            )
        ).lower()
        if "does not create an upward support-state transition" not in boundary_text:
            errors.append(
                f"{record_path.relative_to(ROOT)} lacks upward support-state transition boundary text"
            )
        if (
            "chapter core" not in boundary_text
            and "chapter-core" not in boundary_text
            and "above argument" not in boundary_text
        ):
            errors.append(f"{record_path.relative_to(ROOT)} lacks chapter-core or above-argument boundary text")
        if claim_id not in ledger:
            errors.append(f"ledger does not list no-promotion claim id {claim_id}")
        if transition not in ledger:
            errors.append(f"ledger does not link no-promotion transition record {transition}")
        if "blocks_promotion" not in ledger:
            errors.append("ledger does not expose blocks_promotion for side-lane no-promotion decisions")

    ledger_refs = [
        ("README.md", readme, "docs/non_core_evidence_ledger.md"),
        ("index.qmd", index, "docs/non_core_evidence_ledger.md"),
        ("appendices/C_claim_evidence_matrix.qmd", appendix_c, "docs/non_core_evidence_ledger.md"),
    ]
    for name, text, ref in ledger_refs:
        if ref not in text:
            errors.append(f"{name} does not reference {ref}")

    surface_counts = [
        ("README.md", readme, "six narrow non-core transitions are accepted"),
        ("index.qmd", index, "Six narrow non-core evidence transitions accepted"),
        ("index.qmd", index, "Six narrow non-core transitions are accepted"),
    ]
    for name, text, required in surface_counts:
        if required.lower() not in text.lower():
            errors.append(f"{name} does not expose the current six-transition count: {required}")

    if errors:
        fail(errors)

    print(
        "Non-core evidence ledger validation passed: 6 accepted non-core upward transitions, "
        f"{len(no_promotion_expected)} accepted side-lane no-promotion decisions, "
        "0 chapter-core promotions."
    )


if __name__ == "__main__":
    main()
