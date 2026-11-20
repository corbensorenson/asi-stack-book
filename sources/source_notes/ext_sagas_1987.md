# Sagas

| Field | Value |
|---|---|
| Source ID | `ext_sagas_1987` |
| Publication | Hector Garcia-Molina and Kenneth Salem (1987). [Primary source](https://www.cs.princeton.edu/techreports/1987/070.pdf) |

## Thesis

The authors divide a long transaction into smaller transactions that can interleave, with compensations for already completed steps if the sequence fails.

## Mechanisms

The saga lets committed steps remain available to other transactions before the entire sequence completes. Compensating actions amend the meaning of partial completion in the application.

## Evidence

The book uses the selected source passage for the decision in “What can a compensating action restore?”.
The worked example is illustrative.

## Failure Modes

A compensation repairs a specified consequence. It does not erase historical visibility or guarantee compensation succeeds in a different system.

## Book Chapters Supported

- `governed-operations-incident-command-and-graceful-degradation`

## Claims To Add Or Update

Use the source as a comparator for the chapter's worked decision.
Retain the evidence state of the chapter's core claim.

## Open Questions

What observation from the worked example would justify acting when the
source's assumptions or measured setting do not carry over?
