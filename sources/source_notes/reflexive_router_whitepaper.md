# Source Note: The Reflexive Router

| Field | Value |
|---|---|
| Source ID | `reflexive_router_whitepaper` |
| Source title | The Reflexive Router: A Pre-Deliberative Architecture for Fast, Governed, Tool-Native Intelligence |
| Author / version | Corben Sorenson; version 1.2; July 2026 |
| Ingestion date | 2026-07-16 |
| Canonical local text | `sources/raw/reflexive_router/the_reflexive_router_white_paper_v1_2.md`; SHA-256 `003a693741c40ca96ec3aece5b76ee90ec95a1d6c27ec81a970cff175f509068` |
| Supplied presentation copy | `sources/raw/reflexive_router/the_reflexive_router_white_paper_v1_2.docx`; SHA-256 `52bc04a1bfedaa0fe3a7e530570703bd973849f46b806529f2534509101ace9b` |
| Storage boundary | Both supplied files are retained in the ignored local raw-source cache. This tracked note is public-safe; ingestion does not authorize publication of either raw file. |
| Evidence boundary | The paper explicitly describes an architectural proposal and research agenda. It supplies design rationale, interfaces, algorithms, threat hypotheses, and a proposed benchmark—not an implemented router, measured efficiency gain, verified effect kernel, safe reflex compiler, deployment result, external reproduction, or chapter-core support transition. |

## Thesis

Natural language should be treated as an input and control format, not as a
requirement to invoke a general language model. A persistent pre-deliberative
layer should interpret an authenticated event as a routing problem, admit only
qualified and authorized computations, and use the least general mechanism
that can satisfy the request. Users may explicitly select a route, capability,
or workflow, but direct invocation may bypass inference only—not authority,
type, consequence, verification, or audit controls.

The paper's strongest contribution is the ordering and contract structure of a
larger synthesis:

```text
authenticated event and command plane
-> deterministic and learned route proposals
-> qualification and authority admission
-> bounded single route or execution DAG
-> stable capability or deliberative fallback
-> verifier / effect commit kernel
-> typed result and temporal context
-> governed trace-to-reflex compilation
```

## Mechanisms

1. **Prompt-as-event boundary.** A canonical event envelope keeps principal,
   time, modality, authority, privacy, context handles, and resource budgets
   outside open-ended interpretation.
2. **Explicit command plane before automatic routing.** Route directives,
   direct capability commands, and workflow commands have deterministic
   precedence below constitutional and authority constraints. Failed forced
   routes report typed failure rather than silently falling back.
3. **Qualification before optimization.** A learned router proposes candidates;
   contracts admit them only after schema, entity, temporal freshness,
   authorization, quality, verifier, effect, and fallback obligations hold.
   Generalized cost is minimized only over the qualified set.
4. **Calibrated refusal.** The bounded learned router exposes candidate scores,
   out-of-distribution signals, composite-task detection, and abstention. It
   neither invents capabilities nor gains execution authority.
5. **Semantic-operation routing.** Composite requests become small typed DAGs,
   allowing exact, retrieval, proof, specialist, action, and deliberative nodes
   to differ while preserving dependency and plan provenance.
6. **Stable capability fabric.** Reflexes and callers target semantic contracts,
   not vendor implementations. Replacement requires compatibility in inputs,
   outputs, failure behavior, authority, freshness, quality, and verifier
   expectations.
7. **Action-understanding / effect-commit split.** Natural-language action
   understanding may propose a typed effect; only a narrow Effect Commit Kernel
   may authorize, prepare, commit, observe, verify, and record it. Bound commands
   may skip action interpretation but never the kernel.
8. **Typed result continuity.** Results retain value, route, implementation,
   input identity, valid and recorded time, epistemic state, evidence,
   verification, effects, dependencies, dispatch provenance, and context
   handles. Rendering is downstream of the authoritative packet.
