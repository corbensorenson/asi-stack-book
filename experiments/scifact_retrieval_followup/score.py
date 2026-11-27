"""Score the frozen cohort, retaining paired dependence and the compute boundary."""
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent


def components(cases):
    parent = {}
    def root(k):
        parent.setdefault(k, k)
        while parent[k] != k:
            parent[k] = parent[parent[k]]
            k = parent[k]
        return k
    for c in cases:
        docs = c["group_docs"]
        for doc in docs:
            parent[root(doc)] = root(docs[0])
    return np.unique([root(c["group_docs"][0]) for c in cases], return_inverse=True)[1]


def summarize(data):
    cases = data["cases"]
    groups = components(cases)
    size = int(groups.max()+1)
    draws = np.random.default_rng(1742).integers(size, size=(5000, size))
    def sample(values):
        return np.bincount(groups, weights=values, minlength=size)[draws].sum(axis=1)
    den = sample(np.ones(len(cases)))
    result = {}
    for key in cases[0]["arms"]:
        rows = [c["arms"][key] for c in cases]
        gains = np.array([int(r["outcome"] == "justified") - int(c["arms"]["tfidf_tfidf"]["outcome"] == "justified")
                          for c, r in zip(cases, rows)])
        result[key] = {f:sum(r[f] for r in rows) for f in
                       ["human_doc", "complete", "document_verdict", "tokens", "sentences_ranked"]}
        result[key].update({s:sum(r["outcome"]==s for r in rows) for s in ["justified","unsupported","held"]})
        result[key].update(gained=int((gains>0).sum()), lost=int((gains<0).sum()),
                           difference_per_100=round(100*gains.mean(), 2),
                           interval=np.percentile(100*sample(gains)/den, [2.5,97.5]).round(2).tolist())
    return dict(n=len(cases), groups=size, documents=data["documents"], readings_per_arm=2*len(cases), arms=result,
                cases=[{"id": c["id"], "arms": c["arms"]} for c in cases])


if __name__ == "__main__":
    print(json.dumps(summarize(json.loads((HERE/"cases.json").read_text())), indent=2))
