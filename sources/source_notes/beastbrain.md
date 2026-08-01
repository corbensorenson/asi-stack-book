# Source Note: BeastBrain Cognitive Architecture

| Field | Value |
|---|---|
| Source ID | `beastbrain` |
| Source title | BeastBrain Cognitive Architecture family |
| Source URL | https://docs.google.com/document/d/1PVLtICJVZm36c6M2y9JkuMZF9nfu_6pyR1SXqFzknME |
| Corpus size | 7,619 lines and approximately 70,206 words |
| Version span | Early unified blueprint and versions 1.0, 2.0, 2.2, 2.3, 2.5, 3.0, 3.1, 3.2, 3.3.1–3.3.4, 3.4, 3.5, 3.9, 4.0, 4.1, 5.0, 5.1, 6.0, and 6.1, including duplicates and architectural reviews |
| Ingestion basis | Complete version-family and section-family audit of `sources/raw/google_docs/beastbrain.txt`; raw text is not published. |
| Complete audit date | 2026-07-31 |
| Variant relationship | `beastbrain_timeless` is a separate export of the v3.3.4 Timeless branch, not independent support. |

## Thesis

### Family-level claim boundary

BeastBrain is a large, rapidly evolving architecture notebook rather than one
implemented system or stable paper. Its durable thesis is that advanced AI is
an operating stack whose cognition, memory, hardware placement, planning,
execution, verification, security, perception, background maintenance,
interfaces, and distributed operation must be designed together. Its organism
metaphor helped expose missing systems and homeostatic loops. The ASI Stack
retains those system boundaries and translates them into typed interfaces,
authority separation, evidence states, and lifecycle records.

The family is not evidence that the proposed stack exists or works. Repeated
“final,” “definitive,” “Gold,” “Platinum,” “Diamond,” “Sovereign,” and “Golden
Master” labels mark drafting stages, not release or qualification states. Most
performance, cost, scaling, security, reliability, context-length, power,
adaptation, autonomy, and verification claims are projections. Many cited
components were described as future or recent work inside a January 2026
narrative and require independent primary-source checking. Pseudocode and
formula-shaped text are design sketches, not executable artifacts or proofs.

The family must be counted once. BeastBrain incorporates or paraphrases
PlanForge, Aletheia, Portia Synapse, TreeLLM, Context Engineer, Ladon/Manhattan,
Talos, Titans, PagedAttention, Mamba, BitNet, Grassmann-flow, and other ideas.
Those embedded summaries do not become independent corroboration for the
underlying papers.

## Version lineage

### Early blueprint through 2.5: the local organism spine

The opening drafts establish the “Fragility Trilemma” of efficiency,
verifiability, and autonomy; contrast a stateless cloud model with a local,
stateful organism; and decompose the system into an operating vessel, SSD-first
memory, verification, planning, Portia navigation, background consolidation,
security, and native interfaces. Later 2.x drafts add explicit hardware modes,
context paging, just-in-time expert loading, intelligence tiers, critical-path
scheduling, Digital SCIFs, and a more complete component diagram.

The earliest block is itself labeled version 8.0 before the document restarts
at 1.0. Later blocks call several different versions definitive. The sequence
is therefore treated as a drafting history inferred from document order, not a
reliable semantic-version release history.

### 3.0–3.3.4: geometric, hardware-adaptive, and multimodal expansion

Version 3.0 introduces Grassmann/DyDiLA “geometric verification” and a sensory
cortex; 3.1 adds GIST-like surprise filtering and a sycophancy activation
probe; 3.2 adds the Mimic hardware-adaptation layer; 3.3.x expands hardware
probing, execution modes, Portia training, semantic deep links, Digital SCIFs,
and validation plans. Version 3.3.4 removes a dated roadmap and becomes the
Timeless branch, with pseudocode for routing, graph scouting, sycophancy
detection, consolidation, and a dangerous manual self-evolution trigger that
artificially amplifies recent loss.

