# Private Raw Source Cache

This directory is for local-only exports of source papers from Google Docs or Drive.

Raw source text is ignored by git. Do not force-add raw exports unless publication rights are explicit and intentional.

The public paper library is the governed exception. After Corben's explicit
2026-08-09 publication instruction, `papers/paper_library.json` selects exact
author manuscripts from this private cache. `scripts/sync_paper_library.py`
copies only those selected bytes into tracked `papers/source/` records and
builds reader-facing QMD projections. The private cache itself remains ignored.

Use:

```bash
python3 scripts/cache_drive_sources.py
```

Tracked outputs should be limited to source metadata, cache status, source
notes, derived claim/evidence records, and exact author manuscripts explicitly
admitted by the paper-library manifest.

`sources/corben_raw_source_receipts.json` is the public-safe custody layer for the
audited Corben corpus. It records only source IDs, local-relative paths, byte
counts, and SHA-256 digests. Local validation checks those receipts against the
private bytes; CI checks the tracked receipts and closure topology without
requiring the ignored cache. For manifest-admitted papers, CI verifies the
tracked publication copy against the same receipt. A matching digest
establishes byte identity, not truth, novelty, authorship adjudication, rights,
or evidentiary support.
