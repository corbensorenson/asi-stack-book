# v1.x Active Evidence Cycle

Last updated: 2026-07-01

This ledger names the current v1.x evidence-cycle chapter lanes selected from
`docs/per_chapter_evidence_plan.md`. It exists to enforce the lane cap: this
cycle selects one flagship measured lane plus two direct support lanes and
leaves the other forty-one chapter lanes planned-only. It is a planning and
release-control record, not a support-state transition.

The selected lanes sit inside a wider defended-contribution pool where the
repository already has public-safe evidence paths. The active execution focus is
resource discipline plus report-first implementation evidence; the other
defended tracks remain visible but are not active chapter lanes in this cycle.
`docs/defended_contribution_tracks.md` records the contribution-track selection
boundary for this cycle: five selected contribution tracks, three deep-work
tracks, a narrower three-lane active evidence cycle, and no chapter-core
promotion.

## Cycle Boundary

| Field | Value |
|---|---|
| Selected chapter lanes | 3 |
| Planned-only chapter lanes | 41 |
| Lane cap | 1 flagship measured lane plus at most 2 direct support lanes per v1.x cycle |
| Flagship measured lane | `resource-economics-and-token-budgets` |
| Direct support lanes | `project-theseus-as-report-first-implementation-reference`; `fast-generation-architectures` |
| Chapter core support effect | None; all 44 chapter core claims remain `argument`. |
| Non-core support effect | Existing non-core transitions remain scoped to their accepted records. |
| No-sweep rule | No 44-lane fixture sweep is claimed or implied. |

## Selected Lanes

| Chapter ID | Status | Strongest current evidence path | Recorded artifact or result | Negative controls or failure cases | Support-state effect | Next blocker |
|---|---|---|---|---|---|---|
| `resource-economics-and-token-budgets` | flagship-executed-narrow | Costed-route/resource-budget synthetic slice plus folded simulation-fidelity contract lane | `docs/costed_route_resource_slice.md`; `experiments/costed_route_resource_slice/results/2026-06-29-local.json`; `lean/AsiStackProofs/ResourceEconomics.lean`; `evidence_transitions/v1_0_measured/costed_route_resource_slice_synthetic_test_backed.json`; `schemas/simulation_contract_record.schema.json`; `docs/simulation_transfer_boundary_harness.md`; `experiments/simulation_transfer_boundaries/results/2026-06-30-local.md` | Cheaper failed-verification route and cheaper hidden-residual route are rejected; adequate overkill baseline remains eligible; the Lean fixture is checked against public JSON costs, selected route, negative controls, and eligibility fields; folded simulation-transfer fixtures reject missing fidelity, unbounded world transfer, missing resource bills, missing bottleneck residuals, ignored instrumentation, and support-state promotion. | Non-core `resource-economics.costed_route_budget_slice` is `synthetic-test-backed`; chapter core remains `argument`; simulation-transfer fixtures do not create a new evidence transition. | Larger public trace with workload quality, displaced-cost accounting, physical-feasibility review, scheduler traces, and real simulation outputs. |
| `project-theseus-as-report-first-implementation-reference` | direct-support-executed-narrow | Public-safe Project Theseus static report imports plus Fast Generation Lean fixture alignment | `docs/theseus_report_import_slice.md`; `experiments/theseus_import/results/2026-06-29-local.json`; `scripts/validate_theseus_report.py`; `docs/theseus_generation_mode_import_slice.md`; `experiments/theseus_generation_mode_import/results/2026-07-01-local.json`; `lean/AsiStackProofs/FastGeneration.lean`; `scripts/validate_theseus_generation_mode_import.py` | Architecture-gate digest mismatch, private-payload copying, and support-promotion overclaim are rejected; generation-mode private-payload copying, support-promotion overclaim, raw-speed promotion, and useful-speed overclaim are rejected; the public generation-mode summary is checked against a finite Fast Generation Lean fixture for counts, no-promotion state, and no-useful-speed evidence. | No accepted support-state transition; chapter core remains `argument`. | Clean live replay or archived public Theseus release fixture plus public task bundle before stronger implementation or generation-mode evidence. |
| `fast-generation-architectures` | direct-support-executed-narrow | Project Theseus generation-mode static import plus finite Fast Generation Lean fixture bridge | `docs/theseus_generation_mode_import_slice.md`; `experiments/theseus_generation_mode_import/results/2026-07-01-local.json`; `lean/AsiStackProofs/FastGeneration.lean`; `scripts/validate_theseus_generation_mode_import.py` | Private-payload copying, support-promotion overclaim, raw-speed promotion, useful-speed overclaim, and imported accepted-span speed-lift without useful-solution evidence are rejected. | No chapter core promotion; core claim remains `argument`; no generation-speed or useful-solution-per-second result is claimed. | Clean Theseus replay or public task bundle with quality/residual review before stronger Fast Generation evidence. |

## Planned-Only Lanes

These chapter lanes stay planned-only for this cycle. They keep their evidence
paths in `docs/per_chapter_evidence_plan.md`, but no chapter-lane completion,
chapter-core fixture sweep, support-state pressure, or release claim is created
for them here. A selected-lane import may name a planned-only chapter as a
connected boundary, but that does not make the planned-only chapter selected or
move its support state.

- `asi-is-a-stack-not-a-model`
- `the-efficient-asi-hypothesis`
- `system-boundaries-and-authority`
- `failure-modes-of-ungoverned-intelligence`
- `evidence-states-and-claim-discipline`
- `human-intent-as-a-formal-input`
- `constitutional-alignment-substrate`
- `moral-uncertainty-and-value-conflict`
- `stable-capability-fields`
- `capability-replacement-and-rollback`
- `security-kernel-and-digital-scifs`
- `recursive-self-improvement-boundaries`
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
- `rankfold-neuralfold-and-artifact-compression`
- `mathematical-and-search-substrates`
- `circle-calculus-and-proof-carrying-ai-contracts`
- `coil-attention-cyclic-memory-and-recurrence-contracts`
- `coilra-multicoil-rope-and-cyclic-mixers`
- `executable-specifications-and-lean-proof-envelope`
- `benchmark-ratchets-and-anti-goodhart-evidence`
- `policy-optimization-and-learning-from-feedback`
- `artifact-steward-agents-and-living-project-governance`
- `integrated-reference-architecture`
- `prototype-roadmap`
- `living-book-methodology`
- `open-research-agenda-and-bibliography-plan`

## Non-Claims

- This ledger does not promote any chapter core claim above `argument`.
- This ledger does not create new evidence or rerun any prototype.
- This ledger does not claim that the selected lanes are complete at A+ depth.
- This ledger does not retire the planned-only lanes.
- This ledger does not approve reader, ebook, PDF, DOCX, audio, DOI, archive, or
  release artifacts.
