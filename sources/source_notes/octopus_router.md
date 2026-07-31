# Source Note: Octopus Router Architecture

| Field | Value |
|---|---|
| Source ID | `octopus_router` |
| Source title | Octopus Router Architecture: Dynamically Loaded Modular Intelligence with Independently Ratcheted Specialists |
| Author / release | Corben Sorenson; public release v1.0, May 2026 |
| Ingestion basis | Complete local raw cache at `sources/raw/google_docs/octopus_router.txt`; section-family fidelity audit completed 2026-07-31 |
| Source status | Conceptual framework and AI-systems architecture proposal |
| Evidence boundary | Architecture prose, a compact formal model, registries, routing patterns, lifecycle heuristics, metric families, failure modes, and an eight-phase implementation proposal. No implemented ORA router, arm registry, dynamic loader, quarantine mechanism, specialist benchmark, split/merge decision, production trace, or comparative result is present. |

## Thesis

Octopus Router Architecture, or ORA, proposes that a coherent AI system need
not be one undifferentiated model. A relatively small resident head can
interpret a task, risk, budget, and context; select one or more bounded
specialist subsystems; grant each only the memory, tools, runtime, side effects,
and budget needed for the task; load cold specialists when necessary; compose
their structured outputs; and update routing and lifecycle records afterward.
The user sees one agent, while the implementation is a governed collection of
locally capable modules.

The important unit is not a prompt persona. An **arm** may be a model, tool
bundle, workflow, verifier, memory service, symbolic reasoner, retrieval lane,
sandbox, safety monitor, physical controller, or hybrid, but it becomes an arm
only when it has an explicit capability scope, schemas, tools, memory,
benchmarks, regressions, residuals, permissions, runtime tier, reliability
record, dependencies, cost profile, and lifecycle state. ORA therefore raises
Mixture-of-Experts sparsity from a neural-layer routing pattern to a
system-level capability and governance boundary.

The source's most durable claim is organizational, not empirical: capability
can be decomposed so that selection, execution, verification, residency,
memory, permission, improvement, and retirement remain inspectable. Its most
important corrective is that the head must not become a second monolith. Its
job is allocation and global composition, not hidden domain mastery.

## Claim Boundary and Intellectual Lineage

The octopus nervous system and “goblins in a trenchcoat” are explanatory
metaphors. Biology does not demonstrate that the proposed software topology is
efficient, safe, coherent, or trainable. The source compares ORA to sparse
Mixture-of-Experts, Mixture-of-Agents, Toolformer, Voyager, modular software,
least privilege, WebAssembly isolation, and Rust memory safety. Those are
adjacent design traditions, not evidence that their properties transfer when
combined.

ORA is broader than a proposer/aggregator multi-agent pattern because an arm
owns persistent state, tools, evaluation, permission, runtime, and lifecycle.
It is broader than a tool call because the callable capability carries local
memory, regressions, residuals, and a governed improvement process. It is
coarser than token-level MoE because it routes tasks or subtasks among
standalone systems. These distinctions are useful, but the source does not
establish that a lightweight learned head can perform all of the proposed
decomposition, risk assessment, loading, arbitration, and lifecycle work
without itself becoming expensive or brittle.

The paper explicitly does **not** claim that monoliths are obsolete, routing is
easy, more arms always help, modularity is automatically safe, loading always
reduces latency, quarantine removes all risk, or one topology fits every
deployment. It is a system architecture proposal, not proof that modular
routing beats dense generalism.

## Formal Object Model

The paper represents the system as
`O = (H, A, R, M, P, V, G)`: head, arm set, routing policy, memory system,
permission/runtime policy, verification layer, and growth process. For task
`x`, context `c`, budget `B`, and risk `r`, the head selects a subset of arms.
Each selected arm receives a scoped subtask, context, and permission/resource
envelope. The head composes the returned outputs, and verification chooses
among accept, revise, route-more, fallback, or refuse. A completed run updates
routing memory, reliability, residuals, benchmarks, tools, and lifecycle
signals.

That sketch is underspecified as mathematics but valuable as an ownership
map. The route function cannot be treated as a pure classifier: it consumes
changing registry, readiness, cost, load, privacy, permission, and risk state.
The composition function cannot be treated as concatenation: it needs
claim-level provenance, conflict handling, assumptions, residuals, and a
verification decision. The growth operator cannot autonomously create
authority: adding, splitting, merging, or retiring an arm must be a governed
replacement transaction over versioned capability identity.

