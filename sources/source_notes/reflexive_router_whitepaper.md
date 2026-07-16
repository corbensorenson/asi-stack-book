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
