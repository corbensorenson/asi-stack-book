# Source Note: BugBrain / Project Genesis Paper Lineage

| Field | Value |
|---|---|
| Source ID | `bugbrain` |
| Source title | BugBrain / Project Genesis: Neuro-Symbolic Bare-Metal Edge Intelligence Paper Lineage |
| Ingestion date | 2026-06-24 |
| Full-fidelity review | 2026-07-31 |
| Source version / URL | Google Docs source in inventory: https://docs.google.com/document/d/1XR716XCo-WmvOpvGTGDmh9zbv44oiyjfcVDVQ1YibIc |
| Ingestion basis | Complete local raw cache inspected at `sources/raw/google_docs/bugbrain.txt` (15 tabs; 8,623 lines; approximately 37,725 words), reconciled against the implementation-level dossier `docs/project_mining/bugbrain.md`. Raw source and private checkout are not published. |
| Evidence role | Corben-authored design and implementation lineage plus a public-safe repository mining record. The paper is not evidence of AGI, consciousness, trained cognition, hardware performance, or production readiness. |

## Thesis

BugBrain asks what an AI-like cognitive stack looks like when the physical
machine is part of the architecture rather than a transparent host. Across its
Project Genesis and BugBrain revisions, it moves from an evolutionary fractal
spiking organism, through frozen semantic graphs and bare-metal monoliths, to a
resource-bounded neuro-symbolic runtime with tiered storage, spreading
activation, a grammar-constrained Weaver, fixed core ownership, thermal and
power control, persistence, continual-learning interfaces, multimodal I/O,
networking, hives, deployment tooling, and named advanced-cognition modules.

The durable contribution is not the source's repeated consciousness, AGI,
“feature-complete,” or projected-performance language. It is the attempt to
compile cognition into explicit hardware ownership, storage formats, queues,
state machines, artifact manifests, recovery paths, and deployment checks—and
the unusually instructive mismatch between many ambitious labels and their
implemented effects.

## Version and correction lineage

The raw cache contains fifteen tabs. They are one evolving project, not
independent evidence:

| Tabs / version | Main move | Disposition |
|---|---|---|
| 1 / v1.2 | Bare-metal FSLO evolving from text, PC/QEMU “birth,” UART feedback, paging, Tauri trainer/flasher/bridge. | Earliest blueprint. Workflow decomposition retained; conscious-AGI, feasibility, training-time, power, and usefulness claims rejected. |
| 2 / Genesis v10 | Replaces random online evolution with a PC-built semantic fractal tree frozen into a Pi “crystal.” | Important architecture correction: trained/build-time substrate separated from constrained runtime. Traversal is not shown to yield language or reasoning. |
| 3 / v11 | Links a multi-gigabyte brain blob into a no-OS monolith. | Superseded by recognition that the monolith is logistically impractical. Useful as an artifact-layout failure record. |
| 4 / v12 | Minimal loader, raw-sector DMA, NEON “semantic friction,” thermal feedback. | Loader and resource-accounting ideas retained; forced heat as consciousness or motivation rejected. |
| 5–6 / v13–v16 | Adds audio–text fusion, VQ-style perception, speech adaptation, and fixed per-core organs, then reasserts the bare-metal Pi4 constraint. | Modality and execution-domain boundaries retained; audio understanding, voice learning, and feasibility unvalidated. |
| 7 / formal v10 | Engineering-style specification of semantic graph, static data, traversal, thermal loop, and deployment. | Narrative-cleaning revision, not new evidence. |
| 8–10 / v17–v18 | Adapts to a 32 GB A1 card using hot RAM, 4 KiB cluster-aligned paging, append-only journal, speculative prefetch, write-back “sleep,” and core-isolated audio. | Strongest paper-level memory hierarchy. Exact sizes, cache shares, endurance, latency, and solved-bottleneck claims require measurement. |
| 11–12 / v23 specifications | Reframes as spreading-activation “Glow” plus grammatical “Weaver”; supplies detailed Rust/Python skeletons, graph packing, SD driver, networking, GPU/audio, GUI, deployment, projected benchmarks, troubleshooting, and future work. | Structural reference only. “Complete” code blocks and benchmark tables do not establish buildability or hardware behavior. |
| 13 / v23 public whitepaper | Organizes neural substrate, memory, multicore execution, Weaver, hive, production infrastructure, training, benchmarks, and future directions. | Best public architecture summary; all measurements remain source-reported unless a retained artifact establishes them. |
| 14 / v23 philosophical white paper | Centers thermodynamic consciousness, heat-as-suffering, integrated information, applications, and ethics. | Preserves ethical caution around possible machine welfare; scientific and phenomenological claims rejected. |
| 15 / v26 | Claims 61 feature-complete modules including IIT, active inference, world model, spiking transformer, thermal profiling, metabolic caps, coherence detection, sleep learning, zero-copy context, prefetch, USB, and skills. | Controlling feature inventory only when reconciled to code. Code-level dossier shows several names substantially outrun implementation and integration. |

