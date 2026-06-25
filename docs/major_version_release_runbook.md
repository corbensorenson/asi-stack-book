# Major Version Release Runbook

Last updated: 2026-06-25

This runbook is for turning a tagged live-book state into human-consumable major-version artifacts without forking the manuscript.

The live book remains canonical for AIs and human researchers. Reader and audio editions are derived products for interested humans, and each artifact exists only after the relevant generation, render, review, and release-record step succeeds.

## Audience Contract

| Audience | Surface | Retained content | Removed or adapted content |
|---|---|---|---|
| AIs and writing agents | Live Quarto book and repo contracts | Stable ids, source queues, proof tags, schemas, tests, guardrails, release records, and validation commands. | Nothing is stripped; the live book is the source of truth. |
| Human researchers | Live book plus frozen research release | Full technical argument, evidence matrices, source crosswalks, claim states, residuals, and proof/test status. | Nothing is hidden, but release records freeze what was current at the tag. |
| Interested human readers | Reader release and audio release | Coherent chapter prose, diagrams/images, glossary, bibliography, important uncertainty, examples, and summaries. | Repeated status tables, guardrails, source matrices, Codex test plans, proof hooks, and low-level workflow scaffolding. |

Meaning-changing caveats must appear in the reader-facing spine. Do not put the only statement that a claim is speculative, untested, or source-limited inside a section that `reader_release.strip_headings` removes.

## Release Ladder

1. Tag the live book state.
2. Run the live-book validation gate at that tag.
3. Optionally produce a research release that preserves the full live evidence machinery.
4. Generate a reader source tree from the tag.
5. Review the generated reader manuscript for continuity and e-reader quality.
6. Review generated reader companion notes for dense material that should be retained, summarized, or moved out of the relaxed manuscript.
7. Render EPUB, DOCX, HTML, and PDF only as local dependencies allow.
8. Record only formats that actually rendered.
9. Generate an audio-script workspace only after the reader manuscript is reviewed.
10. Replace generated narration notes with reviewed spoken prose or companion-note references.
11. Review audio companion notes before packaging MP3, M4B, or audio-embedded EPUB artifacts.
12. Produce MP3, M4B, or audio-embedded EPUB only after the reviewed script is recorded, packaged, spot-checked, and recorded.

## Human Consumption Bundle

The human-consumption bundle for a major version is assembled from checked layers:

| Class | Formats | Release-record requirement |
|---|---|---|
| Reader formats | HTML, EPUB, PDF, DOCX | `artifact_formats` names only successful renders, and `human_consumption_gate` records continuity, layout, diagram/image, relaxed-reading, and companion-note review. |
| Optional e-reader conversions | AZW3, MOBI, Markdown, plain text | Record only after conversion from the reviewed reader source or reviewed EPUB and a spot check. |
| Audio artifacts | MP3, M4B | `audiobook_gate` records reviewed script, spoken treatment, chapter markers, and spot checks. |
| Audio embedded in EPUB | audio-embedded EPUB | Record only after the EPUB package is opened and verified to contain playable reviewed audio. |

The reader manuscript is the human source. The audio script is downstream of the reviewed reader manuscript. The live book remains canonical after the bundle is produced.

## Live Gate

```bash
python3 scripts/source_readiness_report.py
python3 scripts/sync_scaffold.py
python3 scripts/sync_proof_manifest.py --check
python3 scripts/validate_publication.py
python3 scripts/validate_release_profiles.py
python3 scripts/validate_book.py
python3 scripts/validate_visual_coverage.py
python3 scripts/validate_schemas.py
python3 scripts/validate_protocol_examples.py
python3 scripts/validate_repeated_prose.py
(cd lean && lake build)
LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 quarto render --to html
```

## Reader Gate

Check that the stripped manuscript will still work as a book:

```bash
python3 scripts/build_reader_edition.py --check
python3 scripts/validate_reader_spine.py --check
python3 scripts/render_reader_formats.py --check
```

Generate the local source workspace:

```bash
python3 scripts/build_reader_edition.py
```

Then review `build/reader_edition/READER_RELEASE_CHECKLIST.md`, `build/reader_edition/companion_notes.md`, and the generated manuscript before rendering release artifacts.

Attempt specific formats and record actual local outcomes:

```bash
python3 scripts/render_reader_formats.py --formats html epub docx
python3 scripts/render_reader_formats.py --formats html epub docx pdf
```

PDF is optional until local Quarto PDF dependencies are present. Optional AZW3, MOBI, Markdown, or plain-text files are downstream conversions from the reviewed reader source or reviewed EPUB, not canonical sources.

## Audio Gate

Audio is downstream of a reviewed reader release, not the live book directly.

```bash
python3 scripts/build_audio_script.py --check
python3 scripts/build_audio_script.py
```

Review `build/audio_script/AUDIO_RELEASE_CHECKLIST.md`, `build/audio_script/companion_notes.md`, `build/audio_script/chapter_markers.md`, and `build/audio_script/pronunciation_glossary.md`.

Before claiming any audio artifact:

- Replace generated table, diagram, image, schema, and code narration notes with reviewed spoken summaries or companion-note references.
- Spot-check audio against the reviewed script.
- Verify chapter markers and metadata.
- Verify that an audio-embedded EPUB actually contains the reviewed audio files.
- Add an `edition_release` record under `release_records/`.

## Release Record Rule

A major-version record must name exactly what exists:

- `research_release` records can preserve live evidence machinery.
- `reader_release` records can list EPUB, DOCX, HTML, PDF, AZW3, MOBI, Markdown, or plain-text artifacts only after render or conversion.
- `audio_release` records can list MP3, M4B, or audio-embedded EPUB only after audio generation and checks.
- `human_consumption_gate` and `audiobook_gate` must reflect what review actually happened, not what the profile intends.

Do not infer artifact existence from a profile target, generated source tree, checklist, or render plan.
