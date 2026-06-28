# Source Note: Distilling the Knowledge in a Neural Network

| Field | Value |
|---|---|
| Source ID | `ext_knowledge_distillation_2015` |
| Source title | Distilling the Knowledge in a Neural Network |
| Ingestion date | 2026-06-28 |
| Source version / URL | arXiv:1503.02531, https://arxiv.org/abs/1503.02531 |
| Citation label | Hinton et al. (2015), Knowledge Distillation |
| Published / updated | 2015-03-09 / 2015-03-09 |
| DOI | 10.48550/arXiv.1503.02531 |
| Ingestion basis | Primary arXiv abstract and metadata inspected for the compression/representation literature queue; paper not vendored into this repository and no distillation experiment reproduced. |

## Thesis

Knowledge distillation belongs in the compactness, generate-verify-repair, artifact-compression, and resource-economics chapters as an external reference for transferring behavior from larger or ensemble models into smaller models. It helps the ASI Stack distinguish compression as behavior transfer from compression as proof of preserved reasoning, evidence use, or safety.

## Mechanisms

- Train a smaller student model using outputs or softened targets from a larger model or ensemble.
- Treat the teacher's distribution over classes as carrying useful information beyond hard labels.
- Use distillation to improve deployability or reduce runtime cost in the source setting.
- Compare compressed student behavior against teacher or ensemble behavior under the paper's tasks.

## Evidence

- The source reports distillation methods and evaluated results in the paper's own setting.
- This repository has not run teacher/student training, reproduced any distillation result, or measured preserved artifact utility.
- Use this source as compression vocabulary, not as evidence for CGS, RankFold, NeuralFold, or artifact compression.

## Failure Modes

- Distillation can transfer teacher errors, hidden biases, or brittle shortcuts.
- Smaller models can preserve headline metrics while losing rare-case behavior, calibration, provenance sensitivity, or safety-relevant refusals.
- Compression success on one task family does not prove general residual honesty.

## Book Chapters Supported

- `compact-generative-systems-and-residual-honesty` (Compact Generative Systems and Residual Honesty)
- `generate-verify-repair-compression` (Generate-Verify-Repair Compression)
- `rankfold-neuralfold-and-artifact-compression` (RankFold, NeuralFold, and Artifact Compression)
- `resource-economics-and-token-budgets` (Resource Economics and Token Budgets)

## Claims To Add Or Update

- Use this note to ground distillation as an external compression mechanism.
- Do not claim local distillation, teacher/student preservation, or benchmark reproduction.
- Keep support state at `argument` until a compression fixture, utility test, or accepted evidence transition exists.

## Open Questions

- Which ASI Stack claims would need rare-case retention tests before distillation could be trusted?
- How should residual ledgers record behavior lost during distillation?
- What artifact-compression benchmark would distinguish useful distillation from metric mimicry?