9. **Temporal Chronicle.** Entity, event, state, claim, plan, prediction, and
   counterfactual records remain distinct and carry valid time, transaction
   time, provenance, derivation, contradiction, and epistemic status.
10. **Governed reflex compilation.** Repeated verified traces may be distilled
    into a rule, query, cache, workflow, program, solver template, or specialist
    policy only after negative-space guard synthesis, static analysis,
    replay/differential testing, shadowing, qualification, signed promotion,
    monitoring, expiry, and decompilation.
11. **Joint routing economics.** Fast-path coverage is meaningful only beside
    wrong-fast-path rate, qualified coverage, route regret, end-to-end quality,
    verification cost, monitoring cost, effects, and abstention. “Useful Reflex
    Efficiency” must not become a score that hides unsafe or useless outputs.

## Claim Boundary and Status

- The source is a Corben-authored architectural synthesis and research plan;
  it is not independent evidence for the novelty, safety, performance, or
  deployability of the proposed system.
- “Reflexive” means a guarded, non-deliberative execution path, not an
  uncontrolled low-latency reaction and not a claim about consciousness.
- “Minimum sufficient compute” is constrained optimization over qualified and
  authorized candidates. It is not permission to choose the cheapest route or
  omit verification, monitoring, human work, recovery, or residual risk.
- User-directed dispatch constrains inference inside an existing authority
  envelope. It does not confer new permissions or make a direct command safe
  by construction.
- The Chronicle and typed-result schemas improve separation and traceability;
  neither structure establishes the truth of its contents.
- Trace-to-reflex compilation is a proposed governed lifecycle. Repetition,
  fluency, user silence, or model agreement is not qualification evidence.
- All manuscript uses remain `Design rationale` / `argument`; no Appendix C
  support transition follows from this source audit.

## Conceptual Primitives

- **Canonical event:** authenticated ingress identity plus literal payload,
  time, modality, principal, tenant, context, authority, privacy, budget, and
  requested route constraints.
- **Command descriptor:** a scoped, versioned binding to a route, capability,
  effort profile, or workflow with typed arguments and lifecycle controls.
- **Reflex:** a bounded executable mapping whose guard, authority, resource,
  verifier, failure, expiry, and fallback contracts are explicit.
- **Route proposal / admission:** a candidate score or decomposition is
  non-authoritative; qualification and authority predicates determine
  eligibility.
- **Qualified plan:** one capability call or a bounded semantic-operation DAG
  whose node and dependency obligations hold for the present event.
- **Stable capability:** a semantic operation separated from replaceable
  implementations and their consumer-relative qualification.
- **Typed result packet:** the authoritative value envelope from which prose,
  UI, speech, prompts, and audit views are derived.
- **Temporal Chronicle:** bitemporal, provenance-aware records that keep
  entities, events, states, claims, plans, predictions, and counterfactuals
  distinct.
- **Reflex candidate:** a proposed rule, query, cache plan, workflow, program,
  solver template, or bounded specialist policy derived from eligible traces.
- **Decompilation:** removal of an active fast path plus restoration of the
  deliberative parent and invalidation of dependent aliases, caches, routes,
  workflows, and descendants.

## Interfaces, Artifacts, and State Machines

The paper defines one ordered interface but assigns authority to separate
owners: event normalization; authenticated command parsing; authority/hazard
gating; deterministic and learned proposal; qualification; bounded planning;
stable-capability resolution; effect custody; verification; result commit;
context and Chronicle projection; trace analysis; and governed compilation.
The common trace must retain ingress mode, proposal denominator,
disqualifications, selection, fallback, requested and realized effort,
capability versions, effects, observations, verification, terminal outcome,
and downstream dependencies.

Three artifact families carry most of the design:

1. reflex and command descriptors with scope, precedence, schemas, dynamic
   defaults, authority, effects, budgets, verifier, fallback, provenance,
   expiry, and rollback;
2. typed plan/result/Chronicle records preserving dependency and temporal
   semantics across heterogeneous executors; and
