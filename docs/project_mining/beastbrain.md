# Project Mining Dossier: BeastBrain

Date opened: 2026-07-10
Project source: local private worktree, read-only for idea mining
Snapshot identity:
`sha256:60aa8121c11deabf98ff71d848d6709d7208a38be6e2b8789de5a0337f1ef684`
Git state: unborn `main` branch; no commit or tree object exists
Source policy: public-safe notes only; raw project files remain outside this
repository

BeastBrain is the earliest currently inspected implementation lineage for the
Dynamic Knowledge Lattice (DKL), Portia navigation, SSD-first memory, PlanForge,
organism-style background cognition, and several later CCA/MoECOT mechanisms.
It is also an unusually useful failure archive. Ambitious whitepapers, broad
interface coverage, partial real implementations, simulations presented as
validation, contradictory readiness audits, and retained compiler logs all
coexist in one tree.

This dossier keeps five evidence classes separate:

1. a mechanism described in a whitepaper;
2. a Rust type or interface present in source;
3. an implementation that performs the named operation;
4. a test or retained artifact that exercises that implementation;
5. a reproduced capability, performance, security, or safety result.

BeastBrain has substantial material in the first three classes, scattered
evidence in the fourth, and no fifth-class result established by this book
work.

## Snapshot and repository posture

The root Git directory is not a usable history. `HEAD` is unborn, every visible
file is untracked, and the object database exposes 8,697 blob objects but no
commit or tree objects. Nested unborn Git directories exist under the kernel,
mimic, and sensory crates. A commit pin would therefore be fictitious.

The replacement identity is a deterministic digest over the 10,483-file local
tree, excluding only the root `.git` directory. The sorted path-and-content
manifest hashes to:

`60aa8121c11deabf98ff71d848d6709d7208a38be6e2b8789de5a0337f1ef684`

This digest includes nested project metadata and retained logs. It identifies
the inspected state; it does not establish authorship, provenance continuity,
or release integrity.

The tree contains 31 crate manifests and 444 Rust source files. A source count
over the current crates found 532 Rust test attributes across 207 files. That
is breadth, not suite closure. At least 129 Rust files contain one or more
`TODO`, `FIXME`, placeholder, stub, mock, or simulation markers, with 280
marker-bearing Rust lines in total.

Approximate Rust lines by major crate include:

| Crate | Approximate Rust lines |
|---|---:|
| `beastbrain-core` | 43,573 |
| `beastbrain-brain` | 19,896 |
| `beastbrain-amorphous` | 17,164 |
| `beastbrain-emulator` | 9,639 |
| `beastbrain-storage` | 5,643 |
| `beastbrain-training` | 5,036 |
| `beastbrain-llm` | 4,568 |
| `beastbrain-dkl` | 4,425 |
| `beastbrain-resonance-term` | 3,951 |
| `beastbrain-api` | 3,559 |
| `beastbrain-mobile` | 3,255 |
| `beastbrain-whitecell` | 2,961 |
| `beastbrain-personality` | 2,828 |
| `beastbrain-flasher` | 2,801 |
| `beastbrain-planforge` | 2,748 |
| `beastbrain-reasonbrain` | 2,184 |
| `beastbrain-synapse` | 1,926 |
| `beastbrain-critique` | 1,863 |
| `beastbrain-skills` | 1,816 |
| `beastbrain-cli` | 1,593 |
| `beastbrain-knowledge` | 1,548 |
| `beastbrain-orchestrator` | 1,334 |
| `beastbrain-sparkstream` | 1,254 |

The root workspace member list repeats critique, emulator, kernel, and mimic.
The codebase audit reports 23 duplicate types, 15 overlapping stores/caches,
164 configuration types, and 66 stubs. These are not merely cleanup trivia:
they show how an architecture can accumulate more control surfaces than it can
keep semantically aligned.

## Primary material inspected

- `README.md`, `INTERNAL_MANIFEST.md`, `docs/CURRENT_STATE.md`, and the main
  whitepaper families.
- `docs/CODEBASE_AUDIT.md`, `docs/PRODUCTION_READINESS_AUDIT.md`,
  `docs/SECURITY_AUDIT.md`, `SSD_AUDIT_SUMMARY.md`, `docs/CLEANUP_PLAN.md`, and
  `docs/REDUNDANCY_LIST.md`.
- `docs/beastbrain.md`, `docs/ssd_first_architecture.md`, the two SSD ADRs, and
  the v6.1 architecture paper.
- `examples/treellm notes/WHITEPAPER.md`, the v6 personal architecture paper,
  training notes, API notes, and archived TreeLLM papers.
- DKL graph, storage, ontology, knowledge, embedding, and Portia source.
- PlanForge DAG, schedule, contract, risk, and airlock source.
- ReasonBrain expert, routing, graph, inference, quantization, and airlock
  source.
- Core episodic memory, semantic consolidation, correction learning, neural
  memory, federated learning, synaptic capability, canonical type/store, and
  research-agent source.
- SSD tensor, disk optimizer, hybrid/ring/hierarchical attention, async weight
  loading, token knowledge routing, trainable routing, GNN prefetch, fractal
  memory, and SSD-training source.
- SparkStream salience, dream, processing, optimization, and DKL integration
  source.
- Ladon/Aigis secret-handle and isolation source; Aletheia, critique, Veritas,
  tribunal, and adversary source.
- Mycelium networking/spore/ATP source and kernel autophagy source.
- Retained build/check/test logs dated from 2025-12-28 through 2026-02-02.
- A current `cargo check --workspace --all-targets` attempt, which could not
  reach compilation because required registry packages were not locally
  cached and network DNS was unavailable. An offline attempt stopped on the
  missing `axum` package. `cargo fmt --all -- --check` parsed the Rust sources
  but found extensive formatting drift.

