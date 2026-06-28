# Reader Artifact Inspection Manifest

Last updated: 2026-06-28

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
| epub | passed | 9,060,193 bytes; 130 entries; 62 XHTML entries; 62 image entries |
| docx | passed | 7,049,660 bytes; 77 entries; 61 media entries; 19,262 paragraph markers |

## Release Blockers Preserved

- `reader_release_record_not_created`
- `full_format_artifact_review_not_completed`
- `app_or_ereader_review_not_completed` for EPUB and DOCX

## Non-Claims

- This manifest records a local structural inspection of ignored reader-format snapshots only.
- This manifest is not a reader release, ebook release, document release, PDF release, edition release record, or artifact approval.
- This manifest does not approve EPUB, DOCX, HTML, PDF, e-reader, or audio artifacts for publication.
- This manifest does not check full editorial quality, full layout quality, e-reader behavior, app behavior, source interpretation, proof adequacy, benchmark behavior, runtime behavior, PDF output, or audio output.
- This manifest does not promote any claim support state.
