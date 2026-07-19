#!/usr/bin/env python3
"""Versioned paths and helpers for the diagnosed P4/M7 v2 repair."""

from __future__ import annotations

from pathlib import Path

from p4_m7_update_unlearning_common import *  # noqa: F401,F403


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "experiments" / "p4_update_unlearning_v2"
CORPUS = BASE / "corpus.json"
PREREG = BASE / "preregistration.json"
PREFLIGHT = BASE / "results" / "preflight_result.json"
RAW_RUN = BASE / "raw" / "training_run.json"
FEATURES = BASE / "raw" / "features.pt"
RESULT = BASE / "results" / "confirmatory_result.json"
V1_DIAGNOSIS = ROOT / "experiments" / "p4_update_unlearning" / "v1_failure_diagnosis.json"
