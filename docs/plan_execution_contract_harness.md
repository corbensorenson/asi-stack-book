# Plan-Execution Contract Harness

Last updated: 2026-06-28

The third Phase 5 harness checks synthetic cross-record consistency for command
contracts, plan graphs, PlanForge DAGs, semantic atoms, and typed jobs under
`experiments/plan_execution_contracts/`.

## What It Checks

- Command contracts, plan graphs, PlanForge DAGs, semantic atoms, and typed jobs
  validate against their existing public schemas before semantic checks run.
- A dispatchable plan must point to the same command contract as its jobs.
- Plan dependencies and DAG edges must name known nodes, stay acyclic, and
  respect declared node order.
- Dispatchable plans need dispatch receipts, and active typed jobs must be
  represented in those receipts.
- Blocked plans can preserve residuals without dispatch receipts.
- Plan authority requirements must include the parent command authority ceiling.
- Semantic atoms must preserve command constraints and avoid unresolved
  obligations before dispatch.
- Expected artifacts must be traceable to a typed-job output or semantic-atom
  target artifact.
- Approval-required active jobs must carry approved approval state.

## Command

```bash
python3 scripts/validate_plan_execution_contracts.py
```

## Current Local Result

The 2026-06-28 local run passed:

```text
Plan-execution contract harness passed: 2 valid fixture(s), 5 expected-invalid fixture(s).
```

The result record is
`experiments/plan_execution_contracts/results/2026-06-28-local.md`.

## Boundary

This is synthetic cross-record gate validation. It improves executable evidence
discipline because it catches cyclic plans, contract mismatches, unreceipted
dispatch, lost requirements, and approval bypasses across existing record
schemas.

It is not a planner benchmark, deployed scheduler test, parser-quality result,
runtime adapter test, tool-execution trace, or proof of AI behavior. It does
not promote Appendix C, prove source interpretation, prove proof adequacy,
reproduce a benchmark, or validate runtime behavior.
