# Reader Companion Notes

Status: generated starter notes for major-version human-reader review.

These notes are derived from the living book reader-edition generator. They are review aids for e-reader, document, and future audio packaging; they are not the canonical evidence ledger and they do not claim any artifact has been rendered.

## Purpose

Keep human-reader and audiobook companion decisions explicit without making dense live-book scaffolding part of the relaxed reader manuscript.

## Removed Live-Only Sections

| Heading | Removed count |
|---|---:|
| `chapter status` | 55 |
| `claim labels` | 1 |
| `claim-source mapping status` | 40 |
| `codex test plan` | 55 |
| `drafting guardrail` | 55 |
| `external literature queue` | 1 |
| `formalization hooks` | 16 |
| `source crosswalk` | 55 |
| `why codex tests matter` | 1 |

## Reader-Language Transformations

| Transform | Count |
|---|---:|
| `core_claim_markers_removed` | 55 |
| `reader_scaffold_terms_humanized` | 47 |
| `reader_source_appendix_tables_converted` | 2 |
| `support_boilerplate_humanized` | 29 |

## Reader Overlay Delta

- Overlay manifest: `editions/reader_overlays/v1_0/manifest.json`
- Active operations: 75
- Applied operations: 75
- Delta report: `reader_delta_report.md`

Overlay-touched reader files:
- `chapters/artifact-graphs-audit-logs-and-replay.qmd`
- `chapters/artifact-steward-agents-and-living-project-governance.qmd`
- `chapters/asi-is-a-stack-not-a-model.qmd`
- `chapters/benchmark-ratchets-and-anti-goodhart-evidence.qmd`
- `chapters/circle-calculus-and-proof-carrying-ai-contracts.qmd`
- `chapters/cognitive-compilation-and-semantic-ir.qmd`
- `chapters/compact-generative-systems-and-residual-honesty.qmd`
- `chapters/context-transactions-snapshots-mounts-and-taint.qmd`
- `chapters/evidence-states-and-claim-discipline.qmd`
- `chapters/executable-specifications-and-lean-proof-envelope.qmd`
- `chapters/fast-generation-architectures.qmd`
- `chapters/human-intent-as-a-formal-input.qmd`
- `chapters/integrated-reference-architecture.qmd`
- `chapters/intent-to-execution-contracts.qmd`
- `chapters/labor-os-and-typed-jobs.qmd`
- `chapters/living-book-methodology.qmd`
- `chapters/mathematical-and-search-substrates.qmd`
- `chapters/personal-compute-hives-and-federated-edge-intelligence.qmd`
- `chapters/planning-as-a-control-layer.qmd`
- `chapters/policy-optimization-and-learning-from-feedback.qmd`
- `chapters/project-theseus-as-report-first-implementation-reference.qmd`
- `chapters/rankfold-neuralfold-and-artifact-compression.qmd`
- `chapters/readiness-gates-residual-escrow-and-quarantine.qmd`
- `chapters/resource-economics-and-token-budgets.qmd`
- `chapters/routing-heads-and-specialist-cores.qmd`
- `chapters/runtime-adapters-tool-permissions-and-human-approval.qmd`
- `chapters/spinoza-verification-and-proof-carrying-claims.qmd`
- `chapters/system-boundaries-and-authority.qmd`
- `chapters/the-efficient-asi-hypothesis.qmd`
- `chapters/verification-bandwidth-and-context-adequacy.qmd`
- `chapters/virtual-context-abi.qmd`

## Chapter-Level Routing Decisions

- Routing manifest: `editions/reader_manuscript/v1_0/companion_note_routing.json`
- Routing status: `active_review_routing`