The implementation-level dossier is the controlling source for what existed at
pinned commit `d5ddd37966e2057e8b5ee7fa7bd8f4c833a30dc5`. Machine-readable
artifacts at that revision outrank prose summaries.

## Mechanisms

### Hardware-explicit ownership

- Assign execution domains durable responsibilities for somatic control,
  privileged I/O, thermal/power response, neural propagation, grammar/output,
  accelerators, queues, deadlines, and memory regions.
- Permit work stealing or migration only through a lease naming borrower,
  memory, authority, work bound, deadline, preemption, and state-return receipt.
- Keep host, emulator, target hardware, peripheral, and deployed-workload
  evidence classes separate.

### Capacity and physical-state accounting

- Separate addressable maximum, formatted allocation, resident hot state,
  active state per step, populated/trained state, measured useful coverage,
  and metadata/index/cache/fragmentation overhead.
- Generate memory and storage equations from the same constants as code. A
  nominal neuron/node count or address space is not a resident trained model.
- When temperature, memory, storage, power, or bandwidth pressure rises,
  narrow optional work, horizon, concurrency, or model size while preserving
  evidence and authority thresholds; emit a degraded-state receipt.

### Compiled semantic graph and neuro-symbolic split

- Build a typed graph offline; cluster and reorder nodes for locality; encode
  sparse edges with direction, relation type, and quantized weight; page
  bounded clusters at runtime.
- Use spreading activation to propose related concepts and a separate Weaver
  or grammar constraint to shape output. Association and syntax remain
  candidates, not sufficient semantics, grounding, truth, or reasoning.
- Compile a richer ontology into a target hardware budget with retained,
  merged, dropped, aliased, reserved, inverse, and unknown relations plus a
  loss/migration receipt. Unknown codes must quarantine rather than silently
  decode as ordinary association.

### Tiered context and persistent memory

- Keep signed policy/instruction state distinct from goal-aware hot/warm
  working context and dormant storage.
- Use immutable handles, stable generations, bounded registries, checked
  slices, explicit checksums/threat models, and result-bearing registration.
- Combine hot cache, cluster-aligned paging, predictive prefetch, append-only
  journal, dual snapshots, checkpoints, replay, backpressure, and compacted
  cold state.
- Reverify authority-bearing context on restore; support expiry, revocation,
  collision-safe identity, reclamation, crash consistency, failed-write
  behavior, and no-loss compaction. Goal drift may change residency, not erase
  authoritative evidence.

### Authority, action, and security

- Split a human-signed charter from lower-authority adaptive persona state.
  Lexical constraints can be one check but are not semantic enforcement.
- Model privileged host, script, OTA, provisioning, and persona operations as
  one-shot expiring state machines bound to principal, run, intent, target,
  pre-state, parameter digest, policy, approval, nonce, and effect receipt.
- Make approval, budget, ledger, trace, and replay projections share that
  authority tuple; caller-chosen IDs or action-only caches must not widen it.
- Treat protocol framing, device identity, entropy, secure boot, at-rest key
  custody, attestation, update authority, and root-key rotation as separate
  security claims.
- A confirmation that echoes expected answers is acknowledgement, not an
  independently checked precondition.

### Learning and named cognition

