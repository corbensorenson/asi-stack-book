# The ASI Stack

**The ASI Stack: A Systems Architecture for Governed, Efficient, Self-Improving AI** is Corben Sorenson's living technical book about AI systems architecture.

Public book site: <https://corbensorenson.github.io/asi-stack-book/>

Public repository: <https://github.com/corbensorenson/asi-stack-book>

This repository is the canonical Quarto source for the book, its scaffolding, validation scripts, schemas, Lean proof workspace, and public-safe source/evidence metadata. The book treats the source papers as fragments of one architecture: alignment, governance, planning, memory, reasoning, execution, routing, compression, evidence, and recursive self-improvement.

## Current Status

The project has moved beyond the initial v0.2 manuscript baseline into an extended v1.0 candidate hardening pass, but it is not yet a final v1.0 evidence release.

- Quarto book structure is initialized and renders to HTML.
- All 54 outline chapters exist as manuscript drafts across four manifest-driven parts.
- `docs/book_outline.md` is the source of truth for the full-book drafting plan, per-part/per-chapter source queues, and Lean proof scope.
- `book_structure.json` controls parts, chapter order, stable chapter IDs, source assignments, implementation horizons, proof hooks, and appendix order, and `schemas/book_structure.schema.json` plus `scripts/validate_book.py` guard its shape.
- `_quarto.yml`, Appendix A, Appendix C, Appendix G, Appendix H, and Appendix K are generated.
- `editions/release_profiles.json` defines live, research, reader, and audio release profiles plus content layers for the reader spine, live research scaffold, evidence matrices, machine contracts, release derivatives, and audio adaptation.
- `scripts/build_reader_edition.py` can derive a cleaned reader-edition Quarto source tree, `reader_manifest.json`, and `reader_delta_report.md` under ignored `build/`.
- `editions/reader_overlays/README.md` and `editions/reader_overlays/v1_0/manifest.json` define the semantic reader-overlay layer for major-version human-edition deltas that should survive regeneration without forking the live book. The current v1.0 overlay set carries 33 active operations across opening-chapter prose, Efficient ASI, Human Intent, System Boundaries, Evidence States, Personal Compute Hives, Command Contracts, Planning, Verification Bandwidth, Runtime Adapters, Labor OS, Circle Contracts, Generate-Verify-Repair, Fast Generation, RankFold/NeuralFold, Mathematical and Search Substrates, Policy Optimization, Artifact Steward Agents, Executable Specifications, and Semantic Representation for Human view and generated reader editions only.
- `editions/reader_manuscript/v1_0/manifest.json` defines the dormant curated reader-manuscript path for the point where generated reader output plus overlays are no longer enough. `editions/reader_manuscript/v1_0/curation_contract.json` and `docs/curated_reader_source_contract.md` define the future curated-chapter record contract. The current manifest status is `not_graduated`, and `scripts/validate_reader_manuscript_manifest.py` enforces that any future curated manuscript remains a parallel derivative source for human prose, not an equal authority for claims, support states, source boundaries, proof/test status, implementation horizons, or release records.
- `scripts/init_curated_reader_chapter.py` can initialize a future curated reader chapter record and starter file from the generated reader baseline after review decides overlays are too small. It defaults to dry-run output and keeps release blockers active when `--write` is used.
- `editions/reader_manuscript/v1_0/chapter_review_matrix.json` and `docs/reader_chapter_review_matrix.md` track the full 54-chapter human-reader review queue. `scripts/sync_reader_chapter_review_matrix.py --check` keeps chapter IDs, part order, live files, generated-reader files, and active overlay counts synced to `book_structure.json` while preserving review statuses, dispositions, companion-note candidates, curated-manuscript candidates, and release blockers.
- `editions/reader_manuscript/v1_0/companion_note_routing.json` and `docs/reader_companion_note_routing_review.md` record the current chapter-level companion-note routing for dense proof/governance chapters. Generated reader and audio companion notes consume this routing manifest, but it is not a reader release, artifact approval, support-state promotion, or curated manuscript.
- `scripts/sync_reader_overlay_asset.py` embeds active reader overlay operations in `assets/reader-overlays.html` so the live Human view and generated reader edition share the same section-delta source.
- `scripts/validate_reader_overlays.py` checks that reader overlays are section-anchored, apply cleanly, and produce a generated delta report with operation digests and before/after review excerpts.
- `scripts/audit_reader_continuity.py --check` keeps `docs/reader_continuity_audit.md` current as a generated Phase 2 heuristic queue for human-reader continuity review; it does not claim a reviewed reader release exists.
- `scripts/validate_reader_spine.py` checks that every generated reader chapter keeps a substantial human-readable spine, required chapter sections, section-level prose/word-count floors, chapter-specific Handoff continuity, and no live-only scaffolding after stripping.
- `scripts/validate_reader_evidence_boundaries.py` checks that every generated reader chapter strips raw live core-claim markers and repeated support boilerplate while preserving the claim text and a compact inline plain-language support-state boundary in the Core Claim section.
- `scripts/validate_human_reading_paths.py` checks that every manifest chapter has exactly one `.asi-human-only` Human Reading Path bridge and that reader-edition generation unwraps it into ordinary prose.
- `scripts/render_reader_formats.py` can attempt reader-edition HTML/EPUB/DOCX/PDF renders, snapshot successful format outputs under ignored `build/reader_edition/format_artifacts/`, and write a local `reader_render_report.json` with actual outcomes.
- `scripts/inspect_reader_format_artifacts.py` can structurally inspect ignored local HTML/EPUB/DOCX reader snapshots for required files, EPUB/DOCX container integrity, EPUB OPF metadata, media counts, and obvious live-scaffold leaks without treating them as release artifacts.
- `scripts/sync_reader_format_review_matrix.py` validates the tracked v1.0 format-review ledger and regenerates the public blocker summary, keeping local dry-run evidence separate from edition release approval.
- `editions/reader_manuscript/v1_0/artifact_inspection_manifest.json`, `docs/reader_artifact_inspection_manifest.md`, and `scripts/validate_reader_artifact_inspection_manifest.py` preserve a tracked summary of the latest local HTML/EPUB/DOCX structural inspection while keeping the ignored build artifacts out of git and keeping all release blockers intact.
- `editions/reader_manuscript/v1_0/epub_probe_manifest.json`, `docs/reader_epub_probe_manifest.md`, and `scripts/validate_reader_epub_probe_manifest.py` preserve the latest local EPUB probe facts: 9,078,787 bytes, 62 XHTML entries, 62 image entries, `en-US` language metadata, sampled evidence-boundary/source-card text, and the remaining e-reader application blocker. This is a probe record, not EPUB approval.
- `editions/reader_manuscript/v1_0/docx_probe_manifest.json`, `docs/reader_docx_probe_manifest.md`, and `scripts/validate_reader_docx_probe_manifest.py` preserve the latest local DOCX LibreOffice conversion probe facts: 514 converted pages, 8,190,162 bytes, expected title/evidence-boundary/source-card text, and a representative six-page visual sample. This is a probe record, not DOCX approval.
- `editions/reader_manuscript/v1_0/pdf_probe_manifest.json`, `docs/reader_pdf_probe_manifest.md`, and `scripts/validate_reader_pdf_probe_manifest.py` preserve the latest local UTF-8 PDF probe facts: 535 pages, 8,613,924 bytes, expected title/evidence-boundary text, refreshed sampled source-card pages, and the remaining full-PDF-layout blocker. This is a probe record, not PDF approval.
- `scripts/build_reader_edition.py` and `scripts/build_audio_script.py` now emit generated review checklists and companion notes so major-version reader, e-reader, and audio work stay downstream of the living book instead of becoming parallel manuscripts.
- `scripts/build_audio_script.py` can derive an audio-script review workspace, `audio_manifest.json`, chapter markers, an audio checklist, and pronunciation glossary under ignored `build/`; its check also verifies that chapter scripts preserve both implementation-horizon sections.
- `scripts/validate_claim_ledger_revision.py`, `scripts/validate_proof_carrying_claims.py`, `scripts/validate_tribunal_review.py`, `scripts/validate_value_conflicts.py`, `scripts/validate_governance_rights.py`, `scripts/validate_agency_rights.py`, `scripts/validate_support_state_transitions.py`, `scripts/validate_authority_transitions.py`, `scripts/validate_plan_execution_contracts.py`, `scripts/validate_runtime_adapter_permissions.py`, `scripts/validate_context_admission_adequacy.py`, `scripts/validate_readiness_residual_gates.py`, `scripts/validate_benchmark_antigoodhart.py`, `scripts/validate_generation_mode_baselines.py`, `scripts/validate_resource_budget_ledgers.py`, and `scripts/validate_capacity_smoothing.py` run synthetic or deterministic harnesses for claim-ledger revision discipline, proof-carrying claim discipline, tribunal-review record discipline, value-conflict record discipline, governance-right record discipline, agency-right checklist discipline, support-state conservatism, authority non-escalation, plan/contract/job consistency, runtime-adapter permission/approval/receipt discipline, context admission/adequacy consistency, readiness/residual custody, benchmark anti-Goodhart discipline, generation-mode baseline accounting, resource-budget ledger discipline, and capacity-smoothing toy traces; `experiments/phase5_harness_registry.json` plus `scripts/validate_phase5_harness_registry.py` keep the harness set wired to docs, fixtures, result records, Appendix E, and book validation. These are executable or traceability checks over fixtures and records, not claim promotions or deployed-runtime evidence.
- The live GitHub Pages site includes a persistent top-of-page reading-mode switch: `AI view` keeps the full live/research scaffold, including raw core-claim markers and repeated support-state boilerplate, while `Human view` hides the same repeated chapter sections, TOC entries, section-numbering artifacts, raw bracketed core-claim markers, and repeated support boilerplate used by the reader-release strip policy. Human view keeps the compact evidence boundary inline with the core claim rather than opening repeated support paragraphs. Readers can open a chapter directly in either mode with `?view=human` or `?view=ai`. All 54 chapters now carry a `.asi-human-only` Human Reading Path bridge for interested readers, and `.asi-ai-only` blocks remain available for mode-specific research notes without forking the manuscript. The rendered-site validator checks the static HTML hooks, and `scripts/validate_live_human_view_browser.js` exercises representative rendered pages by default or every manifest chapter across desktop and mobile viewports with `--all-chapters --all-viewports` in a real browser when Playwright/Chrome is available, including reading-mode control visibility, rendered Mermaid visibility, raw-marker and support-boilerplate hiding/restoration, and page-overflow checks.
- `proofs/proof_manifest.json` is generated from `lean:*` proof tags in the outline.
- `proofs/proof_triage.json` classifies proof targets as Lean, schema, process, or research-agenda work.
- Source notes exist for all currently assigned source records, and connector-readiness metadata remains tracked for source routes that depend on authenticated exports.
- Source documents are cached locally when available, but raw exports are ignored and not published.
- `scripts/validate_source_appendices.py` checks that Appendix G and Appendix H are independent top-level appendices with explicit source-ownership boundary blocks and separate appendix-identity rows: G contains only Corben's own papers, Corben-supplied materials, recovered project records, and local project records, while H contains only external-source and third-party literature records by other authors or organizations generated from `sources/source_inventory.json`.
- `scripts/validate_v1_status_snapshot.py` checks that `docs/v1_0_candidate_status.md` headline counts match current repository artifacts.
- `scripts/validate_outline_consistency.py` checks that `docs/book_outline.md` still matches the manifest chapter order, titles, core claims, assigned source IDs, and Lean proof targets.
- `scripts/validate_implementation_horizons.py` checks that every manifest chapter has a concrete minimum viable implementation and mature endpoint, and that generated Appendix K matches the manifest in order.
- Current source-note coverage, exact claim-source mappings, and passage-reviewed mappings are complete for assigned source/chapter pairs, but all chapter core claims remain at `argument` support until accepted evidence transitions justify promotion.
- Protocol schema fixture checks and manifest schema validation are implemented; broader chapter-level Codex tests remain planned unless a specific test result is recorded.
- `scripts/draft_v02_from_manifest.py` records the repeatable baseline drafting pass; use it intentionally because it rewrites chapter files from the manifest.

