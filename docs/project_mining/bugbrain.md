# BugBrain Project Mining Dossier

Date: 2026-07-10

Project: local historical project `BugBrain` (private source checkout; path intentionally omitted)

Pinned revision: `d5ddd37966e2057e8b5ee7fa7bd8f4c833a30dc5`

## Executive conclusion

BugBrain is the first inspected project in this lineage that makes the physical
computer itself an explicit part of the cognitive architecture. It attempts to
run a neuro-symbolic graph, perception, action, security, persistence, and
continual-learning stack directly on a Raspberry Pi 4 as a bare-metal Rust
unikernel. Its most useful contribution to the ASI Stack is therefore not a
claim that the system is intelligent. It is a collection of concrete contracts
for making authority, memory residency, action admission, persistence, thermal
pressure, and deployment state visible at the machine boundary.

The project also supplies unusually useful negative evidence. Several modules
carry strong scientific or capability names while implementing much narrower
mechanisms: the IIT monitor does not compute a minimum information partition,
the Dreamer-lite world model has fixed pseudo-random weights and no learning
update, its stochastic state is deterministic argmax, and the active-inference
epistemic term is constant across the candidate policies being ranked. The
declared 250-million-neuron capacity is a storage/address-space contract, not a
resident trained brain. Readiness reports can be green while all three artifact
manifests are skipped, neural activity is zero, and TTS is degraded and
untrained. These are exactly the distinctions the book's evidence discipline
needs to make mechanically rather than rhetorically.

BugBrain should be used as a primary implementation reference for:

- hardware-explicit ownership and resource governance;
- signed pinned context and bounded context persistence;
- privileged-action state machines and one-shot execution;
- compact typed graphs and mixed-precision edge storage;
- artifact manifests, deterministic replay, and deployment gates;
- the boundary between protocol structure and a real hardware root of trust;
- the boundary between named cognitive modules and validated cognitive effect.

It does not support a claim of AGI, ASI, consciousness, production readiness,
secure autonomy, or measured Pi-class cognition.

## Snapshot identity and source boundary

The root repository is on branch `master` at commit
`d5ddd37966e2057e8b5ee7fa7bd8f4c833a30dc5`, dated 2026-02-10 with subject
`Execute project upgrade cleanup`. The repository has 54 reachable commits and
789 tracked files. No remote was recorded by the local checkout.

The extracted worktree reports 762 modified files. A content diff contains zero
insertions and zero deletions; the 762 changes are mode-only transitions from
`100644` to `100755`. The source contents therefore match the pinned commit, but
the extraction-induced executable-bit drift must be disclosed rather than
described as a clean worktree.

The retained tree is about 9.7 GiB, almost entirely Git history: roughly 4.19
GiB of loose objects and 5.51 GiB in four packs. The working source is small by
comparison: about 10 MiB for the kernel, 19 MiB for the bridge, 0.8 MiB for the
trainer, 0.2 MiB for docs, and 0.16 MiB for tooling. This history was not
rewritten or deleted. Storage cleanup is no longer in scope.

Private project material remains outside the book repository. This dossier and
the public-safe source note record mechanisms, limitations, and provenance; they
do not copy credentials, project artifacts, model data, or private raw logs.

## Structural inventory

### Kernel

The bare-metal `bugbrain` crate contains 91 Rust source files and approximately
74,735 lines. Its source spans:

- boot, CPU, memory pools, DMA, SD, USB storage, I2S, GPIO, mailbox, power,
  watchdog, panic, logging, metrics, and thermal control;
- compact neurons, clusters, edge encoding, sparse structures, ternary and
  mixed-precision weights, mmap windows, token indexes, prefetch, coalescing,
  and compression;
- four core-specific loops for somatic control, cortex propagation, grammar,
  and VideoCore/GPU work;
- context handles, Context Horizon, persona contracts, task lists, skills,
  scripting, ECAE intent control, contradiction handling, and cognitive focus;
- active inference, a lightweight world model, IIT-labelled monitoring,
  Hebbian/STDP learning, self-modification, sleep replay, and a spiking
  transformer;
- camera, vision, audio, TTS, VAD, denoising, Bluetooth, Ethernet/QUIC, mesh,
  swarm, and hive components;
- cryptography, secure framing, provisioning, OTA, and signed system payloads.

The kernel contains 230 Rust test attributes. A current host library run
reproduced `227 passed; 0 failed; 3 ignored` using Rust 1.90 with `RUSTC` and
`RUSTDOC` pinned directly and all build products routed to `/private/tmp`.
This is evidence for the host-testable library surface only. It is not a
bare-metal target build, Raspberry Pi HIL result, trained-artifact test, or
end-to-end capability evaluation.

### Bridge