3. compilation evidence binding positive, negative, boundary, adversarial,
   replay, differential, shadow, canary, drift, quarantine, and rollback data
   to an exact candidate.

The proposed reflex lifecycle is `PROPOSED -> STATICALLY_CHECKED ->
REPLAY_TESTED -> SHADOWING -> QUALIFIED -> CANARY -> ACTIVE -> MONITORED`, with
revision, quarantine, revocation, rollback, or decompilation as explicit exits.
No transition authorizes itself.

## Assumptions and Invariants

- Only authenticated user-control input can activate command syntax; retrieved
  or generated command-looking text is inert.
- Constitutional and platform invariants, authority, and consequence policy
  precede user commands; user commands precede automatic optimization.
- A user may bypass inference but never authentication, authorization, typing,
  consequence policy, verification, audit, expiry, or revocation.
- Learned components propose; deterministic contracts and policy authorize.
- Optimization occurs only over qualified candidates; high confidence is not
  qualification.
- The LLM is one capability in the fabric, not an exempt control-plane owner.
- Every effectful path converges on one Effect Commit Kernel; preparation,
  commit, observation, verification, and compensation remain distinct.
- Plans, predictions, claims, observations, events, states, counterfactuals,
  and fictional records cannot silently substitute for one another.
- A typed structure can still carry false evidence; provenance and verifier
  independence remain separate obligations.
- Procedure guards are at least as important as bodies; positive examples
  alone cannot define safe applicability.
- Learning from outcomes may change ranking or calibration but cannot learn or
  widen authority.
- Every fast path has an explicit fallback, expiration, quarantine, rollback,
  and decompilation route or remains unqualified.

## Algorithms and Formal Objects

The paper supplies four pseudocode algorithms: dispatch with user overrides,
automatic event routing, reflex compilation, and temporal-fact resolution.
It also defines constrained route selection over a generalized cost vector,
risk–coverage and selective-risk measures, route regret relative to an oracle,
and a break-even condition for compilation after testing and monitoring cost.
These are proposed decision objects, not proved algorithms or measured
estimators. The YAML reflex/command examples, JSON typed-result and benchmark
records, canonical terminal outcomes, and registration checklists are
normative sketches. They belong to protocol and evaluation work until an
implementation binds them to observed behavior.

## Evidence and Falsifiers

The paper would gain empirical support only through matched routes and
resources over natural and adversarial workloads with independent route,
outcome, and effect adjudication. It can be falsified or narrowed if dispatch
overhead erases the savings; wrong fast paths remain high at useful coverage;
qualification is too expensive; OOD abstention fails; bounded decomposition
cannot preserve cross-clause constraints; typed continuity does not improve
downstream accuracy; Chronicle maintenance costs exceed its use; compiled
reflexes fail shifted cases or cannot decompile completely; verifier dependence
launders executor error; or total useful throughput loses after monitoring,
human work, governance, and recovery are included.

## Threats, Costs, and Governance

The complete threat surface includes routing injection, literal-command
activation, rule shadowing, alias cycles, unsafe registry mutation, semantic
cache collision, Chronicle poisoning, privilege amplification, decomposition
bombs, cost amplification, cross-tenant leakage, verifier monoculture, retry
duplication, stale reflexes, context-handle confusion, feedback loops, and
learned self-installation. Governance must cover owners, signatures,
capability diffs, supply-chain dependencies, scopes, precedence, expiry,
review, emergency revocation, and incident custody. Total cost includes
dispatch, execution, verification, monitoring, human review, state, cache and
Chronicle maintenance, invalidation, compilation, rollback, recovery, energy,
latency, money, opportunity cost, and residual risk.

## Cross-Paper Synthesis

- VIEA supplies intent custody, the fast-router/slow-conductor split, artifact
  survival, and transactional integration; Reflexive Router makes the
  event-to-qualified-plan hot path concrete.
