# Circle Public Consumer-Gate Fixtures

This directory contains the public ASI-side consumer-gate lane for the Circle
rope-position receipt recorded in `docs/circle_external_receipt_slice.md`.

- `fixtures/valid/circle_rope_receipt.consumer.valid.json` is the accepted
  public consumer-gate receipt fixture.
- `fixtures/invalid/*.invalid.json` are mutation controls that must be rejected.
- `results/2026-06-29-local.json` records the expected fixture digest, theorem
  count, and non-claim boundary.

The lane verifies a pinned Circle receipt boundary and rejects malformed or
overclaimed downstream use. It does not vendor Circle Calculus, rerun Circle
Lean in this repository, promote a chapter core claim, prove model quality, or
prove deployed proof-contract transport.
