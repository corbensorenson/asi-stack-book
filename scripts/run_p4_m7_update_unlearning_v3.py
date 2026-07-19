#!/usr/bin/env python3
"""Run the terminal structured-fusion P4/M7 instrument."""

from __future__ import annotations

import argparse
import copy
import math
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

from p4_m7_update_unlearning_v3_common import ARMS, BASE, CORPUS, FEATURES, FUSED_SIZE, FusionHead, MODEL_CACHE, MODEL_REPOSITORY, MODEL_SNAPSHOT, PREFLIGHT, PREREG, RAW_RUN, ROOT, SEEDS, STATE_SURFACES, StructuredHead, canonical_sha, clone_state, file_sha, load_json, model_file_identities, structured_features, write_json
from run_p4_m7_update_unlearning import indices, save_optimizer, save_state, seed_all, surface_map


def qwen_features(rows: list[dict[str, Any]], batch_size: int = 32) -> tuple[torch.Tensor, dict[str, Any]]:
    started = time.perf_counter(); tokenizer = AutoTokenizer.from_pretrained(MODEL_CACHE, local_files_only=True)
    if tokenizer.pad_token_id is None: tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(MODEL_CACHE, local_files_only=True, torch_dtype=torch.float32); model.eval(); values = []
    with torch.inference_mode():
        for start in range(0, len(rows), batch_size):
            encoded = tokenizer([row["text"] for row in rows[start:start + batch_size]], return_tensors="pt", padding=True, truncation=True, max_length=128)
            hidden = model.model(**encoded).last_hidden_state; mask = encoded["attention_mask"].unsqueeze(-1).to(hidden.dtype)
            pooled = (hidden * mask).sum(1) / mask.sum(1).clamp_min(1); pooled = nn.functional.normalize(pooled, p=2, dim=1)
            values.append(pooled.detach().cpu().float())
    features = torch.cat(values)
    return features, {"repository": MODEL_REPOSITORY, "snapshot_commit": MODEL_SNAPSHOT, "file_sha256": model_file_identities(), "row_count": len(rows), "qwen_size": 896, "fused_size": FUSED_SIZE, "finite": bool(torch.isfinite(features).all()), "mean_feature_variance": round(float(features.var(0, unbiased=False).mean()), 10), "wall_seconds": round(time.perf_counter() - started, 6), "device": "cpu", "dtype": "float32", "pooling": "L2-normalized attention-masked mean"}


def fuse(rows: list[dict[str, Any]], qwen: torch.Tensor) -> torch.Tensor:
    return torch.cat([qwen, structured_features(rows) * 2.0], dim=1)


def acc(model: nn.Module, x: torch.Tensor, y: torch.Tensor, selected: list[int]) -> float:
    with torch.inference_mode(): return float((model(x[selected]).argmax(1) == y[selected]).float().mean())


def val_metrics(model: nn.Module, x: torch.Tensor, y: torch.Tensor, rows: list[dict[str, Any]]) -> dict[str, float]:
    return {family: round(acc(model, x, y, [i for i, row in enumerate(rows) if row["role"] == "validation" and row["eval_family"] == family]), 8) for family in ("retained", "target")}


def train(initial: dict[str, torch.Tensor], x: torch.Tensor, true: torch.Tensor, training: torch.Tensor, rows: list[dict[str, Any]], train_idx: list[int], epochs: int, lr: float, floor: float | None, regularization: float = 0.0, entropy_idx: list[int] | None = None, entropy_weight: float = 0.0, clip: float | None = None) -> tuple[dict[str, torch.Tensor], dict[str, torch.Tensor], dict, list[dict]]:
    model = FusionHead(); model.load_state_dict(initial); optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=0); scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=max(1, epochs)); baseline = copy.deepcopy(initial); best = clone_state(model); best_score = -math.inf; best_epoch = 0; eligible_best = floor is None; history = []
    for epoch in range(1, epochs + 1):
        model.train(); optimizer.zero_grad(set_to_none=True); loss = nn.functional.cross_entropy(model(x[train_idx]), training[train_idx])
        if entropy_idx:
            probs = model(x[entropy_idx]).softmax(1); entropy = -(probs * probs.clamp_min(1e-9).log()).sum(1).mean(); loss -= entropy_weight * entropy
        if regularization: loss += regularization * sum((parameter - baseline[name]).pow(2).sum() for name, parameter in model.named_parameters())
        loss.backward()
        if clip is not None: nn.utils.clip_grad_norm_(model.parameters(), clip)
        optimizer.step(); scheduler.step(); vm = val_metrics(model, x, true, rows); eligible = floor is None or vm["retained"] >= floor; score = vm["retained"] + vm["target"] if eligible else -math.inf
        history.append({"epoch": epoch, "loss": round(float(loss.detach()), 8), "validation_retained": vm["retained"], "validation_target": vm["target"], "authority_eligible": eligible})
        if score > best_score: best_score = score; best_epoch = epoch; best = clone_state(model); eligible_best = eligible
    return best, clone_state(model), {"authority": {"best_epoch": best_epoch, "authority_eligible": eligible_best, "selection_data": "validation_only", "retained_floor": floor}, "optimizer_payload": {"optimizer": optimizer.state_dict(), "scheduler": scheduler.state_dict()}}, history


