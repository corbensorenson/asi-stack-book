# Source Note: PlanForge

| Field | Value |
|---|---|
| Source ID | `planforge` |
| Source family | Four-tab Google Docs export: original *Universal Hierarchical Task Orchestrator* draft; Cognitive Compiler public-release draft; revised Cognitive Compiler draft without the product roadmap; embedded compiler-architecture export |
| Author / date | Corben Sorenson with source-reported AI collaboration; December 26, 2025 and January 27, 2026 variants |
| Ingestion date | 2026-06-24; fidelity audit 2026-07-31 |
| Canonical local cache | `sources/raw/google_docs/planforge.txt`; SHA-256 `a429b6312668a53fc12982f7ee06b33d94794fb392e2126a57b5afb2d4c32a07` |
| Separate variant | `planforge_compiler_arch` is byte-identical to Tab 4 after removing its UTF-8 BOM and the enclosing Tab 4 marker; it is not independent corroboration. |
| Public boundary | The Google Docs URL is inventoried; the raw cache is not published by this note. |
| Evidence boundary | Conceptual architecture, illustrative equations, design examples, synthetic arithmetic scenarios, implementation suggestions, and related-work claims. No PlanForge code, natural-task trace, scheduler run, quality result, cost result, latency result, safety result, or independent reproduction is supplied. |

## Claim Boundary and Status

The durable proposal is a planning control plane that compiles an accepted
goal into typed obligations, optimizes their dependency graph, estimates the
least costly adequate worker for each obligation, schedules work under cost and
deadline constraints, and hands a versioned schedule to a monitored runtime.
This is an architectural argument. The compiler analogy, hierarchical
decomposition, DAG scheduling, critical-path slack, tier escalation, and
speculative execution are established design patterns or proposed composition;
the paper does not establish that PlanForge implements or improves them.

The family repeatedly describes synthetic scenarios as “validation” and quotes
60–85% routine-task token savings. The actual support is two hand-calculated
examples using assumed per-task prices, serialized baseline time, fifty-way
parallelism, no API rate-limit bottleneck, and no measured plan quality,
dependency truth, worker adequacy, verification, merge, retry, coordination, or
failure cost. These figures remain source-reported illustrations and cannot
support efficiency, reliability, scalability, or benchmark claims.

Tab 2 calls a Python/NetworkX engine “current,” but the source packet contains
no repository, code, artifact, execution receipt, or reproducible benchmark.
The book therefore records the proposed implementation, not implementation
existence. Comparisons claiming other frameworks have “none” for optimization
or tiering are dated, coarse, and unverified; they are research leads rather
than novelty evidence.

## Thesis

Agentic work fails when one probabilistic loop both plans and executes, applies
one expensive capability level everywhere, serializes independent work, and
commits before plan refinement. PlanForge inserts a compiler-like boundary:

`accepted goal -> raw task tree -> typed/optimized DAG -> tiered schedule ->
Watchdog runtime -> observations and scoped replan`.

The central economic idea is **intelligence arbitrage**: use the least costly
worker that has a qualified probability of satisfying the node's adequacy
contract, and reserve expensive or scarce cognition for nodes whose demand,
risk, uncertainty, or critical-path position justifies it. The durable version
is not “always use the smallest model.” It is governed heterogeneous routing
under dependency, quality, verification, authority, and recovery constraints.

## Conceptual Primitives

- **Goal $G$.** A high-level objective already admitted by the intent and
  authority layers; planning does not manufacture authorization.
- **Primitive schema $P$.** Versioned executable operations with typed
  arguments, preconditions, postconditions, effects, output contracts,
  idempotence, authority, verifier, and recovery behavior.
- **Raw task tree $T_{raw}$.** Recursive candidate decomposition before merge,
  dependency, feasibility, or adequacy qualification.
- **Optimized DAG $DAG_{opt}$.** Acyclic obligation graph after proposed
  deduplication, subtree consolidation, consistency checks, and dependency
  annotation. “Optimized” is a stage name, not evidence of global optimality.
- **Semantic hash.** An embedding or other similarity key that proposes
  possible common work. A threshold such as cosine similarity above 0.92 is an
  illustrative retrieval rule, not semantic identity.
- **Minimum Viable Intelligence (MVI).** The lowest-cost route predicted to
  satisfy a node's adequacy contract at an accepted risk; not one scalar IQ,
  model-size tier, or permanent worker property.
- **Worker $w$.** A script, tool, model, service, robot, or human with
  capability, context, authority, cost, latency, capacity, privacy, and
  failure/recovery contracts.
