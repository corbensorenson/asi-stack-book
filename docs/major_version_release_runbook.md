# Major Version Release Runbook

Last updated: 2026-06-28

This runbook is for turning a tagged live-book state into human-consumable major-version artifacts without losing the live book's evidence authority.

The live book remains canonical for AIs and human researchers. Reader and audio editions are derived products for interested humans, and each artifact exists only after the relevant generation, render, review, and release-record step succeeds. A normal reader manuscript may eventually become a curated parallel derivative source for human prose, but it is not an equal source for claims, support states, source boundaries, proof/test status, implementation horizons, or release records.

## Audience Contract

| Audience | Surface | Retained content | Removed or adapted content |
|---|---|---|---|
| AIs and writing agents | Live Quarto book and repo contracts | Stable ids, source queues, proof tags, schemas, tests, guardrails, release records, and validation commands. | Nothing is stripped; the live book is the source of truth. |
| Human researchers | Live book plus frozen research release | Full technical argument, evidence matrices, source crosswalks, claim states, residuals, and proof/test status. | Nothing is hidden, but release records freeze what was current at the tag. |
| Interested human readers | Reader release and audio release | Coherent chapter prose, diagrams/images, glossary, bibliography, important uncertainty, examples, and summaries. | Repeated status tables, guardrails, source matrices, Codex test plans, proof hooks, and low-level workflow scaffolding. |

Meaning-changing caveats must appear in the reader-facing spine. Do not put the only statement that a claim is speculative, untested, or source-limited inside a section that `reader_release.strip_headings` removes.

If a curated reader manuscript exists for the release, review it as a parallel derivative source: it may differ in prose order, section flow, examples, and pacing, but every chapter must reconcile to a live manifest chapter and preserve the live book's claim/evidence boundaries.

## Release Ladder

1. Tag the live book state.
2. Run the live-book validation gate at that tag.
3. Optionally produce a research release that preserves the full live evidence machinery.
4. Generate a reader source tree from the tag.
5. Review the generated reader manuscript for continuity and e-reader quality.
6. If a curated reader manuscript exists, reconcile it against the generated reader source, manifest chapter IDs, support states, implementation horizons, diagrams, and evidence boundaries.
7. Review generated reader companion notes for dense material that should be retained, summarized, or moved out of the relaxed manuscript.
8. Render EPUB, DOCX, HTML, and PDF only as local dependencies allow.
9. Record only formats that actually rendered.
10. Generate an audio-script workspace only after the reader manuscript is reviewed.
11. Replace generated narration notes with reviewed spoken prose or companion-note references.
12. Review audio companion notes before packaging MP3, M4B, or audio-embedded EPUB artifacts.
13. Produce MP3, M4B, or audio-embedded EPUB only after the reviewed script is recorded, packaged, spot-checked, and recorded.

## Human Consumption Bundle

The human-consumption bundle for a major version is assembled from checked layers:

| Class | Formats | Release-record requirement |
|---|---|---|
| Reader formats | HTML, EPUB, PDF, DOCX | `artifact_formats` names only successful renders, and `human_consumption_gate` records continuity, layout, diagram/image, relaxed-reading, and companion-note review. |
| Optional e-reader conversions | AZW3, MOBI, Markdown, plain text | Record only after conversion from the reviewed reader source or reviewed EPUB and a spot check. |
| Audio artifacts | MP3, M4B | `audiobook_gate` records reviewed script, spoken treatment, chapter markers, and spot checks. |
| Audio embedded in EPUB | audio-embedded EPUB | Record only after the EPUB package is opened and verified to contain playable reviewed audio. |

The reader manuscript is the human-prose source. The audio script is downstream of the reviewed reader manuscript. The live book remains canonical after the bundle is produced for evidence, sources, claims, proof/test status, and architecture control.

## Live Gate

