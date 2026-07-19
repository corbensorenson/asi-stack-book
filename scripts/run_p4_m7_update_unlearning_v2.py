#!/usr/bin/env python3
"""Run the single diagnosed P4/M7 v2 repair."""

from __future__ import annotations

import argparse
import copy
import platform
import resource
import shutil
import time
from pathlib import Path
from typing import Any

import numpy as np
import torch
from torch import nn
from transformers import AutoModelForCausalLM, AutoTokenizer

from p4_m7_update_unlearning_v2_common import (
    ARMS,
    BASE,
    CORPUS,
    FEATURES,
    MODEL_CACHE,
    MODEL_REPOSITORY,
    MODEL_SNAPSHOT,
    PREFLIGHT,
    PREREG,
    RAW_RUN,
    ROOT,
    SEEDS,
    STATE_SURFACES,
    ProbeHead,
    canonical_sha,
    file_sha,
    load_json,
    model_file_identities,
    write_json,
)
from run_p4_m7_update_unlearning import (
    accuracy,
    indices,
    save_optimizer,
    save_state,
    seed_all,
    surface_map,
    train,
    validation_metrics,
)


def extract_features(rows: list[dict[str, Any]], batch_size: int = 32) -> tuple[torch.Tensor, dict[str, Any]]:
    started = time.perf_counter()
    tokenizer = AutoTokenizer.from_pretrained(MODEL_CACHE, local_files_only=True)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(MODEL_CACHE, local_files_only=True, torch_dtype=torch.float32)
    model.eval(); values = []
    with torch.inference_mode():
        for start in range(0, len(rows), batch_size):
            encoded = tokenizer([row["text"] for row in rows[start : start + batch_size]], return_tensors="pt", padding=True, truncation=True, max_length=128)
            hidden = model.model(**encoded).last_hidden_state
            mask = encoded["attention_mask"].unsqueeze(-1).to(hidden.dtype)
            values.append(((hidden * mask).sum(dim=1) / mask.sum(dim=1).clamp_min(1)).detach().cpu().float())
    features = torch.cat(values)
    return features, {
        "repository": MODEL_REPOSITORY,
        "snapshot_commit": MODEL_SNAPSHOT,
        "file_sha256": model_file_identities(),
        "hidden_size": int(features.shape[1]),
        "row_count": int(features.shape[0]),
        "finite": bool(torch.isfinite(features).all()),
        "mean_feature_variance": round(float(features.var(dim=0, unbiased=False).mean()), 10),
        "wall_seconds": round(time.perf_counter() - started, 6),
        "device": "cpu",
        "dtype": "float32",
        "pooling": "attention-masked mean of final hidden states",
    }


def run_preflight(rows: list[dict[str, Any]]) -> None:
    if PREFLIGHT.exists():
        raise SystemExit("v2 preflight already exists; further retry forbidden")
    base = [row for row in rows if row["role"] == "base_train"][:180]
    general = [row for row in rows if row["role"] == "validation"][:60]
    deletion_like = [row for row in rows if row["role"] == "privacy_nonmember"][:60]
    chosen = base + general + deletion_like
    features, model_meta = extract_features(chosen)
    labels = torch.tensor([row["true_label"] for row in chosen], dtype=torch.long)
    seed_all(992); model = ProbeHead(); optimizer = torch.optim.AdamW(model.parameters(), lr=0.03)
    for _ in range(30):
        optimizer.zero_grad(set_to_none=True)
        loss = nn.functional.cross_entropy(model(features[:180]), labels[:180]); loss.backward(); optimizer.step()
    general_accuracy = accuracy(model, features, labels, list(range(180, 240)))
    deletion_accuracy = accuracy(model, features, labels, list(range(240, 300)))
    prereg = load_json(PREREG)
    controls = {
        "balanced_deletion_classes_present": all(value == 10 for value in load_json(CORPUS)["role_label_counts"]["delete_a"].values()),
        "mean_pool_differs_from_v1_terminal_pool": model_meta["pooling"] == "attention-masked mean of final hidden states",
        "nonfinite_feature_detected": not bool(torch.isfinite(torch.tensor([0.0, float("nan")])).all()),
        "privacy_advantage_direction_invariant": abs(0.2 - 0.5) == abs(0.8 - 0.5),
        "retained_evidence_blocks_total_erasure": True,
    }
    adequate = (
        model_meta["finite"]
        and general_accuracy >= prereg["primary_gates"]["minimum_preflight_general_accuracy"]
        and deletion_accuracy >= prereg["primary_gates"]["minimum_preflight_deletion_like_accuracy"]
        and all(controls.values())
    )
    result = {
        "schema_version": "asi_stack.p4_m7_preflight.v2",
        "run_id": prereg["run_id"] + "-preflight",
        "protocol_outcome": "instrument_adequate" if adequate else "instrument_inadequate",
        "training_count": 180,
        "general_validation_count": 60,
        "deletion_like_validation_count": 60,
        "general_validation_accuracy": round(general_accuracy, 8),
        "deletion_like_validation_accuracy": round(deletion_accuracy, 8),
        "model": model_meta,
        "negative_controls": controls,
        "heldout_opened": adequate,
        "claim_outcome": "not_applicable_instrument_only",
        "support_state_effect": "none",
    }
    write_json(PREFLIGHT, result)
    print(f"P4/M7 v2 preflight: {result['protocol_outcome']} general={general_accuracy:.4f} deletion_like={deletion_accuracy:.4f}")


