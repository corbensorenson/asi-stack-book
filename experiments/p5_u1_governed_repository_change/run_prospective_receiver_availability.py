#!/usr/bin/env python3
"""Compare caller-visible receiver endpoints under the frozen local design."""

from __future__ import annotations

import argparse
from contextlib import closing, contextmanager
from hashlib import sha256
from itertools import product
import json
from multiprocessing import get_context
from pathlib import Path
import sqlite3
import tempfile
from time import perf_counter_ns


HERE = Path(__file__).resolve().parent
INPUTS = HERE / "prospective_receiver_availability_inputs.json"
INPUT_SHA256 = "95e2d5c58ea4da2847406fca3de23dcec1bc36aabcd494ff28d2f9df924aa1e0"
REVISION = 1


def wire(value):
    return json.dumps(value, separators=(",", ":"), sort_keys=True).encode()


def frozen_design():
    raw = INPUTS.read_bytes()
    if sha256(raw).hexdigest() != INPUT_SHA256:
        raise ValueError("Prospective receiver design changed after it was fixed")
    design = json.loads(raw)
    protocol = (HERE / design["protocol"]).read_bytes()
    if sha256(protocol).hexdigest() != design["protocol_sha256"]:
        raise ValueError("Prospective receiver protocol differs from the fixed design")
    return design


def exchange(channel, request):
    encoded = wire(request)
    channel.send_bytes(encoded)
    if not channel.poll(5):
        raise TimeoutError("No response from a local comparison process")
    response = channel.recv_bytes()
    return json.loads(response), len(encoded) + len(response)


def serve_projection(channel):
    mode, snapshot = "unavailable", ()
    while True:
        request = json.loads(channel.recv_bytes())
        command = request["command"]
        if command == "stop":
            return
        if command == "reset":
            mode, snapshot = request["mode"], request["effects"]
            channel.send_bytes(wire({"reset": True}))
            continue
        if mode == "unavailable":
            observation = None
        else:
            fresh = mode == "fresh"
            observation = {
                "source_revision": REVISION if fresh else 0,
                "response_tick": request["tick"],
                "operation": request["operation"],
                "effects": snapshot if fresh else [],
                "pre_effect_failure": not snapshot if fresh else True,
            }
        channel.send_bytes(wire(observation))


def current(response, task):
    return (response is not None and response["source_revision"] == REVISION
            and response["operation"] == task["operation"])


def serve_gateway(caller, telemetry, primary, secondary):
    """Conventional endpoint with the same two-source access as the caller."""
    while True:
        request = json.loads(caller.recv_bytes())
        if request["command"] == "stop":
            return
        response, size = exchange(primary, request)
        calls = 1
        if not current(response, request):
            response, extra = exchange(secondary, {**request, "tick": 2})
            size += extra
            calls += 1
        caller.send_bytes(wire(response))
        telemetry.send_bytes(wire({"reads": calls, "bytes": size}))


@contextmanager
def services():
    context = get_context("spawn")
    primary, main_port = context.Pipe()
    secondary, extra_port = context.Pipe()
    gateway, gateway_port = context.Pipe()
    telemetry, gateway_telemetry = context.Pipe(duplex=False)
    processes = [
        context.Process(target=serve_projection, args=(main_port,)),
        context.Process(target=serve_projection, args=(extra_port,)),
        context.Process(target=serve_gateway, args=(gateway_port, gateway_telemetry, primary, secondary)),
    ]
    for process in processes:
        process.start()
    try:
        yield primary, secondary, gateway, telemetry
    finally:
        for channel in (gateway, primary, secondary):
            channel.send_bytes(wire({"command": "stop"}))
        for process in processes:
            process.join(5)
            if process.is_alive():
                process.terminate()
                process.join(5)
        for channel in (primary, main_port, secondary, extra_port, gateway,
                        gateway_port, telemetry, gateway_telemetry):
            channel.close()


def effect(task):
    return [task["operation"], task["target"], task["payload"]]


def initial_effects(task, state):
    exact = effect(task)
    if state == "wrong_effect":
        return [[exact[0], exact[1] + "-other", exact[2]]]
    if state == "repeat_effect":
        return [exact, exact]
    return [exact] if state == "exact_effect" else []


def journal(database):
    with closing(sqlite3.connect(database)) as connection:
        return [list(row) for row in connection.execute(
            "SELECT operation, destination, body FROM effects ORDER BY sequence"
        )]


def prepare_journal(database, starting):
    with closing(sqlite3.connect(database)) as connection, connection:
        connection.execute("CREATE TABLE effects (sequence INTEGER PRIMARY KEY, operation TEXT, destination TEXT, body TEXT)")
        connection.executemany("INSERT INTO effects (operation, destination, body) VALUES (?, ?, ?)", starting)


def retry_and_verify(database, task, deduplicates):
    with closing(sqlite3.connect(database)) as connection:
        connection.execute("BEGIN IMMEDIATE")
        known = connection.execute("SELECT 1 FROM effects WHERE operation = ?", (task["operation"],)).fetchone()
        if not known or not deduplicates:
            connection.execute("INSERT INTO effects (operation, destination, body) VALUES (?, ?, ?)", effect(task))
        connection.commit()
    return journal(database) == [effect(task)]


def disposition(response, task):
    if not current(response, task):
        return "hold"
    if response["effects"] == [effect(task)]:
        return "closed"
    if response["pre_effect_failure"] and not response["effects"]:
        return "retry"
    return "escalate"


