# Concurrent effect-ledger consumer receipt

Status: validated finite logical-time consumer; no deployment or support-state
transition.

The consumer independently implements the per-effect transition system in
`AsiStackProofs.IntegratedReferenceTrace`. An effect identity is its idempotency
key. An exact retry under the same active authority epoch is a no-op; a stale or
revoked retry rejects. Observation requires a prior attempt. A terminal action
requires observation, an unused terminal lane, and a receipt, and closes the
effect by exactly one of acknowledgement, compensation, or residualization.

The digest-bound corpus is anchored to the executed governed-trace invariant
result and covers sixteen cases: four accepted and twelve rejected. The four
accepted traces contain seventeen events, five unique effects, three
acknowledgements, one compensation, one residualized effect, one revocation,
and one exact idempotent retry. Twelve additional semantic mutations all
reject. They exercise zero or unknown identities, stale epochs, time
regression, observation without attempt, duplicate observation, wrong or
receipt-free terminal custody, double disposition, unclosed observed effects,
and retry after revocation. The support-state effect is exactly `none`.

Run:

```bash
lake -d lean build AsiStackProofs.IntegratedReferenceTrace
python3 scripts/validate_concurrent_effect_ledger.py
```

This is finite linearizable logical-time evidence. It is not a distributed
clock, partition, retry transport, scheduler, real effect adapter, complete
effect-discovery system, deployed rollback service, safety result, reproduction,
transfer result, or chapter-core promotion.
