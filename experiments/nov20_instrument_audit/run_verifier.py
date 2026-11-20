#!/usr/bin/env python3
"""Compare equally capable cache policies with absolute and provenance gates."""

from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
import json
from pathlib import Path
import sys
from time import process_time_ns

from locked import HERE, ROOT, check

sys.path.insert(0, str(ROOT / "scripts"))
from compare_verifier_replacements import CASES, canonical, digest, evaluate_models


ARMS = ("conventional_memoization", "retained_qualification")
CONSUMERS = ("release-check", "serving-check")
SOURCES = {"reviewer-a": "dashboard", "reviewer-b": "dashboard", "direct-check": "source-artifact"}


def instruments(profile, models):
    scope = "record-change" if profile == "record-change-negative-flips" else "public-copy"
    paired = deepcopy(models[scope]["paired_decisions"])
    if profile not in ("copy-09-shared-miss", "record-change-negative-flips"):
        # Positive instrument control. These are stipulated observations,
        # not a claim about a newly trained model or edited model predictions.
        for row in paired:
            row["prior"] = row["candidate"] = row["label"]
    if profile == "missing-must-pass":
        paired = [row for row in paired if row["case"] != "copy-09"]

    # The dashboard is intentionally blind to one planted field in the two
    # adverse review fixtures. The direct path inspects a separate input.
    artifact_fields = {"title"} if profile == "separate-observers-agree" else {"title", "private_name"}
    cached_dashboard = {"title"}
    agreement = [dict(source="reviewer-a", observed="clear" if "private_name" not in cached_dashboard else "hold")]
    if profile == "shared-dashboard-agreement":
        agreement.append(dict(source="reviewer-b", observed="clear" if "private_name" not in cached_dashboard else "hold"))
    elif profile in ("separate-observer-disagrees", "separate-observers-agree"):
        agreement.append(dict(source="direct-check", observed="hold" if "private_name" in artifact_fields else "clear"))

    expiry = 0 if profile == "fallback-expires" else 2
    review_required = profile.startswith(("shared-dashboard", "separate-observer"))
    return scope, {
        "regression": paired,
        "approval": {"scope": scope, "target": "candidate", "allowed": True},
        "monitor": {"scope": scope, "target": "candidate", "available": True},
        "fallback": {"scope": scope, "target": "prior", "valid_through": expiry},
        "review": {"required": review_required, "witnesses": agreement},
    }


def choose(documents, scope, required, tick):
    trial = documents["regression"]
    by_case = {row["case"]: row for row in trial}
    reasons = []
    candidate_fails = [name for name in required if name not in by_case
                       or by_case[name]["candidate"] != by_case[name]["label"]]
    prior_fails = [name for name in required if name not in by_case
                   or by_case[name]["prior"] != by_case[name]["label"]]
    if candidate_fails:
        reasons.append("candidate must-pass: " + ", ".join(candidate_fails))
    if not trial or sum(row["candidate"] == row["label"] for row in trial) < sum(
        row["prior"] == row["label"] for row in trial
    ):
        reasons.append("relative regression")
    approval = documents["approval"]
    if (approval["scope"], approval["target"], approval["allowed"]) != (scope, "candidate", True):
        reasons.append("approval")
    monitor = documents["monitor"]
    if (monitor["scope"], monitor["target"], monitor["available"]) != (scope, "candidate", True):
        reasons.append("monitor")
    review = documents["review"]
    if review["required"]:
        roots = {SOURCES[row["source"]] for row in review["witnesses"] if row["source"] in SOURCES}
        if len(roots) < 2:
            reasons.append("shared observation source")
        if any(row["observed"] != "clear" or row["source"] not in SOURCES for row in review["witnesses"]):
            reasons.append("review observations disagree or lack provenance")
    fallback = documents["fallback"]
    prior_ready = (fallback["scope"], fallback["target"]) == (scope, "prior") and (
        tick <= fallback["valid_through"] and not prior_fails
    )
    if not prior_ready:
        reasons.append("fallback unavailable or below must-pass floor")
    route = ("prior" if prior_ready else "specialist") if reasons else "candidate"
    return {"route": route, "reasons": reasons, "valid_through": max(tick, fallback["valid_through"])}


class EvidenceStore:
    """Immutable serialized documents plus an authoritative revision index."""

    def __init__(self):
        self.data = {}
        self.hashes = {}
        self.revision = ""

    def publish(self, updates, work):
        for name, value in updates.items():
            encoded = canonical(value)
            self.data[name] = encoded
            self.hashes[name] = digest(encoded)
            work["documents_constructed"] += 1
            work["document_bytes_serialized"] += len(encoded)
            work["document_hashes"] += 1
            work["document_bytes_hashed"] += len(encoded)
        index = canonical(self.hashes)
        self.revision = digest(index)
        work["index_hashes"] += 1
        work["index_bytes_hashed"] += len(index)

    def read(self, work):
        work["document_reads"] += len(self.data)
        return {name: json.loads(data) for name, data in self.data.items()}


