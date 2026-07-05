# Reader DOCX Textutil Fallback Review

Last updated: 2026-07-05

This note records a local text-oriented DOCX fallback probe for the curated reader manuscript. It is not an edition release record, not a rich DOCX approval, not Word/LibreOffice GUI/Google Docs review, and not support-state evidence.

## Summary

| Metric | Value |
|---|---:|
| Source DOCX SHA-256 | `12a33e1eb31b5e0147bc18c586b9b73b8d0b4f7bb3936aaf75dc471db78d4a14` |
| Fallback DOCX SHA-256 | `240d5f6150b59da2c167c595855f241ab8604aca3bf9e359d1946c736b26fdb2` |
| Fallback bytes | 339985 |
| ZIP entries | 8 |
| Text characters checked | 1107976 |
| Paragraph markers | 11594 |
| Media entries | 0 |
| Live-marker hits | 0 |
| Raw core-claim marker hits | 0 |

## Pages Observation

Status: `passed_pages_open_text_fallback_probe`

- Pages opened the textutil fallback document without the rich-DOCX read error.
- Pages exposed the title page text, reader edition draft marker, and table-of-contents text.
- Pages exposed chapter 1 body text in the accessibility tree.
- The fallback is a text-oriented import and does not preserve the rich DOCX visual package.

## Release Boundary

The textutil fallback is useful for Pages-readable text access, but it is not the rich DOCX artifact, not a Word/LibreOffice GUI/Google Docs approval, not visual-package approval, and not reader release approval.

Preserved blockers:

- `docx_application_review_not_completed_for_rich_docx`
- `reader_release_approval_not_created`
- `visual_package_not_preserved_by_text_fallback`

Non-claims:

- does not approve the curated reader DOCX for release
- does not clear the rich DOCX application-review blocker
- does not preserve the full figure and visual package
- does not publish any reader artifact
- does not promote any chapter core claim
