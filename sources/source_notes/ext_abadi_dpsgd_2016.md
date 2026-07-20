# Source Note: Deep Learning with Differential Privacy

| Field | Value |
|---|---|
| Source ID | `ext_abadi_dpsgd_2016` |
| Source title | Deep Learning with Differential Privacy |
| Ingestion date | 2026-07-19 |
| Source version / URL | CCS 2016, https://arxiv.org/abs/1607.00133 |
| Citation label | Abadi et al. (2016), Deep Learning with Differential Privacy |
| Published / updated | 2016-07-01 / 2016-10-24 |
| DOI | 10.1145/2976749.2978318 |
| Review state | Paper-body reviewed. |
| Ingestion basis | Abstract; Sections 2--4 on DP-SGD, clipping/noise, privacy accounting, and experiments. Code was not run. |

## Thesis

Per-example gradient clipping, calibrated noise, sampling, and accounting can
train deep networks with a quantified participation-privacy bound and utility
tradeoff under explicit assumptions.

## Mechanisms

- Clip per-example gradients, add Gaussian noise, sample, and compose privacy
  loss with the moments accountant.

## Evidence

The paper supplies an algorithm, analysis, and source-reported experiments.
They are not locally reproduced, and the guarantee depends on its declared
unit, adjacency, parameters, accountant, implementation, and release surface.

## Failure Modes

- Incorrect clipping, sampling, noise, accountant, or composition.
- Treating DP as purpose limitation, deletion, fairness, or compliance.

## Book Chapters Supported

- `privacy-data-rights-and-information-flow-governance`
- Boundary: `governed-model-training-distributed-optimization-and-scaling`

## Claims To Add Or Update

- Require unit, adjacency, clipping, noise, sampling, accountant, composition,
  and utility cost to travel with a DP claim.

## Open Questions

- How should accounting compose across training, memory, retrieval, and audit?
- Which empirical audits best complement the formal bound?
