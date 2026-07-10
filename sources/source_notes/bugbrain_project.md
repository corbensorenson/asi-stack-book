# Source Note: BugBrain Project

| Field | Value |
|---|---|
| Source ID | `bugbrain_project` |
| Source title | BugBrain bare-metal neuro-symbolic intelligence project |
| Ingestion date | 2026-07-10 |
| Source version / URL | `local-project:BugBrain@d5ddd37966e2057e8b5ee7fa7bd8f4c833a30dc5` |
| Citation label | Sorenson (2026), BugBrain (pinned local project snapshot) |
| Source policy | Local private cache; public-safe note only; raw project tree is not copied into this repository. |
| Ingestion basis | README and whitepaper, readiness and upgrade documents, kernel/bridge/trainer source, retained CI/readiness reports, structural inventory, current host kernel and trainer tests, and targeted implementation tracing. Hardware, bridge, network, expensive training, and end-to-end model evaluations were not reproduced. |

## Thesis

BugBrain is a hardware-explicit implementation reference for a Pi 4 bare-metal
neuro-symbolic stack. It contributes concrete resource, context, intent,
security, persistence, artifact-replay, and deployment contracts. It also
provides high-value negative evidence showing why capacity constants, named
cognitive modules, green readiness Booleans, and structured security protocols
must not be treated as capability, scientific validity, or hardware-root
evidence without effect and lineage tests.

## Snapshot posture

The project is pinned at Git commit
`d5ddd37966e2057e8b5ee7fa7bd8f4c833a30dc5` on local branch `master`. It has
54 commits and 789 tracked files. The extracted worktree reports 762 modified
files, but all changes are mode-only `100644` to `100755`; content has zero
insertions and deletions relative to the commit. No remote is recorded.

The kernel has 91 Rust files and about 74,735 lines, the bridge has 40 Rust
files and about 20,723 lines, and the trainer has 23 Python modules and about
18,928 lines. The 9.7 GiB checkout is almost entirely Git history rather than
working source. These counts establish surface area, not integration or
capability.

## Primary material inspected

- `README.md`, `docs/whitepaper.md`, pre-release and ownership documents,
  feature/status and upgrade material.
- Kernel boot/runtime/core ownership, neurons, clusters, graph encodings,
  ContextHandle, Context Horizon, persona, ECAE, cognition, learning, sleep,
  world-model, IIT-labelled, thermal, crypto, security, and OTA source.
- Bridge security, approval policy, budget governor, intent, run ledger, run
  trace, action replay, emulator, protocol, resource, and host-action source.
- Trainer graph builder, edge quantizer, integrity, deterministic replay,
  readiness, live sources, RL/harness, degradation, audio, vision, partitioning,
  packing, and tests.
- Retained readiness JSON, clippy-pedantic JSON, and hot-path benchmark JSON.
- Current host kernel library and Python trainer test runs. Bridge testing was
  attempted offline and stopped before compilation because `async-trait` was
  not cached.

## Mechanisms

### Hardware and resource architecture

- Four ARM cores with explicit somatic, cortex, grammar/Weaver, and GPU roles.
- Eight-byte neuron state, 512-neuron clusters, SD-backed graph windows, bounded
  cache, prefetch, telemetry, and mixed-precision edges.
- Pi-oriented thermal, fan, power, memory-pressure, allocator, and degradation
  paths.
- A declared 250-million-neuron address/storage capacity.

### Durable graph and context

- Sixteen-type resource-compressed semantic edge ontology derived from the
  broader BeastBrain lineage, with inverses and logical/taxonomic filters.
- Delta-varint edge targets plus ternary/four-bit/eight-bit weights and
  locality-aware graph compilation.
- Immutable `Arc` ContextHandles, virtual slices, IDs, LRU registry, checksum,
  and URI/version representation.
- Context Horizon signed Tier 0, goal-aware hot/warm tiers, dormant SD state,
  tagged generation-leased read snapshots, bounded ingress, dual snapshots,
  journal, CRC, checkpoints, replay, and thaw.

### Authority and action governance

- Signed human charter separated from a mutable adaptive profile.
- Bounded intent lifecycle with action/risk classes, TTL, scenario prompts,
  approval/denial, expiry, one-shot execution, terminal outcomes, telemetry,
  and event ring.