- SCF owns durable semantic capability identity, qualification leases,
  reliance invalidation, state and implementation replacement, and lifecycle
  authority consumed by routes and compiled reflexes.
- PlanForge and Cognitive Compilation own graph planning and semantic IR; the
  router may propose a bounded operation graph but cannot absorb their
  planning authority.
- VCM and Context Transactions own durable context, projections, cache keys,
  snapshots, invalidation, and privacy; the Reflex Context Frame is only a hot
  view.
- Spinoza and the claim ledger own epistemic standing and belief revision; the
  Chronicle is not permitted to turn extracted claims into facts.
- Talos and Runtime Adapters own job/effect execution, observations, receipts,
  idempotency, compensation, and human approval; a route receipt is not an
  effect receipt.
- Cognitive Loop Closure owns procedure lifecycle and descendant recovery;
  Reflexive Router contributes the specific trace-to-reflex compiler and
  pre-deliberative consumer.
- Benchmaxxing/RMI own evidence ratchets, residuals, qualification, and
  promotion discipline; ReflexBench is one proposed campaign within that
  broader evidence system.

## Evidence

- The complete 3,489-line Markdown source was read across all 24 sections,
  seven appendices, glossary, and 36 references.
- The paper supplies proposed contracts, four algorithms, worked examples, a
  threat matrix, a phased implementation blueprint, and the ReflexBench
  evaluation design.
- The supplied DOCX was converted read-only for comparison. It carries the same
  version, central thesis, section sequence, major invariants, and conclusion;
  formatting and title extraction differ, so the Markdown digest is the
  canonical passage-review binding.
- All numerical thresholds and budget values in the paper are proposed targets
  or illustrations. No executed benchmark record, raw result set, trained
  router, deployed service, observed effect campaign, or external reproduction
  accompanies the source.
- The paper's own status and non-claims describe it as an architectural
  proposal and research agenda. Its contribution here is design rationale and
  a stronger falsification program.

## Failure Modes

- A command parser that recognizes syntax but silently widens authority is not
  the proposed command plane.
- A route selected by confidence without contract admission does not establish
  qualification-first dispatch.
- A lower-cost route that is stale, ambiguous, unverifiable, unauthorized, or
  outside its tested distribution is not “minimum sufficient compute.”
- A typed packet can faithfully encode a false claim; structure alone does not
  establish truth.
- A semantic cache whose key omits tenant, authority, time, policy, source, or
  schema dependencies can leak or reuse invalid results.
- A direct command that expands into trusted shell, SQL, URL, or prompt text is
  a macro-injection surface, not a typed capability binding.
- A prepared action, tool call, success-shaped receipt, or model narration does
  not establish an observed effect or complete rollback.
- Trace frequency or unchallenged fluent output is insufficient evidence for
  reflex compilation; positive examples underdetermine guards.
- Executor/verifier monoculture, router/evaluator capture, hidden retries, and
  incomplete candidate denominators can manufacture an apparent gain.
- A reflex that cannot be expired, quarantined, decompiled, or rolled back is
  not a governed fast path.
- A benchmark with only easy exact tasks cannot test ambiguous routing,
  abstention, composite planning, temporal continuity, or effect governance.

## Book Chapters Supported

- Primary: `routing-heads-and-specialist-cores`.
- Command and planning: `intent-to-execution-contracts`,
  `planning-as-a-control-layer`.
- Capability and context: `stable-capability-fields`, `virtual-context-abi`,
  `context-transactions-snapshots-mounts-and-taint`.
- Temporal belief and effects: `claim-ledgers-and-belief-revision`,
  `runtime-adapters-tool-permissions-and-human-approval`.
- Learning and evaluation: `procedural-memory-and-cognitive-loop-closure`,
  `resource-economics-and-token-budgets`,
  `benchmark-ratchets-and-anti-goodhart-evidence`.
- Cross-layer composition: `integrated-reference-architecture`.

## Claims To Add Or Update

- Separate routing proposal from route admission: learned scores suggest;
  qualification and authority decide.