The useful progression is from a fixed architecture diagram to a
hardware-profile negotiation: discover topology and resource constraints,
select among qualified runtime profiles, measure thermal behavior, and shed or
defer background work under pressure. The book does not preserve the source's
hard-coded device modes, claimed sub-five-second adaptation, “panic” mutation,
or assumption that a short thermal burst certifies sustained operation.

### 3.4–3.9: protected power, retention, interfaces, and federation

Version 3.4 adds Ladon blind secret handles, a trusted credential-entry
surface, and late secret injection. Version 3.5 adds a typed graph vocabulary,
the Ouroboros retention/distillation loop, spatial and semantic interfaces, and
eventually BitNet routing. Version 3.9 adds Mycelium: content-addressed artifact
distribution, encrypted communications, collaborative spaces, distributed
service discovery, and an ATP compute-credit economy.

The durable security idea is protected power: the cognitive model should hold
a scoped handle rather than raw credential material, and the actual injection
or signing boundary should be separately mediated. The durable retention idea
is not “infinite memory”; it is a staged lifecycle from raw artifact to
compression, semantic extraction, possible learned candidate, and deletion,
with different fidelity and rights consequences at each transition. The
durable federation idea is that owned devices and specialists can advertise
bounded services and exchange content-addressed artifacts. The book rejects
the claims that an enclave name proves isolation, zeroization proves erasure,
content addressing proves benign content, encryption makes a network
“unstoppable,” CRDT convergence resolves semantic conflicts, or a token economy
solves governance.

### 4.0–4.1: contract-first execution and dependency scheduling

Version 4.0 separates PlanForge as architect from Artificer as implementer. It
defines a box, pipeline, input/output contract, test block, and delegation
sequence. Version 4.1 groups dependency-independent boxes for parallel work and
merges them after local checks. This is the strongest architectural repair in
the later family: plan, implement, and evaluate are distinct roles, and the
critical path rather than raw agent count determines useful parallelism.

The embedded-test idea is retained only as one executable obligation. Tests
written by the planner can be incomplete, wrong, leaked to the implementer,
overfit, or unable to observe integration and external effects. “All tests
green” cannot hide missing requirements, weak oracles, dependency conflicts,
security review, held-out qualification, or rollback. Parallel branches need
isolated state, interface compatibility, shared-resource accounting, merge
validation, conflict handling, and complete failed-attempt denominators.

### Talos review and 5.0–6.1: logistics, maintenance, and governance

The interposed Talos architectural review identifies five BeastBrain gaps:
shared context logistics, offline failure replay, a more explicit routing gate,
immutable/checkpointed evolution, and adversarial review. Versions 5.x and 6.x
fold these into Airlock context handles, Nocturne maintenance windows,
intervention scores, checkpointed candidates, and tribunals. Version 6.1 moves
Mycelium into a central connective-tissue role.

This convergence is valuable lineage evidence: as the stack grew, it needed
immutable identity, shared-state boundaries, explicit update scheduling,
adversarial review, and protected authority rather than only more cognitive
components. But the proposed mechanisms remain underspecified. A raw KV-block
pointer is not a safe or immutable context capability; it needs generation,
source, rights, taint, integrity, lifetime, revocation, tenant, and consumer
binding. An intervention score cannot collapse ambiguity, risk, and historical
failure into one universal weighted sum. A tribunal of related agents is not
independent and consensus is not truth. Idle time is not permission to train.

## Mechanisms

### Durable architecture extracted

### 1. Whole-system and homeostatic design

The organism framing is useful when it forces the architect to ask which
subsystem senses pressure, which regulates it, which state persists, which
component acts, which component checks, and which authority can stop the loop.
The ASI Stack converts the metaphor into separately owned interfaces:

