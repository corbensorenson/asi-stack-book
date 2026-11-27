"""Collect frozen one-vs-three document decisions on previously unscored claims."""
import json
from pathlib import Path
import sys
import tarfile
import hashlib

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'scifact_citation_check'))
import predict as model

OPEN_SHA = '8f4dc238b2eff422bab5c7918fcbddb6996b29d37cb887942ef6ee1a16fb3415'


def collect(cache):
    model.inputs(cache)
    archive = cache / 'open.tar.gz'
    if not archive.exists():
        model.urlretrieve("https://scifact.s3.us-west-2.amazonaws.com/scifact-open/latest/scifact_open.tar.gz", archive)
    with archive.open('rb') as stream:
        if hashlib.file_digest(stream, 'sha256').hexdigest() != OPEN_SHA:
            raise ValueError('SciFact-Open archive differs')
    with tarfile.open(archive) as data:
        def read(name):
            return [json.loads(line) for line in data.extractfile('data/' + name + '.jsonl')]
        claims, meta, docs = read('claims'), read('claims_metadata'), read('corpus_candidates')
    docs = [d for d in docs if d['abstract']]
    earlier = json.loads((HERE.parent/'scifact_retrieval_followup/cases.json').read_text())['cases']
    ids = {170, 263} | {r['id'] for r in earlier}
    for split in ('development', 'reserved'):
        ids.update(json.loads(line)['id'] for line in (model.HERE/(split+'.jsonl')).read_text().splitlines())
    prior_docs = {d for r in earlier for d in r['group_docs']}
    groups = {m['id']: [m['source_doc_id'], *m['cited_doc_ids']] for m in meta}
    claims = [r for r in claims if r['id'] not in ids and prior_docs.isdisjoint(groups[r['id']])]
    if len(claims) != 213:
        raise ValueError('Fresh cohort changed')
    vec = TfidfVectorizer(stop_words='english', ngram_range=(1, 2), sublinear_tf=True)
    documents = vec.fit_transform(' '.join([d['title'], d['title'], *d['abstract']]) for d in docs)
    tokenizer = model.Tokenizer.from_file(str(cache/'tokenizer.json'))
    tokenizer.enable_truncation(max_length=256)
    opts = model.ort.SessionOptions()
    opts.intra_op_num_threads = 4
    session = model.ort.InferenceSession(str(cache/'model.onnx'), opts, providers=['CPUExecutionProvider'])
    rows = []
    for c in claims:
        query = vec.transform([c['claim']])
        ranked = np.argsort(-(documents @ query.T).toarray().ravel(), kind='stable')[:3]
        candidates = []
        for i in ranked:
            d = docs[i]
            sentences = d['abstract']
            sims = (vec.transform(sentences) @ query.T).toarray().ravel()
            cited = sorted(map(int, np.argsort(-sims, kind='stable')[:2]))
            context = sorted({j for k in cited for j in (k-1,k,k+1) if 0 <= j < len(sentences)})
            a, na = model.infer(' '.join([d['title'], *(sentences[j] for j in context)]), c['claim'], session, tokenizer)
            b, nb = model.infer(' '.join(sentences[j] for j in cited), c['claim'], session, tokenizer)
            candidates.append(dict(doc=d['doc_id'], cited=cited, scores=[a,b], tokens=[na,nb]))
        for candidate in candidates:
            candidate['annotation'] = c['evidence'].get(str(candidate['doc']))
        rows.append(dict(id=c['id'], group_docs=groups[c['id']], candidates=candidates))
    return dict(documents=len(docs), cases=rows)


if __name__ == '__main__':
    print(json.dumps(collect(Path(sys.argv[1])), indent=2))
