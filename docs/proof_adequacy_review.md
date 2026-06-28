# Proof Adequacy Review

Last updated: 2026-06-28

This review classifies the 112 implemented Lean proof targets by adequacy for the claims they are attached to. It does not change any support state and does not claim broad system correctness.

## Summary

| Adequacy class | Targets | Meaning |
|---|---:|---|
| adequate finite-record invariant | 8 | The current Lean predicate is adequate for a narrow repository/process or finite-record claim if the claim text remains narrow. |
| useful but too narrow | 27 | The predicate is a useful guard, but the chapter needs state-machine, trace, or integration tests before the proof can support the larger boundary. |
| needs richer state-machine or review semantics | 20 | The current finite record omits timing, lifecycle, review, social, adversarial, or governance semantics that are central to the chapter. |
| needs executable tests first | 41 | Behavior, replay, routing, context, tool-use, memory, or artifact mechanics need deterministic harnesses before stronger proof work is meaningful. |
| needs empirical or baseline tests first | 10 | Performance, efficiency, policy, substrate, or quality claims need workloads, baselines, measurements, and negative controls before proof adequacy can rise. |
| research-agenda until artifact import | 6 | The proof target remains a placeholder guard until external/local project artifacts are imported, built, replayed, or otherwise inspected. |

All 112 targets still build as narrow finite-record predicates. The review changes the project backlog, not the theorem status.

## Review Rules

- Lean build success means the checked finite predicates compile.
- A finite predicate is not automatically an adequate formalization of the chapter boundary.
- Proof adequacy cannot promote a claim unless the claim is scoped to what the proof actually checks.
- Schemas validate record shape, tests validate behavior, benchmarks validate measured claims, and source notes support drafting context. These lanes remain separate.
- `proofs/proof_triage.json` remains unchanged in this pass because it records routing into Lean, not adequacy of the resulting formalization.

## Chapter-Level Target Classification

