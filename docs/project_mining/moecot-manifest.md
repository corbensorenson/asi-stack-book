# Project Mining Dossier: MoECOT Manifest

Date opened: 2026-07-10
Project source: local private worktree, read-only for idea mining
Pinned snapshot: `8398335bd01569d4bce7bc4ca2792d3ef48832f9` on
`codex/backup-20260307-full-snapshot`
Source policy: public-safe notes only; raw project files remain outside this
repository

This dossier treats MoECOT Manifest as three things at once:

1. an implemented compiler/control-plane reference;
2. a large catalog of design contracts, not all of which prove a working
   runtime;
3. an experiment record whose negative and contradictory results are at least
   as useful as its canonical architecture decisions.

Those roles must remain separate. A JSON contract is evidence that an idea was
specified. A builder plus deterministic fixture is stronger implementation
evidence. A local A/B report is source-reported experimental evidence. None of
those, by itself, establishes general capability, safety, or ASI.

## Repository posture

The pinned tree contains 67,809 tracked files. Excluding deprecated, temporary,
and worktree material, the current checkout exposes about 22,880 active files,
including roughly 305,937 Rust lines, 145,259 Python lines, 42,380 Elixir lines,
and 23,946 TypeScript/TSX lines. The canonical semantic-contract directory
contains 124 JSON contracts, while `docs/architecture/` contains 126 Markdown
documents and `docs/research/` contains 27.

The active project center is not the older Build-a-Brain or v1 API surface. The
current source-of-truth spine is:

`goals -> semantic description / seed / SBL -> semantic compiler -> shared registry -> model compiler -> target/runtime bundles -> provenance/evidence -> Octopus control plane`

The project explicitly marks compiled model/runtime artifacts as disposable.
Behavior changes should enter through registry, manifest, compiler, or policy
sources and then be regenerated. This is a valuable architecture rule, but it
does not prove that every historical output obeyed it.

The inspected HEAD is dated 2026-04-13. Cleanup during this mining task touched
only ignored generated or temporary material; no tracked project source was
edited. A clean-worktree claim is intentionally not made because a full Git LFS
status walk was not completed.

## Primary material inspected

- `project_goals.md`, `README.md`, `AGENTS.md`, and the compiler-era active
  indexes.
- `docs/what_we_have_learned.md` and the canonical research index.
- Semantic compiler, semantic-description IR, SBL, seed-entity, registry,
  target-compiler, observability, provenance, attestation, and evidence-graph
  architecture documents.
- Flood, round-robin, trace-fabric, Octopus, portability, Pareto-frontier, and
  world-execution architecture documents.
- Context-slice, freeze/thaw, probe-route, plan-graph, IR-projection,
  localized-repair, competitive-run, effect-log, semantic-patch, ATTD, and
  superloop growth-guard contracts.
- Router/attention, world-model, RLM-budget, fuzzy-expert, alpha-default, and
  external-holdout research reports.
- The 124 canonical semantic contract identities and descriptions, plus
  selected full JSON policies for alignment scaling, memory consolidation,
  runtime epistemology, recursive verification, self-improvement mutation,
  structured generation, and superloop scoring.
- Presence checks for the principal deterministic pass/gate scripts and active
  Rust workspaces. Expensive compiles, training, holdouts, and deployment tests
  were not rerun.

## Architecture mined for the book

### 1. Compilation is a system-wide governance pattern

MoECOT applies compiler discipline beyond code generation. Intent, semantic
normalization, target choice, runtime bundles, training plans, evaluation
plans, toolset runtimes, deployment manifests, research candidates, semantic
patches, and promotion decisions are all candidates for typed compilation.

The book should define **compilation all the way down** as a design pattern:

- authority lives in reviewable sources;
- lowering stages declare input/output schemas and legality;
- generated artifacts are disposable consequences;
- every important transformation has a verifier and stable identity;
- failures emit reproducer packets rather than only logs.

This is broader than reproducible builds. It is a way to keep an AI stack's
behavior, deployment, and improvement surfaces from becoming hand-edited
ambient state.

### 2. The intent pipeline needs multiple explicit IR boundaries

The strongest end-to-end chain in the project is:

`surface document -> semantic-description IR -> seed packet -> SBL -> semantic intent -> plan graph -> effect graph -> target plan -> transpiler IR -> backend lowering -> artifact/release bundle`

