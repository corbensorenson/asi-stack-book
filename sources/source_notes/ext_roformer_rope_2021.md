# Source Note: RoFormer: Enhanced Transformer with Rotary Position Embedding

| Field | Value |
|---|---|
| Source ID | `ext_roformer_rope_2021` |
| Source title | RoFormer: Enhanced Transformer with Rotary Position Embedding |
| Ingestion date | 2026-06-29 |
| Source version / URL | arXiv:2104.09864, https://arxiv.org/abs/2104.09864 |
| Citation label | Su et al. (2021), RoFormer |
| Published / updated | 2021-04-20 / 2023-11-08 |
| DOI | 10.48550/arXiv.2104.09864 |
| Ingestion basis | Public arXiv abstract and metadata inspected for CoilRA/MultiCoil RoPE external positioning; paper not vendored into this repository and no model or benchmark reproduced. |

## Thesis

RoFormer is the primary external RoPE comparator for the CoilRA/MultiCoil RoPE chapter. It grounds rotary position embedding and relative-position behavior in an established Transformer variant while leaving CoilRA structural receipts, exact/discretized proof boundaries, and model-quality claims unpromoted.

## Mechanisms

- Encode absolute position through rotations.
- Incorporate relative-position dependency into self-attention.
- Compare RoPE against alternative position-encoding methods in Transformer language-model settings.
- Distinguish position-encoding mechanics from downstream quality, context-length, speed, memory, and deployment claims.

## Evidence

- The source reports experiments and theoretical analysis under its evaluated RoFormer setup.
- This repository has not reproduced RoFormer, RoPE experiments, position-encoding baselines, or long-context behavior.
- Use this source as an external RoPE baseline for cyclic phase and position-substrate discussion only.

## Failure Modes

- RoPE structural properties can be overclaimed as long-context quality.
- Numerical or finite receipt checks can be mistaken for full real-valued model behavior.
- Position encoding may interact with architecture, training data, length, and task distribution.
- A RoPE comparator does not validate CoilRA, MultiCoil RoPE, or cyclic mixer adoption.

## Book Chapters Supported

- `coilra-multicoil-rope-and-cyclic-mixers` (CoilRA, MultiCoil RoPE, and Cyclic Mixers)

## Claims To Add Or Update

- Use RoFormer as the source-noted RoPE baseline for cyclic position-encoding discussion.
- Keep exact/discretized RoPE receipts separate from real-valued RoPE behavior and model-quality evidence.
- Require ordinary RoPE, learned-position, recurrent, state-space, and adapter baselines before any CoilRA adoption claim.

## Open Questions

- Which RoPE receipt fields should be compared against ordinary RoPE implementations first?
- How should the book present exact finite phase-bank results without implying full RoPE deployment guarantees?
- What context-length workload would be fair for cyclic-positioning baselines?
