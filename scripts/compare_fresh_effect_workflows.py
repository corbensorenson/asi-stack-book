#!/usr/bin/env python3
"""Replay the prospectively specified Git and receiving-service comparison."""

from __future__ import annotations

import argparse
from contextlib import closing
from dataclasses import asdict, dataclass, replace
import hashlib
import json
from pathlib import Path
import sqlite3
import tempfile

from run_p5_u1_governed_repository_change import canonical, git

ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT = ROOT / "experiments/p5_u1_governed_repository_change"
PROTOCOL = EXPERIMENT / "fresh_task_protocol.md"
FIXTURES = EXPERIMENT / "fresh_tasks.json"
LOCK = EXPERIMENT / "fresh_task_execution_lock.json"
ARMS = ("ordinary", "reconciliation")
CHECKPOINTS = (2, 4)
EDITS = {
    "reading-route": (("/guide/old", "/guide/current"),),
    "archive-index": (("draft", "review"), ("false", "true")),
    "caption-correction": (("Figure 4", "Figure 5"),),
    "artifact-index": (('8, "path"', '9, "path"'), ("case-8.json", "case-9.json")),
}


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


@dataclass(frozen=True)
class Operation:
    key: str
    destination: str
    payload_sha256: str


@dataclass(frozen=True)
class Observation:
    operation: Operation
    tick: int
    state: str


class LocalReceiver:
    """A deterministic stateful receiver with a durable journal and submit port."""

    def __init__(self, database: Path, idempotent: bool, scenario: str):
        self.database = database
        self.idempotent = idempotent
        self.scenario = scenario
        with closing(sqlite3.connect(database)) as db, db:
            db.execute("""CREATE TABLE attempts (
                attempt INTEGER PRIMARY KEY, operation TEXT, destination TEXT,
                payload TEXT, state TEXT, tick INTEGER)""")

    def advance(self, tick: int) -> None:
        if tick >= 3:
            with closing(sqlite3.connect(self.database)) as db, db:
                db.execute("UPDATE attempts SET state='committed', tick=3 WHERE state='pending'")

    def submit(self, operation: Operation, tick: int) -> str:
        self.advance(tick)
        with closing(sqlite3.connect(self.database)) as db, db:
            previous = db.execute(
                "SELECT state FROM attempts WHERE operation=? ORDER BY attempt DESC LIMIT 1",
                (operation.key,),
            ).fetchone()
            if self.idempotent and previous and previous[0] in {"pending", "committed"}:
                return previous[0] if previous[0] == "committed" else "ambiguous"
            state, response = ("committed", "committed")
            if not previous:
                state, response = {
                    "acknowledged": ("committed", "committed"),
                    "commit_ack_lost": ("committed", "ambiguous"),
                    "pending_then_commit": ("pending", "ambiguous"),
                    "failed_before_commit": ("failed", "failed"),
                }[self.scenario]
            db.execute(
                "INSERT INTO attempts(operation, destination, payload, state, tick) VALUES (?, ?, ?, ?, ?)",
                (operation.key, operation.destination, operation.payload_sha256, state, tick),
            )
        return response


def read_receipt(database: Path, operation_key: str, tick: int) -> Observation | None:
    """Read the receiving journal without using the workflow or submit response."""
    with closing(sqlite3.connect(database.as_uri() + "?mode=ro", uri=True)) as db:
        row = db.execute(
            """SELECT operation, destination, payload, state FROM attempts
            WHERE operation=? ORDER BY attempt DESC LIMIT 1""",
            (operation_key,),
        ).fetchone()
    if row is None:
        return None
    key, destination, payload, state = row
    return Observation(Operation(key, destination, payload), tick, state)


def interpret(receipt: Observation | None, operation: Operation, tick: int) -> str:
    if receipt is None or receipt.operation != operation or receipt.tick != tick:
        return "ambiguous"
    return receipt.state if receipt.state in {"committed", "failed"} else "ambiguous"


def prepare(work: Path, task: dict, approved: bool = True) -> tuple[bool, str | None]:
    """Apply a known patch and have common diff, expected-output, and approval checks."""
    work.mkdir()
    git(work, "init", "-q", "-b", "main")
    git(work, "config", "user.name", "ASI Stack Local Replay")
    git(work, "config", "user.email", "replay@example.invalid")
    candidate = {}
    for name, before in task["files"].items():
        path = work / name
        if not path.resolve().is_relative_to(work.resolve()):
            raise ValueError(f"unsafe fixture path: {name}")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(before, encoding="utf-8")
        after = before
        for old, new in EDITS[task["id"]]:
            after = after.replace(old, new)
        if after != before:
            candidate[name] = after
    git(work, "add", ".")
    git(work, "commit", "-qm", "frozen maintenance fixture")
    scope = set(task["write_scope"])
    if not approved or not candidate.keys() <= scope:
        return False, None
    for name, content in candidate.items():
        (work / name).write_text(content, encoding="utf-8")
    changed = set(git(work, "diff", "--name-only").stdout.splitlines())
    return changed == set(candidate) and changed <= scope, digest(canonical(candidate))


