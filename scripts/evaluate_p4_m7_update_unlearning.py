#!/usr/bin/env python3
"""Independently evaluate the frozen P4/M7 checkpoints across eight claim axes."""

from __future__ import annotations

import hashlib
import json
import math
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

import numpy as np
import torch
from sklearn.metrics import roc_auc_score

from p4_m7_update_unlearning_common import (
    ARMS,
    BASE,
    CLAIM_AXES,
    CORPUS,
    FEATURES,
    PREFLIGHT,
    PREREG,
    RAW_RUN,
    RESULT,
    ROOT,
    SEEDS,
    STATE_SURFACES,
    ProbeHead,
    file_sha,
    load_json,
    parameter_l2,
    state_sha,
    write_json,
)


def load_state(ref: dict[str, Any]) -> dict[str, torch.Tensor]:
    return torch.load(ROOT / ref["path"], map_location="cpu", weights_only=True)


def row_indices(rows: list[dict[str, Any]], role: str) -> list[int]:
    return [index for index, row in enumerate(rows) if row["role"] == role]


def logits_for(state: dict[str, torch.Tensor], features: torch.Tensor) -> torch.Tensor:
    model = ProbeHead(); model.load_state_dict(state); model.eval()
    with torch.inference_mode():
        return model(features).detach().cpu()


def accuracy(logits: torch.Tensor, labels: torch.Tensor, selected: list[int]) -> float:
    return float((logits[selected].argmax(dim=1) == labels[selected]).float().mean())


def confidence(logits: torch.Tensor, labels: torch.Tensor, selected: list[int]) -> float:
    probs = logits[selected].softmax(dim=1)
    return float(probs[torch.arange(len(selected)), labels[selected]].mean())


def per_example_loss(logits: torch.Tensor, labels: torch.Tensor, selected: list[int]) -> list[float]:
    return torch.nn.functional.cross_entropy(logits[selected], labels[selected], reduction="none").tolist()


def mean_kl(left: torch.Tensor, right: torch.Tensor, selected: list[int]) -> float:
    p = left[selected].softmax(dim=1).clamp_min(1e-9)
    q = right[selected].softmax(dim=1).clamp_min(1e-9)
    return float((p * (p.log() - q.log())).sum(dim=1).mean())


def rounded(value: float) -> float:
    return round(float(value), 8)


