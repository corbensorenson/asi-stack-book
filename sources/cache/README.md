# Source Cache Status

This directory stores tracked cache metadata, not private source text.

- `cache_manifest.json` records which inventory records were attempted, cached, blocked, or failed.
- `status/` can hold small machine-readable status files.

Raw exports live under `sources/raw/` and are ignored by git.
