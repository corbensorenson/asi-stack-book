# Curated Reader Manuscript

This directory is the future home for a manually edited human-reader manuscript when generated reader source plus semantic overlays are no longer enough.

The current v1.0 state is intentionally dormant. `v1_0/manifest.json` records that the curated reader manuscript has **not** graduated yet. Until it graduates, the live Quarto book, generated reader edition, and reader overlays remain the active reader path.

When the curated manuscript does graduate, it remains a parallel derivative source for narrative prose only. It may improve pacing, chapter flow, examples, transitions, and relaxed reading, but it is not an equal source for claims, support states, source boundaries, proof/test status, implementation horizons, or release records.

Validate the manifest with:

```bash
python3 scripts/validate_reader_manuscript_manifest.py
```

Generated reader files under `build/reader_edition/` are still disposable. Do not copy or hand-edit them here as a release shortcut. A curated chapter belongs here only after a review decision says overlays are too small for the intended human-reader edit and the chapter has a reconciliation record back to the live manifest chapter.
