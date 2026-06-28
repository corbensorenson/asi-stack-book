# Phase 7 Site And Visual Review

Last updated: 2026-06-28

This review records the first Phase 7 pass over the rendered live site, diagram
coverage, Human-view behavior, appendix table surfaces, landing-page trust
signals, and local repository hygiene. It is a site/readability audit, not a
claim-evidence promotion.

## Commands Run

```bash
python3 scripts/validate_visual_coverage.py
python3 scripts/validate_live_human_view.py
node scripts/validate_live_human_view_browser.js --all-chapters --all-viewports
LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 quarto render --to html
node scripts/validate_live_human_view_browser.js --all-chapters --all-viewports
```

Results:

- Visual coverage passed: 54 chapter diagrams checked.
- Rendered Human-view static validation passed: 67 rendered book pages, 54
  rendered chapter pages, 323 live-only headings available for runtime hiding,
  323 live-only TOC targets available for runtime hiding, and 54 human-only
  source blocks rendered.
- Browser validation passed: 112 rendered page/view pairs exercised across all
  manifest chapters and the configured desktop/mobile viewport set.
- After the mobile Mermaid readability change, the full browser validation
  passed again for 112 rendered page/view pairs.

## Diagram Audit

The chapter corpus currently has 58 Mermaid diagrams across 54 manifest
chapters. The largest chapter diagrams by non-comment Mermaid line count were:

| Diagram | Lines | Edges | Initial assessment |
|---|---:|---:|---|
| `chapters/asi-is-a-stack-not-a-model.qmd` diagram 1 | 27 | 12 | Dense but still within readable range for an overview architecture diagram. |
| `chapters/fast-generation-architectures.qmd` diagram 1 | 23 | 22 | Edge-dense; desktop readable; mobile readability improved by contained Mermaid scrolling. Keep on the watch list for future split if reader release review still finds it overloaded. |
| `chapters/integrated-reference-architecture.qmd` diagram 1 | 20 | 10 | Appropriate for integrated stack closure. |
| `chapters/recursive-self-improvement-boundaries.qmd` diagram 1 | 18 | 17 | Edge-dense but aligned with boundary/gate semantics; mobile readability improved by contained Mermaid scrolling. |
| `chapters/moral-uncertainty-and-value-conflict.qmd` diagram 1 | 18 | 17 | Edge-dense but still readable as a conflict lifecycle; acceptable after mobile scroll-container review. |

No diagram failed the automated visual-coverage gate. The next visual pass
should revisit the fast-generation and recursive-improvement diagrams during
reader-release review and split either diagram only if the scrollable mobile
presentation still feels too dense.

## Mobile Diagram Screenshot Review

The first mobile screenshot pass found that the fast-generation and recursive
self-improvement diagrams technically fit without page overflow, but their
labels became too small to be useful on a phone. `assets/styles.scss` now lets
Mermaid SVGs keep a readable minimum width inside their own horizontally
scrollable `.cell-output-display` container on small screens while preserving
zero page-level overflow.

Local screenshot metrics after the change:

| Page | Viewport | Page overflow | Container width | Diagram scroll width |
|---|---:|---:|---:|---:|
| `fast-generation-architectures` | 390px mobile | 0px | 339px | 782px |
| `recursive-self-improvement-boundaries` | 390px mobile | 0px | 339px | 782px |
| `moral-uncertainty-and-value-conflict` | 390px mobile | 0px | 339px | 782px |
| `integrated-reference-architecture` | 390px mobile | 0px | 339px | 782px |

The screenshot files remain local under `build/phase7_screenshots/` as review
scratch output, not tracked release artifacts.

## Appendix Table Audit

Rendered appendix tables have the following largest observed row widths:

| Appendix HTML | Tables | Max row columns | Initial assessment |
|---|---:|---:|---|
| `A_source_matrix.html` | 1 | 9 | Wide; should remain a research/AI surface and needs browser overflow checks after source growth. |
| `C_claim_evidence_matrix.html` | 3 | 10 | Widest table; acceptable for live/research view, not reader-release prose. |
| `G_corben_source_corpus.html` | 3 | 7 | Wide but bounded. |
| `H_external_sources.html` | 4 | 7 | Wide but bounded after Phase 6 source expansion. |
| `K_implementation_horizons.html` | 4 | 5 | Moderate. |

The all-chapter/all-viewport browser check passed horizontal-overflow checks,
so no immediate table CSS change is required. The wide source and claim matrices
should remain stripped or companion-noted in human reader editions.

## Landing Page And Trust Signals

- `index.qmd` references `assets/images/asi-stack-hero.png` with descriptive
  alt text.
- The landing page still labels the book as a v0.2 manuscript draft with a v1.0
  improvement pass active; this is conservative and consistent with the current
  evidence boundary.
- README and v1.0 status docs link the public site, repository, current
  candidate status, roadmap, source appendices, reader-mode policy, and release
  gates.
- The site continues to present Human view as a convenience projection, not as a
  reviewed reader-release manuscript.

## Local Hygiene

`git count-objects -vH` reported no garbage and no prune-packable objects. A
manual `git gc` was not run in this pass because the repository did not report
garbage and the Phase 7 goal is site readiness, not repository compaction.

## Remaining Phase 7 Work

- Optional visual refinement or splitting of the fast-generation and
  recursive-improvement diagrams if reader-release review still finds them too
  crowded despite contained mobile scrolling.
- Optional appendix table style review if future source growth introduces
  horizontal overflow.
- Optional clearer stale-site guidance in `scripts/validate_live_human_view.py`
  if contributors run it before rendering.

## Non-Claims

- This review does not prove any chapter claim.
- It does not promote support states.
- It does not certify visual design quality, accessibility compliance, or reader
  release quality.
- It does not produce EPUB, PDF, DOCX, audiobook, or release artifacts.
