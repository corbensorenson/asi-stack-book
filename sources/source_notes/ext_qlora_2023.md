# Source Note: QLoRA: Efficient Finetuning of Quantized LLMs

| Field | Value |
|---|---|
| Source ID | `ext_qlora_2023` |
| Source title | QLoRA: Efficient Finetuning of Quantized LLMs |
| Ingestion date | 2026-06-28 |
| Source version / URL | arXiv:2305.14314, https://arxiv.org/abs/2305.14314 |
| Citation label | Dettmers et al. (2023), QLoRA |
| Published / updated | 2023-05-23 / 2023-05-30 |
| DOI | 10.48550/arXiv.2305.14314 |
| Ingestion basis | Primary arXiv abstract and metadata inspected for the compression/representation literature queue; paper not vendored into this repository and no QLoRA finetuning run reproduced. |

## Thesis

QLoRA belongs in the artifact-compression, resource-economics, policy-optimization, and prototype-roadmap chapters as an external reference for adapting quantized large language models with low-rank adapters. It helps the ASI Stack separate cheap adaptation, compressed storage, training memory, evaluation quality, and governance of updated capabilities.

## Mechanisms

- Backpropagate through a frozen quantized language model into low-rank adapters.
- Use memory-saving quantization and paging techniques to reduce finetuning requirements.
- Train instruction-following adapters in the source setting.
- Report benchmark and qualitative comparisons under the paper's evaluation assumptions.

## Evidence

- The source reports an efficient finetuning technique and evaluated model results.
- This repository has not run QLoRA, trained adapters, measured memory use, or reproduced benchmark comparisons.
- Use this source for quantized-adaptation vocabulary, not as evidence for local policy optimization, compression, or prototype feasibility.

## Failure Modes

- Efficient finetuning can create capability changes whose authority, provenance, and rollback status are unclear.
- Adapter success can be benchmark-specific and may not preserve refusal behavior, source discipline, or task-level reliability.
- Quantized-adapter workflows need release and evidence records before they can affect ASI Stack support states.

## Book Chapters Supported

- `rankfold-neuralfold-and-artifact-compression` (RankFold, NeuralFold, and Artifact Compression)
- `resource-economics-and-token-budgets` (Resource Economics and Token Budgets)
- `policy-optimization-and-learning-from-feedback` (Policy Optimization and Learning from Feedback)
- `prototype-roadmap` (Prototype Roadmap)

## Claims To Add Or Update

- Use this note to ground efficient quantized finetuning and low-rank adaptation boundaries.
- Do not claim local QLoRA training, memory savings, model-quality improvement, or policy-update success.
- Keep support state at `argument` until training logs, model artifacts, evaluation runs, and accepted evidence transitions exist.

## Open Questions

- What adapter-release record should connect quantized finetuning to authority ceilings and rollback?
- Which evaluation tasks would reveal adapter regressions relevant to ASI Stack governance?
- How should prototype sequencing distinguish cheap adaptation from safe or adequate adaptation?
