#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import re
import sys
from typing import Any

from run_resource_flagship_lane import (
    COMMANDS,
    NON_CLAIMS,
    NO_PROMOTION_DECISION_REFS,
    RESIDUALS,
    RESULT,
    RESULT_COMMAND,
    ROOT,
    RUN_ID,
    SUBLANE_NO_PROMOTION_DECISION_REFS,
    TRACKED_ARTIFACTS,
    artifact_stat,
    build_component_summary,
    run_command,
)


DOC = ROOT / "docs" / "resource_flagship_lane_run.md"
LEAN_FIXTURE = ROOT / "lean" / "AsiStackProofs" / "ResourceEconomics.lean"
SHA_RE = re.compile(r"^[0-9a-f]{64}$")
REQUIRED_NON_CLAIM_TERMS = (
    "does not promote the Resource Economics chapter core claim",
    "does not create a new support-state transition",
    "does not prove deployed scheduler behavior",
    "not external review",
)
REQUIRED_AGGREGATE_THEOREMS = (
    "resource_flagship_lane_aggregate_fixture_valid",
    "resource_flagship_lane_aggregate_preserves_no_core_promotion",
    "resource_flagship_lane_aggregate_carries_transition_accounting",
)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Resource flagship lane validation failed:")
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


def validate_record_shape(value: dict[str, Any], errors: list[str]) -> None:
    expected = {
        "schema_version": "0.1",
        "run_id": RUN_ID,
        "record_kind": "resource_flagship_lane_replay",
        "command": RESULT_COMMAND,
        "local_only": True,
        "public_safe": True,
        "pass": True,
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
    }
    for key, expected_value in expected.items():
        if value.get(key) != expected_value:
            errors.append(f"{rel(RESULT)}: {key} must be {expected_value!r}.")
    timestamp = value.get("recorded_at_utc")
    if not isinstance(timestamp, str) or not timestamp.endswith("Z"):
        errors.append(f"{rel(RESULT)}: recorded_at_utc must be a UTC timestamp ending in Z.")
    summary = value.get("summary")
    if not isinstance(summary, str) or "One-command Resource Economics flagship lane replay" not in summary:
        errors.append(f"{rel(RESULT)}: summary must describe the one-command Resource Economics lane.")
    if value.get("residuals") != RESIDUALS:
        errors.append(f"{rel(RESULT)}: residuals must match the runner residual list.")
    if value.get("non_claims") != NON_CLAIMS:
        errors.append(f"{rel(RESULT)}: non_claims must match the runner non-claim list.")
    non_claim_text = text_blob(value.get("non_claims"))
    for term in REQUIRED_NON_CLAIM_TERMS:
        if term.lower() not in non_claim_text:
            errors.append(f"{rel(RESULT)}: non_claims missing boundary phrase {term!r}.")
    if value.get("accepted_transition_refs") != [
        "evidence_transitions/v1_0_measured/costed_route_resource_slice_synthetic_test_backed.json",
        "evidence_transitions/v1_x_measured/resource_load_stability_selector_synthetic_test_backed.json",
        "evidence_transitions/v1_x_measured/resource_workload_quality_selector_empirical_test_backed.json",
    ]:
        errors.append(f"{rel(RESULT)}: accepted_transition_refs must name the bounded Resource transitions.")
    if value.get("no_promotion_decision_refs") != NO_PROMOTION_DECISION_REFS:
        errors.append(
            f"{rel(RESULT)}: no_promotion_decision_refs must name the Resource Economics core and sublane decisions."
        )