The `bugbrain_bridge` crate contains 40 Rust source files and approximately
20,723 lines. It provides transport selection, secure sessions, an emulator,
CLI/GUI surfaces, keyboard/mouse/clipboard actions, approval policy, budget
governance, intent presentation, MCP routing, action replay, run ledgers and
traces, vision streaming, and resource monitoring.

The source contains 91 Rust test attributes. The retained whitepaper reports 86
default bridge tests and 89 with Bluetooth. A current offline run could not
resolve the uncached `async-trait` crate, so those counts were not reproduced.
No bridge pass is inferred from dependency unavailability.

### Trainer and deployment tooling

The Python trainer contains 23 modules and approximately 18,928 lines. It
implements corpus management, BPE, graph construction, clustering and locality
reordering, mixed-precision edge quantization, artifact manifests and
attestation, deterministic replay, live-source planning, audio and vision
training, an emulator harness, RL control-path training, degradation policy,
partitioning, image packing, and SD flashing.

The current Python test run reproduced 79 passes. Pytest could not write its
cache into the read-only project tree, but the test suite itself completed.

### Retained artifacts and reports

- a roughly 8.3 MiB `kernel8.img` is retained;
- several readiness JSON reports are retained;
- `tools/ci/clippy_pedantic_report.json` is retained and reports failure;
- `tools/ci/hotpath_bench_report.json` is retained and reports a macOS host
  microbenchmark pass;
- scripts for Pi HIL and OTA power-failure testing are retained;
- no `tools/hil/pi4_perf_report.json` was found in the snapshot;
- no complete trained brain, vision, and audio manifest set was established by
  the retained green readiness reports.

## Architecture mined for the book

### 1. Put physical ownership in the architecture diagram

BugBrain assigns durable roles to the Pi's four ARM cores:

- Core 0 owns somatic control, networking, thermal state, audio, persistence,
  and privileged control;
- Core 1 owns spreading activation and cortical propagation;
- Core 2 owns grammar and Weaver functions;
- Core 3 owns GPU/VideoCore-oriented work.

The exact partition is project-specific, but the book idea is general. A system
architecture should identify which execution domain owns each authority,
deadline, queue, memory region, and safety interrupt. Static ownership can make
contention and privilege legible in ways that a diagram of abstract agents does
not. Dynamic work stealing can then be constrained by an explicit lease:
temporary borrower, permitted memory, maximum work, deadline, preemption rule,
and state-return receipt.

The project's separate decentralized work-stealing document is still partly a
proposal. The four-core ownership map is a stronger book contribution than a
claim that all proposed sharing is complete.

### 2. Separate declared capacity, formatted capacity, resident state, and useful state

`NEURON_COUNT` is 250,000,000. An eight-byte neuron array at that capacity is
about 2 GB before edges. The graph is divided into 512-neuron clusters. The
runtime cache constant is 2,048 clusters.

The source comment and whitepaper repeatedly call that cache about 1 GB. The
implemented cluster load is 16 sectors, or 8 KiB, consisting of roughly 4 KiB
of neurons plus an edge area. At 2,048 entries, the raw cluster images are about
16 MiB, plus cache metadata and optional mixed-precision payloads—not 1 GB.
Conversely, formatting every declared cluster at 8 KiB would require about 4
GB. These are materially different quantities.

The book should require every capacity claim to expose at least:

- addressable maximum;
- physically formatted or allocated amount;
- resident hot amount;
- active amount per step;
- populated/trained amount;
- measured useful coverage;
- metadata, index, cache, and fragmentation overhead;
- storage and memory equations generated from the same constants as code.

“250 million neurons” is therefore a declared graph-capacity constant, not
evidence for a 250-million-unit trained artifact or any level of capability.

### 3. Resource-aware ontology compression is a first-class design operation

BugBrain explicitly cites BeastBrain's larger edge ontology and reduces it to
16 types that fit in four bits. The upper nibble carries type and the lower
nibble carries a small weight in the typed format. The set covers association,
taxonomy, part/whole, entailment, contradiction, temporal relations, semantic
roles, properties, use, and location. It also defines inverse relations and
taxonomy/logical filters.

This is a useful cross-project evolution: ontology design should respond to
runtime budgets while preserving the distinctions needed for routing and
reasoning. The book should define an ontology compilation step that records:

- source ontology and target budget;
- retained, merged, dropped, and reserved relations;
- inverse and directionality semantics;
- quantization or type/weight packing;
- migration and loss receipts;
- an unknown-value quarantine path.

BugBrain's decoder maps every unrecognized upper nibble, including the reserved
value 15, to `CoOccurrence`. That silently converts unknown semantics into an
ordinary association. The safer rule is preserve-unknown or fail/quarantine,
never reinterpret-unknown-as-common.