## Conceptual Primitives

- **Resident head/router.** User-facing coordinator for intent recognition,
  decomposition, candidate selection, budget and risk allocation, memory and
  permission routing, composition, verification orchestration, escalation, and
  lifecycle proposals. It should not silently perform the specialist work it
  claims to route.
- **Arm.** Bounded specialist subsystem with an input/output contract, local
  capability and state, evaluation frontier, authority ceiling, runtime, cost,
  residuals, and lifecycle.
- **Arm card / registry entry.** Versioned discovery record describing scope,
  schemas, tools, memory access, permission and runtime tiers, cost, benchmark
  frontier, regression suite, residuals, reliability, freshness, dependencies,
  lifecycle state, and retirement criteria.
- **Permission envelope.** Task-local grant over memory, tools, runtime, side
  effects, budget, and risk. It is a strict subset of the arm's maximum
  capability and authority, not a standing appointment.
- **Routing memory.** History of which candidates were available, selected,
  rejected, successful, costly, unavailable, unsafe, or underqualified for
  which task conditions.
- **Arm-local memory.** Domain cases, tools, failures, and preferences visible
  only within an applicable lease; it prevents every specialist from receiving
  the global context by default.
- **Shared task memory.** Temporary collaboration state for a particular
  multi-arm route. It should expire with the route and preserve source and
  writer provenance.
- **Residual escrow.** Unsolved or ambiguous cases and failure clusters that
  remain owned instead of being erased by composition.
- **Residency policy.** Decision over cold, loading, warm, active, unloading,
  unavailable, or quarantined arm state. This is distinct from semantic route
  selection.
- **Growth/lifecycle process.** Governed add, probation, promote, split, merge,
  replace, quarantine, stale, retire, and restore transitions driven by demand,
  cost, regressions, residual topology, permission differences, and evidence.

## Mechanisms

### Arm contract and registry

The arm card is the architectural hinge. A vague label such as “coding arm” is
insufficient because it cannot tell the router whether the arm can handle a
Rust ownership failure, inspect a repository, run tests, or mutate production.
A precise card states supported and excluded task families, accepted inputs,
returned fields, accessible tools and memories, side effects, runtime,
dependencies, cost and latency profile, local benchmark frontier, regression
floor, unresolved residuals, reliability and freshness, lifecycle state, and
retirement conditions.

The source's arm anatomy and arm-card tables overlap but are not identical.
Together they imply three distinct contracts: a **capability contract** for
what transformations the arm can attempt, an **authority contract** for what
resources and effects it may receive, and an **evidence contract** for what
qualifies its output and future readiness. The book should preserve all three
rather than flattening the card into an expert description and score.

### Route selection and composition modes

ORA names six positive route shapes: single-arm, parallel, sequential, debate,
producer/verifier, and reflex. The later verification result adds revise,
route-more, fallback, and refuse. These should be treated as typed plans with
different dependency, latency, cost, correlation, and authority semantics:

- a single route needs one qualified capability and a fallback;
- a sequential route must type and preserve each intermediate handoff;
- a parallel route needs matched inputs and an aggregation rule;
- debate requires genuine error diversity rather than correlated role-play;
- verification keeps producer and checker artifacts and authority distinct;
- reflex routing needs hard latency, trigger, override, and post-event review
  contracts rather than merely a faster prompt.

Composition is an evidence-bearing operation. Each arm returns a result,
confidence, evidence, assumptions, residuals, risk flags, suggested successors,
and resource use. The head must compare claims, preserve provenance, surface
material disagreement, request missing information, invoke verifiers, and
choose an explicit terminal route. If it invents a consensus or misstates an
arm's output, the composition layer—not the arm—has failed.

### Dynamic loading as a separate control problem

Keeping a head resident and arms cold is system-level sparse activation. It can
reduce active memory, isolate sensitive or rare capabilities, permit
hardware-specific placement, and make independent upgrades possible. It can
also increase tail latency, thrash storage or accelerators, load stale state,
break dependencies, or turn prefetch into an information-leak channel.

