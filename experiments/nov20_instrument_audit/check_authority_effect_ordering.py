#!/usr/bin/env python3
"""Compare cached approval and version-checked effect transactions."""

from collections import Counter
from contextlib import closing
from dataclasses import dataclass
import json
from pathlib import Path
import sqlite3
from tempfile import TemporaryDirectory

from check_verifier_process_boundary import call, endpoint
from run_verifier import canonical


@dataclass(frozen=True)
class Schedule:
    events: tuple[str, ...]
    effect_tick: int
    expected_cached: str
    expected_transaction: str


SCHEDULES = {
    "commit_then_revoke": Schedule(("check", "effect", "revoke"), 1, "authorized", "authorized"),
    "revoke_then_check": Schedule(("revoke", "check", "effect"), 1, "absent", "absent"),
    "revoke_between_check_and_effect": Schedule(("check", "revoke", "effect"), 1, "unauthorized", "absent"),
    "expire_between_check_and_effect": Schedule(("check", "effect"), 3, "unauthorized", "absent"),
}
ARMS = ("cached_permission_only", "transactional_memo", "transactional_receipt")
SCOPE = "public-copy"
EFFECT = "hold-for-editor"


def grant(connection):
    row = connection.execute(
        "SELECT revision, active, valid_through FROM authority WHERE scope = ?", (SCOPE,)
    ).fetchone()
    revision, active, valid_through = row
    return {"scope": SCOPE, "revision": revision, "active": bool(active), "valid_through": valid_through}


def authority_worker(channel, database):
    with closing(sqlite3.connect(database)) as connection:
        for data in iter(channel.recv_bytes, b""):
            action = json.loads(data)["action"]
            if action == "revoke":
                with connection:
                    connection.execute(
                        "UPDATE authority SET revision = revision + 1, active = 0 WHERE scope = ?", (SCOPE,)
                    )
            elif action != "read":
                raise ValueError(f"unknown authority action: {action}")
            channel.send_bytes(canonical(grant(connection)))


def effect_worker(channel, database, arm):
    saved = None
    with closing(sqlite3.connect(database)) as connection:
        for data in iter(channel.recv_bytes, b""):
            request = json.loads(data)
            if request["action"] == "cache":
                receipt = request["grant"]
                saved = canonical(receipt) if arm == "transactional_receipt" else receipt
                channel.send_bytes(canonical({"cached": True}))
                continue
            if request["action"] != "commit" or saved is None:
                raise ValueError("effect request requires a cached grant")
            receipt = json.loads(saved) if isinstance(saved, bytes) else saved
            tick = request["tick"]
            with connection:
                connection.execute("BEGIN IMMEDIATE")
                active = grant(connection)
                permitted = receipt["scope"] == SCOPE and receipt["active"]
                if arm != "cached_permission_only":
                    permitted = permitted and receipt == active and tick <= active["valid_through"]
                if permitted:
                    connection.execute(
                        "INSERT INTO effects VALUES (?, ?, ?, ?, ?, ?)",
                        (EFFECT, tick, receipt["revision"], active["revision"],
                         active["active"], active["valid_through"]),
                    )
            channel.send_bytes(canonical({"route": "committed" if permitted else "hold"}))


def run_case(database, arm, schedule):
    with closing(sqlite3.connect(database)) as connection, connection:
        connection.execute("CREATE TABLE authority (scope TEXT PRIMARY KEY, revision, active, valid_through)")
        connection.execute("INSERT INTO authority VALUES (?, 1, 1, 2)", (SCOPE,))
        connection.execute(
            "CREATE TABLE effects (effect TEXT PRIMARY KEY, tick, used_revision, live_revision, live_active, deadline)"
        )
    trace = []
    wire = Counter()
    with (
        endpoint(authority_worker, database) as authority,
        endpoint(effect_worker, database, arm) as worker,
    ):
        current = call(authority, {"action": "read"}, wire)
        for event in schedule.events:
            if event == "check":
                current = observed = call(authority, {"action": "read"}, wire)
                cached = current
                call(worker, {"action": "cache", "grant": cached}, wire)
            elif event == "revoke":
                current = observed = call(authority, {"action": "revoke"}, wire)
            else:
                authority_at_write = current
                observed = call(worker, {"action": "commit", "tick": schedule.effect_tick}, wire)
            trace.append({"event": event, "observation": observed})

    with closing(sqlite3.connect(database.as_uri() + "?mode=ro", uri=True)) as connection:
        connection.row_factory = sqlite3.Row
        row = connection.execute("SELECT * FROM effects WHERE effect = ?", (EFFECT,)).fetchone()
        effect = dict(row) if row else None
        observed_revision = grant(connection)["revision"]
    outcome = "absent"
    if effect is not None:
        if effect != {
            "effect": EFFECT,
            "tick": schedule.effect_tick,
            "used_revision": cached["revision"],
            "live_revision": authority_at_write["revision"],
            "live_active": authority_at_write["active"],
            "deadline": authority_at_write["valid_through"],
        }:
            raise ValueError(f"effect record disagrees with the authority timeline: {effect}")
        authorized = (
            cached["revision"] == authority_at_write["revision"]
            and authority_at_write["active"]
            and schedule.effect_tick <= authority_at_write["valid_through"]
        )
        outcome = "authorized" if authorized else "unauthorized"
    expected = schedule.expected_cached if arm == "cached_permission_only" else schedule.expected_transaction
    if outcome != expected:
        raise ValueError(f"{arm} / {schedule.events}: expected {expected}, observed {outcome}")
    return {"trace": trace, "effect": effect, "outcome": outcome, "revision_at_observation": observed_revision}


def main():
    output = []
    with TemporaryDirectory(prefix="asi-authority-effect-") as root:
        for name, schedule in SCHEDULES.items():
            results = {
                arm: run_case(Path(root, f"{name}-{arm}.sqlite"), arm, schedule)
                for arm in ARMS
            }
            output.append({"case": name, "arms": results})
    print(json.dumps({"cases": output}, indent=2))


if __name__ == "__main__":
    main()
