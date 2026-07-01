# Resource Budget Ledger Harness

Last updated: 2026-07-01

The ninth Phase 5 harness checks deterministic Resource Budget Record fixtures
under `experiments/resource_budget_ledgers/`.

## What It Checks

- Resource budget records validate against the existing public schema.
- Dispatch cannot proceed from underfunded, escalated, deferred, rejected, or
  residualized budget states.
- High-risk or critical dispatch requires verification budget coverage,
  protected overhead, and explicit safety gates.
- Dispatch cannot claim savings by removing security, SCIF, approval, audit
  logging, redaction, or sanitization overhead.
- High-risk underfunded work escalates rather than dispatches.
- Cheap routes with hidden future debugging, human repair, evidence loss,
  privacy exposure, rollback difficulty, or hidden-context burden are
  residualized unless those costs are measured, bounded, or accepted by evidence.
- Low- or medium-risk work cannot dispatch through scarce protected review
  capacity while high-risk work is blocked.
- Fixture records must preserve explicit support-state non-promotion and deny
  scheduler, runtime, load, KV-cache, and economic-result claims.

## Command

```bash
python3 scripts/validate_resource_budget_ledgers.py
```

## Current Local Result

The 2026-07-01 local run passed:

```text
Resource budget ledger harness passed: 5 valid fixture(s), 6 expected-invalid fixture(s).
```

The result record is
`experiments/resource_budget_ledgers/results/2026-07-01-local.md`.

## Boundary

This is a deterministic resource-budget accounting slice. It turns part of the
Resource Economics chapter and the Security Kernel budget-preservation row into
executable record discipline for dispatch, escalation, protected overhead,
security-overhead erasure rejection, displaced costs, review-capacity hoarding,
residuals, and non-promotion boundaries.

It is not a budget scheduler, TokenMana simulation, PlanForge scheduler run,
load-stability experiment, KV-cache or serving-memory measurement,
verification-tax optimization result, runtime budget-enforcement result,
security-kernel enforcement result, SCIF-isolation result, logging-quality
result, sanitization-quality result, or economic outcome. It does not promote
Appendix C, prove source interpretation, prove proof adequacy, or validate
deployed AI behavior.
