#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from validate_book import validate_schema_value


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "experiments" / "policy_update_lease" / "results" / "2026-07-02-local.json"
DOC = ROOT / "docs" / "policy_update_lease_probe.md"
CHAPTER = ROOT / "chapters" / "policy-optimization-and-learning-from-feedback.qmd"
READER = (
    ROOT
    / "editions"
    / "reader_manuscript"
    / "v1_0"
    / "chapters"
    / "policy-optimization-and-learning-from-feedback.qmd"
)
OUTLINE = ROOT / "docs" / "book_outline.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
CHANGELOG = ROOT / "appendices" / "F_changelog.qmd"
MANIFEST = ROOT / "book_structure.json"
VALIDATION_REGISTRY = ROOT / "validation" / "registry.json"
LEAN_FILE = ROOT / "lean" / "AsiStackProofs" / "PolicyOptimization.lean"

COMMAND = "python3 scripts/validate_policy_update_lease_probe.py"
PROOF_TAG = "lean:policy_optimization.lease_probe_fixture_bridge"
CODEX_TEST_NAME = "Policy update lease probe"
REQUIRED_THEOREMS = [
    "policy_update_lease_probe_fixture_valid",
    "policy_update_lease_probe_rejects_reward_only_proxy",
    "policy_update_lease_probe_preserves_rollback_boundary",
]
REQUIRED_NON_CLAIMS = [
    "does not run PPO, DPO, GRPO, RLVR, or any optimizer",
    "does not prove policy improvement, reward quality, or route quality",
    "does not execute a deployed canary or live rollback",
    "does not promote the Policy Optimization chapter core claim",
    "does not create a support-state transition",
]

WORKLOAD = [
    {
        "sample_id": "sample://routine-source-grounded-summary",
        "risk_class": "low",
        "requires_source_grounding": True,
        "requires_human_approval": False,
        "holdout": False,
    },
    {
        "sample_id": "sample://ambiguous-high-risk-approval",
        "risk_class": "high",
        "requires_source_grounding": True,
        "requires_human_approval": True,
        "holdout": True,
    },
    {
        "sample_id": "sample://fast-local-formatting-task",
        "risk_class": "low",
        "requires_source_grounding": False,
        "requires_human_approval": False,
        "holdout": False,
    },
    {
        "sample_id": "sample://medical-advice-boundary",
        "risk_class": "high",
        "requires_source_grounding": True,
        "requires_human_approval": True,
        "holdout": True,
    },
    {
        "sample_id": "sample://citation-sensitive-claim",
        "risk_class": "medium",
        "requires_source_grounding": True,
        "requires_human_approval": False,
        "holdout": False,
    },
    {
        "sample_id": "sample://cheap-answer-negative-control",
        "risk_class": "medium",
        "requires_source_grounding": True,
        "requires_human_approval": False,
        "holdout": False,
    },
]

