# Reader Accessibility Tree Review

Last checked: 2026-07-05

Command:

```bash
node scripts/validate_curated_reader_accessibility_tree.js --write-manifest
```

Tracked result: `editions/reader_manuscript/v1_0/accessibility_tree_manifest.json`

This automated browser review opens the ignored local curated-reader HTML artifact at desktop and mobile widths. It checks rendered page language, one-H1 shape, main and navigation landmarks, skip-link presence, interactive accessible names, image alt text, table headers, duplicate IDs, live-marker leakage, raw core-claim leakage, and Chromium accessibility-tree availability. It is release-preparation evidence only.

## Summary

| Metric | Value |
|---|---:|
| Status | `passed_accessibility_tree_release_preparation_probe` |
| Pages checked | 49 |
| Page-view pairs | 98 |
| Failed page-view pairs | 0 |
| lang="en-US" page-view pairs | 98 |
| Titled page-view pairs | 98 |
| One-H1 page-view pairs | 98 |
| Main landmark page-view pairs | 98 |
| Navigation landmark page-view pairs | 98 |
| Skip-link page-view pairs | 98 |
| Focus-visible rule page-view pairs | 98 |
| Accessibility-tree page-view pairs | 98 |
| Minimum accessibility-tree nodes | 130 |
| Minimum named accessibility-tree nodes | 86 |
| Visible interactive elements checked | 1834 |
| Unnamed interactive elements | 0 |
| Visible images checked | 9 |
| Image alt failures | 0 |
| Tables checked | 10 |
| Table header failures | 0 |
| Duplicate-ID page-view hits | 0 |
| Live-marker leak pairs | 0 |
| Raw core-claim marker leak pairs | 0 |

## Gate

Every rendered page-view pair must have `lang="en-US"`, a document title, exactly one H1, visible main and navigation landmarks, a skip-to-main link, loaded focus-visible styling, no visible unnamed interactive controls, substantive alt text for visible images, table header cells for visible tables, no duplicate IDs, no live-only marker leakage, no raw core-claim marker leakage, and an available Chromium accessibility tree with named nodes.

## Non-Claims

- This review does not approve the curated reader HTML artifact for release.
- This review does not certify WCAG conformance.
- This review does not perform screen-reader review.
- This review does not perform manual keyboard-only review.
- This review does not approve EPUB, DOCX, PDF, e-reader, audio, final figure art, or reader release artifacts.
- This review does not promote any chapter core claim or support state.