Expensive training, model downloads, hardware tests, network tests, mobile/XR
tests, and benchmark suites were not rerun.

## Architecture mined for the book

### 1. Durable semantic memory is distinct from prompt context

BeastBrain's DKL treats long-lived knowledge as typed graph state, not as a bag
of prompt chunks. Nodes can represent text, facts, tools, user memories, and
other semantic objects. Edges express causal, temporal, evidential, taxonomic,
procedural, and associative relations. Vector similarity supplies candidate
retrieval while graph traversal supplies structure and explanation.

The book currently owns nearby concerns in the Virtual Context ABI, claim
ledgers, and procedural memory. None cleanly owns the durable semantic substrate
itself. The distinction should be explicit:

- durable semantic memory stores identity, content, type, relations,
  provenance, revision, and access policy;
- context materialization selects a bounded view for one cognitive operation;
- a claim ledger governs epistemic support and revision;
- procedural memory stores executable or routable know-how;
- model parameters encode statistical competence but are not the authoritative
  record of a particular fact or relationship.

This is BeastBrain's strongest candidate for a new book chapter boundary.

### 2. Semantic coordinates can act as a compact routing address

The TreeLLM design proposes a 32-byte semantic token containing a 128-bit
coordinate, flags/header material, and a residual. The coordinate locates a
concept region in the lattice; the residual carries local information not
captured by the address.

The important book idea is not the exact byte count. It is an **address plus
residual contract**:

- the address must have declared locality semantics;
- aliases and collisions must be measured;
- reconstruction or retrieval must disclose residual dependence;
- coordinate drift must be versioned with the basis/index;
- a compact address must never be described as the knowledge itself.

The TreeLLM papers candidly report that their HLSH coordinate is character-
level rather than truly semantic: `dog` and `canine` remain separate without an
explicit edge. That limitation is precisely the residual-honesty lesson the
book needs.

### 3. Learned navigation should predict relation and destination

Portia is designed as a small navigation model with scout, focus, refinement,
coordinate, edge-type, and confidence heads plus working memory. Its intended
job is narrower than answer generation: given an intent and the current graph
state, choose what kind of edge to traverse and where to go next.

This supports a strong routing principle: keep high-dimensional world
knowledge external, and train a smaller model to navigate it. A navigation
output should contain at least:

- current semantic position and target intent;
- candidate relation distribution;
- predicted destination/region;
- confidence and stop/escalate decision;
- visited path and rejected alternatives;
- a fallback retrieval route.

The current Portia implementation does not establish this vision. Its public
navigation path performs vector entry followed by bounded breadth-first search
to depth three, scores with a symmetric KL-like measure, and uses a threshold.
The neural `forward` path is not what drives graph traversal. The reported
parameter count is a hard-coded five-million placeholder, and DKL navigation
falls back to vector search. The book should preserve the architecture while
describing the implementation as a heuristic baseline.

### 4. Bounded knowledge snapshots are a safer context interface

The DKL snapshot design selects a subgraph with explicit maximum depth, maximum
node count, edge filters, minimum weights, and a recorded reasoning path. This
is better than dumping arbitrary nearest-neighbor chunks into a prompt.

The book should define a semantic snapshot certificate containing:

- source graph/version watermark;
- root intent and entry nodes;
- node/edge budgets and filters;
- provenance and policy filters;
- omitted-frontier summary;
- traversal path and stopping reason;
- staleness/expiry and invalidation behavior.

This should connect a future durable-memory chapter to the Virtual Context ABI.

### 5. One edge ontology must be canonical

BeastBrain contains several incompatible relation systems:

- the DKL graph has a small enum of roughly thirteen edge kinds plus a generic
  relation;
- storage types expose a larger relation enum;
- the storage ontology describes a 59-edge scheme plus custom relations;
- the dynamic registry describes 64 built-ins and custom IDs from 256 upward.

This is a concrete ontology-drift case. A typed graph cannot be trusted merely
because every crate uses an enum. The book should require:

- one canonical edge identifier registry;
- versioned aliases and migrations;
- an unknown/custom quarantine path;
- validators at serialization and API boundaries;
- edge semantics, directionality, inverse, transitivity, and confidence rules;
- migration receipts proving that stored graphs were not silently retyped.

### 6. Provenance must survive memory merge and forgetting

The DKL fact shape can carry sources, and semantic memories can record source
memory IDs. However, source lists are optional, facts can begin with no sources,
and the consolidation layer merges text by concatenation and averages
embeddings. It removes the losing node from the hot map and vector index.

That is not enough for evidence-bearing memory. A safe merge needs:

- immutable parent IDs and source spans;
- a declared merge operator;
- contradiction handling rather than unconditional concatenation;
- an auditable new embedding/version;
- supersession rather than destructive disappearance;
- rollback and replay from parents;
- downstream invalidation when a parent source is retracted.

Later CCA append-only supersession is a clear evolution beyond this BeastBrain
implementation.

### 7. Failure and unresolved outcomes deserve retention weight

Episodic memory assigns higher outcome weight to unresolved and abandoned
interactions than to resolved ones. This is a valuable anti-survivorship idea:
failures, user frustration, and incomplete work should not be forgotten simply
because they are unpleasant or infrequently accessed.

The mechanism needs refinement. Emotional valence is detected by a small
keyword list, and retrieval is keyword matching. The code comment says results
are ranked by recency and salience, but the implemented score discounts
frequently accessed episodes and does not calculate recency. Still, the core
book rule is sound: **memory utility is not the same as positive sentiment**.
Retention policies should explicitly preserve unresolved failures, corrections,
near misses, and contested outcomes.

### 8. Memory consolidation is a policy-bearing state transition

The semantic memory store has hot, cold, archived, merged, and deleted states;
importance signals combine base value, access, recency, and feedback; a
background loop decays, merges, archives, and promotes memories.

