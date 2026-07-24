# Source Note: Training Compute-Optimal Large Language Models

| Field | Value |
|---|---|
| Source ID | `ext_chinchilla_compute_optimal_2022` |
| Source title | Training Compute-Optimal Large Language Models |
| Ingestion date | 2026-07-24 |
| Source version / URL | arXiv:2203.15556, https://arxiv.org/abs/2203.15556 |
| Citation label | Hoffmann et al. (2022), Training Compute-Optimal Large Language Models |
| Published / updated | 2022-03-29 / 2022-03-29 |
| DOI | 10.48550/arXiv.2203.15556 |
| Ingestion basis | Primary abstract, reported run count, allocation result, and comparison inspected; no run, curve, checkpoint, or task result reproduced. |

## Thesis

Compute-efficient training depends on the allocation between model size and
training data. A smaller, better-trained model can dominate a larger,
undertrained one within the source's regime.

## Mechanisms

- Fit model-size and token-count scaling under a compute budget.
- Train and compare a predicted compute-optimal model.
- Evaluate downstream tasks and inference implications.

## Evidence

All training and downstream results are source-reported. The claimed allocation
does not automatically transfer across architecture, tokenizer, data quality,
optimizer, objectives, or hardware.

## Failure Modes

- Parameter count used as capability or efficiency identity.
- Source ratio copied without a current fit.
- Data quality, duplication, rights, and curriculum omitted from token counts.
- Training optimum confused with lifecycle optimum.

## Book Chapters Supported

- `the-efficient-asi-hypothesis`
- `governed-model-training-distributed-optimization-and-scaling`

## Claims To Add Or Update

- Compare complete lifecycle cost and quality, not parameters alone.
- Preserve the fitted regime and uncertainty with every compute allocation.

## Open Questions

- How should quality-adjusted tokens enter the scaling record?
- When do retrieval, distillation, routing, or recurrent substrates change the
  optimum?
