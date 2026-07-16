#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE_RUNNER = ROOT / "scripts" / "run_p4_governed_usefulness_local_instrument.py"


def load_base() -> Any:
    spec = importlib.util.spec_from_file_location("p4_local_instrument_base_v9", BASE_RUNNER)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import local instrument base runner")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    base = ROOT / "experiments" / "p4_governed_usefulness"
    module.PREREG = base / "local_instrument_preregistration_v9.json"
    module.TASKS = base / "local_instrument_tasks_v9.json"
    module.LABELS = base / "local_instrument_labels_v9.json"
    module.PROMPT = base / "local_instrument_prompt_v5.md"
    module.RAW = base / "raw" / "local_instrument_qualification_v9_qwen3_8b.json"
    module.RESULT = base / "results" / "local_instrument_qualification_v9.json"
    module.MODEL = Path.home() / ".cache" / "huggingface" / "hub" / "models--mlx-community--Qwen3-8B-4bit" / "snapshots" / "545dc4251c05440727734bcd94334791f6ab0192"
    return module


def scored_a(row: dict[str, Any], expected: dict[str, Any]) -> bool:
    return row["task_id"] == expected["task_id"] and row["terminal_eligibility"] == expected["terminal_eligibility"] and row["residual_class"] == expected["residual_class"]


def scored_b(row: dict[str, Any], expected: dict[str, Any]) -> bool:
    observed = {(row["task_id"], row["terminal_eligibility"]), (row["task_id"], row["residual_class"])}
    required = {(expected["task_id"], expected["terminal_eligibility"]), (expected["task_id"], expected["residual_class"])}
    return observed == required


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--generate", action="store_true")
    parser.add_argument("--evaluate", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if sum((args.generate, args.evaluate, args.self_test)) != 1:
        raise SystemExit("Choose exactly one mode.")
    module = load_base()
    if args.generate:
        module.generate()
    elif args.self_test:
        print(json.dumps(module.self_test(), indent=2))
    else:
        module.evaluator_a = scored_a
        module.evaluator_b = scored_b
        result = module.evaluate()
        raw = module.load(module.RAW)
        labels = {row["task_id"]: row for row in module.load(module.LABELS)["labels"]}
        document = module.parse_candidate_document(raw["stdout"])
        exact_actions = sum(row["remediation_action"] == labels[row["task_id"]]["remediation_action"] for row in document["candidates"])
        result["scored_semantic_fields"] = ["terminal_eligibility", "residual_class"]
        result["remediation_action_required_enum_but_unscored_for_instrument_gate"] = True
        result["exact_remediation_action_count"] = exact_actions
        module.RESULT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(f"V9 action diagnostic: exact={exact_actions}/{result['expected_task_count']}; instrument outcome remains {result['protocol_outcome']}.")


if __name__ == "__main__":
    main()
