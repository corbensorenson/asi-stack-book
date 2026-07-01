# Measured Or Replayed Slice Ledger

Date: 2026-06-29

This record documents v1.0 measured/replayed slices that clear bounded support
transitions. They are intentionally narrow: the first supports only the
repository-infrastructure claim that the Phase 5 harness registry can be
replayed by a single runner command against the current public-safe synthetic
fixture set, the second supports only a synthetic costed-route/resource-budget
selector discipline claim, and the third supports only a local external Circle
receipt replay for one rope-position contract.

They do not support ASI capability, deployed safety, model quality, benchmark
performance, runtime enforcement, source interpretation, transfer, or any
chapter core claim.

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
- 22 registered harness commands
- 62 valid synthetic fixtures across registered harness fixture directories
- 108 expected-invalid synthetic fixtures across registered harness fixture directories
- Expected registry summaries stored in each registry entry

## Output

The command wrote `docs/phase5_harness_runner.md`.

Observed result:

- 22 registered harnesses run
- 22 harnesses passing return-code and expected-summary checks
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

Claim: A bounded costed-route/resource-budget selector can reject cheaper
routes that fail verification, residual ownership, or hidden-cost handling, compare against an
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
transition record. It also checks that the finite Lean fixture in
`AsiStackProofs.ResourceEconomics` stays aligned with the public JSON route
costs, selected route, negative controls, and eligibility fields.

## Inputs

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

## Output

Observed result:

- Selected route: `route://bounded-transform-plus-verifier`
- Baseline route: `route://frontier-manual-review`
- Negative control: `route://cheap-unverified-transform`
- Selected synthetic cost units: 14.2
- Baseline synthetic cost units: 43.0
- Hidden-residual control synthetic cost units: 8.2
- Cost reduction versus baseline: 66.98 percent
- Lean fixture alignment: route constructors, selected constructor, costs,
  negative controls, and eligibility booleans matched

## Negative Controls

The cheap failed negative-control route has 2.3 synthetic cost units but is rejected
because verification failed, the outcome is `cheap_brittle`, the route is not a
promotion candidate, and the budget is residualized. The hidden-residual
negative-control route has 8.2 synthetic cost units and passes surface
verification, but it is rejected because it hides reviewer handoff and residual
ownership costs. This establishes only the bounded selector discipline encoded
in the tracked records and validator.

## Residuals

The next evidence slice should move from synthetic selector discipline toward a
public-safe prototype or measurement lane: context-admission replay,
compression/RankFold measurement, planner/runtime adapter trace, Theseus
transfer, Circle receipt replay, real route-quality measurement, or load and
serving-system traces.

## Accepted Narrow Claim 3

Claim ID: `circle-calculus.external_rope_receipt_replay`

Claim: A local external Circle Calculus checkout at commit `63b0f511` can build
its `Circle` Lean target, certify the rope position distinguishability contract,
emit a ready digest and accepted receipt for `CC-AI-CONTRACT-ROPE-001`, and pass
the selected public-safe receipt/contract test batch recorded in the result
file.

Support transition: `argument` to `prototype-backed`

Transition record:
`evidence_transitions/v1_0_measured/circle_external_rope_receipt_prototype_backed.json`

Result record: `docs/circle_external_receipt_slice.md`

## Command

The accepted command set is recorded in
`experiments/circle_external_receipt_slice/results/2026-06-29-local.json` and
summarized in `docs/circle_external_receipt_slice.md`. The tracked validator is:

```bash
python3 scripts/validate_circle_external_receipt_slice.py
```

That validator checks the public-safe result summary, evidence-transition
record, required theorem IDs, fingerprints, receipt fields, discarded attempts,
and non-claim boundaries. It does not rerun the external local checkout in CI.

## Inputs

- External checkout: `/Users/corbensorenson/Documents/circle math`
- External checkout commit: `63b0f511`
- One Circle rope-position contract: `CC-AI-CONTRACT-ROPE-001`
- Required theorem IDs: `AIRA-T0058`, `AIRA-T0059`, `AIRA-T0171`,
  `AIRA-T0172`, `AIRA-T0239`, `AIRA-T0240`, and `AIRA-T0241`
- Required recommendation ID: `ROPE-USE-D19-MARGIN-FRONTIER`

## Output

Observed result:

- `lake build Circle` completed successfully with 2624 jobs.
- The rope certification returned `status` `proved`, `request_passed` `true`,
  decision verdict `passed`, assurance `mixed_theorem_and_computation`, and 55
  theorem IDs proved.
- The ready digest returned `ready=True`, `fields=31`, `missing=0`, and
  `theorems=75`.
- The accepted receipt required the seven theorem IDs and the D19 margin
  frontier recommendation.
- The selected receipt/contract pytest batch returned `145 passed in 718.24s
  (0:11:58)`.

## Negative Controls

This slice preserves two discarded procedural attempts: a pytest command that
named a missing test file and ran no tests, and a ready-digest command that
omitted `PYTHONPATH=.` and failed with `ModuleNotFoundError`. These discarded
attempts are kept as non-evidence so the accepted result cannot hide the command
repair path.

## Non-Claims

- Does not promote any chapter core claim above `argument`.
- Does not prove model quality, reasoning ability, context length, speed,
  memory scaling, deployment safety, transfer, or ASI.
- Does not prove deployed proof-contract transport inside The ASI Stack.
- Does not make the external Circle checkout a vendored public dependency.

## Residuals

The next imported-prototype slice should either vendor a public contract pack,
add an explicit public replay fixture, or route a proof-contract receipt through
an ASI Stack consumer gate. Broader Circle and proof-carrying-computation claims
still need separate accepted transitions.
