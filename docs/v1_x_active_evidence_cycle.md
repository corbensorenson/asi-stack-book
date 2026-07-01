# v1.x Active Evidence Cycle

Last updated: 2026-07-01

This ledger names the current v1.x evidence-cycle chapter lanes selected from
`docs/per_chapter_evidence_plan.md`. It exists to enforce the lane cap: this
cycle selects eight high-payoff lanes and leaves the other thirty-six chapter
lanes planned-only. It is a planning and release-control record, not a
support-state transition.

The selected lanes map to defended contribution tracks where the repository
already has public-safe evidence paths: living evidence methodology, evidence
laundering prevention, governed self-improvement, proof-carrying claims,
resource discipline, and report-first implementation evidence.
`docs/defended_contribution_tracks.md` records the contribution-track selection
boundary for this cycle: five selected tracks, three deep-work tracks, and no
chapter-core promotion.

## Cycle Boundary

| Field | Value |
|---|---|
| Selected chapter lanes | 8 |
| Planned-only chapter lanes | 36 |
| Lane cap | 5-8 selected lanes per v1.x cycle |
| Chapter core support effect | None; all 44 chapter core claims remain `argument`. |
| Non-core support effect | Existing non-core transitions remain scoped to their accepted records. |
| No-sweep rule | No 44-lane fixture sweep is claimed or implied. |

## Selected Lanes

| Chapter ID | Status | Strongest current evidence path | Recorded artifact or result | Negative controls or failure cases | Support-state effect | Next blocker |
|---|---|---|---|---|---|---|
| `evidence-states-and-claim-discipline` | executed-narrow | Claim/evidence ledgers, explicit no-promotion decisions, terminal-state Lean envelope, synthetic demotion/refutation fixtures, and one live count-surface narrowing record | `docs/non_core_evidence_ledger.md`; `docs/core_claim_transition_coverage.md`; `claim_decisions/v1_0_core_claim_no_promotion.json`; `claim_revisions/v1_x/manifest_core_claim_count_narrowing.json`; `docs/defended_contribution_prior_art_positioning.md`; `lean/AsiStackProofs/EvidenceStates.lean`; `docs/support_state_transition_harness.md` | No-promotion decisions and support-state transition validators reject unsupported promotion, reasonless demotion, and unsupported refutation; the live narrowing record corrects a stale public count surface from 54 to 44 without moving support state. | No chapter core promotion, demotion, deprecation, or refutation; core claim remains `argument`; the claim-surface narrowing has no support-state effect. | External review and a true chapter-core demotion/refutation record before stronger methodology claims. |
| `recursive-self-improvement-boundaries` | executed-narrow | Safety-critical Lean envelope plus Project Theseus architecture-gate import | `lean/AsiStackProofs/SelfImprovement.lean`; `docs/proof_depth_classification.md`; `docs/theseus_report_import_slice.md` | Authority-widening negative case is blocked in Lean; Theseus import rejects support-promotion overclaim. | No chapter core promotion; core claim remains `argument`. | Clean Theseus replay or archived public fixture before stronger implementation evidence. |
| `resource-economics-and-token-budgets` | executed-narrow | Costed-route/resource-budget synthetic slice plus folded simulation-fidelity contract lane | `docs/costed_route_resource_slice.md`; `experiments/costed_route_resource_slice/results/2026-06-29-local.json`; `evidence_transitions/v1_0_measured/costed_route_resource_slice_synthetic_test_backed.json`; `schemas/simulation_contract_record.schema.json`; `docs/simulation_transfer_boundary_harness.md`; `experiments/simulation_transfer_boundaries/results/2026-06-30-local.md` | Cheaper failed-verification route and cheaper hidden-residual route are rejected; adequate overkill baseline remains eligible; folded simulation-transfer fixtures reject missing fidelity, unbounded world transfer, missing resource bills, missing bottleneck residuals, ignored instrumentation, and support-state promotion. | Non-core `resource-economics.costed_route_budget_slice` is `synthetic-test-backed`; chapter core remains `argument`; simulation-transfer fixtures do not create a new evidence transition. | Larger public trace with workload quality, displaced-cost accounting, physical-feasibility review, scheduler traces, and real simulation outputs. |
| `circle-calculus-and-proof-carrying-ai-contracts` | executed-narrow | Circle external receipt slice plus ASI-side consumer gate | `docs/circle_external_receipt_slice.md`; `docs/circle_public_replay_consumer_gate.md`; `experiments/circle_public_replay/results/2026-06-29-local.json` | Missing theorem ID, digest mismatch, stale contract status, and unsupported transfer claim are rejected. | Non-core `circle-calculus.external_rope_receipt_replay` is `prototype-backed`; chapter core remains `argument`. | Clean Circle replay from this repo, public contract pack, or archived upstream pack before stronger proof-transport claims. |
| `coil-attention-cyclic-memory-and-recurrence-contracts` | executed-narrow | Coil/Circle structural memory records, finite Lean negative cases, and synthetic cyclic-memory contract harness | `docs/cyclic_memory_contract_harness.md`; `experiments/cyclic_memory_contracts/results/2026-06-30-local.md`; `lean/AsiStackProofs/CoilAttentionMemory.lean`; `schemas/cyclic_memory_contract.schema.json` | Hidden aliasing, sparse gaps without fallback, recurrence without exit, stale-read admission without residual escrow, structural-quality promotion, and support-state promotion are rejected by synthetic fixtures or finite Lean predicates. | No chapter core promotion; core claim remains `argument`. | KV-cache certifiers, recurrence benchmarks, learned-memory workloads, retrieval-quality tests, long-context tests, Circle commands, and Theseus transfer consumers before stronger memory claims. |
| `executable-specifications-and-lean-proof-envelope` | executed-supporting | Proof-depth classifier, proof adequacy review, and safety-critical Lean sweep | `docs/proof_depth_classification.md`; `docs/proof_adequacy_review.md`; `docs/proof_artifact_audit.md`; `lake build` | Five safety-critical modules now include derived/decomposed theorem coverage with rejected or blocked negative cases. | No chapter core promotion; core claim remains `argument`. | Richer state machines, executable behavior tests, and proof-review semantics. |
| `project-theseus-as-report-first-implementation-reference` | executed-narrow | Public-safe Project Theseus static report import | `docs/theseus_report_import_slice.md`; `experiments/theseus_import/results/2026-06-29-local.json`; `scripts/validate_theseus_report.py` | Digest mismatch, private-payload copying, and support-promotion overclaim are rejected. | No accepted support-state transition; chapter core remains `argument`. | Clean live replay or archived public Theseus release fixture. |
| `living-book-methodology` | executed-narrow | Phase 5 harness registry runner plus release-control validators | `docs/phase5_harness_runner.md`; `experiments/phase5_harness_registry.json`; `evidence_transitions/v1_0_measured/phase5_harness_runner_synthetic_test_backed.json`; `docs/defended_contribution_prior_art_positioning.md` | Registry guard checks command, doc, fixture-count, result, Appendix E, public-status, and non-claim wiring. | Non-core `living-book-methodology.phase5_harness_registry_runner` is `synthetic-test-backed`; chapter core remains `argument`. | External review and a concise novelty note before stronger methodology claims. |

