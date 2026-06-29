# v1.0 Focus Audit

Last audited: 2026-06-28

This audit is a planning surface for the next ASI Stack work cycle. It answers two questions:

- What is already strong enough to rely on while writing and improving the book?
- Where should effort go next if the goal is a final-quality living book rather than a large but unproven draft?

It does not promote any claim support state, report any new source result, report any benchmark result, or claim that reader, ebook, document, or audio release artifacts have been reviewed or published.

## Audit Basis

The audit is based on the current repository state, the public-safe status documents, and these local checks:

```bash
python3 scripts/validate_v1_status_snapshot.py
python3 scripts/validate_source_evidence_audit.py
python3 scripts/validate_proof_artifact_audit.py
python3 scripts/validate_reader_spine.py --check
python3 scripts/validate_publication.py
python3 scripts/validate_visual_coverage.py
python3 scripts/validate_release_profiles.py
python3 scripts/validate_human_reading_paths.py
python3 scripts/validate_reader_evidence_boundaries.py --check
python3 scripts/sync_reader_overlay_asset.py --check
python3 scripts/validate_reader_overlays.py --check
python3 scripts/audit_reader_continuity.py --check
python3 scripts/validate_reader_manuscript_manifest.py
python3 scripts/validate_outline_consistency.py
python3 scripts/validate_implementation_horizons.py
python3 scripts/validate_repeated_prose.py
python3 scripts/validate_schemas.py
python3 scripts/validate_protocol_examples.py
python3 scripts/validate_claim_ledger_revision.py
python3 scripts/validate_proof_carrying_claims.py
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
python3 scripts/render_reader_formats.py --check
python3 scripts/build_audio_script.py --check
python3 scripts/validate_book.py
python3 scripts/source_readiness_report.py
```

The checks passed in the audit run. The source-readiness command rewrote no tracked content. These checks are structural, traceability, render-readiness, or generated-workspace checks. They do not prove source interpretation, runtime behavior, benchmark quality, proof adequacy, reader-release review, or audiobook quality.

## Current Shape

