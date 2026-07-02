# Typed Job Delivery Probe

The Typed Job Delivery Probe is a deterministic synthetic typed-job delivery
fixture for the `labor-os-and-typed-jobs` chapter.

It validates two valid synthetic typed-job traces and seven expected-invalid controls.
The valid traces cover a verified delivery that is evidence-ready
because artifact refs, audit refs, residuals, verification, and replay state are
present, plus a delivered-but-not-evidence-ready job that remains in
adjudication because verification is pending. The controls reject missing parent
contracts, approval bypass, permission overreach, delivery laundered as
evidence-ready, missing artifact refs, missing audit events, and support-state
promotion from the fixture.

Run:

```bash
python3 scripts/validate_typed_job_delivery_probe.py
```

The local result record is:

```text
experiments/typed_job_delivery/results/2026-07-02-local.json
```

This probe does not execute a deployed scheduler, prove permission
enforcement, prove approval-service behavior, execute a runtime adapter, prove
replay correctness, or promote the chapter support state. In short: no
no support-state transition.
