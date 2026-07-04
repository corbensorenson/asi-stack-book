# Reader Key-Figure Artifact Review

Last checked: 2026-07-04

Command:

```bash
python3 scripts/validate_reader_key_figures.py
```

Rendered HTML probe:

```bash
python3 scripts/validate_reader_key_figure_html_probe.py --write-result
```

Rendered HTML browser layout check:

```bash
node scripts/validate_reader_html_artifact_browser.js --strict --site build/curated_reader_edition/format_artifacts/html/_reader_site --manifest build/curated_reader_edition/reader_manifest.json --report build/curated_reader_edition/curated_reader_html_browser_report.json
```

Format-package probe:

```bash
python3 scripts/validate_reader_key_figure_format_probe.py --write-manifest --write-doc
```

Raster artifact probe:

```bash
python3 scripts/validate_reader_key_figure_raster_probe.py --write-manifest --write-doc
```

PDF key-figure layout probe:

```bash
python3 scripts/validate_reader_key_figure_pdf_layout.py --write-manifest --write-doc
```

DOCX key-figure layout probe:

```bash
python3 scripts/validate_reader_key_figure_docx_layout.py --write-manifest --write-doc
```

This review records the current draft key-figure artifact inspection for the
curated reader manuscript. It is not a release approval and not final figure-artifact review. It checks only that the ten draft SVG assets named in
`editions/reader_manuscript/v1_0/manifest.json` are present, parseable,
accessible as draft reader aids, embedded in their live chapters, embedded in
their curated reader-manuscript chapters, and surrounded by alt text,
captions/text-equivalent anchors, and non-claim boundaries.

The rendered-HTML DOM probe in `docs/reader_key_figure_html_probe.md` builds the
tracked curated reader manuscript in a temporary workspace, renders HTML, and
checks all ten draft figures for rendered image references, copied SVG assets,
alt text, captions, responsive image classes, and visible non-claim boundary
paragraphs. That probe is still not visual review and not release approval.

The format-package probe in `docs/reader_key_figure_format_probe.md` inspects
the current ignored curated EPUB, DOCX, and PDF artifacts. It records that all
ten draft key figures survive as packaged SVG titles and figure-boundary
paragraphs in EPUB, rasterized figure stems and boundaries in DOCX, and
extracted draft captions plus figure-boundary paragraphs in PDF. This is still
not e-reader review, not Word/LibreOffice/Google Docs review, not manual PDF
review, not final figure-artifact approval, and not reader release approval.

The raster artifact probe in `docs/reader_key_figure_raster_review.md` inspects
the current ignored PNG fallbacks generated for the curated reader figures. It
records 10 raster artifacts, 10 standard 1200 x 760 canvases, minimum opaque
pixel coverage 99.954%, minimum luminance standard deviation 27.64, minimum
quantized color count 116, and SHA-256 hashes for every PNG. This catches
missing, blank, low-ink, or visually collapsed raster outputs, but it is still
not manual aesthetic review, not e-reader visual review, not DOCX/PDF
application review, not final figure-artifact approval, and not reader release
approval.

The PDF key-figure layout probe in
`docs/reader_key_figure_pdf_layout_review.md` inspects the current ignored
curated-reader PDF for the ten draft key-figure caption pages. It records 10
unique caption pages, 10 rendered caption-page rasters, 10 standard 612 x 792
page rasters, 165.878 pt minimum caption margin, 3.36% minimum page ink, 0.0%
maximum near-edge ink, and 14.2 minimum luminance standard deviation. This is
still not manual page-by-page PDF review, not PDF viewer review, not final
figure-artifact approval, and not reader release approval.

The DOCX key-figure layout probe in
`docs/reader_key_figure_docx_layout_review.md` converts the current ignored
curated-reader DOCX through LibreOffice headless Writer PDF export, then
inspects the ten draft key-figure title pages in that converted PDF. It
records 10 unique title pages, 10 rendered title-page rasters, 10 standard 612
x 792 page rasters, 72.1 pt minimum title margin, 9.53% minimum page ink, 0.0%
maximum near-edge ink, and 37.95 minimum luminance standard deviation. This is
still not Word review, not LibreOffice GUI review, not Google Docs review, not
manual document review, not final figure-artifact approval, and not reader
release approval.

The curated-reader HTML browser review in
`docs/curated_reader_html_artifact_browser_review.md` now also checks the ten
draft key figures at desktop and mobile widths: 10 figure containers, 20
figure page-view pairs, 0 figure-check failures. It verifies loaded SVG
images, visible figure containers, captions, `Figure boundary:` paragraphs,
substantive rendered dimensions, and viewport-contained figure framing. This
is still not manual visual judgment, measured contrast review, final
figure-artifact approval, or reader release approval.

