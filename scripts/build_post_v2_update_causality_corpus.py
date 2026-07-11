#!/usr/bin/env python3
"""Build the deterministic 1,200-example update-causality corpus."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "experiments/post_v2_update_causality/input/corpus.json"


def main() -> None:
    rng = np.random.default_rng(20260710)
    features = rng.normal(size=(1200, 8)).astype(np.float32)
    score = features[:, 0] * features[:, 1] + 0.7 * features[:, 2] - 0.5 * features[:, 3] + 0.35 * np.sin(features[:, 4] * 2.0) + 0.2 * features[:, 5] ** 2
    labels = (score > 0).astype(int)
    examples = []
    for index, (row, label) in enumerate(zip(features, labels)):
        split = "train" if index < 720 else "validation" if index < 960 else "test"
        train_role = "base_train" if index < 480 else "update" if index < 720 else None
        deletion = 480 <= index < 540
        examples.append({
            "example_id": f"policy-{index:04d}",
            "split": split,
            "train_role": train_role,
            "features": [round(float(value), 7) for value in row],
            "true_label": int(label),
            "training_label": int(1 - label if deletion else label),
            "deletion_cohort": deletion,
            "fixed_probe": 960 <= index < 1000,
        })
    payload = {
        "schema_version": "asi_stack.post_v2_update_causality_corpus.v0",
        "corpus_id": "post-v2-update-causality-1200-2026-07-10",
        "generation_seed": 20260710,
        "frozen_before_update_outcomes": True,
        "split_counts": {"train": 720, "validation": 240, "test": 240},
        "train_role_counts": {"base_train": 480, "update": 240},
        "deletion_cohort_count": 60,
        "fixed_probe_count": 40,
        "campaign_contract": {
            "seeds": [17, 29, 43],
            "base_epochs": 40,
            "challenger_epochs": 12,
            "retrain_epochs": 40,
            "selection_split": "validation",
            "test_selection_forbidden": True,
            "arms": ["no_update", "bounded_finetune", "regularized_challenger", "deletion_aware_retrain"]
        },
        "examples": examples,
    }
    digest_payload = copy.deepcopy(payload)
    payload["corpus_sha256"] = hashlib.sha256(json.dumps(digest_payload, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)} with {len(examples)} examples")


if __name__ == "__main__":
    main()