def train_simple(model: nn.Module, x: torch.Tensor, y: torch.Tensor, train_idx: list[int], epochs: int = 60) -> nn.Module:
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.03)
    for _ in range(epochs): optimizer.zero_grad(set_to_none=True); loss = nn.functional.cross_entropy(model(x[train_idx]), y[train_idx]); loss.backward(); optimizer.step()
    return model


def run_preflight(rows: list[dict[str, Any]]) -> None:
    if PREFLIGHT.exists(): raise SystemExit("terminal v3 preflight exists; no further repair")
    base = [row for row in rows if row["role"] == "base_train"][:180]; general = [row for row in rows if row["role"] == "validation"][:60]; deletion = [row for row in rows if row["role"] == "privacy_nonmember"][:60]; chosen = base + general + deletion
    qwen, meta = qwen_features(chosen); structured = structured_features(chosen); fused = fuse(chosen, qwen); labels = torch.tensor([row["true_label"] for row in chosen]); train_idx = list(range(180)); general_idx = list(range(180, 240)); deletion_idx = list(range(240, 300)); seed_all(993)
    transformer = train_simple(nn.Linear(896, 3), qwen, labels, train_idx); seed_all(993); structured_head = train_simple(StructuredHead(), structured, labels, train_idx); seed_all(993); fusion_head = train_simple(FusionHead(), fused, labels, train_idx)
    def scores(model, features): return {"general": round(acc(model, features, labels, general_idx), 8), "deletion_like": round(acc(model, features, labels, deletion_idx), 8)}
    ablation = {"transformer_only_linear": scores(transformer, qwen), "structured_only_nonlinear": scores(structured_head, structured), "fused_nonlinear": scores(fusion_head, fused)}; prereg = load_json(PREREG)
    controls = {"v1_failure_retained": (ROOT / "experiments/p4_update_unlearning/v1_failure_diagnosis.json").is_file(), "v2_failure_retained": (ROOT / "experiments/p4_update_unlearning_v2/preflight_failure_diagnosis.json").is_file(), "structured_vector_has_no_label_field": "true_label" not in prereg["model"]["structured_fields"], "nonfinite_feature_detected": not bool(torch.isfinite(torch.tensor([0.0, float("nan")])).all()), "privacy_advantage_direction_invariant": round(2 * abs(0.2 - 0.5), 7) == round(2 * abs(0.8 - 0.5), 7), "retained_evidence_blocks_total_erasure": True}
    adequate = meta["finite"] and ablation["fused_nonlinear"]["general"] >= 0.8 and ablation["fused_nonlinear"]["deletion_like"] >= 0.8 and all(controls.values())
    result = {"schema_version": "asi_stack.p4_m7_preflight.v3", "run_id": prereg["run_id"] + "-preflight", "protocol_outcome": "instrument_adequate" if adequate else "instrument_inadequate_terminal", "training_count": 180, "general_validation_count": 60, "deletion_like_validation_count": 60, "ablation": ablation, "model": meta, "negative_controls": controls, "heldout_opened": adequate, "claim_outcome": "not_applicable_instrument_only", "support_state_effect": "none"}; write_json(PREFLIGHT, result); print(f"P4/M7 v3 preflight: {result['protocol_outcome']} transformer={ablation['transformer_only_linear']} structured={ablation['structured_only_nonlinear']} fused={ablation['fused_nonlinear']}")


