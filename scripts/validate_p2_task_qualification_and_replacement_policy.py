#!/usr/bin/env python3
"""Validate the frozen P2 task qualification and replacement policy."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "evidence_quality/p2_task_qualification_and_replacement_policy.json"
SCHEMA = ROOT / "schemas/p2_task_qualification_and_replacement_policy.schema.json"
CORPUS = ROOT / "evidence_quality/p2_development_corpus_preflight.json"
DOC = ROOT / "docs/p2_task_qualification_and_replacement_policy.md"


def failures(record: dict, *, inspect_files: bool = True) -> list[str]:
    out: list[str] = []
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    for error in Draft202012Validator(schema).iter_errors(record):
        out.append(f"schema:{'.'.join(map(str, error.path))}: {error.message}")
    source = record.get("source", {})
    acceptance = record.get("task_acceptance", {})
    dependency = acceptance.get("dependency_phase", {})
    baseline = acceptance.get("baseline_oracle", {})
    gold = acceptance.get("human_gold_oracle", {})
    dual = acceptance.get("dual_evaluator", {})
    repeatability = acceptance.get("repeatability", {})
    exclusion = record.get("exclusion_semantics", {})
    replacement = record.get("replacement_rule", {})
    resource = record.get("resource_boundary", {})
    expected_seed = (
        "asi-stack-p2-replacement-v1|"
        + source.get("eligible_metadata_sha256", "") + "|"
        + source.get("original_development_pool_sha256", "")
    )
    if replacement.get("seed") != expected_seed:
        out.append("replacement seed is not bound to both frozen corpus digests")
    checks = [
        (dependency.get("separate_from_outcome_execution") is True, "dependency phase must be separate"),
        (dependency.get("task_solution_or_test_patch_applied") is False, "dependency phase may not apply task patches"),
        (dependency.get("unrestricted_egress_effect") == "development_diagnostic_only", "unrestricted egress was promoted"),
        (baseline.get("pass_to_pass_set_must_match_exactly") is True, "baseline P2P exactness weakened"),
        (baseline.get("fail_to_pass_set_must_match_exactly") is True, "baseline F2P exactness weakened"),
        (baseline.get("missing_or_unexpected_test_allowed") is False, "baseline missing/extra tests allowed"),
        (gold.get("pass_to_pass_union_fail_to_pass_set_must_match_exactly") is True, "gold exactness weakened"),
        (gold.get("failed_test_allowed") is False, "gold failure allowed"),
        (gold.get("missing_or_unexpected_test_allowed") is False, "gold missing/extra tests allowed"),
        (dual.get("independently_implemented_parser_required") is True, "independent parser removed"),
        (dual.get("exact_status_set_agreement_required") is True, "dual-parser agreement weakened"),
        (dual.get("disagreement_effect") == "close_construct_gate", "parser disagreement no longer fails closed"),
        (len(dual.get("calibration_cases", [])) >= 7, "evaluator calibration coverage weakened"),
        (repeatability.get("raw_logs_required_for_every_attempt") is True, "raw-log custody weakened"),
        (exclusion.get("negative_inference_level") == "N0", "task exclusion was promoted above N0"),
        (exclusion.get("claim_effect") == "none", "task exclusion gained claim effect"),
        (exclusion.get("acceptance_rule_may_be_weakened_after_outcome") is False, "outcome-aware weakening allowed"),
        (replacement.get("sequential_opening") is True, "replacement opening is not sequential"),
        (replacement.get("skipping_candidate_after_outcome_allowed") is False, "outcome-aware candidate skip allowed"),
        (replacement.get("failed_candidates_retained") is True, "failed replacement custody weakened"),
        (resource.get("resource_ceiling_state") == "must_be_frozen_before_replacement_draw", "resource ceiling can be post hoc"),
        (resource.get("resource_failure_is_claim_failure") is False, "resource failure was laundered into claim failure"),
        (len(resource.get("measurements_required", [])) >= 9, "resource measurement coverage weakened"),
    ]
    out.extend(message for passed, message in checks if not passed)
    if inspect_files:
        corpus = json.loads(CORPUS.read_text(encoding="utf-8"))
        if source.get("eligible_metadata_sha256") != corpus["eligible_universe"]["metadata_sha256"]:
            out.append("eligible metadata digest drifted from corpus preflight")
        if source.get("original_development_pool_sha256") != corpus["development_pool"]["pool_sha256"]:
            out.append("original development pool digest drifted")
        doc = DOC.read_text(encoding="utf-8")
        for phrase in [
            "policy frozen before draw",
            "metadata queue now frozen",
            "cannot be waived after inspecting the outcome",
            "no candidate may be skipped after its outcome is known",
            "N0",
            "The final held-out pool remains unselected and unopened",
        ]:
            if phrase not in doc:
                out.append(f"policy receipt missing boundary: {phrase}")
    return out


def main() -> None:
    record = json.loads(RECORD.read_text(encoding="utf-8"))
    out = failures(record)
    mutations = []
    def add(label, edit):
        candidate = copy.deepcopy(record); edit(candidate); mutations.append((label, candidate))
    add("one repetition", lambda r: r["task_acceptance"].__setitem__("repetitions_per_arm", 1))
    add("runtime network", lambda r: r["task_acceptance"].__setitem__("runtime_network", "bridge"))
    add("patch during dependency setup", lambda r: r["task_acceptance"]["dependency_phase"].__setitem__("task_solution_or_test_patch_applied", True))
    add("baseline subset", lambda r: r["task_acceptance"]["baseline_oracle"].__setitem__("fail_to_pass_set_must_match_exactly", False))
    add("gold extras allowed", lambda r: r["task_acceptance"]["human_gold_oracle"].__setitem__("missing_or_unexpected_test_allowed", True))
    add("independent parser removed", lambda r: r["task_acceptance"]["dual_evaluator"].__setitem__("independently_implemented_parser_required", False))
    add("raw logs optional", lambda r: r["task_acceptance"]["repeatability"].__setitem__("raw_logs_required_for_every_attempt", False))
    add("negative promotion", lambda r: r["exclusion_semantics"].__setitem__("negative_inference_level", "N3"))
    add("candidate skipping", lambda r: r["replacement_rule"].__setitem__("skipping_candidate_after_outcome_allowed", True))
    add("seed drift", lambda r: r["replacement_rule"].__setitem__("seed", "favorable"))
    add("queue state erased", lambda r: r["replacement_rule"].__setitem__("replacement_draw_state", "not_started"))
    add("final opened", lambda r: r["custody"].__setitem__("final_pool_opened", True))
    add("support promotion", lambda r: r.__setitem__("support_state_effect", "promotion"))
    for label, candidate in mutations:
        if not failures(candidate, inspect_files=False):
            out.append(f"negative mutation accepted: {label}")
    if out:
        raise SystemExit("P2 task qualification policy failed:\n - " + "\n - ".join(out))
    print("P2 task qualification policy passed: exact paired gold oracle, dual evaluator, N0 exclusions, deterministic queue frozen, final pool closed; 13/13 mutations rejected.")


if __name__ == "__main__":
    main()
