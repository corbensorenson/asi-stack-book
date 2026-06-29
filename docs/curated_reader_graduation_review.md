# Curated Reader Graduation Review

Last updated: 2026-06-29

This note records the v1.0 decision about whether the normal human-reader book
should graduate from generated reader source plus semantic overlays into a
tracked curated reader manuscript. It is not a reader release record, not an
ebook/document/PDF/audio artifact record, and not a support-state promotion.

## Inputs

- Reader manuscript manifest: `editions/reader_manuscript/v1_0/manifest.json`
- Curated source contract: `editions/reader_manuscript/v1_0/curation_contract.json`
- Contract summary: `docs/curated_reader_source_contract.md`
- Reconciliation template: `editions/reader_manuscript/v1_0/reconciliation_report.md`
- Chapter review matrix: `editions/reader_manuscript/v1_0/chapter_review_matrix.json`
- Public review summary: `docs/reader_chapter_review_matrix.md`
- Reader overlay manifest: `editions/reader_overlays/v1_0/manifest.json`
- Generated reader source: `build/reader_edition/`

## Current State

- Curated reader manuscript status: `drafting`
- Generated-reader chapter-text review: complete for all 54 current chapters
- Active reader-overlay operations: 33
- Companion-note candidates: 3
- Curated-manuscript candidates: 1
- Curated chapter records: 1 drafting record for
  `artifact-steward-agents-and-living-project-governance`
- Release blockers: reader release records and format artifact review remain
  open for every chapter
- Consolidation gate: `docs/chapter_consolidation_decision_review.md` defers
  the Part I alignment/governance manifest merge for this v1.x cycle, so
  reader curation may proceed outside the pending merge cluster without
  locking in avoidable duplicate skeletons.

## Decision

Graduate only the first drafting-only curated reader source for
`artifact-steward-agents-and-living-project-governance`; do not treat it as a
reader release artifact.

Generated reader source plus tracked semantic overlays is still the right
release baseline for v1.0 because most current reader problems are localized:
table-to-prose transformations, proof-vocabulary density, companion-note
routing, and artifact-layout review. Those are better handled by overlays,
companion notes, and release-review records than by creating a full parallel
manuscript before the human edition has release artifacts.

The curated manuscript path remains necessary for the future. It should be used
when reader editing becomes paragraph- and chapter-structural rather than
section-local: reordering examples, rewriting openings and closings across
multiple sections, compressing long implementation ladders, adding sustained
reader examples, or producing a final bedtime-readable major-version prose
source.

After the consolidation decision review, curated-reader work should start with
pilot chapters outside the pending Part I merge cluster. The four source
chapters named in the alignment/governance consolidation pilot should not
receive broad reader-only graduation until their merge is executed or
permanently rejected; otherwise the human manuscript would preserve the same
duplicate skeletons the consolidation pilot is trying to remove.

## Candidate Chapters

| Chapter | Current disposition | Graduation decision |
|---|---|---|
| `artifact-steward-agents-and-living-project-governance` | `curated_manuscript_candidate`, `companion_note_candidate`, active overlays | Initialized as the first drafting-only curated reader chapter from the generated baseline. Reconciliation remains incomplete, release blockers remain active, and no reader artifact is approved. |
| `circle-calculus-and-proof-carrying-ai-contracts` | `companion_note_candidate`, active overlays | Prefer companion/glossary treatment before curated prose graduation. |
| `executable-specifications-and-lean-proof-envelope` | `companion_note_candidate`, active overlay | Prefer companion/glossary treatment before curated prose graduation. |

## Graduation Triggers

Graduate a chapter into curated reader source only when at least one of these is
true:

- a reader-only change touches multiple sections and would be brittle as overlay
  replacements;
- the chapter needs sustained example, analogy, pacing, or paragraph-order
  changes that should not alter the AI/research source;
- companion-note routing is not enough to make dense proof, schema, or
  governance material readable;
- release editing identifies human-prose improvements that are too broad for
  `editions/reader_overlays/` but do not belong in the canonical live chapter.

## Required Controls If Graduation Starts

- Add a curated chapter record under
  `editions/reader_manuscript/v1_0/manifest.json`.
- Store curated chapter files under
  `editions/reader_manuscript/v1_0/chapters/`.
- Follow `editions/reader_manuscript/v1_0/curation_contract.json` for required
  record fields, allowed edit scopes, blocked divergence, meaning-preservation
  checks, and pre-release blockers.
- Update `editions/reader_manuscript/v1_0/reconciliation_report.md`.
- Preserve generated-reader baseline refs, live-source refs, claim boundaries,
  source boundaries, proof/test status, implementation horizons, and release
  blockers.
- Run `python3 scripts/validate_reader_manuscript_manifest.py`.
- Run `python3 scripts/sync_reader_chapter_review_matrix.py --check`.

## Non-Claims

- This review creates one drafting-only curated reader chapter file for
  future prose editing; it does not approve that file for release.
- This review does not create or approve EPUB, PDF, DOCX, HTML, audio, or
  audio-embedded EPUB artifacts.
- This review does not remove release blockers from any chapter.
- This review does not promote any support state.
- This review does not make the reader manuscript an equal source of truth
  beside the live AI/research book.
