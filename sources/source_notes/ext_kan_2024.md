# Source Note: KAN

| Field | Value |
|---|---|
| Source ID | `ext_kan_2024` |
| Source title | KAN: Kolmogorov-Arnold Networks |
| Ingestion date | 2026-07-15 |
| Source version / URL | arXiv:2404.19756, https://arxiv.org/abs/2404.19756 |
| Ingestion basis | Primary paper abstract and method/experiment sections reviewed; no reproduction. |

## Thesis

Kolmogorov-Arnold Networks place learnable univariate functions on edges rather
than using fixed node activations and scalar linear weights as in ordinary MLPs.

## Mechanisms

- Spline-parameterized univariate edge functions.
- Layer composition motivated by the Kolmogorov-Arnold representation theorem.
- Visualization, pruning, and symbolic/scientific examples.

## Evidence

The paper reports approximation and scientific-task demonstrations. No KAN has
been trained or evaluated in this repository.

## Failure Modes

- The representation theorem does not imply practical learning superiority.
- Spline evaluation and grid refinement can distort parameter/FLOP comparisons.
- Interpretability demonstrations may be low-dimensional and task-specific.

## Book Chapters Supported

- `replaceable-cognitive-substrates-beyond-transformer-monoculture`

## Claims To Add Or Update

- Treat KANs as components or narrow kernels, not presumed Transformer replacements.
- Require matched MLP baselines, wall time, memory, and task-regime reporting.

## Open Questions

- Which scientific or symbolic regimes produce durable matched-cost gains?
- Can KAN components scale inside larger routed or hybrid systems?
