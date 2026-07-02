#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from validate_benchmark_antigoodhart import (
    FIXTURE_DIR,
    ROOT,
    fixture_expectation,
    load_json,
    load_schemas,
    schema_errors_for_scenario,
    semantic_errors,
)

RESULT = ROOT / "experiments" / "benchmark_antigoodhart" / "results" / "2026-07-02-fixture-bridge.json"
DOC = ROOT / "docs" / "benchmark_antigoodhart_harness.md"
CHAPTER = ROOT / "chapters" / "benchmark-ratchets-and-anti-goodhart-evidence.qmd"
READER = (
    ROOT
    / "editions"
    / "reader_manuscript"
    / "v1_0"
    / "chapters"
    / "benchmark-ratchets-and-anti-goodhart-evidence.qmd"
)
OUTLINE = ROOT / "docs" / "book_outline.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
CHANGELOG = ROOT / "appendices" / "F_changelog.qmd"
MANIFEST = ROOT / "book_structure.json"
VALIDATE_BOOK = ROOT / "scripts" / "validate_book.py"
LEAN_FIXTURE = ROOT / "lean" / "AsiStackProofs" / "BenchmarkRatchets.lean"

COMMAND = "python3 scripts/validate_benchmark_fixture_bridge.py"
PROOF_TAG = "lean:benchmarks.ratchet.fixture_bridge"
CODEX_TEST_NAME = "Benchmark anti-Goodhart fixture bridge"
REQUIRED_THEOREMS = [
    "benchmark_antigoodhart_fixture_bridge_valid",
    "benchmark_antigoodhart_fixture_bridge_has_expected_controls",
    "benchmark_antigoodhart_fixture_bridge_preserves_no_support_promotion",
]
EXPECTED_VALID_SCENARIOS = [
    "benchmark-goodhart-valid-promote-001",
    "benchmark-goodhart-valid-regression-floor-001",
]
EXPECTED_INVALID_SCENARIOS = [
    "benchmark-goodhart-invalid-missing-checks",
    "benchmark-goodhart-invalid-policy-promotes-blocked",
    "benchmark-goodhart-invalid-reward-truth",
    "benchmark-goodhart-invalid-saturated-promoted",
    "benchmark-goodhart-invalid-steward-no-approval",
]
EXPECTED_CONTROL_FLAGS = {
    "missing_goodhart_checks_rejected": "benchmark-goodhart-invalid-missing-checks",
    "policy_from_blocked_ratchet_rejected": "benchmark-goodhart-invalid-policy-promotes-blocked",
    "reward_as_truth_rejected": "benchmark-goodhart-invalid-reward-truth",
    "saturated_promotion_rejected": "benchmark-goodhart-invalid-saturated-promoted",
    "release_without_approval_rejected": "benchmark-goodhart-invalid-steward-no-approval",
}
EXPECTED_LEAN_FIELDS = {
    "validFixtureCount": 2,
    "expectedInvalidFixtureCount": 5,
    "promotionReadyValidCount": 1,
    "regressionFloorValidCount": 1,
    "missingGoodhartChecksRejected": True,
    "policyFromBlockedRatchetRejected": True,
    "rewardAsTruthRejected": True,
    "saturatedPromotionRejected": True,
    "releaseWithoutApprovalRejected": True,
    "supportStateEffectNone": True,
    "nonClaimBoundary": True,
}
REQUIRED_NON_CLAIMS = [
    "does not run an empirical benchmark",
    "does not prove hidden-holdout integrity",
    "does not prove policy-training quality",
    "does not execute a steward release",
    "does not promote chapter core support",
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Benchmark fixture bridge validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def text_blob(value: Any) -> str:
    if isinstance(value, dict):
        return "\n".join(f"{key}: {text_blob(child)}" for key, child in value.items()).lower()
    if isinstance(value, list):
        return "\n".join(text_blob(item) for item in value).lower()
    return str(value).lower()


def validate_fixture_semantics() -> dict[str, Any]:
    schemas = load_schemas()
    fixtures = sorted(FIXTURE_DIR.glob("*.json"))
    if not fixtures:
        fail([f"No benchmark anti-Goodhart fixtures found in {rel(FIXTURE_DIR)}."])

    errors: list[str] = []
    valid_scenarios: list[str] = []
    invalid_scenarios: list[str] = []
    promotion_ready_valid_count = 0
    regression_floor_valid_count = 0
    invalid_control_names: list[str] = []

    for fixture in fixtures:
        relative = rel(fixture)
        expect_valid = fixture_expectation(fixture)
        if expect_valid is None:
            errors.append(f"{relative}: fixture name must start with valid_ or invalid_.")
            continue
        try:
            value = load_json(fixture)
        except Exception as exc:
            errors.append(f"{relative}: invalid JSON: {exc}")
            continue
        if not isinstance(value, dict):
            errors.append(f"{relative}: scenario must contain a JSON object.")
            continue
        scenario_id = value.get("scenario_id")
        if not isinstance(scenario_id, str) or not scenario_id.strip():
            errors.append(f"{relative}: scenario_id must be a non-empty string.")
            continue

        scenario_errors = schema_errors_for_scenario(value, schemas, relative)
        if not scenario_errors:
            scenario_errors.extend(semantic_errors(value, relative))

        ratchet = value["benchmark_ratchet_record"]
        if expect_valid:
            valid_scenarios.append(scenario_id)
            if scenario_errors:
                errors.extend(scenario_errors)
            if ratchet.get("promotion_decision") == "promote":
                promotion_ready_valid_count += 1
            if ratchet.get("promotion_decision") == "regression_only":
                regression_floor_valid_count += 1
        else:
            invalid_scenarios.append(scenario_id)
            invalid_control_names.append(fixture.name)
            if not scenario_errors:
                errors.append(f"{relative}: invalid fixture unexpectedly passed benchmark anti-Goodhart checks.")

    if valid_scenarios != EXPECTED_VALID_SCENARIOS:
        errors.append(f"valid scenario IDs must be {EXPECTED_VALID_SCENARIOS!r}, found {valid_scenarios!r}.")
    if invalid_scenarios != EXPECTED_INVALID_SCENARIOS:
        errors.append(f"expected-invalid scenario IDs must be {EXPECTED_INVALID_SCENARIOS!r}, found {invalid_scenarios!r}.")
    if promotion_ready_valid_count != 1:
        errors.append(f"expected one promotion-ready valid fixture, found {promotion_ready_valid_count}.")
    if regression_floor_valid_count != 1:
        errors.append(f"expected one regression-floor valid fixture, found {regression_floor_valid_count}.")
    if errors:
        fail(errors)

    controls = {
        name: scenario_id in set(invalid_scenarios)
        for name, scenario_id in EXPECTED_CONTROL_FLAGS.items()
    }
    return {
        "valid_fixture_count": len(valid_scenarios),
        "expected_invalid_fixture_count": len(invalid_scenarios),
        "valid_scenarios": valid_scenarios,
        "expected_invalid_scenarios": invalid_scenarios,
        "promotion_ready_valid_count": promotion_ready_valid_count,
        "regression_floor_valid_count": regression_floor_valid_count,
        "invalid_control_fixture_files": invalid_control_names,
        "control_coverage": controls,
    }


def build_expected_result(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "asi_stack.benchmark_antigoodhart_fixture_bridge.v0",
        "result_id": "2026-07-02-benchmark-antigoodhart-fixture-bridge",
        "recorded_date": "2026-07-02",
        "command": COMMAND,
        "input_fixture_dir": rel(FIXTURE_DIR),
        "result_kind": "synthetic_cross_record_fixture_bridge",
        "proof_bridge_type": "Python/Lean finite fixture-summary equivalence",
        **summary,
        "lean_fixture_alignment": {
            "module": "AsiStackProofs.BenchmarkRatchets",
            "proof_tag": PROOF_TAG,
            "theorem_refs": REQUIRED_THEOREMS,
            "expected": {
                "valid_fixture_count": 2,
                "expected_invalid_fixture_count": 5,
                "promotion_ready_valid_count": 1,
                "regression_floor_valid_count": 1,
                "missing_goodhart_checks_rejected": True,
                "policy_from_blocked_ratchet_rejected": True,
                "reward_as_truth_rejected": True,
                "saturated_promotion_rejected": True,
                "release_without_approval_rejected": True,
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
        RESULT.write_text(serialized, encoding="utf-8")
        return
    if not RESULT.exists():
        errors.append(f"Missing {rel(RESULT)}; run {COMMAND} --write-result.")
        return
    current = RESULT.read_text(encoding="utf-8")
    if current != serialized:
        errors.append(f"{rel(RESULT)} is stale; run {COMMAND} --write-result.")
    value = load_json(RESULT)
    non_claims = text_blob(value.get("non_claims", []))
    for phrase in REQUIRED_NON_CLAIMS:
        if phrase not in non_claims:
            errors.append(f"{rel(RESULT)} non_claims missing {phrase!r}.")


def validate_lean_fixture(errors: list[str]) -> None:
    text = LEAN_FIXTURE.read_text(encoding="utf-8", errors="ignore")
    fixture_match = re.search(
        r"def\s+benchmarkAntiGoodhartFixtureBridge\s*:\s*"
        r"AntiGoodhartFixtureBridgeSummary\s*:=\s*\{(?P<body>.*?)\}",
        text,
        re.DOTALL,
    )
    if not fixture_match:
        errors.append(f"{rel(LEAN_FIXTURE)} missing benchmarkAntiGoodhartFixtureBridge.")
        return
    body = fixture_match.group("body")
    for field, expected in EXPECTED_LEAN_FIELDS.items():
        if isinstance(expected, bool):
            expected_text = "true" if expected else "false"
        else:
            expected_text = str(expected)
        pattern = rf"{field}\s*:=\s*{expected_text}\b"
        if not re.search(pattern, body):
            errors.append(
                f"{rel(LEAN_FIXTURE)} benchmarkAntiGoodhartFixtureBridge.{field} "
                f"must be {expected_text}."
            )
    for theorem in REQUIRED_THEOREMS:
        if theorem not in text:
            errors.append(f"{rel(LEAN_FIXTURE)} missing theorem {theorem}.")


def manifest_contains_bridge(errors: list[str]) -> None:
    manifest = load_json(MANIFEST)
    chapters = []
    for part in manifest.get("parts", []):
        chapters.extend(part.get("chapters", []))
    chapter = next(
        (item for item in chapters if item.get("id") == "benchmark-ratchets-and-anti-goodhart-evidence"),
        None,
    )
    if not isinstance(chapter, dict):
        errors.append("book_structure.json missing benchmark chapter entry.")
        return
    codex_names = {test.get("name") for test in chapter.get("codex_tests", []) if isinstance(test, dict)}
    if CODEX_TEST_NAME not in codex_names:
        errors.append(f"book_structure.json missing Codex test {CODEX_TEST_NAME!r}.")
    proof_tags = {target.get("tag") for target in chapter.get("proof_targets", []) if isinstance(target, dict)}
    if PROOF_TAG not in proof_tags:
        errors.append(f"book_structure.json missing proof target {PROOF_TAG!r}.")


def validate_surfaces(errors: list[str]) -> None:
    required_fragments = {
        RESULT: [
            "2026-07-02-benchmark-antigoodhart-fixture-bridge",
            "valid_fixture_count",
            "expected_invalid_fixture_count",
            PROOF_TAG,
        ],
        DOC: [
            COMMAND,
            rel(RESULT),
            "2 valid fixture(s), 5 expected-invalid fixture(s)",
            "Python/Lean finite fixture-summary equivalence",
        ],
        CHAPTER: [
            COMMAND,
            rel(RESULT),
            CODEX_TEST_NAME,
            PROOF_TAG,
            "2 valid fixtures and 5 expected-invalid controls",
        ],
        READER: [
            "fixture bridge",
            "two valid synthetic paths",
            "five expected-invalid controls",
        ],
        OUTLINE: [
            COMMAND,
            rel(RESULT),
            CODEX_TEST_NAME,
            PROOF_TAG,
        ],
        ROADMAP: [
            "Benchmark anti-Goodhart fixture bridge",
            "2 valid fixtures",
            "5 expected-invalid controls",
        ],
        CHANGELOG: [
            "Add benchmark anti-Goodhart fixture bridge",
            rel(RESULT),
            COMMAND,
        ],
        VALIDATE_BOOK: [
            "scripts/validate_benchmark_fixture_bridge.py",
            "experiments/benchmark_antigoodhart/results/2026-07-02-fixture-bridge.json",
            "validate_benchmark_fixture_bridge.py",
        ],
    }
    for path, fragments in required_fragments.items():
        text = path.read_text(encoding="utf-8", errors="ignore")
        for fragment in fragments:
            if fragment not in text:
                errors.append(f"{rel(path)} missing required fragment {fragment!r}.")
    manifest_contains_bridge(errors)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-result", action="store_true", help="Rewrite the tracked bridge result JSON.")
    args = parser.parse_args()

    summary = validate_fixture_semantics()
    expected = build_expected_result(summary)
    errors: list[str] = []
    validate_result(expected, args.write_result, errors)
    validate_lean_fixture(errors)
    validate_surfaces(errors)
    if errors:
        fail(errors)
    print(
        "Benchmark fixture bridge validation passed: "
        f"{summary['valid_fixture_count']} valid fixture(s), "
        f"{summary['expected_invalid_fixture_count']} expected-invalid fixture(s), "
        "Lean fixture bridge aligned."
    )


if __name__ == "__main__":
    main()
