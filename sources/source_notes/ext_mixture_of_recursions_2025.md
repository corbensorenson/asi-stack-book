# Mixture-of-Recursions: Learning Dynamic Recursive Depths for Adaptive Token-Level Computation

| Field | Value |
|---|---|
| Source ID | `ext_mixture_of_recursions_2025` |
| Publication | Bae et al. (2025). [Source version](https://arxiv.org/abs/2507.10524v1) |

## Thesis

Tokens in the same sequence can use different amounts of recurrent computation.

## Mechanisms

A lightweight router assigns individual tokens to further passes and changes the set of cached keys and values.

## Evidence

The authors compare selective caching and sharing first-recursion keys and values across recursion steps.

## Failure Modes

Throughput depends on the batch, implementation and quality target.

## Book Chapters Supported

- [Fast Generation Architectures](../../chapters/fast-generation-architectures.qmd)

## Claims To Add Or Update

External comparison under the existing chapter support state.

## Open Questions

Does this trade-off persist at matched quality, latency and memory on the intended workload?
