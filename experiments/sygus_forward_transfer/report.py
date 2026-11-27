"""Aggregate retained observations without re-running timed searches."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def summary(data):
    cases = data["cases"]
    groups = {}
    if len({(r["task"],r["schedule"],r["arm"]) for r in cases}) != 66 or len(cases) != 66:
        raise ValueError("Incomplete or duplicated experiment")
    for r in cases:
        key = (r["family"], r["schedule"], r["arm"])
        group = groups.setdefault(key, dict(tasks=0, verified=0, exhausted=0, proposals=0,
                                             screen_ops=0, solver_checks=0, search_ns=0, verify_ns=0))
        group["tasks"] += 1
        group["verified"] += r["stop"] == "verified"
        group["exhausted"] += r["stop"].endswith("cap")
        for field in ("proposals","screen_ops","solver_checks","search_ns","verify_ns"):
            group[field] += r[field]
    return [dict(family=f, schedule=s, arm=a, **v) for (f,s,a),v in sorted(groups.items())]


if __name__ == "__main__":
    print(json.dumps(summary(json.loads((HERE/"results.json").read_bytes())), indent=2))
