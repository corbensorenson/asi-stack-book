# v1.x Active Evidence Cycle

Last updated: 2026-07-09

This ledger names the current v1.x evidence-cycle chapter lanes selected from
`docs/per_chapter_evidence_plan.md`. It exists to enforce the lane cap: this
cycle selects one flagship measured lane plus two direct support lanes and
leaves the other 50 chapter lanes planned-only. It is a planning and
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
| Planned-only chapter lanes | 50 |
| Lane cap | 1 flagship measured lane plus at most 2 direct support lanes per v1.x cycle |
| Flagship measured lane | `resource-economics-and-token-budgets` |
| Direct support lanes | `project-theseus-as-report-first-implementation-reference`; `fast-generation-architectures` |
| Chapter core support effect | None; all 53 chapter core claims remain `argument`. |
| Non-core support effect | Existing non-core transitions remain scoped to their accepted records. |
| No-sweep rule | No 53-lane fixture sweep is claimed or implied. |

## Selected Lanes

| Chapter ID | Status | Strongest current evidence path | Recorded artifact or result | Negative controls or failure cases | Support-state effect | Next blocker |
|---|---|---|---|---|---|---|
| `resource-economics-and-token-budgets` | flagship-executed-narrow | Costed-route/resource-budget synthetic slice, deterministic workflow trace, capacity-smoothing reviewer-capacity trace, local command-replay live probe, accepted local five-sample scoped workflow-trace route-selector transition, broader workload-quality no-promotion record, local synthetic load-stability probe, CI publication cost profile with finite Lean classifier bridge, folded simulation-fidelity contract lane, explicit sublane no-promotion decisions, and aggregate one-command flagship replay with an aggregate Python/Lean invariant plus CI classifier bridge | `docs/costed_route_resource_slice.md`; `experiments/costed_route_resource_slice/results/2026-06-29-local.json`; `lean/AsiStackProofs/ResourceEconomics.lean`; `evidence_transitions/v1_0_measured/costed_route_resource_slice_synthetic_test_backed.json`; `docs/resource_workflow_trace.md`; `experiments/resource_workflow_trace/results/2026-07-01-local.json`; `scripts/validate_resource_workflow_trace.py`; `docs/capacity_smoothing_harness.md`; `experiments/capacity_smoothing/results/2026-07-01-local.md`; `scripts/validate_capacity_smoothing.py`; `docs/resource_live_probe.md`; `experiments/resource_live_probe/results/2026-07-01-local.json`; `scripts/validate_resource_live_probe.py`; `docs/resource_workload_quality_probe.md`; `experiments/resource_workload_quality_probe/results/2026-07-01-local.json`; `scripts/run_resource_workload_quality_probe.py`; `scripts/validate_resource_workload_quality_probe.py`; `evidence_transitions/v1_x_measured/resource_workload_quality_selector_empirical_test_backed.json`; `docs/resource_load_stability_probe.md`; `experiments/resource_load_stability_probe/results/2026-07-01-local.json`; `scripts/run_resource_load_stability_probe.py`; `scripts/validate_resource_load_stability_probe.py`; `docs/resource_ci_cost_profile.md`; `experiments/resource_ci_cost_profile/results/2026-07-04-main.json`; `scripts/validate_resource_ci_cost_profile.py`; `evidence_transitions/v1_x_measured/resource_workflow_trace_no_change.json`; `evidence_transitions/v1_x_measured/resource_live_probe_no_change.json`; `evidence_transitions/v1_x_measured/resource_workload_quality_probe_no_change.json`; `evidence_transitions/v1_x_measured/resource_load_stability_probe_no_change.json`; `evidence_transitions/v1_x_measured/resource_ci_cost_profile_no_change.json`; `schemas/simulation_contract_record.schema.json`; `docs/simulation_transfer_boundary_harness.md`; `experiments/simulation_transfer_boundaries/results/2026-06-30-local.md`; `docs/resource_flagship_lane_run.md`; `experiments/resource_flagship_lane/results/2026-07-01-local.json`; `scripts/run_resource_flagship_lane.py`; `scripts/validate_resource_flagship_lane.py` | Cheaper failed-verification route and cheaper hidden-residual route are rejected; adequate overkill baseline remains eligible; the Lean fixture is checked against public JSON costs, selected route, negative controls, eligibility fields, and the finite selector-state trace theorem `costed_route_fixture_trace_selects_lowest_eligible_route`; the workflow trace rejects latency-only selection, erased displaced costs, over-budget aggregate resource bills, physical-feasibility overclaim, and low-risk work scheduled before protected high-risk review, and its Lean bridge now checks finite dispatch-event rollup, high-risk-first order, guard flags, review minutes, verification minutes, capacity-budget-overrun rejection, and no-promotion boundaries; the capacity-smoothing harness checks 3 valid and 6 expected-invalid toy traces for reviewer-capacity arithmetic, protected-review overhead, displaced-review-cost residualization, low-risk review hoarding, erased protected overhead, over-admission, load-stability overclaim, and no-promotion boundaries, with a finite Lean bridge for the reviewer-capacity trace and negative cases; the resource budget ledger harness checks 6 valid and 7 expected-invalid fixtures for KV-cache/serving-memory accounting separation and throughput-to-quality overclaim rejection; the local live probe replays five Resource Economics validators and checks command-output plus tracked-artifact digests; the accepted local workload selector transition selects a scoped workflow-trace validator over a broader Resource live-probe baseline by five-sample median elapsed time and rejects a cheaper no-op success-text route that exits 0 without running the required validator, while the broader workload-quality no-change record blocks stable-speedup, deployed-scheduler, and production-workload promotion; the local synthetic load-stability probe selects protected capacity smoothing over an admit-arrivals baseline in a finite 10-task workload, residualizes 7 selected deferrals, checks a finite ResourceEconomics Lean bridge, and rejects a cheaper review-erasure route with 3 protected-review violations and hidden deferrals; the CI cost profile records eight actual Pages runs, eight completed runs, five successful completed runs, three classified GitHub Pages deploy-service failures, a 131-second recovery boundary, finite CI failure-classification summary, `resourceCICostProfileFixture`, and publication-duration metrics; folded simulation-transfer fixtures reject missing fidelity, unbounded world transfer, missing resource bills, missing bottleneck residuals, ignored instrumentation, and support-state promotion; the five sublane no-promotion records block promotion for workflow-trace, local-replay, broader workload-quality, broader load-stability, and CI-cost claims unless stronger live or externally reviewed artifacts appear; the aggregate flagship replay reruns 10 validators, checks 26 tracked artifact digests, composes 3 accepted non-core transitions, the no-change chapter-core decision, and 5 sublane no-promotion records, and its Lean fixture `resourceFlagshipLaneAggregateFixture` checks the same finite counts plus preserved negative controls, residuals, non-claims, and no-core-promotion/no-new-transition guards. | Non-core `resource-economics.costed_route_budget_slice` and `resource-economics.finite_burst_load_smoothing_selector` are `synthetic-test-backed`; non-core `resource-economics.scoped_workflow_trace_route_selector` is `empirical-test-backed`; chapter core remains `argument`; workflow-trace, local-replay, broader workload-quality, broader load-stability, and CI-cost sublanes keep accepted `blocks_promotion` no-change records; capacity-smoothing, simulation-transfer, and aggregate flagship artifacts remain non-promoting; none of these artifacts create an upward chapter-core transition. | External or live workload-facing trace beyond the local repository task with real workload quality review, production scheduler logs beyond CI metadata, measured displaced-cost accounting, physical-feasibility review, live or externally reviewed load-stability workload, real KV-cache/serving-memory measurement, and measured rather than fixture-declared simulation outputs. |
| `project-theseus-as-report-first-implementation-reference` | direct-support-executed-narrow | Public-safe Project Theseus static report imports, Fast Generation Lean fixture alignment, local Theseus support replay probe, bounded public task-bundle summary import with explicit no-promotion decision, selected Theseus/Fast support-lane aggregate, bounded non-core artifact-retention, module definition-of-done, project-registry, assistant reference-trace, and accelerator parity manifest imports, plus a work-board metadata import with explicit no-promotion decision | `docs/theseus_report_import_slice.md`; `experiments/theseus_import/results/2026-06-29-local.json`; `scripts/validate_theseus_report.py`; `docs/theseus_generation_mode_import_slice.md`; `experiments/theseus_generation_mode_import/results/2026-07-01-local.json`; `lean/AsiStackProofs/FastGeneration.lean`; `scripts/validate_theseus_generation_mode_import.py`; `docs/theseus_support_replay_probe.md`; `experiments/theseus_support_replay_probe/results/2026-07-01-local.json`; `scripts/run_theseus_support_replay_probe.py`; `scripts/validate_theseus_support_replay_probe.py`; `docs/theseus_public_task_bundle_import.md`; `experiments/theseus_public_task_bundle_import/results/2026-07-03-local.json`; `scripts/validate_theseus_public_task_bundle_import.py`; `evidence_transitions/v1_x_measured/theseus_public_task_bundle_import_no_change.json`; `theseus_public_task_bundle_import_2026_07_03_local`; `docs/theseus_fast_support_lane_run.md`; `experiments/theseus_fast_support_lane/results/2026-07-03-local.json`; `scripts/run_theseus_fast_support_lane.py`; `scripts/validate_theseus_fast_support_lane.py`; `docs/theseus_artifact_retention_replay_import.md`; `docs/theseus_module_definition_of_done_import.md`; `docs/theseus_project_registry_import.md`; `experiments/theseus_project_registry_import/results/2026-07-05-local.json`; `scripts/validate_theseus_project_registry_import.py`; `docs/theseus_assistant_reference_trace_import.md`; `experiments/theseus_assistant_reference_trace_import/results/2026-07-06-local.json`; `scripts/validate_theseus_assistant_reference_trace_import.py`; `evidence_transitions/v1_x_measured/theseus_assistant_reference_trace_import_prototype_backed.json`; `docs/theseus_accelerator_parity_manifest_import.md`; `experiments/theseus_accelerator_parity_manifest_import/results/2026-07-06-local.json`; `scripts/validate_theseus_accelerator_parity_manifest_import.py`; `evidence_transitions/v1_x_measured/theseus_accelerator_parity_manifest_import_prototype_backed.json`; `docs/theseus_work_board_import.md`; `experiments/theseus_work_board_import/results/2026-07-06-local.json`; `scripts/validate_theseus_work_board_import.py`; `evidence_transitions/v1_x_measured/theseus_work_board_import_no_change.json`; `lean/AsiStackProofs/TheseusReference.lean` | Architecture-gate digest mismatch, private-payload copying, and support-promotion overclaim are rejected; generation-mode hard boundary-gate failure, private-payload copying, missing-report-ref overclaim, support-promotion overclaim, raw-speed promotion, and useful-speed overclaim are rejected; the public generation-mode summary is checked against a finite Fast Generation Lean fixture for counts, no-promotion state, all-gates-passed state, zero missing report refs, and no-useful-speed evidence; the support replay probe reruns both validators and checks command-output digests plus tracked artifact hashes; the public task-bundle import checks 64 public BigCodeBench metadata-only tasks, 0 public training rows, 0 task-level regressions, 18 benchmark gates, 19 residuals, visible artifact gaps, seven expected-invalid controls, and the finite TheseusReference bridge while preserving that clean live Theseus replay remains unclaimed and the import does not prove model quality; the accepted no-promotion decision blocks clean-live-replay, model-quality, benchmark-superiority, generation-speed, useful-solution-per-second, support-state, deployment, self-evolution, and chapter-core promotion claims; the selected support-lane aggregate result `theseus-fast-support-lane-2026-07-03-local`, guarded by `python3 scripts/validate_theseus_fast_support_lane.py`, reruns four support validators, checks 16 tracked artifact digests, 68 public task records, 14 expected-invalid or rejected controls, 2 accepted no-promotion decisions, and `theseusFastSupportAggregateFixture`; the project-registry import checks 5,662 registered paths, 24 surfaces, full coverage, 0 unregistered active sources, 0 stale or missing report outputs, 0 generated source artifacts, 0 registry-governance violations, 0 external inference calls, nine expected-invalid controls, and `lean:theseus.reference.project_registry_import.fixture_bridge`; the assistant reference-trace import checks 19 required reference-trace record types, 27/27 gates, 2,203 VIEA view records, 12 selected VCM pages, zero public training rows, zero external inference calls, 11 expected-invalid controls, and `lean:theseus.reference.assistant_reference_trace_import.fixture_bridge`, and it does not prove clean live Project Theseus replay, current runtime state, route quality, private verifier quality, model quality, benchmark superiority, useful-solution-per-second improvement, safety, ASI, or chapter-core promotion; the accelerator parity manifest import checks 7/7 surfaces OK, 7 MLX report summaries, 4 Metal report summaries, 4 artifact manifests, 4 scheduler-canary surfaces, zero hard failures, zero public training rows, zero external inference calls, nine expected-invalid controls, and `lean:theseus.reference.accelerator_parity_manifest_import.fixture_bridge`, and it does not prove full CUDA/MLX/Metal parity, production scheduler routing, model promotion, benchmark performance, model quality, clean live Project Theseus replay, safety, ASI, or chapter-core promotion; the work-board metadata import checks 130 durable task rows, 412 event rows, 133 evidence rows, five SQLite tables, one execution-ledger row, four unattended-improvement rows, 72 feedback rows, a stale-snapshot boundary, zero public training rows, zero external inference calls, ten expected-invalid controls, and `lean:theseus.reference.work_board_import.metadata_boundary`, and it does not prove clean live Project Theseus replay, current board state, current dashboard state, deployment, model quality, unattended safety, self-evolution safety, or chapter-core promotion. | Chapter core remains `argument`; the task-bundle import and work-board metadata import have accepted `blocks_promotion` no-change records; the selected support-lane aggregate has support-state effect `none`; artifact-retention, module definition-of-done, project-registry, assistant reference-trace, and accelerator parity manifest imports have accepted bounded non-core upward transitions only. | Clean live replay or archived public Theseus release fixture with environment notes, publication permission, missing-artifact closure, artifact-truth review, fresh work-board status refresh, governance-tax measurement, accelerator replay/review, and external review before stronger implementation or generation-mode evidence. |
| `fast-generation-architectures` | direct-support-executed-narrow | Project Theseus generation-mode static import, finite Fast Generation Lean fixture bridge, local Theseus support replay probe, local Fast Generation task bundle with explicit no-promotion decision, bounded Theseus public task-bundle import with explicit no-promotion decision, and selected Theseus/Fast support-lane aggregate | `docs/theseus_generation_mode_import_slice.md`; `experiments/theseus_generation_mode_import/results/2026-07-01-local.json`; `lean/AsiStackProofs/FastGeneration.lean`; `scripts/validate_theseus_generation_mode_import.py`; `docs/theseus_support_replay_probe.md`; `experiments/theseus_support_replay_probe/results/2026-07-01-local.json`; `scripts/run_theseus_support_replay_probe.py`; `scripts/validate_theseus_support_replay_probe.py`; `docs/fast_generation_task_bundle.md`; `experiments/fast_generation_task_bundle/results/2026-07-02-local.json`; `scripts/validate_fast_generation_task_bundle.py`; `evidence_transitions/v1_x_measured/fast_generation_task_bundle_no_change.json`; `docs/theseus_public_task_bundle_import.md`; `experiments/theseus_public_task_bundle_import/results/2026-07-03-local.json`; `scripts/validate_theseus_public_task_bundle_import.py`; `evidence_transitions/v1_x_measured/theseus_public_task_bundle_import_no_change.json`; `docs/theseus_fast_support_lane_run.md`; `experiments/theseus_fast_support_lane/results/2026-07-03-local.json`; `scripts/run_theseus_fast_support_lane.py`; `scripts/validate_theseus_fast_support_lane.py` | Hard boundary-gate failure, private-payload copying, missing-report-ref overclaim, support-promotion overclaim, raw-speed promotion, useful-speed overclaim, and imported accepted-span speed-lift without useful-solution evidence are rejected; the support replay probe reruns the generation-mode validator as part of the two-validator Theseus support surface; the local Fast Generation task bundle rejects a cheaper latency-only proxy, and the accepted no-promotion decision blocks model-speed, useful-solution-per-second model performance, serving-throughput, route-selector adequacy, benchmark, model-quality, deployed-routing, and chapter-core promotion claims; the bounded Theseus task-bundle import preserves 64 public BigCodeBench metadata-only tasks, 0 public training rows, 0 task-level regressions, residuals, and clean-live-replay non-claim boundaries while preserving that it does not prove model quality; its accepted no-promotion decision separately blocks clean-live-replay, model-quality, benchmark-superiority, generation-speed, useful-solution-per-second, support-state, and chapter-core promotion claims; the selected support-lane aggregate result `theseus-fast-support-lane-2026-07-03-local`, guarded by `python3 scripts/validate_theseus_fast_support_lane.py`, reruns four support validators, checks 16 tracked artifact digests, 68 public task records, 14 expected-invalid or rejected controls, 2 accepted no-promotion decisions, and `theseusFastSupportAggregateFixture`, and does not prove clean live Project Theseus replay, does not prove model quality, does not promote any chapter core claim, and does not create support-state promotion. | No chapter core promotion; core claim remains `argument`; the Fast Generation task-bundle no-promotion decision keeps broader Fast Generation claims at `argument`; the Theseus public task-bundle decision keeps the imported implementation-reference summary at `argument`; the selected support-lane aggregate has support-state effect `none`; no generation-speed or useful-solution-per-second result is claimed. | Clean Theseus replay or archived public task-bundle release fixture with verifier-quality review, fallback execution evidence, serving-memory measurements, and accepted evidence-transition review before stronger Fast Generation evidence. |

