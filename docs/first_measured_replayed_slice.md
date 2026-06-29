# Measured Or Replayed Slice Ledger

Date: 2026-06-29

This record documents v1.0 measured/replayed slices that clear bounded support
transitions. They are intentionally narrow: the first supports only the
repository-infrastructure claim that the Phase 5 harness registry can be
replayed by a single runner command against the current public-safe synthetic
fixture set, and the second supports only a synthetic
costed-route/resource-budget selector discipline claim.

They do not support ASI capability, deployed safety, model quality, benchmark
performance, runtime enforcement, source interpretation, or any chapter core
claim.

## Accepted Narrow Claim 1

Claim ID: `living-book-methodology.phase5_harness_registry_runner`

Claim: The living-book repository can replay its registered Phase 5 synthetic harness suite from `experiments/phase5_harness_registry.json`, execute each registered command locally, and verify that every command output contains the registry's expected `result_summary`.

Support transition: `argument` to `synthetic-test-backed`

Transition record: `evidence_transitions/v1_0_measured/phase5_harness_runner_synthetic_test_backed.json`

## Command

```bash
python3 scripts/run_phase5_harnesses.py --write-report
```

The command was followed by:

```bash
python3 scripts/validate_book.py
python3 scripts/validate_evidence_transitions.py
```

## Inputs

- `experiments/phase5_harness_registry.json`
- 21 registered harness commands
- 60 valid synthetic fixtures across registered harness fixture directories
- 102 expected-invalid synthetic fixtures across registered harness fixture directories
- Expected registry summaries stored in each registry entry

## Output

The command wrote `docs/phase5_harness_runner.md`.

Observed result:

- 21 registered harnesses run
- 21 harnesses passing return-code and expected-summary checks
- 0 harnesses requiring attention

## Negative Controls

The replay included expected-invalid fixture sets for every registered harness lane. The runner itself verifies command success and summary agreement; the individual harnesses verify that their expected-invalid fixtures are rejected. This establishes registry-driven replay and synthetic fixture discipline only.

## Non-Claims

- Does not promote any chapter core claim above `argument`.
- Does not prove deployed runtime behavior.
- Does not prove model quality, benchmark quality, or useful-solution performance.
- Does not prove AI safety, alignment, governance effectiveness, or source interpretation.
- Does not replace future measured cost-quality, context-admission, compression, planner/runtime, Theseus, or Circle replay slices.

## Residuals

This slice proves only repository-infrastructure replay. It does not satisfy
the stronger desire for non-infrastructure evidence.

## Accepted Narrow Claim 2

Claim ID: `resource-economics.costed_route_budget_slice`

Claim: A bounded costed-route/resource-budget selector can reject a cheaper
route that fails verification and residual handling, compare against an
adequate overkill baseline, and select the lowest-cost adequate route when the
route record and budget record preserve verification, fallback, residual, and
non-claim boundaries.

Support transition: `argument` to `synthetic-test-backed`

Transition record:
`evidence_transitions/v1_0_measured/costed_route_resource_slice_synthetic_test_backed.json`

Result record: `docs/costed_route_resource_slice.md`

## Command

```bash
python3 scripts/validate_costed_route_resource_slice.py
```

The command recomputes the tracked result from
`experiments/costed_route_resource_slice/input/v1_0_costed_routes.json`, checks
the tracked JSON result, checks the public summary, and checks the accepted
transition record.

## Inputs

- Three costed route records validating against
  `schemas/costed_route_record.schema.json`
- Three resource budget records validating against
  `schemas/resource_budget_record.schema.json`
- One adequate overkill baseline route:
  `route://frontier-manual-review`
- One selected adequate lower-cost route:
  `route://bounded-transform-plus-verifier`
- One cheaper negative control:
  `route://cheap-unverified-transform`

## Output

Observed result:

- Selected route: `route://bounded-transform-plus-verifier`
- Baseline route: `route://frontier-manual-review`
- Negative control: `route://cheap-unverified-transform`
- Selected synthetic cost units: 14.2
- Baseline synthetic cost units: 43.0
- Cost reduction versus baseline: 66.98 percent

## Negative Controls

The cheaper negative-control route has 2.3 synthetic cost units but is rejected
because verification failed, the outcome is `cheap_brittle`, the route is not a
promotion candidate, and the budget is residualized. This establishes only the
bounded selector discipline encoded in the tracked records and validator.

## Residuals

The next evidence slice should move from synthetic selector discipline toward a
public-safe prototype or measurement lane: context-admission replay,
compression/RankFold measurement, planner/runtime adapter trace, Theseus
transfer, Circle receipt replay, real route-quality measurement, or load and
serving-system traces.
