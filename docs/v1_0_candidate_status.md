# v1.0 Release Status

Last updated: 2026-07-04

This document is the current public-safe status surface for the tagged v1.0.0
living-book release. It supersedes the older prewriting, v0.2 launch-status,
and pre-tag candidate-status documents for current readiness decisions, while
those older documents remain useful historical records.

The book is tagged as `v1.0.0` at source commit
`96d0ca3c6b62f3530202535573941b1f6e50a83d`, with a GitHub Release at
`https://github.com/corbensorenson/asi-stack-book/releases/tag/v1.0.0` and a
tracked living-book release record at
`release_records/2026-06-29-v1.0.0-living-book-96d0ca3c.json`. The repository
now has a complete manifest-driven manuscript, source-note and claim-source
traceability, finite-record Lean coverage, schema fixtures, release-profile
scaffolding, a deployed Quarto site, one bounded synthetic-test-backed
repository-infrastructure transition, one bounded synthetic-test-backed
non-infrastructure costed-route/resource-budget transition, one bounded
synthetic-test-backed finite load-smoothing selector transition, one bounded
empirical-test-backed local scoped-route selector transition, one bounded
prototype-backed imported Circle receipt transition, and one bounded
synthetic-test-backed compact GVR receipt transition. All core chapter support
states remain `argument`.

## Current Snapshot