| Chapter | Targets | Adequacy class | Next action |
|---|---:|---|---|
| `asi-is-a-stack-not-a-model` | 2 | useful but too narrow | Retain as finite guard; add state-machine or trace tests. |
| `the-efficient-asi-hypothesis` | 2 | needs empirical or baseline tests first | Build workload, baseline, and result record before stronger proof. |
| `system-boundaries-and-authority` | 2 | useful but too narrow | Record-aware authority decision envelope added; still add runtime, revocation, confused-deputy, and deployment trace tests. |
| `failure-modes-of-ungoverned-intelligence` | 2 | needs richer state-machine or review semantics | Model lifecycle, review, timing, and adversarial states before adequacy. |
| `evidence-states-and-claim-discipline` | 2 | adequate finite-record invariant | Keep narrow; do not broaden beyond checked records. |
| `human-intent-as-a-formal-input` | 2 | useful but too narrow | Retain as finite guard; add state-machine or trace tests. |
| `constitutional-alignment-substrate` | 2 | needs richer state-machine or review semantics | Model lifecycle, review, timing, and adversarial states before adequacy. |
| `agency-dignity-and-corrigibility` | 2 | needs richer state-machine or review semantics | Model lifecycle, review, timing, and adversarial states before adequacy. |
| `moral-uncertainty-and-value-conflict` | 2 | needs richer state-machine or review semantics | Model lifecycle, review, timing, and adversarial states before adequacy. |
| `governance-rights-fork-exit-and-audit` | 2 | needs richer state-machine or review semantics | Model lifecycle, review, timing, and adversarial states before adequacy. |
| `stable-capability-fields` | 2 | useful but too narrow | Retain as finite guard; add state-machine or trace tests. |
| `capability-replacement-and-rollback` | 2 | useful but too narrow | Retain as finite guard; add state-machine or trace tests. |
| `security-kernel-and-digital-scifs` | 2 | useful but too narrow | Retain as finite guard; add state-machine or trace tests. |
| `recursive-self-improvement-boundaries` | 2 | needs richer state-machine or review semantics | Model lifecycle, review, timing, and adversarial states before adequacy. |
| `intent-to-execution-contracts` | 2 | useful but too narrow | Retain as finite guard; add state-machine or trace tests. |
| `command-contracts-and-semantic-interfaces` | 2 | useful but too narrow | Retain as finite guard; add state-machine or trace tests. |
| `planning-as-a-control-layer` | 2 | useful but too narrow | Plan-control record envelope added; still add decomposition, context-demand, runtime replanning, and planner-quality tests. |
| `planforge-dags-and-intelligence-arbitrage` | 2 | needs executable tests first | Add deterministic fixtures/harnesses before stronger formalization. |
| `cognitive-compilation-and-semantic-ir` | 2 | needs executable tests first | Add deterministic fixtures/harnesses before stronger formalization. |
| `virtual-context-abi` | 2 | needs executable tests first | Add deterministic fixtures/harnesses before stronger formalization. |
| `semantic-pages-context-cells-and-certificates` | 2 | needs executable tests first | Add deterministic fixtures/harnesses before stronger formalization. |
| `context-transactions-snapshots-mounts-and-taint` | 2 | useful but too narrow | Retain as finite guard; add state-machine or trace tests. |
| `verification-bandwidth-and-context-adequacy` | 2 | needs executable tests first | Add deterministic fixtures/harnesses before stronger formalization. |
| `claim-ledgers-and-belief-revision` | 2 | useful but too narrow | Retain as finite guard; add state-machine or trace tests. |
| `spinoza-verification-and-proof-carrying-claims` | 2 | useful but too narrow | Retain as finite guard; add state-machine or trace tests. |
| `unified-adaptive-tribunal-and-adversarial-review` | 2 | needs richer state-machine or review semantics | Model lifecycle, review, timing, and adversarial states before adequacy. |
| `labor-os-and-typed-jobs` | 2 | needs executable tests first | Add deterministic fixtures/harnesses before stronger formalization. |
| `artifact-graphs-audit-logs-and-replay` | 2 | needs executable tests first | Add deterministic fixtures/harnesses before stronger formalization. |
| `runtime-adapters-tool-permissions-and-human-approval` | 2 | needs executable tests first | Add deterministic fixtures/harnesses before stronger formalization. |
| `procedural-memory-and-cognitive-loop-closure` | 2 | needs executable tests first | Add deterministic fixtures/harnesses before stronger formalization. |
| `routing-heads-and-specialist-cores` | 2 | needs executable tests first | Add deterministic fixtures/harnesses before stronger formalization. |
| `readiness-gates-residual-escrow-and-quarantine` | 2 | useful but too narrow | Retain as finite guard; add state-machine or trace tests. |
| `moecot-runtime-and-multi-core-orchestration` | 2 | research-agenda until artifact import | Import/replay artifacts before adequacy can rise. |
| `personal-compute-hives-and-federated-edge-intelligence` | 4 | needs executable tests first | Add deterministic fixtures/harnesses before stronger formalization. |
| `compact-generative-systems-and-residual-honesty` | 2 | needs executable tests first | Add deterministic fixtures/harnesses before stronger formalization. |
| `generate-verify-repair-compression` | 2 | needs executable tests first | Add deterministic fixtures/harnesses before stronger formalization. |
| `fast-generation-architectures` | 2 | needs empirical or baseline tests first | Build workload, baseline, and result record before stronger proof. |
| `rankfold-neuralfold-and-artifact-compression` | 2 | needs executable tests first | Add deterministic fixtures/harnesses before stronger formalization. |
| `semantic-representation-and-tree-structured-models` | 2 | needs executable tests first | Add deterministic fixtures/harnesses before stronger formalization. |
| `resource-economics-and-token-budgets` | 2 | needs executable tests first | Add deterministic fixtures/harnesses before stronger formalization. |
| `simulation-fidelity-and-physical-constraints` | 2 | needs richer state-machine or review semantics | Model lifecycle, review, timing, and adversarial states before adequacy. |
| `mathematical-and-search-substrates` | 2 | needs empirical or baseline tests first | Build workload, baseline, and result record before stronger proof. |
| `circle-calculus-and-proof-carrying-ai-contracts` | 2 | research-agenda until artifact import | Import/replay artifacts before adequacy can rise. |
| `coil-attention-cyclic-memory-and-recurrence-contracts` | 2 | needs executable tests first | Add deterministic fixtures/harnesses before stronger formalization. |
| `coilra-multicoil-rope-and-cyclic-mixers` | 2 | needs empirical or baseline tests first | Build workload, baseline, and result record before stronger proof. |
| `executable-specifications-and-lean-proof-envelope` | 2 | adequate finite-record invariant | Keep narrow; do not broaden beyond checked records. |
| `benchmark-ratchets-and-anti-goodhart-evidence` | 2 | needs executable tests first | Add deterministic fixtures/harnesses before stronger formalization. |
| `policy-optimization-and-learning-from-feedback` | 2 | needs empirical or baseline tests first | Build workload, baseline, and result record before stronger proof. |
| `artifact-steward-agents-and-living-project-governance` | 4 | needs richer state-machine or review semantics | Model lifecycle, review, timing, and adversarial states before adequacy. |
| `integrated-reference-architecture` | 2 | needs executable tests first | Add deterministic fixtures/harnesses before stronger formalization. |
| `project-theseus-as-report-first-implementation-reference` | 2 | research-agenda until artifact import | Import/replay artifacts before adequacy can rise. |
| `prototype-roadmap` | 2 | useful but too narrow | Retain as finite guard; add state-machine or trace tests. |
| `living-book-methodology` | 2 | adequate finite-record invariant | Keep narrow; do not broaden beyond checked records. |
| `open-research-agenda-and-bibliography-plan` | 2 | adequate finite-record invariant | Keep narrow; do not broaden beyond checked records. |

