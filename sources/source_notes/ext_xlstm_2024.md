# Source Note: xLSTM

| Field | Value |
|---|---|
| Source ID | `ext_xlstm_2024` |
| Source title | xLSTM: Extended Long Short-Term Memory |
| Ingestion date | 2026-07-15 |
| Source version / URL | arXiv:2405.04517, https://arxiv.org/abs/2405.04517 |
| Ingestion basis | Primary paper abstract and architecture sections reviewed; no reproduction. |

## Thesis

xLSTM modernizes gated recurrent memory with revised cells intended to scale
recurrent language modeling.

## Mechanisms

- Exponential gating and stabilized recurrent updates.
- Scalar- and matrix-memory cell variants.
- Residual block composition for larger language models.

## Evidence

The source reports language-model comparisons. No local training, inference,
scaling, or extrapolation result exists.

## Failure Modes

- Gated memory can still forget or saturate.
- Matrix memory adds cost and opaque state.
- Fixed-depth training may not support useful unbounded recurrence.

## Book Chapters Supported

- `replaceable-cognitive-substrates-beyond-transformer-monoculture`

## Claims To Add Or Update

- Include modern gated recurrence beyond older RNN stereotypes.
- Test depth, length, and state-schema extrapolation under matched cost.

## Open Questions

- Does learned gating preserve exact obligations across long horizons?
- Can recurrent state be independently inspected or only behaviorally tested?