- **Critical path and slack.** The longest dependency-constrained duration path
  and the delay tolerance of off-path nodes. Both depend on uncertain duration,
  queue, retry, and merge estimates.
- **Schedule $S$.** A versioned mapping from qualified nodes to workers, start
  windows, dependencies, budgets, fallback, cancellation, and merge rules.
- **Watchdog.** Runtime supervisor that validates schemas, observes execution,
  applies permitted retry/escalation, and requests replanning. It does not prove
  the plan or authorize effects.
- **Lazy-start speculation.** A delayed stronger route for selected critical
  nodes while a cheaper route begins first; cancellation, duplicate work, and
  side-effect isolation are part of the cost and safety contract.

## Interfaces, Artifacts, and State Machines

The front end consumes a versioned command contract plus an explicit primitive
registry. It emits candidate nodes with source spans and a stop reason for each
leaf. The middle end emits merge proposals, dependency proposals, consistency
findings, pre/postcondition annotations, and an optimized graph receipt. The
back end consumes route profiles, duration and failure estimates, concurrency
limits, budgets, deadlines, and verifier capacity; it emits a schedule plus
unassigned or blocked residuals. The runtime consumes only dispatchable nodes
and returns observations, artifacts, effects, failures, costs, and replan
requests.

A useful node lifecycle is `proposed -> typed -> dependency_checked ->
route_pending -> dispatchable -> dispatched -> observed -> verified ->
completed`, with explicit `blocked_context`, `blocked_authority`,
`blocked_rights`, `blocked_dependency`, `blocked_verification`, `failed`,
`residualized`, `replanned`, and `stopped` branches. A retry remains the same
obligation with a new attempt identity. A replan creates a new graph version,
invalidates affected future nodes and routes, and preserves unaffected work
only after dependency and assumption closure.

The planner/executor boundary is strict. Intent owns goals and constraints;
Cognitive Compilation owns semantic and target lowering; World Models and
Context owners supply observations; Routing and Stable Capability Fields
qualify workers; Resource Economics owns complete cost; Runtime and Security
own effects; Verification judges outputs; Artifact Graphs preserve lineage;
and Evidence States alone can change book claims. The scheduler can recommend
a worker and start time but cannot grant tools, spending, publication,
physical-effect, human-management, or evidence authority.

## Mechanisms

### Front end

Recursively apply a decomposer to a nonprimitive obligation, preserving
alternative decompositions, until each leaf either binds to a primitive schema
or terminates as clarification, deferral, human planning, no-plan, or residual.
Breadth/depth limits, token and time budgets, coverage checks, and cycle/recursion
guards are part of the record. Argument canonicalization normalizes types and
units; it does not resolve ambiguity without authority.

### Middle end

Generate exact-duplicate and semantic-merge candidates; compare parameters,
consumers, authority, rights, state epochs, side effects, quality predicates,
and downstream meanings before merging. Consolidate shared preconditions only
when observation freshness and consumers align. Infer typed data, control,
temporal, semantic, authority, rights, evidence, resource, state, and recovery
dependencies. Reject contradictions, self-dependencies, cycles, missing
preconditions, unsatisfied effects, and unowned merges. Preserve the raw tree,
rejected merges, and split/rollback path.

### MVI and route qualification

The source sketches a logistic classifier over task embeddings and complexity
features, with historical lower-tier failure rates used to raise the proposed
tier. The durable mechanism instead estimates, for every node/route pair,
failure probability and consequence, data coverage and age, task-family and
context match, tool/format compatibility, latency distribution, verifier
availability, fallback cost, and uncertainty. Unknown primitives default
conservatively. An illustrative “above 20% failure, bump one tier” rule is not a
universal threshold. Tier names and named vendor models are dated examples.

### Scheduler

The source proposes HEFT, critical-path scheduling, greedy list scheduling,
exact solvers for small graphs, or evolutionary search. One illustrative
objective minimizes worker-duration cost plus urgency-weighted sink finish time
under a deadline:

$$
J=\sum_i C(w_i)D(n_i)+\lambda\max_{n\in sinks}Finish(n).
$$

The competent objective also constrains node adequacy, authority, rights,
capacity, context, verifier load, retries, merge, and recovery, and separately
reports makespan, money, compute, energy, human work, risk, and residuals.
Zero-slack nodes may justify faster routes; positive slack creates a cheaper
route option. Uncertain predictions prevent the heuristic schedule from being
called optimal.

### Watchdog runtime

