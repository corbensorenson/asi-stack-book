# Residual Honesty Conservation Fixture

Date: 2026-07-03

This record documents a bounded residual-honesty fixture for Compact
Generative Systems. It uses tracked public-safe synthetic records, not private
source text, not a deployed residual ledger, not a model run, and not a
compression benchmark.

## Command

```bash
python3 scripts/validate_residual_honesty_conservation.py
```

The command reads
`experiments/residual_honesty_conservation/input/residual_conservation_cases.json`,
recomputes the tracked result at
`experiments/residual_honesty_conservation/results/2026-07-03-local.json`,
checks this public summary, checks the contribution novelty ledger, and checks
the reachable residual-custody boundary
`unresolved_obligation_without_owner_blocks_residualization` in
`AsiStackProofs.CompactGenerationRefinement`.

## Fixture Shape

The fixture contains 3 valid residual records:

- accepted visible residual with owner, evidence reference, and remaining
  burden recorded;
- deferred residual with owner and due condition;
- discharged residual with zero remaining burden and a discharge artifact.

It also contains 5 expected-invalid controls:

- hidden residual after a metric gain;
- erased residual without a discharge artifact;
- moved residual without an owner;
- support-state promotion attempt from the fixture;
- zero-residual overclaim with remaining burden.

## Result

The validator accepts only the three honest residual records and rejects all
five controls. The support-state effect is `none`; no chapter core claim moves
above `argument`.

Result record:
`experiments/residual_honesty_conservation/results/2026-07-03-local.json`

## Lean Fixture Bridge

The Lean bridge records the same finite fixture summary:
accepted residuals are recorded, deferred residuals are owned, discharged
residuals have receipts, hidden residuals are rejected, erased residuals are
rejected, unowned moved residuals are rejected, support-state effects remain
`none`, and non-claim boundaries are present.

The theorem proves only this record-level fixture relation. It does not prove
that all real residuals are observable, does not prove that residuals can be
measured completely, and does not prove safety.

## Boundary

- Does not prove all residuals are observable.
- Does not prove safety.
- Does not promote any chapter core claim above `argument`.
- Does not prove residual conservation for all real systems.
- Does not prove deployed residual detection, model quality, benchmark
  performance, compression utility, fallback behavior, or verifier quality.
