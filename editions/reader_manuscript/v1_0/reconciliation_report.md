# v1.0 Curated Reader Reconciliation Report

Status: drafting; two curated reader chapters have first prose curation passes,
with release blockers still active.

This report is the required reconciliation surface for any future curated v1.0 reader manuscript. It is not a reader release record, not an ebook/document/PDF/audio artifact record, not a support-state promotion, and not an equal source of truth beside the live AI/research book.

## Current State

- Curated manuscript status: `drafting`
- Current graduation decision: keep drafting-only curated reader chapters for
  the opener and Artifact Steward Agents while keeping generated reader source
  plus semantic overlays as the release baseline; see
  `docs/curated_reader_graduation_review.md`
- Chapter records: 2 drafting records
- Active reader baseline: generated reader source plus semantic reader overlays
- Manifest source of truth: `book_structure.json`
- Review queue: `editions/reader_manuscript/v1_0/chapter_review_matrix.json`
- Generated baseline command: `python3 scripts/build_reader_edition.py`
- Generated baseline check: `python3 scripts/build_reader_edition.py --check`

## Reconciliation Rule

A curated reader chapter may improve pacing, examples, transitions, paragraph order, section flow, and booklike voice. It must not alter claim meaning, support-state meaning, source boundary meaning, proof/test status, implementation horizons, release artifact existence, or manifest chapter identity.

If a reader edit discovers that the live AI/research source is wrong, thin, misleading, or missing a meaning-critical caveat, the canonical chapter must be fixed and validated before the reader derivative can rely on the change.

## Per-Chapter Reconciliation Table

| Chapter ID | Curated file | Generated baseline ref | Live source ref | Reconciliation status | Divergence summary | Blockers |
|---|---|---|---|---|---|---|
| `asi-is-a-stack-not-a-model` | `editions/reader_manuscript/v1_0/chapters/asi-is-a-stack-not-a-model.qmd` | `build/reader_edition/chapters/asi-is-a-stack-not-a-model.qmd` | `chapters/asi-is-a-stack-not-a-model.qmd@d16c2720` | `drafting` | First curated prose pass completed for opening, pacing, paragraph order, section flow, transitions, and compression; no claim meaning, support-state, source, proof/test, implementation-horizon, or release-artifact divergence has been approved. Review record: `docs/curated_reader_asi_stack_prose_pass.md`. | `reader_release_record_not_created`, `format_artifact_not_reviewed`, `curated_reconciliation_not_approved` |
| `artifact-steward-agents-and-living-project-governance` | `editions/reader_manuscript/v1_0/chapters/artifact-steward-agents-and-living-project-governance.qmd` | `build/reader_edition/chapters/artifact-steward-agents-and-living-project-governance.qmd` | `chapters/artifact-steward-agents-and-living-project-governance.qmd@0f6382f1` | `drafting` | First curated prose pass completed for opening, pacing, paragraph order, section flow, transitions, and compression; no claim meaning, support-state, source, proof/test, implementation-horizon, or release-artifact divergence has been approved. Review record: `docs/curated_reader_artifact_steward_prose_pass.md`. | `reader_release_record_not_created`, `format_artifact_not_reviewed`, `curated_reconciliation_not_approved` |

## Required Checks Before Reader Release

- Every curated chapter maps to exactly one manifest chapter ID.
- Every curated chapter records a generated reader baseline and live source commit or tag.
- Every curated chapter preserves support boundaries, source boundaries, proof/test status, implementation horizons, and release blockers.
- Every meaning-changing prose divergence is either reconciled back into the live chapter or explicitly rejected as reader-only presentation.
- `python3 scripts/validate_reader_manuscript_manifest.py` passes.
- `python3 scripts/sync_reader_chapter_review_matrix.py --check` passes.
- The edition release record names exact rendered artifacts only after generation, review, and artifact inspection.

## Non-Claims

- This report does not approve the drafting curated reader chapter.
- This template does not create or approve EPUB, PDF, DOCX, HTML, audio, or audio-embedded EPUB artifacts.
- This template does not promote any claim support state.
- This template does not supersede the live Quarto book for claims, source boundaries, proof/test status, implementation horizons, or release records.
