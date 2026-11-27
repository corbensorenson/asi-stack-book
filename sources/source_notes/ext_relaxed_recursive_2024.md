# Relaxed Recursive Transformers: Effective Parameter Sharing with Layer-wise LoRA

| Field | Value |
|---|---|
| Source ID | `ext_relaxed_recursive_2024` |
| Publication | Bae et al. (2024). [Source version](https://arxiv.org/abs/2410.20672v1) |

## Thesis

Pass-specific low-rank changes offer an intermediate design between complete tying and separate weights at every depth.

## Mechanisms

A shared matrix plus small depth-specific low-rank updates lets individual passes specialize.

## Evidence

The authors convert an untied Gemma checkpoint and evaluate recovery after further training.

## Failure Modes

The proposed continuous depth-batching throughput gain was modeled.

## Book Chapters Supported

- [Replaceable Cognitive Substrates: Beyond Transformer Monoculture](../../chapters/replaceable-cognitive-substrates-beyond-transformer-monoculture.qmd)

## Claims To Add Or Update

External comparison under the existing chapter support state.

## Open Questions

Does this trade-off persist at matched quality, latency and memory on the intended workload?