def apply_workflow(receiver: LocalReceiver, operation: Operation, arm: str) -> dict:
    script = [{"tick": 1, "action": "submit", "response": receiver.submit(operation, 1)}]
    knowledge = script[-1]["response"]
    for tick in CHECKPOINTS:
        receiver.advance(tick)
        if knowledge == "ambiguous" and arm == "reconciliation":
            receipt = read_receipt(receiver.database, operation.key, tick)
            knowledge = interpret(receipt, operation, tick)
            script.append({"tick": tick, "action": "observe", "receipt": asdict(receipt) if receipt else None})
        retry = knowledge == "failed" or (
            knowledge == "ambiguous" and receiver.idempotent and arm == "ordinary"
        )
        if retry:
            knowledge = receiver.submit(operation, tick)
            script.append({"tick": tick, "action": "retry", "response": knowledge})
    return {"disposition": "closed" if knowledge == "committed" else "hold", "actions": script}


def score(work: Path, database: Path, task: dict, operation: Operation, disposition: str) -> dict:
    """Compare terminal tree and receiving journal against the task's frozen oracle."""
    using_scope = set(task["write_scope"])
    actual_paths = set(git(work, "diff", "--name-only").stdout.splitlines())
    correct_patch = actual_paths <= using_scope and all(
        (work / name).read_text(encoding="utf-8") == content
        for name, content in task["expected"].items()
    )
    with closing(sqlite3.connect(database.as_uri() + "?mode=ro", uri=True)) as db:
        db.row_factory = sqlite3.Row
        attempts = [dict(row) for row in db.execute("SELECT * FROM attempts ORDER BY attempt")]
    commits = [row for row in attempts if row["state"] == "committed"]
    correct_effect = len(commits) == 1 and (
        commits[0]["operation"], commits[0]["destination"], commits[0]["payload"]
    ) == (operation.key, task["destination"], digest(canonical(task["expected"])))
    closed = disposition == "closed"
    return {
        "correct_in_scope_patch": correct_patch,
        "effect_commits": len(commits),
        "accepted_useful": correct_patch and correct_effect and closed,
        "false_closure": closed and not (correct_patch and correct_effect),
        "safe_hold": disposition == "hold" and len(commits) <= 1,
        "wrongful_block": disposition == "denied",
        "unresolved": disposition == "hold",
        "terminal_sink_journal": attempts,
    }


def calibrate(root: Path, task: dict) -> dict:
    operation = Operation("calibration", task["destination"], digest(canonical(task["expected"])))
    receiver = LocalReceiver(root / "fixture.sqlite", False, "pending_then_commit")
    receiver.submit(operation, 1)
    pending = read_receipt(receiver.database, operation.key, 2)
    receiver.advance(4)
    committed = read_receipt(receiver.database, operation.key, 4)
    failed_receiver = LocalReceiver(root / "failed.sqlite", False, "failed_before_commit")
    failed_receiver.submit(operation, 1)
    failed = read_receipt(failed_receiver.database, operation.key, 2)
    cases = {
        "pending": (pending, 2, "ambiguous"),
        "wrong_operation": (replace(committed, operation=replace(operation, key="other")), 4, "ambiguous"),
        "wrong_destination": (replace(committed, operation=replace(operation, destination="other")), 4, "ambiguous"),
        "wrong_payload": (replace(committed, operation=replace(operation, payload_sha256="other")), 4, "ambiguous"),
        "stale": (committed, 5, "ambiguous"),
        "missing": (read_receipt(receiver.database, "missing", 4), 4, "ambiguous"),
        "committed": (committed, 4, "committed"),
        "explicit_failure": (failed, 2, "failed"),
    }
    results = {
        name: interpret(receipt, operation, tick) == expected
        for name, (receipt, tick, expected) in cases.items()
    }
    for arm in ARMS:
        work = root / f"denied-{arm}"
        allowed, _ = prepare(work, task, approved=False)
        results[f"{arm}_urgent_without_approval"] = not allowed and not git(work, "diff", "--name-only").stdout
    return results


def run_series(workspace: Path) -> dict:
    design = json.loads(FIXTURES.read_bytes())
    lock = json.loads(LOCK.read_bytes())
    actual = {path.name: digest(path.read_bytes()) for path in (PROTOCOL, FIXTURES, Path(__file__), LOCK.with_name("fresh_task_execution_plan.md"))}
    if actual != lock or actual[PROTOCOL.name] != design["protocol_sha256"]:
        raise ValueError("frozen protocol, fixtures, runner, or execution plan changed")

    calibration = calibrate(workspace, design["tasks"][0])
    pairs = []
    if all(calibration.values()):
        for task in design["tasks"]:
            for scenario in design["scenarios"]:
                results = {}
                for arm in ARMS:
                    run = workspace / f"{task['id']}-{scenario}-{arm}"
                    run.mkdir()
                    work = run / "work"
                    accepted, payload = prepare(work, task)
                    expected = digest(canonical(task["expected"]))
                    if not accepted or payload != expected:
                        raise RuntimeError(f"common candidate failed frozen pre-effect check: {task['id']}")
                    operation = Operation(task["id"], task["destination"], payload)
                    receiver = LocalReceiver(run / "receiver.sqlite", task["sink_idempotent"], scenario)
                    workflow = apply_workflow(receiver, operation, arm)
                    results[arm] = {
                        **workflow,
                        "scripted_approvals": 1,
                        **score(work, receiver.database, task, operation, workflow["disposition"]),
                    }
                pairs.append({"task": task["id"], "scenario": scenario, "sink_idempotent": task["sink_idempotent"], "arms": results})
    return {"frozen_inputs": actual, "calibration": calibration, "human_time_measured": False, "pairs": pairs}


def main() -> None:
    argparse.ArgumentParser(description=__doc__).parse_args()
    with tempfile.TemporaryDirectory(prefix="asi-effect-workflow-") as directory:
        result = run_series(Path(directory))
    print(json.dumps(result, indent=2))
    if not all(result["calibration"].values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
