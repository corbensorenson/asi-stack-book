# Chapter Reader Overlay Operations

Add one JSON operation file per chapter only when a major human-reader version needs prose that should survive regeneration but should not change the canonical AI/research source. It is valid for this directory to contain no active operation files when the reader edition does not yet need reader-only deltas.

The manifest at `editions/reader_overlays/v1_0/manifest.json` loads `chapters/*.json`. Each file should use this shape:

```json
{
  "schema_version": "0.1",
  "target_file": "chapters/example-chapter.qmd",
  "operations": [
    {
      "id": "v1_0.example_chapter.reader_summary_replace",
      "status": "active",
      "action": "replace_section",
      "section": {
        "level": 2,
        "title": "Summary",
        "aliases": []
      },
      "rationale": "Make the major-version reader summary less workflow-heavy without changing the live AI/research source.",
      "content_lines": [
        "Replacement reader-edition prose goes here."
      ]
    }
  ]
}
```

Supported actions are `replace_section`, `prepend_to_section`, `append_to_section`, `insert_before_section`, and `insert_after_section`. Target stable repository-relative `.qmd` files and heading titles, not generated line numbers. Use `section.aliases` when the generated reader heading differs from the live source heading because of reader-language transformations.

After adding or changing an operation, run:

```bash
python3 scripts/build_reader_edition.py --check
python3 scripts/sync_reader_overlay_asset.py
python3 scripts/sync_reader_overlay_asset.py --check
python3 scripts/validate_reader_overlays.py --check
```

Review `build/reader_edition/reader_delta_report.md` after a non-check reader build. The report includes generated transformations and either a zero-active-operation note or operation metadata, content digests, and before/after excerpts. It is review evidence, not an editable patch file.
