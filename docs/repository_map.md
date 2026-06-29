# Repository Map

This repository is organized around the living book and its validation loop.

| Path | Role | Public status |
|---|---|---|
| `book_structure.json` | Source of truth for parts, chapters, stable IDs, source assignments, implementation horizons, support states, proof targets, and appendices. | tracked; schema-validated |
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
| `docs/reader_continuity_audit.md` | Generated Phase 2 heuristic audit and priority queue for reader-manuscript continuity review. | tracked |
| `docs/reader_chapter_review_matrix.md` | Generated public summary of the manifest-synced 54-chapter human-reader review queue, overlay dispositions, and release blockers. | tracked |
| `docs/reader_format_review_matrix.md` | Generated public summary of the v1.0 reader-format review ledger, local render/inspection evidence, and artifact-release blockers. | tracked |
| `docs/reader_artifact_inspection_manifest.md` | Tracked local HTML/EPUB/DOCX structural-inspection summary for ignored reader-format snapshots, preserving release blockers and non-claims. | tracked |
| `docs/reader_epub_probe_manifest.md` | Tracked local EPUB metadata/source-spine probe summary for the ignored reader snapshot, including exact EPUB metrics, sampled source-card entries, and e-reader-specific release blockers. | tracked |
| `docs/reader_docx_probe_manifest.md` | Tracked local DOCX LibreOffice conversion probe summary for the ignored reader snapshot, including exact conversion metrics, sampled source-card pages, and DOCX-specific release blockers. | tracked |
| `docs/reader_pdf_probe_manifest.md` | Tracked local UTF-8 PDF probe summary for the ignored reader snapshot, including exact PDF metrics, sampled source-card pages, and PDF-specific release blockers. | tracked |
| `docs/reader_companion_note_routing_review.md` | Human-readable companion-note routing decision for the dense proof/governance chapters flagged by the reader matrix. | tracked |
| `docs/reader_part_i_review_pass.md` | First Part I generated-reader review pass over matrix rows, recording no-action decisions without release approval. | tracked |
| `docs/reader_part_ii_review_pass.md` | First Part II generated-reader review pass over matrix rows, recording canonical prose cleanups and no-action decisions without release approval. | tracked |
| `docs/reader_part_iii_review_pass.md` | First Part III generated-reader review pass over matrix rows, recording canonical prose cleanups and no-action decisions without release approval. | tracked |
| `docs/reader_part_iv_review_pass.md` | First Part IV generated-reader review pass over matrix rows, recording reader-generator cleanup and no-action decisions without release approval. | tracked |
| `docs/reader_format_dry_run.md` | Local Phase 8 HTML/EPUB/DOCX reader-format dry-run summary, PDF probe, artifact snapshot paths, review status, and non-release boundary. | tracked |
| `docs/reader_artifact_layout_review.md` | Representative local EPUB/DOCX/PDF/HTML spot-check notes for ignored reader-format snapshots, with residuals before any release artifact can be approved. | tracked |
| `docs/evidence_transition_pilot.md` | Phase 3 evidence-transition pilot summary, recording fifteen no-change support-state decisions and their blockers. | tracked |
| `docs/proof_adequacy_review.md` | Phase 4 proof adequacy review classifying all 112 Lean targets by what they do and do not justify. | tracked |
| `docs/claim_ledger_revision_harness.md` | Phase 5 claim-ledger revision harness summary, command, local result, and non-claim boundary. | tracked |
| `docs/proof_carrying_claim_harness.md` | Phase 5 proof-carrying claim harness summary, command, local result, and non-claim boundary. | tracked |
| `docs/support_state_transition_harness.md` | Phase 5 support-state transition harness summary, command, local result, and non-claim boundary. | tracked |
| `docs/authority_transition_harness.md` | Phase 5 authority transition harness summary, command, local result, and non-claim boundary. | tracked |
| `docs/plan_execution_contract_harness.md` | Phase 5 plan-execution contract harness summary, command, local result, and non-claim boundary. | tracked |
| `docs/runtime_adapter_permission_harness.md` | Phase 5 runtime adapter permission harness summary, command, local result, and non-claim boundary. | tracked |
| `docs/context_admission_adequacy_harness.md` | Phase 5 context admission/adequacy harness summary, command, local result, and non-claim boundary. | tracked |
| `docs/readiness_residual_harness.md` | Phase 5 readiness/residual gate harness summary, command, local result, and non-claim boundary. | tracked |
| `docs/benchmark_antigoodhart_harness.md` | Phase 5 benchmark anti-Goodhart harness summary, command, local result, and non-claim boundary. | tracked |
| `docs/resource_budget_ledger_harness.md` | Phase 5 resource-budget ledger harness summary, command, local result, and non-claim boundary. | tracked |
| `docs/capacity_smoothing_harness.md` | Phase 5 capacity-smoothing toy harness summary, command, local result, and non-claim boundary. | tracked |
| `docs/phase5_harness_registry.md` | Registry and traceability contract for the initial Phase 5 harness set. | tracked |
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
| `editions/reader_manuscript/` | Dormant curated reader-manuscript manifest, curation contract, synced chapter review matrix, artifact-inspection manifest, PDF probe manifest, companion-note routing manifest, reconciliation-report template, and future source area for a human-prose derivative that remains subordinate to the live book. | tracked |
| `scripts/init_curated_reader_chapter.py` | Dry-run-first helper for initializing future curated reader chapter records and starter files from the generated reader baseline when overlays become too small. | tracked |
| `assets/reader-overlays.html` | Generated embedded reader-overlay payload for live Human view. | tracked; regenerate from overlays |
| `sources/source_inventory.json` | Public-safe source metadata inventory. | tracked |
| `sources/cache/cache_manifest.json` | Public-safe cache metadata and hashes. | tracked |
| `sources/raw/` | Local raw source exports. | ignored |
| `sources/inbox/` | Local source drop area, including private or conversation-mined packets before public-safe synthesis. | ignored except README |
| `sources/source_notes/` | Public-safe notes created after source text is actually read. | tracked when notes are added |
| `proofs/` | Proof plans and generated proof target manifest. | tracked |
| `lean/` | Lean 4 proof workspace. | tracked except `.lake/` |
| `schemas/` | JSON Schemas for protocol records and the book-structure manifest contract. | tracked |
| `release_records/` | Public-safe live-book and future major-version edition release records checked against release-record schemas. | tracked |
| `evidence_transitions/` | Evidence-transition review records checked against `schemas/evidence_transition_record.schema.json`. | tracked |
| `experiments/` | Synthetic experiment and benchmark harness workspace, including claim-ledger revision, proof-carrying claim, support-state, authority, plan-execution, runtime-adapter, context-admission, readiness/residual, benchmark anti-Goodhart, generation-mode baseline, resource-budget ledger, and capacity-smoothing fixtures and result records, and the Phase 5 harness registry. | tracked |
| `scripts/` | Manifest sync, source cache, proof manifest, and validation tools. | tracked |
| `build/` | Generated reader/release edition source, reader/audio manifests, and output trees. | ignored |
| `skills/asi-stack-book/` | Project-specific Codex skill for maintaining and drafting the book. | tracked |
| `.github/` | GitHub Pages workflow, issue templates, and PR template. | tracked |
| `_site/`, `.quarto/`, `site_libs/` | Render/build outputs and Quarto cache. | ignored |

