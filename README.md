# The ASI Stack

**The ASI Stack: A Systems Architecture for Governed, Efficient, Self-Improving AI** is Corben Sorenson's living technical book about AI systems architecture.

Public book site: <https://corbensorenson.github.io/asi-stack-book/>

Public repository: <https://github.com/corbensorenson/asi-stack-book>

This repository is the canonical Quarto source for the book, its scaffolding, validation scripts, schemas, Lean proof workspace, and public-safe source/evidence metadata. The book treats the source papers as fragments of one architecture: alignment, governance, planning, memory, reasoning, execution, routing, compression, evidence, and recursive self-improvement.

## Current Status

The project has moved beyond the initial v0.2 manuscript baseline into an extended v1.0 candidate hardening pass, but it is not yet a final v1.0 evidence release.

- Quarto book structure is initialized and renders to HTML.
- All 54 outline chapters exist as manuscript drafts across four manifest-driven parts.
- `docs/book_outline.md` is the source of truth for the full-book drafting plan, per-part/per-chapter source queues, and Lean proof scope.
- `book_structure.json` controls parts, chapter order, stable chapter IDs, and appendix order, including curated lineage appendices.
- `_quarto.yml`, Appendix A, Appendix C, and Appendix G are generated.
- `editions/release_profiles.json` defines live, research, reader, and audio release profiles plus content layers for the reader spine, live research scaffold, evidence matrices, machine contracts, release derivatives, and audio adaptation.
- `scripts/build_reader_edition.py` can derive a cleaned reader-edition Quarto source tree and `reader_manifest.json` under ignored `build/`.
- `scripts/validate_reader_spine.py` checks that every generated reader chapter keeps a substantial human-readable spine, required chapter sections, and no live-only scaffolding after stripping.
- `scripts/render_reader_formats.py` can attempt reader-edition HTML/EPUB/DOCX/PDF renders and write a local `reader_render_report.json` with actual outcomes.
- `scripts/build_reader_edition.py` and `scripts/build_audio_script.py` now emit generated review checklists and companion notes so major-version reader, e-reader, and audio work stay downstream of the living book instead of becoming parallel manuscripts.
- `scripts/build_audio_script.py` can derive an audio-script review workspace, `audio_manifest.json`, chapter markers, an audio checklist, and pronunciation glossary under ignored `build/`.
- The live GitHub Pages site includes a top-of-page reading-mode switch: `AI view` keeps the full live/research scaffold, while `Human view` hides the same repeated chapter sections used by the reader-release strip policy. Optional `.asi-human-only` and `.asi-ai-only` fenced blocks let future chapters carry mode-specific prose without forking the manuscript.
- `proofs/proof_manifest.json` is generated from `lean:*` proof tags in the outline.
- `proofs/proof_triage.json` classifies proof targets as Lean, schema, process, or research-agenda work.
- Source notes exist for all currently assigned source records, and connector-readiness metadata remains tracked for source routes that depend on authenticated exports.
- Source documents are cached locally when available, but raw exports are ignored and not published.
- Current source-note coverage, exact claim-source mappings, and passage-reviewed mappings are complete for assigned source/chapter pairs, but all chapter core claims remain at `argument` support until accepted evidence transitions justify promotion.
- A protocol schema fixture check is implemented; broader chapter-level Codex tests remain planned unless a specific test result is recorded.
- `scripts/draft_v02_from_manifest.py` records the repeatable baseline drafting pass; use it intentionally because it rewrites chapter files from the manifest.

## Start Here

