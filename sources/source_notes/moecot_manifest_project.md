# Source Note: MoECOT Manifest Project

| Field | Value |
|---|---|
| Source ID | `moecot_manifest_project` |
| Source title | MoECOT Manifest compiler-era project |
| Ingestion date | 2026-07-10 |
| Source version / URL | `local-project:moecot-manifest@8398335bd01569d4bce7bc4ca2792d3ef48832f9` |
| Citation label | Corben Sorenson, MoECOT Manifest (pinned local project snapshot) |
| Source policy | Local private cache; public-safe note only; raw project tree is not copied into this repository. |
| Ingestion basis | Project goals, active architecture indexes, canonical architecture/research documents, semantic contracts, selected policy JSON, source-tree metrics, and presence checks for principal builders/gates. Expensive compiles, training, holdouts, and deployments were not rerun. |

## Thesis

MoECOT Manifest proposes a compiler-first AI systems architecture in which
human intent, semantic representations, model composition, runtime targets,
training/evaluation plans, deployment, provenance, and self-improvement are
all mediated by typed artifacts and fail-closed gates. Its most valuable
contribution to the ASI Stack is the combination of broad compiler/control
mechanisms with a candid negative record: strong internal contract scores and
architecture coherence coexisted with weak external task performance.

## Source posture

The pinned tree contains 67,809 tracked files and about 22,880 active files
outside deprecated, temporary, and worktree surfaces. Active-language totals
are approximately 305,937 Rust, 145,259 Python, 42,380 Elixir, and 23,946
TypeScript/TSX lines. The canonical semantic directory contains 124 JSON
contracts.

This scale is evidence of implementation breadth, not capability. Contract
presence, builder presence, deterministic fixtures, and source-reported
experiments are kept as distinct evidence classes.

## Mechanisms

### Compiler and semantic substrate

- Compiler-era authority chain from goals and semantic inputs through semantic
  compiler, shared registry, model compiler, target bundles, evidence, and
  Octopus deployment/control.
- Semantic-description IR preserving entities, actions, constraints, goals,
  deployment hints, provenance, and explicit ambiguity slots.
- SBL as deterministic machine-first representation with semantic primitives,
  relations, qualifiers, immutable invocations, strict/exploratory modes, and
  protected-token semantics.
- Four seed classes—identity-only, referential-lossless,
  constructive-semantic, and predictive-bounded—with frozen basis snapshots,
  expander contracts, residuals, and round-trip verification.
- Explicit goal/plan, semantic IR, target IR, plan graph, effect graph, backend
  lowering, and artifact projection surfaces.
- Pass-level input/output schemas, hash inputs, legality rules, strict failure,
  reproducer bundles, bounded equality saturation, and applied localized-repair
  receipts.

### Registry, runtime, and portability

- Registry V2 canonical events/graph/claims/evidence separated from disposable
  read models and watermark-bound caches.
- Shared registries for domains, clusters, policy experts/cores, toolsets, RL
  environments, benchmarks, holdouts, training data, voice filters, and model
  manifests.
- Explicit locality rules: shared experts remain benchmark-agnostic; track
  routers and fuzzy specialists remain local until promotion; holdouts cannot
  enter training.
- Manifest/compiled-bundle runtime identity distinguished from source-code
  constants.
- Multi-target compiler emitting resource-aware host, VM, edge, mobile, and
  Kubernetes bundles with target compatibility and resource caps.
- Portability acceptance defined as benchmark plus semantic/lowering/
  execution/equivalence survivability, not output-folder existence.
- Multi-objective target Pareto frontier across quality, portability, latency,
  cost, and memory.

### Evidence, authority, and supply chain

- Internal provenance packs with OpenTelemetry/OpenLineage projections rather
  than replacement by external standards.
- SLSA/DSSE-compatible release attestations, immutable artifact digests,
  competitive-run bundles, effect logs, replay checks, semantic patches, and
  obligation bundles.
- Evidence/promotion states from hypothesis through draft, candidate, stable,
  and deprecated, plus durable epistemic states and append-only revision.
- Agent identity, scoped delegation, revocation, trust decay, signatures, and
  hash-chained action attestations.
- Scale-indexed alignment obligations for shutdown, override, veto, replay,
  constitutional immutability, and adversarial evaluation families.
- Stronger alignment verification at durable high-cost commitment boundaries
  than at disposable chat/scratchpad surfaces.

### Context, memory, routing, and deliberation

- Ordered hot/warm/cold context slices with TTL/token bounds, pinned safety,
  goal, and policy constraints, plus capability-boundary attachments.
- Deterministic context freeze/thaw and probe-before-expensive-specialist
  routing with hard-policy escalation receipts.
- KV/episodic persistence and memory consolidation across scratch, task, user,
  world, and policy classes using privacy, utility, evidence, replay,
  calibration, and lineage gates.
- Graph-overlay world state with contradiction recovery, relevance, decay,
  repeated-evidence supersession, counterfactual checks, and drift-triggered
  plan repair.
- Shared-attention, router, fuzzy-expert, and RLM policies selected through
  ablation, target health telemetry, robust/minimax ranking, and clamp penalties.
- Difficulty-scaled heterogeneous verification with bounded disagreement and a
  verifier-of-verifiers.

### Training and self-improvement

- Three-copy round-robin participant/adversary rotation with optional external
  reviewer, repair passes, adaptive curriculum, hard-case replay, holdout
  probes, checkpointing, and all subset collapse evaluation.
- Flood multi-generation candidate batches, promotion sets, mutation reseeding,
  convergence records, and artifact/proof/policy gates.