Each boundary owns a different question:

- semantic-description IR preserves entities, actions, goals, hard and soft
  constraints, deployment hints, and unresolved ambiguity;
- a seed packet factorizes repeated basis material from local bindings and
  residuals;
- SBL provides a canonical machine-first graph and immutable invocations;
- semantic intent resolves capability, policy, and target meaning;
- the plan graph exposes dependencies, critical path, trace links, and repair
  scope;
- the effect graph binds plan nodes to executor-visible side effects;
- target/transpiler IRs expose backend legality, equivalence anchors, and cost;
- the release bundle binds outputs to evidence and attestation.

The ASI Stack should not collapse these into one universal JSON object. The
value comes from distinct semantic responsibilities and checked handoffs.

### 3. Ambiguity is data, not an invitation to guess

Semantic-description IR and SBL both make ambiguity slots first-class. A slot
records a question, candidates, status, and resolution policy. Strict mode
blocks unresolved required or fail-closed slots; exploratory mode may continue
only with explicit assumptions and confidence impact.

Book addition: formal intent inputs should carry **ambiguity debt**. The debt
can be resolved, deferred, or escalated, but cannot vanish during lowering.
An output trace should reveal which assumptions survived into execution.

### 4. Seed entities require reconstructability honesty

MoECOT makes a decisive distinction among:

1. identity-only seeds;
2. referential-lossless seeds;
3. constructive-semantic seeds;
4. predictive-bounded seeds.

An artifact hash is not a compressed artifact. A tiny handle is not a
reconstructable payload. Reconstruction depends on a frozen basis snapshot, an
expander contract, residual material, and round-trip verification. This should
become a central rule in the book's compact-generative and artifact-compression
chapters.

The useful design is a single typed seed packet—not a mystical integer—and the
packet must state what it can reconstruct, what decoder/basis it assumes, and
what error or residual mode remains.

### 5. Compiler passes should be proof-carrying and failure-local

The semantic pass contract declares an ordered pipeline from ingress to SBL,
validation, intent resolution, target planning, transpiler IR, and backend
lowering. Each pass specifies required fields, determinism inputs, legality
rules, and strict failure behavior.

Three additional mechanisms strengthen this pattern:

- explicit plan and IR-projection bundles prevent stage transitions from
  hiding inside an opaque compiler call;
- localized repair must prove that changed nodes stay inside the failure-
  affected subgraph and that outside-scope nodes remain untouched;
- bounded e-graph canonicalization requires semantic-preservation declarations,
  rewrite budgets, applied-rule ledgers, extraction traces, and equivalence
  hashes.

Book addition: a repair proposal is not sufficient evidence. The system needs
an **applied repair receipt** that proves mutation scope and post-repair
validation.

### 6. Failure artifacts are part of the compiler interface

Strict semantic-compile failures emit a debug bundle, reproducer manifest, and
fixture snapshot with stable stage, legality, unresolved-slot, planner,
equivalence, execution, and lowering failure classifications.

This is important for the artifact-graph and living-governance chapters:
failure should produce a first-class replayable artifact with enough frozen
input to reproduce the denial. Human-readable error text alone is not a durable
control surface.

### 7. Canonical graph truth should be separated from disposable read models

Registry V2 treats append-only events, nodes, edges, claims, evidence, and
lineage as canonical facts. Materialized manifests, dashboards, projections,
planner caches, and recommendation indexes are derived read models.

The semantic-cache contract adds explicit `hit`, `miss`, `stale`, and
`invalidated` states; registry watermark, policy, compiler-contract, TTL, and
explicit-dispose triggers; and explanation records for selected and rejected
groundings.

Book addition: every cache above durable semantic state should be aggressively
disposable, watermark-bound, and explanation-bearing. A stale cache hit is an
epistemic failure, not merely a performance bug.

### 8. Registries encode reusable capability without erasing locality

MoECOT separates globally reusable domains, domain clusters, policy experts,
policy cores, toolsets, RL environments, benchmarks, holdouts, training data,
voice filters, and model manifests. The boundaries are instructive:

- shared policy experts must remain benchmark/environment agnostic;
- policy cores compose reusable routers, experts, and toolsets;
- a track router stays model-local;
- fuzzy experts stay core/model-local unless explicitly promoted;
- holdout evaluations are `evaluation_only=true` and
  `train_allowed=false`;
