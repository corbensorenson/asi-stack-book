# Source Note: Optimizing Neural Networks with Kronecker-factored Approximate Curvature

| Field | Value |
|---|---|
| Source ID | `ext_kfac_2015` |
| Ingestion date | 2026-07-21 |
| Source | Martens and Grosse, ICML 2015, https://proceedings.mlr.press/v37/martens15.html |
| Ingestion basis | Primary Fisher approximation, Kronecker factorization, computational argument, and experiments reviewed. |

## Thesis and mechanism

K-FAC approximates layer blocks of the Fisher information matrix as Kronecker
products of smaller factors. This makes a non-diagonal approximate natural-
gradient direction more tractable to store and invert than the exact matrix.

## Evidence and limits

The paper reports more progress per update than momentum SGD in studied
networks at several-times per-step computation. The factorization, damping,
statistics cadence, inversion method, architecture mapping, and distributed
implementation all affect whether that trade is favorable.

## Book use

Primary chapter: `governed-model-training-distributed-optimization-and-scaling`.

Use as the curvature/natural-gradient representative. It grounds an important
theoretical family but does not authorize calling a Fisher approximation exact
geometry or a reduction in steps a reduction in lifecycle cost.
