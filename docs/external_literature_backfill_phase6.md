# Phase 6 External Literature Backfill

Last updated: 2026-06-28

This document records the initial Phase 6 external-literature backfill passes.
The current pass covers alignment/control, AI governance/evaluation,
planning/agent control, retrieval/context, and formal methods. It does not claim
complete literature coverage.

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
| `ext_rag_2020` | retrieval/context | Retrieval-augmented generation and the boundary between model memory and retrieved evidence. |
| `ext_lost_in_middle_2023` | retrieval/context | Long-context position sensitivity and the gap between available context and used evidence. |
| `ext_proof_carrying_code_1997` | formal methods | Proof-carrying artifacts and consumer-side proof checking against a policy. |
| `ext_tla_plus_home_docs` | formal methods | System specification and model-checking vocabulary for concurrent and distributed systems. |

## Current Effect

- Added public-safe source inventory records.
- Added matching source notes.
- Generated Appendix H can now list initial source-noted records for five Phase 6 priority queues.
- No chapter source assignments, Appendix C support states, evidence transitions, proof targets, or test results changed.

## Non-Claims

- This pass does not prove any ASI Stack alignment, governance, safety,
  evaluation, or deployment claim.
- It does not reproduce any paper result.
- It does not claim NIST AI RMF conformance, frontier-governance compliance, or
  independent audit.
- The literature set is initial and selective, not comprehensive.

## Next Queues

1. Deepen planning coverage with HTN, behavior trees, GOAP, TAMP, and agent-orchestration sources.
2. Deepen retrieval/context coverage with context-engineering and long-context benchmark sources.
3. Deepen formal-methods coverage with runtime assurance, proof-assistant, and contract-verification sources.
4. Mixture-of-experts, routing, modular agents, and model/system routing.
5. Compression, representation learning, program synthesis, and residual/error accounting.
6. Benchmark science, contamination, saturation, hidden tests, and evaluation gaming.
