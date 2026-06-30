# v1.0 Focus Audit

Last audited: 2026-06-29

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
python3 scripts/validate_public_site_accessibility.py
python3 scripts/validate_v1_release_gate_audit.py
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
| Manifest chapters | 46 | Coverage is broad enough that new chapters should be added only when a source or idea owns a genuinely new boundary. |
| Manifest claim contract | 46 explicit `claim_label` fields and 46 explicit `evidence_level` fields | Chapter records no longer rely on scaffold defaults for claim classification or support state; `validate_book.py` rejects missing or invalid values. |
| Appendices | 11 | Source, claim, schema, test, proof, release, lineage, and implementation-horizon surfaces exist. |
| Chapter body words | 167,911 | The book is already full-length; the main risk is not shortness. |
| Raw chapter-file words | 175,233 | Live scaffolding adds useful AI/research overhead beyond the reader spine. |
| Source records | 185 | The corpus is substantial, with Corben/local records and external records separated by the current appendices. |
| Assigned source/chapter pairs | 430 | Chapter-source coverage is dense and traceable. |
| Exact claim-source mappings | 430 | Every assigned pair is mapped at the claim-source layer. |
| Passage-reviewed mappings | 430 | Every assigned pair has a recorded passage-review mapping state. |
| Core claim support states | 46 at `argument` | The book is still conservative. The v1.0 evidence-transition gate now records twenty-two accepted no-change decisions, twenty-four explicit no-promotion decisions, two bounded `synthetic-test-backed` non-core transitions, and one bounded `prototype-backed` imported Circle receipt transition; no chapter core support transition exists. |
| Lean proof targets | 112 implemented finite-record targets | Traceability is complete; the initial proof adequacy review is recorded, Authority, Planning, Claim Ledger, and Proof-Carrying Claims now have finite record-envelope follow-through, Runtime Adapters has a synthetic permission harness feeding the adequacy review, Fast Generation has deterministic baseline-accounting fixtures that still do not replace model baselines, Resource Economics has paired resource-budget accounting, deterministic budget-ledger coverage, capacity-smoothing toy traces, and a bounded synthetic costed-route/resource-budget selector slice, and Circle has one bounded external rope receipt replay. These remain too narrow for scheduler, real load, serving, proof-contract transport, model-quality, transfer, or economic claims. Most targets still need stronger semantics, executable tests, empirical baselines, or imported artifacts before they can carry broader claims. |
| Schemas | 74 | Protocol record shapes are well-covered, and the dynamic book manifest now has a whole-file schema. |
| Protocol fixtures | 71 valid fixtures | Fixture validation is broad but not a substitute for runtime tests. |
| Test appendix rows | 230 | Appendix E now records 230 generated chapter-level rows plus a separate repository-level check section. |
| Planned/unrun chapter test rows | 125 | The biggest technical evidence gap is still tests beyond shape validation, deterministic generation-mode accounting, synthetic gate fixtures, toy capacity traces, claim-ledger revision fixtures, proof-carrying claim fixtures, tribunal-review fixtures, value-conflict fixtures, constitutional-predicate fixtures, governance-right fixtures, agency-right fixtures, security-kernel fixtures, stable-capability-field fixtures, replacement-transaction fixtures, self-improvement transition fixtures, and narrow finite-record proofs. |
| Implemented or partial test/proof/check rows in Appendix E | 128 | Appendix E now has 97 implemented chapter rows, 1 partial chapter row, and 30 repository-level checks. Existing rows mostly validate fixtures, synthetic transition gates, synthetic claim-ledger revision discipline, synthetic proof-carrying claim discipline, synthetic tribunal-review record discipline, synthetic value-conflict record discipline, synthetic constitutional-predicate record discipline, synthetic governance-right record discipline, synthetic agency-right checklist discipline, synthetic security-kernel receipt discipline, synthetic stable-capability-field qualification/routing discipline, synthetic replacement-transaction discipline, synthetic self-improvement transition discipline, synthetic plan-execution consistency, synthetic runtime-adapter permission consistency, synthetic context admission/adequacy consistency, synthetic readiness/residual gate consistency, synthetic benchmark anti-Goodhart consistency, deterministic generation-mode baseline and resource-budget accounting, deterministic resource-budget ledger discipline, capacity-smoothing toy traces, the bounded costed-route/resource-budget selector slice, the Phase 5 harness registry, the reader continuity audit, Lean build, or proof/source traceability mechanics. |
| Reader spine | 46 chapters, minimum 2,042 words | The generated reader source is structurally substantial. |
| Reader continuity audit | 46 chapters, 2 high-priority and 3 medium-priority heuristic review rows | The audit gives Phase 2 a deterministic human-review queue without claiming release readiness; `docs/reader_continuity_review.md` records manual decisions for earlier medium rows while `docs/reader_continuity_audit.md` remains the current queue. |
| Human Reading Path bridges | 46, minimum 170 words | Every chapter has a human-entry bridge. |
| Reader overlay operations | 33 active | The opening-chapter semantic overlay pilot, Efficient ASI table-to-prose pass, Human Intent table-to-prose pass, System Boundaries table-to-prose pass, Evidence States table-to-prose pass, Personal Compute Hives table/prose pass, Command Contracts table-to-prose pass, Planning table-to-prose pass, Verification Bandwidth table-to-prose pass, Runtime Adapters table-to-prose pass, Labor OS table-to-prose pass, Circle Contracts table/prose pass, Generate-Verify-Repair table-to-prose pass, Fast Generation table/code-to-prose pass, RankFold/NeuralFold table-to-prose pass, Mathematical and Search Substrates table-to-prose pass, Policy Optimization table-to-prose pass, Artifact Steward Agents table/prose pass, Executable Specifications prose pass, and Semantic Representation table-to-prose pass are active; broader reader continuity review and chapter-by-chapter overlays remain open. |
| Reader format readiness | HTML, EPUB, DOCX setup checks pass; a local dry run rendered 59 reader-site HTML files, 1 EPUB, and 1 DOCX, and snapshotted 81 HTML-site files/dependencies under ignored `build/reader_edition/format_artifacts/`; structural inspection passed for those snapshots; `docs/reader_artifact_inspection_manifest.md` now tracks the latest HTML/EPUB/DOCX structural summary with 59 HTML files, 62 EPUB XHTML entries, OPF language `en-US`, and 61 DOCX media entries; `docs/reader_html_artifact_browser_review.md` records a full local browser review of the generated reader HTML snapshot with 118 of 118 page-view pairs passing across all 59 pages at desktop and mobile widths; `release_records/2026-06-29-v1-reader-html-855dc277.json` records the reviewed local HTML snapshot from source tag `v1.0.0-reader-html-source`; `docs/reader_epub_probe_manifest.md` tracks a 9,078,787-byte EPUB metadata/source-spine probe with sampled reader-note, evidence-boundary, and source-card entries while preserving the e-reader blocker; `docs/reader_docx_probe_manifest.md` tracks a 514-page, 8,190,162-byte LibreOffice conversion probe for the generated DOCX with representative source-card page samples; an isolated PDF probe failed without explicit locale settings but succeeded with `LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8`; `docs/reader_pdf_probe_manifest.md` tracks the latest UTF-8 PDF probe as 535 pages and 8,613,924 bytes with title/evidence-boundary text present and generated reader source-card appendices sampled; refreshed EPUB/PDF/DOCX sampling is recorded; the synced format-review matrix now tracks 4 format rows with HTML release-approved for that local artifact, 3 full-review blockers, 1 application/e-reader blocker, and 1 full-PDF-layout blocker | `docs/reader_format_dry_run.md`, `docs/reader_artifact_inspection_manifest.md`, `docs/reader_html_artifact_browser_review.md`, `release_records/2026-06-29-v1-reader-html-855dc277.json`, `docs/reader_epub_probe_manifest.md`, `docs/reader_docx_probe_manifest.md`, `docs/reader_pdf_probe_manifest.md`, `docs/reader_artifact_layout_review.md`, and `docs/reader_format_review_matrix.md` record local render, structural-inspection, HTML browser-review, the exact HTML edition record, EPUB/DOCX/PDF probe, representative layout-review outcomes, and remaining format blockers. |
| Audio script readiness | 51 script files generated for review | The check confirms script generation, not audio existence or review. |
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
- That MoECOT, Theseus, Talos, VCM, PlanForge, compression, routing, policy-optimization, benchmark, or simulation claims have been reproduced here. Circle reproduction is limited to one bounded external rope receipt replay and does not support model-quality, transfer, deployment, or chapter-core claims.
- That a reviewed reader-release manuscript exists.
- That reviewed or published EPUB, PDF, DOCX, AZW3, MOBI, MP3, M4B, or audio-embedded EPUB release artifacts exist. Local ignored HTML/EPUB/DOCX snapshots now exist only as dry-run review outputs.
- That the Human view has been fully read as a polished book, even though its mechanics validate.
- That diagrams are all optimal explanatory diagrams, even though every chapter has substantive diagram coverage and reading notes.

