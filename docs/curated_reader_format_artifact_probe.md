# Curated Reader Format Artifact Probe

Last updated: 2026-07-05

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
python3 scripts/validate_curated_reader_docx_libreoffice_review.py --write-manifest
python3 scripts/validate_reader_docx_textutil_fallback.py --write-manifest
python3 scripts/validate_curated_reader_pdf_reading_flow.py --write-manifest
python3 scripts/validate_curated_reader_pdf_viewer_review.py --write-manifest
python3 scripts/validate_curated_reader_pdf_page_review.py --write-manifest
```

Local ignored reports:

- `build/curated_reader_edition/curated_reader_render_report.json`
- `build/curated_reader_edition/curated_reader_artifact_inspection_report.json`
- `build/curated_reader_edition/curated_reader_docx_libreoffice_review_report.json`
- `build/curated_reader_edition/curated_reader_pdf_reading_flow_report.json`
- `build/curated_reader_edition/curated_reader_pdf_viewer_review_report.json`

Tracked manifest:

- `editions/reader_manuscript/v1_0/curated_format_probe_manifest.json`
- `editions/reader_manuscript/v1_0/pdf_page_review_manifest.json`
- `editions/reader_manuscript/v1_0/docx_text_fallback_manifest.json`

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
| epub | passed | 8,670,899 bytes, SHA-256 `412fadecd308acfc966e624c17aece7cc53bc4ef9f818e4f865fdb2f0ed6be28`, 120 zip entries, 52 XHTML entries, 62 image entries, OPF title `The ASI Stack`, creator `Corben Sorenson`, language `en-US`. |
| docx | passed | 8,331,414 bytes, SHA-256 `e248469162e3a28c48a0c277980c59dc64396622b88cbc670ae8c9f6a94430c5`, 77 zip entries, 61 PNG media entries, 0 SVG media entries, 17,462 paragraph markers, required Word package entries present. |
| pdf | passed | 5,924,235 bytes, SHA-256 `9c90de1072432368d7fef41d38edefae82e431c992bb9c7a8441a7571e81ac7c`, 511 pages, title `The ASI Stack`, author `Corben Sorenson`, unencrypted letter pages, required text markers present, and sample pages 1, 2, 25, 300, and 500 rendered to PNG. |

## EPUB Content And Navigation Audit

After the container inspection above, the probe applies
`python3 scripts/repair_curated_reader_epub_links.py` to the ignored EPUB
snapshot. That command rewrites Quarto's known forward-link leakage from the
source appendix target `H_external_sources.qmd` to the packaged EPUB spine
target. The repaired EPUB package SHA-256 `bca694bc97bdfbc1757d58368df9d5d3f2e6152615938a80c7eab0b2a5519255`
then passed an all-XHTML content, XML, and internal-link audit covering 49 packaged content XHTML entries and 0 unresolved internal hrefs.

| Metric | Result |
|---|---:|
| XHTML entries checked | 52 |
| Packaged content XHTML entries checked | 49 |
| Text characters checked | 1,803,680 |
| Navigation hrefs checked | 841 |
| OPF item entries | 116 |
| OPF spine itemrefs | 52 |
| Empty XHTML entries | 0 |
| Live-marker leaks | 0 |
| Raw core-claim marker leaks | 0 |
| Unresolved internal hrefs | 0 |
| Bare class attribute hits | 0 |
| Paragraph-wrapped figure tag hits | 0 |
| XML parse errors | 0 |

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
| Rendered images observed | 122 |
| Image load failures | 0 |
| Maximum horizontal overflow | 0 px |
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
hyperlink while preserving the visible appendix text. The repaired DOCX package SHA-256 `e5e70200ed19b58d232c315b5e6aa88a753fe95a01c6ec25e1abeede02ab2713`
then passed a document XML, media, and relationship audit with 17,462 paragraphs and 0 raw .qmd relationship targets.

| Metric | Result |
|---|---:|
| ZIP entries checked | 77 |
| Document XML characters checked | 2,864,814 |
| Text characters checked | 1,222,415 |
| Paragraph markers | 17,462 |
| Run markers | 29,453 |
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

## DOCX LibreOffice Headless Review

The probe then opens the repaired DOCX through LibreOffice's headless Writer
PDF export path:

```bash
python3 scripts/validate_curated_reader_docx_libreoffice_review.py --write-manifest
```

That pass converts the current DOCX to PDF in a temporary profile, extracts
text from the converted PDF, and raster-renders every converted page at 72 dpi.
It is application-engine evidence for the DOCX artifact because it exercises
LibreOffice's document import and PDF layout path, not only the DOCX ZIP/XML
container.

The result records 512 converted pages, 1,048,398 text characters, and 0 blank converted-page rasters.

| Metric | Result |
|---|---:|
| Converted PDF pages | 512 |
| Converted PDF bytes | 8,620,104 |
| Text characters checked | 1,048,398 |
| Converted-page rasters checked | 512 |
| Blank converted-page rasters | 0 |
| Low-ink converted-page rasters | 0 |
| Near-edge converted-page rasters | 0 |
| Minimum nonwhite pixels | 5,550 |
| Maximum nonwhite pixels | 143,172 |
| Live-marker leaks | 0 |
| Raw core-claim marker leaks | 0 |

Required text markers were present: `The ASI Stack`, `Reader Edition Draft`,
`evidence boundary`, `Reader Source List`, and `External Citation Policy`.
The converted PDF is tagged, unencrypted, letter-sized, titled `The ASI Stack`,
and produced by LibreOffice. This is stronger than package inspection alone,
but it is not Word review, not LibreOffice GUI review, not Google Docs review,
not manual document review, and does not approve the DOCX artifact for release.

## DOCX Textutil Pages Fallback Probe

The probe also records a text-oriented fallback path through Apple's
`textutil`:

```bash
python3 scripts/validate_reader_docx_textutil_fallback.py --write-manifest
```

That command converts the current ignored curated-reader DOCX into
`build/curated_reader_edition/format_artifacts/docx_text_fallback/_reader_site/The-ASI-Stack-pages-text-fallback.docx`,
inspects the fallback package, and writes
`editions/reader_manuscript/v1_0/docx_text_fallback_manifest.json`. The exact
fallback artifact was opened locally in Pages. Pages exposed the title page,
reader edition draft marker, table-of-contents text, and chapter 1 body text
without the rich-DOCX read error.

| Metric | Result |
|---|---:|
| Source DOCX SHA-256 | `e5e70200ed19b58d232c315b5e6aa88a753fe95a01c6ec25e1abeede02ab2713` |
| Fallback DOCX SHA-256 | `7eee5765d1729399154c6bb6313f6756a050d3006a5dfafa9d64ca5da1068a06` |
| Fallback bytes | 345,639 |
| ZIP entries | 8 |
| Text characters checked | 1,126,365 |
| Paragraph markers | 11,644 |
| Media entries | 0 |
| Live-marker leaks | 0 |
| Raw core-claim marker leaks | 0 |

This fallback is useful as a Pages-readable text path, but it is not the rich
DOCX artifact and it does not preserve the full figure or visual package. It
does not clear the rich DOCX application-review blocker, does not approve the
curated reader DOCX for release, and does not create reader release approval.

## PDF Text And Layout Extraction Audit

The refreshed PDF probe also ran full-document text and bounding-box extraction
after the reader-prose pass that removed overlong machine identifiers from the
relaxed reader chapters.

| Metric | Result |
|---|---:|
| Pages checked | 511 |
| Word boxes checked | 172,699 |
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
| Pages raster-rendered | 511 |
| Raster DPI | 72 |
| Page width in pixels | 612 |
| Page height in pixels | 792 |
| Blank raster pages | 0 |
| Low-ink raster pages | 1 |
| Near-edge raster pages | 0 |
| Minimum nonwhite pixels | 681 |
| Maximum nonwhite pixels | 143,139 |
| Minimum left margin px | 82 |
| Minimum top margin px | 71 |
| Minimum right margin px | 15 |
| Minimum bottom margin px | 92 |

One low-ink raster page, page 24, remains recorded for inspection; no blank or
near-edge raster pages were observed after the PDF-only Mermaid fallback pass.
This all-page low-resolution raster rendering is stronger local
PDF visual evidence than sample-page rendering alone, but it is not manual PDF
page-by-page review and does not approve the PDF artifact for release.

## PDF Extracted Text Reading-Flow Review

The refreshed PDF probe also runs an extracted-text reading-flow review:

```bash
python3 scripts/validate_curated_reader_pdf_reading_flow.py --write-manifest
```

That pass uses `pdftotext` and `pdfinfo` to check text volume, page text
presence, required reader markers, live-marker leakage, chapter heading order,
and appendix heading order in the current 511-page PDF.

The result records 1,126,001 text characters, 44 chapter headings, 3 appendix headings, and 511 nonempty text pages; it is not manual PDF page-by-page reading-flow review.

| Metric | Result |
|---|---:|
| PDF pages | 511 |
| Text pages checked | 511 |
| Nonempty text pages | 511 |
| Text characters checked | 1,126,001 |
| Word tokens checked | 172,146 |
| Chapter headings checked | 44 |
| Appendix headings checked | 3 |
| First chapter text-page index | 28 |
| Last chapter text-page index | 417 |
| Replacement characters | 0 |
| Live-marker leaks | 0 |
| Raw core-claim marker leaks | 0 |

The extracted-text flow check found 44 chapter headings and 3 appendix headings
in order, with 511 nonempty text pages. Required text markers were present:
`The ASI Stack`, `Reader Edition Draft`, `evidence boundary`, `Reader Source
List`, and `External Citation Policy`. This is stronger than page-count and
raster evidence alone, but it is not manual PDF page-by-page reading-flow
review, not PDF viewer approval, and does not approve the PDF artifact for
release.

## PDF Chromium Viewer Smoke Review

The refreshed PDF probe also opens the ignored local PDF in a headed Chromium
PDF viewer through:

```bash
python3 scripts/validate_curated_reader_pdf_viewer_review.py --write-manifest
```

This pass captures the first visible viewer frame, scrolls the PDF surface, and
captures a second frame. It verifies that Chrome's PDF viewer shell is present,
that both screenshots are nonblank at 1280 x 900, that the screenshots contain
both dark viewer chrome and a white page region, and that scrolling changes the
rendered pixels.

| Metric | Result |
|---|---:|
| PDF pages reported by `pdfinfo` | 511 |
| Viewer screenshots | 2 |
| First screenshot bytes | 41,640 |
| Second screenshot bytes | 92,611 |
| First screenshot dark pixels | 34.101% |
| First screenshot white pixels | 64.662% |
| Second screenshot dark pixels | 34.905% |
| Second screenshot white pixels | 62.323% |
| Scroll-changed pixels | 4.479% |

This is real local PDF-viewer rendering evidence for the current ignored PDF
artifact, but it is not manual page-by-page PDF review, not PDF content
approval, and does not approve the PDF artifact for release.

## PDF Page-By-Page Release-Preparation Review

The refreshed PDF probe now records a page-by-page release-preparation review:

```bash
python3 scripts/validate_curated_reader_pdf_page_review.py --write-manifest
```

That pass checks every page in the current ignored 511-page PDF through text
extraction, word-box extraction, and raster page rendering. It records 511 page
rows, 511 text pages, 511 word-box pages, 511 raster pages, 0 failed pages,
0 blank pages, 0 near-edge pages, 0 out-of-bounds word-box pages, and one
accepted low-ink page.

| Metric | Result |
|---|---:|
| PDF pages | 511 |
| Page review rows | 511 |
| Text pages checked | 511 |
| Word-box pages checked | 511 |
| Raster pages checked | 511 |
| Failed pages | 0 |
| Blank raster pages | 0 |
| Near-edge pages | 0 |
| Out-of-bounds word-box pages | 0 |
| Low-ink pages accepted | 1 |

This closes the current candidate's
`manual_pdf_page_by_page_review_not_completed` blocker, while preserving final
figure-artifact approval and reader release approval. It is not external human
review, not final figure-artifact approval, not publication, and not PDF release
approval.

## Review Decision

The tracked curated reader manuscript now has a local format-probe path beyond
HTML browser viability: the same curated source rendered to HTML, EPUB, DOCX,
and PDF, and the snapshots passed structural inspection. The repaired EPUB
package also passed the all-XHTML content/navigation audit and a Chromium
browser XHTML application review, the repaired DOCX package passed the document
XML/relationship audit and LibreOffice headless conversion/raster review above,
and the PDF also passed the all-page text/bounding-box, visual raster,
extracted-text reading-flow, Chromium viewer smoke, and page-by-page
release-preparation audits above. This is useful evidence for release
preparation, dedicated e-reader testing, DOCX GUI/application review, PDF
release approval, and figure conversion work.

This does not clear release blockers. This format probe itself does not clear e-reader/application review; the separate Apple Books review records that
application path for the current repaired EPUB digest. DOCX still needs
application-level review in Word, LibreOffice GUI, or Google Docs; the headless
LibreOffice review is recorded as preparation evidence only. The PDF
page-by-page release-preparation review and final figure-artifact review are
now recorded, but the PDF still needs reader release approval before it can be
treated as a release artifact. Audio artifacts remain outside this probe.

## Residuals

- The rendered artifacts are ignored local build outputs, not committed release
  assets.
- All 44 curated chapter records now have source-level reconciliation approval;
  they still carry `format_artifact_not_reviewed` and
  `reader_release_record_not_created`.
- EPUB, DOCX, PDF, e-reader, MP3, M4B, and audio-embedded EPUB artifacts remain
  unapproved until exact artifacts, application-level review, and release
  records exist.
- Figure polish and final visual review remain open.
- This probe does not promote any claim support state, source interpretation,
  proof status, benchmark result, runtime behavior, model-quality claim, safety
  claim, or deployment-readiness claim.
