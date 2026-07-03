# Curated Reader Format Artifact Probe

Last updated: 2026-07-03

This note records a local structural render and inspection probe for the
tracked curated reader manuscript. It is not an edition release record, a
format approval, a public deployment artifact, or a support-state promotion.

## Inputs

Commands run:

```bash
python3 scripts/render_curated_reader_formats.py --formats html epub docx
python3 scripts/inspect_curated_reader_format_artifacts.py
```

Local ignored reports:

- `build/curated_reader_edition/curated_reader_render_report.json`
- `build/curated_reader_edition/curated_reader_artifact_inspection_report.json`

Tracked manifest:

- `editions/reader_manuscript/v1_0/curated_format_probe_manifest.json`

## Render Summary

| Format | Render status | Artifacts observed | Preserved artifacts | Warnings | SVG conversion warnings |
|---|---|---:|---:|---:|---:|
| html | rendered | 49 | 81 | 0 | 0 |
| epub | rendered | 1 | 1 | 0 | 0 |
| docx | rendered | 1 | 1 | 10 | 10 |

The DOCX render produced ten Pandoc warnings for SVG image conversion because
`rsvg-convert` was not available on PATH. The DOCX container still rendered and
passed structural inspection, but that warning is a release blocker, not a
cosmetic footnote.

## Structural Inspection Summary

| Format | Status | Key facts |
|---|---|---|
| html | passed | 49 total HTML files, 44 chapter HTML files, 0 live-marker leaks, 0 raw core-claim marker leaks. |
| epub | passed | 8,690,281 bytes, SHA-256 `461bafec5ec6219d4ebb65c25a27ff0ec558a0b1b3a2fe54675d32c44de9be82`, 120 zip entries, 52 XHTML entries, 62 image entries, OPF title `The ASI Stack`, creator `Corben Sorenson`, language `en-US`. |
| docx | passed | 6,784,002 bytes, SHA-256 `b846e2b30ffdecebee82d48e3e6efe4c8d788b11e14e53402a9d4562e4373649`, 77 zip entries, 61 media entries, 16,976 paragraph markers, required Word package entries present. |

## Review Decision

The tracked curated reader manuscript now has a local format-probe path beyond
HTML browser viability: the same curated source rendered to HTML, EPUB, and
DOCX, and the snapshots passed structural inspection. This is useful evidence
for release preparation, e-reader testing, DOCX application review, and figure
conversion work.

This does not clear release blockers. EPUB still needs real e-reader or app
inspection. DOCX still needs application-level review and resolution of the
ten SVG conversion warnings. PDF and audio artifacts remain outside this probe.

## Residuals

- The rendered artifacts are ignored local build outputs, not committed release
  assets.
- All 44 curated chapter records still carry
  `curated_reconciliation_not_approved`, `format_artifact_not_reviewed`, and
  `reader_release_record_not_created`.
- EPUB, DOCX, PDF, e-reader, MP3, M4B, and audio-embedded EPUB artifacts remain
  unapproved until exact artifacts, application-level review, and release
  records exist.
- Figure polish and final visual review remain open.
- This probe does not promote any claim support state, source interpretation,
  proof status, benchmark result, runtime behavior, model-quality claim, safety
  claim, or deployment-readiness claim.
