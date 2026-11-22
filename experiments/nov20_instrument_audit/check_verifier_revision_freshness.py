#!/usr/bin/env python3
"""Check how matched verifier caches handle successful stale revision reads."""

from collections import Counter
from dataclasses import dataclass
import json

from check_verifier_regression_intake import checked_route
from run_verifier import (
    ARMS,
    CASES,
    CONSUMERS,
    HERE,
    EvidenceStore,
    canonical,
    check,
    evaluate_models,
    instruments,
)


@dataclass(frozen=True)
class Lookup:
    pinned_version: str | None
    returned_version: str | None
    expected_route: str


OPEN = Lookup("approved", "approved", "candidate")
REVOKED = Lookup("revoked", "revoked", "prior")
STALE = Lookup("revoked", "approved", "specialist")
UNAVAILABLE = Lookup("revoked", None, "specialist")
UNATTESTED = Lookup(None, "revoked", "specialist")
SCENARIOS = {
    "current_after_missed_notification": (OPEN, REVOKED, REVOKED),
    "successful_stale_lookup": (OPEN, STALE, REVOKED),
    "index_unavailable": (OPEN, UNAVAILABLE, REVOKED),
    "request_lacks_current_revision": (OPEN, UNATTESTED, REVOKED),
    "regression_after_current_lookup": (OPEN, REVOKED, STALE),
}


def decide(cache, required_revision, observed, scope, must_pass, expected_labels, tick, work):
    work["index_lookups"] += 1
    if observed is None:
        return None, "specialist", "index unavailable"

    if required_revision is None:
        return None, "specialist", "no authoritative revision for this request"
    if observed.revision != required_revision:
        return None, "specialist", "returned revision differs from request"

    cached = json.loads(cache) if isinstance(cache, bytes) else cache
    if cached is not None and cached["revision"] == required_revision and tick <= cached["valid_through"]:
        work["cache_hits"] += 1
        return None, cached["route"], "reused verified evidence"

    documents = observed.read(work)
    route, _ = checked_route(documents, scope, must_pass, tick, expected_labels)
    work["policy_evaluations"] += 1
    return {
        "revision": required_revision,
        "route": route,
        "valid_through": documents["fallback"]["valid_through"],
    }, route, "evaluated verified evidence"


def run_arm(lookups, arm, snapshots, scope, must_pass, expected_labels):
    cache = None
    work = Counter()
    decisions = []
    for tick, lookup in enumerate(lookups):
        pinned = snapshots.get(lookup.pinned_version)
        observed = snapshots.get(lookup.returned_version)
        for consumer in CONSUMERS:
            packet, route, reason = decide(
                cache, pinned.revision if pinned else None, observed,
                scope, must_pass, expected_labels, tick, work,
            )
            if packet is not None:
                cache = canonical(packet) if arm == "retained_qualification" else packet
                work["cache_writes"] += 1
                if isinstance(cache, bytes):
                    work["handoff_bytes"] += len(cache)
            decisions.append({
                "tick": tick,
                "consumer": consumer,
                "pinned_version": lookup.pinned_version,
                "returned_version": lookup.returned_version,
                "route": route,
                "reason": reason,
                "expected_route": lookup.expected_route,
            })
    return {"decisions": decisions, "work": dict(sorted(work.items()))}


def fixture():
    design = json.loads(CASES.read_bytes())
    scope, approved = instruments("clean-control", evaluate_models(design))
    must_pass = json.loads((HERE / "verifier_profiles.json").read_bytes())["must_pass"][scope]
    expected_labels = {case: label for case, _, label in design["evaluation"][scope]}
    revoked = {**approved, "approval": {**approved["approval"], "allowed": False}}
    snapshots = {}
    for version, documents in (("approved", approved), ("revoked", revoked)):
        snapshots[version] = EvidenceStore()
        snapshots[version].publish(documents, Counter())
    if snapshots["approved"].revision == snapshots["revoked"].revision:
        raise ValueError("approval revocation did not change the evidence revision")
    return scope, must_pass, expected_labels, snapshots


def main():
    frozen = check()
    scope, must_pass, expected_labels, snapshots = fixture()
    cases = []
    for name, lookups in SCENARIOS.items():
        results = {
            arm: run_arm(lookups, arm, snapshots, scope, must_pass, expected_labels)
            for arm in ARMS
        }
        for arm, result in results.items():
            for row in result["decisions"]:
                if row["route"] != row["expected_route"]:
                    raise ValueError(f"{name} / {arm}: unexpected decision {row}")
        cases.append({"case": name, "arms": results})

    print(json.dumps({
        "scope": scope,
        "frozen_inputs": frozen,
        "revisions": {name: snapshot.revision for name, snapshot in snapshots.items()},
        "paired_checkpoints": sum(len(row["arms"][ARMS[0]]["decisions"]) for row in cases),
        "cases": cases,
    }, indent=2))


if __name__ == "__main__":
    main()
