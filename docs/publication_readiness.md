# Publication Readiness

Last audited: 2026-06-30

This file tracks whether the public repository is ready for continued public
v1.x work after the tagged v1.0.0 release. The current snapshot is summarized
in `docs/v1_0_candidate_status.md`.

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
- The release-edition plan exists at `docs/release_editions_plan.md`, with public appendix coverage in `appendices/J_release_editions.qmd`.
- The major-version release ladder exists at `docs/major_version_release_runbook.md` so live/research, reader, e-reader/document, and audio artifacts have an explicit sequence.
- The current v1.0.0 release status snapshot exists at `docs/v1_0_candidate_status.md`.
- The post-v1.0.0 v1.x roadmap exists at `docs/v1_x_beyond_sota_roadmap.md`, separating future evidence depth, safety-critical Lean proof work, Project Theseus/Circle replay lanes, curated human-reader prose, and artifact-release quality from the already tagged living-book release boundary. The A+ quality scorecard exists at `docs/a_plus_quality_scorecard.md` so the next work can target cold-read legibility, defended contribution tracks, and evidence depth directly. The 48-chapter evidence-lane backlog now lives separately at `docs/per_chapter_evidence_plan.md` and is explicitly a menu for selecting 5-8 high-payoff lanes, not a checklist for a shallow full-book fixture sweep. The governed consolidation sequence exists at `docs/chapter_consolidation_sequence.md`; `scripts/validate_chapter_consolidation_sequence.py` preserves the full 54-to-44/47 candidate map, chapter-ownership rubric, consolidation state model, executed Part I state, executed conservative compression merge, executed intent/contracts merge, executed MoECOT runtime fold, executed simulation-fidelity fold, remaining package gates, and no-support-state boundary as planning guidance. The Part I pilot, conservative compression merge, intent/contracts merge, MoECOT runtime fold, and simulation-fidelity fold have executed with retired-URL historical stubs and archived source manuscripts under `docs/chapter_consolidation_url_history_policy.md`; their dry-run and destination-draft files remain historical review artifacts, not active manifest instructions. Historical executed-package artifacts include `docs/chapter_consolidation_dry_run_compression.md`, `docs/chapter_consolidation_destination_draft_compression.md`, `docs/chapter_consolidation_dry_run_intent_contracts.md`, `docs/chapter_consolidation_destination_draft_intent_contracts.md`, `docs/chapter_consolidation_fold_moecot_runtime.md`, and `docs/chapter_consolidation_fold_simulation_fidelity.md`. `docs/chapter_consolidation_dry_run_context_abi.md`, `docs/chapter_consolidation_destination_draft_context_abi.md`, `docs/chapter_consolidation_dry_run_verification_review.md`, `docs/chapter_consolidation_destination_draft_verification_review.md`, `docs/chapter_consolidation_dry_run_planning_dag.md`, and `docs/chapter_consolidation_destination_draft_planning_dag.md` make the remaining static context ABI, verification/adversarial-review, and planning/DAG-control packages review-ready without authorizing any manifest merge. `docs/chapter_consolidation_fold_semantic_representation.md` keeps the remaining semantic-representation fold candidate decision-gated before any manifest edit. `docs/chapter_consolidation_full_review_packet.md` gives reviewers one full decision-queue surface for those remaining review-ready packages and fold dispositions without creating accepted review input, artifact approval, support-state movement, or manifest authorization. `docs/chapter_consolidation_release_stability_review.md` records a `deferred_for_release` reader-work outcome for the remaining unexecuted packages in the current reader-curation cycle without executing additional merges, changing support states, creating external review, or approving reader release artifacts.
- The defended contribution selection record exists at `docs/defended_contribution_tracks.md`; `scripts/validate_defended_contribution_tracks.py` checks five selected tracks, three deep-work tracks, active evidence-cycle lane anchors, and no chapter-core promotion.
- The defended contribution prior-art positioning record exists at `docs/defended_contribution_prior_art_positioning.md`; `scripts/validate_defended_contribution_prior_art.py` checks that all five selected tracks are positioned against source-noted external comparators while preserving that the record is not exhaustive literature review, novelty proof, external review, evidence creation, or support-state movement.
- The evidence-laundering prevention case-study record exists at `docs/evidence_laundering_prevention_case_studies.md`; `scripts/validate_evidence_laundering_case_studies.py` checks three live no-promotion examples and preserves that no true demotion/refutation case, external review, or support-state movement is claimed.
- The current v1.0.0 reproducibility and citation note exists at `docs/release_reproducibility.md`; `CITATION.cff` records version `1.0.0`, DOI-pending status, tag `v1.0.0`, source commit `96d0ca3c6b62f3530202535573941b1f6e50a83d`, and the public site/repository citation path; `scripts/validate_release_reproducibility.py` checks the pinned CI Quarto/Python/Node setup, Lean toolchain reference, locale notes, tag facts, and non-release artifact boundary.
- The Phase 7 public-site accessibility readiness record exists at `docs/public_site_accessibility_review.md`, and the compact phase progress ledger exists at `docs/v1_progress_ledger.md`; `scripts/validate_public_site_accessibility.py` checks the assistive reading-mode hooks, focus/containment CSS, landing-image alt text, diagram walkthrough coverage, residuals, and non-claims without claiming WCAG conformance or reader-artifact approval.
- The v1.0 release-gate audit exists at `docs/v1_0_release_gate_audit.md`; `scripts/validate_v1_release_gate_audit.py` checks all eleven Definition-of-Done gates, their evidence references, tag `v1.0.0`, source commit, GitHub Release, living-book release record, DOI-pending state, and non-claims without creating a DOI, archive, additional artifact approval, or support-state promotion.
- The non-core evidence ledger exists at `docs/non_core_evidence_ledger.md`; `scripts/validate_non_core_evidence_ledger.py` checks that the three accepted non-core upward transitions are visible, that all 48 chapter core claims remain at `argument`, and that README, landing page, and Appendix C point readers to the no-promotion boundary.
- The external review packet and status ledger exist at `docs/external_review_packet.md` and `docs/external_review_status.md`; `scripts/validate_external_review_status.py` checks that public review is requested through GitHub issue #1 while preserving that no independent external review has been accepted as evidence, support-state promotion, or artifact approval. `external_reviews/request_updates/consolidation_review_request_2026-06-29.json`, `external_reviews/request_updates/full_consolidation_review_request_2026-06-29.json`, and `scripts/validate_external_review_intake.py` preserve the supplemental consolidation-review issue comments as request updates only, not accepted reviews, merge/fold authorization, or support-state movement.
- The chapter external-grounding status ledger exists at `docs/chapter_external_grounding_status.md`; `scripts/validate_chapter_external_grounding_status.py` checks all 48 manifest chapters against source-noted external records, explicit external-baseline exceptions, and first-pass Corben/local source-mining queues without claiming exhaustive literature coverage, reproduced external results, or support-state promotion.
- The Circle external receipt slice exists at `docs/circle_external_receipt_slice.md`; `scripts/validate_circle_external_receipt_slice.py` checks the tracked public-safe result summary and evidence-transition record for the bounded `circle-calculus.external_rope_receipt_replay` prototype-backed transition without rerunning the external checkout or promoting chapter core claims.
- Audience-specific release profiles and content-layer contracts exist in `editions/release_profiles.json` for the live book, research release, reader release, and audio release.
- `scripts/build_reader_edition.py` can derive a cleaned reader-edition Quarto source tree, `reader_manifest.json`, `READER_RELEASE_CHECKLIST.md`, `companion_notes.md`, and `reader_delta_report.md` under ignored `build/`; `editions/reader_overlays/` holds the tracked semantic reader-overlay source for major-version human-edition deltas while `reader_delta_report.md` is generated review output with a zero-active-operation note or operation digests and before/after excerpts; `editions/reader_manuscript/v1_0/chapter_review_matrix.json` and `docs/reader_chapter_review_matrix.md` track the manifest-synced 48-chapter human-reader review queue and release blockers; `editions/reader_manuscript/v1_0/companion_note_routing.json` and `docs/reader_companion_note_routing_review.md` track companion-note routing for the three dense proof/governance chapters, and `editions/reader_manuscript/v1_0/companion_notes/` now contains drafting notes for those chapters without release approval; `scripts/sync_reader_overlay_asset.py` embeds active overlays in `assets/reader-overlays.html` for the live Human view; `scripts/validate_reader_overlays.py` validates that overlay layer and generated delta report; `scripts/sync_reader_chapter_review_matrix.py --check` validates the reader-review matrix; `scripts/validate_reader_manuscript_manifest.py` validates the curated-manuscript and companion-routing controls; `scripts/validate_release_profiles.py` validates profile definitions; `scripts/validate_human_reading_paths.py` checks one Human Reading Path bridge per manifest chapter and generated-reader retention; `scripts/validate_reader_evidence_boundaries.py` checks that generated reader chapters strip raw live core-claim markers and repeated support boilerplate while preserving claim text and an inline plain-language support-state boundary; `scripts/validate_reader_spine.py` checks that the generated human-reader spine remains substantial, structurally complete, free of repeated evidence-boundary paragraph openers, and section-by-section prose-bearing after live-only scaffolding is stripped; `scripts/validate_reading_mode_toggle.py` checks the persistent toggle, shareable `?view=` parameter, live-TOC hiding, section-number hiding, raw claim-marker hiding, support-boilerplate hiding, reader-overlay payload, runtime overlay-count hooks, and assistive-status contract; `scripts/validate_live_human_view.py` checks the rendered GitHub Pages book surface after HTML render; and `scripts/validate_live_human_view_browser.js --all-chapters --all-viewports` can exercise every manifest chapter across desktop and mobile viewports in a real browser when Playwright/Chrome is available, including rendered Mermaid visibility, raw marker and support-boilerplate hiding/restoration, reader-overlay runtime operation-count processing, reading-mode control visibility, and page-overflow checks.
- `scripts/render_reader_formats.py` can attempt selected reader-edition HTML/EPUB/DOCX/PDF renders, snapshot successful outputs under ignored `build/reader_edition/format_artifacts/`, and record actual local outcomes in `reader_render_report.json` without implying publication. `scripts/inspect_reader_format_artifacts.py` can structurally inspect local HTML/EPUB/DOCX snapshots without approving them for release, including EPUB OPF language metadata. `docs/reader_format_dry_run.md` records the local HTML/EPUB/DOCX dry-run, structural-inspection summary, EPUB metadata/source-spine probe, DOCX LibreOffice conversion probe, and PDF probe.
- `scripts/build_audio_script.py` can derive an audio-script review workspace, `audio_manifest.json`, `AUDIO_RELEASE_CHECKLIST.md`, `companion_notes.md`, `chapter_markers.md`, pronunciation glossary, and proof/equation reading rules under ignored `build/` without claiming audio exists; its check also verifies that generated chapter scripts retain both implementation-horizon sections and that the proof/equation rules preserve scoped evidence narration. `docs/reader_audio_script_probe_manifest.md` records the current tracked audio-script probe facts while preserving all audio release blockers.
- Future major-version research, reader, and audio releases have a dedicated public-safe record schema at `schemas/edition_release_record.schema.json`.
- Major-version human-consumption bundles now have explicit reader-format, optional e-reader conversion, audio artifact, and audio-embedded EPUB gates in `editions/release_profiles.json`, generated manifests, and edition release records.
- Every chapter has stable `lean:*` proof targets in the outline.
- `proofs/proof_manifest.json` is generated from the outline.
- `docs/proof_artifact_audit.md` records the current proof artifact traceability audit across all 112 proof targets.
- `docs/source_evidence_audit.md` records the current public-safe source evidence audit: 441 assigned source/chapter pairs, 441 exact claim-source mappings, complete source-note/chapter-listing coverage, and 441 passage-reviewed mappings recorded.
- Source metadata is tracked without publishing raw source exports.
- Source readiness is tracked in `docs/source_readiness_report.md`.
- Source notes exist for all currently assigned source records, and connector-readiness metadata remains tracked for authenticated source routes.
- Every assigned source/chapter pair is explicitly listed in the corresponding source note, and every core claim now has an exact source-note mapping in Appendix C.
- Appendix C now records exact source-note mappings for all 48 core claims without promoting support states.
- Appendix C now includes a generated "What would promote this" field for all 48 chapter core claims, derived from `docs/per_chapter_evidence_plan.md` and checked by `scripts/validate_core_claim_promotion_paths.py`; this is a reviewer-facing burden-of-proof field, not a support-state change.
- All 48 chapters have manuscript drafts from the source-of-truth manifest and hand drafting passes, kept at conservative support states.
- All 48 chapters have `.asi-human-only` Human Reading Path bridges that are hidden from default AI view, visible as unheaded lead-in prose in live Human view, omitted from the page TOC, and unwrapped without the source-only heading into generated reader editions. Generated reader chapters now retain manifest titles as their opening heading.
- `scripts/draft_v02_from_manifest.py` records the repeatable v0.2 baseline drafting pass.
- Per-chapter DoD, source-note, proof-readiness, and repeated-prose validators are wired into `scripts/validate_book.py`.
- The Lean toolchain is pinned and CI builds the Lean workspace.
- The GitHub Pages workflow runs the expanded live-book gate before deployment: generated-scaffold freshness, chapter DoD, outline/manifest consistency, implementation-horizon consistency, reading-mode toggle, Human Reading Path, source-appendix ownership, v1.0 status snapshot freshness, reader-spine, reader-edition, reader-format setup, audio-script setup, visual coverage, proof/source audits, schemas, protocol fixtures, repeated-prose, Lean, Quarto render, and rendered live Human-view validation.
- Generated and curated appendices exist for source matrix, claim/evidence matrix, protocol schemas, test specs, changelog, Corben-authored/supplied/local sources, external literature by other authors, lineage, release editions, and implementation horizons.
- JSON schemas, protocol example fixtures, public release records, and the Lean workspace have local validation commands.
- A public-surface audit has removed stale generated-placeholder language from live chapters and future scaffold defaults.
- GitHub issue templates and PR template exist for source, chapter, evidence, proof/code, and site work.

