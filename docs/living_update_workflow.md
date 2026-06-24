# Living Update Workflow

The book order is manifest-driven.

## Source of Truth

- `book_structure.json` controls front matter, parts, chapter order, chapter IDs, chapter file paths, and appendix order.
- `_quarto.yml` is generated. Do not edit it by hand.
- Chapter filenames use stable slugs, not numbers.
- Quarto generates displayed chapter numbers during render.

## Add a Part

```bash
python3 scripts/add_part.py --title "Part IV - New Research Track"
python3 scripts/sync_scaffold.py
python3 scripts/validate_book.py
```

## Add a Chapter

```bash
python3 scripts/add_chapter.py \
  --part stack-layers \
  --title "New AI Topic" \
  --after planning-and-control

python3 scripts/sync_scaffold.py
python3 scripts/validate_book.py
```

## Reorder, Merge, or Remove Chapters

Edit `book_structure.json` only.

- Reorder: move the chapter object inside the desired part.
- Move to another part: move the chapter object between part arrays.
- Merge: move useful source IDs and claims into the surviving chapter, then remove the obsolete chapter object.
- Remove: remove the chapter object, then decide whether to keep or delete the old `.qmd` file as archival material.

After edits:

```bash
python3 scripts/sync_scaffold.py
python3 scripts/validate_book.py
quarto render --to html
```

## Bring in a New AI Paper

1. Add the paper metadata to `sources/source_inventory.json`.
2. Add the raw or exported source to a private/local source location only if publication is allowed.
3. Create `sources/source_notes/<source-id>.md` after actually reading the source.
4. Decide whether the paper updates an existing chapter or requires a new chapter.
5. Update `book_structure.json`:
   - add the source ID to an existing chapter's `source_ids`, or
   - add a new chapter with `scripts/add_chapter.py`.
6. Update Appendix C only through `scripts/sync_scaffold.py` unless a claim's support state changes after source ingestion or testing.
7. Update `appendices/F_changelog.qmd`.

Do not mark claims as source-derived or test-backed until the source has actually been ingested or the test has actually run.
