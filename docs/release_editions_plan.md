# Release Editions Plan

Last updated: 2026-06-27

The living book is the canonical source. Major-version editions are derived artifacts for different audiences, not parallel manuscripts.

## Audience Model

| Audience | Needs | Primary surface |
|---|---|---|
| AIs and writing agents | stable ids, source queues, claim/evidence states, proof hooks, schemas, validation commands, guardrails | live Quarto/GitHub Pages book |
| Human researchers | complete technical argument, auditability, source and claim traceability, known residuals | live book and frozen research releases |
| Interested human readers | coherent narrative, e-reader/PDF/DOCX formatting, images and diagrams, bibliography, minimal workflow clutter | reader releases and audio releases |

The live GitHub Pages site also provides a persistent reading-mode switch. `AI view` is the default canonical live-book view with chapter status, source crosswalks, proof hooks, Codex tests, and guardrails. `Human view` hides the same live-only chapter headings used by the reader-release strip policy so interested readers can stay on the site and read the prose spine without downloading an EPUB, PDF, or DOCX. Every manifest chapter now carries one `.asi-human-only` `Human Reading Path` bridge for human-specific orientation; reader generation unwraps those blocks and removes `.asi-ai-only` live research notes. This on-site view is a convenience projection; it is not a reviewed major-version reader artifact.

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
| Companion material | Reader/audio companion notes for diagrams, images, tables, code, schemas, omitted dense matrices, and audio-embedded EPUB packaging checks. | Generated as release-workspace review aids; not a substitute for reader prose, evidence ledgers, or actual artifact checks. |

Every chapter should keep meaning-critical caveats in the reader-facing spine. Live-only sections can expand the evidence trail, but they should not be the only place where a reader learns that a claim is speculative, blocked, or untested.

## Major-Version Artifact Ladder

Use this ladder for every major release:

1. The tagged live book remains canonical for AI agents and researchers.
2. A reader source tree is generated from that tag after stripping live-only scaffolding.
3. EPUB, PDF, DOCX, and reader HTML are rendered from the reviewed reader source, and each successful render is recorded separately.
4. Optional AZW3, MOBI, Markdown, or plain-text files are downstream conversions from the reviewed reader source or reviewed EPUB, not new sources.
5. Audio starts only after the reader manuscript is reviewed. MP3, M4B, and audio-embedded EPUB artifacts are separate products that require a reviewed script, generated audio, spot checks, metadata, and a release record.

The practical rule is simple: the live book is for AI agents and researchers, the reader release is for humans who want the book without workflow scaffolding, and the audio release is for listening. Each one is derived from the previous public-safe state and must say exactly which artifacts exist.

## Human Consumption Bundle

A major version can have a human-consumption bundle, but the bundle is assembled in layers rather than treated as one artifact:

| Class | Formats | Gate |
|---|---|---|
| Reader formats | HTML, EPUB, PDF, DOCX | Render from the reviewed reader source and record each successful artifact separately. |
| Optional e-reader conversions | AZW3, MOBI, Markdown, plain text | Convert only from reviewed reader source or reviewed EPUB, then spot-check navigation, figures, tables, and wrapping. |
| Audio artifacts | MP3, M4B | Generate only from a reviewed narration script and spot-check against that script. |
| Audio embedded in EPUB | audio-embedded EPUB | Verify that the packaged EPUB actually contains playable reviewed audio before listing it as produced. |

The reader manuscript is the human source for the bundle. The audio script is downstream of that reader manuscript. The live book remains the canonical source for AI agents and researchers after the human bundle is produced.

## Tracked Source Files