## Known Residuals After v1.0.0

- Source-derived support still requires claim-to-mechanism reconciliation and an accepted evidence transition after passage review; complete passage-reviewed mapping coverage alone remains insufficient for support-state promotion.
- Newly added or previously unassigned sources still require source notes and chapter assignment before they can be used as source-derived support.
- Authenticated connector access succeeded for `vcm_editable`, `moecot`, `coherence_exchange`, `talos_md`, `moecot_md`, `road_to_agi`, and `coilmoecot`, but durable raw cache exports are still local/private and not committed.
- The manifest now tracks 112 proof targets, all implemented as finite-record Lean targets. Appendix E publishes the current coverage/accounting breakdown from `proofs/proof_triage.json`, `docs/proof_artifact_audit.md` records traceability coverage, and `docs/proof_adequacy_review.md` records the first semantic adequacy classification. Most finite-record modules remain useful but too narrow and do not prove broad system behavior.
- Twenty-one synthetic or deterministic behavior/accounting harnesses are wired into validation and registry-checked, including claim-ledger revision, proof-carrying claim, tribunal-review discipline, value-conflict discipline, constitutional-predicate discipline, governance-right discipline, agency-right checklist discipline, security-kernel receipt discipline, stable-capability-field qualification/routing discipline, replacement-transaction discipline, and self-improvement transition discipline. The first bounded non-infrastructure measured/replayed slice validates a synthetic costed-route/resource-budget selector with baseline, negative control, residual, fallback, and non-claim boundaries; the first bounded imported external-prototype slice records a Circle rope-contract receipt replay from a clean local checkout. Most chapter-level Codex tests remain planned, synthetic, or not yet replayed as empirical/prototype runs, and no chapter core claim is promoted by either slice.
- External literature queue is explicit in `docs/external_literature_queue.md`; the current fast-generation set and initial policy-optimization/RL set now have source records, source notes, and primary arXiv citation metadata. Other external areas remain queued before source-derived or external-literature-backed use.
- Phase 6 external-positioning is now machine-tracked in `docs/external_sota_positioning_audit.md`: 48 of 48 chapters currently have in-prose `ext_*` positioning before Source crosswalk, 0 have explicit external-baseline exceptions, and 0 rows remain open under the stricter placement release gate. This closes the current placement gate only; it does not claim exhaustive literature synthesis, reproduced external results, or support-state promotion.
- The generated chapter external-grounding status ledger currently has 48 source-noted chapters, 0 explicit exceptions, 0 candidate-backlog rows, and 0 missing audit rows. It is a routing surface for future source mining and chapter writing, not an external-literature-backed support-state transition.
- The chapters have received broad coherence, transition, Human-view, and generated-reader chapter-text review passes, and the three companion-note candidate chapters now have tracked reader/e-reader/audio routing decisions. The book still needs claim-to-mechanism support review and accepted evidence transitions before chapter core claims can rise above `argument`. The reader chapter review matrix now has all 48 current chapters at reviewed chapter-text status, but release-record and format-artifact blockers remain on every row.
- Reader, research, PDF, EPUB, DOCX, AZW3, MOBI, and audio editions are planned and scaffolded. Local HTML/EPUB/DOCX dry-run snapshots now exist with structural inspection for review, `docs/reader_html_artifact_browser_review.md` records a full local browser review of the generated reader HTML snapshot across 118 page-view pairs, `release_records/2026-06-29-v1-reader-html-855dc277.json` records the reviewed local HTML snapshot from source tag `v1.0.0-reader-html-source`, `docs/reader_epub_probe_manifest.md` records `en-US` EPUB metadata plus sampled source-spine entries while preserving the e-reader blocker, `docs/reader_docx_probe_manifest.md` records a 514-page LibreOffice conversion probe for the generated DOCX, an isolated PDF probe renders when `LANG` and `LC_ALL` are set to `en_US.UTF-8`, `docs/reader_pdf_probe_manifest.md` records the current 535-page PDF probe and sampled source-card appendix pages, and `docs/reader_audio_script_probe_manifest.md` records the current 54-file audio-script review-workspace probe with MP3/M4B/audio-embedded EPUB targets still not generated. The reviewed local HTML snapshot is the only release-approved reader artifact; EPUB, DOCX, PDF, e-reader, and audio artifacts still need their own full application/layout/audio review before they can be reported as release artifacts.
- Public-site accessibility readiness is now recorded, but no full keyboard-only walkthrough, screen-reader pass, measured contrast audit, EPUB e-reader application review, DOCX application review, or PDF page-by-page layout review has been recorded.
- `CITATION.cff` is v1.0.0 metadata. DOI/Zenodo remains pending until an archive exists; the v1.0.0 living-book release record explicitly preserves DOI pending.

