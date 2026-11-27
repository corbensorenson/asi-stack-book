"""Check retained positive witnesses against the pinned grammar and original specification."""
import argparse
from itertools import product
import json
from pathlib import Path

from report import summary
import run


def legal(tree, grammar):
    if isinstance(tree, str):
        return tree in grammar
    return (bool(tree) and (tree[0], *(["Start"] * (len(tree)-1))) in grammar
            and all(legal(child, grammar) for child in tree[1:]))


def verify(data, tasks):
    families = {f"hd-{n:02d}": family for family, ids in run.FAMILIES.items() for n in ids}
    expected = set(product(families, ("none", "whole", "routines"), ("handles", "expanded")))
    seen = set()
    for row in data["cases"]:
        key = row["task"], row["arm"], row["schedule"]
        where = " / ".join(key)
        if key not in expected or key in seen or row["family"] != families[key[0]]:
            raise ValueError(where + ": unexpected, duplicate or mislabeled cell")
        seen.add(key)
        if row["stop"] == "verified":
            args, target, grammar = tasks[key[0]]
            expr = row["solution"]
            try:
                trees = run.parse(expr) if isinstance(expr, str) else []
            except (IndexError, ValueError) as exc:
                raise ValueError(where + ": malformed witness") from exc
            if len(trees) != 1 or not legal(trees[0], grammar):
                raise ValueError(where + ": missing or illegal witness")
            if run.different(args, target, trees[0]) != "unsat":
                raise ValueError(where + ": universal check did not pass")
        elif row["stop"] not in ("proposal cap", "work cap") or row["solution"] is not None:
            raise ValueError(where + ": inconsistent stopping record")
    if expected - seen:
        raise ValueError("Missing cells: " + str(sorted(expected-seen)))
    return summary(data)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("cache", nargs="?", type=Path, default=run.HERE/"benchmarks")
    args = p.parse_args()
    data = json.loads((run.HERE/"results.json").read_bytes())
    print(json.dumps(verify(data, run.load(args.cache)), indent=2))