- Preserve the user-dispatch invariant that an override can bypass inference
  but cannot bypass enforcement, verification, audit, or revocation.
- Upgrade routing granularity from one label per prompt to bounded
  semantic-operation DAGs with plan provenance and partial qualification.
- Preserve typed value, time, evidence, verifier, effect, dependency, and
  dispatch provenance when non-LLM results enter conversation context.
- Add the procedural-memory hypothesis that repeated verified deliberation may
  compile into a guarded reflex, together with the falsifier that frequency,
  fluency, or positive traces alone cannot justify activation.
- Reject fast-path coverage and Useful Reflex Efficiency as sufficient metrics
  unless useful outcomes, wrong-fast-path, verification, monitoring, effects,
  human work, and total cost remain visible.
- Keep all changes at `argument` until accepted claim-specific transitions
  follow a natural and adversarial campaign.

## Existing-Chapter Decision

**Decision: update existing chapters; do not add a Reflexive Router chapter in
this intake.** The paper is a strong architectural synthesis, but its durable
interfaces already have chapter owners. A standalone chapter would currently
repeat those owners and weaken the book's layer discipline.

| Chapter owner | Material to integrate |
|---|---|
| `routing-heads-and-specialist-cores` | Pre-deliberative ordering; deterministic command path; bounded learned proposals; qualification-first selection; abstention/OOD; atomic versus composite routing; route and plan provenance. |
| `intent-to-execution-contracts` | Canonical event envelope; authenticated route constraints; explicit fallback policy; typed terminal outcomes; preservation of user routing intent. |
| `planning-as-a-control-layer` | Bounded semantic-operation DAGs; partial qualification; dependency, cancellation, retry, and partial-result semantics. |
| `stable-capability-fields` | Stable semantic capability names; consumer-relative descriptors; implementation substitution and compatibility; reflex dependency invalidation. |
| `virtual-context-abi` and `context-transactions-snapshots-mounts-and-taint` | Typed result packets, hot routing projection, context handles, provenance-preserving synthesis, and invalidation. |
| `claim-ledgers-and-belief-revision` | Chronicle separation of events, states, claims, plans, predictions, counterfactuals, valid time, transaction time, correction, and contradiction. |
| `runtime-adapters-tool-permissions-and-human-approval` | Action-understanding versus Effect Commit Kernel; “bypass inference, never enforcement”; consequence-aware prepare/commit, idempotency, observation, compensation, and audit. |
| `procedural-memory-and-cognitive-loop-closure` | Trace eligibility; representation selection; guard synthesis; replay, differential, shadow, promotion, monitoring, and decompilation lifecycle. |
| `resource-economics-and-token-budgets` | Minimum sufficient compute as qualified frontier selection; complete routing, verification, monitoring, human, latency, energy, and risk cost. |
| `benchmark-ratchets-and-anti-goodhart-evidence` | ReflexBench task tracks, strong baseline matrix, wrong-fast-path and verification-escape emphasis, metric anti-gaming, complete denominators. |
| `integrated-reference-architecture` | End-to-end command/automatic route, capability/effect, typed-result, Chronicle, and compiler trace with distinct authorities. |

Reconsider a new chapter only if a real campaign shows that the
**pre-deliberative event-to-qualified-plan interface** owns a stable artifact,
invariant, or failure class that the routing, command, planning, capability,
runtime, memory, and evidence chapters cannot express without conflicting
authority. Topic breadth, source length, or the name “System-0” is not enough.

## Open Questions

- Can one bounded pre-deliberative interface remain useful as the capability
  registry grows without becoming a second open-ended agent?
- Which qualification obligations are cheap enough to preserve a real latency
  and cost advantage?
- How should calibration compose across a DAG with dependent node errors and
  effects?
- Which typed result and Chronicle fields are authoritative, and which remain
  projections owned by context, claim, artifact, or memory ledgers?