| Surface | Current state | Interpretation |
|---|---:|---|
| Manifest parts | 4 | The book has a stable four-part architecture. |
| Manifest chapters | 54 | Coverage is broad enough that new chapters should be added only when a source or idea owns a genuinely new boundary. |
| Manifest claim contract | 54 explicit `claim_label` fields and 54 explicit `evidence_level` fields | Chapter records no longer rely on scaffold defaults for claim classification or support state; `validate_book.py` rejects missing or invalid values. |
| Appendices | 11 | Source, claim, schema, test, proof, release, lineage, and implementation-horizon surfaces exist. |
| Chapter body words | 185,317 | The book is already full-length; the main risk is not shortness. |
| Raw chapter-file words | 192,944 | Live scaffolding adds useful AI/research overhead beyond the reader spine. |
| Source records | 160 | The corpus is substantial, with 59 Corben/local records and 101 external records by current appendices. |
| Assigned source/chapter pairs | 461 | Chapter-source coverage is dense and traceable. |
| Exact claim-source mappings | 461 | Every assigned pair is mapped at the claim-source layer. |
| Passage-reviewed mappings | 461 | Every assigned pair has a recorded passage-review mapping state. |
| Core claim support states | 54 at `argument` | The book is still conservative. The v1.0 evidence-transition pilot now records fourteen accepted no-change decisions; no upward support transition exists. |
| Lean proof targets | 112 implemented finite-record targets | Traceability is complete; the initial proof adequacy review is recorded, Authority, Planning, Claim Ledger, and Proof-Carrying Claims now have finite record-envelope follow-through, Runtime Adapters has a synthetic permission harness feeding the adequacy review, Fast Generation has deterministic baseline-accounting fixtures that still do not replace model baselines, and Resource Economics has paired resource-budget accounting, deterministic budget-ledger coverage, and capacity-smoothing toy traces that remain too narrow for scheduler, real load, serving, or economic claims. Most targets still need stronger semantics, executable tests, empirical baselines, or imported artifacts before they can carry broader claims. |
| Schemas | 72 | Protocol record shapes are well-covered, and the dynamic book manifest now has a whole-file schema. |
| Protocol fixtures | 70 valid fixtures | Fixture validation is broad but not a substitute for runtime tests. |
| Test appendix rows | 236 | Appendix E now has 215 chapter-level rows plus 21 repository-level check rows. |
| Planned/unrun chapter test rows | 146 | The biggest technical evidence gap is still tests beyond shape validation, deterministic generation-mode accounting, synthetic gate fixtures, toy capacity traces, claim-ledger revision fixtures, proof-carrying claim fixtures, and narrow finite-record proofs. |
| Implemented or partial test/proof/check rows in Appendix E | 90 | Appendix E now has 68 implemented chapter rows, 1 partial chapter row, and 21 repository-level checks. Existing rows mostly validate fixtures, synthetic transition gates, synthetic claim-ledger revision discipline, synthetic proof-carrying claim discipline, synthetic plan-execution consistency, synthetic runtime-adapter permission consistency, synthetic context admission/adequacy consistency, synthetic readiness/residual gate consistency, synthetic benchmark anti-Goodhart consistency, deterministic generation-mode baseline and resource-budget accounting, deterministic resource-budget ledger discipline, capacity-smoothing toy traces, the Phase 5 harness registry, the reader continuity audit, Lean build, or proof/source traceability mechanics. |
| Reader spine | 54 chapters, minimum 1963 words | The generated reader source is structurally substantial. |
| Reader continuity audit | 54 chapters, 0 high-priority and 3 medium-priority heuristic review rows | The audit gives Phase 2 a deterministic human-review queue without claiming release readiness; `docs/reader_continuity_review.md` records the first manual decisions for the three medium rows. |
| Human Reading Path bridges | 54, minimum 170 words | Every chapter has a human-entry bridge. |
| Reader overlay operations | 33 active | The opening-chapter semantic overlay pilot, Efficient ASI table-to-prose pass, Human Intent table-to-prose pass, System Boundaries table-to-prose pass, Evidence States table-to-prose pass, Personal Compute Hives table/prose pass, Command Contracts table-to-prose pass, Planning table-to-prose pass, Verification Bandwidth table-to-prose pass, Runtime Adapters table-to-prose pass, Labor OS table-to-prose pass, Circle Contracts table/prose pass, Generate-Verify-Repair table-to-prose pass, Fast Generation table/code-to-prose pass, RankFold/NeuralFold table-to-prose pass, Mathematical and Search Substrates table-to-prose pass, Policy Optimization table-to-prose pass, Artifact Steward Agents table/prose pass, Executable Specifications prose pass, and Semantic Representation table-to-prose pass are active; broader reader continuity review and chapter-by-chapter overlays remain open. |
| Reader format readiness | HTML, EPUB, DOCX setup checks pass; a local dry run rendered 59 reader-site HTML files, 1 EPUB, and 1 DOCX, and snapshotted 81 HTML-site files/dependencies under ignored `build/reader_edition/format_artifacts/`; structural inspection passed for those snapshots; `docs/reader_artifact_inspection_manifest.md` now tracks the latest HTML/EPUB/DOCX structural summary with 59 HTML files, 62 EPUB XHTML entries, OPF language `en-US`, and 61 DOCX media entries; `docs/reader_epub_probe_manifest.md` tracks a 9,078,787-byte EPUB metadata/source-spine probe with sampled reader-note, evidence-boundary, and source-card entries while preserving the e-reader blocker; `docs/reader_docx_probe_manifest.md` tracks a 514-page, 8,190,162-byte LibreOffice conversion probe for the generated DOCX with representative source-card page samples; an isolated PDF probe failed without explicit locale settings but succeeded with `LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8`; `docs/reader_pdf_probe_manifest.md` tracks the latest UTF-8 PDF probe as 535 pages and 8,613,924 bytes with title/evidence-boundary text present and generated reader source-card appendices sampled; refreshed EPUB/PDF/DOCX sampling and a broader 28 page-view HTML layout/navigation probe are recorded; the synced format-review matrix now tracks 4 format rows with 4 full-review blockers, 4 release-record blockers, 1 application/e-reader blocker, and 1 full-PDF-layout blocker | `docs/reader_format_dry_run.md`, `docs/reader_artifact_inspection_manifest.md`, `docs/reader_epub_probe_manifest.md`, `docs/reader_docx_probe_manifest.md`, `docs/reader_pdf_probe_manifest.md`, `docs/reader_artifact_layout_review.md`, and `docs/reader_format_review_matrix.md` record local render, structural-inspection, EPUB/DOCX/PDF probe, representative layout-review outcomes, and format blockers, not reviewed or published release artifacts. |
| Audio script readiness | 59 script files generated for review | The check confirms script generation, not audio existence or review. |
| GitHub Pages workflow | Latest checked runs passing | Public deployment mechanics are healthy. |

## What Is Strong

### Architecture And Dynamic Structure