def validate_commands(value: dict[str, Any], errors: list[str]) -> None:
    records = value.get("command_records")
    if not isinstance(records, list):
        errors.append(f"{rel(RESULT)}: command_records must be a list.")
        return
    if len(records) != len(COMMANDS):
        errors.append(f"{rel(RESULT)}: expected {len(COMMANDS)} command records, found {len(records)}.")
        return
    for index, (expected, recorded) in enumerate(zip(COMMANDS, records)):
        owner = f"{rel(RESULT)}:command_records[{index}]"
        if not isinstance(recorded, dict):
            errors.append(f"{owner}: command record must be an object.")
            continue
        for key in ("id", "command", "role"):
            if recorded.get(key) != expected[key]:
                errors.append(f"{owner}: {key} must be {expected[key]!r}.")
        if recorded.get("exit_code") != 0:
            errors.append(f"{owner}: exit_code must be 0.")
        if not isinstance(recorded.get("elapsed_ms"), (int, float)) or recorded["elapsed_ms"] <= 0:
            errors.append(f"{owner}: elapsed_ms must be a positive number.")
        digest = recorded.get("output_sha256")
        if not isinstance(digest, str) or not SHA_RE.match(digest):
            errors.append(f"{owner}: output_sha256 must be a SHA-256 hex digest.")
        if not isinstance(recorded.get("output_excerpt"), list) or not recorded["output_excerpt"]:
            errors.append(f"{owner}: output_excerpt must be a non-empty list.")
        replayed = run_command(expected)
        if replayed["exit_code"] != 0:
            errors.append(f"{owner}: current replay of {expected['command']} failed.")
        if replayed["output_sha256"] != digest:
            errors.append(f"{owner}: current replay output digest differs from recorded digest.")


