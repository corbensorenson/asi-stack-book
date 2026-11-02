# Source Note: Self-Supervised Learning from Images with a Joint-Embedding Predictive Architecture

| Field | Value |
|---|---|
| Source ID | `ext_i_jepa_2023` |
| Ingestion date | 2026-11-02 |
| Primary version | [arXiv:2301.08243v3](https://arxiv.org/html/2301.08243v3) |
| Citation | Assran et al. (2023), I-JEPA |
| Published / updated | 2023-01-19 / 2023-04-13 |
| Review scope | Abstract; Section 3 (context, targets, predictor, masking and loss); reported evaluation framing. Selected primary HTML passages, not a full proof or empirical audit. |
| Custody | Public-safe authored note only; raw primary HTML remains in ignored local research cache. |

## Thesis
I-JEPA learns image representations by predicting target-block embeddings from visible context rather than reconstructing pixels.

## Mechanisms
Section 3 uses ViT context and target encoders, a positional predictor, large target blocks, and spatially informative context. The target encoder is updated by an exponential moving average; overlapping target patches are removed from visible context. Target selection and anti-collapse behavior are part of the recipe, not evidence that any masked prediction objective succeeds.

## Evidence
The paper reports image classification and other vision probes. This review did not execute its implementation or verify its reported timing.

## Failure Modes
A representation objective does not by itself provide an action-conditioned dynamics model, calibrated uncertainty, exact source reconstruction, or permission to act. I-JEPA's Transformer implementation also prevents treating JEPA as a mutually exclusive alternative to attention.

## Claims To Add Or Update
Distinguish prediction target, training recipe, sequence-mixing block, and consumer interface. Keep I-JEPA, action-conditioned V-JEPA 2, and LeJEPA's regularizer distinct.

## Open Questions
Which task-relevant information does the chosen masking/view policy retain or discard?

## Book Chapters Supported

- `governed-world-models-and-reality-grounding`
- `replaceable-cognitive-substrates-beyond-transformer-monoculture`

## Chapter Decision

Update existing owners through `new_paper_triage_scenarios/jepa_platonic_and_hnet_2026_11_02.json`. No new chapter, no claim-core promotion, no local model result.
