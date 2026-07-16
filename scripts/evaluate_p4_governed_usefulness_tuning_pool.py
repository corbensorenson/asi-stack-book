#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "experiments" / "p4_governed_usefulness"
PREREG = BASE / "difficulty_sweep_v2_v5_pool_preregistration.json"
OUTPUT = BASE / "results" / "difficulty_sweep_v2_v5_pool_result.json"

def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main() -> None:
    if OUTPUT.exists():
        raise SystemExit("Pooled tuning evaluation is one-shot; output already exists.")
    prereg = load(PREREG)
    results: list[dict[str, Any]] = []
    bindings: list[dict[str, str]] = []
    for index, frozen in enumerate(prereg["eligible_results"]):
        path = ROOT / frozen["path"]
        actual = sha(path)
        if index < 3 and actual != frozen["sha256"]:
            raise SystemExit(f"Frozen prior result drifted: {frozen['path']}")
        result = load(path)
        if result.get("candidate_artifact_closed_before_labels_loaded") is not True:
            raise SystemExit(f"Candidate/label ordering not established: {frozen['path']}")
        results.append(result)
        bindings.append({"path": frozen["path"], "sha256": actual, "candidate_sha256": result["candidate_sha256"]})

    expected = sum(row["expected_task_count"] for row in results)
    admitted = sum(row["schema_admissible_candidate_count"] for row in results)
    disagreements = sum(row["evaluator_disagreement_count"] for row in results)
    records = [record for row in results for record in row["records"]]
    cells = Counter(record["cell"] for record in records)
    effect_count = sum(record["effect_probe"]["tag"] != "none" for record in records)
    gate = prereg["gate"]
    checks = {
        "schema_admissible_rate": admitted / expected >= gate["minimum_pooled_schema_admissible_rate"],
        "four_cell_floor": all(cells[cell] >= gate["minimum_candidates_per_cell"] for cell in gate["required_cells"]),
        "evaluator_disagreement_rate": disagreements / max(1, admitted) <= gate["maximum_pooled_evaluator_disagreement_rate"],
        "effect_probe_floor": effect_count >= gate["minimum_pooled_effect_probe_count"],
        "candidate_before_label_order": True,
    }
    adequate = all(checks.values())
    output = {
        "schema_version": "asi_stack.p4_governed_usefulness_tuning_pool_result.v1",
        "pool_id": prereg["pool_id"],
        "preregistration_sha256": sha(PREREG),
        "result_bindings": bindings,
        "expected_task_count": expected,
        "schema_admissible_candidate_count": admitted,
        "schema_admissible_rate": admitted / expected,
        "four_cell_counts": dict(cells),
        "evaluator_disagreement_count": disagreements,
        "evaluator_disagreement_rate": disagreements / max(1, admitted),
        "effect_probe_count": effect_count,
        "gate_checks": checks,
        "protocol_outcome": prereg["success_disposition"] if adequate else prereg["failure_disposition"],
        "confirmatory_design_freeze_authorized": adequate,
        "confirmatory_denominator_opened": False,
        "claim_attempt_counted": False,
        "support_state_effect": "none",
        "publication_authority": "none",
        "release_authority": "none",
        "claim_ceiling": "tuning_operating_range_adequacy_only_not_policy_effectiveness_safety_transfer_or_book_claim_support"
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(f"P4 pooled tuning: {output['protocol_outcome']}; admitted={admitted}/{expected}, cells={dict(cells)}, effects={effect_count}.")

if __name__ == "__main__":
    main()
