# Curated Reader Manuscript

This directory is the future home for a manually edited human-reader manuscript when generated reader source plus semantic overlays are no longer enough.

The current v1.0 state is intentionally dormant. `v1_0/manifest.json` records that the curated reader manuscript has **not** graduated yet. Until it graduates, the live Quarto book, generated reader edition, and reader overlays remain the active reader path.

The v1.0 companion-note routing manifest at `v1_0/companion_note_routing.json` records chapter-level reader, e-reader, and audio companion decisions for dense proof/governance chapters. It is review routing only, not a reader release record or artifact approval.

When the curated manuscript does graduate, it remains a parallel derivative source for narrative prose only. It may improve pacing, chapter flow, examples, transitions, and relaxed reading, but it is not an equal source for claims, support states, source boundaries, proof/test status, implementation horizons, or release records.

Validate the manifest with:

```bash
python3 scripts/validate_reader_manuscript_manifest.py
python3 scripts/sync_reader_chapter_review_matrix.py --check
```

Generated reader files under `build/reader_edition/` are still disposable. Do not copy or hand-edit them here as a release shortcut. The durable reader-review queue is `v1_0/chapter_review_matrix.json`, with a public summary at `docs/reader_chapter_review_matrix.md`; run `python3 scripts/sync_reader_chapter_review_matrix.py --write` after chapter, overlay, or review-decision changes. A curated chapter belongs here only after a review decision says overlays are too small for the intended human-reader edit and the chapter has a reconciliation record back to the live manifest chapter.

Use the initializer when that decision exists:

```bash
python3 scripts/build_reader_edition.py
python3 scripts/init_curated_reader_chapter.py --chapter-id <manifest-chapter-id>
python3 scripts/init_curated_reader_chapter.py --chapter-id <manifest-chapter-id> --write
python3 scripts/validate_reader_manuscript_manifest.py
```

The dry run prints the manifest record that would be added. The write step starts a drafting record with release blockers still active; it does not approve a reader release or make the curated chapter equal to the live book.
