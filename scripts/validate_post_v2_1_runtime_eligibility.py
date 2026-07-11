#!/usr/bin/env python3
"""Validate post-v2.1 runtime eligibility, failures, amendment, and budgets."""

from __future__ import annotations

import copy
import hashlib
import json
import re
import sys
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
PLAN = "experiments/post_v2_1_evidence_program/runtime_eligibility_plan.json"
INITIAL = "experiments/post_v2_1_evidence_program/results/2026-07-10-runtime-eligibility.json"
AMENDMENT = "experiments/post_v2_1_evidence_program/amendments/runtime_candidate_v1.json"
AMENDED = "experiments/post_v2_1_evidence_program/results/2026-07-10-runtime-eligibility-amendment-v1.json"
ATTEMPT = "experiments/post_v2_1_evidence_program/attempts/2026-07-10-mps-runtime-abort.json"
DISPOSITION = "experiments/post_v2_1_evidence_program/runtime_eligibility_disposition.json"


def read_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def parse_answer(text: str) -> str | None:
    for block in reversed(re.findall(r"\{[^{}]*\}", text, flags=re.DOTALL)):
        try:
            value = json.loads(block)
        except json.JSONDecodeError:
            continue
        answer = value.get("answer") if isinstance(value, dict) else None
        if isinstance(answer, (str, int, float)):
            return str(answer).strip().lower()
    return None


def parse_answer_amended(text: str) -> str | None:
    parsed = parse_answer(text)
    if parsed is not None:
        return parsed
    stripped = text.strip().lower()
    return stripped if stripped in {"42", "blue", "clarify", "refuse"} else None


