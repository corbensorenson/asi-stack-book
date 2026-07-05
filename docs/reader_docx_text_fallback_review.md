# Reader DOCX Textutil Fallback Review

Last updated: 2026-07-05

This note records a local text-oriented DOCX fallback probe for the curated reader manuscript. It is not an edition release record, not a rich DOCX approval, not Word/LibreOffice GUI/Google Docs review, and not support-state evidence.

## Summary

| Metric | Value |
|---|---:|
| Source DOCX SHA-256 | `ff045865d1d10a002f24835867f96262844d2d8916fe7882c565d95f7b4275bf` |
| Fallback DOCX SHA-256 | `1566f3686ac8369b4d337b6757178c3e292aca85fd77563676f43d648117036a` |
| Fallback bytes | 339628 |
| ZIP entries | 8 |
| Text characters checked | 1106715 |
| Paragraph markers | 11590 |
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
