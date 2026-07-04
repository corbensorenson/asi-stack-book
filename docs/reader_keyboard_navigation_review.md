# Reader Keyboard Navigation Review

Last checked: 2026-07-04

Command:

```bash
node scripts/validate_curated_reader_keyboard_navigation.js --write-manifest
```

Tracked result: `editions/reader_manuscript/v1_0/keyboard_navigation_manifest.json`

This automated browser review tabs through the ignored local curated-reader HTML artifact at desktop and mobile widths. It checks keyboard traversal, focus reachability, focus visibility, search/navigation reachability, main-content reachability, and trap absence. It is release-preparation evidence only.

## Summary

| Metric | Value |
|---|---:|
| Status | `passed_automated_keyboard_traversal_review` |
| Pages checked | 49 |
| Expected pages | 49 |
| Viewports | 2 |
| Page-view pairs | 98 |
| Chapter page-view pairs | 88 |
| Tab steps per page-view | 80 |
| Failed page-view pairs | 0 |
| Minimum focusable elements | 7 |
| Minimum unique focus targets | 8 |
| Skip-link route reached | 98 |
| Skip-link route activated | 98 |
| Main-content focus reached by Tab | 97 |
| Main-content route available | 98 |
| Navigation/search focus reached | 98 / 98 |
| Body/document wrap observations | Recorded in ignored detailed report |
| Offscreen focus observations | Recorded in ignored detailed report |
| Keyboard trap candidates | 0 |

## Gate

Each page-view pair must expose visible focusable elements, make the skip-to-main link reachable in the early keyboard sequence, activate the skip-to-main route, reach navigation and search through repeated `Tab` traversal, and avoid short repeated focus cycles that indicate a likely keyboard trap. Body/document wrap observations and offscreen focus observations are recorded as residuals because Quarto pages can wrap after the finite target list or move fixed mobile controls slightly outside the viewport after scrolling.

## Non-Claims

- This review does not approve the curated reader HTML artifact for release.
- This review does not certify WCAG conformance.
- This review does not perform screen-reader review.
- This review does not perform manual keyboard-only review.
- This review does not approve EPUB, DOCX, PDF, e-reader, audio, final figure art, or reader release artifacts.
- This review does not promote any chapter core claim or support state.
