# Costed Route Resource Slice

This experiment records a bounded v1.0 non-infrastructure measured/replayed
slice for the ASI Stack release gate.

The slice uses public-safe synthetic route and budget records to test one
claim: a costed-route selector can reject a cheaper inadequate route, compare
against an adequate overkill baseline, and select the lowest-cost adequate
route only when resource-budget gates, verification, fallback, residual, and
non-claim boundaries are present.

It is not a model run, runtime router, scheduler, benchmark, economic result,
or deployed safety result.

## Command

```bash
python3 scripts/validate_costed_route_resource_slice.py
```

## Records

- Input: `experiments/costed_route_resource_slice/input/v1_0_costed_routes.json`
- Result: `experiments/costed_route_resource_slice/results/2026-06-29-local.json`
- Public summary: `docs/costed_route_resource_slice.md`
- Transition: `evidence_transitions/v1_0_measured/costed_route_resource_slice_synthetic_test_backed.json`
