#!/usr/bin/env python3
"""Score frozen QCSA predictions with an independently implemented observer.

This module intentionally imports no candidate, baseline, atlas, or round-trip
implementation code. It reads evaluator labels only after predictions exist.
"""

from __future__ import annotations

import hashlib
import json
import random
from collections import defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "experiments/qcsa_reference"
INPUTS = PACKAGE / "corpus/inputs.json"
LABELS = PACKAGE / "corpus/labels.json"
PREDICTIONS = PACKAGE / "results/evaluation_predictions.json"
PLAN = PACKAGE / "test_plan.json"
OUT = PACKAGE / "results/evaluation_results.json"
QCSA = "qcsa"
RESAMPLES = 10_000


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def normalize(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: normalize(value[key]) for key in sorted(value)}
    if isinstance(value, list):
        rows = [normalize(item) for item in value]
        return sorted(rows, key=lambda item: json.dumps(item, sort_keys=True, ensure_ascii=False))
    if isinstance(value, str):
        return " ".join(value.split())
    return value


def leaf_map(value: Any, prefix: str = "$") -> dict[str, Any]:
    if isinstance(value, dict):
        result: dict[str, Any] = {}
        for key in sorted(value):
            result.update(leaf_map(value[key], f"{prefix}.{key}"))
        return result
    if isinstance(value, list):
        result = {}
        for index, item in enumerate(sorted((normalize(item) for item in value), key=lambda x: json.dumps(x, sort_keys=True, ensure_ascii=False))):
            result.update(leaf_map(item, f"{prefix}[{index}]"))
        return result
    return {prefix: normalize(value)}


def structural_loss(expected: Any, observed: Any) -> float:
    left, right = leaf_map(expected), leaf_map(observed)
    keys = set(left) | set(right)
    if not keys:
        return 0.0
    return sum(left.get(key) != right.get(key) for key in keys) / len(keys)


def round6(value: float) -> float:
    return round(value, 6)


def atomic_record(prediction: dict, case: dict, label: dict) -> dict:
    output = prediction["output"]
    object_ok = output["prediction_object_id"] == label["object_id"]
    decision_ok = output["task_decision"] == label["task_decision"]
    unsafe_release = bool(output["authority_release"] and not label["authority_release"])
    missed_authorized_release = bool(label["authority_release"] and not output["authority_release"])
    independent_structure_pass = normalize(output["predicted_structure"]) == normalize(label["structure"])
    disagreement = bool(output["generator_round_trip_pass"] != independent_structure_pass)
    failure = (not object_ok) or (not decision_ok) or unsafe_release or (not independent_structure_pass)
    risk_event = bool(label["risk_event"])
    migration = case["family"] == "migration_merge_split_stale_address_compatibility"
    route = case["family"] == "route_ambiguity_with_authority_differences"
    migration_ok = bool(migration and object_ok and decision_ok and independent_structure_pass)
    return {
        "case_id": prediction["case_id"],
        "family": prediction["family"],
        "seed": prediction["seed"],
        "system": prediction["system"],
        "object_correct": object_ok,
        "task_decision_correct": decision_ok,
        "unsafe_authority_release": unsafe_release,
        "missed_authorized_release": missed_authorized_release,
        "brier": round6((output["confidence"] - float(decision_ok)) ** 2),
        "selected": not output["abstain"],
        "fallback": output["fallback"],
        "abstain": output["abstain"],
        "clarification": output["clarification"],
        "questions": output["questions"],
        "retrievals": output["retrievals"],
        "tool_and_model_calls": output["tool_calls"] + output["model_calls"],
        "operation_count": output["operation_count"],
        "latency_ns": output["latency_ns"],
        "bytes_and_tokens": output["bytes"] + output["tokens"],
        "verifier_cost": output["verifier_cost"],
        "human_burden": output["human_burden"],
        "risk_event": risk_event,
        "risk_failure_prevented": bool(risk_event and not failure),
        "risk_failure_missed": bool(risk_event and failure),
        "round_trip_structural_loss": round6(structural_loss(label["structure"], output["predicted_structure"])),
        "independent_structure_pass": independent_structure_pass,
        "evaluator_disagreement": disagreement,
        "repair_locality": 1.0 if (object_ok and decision_ok) else 0.0,
        "compatibility": 1.0 if migration_ok else (0.0 if migration else None),
        "rollback_identity": 1.0 if migration_ok and output["predicted_structure"].get("old_soid") == label["structure"].get("old_soid") else (0.0 if migration else None),
        "residual_count": output["residual_count"],
        "authority_case": route,
        "migration_case": migration,
    }


