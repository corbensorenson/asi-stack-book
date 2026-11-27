# External Literature Queue

This book currently treats Corben Sorenson's AI papers, local projects, and conversation-mined architecture context as the primary research program being unified. That is a valid starting point, but it is not the same thing as third-party corroboration.

## Stance

- `source-derived` means derived from Corben's papers, Corben-supplied materials, recovered project records, or local project ASI Stack sources unless a claim explicitly cites third-party literature.
- `external-literature-backed` is reserved for claims backed by recorded third-party sources with bibliographic metadata.
- Self-authored sources can explain the architecture, motivate design choices, and preserve lineage, but they should not be presented as external validation.
- Third-party references discovered inside source papers still need to be recorded in this repo before the book relies on them.

## Priority Areas

| Area | Why it matters | Initial action |
|---|---|---|
| AI alignment and corrigibility | Ground constitutional alignment, corrigibility, agency, and power-seeking claims. | Add canonical survey/key-paper candidates before drafting Part I claims as literature-backed. |
| AI governance and evaluations | Ground readiness gates, audits, deployment policy, evals, and incident response. | Create citation-normalized source records for governance/evals references. |
| Agent planning and task decomposition | Compare PlanForge to planning-language interfaces, HTN, behavior trees, GOAP, TAMP, and modern agent orchestration. | Initial records and source notes exist for ReAct, Tree of Thoughts, PDDL, SHOP2, Integrated TAMP, Behavior Trees in Robotics and AI, F.E.A.R.-style GOAP, and AutoGen; PlanForge-translation comparison sources and deeper planning-runtime adapter comparisons remain queued. |
| Memory, RAG, and context engineering | Compare VCM to long-context, RAG, MemGPT-style memory, ClawVM/RAMPART-like context compilation, and benchmark literature. | Initial records and source notes exist for RAG, Lost in the Middle, MemGPT, LongBench, RULER, ALCE, Self-RAG, and LongLLMLingua; context-engineering surveys, VCM-specific adapter references, and any additional provenance/compression sources needed after chapter review remain queued. |
| Formal methods and proof assistants | Ground Lean, proof-carrying claims, runtime assurance, neural-network verification, and contract verification. | Initial records and source notes exist for proof-carrying code, TLA+, Lean theorem proving, Dafny, Reluplex, Black-Box Simplex, Copilot, and PRISM; richer proof-assistant adequacy, ASI Stack protocol-verification sources, and additional deployment model-checking references remain queued. |
| Modular systems and routing | Compare MoECOT, Octopus, RMI, and specialist routing to MoE/routing/modular-agent literature. | Initial records and source notes exist for sparse MoE, GShard, Switch Transformers, Expert Choice Routing, Mixtral, an MoE-in-LLMs survey, FrugalGPT, Hybrid LLM, and RouteLLM; governance-aware route-selection sources, routing-specific modular-agent orchestration, and additional model/system routing comparisons remain queued. |
| Compression and representation learning | Ground CGS, RankFold/NeuralFold, BBVCA, semantic trees, and residual accounting. | Initial records and source notes exist for Deep Compression, LoRA, knowledge distillation, GPTQ, QLoRA, DreamCoder, Information Bottleneck, MDL, and CodeBLEU; compression-regression testing and additional representation-learning sources remain queued. |
| Fast generation and decoding substrates | Ground MTP, speculative decoding, multi-head drafting, diffusion LLMs, early exit, state-space alternatives, KV-cache serving, and useful-solution-per-second metrics. | Initial source records, source notes, and primary arXiv citation metadata exist for the current fast-generation set; no speed-quality claim is promoted without reproduction or narrower passage review. |
| Policy optimization and learning from feedback | Ground REINFORCE/RLOO/ReMax-style policy gradients, TRPO/PPO/RLHF, GRPO/DAPO/GSPO-style group or sequence updates, DPO/IPO/ORPO/KTO/SimPO-style preference optimization, RLVR/context rewards, process rewards, reward hacking, reasoning-budget RL, and control-policy RL for planners, routers, VCM, execution, and generation modes. | Initial source records, source notes, and primary arXiv citation metadata exist for TRPO, PPO, ReMax, DPO, IPO/preference theory, ORPO, KTO, SimPO, REINFORCE-style RLHF, DeepSeek-R1, DAPO, GSPO, S-GRPO, LongRLVR, and RLHF limitations; broader process-reward, RLOO/REINFORCE++, and evaluator-gaming work remains queued. |
| Benchmarks and anti-Goodhart methods | Ground benchmark ratchets, hidden tests, saturation, residual preservation, contamination resistance, and eval gaming. | Initial records and source notes exist for MMLU, BIG-bench, HELM, GPQA, SWE-bench, LiveBench, Dynabench, CheckList, benchmark-contamination work, and Goodhart variants; hidden-holdout operations, saturation analysis, evaluator-gaming sources, and release-grade benchmark governance remain queued. |

## Import Rule

When a third-party source is actually used, add it to `sources/source_inventory.json` with a stable source ID, create a source note after reading it, and update `book_structure.json` only for chapters that will mine it directly. Do not cite a paper from memory or from another source's bibliography without reading it.

## November 27, 2026 integration

Reviewed primary papers and author-maintained project documentation through November 27. Nineteen external records entered the inventory. Their source notes identify the comparison, its limits, and the question that remains open.

| Decision | Technical passage | Reader exercise |
|---|---|---|
| Transfer a numerical edit or rerun its program on the destination checkpoint | [Weight-program transfer](../chapters/cognitive-compilation-and-semantic-ir.qmd#weight-program-transfer) | [A repair that has to travel](../editions/reader_manuscript/current/chapters/unit-13-cognitive-compilation-and-semantic-ir.qmd#reader-weight-program) |
| Choose a better solver or appoint the next editor | [Successor editing ability](../chapters/recursive-self-improvement-boundaries.qmd#better-model-or-better-editor) | [Who gets the editor’s job?](../editions/reader_manuscript/current/chapters/unit-25-recursive-improvement-replication-and-containment.qmd#reader-better-editor) |
| Keep Linux or boot an inference kernel on the device | [Inference-kernel placement](../chapters/physical-compute-infrastructure-energy-and-environmental-constraints.qmd#inference-kernel-placement) | [Two boxes boot to the same prompt](../editions/reader_manuscript/current/chapters/unit-24-physical-compute-energy-and-infrastructure.qmd#reader-inference-kernel) |

The newest selected papers supply two controls. The November 25 forward-only editing study compares operator selection with the same tool library. The November 24 RecurSciBench paper evaluates frozen successors on independent scientific tasks and retains task-level outcomes. The hardware comparison uses the corrected July version of ProbeLogits and distinguishes a physical boot from a hosted inference experiment. [Forward-only programming](https://arxiv.org/abs/2611.34612v1) · [RecurSciBench](https://arxiv.org/abs/2611.32508v1) · [ProbeLogits v3](https://arxiv.org/html/2604.11943v3)