This is a useful state-machine skeleton, but the implementation exposes several
requirements the book should make explicit:

- every transition needs a receipt and previous-state pointer;
- merged/archived records must remain resolvable for replay;
- vector-index mutation and record mutation must be atomic or recoverable;
- promotion from cold must persist updated access/importance;
- merge detection must prevent cascading semantic drift;
- forgetting must be policy-, privacy-, and evidence-aware;
- a memory store must survive restart with tier indexes intact.

The current source inserts a new vector twice, contains duplicated merge
comments, leaves archive-layer Vault updates as intent-only comments, and does
not preserve a robust append-only transition ledger. These are useful failure
examples, not reasons to discard the tiered design.

### 9. Correction memory must match semantics, not character sets

The correction learner records original, corrected, context, category, and an
`applied` field. It extracts the first 100 lowercased characters as a pattern,
then uses Jaccard similarity over the *set of characters* for approximate
matching.

That can apply an unrelated correction to text that merely uses similar
letters. The `applied` flag is never updated. The book should require correction
rules to bind:

- normalized intent/task context;
- the exact faulty span or structured output field;
- correction type and scope;
- applicability predicates and counterexamples;
- source/user authority;
- version and expiry;
- application receipts and rollback;
- evaluation against held-out similar-but-not-applicable cases.

### 10. Test-time learning must be honest about what is being trained

The `TitansMemory` interface is framed as neural long-term memory and
gradient-informed retention. The current implementation uses semantic distance
between input and prediction as a proxy for surprise, derives a simulated
gradient magnitude, and subtracts the same scalar from every element of a
128-value weight vector. The HelixDB field is not used to store the event.

This yields a sharp book rule: an adaptive state blob, a surprise score, and a
hash change do not establish neural test-time learning. A credible test-time
learning record needs the objective, differentiable parameters, optimizer,
gradient path, pre/post evaluation, interference test, rollback, and retention
scope.

### 11. Tools need declarative preconditions, effects, reversibility, and cost

BeastBrain's `ToolPrimitive` includes parameters, preconditions, effects,
estimated tier, duration, confirmation requirement, reversibility, and retry
limits. This is an important precursor to the book's command-contract and
runtime-adapter work.

The book should retain the shape but strengthen it with authority principal,
resource scope, idempotency, compensating action, evidence output, timeout,
side-effect digest, secret policy, and human-approval receipt.

### 12. Planning belongs in a typed DAG with explicit slack

PlanForge models tasks, dependency kinds, parallel groups, critical-path early
and late times, slack, multi-objective cost/time tradeoffs, and tier routing.
Contracts declare inputs, outputs, signatures, genetic tests, and status.

These mechanisms directly support the current planning chapter. They make
parallelism, bottlenecks, and replanning visible instead of hiding them in a
language-model transcript.

The implementation is uneven. The scheduler optimizer is largely a sort by
start time, risk formulas differ across papers and source, and several advanced
claims are design-only. The book should require every quantitative risk or
intervention formula to have one versioned owner, calibrated inputs, monotonic
expectations, and a migration record when the formula changes.

### 13. Context airlocks need integrity and least disclosure

PlanForge and ReasonBrain both propose handles that let modules refer to large
contexts without receiving the entire payload. Context policies include full,
recent, tagged, and blind views. This is a strong least-disclosure pattern.

The implementations do not yet establish zero-copy or isolation. One uses a
simulated pointer (`0xDEADBEEF`) and zero checksum; another stores strings in a
map, returns cloned strings, and uses a zero checksum. The book should define a
real context handle as a capability with:

- immutable blob/version identity and authenticated digest;
- authorized operations and view policy;
- byte/token length and schema;
- owner, grantee, expiry, revocation, and delegation rules;
- taint and secret labels;
- access receipts;
- no ambient dereference outside the airlock service.

### 14. Risk-scaled intelligence should choose the least capable adequate path

ReasonBrain calculates an intervention score from ambiguity, risk, and failure
rate, then limits allowed expert tiers. This is an early form of intelligence
arbitrage: reflex for low-risk work, deeper experts for harder or riskier work.

The current `route_with_intervention` does not actually compare cost or
adequacy; it filters tiers and token-matches experts. Load balancing can add
enough score to a zero-match expert to approach the routing threshold. The
book's stronger rule should be:

`select the lowest-authority, lowest-cost route that passes an explicit
adequacy and readiness predicate; otherwise escalate or refuse.`

The score inputs themselves need provenance. An unexplained numeric risk value
cannot authorize a deeper or more powerful route.

### 15. A trainable router must actually update its parameters

The sparse router computes logits, softmax probabilities, top-k experts, and
usage statistics. It buffers reward examples and calculates a policy-gradient-
like loss. However, the resulting tensor update is never applied to router
weights; only the training-step statistic changes. Expert embeddings are
unused, entropy is never populated, and the auxiliary coefficient is not
applied.

This is a canonical interface-versus-effect test for the routing chapter:

- prove that parameters changed;
- prove the saved artifact contains the changed parameters;
- show route changes on a fixed probe set;
- compare task utility, cost, balance, and safety before/after;
- keep a no-learning control;
- reject a router whose reward rises while external task quality falls.

### 16. Token-level knowledge routing needs more than a batch wrapper

The knowledge router stores topic shards, running centroids, length-prefixed
facts, a small RAM LRU, and per-token routing results. The batch method simply
calls the query-level router for each embedding. Configured shard count and
maximum shard size are not enforced.

The book-worthy architecture is hierarchical retrieval:

`token/intent -> shard candidates -> fact candidates -> graph expansion ->
evidence filter -> context snapshot`

It needs source/conflict policy, shard rebalance, centroid drift handling,
crash-consistent metadata, maximum-size enforcement, and recall/latency
benchmarks against whole-corpus search.

