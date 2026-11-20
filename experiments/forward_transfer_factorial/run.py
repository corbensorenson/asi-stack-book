#!/usr/bin/env python3
"""Run the locked selection × representation follow-up (Python 3.10+)."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
import hashlib
from itertools import product
import json
from pathlib import Path
import re
from time import process_time_ns

from oracle import DOMAIN, FAMILIES, verify


HERE = Path(__file__).resolve().parent
INPUTS = ("protocol.md", "history.json", "oracle.py", "run.py")
VISIBLE = (0, 1, 2, 4, 6, 9, 17, 31)
BUDGETS = {"proposals": 96, "expanded": 1450}
PRIMITIVES = {
    "left": lambda x: (x << 1) & 31,
    "right": lambda x: x >> 1,
    "roll": lambda x: ((x << 1) & 31) | (x >> 4),
    "low": lambda x: x & 15,
    "flip": lambda x: x ^ 31,
    "odd": lambda x: x ^ 1,
    "high": lambda x: x ^ 16,
}
ARMS = ("no_library", "aware_whole", "aware_routine", "blind_whole", "blind_routine")
ORDERS = {
    "forward": (False, False),
    "primitives-reversed": (True, False),
    "library-reversed": (False, True),
    "both-reversed": (True, True),
}


def terms(text):
    return set(re.findall(r"[a-z]+", text.lower()))


def evaluate(program, word):
    for op in program:
        word = PRIMITIVES[op](word)
    return word


def library_index(history):
    groups = defaultdict(list)
    for source in history:
        groups[source["group"]].append(source)
    index = {}
    windows = 0
    for name, sources in sorted(groups.items()):
        ordered = sorted(sources, key=lambda row: row["id"])
        counts = Counter(fragment for row in ordered for fragment in zip(row["program"], row["program"][1:]))
        windows += sum(counts.values())
        motif = min(counts, key=lambda fragment: (-counts[fragment], fragment))
        if counts[motif] < 2 or len(ordered) != 2:
            raise ValueError("a historical group lacks its repeated motif and paired provenance")
        index[name] = {
            "terms": set().union(*(terms(row["description"]) for row in ordered)),
            "whole": tuple(ordered[0]["program"]),
            "routine": motif,
        }
    return index, windows


def select(index, task, description, aware):
    if not aware:
        return sorted(index, key=lambda name: hashlib.sha256(f"{task}/{name}".encode()).digest())[:2]
    query = terms(description)
    return sorted(index, key=lambda name: (
        -len(query & index[name]["terms"]) / len(query | index[name]["terms"]), name
    ))[:2]


def search(expected, library, order, budget):
    reverse_primitive, reverse_library = ORDERS[order]
    names = tuple(PRIMITIVES)
    primitives = [(name, (name,)) for name in (names[::-1] if reverse_primitive else names)]
    operators = primitives + (library[::-1] if reverse_library else library)
    queue = deque([((), ())])
    queued = {()}
    target = tuple(expected[word] for word in VISIBLE)
    attempts = screened = checked = check_calls = 0
    rejected = []
    solution = None
    reason = "queue_exhausted"
    verify_ns = 0
    started = process_time_ns()
    cap = BUDGETS[budget]

    while queue:
        handles, expanded = queue.popleft()
        screen = len(VISIBLE) * len(expanded)
        if (budget == "proposals" and attempts >= cap) or (budget == "expanded" and screened + checked + screen > cap):
            reason = "screen_budget_exhausted"
            break
        attempts += 1
        screened += screen
        if tuple(evaluate(expanded, word) for word in VISIBLE) == target:
            verify_work = len(DOMAIN) * len(expanded)
            if budget == "expanded" and screened + checked + verify_work > cap:
                reason = "verification_budget_exhausted"
                break
            check_calls += 1
            checked += verify_work
            start_check = process_time_ns()
            witness = verify(expanded, expected)
            verify_ns += process_time_ns() - start_check
            if witness is None:
                reason = "verified"
                solution = {"operators": handles, "expanded": expanded}
                break
            rejected.append({"proposal": attempts, "expanded": expanded, "witness": witness})
        for alias, operations in operators:
            proposal = expanded + operations
            if proposal not in queued:
                queued.add(proposal)
                queue.append((handles + (alias,), proposal))
    return {
        "terminal": reason, "proposals": attempts, "screening_steps": screened, "verification_steps": checked,
        "verification_calls": check_calls, "queue_insertions": len(queued),
        "counterexamples": rejected, "solution": solution,
    }, {"search_cpu_ns": process_time_ns() - started - verify_ns, "verification_cpu_ns": verify_ns}


def summary(cases, group):
    result = {}
    for key, selected in group:
        counts = {}
        for arm in ARMS:
            values = [row["arms"][arm] for row in selected]
            counts[arm] = {
                "verified": sum(row["terminal"] == "verified" for row in values),
                "counterexamples": sum(len(row["counterexamples"]) for row in values),
                **{field: sum(row[field] for row in values) for field in (
                    "proposals", "screening_steps", "verification_steps", "verification_calls",
                    "queue_insertions", "index_scores",
                )},
            }
        signed = {arm: row["verified"] for arm, row in counts.items()}
        result[key] = {
            "cells": len(selected), "unique_tasks": len({row["task"] for row in selected}), "arms": counts,
            "paired_count_deltas": {
                "aware_minus_blind_whole": signed["aware_whole"] - signed["blind_whole"],
                "aware_minus_blind_routine": signed["aware_routine"] - signed["blind_routine"],
                "routine_minus_whole_aware": signed["aware_routine"] - signed["aware_whole"],
                "routine_minus_whole_blind": signed["blind_routine"] - signed["blind_whole"],
            },
        }
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timings", type=Path)
    args = parser.parse_args()
    lock = json.loads((HERE / "input_lock.json").read_text())
    observed = {name: hashlib.sha256((HERE / name).read_bytes()).hexdigest() for name in INPUTS}
    if lock != observed:
        raise ValueError("factorial study refuses changed inputs")

    history = json.loads((HERE / "history.json").read_text())
    start = process_time_ns()
    index, windows = library_index(history)
    setup_ns = process_time_ns() - start
    targets = [(family, task, prompt, tuple(fn(x) for x in DOMAIN))
               for family, tasks in FAMILIES.items() for task, (prompt, fn) in tasks.items()]
    preceding = {tuple(evaluate(h["program"], x) for x in DOMAIN) for h in history}
    later = {row[3] for row in targets}
    calibration = {
        "known_good": verify(("left",), tuple(2*x % 32 for x in DOMAIN)) is None,
        "known_bad": verify(("right",), tuple(2*x % 32 for x in DOMAIN)) is not None,
        "identities_disjoint": not {h["id"] for h in history}.intersection(row[1] for row in targets)
        and len({row[1] for row in targets}) == len(targets),
        "historical_maps_disjoint": len(later) == len(targets) and not later.intersection(preceding),
        "equal_distinct_libraries": len(index) == 6 and all(
            len({entry[kind] for entry in index.values()}) == len(index) for kind in ("whole", "routine")
        ),
    }
    if not all(calibration.values()):
        raise ValueError(f"factorial calibration failed: {calibration}")

    cases, measurements = [], []
    for (family, task, descriptive, target), phrasing, budget, order in product(
        targets, ("descriptive", "neutral"), BUDGETS, ORDERS
    ):
        query = descriptive if phrasing == "descriptive" else "apply the specified mapping"
        arms = {}
        for arm in ARMS:
            start = process_time_ns()
            library = []
            scores = 0
            if arm != "no_library":
                selection, representation = arm.split("_")
                groups = select(index, task, query, selection == "aware")
                library = [(name, index[name][representation]) for name in groups]
                scores = len(index)
            retrieval_ns = process_time_ns() - start
            outcome, timing = search(target, library, order, budget)
            arms[arm] = {"library": library, "index_scores": scores, **outcome}
            measurements.append({
                "task": task, "phrasing": phrasing, "budget": budget, "order": order, "arm": arm,
                "retrieval_cpu_ns": retrieval_ns, **timing,
            })
        cases.append({
            "family": family, "task": task, "phrasing": phrasing, "query": query, "budget": budget,
            "order": order, "arms": arms,
        })

    strata = [("all", cases)]
    strata += [(f"{regime}/{phrasing}", [row for row in cases if row["budget"] == regime and row["phrasing"] == phrasing])
               for regime, phrasing in product(BUDGETS, ("descriptive", "neutral"))]
    by_family = [(family, [row for row in cases if row["family"] == family]) for family in FAMILIES]
    ordering = defaultdict(set)
    for row in cases:
        for arm, result in row["arms"].items():
            key = (row["task"], row["phrasing"], row["budget"], arm)
            ordering[key].add(result["terminal"] == "verified")
    result = {
        "schema_version": "asi_stack.forward_transfer_factorial.v1",
        "frozen_inputs": lock, "calibration": calibration, "budget_caps": BUDGETS, "visible_inputs": VISIBLE,
        "historical_programs": len(history), "motif_windows": windows, "unique_task_count": len(targets),
        "target_vectors": {task: target for _, task, _, target in targets},
        "summary": summary(cases, strata), "by_family": summary(cases, by_family),
        "ordering_success_changes": {arm: sum(len(flags) > 1 for key, flags in ordering.items() if key[-1] == arm)
                                     for arm in ARMS},
        "cases": cases,
    }
    if args.timings:
        args.timings.write_text(json.dumps({"indexing_cpu_ns": setup_ns, "cells": measurements}, indent=2) + "\n")
    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    main()
