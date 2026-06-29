# Non-Core Evidence Ledger

Last updated: 2026-06-29

This ledger makes the currently accepted non-core evidence transitions visible
without promoting any chapter core claim. It is a public trust surface for
readers, reviewers, and future writing agents.

## Current Boundary

| Field | Status |
|---|---|
| Chapter core claims | All 54 remain at `argument`. |
| Accepted non-core upward transitions | 3 narrow transitions. |
| Chapter-core promotion effect | None. |
| External review status | Public review request opened in GitHub issue #1; no independent external human review record yet. |
| Project Theseus/Circle status | Circle has the bounded prototype-backed receipt transition below plus a separate ASI-side public consumer gate at `docs/circle_public_replay_consumer_gate.md` that CI verifies by digest and negative controls; Project Theseus has a separate public-safe static architecture-gate report import at `docs/theseus_report_import_slice.md` that CI verifies by digest and negative controls. Neither side lane promotes a chapter core claim, and the Project Theseus import plus Circle consumer gate do not create accepted support-state transitions. |

## Accepted Non-Core Transitions

| Claim ID | New support state | Evidence packet | What moved | What did not move |
|---|---|---|---|---|
| `living-book-methodology.phase5_harness_registry_runner` | `synthetic-test-backed` | `docs/phase5_harness_runner.md`; `evidence_transitions/v1_0_measured/phase5_harness_runner_synthetic_test_backed.json` | The repository-infrastructure claim that the Phase 5 harness registry can be replayed by one local runner command, executes all registered synthetic harnesses, and matches each registry result summary. | No chapter core claim, deployed runtime behavior, model quality, benchmark quality, source interpretation, safety, alignment, or governance-effectiveness claim moved. |
| `resource-economics.costed_route_budget_slice` | `synthetic-test-backed` | `docs/costed_route_resource_slice.md`; `evidence_transitions/v1_0_measured/costed_route_resource_slice_synthetic_test_backed.json` | The bounded synthetic costed-route/resource-budget selector slice that rejects a cheap failed negative control, keeps an adequate overkill baseline, and selects the lowest-cost eligible route in the public-safe fixture. | No chapter core claim, deployed routing, scheduler, runtime, load, KV-cache, economic, benchmark, model-quality, safety, or source-interpretation claim moved. |
| `circle-calculus.external_rope_receipt_replay` | `prototype-backed` | `docs/circle_external_receipt_slice.md`; `evidence_transitions/v1_0_measured/circle_external_rope_receipt_prototype_backed.json` | The bounded imported external-prototype receipt fact that a clean local Circle checkout at commit `63b0f511` built the Circle target, certified one rope position distinguishability contract, emitted/accepted the recorded receipt, and passed the selected receipt/contract test batch summarized in the public-safe result record. | No chapter core claim, deployed proof-contract transport, model quality, reasoning ability, context length, speed, memory scaling, transfer, benchmark, safety, or ASI claim moved. |

## How To Promote Anything Later

A future upward transition needs a separate accepted evidence-transition record
that names the exact claim, artifact, command or replay path, limitations,
counterevidence, downgrade triggers, non-claims, and support-state effect.
External citations, source notes, green validators, local project summaries, or
reader-quality edits do not promote a claim by themselves.

## Validation

The ledger is checked by `scripts/validate_non_core_evidence_ledger.py`. That
validator reads the accepted transition records under
`evidence_transitions/v1_0_measured/`, checks that all three current non-core
claims are listed here, checks the chapter-core non-promotion boundary, and
checks that the public entry surfaces link to this ledger.

## Non-Claims

- This ledger does not create new evidence.
- This ledger does not create an independent external review record.
- This ledger does not vendor Project Theseus or Circle, live-replay Project
  Theseus, or promote the Project Theseus static import into chapter-core
  evidence.
- This ledger does not promote any chapter core claim above `argument`.