- Superloop escalation from bounded hyperparameters to training overlays,
  prototype-only tracks, and approval-gated compiler architecture.
- Self-improvement mutation scopes with protected governance/alignment/safety
  paths and evidence requirements.
- Improvement-rate and meta-improvement monitoring.
- ATTD-inspired architecture-debt audit, lane-local non-compensation,
  behavior-guarded simplification credit, bounded maintenance packets, and a
  RED growth guard that pauses autonomous candidate generation.
- Trace-to-training exchange with encrypted raw traces, retention limits,
  distilled capsules, separate training/payout gates, and anti-gaming decay.

## Evidence

The following are project-reported and were not reproduced by this book work:

- Aggregate internal ablations favored keeping shared attention and a shared
  world model enabled.
- A five-seed project comparison reported graph-overlay world memory at
  `13.4/21` versus `11.0/21` mean full-suite contracts and `5/5` versus `2/5`
  on its targeted world-model suite.
- RLM budget search retained a target-aware profile after rejecting a slightly
  higher-scoring challenger whose gain depended on extra target clamping.
- Fresh patched holdouts recorded MMLU-Pro `10.49%`, HumanEval+ `5.49%`, and
  MBPP+ `6.88%`; speech WER remained near one.
- Speculative decode matched an internal aggregate score but collapsed coding
  holdouts to zero and was therefore not promoted.

## Claims To Add Or Update

1. **Compilation all the way down:** source authority and verified lowering
   for intent, plans, effects, runtime, deployment, research, and promotion.
2. **Ambiguity debt:** unresolved intent remains visible through lowering and
   blocks strict execution where required.
3. **Applied localized-repair receipts:** scope proposals must be matched by
   proof that actual mutations stayed inside the affected subgraph.
4. **Semantic portability:** a target is supported only when behavior,
   policies, interfaces, and acceptance evidence survive lowering/execution.
5. **Clamp-safe resource promotion:** a policy dependent on deployment clamps
   is not a robust default.
6. **Maintenance packets and growth guards:** governance failures compile into
   bounded repair objectives; architecture-debt RED stops autonomous growth.
7. **External-holdout reality:** internal contracts and architecture quality
   require a separate capability scoreboard.
8. **Execution versus mutation authority:** replayable run effects do not by
   themselves authorize source-of-truth changes.

## Book Chapters Supported

Primary destinations:

- `integrated-reference-architecture`
- `cognitive-compilation-and-semantic-ir`
- `artifact-graphs-audit-logs-and-replay`
- `ai-supply-chain-integrity-and-lifecycle-provenance`
- `routing-heads-and-specialist-cores`
- `open-ended-improvement-engines`
- `recursive-self-improvement-boundaries`
- `benchmark-ratchets-and-anti-goodhart-evidence`
- `artifact-steward-agents-and-living-project-governance`

Secondary destinations:

- `human-intent-as-a-formal-input`
- `intent-to-execution-contracts`
- `planning-as-a-control-layer`
- `context-transactions-snapshots-mounts-and-taint`
- `procedural-memory-and-cognitive-loop-closure`
- `claim-ledgers-and-belief-revision`
- `system-boundaries-and-authority`
- `governed-deliberation-and-test-time-scaling`
- `resource-economics-and-token-budgets`
- `policy-optimization-and-learning-from-feedback`
- `data-engines-continual-learning-and-unlearning`
- `capability-thresholds-and-deployment-commitments`
- `safety-cases-and-structured-assurance`

No new chapter is recommended. The project is a convergence reference whose
mechanisms already have layer owners.

## Open Questions

- Which compiler, provenance, attestation, and supply-chain mechanisms are
  directly evidenced in the pinned project versus only described in documents or
  schema surfaces?
- Which SLSA/DSSE-compatible fields can be publicly cross-walked to the book's
  supply-chain records without implying that signing, verification, or release
  workflows were executed?
- Which duplicated or inherited mechanisms belong to MoECOT Manifest versus CCA,
  BeastBrain, Trainer, Best Model, or BugBrain primary provenance?

## Limitations and provenance warnings

- Expensive builds, tests, benchmarks, training, and deployments were not rerun.
- Contract and script presence do not establish deployed enforcement.
- Project thresholds are local policy constants unless separately calibrated.
- Internal world-model and architecture suites are not independent external
  evidence.
- The project's external citations must be ingested as their own sources before
  supporting book claims.
- MoECOT overlaps CCA and likely inherits mechanisms from BeastBrain, Trainer,
  Best Model, and BugBrain; repeated ideas are not independent support.
- The existing connector-only source ID `moecot` remains distinct from this
  pinned local-project record.

## Failure Modes

- Internal success can coexist with severe external capability gaps.
- Reward improvements can conceal routing or holdout regressions.
- Harness bugs can erase evidence or create false zeroes; fixes require a fresh
  baseline.
- A descriptor bundle is not a backend implementation.
- A seed identity is not reconstructable content.
- Memory composition is not parameter merging.
- Frozen configuration is not demonstrated quality.
- Contract abundance can create handoff confusion without a canonical active
  index and deprecation policy.
- Architecture governance must govern its own complexity and stop growth when
  verification capacity is being eroded.

## Non-claims

- Does not claim MoECOT achieved AGI, ASI, flagship capability, safe
  self-improvement, corrigibility, production security, or deployment safety.
- Does not reproduce the project's benchmark, training, world-model, routing,
  attestation, portability, or hardware results.
- Does not treat 124 contracts as 124 implemented capabilities.
- Does not promote an ASI Stack support state.
- Does not authorize publication of the raw private project tree.