- physical-resource observation and hardware-profile qualification;
- memory, context, cache, and model-state lifecycles;
- planning contracts and dependency graphs;
- bounded implementation workers and tool adapters;
- independent-enough verification and claim adjudication;
- secret and capability mediation;
- perception with provenance and hostile-input treatment;
- background maintenance and training transactions;
- collaborative interface and affected-party control; and
- distributed placement, identity, revocation, recovery, and economics.

No subsystem becomes safe or real because it has an organ name. The system
diagram must expose data, control, authority, evidence, failure, and recovery
flows rather than one attractive vertical chain.

### 2. Hardware-profile negotiation

Mimic contributes the idea that a runtime should identify unified versus
discrete memory, NUMA and transfer topology, supported kernels and precisions,
capacity, bandwidth, thermal behavior, battery state, foreground pressure, and
storage behavior before choosing a model and memory policy. The profile is a
versioned qualification artifact with conservative fallback and expiry. A
probe can narrow execution; it cannot grant data rights or tool authority.

The book adds staged evidence—discovered, smoke-measured, sustained-measured,
and workload-qualified—plus profile-switch hysteresis, committed-state
boundaries, and rollback. Silent precision changes, destructive cache
compression, or driver switching during an external effect are rejected.

### 3. Physical memory hierarchy and residency

BeastBrain correctly separates cheap persistent capacity from scarce working
memory and proposes memory mapping, paging, prefetch, quantization, hot/cold
experts, and storage-backed model or context state. The ASI Stack retains the
capacity opportunity but uses a full I/O roofline: largest indivisible object,
simultaneous working set, cold and warm residency, actual serving tier,
sequential and random reads, transfer path, cache pollution, unused prefetch,
latency tails, energy, endurance, conversion, integrity, recovery, and
qualified useful output.

Storage capacity is not context adequacy or inference speed. `mmap` is an
addressing interface, not a promise of zero physical copies or device access.
PagedAttention manages KV allocation; it does not let arbitrary agents safely
share raw pointers. Distributed ring attention and “infinite context” are
research candidates with network, synchronization, correctness, privacy,
failure, and verification costs.

### 4. Memory forms and controlled consolidation

HelixDB's graph-plus-vector pairing, learned memory, working state, artifact
storage, and cached perception reveal several memory forms that must not be
collapsed. A system needs identity, source, version, temporal validity,
uncertainty, rights, deletion, and dependent-state tracking across exact
artifacts, indexes, summaries, graph assertions, KV state, and weight updates.

Surprise can prioritize review; it cannot authorize learning or distinguish
useful novelty from poison by itself. Test-time or background updates require
an isolated candidate, complete optimizer and RNG state, input-cohort rights,
evaluation, rollback, and explicit promotion. The Timeless pseudocode's
`brain://evolve/self` route, which multiplies loss weights to force updates, is
retained only as a negative example of ungoverned self-modification.

### 5. Retention, compression, and deletion

Ouroboros contributes a staged retention decision, but its scalar score is not
sufficient. User importance, graph centrality, recency, legal hold, safety,
reproducibility, evidentiary value, privacy, cost, and deletion duty are
non-fungible controls. The displayed “time decay” logistic term increases with
elapsed time for ordinary positive parameters, contrary to the surrounding
prose, which is a useful warning against trusting formula labels.

Compression, semantic extraction, learning, and deletion are distinct
transactions. A summary does not preserve every quotation or constraint; a
weight update is not a retrievable record; deleting a file does not erase
copies, backups, indexes, descendants, or SSD flash cells; and `shred -u` is
not a reliable general cryptographic-erasure method on modern SSDs. The book's
context, artifact, privacy, and unlearning chapters own these closures.

### 6. Hybrid cognition and routing

BeastBrain repeatedly routes reflex, procedural, and novel work to different
substrates. The stable idea is substrate-neutral capability routing: choose the
least-authority adequate route under quality, cost, readiness, context,
latency, fallback, and residual constraints. Entropy or a fixed weighted
intervention score is a feature candidate, not a route oracle. Geometric,
state-space, Transformer, symbolic, tool, retrieval, human, and abstention
routes need calibrated eligibility and matched evaluation.

