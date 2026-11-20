#!/usr/bin/env python3
"""Compare the original handle-depth queue with expanded-length ordering."""

from __future__ import annotations

import heapq
from itertools import count
import json
import sys

from locked import ROOT, check


FACTORIAL = ROOT / "experiments/forward_transfer_factorial"
sys.path.insert(0, str(FACTORIAL))
import run as prior


def expanded_search(expected, library, order, budget):
    reverse_primitives, reverse_library = prior.ORDERS[order]
    names = tuple(prior.PRIMITIVES)
    ops = [(name, (name,)) for name in (names[::-1] if reverse_primitives else names)]
    ops += library[::-1] if reverse_library else library
    serial = count()
    pending = [(0, next(serial), ())]
    seen = {()}
    target = tuple(expected[word] for word in prior.VISIBLE)
    cap = prior.BUDGETS[budget]
    proposals = screened = verified_work = 0
    terminal = "queue_exhausted"
    solution = None
    counterexamples = []
    while pending:
        _, _, expansion = heapq.heappop(pending)
        work = len(prior.VISIBLE) * len(expansion)
        if (budget == "proposals" and proposals >= cap) or (
            budget == "expanded" and screened + verified_work + work > cap
        ):
            terminal = "screen_budget_exhausted"
            break
        proposals += 1
        screened += work
        if tuple(prior.evaluate(expansion, word) for word in prior.VISIBLE) == target:
            check_work = len(prior.DOMAIN) * len(expansion)
            if budget == "expanded" and screened + verified_work + check_work > cap:
                terminal = "verification_budget_exhausted"
                break
            verified_work += check_work
            witness = prior.verify(expansion, expected)
            if witness is None:
                terminal, solution = "verified", {"expanded": expansion}
                break
            counterexamples.append({"proposal": proposals, "expanded": expansion, "witness": witness})
        for _, suffix in ops:
            candidate = expansion + suffix
            if candidate not in seen:
                seen.add(candidate)
                heapq.heappush(pending, (len(candidate), next(serial), candidate))
    return {"terminal": terminal, "proposals": proposals, "screening_steps": screened,
            "verification_steps": verified_work, "counterexamples": counterexamples,
            "queue_insertions": len(seen), "solution": solution}


def main():
    frozen = check()
    old = json.loads((FACTORIAL / "results/2026-11-20-local.json").read_bytes())
    cases = []
    calibrated = True
    for case in old["cases"]:
        expected = old["target_vectors"][case["task"]]
        comparisons = {}
        for arm, trial in case["arms"].items():
            library = [(label, tuple(ops)) for label, ops in trial["library"]]
            baseline, _ = prior.search(expected, library, case["order"], case["budget"])
            baseline = {"library": trial["library"], "index_scores": trial["index_scores"], **baseline}
            calibrated &= json.loads(json.dumps(baseline)) == trial
            alternative = {"library": trial["library"], **expanded_search(expected, library, case["order"], case["budget"])}
            comparisons[arm + "__handle-depth"] = baseline
            comparisons[arm + "__expanded-length"] = alternative
        cases.append({**case, "arms": comparisons})
    if not calibrated:
        raise ValueError("original scheduler replay did not match its pinned result")
    summary = {}
    for budget in prior.BUDGETS:
        for prompt in ("descriptive", "neutral"):
            rows = [row for row in cases if (row["budget"], row["phrasing"]) == (budget, prompt)]
            summary[f"{budget}/{prompt}"] = {
                "cells": len(rows), "arms": {
                    name: sum(row["arms"][name]["terminal"] == "verified" for row in rows)
                    for name in rows[0]["arms"]
                },
            }
    print(json.dumps({"frozen_inputs": frozen, "calibration": {"exact_prior_replay": calibrated},
                      "budget_caps": old["budget_caps"], "summary": summary, "cases": cases},
                     separators=(",", ":")))


if __name__ == "__main__":
    main()