The graph builder also combines signed delta-varints with optional ternary,
four-bit, and eight-bit weight tiers. It reorders neuron IDs for cluster
locality, budgets edges per fixed cluster image, and emits index tables for
random access. These mechanisms are useful examples of compiling a semantic
graph into a hardware-specific storage ABI.

### 4. Zero-copy context needs bounds, integrity, and initialization contracts

The BeastBrain Airlock idea becomes a concrete `ContextHandle` in BugBrain:
immutable `Arc`-backed blocks, stable IDs, cheap clones, virtual slices, a
bounded LRU registry, a checksum, and a versioned URI.

The mechanism is valuable, but its edge conditions show what the Virtual
Context ABI must specify:

- `metadata_offset` is not checked against data length before slicing;
- a top-level slice clamps `end` but not `start`, so `data()` can panic and
  `len()` can underflow when start exceeds the clamped end;
- the checksum is an additive 32-bit word sum, not an adversarial integrity
  primitive;
- the block version is fixed at one;
- global registration before initialization returns a newly generated default
  ID while dropping the supplied context.

A context handle should be a result-bearing capability. Construction validates
bounds, registration either succeeds durably or returns an error, slices are
checked, integrity identifies the threat model, and the handle carries policy,
generation, provenance, expiry, and revocation behavior.

### 5. Context Horizon is a strong low-resource memory architecture

Context Horizon is one of BugBrain's most developed and integrated subsystems.
It defines a 128,000-unit budget, a signed Tier 0, a hot Tier 1 budgeted at 30%,
a warm Tier 2, and dormant SD-backed state. Chunks carry content, a 512-element
embedding, tier, mass, last-access time, entropy, and tags. A goal vector helps
rank mutable context. Tag indexes and generation-pinned `Arc` read snapshots
allow readers to hold stable views without blocking mutation.

The ingestion path uses bounded rings and per-lane queues with lock telemetry.
Persistence uses two snapshot slots, an append-only journal, CRCs, checkpoint
pages and epochs, journal replay, and a fixed dormant region. This is a strong
embedded analogue of a context transaction system.

The book should preserve the following pattern:

1. a signed, policy-pinned tier for instructions or safety state;
2. goal-aware hot and warm tiers for current work;
3. dormant storage that can be thawed under explicit budget;
4. generation leases for stable concurrent reads;
5. dual snapshots plus a journal for bounded recovery;
6. explicit ingestion backpressure and telemetry;
7. provenance, revocation, expiry, and compaction receipts.

The implementation also exposes essential requirements:

- “tokens” are counted with `content.len()`, which is bytes, not a tokenizer
  contract;
- chunk IDs are based on `now_ticks()` without an explicit collision protocol;
- Tier 0 signatures are verified during accretion, but restored or journaled
  chunks are not visibly reverified on every admission/reload path;
- Tier 0 expiry is set to `u64::MAX`, with no meaningful expiry or revocation
  lifecycle;
- goal drift can demote/archive low-mass chunks, making the current goal part of
  the retention policy;
- entropy contributes positively to mass even though entropy is not evidence
  quality or relevance;
- snapshot budget enforcement and dormant-write failure paths can remove hot
  index state while trying to make space;
- the fixed append-oriented dormant region has no clear reclamation contract;
- an oversized ingest can bypass the ring and take a direct write path,
  weakening the claim that ingestion is uniformly bounded.

The resulting book rule should be: compaction may reduce residency but may not
erase authoritative evidence merely because a goal changed or a cold-store
write failed. Revalidation and revocation must be part of restore, not just
initial admission.

### 6. Split immutable human authority from adaptive presentation

The persona contract has two layers:

- a human charter, signed against the system/vendor key and treated as the
  authoritative layer;
- an adaptive profile that can change under a lower epistemic tier.

Charter updates verify a signature, parse bounded constraints, reject internal
contradictions, and clear an adaptive profile that the new charter invalidates.
Charter and adaptive state have distinct persistence layouts and versions.

This is a useful authority pattern for the constitutional alignment chapter:
human non-negotiables and model-adaptive style should never share an undifferentiated
mutable prompt. The immutable layer needs a distinct signer, update ceremony,
rollback/recovery route, and audit identity.

The enforcement is nevertheless lexical. Rules require or forbid tokens,
token pairs, key/value pairs, and lexeme counts. A signed prose charter plus a
lexical validator is not semantic behavioral enforcement. A default unattested
charter can also exist when no signed charter loads. The book should require a
signed charter to compile into enforceable policy checks, negative/bypass
tests, authority-specific capabilities, and a disclosed fallback state.

### 7. Privileged actions should be durable state machines, not prompt moments

