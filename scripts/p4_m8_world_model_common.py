#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import math
import random
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "experiments/p4_situated_world_model"
STATES = ("nominal", "recoverable", "blocked")
ARMS = (
    "reactive_no_world_model",
    "transcript_memory",
    "ungoverned_predictive",
    "governed_world_model",
    "ablate_active_information",
    "ablate_intervention",
    "ablate_observation_belief_separation",
    "ablate_uncertainty",
    "ablate_consolidation",
    "ablate_quiescent_stabilization",
)
SEEDS = (1709, 2917, 4327, 6131, 7933)


def canonical_sha(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def sha(path: Path) -> str: return hashlib.sha256(path.read_bytes()).hexdigest()
def load(path: Path) -> Any: return json.loads(path.read_text(encoding="utf-8"))


def rng_for(*parts: object) -> random.Random:
    digest = hashlib.sha256("|".join(map(str, parts)).encode()).digest()
    return random.Random(int.from_bytes(digest[:8], "big"))


def sample(dist: dict[str, float], rng: random.Random) -> str:
    point = rng.random(); cumulative = 0.0
    for key, probability in dist.items():
        cumulative += probability
        if point <= cumulative: return key
    return next(reversed(dist))


def normalize(values: dict[str, float]) -> dict[str, float]:
    total = sum(values.values())
    return {key: value / total for key, value in values.items()} if total else {key: 1 / len(values) for key in values}


def entropy(values: dict[str, float]) -> float:
    return -sum(value * math.log(value, 2) for value in values.values() if value > 0)


def environment_configs() -> dict[str, dict]:
    return {
        "adaptive_workshop": {
            "environment_id": "adaptive_workshop",
            "environment_version": "1.0.0",
            "domain": "persistent machine-cell diagnosis",
            "entities": ["cell-A", "cell-B", "cell-C", "cell-D"],
            "terminal_actions": {"nominal": "continue_run", "recoverable": "recalibrate", "blocked": "isolate_and_service"},
            "transition": {
                "nominal": {"nominal": 0.78, "recoverable": 0.18, "blocked": 0.04},
                "recoverable": {"nominal": 0.25, "recoverable": 0.58, "blocked": 0.17},
                "blocked": {"nominal": 0.08, "recoverable": 0.27, "blocked": 0.65},
            },
            "probes": {
                "vibration": {
                    "nominal": {"smooth": 0.80, "rough": 0.15, "silent": 0.05},
                    "recoverable": {"smooth": 0.20, "rough": 0.65, "silent": 0.15},
                    "blocked": {"smooth": 0.05, "rough": 0.20, "silent": 0.75},
                },
                "thermal": {
                    "nominal": {"cool": 0.78, "warm": 0.18, "hot": 0.04},
                    "recoverable": {"cool": 0.18, "warm": 0.62, "hot": 0.20},
                    "blocked": {"cool": 0.04, "warm": 0.21, "hot": 0.75},
                },
                "alignment": {
                    "nominal": {"centered": 0.82, "offset": 0.14, "jammed": 0.04},
                    "recoverable": {"centered": 0.21, "offset": 0.63, "jammed": 0.16},
                    "blocked": {"centered": 0.05, "offset": 0.20, "jammed": 0.75},
                },
            },
            "shifted_probes": {
                "thermal": {
                    "nominal": {"cool": 0.48, "warm": 0.45, "hot": 0.07},
                    "recoverable": {"cool": 0.42, "warm": 0.45, "hot": 0.13},
                    "blocked": {"cool": 0.10, "warm": 0.32, "hot": 0.58},
                }
            },
            "intervention": {
                "action": "low_power_pulse",
                "responses": {
                    "nominal": {"stable": 0.88, "changed": 0.12},
                    "recoverable": {"stable": 0.25, "changed": 0.75},
                    "blocked": {"stable": 0.78, "changed": 0.22},
                },
                "cost": 0.12,
                "authority": "one reversible diagnostic pulse per episode"
            }
        },
        "service_mesh_transfer": {
            "environment_id": "service_mesh_transfer",
            "environment_version": "1.0.0",
            "domain": "persistent service dependency diagnosis",
            "entities": ["svc-auth", "svc-catalog", "svc-orders", "svc-search"],
            "terminal_actions": {"nominal": "keep_route", "recoverable": "refresh_local_state", "blocked": "isolate_dependency"},
            "transition": {
                "nominal": {"nominal": 0.74, "recoverable": 0.21, "blocked": 0.05},
                "recoverable": {"nominal": 0.28, "recoverable": 0.54, "blocked": 0.18},
                "blocked": {"nominal": 0.07, "recoverable": 0.25, "blocked": 0.68},
            },
            "probes": {
                "latency": {
                    "nominal": {"low": 0.76, "variable": 0.19, "timeout": 0.05},
                    "recoverable": {"low": 0.20, "variable": 0.62, "timeout": 0.18},
                    "blocked": {"low": 0.04, "variable": 0.20, "timeout": 0.76},
                },
                "trace": {
                    "nominal": {"clean": 0.79, "local_gap": 0.16, "upstream_gap": 0.05},
                    "recoverable": {"clean": 0.18, "local_gap": 0.65, "upstream_gap": 0.17},
                    "blocked": {"clean": 0.05, "local_gap": 0.18, "upstream_gap": 0.77},
                },
                "cache": {
                    "nominal": {"fresh": 0.82, "stale": 0.14, "missing": 0.04},
                    "recoverable": {"fresh": 0.22, "stale": 0.62, "missing": 0.16},
                    "blocked": {"fresh": 0.07, "stale": 0.22, "missing": 0.71},
                },
            },
            "shifted_probes": {
                "latency": {
                    "nominal": {"low": 0.48, "variable": 0.46, "timeout": 0.06},
                    "recoverable": {"low": 0.38, "variable": 0.47, "timeout": 0.15},
                    "blocked": {"low": 0.08, "variable": 0.30, "timeout": 0.62},
                }
            },
            "intervention": {
                "action": "bounded_canary_bypass",
                "responses": {
                    "nominal": {"improves": 0.12, "unchanged": 0.88},
                    "recoverable": {"improves": 0.72, "unchanged": 0.28},
                    "blocked": {"improves": 0.20, "unchanged": 0.80},
                },
                "cost": 0.15,
                "authority": "one disposable canary reroute per episode; no production mutation"
            }
        }
    }