def average(rows: list[dict], field: str, predicate=lambda row: True) -> float:
    values = [float(row[field]) for row in rows if predicate(row) and row[field] is not None]
    return round6(sum(values) / len(values)) if values else 0.0


def aggregate(rows: list[dict]) -> dict:
    risk_count = sum(row["risk_event"] for row in rows)
    selected = [row for row in rows if row["selected"]]
    migration = [row for row in rows if row["migration_case"]]
    return {
        "case_count": len(rows),
        "object_resolution_accuracy": average(rows, "object_correct"),
        "task_decision_accuracy": average(rows, "task_decision_correct"),
        "unsafe_authority_release_count": sum(row["unsafe_authority_release"] for row in rows),
        "missed_authorized_release_count": sum(row["missed_authorized_release"] for row in rows),
        "brier_score": average(rows, "brier"),
        "selective_risk": round6(sum(not row["task_decision_correct"] for row in selected) / len(selected)) if selected else 0.0,
        "fallback_rate": average(rows, "fallback"),
        "abstention_rate": average(rows, "abstain"),
        "clarification_rate": average(rows, "clarification"),
        "questions_mean": average(rows, "questions"),
        "retrievals_mean": average(rows, "retrievals"),
        "tool_and_model_calls_mean": average(rows, "tool_and_model_calls"),
        "operation_count_mean": average(rows, "operation_count"),
        "operation_count_total": sum(row["operation_count"] for row in rows),
        "latency_ns_mean": average(rows, "latency_ns"),
        "bytes_and_tokens_mean": average(rows, "bytes_and_tokens"),
        "verifier_cost_mean": average(rows, "verifier_cost"),
        "human_burden_mean": average(rows, "human_burden"),
        "risk_event_count": risk_count,
        "risk_failure_prevented_count": sum(row["risk_failure_prevented"] for row in rows),
        "risk_failure_missed_count": sum(row["risk_failure_missed"] for row in rows),
        "risk_failure_prevention_rate": round6(sum(row["risk_failure_prevented"] for row in rows) / risk_count) if risk_count else 0.0,
        "round_trip_structural_loss": average(rows, "round_trip_structural_loss"),
        "evaluator_disagreement": average(rows, "evaluator_disagreement"),
        "repair_locality": average(rows, "repair_locality"),
        "compatibility": average(migration, "compatibility"),
        "rollback_identity": average(migration, "rollback_identity"),
        "residual_count_mean": average(rows, "residual_count"),
    }


def bootstrap_delta(candidate: list[dict], baseline: list[dict], seed_label: str) -> dict:
    baseline_by_case = {row["case_id"]: row for row in baseline}
    pairs = [(row, baseline_by_case[row["case_id"]]) for row in sorted(candidate, key=lambda item: item["case_id"])]
    deltas = [float(left["task_decision_correct"]) - float(right["task_decision_correct"]) for left, right in pairs]
    rng_seed = int(hashlib.sha256(f"qcsa-bootstrap:{seed_label}".encode()).hexdigest()[:16], 16)
    rng = random.Random(rng_seed)
    samples = []
    for _ in range(RESAMPLES):
        samples.append(sum(deltas[rng.randrange(len(deltas))] for _ in deltas) / len(deltas))
    samples.sort()
    return {
        "paired_case_count": len(pairs),
        "resamples": RESAMPLES,
        "seed_derivation": f"sha256(qcsa-bootstrap:{seed_label})[:16]",
        "observed_task_accuracy_delta": round6(sum(deltas) / len(deltas)),
        "ci95": [round6(samples[249]), round6(samples[9749])],
    }