The ECAE intent gate defines action types for host keyboard, mouse, clipboard,
scripts, OTA, swarm/key provisioning, and persona updates. It assigns risk
levels and moves actions through created, proposed, awaiting-decision,
approved, denied, expired, executing, completed, and aborted states. It has 16
bounded slots, a bounded event ring, TTL handling, scenario checks, telemetry,
and an `execution_count` guard that makes execution one-shot.

This is directly useful to the intent-to-execution and runtime approval
chapters. A privileged operation should carry:

- immutable action and parameter digest;
- principal, device, run, target, and current-state binding;
- risk and reversibility class;
- evidence and preconditions;
- expiry and revocation;
- decision identity and rationale;
- one-shot execution receipt and terminal outcome.

BugBrain's scenario checks reveal a subtle anti-pattern. The proposal contains
questions and default answers; approval is accepted only when the caller echoes
those expected answers. For critical actions, “Could this be irreversible
without backup or rollback?” has a built-in expected answer. That checks
agreement with a template, not the truth of the scenario. The book should call
this **confirmation theater**: acknowledgements can confirm that a human saw a
risk, but cannot substitute for independently evaluated preconditions.

The contradiction engine is also a useful small mechanism. It ranks bounded
commitments by entrenchment and retracts the least entrenched when coherence
collapses or a skill/script invariant fails. The book should keep the bounded
belief-revision idea while requiring provenance, justification, appeal, and
downstream invalidation for retraction.

### 8. Approval caches, budgets, ledgers, and traces must share an authority key

The bridge adds per-action approval policy, audit JSONL, TTL decision caches, a
training allowlist, a budget governor, a durable run ledger, step traces, and
action replay. Together they approach an execution control plane.

Their mismatched keys are the main lesson:

- approval cache keys omit the principal and full trace identity, allowing a
  recent decision to be reused across contexts that render the same action;
- the budget governor is keyed by caller-supplied run ID, so arbitrary run IDs
  can shard a quota unless an authority mints and binds them;
- unknown free-memory telemetry is represented as zero but does not force a
  denial;
- CPU admission has three grace actions;
- audit and trace writes silently ignore serialization or filesystem failure;
- JSONL records have no hash chain, signer, or durable flush contract;
- replay uses FNV-1a-style 64-bit outcome hashes rather than a cryptographic
  digest and may retain sensitive command payloads;
- the run ledger defines running, paused, completed, failed, and canceled, but
  only start/resume/cancel/record-step paths are evident; most terminal states
  are not reachable through a complete public transition API;
- recording a step for an unknown or terminal run can return success without
  recording anything.

The book should define a single authority tuple used by approval, budgets,
ledger, trace, and replay:

`principal × run × intent-version × target × target-state × parameter-digest × policy-version`.

Every subsystem can index a projection of this tuple, but it must not invent a
weaker identity silently. Audit failure for a privileged operation must be a
declared fail-open/fail-closed policy decision, not an ignored I/O error.

### 9. Protocol security is not the same as a hardware root of trust

BugBrain contains meaningful security structure: HMAC-authenticated handshake,
ChaCha20-Poly1305 frames, deterministic nonces from direction-specific bases
and sequence numbers, a replay window, session expiration, rekey thresholds,
authentication-failure closure, Ed25519 verification, signed OTA manifests,
two-phase OTA state, and provisioned keys.

The project also implements cryptographic primitives directly. The kernel
tests include SHA-256, HMAC, Ed25519, scalar-multiplication, and round-trip AEAD
coverage. Direct implementation can be necessary in `no_std`, but it raises
the review burden: external test vectors, side-channel review, malformed-input
testing, fuzzing, and independent cryptographic review become part of the
claim.

Two root assumptions are not sufficient for a hardware-root claim:

- device entropy mixes a hardware timer with a static mutable counter and
  multiplication; it is not a demonstrated CSPRNG or hardware entropy source;
- the at-rest wrap key is derived from the board serial, the stored salt, and a
  constant label. The serial and salt are not secrets, so the scheme provides
  integrity and device binding but not strong confidentiality against an
  attacker who can read the card and serial.

The vendor OTA key can be changed through an intent-gated control command. That
is better than an ungated setter, but key rotation still needs an authority
chain: current-root signature, recovery root, anti-rollback counter, physical
presence or equivalent ceremony, and a rotation receipt.

The book should distinguish:

- encrypted/authenticated transport;
- replay-safe session state;
- device binding;
- secret-at-rest protection;
- measured/secure boot;
- immutable or recoverable root authority;
- entropy provenance;
- update and key-rotation authority.

Possessing the first two does not imply the latter five.

### 10. Continual learning needs an apply path, checkpoint, and fixed-probe evidence

BugBrain contains three related learning families:

