# Publication Readiness

Last audited: 2026-06-24

This file tracks whether the public repository is ready for the next major phase: source-substantiating, testing, and improving the v0.2 manuscript draft.

## Ready

- Public GitHub repository exists: <https://github.com/corbensorenson/asi-stack-book>
- Public GitHub Pages site exists: <https://corbensorenson.github.io/asi-stack-book/>
- Quarto renders the book to HTML.
- The book order is manifest-driven by `book_structure.json`.
- The cohesive outline exists at `docs/book_outline.md`.
- The source-mining synthesis exists at `docs/source_mining_synthesis.md`.
- The Project Theseus and Circle Calculus mining report exists at `docs/local_project_mining_theseus_circle.md`.
- The fast-generation context ingestion report exists at `docs/fast_generation_context_ingestion_report.md`.
- The policy-optimization context ingestion report exists at `docs/policy_optimization_context_ingestion_report.md`.
- Every chapter has stable `lean:*` proof targets in the outline.
- `proofs/proof_manifest.json` is generated from the outline.
- Source metadata is tracked without publishing raw source exports.
- Source readiness is tracked in `docs/source_readiness_report.md`.
- Source notes exist for all currently assigned source records, and connector-readiness metadata remains tracked for authenticated source routes.
- All 52 chapters have v0.2 manuscript drafts generated from the source-of-truth manifest and kept at conservative support states.
- `scripts/draft_v02_from_manifest.py` records the repeatable v0.2 baseline drafting pass.
- Per-chapter DoD, source-note, proof-readiness, and repeated-prose validators are wired into `scripts/validate_book.py`.
- The Lean toolchain is pinned and CI builds the Lean workspace.
- Generated appendices exist for source matrix, claim/evidence matrix, protocol schemas, test specs, changelog, and bibliography/source corpus.
- JSON schemas, protocol example fixtures, public release records, and the Lean workspace have local validation commands.
- A public-surface audit has removed stale generated-placeholder language from live chapters and future scaffold defaults.
- GitHub issue templates and PR template exist for source, chapter, evidence, proof/code, and site work.

## Known Blockers Before v1.0 Evidence Release

- Source-derived claims require claim-level mapping from source notes before support-state promotion.
- Newly added or previously unassigned sources still require source notes before they can be used as source-derived support.
- Authenticated connector access succeeded for `vcm_editable`, `moecot`, `coherence_exchange`, `talos_md`, `moecot_md`, `road_to_agi`, and `coilmoecot`, but durable raw cache exports are still local/private and not committed.
- Most Lean proof targets now have finite-record implementations; Appendix E publishes the current coverage/accounting breakdown from `proofs/proof_triage.json`, with the remaining planned targets kept as research agenda items.
- Most chapter-level Codex tests are planned, not implemented or run; protocol schema fixture and release-record validation are implemented.
- External literature queue is explicit in `docs/external_literature_queue.md`, including fast generation, decoding substrates, and policy optimization / learning from feedback, but not citation-normalized.
- The v0.2 chapters are coherent architecture drafts, but most still need source-specific prose, claim-to-source mapping, and hand revision before v1.0 publication quality.

## Manuscript Maintenance Checklist

Before claiming the public book is current:

- Run `python3 scripts/sync_scaffold.py`.
- Run `python3 scripts/sync_proof_manifest.py`.
- Run `python3 scripts/validate_publication.py`.
- Run `python3 scripts/validate_book.py`.
- Run `python3 scripts/validate_visual_coverage.py`.
- Run `python3 scripts/validate_schemas.py`.
- Run `python3 scripts/validate_protocol_examples.py`.
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
