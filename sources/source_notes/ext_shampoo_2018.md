# Source Note: Shampoo: Preconditioned Stochastic Tensor Optimization

| Field | Value |
|---|---|
| Source ID | `ext_shampoo_2018` |
| Ingestion date | 2026-07-21 |
| Source | Gupta, Koren, and Singer, ICML 2018, https://proceedings.mlr.press/v80/gupta18a.html |
| Ingestion basis | Primary tensor preconditioner, convex analysis, and reported runtime/optimization comparisons reviewed. |

## Thesis

Shampoo uses tensor structure instead of flattening every parameter. It
maintains a preconditioning matrix for each tensor dimension, contracting over
the others, as a tractable approximation to richer full-matrix adaptation.

## Mechanisms

The comparison unit must bind tensor blocking, statistics, inverse-root
approximation, grafting, update cadence, precision, distribution, and checkpoint state.

## Evidence

The paper proves convergence in a stochastic-convex setting and reports faster
convergence with per-step runtime comparable to common optimizers in studied
models. Modern large-model use adds inverse-root approximation, grafting,
blocking, update frequency, state precision, distribution, and communication
choices not settled by that result.

## Failure Modes

Poor blocking, stale or inaccurate roots, numerical instability, and
communication or checkpoint overhead can erase iteration-level gains.

## Book Chapters Supported

Primary chapter: `governed-model-training-distributed-optimization-and-scaling`.

Use as the foundational matrix/tensor-preconditioning family. The comparison
must count preconditioner computation, memory, communication, approximations,
and checkpoint state, not just optimizer steps.

## Claims To Add Or Update

- Use Shampoo as the foundational tensor-preconditioning family.
- Count computation, memory, communication, approximation, and recovery cost.

## Open Questions

- Which block and root policies remain stable and efficient across scale?
- When does preconditioning beat competent first-order baselines on time-to-quality?
