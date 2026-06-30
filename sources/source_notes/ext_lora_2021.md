# Source Note: LoRA: Low-Rank Adaptation of Large Language Models

| Field | Value |
|---|---|
| Source ID | `ext_lora_2021` |
| Source title | LoRA: Low-Rank Adaptation of Large Language Models |
| Ingestion date | 2026-06-28 |
| Source version / URL | arXiv:2106.09685, https://arxiv.org/abs/2106.09685 |
| Citation label | Hu et al. (2021), LoRA |
| Published / updated | 2021-06-17 / 2021-10-16 |
| DOI | 10.48550/arXiv.2106.09685 |
| Ingestion basis | Primary arXiv abstract and metadata inspected for the compression/representation literature queue; paper not vendored into this repository and no adaptation result reproduced. |

## Thesis

LoRA belongs in the representation and resource chapters as an external reference for low-rank adaptation. It gives the ASI Stack a concrete comparison point for parameter-efficient updates without claiming local model improvement.

## Mechanisms

- Freeze pretrained model weights.
- Inject trainable low-rank matrices into Transformer layers.
- Reduce trainable parameters and GPU memory for downstream adaptation.
- Preserve inference-latency boundaries compared with some adapter methods in the source framing.

## Evidence

- The source reports parameter, memory, throughput, and model-quality comparisons in its experiments.
- This repository has not reproduced the implementation, datasets, baselines, or model-quality results.
- Use it as external literature for low-rank update vocabulary, not as evidence for RankFold, NeuralFold, or ASI Stack policy updates.

## Failure Modes

- Parameter efficiency can be mistaken for representation adequacy.
- Adaptation quality can fail outside evaluated tasks.
- Low-rank updates still need provenance, rollback, and authority boundaries.

## Book Chapters Supported

- `rankfold-neuralfold-and-artifact-compression` (RankFold, NeuralFold, and Artifact Compression)
- `compact-generative-systems-and-residual-honesty` (Compact Generative Systems: Generate, Verify, Repair, and Residual Honesty)
- `resource-economics-and-token-budgets` (Resource Economics and Token Budgets)
- `policy-optimization-and-learning-from-feedback` (Policy Optimization and Learning from Feedback)
- `coilra-multicoil-rope-and-cyclic-mixers` (CoilRA, MultiCoil RoPE, and Cyclic Mixers)

## Claims To Add Or Update

- Use this note to compare low-rank adaptation with book-specific compression and representation proposals.
- Use this note as one adapter baseline family for cyclic adapter and CoilRA adoption discussions.
- Do not claim LoRA reproduction or local adaptation quality.
- Keep support state at `argument` until local artifacts or accepted transitions exist.

## Open Questions

- Which representation record should capture low-rank update provenance and rollback?
- How should low-rank adapters be treated in capability replacement?
- What tests distinguish lower update cost from preserved behavior?
