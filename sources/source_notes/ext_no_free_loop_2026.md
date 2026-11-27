# There Is No Free Loop: When Does Looping a Trained Model Pay for Its Inference Compute?

| Field | Value |
|---|---|
| Source ID | `ext_no_free_loop_2026` |
| Publication | Sukthanker et al. (2026). [Source version](https://arxiv.org/abs/2610.42030v1) |

## Thesis

A retrofit must earn the extra inference time against the original checkpoint and a compute-matched decoding policy.

## Mechanisms

Retrofit a pretrained decoder and compare with keeping it untied and with alternative uses of the same inference budget.

## Evidence

Only the 0.8B retrofit beat both references among the tested Qwen-family models.

## Failure Modes

Scale, tuning protocol and benchmark selection bound the result.

## Book Chapters Supported

- [Replaceable Cognitive Substrates: Beyond Transformer Monoculture](../../chapters/replaceable-cognitive-substrates-beyond-transformer-monoculture.qmd)

## Claims To Add Or Update

External comparison under the existing chapter support state.

## Open Questions

Does this trade-off persist at matched quality, latency and memory on the intended workload?
