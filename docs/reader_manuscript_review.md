# Reader Manuscript Review Baseline

Last updated: 2026-06-28

This note records the current Phase 2 reader-manuscript baseline for the v1.0 roadmap. It is a review-control document, not a reader release record.

## Generated Baseline

Command run:

```bash
python3 scripts/build_reader_edition.py
```

Generated workspace:

- `build/reader_edition/`
- 54 chapters
- 59 generated files
- target formats listed by profile: HTML, EPUB, PDF, DOCX
- 275 live-only sections removed
- 54 human-only bridges unwrapped
- 54 raw core-claim markers removed
- 50 repeated support-boilerplate passages humanized
- 60 reader scaffold terms humanized
- 0 active reader-overlay operations applied

Generated review files inspected:

- `build/reader_edition/READER_RELEASE_CHECKLIST.md`
- `build/reader_edition/companion_notes.md`
- `build/reader_edition/reader_delta_report.md`

Representative generated chapters spot-read:

- `build/reader_edition/chapters/asi-is-a-stack-not-a-model.qmd`
- `build/reader_edition/chapters/agency-dignity-and-corrigibility.qmd`
- `build/reader_edition/chapters/generate-verify-repair-compression.qmd`
- `build/reader_edition/chapters/open-research-agenda-and-bibliography-plan.qmd`

## What Is Working

- The generated reader source now has a coherent front door for the book: the first chapter opens as architecture prose rather than live scaffold.
- Human Reading Path bridges survive as ordinary prose, and reader-spine validation confirms all 54 chapters preserve Handoff continuity.
- Raw core-claim markers and repeated support boilerplate are stripped or humanized while the evidence boundary remains visible in the Core Claim prose.
- Source crosswalks, Codex test plans, drafting guardrails, and most live/research scaffolding are removed from the reader source.
- The reader delta workflow is in the correct shape: tracked overlays are the editable reader-delta source; generated reader files and generated delta reports are disposable review output.

## Residuals

- The generated manuscript has not received a full 54-chapter human continuity review. It is mechanically valid, not release-reviewed.
- The prose is still derived from the live AI/research book. It reads better than the live scaffold, but many chapters still carry technical interfaces, minimum-field lists, Mermaid diagrams, and implementation language that may need compression, rephrasing, or companion-note treatment for relaxed reading.
- Some reader chapters still contain useful but dense schema-like material. A final human edition should decide chapter by chapter whether to retain it, summarize it, move it to companion material, or leave it only in the live/research book.
- The current overlay manifest has zero active operations. That is a valid baseline, but it means no reader-only prose pacing, example insertion, or section-flow edits have been applied yet.
- No EPUB, PDF, DOCX, AZW3, MOBI, Markdown, plain-text, audio, or audio-embedded EPUB artifact has been rendered, reviewed, or released in this pass.
- No curated parallel reader manuscript exists yet. Graduation from generated source plus overlays remains a future decision once reader-only edits become too substantial for overlays.

## Next Review Pass

The next Phase 2 pass should:

1. Read the generated reader manuscript chapter by chapter for continuity, pacing, duplicated explanations, missing transitions, and e-reader readability.
2. Classify each finding as a canonical live-book edit, a reader-only overlay, companion-note treatment, or no action.
3. Add reader-only semantic deltas under `editions/reader_overlays/v1_0/` only when the live AI/research source should not change.
4. Keep evidence boundaries, support states, implementation horizons, and non-claims inherited from the live book.
5. Render reader HTML, EPUB, and DOCX only after the manuscript review is recorded. Attempt PDF only when local dependencies support it.
6. Generate audio-script review output only after the reader manuscript is reviewed.

## Non-Claims

- This baseline does not claim a reviewed reader release exists.
- This baseline does not claim any ebook, document, PDF, audio, or audio-embedded EPUB artifact exists.
- This baseline does not promote any claim support state.
- The live AI/research book remains canonical for claims, support states, source boundaries, proof/test status, implementation horizons, and release records.
