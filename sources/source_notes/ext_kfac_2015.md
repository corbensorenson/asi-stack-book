# Source Note: Optimizing Neural Networks with Kronecker-factored Approximate Curvature

| Field | Value |
|---|---|
| Source ID | `ext_kfac_2015` |
| Ingestion date | 2026-07-21 |
| Source | Martens and Grosse, ICML 2015, https://proceedings.mlr.press/v37/martens15.html |
| Ingestion basis | Primary Fisher approximation, Kronecker factorization, computational argument, and experiments reviewed. |

## Thesis

K-FAC approximates layer blocks of the Fisher information matrix as Kronecker
products of smaller factors. This makes a non-diagonal approximate natural-
gradient direction more tractable to store and invert than the exact matrix.

## Mechanisms

The comparison unit must bind the Fisher approximation, factor estimation,
damping, inversion cadence, block structure, distribution, and grafting policy.

## Evidence

The paper reports more progress per update than momentum SGD in studied
networks at several-times per-step computation. The factorization, damping,
statistics cadence, inversion method, architecture mapping, and distributed
implementation all affect whether that trade is favorable.

## Failure Modes

Approximation error, stale curvature, unstable damping, inversion cost, or
communication overhead can erase an apparent reduction in optimizer steps.

## Book Chapters Supported

Primary chapter: `governed-model-training-distributed-optimization-and-scaling`.

Use as the curvature/natural-gradient representative. It grounds an important
theoretical family but does not authorize calling a Fisher approximation exact
geometry or a reduction in steps a reduction in lifecycle cost.

## Claims To Add Or Update

- Treat K-FAC as a curvature-aware family, not exact natural gradient by default.
- Report wall time, memory, communication, stability, and quality together.

## Open Questions

- Which factorization and damping policies remain competent at foundation-model scale?
- When does curvature information repay its lifecycle and systems cost?
