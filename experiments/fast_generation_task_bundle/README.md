# Fast Generation Task Bundle

This experiment contains a public-safe local task-bundle replay for the Fast
Generation chapter.

The bundle compares three deterministic routes:

- `route://autoregressive-reference`: a reference baseline route.
- `route://fast-template-verified`: a lower deterministic-cost route that still
  passes the same verifier checks and remains experimental.
- `route://latency-only-proxy`: a cheaper negative control that fails verifier,
  fallback, residual, and support-state boundaries.

Run:

```bash
python3 scripts/run_fast_generation_task_bundle.py --write-result
python3 scripts/validate_fast_generation_task_bundle.py
```

This is no model-speed or deployment claim. It does not reproduce speculative
decoding, MTP, diffusion, KV-cache, or serving benchmarks, and it does not
promote any chapter core claim or Appendix C support state.
