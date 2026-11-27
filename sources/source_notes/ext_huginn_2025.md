# Scaling up Test-Time Compute with Latent Reasoning: A Recurrent Depth Approach

| Field | Value |
|---|---|
| Source ID | `ext_huginn_2025` |
| Publication | Geiping et al. (2025). [Source version](https://arxiv.org/abs/2502.05171v1) |

## Thesis

A language model can allocate more computation to a token by revisiting its hidden representation before decoding.

## Mechanisms

A recurrent core between input and output layers spends compute before producing the next token.

## Evidence

The authors trained a 3.5B checkpoint on 800B tokens and evaluated multiple inference depths.

## Failure Modes

Extra latent depth benefits selected tasks and costs another core execution.

## Book Chapters Supported

- [Replaceable Cognitive Substrates: Beyond Transformer Monoculture](../../chapters/replaceable-cognitive-substrates-beyond-transformer-monoculture.qmd)
- [Governed Deliberation and Test-Time Scaling](../../chapters/governed-deliberation-and-test-time-scaling.qmd)

## Claims To Add Or Update

External comparison under the existing chapter support state.

## Open Questions

Does this trade-off persist at matched quality, latency and memory on the intended workload?
