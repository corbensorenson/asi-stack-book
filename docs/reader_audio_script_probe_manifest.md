# Reader Audio-Script Probe Manifest

Last updated: 2026-06-30

This summary is synced from
`editions/reader_manuscript/v1_0/audio_script_probe_manifest.json`. It records
the latest tracked local audio-script review-workspace facts for the generated
reader edition. It is not an audiobook, not narration approval, not an audio
release, and not a support-state promotion.

## Commands

```bash
python3 scripts/build_audio_script.py --check
python3 scripts/build_audio_script.py
python3 - <<'PY' ... import scripts/build_audio_script.py and inspect audio_manifest.json in a temporary workspace ...
```

## Script Workspace Summary

| Field | Value |
|---|---:|
| Source profile | `reader_release` |
| Audio profile | `audio_release` |
| Script files | 54 |
| Implementation-horizon script status | pass |
| Review status | review_required |

Required review files are generated in the ignored workspace:
`audio_manifest.json`, `AUDIO_RELEASE_CHECKLIST.md`, `companion_notes.md`,
`chapter_markers.md`, `pronunciation_glossary.md`, and
`proof_equation_reading_rules.md`.

## Companion Treatment Totals

| Material | Count |
|---|---:|
| Tables | 5 |
| Mermaid diagrams | 57 |
| Code/schema blocks | 0 |
| Images | 1 |

These counts are script-preparation cues. They tell a future narration review
where tables, diagrams, images, or dense material need spoken summaries or
companion-note routing before any audio artifact can be claimed.

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