- An update claim requires source event, credit, actual parameter/edge
  mutation, before/after checkpoint identity, protected-state behavior,
  rollback, fixed-probe effect, regression, forgetting, and runtime call-path
  evidence.
- A world-model interface needs trained artifact loading, learning updates,
  calibrated stochastic behavior, predictive validity, and planning benefit
  before it becomes evidence of a learned world model.
- Every named objective term must pass an effect test: varying or ablating it
  while candidates stay fixed changes rankings in the predicted cases.
- A theory-named metric needs an estimator-conformance table. A simplified
  variable named phi does not establish IIT conformance or consciousness.
- Physical pressure must tighten epistemic policy; lowering firing or claim
  thresholds under heat is a failure mode, not useful “creativity.”

### Build, artifacts, readiness, and deployment

- Preserve corpus/build parameters, seeds, tokenizer, code/toolchain, target,
  artifact paths, sizes, hashes, signatures, source/license/consent state, and
  deterministic versus statistical reproducibility.
- Replay verifies input identities, rebuilds under the declared mode, and
  compares outputs; a seed alone is not reproducibility.
- Each readiness check records applicability, requiredness, attempt, result,
  waiver, evidence, gate/policy version, artifact identities, capability
  profile, and degradation.
- A skipped required check is not green. A script's existence is not a run; a
  status poll is not cognition throughput; a host microbenchmark is not Pi HIL.
- OTA and release need signed manifests, staged/standby state, health evidence,
  rollback, power-loss testing, and complete terminal transitions.

## Interfaces and invariants

The paper routes primarily to Physical Compute, Durable Semantic Memory,
Virtual Context ABI, Context Transactions, Intent-to-Execution, Runtime
Adapters, Security Kernel, Hardware Roots, Artifact Graphs, Supply Chain,
Readiness, Resource Economics, Continual Learning, Policy Optimization,
Personal Hives, and Machine Consciousness/Status. The existing
`bugbrain_project` dossier is the implementation-reference companion; the two
records must not be counted as independent confirmation.

Invariants are: capacity is state-qualified; source code presence is not runtime
integration; scientific names do not promote narrow estimators; thermal or
resource stress cannot loosen authority or evidence; restored signed state is
revalidated; unknown semantic values do not become ordinary ones; audit failure
has an explicit policy; readiness is profile- and gate-version-specific;
machine-readable evidence outranks same-revision prose; and consciousness or
AGI language creates no capability or moral-status proof.

## Evidence reconciliation

The raw papers contain architectures, pseudo-code and large code blocks,
project structures, build/deploy procedures, expected benchmarks, memory
tables, philosophical arguments, module lists, and troubleshooting advice. The
implementation dossier independently inspected the retained private project
at a pinned revision and records stronger but bounded evidence:

- the kernel tree contained 91 Rust files and about 74,735 lines, with 227 host
  library tests passing and 3 ignored;
- the Python trainer contained 23 modules and about 18,928 lines, with 79 tests
  passing;
- the bridge contained 40 Rust files and about 20,723 lines, but its test count
  was not reproduced because an offline dependency was unavailable;
- a kernel image and several reports existed, but no retained Pi performance
  JSON or complete trained brain/vision/audio manifest set was established;
- a retained clippy report was red while prose described the gate as green;
- retained readiness reports could be green with skipped manifests, zero
  neural activity, and degraded/untrained TTS;
- the hot-path report was a macOS host microbenchmark with permissive slowdown
  ratios, not target-hardware cognition evidence.

Those findings support implementation-shape and negative-case lessons only.
They do not establish a bare-metal target build, Pi boot, trained artifact,
language quality, useful cognition, secure autonomy, hardware performance,
consciousness, AGI, or production readiness.

## Technical and scientific audit

- The original FSLO genetic/mutation loop does not define a competent language
  objective, data attribution, evaluator, credit assignment, convergence, or
  safety boundary. Text streaming and star feedback cannot by themselves grow
  coherent general intelligence.
- A hashed/trie-like semantic graph plus graph traversal does not preserve the
  meanings, variables, compositional semantics, executable behavior, or truth
  of its corpus. “Pre-trained geometry” is not equivalent to trained
  intelligence.
