# v1.0 Curated Reader Reconciliation Report

Status: template only; curated reader manuscript not graduated.

This report is the required reconciliation surface for any future curated v1.0 reader manuscript. It is not a reader release record, not an ebook/document/PDF/audio artifact record, not a support-state promotion, and not an equal source of truth beside the live AI/research book.

## Current State

- Curated manuscript status: `not_graduated`
- Current graduation decision: keep generated reader source plus semantic
  overlays for v1.0; see `docs/curated_reader_graduation_review.md`
- Chapter records: none
- Active reader baseline: generated reader source plus semantic reader overlays
- Manifest source of truth: `book_structure.json`
- Review queue: `editions/reader_manuscript/v1_0/chapter_review_matrix.json`
- Generated baseline command: `python3 scripts/build_reader_edition.py`
- Generated baseline check: `python3 scripts/build_reader_edition.py --check`

## Reconciliation Rule

A curated reader chapter may improve pacing, examples, transitions, paragraph order, section flow, and booklike voice. It must not alter claim meaning, support-state meaning, source boundary meaning, proof/test status, implementation horizons, release artifact existence, or manifest chapter identity.

If a reader edit discovers that the live AI/research source is wrong, thin, misleading, or missing a meaning-critical caveat, the canonical chapter must be fixed and validated before the reader derivative can rely on the change.

## Per-Chapter Reconciliation Table

No curated reader chapters exist yet.

| Chapter ID | Curated file | Generated baseline ref | Live source ref | Reconciliation status | Divergence summary | Blockers |
|---|---|---|---|---|---|---|
| _none_ | _none_ | _none_ | _none_ | `not_started` | No curated derivative exists. | Release record and format artifact review are still blocked; no curated chapter file has been approved. |

## Required Checks Before Reader Release

- Every curated chapter maps to exactly one manifest chapter ID.
- Every curated chapter records a generated reader baseline and live source commit or tag.
- Every curated chapter preserves support boundaries, source boundaries, proof/test status, implementation horizons, and release blockers.
- Every meaning-changing prose divergence is either reconciled back into the live chapter or explicitly rejected as reader-only presentation.
- `python3 scripts/validate_reader_manuscript_manifest.py` passes.
- `python3 scripts/sync_reader_chapter_review_matrix.py --check` passes.
- The edition release record names exact rendered artifacts only after generation, review, and artifact inspection.

## Non-Claims

- This template does not create a curated reader manuscript.
- This template does not create or approve EPUB, PDF, DOCX, HTML, audio, or audio-embedded EPUB artifacts.
- This template does not promote any claim support state.
- This template does not supersede the live Quarto book for claims, source boundaries, proof/test status, implementation horizons, or release records.
