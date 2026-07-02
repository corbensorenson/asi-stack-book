# SCF Lifecycle Trace Probe

The SCF lifecycle trace probe is a synthetic transition check for the chapter
`stable-capability-fields`.

It validates a forward lifecycle trace from `shadow` to `canary`, `qualified`,
`default`, `deprecated`, and `retired`; validates an incident quarantine branch;
and rejects expected-invalid controls for identity drift, default promotion
without a regression floor, default authority expansion, retired-state restart,
deprecation without notice, and retirement without receipt.

Run:

```bash
python3 scripts/validate_scf_lifecycle_trace.py
```

The local result record is:

```text
experiments/scf_lifecycle_trace/results/2026-07-02-local.json
```

This probe does not execute deployed route validation, prove
evaluator-integrity measurement, preserve real regressions, execute rollback,
enforce lifecycle transitions in production, or promote the chapter support
state.