def score(database, task, before, decision):
    """Observe committed rows independently of the caller's claimed disposition."""
    after = journal(database)
    exact = effect(task)
    before_wrong = sum(row != exact for row in before)
    after_wrong = sum(row != exact for row in after)
    return {
        "terminal_effects": after,
        "verified_closure": decision == "closed" and after == [exact],
        "false_closure": decision == "closed" and after != [exact],
        "wrong_effect": after_wrong > 0, "wrong_effect_introduced": after_wrong > before_wrong,
        "repeat_effect": len(after) > 1, "repeat_effect_introduced": len(after) > max(1, len(before)),
        "operator_work_requested": decision in {"hold", "escalate"},
    }


def trial(channels, database, task, starting, modes, arm, dedup, design):
    primary, secondary, gateway, telemetry = channels
    prepare_journal(database, starting)
    for channel, mode in zip((primary, secondary), modes, strict=True):
        exchange(channel, {"command": "reset", "mode": mode, "effects": starting})
    request = {"command": "status", "tick": 1, "operation": task["operation"]}
    start = perf_counter_ns()
    caller = gateway if arm == "matched_conventional_access" else primary
    response, size = exchange(caller, request)
    reads = calls = 1
    if arm == "matched_conventional_access":
        if not telemetry.poll(5):
            raise TimeoutError("Missing matched endpoint work counters")
        work = json.loads(telemetry.recv_bytes())
        size += work["bytes"]
        reads = work["reads"]
    elif arm == "additional_endpoint" and not current(response, task):
        response, extra = exchange(secondary, {**request, "tick": 2})
        size += extra
        reads = calls = 2
    decision = disposition(response, task)
    retry = decision == "retry" and design["retry_allowance"] == 1
    tick = reads
    if retry:
        tick = design["deadline_tick"]
        decision = "closed" if retry_and_verify(database, task, dedup) else "escalate"
    wall_ns = perf_counter_ns() - start
    return {
        "disposition": decision, "observation": response, "decision_tick": tick,
        "unresolved_ticks_through_horizon": tick if decision == "closed" else design["deadline_tick"],
        "caller_status_calls": calls, "logical_status_reads": reads, "status_payload_bytes": size,
        "retries": int(retry), **score(database, task, starting, decision),
    }, wall_ns


def calibrate(channels, root, design):
    task = design["tasks"][0]
    exact = effect(task)
    arms = design["arms"]
    cases = (
        ("exact", [exact], ("fresh", "fresh"), arms[0], "closed", "verified_closure"),
        ("wrong-target", [[exact[0], exact[1] + "-other", exact[2]]], ("fresh", "fresh"), arms[0], "escalate", "wrong_effect"),
        ("wrong-payload", [[exact[0], exact[1], "different document"]], ("fresh", "fresh"), arms[0], "escalate", "wrong_effect"),
        ("repeat", [exact, exact], ("fresh", "fresh"), arms[0], "escalate", "repeat_effect"),
        ("current-tick-stale", [exact], ("stale", "unavailable"), arms[1], "hold", "operator_work_requested"),
        ("confirmed-failure", [], ("fresh", "fresh"), arms[0], "closed", "verified_closure"),
        ("added-access", [exact], ("unavailable", "fresh"), arms[1], "closed", "verified_closure"),
        ("matched-access", [exact], ("unavailable", "fresh"), arms[2], "closed", "verified_closure"),
    )
    passed = {}
    for name, before, modes, arm, decision, marker in cases:
        observed, _ = trial(channels, root / f"control-{name}.sqlite", task, before, modes, arm, False, design)
        valid = observed["disposition"] == decision and observed[marker]
        if name == "current-tick-stale":
            # The primary service really returned the old revision at the current tick.
            stale, _ = exchange(channels[0], {"command": "status", "tick": 3, "operation": task["operation"]})
            valid &= stale["response_tick"] == 3 and not current(stale, task) and observed["retries"] == 0
        if name == "confirmed-failure":
            valid &= observed["retries"] == 1
        passed[name] = valid
    return passed


def paired_series(root, design):
    arms = design["arms"]
    fields = product(design["tasks"], design["observations"], design["observations"],
                     design["initial_states"], design["deduplication"])
    cases, timings = [], []
    with services() as channels:
        controls = calibrate(channels, root, design)
        if not all(controls.values()):
            return {"calibration": controls, "expected_pairs": design["paired_cells"], "pairs": []}, []
        for i, (task, first, second, state, dedup) in enumerate(fields):
            before = initial_effects(task, state)
            shift = i % len(arms)
            trials = {}
            for arm in arms[shift:] + arms[:shift]:
                record, elapsed = trial(channels, root / f"case-{i}-{arm}.sqlite", task, before,
                                        (first, second), arm, dedup, design)
                trials[arm] = record
                timings.append({"case": i, "arm": arm, "wall_ns": elapsed})
            cases.append({"id": i, "task": task["operation"], "primary": first, "secondary": second,
                          "initial_state": state, "deduplication": dedup,
                          "arms": {arm: trials[arm] for arm in arms}})
    if len(cases) != design["paired_cells"]:
        raise ValueError("The receiver run has an incomplete design")
    return {"calibration": controls, "expected_pairs": design["paired_cells"], "pairs": cases}, timings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timing", type=Path, help="Write separate nondeterministic local wall-time observations")
    args = parser.parse_args()
    design = frozen_design()
    with tempfile.TemporaryDirectory(prefix="asi-prospective-receiver-") as directory:
        result, timings = paired_series(Path(directory), design)
    if args.timing:
        args.timing.write_bytes(wire({"wall_time_scope": "lookup through decision and retry verification",
                                      "observations": timings}) + b"\n")
    print(wire({"schema_version": design["schema_version"], "design_sha256": INPUT_SHA256,
                "protocol_sha256": design["protocol_sha256"], **result}).decode())
    if not all(result["calibration"].values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