## Follow-Through Increments

### Authority Decision Envelope

The first follow-through increment strengthened `AsiStackProofs.Authority` beyond the initial ceiling and missing-grant predicates. The module now includes a finite `AuthorityDecisionRecord` and `AuthorityDecisionValid` predicate for modeled allow, deny, and escalate records. The new theorems check that valid modeled decisions retain audit and non-claim fields; allowed decisions carry effect receipts and do not exceed caller or active ceilings; denied decisions carry no effect receipt; and escalation routes to review. The predicate also requires allowed decisions to reject expired or revoked grants.

This keeps the `system-boundaries-and-authority` proof cluster in the `useful but too narrow` class. The predicate is closer to the synthetic authority harness, but it still does not prove runtime adapter enforcement, deployed permission checks, revocation propagation, confused-deputy resistance in a live tool wrapper, or source interpretation adequacy.

### Planning Control Record Envelope

The second follow-through increment strengthened `AsiStackProofs.Planning` beyond the initial authority-inheritance and unsatisfied-constraint predicates. The module now includes a finite `PlanDispatchState`, `PlanControlRecord`, `PlanAuthorityWithinParent`, and `PlanControlRecordValid` envelope for modeled dispatchable, blocked, and replanned records. The new theorems check that valid modeled dispatchable plans expose command validation, satisfied constraints, stop conditions, context requirements, verification planning, dispatch receipts, absence of blocked nodes, and parent-authority preservation; that blocked modeled plans have no dispatch receipt; that replanned modeled plans preserve authority, stop conditions, and residual bookkeeping; and that valid records retain non-claim presence.

This moves `planning-as-a-control-layer` from `needs executable tests first` to `useful but too narrow`. The predicate is now closer to the synthetic plan-execution harness, but it remains a finite-record formalization. It still does not establish planner quality, decomposition accuracy, graph completeness, context-demand prediction, route choice, scheduler behavior, deployed execution, or runtime replanning behavior.

## Result

The proof envelope is traceable and useful, but most targets should not be treated as adequate formalizations of their full chapter boundaries yet. The highest-leverage next steps are deterministic behavior harnesses for execution/context/routing/compression chapters, empirical baselines for efficiency/generation/substrate chapters, and richer lifecycle or review models for governance and agency chapters. Authority and Planning now have stronger finite-record envelopes, but neither increment moves a chapter support state.

No Appendix C support state changes were made.