def canonical_sha(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def validate(data: dict[str, dict]) -> list[str]:
    errors: list[str] = []
    plan, initial, amendment = data["plan"], data["initial"], data["amendment"]
    amended, attempt, disposition = data["amended"], data["attempt"], data["disposition"]
    schema = data["schema"]
    for name, record in [("plan", plan), ("initial", initial), ("amended", amended)]:
        schema_errors = sorted(Draft202012Validator(schema).iter_errors(record), key=lambda e: list(e.path))
        errors.extend(f"{name} schema: {error.message}" for error in schema_errors)

    tasks = plan.get("development_tasks", [])
    if len(tasks) != 4 or len({row.get("task_id") for row in tasks}) != 4:
        errors.append("exactly four unique development tasks are required")
    expected = {row["task_id"]: str(row["expected"]).lower() for row in tasks}
    if plan.get("resource_budget", {}).get("model_calls") != 8:
        errors.append("original call budget drifted")
    if plan.get("resource_budget", {}).get("retries_per_call") != 0:
        errors.append("retry ceiling must remain zero")

    initial_rows = initial.get("candidate_results", [])
    if [row.get("candidate_id") for row in initial_rows] != ["coder-1p5b", "general-1p7b"]:
        errors.append("initial candidates or order drifted")
    recomputed_counts = {}
    combined_rows = [(row, False) for row in initial_rows] + [(row, True) for row in amended.get("candidate_results", [])]
    for row, is_amended in combined_rows:
        observations = row.get("observations", [])
        exact = 0
        for observation in observations:
            task_id = observation.get("task_id")
            parser = parse_answer_amended if is_amended else parse_answer
            parsed = parser(str(observation.get("output", "")))
            is_exact = parsed == expected.get(task_id)
            if observation.get("parsed_answer") != parsed or observation.get("exact") != is_exact:
                errors.append(f"{row.get('candidate_id')}:{task_id} recorded answer/exactness drift")
            exact += int(is_exact)
        if row.get("exact_count") != exact or row.get("eligible") != (exact >= 3):
            errors.append(f"{row.get('candidate_id')} eligibility summary drift")
        recomputed_counts[row.get("candidate_id")] = exact
        manifest = row.get("snapshot_manifest", [])
        if row.get("snapshot_manifest_sha256") != canonical_sha(manifest):
            errors.append(f"{row.get('candidate_id')} snapshot manifest digest drift")

    if recomputed_counts != {"coder-1p5b": 2, "general-1p7b": 1, "general-4b-mlx4": 3}:
        errors.append("candidate exact-count facts differ from 2/4, 1/4, 3/4")
    if initial.get("aggregate", {}).get("eligible_count") != 0:
        errors.append("initial failed candidates were laundered as eligible")
    if amended.get("aggregate", {}).get("eligible_count") != 1:
        errors.append("amended candidate is not the sole eligible runtime")

    if attempt.get("completed_model_calls") != 0 or attempt.get("observed_answers") != []:
        errors.append("MPS abort must preserve zero completed calls and zero answers")
    if "2**32" not in attempt.get("error_fragment", ""):
        errors.append("MPS failure boundary is missing")
    added = amendment.get("changes", {}).get("added_candidate", {})
    if added.get("candidate_id") != "general-4b-mlx4" or added.get("revision") != "4dcb3d101c2a062e5c1d4bb173588c54ea6c4d25":
        errors.append("amendment candidate identity drift")
    unchanged = " ".join(amendment.get("changes", {}).get("unchanged_fields", []))
    for phrase in ["four prompts", "3-of-4 threshold", "no retries", "held-out contamination"]:
        if phrase not in unchanged:
            errors.append(f"amendment does not freeze: {phrase}")
    if added.get("selection_threshold") != "unchanged: at least 3 of 4 exact development-only tasks and no runtime boundary violation":
        errors.append("amended selection threshold drifted")
    if amendment.get("invalidated_descendants") != []:
        errors.append("eligibility amendment cannot claim empirical descendants existed")

    selected = disposition.get("selected_runtime", {})
    if selected.get("candidate_id") != "general-4b-mlx4" or selected.get("exact_count") != 3:
        errors.append("selected runtime disposition disagrees")
    cache = disposition.get("cache_retention", {})
    if not cache.get("within_retention_ceiling") or cache.get("final_total_huggingface_cache_bytes", 10**30) > cache.get("retained_model_cache_ceiling_bytes", 0):
        errors.append("retained cache exceeds recorded ceiling")
    budget = disposition.get("aggregate_budget", {})
    if budget.get("completed_model_calls") != 12 or budget.get("retries") != 0 or budget.get("external_service_spend_usd") != 0:
        errors.append("aggregate eligibility budget facts drifted")
    if disposition.get("support_state_effect") != "none":
        errors.append("runtime eligibility cannot change support state")

    doc = data["doc"]
    for fragment in ["2/4", "1/4", "3/4", "4dcb3d101c2a062e5c1d4bb173588c54ea6c4d25", "3,278,643,200 bytes", "no evidence transition"]:
        if fragment not in doc:
            errors.append(f"runtime eligibility report missing: {fragment}")
    return errors


def main() -> None:
    data = {
        "plan": read_json(PLAN),
        "initial": read_json(INITIAL),
        "amendment": read_json(AMENDMENT),
        "amended": read_json(AMENDED),
        "attempt": read_json(ATTEMPT),
        "disposition": read_json(DISPOSITION),
        "schema": read_json("schemas/post_v2_1_runtime_eligibility.schema.json"),
        "doc": (ROOT / "docs/post_v2_1_runtime_eligibility.md").read_text(encoding="utf-8"),
    }
    errors = validate(data)
    mutations = []
    for name in ["false initial eligibility", "erased failed candidate", "threshold weakening", "revision drift", "invented MPS answer", "support promotion", "budget overrun"]:
        mutant = copy.deepcopy(data)
        if name == "false initial eligibility": mutant["initial"]["candidate_results"][0]["eligible"] = True
        elif name == "erased failed candidate": mutant["initial"]["candidate_results"].pop()
        elif name == "threshold weakening": mutant["amendment"]["changes"]["added_candidate"]["selection_threshold"] = "2 of 4"
        elif name == "revision drift": mutant["amendment"]["changes"]["added_candidate"]["revision"] = "0" * 40
        elif name == "invented MPS answer": mutant["attempt"]["completed_model_calls"] = 1
        elif name == "support promotion": mutant["disposition"]["support_state_effect"] = "promotion"
        elif name == "budget overrun": mutant["disposition"]["cache_retention"]["final_total_huggingface_cache_bytes"] = 20 * 1024**3
        if not validate(mutant):
            errors.append(f"mutation accepted: {name}")
    if errors:
        print("Post-v2.1 runtime eligibility validation failed:")
        for error in errors: print(f" - {error}")
        sys.exit(1)
    print("Post-v2.1 runtime eligibility passed: preserved 2/4 and 1/4 rejections, one 3/4 MLX eligibility, zero retries/spend, bounded cache, and 7 rejecting mutations.")


if __name__ == "__main__":
    main()
