# Reader Format Review Matrix

Last updated: 2026-06-28

This generated summary is synced from `editions/reader_manuscript/v1_0/format_review_matrix.json`. It records local reader-format review evidence and blockers. It is not an edition release record, not artifact approval, and not a support-state promotion.

## Counts

| Metric | Count |
|---|---:|
| format rows | 4 |
| release_blocker:app_or_ereader_review_not_completed | 1 |
| release_blocker:full_format_artifact_review_not_completed | 4 |
| release_blocker:full_pdf_layout_review_not_completed | 1 |
| release_blocker:reader_release_record_not_created | 4 |

## Format Queue

| Format | Render status | Structural status | Manual review | Release approved | Blockers | Evidence refs |
|---|---|---|---|---:|---|---|
| html | rendered_local | passed | representative_spot_check | no | reader_release_record_not_created, full_format_artifact_review_not_completed | docs/reader_format_dry_run.md#structural-inspection, docs/reader_artifact_inspection_manifest.md#inspection-summary, docs/reader_artifact_layout_review.md#broader-html-navigation-and-layout-probe |
| epub | rendered_local | passed | in_progress | no | reader_release_record_not_created, full_format_artifact_review_not_completed, app_or_ereader_review_not_completed | docs/reader_format_dry_run.md#structural-inspection, docs/reader_format_dry_run.md#epub-probe, docs/reader_artifact_inspection_manifest.md#inspection-summary, docs/reader_epub_probe_manifest.md#epub-container-summary, docs/reader_artifact_layout_review.md#residuals |
| docx | rendered_local | passed | representative_spot_check | no | reader_release_record_not_created, full_format_artifact_review_not_completed | docs/reader_format_dry_run.md#structural-inspection, docs/reader_artifact_inspection_manifest.md#inspection-summary, docs/reader_docx_probe_manifest.md#docx-conversion-probe-summary, docs/reader_artifact_layout_review.md#residuals |
| pdf | probe_rendered_local | partial | representative_spot_check | no | reader_release_record_not_created, full_format_artifact_review_not_completed, full_pdf_layout_review_not_completed | docs/reader_format_dry_run.md#pdf-probe, docs/reader_pdf_probe_manifest.md#pdf-probe-summary, docs/reader_artifact_layout_review.md#pdf-spot-check |

## Release Rule

No reader HTML, EPUB, DOCX, PDF, e-reader conversion, audio, or audio-embedded EPUB artifact is release-approved until the relevant format row has no release blockers and an edition release record names the exact reviewed artifact.

## Non-Claims

- This matrix is a pre-release format-review ledger, not an edition release record.
- This matrix does not publish or approve reader artifacts.
- This matrix does not promote any claim support state.
- This matrix does not supersede the live AI/research book for claims, source boundaries, proof/test status, implementation horizons, or release records.