2026-07-04 measured contrast/readability update:
`python3 scripts/validate_reader_key_figure_contrast.py` now records
`editions/reader_manuscript/v1_0/key_figure_contrast_manifest.json` and the
review surface `docs/reader_key_figure_contrast_review.md`. The ten draft key
figures pass the source-level gate with minimum text contrast ratio 5.19,
minimum flow-line contrast ratio 3.96, minimum marker contrast ratio 3.96, and
minimum SVG text size 15 px. This closes the measured SVG contrast/readability
slice only; it does not approve final figure art, EPUB, DOCX, PDF, e-reader,
audio, HTML, or a reader release artifact.

2026-07-04 presentation-layer update: `assets/styles.scss` now applies a shared
key-figure presentation shell to both live `.asi-key-figure` blocks and curated
reader `reader-fig-*` Quarto figure blocks, including a restrained rule,
caption treatment, mobile contained horizontal scroll for wide diagrams, and
print page-break avoidance. This improves the rendered review surface, but it
does not approve final figure art or any reader release artifact.

2026-07-04 source-geometry update:
`python3 scripts/validate_reader_key_figure_geometry.py` now records
`editions/reader_manuscript/v1_0/key_figure_geometry_manifest.json` and the
review surface `docs/reader_key_figure_geometry_review.md`. The CI-friendly
source-geometry review checks the ten draft SVG figures for the standard
`0 0 1200 760` viewBox, visible content bounds, text-anchor bounds, entity
counts, and visible draft/non-release status. It records 10 content-bound
checks, 10 text-anchor checks, minimum visible text nodes 25, minimum visible
rectangles 7, minimum visible connector paths 8, and 22.0 px minimum content
edge margin. This is not raster review, not manual aesthetic review, not final
figure-artifact approval, and not reader release approval.

2026-07-04 visual identity source-level update:
`python3 scripts/validate_reader_visual_identity.py` now records
`editions/reader_manuscript/v1_0/visual_identity_manifest.json` and the review
surface `docs/reader_visual_identity_review.md`. The source-level review checks
stylesheet tokens, shared key-figure presentation rules, mobile/print behavior,
SVG accessibility metadata, palette diversity, and carried contrast metrics for
the ten draft key figures. It records 54 combined colors, 5 non-neutral color
families, minimum text contrast ratio 5.19, minimum flow-line contrast ratio
3.96, minimum marker contrast ratio 3.96, and minimum SVG text size 15 px. This
is not manual aesthetic review, not e-reader visual review, not DOCX/PDF
application review, not final figure-artifact approval, and not reader release
approval.

2026-07-04 raster artifact update:
`python3 scripts/validate_reader_key_figure_raster_probe.py` now records
`editions/reader_manuscript/v1_0/key_figure_raster_manifest.json` and the
review surface `docs/reader_key_figure_raster_review.md`. The automated local
PNG review checks the ten generated raster fallbacks for standard 1200 x 760
dimensions, opaque page-area coverage, nonblank luminance variation, dark and
mid-tone pixel presence, quantized color diversity, and per-artifact SHA-256
digests. It is not manual aesthetic review, not e-reader visual review, not
DOCX/PDF application review, not final figure-artifact approval, and not reader
release approval.

2026-07-04 PDF key-figure layout update:
`python3 scripts/validate_reader_key_figure_pdf_layout.py` now records
`editions/reader_manuscript/v1_0/key_figure_pdf_layout_manifest.json` and the
review surface `docs/reader_key_figure_pdf_layout_review.md`. The local PDF
probe checks exact key-figure caption pages, caption bounding-box margins,
caption-page raster dimensions, page ink, near-edge ink absence, and luminance
variation. It is not manual page-by-page PDF review, not PDF viewer review, not
final figure-artifact approval, and not reader release approval.

2026-07-04 DOCX key-figure layout update:
`python3 scripts/validate_reader_key_figure_docx_layout.py` now records
`editions/reader_manuscript/v1_0/key_figure_docx_layout_manifest.json` and the
review surface `docs/reader_key_figure_docx_layout_review.md`. The local DOCX
probe converts the ignored curated-reader DOCX through LibreOffice headless
Writer PDF export, then checks exact key-figure title pages, title bounding-box
margins, title-page raster dimensions, page ink, near-edge ink absence, and
luminance variation. It is not Word review, not LibreOffice GUI review, not
Google Docs review, not manual document review, not final figure-artifact
approval, and not reader release approval.

2026-07-04 audio/e-reader companion update:
`editions/reader_manuscript/v1_0/companion_notes/key-figures.md` now records a
draft spoken summary, e-reader treatment note, and non-claim boundary for each
of the ten key figures. `python3 scripts/validate_reader_key_figures.py` checks
that the companion note covers every manifest key-figure asset. This is still
not narration approval, final figure-artifact approval, or an audio/e-reader
release record.

## Current Draft Assets

