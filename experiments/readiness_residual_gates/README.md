# Readiness/Residual Gate Harness

This directory contains synthetic fixtures for
`scripts/validate_readiness_residual_gates.py`.

The harness checks cross-record consistency across existing public schemas:

- `costed_route_record`
- `readiness_gate_record`
- `replacement_transaction`

It tests only deterministic fixture semantics:

- canary and default decisions require ready evidence, passing route checks,
  authority compatibility, fallback paths, rollback readiness, monitor state,
  and evaluator independence;
- route residual obligations and inherited residuals must stay in gate or
  replacement escrow before promotion;
- failed, partial, unsafe, stale, or not-run routes cannot become promotion
  candidates;
- quarantine blocks the failed selected route while preserving fallback and
  diagnosis;
- expired evidence routes to rerun/reject behavior rather than canary or
  default promotion.

It does not implement a router, readiness engine, residual database, rollback
executor, runtime monitor, MoECOT replay path, benchmark, or support-state
promotion.
