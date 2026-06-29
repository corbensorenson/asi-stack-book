# Reader Artifact Inspection Manifest

Last updated: 2026-06-29

This summary is synced from
`editions/reader_manuscript/v1_0/artifact_inspection_manifest.json`. It records
the latest tracked local structural-inspection evidence for ignored
human-reader format snapshots. It is not a reader release, not artifact
approval, and not a support-state promotion.

## Commands

```bash
python3 scripts/render_reader_formats.py --formats html epub docx
python3 scripts/inspect_reader_format_artifacts.py
```

## Render Summary

| Format | Status | Artifacts observed | Preserved artifacts |
|---|---|---:|---:|
| html | rendered | 59 | 81 |
| epub | rendered | 1 | 1 |
| docx | rendered | 1 | 1 |

## Inspection Summary

| Format | Status | Key metrics |
|---|---|---|
| html | passed | 59 HTML files; 54 chapter files; 0 live-marker leaks; 0 raw core-claim marker leaks |
| epub | passed | 9,090,771 bytes; 130 entries; 62 XHTML entries; 62 image entries; OPF metadata title `The ASI Stack`, creator `Corben Sorenson`, language `en-US` |
| docx | passed | 7,077,680 bytes; 77 entries; 61 media entries; 19,376 paragraph markers |

## Release Blockers Preserved

- `full_format_artifact_review_not_completed`
- `app_or_ereader_review_not_completed` for EPUB; EPUB has a separate
  metadata/source-spine probe and DOCX has a separate representative
  LibreOffice conversion probe
- `release_records/2026-06-29-v1-reader-html-855dc277.json` approves only the
  separately reviewed local HTML snapshot, not EPUB or DOCX

## Non-Claims

- This manifest records a local structural inspection of ignored reader-format snapshots only.
- This manifest is not a reader release, ebook release, document release, PDF release, edition release record, or artifact approval.
- This manifest does not approve EPUB, DOCX, HTML, PDF, e-reader, or audio artifacts for publication.
- This manifest does not check full editorial quality, full layout quality, e-reader behavior, app behavior, source interpretation, proof adequacy, benchmark behavior, runtime behavior, PDF output, or audio output.
- This manifest does not promote any claim support state.
