# How Much Is One Recurrence Worth? Iso-Depth Scaling Laws for Looped Language Models

| Field | Value |
|---|---|
| Source ID | `ext_loop_iso_depth_2026` |
| Publication | Schwethelm et al. (2026). [Source version](https://arxiv.org/abs/2604.21106v1) |

## Thesis

A recurrent model’s resident parameter count alone is a poor estimate of its training cost.

## Mechanisms

A dense iso-depth sweep separates resident parameter savings from the training computation needed to recover validation loss.

## Evidence

A four-pass 410M model matched a roughly 580M untied model at the training cost of a roughly 1B one.

## Failure Modes

The fitted recurrence exponent describes the sweep and its validation loss.

## Book Chapters Supported

- [Replaceable Cognitive Substrates: Beyond Transformer Monoculture](../../chapters/replaceable-cognitive-substrates-beyond-transformer-monoculture.qmd)

## Claims To Add Or Update

External comparison under the existing chapter support state.

## Open Questions

Does this trade-off persist at matched quality, latency and memory on the intended workload?
