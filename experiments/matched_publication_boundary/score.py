"""Recompute counts and time summaries from every retained observation."""
import itertools
import json
from pathlib import Path
from statistics import median

HERE = Path(__file__).resolve().parent
ARMS = ("primary_only", "direct", "gateway")


def summarize(rows):
    totals = {}
    for name in ARMS:
        arms = [r["arms"][name] for r in rows]
        verified = [a for a in arms if a["closed"] and a["truth"]]
        totals[name] = dict(verified=len(verified), false_closures=sum(a["closed"] and not a["truth"] for a in arms),
                            unresolved=sum(not a["closed"] for a in arms),
                            **{k:sum(a[k] for a in arms) for k in ("caller_requests","requests","body_bytes")},
                            median_decision_us=round(median(a["elapsed_ns"] for a in arms)/1000, 1),
                            median_verified_us=round(median(a["elapsed_ns"] for a in verified)/1000, 1) if verified else None)
    return totals


def score(rows):
    digests = {item["repo"]: item["sha256"] for item in json.loads((HERE / "cohort.json").read_text())}
    tasks = list(digests)
    expected = set(itertools.product(tasks, ("exact","absent","wrong"), ("up","down"), ("shared","separate")))
    cells = [(r["task"],r["effect"],r["primary"],r["fallback"]) for r in rows]
    if len(cells) != len(expected) or set(cells) != expected:
        raise ValueError("Missing or duplicate cells")
    for row in rows:
        if set(row["arms"]) != set(ARMS) or any(a["truth"] != (row["effect"]=="exact") for a in row["arms"].values()):
            raise ValueError(row["id"])
        for name, arm in row["arms"].items():
            observed_closure = arm["status"] == 200 and arm["observed"] == digests[row["task"]]
            if arm["closed"] is not observed_closure:
                raise ValueError(f"{row['id']} / {name}: closure disagrees with HTTP status and expected digest")
    strata = {p+"-"+f:summarize([r for r in rows if r["primary"]==p and r["fallback"]==f])
              for p,f in itertools.product(("up","down"),("shared","separate"))}
    return dict(n=len(rows), totals=summarize(rows), strata=strata, cases=rows)


if __name__ == "__main__":
    print(json.dumps(score(json.loads((HERE / "observations.json").read_text())), indent=2))
