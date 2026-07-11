#!/usr/bin/env python3
"""Validate and red-team the outcome-unopened post-v2.1 executable setup."""

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
MANIFEST = ROOT / BASE / "setup_manifest.json"
EXPECTED_FILES = [
    "scripts/post_v2_1_p1_observer.py", "scripts/run_post_v2_1_p1.py",
    "scripts/post_v2_1_p2_evaluator.py", "scripts/run_post_v2_1_p2.py",
    "scripts/post_v2_1_p3_observer.py", "scripts/run_post_v2_1_p3.py",
    "scripts/build_post_v2_1_setup_manifest.py", "scripts/validate_post_v2_1_evidence_setup.py",
    "schemas/post_v2_1_evidence_setup.schema.json",
]


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text())


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def commit_paths(commit: str) -> set[str]:
    process = subprocess.run(["git", "ls-tree", "-r", "--name-only", commit], cwd=ROOT, text=True, capture_output=True)
    if process.returncode:
        return set()
    return set(process.stdout.splitlines())


def commit_blob(commit: str, path: str) -> bytes | None:
    process = subprocess.run(["git", "show", f"{commit}:{path}"], cwd=ROOT, capture_output=True)
    return process.stdout if process.returncode == 0 else None


def validate(data: dict, check_git: bool = True) -> list[str]:
    manifest, prereg, p1, p2, p3, inventory, schema = (data[key] for key in ["manifest", "prereg", "p1", "p2", "p3", "inventory", "schema"])
    errors = [f"setup schema: {error.message}" for error in sorted(Draft202012Validator(schema).iter_errors(manifest), key=lambda value: list(value.path))]
    files = manifest.get("implementation_files", [])
    if [row.get("path") for row in files] != EXPECTED_FILES:
        errors.append("implementation file order or membership drifted")
    for row in files:
        path = ROOT / row.get("path", "")
        if not path.is_file() or row.get("sha256") != sha_bytes(path.read_bytes()):
            errors.append(f"implementation digest drifted: {row.get('path')}")
    programs = manifest.get("programs", [])
    if [row.get("priority") for row in programs] != ["P1", "P2", "P3"]:
        errors.append("setup program order drifted")
    if len(programs) == 3:
        if programs[0].get("phase_calls") != {"development": 12, "calibration": 24, "test": 36} or programs[0].get("model_calls") != 72:
            errors.append("P1 phased call schedule drifted")
        if programs[1].get("phase_calls") != {"validation": 20, "test": 240} or programs[1].get("model_calls") != 260:
            errors.append("P2 phased call schedule drifted")
        if programs[2].get("model_calls") != 0 or programs[2].get("state_surfaces") != 24:
            errors.append("P3 model-call or state-surface boundary drifted")
    budget = manifest.get("combined_budget", {})
    if budget != {"model_calls": 332, "generated_tokens": 59960, "global_call_ceiling": 340, "global_token_ceiling": 60000}:
        errors.append("combined setup budget drifted")
    if sum(row.get("model_calls", 0) for row in programs) > budget.get("global_call_ceiling", 0):
        errors.append("program calls exceed global ceiling")
    if sum(row.get("generated_token_ceiling", 0) for row in programs) > budget.get("global_token_ceiling", 0):
        errors.append("program tokens exceed global ceiling")
    guards = manifest.get("execution_guard", {})
    expected_guards = {
        "outcomes_must_be_absent_at_freeze": True, "runners_require_final_preregistration_state": True,
        "overwrite_or_retry_flag": False, "network_after_freeze": False, "model_snapshot_local_only": True,
        "hidden_chain_of_thought_retained": False, "external_service_spend_usd": 0,
    }
    if guards != expected_guards:
        errors.append("execution guard drifted")
    roles = manifest.get("role_interfaces", {})
    if "separate" not in roles.get("P1_effect_observer", "") or "separate" not in roles.get("P2_evaluator", "") or "separate" not in roles.get("P3_state_observer", ""):
        errors.append("observer/evaluator implementation separation collapsed")
    if manifest.get("support_state_effect") != "none_before_accepted_post_run_dispositions":
        errors.append("setup launders support state")
    if manifest.get("parent_input_commit") != "52925c426" or manifest.get("amendment_ref") != f"{BASE}/amendments/preregistration_inputs_v1.json":
        errors.append("input-freeze lineage drifted")
    if manifest.get("setup_amendment_ref") != f"{BASE}/amendments/setup_validator_v1.json":
        errors.append("setup-validator amendment lineage drifted")
    if manifest.get("source_gap_scan_ref") != "docs/post_v2_1_focused_source_gap_scan.md" or prereg.get("source_gap_scan_ref") != manifest.get("source_gap_scan_ref"):
        errors.append("focused source-gap scan is not bound")
    state, setup_commit = manifest.get("state"), manifest.get("setup_commit")
    outputs = [path for row in programs for path in row.get("outcome_outputs", [])]
    if state == "implementations_installed_setup_commit_pending":
        if setup_commit is not None or prereg.get("state") != "draft_inputs_frozen_outcomes_unopened":
            errors.append("installed setup prematurely claims final freeze")
        if any((ROOT / path).exists() for path in outputs):
            errors.append("outcomes exist before setup commit binding")
    elif state == "frozen_before_outcome_runs":
        if not isinstance(setup_commit, str) or len(setup_commit) != 40 or prereg.get("state") != "frozen_before_outcome_runs":
            errors.append("final setup/preregistration binding is incomplete")
        elif check_git:
            paths = commit_paths(setup_commit)
            if not paths or any(path in paths for path in outputs):
                errors.append("setup commit is missing or already contains outcomes")
            for row in files:
                blob = commit_blob(setup_commit, row["path"])
                if blob is None or sha_bytes(blob) != row["sha256"]:
                    errors.append(f"setup commit implementation mismatch: {row['path']}")
    if p1.get("content_sha256") != prereg["programs"][0].get("corpus_sha256"):
        errors.append("P1 setup corpus binding drifted")
    if p2.get("content_sha256") != prereg["programs"][1].get("corpus_sha256"):
        errors.append("P2 setup corpus binding drifted")
    if p3.get("content_sha256") != prereg["programs"][2].get("corpus_sha256"):
        errors.append("P3 setup corpus binding drifted")
    if inventory.get("surface_count") != 24:
        errors.append("P3 inventory no longer contains 24 surfaces")

    sources = {path: (ROOT / path).read_text() for path in EXPECTED_FILES if path.endswith(".py")}
    p1_source, p2_source, p3_source = sources["scripts/run_post_v2_1_p1.py"], sources["scripts/run_post_v2_1_p2.py"], sources["scripts/run_post_v2_1_p3.py"]
    if 'local_files_only=True' not in p1_source or 'OBSERVER.as_posix()' not in p1_source or '--force' in p1_source:
        errors.append("P1 local-only observer/no-overwrite boundary drifted")
    if 'local_files_only=True' not in p2_source or 'EVALUATOR.as_posix()' not in p2_source or '--force' in p2_source:
        errors.append("P2 local-only evaluator/no-overwrite boundary drifted")
    learned_body = p2_source.split("def learned_action", 1)[1].split("def rule_action", 1)[0]
    if 'allowed_route_features' not in learned_body or 'gold_action' in learned_body or 'answer_key' in learned_body:
        errors.append("P2 learned router leaks evaluator-only fields")
    authority_body = p3_source.split("def run_arm", 1)[1].split("def write_json", 1)[0]
    if 'rows["test"]' in authority_body or 'rows["deletion"]' in authority_body or 'rows["probe"]' in authority_body:
        errors.append("P3 authority selection consumes forbidden outcome splits")
    if 'OBSERVER.as_posix()' not in p3_source or 'torch.use_deterministic_algorithms(True)' not in p3_source or '--force' in p3_source:
        errors.append("P3 observer/determinism/no-overwrite boundary drifted")
    return errors


