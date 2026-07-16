#!/usr/bin/env python3
"""Validate the compact GVR status ledger used by the v1.0 status snapshot."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "compact_gvr_status_ledger.md"
SUMMARY = ROOT / "docs" / "compact_gvr_slice.md"
INPUT = ROOT / "experiments" / "compact_gvr_slice" / "input" / "v1_x_compact_gvr_records.json"
RESULT = ROOT / "experiments" / "compact_gvr_slice" / "results" / "2026-07-01-local.json"
TRANSITION = ROOT / "evidence_transitions" / "v1_x_measured" / "compact_gvr_slice_synthetic_test_backed.json"
LEAN_FIXTURE = ROOT / "lean" / "AsiStackProofs" / "CompactGenerationRefinement.lean"
VALIDATOR = ROOT / "scripts" / "validate_compact_gvr_slice.py"

EXPECTED_SELECTED = "receipt://repeat-generator-plus-repair"
EXPECTED_BASELINE = "receipt://literal-baseline"
EXPECTED_REJECTED = {
    "receipt://bounded-search-overrun",
    "receipt://lossy-summary-marked-exact",
    "receipt://negative-rate-no-fallback",
}
REQUIRED_THEOREMS = (
    "lossy_exactness_is_blocked_before_verification",
    "reconstruction_mismatch_activates_preserved_source_fallback",
    "reconstruction_mismatch_without_executable_fallback_is_blocked",
    "fallback_lifecycle_reaches_closed_without_support_or_effect_authority",
)
REQUIRED_BOUNDARIES = (
    "does not promote any chapter core claim",
    "does not prove compression utility",
    "does not prove deployed generator",
)


def fail(errors: list[str]) -> None:
    print("Compact GVR status ledger validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def as_list(value: Any, label: str, errors: list[str]) -> list[Any]:
    if isinstance(value, list):
        return value
    errors.append(f"{label} must contain a list; found {type(value).__name__}.")
    return []


def qmd_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def collect() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    for path in (SUMMARY, INPUT, RESULT, TRANSITION, LEAN_FIXTURE, VALIDATOR):
        if not path.exists():
            errors.append(f"required path missing: {rel(path)}")
    if errors:
        return {}, errors

    result = load_json(RESULT)
    transition = load_json(TRANSITION)
    if not isinstance(result, dict):
        errors.append(f"{rel(RESULT)} must contain a JSON object.")
        result = {}
    if not isinstance(transition, dict):
        errors.append(f"{rel(TRANSITION)} must contain a JSON object.")
        transition = {}

    rejected_receipts = as_list(result.get("rejected_receipts", []), f"{rel(RESULT)} rejected_receipts", errors)
    rejected = {
        str(row.get("receipt_id"))
        for row in rejected_receipts
        if isinstance(row, dict)
    }
    case_results = as_list(result.get("case_results", []), f"{rel(RESULT)} case_results", errors)
    case_count = len(case_results)
    selected = str(result.get("selected_receipt", ""))
    baseline = str(result.get("baseline_receipt", ""))
    selected_bytes = result.get("selected_bytes")
    baseline_bytes = result.get("baseline_bytes")
    byte_reduction = result.get("byte_reduction_vs_literal_percent")

    expected_result_values = {
        "verification_result": "pass",
        "support_state_effect": "eligible_for_bounded_evidence_review",
        "target_bytes": 368,
        "baseline_receipt": EXPECTED_BASELINE,
        "baseline_bytes": 368,
        "selected_receipt": EXPECTED_SELECTED,
        "selected_bytes": 78,
        "byte_reduction_vs_literal_percent": 78.8,
    }
    for key, expected in expected_result_values.items():
        if result.get(key) != expected:
            errors.append(f"{rel(RESULT)} {key} must be {expected!r}; found {result.get(key)!r}.")
    if case_count != 5:
        errors.append(f"{rel(RESULT)} must contain 5 case_results; found {case_count}.")
    if rejected != EXPECTED_REJECTED:
        errors.append(f"{rel(RESULT)} rejected receipts must be {sorted(EXPECTED_REJECTED)}; found {sorted(rejected)}.")

    expected_transition_values = {
        "claim_id": "compact-generative-systems.compact_gvr_receipt_slice",
        "old_support_state": "argument",
        "new_support_state": "synthetic-test-backed",
        "transition_effect": "upward",
        "transition_validity_state": "review_accepted",
        "verification_result": "pass",
        "support_state_effect": "eligible_for_bounded_evidence_review",
        "review_status": "accepted",
    }
    for key, expected in expected_transition_values.items():
        if transition.get(key) != expected:
            errors.append(f"{rel(TRANSITION)} {key} must be {expected!r}; found {transition.get(key)!r}.")

    artifact_refs = as_list(transition.get("artifact_refs", []), f"{rel(TRANSITION)} artifact_refs", errors)
    transition_refs = set(str(ref) for ref in artifact_refs if isinstance(ref, str))
    for required_ref in (rel(INPUT), rel(RESULT), rel(VALIDATOR), rel(LEAN_FIXTURE), rel(SUMMARY)):
        if required_ref not in transition_refs:
            errors.append(f"{rel(TRANSITION)} artifact_refs missing {required_ref}.")

    result_non_claims = as_list(result.get("non_claims", []), f"{rel(RESULT)} non_claims", errors)
    transition_non_claims = as_list(transition.get("non_claims", []), f"{rel(TRANSITION)} non_claims", errors)
    non_claim_text = " ".join(str(item) for item in [*result_non_claims, *transition_non_claims]).lower()
    for phrase in REQUIRED_BOUNDARIES:
        if phrase not in non_claim_text:
            errors.append(f"Compact GVR non-claim boundary missing {phrase!r}.")

    lean_text = LEAN_FIXTURE.read_text(encoding="utf-8")
    for theorem in REQUIRED_THEOREMS:
        if theorem not in lean_text:
            errors.append(f"{rel(LEAN_FIXTURE)} missing theorem/fixture name {theorem}.")

    summary_text = SUMMARY.read_text(encoding="utf-8")
    for fragment in (
        "Compact GVR Synthetic Slice",
        "Support transition: `argument` to `synthetic-test-backed`",
        "`receipt://repeat-generator-plus-repair` | selected compact receipt | 78 | eligible",
        "`receipt://literal-baseline` | literal baseline | 368 | baseline",
        "78.8 percent smaller",
        "Does not promote any chapter core claim above `argument`",
    ):
        if fragment not in summary_text:
            errors.append(f"{rel(SUMMARY)} missing required fragment: {fragment}")

    metrics = {
        "case_count": case_count,
        "selected": selected,
        "baseline": baseline,
        "selected_bytes": selected_bytes,
        "baseline_bytes": baseline_bytes,
        "byte_reduction": byte_reduction,
        "rejected_count": len(rejected),
        "rejected": sorted(rejected),
        "claim_id": transition.get("claim_id"),
        "old_support_state": transition.get("old_support_state"),
        "new_support_state": transition.get("new_support_state"),
        "transition_effect": transition.get("transition_effect"),
        "transition_validity_state": transition.get("transition_validity_state"),
        "lean_theorem_count": len(REQUIRED_THEOREMS),
        "result": rel(RESULT),
        "transition": rel(TRANSITION),
        "summary": rel(SUMMARY),
        "input": rel(INPUT),
        "lean": rel(LEAN_FIXTURE),
        "validator": rel(VALIDATOR),
    }
    return metrics, errors


def build_report(metrics: dict[str, Any], errors: list[str]) -> str:
    validation_lines = ["- None."] if not errors else [f"- {qmd_escape(error)}" for error in errors]
    rejected = ", ".join(f"`{item}`" for item in metrics["rejected"])
    return "\n".join(
        [
            "# Compact GVR Status Ledger",
            "",
            "Generated by `python3 scripts/validate_compact_gvr_status_ledger.py --write`.",
            "",
            "This ledger keeps the public v1.0 status snapshot readable by moving the Compact GVR synthetic-slice detail out of the status row. It summarizes the current bounded compact-generation receipt result, accepted narrow transition, Lean fixture alignment, residuals, and non-claim boundaries.",
            "",
            "It does **not** create a new compact-generation result, promote a chapter core claim, prove a deployed codec, prove model quality, prove benchmark performance, or prove semantic utility.",
            "",
            "## Summary",
            "",
            "| Metric | Value |",
            "|---|---:|",
            f"| Receipt records checked | {metrics['case_count']} |",
            f"| Literal baseline bytes | {metrics['baseline_bytes']} |",
            f"| Selected receipt bytes | {metrics['selected_bytes']} |",
            f"| Byte reduction versus literal baseline | {metrics['byte_reduction']}% |",
            f"| Rejected negative controls | {metrics['rejected_count']} |",
            f"| Lean fixture names checked | {metrics['lean_theorem_count']} |",
            "",
            "## Receipt Outcome",
            "",
            f"- Baseline receipt: `{metrics['baseline']}`.",
            f"- Selected receipt: `{metrics['selected']}`.",
            f"- Rejected controls: {rejected}.",
            "- Selection remains bounded by exact reconstruction, visible repair residual and fallback path, declared search bound, exact-replay consumer policy, and negative-control rejection.",
            "",
            "## Transition Boundary",
            "",
            f"- Narrow claim: `{metrics['claim_id']}`.",
            f"- Accepted transition: `{metrics['old_support_state']}` to `{metrics['new_support_state']}` with `{metrics['transition_effect']}` effect and `{metrics['transition_validity_state']}` validity.",
            "- This transition applies only to the bounded receipt-discipline slice. It does not promote `compact-generative-systems-and-residual-honesty.core` or any other chapter core claim.",
            "",
            "## Evidence Surfaces",
            "",
            f"- `{metrics['summary']}` is the human-readable slice report.",
            f"- `{metrics['input']}` contains the public-safe compact-generation records.",
            f"- `{metrics['result']}` records the recomputed local deterministic result.",
            f"- `{metrics['transition']}` records the accepted narrow non-core transition.",
            f"- `{metrics['lean']}` contains the finite fixture bridge names checked by `{metrics['validator']}`.",
            "",
            "## Non-Claim Boundary",
            "",
            "- No chapter core claim is promoted above `argument`.",
            "- No deployed compact generator, codec, fallback executor, semantic verifier, benchmark, model-quality result, safety result, or ASI capability is claimed.",
            "- The byte reduction is a fixture serialization count over one synthetic target, not a corpus compression benchmark.",
            "- Future broader claims require a separate accepted transition with real implementation artifacts, workloads, baselines, utility checks, negative controls, and explicit non-claims.",
            "",
            "## Validation Errors",
            "",
            *validation_lines,
            "",
        ]
    )


def compact_status_row(metrics: dict[str, Any] | None = None) -> str:
    if metrics is None:
        metrics, errors = collect()
        if errors:
            fail(errors)
    return (
        "| Compact GVR synthetic slice | Compact GVR detail is generated in "
        "`docs/compact_gvr_status_ledger.md`: "
        f"{metrics['case_count']} public-safe receipt records, "
        f"{metrics['baseline_bytes']}-byte literal baseline, "
        f"{metrics['selected_bytes']}-byte selected repeat-generator-plus-repair receipt, "
        f"{metrics['rejected_count']} rejected negative controls, "
        f"{metrics['byte_reduction']}% synthetic byte reduction, "
        "1 accepted narrow `synthetic-test-backed` non-core transition, and finite Lean fixture alignment. "
        "No chapter-core, deployed compression, codec-correctness, model-quality, benchmark, safety, or ASI claim is promoted. | "
        "`docs/compact_gvr_status_ledger.md`; `docs/compact_gvr_slice.md`; "
        "`experiments/compact_gvr_slice/input/v1_x_compact_gvr_records.json`; "
        "`experiments/compact_gvr_slice/results/2026-07-01-local.json`; "
        "`lean/AsiStackProofs/CompactGenerationRefinement.lean`; "
        "`evidence_transitions/v1_x_measured/compact_gvr_slice_synthetic_test_backed.json`; "
        "`python3 scripts/validate_compact_gvr_status_ledger.py`; "
        "`python3 scripts/validate_compact_gvr_slice.py` |"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help=f"rewrite {rel(LEDGER)}")
    args = parser.parse_args()

    metrics, errors = collect()
    if not metrics:
        fail(errors)
    report = build_report(metrics, errors)
    if args.write:
        LEDGER.write_text(report, encoding="utf-8")
        if errors:
            fail(errors)
        print(f"Wrote {rel(LEDGER)}")
        return

    if errors:
        fail(errors)
    if not LEDGER.exists():
        fail([f"{rel(LEDGER)} is missing; run with --write."])
    if LEDGER.read_text(encoding="utf-8").rstrip() != report.rstrip():
        fail([f"{rel(LEDGER)} is stale; run `python3 scripts/validate_compact_gvr_status_ledger.py --write`."])
    print(
        "Compact GVR status ledger validation passed: "
        f"{metrics['case_count']} receipts, {metrics['rejected_count']} controls rejected."
    )


if __name__ == "__main__":
    main()
