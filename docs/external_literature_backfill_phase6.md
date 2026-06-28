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
| `ext_behavior_trees_robotics_ai_2017` | planning/behavior trees | Modular reactive task switching, behavior-tree robustness/safety analysis vocabulary, planning integration, and stochastic outcome accounting. |
| `ext_three_states_plan_fear_2006` | planning/GOAP | Goal Oriented Action Planning in real-time action games, practical planner constraints, autonomous characters, and squad-behavior composition. |
| `ext_autogen_2023` | planning/agent orchestration | Conversable multi-agent LLM workflows, human/tool/LLM modes, programmable interaction patterns, and application-level orchestration boundaries. |
| `ext_rag_2020` | retrieval/context | Retrieval-augmented generation and the boundary between model memory and retrieved evidence. |
| `ext_lost_in_middle_2023` | retrieval/context | Long-context position sensitivity and the gap between available context and used evidence. |
| `ext_memgpt_2023` | retrieval/context management | OS-inspired virtual context management, memory tiers, and long-running conversation/document-analysis boundaries. |
| `ext_longbench_2023` | long-context evaluation | Bilingual, multitask long-context benchmark coverage and task-specific context-understanding boundaries. |
| `ext_ruler_2024` | long-context evaluation | Synthetic long-context stress testing beyond simple needle retrieval, including multi-needle, tracing, and aggregation tasks. |
| `ext_alce_2023` | retrieval/citation evaluation | Retrieval-backed answer generation, citation-quality metrics, factual correctness, and evidence-support gaps. |
| `ext_self_rag_2023` | retrieval/reflection | Adaptive retrieval, generated critique/reflection tokens, passage relevance, factuality, and citation accuracy boundaries. |
| `ext_longllmlingua_2023` | context compression | Long-context prompt compression, key-information density, position bias, cost, latency, and compression-evaluation boundaries. |
| `ext_proof_carrying_code_1997` | formal methods | Proof-carrying artifacts and consumer-side proof checking against a policy. |
| `ext_tla_plus_home_docs` | formal methods | System specification and model-checking vocabulary for concurrent and distributed systems. |
| `ext_lean4_theorem_proving` | proof assistants | Lean theorem-proving vocabulary, dependent type theory, tactics, records, inductive types, and proof-term boundaries. |
| `ext_dafny_2010` | program verification | Specification-oriented programming, functional-correctness verification, SMT-backed automation, and contract/verifier boundaries. |
| `ext_reluplex_2017` | AI formal verification | Property-specific verification for ReLU neural networks, counterexamples, safety-critical property scope, and ACAS Xu evaluation boundaries. |
| `ext_black_box_simplex_2021` | runtime assurance | Runtime control switching, backup safety behavior, black-box controllers, and assurance-wrapper boundaries. |
| `ext_copilot_runtime_monitor_2010` | runtime monitoring | Stream-based hard real-time monitors, constant-time/constant-space generated C monitors, and monitor-scheduler boundaries. |
| `ext_prism_model_checker_2002` | probabilistic model checking | Symbolic probabilistic model checking, model/property/tool-run separation, and probabilistic reliability-analysis vocabulary. |
| `ext_sparse_moe_2017` | routing/MoE | Sparsely gated expert layers, conditional computation, and load-balancing limits. |
| `ext_gshard_2020` | routing/MoE | Conditional computation with automatic sharding and distributed sparse-model constraints. |
| `ext_switch_transformer_2021` | routing/MoE | Simplified sparse expert routing, stability, communication, and speed/scale boundaries. |
| `ext_expert_choice_routing_2022` | routing/MoE | Expert-choice routing, token/expert assignment direction, load-balancing pressure, expert capacity, and convergence/performance boundaries. |
| `ext_mixtral_2024` | routing/MoE | Sparse LLM token-level expert routing, active-parameter accounting, open model release boundaries, and benchmark-claim limits. |
| `ext_moe_llm_survey_2024` | routing/MoE survey | LLM MoE taxonomy, algorithmic/systemic design issues, implementation patterns, evaluation practice, and open directions. |
| `ext_frugalgpt_2023` | routing/task cascades | Prompt adaptation, model approximation, LLM cascades, cost/performance tradeoffs, and query-specific model selection. |
| `ext_hybrid_llm_2024` | routing/cost-quality | Predicted query difficulty, small/large model routing, dynamic quality-cost tradeoffs, and large-model-call reduction. |
| `ext_routellm_2024` | routing/learned routers | Preference-data routers, stronger/weaker LLM selection, cost-quality tradeoffs, and model-pair transfer boundaries. |
| `ext_deep_compression_2015` | compression/representation | Pruning, trained quantization, coding, and utility-preservation boundaries. |
| `ext_lora_2021` | compression/representation | Low-rank adaptation, parameter-efficient updates, and adaptation-boundary vocabulary. |
| `ext_knowledge_distillation_2015` | compression/distillation | Teacher/student distillation, soft-target transfer, ensemble compression, and behavior-transfer limits. |
| `ext_gptq_2022` | compression/quantization | Post-training transformer quantization, memory reduction, and accuracy/speed tradeoff boundaries. |
| `ext_qlora_2023` | compression/quantized adaptation | Quantized LLM finetuning with low-rank adapters, memory-efficient adaptation, and benchmark-claim limits. |
| `ext_dreamcoder_2020` | program synthesis/representation | Wake-sleep library learning, reusable symbolic abstractions, and compression-through-abstraction boundaries. |
| `ext_information_bottleneck_2000` | representation/compression | Relevance-preserving compression, bottleneck variables, and utility-versus-size tradeoff vocabulary. |
| `ext_mdl_tutorial_2004` | description length/residuals | Model/data description-length tradeoffs, compression discipline, and residual-accounting vocabulary. |
| `ext_codebleu_2020` | artifact utility metrics | Code-aware artifact evaluation using lexical, syntax, data-flow, and semantic matching signals. |
| `ext_mmlu_2020` | benchmark science | Broad multitask benchmark coverage, uneven performance, and saturation pressure. |
| `ext_bigbench_2022` | benchmark science | Broad community benchmark tasks, scale trends, calibration, and residual tradeoffs. |
| `ext_helm_2022` | benchmark science | Multi-scenario, multi-metric, transparent, living evaluation practice. |
| `ext_gpqa_2023` | benchmark science | Expert-written Google-proof questions, scalable-oversight pressure, and skilled non-expert validation limits. |
| `ext_swe_bench_2023` | benchmark science | Real-world GitHub issue resolution, repository-scale context, executable environments, and patch-evaluation boundaries. |
| `ext_livebench_2024` | benchmark science | Contamination-limited monthly updated benchmark practice, objective ground-truth scoring, and stale-score pressure. |
| `ext_dynabench_2021` | dynamic benchmarking | Human-and-model-in-the-loop data collection, adversarial benchmark evolution, and stale static benchmark pressure. |
| `ext_checklist_2020` | behavioral evaluation | Capability matrices, minimum functionality tests, invariance tests, and directional expectation tests beyond aggregate accuracy. |
| `ext_benchmark_contamination_2023` | benchmark contamination | Training/test overlap pressure, benchmark-leakage risk, and score-interpretation limits in modern LLM evaluations. |
| `ext_goodhart_variants_2018` | Goodhart taxonomy | Regressive, extremal, causal, and adversarial proxy-metric failure vocabulary. |

