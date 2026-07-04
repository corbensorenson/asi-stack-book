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
python3 scripts/sync_curated_reader_format_probe_manifest.py
python3 scripts/repair_curated_reader_epub_links.py
python3 scripts/repair_curated_reader_docx_links.py
python3 scripts/audit_curated_reader_pdf_layout.py
python3 scripts/audit_curated_reader_pdf_visual_raster.py
python3 scripts/audit_curated_reader_epub_content.py
node scripts/validate_curated_reader_epub_browser_review.js --write-manifest
python3 scripts/audit_curated_reader_docx_content.py
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

The PDF render also generates 50 temporary Chrome-screenshot Mermaid fallbacks
from the rendered HTML pages before running Pandoc. This keeps browser-rendered
Mermaid labels visible in the PDF and prevents the previously observed diagram
clipping in the ignored PDF artifact. It remains automated format-preparation
evidence, not manual figure, page-flow, or release approval.

## Structural Inspection Summary

| Format | Status | Key facts |
|---|---|---|
| html | passed | 49 total HTML files, 44 chapter HTML files, 0 live-marker leaks, 0 raw core-claim marker leaks. |
| epub | passed | 8,663,801 bytes, SHA-256 `9b03601a6023392d52bfa594cf1f4e6c20bd6e9d79bac62d362f30ad58938157`, 120 zip entries, 52 XHTML entries, 62 image entries, OPF title `The ASI Stack`, creator `Corben Sorenson`, language `en-US`. |
| docx | passed | 8,321,124 bytes, SHA-256 `99f9bf48050c2a34244e98fb43e35ee35c377db207fd79d891c3385e11337bc6`, 77 zip entries, 61 PNG media entries, 0 SVG media entries, 17,354 paragraph markers, required Word package entries present. |
| pdf | passed | 5,892,357 bytes, SHA-256 `7c120d9e8ef4b595e46d52434c80d7ec72135ef11472e908133db76ed606317d`, 504 pages, title `The ASI Stack`, author `Corben Sorenson`, unencrypted letter pages, required text markers present, and sample pages 1, 2, 25, 300, and 500 rendered to PNG. |

## EPUB Content And Navigation Audit

After the container inspection above, the probe applies
`python3 scripts/repair_curated_reader_epub_links.py` to the ignored EPUB
snapshot. That command rewrites Quarto's known forward-link leakage from the
source appendix target `H_external_sources.qmd` to the packaged EPUB spine
target. The repaired EPUB package SHA-256 `2e15e9f20bebd4816ae10081e2faff69314686d659c62c85c2c93ef23e70aca9`
then passed an all-XHTML content and internal-link audit covering 49 packaged content XHTML entries and 0 unresolved internal hrefs.

| Metric | Result |
|---|---:|
| XHTML entries checked | 52 |
| Packaged content XHTML entries checked | 49 |
| Text characters checked | 1,780,626 |
| Navigation hrefs checked | 840 |
| OPF item entries | 116 |
| OPF spine itemrefs | 52 |
| Empty XHTML entries | 0 |
| Live-marker leaks | 0 |
| Raw core-claim marker leaks | 0 |
| Unresolved internal hrefs | 0 |

Required text markers were present: `The ASI Stack`, `Reader Edition Draft`,
`evidence boundary`, `Reader Source List`, and `External Citation Policy`.
This all-XHTML EPUB package audit is stronger local EPUB evidence than
container inspection alone, but it is not e-reader application review and does
not approve the EPUB artifact for release.

## EPUB Browser XHTML Application Review

The probe then renders the repaired EPUB spine XHTML in Chromium through:

```bash
node scripts/validate_curated_reader_epub_browser_review.js --write-manifest
```

That pass checks the unpacked EPUB spine at desktop and e-reader-like viewport
widths. It covered 104 page-view pairs. It also treats the cover page
separately from content pages, so a visual cover can be textless while every
content spine entry still has substantive body text.

| Metric | Result |
|---|---:|
| Spine entries checked | 52 |
| Packaged content XHTML entries checked | 49 |
| Viewports checked | 2 |
| Browser page-view pairs | 104 |
| Failed page-view pairs | 0 |
| Rendered images observed | 22 |
| Image load failures | 0 |
| Maximum horizontal overflow | 10 px |
| Minimum content body text characters | 1,225 |
| Live-marker leaks | 0 |
| Raw core-claim marker leaks | 0 |

