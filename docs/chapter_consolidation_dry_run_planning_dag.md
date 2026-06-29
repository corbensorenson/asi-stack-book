# Chapter Consolidation Dry Run: Planning And DAG Control

Last updated: 2026-06-29

This is a non-pilot dry-run package required by
`docs/v1_x_beyond_sota_roadmap.md` and
`docs/chapter_consolidation_sequence.md`. It is a review artifact only. It
does not edit `book_structure.json`, delete a chapter, change a URL, rewrite a
chapter, change source mappings, change proof targets, change support states,
or approve a reader artifact.

Dry-run destination:
`planning-as-a-control-layer`, retitled **Planning as a Control Layer: DAGs
and Intelligence Arbitrage**.

Source chapters:

- `planning-as-a-control-layer`
- `planforge-dags-and-intelligence-arbitrage`

Related chapter not merged by this package:

- `cognitive-compilation-and-semantic-ir`

Continuity decision:

- Keep `planning-as-a-control-layer` as the public continuity ID if this merge
  later proceeds, because it already owns the general control-plane boundary:
  accepted command contracts become governed plans without the planner owning
  memory, reasoning, execution authority, or side effects.
- Treat `planforge-dags-and-intelligence-arbitrage` as a folded source chapter
  whose DAG scheduling, dependency order, capability-tier annotations,
  adequacy contracts, cost/quality ledger, escalation/residual behavior, proof
  hooks, tests, source mappings, and reader path become named sections,
  subclaims, and history records in the destination chapter.
- Keep `cognitive-compilation-and-semantic-ir` standalone. It owns semantic
  atoms, IR validity, lowering receipts, target artifact refs, repair-ledger
  refs, and obligation-preserving compilation. The planning/DAG chapter may
  hand work to semantic IR, but it should not absorb the compiler artifact.

## Non-Actions

- No manifest edit has been made.
- No chapter file has been removed or rewritten.
- No source note, external source, proof target, test result, or support state
  has changed.
- No support state changes are made or implied.
- No claim is promoted above `argument`.
- No external comparator is treated as proving ASI Stack planner quality,
  scheduler correctness, decomposition accuracy, route adequacy, model
  selection quality, runtime replanning, tool execution, or deployment behavior.
- No reader, EPUB, DOCX, PDF, or audio artifact is approved by this package.
- No new result is created by this dry run.

## Proposed `book_structure.json` Diff

This proposed `book_structure.json` diff is illustrative and unapplied. If the
merge is later executed, apply one cluster merge in one commit, then regenerate
and validate every generated surface.

```diff
@@ Part II - Planning, Memory, Reasoning, and Execution
 {
   "id": "planning-as-a-control-layer",
-  "title": "Planning as a Control Layer",
+  "title": "Planning as a Control Layer: DAGs and Intelligence Arbitrage",
   "file": "chapters/planning-as-a-control-layer.qmd",
   "status": "conceptual",
   "evidence_level": "argument",
   "claim_label": "Design rationale",
   "source_ids": [
     "planforge",
     "viea",
     "cognitive_compilation",
     "software_magic_grimoire",
-    "moecot"
+    "moecot",
+    "planforge_compiler_arch",
+    "coherence_exchange",
+    "tokenmana"
   ],
-  "problem": "Goals need to become governed plans with dependencies, budgets, risk limits, tool choices, and stopping conditions.",
-  "insufficient": "Planning cannot be collapsed into memory, reasoning, or execution because each layer has different authority and failure modes.",
-  "core_claim": "Planning is a separate control layer that converts accepted goals into governed action without owning memory, reasoning, or side effects.",
-  "minimal_implementation": "A plan graph format with assumptions, task graph, dependencies, context and tool requirements, authority requirements, budgets, verification plan, replanning policy, stop conditions, and failure behavior.",
-  "beyond_state_of_art": "The mature version is a live control plane for work..."
+  "problem": "Accepted goals need governed plan graphs whose dependencies, authority requirements, context demands, capability tiers, budgets, adequacy contracts, verification burdens, stop conditions, dispatch receipts, escalation paths, and residuals remain inspectable before execution.",
+  "insufficient": "Planning cannot be collapsed into prompting, memory, reasoning, routing, or execution because a plausible plan graph can still hide authority overreach, cyclic dependencies, inadequate context, missing verification, unsafe dispatch, bad tier selection, or displaced human-review cost.",
+  "core_claim": "Planning should be a separate control layer that turns accepted command contracts into schedulable DAGs with explicit dependencies, authority ceilings, context demands, capability-tier assignments, adequacy contracts, verification burdens, cost/quality ledgers, escalation routes, and residuals.",
+  "minimal_implementation": "A plan graph and PlanForge DAG fixture suite validated by the plan-execution contract harness, covering lifecycle state, dependency order, dispatch receipts, authority requirements, capability tiers, adequacy contracts, cost-quality ledgers, residuals, and expected-invalid cycle, requirement-loss, approval-bypass, and unreceipted-dispatch cases.",
+  "beyond_state_of_art": "A mature planning control plane is a governed scheduler for cognitive work: it decomposes accepted contracts into DAGs, assigns the minimum adequate capability and verification burden to each node, blocks unsafe dispatch, counts repair and residual costs, and hands validated semantic obligations to compiler, context, routing, execution, and evidence layers without owning their authority."
 }
-
-{
-  "id": "planforge-dags-and-intelligence-arbitrage",
-  "title": "PlanForge DAGs and Intelligence Arbitrage",
-  "file": "chapters/planforge-dags-and-intelligence-arbitrage.qmd",
-  ...
-}
```