Therefore semantic selection and physical residency must remain separate. A
route can be correct while the chosen arm is unavailable, too slow to load,
placed on an untrusted node, incompatible with a dependency, or more expensive
than a warm generalist. The residency receipt should preserve artifact and
dependency versions, prior and terminal state, placement, cold-start time,
transfer volume, peak memory, warm-cache hit or miss, prefetch reason,
load/unload overhead, failure or fallback, and total route cost. Benefits are
credible only when end-to-end task quality, safety, and isolation remain at
least within their declared floors.

### Memory and domain quarantine

ORA divides memory into global, arm-local, shared-task, routing, safety, and
residual layers. Routing memory and safety memory are not ordinary prompt
context; they are decision records with stricter integrity requirements.
Shared task memory needs a writer and reader policy so a compromised or
hallucinating arm cannot silently contaminate every downstream arm.

Quarantine is multidimensional: memory, tools, runtime, domain, failure, and
safety. Over-quarantine can make a specialist useless; under-quarantine can
leak data or authority. Temporary grants, head-mediated retrieval, explicit
escalation, audit logs, sandboxing, and verifier review are proposed
mitigations. The book should treat quarantine as an empirical precision/recall
and utility problem, not a label that proves containment.

### Independent ratchets and ecosystem evolution

Each arm has a local loop: benchmark frontier, attempts, residual logging,
tool and memory improvement, regression preservation, and frontier movement.
This permits one capability to improve without retraining all others, but only
if shared dependencies and router behavior are included in regression scope.
An “independent” arm update that changes common embeddings, memory formats,
tool schemas, or composition policy is not independent in effect.

The source proposes spawning an arm when recurring demand times specialization
value and expected gain exceeds creation and maintenance cost. Split signals
include tool count, latency, unrelated scope, memory growth, reliability loss,
conflicting subskills, distinct residual clusters, router confusion, branching,
and risk-domain divergence. Merge signals include overlapping tools, memory,
benchmarks, outputs, failures, and low usage. Retirement is appropriate for
stale, unsafe, superseded, expensive, unused, regression-failing, or
goal-incompatible arms.

Those are diagnostic variables, not automatic thresholds. Every topology
change alters candidate denominators, routing policy, memory custody,
dependencies, regressions, and rollback. Split/merge/retire therefore belongs
under readiness and capability-replacement governance, with a counterfactual
comparison against leaving the topology unchanged.

### Runtime and risk tiers

The source proposes execution tiers from text-only procedure through structured
workflow, deterministic function, sandbox, memory-safe systems runtime, and
real-time reflex controller. Its risk table moves from automated low-risk work
through verified/rollback-capable medium-risk work to approval-bound high-risk
and certified/failsafe critical work. The useful idea is that the arm card must
bind capability to a runtime and risk envelope. The specific tier labels do not
constitute certification, and a Safety Arm cannot self-grant veto authority or
replace the institutional owner of a consequential decision.

## Interfaces and State Machines

An arm moves through proposed, registered, probationary, qualified, active,
warm/cold/unavailable runtime substates, stale, quarantined, split candidate,
merge candidate, superseded, retired, and rollback/restoration states. A route
moves through requested, candidate-enumerated, gated, selected, lease-issued,
loading, executing, composing, verifying, accepted, revised, expanded,
fallback, refused, cancelled, residualized, and closed states.

The Routing chapter owns candidate enumeration, route policy, leases,
composition, and decision receipts. Readiness owns qualification, expiry,
quarantine, and ordinary/canary eligibility. Stable Capability Fields and
Capability Replacement own identity-preserving split, merge, upgrade,
retirement, and rollback. Virtual Context ABI owns memory materialization and
revocation. Runtime owns placement and effects. Evidence and Artifact Graphs
own output support and provenance. Resource Economics owns total cost and
residency accounting. The head may propose changes across these boundaries; it
does not absorb their authority.

## Evidence

The source provides a coherent architecture, a compact formal vocabulary,
concrete card fields, route patterns, permission and memory partitions,
lifecycle signals, runtime/risk tiers, metric families, failure modes, and a
manual-to-multi-arm implementation sequence. This is strong design material
for the book.

It supplies no measurements, datasets, thresholds, implementation artifacts,
route logs, arm outputs, security tests, loading traces, or independent
comparisons. Statements that system-level sparsity can reduce active memory,
that bounded modules improve quarantine and fault containment, or that local
ratcheting avoids interference are hypotheses conditioned on placement,
dependency, workload, and governance design.

## Evaluation and Falsifiers