These are not failures. They are the correct next frontier after a strong scaffold.

## Highest-Leverage Focus Areas

| Priority | Focus area | Current strength | Main gap | Best next artifact |
|---|---|---|---|---|
| P0 | Human-reader continuity review | Generated reader spine is substantial and mechanically clean; `docs/reader_continuity_audit.md` gives the review pass a deterministic heuristic queue; `docs/reader_continuity_review.md` records first manual decisions for the medium rows; `docs/reader_part_i_review_pass.md`, `docs/reader_part_ii_review_pass.md`, `docs/reader_part_iii_review_pass.md`, and `docs/reader_part_iv_review_pass.md` record first-pass part decisions; the full-review pass records from `docs/reader_opening_full_review_pass.md` through `docs/reader_part_iv_completion_full_review_pass.md` remain the historical review trail; `docs/curated_reader_graduation_review.md` records the no-graduation decision for v1.0; and `docs/reader_chapter_review_matrix.md` now tracks the manifest-synced 46-chapter review queue with 46 `reviewed`, 0 `spot_checked`, 0 `not_started`, 20 active-overlay chapters, 46 no-immediate-action decisions, 3 companion-note candidates, and 43 curated-manuscript candidates. | A minimum reviewed local reader HTML artifact now has an edition release record, but EPUB/DOCX/PDF/audio artifacts remain unapproved, the chapter matrix remains a review queue rather than final reader-manuscript release packaging, and curated reader chapter files remain drafting-only. | Continue EPUB e-reader inspection, broader DOCX/PDF layout review, audio-script review only after reader packaging, and curated prose graduation only when edits become too broad for overlays. |
| P0 | Claim-to-mechanism support review | 430 mappings are exact and passage-reviewed, with twenty-two accepted no-change decisions and twenty-four explicit no-promotion decisions preserving support boundaries for the current 46 chapter core claims; the separate measured set records three accepted non-core upward transitions. | No accepted chapter core evidence transition has promoted a chapter claim above `argument`. | Evidence transition records for a small number of narrow claims, or explicit decisions to keep chapter core claims at `argument`. |
| P0 | Test/prototype execution | 74 schemas and 71 fixtures validate record shape, including the manifest schema, with twenty-one synthetic or deterministic behavior/accounting harnesses now wired into validation and registry-checked; `docs/costed_route_resource_slice.md` records the first bounded non-infrastructure measured/replayed selector slice with baseline, negative control, fallback, residuals, and non-claims; `docs/circle_external_receipt_slice.md` records the first bounded imported external-prototype receipt slice. | 125 Appendix E chapter rows remain planned/not run, the costed-route slice is still synthetic selector evidence rather than a prototype scheduler, real route-quality trace, load test, or economic result, and the Circle receipt slice is not an ASI Stack consumer-gate trace or chapter-core proof-contract transport result. | Next executable test work should move toward replayable empirical slices, public proof-contract consumer gates, or deeper imported prototype traces with command, environment, result, and non-claim boundaries. |
| P0 | Proof adequacy follow-through | 112 Lean targets build, the initial adequacy review classifies the target set, Authority has a record-aware allow/deny/escalate decision envelope, Planning has a record-aware dispatchable/blocked/replanned control envelope, Claim Ledger and Proof-Carrying Claims have finite record envelopes, Runtime Adapters has a synthetic permission/approval/receipt harness, Fast Generation has deterministic baseline-accounting fixtures plus an explicit no-change evidence decision, and Resource Economics now has paired resource-budget accounting, deterministic budget-ledger coverage, capacity-smoothing toy traces, a bounded costed-route/resource-budget selector slice, and an explicit no-change decision for the chapter core claim. | Most targets remain useful-but-narrow or require richer state semantics, executable tests, empirical baselines, or imported artifacts before they can strengthen prose. | Continue one cluster at a time: implement a stronger predicate/test path or record an explicit no-promotion decision without support-state promotion. |
| P1 | External literature normalization | Initial source-noted records now exist across alignment/control, governance/evals, planning/agent control, retrieval/context, formal methods, routing/MoE, compression/representation, benchmark science, fast generation, policy optimization, hives, and artifact stewardship. Planning now includes ReAct, Tree of Thoughts, PDDL, SHOP2, Integrated TAMP, behavior trees, GOAP/F.E.A.R., and AutoGen; retrieval/context now includes RAG, Lost in the Middle, MemGPT, LongBench, RULER, ALCE, Self-RAG, and LongLLMLingua; formal methods now includes proof-carrying code, TLA+, Lean theorem proving, Dafny, Reluplex, Black-Box Simplex, Copilot, and PRISM; routing/MoE now includes sparse MoE, GShard, Switch Transformers, Expert Choice Routing, Mixtral, an MoE-in-LLMs survey, FrugalGPT, Hybrid LLM, and RouteLLM; compression now includes Deep Compression, LoRA, knowledge distillation, GPTQ, QLoRA, DreamCoder, Information Bottleneck, MDL, and CodeBLEU; benchmark science now includes MMLU, BIG-bench, HELM, GPQA, SWE-bench, LiveBench, Dynabench, CheckList, benchmark-contamination work, and Goodhart variants as comparison vocabulary. | Coverage is still selective; PlanForge-translation comparison, context-engineering surveys, VCM-specific adapter references, richer proof-assistant adequacy, ASI Stack protocol-verification sources, governance-aware route-selection literature, routing-specific modular-agent orchestration, compression-regression testing, additional representation-learning sources, hidden-holdout operations, saturation analysis, evaluator-gaming work, and release-grade benchmark governance remain queued. | Add citation-normalized source records and source notes only after reading the sources, without turning external comparison vocabulary into support-state promotion. |
| P1 | Reader release dry run | Reader generation and HTML/EPUB/DOCX/PDF local render paths have been probed; `docs/reader_format_dry_run.md` records a local HTML/EPUB/DOCX dry run, structural inspection, EPUB metadata/source-spine probe, DOCX LibreOffice conversion probe, and UTF-8 PDF probe with ignored snapshots; `docs/reader_artifact_inspection_manifest.md` now preserves a tracked HTML/EPUB/DOCX structural-inspection summary; `docs/reader_html_artifact_browser_review.md` records a full local browser review of the generated reader HTML snapshot with 118 of 118 page-view pairs passing; `release_records/2026-06-29-v1-reader-html-855dc277.json` records that exact local HTML artifact; `docs/reader_epub_probe_manifest.md` records the current 9,078,787-byte EPUB probe with `en-US` metadata and sampled source-card entries; `docs/reader_docx_probe_manifest.md` records the current 514-page, 8,190,162-byte DOCX conversion probe and sampled source-card pages; `docs/reader_pdf_probe_manifest.md` records the current 535-page, 8,613,924-byte PDF probe and sampled source-card pages; `docs/reader_format_review_matrix.md` now keeps the format blockers structured. | HTML has passed full local browser artifact review and has a source-tagged edition release record for the local ignored snapshot; EPUB, DOCX, and PDF source appendices now render as reader source cards in sampled outputs, but EPUB has not received e-reader application review, DOCX has not received full Word/LibreOffice GUI/Google Docs review, and PDF has not received page-by-page layout review. | Continue EPUB e-reader inspection, broader DOCX/PDF layout review, and release-record preparation only for additional artifacts that pass; keep audio deferred until the reader package is explicitly ready. |
| P1 | Visual and diagram quality | Every chapter has a Mermaid diagram and walkthrough note; the first mobile screenshot pass improved dense Mermaid readability with contained diagram scrolling, and the Fast Generation plus Recursive Self-Improvement mechanisms have been split into smaller diagrams. | Validation proves coverage, not full explanatory excellence or e-reader artifact quality. | Continue manual diagram review during reader-release work, especially e-reader legibility for split diagrams. |
| P1 | Public-site UX/accessibility | Pages deploy, Human view validates, `docs/site_visual_phase7_review.md` records visual/mobile and overflow passes, and `docs/public_site_accessibility_review.md` plus `scripts/validate_public_site_accessibility.py` now record candidate accessibility readiness for assistive toggle hooks, focus-visible CSS, mobile Mermaid containment, landing-image alt text, diagram walkthrough coverage, residuals, and non-claims. | Site quality beyond mechanics still needs broader human inspection and must not be described as accessibility-certified, WCAG-conformant, screen-reader approved, or e-reader approved. | Continue manual keyboard-only review, screen-reader review, measured contrast audit if desired, browser screenshots after future growth, and e-reader-specific diagram/table review. |
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