### 17. SSD-first memory is a resource architecture, not a capability claim

BeastBrain explores memory-mapped weights, SSD optimizer state, hot/warm/cold
KV tiers, append-only RAG documents, disk-loaded experts, tiled attention,
ring attention, asynchronous layer loading, prefetch, and storage-aware target
selection.

The central book idea is sound: design around a declared RAM budget and make
resident state, paged state, prefetch, eviction, and I/O cost observable.
However, statements such as “one million tokens,” “train seven billion
parameters on a laptop,” or large power/throughput gains are projections unless
matched model runs and baselines exist.

### 18. Tiered KV requires crash consistency and promotion accounting

The hierarchical KV cache provides an instructive incomplete implementation:

- hot entries use an in-memory LRU-like order;
- warm entries use a preallocated memory-mapped file;
- cold entries use per-position f16 files;
- stride detection proposes prefetch positions.

But warm position maps are not persisted, promotion can discard the hot entry
evicted by the promotion, clearing resets only hot state/statistics while lower
tiers remain, overwrites inflate total-token count, cold capacity is reported as
effectively unlimited, and a negative stride can wrap to a huge unsigned
position.

The book should require a tier ledger, durable indexes, bounded capacity,
atomic promotion/demotion, generation IDs, tombstones, restart tests, and
quality-aware compression.

### 19. SSD tensor APIs need progress guarantees

`MmapTensor` and `DiskAdamW` contain real file I/O and Candle tensor operations,
but important gaps remain:

- the `mmap` field is not used as a persistent map;
- tensor creation always converts through f32 even when metadata names another
  dtype;
- a tensor larger than the cache budget can make eviction loop without
  progress;
- the safetensors loader never populates its cache, so `get` cannot find a
  named tensor;
- optimizer step counters are not persisted;
- state writes are not atomic;
- normalized parameter filenames can collide.

The reusable lesson is a general systems invariant: every paging loop needs a
detectable no-progress state and a fail-closed oversized-item route.

### 20. Async I/O needs cancellation-safe accounting

The “async mmap” implementation performs asynchronous buffered reads rather
than memory mapping. Concurrent callers can duplicate loads. The concurrency
counter increments before file operations but is not decremented on all error
paths, which can permanently consume a slot; a zero concurrency limit waits
forever. Missing layer weights return empty vectors rather than a required-
parameter error.

Book addition: resource leases must be acquired with RAII/cancellation-safe
guards, released on every outcome, reject zero capacity, and distinguish
optional from required artifacts.

### 21. Prefetch intelligence needs a baseline and realized-hit metric

The GNN prefetcher defines graph-convolution layers but leaves the model
uninitialized. Prediction returns the first neighboring node IDs, and training
does nothing. This is a useful minimum baseline masquerading under an advanced
name.

The book should always compare a learned prefetcher to sequential, stride,
neighbor, recency, and no-prefetch baselines. Report precision, coverage,
wasted bytes, realized latency savings, cache pollution, and energy—not only
predicted next-node accuracy.

### 22. Recursive summarization must preserve drill-down and residuals

Fractal memory recursively groups items and optionally asks an LLM for a
summary. Without an LLM it emits metadata placeholders; embeddings are all
zeros, storage is in RAM, query text is ignored, and retrieval returns every
level-one summary. At maximum depth it clears the buffer but retains nodes,
which is neither bounded storage nor explicit archival.

The concept still belongs in long-horizon memory if strengthened with source
children, summary model/version, coverage, residual/exception records,
contradiction checks, query-aware traversal, and regeneration tests.

### 23. Ring and tiled attention need numerically stable global accounting

Hybrid tiled attention uses an online-softmax pattern and is closer to a real
bounded-memory implementation. Ring attention instead exponentiates and clips
individual scores without a global max, which can distort normalization; a
zero tile size can also make stepped iteration fail. Cross-ring summaries use
the same value for summary key and value.

The book should demand equivalence tests against dense attention on small
inputs, adversarial numeric ranges, boundary positions, restart behavior,
quality-versus-I/O curves, and exact accounting for summary approximation.

### 24. A simulated training curve is not convergence evidence

The SSD training validator creates deterministic files, generates a
mathematically decreasing synthetic loss, writes a small synthetic gradient,
and rewrites unchanged weights. It calls a greater-than-ten-percent decline
“convergence verified.” The RAM baseline is created by multiplying throughput
by 1.5 and loss by 0.98.

The LLM inference benchmark likewise sleeps per token, samples a synthetic 90%
cache hit, and reports throughput and SSD reads. These should be described as
I/O harnesses, never model benchmarks.

Book rule: simulated quantities must be schema-labeled at the field level and
cannot satisfy measured-evidence gates.

### 25. Benchmark code can create benchmark theater

The “standard evaluation” has three toy tasks. Code generation receives partial
credit if output contains code-like keywords rather than passing tests.
“Semantic similarity” is word-set Jaccard overlap. Reasoning receives partial
credit for any attempt, category weights are ignored, and category scores only
repeat overall score.

This is a concrete anti-Goodhart example. A benchmark-shaped API, polished
report, and aggregate score are not a valid evaluation unless task provenance,
scoring semantics, negative controls, execution, and baseline comparability are
real.

### 26. TreeLLM supplies valuable negative training evidence

The TreeLLM record reports strong results on some internal suites but severe
gaps elsewhere. Source-reported results include:

| Suite | Source-reported result |
|---|---:|
| Q&A | 29/29 |
| SOTA | 122/130 |
| Advanced | 196/220 |
| Super | 144/168 |
| Medical | 85/283 |
| HLE | 0/20 |
| Inference | 37/56 |
| Extended | 18/33 |

The project also reports zero percent negation performance in one diagnostic,
limited numerical reasoning, domain gaps, and coordinate prediction near 40%.
These figures were not reproduced and the suites are not independent external
evidence.