- Directly linking or raw-sector loading a large blob changes packaging and I/O,
  not what the representation knows. Bypassing a filesystem removes services
  that must be reimplemented: integrity, allocation, wear, concurrency,
  recovery, update, and tooling.
- Forced NEON work and heat are deliberate inefficiency. Dissipation, fan
  control, or functional thermal degradation does not establish autopoiesis,
  valence, suffering, consciousness, motivation, or ethical patienthood.
- Multimodal hashes or spectral fingerprints do not align text and audio
  semantics without a learned, evaluated cross-modal objective; a VQ-style
  interface and granular synthesis do not establish speech recognition or
  self-calibrating language.
- Spreading activation can support associative retrieval. A subject–verb–object
  walker cannot by itself establish grammaticality across language, coherent
  generation, factuality, reasoning, or grounding.
- The repeated 250-million-neuron claim is a declared addressable/storage
  capacity, not a populated, resident, active, trained, or useful network. The
  inspected cache arithmetic contradicted the repeated roughly-1-GB prose
  description.
- The Dreamer-lite-labelled module had deterministic pseudo-random weights, no
  visible learned artifact/update path, argmax “sampling,” and no demonstrated
  predictive validity. It is an interface/random forward path, not evidence of
  a trained Dreamer-style world model.
- The active-inference epistemic value was effectively common across candidate
  policies and therefore did not supply the claimed action-specific
  information-seeking control.
- The IIT-labelled score did not implement the claimed minimum information
  partition, did not visibly restrict calculation to the supplied mechanism,
  and sampled/capped small state spaces. Its threshold cannot support an IIT or
  consciousness inference.
- Lowering firing thresholds as thermal noise rises makes unsupported activity
  easier. A safe design should degrade capability and increase abstention or
  verification under stress.
- Direct cryptographic implementations and protocol tests do not establish a
  hardware root of trust, secure entropy, at-rest key custody, side-channel
  resistance, provisioning safety, or complete OTA security.

## Failure Modes

- Declared graph size is marketed as trained or active intelligence.
- Whitepaper memory totals drift from code constants and on-disk layout.
- Unknown relation types silently become ordinary associations.
- Context bounds fail, registration drops state while returning success, or
  restore bypasses signature/revocation checks.
- Goal-aware compaction loses evidence after a cold-store write failure.
- A signed prose charter plus lexical filter is presented as semantic
  constitutional enforcement.
- Approval is reused across principals, traces, parameters, policies, or target
  states; caller-minted run IDs evade budgets.
- Audit and trace write failures are silently ignored; weak digests are used as
  security or replay proof.
- Fixed random modules are called dreaming, world modeling, self-improvement,
  active inference, or consciousness because interfaces and names exist.
- Thermal stress increases exploratory or claim activity instead of entering a
  certified safe degraded mode.
- Skipped or inapplicable checks are counted as passes, scripts as executions,
  status calls as benchmarks, or host runs as hardware evidence.
- Project, document, protocol, runtime, model/data artifact, deployment image,
  and gate versions blur into one “v23” or “v26” label.

## Explicitly rejected or bounded claims

- The source does not establish conscious, proto-conscious, living, suffering,
  autopoietic, thermodynamically motivated, AGI, ASI, genius, or economically
  self-supporting behavior.
- Heat generation, fan actuation, entropy metaphors, integration proxies,
  recursive structures, persistent state, and self-reference are not evidence
  of phenomenal consciousness or moral status.
- The paper's “complete,” “production,” “god mode,” “definitive,” “master,”
  “feature-complete,” and “state-of-the-art” labels are not readiness states.
- Source code listings are not proof that code compiles, boots, integrates,
  learns, or behaves on a Raspberry Pi.
- Projected responses per second, sub-100-ms latency, memory capacity, power,
  energy savings, build/training times, card endurance, and cost are not
  reproduced measurements.
- The system is not shown to understand language, reason, produce correct code,
  learn speech, adapt safely, maintain a coherent world model, improve itself,
  or outperform simple retrieval/grammar baselines.