Required text markers were present: `The ASI Stack`, `Reader Edition Draft`,
`evidence boundary`, `Reader Source List`, and `External Citation Policy`.
This Chromium pass is stronger than package inspection because it actually
renders the unpacked EPUB spine XHTML, but it is not dedicated e-reader device/app approval, not a release record, and does not approve the EPUB artifact.

## DOCX Document XML And Relationship Audit

After the container inspection above, the probe applies
`python3 scripts/repair_curated_reader_docx_links.py` to the ignored DOCX
snapshot. That command removes Quarto's known forward-link leakage from the
source appendix target `H_external_sources.qmd` by unwrapping the broken DOCX
hyperlink while preserving the visible appendix text. The repaired DOCX package SHA-256 `1690f5b3bf63781e9dd819a7c66f1724043d74eee4d2132fa48e6597d4e5d7c1`
then passed a document XML, media, and relationship audit with 17,354 paragraphs and 0 raw .qmd relationship targets.

| Metric | Result |
|---|---:|
| ZIP entries checked | 77 |
| Document XML characters checked | 2,793,806 |
| Text characters checked | 1,195,187 |
| Paragraph markers | 17,354 |
| Run markers | 28,255 |
| Relationships checked | 286 |
| Image relationships | 61 |
| External hyperlink relationships | 217 |
| Media entries | 61 |
| PNG media entries | 61 |
| SVG media entries | 0 |
| Raw `.qmd` relationship targets | 0 |
| Unresolved internal relationship targets | 0 |
| Live-marker leaks | 0 |
| Raw core-claim marker leaks | 0 |

Required text markers were present: `The ASI Stack`, `Reader Edition Draft`,
`evidence boundary`, `Reader Source List`, and `External Citation Policy`.
This DOCX package audit is stronger local DOCX evidence than package
inspection alone, but it is not Word, LibreOffice GUI, or Google Docs application review and does not approve the DOCX artifact for release.

## PDF Text And Layout Extraction Audit

The refreshed PDF probe also ran full-document text and bounding-box extraction
after the reader-prose pass that removed overlong machine identifiers from the
relaxed reader chapters.

| Metric | Result |
|---|---:|
| Pages checked | 504 |
| Word boxes checked | 169,766 |
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

## PDF Visual Raster Audit

The refreshed PDF probe also raster-rendered every page at 72 dpi in a
temporary review workspace. This is a low-resolution visual smoke test for
blank pages, unexpected page dimensions, low-ink pages, and near-edge content.
It preserves release blockers rather than treating automated raster cleanliness
as manual page-flow approval.

| Metric | Result |
|---|---:|
| Pages raster-rendered | 504 |
| Raster DPI | 72 |
| Page width in pixels | 612 |
| Page height in pixels | 792 |
| Blank raster pages | 0 |
| Low-ink raster pages | 0 |
| Near-edge raster pages | 0 |
| Minimum nonwhite pixels | 1,961 |
| Maximum nonwhite pixels | 105,544 |
| Minimum left margin px | 82 |
| Minimum top margin px | 71 |
| Minimum right margin px | 4 |
| Minimum bottom margin px | 92 |

No low-ink or near-edge raster pages were observed after the PDF-only Mermaid
fallback pass. This all-page low-resolution raster rendering is stronger local
PDF visual evidence than sample-page rendering alone, but it is not manual PDF
page-by-page review and does not approve the PDF artifact for release.

## Review Decision

The tracked curated reader manuscript now has a local format-probe path beyond
HTML browser viability: the same curated source rendered to HTML, EPUB, DOCX,
and PDF, and the snapshots passed structural inspection. The repaired EPUB
package also passed the all-XHTML content/navigation audit and a Chromium
browser XHTML application review, the repaired DOCX package passed the document
XML/relationship audit above, and the PDF also passed the all-page
text/bounding-box and visual raster audits above. This is useful evidence for
release preparation, dedicated e-reader testing, DOCX application review, PDF
layout review, and figure conversion work.

This does not clear release blockers. EPUB still needs dedicated e-reader
device/app approval or an explicit release decision that accepts the Chromium
XHTML review as sufficient for a named artifact. DOCX still needs
application-level review in Word, LibreOffice GUI, or Google Docs. PDF still needs page-layout and reading-flow review in a PDF viewer. Audio artifacts remain outside this probe.

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
