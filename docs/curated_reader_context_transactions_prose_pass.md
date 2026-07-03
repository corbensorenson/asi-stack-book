# Curated Reader Prose Pass: Context Transactions, Snapshots, Mounts, and Taint

Last updated: 2026-07-02

Follow-up: 2026-07-02

Chapter ID: `context-transactions-snapshots-mounts-and-taint`

Curated reader file:
`editions/reader_manuscript/v1_0/chapters/context-transactions-snapshots-mounts-and-taint.qmd`

## Reader Promise

A human reader should leave this chapter understanding that AI memory needs
transaction semantics. The chapter should make clear that relevant context is
not enough if the system cannot explain which memory view was mounted, which
snapshot was read, what taint propagated, what deletion obligations remained,
and whether the view was allowed to materialize.

## Scope

This pass turns the initialized generated reader baseline for Context
Transactions, Snapshots, Mounts, and Taint into a first booklike curated reader
draft. It is a reader-prose derivative only.

Allowed curation scopes used:

- chapter openings and closings;
- pacing;
- paragraph ordering;
- section flow;
- transition prose;
- sentence-level voice;
- chapter compression.

Proof/test boundary clarification is recorded as meaning preservation, not as
permission to change proof or test status.

## What Changed

- Reframed the chapter around memory as accountable state rather than relevant
  retrieved snippets.
- Added a simple memory-incident example that contrasts committed source
  updates, draft corrections, stale summaries, private mounts, taint
  propagation, quarantine, and replay boundaries as transaction-state
  questions rather than retrieval-quality questions.
- Organized the mechanism around immutable events, versioned pages, mounts,
  snapshots, branches, taint/deletion closure, materialization, faults, and
  downstream artifact inheritance.
- Preserved RAG, MemGPT, long-context, and compression references as external
  comparators and orientation, not local benchmark results.
- Preserved the VCM, Ladon/Manhattan, Context Engineer, Black Hole Context
  Manager, and editable VCM source boundaries.
- Preserved the current evidence boundary that record schemas, fixtures,
  synthetic deletion-closure checks, and finite Lean predicates support record
  discipline only.
- Preserved the missing-work boundary: no transactional memory-store,
  read-your-writes, branch-isolation, mount-visibility, replay,
  poisoning-resistance, side-channel, VCM conformance, Digital SCIF, or context
  manager benchmark result is claimed.
- Preserved the minimum viable implementation, beyond-state-of-the-art endpoint,
  and handoff into Verification Bandwidth and Context Adequacy.
- Preserved the release and runtime boundary: the new example explains the
  contract and does not claim a deployed transaction store, mount policy
  engine, taint engine, deletion-closure engine, replay system, or context
  compiler.

## Meaning Preservation Checks

| Check | Result |
|---|---|
| Core claim meaning preserved | Pass. The curated draft keeps the claim that VCM should use transactional memory semantics: immutable events, versioned pages, snapshots, mounts, taint, temporal validity, and deletion closure. |
| Support-state boundary preserved | Pass. The curated draft states that the live book keeps the claim at `argument` support. |
| Source boundary preserved | Pass. No new source IDs, source facts, citations, or external claims were introduced by this pass; external records remain comparators. |
| Proof/test status preserved | Pass. The curated draft keeps the boundary that finite Lean predicates, protocol validation, and the synthetic context admission/adequacy harness do not prove memory-store behavior, branch isolation, mount visibility, deletion closure in a deployed store, poisoning resistance, side-channel defense, or VCM conformance. |
| Implementation horizon preserved | Pass. The minimum viable implementation remains a transaction record schema plus fixtures and finite predicates; the mature endpoint remains an unimplemented transactional memory substrate for AI context. |
| Release blockers preserved | Pass. No reader release record, format review, reconciliation approval, EPUB, DOCX, PDF, HTML, or audio artifact is approved by this pass. |

## Non-Claims

- This pass does not change the live AI/research chapter.
- This pass does not change `book_structure.json`.
- This pass does not alter Appendix C, source assignments, proof targets, test
  status, implementation horizons, or release records.
- This pass does not approve the curated chapter for reader release.
- This pass does not create EPUB, DOCX, PDF, HTML, audio, or audio-embedded EPUB
  artifacts.
- This pass does not promote any chapter core claim or non-core claim.
- This pass does not claim a deployed VCM resolver, context compiler,
  transactional memory store, read-your-writes behavior, branch isolation,
  mount visibility, replay correctness, poisoning resistance, side-channel
  defense, Digital SCIF implementation, VCM conformance, or context manager
  benchmark reproduction.

## Remaining Blockers

- `reader_release_record_not_created`
- `format_artifact_not_reviewed`
- `curated_reconciliation_not_approved`

Before this curated source can be release input, the reader manuscript needs a
full reconciliation pass against the live chapter, generated baseline,
support-state boundaries, implementation horizons, and exact rendered reader
artifacts.