- Contradiction resolution that retracts a least-entrenched bounded commitment.
- Bridge approval policy, allowlist, decision cache, budget governor, run
  ledger, run trace, action replay, and host resource telemetry.

### Security and supply chain

- HMAC handshake, ChaCha20-Poly1305 framing, sequence-derived nonces, replay
  window, session expiry/rekey, authentication-failure closure.
- Ed25519 verification, signed OTA manifests, staged update state, provisioning,
  device-bound key blobs, and OTA power-failure test tooling.
- Signed artifact manifests, trust roots, corpus and artifact SHA-256 hashes,
  deterministic graph replay, and output hash comparison.
- Live-source registry with source, split, modality, language, license label,
  URL/field configuration, and bounded sampling plans.

### Cognitive and learning surfaces

- Integrated active-inference path with hierarchical belief updates, candidate
  policies, episodic memory, and habit cache.
- Standalone STDP/Hebbian, importance, self-modification, sleep replay,
  lightweight world-model, and IIT-labelled modules.
- Thermal coupling and coherence/contradiction responses.

## Evidence

- The 250-million-neuron value is a capacity constant, not a retained trained
  or validated artifact.
- Cache arithmetic in comments/whitepaper calls 2,048 clusters roughly 1 GB;
  the implemented raw 8 KiB cluster images imply roughly 16 MiB before
  metadata/mixed payloads. A full declared cluster image would be roughly 4 GB.
- Unknown/reserved typed-edge values decode as co-occurrence, erasing the
  unknown state.
- ContextHandle construction/slicing does not fully validate offsets and can
  panic or underflow; registration before global initialization drops the
  handle while returning a fresh-looking ID.
- Context Horizon counts bytes as tokens, uses time-based IDs without explicit
  collision resolution, sets Tier 0 expiry to infinity, and does not visibly
  reverify Tier 0 signatures on every restore/replay path.
- Goal similarity and entropy influence retention mass; compaction and dormant
  persistence need stronger no-loss and evidence-preservation guarantees.
- Persona constraints are lexical rather than semantic behavioral enforcement;
  an unattested fallback charter can exist.
- Intent scenario checks compare approvals with embedded expected answers.
  They are acknowledgements, not independent precondition verification.
- Approval cache keys omit full principal/trace/target-state binding. Budget
  state can be sharded by caller-supplied run IDs. Unknown free memory does not
  force denial.
- Audit and trace I/O failures can be silently ignored; JSONL records are not
  tamper-evident. Replay uses non-cryptographic outcome hashing and may include
  sensitive payloads.
- The run ledger exposes more states than the visible transition API can reach,
  and some invalid step recordings return success without a record.
- Device entropy is a timer-plus-counter mixer. The at-rest wrap key derives
  from board serial, stored salt, and a constant; this is not a secret hardware
  root.
- The world model has deterministic pseudo-random fixed weights and no weight
  update or trained-artifact load path. Its stochastic state is argmax and
  `dream_idle` does not train.
- The active-inference epistemic term is constant across candidate policies and
  therefore does not establish action-specific information seeking.
- The IIT-labelled score does not implement the stated minimum information
  partition and cannot support a consciousness claim.
- No normal runtime call sites were found for the self-modification controller,
  sleep-cycle updater, world model, or IIT monitor outside their own modules.
- Higher thermal noise lowers firing thresholds. Resource pressure therefore
  increases firing permissiveness even though the runtime also throttles.
- Retained green readiness reports mark missing artifact manifests as skipped
  successes, and can be green with zero active neurons/queries and degraded,
  untrained TTS. Current code is stricter, but old reports omit sufficient gate
  policy identity.
- The retained clippy report is `fail` at the pinned commit despite narrative
  prose calling the gate green.
- The retained hot-path report is a macOS host microbenchmark with tolerated
  regression ratios of 1.75–2.0, not Pi cognition evidence.
- No retained structured Pi performance report was found. The default HIL
  workload is status polling, not a cognition query.

### Reproduced evidence

- Kernel host library: 227 passed, 0 failed, 3 ignored.
- Python trainer: 79 passed.
- Git content identity, mode-only dirty-state classification, source metrics,
  and retained report contents.

