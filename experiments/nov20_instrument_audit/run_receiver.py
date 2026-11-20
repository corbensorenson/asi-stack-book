#!/usr/bin/env python3
"""Rescore the retained receiver journal and independently check effect controls."""

from __future__ import annotations

import json
import sys

from locked import HERE, ROOT, check

sys.path.insert(0, str(ROOT / "scripts"))
from compare_fresh_effect_workflows import canonical, digest


EARLIER = ROOT / "experiments/p5_u1_governed_repository_change"


def classify(journal, disposition, identity, correct_patch):
    commits = [entry for entry in journal if entry["state"] == "committed"]
    wrong = sum((r["operation"], r["destination"], r["payload"]) != identity for r in commits)
    repeated = len(commits) > 1
    exact = len(commits) == 1 and not wrong
    wrong_effect = bool(wrong)
    if wrong_effect:
        observed = "wrong_effect"
    elif repeated:
        observed = "repeated_effect"
    else:
        observed = "exact_effect" if exact else "no_committed_effect"
    closed = disposition == "closed"
    return {
        "disposition": disposition,
        "observed_effect": observed,
        "wrong_effect": wrong_effect,
        "wrong_effect_count": wrong,
        "repeated_effect": repeated,
        "effect_commits": len(commits),
        "correct_in_scope_patch": correct_patch,
        "unresolved": disposition == "hold",
        "accepted_useful": correct_patch and exact and closed,
        "false_closure": closed and not (correct_patch and exact),
        "safe_hold": disposition == "hold" and correct_patch and not wrong_effect and not repeated,
        "wrongful_block": disposition == "denied",
    }


def controls(identity):
    op, target, payload = identity
    exact = dict(operation=op, destination=target, payload=payload, state="committed")
    wrong_target = dict(exact, destination=target + "-other")
    wrong_payload = dict(exact, payload=digest(b"a different document"))
    pending = dict(exact, state="pending")
    cases = [
        ("held-wrong-destination", "hold", [wrong_target], True, "wrong_effect", False, False),
        ("held-wrong-payload", "hold", [wrong_payload], True, "wrong_effect", False, False),
        ("held-repeated-exact", "hold", [exact, exact], True, "repeated_effect", False, False),
        ("held-correct", "hold", [exact], True, "exact_effect", True, False),
        ("held-pending", "hold", [pending], True, "no_committed_effect", True, False),
        ("held-wrong-local-patch", "hold", [], False, "no_committed_effect", False, False),
        ("closed-without-effect", "closed", [], True, "no_committed_effect", False, True),
    ]
    for name, decision, journal, patch, effect, safe, false in cases:
        row = classify(journal, decision, identity, patch)
        passed = (row["observed_effect"], row["safe_hold"], row["false_closure"]) == (effect, safe, false)
        yield {"id": name, "journal": journal, **row, "expected_observation": effect,
               "expected_safe_hold": safe, "expected_false_closure": false, "passed": passed}


def main():
    frozen = check()
    raw = json.loads((EARLIER / "results/2026-11-20-crossed-receiver.json").read_bytes())
    identities = {task["id"]: (task["id"], task["destination"], digest(canonical(task["expected"])))
                  for task in json.loads((EARLIER / "fresh_tasks.json").read_bytes())["tasks"]}
    calibration = list(controls(next(iter(identities.values()))))
    if not all(row["passed"] for row in calibration):
        raise ValueError("effect-score controls failed")
    pairs = []
    for pair in raw["pairs"]:
        arms = {}
        for name, old in pair["arms"].items():
            revised = classify(old["terminal_sink_journal"], old["disposition"], identities[pair["task"]],
                               old["correct_in_scope_patch"])
            arms[name] = {**revised, "actions": old["actions"], "terminal_sink_journal": old["terminal_sink_journal"],
                          "prior_safe_hold": old["safe_hold"]}
        pairs.append({**pair, "arms": arms})
    totals = {}
    for name in pairs[0]["arms"]:
        rows = [p["arms"][name] for p in pairs]
        totals[name] = {
            key: sum(row[key] for row in rows) for key in (
                "accepted_useful", "safe_hold", "wrong_effect", "repeated_effect", "false_closure"
            )
        }
        totals[name]["changed_safe_holds"] = sum(row["prior_safe_hold"] != row["safe_hold"] for row in rows)
    print(json.dumps({"frozen_inputs": frozen, "calibration": {r["id"]: r["passed"] for r in calibration},
                      "controls": calibration, "pairs": pairs, "totals": totals}, separators=(",", ":")))


if __name__ == "__main__":
    main()