Grassmann or orthogonality invariants can check an exact geometric property.
They cannot prove semantic truth, logical consistency, absence of
hallucination, or “zero false positives” unless a separate refinement argument
connects the property to the claim. A linear sycophancy probe can be one
detector with false-positive, false-negative, drift, gaming, and transfer
measurement; it is not a universal pre-token safety interlock.

### 7. Contract-first planning and execution

The box–pipeline–contract–delegation sequence aligns with the ASI Stack's
intent, plan, job, execution, and evidence boundaries. Its key rule is that the
planner defines interfaces and success obligations before implementation, and
that workers receive bounded work rather than ambient goals. The Lightning
variant adds dependency-aware parallelism and critical-path accounting.

The book strengthens the proposal with assumption and ambiguity records,
forbidden effects, authority and data leases, independent/hidden tests,
integration and adversarial cases, artifact/effect receipts, failed attempts,
merge conflicts, causal attribution, rollback, and residual custody. Passing a
planner-authored test suite cannot be its own evidence gate.

### 8. Protected secrets and effects

Ladon and Manhattan preserve a strong separation: the model should request a
scoped operation or opaque handle, while a trusted component resolves the
secret as late as possible in an isolated effect path. A trusted user-input
surface should be outside model-observable UI and logs. These ideas now live in
Security Kernel, Context Transactions, Runtime Adapters, and Weight Custody.

The “Ignorance Theorem” is rejected. Even when a model never holds the literal
secret, it can misuse the capability, exfiltrate results, influence endpoints,
exploit an adapter, infer secret-dependent behavior, trigger repeated calls, or
observe side channels. Kernel, enclave, eBPF, zeroize, cache partition, and
Digital SCIF labels require threat-model-specific implementation and testing.

### 9. Perception and native interfaces

DOM-plus-rendered-pixel fusion is a useful perception pattern because code and
appearance can disagree. A serious interface retains source identity,
observation time, viewport, accessibility tree, transformations, confidence,
cross-modal conflict, hostile-content status, requested action, and effect
authority. Cached perception is a versioned observation, not offline truth.

Semantic deep links can standardize ingest, recall, connection, and proposal
requests, but URI syntax does not authorize them. In particular, semantic
similarity must never map vague text such as “clean up those logs” directly to
a destructive command. Intent compilation, preview, constrained paths,
approval, effect receipts, and rollback remain mandatory.

### 10. Distributed artifacts, services, and collaboration

Content addressing, peer discovery, local transfer, encrypted messaging,
store-and-forward delivery, CRDT collaboration, service cards, and resource
credits are distinct facilities. The ASI Stack retains them behind identity,
rights, locality, availability, consistency, revocation, provenance, privacy,
economic, and recovery controls. A matching hash establishes byte identity,
not safety, provenance, legality, or currentness. CRDT convergence establishes
a merge property, not semantic correctness. Encrypted messaging still leaks
metadata and endpoint state. Compute credits do not justify resource use,
surveillance, token speculation, or unbounded delegation.

### 11. Maintenance windows and failure replay

Nocturne's durable idea is to schedule replay, counterfactual search, artifact
compaction, dataset proposal, and candidate training during low-contention
windows. These operations have different authority. Idle state is merely a
schedule predicate; it does not license private logs for training, make
model-generated preferences correct, or authorize durable state mutation.

The book adds a `MaintenanceLearningWindow` whose default terminal state is no
mutation. Every sampled failure, excluded trace, search candidate, judge,
dataset transformation, cost, and outcome remains in the denominator.
Candidate updates enter ordinary training, qualification, replacement, and
rollback gates.

## Failure Modes

- Metaphor-to-mechanism substitution and “master edition” maturity theater.
- Version drift, repeated contradictory constants, and double counting.
- SSD capacity presented as interactive speed, verified context, or zero-copy
  execution.
