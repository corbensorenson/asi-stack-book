#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "experiments" / "compact_gvr_slice" / "input" / "v1_x_compact_gvr_records.json"
RESULT = ROOT / "experiments" / "compact_gvr_slice" / "results" / "2026-07-01-local.json"
SUMMARY = ROOT / "docs" / "compact_gvr_slice.md"
TRANSITION = (
    ROOT
    / "evidence_transitions"
    / "v1_x_measured"
    / "compact_gvr_slice_synthetic_test_backed.json"
)
LEAN_FIXTURE = ROOT / "lean" / "AsiStackProofs" / "CompactGenerativeSystems.lean"

EXPECTED_CASES = 5
EXPECTED_SELECTED = "receipt://repeat-generator-plus-repair"
EXPECTED_BASELINE = "receipt://literal-baseline"
EXPECTED_NEGATIVE_CONTROLS = {
    "receipt://lossy-summary-marked-exact",
    "receipt://negative-rate-no-fallback",
    "receipt://bounded-search-overrun",
}
REQUIRED_NON_CLAIMS = (
    "does not promote any chapter core claim",
    "compression utility",
    "codec correctness",
)
REQUIRED_LEAN_THEOREMS = (
    "compact_gvr_fixture_selected_is_eligible",
    "lossy_marked_exact_fixture_rejected",
    "negative_rate_without_fallback_fixture_rejected",
    "bounded_search_overrun_fixture_rejected",
    "compact_gvr_fixture_selected_beats_literal_baseline",
)
RECEIPT_ID_TO_LEAN_CONSTRUCTOR = {
    "receipt://literal-baseline": "literalBaseline",
    "receipt://repeat-generator-plus-repair": "repeatGeneratorPlusRepair",
    "receipt://lossy-summary-marked-exact": "lossySummaryMarkedExact",
    "receipt://negative-rate-no-fallback": "negativeRateNoFallback",
    "receipt://bounded-search-overrun": "boundedSearchOverrun",
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def fail(errors: list[str]) -> None:
    print("Compact GVR slice validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def text_blob(value: Any) -> str:
    if isinstance(value, list):
        return "\n".join(str(item) for item in value).lower()
    if isinstance(value, dict):
        return "\n".join(f"{key}: {child}" for key, child in value.items()).lower()
    return str(value).lower()


def reconstruct(case: dict[str, Any]) -> str:
    generation = case["generation"]
    mode = generation["mode"]
    if mode == "literal":
        return str(generation["literal"])
    if mode == "repeat":
        return str(generation["seed"]) * int(generation["count"]) + str(generation.get("repair_residual", ""))
    if mode == "search_overrun":
        return str(generation["seed"]) * int(generation["attempted_count"])
    raise ValueError(f"unknown generation mode {mode!r}")


def byte_len(text: str) -> int:
    return len(text.encode("utf-8"))


def case_role(case: dict[str, Any]) -> str:
    return str(case.get("role", ""))


def rejection_reasons(case: dict[str, Any], target: str, baseline_bytes: int) -> list[str]:
    generated = reconstruct(case)
    exact = generated == target
    representation_bytes = byte_len(str(case["serialized_form"]))
    reasons: list[str] = []
    if case.get("marked_exact") is not True:
        reasons.append("not_marked_exact")
    if case.get("verification_result") != "pass":
        reasons.append(f"verification_result={case.get('verification_result')}")
    if not exact:
        reasons.append("reconstruction_mismatch")
    if case.get("fallback_present") is not True:
        reasons.append("fallback_missing")
    if not case.get("residual_owner"):
        reasons.append("residual_owner_missing")
    if int(case.get("search_steps", 0)) > int(case.get("search_bound", 0)):
        reasons.append("search_bound_exceeded")
    if representation_bytes >= baseline_bytes:
        reasons.append("not_smaller_than_literal_baseline")
    if "exact_replay" not in case.get("consumer_policy", []):
        reasons.append("consumer_policy_lacks_exact_replay")
    if case.get("support_state_effect") != "eligible_for_bounded_evidence_review":
        reasons.append(f"support_state_effect={case.get('support_state_effect')}")
    return reasons


def case_is_eligible(case: dict[str, Any], target: str, baseline_bytes: int) -> bool:
    return not rejection_reasons(case, target, baseline_bytes)


def validate_non_claims(owner: str, non_claims: Any, errors: list[str]) -> None:
    if not isinstance(non_claims, list) or not non_claims:
        errors.append(f"{owner}: non_claims must be a non-empty list.")
        return
    blob = text_blob(non_claims)
    for phrase in REQUIRED_NON_CLAIMS:
        if phrase not in blob:
            errors.append(f"{owner}: non_claims missing boundary phrase {phrase!r}.")


def build_result(packet: dict[str, Any], errors: list[str]) -> dict[str, Any]:
    target = str(packet["target_text"])
    cases = packet["cases"]
    if not isinstance(cases, list) or len(cases) != EXPECTED_CASES:
        errors.append(f"{rel(INPUT)} must contain {EXPECTED_CASES} case records.")
        cases = []

    baseline = next((case for case in cases if case.get("receipt_id") == EXPECTED_BASELINE), None)
    if baseline is None:
        errors.append(f"{rel(INPUT)} missing baseline {EXPECTED_BASELINE}.")
        baseline_bytes = byte_len(target)
    else:
        baseline_bytes = byte_len(str(baseline["serialized_form"]))
        if reconstruct(baseline) != target:
            errors.append(f"{EXPECTED_BASELINE} must reconstruct the target exactly.")
        if baseline_bytes != byte_len(target):
            errors.append(f"{EXPECTED_BASELINE} serialized bytes must equal target bytes.")

    case_results: list[dict[str, Any]] = []
    eligible: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    for case in cases:
        receipt_id = str(case.get("receipt_id"))
        generated = reconstruct(case)
        representation_bytes = byte_len(str(case.get("serialized_form", "")))
        exact = generated == target
        reasons = rejection_reasons(case, target, baseline_bytes)
        is_baseline = receipt_id == EXPECTED_BASELINE
        status = "baseline" if is_baseline else ("eligible" if not reasons else "rejected")
        row = {
            "receipt_id": receipt_id,
            "role": case_role(case),
            "status": status,
            "representation_bytes": representation_bytes,
            "exact_reconstruction": exact,
            "rejection_reasons": reasons,
        }
        case_results.append(row)
        validate_non_claims(receipt_id, case.get("non_claims"), errors)
        if not is_baseline and case_is_eligible(case, target, baseline_bytes):
            eligible.append(row)
        elif not is_baseline:
            rejected.append(row)

    selected = min(eligible, key=lambda row: row["representation_bytes"]) if eligible else None
    if selected is None:
        errors.append("no eligible compact receipt found.")
        selected_id = ""
        selected_bytes = 0
    else:
        selected_id = str(selected["receipt_id"])
        selected_bytes = int(selected["representation_bytes"])
        if selected_id != EXPECTED_SELECTED:
            errors.append(f"selected receipt {selected_id!r} did not match {EXPECTED_SELECTED!r}.")

    rejected_ids = {str(row["receipt_id"]) for row in rejected}
    missing_controls = sorted(EXPECTED_NEGATIVE_CONTROLS - rejected_ids)
    for receipt_id in missing_controls:
        errors.append(f"negative control {receipt_id} was not rejected.")

    result = {
        "schema_version": "0.1",
        "result_id": "2026-07-01-local-compact-gvr-slice",
        "slice_id": str(packet.get("slice_id")),
        "input_ref": rel(INPUT),
        "command": "python3 scripts/validate_compact_gvr_slice.py",
        "environment": "local deterministic Python validation over tracked public-safe synthetic compact-generation records",
        "target_bytes": byte_len(target),
        "baseline_receipt": EXPECTED_BASELINE,
        "baseline_bytes": baseline_bytes,
        "selected_receipt": selected_id,
        "selected_bytes": selected_bytes,
        "byte_reduction_vs_literal_percent": round((baseline_bytes - selected_bytes) / baseline_bytes * 100, 2)
        if baseline_bytes and selected_bytes
        else 0,
        "eligible_receipts": [str(row["receipt_id"]) for row in eligible],
        "negative_control_receipts": sorted(EXPECTED_NEGATIVE_CONTROLS),
        "rejected_receipts": rejected,
        "case_results": case_results,
        "acceptance_predicate": (
            "The selected compact receipt must reconstruct the target exactly, remain below the literal "
            "baseline byte count, keep repair residual and fallback records visible, stay within the search "
            "bound, preserve exact-replay consumer policy, and reject lossy exactness, negative-rate/no-fallback, "
            "and bounded-search-overrun controls."
        ),
        "lean_fixture_alignment": {
            "lean_module": rel(LEAN_FIXTURE),
            "selected_constructor": RECEIPT_ID_TO_LEAN_CONSTRUCTOR[EXPECTED_SELECTED],
            "baseline_constructor": RECEIPT_ID_TO_LEAN_CONSTRUCTOR[EXPECTED_BASELINE],
            "receipt_constructors": RECEIPT_ID_TO_LEAN_CONSTRUCTOR,
            "checked_theorem_names": list(REQUIRED_LEAN_THEOREMS),
        },
        "verification_result": "pass",
        "support_state_effect": "eligible_for_bounded_evidence_review",
        "residuals": [
            "The selected receipt uses an explicit repair residual and fallback path.",
            "The lossy exactness negative control is rejected after reconstruction mismatch and failed verification.",
            "The negative-rate/no-fallback control is rejected despite exact reconstruction because its serialized form is larger than the literal baseline and fallback is missing.",
            "The bounded-search-overrun control is rejected because attempted search exceeds the declared bound.",
            "The result is synthetic and local; no deployed codec, generator, verifier, compression-utility, model-quality, or chapter-core claim is made.",
        ],
        "non_claims": [
            "does not promote any chapter core claim above argument",
            "does not prove compression utility, codec correctness, semantic utility, model quality, or benchmark performance",
            "does not prove deployed generator, verifier, fallback execution, or reconstruction behavior outside this synthetic fixture",
        ],
    }
    return result


def validate_summary(expected_result: dict[str, Any], errors: list[str]) -> None:
    if not SUMMARY.exists():
        errors.append(f"Missing {rel(SUMMARY)}.")
        return
    text = SUMMARY.read_text(encoding="utf-8")
    required_fragments = [
        "Compact GVR Synthetic Slice",
        "compact-generative-systems.compact_gvr_receipt_slice",
        "Support transition: `argument` to `synthetic-test-backed`",
        "`receipt://repeat-generator-plus-repair` | selected compact receipt | 78 | eligible",
        "`receipt://literal-baseline` | literal baseline | 368 | baseline",
        "`receipt://lossy-summary-marked-exact` | lossy exactness control | 55 | rejected",
        "`receipt://negative-rate-no-fallback` | negative-rate/no-fallback control | 485 | rejected",
        "`receipt://bounded-search-overrun` | bounded-search control | 72 | rejected",
        "78.8 percent smaller",
        "Lean Fixture Bridge",
        "`AsiStackProofs.CompactGenerativeSystems`",
        "Does not promote any chapter core claim above `argument`.",
        "Does not prove compression utility",
    ]
    for fragment in required_fragments:
        if fragment not in text:
            errors.append(f"{rel(SUMMARY)} missing required fragment: {fragment}")
    if expected_result["selected_receipt"] not in text:
        errors.append(f"{rel(SUMMARY)} does not name selected receipt.")


def validate_transition(expected_result: dict[str, Any], errors: list[str]) -> None:
    if not TRANSITION.exists():
        errors.append(f"Missing {rel(TRANSITION)}.")
        return
    value = load_json(TRANSITION)
    if not isinstance(value, dict):
        errors.append(f"{rel(TRANSITION)} must contain an object.")
        return
    expected = {
        "claim_id": "compact-generative-systems.compact_gvr_receipt_slice",
        "old_support_state": "argument",
        "new_support_state": "synthetic-test-backed",
        "transition_effect": "upward",
        "transition_validity_state": "review_accepted",
        "verification_result": "pass",
        "review_status": "accepted",
        "support_state_effect": "eligible_for_bounded_evidence_review",
    }
    for key, expected_value in expected.items():
        if value.get(key) != expected_value:
            errors.append(f"{rel(TRANSITION)}: {key} must be {expected_value!r}.")
    refs = (
        value.get("artifact_refs", [])
        + value.get("evidence_packet_refs", [])
        + value.get("claim_surface_refs", [])
        + value.get("claim_record_refs", [])
    )
    for ref in (
        rel(INPUT),
        rel(RESULT),
        rel(SUMMARY),
        rel(LEAN_FIXTURE),
        "scripts/validate_compact_gvr_slice.py",
    ):
        if ref not in refs:
            errors.append(f"{rel(TRANSITION)} must reference {ref}.")
    if expected_result["selected_receipt"] not in value.get("transition_reason", ""):
        errors.append(f"{rel(TRANSITION)} transition_reason must name selected receipt.")
    validate_non_claims(rel(TRANSITION), value.get("non_claims"), errors)


def validate_lean_fixture(errors: list[str]) -> None:
    if not LEAN_FIXTURE.exists():
        errors.append(f"Missing {rel(LEAN_FIXTURE)}.")
        return
    text = LEAN_FIXTURE.read_text(encoding="utf-8")
    constructor_match = re.search(
        r"inductive\s+CompactGVRFixtureReceipt\s+where(?P<body>.*?)deriving\s+DecidableEq",
        text,
        re.DOTALL,
    )
    if not constructor_match:
        errors.append(f"{rel(LEAN_FIXTURE)} missing CompactGVRFixtureReceipt constructors.")
        constructors: set[str] = set()
    else:
        constructors = set(re.findall(r"^\s*\|\s+(\w+)\s*$", constructor_match.group("body"), re.MULTILINE))
    missing_constructors = sorted(set(RECEIPT_ID_TO_LEAN_CONSTRUCTOR.values()) - constructors)
    for constructor in missing_constructors:
        errors.append(f"{rel(LEAN_FIXTURE)} missing constructor {constructor}.")

    declared_theorems = set(re.findall(r"^theorem\s+(\w+)\b", text, re.MULTILINE))
    for theorem in sorted(set(REQUIRED_LEAN_THEOREMS) - declared_theorems):
        errors.append(f"{rel(LEAN_FIXTURE)} missing theorem {theorem}.")
    for number in ("368", "78", "55", "485", "72"):
        if number not in text:
            errors.append(f"{rel(LEAN_FIXTURE)} missing fixture byte number {number}.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-result", action="store_true", help="Rewrite the tracked result JSON from the input fixture.")
    args = parser.parse_args()

    errors: list[str] = []
    packet = load_json(INPUT)
    if not isinstance(packet, dict):
        fail([f"{rel(INPUT)} must contain an object."])
    validate_non_claims(rel(INPUT), packet.get("non_claims"), errors)
    result = build_result(packet, errors)

    serialized_result = json.dumps(result, indent=2, sort_keys=False) + "\n"
    if args.write_result:
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(serialized_result, encoding="utf-8")
    elif not RESULT.exists():
        errors.append(f"Missing {rel(RESULT)}; run with --write-result to create it.")
    else:
        current = RESULT.read_text(encoding="utf-8")
        if current != serialized_result:
            errors.append(f"{rel(RESULT)} is stale; run scripts/validate_compact_gvr_slice.py --write-result.")

    validate_summary(result, errors)
    validate_transition(result, errors)
    validate_lean_fixture(errors)

    if errors:
        fail(errors)

    print(
        "Compact GVR slice validation passed: "
        f"{EXPECTED_CASES} receipt(s), selected {result['selected_receipt']}, "
        f"{len(EXPECTED_NEGATIVE_CONTROLS)} negative control(s) rejected, "
        f"{result['byte_reduction_vs_literal_percent']} percent byte reduction vs literal baseline."
    )


if __name__ == "__main__":
    main()