More important is the retained SpiderSynapse failure: loss remained around
0.57, accuracy around 68–70% without a learning trend, and coordinate alignment
around 0.5621 after hours. The source hypothesizes gradient dilution across four
hypotheses and three refinement iterations, route collapse, loss imbalance, and
context conversion issues. Its proposed response—reduce to one path, log
gradients, isolate coordinate loss, and compare a DKL-aware baseline—is sound.

Book addition: branching deliberation during training can dilute credit. Every
multi-path learner needs per-path gradient/advantage accounting and a one-path
ablation.

### 27. Tensor layout is an experimental variable

The TreeLLM training notes record a Metal failure in which a sliced tensor had
the expected shape but a non-contiguous layout, producing zero loss/accuracy.
Copying through CPU into a fresh GPU tensor restored correctness but made
training dramatically slower.

This deserves a general benchmark-truth rule: shape equality does not establish
layout or backend equivalence. Retain device, dtype, strides/contiguity, copy
path, kernel, and backend version in training lineage.

### 28. Background cognition needs bounded autonomy and independent judges

SparkStream models stochastic “sparks,” circadian states, working memory,
dreaming, and optimization. The architecture is useful as a vocabulary for
opportunistic background work, but the current runtime often emits hard-coded
phrases and entropy-seeded random events. Salience uses placeholder intensity,
and a processor hard-codes insight confidence and timing values.

The dream loop uses the same brain as generator and judge, parses a float with a
0.5 fallback, and persists insights above 0.7. This is not independent
verification. The optimizer can delete traces and decay/prune graph edges in
place without a provenance ledger, replay, or appeal path.

The book should allow background cognition only under explicit work budgets,
reproducible event identity, independent or diverse verification for promotion,
quarantine before durable writes, and reversible memory maintenance.

### 29. Secret handles are useful, but handles do not create isolation

Ladon/Aigis models blind handles, secret metadata, permissions, persistence,
and a SCIF-like execution wrapper. The current secret retrieval path does not
enforce permissions; permissions remain metadata. The SCIF is a blocking task,
not process, VM, WASM, or kernel isolation. Raw secrets are substituted into
URLs and headers, and the source notes that the HTTP client does not guarantee
zeroization.

The “Ignorance Theorem” is therefore an aspiration. The book should require
secret use through a brokered operation API where callers submit a permitted
operation and receive only the result, with hardware/process isolation where
the threat model requires it.

### 30. Permission decay can reduce or increase attack persistence

Synaptic capabilities decay when unused and strengthen when used. The
least-privilege intuition is interesting: dormant authority should expire.
But repeated malicious use also strengthens a compromised capability.

Additional implementation issues matter:

- policy config defaults are not applied when a capability is granted;
- checks use exact path/string equality without normalization or containment;
- wall-clock subtraction can misbehave if time moves backward;
- the manager is not demonstrated as an enforcement point around effects;
- tests do not simulate time.

The book should keep hard expiry and explicit revocation authoritative.
Activity may refresh a lease only within policy bounds; it should never create
more authority merely through use.

### 31. Constitutional prose must compile into enforcement

The internal manifest declares immutable primitives and read-only
constitutional state, but it is a prose file without cryptographic or OS-level
enforcement. Aletheia's contract lock hashes an exact clarification string;
this detects byte changes, not semantic drift. Gating is keyword and metadata
heuristics. The geometric verifier checks matrix properties, not factual truth.
The sycophancy probe begins as a constant vector stub.

The book should explicitly distinguish:

- a stated constitution;
- a typed, versioned policy;
- a compiled enforcement rule;
- a protected enforcement mechanism;
- an adversarial test demonstrating that bypass attempts fail.

### 32. Tribunals need real disagreement and falsification

The critique/tribunal layer promises Pedant, Logician, Geometer, Sycophancy,
Veritas, and Curia roles. In code, Pedant mainly checks output length,
Logician returns true, the contract lock is unused, and external Veritas is not
used. Veritas splits text into sentences but its falsification attempt always
returns false, so claims are verified by default. The rule-based adversary can
penalize expressions of uncertainty, creating pressure against epistemic
humility.

The book should require reviewer independence, distinct failure hypotheses,
real tool/evidence access, explicit abstention, uncertainty preservation,
dissent records, changed-evidence invalidation, and measured false-accept/
false-reject behavior.

### 33. Federated learning needs distinct participants and cryptographic rounds

The federated hub models LoRA updates, FedAvg/FedProx/FedAdam/SCAFFOLD options,
differential privacy, secure aggregation, node reliability, and round records.
But secure masking is not called, unmasking is empty, signatures are ignored,
the minimum update count does not require distinct node identities, and all
non-FedAvg algorithms call FedAvg.

Privacy accounting increments in a simplistic way with no budget refusal; a
zero total sample count can divide by zero; shape mismatches can panic or
misaggregate.

The book should require authenticated participants, unique contribution
constraints, update-shape/schema hashes, clipping before calibrated noise,
composed privacy accounting, dropout-safe secure aggregation, poisoning and
sybil defenses, per-round admission receipts, and held-out global/local utility.

### 34. Peer-to-peer cognition needs content admission, not only transport

Mycelium uses signed libp2p gossipsub, Kademlia discovery, and Noise transport.
That is meaningful network plumbing. Yet bootnodes are not consumed, a fresh
identity is generated every start, an empty peer address list can panic, and
the global topic forwards arbitrary bytes without a semantic admission gate.

`SporeId` is commented as a Merkle root but has no constructor or verification
logic. ATP is a local mutable balance map with unrestricted minting, no durable
ledger, no conservation, and no identity binding.

The book should separate transport authenticity from artifact trust. Every
shared “spore” needs content hashing, schema/type, author/delegation, malware
and policy checks, provenance, resource price, quarantine, and revocation.

