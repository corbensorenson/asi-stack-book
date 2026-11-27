# Lessons on Parameter Sharing across Layers in Transformers

| Field | Value |
|---|---|
| Source ID | `ext_layer_sharing_orders_2021` |
| Publication | Takase et al. (2021). [Source version](https://arxiv.org/abs/2104.06022v1) |

## Thesis

The order in which a finite set of layers is reused is an architectural choice.

## Mechanisms

Consecutive, cyclic and reversed reuse change which hidden state each block sees on its next visit.

## Evidence

Translation comparisons evaluate several ways to assign a fixed set of layers to depth positions.

## Failure Modes

The ranking depends on the translation setting and budget.

## Book Chapters Supported

- [Replaceable Cognitive Substrates: Beyond Transformer Monoculture](../../chapters/replaceable-cognitive-substrates-beyond-transformer-monoculture.qmd)

## Claims To Add Or Update

External comparison under the existing chapter support state.

## Open Questions

Does this trade-off persist at matched quality, latency and memory on the intended workload?
