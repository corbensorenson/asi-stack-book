# Publication Readiness

Last audited: 2026-06-24

This file tracks whether the public repository is ready for the next major phase: drafting the full book from the outline.

## Ready

- Public GitHub repository exists: <https://github.com/corbensorenson/asi-stack-book>
- Public GitHub Pages site exists: <https://corbensorenson.github.io/asi-stack-book/>
- Quarto renders the book to HTML.
- The book order is manifest-driven by `book_structure.json`.
- The cohesive outline exists at `docs/book_outline.md`.
- The source-mining synthesis exists at `docs/source_mining_synthesis.md`.
- The Project Theseus and Circle Calculus mining report exists at `docs/local_project_mining_theseus_circle.md`.
- Every chapter has stable `lean:*` proof targets in the outline.
- `proofs/proof_manifest.json` is generated from the outline.
- Source metadata is tracked without publishing raw source exports.
- Source readiness is tracked in `docs/source_readiness_report.md`.
- Backbone source notes and connector-readiness metadata exist for the main pre-drafting sources.
- Per-chapter DoD, source-note, and proof-readiness validators are wired into `scripts/validate_book.py`.
- The Lean toolchain is pinned and CI builds the Lean workspace.
- Generated appendices exist for source matrix, claim/evidence matrix, protocol schemas, test specs, changelog, and bibliography/source corpus.
- JSON schemas and Lean workspace both have local validation commands.
- GitHub issue templates and PR template exist for source, chapter, evidence, proof/code, and site work.

## Known Blockers Before Full Draft Completion

- Chapters are currently guarded stubs, not manuscript chapters.
- Source-derived claims require source notes before support-state promotion.
- Project Theseus, Circle Calculus, and Field of God AI Constitution source records still need source notes before being used as source-derived support.
- Authenticated connector access succeeded for `vcm_editable`, `moecot`, `coherence_exchange`, `talos_md`, `moecot_md`, `road_to_agi`, and `coilmoecot`, but durable raw cache exports are still local/private and not committed.
- Most Lean proof targets are planned or triaged as schema/process/research targets, not implemented.
- Codex tests are planned, not implemented or run.
- External literature queue is explicit in `docs/external_literature_queue.md`, but not citation-normalized.

## Pre-Drafting Checklist

Before starting a goal to write the whole book:

- Run `python3 scripts/sync_scaffold.py`.
- Run `python3 scripts/sync_proof_manifest.py`.
- Run `python3 scripts/validate_publication.py`.
- Run `python3 scripts/validate_book.py`.
- Run `python3 scripts/validate_schemas.py`.
- Run `(cd lean && lake build)`.
- Run `quarto render --to html`.
- Confirm no raw source exports are staged.

## Definition of Presentable Public State

The public repository is presentable when:

- README explains the project, status, source discipline, proof discipline, and validation path.
- Contributor and rights files are present.
- GitHub metadata points to the live site.
- GitHub Pages workflow passes.
- Rendered site links are live.
- Validation scripts pass locally.
- The working tree is clean after commit and push.
