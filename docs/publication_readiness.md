# Publication Readiness

Last audited: 2026-06-25

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
- The release-edition plan exists at `docs/release_editions_plan.md`, with public appendix coverage in `appendices/I_release_editions.qmd`.
- Audience-specific release profiles and content-layer contracts exist in `editions/release_profiles.json` for the live book, research release, reader release, and audio release.
- `scripts/build_reader_edition.py` can derive a cleaned reader-edition Quarto source tree, `reader_manifest.json`, and `READER_RELEASE_CHECKLIST.md` under ignored `build/`; `scripts/validate_release_profiles.py` validates profile definitions; and `scripts/validate_reader_spine.py` checks that the generated human-reader spine remains substantial after live-only scaffolding is stripped.
- `scripts/render_reader_formats.py` can attempt selected reader-edition HTML/EPUB/DOCX/PDF renders and record actual local outcomes in `reader_render_report.json` without implying publication.
- `scripts/build_audio_script.py` can derive an audio-script review workspace, `audio_manifest.json`, `AUDIO_RELEASE_CHECKLIST.md`, `chapter_markers.md`, and pronunciation glossary under ignored `build/` without claiming audio exists.
- Future major-version research, reader, and audio releases have a dedicated public-safe record schema at `schemas/edition_release_record.schema.json`.
- Every chapter has stable `lean:*` proof targets in the outline.
- `proofs/proof_manifest.json` is generated from the outline.
- Source metadata is tracked without publishing raw source exports.
- Source readiness is tracked in `docs/source_readiness_report.md`.
- Source notes exist for all currently assigned source records, and connector-readiness metadata remains tracked for authenticated source routes.
- Every assigned source/chapter pair is explicitly listed in the corresponding source note, and every core claim now has an exact source-note mapping in Appendix C.
- Appendix C now records exact source-note mappings for all 52 core claims without promoting support states.
- All 52 chapters have v0.2 manuscript drafts generated from the source-of-truth manifest and kept at conservative support states.
- `scripts/draft_v02_from_manifest.py` records the repeatable v0.2 baseline drafting pass.
- Per-chapter DoD, source-note, proof-readiness, and repeated-prose validators are wired into `scripts/validate_book.py`.
- The Lean toolchain is pinned and CI builds the Lean workspace.
- Generated and curated appendices exist for source matrix, claim/evidence matrix, protocol schemas, test specs, changelog, bibliography/source corpus, lineage, and release editions.
- JSON schemas, protocol example fixtures, public release records, and the Lean workspace have local validation commands.
- A public-surface audit has removed stale generated-placeholder language from live chapters and future scaffold defaults.
- GitHub issue templates and PR template exist for source, chapter, evidence, proof/code, and site work.

## Known Blockers Before v1.0 Evidence Release

- Source-derived support still requires passage-level source review, claim-to-mechanism reconciliation, and an accepted evidence transition; exact source-note mapping alone is not a support-state promotion.
- Newly added or previously unassigned sources still require source notes and chapter assignment before they can be used as source-derived support.
- Authenticated connector access succeeded for `vcm_editable`, `moecot`, `coherence_exchange`, `talos_md`, `moecot_md`, `road_to_agi`, and `coilmoecot`, but durable raw cache exports are still local/private and not committed.
- All 104 manifest proof targets now have finite-record Lean implementations and Appendix E publishes the current coverage/accounting breakdown from `proofs/proof_triage.json`; artifact-by-artifact proof audits remain planned and the finite-record modules do not prove broad system behavior.
- Most chapter-level Codex tests are planned, not implemented or run; protocol schema fixture and release-record validation are implemented.
- External literature queue is explicit in `docs/external_literature_queue.md`, including fast generation, decoding substrates, and policy optimization / learning from feedback, but not citation-normalized or source-noted.
- The v0.2 chapters are coherent architecture drafts, but several still need source-specific prose, direct passage review, claim-to-mechanism reconciliation, and hand revision before v1.0 publication quality.
- Reader, research, PDF, EPUB, DOCX, AZW3, MOBI, and audio editions are planned and scaffolded, but no human-reader major-version artifact or audiobook should be reported until the corresponding generated manuscript, render or conversion, review, and release record exist.

## Manuscript Maintenance Checklist

Before claiming the public book is current:

- Run `python3 scripts/sync_scaffold.py`.
- Run `python3 scripts/sync_proof_manifest.py`.
- Run `python3 scripts/validate_publication.py`.
- Run `python3 scripts/validate_release_profiles.py`.
- Run `python3 scripts/build_reader_edition.py --check`.
- Run `python3 scripts/validate_reader_spine.py --check`.
- Run `python3 scripts/render_reader_formats.py --check`.
- Run `python3 scripts/build_audio_script.py --check` when preparing an audio script or checking the full edition path.
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
- Edition profiles validate, the reader-edition derivation check passes, and the reader-spine check passes.
- The working tree is clean after commit and push.