The project now has the right control plane. `book_structure.json` controls parts, chapter IDs, chapter order, source assignments, implementation horizons, claim labels, support states, and appendices. Quarto numbering is generated at render time. Chapter filenames are stable slugs. `scripts/add_chapter.py`, `scripts/add_part.py`, `scripts/chapter_adjacency_report.py`, `scripts/sync_scaffold.py`, `scripts/validate_book.py`, and `scripts/validate_chapter_handoffs.py` make insertion, movement, and deletion feasible without manual renumbering while requiring explicit claim-label and support-state fields.

The outline is also doing real work. `docs/book_outline.md` matches the manifest order, titles, core claims, assigned sources, and Lean proof targets. That makes it a usable source of truth for future "write the whole book" goals.

### Three-Audience Design

The book has a credible audience model:

- AI/writing-agent view: full live scaffold, source queues, proof hooks, validation commands, support states, and guardrails.
- Human researcher view: complete live book with matrices, sources, proof/test status, and residuals.
- Interested human view: on-site Human view and future reader/audio releases derived from the same source.

The `AI view` / `Human view` toggle is no longer just a visual idea. It has static validation, rendered HTML validation, and browser validation that can exercise every chapter across desktop and mobile. The generated reader source and live Human view share the reader-strip policy and overlay payload path.

### Evidence Boundaries

The source/evidence layer is disciplined. Appendix C records one core claim per manifest chapter, all core claims stay at `argument`, and exact claim-source mappings are present for assigned source/chapter pairs. Appendix G and Appendix H now separate Corben/local sources from external sources by other authors, which avoids confusing authorial lineage with third-party corroboration.

The strongest thing about the current evidence system is what it refuses to claim. It does not treat source notes, local raw caches, connector-readable documents, Lean finite-record predicates, or protocol fixtures as proof of broad ASI behavior.

### Validation Surface

The project has a serious local and CI validation loop:

- Manifest/scaffold sync.
- Outline/manifest consistency.
- Chapter definition-of-done checks.
- Handoff continuity.
- Human Reading Path coverage.
- Reader-spine and reader evidence-boundary checks.
- Reader-overlay checks.
- Source appendix ownership checks.
- Source/evidence audit.
- Proof artifact audit.
- Schema and protocol fixture validation.
- Repeated-prose ratchets.
- Visual coverage and diagram-walkthrough checks.
- Live Human view validation.
- Lean build.
- Quarto render.

This is exactly the right substrate for a living book. Future work should extend this loop into semantic review, tests, and release records instead of adding redundant scaffold checks.

## What Is Not Yet Established

The current repository does not yet establish the following:

- Any ASI capability, model-quality gain, deployment readiness, safety theorem, benchmark result, simulation result, or runtime behavior.
- That source interpretation is semantically adequate for support-state promotion.
- That all 112 finite-record Lean predicates are the best formalization of the intended chapter boundaries.
- That protocol fixtures validate behavior beyond schema shape.
- That MoECOT, Theseus, Circle, Talos, VCM, PlanForge, compression, routing, policy-optimization, benchmark, or simulation claims have been reproduced here.
- That a reviewed reader-release manuscript exists.
- That reviewed or published EPUB, PDF, DOCX, AZW3, MOBI, MP3, M4B, or audio-embedded EPUB release artifacts exist. Local ignored HTML/EPUB/DOCX snapshots now exist only as dry-run review outputs.
- That the Human view has been fully read as a polished book, even though its mechanics validate.
- That diagrams are all optimal explanatory diagrams, even though every chapter has substantive diagram coverage and reading notes.

These are not failures. They are the correct next frontier after a strong scaffold.

## Highest-Leverage Focus Areas