Manifest notes:

- The proposed Corben/local `source_ids` union is `planforge`, `viea`,
  `cognitive_compilation`, `software_magic_grimoire`, `moecot`,
  `planforge_compiler_arch`, `coherence_exchange`, and `tokenmana`.
- If the merge proceeds, remove only the
  `planforge-dags-and-intelligence-arbitrage` chapter object after all claim,
  source, proof, reader, handoff, URL, and validation steps pass.
- Do not fold `cognitive-compilation-and-semantic-ir` into this destination.
  Semantic IR owns the intermediate representation and lowering receipts that
  compile plans into target artifacts; it is not just another plan-graph field.
- Run `python3 scripts/chapter_adjacency_report.py --if-removing
  planforge-dags-and-intelligence-arbitrage` before editing the manifest.

## Destination Section Outline

The merged chapter should use one chapter skeleton, not two pasted skeletons.

Recommended section sequence:

1. Chapter status: one status block with merged evidence gaps.
2. Drafting guardrail: plan graphs and DAG schemas are not deployed planner
   quality, scheduler correctness, model-routing adequacy, runtime replanning,
   or tool-execution evidence.
3. Human Reading Path: start from the reader question, "When does a request
   become an executable plan, and when should the plan refuse to dispatch?"
4. Problem: accepted command contracts need plan graphs with dependencies,
   context, authority, capability tiers, budgets, adequacy contracts,
   verification burdens, stop conditions, dispatch receipts, and residuals.
5. Why existing approaches are insufficient: prompt plans, chain-of-thought
   outlines, and uniform model routing can hide cycles, missing context,
   authority gaps, budget exhaustion, inadequate verification, or wrong-tier
   model choices.
6. Core Claim: use the merged core claim above.
7. Claim-source mapping status: one table that separates control-layer lineage
   from PlanForge DAG/intelligence-arbitrage lineage and keeps all support at
   `argument`.
8. Mechanism:
   - accepted command contract intake;
   - plan node lifecycle states;
   - dependency DAG and acyclicity;
   - context/tool/worker requirements;
   - authority ceiling and side-effect boundary;
   - capability tier and intelligence-arbitrage assignment;
   - adequacy contract and verification plan;
   - cost/quality ledger, repair cost, residuals, and human-review cost;
   - dispatch receipts and typed-job lowering;
   - replanning deltas, stop conditions, and blocked states;
   - no-claim boundaries for planner quality, scheduler performance, and
     runtime behavior.
9. Interfaces:
   - command contracts supply accepted work and authority ceiling;
   - VCM supplies context packets;
   - routing consumes capability annotations;
   - cognitive compilation receives semantic obligations for IR lowering;
   - Labor OS receives only dispatchable typed jobs;
   - evidence ledgers record cost, quality, verification, and residual results.
10. Invariants:
    - plan nodes inherit or lower parent authority ceilings;
    - unsatisfied required constraints block dispatch;
    - dispatchable DAGs are acyclic and dependency ordered;
    - failed quality predicates escalate or emit residuals;
    - candidate, blocked, and review-only nodes do not imply execution
      permission;
    - cheap routes do not count as adequate until verification and downstream
      utility are counted.
11. Failure modes:
    - scope creep;
    - planning without replanning;
    - dependency cycles;
    - dispatch laundering;
    - wrong capability tier;
    - economic optimization overriding safety;
    - replanning erasure;
    - hidden human-review or repair burden.
12. Minimum Viable Implementation: combine
    `schemas/plan_graph.schema.json`, `schemas/planforge_dag.schema.json`,
    `schemas/command_contract.schema.json`, `schemas/hive_job_contract.schema.json`,
    and `python3 scripts/validate_plan_execution_contracts.py`. The MVI should
    preserve the valid dispatchable and blocked-authority cases plus
    expected-invalid cycle, contract-mismatch, lost-requirement,
    dispatch-without-receipt, and approval-bypass cases.