The current automated audit identifies 2 high-priority and 3 medium-priority heuristic rows after the table-to-prose and medium-density overlay pass. `docs/reader_continuity_review.md` records a first manual review of earlier medium rows: the two proof-heavy chapters are no-action for now with companion-note/glossary candidates, and the long Artifact Steward chapter is retained with future curated-reader compression as a possible release-editing task. The full-review trail through `docs/reader_part_iv_completion_full_review_pass.md` now maps into a 46-chapter reviewed generated-reader queue after consolidation. `docs/reader_companion_note_routing_review.md` and `editions/reader_manuscript/v1_0/companion_note_routing.json` route the three companion-note candidates for reader, e-reader, and audio treatment while preserving meaning-critical boundaries in the reader spine. The matrix itself is not a release review and should not be treated as release approval.

### 2. Next Evidence Transition

Do not attempt to promote all 46 core claims at once. The initial v1.0
claim-state pass is complete: every chapter core claim now has either an
accepted no-change transition or an explicit no-promotion decision, and the
three upward transitions are bounded to repository infrastructure, a synthetic
costed-route/resource-budget selector slice, and one imported Circle rope
receipt replay. The next evidence move should be a deeper prototype, empirical,
replayed, or imported-trace slice with a
public-safe command, input, output, baseline or negative control, residuals,
and non-claims.