### 35. Self-pruning requires a mathematically valid retention function

Kernel autophagy is currently simulation-only. Its retention formula uses a
logarithmic age expression that can be singular or counterintuitive for recent
ages. No DKL deletion occurs.

This is a useful warning: an intuitively named retention score must be tested
for boundary values, monotonicity, units, continuity, and adversarial cases.
Self-pruning must also preserve protected evidence, active obligations,
appeals, dependencies, and reconstructability.

### 36. Architecture breadth needs a growth guard

The development log frequently counts “features” as numbered interfaces or
design entries. Readiness documents describe the system as production ready
while audits record thousands of warnings, stale integration tests, missing
hardware/load/security validation, duplicate subsystems, and unresolved stubs.

The codebase provides a historical reason for the later MoECOT architecture-
debt and growth-guard mechanisms: adding more named organs can outrun the
ability to compile, test, integrate, and measure them.

The ASI Stack should treat architecture surface area as a budgeted liability.
New subsystems should require an owner, integration path, removal of the
superseded surface, tests, observability, and evidence that they improve a
named bottleneck.

## Implementation-reality audit

| Named mechanism | Useful design content | Inspected implementation reality | Book treatment |
|---|---|---|---|
| DKL | Typed graph plus vectors, provenance, bounded snapshots | Multiple edge ontologies; optional provenance; destructive merge gaps | Primary architecture lineage; no retrieval-quality claim |
| Portia | Small learned graph navigator predicting relation/destination | Public navigation is vector entry plus bounded BFS; parameter count placeholder | Heuristic baseline and research design |
| TreeLLM | External knowledge plus small synapse; visible reasoning path | Internal suites and major negative gaps; failed SpiderSynapse run retained | Strong negative/diagnostic case |
| PlanForge | Typed DAG, critical path, contracts, cost/risk routing | Scheduler optimization shallow; formula drift | Implementation-reference pattern |
| Airlock | Least-disclosure context handles | Zero checksums, cloning, simulated pointer | Interface proposal, not isolation evidence |
| SSD-first tensors | Mmap/paging/disk optimizer architecture | Partial real I/O with cache/progress/persistence bugs | Resource-design reference only |
| SSD training validator | Storage I/O harness | Synthetic loss/gradient/baseline; unchanged weights | Simulation, not convergence evidence |
| Trainable router | Sparse top-k router plus online reward buffer | Loss computed; weights not updated | Negative interface/effect example |
| GNN prefetch | Learned graph-based access prediction | Model absent; neighbor heuristic; no training | Baseline mislabeled as learned |
| Fractal memory | Multiscale recursive summaries | In-RAM, zero embeddings, query ignored, placeholder summaries | Research design requiring residual honesty |
| SparkStream | Background cognition and consolidation | Hard-coded/random sparks; same-model dream judge; irreversible pruning risk | Bounded-autonomy caution |
| Ladon/Aigis | Secret handles and SCIF execution | Permission metadata not enforced; no process isolation; raw secret substitution | Security-boundary negative case |
| Aletheia/Curia/Veritas | Risk-scaled active epistemics and tribunal | Keyword gates and verifier stubs; default verification behavior | Whitepaper hypothesis, not truth engine |
| Federated learning | Private LoRA aggregation and round ledger | Secure aggregation/signatures absent; algorithms collapse to FedAvg | Contract backlog, not privacy result |
| Mycelium | Signed P2P transport and content-addressed spores | Transport partly real; content identity/economy/admission incomplete | Hive transport precursor |
| Autophagy | Pressure-triggered self-pruning | Logs intent only; retention function unsafe | Negative self-maintenance case |

## Retained evidence and contradictions

### Readiness contradiction

`docs/CURRENT_STATE.md` and top-level prose call the project complete or
production ready. `docs/PRODUCTION_READINESS_AUDIT.md` instead reports roughly
97% readiness, about 5,660 warnings, outdated/failing integration tests, and no
completed headset, hardware, load, or substantive security validation.
`docs/CODEBASE_AUDIT.md` reports 66 stubs and identifies missing real Portia
lookup, agent execution, and DKL queries.

`docs/SECURITY_AUDIT.md` is principally a dependency-vulnerability scan. It
does not test whether Ladon permissions, SCIF isolation, policy enforcement,
secret non-disclosure, or tribunal behavior are effective.

These records should be used as a book case study in readiness-state
discipline: a percentage and checklist cannot outrank unresolved gate classes.

### Historical build lineage

Retained logs show a sequence of compilation failures, including:

- moved-value failure in brain RAG code (`check.log`, 2025-12-28);
- an LLM quantized-inference pointer type error (`error.log`, 2026-01-27);
- missing DKL statistics imports and missing Portia navigation method
  (`check_dkl.log`, 2026-01-28);
- a missing SparkStream field (`compile_error.log`, 2026-01-31);
- repeated Amorphous visibility, trait, equality, import, and type failures
  (`build_errors*.txt`, `check_output*.txt`, 2026-02-01);
- emulator constant/type failures (`compile_errors.txt`, 2026-02-02);
- eleven kernel integration errors, including unresolved core/artificer/sensory
  symbols and stale PlanForge/VectorQuery APIs (`kernel_errors.txt`,
  2026-02-02).

Two later test logs show only filtered Amorphous tests: one ran two tests and
one ran three, with 54 tests filtered out; neither is workspace-suite closure.
They also contain tens of thousands of warning lines. The logs are valuable
historical evidence of iterative repair, but they do not support “all tests
pass.”

The current mining environment could not compile because dependencies were not
available offline and network access failed. No claim is made that every
historical compiler error remains present in the snapshot. The retained logs
do establish that production-readiness prose and a closed build record were not
aligned at the time of those artifacts.

## Exact chapter crosswalk