- `editions/release_profiles.json` defines release profiles, audiences, strip rules, expected formats, release gates, and non-claims.
- `appendices/I_release_editions.qmd` publishes the model inside the live book.
- `docs/major_version_release_runbook.md` gives the operational sequence for live, research, reader, ebook/document, and audio release work.
- `scripts/validate_release_profiles.py` checks the profile metadata.
- `scripts/build_reader_edition.py` creates a cleaned reader-edition Quarto source tree under `build/reader_edition/`.
- `scripts/validate_reader_spine.py` checks the generated reader manuscript for substantial chapter prose, required reader headings, view-block cleanup, and stripped live-only scaffolding.
- `scripts/validate_human_reading_paths.py` checks that every manifest chapter has exactly one Human Reading Path bridge and that generated reader chapters retain it as ordinary prose.
- `scripts/render_reader_formats.py` attempts selected reader-edition renders and writes `reader_render_report.json` with actual local outcomes.
- `scripts/build_audio_script.py` creates a narration-script candidate under `build/audio_script/` after deriving the reader source.
- `schemas/edition_release_record.schema.json` defines public-safe records for future major-version research, reader, and audio releases.
- `assets/reading-mode.html` and `assets/styles.scss` implement the live-site reading-mode switch.
- `scripts/validate_reading_mode_toggle.py` checks that the live-site Human view tracks `reader_release.strip_headings`, uses the recorded local-storage key, and exposes the assistive description/status contract.
- `scripts/validate_live_human_view.py` runs after `quarto render --to html` and checks that rendered chapter pages include the toggle, assistive status strings, live-only headings needed for runtime hiding, and any source view-mode block classes such as `.asi-human-only`.

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

Each generated reader tree includes `reader_manifest.json`, which records the source profile, target formats, content-layer policy, stripped-heading policy, view-block processing counts, review status, e-reader quality checks, downstream-format notes, companion-material policy, and non-claims. It also includes `READER_RELEASE_CHECKLIST.md` as the local review checklist for continuity, typography, figure/diagram behavior, EPUB/DOCX/PDF checks, optional e-reader conversions, companion notes, and release-record residuals. The generated `companion_notes.md` records stripped live-only section counts and the dense material that needs reader/audio treatment. These files are release-preparation aids; they are not evidence that any ebook or PDF has been rendered.

The generated reader manifest also carries the human-consumption bundle policy so a release run can distinguish reader formats, optional e-reader conversions, and later audio artifacts without relying on memory.

`docs/major_version_release_runbook.md` is the checklist to follow once a tagged major version is ready. It keeps the live/research surface, reader manuscript, and audio package in a single derivation ladder so a generated source tree cannot be mistaken for a published artifact.

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

The live-site `Human view` uses this same heading list at render time. `.asi-live-only` and `.asi-ai-only` blocks are hidden in Human view; `.asi-human-only` Human Reading Path blocks are hidden in AI view and shown in Human view. If these strip rules change, update the reading-mode asset and run:

```bash
python3 scripts/validate_reading_mode_toggle.py
python3 scripts/validate_human_reading_paths.py
quarto render --to html
python3 scripts/validate_live_human_view.py
```

`scripts/validate_human_reading_paths.py` checks the source chapters before a reader manuscript is generated: each manifest chapter must have exactly one Human Reading Path bridge, the bridge must appear before the main problem statement, and the generated reader chapter must retain exactly one `Human Reading Path` heading without view-mode markers.

`scripts/validate_reader_spine.py --check` derives the reader manuscript in a temporary workspace and fails if stripped headings remain, if view-mode markers leak into generated reader source, if hard live-only terms such as `Drafting guardrail` or `Codex test plan` leak into generated chapter prose, if a required reader heading is missing, or if a chapter falls below the configured minimum reader-spine word count. A normal run writes `build/reader_spine_report.json`, which is ignored by git and is useful during major-version review.

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

The generated audio workspace includes `audio_manifest.json`, `AUDIO_RELEASE_CHECKLIST.md`, `chapter_markers.md`, `pronunciation_glossary.md`, and `companion_notes.md`. The manifest records that the script was derived from the reader release path and still requires review before any MP3, M4B, or audio-embedded EPUB can be claimed. The companion notes count tables, diagrams, code/schema blocks, and images by script file so the narration review can decide what is spoken, summarized, or moved to companion material. The checklist records table/diagram/code spoken-treatment requirements, packaging checks, and the rule that an audio-embedded EPUB exists only after the reviewed audio files are actually embedded and checked.

The audio manifest carries the same human-consumption bundle policy, but only to enforce dependency direction. Audio is not a shortcut around reader review, and audio embedded in EPUB remains a separate checked artifact.

## Major Version Rule

Each major version should have a public-safe release record under `release_records/` that states:

- source commit or tag
- edition profile
- formats actually rendered
- generated manuscript or script workspace used
- validation commands actually run
- validation status
- reader/audio review status
- human-consumption gate status
- audiobook gate status
- residuals
- non-claims

This rule prevents the repo from naming a format as a goal and accidentally implying that the artifact already exists.
