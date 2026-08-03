#!/usr/bin/env python3
from __future__ import annotations

import argparse
from itertools import product
import json
import re
import subprocess
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
VALIDATION_REGISTRY = ROOT / "validation" / "registry.json"
LEAN_FIXTURE = ROOT / "lean" / "AsiStackProofs" / "BenchmarkRatchets.lean"
LEAN_ROOT = ROOT / "lean"

COMMAND = "python3 scripts/validate_benchmark_fixture_bridge.py"
PROOF_TAG = "lean:benchmarks.ratchet.fixture_bridge"
CODEX_TEST_NAME = "Benchmark anti-Goodhart fixture bridge"
REQUIRED_THEOREMS = [
    "accepted_readiness_promotion_requires_transfer_negative_and_regression_records",
    "accepted_saturated_floor_requires_regression_records",
    "contaminated_review_cannot_promote_readiness",
]
LIFECYCLE_THEOREMS = {
    "ratchet_rejected_event_is_noninterfering",
    "ratchet_step_preserves_identity_and_authority",
    "ratchet_step_preserves_custody",
    "ratchet_custody_transitive",
    "run_ratchet_lifecycle_preserves_custody",
    "ratchet_step_preserves_stage_coherence",
    "run_ratchet_lifecycle_preserves_stage_coherence",
    "ratchet_accepted_step_adds_exactly_one_receipt",
    "accepted_ratchet_trace_accounts_for_every_event",
    "run_ratchet_lifecycle_append",
    "contaminated_decision_cannot_recommend_promotion",
    "saturated_decision_routes_to_regression_floor",
    "missing_transfer_check_rejected_noninterferingly",
    "missing_preserved_evidence_rejects_disposition",
    "clean_trace_reaches_closed_independent_review_candidate",
    "saturated_trace_reaches_closed_regression_floor",
    "contaminated_trace_quarantines_before_transfer",
    "closed_ratchet_is_absorbing",
    "quarantine_containment_survives_one_step",
    "quarantine_containment_survives_arbitrary_suffix",
    "clean_promotion_trace_is_accepted",
    "saturated_promotion_trace_is_accepted",
    "contaminated_quarantine_trace_is_accepted",
    "ratchet_decision_accepted_bool_iff",
    "aggregate_pass_count_cannot_identify_promotion_admissibility",
    "no_exact_aggregate_pass_count_promotion_classifier",
}
PROTECTED_FIELDS = (
    "instrument_digest",
    "dataset_version",
    "harness_version",
    "claim_digest",
    "authority_ceiling",
    "benchmark_saturated",
    "contamination_suspected",
    "transfer_or_mutation_check_present",
    "regression_records_preserved",
    "negative_results_preserved",
    "support_assignments",
    "external_effects",
)
CLEAN_TRACE = (
    "lock_baseline",
    "record_evaluation",
    "review_integrity",
    "review_transfer",
    "decide",
    "close",
)
ALL_EVENTS = CLEAN_TRACE
RETIRED_FIXTURE_THEOREMS = [
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


def build_expected_result(
    summary: dict[str, Any], semantic_depth: dict[str, Any]
) -> dict[str, Any]:
    return {
        "schema_version": "asi_stack.benchmark_antigoodhart_fixture_bridge.v0",
        "result_id": "2026-07-02-benchmark-antigoodhart-fixture-bridge",
        "recorded_date": "2026-07-02",
        "command": COMMAND,
        "input_fixture_dir": rel(FIXTURE_DIR),
        "result_kind": "synthetic_cross_record_fixture_bridge",
        "proof_bridge_type": "independent executable fixture with separate quantified Lean decision consequences",
        **summary,
        "semantic_depth_checks": semantic_depth,
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
        if not re.search(rf"\btheorem\s+{re.escape(theorem)}\b", text):
            errors.append(f"{rel(LEAN_FIXTURE)} missing theorem {theorem}.")
    for theorem in RETIRED_FIXTURE_THEOREMS:
        if re.search(rf"\btheorem\s+{re.escape(theorem)}\b", text):
            errors.append(f"{rel(LEAN_FIXTURE)} must keep copied fixture theorem {theorem} retired.")
    theorem_names = set(
        re.findall(r"(?m)^theorem\s+([A-Za-z_][A-Za-z0-9_']*)", text)
    )
    missing_lifecycle = sorted(LIFECYCLE_THEOREMS - theorem_names)
    if missing_lifecycle:
        errors.append(f"{rel(LEAN_FIXTURE)} missing lifecycle theorems {missing_lifecycle!r}.")
    if len(theorem_names) != 29:
        errors.append(
            f"{rel(LEAN_FIXTURE)} must contain exactly 29 theorem declarations, "
            f"found {len(theorem_names)}."
        )
    completed = subprocess.run(
        ["lake", "env", "lean", "AsiStackProofs/BenchmarkRatchets.lean"],
        cwd=LEAN_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        errors.append(
            "Lean benchmark-ratchet lifecycle did not compile: "
            + (completed.stdout + completed.stderr).strip()
        )


def reference_lifecycle_state() -> dict[str, Any]:
    return {
        "stage": "registered",
        "instrument_digest": 6101,
        "dataset_version": 6102,
        "harness_version": 6103,
        "claim_digest": 6104,
        "authority_ceiling": 1,
        "benchmark_saturated": False,
        "contamination_suspected": False,
        "transfer_or_mutation_check_present": True,
        "regression_records_preserved": True,
        "negative_results_preserved": True,
        "outcome": "none",
        "receipt_count": 0,
        "support_assignments": 0,
        "external_effects": 0,
    }


def lifecycle_step(state: dict[str, Any], event: str) -> tuple[str, dict[str, Any]]:
    next_state = dict(state)
    if event == "lock_baseline":
        if state["stage"] != "registered":
            return "reject_stage", dict(state)
        next_state["stage"] = "baseline_locked"
    elif event == "record_evaluation":
        if state["stage"] != "baseline_locked":
            return "reject_stage", dict(state)
        next_state["stage"] = "evaluation_recorded"
    elif event == "review_integrity":
        if state["stage"] != "evaluation_recorded":
            return "reject_stage", dict(state)
        if state["contamination_suspected"]:
            next_state["stage"] = "dispositioned"
            next_state["outcome"] = "quarantine"
        else:
            next_state["stage"] = "integrity_reviewed"
    elif event == "review_transfer":
        if state["stage"] != "integrity_reviewed":
            return "reject_stage", dict(state)
        if not state["transfer_or_mutation_check_present"]:
            return "reject_evidence", dict(state)
        next_state["stage"] = "transfer_reviewed"
    elif event == "decide":
        if state["stage"] != "transfer_reviewed":
            return "reject_stage", dict(state)
        if state["contamination_suspected"]:
            next_state["outcome"] = "quarantine"
        elif not state["regression_records_preserved"] or not state["negative_results_preserved"]:
            return "reject_evidence", dict(state)
        elif state["benchmark_saturated"]:
            next_state["outcome"] = "regression_floor"
        else:
            next_state["outcome"] = "independent_review_candidate"
        next_state["stage"] = "dispositioned"
    elif event == "close":
        if state["stage"] != "dispositioned":
            return "reject_stage", dict(state)
        next_state["stage"] = "closed"
    else:
        raise ValueError(f"unknown ratchet event {event}")
    next_state["receipt_count"] += 1
    return "accepted", next_state


def run_lifecycle(state: dict[str, Any], events: tuple[str, ...]) -> dict[str, Any]:
    current = dict(state)
    for event in events:
        _, current = lifecycle_step(current, event)
    return current


def stage_coherent(state: dict[str, Any]) -> bool:
    pending = {
        "registered",
        "baseline_locked",
        "evaluation_recorded",
        "integrity_reviewed",
        "transfer_reviewed",
    }
    if state["stage"] in pending:
        return state["outcome"] == "none"
    if state["stage"] in {"dispositioned", "closed"}:
        return state["outcome"] != "none"
    return False


def quarantine_contained(state: dict[str, Any]) -> bool:
    return (
        state["stage"] in {"dispositioned", "closed"}
        and state["outcome"] == "quarantine"
    )


def semantic_state_errors(
    origin: dict[str, Any], current: dict[str, Any]
) -> list[str]:
    errors: list[str] = []
    if not stage_coherent(current):
        errors.append("stage/outcome incoherent")
    for field in PROTECTED_FIELDS:
        if current[field] != origin[field]:
            errors.append(f"custody changed: {field}")
    return errors


def aggregate_pass_count(review: dict[str, bool]) -> int:
    return sum(
        (
            review["benchmark_saturated"],
            not review["contamination_suspected"],
            review["transfer_or_mutation_check_present"],
            review["regression_records_preserved"],
            review["negative_results_preserved"],
        )
    )


def promotion_accepted(review: dict[str, bool]) -> bool:
    return (
        review["regression_records_preserved"]
        and review["transfer_or_mutation_check_present"]
        and review["negative_results_preserved"]
        and not review["contamination_suspected"]
    )


def validate_semantic_depth(errors: list[str]) -> dict[str, Any]:
    roots = {
        "clean": reference_lifecycle_state(),
        "saturated": {
            **reference_lifecycle_state(),
            "benchmark_saturated": True,
        },
        "contaminated": {
            **reference_lifecycle_state(),
            "contamination_suspected": True,
        },
    }
    reachable_state_count = 0
    transition_check_count = 0
    quarantine_suffix_check_count = 0
    for root_name, root in roots.items():
        seen = {tuple(sorted(root.items()))}
        frontier = [root]
        for _ in range(7):
            next_frontier: dict[tuple[tuple[str, Any], ...], dict[str, Any]] = {}
            for state in frontier:
                for event in ALL_EVENTS:
                    route, next_state = lifecycle_step(state, event)
                    transition_check_count += 1
                    for defect in semantic_state_errors(root, next_state):
                        errors.append(f"{root_name}/{event}: {defect}")
                    if route == "accepted":
                        if next_state["receipt_count"] != state["receipt_count"] + 1:
                            errors.append(f"{root_name}/{event}: accepted receipt drift")
                    elif next_state != state:
                        errors.append(f"{root_name}/{event}: rejected transition interfered")
                    if quarantine_contained(state):
                        quarantine_suffix_check_count += 1
                        if not quarantine_contained(next_state):
                            errors.append(f"{root_name}/{event}: quarantine escaped")
                    key = tuple(sorted(next_state.items()))
                    if key not in seen:
                        seen.add(key)
                        next_frontier[key] = next_state
            frontier = list(next_frontier.values())
        reachable_state_count += len(seen)

    semantic_mutations = [
        {"stage": "registered", "outcome": "independent_review_candidate"},
        {"stage": "closed", "outcome": "none"},
        {"instrument_digest": 9991},
        {"dataset_version": 9992},
        {"harness_version": 9993},
        {"claim_digest": 9994},
        {"authority_ceiling": 2},
        {"transfer_or_mutation_check_present": False},
        {"negative_results_preserved": False},
        {"support_assignments": 1},
        {"external_effects": 1},
    ]
    semantic_mutations_rejected = 0
    for mutation in semantic_mutations:
        candidate = {**roots["clean"], **mutation}
        if semantic_state_errors(roots["clean"], candidate):
            semantic_mutations_rejected += 1
        else:
            errors.append(f"semantic mutation accepted: {mutation}")

    review_fields = (
        "benchmark_saturated",
        "contamination_suspected",
        "transfer_or_mutation_check_present",
        "regression_records_preserved",
        "negative_results_preserved",
    )
    buckets: dict[int, set[bool]] = {}
    for values in product((False, True), repeat=len(review_fields)):
        review = dict(zip(review_fields, values, strict=True))
        buckets.setdefault(aggregate_pass_count(review), set()).add(
            promotion_accepted(review)
        )
    collision_scores = sorted(score for score, decisions in buckets.items() if len(decisions) > 1)
    if collision_scores != [4]:
        errors.append(f"aggregate promotion collision scores drifted: {collision_scores}")

    return {
        "lean_theorem_count": 29,
        "exploration_depth": 7,
        "root_state_count": len(roots),
        "reachable_state_count": reachable_state_count,
        "transition_check_count": transition_check_count,
        "quarantine_suffix_check_count": quarantine_suffix_check_count,
        "semantic_mutations_rejected": semantic_mutations_rejected,
        "aggregate_review_count": 32,
        "aggregate_collision_scores": collision_scores,
        "exact_aggregate_classifier_exists": False,
    }


def validate_lifecycle(errors: list[str]) -> tuple[int, int, int]:
    baseline = reference_lifecycle_state()
    current = dict(baseline)
    accepted_count = 0
    for event in CLEAN_TRACE:
        route, next_state = lifecycle_step(current, event)
        if route != "accepted":
            errors.append(f"clean benchmark lifecycle event {event} returned {route}")
        else:
            accepted_count += 1
        for field in PROTECTED_FIELDS:
            if next_state[field] != current[field]:
                errors.append(f"clean benchmark lifecycle event {event} changed {field}")
        if route == "accepted" and next_state["receipt_count"] != current["receipt_count"] + 1:
            errors.append(f"clean benchmark lifecycle event {event} did not add one receipt")
        current = next_state
    if current["stage"] != "closed" or current["outcome"] != "independent_review_candidate":
        errors.append("clean benchmark lifecycle did not close with an independent-review candidate")
    for split in range(len(CLEAN_TRACE) + 1):
        left = run_lifecycle(baseline, CLEAN_TRACE[:split])
        if run_lifecycle(left, CLEAN_TRACE[split:]) != current:
            errors.append(f"benchmark lifecycle composition failed at split {split}")

    saturated = reference_lifecycle_state()
    saturated["benchmark_saturated"] = True
    saturated_final = run_lifecycle(saturated, CLEAN_TRACE)
    if saturated_final["outcome"] != "regression_floor" or saturated_final["receipt_count"] != 6:
        errors.append("saturated benchmark did not close as a regression floor")

    contaminated = reference_lifecycle_state()
    contaminated["contamination_suspected"] = True
    contaminated_trace = ("lock_baseline", "record_evaluation", "review_integrity", "close")
    contaminated_final = run_lifecycle(contaminated, contaminated_trace)
    if contaminated_final["outcome"] != "quarantine" or contaminated_final["receipt_count"] != 4:
        errors.append("contaminated benchmark did not quarantine before transfer review")

    def changed(**updates: Any) -> dict[str, Any]:
        state = reference_lifecycle_state()
        state.update(updates)
        return state

    mutations = [
        ("lock wrong stage", "lock_baseline", changed(stage="baseline_locked"), "reject_stage"),
        ("record wrong stage", "record_evaluation", changed(), "reject_stage"),
        ("integrity wrong stage", "review_integrity", changed(), "reject_stage"),
        ("transfer wrong stage", "review_transfer", changed(), "reject_stage"),
        ("missing transfer evidence", "review_transfer", changed(stage="integrity_reviewed", transfer_or_mutation_check_present=False), "reject_evidence"),
        ("decision wrong stage", "decide", changed(), "reject_stage"),
        ("missing regression records", "decide", changed(stage="transfer_reviewed", regression_records_preserved=False), "reject_evidence"),
        ("missing negative results", "decide", changed(stage="transfer_reviewed", negative_results_preserved=False), "reject_evidence"),
        ("close wrong stage", "close", changed(), "reject_stage"),
    ]
    closed = changed(stage="closed", outcome="independent_review_candidate", receipt_count=6)
    mutations.extend(
        (f"closed absorbs {event}", event, closed, "reject_stage")
        for event in CLEAN_TRACE
    )
    rejected_count = 0
    for name, event, state, expected_route in mutations:
        route, next_state = lifecycle_step(state, event)
        if route != expected_route:
            errors.append(f"benchmark lifecycle mutation {name} expected {expected_route}, got {route}")
        elif next_state != state:
            errors.append(f"benchmark lifecycle mutation {name} changed state on rejection")
        else:
            rejected_count += 1
    return accepted_count, len(CLEAN_TRACE) + 1, rejected_count


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
            "independent executable fixture with separate quantified Lean decision consequences",
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
        VALIDATION_REGISTRY: [
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

    errors: list[str] = []
    summary = validate_fixture_semantics()
    semantic_depth = validate_semantic_depth(errors)
    expected = build_expected_result(summary, semantic_depth)
    validate_result(expected, args.write_result, errors)
    validate_lean_fixture(errors)
    accepted_count, split_count, rejected_count = validate_lifecycle(errors)
    validate_surfaces(errors)
    if errors:
        fail(errors)
    print(
        "Benchmark fixture bridge validation passed: "
        f"{summary['valid_fixture_count']} valid fixture(s), "
        f"{summary['expected_invalid_fixture_count']} expected-invalid fixture(s), "
        f"29 Lean declarations, {accepted_count} accepted clean transitions, "
        f"{split_count}/{split_count} trace splits, saturated-floor and "
        f"contamination-quarantine witnesses, and {rejected_count}/15 rejecting "
        f"lifecycle mutations; {semantic_depth['reachable_state_count']} reachable "
        f"states, {semantic_depth['transition_check_count']} transition checks, "
        f"{semantic_depth['quarantine_suffix_check_count']} quarantine suffix checks, "
        f"{semantic_depth['semantic_mutations_rejected']} semantic mutations, and "
        "one aggregate-score collision class checked; executable fixture and finite "
        "decision boundary aligned."
    )


if __name__ == "__main__":
    main()
