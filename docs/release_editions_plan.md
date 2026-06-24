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

## Audio Path

The audio release is downstream of a reviewed reader release. It should not be generated directly from the live book.

Required future artifacts:

- narration script by chapter
- pronunciation glossary
- table-to-prose conversion notes
- chapter markers and audio metadata
- spot-check record against the reviewed script
- release record listing actual audio formats produced

Embedding audio into an EPUB is allowed only when the produced EPUB actually contains the audio and the release record says so.

## Major Version Rule

Each major version should have a public-safe release record under `release_records/` that states:

- source commit or tag
- edition profile
- formats actually rendered
- validation commands actually run
- validation status
- residuals
- non-claims

This rule prevents the repo from naming a format as a goal and accidentally implying that the artifact already exists.
