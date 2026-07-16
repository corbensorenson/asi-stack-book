# Source Note: Mamba-3

| Field | Value |
|---|---|
| Source ID | `ext_mamba3_2026` |
| Source title | Mamba-3: Improved Sequence Modeling using State Space Principles |
| Ingestion date | 2026-07-15 |
| Source version / URL | arXiv:2603.15569v1 (submitted 2026-03-16), https://arxiv.org/abs/2603.15569 |
| Ingestion basis | Current primary preprint abstract and architecture descriptions reviewed; no reproduction. |

## Thesis

Mamba-3 revisits selective state-space design through revised discretization,
complex-valued state updates, and multi-input/multi-output formulation.

## Mechanisms

- Selective recurrent state-space updates.
- Complex-valued state representation and improved discretization.
- MIMO state-space structure and hardware-oriented kernels.

## Evidence

The preprint reports architecture and benchmark results under its own setup.
The repository has no Mamba-3 training or inference evidence.

## Failure Modes

- Recency bias can promote an architecture before independent reproduction.
- Complex state can complicate migration, interpretation, and recovery.
- Reported efficiency may depend on specialized kernels and hardware.

## Book Chapters Supported

- `replaceable-cognitive-substrates-beyond-transformer-monoculture`

## Claims To Add Or Update

- Keep the taxonomy current while refusing recency-based promotion.
- Include state-schema and checkpoint-adapter costs in comparison.

## Open Questions

- Do the reported gains transfer across modalities and hardware?
- What exact recovery guarantees can a complex recurrent state expose?