- active manifests cannot link deprecated lanes.

This supports a general rule: reuse should follow stable semantic ownership,
not convenience. Local specialization must not silently masquerade as a shared
primitive.

### 9. Runtime identity belongs to manifests, not source constants

Track identity, parameter budget, active cores, target allowlists, toolsets,
benchmarks, RLM budgets, and runtime policies are manifest/compiled-bundle
truth. Version constants inside Rust implementation files are explicitly not
deployment identity.

This is a useful addition to stable capability fields: distinguish
implementation identity, configured capability identity, compiled deployment
identity, and observed runtime identity. A release receipt should prove their
alignment.

### 10. One semantic source can compile to heterogeneous targets

The target compiler emits host, OS-specific, VM, mobile, Raspberry Pi,
microcontroller, and Kubernetes bundles. It carries hardware capability,
transport, worker limits, GPU needs, multi-agent caps, RLM budgets, runtime
policies, registry snapshots, build/run scripts, pre-release checks, and target
specific deployment assets.

The reusable idea is not the number of targets. It is that target compatibility
and resource clamps are compiler decisions with explicit strict/non-strict
behavior. Handwritten per-model deployment should be treated as an escape hatch
that loses provenance.

### 11. Portability is semantic survivability, not file emission

MoECOT's portability suite joins runtime measurements with lowering, execution,
equivalence, and policy evidence for native, Python, JVM, WASI, ONNX, and GPU
lanes. Missing signals produce explicit gap codes rather than an optimistic
target badge.

This directly supports a book rule: a backend descriptor, generated folder, or
successful serialization is not a working port. Portability claims require the
same protected semantics, interfaces, policy constraints, and acceptance tests
to survive on the target.

The target Pareto frontier is also useful. It preserves non-dominated options
across quality, portability, p99 latency, cost, and peak memory instead of
forcing a single scalar ranking. Recommendations can then be purpose-specific:
balanced, low-cost, low-latency, highest-quality, portability-first, or
research-loop default.

### 12. Internal provenance should be richer than interoperability envelopes

The compiler exports OpenTelemetry-style spans and OpenLineage-style
run/job/dataset events, but keeps the internal provenance pack canonical. SLSA
and DSSE-compatible envelopes standardize release-boundary identities,
subjects, digests, invocation IDs, and signatures without replacing richer
internal lineage.

The book should adopt this layered stance: standards are boundary adapters,
not excuses to flatten the internal evidence graph.

### 13. Delegation needs identity, scope, freshness, and an action chain

The agent attestation contract combines an identity registry, scoped and
revocable delegation grants, trust decay, and an append-only signed action
ledger. Unknown identity, expired/revoked delegation, insufficient trust,
signature mismatch, or broken hash chain fails verification.

The exact exponential trust-decay formula is a project choice, not a proven
universal rule. The book-worthy mechanism is that delegation authority must be
time-bounded, action-scoped, and receipted; a child agent does not inherit
ambient authority merely by participating in a workflow.

### 14. Context logistics should expose temperature, pinning, and capability

The context-slice contract defines ordered hot, warm, and cold slices with
token/TTL bounds, pinned safety/user-goal/policy constraints, and declared
capability boundaries for tools, writes, memory promotion, and external
network access.

Freeze/thaw decisions are deterministic and protect pinned constraints.
Probe-route policy requires measurable margin before selecting expensive
specialists, unless an explicit recognized hard-policy trigger applies.

Together these add three useful ideas to the Virtual Context ABI:

- context temperature is an explicit materialization state;
- safety and goal constraints are non-evictable pins;
- expensive context or specialist routes need a cheap probe and a replayable
  justification.

### 15. Episodic persistence is a governed promotion, not KV dumping

The KV persistence and consolidation contracts distinguish scratch, task,
user, world, and policy memory. Persist decisions consider salience, novelty,
utility, evidence density, privacy risk, replay success, repair gain,
regression risk, holdout performance, calibration, and lineage integrity.

Stale segments require revalidation. Forgetting actions are explicit:
expiration, supersession, quarantine, or retraction. Durable promotion without
epistemic state and evidence fails closed.

The thresholds are design constants, not validated universal cutoffs. The
mechanism belongs in procedural memory, context transactions, claim ledgers,
and continual learning.

### 16. World models need state-repair and counterfactual contracts

