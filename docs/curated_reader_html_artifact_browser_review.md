# Curated Reader HTML Artifact Browser Review

Last updated: 2026-07-04

This note records a full local browser review of the tracked curated reader
manuscript rendered as local HTML. It is not an edition release record, a
format-row approval, a public deployment artifact, or a support-state promotion.

## Inputs

Commands run:

```bash
python3 scripts/render_curated_reader_formats.py --formats html epub docx --include-pdf
python3 scripts/inspect_curated_reader_format_artifacts.py
node scripts/validate_reader_html_artifact_browser.js --strict --site build/curated_reader_edition/format_artifacts/html/_reader_site --manifest build/curated_reader_edition/reader_manifest.json --report build/curated_reader_edition/curated_reader_html_browser_report.json
```

Local ignored reports:

- `build/curated_reader_edition/curated_reader_build_report.json`
- `build/curated_reader_edition/curated_reader_render_report.json`
- `build/curated_reader_edition/curated_reader_artifact_inspection_report.json`
- `build/curated_reader_edition/reader_manifest.json`
- `build/curated_reader_edition/curated_reader_html_browser_report.json`

Reviewed HTML root:

`build/curated_reader_edition/format_artifacts/html/_reader_site`

Deterministic directory digest:

`690117e693b92f9d836c2d17a39ddb96747b87bb4e31f4598c705e54ec70c177`

The digest is computed over 81 files by hashing each relative path and file
content in sorted order. The rendered site is ignored local build output, not a
committed release asset.

## Source Build Summary

The curated source build passed for the fresh local review workspace:

| Field | Result |
|---|---:|
| Curated chapters copied | 44 |
| Build report status | `curated_reader_source_renderable` |
| Build review status | `review_required` |
| `curated_reconciliation_not_approved` blockers | 44 |
| `format_artifact_not_reviewed` blockers | 44 |
| `reader_release_record_not_created` blockers | 44 |

The generated `reader_manifest.json` records
`source_mode: tracked_curated_reader_manuscript` and
`review_status: curated_review_required`, preserving the boundary that this is
review input rather than release approval.

## Browser Sweep

`node scripts/validate_reader_html_artifact_browser.js --strict --site build/curated_reader_edition/format_artifacts/html/_reader_site --manifest build/curated_reader_edition/reader_manifest.json --report build/curated_reader_edition/curated_reader_html_browser_report.json`
opened every curated reader HTML page at desktop and mobile widths.

| Metric | Result |
|---|---:|
| Pages opened | 49 |
| Expected pages | 49 |
| Viewports | 2 |
| Page-view pairs | 98 |
| Failed page-view pairs | 0 |
| Reader key figures detected | 10 |
| Reader key-figure page-view pairs | 20 |
| Failed reader key-figure checks | 0 |

For each page-view pair, the browser check required:

- stylesheet loading;
- visible main content and a visible H1;
- at least 1,000 body-text characters;
- no page-level horizontal overflow above 2 pixels;
- no raw bracketed core-claim marker leakage;
- no live-only scaffold headings such as `Chapter status`, `Drafting guardrail`,
  `Codex test plan`, `Source crosswalk`, `Claim-source mapping status`, or
  `Formalization hooks`;
- at least one rendered SVG diagram on every chapter page.

For each rendered curated-reader key figure, the browser check now also
requires a visible figure container, a loaded SVG image with substantive
natural and rendered dimensions, a caption, a `Figure boundary:` paragraph,
and viewport-contained figure framing at desktop and mobile widths. This is
an automated rendered-layout check, not final art direction.

## Review Decision

The tracked curated reader manuscript clears local HTML browser viability for
this ignored review snapshot. The ten draft key figures also clear automated
HTML browser layout and visibility checks for this snapshot. This means the
curated reader source can be used as a concrete input for release-quality
continuity, figure, and format review.

This review does not clear any release blocker, does not mark the HTML format
row release-approved, does not create an edition release record, does not
publish a public artifact, and does not replace application-level EPUB, DOCX,
PDF, e-reader, audio, or audio-embedded EPUB inspection.

## Residuals

- The reviewed HTML tree is local ignored build output, not a GitHub Pages
  deployment artifact or external archive asset.
- All 44 curated chapter records still carry `curated_reconciliation_not_approved`,
  `format_artifact_not_reviewed`, and `reader_release_record_not_created`.
- The generated-reader HTML release record remains the only approved reader
  HTML artifact record; this curated-reader review is a newer local viability
  review, not a release approval.
- EPUB, DOCX, PDF, e-reader, MP3, M4B, and audio-embedded EPUB artifacts remain
  unapproved until exact artifacts, application-level review, and release
  records exist.
- Figure polish, manual visual judgment, measured contrast review, and final
  visual review remain open.
- This review does not promote any claim support state, source interpretation,
  proof status, benchmark result, runtime behavior, model-quality claim, safety
  claim, or deployment-readiness claim.