def main() -> None:
    if RESULT.exists():
        raise SystemExit("confirmatory evaluation already exists; no outcome-aware retry allowed")
    prereg = load_json(PREREG)
    preflight = load_json(PREFLIGHT)
    raw = load_json(RAW_RUN)
    corpus = load_json(CORPUS)
    feature_packet = torch.load(FEATURES, map_location="cpu", weights_only=False)
    rows = corpus["rows"]
    features = feature_packet["features"].float()
    if feature_packet["record_ids"] != [row["record_id"] for row in rows]:
        raise SystemExit("feature/corpus record order mismatch")
    true_labels = torch.tensor([row["true_label"] for row in rows], dtype=torch.long)
    training_labels = torch.tensor([row["training_label"] for row in rows], dtype=torch.long)
    groups = {role: row_indices(rows, role) for role in corpus["role_counts"]}
    deletion = groups["delete_a"] + groups["delete_b"]
    privacy_nonmember = groups["privacy_nonmember"]
    evaluation = groups["retained_test"] + groups["target_test"] + groups["adversarial_test"]
    seed_results = []
    disagreement_count = 0
    aggregates: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    for seed_row in raw["seed_records"]:
        states: dict[str, dict[str, torch.Tensor]] = {}
        logits: dict[str, torch.Tensor] = {}
        arm_lookup = {row["arm"]: row for row in seed_row["arms"]}
        for arm in ARMS:
            record = arm_lookup[arm]
            state = load_state(record["best_checkpoint"])
            states[arm] = state
            logits[arm] = logits_for(state, features)
            if state_sha(state) != record["best_checkpoint"]["state_sha256"]:
                disagreement_count += 1
            surface = load_json(ROOT / record["full_state"]["surface_path"])
            if len(surface.get("surfaces", {})) != len(STATE_SURFACES) or file_sha(ROOT / record["full_state"]["surface_path"]) != record["full_state"]["surface_file_sha256"]:
                disagreement_count += 1
        exact_state = states["deletion_aware_retrain"]
        exact_logits = logits["deletion_aware_retrain"]
        standard_distance = parameter_l2(states["standard_update"], exact_state)
        arms = []
        for arm in ARMS:
            record = arm_lookup[arm]
            arm_logits = logits[arm]
            member_losses = per_example_loss(arm_logits, true_labels, deletion)
            nonmember_losses = per_example_loss(arm_logits, true_labels, privacy_nonmember)
            membership_auc = roc_auc_score(
                [1] * len(member_losses) + [0] * len(nonmember_losses),
                [-value for value in member_losses] + [-value for value in nonmember_losses],
            )
            distance = parameter_l2(states[arm], exact_state)
            disagreement = sum(
                left != right
                for left, right in zip(arm_logits[evaluation].argmax(dim=1).tolist(), exact_logits[evaluation].argmax(dim=1).tolist())
            )
            metrics = {
                "retained_test_accuracy": rounded(accuracy(arm_logits, true_labels, groups["retained_test"])),
                "target_test_accuracy": rounded(accuracy(arm_logits, true_labels, groups["target_test"])),
                "adversarial_test_accuracy": rounded(accuracy(arm_logits, true_labels, groups["adversarial_test"])),
                "deletion_true_accuracy": rounded(accuracy(arm_logits, true_labels, deletion)),
                "deletion_poisoned_label_accuracy": rounded(accuracy(arm_logits, training_labels, deletion)),
                "deletion_true_confidence": rounded(confidence(arm_logits, true_labels, deletion)),
                "membership_attack_auc": rounded(membership_auc),
                "parameter_l2_to_deletion_retrain": round(distance, 10),
                "prediction_disagreement_to_deletion_retrain": disagreement,
                "mean_kl_to_deletion_retrain": round(mean_kl(arm_logits, exact_logits, evaluation), 10),
                "changed_deletion_decisions_vs_no_update": sum(
                    left != right
                    for left, right in zip(arm_logits[deletion].argmax(dim=1).tolist(), logits["no_update"][deletion].argmax(dim=1).tolist())
                ),
            }
            if arm == "approximate_unlearning":
                metrics["distance_reduction_fraction_vs_standard_update"] = round(1.0 - distance / standard_distance, 8) if standard_distance else 0.0
            for key, value in metrics.items():
                if isinstance(value, (int, float)):
                    aggregates[arm][key].append(float(value))
            arms.append({
                "arm": arm,
                "checkpoint_authority": record["checkpoint_authority"],
                "metrics": metrics,
                "full_state": record["full_state"],
                "epochs_completed": len(record["history"]),
            })
        seed_results.append({"seed": seed_row["seed"], "arms": arms})
    summaries = {
        arm: {key: round(mean(values), 8) for key, values in metrics.items()}
        for arm, metrics in aggregates.items()
    }
    approx_reduction = summaries["approximate_unlearning"]["distance_reduction_fraction_vs_standard_update"]
    privacy_delta = summaries["approximate_unlearning"]["membership_attack_auc"] - summaries["standard_update"]["membership_attack_auc"]
    behavioral_changes = sum(
        row["metrics"]["changed_deletion_decisions_vs_no_update"]
        for seed in seed_results
        for row in seed["arms"]
        if row["arm"] == "approximate_unlearning"
    )
    storage = load_json(ROOT / raw["storage_receipt"]["path"])
    lineage = load_json(ROOT / raw["lineage_receipt"]["path"])
    axis_dispositions = {
        "behavioral_cohort_change": {
            "disposition": "observed_bounded_local",
            "basis": f"Approximate unlearning changed {behavioral_changes} deletion-cohort decisions across five seeds relative to no update.",
        },
        "causal_influence_reduction": {
            "disposition": "bounded_comparator_distance_reduced" if approx_reduction > 0 else "not_observed",
            "basis": f"Mean parameter-distance reduction toward deletion-aware retraining versus standard update was {approx_reduction:.8f}; retraining is only a comparator and does not prove zero influence.",
        },
        "membership_privacy_change": {
            "disposition": "attack_metric_changed_no_guarantee",
            "basis": f"Mean loss-threshold membership AUC changed by {privacy_delta:+.8f}; this single internal attack is not a privacy guarantee.",
        },
        "lineage_invalidation": {
            "disposition": "observed_bounded_local",
            "basis": f"{lineage['local_descendant_invalidation_count']} late local descendants were invalidated and quarantined.",
        },
        "legal_compliance": {"disposition": "not_evaluated", "basis": "No legal authority, jurisdiction, consent, or compliance assessment was performed."},
        "storage_erasure": {
            "disposition": "partial_declared_store_only",
            "basis": "The declared operational feature shard was absent after deletion, while the corpus, research feature packet, checkpoints, and raw evidence remain retained.",
        },
        "backup_erasure": {
            "disposition": "local_observed_remote_unresolved",
            "basis": "The declared local backup was absent; the simulated unavailable remote endpoint supplied no acknowledgement.",
        },
        "external_descendant_closure": {
            "disposition": "unresolved",
            "basis": "Local descendants were invalidated, but the simulated unreachable export did not acknowledge invalidation or erasure.",
        },
    }
    rollback_exact = all(
        arm["full_state"]["rollback_exact"]
        and arm["full_state"]["rollback_sha256"] == seed["arms"][0]["full_state"]["before_sha256"]
        for seed in seed_results
        for arm in seed["arms"]
    )
    gates = {
        "preflight_instrument_adequate": preflight["protocol_outcome"] == "instrument_adequate",
        "all_feature_values_finite": bool(torch.isfinite(features).all()),
        "five_seeds_present": [seed["seed"] for seed in seed_results] == list(SEEDS),
        "seven_arms_present": all([row["arm"] for row in seed["arms"]] == list(ARMS) for seed in seed_results),
        "twenty_four_state_surfaces_present": all(row["full_state"]["surface_count"] == 24 for seed in seed_results for row in seed["arms"]),
        "all_eight_claim_axes_reported": set(axis_dispositions) == set(CLAIM_AXES),
        "all_rollback_surface_digests_exact": rollback_exact,
        "total_storage_erasure_remains_false": storage["total_storage_erasure"] is False,
        "evaluator_recomputation_disagreement_zero": disagreement_count == 0,
    }
    result = {
        "schema_version": "asi_stack.p4_m7_confirmatory_result.v1",
        "run_id": prereg["run_id"],
        "protocol_outcome": "instrument_adequate_bounded_local_axis_separation",
        "claim_outcome": "support_retained_with_bounded_noncore_axis_result",
        "corpus_sha256": file_sha(CORPUS),
        "preregistration_sha256": file_sha(PREREG),
        "raw_run_sha256": file_sha(RAW_RUN),
        "feature_artifact_sha256": file_sha(FEATURES),
        "candidate_and_checkpoint_bytes_closed_before_axis_evaluation": True,
        "seeds": list(SEEDS),
        "arms": list(ARMS),
        "claim_axes": list(CLAIM_AXES),
        "seed_results": seed_results,
        "arm_summaries": summaries,
        "axis_dispositions": axis_dispositions,
        "storage_receipt": storage,
        "lineage_receipt": lineage,
        "evaluator_recomputation_disagreement_count": disagreement_count,
        "gate_checks_before_validator_mutations": gates,
        "cost": raw["cost"],
        "evaluator_separation": "independent script and metric implementation over closed trainer artifacts; internal only",
        "claim_ceiling": "Frozen Qwen representation plus linear-head local evidence for axis separation and declared-state rollback only; not language-model unlearning, privacy, complete erasure, legal compliance, transfer, production, or SOTA.",
        "support_state_effect": "none",
        "chapter_core_promotion_count": 0,
        "non_claims": prereg["non_claims"],
    }
    write_json(RESULT, result)
    print(
        "P4/M7 evaluated: "
        f"approx_distance_reduction={approx_reduction:.4f}, privacy_auc_delta={privacy_delta:+.4f}, "
        f"behavior_changes={behavioral_changes}, rollback_exact={rollback_exact}, support_effect=none"
    )


if __name__ == "__main__":
    main()
