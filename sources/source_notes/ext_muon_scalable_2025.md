# Source Note: Muon is Scalable for LLM Training

| Field | Value |
|---|---|
| Source ID | `ext_muon_scalable_2025` |
| Ingestion date | 2026-07-21 |
| Source | Liu et al., arXiv:2502.16982, https://arxiv.org/abs/2502.16982 |
| Ingestion basis | Primary algorithm/scaling sections, distributed design, scaling-law comparison, and Moonlight report reviewed; code and checkpoints not reproduced. |

## Thesis

Muon applies momentum and then approximately orthogonalizes eligible matrix
updates, commonly using Newton--Schulz iterations. The paper argues that weight
decay and per-parameter update scaling are necessary to extend the method to
large language models, and supplies a distributed implementation. Non-matrix
parameters require an explicitly declared fallback policy.

## Mechanisms

The comparison unit must bind matrix selection, orthogonalization algorithm and
iterations, scaling, momentum, decay, precision, distribution, and fallback.

## Evidence

The paper reports about twofold compute efficiency relative to AdamW in its
compute-optimal scaling study and describes a 3B/16B MoE trained on 5.7T tokens.
Those are source-reported results. Matrix eligibility, transpose conventions,
orthogonalization coefficients/iterations, update scaling, fallback optimizer,
decay, communication, and tuning are all part of Muon's executable identity.

## Failure Modes

Naive Newton--Schulz settings, unmatched parameter groups, weak AdamW tuning,
or uncounted communication can create a false positive or false negative.

## Book Chapters Supported

Primary chapter: `governed-model-training-distributed-optimization-and-scaling`.

Use as the main modern orthogonalized-matrix case. A naive implementation or
unmatched AdamW baseline cannot support a Muon negative or positive claim.

## Claims To Add Or Update

- Use scalable Muon as the main modern orthogonalized-matrix comparator.
- Require competent implementations and equal tuning/resource envelopes.

## Open Questions

- Which matrix shapes and scales benefit after total systems cost is counted?
- How sensitive are results to orthogonalization accuracy and distributed topology?