## Manuscript Maintenance Checklist

Before claiming the public book is current:

- Run `python3 scripts/sync_scaffold.py`.
- Run `python3 scripts/sync_proof_manifest.py`.
- Run `python3 scripts/validate_chapter_dod.py`.
- Run `python3 scripts/validate_proof_artifact_audit.py`.
- Run `python3 scripts/validate_source_evidence_audit.py`.
- Run `python3 scripts/validate_release_reproducibility.py`.
- Run `python3 scripts/validate_public_site_accessibility.py`.
- Run `python3 scripts/validate_v1_release_gate_audit.py`.
- Run `python3 scripts/validate_circle_external_receipt_slice.py`.
- Run `python3 scripts/validate_non_core_evidence_ledger.py`.
- Run `python3 scripts/validate_external_review_status.py`.
- Run `python3 scripts/validate_external_review_intake.py`.
- Run `python3 scripts/validate_chapter_consolidation_sequence.py`.
- Run `python3 scripts/validate_defended_contribution_prior_art.py`.
- Run `python3 scripts/validate_evidence_laundering_case_studies.py`.
- Run `python3 scripts/validate_core_claim_promotion_paths.py`.
- Run `python3 scripts/validate_chapter_external_grounding_status.py`.
- Run `python3 scripts/validate_external_sota_positioning.py`.
- Run `python3 scripts/validate_publication.py`.
- Run `python3 scripts/validate_release_profiles.py`.
- Run `python3 scripts/build_reader_edition.py --check`.
- Run `python3 scripts/sync_reader_overlay_asset.py --check`.
- Run `python3 scripts/validate_reader_overlays.py --check`.
- Run `python3 scripts/sync_reader_chapter_review_matrix.py --check`.
- Run `python3 scripts/validate_human_reading_paths.py`.
- Run `python3 scripts/validate_source_appendices.py`.
- Run `python3 scripts/validate_v1_status_snapshot.py`.
- Run `python3 scripts/validate_outline_consistency.py`.
- Run `python3 scripts/validate_implementation_horizons.py`.
- Run `python3 scripts/validate_reader_evidence_boundaries.py --check`.
- Run `python3 scripts/validate_reader_spine.py --check`.
- Run `python3 scripts/validate_claim_ledger_revision.py`.
- Run `python3 scripts/validate_proof_carrying_claims.py`.
- Run `python3 scripts/validate_tribunal_review.py`.
- Run `python3 scripts/validate_value_conflicts.py`.
- Run `python3 scripts/validate_constitutional_alignment.py`.
- Run `python3 scripts/validate_governance_rights.py`.
- Run `python3 scripts/validate_agency_rights.py`.
- Run `python3 scripts/validate_security_kernel.py`.
- Run `python3 scripts/validate_stable_capability_fields.py`.
- Run `python3 scripts/validate_capability_replacement.py`.
- Run `python3 scripts/validate_self_improvement_boundaries.py`.
- Run `python3 scripts/render_reader_formats.py --check`.
- Run `python3 scripts/build_audio_script.py --check` when preparing an audio script or checking the full edition path.
- Run `python3 scripts/validate_book.py`.
- Run `python3 scripts/validate_visual_coverage.py`.
- Run `python3 scripts/validate_schemas.py`.
- Run `python3 scripts/validate_protocol_examples.py`.
- Run `python3 scripts/validate_repeated_prose.py`.
- Run `(cd lean && lake build)`.
- Run `quarto render --to html`.
- Run `python3 scripts/validate_live_human_view.py`.
- Run `node scripts/validate_live_human_view_browser.js --all-chapters --all-viewports`.
- Confirm no raw source exports are staged.

## Definition of Presentable Public State

The public repository is presentable when:

- README explains the project, status, source discipline, proof discipline, and validation path.
- Contributor and rights files are present.
- GitHub metadata points to the live site.
- GitHub Pages workflow passes.
- Reproducibility and citation metadata identify the exact candidate or release status without claiming a DOI, tag, artifact, or evidence transition that does not exist.
- Rendered site links are live.
- Validation scripts pass locally.
- Edition profiles validate, the reader-edition derivation check passes, the reader-spine check passes, and the rendered whole-book live Human view check passes.
- Human Reading Path coverage validates for every manifest chapter and generated reader chapter.
- Reader evidence-boundary validation proves generated reader chapters keep core-claim support states visible.
- Implementation horizons validate for every manifest chapter and generated Appendix K row.
- The working tree is clean after commit and push.