CANDIDATES = [
    {
        "policy_ref": "policy://router-v0-baseline",
        "role": "baseline",
        "feedback_admissible": True,
        "target_evaluation_refs_present": True,
        "holdout_refs_present": True,
        "contamination_check_present": True,
        "reward_hacking_probe_passed": True,
        "governance_gate_refs_present": True,
        "authority_effect": "unchanged",
        "rollback_plan_present": True,
        "regressions_preserved": True,
        "residuals_recorded": True,
        "proxy_used_as_sole_evidence": False,
        "synthetic_score": 8,
    },
    {
        "policy_ref": "policy://router-v1-source-grounded-canary",
        "role": "selected_canary",
        "feedback_admissible": True,
        "target_evaluation_refs_present": True,
        "holdout_refs_present": True,
        "contamination_check_present": True,
        "reward_hacking_probe_passed": True,
        "governance_gate_refs_present": True,
        "authority_effect": "unchanged",
        "rollback_plan_present": True,
        "regressions_preserved": True,
        "residuals_recorded": True,
        "proxy_used_as_sole_evidence": False,
        "synthetic_score": 11,
    },
    {
        "policy_ref": "policy://router-v1-reward-only-fast-route",
        "role": "expected_invalid_reward_only_proxy",
        "feedback_admissible": True,
        "target_evaluation_refs_present": False,
        "holdout_refs_present": False,
        "contamination_check_present": True,
        "reward_hacking_probe_passed": False,
        "governance_gate_refs_present": True,
        "authority_effect": "unchanged",
        "rollback_plan_present": True,
        "regressions_preserved": False,
        "residuals_recorded": True,
        "proxy_used_as_sole_evidence": True,
        "synthetic_score": 14,
    },
    {
        "policy_ref": "policy://router-v1-authority-expanding-route",
        "role": "expected_invalid_authority_expansion",
        "feedback_admissible": True,
        "target_evaluation_refs_present": True,
        "holdout_refs_present": True,
        "contamination_check_present": True,
        "reward_hacking_probe_passed": True,
        "governance_gate_refs_present": False,
        "authority_effect": "requires_review",
        "rollback_plan_present": True,
        "regressions_preserved": True,
        "residuals_recorded": True,
        "proxy_used_as_sole_evidence": False,
        "synthetic_score": 12,
    },
    {
        "policy_ref": "policy://router-v1-missing-rollback-route",
        "role": "expected_invalid_missing_rollback",
        "feedback_admissible": True,
        "target_evaluation_refs_present": True,
        "holdout_refs_present": True,
        "contamination_check_present": True,
        "reward_hacking_probe_passed": True,
        "governance_gate_refs_present": True,
        "authority_effect": "unchanged",
        "rollback_plan_present": False,
        "regressions_preserved": True,
        "residuals_recorded": True,
        "proxy_used_as_sole_evidence": False,
        "synthetic_score": 13,
    },
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Policy update lease probe validation failed:")
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


def candidate_is_lease_eligible(candidate: dict[str, Any]) -> bool:
    return (
        candidate["feedback_admissible"] is True
        and candidate["target_evaluation_refs_present"] is True
        and candidate["holdout_refs_present"] is True
        and candidate["contamination_check_present"] is True
        and candidate["reward_hacking_probe_passed"] is True
        and candidate["governance_gate_refs_present"] is True
        and candidate["authority_effect"] == "unchanged"
        and candidate["rollback_plan_present"] is True
        and candidate["regressions_preserved"] is True
        and candidate["residuals_recorded"] is True
        and candidate["proxy_used_as_sole_evidence"] is False
    )


def build_policy_record() -> dict[str, Any]:
    return {
        "update_id": "policy-update-lease-probe-2026-07-02",
        "update_state": "canary",
        "target_layer": "router",
        "policy_ref": "policy://router-v1-source-grounded-canary",
        "policy_delta_summary": (
            "Synthetic router-policy lease keeps source-grounded tasks on the "
            "grounded route and preserves approval-first handling for high-risk tasks."
        ),
        "training_mode": "not_run",
        "feedback_source": "synthetic router-policy lease fixture",
        "feedback_admissibility": "admissible_for_canary",
        "reward_or_preference_signal": "toy score over six synthetic routing samples",
        "reward_boundary": (
            "The score cannot stand in for route quality, policy improvement, "
            "authority, verifier quality, or deployment readiness."
        ),
        "verifier_refs": [
            "validator://validate_policy_update_lease_probe.route-boundary",
            "validator://validate_policy_update_lease_probe.rollback-dry-run",
        ],
        "reward_hacking_probes": [
            "probe://reward-only-fast-route-rejected",
            "probe://authority-expanding-route-rejected",
            "probe://missing-rollback-route-rejected",
        ],
        "update_constraint": "synthetic canary lease only; no optimizer, weights, or live router changed",
        "drift_bound": "candidate must preserve source-grounding, approval, governance, and rollback fields",
        "holdout_refs": [
            "sample://ambiguous-high-risk-approval",
            "sample://medical-advice-boundary",
        ],
        "regression_refs": [
            "sample://routine-source-grounded-summary",
            "sample://citation-sensitive-claim",
        ],
        "evaluation_refs": [
            "experiments/policy_update_lease/results/2026-07-02-local.json",
        ],
        "governance_gate_refs": [
            "scf://policy-update-lease-no-promotion",
        ],
        "authority_effect": "unchanged",
        "rollback_plan": (
            "Dry-run rollback restores policy://router-v0-baseline when the synthetic "
            "monitor injection trips the rollback condition."
        ),
        "monitor_window": "synthetic six-sample canary window plus one injected rollback event",
        "evidence_packet_refs": [
            "docs/policy_update_lease_probe.md",
            "experiments/policy_update_lease/results/2026-07-02-local.json",
        ],
        "deployment_scope": "none; local deterministic fixture only",
        "promotion_decision": "keep_experimental",
        "measurement_status": "run",
        "support_state_effect": "none",
        "residuals": [
            "No real router, preference dataset, reward model, RL run, or deployment monitor exists.",
            "The fixture exercises governance fields and negative controls only.",
        ],
        "non_claims": REQUIRED_NON_CLAIMS,
    }


def validate_policy_record(record: dict[str, Any], errors: list[str]) -> None:
    schema = load_json(ROOT / "schemas" / "policy_optimization_record.schema.json")
    if not isinstance(schema, dict):
        errors.append("schemas/policy_optimization_record.schema.json must contain an object.")
        return
    errors.extend(validate_schema_value(record, schema, "policy_update_record"))


def build_expected_result() -> dict[str, Any]:
    candidate_summaries = []
    for candidate in CANDIDATES:
        eligible = candidate_is_lease_eligible(candidate)
        candidate_summaries.append(
            {
                "policy_ref": candidate["policy_ref"],
                "role": candidate["role"],
                "eligible_for_canary_lease": eligible,
                "synthetic_score": candidate["synthetic_score"],
                "authority_effect": candidate["authority_effect"],
                "rollback_plan_present": candidate["rollback_plan_present"],
            }
        )

    selected = next(candidate for candidate in CANDIDATES if candidate["role"] == "selected_canary")
    baseline = next(candidate for candidate in CANDIDATES if candidate["role"] == "baseline")
    reward_only = next(candidate for candidate in CANDIDATES if candidate["role"] == "expected_invalid_reward_only_proxy")
    authority_expanding = next(
        candidate for candidate in CANDIDATES if candidate["role"] == "expected_invalid_authority_expansion"
    )
    missing_rollback = next(
        candidate for candidate in CANDIDATES if candidate["role"] == "expected_invalid_missing_rollback"
    )

    rollback_dry_run = {
        "injected_event_id": "monitor://policy-lease-rollback-injection-001",
        "selected_policy_ref": selected["policy_ref"],
        "restored_policy_ref": baseline["policy_ref"],
        "rollback_trigger": "synthetic monitor event; no live deployment or router was changed",
        "rollback_result": "baseline_restored_in_fixture",
    }

    policy_record = build_policy_record()

    return {
        "schema_version": "asi_stack.policy_update_lease_probe.v0",
        "result_id": "2026-07-02-policy-update-lease-probe",
        "recorded_date": "2026-07-02",
        "command": COMMAND,
        "result_kind": "deterministic_synthetic_policy_update_lease_probe",
        "workload_sample_count": len(WORKLOAD),
        "holdout_sample_count": sum(1 for sample in WORKLOAD if sample["holdout"]),
        "candidate_count": len(CANDIDATES),
        "selected_policy_ref": selected["policy_ref"],
        "baseline_policy_ref": baseline["policy_ref"],
        "selected_canary_eligible": candidate_is_lease_eligible(selected),
        "selected_canary_promotion_decision": "keep_experimental",
        "baseline_eligible": candidate_is_lease_eligible(baseline),
        "negative_controls": {
            "reward_only_proxy_rejected": not candidate_is_lease_eligible(reward_only),
            "authority_expansion_rejected": not candidate_is_lease_eligible(authority_expanding),
            "missing_rollback_rejected": not candidate_is_lease_eligible(missing_rollback),
        },
        "candidate_summaries": candidate_summaries,
        "rollback_dry_run": rollback_dry_run,
        "policy_update_record": policy_record,
        "lean_fixture_alignment": {
            "module": "AsiStackProofs.PolicyOptimization",
            "proof_tag": PROOF_TAG,
            "theorem_refs": REQUIRED_THEOREMS,
            "expected": {
                "sample_count": 6,
                "candidate_count": 5,
                "selected_canary_kept_experimental": True,
                "negative_reward_only_rejected": True,
                "negative_authority_expansion_rejected": True,
                "negative_missing_rollback_rejected": True,
                "holdout_checks_present": True,
                "contamination_check_present": True,
                "reward_hacking_probe_present": True,
                "rollback_dry_run_present": True,
                "support_state_effect_none": True,
                "non_claim_boundary": True,
            },
        },
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
        "verification_result": "pass",
        "residuals": policy_record["residuals"],
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
    if value.get("verification_result") != "pass":
        errors.append(f"{rel(RESULT)}: verification_result must be pass.")
    if value.get("support_state_effect") != "none":
        errors.append(f"{rel(RESULT)}: support_state_effect must remain none.")
    non_claim_text = text_blob(value.get("non_claims", []))
    for phrase in REQUIRED_NON_CLAIMS:
        if phrase.lower() not in non_claim_text:
            errors.append(f"{rel(RESULT)} non_claims missing {phrase!r}.")
    validate_policy_record(value.get("policy_update_record", {}), errors)


def validate_manifest(errors: list[str]) -> None:
    value = load_json(MANIFEST)
    chapter = None
    for part in value.get("parts", []):
        for candidate in part.get("chapters", []):
            if candidate.get("id") == "policy-optimization-and-learning-from-feedback":
                chapter = candidate
                break
    if chapter is None:
        errors.append("book_structure.json: missing policy optimization chapter.")
        return
    codex_blob = text_blob(chapter.get("codex_tests", []))
    if CODEX_TEST_NAME.lower() not in codex_blob:
        errors.append(f"book_structure.json: codex_tests missing {CODEX_TEST_NAME!r}.")
    proof_tags = {target.get("tag") for target in chapter.get("proof_targets", []) if isinstance(target, dict)}
    if PROOF_TAG not in proof_tags:
        errors.append(f"book_structure.json: proof_targets missing {PROOF_TAG!r}.")


def validate_lean(errors: list[str]) -> None:
    text = LEAN_FILE.read_text(encoding="utf-8", errors="ignore")
    for theorem in REQUIRED_THEOREMS:
        if not re.search(rf"\btheorem\s+{re.escape(theorem)}\b", text):
            errors.append(f"{rel(LEAN_FILE)} missing theorem {theorem}.")
    for field in (
        "sampleCount",
        "candidateCount",
        "selectedCanaryKeptExperimental",
        "negativeRewardOnlyRejected",
        "negativeAuthorityExpansionRejected",
        "negativeMissingRollbackRejected",
        "rollbackDryRunPresent",
        "supportStateEffectNone",
        "nonClaimBoundary",
    ):
        if field not in text:
            errors.append(f"{rel(LEAN_FILE)} missing fixture field {field}.")


def validate_surfaces(errors: list[str]) -> None:
    required = {
        DOC: [
            "Policy update lease probe",
            rel(RESULT),
            "six synthetic routing samples",
            "three expected-invalid controls",
            "no support-state transition",
        ],
        CHAPTER: [
            "Policy update lease probe",
            rel(RESULT),
            "no PPO, DPO, GRPO, RLVR, router-policy, context-policy, execution-policy, verifier-policy, or reasoning-budget training run",
        ],
        READER: [
            "policy update lease probe",
            "dry-run rollback",
            "not a deployed learning result",
        ],
        OUTLINE: [
            CODEX_TEST_NAME,
            PROOF_TAG,
            rel(RESULT),
        ],
        ROADMAP: [
            "Policy update lease probe",
            "deterministic policy-update lease fixture",
            "no support-state promotion",
        ],
        CHANGELOG: [
            "Policy update lease probe",
            rel(RESULT),
        ],
        VALIDATION_REGISTRY: [
            "scripts/validate_policy_update_lease_probe.py",
            "docs/policy_update_lease_probe.md",
            "experiments/policy_update_lease/results/2026-07-02-local.json",
            '"script": "validate_policy_update_lease_probe.py"',
        ],
    }
    for path, phrases in required.items():
        if not path.exists():
            errors.append(f"Missing required policy lease surface {rel(path)}.")
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        lowered = text.lower()
        for phrase in phrases:
            if phrase.lower() not in lowered:
                errors.append(f"{rel(path)} missing required phrase {phrase!r}.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-result", action="store_true")
    args = parser.parse_args()

    errors: list[str] = []
    expected = build_expected_result()
    if expected["workload_sample_count"] != 6:
        errors.append("Expected six synthetic routing samples.")
    if expected["candidate_count"] != 5:
        errors.append("Expected five candidate policies.")
    if expected["selected_canary_eligible"] is not True:
        errors.append("Selected canary must satisfy the finite lease gate.")
    controls = expected["negative_controls"]
    for key in ("reward_only_proxy_rejected", "authority_expansion_rejected", "missing_rollback_rejected"):
        if controls.get(key) is not True:
            errors.append(f"Negative control {key} must be rejected.")
    if expected["rollback_dry_run"].get("restored_policy_ref") != expected["baseline_policy_ref"]:
        errors.append("Rollback dry run must restore the baseline policy ref.")
    if expected["selected_canary_promotion_decision"] != "keep_experimental":
        errors.append("Selected canary must remain experimental.")
    validate_policy_record(expected["policy_update_record"], errors)
    validate_result(expected, args.write_result, errors)
    validate_manifest(errors)
    validate_lean(errors)
    validate_surfaces(errors)

    if errors:
        fail(errors)
    print("Policy update lease probe validation passed.")


if __name__ == "__main__":
    main()
