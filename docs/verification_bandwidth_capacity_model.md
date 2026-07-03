# Verification Bandwidth Capacity Model

The Verification Bandwidth Capacity Model is a deterministic synthetic
record-level model for the chapter
`verification-bandwidth-and-context-adequacy`.

It models one narrow proposition: for a claim whose relevant semantic units all
need pairwise comparison, context exposure grows with the number of units while
comparison obligations grow as pairwise obligations. In the tracked synthetic
fixture, 12 semantic units create 66 all-pairwise obligations. A verifier that
checks only 18 obligations leaves 48 residual obligations and must split,
escalate, or keep the claim below verified support.

The fixture also records a valid decomposition case: three named clusters of
four units each plus six named boundary checks reduce the modeled obligation
set to 24 checks. That is not free capacity. It is a scoped decomposition
contract: the boundary checks must be named, checked, and residualized if
missing.

Run:

```bash
python3 scripts/validate_verification_bandwidth_capacity_model.py
```

The local result record is:

```text
experiments/verification_bandwidth_capacity/results/2026-07-03-local.json
```

This model does not prove a model verification bandwidth law, does not measure
contradiction-rate performance, does not validate an adequacy classifier, does
not prove long-context failure in deployed systems, and does not create a
support-state transition. In short: no support-state transition.
