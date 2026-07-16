# Source Note: KAN or MLP: A Fairer Comparison

| Field | Value |
|---|---|
| Source ID | `ext_kan_or_mlp_fairer_comparison_2024` |
| Source title | KAN or MLP: A Fairer Comparison |
| Ingestion date | 2026-07-15 |
| Source version / URL | arXiv:2407.16674, https://arxiv.org/abs/2407.16674 |
| Ingestion basis | Primary comparison paper abstract and experimental design reviewed; no reproduction. |

## Thesis

KAN-versus-MLP conclusions depend strongly on how parameters, FLOPs, tasks, and
training settings are matched; architecture claims require fairer comparison.

## Mechanisms

- Match alternative resource views rather than one favorable size proxy.
- Compare across task regimes and training settings.
- Separate representational appeal from empirical efficiency.

## Evidence

The paper reports controlled comparisons under its selected tasks. The book has
not reproduced them and treats the paper as an objection, not a final verdict.

## Failure Modes

- Equal parameters can hide unequal FLOPs or wall time.
- Equal FLOPs can hide optimization and memory differences.
- A narrow benchmark suite can overgeneralize either positive or negative results.

## Book Chapters Supported

- `replaceable-cognitive-substrates-beyond-transformer-monoculture`

## Claims To Add Or Update

- Preregister equal-active-parameter and equal-total-lifecycle-cost views.
- Preserve task-specific wins without promoting general superiority.

## Open Questions

- Which matching rule best predicts deployment value across hardware?
- How should interpretability work be priced without turning it into a vague bonus?