Good next candidates:

- Additional Theseus/Circle transfer receipts where the source artifact can be inspected,
  built, replayed, or linked without smuggling private artifacts into the
  public repo.
- A real route-quality/resource-budget trace that compares at least one
  adequate route, one negative control, and one overkill baseline while keeping
  economic and model-quality non-claims explicit.
- Context-admission, compression, planner/runtime, or benchmark-governance
  traces that can run from tracked fixtures or public-safe inputs.
- Narrow repository-method claims only when the claim text is explicitly about
  this book's own validation, release, source, proof, or evidence machinery.

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
| Tribunal review harness | UAT, Spinoza, moral uncertainty, benchmark ratchets | Makes dossier boundaries, reviewer roles, adversarial probes, evidence-backed accept verdicts, dissent preservation, prior-review guards, required actions, constraint effects, and non-claim boundaries executable. |
| Value conflict harness | Moral uncertainty, UAT, governance rights, constitutional alignment | Makes multi-axis conflict classification, high-stakes review routing, residual uncertainty, authority narrowing, dissent payloads, and revisit conditions executable. |
| Constitutional alignment harness | Constitutional alignment, moral uncertainty, agency, recursive self-improvement | Makes protected scope, operational tests, conflict routing, review routes, self-modification weakening rules, migration policies, least-sufficient-power behavior, uncertainty preservation, and non-claim boundaries executable. |
| Governance rights harness | Governance rights, agency, stable capability fields, artifact stewardship | Makes audit material and receipts, redaction appeals, exit/fork access paths, fork safety constraints, preservation obligations, durable records, and non-claim boundaries executable. |
| Agency rights harness | Agency, governance rights, constitutional alignment, runtime adapters | Makes affected parties, bounded delegation, material usability, timing-before-effect review, review/appeal paths, corrigibility paths, high-impact approval, residual dependency risk, and accountability executable. |
| Support-state transition checker | Evidence states, claim ledgers, benchmark ratchets, living-book methodology | Directly supports the book's central evidence discipline. |
| Authority non-escalation / permission receipt tests | System boundaries, security kernel, runtime adapters, labor OS | Turns authority vocabulary into reject/accept behavior. |
| Security kernel harness | Security kernel, system boundaries, runtime adapters, context transactions | Makes handle mediation, approval artifacts, scoped action, SCIF lifecycle, sanitization, residual leak-risk notes, revocation paths, and prompt-injection non-disclosure boundaries executable. |
| Stable capability fields harness | Stable capability fields, replacement, recursive self-improvement, governance rights | Makes qualification predicates, evidence refs, authority ceilings, route permission effects, evaluator independence, rollback obligations, default-route blockers, and non-claim boundaries executable. |
| Capability replacement harness | Capability replacement, stable capability fields, recursive self-improvement, readiness gates | Makes field identity, qualification evidence, regression results, non-widening authority checks, evaluator separation, residual escrow, rollback receipts, approvals, monitor state, promotion blockers, and non-claim boundaries executable. |
| Self-improvement boundary harness | Recursive self-improvement, constitutional alignment, capability replacement, stable capability fields, readiness gates | Makes protected invariants, evaluator separation, cheaper-intervention ordering, authority non-widening, governance review, monitor windows, rollback paths, and no-promotion language executable. |
| Plan graph and execution-contract tests | Intent contracts, command contracts, planning, PlanForge, cognitive compilation | Makes the planning/execution boundary executable. |
| Runtime adapter permission and approval tests | Runtime adapters, security kernel, Labor OS, artifact graphs | Turns effect-boundary vocabulary into permission, approval, receipt, rollback, and residual gate behavior. |
| Context admission vs adequacy tests | Virtual Context ABI, semantic pages, context transactions, verification bandwidth | Tests a core memory/reasoning interface. |
| Readiness gate and residual escrow tests | Routing, readiness gates, MoECOT, prototype roadmap, recursive self-improvement | Converts promotion-blocking language into synthetic cross-record gate behavior. |
| Benchmark ratchet anti-Goodhart tests | Benchmark ratchets, policy optimization, artifact steward agents | Keeps benchmark, policy-update, and steward-release handoffs from treating proxy scores as authority. |
| Generation mode baseline accounting tests | Fast generation architectures, efficient ASI hypothesis, resource economics | Keeps useful-solution-per-second, quality, residual, baseline, and fallback accounting together before any fast-generation claim can move. |
| Resource budget ledger tests | Resource economics, efficient ASI hypothesis, planning, runtime adapters, benchmark ratchets | Makes dispatch, escalation, protected overhead, displaced-cost residualization, review-capacity hoarding, evidence refs, and no-promotion boundaries executable before any resource-economics claim can move. |
| Capacity smoothing toy traces | Resource economics, efficient ASI hypothesis, planning, PlanForge | Makes bounded regeneration arithmetic, priority deferral, scope reduction, overload rejection, and no-promotion boundaries executable without claiming real load stability. |

