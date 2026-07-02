# Source Note: Better & Faster Large Language Models via Multi-token Prediction

| Field | Value |
|---|---|
| Source ID | `ext_multi_token_prediction_2024` |
| Source title | Better & Faster Large Language Models via Multi-token Prediction |
| Ingestion date | 2026-06-25 |
| Source version / URL | arXiv:2404.19737, https://arxiv.org/abs/2404.19737 |
| Ingestion basis | Public arXiv abstract and metadata inspected for the fast-generation literature queue; paper not vendored into this repository. |

## Thesis

Multi-token prediction trains a model to predict several future tokens from each position rather than only the next token. For this book, the important point is not a standalone speed claim; it is that future-token heads create a structured proposal surface that can be measured by accepted-token and task-success accounting.

## Mechanisms

- Add multiple independent future-token output heads on top of a shared model trunk.
- Use multi-token prediction as an auxiliary training objective.
- Evaluate both capability changes and inference-time acceleration when multiple predicted tokens can be accepted.
- Keep proposal count separate from accepted count.
- Treat the method as a training-time route to richer draft proposals, distinct from serving-only acceleration.

## Evidence

- The source reports downstream improvements and inference acceleration under its experimental setup.
- The repository has not trained or evaluated a multi-token-prediction model.
- Use the source to support a taxonomy row and test-plan item for MTP, not as local evidence that MTP improves this book's target workloads.

## Failure Modes

- Extra heads can predict plausible but unacceptable future tokens.
- Gains may depend on model size, domain, training recipe, and acceptance policy.
- Training-time improvements and inference-time speedups are different evidence types and should not be merged.
- Accepted-token accounting can hide quality regressions unless task success and verifier cost are recorded.

## Book Chapters Supported

- `fast-generation-architectures` (Fast Generation Architectures)
- `the-efficient-asi-hypothesis` (The Efficient ASI Hypothesis)

## Claims To Add Or Update

- Use this source to source-note multi-token prediction as a future-token drafting family.
- Keep ASI Stack treatment tied to governance records, verifier predicates, fallback, and measured accepted-output rates.
- Do not claim MTP has been implemented or benchmarked in this repository.

## Open Questions

- What acceptance predicate should distinguish a useful multi-token draft from a misleading continuation?
- Should MTP heads be modeled as part of a specialist core or as a generation-mode attribute?
- Which tasks are most sensitive to a mismatch between accepted token count and final artifact quality?
