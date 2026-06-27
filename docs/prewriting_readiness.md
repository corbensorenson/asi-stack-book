# Prewriting Readiness

Last updated: 2026-06-27

This file records the repo changes that made the full-book v0.2 drafting goal safe to start. The launch phase is complete; current v1.0 candidate status is tracked in `docs/v1_0_candidate_status.md`.

The recommended launch wording is tracked in `docs/full_book_writing_goal.md`.

## Completed Readiness Work

- A manuscript baseline now exists across all 54 manifest-driven chapters.
- Backbone source notes now exist for VIEA, SCF, PlanForge, Talos, VCM, Spinoza, Alignment Field, MoECOT, and connector-resolved variants.
- Authenticated connector reads are recorded in `sources/connector_readiness.json` and reflected in the source readiness report.
- The per-chapter Definition of Done is machine-checked by `scripts/validate_chapter_dod.py`.
- Required backbone source notes are machine-checked by `scripts/validate_source_notes.py`.
- Source-note, claim-source mapping, and passage-review queue consistency is machine-checked by `scripts/validate_source_evidence_audit.py`.
- Proof target triage is machine-checked by `scripts/validate_proof_readiness.py`.
- Protocol schema examples are machine-checked by `scripts/validate_protocol_examples.py`.
- Major-version reader and audio edition paths are scaffolded with `scripts/build_reader_edition.py`, `scripts/validate_human_reading_paths.py`, `scripts/validate_reader_spine.py`, `scripts/validate_reading_mode_toggle.py`, `scripts/validate_live_human_view.py`, `scripts/validate_live_human_view_browser.js`, `scripts/build_audio_script.py`, and edition release-record validation.
- The Lean toolchain is pinned and the implemented evidence-state proofs are wired to the outline/manifest.
- CI is configured to run the expanded live-book gate, render Quarto, validate the rendered Human view, and build the Lean workspace.
- Stale local handoff trees are quarantined under ignored `_archive/local_context/`.

## Still Missing Before Claims Can Rise Above Argument

- Chapter claims now have exact source-note mappings and passage-reviewed mapping records for all 461 current claim-source mappings, but support-state promotion still requires claim-to-mechanism reconciliation and accepted evidence transitions.
- Lean targets are implemented as finite-record predicates and traceability-audited, but semantic proof adequacy review remains planned.
- Most chapter-level Codex tests are planned but not implemented or run; protocol schema fixture validation is implemented.
- Source-reported benchmark results from MoECOT, Talos, Road To AGI, or other papers have not been reproduced in this repo.
- External literature has a queue and stance, but not a citation-normalized bibliography.

## Full-Book Maintenance Gate

Before claiming the manuscript is current after a structural or drafting change, run:

```bash
python3 scripts/source_readiness_report.py
python3 scripts/sync_scaffold.py
python3 scripts/sync_proof_manifest.py
python3 scripts/validate_chapter_dod.py
python3 scripts/validate_source_evidence_audit.py
python3 scripts/validate_publication.py
python3 scripts/validate_release_profiles.py
python3 scripts/validate_reading_mode_toggle.py
python3 scripts/build_reader_edition.py --check
python3 scripts/validate_human_reading_paths.py
python3 scripts/validate_source_appendices.py
python3 scripts/validate_v1_status_snapshot.py
python3 scripts/validate_outline_consistency.py
python3 scripts/validate_implementation_horizons.py
python3 scripts/validate_reader_spine.py --check
python3 scripts/render_reader_formats.py --check
python3 scripts/build_audio_script.py --check
python3 scripts/validate_book.py
python3 scripts/validate_visual_coverage.py
python3 scripts/validate_schemas.py
python3 scripts/validate_protocol_examples.py
python3 scripts/validate_repeated_prose.py
(cd lean && lake build)
quarto render --to html
python3 scripts/validate_live_human_view.py
node scripts/validate_live_human_view_browser.js
```

The drafting agent should read `docs/book_outline.md`, then source notes for the chapters in scope, then raw source text only when needed. Handoff packets and conversation-mined material remain author-intent and recovery context, not source-derived evidence.
