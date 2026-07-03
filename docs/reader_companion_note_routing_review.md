# Reader Companion-Note Routing Review

Last updated: 2026-07-02

This review records the v1.0 routing decision for the twelve chapters flagged as
companion-note candidates in the reader chapter review matrix. It is not a
reader release record, not an ebook/document/PDF/audio artifact review, not a
curated reader-manuscript graduation, and not a support-state promotion.

## Inputs

- `editions/reader_manuscript/v1_0/chapter_review_matrix.json`
- `docs/reader_chapter_review_matrix.md`
- `docs/reader_continuity_review.md`
- `docs/reader_part_iii_iv_proof_bridge_full_review_pass.md`
- `docs/reader_part_iv_evidence_governance_full_review_pass.md`
- `docs/curated_reader_graduation_review.md`
- Generated reader chapters under `build/reader_edition/chapters/`

## Decision

Create a tracked companion-note routing manifest at
`editions/reader_manuscript/v1_0/companion_note_routing.json` and keep generated
reader source plus semantic overlays as the v1.0 reader path.

The twelve candidate chapters remain in the reader spine because their dense
terms carry meaning-critical boundaries. For v1.0, companion notes should help
e-reader and audio users with glossary, quick-reference, and spoken-treatment
support. They should not remove caveats that change claim meaning from ordinary
reader prose.

## Chapter Decisions

| Chapter | Reader treatment | Companion route | Release decision |
|---|---|---|---|
| `planning-as-a-control-layer` | Retain command-contract inheritance, plan-node lifecycle states, DAG/dependency boundaries, adequacy contracts, dispatch receipts, replanning deltas, residual registers, and planner-quality non-claims in the reader chapter. | Drafting companion note added at `editions/reader_manuscript/v1_0/companion_notes/planning-as-a-control-layer.md` for plan graphs, DAG scheduling, adequacy contracts, dispatch receipts, replanning history, residual registers, and audio treatment. | Drafting-only curated reader prose pass recorded in `docs/curated_reader_planning_control_prose_pass.md`; no release blocker cleared. |
| `routing-heads-and-specialist-cores` | Retain route-as-lease framing, specialist registry boundaries, routing decision records, selected authority subsets, rejected alternatives, readiness/fallback boundaries, residual ownership, MoECOT source-boundary caveats, and route-quality non-claims in the reader chapter. | Drafting companion note added at `editions/reader_manuscript/v1_0/companion_notes/routing-heads-and-specialist-cores.md` for route leases, specialist registry records, routing decisions, route receipts, rejected alternatives, readiness/fallback, residuals, MoECOT crosswalk limits, and audio treatment. | Drafting-only curated reader prose pass recorded in `docs/curated_reader_routing_heads_prose_pass.md`; no release blocker cleared. |
| `personal-compute-hives-and-federated-edge-intelligence` | Retain policy-first scheduling, device and portal authority boundaries, consent, privacy, family/project mediation, rented-node limits, revocation, evidence return, and implementation non-claims in the reader chapter. | Drafting companion note added at `editions/reader_manuscript/v1_0/companion_notes/personal-compute-hives-and-federated-edge-intelligence.md` for hive object vocabulary, scheduler decisions, approval receipts, federation leases, rented-node boundaries, and audio treatment. | Drafting-only curated reader prose pass recorded in `docs/curated_reader_personal_compute_hives_prose_pass.md`; no release blocker cleared. |
| `compact-generative-systems-and-residual-honesty` | Retain compactness-as-claim, verifier separation, generate/verify/repair receipts, repair residuals, fallback, semantic representation leases, consumer policy, residual-cost ownership, and non-claims in the reader chapter. | Drafting companion note added at `editions/reader_manuscript/v1_0/companion_notes/compact-generative-systems-and-residual-honesty.md` for Compact Generative Record vocabulary, GVR receipt flow, residual burden, literal fallback, Semantic Node Records, and audio treatment. | Drafting-only curated reader prose pass recorded in `docs/curated_reader_compact_generative_systems_prose_pass.md`; no release blocker cleared. |
| `fast-generation-architectures` | Retain proposed-versus-accepted output, verifier cost, fallback, repair, memory pressure, task success, route promotion, benchmark, serving, and no-speed-claim boundaries in the reader chapter. | Drafting companion note added at `editions/reader_manuscript/v1_0/companion_notes/fast-generation-architectures.md` for generation-mode taxonomy, speed-quality ledgers, verifier bottlenecks, serving-memory boundaries, fallback, and audio treatment. | Drafting-only curated reader prose pass recorded in `docs/curated_reader_fast_generation_prose_pass.md`; no release blocker cleared. |
| `resource-economics-and-token-budgets` | Retain verification tax, protected overhead, route eligibility, residual ownership, local evidence-lane boundaries, sublane no-change/no-promotion decisions, serving-memory separation, scheduler non-claims, and economic non-claims in the reader chapter. | Drafting companion note added at `editions/reader_manuscript/v1_0/companion_notes/resource-economics-and-token-budgets.md` for Resource Budget Records, costed-route slices, workflow traces, local probes, load-stability probes, CI cost metadata, and audio treatment. | Drafting-only curated reader prose pass recorded in `docs/curated_reader_resource_economics_prose_pass.md`; no release blocker cleared. |
| `circle-calculus-and-proof-carrying-ai-contracts` | Retain proof receipt states, theorem references, resolver/replay boundaries, consumer gates, workload blockers, and non-claims in the reader chapter. | Drafting companion note added at `editions/reader_manuscript/v1_0/companion_notes/circle-calculus-and-proof-carrying-ai-contracts.md` for receipt-state glossary, theorem laundering, fingerprints, replay, workload-blocked promotion, and audio treatment. | Drafting-only curated reader prose pass recorded in `docs/curated_reader_circle_contracts_prose_pass.md`; no release blocker cleared. |
| `coilra-multicoil-rope-and-cyclic-mixers` | Retain cyclic-substrate adoption discipline, structural receipts, alias/load diagnostics, parameter and hardware ledgers, baseline symmetry, negative controls, tradeoff packets, canary-route state, fallback, and quality/performance non-claims in the reader chapter. | Drafting companion note added at `editions/reader_manuscript/v1_0/companion_notes/coilra-multicoil-rope-and-cyclic-mixers.md` for cyclic-substrate evaluation records, structural receipts, alias/load diagnostics, baseline symmetry, tradeoff packets, canary routes, and audio treatment. | Drafting-only curated reader prose pass recorded in `docs/curated_reader_coilra_cyclic_mixers_prose_pass.md`; no release blocker cleared. |
| `executable-specifications-and-lean-proof-envelope` | Retain the distinction between Lean predicates, schemas, validators, behavior tests, benchmarks, external theorem references, and semantic adequacy review. | Drafting companion note added at `editions/reader_manuscript/v1_0/companion_notes/executable-specifications-and-lean-proof-envelope.md` for proof-lane glossary, finite-predicate examples, semantic adequacy, and audio treatment. | Drafting-only curated reader prose pass recorded in `docs/curated_reader_executable_specs_prose_pass.md`; no release blocker cleared. |
| `policy-optimization-and-learning-from-feedback` | Retain policy-update-as-lease framing, target-policy identity, feedback admissibility, reward boundary, drift limits, holdouts, regressions, reward-hacking probes, authority conservation, rollback, promotion gates, method-family non-claims, proof/test limits, and no-training-result boundaries in the reader chapter. | Drafting companion note added at `editions/reader_manuscript/v1_0/companion_notes/policy-optimization-and-learning-from-feedback.md` for Policy Optimization Records, reward/preference boundaries, reward-hacking probes, holdouts, regressions, authority effects, rollback, monitor windows, method-family limits, and audio treatment. | Drafting-only curated reader prose pass recorded in `docs/curated_reader_policy_optimization_prose_pass.md`; no release blocker cleared. |
| `artifact-steward-agents-and-living-project-governance` | Retain charter, work contract, contribution ledger, treasury policy, event taint, steward action, sunset, federation, and non-ownership boundaries. | Drafting companion note added at `editions/reader_manuscript/v1_0/companion_notes/artifact-steward-agents-and-living-project-governance.md` for project-object quick reference, implementation ladder, and audio treatment; the first curated prose pass still remains drafting-only. | Drafting-only curated reader prose pass recorded; no release blocker cleared. |
| `project-theseus-as-report-first-implementation-reference` | Retain Theseus as report-first implementation-reference context, with source-note, imported-report, replay-readiness, missing-artifact, public/non-public, currentness, dashboard, benchmark, runtime, model-quality, deployment, and support-state boundaries in the reader chapter. | Drafting companion note added at `editions/reader_manuscript/v1_0/companion_notes/project-theseus-as-report-first-implementation-reference.md` for report-first evidence, architecture-gate imports, generation-mode imports, support replay probes, missing-artifact rows, Theseus Report Crosswalk Records, and audio treatment. | Drafting-only curated reader prose pass recorded in `docs/curated_reader_project_theseus_prose_pass.md`; no release blocker cleared. |

