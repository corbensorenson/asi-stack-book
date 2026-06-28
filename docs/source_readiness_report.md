# Source Readiness Report

Generated from `sources/source_inventory.json`, `sources/cache/cache_manifest.json`, and authenticated connector-readiness overrides when present.

Raw source exports are local-only and ignored by git. This report tracks readiness without publishing the raw source text.

## Summary

- `cached_existing`: 38
- `connector_readable`: 7
- `source_note_available_public_project`: 17
- `source_note_available_uncached`: 90

## Records

| Source ID | Title | Cache status | Bytes | Local raw path | Error / note |
|---|---|---:|---:|---|---|
| `viea` | Verified Intent-to-Execution Architecture | `cached_existing` | 211471 | sources/raw/google_docs/viea.txt | source note available |
| `scf` | Stable Capability Fields | `cached_existing` | 215254 | sources/raw/google_docs/scf.txt | source note available |
| `planforge` | PlanForge | `cached_existing` | 49857 | sources/raw/google_docs/planforge.txt | source note available |
| `planforge_compiler_arch` | PlanForge: A Compiler Architecture for AI Task Orchestration | `cached_existing` | 18745 | sources/raw/google_docs/planforge_compiler_arch.txt | source note available |
| `cognitive_compilation` | Cognitive Compilation | `cached_existing` | 112425 | sources/raw/google_docs/cognitive_compilation.txt | source note available |
| `talos` | Talos Protocol | `cached_existing` | 440468 | sources/raw/google_docs/talos.txt | source note available |
| `talos_md` | Talos_Protocol_v1.0.md | `connector_readable` | 947861 | sources/raw/google_docs/talos_md.bin | source note available; Authenticated connector fetch succeeded for the public Markdown Talos release; local cache is an auth-gate placeholder; local cache note: local cache is a Google sign-in/auth-gate page, not usable source text |
| `vcm_public` | Virtual_Context_Memory_v1 | `cached_existing` | 235401 | sources/raw/google_docs/vcm_public.txt | source note available |
| `vcm_editable` | Virtual_Context_Memory_v1.0_Editable | `connector_readable` |  |  | source note available; Authenticated connector fetch succeeded for the editable VCM paper; local curl cache is not authoritative; local cache note: curl: (56) The requested URL returned error: 401 |
| `spinoza` | Proof of Belief / The Spinoza Architecture | `cached_existing` | 209889 | sources/raw/google_docs/spinoza.txt | source note available |
| `spinoza_composer` | Spinoza Composer / Spinoza Trinity | `cached_existing` | 113517 | sources/raw/google_docs/spinoza_composer.txt | source note available |
| `moecot` | MoECOT-Agent Architecture Whitepaper | `connector_readable` |  |  | source note available; Authenticated connector fetch succeeded for the MoECOT-Agent Architecture Whitepaper; use the source note before source-derived claims; local cache note: curl: (56) The requested URL returned error: 401 |
| `moecot_md` | moecot_agent_whitepaper.md | `connector_readable` | 947532 | sources/raw/google_docs/moecot_md.bin | source note available; Authenticated connector fetch succeeded for the Markdown MoECOT whitepaper; local cache is an auth-gate placeholder; local cache note: local cache is a Google sign-in/auth-gate page, not usable source text |
| `octopus_router` | Octopus Router Architecture | `cached_existing` | 49310 | sources/raw/google_docs/octopus_router.txt | source note available |
| `rmi` | Ratcheting Modular Intelligence | `cached_existing` | 49750 | sources/raw/google_docs/rmi.txt | source note available |
| `cognitive_loop_closure` | Cognitive Loop Closure | `cached_existing` | 77845 | sources/raw/google_docs/cognitive_loop_closure.txt | source note available |
| `benchmaxxing` | Benchmaxxing: The Performance Ratchet | `cached_existing` | 51787 | sources/raw/google_docs/benchmaxxing.txt | source note available |
| `cgs` | Compact Generative Systems | `cached_existing` | 60191 | sources/raw/google_docs/cgs.txt | source note available |
| `rgs` | Ratcheting Generative Systems | `cached_existing` | 58010 | sources/raw/google_docs/rgs.txt | source note available |
| `rankfold_neuralfold` | RankFold + NeuralFold | `cached_existing` | 108056 | sources/raw/google_docs/rankfold_neuralfold.txt | source note available |
| `rankfold_compressor` | rankFold compressor | `cached_existing` | 185058 | sources/raw/google_docs/rankfold_compressor.txt | source note available |
| `bbvca_v9` | BBVCA_v9_final_public_release | `cached_existing` | 71278 | sources/raw/google_docs/bbvca_v9.txt | source note available |
| `bbvca_main` | Big Bang Volumetric Compression Architecture | `cached_existing` | 416925 | sources/raw/google_docs/bbvca_main.txt | source note available |
| `genesiscode` | GenesisCode | `cached_existing` | 60187 | sources/raw/google_docs/genesiscode.txt | source note available |
| `alignment_field` | Field of God / Alignment Field family | `cached_existing` | 458438 | sources/raw/google_docs/alignment_field.txt | source note available |
| `field_of_god` | The Field of God | `cached_existing` | 246511 | sources/raw/google_docs/field_of_god.txt | source note available |
| `field_of_god_ai_constitution` | Field of God AI Constitution | `source_note_available_public_project` |  |  | source note available from inspected public project source; not part of Google Drive cache manifest |
| `ethica_mechanica` | Ethica Mechanica | `cached_existing` | 15708 | sources/raw/google_docs/ethica_mechanica.txt | source note available |
| `eternal_code` | The Eternal Code / unified God, reality, conscious, alignment | `cached_existing` | 92385 | sources/raw/google_docs/eternal_code.txt | source note available |
| `coherence_exchange` | The Coherence Exchange | `connector_readable` |  |  | source note available; Authenticated connector fetch succeeded; speculative/metaphysical material must remain explicitly bounded; local cache note: curl: (56) The requested URL returned error: 401 |
| `verification_bandwidth` | Verification Bandwidth in Bounded Contexts | `cached_existing` | 10913 | sources/raw/google_docs/verification_bandwidth.txt | source note available |
| `beastbrain` | BeastBrain Cognitive Architecture | `cached_existing` | 571911 | sources/raw/google_docs/beastbrain.txt | source note available |
| `beastbrain_timeless` | BeastBrain Architecture: Timeless Edition | `cached_existing` | 26911 | sources/raw/google_docs/beastbrain_timeless.txt | source note available |
| `aletheia` | Aletheia Foundry | `cached_existing` | 91713 | sources/raw/google_docs/aletheia.txt | source note available |
| `context_engineer` | Context Engineer / Manhattan Protocol | `cached_existing` | 18556 | sources/raw/google_docs/context_engineer.txt | source note available |
| `black_hole_context_manager` | Black Hole Context Manager | `cached_existing` | 19880 | sources/raw/google_docs/black_hole_context_manager.txt | source note available |
| `ladon_manhattan` | Ladon & The Manhattan Protocol | `cached_existing` | 8945 | sources/raw/google_docs/ladon_manhattan.txt | source note available |
| `uat` | Unified Adaptive Tribunal | `cached_existing` | 40830 | sources/raw/google_docs/uat.txt | source note available |
| `treellm` | TreeLLM | `cached_existing` | 550184 | sources/raw/google_docs/treellm.txt | source note available |
| `software_magic_grimoire` | Software Magic Grimoire | `cached_existing` | 407939 | sources/raw/google_docs/software_magic_grimoire.txt | source note available |
| `road_to_agi` | Road To AGI | `connector_readable` | 947750 | sources/raw/google_docs/road_to_agi.bin | source note available; Authenticated connector fetch succeeded; reported benchmark claims remain source-reported until artifacts are independently ingested and verified; local cache note: local cache is a Google sign-in/auth-gate page, not usable source text |
| `simulation_scaling` | Simulation Scaling Law | `cached_existing` | 136055 | sources/raw/google_docs/simulation_scaling.txt | source note available |
| `tokenmana` | TokenMana | `cached_existing` | 60285 | sources/raw/google_docs/tokenmana.txt | source note available |
| `coilmoecot` | CoilMoECOT Whitepaper v2.0 | `connector_readable` | 947737 | sources/raw/google_docs/coilmoecot.bin | source note available; Authenticated connector fetch succeeded for the CoilMoECOT design/spec source; do not treat it as performance evidence; local cache note: local cache is a Google sign-in/auth-gate page, not usable source text |
| `temporal_coil_research` | Temporal Coil Research | `cached_existing` | 11522 | sources/raw/google_docs/temporal_coil_research.bin | source note available |
| `bugbrain` | BugBrain | `cached_existing` | 313058 | sources/raw/google_docs/bugbrain.txt | source note available |
| `project_theseus_whitepaper` | Project Theseus Whitepaper | `source_note_available_public_project` |  |  | source note available from inspected public project source; not part of Google Drive cache manifest |
| `theseus_plan_compiler` | Theseus Plan Compiler | `source_note_available_public_project` |  |  | source note available from inspected public project source; not part of Google Drive cache manifest |
| `theseus_self_evolution_system` | Theseus Self-Evolution System | `source_note_available_public_project` |  |  | source note available from inspected public project source; not part of Google Drive cache manifest |
| `theseus_architecture_gate` | Theseus Architecture Gate | `source_note_available_public_project` |  |  | source note available from inspected public project source; not part of Google Drive cache manifest |
| `theseus_operator_os` | Hive Operator OS and Work Board | `source_note_available_public_project` |  |  | source note available from inspected public project source; not part of Google Drive cache manifest |
| `theseus_circle_transfer` | Theseus Circle Calculus Transfer Lane | `source_note_available_public_project` |  |  | source note available from inspected public project source; not part of Google Drive cache manifest |
| `circle_calculus_core` | Circle Calculus | `source_note_available_public_project` |  |  | source note available from inspected public project source; not part of Google Drive cache manifest |
| `circle_ai_contract_suite` | Circle Calculus AI Contract Suite | `source_note_available_public_project` |  |  | source note available from inspected public project source; not part of Google Drive cache manifest |
| `circle_ai_architectures` | Circle AI Architectures | `source_note_available_public_project` |  |  | source note available from inspected public project source; not part of Google Drive cache manifest |
| `coil_attention_memory` | Coil Attention and Memory | `source_note_available_public_project` |  |  | source note available from inspected public project source; not part of Google Drive cache manifest |
| `coilra_multicoil_rope` | CoilRA and MultiCoil RoPE | `source_note_available_public_project` |  |  | source note available from inspected public project source; not part of Google Drive cache manifest |
| `rope_position_certifier` | Proof-Carrying RoPE Position Distinguishability | `source_note_available_public_project` |  |  | source note available from inspected public project source; not part of Google Drive cache manifest |
| `proof_carrying_circular_computation` | Proof-Carrying Circular Computation | `source_note_available_public_project` |  |  | source note available from inspected public project source; not part of Google Drive cache manifest |
| `ext_concrete_ai_safety_2016` | Concrete Problems in AI Safety | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_corrigibility_2015` | Corrigibility | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_off_switch_game_2016` | The Off-Switch Game | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_optimal_policies_power_2019` | Optimal Policies Tend to Seek Power | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_model_evaluation_extreme_risks_2023` | Model evaluation for extreme risks | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_frontier_ai_regulation_2023` | Frontier AI Regulation: Managing Emerging Risks to Public Safety | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_nist_ai_rmf_1_0_2023` | Artificial Intelligence Risk Management Framework (AI RMF 1.0) | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_react_2022` | ReAct: Synergizing Reasoning and Acting in Language Models | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_tree_of_thoughts_2023` | Tree of Thoughts: Deliberate Problem Solving with Large Language Models | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_pddl_1998` | PDDL: The Planning Domain Definition Language | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_shop2_2003` | SHOP2: An HTN Planning System | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_integrated_tamp_2020` | Integrated Task and Motion Planning | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_behavior_trees_robotics_ai_2017` | Behavior Trees in Robotics and AI: An Introduction | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_three_states_plan_fear_2006` | Three States and a Plan: The A.I. of F.E.A.R. | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_autogen_2023` | AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_rag_2020` | Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_lost_in_middle_2023` | Lost in the Middle: How Language Models Use Long Contexts | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_memgpt_2023` | MemGPT: Towards LLMs as Operating Systems | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_longbench_2023` | LongBench: A Bilingual, Multitask Benchmark for Long Context Understanding | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_ruler_2024` | RULER: What's the Real Context Size of Your Long-Context Language Models? | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_alce_2023` | Enabling Large Language Models to Generate Text with Citations | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_self_rag_2023` | Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_longllmlingua_2023` | LongLLMLingua: Accelerating and Enhancing LLMs in Long Context Scenarios via Prompt Compression | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_proof_carrying_code_1997` | Proof-Carrying Code | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_tla_plus_home_docs` | My TLA+ Home Page | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_lean4_theorem_proving` | Theorem Proving in Lean 4 | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_dafny_2010` | Dafny: An Automatic Program Verifier For Functional Correctness | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_reluplex_2017` | Reluplex: An Efficient SMT Solver for Verifying Deep Neural Networks | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_black_box_simplex_2021` | The Black-Box Simplex Architecture for Runtime Assurance of Autonomous CPS | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_copilot_runtime_monitor_2010` | Copilot: A Hard Real-Time Runtime Monitor | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_prism_model_checker_2002` | PRISM: Probabilistic Symbolic Model Checker | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_sparse_moe_2017` | Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_gshard_2020` | GShard: Scaling Giant Models with Conditional Computation and Automatic Sharding | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_switch_transformer_2021` | Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_expert_choice_routing_2022` | Mixture-of-Experts with Expert Choice Routing | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_mixtral_2024` | Mixtral of Experts | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_moe_llm_survey_2024` | A Survey on Mixture of Experts in Large Language Models | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_frugalgpt_2023` | FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_hybrid_llm_2024` | Hybrid LLM: Cost-Efficient and Quality-Aware Query Routing | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_routellm_2024` | RouteLLM: Learning to Route LLMs with Preference Data | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_deep_compression_2015` | Deep Compression: Compressing Deep Neural Networks with Pruning, Trained Quantization and Huffman Coding | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_lora_2021` | LoRA: Low-Rank Adaptation of Large Language Models | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_knowledge_distillation_2015` | Distilling the Knowledge in a Neural Network | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_gptq_2022` | GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_qlora_2023` | QLoRA: Efficient Finetuning of Quantized LLMs | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_mmlu_2020` | Measuring Massive Multitask Language Understanding | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_bigbench_2022` | Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_helm_2022` | Holistic Evaluation of Language Models | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_gpqa_2023` | GPQA: A Graduate-Level Google-Proof Q&A Benchmark | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_swe_bench_2023` | SWE-bench: Can Language Models Resolve Real-World GitHub Issues? | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_livebench_2024` | LiveBench: A Challenging, Contamination-Limited LLM Benchmark | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_speculative_decoding_2022` | Fast Inference from Transformers via Speculative Decoding | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_multi_token_prediction_2024` | Better & Faster Large Language Models via Multi-token Prediction | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_medusa_2024` | Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_eagle_2024` | EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_lookahead_decoding_2024` | Break the Sequential Dependency of LLM Inference Using Lookahead Decoding | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_layerskip_2024` | LayerSkip: Enabling Early Exit Inference and Self-Speculative Decoding | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_pagedattention_vllm_2023` | Efficient Memory Management for Large Language Model Serving with PagedAttention | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_mamba_2023` | Mamba: Linear-Time Sequence Modeling with Selective State Spaces | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_llada_2025` | Large Language Diffusion Models | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_scaling_dllms_2026` | Scaling Beyond Masked Diffusion Language Models | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_trpo_2015` | Trust Region Policy Optimization | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_ppo_2017` | Proximal Policy Optimization Algorithms | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_remax_2023` | ReMax: A Simple, Effective, and Efficient Reinforcement Learning Method for Aligning Large Language Models | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_dpo_2023` | Direct Preference Optimization: Your Language Model is Secretly a Reward Model | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_ipo_preference_2023` | A General Theoretical Paradigm to Understand Learning from Human Preferences | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_orpo_2024` | ORPO: Monolithic Preference Optimization without Reference Model | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_kto_2024` | KTO: Model Alignment as Prospect Theoretic Optimization | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_simpo_2024` | SimPO: Simple Preference Optimization with a Reference-Free Reward | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_reinforce_style_rlhf_2024` | Back to Basics: Revisiting REINFORCE Style Optimization for Learning from Human Feedback in LLMs | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_deepseek_r1_2025` | DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_dapo_2025` | DAPO: An Open-Source LLM Reinforcement Learning System at Scale | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_gspo_2025` | Group Sequence Policy Optimization | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_s_grpo_2025` | S-GRPO: Early Exit via Reinforcement Learning in Reasoning Models | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_longrlvr_2026` | LongRLVR: Long-Context Reinforcement Learning Requires Verifiable Context Rewards | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_rlhf_limitations_2023` | Open Problems and Fundamental Limitations of Reinforcement Learning from Human Feedback | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_tailscale_docs_2025` | What is Tailscale? | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_kubernetes_overview_docs` | Kubernetes Documentation: Overview | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_k3s_docs_2026` | K3s: Lightweight Kubernetes | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_nomad_docs` | Nomad Documentation | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_ray_core_docs_2026` | What's Ray Core? | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_boinc_home_2026` | BOINC | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_syncthing_home` | Syncthing | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_ipfs_docs` | IPFS Documentation and Project Site | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_akash_docs_2026` | Akash Network Documentation | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_golem_docs_2025` | Golem Developer Resources | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_github_webhooks_docs` | Webhook events and payloads | `source_note_available_public_project` |  |  | source note available from inspected public project source; not part of Google Drive cache manifest |
| `ext_github_self_hosted_runners_docs` | Self-hosted runners | `source_note_available_public_project` |  |  | source note available from inspected public project source; not part of Google Drive cache manifest |
| `ext_openzeppelin_governor_docs` | OpenZeppelin Contracts: Governance | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_open_collective_docs` | Open Collective Documentation | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_github_sponsors_docs` | About GitHub Sponsors for open source contributors | `source_note_available_public_project` |  |  | source note available from inspected public project source; not part of Google Drive cache manifest |
| `ext_agentic_workflow_injection_2026` | Demystifying and Detecting Agentic Workflow Injection Vulnerabilities in GitHub Actions | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
| `ext_dao_delegation_fairness_2025` | Fairness in Token Delegation: Mitigating Voting Power Concentration in DAOs | `source_note_available_uncached` |  |  | source note available; source inventory record is not present in the cache manifest |
