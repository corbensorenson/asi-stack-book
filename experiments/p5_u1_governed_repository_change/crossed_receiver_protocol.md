# Crossed receiver comparison

Protocol date: 2026-11-20

## Question

When does a separate receiving-side observation change a workflow decision
after a request times out? Compare it with competent scoped change control
that already uses a trustworthy status lookup. This is a prospective,
authored mechanism study. The earlier result is retained unchanged as the
motivation. Its task and receiver settings were confounded. This study varies
receiver behavior for each exact task. Neither study estimates how often these
conditions occur in production.

## Cases and baseline

Cross the four frozen Git patches from the first receiver series with both
receiver contracts, all four transport scenarios and five observation profiles.
The design has 160 matched pairs. Both arms use the same work, target and
scope check, approved effect identity, simulated deadline and retry budget.
Each run gets an isolated receiving journal and task context.

| Observation profile | Conventional status lookup | Separate receiving-side read |
|---|---|---|
| Shared fresh | Fresh | Fresh |
| Shared stale | Stale | Stale |
| Shared unavailable | Unavailable | Unavailable |
| Stale status | Stale | Fresh |
| Unavailable status | Unavailable | Fresh |

Fresh observations carry the current read tick and exact operation key,
destination and payload identity. A stale observation reports an older known
state using its original read tick. Deadlines and identity checks are shared.
An operation pending at tick 2 may commit at tick 3. Both arms have decision
opportunities at ticks 2 and 4. Report the exact synthetic timing and fixtures.
Use logical time to keep the fault schedule deterministic. No real network
or service is involved.

- **Competent conventional workflow.** Check status on ambiguous responses.
  Close on a fresh exact committed observation. A definitive failure allows a
  bounded retry. Otherwise retry only with a receiver contract that can
  deduplicate the same operation key. Hold ambiguous operations that cannot
  safely be reissued.
- **Additional observation route.** Apply the conventional status lookup
  and the same retry rules. When status is stale or unavailable, consult the
  separate receiving-side read. Accept that result under the same freshness
  and identity conditions. Pending or missing evidence leaves the disposition
  open. There is no extra time, permission or retry budget.

Both status routes are views of one simulated receiver, with controlled read
availability and freshness. A different interface can supply the same
evidence. A win in the stale-status or unavailable-status profile isolates the
value of a second qualified observation under the simulated failure pattern.
It does not establish physical fault isolation or an architectural advantage
with equally good evidence access.

## Scoring and calibration

Score against terminal committed effects independently of the caller-facing
status views. Report useful closure, safe hold, repeated effect, false closure
and wrongly blocked authorized work by observation and receiver contract.
Report retries and separate observer reads as counts. The study has no human
review time measure. Keep all attempted pairs and the raw records needed to
replay the scoring.

Before opening the series, run isolated controls for local scope, fresh
commit, pending, explicit failure, incorrect target or operation, stale read
and missing read. Exercise the direct source of terminal truth and show that
the score can distinguish one exact commit, a repeated commit, and a
reported closure without the required effect. Calibration failures stop
outcome reporting and remain visible as instrument failures.

The primary comparison is straightforward. Under shared fresh access, match
the ordinary status result before paying for a separate interface. Under
shared observation failures, credit safe holds and any protection already
provided by receiver deduplication. When fresh receiving-side evidence
remains available, report which additional cases closed without a repeated
effect or false closure. Preserve deviations as a dated amendment or a
separate exploratory run.
