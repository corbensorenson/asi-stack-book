#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "experiments" / "substrate_adoption_trace" / "results" / "2026-07-02-local.json"
DOC = ROOT / "docs" / "substrate_adoption_trace.md"
CHAPTER = ROOT / "chapters" / "mathematical-and-search-substrates.qmd"
READER = (
    ROOT
    / "editions"
    / "reader_manuscript"
    / "v1_0"
    / "chapters"
    / "mathematical-and-search-substrates.qmd"
)
OUTLINE = ROOT / "docs" / "book_outline.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
CHANGELOG = ROOT / "appendices" / "F_changelog.qmd"
MANIFEST = ROOT / "book_structure.json"
VALIDATION_REGISTRY = ROOT / "validation" / "registry.json"
LEAN_FILE = ROOT / "lean" / "AsiStackProofs" / "SearchSubstrates.lean"

COMMAND = "python3 scripts/validate_substrate_adoption_trace.py"
PROOF_TAG = "lean:substrates.search.adoption_trace_bridge"
CODEX_TEST_NAME = "Substrate adoption trace"
REQUIRED_THEOREMS = [
    "substrate_adoption_trace_fixture_valid",
    "substrate_adoption_trace_rejects_axis_laundering",
    "substrate_adoption_trace_preserves_no_promotion_boundary",
]
REQUIRED_NON_CLAIMS = [
    "does not run a substrate A/B test",
    "does not prove representation efficiency, search quality, routing quality, compression quality, model quality, or runtime performance",
    "does not validate Circle, CoilMoECOT, Mamba, TreeLLM, or Theseus substrate adoption",
    "does not promote the Mathematical and Search Substrates chapter core claim",
    "does not create a support-state transition",
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Substrate adoption trace validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def text_blob(value: Any) -> str:
    if isinstance(value, dict):
        return "\n".join(f"{key}: {text_blob(child)}" for key, child in value.items()).lower()
    if isinstance(value, list):
        return "\n".join(text_blob(item) for item in value).lower()
    return str(value).lower()


def axis(axis_name: str, status: str, evidence_refs: list[str] | None = None) -> dict[str, Any]:
    return {
        "axis": axis_name,
        "status": status,
        "evidence_refs": evidence_refs or [],
        "non_claims": [f"{axis_name} axis is not promoted by this trace"],
    }


def trace(
    trace_id: str,
    *,
    expect_valid: bool,
    adoption_state: str,
    routing_permission_effect: str,
    consumer_requested_axis: str,
    requested_axis_status: str,
    workload_ref_present: bool = False,
    baseline_ref_present: bool = True,
    negative_control_present: bool = True,
    proof_boundary_present: bool = True,
    falsification_condition_present: bool = True,
    result_report_present: bool = False,
    failed_negative_control_recorded: bool = False,
    fallback_preserved: bool = True,
    retirement_or_supersession_path_present: bool = True,
    residuals_preserved: bool = True,
    support_state_effect: str = "none",
    non_claims: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "trace_id": trace_id,
        "expect_valid": expect_valid,
        "substrate_ref": "substrate://temporal-coil-demo",
        "ordinary_baseline_ref": "baseline://ordinary-dense-or-learned" if baseline_ref_present else "",
        "workload_ref": "workload://bounded-periodic-search-probe" if workload_ref_present else "",
        "negative_control_ref": "control://wrong-period-nonperiodic" if negative_control_present else "",
        "proof_boundary_ref": "proof-boundary://structural-only" if proof_boundary_present else "",
        "falsification_condition": (
            "retire or narrow if wrong-period or nonperiodic controls erase the advantage"
            if falsification_condition_present
            else ""
        ),
        "result_report_ref": "report://synthetic-negative-control-failed" if result_report_present else "",
        "axis_ledger": [
            axis("structure", "structural_only", ["proof-boundary://structural-only"] if proof_boundary_present else []),
            axis(consumer_requested_axis, requested_axis_status),
            axis("downstream_task_quality", "unmeasured"),
        ],
        "consumer_requested_axis": consumer_requested_axis,
        "requested_axis_status": requested_axis_status,
        "adoption_state": adoption_state,
        "routing_permission_effect": routing_permission_effect,
        "failed_negative_control_recorded": failed_negative_control_recorded,
        "fallback_substrate": "baseline://ordinary-dense-or-learned" if fallback_preserved else "",
        "fallback_preserved": fallback_preserved,
        "retirement_or_supersession_path_present": retirement_or_supersession_path_present,
        "residuals": [
            "synthetic adoption trace only; no substrate benchmark, sidecar run, or transfer consumer executed",
            "chapter core support state remains argument",
        ],
        "residuals_preserved": residuals_preserved,
        "support_state_effect": support_state_effect,
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
        "non_claims": REQUIRED_NON_CLAIMS if non_claims is None else non_claims,
    }


TRACES: list[dict[str, Any]] = [
    trace(
        "valid_exploratory_registration",
        expect_valid=True,
        adoption_state="exploratory",
        routing_permission_effect="planning_only",
        consumer_requested_axis="search_quality",
        requested_axis_status="planned",
    ),
    trace(
        "valid_structural_only_receipt",
        expect_valid=True,
        adoption_state="structural_only",
        routing_permission_effect="diagnostic_only",
        consumer_requested_axis="structure",
        requested_axis_status="structural_only",
    ),
    trace(
        "valid_consumer_axis_blocked",
        expect_valid=True,
        adoption_state="blocked",
        routing_permission_effect="blocked",
        consumer_requested_axis="routing_quality",
        requested_axis_status="unmeasured",
    ),
    trace(
        "valid_negative_control_retirement",
        expect_valid=True,
        adoption_state="refuted",
        routing_permission_effect="retired",
        consumer_requested_axis="search_quality",
        requested_axis_status="measured_negative",
        workload_ref_present=True,
        result_report_present=True,
        failed_negative_control_recorded=True,
    ),
    trace(
        "invalid_missing_baseline",
        expect_valid=False,
        adoption_state="exploratory",
        routing_permission_effect="planning_only",
        consumer_requested_axis="search_quality",
        requested_axis_status="planned",
        baseline_ref_present=False,
    ),
    trace(
        "invalid_missing_falsification_condition",
        expect_valid=False,
        adoption_state="exploratory",
        routing_permission_effect="planning_only",
        consumer_requested_axis="search_quality",
        requested_axis_status="planned",
        falsification_condition_present=False,
    ),
    trace(
        "invalid_theorem_spillover_route",
        expect_valid=False,
        adoption_state="qualified_for_scope",
        routing_permission_effect="qualified_route_allowed",
        consumer_requested_axis="search_quality",
        requested_axis_status="structural_only",
    ),
    trace(
        "invalid_unmeasured_axis_allowed",
        expect_valid=False,
        adoption_state="canary",
        routing_permission_effect="canary_route_allowed",
        consumer_requested_axis="compression_quality",
        requested_axis_status="unmeasured",
    ),
    trace(
        "invalid_failed_negative_control_promoted",
        expect_valid=False,
        adoption_state="qualified_for_scope",
        routing_permission_effect="qualified_route_allowed",
        consumer_requested_axis="search_quality",
        requested_axis_status="measured_negative",
        workload_ref_present=True,
        result_report_present=True,
        failed_negative_control_recorded=True,
    ),
    trace(
        "invalid_missing_fallback",
        expect_valid=False,
        adoption_state="canary",
        routing_permission_effect="canary_route_allowed",
        consumer_requested_axis="search_quality",
        requested_axis_status="measured_positive",
        workload_ref_present=True,
        result_report_present=True,
        fallback_preserved=False,
    ),
    trace(
        "invalid_support_promotion_overclaim",
        expect_valid=False,
        adoption_state="structural_only",
        routing_permission_effect="diagnostic_only",
        consumer_requested_axis="structure",
        requested_axis_status="structural_only",
        support_state_effect="synthetic-test-backed",
    ),
    trace(
        "invalid_missing_non_claim_boundary",
        expect_valid=False,
        adoption_state="blocked",
        routing_permission_effect="blocked",
        consumer_requested_axis="routing_quality",
        requested_axis_status="unmeasured",
        non_claims=["does not run a substrate A/B test"],
    ),
]


def route_allowed(effect: str) -> bool:
    return effect in {"canary_route_allowed", "qualified_route_allowed"}


def structural_diagnostic_allowed(record: dict[str, Any]) -> bool:
    return (
        record.get("consumer_requested_axis") == "structure"
        and record.get("requested_axis_status") == "structural_only"
        and record.get("routing_permission_effect") == "diagnostic_only"
    )


def measured_route_allowed(record: dict[str, Any]) -> bool:
    if record.get("requested_axis_status") != "measured_positive":
        return False
    return (
        bool(record.get("workload_ref"))
        and bool(record.get("ordinary_baseline_ref"))
        and bool(record.get("negative_control_ref"))
        and bool(record.get("result_report_ref"))
        and record.get("fallback_preserved") is True
        and record.get("residuals_preserved") is True
    )


def trace_errors(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    trace_id = str(record.get("trace_id", "<missing>"))
    if not str(record.get("substrate_ref", "")).startswith("substrate://"):
        errors.append(f"{trace_id}: substrate_ref must be present.")
    if not str(record.get("ordinary_baseline_ref", "")).startswith("baseline://"):
        errors.append(f"{trace_id}: ordinary baseline must be present.")
    if not str(record.get("negative_control_ref", "")).startswith("control://"):
        errors.append(f"{trace_id}: negative control must be present.")
    if not str(record.get("falsification_condition", "")).strip():
        errors.append(f"{trace_id}: falsification condition must be present.")
    if not str(record.get("proof_boundary_ref", "")).startswith("proof-boundary://"):
        errors.append(f"{trace_id}: proof boundary must be present.")
    if record.get("fallback_preserved") is not True or not str(record.get("fallback_substrate", "")).startswith("baseline://"):
        errors.append(f"{trace_id}: fallback substrate must be preserved.")
    if record.get("retirement_or_supersession_path_present") is not True:
        errors.append(f"{trace_id}: retirement or supersession path must be present.")
    if record.get("residuals_preserved") is not True:
        errors.append(f"{trace_id}: residuals must be preserved.")
    if record.get("support_state_effect") != "none":
        errors.append(f"{trace_id}: support_state_effect must remain none.")
    if record.get("chapter_core_support_effect") != "none":
        errors.append(f"{trace_id}: chapter_core_support_effect must remain none.")
    if record.get("evidence_transition_created") is not False:
        errors.append(f"{trace_id}: evidence_transition_created must remain false.")

    axis_status = str(record.get("requested_axis_status", ""))
    effect = str(record.get("routing_permission_effect", ""))
    if structural_diagnostic_allowed(record):
        pass
    elif route_allowed(effect):
        if not measured_route_allowed(record):
            errors.append(f"{trace_id}: route permission requires measured positive axis evidence and complete packet.")
    elif effect not in {"planning_only", "diagnostic_only", "blocked", "retired"}:
        errors.append(f"{trace_id}: routing_permission_effect {effect!r} is not recognized.")

    if axis_status in {"unmeasured", "planned", "blocked", "out_of_scope", "measured_negative"} and route_allowed(effect):
        errors.append(f"{trace_id}: {axis_status} axis cannot grant route permission.")
    if axis_status == "structural_only" and effect == "qualified_route_allowed":
        errors.append(f"{trace_id}: structural-only theorem boundary cannot grant qualified route permission.")
    if record.get("failed_negative_control_recorded") is True and effect != "retired":
        errors.append(f"{trace_id}: failed negative controls must retire or block route permission.")
    if record.get("failed_negative_control_recorded") is True and record.get("adoption_state") not in {"retired", "refuted", "blocked"}:
        errors.append(f"{trace_id}: failed negative controls cannot leave the substrate qualified.")

    residuals = record.get("residuals")
    if not isinstance(residuals, list) or not residuals:
        errors.append(f"{trace_id}: residuals must be recorded.")
    non_claim_text = text_blob(record.get("non_claims", []))
    for phrase in REQUIRED_NON_CLAIMS:
        if phrase.lower() not in non_claim_text:
            errors.append(f"{trace_id}: non_claims missing {phrase!r}.")
    return errors


def build_expected_result() -> dict[str, Any]:
    valid = [record for record in TRACES if record["expect_valid"]]
    invalid = [record for record in TRACES if not record["expect_valid"]]
    return {
        "schema_version": "asi_stack.substrate_adoption_trace.v0",
        "result_id": "2026-07-02-substrate-adoption-trace",
        "recorded_date": "2026-07-02",
        "command": COMMAND,
        "result_kind": "deterministic_synthetic_substrate_adoption_trace",
        "valid_trace_count": len(valid),
        "expected_invalid_control_count": len(invalid),
        "trace_count": len(TRACES),
        "traces": TRACES,
        "trace_assertions": {
            "exploratory_registration_present": True,
            "structural_only_receipt_present": True,
            "consumer_axis_blocked_present": True,
            "negative_control_retirement_present": True,
            "missing_baseline_rejected": True,
            "missing_falsification_rejected": True,
            "theorem_spillover_route_rejected": True,
            "unmeasured_axis_allowed_rejected": True,
            "failed_negative_control_promotion_rejected": True,
            "fallback_required": True,
            "support_state_effect_none": True,
            "chapter_core_support_effect_none": True,
            "evidence_transition_created": False,
            "non_claim_boundary": True,
        },
        "lean_fixture_alignment": {
            "module": "AsiStackProofs.SearchSubstrates",
            "proof_tag": PROOF_TAG,
            "theorem_refs": REQUIRED_THEOREMS,
            "expected": {
                "valid_trace_count": len(valid),
                "expected_invalid_control_count": len(invalid),
                "exploratory_registration_present": True,
                "structural_only_receipt_present": True,
                "consumer_axis_blocked_present": True,
                "negative_control_retirement_present": True,
                "missing_baseline_rejected": True,
                "theorem_spillover_rejected": True,
                "failed_negative_control_promotion_rejected": True,
                "unmeasured_axis_allowed_rejected": True,
                "fallback_required": True,
                "support_state_effect_none": True,
                "non_claim_boundary": True,
            },
        },
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
        "verification_result": "pass",
        "non_claims": REQUIRED_NON_CLAIMS,
    }


def validate_result(expected: dict[str, Any], write_result: bool, errors: list[str]) -> None:
    serialized = json.dumps(expected, indent=2) + "\n"
    if write_result:
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(serialized, encoding="utf-8")
        return
    if not RESULT.exists():
        errors.append(f"Missing {rel(RESULT)}; run {COMMAND} --write-result.")
        return
    current = RESULT.read_text(encoding="utf-8")
    if current != serialized:
        errors.append(f"{rel(RESULT)} is stale; run {COMMAND} --write-result.")
    value = load_json(RESULT)
    non_claim_text = text_blob(value.get("non_claims", []))
    for phrase in REQUIRED_NON_CLAIMS:
        if phrase.lower() not in non_claim_text:
            errors.append(f"{rel(RESULT)} non_claims missing {phrase!r}.")


def validate_lean(errors: list[str]) -> None:
    text = LEAN_FILE.read_text(encoding="utf-8", errors="ignore")
    fixture_match = re.search(
        r"def\s+substrateAdoptionTraceFixture\s*:\s*SubstrateAdoptionTraceSummary\s*:=\s*\{(?P<body>.*?)\n\}",
        text,
        re.S,
    )
    if not fixture_match:
        errors.append(f"{rel(LEAN_FILE)} missing substrateAdoptionTraceFixture.")
        return
    body = fixture_match.group("body")
    expected_fields = {
        "validTraceCount": "4",
        "expectedInvalidControlCount": "8",
        "exploratoryRegistrationPresent": "true",
        "structuralOnlyReceiptPresent": "true",
        "consumerAxisBlockedPresent": "true",
        "negativeControlRetirementPresent": "true",
        "missingBaselineRejected": "true",
        "theoremSpilloverRejected": "true",
        "failedNegativeControlPromotionRejected": "true",
        "unmeasuredAxisAllowedRejected": "true",
        "fallbackRequired": "true",
        "supportStateEffectNone": "true",
        "nonClaimBoundary": "true",
    }
    for field, expected in expected_fields.items():
        if not re.search(rf"{field}\s*:=\s*{expected}\b", body):
            errors.append(f"{rel(LEAN_FILE)} fixture field {field} must be {expected}.")
    for theorem in REQUIRED_THEOREMS:
        if f"theorem {theorem}" not in text:
            errors.append(f"{rel(LEAN_FILE)} missing theorem {theorem}.")


def require_text(path: Path, snippets: list[str], errors: list[str]) -> None:
    if not path.exists():
        errors.append(f"Missing {rel(path)}.")
        return
    text = path.read_text(encoding="utf-8", errors="ignore")
    normalized_text = " ".join(text.split()).lower()
    for snippet in snippets:
        normalized_snippet = " ".join(snippet.split()).lower()
        if normalized_snippet not in normalized_text:
            errors.append(f"{rel(path)} missing {snippet!r}.")


def validate_surfaces(errors: list[str]) -> None:
    surface_snippets = [
        "Substrate adoption trace",
        "valid_exploratory_registration",
        "invalid_theorem_spillover_route",
        "no substrate A/B test",
        "no support-state promotion",
    ]
    for path in (DOC, CHAPTER, READER, OUTLINE, ROADMAP, CHANGELOG):
        require_text(path, surface_snippets[:1], errors)
    require_text(CHAPTER, ["substrate adoption trace", "valid_negative_control_retirement"], errors)
    require_text(READER, ["substrate adoption trace", "negative-control retirement"], errors)
    require_text(OUTLINE, [PROOF_TAG, CODEX_TEST_NAME], errors)
    require_text(ROADMAP, ["Substrate adoption trace", "valid_negative_control_retirement"], errors)
    require_text(CHANGELOG, [COMMAND, PROOF_TAG], errors)
    require_text(VALIDATION_REGISTRY, [rel(RESULT), "validate_substrate_adoption_trace.py"], errors)

    manifest_text = MANIFEST.read_text(encoding="utf-8", errors="ignore")
    for snippet in (CODEX_TEST_NAME, PROOF_TAG):
        if snippet not in manifest_text:
            errors.append(f"{rel(MANIFEST)} missing {snippet!r}.")


def validate_traces(errors: list[str]) -> None:
    valid_count = 0
    invalid_count = 0
    for record in TRACES:
        semantic_errors = trace_errors(record)
        if record["expect_valid"]:
            valid_count += 1
            if semantic_errors:
                errors.extend(semantic_errors)
        else:
            invalid_count += 1
            if not semantic_errors:
                errors.append(f"{record['trace_id']}: expected-invalid control unexpectedly passed.")
    if valid_count != 4:
        errors.append(f"Expected 4 valid traces, found {valid_count}.")
    if invalid_count != 8:
        errors.append(f"Expected 8 expected-invalid controls, found {invalid_count}.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-result", action="store_true", help="Write the deterministic result artifact.")
    args = parser.parse_args()

    errors: list[str] = []
    validate_traces(errors)
    expected = build_expected_result()
    validate_result(expected, args.write_result, errors)
    validate_lean(errors)
    validate_surfaces(errors)

    if errors:
        fail(errors)

    action = "wrote" if args.write_result else "validated"
    print(
        f"Substrate adoption trace {action}: "
        f"{expected['valid_trace_count']} valid traces, "
        f"{expected['expected_invalid_control_count']} expected-invalid controls."
    )


if __name__ == "__main__":
    main()
