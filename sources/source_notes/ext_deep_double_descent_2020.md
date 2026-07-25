# Source Note: Deep Double Descent

| Field | Value |
|---|---|
| Source ID | `ext_deep_double_descent_2020` |
| Source title | Deep Double Descent: Where Bigger Models and More Data Hurt |
| Source version / URL | <https://openreview.net/forum?id=-bJ_Hb7lCVH> |
| Ingestion date | 2026-07-24 |

## Thesis

Nakkiran and colleagues report model-wise, sample-wise, and epoch-wise
double-descent behavior and propose effective model complexity as a unifying
lens. Generalization may worsen near an interpolation threshold before
improving again.

## Mechanisms

- capacity, sample, and training-time sweeps;
- interpolation threshold identification;
- effective rather than nominal model complexity;
- matched train/test error curves across controlled configurations.

## Evidence

The result is empirical and bounded to the studied datasets, models,
optimizers, noise, and sweep procedures. It challenges one-dimensional
monotonic intuitions but does not establish a universal scaling law or predict
a particular frontier run.

## Failure Modes

- sparse sweeps hiding the peak;
- cherry-picked endpoints;
- nominal parameter count standing in for effective complexity;
- data or epoch changes confounded with architecture changes;
- a descriptive curve mistaken for a causal mechanism.

## Book Chapters Supported

- `learning-theory-generalization-and-scaling-science`

## Claims To Add Or Update

- Scaling claims should expose regime, sweep density, interpolation behavior,
  noise, uncertainty, and competing explanations.
- “More model, data, or training helps” is an empirical claim, not a default
  theorem for modern systems.

## Open Questions

- Which modern pretraining regimes exhibit analogous transitions?
- How should compute-optimal decisions account for non-monotonic regions?
- Can effective complexity be estimated prospectively?
