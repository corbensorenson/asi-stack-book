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

The sync step creates only a generated starting point for a missing chapter. To regenerate the v0.2 manuscript baseline from the manifest, run:

```bash
python3 scripts/draft_v02_from_manifest.py
```

Use that command intentionally; it rewrites all chapter files from `book_structure.json`.

## Add a Chapter

```bash
python3 scripts/add_chapter.py \
  --part planning-memory-reasoning-execution \
  --title "New AI Topic" \
  --after planning-as-a-control-layer

python3 scripts/sync_scaffold.py
python3 scripts/validate_book.py
```

Then draft the new chapter directly, or intentionally rerun `python3 scripts/draft_v02_from_manifest.py` if you want to refresh the full baseline from the manifest.

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

## Bring in Conversation-Mined Context

1. Move the raw packet under `sources/inbox/` so it remains local-only unless explicitly approved for publication.
2. Read provenance and limitations first.
3. Extract only public-safe author intent, terminology, architecture lineage, deduplication decisions, and recovery tasks.
4. Update `docs/book_outline.md`, `book_structure.json`, appendices, or docs only when the mined context changes the future writing plan.
5. Do not quote private conversation wording verbatim or mark claims as source-derived from conversation context.
6. Record a public-safe ingestion report under `docs/` and update the changelog.

## Prepare a Major-Version Reader Edition

The live book remains the canonical source. Reader, research, and audio editions are derived from a tagged live-book state.

1. Confirm the live-book gate passes:

```bash
python3 scripts/sync_scaffold.py
python3 scripts/sync_proof_manifest.py --check
python3 scripts/validate_release_profiles.py
python3 scripts/render_reader_formats.py --check
python3 scripts/validate_book.py
quarto render --to html
```

2. Check the reader-edition derivation:

```bash
python3 scripts/build_reader_edition.py --check
```

3. Generate the local reader manuscript source:

```bash
python3 scripts/build_reader_edition.py
```

4. Attempt selected local reader renders and write a render report:

```bash
python3 scripts/render_reader_formats.py --formats html epub docx
```

Use `--include-pdf` or add `pdf` to `--formats` only when local PDF dependencies are available.

5. Review the generated manuscript for continuity before publishing EPUB, DOCX, PDF, or HTML from `build/reader_edition/`.
6. Record only the formats that actually render successfully.
7. For audio, create and review a narration script from the reader edition before producing MP3, M4B, or audio-embedded EPUB artifacts.

Do not report an ebook, PDF, DOCX, or audiobook as complete just because the profile lists it as a target.

## Prepare a Major-Version Audio Script

Audio is downstream of the reader edition, not the live book directly.

1. Confirm the reader release candidate was generated and reviewed for human continuity.
2. Generate or check the narration-script workspace:

```bash
python3 scripts/build_audio_script.py --check
python3 scripts/build_audio_script.py
```

3. Review `build/audio_script/` and replace generated narration notes for tables, diagrams, images, code, and schemas with spoken summaries or companion-note references.
4. Keep the pronunciation glossary current.
5. Produce MP3, M4B, or audio-embedded EPUB only after the exact script is reviewed.
6. Add an `edition_release` record under `release_records/` that lists exactly which audio artifacts were produced and checked.

The generated audio script is not an audiobook and does not imply that any audio artifact exists.