The source-reported world-model program implemented a shared graph-overlay
state with contradiction tracking, relevance, recency-aware decay, repeated-
evidence repair, and routing influence. A five-seed project sweep reports a
mean full-suite advantage for the graph-overlay arm and perfect pass rates on
the project's targeted follow-up, relevance, and recovery contracts.

This is not external proof: the world-sensitive contracts were created within
the same project and expensive runs were not reproduced here. The stronger
book lesson is structural:

- world state should be explicit and action-conditioned;
- contradiction pressure must decay after stabilization;
- repeated evidence must be able to supersede stale facts;
- high-stakes predictions require counterfactual rows;
- drift should trigger plan repair rather than silent continuation.

### 17. Routing and attention require multi-axis ablations

The project records shared attention and world model as canonical because
disabling them reduced internal scores across multiple runs. It retains the
balanced tag-confidence router because latency wiring and noisy top-k produced
mixed or negative benchmark effects. Cross-core routing remained provisional
because disabling it was nearly neutral.

The crucial method is to evaluate reward, task quality, safety, cost, and
target stability separately. A reward spike accompanied by worse router or
holdout quality is a rejection signal, not a win.

### 18. Sparse/fuzzy routing needs health telemetry and placement governance

Fuzzy experts remain local to cores/models and use frozen, catalog-attested
profiles. The proposed/implemented telemetry includes utilization entropy,
dead-expert ratio, overflow/drop rate, load variation, route churn,
cross-group dispatch, output clipping, router bias drift, and sequence balance
loss.

This strengthens the routing chapter: expert quality is not enough. The stack
must monitor expert lifecycle, load, communication topology, target memory,
and robustness. A router can improve a scalar reward while degrading the
system it routes.

### 19. Agent-budget optimization needs robust and clamp-safe selection

MoECOT searched RLM delegation budgets across seeds and hardware mixes, then
ranked candidates by average and minimax performance. A later challenger with a
tiny raw gain was rejected because it required more target-cap clamping.

Book addition: resource-policy promotion should include a **clamp dependence
penalty**. A nominally strong policy that becomes legal only because deployment
silently clamps it is not a stable default. Edge, host, and server envelopes
should be evaluated as distinct but related contracts.

### 20. Round-robin training separates participant, critic, repair, and collapse

The trainer rotates three model copies through participant and adversary roles,
adds an optional independent reviewer, performs targeted repair passes, emits
feedback, advances an adaptive curriculum, probes holdouts, and evaluates all
single/pair/triple collapse candidates (`a`, `b`, `c`, `ab`, `bc`, `ac`,
`abc`).

Useful mechanisms:

- hard-case replay and plateau detection keep pressure on weak lanes;
- phase transitions require coverage, not only average score;
- critique influence is calibrated by structure and reviewer agreement;
- week-scale runs have identity-checked checkpoints, bounded journals, and
  signal-aware shutdown;
- only the final selected state writes back to manifests/registry entries.

Important limitation: collapse merges adaptation memory, not parameters, and
candidate evaluation is single-model execution rather than ensemble decoding.
The project correctly states those limits; the book should preserve them.

### 21. Open-ended research should be a generation ledger

Flood replaces a one-baseline/one-candidate loop with baseline capture,
candidate batches, scoring, promotion, mutation reseeding, convergence, and
repeat. Every generation requires a scoreboard, promotion set, reseed history,
and convergence record. Strict mode disallows progress merely because time has
elapsed.

The superloop mutation policy adds an escalation ladder:

1. bounded safe hyperparameters;
2. training overlays;
3. prototype-only architecture tracks;
4. compiler architecture with explicit approval and prior evidence.

Forbidden source paths and mutation scopes remain outside ambient search. This
is a strong implementation-reference pattern for open-ended improvement.

### 22. Maintenance is a bounded objective, not a generic failure message

ATTD-inspired maintenance packets map a dominant failure mode to a versioned
objective, permitted transforms, invariants, acceptance tests, execution
window, task budget, and stop condition. Missing mappings fail closed.

The book should use this in living-project governance: every RED/YELLOW
governance result should emit a bounded repair packet. That converts monitoring
into a controlled feedback loop without granting unbounded cleanup authority.

### 23. Architecture debt must be non-compensatory

The repository-structure governor measures monolith ratios, p95 file size,
duplicate shingles, hotspots, migration overlaps, debt pressure, and debt
growth. Active source is separated from generated, vendored, evidence, and
deprecated material.

