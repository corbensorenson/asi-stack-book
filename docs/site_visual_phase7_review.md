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

## Source-Growth Site UX Probe

After the Phase 6 external-literature expansion raised Appendix H and the
source-readiness surfaces, a second local browser probe checked the rendered
landing page, two dense diagram chapters, and the widest source/claim appendices
at desktop and mobile sizes.

Command:

```bash
LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 quarto render --to html
python3 scripts/validate_live_human_view.py
node scripts/validate_live_human_view_browser.js --all-chapters --all-viewports
node <local Playwright probe against _site/index.html, fast-generation, recursive-self-improvement, Appendix A, Appendix C, and Appendix H>
```

Probe metrics:

| Page | Viewport | Scroll width | Client width | Page overflow | Tables | Wide tables | Toggle visible | Mermaid visible | Hero visible |
|---|---:|---:|---:|---:|---:|---:|---|---|---|
| `index` | desktop 1366 x 900 | 1366 | 1366 | 0 | 0 | 0 | yes | yes | yes |
| `index` | mobile 390 x 844 | 390 | 390 | 0 | 0 | 0 | yes | yes | yes |
| `fast-generation-architectures` | desktop 1366 x 900 | 1366 | 1366 | 0 | 6 | 0 | yes | yes | no |
| `fast-generation-architectures` | mobile 390 x 844 | 390 | 390 | 0 | 6 | 0 | yes | yes | no |
| `recursive-self-improvement-boundaries` | desktop 1366 x 900 | 1366 | 1366 | 0 | 5 | 0 | yes | yes | no |
| `recursive-self-improvement-boundaries` | mobile 390 x 844 | 390 | 390 | 0 | 5 | 0 | yes | yes | no |
| `A_source_matrix` | desktop 1366 x 900 | 1366 | 1366 | 0 | 1 | 0 | yes | no | no |
| `A_source_matrix` | mobile 390 x 844 | 390 | 390 | 0 | 1 | 0 | yes | no | no |
| `C_claim_evidence_matrix` | desktop 1366 x 900 | 1366 | 1366 | 0 | 3 | 0 | yes | no | no |
| `C_claim_evidence_matrix` | mobile 390 x 844 | 390 | 390 | 0 | 3 | 0 | yes | no | no |
| `H_external_sources` | desktop 1366 x 900 | 1366 | 1366 | 0 | 4 | 0 | yes | no | no |
| `H_external_sources` | mobile 390 x 844 | 390 | 390 | 0 | 4 | 0 | yes | no | no |

The probe found no page-level horizontal overflow on the inspected pages after
the source-table growth. The reading-mode switch was visible on all inspected
pages and both inspected viewports. Mermaid visibility was present on the
landing page and dense chapter pages; appendix pages correctly had no Mermaid or
hero-image expectation. This is a focused UX/readability probe only, not an
accessibility certification, reader-release review, or proof of full design
quality.

## Appendix Inline-Code Overflow Follow-up

After the source inventory reached 160 records, a focused local Playwright probe
rechecked the landing page, the two dense diagram chapters, and Appendices A,
C, F, H, and K at desktop and mobile sizes. The first run found a real overflow
issue in Appendix F: long inline `code` spans in the changelog forced 191px of
page-level horizontal overflow on a 1366px desktop viewport and 884px on a
390px mobile viewport.

`assets/styles.scss` now lets inline `code` in prose, list, and table contexts
wrap within the available content width while leaving fenced code blocks alone.
After rerendering, the same focused probe produced these metrics:

| Page | Viewport | Scroll width | Client width | Page overflow | Tables | Wide tables | Toggle visible | Mermaid visible | Hero visible |
|---|---:|---:|---:|---:|---:|---:|---|---|---|
| `index` | desktop 1366 x 900 | 1366 | 1366 | 0 | 0 | 0 | yes | yes | yes |
| `index` | mobile 390 x 844 | 390 | 390 | 0 | 0 | 0 | yes | yes | yes |
| `fast-generation-architectures` | desktop 1366 x 900 | 1366 | 1366 | 0 | 6 | 0 | yes | yes | no |
| `fast-generation-architectures` | mobile 390 x 844 | 390 | 390 | 0 | 6 | 0 | yes | yes | no |
| `recursive-self-improvement-boundaries` | desktop 1366 x 900 | 1366 | 1366 | 0 | 5 | 0 | yes | yes | no |
| `recursive-self-improvement-boundaries` | mobile 390 x 844 | 390 | 390 | 0 | 5 | 0 | yes | yes | no |
| `A_source_matrix` | desktop 1366 x 900 | 1366 | 1366 | 0 | 1 | 0 | yes | no | no |
| `A_source_matrix` | mobile 390 x 844 | 390 | 390 | 0 | 1 | 0 | yes | no | no |
| `C_claim_evidence_matrix` | desktop 1366 x 900 | 1366 | 1366 | 0 | 3 | 0 | yes | no | no |
| `C_claim_evidence_matrix` | mobile 390 x 844 | 390 | 390 | 0 | 3 | 0 | yes | no | no |
| `F_changelog` | desktop 1366 x 900 | 1366 | 1366 | 0 | 0 | 0 | yes | no | no |
| `F_changelog` | mobile 390 x 844 | 390 | 390 | 0 | 0 | 0 | yes | no | no |
| `H_external_sources` | desktop 1366 x 900 | 1366 | 1366 | 0 | 4 | 0 | yes | no | no |
| `H_external_sources` | mobile 390 x 844 | 390 | 390 | 0 | 4 | 0 | yes | no | no |
| `K_implementation_horizons` | desktop 1366 x 900 | 1366 | 1366 | 0 | 4 | 0 | yes | no | no |
| `K_implementation_horizons` | mobile 390 x 844 | 390 | 390 | 0 | 4 | 0 | yes | no | no |