- How independent can an outcome evaluator be when executor and verifier share
  a model family, training data, tool, implementation, or organization?
- Which task families are stable enough to compile, and how can negative-space
  guards retain rare consequential exceptions?
- When does decompilation restore the full deliberative path, including caches,
  aliases, downstream workflows, authority, and learned descendants?
- Does observed evidence eventually justify a distinct pre-deliberative
  chapter, or confirm that the existing chapter owners are clearer?

## Completed Argument-Only Book Integration

The source is now assigned in `book_structure.json` to all twelve receiving
chapters. Each chapter contains a bounded owner-specific integration and source
crosswalk entry. The shared vocabulary is anchored by
`schemas/reflexive_dispatch_trace_record.schema.json` and its public-safe valid
fixture, which join event intake, ingress mode, route proposals, qualification,
selection, plan nodes, effect custody, typed result continuity, Chronicle
updates, compilation state, and joint metrics without claiming runtime
behavior. The dedicated validator rejects selected inference/enforcement,
proposal/admission, fallback, effect, provenance, Chronicle, compilation, source
identity, and support-laundering failures.

This completes source-to-manuscript integration at `argument` support. It does
not complete the empirical, causal, transfer, security, or external-literature
program below.

## Remaining Roadmap Work After Prose Integration

1. Extend the finite shared trace into independently owned protocol records
   where implementation pressure shows that one joined record is too coarse.
2. Build a public-safe bounded reference slice that exercises automatic,
   forced-route, direct-command, and workflow paths over the same authority and
   verification kernels.
3. Add negative controls for untrusted command text, silent fallback, stale
   context, ambiguous parses, OOD routing, authority widening, partial effects,
   retry duplication, verifier monoculture, cache collision, Chronicle
   poisoning, premature compilation, and failed decompilation.
4. Expand P4 Campaign 2 into a ReflexBench-derived natural and adversarial
   campaign spanning atomic exact, paraphrase, context-dependent, composite,
   temporal, effectful, adversarial, and trace-compilation tracks.
5. Compare LLM-first, hard-rule-only, learned model routing, semantic cache,
   tool-agent, modular routing, and full reflexive routes under matched models,
   candidate bytes, information, authority, retries, verification, and total
   cost. Use independent route/outcome/effect evaluators.
6. Measure useful task outcomes, wrong-fast-path rate, qualified coverage,
   selective risk, route regret, override fidelity, silent fallback,
   parameter-binding accuracy, OOD abstention, DAG validity, context
   continuity, temporal accuracy, unauthorized effects, verification escape,
   rollback completeness, compilation transfer, latency, and total cost.
7. Attempt trace-to-reflex compilation only after the routing instrument is
   adequate; require varied positive/negative cases, shadow evidence, safe
   activation, drift injection, quarantine, and decompilation.
8. Passage-review the paper's external references against current primary
   sources before treating any novelty, prior-work, security, or performance
   statement as external-literature support.
9. Reconcile results into exact retain, narrow, refute, deprecate, or promote
    dispositions before chapter prose, Appendix C, reader editions, or the X
    synopsis changes.

## Passage Review Map

- Abstract, Executive Summary, §§1–4: system thesis, scope, ordering, canonical
  event, command plane, qualification, capability, effect, result, Chronicle,
  and compiler boundaries.
- §§5–8: reflex contracts, command registry, calibrated learned routing,
  selective risk, qualification predicates, risk classes, route regret, and
  deadline-aware cascading.
- §§9–12: composite DAGs, stable capability fabric, structured effects, typed
  results, context projections, and dispatch provenance.
- §§13–14: bitemporal Chronicle and trace-to-reflex lifecycle.
- §§15–17: algorithms, security invariants, threat model, and non-adversarial
  failure modes.
- §§18–19: ReflexBench, baselines, metrics, launch gates, implementation stages,
  and minimum viable experiment.
- §§20–24 and Appendices A–G: worked boundary cases, prior-work positioning,
  implications, open questions, proposed schemas, outcomes, and checklists.