| Surface | Current state | Evidence |
|---|---|---|
| Book structure | 4 parts, 44 manifest-driven chapters, 11 appendices | `book_structure.json`; `python3 scripts/sync_scaffold.py` |
| Manifest claim contract | 44 chapters explicitly declare `claim_label` and `evidence_level`; current distribution is 44 `Design rationale` labels and 44 `argument` support states; missing or invalid values fail validation | `book_structure.json`; `python3 scripts/validate_book.py` |
| Manuscript scale | 44 chapter files; 205,295 chapter words excluding YAML front matter; 215,298 raw chapter-file words including metadata and live scaffolding | Local word-count check on `chapters/*.qmd` |
| Source inventory | 217 public-safe source records, each with a matching public source note; `sources/source_notes/` also contains a README and template | `sources/source_inventory.json`; `sources/source_notes/` |
| Source appendix ownership | Appendix G (`Corben's Own Sources, Papers, and Local Projects`) and Appendix H (`External Sources by Other Authors`) are independent top-level appendices with explicit source-ownership boundary blocks, ownership-rule rows, and appendix-local identity rows: G contains Corben's own papers, Corben-supplied materials, recovered project records, and local project records; H contains external records and third-party literature marked `external_literature`; neither appendix renders the other source class as a second ownership row | `python3 scripts/validate_source_appendices.py` |
| Claim/source traceability | 437 assigned source/chapter pairs, 435 exact claim-source mappings, 435 passage-reviewed mappings | `docs/source_evidence_audit.md`; `python3 scripts/validate_source_evidence_audit.py` |
| Support states | All 44 chapter core claims remain at `argument`; detailed core coverage, disposition, non-core upward transitions, and no-promotion side-lane decisions live in generated ledgers. Current counts: 22 accepted core no-change records, 22 accepted explicit core no-promotion decisions, 6 accepted narrow non-core upward transitions, 29 accepted `blocks_promotion` side-lane decisions, 0 promoted core claims, and no chapter core claim support-state promotion. | `book_structure.json`; Appendix C; `docs/core_claim_transition_coverage.md`; `docs/core_claim_disposition_ledger.md`; `docs/non_core_evidence_ledger.md`; `python3 scripts/validate_evidence_transitions.py`; `python3 scripts/validate_core_claim_decisions.py`; `python3 scripts/validate_v1_x_core_claim_dispositions.py`; `python3 scripts/validate_non_core_evidence_ledger.py` |
| External SOTA positioning | Phase 6 placement is machine-tracked and closed for the v1.0 placement gate: 44 of 44 chapters have `ext_*` positioning before the Source crosswalk, 0 chapters have explicit external-baseline exceptions, 0 chapters need source-target placement, and 0 chapters need an exception or added source-noted baseline | `docs/external_sota_positioning_audit.md`; `python3 scripts/validate_external_sota_positioning.py`; `python3 scripts/validate_external_sota_positioning.py --release` |
| Test harnesses | 62 wired checks: 22 Phase 5 registry harnesses and 40 chapter-specific/support book-gate checks. Detailed harness summaries, artifact references, and non-claim boundaries are generated in `docs/test_harness_status_ledger.md`; Appendix E remains the per-harness source of truth. None of these harnesses promotes chapter core claims. | `docs/test_harness_status_ledger.md`; `appendices/E_codex_test_specs.qmd`; `experiments/phase5_harness_registry.json`; `docs/phase5_harness_registry.md`; `python3 scripts/validate_test_harness_status_ledger.py`; `python3 scripts/validate_phase5_harness_registry.py`; `python3 scripts/validate_book.py` |
| Non-infrastructure measured slice | Resource Economics measured/replayed detail is generated in `docs/non_infrastructure_measured_slice_status_ledger.md`: 3 accepted bounded non-core transitions (1 `empirical-test-backed`, 2 `synthetic-test-backed`), 6 local Resource result artifacts, 5 replayed validators, 3 route-selection probes, 8 GitHub Pages runs classified, and all chapter-core/non-claim boundaries preserved. | `docs/non_infrastructure_measured_slice_status_ledger.md`; `docs/costed_route_resource_slice.md`; `docs/resource_workflow_trace.md`; `docs/resource_live_probe.md`; `docs/resource_workload_quality_probe.md`; `docs/resource_load_stability_probe.md`; `docs/resource_ci_cost_profile.md`; `lean/AsiStackProofs/ResourceEconomics.lean`; `evidence_transitions/v1_0_measured/costed_route_resource_slice_synthetic_test_backed.json`; `evidence_transitions/v1_x_measured/resource_load_stability_selector_synthetic_test_backed.json`; `evidence_transitions/v1_x_measured/resource_workload_quality_selector_empirical_test_backed.json`; `python3 scripts/validate_non_infrastructure_measured_slice_status_ledger.py` |
| Compact GVR synthetic slice | Compact GVR detail is generated in `docs/compact_gvr_status_ledger.md`: 5 public-safe receipt records, 368-byte literal baseline, 78-byte selected repeat-generator-plus-repair receipt, 3 rejected negative controls, 78.8% synthetic byte reduction, 1 accepted narrow `synthetic-test-backed` non-core transition, and finite Lean fixture alignment. No chapter-core, deployed compression, codec-correctness, model-quality, benchmark, safety, or ASI claim is promoted. | `docs/compact_gvr_status_ledger.md`; `docs/compact_gvr_slice.md`; `experiments/compact_gvr_slice/input/v1_x_compact_gvr_records.json`; `experiments/compact_gvr_slice/results/2026-07-01-local.json`; `lean/AsiStackProofs/CompactGenerativeSystems.lean`; `evidence_transitions/v1_x_measured/compact_gvr_slice_synthetic_test_backed.json`; `python3 scripts/validate_compact_gvr_status_ledger.py`; `python3 scripts/validate_compact_gvr_slice.py` |
| Imported external prototype slice | The first bounded imported external-prototype receipt slice records a clean local Circle checkout at commit `63b0f511`, a successful `lake build Circle`, a proved and passed rope certification for `CC-AI-CONTRACT-ROPE-001`, a ready digest with 31 fields, 0 missing fields, and 75 theorems, an accepted receipt requiring seven theorem IDs plus `ROPE-USE-D19-MARGIN-FRONTIER`, and a selected receipt/contract pytest batch with 145 passing tests. This supports only `circle-calculus.external_rope_receipt_replay`; it does not promote any chapter core claim, deployed proof-contract transport claim, model-quality claim, benchmark claim, safety claim, transfer claim, or ASI claim | `docs/circle_external_receipt_slice.md`; `experiments/circle_external_receipt_slice/results/2026-06-29-local.json`; `evidence_transitions/v1_0_measured/circle_external_rope_receipt_prototype_backed.json`; `python3 scripts/validate_circle_external_receipt_slice.py` |
| Circle public consumer gate | The first ASI-side public Circle consumer-gate fixture validates the pinned `CC-AI-CONTRACT-ROPE-001` receipt boundary with public fixture SHA-256 `7b33bc7059fa8f6b2ed1282ca5b0c4ab7f6f5044c2f834d487bdefbce44969c6`, contract content fingerprint `a0f35d3e89e9b6eac555f0392450f4f75cf7e70f30cff44ec7434f61bd85b468`, seven required theorem IDs, `ROPE-USE-D19-MARGIN-FRONTIER`, and four expected-invalid controls for digest mismatch, missing theorem ID, stale contract status, and unsupported transfer claims. `evidence_transitions/v1_x_measured/circle_public_consumer_gate_no_change.json` records the gate as an accepted `blocks_promotion` no-change decision, not a new upward support-state transition, not a local Circle Lean rerun, not a vendored contract pack, and not a chapter-core promotion | `docs/circle_public_replay_consumer_gate.md`; `experiments/circle_public_replay/fixtures/valid/circle_rope_receipt.consumer.valid.json`; `experiments/circle_public_replay/results/2026-06-29-local.json`; `evidence_transitions/v1_x_measured/circle_public_consumer_gate_no_change.json`; `python3 scripts/validate_circle_public_replay.py` |
| Project Theseus static import lane | Project Theseus detail is generated in `docs/project_theseus_static_import_status_ledger.md`: 2 sanitized static report imports, 1 support replay probe, 64 metadata-only public tasks, 0 public training rows, 18 generation modes, 13 comparisons, 0 promotable comparisons, 16 expected-invalid controls, and 1 accepted no-promotion decision; clean live replay remains unclaimed. | `docs/project_theseus_static_import_status_ledger.md`; `docs/theseus_report_import_slice.md`; `docs/theseus_generation_mode_import_slice.md`; `docs/theseus_support_replay_probe.md`; `docs/theseus_public_task_bundle_import.md`; `evidence_transitions/v1_x_measured/theseus_public_task_bundle_import_no_change.json`; `python3 scripts/validate_project_theseus_static_import_status_ledger.py` |
| Proof envelope | 200 proof targets remain implemented as bounded finite-record Lean predicates; the generated proof envelope ledger records traceability, adequacy classes, proof-depth metrics, and non-claim boundaries. Current adequacy: 13 `adequate finite-record invariant`, 114 `useful but too narrow`, 18 `needs richer state-machine or review semantics`, 35 `needs executable tests first`, 18 `needs empirical or baseline tests first`, and 2 `research-agenda until artifact import`. No proof-envelope artifact promotes any chapter core claim above `argument`. | `proofs/proof_manifest.json`; `docs/proof_envelope_status_ledger.md`; `docs/proof_artifact_audit.md`; `docs/proof_adequacy_review.md`; `docs/proof_depth_classification.md`; `lake build` |
| Schemas and fixtures | 76 JSON Schemas, 71 valid protocol fixtures, 4 public release records | `schemas/`; `schemas/book_structure.schema.json`; `schemas/theseus_report.schema.json`; `tests/fixtures/protocol_records/`; `release_records/`; `python3 scripts/validate_schemas.py`; `python3 scripts/validate_protocol_examples.py`; `python3 scripts/validate_book.py` |
| Implementation horizons | 44 generated chapter build horizons with manifest-sourced minimum viable implementation and beyond-state-of-the-art endpoint fields | `book_structure.json`; Appendix K; `python3 scripts/validate_implementation_horizons.py` |
| Visual coverage | Every chapter has at least one substantive Mermaid diagram with at least 12 non-comment lines plus enough named states, edges, and labeled transitions to explain a mechanism; every chapter has a required diagram walkthrough note for its primary diagram with a chapter-specific label; landing page has a generated visual asset; browser Human-view gate checks rendered Mermaid SVG visibility; dense Mermaid diagrams keep mobile labels readable through contained diagram-block scrolling without page-level horizontal overflow | `python3 scripts/validate_visual_coverage.py`; `node scripts/validate_live_human_view_browser.js --all-chapters --all-viewports`; `docs/site_visual_phase7_review.md` |
| Public-site accessibility readiness | Phase 7 accessibility readiness is recorded without claiming compliance: the live-site review checks reading-mode assistive hooks, focus-visible and mobile-containment CSS, landing-image alt text, diagram walkthrough coverage, compact progress-ledger rows, residuals, and non-claims. Manual keyboard-only review, screen-reader review, measured contrast audit, EPUB e-reader inspection, DOCX application review, and PDF page-by-page layout review remain explicit residuals | `docs/public_site_accessibility_review.md`; `docs/v1_progress_ledger.md`; `python3 scripts/validate_public_site_accessibility.py` |
| v1.0 release gate audit | The release-gate audit records all eleven Definition-of-Done gates, the v1.0.0 source tag, source commit, GitHub Release, living-book release record, current evidence, residuals, and non-claims without creating a DOI, archive, or chapter support-state promotion. | `docs/v1_0_release_gate_audit.md`; `release_records/2026-06-29-v1.0.0-living-book-96d0ca3c.json`; `python3 scripts/validate_v1_release_gate_audit.py` |
| Architecture red-team | Phase 7A desk review covers six composed-system attacks: authority ladder, SCIF/context leakage, evaluator capture, support-state inflation, benchmark gaming, and reader-release laundering. The review records setup, expected failure, observed current defense, residual risk, and routed follow-up without claiming runtime safety or external audit | `docs/architecture_red_team_review.md`; `python3 scripts/validate_architecture_red_team.py` |
| Release reproducibility | v1.0.0 toolchain and citation metadata are now explicit: CI pins Quarto `1.9.38`, Python `3.11`, Node `22`, and Lean through `lean/lean-toolchain`; `CITATION.cff` records version `1.0.0` and DOI-pending status; `docs/release_reproducibility.md` records local tool paths, locale boundaries, reader-format dependency boundaries, tag `v1.0.0`, source commit `96d0ca3c6b62f3530202535573941b1f6e50a83d`, and how to cite v1.0.0 without implying DOI, Zenodo archive, or additional approved reader artifacts | `docs/release_reproducibility.md`; `CITATION.cff`; `.github/workflows/publish.yml`; `release_records/2026-06-29-v1.0.0-living-book-96d0ca3c.json`; `python3 scripts/validate_release_reproducibility.py` |
| Chapter handoffs | All 44 manifest chapters now end with reader-facing `Handoff` sections: non-final chapters name the next manifest chapter title and avoid numbered chapter references, while the final chapter closes the book-level arc; generated reader chapters must preserve the same single Handoff continuity after live-only stripping | `python3 scripts/validate_chapter_handoffs.py`; `python3 scripts/validate_reader_spine.py --check` |
| Release surfaces | Live, research, reader, and audio profiles exist. Release detail is generated in `docs/release_surface_status_ledger.md`: generated-reader HTML remains the only approved reader artifact; `release_records/2026-07-04-v1-curated-reader-blocked-5dc1cd46.json` records the current curated-reader candidate as partial and blocked; `docs/reader_format_review_matrix.md` tracks 6 current curated-candidate rows with release blockers; automated keyboard traversal covers 98 page-view pairs with 0 failures; the human-consumption pre-release gate is `passed_human_consumption_pre_release_gate`; PDF page-by-page release-preparation review covers 506 pages with 0 failures; final figure-artifact review is `passed_final_figure_artifact_release_preparation_review` for 10 figures; the curated manuscript remains `drafting` with 44 records (44 reconciled); chapter reconciliation approval is `passed_curated_chapter_reconciliation_approval`; 73 overlay operations are tracked; Apple Books EPUB application review is passed, while EPUB publication, DOCX, PDF, audio, and refreshed reader HTML remain unapproved. | `docs/release_surface_status_ledger.md`; `editions/release_profiles.json`; `editions/reader_overlays/v1_0/manifest.json`; `editions/reader_manuscript/v1_0/manifest.json`; `editions/reader_manuscript/v1_0/chapter_review_matrix.json`; `editions/reader_manuscript/v1_0/chapter_reconciliation_approval_manifest.json`; `editions/reader_manuscript/v1_0/format_review_matrix.json`; `docs/reader_chapter_review_matrix.md`; `docs/reader_chapter_reconciliation_approval.md`; `docs/reader_format_review_matrix.md`; `docs/reader_html_artifact_browser_review.md`; `docs/curated_reader_html_artifact_browser_review.md`; `docs/curated_reader_format_artifact_probe.md`; `docs/reader_epub_probe_manifest.md`; `docs/reader_docx_probe_manifest.md`; `docs/reader_pdf_probe_manifest.md`; `docs/reader_audio_script_probe_manifest.md`; `docs/reader_key_figure_format_probe.md`; `docs/reader_human_consumption_gate_review.md`; `docs/curated_reader_pdf_page_review.md`; `docs/reader_final_figure_artifact_review.md`; `docs/reader_key_figure_geometry_review.md`; `docs/reader_visual_identity_review.md`; `docs/reader_accessibility_navigation_review.md`; `docs/reader_key_figure_raster_review.md`; `docs/reader_keyboard_navigation_review.md`; `docs/reader_key_figure_epub_layout_review.md`; `docs/reader_epub_apple_books_review.md`; `docs/reader_key_figure_pdf_layout_review.md`; `docs/reader_key_figure_docx_layout_review.md`; `release_records/2026-06-29-v1-reader-html-855dc277.json`; `release_records/2026-07-04-v1-curated-reader-blocked-5dc1cd46.json`; `python3 scripts/validate_curated_reader_blocked_release_record.py`; `python3 scripts/validate_curated_reader_pdf_page_review.py`; `python3 scripts/validate_reader_human_consumption_gate.py`; `python3 scripts/validate_reader_final_figure_artifact_review.py`; `python3 scripts/validate_reader_chapter_reconciliation_approval.py`; `python3 scripts/validate_release_surface_status_ledger.py` |
| Live Human view | Live/Human-view detail is generated in `docs/live_human_view_status_ledger.md`: 57 expected book pages, 44 manifest chapters with one Human Reading Path each, 73 active reader-overlay operations across 30 chapters, bridge minima 170/11/11 words with 0 template hits, and post-render static/browser gates remain required for hiding, restoration, overlay processing, and overflow checks. | `docs/live_human_view_status_ledger.md`; `assets/reader-overlays.html`; `assets/reading-mode.html`; `assets/styles.scss`; `python3 scripts/validate_live_human_view_status_ledger.py`; `python3 scripts/validate_live_human_view.py`; `node scripts/validate_live_human_view_browser.js --all-chapters --all-viewports` |
| Public site | GitHub Pages renders the live Quarto book | <https://corbensorenson.github.io/asi-stack-book/> |
| Status snapshot freshness | The headline counts in this status document are checked against current repository artifacts | `python3 scripts/validate_v1_status_snapshot.py` |
| Outline/manifest consistency | The drafting outline matches manifest chapter order, titles, core claims, assigned sources, and Lean proof targets | `python3 scripts/validate_outline_consistency.py` |