- STDP/Hebbian history, update buffers, sparse attention, and a Fisher-like
  importance table;
- a self-modifying controller with neuromodulators, local rules, importance-
  scaled plasticity, reward-trend meta-updates, and pending changes;
- a sleep cycle with a 1,024-entry coactivation buffer, recency-weighted replay,
  homeostatic scaling, and age/weight pruning.

These are valuable low-memory designs. In particular, deferred updates allow a
fast event path to emit bounded learning deltas for later application, and
sleep-style consolidation provides a distinct maintenance window.

The integration audit found no ordinary kernel call sites for the
self-modification controller, sleep cycle, world model, or IIT monitor outside
their own modules. The update-producing interfaces therefore should not be
described as deployed self-improvement. A learning claim requires:

- the source event and credit signal;
- bounded update generation;
- actual parameter/edge mutation;
- before/after checkpoint identity;
- protected-weight behavior;
- rollback and recovery;
- fixed-probe behavior changes;
- regression, forgetting, and safety measurements;
- runtime call-path evidence.

The self-modification importance accumulator is described as a Fisher proxy but
uses a moving average of gradient magnitude rather than the same squared-
gradient treatment used elsewhere. Terminology should disclose the estimator,
not borrow the confidence of EWC by name.

### 11. A world-model interface is not a learned world model

The DreamerV3-lite-labelled module has a compact 8-bit matrix layout, a small
GRU, discrete latent state, prior/posterior projections, reward and continuation
heads, imagined rollouts, state save/restore, and a thermal guard. Those are
reasonable interfaces for a Pi-scale world model.

But every matrix is initialized deterministically from a pseudo-random function
and there is no weight-update or artifact-load path in the module. The latent
“sample” ignores its seed and selects the argmax. `dream_idle` takes a random
action and reports predictions from the same fixed random heads; it does not
refine transitions despite the comment saying that it does. The so-called
hallucination intensity is a magnitude proxy, not a measured prior/posterior KL.

This should become a canonical evidence example:

- **interface present**: yes;
- **random forward path executable**: likely yes and host-tested indirectly;
- **trained artifact loaded**: no evidence;
- **learning update applied**: no;
- **predictive validity measured**: no;
- **planning benefit established**: no.

### 12. Epistemic terms must affect the decision they are said to govern

The active-inference agent has hierarchical Gaussian beliefs, learned-in-place
generative layers, candidate policies, expected-free-energy scoring, episodic
memory, and a habit cache. It is integrated through the cognitive-focus path.

The expected-free-energy calculation computes its epistemic value once from
the current belief precision, outside the action loop. The same value is then
subtracted for every action step in every candidate policy. It therefore shifts
all scores by substantially the same amount and does not create action-specific
information seeking. Candidate ranking is dominated by distance to a preferred
observation under a fixed pseudo-random transition matrix.

The book should require a decision-term effect test: vary or ablate each claimed
objective term while holding candidates fixed, and show that it changes route
or action rankings in the expected cases. A named curiosity, safety, or
epistemic coefficient that is constant across candidates is telemetry, not
control.

### 13. A metric named after a theory is not evidence for the theory

The IIT-labelled module records binary state transitions for small neuron
subsystems and computes cause/effect distributions. It calls its score small
phi and marks a subsystem “integrated” over a threshold of 0.01.

The implementation comment says it computes a minimum information partition,
but the function actually compares cause and effect repertoires to an
unconstrained distribution and takes their minimum. System phi is an average
over mechanism scores; larger systems sample mechanisms. The `mechanism`
argument is not used to restrict the repertoire in the visible computation,
and the transition matrix caps represented states at 12 elements even when the
declared subsystem is larger.

The book should use this as a theory-name laundering warning. A metric must be
named for the implemented estimator, with a conformance table showing which
parts of the referenced theory are present, approximated, or absent. No
consciousness inference follows from a thresholded variable named phi.

### 14. Physical pressure should tighten epistemic policy, not loosen it

BugBrain deliberately couples temperature to cognition. The thermal subsystem
also contains ordinary fan control and throttling, which are sensible. But
`Neuron::can_fire` subtracts `thermal_noise` from the firing threshold. As the
noise increases, firing becomes easier. The README and whitepaper describe this
as delirium, creativity, or hallucination caused by heat.

This is a powerful negative design lesson. Physical resource pressure should:

- reduce concurrency or model size;
- shorten horizons;
- increase verification or abstention;
- shed optional work;
- preserve authority and epistemic thresholds;
- emit a degraded-state certificate.

It should not make unsupported firing, claims, approvals, or exploration easier.
Metaphorically making a system “experience heat” is not a safety mechanism.

### 15. Readiness needs applicability, requiredness, capability state, and evidence lineage

