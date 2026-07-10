# Source Note: BeastBrain Project

| Field | Value |
|---|---|
| Source ID | `beastbrain_project` |
| Source title | BeastBrain historical AI system project |
| Ingestion date | 2026-07-10 |
| Source version / URL | `local-project:BeastBrain@sha256:60aa8121c11deabf98ff71d848d6709d7208a38be6e2b8789de5a0337f1ef684` |
| Citation label | BeastBrain (2026), pinned local project snapshot |
| Source policy | Local private cache; public-safe note only; raw project tree is not copied into this repository. |
| Ingestion basis | Main whitepapers, current-state/readiness/security/codebase audits, TreeLLM papers and training notes, DKL/Portia/PlanForge/ReasonBrain/memory/SSD/SparkStream/Ladon/Aletheia/tribunal/federation/Mycelium source, structural metrics, and retained build/test logs. Expensive training, hardware, model, network, and full-workspace evaluations were not rerun. |

## Thesis

BeastBrain is the primary currently inspected lineage for the Dynamic Knowledge
Lattice, Portia graph navigation, semantic coordinates, bounded knowledge
snapshots, PlanForge, organism-style background cognition, blind security
handles, and SSD-first resource architecture. Its strongest ASI Stack value is
the combination of ambitious designs with implementation-level negative
evidence showing why interfaces, simulations, feature counts, and readiness
checklists must not be confused with working or validated capability.

## Snapshot posture

The root Git repository has an unborn `main` branch, no commit or tree object,
and 8,697 blob objects. A commit pin is unavailable. The source identity is a
deterministic digest over the 10,483-file current tree excluding the root Git
directory:

`60aa8121c11deabf98ff71d848d6709d7208a38be6e2b8789de5a0337f1ef684`

The project contains 31 crate manifests, 444 Rust source files, and 532 Rust
test attributes across 207 files. At least 129 Rust files contain an explicit
TODO/FIXME/placeholder/stub/mock/simulation marker. These counts establish
surface breadth, not integration or capability.

## Mechanisms

### Durable memory and representation

- Typed graph-plus-vector Dynamic Knowledge Lattice for durable semantic
  objects, facts, tools, user memory, provenance, and relations.
- Portia small-model architecture for predicting edge type, semantic
  destination, confidence, and navigation path.
- Bounded graph snapshots with node/depth/edge/weight limits and reasoning-path
  capture.
- Thirty-two-byte semantic-token proposal combining a 128-bit coordinate,
  flags/header, and residual.
- Hot/cold/archive/merged/deleted memory states with background decay,
  similarity merge, archive, and promotion.
- Episodic memory that gives unresolved and abandoned outcomes elevated
  salience.
- Recursive/fractal multiscale summarization and external-knowledge/small-
  navigator separation.

### Planning, routing, and execution

- PlanForge task DAGs, dependency types, parallel groups, critical path,
  early/late times, slack, multi-objective scheduling, and contracts.
- Tool primitives with parameters, preconditions, effects, tier, duration,
  confirmation, reversibility, and retry limits.
- Risk-scaled routing across reflex, standard, deep, and savage expert tiers.
- Sparse top-k router, token-level knowledge sharding, and disk-loaded expert
  designs.
- Context airlocks and blind/recent/tagged/full disclosure policies.

### Resource architecture

- Memory-mapped tensors, SSD-resident optimizer state, on-demand expert
  loading, and bounded RAM caches.
- Hybrid tiled attention, ring attention, hot/warm/cold hierarchical KV,
  asynchronous layer loading, and prefetch designs.
- Storage-pressure/autophagy and hardware-aware target-selection concepts.

### Governance, security, and collaboration

- Aletheia/Talos contract-first risk gating, active epistemics, tribunal, and
  premortem framing.
- Ladon/Aigis blind secret handles and SCIF-like execution framing.
- Synaptic capabilities that decay when unused and strengthen through use.
- SparkStream background cognition, dream, circadian, and memory-maintenance
  loops.
- Federated LoRA round/update types, privacy and secure-aggregation interfaces.
- Mycelium signed P2P transport, content-addressed spore framing, and ATP
  resource-economy framing.

## Evidence

- Portia's current public navigation uses vector entry plus bounded BFS rather
  than the intended neural navigation path; its parameter count is a
  placeholder.
- Multiple incompatible edge ontologies coexist, ranging from a small DKL enum
  to 59-edge and 64-built-in registries.
- Memory merge concatenates content and averages embeddings without a complete
  append-only provenance/supersession transaction.
- The correction learner uses character-set similarity, which is not a safe
  semantic applicability test.
- “Titans” test-time memory uses semantic distance as a simulated gradient and
  applies a uniform toy weight update.
- The trainable sparse router computes a loss but does not mutate its weights.
- GNN prefetch falls back to neighbor selection and has no training update.
- Fractal memory is in RAM, uses zero embeddings, ignores the query, and can
  emit placeholder summaries.
- SSD training and inference benchmark paths use synthetic loss, gradients,
  cache hits, delays, and derived baselines. They are simulations, not model or
  hardware results.
- Secret permissions are metadata rather than demonstrated retrieval
  enforcement; SCIF execution is not process/VM/WASM isolation.
- Tribunal/Veritas paths contain default-success and stub behavior rather than
  demonstrated falsification or independent review.
- Federated secure aggregation, signatures, distinct-node admission, and
  alternative algorithms are incomplete.
- Mycelium has meaningful signed transport plumbing but not complete content
  admission, stable identity, Merkle verification, or a trusted economy.

### Source-reported negative results

These are project-reported and were not reproduced:

- TreeLLM reports 29/29 Q&A, 122/130 SOTA, 196/220 Advanced, 144/168 Super,
  85/283 Medical, 0/20 HLE, 37/56 Inference, and 18/33 Extended.
