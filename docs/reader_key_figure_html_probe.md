# Reader Key-Figure HTML Probe

Last checked: 2026-07-02

Command:

```bash
python3 scripts/validate_reader_key_figure_html_probe.py --write-result
```

This probe builds the tracked curated reader manuscript into a temporary
Quarto workspace, renders HTML, and inspects the rendered HTML DOM for the
ten draft key figures. It checks image references, copied SVG assets, alt
text, captions, responsive image classes, and visible non-claim boundary
paragraphs. It is not a release approval and not final figure-artifact review.

## Result

- Status: `passed`
- Figures checked: 10
- Result artifact: `experiments/reader_key_figure_html_probe/results/2026-07-02-local.json`

## Rendered Figure Checks

| Figure | Rendered chapter HTML | Alt words | Caption | Boundary excerpt |
|---|---|---:|---|---|
| `assets/diagrams/asi-stack-control-plane.svg` | `_reader_site/chapters/asi-is-a-stack-not-a-model.html` | 23 | Draft ASI Stack control plane. | Figure boundary: this draft reader aid shows the book’s intended control-plane shape. It is not release-reviewed art, not a deployment diagram, and not evidence that an integrated runtime exists. |
| `assets/diagrams/authority-to-effect-path.svg` | `_reader_site/chapters/system-boundaries-and-authority.html` | 23 | Draft authority-to-effect path. | Figure boundary: this draft reader aid shows how permission is supposed to constrain external effects. It is not release-reviewed art and does not prove deployed authorization, revocation, rollback, or incident handling. |
| `assets/diagrams/evidence-state-ladder.svg` | `_reader_site/chapters/evidence-states-and-claim-discipline.html` | 27 | Draft evidence-state ladder. | Figure boundary: this draft reader aid visualizes support-state movement and claim-label separation. It is not release-reviewed art and does not promote any claim beyond the support recorded in the live book. |
| `assets/diagrams/intent-to-artifact-trace.svg` | `_reader_site/chapters/intent-to-execution-contracts.html` | 29 | Draft intent-to-artifact trace. | Figure boundary: this draft reader aid shows the intended continuity path from request to artifact. It is not release-reviewed art and does not prove parser quality, dispatcher enforcement, adapter safety, replay behavior, or artifact satisfaction. |
| `assets/diagrams/context-transaction-lifecycle.svg` | `_reader_site/chapters/context-transactions-snapshots-mounts-and-taint.html` | 35 | Draft context transaction lifecycle. | Figure boundary: this draft reader aid shows the intended memory lifecycle. It is not release-reviewed art and does not prove retrieval quality, runtime store behavior, deletion closure, taint enforcement, or context adequacy. |
| `assets/diagrams/readiness-residual-quarantine-map.svg` | `_reader_site/chapters/readiness-gates-residual-escrow-and-quarantine.html` | 35 | Draft readiness residual quarantine map. | Figure boundary: this draft reader aid shows readiness, residual, and quarantine routes. It is not release-reviewed art and does not prove lifecycle execution, live quarantine behavior, rollback behavior, or support-state promotion. |
| `assets/diagrams/route-selection-budget-tradeoff.svg` | `_reader_site/chapters/resource-economics-and-token-budgets.html` | 32 | Draft route-selection budget tradeoff. | Figure boundary: this draft reader aid shows one bounded costed-route selection pattern. It is not release-reviewed art and does not prove deployed routing, production scheduler behavior, model quality, or core-claim promotion. |
| `assets/diagrams/compression-and-generation-acceptance.svg` | `_reader_site/chapters/compact-generative-systems-and-residual-honesty.html` | 32 | Draft compression and generation acceptance. | Figure boundary: this draft reader aid compares compact generation, fast generation, and artifact compression as acceptance-gated paths. It is not release-reviewed art and does not prove compression ratios, task quality, reconstruction utility, or model performance. |
| `assets/diagrams/cyclic-substrate-adoption-gate.svg` | `_reader_site/chapters/coilra-multicoil-rope-and-cyclic-mixers.html` | 33 | Draft cyclic substrate adoption gate. | Figure boundary: this draft reader aid shows how cyclic substrates would earn adoption. It is not release-reviewed art and does not prove model quality, context-length improvement, hardware performance, transfer, or deployment. |
| `assets/diagrams/living-book-release-pipeline.svg` | `_reader_site/chapters/living-book-methodology.html` | 27 | Draft living book release pipeline. | Figure boundary: this draft reader aid shows the living-book release pipeline. It is not release-reviewed art and does not prove reader release approval, ebook/PDF/DOCX/audio quality, source adequacy, or support-state promotion. |

## Non-Claims

- This probe does not approve the figures as final art.
- This probe does not approve HTML, EPUB, DOCX, PDF, e-reader, audio, or release artifacts.
- This probe does not promote any chapter core claim or support state.
- EPUB, DOCX, PDF, e-reader, visual-design, contrast, page-break, and audio companion review remain open.