```bash
python3 scripts/source_readiness_report.py
python3 scripts/sync_scaffold.py
python3 scripts/sync_proof_manifest.py --check
python3 scripts/validate_publication.py
python3 scripts/validate_release_profiles.py
python3 scripts/validate_reading_mode_toggle.py
python3 scripts/validate_human_reading_paths.py
python3 scripts/validate_reader_evidence_boundaries.py --check
python3 scripts/audit_reader_continuity.py --check
python3 scripts/validate_reader_manuscript_manifest.py
python3 scripts/sync_reader_chapter_review_matrix.py --check
python3 scripts/validate_book.py
python3 scripts/validate_visual_coverage.py
python3 scripts/validate_schemas.py
python3 scripts/validate_protocol_examples.py
python3 scripts/validate_repeated_prose.py
(cd lean && lake build)
LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 quarto render --to html
python3 scripts/validate_live_human_view.py
node scripts/validate_live_human_view_browser.js --all-chapters --all-viewports
```

## Reader Gate

Check that the stripped manuscript will still work as a book:

```bash
python3 scripts/build_reader_edition.py --check
python3 scripts/sync_reader_overlay_asset.py --check
python3 scripts/validate_reader_overlays.py --check
python3 scripts/audit_reader_continuity.py --check
python3 scripts/validate_reader_manuscript_manifest.py
python3 scripts/sync_reader_chapter_review_matrix.py --check
python3 scripts/validate_human_reading_paths.py
python3 scripts/validate_reader_evidence_boundaries.py --check
python3 scripts/validate_reader_spine.py --check
python3 scripts/render_reader_formats.py --check
```

Generate the local source workspace:

```bash
python3 scripts/build_reader_edition.py
```

Then review `build/reader_edition/READER_RELEASE_CHECKLIST.md`, `build/reader_edition/companion_notes.md`, `build/reader_edition/reader_delta_report.md`, `docs/reader_continuity_audit.md`, `docs/reader_chapter_review_matrix.md`, the live `assets/reader-overlays.html` payload and runtime-count validation when active overlays exist, and the generated manuscript before rendering release artifacts. The delta report carries a zero-active-operation note or operation digests and before/after excerpts for review, not editable patch instructions. The review matrix names which chapters are not started, spot checked, active-overlay chapters, companion-note candidates, curated-manuscript candidates, and still blocked from release. If review finds a reader-only prose change, edit the tracked overlay operation under `editions/reader_overlays/` and regenerate; do not edit generated reader source or hand-patch the generated delta report.

If the reader release has graduated to a curated reader manuscript, do not treat generated source as the only review target. Use `editions/reader_manuscript/v1_0/manifest.json` as the source-status record, use `editions/reader_manuscript/v1_0/chapter_review_matrix.json` as the chapter review queue, use `editions/reader_manuscript/v1_0/reconciliation_report.md` as the chapter-by-chapter reconciliation surface, use generated reader source as the reconciliation baseline, then review the curated manuscript chapter by chapter against the manifest and evidence boundaries before rendering.

Attempt specific formats and record actual local outcomes:

```bash
python3 scripts/render_reader_formats.py --formats html epub docx
python3 scripts/inspect_reader_format_artifacts.py
LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 python3 scripts/render_reader_formats.py --formats html epub docx pdf
```

Successful format attempts are snapshotted under ignored `build/reader_edition/format_artifacts/` for local review and summarized in `build/reader_edition/reader_render_report.json`; structural artifact inspection writes `build/reader_edition/reader_artifact_inspection_report.json`. PDF is optional until local Quarto PDF dependencies are present and should use the explicit UTF-8 locale environment unless a later probe proves it unnecessary. Optional AZW3, MOBI, Markdown, or plain-text files are downstream conversions from the reviewed reader source or reviewed EPUB, not canonical sources.

## Audio Gate

Audio is downstream of a reviewed reader release, not the live book directly.

```bash
python3 scripts/build_audio_script.py --check
python3 scripts/build_audio_script.py
```

Review `build/audio_script/AUDIO_RELEASE_CHECKLIST.md`, `build/audio_script/companion_notes.md`, `build/audio_script/chapter_markers.md`, and `build/audio_script/pronunciation_glossary.md`.

Before claiming any audio artifact:

- Verify that `audio_manifest.json` reports a passing implementation-horizon script status for `Minimum Viable Implementation` and `Beyond the State of the Art`.
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