| File or page | Purpose |
|---|---|
| [Live book](https://corbensorenson.github.io/asi-stack-book/) | Rendered public site. |
| [docs/book_outline.md](docs/book_outline.md) | Cohesive full-book outline and proof target source of truth. |
| [docs/prewriting_readiness.md](docs/prewriting_readiness.md) | Launch gate for a full-book drafting goal. |
| [docs/full_book_writing_goal.md](docs/full_book_writing_goal.md) | Suggested wording for the full-book writing goal. |
| [docs/v1_0_candidate_status.md](docs/v1_0_candidate_status.md) | Current v1.0 candidate snapshot, remaining evidence gaps, and release gate. |
| [docs/v02_manuscript_status.md](docs/v02_manuscript_status.md) | Historical v0.2 manuscript completion, gaps, and validation status. |
| [docs/external_literature_queue.md](docs/external_literature_queue.md) | Explicit stance and queue for third-party literature. |
| [docs/release_editions_plan.md](docs/release_editions_plan.md) | Major-version EPUB/PDF/DOCX/audio edition plan and gates. |
| [docs/major_version_release_runbook.md](docs/major_version_release_runbook.md) | Operational ladder for tagged live, reader, e-reader/document, and audio releases. |
| [docs/local_project_mining_theseus_circle.md](docs/local_project_mining_theseus_circle.md) | Public-safe mining report for Project Theseus and Circle Calculus. |
| [book_structure.json](book_structure.json) | Manifest for dynamic parts, chapters, source assignments, and appendices. |
| [editions/release_profiles.json](editions/release_profiles.json) | Audience-specific release profile definitions. |
| [appendices/A_source_matrix.qmd](appendices/A_source_matrix.qmd) | Generated source-to-chapter matrix. |
| [appendices/C_claim_evidence_matrix.qmd](appendices/C_claim_evidence_matrix.qmd) | Generated claim/evidence matrix. |
| [appendices/G_bibliography.qmd](appendices/G_bibliography.qmd) | Generated bibliography and source-corpus appendix. |
| [appendices/H_author_intent_and_lineage.qmd](appendices/H_author_intent_and_lineage.qmd) | Public-safe author-intent and architecture-lineage appendix. |
| [appendices/I_release_editions.qmd](appendices/I_release_editions.qmd) | Live-book explanation of reader, research, and audio edition paths. |
| [proofs/proof_manifest.json](proofs/proof_manifest.json) | Generated Lean proof target manifest. |
| [docs/repository_map.md](docs/repository_map.md) | Repository layout and ownership map. |
| [docs/publication_readiness.md](docs/publication_readiness.md) | Public-readiness checklist and known blockers. |

## Local Validation

Run this before committing structural, source, proof, or publication changes:

```bash
python3 scripts/sync_scaffold.py
python3 scripts/sync_proof_manifest.py
python3 scripts/source_readiness_report.py
python3 scripts/validate_publication.py
python3 scripts/validate_release_profiles.py
python3 scripts/validate_reader_spine.py --check
python3 scripts/validate_book.py
python3 scripts/validate_visual_coverage.py
python3 scripts/validate_reading_mode_toggle.py
python3 scripts/validate_schemas.py
python3 scripts/validate_protocol_examples.py
quarto render --to html
python3 scripts/validate_live_human_view.py
```

For Lean proof work:

```bash
cd lean
lake build
```

The rendered HTML is written to `_site/`, which is ignored by git.

## Release Editions

The live book is optimized for AIs and human researchers. Major versions can also produce cleaned human-reader editions and audio editions from the same source.

The project uses one canonical source tree with explicit content layers:

- The reader-facing chapter spine is ordinary prose, diagrams, examples, uncertainty, and summaries that should still read well after live-only headings are removed.
- The live research scaffold contains source crosswalks, guardrails, Codex tests, formalization hooks, claim mappings, and other audit machinery for AIs and researchers.
- The live Human view uses the same reader-strip policy on the GitHub Pages site, while future `.asi-human-only` blocks are retained for reader editions and `.asi-ai-only` blocks are removed from them.
- Companion material records how diagrams, tables, code, schemas, and omitted dense matrices should be handled for e-reader, document, and audio releases.
- Release derivatives such as EPUB, PDF, DOCX, MP3, M4B, and audio-embedded EPUB exist only after generation or render, review, and release-record entry.

For major versions, use [docs/major_version_release_runbook.md](docs/major_version_release_runbook.md) as the operating sequence: tag the live book, validate the live/research surface, generate and review the reader manuscript, render only the formats that pass locally, then derive audio from the reviewed reader script.

Tracked release profile source:

```bash
python3 scripts/validate_release_profiles.py
```

Generate or check a local reader-edition Quarto source tree:

```bash
python3 scripts/build_reader_edition.py --check
python3 scripts/validate_reader_spine.py --check
python3 scripts/build_reader_edition.py
```

Render selected reader-edition formats and record actual local outcomes:

```bash
python3 scripts/render_reader_formats.py --check
python3 scripts/render_reader_formats.py --formats html epub docx
python3 scripts/render_reader_formats.py --formats html epub docx pdf
```

Generate or check a narration-script candidate after the reader manuscript is ready for review:

```bash
python3 scripts/build_audio_script.py --check
python3 scripts/build_audio_script.py
```

Generated edition builds are written under `build/` and ignored by git. Reader builds include `READER_RELEASE_CHECKLIST.md` and `companion_notes.md`; audio builds include `AUDIO_RELEASE_CHECKLIST.md`, `companion_notes.md`, `chapter_markers.md`, and `pronunciation_glossary.md`. Do not claim EPUB, PDF, DOCX, AZW3, MOBI, MP3, M4B, or audio-embedded EPUB artifacts unless those specific render, conversion, or audio-generation commands have actually succeeded and a release record says so.

## Dynamic Book Structure

Do not hand-edit `_quarto.yml` or use numbered chapter filenames. Edit `book_structure.json`, then run:

```bash
python3 scripts/sync_scaffold.py
```

Useful helpers:

```bash
python3 scripts/add_part.py --title "Part IV - New Research Track"
python3 scripts/add_chapter.py --part planning-memory-reasoning-execution --title "New AI Topic" --after planning-as-a-control-layer
```

Quarto generates displayed chapter numbers at render time, so chapters can be inserted, moved, merged, or removed without renumbering files.

## Manuscript Regeneration

The v0.2 baseline can be regenerated from `book_structure.json`:

```bash
python3 scripts/draft_v02_from_manifest.py
```

This is a bulk rewrite tool. Use it for intentional full-baseline regeneration, not for routine chapter editing after hand-written source-specific prose has been added.

## Source Discipline

Raw source exports are private/local and ignored by git.

```bash
python3 scripts/cache_drive_sources.py
python3 scripts/source_readiness_report.py
```

The tracked readiness report is `docs/source_readiness_report.md`. Raw exports stay under `sources/raw/`.

When adding a new AI paper or artifact, use [docs/living_update_workflow.md](docs/living_update_workflow.md) and the repo skill triage reference before editing prose. New sources need storage/public-safety policy, deduplication state, chapter-decision refs, required pre-drafting work, and promotion blockers. `schemas/research_backlog_record.schema.json` records durable backlog items, and `schemas/new_paper_triage_scenario.schema.json` validates synthetic update/add/defer/reject decision shape only.

Claims use both a claim label and a support state. Do not mark a claim as `source-derived`, `prototype-backed`, `synthetic-test-backed`, `empirical-test-backed`, or `external-literature-backed` unless the source ingestion, prototype review, proof check, or test execution actually happened and is recorded. Conversation-mined material can guide author intent and lineage, but it is not external evidence.

## Proof Discipline

`docs/book_outline.md` is the source of truth for Lean proof scope. Every chapter has `lean:*` proof tags under `Lean proof targets`, plus source queues that tell future writing runs what to load first.

Generate the machine-readable proof manifest from the outline:

```bash
python3 scripts/sync_proof_manifest.py
python3 scripts/validate_proof_readiness.py
```

Do not report a theorem as proven unless the corresponding Lean module exists, the module is imported by the Lean package root, the target is marked implemented in the outline, and `lake build` passes. Use `proofs/proof_triage.json` to keep schema/process/research targets from becoming ceremonial Lean; `scripts/validate_proof_readiness.py` checks that triage tags, modules, root imports, formal targets, and target statuses stay aligned with the generated manifest.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). The short version:

- Preserve the manifest-driven structure.
- Keep speculative claims labeled.
- Do not publish private raw sources.
- Do not fabricate source content, citations, proofs, benchmark results, or test results.
- Run validation and render locally before proposing changes.

## Rights

See [LICENSE.md](LICENSE.md). This public repository is available for reading and review, but no reuse license is granted unless Corben Sorenson provides one separately.
