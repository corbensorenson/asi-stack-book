# Source Note: Associative-State Universal Transformers (UniMatrix)

| Field | Value |
|---|---|
| Source ID | `ext_unimatrix_2026` |
| Source title | Associative-State Universal Transformers: Sparse Retrieval Meets Structured Recurrence |
| Ingestion date | 2026-07-15 |
| Source version / URL | arXiv:2604.25930v1, https://arxiv.org/abs/2604.25930 |
| Ingestion basis | Primary preprint abstract and reported associative-recall ablations reviewed; no code or result reproduced. |

## Thesis

Compressed structured recurrence alone fails exact associative lookup in the
reported small-scale setup, while sufficient sparse slots and direct
pointer-level routing materially change the result.

## Mechanisms

- Shared Universal-Transformer-style recurrent block.
- Structured recurrent state and residual update variants.
- Sparse slot routing and direct pointer-logit fusion in the successful recall variant.

## Evidence

The source reports near-chance recall for the original UniMatrix family while
its Transformer control reaches 25.4 percent, then reports 75.6 percent and a
99.2-percent no-dropout follow-up for a sparse-pointer variant. These exact
figures remain source-reported and unreproduced.

## Failure Modes

- A small byte-level and synthetic setup may not transfer to larger models or natural tasks.
- Pointer routing can act as a privileged task-specific retrieval path.
- Parameter efficiency can hide slot capacity, routing, and output-fusion cost.

## Book Chapters Supported

- `replaceable-cognitive-substrates-beyond-transformer-monoculture`

## Claims To Add Or Update

- Separate recurrent computation from addressable retrieval capacity.
- Include exact-pointer, sparse-slot, and no-pointer controls in OneCell memory tests.

## Open Questions

- Which retrieval interface generalizes without embedding the benchmark's answer format?
- How should sparse slots expose custody, migration, revocation, and rollback?
