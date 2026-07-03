# Curated Reader Graduation Review

Last updated: 2026-07-03

This note records the v1.0 decision about whether the normal human-reader book
should graduate from generated reader source plus semantic overlays into a
tracked curated reader manuscript. It is not a reader release record, not an
ebook/document/PDF/audio artifact record, and not a support-state promotion.

## Inputs

- Reader manuscript manifest: `editions/reader_manuscript/v1_0/manifest.json`
- Curated source contract: `editions/reader_manuscript/v1_0/curation_contract.json`
- Contract summary: `docs/curated_reader_source_contract.md`
- Reconciliation template: `editions/reader_manuscript/v1_0/reconciliation_report.md`
- Chapter review matrix: `editions/reader_manuscript/v1_0/chapter_review_matrix.json`
- Public review summary: `docs/reader_chapter_review_matrix.md`
- Reader overlay manifest: `editions/reader_overlays/v1_0/manifest.json`
- Generated reader source: `build/reader_edition/`

## Current State

- Curated reader manuscript status: `drafting`
- Generated-reader chapter-text review: complete for all 44 current chapters
- Active reader-overlay operations: 31
- Companion-note candidates: 3
- Curated-manuscript candidates: 44
- Curated chapter records: 32 drafting records and 12 reconciled records; see `editions/reader_manuscript/v1_0/manifest.json` and `editions/reader_manuscript/v1_0/reconciliation_report.md` for the current chapter-level list. Earlier curated records include
  `asi-is-a-stack-not-a-model`,
  `the-efficient-asi-hypothesis`,
  `system-boundaries-and-authority`,
  `failure-modes-of-ungoverned-intelligence`,
  `evidence-states-and-claim-discipline`,
  `human-intent-as-a-formal-input`,
  `constitutional-alignment-substrate`,
  `moral-uncertainty-and-value-conflict`,
  `security-kernel-and-digital-scifs`,
  `stable-capability-fields`,
  `capability-replacement-and-rollback`,
  `routing-heads-and-specialist-cores`,
  `moecot-runtime-and-multi-core-orchestration`,
  `readiness-gates-residual-escrow-and-quarantine`,
  `cognitive-compilation-and-semantic-ir`,
  `context-transactions-snapshots-mounts-and-taint`,
  `verification-bandwidth-and-context-adequacy`,
  `claim-ledgers-and-belief-revision`,
  `spinoza-verification-and-proof-carrying-claims`,
  `unified-adaptive-tribunal-and-adversarial-review`,
  `labor-os-and-typed-jobs`,
  `artifact-graphs-audit-logs-and-replay`,
  `runtime-adapters-tool-permissions-and-human-approval`,
  `procedural-memory-and-cognitive-loop-closure`,
  `benchmark-ratchets-and-anti-goodhart-evidence`,
  `policy-optimization-and-learning-from-feedback`,
  `integrated-reference-architecture`,
  `project-theseus-as-report-first-implementation-reference`,
  `prototype-roadmap`,
  `living-book-methodology`,
  `open-research-agenda-and-bibliography-plan`,
  `personal-compute-hives-and-federated-edge-intelligence`,
  `resource-economics-and-token-budgets`,
  `fast-generation-architectures`,
  `mathematical-and-search-substrates`,
  `coil-attention-cyclic-memory-and-recurrence-contracts`,
  `coilra-multicoil-rope-and-cyclic-mixers`,
  `recursive-self-improvement-boundaries`,
  `intent-to-execution-contracts`,
  `planning-as-a-control-layer`,
  `virtual-context-abi`,
  `circle-calculus-and-proof-carrying-ai-contracts`,
  `executable-specifications-and-lean-proof-envelope`, and
  `artifact-steward-agents-and-living-project-governance`
- Release blockers: reader release records and format artifact review remain
  open for every chapter
- Consolidation gate: `docs/chapter_consolidation_decision_review.md` defers
  the Part I alignment/governance manifest merge for this v1.x cycle, so
  reader curation may proceed outside the pending merge cluster without
  locking in avoidable duplicate skeletons.

## Decision