13. Beyond the State of the Art: describe a governed scheduler and capacity
    allocator that decomposes accepted contracts into DAGs, assigns minimum
    adequate capability tiers, preserves authority and adequacy contracts,
    blocks unsafe dispatch, counts repair/residual/human-review costs, and
    hands obligations to semantic IR. Preserve the claim boundary that this is
    an architectural endpoint, not a demonstrated deployed scheduler.
14. Codex test plan: union decomposition, dependency ordering, context-demand,
    runtime replanning, DAG acyclicity, tier assignment, escalation trigger,
    dispatch-state, and replanning-delta tests.
15. Formalization hooks: keep both Lean modules and all four proof tags.
16. Source crosswalk: union Corben/local sources and external comparators.
17. Repetition-removal ledger: collapse two repeated planning/DAG skeletons
    into one control-plane chapter; reinvest space in authority-preserving
    scheduling, adequacy contracts, and cost/quality residual accounting.
18. Summary: one synthesis of planning control, PlanForge DAG scheduling,
    intelligence arbitrage, dispatch receipts, residuals, and handoff to
    semantic IR and typed execution.
19. Handoff: route directly to `cognitive-compilation-and-semantic-ir`, because
    semantic IR turns accepted plan obligations into target artifacts and
    lowering receipts.

## Appendix C Row Plan

Proposed merged core row:

| Row | Chapter | Claim label | Support state | Source effect |
|---|---|---|---|---|
| `planning-as-a-control-layer.core` | `planning-as-a-control-layer` | Design rationale | argument | Union the source mappings from both source chapters; keep limits and passage-review notes. |

Proposed merged core claim:

> Planning should be a separate control layer that turns accepted command
> contracts into schedulable DAGs with explicit dependencies, authority
> ceilings, context demands, capability-tier assignments, adequacy contracts,
> verification burdens, cost/quality ledgers, escalation routes, and residuals.

Claim-history treatment for folded and protected chapters:

| Existing row | Proposed disposition | Required preservation |
|---|---|---|
| `planforge-dags-and-intelligence-arbitrage.core` | Redirect to destination as a subclaim about DAG scheduling, dependency ordering, capability tiers, intelligence arbitrage, adequacy contracts, cost-quality ledgers, escalation, and residuals. | Preserve claim text in history, proof tags, source mappings, fixture/test rows, and no-promotion limits. |
| `cognitive-compilation-and-semantic-ir.core` | No merge in this package. | Keep semantic atoms, obligation-preserving IR, lowering receipts, target artifacts, repair-ledger refs, and compiler proof tags standalone. |

No support state changes are authorized. All core and subclaim rows remain
`argument` unless a separate evidence-transition record later justifies a
change.

## Source Union

Corben/local source union:

- `planforge`
- `viea`
- `cognitive_compilation`
- `software_magic_grimoire`
- `moecot`
- `planforge_compiler_arch`
- `coherence_exchange`
- `tokenmana`

External-source union:

- `ext_autogen_2023`
- `ext_behavior_trees_robotics_ai_2017`
- `ext_integrated_tamp_2020`
- `ext_pddl_1998`
- `ext_react_2022`
- `ext_shop2_2003`
- `ext_three_states_plan_fear_2006`
- `ext_tla_plus_home_docs`
- `ext_tree_of_thoughts_2023`

Adjacent external comparator retained by `cognitive-compilation-and-semantic-ir`:

- `ext_dreamcoder_2020`

These external records remain comparators and positioning sources. They do not
prove ASI Stack planner quality, scheduler correctness, route adequacy,
runtime replanning, or deployment behavior.

## Lean Module And Proof-Manifest Treatment

Keep these modules:

- `AsiStackProofs.Planning`
- `AsiStackProofs.PlanForge`

Keep these proof tags:

- `lean:planning.control_layer.operational_invariant`
- `lean:planning.control_layer.failure_blocks_promotion`
- `lean:planforge.dag.operational_invariant`
- `lean:planforge.dag.failure_blocks_promotion`

Do not move or retire the adjacent semantic-IR module or proof tags:

- `AsiStackProofs.CognitiveCompilation`
- `lean:cognitive_compilation.ir.operational_invariant`
- `lean:cognitive_compilation.ir.failure_blocks_promotion`

If the merge proceeds, `proofs/proof_manifest.json` should continue to record
both destination proof families. The folded source chapter ID may become a
historical source for proof lineage only after the outline and proof manifest
are updated deliberately.

## Tests, Schemas, And Fixtures

Preserve these schema and harness surfaces:

