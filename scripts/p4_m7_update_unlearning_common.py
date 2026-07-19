#!/usr/bin/env python3
"""Shared frozen constants and byte-stable helpers for P4/M7."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from typing import Any

import torch
from torch import nn


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "experiments" / "p4_update_unlearning"
CORPUS = BASE / "corpus.json"
PREREG = BASE / "preregistration.json"
PREFLIGHT = BASE / "results" / "preflight_result.json"
RAW_RUN = BASE / "raw" / "training_run.json"
FEATURES = BASE / "raw" / "features.pt"
RESULT = BASE / "results" / "confirmatory_result.json"
MODEL_REPOSITORY = "Qwen/Qwen2.5-Coder-0.5B-Instruct"
MODEL_SNAPSHOT = "ea3f2471cf1b1f0db85067f1ef93848e38e88c25"
MODEL_CACHE = Path.home() / ".cache" / "huggingface" / "hub" / "models--Qwen--Qwen2.5-Coder-0.5B-Instruct" / "snapshots" / MODEL_SNAPSHOT
SEEDS = (1701, 2903, 4307, 6101, 7907)
ARMS = (
    "no_update",
    "standard_update",
    "governed_update",
    "regularized_forgetting_mitigation",
    "approximate_unlearning",
    "deletion_aware_retrain",
    "exact_rollback",
)
CLAIM_AXES = (
    "behavioral_cohort_change",
    "causal_influence_reduction",
    "membership_privacy_change",
    "lineage_invalidation",
    "legal_compliance",
    "storage_erasure",
    "backup_erasure",
    "external_descendant_closure",
)
STATE_SURFACES = (
    "model_parameters",
    "model_buffers",
    "optimizer_state",
    "scheduler_state",
    "accumulated_gradients",
    "python_rng",
    "numpy_rng",
    "torch_rng",
    "sampler_order",
    "dataset_and_splits",
    "tokenizer_preprocessor",
    "training_config",
    "code_revision",
    "environment",
    "best_checkpoint",
    "final_checkpoint",
    "released_checkpoint",
    "shadow_checkpoint",
    "rollback_checkpoint",
    "evaluator_and_policy",
    "inference_cache",
    "feature_cache",
    "lineage_index",
    "local_backup_store",
)


class ProbeHead(nn.Module):
    """Small auditable head over a frozen open-weight Transformer representation."""

    def __init__(self, hidden_size: int = 896, classes: int = 3) -> None:
        super().__init__()
        self.linear = nn.Linear(hidden_size, classes)

    def forward(self, values: torch.Tensor) -> torch.Tensor:
        return self.linear(values)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def canonical_sha(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def state_sha(state: dict[str, torch.Tensor]) -> str:
    digest = hashlib.sha256()
    for name in sorted(state):
        value = state[name].detach().cpu().contiguous()
        digest.update(name.encode("utf-8"))
        digest.update(str(value.dtype).encode("ascii"))
        digest.update(str(tuple(value.shape)).encode("ascii"))
        digest.update(value.numpy().tobytes())
    return digest.hexdigest()


def clone_state(model: nn.Module) -> dict[str, torch.Tensor]:
    return {name: value.detach().cpu().clone() for name, value in model.state_dict().items()}


def parameter_l2(left: dict[str, torch.Tensor], right: dict[str, torch.Tensor]) -> float:
    values = (
        difference * difference
        for name in sorted(left)
        for difference in (
            float(a) - float(b)
            for a, b in zip(left[name].reshape(-1).tolist(), right[name].reshape(-1).tolist())
        )
    )
    return math.sqrt(math.fsum(values))


def model_file_identities() -> dict[str, str]:
    names = ("config.json", "tokenizer.json", "tokenizer_config.json", "model.safetensors")
    if not MODEL_CACHE.is_dir():
        raise FileNotFoundError(f"required local model snapshot missing: {MODEL_CACHE}")
    return {name: file_sha(MODEL_CACHE / name) for name in names}
