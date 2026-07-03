# Release Editions Plan

Last updated: 2026-06-28

The living book is the canonical architecture, evidence, source, proof, schema, and release-control source. Major-version editions begin as derived artifacts for different audiences. Once the normal reader manuscript needs sustained prose editing, it may become a curated parallel derivative source for human reading, but it is not an equal authority: claims, support states, source boundaries, proof/test status, implementation horizons, and release records remain governed by the live book.

## Audience Model

| Audience | Needs | Primary surface |
|---|---|---|
| AIs and writing agents | stable ids, source queues, claim/evidence states, proof hooks, schemas, validation commands, guardrails | live Quarto/GitHub Pages book |
| Human researchers | complete technical argument, auditability, source and claim traceability, known residuals | live book and frozen research releases |
| Interested human readers | coherent narrative, e-reader/PDF/DOCX formatting, images and diagrams, bibliography, minimal workflow clutter | reader releases and audio releases |

The live GitHub Pages site also provides a persistent reading-mode switch. `AI view` is the default canonical live-book view with chapter status, source crosswalks, proof hooks, Codex tests, guardrails, raw core-claim markers, and repeated support-state boilerplate. `Human view` hides the same live-only chapter headings, page-TOC entries, visible section numbers, raw bracketed core-claim markers, and repeated support boilerplate used by the reader-release strip policy so interested readers can stay on the site and read the prose spine without downloading an EPUB, PDF, or DOCX. Readers can also open a chapter directly in either projection with `?view=human` or `?view=ai`. Every manifest chapter now carries one `.asi-human-only` `Human Reading Path` bridge for human-specific orientation; reader generation unwraps those blocks, removes `.asi-ai-only` live research notes, strips raw core-claim markers and repeated support boilerplate while preserving claim text and a compact inline evidence-boundary phrase, preserves one Handoff section per generated chapter, and now validates section-level word/prose-paragraph floors after stripping. The embedded reader-overlay payload is processed by the same live Human-view runtime used for the toggle, and rendered pages expose operation-count attributes so browser validation can prove the payload was actually processed. This on-site view is a convenience projection; it is not a reviewed major-version reader artifact.

## Content Layers

The live book serves all three audiences by separating content layers instead of maintaining parallel books:

| Layer | Purpose | Reader/audio treatment |
|---|---|---|
| Reader-facing chapter spine | The ordinary chapter prose, diagrams, mechanisms, examples, uncertainty, and summaries that should still read as a coherent manuscript. | Retained in reader releases; adapted into narration for audio. |
| Live research scaffold | Chapter status, guardrails, source crosswalks, claim-source mappings, Codex tests, formalization hooks, and source-loading notes. | Kept in live/research releases; stripped or summarized for reader/audio releases. |
| Evidence and source matrices | Appendices, source notes, schemas, release records, test specs, proof manifest, Corben's sources/local projects, external literature by other authors, and changelog. | Kept for live/research; reader releases keep selected human-useful appendices such as glossary, Corben's sources/local projects, and the separate external-literature appendix. |
| Machine-readable contracts | `book_structure.json`, `docs/book_outline.md`, inventories, schemas, scripts, Lean modules, and validation commands. | Canonical for AI/writing agents; excluded from reader/audio manuscripts except where explained in prose. |
| Curated reader manuscript | A reviewed human-prose source that may eventually diverge from the live AI/research text for pacing, section flow, examples, and relaxed reading. | Parallel derivative source for narrative only; must reconcile back to live-book claims, support states, source boundaries, proof/test status, implementation horizons, and release records. |
| Release derivatives | Generated reader source, EPUB/PDF/DOCX/HTML builds, audio scripts, MP3/M4B packages, and audio-embedded EPUBs. | Non-canonical outputs that exist only after generation, review or render, and release-record entry. |
| Audio adaptation | Narration script, pronunciation guidance, chapter markers, and spoken-treatment notes. | Derived from the reviewed reader release, not directly from the live book. |
| Companion material | Reader/audio companion notes for diagrams, images, tables, code, schemas, omitted dense matrices, and audio-embedded EPUB packaging checks. | Generated as release-workspace review aids; not a substitute for reader prose, evidence ledgers, or actual artifact checks. |

