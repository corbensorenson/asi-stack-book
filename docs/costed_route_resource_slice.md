# Costed Route Resource Slice

Date: 2026-06-29

This record documents the first non-infrastructure v1.0 measured/replayed
slice accepted by the book's evidence system. It is intentionally narrow: it
supports only a bounded costed-route/resource-budget selection claim over a
tracked public-safe synthetic input record.

It does not support ASI capability, deployed routing, scheduler quality,
runtime enforcement, model quality, benchmark performance, source
interpretation, safety, or any chapter core claim.

## Accepted Narrow Claim

Claim ID: `resource-economics.costed_route_budget_slice`

Claim: A bounded costed-route/resource-budget selector can reject cheaper
routes that fail verification, residual ownership, or hidden-cost handling, compare against an
adequate overkill baseline, and select the lowest-cost adequate route when the
route record and budget record preserve verification, fallback, residual, and
non-claim boundaries.

Support transition: `argument` to `synthetic-test-backed`

Transition record:
`evidence_transitions/v1_0_measured/costed_route_resource_slice_synthetic_test_backed.json`

## Command

```bash
python3 scripts/validate_costed_route_resource_slice.py
```

The command recomputes the result from the tracked input and verifies the
tracked result record, this summary, and the accepted evidence-transition
record.

## Lean Fixture Bridge

The command also checks that the finite Lean fixture in
`AsiStackProofs.ResourceEconomics` matches the tracked JSON route costs,
selected route, rejection controls, and eligibility fields. This links the
public-safe replay to `lean/AsiStackProofs/ResourceEconomics.lean` without
claiming scheduler completeness, deployed routing behavior, economic
optimality, or chapter-core support-state promotion.

The bridge now also checks a finite selector-state trace theorem:
`costed_route_fixture_trace_selects_lowest_eligible_route`. The trace considers
the cheaper failed-verification control, the cheaper hidden-residual control,
the adequate overkill baseline, and the bounded selected route, then proves
that the replay ends with the selected route, two eligible routes seen, and two
cheaper rejected controls. This is still fixture-level trace evidence, not a
deployed scheduler proof.

## Inputs

- `experiments/costed_route_resource_slice/input/v1_0_costed_routes.json`
- Four costed route records validating against
  `schemas/costed_route_record.schema.json`
- Four resource budget records validating against
  `schemas/resource_budget_record.schema.json`
- One adequate overkill baseline route:
  `route://frontier-manual-review`
- One selected adequate lower-cost route:
  `route://bounded-transform-plus-verifier`
- Two cheaper negative controls:
  `route://cheap-unverified-transform`
  and `route://hidden-residual-auto-merge`

## Selection Rule

The deterministic cost formula is:

```text
estimated_tokens / 1000 + estimated_time_seconds / 60 + tool_cost_units * 5
```

A route is eligible only when it is evaluated, passes verification, has an
adequate outcome, is a promotion candidate for bounded evidence review, has a
dispatchable resource budget, dispatches under that budget, and keeps fallback,
residual, and non-claim boundaries visible.

## Observed Result

| Route | Role | Cost units | Eligibility |
|---|---:|---:|---|
| `route://bounded-transform-plus-verifier` | selected candidate | 14.2 | eligible |
| `route://frontier-manual-review` | adequate overkill baseline | 43.0 | eligible |
| `route://cheap-unverified-transform` | negative control | 2.3 | rejected |
| `route://hidden-residual-auto-merge` | hidden-residual control | 8.2 | rejected |

The selected route is 66.98 percent cheaper than the adequate overkill
baseline under the tracked synthetic cost formula.

## Negative Controls

The cheap failed negative-control route is rejected because it has
`verification_result: fail`, `outcome_state: cheap_brittle`,
`promotion_candidate: false`, `budget_state: residualized`, and
`budget_decision: residual`.

The hidden-residual negative-control route is rejected even though surface
verification passes, because it has `outcome_state: hidden_cost`,
`budget_state: residualized`, `budget_decision: residual`, missing residual
ownership, and lost reviewer handoff. The slice therefore does not choose the
cheapest route or the route that merely passes a shallow surface check; it
chooses the cheapest route that clears the recorded quality, verification,
budget, fallback, residual, and non-claim gates.

## Non-Claims

- Does not promote any chapter core claim above `argument`.
- Does not prove deployed routing, scheduler, runtime, load, KV-cache, or
  economic behavior.
- Does not measure model quality, benchmark quality, useful-solution
  performance, or safety outcomes.
- Does not replace future prototype traces, real route-quality measurements,
  load tests, benchmark runs, Theseus/Circle imported receipts, or independent
  review.
