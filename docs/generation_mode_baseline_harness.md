# Generation Mode Baseline Harness

Last updated: 2026-06-28

The eighth Phase 5 harness checks deterministic generation-mode and resource
budget accounting fixtures under `experiments/generation_mode_baselines/`.

## What It Checks

- All nested generation-mode and resource-budget records validate against their
  existing public schemas.
- A measured generation-mode record must carry run, baseline, and negative
  control evidence refs.
- Metric definitions must include useful-solution-per-second, quality, and
  residual accounting rather than latency alone.
- Failed or unmeasured quality cannot pass as an accepted generation result.
- Medium-or-higher non-autoregressive candidates must name fallback behavior.
- Generation-mode baseline fixtures cannot promote support state or release
  state.

## Command

```bash
python3 scripts/validate_generation_mode_baselines.py
```

## Current Local Result

The 2026-06-28 local run passed:

```text
Generation mode baseline harness passed: 2 valid fixture(s), 4 expected-invalid fixture(s).
```

The result record is
`experiments/generation_mode_baselines/results/2026-06-28-local.md`.

## Boundary

This is a deterministic empirical-accounting slice. It improves executable
evidence discipline because it catches missing baselines, latency-only proxy
use, failed-quality promotion, missing fallback behavior, and support-state
promotion attempts across existing protocol schemas.

It is not a model benchmark, speculative decoding run, diffusion model run,
KV-cache throughput measurement, routing result, useful-solution-per-second
claim, deployment result, or proof of AI behavior. It does not promote Appendix
C, prove source interpretation, prove proof adequacy, or validate runtime
behavior.