def validate_component_summary(value: dict[str, Any], errors: list[str]) -> None:
    recorded = value.get("component_summary")
    if not isinstance(recorded, dict):
        errors.append(f"{rel(RESULT)}: component_summary must be an object.")
        return
    current = build_component_summary()
    if recorded != current:
        errors.append(f"{rel(RESULT)}: component_summary must match current tracked Resource evidence artifacts.")
        return

    accepted = recorded.get("accepted_non_core_transition", {})
    if accepted.get("claim_id") != "resource-economics.costed_route_budget_slice":
        errors.append(f"{rel(RESULT)}: accepted transition must stay scoped to the non-core costed-route claim.")
    if accepted.get("new_support_state") != "synthetic-test-backed":
        errors.append(f"{rel(RESULT)}: accepted transition must remain synthetic-test-backed.")
    if accepted.get("cost_reduction_vs_baseline_percent") != 66.98:
        errors.append(f"{rel(RESULT)}: costed-route reduction percent must remain 66.98.")

    load_transition = recorded.get("load_stability_accepted_transition", {})
    if load_transition.get("claim_id") != "resource-economics.finite_burst_load_smoothing_selector":
        errors.append(f"{rel(RESULT)}: load-stability transition must stay scoped to the finite selector claim.")
    if load_transition.get("new_support_state") != "synthetic-test-backed":
        errors.append(f"{rel(RESULT)}: load-stability transition must be synthetic-test-backed.")
    if load_transition.get("support_state_effect") != "eligible_for_bounded_evidence_review":
        errors.append(f"{rel(RESULT)}: load-stability transition support effect must stay bounded.")
    if load_transition.get("selected_route_id") != "route://selected-protected-capacity-smoothing":
        errors.append(f"{rel(RESULT)}: load-stability transition selected route mismatch.")

    workload_transition = recorded.get("workload_quality_accepted_transition", {})
    if workload_transition.get("claim_id") != "resource-economics.scoped_workflow_trace_route_selector":
        errors.append(f"{rel(RESULT)}: workload-quality transition must stay scoped to the local selector claim.")
    if workload_transition.get("new_support_state") != "empirical-test-backed":
        errors.append(f"{rel(RESULT)}: workload-quality transition must be empirical-test-backed.")
    if workload_transition.get("support_state_effect") != "eligible_for_bounded_evidence_review":
        errors.append(f"{rel(RESULT)}: workload-quality transition support effect must stay bounded.")
    if workload_transition.get("selected_route_id") != "route://selected-scoped-workflow-trace-validator":
        errors.append(f"{rel(RESULT)}: workload-quality transition selected route mismatch.")

    core = recorded.get("chapter_core_decision", {})
    if core.get("claim_id") != "resource-economics-and-token-budgets.core":
        errors.append(f"{rel(RESULT)}: chapter-core decision must reference Resource Economics core claim.")
    if core.get("transition_effect") != "no_change":
        errors.append(f"{rel(RESULT)}: chapter-core decision must remain no_change.")

    ci_profile = recorded.get("ci_cost_profile", {})
    ci_metrics = ci_profile.get("metrics", {}) if isinstance(ci_profile.get("metrics"), dict) else {}
    if ci_profile.get("lean_bridge") != "finite CI failure-classification summary":
        errors.append(f"{rel(RESULT)}: CI cost profile must expose the finite Lean classifier bridge.")
    if ci_profile.get("deploy_service_failure_count") != ci_metrics.get("failure_count"):
        errors.append(f"{rel(RESULT)}: CI deploy-service failures must account for all recorded failures.")
    if ci_profile.get("recovery_run_seconds") != 131:
        errors.append(f"{rel(RESULT)}: CI recovery boundary must remain the 131-second run in this profile.")
    if ci_profile.get("support_state_effect") != "none":
        errors.append(f"{rel(RESULT)}: CI cost profile support_state_effect must remain none.")

    workload = recorded.get("workload_quality_probe", {})
    if workload.get("negative_control_rejected") is not True:
        errors.append(f"{rel(RESULT)}: workload-quality negative control must be rejected.")
    if workload.get("selected_elapsed_ms", 0) >= workload.get("baseline_elapsed_ms", 0):
        errors.append(f"{rel(RESULT)}: selected workload route must remain cheaper than baseline in the recorded result.")
    if workload.get("negative_control_elapsed_ms", 0) >= workload.get("selected_elapsed_ms", 0):
        errors.append(f"{rel(RESULT)}: negative workload route should remain cheaper but invalid.")

    load = recorded.get("load_stability_probe", {})
    if load.get("selected_load_instability_units") != 0:
        errors.append(f"{rel(RESULT)}: selected load-stability route must record zero instability units.")
    if load.get("baseline_load_instability_units", 0) <= load.get("selected_load_instability_units", 0):
        errors.append(f"{rel(RESULT)}: selected load-stability route must reduce baseline instability.")
    if load.get("negative_protected_review_violation_count", 0) <= 0:
        errors.append(f"{rel(RESULT)}: load-stability negative control must expose protected-review violations.")

    decisions = recorded.get("sublane_no_promotion_decisions", {})
    expected_decision_ids = {
        "resource_workflow_trace_no_change",
        "resource_live_probe_no_change",
        "resource_workload_quality_probe_no_change",
        "resource_load_stability_probe_no_change",
        "resource_ci_cost_profile_no_change",
    }
    if set(decisions) != expected_decision_ids:
        errors.append(f"{rel(RESULT)}: sublane_no_promotion_decisions mismatch: {sorted(decisions)}.")
    for decision_id, decision in decisions.items():
        if decision.get("transition_effect") != "no_change":
            errors.append(f"{rel(RESULT)}:{decision_id}: transition_effect must remain no_change.")
        if decision.get("support_state_effect") != "blocks_promotion":
            errors.append(f"{rel(RESULT)}:{decision_id}: support_state_effect must remain blocks_promotion.")
        if decision.get("verification_result") != "pass":
            errors.append(f"{rel(RESULT)}:{decision_id}: verification_result must remain pass.")
        if decision.get("transition_validity_state") != "review_accepted":
            errors.append(f"{rel(RESULT)}:{decision_id}: transition_validity_state must remain review_accepted.")