## Start Here

| File or page | Purpose |
|---|---|
| [Live book](https://corbensorenson.github.io/asi-stack-book/) | Rendered public site. |
| [docs/book_outline.md](docs/book_outline.md) | Cohesive full-book outline and proof target source of truth. |
| [docs/prewriting_readiness.md](docs/prewriting_readiness.md) | Launch gate for a full-book drafting goal. |
| [docs/full_book_writing_goal.md](docs/full_book_writing_goal.md) | Suggested wording for the full-book writing goal. |
| [docs/v1_0_candidate_status.md](docs/v1_0_candidate_status.md) | Current v1.0 candidate snapshot, remaining evidence gaps, and release gate. |
| [docs/v1_0_focus_audit.md](docs/v1_0_focus_audit.md) | Detailed current-state audit and prioritized work plan for moving from v1.0 candidate toward evidence-release and reader-release quality. |
| [docs/v1_0_roadmap.md](docs/v1_0_roadmap.md) | Execution roadmap and recommended next long-running goal for v1.0 voice, reader, evidence, proof, test, source, site, and release work. |
| [docs/reader_overlay_pilot.md](docs/reader_overlay_pilot.md) | First active v1.0 semantic reader-overlay pilot. |
| [docs/reader_continuity_audit.md](docs/reader_continuity_audit.md) | Generated Phase 2 heuristic queue for reader-manuscript continuity review. |
| [docs/reader_chapter_review_matrix.md](docs/reader_chapter_review_matrix.md) | Manifest-synced 54-chapter human-reader review queue and release blockers. |
| [docs/reader_part_i_review_pass.md](docs/reader_part_i_review_pass.md) | First Part I reader-review matrix pass and no-action decisions. |
| [docs/reader_part_ii_review_pass.md](docs/reader_part_ii_review_pass.md) | First Part II reader-review matrix pass and canonical prose cleanup decisions. |
| [docs/reader_part_iii_review_pass.md](docs/reader_part_iii_review_pass.md) | First Part III reader-review matrix pass and canonical prose cleanup decisions. |
| [docs/reader_part_iv_review_pass.md](docs/reader_part_iv_review_pass.md) | First Part IV reader-review matrix pass and reader-generator capitalization cleanup decision. |
| [editions/reader_manuscript/v1_0/reconciliation_report.md](editions/reader_manuscript/v1_0/reconciliation_report.md) | Dormant curated-reader reconciliation template for future parallel human-prose chapters. |
| [docs/curated_reader_source_contract.md](docs/curated_reader_source_contract.md) | Contract for future curated reader chapter files as parallel derivative prose, not equal evidence authority. |
| [scripts/init_curated_reader_chapter.py](scripts/init_curated_reader_chapter.py) | Dry-run-first initializer for future curated reader chapter records and starter files. |
| [editions/reader_manuscript/v1_0/companion_note_routing.json](editions/reader_manuscript/v1_0/companion_note_routing.json) | Chapter-level companion-note routing manifest for reader, e-reader, and audio review. |
| [docs/reader_companion_note_routing_review.md](docs/reader_companion_note_routing_review.md) | Human-readable review note for current companion-note routing decisions. |
| [docs/reader_format_dry_run.md](docs/reader_format_dry_run.md) | Local HTML/EPUB/DOCX reader-format dry-run record and non-release boundary. |
| [docs/reader_format_review_matrix.md](docs/reader_format_review_matrix.md) | Synced pre-release reader-format review ledger for HTML, EPUB, DOCX, and PDF blockers. |
| [docs/reader_artifact_inspection_manifest.md](docs/reader_artifact_inspection_manifest.md) | Tracked local HTML/EPUB/DOCX structural-inspection summary for ignored reader-format snapshots. |
| [docs/reader_epub_probe_manifest.md](docs/reader_epub_probe_manifest.md) | Tracked local EPUB metadata/source-spine probe summary and e-reader-specific release blockers. |
| [docs/reader_docx_probe_manifest.md](docs/reader_docx_probe_manifest.md) | Tracked local DOCX LibreOffice conversion probe summary, spot-check residuals, and DOCX-specific release blockers. |
| [docs/reader_pdf_probe_manifest.md](docs/reader_pdf_probe_manifest.md) | Tracked local UTF-8 PDF probe summary, spot-check residuals, and PDF-specific release blockers. |
| [docs/reader_artifact_layout_review.md](docs/reader_artifact_layout_review.md) | Representative local PDF/HTML layout spot check and remaining artifact-review residuals. |
| [docs/claim_ledger_revision_harness.md](docs/claim_ledger_revision_harness.md) | Phase 5 synthetic claim-ledger and belief-revision record-discipline harness. |
| [docs/proof_carrying_claim_harness.md](docs/proof_carrying_claim_harness.md) | Phase 5 synthetic proof-carrying claim tier, verifier, and mismatch harness. |
| [docs/tribunal_review_harness.md](docs/tribunal_review_harness.md) | Phase 5 synthetic tribunal-review dossier, dissent, and verdict-boundary harness. |
| [docs/value_conflict_harness.md](docs/value_conflict_harness.md) | Phase 5 synthetic value-conflict classification, review, and residual-boundary harness. |
| [docs/governance_rights_harness.md](docs/governance_rights_harness.md) | Phase 5 synthetic governance-right audit, exit, fork, and appeal-boundary harness. |
| [docs/agency_rights_harness.md](docs/agency_rights_harness.md) | Phase 5 synthetic agency-right material-usability, timing, corrigibility, and approval-boundary harness. |
| [docs/support_state_transition_harness.md](docs/support_state_transition_harness.md) | Phase 5 synthetic support-state transition gate harness. |
| [docs/authority_transition_harness.md](docs/authority_transition_harness.md) | Phase 5 synthetic authority non-escalation and permission-separation harness. |
| [docs/plan_execution_contract_harness.md](docs/plan_execution_contract_harness.md) | Phase 5 synthetic plan graph and execution-contract harness. |
| [docs/runtime_adapter_permission_harness.md](docs/runtime_adapter_permission_harness.md) | Phase 5 synthetic runtime adapter permission, approval, receipt, and rollback/residual harness. |
| [docs/context_admission_adequacy_harness.md](docs/context_admission_adequacy_harness.md) | Phase 5 synthetic context admission and adequacy harness. |
| [docs/readiness_residual_harness.md](docs/readiness_residual_harness.md) | Phase 5 synthetic readiness gate and residual escrow harness. |
| [docs/benchmark_antigoodhart_harness.md](docs/benchmark_antigoodhart_harness.md) | Phase 5 synthetic benchmark anti-Goodhart harness. |
| [docs/generation_mode_baseline_harness.md](docs/generation_mode_baseline_harness.md) | Phase 5 deterministic generation-mode baseline and resource-budget alignment harness. |
| [docs/resource_budget_ledger_harness.md](docs/resource_budget_ledger_harness.md) | Phase 5 deterministic resource-budget ledger harness. |
| [docs/capacity_smoothing_harness.md](docs/capacity_smoothing_harness.md) | Phase 5 deterministic capacity-smoothing toy harness. |
| [docs/phase5_harness_registry.md](docs/phase5_harness_registry.md) | Registry and traceability contract for the initial Phase 5 harness set. |
| [docs/v02_manuscript_status.md](docs/v02_manuscript_status.md) | Historical v0.2 manuscript completion, gaps, and validation status. |
| [docs/external_literature_queue.md](docs/external_literature_queue.md) | Explicit stance and queue for third-party literature. |
| [docs/release_editions_plan.md](docs/release_editions_plan.md) | Major-version EPUB/PDF/DOCX/audio edition plan and gates. |
| [docs/major_version_release_runbook.md](docs/major_version_release_runbook.md) | Operational ladder for tagged live, reader, e-reader/document, and audio releases. |
| [docs/local_project_mining_theseus_circle.md](docs/local_project_mining_theseus_circle.md) | Public-safe mining report for Project Theseus and Circle Calculus. |
| [book_structure.json](book_structure.json) | Schema-validated manifest for dynamic parts, chapters, source assignments, implementation horizons, proof hooks, and appendices. |
| [editions/release_profiles.json](editions/release_profiles.json) | Audience-specific release profile definitions. |
| [editions/reader_manuscript/README.md](editions/reader_manuscript/README.md) | Dormant curated reader-manuscript path and future graduation rule. |
| [appendices/A_source_matrix.qmd](appendices/A_source_matrix.qmd) | Generated source-to-chapter matrix. |
| [appendices/C_claim_evidence_matrix.qmd](appendices/C_claim_evidence_matrix.qmd) | Generated claim/evidence matrix. |
| [appendices/G_corben_source_corpus.qmd](appendices/G_corben_source_corpus.qmd) | Generated appendix for Corben's own sources, papers, and local project records. |
| [appendices/H_external_sources.qmd](appendices/H_external_sources.qmd) | Generated appendix for external sources and third-party literature by other authors. |
| [appendices/I_author_intent_and_lineage.qmd](appendices/I_author_intent_and_lineage.qmd) | Public-safe author-intent and architecture-lineage appendix. |
| [appendices/J_release_editions.qmd](appendices/J_release_editions.qmd) | Live-book explanation of reader, research, and audio edition paths. |
| [appendices/K_implementation_horizons.qmd](appendices/K_implementation_horizons.qmd) | Generated implementation-horizon matrix. |
| [proofs/proof_manifest.json](proofs/proof_manifest.json) | Generated Lean proof target manifest. |
| [docs/repository_map.md](docs/repository_map.md) | Repository layout and ownership map. |
| [docs/publication_readiness.md](docs/publication_readiness.md) | Public-readiness checklist and known blockers. |

## Local Validation

Run this before committing structural, source, proof, or publication changes:

```bash
python3 scripts/sync_scaffold.py
python3 scripts/sync_proof_manifest.py
python3 scripts/sync_reader_overlay_asset.py --check
python3 scripts/source_readiness_report.py
python3 scripts/validate_publication.py
python3 scripts/validate_release_profiles.py
python3 scripts/validate_human_reading_paths.py
python3 scripts/validate_source_appendices.py
python3 scripts/validate_v1_status_snapshot.py
python3 scripts/validate_outline_consistency.py
python3 scripts/validate_implementation_horizons.py
python3 scripts/validate_reader_evidence_boundaries.py --check
python3 scripts/validate_reader_overlays.py --check
python3 scripts/audit_reader_continuity.py --check
python3 scripts/validate_reader_manuscript_manifest.py
python3 scripts/validate_reader_artifact_inspection_manifest.py
python3 scripts/validate_reader_epub_probe_manifest.py
python3 scripts/validate_reader_docx_probe_manifest.py
python3 scripts/validate_reader_pdf_probe_manifest.py
python3 scripts/sync_reader_chapter_review_matrix.py --check
python3 scripts/sync_reader_format_review_matrix.py --check
python3 scripts/validate_reader_spine.py --check
python3 scripts/validate_claim_ledger_revision.py
python3 scripts/validate_proof_carrying_claims.py
python3 scripts/validate_tribunal_review.py
python3 scripts/validate_value_conflicts.py
python3 scripts/validate_governance_rights.py
python3 scripts/validate_agency_rights.py
python3 scripts/validate_support_state_transitions.py
python3 scripts/validate_authority_transitions.py
python3 scripts/validate_plan_execution_contracts.py
python3 scripts/validate_runtime_adapter_permissions.py
python3 scripts/validate_context_admission_adequacy.py
python3 scripts/validate_readiness_residual_gates.py
python3 scripts/validate_benchmark_antigoodhart.py
python3 scripts/validate_generation_mode_baselines.py
python3 scripts/validate_resource_budget_ledgers.py
python3 scripts/validate_capacity_smoothing.py
python3 scripts/validate_phase5_harness_registry.py
python3 scripts/validate_book.py
python3 scripts/validate_visual_coverage.py
python3 scripts/validate_reading_mode_toggle.py
python3 scripts/validate_schemas.py
python3 scripts/validate_protocol_examples.py
quarto render --to html
python3 scripts/validate_live_human_view.py
node scripts/validate_live_human_view_browser.js --all-chapters --all-viewports
```

For Lean proof work:

```bash
cd lean
lake build
```

The rendered HTML is written to `_site/`, which is ignored by git.

## Release Editions

The live book is optimized for AIs and human researchers. Major versions can also produce cleaned human-reader editions and audio editions from the same source.

The project uses one canonical source tree with explicit content layers:

- The reader-facing chapter spine is ordinary prose, diagrams, examples, uncertainty, and summaries that should still read well after live-only headings are removed.
- The live research scaffold contains source crosswalks, guardrails, Codex tests, formalization hooks, claim mappings, and other audit machinery for AIs and researchers.
- The live Human view uses the same reader-strip policy on the GitHub Pages site. Each chapter's `.asi-human-only` Human Reading Path bridge is hidden in default AI view, shown in Human view, and unwrapped into reader editions; `.asi-ai-only` blocks are removed from reader editions; raw bracketed core-claim markers and repeated support-state boilerplate are visible in AI view but hidden or humanized in Human view and stripped from generated reader chapters while the claim text and compact inline evidence boundary remain.
- Reader overlays under `editions/reader_overlays/` are tracked semantic deltas for major human-reader versions. They target stable files and headings, feed both generated reader editions and the live Human view through `assets/reader-overlays.html`, then generate `reader_delta_report.md` with operation digests and before/after excerpts for review; generated reader files under `build/` are still disposable and should not be hand-edited. When overlays become too large or too numerous for clean semantic deltas, the dormant curated reader-manuscript path can graduate into a human-prose derivative while the live book remains canonical for evidence.
- Companion material records how diagrams, tables, code, schemas, and omitted dense matrices should be handled for e-reader, document, and audio releases.
- Release derivatives such as EPUB, PDF, DOCX, MP3, M4B, and audio-embedded EPUB exist only after generation or render, review, and release-record entry.

For major versions, use [docs/major_version_release_runbook.md](docs/major_version_release_runbook.md) as the operating sequence: tag the live book, validate the live/research surface, generate and review the reader manuscript, render only the formats that pass locally, then derive audio from the reviewed reader script.

Tracked release profile source:

```bash
python3 scripts/validate_release_profiles.py
python3 scripts/sync_reader_overlay_asset.py --check
```

Generate or check a local reader-edition Quarto source tree:

```bash
python3 scripts/build_reader_edition.py --check
python3 scripts/validate_reader_overlays.py --check
python3 scripts/validate_human_reading_paths.py
python3 scripts/validate_reader_evidence_boundaries.py --check
python3 scripts/validate_reader_spine.py --check
python3 scripts/build_reader_edition.py
```

Render selected reader-edition formats and record actual local outcomes:

```bash
python3 scripts/render_reader_formats.py --check
python3 scripts/render_reader_formats.py --formats html epub docx
python3 scripts/inspect_reader_format_artifacts.py
python3 scripts/validate_reader_epub_probe_manifest.py
python3 scripts/validate_reader_docx_probe_manifest.py
python3 scripts/validate_reader_pdf_probe_manifest.py
python3 scripts/sync_reader_format_review_matrix.py --check
LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 python3 scripts/render_reader_formats.py --formats html epub docx pdf
```

Generate or check a narration-script candidate after the reader manuscript is ready for review:

```bash
python3 scripts/build_audio_script.py --check
python3 scripts/build_audio_script.py
```

Generated edition builds are written under `build/` and ignored by git. Reader builds include `READER_RELEASE_CHECKLIST.md`, `companion_notes.md`, and `reader_delta_report.md`; render dry runs also preserve per-format snapshots under `build/reader_edition/format_artifacts/` for local review. Audio builds include `AUDIO_RELEASE_CHECKLIST.md`, `companion_notes.md`, `chapter_markers.md`, and `pronunciation_glossary.md`. Do not claim EPUB, PDF, DOCX, AZW3, MOBI, MP3, M4B, or audio-embedded EPUB artifacts as release artifacts unless those specific render, conversion, or audio-generation commands have actually succeeded, been reviewed where required, and a release record says so.

## Dynamic Book Structure

Do not hand-edit `_quarto.yml` or use numbered chapter filenames. Edit `book_structure.json`, then run:

```bash
python3 scripts/sync_scaffold.py
```

Useful helpers:

```bash
python3 scripts/add_part.py --title "Part IV - New Research Track"
python3 scripts/add_chapter.py --part planning-memory-reasoning-execution --title "New AI Topic" --after planning-as-a-control-layer
python3 scripts/chapter_adjacency_report.py --chapter new-ai-topic
```

Quarto generates displayed chapter numbers at render time, so chapters can be inserted, moved, merged, or removed without renumbering files. Chapter prose still has manifest-aware Handoffs; after structural edits, use the adjacency report and `python3 scripts/validate_chapter_handoffs.py` to update only the affected neighboring Handoff sections.

## Manuscript Regeneration

The v0.2 baseline can be regenerated from `book_structure.json`:

```bash
python3 scripts/draft_v02_from_manifest.py
```

This is a bulk rewrite tool. Use it for intentional full-baseline regeneration, not for routine chapter editing after hand-written source-specific prose has been added.

## Source Discipline

Raw source exports are private/local and ignored by git.

```bash
python3 scripts/cache_drive_sources.py
python3 scripts/source_readiness_report.py
```

The tracked readiness report is `docs/source_readiness_report.md`. Raw exports stay under `sources/raw/`.

When adding a new AI paper or artifact, use [docs/living_update_workflow.md](docs/living_update_workflow.md) and the repo skill triage reference before editing prose. New sources need storage/public-safety policy, deduplication state, chapter-decision refs, required pre-drafting work, and promotion blockers. `schemas/research_backlog_record.schema.json` records durable backlog items, and `schemas/new_paper_triage_scenario.schema.json` validates synthetic update/add/defer/reject decision shape only.

Claims use both a claim label and a support state. Do not mark a claim as `source-derived`, `prototype-backed`, `synthetic-test-backed`, `empirical-test-backed`, or `external-literature-backed` unless the source ingestion, prototype review, proof check, or test execution actually happened and is recorded. Conversation-mined material can guide author intent and lineage, but it is not external evidence.

Every chapter record in `book_structure.json` must explicitly declare both `claim_label` and `evidence_level`. `scripts/add_chapter.py` supplies conservative defaults for new chapters, and `python3 scripts/validate_book.py` validates the manifest against `schemas/book_structure.schema.json` before rejecting missing or invalid semantic values.

## Proof Discipline

`docs/book_outline.md` is the source of truth for Lean proof scope. Every chapter has `lean:*` proof tags under `Lean proof targets`, plus source queues that tell future writing runs what to load first.

Generate the machine-readable proof manifest from the outline:

```bash
python3 scripts/sync_proof_manifest.py
python3 scripts/validate_proof_readiness.py
```

Do not report a theorem as proven unless the corresponding Lean module exists, the module is imported by the Lean package root, the target is marked implemented in the outline, and `lake build` passes. Use `proofs/proof_triage.json` to keep schema/process/research targets from becoming ceremonial Lean; `scripts/validate_proof_readiness.py` checks that triage tags, modules, root imports, formal targets, and target statuses stay aligned with the generated manifest.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). The short version:

- Preserve the manifest-driven structure.
- Keep speculative claims labeled.
- Do not publish private raw sources.
- Do not fabricate source content, citations, proofs, benchmark results, or test results.
- Run validation and render locally before proposing changes.

## Rights

See [LICENSE.md](LICENSE.md). This public repository is available for reading and review, but no reuse license is granted unless Corben Sorenson provides one separately.
