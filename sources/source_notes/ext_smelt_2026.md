# SMELT: Scaling Laws for Compute-Matched MoE Looped Transformers

| Field | Value |
|---|---|
| Source ID | `ext_smelt_2026` |
| Publication | Wang et al. (2026). [Source version](https://arxiv.org/abs/2609.01343v1) |

## Thesis

Sparse expert routing changes the compute trade-off observed for dense recurrent models.

## Mechanisms

A sparse mixture-of-experts architecture repeats the middle half twice while balancing active work, parameter count and cache.

## Evidence

Across four scales the authors estimate 6.8–18.0 percent training FLOP savings on the fitted compute-optimal frontier.

## Failure Modes

A fitted sparse-model frontier cannot be imported as a dense inference speedup.

## Book Chapters Supported

- [Replaceable Cognitive Substrates: Beyond Transformer Monoculture](../../chapters/replaceable-cognitive-substrates-beyond-transformer-monoculture.qmd)

## Claims To Add Or Update

External comparison under the existing chapter support state.

## Open Questions

Does this trade-off persist at matched quality, latency and memory on the intended workload?
