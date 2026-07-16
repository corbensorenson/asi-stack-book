# Source Note: Jamba

| Field | Value |
|---|---|
| Source ID | `ext_jamba_2024` |
| Source title | Jamba: A Hybrid Transformer-Mamba Language Model |
| Ingestion date | 2026-07-15 |
| Source version / URL | arXiv:2403.19887v2, https://arxiv.org/abs/2403.19887 |
| Ingestion basis | Primary preprint abstract and architecture descriptions reviewed; no reproduction. |

## Thesis

Jamba interleaves Transformer and Mamba layers and adds mixture-of-experts
capacity, making architecture composition itself a configurable design variable.

## Mechanisms

- Alternating attention and selective-state-space layers.
- Mixture-of-experts capacity with a smaller active-parameter footprint.
- Resource- and objective-specific choices about layer and expert composition.

## Evidence

The paper reports quality, context, throughput, and memory results for its
configuration. No local Jamba model, hybrid ablation, serving benchmark, or
hardware comparison exists.

## Failure Modes

- A hybrid can inherit both families' state, migration, and maintenance burdens.
- Active-parameter accounting can hide total parameters, routing, memory, and serving cost.
- One successful composition does not establish a universal mixture ratio.

## Book Chapters Supported

- `replaceable-cognitive-substrates-beyond-transformer-monoculture`

## Claims To Add Or Update

- Treat hybrids as first-class candidates rather than architecture-label exceptions.
- Require component, router, active/total parameter, and complete-cost ablations.

## Open Questions

- When is a hybrid causally better than routing whole tasks to separate kernels?
- How should mixed attention/recurrent checkpoints expose exact state and rollback?
