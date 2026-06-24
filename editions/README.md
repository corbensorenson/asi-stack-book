# Edition Profiles

This directory defines how major versions of the living book become audience-specific release artifacts.

`release_profiles.json` is the machine-readable source for the edition model:

- `live_book`: the canonical GitHub Pages / Quarto living book for AIs and human researchers.
- `research_release`: a frozen major-version research snapshot with evidence machinery intact.
- `reader_release`: a cleaned human manuscript path for EPUB, PDF, DOCX, and HTML.
- `audio_release`: a narration-ready path derived from the reviewed reader release.

Generated edition builds belong under `build/` and are ignored by git. Do not hand-edit generated reader or audio manuscripts as the canonical source; fix the live book, update the profile, or add a reviewed release script instead.

Validate the profile definitions with:

```bash
python3 scripts/validate_release_profiles.py
```

Create or check a derived reader-edition draft with:

```bash
python3 scripts/build_reader_edition.py --check
python3 scripts/build_reader_edition.py
```

Create or check a derived audio-script review workspace with:

```bash
python3 scripts/build_audio_script.py --check
python3 scripts/build_audio_script.py
```

The generated reader edition and audio script are publication candidate scaffolds. They do not prove that EPUB, PDF, DOCX, MP3, M4B, or audio-embedded EPUB artifacts have been rendered or generated until those commands actually run and a release record says so.
