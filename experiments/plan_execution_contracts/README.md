# Plan-Execution Contract Harness

This experiment checks synthetic cross-record consistency for command contracts,
plan graphs, PlanForge DAGs, semantic atoms, and typed jobs.

It is intentionally not a planner benchmark, scheduler test, tool-execution
trace, or parser-quality evaluation. The fixtures are small public-safe records
that exercise deterministic gate behavior across already-defined schemas.

## Command

```bash
python3 scripts/validate_plan_execution_contracts.py
```

## Fixtures

- `fixtures/valid_dispatchable_linear_plan.json` checks a linear dispatchable
  plan where intent-origin, command, graph, DAG, semantic atom, and typed jobs
  agree.
- `fixtures/valid_blocked_authority_plan.json` checks that a blocked plan can
  preserve residuals without dispatch receipts.
- `fixtures/invalid_cycle_in_dag.json` checks that cyclic dependencies are
  rejected.
- `fixtures/invalid_contract_mismatch.json` checks that plan and job records
  cannot point at different command contracts.
- `fixtures/invalid_dispatch_without_receipt.json` checks that an active typed
  job must be represented in dispatch receipts.
- `fixtures/invalid_requirement_lost.json` checks that unresolved lowered
  obligations block a dispatchable plan.
- `fixtures/invalid_approval_bypass.json` checks that approval-required active
  jobs cannot dispatch without approval.
- `fixtures/invalid_ambiguity_dispatched.json` checks that unresolved intent
  ambiguity cannot validate and dispatch a plan.
- `fixtures/invalid_hidden_override_applied.json` checks that hidden override
  requests must be rejected, quarantined, or ignored before planning.
- `fixtures/invalid_authority_widened_from_intent.json` checks that a command
  contract cannot widen the explicit intent authority ceiling.

## Environment

- Python 3.
- No network access.
- No external packages beyond the repository's dependency-free schema subset
  validator in `scripts/validate_protocol_examples.py`.

## Non-Claims

- This harness validates synthetic cross-record gate semantics only.
- It does not prove planner quality, scheduler behavior, deployed execution,
  runtime adapter safety, semantic-parser quality, prompt-injection
  containment, authority-extraction quality, benchmark performance, or any AI
  safety property.
- It does not promote any live chapter claim above `argument`.