Validate input/output schemas and exact job identity; observe start, heartbeat,
artifact, effect, failure, verifier, and completion events; retry only if
idempotence or compensation permits; carry structured error context into a
qualified escalation; and request a replan on changed assumptions or
dependencies. Lazy-start speculation launches a stronger route near a declared
latency quantile, cancels it if the first route qualifies in time, and otherwise
reduces takeover delay. Both attempts, cancellations, duplicate effects,
privacy exposure, capacity, and rate-limit pressure stay in the denominator.

## Assumptions and Invariants

- The input goal has an exact contract and authority ceiling before planning.
- Decomposition completeness is evaluated; reaching schema-like leaves does not
  prove the goal is covered or feasible.
- A semantic atom is not an executable primitive without environment, operand,
  effect, evidence, authority, and recovery binding.
- Acyclicity is necessary but cannot prove dependency truth, completeness, or
  correct temporal semantics.
- Embedding similarity proposes merges; it never proves obligation identity.
- Every merge preserves consumers, effects, authority, rights, provenance,
  downstream meaning, and a reversible split.
- MVI is node-, route-, environment-, epoch-, and adequacy-contract-specific.
  Model size, price, brand, or historical tier is not sufficient.
- Worker failure data include selection denominators, attempts, task mix,
  verifier coverage, shifts, and censored or escalated outcomes.
- Scheduling occurs only after feasibility, route eligibility, verifier,
  fallback, recovery, and resource predicates are visible.
- Parallel and speculative work is isolated from irreversible effects until a
  commit owner accepts one result.
- Replanning is prospective and versioned; it cannot rewrite failed attempts,
  costs, negative knowledge, or effects out of history.
- The complete ledger includes planner inference, embedding and merge search,
  queueing, context preparation, coordination, verification, retry, canceled
  work, repair, human review, merge, fallback, and residual custody.
- A planner may emit dispatch requests, never self-granted execution,
  publication, spending, deployment, or support authority.

## Evidence

A competent PlanForge campaign uses natural heterogeneous tasks with hidden
obligations, dependencies, bottlenecks, tool/context needs, authority and rights
traps, ambiguous aliases, failures, and replanning shocks. Baselines include a
direct strong model, a single agent loop, human-authored workflow, HTN/PDDL or
workflow planners where applicable, tree/search planning, no-tier DAG
scheduling, static routing, HEFT/list scheduling without learned MVI, and the
full governed policy. Every arm receives matched models, tools, context,
authority, budgets, deadlines, verifier capacity, and retry rules.

Measure obligation coverage; primitive typing; dependency precision/recall;
merge precision/recall; feasibility; selected-route adequacy and calibration;
critical-path prediction; accepted completion and downstream utility; unsafe or
unauthorized effects; abstention and missed help; retry, replan, recovery, and
merge correctness; latency and tails; compute, tokens, money, energy, human and
coordination work; privacy and rights burden; and total useful cost. Preserve
all alternatives, blocks, failures, canceled work, and residuals.

The proposal narrows or loses when direct/human/static baselines match outcomes
at lower total cost; decompositions omit or invent obligations; dependency
models remain unreliable; semantic dedup creates more incorrect merges than
useful reuse; MVI is uncalibrated or merely proxies model price; critical-path
estimates do not improve scheduling; tiering raises quality failures; parallel
merge and coordination erase latency gains; speculation causes duplicate
effects or cost overruns; Watchdog escalation fails to recover; replanning
cannot localize invalidation; or transfer fails across tasks, models, tools,
languages, organizations, and time.

The source's two synthetic scenarios are retained only as arithmetic examples.
Scenario A assigns 30 scrapes, 15 summaries, and 5 syntheses to assumed tiers
and reports $1.50/300s versus $0.21/65s. Scenario B assigns 2 configuration
updates and 18 refactors and reports $0.60/120s versus $0.541/~115s. They have
no observed outputs, confidence intervals, raw traces, planner work, rate-limit
model, failure/repair, or verifier denominator and therefore establish no
empirical result.

## Failure Modes

- **Decomposer hallucination and omission:** a polished DAG can invent tools,
  miss obligations, or hide ambiguity; dry-run checks need independent
  environment and obligation evidence.
- **Semantic merge corruption:** false aliases combine different actors,
  effects, epochs, or consumers; false negatives duplicate sensitive or costly
  work.
- **Cold-start and feedback bias:** lower-tier failures may be overrepresented
  because hard tasks are selectively assigned, while escalated success launders
  the first route's inadequacy.
- **Capability-tier laundering:** price, parameter count, or prestige becomes
  “intelligence,” hiding tool access, context, verification, safety, and domain
  competence.
- **Dependency and critical-path fantasy:** missing shared bottlenecks, queueing,
  rate limits, human review, and merge gates produce fake parallelism.