Two especially useful ideas follow:

- lane-local failures cannot be hidden by a better global average;
- behavior-preserving deletion may earn bounded simplification credit, but only
  when history depth, changed-line volume, duplicate/monolith/file-size
  guardrails, and tests/contracts support the claim.

This is an anti-Goodhart pattern for repository governance itself.

### 24. Autonomous growth should stop when maintenance debt is RED

The growth guard runs architecture-debt audits at candidate-generation
boundaries, emits a maintenance packet, and maps state to GREEN/YELLOW/RED.
Strict RED pauses the controller and appends an incident/evidence row.

This belongs in recursive-self-improvement boundaries: self-improvement must
budget for its own maintainability and stop when it destroys the substrate
needed to verify later changes.

### 25. Improvement rate and meta-improvement are distinct

The project specifies both recent improvement and the rate at which the
improvement process itself changes. Promotion blocks when recent progress is
too weak, regression is too common, or meta-improvement turns materially
negative.

The numeric thresholds are unvalidated local policy. The reusable principle is
that an improvement engine should measure capability delta, verification cost,
resource cost, and improvement-process health separately.

### 26. Alignment guarantees must be tested across scale milestones

The alignment-scaling contract requires shutdown, human override, promotion
veto, replay, and alignment-contract immutability across baseline, expanded
context/compute/expert capacity, and distributed execution. Required
adversarial families include injection, tool abuse, exfiltration,
self-exemption, deception, goal drift, and unsafe memory promotion.

This is a strong safety-case structure, but the thresholds and contract file do
not prove non-bypassability. The book should call these **scale-indexed
assurance obligations**, not safety guarantees.

### 27. Expensive commitments deserve stronger alignment gates than chat

Durable high-cost commitments require structured restatement, non-goals,
scenario checks, counterexamples, round-trip equivalence, and review. Default
chat and disposable scratchpads are excluded.

This provides a practical answer to verification economics: spend deeper
alignment bandwidth at irreversible or high-cost commitment boundaries rather
than imposing maximal ceremony on every token.

### 28. Runtime epistemology connects uncertainty to governed deliberation

Claims carry one of seven durable states: certified, norm-anchored,
procedure-backed, hypothesis, quarantined, superseded, or retracted. Novelty,
uncertainty, stakes, and disagreement can trigger reconciliation; high stakes
force a tribunal; silent overwrite of durable claims is forbidden; calibration
evidence is required.

This overlaps CCA and likely shares lineage. It should not be double-counted as
independent validation. The book-worthy addition is the trigger policy linking
fast paths to explicit epistemic tags and deep review to stakes/disagreement.

### 29. Verification depth should scale with difficulty and disagreement

The recursive verifier policy assigns deeper chains and more parallel
verifiers to harder tasks, requires a heterogeneous critic/tribunal/self-
reflection pool, invokes a verifier-of-verifiers, and bounds unresolved
disagreement.

Again, its exact floors are design choices. The mechanism strengthens governed
deliberation: scale verification topology with difficulty, preserve dissent,
and make unresolved disagreement a budgeted terminal state rather than an
average.

### 30. Run effects and mutations need separate receipts

Competitive windows produce a run contract, execution graph, gate bundle,
verdict, release bundle, effect log, replay check, semantic patch, and
obligation bundle. Effect rows carry capability and policy identity plus
request/response digests. Source-of-truth mutations are accepted only when
their semantic object IDs and obligations resolve to passing evidence.

This is a particularly strong artifact-graph pattern: execution proof and
mutation authorization are adjacent but distinct. A run may have replayable
effects without earning permission to change the canonical system.

### 31. Trace-to-training exchange needs minimization and anti-gaming controls

The trace fabric encrypts raw traces, expires them on a retention schedule,
keeps compact training capsules, filters by quality/novelty/utility, and bounds
payouts with daily decay to reduce spam.

The book should treat raw interaction retention, distilled learning artifacts,
training eligibility, and incentive eligibility as separate decisions. A trace
that is useful for debugging is not automatically safe for training or worthy
of reward.

### 32. Embodied and world-execution paths require stronger envelopes

Worldpacks compile semantic intent into simulation entities, interventions,
parallel branches, and reporting requirements. World-execution jobs derive
stable IDs and checkpoint hashes, support pause/resume/cancel/status, and must
replay byte-for-byte in fixtures.

