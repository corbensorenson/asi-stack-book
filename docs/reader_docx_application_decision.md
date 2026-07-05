# Reader DOCX Application Evidence Decision

Last updated: 2026-07-05

Status: `accepted_docx_application_evidence_for_release_preparation`

This note records a narrow release-preparation decision for the curated reader
DOCX candidate. It accepts the available local application-engine evidence as
enough to close the current `docx_application_review_not_completed` blocker,
while keeping DOCX publication and reader release approval blocked.

## Evidence Accepted

| Evidence lane | Recorded result |
|---|---:|
| Rich DOCX package SHA-256 | `71ed95b7ded6f85ea94652d7c139cd1f68ed929632822d66d2db0f1b924797b8` |
| Repaired DOCX SHA-256 | `12a33e1eb31b5e0147bc18c586b9b73b8d0b4f7bb3936aaf75dc471db78d4a14` |
| DOCX paragraph markers | 17,387 |
| DOCX relationships | 286 |
| Raw `.qmd` relationship targets | 0 |
| Unresolved internal relationship targets | 0 |
| Live-marker leaks | 0 |
| Raw core-claim marker leaks | 0 |
| LibreOffice converted document | 506-page PDF |
| LibreOffice text checked | 1,030,310 text characters |
| Blank converted-page rasters | 0 |
| Low-ink converted-page rasters | 0 |
| Near-edge converted-page rasters | 0 |
| DOCX key-figure title pages | 10 key-figure title pages |
| DOCX title-page minimum margin | 72.1 pt |
| DOCX title-page maximum near-edge ink | 0.0% |
| Final figure-artifact review | 10 figures reviewed |
| Pages-readable text fallback | 1,107,976 text characters, 0 media entries |

## Decision

For this candidate, the release-preparation gate accepts the repaired DOCX
document XML and relationship checks, the LibreOffice headless Writer conversion
and full converted-page raster review, the DOCX key-figure layout check, the
final figure-artifact release-preparation review, and the Pages-readable text
fallback as enough to close the DOCX application-review blocker.

This clears only `docx_application_review_not_completed`. It does not claim Word, LibreOffice GUI, or Google Docs approval; it does not treat the Pages-readable text fallback as rich-DOCX visual approval; it does not approve DOCX publication; and it does not create reader release approval.

## Preserved Blockers

- `reader_release_approval_not_created`
- `manual_keyboard_only_review_not_completed`
- `screen_reader_review_not_completed`
- `wcag_conformance_review_not_completed`
- `reviewed_reader_release_record_not_created_for_audio`
- `narration_quality_review_not_completed`
- `audio_files_not_generated`
- `chapter_markers_not_timecoded`
- `audio_edition_release_record_not_created`

## Non-Claims

- does not claim Word approval
- does not claim LibreOffice GUI approval
- does not claim Google Docs approval
- does not approve the curated reader DOCX for publication
- does not publish or archive a reader artifact
- does not promote any chapter core claim
