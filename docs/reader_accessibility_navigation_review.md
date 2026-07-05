# Reader Accessibility And Navigation Review

Last checked: 2026-07-04

Command:

```bash
python3 scripts/validate_reader_accessibility_navigation.py
```

Tracked result: `editions/reader_manuscript/v1_0/accessibility_navigation_manifest.json`

This CI-friendly source-level review checks the tracked curated reader manuscript for chapter navigation shape, handoff consistency, release-blocker preservation, draft key-figure text alternatives, and source-leak boundaries. It is not rendered browser review, not keyboard-only review, not screen-reader review, not WCAG conformance, not e-reader review, not audiobook review, and not reader release approval.

## Summary

| Metric | Value |
|---|---:|
| Status | `passed_source_accessibility_navigation_review` |
| Chapter records | 44 |
| Existing chapter files | 44 |
| Reconciled records | 44 |
| Release blockers preserved | 44 |
| Chapters with one H1 | 44 |
| Total headings | 598 |
| Maximum heading level | 3 |
| Skipped heading levels | 0 |
| Duplicate heading slugs | 0 |
| Handoff sections | 44 |
| H2 sections per chapter | 10 min / 19 max |
| Character count per chapter | 16650 min / 37352 max |
| Draft reader images | 10 |
| Figure alt texts | 10 |
| Figure boundary paragraphs | 10 |
| Live-marker leaks | 0 |
| Raw core-claim marker leaks | 0 |
| Key-figure targets | 10 |
| Key-figure assets present | 10 |
| Key-figure reader refs present | 10 |
| Key-figure fig-alt refs present | 10 |
| Key-figure boundary refs present | 10 |

## Gate

Every curated reader chapter must exist, remain reconciled, preserve release blockers, keep exactly one H1, keep one `## Handoff` section, avoid heading-level skips and duplicate heading slugs, avoid live-book scaffold markers, and avoid raw claim-marker leakage. The ten draft reader figures must resolve to tracked SVG assets and carry `fig-alt` text plus nearby `Figure boundary:` paragraphs in the reader manuscript.

## Non-Claims

- This review does not certify WCAG conformance.
- This review does not perform screen-reader or keyboard-only review.
- This review does not approve EPUB, DOCX, PDF, e-reader, audio, or reader release artifacts.
- This review does not approve final figure art.
- This review does not promote any chapter core claim or support state.
