---
name: asi-stack-book
description: Maintain and write Corben Sorenson's Quarto living book "The ASI Stack" with manifest-driven parts/chapters, source ingestion, claim/evidence discipline, chapter drafting, source-to-chapter triage, changelog updates, and local render validation. Use when Codex is asked to add or reorganize chapters/parts, ingest or triage a new AI paper/source, draft or revise ASI Stack book chapters, update evidence states, maintain the source matrix or claim/evidence matrix, or publish/check the living book.
---

# ASI Stack Book

## Operating Rules

- Treat Quarto as the source of truth and GitHub Pages as a rendered publication target.
- Treat `book_structure.json` as the only ordering source of truth for parts, chapters, chapter IDs, and chapter file paths.
- Do not hand-edit `_quarto.yml`; regenerate it with `python3 scripts/sync_scaffold.py`.
- Do not use numbered chapter filenames. Use stable slug filenames and stable `chapter_id` values.
- Do not fabricate source content, citations, summaries, benchmark results, or test results.
- Keep claim support states explicit: `unsupported`, `argument`, `source-derived`, `prototype-backed`, `synthetic-test-backed`, `empirical-test-backed`, `external-literature-backed`.
- Preserve speculative material as speculative.
- Update `appendices/F_changelog.qmd` for meaningful structural, source, claim, evidence, or publication changes.

## Standard Workflow

1. Read `prompts/MASTER_CODEX_PROMPT.md`, `book_structure.json`, `sources/source_inventory.json`, and `docs/living_update_workflow.md`.
2. Inspect the relevant chapters and appendices before editing.
3. If adding, moving, merging, or deleting parts/chapters, edit `book_structure.json` or use:
   - `python3 scripts/add_part.py --title "..."`
   - `python3 scripts/add_chapter.py --part <part-id> --title "..."`
4. Run `python3 scripts/sync_scaffold.py` after manifest changes.
5. Update chapter prose and source notes only from available source text or clearly labeled design reasoning.
6. Update Appendix C when a claim changes or its support state changes.
7. Run `python3 scripts/validate_book.py`.
8. Render with `quarto render --to html`; for full local output use `LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 quarto render`.

## New Paper Triage

When the user brings a new AI-related paper:

1. Create or update a record in `sources/source_inventory.json` with a stable source ID.
2. Do not place private or restricted source text in the public repo unless the user explicitly approves.
3. If the source text is available, create `sources/source_notes/<source-id>.md` with thesis, mechanisms, evidence, failure modes, supported chapters, and open questions.
4. Decide whether the source updates an existing chapter, needs a new chapter, belongs in an appendix, or should remain unassigned.
5. If it updates a chapter, add the source ID to that chapter's `source_ids` in `book_structure.json`.
6. If it needs a new chapter, add it to the most fitting part with `scripts/add_chapter.py`, then fill its manifest fields.
7. Keep the claim/evidence state at `argument` unless source ingestion or tests justify a stronger state.

Read `references/triage.md` when deciding whether to update an existing chapter or create a new one.

## Drafting Standards

- Write as one architecture, not an anthology.
- Keep planning, memory, reasoning, execution, routing, compression, governance, and evidence as separate layers unless the text is explicitly describing an interface.
- Prefer systems language: boundary, authority, invariant, interface, artifact, evidence state, route, ledger, regression, residual.
- Avoid unscoped safety claims and hype.
- Every chapter should maintain: problem, insufficiency of current approaches, core claim, mechanism, interfaces, invariants, failure modes, minimal implementation, test plan, source crosswalk, and summary.

## Validation

Use these commands before reporting completion:

```bash
python3 scripts/sync_scaffold.py
python3 scripts/validate_book.py
quarto render --to html
```

If PDF output matters, also run:

```bash
LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 quarto render
```