## What The Current Candidate Proves

- The book order is dynamic and manifest-driven.
- The outline is a usable source of truth for drafting, source queues, and Lean proof targets.
- Every manifest chapter exists and has the required chapter contract in order: problem, insufficiency, core claim, mechanism, interfaces, invariants, failure modes, minimum viable implementation, beyond-state-of-the-art end state, test plan, source crosswalk, and summary. The chapter DoD guard also requires `Problem`, insufficiency, and summary sections to clear a 130-word substance floor, `Mechanism` sections to clear a 300-word architecture floor, `Interfaces` sections to clear a 130-word systems-handoff floor, invariants to clear a 110-word preserved-boundary floor, failure modes to clear a 110-word concrete-risk floor, minimum viable implementation sections to clear a 125-word smallest-honest-build floor, and mature endpoints to clear a 200-word product-end-state floor while rejecting self-referential chapter phrasing, mechanical section handoffs, and live crosswalk references. The repeated-prose guard also rejects generic problem and insufficiency formulas such as `The book needs a place`, `The book needs`, `The stack needs`, `The ASI Stack needs`, `The problem is`, `The insufficiency is`, `The stack should`, `The record should`, and `The response is`, formulaic mature-endpoint openers and lead-ins such as `Operating mechanism:`, `At maturity,`, `The mature version is`, `The mature version of`, `The logical end state is`, `At full build-out`, `The mature product surface would include:`, `The final product surface would include:`, `would expose:`, `The operational contract is`, `Support should stay at`, `At that mature boundary`, `In that final product`, `Failure closure:`, `detect and route failure modes such as`, `This is a target architecture, not a current-result claim`, `remains a target architecture, not a current-result claim`, `It remains beyond the chapter's present support state`, `Another invariant is`, `A second invariant is`, `The strongest invariant is`, `The key invariant is`, `The invariant is`, `The subtle failure is`, `The subtle failure mode is`, `Another failure is`, and `Each failure should`, support-state formulas such as `The support state remains argument`, MVI formulas such as `The next useful implementation step is`, `The next useful fixture set is`, `The next useful fixture is`, `The fixture validates`, `The fixture is not`, `The fixture is only`, `Passing the fixture`, `Passing schema validation only`, `That would`, `without claiming`, `does not prove`, `do not prove`, `proves only`, `prove only`, `cannot prove`, `The accompanying Lean module is`, `The Lean predicates do not`, `These proofs do not implement`, and `The Lean coverage stays at`, generic interface formulas such as `The interface is the`, `The interface is a`, `The interface is an`, `The public schema now records`, `The interface should`, `The interface should also record`, `The interface should distinguish`, `The interface should expose`, `The interface should carry`, `The interface should also`, and `The contract should also`, generic mechanism evidence-boundary formulas such as `None of those passages show` and `The reviewed passages sharpen the`, and generic summary formulas such as `The evidence map is narrower now`.
- The repeated-prose guard now also rejects `The passage-reviewed mappings support discussion` so Core Claim support paragraphs must name the actual source family or evidence boundary.
- The repeated-prose guard now rejects generic practical-purpose formulas such as `The practical point is`, `The practical test is`, `The practical rule is`, `The practical purpose is`, and `The practical problem is`, so reader-visible prose names the actual boundary instead of leaning on a reusable cadence.
- The repeated-prose guard now rejects `The stack should`, so reader-visible prose has to name the actual layer, artifact, gate, record, or accounting surface rather than falling back to generic stack-level obligation language.
- The repeated-prose guard now rejects `The record should`, so record-bearing prose must name the actual ledger, receipt, packet, card, admission record, or claim record carrying the obligation.
- The repeated-prose guard now rejects `The response is`, so failure-mode prose must name the actual mitigation, governance control, protocol, or continuity path.
- The repeated-prose guard now rejects `Each failure should`, so failure-mode prose must name the actual residual, downgrade, blocked-promotion, rollback, violation, or acceptance path directly.
- The repeated-prose guard now rejects `The invariant is`, so invariant sections must name the preserved boundary directly instead of falling back to a generic invariant opener.
- The repeated-prose guard now rejects `The minimum should`, so MVI sections must name the concrete first fixture, ledger, checklist, or evaluation slice directly.
- The repeated-prose guard now rejects fixture caveat formulas such as `The fixture validates`, `The fixture is not`, and `The fixture is only`, so MVI and proof-envelope passages must name the concrete fixture surface and non-claim boundary directly.
- The repeated-prose guard now rejects `This is why`, so causal transitions must name the specific layer, record, authority change, or consequence directly.
- The repeated-prose guard now rejects `This matters because`, so causal explanations must be integrated into chapter-specific prose rather than attached as reusable explanatory scaffolding.
- The repeated-prose guard now rejects `The result is`, so summaries and transitions must name the actual bridge, discipline, lifecycle, or artifact path directly.
- The repeated-prose guard now rejects `Operating mechanism:`, the exact `remains a target architecture, not a current-result claim` disclaimer, and the reusable `keeps ... honest` cadence, so mature-endpoint prose must integrate operation, evidence, interface, upgrade, closure, and non-claim boundaries in chapter-specific language.
- Appendix K is generated from the manifest and machine-checked as a book-wide implementation horizon map: one concrete first-build slice and one mature target endpoint per chapter, in manifest order.
- Current source-note coverage, source-to-chapter assignment, core claim mapping, and passage-review mapping are internally traceable.
- Current proof targets are wired through outline tags, generated manifest records, triage records, Lean modules, root imports, chapter hooks, limitation prose, and Appendix E.
- Current schemas and example fixtures validate record shape for the protocol surfaces created so far.
- The live site can project the same source into the default AI/research surface and a cleaner Human view without creating a parallel manuscript; the bridge guard now rejects the recurring formulas found during the editorial pass.
- The live book renders locally and through GitHub Pages when the publication workflow passes.