| Priority | Focus area | Current strength | Main gap | Best next artifact |
|---|---|---|---|---|
| P0 | Human-reader continuity review | Generated reader spine is substantial and mechanically clean; `docs/reader_continuity_audit.md` gives the review pass a deterministic heuristic queue; `docs/reader_continuity_review.md` records first manual decisions for the medium rows; `docs/reader_part_i_review_pass.md` records eight first-pass Part I decisions including one canonical prose cleanup; `docs/reader_part_ii_review_pass.md` records eleven first-pass Part II decisions including three canonical prose cleanups; `docs/reader_part_iii_review_pass.md` records eight first-pass Part III decisions including three canonical prose cleanups; `docs/reader_part_iv_review_pass.md` records five first-pass Part IV decisions plus a reader-generator capitalization cleanup; `docs/reader_opening_full_review_pass.md` records the first release-grade chapter-text review for the opening three chapters; `docs/reader_boundary_full_review_pass.md` records the second full chapter-text review for the failure/evidence/intent boundary sequence; `docs/reader_normative_full_review_pass.md` records the third full chapter-text review for the constitutional/agency/value-conflict sequence; `docs/reader_part_i_full_review_completion.md` records the Part I full-review completion pass; `docs/reader_part_ii_contracts_full_review_pass.md` records the first Part II contracts full-review pass; `docs/reader_part_ii_context_full_review_pass.md` records the first Part II context/compiler full-review pass; `docs/reader_part_ii_verification_full_review_pass.md` records the first Part II verification/evidence full-review pass; `docs/reader_part_ii_full_review_completion.md` records the Part II full-review completion pass; `docs/reader_part_iii_opening_full_review_pass.md` records the Part III opening full-review pass; `docs/reader_part_iii_compression_full_review_pass.md` records the Part III compression/generation full-review pass; `docs/reader_part_iii_representation_full_review_pass.md` records the Part III representation/resource full-review pass; `docs/reader_part_iii_iv_proof_bridge_full_review_pass.md` records the Part III-IV proof-bridge full-review pass; `docs/reader_part_iv_evidence_governance_full_review_pass.md` records the Part IV evidence/governance full-review pass; `docs/reader_part_iv_completion_full_review_pass.md` records the final Part IV completion pass; `docs/curated_reader_graduation_review.md` records the no-graduation decision for v1.0; and `docs/reader_chapter_review_matrix.md` now tracks the manifest-synced 54-chapter review queue with 54 `reviewed`, 0 `spot_checked`, 0 `not_started`, 20 active-overlay chapters, 54 no-immediate-action decisions, 3 companion-note candidates, and 1 curated-manuscript candidate. | No reader release exists; all rows still need release records or artifact review, and no curated reader chapter files exist. | Move from generated-reader chapter-text review into companion-note routing, EPUB/DOCX/PDF artifact inspection, and release records; graduate curated prose only when edits become too broad for overlays. |
| P0 | Claim-to-mechanism support review | 461 mappings are exact and passage-reviewed, with fourteen accepted no-change decisions now preserving support boundaries for book-method, control, claim-ledger, fast-generation, efficiency, and resource-accounting claims. | No accepted evidence transitions have promoted claims above `argument`. | Evidence transition records for a small number of narrow claims, or explicit decisions to keep them at `argument`. |
| P0 | Test/prototype execution | 72 schemas and 70 fixtures validate record shape, including the manifest schema, with twelve synthetic or deterministic behavior/accounting harnesses now wired into validation and registry-checked. | 146 Appendix E chapter rows remain planned/not run. | Next executable test harnesses should move toward replayable empirical slices or imported prototype traces with command, environment, result, and non-claim boundaries. |
| P0 | Proof adequacy follow-through | 112 Lean targets build, the initial adequacy review classifies the target set, Authority has a record-aware allow/deny/escalate decision envelope, Planning has a record-aware dispatchable/blocked/replanned control envelope, Claim Ledger and Proof-Carrying Claims have finite record envelopes, Runtime Adapters has a synthetic permission/approval/receipt harness, Fast Generation has deterministic baseline-accounting fixtures plus an explicit no-change evidence decision, and Resource Economics now has paired resource-budget accounting, deterministic budget-ledger coverage, capacity-smoothing toy traces, and an explicit no-change evidence decision. | Most targets remain useful-but-narrow or require richer state semantics, executable tests, empirical baselines, or imported artifacts before they can strengthen prose. | Continue one cluster at a time: implement a stronger predicate/test path or record an explicit no-promotion decision without support-state promotion. |
| P1 | External literature normalization | Initial source-noted records now exist across alignment/control, governance/evals, planning/agent control, retrieval/context, formal methods, routing/MoE, compression/representation, benchmark science, fast generation, policy optimization, hives, and artifact stewardship. Planning now includes ReAct, Tree of Thoughts, PDDL, SHOP2, Integrated TAMP, behavior trees, GOAP/F.E.A.R., and AutoGen; retrieval/context now includes RAG, Lost in the Middle, MemGPT, LongBench, RULER, ALCE, Self-RAG, and LongLLMLingua; formal methods now includes proof-carrying code, TLA+, Lean theorem proving, Dafny, Reluplex, Black-Box Simplex, Copilot, and PRISM; routing/MoE now includes sparse MoE, GShard, Switch Transformers, Expert Choice Routing, Mixtral, an MoE-in-LLMs survey, FrugalGPT, Hybrid LLM, and RouteLLM; compression now includes Deep Compression, LoRA, knowledge distillation, GPTQ, QLoRA, DreamCoder, Information Bottleneck, MDL, and CodeBLEU; benchmark science now includes MMLU, BIG-bench, HELM, GPQA, SWE-bench, LiveBench, Dynabench, CheckList, benchmark-contamination work, and Goodhart variants as comparison vocabulary. | Coverage is still selective; PlanForge-translation comparison, context-engineering surveys, VCM-specific adapter references, richer proof-assistant adequacy, ASI Stack protocol-verification sources, governance-aware route-selection literature, routing-specific modular-agent orchestration, compression-regression testing, additional representation-learning sources, hidden-holdout operations, saturation analysis, evaluator-gaming work, and release-grade benchmark governance remain queued. | Add citation-normalized source records and source notes only after reading the sources, without turning external comparison vocabulary into support-state promotion. |
| P1 | Reader release dry run | Reader generation and HTML/EPUB/DOCX/PDF local render paths have been probed; `docs/reader_format_dry_run.md` records a local HTML/EPUB/DOCX dry run, structural inspection, EPUB metadata/source-spine probe, DOCX LibreOffice conversion probe, and UTF-8 PDF probe with ignored snapshots; `docs/reader_artifact_inspection_manifest.md` now preserves a tracked HTML/EPUB/DOCX structural-inspection summary; `docs/reader_epub_probe_manifest.md` records the current 9,078,787-byte EPUB probe with `en-US` metadata and sampled source-card entries; `docs/reader_docx_probe_manifest.md` records the current 514-page, 8,190,162-byte DOCX conversion probe and sampled source-card pages; `docs/reader_pdf_probe_manifest.md` records the current 535-page, 8,613,924-byte PDF probe and sampled source-card pages; `docs/reader_artifact_layout_review.md` records refreshed EPUB/PDF/DOCX sampling and a broader 28 page-view HTML layout/navigation probe; `docs/reader_format_review_matrix.md` now keeps the format blockers structured. | No actual reviewed reader artifact or release record is recorded; EPUB, DOCX, and PDF source appendices now render as reader source cards in the sampled outputs, but EPUB has not received e-reader application review, DOCX has not received full Word/LibreOffice GUI/Google Docs review, and PDF has not received page-by-page layout review. | Continue EPUB e-reader inspection, broader DOCX/PDF layout review, and release-record preparation only if the reviewed artifacts pass, updating the format-review matrix rather than clearing blockers in prose. |
| P1 | Visual and diagram quality | Every chapter has a Mermaid diagram and walkthrough note; the first mobile screenshot pass improved dense Mermaid readability with contained diagram scrolling, and the Fast Generation plus Recursive Self-Improvement mechanisms have been split into smaller diagrams. | Validation proves coverage, not full explanatory excellence or e-reader artifact quality. | Continue manual diagram review during reader-release work, especially e-reader legibility for split diagrams. |
| P1 | Public-site UX/accessibility | Pages deploy, Human view validates, and `docs/site_visual_phase7_review.md` now records the first visual/mobile diagram pass, a source-growth browser probe over the landing page, dense chapters, and Appendices A/C/H, and an inline-code overflow follow-up that fixed Appendix F and rechecked Appendices A/C/F/H/K with zero page-level overflow at inspected desktop/mobile sizes. | Site quality beyond mechanics still needs broader human inspection and should not be described as accessibility-certified. | Continue browser screenshots and manual notes for landing page, nav, mobile reading, table overflow after future growth, toggle clarity, and diagram legibility. |
| P2 | Citation and bibliography polish | Source ownership is clear. | 59 Corben/local records still use stable source IDs rather than normalized citation metadata. | Citation-normalization pass where metadata is actually known, preserving unknowns honestly. |
| P2 | Manifest schema hardening | `schemas/book_structure.schema.json` now records the whole-file manifest contract for top-level metadata, parts, source queues, chapters, claim labels, support states, source mappings, implementation horizons, test rows, proof targets, and appendices; `scripts/validate_book.py` validates `book_structure.json` against that schema before running semantic source/proof checks. | The schema validates manifest shape, not source interpretation, proof adequacy, runtime behavior, reader release readiness, or evidence promotion. | Maintain the schema alongside future manifest fields and keep semantic validators responsible for cross-file, source, proof, reader, and evidence boundaries. |
| P2 | Audio release path | Audio script generation check passes. | No reviewed audio script or audio artifacts exist. | Only begin after reader manuscript review; produce reviewed spoken-treatment notes before audio generation. |