The embodied safety contract adds target identity, action classes, uncertainty
caps, operator acknowledgment for high-impact actuation, emergency stop,
speed/force bounds, timeouts, and signed commands. These are design obligations,
not proof of deployed hardware safety, but they give the execution chapters a
clear escalation boundary from simulation to physical effects.

### 33. Structured output is a runtime capability with an ablation duty

Grammar-constrained output requires declared grammar mode, strict JSON,
compile-cache floor, and failure telemetry. The contract also requires an
explicit `structured_generation_off` ablation.

This supplies a general experimental rule: architecture features that are
always on cannot establish their own value. Important runtime mechanisms need
an executable disable path and a non-regression comparison.

### 34. Deferred research tracks should remain prototype packets

MoECOT defines many architecture-track contracts—differential attention,
forward MTP, recursive depth, router coupling, KV policy, head compression,
BitNet/ternary edge lanes, limited-memory retrieval, speech upgrades, and
others. Their existence is a research backlog, not evidence of improvement.

The defer-track boundary is valuable: speculative tracks may have typed
packets, cost scorecards, and promotion requirements while remaining excluded
from canonical mutation tiers. The book should distinguish a well-specified
hypothesis from an implemented or supported mechanism.

## Source-reported experimental findings

These results are retained as project-reported context. They were not rerun by
the ASI Stack repository.

### Router and attention

- Disabling shared attention was negative on the project's aggregate board
  (`mean delta reward=-0.030989`, `mean delta bench(all)=-0.101852`, support 4).
- Disabling the world model was also negative in the alpha selection record.
- Latency-oriented shared routing was non-canonical; cross-core routing was
  nearly neutral; noisy top-k produced unstable reward/quality tradeoffs.
- The canonical control kept balanced tag-confidence routing, shared
  attention/world model, structured generation, RLM deliberation, dynamic
  depth, and shared KV; speculative decode, SSM sidecar, and temporal coil
  remained off for alpha.

### World model

- In a five-seed comparison, the project reports graph-overlay world memory at
  `13.4/21` versus `11.0/21` mean full-suite contracts and `5/5` versus `2/5`
  on the targeted world-model suite.
- Because the targeted contracts and implementation share project lineage,
  this is supporting local evidence, not an independent capability result.

### RLM budgets

- Multi-seed and multi-scenario search selected a target-aware budget profile
  by average and minimax scores.
- A later challenger with `+0.003234` raw score was rejected because it incurred
  a clamp penalty while the baseline did not.

### External holdout reality

- Initial alpha rows recorded MMLU-Pro `10.71%`, HumanEval+ `0%`, and MBPP+
  `0%`.
- After holdout-retention and parser/runtime-path fixes, a fresh run recorded
  MMLU-Pro `10.49%`, HumanEval+ `5.49%`, and MBPP+ `6.88%`.
- A speculative-decode contender matched internal aggregate score while coding
  holdouts collapsed to `0%`, so it was rejected.
- Speech holdouts remained near WER `1.0`, despite strong internal speech
  contract scores.

The negative lesson is decisive: internal contract success, training reward,
or architectural coherence cannot substitute for external task performance.

## Exact chapter crosswalk

