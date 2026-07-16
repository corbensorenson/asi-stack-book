# Safety-critical lifecycle trace corpus

This corpus is an independent executable refinement of
`AsiStackProofs.SafetyCriticalLifecycle`. It exercises the shared transition
semantics used by the Constitutional Alignment, Corrigibility, Value Conflict,
Governance Rights, and Self-Improvement proof surfaces.

Run:

```bash
python3 scripts/validate_safety_critical_lifecycle.py
python3 scripts/validate_safety_critical_lifecycle_consumer_trace.py
```

The validator checks exact accepted and rejected traces, final state snapshots,
domain coverage, deletion countermodels for every required obligation, protected
predicate removal, authority monotonicity, rollback conditions, support-promotion
conditions, and a digest binding to the Lean source. Passing is bounded to this
finite model and corpus. It does not establish moral correctness, legal rights,
real evaluator independence, affected-party completeness, or deployed safety.

The second validator is a downstream consumer rather than another theorem
counter. It independently replays five accepted and five rejected domain traces,
then admits exactly one bounded fixture effect per accepted effect trace and
routes every rejection to a durable residual. It rejects digest forgery, domain
substitution, acceptance forgery, effects on rejected traces, authority excess,
support-promotion laundering, and duplicate receipts. Its tracked result under
`results/` is local finite consumer evidence only, not a deployed effect path or
chapter-core promotion.