## What It Does Not Prove

- It does not prove any ASI capability, model quality, deployment readiness, safety property, benchmark result, simulation result, or runtime behavior.
- It does not prove that source interpretation is semantically adequate for support-state promotion.
- It does not prove that the finite-record Lean predicates are the best formalization of each intended chapter boundary.
- It does not reproduce MoECOT, Talos, VCM, PlanForge, policy-optimization, compression, routing, benchmark, or simulation results. Circle reproduction is limited to the external local build and receipt slice recorded in `docs/circle_external_receipt_slice.md`; Project Theseus import is limited to the static digest-verified architecture-gate report fixture recorded in `docs/theseus_report_import_slice.md` and the static digest-verified generation-mode gate fixture recorded in `docs/theseus_generation_mode_import_slice.md`, and bounded public task-bundle import recorded in `docs/theseus_public_task_bundle_import.md`. Those slices do not imply model quality, reasoning ability, context length, speed, memory scaling, deployment safety, transfer, or ASI.
- It does not publish the reviewed local reader HTML artifact to GitHub Pages or an external archive, and it does not fully review, release, or publish EPUB, PDF, DOCX, AZW3, MOBI, MP3, M4B, or audio-embedded EPUB artifacts. Local ignored EPUB/DOCX/PDF snapshots exist only as dry-run review outputs with basic structural, EPUB metadata/source-spine probe, DOCX conversion-probe, PDF-probe, and representative EPUB/PDF/DOCX sampling; the current EPUB, DOCX, and PDF probes clear sampled source-appendix table collisions by using generated reader source cards, but EPUB still has no e-reader application review, DOCX still has no full application review, and PDF still has no full page-by-page layout review. The local ignored audio-script workspace now derives from the tracked curated reader manuscript, but it still exists only as a script-preparation probe with MP3/M4B/audio-embedded EPUB targets not generated.
- The live Human view is a convenience projection, not a reviewed reader-release manuscript and not a substitute for final human editorial review.

