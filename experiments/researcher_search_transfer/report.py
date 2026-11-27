"""Score the first three distinct ordinary-search destinations against exact page sections."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = "/asi-stack-book/"
DESTINATIONS = {
    "reader-better-editor":"reader/chapters/unit-25-recursive-improvement-replication-and-containment.html",
    "run-fresh-citation-retrieval--case-833":"products/evidence-registry/study-citation-retrieval.html",
    "from-a-token-meter-to-an-answer-bill":"chapters/physical-compute-infrastructure-energy-and-environmental-constraints.html",
    "verifier-measurement-boundary":"chapters/stable-capability-fields.html",
}


def score(read):
    questions = json.loads(read("queries.json"))
    before, after = [json.loads(read(name+".json")) for name in ("before","after")]
    result = []
    for observation in (before, after):
        if [(r["query"],r["target"]) for r in observation["rows"]] != [tuple(q) for q in questions]:
            raise ValueError("Observation differs from reserved query set")
    for i, (question, anchor) in enumerate(questions):
        target = BASE+DESTINATIONS[anchor]+"#"+anchor
        row = {"query":question, "target":target}
        for label, observation in (("before",before),("after",after)):
            urls = observation["rows"][i]["links"]
            if len(urls) != len(set(urls)) or len(urls)>3:
                raise ValueError("Invalid result window")
            row[label] = urls.index(target)+1 if target in urls else 0
        result.append(row)
    return {"before_revision":before["revision"], "after_revision":after["revision"], "queries":result}


if __name__ == "__main__":
    print(json.dumps(score(lambda name:(HERE/name).read_bytes()),indent=2))
