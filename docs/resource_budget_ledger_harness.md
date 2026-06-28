# Resource Budget Ledger Harness

Last updated: 2026-06-28

The ninth Phase 5 harness checks deterministic Resource Budget Record fixtures
under `experiments/resource_budget_ledgers/`.

## What It Checks

- Resource budget records validate against the existing public schema.
- Dispatch cannot proceed from underfunded, escalated, deferred, rejected, or
  residualized budget states.
- High-risk or critical dispatch requires verification budget coverage,
  protected overhead, and explicit safety gates.
- High-risk underfunded work escalates rather than dispatches.
- Cheap routes with hidden future debugging, human repair, evidence loss,
  privacy exposure, rollback difficulty, or hidden-context burden are
  residualized unless those costs are measured, bounded, or accepted by evidence.
- Fixture records must preserve explicit support-state non-promotion and deny
  scheduler, runtime, load, KV-cache, and economic-result claims.

## Command

```bash
python3 scripts/validate_resource_budget_ledgers.py
```

## Current Local Result

The 2026-06-28 local run passed:

```text
Resource budget ledger harness passed: 4 valid fixture(s), 4 expected-invalid fixture(s).
```

The result record is
`experiments/resource_budget_ledgers/results/2026-06-28-local.md`.

## Boundary

This is a deterministic resource-budget accounting slice. It turns part of the
Resource Economics chapter into executable record discipline for dispatch,
escalation, protected overhead, displaced costs, residuals, and non-promotion
boundaries.

It is not a budget scheduler, TokenMana simulation, PlanForge scheduler run,
load-stability experiment, KV-cache or serving-memory measurement,
verification-tax optimization result, runtime budget-enforcement result, or
economic outcome. It does not promote Appendix C, prove source interpretation,
prove proof adequacy, or validate deployed AI behavior.