Retained reports show both progress and a serious semantic weakness. One report
is false because the release bridge binary is absent. Later reports become true
once the binary exists. In the green reports:

- brain, vision, and audio manifests are `ok: true` because they were skipped;
- emulator status reports zero active neurons and zero queries;
- later status reports TTS as degraded and untrained;
- the control-path check proves that policy, demand, and focus commands are
  accepted and reflected, not that learning or cognition works;
- deploy tooling passes because scripts exist.

The current `readiness.py` has since changed to require manifests by default.
The old reports do not include enough policy/code identity to tell whether they
were created by an earlier implementation or an explicit allow-missing mode.
This is itself a lineage requirement: every readiness result must record the
gate version, required checks, waivers, configuration, artifact identities,
and capability degradation.

A skipped required check is not a pass. The book should model each check as:

`applicable × required × attempted × result × waiver × evidence-ref`.

Overall readiness should be computed per declared deployment profile and
capability set, not as a Boolean conjunction over checks whose semantics can
change between runs.

### 16. Retained contradictory reports outrank summary prose

The whitepaper reports a green clippy-pedantic gate at a 3,901-warning kernel
budget. The retained machine-readable report has `status: fail`: 3,903 kernel
warnings exceed that budget, while the bridge has 981 warnings against a 1,052
budget. The report is pinned to the same commit as this dossier.

The retained hot-path report is a macOS host microbenchmark. Its four cases run
at roughly 61–103 ns per iteration and pass. But accepted regression ratios are
1.75 or 2.0, meaning a 75–100% slowdown can still be labelled a non-regression.
It is not Pi hardware evidence.

The whitepaper says Pi HIL gates are measured and enforced, but no structured
Pi performance report is retained in the snapshot. The HIL script's default
workload is a bridge `status` command while the report vocabulary calls
iterations “queries” and derives QPS. A status-poll threshold is useful for
transport monitoring, not a cognition-throughput benchmark.

The book rules are:

- machine-readable result artifacts outrank prose summaries;
- a gate must disclose how much regression it permits;
- workload names must describe the actual operation;
- missing retained results remain missing even when a script exists;
- host, emulator, target hardware, and deployed workload results are different
  evidence classes.

### 17. Document version, kernel version, protocol version, and artifact identity must not blur

The README identifies BugBrain v23.0, the package version is 23.0.0, and the
whitepaper changelog describes itself as version 177.0 while retaining many
earlier milestone labels. This is normal for a long-lived project, but a single
“version” field would be ambiguous.

The ASI Stack should distinguish:

- document/research narrative version;
- source commit;
- compiler/toolchain and target;
- kernel/runtime version;
- protocol and schema versions;
- brain/model/data artifact identities;
- deployment-image identity;
- gate and policy versions.

### 18. Deterministic artifact replay is stronger than a generic reproducibility claim

The trainer has one of the project's strongest provenance mechanisms. Graph
manifests record corpus hashes, build parameters, clustering decisions, seed,
deterministic mode, artifact paths, sizes, and SHA-256 hashes. Manifests can be
signed with Ed25519 through OpenSSL and checked against trust roots. Replay
verifies the manifest signature, verifies corpus hashes, rebuilds in
deterministic mode, and compares artifact hashes and sizes.

This is a useful pattern for the supply-chain and data-engine chapters. It
should be extended with:

- content-addressed or relocatable corpus references rather than fragile
  absolute paths;
- tokenizer/code/toolchain/container identity;
- source license and consent state;
- train/eval separation and contamination checks;
- deletion/unlearning lineage;
- deterministic versus statistically reproducible fields;
- signer role and key-rotation history.

The live-source registry records provider, source ID, split, modality,
language, license label, fields, URLs, budgets, and enabled state. That is a
useful admission plan, but a user-entered license string is metadata, not legal
verification, and live streams require immutable sample receipts if a run is to
be replayable.

## Cross-project provenance

| Mechanism | BeastBrain lineage | BugBrain evolution | Later ASI Stack implication |
|---|---|---|---|
| Typed durable graph | large and drifting DKL ontologies | explicit 16-type Pi budget, nibble packing, filters and inverses | ontology compilation with loss/migration receipts |
| Airlock/context | disclosure policies and conceptual handles | immutable `Arc` handle, slice, registry, checksum, then integrated Context Horizon | capability-bearing VCA handles with checked bounds, policy, provenance, generation, expiry |
| SSD-first memory | broad paged tensor/memory proposals and simulations | fixed clusters, SD paging, bounded caches, dual snapshots and journal | budget equations generated from concrete storage ABI |
| Organism-style cognition | SparkStream/dream/sleep concepts | thermal gating, sleep replay, world-model and IIT-labelled modules | distinguish wired maintenance from named standalone surfaces |
| Planning and approval | PlanForge and Aletheia/Talos contracts | bounded kernel intent state machine plus bridge policy | authority-bound approval, budget, ledger, trace and replay tuple |
| Security | Ladon/Aigis handles and signed P2P concepts | secure framing, provisioning, OTA, replay windows, key storage | separate protocol security from hardware roots and secret custody |
| Evidence discipline | many internal reports and implementation gaps | retained JSON contradicts whitepaper; readiness can pass skips | report-first gates with machine-readable lineage and requiredness |

