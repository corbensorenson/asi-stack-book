#!/usr/bin/env python3
"""Check a stricter regression intake against the frozen verifier fixture."""

from copy import deepcopy
import json

from run_verifier import CASES, HERE, check, choose, evaluate_models, instruments
from compare_verifier_replacements import LABELS


def checked_route(documents, scope, required, tick, expected_labels):
    """Use the fixture's case manifest to validate submitted predictions."""
    seen = set()
    for row in documents["regression"]:
        case = row["case"]
        if case in seen:
            return "specialist", f"duplicate case: {case}"
        if case not in expected_labels:
            return "specialist", f"unexpected case: {case}"
        if row["label"] != expected_labels[case]:
            return "specialist", f"reference label mismatch: {case}"
        if row["prior"] not in LABELS or row["candidate"] not in LABELS:
            return "specialist", f"invalid prediction: {case}"
        seen.add(case)
    missing = sorted(expected_labels.keys() - seen)
    if missing:
        return "specialist", "missing cases: " + ", ".join(missing)
    return choose(documents, scope, required, tick)["route"], "valid evidence"


def main():
    check()
    design = json.loads(CASES.read_bytes())
    expected = {
        scope: {case: label for case, _, label in cases}
        for scope, cases in design["evaluation"].items()
    }
    required = json.loads((HERE / "verifier_profiles.json").read_bytes())["must_pass"]
    models = evaluate_models(design)
    scope, clean = instruments("clean-control", models)
    _, shared_miss = instruments("copy-09-shared-miss", models)
    _, missing_required = instruments("missing-must-pass", models)
    record_scope, regression = instruments("record-change-negative-flips", models)
    target = next(row for row in clean["regression"] if row["case"] == "copy-09")
    wrong_label = next(label for label in LABELS if label != target["label"])
    failed = {**target, "prior": wrong_label, "candidate": wrong_label}

    earlier_duplicate = deepcopy(clean)
    earlier_duplicate["regression"].insert(0, failed)
    later_duplicate = deepcopy(clean)
    later_duplicate["regression"].append(failed)
    relabeled = deepcopy(clean)
    index = relabeled["regression"].index(target)
    relabeled["regression"][index] = {**failed, "label": wrong_label}
    unexpected = deepcopy(clean)
    unexpected["regression"].append({**target, "case": "out-of-scope"})
    invalid = deepcopy(clean)
    invalid["regression"][index]["candidate"] = "unrecognized"
    missing_other = deepcopy(clean)
    other_id = missing_other["regression"][0]["case"]
    del missing_other["regression"][0]

    controls = (
        ("clean", scope, clean, "candidate", "candidate", "valid evidence"),
        ("shared miss", scope, shared_miss, "specialist", "specialist", "valid evidence"),
        ("protected regression", record_scope, regression, "prior", "prior", "valid evidence"),
        ("earlier duplicate", scope, earlier_duplicate, "candidate", "specialist", "duplicate case: copy-09"),
        ("later duplicate", scope, later_duplicate, "specialist", "specialist", "duplicate case: copy-09"),
        ("substituted label", scope, relabeled, "candidate", "specialist", "reference label mismatch: copy-09"),
        ("unexpected case", scope, unexpected, "candidate", "specialist", "unexpected case: out-of-scope"),
        ("invalid prediction", scope, invalid, "prior", "specialist", "invalid prediction: copy-09"),
        ("missing required case", scope, missing_required, "specialist", "specialist", "missing cases: copy-09"),
        ("missing other case", scope, missing_other, "candidate", "specialist", f"missing cases: {other_id}"),
    )
    for name, scope, documents, old_route, new_route, reason in controls:
        retained = choose(documents, scope, required[scope], 0)["route"]
        checked = checked_route(documents, scope, required[scope], 0, expected[scope])
        if retained != old_route or checked != (new_route, reason):
            raise ValueError(f"{name}: expected {old_route} -> {new_route} ({reason}), got {retained} -> {checked}")
        print(f"{name}: {retained} -> {new_route} ({reason})")


if __name__ == "__main__":
    main()
