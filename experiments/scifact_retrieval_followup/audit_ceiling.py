"""Retrospective audit of certifiability at the original two-sentence budget."""
from collections import Counter
import json
from pathlib import Path
import sys

from run import load

HERE = Path(__file__).resolve().parent


def audit(cache):
    claims, _, docs = load(cache)
    docs = {d["doc_id"]: d for d in docs}
    saved = {r["id"]: r["arms"]["tfidf_tfidf"] for r in json.loads((HERE/"cases.json").read_text())["cases"]}
    cases = []
    for claim in claims:
        row = saved[claim["id"]]
        human = {int(p): e for p,e in claim["evidence"].items() if int(p) in docs and e["provenance"] == "citation"}
        fits = sorted(p for p,e in human.items() if 0 < len(e["sentences"]) <= 2)
        reason = "certifiable" if fits else "no eligible human paper" if not human else "no highlight set fits"
        evidence = claim["evidence"].get(str(row["doc"]))
        detail = None
        if row["outcome"] == "unsupported":
            if evidence is None:
                detail = "unjudged paper"
            elif evidence["provenance"] != "citation":
                detail = "pooled highlight"
            elif evidence["label"] != row["verdict"]:
                detail = "verdict mismatch"
            else:
                detail = "incomplete citation"
        cases.append(dict(id=claim["id"], ceiling=reason, possible_papers=fits, returned_human=row["doc"] in human,
                          returned_certifiable=row["doc"] in fits, complete=row["complete"], outcome=row["outcome"], reason=detail))
    return dict(ceiling=dict(Counter(r["ceiling"] for r in cases)),
                unsupported=dict(Counter(r["reason"] for r in cases if r["reason"])),
                stages={key:sum(r[key] for r in cases) for key in ("returned_human","returned_certifiable","complete")},
                justified=sum(r["outcome"]=="justified" for r in cases),cases=cases)


if __name__ == "__main__":
    print(json.dumps(audit(Path(sys.argv[1])), indent=2))