def main() -> None:
    data = {
        "manifest": load(f"{BASE}/setup_manifest.json"), "prereg": load(f"{BASE}/preregistration.json"),
        "p1": load(f"{BASE}/p1/input/corpus.json"), "p2": load(f"{BASE}/p2/input/corpus.json"),
        "p3": load(f"{BASE}/p3/input/corpus.json"), "inventory": load(f"{BASE}/p3/state_inventory.json"),
        "schema": load("schemas/post_v2_1_evidence_setup.schema.json"),
    }
    errors = validate(data)
    for command in data["manifest"].get("preflight_commands", []):
        process = subprocess.run(command.split(), cwd=ROOT, text=True, capture_output=True, timeout=60)
        if process.returncode:
            errors.append(f"preflight failed: {command}: {process.stdout}{process.stderr}")
    mutations = [
        "implementation digest", "program order", "P1 calls", "P2 calls", "P3 surface count",
        "token budget", "observer collapse", "outcome guard", "support promotion", "setup commit shape",
    ]
    for name in mutations:
        mutant = copy.deepcopy(data)
        if name == "implementation digest": mutant["manifest"]["implementation_files"][0]["sha256"] = "0" * 64
        elif name == "program order": mutant["manifest"]["programs"].reverse()
        elif name == "P1 calls": mutant["manifest"]["programs"][0]["model_calls"] = 73
        elif name == "P2 calls": mutant["manifest"]["programs"][1]["phase_calls"]["test"] = 241
        elif name == "P3 surface count": mutant["manifest"]["programs"][2]["state_surfaces"] = 23
        elif name == "token budget": mutant["manifest"]["combined_budget"]["generated_tokens"] = 60001
        elif name == "observer collapse": mutant["manifest"]["role_interfaces"]["P1_effect_observer"] = "same proposer"
        elif name == "outcome guard": mutant["manifest"]["execution_guard"]["outcomes_must_be_absent_at_freeze"] = False
        elif name == "support promotion": mutant["manifest"]["support_state_effect"] = "promote"
        elif name == "setup commit shape": mutant["manifest"]["setup_commit"] = "0" * 39
        if not validate(mutant, check_git=False):
            errors.append(f"setup mutation accepted: {name}")
    if errors:
        print("Post-v2.1 executable setup validation failed:")
        for error in errors: print(f" - {error}")
        raise SystemExit(1)
    print("Post-v2.1 executable setup passed: six separated runner/observer/evaluator implementations, 332 calls/59,960 maximum tokens, 24 P3 state surfaces, three no-outcome preflights, and 10 rejecting mutations.")


if __name__ == "__main__":
    main()
