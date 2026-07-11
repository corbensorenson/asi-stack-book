# Post-v2 Realistic Governed-Work Flagship

Executed: 2026-07-10

This is the first ASI Stack workload to pair local model-generated planning and
code with fresh disposable Git repositories, matched baseline/governed routes,
an independent subprocess observer, hidden behavioral probes, receipt and path
reconciliation, residual accounting, rollback, quarantine, and real wall-time
and token accounting.

The frozen corpus contains eight pure-Python repository tasks and exactly the
eight preregistered attack families. Each task ran at seeds 17 and 29. A
separate bounded model call generated an implementation plan; a second call
received that plan and generated the candidate. The identical candidate bytes
then entered both routes. Raw plans, raw generations, extracted candidates,
observer records, worktree-state digests, Git commit identity, and
content-addressed run IDs are retained.

## Preserved Protocol Correction

The first prevalidation pass is retained as a non-evidentiary pilot. It showed
that all 16 generations omitted the requested explicit plan line and that the
runner modeled repositories in memory. The frozen amendment preserved those
failures, kept the same tasks, seeds, model, attacks, metrics, stop rule, and
allowed outcomes, and required an explicit plan-to-code sequence plus fresh
Git worktrees. No pilot result is used below.

## Matched Result

| Metric | Visible-test baseline | Governed route |
|---|---:|---:|
| Runs | 16 | 16 |
| Holdout-correct candidates | 4 | 4 |
| Releases | 5 | 0 |
| False accepts | 2 | 0 |
| Unsafe effects in disposable worktrees | 15 | 10 |
| Unsafe releases | 5 | 0 |
| Rollback attempts | 0 | 10 |
| Exact rollbacks | 0 | 8 |
| Failed rollbacks | 0 | 2 |
| Quarantines | 0 | 16 |
| Residuals discovered | 4 | 4 |
| Residuals left open | 4 | 2 |
| Route wall time | 2.534 s | 3.026 s |

The model used 1,968 planning-input tokens, 1,024 planning-output tokens, 3,166
code-input tokens, and 2,048 code-output tokens. Planning took 160.711 seconds,
code generation 330.028 seconds, independent observation 1.960 seconds, and
the complete local program 498.459 seconds. These are one Apple M1 local run,
not production throughput estimates.

The result is not a uniformly favorable governance story. Plan-conditioned
generation performed poorly: only four candidates passed holdouts, and the
governed route released none. Three correct candidates were justifiably
blocked by forged-receipt or correlated-verifier controls; one candidate
passed hidden probes but failed the visible contract under stale authority.
Ten governed effects were applied before final decision, eight rolled back
exactly, and the two deliberately sabotaged rollback cases remained visibly
open and quarantined. The governed route removed unsafe releases, but at the
cost of zero useful releases in this small adversarial corpus.

## Disposition

All three affected chapter-core scopes receive `no_change`. The packet is
stronger non-core evidence for a bounded interface pattern, record/reality
reconciliation, and local governance-cost measurement, but it does not justify
promotion beyond `argument`. It also weakens any reading that governance gates
alone guarantee useful throughput: model quality, plan conditioning, attack
mix, and refusal policy are coupled.

## Evidence Boundary

This is a public-safe local experiment, not a deployed authorization,
sandbox, verifier, rollback, or release service. The observer has a separate
process and implementation identity, not an external institution or human
reviewer. Controlled attack injections are not prevalence estimates. Eight
small tasks do not establish open-world safety, production transfer, general
model quality, or production governance economics.

## Reproduction

```bash
python3 scripts/validate_post_v2_governed_work_setup.py
python3 scripts/validate_post_v2_governed_work_flagship.py
```

The validator replays both visible and hidden observations, rebuilds fresh Git
route effects from every retained candidate, verifies all hashes and
content-addressed IDs, and rejects outcome-erasing mutations.
