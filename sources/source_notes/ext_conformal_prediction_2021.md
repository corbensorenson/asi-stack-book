# Source Note: Conformal Prediction

| Field | Value |
|---|---|
| Source ID | `ext_conformal_prediction_2021` |
| Source title | A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification |
| Ingestion date | 2026-07-24 |
| Source version / URL | arXiv:2107.07511, https://arxiv.org/abs/2107.07511 |
| Citation label | Angelopoulos and Bates (2021), Conformal Prediction |
| Published / updated | 2021-07-15 / 2022-12-01 |
| DOI | 10.48550/arXiv.2107.07511 |
| Ingestion basis | Primary technical introduction and abstract inspected; no notebook, dataset, coverage test, or extension reproduced. |

## Thesis

Conformal prediction can wrap a predictor with finite-sample coverage
statements under explicit assumptions. Coverage is about a declared target and
population, not truth, causal adequacy, or safety.

## Mechanisms

- Reserve calibration data and define a nonconformity score.
- Construct prediction sets or intervals at a chosen coverage level.
- Extend the framework cautiously to shift, time series, structured outputs,
  and abstention.

## Evidence

The source provides theory, examples, and implementation guidance. This
repository has not validated coverage, exchangeability, or shifted extensions.

## Failure Modes

- Marginal coverage hiding subgroup or high-consequence misses.
- Exchangeability broken by time, policy, or adaptive data collection.
- Wide sets presented as useful certainty.
- Coverage target confused with semantic correctness.

## Book Chapters Supported

- `governed-world-models-and-reality-grounding`
- `readiness-gates-residual-escrow-and-quarantine`

## Claims To Add Or Update

- Every conformal receipt must bind target, score, calibration cohort,
  assumptions, and observed set utility.
- Broken assumptions route to residual rather than inherited coverage.

## Open Questions

- Which online or shift-aware variants are competent for a world-model stream?
- How should consequence-weighted errors coexist with marginal coverage?
