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
python3 scripts/validate_source_evidence_audit.py
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

python3 scripts/chapter_adjacency_report.py --chapter new-ai-topic
python3 scripts/sync_scaffold.py
python3 scripts/validate_chapter_handoffs.py
python3 scripts/validate_book.py
```

Then draft the new chapter directly, or intentionally rerun `python3 scripts/draft_v02_from_manifest.py` if you want to refresh the full baseline from the manifest. `scripts/add_chapter.py` prints the adjacent Handoff repair notes for the new slot; the adjacency report can be rerun later if the chapter is moved.

## Reorder, Merge, or Remove Chapters

Edit `book_structure.json` only.

- Reorder: move the chapter object inside the desired part.
- Move to another part: move the chapter object between part arrays.
- Merge: move useful source IDs and claims into the surviving chapter, run `python3 scripts/chapter_adjacency_report.py --if-removing <chapter-id>` to identify the predecessor Handoff repair, then remove the obsolete chapter object.
- Remove: remove the chapter object, then decide whether to keep or delete the old `.qmd` file as archival material.

After edits:

```bash
python3 scripts/chapter_adjacency_report.py --chapter <changed-chapter-id>
python3 scripts/sync_scaffold.py
python3 scripts/validate_source_evidence_audit.py
python3 scripts/validate_chapter_handoffs.py
python3 scripts/validate_book.py
quarto render --to html
```

## Bring in a New AI Paper

1. Decide the source storage and public-safety policy before adding text:
   - `repo_public_note_only` for public-safe notes without raw source publication.
   - `repo_public_source_allowed` only when publication is explicitly allowed.
   - `connector_only`, `local_private_cache`, `external_url_only`, or `blocked` when raw text should not enter the public repo.
2. Add or update the paper metadata in `sources/source_inventory.json` with a stable source ID.
3. Create or update a `research_backlog_record` when the source changes chapter boundaries, evidence state, proof/test backlog, or publication risk.
4. Use the `new_paper_triage_scenario` decision surface before prose changes:
   - update an existing chapter when the source strengthens an existing boundary,
   - propose a new chapter only when it owns a distinct interface, invariant, artifact type, or failure mode,
   - route to appendix/backlog when it is useful but not chapter-owning,
   - defer unread external literature,
   - reject duplicate or superseded variants.
5. Create `sources/source_notes/<source-id>.md` only after actually reading the source or a permitted connector/export.
6. Update `book_structure.json` only after the chapter decision is clear:
   - add the source ID to an existing chapter's `source_ids`, or
   - add a new chapter with `scripts/add_chapter.py`.
7. Record required pre-drafting work, chapter-decision refs, deduplication state, evidence-transition preconditions, promotion blockers, and non-claims before strengthening chapter prose.
8. Update Appendix C only through `scripts/sync_scaffold.py` unless a claim's support state changes after source ingestion, proof, or testing.
9. Run the relevant checks:

```bash
python3 scripts/sync_scaffold.py
python3 scripts/validate_schemas.py
python3 scripts/validate_protocol_examples.py
python3 scripts/validate_source_evidence_audit.py
python3 scripts/validate_source_appendices.py
python3 scripts/validate_v1_status_snapshot.py
python3 scripts/validate_outline_consistency.py
python3 scripts/validate_implementation_horizons.py
python3 scripts/validate_book.py
quarto render --to html
```

10. Update `appendices/F_changelog.qmd`.

Do not mark claims as source-derived or test-backed until the source has actually been ingested, mapped to the claim, passage-reviewed or accepted through an evidence transition, and any claimed test has actually run.

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
python3 scripts/validate_source_evidence_audit.py
python3 scripts/validate_release_profiles.py
python3 scripts/validate_reading_mode_toggle.py
python3 scripts/validate_human_reading_paths.py
python3 scripts/validate_source_appendices.py
python3 scripts/validate_v1_status_snapshot.py
python3 scripts/validate_outline_consistency.py
python3 scripts/validate_implementation_horizons.py
python3 scripts/validate_reader_evidence_boundaries.py --check
python3 scripts/validate_reader_spine.py --check
python3 scripts/render_reader_formats.py --check
python3 scripts/validate_book.py
quarto render --to html
python3 scripts/validate_live_human_view.py
node scripts/validate_live_human_view_browser.js --all-chapters --all-viewports
```

2. Check the reader-edition derivation:

```bash
python3 scripts/build_reader_edition.py --check
python3 scripts/validate_reader_evidence_boundaries.py --check
python3 scripts/validate_reader_spine.py --check
```

3. Generate the local reader manuscript source:

```bash
python3 scripts/build_reader_edition.py
```

Review `build/reader_edition/READER_RELEASE_CHECKLIST.md` and `build/reader_edition/companion_notes.md` alongside the generated manuscript.

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

3. Confirm the generated `audio_manifest.json` reports a passing implementation-horizon script status, meaning every manifest chapter script keeps both `Minimum Viable Implementation` and `Beyond the State of the Art`.
4. Review `build/audio_script/AUDIO_RELEASE_CHECKLIST.md`, `build/audio_script/companion_notes.md`, and `build/audio_script/chapter_markers.md`, then replace generated narration notes for tables, diagrams, images, code, and schemas with spoken summaries or companion-note references.
5. Keep the pronunciation glossary current.
6. Produce MP3, M4B, or audio-embedded EPUB only after the exact script is reviewed.
7. Add an `edition_release` record under `release_records/` that lists exactly which audio artifacts were produced and checked.

The generated audio script is not an audiobook and does not imply that any audio artifact exists.