- `schemas/plan_graph.schema.json`
- `schemas/planforge_dag.schema.json`
- `schemas/command_contract.schema.json`
- `schemas/hive_job_contract.schema.json`
- `schemas/semantic_atom.schema.json`
- `experiments/plan_execution_contracts/fixtures/valid_dispatchable_linear_plan.json`
- `experiments/plan_execution_contracts/fixtures/valid_blocked_authority_plan.json`
- `experiments/plan_execution_contracts/fixtures/invalid_cycle_in_dag.json`
- `experiments/plan_execution_contracts/fixtures/invalid_contract_mismatch.json`
- `experiments/plan_execution_contracts/fixtures/invalid_requirement_lost.json`
- `experiments/plan_execution_contracts/fixtures/invalid_dispatch_without_receipt.json`
- `experiments/plan_execution_contracts/fixtures/invalid_approval_bypass.json`
- `python3 scripts/validate_plan_execution_contracts.py`

The harness result remains the existing synthetic plan-execution contract
gate. This package does not create a new test result, deployed planner
evidence, scheduler conformance result, tier-routing benchmark, context-demand
prediction result, runtime-replanning trace, tool-execution trace, or model
behavior result.

## Reader Path, Handoff, And Review Repairs

If the merge is executed later:

- Rewrite the destination Human Reading Path to explain why plans are governed
  control artifacts, not permission to execute.
- Remove the separate `planforge-dags-and-intelligence-arbitrage`
  reader-review row only after preserving its reader path as a subsection or
  history note in the destination row.
- Update the predecessor handoff from
  `command-contracts-and-semantic-interfaces` or the accepted command-contract
  destination if that earlier merge executes.
- Update the destination handoff so it points directly to
  `cognitive-compilation-and-semantic-ir`.
- Preserve a local explanation that semantic IR remains the protected compiler
  and lowering chapter.
- Update reader overlays and curated-reader matrices only after the manifest
  merge is accepted.

## Repetition-Removal Ledger

Repeated skeleton load removed:

- Two separate Problem sections about turning goals into structured work become
  one problem about governed plan graphs.
- Two Insufficiency sections about planning and uniform model routing become
  one insufficiency section about plans that hide authority, context,
  verification, cost, and dispatch risks.
- Two Mechanism sections become one control-plane mechanism with lifecycle
  states, dependency DAGs, capability tiers, adequacy contracts,
  verification burdens, cost/quality ledgers, dispatch receipts, and residuals.
- Two MVI sections become one fixture/harness story over the existing
  plan-graph and PlanForge DAG schemas.

Saved-space reinvestment:

- Deeper explanation of dispatchable versus blocked plan states.
- Clearer authority-preserving replanning and stop-condition handling.
- Clearer capability-tier assignment as adequacy-plus-verification accounting,
  not just cost minimization.
- Stronger no-claim language around deployed planner quality and scheduler
  performance.

Reader-work disposition:

- Pause curated-reader graduation for the planning/DAG pair until this package
  is reviewed and the merge is executed, explicitly deferred, or
  rejected/retained.
- Local prose cleanup may continue if it does not entrench duplicate chapter
  skeletons.
- Reader curation may continue for `cognitive-compilation-and-semantic-ir`,
  because this package protects that chapter boundary.

## Validation If Executed Later

If a future review accepts the merge, the execution commit should run at least:

```bash
python3 scripts/chapter_adjacency_report.py --if-removing planforge-dags-and-intelligence-arbitrage
python3 scripts/sync_scaffold.py
python3 scripts/sync_proof_manifest.py
python3 scripts/validate_source_evidence_audit.py
python3 scripts/validate_source_appendices.py
python3 scripts/validate_outline_consistency.py
python3 scripts/validate_implementation_horizons.py
python3 scripts/validate_reader_spine.py --check
python3 scripts/validate_book.py
python3 scripts/validate_schemas.py
python3 scripts/validate_protocol_examples.py
python3 scripts/validate_plan_execution_contracts.py
(cd lean && lake build)
LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 quarto render --to html
node scripts/validate_live_human_view_browser.js --all-chapters --all-viewports
```

## Review Questions

- Does the destination preserve a clearer artifact boundary than the current
  two-chapter split?
- Does PlanForge DAG scheduling become stronger as a concrete lane inside the
  planning control layer, or does it still deserve standalone chapter
  ownership?
- Is `planning-as-a-control-layer` the right continuity ID, or should the
  URL/title policy preserve both public pages more visibly?
- Is the semantic IR chapter protected strongly enough?
- Does the one-skeleton draft reduce reader repetition without hiding proof,
  source, or test limits?

## Non-Claims

- This dry run does not merge chapters.
- This dry run does not change `book_structure.json`.
- This dry run does not change Appendix C support states.
- This dry run does not create a source-derived, external-literature-backed,
  proof-derived, prototype-backed, synthetic-test-backed, or empirical support
  transition.
- This dry run does not prove planner quality, scheduler correctness,
  decomposition accuracy, model-routing adequacy, runtime replanning,
  tool-execution behavior, deployed runtime behavior, or ASI capability.