Every chapter should keep meaning-critical caveats in the reader-facing spine. Live-only sections can expand the evidence trail, but they should not be the only place where a reader learns that a claim is speculative, blocked, or untested.

Reader-source divergence is allowed only after review shows that generated reader source plus overlays are too limited for a high-quality human book. The manifest-synced review matrix at `editions/reader_manuscript/v1_0/chapter_review_matrix.json` is the durable queue for that decision: it records each manifest chapter's review status, active overlay count, companion-note candidate status, curated-manuscript candidate status, and release blockers. At graduation, the curated reader manuscript becomes a tracked human-prose source, while `book_structure.json`, `docs/book_outline.md`, Appendix C, source appendices, proof artifacts, and release records remain authoritative for evidence and structure. Each major reader release should include a reconciliation report that confirms the curated reader manuscript still maps to manifest chapters and preserves support boundaries.

## Major-Version Artifact Ladder

Use this ladder for every major release:

1. The tagged live book remains canonical for AI agents and researchers.
2. A reader source tree is generated from that tag after stripping live-only scaffolding.
3. If the major version uses a curated reader manuscript, reconcile it against the generated source and live-book manifest before rendering.
4. EPUB, PDF, DOCX, and reader HTML are rendered from the reviewed reader source, and each successful render is recorded separately.
5. Optional AZW3, MOBI, Markdown, or plain-text files are downstream conversions from the reviewed reader source or reviewed EPUB, not new sources.
6. Audio starts only after the reader manuscript is reviewed. MP3, M4B, and audio-embedded EPUB artifacts are separate products that require a reviewed script, generated audio, spot checks, metadata, and a release record.

The practical rule is simple: the live book is for AI agents and researchers, the reader release is for humans who want the book without workflow scaffolding, and the audio release is for listening. Each one is derived from the previous public-safe state and must say exactly which artifacts exist.

## Human Consumption Bundle

A major version can have a human-consumption bundle, but the bundle is assembled in layers rather than treated as one artifact:

| Class | Formats | Gate |
|---|---|---|
| Reader formats | HTML, EPUB, PDF, DOCX | Render from the reviewed reader source and record each successful artifact separately. |
| Optional e-reader conversions | AZW3, MOBI, Markdown, plain text | Convert only from reviewed reader source or reviewed EPUB, then spot-check navigation, figures, tables, and wrapping. |
| Audio artifacts | MP3, M4B | Generate only from a reviewed narration script and spot-check against that script. |
| Audio embedded in EPUB | audio-embedded EPUB | Verify that the packaged EPUB actually contains playable reviewed audio before listing it as produced. |

The reader manuscript is the human-prose source for the bundle. The audio script is downstream of that reader manuscript. The live book remains the canonical source for AI agents, researchers, claim/evidence state, proof/test status, and future source ingestion after the human bundle is produced.

## Tracked Source Files

