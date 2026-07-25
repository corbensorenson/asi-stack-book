# Source Note: Test-Time Training with Self-Supervision

| Field | Value |
|---|---|
| Source ID | `ext_test_time_training_2020` |
| Source title | Test-Time Training with Self-Supervision for Generalization under Distribution Shifts |
| Source version / URL | <https://proceedings.mlr.press/v119/sun20b.html> |
| Ingestion date | 2026-07-24 |

## Thesis

Sun and colleagues update model parameters on each test sample using a
self-supervised auxiliary objective and report improvements on studied image
corruption benchmarks. Inference can therefore contain a state-changing
learning loop.

## Mechanisms

- shared feature extractor with supervised and auxiliary heads;
- self-supervised loss evaluated on the current test input;
- bounded parameter update before task prediction;
- comparison with frozen and adaptation baselines.

## Evidence

The reported gains are limited to the studied image settings, corruptions,
architectures, objectives, and update rules. They do not establish safe
adaptation under arbitrary shift or transfer to language and agent systems.

## Failure Modes

- poisoning or adversarial inputs changing persistent state;
- auxiliary objective improving while target behavior degrades;
- order dependence and cross-user contamination;
- unlogged optimizer and RNG state;
- rollback that restores weights but not caches or descendants;
- latency and energy costs hidden from utility claims.

## Book Chapters Supported

- `governed-model-training-distributed-optimization-and-scaling`
- `replaceable-cognitive-substrates-beyond-transformer-monoculture`

## Claims To Add Or Update

- Test-time training is a governed update, not ordinary stateless inference;
  it needs state identity, authority, isolation, evaluation, rollback, expiry,
  and poisoning controls.
- Any benefit claim must compare frozen, adaptation, and no-update baselines
  while measuring safety, latency, resource cost, and contamination.

## Open Questions

- Which test-time states may persist across requests?
- How can updates be reverted effect-completely?
- When does self-supervision track the operational objective under shift?
