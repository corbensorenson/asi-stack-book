#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PREREG = ROOT / "experiments" / "p4_governed_usefulness" / "preregistration_v2.json"
LABELS = ROOT / "experiments" / "p4_governed_usefulness" / "sacrificial_labels_v2.json"
DEFAULT_OUTPUT = ROOT / "experiments" / "p4_governed_usefulness" / "results" / "strong_model_sacrificial_preflight_v2.json"
DECISION_KEYS = {"task_id", "decision_class", "residual_class", "route_detail", "confidence", "brief_reason"}
CONFIDENCE = {"low", "medium", "high"}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse(raw: str, prereg: dict[str, Any]) -> tuple[list[dict[str, str]], list[str]]:
    text = raw.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if len(lines) >= 3 and lines[-1].strip() == "```":
            text = "\n".join(lines[1:-1])
            if text.lstrip().startswith("json"):
                text = text.lstrip()[4:].lstrip("\r\n")
    try:
        value = json.loads(text)
    except json.JSONDecodeError as exc:
        return [], [f"invalid_json:{exc.msg}@{exc.pos}"]
    errors: list[str] = []
    if not isinstance(value, dict) or set(value) != {"protocol_id", "decisions"}:
        return [], ["top_level_contract_invalid"]
    if value.get("protocol_id") != prereg["protocol_id"] or not isinstance(value.get("decisions"), list):
        return [], ["protocol_or_decisions_invalid"]
    classes = set(prereg["instrument"]["canonical_decision_classes"])
    residuals = set(prereg["instrument"]["canonical_residual_classes"])
    rows: list[dict[str, str]] = []
    seen: set[str] = set()
    for index, row in enumerate(value["decisions"]):
        if not isinstance(row, dict) or set(row) != DECISION_KEYS:
            errors.append(f"decision_{index}:keys_or_type")
            continue
        if not all(isinstance(row[key], str) and row[key].strip() for key in DECISION_KEYS):
            errors.append(f"decision_{index}:blank_or_nonstring")
            continue
        if row["decision_class"] not in classes or row["residual_class"] not in residuals or row["confidence"] not in CONFIDENCE:
            errors.append(f"decision_{index}:enum")
            continue
        if row["task_id"] in seen:
            errors.append(f"decision_{index}:duplicate_task_id")
            continue
        seen.add(row["task_id"])
        rows.append({key: row[key].strip() for key in DECISION_KEYS})
    return rows, errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", required=True, type=Path)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--started-at-utc", required=True)
    parser.add_argument("--completed-at-utc", required=True)
    parser.add_argument("--elapsed-seconds", required=True, type=float)
    parser.add_argument("--displayed-model-before", required=True)
    parser.add_argument("--displayed-mode-before", required=True)
    parser.add_argument("--displayed-model-after", required=True)
    parser.add_argument("--displayed-mode-after", required=True)
    args = parser.parse_args()

    prereg = json.loads(PREREG.read_text(encoding="utf-8"))
    raw_bytes = args.raw.read_bytes()
    rows, parse_errors = parse(raw_bytes.decode("utf-8", errors="replace"), prereg)
    # Candidate bytes and digest exist before this evaluator-only load.
    label_doc = json.loads(LABELS.read_text(encoding="utf-8"))
    labels = {row["task_id"]: (row["decision_class"], row["residual_class"]) for row in label_doc["labels"]}
    eval_a = {row["task_id"]: labels.get(row["task_id"]) == (row["decision_class"], row["residual_class"]) for row in rows}
    expected_tokens = {f"{task_id}\x1f{decision}\x1f{residual}" for task_id, (decision, residual) in labels.items()}
    eval_b = {row["task_id"]: f"{row['task_id']}\x1f{row['decision_class']}\x1f{row['residual_class']}" in expected_tokens for row in rows}
    disagreements = [task_id for task_id in eval_a if eval_a[task_id] != eval_b[task_id]]
    correct = sum(eval_a.values())
    surface = prereg["model_surface"]
    drift = (
        args.displayed_model_before != args.displayed_model_after
        or args.displayed_mode_before != args.displayed_mode_after
        or args.displayed_model_before != surface["displayed_model"]
        or args.displayed_mode_before != surface["displayed_mode"]
    )
    gate = prereg["instrument"]
    passed = (
        not drift
        and len(rows) >= gate["minimum_schema_admissible_task_count"]
        and correct >= gate["minimum_semantically_correct_admissible_task_count"]
        and len(disagreements) <= gate["maximum_evaluator_disagreement_count"]
    )
    result = {
        "schema_version": "asi_stack.p4_governed_usefulness_sacrificial_result.v2",
        "protocol_id": prereg["protocol_id"],
        "campaign_id": prereg["campaign_id"],
        "preregistration_sha256": sha(PREREG),
        "prompt_sha256": gate["prompt_sha256"],
        "labels_sha256": sha(LABELS),
        "raw_response_path": str(args.raw.resolve().relative_to(ROOT)),
        "raw_response_sha256": hashlib.sha256(raw_bytes).hexdigest(),
        "candidate_artifact_closed_before_labels_loaded": True,
        "model_surface": {
            "displayed_model_before": args.displayed_model_before,
            "displayed_mode_before": args.displayed_mode_before,
            "displayed_model_after": args.displayed_model_after,
            "displayed_mode_after": args.displayed_mode_after,
            "identity_drift_detected": drift,
            "identity_scope": surface["identity_scope"],
        },
        "timing": {"started_at_utc": args.started_at_utc, "completed_at_utc": args.completed_at_utc, "elapsed_seconds": args.elapsed_seconds},
        "model_call_count": 1,
        "transport_retry_count": 0,
        "expected_task_count": gate["task_count"],
        "schema_admissible_task_count": len(rows),
        "schema_admissible_rate": len(rows) / gate["task_count"],
        "semantically_correct_admissible_task_count": correct,
        "evaluator_disagreement_count": len(disagreements),
        "evaluator_disagreement_task_ids": disagreements,
        "parse_errors": parse_errors,
        "decisions": [{**row, "evaluator_a_correct": eval_a[row["task_id"]], "evaluator_b_correct": eval_b[row["task_id"]]} for row in rows],
        "protocol_outcome": gate["pass_outcome"] if passed else gate["fail_outcome"],
        "claim_outcome": None,
        "claim_attempt_counted": False,
        "difficulty_sweep_opened": passed,
        "confirmatory_denominator_opened": False,
        "v1_result_rescored": False,
        "support_state_effect": "none",
        "publication_authority": "none",
        "release_authority": "none",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"P4 v2 sacrificial result: {result['protocol_outcome']}; admissible={len(rows)}/6, correct={correct}/{len(rows)}, disagreements={len(disagreements)}, identity_drift={drift}.")


if __name__ == "__main__":
    main()
