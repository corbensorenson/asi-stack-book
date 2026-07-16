# Source Note: Mamba: Linear-Time Sequence Modeling with Selective State Spaces

| Field | Value |
|---|---|
| Source ID | `ext_mamba_2023` |
| Source title | Mamba: Linear-Time Sequence Modeling with Selective State Spaces |
| Ingestion date | 2026-06-25 |
| Source version / URL | arXiv:2312.00752, https://arxiv.org/abs/2312.00752 |
| Ingestion basis | Public arXiv abstract and metadata inspected for the fast-generation and substrate literature queues; paper not vendored into this repository. |

## Thesis

Mamba proposes selective state-space sequence modeling as an efficient alternative backbone for long sequences. For the ASI Stack, it belongs in fast generation only as a substrate axis: changing the sequence model can change inference and long-context economics, but it is not the same as draft-token acceleration.

## Mechanisms

- Use input-dependent selective state-space parameters.
- Provide a hardware-aware parallel algorithm for recurrent-mode computation.
- Aim for linear scaling in sequence length rather than quadratic attention cost.
- Evaluate across sequence modalities and language-model settings.
- Separate backbone efficiency from generation-mode acceptance accounting.

## Evidence

- The source reports throughput, scaling, and benchmark comparisons under its evaluated setup.
- This repository has not trained, served, or benchmarked a Mamba model.
- Use the source to support the state-space/recurrent alternatives row and substrate taxonomy, not local performance claims.

## Failure Modes

- Backbone efficiency does not automatically imply better governed output or easier verification.
- Comparisons to transformers depend on training budget, data, model size, tasks, and implementation maturity.
- Long-context scaling claims need separate adequacy, retrieval, memory, and downstream-quality tests.
- State-space routes should not be conflated with speculative or MTP acceptance mechanisms.

## Book Chapters Supported

- `fast-generation-architectures` (Fast Generation Architectures)
- `mathematical-and-search-substrates` (Mathematical and Search Substrates)
- `coilra-multicoil-rope-and-cyclic-mixers` (CoilRA, MultiCoil RoPE, and Cyclic Mixers)
- `replaceable-cognitive-substrates-beyond-transformer-monoculture` (Replaceable Cognitive Substrates: Beyond Transformer Monoculture)

## Claims To Add Or Update

- Use this source to source-note state-space sequence models as a distinct speed/sequence substrate.
- Keep generation-mode records clear about whether speed comes from backbone choice or decoding acceptance.
- Use this source in mathematical/search substrates to keep backbone-efficiency claims separate from substrate adoption, verifier adequacy, and downstream quality claims.
- Use this source in cyclic-mixer positioning as a state-space baseline family that cyclic substrates must compare against before adoption.
- Do not claim Mamba-like substrates are adopted into the ASI Stack without A/B tests and governance gates.

## Open Questions

- Should substrate choices be represented in the same generation-mode record or a separate specialist-core record?
- Which long-context tasks would reveal verifier adequacy differences between attention and state-space models?
- What fallback should be required before routing high-risk tasks to a non-transformer sequence substrate?