## Non-Claims

- No standalone chapter is added by this intake.
- No current chapter support state changes.
- The paper is not treated as independent external evidence for its own
  architecture or novelty.
- The supplied DOCX is retained as a presentation copy; the Markdown digest is
  the canonical local text binding for passage review.
- No claimed latency, cost, energy, correctness, safety, compilation, memory,
  temporal, routing, or effect result has been reproduced.
- No raw-source publication, release, deployment, or external post is
  authorized by ingestion.

## Section-Family Coverage

| Paper section family | Actual manuscript or durable owner | Disposition and boundary |
|---|---|---|
| Abstract, Executive Summary, §§1–3 | `routing-heads-and-specialist-cores`; `resource-economics-and-token-budgets`; this note | Interface/executor separation, pre-deliberative thesis, user-directed dispatch, exact invocation, qualification-before-optimization, and non-claims integrated. Minimum sufficient compute remains a proposed constrained objective. |
| §4 architecture overview | `integrated-reference-architecture`; `intent-to-execution-contracts`; `runtime-adapters-tool-permissions-and-human-approval` | Fifteen-component ordering, distinct authorities, shared enforcement convergence, typed results, Chronicle updates, and compiler feedback integrated. The diagram is an architecture contract, not a running system. |
| §5 reflex classes and contracts | `procedural-memory-and-cognitive-loop-closure`; `stable-capability-fields`; this note | Reflex taxonomy, declarative contract fields, guard primacy, precedence/conflict analysis, and effect classes integrated or retained as proposed artifact requirements. |
| §6 User Command Plane | `intent-to-execution-contracts`; `routing-heads-and-specialist-cores` | Route/direct/workflow modes, effort profiles, typed parameters and defaults, context variables, registry scope/namespace, inspection, mutation, supply chain, literal isolation, requested/realized fidelity, and formal dispatch boundary integrated. |
| §7 learned router | `routing-heads-and-specialist-cores` | Bounded hierarchical router, calibrated selective risk, OOD-triggered abstention, outcome learning without authority learning, versioning, shadowing, and rollback integrated. No trained router result imported. |
| §8 qualification-first dispatch | `routing-heads-and-specialist-cores`; `resource-economics-and-token-budgets` | Contract proof obligations, consequence-relative thresholds, generalized cost, route regret, and deadline-aware cascading integrated. Formal expressions remain proposed targets. |
| §9 composite requests | `planning-as-a-control-layer`; `routing-heads-and-specialist-cores` | Semantic-operation DAGs, bounded decomposition, node-local partial qualification, concurrency/cancellation/retry, and plan provenance integrated. Planning authority remains outside Routing. |
| §10 Stable Capability Fabric | `stable-capability-fields`; `integrated-reference-architecture` | Semantic names, consumer-relative descriptors, typed composition, deliberation as one capability, and shared inside/outside capability access integrated. No substitution result imported. |
| §11 structured actions | `runtime-adapters-tool-permissions-and-human-approval`; `claim-ledgers-and-belief-revision` | Action-understanding/effect-commit split, consequence-aware confirmation, idempotency, partial failure, compensation, result receipts, and action/observation/state Chronicle writes integrated. |
| §12 typed results and continuity | `virtual-context-abi`; `context-transactions-snapshots-mounts-and-taint` | Authoritative packet versus rendering, hot projections, provenance-preserving synthesis, dispatch provenance, dependency closure, and invalidation integrated. A typed packet does not prove truth. |
| §13 Temporal Chronicle | `claim-ledgers-and-belief-revision`; `context-transactions-snapshots-mounts-and-taint` | Entity/event/state/claim/plan/prediction/counterfactual separation, valid/transaction time, epistemic status, provenance, event-sourced views, temporal relations, scoped writes, and poisoning/invalidation integrated or retained. |
| §14 reflex compilation | `procedural-memory-and-cognitive-loop-closure`; `stable-capability-fields` | Representation selection, trace eligibility, distillation, negative-space guards, static analysis, replay/differential/shadow stages, signed promotion, monitoring, economics, expiry, and decompilation integrated. No compiler result imported. |
| §15 algorithms | this note; `schemas/reflexive_dispatch_trace_record.schema.json`; protocol/evaluation backlog | Four algorithms are retained as normative pseudocode and finite design-record targets. They are not presented as implemented or correct algorithms. |
| §§16–17 security and failure model | `intent-to-execution-contracts`; `runtime-adapters-tool-permissions-and-human-approval`; `context-transactions-snapshots-mounts-and-taint`; `benchmark-ratchets-and-anti-goodhart-evidence`; this note | Instruction/data isolation, capability security, cache/Chronicle poisoning, registry and reflex supply chain, threat matrix, premature reflexization, latency inversion, rule explosion, false structure, and feedback loops integrated or retained as negative controls. |
| §18 ReflexBench | `benchmark-ratchets-and-anti-goodhart-evidence`; `resource-economics-and-token-budgets`; active experiment roadmap | Eight tracks, comparator matrix, launch-gate boundary, user-command track, complete denominators, and plural usefulness/safety/effect/cost metrics integrated as an argument-exit program. Source contains no run. |
| §19 implementation blueprint | `prototype-roadmap`; `integrated-reference-architecture`; this note | Service/store decomposition, stage budgets, structured concurrency, observability, compatibility, seven phases, minimal experiment, deterministic shell, typed pipelines, and modes retained as implementation obligations rather than copied as accomplished work. |
| §20 worked examples | receiving chapter examples and this note | Historical, ambiguous arithmetic, proof, current-information, effectful, deployment, forced-route, parameterized, analytical-profile, and compiled-workflow cases retained as boundary illustrations only. |
| §21 prior work | Appendix H records and external-source backlog | Comparators and narrow synthesis claim retained pending independent primary-source passage review; the Corben paper does not independently establish novelty. |
| §22 advanced-intelligence implications | `asi-is-a-stack-not-a-model`; `replaceable-cognitive-substrates-beyond-transformer-monoculture`; `recursive-self-improvement-boundaries`; `procedural-memory-and-cognitive-loop-closure` | LLM-as-exception-handler, hierarchy of computation, procedural accumulation, temporal continuity, controlled execution-graph improvement, and personal instruction set integrated as design implications, not ASI evidence. |
| §§23–24 | this note; `open-research-agenda-and-bibliography-plan`; chapter summaries | Twenty-three research questions remain open; conclusion is represented by the cross-layer synthesis without promoting capability or safety. |
| Appendices A–G | this note; schema/fixture/benchmark backlogs; `schemas/reflexive_dispatch_trace_record.schema.json` | Reflex contract, typed packet, terminal outcomes, registration checklists, benchmark record, and command descriptor retained as normative sketches. The repository's finite trace schema is a design consumer, not a deployed implementation. |
| Glossary and references | chapter terminology; Appendix H | Durable terms integrated where owned. The 36 references require independent current-primary-source review before external support or novelty use. |

## Closure Status

**Section-family audit complete as of 2026-07-31.** All 24 numbered sections,
seven appendices, glossary, and references terminate in manuscript integration,
public-safe source-note retention, a concrete protocol/evaluation/research
obligation, or an explicit non-claim. This pass repaired two compressed
families in the manuscript: the scoped and mutable User Command Registry as a
governed personal instruction set, and hierarchical selective-risk routing
with OOD-triggered abstention, deadline-aware cascades, and outcome learning
that cannot learn authority. No substantive section is orphaned.

Closure does not establish a trained router, calibrated selective-risk result,
useful-throughput advantage, deployed command plane, Temporal Chronicle,
effect kernel, safe reflex compiler, security result, independent novelty
finding, production transfer, or ASI claim. The source remains `argument` and
must be reopened if the paper or any receiving chapter materially changes.