Graduate drafting-only curated reader sources for the opener, Efficient ASI,
System Boundaries, Failure Modes, Evidence States, Human Intent,
Constitutional Alignment, Moral Uncertainty, Security Kernel, Stable Capability Fields,
Capability Replacement and Rollback, Routing Heads, MoECOT Runtime, Readiness Gates, Cognitive Compilation,
Context Transactions, Verification Bandwidth, Claim Ledgers, Spinoza Verification, Unified Adaptive Tribunal, Labor OS,
Artifact Graphs, Runtime Adapters, Procedural Memory, Benchmark Ratchets,
Policy Optimization, Integrated Reference Architecture, Project Theseus,
Prototype Roadmap, Living Book Methodology, Open Research Agenda, Personal
Compute Hives, Resource Economics, Mathematical and Search Substrates,
Coil Attention and Cyclic Memory,
CoilRA and Cyclic Mixers, Recursive Self-Improvement, Planning as a Control
Layer: DAGs and Intelligence Arbitrage, The Virtual Context ABI,
`circle-calculus-and-proof-carrying-ai-contracts`,
`executable-specifications-and-lean-proof-envelope`, and
`artifact-steward-agents-and-living-project-governance`; do not treat any file
as a reader release artifact.

Generated reader source plus tracked semantic overlays is still the right
release baseline for v1.0 because most current reader problems are localized:
table-to-prose transformations, proof-vocabulary density, companion-note
routing, and artifact-layout review. Those are better handled by overlays,
companion notes, and release-review records than by creating a full parallel
manuscript before the human edition has release artifacts.

The curated manuscript path remains necessary for the future. It should be used
when reader editing becomes paragraph- and chapter-structural rather than
section-local: reordering examples, rewriting openings and closings across
multiple sections, compressing long implementation ladders, adding sustained
reader examples, or producing a final bedtime-readable major-version prose
source.

After the release-stability review, curated-reader work may enter a pending
consolidation cluster only when the prose-pass record cites
`docs/chapter_consolidation_release_stability_review.md` and keeps the merge
or fold caveat active. The deferred-package passes now improve current reader
manuscript prose without executing, rejecting, or authorizing their future
merge or fold packages.

## Candidate Chapters