- `editions/release_profiles.json` defines release profiles, audiences, strip rules, expected formats, release gates, and non-claims.
- `editions/reader_overlays/` defines versioned semantic reader overlays for human-edition deltas that should survive regeneration without forking the live book.
- `editions/reader_manuscript/v1_0/manifest.json` records the curated reader-manuscript path, its graduation criteria, allowed prose divergence, blocked evidence divergence, generated-reader baseline, reconciliation requirement, and current `drafting` status with forty-four curated chapter records: five still drafting and thirty-nine reconciled for prose meaning, with no active manifest chapter missing a curated reader file. Its reader handoff contract records the book-level thesis, four part arcs, ten recurring signature ideas, ten key-figure targets, twelve Corben voice-pass slots, and chapter-specific stakes/payoffs while preserving the no-release boundary. The prose-pass notes under `docs/curated_reader_*_prose_pass.md`, including `docs/curated_reader_asi_stack_prose_pass.md`, `docs/curated_reader_compact_generative_systems_prose_pass.md`, and `docs/curated_reader_rankfold_artifact_compression_prose_pass.md`, record chapter-level curation scopes, reader promises, meaning-preservation checks, non-claims, reconciliation state where applicable, and blockers. `editions/reader_manuscript/v1_0/reconciliation_report.md` records the chapter-level reconciliation statuses and keeps release blockers active until reconciliation, format review, and an edition release record exist.
- `editions/reader_manuscript/v1_0/companion_notes/` now contains three drafting companion notes for dense e-reader and audio treatment: Circle proof receipts, executable-specification proof lanes, and artifact-steward project objects. They explain dense vocabulary and spoken-treatment choices while leaving meaning-critical limits in the reader spine. They are not release artifacts or artifact reviews.
- `editions/reader_manuscript/v1_0/chapter_review_matrix.json` records the manifest-synced human-reader chapter review queue; `docs/reader_chapter_review_matrix.md` is the generated public summary.
- `appendices/J_release_editions.qmd` publishes the model inside the live book.
- `docs/major_version_release_runbook.md` gives the operational sequence for live, research, reader, ebook/document, and audio release work.
- `scripts/validate_release_profiles.py` checks the profile metadata.
- `scripts/build_reader_edition.py` creates a cleaned reader-edition Quarto source tree under `build/reader_edition/`.
- `scripts/validate_reader_overlays.py` checks the reader-overlay manifest and confirms generated reader builds include a coherent `reader_delta_report.md` with either a zero-active-operation note or operation digests and before/after review excerpts.
- `scripts/audit_reader_continuity.py --check` verifies that `docs/reader_continuity_audit.md` matches the current generated reader source and remains a heuristic review queue rather than a manual review claim.
- `scripts/validate_reader_manuscript_manifest.py` checks that any future curated reader manuscript remains a parallel derivative source for prose and cannot silently diverge from manifest chapter IDs, support boundaries, source boundaries, proof/test status, implementation horizons, release records, or the explicit reader-handoff metadata needed for Corben review.
- `scripts/sync_reader_chapter_review_matrix.py --check` checks that the reader-review queue stays in manifest order with current overlay counts and explicit release blockers.
- `scripts/sync_reader_overlay_asset.py` embeds active overlay operations in `assets/reader-overlays.html` so the live Human view can apply the same section deltas as generated reader editions.
- `scripts/validate_reader_spine.py` checks the generated reader manuscript for substantial chapter prose, required reader headings, chapter-specific Handoff continuity, view-block cleanup, and stripped live-only scaffolding.
- `scripts/validate_reader_evidence_boundaries.py` checks that generated reader chapters strip raw live core-claim markers and repeated support boilerplate while preserving claim text and inline plain-language support-state boundaries.
- `scripts/validate_human_reading_paths.py` checks that every manifest chapter has exactly one Human Reading Path bridge and that generated reader chapters retain it as ordinary prose.
- `scripts/render_reader_formats.py` attempts selected reader-edition renders, snapshots successful format outputs under ignored `build/reader_edition/format_artifacts/`, and writes `reader_render_report.json` with actual local outcomes.
- `scripts/inspect_reader_format_artifacts.py` structurally inspects ignored local HTML/EPUB/DOCX snapshots for expected files, EPUB/DOCX container integrity, media counts, and obvious live-scaffold leaks.
- `scripts/build_audio_script.py` creates a narration-script candidate under `build/audio_script/` after deriving the reader source, and its check verifies that chapter scripts preserve the minimum-viable and beyond-state-of-the-art implementation horizons.
- `editions/reader_manuscript/v1_0/audio_script_probe_manifest.json`, `docs/reader_audio_script_probe_manifest.md`, and `scripts/validate_reader_audio_script_probe_manifest.py` record and check the current audio-script review-workspace probe without treating the ignored scripts as narration approval or audio artifacts.
- `schemas/edition_release_record.schema.json` defines public-safe records for future major-version research, reader, and audio releases.
- `assets/reading-mode.html` and `assets/styles.scss` implement the live-site reading-mode switch.
- `scripts/validate_reading_mode_toggle.py` checks that the live-site Human view tracks `reader_release.strip_headings`, uses the recorded local-storage key and URL query parameter, hides live-only page-TOC entries, section numbers, raw core-claim markers, and repeated support boilerplate, and exposes the assistive description/status contract.
- `scripts/validate_live_human_view.py` runs after `quarto render --to html` and checks that every rendered book page includes the toggle and assistive status strings, and that rendered chapter pages include the live-only headings, TOC targets, and source view-mode block classes such as `.asi-human-only` needed for runtime hiding.
- `scripts/validate_live_human_view_browser.js` runs after HTML render and, when Playwright/Chrome is available, opens representative rendered pages by default or every manifest chapter across desktop and mobile viewports with `--all-chapters --all-viewports` to check `?view=human`, `?view=ai`, local persistence, live-section hiding, TOC hiding, raw marker and support-boilerplate hiding/restoration, bridge visibility, rendered Mermaid visibility, reading-mode control visibility, reader-overlay payload availability and runtime operation-count processing, page-level horizontal overflow, and AI-view restoration.

