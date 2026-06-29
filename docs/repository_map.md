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
| `docs/v1_x_beyond_sota_roadmap.md` | Post-v1.0.0 roadmap for v1.x evidence depth, safety-critical Lean upgrades, public-safe Project Theseus/Circle replay lanes, per-chapter evidence targets, curated reader prose, and human artifact quality. | tracked |
| `docs/a_plus_quality_scorecard.md` | Planning scorecard translating current project grade gaps into A+ conditions for cold-read legibility, evidence depth, proof rigor, external grounding, reader quality, and defended contribution tracks. | tracked |
| `docs/defended_contribution_tracks.md` | v1.x defended-contribution selection record: five selected tracks, three deep-work tracks, active evidence-cycle anchors, and no-promotion boundaries. | tracked |
| `docs/defended_contribution_prior_art_positioning.md` | Source-noted prior-art positioning record for the five defended contribution tracks, with comparator IDs, remaining gaps, and no-support-state-movement boundaries. | tracked |
| `docs/evidence_laundering_prevention_case_studies.md` | No-promotion case-study record for evidence-laundering prevention, covering Theseus static import, Circle consumer gate, reader HTML artifact review, and the remaining demotion/refutation gap. | tracked |
| `docs/per_chapter_evidence_plan.md` | 54-chapter evidence-lane backlog for selecting a small high-payoff v1.x execution set without triggering another shallow breadth sweep. | tracked |
| `docs/v1_x_active_evidence_cycle.md` | Active v1.x evidence-cycle ledger naming the seven selected high-payoff lanes, the forty-seven planned-only lanes, and the no-chapter-core-promotion boundary. | tracked |
| `docs/chapter_consolidation_sequence.md` | Governed full consolidation sequence for the 54-to-44/47 chapter-shape critique, preserving cluster order, protected chapters, no-manifest-edit boundaries, and review prerequisites. | tracked |
| `docs/chapter_consolidation_pilot_plan.md` | Governed chapter-consolidation pilot plan for the Part I alignment/governance cluster, preserving claim/source/proof/reader boundaries before any manifest merge. | tracked |
| `docs/chapter_consolidation_dry_run_constitutional_alignment.md` | First dry-run merge package for `constitutional-alignment-substrate` plus `agency-dignity-and-corrigibility`; review artifact only, not a manifest edit or support-state change. | tracked |
| `docs/chapter_consolidation_destination_draft_constitutional_alignment.md` | First review-ready destination draft for the proposed Constitutional Alignment plus Agency/Dignity/Corrigibility merge; not reviewed, not canonical, and not a manifest edit. | tracked |
| `docs/chapter_consolidation_dry_run_contestable_governance.md` | Second dry-run merge package for `moral-uncertainty-and-value-conflict` plus `governance-rights-fork-exit-and-audit`; review artifact only, not a manifest edit or support-state change. | tracked |
| `docs/chapter_consolidation_destination_draft_contestable_governance.md` | Second review-ready destination draft for the proposed Moral Uncertainty plus Governance Rights merge; not reviewed, not canonical, and not a manifest edit. | tracked |
| `docs/chapter_consolidation_dry_run_compression.md` | First non-pilot dry-run package for `compact-generative-systems-and-residual-honesty`, `generate-verify-repair-compression`, and conditional RankFold/NeuralFold folding; review artifact only, not a manifest edit or support-state change. | tracked |
| `docs/chapter_consolidation_destination_draft_compression.md` | First non-pilot review-ready destination draft for **Compact Generative Systems: Generate, Verify, Repair, and Residual Honesty**; not reviewed, not canonical, and not a manifest edit. | tracked |
| `docs/chapter_consolidation_dry_run_intent_contracts.md` | Dry-run merge package for `intent-to-execution-contracts` plus `command-contracts-and-semantic-interfaces`; review artifact only, not a manifest edit or support-state change. | tracked |
| `docs/chapter_consolidation_destination_draft_intent_contracts.md` | Review-ready destination draft for **Command Contracts: From Intent to Executable Work**; not reviewed, not canonical, and not a manifest edit. | tracked |
| `docs/chapter_consolidation_dry_run_context_abi.md` | Dry-run merge package for `virtual-context-abi` plus `semantic-pages-context-cells-and-certificates`; review artifact only, not a manifest edit or support-state change. | tracked |
| `docs/chapter_consolidation_destination_draft_context_abi.md` | Review-ready destination draft for **The Virtual Context ABI: Typed Pages, Cells, and Certificates**; not reviewed, not canonical, and not a manifest edit. | tracked |
| `docs/chapter_consolidation_decision_review.md` | Current Part I consolidation decision: destination drafts are review-ready, but manifest merge waits on human/external review plus a public URL, redirect, or historical-note policy. | tracked |
| `docs/chapter_consolidation_external_review_packet.md` | Supplemental review request packet for deciding whether to execute, revise, defer, or reject the Part I consolidation pilot before any manifest merge. | tracked |
| `docs/external_review_packet.md` | Public packet for v1.x external review, including scope, questions, response template, and review-is-not-evidence boundary. | tracked |
| `docs/external_review_status.md` | Ledger for the public external-review request, current no-accepted-review state, routing rules, and non-claims. | tracked |
| `external_reviews/request_updates/consolidation_review_request_2026-06-29.json` | Structured request-update record for the supplemental consolidation review solicitation; validates as no accepted review and no support-state effect. | tracked |
| `schemas/external_review_intake_record.schema.json` | Schema for public request updates, accepted review records, blockers, and rejected-review intake records. | tracked |
| `docs/chapter_external_grounding_status.md` | Generated 54-chapter status ledger tying each chapter to source-noted external comparators, explicit exceptions, and Corben/local sources to mine before broad literature search. | tracked |
| `docs/reader_manuscript_review.md` | Phase 2 baseline for the generated reader manuscript, including generated-reader metrics, spot-review notes, residuals, and non-claims. | tracked |
| `docs/reader_overlay_pilot.md` | First active Phase 2 semantic reader-overlay pilot for opening-chapter Human-view and generated-reader prose. | tracked |
| `docs/reader_continuity_audit.md` | Generated Phase 2 heuristic audit and priority queue for reader-manuscript continuity review. | tracked |
| `docs/reader_chapter_review_matrix.md` | Generated public summary of the manifest-synced 54-chapter human-reader review queue, overlay dispositions, and release blockers. | tracked |
| `docs/reader_format_review_matrix.md` | Generated public summary of the v1.0 reader-format review ledger, local render/inspection evidence, and artifact-release blockers. | tracked |
| `docs/reader_artifact_inspection_manifest.md` | Tracked local HTML/EPUB/DOCX structural-inspection summary for ignored reader-format snapshots, preserving release blockers and non-claims. | tracked |
| `docs/reader_html_artifact_browser_review.md` | Full local browser review record for the generated reader HTML snapshot, including exact ignored-artifact digest and the boundary between review evidence and the separate edition release record. | tracked |
| `docs/reader_epub_probe_manifest.md` | Tracked local EPUB metadata/source-spine probe summary for the ignored reader snapshot, including exact EPUB metrics, sampled source-card entries, and e-reader-specific release blockers. | tracked |
| `docs/reader_docx_probe_manifest.md` | Tracked local DOCX LibreOffice conversion probe summary for the ignored reader snapshot, including exact conversion metrics, sampled source-card pages, and DOCX-specific release blockers. | tracked |
| `docs/reader_pdf_probe_manifest.md` | Tracked local UTF-8 PDF probe summary for the ignored reader snapshot, including exact PDF metrics, sampled source-card pages, and PDF-specific release blockers. | tracked |
| `docs/reader_audio_script_probe_manifest.md` | Tracked local audio-script review-workspace probe summary for the ignored audio script, including script-file count, spoken-treatment counts, and audio-specific release blockers. | tracked |
| `docs/reader_companion_note_routing_review.md` | Human-readable companion-note routing decision for the dense proof/governance chapters flagged by the reader matrix. | tracked |
| `docs/curated_reader_circle_contracts_prose_pass.md` | Drafting-only curated reader prose-pass record for the Circle proof-carrying contracts chapter; preserves proof/test, support-state, release, and Circle replay boundaries. | tracked |
| `docs/curated_reader_executable_specs_prose_pass.md` | Drafting-only curated reader prose-pass record for the Executable Specifications and Lean proof-envelope chapter; preserves proof adequacy, support-state, and release boundaries. | tracked |
| `docs/curated_reader_evidence_states_prose_pass.md` | Drafting-only curated reader prose-pass record for the Evidence States and Claim Discipline chapter; preserves support-state, source, proof/test, demotion/refutation, and release boundaries. | tracked |
| `docs/reader_part_i_review_pass.md` | First Part I generated-reader review pass over matrix rows, recording no-action decisions without release approval. | tracked |
| `docs/reader_part_ii_review_pass.md` | First Part II generated-reader review pass over matrix rows, recording canonical prose cleanups and no-action decisions without release approval. | tracked |
| `docs/reader_part_iii_review_pass.md` | First Part III generated-reader review pass over matrix rows, recording canonical prose cleanups and no-action decisions without release approval. | tracked |
| `docs/reader_part_iv_review_pass.md` | First Part IV generated-reader review pass over matrix rows, recording reader-generator cleanup and no-action decisions without release approval. | tracked |
| `docs/reader_format_dry_run.md` | Local Phase 8 HTML/EPUB/DOCX reader-format dry-run summary, PDF probe, artifact snapshot paths, review status, and non-release boundary. | tracked |
| `docs/reader_artifact_layout_review.md` | Representative local EPUB/DOCX/PDF/HTML spot-check notes for ignored reader-format snapshots, with residuals before any release artifact can be approved. | tracked |
| `docs/evidence_transition_pilot.md` | Phase 3 evidence-transition summary, recording twenty-six no-change support-state decisions plus the separate bounded registry-runner, costed-route/resource-budget, and Circle external receipt transitions. | tracked |
| `docs/first_measured_replayed_slice.md` | Accepted measured/replayed slice ledger: a narrow `synthetic-test-backed` repository-infrastructure transition, a bounded non-infrastructure costed-route/resource-budget transition, and a bounded `prototype-backed` Circle external receipt transition, with non-claims. | tracked |
| `docs/non_core_evidence_ledger.md` | Public trust-surface ledger for the three accepted non-core upward transitions and the explicit no-chapter-core-promotion boundary, validated against the transition records. | tracked |
| `docs/costed_route_resource_slice.md` | First bounded non-infrastructure measured/replayed slice for costed-route/resource-budget selector discipline. | tracked |
| `docs/circle_external_receipt_slice.md` | First bounded imported external prototype receipt slice for a local Circle rope contract replay. | tracked |
| `docs/circle_public_replay_consumer_gate.md` | Public ASI-side Circle consumer-gate fixture, digest check, and mutation-control record for guarded proof-contract receipt use. | tracked |
| `docs/theseus_report_import_slice.md` | First public-safe Project Theseus static architecture-gate report import, CI-verifiable by digest and negative controls without chapter-core promotion. | tracked |
| `docs/core_claim_transition_coverage.md` | Generated Phase 3 coverage report proving all 54 chapter core claims have either an accepted transition record or an accepted no-promotion decision. | tracked |
| `docs/architecture_red_team_review.md` | Phase 7A architecture-level desk red-team covering authority escalation, context leakage, evaluator capture, support-state inflation, benchmark gaming, and reader-release laundering. | tracked |
| `docs/release_reproducibility.md` | Phase 7 candidate toolchain, citation, locale, font, and release-artifact boundary, including pinned CI versions and DOI-pending status. | tracked |
| `docs/public_site_accessibility_review.md` | Phase 7 accessibility-readiness ledger for the live site, including assistive hooks, diagram text equivalents, residuals, and non-claims. | tracked |
| `docs/v1_progress_ledger.md` | Compact v1.0 progress ledger for phase status, release classification, and remaining blockers. | tracked |
| `docs/v1_0_release_gate_audit.md` | Gate-by-gate v1.0 Definition-of-Done audit, evidence refs, residuals, and final-release boundary. | tracked |
| `docs/proof_adequacy_review.md` | Phase 4 proof adequacy review classifying all 112 Lean targets by what they do and do not justify. | tracked |
| `docs/proof_depth_classification.md` | Generated Phase 4 proof-shape report classifying Lean theorem declarations as direct/projection-style, derived/decomposed, or unknown/mixed. | tracked |
| `docs/protocol_record_crosswalk.md` | Generated Phase 5A report reconciling v1-critical schemas, fixtures, harnesses, Appendix E markers, chapters, and Lean abstractions. | tracked |
| `docs/claim_ledger_revision_harness.md` | Phase 5 claim-ledger revision harness summary, command, local result, and non-claim boundary. | tracked |
| `docs/proof_carrying_claim_harness.md` | Phase 5 proof-carrying claim harness summary, command, local result, and non-claim boundary. | tracked |
| `docs/tribunal_review_harness.md` | Phase 5 tribunal review harness summary, command, local result, and non-claim boundary. | tracked |
| `docs/value_conflict_harness.md` | Phase 5 value conflict harness summary, command, local result, and non-claim boundary. | tracked |
| `docs/constitutional_alignment_harness.md` | Phase 5 constitutional alignment harness summary, command, local result, and non-claim boundary. | tracked |
| `docs/governance_rights_harness.md` | Phase 5 governance rights harness summary, command, local result, and non-claim boundary. | tracked |
| `docs/agency_rights_harness.md` | Phase 5 agency rights harness summary, command, local result, and non-claim boundary. | tracked |
| `docs/support_state_transition_harness.md` | Phase 5 support-state transition harness summary, command, local result, and non-claim boundary. | tracked |
| `docs/authority_transition_harness.md` | Phase 5 authority transition harness summary, command, local result, and non-claim boundary. | tracked |
| `docs/security_kernel_harness.md` | Phase 5 security kernel harness summary, command, local result, and non-claim boundary. | tracked |
| `docs/stable_capability_field_harness.md` | Phase 5 stable capability fields harness summary, command, local result, and non-claim boundary. | tracked |
| `docs/capability_replacement_harness.md` | Phase 5 capability replacement harness summary, command, local result, and non-claim boundary. | tracked |
| `docs/self_improvement_boundary_harness.md` | Phase 5 self-improvement transition-boundary harness summary, command, local result, and non-claim boundary. | tracked |
| `docs/plan_execution_contract_harness.md` | Phase 5 plan-execution contract harness summary, command, local result, and non-claim boundary. | tracked |
| `docs/runtime_adapter_permission_harness.md` | Phase 5 runtime adapter permission harness summary, command, local result, and non-claim boundary. | tracked |
| `docs/context_admission_adequacy_harness.md` | Phase 5 context admission/adequacy harness summary, command, local result, and non-claim boundary. | tracked |
| `docs/readiness_residual_harness.md` | Phase 5 readiness/residual gate harness summary, command, local result, and non-claim boundary. | tracked |
| `docs/benchmark_antigoodhart_harness.md` | Phase 5 benchmark anti-Goodhart harness summary, command, local result, and non-claim boundary. | tracked |
| `docs/resource_budget_ledger_harness.md` | Phase 5 resource-budget ledger harness summary, command, local result, and non-claim boundary. | tracked |
| `docs/capacity_smoothing_harness.md` | Phase 5 capacity-smoothing toy harness summary, command, local result, and non-claim boundary. | tracked |
| `docs/phase5_harness_registry.md` | Registry and traceability contract for the initial Phase 5 harness set. | tracked |
| `docs/phase5_harness_runner.md` | Registry-driven local execution report for the Phase 5 harness suite. | tracked |
| `docs/external_literature_backfill_phase6.md` | Phase 6 initial external-literature backfill report for alignment/control and governance/evaluation records. | tracked |
| `docs/external_sota_positioning_audit.md` | Generated Phase 6 audit of which chapters already position against external baselines before Source crosswalk and which still need prose or exceptions. | tracked |
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
| `editions/reader_manuscript/` | Drafting curated reader-manuscript manifest, curation contract, synced chapter review matrix, artifact-inspection manifest, PDF probe manifest, companion-note routing manifest, drafting companion-note directory, reconciliation report, and source area for a human-prose derivative that remains subordinate to the live book. | tracked |
| `release_records/2026-06-29-v1-reader-html-855dc277.json` | Edition release record for the reviewed local generated reader HTML artifact from source tag `v1.0.0-reader-html-source`; EPUB, DOCX, PDF, e-reader, and audio artifacts remain unapproved. | tracked |
| `scripts/init_curated_reader_chapter.py` | Dry-run-first helper for initializing future curated reader chapter records and starter files from the generated reader baseline when overlays become too small. | tracked |
| `scripts/validate_defended_contribution_prior_art.py` | Validator for defended-contribution prior-art positioning, source-note coverage, public references, and no-novelty/no-promotion boundaries. | tracked |
| `scripts/validate_evidence_laundering_case_studies.py` | Validator for evidence-laundering no-promotion case studies, referenced evidence boundary files, public references, and the remaining demotion/refutation gap. | tracked |
| `scripts/validate_chapter_consolidation_sequence.py` | Validator for the full governed consolidation sequence, public-surface references, no-manifest-edit boundary, and current 54-chapter manifest preservation. | tracked |
| `assets/reader-overlays.html` | Generated embedded reader-overlay payload for live Human view. | tracked; regenerate from overlays |
| `sources/source_inventory.json` | Public-safe source metadata inventory. | tracked |
| `sources/cache/cache_manifest.json` | Public-safe cache metadata and hashes. | tracked |
| `sources/raw/` | Local raw source exports. | ignored |
| `sources/inbox/` | Local source drop area, including private or conversation-mined packets before public-safe synthesis. | ignored except README |
| `sources/source_notes/` | Public-safe notes created after source text is actually read. | tracked when notes are added |
| `proofs/` | Proof plans and generated proof target manifest. | tracked |
| `lean/` | Lean 4 proof workspace. | tracked except `.lake/` |
| `protocols/` | Structured protocol-record crosswalk manifests for schema/fixture/harness/Lean reconciliation. | tracked |
| `claim_decisions/` | Structured release-gate decision ledgers for explicit no-promotion or non-transition decisions that are not evidence-transition records. | tracked |
| `evidence_transitions/v1_0_pilot/` | No-change evidence-transition records for reviewed chapter/book claims that remain at `argument`. | tracked |
| `evidence_transitions/v1_0_measured/` | Accepted bounded measured/replayed evidence-transition records for the Phase 5 registry-runner infrastructure claim, the costed-route/resource-budget selector slice, and the Circle external rope receipt slice. The Project Theseus static report import is intentionally not an accepted support-state transition. | tracked |
| `schemas/` | JSON Schemas for protocol records and the book-structure manifest contract. | tracked |
| `release_records/` | Public-safe live-book and future major-version edition release records checked against release-record schemas. | tracked |
| `evidence_transitions/` | Evidence-transition review records checked against `schemas/evidence_transition_record.schema.json`. | tracked |
| `experiments/` | Synthetic experiment and benchmark harness workspace, including claim-ledger revision, proof-carrying claim, tribunal review, value conflict, constitutional alignment, governance rights, agency rights, support-state, authority, security-kernel, stable-capability-field, capability-replacement, self-improvement-boundary, plan-execution, runtime-adapter, context-admission, readiness/residual, benchmark anti-Goodhart, generation-mode baseline, resource-budget ledger, capacity-smoothing, costed-route/resource-budget slice fixtures and result records, Circle external receipt public-safe result records, Circle public consumer-gate fixtures and result record, Project Theseus static report import fixtures and result record, and the Phase 5 harness registry. | tracked |
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
- Edit `editions/release_profiles.json` for edition policy, then run `python3 scripts/validate_release_profiles.py`, `python3 scripts/sync_reader_overlay_asset.py --check`, `python3 scripts/validate_reading_mode_toggle.py`, `python3 scripts/validate_human_reading_paths.py`, `python3 scripts/build_reader_edition.py --check`, `python3 scripts/validate_reader_overlays.py --check`, `python3 scripts/validate_reader_evidence_boundaries.py --check`, `python3 scripts/validate_reader_spine.py --check`, `python3 scripts/render_reader_formats.py --check`, `node scripts/validate_reader_html_artifact_browser.js --strict` after generating HTML artifacts for full reader-HTML review, and `python3 scripts/build_audio_script.py --check` when the audio path is affected.
- Run `python3 scripts/audit_reader_continuity.py --write` after reader prose, overlay, or strip-policy changes that affect the generated reader manuscript, then validate with `python3 scripts/audit_reader_continuity.py --check`.
- Edit `editions/reader_manuscript/v1_0/manifest.json`, `editions/reader_manuscript/v1_0/curation_contract.json`, `editions/reader_manuscript/v1_0/artifact_inspection_manifest.json`, `editions/reader_manuscript/v1_0/epub_probe_manifest.json`, `editions/reader_manuscript/v1_0/docx_probe_manifest.json`, `editions/reader_manuscript/v1_0/pdf_probe_manifest.json`, `editions/reader_manuscript/v1_0/companion_note_routing.json`, or files under `editions/reader_manuscript/v1_0/companion_notes/` only when reader-manuscript status, curated-source policy, artifact-inspection evidence, EPUB probe evidence, DOCX probe evidence, PDF probe evidence, companion-note routing, or drafting companion-note treatment changes, then run `python3 scripts/validate_reader_manuscript_manifest.py`, `python3 scripts/validate_reader_artifact_inspection_manifest.py`, `python3 scripts/validate_reader_epub_probe_manifest.py`, `python3 scripts/validate_reader_docx_probe_manifest.py`, and `python3 scripts/validate_reader_pdf_probe_manifest.py` as applicable.
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