## Planned-Only Lanes

These chapter lanes stay planned-only for this cycle. They keep their evidence
paths in `docs/per_chapter_evidence_plan.md`, but no fixture, pass/fail result,
support-state pressure, or release claim is created for them here.

- `asi-is-a-stack-not-a-model`
- `the-efficient-asi-hypothesis`
- `system-boundaries-and-authority`
- `failure-modes-of-ungoverned-intelligence`
- `human-intent-as-a-formal-input`
- `constitutional-alignment-substrate`
- `moral-uncertainty-and-value-conflict`
- `stable-capability-fields`
- `capability-replacement-and-rollback`
- `security-kernel-and-digital-scifs`
- `intent-to-execution-contracts`
- `planning-as-a-control-layer`
- `cognitive-compilation-and-semantic-ir`
- `virtual-context-abi`
- `context-transactions-snapshots-mounts-and-taint`
- `verification-bandwidth-and-context-adequacy`
- `claim-ledgers-and-belief-revision`
- `spinoza-verification-and-proof-carrying-claims`
- `labor-os-and-typed-jobs`
- `artifact-graphs-audit-logs-and-replay`
- `runtime-adapters-tool-permissions-and-human-approval`
- `procedural-memory-and-cognitive-loop-closure`
- `routing-heads-and-specialist-cores`
- `readiness-gates-residual-escrow-and-quarantine`
- `personal-compute-hives-and-federated-edge-intelligence`
- `compact-generative-systems-and-residual-honesty`
- `fast-generation-architectures`
- `rankfold-neuralfold-and-artifact-compression`
- `mathematical-and-search-substrates`
- `coilra-multicoil-rope-and-cyclic-mixers`
- `benchmark-ratchets-and-anti-goodhart-evidence`
- `policy-optimization-and-learning-from-feedback`
- `artifact-steward-agents-and-living-project-governance`
- `integrated-reference-architecture`
- `prototype-roadmap`
- `open-research-agenda-and-bibliography-plan`

## Non-Claims

- This ledger does not promote any chapter core claim above `argument`.
- This ledger does not create new evidence or rerun any prototype.
- This ledger does not claim that the selected lanes are complete at A+ depth.
- This ledger does not retire the planned-only lanes.
- This ledger does not approve reader, ebook, PDF, DOCX, audio, DOI, archive, or
  release artifacts.
