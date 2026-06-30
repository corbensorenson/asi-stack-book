# Curated Reader Graduation Review

Last updated: 2026-06-30

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
- Generated-reader chapter-text review: complete for all 54 current chapters
- Active reader-overlay operations: 33
- Companion-note candidates: 3
- Curated-manuscript candidates: 23
- Curated chapter records: 30 drafting records for
  `asi-is-a-stack-not-a-model`,
  `the-efficient-asi-hypothesis`,
  `system-boundaries-and-authority`,
  `failure-modes-of-ungoverned-intelligence`,
  `evidence-states-and-claim-discipline`,
  `human-intent-as-a-formal-input`,
  `security-kernel-and-digital-scifs`,
  `stable-capability-fields`,
  `capability-replacement-and-rollback`,
  `readiness-gates-residual-escrow-and-quarantine`,
  `context-transactions-snapshots-mounts-and-taint`,
  `verification-bandwidth-and-context-adequacy`,
  `claim-ledgers-and-belief-revision`,
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
  `mathematical-and-search-substrates`,
  `coil-attention-cyclic-memory-and-recurrence-contracts`,
  `recursive-self-improvement-boundaries`,
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
System Boundaries, Failure Modes, Evidence States, Human Intent, Security
Kernel, Stable Capability Fields, Capability Replacement and Rollback,
Readiness Gates, Context Transactions, Verification Bandwidth, Claim Ledgers,
Labor OS, Artifact Graphs, Runtime Adapters, Procedural Memory,
Benchmark Ratchets, Policy Optimization, Integrated Reference Architecture, Project Theseus,
Prototype Roadmap, Living Book Methodology, Open Research Agenda,
Mathematical and Search Substrates, Coil Attention and Cyclic Memory,
Recursive Self-Improvement,
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

After the consolidation decision review, curated-reader work should start with
pilot chapters outside the pending Part I merge cluster. The four source
chapters named in the alignment/governance consolidation pilot should not
receive broad reader-only graduation until their merge is executed or
permanently rejected; otherwise the human manuscript would preserve the same
duplicate skeletons the consolidation pilot is trying to remove.

## Candidate Chapters