The set is registered in `experiments/phase5_harness_registry.json`, documented in `docs/phase5_harness_registry.md`, and checked by `python3 scripts/validate_phase5_harness_registry.py`. The registry guard verifies command scripts, docs, fixture counts, result records, Appendix E rows, public status references, primary chapter mappings, non-claim boundaries, and `scripts/validate_book.py` wiring.

Each future harness should write public-safe results under a tracked result or report location only after it actually runs. If a test is negative, failed, or inconclusive, keep that result visible. The current harnesses remain synthetic record gates, synthetic cross-record gates, deterministic accounting gates, claim-ledger revision fixtures, proof-carrying claim fixtures, tribunal-review fixtures, value-conflict fixtures, constitutional-predicate fixtures, governance-right fixtures, agency-right fixtures, stable-capability-field fixtures, replacement-transaction fixtures, self-improvement transition fixtures, and toy capacity traces only; they do not prove source interpretation, open-domain claim extraction, theorem validity, semantic equivalence, citation accuracy, verifier quality, belief-engine correctness, reviewer independence, adversarial-review quality, verdict correctness, moral correctness, value-conflict classification quality, human-review quality, institutional governance, legal rights, runtime right enforcement, routing accuracy, deployed authorization, planner quality, adapter runtime safety, memory correctness, benchmark quality, generation speed, model quality, budget scheduling, real load stability, economic outcomes, policy-training quality, steward-agent behavior, runtime safety, route validity, capability identity, evaluator integrity, authority enforcement, replacement safety, deployed self-improvement behavior, recursive self-improvement safety, rollback execution, regression quality, or support-state promotion.

