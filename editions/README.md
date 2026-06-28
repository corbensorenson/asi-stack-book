# Edition Profiles

This directory defines how major versions of the living book become audience-specific release artifacts.

`release_profiles.json` is the machine-readable source for the edition model:

- `live_book`: the canonical GitHub Pages / Quarto living book for AIs and human researchers.
- `research_release`: a frozen major-version research snapshot with evidence machinery intact.
- `reader_release`: a cleaned human manuscript path for EPUB, PDF, DOCX, and HTML.
- `audio_release`: a narration-ready path derived from the reviewed reader release.

The same file also defines the content-layer contract: reader-facing chapter spine, live research scaffold, evidence matrices, machine-readable contracts, release derivatives, audio adaptation, and companion material. It also records the live Human view policy used by the GitHub Pages toggle. Future writing runs should keep meaning-critical prose in the reader spine and put repeatable source/proof/test machinery in live-only sections that the release profiles can remove or summarize.

Generated edition builds belong under `build/` and are ignored by git. Do not hand-edit generated reader or audio manuscripts as the canonical source; fix the live book, update the profile, or add a semantic reader overlay under `reader_overlays/` when the delta belongs only to a major human-reader edition. The tracked overlay manifest and chapter operation files are the editable reader-delta source; `reader_delta_report.md` is generated review output with a zero-active-operation note or operation digests and before/after excerpts, and should not be patched by hand.

`editions/reader_manuscript/` is the dormant future path for a curated human-reader manuscript. Its v1.0 manifest currently records `not_graduated`: generated reader source plus overlays remain the active path. The chapter review matrix at `editions/reader_manuscript/v1_0/chapter_review_matrix.json` tracks the 54-chapter human-reader review queue, overlay dispositions, companion-note candidates, curated-manuscript candidates, and release blockers while staying synced to `book_structure.json`. If the normal reader edition eventually needs sustained prose editing chapter by chapter, the curated manuscript can become a tracked parallel derivative source for narrative only, with reconciliation back to the live manifest, support states, source boundaries, proof/test status, implementation horizons, and release records.

Validate the profile definitions with:

```bash
python3 scripts/validate_release_profiles.py
python3 scripts/validate_reading_mode_toggle.py
python3 scripts/validate_reader_manuscript_manifest.py
python3 scripts/sync_reader_chapter_review_matrix.py --check
```

Create or check a derived reader-edition draft with:

```bash
python3 scripts/build_reader_edition.py --check
python3 scripts/sync_reader_overlay_asset.py --check
python3 scripts/validate_reader_overlays.py --check
python3 scripts/sync_reader_chapter_review_matrix.py --check
python3 scripts/build_reader_edition.py
```

Attempt and record reader-format renders with:

```bash
python3 scripts/render_reader_formats.py --check
python3 scripts/render_reader_formats.py --formats html epub docx
```

Create or check a derived audio-script review workspace with:

```bash
python3 scripts/build_audio_script.py --check
python3 scripts/build_audio_script.py
```

The generated reader edition and audio script are publication candidate scaffolds. They do not prove that EPUB, PDF, DOCX, AZW3, MOBI, MP3, M4B, or audio-embedded EPUB artifacts have been rendered, converted, or generated until those commands actually run and a release record says so.

`scripts/sync_reader_overlay_asset.py` embeds active overlay operations in `assets/reader-overlays.html`, which is included before the live reading-mode toggle so the GitHub Pages Human view can consume the same section-delta source as generated reader editions. Generated reader workspaces include `reader_manifest.json`, `READER_RELEASE_CHECKLIST.md`, `companion_notes.md`, and `reader_delta_report.md`; reader render attempts write `reader_render_report.json`; generated audio workspaces include `audio_manifest.json`, `AUDIO_RELEASE_CHECKLIST.md`, `companion_notes.md`, `chapter_markers.md`, and `pronunciation_glossary.md`. These manifests, checklists, delta reports, and companion notes document derivation, local render outcomes, and review status for the release process. The delta report records generated transformations and reviewer-facing excerpts, not durable patch instructions. They are not publication artifacts by themselves and are not canonical inputs for prose changes.
