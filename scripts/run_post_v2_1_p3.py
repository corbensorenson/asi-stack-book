#!/usr/bin/env python3
"""Execute P3 full-state update, checkpoint authority, and unlearning causality."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import pickle
import platform
import random
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import numpy as np
import torch
from torch import nn


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "experiments/post_v2_1_evidence_program"
CORPUS = BASE / "p3/input/corpus.json"
INVENTORY = BASE / "p3/state_inventory.json"
PREREG = BASE / "preregistration.json"
RESULT = BASE / "p3/results/result.json"
STATE_ROOT = BASE / "p3/artifacts/state"
MUTATED_ROOT = BASE / "p3/artifacts/mutated_state"
OBSERVER = ROOT / "scripts/post_v2_1_p3_observer.py"
SEEDS = (1701, 2903, 4307)
ARMS = ("bit_identical_no_update", "bounded_update", "ewc_forgetting_mitigation", "deletion_aware_retrain", "authorized_data_retrain_comparator")


class PolicyNet(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.layers = nn.Sequential(nn.Linear(3, 8), nn.Tanh(), nn.Linear(8, 2))

    def forward(self, values: torch.Tensor) -> torch.Tensor:
        return self.layers(values)


def canonical_sha(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tensor_sha(state: dict[str, torch.Tensor]) -> str:
    digest = hashlib.sha256()
    for name in sorted(state):
        value = state[name].detach().cpu().contiguous()
        digest.update(name.encode()); digest.update(str(value.dtype).encode()); digest.update(str(tuple(value.shape)).encode()); digest.update(value.numpy().tobytes())
    return digest.hexdigest()


def clone_state(model: nn.Module) -> dict[str, torch.Tensor]:
    return {name: value.detach().cpu().clone() for name, value in model.state_dict().items()}


def tensor_rows(rows: list[dict]) -> tuple[torch.Tensor, torch.Tensor]:
    return torch.tensor([row["features"] for row in rows], dtype=torch.float32), torch.tensor([row["label"] for row in rows], dtype=torch.long)


def accuracy(model: nn.Module, rows: list[dict]) -> float:
    if not rows:
        return 0.0
    x, y = tensor_rows(rows)
    model.eval()
    with torch.inference_mode():
        return float((model(x).argmax(dim=1) == y).float().mean())


def predictions(model: nn.Module, rows: list[dict]) -> list[int]:
    x, _ = tensor_rows(rows)
    model.eval()
    with torch.inference_mode():
        return model(x).argmax(dim=1).tolist()


def mean_true_confidence(model: nn.Module, rows: list[dict]) -> float:
    x, y = tensor_rows(rows)
    model.eval()
    with torch.inference_mode():
        probabilities = model(x).softmax(dim=1)
        return float(probabilities[torch.arange(len(y)), y].mean())


def split_rows(corpus: dict) -> dict[str, list[dict]]:
    rows = corpus["examples"]
    output = {split: [row for row in rows if row["split"] == split] for split in corpus["split_counts"]}
    output["initial"] = [row for row in rows if row["initial_training_member"]]
    output["authorized"] = [row for row in rows if row["split"] in {"train", "update"} and not row["deletion_member"]]
    output["retained_validation"] = [row for row in output["validation"] if row["family"] != "target_gamma"]
    output["target_validation"] = [row for row in output["validation"] if row["family"] == "target_gamma"]
    output["retained_test"] = [row for row in output["test"] if row["family"] != "target_gamma"]
    output["target_test"] = [row for row in output["test"] if row["family"] == "target_gamma"]
    return output


def train_base(seed: int, rows: dict[str, list[dict]]) -> tuple[PolicyNet, dict, dict, list[dict]]:
    torch.manual_seed(seed); np.random.seed(seed); random.seed(seed)
    model = PolicyNet(); optimizer = torch.optim.SGD(model.parameters(), lr=0.08, momentum=0.9)
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.7)
    x, y = tensor_rows(rows["initial"]); loss_fn = nn.CrossEntropyLoss(); history = []
    for epoch in range(1, 21):
        model.train(); optimizer.zero_grad(set_to_none=True); loss = loss_fn(model(x), y); loss.backward(); optimizer.step(); scheduler.step()
        history.append({"epoch": epoch, "loss": round(float(loss.detach()), 8), "validation": round(accuracy(model, rows["validation"]), 8)})
    return model, optimizer.state_dict(), scheduler.state_dict(), history


def run_arm(arm: str, seed: int, base_state: dict[str, torch.Tensor], base_retained_validation: float, rows: dict[str, list[dict]]) -> dict:
    torch.manual_seed(seed + 100); np.random.seed(seed + 100); random.seed(seed + 100)
    if arm == "authorized_data_retrain_comparator":
        model = PolicyNet()
    else:
        model = PolicyNet(); model.load_state_dict(base_state)
    optimizer = torch.optim.SGD(model.parameters(), lr=0.05, momentum=0.9)
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=4, gamma=0.7)
    training_rows = rows["update"]
    if arm in {"deletion_aware_retrain", "authorized_data_retrain_comparator"}:
        training_rows = rows["authorized"]
    x, y = tensor_rows(training_rows); loss_fn = nn.CrossEntropyLoss()
    checkpoints = []
    max_epochs = 0 if arm == "bit_identical_no_update" else 12
    if max_epochs == 0:
        checkpoints.append({"epoch": 0, "state": clone_state(model), "validation_target": accuracy(model, rows["target_validation"]), "validation_retained": accuracy(model, rows["retained_validation"]), "loss": None})
    stopped = None
    for epoch in range(1, max_epochs + 1):
        model.train(); optimizer.zero_grad(set_to_none=True); loss = loss_fn(model(x), y)
        if arm == "ewc_forgetting_mitigation":
            penalty = sum((parameter - base_state[name].to(parameter.device)).pow(2).sum() for name, parameter in model.named_parameters())
            loss = loss + 0.04 * penalty
        loss.backward(); optimizer.step(); scheduler.step()
        target = accuracy(model, rows["target_validation"]); retained = accuracy(model, rows["retained_validation"])
        checkpoints.append({"epoch": epoch, "state": clone_state(model), "validation_target": target, "validation_retained": retained, "loss": float(loss.detach())})
        if base_retained_validation - retained > 0.08:
            stopped = "retained_validation_regression_exceeded_0.08"; break
    eligible = [row for row in checkpoints if base_retained_validation - row["validation_retained"] <= 0.03]
    candidates = eligible or checkpoints
    authority = sorted(candidates, key=lambda row: (-row["validation_target"], -row["validation_retained"], row["epoch"], tensor_sha(row["state"])))[0]
    final = checkpoints[-1]
    return {
        "model": model, "optimizer": optimizer, "scheduler": scheduler,
        "checkpoints": checkpoints, "authority": authority, "final": final,
        "authority_eligible": authority in eligible, "stop_reason": stopped,
    }


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(value, sort_keys=True, indent=2) + "\n")


def create_surface_root(root: Path, seed: int, arm: str, model_state: dict[str, torch.Tensor], optimizer_state: dict, scheduler_state: dict, corpus: dict, training_ids: list[str], authority_state: dict[str, torch.Tensor], final_state: dict[str, torch.Tensor], rollback_state: dict[str, torch.Tensor]) -> Path:
    if root.exists(): shutil.rmtree(root)
    root.mkdir(parents=True)
    mapping = {
        "model_parameters": "checkpoints/model.pt", "model_buffers": "checkpoints/buffers.pt",
        "optimizer_state": "runtime/optimizer.pt", "scheduler_state": "runtime/scheduler.pt",
        "accumulated_gradients": "runtime/gradients.json", "python_rng": "rng/python.pkl",
        "numpy_rng": "rng/numpy.pkl", "torch_cpu_rng": "rng/torch.pt", "sampler_order": "runtime/sampler.json",
        "dataset_and_splits": "config/dataset.json", "tokenizer_preprocessor": "config/preprocessor.json",
        "training_config": "config/training.json", "code_revision": "config/code.json", "environment": "config/environment.json",
        "best_checkpoint": "checkpoints/best.pt", "final_checkpoint": "checkpoints/final.pt",
        "released_checkpoint": "checkpoints/released.pt", "shadow_checkpoint": "checkpoints/shadow.json",
        "rollback_checkpoint": "checkpoints/rollback.pt", "evaluator_and_policy": "config/evaluator.json",
        "inference_cache": "caches/inference", "feature_cache": "caches/features", "lineage_index": "lineage/index.json",
        "local_backup_store": "backups/local",
    }
    write_json(root / "surface_map.json", {"surfaces": mapping})
    for relative in ("checkpoints", "runtime", "rng", "config", "caches/inference", "caches/features", "lineage", "backups/local"):
        (root / relative).mkdir(parents=True, exist_ok=True)
    torch.save(model_state, root / mapping["model_parameters"]); torch.save({}, root / mapping["model_buffers"])
    torch.save(optimizer_state, root / mapping["optimizer_state"]); torch.save(scheduler_state, root / mapping["scheduler_state"])
    write_json(root / mapping["accumulated_gradients"], {"state": "cleared_after_step"})
    (root / mapping["python_rng"]).write_bytes(pickle.dumps(random.getstate()))
    (root / mapping["numpy_rng"]).write_bytes(pickle.dumps(np.random.get_state()))
    torch.save(torch.get_rng_state(), root / mapping["torch_cpu_rng"])
    write_json(root / mapping["sampler_order"], {"seed": seed, "ordered_training_ids_sha256": canonical_sha(training_ids)})
    write_json(root / mapping["dataset_and_splits"], {"corpus_sha256": corpus["content_sha256"], "training_ids": training_ids})
    write_json(root / mapping["tokenizer_preprocessor"], {"type": "identity_float32_three_feature"})
    write_json(root / mapping["training_config"], {"seed": seed, "arm": arm, "max_epochs": 12, "dtype": "float32"})
    commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True, check=True).stdout.strip()
    write_json(root / mapping["code_revision"], {"commit": commit, "runner_sha256": file_sha(Path(__file__))})
    write_json(root / mapping["environment"], {"python": platform.python_version(), "torch": torch.__version__, "numpy": np.__version__, "platform": platform.platform(), "threads": 1})
    torch.save(authority_state, root / mapping["best_checkpoint"]); torch.save(final_state, root / mapping["final_checkpoint"])
    torch.save(authority_state, root / mapping["released_checkpoint"]); write_json(root / mapping["shadow_checkpoint"], {"state": "none"})
    torch.save(rollback_state, root / mapping["rollback_checkpoint"])
    write_json(root / mapping["evaluator_and_policy"], {"authority": "validation target subject to retained regression <=0.03", "test_selects": False})
    write_json(root / mapping["lineage_index"], {"seed": seed, "arm": arm, "base": "rollback_checkpoint", "descendants": ["best", "final", "released"]})
    write_json(root / mapping["local_backup_store"] / "receipt.json", {"state": "local_disposable_only", "remote_copies": 0})
    return root / "surface_map.json"


def observe(state_root: Path) -> dict:
    process = subprocess.run([
        sys.executable, OBSERVER.as_posix(), "--inventory", INVENTORY.as_posix(),
        "--surface-map", (state_root / "surface_map.json").as_posix(), "--state-root", state_root.as_posix(),
    ], text=True, capture_output=True, timeout=30)
    if process.returncode: raise RuntimeError(f"P3 observer failed: {process.stderr[-1000:]}")
    return json.loads(process.stdout)


def evaluate_authority(model_state: dict[str, torch.Tensor], base_model: PolicyNet, rows: dict[str, list[dict]]) -> dict:
    model = PolicyNet(); model.load_state_dict(model_state)
    base_test = predictions(base_model, rows["test"]); current_test = predictions(model, rows["test"])
    return {
        "target_test_utility": round(accuracy(model, rows["target_test"]), 8),
        "retained_test_utility": round(accuracy(model, rows["retained_test"]), 8),
        "worst_family_test_utility": round(min(accuracy(model, [row for row in rows["test"] if row["family"] == family]) for family in sorted({row["family"] for row in rows["test"]})), 8),
        "changed_test_decisions": sum(left != right for left, right in zip(base_test, current_test)),
        "deletion_behavior_changes": sum(left != right for left, right in zip(predictions(base_model, rows["deletion"]), predictions(model, rows["deletion"]))),
        "deletion_true_confidence": round(mean_true_confidence(model, rows["deletion"]), 8),
        "probe_changes": sum(left != right for left, right in zip(predictions(base_model, rows["probe"]), predictions(model, rows["probe"]))),
        "test_prediction_sha256": canonical_sha(current_test),
    }


def preflight() -> None:
    corpus = json.loads(CORPUS.read_text()); seed = SEEDS[0]; model = PolicyNet(); state = clone_state(model)
    with tempfile.TemporaryDirectory(prefix="asi-p3-preflight-") as temp:
        root = Path(temp) / "state"
        create_surface_root(root, seed, "preflight", state, {}, {}, corpus, [], state, state, state)
        observation = observe(root)
        if not observation["complete_mapping"] or observation["surface_count"] != 24:
            raise SystemExit("P3 observer preflight lacks complete mapping")
    print("P3 preflight passed without training or held-out execution.")


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("--preflight", action="store_true"); args = parser.parse_args()
    if args.preflight: preflight(); return
    if json.loads(PREREG.read_text())["state"] != "frozen_before_outcome_runs": raise SystemExit("final preregistration is not frozen")
    if RESULT.exists(): raise SystemExit(f"result exists: {RESULT.relative_to(ROOT)}")
    torch.set_num_threads(1); torch.use_deterministic_algorithms(True)
    corpus = json.loads(CORPUS.read_text()); rows = split_rows(corpus); seed_records = []; started = time.perf_counter()
    for seed in SEEDS:
        base_model, base_optimizer, base_scheduler, base_history = train_base(seed, rows)
        base_state = clone_state(base_model); base_retained_validation = accuracy(base_model, rows["retained_validation"])
        base_root = STATE_ROOT / f"seed-{seed}" / "base"
        create_surface_root(base_root, seed, "base", base_state, base_optimizer, base_scheduler, corpus, [row["example_id"] for row in rows["initial"]], base_state, base_state, base_state)
        base_observation = observe(base_root); arms = []
        for arm in ARMS:
            arm_run = run_arm(arm, seed, base_state, base_retained_validation, rows)
            authority, final = arm_run["authority"], arm_run["final"]
            arm_root = STATE_ROOT / f"seed-{seed}" / arm
            training_rows = rows["authorized"] if arm in {"deletion_aware_retrain", "authorized_data_retrain_comparator"} else rows["update"]
            if arm == "bit_identical_no_update": training_rows = rows["initial"]
            if arm == "bit_identical_no_update":
                if arm_root.exists(): shutil.rmtree(arm_root)
                shutil.copytree(base_root, arm_root)
            else:
                create_surface_root(arm_root, seed, arm, clone_state(arm_run["model"]), arm_run["optimizer"].state_dict(), arm_run["scheduler"].state_dict(), corpus, [row["example_id"] for row in training_rows], authority["state"], final["state"], base_state)
            mutated_observation = observe(arm_root)
            preserved = MUTATED_ROOT / f"seed-{seed}" / arm
            if preserved.exists(): shutil.rmtree(preserved)
            preserved.parent.mkdir(parents=True, exist_ok=True); shutil.copytree(arm_root, preserved)
            shutil.rmtree(arm_root); shutil.copytree(base_root, arm_root)
            rollback_observation = observe(arm_root)
            authority_metrics = evaluate_authority(authority["state"], base_model, rows)
            final_metrics = evaluate_authority(final["state"], base_model, rows)
            arms.append({
                "arm": arm, "epochs_completed": len(arm_run["checkpoints"]) - (1 if arm == "bit_identical_no_update" else 0),
                "stop_reason": arm_run["stop_reason"], "authority_epoch": authority["epoch"],
                "authority_eligible": arm_run["authority_eligible"], "authority_validation_target": round(authority["validation_target"], 8),
                "authority_validation_retained": round(authority["validation_retained"], 8), "final_epoch": final["epoch"],
                "best_final_state_disagreement": tensor_sha(authority["state"]) != tensor_sha(final["state"]),
                "authority_state_sha256": tensor_sha(authority["state"]), "final_state_sha256": tensor_sha(final["state"]),
                "authority_metrics": authority_metrics, "final_metrics": final_metrics,
                "full_state_before_sha256": base_observation["observation_sha256"],
                "full_state_mutated_sha256": mutated_observation["observation_sha256"],
                "full_state_rollback_sha256": rollback_observation["observation_sha256"],
                "full_state_rollback_exact": rollback_observation["observation_sha256"] == base_observation["observation_sha256"],
                "state_surface_count": rollback_observation["surface_count"],
                "lineage_descendants_invalidated": 3 if arm != "bit_identical_no_update" else 0,
                "unlearning_claims": {
                    "behavioral_cohort_change": authority_metrics["deletion_behavior_changes"],
                    "influence_reduction": "not_established_true-confidence-proxy_only",
                    "lineage_propagation": arm in {"deletion_aware_retrain", "authorized_data_retrain_comparator"},
                    "storage_erasure": False,
                    "storage_boundary": "immutable public-safe source corpus retained; no legal/privacy erasure claim",
                },
                "preserved_mutated_state": preserved.relative_to(ROOT).as_posix(),
            })
            print(f"P3 seed={seed} arm={arm} complete", flush=True)
        seed_records.append({
            "seed": seed, "base_history": base_history, "base_state_sha256": tensor_sha(base_state),
            "base_validation_retained": round(base_retained_validation, 8), "base_test": round(accuracy(base_model, rows["test"]), 8),
            "base_full_state_sha256": base_observation["observation_sha256"], "arms": arms,
        })
    result = {
        "schema_version": "asi_stack.post_v2_1_p3_result.v0", "corpus_sha256": corpus["content_sha256"],
        "inventory_sha256": json.loads(INVENTORY.read_text())["content_sha256"], "seeds": list(SEEDS), "arms": list(ARMS),
        "environment": {"platform": platform.platform(), "python": platform.python_version(), "torch": torch.__version__, "numpy": np.__version__, "threads": 1, "deterministic_algorithms": True},
        "seed_records": seed_records, "wall_seconds": round(time.perf_counter() - started, 6),
        "support_state_effect": "none_pending_disposition",
        "non_claims": ["The synthetic policy network does not establish language-model unlearning.", "Behavioral change does not establish influence reduction or storage erasure.", "Exact rollback is bounded to the 24 declared local disposable surfaces.", "Internal process separation is not external independence."],
    }
    result["bundle_sha256"] = canonical_sha(result); RESULT.parent.mkdir(parents=True, exist_ok=True); RESULT.write_text(json.dumps(result, indent=2) + "\n")
    print(f"wrote {RESULT.relative_to(ROOT)} bundle_sha256={result['bundle_sha256']}")


if __name__ == "__main__":
    main()