| Chapter | Current disposition | Graduation decision |
|---|---|---|
| `asi-is-a-stack-not-a-model` | pilot curated reader chapter outside the pending consolidation cluster | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_asi_stack_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, and no reader artifact is approved. |
| `the-efficient-asi-hypothesis` | pilot curated reader chapter outside the pending consolidation cluster | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_efficient_asi_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, and no reader artifact is approved. |
| `system-boundaries-and-authority` | foundational protected standalone chapter outside the pending consolidation cluster; active overlay already existed for permission-class prose | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_system_boundaries_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, no reader artifact is approved, and deployed authorization enforcement is not claimed. |
| `failure-modes-of-ungoverned-intelligence` | foundational protected standalone chapter outside the pending consolidation cluster; owns the failure-obligation map that follows authority boundaries | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_failure_modes_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, no reader artifact is approved, and no scenario-coverage, deployed-detection, or deployed-prevention claim is implied. |
| `evidence-states-and-claim-discipline` | protected standalone evidence-discipline chapter and active evidence-cycle lane outside the pending consolidation cluster | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_evidence_states_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, no reader artifact is approved, and no claim-support movement is implied. |
| `human-intent-as-a-formal-input` | local prose improvement allowed by the consolidation decision review; outside the pending four-chapter merge cluster but adjacent to a possible future Constitutional Alignment destination | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_human_intent_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, no reader artifact is approved, and the handoff must be revisited if the Part I consolidation changes the Constitutional Alignment destination. |
| `security-kernel-and-digital-scifs` | protected standalone security-boundary chapter outside the pending consolidation cluster; owns least-exposure, handle-lease, Digital SCIF, and authority-receipt reader vocabulary | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_security_kernel_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, no reader artifact is approved, and no deployed security, sandbox-isolation, side-channel-resistance, prompt-injection-containment, OWASP-conformance, or NIST-zero-trust-implementation claim is implied. |
| `stable-capability-fields` | protected standalone capability-identity chapter outside the pending consolidation cluster; owns field/implementation separation, qualification leases, route-validation boundaries, authority ceilings, and rollback obligations | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_stable_capability_fields_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, no reader artifact is approved, and no deployed route validation, authority enforcement, replacement safety, rollback execution, SLSA workflow, SemVer checker, object-capability implementation, or MoECOT runtime reproduction claim is implied. |
| `capability-replacement-and-rollback` | protected standalone replacement-control chapter outside the pending consolidation cluster; owns candidate/accepted replacement separation, regression floors, residual escrow, monitor windows, rollback receipts, and evaluator independence | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_capability_replacement_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, no reader artifact is approved, and no deployed replacement behavior, real regression-suite quality, monitor-window success, rollback execution, evaluator-integrity enforcement, authority enforcement, MoECOT runtime reproduction, or implemented-corrigibility claim is implied. |
| `readiness-gates-residual-escrow-and-quarantine` | protected standalone readiness-control chapter outside the pending consolidation cluster; owns scoped permission, residual escrow, productive quarantine, stale-gate prevention, inherited residuals, and lifecycle control | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_readiness_gates_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, no reader artifact is approved, and no deployed readiness engine, residual-ledger storage, benchmark quality, live quarantine routing, gate-expiry enforcement, live rerouting, current Theseus runtime behavior, or MoECOT replay claim is implied. |
| `context-transactions-snapshots-mounts-and-taint` | protected standalone transaction-memory chapter outside the pending static context ABI merge package; owns memory-as-accountable-state, mounted snapshots, branches, taint/deletion closure, typed faults, and downstream artifact inheritance | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_context_transactions_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, no reader artifact is approved, and no memory-store behavior, read-your-writes result, branch-isolation result, mount-visibility result, replay correctness, poisoning resistance, side-channel defense, VCM conformance, or Digital SCIF implementation claim is implied. |
| `verification-bandwidth-and-context-adequacy` | protected standalone context-adequacy chapter outside the pending static context ABI merge package; owns generation-versus-verification, target-claim scoped adequacy, semantic-unit comparison, escalation, and mode-confusion boundaries | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_verification_bandwidth_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, no reader artifact is approved, and no contradiction-rate benchmark, distractor-resistance result, summary-fidelity result, adequacy-classifier correctness, deployed VCM behavior, deployed escalation, or support-state movement claim is implied. |
| `claim-ledgers-and-belief-revision` | protected standalone belief-revision substrate outside the pending verification/adversarial-review merge package; owns claim identity, support states, contradiction links, revision history, downgrade behavior, and confidence-laundering boundaries | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_claim_ledgers_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, no reader artifact is approved, and no claim-extraction, contradiction-detection, semantic-equivalence, citation-correctness, belief-engine, deployed-epistemic-correctness, or support-state movement claim is implied. |
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
| `mathematical-and-search-substrates` | protected standalone substrate-adoption chapter outside pending consolidation clusters; owns optional-substrate discipline, adoption records, axis ledgers, consumer gates, theorem-spillover controls, and retirement/falsification boundaries | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_mathematical_search_substrates_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, no reader artifact is approved, and no temporal-coil A/B run, representation-efficiency benchmark, CoilMoECOT route benchmark, Mamba comparison, Circle substrate sidecar, Theseus transfer consumer, useful-substrate result, model-quality result, or support-state movement claim is implied. |
| `coil-attention-cyclic-memory-and-recurrence-contracts` | protected standalone cyclic-memory contract chapter outside pending consolidation clusters; owns structural memory versus useful memory, residue/winding visibility, freshness policy, sparse coverage, recurrence exits, fallback, baseline obligations, and retrieval-quality non-claims | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_coil_attention_memory_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, no reader artifact is approved, and no KV-cache freshness checker, sparse-coverage harness, recurrence benchmark, learned-memory workload, Circle contract pack, Theseus transfer consumer, external benchmark reproduction, retrieval-quality result, reasoning-quality result, speed result, memory-savings result, long-context result, or support-state movement claim is implied. |
| `recursive-self-improvement-boundaries` | pilot curated reader chapter outside the pending consolidation cluster | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_recursive_self_improvement_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, and no reader artifact is approved. |
| `artifact-steward-agents-and-living-project-governance` | `curated_manuscript_candidate`, `companion_note_candidate`, active overlays | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_artifact_steward_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, and no reader artifact is approved. |
| `circle-calculus-and-proof-carrying-ai-contracts` | `companion_note_candidate`, active overlays | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_circle_contracts_prose_pass.md`; companion/glossary treatment remains active, reconciliation remains incomplete, release blockers remain active, and no reader artifact is approved. |
| `executable-specifications-and-lean-proof-envelope` | `companion_note_candidate`, active overlay | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_executable_specs_prose_pass.md`; companion/glossary treatment remains active, reconciliation remains incomplete, release blockers remain active, and no reader artifact is approved. |

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

- This review creates thirty drafting-only curated reader chapter files for
  future prose editing; it does not approve any file for release.
- This review does not create or approve EPUB, PDF, DOCX, HTML, audio, or
  audio-embedded EPUB artifacts.
- This review does not remove release blockers from any chapter.
- This review does not promote any support state.
- This review does not make the reader manuscript an equal source of truth
  beside the live AI/research book.
