# Public Site Accessibility Readiness Review

Date: 2026-06-29

Status: v1.0 Phase 7 readiness record, not an accessibility certification.

This review records the accessibility-facing state of the live Quarto site. It
uses existing rendered-site, Human-view, diagram, and release-readiness
evidence, then names the residuals that must not be hidden by a passing browser
smoke test.

## Scope

The scope is the public GitHub Pages live book and the local `_site/` render
used for validation. It covers the reading-mode switch, AI/Human view
projection, Mermaid diagrams, diagram text equivalents, the landing image,
appendix tables, color and contrast hooks, keyboard/focus hooks, screen-reader
hooks, status language, and downstream e-reader boundaries.

This review does not cover a full manual screen-reader pass, full keyboard-only
walkthrough, WCAG conformance audit, EPUB publication or e-reader release approval, DOCX publication or reader release approval, PDF publication or reader release approval, or accessibility testing of future audio artifacts.

## Evidence Reviewed

- `assets/reading-mode.html` exposes the `AI view` / `Human view` control,
  button `aria-pressed` state, an assistive description, and a `role="status"`
  live region with `aria-live="polite"`.
- `assets/styles.scss` defines `.asi-sr-only`, `:focus-visible` button styling,
  high-contrast active toggle styling, table containment, inline-code wrapping,
  and contained Mermaid scrolling on small screens.
- `index.qmd` references the generated landing image with `fig-alt` text.
- `scripts/validate_visual_coverage.py` requires every chapter to contain a
  substantive Mermaid diagram and a chapter-specific diagram walkthrough note in
  the ratcheted parts.
- `scripts/validate_reading_mode_toggle.py`,
  `scripts/validate_live_human_view.py`, and
  `scripts/validate_live_human_view_browser.js --all-chapters --all-viewports`
  check the reading-mode contract, rendered hooks, real-browser visibility,
  page-level horizontal overflow, Human-view hiding/restoration behavior, and
  rendered Mermaid visibility.
- `docs/site_visual_phase7_review.md` records the mobile diagram containment
  pass, source-growth browser probe, Appendix F inline-code overflow fix, and
  remaining visual non-claims.

## Accessibility Readiness Matrix

| Surface | Current evidence | v1.0 readiness decision | Residual or blocker |
|---|---|---|---|
| Reading-mode switch | `assets/reading-mode.html`; `scripts/validate_reading_mode_toggle.py`; rendered Human-view browser validation | Ready as a convenience projection control for the live site | Still needs a manual keyboard-only pass before claiming polished accessibility. |
| AI/Human view projection | Static and browser validators check mode persistence, shareable `?view=`, live-section hiding, TOC hiding, raw marker hiding, support-boundary restoration, and AI-view restoration | Ready for v1.0 live-site mechanics | Human view remains a convenience projection, not a fully reviewed reader-release manuscript. |
| Mermaid diagrams | 60 diagrams across 54 manifest chapters; `scripts/validate_visual_coverage.py`; all-chapter browser validation checks rendered Mermaid visibility | Ready for v1.0 coverage and rendered visibility | Dense diagrams may still need reader/e-reader simplification or companion notes. |
| Diagram text equivalents | Chapter-specific walkthrough notes are required for ratcheted parts and preserved in source prose | Ready as prose orientation for Human view, reader editions, and future audio treatment | Walkthroughs are not full long descriptions for every diagram state or edge. |
| Landing image | `index.qmd` uses `fig-alt` text for `assets/images/asi-stack-hero.png` | Ready for the current landing-page asset | Future generated images need the same alt-text review before release. |
| Tables and appendices | Browser probes over Appendices A/C/F/H/K found zero page-level overflow after inline-code wrapping | Ready for live/research site use | Wide matrices remain research surfaces and should stay stripped or companion-noted in relaxed reader formats. |
| Color and contrast | Styles use dark body text, high-contrast active toggle color, visible focus styling, and restrained accent colors | Acceptable for current candidate readiness | No measured WCAG contrast report has been run, so no contrast-compliance claim is made. |
| Keyboard and focus | Toggle buttons are native buttons and have `:focus-visible` styling | Candidate-ready hook exists | No full tab-order, skip-link, or keyboard-only walkthrough has been recorded. |
| Screen reader | The reading-mode switch exposes an assistive description and polite status updates | Candidate-ready hook exists | No VoiceOver, NVDA, JAWS, or other screen-reader pass has been recorded. |
| E-reader and reader artifacts | Reader-format probes and the HTML artifact review exist; EPUB/DOCX/PDF blockers remain explicit | Live-site accessibility review does not approve downstream artifacts | EPUB publication/e-reader release approval, DOCX publication/release approval, and PDF publication/release approval remain blockers. |
| Release/status language | Roadmap, candidate status, publication readiness, and release records separate live-site readiness from reader artifact approval | Ready for conservative public status | Final v1.0 tag metadata and DOI/archive facts remain pending until they exist. |

## Residuals

- Run and record a manual keyboard-only walkthrough for the landing page, a
  representative chapter in both AI and Human view, Appendix A, and Appendix C
  before calling the public site accessibility-polished.
- Run and record at least one screen-reader pass before making screen-reader
  quality claims.
- Add a measured contrast audit only if the project wants a contrast-compliance
  claim; until then, keep the status at candidate readiness.
- Revisit dense Mermaid diagrams during EPUB e-reader review and audio-script
  review because contained scrolling in the live site is not the same as good
  e-reader or spoken treatment.
- Recheck appendix table overflow after large source, claim, changelog, or
  implementation-horizon growth.

## Validation Command

```bash
python3 scripts/validate_public_site_accessibility.py
```

This command checks the accessibility-readiness ledger, progress ledger,
reading-mode assistive hooks, CSS focus and containment hooks, landing-image alt
text, and the presence of residual/non-claim boundaries.

## Non-Claims

- This review does not claim WCAG conformance.
- This review does not certify the site as fully accessible.
- This review does not approve EPUB, DOCX, PDF, e-reader, audio, or
  audio-embedded EPUB artifacts.
- This review does not promote any chapter core claim above `argument`.
- This review does not prove runtime behavior, model quality, benchmark
  performance, safety, source interpretation, or reader-release quality.