## Remaining Work Before v1.0 Evidence Release

- Continue claim-to-mechanism support review after the passage-reviewed mappings. The v1.0 claim-state coverage gate now records 22 chapter-core no-change transition records plus 22 explicit no-promotion decisions, and the v1.x disposition ledger records 44 per-chapter core-claim dispositions with 0 promoted core claims. Every active core chapter claim has a support-state decision and movement path while remaining at `argument`; accepted chapter-core upward evidence transitions are still required before any chapter core claim moves above `argument`.
- Continue from the initial semantic proof adequacy review: add richer state-machine semantics, executable behavior tests, empirical baselines, or imported artifacts before treating most finite-record predicates as adequate chapter formalizations.
- Implement or defer chapter-level Codex tests beyond protocol fixture validation, with explicit command, environment, and result records.
- Normalize additional external literature where the book currently has queues rather than direct source records and source notes.
- Import or reproduce additional prototype, benchmark, Circle, Theseus, MoECOT, VCM, Talos, PlanForge, compression, routing, or policy-training artifacts before using them as stronger evidence.
- Inspect additional local reader-format dry-run snapshots, then approve further reader-edition artifacts only after exact artifact review and an edition release record is ready to name exact reviewed outputs.
- Use `editions/reader_manuscript/v1_0/format_review_matrix.json` and `docs/reader_format_review_matrix.md` as the format-level release blocker ledger before any reader HTML, EPUB, DOCX, PDF, e-reader conversion, or audio-embedded EPUB artifact is called approved.
- Generate audio scripts and audio artifacts only from a reviewed reader edition, preserve the implementation-horizon sections in the script, and record exact produced artifacts.
- Continue the final reader-facing editorial pass over both the generated reader manuscript and representative live Human view chapters. The opening-chapter, Efficient ASI, Human Intent, System Boundaries, Evidence States, Personal Compute Hives, Command Contracts, Planning, Verification Bandwidth, Runtime Adapters, Labor OS, Circle Contracts, Generate-Verify-Repair, Fast Generation, RankFold/NeuralFold, Mathematical and Search Substrates, Policy Optimization, Artifact Steward Agents, Executable Specifications, and Virtual Context ABI overlays prove the semantic-delta path for reader-only prose; the standalone Semantic Representation overlay operations are retired after the fold. `docs/reader_chapter_review_matrix.md` now gives the 44-chapter queue for release-control review. All rows have generated-reader chapter-text review records, but release-record and artifact-review blockers remain on every row.
- Use `editions/reader_manuscript/v1_0/companion_note_routing.json`, `docs/reader_companion_note_routing_review.md`, and the twelve drafting files under `editions/reader_manuscript/v1_0/companion_notes/` for the current dense planning/routing/hive/compression/speed/resource/proof/cyclic-substrate/policy/governance/implementation-reference companion-note candidates; generated companion notes still need release review before e-reader or audio artifacts can rely on them.
- Add a DOI/Zenodo identifier only after the archive exists; until then, the v1.0.0 release record explicitly preserves DOI pending.

