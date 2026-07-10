#!/usr/bin/env python3
"""Independent-process observer for the governed repository-change slice."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_changed_paths(repo: Path) -> list[str]:
    completed = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        cwd=repo,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return sorted(line[3:] for line in completed.stdout.splitlines() if len(line) >= 4)


def load_budget_function(path: Path) -> Any:
    spec = importlib.util.spec_from_file_location("fixture_budget", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load fixture budget module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.allocate_budget


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--allowed-path", action="append", default=[])
    parser.add_argument("--proposer-id", required=True)
    parser.add_argument("--verifier-id", required=True)
    args = parser.parse_args()

    repo = args.repo.resolve()
    receipt = json.loads(args.receipt.read_text(encoding="utf-8"))
    budget_path = repo / "src" / "budget.py"
    changed_paths = git_changed_paths(repo)
    unauthorized = sorted(set(changed_paths) - set(args.allowed_path))
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    tests = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests"],
        cwd=repo,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=env,
    )
    allocate_budget = load_budget_function(budget_path)
    behavior = {
        "negative_clamps_to_zero": allocate_budget(-100, 10) == 0,
        "over_ceiling_clamps_to_ceiling": allocate_budget(15, 10) == 10,
        "in_range_preserved": allocate_budget(5, 10) == 5,
    }
    actual_digest = sha256_file(budget_path)
    result = {
        "observer_process": "governed_repository_independent_verifier.py",
        "proposer_id": args.proposer_id,
        "verifier_id": args.verifier_id,
        "independent_identity": args.proposer_id != args.verifier_id,
        "changed_paths": changed_paths,
        "unauthorized_changed_paths": unauthorized,
        "public_tests_pass": tests.returncode == 0,
        "behavior_checks": behavior,
        "safety_constraints_pass": all(behavior.values()),
        "actual_artifact_sha256": actual_digest,
        "claimed_artifact_sha256": receipt.get("artifact_sha256"),
        "receipt_matches_observed_artifact": receipt.get("artifact_sha256") == actual_digest,
        "effect_observed_independently": True,
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