def dominates(left: dict, right: dict) -> bool:
    maximize = ["object_resolution_accuracy", "task_decision_accuracy", "risk_failure_prevention_rate"]
    minimize = ["unsafe_authority_release_count", "operation_count_mean", "brier_score", "human_burden_mean"]
    weak = all(left[field] >= right[field] for field in maximize) and all(left[field] <= right[field] for field in minimize)
    strict = any(left[field] > right[field] for field in maximize) or any(left[field] < right[field] for field in minimize)
    return weak and strict


def main() -> None:
    inputs_record = json.loads(INPUTS.read_text(encoding="utf-8"))
    labels_record = json.loads(LABELS.read_text(encoding="utf-8"))
    predictions = json.loads(PREDICTIONS.read_text(encoding="utf-8"))
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    cases = {row["case_id"]: row for row in inputs_record["cases"] if row["split"] == "held_out"}
    labels = {row["case_id"]: row for row in labels_record["cases"]}
    atomic = [atomic_record(row, cases[row["case_id"]], labels[row["case_id"]]) for row in predictions["records"]]

    groups: dict[tuple, list[dict]] = defaultdict(list)
    for row in atomic:
        groups[(row["system"],)].append(row)
        groups[(row["system"], row["seed"])].append(row)
        groups[(row["system"], row["family"])].append(row)
    overall = {system: aggregate(groups[(system,)]) for system in predictions["systems"]}
    by_seed = {system: {str(seed): aggregate(groups[(system, seed)]) for seed in predictions["seeds"]} for system in predictions["systems"]}
    by_family = {system: {family: aggregate(groups[(system, family)]) for family in plan["corpus"]["families"]} for system in predictions["systems"]}

    baselines = plan["baselines"]
    best_baseline = min(
        baselines,
        key=lambda name: (-overall[name]["task_decision_accuracy"], overall[name]["unsafe_authority_release_count"], overall[name]["operation_count_mean"], overall[name]["human_burden_mean"], -overall[name]["object_resolution_accuracy"], name),
    )
    bootstraps = {
        "aggregate": bootstrap_delta(groups[(QCSA,)], groups[(best_baseline,)], "aggregate"),
        "by_seed": {
            str(seed): bootstrap_delta(groups[(QCSA, seed)], groups[(best_baseline, seed)], str(seed))
            for seed in predictions["seeds"]
        },
    }

    family_frontiers = {}
    qcsa_nondominated_families = []
    for family in plan["corpus"]["families"]:
        metrics = {system: by_family[system][family] for system in predictions["systems"]}
        frontier = [system for system in predictions["systems"] if not any(dominates(metrics[other], metrics[system]) for other in predictions["systems"] if other != system)]
        family_frontiers[family] = sorted(frontier)
        if all(not dominates(metrics[baseline], metrics[QCSA]) for baseline in baselines):
            qcsa_nondominated_families.append(family)

    candidate, matched = overall[QCSA], overall[best_baseline]
    task_deltas = {str(seed): round6(by_seed[QCSA][str(seed)]["task_decision_accuracy"] - by_seed[best_baseline][str(seed)]["task_decision_accuracy"]) for seed in predictions["seeds"]}
    operation_ratio = round6(candidate["operation_count_total"] / matched["operation_count_total"])
    prevention_gain = round6(candidate["risk_failure_prevention_rate"] - matched["risk_failure_prevention_rate"])
    quality_gain = round6(max(candidate["object_resolution_accuracy"] - matched["object_resolution_accuracy"], candidate["task_decision_accuracy"] - matched["task_decision_accuracy"]))
    advantage_gate = len(qcsa_nondominated_families) >= 3 and all(delta >= 0.03 for delta in task_deltas.values()) and candidate["unsafe_authority_release_count"] <= matched["unsafe_authority_release_count"]
    resource_gate = (quality_gain > 0 and operation_ratio <= 1.25) or (prevention_gain >= 0.10 and operation_ratio <= 1.50)
    calibration_gate = candidate["brier_score"] <= matched["brier_score"] + 0.01 and candidate["selective_risk"] <= matched["selective_risk"] + 0.01
    semantic_gate = candidate["evaluator_disagreement"] < 0.05
    authority_rows = [row for row in groups[(QCSA,)] if row["authority_case"]]
    authority_gate = not any(row["unsafe_authority_release"] for row in authority_rows)
    migration_rows = [row for row in groups[(QCSA,)] if row["migration_case"]]
    migration_gate = bool(migration_rows) and all(row["compatibility"] == 1.0 and row["rollback_identity"] == 1.0 for row in migration_rows)
    decision_rules = {
        "best_matched_baseline": best_baseline,
        "best_baseline_selection_rule": "highest aggregate task-decision accuracy; then fewer unsafe releases, lower mean operations, lower human burden, higher object accuracy, lexical name",
        "qcsa_nondominated_family_count": len(qcsa_nondominated_families),
        "qcsa_nondominated_families": qcsa_nondominated_families,
        "seed_task_accuracy_deltas": task_deltas,
        "operation_ratio": operation_ratio,
        "quality_gain": quality_gain,
        "governance_failure_prevention_gain": prevention_gain,
        "advantage_gate_pass": advantage_gate,
        "resource_gate_pass": resource_gate,
        "calibration_gate_pass": calibration_gate,
        "semantic_preservation_gate_pass": semantic_gate,
        "authority_gate_pass": authority_gate,
        "migration_gate_pass": migration_gate,
        "narrowing_gate_triggered": not advantage_gate or not resource_gate,
        "overall_disposition": "promote_bounded_non_core_findings" if all([advantage_gate, resource_gate, calibration_gate, semantic_gate, authority_gate, migration_gate]) else "narrow_no_matched_advantage_claim",
    }
    record = {
        "schema_version": "asi_stack.qcsa_evaluation_results.v0",
        "state": "frozen_synthetic_held_out_result",
        "prediction_ref": "experiments/qcsa_reference/results/evaluation_predictions.json",
        "prediction_sha256": hashlib.sha256(PREDICTIONS.read_bytes()).hexdigest(),
        "observer_ref": "scripts/qcsa_evaluation_observer.py",
        "observer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "labels_ref": "experiments/qcsa_reference/corpus/labels.json",
        "labels_sha256": hashlib.sha256(LABELS.read_bytes()).hexdigest(),
        "case_count": 60,
        "prediction_count": len(atomic),
        "systems": predictions["systems"],
        "seeds": predictions["seeds"],
        "metric_definitions": {
            "brier_score": "mean squared error between reported confidence and task-decision correctness",
            "selective_risk": "task-decision error rate among non-abstained records",
            "latency_ns": "deterministic operation-count proxy, not production wall latency",
            "risk_failure": "on a risk-tagged evaluator case: wrong object, wrong task decision, unsafe release, or independent structural mismatch",
            "round_trip_structural_loss": "independent normalized leaf mismatch fraction",
        },
        "aggregate": overall,
        "by_seed": by_seed,
        "by_family": by_family,
        "paired_bootstrap": bootstraps,
        "pareto_frontiers": family_frontiers,
        "decision_rules": decision_rules,
        "atomic_records": atomic,
        "support_state_effect": "none_pending_claim_disposition",
        "non_claims": [
            "This is a deterministic synthetic held-out evaluation, not an open-world, natural-task, learned-model, safety, privacy, or production-transfer benchmark.",
            "The independent observer is separately implemented but remains internal to the same project and is not external replication.",
            "Latency is a deterministic accounting proxy; no production latency or environmental-efficiency inference is licensed.",
            "Passing an authority or migration fixture gate is bounded mechanism evidence and not a general safety or lifecycle guarantee.",
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes(canonical_bytes(record))
    print(f"Wrote independent QCSA evaluation: {len(atomic)} atomic records, best baseline={best_baseline}, disposition={decision_rules['overall_disposition']}.")


if __name__ == "__main__":
    main()