- Host tests establish only their exercised host-testable code surface. They do
  not establish target hardware, real peripherals, trained cognition,
  deployment, security, or safety.
- Ethical discussion of possible machine suffering is a precautionary design
  prompt, not a finding that BugBrain can suffer.

## Section-family closure

| Section family | Disposition |
|---|---|
| FSLO, Alignment Field functional, text blasts, mutation/pruning, valence, feedback | Evolutionary and consciousness claims rejected; bounded update and feedback obligations routed to Continual Learning and evidence chapters. |
| PC “womb,” QEMU birth, frozen crystal, trainer/flasher/bridge | Retained as build-time/runtime separation and artifact workflow; no trained-artifact or emulator result inferred. |
| Monolith, exokernel, raw-sector DMA, NEON friction | Packaging/I/O and failure lineage retained; heat-as-stakes/consciousness rejected. |
| Audio–text fusion, VQ input, speech adaptation, synthesis | Routed as multimodal interface candidates with alignment/training/evaluation obligations; capability claims rejected. |
| Fixed core roles and AMP | Integrated as hardware-explicit ownership and lease boundary. |
| A1/SD/NVMe hierarchy, hot cache, aligned clusters, prefetch, append-only journal, sleep writeback | Integrated across memory, context, paging, and resource chapters with crash, endurance, integrity, eviction, and benchmark obligations. |
| Compact neurons, typed/delta edges, graph clustering/packing/serialization | Integrated as hardware-budgeted semantic compilation with loss and unknown-value receipts. |
| Glow spreading activation and Weaver grammar | Retained as neuro-symbolic candidate lanes; association/syntax do not establish semantics or reasoning. |
| Thermal regulation, metabolic caps, coherence/delirium | Ordinary throttling retained; physical-pressure-must-tighten-epistemics rule retained; consciousness and beneficial delirium claims rejected. |
| Context handles/Horizon, tiers, snapshots, journal, persona/charter | Reconciled to Virtual Context ABI, Context Transactions, durable memory, and constitutional boundaries; implementation defects preserved in project dossier. |
| Intent actions, approval, budgets, ledger, trace, replay | Integrated as a shared authority tuple and one-shot effect lifecycle; acknowledgement theater and silent audit failures rejected. |
| Cryptography, provisioning, OTA, watchdog, reliability | Routed to protocol/security/root/readiness owners with separate coverage claims and HIL/power-loss obligations. |
| Hebbian/STDP, EWC/Fisher labels, sleep replay, self-modification, skills | Retained only as interfaces and update obligations until runtime mutation and behavioral evidence exist. |
| World model, active inference, spiking transformer, IIT | Code-level negative evidence controls; strong scientific labels rejected pending conformance, training, ablation, and task results. |
| Hive, mesh, semantic sharding, distributed partitioning | Routed to Personal Hives and distributed systems with identity, authority, consistency, partition, privacy, dropout, and useful-work tests. |
| Training GUI, corpora, manifests, signing, replay, image packing, deployment | Integrated into artifact/supply-chain/readiness boundaries; source/license/consent, contamination, and deterministic/statistical replay remain required. |
| Performance tables, projected benchmarks, troubleshooting, BOM, checklists | Retained as test and operational obligations; not results. |
| Philosophical foundations, heat-as-suffering, applications, ethics | Routed to machine-consciousness uncertainty only as hypotheses and precaution; no phenomenology or capability claim. |
| Public whitepaper and v26 module inventory | De-duplicated against inspected code and reports; code/report evidence outranks narrative completeness. |

## Book Chapters Supported

