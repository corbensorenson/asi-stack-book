"""Produce the four paired decisions; the upstream annotations never enter ranking."""
import hashlib
import json
from pathlib import Path
import sys
import tarfile
from urllib.request import urlretrieve

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

HERE = Path(__file__).resolve().parent
PREVIOUS = HERE.parent / "scifact_citation_check"
sys.path.insert(0, str(PREVIOUS))
import predict as verifier

OPEN_URL = "https://scifact.s3.us-west-2.amazonaws.com/scifact-open/latest/scifact_open.tar.gz"
OPEN_HASH = "8f4dc238b2eff422bab5c7918fcbddb6996b29d37cb887942ef6ee1a16fb3415"


def load(cache):
    verifier.inputs(cache)
    path = cache / "open.tar.gz"
    if not path.is_file():
        urlretrieve(OPEN_URL, path)
    with path.open("rb") as stream:
        if hashlib.file_digest(stream, "sha256").hexdigest() != OPEN_HASH:
            raise ValueError("SciFact-Open archive differs from the frozen release")
    with tarfile.open(path) as archive:
        def read(name):
            return [json.loads(line) for line in archive.extractfile(f"data/{name}.jsonl")]
        claims, metadata, docs = (read(n) for n in ("claims", "claims_metadata", "corpus_candidates"))
    prev = [json.loads(line) for fold in ("development", "reserved")
            for line in (PREVIOUS / (fold + ".jsonl")).read_text().splitlines()]
    seen = {i for r in prev for i in [*r["group_docs"], r["doc"]]}
    excluded = {r["id"] for r in prev} | {170, 263}
    meta = {r["id"]: r for r in metadata if seen.isdisjoint(r["cited_doc_ids"]) and r["id"] not in excluded}
    corpus = [d for d in docs if d["doc_id"] not in seen and d["abstract"]]
    return [c for c in claims if c["id"] in meta], meta, corpus


def bm_weights(counts, lengths, mean_length, idf):
    weights = counts.astype(float).tocsr()
    norm = np.repeat(1.2 * (.25 + .75 * lengths / mean_length), np.diff(weights.indptr))
    weights.data = idf[weights.indices] * (weights.data * 2.2) / (weights.data + norm)
    return weights


def scores(matrix, query):
    return (matrix @ query.T).toarray().ravel()


def run(cache):
    claims, meta, docs = load(cache)
    text = [" ".join([d["title"], d["title"], *d["abstract"]]) for d in docs]
    tfidf = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), sublinear_tf=True)
    cos_docs = tfidf.fit_transform(text)
    counts = CountVectorizer(analyzer=tfidf.build_analyzer(), vocabulary=tfidf.vocabulary_)
    doc_counts = counts.transform(text)
    idf = np.log1p((len(docs) - doc_counts.getnnz(axis=0) + .5) / (doc_counts.getnnz(axis=0) + .5))
    lengths = np.asarray(doc_counts.sum(axis=1)).ravel()
    bm_docs = bm_weights(doc_counts, lengths, lengths.mean(), idf)
    options = verifier.ort.SessionOptions()
    options.intra_op_num_threads = 4
    model = verifier.ort.InferenceSession(str(cache / "model.onnx"), options, providers=["CPUExecutionProvider"])
    tokenizer = verifier.Tokenizer.from_file(str(cache / "tokenizer.json"))
    tokenizer.enable_truncation(max_length=256)
    cases = []
    for c in claims:
        q = c["claim"]
        cosine_query = tfidf.transform([q])
        terms = counts.transform([q]).astype(float)
        terms.data[:] = 1
        selected_docs = {"tfidf": scores(cos_docs, cosine_query).argmax(), "bm25": scores(bm_docs, terms).argmax()}
        arms = {}
        for retrieval, index in selected_docs.items():
            d = docs[index]
            sentences = d["abstract"]
            original = np.argsort(-scores(tfidf.transform(sentences), cosine_query), kind="stable")[:2]
            sc = counts.transform(sentences)
            lens = np.asarray(sc.sum(axis=1)).ravel()
            bm = bm_weights(sc, lens, max(1, lens.mean()), idf)
            first = int(scores(bm, terms).argmax())
            complement = terms.copy()
            complement.data[np.isin(complement.indices, sc[first].indices)] = .5
            remaining = scores(bm, complement)
            remaining[first] = -np.inf
            diverse = [first, int(remaining.argmax())] if len(sentences) > 1 else [first]
            for selector, chosen in (("tfidf", original), ("coverage", diverse)):
                cited = sorted(map(int, chosen))
                around = sorted({j for i in cited for j in (i-1, i, i+1) if 0 <= j < len(sentences)})
                context = " ".join([d["title"], *(sentences[i] for i in around)])
                a, na = verifier.infer(context, q, model, tokenizer)
                b, nb = verifier.infer(" ".join(sentences[i] for i in cited), q, model, tokenizer)
                label = verifier.LABELS[np.argmax(np.array(a) + b)]
                evidence = c["evidence"].get(str(d["doc_id"]), {})
                human = evidence.get("provenance") == "citation"
                complete = human and bool(evidence["sentences"]) and set(evidence["sentences"]) <= set(cited)
                same = evidence.get("label") == label
                outcome = "held" if label == "NEUTRAL" else ("justified" if complete and same else "unsupported")
                arms[retrieval + "_" + selector] = dict(doc=d["doc_id"], cited=cited, verdict=label,
                    human_doc=human, complete=complete, document_verdict=same, outcome=outcome,
                    tokens=na+nb, sentences_ranked=len(sentences))
        m = meta[c["id"]]
        cases.append(dict(id=c["id"], group_docs=[m["source_doc_id"], *m["cited_doc_ids"]], arms=arms))
    return dict(documents=len(docs), cases=cases)


if __name__ == "__main__":
    print(json.dumps(run(Path(sys.argv[1])), indent=2))
