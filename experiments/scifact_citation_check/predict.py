"""Generate paired predictions with upstream data and model bytes checked by digest."""
import hashlib
import json
import sys
import tarfile
from pathlib import Path
from urllib.request import urlretrieve

import numpy as np
import onnxruntime as ort
from sklearn.feature_extraction.text import TfidfVectorizer
from tokenizers import Tokenizer

HERE = Path(__file__).resolve().parent
BASE = "https://huggingface.co/cross-encoder/nli-MiniLM2-L6-H768/resolve/b95119ce93d3e065de6214e38cd4a97b0f2f2c6d/"
INPUTS = {
    "data.tar.gz": ("https://scifact.s3-us-west-2.amazonaws.com/release/latest/data.tar.gz",
                    "11c621288d41ac144d29b13b0f8503b3820b7d6e8b1f6ff24dff335c196d76be"),
    "model.onnx": (BASE + "onnx/model_qint8_arm64.onnx",
                   "449024a8711a3e655cad410cb2192158f9897fc2a32b65dbb817922351150db7"),
    "tokenizer.json": (BASE + "tokenizer.json",
                       "82139106e603ee4e1d5bc99d056ccbed5a92bc24848b1b5a7137c26e00d0dbf6"),
}
LABELS = ["CONTRADICT", "SUPPORT", "NEUTRAL"]


def inputs(cache):
    cache.mkdir(exist_ok=True, parents=True)
    for name, (url, digest) in INPUTS.items():
        path = cache / name
        if not path.exists():
            urlretrieve(url, path)
        if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise ValueError(f"Unexpected {name} bytes. Supply the pinned input in {cache}.")


def partition(train, dev):
    excluded = set(next(c["cited_doc_ids"] for c in dev if c["id"] == 3))
    reserved = {doc for c in dev for doc in c["cited_doc_ids"]}
    return {
        "development": [c for c in train if reserved.isdisjoint(c["cited_doc_ids"])],
        "reserved": [c for c in dev if excluded.isdisjoint(c["cited_doc_ids"])],
    }


def infer(text, claim, model, tokenizer):
    encoded = tokenizer.encode(text, claim)
    ids = np.array([encoded.ids], dtype=np.int64)
    feed = {"input_ids": ids, "attention_mask": np.ones_like(ids)}
    logits = model.run(None, feed)[0][0].astype(float)
    probs = np.exp(logits - logits.max())
    return (probs / probs.sum()).round(7).tolist(), ids.size


def main(cache):
    inputs(cache)
    with tarfile.open(cache / "data.tar.gz") as archive:
        def read(name):
            return [json.loads(line) for line in archive.extractfile(f"data/{name}.jsonl")]
        corpus = read("corpus")
        splits = partition(read("claims_train"), read("claims_dev"))
    vec = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), sublinear_tf=True)
    abstracts = vec.fit_transform(" ".join([d["title"], d["title"], *d["abstract"]]) for d in corpus)
    tokenizer = Tokenizer.from_file(str(cache / "tokenizer.json"))
    tokenizer.enable_truncation(max_length=256)
    options = ort.SessionOptions()
    options.intra_op_num_threads = 4
    model = ort.InferenceSession(str(cache / "model.onnx"), options, providers=["CPUExecutionProvider"])
    for split, claims in splits.items():
        rows = []
        for claim in claims:
            text = claim["claim"]
            q = vec.transform([text])
            doc = corpus[int((abstracts @ q.T).toarray().argmax())]
            sentences = doc["abstract"]
            ranks = (vec.transform(sentences) @ q.T).toarray().ravel()
            cited = sorted(map(int, np.argsort(-ranks, kind="stable")[:2]))
            around = sorted({j for i in cited for j in (i-1, i, i+1) if 0 <= j < len(sentences)})
            context = " ".join([doc["title"], *(sentences[j] for j in around)])
            a, tokens_a = infer(context, text, model, tokenizer)
            b, tokens_b = infer(" ".join(sentences[j] for j in cited), text, model, tokenizer)
            observed = claim["evidence"].get(str(doc["doc_id"]), [])
            rows.append(dict(id=claim["id"], group_docs=claim["cited_doc_ids"], doc=doc["doc_id"],
                             cited=cited, evidence_here=observed, answerable=bool(claim["evidence"]),
                             context=a, citation=b, tokens=[tokens_a, tokens_b]))
        path = HERE / (split + ".jsonl")
        path.write_text("".join(json.dumps(row, separators=(",", ":")) + "\n" for row in rows))
        print(split, len(rows), flush=True)


if __name__ == "__main__":
    main(Path(sys.argv[1]))
