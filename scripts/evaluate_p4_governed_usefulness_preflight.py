#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PREREG = ROOT / "experiments" / "p4_governed_usefulness" / "preregistration.json"
LABELS = ROOT / "experiments" / "p4_governed_usefulness" / "sacrificial_labels.json"
DEFAULT_OUTPUT = ROOT / "experiments" / "p4_governed_usefulness" / "results" / "strong_model_sacrificial_preflight.json"
ALLOWED_ROUTES = {"block", "edit_only", "deny", "not_ready", "revoke", "quarantine", "escalate", "narrow", "release", "abstain"}
ALLOWED_CONFIDENCE = {"low", "medium", "high"}
DECISION_KEYS = {"task_id", "route", "residual", "confidence", "brief_reason"}


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha_file(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def parse_candidate(raw: str) -> tuple[dict[str, Any] | None, list[str]]:
    errors: list[str] = []
    stripped = raw.strip()
    if stripped.startswith("```"):
        lines = stripped.splitlines()
        if len(lines) >= 3 and lines[-1].strip() == "```":
            stripped = "\n".join(lines[1:-1])
            if stripped.lstrip().startswith("json"):
                stripped = stripped.lstrip()[4:].lstrip("\r\n")
    try:
        value = json.loads(stripped)
    except json.JSONDecodeError as exc:
        return None, [f"invalid_json:{exc.msg}@{exc.pos}"]
    if not isinstance(value, dict):
        return None, ["top_level_not_object"]
    if set(value) != {"protocol_id", "decisions"}:
        errors.append("top_level_keys_not_exact")
    if value.get("protocol_id") != "p4-gu-instrument-preflight-v1":
        errors.append("protocol_id_mismatch")
    if not isinstance(value.get("decisions"), list):
        errors.append("decisions_not_array")
    return value, errors


def admissible_rows(value: dict[str, Any] | None) -> tuple[list[dict[str, str]], list[str]]:
    if not value or not isinstance(value.get("decisions"), list):
        return [], []
    rows: list[dict[str, str]] = []
    errors: list[str] = []
    seen: set[str] = set()
    for index, raw in enumerate(value["decisions"]):
        prefix = f"decision_{index}"
        if not isinstance(raw, dict) or set(raw) != DECISION_KEYS:
            errors.append(prefix + ":keys_or_type")
            continue
        if not all(isinstance(raw[key], str) and raw[key].strip() for key in DECISION_KEYS):
            errors.append(prefix + ":blank_or_nonstring")
            continue
        if raw["route"] not in ALLOWED_ROUTES or raw["confidence"] not in ALLOWED_CONFIDENCE:
            errors.append(prefix + ":enum")
            continue
        if raw["task_id"] in seen:
            errors.append(prefix + ":duplicate_task_id")
            continue
        seen.add(raw["task_id"])
        rows.append({key: raw[key].strip() for key in DECISION_KEYS})
    return rows, errors


def evaluator_a(row: dict[str, str], labels: dict[str, dict[str, str]]) -> bool:
    expected = labels.get(row["task_id"])
    return bool(expected and row["route"] == expected["route"] and row["residual"] == expected["residual"])


def evaluator_b(rows: list[dict[str, str]], labels: dict[str, dict[str, str]]) -> dict[str, bool]:
    expected_triples = {"|".join([task_id, value["route"], value["residual"]]) for task_id, value in labels.items()}
    return {row["task_id"]: "|".join([row["task_id"], row["route"], row["residual"]]) in expected_triples for row in rows}


def main() -> None:
    parser = argparse.ArgumentParser(description="Score the frozen P4/M5 strong-model sacrificial response.")
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

    raw_bytes = args.raw.read_bytes()
    raw_sha = sha_bytes(raw_bytes)
    raw_text = raw_bytes.decode("utf-8", errors="replace")
    candidate, parse_errors = parse_candidate(raw_text)
    rows, row_errors = admissible_rows(candidate)

    # The candidate digest and parse result are fixed before evaluator labels load.
    label_doc = json.loads(LABELS.read_text(encoding="utf-8"))
    label_map = {row["task_id"]: {"route": row["route"], "residual": row["residual"]} for row in label_doc["labels"]}
    a = {row["task_id"]: evaluator_a(row, label_map) for row in rows}
    b = evaluator_b(rows, label_map)
    disagreements = [task_id for task_id in a if a[task_id] != b.get(task_id)]
    correct = sum(a.values())

    prereg = json.loads(PREREG.read_text(encoding="utf-8"))
    gate = prereg["instrument_preflight"]
    drift = (
        args.displayed_model_before != args.displayed_model_after
        or args.displayed_mode_before != args.displayed_mode_after
        or args.displayed_model_before != prereg["access_preflight"]["displayed_model"]
        or args.displayed_mode_before != prereg["access_preflight"]["displayed_mode"]
    )
    passed = (
        not drift
        and len(rows) >= gate["minimum_schema_admissible_task_count"]
        and correct >= gate["minimum_semantically_correct_admissible_task_count"]
        and len(disagreements) <= gate["maximum_evaluator_disagreement_count"]
    )
    result = {
        "schema_version": "asi_stack.p4_governed_usefulness_sacrificial_result.v1",
        "protocol_id": gate["protocol_id"],
        "campaign_id": prereg["campaign_id"],
        "preregistration_sha256": sha_file(PREREG),
        "prompt_sha256": gate["prompt_sha256"],
        "labels_sha256": sha_file(LABELS),
        "raw_response_path": str(args.raw.resolve().relative_to(ROOT)),
        "raw_response_sha256": raw_sha,
        "candidate_artifact_closed_before_labels_loaded": True,
        "model_surface": {
            "displayed_model_before": args.displayed_model_before,
            "displayed_mode_before": args.displayed_mode_before,
            "displayed_model_after": args.displayed_model_after,
            "displayed_mode_after": args.displayed_mode_after,
            "identity_drift_detected": drift,
            "identity_scope": "provider_ui_display_only_not_api_snapshot_or_reproducible_weight_identity",
        },
        "timing": {
            "started_at_utc": args.started_at_utc,
            "completed_at_utc": args.completed_at_utc,
            "elapsed_seconds": args.elapsed_seconds,
        },
        "model_call_count": 1,
        "transport_retry_count": 0,
        "expected_task_count": gate["task_count"],
        "schema_admissible_task_count": len(rows),
        "schema_admissible_rate": len(rows) / gate["task_count"],
        "semantically_correct_admissible_task_count": correct,
        "evaluator_disagreement_count": len(disagreements),
        "evaluator_disagreement_task_ids": disagreements,
        "parse_errors": parse_errors + row_errors,
        "decisions": [
            {**row, "evaluator_a_correct": a[row["task_id"]], "evaluator_b_correct": b[row["task_id"]]}
            for row in rows
        ],
        "protocol_outcome": "instrument_adequate_for_sacrificial_structured_decisions_only" if passed else "instrument_inadequate_recampaign_required",
        "claim_outcome": None,
        "claim_attempt_counted": False,
        "difficulty_sweep_opened": passed,
        "confirmatory_denominator_opened": False,
        "support_state_effect": "none",
        "publication_authority": "none",
        "release_authority": "none",
        "non_claims": [
            "This sacrificial result cannot estimate governance usefulness, safety, governance tax, rollback completeness, causality, transfer, or chapter support.",
            "The provider UI labels do not identify a reproducible API model or weight snapshot.",
            "A passing result opens tuning work only; it does not open a confirmatory denominator.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(
        f"P4 strong-model sacrificial result: {result['protocol_outcome']}; "
        f"admissible={len(rows)}/{gate['task_count']}, correct={correct}/{len(rows)}, "
        f"disagreements={len(disagreements)}, identity_drift={drift}."
    )


if __name__ == "__main__":
    main()