## Reader Edition Generation

Check the reader profile without leaving generated files in the repo:

```bash
python3 scripts/build_reader_edition.py --check
python3 scripts/sync_reader_overlay_asset.py --check
python3 scripts/validate_reader_overlays.py --check
python3 scripts/audit_reader_continuity.py --check
python3 scripts/validate_reader_manuscript_manifest.py
python3 scripts/sync_reader_chapter_review_matrix.py --check
python3 scripts/validate_reader_evidence_boundaries.py --check
python3 scripts/validate_reader_spine.py --check
```

Generate a local reader-edition source tree:

```bash
python3 scripts/build_reader_edition.py
```

The generated tree is ignored by git. Review it before rendering release artifacts.

Each generated reader tree includes `reader_manifest.json`, which records the source profile, target formats, content-layer policy, stripped-heading policy, view-block processing counts, reader-overlay status, reader-spine validation policy, Handoff continuity review requirement, review status, e-reader quality checks, downstream-format notes, companion-material policy, and non-claims. It also includes `READER_RELEASE_CHECKLIST.md` as the local review checklist for continuity, Handoff review, overlay delta review, typography, figure/diagram behavior, EPUB/DOCX/PDF checks, optional e-reader conversions, companion notes, and release-record residuals. The generated `companion_notes.md` records stripped live-only section counts and the dense material that needs reader/audio treatment. The generated `reader_delta_report.md` records generator transformations, editable overlay source, loaded operation files, operation content digests, before/after review excerpts, review checklist, and any semantic overlay operations applied for the major reader version. The tracked overlay files under `editions/reader_overlays/` are the editable reader-delta source; the generated report is reviewed, not manually patched. The tracked `assets/reader-overlays.html` payload is the live-site counterpart for those same active overlay operations. These files are release-preparation aids; they are not evidence that any ebook or PDF has been rendered.

The generated reader manifest also carries the human-consumption bundle policy so a release run can distinguish reader formats, optional e-reader conversions, and later audio artifacts without relying on memory.

The tracked `docs/reader_continuity_audit.md` is regenerated from a temporary reader-edition workspace. It gives the human review pass a deterministic queue based on word counts, table/code/diagram density, repeated-opening heuristics, and reader-overlay counts. It is not a replacement for reading the manuscript.

`docs/major_version_release_runbook.md` is the checklist to follow once a tagged major version is ready. It keeps the live/research surface, reader manuscript, and audio package in a single derivation ladder so a generated source tree cannot be mistaken for a published artifact.

From `build/reader_edition/`, later release runs can attempt specific formats:

```bash
quarto render --to epub
quarto render --to docx
quarto render --to html
```

PDF should be attempted only when local Quarto PDF dependencies are available:

```bash
LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 quarto render --to pdf
```

Do not report EPUB, PDF, DOCX, or HTML reader artifacts unless the corresponding render actually succeeds and the result is recorded.

For a recorded local render attempt, use:

```bash
python3 scripts/render_reader_formats.py --check
python3 scripts/render_reader_formats.py --formats html epub docx
python3 scripts/inspect_reader_format_artifacts.py
LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 python3 scripts/render_reader_formats.py --formats html epub docx pdf
```

This writes `build/reader_edition/reader_render_report.json`, snapshots successful formats under `build/reader_edition/format_artifacts/` for local review, and can write `build/reader_edition/reader_artifact_inspection_report.json` after structural inspection. A successful report is still not a major-version publication until the manuscript is reviewed and an edition release record names the produced artifacts.

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

