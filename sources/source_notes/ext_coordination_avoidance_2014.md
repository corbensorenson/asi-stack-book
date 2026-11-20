# Coordination Avoidance in Database Systems

| Field | Value |
|---|---|
| Source ID | `ext_coordination_avoidance_2014` |
| Publication | Peter Bailis et al. (2014). [Primary source](https://www.vldb.org/pvldb/vol8/p185-bailis.pdf) |

## Thesis

The authors formalize invariant confluence for a specified transaction set, merge operation and application invariant.

## Mechanisms

Under the paper's model, invariant confluence characterizes when that invariant can survive coordination-free execution.

## Evidence

The book uses the selected source passage for the decision in “Check whether two valid local writes still merge safely”.
The worked example is illustrative.

## Failure Modes

The condition depends on the named invariant and transaction/merge semantics. It does not grant permission to share data or excuse unmodeled concurrency effects.

## Book Chapters Supported

- `context-transactions-snapshots-mounts-and-taint`

## Claims To Add Or Update

Use the source as a comparator for the chapter's worked decision.
Retain the evidence state of the chapter's core claim.

## Open Questions

What observation from the worked example would justify acting when the
source's assumptions or measured setting do not carry over?
