# Runtime Adapter Permission Harness

Last updated: 2026-06-28

The seventh Phase 5 harness checks synthetic cross-record consistency for typed
jobs, runtime adapter invocations, and authority-use receipts under
`experiments/runtime_adapter_permissions/`.

## What It Checks

- Typed jobs, runtime adapter invocations, and authority-use receipts validate
  against their existing public schemas before semantic checks run.
- The invocation must point to the same job and adapter named by the typed job.
- The typed job must carry both the adapter capability and the required
  permission.
- High-impact, irreversible, unknown-impact, high-risk, critical-risk, or
  unknown-risk invocations must carry scoped approval records, non-expired
  approval markers, and approved typed-job state.
- Active invocations need authority handles and effect leases.
- Executed invocations need receipt refs, pre-state refs, post-state refs,
  verification refs, and audit refs.
- Executed external or high-impact invocations need either rollback handles or
  irreversible residual records.
- Authority-use receipts must match the invocation handle, allowed action, and
  approval record when approval is required.
- Scenario and invocation non-claims must explicitly preserve support-state
  non-promotion.

## Command

```bash
python3 scripts/validate_runtime_adapter_permissions.py
```

## Current Local Result

The 2026-06-28 local run passed:

```text
Runtime adapter permission harness passed: 2 valid fixture(s), 5 expected-invalid fixture(s).
```

The result record is
`experiments/runtime_adapter_permissions/results/2026-06-28-local.md`.

## Boundary

This is synthetic runtime-adapter record validation. It improves executable
evidence discipline because it catches missing typed-job permissions, high-impact
approval bypasses, expired approvals, missing effect receipts, and missing
rollback/residual records across existing schemas.

It is not a deployed adapter test, sandbox test, human approval service test,
secret-handle safety test, tool-execution trace, rollback execution, or proof of
AI behavior. It does not promote Appendix C, prove source interpretation, prove
proof adequacy, reproduce a benchmark, or validate runtime behavior.
