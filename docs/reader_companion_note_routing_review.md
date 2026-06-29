# Reader Companion-Note Routing Review

Last updated: 2026-06-29

This review records the v1.0 routing decision for the three chapters flagged as
companion-note candidates in the reader chapter review matrix. It is not a
reader release record, not an ebook/document/PDF/audio artifact review, not a
curated reader-manuscript graduation, and not a support-state promotion.

## Inputs

- `editions/reader_manuscript/v1_0/chapter_review_matrix.json`
- `docs/reader_chapter_review_matrix.md`
- `docs/reader_continuity_review.md`
- `docs/reader_part_iii_iv_proof_bridge_full_review_pass.md`
- `docs/reader_part_iv_evidence_governance_full_review_pass.md`
- `docs/curated_reader_graduation_review.md`
- Generated reader chapters under `build/reader_edition/chapters/`

## Decision

Create a tracked companion-note routing manifest at
`editions/reader_manuscript/v1_0/companion_note_routing.json` and keep generated
reader source plus semantic overlays as the v1.0 reader path.

The three candidate chapters remain in the reader spine because their dense
terms carry meaning-critical boundaries. For v1.0, companion notes should help
e-reader and audio users with glossary, quick-reference, and spoken-treatment
support. They should not remove caveats that change claim meaning from ordinary
reader prose.

## Chapter Decisions

| Chapter | Reader treatment | Companion route | Release decision |
|---|---|---|---|
| `circle-calculus-and-proof-carrying-ai-contracts` | Retain proof receipt states, theorem references, resolver/replay boundaries, consumer gates, workload blockers, and non-claims in the reader chapter. | Drafting companion note added at `editions/reader_manuscript/v1_0/companion_notes/circle-calculus-and-proof-carrying-ai-contracts.md` for receipt-state glossary, theorem laundering, fingerprints, replay, workload-blocked promotion, and audio treatment. | Drafting-only curated reader prose pass recorded in `docs/curated_reader_circle_contracts_prose_pass.md`; no release blocker cleared. |
| `executable-specifications-and-lean-proof-envelope` | Retain the distinction between Lean predicates, schemas, validators, behavior tests, benchmarks, external theorem references, and semantic adequacy review. | Drafting companion note added at `editions/reader_manuscript/v1_0/companion_notes/executable-specifications-and-lean-proof-envelope.md` for proof-lane glossary, finite-predicate examples, semantic adequacy, and audio treatment. | Drafting-only curated reader prose pass recorded in `docs/curated_reader_executable_specs_prose_pass.md`; no release blocker cleared. |
| `artifact-steward-agents-and-living-project-governance` | Retain charter, work contract, contribution ledger, treasury policy, event taint, steward action, sunset, federation, and non-ownership boundaries. | Drafting companion note added at `editions/reader_manuscript/v1_0/companion_notes/artifact-steward-agents-and-living-project-governance.md` for project-object quick reference, implementation ladder, and audio treatment; the first curated prose pass still remains drafting-only. | Drafting-only curated reader prose pass recorded; no release blocker cleared. |

## Routing Rule

Dense material can move to companion support only when the reader chapter still
states the meaning-critical boundary in ordinary prose. Companion notes are for
orientation, reference, and spoken-treatment decisions. They are not allowed to
be the only place where a support limit, proof boundary, governance boundary,
release blocker, or non-claim appears.

For audio, these chapters should be narrated as arguments first and field lists
second. Exact record names, lifecycle states, and proof-lane vocabulary can be
summarized in the script and routed to companion notes, but the spoken script
must preserve the claim boundary.

## Non-Claims

- This review does not approve a reader release.
- This review does not approve EPUB, PDF, DOCX, HTML, AZW3, MOBI, Markdown,
  plain-text, MP3, M4B, or audio-embedded EPUB artifacts.
- This review records that eight drafting-only curated reader chapters now
  exist; it does not approve any chapter for release.
- This review records three drafting companion notes for dense proof/governance
  chapters; it does not approve them as e-reader, audio, or release artifacts.
- This review does not promote any claim support state.
- This review does not claim proof adequacy, Circle theorem replay, steward
  workflow execution, treasury execution, governance correctness, audiobook
  quality, or release readiness.