- Other diagnostics report zero percent negation performance, limited
  numerical reasoning, domain gaps, and coordinate prediction near 40%.
- SpiderSynapse remained near loss 0.57, accuracy 68–70%, and coordinate
  alignment 0.5621 without a learning trend after hours.
- A Metal non-contiguous tensor path produced zero-loss/zero-accuracy behavior;
  copying through CPU into a fresh GPU tensor restored correctness with a major
  speed penalty.

### Retained build evidence

Project logs dated 2025-12-28 through 2026-02-02 preserve compiler failures in
brain RAG, LLM quantized inference, DKL/Portia integration, SparkStream,
Amorphous, emulator, and kernel integration. Later test logs show only two or
three filtered Amorphous tests with 54 filtered out. The current mining attempt
could not compile because dependencies were unavailable offline and network DNS
failed. No claim is made about which historical compiler failures remain live.

## Claims To Add Or Update

1. Add durable semantic memory as a distinct substrate between model weights,
   prompt context, claim ledgers, and procedural memory.
2. Add an address-plus-residual contract for semantic coordinates.
3. Add certified bounded subgraph snapshots as the durable-memory/context
   bridge.
4. Require a canonical versioned edge ontology and migration receipts.
5. Require append-only provenance through merge, supersession, forgetting, and
   rollback.
6. Treat unresolved failure and corrections as positive retention signals.
7. Require parameter-change and fixed-probe route-change evidence before
   calling a router trained.
8. Require per-path credit diagnostics and a one-path ablation for branching
   learners.
9. Add tensor layout/device/backend identity to benchmark lineage.
10. Label simulated, synthetic, measured, and reproduced fields separately.
11. Require cancellation-safe resource leases and no-progress detection for
    paging/prefetch systems.
12. Distinguish security handles from broker enforcement and hard isolation.
13. Require tribunal independence, falsification, abstention, dissent, and
    uncertainty-preservation tests.
14. Add architecture surface area, duplicate subsystems, warnings, and open
    integration gates to the growth guard.

## Book Chapters Supported

Primary destinations:

- proposed `durable-semantic-memory-and-knowledge-lattices`
- `routing-heads-and-specialist-cores`
- `planning-as-a-control-layer`
- `resource-economics-and-token-budgets`
- `benchmark-ratchets-and-anti-goodhart-evidence`
- `readiness-gates-residual-escrow-and-quarantine`
- `security-kernel-and-digital-scifs`
- `artifact-steward-agents-and-living-project-governance`

Secondary destinations:

- `system-boundaries-and-authority`
- `virtual-context-abi`
- `context-transactions-snapshots-mounts-and-taint`
- `claim-ledgers-and-belief-revision`
- `procedural-memory-and-cognitive-loop-closure`
- `compact-generative-systems-and-residual-honesty`
- `rankfold-neuralfold-and-artifact-compression`
- `intent-to-execution-contracts`
- `runtime-adapters-tool-permissions-and-human-approval`
- `fast-generation-architectures`
- `policy-optimization-and-learning-from-feedback`
- `data-engines-continual-learning-and-unlearning`
- `personal-compute-hives-and-federated-edge-intelligence`
- `constitutional-alignment-substrate`
- `spinoza-verification-and-proof-carrying-claims`
- `scalable-oversight-and-adversarial-ai-control`
- `recursive-self-improvement-boundaries`
- `open-ended-improvement-engines`
- `evidence-states-and-claim-discipline`
- `capability-thresholds-and-deployment-commitments`
- `ai-supply-chain-integrity-and-lifecycle-provenance`

## Chapter-boundary decision

The project supplies primary provenance for a likely new chapter, **Durable
Semantic Memory and Knowledge Lattices**. The boundary remains provisional
until BugBrain, Corben's Trainer, Corben's Best Model Possible, and any newly
unzipped projects are mined and independent external literature is ingested.
No manifest change is authorized by this source note alone.

## Failure Modes

- Treating an interface/type as a working capability.
- Treating simulated I/O activity as model training or inference evidence.
- Counting toy or internally authored suites as general capability.
- Letting multiple edge ontologies silently reinterpret durable knowledge.
- Merging or pruning memory without immutable lineage and appeal.
- Calling a router trainable when its parameters do not change.
- Using the same model as generator and independent judge.
- Punishing uncertainty as a critique violation.
- Treating signed transport as trusted content.
- Letting activity strengthen compromised authority.
- Treating a prose constitution as protected enforcement.
- Using feature counts or percentage readiness to override open compiler,
  integration, hardware, security, or benchmark gates.

## Open Questions

- Which exact BeastBrain files/symbols were ported into CCA and then compiled
  into MoECOT mechanisms?
- What independent literature best bounds DKL, graph RAG, learned graph
  navigation, and long-term agent memory claims?
- Which retained build errors are repaired in the hashed snapshot?
- Are any benchmark datasets, checkpoints, or run environments retained
  elsewhere with enough lineage for replay?
- Does any later project implement real Portia neural navigation, secure secret
  brokering, federated aggregation, or persistent tier indexes?

## Non-claims

- Does not claim BeastBrain achieved AGI, ASI, production readiness, safe
  autonomy, factual verification, secret isolation, secure federation, or
  deployed constitutional enforcement.
- Does not reproduce TreeLLM, SpiderSynapse, SSD, attention, routing, memory,
  security, hardware, mobile, XR, network, or performance results.
- Does not treat a source file, test attribute, design table, or feature count
  as proof that the named capability works.
- Does not treat the tree digest as a Git commit, signed release, or authorship
  attestation.
- Does not promote an ASI Stack support state.
- Does not authorize publication of the raw private project tree.
