# Curated Reader Prose Pass: Executable Specifications and Lean Proof Envelope

Last updated: 2026-06-29

Chapter ID: `executable-specifications-and-lean-proof-envelope`

Curated reader file: `editions/reader_manuscript/v1_0/chapters/executable-specifications-and-lean-proof-envelope.qmd`

Status: drafting only; not release-reviewed.

## Reader Promise

A human reader should understand the proof envelope as a claims-control layer
that keeps Lean predicates, schemas, validators, behavior tests, benchmarks,
external theorem references, semantic adequacy reviews, and research backlog
items in separate authority lanes.

## Scope

Allowed curation scopes used in this pass:

- pacing;
- chapter openings and closings;
- section flow;
- transition prose;
- sentence-level voice;
- paragraph ordering;
- chapter compression;
- companion-note integration.

## What Changed

- Reworked the opening around formal language making claims smaller rather than
  grander.
- Strengthened the distinction between Lean predicates, schemas, process
  validators, behavior tests, benchmarks, external theorem references, semantic
  adequacy reviews, and research backlog.
- Preserved the current local implementation boundary: generated proof
  manifest, `proof_target_record` fixture, local `lake build`,
  `AsiStackProofs.ProofEnvelope`, Appendix E coverage, proof artifact
  traceability audit, and unrun semantic adequacy review.
- Preserved the companion-note route while keeping lane vocabulary in the
  reader spine because it is meaning-critical.
- Preserved the Mermaid diagram, core claim, evidence boundary, minimum viable
  implementation, beyond-state-of-the-art endpoint, and handoff to Benchmark
  Ratchets.

## Meaning Preservation Checks

| Check | Result |
|---|---|
| Core claim meaning preserved | Pass. The claim remains that Lean proofs and executable specs should target small invariants. |
| Support-state boundary preserved | Pass. The chapter core claim remains `argument`. |
| Source boundary preserved | Pass. No new source IDs, source facts, citations, or external claims were introduced. |
| Proof/test status preserved | Pass. The pass names existing local finite-record proof, schema, traceability, and build gates while preserving that semantic proof adequacy remains planned and not run. |
| Implementation horizon preserved | Pass. The MVI remains the proof manifest, proof target fixture, local Lean build, Appendix E coverage, and proof artifact traceability; the mature claims control plane remains a target architecture. |
| Companion note routing preserved | Pass. The companion note remains drafting support, not release-reviewed evidence. |
| Release blockers preserved | Pass. Reader release, format review, and curated reconciliation blockers remain active. |

## Non-Claims

- This pass does not change the live chapter, `book_structure.json`, Appendix
  C, source assignments, proof targets, test status, implementation horizons,
  or release records.
- This pass does not approve the curated chapter, reader release, EPUB, DOCX,
  PDF, HTML artifact, audio artifact, or audio-embedded EPUB.
- This pass does not promote any claim support state.
- This pass does not claim semantic proof adequacy, broad proof adequacy,
  deployed enforcement, source-truth validation, model quality, benchmark
  improvement, safety, or ASI capability.

## Remaining Blockers

- `reader_release_record_not_created`
- `format_artifact_not_reviewed`
- `curated_reconciliation_not_approved`
- companion note remains `drafting_not_release_reviewed`
