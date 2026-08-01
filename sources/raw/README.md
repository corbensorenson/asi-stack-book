# Private Raw Source Cache

This directory is for local-only exports of source papers from Google Docs or Drive.

Raw source text is ignored by git. Do not force-add raw exports unless publication rights are explicit and intentional.

Use:

```bash
python3 scripts/cache_drive_sources.py
```

Tracked outputs should be limited to source metadata, cache status, source notes, and derived claim/evidence records.

`sources/corben_raw_source_receipts.json` is the public-safe custody layer for the
audited Corben corpus. It records only source IDs, local-relative paths, byte
counts, and SHA-256 digests. Local validation checks those receipts against the
private bytes; CI checks the tracked receipts and closure topology without
requiring or publishing the ignored paper bodies. A matching digest establishes
byte identity, not truth, novelty, rights, or evidentiary support.
