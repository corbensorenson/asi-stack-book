# Benchmark Anti-Goodhart Harness

Last updated: 2026-06-28

The sixth Phase 5 harness checks synthetic cross-record consistency for
benchmark ratchets, policy updates, and steward release decisions under
`experiments/benchmark_antigoodhart/`.

## What It Checks

- All nested benchmark, policy, and steward records validate against their
  existing public schemas.
- Benchmark promotion requires active/not-saturated state, run refs, baselines,
  regression refs, negative-result retention, eligible support effect, holdout
  and contamination checks, a mutation or transfer check, and no failed
  anti-Goodhart checks.
- Saturated benchmarks can become regression floors, but cannot be the basis of
  stronger readiness or claim promotion.
- Policy promotion requires a promotion-ready ratchet, run measurement status,
  non-`not_run` training mode, admissible feedback, holdouts, regressions,
  evaluation refs, governance gates, authority review, and evidence packet refs
  that include the ratchet id.
- Policy promotion cannot treat reward or score as truth, sole evidence, or
  authority.
- Approved or executed steward release actions must reference the benchmark
  ratchet id and policy update id, and must carry approval refs when approvals
  are required.

## Command

```bash
python3 scripts/validate_benchmark_antigoodhart.py
```

## Current Local Result

The 2026-06-28 local run passed:

```text
Benchmark anti-Goodhart harness passed: 2 valid fixture(s), 5 expected-invalid fixture(s).
```

The result record is
`experiments/benchmark_antigoodhart/results/2026-06-28-local.md`.

## Boundary

This is synthetic cross-record gate validation. It improves executable evidence
discipline because it catches saturated benchmark promotion, public-score-only
promotion, policy promotion from blocked ratchet evidence, reward-as-truth
confusion, and steward release without approval across existing protocol
schemas.

It is not a benchmark run, hidden-holdout validation, contamination detector,
policy-training result, reward-hacking evaluation, steward-agent execution,
release-safety review, or proof of AI behavior. It does not promote Appendix C,
prove source interpretation, prove proof adequacy, reproduce a benchmark, or
validate runtime behavior.