| BeastBrain finding | Primary ASI Stack destination | Secondary destinations | Evidence boundary |
|---|---|---|---|
| Durable typed semantic memory | proposed `durable-semantic-memory-and-knowledge-lattices` | `virtual-context-abi`, `claim-ledgers-and-belief-revision`, `procedural-memory-and-cognitive-loop-closure` | Primary design/source lineage; no open-domain quality result |
| Semantic coordinates plus residuals | `compact-generative-systems-and-residual-honesty` | `rankfold-neuralfold-and-artifact-compression`, proposed memory chapter | TreeLLM design with explicit non-semantic HLSH limitation |
| Portia relation/destination navigation | `routing-heads-and-specialist-cores` | proposed memory chapter, `governed-deliberation-and-test-time-scaling` | Neural design; current traversal heuristic |
| Bounded DKL snapshots | `virtual-context-abi` | `context-transactions-snapshots-mounts-and-taint`, proposed memory chapter | Interface/source reference |
| Ontology versioning and migration | `claim-ledgers-and-belief-revision` | `ai-supply-chain-integrity-and-lifecycle-provenance`, proposed memory chapter | Strong negative ontology-drift evidence |
| Memory merge/supersession provenance | `claim-ledgers-and-belief-revision` | `data-engines-continual-learning-and-unlearning`, proposed memory chapter | Partial implementation; later CCA improves lineage |
| Failure-weighted episodic retention | `procedural-memory-and-cognitive-loop-closure` | `failure-modes-of-ungoverned-intelligence`, `data-engines-continual-learning-and-unlearning` | Design plus simple implementation; scoring defects retained |
| Correction applicability contracts | `data-engines-continual-learning-and-unlearning` | `policy-optimization-and-learning-from-feedback` | Negative character-set-matching case |
| Test-time learning identity | `data-engines-continual-learning-and-unlearning` | `evidence-states-and-claim-discipline`, `policy-optimization-and-learning-from-feedback` | Simulated update, no learning claim |
| Tool primitive preconditions/effects/reversibility | `intent-to-execution-contracts` | `runtime-adapters-tool-permissions-and-human-approval` | Useful type/interface lineage |
| PlanForge DAG/slack/contracts | `planning-as-a-control-layer` | `labor-os-and-typed-jobs`, `resource-economics-and-token-budgets` | Mixed real graph algorithms and shallow scheduler |
| Context airlocks | `security-kernel-and-digital-scifs` | `virtual-context-abi`, `context-transactions-snapshots-mounts-and-taint` | Design only; no zero-copy/isolation evidence |
| Minimum-viable-intelligence routing | `routing-heads-and-specialist-cores` | `planning-as-a-control-layer`, `resource-economics-and-token-budgets` | Tier filter/token router, not costed adequacy selector |
| Router effect verification | `benchmark-ratchets-and-anti-goodhart-evidence` | `routing-heads-and-specialist-cores` | Strong negative no-weight-update example |
| SSD-first paging and tiered KV | `resource-economics-and-token-budgets` | `fast-generation-architectures`, `coil-attention-cyclic-memory-and-recurrence-contracts` | Partial implementation; headline scale unverified |
| Cancellation-safe I/O leases | `system-boundaries-and-authority` | `resource-economics-and-token-budgets`, `artifact-graphs-audit-logs-and-replay` | Source-level failure-mode analysis |
| Recursive summary residuals | `rankfold-neuralfold-and-artifact-compression` | `procedural-memory-and-cognitive-loop-closure` | Prototype design; retrieval not implemented |
| SpiderSynapse credit dilution | `policy-optimization-and-learning-from-feedback` | `governed-deliberation-and-test-time-scaling`, `benchmark-ratchets-and-anti-goodhart-evidence` | Source-reported failed training run |
| Tensor layout lineage | `benchmark-ratchets-and-anti-goodhart-evidence` | `ai-supply-chain-integrity-and-lifecycle-provenance` | Source-reported Metal debugging record |
| Background cognition budgets | `open-ended-improvement-engines` | `recursive-self-improvement-boundaries`, `procedural-memory-and-cognitive-loop-closure` | Architecture plus placeholder/random implementation |
| Secret broker versus blind handle | `security-kernel-and-digital-scifs` | `system-boundaries-and-authority`, `runtime-adapters-tool-permissions-and-human-approval` | Negative enforcement/isolation audit |
| Decaying capabilities | `system-boundaries-and-authority` | `runtime-adapters-tool-permissions-and-human-approval` | Interesting lease concept with attack-persistence caveat |
| Constitution-to-enforcement ladder | `constitutional-alignment-substrate` | `security-kernel-and-digital-scifs`, `safety-cases-and-structured-assurance` | Prose/type/heuristic only; no protected enforcement |
| Tribunal independence and falsification | `spinoza-verification-and-proof-carrying-claims` | `scalable-oversight-and-adversarial-ai-control`, `governed-deliberation-and-test-time-scaling` | Strong negative stub/default-accept case |
| Federated rounds and private updates | `personal-compute-hives-and-federated-edge-intelligence` | `model-weight-custody-and-hardware-roots-of-trust`, `data-engines-continual-learning-and-unlearning` | Interfaces present; privacy/security not established |
| Mycelium transport/content admission | `personal-compute-hives-and-federated-edge-intelligence` | `ai-supply-chain-integrity-and-lifecycle-provenance`, `system-boundaries-and-authority` | Signed transport partial; artifact trust absent |
| Self-pruning and memory erosion | `recursive-self-improvement-boundaries` | `artifact-steward-agents-and-living-project-governance`, `claim-ledgers-and-belief-revision` | Simulation and unsafe formula |
| Simulation-labeled metrics | `benchmark-ratchets-and-anti-goodhart-evidence` | `evidence-states-and-claim-discipline`, `capability-thresholds-and-deployment-commitments` | Direct source evidence of benchmark theater |
| Architecture growth guard | `artifact-steward-agents-and-living-project-governance` | `open-ended-improvement-engines`, `recursive-self-improvement-boundaries` | Strong project-level negative record |

