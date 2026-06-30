# Source Note: GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers

| Field | Value |
|---|---|
| Source ID | `ext_gptq_2022` |
| Source title | GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers |
| Ingestion date | 2026-06-28 |
| Source version / URL | arXiv:2210.17323, https://arxiv.org/abs/2210.17323 |
| Citation label | Frantar et al. (2022), GPTQ |
| Published / updated | 2022-10-31 / 2023-03-06 |
| DOI | 10.48550/arXiv.2210.17323 |
| Ingestion basis | Primary arXiv abstract and metadata inspected for the compression/representation literature queue; paper not vendored into this repository and no quantization run reproduced. |

## Thesis

GPTQ belongs in the artifact-compression, generate-verify-repair, resource-economics, and fast-generation chapters as an external reference for post-training quantization of large generative transformers. It sharpens the ASI Stack distinction between memory-footprint improvement, speed/serving impact, and preserved model utility.

## Mechanisms

- Quantize pretrained transformer weights after training.
- Use approximate second-order information to reduce quantization error.
- Target large generative transformer models where full retraining is expensive.
- Report memory, accuracy, and speed tradeoffs in the source paper's evaluation.

## Evidence

- The source reports post-training quantization method and evaluated results in its own setting.
- This repository has not run GPTQ, quantized any model, measured perplexity or task performance, or recorded serving-cost changes.
- Use this source as external quantization vocabulary, not as local evidence for compression or resource claims.

## Failure Modes

- Quantization can preserve average metrics while degrading edge cases, long-context behavior, tool-use reliability, or calibrated uncertainty.
- Smaller memory footprint can be mistaken for useful-solution-per-second improvement without end-to-end serving measurement.
- Quantized artifacts need residual records for tasks where compression changes behavior.

## Book Chapters Supported

- `rankfold-neuralfold-and-artifact-compression` (RankFold, NeuralFold, and Artifact Compression)
- `compact-generative-systems-and-residual-honesty` (Compact Generative Systems: Generate, Verify, Repair, and Residual Honesty)
- `resource-economics-and-token-budgets` (Resource Economics and Token Budgets)
- `fast-generation-architectures` (Fast Generation Architectures)

## Claims To Add Or Update

- Use this note to ground post-training quantization as an external compression pathway.
- Do not claim local quantization, memory reduction, speed improvement, or utility preservation.
- Keep support state at `argument` until quantized artifacts, measurement scripts, and accepted evidence transitions exist.

## Open Questions

- What ASI Stack residual record should capture behavior changed by quantization?
- Which tasks should be rerun before a quantized artifact can replace an uncompressed route?
- How should resource economics account for memory savings versus quality or verification losses?
