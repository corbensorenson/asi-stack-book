#!/usr/bin/env python3
"""Validate frozen post-v2.1 P1/P2/P3 inputs and draft preregistration."""

from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
BASE = "experiments/post_v2_1_evidence_program"


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def canonical_sha(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def unique(rows: list[dict], key: str) -> bool:
    values = [row.get(key) for row in rows]
    return len(values) == len(set(values))


def validate(data: dict[str, object]) -> list[str]:
    errors: list[str] = []
    prereg, p1, p2, harm, p3, inventory = (data[k] for k in ["prereg", "p1", "p2", "harm", "p3", "inventory"])
    schema_errors = sorted(Draft202012Validator(data["schema"]).iter_errors(prereg), key=lambda e: list(e.path))
    errors.extend(f"preregistration schema: {error.message}" for error in schema_errors)

    p1_rows = p1.get("tasks", [])
    if p1.get("task_count") != 36 or p1.get("family_count") != 6 or not unique(p1_rows, "task_id"):
        errors.append("P1 must contain 36 unique tasks across six families")
    if p1.get("split_counts") != {"development": 6, "calibration": 12, "test": 18}:
        errors.append("P1 split counts drifted")
    if p1.get("content_sha256") != canonical_sha({"tasks": p1_rows, "split_counts": p1.get("split_counts")}):
        errors.append("P1 content digest drifted")
    if set(row.get("expected_route") for row in p1_rows) != {"release", "clarify", "quarantine", "refuse"}:
        errors.append("P1 route coverage incomplete")
    required_effects = {"tracked_file_bytes", "untracked_file", "rename", "delete", "symlink_target", "executable_bit", "generated_artifact", "nested_repository", "cache_entry"}
    if set(row.get("effect_surface") for row in p1_rows) != required_effects:
        errors.append("P1 effect-surface coverage drifted")
    for row in p1_rows:
        if row.get("expected_route") == "release" and (not row.get("function_name") or len(row.get("observer_only_cases", [])) < 3):
            errors.append(f"P1 releasable task lacks function or observer-only cases: {row.get('task_id')}")

    p2_rows = p2.get("requests", [])
    if p2.get("request_count") != 240 or not unique(p2_rows, "request_id"):
        errors.append("P2 must contain 240 unique requests")
    if p2.get("split_counts") != {"train": 120, "validation": 60, "test": 60}:
        errors.append("P2 split counts drifted")
    actions = ["specialist_alpha", "specialist_beta", "generalist", "fallback", "abstain", "clarify"]
    if p2.get("test_action_counts") != {action: 10 for action in actions}:
        errors.append("P2 test fallback/abstention/clarification/action coverage drifted")
    if p2.get("content_sha256") != canonical_sha({"requests": p2_rows, "split_counts": p2.get("split_counts")}):
        errors.append("P2 content digest drifted")
    forbidden_features = {"gold_action", "answer_key", "specialist_competence", "split"}
    for row in p2_rows:
        if forbidden_features.intersection(row.get("allowed_route_features", {})):
            errors.append(f"P2 route feature leaks evaluator-only data: {row.get('request_id')}")
    if harm.get("case_count") != 15 or len(harm.get("cases", [])) != 15:
        errors.append("known extra-compute harm set must preserve fifteen cases")
    if any("excluded from new held-out" not in row.get("use", "") for row in harm.get("cases", [])):
        errors.append("known harm cases are not held-out-excluded")

    p3_rows = p3.get("examples", [])
    expected_p3 = {"train": 800, "update": 320, "validation": 160, "test": 160, "deletion": 80, "probe": 80}
    if p3.get("example_count") != 1600 or p3.get("split_counts") != expected_p3 or not unique(p3_rows, "example_id"):
        errors.append("P3 corpus count, splits, or identities drifted")
    if p3.get("content_sha256") != canonical_sha({"examples": p3_rows, "split_counts": p3.get("split_counts")}):
        errors.append("P3 content digest drifted")
    if sum(bool(row.get("deletion_member")) for row in p3_rows) != 80 or sum(bool(row.get("fixed_probe")) for row in p3_rows) != 80:
        errors.append("P3 deletion/probe cohort counts drifted")
    surfaces = inventory.get("surfaces", [])
    if inventory.get("surface_count") != 24 or len(surfaces) != 24 or not unique(surfaces, "surface_id"):
        errors.append("P3 state inventory must contain 24 unique owned surfaces")
    if inventory.get("content_sha256") != canonical_sha(surfaces):
        errors.append("P3 state inventory digest drifted")

    eligibility = data["eligibility"]
    eligibility_prompts = [row.get("prompt", "") for row in eligibility.get("development_tasks", [])]
    combined_text = json.dumps(p1_rows + p2_rows, sort_keys=True)
    if any(prompt and prompt in combined_text for prompt in eligibility_prompts):
        errors.append("runtime eligibility prompt leaked into P1/P2 corpus")

    programs = prereg.get("programs", [])
    if [row.get("priority") for row in programs] != ["P1", "P2", "P3"]:
        errors.append("preregistered program order must be P1/P2/P3")
    expected_residuals = {"P1": ["GW-01", "GW-02", "GW-03"], "P2": ["RD-01", "RD-02", "RD-03", "RD-04"], "P3": ["UU-01", "UU-02", "UU-03", "UU-04"]}
    for row in programs:
        if row.get("residual_ids") != expected_residuals.get(row.get("priority")):
            errors.append(f"{row.get('priority')} residual ownership drifted")
        if not row.get("primary_endpoints") or not row.get("decision_thresholds") or not row.get("stop_rules"):
            errors.append(f"{row.get('priority')} lacks endpoints, thresholds, or stop rules")
    if sum(row.get("model_calls", 0) for row in programs) > prereg.get("global_budget", {}).get("model_calls", 0):
        errors.append("program model calls exceed global budget")
    maximum_generated_tokens = sum(
        row.get("model_calls", 0) * row.get("max_new_tokens_per_call", 0)
        for row in programs
    )
    if maximum_generated_tokens > prereg.get("global_budget", {}).get("generated_tokens", 0):
        errors.append("program maximum generated tokens exceed global budget")
    if prereg.get("shared_governance", {}).get("support_state_effect") != "none_before_accepted_post_run_dispositions":
        errors.append("preregistration launders support state")
    if prereg.get("state") != "draft_inputs_frozen_outcomes_unopened" or len(prereg.get("completion_blockers", [])) != 3:
        errors.append("draft preregistration state/blockers are dishonest")

    doc = data["doc"]
    for fragment in ["36 tasks", "240 requests", "1,600 examples", "24 owned state surfaces", "fifteen v2.1", "outcomes unopened", "not an empirical result"]:
        if fragment not in doc:
            errors.append(f"preregistration report missing: {fragment}")
    return errors


def main() -> None:
    process = subprocess.run([sys.executable, "scripts/build_post_v2_1_preregistration_inputs.py", "--check"], cwd=ROOT, text=True, capture_output=True)
    errors = [] if process.returncode == 0 else [process.stdout + process.stderr]
    data = {
        "prereg": load(f"{BASE}/preregistration.json"),
        "p1": load(f"{BASE}/p1/input/corpus.json"),
        "p2": load(f"{BASE}/p2/input/corpus.json"),
        "harm": load(f"{BASE}/p2/input/known_harm_regression.json"),
        "p3": load(f"{BASE}/p3/input/corpus.json"),
        "inventory": load(f"{BASE}/p3/state_inventory.json"),
        "eligibility": load(f"{BASE}/runtime_eligibility_plan.json"),
        "schema": load("schemas/post_v2_1_evidence_preregistration.schema.json"),
        "doc": (ROOT / "docs/post_v2_1_preregistration.md").read_text(encoding="utf-8"),
    }
    errors.extend(validate(data))
    mutations = []
    names = ["duplicate P1 ID", "eligibility overlap", "fallback erasure", "gold feature leak", "P3 cohort erasure", "inventory omission", "budget overrun", "support promotion", "threshold erasure"]
    for name in names:
        mutant = copy.deepcopy(data)
        if name == "duplicate P1 ID": mutant["p1"]["tasks"][1]["task_id"] = mutant["p1"]["tasks"][0]["task_id"]
        elif name == "eligibility overlap": mutant["p1"]["tasks"][0]["prompt"] = mutant["eligibility"]["development_tasks"][0]["prompt"]
        elif name == "fallback erasure": mutant["p2"]["test_action_counts"]["fallback"] = 0
        elif name == "gold feature leak": mutant["p2"]["requests"][0]["allowed_route_features"]["gold_action"] = "fallback"
        elif name == "P3 cohort erasure": mutant["p3"]["examples"][-81]["deletion_member"] = False
        elif name == "inventory omission": mutant["inventory"]["surfaces"].pop()
        elif name == "budget overrun": mutant["prereg"]["global_budget"]["model_calls"] = 100
        elif name == "support promotion": mutant["prereg"]["shared_governance"]["support_state_effect"] = "promotion"
        elif name == "threshold erasure": mutant["prereg"]["programs"][0]["decision_thresholds"] = {}
        if not validate(mutant):
            errors.append(f"mutation accepted: {name}")
    if errors:
        print("Post-v2.1 preregistration input validation failed:")
        for error in errors: print(f" - {error}")
        raise SystemExit(1)
    print("Post-v2.1 preregistration inputs passed: P1 36/6 families, P2 240 with 10 each test action and 15 harms, P3 1600 plus 24 state surfaces, and 9 rejecting mutations.")


if __name__ == "__main__":
    main()
