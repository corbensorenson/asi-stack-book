# Source Note: A tutorial introduction to the minimum description length principle

| Field | Value |
|---|---|
| Source ID | `ext_mdl_tutorial_2004` |
| Source title | A tutorial introduction to the minimum description length principle |
| Ingestion date | 2026-06-28 |
| Source version / URL | arXiv:math/0406077, https://arxiv.org/abs/math/0406077 |
| Citation label | Grunwald (2004), MDL Tutorial |
| Published / updated | 2004-06-04 / 2004-06-04 |
| DOI | 10.48550/arXiv.math/0406077 |
| Ingestion basis | Primary arXiv metadata and abstract inspected for the residual/error-accounting literature queue; no MDL implementation, dataset, or model-selection result is imported into this repository. |

## Thesis

The MDL tutorial belongs in the compression and benchmark chapters as an external reference for treating compression as a disciplined model-selection and residual-accounting problem. It helps the ASI Stack keep "shorter" separate from "better" unless the residual burden is recorded.

## Mechanisms

- Compare descriptions by the combined cost of model and data given the model.
- Penalize models that compress by hiding unexplained complexity.
- Use description length as an inductive-bias and model-selection discipline.
- Preserve the distinction between compact representation and remaining residual.

## Evidence

- The source explains the MDL principle and tutorial framing in its own mathematical scope.
- This repository has not implemented an MDL scorer, applied it to ASI Stack artifacts, or measured residual coding cost.
- Use the source as external description-length vocabulary, not as evidence for local compression correctness.

## Failure Modes

- Description-length scores can be treated as truth when the coding scheme encodes the wrong assumptions.
- Residual complexity can be pushed into external tools, prompts, human labor, or hidden benchmarks.
- A compact artifact can still fail downstream utility, authority, or evidence obligations.

## Book Chapters Supported

- `compact-generative-systems-and-residual-honesty` (Compact Generative Systems and Residual Honesty)
- `rankfold-neuralfold-and-artifact-compression` (RankFold, NeuralFold, and Artifact Compression)
- `benchmark-ratchets-and-anti-goodhart-evidence` (Benchmark Ratchets and Anti-Goodhart Evidence)

## Claims To Add Or Update

- Use this note to anchor residual honesty in model-plus-residual accounting vocabulary.
- Do not claim local MDL scoring, compression optimality, or benchmark adequacy.
- Keep support state at `argument` until local compression receipts or residual-cost tests exist.

## Open Questions

- What receipt fields should record model cost, residual cost, and downstream verification cost separately?
- Which benchmark ratchet should fail when a metric improves by moving burden into hidden residuals?
- Can a future artifact-compression harness compare residual burden across candidate encodings?
