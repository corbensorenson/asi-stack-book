# Reader PDF Probe Manifest

Last updated: 2026-06-28

This summary is synced from
`editions/reader_manuscript/v1_0/pdf_probe_manifest.json`. It records the
latest tracked local UTF-8 PDF render probe for the generated reader edition.
It is not a reader release, not a PDF release, not artifact approval, and not a
support-state promotion.

## Command

```bash
LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 python3 scripts/render_reader_formats.py --output build/reader_edition_pdf_probe_utf8 --formats pdf
```

## PDF Probe Summary

| Field | Value |
|---|---:|
| Status | rendered |
| Local artifact | `build/reader_edition_pdf_probe_utf8/format_artifacts/pdf/_reader_site/The-ASI-Stack.pdf` |
| Pages | 614 |
| File size | 8,672,117 bytes |
| Page size | 612 x 792 pts (letter) |
| Encrypted | no |
| Producer | LuaTeX-1.24.0 |
| PDF version | 1.7 |

Local text extraction found the book title, `Reader Edition Draft`, and compact
`evidence boundary: architectural argument` text. This confirms only that a PDF
can be produced on this machine when the locale environment is set explicitly.

## Refreshed Spot Check

| Page | Surface | Observation |
|---:|---|---|
| 1 | Title page | Title, subtitle, and author text are readable and not clipped. |
| 21 | Reader edition note | Cover image, caption, note heading, and note prose are readable and not clipped. |
| 25 | Opening chapter start | Opening chapter title, lead-in prose, and Problem section are readable and not clipped. |
| 527 | Corben/local source appendix table | The page is not blank or clipped, but long source IDs and neighboring table cells collide horizontally in the PDF table. |
| 614 | External citation policy | Final external citation-policy page is readable and not clipped. |

## Release Blockers Preserved

- `reader_release_record_not_created`
- `full_format_artifact_review_not_completed`
- `full_pdf_layout_review_not_completed`
- `pdf_source_appendix_table_collision_unresolved`

## Non-Claims

- This manifest records a local UTF-8 PDF render probe in ignored build space only.
- This manifest is not a reader release, PDF release, ebook release, edition release record, or artifact approval.
- This manifest does not approve PDF, EPUB, DOCX, HTML, e-reader, document, audio, or audio-embedded EPUB artifacts for publication.
- This manifest does not check full editorial quality, full layout quality, e-reader behavior, app behavior, source interpretation, proof adequacy, benchmark behavior, runtime behavior, or audio output.
- This manifest does not promote any claim support state.
