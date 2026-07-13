#!/usr/bin/env python3
"""Run frozen QCSA systems on held-out inputs without loading evaluator labels."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "experiments/qcsa_reference"
sys.path.insert(0, str(PACKAGE_ROOT))

from qcsa_ref.evaluation import SYSTEMS, predict  # noqa: E402


INPUTS = PACKAGE_ROOT / "corpus/inputs.json"
PLAN = PACKAGE_ROOT / "test_plan.json"
BUDGET = PACKAGE_ROOT / "budgets.json"
OUT = PACKAGE_ROOT / "results/evaluation_predictions.json"
AUTHORIZATION = ROOT / "roadmap_records/qcsa_evaluation_execution_authorization.json"
SEEDS = [11, 29, 47]


def canonical_bytes(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def main() -> None:
    for command in [
        [sys.executable, "scripts/validate_qcsa_reference_implementation_freeze.py"],
        [sys.executable, "scripts/validate_qcsa_reference_implementation.py"],
        [sys.executable, "scripts/validate_qcsa_evaluation_corpus.py"],
    ]:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    if not AUTHORIZATION.is_file():
        raise SystemExit("held-out execution remains sealed: missing evaluation execution authorization")
    authorization = json.loads(AUTHORIZATION.read_text(encoding="utf-8"))
    setup_commit = authorization.get("setup_commit", "")
    if authorization.get("state") != "authorized_for_outcome_execution" or len(setup_commit) != 40:
        raise SystemExit("held-out execution remains sealed: authorization is not active")
    if subprocess.run(["git", "merge-base", "--is-ancestor", setup_commit, "HEAD"], cwd=ROOT, check=False).returncode:
        raise SystemExit("held-out execution remains sealed: setup commit is not in history")
    inputs_record = json.loads(INPUTS.read_text(encoding="utf-8"))
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    budget = json.loads(BUDGET.read_text(encoding="utf-8"))
    held_out = [row for row in inputs_record["cases"] if row["split"] == "held_out"]
    if len(held_out) != plan["corpus"]["held_out_cases"] or SEEDS != plan["seeds"]:
        raise SystemExit("held-out case or seed binding drifted")
    records = []
    for seed in SEEDS:
        for system in SYSTEMS:
            for case in held_out:
                output = predict(system, case, seed)
                if output == {"action": "request_clarification"}:
                    if not case["interaction_fixture"]["clarification_available"]:
                        raise SystemExit(f"{system}/{case['case_id']}: requested unavailable clarification")
                    output = predict(system, case, seed, case["interaction_fixture"]["clarification_tokens"])
                if output["questions"] > budget["max_questions_per_case"] or output["retrievals"] > budget["max_retrievals_per_case"] or output["tool_calls"] > budget["max_tool_attempts_per_case"]:
                    raise SystemExit(f"{system}/{case['case_id']}: per-case budget exceeded")
                row = {"case_id": case["case_id"], "family": case["family"], "seed": seed, "system": system, "output": output}
                row["record_digest"] = hashlib.sha256(canonical_bytes(row)).hexdigest()
                records.append(row)
    records.sort(key=lambda row: (row["seed"], row["system"], row["case_id"]))
    record = {
        "schema_version": "asi_stack.qcsa_evaluation_predictions.v0",
        "state": "held_out_predictions_complete_labels_not_loaded_by_runner",
        "input_ref": "experiments/qcsa_reference/corpus/inputs.json",
        "input_sha256": hashlib.sha256(INPUTS.read_bytes()).hexdigest(),
        "plan_ref": "experiments/qcsa_reference/test_plan.json",
        "systems": list(SYSTEMS),
        "seeds": SEEDS,
        "held_out_case_count": len(held_out),
        "prediction_count": len(records),
        "records": records,
        "execution_accounting": {
            "decision_latency_field": "deterministic operation-count proxy; excluded from production-latency inference",
            "network_calls": 0,
            "service_spend_usd": 0,
        },
        "support_state_effect": "none",
        "non_claims": [
            "This file contains unscored held-out predictions and does not establish any evaluation outcome.",
            "The runner imports no evaluator label file; clarification tokens are released only after an explicit request.",
            "Deterministic latency is an accounting proxy, not production latency."
        ],
    }
    OUT.write_bytes(canonical_bytes(record))
    print(f"Wrote {len(records)} deterministic QCSA held-out predictions: {len(SYSTEMS)} systems x {len(SEEDS)} seeds x {len(held_out)} cases; no network or service spend.")


if __name__ == "__main__":
    main()
