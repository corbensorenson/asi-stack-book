#!/usr/bin/env python3
"""Replay two rollout policies over frozen, synthetic verifier cases."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT = ROOT / "experiments/verifier_replacement_comparison"
CASES = EXPERIMENT / "model_cases.json"
LOCK = EXPERIMENT / "input_lock.json"
SCOPES = ("public-copy", "record-change")
ARMS = ("conventional", "bound_handoff")
LABELS = ("review", "clear")
KEYS = ("regression", "approval", "monitor", "fallback", "reviewer")
CANDIDATE = "verifier-v2"
PRIOR = "verifier-v1"
DEPLOYMENT = "clearance-policy-v1"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def tokens(request: str) -> list[str]:
    return re.findall(r"[a-z]+", request.lower())


class Verifier:
    def __init__(self, training: dict[str, list[str]]) -> None:
        self.counts = {
            label: Counter(token for example in training[label] for token in tokens(example))
            for label in LABELS
        }
        vocabulary = set().union(*(set(count) for count in self.counts.values()))
        self.vocabulary = vocabulary
        self.totals = {label: sum(self.counts[label].values()) for label in LABELS}
        self.log_priors = {
            label: math.log(len(training[label]) / sum(map(len, training.values())))
            for label in LABELS
        }

    def predict(self, request: str) -> str:
        known = [token for token in tokens(request) if token in self.vocabulary]
        return max(LABELS, key=lambda label: self.log_priors[label] + sum(
            math.log((1 + self.counts[label][token]) / (self.totals[label] + len(self.vocabulary)))
            for token in known
        ))


def evaluate_models(design: dict) -> dict:
    training = design["prior_training"]
    prior = Verifier(training)
    candidate = Verifier({
        label: training[label] + design["update_training"][label] for label in LABELS
    })
    observations = {}
    for scope in SCOPES:
        records = [
            {"case": name, "prior": prior.predict(request), "candidate": candidate.predict(request), "label": label}
            for name, request, label in design["evaluation"][scope]
        ]
        negative_flips = [
            row["case"] for row in records
            if row["prior"] == row["label"] and row["candidate"] != row["label"]
        ]
        observations[scope] = {
            "cases": len(records),
            "prior_correct": sum(row["prior"] == row["label"] for row in records),
            "candidate_correct": sum(row["candidate"] == row["label"] for row in records),
            "negative_flips": negative_flips,
            "protected_negative_flips": [
                row["case"] for row in records
                if scope == "record-change" and row["case"] in negative_flips and row["label"] == "review"
            ],
            "paired_decisions": records,
        }
    return observations


def observed_documents(scope: str, condition: str, tick: int, result: dict) -> dict[str, dict]:
    common = {"scope": scope, "deployment": DEPLOYMENT, "target": CANDIDATE, "valid_through": 1}
    records = {
        "regression": {**common, **{key: result[key] for key in (
            "cases", "prior_correct", "candidate_correct", "protected_negative_flips"
        )}},
        "approval": {**common, "authority": "release-owner"},
        "monitor": {**common, "available": True},
        "fallback": {**common, "target": PRIOR, "qualified": True},
        "reviewer": {
            **common, "owns_candidate": condition == "self_review",
            "qualification_source": "candidate" if condition == "self_review" else "independent",
            "verifier_changes": condition in {"self_review", "independent_review"},
        },
    }
    if condition == "stale_approval":
        records["approval"]["valid_through"] = -1
    if condition == "wrong_monitor":
        records["monitor"]["target"] = "verifier-control"
    if condition == "fallback_expired":
        records["fallback"]["valid_through"] = -1
    if condition == "monitor_recovers" and tick == 0:
        records["monitor"]["available"] = False
    return records


def qualifies(records: dict, scope: str, tick: int) -> tuple[str, list[str]]:
    def current(key: str, target: str) -> bool:
        row = records[key]
        return (
            (row["scope"], row["deployment"], row["target"]) == (scope, DEPLOYMENT, target)
            and tick <= row["valid_through"]
        )

    regression = records["regression"]
    reviewer = records["reviewer"]
    regression_passed = (
        current("regression", CANDIDATE)
        and regression["cases"] > 0
        and regression["candidate_correct"] >= regression["prior_correct"]
        and not regression["protected_negative_flips"]
    )
    fallback_ready = current("fallback", PRIOR) and records["fallback"]["qualified"]
    checks = {
        "paired regression": regression_passed,
        "target approval": current("approval", CANDIDATE) and records["approval"]["authority"] == "release-owner",
        "current monitor": current("monitor", CANDIDATE) and records["monitor"]["available"],
        "qualified fallback": fallback_ready,
        "review authority": current("reviewer", CANDIDATE) and (
            not reviewer["verifier_changes"]
            or (not reviewer["owns_candidate"] and reviewer["qualification_source"] == "independent")
        ),
    }
    gaps = [name for name, ready in checks.items() if not ready]
    if gaps:
        return ("prior" if fallback_ready else "specialist"), gaps
    return "candidate", gaps


def replay(scope: str, condition: str, arm: str, observations: dict) -> list[dict]:
    receipts = []
    stored = None
    for tick in range(2):
        docs = observed_documents(scope, condition, tick, observations)
        revision = digest(canonical(docs))
        cache_hit = (
            arm == "bound_handoff" and stored is not None
            and revision == stored["revision"] and tick <= stored["valid_through"]
        )
        if cache_hit:
            route, gaps = stored["route"], stored["gaps"]
        else:
            resolved = {key: docs[key] for key in KEYS}
            route, gaps = qualifies(resolved, scope, tick)
            if arm == "bound_handoff":
                deadlines = [row["valid_through"] for row in resolved.values() if tick <= row["valid_through"]]
                stored = {
                    "revision": revision, "valid_through": min(deadlines, default=tick),
                    "route": route, "gaps": gaps,
                }
        receipts.append({
            "tick": tick,
            "decision": "promote" if route == "candidate" else "hold",
            "route": route,
            "gaps": gaps,
            "evidence_sha256": revision,
            "revision_index_reads": 1,
            "evidence_document_reads": 0 if cache_hit else len(KEYS),
            "policy_evaluations": int(not cache_hit),
            "handoff_writes": int(arm == "bound_handoff" and not cache_hit),
        })
    return receipts


def main() -> None:
    frozen = json.loads(LOCK.read_text())
    inputs = (EXPERIMENT / "protocol.md", CASES, Path(__file__).resolve())
    actual = {str(path.relative_to(ROOT)): digest(path.read_bytes()) for path in inputs}
    if actual != frozen:
        raise ValueError("verifier comparison refuses altered frozen inputs")

    design = json.loads(CASES.read_text())
    model_results = evaluate_models(design)
    pairs = []
    metrics = (
        "wrong_promotion", "wrong_hold", "wrong_route", "revision_index_reads",
        "evidence_document_reads", "policy_evaluations", "handoff_writes",
    )
    summary = {arm: {metric: 0 for metric in metrics} for arm in ARMS}
    for scope in SCOPES:
        for name, (condition, public, protected, on_hold) in design["profiles"].items():
            gold = public if scope == "public-copy" else protected
            expected = ["candidate" if decision == "promote" else on_hold[tick] for tick, decision in enumerate(gold)]
            arms = {arm: replay(scope, condition, arm, model_results[scope]) for arm in ARMS}
            for arm, receipts in arms.items():
                for result, target in zip(receipts, expected, strict=True):
                    result["wrong_promotion"] = int(result["route"] == "candidate" and target != "candidate")
                    result["wrong_hold"] = int(result["route"] != "candidate" and target == "candidate")
                    result["wrong_route"] = int(result["route"] != target)
                    for metric in metrics:
                        summary[arm][metric] += result[metric]
            pairs.append({"scope": scope, "profile": name, "expected_routes": expected, "arms": arms})

    observed = {(row["scope"], row["profile"]): row["arms"]["conventional"] for row in pairs}
    checks = {
        "clean_public_promotion": observed[("public-copy", "current")][0]["route"] == "candidate",
        "protected_regression_observed": bool(model_results["record-change"]["protected_negative_flips"]),
        "fresh_monitor_recovers": [row["route"] for row in observed[("public-copy", "monitor_recovers")]] == ["prior", "candidate"],
        "expired_fallback_uses_specialist": observed[("public-copy", "fallback_expired")][0]["route"] == "specialist",
    }
    result = {
        "frozen_inputs": frozen, "calibration": checks, "model_results": model_results,
        "paired_checkpoints": sum(len(row["expected_routes"]) for row in pairs),
        "effort_scope": "scripted reads, evaluations and writes only; no human effort measured",
        "summary": summary, "pairs": pairs,
    }
    print(json.dumps(result, indent=2))
    if not all(checks.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
