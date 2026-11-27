# Dory1.0-4B: A Looped Normalized-GPT

| Field | Value |
|---|---|
| Source ID | `ext_dory_loop_budget_2026` |
| Publication | Fishman et al. (2026). [Source version](https://arxiv.org/abs/2611.03998v1) |

## Thesis

The best observed number of passes depends on the workload, even with the weights held fixed.

## Mechanisms

A normalized transformer reuses its middle block at different inference depths and retains the last loop’s decoding cache.

## Evidence

Base checkpoint Table 1 compares one, two, four, six and eight loops on fixed evaluations.

## Failure Modes

The base accuracy table gives no workload-specific latency or cost per accepted answer.

## Book Chapters Supported

- [Replaceable Cognitive Substrates: Beyond Transformer Monoculture](../../chapters/replaceable-cognitive-substrates-beyond-transformer-monoculture.qmd)
- [Fast Generation Architectures](../../chapters/fast-generation-architectures.qmd)
- [Governed Deliberation and Test-Time Scaling](../../chapters/governed-deliberation-and-test-time-scaling.qmd)

## Claims To Add Or Update

External comparison under the existing chapter support state.

## Open Questions

Does this trade-off persist at matched quality, latency and memory on the intended workload?
