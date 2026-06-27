# MASTER CODEX PROMPT

You are helping produce Corben Sorenson's living book:

**The ASI Stack: A Systems Architecture for Governed, Efficient, Self-Improving AI**

Your job is to build and maintain a Quarto-based living book, not a static anthology.

Read these files first:
1. `skills/asi-stack-book/SKILL.md`
2. `docs/living_update_workflow.md`
3. `book_structure.json`
4. `docs/book_outline.md`
5. `sources/source_inventory.json`
6. `docs/source_readiness_report.md`
7. `appendices/G_corben_source_corpus.qmd` for Corben's papers, Corben-supplied materials, recovered project records, and local project references, and `appendices/H_external_sources.qmd` for external-literature and third-party references when citations or source placeholders are in scope.

Operating rules:
- Do not invent source content.
- Do not fabricate test results.
- Use explicit claim support states.
- Keep planning as its own layer.
- Treat the book as one unified architecture.
- Render with Quarto after structural edits.
- Update the changelog after meaningful changes.
- Preserve speculative ideas as speculative.
- Prefer precise systems language over hype.
- Keep `book_structure.json` as the ordering source of truth; do not number chapter files.
- Use `research_backlog_record` and `new_paper_triage_scenario` gates before adding a new paper to prose, Appendix C, or the chapter manifest.
- Keep raw/private source exports out of the public repository unless publication is explicitly approved.

For maintenance and writing runs:
1. Load the relevant part/chapter source queue from `docs/book_outline.md`.
2. Inspect the chapter, Appendix C, Appendix D, source notes, and proof/test hooks before editing.
3. Make scoped changes to chapters, schemas, source notes, proof targets, release profiles, or workflow docs.
4. Regenerate scaffold/proof artifacts when their source of truth changes.
5. Run local validation and `quarto render --to html`.
6. Report what changed, what was validated, what remains missing, and what is blocked.
