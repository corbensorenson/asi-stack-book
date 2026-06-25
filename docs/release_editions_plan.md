# Release Editions Plan

Last updated: 2026-06-25

The living book is the canonical source. Major-version editions are derived artifacts for different audiences, not parallel manuscripts.

## Audience Model

| Audience | Needs | Primary surface |
|---|---|---|
| AIs and writing agents | stable ids, source queues, claim/evidence states, proof hooks, schemas, validation commands, guardrails | live Quarto/GitHub Pages book |
| Human researchers | complete technical argument, auditability, source and claim traceability, known residuals | live book and frozen research releases |
| Interested human readers | coherent narrative, e-reader/PDF/DOCX formatting, images and diagrams, bibliography, minimal workflow clutter | reader releases and audio releases |

## Content Layers

The live book serves all three audiences by separating content layers instead of maintaining parallel books:

| Layer | Purpose | Reader/audio treatment |
|---|---|---|
| Reader-facing chapter spine | The ordinary chapter prose, diagrams, mechanisms, examples, uncertainty, and summaries that should still read as a coherent manuscript. | Retained in reader releases; adapted into narration for audio. |
| Live research scaffold | Chapter status, guardrails, source crosswalks, claim-source mappings, Codex tests, formalization hooks, and source-loading notes. | Kept in live/research releases; stripped or summarized for reader/audio releases. |
| Evidence and source matrices | Appendices, source notes, schemas, release records, test specs, proof manifest, bibliography, and changelog. | Kept for live/research; reader releases keep selected human-useful appendices such as glossary and bibliography. |
| Machine-readable contracts | `book_structure.json`, `docs/book_outline.md`, inventories, schemas, scripts, Lean modules, and validation commands. | Canonical for AI/writing agents; excluded from reader/audio manuscripts except where explained in prose. |
| Release derivatives | Generated reader source, EPUB/PDF/DOCX/HTML builds, audio scripts, MP3/M4B packages, and audio-embedded EPUBs. | Non-canonical outputs that exist only after generation, review or render, and release-record entry. |
| Audio adaptation | Narration script, pronunciation guidance, chapter markers, and spoken-treatment notes. | Derived from the reviewed reader release, not directly from the live book. |

Every chapter should keep meaning-critical caveats in the reader-facing spine. Live-only sections can expand the evidence trail, but they should not be the only place where a reader learns that a claim is speculative, blocked, or untested.

## Major-Version Artifact Ladder

Use this ladder for every major release:

1. The tagged live book remains canonical for AI agents and researchers.
2. A reader source tree is generated from that tag after stripping live-only scaffolding.
3. EPUB, PDF, DOCX, and reader HTML are rendered from the reviewed reader source, and each successful render is recorded separately.
4. Optional AZW3, MOBI, Markdown, or plain-text files are downstream conversions from the reviewed reader source or reviewed EPUB, not new sources.
5. Audio starts only after the reader manuscript is reviewed. MP3, M4B, and audio-embedded EPUB artifacts are separate products that require a reviewed script, generated audio, spot checks, metadata, and a release record.

The practical rule is simple: the live book is for AI agents and researchers, the reader release is for humans who want the book without workflow scaffolding, and the audio release is for listening. Each one is derived from the previous public-safe state and must say exactly which artifacts exist.

## Tracked Source Files

- `editions/release_profiles.json` defines release profiles, audiences, strip rules, expected formats, release gates, and non-claims.
- `appendices/I_release_editions.qmd` publishes the model inside the live book.
- `scripts/validate_release_profiles.py` checks the profile metadata.
- `scripts/build_reader_edition.py` creates a cleaned reader-edition Quarto source tree under `build/reader_edition/`.
- `scripts/validate_reader_spine.py` checks the generated reader manuscript for substantial chapter prose and stripped live-only scaffolding.
- `scripts/render_reader_formats.py` attempts selected reader-edition renders and writes `reader_render_report.json` with actual local outcomes.
- `scripts/build_audio_script.py` creates a narration-script candidate under `build/audio_script/` after deriving the reader source.
- `schemas/edition_release_record.schema.json` defines public-safe records for future major-version research, reader, and audio releases.

## Reader Edition Generation

Check the reader profile without leaving generated files in the repo:

```bash
python3 scripts/build_reader_edition.py --check
python3 scripts/validate_reader_spine.py --check
```

Generate a local reader-edition source tree:

```bash
python3 scripts/build_reader_edition.py
```

The generated tree is ignored by git. Review it before rendering release artifacts.

Each generated reader tree includes `reader_manifest.json`, which records the source profile, target formats, content-layer policy, stripped-heading policy, removed section counts, review status, e-reader quality checks, downstream-format notes, and non-claims. It also includes `READER_RELEASE_CHECKLIST.md` as the local review checklist for continuity, typography, figure/diagram behavior, EPUB/DOCX/PDF checks, optional e-reader conversions, and release-record residuals. These files are release-preparation aids; they are not evidence that any ebook or PDF has been rendered.

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

For a recorded local render attempt, use:

```bash
python3 scripts/render_reader_formats.py --check
python3 scripts/render_reader_formats.py --formats html epub docx
python3 scripts/render_reader_formats.py --formats html epub docx pdf
```

This writes `build/reader_edition/reader_render_report.json`. A successful report is still not a major-version publication until the manuscript is reviewed and an edition release record names the produced artifacts.

Optional downstream formats such as Markdown, plain text, MOBI, or AZW3 can be produced from the reviewed reader source or reviewed EPUB with external tools. They should be listed in a release record only after generation and spot-checking.

Images and diagrams remain part of the reader path when they carry meaning. For audio, they need either a concise spoken walkthrough or a companion-note route before an audiobook or audio-embedded EPUB is claimed.

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

`scripts/validate_reader_spine.py --check` derives the reader manuscript in a temporary workspace and fails if stripped headings remain, if hard live-only terms such as `Drafting guardrail` or `Codex test plan` leak into generated chapter prose, or if a chapter falls below the configured minimum reader-spine word count. A normal run writes `build/reader_spine_report.json`, which is ignored by git and is useful during major-version review.

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

The generated audio workspace includes `audio_manifest.json`, `AUDIO_RELEASE_CHECKLIST.md`, `chapter_markers.md`, and `pronunciation_glossary.md`. The manifest records that the script was derived from the reader release path and still requires review before any MP3, M4B, or audio-embedded EPUB can be claimed. The checklist records table/diagram/code spoken-treatment requirements, packaging checks, and the rule that an audio-embedded EPUB exists only after the reviewed audio files are actually embedded and checked.

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
