# Source Note: TxFS

| Field | Value |
|---|---|
| Source ID | `ext_txfs_2018` |
| Source title | TxFS: Leveraging File-System Crash Consistency to Provide ACID Transactions |
| Ingestion date | 2026-07-11 |
| Source version / URL | USENIX ATC 2018, https://www.usenix.org/conference/atc18/presentation/hu |
| Citation label | Hu et al. (2018), TxFS |
| Published / updated | 2018-07-11 / 2018-07-11 |
| DOI |  |
| Ingestion basis | Primary USENIX paper page and paper abstract/mechanism description reviewed; TxFS was not installed or reproduced. |

## Thesis

Application-visible transactions can leverage filesystem journaling to provide
ACID behavior, but only within explicit API, isolation, size, and platform bounds.

## Mechanisms

- Place logical updates inside journal transactions.
- Isolate in-progress changes and detect conflicts before commit.
- Expose a user-space transaction API evaluated with Git and SQLite.

## Evidence

The paper reports crash-consistency and performance results on its systems.
P1's directory snapshot is not TxFS and makes no ACID or crash-safety claim.

## Failure Modes

Journal capacity bounds transaction size; isolation adds complexity; byte-copy
restoration omits processes, services, and external effects.

## Book Chapters Supported

- `capability-replacement-and-rollback`
- `artifact-graphs-audit-logs-and-replay`
- `runtime-adapters-tool-permissions-and-human-approval`

## Claims To Add Or Update

Distinguish effect-inventory rollback from filesystem transactions and from
crash-consistent durable commit.

## Open Questions

- Which P1 effects require transactional primitives rather than snapshots?
- What evidence would support crash-time rather than post-run rollback?