| Asset | Live chapter | Curated reader chapter | Current state |
|---|---|---|---|
| `assets/diagrams/asi-stack-control-plane.svg` | `chapters/asi-is-a-stack-not-a-model.qmd` | `editions/reader_manuscript/v1_0/chapters/asi-is-a-stack-not-a-model.qmd` | Draft reader aid; no implementation, benchmark, external review, release approval, or support-state promotion claim. |
| `assets/diagrams/authority-to-effect-path.svg` | `chapters/system-boundaries-and-authority.qmd` | `editions/reader_manuscript/v1_0/chapters/system-boundaries-and-authority.qmd` | Draft reader aid; no deployed enforcement, security validation, external review, release approval, or support-state promotion claim. |
| `assets/diagrams/evidence-state-ladder.svg` | `chapters/evidence-states-and-claim-discipline.qmd` | `editions/reader_manuscript/v1_0/chapters/evidence-states-and-claim-discipline.qmd` | Draft reader aid; no accepted evidence transition, external review, proof result, test result, release approval, or support-state promotion claim. |
| `assets/diagrams/intent-to-artifact-trace.svg` | `chapters/intent-to-execution-contracts.qmd` | `editions/reader_manuscript/v1_0/chapters/intent-to-execution-contracts.qmd` | Draft reader aid; no parser, planner, dispatcher, adapter, replay, release approval, or support-state promotion claim. |
| `assets/diagrams/context-transaction-lifecycle.svg` | `chapters/context-transactions-snapshots-mounts-and-taint.qmd` | `editions/reader_manuscript/v1_0/chapters/context-transactions-snapshots-mounts-and-taint.qmd` | Draft reader aid; no deployed memory store, branch isolation, deletion closure, benchmark, release approval, or support-state promotion claim. |
| `assets/diagrams/readiness-residual-quarantine-map.svg` | `chapters/readiness-gates-residual-escrow-and-quarantine.qmd` | `editions/reader_manuscript/v1_0/chapters/readiness-gates-residual-escrow-and-quarantine.qmd` | Draft reader aid; no readiness-engine behavior, residual-ledger storage, quarantine enforcement, release approval, or support-state promotion claim. |
| `assets/diagrams/route-selection-budget-tradeoff.svg` | `chapters/resource-economics-and-token-budgets.qmd` | `editions/reader_manuscript/v1_0/chapters/resource-economics-and-token-budgets.qmd` | Draft reader aid; no deployed router, scheduler behavior, model quality, new evidence transition, release approval, or support-state promotion claim. |
| `assets/diagrams/compression-and-generation-acceptance.svg` | `chapters/compact-generative-systems-and-residual-honesty.qmd` | `editions/reader_manuscript/v1_0/chapters/compact-generative-systems-and-residual-honesty.qmd` | Draft reader aid; no compression ratio, useful-speed result, model quality, deployed verifier, release approval, or support-state promotion claim. |
| `assets/diagrams/cyclic-substrate-adoption-gate.svg` | `chapters/coilra-multicoil-rope-and-cyclic-mixers.qmd` | `editions/reader_manuscript/v1_0/chapters/coilra-multicoil-rope-and-cyclic-mixers.qmd` | Draft reader aid; no model quality, runtime, memory, training-stability, deployment, release approval, or support-state promotion claim. |
| `assets/diagrams/living-book-release-pipeline.svg` | `chapters/living-book-methodology.qmd` | `editions/reader_manuscript/v1_0/chapters/living-book-methodology.qmd` | Draft reader aid; no EPUB, PDF, DOCX, audio, release-artifact approval, manuscript-quality evidence, or support-state promotion claim. |

## Format-Specific Residuals

The validator checks source-level SVG structure and manuscript placement; the
format-package probe checks EPUB/DOCX/PDF package or text survival; the raster
probe checks generated PNG fallback presence, dimensions, hashes, and nonblank
visual variation; the PDF key-figure layout probe checks the ten figure caption
pages for safe margins and page-raster health; the DOCX key-figure layout probe
checks the ten LibreOffice-converted DOCX figure title pages for safe margins
and page-raster health. None replaces visual review in
rendered HTML, EPUB, DOCX, PDF, e-reader, or audio companion treatment. Before
a reader release can call the figures final, each format still needs inspection
for scale, line weight, text legibility, caption placement, page breaks, color
contrast, and audio-friendly text equivalents.

Open residuals:

- HTML visual/layout: automated browser checks now cover rendered figure
  loading, size, captions, boundaries, and viewport containment for all ten
  draft key figures at desktop and mobile widths. The source-SVG contrast and
  readability gate now passes, and the generated PNG fallback raster probe now
  catches missing, blank, low-ink, or visually collapsed fallback outputs;
  manual aesthetic judgment, line-weight review, rendered-format inspection,
  and final visual approval remain open.
- EPUB: inspect actual e-reader behavior, image sizing, and fallback text.
- DOCX: automated LibreOffice-converted key-figure title-page layout now passes
  for all ten figures; inspect Word/LibreOffice GUI/Google Docs page breaks,
  image anchoring, and caption flow.
- PDF: automated key-figure caption-page layout now passes for all ten figures;
  manual page-by-page PDF review and PDF viewer review remain open.
- Audio: integrate and review the companion summaries inside the future
  narration script.
- Audio: review the drafting spoken summaries in
  `editions/reader_manuscript/v1_0/companion_notes/key-figures.md` inside the
  future narration script; no audio artifact or narration approval exists yet.
- Release: create or update an edition release record only after format review
  is complete.
