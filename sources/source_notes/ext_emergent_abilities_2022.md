# Source Note: Emergent Abilities of Large Language Models

| Field | Value |
|---|---|
| Source ID | `ext_emergent_abilities_2022` |
| Source title | Emergent Abilities of Large Language Models |
| Ingestion date | 2026-07-24 |
| Source version / URL | arXiv:2206.07682, https://arxiv.org/abs/2206.07682 |
| Citation label | Wei et al. (2022), Emergent Abilities of Large Language Models |
| Published / updated | 2022-06-15 / 2022-06-15 |
| DOI | 10.48550/arXiv.2206.07682 |
| Ingestion basis | Primary abstract and definition inspected; no model family, prompt, task, or threshold reproduced. |

## Thesis

Some task metrics in studied language-model families appear only above a scale
threshold. Whether this reflects an underlying discontinuity, measurement
resolution, prompting, loss level, or another cause requires separate analysis.

## Mechanisms

- Define emergence relative to smaller and larger models on a task.
- Catalogue reported capability transitions.
- Motivate monitoring around scale and training changes.

## Evidence

This repository has not reproduced the reported transitions. The paper is one
side of an active measurement debate and is paired here with a metric-based
critique.

## Failure Modes

- Retrospective threshold selection.
- Discrete metrics hiding continuous improvement.
- Prompt and contamination differences.
- A capability threshold generalized across model families.

## Book Chapters Supported

- `the-efficient-asi-hypothesis`
- `capability-thresholds-and-deployment-commitments`

## Claims To Add Or Update

- Threshold governance needs continuous metrics and prospective break tests.
- Observed emergence does not identify mechanism or predict the next threshold.

## Open Questions

- Which thresholds survive alternative scoring and loss-based analysis?
- How should sudden risk-relevant behavior alter run-time stop rules?
