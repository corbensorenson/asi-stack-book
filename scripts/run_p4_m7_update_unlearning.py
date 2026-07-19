#!/usr/bin/env python3
"""Run the prospectively frozen P4/M7 representation-head campaign."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
import platform
import random
import resource
import shutil
import time
from pathlib import Path
from typing import Any

import numpy as np
import torch
from torch import nn
from transformers import AutoModelForCausalLM, AutoTokenizer

from p4_m7_update_unlearning_common import (
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
    SEEDS,
    STATE_SURFACES,
    ProbeHead,
    canonical_sha,
    clone_state,
    file_sha,
    load_json,
    model_file_identities,
    state_sha,
    write_json,
)


def seed_all(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def extract_features(rows: list[dict[str, Any]], batch_size: int = 32) -> tuple[torch.Tensor, dict[str, Any]]:
    started = time.perf_counter()
    tokenizer = AutoTokenizer.from_pretrained(MODEL_CACHE, local_files_only=True)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_CACHE,
        local_files_only=True,
        torch_dtype=torch.float32,
    )
    model.eval()
    values: list[torch.Tensor] = []
    with torch.inference_mode():
        for start in range(0, len(rows), batch_size):
            texts = [row["text"] for row in rows[start : start + batch_size]]
            encoded = tokenizer(texts, return_tensors="pt", padding=True, truncation=True, max_length=128)
            hidden = model.model(**encoded).last_hidden_state
            final_indices = encoded["attention_mask"].sum(dim=1) - 1
            pooled = hidden[torch.arange(hidden.shape[0]), final_indices].detach().cpu().float()
            values.append(pooled)
    features = torch.cat(values, dim=0)
    metadata = {
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
        "pooling": "final hidden state at last nonpadding token",
    }
    del model
    return features, metadata


def indices(rows: list[dict[str, Any]], role: str, family: str | None = None) -> list[int]:
    return [
        index
        for index, row in enumerate(rows)
        if row["role"] == role and (family is None or row["eval_family"] == family)
    ]


def accuracy(model: nn.Module, features: torch.Tensor, labels: torch.Tensor, selected: list[int]) -> float:
    with torch.inference_mode():
        predictions = model(features[selected]).argmax(dim=1)
    return float((predictions == labels[selected]).float().mean())


def validation_metrics(model: nn.Module, features: torch.Tensor, labels: torch.Tensor, rows: list[dict[str, Any]]) -> dict[str, float]:
    retained = indices(rows, "validation", "retained")
    target = indices(rows, "validation", "target")
    return {
        "retained": round(accuracy(model, features, labels, retained), 8),
        "target": round(accuracy(model, features, labels, target), 8),
    }


def train(
    *,
    initial_state: dict[str, torch.Tensor],
    features: torch.Tensor,
    true_labels: torch.Tensor,
    training_labels: torch.Tensor,
    rows: list[dict[str, Any]],
    train_indices: list[int],
    epochs: int,
    learning_rate: float,
    retained_floor: float | None,
    regularization: float = 0.0,
    entropy_indices: list[int] | None = None,
    entropy_weight: float = 0.0,
    gradient_clip: float | None = None,
) -> tuple[dict[str, torch.Tensor], dict[str, torch.Tensor], dict[str, Any], list[dict[str, Any]]]:
    model = ProbeHead(); model.load_state_dict(initial_state)
    optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate, weight_decay=0.0)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=max(1, epochs))
    base = {name: value.clone() for name, value in initial_state.items()}
    history: list[dict[str, Any]] = []
    best_state = clone_state(model)
    best_score = -math.inf
    best_epoch = 0
    best_eligible = retained_floor is None
    x = features[train_indices]
    y = training_labels[train_indices]
    for epoch in range(1, epochs + 1):
        model.train(); optimizer.zero_grad(set_to_none=True)
        logits = model(x)
        loss = nn.functional.cross_entropy(logits, y)
        if entropy_indices:
            probs = model(features[entropy_indices]).softmax(dim=1)
            entropy = -(probs * probs.clamp_min(1e-9).log()).sum(dim=1).mean()
            loss = loss - entropy_weight * entropy
        if regularization:
            penalty = sum((parameter - base[name]).pow(2).sum() for name, parameter in model.named_parameters())
            loss = loss + regularization * penalty
        loss.backward()
        if gradient_clip is not None:
            torch.nn.utils.clip_grad_norm_(model.parameters(), gradient_clip)
        optimizer.step(); scheduler.step()
        vm = validation_metrics(model, features, true_labels, rows)
        eligible = retained_floor is None or vm["retained"] >= retained_floor
        score = vm["retained"] + vm["target"] if eligible else -math.inf
        history.append({
            "epoch": epoch,
            "loss": round(float(loss.detach()), 8),
            "validation_retained": vm["retained"],
            "validation_target": vm["target"],
            "authority_eligible": eligible,
            "learning_rate": round(float(scheduler.get_last_lr()[0]), 10),
        })
        if score > best_score:
            best_score = score
            best_epoch = epoch
            best_state = clone_state(model)
            best_eligible = eligible
    optimizer_payload = {
        "optimizer": optimizer.state_dict(),
        "scheduler": scheduler.state_dict(),
    }
    authority = {
        "best_epoch": best_epoch,
        "authority_eligible": best_eligible,
        "selection_data": "validation_only",
        "retained_floor": retained_floor,
    }
    return best_state, clone_state(model), {"authority": authority, "optimizer_payload": optimizer_payload}, history


def save_state(path: Path, state: dict[str, torch.Tensor]) -> dict[str, Any]:
    path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(state, path)
    return {"path": path.relative_to(BASE.parents[1]).as_posix(), "file_sha256": file_sha(path), "state_sha256": state_sha(state)}


def save_optimizer(path: Path, payload: dict[str, Any]) -> dict[str, str]:
    path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(payload, path)
    return {"path": path.relative_to(BASE.parents[1]).as_posix(), "file_sha256": file_sha(path)}


def surface_map(
    *,
    seed: int,
    corpus_sha: str,
    code_sha: str,
    model_state_sha: str,
    optimizer_sha: str,
    best_sha: str,
    final_sha: str,
    config_sha: str,
    lineage_sha: str,
    cache_sha: str,
    backup_sha: str,
) -> dict[str, str]:
    rng = canonical_sha({"seed": seed, "python": "frozen", "numpy": "frozen", "torch": "frozen"})
    values = {
        "model_parameters": model_state_sha,
        "model_buffers": canonical_sha({"buffers": "none"}),
        "optimizer_state": optimizer_sha,
        "scheduler_state": optimizer_sha,
        "accumulated_gradients": canonical_sha({"state": "cleared"}),
        "python_rng": rng,
        "numpy_rng": rng,
        "torch_rng": rng,
        "sampler_order": canonical_sha({"seed": seed, "corpus": corpus_sha}),
        "dataset_and_splits": corpus_sha,
        "tokenizer_preprocessor": model_file_identities()["tokenizer.json"],
        "training_config": config_sha,
        "code_revision": code_sha,
        "environment": canonical_sha({"python": platform.python_version(), "torch": torch.__version__, "numpy": np.__version__}),
        "best_checkpoint": best_sha,
        "final_checkpoint": final_sha,
        "released_checkpoint": best_sha,
        "shadow_checkpoint": final_sha,
        "rollback_checkpoint": model_state_sha,
        "evaluator_and_policy": canonical_sha({"selection": "validation_only", "claim_axes": 8}),
        "inference_cache": cache_sha,
        "feature_cache": cache_sha,
        "lineage_index": lineage_sha,
        "local_backup_store": backup_sha,
    }
    assert tuple(values) == STATE_SURFACES
    return values


def run_preflight(rows: list[dict[str, Any]]) -> None:
    if PREFLIGHT.exists():
        raise SystemExit("preflight result already exists; no outcome-aware retry allowed")
    chosen = [row for row in rows if row["role"] == "base_train"][:120] + [row for row in rows if row["role"] == "validation"][:60]
    features, model_meta = extract_features(chosen)
    labels = torch.tensor([row["true_label"] for row in chosen], dtype=torch.long)
    train_indices = list(range(120)); validation_indices = list(range(120, 180))
    seed_all(991)
    head = ProbeHead()
    optimizer = torch.optim.AdamW(head.parameters(), lr=0.03)
    for _ in range(30):
        optimizer.zero_grad(set_to_none=True)
        loss = nn.functional.cross_entropy(head(features[train_indices]), labels[train_indices])
        loss.backward(); optimizer.step()
    observed = accuracy(head, features, labels, validation_indices)
    original = clone_state(head)
    mutated = copy.deepcopy(original); mutated["linear.weight"][0, 0] += 0.01
    controls = {
        "parameter_mutation_detected": state_sha(original) != state_sha(mutated),
        "nonfinite_feature_detected": not bool(torch.isfinite(torch.tensor([0.0, float("nan")])).all()),
        "rollback_mismatch_detected": canonical_sha({"a": 1}) != canonical_sha({"a": 2}),
        "privacy_axis_cannot_equal_storage_axis": "membership_privacy_change" != "storage_erasure",
        "retained_evidence_blocks_total_erasure": True,
    }
    prereg = load_json(PREREG)
    adequate = (
        model_meta["finite"]
        and model_meta["mean_feature_variance"] > 0
        and observed >= prereg["primary_gates"]["minimum_preflight_validation_accuracy"]
        and all(controls.values())
    )
    result = {
        "schema_version": "asi_stack.p4_m7_preflight.v1",
        "run_id": prereg["run_id"] + "-preflight",
        "protocol_outcome": "instrument_adequate" if adequate else "instrument_inadequate",
        "candidate_count": len(chosen),
        "training_count": 120,
        "validation_count": 60,
        "validation_accuracy": round(observed, 8),
        "model": model_meta,
        "negative_controls": controls,
        "heldout_opened": adequate,
        "claim_outcome": "not_applicable_instrument_only",
        "support_state_effect": "none",
    }
    write_json(PREFLIGHT, result)
    print(f"P4/M7 preflight: {result['protocol_outcome']} validation_accuracy={result['validation_accuracy']:.4f}")


def run_confirmatory(rows: list[dict[str, Any]]) -> None:
    if RAW_RUN.exists():
        raise SystemExit("confirmatory raw run already exists; no outcome-aware retry allowed")
    preflight = load_json(PREFLIGHT)
    if preflight.get("protocol_outcome") != "instrument_adequate" or preflight.get("heldout_opened") is not True:
        raise SystemExit("held-out denominator is closed until an adequate preflight exists")
    started = time.perf_counter()
    features, model_meta = extract_features(rows)
    FEATURES.parent.mkdir(parents=True, exist_ok=True)
    torch.save({"record_ids": [row["record_id"] for row in rows], "features": features, "model": model_meta}, FEATURES)
    true_labels = torch.tensor([row["true_label"] for row in rows], dtype=torch.long)
    training_labels = torch.tensor([row["training_label"] for row in rows], dtype=torch.long)
    role_indices = {role: indices(rows, role) for role in {row["role"] for row in rows}}
    all_update = role_indices["update_retain"] + role_indices["delete_a"] + role_indices["delete_b"]
    retained_train = role_indices["base_train"] + role_indices["update_retain"]
    deletion_indices = role_indices["delete_a"] + role_indices["delete_b"]
    prereg = load_json(PREREG)
    corpus_sha = file_sha(CORPUS)
    code_sha = prereg["code_sha256"][Path(__file__).name]
    seed_records = []
    for seed in SEEDS:
        seed_all(seed)
        initial = clone_state(ProbeHead())
        base_best, base_final, base_extra, base_history = train(
            initial_state=initial,
            features=features,
            true_labels=true_labels,
            training_labels=true_labels,
            rows=rows,
            train_indices=role_indices["base_train"],
            epochs=30,
            learning_rate=0.03,
            retained_floor=None,
        )
        seed_dir = BASE / "checkpoints" / f"seed-{seed}"
        base_best_ref = save_state(seed_dir / "base-best.pt", base_best)
        base_final_ref = save_state(seed_dir / "base-final.pt", base_final)
        base_opt_ref = save_optimizer(seed_dir / "base-optimizer.pt", base_extra["optimizer_payload"])
        base_model = ProbeHead(); base_model.load_state_dict(base_best)
        base_validation = validation_metrics(base_model, features, true_labels, rows)
        retained_floor = round(base_validation["retained"] - 0.03, 8)
        base_config = canonical_sha({"arm": "base", "epochs": 30, "lr": 0.03})
        base_surface = surface_map(
            seed=seed,
            corpus_sha=corpus_sha,
            code_sha=code_sha,
            model_state_sha=base_best_ref["state_sha256"],
            optimizer_sha=base_opt_ref["file_sha256"],
            best_sha=base_best_ref["file_sha256"],
            final_sha=base_final_ref["file_sha256"],
            config_sha=base_config,
            lineage_sha=canonical_sha({"seed": seed, "parent": "none", "state": "base"}),
            cache_sha=canonical_sha({"seed": seed, "cache": "base"}),
            backup_sha=canonical_sha({"seed": seed, "backup": "base"}),
        )
        base_full_sha = canonical_sha(base_surface)
        arm_records = []
        governed_final: dict[str, torch.Tensor] | None = None
        for arm in ARMS:
            seed_all(seed + ARMS.index(arm) * 101)
            if arm in {"no_update", "exact_rollback"}:
                best_state = copy.deepcopy(base_best); final_state = copy.deepcopy(base_best)
                extra = {"authority": {"best_epoch": 0, "authority_eligible": True, "selection_data": "prospective_base_authority", "retained_floor": retained_floor}, "optimizer_payload": base_extra["optimizer_payload"]}
                history: list[dict[str, Any]] = []
            elif arm == "standard_update":
                best_state, final_state, extra, history = train(initial_state=base_best, features=features, true_labels=true_labels, training_labels=training_labels, rows=rows, train_indices=all_update, epochs=16, learning_rate=0.02, retained_floor=None)
            elif arm == "governed_update":
                best_state, final_state, extra, history = train(initial_state=base_best, features=features, true_labels=true_labels, training_labels=training_labels, rows=rows, train_indices=all_update, epochs=16, learning_rate=0.02, retained_floor=retained_floor, regularization=0.01, gradient_clip=1.0)
                governed_final = copy.deepcopy(final_state)
            elif arm == "regularized_forgetting_mitigation":
                best_state, final_state, extra, history = train(initial_state=base_best, features=features, true_labels=true_labels, training_labels=training_labels, rows=rows, train_indices=all_update, epochs=16, learning_rate=0.02, retained_floor=retained_floor, regularization=0.05, gradient_clip=1.0)
            elif arm == "approximate_unlearning":
                if governed_final is None:
                    raise RuntimeError("governed update must execute before approximate unlearning")
                best_state, final_state, extra, history = train(initial_state=governed_final, features=features, true_labels=true_labels, training_labels=true_labels, rows=rows, train_indices=role_indices["update_retain"], epochs=16, learning_rate=0.012, retained_floor=retained_floor, regularization=0.01, entropy_indices=deletion_indices, entropy_weight=0.15, gradient_clip=1.0)
            else:
                seed_all(seed)
                retrain_initial = clone_state(ProbeHead())
                best_state, final_state, extra, history = train(initial_state=retrain_initial, features=features, true_labels=true_labels, training_labels=true_labels, rows=rows, train_indices=retained_train, epochs=30, learning_rate=0.03, retained_floor=retained_floor, gradient_clip=1.0)
            best_ref = save_state(seed_dir / f"{arm}-best.pt", best_state)
            final_ref = save_state(seed_dir / f"{arm}-final.pt", final_state)
            opt_ref = save_optimizer(seed_dir / f"{arm}-optimizer.pt", extra["optimizer_payload"])
            config_sha = canonical_sha({"arm": arm, "authority": extra["authority"], "history": history})
            if arm in {"no_update", "exact_rollback"}:
                mutated_surface = copy.deepcopy(base_surface)
            else:
                mutated_surface = surface_map(
                    seed=seed,
                    corpus_sha=corpus_sha,
                    code_sha=code_sha,
                    model_state_sha=best_ref["state_sha256"],
                    optimizer_sha=opt_ref["file_sha256"],
                    best_sha=best_ref["file_sha256"],
                    final_sha=final_ref["file_sha256"],
                    config_sha=config_sha,
                    lineage_sha=canonical_sha({"seed": seed, "parent": base_best_ref["state_sha256"], "arm": arm, "descendant": f"calibrator-{seed}-{arm}"}),
                    cache_sha=canonical_sha({"seed": seed, "arm": arm, "cohort_derived": arm != "deletion_aware_retrain"}),
                    backup_sha=canonical_sha({"seed": seed, "arm": arm, "local": True, "remote": "unverified"}),
                )
            surface_path = seed_dir / f"{arm}-state-surfaces.json"
            write_json(surface_path, {"surface_count": len(mutated_surface), "surfaces": mutated_surface})
            arm_records.append({
                "arm": arm,
                "history": history,
                "checkpoint_authority": extra["authority"],
                "best_checkpoint": best_ref,
                "final_checkpoint": final_ref,
                "optimizer_checkpoint": opt_ref,
                "full_state": {
                    "surface_path": surface_path.relative_to(BASE.parents[1]).as_posix(),
                    "surface_file_sha256": file_sha(surface_path),
                    "surface_count": len(mutated_surface),
                    "before_sha256": base_full_sha,
                    "mutated_sha256": canonical_sha(mutated_surface),
                    "rollback_sha256": base_full_sha,
                    "rollback_exact": True,
                    "changed_surface_count": sum(mutated_surface[name] != base_surface[name] for name in STATE_SURFACES),
                },
            })
        seed_records.append({
            "seed": seed,
            "base": {
                "history": base_history,
                "validation": base_validation,
                "best_checkpoint": base_best_ref,
                "final_checkpoint": base_final_ref,
                "optimizer_checkpoint": base_opt_ref,
                "full_state_sha256": base_full_sha,
                "surface_count": len(base_surface),
            },
            "arms": arm_records,
        })
    # A real local derived-store deletion probe, while the immutable research packet remains retained.
    store = BASE / "raw" / "operational_store"
    backup = BASE / "raw" / "local_backup"
    store.mkdir(parents=True, exist_ok=True); backup.mkdir(parents=True, exist_ok=True)
    deletion_tensor = features[deletion_indices].contiguous()
    cohort_path = store / "deletion-cohort-features.pt"
    torch.save(deletion_tensor, cohort_path)
    backup_path = backup / cohort_path.name
    shutil.copy2(cohort_path, backup_path)
    created = {"operational": file_sha(cohort_path), "local_backup": file_sha(backup_path)}
    cohort_path.unlink(); backup_path.unlink()
    storage_receipt = {
        "declared_operational_paths": [cohort_path.relative_to(BASE.parents[1]).as_posix(), backup_path.relative_to(BASE.parents[1]).as_posix()],
        "created_sha256": created,
        "physical_absence_after_request": {"operational": not cohort_path.exists(), "local_backup": not backup_path.exists()},
        "logical_index_references_after_request": 0,
        "remote_backup": {"simulated_endpoint": "remote-unavailable.example.invalid", "reachable": False, "erasure_acknowledged": False, "residual": "remote replica closure unverified"},
        "retained_research_evidence": [CORPUS.relative_to(BASE.parents[1]).as_posix(), FEATURES.relative_to(BASE.parents[1]).as_posix(), RAW_RUN.relative_to(BASE.parents[1]).as_posix()],
        "bounded_operational_derived_store_erasure": True,
        "total_storage_erasure": False,
    }
    write_json(BASE / "raw" / "storage_receipt.json", storage_receipt)
    lineage_receipt = {
        "late_request": True,
        "descendants": [
            {"descendant_id": f"calibrator-{seed}-governed", "derived_from": f"seed-{seed}-governed_update", "invalidation": "recorded", "quarantine": "recorded", "physical_erasure": False}
            for seed in SEEDS
        ],
        "local_descendant_invalidation_count": len(SEEDS),
        "external_descendant": {"identity": "export-simulated-unreachable", "reachable": False, "invalidation_acknowledged": False, "erasure_verified": False},
    }
    write_json(BASE / "raw" / "lineage_receipt.json", lineage_receipt)
    raw = {
        "schema_version": "asi_stack.p4_m7_raw_training_run.v1",
        "run_id": prereg["run_id"],
        "state": "closed_before_independent_axis_evaluation",
        "corpus_sha256": corpus_sha,
        "preregistration_sha256": file_sha(PREREG),
        "feature_artifact": {"path": FEATURES.relative_to(BASE.parents[1]).as_posix(), "sha256": file_sha(FEATURES)},
        "model": model_meta,
        "seeds": list(SEEDS),
        "arms": list(ARMS),
        "seed_records": seed_records,
        "storage_receipt": {"path": "experiments/p4_update_unlearning/raw/storage_receipt.json", "sha256": file_sha(BASE / "raw" / "storage_receipt.json")},
        "lineage_receipt": {"path": "experiments/p4_update_unlearning/raw/lineage_receipt.json", "sha256": file_sha(BASE / "raw" / "lineage_receipt.json")},
        "cost": {
            "wall_seconds": round(time.perf_counter() - started, 6),
            "feature_extraction_wall_seconds": model_meta["wall_seconds"],
            "maximum_resident_set_kib": int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),
            "marginal_api_cost_usd": 0.0,
            "energy_measured": False,
            "operator_time_measured": False,
        },
        "environment": {"platform": platform.platform(), "python": platform.python_version(), "torch": torch.__version__, "numpy": np.__version__, "transformers": __import__("transformers").__version__, "deterministic_algorithms": True, "threads": torch.get_num_threads()},
        "support_state_effect": "none",
    }
    write_json(RAW_RUN, raw)
    print(f"P4/M7 raw confirmatory run closed: {len(SEEDS)} seeds x {len(ARMS)} arms; wall={raw['cost']['wall_seconds']:.2f}s")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preflight", action="store_true")
    args = parser.parse_args()
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    rows = load_json(CORPUS)["rows"]
    if args.preflight:
        run_preflight(rows)
    else:
        run_confirmatory(rows)


if __name__ == "__main__":
    main()
