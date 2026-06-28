# Curated Reader Graduation Review

Last updated: 2026-06-28

This note records the v1.0 decision about whether the normal human-reader book
should graduate from generated reader source plus semantic overlays into a
tracked curated reader manuscript. It is not a reader release record, not an
ebook/document/PDF/audio artifact record, and not a support-state promotion.

## Inputs

- Reader manuscript manifest: `editions/reader_manuscript/v1_0/manifest.json`
- Reconciliation template: `editions/reader_manuscript/v1_0/reconciliation_report.md`
- Chapter review matrix: `editions/reader_manuscript/v1_0/chapter_review_matrix.json`
- Public review summary: `docs/reader_chapter_review_matrix.md`
- Reader overlay manifest: `editions/reader_overlays/v1_0/manifest.json`
- Generated reader source: `build/reader_edition/`

## Current State

- Curated reader manuscript status: `not_graduated`
- Generated-reader chapter-text review: complete for all 54 current chapters
- Active reader-overlay operations: 33
- Companion-note candidates: 3
- Curated-manuscript candidates: 1
- Release blockers: reader release records and format artifact review remain
  open for every chapter

## Decision

Do not graduate the v1.0 reader manuscript into curated chapter source yet.

Generated reader source plus tracked semantic overlays is still the right
working model for v1.0 because the current reader problems are localized:
table-to-prose transformations, proof-vocabulary density, companion-note
routing, and artifact-layout review. Those are better handled by overlays,
companion notes, and release-review records than by creating a second full
manuscript source before the human edition has release artifacts.

The curated manuscript path remains necessary for the future. It should be used
when reader editing becomes paragraph- and chapter-structural rather than
section-local: reordering examples, rewriting openings and closings across
multiple sections, compressing long implementation ladders, adding sustained
reader examples, or producing a final bedtime-readable major-version prose
source.

## Candidate Chapters

| Chapter | Current disposition | Graduation decision |
|---|---|---|
| `artifact-steward-agents-and-living-project-governance` | `curated_manuscript_candidate`, `companion_note_candidate`, active overlays | Keep as the first curated-manuscript candidate, but do not graduate yet. Review companion-note routing and long-chapter compression during reader-release editing. |
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
- Update `editions/reader_manuscript/v1_0/reconciliation_report.md`.
- Preserve generated-reader baseline refs, live-source refs, claim boundaries,
  source boundaries, proof/test status, implementation horizons, and release
  blockers.
- Run `python3 scripts/validate_reader_manuscript_manifest.py`.
- Run `python3 scripts/sync_reader_chapter_review_matrix.py --check`.

## Non-Claims

- This review does not create curated reader chapter files.
- This review does not create or approve EPUB, PDF, DOCX, HTML, audio, or
  audio-embedded EPUB artifacts.
- This review does not remove release blockers from any chapter.
- This review does not promote any support state.
- This review does not make the reader manuscript an equal source of truth
  beside the live AI/research book.
