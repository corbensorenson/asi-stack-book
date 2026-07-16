# Compact GVR Synthetic Slice

Date: 2026-07-01

This record documents a bounded v1.x generate-verify-repair slice for Compact
Generative Systems. It uses tracked public-safe synthetic records, not private
source text, not a real codec, and not a model run.

## Accepted Narrow Claim

Claim ID: `compact-generative-systems.compact_gvr_receipt_slice`

Claim: A bounded compact-generation receipt validator can compare a literal
baseline against a compact generator-plus-repair receipt, reject lossy exactness
overclaims, reject negative-rate/no-fallback receipts, reject bounded-search
overruns, and keep residual, fallback, consumer-policy, and non-claim
boundaries visible.

Support transition: `argument` to `synthetic-test-backed`

Transition record:
`evidence_transitions/v1_x_measured/compact_gvr_slice_synthetic_test_backed.json`

## Command

```bash
python3 scripts/validate_compact_gvr_slice.py
```

The command recomputes the tracked result from
`experiments/compact_gvr_slice/input/v1_x_compact_gvr_records.json`, checks the
tracked JSON result, checks this public summary, checks the evidence-transition
record, and checks that the finite Lean fixture bridge in
`AsiStackProofs.CompactGenerativeSystems` keeps the same receipt constructors,
byte counts, selected receipt, and rejected controls.

## Inputs

- One literal baseline receipt.
- One exact compact receipt with a repeat generator, explicit repair residual,
  fallback path, residual owner, exact-replay consumer policy, and search bound.
- Three negative controls: lossy exactness, negative-rate/no-fallback, and
  bounded-search overrun.

## Output

| Receipt | Role | Serialized bytes | Status |
|---|---|---:|---|
| `receipt://repeat-generator-plus-repair` | selected compact receipt | 78 | eligible |
| `receipt://literal-baseline` | literal baseline | 368 | baseline |
| `receipt://lossy-summary-marked-exact` | lossy exactness control | 55 | rejected |
| `receipt://negative-rate-no-fallback` | negative-rate/no-fallback control | 485 | rejected |
| `receipt://bounded-search-overrun` | bounded-search control | 72 | rejected |

Observed result:

- Selected receipt: `receipt://repeat-generator-plus-repair`
- Baseline receipt: `receipt://literal-baseline`
- Selected serialized bytes: 78
- Literal baseline bytes: 368
- Byte reduction versus literal baseline: 78.8 percent smaller
- Negative controls rejected: 3 of 3
- Result record:
  `experiments/compact_gvr_slice/results/2026-07-01-local.json`

## Negative Controls

The lossy exactness control is smaller than the selected receipt but is rejected
because verification fails and reconstruction does not match the target. The
negative-rate/no-fallback control reconstructs exactly, but its serialized form
is larger than the literal baseline and it has no fallback path. The
bounded-search control is rejected because the attempted search exceeds the
declared bound, verification is not run, exact replay is not allowed, and
reconstruction does not match the target.

## Lean Fixture Bridge

The command also checks the reachable verification and fallback boundary in
`AsiStackProofs.CompactGenerationRefinement`: lossy exactness is blocked,
reconstruction mismatch activates a preserved-source fallback only when it is
executable, missing fallback blocks progress, and the fallback witness reaches
closure without support or external-effect authority. Receipt values and byte
comparisons remain owned by this Python validator rather than copied into Lean.

## Residuals

- The selected receipt is a synthetic record, not a general-purpose compressor.
- The generator is a deterministic toy repeat rule, not a learned model.
- The verifier is the local validator's exact string reconstruction check, not
  an independent semantic verifier.
- The byte count is a fixture serialization count, not a real compression
  benchmark over a corpus.
- Fallback execution is recorded but not deployed.

## Non-Claims

- Does not promote any chapter core claim above `argument`.
- Does not prove compression utility, codec correctness, semantic utility,
  model quality, or benchmark performance.
- Does not prove deployed generator, verifier, fallback execution, or
  reconstruction behavior outside this synthetic fixture.