## Release Gate

Before tagging or continuing to describe a state as a v1.0.0 release, run:

```bash
python3 scripts/sync_scaffold.py
git diff --exit-code
python3 scripts/sync_proof_manifest.py --check
python3 scripts/validate_chapter_dod.py
python3 scripts/validate_architecture_red_team.py
python3 scripts/validate_release_reproducibility.py
python3 scripts/validate_proof_artifact_audit.py
python3 scripts/validate_source_evidence_audit.py
python3 scripts/validate_core_claim_decisions.py
python3 scripts/validate_external_sota_positioning.py
python3 scripts/validate_claim_ledger_revision.py
python3 scripts/validate_proof_carrying_claims.py
python3 scripts/validate_tribunal_review.py
python3 scripts/validate_value_conflicts.py
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
python3 scripts/validate_capacity_smoothing.py
python3 scripts/validate_costed_route_resource_slice.py
python3 scripts/validate_resource_workflow_trace.py
python3 scripts/validate_resource_live_probe.py
python3 scripts/validate_resource_ci_cost_profile.py
python3 scripts/validate_circle_external_receipt_slice.py
python3 scripts/validate_circle_public_replay.py
python3 scripts/validate_phase5_harness_registry.py
python3 scripts/validate_publication.py
python3 scripts/validate_release_profiles.py
python3 scripts/validate_reading_mode_toggle.py
python3 scripts/validate_public_site_accessibility.py
python3 scripts/validate_v1_release_gate_audit.py
python3 scripts/validate_human_reading_paths.py
python3 scripts/validate_source_appendices.py
python3 scripts/validate_v1_status_snapshot.py
python3 scripts/validate_outline_consistency.py
python3 scripts/validate_implementation_horizons.py
python3 scripts/validate_reader_evidence_boundaries.py --check
python3 scripts/build_reader_edition.py --check
python3 scripts/sync_reader_overlay_asset.py --check
python3 scripts/validate_reader_overlays.py --check
python3 scripts/audit_reader_continuity.py --check
python3 scripts/validate_reader_manuscript_manifest.py
python3 scripts/validate_reader_artifact_inspection_manifest.py
python3 scripts/validate_reader_epub_probe_manifest.py
python3 scripts/validate_reader_docx_probe_manifest.py
python3 scripts/validate_reader_pdf_probe_manifest.py
python3 scripts/validate_reader_audio_script_probe_manifest.py
python3 scripts/sync_reader_chapter_review_matrix.py --check
python3 scripts/sync_reader_format_review_matrix.py --check
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
node scripts/validate_live_human_view_browser.js --all-chapters --all-viewports
```

Before describing a state as a v1.0 evidence release, also record the accepted evidence transitions, rendered reader artifacts if any, audio artifacts if any, and release records that actually exist.