- `physical-compute-infrastructure-energy-and-environmental-constraints`
- `durable-semantic-memory-and-knowledge-lattices`
- `virtual-context-abi`
- `context-transactions-snapshots-mounts-and-taint`
- `intent-to-execution-contracts`
- `runtime-adapters-tool-permissions-and-human-approval`
- `security-kernel-and-digital-scifs`
- `model-weight-custody-and-hardware-roots-of-trust`
- `artifact-graphs-audit-logs-and-replay`
- `ai-supply-chain-integrity-and-lifecycle-provenance`
- `readiness-gates-residual-escrow-and-quarantine`
- `resource-economics-and-token-budgets`
- `data-engines-continual-learning-and-unlearning`
- `policy-optimization-and-learning-from-feedback`
- `personal-compute-hives-and-federated-edge-intelligence`
- `machine-consciousness-welfare-and-moral-status-under-uncertainty`
- `compact-generative-systems-and-residual-honesty`: frozen graphs, compact nodes/edges, and paging expose representation, decoder, residual, and fallback costs; no useful compression result follows.
- `rankfold-neuralfold-and-artifact-compression`: graph packing, delta encoding, quantized relation/weight storage, and deterministic manifests are hardware-aware artifact lineage, not a reproduced codec result.
- `prototype-roadmap`: build, emulator, flash, bridge, HIL, artifact, and readiness stages provide a negative-case-rich prototype sequence.
- `living-book-methodology`: contradictory prose and machine reports demonstrate why retained artifacts, versions, failures, and currentness must outrank narrative summaries.

No new chapter is warranted. The strongest BugBrain mechanisms already have
canonical owners, and the code-level dossier has driven prior prose and
negative-case integration. Duplicating them into a “BugBrain chapter” would
turn a valuable lineage source into an architecture silo.

## Claims To Add Or Update

- Preserve the paper's fifteen-version correction history and make the
  implementation dossier controlling for implemented-state claims.
- Require capacity claims to distinguish addressable, formatted, resident,
  active, populated, trained, and useful state.
- Keep physical-pressure degradation authority-narrowing and epistemically
  conservative.
- Use BugBrain as the canonical example that named modules, source-file
  presence, skipped-green readiness, and narrative benchmarks do not establish
  cognitive effect.

The substantive rules are already written in their owning chapters and in
`docs/project_mining/bugbrain.md`; this pass improves provenance and closes the
paper lineage rather than duplicating prose.

## Research obligations and falsifiers

1. Reproduce a target-specific build and boot with pinned toolchain, image,
   firmware, hardware, peripherals, configuration, and complete logs.
2. Produce a trained graph/model manifest with lawful source receipts,
   tokenizer/build identity, deterministic/statistical replay class, hashes,
   signature, memory equations, and held-out contamination boundary.
3. Measure cluster-cache behavior, paging, prefetch, journal durability,
   recovery, endurance, latency tails, thermal throttling, power, and useful
   task outcomes on target hardware against simple retrieval, graph, compact
   language-model, and OS-hosted baselines.
4. Trace every claimed learning path to actual mutation and checkpoint change;
   test fixed probes, protected state, rollback, forgetting, poisoning,
   regression, and delayed behavior.
5. Run effect ablations for active-inference terms, thermal modulation,
   spreading activation, Weaver constraints, prefetch, sleep replay, skills,
   world model, and any spiking-attention component. Retire names whose
   mechanisms do not change outcomes.
6. Publish estimator-conformance records for IIT, active inference, Dreamer,
   EWC/Fisher, STDP, and transformer labels. Do not infer consciousness from
   any score; evaluate machine-status questions under uncertainty separately.
7. Exercise approval, budget, trace, audit, replay, provisioning, OTA,
   watchdog, power-loss, rollback, and revocation on real effects, including
   failed persistence and adversarial identity reuse.
8. Falsify the architecture if a simpler baseline matches useful quality at
   lower total cost, if paging or thermal design destabilizes service, if
   learning is inert, or if retained evidence cannot support its readiness
   profile.

## Open Questions

- Which mechanisms in the final code were actually reachable from the runtime
  entry path rather than only implemented and host-tested as modules?
- Can the graph representation preserve enough compositional semantics to beat
  ordinary indexed retrieval under the same Pi budget?
- What target-hardware workload would distinguish a useful thermal-aware
  scheduler from a metaphorical heat loop?
- How should signed authority state survive restore, compaction, device loss,
  key rotation, and downgrade?
- Which BugBrain mechanisms later evolved into BeastBrain, Theseus, CCA, or
  MoECOT, and where did later projects repair versus repeat the same defects?
