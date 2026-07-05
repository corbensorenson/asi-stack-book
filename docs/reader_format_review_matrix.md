# Reader Format Review Matrix

Last updated: 2026-07-05

This generated summary is synced from `editions/reader_manuscript/v1_0/format_review_matrix.json`. It records local reader-format review evidence and blockers. It is not itself an edition release record, artifact approval, or support-state promotion.

## Counts

| Metric | Count |
|---|---:|
| format rows | 4 |
| release_blocker:app_or_ereader_review_not_completed | 1 |
| release_blocker:full_format_artifact_review_not_completed | 3 |
| release_blocker:full_pdf_layout_review_not_completed | 1 |
| current_curated_candidate rows | 6 |
| current_curated_candidate_blocker:audio_edition_release_record_not_created | 1 |
| current_curated_candidate_blocker:audio_embedded_epub_not_packaged_or_checked | 1 |
| current_curated_candidate_blocker:audio_files_not_generated | 1 |
| current_curated_candidate_blocker:audio_metadata_not_reviewed | 1 |
| current_curated_candidate_blocker:audio_spot_check_not_performed | 1 |
| current_curated_candidate_blocker:chapter_markers_not_timecoded | 1 |
| current_curated_candidate_blocker:manual_keyboard_only_review_not_completed | 1 |
| current_curated_candidate_blocker:reader_release_approval_not_created | 5 |
| current_curated_candidate_blocker:reviewed_reader_release_record_not_created_for_audio | 1 |
| current_curated_candidate_blocker:screen_reader_review_not_completed | 1 |
| current_curated_candidate_blocker:wcag_conformance_review_not_completed | 1 |

## Format Queue

| Format | Render status | Structural status | Manual review | Release approved | Blockers | Evidence refs |
|---|---|---|---|---:|---|---|
| html | rendered_local | passed | pass | yes |  | docs/reader_format_dry_run.md#structural-inspection, docs/reader_artifact_inspection_manifest.md#inspection-summary, docs/reader_artifact_layout_review.md#broader-html-navigation-and-layout-probe, docs/reader_html_artifact_browser_review.md#browser-sweep, release_records/2026-06-29-v1-reader-html-855dc277.json |
| epub | rendered_local | passed | in_progress | no | full_format_artifact_review_not_completed, app_or_ereader_review_not_completed | docs/reader_format_dry_run.md#structural-inspection, docs/reader_format_dry_run.md#epub-probe, docs/reader_artifact_inspection_manifest.md#inspection-summary, docs/reader_epub_probe_manifest.md#epub-container-summary, docs/reader_artifact_layout_review.md#residuals |
| docx | rendered_local | passed | representative_spot_check | no | full_format_artifact_review_not_completed | docs/reader_format_dry_run.md#structural-inspection, docs/reader_artifact_inspection_manifest.md#inspection-summary, docs/reader_docx_probe_manifest.md#docx-conversion-probe-summary, docs/reader_artifact_layout_review.md#residuals |
| pdf | probe_rendered_local | partial | representative_spot_check | no | full_format_artifact_review_not_completed, full_pdf_layout_review_not_completed | docs/reader_format_dry_run.md#pdf-probe, docs/reader_pdf_probe_manifest.md#pdf-probe-summary, docs/reader_artifact_layout_review.md#pdf-spot-check |

## Current Curated Reader Candidate

Status: `partial_release_candidate_blocked`

Release-candidate record: `release_records/2026-07-04-v1-curated-reader-blocked-5dc1cd46.json`

Tracked curated reader manuscript rendered into ignored local HTML, EPUB, DOCX, and PDF review artifacts, plus e-reader and audio release-preparation lanes.