- Future or source-reported hardware features presented as available facts.
- A short microbenchmark treated as a thermal, endurance, or workload
  qualification.
- Destructive panic actions at the moment state and memory are least stable.
- A fixed entropy or intervention threshold used across task, risk, and model
  distributions.
- Test leakage, planner-oracle failure, overfitting, and green-test promotion.
- Parallel-worker shared-state interference and merge/integration omission.
- Geometric property checks or activation probes promoted to semantic truth or
  general safety.
- Related agents counted as an independent tribunal; consensus counted as
  correctness.
- Shared raw pointers, stale handles, cross-tenant KV reuse, and missing
  revocation or generation binding.
- Surprise-driven poisoning, catastrophic forgetting, hidden cross-user state,
  and self-generated preference loops.
- Summary/deletion laundering, backup and descendant survival, and unreliable
  SSD erasure assumptions.
- Secret-capability misuse and side channels despite literal non-disclosure.
- Content-addressed poison, malicious peers, metadata leakage, Sybil behavior,
  economic gaming, and partitioned revocation.
- Semantic command routing that converts ambiguity into destructive effects.
- Benchmarks or projections whose baseline, hardware, denominator, and
  measurement artifacts do not exist.

## Section-family closure ledger

| Source family | Disposition | Canonical manuscript owners |
|---|---|---|
| Early blueprint and versions 1.0–2.5 | Integrated as whole-stack lineage | `asi-is-a-stack-not-a-model`, `the-efficient-asi-hypothesis`, `routing-heads-and-specialist-cores`, and `integrated-reference-architecture`; no hardware or capability result. |
| OS vessel, watchdog, persistence, and hardware modes | Integrated with correction | Personal Hives, Physical Infrastructure, Resource Economics, Context Transactions, Runtime Adapters, and Reliability own qualification, state, and recovery; organism and PID-1 claims are not imported. |
| SSD, paging, JIT experts, Airlock, and ring scaling | Integrated with stronger external comparators | Fast Generation, Virtual Context ABI, Personal Hives, Resource Economics, Routing Heads, and Weight Custody own memory-tier contracts; no infinite-context or zero-copy claim. |
| HelixDB, graph/vector memory, Portia | Integrated and superseded by dedicated sources | Durable Semantic Memory, Virtual Context ABI, Context Transactions, and the TreeLLM/Spider/Portia notes control precise lineage; BeastBrain is not independent support. |
| Titans/GIST/surprise and TTT | Integrated as governed update pressure | Governed Model Training and Replaceable Substrates own input cohorts, mutable state, reset, qualification, rollback, and cross-user risk; no safe continual-learning result. |
| Grassmann/DyDiLA/Mamba/BitNet/hybrid tiers | Integrated as substrate-neutral routing question | Replaceable Substrates, Mathematical Substrates, Fast Generation, and Routing Heads own comparison; geometric truth and efficiency claims are rejected. |
| Aletheia, Geometer, sycophancy probe, Tribunal | Integrated with strict ceilings | Verification Bandwidth, Proof-Carrying Claims, Tribunal, Scalable Oversight, and Interpretability own scoped checks and dependence; no deterministic truth or consensus guarantee. |
| PlanForge, Black Box, Artificer, PyTestEmbed, Lightning | Integrated | Planning, Intent-to-Execution, Labor OS, Runtime Adapters, Executable Specifications, and Artifact Graphs own contracts, workers, tests, effects, merge, and receipts. |
| Context Engineer, Ladon, Manhattan, Aigis, Digital SCIF | Integrated and controlled by dedicated sources | Security Kernel, Context Transactions, Runtime Adapters, Privacy, and Weight Custody own threat models; no isolation or ignorance theorem. |
| Neural Browser, `brain://`, Amorphous, Resonance | Integrated by function | Perception, Human Intent, Human Factors, Runtime Adapters, and Inter-Stack Protocols own multimodal evidence, interface control, URI semantics, and effects; no semantic-command authorization. |
| Ouroboros and SparkStream | Integrated with formula and erasure corrections | Context Transactions, Artifact Graphs, Compression, Privacy, Unlearning, and Resource Economics own retention, fidelity, deletion, descendants, and cost. |
| Mycelium, Spore, Pheromone, Dead Drops, ATP | Integrated by function | Personal Hives, Inter-Stack Protocols, Institutions, Privacy, Security, and Resource Economics own federation, messaging, incentives, rights, and partitions; censorship-resistance and infinite-scaling claims are rejected. |
| Nocturne | Newly integrated as a governed maintenance-learning window | Governed Model Training, Policy Optimization, Procedural Memory, and Recursive Self-Improvement own replay, dataset proposal, updates, qualification, and rollback. |
| Appendices, equations, diagrams, pseudocode, forecasts, and validation plans | Retained as research proposals or negative examples | Exact executable implementations, primary-source checks, matched baselines, adversarial tests, device measurements, and independent evaluation are required; snippets confer no evidence state. |