The live-site `Human view` uses this same heading list at render time. `.asi-live-only` and `.asi-ai-only` blocks are hidden in Human view; matching page-TOC entries are hidden with runtime markers; visible section numbers are hidden so filtered chapters do not show numbering gaps; raw bracketed core-claim markers are hidden while their claim text remains visible; repeated support-state boilerplate is hidden while a compact `evidence boundary: architectural argument` parenthetical is attached to the core claim; `.asi-human-only` bridge blocks are hidden in AI view, shown as unheaded lead-in prose in Human view, and omitted from the page TOC because they are internal reader scaffolding rather than navigable manuscript sections; `?view=human` and `?view=ai` deep-link directly into the chosen projection. If these strip rules or mode-linking rules change, update the reading-mode asset and run:

```bash
python3 scripts/validate_reading_mode_toggle.py
python3 scripts/validate_human_reading_paths.py
python3 scripts/validate_reader_evidence_boundaries.py --check
quarto render --to html
python3 scripts/validate_live_human_view.py
node scripts/validate_live_human_view_browser.js --all-chapters --all-viewports
```

`scripts/validate_human_reading_paths.py` checks the source chapters before a reader manuscript is generated: each manifest chapter must have exactly one Human Reading Path bridge, the bridge must appear before the main problem statement, and the generated reader chapter must retain the bridge prose without the source-only `Human Reading Path` heading or view-mode markers.

`scripts/validate_reader_spine.py --check` derives the reader manuscript in a temporary workspace and fails if generated chapters do not start with their manifest titles, if stripped headings remain, if view-mode markers or source-only Human Reading Path markers leak into generated reader source, if hard live-only terms such as `Drafting guardrail`, `Codex test plan`, `Codex workflow`, `source crosswalk`, or hyphenated `source-note` jargon leak into generated chapter prose, if a generated reader paragraph opens with the compact evidence-boundary phrase, if a required reader heading is missing, if a chapter falls below the configured minimum reader-spine word count, or if the generated reader chapter lacks exactly one substantial Handoff after `Summary` that names the next manifest chapter title without numbered chapter references or generic transition formulas. The final generated chapter must close the book-level arc. A normal run writes `build/reader_spine_report.json`, which is ignored by git and is useful during major-version review.

`scripts/validate_reader_evidence_boundaries.py --check` derives the reader manuscript in a temporary workspace and fails if a live source chapter lacks its raw core-claim marker, if a generated reader chapter retains that raw machine marker or repeated support boilerplate, if the generated Core Claim section loses the stripped claim text, if the live marker disagrees with the manifest support state, or if the generated Core Claim section lacks an inline plain-language support-state boundary. A normal run writes `build/reader_evidence_boundaries_report.json`, which is ignored by git and is useful during major-version review.

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

The generated audio workspace includes `audio_manifest.json`, `AUDIO_RELEASE_CHECKLIST.md`, `chapter_markers.md`, `pronunciation_glossary.md`, `proof_equation_reading_rules.md`, and `companion_notes.md`. The manifest records that the script was derived from the reader release path, whether every chapter script preserved both implementation-horizon sections, and that review is still required before any MP3, M4B, or audio-embedded EPUB can be claimed. The companion notes count tables, diagrams, code/schema blocks, and images by script file so the narration review can decide what is spoken, summarized, or moved to companion material. The proof/equation rules keep theorem IDs, equations, support states, schemas, hashes, and negative controls scoped in spoken form. The checklist records table/diagram/code spoken-treatment requirements, packaging checks, and the rule that an audio-embedded EPUB exists only after the reviewed audio files are actually embedded and checked.

The audio manifest carries the same human-consumption bundle policy, but only to enforce dependency direction. Audio is not a shortcut around reader review, and audio embedded in EPUB remains a separate checked artifact.

The tracked audio-script probe manifest records the current local workspace
facts: 49 generated script files, preserved implementation horizons, 8 table
treatment notes, 53 Mermaid diagram notes, 8 image notes, and MP3/M4B/
audio-embedded EPUB targets still marked `target_not_generated`. This keeps
audio preparation visible without approving narration or claiming audio files
exist.

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
