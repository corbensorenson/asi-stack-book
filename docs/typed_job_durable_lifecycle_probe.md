# Typed Job Durable Lifecycle Probe

The Typed Job Durable Lifecycle Probe is a deterministic synthetic durable
lifecycle fixture for the `labor-os-and-typed-jobs` chapter.

It validates two valid synthetic durable lifecycle traces and nine expected-invalid controls.
The valid traces cover a retry that resumes under
the same parent contract, idempotency key, authority envelope, permission
basis, active lease, completion receipt, artifact refs, audit refs, replay ref,
and non-claim boundary, plus an expired-lease trace that blocks dispatch and
assigns a residual owner instead of pretending the job ran. The controls reject
retry without idempotency, authority widening on retry, permission overreach
after resume, expired-lease dispatch, missing completion receipt, missing
replay ref, missing residual owner, missing non-claim boundary, and support
state promotion from the fixture.

Run:

```bash
python3 scripts/validate_typed_job_durable_lifecycle_probe.py
```

The local result record is:

```text
experiments/typed_job_durable_lifecycle/results/2026-07-02-local.json
```

This probe does not execute a deployed scheduler, prove durable workflow
recovery, prove permission enforcement, prove approval-service behavior, prove
replay correctness, or promote the chapter support state. In short: no support-state transition.

The accepted no-promotion decision
`evidence_transitions/v1_x_measured/typed_job_durable_lifecycle_probe_no_change.json`
records this fixture as a blocking decision, not upward support movement. It
blocks deployed scheduler, durable workflow recovery, permission-enforcement,
approval-service, adapter-runner, completion-receipt service, replay-engine,
workflow-trace, benchmark, model-quality, safety, ASI, and chapter-core
promotion claims until stronger artifacts exist.
