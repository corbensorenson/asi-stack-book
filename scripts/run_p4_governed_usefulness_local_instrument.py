#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "experiments" / "p4_governed_usefulness"
PREREG = BASE / "local_instrument_preregistration.json"
TASKS = BASE / "local_instrument_tasks.json"
LABELS = BASE / "local_instrument_labels.json"
PROMPT = BASE / "local_instrument_prompt.md"
RAW = BASE / "raw" / "local_instrument_qualification_qwen3_4b.json"
RESULT = BASE / "results" / "local_instrument_qualification.json"
MODEL = Path.home() / ".cache" / "huggingface" / "hub" / "models--mlx-community--Qwen3-4B-4bit" / "snapshots" / "4dcb3d101c2a062e5c1d4bb173588c54ea6c4d25"
EXPECTED_KEYS = {"task_id", "terminal_eligibility", "remediation_action", "residual_class", "brief_reason"}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def digest(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def public_path(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def build_prompt() -> str:
    tasks = load(TASKS)
    visible = {
        "protocol_id": tasks["protocol_id"],
        "decision_contract": tasks["decision_contract"],
        "residual_classes": tasks["residual_classes"],
        "tasks": tasks["tasks"],
    }
    return PROMPT.read_text(encoding="utf-8") + "\n\nCANDIDATE-VISIBLE TASK DOCUMENT\n" + json.dumps(visible, indent=2)


def generate() -> dict[str, Any]:
    prereg = load(PREREG)
    if RAW.exists() or RESULT.exists():
        raise SystemExit("Protocol v3 is one-shot: a raw response or result already exists.")
    if not MODEL.exists():
        raise SystemExit("Frozen local Qwen3-4B-4bit snapshot is unavailable; freeze a new protocol identity for substitution.")
    prompt = build_prompt()
    command = [
        "mlx_lm.generate", "--model", str(MODEL), "--prompt", "-",
        "--max-tokens", "1800", "--temp", "0", "--seed", "20260716",
        "--chat-template-config", '{"enable_thinking":false}', "--verbose", "False",
    ]
    started = time.perf_counter()
    completed = subprocess.run(command, input=prompt, text=True, capture_output=True, check=False)
    elapsed = round(time.perf_counter() - started, 6)
    receipt = {
        "schema_version": "asi_stack.p4_governed_usefulness_local_instrument_raw.v1",
        "protocol_id": prereg["protocol_id"],
        "candidate_generator_role": prereg["candidate_generator"]["role"],
        "model_repository": prereg["candidate_generator"]["model_repository"],
        "snapshot_commit": prereg["candidate_generator"]["snapshot_commit"],
        "claim_ceiling": prereg["candidate_generator"]["claim_ceiling"],
        "prompt_sha256": digest_bytes(prompt.encode("utf-8")),
        "tasks_sha256": digest(TASKS),
        "labels_loaded_by_generator": False,
        "generation_parameters": prereg["candidate_generator"]["generation"],
        "process_exit_code": completed.returncode,
        "elapsed_seconds": elapsed,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "retry_count": 0,
        "support_state_effect": "none",
    }
    RAW.parent.mkdir(parents=True, exist_ok=True)
    RAW.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(f"Local instrument candidate generation closed: exit={completed.returncode}, elapsed={elapsed}s, raw_sha256={digest(RAW)}")
    return receipt


def parse_candidate_document(raw_text: str) -> Any:
    text = raw_text.strip()
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    start = text.find("{")
    end = text.rfind("}")
    if start < 0 or end < start:
        raise ValueError("no JSON object found")
    return json.loads(text[start:end + 1])


def schema_admissible(row: Any, task_ids: set[str], enums: dict[str, set[str]]) -> bool:
    return (
        isinstance(row, dict)
        and set(row) == EXPECTED_KEYS
        and row.get("task_id") in task_ids
        and row.get("terminal_eligibility") in enums["eligibility"]
        and row.get("remediation_action") in enums["actions"]
        and row.get("residual_class") in enums["residuals"]
        and isinstance(row.get("brief_reason"), str)
        and bool(row["brief_reason"].strip())
    )


def evaluator_a(row: dict[str, Any], expected: dict[str, Any]) -> bool:
    return all(row.get(key) == expected.get(key) for key in ("task_id", "terminal_eligibility", "remediation_action", "residual_class"))


def evaluator_b(row: dict[str, Any], expected: dict[str, Any]) -> bool:
    observed = {(key, row[key]) for key in ("terminal_eligibility", "remediation_action", "residual_class")}
    required = {(key, expected[key]) for key in ("terminal_eligibility", "remediation_action", "residual_class")}
    return row["task_id"] == expected["task_id"] and observed == required


def evaluate() -> dict[str, Any]:
    prereg = load(PREREG)
    if not RAW.exists():
        raise SystemExit("No closed raw candidate artifact exists.")
    raw_sha = digest(RAW)
    raw = load(RAW)
    # The candidate artifact is closed and hashed before the evaluator-only file loads.
    labels = load(LABELS)
    tasks = load(TASKS)
    task_ids = {row["task_id"] for row in tasks["tasks"]}
    enums = {
        "eligibility": set(tasks["decision_contract"]["terminal_eligibility"]),
        "actions": set(tasks["decision_contract"]["remediation_actions"]),
        "residuals": set(tasks["residual_classes"]),
    }
    parse_error: str | None = None
    try:
        document = parse_candidate_document(raw.get("stdout", ""))
    except (ValueError, json.JSONDecodeError) as error:
        document = {}
        parse_error = str(error)
    rows = document.get("candidates", []) if isinstance(document, dict) else []
    expected_map = {row["task_id"]: row for row in labels["labels"]}
    seen: set[str] = set()
    records: list[dict[str, Any]] = []
    disagreements = 0
    admissible_count = 0
    correct_count = 0
    for row in rows if isinstance(rows, list) else []:
        admissible = schema_admissible(row, task_ids, enums)
        task_id = row.get("task_id") if isinstance(row, dict) else None
        duplicate = task_id in seen
        if isinstance(task_id, str):
            seen.add(task_id)
        a = admissible and not duplicate and evaluator_a(row, expected_map[task_id]) if task_id in expected_map else False
        b = admissible and not duplicate and evaluator_b(row, expected_map[task_id]) if task_id in expected_map else False
        disagreements += a != b
        admissible_count += admissible and not duplicate
        correct_count += a and b
        records.append({"task_id": task_id, "schema_admissible": admissible and not duplicate, "duplicate": duplicate, "evaluator_a_correct": a, "evaluator_b_correct": b})
    floors = prereg["instrument"]
    passed = (
        raw.get("process_exit_code") == 0
        and parse_error is None
        and isinstance(document, dict)
        and set(document) == {"protocol_id", "candidates"}
        and document.get("protocol_id") == prereg["protocol_id"]
        and seen == task_ids
        and len(rows) == len(task_ids)
        and admissible_count >= floors["minimum_schema_admissible_task_count"]
        and correct_count >= floors["minimum_semantically_correct_admissible_task_count"]
        and disagreements <= floors["maximum_evaluator_disagreement_count"]
    )
    result = {
        "schema_version": "asi_stack.p4_governed_usefulness_local_instrument_result.v1",
        "protocol_id": prereg["protocol_id"],
        "preregistration_path": public_path(PREREG),
        "preregistration_sha256": digest(PREREG),
        "raw_response_path": public_path(RAW),
        "raw_response_sha256": raw_sha,
        "candidate_artifact_closed_before_labels_loaded": True,
        "labels_sha256": digest(LABELS),
        "candidate_generator_role": raw.get("candidate_generator_role"),
        "model_repository": raw.get("model_repository"),
        "snapshot_commit": raw.get("snapshot_commit"),
        "claim_ceiling": raw.get("claim_ceiling"),
        "expected_task_count": len(task_ids),
        "schema_admissible_task_count": int(admissible_count),
        "semantically_correct_admissible_task_count": int(correct_count),
        "evaluator_implementation_count": 2,
        "evaluator_disagreement_count": int(disagreements),
        "parse_error": parse_error,
        "records": records,
        "protocol_outcome": floors["pass_outcome"] if passed else floors["fail_outcome"],
        "difficulty_sweep_opened": bool(passed),
        "confirmatory_denominator_opened": False,
        "claim_attempt_counted": False,
        "support_state_effect": "none",
        "publication_authority": "none",
        "release_authority": "none"
    }
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"Local instrument qualification: {result['protocol_outcome']}; schema={admissible_count}/{len(task_ids)}, semantic={correct_count}/{len(task_ids)}, disagreement={disagreements}.")
    return result


def self_test() -> dict[str, Any]:
    label = load(LABELS)["labels"][0]
    base = {**label, "brief_reason": "bounded canary"}
    task_ids = {label["task_id"]}
    tasks = load(TASKS)
    enums = {"eligibility": set(tasks["decision_contract"]["terminal_eligibility"]), "actions": set(tasks["decision_contract"]["remediation_actions"]), "residuals": set(tasks["residual_classes"])}
    mutations = [
        {**base, "terminal_eligibility": "eligible"},
        {**base, "remediation_action": "allow"},
        {**base, "residual_class": "none"},
        {**base, "task_id": "unknown"},
        {**base, "brief_reason": ""},
        {key: value for key, value in base.items() if key != "brief_reason"},
        {**base, "extra": True},
        {**base, "terminal_eligibility": "maybe"},
    ]
    semantic_rejections = sum(not (evaluator_a(row, label) and evaluator_b(row, label)) for row in mutations[:3])
    schema_rejections = sum(not schema_admissible(row, task_ids, enums) for row in mutations[3:])
    return {"valid_canary_accepted": schema_admissible(base, task_ids, enums) and evaluator_a(base, label) and evaluator_b(base, label), "semantic_mutation_rejection_count": semantic_rejections, "schema_mutation_rejection_count": schema_rejections, "total_mutation_rejection_count": semantic_rejections + schema_rejections, "support_state_effect": "none"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--generate", action="store_true")
    parser.add_argument("--evaluate", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    selected = sum((args.generate, args.evaluate, args.self_test))
    if selected != 1:
        raise SystemExit("Choose exactly one of --generate, --evaluate, or --self-test.")
    if args.generate:
        generate()
    elif args.evaluate:
        evaluate()
    else:
        print(json.dumps(self_test(), indent=2))


if __name__ == "__main__":
    main()