def negative_controls_preserved(summary: dict[str, Any]) -> bool:
    accepted = summary.get("accepted_non_core_transition", {})
    workload = summary.get("workload_quality_probe", {})
    load = summary.get("load_stability_probe", {})
    workflow = summary.get("workflow_trace", {})
    return (
        accepted.get("negative_control_routes")
        == ["route://cheap-unverified-transform", "route://hidden-residual-auto-merge"]
        and workload.get("negative_control_rejected") is True
        and load.get("negative_protected_review_violation_count", 0) > 0
        and workflow.get("expected_invalid_fixture_count") == 5
    )


def validate_aggregate_lean_alignment(value: dict[str, Any], errors: list[str]) -> None:
    alignment = value.get("aggregate_lean_alignment")
    if not isinstance(alignment, dict):
        errors.append(f"{rel(RESULT)}: aggregate_lean_alignment must be an object.")
        return

    summary = value.get("component_summary")
    if not isinstance(summary, dict):
        errors.append(f"{rel(RESULT)}: component_summary is required before aggregate alignment can be checked.")
        return
    core = summary.get("chapter_core_decision", {})
    expected = {
        "proof_bridge_type": "aggregate Python/Lean flagship invariant",
        "lean_module": "AsiStackProofs.ResourceEconomics",
        "lean_fixture": "resourceFlagshipLaneAggregateFixture",
        "lean_theorem_names": list(REQUIRED_AGGREGATE_THEOREMS),
        "command_replay_count": len(COMMANDS),
        "tracked_artifact_count": len(TRACKED_ARTIFACTS),
        "accepted_transition_count": len(value.get("accepted_transition_refs", [])),
        "sublane_no_promotion_decision_count": len(SUBLANE_NO_PROMOTION_DECISION_REFS),
        "chapter_core_no_change": core.get("transition_effect") == "no_change",
        "evidence_transition_created": value.get("evidence_transition_created"),
        "support_state_effect_none": value.get("support_state_effect") == "none",
        "chapter_core_support_effect_none": value.get("chapter_core_support_effect") == "none",
        "negative_controls_preserved": negative_controls_preserved(summary),
        "residuals_recorded": len(value.get("residuals", [])) == len(RESIDUALS),
        "non_claim_boundary": all(
            term.lower() in text_blob(value.get("non_claims"))
            for term in REQUIRED_NON_CLAIM_TERMS
        ),
    }
    for key, expected_value in expected.items():
        if alignment.get(key) != expected_value:
            errors.append(f"{rel(RESULT)}: aggregate_lean_alignment.{key} must be {expected_value!r}.")

    non_claims = alignment.get("non_claims")
    non_claim_text = text_blob(non_claims)
    for term in ("finite-record accounting", "does not prove deployed scheduler behavior", "chapter-core support-state promotion"):
        if term not in non_claim_text:
            errors.append(f"{rel(RESULT)}: aggregate_lean_alignment non_claims missing {term!r}.")

    if not LEAN_FIXTURE.exists():
        errors.append(f"Missing {rel(LEAN_FIXTURE)}.")
        return
    lean_text = LEAN_FIXTURE.read_text(encoding="utf-8")
    for theorem in REQUIRED_AGGREGATE_THEOREMS:
        if not re.search(rf"^theorem\s+{re.escape(theorem)}\b", lean_text, flags=re.MULTILINE):
            errors.append(f"{rel(LEAN_FIXTURE)} missing theorem {theorem}.")
    for fragment in (
        "structure FlagshipLaneAggregateSummary",
        "def resourceFlagshipLaneAggregateFixture",
        "commandReplayCount := 10",
        "trackedArtifactCount := 26",
        "acceptedTransitionCount := 3",
        "sublaneNoPromotionDecisionCount := 5",
        "chapterCoreNoChange := true",
        "evidenceTransitionCreated := false",
        "supportStateEffectNone := true",
        "chapterCoreSupportEffectNone := true",
        "negativeControlsPreserved := true",
        "residualsRecorded := true",
        "nonClaimBoundary := true",
    ):
        if fragment not in lean_text:
            errors.append(f"{rel(LEAN_FIXTURE)} missing aggregate fixture fragment {fragment!r}.")


