# Source Mining Synthesis

Updated: 2026-06-24

This report records the source-mining pass used to expand the book from a 16-chapter starter scaffold into a more granular source-of-truth outline. It is a planning and architecture synthesis record, not a replacement for per-source notes. Do not promote claims to `source-derived` solely because they appear here.

## Coverage

- Inventoried source records: 45.
- Locally readable cached text exports materially mined: 38.
- Connector-mined in this working session: `coherence_exchange`.
- Connector-mined earlier in this same project session and reflected in the outline: `vcm_editable`.
- Conversation-mined v2 packet reviewed locally from `sources/inbox/conversation_mining_v2/`; it is used only as author-intent, terminology, lineage, deduplication, and recovery context.
- Authenticated or recovery gaps still requiring durable source notes before source-derived claims: `moecot`, `moecot_md`, `road_to_agi`, `coilmoecot`, and `talos_md` variant.
- The `talos` primary source is readable, so the unusable `talos_md` variant is not a blocker for execution-layer outlining.

Several Drive-file `.bin` cache entries are Google sign-in pages rather than source exports. They remain useful as inventory records but not as source text. The outline now marks these as connector/recovery sources where relevant.

## Main Architecture Clusters Mined

| Cluster | Mined source families | Architectural role in the expanded outline |
|---|---|---|
| Whole-stack frame | `viea`, `beastbrain`, `aletheia`, `talos`, `moecot` inventory/handoff | ASI as a governed stack; intent-to-execution; artifacts; routing; runtime; feedback. |
| Governance and self-improvement | `scf`, `rmi`, `benchmaxxing`, `talos`, `ladon_manhattan` | Stable fields, authority ceilings, replacement transactions, rollback, readiness gates, residual escrow. |
| Alignment and constitutional substrate | `alignment_field`, `field_of_god`, `ethica_mechanica`, `eternal_code`, `coherence_exchange` | Dignity, agency, corrigibility, moral uncertainty, fork/exit/audit rights, constitutional kernels. |
| Planning and compilation | `planforge`, `planforge_compiler_arch`, `cognitive_compilation`, `software_magic_grimoire`, `viea` | Goals become plans, DAGs, semantic IR, command contracts, target compilation, repair loops. |
| Memory and context | `vcm_public`, `vcm_editable`, `context_engineer`, `black_hole_context_manager`, `verification_bandwidth` | Virtual Context ABI, semantic pages, certificates, snapshots, mounts, taint, adequacy, verification bandwidth. |
| Reasoning and verification | `spinoza`, `uat`, `verification_bandwidth`, `treellm`, `coherence_exchange`, `aletheia` | Claim ledgers, belief revision, proof-carrying claims, tribunals, adversarial review, support tiers. |
| Execution and labor OS | `talos`, `viea`, `genesiscode`, `software_magic_grimoire`, `cognitive_loop_closure`, `ladon_manhattan` | Typed jobs, tool permissions, approvals, artifact graphs, audit logs, replay, loop closure. |
| Routing and modular intelligence | `octopus_router`, `rmi`, `benchmaxxing`, `cognitive_loop_closure`, `beastbrain`, `moecot` inventory/handoff | Router head, specialist cores, readiness, quarantine, residuals, multi-core runtime crosswalk. |
| Compression and representation | `cgs`, `rgs`, `bbvca_v9`, `bbvca_main`, `rankfold_neuralfold`, `rankfold_compressor`, `treellm`, `bugbrain` | Compact generative systems, generate-verify-repair, artifact compression, semantic representation, fallback. |
| Resources and substrates | `tokenmana`, `simulation_scaling`, `genesiscode`, `temporal_coil_research`, `coilmoecot` inventory/handoff | Token budgets, verification tax, fidelity limits, executable specs, optional mathematical/search substrates. |
| Living evidence process | `benchmaxxing`, `viea`, `rmi`, `cognitive_loop_closure`, `road_to_agi` inventory/handoff | Claim/evidence discipline, benchmarks, proof manifest, prototype roadmap, source queues, bibliography plan. |

## Why the Outline Needed More Chapters

The starter scaffold had the correct architecture layers but packed several distinct mechanisms into monolithic chapters. The source pass showed that many concepts deserve their own precise drafting and proof surface:

- `Alignment and Constitution` split into constitutional substrate, dignity/corrigibility, value conflict, and governance rights.
- `Governance and SCF` split into authority boundaries, SCFs, replacement/rollback, security kernel, and self-improvement boundaries.
- `Planning and Control` split into intent contracts, command contracts, planning, PlanForge DAGs, and cognitive compilation.
- `Virtual Context Memory` split into ABI, semantic pages/certificates, transactions/snapshots/taint, and verification bandwidth.
- `Reasoning and Verification` split into claim ledgers, proof-carrying claims, and tribunal/adversarial review.
- `Labor and Execution OS` split into typed jobs, artifacts/audit/replay, runtime adapters, and procedural memory.
- `Routing and Modular Intelligence` split into routing heads, readiness/residual/quarantine, and MoECOT runtime crosswalk.
- `Compression and Representation` split into CGS, generate-verify-repair, RankFold/NeuralFold, TreeLLM, resource economics, simulation fidelity, and mathematical/executable substrates.
- `Integration and Implementation` split into benchmark ratchets, reference architecture, prototype roadmap, living methodology, and bibliography/research agenda.

## Source Handling Notes

- The v2 conversation-mining packet strengthens the architecture framing around raw LLMs as semantic-compression engines, planning as a three-horizon control layer, Virtual Context Memory adequacy states, SCF lifecycle governance, evidence bundles, negative-result retention, and the book itself as a governed artifact pipeline. It does not promote any claim to source-derived status.
- `coherence_exchange` is useful for verified epistemic units, verification markets, RAIV-style cost/risk accounting, fork/exit/audit rights, constitutional kernels, Sentinel nodes, and Digital SCIF governance. It also contains explicitly speculative metaphysical language and draft tabs with internal dates after 2026-06-24; treat those as source-text metadata, not verified publication dates.
- `vcm_editable` adds the strongest context architecture refinements: Virtual Context ABI, typed pages/cells, representation certificates, authority non-escalation, protected context compilation, CMMU, snapshots, mounts, taint, deletion closure, and VCM-Bench directions.
- `moecot` remains a must-load authenticated source before implementation-reference claims move beyond argument level. The outline includes a MoECOT chapter so the future writing goal has a precise place to mine it.
- Handoff-only recovery items such as Field of God AI Constitution, Circle Calculus, Genesis Engine/Foundry, and SymLiquid FEP-Net are listed in the outline as recovery queue items, not as existing evidence.
- Conversation-derived author intent should be routed through `appendices/H_author_intent_and_lineage.qmd` and `docs/conversation_context_ingestion_report.md`, not copied verbatim into chapters.

## Evidence Discipline

This pass changed structure and drafting scope. It did not promote any claim support state. All new chapter core claims remain `argument` until sources are turned into source notes or tests/proofs are actually executed.
