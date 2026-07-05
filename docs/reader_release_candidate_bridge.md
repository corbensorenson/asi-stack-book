# Reader Release-Candidate Bridge

This note records the bounded reader release-candidate bridge for Living Book
Methodology.

Command:

```bash
python3 scripts/validate_reader_release_candidate_bridge.py
```

Result record:
`experiments/reader_release_candidate_bridge/results/2026-07-05-local.json`.

Lean bridge:
`lean:living_book.methodology.reader_release_candidate_bridge` in
`AsiStackProofs.LivingBook`.

## What It Checks

The bridge reads the tracked blocked curated-reader release candidate and
format-review matrix, then mirrors the same finite route in Lean and Python.
The current candidate is modeled as:

- local HTML, EPUB, DOCX, PDF, application, key-figure, keyboard-only, and
  accessibility-tree preparation evidence complete enough to be locally useful;
- screen-reader and WCAG conformance review still incomplete;
- audio files, listening review, chapter-marker timecoding, audio-embedded
  EPUB packaging, and audio release record still incomplete;
- reader release approval and approved edition release record still missing.

The actual tracked row is
`actual_current_curated_candidate_blocked_by_accessibility`, and it routes to
`request_accessibility_review`, not `approve_release`.

The bridge also checks synthetic controls for:

- accessibility complete but audio artifacts still missing;
- audio complete but release approval still missing;
- all release gates complete;
- `invalid_current_candidate_claimed_approved`, an invalid copy of the
  tracked current candidate claimed as approved while preserving the visible
  screen-reader, WCAG, audio, and release-approval blocker list;
- `invalid_screen_reader_missing_claimed_approved`;
- `invalid_wcag_conformance_missing_claimed_approved`;
- `invalid_audio_missing_claimed_approved`;
- `invalid_audio_files_missing_claimed_approved`;
- `invalid_chapter_markers_missing_claimed_approved`;
- `invalid_release_approval_missing_claimed_approved`;
- `invalid_reader_release_approval_missing_claimed_approved`;
- `invalid_approved_release_record_missing_claimed_approved`;
- invalid support-promotion and missing non-claim controls.

## Why It Matters

The release ladder now has substantial local preparation evidence. That
evidence is useful, but it must not become publication laundering. This bridge
keeps a crisp boundary: local format evidence, keyboard traversal,
accessibility-tree probes, Apple Books smoke review, DOCX application evidence,
PDF page review, audio-script narration treatment, and audio metadata do not
approve a reader release while screen-reader/WCAG, audio artifact, timecoding,
and explicit release-approval blockers remain.

## Boundary

This is a finite release-boundary bridge. It does not approve curated reader
HTML, EPUB, DOCX, PDF, e-reader, audio, MP3, M4B, or audio-embedded EPUB
artifacts. It does not publish a reader artifact to GitHub Pages or an external
archive. It does not create a source tag, DOI, Zenodo archive, audiobook, or
final reader release. It does not promote any chapter core claim above
`argument`.

The weakening condition is explicit: the reader-release boundary weakens if
local format evidence, keyboard/accessibility-tree probes, application smoke
checks, or audio-script metadata can be converted into release approval while
screen-reader, WCAG, audio artifact, timecoding, and explicit reader-release
approval blockers remain.
