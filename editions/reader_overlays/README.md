# Reader Overlays

Reader overlays are semantic deltas for major human-reader editions and live Human view.

The live Quarto source remains canonical. Generated reader workspaces under `build/reader_edition/` remain disposable. When a major reader version needs prose that is specific to the relaxed human edition, add an overlay operation here instead of hand-editing generated files.

Use overlays only when the change should affect the generated reader edition without changing the live AI/research source. If the change should also affect the live site, source maps, proof hooks, or future writing runs, edit the canonical chapter source instead.

The editable delta source is the tracked overlay manifest plus operation files under this directory. `reader_delta_report.md` is generated from that source during `scripts/build_reader_edition.py`; review the report, but do not edit it to change reader prose. The report records operation metadata, content digests, and before/after excerpts so a reviewer can inspect the semantic delta without treating it as a patch file. If the report shows the wrong delta, edit the overlay operation or the canonical chapter and regenerate.

Supported operation types are section-anchored:

- `replace_section`
- `prepend_to_section`
- `append_to_section`
- `insert_before_section`
- `insert_after_section`

Each operation targets a stable repository-relative `.qmd` file and a heading by level and title. Do not target generated line numbers.

Active operations are embedded into `assets/reader-overlays.html` by `scripts/sync_reader_overlay_asset.py`. The generated reader edition applies the operations to derived Quarto source, while the live Human view applies the same operations in the browser only when Human view is active.

Validate overlays with:

```bash
python3 scripts/sync_reader_overlay_asset.py --check
python3 scripts/validate_reader_overlays.py --check
python3 scripts/build_reader_edition.py --check
```

Generating the reader edition writes `build/reader_edition/reader_delta_report.md`, which records generator transformations, applied overlay operations, content digests, and before/after excerpts. That report is a review aid, not a release record and not proof that any EPUB, PDF, DOCX, or audio artifact exists.
