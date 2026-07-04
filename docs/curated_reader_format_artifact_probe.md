# Curated Reader Format Artifact Probe

Last updated: 2026-07-04

This note records a local structural render and inspection probe for the
tracked curated reader manuscript. It is not an edition release record, a
format approval, a public deployment artifact, or a support-state promotion.

## Inputs

Commands and reproduction path:

```bash
python3 scripts/render_curated_reader_formats.py --formats html epub docx --include-pdf
python3 scripts/inspect_curated_reader_format_artifacts.py
python3 scripts/audit_curated_reader_pdf_layout.py
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
| docx | rendered | 1 | 1 | 0 | 0 |
| pdf | rendered | 1 | 1 | 0 | 0 |

The DOCX and PDF renders now generate ten temporary PNG fallbacks from the
tracked SVG key figures inside the ignored build workspace before running
Pandoc. The renderer restored the curated source workspace after each raster
fallback pass. The resulting DOCX render produced zero SVG conversion warnings
and the DOCX package contains PNG media entries rather than embedded SVG media
entries. The PDF render also produced zero SVG conversion warnings. This
removes the previous conversion-warning blocker; it does not approve the DOCX
or PDF artifact.

## Structural Inspection Summary

| Format | Status | Key facts |
|---|---|---|
| html | passed | 49 total HTML files, 44 chapter HTML files, 0 live-marker leaks, 0 raw core-claim marker leaks. |
| epub | passed | 8,703,384 bytes, SHA-256 `1507dc1658969e081ce9a80b000f28b367a32474fef02932eccf3b00494803e4`, 120 zip entries, 52 XHTML entries, 62 image entries, OPF title `The ASI Stack`, creator `Corben Sorenson`, language `en-US`. |
| docx | passed | 8,360,691 bytes, SHA-256 `9ac3b9de5b994e411cd17f4cff4bb6ffdf05abbb7de0b9b9b2329e44ddb0013c`, 77 zip entries, 61 PNG media entries, 0 SVG media entries, 17,360 paragraph markers, required Word package entries present. |
| pdf | passed | 9,360,937 bytes, SHA-256 `f39001097c0d8289980034a681d261ac737905b5840e231e2a0dba6ad8a41f2a`, 528 pages, title `The ASI Stack`, author `Corben Sorenson`, unencrypted letter pages, required text markers present, and sample pages 1, 2, 25, 300, and 500 rendered to PNG. |

## PDF Text And Layout Extraction Audit

The refreshed PDF probe also ran full-document text and bounding-box extraction
after the reader-prose pass that removed overlong machine identifiers from the
relaxed reader chapters.

| Metric | Result |
|---|---:|
| Pages checked | 528 |
| Word boxes checked | 169,904 |
| Textless pages | 0 |
| Out-of-bounds word boxes | 0 |
| Layout lines over 160 characters | 0 |
| Minimum word-box height | 14.531 |
| Maximum word-box height | 35.47 |

Required text markers were present: `The ASI Stack`, `Reader Edition Draft`,
`evidence boundary`, `Reader Source List`, and `External Citation Policy`.
This all-page extraction audit is stronger local PDF evidence than
representative sampling, but it is not manual PDF page-by-page review and does
not approve the PDF artifact for release.

## Review Decision

The tracked curated reader manuscript now has a local format-probe path beyond
HTML browser viability: the same curated source rendered to HTML, EPUB, DOCX,
and PDF, and the snapshots passed structural inspection. The PDF also passed
the all-page text/bounding-box audit above. This is useful evidence for release
preparation, e-reader testing, DOCX application review, PDF layout review, and
figure conversion work.

This does not clear release blockers. EPUB still needs real e-reader or app
inspection. DOCX still needs application-level review in Word, LibreOffice GUI,
or Google Docs. PDF still needs page-layout and reading-flow review in a PDF
viewer. Audio artifacts remain outside this probe.

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
