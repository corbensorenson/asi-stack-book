"""Join retained arm decisions to bibliographic fields in the pinned SciFact-Open archive."""
import hashlib
import json
from pathlib import Path
import sys
import tarfile

HERE = Path(__file__).resolve().parent
ARCHIVE_SHA = "8f4dc238b2eff422bab5c7918fcbddb6996b29d37cb887942ef6ee1a16fb3415"


def extract(path):
    with path.open("rb") as stream:
        if hashlib.file_digest(stream, "sha256").hexdigest() != ARCHIVE_SHA:
            raise ValueError("Unexpected SciFact-Open archive")
    cases = json.loads((HERE/"cases.json").read_bytes())["cases"]
    ids = {r["id"] for r in cases}
    papers = {v["doc"] for r in cases for v in r["arms"].values()}
    with tarfile.open(path) as archive:
        def lines(name):
            return (json.loads(v) for v in archive.extractfile("data/"+name+".jsonl"))
        claims = {v["id"]:v for v in lines("claims") if v["id"] in ids}
        # Include known annotated alternatives even when every arm retrieved another paper.
        papers.update(int(p) for c in claims.values() for p in c["evidence"])
        docs = {v["doc_id"]:v for v in lines("corpus_candidates") if v["doc_id"] in papers}
    out = {}
    for case in cases:
        c = claims[case["id"]]
        selected = {v["doc"] for v in case["arms"].values()}
        doc_ids = sorted(selected | {int(k) for k in c["evidence"]})
        records = []
        for key in doc_ids:
            doc = docs.get(key, {})
            ann = c["evidence"].get(str(key))
            records.append(dict(id=key, title=doc.get("title", f"SciFact-Open document {key}"),
                url=f"https://api.semanticscholar.org/CorpusID:{key}", annotation=ann and {
                    k:ann[k] for k in ("provenance","label","sentences")}))
        out[str(c["id"])] = dict(claim=c["claim"], papers=records)
    return out


if __name__ == "__main__":
    print(json.dumps(extract(Path(sys.argv[1])),indent=2,ensure_ascii=False))
