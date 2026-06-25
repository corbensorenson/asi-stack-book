# Source Note: Large Language Diffusion Models

| Field | Value |
|---|---|
| Source ID | `ext_llada_2025` |
| Source title | Large Language Diffusion Models |
| Ingestion date | 2026-06-25 |
| Source version / URL | arXiv:2502.09992, https://arxiv.org/abs/2502.09992 |
| Ingestion basis | Public arXiv abstract and metadata inspected for the fast-generation literature queue; paper not vendored into this repository. |

## Thesis

LLaDA challenges the assumption that large language-model capability must be tied to left-to-right autoregression by presenting a masked-diffusion language model trained under a large-model pretraining and supervised fine-tuning paradigm. For this book, it source-notes diffusion LLMs as a real external family while preserving uncertainty about speed-quality tradeoffs.

## Mechanisms

- Use a forward masking process and reverse generation process for token prediction.
- Train a transformer to predict masked tokens under a diffusion-style process.
- Apply pretraining and supervised fine-tuning rather than only small-scale masked-model experiments.
- Generate by iterative refinement rather than strict next-token commitment.
- Compare diffusion language modeling against autoregressive assumptions in selected evaluations.

## Evidence

- The source reports capabilities for a large masked-diffusion language model.
- This repository has not run LLaDA, reproduced its training, or benchmarked diffusion generation against autoregressive baselines.
- Use the source to support diffusion LLMs as a source-noted generation family, not as proof that diffusion is faster or safer for this book's use cases.

## Failure Modes

- Parallel or arbitrary-order generation can still require many refinement steps.
- Quality, latency, and controllability can trade off differently from autoregressive decoding.
- Diffusion generation may complicate citation, ordering, and artifact-boundary verification.
- Claims about reversal, reasoning, or controllability should remain source-reported unless independently tested.

## Book Chapters Supported

- `fast-generation-architectures` (Fast Generation Architectures)

## Claims To Add Or Update

- Use this source to source-note large diffusion language models in the generation-mode taxonomy.
- Keep multi-seed diffusion and hybrid AR/diffusion ideas speculative until local tests or stronger source-specific mappings exist.
- Do not claim a diffusion LLM has been integrated into the ASI Stack.

## Open Questions

- How should a generation-mode record capture iterative denoising steps and partial span commitments?
- What verifier should evaluate non-left-to-right drafts before artifactization?
- Which tasks best expose whether diffusion-style generation improves useful solution per second?