## Manuscript additions from the second pass

1. `personal-compute-hives-and-federated-edge-intelligence` now turns Mimic's
   hardware handshake into a versioned `HardwareProfileDecision` with staged
   measurement, conservative baselines, expiry, safe profile transitions, and
   no authority expansion.
2. `governed-model-training-distributed-optimization-and-scaling` now turns
   Nocturne into a `MaintenanceLearningWindow` that separates compaction,
   replay, search, dataset construction, and mutation; idle time never grants
   data or update authority.

All other durable mechanisms already have stronger, more precise owners in the
84-chapter manuscript or in the dedicated component-source notes. Adding a
BeastBrain chapter would reintroduce the monolithic architecture that the book
has deliberately decomposed.

## Book Chapters Supported

- `asi-is-a-stack-not-a-model`, `the-efficient-asi-hypothesis`, and
  `integrated-reference-architecture` own the whole-stack lineage.
- `personal-compute-hives-and-federated-edge-intelligence` owns hardware-profile
  qualification and governed distributed placement.
- `governed-model-training-distributed-optimization-and-scaling` owns the
  maintenance-learning window and mutable training state.
- Routing, memory, context, fast generation, substrate replacement, security,
  perception, planning, execution, verification, privacy, unlearning, and
  resource chapters own their corresponding decomposed mechanisms.
- `prototype-roadmap` retains BeastBrain as historical implementation-roadmap
  pressure without treating any edition as a completed phase.

## Claims To Add Or Update

- Add a versioned hardware-profile qualification instead of hard-coded Mimic
  device modes; completed in Personal Compute Hives.
- Add a governed idle-time maintenance-learning transaction instead of an
  autonomous Nocturne loop; completed in Governed Model Training.
- Treat the Timeless export and repeated master editions as variants, not
  corroboration.
- Keep every geometric, infinite-context, zero-copy, security, efficiency,
  power, autonomy, and scaling statement at proposal or explicit non-claim.
- Do not add a BeastBrain chapter; the source's useful content is inherently a
  cross-stack lineage and now has precise canonical owners.

## Open Questions

- Which hardware signals are trustworthy and portable enough for qualification
  without requiring excessive privilege or destabilizing calibration?
- When does background replay improve a candidate over simpler cache, tool,
  retrieval, or policy repairs under the same total lifecycle cost?
- Which shared-state mechanisms can provide real reuse without unsafe pointer,
  tenant, rights, or revocation coupling?
- How should architecture-family versioning preserve supersession and negative
  lessons when successive drafts reuse the same component names?

## Evidence state

`argument` and architecture lineage. The source contains no locally reproduced
BeastBrain runtime, hardware profile decision, SSD-memory benchmark, model
training run, routing study, graph navigator, geometric verifier, security
boundary, perception system, hive, maintenance-learning run, or end-to-end
effect trace. The book's later schemas, fixtures, proofs, project audits, and
external sources are separate evidence and must not be attributed backward to
this paper family.
