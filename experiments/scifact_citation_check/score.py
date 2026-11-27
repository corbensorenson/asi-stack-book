"""Calibrate two release rules, then evaluate the locked thresholds on paired cases."""
import hashlib
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ARMS = ("pool", "agreement")
USERS = ("triage", "publication")
LABELS = ("CONTRADICT", "SUPPORT", "NEUTRAL")
GRID = [i / 20 for i in range(21)]


def write(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")


def load(split):
    return [json.loads(line) for line in (HERE / (split + ".jsonl")).read_text().splitlines()]


def decision(row, arm, threshold):
    a, b = np.array(row["context"]), np.array(row["citation"])
    if arm == "pool":
        probabilities = (a + b) / 2
    elif a.argmax() == b.argmax():
        probabilities = np.minimum(a, b)
    else:
        return "HOLD"
    i = probabilities.argmax()
    if i == 2 or threshold is None or probabilities[i] < threshold:
        return "HOLD"
    return LABELS[i]


def judge(row, label):
    if label == "HOLD":
        return "held"
    evidence = [set(r["sentences"]) for r in row["evidence_here"] if r["label"] == label]
    cited = set(row["cited"])
    if cited in evidence:
        return "exact"
    if any(rationale <= cited for rationale in evidence):
        return "contains"
    return "unsupported"


def summary(rows, decisions):
    grades = [judge(row, label) for row, label in zip(rows, decisions, strict=True)]
    return dict(justified=grades.count("exact") + grades.count("contains"), exact=grades.count("exact"),
                unsupported=grades.count("unsupported"), held=grades.count("held"),
                answerable_held=sum(g == "held" and r["answerable"] for g, r in zip(grades, rows)))


def measure(rows, arm, threshold):
    return summary(rows, [decision(r, arm, threshold) for r in rows])


def utility(record):
    return record["justified"] - record["unsupported"]


def select(rows):
    policies = {}
    for arm in ARMS:
        grid = [(t, measure(rows, arm, t)) for t in GRID]
        triage = [(t, s) for t, s in grid if 2 * s["held"] <= len(rows)]
        if not triage:
            minimum = min(s["held"] for _, s in grid)
            triage = [(t, s) for t, s in grid if s["held"] == minimum]
        publication = [(t, s) for t, s in grid if len(rows)-s["held"] >= 15
                       and 5*s["unsupported"] <= len(rows)-s["held"]]
        policies[arm] = {
            "triage": max(triage, key=lambda p: (utility(p[1]), -p[1]["unsupported"], -p[0]))[0],
            "publication": max(publication, key=lambda p: (p[1]["justified"], -p[1]["unsupported"], -p[0]))[0]
                           if publication else None,
        }
    return dict(development_sha256=hashlib.sha256((HERE / "development.jsonl").read_bytes()).hexdigest(),
                n=len(rows), policies=policies,
                development={arm: {u: measure(rows, arm, policies[arm][u]) for u in USERS} for arm in ARMS})


def cluster_index(rows):
    # Claims sharing any cited paper belong to one connected component.
    parent = {}
    def root(doc):
        parent.setdefault(doc, doc)
        while parent[doc] != doc:
            parent[doc] = parent[parent[doc]]
            doc = parent[doc]
        return doc
    for row in rows:
        docs = row["group_docs"]
        for doc in docs:
            parent[root(doc)] = root(docs[0])
    ids = [root(r["group_docs"][0]) for r in rows]
    return np.unique(ids, return_inverse=True)[1]


def interval(values):
    finite = values[np.isfinite(values)]
    return np.percentile(finite, [2.5, 97.5]).round(3).tolist() if len(finite) else None


def evaluate(rows, policies):
    groups = cluster_index(rows)
    n_groups = groups.max() + 1
    rng = np.random.default_rng(742)
    draws = rng.integers(0, n_groups, size=(5000, n_groups))
    def sampled(values):
        return np.bincount(groups, weights=values, minlength=n_groups)[draws].sum(axis=1)
    n = sampled(np.ones(len(rows)))
    stats, cases, values = {}, [dict(id=row["id"]) for row in rows], {}
    for arm in ARMS:
        stats[arm] = {}
        for user in USERS:
            threshold = policies[arm][user]
            labels = [decision(r, arm, threshold) for r in rows]
            grades = [judge(r, label) for r, label in zip(rows, labels)]
            record = summary(rows, labels)
            unsupported = np.array([g == "unsupported" for g in grades])
            released = np.array([g != "held" for g in grades])
            numerator, denominator = sampled(unsupported), sampled(released)
            risk = np.divide(numerator, denominator, out=np.full_like(n, np.nan), where=denominator > 0)
            record["error_fraction_interval"] = interval(risk)
            stats[arm][user] = record
            if user == "triage":
                values[arm] = released.astype(int) - 2*unsupported
            for case, label, grade in zip(cases, labels, grades):
                case[f"{arm}_{user}"] = [label, grade]
    diff = values["agreement"] - values["pool"]
    return dict(n=len(rows), paper_groups=int(n_groups), answerable=sum(r["answerable"] for r in rows),
                calls_per_arm=2*len(rows), tokens_per_arm=sum(sum(r["tokens"]) for r in rows),
                policies=policies, outcomes=stats, paired_delta_per_100=round(100*diff.mean(), 3),
                paired_interval=interval(100*sampled(diff)/n),
                cases=cases)


if __name__ == "__main__":
    lock = select(load("development"))
    if sys.argv[1:] == ["select"]:
        write("thresholds.json", lock)
    elif sys.argv[1:] == ["evaluate"]:
        if lock != json.loads((HERE / "thresholds.json").read_text()):
            raise ValueError("Threshold file differs from development selection")
        write("results.json", evaluate(load("reserved"), lock["policies"]))
    else:
        sys.exit("Use select or evaluate")
