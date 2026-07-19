#!/usr/bin/env python3
"""Terminal v3 instrument constants for P4/M7."""

from __future__ import annotations

from pathlib import Path

import torch
from torch import nn

from p4_m7_update_unlearning_common import *  # noqa: F401,F403


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "experiments" / "p4_update_unlearning_v3"
CORPUS = ROOT / "experiments" / "p4_update_unlearning_v2" / "corpus.json"
PREREG = BASE / "preregistration.json"
PREFLIGHT = BASE / "results" / "preflight_result.json"
RAW_RUN = BASE / "raw" / "training_run.json"
FEATURES = BASE / "raw" / "features.pt"
RESULT = BASE / "results" / "confirmatory_result.json"
V1_DIAGNOSIS = ROOT / "experiments" / "p4_update_unlearning" / "v1_failure_diagnosis.json"
V2_DIAGNOSIS = ROOT / "experiments" / "p4_update_unlearning_v2" / "preflight_failure_diagnosis.json"
STRUCTURED_FIELDS = {
    "authority": ("valid", "delegated", "expired", "missing"),
    "provenance": ("verified", "partial", "unknown"),
    "contamination": ("clear", "suspected", "confirmed"),
    "deletion": ("none", "requested", "residual"),
    "risk": ("low", "medium", "high"),
}
STRUCTURED_SIZE = sum(len(values) for values in STRUCTURED_FIELDS.values())
FUSED_SIZE = 896 + STRUCTURED_SIZE


class FusionHead(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.layers = nn.Sequential(nn.Linear(FUSED_SIZE, 32), nn.Tanh(), nn.Linear(32, 3))

    def forward(self, values: torch.Tensor) -> torch.Tensor:
        return self.layers(values)


class StructuredHead(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.layers = nn.Sequential(nn.Linear(STRUCTURED_SIZE, 32), nn.Tanh(), nn.Linear(32, 3))

    def forward(self, values: torch.Tensor) -> torch.Tensor:
        return self.layers(values)


def structured_features(rows: list[dict]) -> torch.Tensor:
    vectors = []
    for row in rows:
        vector = []
        for field, values in STRUCTURED_FIELDS.items():
            vector.extend(1.0 if row["attributes"][field] == value else 0.0 for value in values)
        vectors.append(vector)
    return torch.tensor(vectors, dtype=torch.float32)
