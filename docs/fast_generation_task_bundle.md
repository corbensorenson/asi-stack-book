# Fast Generation Task Bundle

Generated result: `experiments/fast_generation_task_bundle/results/2026-07-02-local.json`

Validator: `python3 scripts/validate_fast_generation_task_bundle.py`

Runner: `python3 scripts/run_fast_generation_task_bundle.py --write-result`

No-promotion decision:
`evidence_transitions/v1_x_measured/fast_generation_task_bundle_no_change.json`

## What It Checks

This local public-safe task bundle compares a reference baseline, a verified
fast-template route, and a latency-only proxy route over four deterministic
text-to-receipt tasks. The validator recomputes deterministic outputs, verifier
outcomes, output digests, cost units, and useful-solution-per-cost accounting.

The selected route is `route://fast-template-verified`. It passes the same four
tasks as `route://autoregressive-reference` under lower deterministic cost
units. The cheaper `route://latency-only-proxy` is rejected because it fails
verifier, fallback, residual, and support-state boundaries.

Result ID: `fast_generation_task_bundle_2026_07_02_local`.

## Boundary

This is a no model-speed or deployment claim. The elapsed milliseconds in the
result are local run metadata; route selection uses deterministic cost units so
the result remains stable in validation. The bundle does not prove model
generation speed, useful-solution-per-second improvement for an AI model,
speculative decoding quality, MTP quality, diffusion quality, KV-cache
throughput, serving throughput, route-selector adequacy, model quality,
runtime behavior, or support-state promotion.

## Current Local Result

```text
Fast generation task-bundle validation passed: candidate 4/4 tasks at 264 cost units vs baseline 632; latency-only negative rejected at 176 cost units.
```

The result gives the Fast Generation chapter one public-safe task-bundle
accounting slice. The accepted no-promotion decision records that the slice
blocks model-speed, useful-solution-per-second model performance, serving
throughput, route-selector adequacy, benchmark, model-quality, deployed-routing,
and chapter-core promotion claims. It does not close the remaining real
benchmark blockers.
