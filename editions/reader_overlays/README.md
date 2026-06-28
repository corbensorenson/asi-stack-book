# Reader Overlays

Reader overlays are semantic deltas for major human-reader editions.

The live Quarto source remains canonical. Generated reader workspaces under `build/reader_edition/` remain disposable. When a major reader version needs prose that is specific to the relaxed human edition, add an overlay operation here instead of hand-editing generated files.

Use overlays only when the change should affect the generated reader edition without changing the live AI/research source. If the change should also affect the live site, source maps, proof hooks, or future writing runs, edit the canonical chapter source instead.

Supported operation types are section-anchored:

- `replace_section`
- `prepend_to_section`
- `append_to_section`
- `insert_before_section`
- `insert_after_section`

Each operation targets a stable repository-relative `.qmd` file and a heading by level and title. Do not target generated line numbers.

Validate overlays with:

```bash
python3 scripts/validate_reader_overlays.py --check
python3 scripts/build_reader_edition.py --check
```

Generating the reader edition writes `build/reader_edition/reader_delta_report.md`, which records generator transformations and applied overlay operations. That report is a review aid, not a release record and not proof that any EPUB, PDF, DOCX, or audio artifact exists.
