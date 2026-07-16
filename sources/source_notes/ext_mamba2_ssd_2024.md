# Source Note: Transformers are SSMs

| Field | Value |
|---|---|
| Source ID | `ext_mamba2_ssd_2024` |
| Source title | Transformers are SSMs: Generalized Models and Efficient Algorithms Through Structured State Space Duality |
| Ingestion date | 2026-07-15 |
| Source version / URL | arXiv:2405.21060, https://arxiv.org/abs/2405.21060 |
| Ingestion basis | Primary paper abstract and duality/architecture sections reviewed; no model reproduced. |

## Thesis

Structured state-space duality connects SSM and attention-like formulations and
supports a Mamba-2 architecture and efficient sequence algorithms.

## Mechanisms

- Structured state-space duality.
- Recurrent and matrix-oriented views of sequence computation.
- Hardware-aware implementation and revised Mamba blocks.

## Evidence

The source reports quality and efficiency comparisons. No local training,
kernel benchmark, or hardware result exists.

## Failure Modes

- Mathematical duality can be mistaken for implementation interchangeability.
- State compression can lose exact copying or tracking information.
- Kernel maturity and hardware fit can dominate nominal complexity.

## Book Chapters Supported

- `replaceable-cognitive-substrates-beyond-transformer-monoculture`

## Claims To Add Or Update

- Compare state semantics and hardware behavior, not architecture labels alone.
- Require exact state-tracking and copying stress tests.

## Open Questions

- Which ABI state can cross between attention and SSD implementations without loss?
- Where do dual formulations diverge in training stability or inference behavior?