- **Speculative side effects:** duplicate messages, writes, purchases, or
  releases occur when cancellation is not transactional.
- **Error-context poisoning:** a failed worker's misleading diagnosis biases the
  escalated route; error context remains evidence, not truth.
- **Scheduler objective capture:** visible cost and makespan improve by moving
  quality, repair, review, privacy, or residual work outside the objective.
- **Planner authority expansion:** learned decompositions add goals or means,
  worker bidding bypasses policy, or a Watchdog turns retry into unauthorized
  persistence.
- **Marketplace and hive risks:** worker bids can misstate capability, leak task
  data, collude, or create unreviewed jurisdiction and labor obligations.
- **Variant/novelty inflation:** duplicated tabs, named frameworks, and
  promotional comparisons are counted as independent evidence.

## Cross-Paper Synthesis

- **VIEA and Human Intent:** PlanForge consumes an accepted command contract;
  it cannot infer authority while decomposing structure.
- **Cognitive Compilation:** PlanForge owns obligation/dependency/schedule IR;
  Cognitive Compilation owns semantic and target lowering. “DAG as machine
  code” is an analogy until target execution semantics are bound.
- **Talos:** PlanForge requests routes and emits dispatchable node packets;
  Talos owns typed jobs, isolation, tools, effects, audit, and delivery.
- **Reflexive Router and Octopus:** route systems return qualified candidates;
  MVI proposes the least costly adequate class but cannot install or authorize a
  worker.
- **Resource Economics and TokenMana:** cost and deadline are vector budgets,
  not token price alone; capacity, verification, retry, human work, and degraded
  operation remain visible.
- **Aletheia/Spinoza:** schema checking and falsification inspire the Watchdog,
  but a runtime validator is not an independent judicial tribunal or proof.
- **BeastBrain/personal hives:** PlanForge can schedule heterogeneous local and
  remote workers, but hive policy, privacy, partitions, identity, and bid
  governance precede optimization.
- **Procedural memory and RMI:** successful recurring subgraphs can become
  reusable workflows only after outcome evidence, residuals, regression tests,
  expiry, and retirement—not because a subtree was cached.

## Claims To Add Or Update

- Treat recursive decomposition as candidate obligation coverage, not proof
  that the goal has been correctly or completely compiled.
- Require executable primitive bindings rather than stopping on a semantic
  verb or free-text action description.
- Treat embedding similarity as a merge proposal whose consumers, effects,
  authority, rights, state, and rollback split must qualify.
- Define MVI as a calibrated node-route adequacy estimate with uncertainty,
  shift, verifier, and fallback costs rather than a static model-size tier.
- Use critical-path slack as an opportunity for qualified substitution while
  reporting uncertain duration, queue, retry, verification, merge, and repair.
- Separate Watchdog schema validity, route escalation, runtime outcome,
  authority, and evidence state.
- Count both sides of lazy-start speculation and block duplicate irreversible
  effects without isolation and commit control.
- Retain the source's savings figures only as synthetic arithmetic examples.

## Open Questions

- Which primitive schema gives broad task coverage without turning semantic
  labels into underspecified executable operations?
- How can decomposition coverage and dependency recall be evaluated on natural
  tasks without giving one planner privileged latent structure?
- What positive and negative controls make semantic merge qualification
  sensitive to aliases, homonyms, changing state, and side effects?
- Can MVI calibration transfer across model revisions, tools, organizations,
  languages, and new primitive families?
- When does critical-path-aware heterogeneity improve accepted outcomes after
  queueing, verification, repair, and merge costs?
- Which runtime effects can safely use speculation, retry, or compensation?
- How should worker-market bids be verified without leaking task data or
  allowing the scheduler to bypass governance?

## Book Chapters Supported

- `human-intent-as-a-formal-input`
- `planning-as-a-control-layer`
- `cognitive-compilation-and-semantic-ir` through the exact compiler variant
- `governed-world-models-and-reality-grounding`
- `personal-compute-hives-and-federated-edge-intelligence`
- `fast-generation-architectures`
- `resource-economics-and-token-budgets`
- `policy-optimization-and-learning-from-feedback`
- `artifact-steward-agents-and-living-project-governance`
- `integrated-reference-architecture`
- `prototype-roadmap`
- `open-research-agenda-and-bibliography-plan`

## Section-Family Coverage

