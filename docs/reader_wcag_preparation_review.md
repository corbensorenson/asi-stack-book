# Reader WCAG Preparation Review

Last checked: 2026-07-05

Command:

```bash
node scripts/validate_curated_reader_wcag_preparation.js --write-manifest
```

Tracked result: `editions/reader_manuscript/v1_0/wcag_preparation_manifest.json`

This automated browser review opens the ignored local curated-reader HTML artifact at desktop and mobile widths. It checks rendered language metadata, document titles, one-H1 page shape, main and navigation landmarks, skip-link presence, focus-visible CSS, accessible names, visible image alt text, visible table header cells, duplicate IDs, live-marker leakage, raw core-claim leakage, and WCAG 2.x-style contrast thresholds for visible text samples.

## Decision

Status: `accepted_wcag_automation_evidence_for_release_preparation`.

Cleared blockers | wcag_conformance_review_not_completed

Preserved blockers include `screen_reader_review_not_completed`, `reader_release_approval_not_created`, and downstream audio artifact gates.

## Summary

| Metric | Value |
|---|---:|
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
| Visible interactive elements checked | 1786 |
| Unnamed interactive elements | 0 |
| Visible images checked | 9 |
| Image alt failures | 0 |
| Tables checked | 10 |
| Table header failures | 0 |
| Duplicate-ID page-view hits | 0 |
| Text contrast samples | 3523 |
| Contrast failure samples | 0 |
| Minimum contrast ratio | 4.69 |
| Live-marker leak pairs | 0 |
| Raw core-claim marker leak pairs | 0 |

## Non-Claims

- This review does not approve the curated reader HTML artifact for release.
- This review does not perform screen-reader or assistive-technology review.
- This review does not provide third-party or legal WCAG certification.
- This review does not approve EPUB, DOCX, PDF, e-reader, audio, final figure art, or reader release artifacts.
- This review does not publish the ignored local curated reader HTML artifact.
- This review does not promote any chapter core claim or support state.
