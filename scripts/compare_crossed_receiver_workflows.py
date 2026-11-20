#!/usr/bin/env python3
"""Compare conventional status checks with an optional receiving-side read."""

from __future__ import annotations

import argparse
from dataclasses import asdict
from itertools import product
import json
from pathlib import Path
import tempfile

from compare_fresh_effect_workflows import (
    CHECKPOINTS,
    EXPERIMENT,
    FIXTURES,
    ROOT,
    LocalReceiver,
    Observation,
    Operation,
    calibrate,
    canonical,
    digest,
    interpret,
    prepare,
    read_receipt,
    score,
)

LOCK = EXPERIMENT / "crossed_receiver_lock.json"
PROFILE_READS = {
    "shared_fresh": ("fresh", "fresh"),
    "shared_stale": ("stale", "stale"),
    "shared_unavailable": ("unavailable", "unavailable"),
    "stale_status": ("stale", "fresh"),
    "unavailable_status": ("unavailable", "fresh"),
}
ARMS = ("conventional_status", "additional_observation")


def observation(
    receiver: LocalReceiver,
    operation: Operation,
    tick: int,
    mode: str,
    initial: Observation | None,
) -> Observation | None:
    if mode == "fresh":
        return read_receipt(receiver.database, operation.key, tick)
    if mode == "stale":
        return initial
    if mode == "unavailable":
        return None
    raise ValueError(f"unknown observation mode: {mode}")


def workflow(receiver: LocalReceiver, operation: Operation, arm: str, profile: str) -> dict:
    response = receiver.submit(operation, 1)
    actions = [{"tick": 1, "action": "submit", "response": response}]
    status_mode, direct_mode = PROFILE_READS[profile]
    # Capture the known initial state for the simulated stale views. This
    # fixture action occurs outside both workflows and grants no knowledge.
    initial = read_receipt(receiver.database, operation.key, 1)
    for tick in CHECKPOINTS:
        receiver.advance(tick)
        if response == "ambiguous":
            status = observation(receiver, operation, tick, status_mode, initial)
            actions.append({"tick": tick, "action": "status", "receipt": asdict(status) if status else None})
            if arm == "additional_observation" and (status is None or status.tick != tick):
                status = observation(receiver, operation, tick, direct_mode, initial)
                actions.append({"tick": tick, "action": "receive_read", "receipt": asdict(status) if status else None})
            response = interpret(status, operation, tick)
        if response == "failed" or (response == "ambiguous" and receiver.idempotent):
            response = receiver.submit(operation, tick)
            actions.append({"tick": tick, "action": "retry", "response": response})
    return {"disposition": "closed" if response == "committed" else "hold", "actions": actions}


def calibration(root: Path, task: dict) -> dict:
    results = calibrate(root, task)
    for scenario, submissions, expected_commits, expected_closure in (
        ("acknowledged", 1, 1, True),
        ("acknowledged", 2, 2, False),
        ("failed_before_commit", 1, 0, False),
    ):
        name = f"scorer_{expected_commits}_commit"
        work = root / name
        allowed, payload = prepare(work, task)
        assert allowed and payload
        op = Operation(task["id"], task["destination"], payload)
        receiver = LocalReceiver(root / f"{name}.sqlite", False, scenario)
        for tick in range(1, submissions + 1):
            receiver.submit(op, tick)
        result = score(work, receiver.database, task, op, "closed")
        results[name] = (
            result["effect_commits"] == expected_commits
            and result["accepted_useful"] == expected_closure
            and result["false_closure"] == (not expected_closure)
        )

    work = root / "wrong-scope"
    narrowed = {**task, "write_scope": task["write_scope"][:1]}
    allowed, payload = prepare(work, narrowed)
    results["scope_rejection"] = not allowed and payload is None
    return results


def run_pair(root: Path, task: dict, idempotent: bool, scenario: str, profile: str) -> dict:
    results = {}
    for arm in ARMS:
        run = root / arm
        run.mkdir(parents=True)
        work = run / "work"
        allowed, payload = prepare(work, task)
        expected = digest(canonical(task["expected"]))
        op = Operation(task["id"], task["destination"], payload or expected)
        receiver = LocalReceiver(run / "receiver.sqlite", idempotent, scenario)
        if allowed and payload == expected:
            disposition = workflow(receiver, op, arm, profile)
        else:
            disposition = {"disposition": "denied", "actions": []}
        results[arm] = {
            **disposition,
            **score(work, receiver.database, task, op, disposition["disposition"]),
        }
    return {
        "task": task["id"],
        "sink_idempotent": idempotent,
        "scenario": scenario,
        "observation_profile": profile,
        "arms": results,
    }


def summary(pairs: list[dict]) -> list[dict]:
    rows = []
    for profile, idempotent, arm in product(PROFILE_READS, (False, True), ARMS):
        group = [
            pair["arms"][arm] for pair in pairs
            if pair["observation_profile"] == profile and pair["sink_idempotent"] == idempotent
        ]
        metrics = {
            outcome: sum(row[outcome] for row in group)
            for outcome in ("accepted_useful", "safe_hold", "unresolved", "false_closure", "wrongful_block")
        }
        rows.append({
            "profile": profile,
            "sink_idempotent": idempotent,
            "arm": arm,
            "cases": len(group),
            **metrics,
            "repeated_effect": sum(row["effect_commits"] > 1 for row in group),
            "retries": sum(action["action"] == "retry" for row in group for action in row["actions"]),
            "receiver_reads": sum(action["action"] == "receive_read" for row in group for action in row["actions"]),
        })
    return rows


def run_series(workspace: Path) -> dict:
    frozen = json.loads(LOCK.read_bytes())
    files = (
        EXPERIMENT / "crossed_receiver_protocol.md",
        FIXTURES,
        Path(__file__).resolve(),
        ROOT / "scripts/compare_fresh_effect_workflows.py",
        ROOT / "scripts/run_p5_u1_governed_repository_change.py",
    )
    actual = {str(path.relative_to(ROOT)): digest(path.read_bytes()) for path in files}
    if frozen != actual:
        raise ValueError("crossed receiver series refuses altered frozen inputs")
    design = json.loads(FIXTURES.read_bytes())
    controls = calibration(workspace, design["tasks"][0])
    pairs = []
    if all(controls.values()):
        for index, args in enumerate(product(design["tasks"], (False, True), design["scenarios"], PROFILE_READS)):
            pairs.append(run_pair(workspace / str(index), *args))
    return {
        "frozen_inputs": frozen,
        "calibration": controls,
        "human_time_measured": False,
        "paired_results_by_condition": summary(pairs) if pairs else [],
        "pairs": pairs,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--compact", action="store_true", help="emit compact JSON with one pair per line")
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="asi-crossed-receiver-") as directory:
        result = run_series(Path(directory))
    if args.compact:
        pairs = result.pop("pairs")
        print(json.dumps(result, indent=2).removesuffix("\n}") + ',\n  "pairs": [')
        print(",\n".join("    " + json.dumps(row, separators=(",", ":")) for row in pairs))
        print("  ]\n}")
    else:
        print(json.dumps(result, indent=2))
    if not all(result["calibration"].values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
