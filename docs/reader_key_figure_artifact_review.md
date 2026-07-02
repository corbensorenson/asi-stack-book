# Reader Key-Figure Artifact Review

Last checked: 2026-07-02

Command:

```bash
python3 scripts/validate_reader_key_figures.py
```

Rendered HTML probe:

```bash
python3 scripts/validate_reader_key_figure_html_probe.py --write-result
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

- HTML visual/layout: inspect scale, line weight, text legibility, caption
  placement, and color contrast in the rendered reader HTML beyond the DOM
  probe.
- EPUB: inspect actual e-reader behavior, image sizing, and fallback text.
- DOCX: inspect Word/LibreOffice page breaks, image anchoring, and caption flow.
- PDF: inspect page-level layout, figure scaling, and caption placement.
- Audio: write companion narration or spoken summaries for each figure.
- Release: create or update an edition release record only after format review
  is complete.
