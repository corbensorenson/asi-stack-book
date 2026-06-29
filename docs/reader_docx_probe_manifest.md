# Reader DOCX Probe Manifest

Last updated: 2026-06-28

This summary is synced from
`editions/reader_manuscript/v1_0/docx_probe_manifest.json`. It records the
latest tracked local LibreOffice conversion and representative visual spot
check for the generated reader DOCX snapshot. It is not a reader release, not a
DOCX release, not artifact approval, and not a support-state promotion.

## Commands

```bash
python3 scripts/render_reader_formats.py --formats html epub docx
python3 scripts/inspect_reader_format_artifacts.py
python3 <documents-skill>/render_docx.py build/reader_edition/format_artifacts/docx/_reader_site/The-ASI-Stack.docx --output_dir build/reader_docx_probe --emit_pdf
pdfinfo build/reader_docx_probe/The-ASI-Stack.pdf
```

## DOCX Source Summary

| Field | Value |
|---|---:|
| Local artifact | `build/reader_edition/format_artifacts/docx/_reader_site/The-ASI-Stack.docx` |
| File size | 7,059,486 bytes |
| Zip entries | 77 |
| Media entries | 61 |
| Paragraph markers | 19,229 |

## DOCX Conversion Probe Summary

| Field | Value |
|---|---:|
| Status | converted |
| Renderer | documents skill `render_docx.py` via headless LibreOffice |
| Local converted PDF | `build/reader_docx_probe/The-ASI-Stack.pdf` |
| Pages | 514 |
| File size | 8,190,162 bytes |
| Page size | 612 x 792 pts (letter) |
| Encrypted | no |
| Tagged | yes |
| Producer | LibreOfficeDev 26.8.0.0.alpha0 (AARCH64) |
| PDF version | 1.7 |

Local text extraction found the book title, `Reader Edition Draft`, compact
`evidence boundary: architectural argument` text, `Reader Source List`, and
`External Citation Policy`. This confirms only that the generated DOCX can be
converted locally through the available LibreOffice path and sampled as page
images on this machine.

## Refreshed Spot Check

| Page | Surface | Observation |
|---:|---|---|
| 1 | Front matter and reader note | Title, Reader Edition Draft marker, cover image, figure caption, and reader-edition note are readable and not clipped. |
| 25 | Body prose and list sample | Body prose and nested bullet fields are readable with no visible clipping or overlap in the sampled page. |
| 447 | Corben/local source appendix cards | Reader Source List heading, source-card introduction, and first Corben/local source card are readable and not clipped. |
| 472 | Corben/local long source ID card | The long `proof_carrying_circular_computation` source ID wraps as a source-card bullet without visible table-cell overlap. |
| 474 | External source appendix cards | External source-card heading, source-card introduction, first external source card, citation text, and wrapped chapter assignments are readable. |
| 514 | External citation policy | Final external citation-policy page is readable and not clipped. |

## Release Blockers Preserved

- `reader_release_record_not_created`
- `full_format_artifact_review_not_completed`

This is a representative LibreOffice conversion and page-image spot check, not
a full DOCX application review in Word, LibreOffice GUI, or Google Docs.

## Non-Claims

- This manifest records a local DOCX conversion and representative visual spot check in ignored build space only.
- This manifest is not a reader release, DOCX release, document release, edition release record, or artifact approval.
- This manifest does not approve DOCX, EPUB, PDF, HTML, e-reader, document, audio, or audio-embedded EPUB artifacts for publication.
- This manifest does not check full editorial quality, full layout quality, full application behavior, Google Docs import behavior, e-reader behavior, source interpretation, proof adequacy, benchmark behavior, runtime behavior, PDF output approval, or audio output.
- This manifest does not promote any claim support state.