### 4. Proof Adequacy Follow-Through

The Lean workspace is valuable because it makes local invariants executable and checkable. The risk is that a finite-record predicate can look stronger than it is.

The first semantic proof adequacy review is now recorded in
`docs/proof_adequacy_review.md`, and the proof-depth classifier records the
projection-vs-derived split in `docs/proof_depth_classification.md`. The next
proof work should follow those classifications rather than reclassify from
scratch:

- Adequate finite-record invariant for the chapter's current claim boundary.
- Useful but too narrow to affect support state.
- Needs richer state-machine semantics.
- Needs executable test or schema before Lean is meaningful.
- Should stay as research agenda rather than Lean.

`proofs/proof_triage.json` still records routing into Lean, not semantic
adequacy of the resulting formalization. Future proof work should strengthen
one finite-record cluster at a time, update the public adequacy boundary, and
record a no-promotion decision unless the stronger predicate actually supports
a narrowed claim.

### 5. External Literature Deepening

The v1.0 external-SOTA placement gate is closed for the current chapter set:
44 chapters have in-prose external positioning and 10 have explicit exceptions.
The next work is deeper synthesis and exception replacement where the book
relies on outside comparison, not another broad scaffold pass.

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

1. Keep the v1.0 release-gate audit, progress ledger, validators, render, Lean
   build, and browser checks green while the final tag/release facts remain
   pending.