| Source family section | Actual manuscript or durable owner | Disposition and boundary |
|---|---|---|
| Tab 1 abstract/§1 | Planning; Efficient ASI; source note | Orchestration-gap problem and planner/executor separation integrated. No superiority or general bottleneck claim inferred. |
| Tab 1 §2.1 | Human Intent; Planning | Recursive decomposition, primitive-schema stop, raw tree, and breadth/depth limits integrated with clarification and residual branches. |
| Tab 1 §2.2 | Planning; Cognitive Compilation | Exact/semantic dedup, subtree merge, consistency, pre/postconditions, and DAG output integrated with merge qualification and rollback split. |
| Tab 1 §2.3 | Planning; Routing; Resource Economics | Four-tier example and classifier/human override retained as illustrative MVI mechanisms, not universal intelligence levels. |
| Tab 1 §2.4 | Planning; Resource Economics | Partial order, duration estimates, multi-objective assignment, makespan/cost/tier constraints, HEFT/CPM/exact options, parallelism, and fallback integrated. |
| Tab 1 §2.5 | Planning; Talos/Runtime owners | Serialized schedule, execution handoff, and feedback-driven replan integrated without planner authority. |
| Tab 1 §§3–4 | source note; external-resolution backlog | Claimed advantages and HTN/TAMP/agent/BT/GOAP/learned-planner relations retained as hypotheses/comparators. No novelty or performance claim imported. |
| Tab 1 §5 | Prototype Roadmap; source note | Python prompting, NetworkX, classifier, OR-Tools/Dask, JSON Schema, sandbox, and human-gate suggestions retained as implementation options, not existing artifacts. |
| Tab 1 §§6–8 | receiving-chapter examples; research backlog; source note | Software, research, enterprise, robotics use cases; learned decomposer; realtime replan; subtree cache; formal verification; worker marketplace; conclusion retained as research directions. |
| Tab 2 abstract/§1 | Planning; source note | Cognitive Compiler, uniformity/linearity framing, and 60–85% language retained with synthetic-only boundary. |
| Tab 2 §2 | Planning; Cognitive Compilation | Front/middle/back stack, typed argument canonicalization, semantic hash, MVI classifier/failure rule, and tier examples integrated with stronger boundaries. |
| Tab 2 §3 | Planning; Resource Economics | NP-hard scheduling framing, greedy/HEFT, objective, urgency factor, critical path, and slack arbitrage integrated as heuristics. |
| Tab 2 §4 | source note; mature campaign | Both synthetic arithmetic scenarios retained exactly as non-empirical examples; no book performance claim. |
| Tab 2 §5 and references | source note; Appendix H backlog | Feature table and HEFT/SBERT/LangGraph/AutoGen/MetaGPT references retained for independent current verification; “none” cells and novelty claims not admitted. |
| Tab 2 §6 | Planning; Runtime; Fast Generation | Schema validation, tier escalation with error context, and lazy-start speculative execution integrated with idempotence, cancellation, effect, privacy, and cost constraints. |
| Tab 2 §7 | Planning failure modes; source note | Decomposer hallucination, cold-start MVI, and semantic drift retained and broadened. |
| Tab 2 §8 | Prototype Roadmap; Personal Hives; source note | Claimed current Python engine, planned learned decomposer, WASM sandbox, and JSON-RPC worker marketplace retained as unimplemented proposals. |
| Tab 2 §9 | Planning summary; source note | Infrastructure-layer conclusion retained at `argument`. |
| Tab 3 | this ledger; variant reconciliation | Near-duplicate of Tab 2 with product roadmap removed and dry-run wording tightened. Unique editorial decision retained; repeated content is not independent support. |
| Tab 4 | `planforge_compiler_arch` note; Planning; Cognitive Compilation | Separate exact compiler-architecture wording adds BeastBrain-kernel and Aletheia-tribunal analogies plus primitive-atom language; normalized text is duplicated by the separate source file and counts once. |

## Closure Status

**Variant-family and section-family audit complete as of 2026-07-31.** All four
tabs terminate in manuscript integration, durable note retention, a concrete
research obligation, variant deduplication, or an explicit non-claim. The
planning chapter now makes typed primitive stopping, semantic-merge
qualification, calibrated MVI, critical-path slack, Watchdog transitions,
lazy-start speculation, and synthetic-benchmark limits reader-visible. The
Cognitive Compilation chapter now separates semantic atoms from bound
executable primitives.

Closure does not establish a PlanForge implementation, complete decomposition,
dependency truth, correct merge, calibrated MVI, optimal schedule, useful
parallelism, Watchdog recovery, cost or latency saving, quality preservation,
security, reliability, generality, external novelty, production transfer, or
ASI support. The source remains `argument`; reopen on material family or
receiving-chapter drift.
