# Reader Overlay Pilot

Last updated: 2026-06-28

This note records the first active v1.0 semantic reader-overlay pilot. It is a reader-prose control record, not a reader release record.

## Scope

The pilot adds two active operations under `editions/reader_overlays/v1_0/chapters/asi-is-a-stack-not-a-model.json`:

- `v1_0.asi_stack_not_model.problem_reader_replace` replaces the generated-reader and live Human-view `Problem` section for `chapters/asi-is-a-stack-not-a-model.qmd`.
- `v1_0.asi_stack_not_model.summary_reader_replace` replaces the generated-reader and live Human-view `Summary` section for the same chapter.

The canonical chapter source remains unchanged. AI view keeps the original live/research prose, source mappings, claim labels, support state, proof hooks, test-plan surface, and source crosswalk. Human view and generated reader editions receive the reader-only section prose through the same tracked overlay payload.

## Why This Pilot Exists

The v1.0 roadmap allows the normal reader edition to diverge from the AI/research source for pacing, prose flow, and relaxed reading, while keeping the live book canonical for claims, support states, source boundaries, proof/test status, implementation horizons, and release records. This pilot exercises that path on the opening chapter before scaling chapter-by-chapter reader editing.

The opening chapter is a good pilot because it has high reader-framing value and low claim risk. The overlay does not change the core claim. It rewrites the first problem statement and closing summary into calmer book prose so the Human view can begin as a readable book while the AI/research view remains a full architecture workbench.

## Review Contract

Reviewers should compare the generated `build/reader_edition/reader_delta_report.md` against the tracked operation file. The delta report should show both operation digests and before/after excerpts after `python3 scripts/build_reader_edition.py` runs.

For live-site review, `assets/reader-overlays.html` should be regenerated from the overlay source with `python3 scripts/sync_reader_overlay_asset.py`, and browser validation should confirm the embedded operation count is processed in Human view.

## Local Validation

Current local results for this pilot:

- `python3 scripts/sync_reader_overlay_asset.py` regenerated `assets/reader-overlays.html` with 2 active operations.
- `python3 scripts/build_reader_edition.py` regenerated `build/reader_edition/`; `reader_delta_report.md` records 2 active and 2 applied operations.
- `python3 scripts/sync_reader_overlay_asset.py --check` passed with 2 active operations.
- `python3 scripts/validate_reader_overlays.py --check` passed with 2 active operations and 2 applied operations.
- `python3 scripts/build_reader_edition.py --check` passed for 54 chapters, 59 files, 275 stripped live-only sections, 60 humanized reader-scaffold terms, and 2 reader overlay operations applied.
- `python3 scripts/validate_reader_spine.py --check` passed for 54 chapters, with minimum reader-spine length 1,957 words.
- `python3 scripts/validate_reader_evidence_boundaries.py --check` passed for 54 chapters.
- `LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 quarto render --to html` completed and wrote `_site/index.html`.
- `python3 scripts/validate_live_human_view.py` passed for 67 rendered book pages and 54 rendered chapter pages.
- `node scripts/validate_live_human_view_browser.js --all-chapters --all-viewports` passed for 112 rendered page-view pairs.

## Non-Claims

- This pilot is not a reviewed reader manuscript.
- This pilot is not an EPUB, DOCX, PDF, audiobook, audio-embedded EPUB, or edition release.
- This pilot does not introduce new source-derived claims.
- This pilot does not promote any support state.
- This pilot does not claim proof adequacy, benchmark behavior, runtime behavior, or implementation completion.

## Remaining Work

- Review the generated reader delta report after each overlay edit.
- Expand reader-only overlays only where the live AI/research source should remain unchanged.
- Make canonical chapter edits when reader review reveals a problem that also affects AI/research readers.
- Graduate to a curated parallel reader manuscript only when overlays become too large or too numerous to remain a clean semantic delta layer.