## Recommended Work Packages

### 1. Reader Manuscript Review

Generate the reader edition, refresh `docs/reader_continuity_audit.md`, then read it like a book rather than like a validation target. The goal is not more word count. The goal is continuity, pacing, lack of duplicated scaffolding, readable transitions, and confidence that the ordinary prose carries all meaning-critical caveats after live-only sections are stripped.

Use the reader-overlay system only for human-reader presentation deltas that should not alter the canonical AI/research source. If the improvement also belongs in AI view, edit the chapter source instead.

Suggested review order:

1. Front matter, Part I, and Part II continuity.
2. Dense technical Part III chapters, especially routing, MoECOT, hives, fast generation, resource economics, simulations, mathematical substrates, Circle, coil memory, and cyclic mixers.
3. Part IV evidence and implementation chapters, especially proof envelope, benchmark ratchets, policy optimization, artifact steward agents, integrated reference architecture, prototype roadmap, and living-book methodology.
4. Appendices selected for reader release: glossary, Corben/local sources, external sources, release editions, and implementation horizons.

Output should be either canonical prose edits or tracked reader overlay operations, plus a reviewed residual list. Do not claim a reader release until a release record names actual rendered artifacts and review status.

The current automated audit identifies 0 high-priority and 3 medium-priority heuristic rows after the table-to-prose and medium-density overlay pass. `docs/reader_continuity_review.md` records a first manual review of those rows: the two proof-heavy chapters are no-action for now with companion-note/glossary candidates, and the long Artifact Steward chapter is retained with future curated-reader compression as a possible release-editing task. The full-review passes through `docs/reader_part_iv_completion_full_review_pass.md` move all 54 chapters to reviewed generated-reader chapter-text status. `docs/reader_companion_note_routing_review.md` and `editions/reader_manuscript/v1_0/companion_note_routing.json` now route the three companion-note candidates for reader, e-reader, and audio treatment while preserving meaning-critical boundaries in the reader spine. The matrix itself is not a release review and should not be treated as release approval.