| Chapter | Decision | Reader treatment | Companion/audio route |
|---|---|---|---|
| `planning-as-a-control-layer` | `retain_in_reader_spine_with_companion_note` | Keep command-contract inheritance, plan-node lifecycle states, DAG/dependency boundaries, adequacy contracts, dispatch receipts, replanning deltas, residual registers, and planner-quality non-claims in the reader chap... | Use the drafting companion note for e-reader and audio review; it gives a short reference for plan graphs, DAG scheduling, adequacy contracts, dispatch receipts, replanning history, residual registers, and finite proo... |
| `routing-heads-and-specialist-cores` | `retain_in_reader_spine_with_companion_note` | Keep route-as-lease framing, specialist registry boundaries, routing decision records, selected authority subsets, rejected alternatives, readiness/fallback boundaries, residual ownership, MoECOT source-boundary cavea... | Use the drafting companion note for e-reader and audio review; it gives a short reference for Specialist Registry Records, Routing Decision Records, route receipts, rejected alternatives, readiness/fallback, residuals... |
| `personal-compute-hives-and-federated-edge-intelligence` | `retain_in_reader_spine_with_companion_note` | Keep policy-first scheduling, device and portal authority boundaries, consent, privacy, family and project mediation, rented-node limits, revocation, evidence return, and implementation non-claims in the reader chapter. | Use the drafting companion note for e-reader and audio review; it gives a short reference for Device Resource Cards, Portal Cards, Hive Job Contracts, Hive Job Bids, Hive Scheduling Decisions, approval receipts, feder... |
| `compact-generative-systems-and-residual-honesty` | `retain_in_reader_spine_with_companion_note` | Keep compactness-as-claim, verifier separation, repair residuals, fallback, semantic representation leases, consumer policy, cost ownership, and non-claim boundaries in the reader chapter. | Use the drafting companion note for e-reader and audio review; it gives a short reference for Compact Generative Records, generate/verify/repair receipts, residual burden, literal fallback, and Semantic Node Records.... |
| `fast-generation-architectures` | `retain_in_reader_spine_with_companion_note` | Keep proposed-versus-accepted output, verifier cost, fallback, repair, memory pressure, task success, route promotion, benchmark, serving, and no-speed-claim boundaries in the reader chapter. | Use the drafting companion note for e-reader and audio review; it gives a short reference for accelerated generation families, speed-quality ledgers, proposed/accepted output separation, verifier bottlenecks, serving-... |
| `resource-economics-and-token-budgets` | `retain_in_reader_spine_with_companion_note` | Keep verification tax, protected overhead, route eligibility, residual ownership, no-change sublane decisions, serving-memory separation, scheduler non-claims, and economic non-claims in the reader chapter. | Use the drafting companion note for e-reader and audio review; it gives a short reference for Resource Budget Records, costed-route slices, workflow traces, local probes, load-stability probes, CI cost metadata, and n... |
| `circle-calculus-and-proof-carrying-ai-contracts` | `retain_in_reader_spine_with_companion_note` | Keep proof receipt states, theorem references, resolver and replay boundaries, consumer gates, workload blockers, and explicit non-claims in the reader chapter; the drafting curated reader source must preserve those b... | Use the drafting companion note for e-reader and audio review; it gives a short glossary for proof receipt, theorem-linked receipt, resolver-checked, consumer-gated, workload-blocked, fingerprint, replay, and theorem... |
| `coilra-multicoil-rope-and-cyclic-mixers` | `retain_in_reader_spine_with_companion_note` | Keep cyclic-substrate adoption discipline, structural receipts, alias/load diagnostics, parameter and hardware ledgers, baseline symmetry, negative controls, tradeoff packets, canary-route state, fallback, and quality... | Use the drafting companion note for e-reader and audio review; it gives a short reference for cyclic-substrate evaluation records, structural receipts, alias/load diagnostics, baseline symmetry, tradeoff packets, and... |
| `executable-specifications-and-lean-proof-envelope` | `retain_in_reader_spine_with_companion_note` | Keep the distinction between Lean predicates, schemas, process validators, behavior tests, benchmarks, external theorem references, semantic adequacy review, and research backlog in the reader chapter; the drafting cu... | Use the drafting companion note to map proof lanes to ordinary reader language and explain why each lane has a different authority boundary. Narrate the proof envelope as a claims-control discipline and route detailed... |
| `policy-optimization-and-learning-from-feedback` | `retain_in_reader_spine_with_companion_note` | Keep policy-update-as-lease framing, target-policy identity, feedback admissibility, reward boundary, drift limits, holdouts, regressions, reward-hacking probes, authority conservation, rollback, promotion gates, meth... | Use the drafting companion note for e-reader and audio review; it gives a short reference for Policy Optimization Records, reward/preference boundaries, reward-hacking probes, holdouts, regressions, authority effects,... |
| `artifact-steward-agents-and-living-project-governance` | `future_curated_review_with_companion_note` | Keep charter, work contract, contribution ledger, treasury policy, event taint, steward action, sunset, worker federation, project-economy, and non-ownership boundaries in the reader chapter for v1.0. | Use the drafting companion note for the implementation ladder and project-object quick reference; revisit curated reader compression during release editing if the chapter still feels too long. Summarize project object... |
| `project-theseus-as-report-first-implementation-reference` | `retain_in_reader_spine_with_companion_note` | Keep Theseus as report-first implementation-reference context, with source-note, imported-report, replay-readiness, missing-artifact, public/non-public, currentness, dashboard, benchmark, runtime, model-quality, deplo... | Use the drafting companion note for e-reader and audio review; it gives a short reference for report-first evidence, architecture-gate imports, generation-mode imports, support replay probes, missing-artifact rows, an... |

Routing note: meaning-critical caveats, support limits, proof boundaries, governance boundaries, release blockers, and non-claims must remain in the reader manuscript. Companion notes can help with glossary, quick-reference, and spoken-treatment support, but they are not a substitute for the reader spine.

## Companion Topics To Review

- [ ] meaning-carrying diagrams and images
- [ ] key-figure spoken summaries in editions/reader_manuscript/v1_0/companion_notes/key-figures.md
- [ ] tables that should be summarized rather than read verbatim
- [ ] code, schemas, and proof-adjacent passages that need companion treatment
- [ ] omitted source matrices, guardrails, validation details, and release machinery
- [ ] audio-embedded EPUB packaging and navigation checks

## Review Requirements

- [ ] Companion notes must say which dense material was omitted, summarized, retained, or moved.
- [ ] Meaning-changing uncertainty must stay in the reader or spoken prose, not only in companion notes.
- [ ] Audio companion notes must be reviewed before MP3, M4B, or audio-embedded EPUB artifacts are claimed.
- [ ] Reader companion notes must be checked for e-reader usefulness before optional AZW3, MOBI, Markdown, or plain-text derivatives are recorded.

## Artifact Notes

- [ ] Confirm EPUB, PDF, DOCX, HTML, AZW3, MOBI, Markdown, or plain-text artifacts are named only after the corresponding render or conversion succeeds.
- [ ] Confirm audio companion decisions are moved into the audio workspace before MP3, M4B, or audio-embedded EPUB work begins.
- [ ] Confirm meaning-critical caveats remain in the reader manuscript, not only in these notes.

## Non-Claims

- Generated companion notes are review aids, not proof of artifact quality.
- Generated companion notes do not claim that audio files, EPUB packages, or e-reader conversions exist.