## Planned-Only Lanes

These chapter lanes stay planned-only for this cycle. They keep their evidence
paths in `docs/per_chapter_evidence_plan.md`, but no chapter-lane completion,
chapter-core fixture sweep, support-state pressure, or release claim is created
for them here. A selected-lane import may name a planned-only chapter as a
connected boundary, but that does not make the planned-only chapter selected or
move its support state.

Implementation note: the Project Theseus selected lane also carries the
book-to-Theseus crosswalk import recorded in
`docs/theseus_book_crosswalk_import.md`,
`experiments/theseus_book_crosswalk_import/results/2026-07-05-local.json`,
`scripts/validate_theseus_book_crosswalk_import.py`, and
`evidence_transitions/v1_x_measured/theseus_book_crosswalk_import_no_change.json`.
It records 53 public-safe pointer rows, 20 backlog cards, 134 source-sync
review decisions, and ten expected-invalid controls. It is pointer-only
implementation-reference evidence: it does not prove clean live Project
Theseus replay, artifact truth for referenced rows, model quality, deployment,
self-evolution safety, support-state promotion, or chapter-core promotion.

Implementation note: the evidence ladder now records 14 narrow non-core upward transitions.
The Project Theseus selected lane includes the bounded assistant
reference-trace import recorded in
`docs/theseus_assistant_reference_trace_import.md`, validated by
`python3 scripts/validate_theseus_assistant_reference_trace_import.py`, and
bridged by `lean:theseus.reference.assistant_reference_trace_import.fixture_bridge`.
It packages one sanitized runtime trace skeleton, not a clean live Project
Theseus replay, current runtime-state proof, route-quality result, model-quality
result, benchmark-superiority result, support-state promotion, or chapter-core
promotion.