## Routing Rule

Dense material can move to companion support only when the reader chapter still
states the meaning-critical boundary in ordinary prose. Companion notes are for
orientation, reference, and spoken-treatment decisions. They are not allowed to
be the only place where a support limit, proof boundary, governance boundary,
release blocker, or non-claim appears.

For audio, these chapters should be narrated as arguments first and field lists
second. Exact record names, lifecycle states, and proof-lane vocabulary can be
summarized in the script and routed to companion notes, but the spoken script
must preserve the claim boundary.

## Non-Claims

- This review does not approve a reader release.
- This review does not approve EPUB, PDF, DOCX, HTML, AZW3, MOBI, Markdown,
  plain-text, MP3, M4B, or audio-embedded EPUB artifacts.
- This review records that forty-four curated reader chapters now exist, with
  zero drafting records and forty-four reconciled prose records; it does not
  approve any chapter for release.
- This review records twelve drafting companion notes for dense planning,
  routing, hive, compression, speed, resource, proof, cyclic-substrate, policy,
  governance, and implementation-reference chapters; it does not approve them as
  e-reader, audio, or release artifacts.
- This review does not promote any claim support state.
- This review does not claim planner quality, route quality, hive scheduler
  execution, federation safety, speedup, compression utility, semantic
  adequacy, deployed scheduler behavior, production workload quality, proof
  adequacy, cyclic-substrate quality, policy-training quality, Project Theseus
  live replay, Circle theorem replay, steward workflow execution, treasury
  execution, governance correctness, audiobook quality, or release readiness.