BugBrain is therefore not merely “BeastBrain on a Pi.” It is a compression and
operationalization pass. It converts several broad designs into bounded data
structures and machine interfaces, while also revealing which metaphors and
scientific labels did not survive that translation.

## Claims to add or update in the ASI Stack

1. Every runtime architecture should expose execution-domain ownership for
   authority, memory, queues, deadlines, and interrupts.
2. Capacity claims must separate addressable, formatted, resident, active,
   populated, trained, and useful quantities.
3. Semantic ontologies can be compiled to hardware budgets, but the compiler
   must emit loss, alias, unknown-value, and migration receipts.
4. Context handles require checked construction, result-bearing registration,
   generation, provenance, policy, expiry, and revocation.
5. Signed Tier 0 context should be reverified on restore and governed by a real
   expiry/revocation lifecycle.
6. Goal-aware memory compaction may change residency but must not silently
   erase authoritative evidence.
7. Human charter authority and adaptive persona state should have different
   signers, update paths, persistence, and enforcement.
8. Privileged actions should be one-shot expiring state machines bound to
   principal, run, target state, parameter digest, and policy version.
9. Scenario acknowledgements are not independent precondition checks.
10. Approval, budget, ledger, trace, and replay systems must share an authority
    identity rather than each using a weaker cache key.
11. Protocol cryptography, device binding, secure boot, entropy, secret-at-rest
    custody, and root-key rotation are separate claims.
12. A continual-learning interface must show actual parameter mutation,
    checkpoint lineage, fixed-probe effect, forgetting, and rollback.
13. Each named objective term must pass an ablation showing that it affects the
    decisions it purports to govern.
14. Theory-named metrics require estimator-conformance tables and cannot by
    themselves establish the theory's target phenomenon.
15. Physical pressure should tighten or degrade epistemic behavior, never
    lower evidence or approval thresholds.
16. Readiness checks need applicability, requiredness, attempt, result, waiver,
    and evidence identity.
17. Machine-readable result artifacts outrank narrative claims at the same
    revision.
18. Deterministic artifact replay should verify inputs and output identities,
    not merely save a seed.

## Existing chapter destinations

Primary destinations:

- `system-boundaries-and-authority`
- `model-weight-custody-and-hardware-roots-of-trust`
- `security-kernel-and-digital-scifs`
- `virtual-context-abi`
- `context-transactions-snapshots-mounts-and-taint`
- `intent-to-execution-contracts`
- `runtime-adapters-tool-permissions-and-human-approval`
- `artifact-graphs-audit-logs-and-replay`
- `resource-economics-and-token-budgets`
- `readiness-gates-residual-escrow-and-quarantine`
- `benchmark-ratchets-and-anti-goodhart-evidence`
- `ai-supply-chain-integrity-and-lifecycle-provenance`

Secondary destinations:

- `constitutional-alignment-substrate`
- `claim-ledgers-and-belief-revision`
- `procedural-memory-and-cognitive-loop-closure`
- `routing-heads-and-specialist-cores`
- `personal-compute-hives-and-federated-edge-intelligence`
- `recursive-self-improvement-boundaries`
- `open-ended-improvement-engines`
- `capability-thresholds-and-deployment-commitments`
- `data-engines-continual-learning-and-unlearning`
- `policy-optimization-and-learning-from-feedback`
- `compact-generative-systems-and-residual-honesty`
- `artifact-steward-agents-and-living-project-governance`
- proposed `durable-semantic-memory-and-knowledge-lattices`

BugBrain does not by itself justify a new chapter. Its Context Horizon material
strengthens the provisional durable-memory boundary first identified in
BeastBrain, but the decision remains deferred until the Trainer, Best Model,
newly extracted projects, and independent literature are mined.

## Evidence ledger

### Reproduced in this mining pass

- source content matches commit `d5ddd379...`; dirty state is 762 mode-only
  changes;
- kernel host library: 227 passed, 3 ignored;
- Python trainer: 79 passed;
- source/report structural counts and storage sizes;
- machine-readable clippy report status and hot-path report contents.

### Source-reported or retained, not reproduced