2. Pursue the next prototype, empirical, replayed, or imported-trace evidence slice
   that can strengthen a narrow claim without touching chapter core claims by
   implication.
3. Continue reader artifact review only where the artifact will receive an
   exact release record: EPUB e-reader inspection, DOCX application review, PDF
   page-by-page layout review, and audio script review remain separate lanes.
4. Use the proof adequacy and proof-depth reports to pick targeted Lean
   upgrades, especially where richer state-machine or review semantics would
   reduce residual risk.
5. Deepen external literature synthesis or replace recorded exceptions only
   when a chapter claim, external baseline, or release classification depends
   on it.
6. Continue manual public-site quality work through ledgered keyboard,
   screen-reader, contrast, and e-reader/readability passes.
7. Defer audiobook production and standalone preprints until the reviewed reader
   release and final v1.0 release record exist.

## Current Blocking Conditions

The project is not blocked from further writing or improvement. It is blocked from calling itself a final v1.0 evidence release until these conditions are handled:

- The exact final v1.0 source commit is known, the full local gate passes on
  that commit, and the GitHub Pages run for that commit succeeds.
- A final release record names the commit, release classification, local
  validation commands, Pages run, DOI/Zenodo state, reader artifact state,
  residuals, and non-claims.
- `CITATION.cff` and `docs/release_reproducibility.md` move from candidate
  metadata to final metadata only after the tag, release record, and archive
  facts actually exist.
- Any claim moved above `argument` has an accepted evidence-transition record.
  All chapter core claims currently remain at `argument`.
- EPUB, DOCX, PDF, e-reader, audio, and audio-embedded EPUB remain unapproved
  unless their own exact artifact review and release records exist.
- Manual keyboard-only review, screen-reader review, measured contrast audit,
  and e-reader/readability review remain quality residuals unless recorded in
  the relevant public ledger.

## Bottom Line

The repo is no longer in scaffold-building mode. It is in release-gate,
evidence-depth, and reader-quality mode.

The highest-value work is to keep the explicit v1.0 gates green, pursue the next
stronger prototype or empirical evidence slice, preserve final-release metadata
until facts exist, and review only the reader/site artifacts that will be
recorded exactly. That work will improve the book more than adding raw volume.
