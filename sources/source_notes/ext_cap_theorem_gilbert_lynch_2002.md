# Source Note: Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services

| Field | Value |
|---|---|
| Source ID | `ext_cap_theorem_gilbert_lynch_2002` |
| Source title | Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services |
| Ingestion date | 2026-07-03 |
| Source version / URL | ACM DOI page, https://dl.acm.org/doi/10.1145/564585.564601; public PDF mirror, https://groups.csail.mit.edu/tds/papers/Gilbert/Brewer2.pdf |
| Citation label | Gilbert and Lynch (2002), Brewer's Conjecture / CAP theorem |
| Published / updated | 2002-06-01 / not recorded |
| DOI | 10.1145/564585.564601 |
| Ingestion basis | Public ACM metadata and public PDF inspected for high-level CAP-theorem framing; no distributed-system implementation, network partition test, or authority-propagation experiment reproduced. |

## Thesis

Gilbert and Lynch formalize Brewer's CAP intuition as a distributed-systems trade-off between consistency, availability, and partition tolerance. For the ASI Stack, this is a comparator for partitioned authority: a personal hive or runtime adapter cannot honestly promise both always-available dispatch and perfectly fresh authority consistency when revocations, grants, or approval state may be partitioned.

## Mechanisms

- Treat communication partitions and delays as first-class distributed-system failure modes.
- Separate safety-style consistency from liveness-style availability.
- Show that, under partition pressure, systems must choose how to trade response availability against correctness/consistency guarantees.
- Motivate application-specific coping strategies rather than blanket claims that a distributed service can have all properties at once.

## Evidence

- The source contributes external distributed-systems grounding for consistency/availability/partition-tolerance language.
- This repository has not implemented a distributed authority service, run a real partition test, reproduced the CAP proof, or measured grant/revocation propagation in a live hive; the bounded fixture does not prove deployed revocation propagation.
- Use this source to position partitioned authority as a design pressure and non-claim boundary, not as evidence that the ASI Stack solves distributed governance consistency.

## Failure Modes

- Treating a stale grant as current authority because a node can still respond.
- Allowing high-impact effects during a partition without fresh authority receipts or no-mutation evidence.
- Confusing audit-log availability with authority consistency.
- Claiming deployed revocation propagation from finite fixtures or local repository traces.

## Book Chapters Supported

- `personal-compute-hives-and-federated-edge-intelligence` (Personal Compute Hives and Federated Edge Intelligence)
- `runtime-adapters-tool-permissions-and-human-approval` (Runtime Adapters, Tool Permissions, and Human Approval)

## Claims To Add Or Update

- Add partitioned-authority language to the hive/runtime boundary: grant/effect races, revocation delay, stale receipts, quarantine while syncing, and fresh-authority receipt requirements.
- Preserve the non-claim that finite partitioned-authority fixtures do not prove deployed partition tolerance, distributed consensus, revocation propagation, availability, or safety.
- Route any future stronger claim through live or externally reviewable distributed authority traces before support-state movement.

## Open Questions

- What minimum live trace would make authority consistency under partitions externally reviewable?
- Which effects should prefer availability with quarantine, and which should prefer denial until authority freshness is restored?
- How should a personal hive expose partition status to humans without encouraging unsafe override?