| Candidate format | Render status | Automated review | Release approved | Blockers | Evidence refs |
|---|---|---|---:|---|---|
| curated_reader_html | rendered_local | passed_release_preparation_probe | no | manual_keyboard_only_review_not_completed, screen_reader_review_not_completed, wcag_conformance_review_not_completed, reader_release_approval_not_created | docs/curated_reader_html_artifact_browser_review.md#browser-sweep, docs/reader_keyboard_navigation_review.md#summary, editions/reader_manuscript/v1_0/accessibility_tree_manifest.json, docs/reader_accessibility_tree_review.md#summary, docs/reader_final_figure_artifact_review.md#summary, release_records/2026-07-04-v1-curated-reader-blocked-5dc1cd46.json |
| curated_reader_epub | rendered_local | passed_release_preparation_probe | no | reader_release_approval_not_created | docs/curated_reader_format_artifact_probe.md#epub-content-and-navigation-audit, docs/reader_key_figure_epub_layout_review.md#summary, docs/reader_final_figure_artifact_review.md#summary, release_records/2026-07-04-v1-curated-reader-blocked-5dc1cd46.json, docs/reader_epub_apple_books_review.md#what-was-checked, editions/reader_manuscript/v1_0/epub_apple_books_review_manifest.json |
| curated_reader_docx | rendered_local | passed_release_preparation_probe | no | reader_release_approval_not_created | docs/curated_reader_format_artifact_probe.md#docx-libreoffice-headless-review, docs/reader_key_figure_docx_layout_review.md#summary, docs/reader_final_figure_artifact_review.md#summary, release_records/2026-07-04-v1-curated-reader-blocked-5dc1cd46.json, docs/reader_docx_text_fallback_review.md#pages-observation, editions/reader_manuscript/v1_0/docx_text_fallback_manifest.json, docs/reader_docx_application_decision.md#decision, editions/reader_manuscript/v1_0/docx_application_decision_manifest.json |
| curated_reader_pdf | rendered_local | passed_release_preparation_probe | no | reader_release_approval_not_created | docs/curated_reader_format_artifact_probe.md#pdf-text-and-layout-extraction-audit, docs/curated_reader_pdf_page_review.md#summary, docs/curated_reader_format_artifact_probe.md#pdf-chromium-viewer-smoke-review, docs/reader_key_figure_pdf_layout_review.md#summary, docs/reader_final_figure_artifact_review.md#summary, release_records/2026-07-04-v1-curated-reader-blocked-5dc1cd46.json |
| ereader_application_review | rendered_local | passed_application_review | no | reader_release_approval_not_created | docs/reader_epub_apple_books_review.md#what-was-checked, editions/reader_manuscript/v1_0/epub_apple_books_review_manifest.json, docs/reader_key_figure_epub_layout_review.md#summary, release_records/2026-07-04-v1-curated-reader-blocked-5dc1cd46.json |
| audio | not_attempted | partial_release_preparation_probe | no | reviewed_reader_release_record_not_created_for_audio, audio_files_not_generated, audio_spot_check_not_performed, chapter_markers_not_timecoded, audio_metadata_not_reviewed, audio_embedded_epub_not_packaged_or_checked, audio_edition_release_record_not_created | docs/reader_audio_script_probe_manifest.md#audio-script-reading-flow-review, release_records/2026-07-04-v1-curated-reader-blocked-5dc1cd46.json, docs/reader_audio_narration_treatment_review.md#decision, editions/reader_manuscript/v1_0/audio_narration_treatment_review_manifest.json |

Curated-candidate release boundary:

The current curated candidate is not release-approved. It records automated preparation evidence, the Apple Books EPUB application review, the DOCX application-evidence decision, the accessibility-tree release-preparation probe, and the script-level audio narration treatment review, but it does not approve any curated HTML, EPUB, DOCX, PDF, e-reader, audio, or final figure artifact; future approval still requires an edition release record naming the exact reviewed artifact.

## Release Rule

No reader HTML, EPUB, DOCX, PDF, e-reader conversion, audio, or audio-embedded EPUB artifact is release-approved until the relevant format row has no release blockers and an edition release record names the exact reviewed artifact.

## Non-Claims

- This matrix is a pre-release format-review ledger, not an edition release record.
- This matrix does not publish reader artifacts and does not independently approve artifacts outside referenced edition release records.
- This matrix does not promote any claim support state.
- This matrix does not supersede the live AI/research book for claims, source boundaries, proof/test status, implementation horizons, or release records.
