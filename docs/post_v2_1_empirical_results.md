# Post-v2.1 Empirical Results

Recorded: 2026-07-11

The three preregistered programs completed exactly once from setup commit
`707fc10969b04bd31e135c8a711b33e9505e0d87`. They consumed the full registered
332-call budget, added no arm, retried no atomic call, and retained every raw
result. The deterministic outcome ledger is
`experiments/post_v2_1_evidence_program/results/2026-07-11-post-v2-1-outcomes.json`;
`scripts/validate_post_v2_1_outcomes.py` recomputes it from all six phase
bundles and replays the retained public-safe artifacts.

The results warrant book integration and a public release because they are
reproducible and public-safe. They do not warrant a chapter-core support
promotion.

## P1 — governed usefulness and effect-complete rollback

The held-out set contained 36 task-seed transactions. The policy route was
correct on 36/36, but the model candidate was correct on only 2/36. Direct
execution released 26 candidates: two were useful and 24 were unsafe. The
governed transaction released the same two useful candidates and no unsafe
candidate, while clarifying six, quarantining eighteen, and refusing ten.

| Endpoint | Observed | Preregistered requirement | Result |
|---|---:|---:|---|
| Governed useful-release rate | 2/36 = 0.0556 | at least 0.50 | fail |
| Unsafe-release reduction versus direct | 24/36 = 0.6667 | at least 0.15 | pass |
| Exact rollback on attack controls | 32/36 = 0.8889 | at least 0.95 | fail |

Disposition: `narrow`. The finite workload supports a bounded safety result,
not governed usefulness or effect-complete rollback. `GW-01` persists because
four registered rollback controls remained inexact. `GW-02` narrows from zero
useful throughput to a nonzero but inadequate 2/36. `GW-03` persists because
the observer remains internally separated rather than externally independent.

## P2 — ambiguous routing and real-model deliberation

The held-out set contained 60 requests: ten for each of six target actions.
The learned router selected the correct route on 59/60, including ten
fallbacks, eleven abstentions, and ten clarifications. The rule router was
correct on 41/60 and the generalist on 10/60. The routing arms therefore
genuinely differed and both formerly unused coverage paths activated.

That routing result must not be mistaken for generated-answer quality. The
learned route's 20 correct outcomes were correct non-answer actions. Across 60
requests and six evaluator-visible candidates per request, all 360 substantive
candidate evaluations were wrong, with zero parse failures. No-deliberation,
fixed-three, adaptive, overcompute-five, and verifier-disabled arms all ended
at 0/60 correct. Adaptive stopping consumed all five candidates for all 60
requests, so it neither improved utility nor supplied any initially-correct
case on which to estimate corruption reduction.

Routing disposition: `narrow`. Deliberation disposition: `no_change`.
`RD-01` narrows because the policies now separate only on a bounded synthetic
finite workload. `RD-02` closes because fallback and abstention both activated
under the registered criteria. `RD-03` narrows because candidates are actual
model outputs but evaluator validity remains internal and generated utility is
zero. `RD-04` persists: the fifteen historical extra-compute harms remain a
regression-only set, and this new workload had no initially-correct candidate
with which to establish less corruption.

## P3 — full-state update and unlearning causality

The campaign ran five arms at each of three seeds. Every one of the fifteen
seed-arm transactions restored all 24 declared model, optimizer, scheduler,
RNG, cache, checkpoint, backup, and descendant-state surfaces exactly.
Prospective validation-only checkpoint authority was honored; six arms
exhibited best/final disagreement, and the three authorized-data comparators
stopped after crossing the retained-validation safety bound and remained
ineligible.

None of the nine eligible challenger seed-arms reached the preregistered 0.05
target-utility gain. Deletion-aware retraining changed 4, 0, and 1 deletion
cohort decisions across the three seeds. It propagated lineage invalidation,
but the true-confidence signal remained only a proxy for influence and the
immutable source corpus remained stored.

Update disposition: `no_change`. Rollback and unlearning dispositions:
`narrow`. `UU-01` narrows because retained utility was protected but target
gain remained sub-threshold and seed-sensitive. `UU-02` narrows because the
authority rule was prospective and honored, while disagreement remained an
observed property. `UU-03` persists because behavioral and lineage evidence is
not influence, privacy, legal, or storage erasure. `UU-04` closes only for the
declared local 24-surface inventory; external and production transfer remain
explicitly outside the result.

## Statistical and claim boundary

The ledger reports exact raw counts and paired effects over the complete
registered finite workloads. It makes no population claim and reports no
population interval, so the preregistered optional 10,000-resample bootstrap
rule is not invoked. Internal process separation is not external independence;
synthetic local workloads are not production transfer; exact rollback is only
over each declared inventory; and no result promotes a chapter-core claim
above `argument`.

## Reproduction

Run:

```bash
python3 scripts/validate_post_v2_1_outcomes.py
```

The validator checks all six content-addressed phase bundles, replays 72 P1
candidate observations, checks 65 P2 request records and their retained model
outputs, re-observes all fifteen P3 state trees, recomputes all dispositions,
and rejects twelve outcome-laundering mutations.
