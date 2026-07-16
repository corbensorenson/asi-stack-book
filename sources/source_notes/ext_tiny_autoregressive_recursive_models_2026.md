# Source Note: Tiny Autoregressive Recursive Models

| Field | Value |
|---|---|
| Source ID | `ext_tiny_autoregressive_recursive_models_2026` |
| Source title | Tiny Autoregressive Recursive Models |
| Ingestion date | 2026-07-15 |
| Source version / URL | arXiv:2603.08082v1; ICLR 2026 Workshop RSI Spotlight, https://arxiv.org/abs/2603.08082 |
| Ingestion basis | Primary paper abstract and controlled-comparison design reviewed; no experiment reproduced. |

## Thesis

When a standard autoregressive model is progressively transformed into a TRM-like
model under fixed block, token-stream, objective, and compute conditions, simpler
two-level refinement baselines can help but the full autoregressive TRM mechanism
shows no reliable advantage in the reported tasks.

## Mechanisms

- A staged architectural path from standard autoregression to TRM-style recurrence.
- Fixed block design, token stream, next-token objective, and compute-matched evaluation.
- Character-level algorithmic tasks that isolate refinement mechanisms.

## Evidence

The workshop paper reports no reliable advantage for the full Autoregressive TRM
architecture. This repository has not reproduced the models, seeds, tasks, or
statistics and does not generalize the negative result beyond its scope.

## Failure Modes

- Small character tasks may not expose benefits on other modalities or horizons.
- A null full-mechanism result may conceal a useful submechanism.
- Architecture labels can obscure the actual causal change between arms.

## Book Chapters Supported

- `replaceable-cognitive-substrates-beyond-transformer-monoculture`

## Claims To Add Or Update

- Use progressive mechanism ablations rather than Transformer-versus-OneCell labels alone.
- Preserve null results and qualify only the smallest causal mechanism that survives.

## Open Questions

- Which refinement component, if any, transfers to natural tasks?
- Can a preregistered stopping policy allocate recursion without post-hoc tuning?