| Chapter | Current disposition | Graduation decision |
|---|---|---|
| `asi-is-a-stack-not-a-model` | `curated_manuscript_candidate`; pilot curated reader chapter outside the pending consolidation cluster | Curated reader reconciliation completed and recorded in `docs/curated_reader_asi_stack_prose_pass.md`. Release blockers remain active, no reader artifact is approved, and this does not make the full curated manuscript release-candidate or released. |
| `the-efficient-asi-hypothesis` | `curated_manuscript_candidate`; pilot curated reader chapter outside the pending consolidation cluster | Curated reader reconciliation completed and recorded in `docs/curated_reader_efficient_asi_prose_pass.md`. Release blockers remain active, no reader artifact is approved, and the Resource Economics selector slice is not treated as proof or promotion of the Efficient ASI core claim. |
| `system-boundaries-and-authority` | foundational protected standalone chapter outside the pending consolidation cluster; active overlay already existed for permission-class prose | Curated reader reconciliation completed and recorded in `docs/curated_reader_system_boundaries_prose_pass.md`. Release blockers remain active, no reader artifact is approved, and deployed authorization enforcement is not claimed. |
| `failure-modes-of-ungoverned-intelligence` | foundational protected standalone chapter outside the pending consolidation cluster; owns the failure-obligation map that follows authority boundaries | Curated reader reconciliation completed and recorded in `docs/curated_reader_failure_modes_prose_pass.md`. Release blockers remain active, no reader artifact is approved, and no scenario-coverage, deployed-detection, or deployed-prevention claim is implied. |
| `evidence-states-and-claim-discipline` | `curated_manuscript_candidate`; protected standalone evidence-discipline chapter and active evidence-cycle lane outside the pending consolidation cluster | Curated reader reconciliation completed and recorded in `docs/curated_reader_evidence_states_prose_pass.md`. Release blockers remain active, no reader artifact is approved, and no claim-support movement is implied. |
| `human-intent-as-a-formal-input` | `curated_manuscript_candidate`; remains the standalone intent-intake chapter before Constitutional Alignment | Curated reader reconciliation completed and recorded in `docs/curated_reader_human_intent_prose_pass.md`. Release blockers remain active, no reader artifact is approved, and no parser, authority-extractor, approval-service, runtime-dispatch, prompt-injection-containment, or end-to-end execution-handoff claim is implied. |
| `constitutional-alignment-substrate` | `curated_manuscript_candidate`; executed alignment/corrigibility merge now routes reader work through this destination chapter; archived Agency/Dignity reader draft remains historical only | Curated reader reconciliation completed and recorded in `docs/curated_reader_constitutional_alignment_prose_pass.md`. Release blockers remain active, no reader artifact is approved, and no deployed constitutional alignment, agency preservation, dignity preservation, manipulation resistance, runtime corrigibility, intervention tolerance, shutdown compliance, moral-correctness proof, Constitutional AI reproduction, public-input governance legitimacy, runtime policy engine, or reader-release approval is implied. |
| `moral-uncertainty-and-value-conflict` | `curated_manuscript_candidate`; executed contestable-governance merge now routes reader work through this destination chapter; archived Governance Rights reader draft remains historical only | Curated reader reconciliation completed and recorded in `docs/curated_reader_moral_uncertainty_prose_pass.md`. Release blockers remain active, no reader artifact is approved, and no moral correctness, solved moral uncertainty, classification quality, reviewer independence, tribunal quality, runtime policy behavior, deployed conflict handling, legal rights, institutional legitimacy, real audit availability, real export usability, fork safety, runtime enforcement, redaction quality, external experiment reproduction, or reader-release approval is implied. |
| `security-kernel-and-digital-scifs` | protected standalone security-boundary chapter outside the pending consolidation cluster; owns least-exposure, handle-lease, Digital SCIF, and authority-receipt reader vocabulary | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_security_kernel_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, no reader artifact is approved, and no deployed security, sandbox-isolation, side-channel-resistance, prompt-injection-containment, OWASP-conformance, or NIST-zero-trust-implementation claim is implied. |
| `stable-capability-fields` | protected standalone capability-identity chapter outside the pending consolidation cluster; owns field/implementation separation, qualification leases, route-validation boundaries, authority ceilings, and rollback obligations | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_stable_capability_fields_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, no reader artifact is approved, and no deployed route validation, authority enforcement, replacement safety, rollback execution, SLSA workflow, SemVer checker, object-capability implementation, or MoECOT runtime reproduction claim is implied. |
| `capability-replacement-and-rollback` | protected standalone replacement-control chapter outside the pending consolidation cluster; owns candidate/accepted replacement separation, regression floors, residual escrow, monitor windows, rollback receipts, and evaluator independence | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_capability_replacement_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, no reader artifact is approved, and no deployed replacement behavior, real regression-suite quality, monitor-window success, rollback execution, evaluator-integrity enforcement, authority enforcement, MoECOT runtime reproduction, or implemented-corrigibility claim is implied. |
| `routing-heads-and-specialist-cores` | `curated_manuscript_candidate`; executed MoECOT runtime fold now routes reader work through this destination chapter; archived standalone MoECOT reader draft remains historical only | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_routing_heads_prose_pass.md`, with MoECOT runtime prose lineage retained in `docs/curated_reader_moecot_runtime_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, no reader artifact is approved, and no routing accuracy, learned-router quality, specialist adequacy, deployed authority enforcement, route-quality dominance, cost savings, MoECOT runtime behavior, MoECOT replay, current Theseus runtime behavior, support-state movement, or reader-release approval is implied. |
| `moecot-runtime-and-multi-core-orchestration` | historical curated-reader draft only; folded into `routing-heads-and-specialist-cores` and no longer a current manifest chapter | First drafting-only curated reader prose pass remains archived lineage in `docs/curated_reader_moecot_runtime_prose_pass.md`. It is not a standalone reader-release chapter, and no MoECOT runtime execution, benchmark reproduction, replay correctness, current report-bundle verification, worker/core balance trace, isolation result, specialist adequacy, routing quality, model quality, current Theseus runtime behavior, support-state movement, or manifest fold decision is implied. |
| `readiness-gates-residual-escrow-and-quarantine` | protected standalone readiness-control chapter outside the pending consolidation cluster; owns scoped permission, residual escrow, productive quarantine, stale-gate prevention, inherited residuals, and lifecycle control | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_readiness_gates_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, no reader artifact is approved, and no deployed readiness engine, residual-ledger storage, benchmark quality, live quarantine routing, gate-expiry enforcement, live rerouting, current Theseus runtime behavior, or MoECOT replay claim is implied. |
| `cognitive-compilation-and-semantic-ir` | protected standalone semantic-IR and lowering chapter outside pending consolidation clusters; owns obligation addressability, semantic atoms, lowering receipts, validator failure routing, localized repair, and compiler non-claims | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_cognitive_compilation_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, no reader artifact is approved, and no source-plan parser, target-lowering correctness, compiler correctness, localized-repair performance, artifact-validator adequacy, quality improvement, cost improvement, deployed compiler behavior, or support-state movement claim is implied. |
| `context-transactions-snapshots-mounts-and-taint` | protected standalone transaction-memory chapter outside the pending static context ABI merge package; owns memory-as-accountable-state, mounted snapshots, branches, taint/deletion closure, typed faults, and downstream artifact inheritance | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_context_transactions_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, no reader artifact is approved, and no memory-store behavior, read-your-writes result, branch-isolation result, mount-visibility result, replay correctness, poisoning resistance, side-channel defense, VCM conformance, or Digital SCIF implementation claim is implied. |
| `verification-bandwidth-and-context-adequacy` | protected standalone context-adequacy chapter outside the pending static context ABI merge package; owns generation-versus-verification, target-claim scoped adequacy, semantic-unit comparison, escalation, and mode-confusion boundaries | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_verification_bandwidth_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, no reader artifact is approved, and no contradiction-rate benchmark, distractor-resistance result, summary-fidelity result, adequacy-classifier correctness, deployed VCM behavior, deployed escalation, or support-state movement claim is implied. |
| `claim-ledgers-and-belief-revision` | protected standalone belief-revision substrate outside the pending verification/adversarial-review merge package; owns claim identity, support states, contradiction links, revision history, downgrade behavior, and confidence-laundering boundaries | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_claim_ledgers_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, no reader artifact is approved, and no claim-extraction, contradiction-detection, semantic-equivalence, citation-correctness, belief-engine, deployed-epistemic-correctness, or support-state movement claim is implied. |
| `spinoza-verification-and-proof-carrying-claims` | `curated_manuscript_candidate`; executed verification/adversarial-review merge now routes reader work through this destination chapter; archived UAT reader draft remains historical only | Drafting-only curated reader prose now combines `docs/curated_reader_spinoza_prose_pass.md` with folded tribunal/adversarial-review material from `docs/curated_reader_uat_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, no reader artifact is approved, and no theorem validity, verifier quality, citation accuracy, semantic equivalence, open-domain autoformalization, proof generation, source interpretation, reviewer independence, adversarial-probe quality, consensus quality, verdict correctness, human-adjudication quality, tribunal quality, deployed contestability, whole-system epistemic correctness, support-state movement, or reader-release approval is implied. |
| `labor-os-and-typed-jobs` | protected standalone execution-boundary chapter outside pending consolidation clusters; owns typed jobs, contract locks, permission checks, approval gates, runtime-adapter boundaries, completion receipts, delivery-versus-evidence readiness, residuals, quarantine, and artifact handoff | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_labor_os_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, no reader artifact is approved, and no deployed Labor OS, scheduler, permission service, approval service, adapter runner, replay system, benchmark, security result, AutoGen reproduction, SWE-bench reproduction, Talos runtime, or MoECOT runtime reproduction claim is implied. |
| `artifact-graphs-audit-logs-and-replay` | protected standalone execution-continuity chapter outside pending consolidation clusters; owns artifact identity, provenance, audit events, replay grades, claim/test links, evidence gates, residuals, and allowed reuse | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_artifact_graphs_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, no reader artifact is approved, and no artifact-graph service, replay engine, audit reconstruction, produced-artifact completeness, provenance-completeness service, benchmark, security result, proof-carrying-code implementation, SWE-bench reproduction, AutoGen reproduction, or MoECOT runtime reproduction claim is implied. |
| `runtime-adapters-tool-permissions-and-human-approval` | protected standalone execution-effect boundary chapter outside pending consolidation clusters; owns capability leases, typed permissions, sandbox modes, authority handles, scoped approval, effect receipts, rollback or residual records, incident paths, and evidence-state boundaries | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_runtime_adapters_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, no reader artifact is approved, and no deployed runtime adapter service, sandbox isolation, approval service, secret-handle safety, live effect receipt validation, rollback execution, incident response, runtime security, benchmark performance, Talos runtime, MoECOT runtime reproduction, ReAct reproduction, Simplex-level assurance, Copilot-style runtime monitoring, proof-carrying-code enforcement, or deployed approval enforcement claim is implied. |
| `procedural-memory-and-cognitive-loop-closure` | protected standalone procedural-reuse chapter outside pending consolidation clusters; owns comparable traces, failures and near misses, invariant abstraction, parameter discovery, procedure qualification, regression checks, quarantine/residual handling, monitoring, and retirement triggers | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_procedural_memory_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, no reader artifact is approved, and no loop detector, tool synthesis, parameter-discovery engine, deployed tool behavior, regression success, routing monitor, retirement automation, Talos loop-closure behavior, MoECOT runtime reproduction, Project Theseus replay, or autonomous self-improvement claim is implied. |
| `benchmark-ratchets-and-anti-goodhart-evidence` | protected standalone evidence-governance chapter outside pending consolidation clusters; owns score-versus-evidence distinction, evidence-state classification, run records, residuals, regression floors, anti-Goodhart checks, contamination/transfer boundaries, and claim-specific promotion decisions | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_benchmark_ratchets_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, no reader artifact is approved, and no empirical benchmark success, hidden-holdout validity, benchmark transfer, contamination resistance, regression-suite quality, anti-Goodhart effectiveness, source-reported replay, current Theseus readiness, deployment readiness, model quality, or ASI-progress claim is implied. |
| `policy-optimization-and-learning-from-feedback` | protected standalone governed-learning chapter outside pending consolidation clusters; owns policy updates as behavior-change leases, target-policy identity, feedback admissibility, reward boundaries, drift bounds, holdouts, regressions, reward-hacking probes, authority conservation, rollback, and promotion gates | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_policy_optimization_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, no reader artifact is approved, and no PPO, DPO, GRPO, RLVR, router-policy RL, context-policy RL, reasoning-budget RL, reward-model validation, preference-data quality, optimizer convergence, benchmark improvement, policy safety, route quality, context-selection quality, rollback success, governed deployment, or reward-hacking-resistance claim is implied. |
| `integrated-reference-architecture` | protected standalone synthesis chapter outside pending consolidation clusters; owns the reference trace kernel, parent artifacts, authority deltas, evidence deltas, residual deltas, stop conditions, blocked-path visibility, and downstream trace rejection | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_integrated_reference_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, no reader artifact is approved, and no integrated runtime, end-to-end trace harness, artifact-continuity audit, authority stop-condition execution, deployed authority enforcement, replayed runtime trace, current Theseus dashboard or command result, operator-board execution, compiler proof, benchmark ledger replay, model-quality result, deployment-readiness, stack-safety, or public empirical-proof claim is implied. |
| `project-theseus-as-report-first-implementation-reference` | protected standalone implementation-reference chapter outside pending consolidation clusters; owns the report-first Theseus boundary, static import boundary, missing-artifact visibility, and no-promotion discipline | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_project_theseus_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, no reader artifact is approved, and no clean live Theseus replay, current dashboard state, reproduced benchmark, model-quality result, deployment readiness, training authorization, self-evolution safety, public-compute readiness, or support-state movement claim is implied. |
| `prototype-roadmap` | protected standalone build-order chapter outside pending consolidation clusters; owns phase sequencing, dependency gates, phase debt, roadmap-as-non-evidence boundaries, and delayed self-improvement | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_prototype_roadmap_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, no reader artifact is approved, and no phase acceptance, dependency-gate audit, phase execution, benchmark result, model-quality result, deployment readiness, self-improvement readiness, roadmap-controller deployment, or support-state movement claim is implied. |
| `living-book-methodology` | protected standalone living-method chapter outside pending consolidation clusters; owns the book-as-governed-research-instrument throughline, stable IDs, change packets, tri-audience derivation, publication-laundering controls, and non-claim boundaries | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_living_book_methodology_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, no reader artifact is approved, and no manuscript-quality, source-interpretation-quality, rendered-site-availability, external-review, reader-release, audio-production, ASI-capability, or support-state movement claim is implied. |
| `open-research-agenda-and-bibliography-plan` | protected standalone final research-agenda chapter outside pending consolidation clusters; owns source-intake, bibliography-control, external-literature, backlog, new-paper triage, proof/test lane, and no-promotion boundaries | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_open_research_agenda_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, no reader artifact is approved, and no citation-normalization, external-literature-completeness, benchmark-reproduction, artifact-reproduction, live-new-paper-triage, public-release-permission, external-review, or support-state movement claim is implied. |
| `personal-compute-hives-and-federated-edge-intelligence` | protected standalone owned-compute chapter outside pending consolidation clusters; owns reachability-versus-authority, policy-first placement, owned/rented device roles, family/project mediation, Hive-to-Hive protocol, and hive-memory boundaries | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_personal_compute_hives_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, no reader artifact is approved, and no live device registry, policy-first scheduler, portal approval service, family-governance policy engine, rented-node sandbox, cross-router connectivity result, energy-aware scheduling result, contribution ledger, federation run, or support-state movement claim is implied. |
| `resource-economics-and-token-budgets` | protected standalone resource-accounting chapter outside pending consolidation clusters; owns budget-as-governance, verification tax, protected overhead, displaced costs, serving pressure, cost-quality residuals, and resource-ledger non-claims | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_resource_economics_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, no reader artifact is approved, and no TokenMana simulation, PlanForge scheduler benchmark, welfare/load study, serving-memory audit, KV-cache reproduction, cost-quality experiment, scarce-resource scheduler trace, economic outcome, or support-state movement claim is implied. |
| `fast-generation-architectures` | protected standalone generation-control chapter outside pending consolidation clusters; owns proposed-versus-accepted output, verifier and fallback accounting, generation-mode records, risk-tiered mode selection, memory-pressure boundaries, and no-latency-only promotion | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_fast_generation_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, no reader artifact is approved, and no local fast decoder, mode selector, useful-solution-per-second result, accepted-token measurement, speculative decoding reproduction, MTP reproduction, Medusa reproduction, EAGLE reproduction, lookahead reproduction, LayerSkip reproduction, vLLM/PagedAttention deployment, Mamba comparison, LLaDA run, diffusion benchmark, KV-cache audit, serving throughput result, quality improvement, memory savings, route promotion, or support-state movement claim is implied. |
| `mathematical-and-search-substrates` | protected standalone substrate-adoption chapter outside pending consolidation clusters; owns optional-substrate discipline, adoption records, axis ledgers, consumer gates, theorem-spillover controls, and retirement/falsification boundaries | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_mathematical_search_substrates_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, no reader artifact is approved, and no temporal-coil A/B run, representation-efficiency benchmark, CoilMoECOT route benchmark, Mamba comparison, Circle substrate sidecar, Theseus transfer consumer, useful-substrate result, model-quality result, or support-state movement claim is implied. |
| `coil-attention-cyclic-memory-and-recurrence-contracts` | protected standalone cyclic-memory contract chapter outside pending consolidation clusters; owns structural memory versus useful memory, residue/winding visibility, freshness policy, sparse coverage, recurrence exits, fallback, baseline obligations, and retrieval-quality non-claims | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_coil_attention_memory_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, no reader artifact is approved, and no KV-cache freshness checker, sparse-coverage harness, recurrence benchmark, learned-memory workload, Circle contract pack, Theseus transfer consumer, external benchmark reproduction, retrieval-quality result, reasoning-quality result, speed result, memory-savings result, long-context result, or support-state movement claim is implied. |
| `coilra-multicoil-rope-and-cyclic-mixers` | protected standalone cyclic-substrate evaluation chapter outside pending consolidation clusters; owns optional cyclic-substrate adoption, structural receipts, alias/load diagnostics, parameter and hardware ledgers, baseline symmetry, negative controls, tradeoff packets, and canary-route non-claims | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_coilra_cyclic_mixers_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, no reader artifact is approved, and no RoPE certifier run, sidecar regeneration, Circle contract pack, cyclic mixer benchmark, MLX model experiment, hardware-kernel benchmark, downstream quality evaluation, external Circle Lean build, Theseus transfer consumer, model-quality result, context-length result, runtime result, memory-savings result, training-stability result, hardware-efficiency result, deployment-readiness result, transfer result, or support-state movement claim is implied. |
| `recursive-self-improvement-boundaries` | `curated_manuscript_candidate`; pilot curated reader chapter outside the pending consolidation cluster | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_recursive_self_improvement_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, and no reader artifact is approved. |
| `intent-to-execution-contracts` | `curated_manuscript_candidate`; executed intent/contracts merge now routes reader work through this destination chapter; archived command-contract reader draft remains historical only | Drafting-only curated reader prose now combines `docs/curated_reader_intent_execution_prose_pass.md` with folded command-contract material from `docs/curated_reader_command_contracts_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, no reader artifact is approved, and no deployed parser, prompt safety, dispatch enforcement, approval enforcement, runtime execution, artifact acceptance, benchmark performance, or support-state movement is implied. |
| `planning-as-a-control-layer` | `curated_manuscript_candidate`; executed planning/DAG merge now routes reader work through this destination chapter; archived PlanForge reader draft remains historical only | Drafting-only curated reader prose now combines `docs/curated_reader_planning_control_prose_pass.md` with folded PlanForge material from `docs/curated_reader_planforge_dag_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, no reader artifact is approved, and no deployed planner behavior, decomposition accuracy, dependency soundness, scheduler correctness, route-selection quality, selected-tier adequacy, cost savings, cost-quality dominance, context-demand prediction, runtime replanning, dispatch safety, tool execution, PlanForge runtime behavior, MoECOT runtime behavior, benchmark performance, support-state movement, or reader-release approval is implied. |
| `virtual-context-abi` | `curated_manuscript_candidate`; executed static context ABI merge now routes reader work through this destination chapter; archived semantic-pages reader draft remains historical only | Drafting-only curated reader prose now combines `docs/curated_reader_virtual_context_abi_prose_pass.md` with folded semantic-pages material from `docs/curated_reader_semantic_pages_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, no reader artifact is approved, and no deployed VCM behavior, resolver correctness, context compiler correctness, certificate-truthfulness checking, snapshot-service behavior, adequacy-classifier quality, materialization correctness, summary fidelity, omission-completeness checking, contradiction-rate reduction, distractor resistance, leak prevention, Digital SCIF behavior, transactional memory-store behavior, VCM-Bench performance, model-facing context quality, MoECOT runtime behavior, source-interpretation adequacy, support-state movement, or reader-release approval is implied. |
| `artifact-steward-agents-and-living-project-governance` | `curated_manuscript_candidate`, `companion_note_candidate`, active overlays | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_artifact_steward_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, and no reader artifact is approved. |
| `circle-calculus-and-proof-carrying-ai-contracts` | `curated_manuscript_candidate`, `companion_note_candidate`, active overlays | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_circle_contracts_prose_pass.md`; companion/glossary treatment remains active, reconciliation remains incomplete, release blockers remain active, and no reader artifact is approved. |
| `executable-specifications-and-lean-proof-envelope` | `curated_manuscript_candidate`, `companion_note_candidate`, active overlay | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_executable_specs_prose_pass.md`; companion/glossary treatment remains active, reconciliation remains incomplete, release blockers remain active, and no reader artifact is approved. |