A faithful ORA evaluation must compare at least a strong single generalist,
static tool routing, token-level or conventional MoE where applicable, a
simple rule router, cost-aware cascades, and learned ORA policies on frozen
natural and adversarial tasks. Candidate systems receive matched tools,
context, authority, retries, wall time, and verification. Report complete
denominators for:

- end-to-end useful task success, not route label accuracy alone;
- correct, unnecessary, missed, overprivileged, and no-fit routing;
- selective coverage, clarification, fallback, refusal, and escalation;
- composition faithfulness, hidden disagreement, correlation, and collusion;
- cold-start and tail latency, warm-cache hits, prefetch precision, transfer
  volume, peak/active memory, unload cost, thrashing, and unavailable-arm
  failures;
- local benchmark and regression movement, residual growth, freshness,
  dependency breakage, interference, and bloat;
- unauthorized access attempts, over-grants, cross-domain leakage, safety
  veto precision/recall, and useful work blocked by quarantine;
- compute, financial, storage, engineering, evaluator, human-review,
  governance, migration, and recovery cost; and
- split/merge/retire counterfactuals, rollback success, delayed failures, and
  transfer to new domains, hardware, organizations, and model families.

ORA should be narrowed or rejected where a warm generalist wins on total
quality-adjusted cost; a lightweight head cannot retain route calibration;
arms share enough state that quarantine is nominal; dynamic loading loses to
ordinary caching or paging; composition adds correlated error; lifecycle
management costs exceed specialization benefits; or split/merge decisions do
not improve held-out utility after accounting for transition cost and
regression risk.

## Failure Modes

- **Bad routing:** wrong, missing, excessive, or unsafe specialist selection.
- **Head recentering:** decomposition and domain reasoning accumulate in the
  supposedly lightweight head until it is the new monolith.
- **Arm bloat:** a specialist hides unrelated tools, memory, risks, and internal
  branches behind one label.
- **Arm-card fiction:** registry declarations drift from actual model, tools,
  authority, state, cost, or reliability.
- **Goblin chaos:** multi-arm outputs are incoherent, correlated, duplicative,
  or expensive, and composition hides the disagreement.
- **Composition hallucination:** the head invents support, consensus, or
  conclusions absent from arm outputs.
- **Residency thrash:** load/unload and transfer costs erase sparse-activation
  benefits or violate deadlines.
- **Stale restoration:** a cold or retired arm reloads stale weights, tools,
  memory, policy, or dependencies.
- **Prefetch leakage:** speculative loading reveals sensitive task intent or
  exposes capabilities before authorization.
- **Over-quarantine:** needed context or tools are withheld, reducing useful
  performance and driving unsafe workarounds.
- **Under-quarantine:** arms receive unnecessary memory, tools, runtime, or side
  effects and cross-contaminate domains.
- **Safety-arm sovereignty:** a specialist presented as a safety monitor gains
  unreviewed global veto or policy-writing power.
- **False independence:** a local update changes shared state or downstream
  behavior outside the arm's declared regression boundary.
- **Lifecycle churn:** noisy residuals or usage shifts cause repeated spawning,
  splitting, merging, and retirement without net benefit.
- **Metric gaming:** route accuracy, cache hits, benchmark scores, or low active
  memory improve while useful outcomes, safety, or total cost worsen.
- **Identity and authority laundering:** the coherent external persona causes
  users or downstream systems to attribute every arm's claim and permission to
  one trusted identity.

## Book Chapters Supported

- `routing-heads-and-specialist-cores` (Routing Heads and Specialist Cores)
- `readiness-gates-residual-escrow-and-quarantine` (Readiness Gates, Residual Escrow, and Quarantine)
- `personal-compute-hives-and-federated-edge-intelligence` (Personal Compute Hives and Federated Edge Intelligence)
- `policy-optimization-and-learning-from-feedback` (Policy Optimization and Learning from Feedback)
- `integrated-reference-architecture` (Integrated Reference Architecture)

## Claims To Add Or Update

- Define an arm as a capability, authority, evidence, memory, runtime, cost, and
  lifecycle contract—not a role prompt or model endpoint.
- Keep semantic selection, task-local authorization, physical residency,
  execution, composition, verification, and lifecycle change as distinct
  decisions and receipts.
- Require structured arm outputs that preserve claim, evidence, assumptions,
  residuals, risk, successor suggestions, provenance, and total resource use.
