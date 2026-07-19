# The ASI Stack

**The ASI Stack: A Governed Systems Architecture for Advanced AI, with ASI as the Stress Case** is Corben Sorenson's living technical book about AI systems architecture.

Public book site: <https://corbensorenson.github.io/asi-stack-book/>

Public repository: <https://github.com/corbensorenson/asi-stack-book>

This repository is the canonical Quarto source for the book, its scaffolding, validation scripts, schemas, Lean proof workspace, and public-safe source/evidence metadata. The book treats the source papers as fragments of one architecture: alignment, governance, planning, memory, reasoning, execution, routing, compression, evidence, and recursive self-improvement.

## Choose the product you need

| Product | Best for | Start here |
|---|---|---|
| Narrative book | A bounded 15-chapter thesis-to-method route with the research scaffolding hidden. | [Open the narrative route](https://corbensorenson.github.io/asi-stack-book/products/narrative-book/) |
| Architecture reference | Interfaces, invariants, failure routes, protocols, tests, proofs, and implementation horizons across all 55 live chapters. | [Open the architecture index](https://corbensorenson.github.io/asi-stack-book/products/architecture-reference/) |
| Evidence registry | Current commit/count state, claim support, sources, tests, proofs, releases, and residuals. | [Open the evidence registry](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/) |

The three projections share one source of truth but have different density and review contracts; see [docs/product_contracts.md](docs/product_contracts.md) and [docs/product_projection_artifacts.md](docs/product_projection_artifacts.md). The [Post-v2.3 Claim Proof, Causal Validation, and SOTA-Challenge Roadmap](docs/post_v2_3_claim_proof_and_sota_challenge_roadmap.md) is complete with an exact [terminal no-public-release record](release_records/2026-07-16-post-v2-3-claim-proof-sota-roadmap-complete-no-public-release.json). Its [Post-v2.3 Evidence Competence, Transfer, and Publication Roadmap](docs/post_v2_3_maintenance_transfer_and_publication_roadmap.md) is the sole active successor, with machine authority in [roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json](roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json), an [N0–N5 claim-bearing experiment standard](docs/claim_bearing_experiment_competence_standard.md), and a [complete accepted-transition identity crosswalk](docs/claim_identity_graph_reconciliation.md). All 115 accepted transitions now resolve through 25 exact atom, 61 bounded subclaim, and 29 proxy relations with zero indirect parent support movement. The competence contract prevents weak implementations, invalid instruments, bad proxies, or underpowered tests from becoming negative evidence about an architecture. The live working tree has 55/55 chapter-core claims at `argument`, zero chapter-core promotions, zero external reproductions, and no SOTA support; the local X synopsis source is current, but its older unpublished platform draft is stale and must be refreshed before publication. `v2.3.0` remains the latest immutable public living-book release. <!-- canonical-status:historical -->

The completed post-v2.1 roadmap remains historical authority at [docs/post_v2_1_residual_and_transfer_roadmap.md](docs/post_v2_1_residual_and_transfer_roadmap.md); it is not an active successor.

## 60-Second Trust Surface

<!-- canonical-status:generated-begin -->
_Current canonical metrics (generated from machine records): **55 manifest chapters; 319 public-safe records; 55 chapter-core claims; 55/55 chapters externally positioned; 0 promoted core claims; 115/115 accepted transitions identity-resolved (25 direct, 61 subclaim, 29 proxy; 0 parent movements).**_
<!-- canonical-status:generated-end -->

**What this is:** a public living-book research program and evidence system for governed advanced-AI systems, using ASI as the extreme stress case. The strongest current contribution is the manifest-driven, CI-validated method for keeping claims, sources, proofs, tests, reader editions, and non-claims explicit.

**What this is not:** not a validated ASI implementation, not a deployed safety system, not a benchmark-proven architecture, and not a claim that all chapter theses are externally proven.

**Auditable current state:** the inventory has 319 public-safe records; 55/55 chapters are externally positioned with 0 explicit external-baseline exceptions. All 55 chapter core claims remain at `argument`; [the core-claim disposition ledger](docs/core_claim_disposition_ledger.md) records 55 per-chapter core-claim dispositions, 22 accepted no-change transition dispositions, 33 accepted no-promotion dispositions, and 0 promoted core claims. Twenty-five narrow non-core transitions are recorded in [the non-core evidence ledger](docs/non_core_evidence_ledger.md), alongside 61 accepted `blocks_promotion` decisions and three historical `refuted` labels. The competence audit classifies all 90 accepted negative/no-change records as 1 N0, 15 N1, 74 N2, and 0 N3–N5, so no exact, broad, parent, or chapter-core refutation currently follows.

**Reader and source boundaries:** [Appendix C](appendices/C_claim_evidence_matrix.qmd) is the claim/support-state ledger. [Appendix G](appendices/G_corben_source_corpus.qmd) separates Corben-authored, Corben-supplied, and local-project sources from [Appendix H](appendices/H_external_sources.qmd), which holds external literature; external positioning is not exhaustive literature synthesis. [Novelty positioning](docs/contribution_novelty_ledger.md) is not proof of novelty. Human view is a convenience projection, not a reviewed reader-release manuscript; its current heuristic queue is in [the reader continuity audit](docs/reader_continuity_audit.md). By author decision, no external-human review or outreach is a prepublication gate; the preserved specialist packets may be used only after the author declares the book complete, and no independent review is claimed in [the review ledger](docs/external_review_status.md).

Fast audit path: [the active Evidence Competence, Transfer, and Publication Roadmap](docs/post_v2_3_maintenance_transfer_and_publication_roadmap.md), its [experiment-competence standard](docs/claim_bearing_experiment_competence_standard.md), and its machine [status](roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json); then the completed [Claim Proof, Causal Validation, and SOTA-Challenge Roadmap](docs/post_v2_3_claim_proof_and_sota_challenge_roadmap.md), its machine [status](roadmap_records/post_v2_3_claim_proof_and_sota_challenge_status.json), and [terminal record](release_records/2026-07-16-post-v2-3-claim-proof-sota-roadmap-complete-no-public-release.json); then [the v2.3.0 completion declaration](docs/v2_3_completion_declaration.md), [exact release record](release_records/2026-07-13-v2.3.0-qcsa-e2766116.json), claim ledgers, and Appendices C, G, and H. The landing-page and README trust contract is guarded by `scripts/validate_trust_surface.py`.

## Current Status

`v2.3.0` is the latest completed immutable canonical live/research HTML release, bound to tag `v2.3.0`, source commit `e27661166e9105f37cb36d63b15795f80715ca24`, hosted build/deploy runs `29234323320` and `29234640734`, and archive SHA-256 `ebb3cccb0841a15a49d7d20ee8d5c7f7dce97dac562ca05068025951274ee28c`. The completed post-v2.3 cycle adds no public version: it preserves the 54-chapter architecture, leaves all 54 chapter-core claims at `argument`, releases one exact local 54-chapter curated HTML archive under its own edition record, and retains both new model comparisons as protocol-failure `no_change` results. Historical `v1.0.0`, `v2.0.0`, `v2.1.0`, and `v2.2.0` releases remain intact. The root site and `/latest/` are mutable. <!-- canonical-status:historical -->

- Quarto book structure is initialized and renders to HTML.
- All 55 manifest chapters exist as manuscript drafts across four manifest-driven parts.
- `docs/book_outline.md` is the source of truth for the full-book drafting plan, per-part/per-chapter source queues, and Lean proof scope.
- `book_structure.json` controls parts, chapter order, stable chapter IDs, source assignments, implementation horizons, proof hooks, and appendix order, and `schemas/book_structure.schema.json` plus `scripts/validate_book.py` guard its shape.
- `_quarto.yml`, Appendix A, Appendix C, Appendix G, Appendix H, and Appendix K are generated.
- Appendix C now carries a generated "What would promote this" field for all 55 chapter core claims, derived from `docs/per_chapter_evidence_plan.md` and validated by `scripts/validate_core_claim_promotion_paths.py`, without changing any support state. `docs/core_claim_disposition_ledger.md` consolidates those per-chapter movement paths with accepted no-change transition records and accepted no-promotion decisions.
- `docs/chapter_consolidation_sequence.md` records the accepted governed consolidation sequence for the 54-to-44/47 chapter-shape critique, the executed Part I 4-to-2 pilot, the executed conservative compression merge, the executed intent/contracts merge, the executed MoECOT runtime fold, the executed simulation-fidelity fold, the executed static context ABI merge, the executed verification/adversarial-review merge, the executed planning/DAG consolidation, the executed semantic-representation fold, the historical 44-chapter consolidation snapshot, and the no-support-state-change boundary. The activation manifest had 54 chapters; the active manifest now has 55 after the distinct-interface cognitive-substrate insertion. `docs/chapter_consolidation_release_stability_review.md` records the current `deferred_for_release` reader-work outcome for remaining unexecuted consolidation packages without authorizing additional merges or folds; `scripts/validate_chapter_consolidation_sequence.py` keeps that sequence visible from the roadmap and public surfaces. <!-- canonical-status:historical -->
- `editions/release_profiles.json` defines live, research, reader, and audio release profiles plus content layers for the reader spine, live research scaffold, evidence matrices, machine contracts, release derivatives, and audio adaptation.
- `scripts/build_reader_edition.py` can derive a cleaned reader-edition Quarto source tree, `reader_manifest.json`, and `reader_delta_report.md` under ignored `build/`.
- `editions/reader_overlays/README.md` and `editions/reader_overlays/v1_0/manifest.json` define the semantic reader-overlay layer for major-version human-edition deltas that should survive regeneration without forking the live book. The current v1.0 overlay set carries 74 active operations across 30 chapters for Human view and generated reader editions only; `assets/reader-overlays.html`, `docs/reader_continuity_audit.md`, and `docs/reader_chapter_review_matrix.md` are the generated review surfaces for the exact operation set.
- `editions/reader_manuscript/v1_0/manifest.json` is the frozen historical 44-chapter curated-reader snapshot. The completed post-v2.3 cycle preserves it byte-for-byte and creates `editions/reader_manuscript/v2_0/manifest.json`, a reconciled 54-chapter successor with one exact approved local HTML archive and its own `reader_release_record.json`. That approval is not public deployment, another format, a license grant, external-human or screen-reader review, WCAG certification, or evidence movement. `scripts/validate_reader_manuscript_manifest.py` keeps curated prose subordinate to the live book's claim, evidence, proof/test, implementation, and release authority.
- `scripts/init_curated_reader_chapter.py` can initialize a future curated reader chapter record and starter file from the generated reader baseline after review decides overlays are too small. It defaults to dry-run output and keeps release blockers active when `--write` is used.
- `editions/reader_manuscript/v1_0/chapter_review_matrix.json` and `docs/reader_chapter_review_matrix.md` track the full 44-chapter human-reader review queue. `scripts/sync_reader_chapter_review_matrix.py --check` keeps chapter IDs, part order, live files, generated-reader files, and active overlay counts synced to `book_structure.json` while preserving review statuses, dispositions, companion-note candidates, curated-manuscript candidates, and release blockers.
- `editions/reader_manuscript/v1_0/companion_note_routing.json` and `docs/reader_companion_note_routing_review.md` record the current chapter-level companion-note routing for dense proof/governance chapters. `editions/reader_manuscript/v1_0/companion_notes/` now contains drafting companion notes for Circle proof receipts, executable-specification proof lanes, and artifact-steward project objects for e-reader and audio review. Generated reader and audio companion notes consume this routing manifest, but it is not a reader release, artifact approval, support-state promotion, or curated manuscript.
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
- `editions/reader_manuscript/v1_0/audio_script_probe_manifest.json`, `docs/reader_audio_script_probe_manifest.md`, and `scripts/validate_reader_audio_script_probe_manifest.py` preserve the latest local audio-script review-workspace facts from the tracked curated reader manuscript: 49 script files, implementation horizons preserved, 5 table notes, 50 Mermaid diagram notes, 11 image notes, ten key-figure spoken-summary rows routed into generated audio companion notes, pronunciation/proof reading files present, and MP3/M4B/audio-embedded EPUB targets still not generated. This is a probe record, not audiobook approval.
- `docs/reader_html_artifact_browser_review.md` and `scripts/validate_reader_html_artifact_browser.js` record the first full local browser artifact review for generated reader HTML: 59 pages opened at desktop and mobile widths, 118 page-view pairs passed, 0 failures, and an exact ignored-snapshot directory digest. `release_records/2026-06-29-v1-reader-html-855dc277.json` now names that exact local HTML snapshot from source tag `v1.0.0-reader-html-source`, so the HTML format row is release-approved for that local artifact only. EPUB, DOCX, PDF, e-reader, audio, and audio-embedded EPUB artifacts remain unapproved.
- `scripts/build_reader_edition.py` and `scripts/build_audio_script.py` now emit generated review checklists and companion notes so major-version reader, e-reader, and audio work stay downstream of the living book instead of becoming parallel manuscripts.
- `scripts/build_audio_script.py` can derive an audio-script review workspace, `audio_manifest.json`, chapter markers, an audio checklist, audio companion notes with the ten tracked key-figure spoken summaries, pronunciation glossary, and proof/equation reading rules under ignored `build/`; its check also verifies that chapter scripts preserve both implementation-horizon sections and that proof/equation narration rules exist.
- The current harness inventory is recorded in `docs/v1_0_candidate_status.md` and Appendix E rather than hand-maintained in this README. `experiments/phase5_harness_registry.json` plus `scripts/validate_phase5_harness_registry.py` keep the registry-controlled harness set wired to docs, fixtures, result records, Appendix E, and book validation; chapter-specific and support checks include stack-layer traceability, artifact replay, routing leases, VCM resolver/certificate records, runtime-adapter effect and adversarial probes, typed-job durable lifecycle records, readiness lifecycle records, RankFold replay/import records, Theseus support/report-bundle checks, resource workflow/live/load probes, and living-book change-packet checks. These are executable or traceability checks over fixtures, records, and local command output, not chapter-claim promotions or deployed-runtime evidence.
- `scripts/run_phase5_harnesses.py --write-report` is the first accepted measured/replayed slice for v1.0: it replays the registered Phase 5 harness suite and records 22 of 22 summary-checked harnesses passing in `docs/phase5_harness_runner.md`. `docs/first_measured_replayed_slice.md` and `evidence_transitions/v1_0_measured/phase5_harness_runner_synthetic_test_backed.json` scope the resulting `synthetic-test-backed` transition to the repository-infrastructure claim `living-book-methodology.phase5_harness_registry_runner`; no chapter core claim, runtime claim, model-quality claim, safety claim, benchmark claim, or source-interpretation claim is promoted.
- `scripts/validate_costed_route_resource_slice.py` records the first bounded non-infrastructure measured/replayed slice: `docs/costed_route_resource_slice.md`, `experiments/costed_route_resource_slice/results/2026-06-29-local.json`, and `evidence_transitions/v1_0_measured/costed_route_resource_slice_synthetic_test_backed.json` scope a `synthetic-test-backed` transition to `resource-economics.costed_route_budget_slice`. The validator recomputes a public-safe four-route costed-route/resource-budget result, rejects a cheaper failed-verification control, rejects a cheaper hidden-residual control, keeps an adequate overkill baseline, selects the lowest-cost eligible route, and checks the finite Lean fixture in `AsiStackProofs.ResourceEconomics` against the public JSON route costs, selected route, negative controls, eligibility fields, and selector-state trace theorem; no chapter core claim, deployed routing claim, scheduler claim, model-quality claim, benchmark claim, safety claim, economic claim, or source-interpretation claim is promoted.
- `scripts/validate_resource_load_stability_probe.py` now supports a bounded `synthetic-test-backed` transition for `resource-economics.finite_burst_load_smoothing_selector`: `docs/resource_load_stability_probe.md`, `experiments/resource_load_stability_probe/results/2026-07-01-local.json`, and `evidence_transitions/v1_x_measured/resource_load_stability_selector_synthetic_test_backed.json` record a finite 10-task burst-review workload where protected capacity smoothing reduces instability from 5 units to 0, residualizes 7 deferred task-ticks, rejects a cheaper review-erasure negative control, and checks a finite `AsiStackProofs.ResourceEconomics` fixture bridge. This remains a synthetic selector claim only; no Resource Economics chapter core claim, real load-stability claim, deployed scheduler claim, TokenMana/PlanForge claim, model-quality claim, safety claim, economic claim, or source-interpretation claim is promoted.
- `scripts/validate_compact_gvr_slice.py` records a bounded Compact Generative Systems synthetic receipt slice: `docs/compact_gvr_slice.md`, `experiments/compact_gvr_slice/results/2026-07-01-local.json`, and `evidence_transitions/v1_x_measured/compact_gvr_slice_synthetic_test_backed.json` scope a `synthetic-test-backed` transition to `compact-generative-systems.compact_gvr_receipt_slice`. The validator recomputes five public-safe compact-generation receipt records, keeps a 368-byte literal baseline, selects a 78-byte exact repeat-generator-plus-repair receipt, rejects lossy exactness, negative-rate/no-fallback, and bounded-search-overrun controls, and checks the finite Lean fixture bridge in `AsiStackProofs.CompactGenerativeSystems`; no chapter core claim, deployed compression claim, codec-correctness claim, fallback-execution claim, model-quality claim, benchmark claim, safety claim, or source-interpretation claim is promoted.
- `scripts/validate_rankfold_public_safe_probe.py` records a RankFold public-safe replay probe: `docs/rankfold_public_safe_probe.md`, `experiments/rankfold_public_safe_probe/results/2026-07-02-local.json`, and `evidence_transitions/v1_x_measured/rankfold_public_safe_replay_probe_no_change.json` preserve a fresh RAW0 roundtrip-exact pack/verify/list/unpack run over a generated synthetic public-safe file plus a rejected single-byte archive mutation. The local CLI reported NeuralFold disabled by license, and the archive had no compression advantage, so this does not prove NeuralFold compression, compression advantage, RankFold codec correctness, downstream utility, fallback execution, deployed compression behavior, or chapter-core support-state promotion.
- `scripts/validate_runtime_adapter_effect_probe.py` records a Runtime adapter effect replay probe: `docs/runtime_adapter_effect_probe.md` and `experiments/runtime_adapter_effect_probe/results/2026-07-02-local.json` preserve `valid_low_impact_local_write_effect_replay`, pre/post/rollback hashes, rollback-exact temp-file restoration, `invalid_missing_permission_no_mutation`, and `invalid_expired_approval_no_mutation`. `evidence_transitions/v1_x_measured/runtime_adapter_effect_probe_no_change.json` records the accepted no-promotion decision for this probe. It records `support_state_effect=none` and does not prove deployed adapter behavior, sandbox isolation, approval-service behavior, secret-handle safety, revocation propagation, rollback-service behavior, policy-enforcement correctness, benchmark performance, or chapter-core support-state promotion.
- `scripts/validate_runtime_adapter_adversarial_boundary_probe.py` records a Runtime adapter adversarial boundary probe: `docs/runtime_adapter_adversarial_boundary_probe.md` and `experiments/runtime_adapter_adversarial_boundary/results/2026-07-02-local.json` preserve two valid synthetic adapter boundary reviews and twelve expected-invalid controls for confused-deputy parent mismatch, parent/lease authority ceiling overrun, approval scope mismatch, expired approval, sandbox escape path, secret materialization, missing rollback handle, missing effect receipt, missing audit refs, support-state promotion, and missing non-claim boundary. `evidence_transitions/v1_x_measured/runtime_adapter_adversarial_boundary_no_change.json` records the accepted no-promotion decision for this probe. It records `support_state_effect=none` and does not prove deployed adapter behavior, sandbox isolation, approval-service behavior, secret-handle safety, policy-enforcement correctness, rollback-service behavior, revocation propagation, security review, or chapter-core support-state promotion.
- `scripts/validate_partitioned_authority_fixture.py` records the cross-boundary partitioned-authority fixture: `docs/partitioned_authority_fixture.md` and `experiments/partitioned_authority/results/2026-07-03-local.json` preserve three finite hives/runtime records and six expected-invalid controls for stale-grant dispatch, mutation after unseen revocation, grant/effect race residual ownership, missing no-mutation evidence, support-state promotion, and missing non-claim boundaries. `evidence_transitions/v1_x_measured/partitioned_authority_fixture_no_change.json` records the accepted no-promotion decision for this fixture. It records `support_state_effect=none` and does not prove deployed partition tolerance, distributed consensus, availability, runtime-adapter enforcement, revocation propagation, hive scheduler behavior, rented-node sandbox behavior, family-governance behavior, network-overlay behavior, security, privacy, benchmark performance, or chapter-core support-state promotion.
- `scripts/validate_readiness_lifecycle_probe.py` records the Readiness lifecycle probe: `docs/readiness_lifecycle_probe.md` and `experiments/readiness_lifecycle_probe/results/2026-07-02-local.json` preserve six valid synthetic lifecycle transitions and twelve expected-invalid controls for non-forward jumps, missing fresh evidence, missing residual escrow, unsafe default readiness, quarantine leakage, missing terminal records, retired-state reuse, missing non-claims, and support promotion. `evidence_transitions/v1_x_measured/readiness_lifecycle_probe_no_change.json` records the accepted no-promotion decision for this probe. It records `support_state_effect=none` and does not prove deployed readiness-engine behavior, lifecycle execution, residual-ledger storage, live quarantine routing, gate-quality checks, terminal-state governance, rollback execution, runtime monitoring, MoECOT replay, benchmark performance, current module readiness, or chapter-core support-state promotion.
- `scripts/validate_artifact_steward_lifecycle_probe.py` records an Artifact steward lifecycle probe: `docs/artifact_steward_lifecycle_probe.md` and `experiments/artifact_steward_lifecycle_probe/results/2026-07-02-local.json` preserve `valid_clean_release_review_proposal`, `valid_sunset_review_route`, `invalid_tainted_event_without_review`, `invalid_over_policy_treasury_spend`, `invalid_contribution_governance_laundering`, `invalid_unscoped_federation_contract`, `invalid_release_without_gate_evidence`, and `invalid_sunset_criteria_ordinary_work`. This is a no steward-bot, treasury-executor, event-taint-workflow, contributor-ledger, governance-runner, project-federation, release-runner, sunset-protocol, or support-state-promotion claim.
- `scripts/validate_vcm_resolver_certificate_probe.py` records a VCM resolver/certificate probe: `docs/vcm_resolver_certificate_probe.md` and `experiments/vcm_resolver_certificate_probe/results/2026-07-02-local.json` preserve `valid_resolver_materialization_receipt`, `valid_mandatory_miss_typed_fault`, `invalid_address_mismatch_materialization_denied`, `invalid_version_mismatch_materialization_denied`, `invalid_snapshot_mismatch_materialization_denied`, `invalid_mount_policy_denied`, `invalid_lease_expired_reuse_blocked`, `invalid_certificate_source_binding_mismatch_denied`, `invalid_certificate_authority_escalation_denied`, `invalid_certificate_truthfulness_overclaim_denied`, and `invalid_summary_fidelity_omission_denied`. This is a no deployed-resolver, memory-store, context-compiler, open-domain-summary-fidelity, certificate-truthfulness, transaction-isolation, deletion-enforcement, model-facing-context-quality, VCM-Bench, leak-prevention, or support-state-promotion claim.
- `scripts/validate_intent_recontract_probe.py` records an Intent re-contract trigger probe: `docs/intent_recontract_probe.md` and `experiments/intent_recontract_probe/results/2026-07-02-local.json` preserve `valid_no_material_delta_continue`, `valid_publication_surface_delta_recontracts`, `invalid_authority_delta_without_recontract`, `invalid_private_source_delta_without_recontract`, `invalid_stop_condition_erasure_without_recontract`, `invalid_evidence_bar_weakening_without_recontract`, `invalid_affected_party_widening_without_recontract`, `invalid_means_expansion_without_recontract`, and `invalid_support_state_promotion_without_recontract`. This is a no natural-language-intent-understanding, deployed-parser-quality, deployed-authority-extraction, prompt-injection-containment, runtime-dispatch, approval-service, user-satisfaction, or support-state-promotion claim.
- `scripts/validate_intent_governed_replacement_bridge.py` records an Intent-governed replacement bridge: `docs/intent_governed_replacement_bridge.md` and `experiments/intent_governed_replacement_bridge/results/2026-07-02-local.json` preserve two valid synthetic bridge traces and six expected-invalid controls for command authority into replacement admission, default-without-approval blocking, authority-widening rejection, stop-condition-erasure rejection, rollback-owner requirement, and support-promotion overclaim. This is a no parser, deployed dispatcher, approval-service, replacement-execution, production-rollback, monitor-quality, regression-suite-quality, evidence-transition, or support-state-promotion claim.
- `scripts/validate_substrate_adoption_trace.py` records a Mathematical and Search Substrates adoption trace: `docs/substrate_adoption_trace.md` and `experiments/substrate_adoption_trace/results/2026-07-02-local.json` preserve four synthetic adoption states and eight expected-invalid controls for missing baselines, missing falsification, theorem spillover, unmeasured-axis routing, failed-control promotion, missing fallback, support-promotion overclaim, and missing non-claim boundaries. This is no substrate A/B test, representation-efficiency result, search/routing/compression-quality result, model-quality result, runtime result, Circle/CoilMoECOT/Mamba/TreeLLM/Theseus adoption validation, evidence transition, or support-state-promotion claim.
- `scripts/validate_artifact_graph_record_reality_sequence.py` records an Artifact Graph record-reality sequence: `docs/artifact_graph_record_reality_sequence.md` and `experiments/artifact_graph_record_reality_sequence/results/2026-07-04-local.json` preserve one stale/partial/fresh replay sequence plus four expected-invalid controls for stale-certificate support movement, restoration without fresh replay/provenance, missing non-claims, and support review without replay-validated transaction state. `evidence_transitions/v1_x_measured/artifact_record_reality_sequence_no_change.json` records the accepted no-promotion decision for this bridge. This is no deployed artifact graph, deployed replay, audit-durability, verifier-correctness, open-world receipt-faithfulness, upward-evidence-transition, or support-state-promotion claim.
- `scripts/validate_epistemic_trusted_computing_base.py` records an Artifact Graph epistemic-TCB fixture: `docs/epistemic_trusted_computing_base_fixture.md` and `experiments/epistemic_tcb/results/2026-07-03-local.json` preserve three valid finite trust-base records plus six expected-invalid controls for missing roots of trust, same-component verifier laundering, unbounded trust propagation, missing recursion stops, erased outside-TCB residuals, and support promotion from trust-base shape. `evidence_transitions/v1_x_measured/artifact_epistemic_tcb_fixture_no_change.json` records the accepted no-promotion decision for this fixture. This is no verifier-correctness, deployed trust-base, audit-log durability, policy-correctness, open-world receipt-faithfulness, upward-evidence-transition, or support-state-promotion claim.
- `scripts/validate_planning_scheduler_state_probe.py` records a Planning scheduler-state probe: `docs/planning_scheduler_state_probe.md` and `experiments/planning_scheduler_state/results/2026-07-02-local.json` preserve two valid synthetic scheduler traces and seven expected-invalid controls for blocked-node dispatch, ready-without-context dispatch, failed-adequacy route selection, conflicting merge acceptance, replanning authority erasure, accepted dependency cycles, and hidden-cost ledger erasure. `evidence_transitions/v1_x_measured/planning_scheduler_state_probe_no_change.json` records the accepted no-promotion decision for this probe. This is no deployed-planner, deployed-scheduler, decomposition-quality, context-demand-prediction, route-quality, selected-tier-adequacy, scheduler-optimality, runtime-replanning, upward-evidence-transition, or support-state-promotion claim.
- `scripts/validate_planning_runtime_replan_delta.py` records a Planning runtime-replan delta audit: `docs/planning_runtime_replan_delta_audit.md` and `experiments/planning_runtime_replan_delta/results/2026-07-02-local.json` preserve two valid synthetic runtime-replan traces and nine expected-invalid controls for authority widening, stop-condition erasure, unaffected-node rerun without dependency impact, missing residual ownership, missing context delta, missing verification delta, blocked-authority dispatch, support-promotion overclaim, and missing non-claim boundaries. `evidence_transitions/v1_x_measured/planning_runtime_replan_delta_no_change.json` records the accepted no-promotion decision for this audit. This is no deployed-planner, runtime-scheduler, decomposition-quality, context-demand-prediction, route-quality, selected-tier-adequacy, live-feedback-handling, deployed-runtime-replanning, upward-evidence-transition, or support-state-promotion claim.
- `scripts/validate_typed_job_durable_lifecycle_probe.py` records a Labor OS durable lifecycle probe: `docs/typed_job_durable_lifecycle_probe.md` and `experiments/typed_job_durable_lifecycle/results/2026-07-02-local.json` preserve two valid synthetic durable lifecycle traces and nine expected-invalid controls for retry idempotency, authority preservation, permission scope, expired-lease dispatch blocking, completion receipts, replay refs, residual ownership, non-claim boundaries, and support-promotion overclaim. `evidence_transitions/v1_x_measured/typed_job_durable_lifecycle_probe_no_change.json` records the accepted no-promotion decision for this probe. This is no deployed-scheduler, durable-workflow-recovery, permission-enforcement, approval-service, adapter-runner, completion-receipt-service, replay-correctness, upward-evidence-transition, or support-state-promotion claim.
- `scripts/validate_security_scif_commit_probe.py` records a SCIF sanitized commit replay probe: `docs/security_scif_commit_probe.md` and `experiments/security_scif_commit_probe/results/2026-07-02-local.json` preserve `valid_sanitized_commit_replay`, `valid_prompt_injection_blocked_commit`, `invalid_unsanitized_secret_commit_blocked`, `invalid_handle_leak_commit_blocked`, `invalid_missing_zeroize_commit_blocked`, `invalid_overbroad_context_commit_blocked`, `invalid_unapproved_destination_commit_blocked`, and `invalid_missing_residual_commit_blocked`. `evidence_transitions/v1_x_measured/security_scif_commit_probe_no_change.json` records the accepted no-promotion decision for this probe. This is a no deployed-kernel, sandbox-isolation, side-channel-safety, prompt-injection-containment, secret-handle-safety, approval-service, least-privilege-context, privacy, security, or support-state-promotion claim.
- `scripts/validate_rankfold_artifact_import.py` records a bounded public-safe RankFold artifact import: `docs/rankfold_artifact_import.md`, `experiments/rankfold_artifact_import/results/2026-07-02-local.json`, and `evidence_transitions/v1_x_measured/rankfold_artifact_import_no_change.json` preserve metadata for three existing local `.rfa` archive observations over a 100,000,000-byte decoded artifact digest, archive ratios up to 2.76634019 decoded/archive, `rfa verify` summaries of 1 OK and 0 failed, and `NEURAL0` inspect metadata. No dataset bytes, archive bytes, codec-correctness claim, fresh benchmark claim, downstream-utility claim, fallback-execution claim, deployed-compression claim, or chapter-core support-state promotion is included.
- `scripts/validate_resource_workflow_trace.py` adds a deterministic public Resource Economics workflow trace: `docs/resource_workflow_trace.md` and `experiments/resource_workflow_trace/results/2026-07-01-local.json` record 1 valid and 4 expected-invalid multi-step workflow fixtures checking selected-route cost recomputation, high-risk-first scheduler ordering, protected review overhead, displaced-cost residual ownership, physical-feasibility overclaim rejection, and no-promotion boundaries; no chapter core claim, deployed scheduler claim, economic claim, physical-feasibility claim, simulator-adequacy claim, model-quality claim, or support-state transition is promoted.
- `scripts/run_resource_live_probe.py --write-result` and `scripts/validate_resource_live_probe.py` add a local Resource Economics command-replay probe: `docs/resource_live_probe.md` and `experiments/resource_live_probe/results/2026-07-01-local.json` record five local validator replays, command-output digests, elapsed milliseconds, and tracked artifact hashes for the flagship lane; no chapter core claim, deployed scheduler claim, live workload-quality claim, production scheduler-log claim, physical-feasibility claim, simulator-adequacy claim, model-quality claim, economic claim, or support-state transition is promoted.
- `scripts/run_theseus_support_replay_probe.py --write-result` and `scripts/validate_theseus_support_replay_probe.py` add a local Project Theseus support replay probe: `docs/theseus_support_replay_probe.md` and `experiments/theseus_support_replay_probe/results/2026-07-01-local.json` record two local validator replays, command-output digests, elapsed milliseconds, and tracked artifact hashes for the selected Project Theseus support lanes; no chapter core claim, live Theseus replay claim, public task-bundle claim, generation-speed claim, useful-solution-per-second claim, model-quality claim, safety claim, alignment claim, or support-state transition is promoted.
- `scripts/validate_theseus_report_bundle_audit.py` adds a public-safe Project Theseus report-bundle audit: `docs/theseus_report_bundle_audit.md` and `experiments/theseus_report_bundle_audit/results/2026-07-02-local.json` validate one bundle-shaped fixture, seven expected-invalid controls, replay-readiness rows, crosswalk rows, gate mappings, work-board contract fields, visible artifact gaps, intervention-ladder ordering, and no-promotion boundaries; no clean live Theseus replay, public task-bundle run, current work-board import, benchmark result, model-quality result, safety claim, alignment claim, or support-state transition is promoted.
- `scripts/build_resource_ci_cost_profile.py --write-result` and `scripts/validate_resource_ci_cost_profile.py` add a Resource Economics CI cost profile: `docs/resource_ci_cost_profile.md` and `experiments/resource_ci_cost_profile/results/2026-07-01-main.json` record eight actual GitHub Pages workflow runs, seven completed runs, six successful completed runs, one generated-scaffold failure, one repair run, and publication-duration metrics; this is publication-pipeline metadata only and does not promote chapter claims or prove production scheduler behavior.
- `scripts/run_resource_flagship_lane.py --write-result` and `scripts/validate_resource_flagship_lane.py` add an aggregate Resource Economics flagship replay: `docs/resource_flagship_lane_run.md` and `experiments/resource_flagship_lane/results/2026-07-01-local.json` compose ten existing validators, command-output digests, and 26 tracked artifact hashes into one local replay gate; this is not a new support-state transition, external review, deployed scheduler result, production workload, artifact approval, model-quality result, or economic outcome.
- `scripts/validate_circle_external_receipt_slice.py` records the first bounded imported external-prototype receipt slice: `docs/circle_external_receipt_slice.md`, `experiments/circle_external_receipt_slice/results/2026-06-29-local.json`, and `evidence_transitions/v1_0_measured/circle_external_rope_receipt_prototype_backed.json` scope a `prototype-backed` transition to `circle-calculus.external_rope_receipt_replay`. The validator checks the public-safe summary of a clean local Circle checkout at commit `63b0f511`, successful `lake build Circle`, proved/passed rope certification for `CC-AI-CONTRACT-ROPE-001`, accepted receipt requirements, and 145 passing receipt/contract tests; no chapter core claim, deployed proof-contract transport claim, model-quality claim, benchmark claim, safety claim, transfer claim, or ASI claim is promoted.
- `scripts/validate_circle_cyclic_memory_receipt_slice.py` records a bounded Circle cyclic-memory structural receipt slice: `docs/circle_cyclic_memory_receipt_slice.md` and `experiments/circle_cyclic_memory_receipt_slice/results/2026-07-02-local.json` preserve `CC-AI-CONTRACT-MEMORY-001`, theorem IDs `AIM-T0001`, `AIM-T0002`, `AIM-T0004`, `AIM-T0005`, same-residue events `[7, 15, 23, 31]`, same-residue windings `[0, 1, 2, 3]`, `max_alias_load=4`, a strict receipt fingerprint, and `3 passed in 2.51s`; no retrieval-quality, long-context, model-quality, speed, memory-scaling, deployment, transfer, ASI, or support-state-transition claim is promoted.
- `docs/defended_contribution_prior_art_positioning.md` positions the five selected defended contribution tracks against source-noted external comparators and records the remaining novelty, review, replay, proof, and routing residual-governance gaps; `scripts/validate_defended_contribution_prior_art.py` keeps the comparison visible without support-state movement.
- `docs/evidence_laundering_prevention_case_studies.md` records three live no-promotion case studies plus one historical claim-surface narrowing record: the Project Theseus static import, Circle public consumer gate, and reader HTML artifact review each had tempting promotion pressure but stayed inside exact evidence and artifact boundaries, while `claim_revisions/v1_x/manifest_core_claim_count_narrowing.json` records an earlier correction from a stale 54-count surface to the then-current 44-chapter consolidation snapshot. That historical record is not the active manifest count; the active manifest is derived from `book_structure.json`. `scripts/validate_evidence_laundering_case_studies.py` keeps those examples visible while preserving that no chapter core claim has been demoted or refuted.
- `scripts/validate_circle_public_replay.py` records the public ASI-side Circle consumer gate: `docs/circle_public_replay_consumer_gate.md`, `experiments/circle_public_replay/fixtures/valid/circle_rope_receipt.consumer.valid.json`, and `experiments/circle_public_replay/results/2026-06-29-local.json` validate the pinned `CC-AI-CONTRACT-ROPE-001` receipt boundary and reject digest-mismatch, missing-theorem, stale-contract, and unsupported-transfer mutation controls. `evidence_transitions/v1_x_measured/circle_public_consumer_gate_no_change.json` now records that gate as an accepted `blocks_promotion` no-change decision; it does not create a seventh accepted upward transition, rerun Circle Lean here, vendor Circle, prove deployed proof-contract transport, or promote any chapter core claim.
- `claim_decisions/v1_0_core_claim_no_promotion.json`, `claim_decisions/v1_x_core_claim_dispositions.json`, `docs/core_claim_transition_coverage.md`, `docs/core_claim_disposition_ledger.md`, `scripts/validate_core_claim_decisions.py`, and `scripts/validate_v1_x_core_claim_dispositions.py` close the current chapter-core claim-state coverage and disposition gates: every active chapter core claim has either an accepted no-change transition record or an accepted explicit no-promotion decision, every active chapter has a recorded "what would move this" disposition, and all 55 remain at `argument`.
- `docs/architecture_red_team_review.md` and `scripts/validate_architecture_red_team.py` close the Phase 7A desk-review gate for six composed-system attacks: authority escalation, context leakage, evaluator capture, support-state inflation, benchmark gaming, and reader-release laundering. This is residual routing, not runtime safety validation.
- `docs/release_reproducibility.md`, `CITATION.cff`, and `scripts/validate_release_reproducibility.py` govern reproducibility and citability: CI pins Quarto `1.9.38`, Python `3.11`, Node `22`, and Lean through `lean/lean-toolchain`; the citation file records completed release version `2.0.0`; no DOI or unselected reader-format artifact approval is claimed.
- `docs/public_site_accessibility_review.md`, `docs/v1_progress_ledger.md`, and `scripts/validate_public_site_accessibility.py` close the current Phase 7 accessibility-readiness ledger gap by checking assistive reading-mode hooks, focus and containment CSS, landing-image alt text, diagram walkthrough coverage, phase-progress rows, residuals, and non-claims. This is not a WCAG conformance claim, screen-reader approval, or reader-artifact approval.
- `docs/v1_0_release_gate_audit.md` and `scripts/validate_v1_release_gate_audit.py` preserve the historical v1.0 Definition-of-Done audit and its evidence/residual boundaries. The completed v2.0.0 release state is recorded separately in `docs/v2_0_completion_declaration.md` and `release_records/2026-07-10-v2.0.0-research-52e54b71.json`; neither release creates a support-state promotion or DOI claim.
- `docs/external_sota_positioning_audit.md` and `scripts/validate_external_sota_positioning.py` keep the Phase 6 external-positioning gate honest: 55 of 55 chapters currently have in-prose `ext_*` positioning before the Source crosswalk, 0 have explicit external-baseline exceptions, and the stricter placement release check has 0 open positioning rows.
- `docs/chapter_external_grounding_status.md` and `scripts/validate_chapter_external_grounding_status.py` turn that placement audit into a 55-chapter grounding ledger: all 55 chapters have source-noted external positioning records, 0 carry explicit exceptions, and each row names the Corben/local sources to mine first before broader citation backfill.
- The live GitHub Pages site includes a persistent top-of-page reading-mode switch: `AI view` keeps the full live/research scaffold, including raw core-claim markers and repeated support-state boilerplate, while `Human view` hides the same repeated chapter sections, TOC entries, section-numbering artifacts, raw bracketed core-claim markers, and repeated support boilerplate used by the reader-release strip policy. Human view keeps the compact evidence boundary inline with the core claim rather than opening repeated support paragraphs. Readers can open a chapter directly in either mode with `?view=human` or `?view=ai`. All 55 chapters now carry a `.asi-human-only` Human Reading Path bridge for interested readers, and `.asi-ai-only` blocks remain available for mode-specific research notes without forking the manuscript. The rendered-site validator checks the static HTML hooks, and `scripts/validate_live_human_view_browser.js` exercises representative rendered pages by default or every manifest chapter across desktop and mobile viewports with `--all-chapters --all-viewports` in a real browser when Playwright/Chrome is available, including reading-mode control visibility, rendered Mermaid visibility, raw-marker and support-boilerplate hiding/restoration, and page-overflow checks.
- `proofs/proof_manifest.json` is generated from `lean:*` proof tags in the outline.
- `proofs/proof_triage.json` classifies proof targets as Lean, schema, process, or research-agenda work.
- Source notes exist for all currently assigned source records, and connector-readiness metadata remains tracked for source routes that depend on authenticated exports.
- Source documents are cached locally when available, but raw exports are ignored and not published.
- `scripts/validate_source_appendices.py` checks that Appendix G and Appendix H are independent top-level appendices with explicit source-ownership boundary blocks and separate appendix-identity rows: G contains only Corben's own papers, Corben-supplied materials, recovered project records, and local project records, while H contains only external-source and third-party literature records by other authors or organizations generated from `sources/source_inventory.json`.
- `scripts/validate_v1_status_snapshot.py` checks that `docs/v1_0_candidate_status.md` headline counts match current repository artifacts.
- `scripts/validate_outline_consistency.py` checks that `docs/book_outline.md` still matches the manifest chapter order, titles, core claims, assigned source IDs, and Lean proof targets.
- `scripts/validate_implementation_horizons.py` checks that every manifest chapter has a concrete minimum viable implementation and mature endpoint, and that generated Appendix K matches the manifest in order.
- Current source-note coverage, exact claim-source mappings, passage-reviewed mappings, and v1.0 core-claim transition/no-promotion coverage are complete for assigned source/chapter pairs, but all chapter core claims remain at `argument` support until accepted upward evidence transitions justify promotion.
- Protocol schema fixture checks and manifest schema validation are implemented; broader chapter-level Codex tests remain planned unless a specific test result is recorded.
- `scripts/draft_v02_from_manifest.py` records the repeatable baseline drafting pass; use it intentionally because it rewrites chapter files from the manifest.

## Start Here

| File or page | Purpose |
|---|---|
| [Live book](https://corbensorenson.github.io/asi-stack-book/) | Rendered public site. |
| [Canonical public status](https://corbensorenson.github.io/asi-stack-book/status/canonical-public-status.json) | Build-generated commit, tree-state, count, order, evidence-state, transition, and digest envelope for the deployed site. |
| [docs/book_outline.md](docs/book_outline.md) | Cohesive full-book outline and proof target source of truth. |
| [docs/prewriting_readiness.md](docs/prewriting_readiness.md) | Launch gate for a full-book drafting goal. |
| [docs/full_book_writing_goal.md](docs/full_book_writing_goal.md) | Suggested wording for the full-book writing goal. |
| [docs/v1_0_candidate_status.md](docs/v1_0_candidate_status.md) | Current v1.0 candidate snapshot, remaining evidence gaps, and release gate. |
| [docs/v1_0_focus_audit.md](docs/v1_0_focus_audit.md) | Detailed current-state audit and prioritized work plan for moving from v1.0 candidate toward evidence-release and reader-release quality. |
| [docs/v1_0_roadmap.md](docs/v1_0_roadmap.md) | Execution roadmap and recommended next long-running goal for v1.0 voice, reader, evidence, proof, test, source, site, and release work. |
| [docs/v1_x_beyond_sota_roadmap.md](docs/v1_x_beyond_sota_roadmap.md) | Post-v1.0.0 roadmap for deeper Lean proofs, Project Theseus/Circle replay evidence, per-chapter evidence lanes, curated reader prose, and human artifact release quality. |
| [docs/external_ai_review_remediation_program.md](docs/external_ai_review_remediation_program.md) | Evidence-checked remediation program for the user-supplied AI-assisted review, including P0 release coherence, the governed vertical slice, deeper invariants, product separation, contribution focus, CI refactoring, and decision gates. |
| [docs/governed_repository_change_slice.md](docs/governed_repository_change_slice.md) | Executed nine-scenario local repository-change comparison with eight adversarial cases, a simpler baseline, independent effect observation, rollback/quarantine, overhead accounting, and no chapter-core promotion. |
| [docs/CHAPTER_REVIEWS.md](docs/CHAPTER_REVIEWS.md) | External reviewer chapter-by-chapter guidance for the roadmap burn-down; not source evidence or support-state promotion. |
| [docs/a_plus_quality_scorecard.md](docs/a_plus_quality_scorecard.md) | Planning scorecard for moving every project dimension toward A+ quality, including cold-read legibility and defended contribution tracks. |
| [docs/defended_contribution_tracks.md](docs/defended_contribution_tracks.md) | v1.x contribution-track selection: five selected tracks, three deep-work tracks, and no chapter-core promotion. |
| [docs/defended_contribution_prior_art_positioning.md](docs/defended_contribution_prior_art_positioning.md) | Source-noted prior-art positioning for the five defended contribution tracks; not novelty proof or support-state movement. |
| [docs/contribution_novelty_ledger.md](docs/contribution_novelty_ledger.md) | Source-noted novelty-positioning ledger for eight signature ideas; not proof of novelty or support-state movement. |
| [docs/core_claim_disposition_ledger.md](docs/core_claim_disposition_ledger.md) | Per-chapter core-claim disposition ledger: 54 current dispositions, 0 promoted core claims, and explicit movement paths without support-state inflation. |
| [docs/evidence_laundering_prevention_case_studies.md](docs/evidence_laundering_prevention_case_studies.md) | No-promotion case studies plus one live claim-surface narrowing record for evidence-laundering prevention; preserves the remaining chapter-core demotion/refutation gap. |
| [docs/non_core_evidence_ledger.md](docs/non_core_evidence_ledger.md) | Public ledger for 25 accepted non-core upward evidence transitions, 61 accepted `blocks_promotion` decisions, three historical `refuted` labels with N1/N2 interpretation ceilings, one historical count-surface narrowing record, and their no-chapter-core-promotion boundary. |
| [docs/external_review_packet.md](docs/external_review_packet.md) | Public packet for independent v1.x safety, evidence, roadmap, grounding, and reader-quality review. |
| [docs/external_review_status.md](docs/external_review_status.md) | Ledger for the external-review request and the boundary that review input is not evidence by itself. |
| [external_reviews/request_updates/consolidation_review_request_2026-06-29.json](external_reviews/request_updates/consolidation_review_request_2026-06-29.json) | Structured request-update record for the supplemental consolidation review solicitation; no accepted review is claimed. |
| [external_reviews/request_updates/full_consolidation_review_request_2026-06-29.json](external_reviews/request_updates/full_consolidation_review_request_2026-06-29.json) | Structured request-update record for the full consolidation queue review solicitation; no accepted review or merge/fold authorization is claimed. |
| [docs/chapter_external_grounding_status.md](docs/chapter_external_grounding_status.md) | Generated 55-chapter grounding ledger tying each chapter to source-noted external comparators, explicit exceptions, and Corben/local sources to mine first. |
| [docs/per_chapter_evidence_plan.md](docs/per_chapter_evidence_plan.md) | 55-chapter evidence-lane backlog used as a menu for selecting one flagship measured lane plus direct supports, not as a breadth-sweep checklist. |
| [docs/v1_x_active_evidence_cycle.md](docs/v1_x_active_evidence_cycle.md) | Active v1.x evidence-cycle ledger: one flagship lane, two direct support lanes, forty-one planned-only lanes, and no chapter-core promotion. |
| [docs/chapter_consolidation_sequence.md](docs/chapter_consolidation_sequence.md) | Full governed consolidation sequence for the 54-to-44/47 critique, with the Part I pilot, conservative compression merge, intent/contracts merge, MoECOT runtime fold, simulation-fidelity fold, static context ABI merge, and verification/adversarial-review merge and planning/DAG consolidation executed and remaining packages still decision-gated. |
| [docs/chapter_consolidation_pilot_plan.md](docs/chapter_consolidation_pilot_plan.md) | Historical governed consolidation pilot plan for the Part I alignment/governance cluster; the pilot has since executed. |
| [docs/chapter_consolidation_decision_review.md](docs/chapter_consolidation_decision_review.md) | Historical consolidation decision surface for the Part I pilot; the pilot has since executed with URL/history handling. |
| [docs/chapter_consolidation_url_history_policy.md](docs/chapter_consolidation_url_history_policy.md) | Active URL/history policy applied to executed merges and folds and used for future consolidation packages. |
| [docs/chapter_consolidation_external_review_packet.md](docs/chapter_consolidation_external_review_packet.md) | Historical review packet for deciding whether to execute, revise, defer, or reject the Part I consolidation pilot. |
| [docs/chapter_consolidation_full_review_packet.md](docs/chapter_consolidation_full_review_packet.md) | Full decision-queue review packet with executed packages marked historical and remaining fold dispositions decision-gated; request surface only, not a manifest edit. |
| [docs/chapter_consolidation_release_stability_review.md](docs/chapter_consolidation_release_stability_review.md) | Release-stability decision deferring the remaining unexecuted semantic-representation fold for the current reader-curation cycle; no support-state movement, external-review claim, or reader-release approval. |
| [docs/chapter_consolidation_dry_run_constitutional_alignment.md](docs/chapter_consolidation_dry_run_constitutional_alignment.md) | Historical dry-run merge package for the executed constitutional alignment plus agency/corrigibility merge. |
| [docs/chapter_consolidation_dry_run_compression.md](docs/chapter_consolidation_dry_run_compression.md) | Historical dry-run package for the executed conservative compact-generative consolidation. |
| [docs/chapter_consolidation_destination_draft_compression.md](docs/chapter_consolidation_destination_draft_compression.md) | Historical one-skeleton destination draft for the executed conservative compression package. |
| [docs/chapter_consolidation_dry_run_intent_contracts.md](docs/chapter_consolidation_dry_run_intent_contracts.md) | Historical dry-run package for the executed intent-to-execution plus command-contracts merge. |
| [docs/chapter_consolidation_destination_draft_intent_contracts.md](docs/chapter_consolidation_destination_draft_intent_contracts.md) | Historical one-skeleton destination draft for the executed Command Contracts: From Intent to Executable Work merge. |
| [docs/chapter_consolidation_dry_run_context_abi.md](docs/chapter_consolidation_dry_run_context_abi.md) | Historical dry-run package for the executed Virtual Context ABI plus semantic pages/certificates merge. |
| [docs/chapter_consolidation_destination_draft_context_abi.md](docs/chapter_consolidation_destination_draft_context_abi.md) | Historical one-skeleton destination draft for the executed The Virtual Context ABI: Typed Pages, Cells, and Certificates merge. |
| [docs/chapter_consolidation_dry_run_verification_review.md](docs/chapter_consolidation_dry_run_verification_review.md) | Historical dry-run package for the executed Spinoza proof-carrying claims plus tribunal/adversarial-review merge. |
| [docs/chapter_consolidation_destination_draft_verification_review.md](docs/chapter_consolidation_destination_draft_verification_review.md) | Historical one-skeleton destination draft for the executed Proof-Carrying Claims and Adversarial Review merge. |
| [docs/chapter_consolidation_dry_run_planning_dag.md](docs/chapter_consolidation_dry_run_planning_dag.md) | Historical dry-run merge package for the executed Planning/DAG consolidation; not a live manifest instruction. |
| [docs/chapter_consolidation_destination_draft_planning_dag.md](docs/chapter_consolidation_destination_draft_planning_dag.md) | Historical one-skeleton destination draft for the executed Planning as a Control Layer: DAGs and Intelligence Arbitrage consolidation. |
| [docs/chapter_consolidation_fold_moecot_runtime.md](docs/chapter_consolidation_fold_moecot_runtime.md) | Executed fold history for MoECOT runtime into Routing Heads and Specialist Cores. |
| [docs/chapter_consolidation_fold_simulation_fidelity.md](docs/chapter_consolidation_fold_simulation_fidelity.md) | Executed fold history for Simulation Fidelity and Physical Constraints into Resource Economics and Token Budgets as Simulation Fidelity and Claim Transport. |
| [docs/chapter_consolidation_fold_semantic_representation.md](docs/chapter_consolidation_fold_semantic_representation.md) | Fold disposition for Semantic Representation and Tree-Structured Models into the compression/representation package as Semantic Representation Leasing; not reviewed, not executed, and not a manifest edit. |
| [docs/reader_overlay_pilot.md](docs/reader_overlay_pilot.md) | First active v1.0 semantic reader-overlay pilot. |
| [docs/reader_continuity_audit.md](docs/reader_continuity_audit.md) | Generated Phase 2 heuristic queue for reader-manuscript continuity review. |
| [docs/reader_chapter_review_matrix.md](docs/reader_chapter_review_matrix.md) | Manifest-synced 44-chapter human-reader review queue and release blockers. |
| [docs/reader_part_i_review_pass.md](docs/reader_part_i_review_pass.md) | First Part I reader-review matrix pass and no-action decisions. |
| [docs/reader_part_ii_review_pass.md](docs/reader_part_ii_review_pass.md) | First Part II reader-review matrix pass and canonical prose cleanup decisions. |
| [docs/reader_part_iii_review_pass.md](docs/reader_part_iii_review_pass.md) | First Part III reader-review matrix pass and canonical prose cleanup decisions. |
| [docs/reader_part_iv_review_pass.md](docs/reader_part_iv_review_pass.md) | First Part IV reader-review matrix pass and reader-generator capitalization cleanup decision. |
| [editions/reader_manuscript/v1_0/reconciliation_report.md](editions/reader_manuscript/v1_0/reconciliation_report.md) | Drafting curated-reader reconciliation report for parallel human-prose chapters and remaining release blockers. |
| [docs/curated_reader_source_contract.md](docs/curated_reader_source_contract.md) | Contract for future curated reader chapter files and reader handoff metadata as parallel derivative prose, not equal evidence authority. |
| [scripts/init_curated_reader_chapter.py](scripts/init_curated_reader_chapter.py) | Dry-run-first initializer for future curated reader chapter records and starter files. |
| [editions/reader_manuscript/v1_0/companion_note_routing.json](editions/reader_manuscript/v1_0/companion_note_routing.json) | Chapter-level companion-note routing manifest for reader, e-reader, and audio review. |
| [editions/reader_manuscript/v1_0/companion_notes/README.md](editions/reader_manuscript/v1_0/companion_notes/README.md) | Drafting companion-note directory policy for dense reader/audio material. |
| [editions/reader_manuscript/v1_0/companion_notes/circle-calculus-and-proof-carrying-ai-contracts.md](editions/reader_manuscript/v1_0/companion_notes/circle-calculus-and-proof-carrying-ai-contracts.md) | Drafting Circle companion note for proof receipt vocabulary, consumer gates, theorem laundering, and audio treatment. |
| [docs/curated_reader_circle_contracts_prose_pass.md](docs/curated_reader_circle_contracts_prose_pass.md) | Drafting-only curated reader prose pass for Circle proof-carrying contracts; no reader release or support-state promotion. |
| [editions/reader_manuscript/v1_0/companion_notes/executable-specifications-and-lean-proof-envelope.md](editions/reader_manuscript/v1_0/companion_notes/executable-specifications-and-lean-proof-envelope.md) | Drafting proof-envelope companion note for proof lanes, semantic adequacy, and audio treatment. |
| [docs/curated_reader_executable_specs_prose_pass.md](docs/curated_reader_executable_specs_prose_pass.md) | Drafting-only curated reader prose pass for Executable Specifications and the Lean proof envelope; no proof-adequacy or release claim. |
| [docs/curated_reader_system_boundaries_prose_pass.md](docs/curated_reader_system_boundaries_prose_pass.md) | Drafting-only curated reader prose pass for System Boundaries and Authority; no deployed enforcement or reader release claim. |
| [docs/curated_reader_failure_modes_prose_pass.md](docs/curated_reader_failure_modes_prose_pass.md) | Drafting-only curated reader prose pass for Failure Modes of Ungoverned Intelligence; no scenario-coverage, deployed-detection, or reader release claim. |
| [docs/curated_reader_evidence_states_prose_pass.md](docs/curated_reader_evidence_states_prose_pass.md) | Drafting-only curated reader prose pass for Evidence States and Claim Discipline; no support-state movement or reader release. |
| [docs/curated_reader_security_kernel_prose_pass.md](docs/curated_reader_security_kernel_prose_pass.md) | Drafting-only curated reader prose pass for Security Kernel and Digital SCIFs; no deployed security, sandbox, side-channel, prompt-injection containment, or reader release claim. |
| [docs/curated_reader_stable_capability_fields_prose_pass.md](docs/curated_reader_stable_capability_fields_prose_pass.md) | Drafting-only curated reader prose pass for Stable Capability Fields; no route-validation, authority-enforcement, replacement-safety, rollback-execution, SLSA, or reader release claim. |
| [docs/curated_reader_capability_replacement_prose_pass.md](docs/curated_reader_capability_replacement_prose_pass.md) | Drafting-only curated reader prose pass for Capability Replacement and Rollback; no deployed replacement, regression-suite, monitor-window, rollback-execution, or reader release claim. |
| [docs/curated_reader_routing_heads_prose_pass.md](docs/curated_reader_routing_heads_prose_pass.md) | Drafting-only curated reader prose pass for Routing Heads and Specialist Cores; no routing accuracy, learned-router, deployed authority enforcement, MoECOT runtime, or reader release claim. |
| [docs/curated_reader_moecot_runtime_prose_pass.md](docs/curated_reader_moecot_runtime_prose_pass.md) | Historical curated reader prose pass for the retired standalone MoECOT Runtime draft; active reader work now routes through Routing Heads, with no runtime replay, benchmark reproduction, or reader release claim. |
| [docs/curated_reader_readiness_gates_prose_pass.md](docs/curated_reader_readiness_gates_prose_pass.md) | Drafting-only curated reader prose pass for Readiness Gates, Residual Escrow, and Quarantine; no deployed readiness engine, residual-ledger, live quarantine-routing, or reader release claim. |
| [docs/curated_reader_context_transactions_prose_pass.md](docs/curated_reader_context_transactions_prose_pass.md) | Drafting-only curated reader prose pass for Context Transactions, Snapshots, Mounts, and Taint; no memory-store, branch-isolation, mount-visibility, VCM conformance, or reader release claim. |
| [docs/curated_reader_verification_bandwidth_prose_pass.md](docs/curated_reader_verification_bandwidth_prose_pass.md) | Drafting-only curated reader prose pass for Verification Bandwidth and Context Adequacy; no contradiction-rate, distractor-resistance, adequacy-classifier, deployment, or reader release claim. |
| [docs/curated_reader_claim_ledgers_prose_pass.md](docs/curated_reader_claim_ledgers_prose_pass.md) | Drafting-only curated reader prose pass for Claim Ledgers and Belief Revision; no claim extraction, contradiction detection, belief-engine, support-state movement, or reader release claim. |
| [docs/curated_reader_artifact_graphs_prose_pass.md](docs/curated_reader_artifact_graphs_prose_pass.md) | Drafting-only curated reader prose pass for Artifact Graphs, Audit Logs, and Replay; no replay engine, audit reconstruction, artifact service, benchmark, or reader release claim. |
| [docs/curated_reader_labor_os_prose_pass.md](docs/curated_reader_labor_os_prose_pass.md) | Drafting-only curated reader prose pass for Labor OS and Typed Jobs; no scheduler, permission service, approval service, runtime adapter, replay system, benchmark, security, or reader release claim. |
| [docs/curated_reader_living_book_methodology_prose_pass.md](docs/curated_reader_living_book_methodology_prose_pass.md) | Drafting-only curated reader prose pass for Living Book Methodology; no manuscript-quality, source-interpretation, release-artifact, ASI-capability, or support-state promotion claim. |
| [docs/curated_reader_open_research_agenda_prose_pass.md](docs/curated_reader_open_research_agenda_prose_pass.md) | Drafting-only curated reader prose pass for Open Research Agenda and Bibliography Plan; no citation-normalization, benchmark-reproduction, artifact-reproduction, external-review, reader-release, or support-state promotion claim. |
| [docs/curated_reader_compact_generative_systems_prose_pass.md](docs/curated_reader_compact_generative_systems_prose_pass.md) | Drafting-only curated reader prose pass for Compact Generative Systems; no CGS implementation, codec, semantic-graph, benchmark, or support-state promotion claim. |
| [docs/curated_reader_rankfold_artifact_compression_prose_pass.md](docs/curated_reader_rankfold_artifact_compression_prose_pass.md) | Drafting-only curated reader prose pass for RankFold/NeuralFold artifact compression; no compressor, deterministic decoder, corpus benchmark, utility, or release claim. |
| [editions/reader_manuscript/v1_0/companion_notes/artifact-steward-agents-and-living-project-governance.md](editions/reader_manuscript/v1_0/companion_notes/artifact-steward-agents-and-living-project-governance.md) | Drafting artifact-steward companion note for project objects, implementation ladder, and audio treatment. |
| [docs/reader_companion_note_routing_review.md](docs/reader_companion_note_routing_review.md) | Human-readable review note for current companion-note routing decisions. |
| [docs/reader_format_dry_run.md](docs/reader_format_dry_run.md) | Local HTML/EPUB/DOCX reader-format dry-run record and non-release boundary. |
| [docs/reader_format_review_matrix.md](docs/reader_format_review_matrix.md) | Synced pre-release reader-format review ledger for HTML, EPUB, DOCX, and PDF blockers. |
| [docs/reader_artifact_inspection_manifest.md](docs/reader_artifact_inspection_manifest.md) | Tracked local HTML/EPUB/DOCX structural-inspection summary for ignored reader-format snapshots. |
| [docs/reader_key_figure_artifact_review.md](docs/reader_key_figure_artifact_review.md) | Tracked draft key-figure placement, metadata, rendered-browser, companion-note, and contrast review for the live book and curated reader manuscript; not final figure-artifact approval. |
| [docs/reader_key_figure_contrast_review.md](docs/reader_key_figure_contrast_review.md) | Measured source-SVG contrast/readability review for the ten draft key figures; not release approval or final art approval. |
| [docs/reader_key_figure_html_probe.md](docs/reader_key_figure_html_probe.md) | Rendered curated-reader HTML DOM probe for the ten draft key figures; not visual review or release approval. |
| [docs/reader_epub_probe_manifest.md](docs/reader_epub_probe_manifest.md) | Tracked local EPUB metadata/source-spine probe summary and e-reader-specific release blockers. |
| [docs/reader_docx_probe_manifest.md](docs/reader_docx_probe_manifest.md) | Tracked local DOCX LibreOffice conversion probe summary, spot-check residuals, and DOCX-specific release blockers. |
| [docs/reader_pdf_probe_manifest.md](docs/reader_pdf_probe_manifest.md) | Tracked local UTF-8 PDF probe summary, spot-check residuals, and PDF-specific release blockers. |
| [docs/reader_audio_script_probe_manifest.md](docs/reader_audio_script_probe_manifest.md) | Tracked local audio-script review-workspace probe summary, spoken-treatment counts, key-figure spoken-summary routing, and audio-specific release blockers. |
| [docs/reader_artifact_layout_review.md](docs/reader_artifact_layout_review.md) | Representative local PDF/HTML layout spot check and remaining artifact-review residuals. |
| [docs/reader_html_artifact_browser_review.md](docs/reader_html_artifact_browser_review.md) | Full local browser review record for the generated reader HTML artifact. |
| [docs/curated_reader_html_artifact_browser_review.md](docs/curated_reader_html_artifact_browser_review.md) | Full local browser viability review record for the tracked curated reader manuscript rendered as ignored HTML; not release approval. |
| [docs/claim_ledger_revision_harness.md](docs/claim_ledger_revision_harness.md) | Phase 5 synthetic claim-ledger and belief-revision record-discipline harness. |
| [docs/proof_carrying_claim_harness.md](docs/proof_carrying_claim_harness.md) | Phase 5 synthetic proof-carrying claim tier, verifier, and mismatch harness. |
| [docs/tribunal_review_harness.md](docs/tribunal_review_harness.md) | Phase 5 synthetic tribunal-review dossier, dissent, and verdict-boundary harness. |
| [docs/value_conflict_harness.md](docs/value_conflict_harness.md) | Phase 5 synthetic value-conflict classification, review, and residual-boundary harness. |
| [docs/constitutional_alignment_harness.md](docs/constitutional_alignment_harness.md) | Phase 5 synthetic constitutional-predicate scope, conflict, migration, self-modification, and power-boundary harness. |
| [docs/governance_rights_harness.md](docs/governance_rights_harness.md) | Phase 5 synthetic governance-right audit, exit, fork, and appeal-boundary harness. |
| [docs/agency_rights_harness.md](docs/agency_rights_harness.md) | Phase 5 synthetic agency-right material-usability, timing, corrigibility, and approval-boundary harness. |
| [docs/support_state_transition_harness.md](docs/support_state_transition_harness.md) | Phase 5 synthetic support-state transition gate harness. |
| [docs/authority_transition_harness.md](docs/authority_transition_harness.md) | Phase 5 synthetic authority non-escalation and permission-separation harness. |
| [docs/security_kernel_harness.md](docs/security_kernel_harness.md) | Phase 5 synthetic security-kernel handle, SCIF lifecycle, sanitization, revocation, and prompt-injection boundary harness. |
| [docs/security_scif_commit_probe.md](docs/security_scif_commit_probe.md) | Book-gate SCIF sanitized commit replay probe with two valid fixture routes, six expected-invalid controls, and no-promotion boundary. |
| [docs/stable_capability_field_harness.md](docs/stable_capability_field_harness.md) | Phase 5 synthetic stable-capability-field qualification and routing-boundary harness. |
| [docs/capability_replacement_harness.md](docs/capability_replacement_harness.md) | Phase 5 synthetic capability-replacement transaction-boundary harness. |
| [docs/self_improvement_boundary_harness.md](docs/self_improvement_boundary_harness.md) | Phase 5 synthetic recursive self-improvement transition-boundary harness. |
| [docs/plan_execution_contract_harness.md](docs/plan_execution_contract_harness.md) | Phase 5 synthetic plan graph and execution-contract harness. |
| [docs/runtime_adapter_permission_harness.md](docs/runtime_adapter_permission_harness.md) | Phase 5 synthetic runtime adapter permission, approval, receipt, and rollback/residual harness. |
| [docs/runtime_adapter_effect_probe.md](docs/runtime_adapter_effect_probe.md) | Book-gate Runtime adapter effect replay probe with one public-safe temp-file write, rollback-exact restoration, missing-permission denial, expired-approval denial, and no-promotion boundary. |
| [docs/runtime_adapter_adversarial_boundary_probe.md](docs/runtime_adapter_adversarial_boundary_probe.md) | Book-gate Runtime adapter adversarial boundary probe for parentage, authority, approval, sandbox, secret, rollback, receipt, audit, support-state, and non-claim controls. |
| [docs/artifact_steward_lifecycle_probe.md](docs/artifact_steward_lifecycle_probe.md) | Book-gate Artifact steward lifecycle probe with two valid fixture-composed routes, six expected-invalid controls, and no-promotion boundary. |
| [docs/vcm_resolver_certificate_probe.md](docs/vcm_resolver_certificate_probe.md) | Book-gate VCM resolver/certificate probe with two valid fixture routes, nine expected-invalid controls, and no-promotion boundary. |
| [docs/intent_recontract_probe.md](docs/intent_recontract_probe.md) | Book-gate Intent re-contract trigger probe with two valid fixture routes, seven expected-invalid controls, and no-promotion boundary. |
| [docs/artifact_graph_replay_harness.md](docs/artifact_graph_replay_harness.md) | Book-gate synthetic artifact graph replay, audit reconstruction, and promotion-blocking harness. |
| [docs/procedural_memory_loop_harness.md](docs/procedural_memory_loop_harness.md) | Book-gate synthetic procedural-memory loop qualification harness. |
| [docs/routing_decision_lease_harness.md](docs/routing_decision_lease_harness.md) | Book-gate synthetic routing decision lease, fallback, overprivilege-rejection, and MoECOT source-boundary harness. |
| [docs/context_admission_adequacy_harness.md](docs/context_admission_adequacy_harness.md) | Phase 5 synthetic context admission and adequacy harness. |
| [docs/readiness_residual_harness.md](docs/readiness_residual_harness.md) | Phase 5 synthetic readiness gate and residual escrow harness. |
| [docs/benchmark_antigoodhart_harness.md](docs/benchmark_antigoodhart_harness.md) | Phase 5 synthetic benchmark anti-Goodhart harness. |
| [docs/generation_mode_baseline_harness.md](docs/generation_mode_baseline_harness.md) | Phase 5 deterministic generation-mode baseline and resource-budget alignment harness. |
| [docs/resource_budget_ledger_harness.md](docs/resource_budget_ledger_harness.md) | Phase 5 deterministic resource-budget ledger harness. |
| [docs/reference_trace_harness.md](docs/reference_trace_harness.md) | Phase 5 deterministic reference-trace continuity and stop-condition harness. |
| [docs/capacity_smoothing_harness.md](docs/capacity_smoothing_harness.md) | Phase 5 deterministic capacity-smoothing toy harness. |
| [docs/phase5_harness_registry.md](docs/phase5_harness_registry.md) | Registry and traceability contract for the initial Phase 5 harness set. |
| [docs/phase5_harness_runner.md](docs/phase5_harness_runner.md) | Registry-driven local execution record for the Phase 5 harness suite. |
| [docs/first_measured_replayed_slice.md](docs/first_measured_replayed_slice.md) | Bounded measured/replayed slice ledger and non-claim boundaries. |
| [docs/costed_route_resource_slice.md](docs/costed_route_resource_slice.md) | First bounded non-infrastructure costed-route/resource-budget slice. |
| [docs/resource_workflow_trace.md](docs/resource_workflow_trace.md) | Deterministic Resource Economics workflow trace with selected-route cost recomputation, scheduler-ordering checks, displaced-cost residual controls, and physical-feasibility overclaim rejection. |
| [docs/circle_external_receipt_slice.md](docs/circle_external_receipt_slice.md) | First bounded imported external Circle receipt slice and prototype-backed non-claim boundary. |
| [docs/circle_public_replay_consumer_gate.md](docs/circle_public_replay_consumer_gate.md) | Public ASI-side Circle consumer-gate fixture, digest check, and negative controls for receipt overclaim prevention. |
| [docs/circle_cyclic_memory_receipt_slice.md](docs/circle_cyclic_memory_receipt_slice.md) | Bounded Circle cyclic-memory residue/winding receipt slice with theorem IDs, alias-load facts, output digests, and no-promotion boundaries. |
| [docs/circle_multicoil_phase_receipt_slice.md](docs/circle_multicoil_phase_receipt_slice.md) | Bounded Circle MultiCoil phase-feature receipt slice with theorem IDs, joint-repeat and relative-phase facts, output digests, and no-promotion boundaries. |
| [docs/circle_sparse_attention_receipt_slice.md](docs/circle_sparse_attention_receipt_slice.md) | Bounded Circle sparse-attention gap and dense-local fallback receipt slice with theorem IDs, output digests, and no-promotion boundaries. |
| [docs/circle_strided_fanout_receipt_slice.md](docs/circle_strided_fanout_receipt_slice.md) | Bounded Circle strided candidate-fanout receipt slice with theorem IDs, finite stride-cycle facts, duplicate-budget accounting, output digests, and no-promotion boundaries. |
| [docs/circle_seed_rule_receipt_slice.md](docs/circle_seed_rule_receipt_slice.md) | Bounded Circle seed-rule exact-regeneration and storage-accounting receipt slice with theorem IDs, bounded candidate-search facts, output digests, and no-promotion boundaries. |
| [docs/rankfold_public_safe_probe.md](docs/rankfold_public_safe_probe.md) | Fresh RankFold public-safe replay probe with RAW0 roundtrip-exact archive behavior, corrupt-archive negative control, and no-compression-advantage boundary. |
| [docs/rankfold_artifact_import.md](docs/rankfold_artifact_import.md) | Bounded public-safe RankFold artifact import with archive metadata, digest consensus, verifier summaries, and no-promotion boundaries. |
| [docs/theseus_support_replay_probe.md](docs/theseus_support_replay_probe.md) | Local Project Theseus support replay probe recording two validator replays, output digests, artifact hashes, and no-transition boundaries. |
| [docs/core_claim_transition_coverage.md](docs/core_claim_transition_coverage.md) | Generated v1.0 coverage report proving every chapter core claim has an accepted transition record or explicit no-promotion decision. |
| [docs/architecture_red_team_review.md](docs/architecture_red_team_review.md) | Phase 7A architecture-level desk red-team report and residual routing. |
| [docs/release_reproducibility.md](docs/release_reproducibility.md) | Candidate toolchain, citation, locale, and non-release artifact boundary. |
| [docs/public_site_accessibility_review.md](docs/public_site_accessibility_review.md) | Phase 7 public-site accessibility readiness review, residuals, and non-claims. |
| [docs/v1_progress_ledger.md](docs/v1_progress_ledger.md) | Compact v1.0 phase progress ledger and release-classification boundary. |
| [docs/v1_0_release_gate_audit.md](docs/v1_0_release_gate_audit.md) | Gate-by-gate v1.0 Definition-of-Done audit and final-release boundary. |
| [docs/external_sota_positioning_audit.md](docs/external_sota_positioning_audit.md) | Generated Phase 6 queue for in-prose external baseline positioning and exceptions. |
| [docs/v02_manuscript_status.md](docs/v02_manuscript_status.md) | Historical v0.2 manuscript completion, gaps, and validation status. |
| [docs/external_literature_queue.md](docs/external_literature_queue.md) | Explicit stance and queue for third-party literature. |
| [docs/release_editions_plan.md](docs/release_editions_plan.md) | Major-version EPUB/PDF/DOCX/audio edition plan and gates. |
| [docs/major_version_release_runbook.md](docs/major_version_release_runbook.md) | Operational ladder for tagged live, reader, e-reader/document, and audio releases. |
| [docs/local_project_mining_theseus_circle.md](docs/local_project_mining_theseus_circle.md) | Public-safe mining report for Project Theseus and Circle Calculus. |
| [book_structure.json](book_structure.json) | Schema-validated manifest for dynamic parts, chapters, source assignments, implementation horizons, proof hooks, and appendices. |
| [editions/release_profiles.json](editions/release_profiles.json) | Audience-specific release profile definitions. |
| [editions/reader_manuscript/README.md](editions/reader_manuscript/README.md) | Drafting curated reader-manuscript path, companion-note support, and release-boundary rules. |
| [appendices/A_source_matrix.qmd](appendices/A_source_matrix.qmd) | Generated source-to-chapter matrix. |
| [appendices/C_claim_evidence_matrix.qmd](appendices/C_claim_evidence_matrix.qmd) | Generated claim/evidence matrix. |
| [appendices/G_corben_source_corpus.qmd](appendices/G_corben_source_corpus.qmd) | Generated appendix for Corben's own sources, papers, and local project records. |
| [appendices/H_external_sources.qmd](appendices/H_external_sources.qmd) | Generated appendix for external sources and third-party literature by other authors. |
| [appendices/I_author_intent_and_lineage.qmd](appendices/I_author_intent_and_lineage.qmd) | Public-safe author-intent and architecture-lineage appendix. |
| [appendices/J_release_editions.qmd](appendices/J_release_editions.qmd) | Live-book explanation of reader, research, and audio edition paths. |
| [appendices/K_implementation_horizons.qmd](appendices/K_implementation_horizons.qmd) | Generated implementation-horizon matrix. |
| [proofs/proof_manifest.json](proofs/proof_manifest.json) | Generated Lean proof target manifest. |
| [docs/proof_depth_classification.md](docs/proof_depth_classification.md) | Generated proof-shape depth report separating projection-style Lean hooks from derived/decomposed theorem bodies. |
| [protocols/v1_critical_protocol_crosswalk.json](protocols/v1_critical_protocol_crosswalk.json) | Structured v1-critical schema/fixture/harness/Lean protocol crosswalk. |
| [docs/protocol_record_crosswalk.md](docs/protocol_record_crosswalk.md) | Generated protocol-record reconciliation report for v1-critical records. |
| [docs/repository_map.md](docs/repository_map.md) | Repository layout and ownership map. |
| [docs/publication_readiness.md](docs/publication_readiness.md) | Public-readiness checklist and known blockers. |

## Local Validation

Run this before committing structural, source, proof, or publication changes:

```bash
python3 scripts/sync_scaffold.py
python3 scripts/sync_proof_manifest.py
python3 scripts/sync_reader_overlay_asset.py --check
python3 scripts/source_readiness_report.py
python3 scripts/validate_validator_coverage.py
python3 scripts/validate_proof_depth.py
python3 scripts/validate_architecture_red_team.py
python3 scripts/validate_release_reproducibility.py
python3 scripts/validate_public_site_accessibility.py
python3 scripts/validate_v1_release_gate_audit.py
python3 scripts/validate_non_core_evidence_ledger.py
python3 scripts/validate_claim_revision_records.py
python3 scripts/validate_external_review_status.py
python3 scripts/validate_external_review_intake.py
python3 scripts/validate_defended_contribution_tracks.py
python3 scripts/validate_defended_contribution_prior_art.py
python3 scripts/validate_evidence_laundering_case_studies.py
python3 scripts/validate_chapter_consolidation_sequence.py
python3 scripts/validate_core_claim_promotion_paths.py
python3 scripts/validate_chapter_external_grounding_status.py
python3 scripts/validate_external_sota_positioning.py
python3 scripts/validate_trust_surface.py
python3 scripts/validate_publication.py
python3 scripts/validate_release_profiles.py
python3 scripts/validate_human_reading_paths.py
python3 scripts/validate_source_appendices.py
python3 scripts/validate_v1_status_snapshot.py
python3 scripts/validate_core_claim_decisions.py
python3 scripts/validate_outline_consistency.py
python3 scripts/validate_implementation_horizons.py
python3 scripts/validate_reader_evidence_boundaries.py --check
python3 scripts/validate_reader_overlays.py --check
python3 scripts/audit_reader_continuity.py --check
python3 scripts/validate_reader_manuscript_manifest.py
python3 scripts/validate_reader_key_figures.py
python3 scripts/validate_reader_key_figure_contrast.py
python3 scripts/validate_reader_key_figure_html_probe.py
python3 scripts/validate_reader_key_figure_format_probe.py
python3 scripts/validate_reader_artifact_inspection_manifest.py
python3 scripts/validate_reader_epub_probe_manifest.py
python3 scripts/validate_reader_docx_probe_manifest.py
python3 scripts/validate_reader_pdf_probe_manifest.py
python3 scripts/validate_reader_audio_script_probe_manifest.py
python3 scripts/sync_reader_chapter_review_matrix.py --check
python3 scripts/sync_reader_format_review_matrix.py --check
python3 scripts/validate_reader_spine.py --check
node scripts/validate_reader_html_artifact_browser.js --strict
python3 scripts/validate_claim_ledger_revision.py
python3 scripts/validate_protocol_crosswalk.py
python3 scripts/validate_proof_carrying_claims.py
python3 scripts/validate_tribunal_review.py
python3 scripts/validate_value_conflicts.py
python3 scripts/validate_constitutional_alignment.py
python3 scripts/validate_governance_rights.py
python3 scripts/validate_agency_rights.py
python3 scripts/validate_support_state_transitions.py
python3 scripts/validate_authority_transitions.py
python3 scripts/validate_security_kernel.py
python3 scripts/validate_stable_capability_fields.py
python3 scripts/validate_capability_replacement.py
python3 scripts/validate_self_improvement_boundaries.py
python3 scripts/validate_stack_layer_traceability.py
python3 scripts/validate_plan_execution_contracts.py
python3 scripts/validate_cognitive_compilation_traces.py
python3 scripts/validate_runtime_adapter_permissions.py
python3 scripts/validate_context_admission_adequacy.py
python3 scripts/validate_readiness_residual_gates.py
python3 scripts/validate_benchmark_antigoodhart.py
python3 scripts/validate_generation_mode_baselines.py
python3 scripts/validate_resource_budget_ledgers.py
python3 scripts/validate_reference_trace.py
python3 scripts/validate_capacity_smoothing.py
python3 scripts/validate_phase5_harness_registry.py
python3 scripts/validate_theseus_support_replay_probe.py
python3 scripts/validate_theseus_report_bundle_audit.py
python3 scripts/run_phase5_harnesses.py
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
- Reader overlays under `editions/reader_overlays/` are tracked semantic deltas for major human-reader versions. They target stable files and headings, feed both generated reader editions and the live Human view through `assets/reader-overlays.html`, then generate `reader_delta_report.md` with operation digests and before/after excerpts for review; generated reader files under `build/` are still disposable and should not be hand-edited. When overlays become too large or too numerous for clean semantic deltas, the drafting curated reader-manuscript path can expand into a human-prose derivative while the live book remains canonical for evidence.
- Curated reader builds use `scripts/build_curated_reader_edition.py` to assemble tracked curated chapter drafts into `build/curated_reader_edition/` for source-level review and local rendering. A historical candidate can be source-validated after the active spine changes, but it cannot render against a divergent spine; the next active reader edition must have its own directory and release record. This is a review workspace, not a release record, and it keeps all curated reconciliation and format-artifact blockers intact.
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

Generate or check the tracked curated-reader manuscript as a local Quarto review workspace:

```bash
python3 scripts/build_curated_reader_edition.py --check
python3 scripts/validate_reader_key_figures.py
python3 scripts/validate_reader_key_figure_contrast.py
python3 scripts/validate_reader_key_figure_html_probe.py
python3 scripts/validate_reader_key_figure_format_probe.py
python3 scripts/build_curated_reader_edition.py --output build/curated_reader_edition
LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 quarto render build/curated_reader_edition --to html
node scripts/validate_reader_html_artifact_browser.js --strict --site build/curated_reader_edition/_reader_site --manifest build/curated_reader_edition/reader_manifest.json --report build/curated_reader_edition/curated_reader_html_browser_report.json
```

Render selected reader-edition formats and record actual local outcomes:

```bash
python3 scripts/render_reader_formats.py --check
python3 scripts/render_reader_formats.py --formats html epub docx
python3 scripts/inspect_reader_format_artifacts.py
python3 scripts/validate_reader_epub_probe_manifest.py
python3 scripts/validate_reader_docx_probe_manifest.py
python3 scripts/validate_reader_pdf_probe_manifest.py
python3 scripts/validate_reader_key_figures.py
python3 scripts/validate_reader_key_figure_contrast.py
python3 scripts/validate_reader_key_figure_html_probe.py
python3 scripts/validate_reader_key_figure_format_probe.py
python3 scripts/validate_reader_audio_script_probe_manifest.py
python3 scripts/sync_reader_format_review_matrix.py --check
LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 python3 scripts/render_reader_formats.py --formats html epub docx pdf
```

Generate or check a narration-script candidate after the reader manuscript is ready for review:

```bash
python3 scripts/build_audio_script.py --check
python3 scripts/build_audio_script.py --source-mode curated_reader_manuscript
```

Generated edition builds are written under `build/` and ignored by git. Reader builds include `READER_RELEASE_CHECKLIST.md`, `companion_notes.md`, and `reader_delta_report.md`; render dry runs also preserve per-format snapshots under `build/reader_edition/format_artifacts/` for local review. Audio builds include `AUDIO_RELEASE_CHECKLIST.md`, `companion_notes.md`, `chapter_markers.md`, `pronunciation_glossary.md`, and `proof_equation_reading_rules.md`. Do not claim EPUB, PDF, DOCX, AZW3, MOBI, MP3, M4B, or audio-embedded EPUB artifacts as release artifacts unless those specific render, conversion, or audio-generation commands have actually succeeded, been reviewed where required, and a release record says so.

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

See [LICENSE.md](LICENSE.md), [NOTICE.md](NOTICE.md), and the path-level release routing ledger. At exact tag `v2.3.0`, cleared author-owned prose/figures are routed to CC BY 4.0 and cleared software-like artifacts to Apache-2.0; excluded paths and untagged or later drafting changes receive no grant. The completed v2.0.0, v2.1.0, and v2.2.0 grants remain bound to their own exact tags. The root site and `/latest/` are mutable and do not extend a tag-bound grant to later revisions.