## Graduation Triggers

Graduate a chapter into curated reader source only when at least one of these is
true:

- a reader-only change touches multiple sections and would be brittle as overlay
  replacements;
- the chapter needs sustained example, analogy, pacing, or paragraph-order
  changes that should not alter the AI/research source;
- companion-note routing is not enough to make dense proof, schema, or
  governance material readable;
- release editing identifies human-prose improvements that are too broad for
  `editions/reader_overlays/` but do not belong in the canonical live chapter.

## Required Controls If Graduation Starts

- Add a curated chapter record under
  `editions/reader_manuscript/v1_0/manifest.json`.
- Store curated chapter files under
  `editions/reader_manuscript/v1_0/chapters/`.
- Follow `editions/reader_manuscript/v1_0/curation_contract.json` for required
  record fields, allowed edit scopes, blocked divergence, meaning-preservation
  checks, and pre-release blockers.
- Update `editions/reader_manuscript/v1_0/reconciliation_report.md`.
- Preserve generated-reader baseline refs, live-source refs, claim boundaries,
  source boundaries, proof/test status, implementation horizons, and release
  blockers.
- Run `python3 scripts/validate_reader_manuscript_manifest.py`.
- Run `python3 scripts/sync_reader_chapter_review_matrix.py --check`.

## Non-Claims

- This review records forty-four curated reader chapter files for future prose
  editing, with thirty-two drafting records and twelve reconciled prose records;
  it does not approve any file for release.
- This review does not create or approve EPUB, PDF, DOCX, HTML, audio, or
  audio-embedded EPUB artifacts.
- This review does not remove release blockers from any chapter.
- This review does not promote any support state.
- This review does not make the reader manuscript an equal source of truth
  beside the live AI/research book.
