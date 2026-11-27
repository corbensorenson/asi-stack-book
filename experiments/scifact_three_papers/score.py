"""Replay selection and score from retained model readings and annotations."""
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
LABELS = ('CONTRADICT', 'SUPPORT', 'NEUTRAL')


def decide(candidates):
    scored = [[a+b for a,b in zip(*c['scores'])] for c in candidates]
    rank = max(range(len(scored)), key=lambda i:max(scored[i][:2])-scored[i][2])
    c = candidates[rank]
    label = LABELS[max(range(3), key=scored[rank].__getitem__)]
    ann = c['annotation'] or {}
    complete = ann.get('provenance') == 'citation' and bool(ann['sentences']) and set(ann['sentences']) <= set(c['cited'])
    outcome = 'held' if label == 'NEUTRAL' else 'justified' if complete and ann['label'] == label else 'unsupported'
    return dict(outcome=outcome, verdict=label, rank=rank+1, doc=c['doc'], cited=c['cited'],
                readings=2*len(candidates), tokens=sum(sum(v['tokens']) for v in candidates))


def summarize(data):
    import numpy as np
    import sys
    from importlib.util import spec_from_file_location, module_from_spec
    spec = spec_from_file_location('paired_groups', HERE.parent/'scifact_retrieval_followup/score.py')
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    cases = data['cases']
    if len({r['id'] for r in cases}) != 213 or len(cases) != 213 or any(len(r['candidates']) != 3 for r in cases):
        raise ValueError('Incomplete paired cohort')
    groups = module.components(cases)
    rows = [dict(id=r['id'], arms={name:decide(r['candidates'][:k]) for name,k in [('first',1),('three',3)]}) for r in cases]
    totals = {}
    for name in ('first','three'):
        arms = [r['arms'][name] for r in rows]
        totals[name] = {s:sum(a['outcome']==s for a in arms) for s in ('justified','unsupported','held')}
        totals[name].update({s:sum(a[s] for a in arms) for s in ('tokens','readings')})
    gains = np.array([int(r['arms']['three']['outcome']=='justified')-int(r['arms']['first']['outcome']=='justified') for r in rows])
    n = int(groups.max())+1
    draws = np.random.default_rng(1742).integers(n,size=(5000,n))
    delta = 100*np.bincount(groups,weights=gains)[draws].sum(axis=1)/np.bincount(groups)[draws].sum(axis=1)
    return dict(n=len(rows), documents=data['documents'], groups=n, gained=int(sum(gains>0)), lost=int(sum(gains<0)),
                interval=np.percentile(delta,[2.5,97.5]).round(2).tolist(), totals=totals, cases=rows)


if __name__ == '__main__':
    print(json.dumps(summarize(json.loads((HERE/'observations.json').read_bytes())),indent=2))