The bridge suite was not reproduced because its uncached dependency set could
not resolve offline. The current machine also lacks the nightly toolchain and
target components requested by the project; the successful kernel test used the
available stable host compiler directly. This does not contradict an older
report that observed those components in a different environment.

## Claims To Add Or Update

1. Make hardware/process ownership, memory residency, queue authority, and
   safety interrupts explicit in runtime architecture.
2. Split capacity into addressable, formatted, resident, active, populated,
   trained, and useful quantities.
3. Treat ontology reduction as a compilation with loss, alias, migration, and
   unknown-state receipts.
4. Require checked, result-bearing, policy/provenance-bearing context handles.
5. Reverify signed pinned context on restore and enforce expiry/revocation.
6. Require no-loss compaction for authoritative context and evidence.
7. Separate signed human authority from adaptive persona state and compile it
   into behavioral enforcement.
8. Bind privileged intents to principal, run, target state, parameters, policy,
   evidence, expiry, and one-shot receipts.
9. Do not treat acknowledgement templates as independent risk checks.
10. Use one authority tuple across approval, budgets, ledgers, traces, and
    replay.
11. Separate transport security, device binding, entropy, secret custody,
    secure boot, and root-key rotation evidence.
12. Require parameter-change, checkpoint, fixed-probe, rollback, forgetting,
    and runtime-call-path evidence for continual-learning claims.
13. Require objective-term ablations and estimator-conformance tables before
    adopting strong cognitive or scientific labels.
14. Make degraded physical state tighten epistemic policy rather than lower
    thresholds.
15. Represent readiness checks with applicability, requiredness, attempt,
    result, waiver, and evidence identity.
16. Give machine-readable pinned reports priority over narrative summaries.
17. Extend deterministic replay with toolchain, tokenizer, license, split,
    contamination, and deletion lineage.

## Book Chapters Supported

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
- proposed `durable-semantic-memory-and-knowledge-lattices`

## Chapter-boundary decision

No new BugBrain-specific chapter is recommended. The project strengthens the
provisional Durable Semantic Memory and Knowledge Lattices boundary through
Context Horizon and graph compilation, but it also maps cleanly into existing
context, authority, execution, resource, security, supply-chain, benchmark, and
readiness chapters. The durable-memory decision remains deferred until all old
projects and independent literature are mined.

## Failure Modes

- Conflating declared graph capacity with trained or active capacity.
- Maintaining budget tables separately from source constants.
- Reinterpreting unknown ontology values as ordinary relations.
- Returning success-shaped IDs or records after dropping state.
- Verifying authority only at initial ingestion rather than restoration.
- Letting current goals decide whether evidence remains durable.
- Treating signed prose and lexical rules as semantic enforcement.
- Treating expected-answer confirmation as risk analysis.
- Reusing approval or quota state across weaker identities.
- Silently losing privileged-operation audit records.
- Calling fixed random forward paths learning, dreaming, or world modelling.
- Calling simplified proxy variables consciousness metrics.
- Making physical stress lower epistemic thresholds.
- Marking skipped artifacts as passed readiness checks.
- Calling status transport a cognitive throughput workload.
- Letting prose override contradictory machine-readable evidence.

## Open Questions

- Where are the retained Pi HIL reports and trained brain/vision/audio
  manifests, if they still exist?
- Which BugBrain mechanisms were later ported into CCA, MoECOT, Trainer, and
  Best Model?
- Can context restore be made signer-, expiry-, and revocation-complete without
  breaking the embedded budget?
- Is there a later secure-element, measured-boot, recovery-root, or CSPRNG
  implementation?
- Can the graph storage equation be generated and tested against a fully
  formatted artifact at the declared maximum?
- Does any later project turn the world-model, sleep, self-modification, or IIT
  interfaces into measured runtime effects?

## Non-claims

- Does not claim BugBrain achieved AGI, ASI, consciousness, production
  readiness, secure autonomy, safe self-improvement, or useful deployed
  cognition.
- Does not claim the full graph capacity was populated or trained.
- Does not reproduce Pi, bridge, HIL, OTA, swarm, GPU, vision, audio, TTS, or
  network results.
- Does not adjudicate the custom cryptographic implementation as secure or
  insecure in full.
- Does not publish private raw project material.
- Does not add a chapter or promote any ASI Stack support state.
