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

## Structural Inspection

Command:

```bash
python3 scripts/inspect_reader_format_artifacts.py
```

Result:

```text
Reader artifact inspection report wrote: /Users/corbensorenson/Documents/AI_book/build/reader_edition/reader_artifact_inspection_report.json
Reader artifact inspection passed: 61 HTML files, 62 EPUB XHTML entries, 59 DOCX media entries.
```

The ignored local inspection report at
`build/reader_edition/reader_artifact_inspection_report.json` records:

| Format | Structural checks passed |
|---|---|
| HTML | 61 total HTML files, 59 rendered reader-site HTML files, 54 chapter files, required index/preface/source-appendix/opening-chapter files present, no live-only heading leaks detected in reader-site HTML, and no raw core-claim marker leaks detected in reader-site HTML. |
| EPUB | Readable EPUB zip container, required `mimetype`, container, OPF, nav, and NCX entries present, `mimetype` first with `application/epub+zip`, 128 entries, 62 XHTML entries, and 60 image entries. |
| DOCX | Readable DOCX zip container, required content types, relationships, document, styles, and document relationship entries present, 75 entries, 59 embedded media entries, 18,440 paragraph markers, book title present, and compact evidence-boundary text present. |

## PDF Probe

The first isolated PDF probe without explicit locale settings failed:

```bash
python3 scripts/render_reader_formats.py --output build/reader_edition_pdf_probe --formats pdf
```

The failure occurred inside the LuaLaTeX path. The local report at
`build/reader_edition_pdf_probe/reader_render_report.json` recorded
`returncode: 1`, no PDF artifacts, and this blocker in the log excerpt:

```text
Unable to read locale data: please check the 'locale' settings of your environment for consistency. Exiting now.
compilation failed- missing packages (automatic installation failed)
```

The UTF-8 locale retry succeeded in a separate ignored workspace:

```bash
LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 python3 scripts/render_reader_formats.py --output build/reader_edition_pdf_probe_utf8 --formats pdf
```

Result:

```text
pdf: rendered
Reader render report wrote: build/reader_edition_pdf_probe_utf8/reader_render_report.json
Rendered formats recorded: 1
```

The successful PDF probe produced
`build/reader_edition_pdf_probe_utf8/format_artifacts/pdf/_reader_site/The-ASI-Stack.pdf`.
Local `pdfinfo` reported:

| Field | Value |
|---|---:|
| File size | 8.0 MB |
| Pages | 574 |
| Page size | letter |
| Encrypted | no |
| Producer | LuaTeX-1.24.0 |

Local text extraction found the book title, `Reader Edition Draft`, and compact
`evidence boundary: architectural argument` text. This confirms only that a PDF
can be produced on this machine when the locale environment is set explicitly.

## Review State

The dry run establishes only that the current generated reader source can be
rendered locally to HTML, EPUB, and DOCX on this machine and that the resulting
local snapshots pass basic structural inspection. The isolated PDF probe also
establishes that PDF can render locally when `LANG` and `LC_ALL` are set to
`en_US.UTF-8`. It does not establish that the reader manuscript has been
reviewed as a book, that diagrams and tables are optimal for e-readers or PDF,
that navigation and bibliography behavior have been manually accepted, or that
any artifact is suitable for publication.

Audio generation was not attempted.

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
