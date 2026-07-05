# Reader Keyboard-Only Evidence Decision

Last checked: 2026-07-05

Command:

```bash
python3 scripts/validate_reader_keyboard_only_decision.py
```

Tracked result: `editions/reader_manuscript/v1_0/keyboard_only_decision_manifest.json`

This decision accepts the current automated keyboard-only browser evidence as sufficient to clear the current curated-reader HTML keyboard-only release-preparation blocker. It is not screen-reader review, WCAG conformance review, reader release approval, or artifact publication.

## Decision

| Metric | Value |
|---|---:|
| Status | `accepted_keyboard_only_evidence_for_release_preparation` |
| HTML digest | `2ca82608207741a56a861da7d32f4d8c7e7a25dc390df3836dca11560b19ce34` |
| Keyboard page-view pairs | 98 |
| Keyboard failed pairs | 0 |
| Skip-link activations | 98 |
| Main-content routes | 98 |
| Navigation/search reached | 98 / 98 |
| Keyboard-trap candidates | 0 |
| Accessibility-tree page-view pairs | 98 |
| Unnamed interactive elements | 0 |
| Duplicate-ID hits | 0 |
| Cleared blockers | manual_keyboard_only_review_not_completed |
| Preserved blockers | 9 |

## Basis

The current curated reader HTML candidate has a passing automated Chromium keyboard traversal review over 98 desktop/mobile page-view pairs, a passing accessibility-tree release-preparation probe over the same page-view pairs, zero keyboard-trap candidates, zero unnamed interactive elements, and a passing strict local HTML browser viability sweep. This is enough to clear only the keyboard-only review blocker for release preparation.

## Release Boundary

This decision clears only `manual_keyboard_only_review_not_completed` for the current curated reader HTML candidate. It does not perform screen-reader review, does not certify WCAG conformance, does not approve reader release, does not approve EPUB, DOCX, PDF, e-reader, audio, or audiobook artifacts, and does not promote any chapter core claim or support state.

## Non-Claims

- This decision does not perform screen-reader review.
- This decision does not certify WCAG conformance.
- This decision does not create reader release approval.
- This decision does not publish or approve curated reader HTML.
- This decision does not approve EPUB, DOCX, PDF, e-reader, audio, or audiobook artifacts.
- This decision does not promote any chapter core claim or support state.