def validate_artifacts(value: dict[str, Any], errors: list[str]) -> None:
    expected_refs = [*TRACKED_ARTIFACTS, rel(RESULT)]
    if value.get("artifact_refs") != expected_refs:
        errors.append(f"{rel(RESULT)}: artifact_refs must match the flagship tracked artifact list.")
    for relative in expected_refs:
        if not (ROOT / relative).exists():
            errors.append(f"{rel(RESULT)}: referenced artifact does not exist: {relative}.")

    tracked = value.get("tracked_artifacts")
    if not isinstance(tracked, list):
        errors.append(f"{rel(RESULT)}: tracked_artifacts must be a list.")
        return
    if len(tracked) != len(TRACKED_ARTIFACTS):
        errors.append(f"{rel(RESULT)}: expected {len(TRACKED_ARTIFACTS)} tracked artifact stats, found {len(tracked)}.")
        return
    for index, (relative, recorded) in enumerate(zip(TRACKED_ARTIFACTS, tracked)):
        owner = f"{rel(RESULT)}:tracked_artifacts[{index}]"
        if not isinstance(recorded, dict):
            errors.append(f"{owner}: tracked artifact record must be an object.")
            continue
        current = artifact_stat(relative)
        if recorded != current:
            errors.append(f"{owner}: artifact stat must match current {relative}.")
        if not SHA_RE.match(str(recorded.get("sha256", ""))):
            errors.append(f"{owner}: sha256 must be a SHA-256 digest.")


def validate_doc(errors: list[str]) -> None:
    if not DOC.exists():
        errors.append(f"Missing {rel(DOC)}.")
        return
    text = DOC.read_text(encoding="utf-8")
    required = [
        "Resource Flagship Lane Run",
        RESULT_COMMAND,
        rel(RESULT),
        "resource-economics.costed_route_budget_slice",
        "resource-economics.finite_burst_load_smoothing_selector",
        "resource-economics.scoped_workflow_trace_route_selector",
        "resource-economics-and-token-budgets.core",
        "route://bounded-transform-plus-verifier",
        "route://selected-scoped-workflow-trace-validator",
        "route://selected-protected-capacity-smoothing",
        "Sublane No-Promotion Decisions",
        "resource-economics.local_workload_quality_route_selection",
        "resource-economics.synthetic_load_stability_route_selection",
        "aggregate Python/Lean flagship invariant",
        "resourceFlagshipLaneAggregateFixture",
        "CI Classifier Lean Alignment",
        "finite CI failure-classification summary",
        "resourceCICostProfileFixture",
        "Support-state effect: `none`",
        "This run does not promote the Resource Economics chapter core claim",
    ]
    for fragment in required:
        if fragment not in text:
            errors.append(f"{rel(DOC)} missing required fragment: {fragment}")


def main() -> None:
    errors: list[str] = []
    if not RESULT.exists():
        fail([f"Missing {rel(RESULT)}. Run `{RESULT_COMMAND}` first."])
    value = load_json(RESULT)
    if not isinstance(value, dict):
        fail([f"{rel(RESULT)} must contain a JSON object."])

    validate_record_shape(value, errors)
    validate_commands(value, errors)
    validate_component_summary(value, errors)
    validate_aggregate_lean_alignment(value, errors)
    validate_artifacts(value, errors)
    validate_doc(errors)

    if errors:
        fail(errors)
    print(
        "Resource flagship lane validation passed: "
        f"{len(COMMANDS)} command replay(s), {len(TRACKED_ARTIFACTS)} tracked artifact digest(s), "
        "support-state effect none."
    )


if __name__ == "__main__":
    main()