## Provisional new chapter decision

BeastBrain resolves the CCA dossier's primary-provenance question: DKL, Portia,
semantic coordinates, bounded knowledge snapshots, and external-knowledge/
small-navigator separation are present here as an earlier coherent lineage.

A distinct chapter tentatively named **Durable Semantic Memory and Knowledge
Lattices** is warranted because the live spine does not currently assign one
owner to:

- durable semantic object identity;
- typed graph relations and ontology migration;
- graph/vector hybrid retrieval;
- provenance-preserving merge, supersession, forgetting, and rollback;
- learned or heuristic graph navigation;
- certified subgraph snapshots for context materialization;
- memory-tier persistence and restart consistency.

The chapter should not become a BeastBrain promotional chapter. BeastBrain is
the motivating implementation lineage and failure case. External knowledge-
graph, graph-RAG, agent-memory, long-term-memory, and learned-retrieval sources
must be ingested before the chapter is added to `book_structure.json` or used
for stronger claims. The final manifest action remains deferred until the
remaining old projects are mined and the boundary is checked for duplicate
ownership.

## Priority book additions from this project

1. Add the durable-semantic-memory chapter boundary after cross-project review.
2. Add an address-plus-residual contract for semantic coordinates and compact
   knowledge references.
3. Add certified bounded graph snapshots as the bridge from durable memory to
   context.
4. Add ontology version/migration requirements and use BeastBrain's four edge
   systems as the negative case.
5. Add provenance-preserving memory merge, supersession, retraction, and
   forgetting requirements.
6. Add unresolved-failure retention as an explicit memory utility signal.
7. Add a router-effect gate: computing a training loss is not evidence that a
   router learned.
8. Add per-path credit diagnostics for branching deliberation and learned
   navigation.
9. Add tensor layout/backend lineage to benchmark-truth records.
10. Add field-level `simulated`, `synthetic`, `measured`, and `reproduced`
    evidence labels.
11. Add cancellation-safe resource leases and no-progress detection to paged
    storage/runtime contracts.
12. Strengthen security chapters with brokered secret use, hard isolation, and
    enforceable capability leases.
13. Strengthen tribunal chapters with independence, falsification, abstention,
    uncertainty preservation, and default-deny evidence gates.
14. Use BeastBrain as a central architecture-breadth/feature-count/production-
    readiness anti-pattern.

## Cross-project provenance

BeastBrain appears primary among the currently inspected projects for:

- DKL and Portia naming and core architecture;
- semantic-coordinate/TreeLLM navigation;
- organism-style SparkStream background cognition;
- PlanForge DAG and intelligence-arbitrage framing;
- Ladon/Aigis blind-handle security framing;
- Aletheia/Talos active-epistemic and tribunal framing;
- SSD-first model/memory/resource architecture;
- Mycelium/ATP personal mesh framing.

CCA appears to evolve BeastBrain's memory and governance designs by adding
append-only epistemic revision, compiler contracts, benchmark truth, and
bounded self-modification. MoECOT further compiles these ideas into registry,
target, evidence, maintenance, and self-improvement control planes. Repeated
mechanisms across the three are one lineage, not three independent supports.

BugBrain, Corben's Trainer, and Corben's Best Model Possible may still own
primary provenance for edge hardware, training loops, model search, or external
evaluation mechanisms. Those decisions remain open.

## Negative lessons and non-claims

1. A named organ or interface is not an implemented capability.
2. A type definition is not an enforcement point.
3. A simulated loss curve is not convergence.
4. A synthetic cache hit rate is not an inference benchmark.
5. A dependency audit is not a security-effectiveness test.
6. A handle is not isolation, zero-copy, or secrecy.
7. A hash over text detects byte changes, not semantic intent drift.
8. A verifier that never falsifies defaults to approval, regardless of its
   name.
9. A router that computes a loss but does not update weights has not learned.
10. A graph model defined in source but bypassed by BFS is not the deployed
    navigation algorithm.
11. Multiple typed ontologies can still create untyped system behavior.
12. Memory merge without immutable parents and supersession can destroy
    evidence.
13. Use-strengthened permissions can reward attacker persistence.
14. Signed network transport does not make received content trustworthy.
15. Internal toy suites cannot establish open-domain knowledge or reasoning.
16. Filtered crate tests cannot support workspace readiness.
17. Thousands of warnings and retained compiler failures contradict a closed
    production gate even if feature checklists are nearly complete.
18. This dossier does not claim BeastBrain achieved AGI, ASI, production
    readiness, safe autonomy, factual truth verification, secret isolation,
    privacy-preserving federation, one-million-token quality, laptop-scale 7B
    training, or any stated power/performance improvement.
19. No source-reported TreeLLM score or training result was reproduced.
20. No ASI Stack support state is promoted by this mining pass.

## Remaining work before BeastBrain is fully closed

- Compare exact DKL/Portia symbols against CCA imports and MoECOT successors to
  record a file/symbol-level provenance chain.
- Classify the 31 crate families as active integrated, active isolated,
  historical, design-only, or superseded.
- Audit the retained build logs against current source to distinguish repaired
  failures from still-live failures once an offline dependency cache is
  available.
- Ingest independent literature for knowledge graphs, graph RAG, learned graph
  navigation, long-term agent memory, test-time learning, SSD inference, and
  secure aggregation before drafting source-supported chapter prose.
- Inspect any newly unzipped predecessor or successor archives before the
  durable-memory chapter boundary is finalized.
- Keep source-reported benchmark tables and hardware projections bounded to
  this implementation-reference record unless independently reproduced.
