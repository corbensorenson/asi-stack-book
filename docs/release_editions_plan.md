# Release Editions Plan

Last updated: 2026-06-24

The living book is the canonical source. Major-version editions are derived artifacts for different audiences, not parallel manuscripts.

## Audience Model

| Audience | Needs | Primary surface |
|---|---|---|
| AIs and writing agents | stable ids, source queues, claim/evidence states, proof hooks, schemas, validation commands, guardrails | live Quarto/GitHub Pages book |
| Human researchers | complete technical argument, auditability, source and claim traceability, known residuals | live book and frozen research releases |
| Interested human readers | coherent narrative, e-reader/PDF/DOCX formatting, images and diagrams, bibliography, minimal workflow clutter | reader releases and audio releases |

## Tracked Source Files

- `editions/release_profiles.json` defines release profiles, audiences, strip rules, expected formats, release gates, and non-claims.
- `appendices/I_release_editions.qmd` publishes the model inside the live book.
- `scripts/validate_release_profiles.py` checks the profile metadata.
- `scripts/build_reader_edition.py` creates a cleaned reader-edition Quarto source tree under `build/reader_edition/`.
- `scripts/build_audio_script.py` creates a narration-script candidate under `build/audio_script/` after deriving the reader source.
- `schemas/edition_release_record.schema.json` defines public-safe records for future major-version research, reader, and audio releases.

## Reader Edition Generation

Check the reader profile without leaving generated files in the repo:

```bash
python3 scripts/build_reader_edition.py --check
```

Generate a local reader-edition source tree:

```bash
python3 scripts/build_reader_edition.py
```

The generated tree is ignored by git. Review it before rendering release artifacts.

From `build/reader_edition/`, later release runs can attempt specific formats:

```bash
quarto render --to epub
quarto render --to docx
quarto render --to html
```

PDF should be attempted only when local Quarto PDF dependencies are available:

```bash
quarto render --to pdf
```

Do not report EPUB, PDF, DOCX, or HTML reader artifacts unless the corresponding render actually succeeds and the result is recorded.

Optional downstream formats such as Markdown, plain text, MOBI, or AZW3 can be produced from the reviewed reader source or reviewed EPUB with external tools. They should be listed in a release record only after generation and spot-checking.

## Reader Strip Rules

The reader release removes repeated live-workflow sections by heading:

- `Chapter status`
- `Drafting guardrail`
- `Codex test plan`
- `External literature queue`
- `Source crosswalk`
- `Claim labels`
- `Why Codex tests matter`
- `Claim-source mapping status`
- `Formalization hooks`

The reader release keeps the core prose and diagrams. If an uncertainty caveat changes the meaning of a claim, keep it in the narrative rather than relying on a stripped guardrail block.

## Reader-Facing Spine

The live book can contain AI/research scaffolding, but the reader-facing spine should still read as a human manuscript after those sections are stripped. Essential thesis movement, uncertainty, examples, transitions, and diagrams belong in ordinary chapter prose, not only in live-only sections.

Before a major reader release, review the generated manuscript for:

- chapter-to-chapter continuity
- duplicated explanations introduced by live-book drafting passes
- missing transitions after stripped source crosswalks or proof hooks
- e-reader typography for diagrams, images, tables, and long code-adjacent terms
- bibliography and glossary usefulness for a non-specialist reader

## Audio Path

The audio release is downstream of a reviewed reader release. It should not be generated directly from the live book.

Generate the audio-script candidate with:

```bash
python3 scripts/build_audio_script.py --check
python3 scripts/build_audio_script.py
```

Required future artifacts:

- narration script by chapter
- pronunciation glossary
- table-to-prose conversion notes
- chapter markers and audio metadata
- spot-check record against the reviewed script
- release record listing actual audio formats produced

Embedding audio into an EPUB is allowed only when the produced EPUB actually contains the audio and the release record says so.

The generated audio script is a review workspace, not an audiobook. It marks tables, diagrams, images, code, and schemas for spoken treatment so they are not silently omitted.

## Major Version Rule

Each major version should have a public-safe release record under `release_records/` that states:

- source commit or tag
- edition profile
- formats actually rendered
- generated manuscript or script workspace used
- validation commands actually run
- validation status
- reader/audio review status
- residuals
- non-claims

This rule prevents the repo from naming a format as a goal and accidentally implying that the artifact already exists.
