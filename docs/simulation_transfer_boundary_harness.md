# Simulation Transfer Boundary Harness

Command: `python3 scripts/validate_simulation_transfer_boundaries.py`

Result record: `experiments/simulation_transfer_boundaries/results/2026-06-30-local.md`

Latest local result:

```text
Simulation transfer boundary harness passed: 3 valid fixture(s), 6 expected-invalid fixture(s).
```

## What It Checks

This book-gate harness validates deterministic wrappers around
`Simulation Contract Record` fixtures. It checks that simulation or synthetic
evidence cannot travel beyond declared fidelity, resource, bottleneck,
omission, approximation, instrumentation, and transfer boundaries.

The fixture set covers:

- unit-invariant transfer within a declared boundary;
- benchmark comparison downgraded to reduced scope;
- scenario-only transfer blocking;
- missing fidelity declaration;
- unbounded world/deployment transfer;
- missing resource bill;
- blocked transfer without residual custody;
- ignored instrumentation effects;
- support-state promotion attempts.

## Boundary

This is fixture discipline over simulation-transfer records. It does not run a
simulator, validate simulator adequacy, prove physical feasibility, reproduce a
benchmark, measure economic optimality, validate open-world transfer, exercise a
scheduler, or promote Appendix C or any chapter core claim above `argument`.