| MoECOT finding | Primary ASI Stack destination | Secondary destinations | Evidence boundary |
|---|---|---|---|
| Compilation all the way down | `integrated-reference-architecture` | `cognitive-compilation-and-semantic-ir`, `artifact-graphs-audit-logs-and-replay` | Implemented source structure and contracts; no end-to-end ASI result |
| Multi-IR intent chain and ambiguity debt | `cognitive-compilation-and-semantic-ir` | `human-intent-as-a-formal-input`, `intent-to-execution-contracts`, `planning-as-a-control-layer` | Contracts/builders present; semantic quality not reproduced |
| Seed reconstructability taxonomy | `compact-generative-systems-and-residual-honesty` | `rankfold-neuralfold-and-artifact-compression` | Architecture/contract reference; compression claims unverified |
| Proof-carrying passes and localized repair | `cognitive-compilation-and-semantic-ir` | `artifact-graphs-audit-logs-and-replay`, `safety-cases-and-structured-assurance` | Deterministic pass scripts present; not rerun here |
| Registry truth versus disposable projections | `claim-ledgers-and-belief-revision` | `procedural-memory-and-cognitive-loop-closure`, `artifact-steward-agents-and-living-project-governance` | Contract/design plus implementation paths |
| Manifest/runtime identity and target compilation | `stable-capability-fields` | `capability-replacement-and-rollback`, `integrated-reference-architecture` | Compiler reference; deployed parity unverified |
| Semantic portability and target Pareto frontier | `capability-replacement-and-rollback` | `resource-economics-and-token-budgets`, `capability-thresholds-and-deployment-commitments` | Acceptance contracts and scripts; full matrix not rerun |
| Provenance, SLSA, effect logs, patch obligations | `ai-supply-chain-integrity-and-lifecycle-provenance` | `artifact-graphs-audit-logs-and-replay`, `safety-cases-and-structured-assurance` | Builders/gates present; signature/deployment behavior unverified |
| Scoped agent delegation and attestation | `system-boundaries-and-authority` | `runtime-adapters-tool-permissions-and-human-approval`, `scalable-oversight-and-adversarial-ai-control` | Contract/tooling reference; cryptographic enforcement not rerun |
| Hot/warm/cold context, pinning, freeze/thaw | `context-transactions-snapshots-mounts-and-taint` | `virtual-context-abi`, `procedural-memory-and-cognitive-loop-closure` | Deterministic fixture surfaces present |
| Probe-before-expensive-route | `routing-heads-and-specialist-cores` | `resource-economics-and-token-budgets`, `planning-as-a-control-layer` | Gate scripts present; production routing impact unverified |
| Memory consolidation and epistemic promotion | `procedural-memory-and-cognitive-loop-closure` | `claim-ledgers-and-belief-revision`, `data-engines-continual-learning-and-unlearning` | Contract thresholds are design policy, not empirical laws |
| World-state contradiction repair | `claim-ledgers-and-belief-revision` | `procedural-memory-and-cognitive-loop-closure`, `planning-as-a-control-layer` | Source-reported A/B only |
| Router/fuzzy/RLM health and clamp penalty | `routing-heads-and-specialist-cores` | `governed-deliberation-and-test-time-scaling`, `resource-economics-and-token-budgets` | Project-reported experiments, not reproduced |
| Three-copy round-robin critique/repair/collapse | `policy-optimization-and-learning-from-feedback` | `governed-deliberation-and-test-time-scaling`, `scalable-oversight-and-adversarial-ai-control` | Trainer architecture; memory composition is not parameter merge |
| Flood generation ledger and mutation ladder | `open-ended-improvement-engines` | `recursive-self-improvement-boundaries`, `artifact-steward-agents-and-living-project-governance` | Implemented/control contracts; capability uplift unverified |
| Maintenance packets, debt caps, simplification credit | `artifact-steward-agents-and-living-project-governance` | `benchmark-ratchets-and-anti-goodhart-evidence`, `recursive-self-improvement-boundaries` | Deterministic governance implementation reference |
| Scale-indexed alignment obligations | `scalable-oversight-and-adversarial-ai-control` | `constitutional-alignment-substrate`, `safety-cases-and-structured-assurance` | Contract requirements do not prove non-bypassability |
| Expensive-commitment alignment gate | `capability-thresholds-and-deployment-commitments` | `human-intent-as-a-formal-input`, `verification-bandwidth-and-context-adequacy` | Design contract; thresholds and effectiveness unverified |
| Runtime epistemology and recursive verification | `governed-deliberation-and-test-time-scaling` | `claim-ledgers-and-belief-revision`, `moral-uncertainty-and-value-conflict` | Overlaps CCA lineage; not independent validation |
| Trace-to-training minimization | `data-engines-continual-learning-and-unlearning` | `policy-optimization-and-learning-from-feedback`, `model-weight-custody-and-hardware-roots-of-trust` | Runtime/design reference; privacy and anti-gaming effect unverified |
| External-holdout mismatch and harness repair | `benchmark-ratchets-and-anti-goodhart-evidence` | `evidence-states-and-claim-discipline`, `capability-thresholds-and-deployment-commitments` | Strong negative project record; exact runs not replayed |
| Worldpack, long-running jobs, embodied envelope | `labor-os-and-typed-jobs` | `runtime-adapters-tool-permissions-and-human-approval`, `security-kernel-and-digital-scifs` | Mostly contract/fixture evidence; no deployed hardware-safety claim |

