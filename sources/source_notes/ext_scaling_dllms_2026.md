# Source Note: Scaling Beyond Masked Diffusion Language Models

| Field | Value |
|---|---|
| Source ID | `ext_scaling_dllms_2026` |
| Source title | Scaling Beyond Masked Diffusion Language Models |
| Ingestion date | 2026-06-25 |
| Source version / URL | arXiv:2602.15014, https://arxiv.org/abs/2602.15014 |
| Ingestion basis | Public arXiv abstract and metadata inspected for the fast-generation literature queue; paper not vendored into this repository. |

## Thesis

Scaling Beyond Masked Diffusion Language Models argues that diffusion language-model evaluation should consider speed-quality Pareto behavior, not only likelihood or perplexity. This maps directly to the ASI Stack's insistence that generation modes be compared by useful verified output under cost and verifier constraints.

## Mechanisms

- Compare multiple discrete diffusion families rather than treating masked diffusion as the only candidate.
- Study scaling under matched training compute.
- Separate perplexity from inference-time sampling behavior and speed-quality tradeoffs.
- Evaluate diffusion methods at larger parameter scale under the paper's setup.
- Report code and checkpoints through the project page according to the source.

## Evidence

- The source reports scaling-law and speed-quality comparisons for diffusion language-model families.
- This repository has not reviewed the released code, downloaded checkpoints, or reproduced any diffusion-language-model benchmark.
- Use the source to support a diffusion-evaluation warning: perplexity alone is insufficient for generation-mode adoption.

## Failure Modes

- A method can look better on likelihood while being worse on practical sampling cost.
- A method can look faster while requiring more verification, repair, or task-specific fallback.
- Reported Pareto behavior can depend on model scale, sampling schedule, benchmark choice, and hardware.
- Current diffusion literature remains active; the book should keep the taxonomy updateable.

## Book Chapters Supported

- `fast-generation-architectures` (Fast Generation Architectures)

## Claims To Add Or Update

- Use this source to strengthen the chapter's speed-quality accounting principle for diffusion LLMs.
- Keep support limited to external-literature context and test-plan design until local experiments exist.
- Do not use this note to claim diffusion language models are categorically superior to autoregressive models.

## Open Questions

- Should the book's first diffusion test compare fixed-step, confidence-based, and adaptive refinement schedules?
- What release-record fields should preserve sampling schedule, compute, verifier cost, and final task success?
- How often should the living book refresh this fast-moving literature queue?
