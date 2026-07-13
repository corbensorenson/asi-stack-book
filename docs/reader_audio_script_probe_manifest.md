# Reader Audio-Script Probe Manifest

Last updated: 2026-07-10

This summary is synced from
`editions/reader_manuscript/v1_0/audio_script_probe_manifest.json`. It records
the current active generated reader edition audio-script review workspace. The
frozen v1.0 curated-reader audio review remains historical evidence and is not
regenerated from a later active spine. Neither record is an audiobook,
narration approval, audio release, or support-state promotion.

## Commands

```bash
python3 scripts/build_audio_script.py --check
python3 scripts/build_audio_script.py --source-mode generated_reader_edition
python3 - <<'PY' ... import scripts/build_audio_script.py and inspect audio_manifest.json in a temporary workspace ...
python3 scripts/validate_reader_audio_script_reading_flow.py --write-manifest
```

## Script Workspace Summary

| Field | Value |
|---|---:|
| Source profile | `reader_release` |
| Source mode | `generated_reader_edition` |
| Source generator | `scripts/build_reader_edition.py` |
| Audio profile | `audio_release` |
| Script files | 59 |
| Implementation-horizon script status | pass |
| Review status | review_required |

Required review files are generated in the ignored workspace:
`audio_manifest.json`, `AUDIO_RELEASE_CHECKLIST.md`, `companion_notes.md`,
`chapter_markers.md`, `pronunciation_glossary.md`, and
`proof_equation_reading_rules.md`.

## Audio Script Reading-Flow Review

The generated script workspace now has an automated reading-flow review. It
checks that `index.md`, `preface.md`, the 54 active chapter scripts, and the included
appendix scripts follow `book_structure.json` order instead of alphabetical
filesystem order. It also checks that `chapter_markers.md` follows the same
script order.

| Metric | Value |
|---|---:|
| Script files checked | 59 |
| Front-matter scripts checked | 2 |
| Chapter scripts checked | 54 |
| Appendix scripts checked | 3 |
| Script order | matches book-structure order |
| Ordered chapter markers | 59 ordered markers |
| Chapter-marker timecodes | 59 `TBD` rows |
| Narration notes | 102 narration notes |
| Table narration notes | 23 |
| Diagram narration notes | 68 |
| Image narration notes | 11 |
| Code/schema narration notes | 0 |
| Implementation-horizon chapter scripts | 54 |
| Script statistics | Current digest and text statistics are recorded in the tracked audio-script probe manifest. |
| Replacement characters | 0 |
| Live/research marker hits | 0 |
| Raw core-claim marker hits | 0 |

First scripts in order: `index.md`, `preface.md`,
`chapters/asi-is-a-stack-not-a-model.md`,
`chapters/the-efficient-asi-hypothesis.md`, and
`chapters/system-boundaries-and-authority.md`.

Last scripts in order: `chapters/living-book-methodology.md`,
`chapters/open-research-agenda-and-bibliography-plan.md`,
`appendices/B_glossary.md`, `appendices/G_corben_source_corpus.md`, and
`appendices/H_external_sources.md`.

This is not narration quality review, not pronunciation review, not chapter
timecoding, not an audiobook, not audio generation, and not release approval.

## Companion Treatment Totals

| Material | Count |
|---|---:|
| Tables | 23 |
| Mermaid diagrams | 68 |
| Code/schema blocks | 0 |
| Images | 11 |

These counts are script-preparation cues. They tell a future narration review
where tables, diagrams, images, or dense material need spoken summaries or
companion-note routing before any audio artifact can be claimed.

The ten reader-manuscript key figures now have tracked draft spoken summaries
and e-reader fallback guidance in
`editions/reader_manuscript/v1_0/companion_notes/key-figures.md`. The generated
audio companion workspace points future reviewers to that note through the
release-profile companion-material policy. This is still not narration
approval, final figure-artifact approval, or evidence that audio files exist.
The bridge routes ten draft key figures into the generated audio companion
workspace for review.

| Key-figure companion note | Value |
|---|---:|
| Source note | `editions/reader_manuscript/v1_0/companion_notes/key-figures.md` |
| Source status | `drafting companion note, not release reviewed.` |
| Draft figure summaries routed | 10 |
| Audio treatment section present | true |
| E-reader treatment section present | true |
| Non-claim boundaries | 6 |

## Target Artifact Status

| Artifact | Status |
|---|---|
| MP3 | `target_not_generated` |
| M4B | `target_not_generated` |
| Audio-embedded EPUB | `target_not_generated` |

## Release Blockers Preserved

- `reviewed_reader_release_record_not_created_for_audio`
- `narration_script_not_reviewed`
- `audio_files_not_generated`
- `audio_spot_check_not_performed`
- `chapter_markers_not_timecoded`
- `audio_metadata_not_reviewed`
- `audio_embedded_epub_not_packaged_or_checked`
- `audio_edition_release_record_not_created`

Full narration review, pronunciation review, audio generation, listening spot
checks, chapter-marker timecoding, metadata review, and audio-embedded EPUB
packaging have not been completed.

## Non-Claims

- This manifest records a local audio-script review-workspace probe in ignored build space only.
- This manifest is not an audiobook, audio release, narration approval, edition release record, MP3 approval, M4B approval, or audio-embedded EPUB approval.
- This manifest does not approve EPUB, DOCX, PDF, HTML, e-reader, document, audio, MP3, M4B, or audio-embedded EPUB artifacts for publication.
- This manifest does not check narration quality, pronunciation quality, accessibility quality, full editorial quality, source interpretation, proof adequacy, theorem validity, benchmark behavior, runtime behavior, model quality, deployment safety, or release readiness.
- This manifest does not promote any chapter core claim and does not promote any claim support state.