def simulate(profile, mode, expected, models, must_pass):
    start = process_time_ns()
    scope, initial = instruments(profile, models)
    store = EvidenceStore()
    work = Counter()
    store.publish(initial, work)
    setup_ns = process_time_ns() - start
    decisions = []
    cache = None
    update_ns = lookup_ns = 0
    for tick in range(3):
        if tick == 1 and profile.startswith("update-"):
            timer = process_time_ns()
            store.publish({"approval": {**initial["approval"], "allowed": False}}, work)
            if profile == "update-notified":
                cache = None
                work["notification_invalidations"] += 1
            update_ns += process_time_ns() - timer

        for consumer in CONSUMERS:
            timer = process_time_ns()
            work["index_reads"] += 1
            revision = None if profile == "revision-index-unavailable" and tick == 1 else store.revision
            previous = json.loads(cache) if isinstance(cache, bytes) else cache
            if revision is None:
                route = {"route": "specialist", "reasons": ["revision index unavailable"]}
            else:
                changed = previous is not None and previous["revision"] != revision
                expired = previous is not None and tick > previous["valid_through"]
                if changed:
                    work["missed_update_recoveries"] += 1
                if expired:
                    work["expiry_invalidations"] += 1
                if previous is None or changed or expired:
                    packet = choose(store.read(work), scope, must_pass[scope], tick)
                    packet["revision"] = revision
                    work["policy_evaluations"] += 1
                    work["cache_writes"] += 1
                    cache = canonical(packet) if mode == "retained_qualification" else packet
                    if isinstance(cache, bytes):
                        work["handoff_bytes_serialized"] += len(cache)
                    route = packet
                else:
                    route = previous
            decisions.append({"tick": tick, "consumer": consumer, "expected": expected[tick],
                              "route": route["route"], "reasons": route["reasons"], "revision": revision})
            lookup_ns += process_time_ns() - timer

    wrong = sum(row["route"] != row["expected"] for row in decisions)
    return {"scope": scope, "decisions": decisions, "wrong_routes": wrong, "work": dict(sorted(work.items())),
            "review_witnesses": initial["review"]["witnesses"]}, {
                "setup_cpu_ns": setup_ns, "update_cpu_ns": update_ns, "lookup_cpu_ns": lookup_ns,
            }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timings", type=Path)
    args = parser.parse_args()
    frozen = check()
    fixture = json.loads((HERE / "verifier_profiles.json").read_bytes())
    models = evaluate_models(json.loads(CASES.read_bytes()))
    shared = next(row for row in models["public-copy"]["paired_decisions"] if row["case"] == "copy-09")
    cases = []
    times = []
    for profile, expected in fixture["profiles"].items():
        arms = {}
        for arm in ARMS:
            result, timing = simulate(profile, arm, expected, models, fixture["must_pass"])
            arms[arm] = result
            times.append({"profile": profile, "arm": arm, **timing})
        cases.append({"id": profile, "scope": arms[ARMS[0]]["scope"], "arms": arms})
    def arms_for(profile):
        return next(row["arms"] for row in cases if row["id"] == profile)
    calibration = {
        "retained_copy09_shared_failure": shared["prior"] == shared["candidate"] != shared["label"],
        "declared_routes": not any(a["wrong_routes"] for row in cases for a in row["arms"].values()),
        "missed_invalidation_detected": all(a["work"]["missed_update_recoveries"] == 1
                                             for a in arms_for("update-notification-missed").values()),
        "notified_invalidation_detected": all(a["work"]["notification_invalidations"] == 1
                                             for a in arms_for("update-notified").values()),
        "agreeing_mirrors_share_dependency": all("shared observation source" in a["decisions"][0]["reasons"]
                                                for a in arms_for("shared-dashboard-agreement").values()),
        "direct_observation_disputes_dashboard": all("review observations disagree or lack provenance" in a["decisions"][0]["reasons"]
                                                    for a in arms_for("separate-observer-disagrees").values()),
    }
    if not all(calibration.values()):
        wrong = [(row["id"], name, [(d["tick"], d["route"], d["expected"]) for d in a["decisions"]
                                  if d["route"] != d["expected"]])
                 for row in cases for name, a in row["arms"].items() if a["wrong_routes"]]
        raise ValueError(f"verifier controls did not match: {calibration}, {wrong}")
    totals = {}
    for arm in ARMS:
        rows = [row["arms"][arm] for row in cases]
        counts = Counter()
        for row in rows:
            counts.update(row["work"])
        totals[arm] = {"wrong_routes": sum(row["wrong_routes"] for row in rows), **dict(sorted(counts.items()))}
    if args.timings:
        args.timings.write_text(json.dumps({"profiles": times}, indent=2) + "\n")
    print(json.dumps({"frozen_inputs": frozen, "calibration": calibration, "must_pass": fixture["must_pass"],
                      "cases": cases, "paired_checkpoints": len(cases) * 3 * len(CONSUMERS),
                      "totals": totals}, separators=(",", ":")))


if __name__ == "__main__":
    main()
