#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "experiments" / "planning_runtime_replan_delta" / "results" / "2026-07-02-local.json"
DOC = ROOT / "docs" / "planning_runtime_replan_delta_audit.md"
README = ROOT / "experiments" / "planning_runtime_replan_delta" / "README.md"
CHAPTER = ROOT / "chapters" / "planning-as-a-control-layer.qmd"
READER = (
    ROOT
    / "editions"
    / "reader_manuscript"
    / "v1_0"
    / "chapters"
    / "planning-as-a-control-layer.qmd"
)
OUTLINE = ROOT / "docs" / "book_outline.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
CHANGELOG = ROOT / "appendices" / "F_changelog.qmd"
MANIFEST = ROOT / "book_structure.json"
VALIDATION_REGISTRY = ROOT / "validation" / "registry.json"
LEAN_FILE = ROOT / "lean" / "AsiStackProofs" / "Planning.lean"

COMMAND = "python3 scripts/validate_planning_runtime_replan_delta.py"
PROOF_TAG = "lean:planning.runtime_replan.delta_audit_bridge"
CODEX_TEST_NAME = "Planning runtime-replan delta audit"
REQUIRED_THEOREMS = [
    "runtime_replan_delta_authority_widening_rejected",
    "runtime_replan_delta_stop_erasure_rejected",
    "runtime_replan_delta_blocked_authority_dispatch_rejected",
    "runtime_replan_delta_complete_audit_accepted",
    "planning_runtime_replan_delta_audit_bridge",
]
REQUIRED_NON_CLAIMS = [
    "does not execute a deployed planner",
    "does not prove runtime scheduler behavior",
    "does not prove decomposition quality",
    "does not prove route quality or selected-tier adequacy",
    "does not prove live feedback handling",
    "does not promote the chapter support state",
]

REQUIRED_DELTA_FIELDS = {
    "changed_nodes",
    "dependency_impact",
    "context_delta",
    "verification_delta",
    "authority_delta",
    "stop_condition_delta",
    "residual_delta",
    "cost_quality_delta",
    "non_claim_delta",
}


