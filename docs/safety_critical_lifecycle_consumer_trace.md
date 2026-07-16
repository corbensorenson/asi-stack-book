# Safety-Critical Lifecycle Consumer Trace

## Result

The local consumer trace passed on 2026-07-15. A separately implemented,
set-based replay consumed five accepted and five rejected traces from the
digest-bound `AsiStackProofs.SafetyCriticalLifecycle` corpus. The downstream
effect gate committed five bounded fixture effects, denied five effects, wrote
five denial residuals, and claimed zero support promotions.
The support-state effect is `none`.

| Metric | Observed value |
|---|---:|
| Selected source traces | 10 |
| Safety domains | 5 |
| Bounded fixture effects committed | 5 |
| Effects denied | 5 |
| Denial residuals recorded | 5 |
| Support promotions claimed | 0 |
| Rejecting consumer mutations | 8 |

The result artifact is
`experiments/safety_critical_lifecycle/results/2026-07-15-consumer-local.json`,
SHA-256
`f2cf54e61e2f8bde60f48c8dc0e51e2b04cb12f3372d84c9223d1ccc105ec32b`.
It binds the upstream corpus digest
`991bf35d88008e2ff3e356e15a689d38db9a81b700f75fa4a6fff57e4c03a1af`
and the exact digest of every selected source trace.

## Consumer boundary

The consumer does not trust a case label or expected result. It independently
replays each event sequence, recomputes the final phase and authority, and
admits an effect only when the replay accepts, ends in `effect_committed`, and
retains at least the requested authority. Every other route emits no effect and
must retain a residual.

The validator rejects mutations for corpus-digest forgery, source-trace digest
forgery, domain substitution, forged acceptance of a rejected trace, an effect
on a rejected trace, an effect above replayed authority, support-promotion
laundering, and duplicate receipts.

Run:

```bash
python3 scripts/validate_safety_critical_lifecycle_consumer_trace.py
```

## Evidence boundary

This is an executable finite consumer trace, not a deployed effect service. It
shows that one separately encoded local consumer can use the shared model's
bounded verdicts without committing rejected fixture effects or manufacturing a
support transition. It does not establish moral correctness, legal rights,
affected-party completeness, evaluator independence, attack completeness,
runtime integration, production safety, reproduction, transfer, AGI, or ASI.