- bridge test counts;
- Raspberry Pi kernel build and boot;
- HIL latency, thermal, power, or throughput gates;
- OTA power-failure behavior on hardware;
- security interop beyond host library tests;
- any trained brain, vision, audio, or TTS capability;
- projected benchmark and memory-table claims in the whitepaper;
- swarm, hive, Bluetooth, camera, GPU, and hardware deployment behavior.

### Direct contradictions or narrowing evidence

- retained clippy JSON is red while the narrative calls the gate green;
- retained readiness can be green with skipped manifests and degraded TTS;
- no retained Pi performance JSON was found despite narrative measured-gate
  claims;
- cluster-cache arithmetic does not match the repeated ~1 GB claim;
- world-model, IIT, sleep, and self-modification names outrun their integrated
  effect;
- active-inference epistemic value does not discriminate policies;
- the device wrap key is derivable from non-secret material;
- thermal “creativity” lowers firing thresholds under physical stress.

## Minimum implementations suggested by the project

### Hardware-explicit governed runtime

1. declare core/process/accelerator ownership;
2. bind queues and memory regions to owners;
3. measure deadlines, backpressure, thermal state, and free memory;
4. degrade optional work while preserving safety policy;
5. issue leases for cross-domain work;
6. record a target-specific runtime receipt.

### Signed pinned context

1. verify signer and charter/policy scope;
2. assign collision-safe content identity;
3. admit to a pinned tier with expiry and revocation;
4. expose generation-leased read snapshots;
5. persist through dual snapshots plus journal;
6. reverify on restore and policy change;
7. compact only after a durable no-loss receipt.

### Privileged action

1. create immutable intent with full authority tuple;
2. evaluate machine-checkable preconditions;
3. render human risks and residuals;
4. approve/deny with signer and TTL;
5. execute once against the bound target state;
6. write tamper-evident audit and outcome receipts;
7. expire, revoke, or rollback explicitly.

### Honest cognitive-module promotion

1. interface and random baseline;
2. training/update path;
3. artifact/checkpoint identity;
4. fixed-probe before/after effect;
5. ablation of each named objective term;
6. target-hardware resource measurement;
7. external task validity;
8. only then adopt the stronger scientific/capability label.

## Failure modes to retain

- capacity marketing that hides residency and population;
- comments and whitepapers deriving memory totals independently from code;
- reserved/unknown ontology values silently becoming ordinary associations;
- unchecked context slices and success-shaped dropped registration;
- signature checks performed only at first admission;
- goal-driven compaction erasing evidence or failed cold-store writes losing
  indexed state;
- lexical constitutions presented as semantic enforcement;
- confirmations that merely echo expected answers;
- approval reuse across principals, traces, or target states;
- quota evasion through caller-minted run IDs;
- audit errors being silently discarded;
- fixed random networks described as world models or dreaming;
- decision-objective terms that are constant across candidates;
- simplified theory metrics described as consciousness measures;
- heat making neurons or claims easier to fire;
- skipped checks counted as green;
- status polling labelled cognition throughput;
- machine-readable failures overwritten by narrative summaries;
- broad “implemented” feature matrices based on source-file presence.

## Open questions for the cross-project pass

- Which BugBrain context, persona, intent, graph, and artifact-manifest
  mechanisms were later ported into CCA or MoECOT rather than independently
  reinvented?
- Does Corben's Trainer preserve or repair BugBrain's deterministic replay,
  source licensing, artifact signing, and readiness semantics?
- Does Corben's Best Model implement a real trained world model, action-specific
  epistemic value, or a canonical durable-memory ontology?
- Are Pi HIL JSON reports, trained manifests, brain images, public keys, build
  receipts, or deployment logs retained outside this checkout?
- Is there an authority-protected key-rotation path with anti-rollback and
  recovery roots in a later project?
- Can the 250-million-neuron storage format be generated and mounted without
  exceeding a 4 GB card/RAM budget once edges and indexes are included?
- Which bridge tests require network-restored dependencies, and do their crypto
  vectors agree with the kernel implementation across malformed inputs?

## Non-claims

- Does not claim BugBrain achieved intelligence, AGI, ASI, consciousness,
  secure autonomy, production readiness, or safe self-improvement.
- Does not claim the 250-million-neuron capacity was fully populated, trained,
  resident, or useful.
- Does not claim Raspberry Pi, GPU, camera, Bluetooth, swarm, OTA, or HIL
  behavior was reproduced.
- Does not claim the bridge test suite passed in the current environment.
- Does not claim the custom cryptography is insecure or secure as a whole; it
  identifies root-of-trust and review boundaries visible in the source.
- Does not claim the retained machine-readable reports describe every later or
  external run.
- Does not promote any ASI Stack support state or add a chapter.