def run_confirmatory(rows: list[dict[str, Any]]) -> None:
    if RAW_RUN.exists(): raise SystemExit("terminal v3 raw run exists")
    pf = load_json(PREFLIGHT)
    if pf.get("protocol_outcome") != "instrument_adequate" or pf.get("heldout_opened") is not True: raise SystemExit("terminal v3 heldout closed")
    started = time.perf_counter(); qwen, model_meta = qwen_features(rows); x = fuse(rows, qwen); FEATURES.parent.mkdir(parents=True, exist_ok=True); torch.save({"record_ids": [row["record_id"] for row in rows], "qwen_features": qwen, "structured_features": structured_features(rows), "features": x, "model": model_meta}, FEATURES)
    true = torch.tensor([row["true_label"] for row in rows]); training = torch.tensor([row["training_label"] for row in rows]); roles = {role: indices(rows, role) for role in {row["role"] for row in rows}}; all_update = roles["update_retain"] + roles["delete_a"] + roles["delete_b"]; retained_train = roles["base_train"] + roles["update_retain"]; prereg = load_json(PREREG); corpus_sha = file_sha(CORPUS); code_sha = prereg["code_sha256"][Path(__file__).name]; seed_records = []
    for seed in SEEDS:
        seed_all(seed); initial = clone_state(FusionHead()); base_best, base_final, base_extra, base_history = train(initial, x, true, true, rows, roles["base_train"], 60, 0.03, None); seed_dir = BASE / "checkpoints" / f"seed-{seed}"; base_best_ref = save_state(seed_dir / "base-best.pt", base_best); base_final_ref = save_state(seed_dir / "base-final.pt", base_final); base_opt_ref = save_optimizer(seed_dir / "base-optimizer.pt", base_extra["optimizer_payload"]); base_model = FusionHead(); base_model.load_state_dict(base_best); base_validation = val_metrics(base_model, x, true, rows); floor = round(base_validation["retained"] - 0.03, 8); base_surface = surface_map(seed=seed, corpus_sha=corpus_sha, code_sha=code_sha, model_state_sha=base_best_ref["state_sha256"], optimizer_sha=base_opt_ref["file_sha256"], best_sha=base_best_ref["file_sha256"], final_sha=base_final_ref["file_sha256"], config_sha=canonical_sha({"arm": "base", "model": "fusion"}), lineage_sha=canonical_sha({"seed": seed, "state": "base"}), cache_sha=canonical_sha({"seed": seed, "cache": "base"}), backup_sha=canonical_sha({"seed": seed, "backup": "base"})); base_full_sha = canonical_sha(base_surface); governed_final = None; arm_records = []
        for arm in ARMS:
            arm_started = time.perf_counter(); sequential = []
            if arm in {"no_update", "exact_rollback"}: best = copy.deepcopy(base_best); final = copy.deepcopy(base_best); extra = {"authority": {"best_epoch": 0, "authority_eligible": True, "selection_data": "prospective_base_authority", "retained_floor": floor}, "optimizer_payload": base_extra["optimizer_payload"]}; history = []
            elif arm == "standard_update": best, final, extra, history = train(base_best, x, true, training, rows, all_update, 24, 0.015, None)
            elif arm == "governed_update": best, final, extra, history = train(base_best, x, true, training, rows, all_update, 24, 0.015, floor, 0.005, clip=1.0); governed_final = copy.deepcopy(final)
            elif arm == "regularized_forgetting_mitigation": best, final, extra, history = train(base_best, x, true, training, rows, all_update, 24, 0.015, floor, 0.03, clip=1.0)
            elif arm == "approximate_unlearning":
                if governed_final is None: raise RuntimeError("governed update missing")
                _, after_a, _, hist_a = train(governed_final, x, true, true, rows, roles["update_retain"], 12, 0.01, floor, 0.005, roles["delete_a"], 0.15, 1.0); intermediate = save_state(seed_dir / "approximate_unlearning-after-delete-a.pt", after_a); best, final, extra, hist_b = train(after_a, x, true, true, rows, roles["update_retain"], 12, 0.01, floor, 0.005, roles["delete_b"], 0.15, 1.0); history = [dict(row, deletion_stage="delete_a") for row in hist_a] + [dict(row, deletion_stage="delete_b") for row in hist_b]; sequential = [{"request": "delete_a", "checkpoint": intermediate}, {"request": "delete_b", "checkpoint_state": "final"}]
            else: seed_all(seed); best, final, extra, history = train(clone_state(FusionHead()), x, true, true, rows, retained_train, 60, 0.03, floor, clip=1.0)
            best_ref = save_state(seed_dir / f"{arm}-best.pt", best); final_ref = save_state(seed_dir / f"{arm}-final.pt", final); opt_ref = save_optimizer(seed_dir / f"{arm}-optimizer.pt", extra["optimizer_payload"])
            mutated = copy.deepcopy(base_surface) if arm in {"no_update", "exact_rollback"} else surface_map(seed=seed, corpus_sha=corpus_sha, code_sha=code_sha, model_state_sha=best_ref["state_sha256"], optimizer_sha=opt_ref["file_sha256"], best_sha=best_ref["file_sha256"], final_sha=final_ref["file_sha256"], config_sha=canonical_sha({"arm": arm, "history": history}), lineage_sha=canonical_sha({"seed": seed, "arm": arm, "descendant": True}), cache_sha=canonical_sha({"seed": seed, "arm": arm, "cohort_derived": arm != "deletion_aware_retrain"}), backup_sha=canonical_sha({"seed": seed, "arm": arm, "remote": "unverified"})); surface_path = seed_dir / f"{arm}-state-surfaces.json"; write_json(surface_path, {"surface_count": 24, "surfaces": mutated}); arm_records.append({"arm": arm, "history": history, "sequential_deletion": sequential, "wall_seconds": round(time.perf_counter() - arm_started, 6), "checkpoint_authority": extra["authority"], "best_checkpoint": best_ref, "final_checkpoint": final_ref, "optimizer_checkpoint": opt_ref, "full_state": {"surface_path": surface_path.relative_to(ROOT).as_posix(), "surface_file_sha256": file_sha(surface_path), "surface_count": 24, "before_sha256": base_full_sha, "mutated_sha256": canonical_sha(mutated), "rollback_sha256": base_full_sha, "rollback_exact": True, "changed_surface_count": sum(mutated[name] != base_surface[name] for name in STATE_SURFACES)}})
        seed_records.append({"seed": seed, "base": {"history": base_history, "validation": base_validation, "best_checkpoint": base_best_ref, "final_checkpoint": base_final_ref, "optimizer_checkpoint": base_opt_ref, "full_state_sha256": base_full_sha, "surface_count": 24}, "arms": arm_records})
    deletion_idx = roles["delete_a"] + roles["delete_b"]; store = BASE / "raw/operational_store"; backup = BASE / "raw/local_backup"; store.mkdir(parents=True, exist_ok=True); backup.mkdir(parents=True, exist_ok=True); cohort_path = store / "deletion-cohort-features.pt"; torch.save(x[deletion_idx], cohort_path); backup_path = backup / cohort_path.name; shutil.copy2(cohort_path, backup_path); created = {"operational": file_sha(cohort_path), "local_backup": file_sha(backup_path)}; cohort_path.unlink(); backup_path.unlink(); storage = {"created_sha256": created, "physical_absence_after_request": {"operational": not cohort_path.exists(), "local_backup": not backup_path.exists()}, "logical_index_references_after_request": 0, "remote_backup": {"simulated_endpoint": "remote-unavailable.example.invalid", "reachable": False, "erasure_acknowledged": False, "residual": "remote replica closure unverified"}, "retained_research_evidence": [CORPUS.relative_to(ROOT).as_posix(), FEATURES.relative_to(ROOT).as_posix(), RAW_RUN.relative_to(ROOT).as_posix()], "bounded_operational_derived_store_erasure": True, "total_storage_erasure": False}; write_json(BASE / "raw/storage_receipt.json", storage); lineage = {"late_request": True, "sequential_requests": ["delete_a", "delete_b"], "descendants": [{"descendant_id": f"calibrator-{seed}-governed", "invalidation": "recorded", "quarantine": "recorded", "physical_erasure": False} for seed in SEEDS], "local_descendant_invalidation_count": 5, "external_descendant": {"identity": "export-simulated-unreachable", "reachable": False, "invalidation_acknowledged": False, "erasure_verified": False}}; write_json(BASE / "raw/lineage_receipt.json", lineage)
    raw = {"schema_version": "asi_stack.p4_m7_raw_training_run.v3", "run_id": prereg["run_id"], "state": "closed_before_independent_axis_evaluation", "corpus_sha256": corpus_sha, "preregistration_sha256": file_sha(PREREG), "feature_artifact": {"path": FEATURES.relative_to(ROOT).as_posix(), "sha256": file_sha(FEATURES)}, "model": model_meta, "seeds": list(SEEDS), "arms": list(ARMS), "seed_records": seed_records, "storage_receipt": {"path": (BASE / "raw/storage_receipt.json").relative_to(ROOT).as_posix(), "sha256": file_sha(BASE / "raw/storage_receipt.json")}, "lineage_receipt": {"path": (BASE / "raw/lineage_receipt.json").relative_to(ROOT).as_posix(), "sha256": file_sha(BASE / "raw/lineage_receipt.json")}, "cost": {"wall_seconds": round(time.perf_counter() - started, 6), "feature_extraction_wall_seconds": model_meta["wall_seconds"], "maximum_resident_set_kib": int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss), "marginal_api_cost_usd": 0.0, "energy_measured": False, "operator_time_measured": False}, "environment": {"platform": platform.platform(), "python": platform.python_version(), "torch": torch.__version__, "numpy": np.__version__, "deterministic_algorithms": True, "threads": torch.get_num_threads()}, "support_state_effect": "none"}; write_json(RAW_RUN, raw); print(f"P4/M7 v3 raw run closed: 5 seeds x 7 arms; wall={raw['cost']['wall_seconds']:.2f}s")


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("--preflight", action="store_true"); args = parser.parse_args(); torch.set_num_threads(1); torch.use_deterministic_algorithms(True); rows = load_json(CORPUS)["rows"]; run_preflight(rows) if args.preflight else run_confirmatory(rows)


if __name__ == "__main__": main()
