#!/usr/bin/env python3
"""Compare matched cache decisions using a separate revision authority process."""

from collections import Counter
from contextlib import contextmanager
import json
from multiprocessing import get_context

from check_verifier_revision_freshness import (
    ARMS,
    CONSUMERS,
    Lookup,
    OPEN,
    REVOKED,
    SCENARIOS,
    canonical,
    check,
    decide,
    fixture,
)


PROCESS_SCENARIOS = {
    **SCENARIOS,
    "fallback_expired": (OPEN, REVOKED, REVOKED, Lookup("revoked", "revoked", "specialist")),
}


def revision_authority(channel, scope, revisions):
    """Own the scoped revision pointer and answer requests independently of the index view."""
    version = "approved"
    for data in iter(channel.recv_bytes, b""):
        request = json.loads(data)
        action = request["action"]
        if action == "set":
            next_version = request["version"]
            if next_version not in revisions:
                raise ValueError(f"unknown evidence version: {next_version}")
            version = next_version
            response = {"set": version}
        elif action == "read":
            valid = request["scope"] == scope and request["available"]
            response = {"scope": scope, "revision": revisions[version] if valid else None}
        else:
            raise ValueError(f"unknown authority action: {action}")
        channel.send_bytes(canonical(response))


def cache_worker(channel, arm, scope, must_pass, expected_labels, snapshots):
    cache = None
    work = Counter()
    for data in iter(channel.recv_bytes, b""):
        request = json.loads(data)
        if request == {"read_work_counters": True}:
            channel.send_bytes(canonical(dict(sorted(work.items()))))
            continue
        tick = request["tick"]
        authority = request["authority"]
        required = authority["revision"] if authority["scope"] == scope else None
        observed = snapshots.get(request["index_version"])
        packet, route, reason = decide(
            cache, required, observed, scope, must_pass, expected_labels, tick, work
        )
        if packet is not None:
            cache = canonical(packet) if arm == "retained_qualification" else packet
            work["cache_writes"] += 1
            if isinstance(cache, bytes):
                work["handoff_bytes"] += len(cache)
        channel.send_bytes(canonical({
            "route": route,
            "reason": reason,
            "revision": required,
        }))


@contextmanager
def endpoint(target, *arguments):
    ctx = get_context("spawn")
    parent, child = ctx.Pipe()
    process = ctx.Process(target=target, args=(child, *arguments))
    process.start()
    child.close()
    try:
        yield parent
        parent.send_bytes(b"")
        process.join(timeout=5)
        if process.exitcode != 0:
            raise RuntimeError(f"{target.__name__} did not exit cleanly: {process.exitcode}")
    finally:
        parent.close()
        if process.is_alive():
            process.terminate()
            process.join()
        process.close()


def call(channel, request, wire):
    encoded = canonical(request)
    channel.send_bytes(encoded)
    if not channel.poll(5):
        raise RuntimeError(f"no response for {request}")
    data = channel.recv_bytes()
    wire["messages"] += 2
    wire["payload_bytes"] += len(encoded) + len(data)
    return json.loads(data)


def run_arm(lookups, arm, scope, must_pass, expected_labels, snapshots):
    revisions = {name: snapshot.revision for name, snapshot in snapshots.items()}
    authority_wire, worker_wire = Counter(), Counter()
    decisions = []
    with (
        endpoint(revision_authority, scope, revisions) as authority,
        endpoint(cache_worker, arm, scope, must_pass, expected_labels, snapshots) as worker,
    ):
        for tick, lookup in enumerate(lookups):
            if tick == 1:
                response = call(authority, {"action": "set", "version": "revoked"}, authority_wire)
                if response["set"] != "revoked":
                    raise ValueError("authority did not record revocation")
            for consumer in CONSUMERS:
                authority_record = call(authority, {
                    "action": "read", "scope": scope, "available": lookup.pinned_version is not None,
                }, authority_wire)
                expected_revision = revisions.get(lookup.pinned_version)
                if authority_record != {"scope": scope, "revision": expected_revision}:
                    raise ValueError(f"unexpected authority response: {authority_record}")
                result = call(worker, {
                    "authority": authority_record,
                    "index_version": lookup.returned_version,
                    "tick": tick,
                }, worker_wire)
                if result["route"] != lookup.expected_route:
                    raise ValueError(f"{arm} / tick {tick} / {consumer}: unexpected decision {result}")
                decisions.append({
                    "tick": tick, "consumer": consumer, "observed_index_version": lookup.returned_version,
                    "expected_route": lookup.expected_route,
                    "route": result["route"], "reason": result["reason"], "revision": result["revision"],
                })
        work = call(worker, {"read_work_counters": True}, Counter())
    return {
        "decisions": decisions,
        "authority_pipe": dict(authority_wire),
        "worker_pipe": dict(worker_wire),
        "work": work,
    }


def main():
    frozen = check()
    scope, must_pass, expected_labels, snapshots = fixture()
    cases = [
        {"case": name, "arms": {
            arm: run_arm(lookups, arm, scope, must_pass, expected_labels, snapshots)
            for arm in ARMS
        }}
        for name, lookups in PROCESS_SCENARIOS.items()
    ]
    totals = {}
    for arm in ARMS:
        work, wire, routes = Counter(), Counter(), Counter()
        for case in cases:
            outcome = case["arms"][arm]
            work.update(outcome["work"])
            wire.update(outcome["authority_pipe"])
            wire.update(outcome["worker_pipe"])
            routes.update(row["route"] for row in outcome["decisions"])
        totals[arm] = {"work": dict(work), "wire": dict(wire), "routes": dict(routes)}
    print(json.dumps({
        "scope": scope,
        "frozen_inputs": frozen,
        "paired_checkpoints": sum(len(case["arms"][ARMS[0]]["decisions"]) for case in cases),
        "cases": cases,
        "totals": totals,
    }, indent=2))


if __name__ == "__main__":
    main()