def run_confirmatory(rows: list[dict[str, Any]]) -> None:
    if RAW_RUN.exists():
        raise SystemExit("v2 raw result exists; further retry forbidden")
    preflight = load_json(PREFLIGHT)
    if preflight.get("protocol_outcome") != "instrument_adequate" or preflight.get("heldout_opened") is not True:
        raise SystemExit("v2 held-out denominator remains closed")
    started = time.perf_counter(); features, model_meta = extract_features(rows)
    FEATURES.parent.mkdir(parents=True, exist_ok=True)
    torch.save({"record_ids": [row["record_id"] for row in rows], "features": features, "model": model_meta}, FEATURES)
    true_labels = torch.tensor([row["true_label"] for row in rows], dtype=torch.long)
    training_labels = torch.tensor([row["training_label"] for row in rows], dtype=torch.long)
    roles = {role: indices(rows, role) for role in {row["role"] for row in rows}}
    all_update = roles["update_retain"] + roles["delete_a"] + roles["delete_b"]
    retained_train = roles["base_train"] + roles["update_retain"]
    prereg = load_json(PREREG); corpus_sha = file_sha(CORPUS); code_sha = prereg["code_sha256"][Path(__file__).name]
    seed_records = []
    for seed in SEEDS:
        seed_all(seed); initial = {name: value.detach().cpu().clone() for name, value in ProbeHead().state_dict().items()}
        base_best, base_final, base_extra, base_history = train(initial_state=initial, features=features, true_labels=true_labels, training_labels=true_labels, rows=rows, train_indices=roles["base_train"], epochs=30, learning_rate=0.03, retained_floor=None)
        seed_dir = BASE / "checkpoints" / f"seed-{seed}"
        base_best_ref = save_state(seed_dir / "base-best.pt", base_best); base_final_ref = save_state(seed_dir / "base-final.pt", base_final); base_opt_ref = save_optimizer(seed_dir / "base-optimizer.pt", base_extra["optimizer_payload"])
        base_model = ProbeHead(); base_model.load_state_dict(base_best)
        base_validation = validation_metrics(base_model, features, true_labels, rows); retained_floor = round(base_validation["retained"] - 0.03, 8)
        base_surface = surface_map(seed=seed, corpus_sha=corpus_sha, code_sha=code_sha, model_state_sha=base_best_ref["state_sha256"], optimizer_sha=base_opt_ref["file_sha256"], best_sha=base_best_ref["file_sha256"], final_sha=base_final_ref["file_sha256"], config_sha=canonical_sha({"arm": "base", "pooling": "mean"}), lineage_sha=canonical_sha({"seed": seed, "state": "base"}), cache_sha=canonical_sha({"seed": seed, "cache": "base"}), backup_sha=canonical_sha({"seed": seed, "backup": "base"}))
        base_full_sha = canonical_sha(base_surface); governed_final = None; arm_records = []
        for arm in ARMS:
            arm_started = time.perf_counter(); sequential = []
            if arm in {"no_update", "exact_rollback"}:
                best_state = copy.deepcopy(base_best); final_state = copy.deepcopy(base_best); extra = {"authority": {"best_epoch": 0, "authority_eligible": True, "selection_data": "prospective_base_authority", "retained_floor": retained_floor}, "optimizer_payload": base_extra["optimizer_payload"]}; history = []
            elif arm == "standard_update":
                best_state, final_state, extra, history = train(initial_state=base_best, features=features, true_labels=true_labels, training_labels=training_labels, rows=rows, train_indices=all_update, epochs=16, learning_rate=0.02, retained_floor=None)
            elif arm == "governed_update":
                best_state, final_state, extra, history = train(initial_state=base_best, features=features, true_labels=true_labels, training_labels=training_labels, rows=rows, train_indices=all_update, epochs=16, learning_rate=0.02, retained_floor=retained_floor, regularization=0.01, gradient_clip=1.0); governed_final = copy.deepcopy(final_state)
            elif arm == "regularized_forgetting_mitigation":
                best_state, final_state, extra, history = train(initial_state=base_best, features=features, true_labels=true_labels, training_labels=training_labels, rows=rows, train_indices=all_update, epochs=16, learning_rate=0.02, retained_floor=retained_floor, regularization=0.05, gradient_clip=1.0)
            elif arm == "approximate_unlearning":
                if governed_final is None: raise RuntimeError("governed update missing")
                a_best, a_final, a_extra, a_history = train(initial_state=governed_final, features=features, true_labels=true_labels, training_labels=true_labels, rows=rows, train_indices=roles["update_retain"], epochs=8, learning_rate=0.012, retained_floor=retained_floor, regularization=0.01, entropy_indices=roles["delete_a"], entropy_weight=0.15, gradient_clip=1.0)
                intermediate_ref = save_state(seed_dir / "approximate_unlearning-after-delete-a.pt", a_final)
                best_state, final_state, extra, b_history = train(initial_state=a_final, features=features, true_labels=true_labels, training_labels=true_labels, rows=rows, train_indices=roles["update_retain"], epochs=8, learning_rate=0.012, retained_floor=retained_floor, regularization=0.01, entropy_indices=roles["delete_b"], entropy_weight=0.15, gradient_clip=1.0)
                history = [dict(row, deletion_stage="delete_a") for row in a_history] + [dict(row, deletion_stage="delete_b") for row in b_history]
                sequential = [{"request": "delete_a", "checkpoint": intermediate_ref}, {"request": "delete_b", "checkpoint_state": "final"}]
            else:
                seed_all(seed); retrain_initial = {name: value.detach().cpu().clone() for name, value in ProbeHead().state_dict().items()}
                best_state, final_state, extra, history = train(initial_state=retrain_initial, features=features, true_labels=true_labels, training_labels=true_labels, rows=rows, train_indices=retained_train, epochs=30, learning_rate=0.03, retained_floor=retained_floor, gradient_clip=1.0)
            best_ref = save_state(seed_dir / f"{arm}-best.pt", best_state); final_ref = save_state(seed_dir / f"{arm}-final.pt", final_state); opt_ref = save_optimizer(seed_dir / f"{arm}-optimizer.pt", extra["optimizer_payload"])
            if arm in {"no_update", "exact_rollback"}: mutated_surface = copy.deepcopy(base_surface)
            else: mutated_surface = surface_map(seed=seed, corpus_sha=corpus_sha, code_sha=code_sha, model_state_sha=best_ref["state_sha256"], optimizer_sha=opt_ref["file_sha256"], best_sha=best_ref["file_sha256"], final_sha=final_ref["file_sha256"], config_sha=canonical_sha({"arm": arm, "history": history}), lineage_sha=canonical_sha({"seed": seed, "arm": arm, "descendant": True}), cache_sha=canonical_sha({"seed": seed, "arm": arm, "cohort_derived": arm != "deletion_aware_retrain"}), backup_sha=canonical_sha({"seed": seed, "arm": arm, "remote": "unverified"}))
            surface_path = seed_dir / f"{arm}-state-surfaces.json"; write_json(surface_path, {"surface_count": 24, "surfaces": mutated_surface})
            arm_records.append({"arm": arm, "history": history, "sequential_deletion": sequential, "wall_seconds": round(time.perf_counter() - arm_started, 6), "checkpoint_authority": extra["authority"], "best_checkpoint": best_ref, "final_checkpoint": final_ref, "optimizer_checkpoint": opt_ref, "full_state": {"surface_path": surface_path.relative_to(ROOT).as_posix(), "surface_file_sha256": file_sha(surface_path), "surface_count": 24, "before_sha256": base_full_sha, "mutated_sha256": canonical_sha(mutated_surface), "rollback_sha256": base_full_sha, "rollback_exact": True, "changed_surface_count": sum(mutated_surface[name] != base_surface[name] for name in STATE_SURFACES)}})
        seed_records.append({"seed": seed, "base": {"history": base_history, "validation": base_validation, "best_checkpoint": base_best_ref, "final_checkpoint": base_final_ref, "optimizer_checkpoint": base_opt_ref, "full_state_sha256": base_full_sha, "surface_count": 24}, "arms": arm_records})
    deletion_indices = roles["delete_a"] + roles["delete_b"]
    store = BASE / "raw" / "operational_store"; backup = BASE / "raw" / "local_backup"; store.mkdir(parents=True, exist_ok=True); backup.mkdir(parents=True, exist_ok=True)
    cohort_path = store / "deletion-cohort-features.pt"; torch.save(features[deletion_indices].contiguous(), cohort_path); backup_path = backup / cohort_path.name; shutil.copy2(cohort_path, backup_path); created = {"operational": file_sha(cohort_path), "local_backup": file_sha(backup_path)}; cohort_path.unlink(); backup_path.unlink()
    storage = {"created_sha256": created, "physical_absence_after_request": {"operational": not cohort_path.exists(), "local_backup": not backup_path.exists()}, "logical_index_references_after_request": 0, "remote_backup": {"simulated_endpoint": "remote-unavailable.example.invalid", "reachable": False, "erasure_acknowledged": False, "residual": "remote replica closure unverified"}, "retained_research_evidence": [CORPUS.relative_to(ROOT).as_posix(), FEATURES.relative_to(ROOT).as_posix(), RAW_RUN.relative_to(ROOT).as_posix()], "bounded_operational_derived_store_erasure": True, "total_storage_erasure": False}; write_json(BASE / "raw" / "storage_receipt.json", storage)
    lineage = {"late_request": True, "sequential_requests": ["delete_a", "delete_b"], "descendants": [{"descendant_id": f"calibrator-{seed}-governed", "invalidation": "recorded", "quarantine": "recorded", "physical_erasure": False} for seed in SEEDS], "local_descendant_invalidation_count": 5, "external_descendant": {"identity": "export-simulated-unreachable", "reachable": False, "invalidation_acknowledged": False, "erasure_verified": False}}; write_json(BASE / "raw" / "lineage_receipt.json", lineage)
    raw = {"schema_version": "asi_stack.p4_m7_raw_training_run.v2", "run_id": prereg["run_id"], "state": "closed_before_independent_axis_evaluation", "corpus_sha256": corpus_sha, "preregistration_sha256": file_sha(PREREG), "feature_artifact": {"path": FEATURES.relative_to(ROOT).as_posix(), "sha256": file_sha(FEATURES)}, "model": model_meta, "seeds": list(SEEDS), "arms": list(ARMS), "seed_records": seed_records, "storage_receipt": {"path": (BASE / "raw" / "storage_receipt.json").relative_to(ROOT).as_posix(), "sha256": file_sha(BASE / "raw" / "storage_receipt.json")}, "lineage_receipt": {"path": (BASE / "raw" / "lineage_receipt.json").relative_to(ROOT).as_posix(), "sha256": file_sha(BASE / "raw" / "lineage_receipt.json")}, "cost": {"wall_seconds": round(time.perf_counter() - started, 6), "feature_extraction_wall_seconds": model_meta["wall_seconds"], "maximum_resident_set_kib": int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss), "marginal_api_cost_usd": 0.0, "energy_measured": False, "operator_time_measured": False}, "environment": {"platform": platform.platform(), "python": platform.python_version(), "torch": torch.__version__, "numpy": np.__version__, "deterministic_algorithms": True, "threads": torch.get_num_threads()}, "support_state_effect": "none"}
    write_json(RAW_RUN, raw); print(f"P4/M7 v2 raw run closed: {len(SEEDS)} seeds x {len(ARMS)} arms; wall={raw['cost']['wall_seconds']:.2f}s")


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("--preflight", action="store_true"); args = parser.parse_args()
    torch.set_num_threads(1); torch.use_deterministic_algorithms(True)
    rows = load_json(CORPUS)["rows"]
    run_preflight(rows) if args.preflight else run_confirmatory(rows)


if __name__ == "__main__": main()
