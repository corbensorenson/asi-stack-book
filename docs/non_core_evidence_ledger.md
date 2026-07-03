# Non-Core Evidence Ledger

Last updated: 2026-07-03

This ledger makes the currently accepted non-core evidence transitions visible
without promoting any chapter core claim. It is a public trust surface for
readers, reviewers, and future writing agents.

## Current Boundary

| Field | Status |
|---|---|
| Chapter core claims | All 44 remain at `argument`. |
| Accepted non-core upward transitions | 6 narrow transitions. |
| Accepted live claim-surface narrowing records | 1 count-surface correction; no support-state movement. |
| Chapter-core promotion effect | None. |
| External review status | Public review request opened in GitHub issue #1; no independent external human review record yet. |
| Project Theseus/Circle status | Circle has the bounded prototype-backed receipt transition below plus a separate ASI-side public consumer gate at `docs/circle_public_replay_consumer_gate.md` that CI verifies by digest and negative controls; Project Theseus has a separate public-safe static architecture-gate report import at `docs/theseus_report_import_slice.md` that CI verifies by digest and negative controls. Neither side lane promotes a chapter core claim, and the Project Theseus import plus Circle consumer gate do not create accepted support-state transitions. |

## Accepted Non-Core Transitions

| Claim ID | New support state | Evidence packet | What moved | What did not move |
|---|---|---|---|---|
| `living-book-methodology.phase5_harness_registry_runner` | `synthetic-test-backed` | `docs/phase5_harness_runner.md`; `evidence_transitions/v1_0_measured/phase5_harness_runner_synthetic_test_backed.json` | The repository-infrastructure claim that the Phase 5 harness registry can be replayed by one local runner command, executes all registered synthetic harnesses, and matches each registry result summary. | No chapter core claim, deployed runtime behavior, model quality, benchmark quality, source interpretation, safety, alignment, or governance-effectiveness claim moved. |
| `resource-economics.costed_route_budget_slice` | `synthetic-test-backed` | `docs/costed_route_resource_slice.md`; `evidence_transitions/v1_0_measured/costed_route_resource_slice_synthetic_test_backed.json` | The bounded synthetic costed-route/resource-budget selector slice that rejects a cheap failed negative control, keeps an adequate overkill baseline, and selects the lowest-cost eligible route in the public-safe fixture. | No chapter core claim, deployed routing, scheduler, runtime, load, KV-cache, economic, benchmark, model-quality, safety, or source-interpretation claim moved. |
| `resource-economics.finite_burst_load_smoothing_selector` | `synthetic-test-backed` | `docs/resource_load_stability_probe.md`; `evidence_transitions/v1_x_measured/resource_load_stability_selector_synthetic_test_backed.json` | The bounded finite synthetic load-smoothing selector claim that a 10-task burst-review workload selects protected capacity smoothing over admit-arrivals, reduces instability units from 5 to 0, residualizes 7 deferred task-ticks, and rejects a cheaper review-erasure negative control. | No chapter core claim, real load-stability, deployed scheduler, TokenMana, PlanForge, reviewer-optimization, human-productivity, economic, benchmark, model-quality, safety, or source-interpretation claim moved. |
| `resource-economics.scoped_workflow_trace_route_selector` | `empirical-test-backed` | `docs/resource_workload_quality_probe.md`; `evidence_transitions/v1_x_measured/resource_workload_quality_selector_empirical_test_backed.json` | The bounded local repository-task selector claim that five measured samples per route select the scoped workflow-trace validator over the broader Resource live-probe baseline while rejecting a cheaper no-op success-text command that exits 0 without producing the required validation surface. | No chapter core claim, broader workload-quality claim, stable-speedup claim, deployed scheduler, TokenMana, PlanForge, production workload, economic, benchmark, model-quality, safety, or source-interpretation claim moved. |
| `circle-calculus.external_rope_receipt_replay` | `prototype-backed` | `docs/circle_external_receipt_slice.md`; `evidence_transitions/v1_0_measured/circle_external_rope_receipt_prototype_backed.json` | The bounded imported external-prototype receipt fact that a clean local Circle checkout at commit `63b0f511` built the Circle target, certified one rope position distinguishability contract, emitted/accepted the recorded receipt, and passed the selected receipt/contract test batch summarized in the public-safe result record. | No chapter core claim, deployed proof-contract transport, model quality, reasoning ability, context length, speed, memory scaling, transfer, benchmark, safety, or ASI claim moved. |
| `compact-generative-systems.compact_gvr_receipt_slice` | `synthetic-test-backed` | `docs/compact_gvr_slice.md`; `evidence_transitions/v1_x_measured/compact_gvr_slice_synthetic_test_backed.json` | The bounded synthetic compact-generation/GVR receipt claim that a local validator compares a 368-byte literal baseline to a 78-byte exact compact generator-plus-repair receipt, rejects lossy exactness, negative-rate/no-fallback, and bounded-search-overrun controls, and checks a finite Lean fixture bridge. | No chapter core claim, deployed compression, codec correctness, semantic utility, fallback execution, benchmark, model-quality, safety, ASI, or source-interpretation claim moved. |

## Live Claim-Surface Narrowing Records

| Claim surface | Record | What narrowed | Support-state effect |
|---|---|---|---|
| `non-core-evidence-ledger.chapter-core-count-surface` | `claim_revisions/v1_x/manifest_core_claim_count_narrowing.json` | The obsolete public count phrase "All 54 remain at `argument`" was narrowed to the current manifest state, "All 44 remain at `argument`," based on `book_structure.json` and `docs/core_claim_transition_coverage.md`. | None; this is a count-surface correction, not a demotion, refutation, or promotion. |

## How To Promote Anything Later

A future upward transition needs a separate accepted evidence-transition record
that names the exact claim, artifact, command or replay path, limitations,
counterevidence, downgrade triggers, non-claims, and support-state effect.
External citations, source notes, green validators, local project summaries, or
reader-quality edits do not promote a claim by themselves.

## Validation

The ledger is checked by `scripts/validate_non_core_evidence_ledger.py`. That
validator reads the accepted transition records under
`evidence_transitions/v1_0_measured/` and `evidence_transitions/v1_x_measured/`,
checks that all six current non-core claims are listed here, checks the live
claim-surface narrowing record, checks the chapter-core non-promotion boundary,
and checks that the public entry surfaces link to this ledger. The live
revision record is also checked by `scripts/validate_claim_revision_records.py`.

## Non-Claims

- This ledger does not create new evidence.
- This ledger does not demote, deprecate, or refute any chapter core claim.
- This ledger does not create an independent external review record.
- This ledger does not vendor Project Theseus or Circle, live-replay Project
  Theseus, or promote the Project Theseus static import into chapter-core
  evidence.
- This ledger does not promote any chapter core claim above `argument`.
