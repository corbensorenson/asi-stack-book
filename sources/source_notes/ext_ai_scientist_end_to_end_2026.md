# Source Note: Towards End-to-End Automation of AI Research

| Field | Value |
|---|---|
| Source ID | `ext_ai_scientist_end_to_end_2026` |
| Source title | Towards end-to-end automation of AI research |
| Ingestion date | 2026-08-13 |
| Source version / URL | Nature article and open-access PDF, https://www.nature.com/articles/s41586-026-10265-5 |
| Citation label | Lu et al. (2026), Towards end-to-end automation of AI research |
| Published | 2026-03-25 |
| DOI | 10.1038/s41586-026-10265-5 |
| Review state | Passage-reviewed external source for bounded computational research automation; no result has been reproduced locally and no support promotion follows. |
| Ingestion basis | Official Nature article and full open-access paper, including methods, workshop evaluation, limitations, and automated-review description. |

## Thesis

The paper presents an AI-research system that can connect idea generation,
literature search, code changes, experiments, analysis, manuscript production,
and automated review in a bounded machine-learning setting. It is useful here
because the apparently complete paper-production loop makes two hidden
denominators visible: the branches searched before the manuscript was selected
and the dependencies shared by generation and evaluation.

## Mechanisms

- A focused mode extends a supplied code template; a broader mode uses agentic
  tree search to construct and revise a research project.
- Agents search literature, alter code, run computational experiments, inspect
  results, make figures, and draft a manuscript.
- An automated reviewer aggregates five model-generated reviews into a
  meta-review and is compared with public OpenReview decisions.
- Workshop submission provides an institutional downstream observation, not a
  direct measurement of scientific truth.

## Evidence

The authors submitted three generated manuscripts under a preregistered
workshop protocol. One received a mean score of 6.33 and would probably have
been accepted at a workshop whose reported acceptance rate was 70 percent, but
the authors withdrew it as the protocol required. Their internal assessment
found none of the manuscripts met the main ICLR conference bar. The paper also
reports underdeveloped ideas, implementation errors, insufficient rigor,
duplicated figures, and inaccurate or hallucinated citations. These are
source-reported results from a computational machine-learning setting; this
repository has not rerun the system, reviewed the hidden search tree, or
independently assessed the manuscripts.

## Failure Modes

- Treating a polished manuscript or venue score as confirmation of its claims.
- Reporting only the selected paper while hiding generated ideas, failed code,
  abandoned branches, reviewer feedback, and selection policy.
- Counting several model reviews as independent when they share model families,
  training data, prompts, tools, or evaluator heuristics.
- Allowing automated review to optimize the generator against its own proxy.
- Generalizing a computational machine-learning workflow to physical science or
  scientific discovery in general.

## Book Chapters Supported

- `scientific-discovery-and-experimental-governance`
- Adjacent boundary owners: `planning-as-a-control-layer`,
  `benchmark-ratchets-and-anti-goodhart-evidence`, and
  `artifact-graphs-audit-logs-and-replay`

## Claims To Add Or Update

- Preserve candidate, branch, pruning, repair, compute, human-intervention, and
  selection denominators for end-to-end research agents.
- Represent reviewer independence as a dependency graph rather than a review
  count.
- Treat paper completion, review score, and acceptance as downstream
  observations whose relation to the paper's scientific claims must still be
  adjudicated.

## Open Questions

- Which search branches and failed experiments were unavailable to external
  reviewers, and how would their inclusion change appraisal?
- How should an evaluation remain informative when the generator can adapt to
  the same model-based reviewer?
- Which results survive independently implemented analysis and replication?
