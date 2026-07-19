#!/usr/bin/env python3
"""Evaluate the closed P4/M7 v2 repair with direction-invariant privacy scoring."""

from __future__ import annotations

from collections import defaultdict
from statistics import mean

import torch
from sklearn.metrics import roc_auc_score

from evaluate_p4_m7_update_unlearning import accuracy, confidence, mean_kl, per_example_loss
from p4_m7_update_unlearning_v2_common import ARMS, BASE, CLAIM_AXES, CORPUS, FEATURES, PREFLIGHT, PREREG, RAW_RUN, RESULT, ROOT, SEEDS, ProbeHead, file_sha, load_json, parameter_l2, state_sha, write_json


def main() -> None:
    if RESULT.exists(): raise SystemExit("v2 evaluation exists; further retry forbidden")
    prereg = load_json(PREREG); preflight = load_json(PREFLIGHT); raw = load_json(RAW_RUN); corpus = load_json(CORPUS)
    packet = torch.load(FEATURES, map_location="cpu", weights_only=False); features = packet["features"].float(); rows = corpus["rows"]
    if packet["record_ids"] != [row["record_id"] for row in rows]: raise SystemExit("v2 feature order mismatch")
    true = torch.tensor([row["true_label"] for row in rows]); training = torch.tensor([row["training_label"] for row in rows])
    groups = {role: [i for i, row in enumerate(rows) if row["role"] == role] for role in corpus["role_counts"]}; deletion = groups["delete_a"] + groups["delete_b"]; evaluation = groups["retained_test"] + groups["target_test"] + groups["adversarial_test"]
    seed_results = []; aggregates = defaultdict(lambda: defaultdict(list)); disagreements = 0
    for seed_row in raw["seed_records"]:
        lookup = {row["arm"]: row for row in seed_row["arms"]}; states = {}; logits = {}
        for arm in ARMS:
            state = torch.load(ROOT / lookup[arm]["best_checkpoint"]["path"], map_location="cpu", weights_only=True); states[arm] = state
            model = ProbeHead(); model.load_state_dict(state); model.eval()
            with torch.inference_mode(): logits[arm] = model(features)
            if state_sha(state) != lookup[arm]["best_checkpoint"]["state_sha256"]: disagreements += 1
        exact = states["deletion_aware_retrain"]; exact_logits = logits["deletion_aware_retrain"]; standard_distance = parameter_l2(states["standard_update"], exact); arms = []
        for arm in ARMS:
            l = logits[arm]; member_loss = per_example_loss(l, true, deletion); nonmember_loss = per_example_loss(l, true, groups["privacy_nonmember"])
            auc = float(roc_auc_score([1] * 60 + [0] * 60, [-x for x in member_loss] + [-x for x in nonmember_loss])); advantage = 2 * abs(auc - 0.5); distance = parameter_l2(states[arm], exact)
            metrics = {
                "retained_test_accuracy": round(accuracy(l, true, groups["retained_test"]), 8),
                "target_test_accuracy": round(accuracy(l, true, groups["target_test"]), 8),
                "adversarial_test_accuracy": round(accuracy(l, true, groups["adversarial_test"]), 8),
                "deletion_true_accuracy": round(accuracy(l, true, deletion), 8),
                "deletion_poisoned_label_accuracy": round(accuracy(l, training, deletion), 8),
                "deletion_true_confidence": round(confidence(l, true, deletion), 8),
                "membership_attack_auc": round(auc, 8),
                "membership_attack_advantage": round(advantage, 8),
                "parameter_l2_to_deletion_retrain": round(distance, 10),
                "prediction_disagreement_to_deletion_retrain": sum(a != b for a, b in zip(l[evaluation].argmax(1).tolist(), exact_logits[evaluation].argmax(1).tolist())),
                "mean_kl_to_deletion_retrain": round(mean_kl(l, exact_logits, evaluation), 10),
                "changed_deletion_decisions_vs_no_update": sum(a != b for a, b in zip(l[deletion].argmax(1).tolist(), logits["no_update"][deletion].argmax(1).tolist())),
            }
            if arm == "approximate_unlearning": metrics["distance_reduction_fraction_vs_standard_update"] = round(1 - distance / standard_distance, 8) if standard_distance else 0.0
            for key, value in metrics.items(): aggregates[arm][key].append(float(value))
            arms.append({"arm": arm, "checkpoint_authority": lookup[arm]["checkpoint_authority"], "sequential_deletion": lookup[arm]["sequential_deletion"], "wall_seconds": lookup[arm]["wall_seconds"], "metrics": metrics, "full_state": lookup[arm]["full_state"], "epochs_completed": len(lookup[arm]["history"])})
        seed_results.append({"seed": seed_row["seed"], "arms": arms})
    summaries = {arm: {key: round(mean(values), 8) for key, values in metrics.items()} for arm, metrics in aggregates.items()}
    exact_deletion = summaries["deletion_aware_retrain"]["deletion_true_accuracy"]; approx_distance = summaries["approximate_unlearning"]["distance_reduction_fraction_vs_standard_update"]; privacy_advantage_delta = summaries["approximate_unlearning"]["membership_attack_advantage"] - summaries["standard_update"]["membership_attack_advantage"]
    storage = load_json(ROOT / raw["storage_receipt"]["path"]); lineage = load_json(ROOT / raw["lineage_receipt"]["path"])
    adequate = exact_deletion >= prereg["primary_gates"]["minimum_confirmatory_deletion_retrain_true_accuracy"]
    axes = {
        "behavioral_cohort_change": {"disposition": "observed_bounded_local", "basis": f"Approximate and retraining arms produced separately recorded deletion-cohort behavior; exact retraining true accuracy was {exact_deletion:.8f}."},
        "causal_influence_reduction": {"disposition": "bounded_comparator_distance_reduced" if approx_distance > 0 else "not_observed", "basis": f"Approximate-unlearning distance reduction toward deletion-aware retraining versus standard update was {approx_distance:.8f}; the comparator does not prove zero influence."},
        "membership_privacy_change": {"disposition": "bounded_attack_advantage_reduced" if privacy_advantage_delta < 0 else "not_observed", "basis": f"Direction-invariant loss-attack advantage changed by {privacy_advantage_delta:+.8f}; one internal attack is not a privacy guarantee."},
        "lineage_invalidation": {"disposition": "observed_bounded_local", "basis": "Five late local descendants were invalidated and quarantined after sequential A/B deletion requests."},
        "legal_compliance": {"disposition": "not_evaluated", "basis": "No legal or jurisdictional assessment ran."},
        "storage_erasure": {"disposition": "partial_declared_store_only", "basis": "Declared operational shards were absent, while research evidence remained intentionally retained."},
        "backup_erasure": {"disposition": "local_observed_remote_unresolved", "basis": "Local backup absence was observed; the unavailable remote endpoint did not acknowledge erasure."},
        "external_descendant_closure": {"disposition": "unresolved", "basis": "Local invalidation is not external descendant erasure."},
    }
    rollback = all(row["full_state"]["rollback_exact"] and row["full_state"]["rollback_sha256"] == row["full_state"]["before_sha256"] for seed in seed_results for row in seed["arms"])
    gates = {"preflight_instrument_adequate": preflight["protocol_outcome"] == "instrument_adequate", "confirmatory_retrain_target_adequate": adequate, "all_feature_values_finite": bool(torch.isfinite(features).all()), "five_seeds_present": [x["seed"] for x in seed_results] == list(SEEDS), "seven_arms_present": all([x["arm"] for x in seed["arms"]] == list(ARMS) for seed in seed_results), "twenty_four_state_surfaces_present": all(x["full_state"]["surface_count"] == 24 for seed in seed_results for x in seed["arms"]), "all_eight_claim_axes_reported": set(axes) == set(CLAIM_AXES), "all_rollback_surface_digests_exact": rollback, "total_storage_erasure_remains_false": storage["total_storage_erasure"] is False, "evaluator_recomputation_disagreement_zero": disagreements == 0}
    result = {"schema_version": "asi_stack.p4_m7_confirmatory_result.v2", "run_id": prereg["run_id"], "protocol_outcome": "instrument_adequate_bounded_local_axis_separation" if adequate else "instrument_inadequate_v2_terminal", "claim_outcome": "claim_narrowed_after_full_attempt" if adequate else "not_applicable_instrument_failure", "corpus_sha256": file_sha(CORPUS), "preregistration_sha256": file_sha(PREREG), "raw_run_sha256": file_sha(RAW_RUN), "feature_artifact_sha256": file_sha(FEATURES), "candidate_and_checkpoint_bytes_closed_before_axis_evaluation": True, "seeds": list(SEEDS), "arms": list(ARMS), "claim_axes": list(CLAIM_AXES), "seed_results": seed_results, "arm_summaries": summaries, "axis_dispositions": axes, "storage_receipt": storage, "lineage_receipt": lineage, "evaluator_recomputation_disagreement_count": disagreements, "gate_checks_before_validator_mutations": gates, "cost": raw["cost"], "evaluator_separation": "separate metric implementation over closed trainer bytes; internal only", "claim_ceiling": "Frozen Qwen representation plus linear-head local evidence only; not language-model unlearning, zero influence, privacy, complete erasure, legal compliance, transfer, production, or SOTA.", "support_state_effect": "none", "chapter_core_promotion_count": 0, "non_claims": prereg["non_claims"]}
    write_json(RESULT, result); print(f"P4/M7 v2 evaluated: retrain_deletion={exact_deletion:.4f}, approx_distance={approx_distance:+.4f}, privacy_advantage_delta={privacy_advantage_delta:+.4f}, adequate={adequate}")


if __name__ == "__main__": main()
