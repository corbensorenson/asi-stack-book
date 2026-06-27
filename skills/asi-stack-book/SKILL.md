---
name: asi-stack-book
description: Maintain and write Corben Sorenson's Quarto living book "The ASI Stack" with manifest-driven parts/chapters, source ingestion, claim/evidence discipline, chapter drafting, source-to-chapter triage, changelog updates, and local render validation. Use when Codex is asked to add or reorganize chapters/parts, ingest or triage a new AI paper/source, draft or revise ASI Stack book chapters, update evidence states, maintain the source matrix or claim/evidence matrix, or publish/check the living book.
---

# ASI Stack Book

## Operating Rules

- Treat Quarto as the source of truth and GitHub Pages as a rendered publication target.
- Treat `book_structure.json` as the only ordering source of truth for parts, chapters, chapter IDs, and chapter file paths.
- Treat `docs/book_outline.md` as the drafting source of truth for chapter jobs, part-level and chapter-level source loading queues, and Lean proof targets.
- Do not hand-edit `_quarto.yml`; regenerate it with `python3 scripts/sync_scaffold.py`.
- Do not use numbered chapter filenames. Use stable slug filenames and stable `chapter_id` values.
- Do not fabricate source content, citations, summaries, benchmark results, or test results.
- Keep claim labels and support states separate. Claim labels: `Demonstrated`, `Measured`, `Mechanized`, `Hypothesized`, `Design rationale`, `Speculative`. Support states: `unsupported`, `argument`, `source-derived`, `prototype-backed`, `synthetic-test-backed`, `empirical-test-backed`, `external-literature-backed`, `deprecated`, `refuted`.
- Treat handoff packets and conversation-mined packets as planning, author-intent, lineage, terminology, and recovery context only. Do not use them as external evidence or quote private conversational wording without explicit approval.
- Preserve speculative material as speculative.
- Update `appendices/F_changelog.qmd` for meaningful structural, source, claim, evidence, or publication changes.

## Standard Workflow

1. Read `prompts/MASTER_CODEX_PROMPT.md`, `book_structure.json`, `docs/book_outline.md`, `sources/source_inventory.json`, and `docs/living_update_workflow.md`.
2. Read `docs/source_readiness_report.md` if source ingestion or drafting depends on source availability.
3. Read `appendices/G_corben_source_corpus.qmd` when drafting from Corben-authored, Corben-supplied, or local project records; read `appendices/H_external_sources.qmd` when drafting external-literature or third-party citation context by other authors.
4. Use the source loading queues in `docs/book_outline.md` to decide which primary, supporting, variant, connector, or recovery sources are in scope.
5. Inspect the relevant chapters and appendices before editing.
6. If adding, moving, merging, or deleting parts/chapters, edit `book_structure.json` or use:
   - `python3 scripts/add_part.py --title "..."`
   - `python3 scripts/add_chapter.py --part <part-id> --title "..."`
7. Run `python3 scripts/sync_scaffold.py` after manifest changes.
8. Run `python3 scripts/sync_proof_manifest.py` after outline proof-tag changes.
9. Update chapter prose and source notes only from available source text, clearly labeled design reasoning, or clearly labeled author-intent context.
10. Update Appendix C when a claim changes, its claim label changes, or its support state changes.
11. Run `python3 scripts/validate_publication.py` for public-surface changes.
12. Run `python3 scripts/validate_release_profiles.py` and `python3 scripts/validate_reader_spine.py --check` after edition/profile/reader-spine changes.
13. Run `python3 scripts/validate_book.py`.
14. Run `python3 scripts/validate_visual_coverage.py` after visual, chapter, or site changes.
15. Run schema and fixture validators when protocol artifacts change: `python3 scripts/validate_schemas.py` and `python3 scripts/validate_protocol_examples.py`.
16. Render with `quarto render --to html`; for full local output use `LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 quarto render`.

## New Paper Triage

When the user brings a new AI-related paper:

1. Decide source storage and public-safety policy before adding text: public source, public note only, connector only, local private cache, external URL only, or blocked.
2. Create or update a record in `sources/source_inventory.json` with a stable source ID.
3. Do not place private or restricted source text in the public repo unless the user explicitly approves.
4. Use `python3 scripts/cache_drive_sources.py` and `python3 scripts/source_readiness_report.py` to refresh local cache status when appropriate.
5. If the source text is available and permitted, create `sources/source_notes/<source-id>.md` with thesis, mechanisms, evidence, failure modes, supported chapters, and open questions.
6. Use the Research Backlog Record and New Paper Triage Scenario surfaces to decide whether the source updates an existing chapter, proposes a precise new chapter, belongs in an appendix/backlog, should be deferred until read, or should be rejected as duplicate/out of scope.
7. Record deduplication state, chapter-decision refs, merge/split policy, required pre-drafting work, evidence-transition preconditions, promotion blockers, and non-claims before strengthening prose.
8. If it updates a chapter, add the source ID to that chapter's `source_ids` in `book_structure.json`.
9. If it needs a new chapter, add it to the most fitting part with `scripts/add_chapter.py`, then fill its manifest fields.
10. Keep support state at `argument` unless source ingestion, passage review, accepted evidence transition, proof, or tests justify a stronger state.

Read `references/triage.md` when deciding whether to update an existing chapter or create a new one.

## Drafting Standards

- Write as one architecture, not an anthology.
- Keep planning, memory, reasoning, execution, routing, compression, governance, and evidence as separate layers unless the text is explicitly describing an interface.
- Prefer systems language: boundary, authority, invariant, interface, artifact, evidence state, route, ledger, regression, residual.
- Avoid unscoped safety claims and hype.
- Treat `docs/book_outline.md` as the source of truth for full-book drafting and Lean proof scope.
- Follow the outline's source queues before drafting: primary sources first, supporting sources second, variants for version comparison, connector/recovery sources as explicit blockers until loaded.
- Use conversation-derived context to preserve architecture intent and deduplicate concepts, but keep it out of source-derived support unless the corresponding source text is actually loaded.
- Keep `proofs/proof_manifest.json` generated from outline `lean:*` proof tags.
- Every chapter should maintain: problem, insufficiency of current approaches, core claim, mechanism, interfaces, invariants, failure modes, minimum viable implementation, beyond-state-of-the-art end state, test plan, source crosswalk, and summary.
- `Minimum Viable Implementation` should name the smallest honest artifact or validated slice that can start the idea without overstating it; `Beyond the State of the Art` should name the mature product-level logical conclusion of the idea without implying that the end state has already been implemented or validated.
- Treat Appendix K, `Implementation Horizons`, as the generated book-wide view of the manifest's first-build and mature-endpoint fields.
- Every chapter should contain at least one Mermaid diagram that explains an interface, lifecycle, evidence flow, state transition, or boundary. Keep diagrams technical and do not use them to imply unrecorded proof, benchmark, or implementation status.

## Validation

Use these commands before reporting completion:

```bash
python3 scripts/sync_scaffold.py
python3 scripts/sync_proof_manifest.py
python3 scripts/validate_publication.py
python3 scripts/validate_release_profiles.py
python3 scripts/validate_reader_spine.py --check
python3 scripts/validate_book.py
python3 scripts/validate_visual_coverage.py
python3 scripts/validate_schemas.py
python3 scripts/validate_protocol_examples.py
(cd lean && lake build)
quarto render --to html
```

The book is HTML-first by default. Do not report a PDF artifact unless PDF output has been explicitly configured and rendered. If PDF output matters, add or verify a `pdf` format in `_quarto.yml` through the scaffold generator before running:

```bash
LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 quarto render
```