TRACES: list[dict[str, Any]] = [
    {
        "trace_id": "valid_local_source_repair_delta",
        "expect_valid": True,
        "support_state_effect": "none",
        "replan_trigger": "feedback://stale-source-version",
        "parent_contract_ref": "command://public-reader-planning-pass",
        "previous_plan_ref": "plan://reader-pass-v1",
        "revised_plan_ref": "plan://reader-pass-v2",
        "authority_preserved": True,
        "stop_conditions_preserved": True,
        "affected_subgraph_only": True,
        "unaffected_nodes_rerun": False,
        "blocked_authority_path": False,
        "dispatch_receipt_issued": True,
        "delta_fields": sorted(REQUIRED_DELTA_FIELDS),
        "changed_nodes": ["node://source-refresh", "node://dependent-summary"],
        "rerun_nodes": ["node://source-refresh", "node://dependent-summary"],
        "dependency_impacted_nodes": ["node://dependent-summary"],
        "context_delta_recorded": True,
        "verification_delta_recorded": True,
        "authority_delta_recorded": True,
        "stop_condition_delta_recorded": True,
        "residual_owner": "owner://planning-residual-ledger",
        "cost_quality_delta_includes_repair": True,
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "valid_authority_blocked_replan_delta",
        "expect_valid": True,
        "support_state_effect": "none",
        "replan_trigger": "feedback://external-publication-request",
        "parent_contract_ref": "command://safe-local-edit-only",
        "previous_plan_ref": "plan://local-edit-v1",
        "revised_plan_ref": "plan://local-edit-v2",
        "authority_preserved": True,
        "stop_conditions_preserved": True,
        "affected_subgraph_only": True,
        "unaffected_nodes_rerun": False,
        "blocked_authority_path": True,
        "dispatch_receipt_issued": False,
        "delta_fields": sorted(REQUIRED_DELTA_FIELDS),
        "changed_nodes": ["node://publication-route-denied"],
        "rerun_nodes": [],
        "dependency_impacted_nodes": [],
        "context_delta_recorded": True,
        "verification_delta_recorded": True,
        "authority_delta_recorded": True,
        "stop_condition_delta_recorded": True,
        "residual_owner": "owner://approval-needed-residual",
        "cost_quality_delta_includes_repair": True,
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "invalid_authority_widening_replan_admitted",
        "expect_valid": False,
        "support_state_effect": "none",
        "replan_trigger": "feedback://needs-network",
        "parent_contract_ref": "command://local-only",
        "previous_plan_ref": "plan://local-v1",
        "revised_plan_ref": "plan://network-v2",
        "authority_preserved": False,
        "stop_conditions_preserved": True,
        "affected_subgraph_only": True,
        "unaffected_nodes_rerun": False,
        "blocked_authority_path": False,
        "dispatch_receipt_issued": True,
        "delta_fields": sorted(REQUIRED_DELTA_FIELDS),
        "changed_nodes": ["node://network-fetch"],
        "rerun_nodes": ["node://network-fetch"],
        "dependency_impacted_nodes": [],
        "context_delta_recorded": True,
        "verification_delta_recorded": True,
        "authority_delta_recorded": True,
        "stop_condition_delta_recorded": True,
        "residual_owner": "owner://planning-residual-ledger",
        "cost_quality_delta_includes_repair": True,
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "invalid_stop_condition_erased",
        "expect_valid": False,
        "support_state_effect": "none",
        "replan_trigger": "feedback://budget-pressure",
        "parent_contract_ref": "command://stop-on-missing-source",
        "previous_plan_ref": "plan://with-stop-v1",
        "revised_plan_ref": "plan://without-stop-v2",
        "authority_preserved": True,
        "stop_conditions_preserved": False,
        "affected_subgraph_only": True,
        "unaffected_nodes_rerun": False,
        "blocked_authority_path": False,
        "dispatch_receipt_issued": True,
        "delta_fields": sorted(REQUIRED_DELTA_FIELDS),
        "changed_nodes": ["node://source-read"],
        "rerun_nodes": ["node://source-read"],
        "dependency_impacted_nodes": [],
        "context_delta_recorded": True,
        "verification_delta_recorded": True,
        "authority_delta_recorded": True,
        "stop_condition_delta_recorded": True,
        "residual_owner": "owner://planning-residual-ledger",
        "cost_quality_delta_includes_repair": True,
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "invalid_unaffected_node_rerun_without_dependency",
        "expect_valid": False,
        "support_state_effect": "none",
        "replan_trigger": "feedback://stale-source-version",
        "parent_contract_ref": "command://public-reader-planning-pass",
        "previous_plan_ref": "plan://reader-pass-v1",
        "revised_plan_ref": "plan://reader-pass-v2",
        "authority_preserved": True,
        "stop_conditions_preserved": True,
        "affected_subgraph_only": False,
        "unaffected_nodes_rerun": True,
        "blocked_authority_path": False,
        "dispatch_receipt_issued": True,
        "delta_fields": sorted(REQUIRED_DELTA_FIELDS),
        "changed_nodes": ["node://source-refresh"],
        "rerun_nodes": ["node://source-refresh", "node://unaffected-figure"],
        "dependency_impacted_nodes": [],
        "context_delta_recorded": True,
        "verification_delta_recorded": True,
        "authority_delta_recorded": True,
        "stop_condition_delta_recorded": True,
        "residual_owner": "owner://planning-residual-ledger",
        "cost_quality_delta_includes_repair": True,
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "invalid_changed_node_without_residual_owner",
        "expect_valid": False,
        "support_state_effect": "none",
        "replan_trigger": "feedback://failed-quality-predicate",
        "parent_contract_ref": "command://reader-pass",
        "previous_plan_ref": "plan://quality-v1",
        "revised_plan_ref": "plan://quality-v2",
        "authority_preserved": True,
        "stop_conditions_preserved": True,
        "affected_subgraph_only": True,
        "unaffected_nodes_rerun": False,
        "blocked_authority_path": False,
        "dispatch_receipt_issued": True,
        "delta_fields": sorted(REQUIRED_DELTA_FIELDS),
        "changed_nodes": ["node://revise-section"],
        "rerun_nodes": ["node://revise-section"],
        "dependency_impacted_nodes": [],
        "context_delta_recorded": True,
        "verification_delta_recorded": True,
        "authority_delta_recorded": True,
        "stop_condition_delta_recorded": True,
        "residual_owner": "",
        "cost_quality_delta_includes_repair": True,
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "invalid_missing_context_delta",
        "expect_valid": False,
        "support_state_effect": "none",
        "replan_trigger": "feedback://new-source-version",
        "parent_contract_ref": "command://source-bounded",
        "previous_plan_ref": "plan://source-v1",
        "revised_plan_ref": "plan://source-v2",
        "authority_preserved": True,
        "stop_conditions_preserved": True,
        "affected_subgraph_only": True,
        "unaffected_nodes_rerun": False,
        "blocked_authority_path": False,
        "dispatch_receipt_issued": True,
        "delta_fields": sorted(REQUIRED_DELTA_FIELDS - {"context_delta"}),
        "changed_nodes": ["node://source-update"],
        "rerun_nodes": ["node://source-update"],
        "dependency_impacted_nodes": [],
        "context_delta_recorded": False,
        "verification_delta_recorded": True,
        "authority_delta_recorded": True,
        "stop_condition_delta_recorded": True,
        "residual_owner": "owner://planning-residual-ledger",
        "cost_quality_delta_includes_repair": True,
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "invalid_missing_verification_delta",
        "expect_valid": False,
        "support_state_effect": "none",
        "replan_trigger": "feedback://new-quality-predicate",
        "parent_contract_ref": "command://quality-bounded",
        "previous_plan_ref": "plan://quality-v1",
        "revised_plan_ref": "plan://quality-v2",
        "authority_preserved": True,
        "stop_conditions_preserved": True,
        "affected_subgraph_only": True,
        "unaffected_nodes_rerun": False,
        "blocked_authority_path": False,
        "dispatch_receipt_issued": True,
        "delta_fields": sorted(REQUIRED_DELTA_FIELDS - {"verification_delta"}),
        "changed_nodes": ["node://quality-review"],
        "rerun_nodes": ["node://quality-review"],
        "dependency_impacted_nodes": [],
        "context_delta_recorded": True,
        "verification_delta_recorded": False,
        "authority_delta_recorded": True,
        "stop_condition_delta_recorded": True,
        "residual_owner": "owner://planning-residual-ledger",
        "cost_quality_delta_includes_repair": True,
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "invalid_blocked_authority_dispatch_receipt",
        "expect_valid": False,
        "support_state_effect": "none",
        "replan_trigger": "feedback://external-publication-request",
        "parent_contract_ref": "command://safe-local-edit-only",
        "previous_plan_ref": "plan://local-edit-v1",
        "revised_plan_ref": "plan://local-edit-v2",
        "authority_preserved": True,
        "stop_conditions_preserved": True,
        "affected_subgraph_only": True,
        "unaffected_nodes_rerun": False,
        "blocked_authority_path": True,
        "dispatch_receipt_issued": True,
        "delta_fields": sorted(REQUIRED_DELTA_FIELDS),
        "changed_nodes": ["node://publication-route-denied"],
        "rerun_nodes": [],
        "dependency_impacted_nodes": [],
        "context_delta_recorded": True,
        "verification_delta_recorded": True,
        "authority_delta_recorded": True,
        "stop_condition_delta_recorded": True,
        "residual_owner": "owner://approval-needed-residual",
        "cost_quality_delta_includes_repair": True,
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "invalid_support_promotion_overclaim",
        "expect_valid": False,
        "support_state_effect": "synthetic-test-backed",
        "replan_trigger": "feedback://local-fixture",
        "parent_contract_ref": "command://reader-pass",
        "previous_plan_ref": "plan://fixture-v1",
        "revised_plan_ref": "plan://fixture-v2",
        "authority_preserved": True,
        "stop_conditions_preserved": True,
        "affected_subgraph_only": True,
        "unaffected_nodes_rerun": False,
        "blocked_authority_path": False,
        "dispatch_receipt_issued": True,
        "delta_fields": sorted(REQUIRED_DELTA_FIELDS),
        "changed_nodes": ["node://fixture"],
        "rerun_nodes": ["node://fixture"],
        "dependency_impacted_nodes": [],
        "context_delta_recorded": True,
        "verification_delta_recorded": True,
        "authority_delta_recorded": True,
        "stop_condition_delta_recorded": True,
        "residual_owner": "owner://planning-residual-ledger",
        "cost_quality_delta_includes_repair": True,
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "trace_id": "invalid_missing_non_claim_boundary",
        "expect_valid": False,
        "support_state_effect": "none",
        "replan_trigger": "feedback://local-fixture",
        "parent_contract_ref": "command://reader-pass",
        "previous_plan_ref": "plan://fixture-v1",
        "revised_plan_ref": "plan://fixture-v2",
        "authority_preserved": True,
        "stop_conditions_preserved": True,
        "affected_subgraph_only": True,
        "unaffected_nodes_rerun": False,
        "blocked_authority_path": False,
        "dispatch_receipt_issued": True,
        "delta_fields": sorted(REQUIRED_DELTA_FIELDS),
        "changed_nodes": ["node://fixture"],
        "rerun_nodes": ["node://fixture"],
        "dependency_impacted_nodes": [],
        "context_delta_recorded": True,
        "verification_delta_recorded": True,
        "authority_delta_recorded": True,
        "stop_condition_delta_recorded": True,
        "residual_owner": "owner://planning-residual-ledger",
        "cost_quality_delta_includes_repair": True,
        "non_claims": REQUIRED_NON_CLAIMS[:-1],
    },
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Planning runtime-replan delta audit failed:")
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


def trace_errors(trace: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    trace_id = str(trace.get("trace_id", "<missing>"))
    for key, prefix in (
        ("replan_trigger", "feedback://"),
        ("parent_contract_ref", "command://"),
        ("previous_plan_ref", "plan://"),
        ("revised_plan_ref", "plan://"),
    ):
        if not isinstance(trace.get(key), str) or not trace[key].startswith(prefix):
            errors.append(f"{trace_id}: {key} must use {prefix}.")

    if trace.get("support_state_effect") != "none":
        errors.append(f"{trace_id}: support_state_effect must remain none.")
    if trace.get("authority_preserved") is not True:
        errors.append(f"{trace_id}: replanning must preserve parent authority.")
    if trace.get("stop_conditions_preserved") is not True:
        errors.append(f"{trace_id}: replanning must preserve stop conditions.")
    if trace.get("affected_subgraph_only") is not True:
        errors.append(f"{trace_id}: replanning must stay inside the affected subgraph.")
    if trace.get("unaffected_nodes_rerun") is True and not trace.get("dependency_impacted_nodes"):
        errors.append(f"{trace_id}: unaffected reruns require a dependency-impact record.")

    delta_fields = set(trace.get("delta_fields", []))
    if delta_fields != REQUIRED_DELTA_FIELDS:
        errors.append(f"{trace_id}: delta_fields must include {sorted(REQUIRED_DELTA_FIELDS)}.")
    if trace.get("context_delta_recorded") is not True:
        errors.append(f"{trace_id}: context delta must be recorded.")
    if trace.get("verification_delta_recorded") is not True:
        errors.append(f"{trace_id}: verification delta must be recorded.")
    if trace.get("authority_delta_recorded") is not True:
        errors.append(f"{trace_id}: authority delta must be recorded.")
    if trace.get("stop_condition_delta_recorded") is not True:
        errors.append(f"{trace_id}: stop-condition delta must be recorded.")
    if not str(trace.get("residual_owner", "")).startswith("owner://"):
        errors.append(f"{trace_id}: residual owner must be recorded.")
    if trace.get("cost_quality_delta_includes_repair") is not True:
        errors.append(f"{trace_id}: repair/review cost delta must remain in the ledger.")
    if trace.get("blocked_authority_path") is True and trace.get("dispatch_receipt_issued") is True:
        errors.append(f"{trace_id}: blocked authority path cannot issue a dispatch receipt.")

    changed_nodes = trace.get("changed_nodes", [])
    if not isinstance(changed_nodes, list) or not changed_nodes:
        errors.append(f"{trace_id}: changed_nodes must name at least one affected node.")
    for field in ("changed_nodes", "rerun_nodes", "dependency_impacted_nodes"):
        values = trace.get(field, [])
        if not isinstance(values, list):
            errors.append(f"{trace_id}: {field} must be a list.")
            continue
        for value in values:
            if not isinstance(value, str) or not value.startswith("node://"):
                errors.append(f"{trace_id}: {field} entries must use node://.")

    non_claim_text = text_blob(trace.get("non_claims", []))
    for phrase in REQUIRED_NON_CLAIMS:
        if phrase.lower() not in non_claim_text:
            errors.append(f"{trace_id}: non_claims missing {phrase!r}.")

    return errors


def build_expected_result(valid_count: int, invalid_count: int) -> dict[str, Any]:
    return {
        "schema_version": "asi_stack.planning_runtime_replan_delta.v0",
        "result_id": "2026-07-02-planning-runtime-replan-delta-audit",
        "recorded_date": "2026-07-02",
        "command": COMMAND,
        "result_kind": "deterministic_synthetic_runtime_replan_delta_audit",
        "valid_trace_count": valid_count,
        "expected_invalid_control_count": invalid_count,
        "trace_count": len(TRACES),
        "negative_controls": {
            "authority_widening_rejected": True,
            "stop_condition_erasure_rejected": True,
            "unaffected_rerun_without_dependency_rejected": True,
            "missing_residual_owner_rejected": True,
            "missing_context_delta_rejected": True,
            "missing_verification_delta_rejected": True,
            "blocked_authority_dispatch_rejected": True,
            "support_promotion_overclaim_rejected": True,
            "missing_non_claim_boundary_rejected": True,
        },
        "transition_coverage": {
            "local_source_repair_delta": True,
            "blocked_authority_replan_delta": True,
            "authority_preserved": True,
            "stop_conditions_preserved": True,
            "affected_subgraph_scoped": True,
            "context_delta_recorded": True,
            "verification_delta_recorded": True,
            "residual_owner_recorded": True,
            "cost_quality_repair_delta_recorded": True,
            "no_support_state_effect": True,
        },
        "lean_fixture_alignment": {
            "module": "AsiStackProofs.Planning",
            "proof_tag": PROOF_TAG,
            "theorem_refs": REQUIRED_THEOREMS,
            "expected": {
                "valid_local_repair_trace_present": True,
                "valid_blocked_authority_trace_present": True,
                "negative_controls_rejected": True,
                "authority_preserved": True,
                "stop_conditions_preserved": True,
                "affected_subgraph_scoped": True,
                "context_delta_recorded": True,
                "verification_delta_recorded": True,
                "residuals_recorded": True,
                "blocked_authority_no_dispatch": True,
                "support_state_effect_none": True,
                "non_claim_boundary": True,
            },
        },
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
        "verification_result": "pass",
        "residuals": [
            "Synthetic runtime-replan delta audit only; no deployed planner, scheduler, or live feedback loop was exercised.",
            "The chapter core claim remains at argument support.",
        ],
        "non_claims": REQUIRED_NON_CLAIMS,
    }


def validate_result(expected: dict[str, Any], write_result: bool, errors: list[str]) -> None:
    serialized = json.dumps(expected, indent=2, sort_keys=True) + "\n"
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
    if value.get("evidence_transition_created") is not False:
        errors.append(f"{rel(RESULT)}: evidence_transition_created must remain false.")


def validate_manifest(errors: list[str]) -> None:
    value = load_json(MANIFEST)
    chapter = None
    for part in value.get("parts", []):
        for candidate in part.get("chapters", []):
            if candidate.get("id") == "planning-as-a-control-layer":
                chapter = candidate
                break
    if chapter is None:
        errors.append("book_structure.json: missing planning chapter.")
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
        "validLocalRepairTracePresent",
        "validBlockedAuthorityTracePresent",
        "negativeControlsRejected",
        "authorityPreserved",
        "stopConditionsPreserved",
        "affectedSubgraphScoped",
        "contextDeltaRecorded",
        "verificationDeltaRecorded",
        "residualsRecorded",
        "blockedAuthorityNoDispatch",
        "supportStateEffectNone",
        "nonClaimBoundary",
    ):
        if field not in text:
            errors.append(f"{rel(LEAN_FILE)} missing fixture field {field}.")


def validate_surfaces(errors: list[str]) -> None:
    required = {
        DOC: [
            "Planning Runtime-Replan Delta Audit",
            rel(RESULT),
            "two valid synthetic runtime-replan traces",
            "nine expected-invalid controls",
            "no support-state transition",
        ],
        README: [
            "Planning Runtime-Replan Delta Audit",
            rel(RESULT),
            "synthetic runtime-replan",
        ],
        CHAPTER: [
            "Planning runtime-replan delta audit",
            rel(RESULT),
            "two valid synthetic runtime-replan traces",
            "nine expected-invalid controls",
        ],
        READER: [
            "runtime-replan delta audit",
            "two synthetic runtime-replan traces",
            "not a deployed planner result",
        ],
        OUTLINE: [
            CODEX_TEST_NAME,
            PROOF_TAG,
            rel(RESULT),
        ],
        ROADMAP: [
            "Planning runtime-replan delta audit",
            "deterministic synthetic runtime-replan delta audit",
            "no support-state promotion",
        ],
        CHANGELOG: [
            "Planning runtime-replan delta audit",
            rel(RESULT),
        ],
        VALIDATION_REGISTRY: [
            "scripts/validate_planning_runtime_replan_delta.py",
            "docs/planning_runtime_replan_delta_audit.md",
            "experiments/planning_runtime_replan_delta/results/2026-07-02-local.json",
            '"script": "validate_planning_runtime_replan_delta.py"',
        ],
    }
    for path, phrases in required.items():
        if not path.exists():
            errors.append(f"Missing required runtime-replan surface {rel(path)}.")
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
    valid_count = 0
    invalid_count = 0
    for trace in TRACES:
        expect_valid = bool(trace.get("expect_valid"))
        trace_id = str(trace.get("trace_id", "<missing>"))
        current_errors = trace_errors(trace)
        if expect_valid:
            valid_count += 1
            errors.extend(current_errors)
        else:
            invalid_count += 1
            if not current_errors:
                errors.append(f"{trace_id}: expected-invalid control unexpectedly passed.")

    if valid_count != 2:
        errors.append("Expected exactly two valid synthetic runtime-replan traces.")
    if invalid_count != 9:
        errors.append("Expected exactly nine expected-invalid controls.")

    expected = build_expected_result(valid_count, invalid_count)
    validate_result(expected, args.write_result, errors)
    validate_manifest(errors)
    validate_lean(errors)
    validate_surfaces(errors)

    if errors:
        fail(errors)
    print("Planning runtime-replan delta audit passed.")


if __name__ == "__main__":
    main()
