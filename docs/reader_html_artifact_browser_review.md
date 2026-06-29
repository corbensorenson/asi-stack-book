# Reader HTML Artifact Browser Review

Last updated: 2026-06-29

This note records a full local browser review of the generated reader HTML
snapshot for the current v1.0 candidate. It is not an edition release record
and does not publish or approve any artifact.

## Inputs

Commands run:

```bash
python3 scripts/render_reader_formats.py --formats html epub docx
python3 scripts/inspect_reader_format_artifacts.py
node scripts/validate_reader_html_artifact_browser.js --strict
```

Local ignored reports:

- `build/reader_edition/reader_render_report.json`
- `build/reader_edition/reader_artifact_inspection_report.json`
- `build/reader_html_artifact_browser_report.json`

Reviewed HTML artifact root:

`build/reader_edition/format_artifacts/html/_reader_site`

Deterministic directory digest:

`f2b98bdb82c1c42cfe7d8bc85e63ce5ed06b45d29c8023d4948cd039599a4dfa`

The digest is computed over 81 files by hashing each relative path and file
content in sorted order. The artifact is ignored local build output, not a
committed release asset.

## Structural Inspection

The structural inspection passed for the fresh reader-format snapshot:

| Format | Status | Key metrics |
|---|---|---|
| HTML | passed | 59 HTML files; 54 chapter files; 0 live-marker leaks; 0 raw core-claim marker leaks |
| EPUB | passed | 9,090,771 bytes; 130 zip entries; 62 XHTML entries; 62 image entries; OPF metadata title `The ASI Stack`, creator `Corben Sorenson`, language `en-US` |
| DOCX | passed | 7,077,680 bytes; 77 zip entries; 61 media entries; 19,376 paragraph markers |

The EPUB and DOCX rows are structural context only. This review approves
neither EPUB nor DOCX.

## Browser Sweep

`node scripts/validate_reader_html_artifact_browser.js --strict` opened every
generated reader HTML page at desktop and mobile widths.

| Metric | Result |
|---|---:|
| Pages opened | 59 |
| Viewports | 2 |
| Page-view pairs | 118 |
| Failed page-view pairs | 0 |

For each page-view pair, the browser check required:

- stylesheet loading;
- visible main content and a visible H1;
- at least 1,000 body-text characters;
- no page-level horizontal overflow above 2 pixels;
- no raw bracketed core-claim marker leakage;
- no live-only scaffold headings such as `Chapter status`, `Drafting guardrail`, `Codex test plan`, `Source crosswalk`, `Claim-source mapping status`, or `Formalization hooks`;
- at least one rendered SVG diagram on every chapter page.

## Review Decision

The generated reader HTML artifact clears full local browser artifact review
for this snapshot. The HTML format row may therefore move from
`representative_spot_check` to `pass` and may drop the
`full_format_artifact_review_not_completed` blocker.

The HTML artifact is still not release-approved because no tagged edition
release record names this exact artifact. The remaining HTML blocker is
`reader_release_record_not_created`.

## Residuals

- The reviewed artifact is a local ignored build snapshot, not a published
  release asset.
- No `source_tag` or final v1.0 edition release record exists for this
  artifact.
- This review does not approve EPUB, DOCX, PDF, e-reader conversion, audio, or
  audio-embedded EPUB artifacts.
- This review does not replace human editorial judgment about prose quality.
- This review does not promote any claim support state, source interpretation,
  proof status, benchmark result, runtime behavior, or safety claim.
