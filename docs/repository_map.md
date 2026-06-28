# Repository Map

This repository is organized around the living book and its validation loop.

| Path | Role | Public status |
|---|---|---|
| `book_structure.json` | Source of truth for parts, chapters, stable IDs, source assignments, and appendices. | tracked |
| `_quarto.yml` | Generated Quarto configuration. | tracked; do not hand-edit |
| `index.qmd`, `preface.qmd` | Front matter for the rendered book. | tracked |
| `chapters/` | Chapter source files. | tracked |
| `appendices/` | Generated and curated appendices: source matrix, glossary, claims, schemas, tests, changelog, Corben's own sources/papers/local projects, external sources by other authors, author-intent lineage, release editions, and implementation horizons. | tracked |
| `docs/book_outline.md` | Full-book drafting outline, source loading queues, and Lean proof target source of truth. | tracked |
| `docs/v1_0_candidate_status.md` | Current v1.0 candidate snapshot, remaining evidence gaps, and release gate. | tracked |
| `docs/v1_0_focus_audit.md` | Detailed current-state audit and prioritized focus plan for evidence-release, reader-release, proof adequacy, testing, source, and site work. | tracked |
| `docs/v1_0_roadmap.md` | Roadmap and recommended next long-running goal for v1.0 completion work, reconciling current audit findings with external review input. | tracked |
| `docs/reader_manuscript_review.md` | Phase 2 baseline for the generated reader manuscript, including generated-reader metrics, spot-review notes, residuals, and non-claims. | tracked |
| `docs/reader_overlay_pilot.md` | First active Phase 2 semantic reader-overlay pilot for opening-chapter Human-view and generated-reader prose. | tracked |
| `docs/evidence_transition_pilot.md` | Phase 3 evidence-transition pilot summary, recording four no-change support-state decisions and their blockers. | tracked |
| `docs/proof_adequacy_review.md` | Phase 4 proof adequacy review classifying all 112 Lean targets by what they do and do not justify. | tracked |
| `docs/support_state_transition_harness.md` | Phase 5 support-state transition harness summary, command, local result, and non-claim boundary. | tracked |
| `docs/authority_transition_harness.md` | Phase 5 authority transition harness summary, command, local result, and non-claim boundary. | tracked |
| `docs/plan_execution_contract_harness.md` | Phase 5 plan-execution contract harness summary, command, local result, and non-claim boundary. | tracked |
| `docs/context_admission_adequacy_harness.md` | Phase 5 context admission/adequacy harness summary, command, local result, and non-claim boundary. | tracked |
| `docs/external_literature_backfill_phase6.md` | Phase 6 initial external-literature backfill report for alignment/control and governance/evaluation records. | tracked |
| `docs/site_visual_phase7_review.md` | Phase 7 rendered-site, visual coverage, appendix table, landing-page trust, and local-hygiene review. | tracked |
| `docs/v1_0_release_preparation_review.md` | Phase 8 preparation review for reader, ebook/document/PDF, and audio release gates and blockers. | tracked |
| `docs/source_mining_synthesis.md` | Source-mining coverage, architecture cluster map, split rationale, and remaining source gaps. | tracked |
| `docs/local_project_mining_theseus_circle.md` | Public-safe local mining report for Project Theseus and Circle Calculus. | tracked |
| `docs/conversation_context_ingestion_report.md` | Public-safe synthesis of conversation-mined author intent and recovery tasks. | tracked |
| `docs/fast_generation_context_ingestion_report.md` | Public-safe synthesis of the fast-generation browser-GPT planning note and evidence boundaries. | tracked |
| `docs/release_editions_plan.md` | Major-version reader/research/audio release plan, strip rules, and artifact gates. | tracked |
| `docs/major_version_release_runbook.md` | Operational ladder for tagged live, research, reader, ebook/document, and audio releases. | tracked |
| `docs/` | Runbooks, quality standards, readiness reports, and publication guidance. | tracked |
| `editions/release_profiles.json` | Machine-readable audience, content-layer, and release-profile definitions for live, research, reader, and audio editions. | tracked |
| `editions/reader_overlays/` | Versioned semantic reader-edition overlays and examples; editable source for major human-reader deltas. | tracked |
| `assets/reader-overlays.html` | Generated embedded reader-overlay payload for live Human view. | tracked; regenerate from overlays |
| `sources/source_inventory.json` | Public-safe source metadata inventory. | tracked |
| `sources/cache/cache_manifest.json` | Public-safe cache metadata and hashes. | tracked |
| `sources/raw/` | Local raw source exports. | ignored |
| `sources/inbox/` | Local source drop area, including private or conversation-mined packets before public-safe synthesis. | ignored except README |
| `sources/source_notes/` | Public-safe notes created after source text is actually read. | tracked when notes are added |
| `proofs/` | Proof plans and generated proof target manifest. | tracked |
| `lean/` | Lean 4 proof workspace. | tracked except `.lake/` |
| `schemas/` | JSON Schemas for protocol records. | tracked |
| `release_records/` | Public-safe live-book and future major-version edition release records checked against release-record schemas. | tracked |
| `evidence_transitions/` | Evidence-transition review records checked against `schemas/evidence_transition_record.schema.json`. | tracked |
| `experiments/` | Synthetic experiment and benchmark harness workspace, including support-state transition fixtures and result records. | tracked |
| `scripts/` | Manifest sync, source cache, proof manifest, and validation tools. | tracked |
| `build/` | Generated reader/release edition source, reader/audio manifests, and output trees. | ignored |
| `skills/asi-stack-book/` | Project-specific Codex skill for maintaining and drafting the book. | tracked |
| `.github/` | GitHub Pages workflow, issue templates, and PR template. | tracked |
| `_site/`, `.quarto/`, `site_libs/` | Render/build outputs and Quarto cache. | ignored |

## Ownership Rules

- Edit `book_structure.json`, then run `python3 scripts/sync_scaffold.py`.
- Use `python3 scripts/chapter_adjacency_report.py` after adding, moving, merging, or removing chapters to identify the small set of Handoff sections whose manifest-order prose must be repaired.
- Edit `docs/book_outline.md`, then run `python3 scripts/sync_proof_manifest.py`.
- Edit public source metadata in `sources/source_inventory.json`; keep raw source text out of git unless publication is explicitly approved.
- Update `appendices/F_changelog.qmd` for meaningful changes.
- Edit `editions/release_profiles.json` for edition policy, then run `python3 scripts/validate_release_profiles.py`, `python3 scripts/sync_reader_overlay_asset.py --check`, `python3 scripts/validate_reading_mode_toggle.py`, `python3 scripts/validate_human_reading_paths.py`, `python3 scripts/build_reader_edition.py --check`, `python3 scripts/validate_reader_overlays.py --check`, `python3 scripts/validate_reader_evidence_boundaries.py --check`, `python3 scripts/validate_reader_spine.py --check`, `python3 scripts/render_reader_formats.py --check`, and `python3 scripts/build_audio_script.py --check` when the audio path is affected.

## Public Readiness Invariants

- No raw source exports are tracked.
- No rendered `_site/` output is tracked.
- No `.quarto/` cache is tracked.
- No Lean `.lake/` build output is tracked.
- No claim support state is promoted without a recorded basis.
- No proof or test result is reported unless the command was run and the result is recorded.
- No EPUB, PDF, DOCX, or audio artifact is reported unless that specific artifact was rendered or generated and recorded.
- Conversation-mined context is treated as author intent and lineage, not as external evidence or quotable source text.
