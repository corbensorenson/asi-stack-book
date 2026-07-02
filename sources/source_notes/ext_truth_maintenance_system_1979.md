# Source Note: A Truth Maintenance System

| Field | Value |
|---|---|
| Source ID | `ext_truth_maintenance_system_1979` |
| Source title | A Truth Maintenance System |
| Ingestion date | 2026-07-01 |
| Source version / URL | PhilPapers metadata, https://philpapers.org/rec/DOYATM |
| Citation label | Doyle (1979), A Truth Maintenance System |
| Published / updated | 1979 / 1979 |
| DOI | 10.1016/0004-3702(79)90008-0 |
| Ingestion basis | PhilPapers bibliographic metadata inspected for the truth-maintenance literature queue; the journal article text, algorithms, and implementation details are not imported into this repository. |

## Thesis

This source belongs in `claim-ledgers-and-belief-revision` as a classic truth-maintenance comparator. It grounds the chapter's reason-maintenance language in prior AI work on maintaining the reasons behind program beliefs, while keeping the ASI claim ledger scoped to support states, claim surfaces, revision history, and publication boundaries.

## Mechanisms

- Maintain reasons or justifications for program beliefs.
- Support belief revision by keeping dependencies visible to the reasoning system.
- Use maintained reasons to explain actions and guide later problem solving.
- Treat the belief-maintenance subsystem as a component that supports, but does not replace, the problem solver.

## Evidence

- The source is a journal article in Artificial Intelligence, 12(3):231-272, with DOI `10.1016/0004-3702(79)90008-0`.
- This repository has not implemented Doyle's TMS, reproduced a truth-maintenance algorithm, or run dependency-directed backtracking.
- Use this source as external lineage for reason maintenance, not as proof that ASI Stack claim ledgers maintain truth over open-domain language.

## Failure Modes

- Treating stored reasons as verified evidence when they may only be internal justifications.
- Mistaking a claim ledger's publication boundary for a complete truth-maintenance reasoner.
- Using TMS terminology to imply deployed belief revision, dependency-directed backtracking, or general truth maintenance without an implementation trace.

## Book Chapters Supported

- `claim-ledgers-and-belief-revision` (Claim Ledgers and Belief Revision)

## Claims To Add Or Update

- Use this note to connect the ASI claim ledger to truth-maintenance lineage around reasons, justifications, dependencies, and revision.
- Make clear that the ASI ledger adds publication-support boundaries, support states, and cross-surface synchronization for living AI artifacts.
- Keep support at `argument` until local truth-maintenance or claim-revision machinery exists beyond finite schemas and synthetic fixtures.

## Open Questions

- Which claim-ledger fields should preserve internal reasons separately from external evidence refs?
- What future fixture would show dependency-preserving downgrade over a real artifact graph?
- How should a ledger distinguish explanation of why a system believed a claim from evidence that the claim is true?
