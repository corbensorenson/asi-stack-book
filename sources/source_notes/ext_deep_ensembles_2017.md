# Source Note: Deep Ensembles

| Field | Value |
|---|---|
| Source ID | `ext_deep_ensembles_2017` |
| Source title | Simple and Scalable Predictive Uncertainty Estimation using Deep Ensembles |
| Ingestion date | 2026-07-24 |
| Source version / URL | NeurIPS 2017, https://papers.nips.cc/paper_files/paper/2017/hash/9ef2ed4b7fd2c810847ffa5fa85bce38-Abstract.html |
| Citation label | Lakshminarayanan, Pritzel, and Blundell (2017), Deep Ensembles |
| Published / updated | 2017-12-04 / 2017-12-04 |
| DOI | not assigned in the inspected record |
| Ingestion basis | Primary abstract and paper mechanism inspected; no ensemble, dataset, calibration, or OOD result reproduced. |

## Thesis

Independently trained probabilistic networks form a simple, strong empirical
baseline for predictive uncertainty. Ensemble disagreement can be useful
without becoming a calibrated ignorance oracle.

## Mechanisms

- Train multiple probabilistic networks with proper scoring rules.
- Aggregate predictive distributions.
- Evaluate calibration and responses to unknown distributions.

## Evidence

The paper reports competitive calibration and OOD uncertainty in its benchmark
settings. No result is reproduced locally and no distribution-free guarantee
follows.

## Failure Modes

- Ensemble members sharing data, architecture, and blind spots.
- Low disagreement under common-mode shift.
- Averaging suppressing rare but consequential hypotheses.
- Compute cost omitted from comparison.

## Book Chapters Supported

- `governed-world-models-and-reality-grounding`

## Claims To Add Or Update

- Deep ensembles should be a strong baseline for world-model uncertainty.
- Disagreement must be paired with shift and positive-control tests.

## Open Questions

- Which diversity interventions reduce common-mode error without unfair cost?
- When should disagreement trigger observation, abstention, or safe hold?