## Current Effect

- Added public-safe source inventory records.
- Added matching source notes.
- Generated Appendix H can now list initial source-noted records for all Phase 6 priority queues.
- The planning queue now has initial source-noted coverage for interleaved reasoning/acting, tree search, planning-language interfaces, HTN decomposition, task-and-motion planning, behavior trees, GOAP/F.E.A.R.-style game planning, and AutoGen-style multi-agent orchestration.
- The retrieval/context queue now has initial source-noted coverage for RAG, long-context position sensitivity, virtual context management, multitask long-context evaluation, synthetic context-size stress tests, citation-quality evaluation, adaptive retrieval/reflection, and long-context prompt compression.
- The formal-methods queue now has initial source-noted coverage for proof-carrying artifacts, TLA+ system modeling, Lean proof-assistant practice, Dafny-style program verification, Reluplex-style neural-network property checking, runtime assurance, generated runtime monitors, and probabilistic model checking.
- The routing/MoE queue now has initial source-noted coverage for sparsely gated MoE, GShard, Switch Transformers, Expert Choice Routing, Mixtral, MoE-in-LLMs survey taxonomy, LLM cascades, quality-aware query routing, and learned route policies.
- The compression/representation queue now has initial source-noted coverage for pruning/quantization/coding, low-rank adaptation, knowledge distillation, GPTQ-style post-training quantization, QLoRA-style quantized finetuning, program-synthesis library learning, relevance-preserving bottlenecks, description-length residual accounting, and code-aware artifact metrics.
- The benchmark-science queue now has initial source-noted coverage for broad multitask benchmarks, community benchmark collections, holistic evaluation, expert hard-question oversight, real-world software issue resolution, contamination-limited living benchmarks, dynamic adversarial benchmark evolution, behavioral test matrices, contamination-risk auditing, and Goodhart-style proxy-metric failure taxonomy.
- No chapter source assignments, Appendix C support states, evidence transitions, proof targets, planner runs, motion-planning runs, context-management runs, long-context benchmark runs, proof-assistant imports, verifier runs, MoE training runs, model inference runs, compression experiments, program-synthesis runs, information-bottleneck or MDL scorer implementations, CodeBLEU runs, dynamic benchmark runs, behavioral-test runs, contamination audits, Goodhart taxonomies over local tests, finetuning runs, benchmark runs, or test results changed.

## Non-Claims

- This pass does not prove any ASI Stack alignment, governance, safety,
  evaluation, or deployment claim.
- It does not reproduce any paper result.
- It does not claim NIST AI RMF conformance, frontier-governance compliance, or
  independent audit.
- The literature set is initial and selective, not comprehensive.

## Next Queues

1. Deepen planning coverage with PlanForge-specific planning-language translation references, planner/runtime-adapter comparison records, and any additional orchestration sources needed after chapter-level review.
2. Deepen retrieval/context coverage with MemGPT-adjacent memory-system follow-ups, context-engineering surveys, VCM-specific adapter references, and any additional provenance/compression sources needed after chapter-level review.
3. Deepen formal-methods coverage with proof-assistant adequacy literature, ASI Stack protocol-verification sources, and any additional deployment model-checking references needed after chapter-level review.
4. Deepen routing coverage with governance-aware route-selection sources, routing-specific modular-agent orchestration, and any additional model/system routing comparisons needed after chapter-level review.
5. Deepen compression coverage with compression-regression testing, additional representation-learning sources, and any chapter-specific residual/error-accounting sources needed after review.
6. Deepen benchmark-science coverage with hidden-holdout operations, saturation analysis, evaluator-gaming sources, and release-grade benchmark governance.