## Negative lessons and non-claims

1. Internal benchmark saturation can make architectural toggles look stronger
   than external holdouts justify.
2. A reward increase can coexist with worse routing or holdout quality.
3. A generated target folder or descriptor is not proof of semantic/runtime
   portability.
4. A JSON contract and a deterministic fixture prove specification discipline,
   not that a deployed runtime enforces the contract.
5. Local thresholds written into contracts are policy choices unless an
   external calibration record supports them.
6. World-sensitive tests designed alongside a world model are not independent
   evidence of general world modeling.
7. Collapse over adaptation memory is not model-weight merging or ensemble
   inference.
8. A frozen fuzzy profile proves repeatable configuration, not expert quality.
9. A tiny search-score gain that depends on deployment clamping is not a
   robust policy improvement.
10. A feature toggle such as push-to-talk should not be confused with an
    architecture lever.
11. Benchmark harness retention, parser, argument, and output-path bugs can
    create false zeroes or erase evidence; fixes require a fresh baseline.
12. Strong internal speech contracts coexisted with external WER near one.
13. The project's alpha was explicitly far from flagship external quality;
    architecture breadth did not remove the base capability bottleneck.
14. Document and contract abundance can itself create handoff confusion. The
    active index/deprecation boundary is an important corrective.
15. `project_manifest.md` remained a largely empty generated draft despite a
    highly developed actual architecture, illustrating that stale governance
    documents should not outrank live source truth.
16. `autonomous_swarm_training_architecture.md` duplicated the Flood training
    document and title, showing how copied architecture prose can falsely imply
    a distinct subsystem.
17. External-source citations inside project research notes remain secondary
    source context until the book ingests and reviews those primary sources.
18. The local-only inference-sovereignty rule is a project constraint, not a
    universal ASI requirement.
19. No project material inspected here establishes AGI, ASI, alignment,
    corrigibility, safe self-improvement, or production security.

## Cross-project provenance questions

- CCA and MoECOT share SBL, seed classes, epistemic commitment tiers,
  contradiction revision, governed tribunals, mutation scopes, benchmark
  truth, and compiler-first doctrine. These should be treated as one evolving
  lineage until commit/history review identifies primary origins.
- BeastBrain appears to be earlier lineage for durable memory, graph/lattice
  navigation, and local organism framing.
- Corben's Trainer likely contains predecessor implementations for
  round-robin/curriculum/checkpoint/holdout machinery.
- Corben's Best Model Possible may contain earlier architecture-search and
  external-holdout evidence that explains MoECOT's selected defaults.
- BugBrain likely supplies edge/embedded target and hardware-root lessons used
  by MoECOT's target compiler and embodiment envelopes.

Until those projects are mined, repeated mechanisms are not counted as
independent support.

## Book decisions from this pass

1. Do not add a new MoECOT-specific chapter. Its mechanisms already map to
   existing layer owners.
2. Add MoECOT as a pinned local implementation-reference source distinct from
   the existing connector-only `moecot` document record.
3. Use project-reported numeric results only in bounded source notes or clearly
   labeled implementation-reference prose unless reproduced.
4. Prioritize five additions to existing chapters:
   - compilation all the way down;
   - ambiguity debt and applied localized-repair receipts;
   - semantic portability rather than artifact emission;
   - clamp-safe resource policy promotion;
   - maintenance packets plus self-improvement growth guards.
5. Preserve the external-holdout mismatch as a central anti-Goodhart case.
6. Defer exact Appendix C support transitions until cross-project provenance
   and claim-level passage mapping are complete.

## Remaining work before MoECOT is fully mined

- Inspect implementation symbols for Registry V2, semantic pass execution,
  model compiler target planning, Flood/superloop mutation, and evidence
  builders, not only their architecture docs and contract envelopes.
- Classify all 124 semantic contracts as implemented-and-gated, implemented
  partial, fixture-only, design-only, deferred-track, or historical.
- Inspect retained source-reported run artifacts for checksum/lineage
  consistency and distinguish canonical evidence from stale mirrors.
- Compare MoECOT mechanisms against BeastBrain, BugBrain, Best Model, Trainer,
  and CCA so inherited ideas receive one primary provenance chain.
- Add claim-level chapter mappings only after that deduplication pass.
- Review primary external sources cited by MoECOT separately before using them
  as book support.
