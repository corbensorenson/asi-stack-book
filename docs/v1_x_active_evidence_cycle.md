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
| `resource-economics-and-token-budgets` | flagship-executed-narrow | Costed-route/resource-budget synthetic slice, deterministic workflow trace, capacity-smoothing reviewer-capacity trace, local command-replay live probe, local five-sample measured workload-quality probe, local synthetic load-stability probe, CI publication cost profile, folded simulation-fidelity contract lane, explicit sublane no-promotion decisions, and aggregate one-command flagship replay | `docs/costed_route_resource_slice.md`; `experiments/costed_route_resource_slice/results/2026-06-29-local.json`; `lean/AsiStackProofs/ResourceEconomics.lean`; `evidence_transitions/v1_0_measured/costed_route_resource_slice_synthetic_test_backed.json`; `docs/resource_workflow_trace.md`; `experiments/resource_workflow_trace/results/2026-07-01-local.json`; `scripts/validate_resource_workflow_trace.py`; `docs/capacity_smoothing_harness.md`; `experiments/capacity_smoothing/results/2026-07-01-local.md`; `scripts/validate_capacity_smoothing.py`; `docs/resource_live_probe.md`; `experiments/resource_live_probe/results/2026-07-01-local.json`; `scripts/validate_resource_live_probe.py`; `docs/resource_workload_quality_probe.md`; `experiments/resource_workload_quality_probe/results/2026-07-01-local.json`; `scripts/run_resource_workload_quality_probe.py`; `scripts/validate_resource_workload_quality_probe.py`; `docs/resource_load_stability_probe.md`; `experiments/resource_load_stability_probe/results/2026-07-01-local.json`; `scripts/run_resource_load_stability_probe.py`; `scripts/validate_resource_load_stability_probe.py`; `docs/resource_ci_cost_profile.md`; `experiments/resource_ci_cost_profile/results/2026-07-01-main.json`; `scripts/validate_resource_ci_cost_profile.py`; `evidence_transitions/v1_x_measured/resource_workflow_trace_no_change.json`; `evidence_transitions/v1_x_measured/resource_live_probe_no_change.json`; `evidence_transitions/v1_x_measured/resource_workload_quality_probe_no_change.json`; `evidence_transitions/v1_x_measured/resource_load_stability_probe_no_change.json`; `evidence_transitions/v1_x_measured/resource_ci_cost_profile_no_change.json`; `schemas/simulation_contract_record.schema.json`; `docs/simulation_transfer_boundary_harness.md`; `experiments/simulation_transfer_boundaries/results/2026-06-30-local.md`; `docs/resource_flagship_lane_run.md`; `experiments/resource_flagship_lane/results/2026-07-01-local.json`; `scripts/run_resource_flagship_lane.py`; `scripts/validate_resource_flagship_lane.py` | Cheaper failed-verification route and cheaper hidden-residual route are rejected; adequate overkill baseline remains eligible; the Lean fixture is checked against public JSON costs, selected route, negative controls, eligibility fields, and the finite selector-state trace theorem `costed_route_fixture_trace_selects_lowest_eligible_route`; the workflow trace rejects latency-only selection, erased displaced costs, over-budget aggregate resource bills, physical-feasibility overclaim, and low-risk work scheduled before protected high-risk review, and its Lean bridge now checks finite dispatch-event rollup, high-risk-first order, guard flags, review minutes, verification minutes, capacity-budget-overrun rejection, and no-promotion boundaries; the capacity-smoothing harness checks 3 valid and 6 expected-invalid toy traces for reviewer-capacity arithmetic, protected-review overhead, displaced-review-cost residualization, low-risk review hoarding, erased protected overhead, over-admission, load-stability overclaim, and no-promotion boundaries, with a finite Lean bridge for the reviewer-capacity trace and negative cases; the resource budget ledger harness checks 6 valid and 7 expected-invalid fixtures for KV-cache/serving-memory accounting separation and throughput-to-quality overclaim rejection; the local live probe replays five Resource Economics validators and checks command-output plus tracked-artifact digests; the local workload-quality probe selects a scoped workflow-trace validator over a broader Resource live-probe baseline by five-sample median elapsed time and rejects a cheaper no-op success-text route that exits 0 without running the required validator; the local synthetic load-stability probe selects protected capacity smoothing over an admit-arrivals baseline in a finite 10-task workload, residualizes 7 selected deferrals, checks a finite ResourceEconomics Lean bridge, and rejects a cheaper review-erasure route with 3 protected-review violations and hidden deferrals; the CI cost profile records eight actual Pages runs, one generated-scaffold failure, one repair run, and publication-duration metrics; folded simulation-transfer fixtures reject missing fidelity, unbounded world transfer, missing resource bills, missing bottleneck residuals, ignored instrumentation, and support-state promotion; the five sublane no-promotion records block promotion for workflow-trace, local-replay, workload-quality, load-stability, and CI-cost claims unless stronger live or externally reviewed artifacts appear; the aggregate flagship replay reruns 10 validators, checks 25 tracked artifact digests, composes the accepted non-core transition, no-change chapter-core decision, and sublane no-promotion records, and preserves residual and non-claim boundaries. | Non-core `resource-economics.costed_route_budget_slice` is `synthetic-test-backed`; chapter core remains `argument`; workflow-trace, local-replay, workload-quality, load-stability, and CI-cost sublanes now have accepted `blocks_promotion` no-change records; capacity-smoothing, simulation-transfer, and aggregate flagship artifacts remain non-promoting; none of these artifacts create an upward chapter-core transition. | External or live workload-facing trace beyond the local repository task with real workload quality review, production scheduler logs beyond CI metadata, measured displaced-cost accounting, physical-feasibility review, live or externally reviewed load-stability workload, real KV-cache/serving-memory measurement, and measured rather than fixture-declared simulation outputs. |
| `project-theseus-as-report-first-implementation-reference` | direct-support-executed-narrow | Public-safe Project Theseus static report imports, Fast Generation Lean fixture alignment, local Theseus support replay probe, and bounded public task-bundle summary import | `docs/theseus_report_import_slice.md`; `experiments/theseus_import/results/2026-06-29-local.json`; `scripts/validate_theseus_report.py`; `docs/theseus_generation_mode_import_slice.md`; `experiments/theseus_generation_mode_import/results/2026-07-01-local.json`; `lean/AsiStackProofs/FastGeneration.lean`; `scripts/validate_theseus_generation_mode_import.py`; `docs/theseus_support_replay_probe.md`; `experiments/theseus_support_replay_probe/results/2026-07-01-local.json`; `scripts/run_theseus_support_replay_probe.py`; `scripts/validate_theseus_support_replay_probe.py`; `docs/theseus_public_task_bundle_import.md`; `experiments/theseus_public_task_bundle_import/results/2026-07-03-local.json`; `scripts/validate_theseus_public_task_bundle_import.py`; `theseus_public_task_bundle_import_2026_07_03_local`; `lean/AsiStackProofs/TheseusReference.lean` | Architecture-gate digest mismatch, private-payload copying, and support-promotion overclaim are rejected; generation-mode hard boundary-gate failure, private-payload copying, missing-report-ref overclaim, support-promotion overclaim, raw-speed promotion, and useful-speed overclaim are rejected; the public generation-mode summary is checked against a finite Fast Generation Lean fixture for counts, no-promotion state, all-gates-passed state, zero missing report refs, and no-useful-speed evidence; the support replay probe reruns both validators and checks command-output digests plus tracked artifact hashes; the public task-bundle import checks 64 public BigCodeBench metadata-only tasks, 0 public training rows, 0 task-level regressions, 18 benchmark gates, 19 residuals, visible artifact gaps, seven expected-invalid controls, and the finite TheseusReference bridge while preserving that clean live Theseus replay remains unclaimed and the import does not prove model quality. | No accepted support-state transition; chapter core remains `argument`. | Clean live replay or archived public Theseus release fixture with environment notes, publication permission, missing-artifact closure, and external review before stronger implementation or generation-mode evidence. |
| `fast-generation-architectures` | direct-support-executed-narrow | Project Theseus generation-mode static import, finite Fast Generation Lean fixture bridge, local Theseus support replay probe, local Fast Generation task bundle, and bounded Theseus public task-bundle import | `docs/theseus_generation_mode_import_slice.md`; `experiments/theseus_generation_mode_import/results/2026-07-01-local.json`; `lean/AsiStackProofs/FastGeneration.lean`; `scripts/validate_theseus_generation_mode_import.py`; `docs/theseus_support_replay_probe.md`; `experiments/theseus_support_replay_probe/results/2026-07-01-local.json`; `scripts/run_theseus_support_replay_probe.py`; `scripts/validate_theseus_support_replay_probe.py`; `docs/fast_generation_task_bundle.md`; `experiments/fast_generation_task_bundle/results/2026-07-02-local.json`; `scripts/validate_fast_generation_task_bundle.py`; `docs/theseus_public_task_bundle_import.md`; `experiments/theseus_public_task_bundle_import/results/2026-07-03-local.json`; `scripts/validate_theseus_public_task_bundle_import.py` | Hard boundary-gate failure, private-payload copying, missing-report-ref overclaim, support-promotion overclaim, raw-speed promotion, useful-speed overclaim, and imported accepted-span speed-lift without useful-solution evidence are rejected; the support replay probe reruns the generation-mode validator as part of the two-validator Theseus support surface; the local Fast Generation task bundle rejects a cheaper latency-only proxy; the bounded Theseus task-bundle import preserves 64 public BigCodeBench metadata-only tasks, 0 public training rows, 0 task-level regressions, residuals, and clean-live-replay non-claim boundaries while preserving that it does not prove model quality. | No chapter core promotion; core claim remains `argument`; no generation-speed or useful-solution-per-second result is claimed. | Clean Theseus replay or archived public task-bundle release fixture with verifier-quality review, fallback execution evidence, serving-memory measurements, and accepted evidence-transition review before stronger Fast Generation evidence. |

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