- `asi-is-a-stack-not-a-model`
- `the-efficient-asi-hypothesis`
- `system-boundaries-and-authority`
- `failure-modes-of-ungoverned-intelligence`
- `evidence-states-and-claim-discipline`
- `scalable-oversight-and-adversarial-ai-control`
- `human-intent-as-a-formal-input`
- `constitutional-alignment-substrate`
- `moral-uncertainty-and-value-conflict`
- `stable-capability-fields`
- `capability-replacement-and-rollback`
- `security-kernel-and-digital-scifs`
- `model-weight-custody-and-hardware-roots-of-trust`
- `ai-supply-chain-integrity-and-lifecycle-provenance`
- `recursive-self-improvement-boundaries`
- `open-ended-improvement-engines`
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
- `governed-deliberation-and-test-time-scaling`
- `rankfold-neuralfold-and-artifact-compression`
- `mathematical-and-search-substrates`
- `circle-calculus-and-proof-carrying-ai-contracts`
- `coil-attention-cyclic-memory-and-recurrence-contracts`
- `coilra-multicoil-rope-and-cyclic-mixers`
- `executable-specifications-and-lean-proof-envelope`
- `benchmark-ratchets-and-anti-goodhart-evidence`
- `capability-thresholds-and-deployment-commitments`
- `adversarial-evaluation-sandbagging-and-training-time-deception`
- `safety-cases-and-structured-assurance`
- `policy-optimization-and-learning-from-feedback`
- `data-engines-continual-learning-and-unlearning`
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
