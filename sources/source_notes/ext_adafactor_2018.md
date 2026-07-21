# Source Note: Adafactor: Adaptive Learning Rates with Sublinear Memory Cost

| Field | Value |
|---|---|
| Source ID | `ext_adafactor_2018` |
| Ingestion date | 2026-07-21 |
| Source | Shazeer and Stern, ICML 2018, https://proceedings.mlr.press/v80/shazeer18a.html |
| Ingestion basis | Primary mechanism, memory analysis, clipping remedies, and Transformer experiment reviewed. |

## Thesis and mechanism

Adafactor replaces a full per-parameter second-moment tensor for matrix weights
with row and column statistics used to construct a factored approximation. It
also introduces update clipping, a changing second-moment decay rule, and
parameter-scale-relative updates. Dropping first-moment state further reduces
auxiliary memory in the paper's main low-memory configuration.

## Evidence and limits

The paper reports comparable machine-translation results to a published Adam
regime while using much less auxiliary optimizer storage. Factorization is an
approximation, vector/scalar parameters need different handling, and the result
does not establish parity across architectures or objectives.

## Book use

Primary chapter: `governed-model-training-distributed-optimization-and-scaling`.

Use as the principal optimizer-state/memory alternative. Compare total memory,
stability, tuning, and time-to-quality rather than state bytes alone.