## Ownership Rules

- Edit `book_structure.json`, then run `python3 scripts/sync_scaffold.py`; `python3 scripts/validate_book.py` validates the manifest against `schemas/book_structure.schema.json` before semantic source/proof checks.
- Keep every chapter record in `book_structure.json` explicit about `claim_label` and `evidence_level`; `python3 scripts/validate_book.py` rejects missing or invalid values.
- Use `python3 scripts/chapter_adjacency_report.py` after adding, moving, merging, or removing chapters to identify the small set of Handoff sections whose manifest-order prose must be repaired.
- Edit `docs/book_outline.md`, then run `python3 scripts/sync_proof_manifest.py`.
- Edit public source metadata in `sources/source_inventory.json`; keep raw source text out of git unless publication is explicitly approved.
- Update `appendices/F_changelog.qmd` for meaningful changes.
- Edit `editions/release_profiles.json` for edition policy, then run `python3 scripts/validate_release_profiles.py`, `python3 scripts/sync_reader_overlay_asset.py --check`, `python3 scripts/validate_reading_mode_toggle.py`, `python3 scripts/validate_human_reading_paths.py`, `python3 scripts/build_reader_edition.py --check`, `python3 scripts/validate_reader_overlays.py --check`, `python3 scripts/validate_reader_evidence_boundaries.py --check`, `python3 scripts/validate_reader_spine.py --check`, `python3 scripts/render_reader_formats.py --check`, and `python3 scripts/build_audio_script.py --check` when the audio path is affected.
- Run `python3 scripts/audit_reader_continuity.py --write` after reader prose, overlay, or strip-policy changes that affect the generated reader manuscript, then validate with `python3 scripts/audit_reader_continuity.py --check`.
- Edit `editions/reader_manuscript/v1_0/manifest.json`, `editions/reader_manuscript/v1_0/curation_contract.json`, `editions/reader_manuscript/v1_0/artifact_inspection_manifest.json`, `editions/reader_manuscript/v1_0/epub_probe_manifest.json`, `editions/reader_manuscript/v1_0/docx_probe_manifest.json`, `editions/reader_manuscript/v1_0/pdf_probe_manifest.json`, or `editions/reader_manuscript/v1_0/companion_note_routing.json` only when reader-manuscript status, curated-source policy, artifact-inspection evidence, EPUB probe evidence, DOCX probe evidence, PDF probe evidence, or companion-note routing changes, then run `python3 scripts/validate_reader_manuscript_manifest.py`, `python3 scripts/validate_reader_artifact_inspection_manifest.py`, `python3 scripts/validate_reader_epub_probe_manifest.py`, `python3 scripts/validate_reader_docx_probe_manifest.py`, and `python3 scripts/validate_reader_pdf_probe_manifest.py` as applicable.
- Use `python3 scripts/init_curated_reader_chapter.py --chapter-id <id>` before hand-creating curated reader records; add `--write` only after review decides overlays are insufficient for that chapter.
- Run `python3 scripts/sync_reader_chapter_review_matrix.py --write` after chapter additions, removals, moves, overlay changes, or manual reader-review decisions; validate with `python3 scripts/sync_reader_chapter_review_matrix.py --check`.
- Edit `editions/reader_manuscript/v1_0/format_review_matrix.json` after reader-format render, structural inspection, e-reader/app inspection, PDF layout review, or release-record status changes; regenerate `docs/reader_format_review_matrix.md` with `python3 scripts/sync_reader_format_review_matrix.py --write`.

## Public Readiness Invariants

- No raw source exports are tracked.
- No rendered `_site/` output is tracked.
- No `.quarto/` cache is tracked.
- No Lean `.lake/` build output is tracked.
- No claim support state is promoted without a recorded basis.
- No proof or test result is reported unless the command was run and the result is recorded.
- No EPUB, PDF, DOCX, or audio artifact is reported unless that specific artifact was rendered or generated and recorded.
- Conversation-mined context is treated as author intent and lineage, not as external evidence or quotable source text.
