#!/usr/bin/env python3
"""Validate the frozen governed-work corpus and post-pilot amendment."""
from __future__ import annotations

import copy
import json
from pathlib import Path

from build_canonical_public_status import ROOT, load_json, validate_against_schema


TASKS = ROOT / "experiments/post_v2_governed_work_flagship/tasks.json"
TASK_SCHEMA = ROOT / "schemas/post_v2_governed_work_tasks.schema.json"
AMENDMENT = ROOT / "experiments/post_v2_evidence_program/amendments/governed_work_v1.json"
AMENDMENT_SCHEMA = ROOT / "schemas/post_v2_evidence_preregistration_amendment.schema.json"
PILOT = ROOT / "experiments/post_v2_governed_work_flagship/attempts/2026-07-10-plan-format-pilot/result.json"
PILOT_README = PILOT.parent / "README.md"
RUNNER = ROOT / "scripts/run_post_v2_governed_work_flagship.py"
ATTACKS = {
    "retrieved-context prompt injection",
    "stale authorization",
    "revocation during execution",
    "forged or mismatched receipt",
    "correlated proposer and verifier",
    "hidden residual cost",
    "failed rollback",
    "cheaper route violating a safety constraint",
}


def semantic_errors(corpus: dict, amendment: dict) -> list[str]:
    errors: list[str] = []
    tasks = corpus.get("tasks", [])
    if corpus.get("task_count") != len(tasks) or len(tasks) != 8:
        errors.append("corpus must contain exactly eight tasks")
    if {row.get("attack_family") for row in tasks} != ATTACKS:
        errors.append("corpus must cover each registered attack family exactly once")
    if len({row.get("task_id") for row in tasks}) != 8 or len({row.get("function_name") for row in tasks}) != 8:
        errors.append("task IDs and function names must be unique")
    for row in tasks:
        visible = set(row.get("visible_tests", []))
        hidden = set(row.get("hidden_tests", []))
        if visible & hidden:
            errors.append(f"{row.get('task_id')}: visible and hidden probes overlap")
        prompt_surface = "\n".join([row.get("request", ""), row.get("trusted_context", ""), row.get("untrusted_context", "")])
        if any(probe in prompt_surface for probe in hidden):
            errors.append(f"{row.get('task_id')}: hidden probe leaked into proposer context")
    unchanged = amendment.get("unchanged_fields", {})
    if unchanged.get("task_count") != 8 or unchanged.get("repeat_seeds") != [17, 29]:
        errors.append("amendment changed task count or repeat seeds")
    if unchanged.get("model_revision") != "ea3f2471cf1b1f0db85067f1ef93848e38e88c25":
        errors.append("amendment does not preserve the pinned model revision")
    if amendment.get("pilot_support_state_effect") != "none":
        errors.append("prevalidation pilot cannot affect support state")
    runner = RUNNER.read_text(encoding="utf-8")
    for phrase in ("plan_prompt(task)", "code_prompt(task, plan)", "TemporaryDirectory", "git(root, \"init\"", "local_files_only=True"):
        if phrase not in runner:
            errors.append(f"runner missing amended protocol surface: {phrase}")
    return errors


def main() -> None:
    required = (TASKS, TASK_SCHEMA, AMENDMENT, AMENDMENT_SCHEMA, PILOT, PILOT_README, RUNNER)
    missing = [path.relative_to(ROOT).as_posix() for path in required if not path.is_file()]
    if missing:
        raise SystemExit("missing governed-work setup artifacts: " + ", ".join(missing))
    corpus = load_json(TASKS)
    amendment = load_json(AMENDMENT)
    errors = validate_against_schema(corpus, load_json(TASK_SCHEMA), TASKS.relative_to(ROOT).as_posix())
    errors.extend(validate_against_schema(amendment, load_json(AMENDMENT_SCHEMA), AMENDMENT.relative_to(ROOT).as_posix()))
    errors.extend(semantic_errors(corpus, amendment))
    pilot = load_json(PILOT)
    if pilot.get("run_count") != 16 or any(row.get("model_output", {}).get("plan_line_present") for row in pilot.get("runs", [])):
        errors.append("preserved pilot must retain all 16 plan-format failures")
    readme = PILOT_README.read_text(encoding="utf-8")
    if "not evidence for a book claim" not in readme or "in-memory repository snapshots" not in readme:
        errors.append("pilot README does not preserve both non-evidentiary defects")

    mutations = []
    duplicate_attack = copy.deepcopy(corpus)
    duplicate_attack["tasks"][0]["attack_family"] = duplicate_attack["tasks"][1]["attack_family"]
    mutations.append((duplicate_attack, amendment))
    leaked_holdout = copy.deepcopy(corpus)
    leaked_holdout["tasks"][0]["request"] += " " + leaked_holdout["tasks"][0]["hidden_tests"][0]
    mutations.append((leaked_holdout, amendment))
    changed_seed = copy.deepcopy(amendment)
    changed_seed["unchanged_fields"]["repeat_seeds"] = [17]
    mutations.append((corpus, changed_seed))
    mutable_model = copy.deepcopy(amendment)
    mutable_model["unchanged_fields"]["model_revision"] = "main"
    mutations.append((corpus, mutable_model))
    promoted_pilot = copy.deepcopy(amendment)
    promoted_pilot["pilot_support_state_effect"] = "promote"
    mutations.append((corpus, promoted_pilot))
    for mutated_corpus, mutated_amendment in mutations:
        if not semantic_errors(mutated_corpus, mutated_amendment):
            errors.append("a governed-work setup negative control was accepted")
    if errors:
        raise SystemExit("Post-v2 governed-work setup validation failed:\n - " + "\n - ".join(errors))
    print("Post-v2 governed-work setup passed: 8 frozen tasks, 8 attacks, isolated holdouts, preserved 16-run non-evidentiary pilot, amended plan-to-code protocol, real Git worktrees, and 5 rejecting controls.")


if __name__ == "__main__":
    main()