### 2. Evidence Transition Pilot

Do not attempt to promote all 54 core claims at once. Pick a small pilot set where the support boundary is narrow and the source basis is strongest.

Good first candidates:

- `evidence-states-and-claim-discipline`: the claim discipline is about the repository's own method and has strong internal artifacts.
- `living-book-methodology`: the repository itself demonstrates manifest-driven Quarto, source queues, claim/evidence matrices, proof manifests, tests, changelogs, and releases, but the claim must stay scoped to this project.
- `executable-specifications-and-lean-proof-envelope`: proof traceability is strong, while semantic proof adequacy still blocks broad promotion.
- `source appendices and implementation horizons`: these are generated public surfaces and can support narrow claims about book mechanics, not AI behavior.

For each pilot claim, record:

- Exact claim text.
- Proposed narrower support-state movement, if any.
- Source passages or repository artifacts used.
- Counterevidence or limitation.
- Command outputs, if commands matter.
- Evidence transition record.
- Appendix C update only after the transition is accepted.

Most claims may still remain at `argument`. A recorded non-promotion decision is useful evidence discipline.

### 3. First Executable Test Harnesses

The current test backlog is much larger than the implemented test surface. The first synthetic and deterministic harness set is now implemented and registry-validated; the next test work should prioritize replayable empirical slices, imported prototype traces, or richer deterministic harnesses that strengthen multiple chapters without overstating evidence.

Initial harness set:

| Harness | Chapters helped | Why first |
|---|---|---|
| Claim ledger revision harness | Claim ledgers, evidence states, proof-carrying claims, living-book methodology | Makes contradiction routing, revision history, affected surfaces, residuals, and support-state promotion blockers executable. |
| Proof-carrying claim harness | Spinoza, claim ledgers, proof envelope, UAT | Makes tier/justification matching, verifier artifact refs, failed-attempt preservation, formalization mismatch escalation, and non-promotion boundaries executable. |
| Support-state transition checker | Evidence states, claim ledgers, benchmark ratchets, living-book methodology | Directly supports the book's central evidence discipline. |
| Authority non-escalation / permission receipt tests | System boundaries, security kernel, runtime adapters, labor OS | Turns authority vocabulary into reject/accept behavior. |
| Plan graph and execution-contract tests | Intent contracts, command contracts, planning, PlanForge, cognitive compilation | Makes the planning/execution boundary executable. |
| Runtime adapter permission and approval tests | Runtime adapters, security kernel, Labor OS, artifact graphs | Turns effect-boundary vocabulary into permission, approval, receipt, rollback, and residual gate behavior. |
| Context admission vs adequacy tests | Virtual Context ABI, semantic pages, context transactions, verification bandwidth | Tests a core memory/reasoning interface. |
| Readiness gate and residual escrow tests | Routing, readiness gates, MoECOT, prototype roadmap, recursive self-improvement | Converts promotion-blocking language into synthetic cross-record gate behavior. |
| Benchmark ratchet anti-Goodhart tests | Benchmark ratchets, policy optimization, artifact steward agents | Keeps benchmark, policy-update, and steward-release handoffs from treating proxy scores as authority. |
| Generation mode baseline accounting tests | Fast generation architectures, efficient ASI hypothesis, resource economics | Keeps useful-solution-per-second, quality, residual, baseline, and fallback accounting together before any fast-generation claim can move. |
| Resource budget ledger tests | Resource economics, efficient ASI hypothesis, planning, runtime adapters, benchmark ratchets | Makes dispatch, escalation, protected overhead, displaced-cost residualization, review-capacity hoarding, evidence refs, and no-promotion boundaries executable before any resource-economics claim can move. |
| Capacity smoothing toy traces | Resource economics, efficient ASI hypothesis, planning, PlanForge | Makes bounded regeneration arithmetic, priority deferral, scope reduction, overload rejection, and no-promotion boundaries executable without claiming real load stability. |