- Treat single, sequential, parallel, debate, verification, and reflex routes
  as typed plans with different cost, correlation, dependency, and failure
  semantics.
- Measure dynamic loading against warm-generalist and ordinary cache/paging
  baselines, including tail latency, transfer, thrash, unavailability, and
  security costs.
- Govern spawn, split, merge, replace, and retire decisions through prospective
  evidence, complete dependency/state inventories, regression, rollback, and
  counterfactual topology comparisons.
- Evaluate quarantine for both leakage prevented and useful work blocked.
- Prevent the head, safety arm, or external single-agent identity from
  laundering specialist authority or evidence.

## Section-Family Closure Ledger

| Section family | Disposition |
|---|---|
| Abstract, monolith problem, octopus and trenchcoat metaphors | Thesis and lineage retained here; metaphors are explanatory, not biological evidence. |
| Six-part core thesis | Integrated into Routing's head/specialist boundary, leases, dynamic residency, local ratchets, and quarantine. |
| MoE, MoA, Toolformer, Voyager, modular software, WebAssembly, and Rust relations | Retained as adjacent architecture families and non-transfer boundaries; no independent corroboration inferred. |
| Five-layer overview and formal tuple | Reconstructed as an ownership model; mathematical underspecification and authority limits made explicit. |
| Head role and anti-monolith constraint | Canonical in Routing; strengthened with head-recentering failure and scope tests. |
| Arm definition, anatomy, examples, and arm card | Added to Routing as a three-contract capability/authority/evidence object; examples retained here to avoid bloating canonical prose. |
| Dynamic loading benefits and metrics | Added to Routing as a separate residency control problem with cold/warm state, end-to-end cost, security, and warm-generalist baselines. |
| Six routing patterns | Canonical in Routing; deep note preserves distinct dependency, correlation, latency, and authority semantics. |
| Structured outputs, composition, and conflict resolution | Added to Routing as an Arm Result Envelope and Composition Receipt; no concatenation-as-composition shortcut. |
| Domain quarantine and permission envelope | Canonical across Routing and Readiness; audit adds over-quarantine utility and under-quarantine leakage measurement. |
| Six memory layers and routed-memory principle | Retained here and linked to VCM ownership; shared-task writer provenance and expiry added as obligations. |
| Independent arm ratchet | Routed to Policy Optimization and Readiness; false independence through shared dependencies remains a falsifier. |
| Spawn, split, merge, and retire lifecycle | Added to Routing as evidence-bound topology change; formulas and signal lists retained as proposed diagnostics, not automatic rules. |
| Router, arm, system, loading, and quarantine metrics | Consolidated into the evaluation program with complete quality, cost, governance, and failure denominators. |
| Runtime tiers, risk tiers, and Safety Arm | Retained as design vocabulary under Runtime and governance owners; not certification or autonomous veto authority. |
| Eight failure modes | Preserved and extended with registry drift, residency thrash, false independence, lifecycle churn, and identity laundering. |
| Eight implementation phases | Converted into ordered implementation obligations; no phase or goal is represented as completed by the paper. |
| Claims and non-claims | Preserved in the source boundary and manuscript non-claim language. |
| Arm-card template and router checklist appendices | Fully represented by the note and Routing interfaces; no duplicate book appendix required. |
| Public summary and compact manifesto | Editorial restatements only; no additional technical claim or chapter warranted. |

## Open Questions

- Can a small head remain calibrated as registry size, domains, risk tiers, and
  composition modes grow, or does coordination complexity recreate a monolith?
- What evidence distinguishes a useful arm boundary from an arbitrary service
  boundary, prompt persona, or duplicated generalist?
- How should local reliability be updated under selection bias when difficult
  tasks, fallbacks, and verifiers are routed non-randomly?
- Can shared-task memory remain useful without becoming a cross-arm taint and
  prompt-injection bus?
- Which split/merge signals predict held-out benefit after migration,
  retraining, cache, governance, and rollback costs?
- When does dynamic loading beat quantization, ordinary memory mapping,
  accelerator caching, SSD paging, or a warm generalist on total cost and tail
  latency?
- How can independent evaluators detect composition hallucination when the head
  controls which arm artifacts are surfaced?
- What external identity and disclosure rules keep a coherent user experience
  from hiding material differences in provenance, authority, and uncertainty?
