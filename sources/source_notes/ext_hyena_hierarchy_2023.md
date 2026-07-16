# Source Note: Hyena Hierarchy

| Field | Value |
|---|---|
| Source ID | `ext_hyena_hierarchy_2023` |
| Source title | Hyena Hierarchy: Towards Larger Convolutional Language Models |
| Ingestion date | 2026-07-15 |
| Source version / URL | arXiv:2302.10866, https://arxiv.org/abs/2302.10866 |
| Ingestion basis | Primary paper abstract and method/evaluation sections reviewed; no reproduction. |

## Thesis

Hyena replaces dense attention with a hierarchy of gated long convolutions and
offers a non-attention route to long-sequence mixing.

## Mechanisms

- Implicit long filters.
- Data-controlled gating and hierarchical recurrence of operators.
- Hardware-aware subquadratic sequence processing.

## Evidence

The paper reports language and long-context comparisons. No local model,
throughput, quality, or scaling result exists.

## Failure Modes

- Asymptotic advantage may not survive kernel and memory traffic costs.
- Long-range mixing does not guarantee selective recall or reasoning.
- Convolutional state may be difficult to migrate across implementations.

## Book Chapters Supported

- `replaceable-cognitive-substrates-beyond-transformer-monoculture`

## Claims To Add Or Update

- Include long convolution as a distinct ABI implementation family.
- Measure exact retrieval, distractor resistance, and total hardware cost.

## Open Questions

- Which task structures favor long filters over content-addressable attention?
- Can filters be checkpointed and migrated with explicit semantic guarantees?