The set is registered in `experiments/phase5_harness_registry.json`, documented in `docs/phase5_harness_registry.md`, and checked by `python3 scripts/validate_phase5_harness_registry.py`. The registry guard verifies command scripts, docs, fixture counts, result records, Appendix E rows, public status references, primary chapter mappings, non-claim boundaries, and `scripts/validate_book.py` wiring.

Each future harness should write public-safe results under a tracked result or report location only after it actually runs. If a test is negative, failed, or inconclusive, keep that result visible. The current harnesses remain synthetic record gates, synthetic cross-record gates, deterministic accounting gates, claim-ledger revision fixtures, proof-carrying claim fixtures, and toy capacity traces only; they do not prove source interpretation, open-domain claim extraction, theorem validity, semantic equivalence, citation accuracy, verifier quality, belief-engine correctness, routing accuracy, deployed authorization, planner quality, adapter runtime safety, memory correctness, benchmark quality, generation speed, model quality, budget scheduling, real load stability, economic outcomes, policy-training quality, steward-agent behavior, runtime safety, or support-state promotion.

### 4. Proof Adequacy Review

The Lean workspace is valuable because it makes local invariants executable and checkable. The risk is that a finite-record predicate can look stronger than it is.

The next proof work should classify each proof target:

- Adequate finite-record invariant for the chapter's current claim boundary.
- Useful but too narrow to affect support state.
- Needs richer state-machine semantics.
- Needs executable test or schema before Lean is meaningful.
- Should stay as research agenda rather than Lean.

The current `proofs/proof_triage.json` routes all 112 targets as `formal-invariant` and `lean-candidate`. That is coherent for the current proof envelope, but a mature v1.0 evidence release should be more discriminating. The first follow-through increments show the intended pattern: strengthen one finite-record cluster, update the public adequacy boundary, then record a no-promotion decision unless the stronger predicate actually supports a narrowed claim.

### 5. External Literature Backfill

The external-source appendix already covers important fast-generation, policy-optimization, personal-compute-hive, and artifact-steward context. It does not yet cover all areas where a serious public technical book will be judged against outside literature.

Prioritize these queues:

1. Alignment, corrigibility, and power-seeking literature for Part I.
2. AI governance, evaluations, deployment policy, incident response, and model evals for readiness and governance chapters.
3. Planning, task decomposition, PlanForge translation, and deeper planning-runtime adapter comparisons after the initial ReAct, Tree of Thoughts, PDDL, SHOP2, TAMP, behavior-tree, GOAP/F.E.A.R., and AutoGen records.
4. RAG, memory systems, context engineering, long-context evaluation, and context-compilation work for VCM chapters.
5. Formal methods, proof assistants, runtime assurance, generated monitors, probabilistic model checking, and contract verification for proof chapters.
6. Mixture-of-experts, model routing, modular agents, and systems routing for MoECOT/RMI/routing chapters.
7. Compression, representation learning, program synthesis, and residual/error accounting for CGS, RankFold/NeuralFold, BBVCA, and semantic representation chapters.
8. Benchmark science, contamination, saturation, hidden tests, and eval gaming for benchmark ratchets.

Do not cite a source from memory. Add a source record, read it, create a source note, assign only relevant chapters, then update mappings.

### 6. Release Artifact Dry Run

