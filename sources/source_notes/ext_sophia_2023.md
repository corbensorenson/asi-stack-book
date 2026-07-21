# Source Note: Sophia

| Field | Value |
|---|---|
| Source ID | `ext_sophia_2023` |
| Ingestion date | 2026-07-21 |
| Source | Liu et al., arXiv:2305.14342, https://arxiv.org/abs/2305.14342 |
| Ingestion basis | Primary diagonal-Hessian estimator, clipping rule, simplified theory, and GPT experiments reviewed. |

## Thesis and mechanism

Sophia maintains a momentum estimate of gradients and a periodically refreshed
diagonal curvature estimate, divides by that curvature proxy, and clips each
preconditioned coordinate. The curvature estimate is intentionally less
frequent than the parameter update to control average overhead.

## Evidence and limits

The source reports reaching matched language-model perplexity with roughly half
the steps, compute, and wall time of its Adam comparison for 125M--1.5B GPT
models. The theorem concerns a simplified setting, and the empirical result is
bound to its estimator, cadence, clipping, models, data, and tuning.

## Book use

Primary chapter: `governed-model-training-distributed-optimization-and-scaling`.

Use as the scalable curvature-aware representative. A fair implementation must
test estimator accuracy/cost, cadence, clipping sensitivity, and failure modes
rather than copying the method name with default settings.
