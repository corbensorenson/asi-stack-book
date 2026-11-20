#!/usr/bin/env python3
"""Paired finite synthesis pilot. Requires Python 3.10+ and the local fixture."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
import hashlib
import json
from pathlib import Path
import re
from time import process_time_ns

from heldout import FAMILIES, verify


HERE = Path(__file__).resolve().parent
INPUTS = ("protocol.md", "history.json", "heldout.py", "run.py")
BUDGET = 96
EXAMPLES = (0, 1, 2, 3, 6, 7, 10, 15)
PRIMITIVES = {
    "left": lambda x: (x << 1) & 15,
    "right": lambda x: x >> 1,
    "rotate": lambda x: ((x << 1) & 15) | (x >> 3),
    "low": lambda x: x & 7,
    "flip": lambda x: 15 ^ x,
    "odd": lambda x: 1 ^ x,
    "high": lambda x: 8 ^ x,
}
ARMS = ("no_library", "ordinary_retrieval", "reusable_routines")


def evaluate(word: int, program: tuple[str, ...]) -> int:
    for command in program:
        word = PRIMITIVES[command](word)
    return word


def words(prompt: str) -> set[str]:
    return set(re.findall(r"[a-z]+", prompt.lower()))


def retrieved(query: str, index: list[tuple[str, set[str], tuple[str, ...]]]) -> list:
    terms = words(query)
    ranked = sorted(index, key=lambda row: (
        -len(terms & row[1]) / len(terms | row[1]), row[0]
    ))
    return [(row[0], row[2]) for row in ranked[:2]]


def discover(history: list[dict]) -> tuple[list, int]:
    frequency = Counter()
    lineages = defaultdict(set)
    examined = 0
    for row in history:
        program = row["program"]
        for fragment in zip(program, program[1:]):
            examined += 1
            frequency[fragment] += 1
            lineages[fragment].add(row["lineage"])
    ranked = sorted(
        (fragment for fragment, sources in lineages.items() if len(sources) >= 2),
        key=lambda fragment: (-frequency[fragment], fragment),
    )
    return [(f"routine-{n}", ops) for n, ops in enumerate(ranked[:2], 1)], examined


def search(expected: tuple[int, ...], extra: list) -> tuple[dict, dict]:
    operators = {**{key: (key,) for key in PRIMITIVES}, **dict(extra)}
    # The queue stores action handles and their expanded programs. Syntactically
    # identical expansions get one search opportunity regardless of the aliases.
    queue = deque([((), ())])
    seen = {()}
    attempts = screening_work = checker_calls = checker_work = verification_ns = 0
    discarded = []
    enqueued = 1
    search_started = process_time_ns()
    while queue and attempts < BUDGET:
        handles, expanded = queue.popleft()
        attempts += 1
        visible = tuple(evaluate(word, expanded) for word in EXAMPLES)
        screening_work += len(EXAMPLES) * len(expanded)
        if visible == tuple(expected[word] for word in EXAMPLES):
            checker_calls += 1
            start = process_time_ns()
            counterexample, work = verify(expanded, expected)
            verification_ns += process_time_ns() - start
            checker_work += work
            if counterexample is None:
                break
            discarded.append({
                "attempt": attempts, "expanded": expanded, "witness": counterexample,
            })
        for alias, expansion in operators.items():
            candidate = expanded + expansion
            if candidate not in seen:
                seen.add(candidate)
                enqueued += 1
                queue.append((handles + (alias,), candidate))
    else:
        handles = None
        expanded = None
    counters = {
        "terminal": "verified" if expanded is not None else "budget_exhausted",
        "attempts": attempts, "queue_insertions": enqueued, "screening_primitive_steps": screening_work,
        "full_checks": checker_calls, "checker_primitive_steps": checker_work,
        "counterexamples": discarded, "operator_handles": handles, "expanded_program": expanded,
        "expanded_length": len(expanded) if expanded is not None else None,
    }
    return counters, {
        "search_cpu_ns": process_time_ns() - search_started - verification_ns,
        "verification_cpu_ns": verification_ns,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timings", type=Path, help="write diagnostic process CPU times separately")
    args = parser.parse_args()
    frozen = json.loads((HERE / "input_lock.json").read_text())
    actual = {name: hashlib.sha256((HERE / name).read_bytes()).hexdigest() for name in INPUTS}
    if actual != frozen:
        raise ValueError("pilot refuses changed inputs")
    history = json.loads((HERE / "history.json").read_text())
    tasks = [
        (family, identity, query, tuple(reference(x) for x in range(16)))
        for family, rows in FAMILIES.items() for identity, (query, reference) in rows.items()
    ]
    left_vector = tuple(2 * x % 16 for x in range(16))
    historical_vectors = {tuple(evaluate(x, tuple(h["program"])) for x in range(16)) for h in history}
    checks = {
        "known_good_full_domain": verify(("left",), left_vector)[0] is None,
        "known_wrong_candidate_rejected": verify(("right",), left_vector)[0] is not None,
        "unique_later_ids": len({row[1] for row in tasks}) == len(tasks),
        "disjoint_ids_and_lineages": not ({h["id"] for h in history} & {row[1] for row in tasks}
                                         or {h["lineage"] for h in history} & set(FAMILIES)),
        "disjoint_full_output_vectors": len({row[3] for row in tasks}) == len(tasks)
        and not historical_vectors.intersection(row[3] for row in tasks),
    }
    if not all(checks.values()):
        raise ValueError(f"pilot calibration failed: {checks}")

    start = process_time_ns()
    index = [(h["id"], words(h["task"]), tuple(h["program"])) for h in history]
    indexing_ns = process_time_ns() - start
    start = process_time_ns()
    routines, patterns = discover(history)
    discovery_ns = process_time_ns() - start
    if len(routines) != 2:
        raise ValueError("pilot requires two historical routines")
    rows, timing = [], []
    for family, identity, prompt, expected in tasks:
        outcomes = {}
        for arm in ARMS:
            start = process_time_ns()
            library = retrieved(prompt, index) if arm == "ordinary_retrieval" else routines if arm == "reusable_routines" else []
            selection_ns = process_time_ns() - start
            result, diagnostics = search(expected, library)
            outcomes[arm] = {
                "library_entries": library,
                "retrieval_similarities": len(index) if arm == "ordinary_retrieval" else 0,
                **result,
            }
            timing.append({"task": identity, "arm": arm, "selection_cpu_ns": selection_ns, **diagnostics})
        rows.append({"family": family, "task": identity, "description": prompt, "full_reference": expected, "outcomes": outcomes})
    keys = ("attempts", "queue_insertions", "screening_primitive_steps", "full_checks",
            "checker_primitive_steps", "retrieval_similarities")
    totals = {}
    for arm in ARMS:
        runs = [row["outcomes"][arm] for row in rows]
        totals[arm] = {
            "verified": sum(run["terminal"] == "verified" for run in runs),
            "budget_exhausted": sum(run["terminal"] == "budget_exhausted" for run in runs),
            "counterexamples": sum(len(run["counterexamples"]) for run in runs),
            **{key: sum(run[key] for run in runs) for key in keys},
        }
    result = {
        "frozen_inputs": frozen, "calibration": checks, "search_budget": BUDGET,
        "setup": {"historical_programs_indexed": len(index), "adjacent_patterns_examined": patterns, "routines": routines},
        "totals": totals, "tasks": rows,
    }
    if args.timings:
        args.timings.write_text(json.dumps({
            "indexing_cpu_ns": indexing_ns, "discovery_cpu_ns": discovery_ns, "tasks": timing,
        }, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
