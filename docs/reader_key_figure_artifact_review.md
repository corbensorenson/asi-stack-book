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

The validator checks source-level SVG structure and manuscript placement. It
does not replace visual review in rendered HTML, EPUB, DOCX, PDF, e-reader, or
audio companion treatment. Before a reader release can call the figures final,
each format still needs inspection for scale, line weight, text legibility,
caption placement, page breaks, color contrast, and audio-friendly text
equivalents.

Open residuals:

- HTML visual/layout: automated browser checks now cover rendered figure
  loading, size, captions, boundaries, and viewport containment for all ten
  draft key figures at desktop and mobile widths. The source-SVG contrast and
  readability gate now passes; manual aesthetic judgment, line-weight review,
  rendered-format inspection, and final visual approval remain open.
- EPUB: inspect actual e-reader behavior, image sizing, and fallback text.
- DOCX: inspect Word/LibreOffice page breaks, image anchoring, and caption flow.
- PDF: inspect page-level layout, figure scaling, and caption placement.
- Audio: write companion narration or spoken summaries for each figure.
- Audio: review the drafting spoken summaries in
  `editions/reader_manuscript/v1_0/companion_notes/key-figures.md` inside the
  future narration script; no audio artifact or narration approval exists yet.
- Release: create or update an edition release record only after format review
  is complete.
