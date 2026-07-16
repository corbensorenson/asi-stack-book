#!/usr/bin/env python3
"""Freeze the P4/M6 v2 candidate-contract repair after the v1 sacrificial failure."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "experiments/p4_routing_deliberation"
BUILDER = ROOT / "scripts/build_p4_m6_routing_deliberation_campaign.py"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def module() -> Any:
    spec = importlib.util.spec_from_file_location("p4_m6_builder", BUILDER)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import P4/M6 campaign builder")
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def main() -> None:
    if not (BASE / "results/preflight_result.json").is_file():
        raise SystemExit("v1 failure result is required")
    result = json.loads((BASE / "results/preflight_result.json").read_text(encoding="utf-8"))
    if result.get("protocol_outcome") != "instrument_inadequate" or result.get("schema_admissible_count") != 1:
        raise SystemExit("v2 repair authority requires the exact 1/4 v1 schema failure")
    helper = module()
    tasks = [helper.visible_task(helper.TRACKS[i + 4], "automatic", 910 + i) for i in range(4)]
    task_doc = {"schema_version": "asi_stack.p4_m6_tasks.v1", "split": "sacrificial_instrument_v2", "task_count": 4, "tasks": tasks}
    task_path = BASE / "preflight_tasks_v2.json"
    write(task_path, task_doc)
    amendment = {
        "schema_version": "asi_stack.p4_m6_instrument_repair.v2",
        "state": "frozen_after_v1_instrument_failure_before_heldout_generation",
        "v1_result_path": "experiments/p4_routing_deliberation/results/preflight_result.json",
        "v1_result_sha256": sha(BASE / "results/preflight_result.json"),
        "diagnosis": "Three of four raw outputs contained useful answer text but invalid JSON because the model corrupted repeated role labels inside a seven-object array.",
        "single_change": "Replace the repeated candidate-object array with one fixed-key answers object; task content, route enums, model snapshot, temperature, retry count, evidence ceiling, and held-out denominator remain unchanged.",
        "candidate_contract_version": "p4-m6-candidate-contract-v2-fixed-answer-keys",
        "preflight_tasks_v2_sha256": sha(task_path),
        "heldout_open": False,
        "outcome_aware_retry_allowed": False,
        "claim_attempt_count": 0,
        "support_state_effect": "none",
        "publication_authority": "none",
        "release_authority": "none",
    }
    write(BASE / "instrument_repair_v2.json", amendment)
    print("P4/M6 instrument repair v2 frozen before any v2 generation.")


if __name__ == "__main__":
    main()
