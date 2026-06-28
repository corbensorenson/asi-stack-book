# Reader Format Dry Run

Last updated: 2026-06-28

This note records a local Phase 8 reader-format dry run for the generated
human-reader edition. It is not a reader release, ebook release, document
release, PDF release, or edition release record.

## Command

```bash
python3 scripts/render_reader_formats.py --formats html epub docx
```

Result:

```text
html: rendered
epub: rendered
docx: rendered
Reader render report wrote: /Users/corbensorenson/Documents/AI_book/build/reader_edition/reader_render_report.json
Rendered formats recorded: 3
```

## Local Report

The ignored local report at `build/reader_edition/reader_render_report.json`
records:

| Format | Status | Return code | Artifacts observed | Preserved snapshots |
|---|---:|---:|---:|---:|
| HTML | rendered | 0 | 61 | 61 |
| EPUB | rendered | 0 | 1 | 1 |
| DOCX | rendered | 0 | 1 | 1 |

The render script now snapshots each format under
`build/reader_edition/format_artifacts/` before the next Quarto format pass can
replace the output tree:

- HTML snapshot: `build/reader_edition/format_artifacts/html/`
- EPUB snapshot: `build/reader_edition/format_artifacts/epub/_reader_site/The-ASI-Stack.epub`
- DOCX snapshot: `build/reader_edition/format_artifacts/docx/_reader_site/The-ASI-Stack.docx`

The EPUB snapshot was 8.4 MB in the local dry-run workspace. The DOCX snapshot
was 6.5 MB in the local dry-run workspace. These files are ignored build
outputs, not tracked release artifacts.

## Review State

The dry run establishes only that the current generated reader source can be
rendered locally to HTML, EPUB, and DOCX on this machine. It does not establish
that the reader manuscript has been reviewed as a book, that diagrams and tables
are optimal for e-readers, that navigation and bibliography behavior have been
manually accepted, or that any artifact is suitable for publication.

PDF was not attempted in this dry run. Audio generation was not attempted.

## Non-Claims

- No v1.0 tag was created.
- No reader release was approved.
- No edition release record was written.
- No EPUB, DOCX, HTML bundle, PDF, AZW3, MOBI, MP3, M4B, or audio-embedded EPUB
  artifacts are claimed as published.
- The local snapshots are disposable review artifacts in ignored `build/`
  space.
- Passing this dry run does not promote any chapter support state, proof
  adequacy status, source-derived evidence state, benchmark result, runtime
  behavior, or safety claim.

## Next Review Step

Inspect representative rendered reader outputs before any release record:

- Front matter, Part I, and Part II for continuity and pacing.
- Dense Part III chapters for diagram and table behavior in HTML/EPUB/DOCX.
- Part IV proof, evidence, benchmark, release, and methodology chapters for
  caveat preservation.
- Appendix G and Appendix H for source-ownership clarity in e-reader and
  document formats.
