# Benchmark Anti-Goodhart Harness

This directory contains synthetic fixtures for
`scripts/validate_benchmark_antigoodhart.py`.

The harness checks cross-record consistency across existing public schemas:

- `benchmark_ratchet_record`
- `policy_optimization_record`
- `steward_action_decision`

It tests only deterministic fixture semantics:

- a benchmark promotion must preserve run refs, baselines, regression refs,
  negative results, holdouts, contamination checks, and a mutation or transfer
  check;
- saturated benchmarks become regression floors rather than promotion evidence;
- blocked, contaminated, rerun, or regression-only ratchets cannot promote a
  policy update;
- policy updates cannot treat reward or score as truth, sole evidence, or
  authority;
- steward release actions must reference the ratchet and policy evidence and
  carry required approvals.

It does not run a benchmark, train a policy, execute a steward agent, publish a
release, or promote a support state.
