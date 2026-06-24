# Prewriting Readiness

Last updated: 2026-06-24

This file records the repo changes needed before starting a goal to draft the full book.

The recommended launch wording is tracked in `docs/full_book_writing_goal.md`.

## Completed Readiness Work

- Backbone source notes now exist for VIEA, SCF, PlanForge, Talos, VCM, Spinoza, Alignment Field, MoECOT, and connector-resolved variants.
- Authenticated connector reads are recorded in `sources/connector_readiness.json` and reflected in the source readiness report.
- The per-chapter Definition of Done is machine-checked by `scripts/validate_chapter_dod.py`.
- Required backbone source notes are machine-checked by `scripts/validate_source_notes.py`.
- Proof target triage is machine-checked by `scripts/validate_proof_readiness.py`.
- The Lean toolchain is pinned and the implemented evidence-state proofs are wired to the outline/manifest.
- CI is configured to run validation, render Quarto, and build the Lean workspace.
- Stale local handoff trees are quarantined under ignored `_archive/local_context/`.

## Still Missing Before Claims Can Rise Above Argument

- Most chapter claims have not been mapped from source notes into Appendix C.
- Most Lean targets remain planned or triaged as schema/process/research work.
- Codex tests are planned but not implemented or run.
- Source-reported benchmark results from MoECOT, Talos, Road To AGI, or other papers have not been reproduced in this repo.
- External literature has a queue and stance, but not a citation-normalized bibliography.

## Full-Book Drafting Launch Gate

Before starting an autonomous full-book writing goal, run:

```bash
python3 scripts/source_readiness_report.py
python3 scripts/sync_scaffold.py
python3 scripts/sync_proof_manifest.py
python3 scripts/validate_publication.py
python3 scripts/validate_book.py
python3 scripts/validate_schemas.py
(cd lean && lake build)
quarto render --to html
```

The drafting agent should read `docs/book_outline.md`, then source notes for the chapters in scope, then raw source text only when needed. Handoff packets and conversation-mined material remain author-intent and recovery context, not source-derived evidence.