The first local HTML/EPUB/DOCX dry run, structural artifact inspection, EPUB
metadata/source-spine probe, DOCX LibreOffice conversion probe, UTF-8 PDF
probe, representative EPUB/PDF/DOCX sampling, and broader HTML
layout/navigation spot check are recorded in
`docs/reader_format_dry_run.md`, `docs/reader_artifact_inspection_manifest.md`,
`docs/reader_epub_probe_manifest.md`, `docs/reader_docx_probe_manifest.md`,
`docs/reader_pdf_probe_manifest.md`, and `docs/reader_artifact_layout_review.md`.
They produced ignored snapshots and local reports for review, not a release. The
continuing sequence is:

1. Generate the reader source.
2. Review the generated reader manuscript and delta report.
3. Continue manual inspection of the local HTML, EPUB, DOCX, and PDF snapshots
   for navigation, figures, tables, diagrams, wrapping, and bibliography
   behavior, starting with EPUB e-reader behavior and broader DOCX/PDF
   source-card and appendix layout review.
4. Keep the explicit UTF-8 locale environment in the PDF render command unless
   the local Quarto/PDF setup is changed and re-tested.
5. Record exact produced artifacts only after they exist, have been reviewed,
   and have an edition release record.

The audiobook path should wait. Audio scripts are useful review workspaces, but audio should not start until the reader manuscript is reviewed.

### 7. Visual Quality Review

Mermaid coverage is now present across every chapter. The next visual pass should ask harder questions:

- Does the diagram explain the main boundary of the chapter, or only restate section names?
- Is it legible on mobile and e-reader-sized surfaces?
- Does it preserve evidence boundaries, or could it imply implementation/proof status?
- Should a dense diagram be split into a lifecycle diagram plus a record schema diagram?
- Does the diagram walkthrough actually help a reader understand the state transition?

Only add generated bitmap images where they carry meaning. Avoid decorative image work until diagrams and reader figures are clear.

### 8. Public-Site Inspection

The live site works mechanically. A human public-site pass should inspect:

- Landing page first impression and status honesty.
- Human view toggle placement, labeling, and persistence.
- Mobile and desktop navigation.
- Table overflow in source and claim appendices.
- Mermaid sizing and contrast.
- Reader flow when opened directly with `?view=human`.
- Whether the site makes the living/evidence-release distinction obvious.

The browser validator is necessary but not sufficient. It catches broken mechanics, not taste, pacing, or trust.

## Do Not Spend Much Effort Here Yet

- Adding many new chapters without a genuinely new boundary.
- Promoting support states because the prose sounds good.
- Producing audio before a reviewed reader manuscript.
- Treating source notes as external validation.
- Expanding Lean proofs without adequacy review.
- Adding decorative images before diagram and reader-legibility review.
- Polishing marketing copy while evidence transitions, tests, and reader review remain open.

## Suggested Focus Order

The best next sequence is:

1. Reader manuscript review and overlay/canonical prose corrections.
2. Evidence transition pilot on a small set of narrow repository-method claims.
3. First executable test harnesses for claim-ledger revision, proof-carrying claims, support transitions, authority, planning, runtime adapters, context adequacy, readiness gates, and benchmark ratchets.
4. Proof adequacy review across all 112 Lean targets.
5. External literature backfill for alignment/governance/planning/memory/formal-methods/routing/compression/benchmark areas.
6. Manual reader release dry-run inspection of the actual local HTML/EPUB/DOCX/PDF snapshots, including EPUB e-reader behavior and source-appendix card behavior in EPUB, DOCX, and PDF.
7. Visual and public-site quality review.
8. Audio script review and eventual audio artifact generation only after the reviewed reader release exists.

## Current Blocking Conditions

The project is not blocked from further writing or improvement. It is blocked from calling itself a v1.0 evidence release until these conditions are handled:

- Accepted evidence transitions exist for any claim moved above `argument`.
- Semantic proof adequacy review is recorded.
- At least the intended first wave of chapter-level tests is implemented, run, and recorded, or explicitly deferred.
- External literature queues are normalized where the book relies on outside comparison.
- Reader manuscript review is recorded before reader artifacts are called published.
- Actual format renders, artifact review, and release records exist before EPUB, PDF, DOCX, or other artifacts are claimed as release artifacts.
- Audio script review, generated audio, spot checks, and release records exist before any audiobook or audio-embedded EPUB is claimed.

## Bottom Line

The repo is no longer in scaffold-building mode. It is in evidence-release and reader-quality mode.

The highest-value work is to review the generated human manuscript, run a narrow evidence-transition pilot, implement the first real tests, review the semantic adequacy of the Lean proofs, and backfill third-party literature where outside grounding matters. That work will improve the book more than adding raw volume.
