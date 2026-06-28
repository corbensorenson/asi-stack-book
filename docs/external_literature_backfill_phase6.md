# Phase 6 External Literature Backfill

Last updated: 2026-06-28

This document records the initial Phase 6 external-literature backfill passes.
The current pass covers alignment/control, AI governance/evaluation,
planning/agent control, retrieval/context, formal methods, routing/MoE,
compression/representation, and benchmark science. It does not claim complete
literature coverage.

## Added Records

| Source ID | Area | Primary role |
|---|---|---|
| `ext_concrete_ai_safety_2016` | alignment/control | Practical accident-risk taxonomy: side effects, reward hacking, scalable oversight, safe exploration, and distributional shift. |
| `ext_corrigibility_2015` | alignment/control | Corrigibility, shutdown tolerance, operator correction, and intervention-channel preservation. |
| `ext_off_switch_game_2016` | alignment/control | Shutdown incentives and uncertainty about human objectives. |
| `ext_optimal_policies_power_2019` | alignment/control | Power-seeking and option-preservation pressure. |
| `ext_model_evaluation_extreme_risks_2023` | governance/evals | Dangerous-capability and alignment evaluations for extreme-risk decisions. |
| `ext_frontier_ai_regulation_2023` | governance/evals | Frontier AI governance, pre-deployment risk assessment, external scrutiny, and post-deployment monitoring. |
| `ext_nist_ai_rmf_1_0_2023` | governance/evals | Official AI risk-management framework structure and lifecycle vocabulary. |
| `ext_react_2022` | planning/agent control | Interleaved reasoning, acting, observation, and environment interaction. |
| `ext_tree_of_thoughts_2023` | planning/search | Deliberative search over intermediate reasoning paths with evaluation and backtracking. |
| `ext_pddl_1998` | planning/modeling | Domain/problem separation, action schemas, comparable planning notation, and planner-interface discipline. |
| `ext_shop2_2003` | planning/HTN | Hierarchical task-network planning, ordered task decomposition, method selection, and competition-result boundaries. |
| `ext_integrated_tamp_2020` | planning/TAMP | Discrete task planning, continuous feasibility subproblems, motion-planning interfaces, and integration-strategy vocabulary. |
| `ext_rag_2020` | retrieval/context | Retrieval-augmented generation and the boundary between model memory and retrieved evidence. |
| `ext_lost_in_middle_2023` | retrieval/context | Long-context position sensitivity and the gap between available context and used evidence. |
| `ext_memgpt_2023` | retrieval/context management | OS-inspired virtual context management, memory tiers, and long-running conversation/document-analysis boundaries. |
| `ext_longbench_2023` | long-context evaluation | Bilingual, multitask long-context benchmark coverage and task-specific context-understanding boundaries. |
| `ext_ruler_2024` | long-context evaluation | Synthetic long-context stress testing beyond simple needle retrieval, including multi-needle, tracing, and aggregation tasks. |
| `ext_proof_carrying_code_1997` | formal methods | Proof-carrying artifacts and consumer-side proof checking against a policy. |
| `ext_tla_plus_home_docs` | formal methods | System specification and model-checking vocabulary for concurrent and distributed systems. |
| `ext_sparse_moe_2017` | routing/MoE | Sparsely gated expert layers, conditional computation, and load-balancing limits. |
| `ext_gshard_2020` | routing/MoE | Conditional computation with automatic sharding and distributed sparse-model constraints. |
| `ext_switch_transformer_2021` | routing/MoE | Simplified sparse expert routing, stability, communication, and speed/scale boundaries. |
| `ext_deep_compression_2015` | compression/representation | Pruning, trained quantization, coding, and utility-preservation boundaries. |
| `ext_lora_2021` | compression/representation | Low-rank adaptation, parameter-efficient updates, and adaptation-boundary vocabulary. |
| `ext_mmlu_2020` | benchmark science | Broad multitask benchmark coverage, uneven performance, and saturation pressure. |
| `ext_bigbench_2022` | benchmark science | Broad community benchmark tasks, scale trends, calibration, and residual tradeoffs. |
| `ext_helm_2022` | benchmark science | Multi-scenario, multi-metric, transparent, living evaluation practice. |

## Current Effect

- Added public-safe source inventory records.
- Added matching source notes.
- Generated Appendix H can now list initial source-noted records for all Phase 6 priority queues.
- The planning queue now has initial source-noted coverage for interleaved reasoning/acting, tree search, planning-language interfaces, HTN decomposition, and task-and-motion planning.
- The retrieval/context queue now has initial source-noted coverage for RAG, long-context position sensitivity, virtual context management, multitask long-context evaluation, and synthetic context-size stress tests.
- No chapter source assignments, Appendix C support states, evidence transitions, proof targets, planner runs, motion-planning runs, context-management runs, long-context benchmark runs, or test results changed.

## Non-Claims

- This pass does not prove any ASI Stack alignment, governance, safety,
  evaluation, or deployment claim.
- It does not reproduce any paper result.
- It does not claim NIST AI RMF conformance, frontier-governance compliance, or
  independent audit.
- The literature set is initial and selective, not comprehensive.

## Next Queues

1. Deepen planning coverage with behavior trees, GOAP, broader agent-orchestration sources, and any PlanForge-specific planning-language translation references that become necessary.
2. Deepen retrieval/context coverage with MemGPT-adjacent memory-system follow-ups, context-engineering surveys, provenance-aware RAG, context compression/evaluation, and VCM-specific adapter references.
3. Deepen formal-methods coverage with runtime assurance, proof-assistant, and contract-verification sources.
4. Deepen routing coverage with modern LLM MoE surveys, router evaluation, and modular-agent orchestration sources.
5. Deepen compression coverage with program synthesis, quantization, distillation, residual coding, and artifact-utility sources.
6. Deepen benchmark-science coverage with contamination, hidden-test, saturation, and evaluation-gaming sources.