This follow-up hardens rendered-site readability for long inline paths and
commands. It is not an accessibility certification, reader-release review,
ebook layout review, or claim-evidence promotion.

## Dense Diagram Split Follow-up

The fast-generation and recursive self-improvement mechanism diagrams were
split into smaller Mermaid diagrams so neither chapter asks one graph to carry
too many state transitions at once.

- The selector diagram now covers task risk, context, budget, mode family, and
  proposed-span handoff.
- The acceptance/accounting diagram now covers verifier outcome, fallback,
  rejected-work accounting, Talos artifactization, Benchmaxxing records, and SCF
  promotion review.
- The recursive self-improvement review diagram now covers the cheaper
  intervention ladder, boundary-delta review, protected invariant checks,
  evaluator independence, and blocked proposal outcomes.
- The recursive self-improvement canary diagram now covers gate review,
  governance approval, canary monitoring, rollback, promotion, outcome ledger,
  and next review trigger.
- `python3 scripts/validate_visual_coverage.py` passed after the split.
- The chapter corpus now has 55 Mermaid diagrams across 47 manifest chapters.

This is a readability improvement only. It does not change Fast Generation's
or Recursive Self-Improvement's support state, prove speed-quality performance,
prove safe autonomous self-improvement, approve a reader artifact, or claim
model/runtime behavior.

## Diagram Audit

The chapter corpus currently has 55 Mermaid diagrams across 47 manifest
chapters. The largest chapter diagrams by non-comment Mermaid line count were:

| Diagram | Lines | Edges | Initial assessment |
|---|---:|---:|---|
| `chapters/asi-is-a-stack-not-a-model.qmd` diagram 1 | 27 | 12 | Dense but still within readable range for an overview architecture diagram. |
| `chapters/integrated-reference-architecture.qmd` diagram 1 | 20 | 10 | Appropriate for integrated stack closure. |
| `chapters/moral-uncertainty-and-value-conflict.qmd` diagram 1 | 18 | 17 | Edge-dense but still readable as a conflict lifecycle; acceptable after mobile scroll-container review. |
| `chapters/fast-generation-architectures.qmd` diagrams 1 and 2 | 16 and 9 | 15 and 8 | Split into selector and acceptance/accounting diagrams; no longer a single edge-dense mechanism graph. |
| `chapters/recursive-self-improvement-boundaries.qmd` diagrams 1 and 2 | 15 and 14 | 14 and 13 | Split into boundary-review and canary/promotion diagrams; no longer a single edge-dense gate graph. |

No diagram failed the automated visual-coverage gate. The next visual pass
should revisit the split diagrams during e-reader and reader-release review
only if their scrollable presentation still feels too dense.

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

- Optional visual refinement of split diagrams if reader-release or e-reader
  review still finds them too crowded despite contained mobile scrolling; the
  fast-generation and recursive self-improvement mechanisms have already been
  split into smaller diagrams.
- Optional appendix table style review if future source growth introduces
  horizontal overflow; the current source-growth and inline-code probes found
  zero page-level overflow on Appendices A, C, F, H, and K at desktop/mobile
  sizes.
- Keep the `scripts/validate_live_human_view.py` preflight aligned with the
  rendered-site contract so missing, incomplete, or stale `_site` output keeps
  producing render-first guidance.

## Non-Claims

- This review does not prove any chapter claim.
- It does not promote support states.
- It does not certify visual design quality, accessibility compliance, or reader
  release quality.
- It does not produce EPUB, PDF, DOCX, audiobook, or release artifacts.
