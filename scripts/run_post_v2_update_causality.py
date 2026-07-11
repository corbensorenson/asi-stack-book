#!/usr/bin/env python3
"""Execute the frozen real update-causality campaign."""
from __future__ import annotations

import argparse
import copy
import hashlib
import io
import json
import math
import platform
import time
from pathlib import Path

import numpy as np
import torch
from torch import nn


ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "experiments/post_v2_update_causality/input/corpus.json"
CHECKPOINTS = ROOT / "experiments/post_v2_update_causality/checkpoints"
RESULT = ROOT / "experiments/post_v2_update_causality/results/2026-07-10-local.json"
SEEDS = (17, 29, 43)
ARMS = ("no_update", "bounded_finetune", "regularized_challenger", "deletion_aware_retrain")


class PolicyNet(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.layers = nn.Sequential(nn.Linear(8, 12), nn.Tanh(), nn.Linear(12, 2))

    def forward(self, values: torch.Tensor) -> torch.Tensor:
        return self.layers(values)


def canonical_sha(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def state_sha(state: dict[str, torch.Tensor]) -> str:
    digest = hashlib.sha256()
    for name in sorted(state):
        array = state[name].detach().cpu().contiguous().numpy()
        digest.update(name.encode("utf-8")); digest.update(str(array.dtype).encode("ascii")); digest.update(str(array.shape).encode("ascii")); digest.update(array.tobytes())
    return digest.hexdigest()


def clone_state(model: nn.Module) -> dict[str, torch.Tensor]:
    return {name: value.detach().cpu().clone() for name, value in model.state_dict().items()}


def tensor_rows(rows: list[dict], label_key: str = "true_label") -> tuple[torch.Tensor, torch.Tensor]:
    return torch.tensor([row["features"] for row in rows], dtype=torch.float32), torch.tensor([row[label_key] for row in rows], dtype=torch.long)


def predictions(model: nn.Module, rows: list[dict]) -> list[int]:
    x, _ = tensor_rows(rows)
    model.eval()
    with torch.inference_mode():
        return model(x).argmax(dim=1).tolist()


def accuracy(preds: list[int], rows: list[dict], label_key: str = "true_label") -> float:
    return sum(pred == row[label_key] for pred, row in zip(preds, rows)) / len(rows)


def parameter_delta_l2(state: dict[str, torch.Tensor], base_state: dict[str, torch.Tensor]) -> float:
    """Compute a replay-stable norm from the stored float32 tensor values.

    Torch's parallel reduction kernels may accumulate the same tensor values in
    a different order across CPU architectures.  ``math.fsum`` over a fixed
    name/element order makes this recorded audit metric portable without
    changing the trained checkpoints or their output decisions.
    """
    squares = (
        difference * difference
        for name in sorted(state)
        for difference in (
            float(value) - float(base)
            for value, base in zip(
                state[name].detach().cpu().contiguous().view(-1).tolist(),
                base_state[name].detach().cpu().contiguous().view(-1).tolist(),
            )
        )
    )
    return math.sqrt(math.fsum(squares))


def train_model(model: PolicyNet, rows: list[dict], validation: list[dict], epochs: int, lr: float, base_state: dict[str, torch.Tensor] | None = None, regularization: float = 0.0) -> tuple[dict[str, torch.Tensor], dict[str, torch.Tensor], list[dict]]:
    x_train, y_train = tensor_rows(rows, "training_label")
    optimizer = torch.optim.SGD(model.parameters(), lr=lr)
    loss_fn = nn.CrossEntropyLoss()
    history = []
    best_state = clone_state(model)
    best_val = -1.0
    for epoch in range(1, epochs + 1):
        model.train(); optimizer.zero_grad(set_to_none=True)
        loss = loss_fn(model(x_train), y_train)
        if base_state is not None and regularization:
            penalty = sum((parameter - base_state[name].to(parameter.device)).pow(2).sum() for name, parameter in model.named_parameters())
            loss = loss + regularization * penalty
        loss.backward(); optimizer.step()
        val_preds = predictions(model, validation)
        val_accuracy = accuracy(val_preds, validation)
        history.append({"epoch": epoch, "train_loss": round(float(loss.detach()), 8), "validation_accuracy": round(val_accuracy, 8)})
        if val_accuracy > best_val:
            best_val = val_accuracy
            best_state = clone_state(model)
    return best_state, clone_state(model), history


def save_state(path: Path, state: dict[str, torch.Tensor]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(state, path)
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_state(path: Path) -> dict[str, torch.Tensor]:
    return torch.load(path, map_location="cpu", weights_only=True)


def evaluate_checkpoint(path: Path, rows: dict[str, list[dict]], base_state: dict[str, torch.Tensor], base_predictions: dict[str, list[int]]) -> dict:
    model = PolicyNet(); state = load_state(path); model.load_state_dict(state)
    output = {name: predictions(model, values) for name, values in rows.items()}
    delta = parameter_delta_l2(state, base_state)
    return {
        "state_sha256": state_sha(state),
        "parameter_delta_l2": round(delta, 10),
        "validation_accuracy": round(accuracy(output["validation"], rows["validation"]), 8),
        "test_accuracy": round(accuracy(output["test"], rows["test"]), 8),
        "retained_base_accuracy": round(accuracy(output["base_train"], rows["base_train"]), 8),
        "changed_test_decisions": sum(a != b for a, b in zip(output["test"], base_predictions["test"])),
        "fixed_probe_changes": sum(a != b for a, b in zip(output["probes"], base_predictions["probes"])),
        "deletion_cohort_changes": sum(a != b for a, b in zip(output["deletion"], base_predictions["deletion"])),
        "deletion_true_accuracy": round(accuracy(output["deletion"], rows["deletion"]), 8),
        "deletion_training_label_accuracy": round(accuracy(output["deletion"], rows["deletion"], "training_label"), 8),
        "nonmember_test_utility": round(accuracy(output["test"], rows["test"]), 8),
        "output_sha256": {name: canonical_sha(values) for name, values in output.items()},
    }


def refresh_existing_metrics() -> None:
    """Refresh portable derived metrics without retraining or replacing checkpoints."""
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    corpus = json.loads(CORPUS.read_text(encoding="utf-8"))
    examples = corpus["examples"]
    rows = {
        "base_train": [row for row in examples if row["train_role"] == "base_train"],
        "update": [row for row in examples if row["train_role"] == "update"],
        "deletion": [row for row in examples if row["deletion_cohort"]],
        "validation": [row for row in examples if row["split"] == "validation"],
        "test": [row for row in examples if row["split"] == "test"],
        "probes": [row for row in examples if row["fixed_probe"]],
    }
    for seed_row in result["seed_records"]:
        base = seed_row["base_checkpoint"]
        base_path = ROOT / base["path"]
        base_state = load_state(base_path)
        base_model = PolicyNet(); base_model.load_state_dict(base_state)
        base_predictions = {name: predictions(base_model, values) for name, values in rows.items()}
        base["test_accuracy"] = round(accuracy(base_predictions["test"], rows["test"]), 8)
        for arm in seed_row["arms"]:
            for checkpoint_name in ("best_checkpoint", "final_checkpoint"):
                checkpoint = arm[checkpoint_name]
                checkpoint["metrics"] = evaluate_checkpoint(
                    ROOT / checkpoint["path"], rows, base_state, base_predictions
                )
            best_model = PolicyNet(); best_model.load_state_dict(load_state(ROOT / arm["best_checkpoint"]["path"]))
            final_model = PolicyNet(); final_model.load_state_dict(load_state(ROOT / arm["final_checkpoint"]["path"]))
            arm["best_final_test_disagreement"] = sum(
                left != right
                for left, right in zip(
                    predictions(best_model, rows["test"]),
                    predictions(final_model, rows["test"]),
                )
            )
            arm["actual_parameter_mutation"] = arm["final_checkpoint"]["metrics"]["parameter_delta_l2"] > 0
    result["environment"]["parameter_delta_accumulator"] = "math.fsum_fixed_tensor_and_element_order"
    result.pop("bundle_sha256", None)
    result["bundle_sha256"] = canonical_sha(result)
    RESULT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"refreshed {RESULT.relative_to(ROOT)} bundle_sha256={result['bundle_sha256']}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--refresh-existing-metrics", action="store_true")
    args = parser.parse_args()
    if args.refresh_existing_metrics:
        if not RESULT.is_file():
            raise SystemExit(f"result does not exist: {RESULT.relative_to(ROOT)}")
        torch.set_num_threads(1); torch.use_deterministic_algorithms(True)
        refresh_existing_metrics()
        return
    if RESULT.exists() and not args.force:
        raise SystemExit(f"result already exists: {RESULT.relative_to(ROOT)}")
    torch.set_num_threads(1); torch.use_deterministic_algorithms(True)
    corpus = json.loads(CORPUS.read_text(encoding="utf-8"))
    examples = corpus["examples"]
    rows = {
        "base_train": [row for row in examples if row["train_role"] == "base_train"],
        "update": [row for row in examples if row["train_role"] == "update"],
        "deletion": [row for row in examples if row["deletion_cohort"]],
        "validation": [row for row in examples if row["split"] == "validation"],
        "test": [row for row in examples if row["split"] == "test"],
        "probes": [row for row in examples if row["fixed_probe"]],
    }
    started = time.perf_counter(); seed_records = []
    for seed in SEEDS:
        torch.manual_seed(seed); np.random.seed(seed)
        base_model = PolicyNet()
        base_best, base_final, base_history = train_model(base_model, rows["base_train"], rows["validation"], 40, 0.12)
        base_state = base_final
        base_path = CHECKPOINTS / f"seed-{seed}-base-final.pt"
        base_file_sha = save_state(base_path, base_state)
        base_loaded = PolicyNet(); base_loaded.load_state_dict(load_state(base_path))
        base_predictions = {name: predictions(base_loaded, values) for name, values in rows.items()}
        arms = []
        for arm in ARMS:
            if arm == "no_update":
                best_state = final_state = clone_state(base_loaded)
                history = []
            elif arm == "bounded_finetune":
                model = PolicyNet(); model.load_state_dict(base_state)
                best_state, final_state, history = train_model(model, rows["update"], rows["validation"], 12, 0.08)
            elif arm == "regularized_challenger":
                model = PolicyNet(); model.load_state_dict(base_state)
                best_state, final_state, history = train_model(model, rows["update"], rows["validation"], 12, 0.08, base_state, 0.02)
            else:
                torch.manual_seed(seed)
                model = PolicyNet()
                retained = rows["base_train"] + [row for row in rows["update"] if not row["deletion_cohort"]]
                best_state, final_state, history = train_model(model, retained, rows["validation"], 40, 0.12)
            best_path = CHECKPOINTS / f"seed-{seed}-{arm}-best.pt"
            final_path = CHECKPOINTS / f"seed-{seed}-{arm}-final.pt"
            best_file_sha = save_state(best_path, best_state); final_file_sha = save_state(final_path, final_state)
            best_metrics = evaluate_checkpoint(best_path, rows, base_state, base_predictions)
            final_metrics = evaluate_checkpoint(final_path, rows, base_state, base_predictions)
            best_model = PolicyNet(); best_model.load_state_dict(load_state(best_path))
            final_model = PolicyNet(); final_model.load_state_dict(load_state(final_path))
            best_final_disagreement = sum(a != b for a, b in zip(predictions(best_model, rows["test"]), predictions(final_model, rows["test"])))
            best_epoch = 0 if not history else max(history, key=lambda row: (row["validation_accuracy"], -row["epoch"]))["epoch"]
            arms.append({
                "arm": arm,
                "history": history,
                "best_epoch_selected_by_validation": best_epoch,
                "best_checkpoint": {"path": best_path.relative_to(ROOT).as_posix(), "file_sha256": best_file_sha, "metrics": best_metrics},
                "final_checkpoint": {"path": final_path.relative_to(ROOT).as_posix(), "file_sha256": final_file_sha, "metrics": final_metrics},
                "best_final_test_disagreement": best_final_disagreement,
                "actual_parameter_mutation": final_metrics["parameter_delta_l2"] > 0,
            })
        rollback = PolicyNet(); rollback.load_state_dict(load_state(base_path))
        rollback_state = clone_state(rollback)
        seed_records.append({
            "seed": seed,
            "base_checkpoint": {"path": base_path.relative_to(ROOT).as_posix(), "file_sha256": base_file_sha, "state_sha256": state_sha(base_state), "history": base_history, "test_accuracy": round(accuracy(base_predictions["test"], rows["test"]), 8)},
            "arms": arms,
            "rollback": {"target": "base_checkpoint", "state_sha256": state_sha(rollback_state), "exact": state_sha(rollback_state) == state_sha(base_state), "descendant_arms_invalidated": 3},
        })
    result = {
        "schema_version": "asi_stack.post_v2_update_causality_result.v0",
        "program_id": "real_update_causality_campaign",
        "recorded_date": "2026-07-10",
        "execution_state": "completed_exact_preregistered_campaign",
        "corpus_ref": CORPUS.relative_to(ROOT).as_posix(),
        "corpus_sha256": corpus["corpus_sha256"],
        "environment": {"platform": platform.platform(), "python": platform.python_version(), "torch": torch.__version__, "numpy": np.__version__, "deterministic_algorithms": True, "threads": 1},
        "seed_records": seed_records,
        "program_wall_seconds": round(time.perf_counter() - started, 6),
        "claim_dispositions": [
            {"claim_id": "data-engines-continual-learning-and-unlearning.core", "disposition": "no_change", "basis": "Real mutation, deletion-aware retraining, forgetting, and rollback are measured on a small synthetic policy network without production unlearning transfer."},
            {"claim_id": "policy-optimization-and-learning-from-feedback.core", "disposition": "no_change", "basis": "The campaign establishes bounded checkpoint/output causality but does not evaluate human or model feedback learning."},
            {"claim_id": "open-ended-improvement-engines.core", "disposition": "no_change", "basis": "A fixed four-arm stopped campaign is evidence about bounded update records, not open-ended improvement."},
            {"claim_id": "recursive-self-improvement-boundaries.core", "disposition": "no_change", "basis": "Rollback and descendant invalidation exercise only the transaction boundary and not recursive improvement."}
        ],
        "support_state_effect": "none",
        "non_claims": [
            "Parameter mutation is necessary but not sufficient evidence of useful learning.",
            "Deletion-aware retraining on a synthetic poisoned cohort is not proof of production unlearning or legal erasure.",
            "Validation-only checkpoint selection prevents test tuning but does not create external evaluator independence.",
            "Rollback digest equality does not prove deletion from storage outside the recorded checkpoint set.",
            "No chapter-core support state changes."
        ]
    }
    result["bundle_sha256"] = canonical_sha(result)
    RESULT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {RESULT.relative_to(ROOT)} bundle_sha256={result['bundle_sha256']}")


if __name__ == "__main__":
    main()
