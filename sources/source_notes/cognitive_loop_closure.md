# Source Note: Cognitive Loop Closure

| Field | Value |
|---|---|
| Source ID | `cognitive_loop_closure` |
| Source title | Cognitive Loop Closure: Compiling Repeated AI Reasoning Trajectories into Verified Parameterized Tools |
| Author / release | Corben Sorenson; public release v1.0, May 2026 |
| Ingestion basis | Complete local raw cache at `sources/raw/google_docs/cognitive_loop_closure.txt`; section-family fidelity audit completed 2026-07-31 |
| Source status | Conceptual framework and agent-architecture proposal |
| Evidence boundary | Architecture prose, formal sketches, comparison tables, parameter-probing methods, assurance and runtime taxonomies, example tool cards, lifecycle criteria, metric families, governance requirements, research questions, and an eight-phase implementation proposal. No trajectory-mining corpus, loop detector, abstraction engine, synthesized tool, verifier, registry, routing experiment, runtime monitor, embodied logger, safety controller, lifecycle automation, or independent reproduction is present. |

## Thesis

Cognitive Loop Closure proposes that repeated AI reasoning and action should
become explicit procedural memory rather than being improvised indefinitely.
The system mines a complete execution history, detects comparable recurring
trajectories, separates invariant structure from variable parameters and
preconditions, actively probes hidden assumptions, synthesizes a deterministic
or bounded semi-deterministic procedure, verifies it on replay, held-out,
synthetic, adversarial, schema, sandbox, and runtime evidence, registers a
versioned tool card, routes future matching work through it, monitors live
residuals, and revises or retires the tool as its environment changes.

The compact slogan is **reason when novel, execute when closed, reflex when
safety-critical**. These are three different control and authority modes.
Interpreter reasoning preserves flexibility for ambiguity and novelty.
Compiled-tool execution applies a qualified procedure inside a known envelope.
Reflex/failsafe execution uses a hard-latency controller or containment action
when neither deliberation nor an ordinary workflow can respond safely.

The deepest contribution is not automatic tool creation. It is the claim that
procedural memory must preserve its derivation and its right to be reused. A
procedure remains useful only while the trace family, parameters,
preconditions, verifier, runtime, risk, latency, permissions, dependencies,
monitoring, and retirement evidence remain current.

## Claim Boundary and Related Work

The paper presents Cognitive Loop Closure as a synthesis of reinforcement-
learning options, process mining, robotic process automation, programming by
demonstration, LLM tool use and tool creation, embodied skill libraries, human
procedural learning, runtime verification, and safety-critical control. Those
families motivate components; they do not independently establish the combined
lifecycle or its novelty. The selected references inside the source are
bibliographic leads until independently reviewed from primary sources.

Loop Closure is also part of Corben's author-side architecture lineage. RMI
places it inside a broader pressure-to-structure ratchet. RGS and Compact
Generative Systems frame a tool as a compact seed/rule/state/residual/verifier
object. Octopus Router makes the resulting tool or capability routable. VIEA
and Stable Capability Fields supply stronger maturity, qualification,
replacement, and authority boundaries. These overlaps are complementary
design ownership, not corroborating experiments.

The source does not claim that all repeated action should be automated, that
deterministic tools should replace reasoning, that closed tools are safe by
construction, that open-world verification is absolute, that prompt templates
are sufficient, that fine-tuning is obsolete, that synthesis is easy, that
current agents implement the lifecycle, that human approval is unnecessary,
that a physical system can always fall back to an LLM, or that high-bandwidth
telemetry can be compressed without safety-relevant loss.

## Formal Object Model

A trajectory is sketched as task, context, action sequence, observation
sequence, final output, and verification outcome. A closure maps a family of
trajectories to a tool definition and parameter vector. Verification compares
the tool's output against required outcomes above a proposed threshold. A
piecewise router chooses tool, reasoning, or reflex based on match,
preconditions, risk, verification, novelty, and latency.

These formulas omit several objects required for an evidentially valid
implementation: stable run and artifact identity, the eligible trace universe,
failures and missing outcomes, effect receipts, principal and authority,
environment and dependency versions, selection lineage, evaluator identity,
cost, delayed consequences, and residual ownership. They also use scalar
verification and route predicates where a real system needs distinct
correctness, safety, applicability, authority, rights, freshness, latency, and
consumer gates. The book should preserve the sketches as intuition and use the
richer Procedure Qualification Packet as the executable target.

## Conceptual Primitives

- **Trajectory.** Versioned record of task, context, actions, tool calls,
  observations, artifacts, decisions, output, effects, intervention, cost, and
  verification. Summarized internal reasoning is optional and never substitutes
  for observable behavior.
- **Eligible trace universe.** All runs that could have entered loop discovery,
  including failures, abstentions, repairs, human interventions, timeouts, and
  censored outcomes.
- **Loop candidate.** Recurrent structural pattern whose task, pre-state,
  environment, authority, effects, and outcome comparability remain hypotheses.
- **Invariant.** Step or relation predicted to remain stable across the
  declared task family, supported by variation and counterexamples rather than
  mere constancy in observed logs.
- **Parameter.** Typed, bounded, validated input expected to vary across uses.
- **Precondition.** Machine-checkable requirement that must hold before use.
- **Unknown assumption.** Suspected dependency that remains visible and blocks
  broad automatic routing until resolved or converted into a precondition.
- **Closed tool.** Parameterized, bounded, verifiable, routable, monitorable,
  versioned procedure; it may be code, workflow, query, controller, checker,
  API wrapper, browser automation, or restricted model-assisted process.
- **Tool card.** Procedural-memory record containing scope, schemas,
  parameters, pre/postconditions, verification, runtime, latency, risk,
  authority, side effects, provenance, failures, metrics, fallback,
  monitoring, version, and retirement.
- **Verification grade.** Bounded evidence class such as unverified,
  replay-passed, held-out-passed, synthetic-passed, adversarial-tested,
  runtime-monitored, human-approved, or domain-certified. These are not one
  monotone universal scale.
- **Assurance level.** Proposed automation/environment class from prompt or
  checklist through assisted, typed, sandboxed, high-assurance, and reflex
  tools. It does not itself establish certification.
- **Latency class.** Declared timing envelope from nonurgent through
  interactive, operational, real-time, and safety-reflex deadlines.
- **Residual.** Failure, near miss, violated assumption, monitor event, user
  correction, drift, or unexplained outcome that narrows or challenges reuse.

## Mechanisms

### Ten-component closure architecture

The paper defines a trajectory logger, loop detector, abstraction engine,
active parameter discovery component, tool synthesizer, verifier, registry,
router, runtime monitor, and revision/retirement manager. The boundaries are
important. Logging does not decide comparability. Similarity does not prove an
invariant. Synthesis does not verify. Verification does not grant authority.
Registration does not make a tool routable. Routing does not execute effects.
Monitoring does not authorize its own repair, and successful use does not make
retirement unreachable.

The logger should record inputs, outputs, actions, calls, artifacts, failures,
verification, timing, resources, feedback, and environment. The detector
clusters action graphs and task families while preserving near matches and
differences. The abstraction engine proposes stable order, transformations,
validation, approvals, and failure handling. The parameter component attacks
that proposal. The synthesizer selects a representation; the verifier tests
it; the registry exposes it to governed routing; monitors update evidence;
lifecycle management tightens, splits, merges, downgrades, quarantines, or
retires it.

### Active parameter discovery

Passive observation cannot distinguish an invariant from a value that happened
not to vary. The paper proposes six complementary probes:

1. historical variance identifies already-observed variation;
2. counterfactual replay substitutes formats, paths, schemas, arguments,
   dependencies, environment variables, and edge cases in a sandbox;
3. synthetic case generation constructs plausible missing-field, schema,
   package-manager, pagination, or structural variants;
4. adversarial probing seeks malformed, ambiguous, partial, conflicting,
   stale, and mismatched cases;
5. environment interrogation checks configuration, versions, units,
   permissions, dependencies, and platform immediately before execution; and
6. a named human or supervisory question resolves ambiguities that cannot be
   safely inferred.

Each variable becomes invariant, parameter, precondition, or unknown
assumption. A parameter is admissible only if it explains variation, fits the
input schema, affects execution or verification, is bounded or validated, and
survives controlled changes without invalidating the procedure unexpectedly.
Otherwise it becomes a precondition, abstention trigger, or unresolved
residual. Probe safety, data rights, and effect authority must be checked
before active exploration; “discover the boundary” cannot authorize harmful
experiments.

### Tool synthesis and bounded model calls

A closed tool can be a function, workflow graph, query, wrapper, repository
command, transformation, validator, browser automation, control primitive,
monitor, or failsafe. Its essential properties are parameterization,
boundedness, verifiability, routability, and monitorability. Deterministic tools
offer the clearest replay boundary, but the paper permits semi-deterministic
tools whose internal model calls are constrained by input/output schemas,
verifiers, confidence or abstention rules, fallback, and audit.

The closure is not “the model knows how to think.” It is that a model is one
fallible component inside a declared procedure. The tool record must bind the
model, prompt/policy, sampling, source context, evaluator, retry policy, and
nondeterminism. A semi-deterministic tool should not borrow the evidence state
of a deterministic parser or checker simply because both are callable.

### Verification as a portfolio, not a badge

Verification sources include prior replays, held-out trajectories, synthetic
variation, adversarial cases, schema and invariant checks, sandboxes, human
review, and runtime monitoring. The source's grades capture accumulated
coverage, but different evidence types answer different questions. Replay can
show backward compatibility without generalization. Held-out success can miss
novel parameters. Synthetic and adversarial suites depend on generator quality.
Runtime monitoring observes only encoded properties. Human approval is scoped
judgment, and “certified” requires a named domain and authority.

Promotion therefore binds a verification vector to task, environment,
consumer, risk, runtime, version, and expiry. False-positive and false-negative
rates, coverage gaps, correlated generator/verifier dependencies, and known
counterexamples remain attached. Open-world verification can make a procedure
more falsifiable and controlled than repeated improvisation; it cannot make it
perfectly safe.

### Execution, routing, latency, and authority

Execution tiers range from text templates and human-reviewed workflows through
typed deterministic functions, sandboxes, memory-safe runtimes, and real-time
controllers. Every tool declares schemas, parameters, pre/postconditions,
permission requirements, allowed side effects, time/memory/rate limits, and a
least-powerful-sufficient environment.

The router rechecks task match, parameter availability, preconditions,
verification scope, freshness, environment, authority, risk, latency, recent
failure, novelty, fallback, and monitoring at every invocation. L0/L1 work may
wait for hours or seconds; L2 work expects operational sub-second service; L3
has real-time millisecond constraints; L4 is a safety reflex where language-
model fallback is invalid. Latency class is not speed marketing: it binds
deadline, tail/jitter budget, trigger-to-effect path, overload policy, and safe
failure destination.

### Lifecycle and closure economics

The source's lifecycle is candidate, proposed, probed, tested, probationary,
active, monitored, revised, and retired. Candidate requires recurrence,
structural similarity, meaningful cost, plausible parameterization, acceptable
risk, and possible verification. Proposed adds the tool specification. Probed
attacks hidden parameters. Tested exercises multiple evidence sources.
Probation limits risk through dry-run, approval, monitoring, and fallback.
Active permits scoped automatic invocation. Monitored execution updates
evidence. Revision may add parameters, tighten preconditions, expand verifiers,
restrict runtime, split, merge, or version. Retirement responds to staleness,
failure, disuse, overlap, changed risk, or excessive maintenance.

The close/don't-close rule compares recurrence, expected savings, quality,
and automation appropriateness with creation, maintenance, risk, verification,
and drift/depreciation cost. The displayed formula is typographically malformed
and uncalibrated. It should be interpreted as a complete decision-factor list.
The denominator must also include trace collection, privacy, security, human
deskilling, exception handling, routing, monitoring, incident, rollback,
dependency, and retirement cost.

### Hierarchical embodied logging

The paper distinguishes raw telemetry, cognitive trajectory, discrete events,
compressed features/semantic state, active skill/controller, outcomes, and
residuals. A rolling raw buffer is selectively pinned around collision risk,
uncertainty, saturation, unexpected objects, reflex activation, tool failure,
human override, verification failure, prediction residual, and environment
mismatch. Reflex records preserve pre/post sensor windows, control output,
active controller, monitor state, trigger, latency, outcome, and intervention.

The loop detector normally consumes event and cognitive traces, but every
derived record needs a shared clock and trace ID back to raw evidence. The
budget equation is a storage constraint, not an adequacy proof. Semantic
eventization and feature compression can erase causal precursors, minority
conditions, or safety evidence; their loss, false trigger, missed trigger,
reconstruction, privacy, and retention properties must be measured.

### Distinctions from adjacent shortcuts

A cache maps repeated inputs to outputs; a loop tool covers a parameterized
task family. A prompt template still delegates core behavior to improvisation;
a qualified tool binds schemas, tests, monitoring, and fallback. Fine-tuning
changes weights; loop closure externalizes a narrower skill that can be
versioned, inspected, and retired. Ordinary tool use assumes a tool exists;
loop closure governs when observed behavior may become one. These distinctions
are tendencies, not absolutes: model-assisted tools remain nondeterministic,
and a tool ecosystem can be harder to govern than a narrow weight update.

## Interfaces and State Machines

Trace state moves through observed, eligible/ineligible, comparable/disputed,
clustered, included/excluded, and retained historical. A procedure moves
through candidate, proposed, probed, tested, probationary, active, monitored,
revised, quarantined, deprecated, superseded, and retired. Verification moves
through unverified and multiple scoped evidence classes rather than one global
pass. A route moves through match, precondition/authority/freshness/risk/
latency checks, selected, executing, monitored, fallback/abstain/reflex,
residualized, and closed.

Artifact Graphs owns trace and effect lineage. Procedural Memory owns mining,
abstraction, qualification packets, and tool lifecycle. Cognitive Compilation
owns executable representation. VCM and Context Transactions own memory state.
Routing owns invocation leases. Runtime owns effects and containment. Evidence
owners own verification meaning. Readiness and SCF own qualification,
replacement, rollback, and routability. Human and institutional owners retain
approval, exception, appeal, and consequence authority.

## Evidence

The paper supplies a coherent end-to-end architecture; formal intuition;
ten-component responsibilities; six active parameter probes; four variable
states; tool, assurance, verification, runtime, latency, and risk taxonomies;
four detailed example cards; a nine-stage lifecycle; close/don't-close cost
factors; distinctions from adjacent mechanisms; seven evaluation families;
governance requirements; seven research areas; eight implementation phases;
and a sixteen-field specification template.

It supplies no run data, corpus, code, measured thresholds, tool candidates,
verification outputs, savings, reliability changes, safety evidence, or user
outcomes. Claims that closed tools can reduce cost, increase consistency, or
improve interpretability are hypotheses to compare under total lifecycle cost.

## Evaluation and Falsifiers

A faithful campaign uses natural repeated work with frozen missions,
authorities, environments, effects, and delayed outcomes. It compares repeated
interpreter execution, retrieval-only memory, caches, prompt/checklist reuse,
human-authored scripts and workflows, fine-tuning, learned tool use, program or
skill libraries, and the full governed closure system under matched models,
tools, context, human help, retries, and time. It reports:

- loop-candidate precision/recall, cluster coherence, time to detection,
  storage, and selection denominators;
- trace comparability, invariant correctness, counterexample coverage,
  parameter sufficiency, unknown assumptions, missing preconditions, and probe
  safety;
- generated-tool build/replay, determinism, schema/effect conformance,
  nondeterministic variance, and supply-chain integrity;
- verifier false accepts/rejects, held-out and transfer performance,
  adversarial discovery, monitor coverage, and evaluator dependence;
- correct/wrong/missed invocation, abstention, fallback, novelty, route drift,
  latency compliance, reflex triggers, and authority violations;
- useful success, unsafe reuse, false blocking, user correction, consistency,
  incident, rollback, delayed effects, and residual movement;
- tokens, latency, compute, storage, human work, verification, maintenance,
  privacy, security, deskilling, recovery, and opportunity cost; and
- active/stale/overlapping/retired tools, dependency complexity, lifecycle
  churn, maintenance burden, and value per tool.

Causal ablations remove active probing, failures/negative examples,
independent verification, typed schemas, scoped permissions, freshness checks,
monitoring, retirement, reflex routing, and raw-event trace joins. The system
should be narrowed or rejected if it cannot find stable task families; hidden
parameters remain common; generated tools fail to beat simple scripts or
checklists; verifier errors dominate; maintenance and governance erase savings;
automation weakens human exception handling; retirement fails; or a simpler
memory or fine-tuning route delivers equal useful outcomes at lower total cost.

## Failure Modes

- **Anecdote/premature closure:** one elegant trace becomes a general tool.
- **Similarity laundering:** superficially similar traces differ in state,
  authority, effects, or outcome.
- **Hidden-parameter closure:** observed constants are compiled as invariants.
- **Unsafe active probing:** parameter discovery creates real harmful effects.
- **Overgeneralization:** the tool fires outside its validated envelope.
- **Success survivorship:** failures, near misses, abstentions, repairs, and
  missing outcomes disappear from the training denominator.
- **Semi-determinism laundering:** an internal model call is narrated as a
  deterministic procedure.
- **Verification-grade inflation:** replay or synthetic success is presented as
  domain certification or open-world safety.
- **Router misuse:** a qualified tool is invoked with missing parameters,
  stale dependencies, excessive authority, wrong risk, or invalid latency.
- **Stale tool:** APIs, schemas, policies, users, models, or environments change
  while routing remains active.
- **Tool bloat:** overlap, dependency, monitoring, and retirement costs exceed
  saved cognition.
- **Unsafe automation:** convenience creates side effects without approval,
  dry-run, containment, or recovery.
- **Reflex gap:** slow reasoning is treated as a fallback inside a hard deadline.
- **Tool-card fiction:** declared behavior, tests, permissions, or metrics are
  not bound to the executed artifact.
- **Automation complacency:** human skill, attention, responsibility, and
  exception handling degrade as nominal throughput rises.
- **Telemetry amnesia:** event or feature compression discards rare precursors
  required for incident reconstruction.
- **Retirement failure:** once-useful procedures become immortal dependencies.
- **Support laundering:** reuse frequency or schema conformance is presented as
  general learning, capability, safety, or ASI.

## Book Chapters Supported

- `capability-replacement-and-rollback` (Capability Replacement and Rollback)
- `artifact-graphs-audit-logs-and-replay` (Artifact Graphs, Audit Logs, and Replay)
- `embodied-agency-real-time-control-and-physical-safety` (Embodied Agency, Real-Time Control, and Physical Safety)
- `procedural-memory-and-cognitive-loop-closure` (Procedural Memory and Cognitive Loop Closure)
- `routing-heads-and-specialist-cores` (Routing Heads and Specialist Cores)
- `readiness-gates-residual-escrow-and-quarantine` (Readiness Gates, Residual Escrow, and Quarantine)
- `benchmark-ratchets-and-anti-goodhart-evidence` (Benchmark Ratchets and Anti-Goodhart Evidence)
- `open-ended-improvement-engines` (Open-Ended Improvement Engines)
- `fast-generation-architectures` (Fast Generation Architectures)
- `policy-optimization-and-learning-from-feedback` (Policy Optimization and Learning from Feedback)
- `artifact-steward-agents-and-living-project-governance` (Artifact Steward Agents and Living Project Governance)
- `integrated-reference-architecture` (Integrated Reference Architecture)
- `living-book-methodology` (Living Book Methodology)
- `adjudicated-persistence-and-the-adaptive-commit-boundary` (Adjudicated Persistence and the Adaptive Commit Boundary)

## Claims To Add Or Update

- Define a procedure candidate over a complete eligible trace universe, not a
  success-only example set or hidden reasoning summary.
- Treat active parameter discovery as an adversarial evidence-acquisition
  phase with safe historical, counterfactual, synthetic, environmental, and
  supervisory probes.
- Preserve invariant, parameter, precondition, and unknown-assumption states;
  inability to encode a factor routes to abstention or a narrower tool.
- Separate tool determinism, verification evidence, runtime assurance, latency,
  risk, authority, freshness, and lifecycle rather than collapsing them into a
  “verified” badge.
- Bind semi-deterministic model calls, retries, sampling, context, evaluator,
  and output variance inside the tool record.
- Require per-invocation task, parameter, precondition, authority, risk,
  freshness, environment, latency, monitoring, and fallback checks.
- Use linked raw, event, semantic, skill, outcome, and residual logging with
  trigger-based retention and measured information loss for embodied closure.
- Evaluate closure against scripts, workflows, caches, templates, fine-tuning,
  learned-tool systems, and no-closure baselines at total lifecycle cost.

## Section-Family Closure Ledger

| Section family | Disposition |
|---|---|
| Executive abstract, definition, stair analogy, three modes | Thesis and non-claim boundary integrated in Procedural Memory and Routing. |
| Problem examples and procedural-memory gap | Retained as motivating task families; examples do not establish recurrence or savings. |
| Formal trajectory/tool/verification/route sketches | Preserved with missing identity, authority, denominator, effect, and scalar-gate limitations. |
| Six core-thesis claims | Integrated into the governed trace-to-tool lifecycle and applicability boundary. |
| Nine adjacent research families | Retained as lineage/comparator leads; novelty and property transfer require independent primary-source review. |
| Ten-component architecture | Canonical in Procedural Memory; owner separation and non-authority boundaries deepened. |
| Six active parameter-discovery methods and four states | Added directly to Procedural Memory with safe-probe, typed-bound, and abstention obligations. |
| Embodied logging problem, multi-resolution logs, triggers, eventization, features, reflex data, and budget | Added to Embodied Control; deep note preserves full source detail and loss/reconstruction boundary. |
| Tool forms and deterministic/semi-deterministic distinction | Added to Procedural Memory with model-call custody and nondeterminism accounting. |
| Assurance levels and verification grades | Added as orthogonal evidence/runtime axes; source labels are proposed vocabulary, not certification. |
| Verification sources and open-world limit | Canonical in Procedural Memory; evaluator correlation and coverage limits retained. |
| Execution tiers, schemas, sandbox/memory safety, capability restrictions | Canonical across Procedural Memory, Runtime, Security, and Embodied Control. |
| Routing modes and L0–L4 latency classes | Added to Procedural Memory's route contract; reflex deadlines cannot fall back to LLM reasoning. |
| Registry and full tool-card fields | Canonical Procedure Qualification Packet expanded with determinism, verification vector, latency, authority, dependencies, and effect receipts. |
| Four example tool cards | Retained here as design examples only; no tool or domain result inferred. |
| Nine lifecycle states | Reconciled with richer canonical candidate-to-retired lifecycle and readiness/replacement authority. |
| Loop-closure decision rule | Retained as a malformed/un-calibrated factor inventory; total lifecycle-cost omissions made explicit. |
| Cache/template/fine-tuning/ordinary-tool distinctions | Retained with counterexamples and no-obsolescence boundary. |
| CGS mapping | Routed to Compact Generative Systems as author-side conceptual lineage, not independent support. |
| Seven evaluation families | Converted into the mature matched campaign and causal ablations. |
| Risk tiers, human approval, audit logs, sandboxing | Canonical across Runtime, Human Factors, Security, and Procedural Memory; no assurance claim. |
| Seven failure modes | Preserved and expanded with survivorship, semi-determinism, grade inflation, tool-card fiction, automation complacency, telemetry amnesia, and support laundering. |
| Seven-part research agenda | Retained as open implementation/evaluation questions in the deep note and manuscript test program. |
| Eight implementation phases | Retained as ordered obligations from logging through ecosystem management; no phase is implied complete. |
| Claims/non-claims, conclusion, specification template | Fully represented in note and interfaces; public summary/manifesto repetition adds no new technical claim. |
| Selected references | Leads only until independently ingested and passage-reviewed. |

## Open Questions

- How should trace comparability be defined without post-hoc outcome leakage or
  storing private chain-of-thought?
- Can safe active probes discover hidden parameters without authorizing the
  effects whose boundaries they are meant to learn?
- Which procedure representation—code, workflow, controller, policy, query,
  checklist, or bounded model call—minimizes total verification and maintenance
  burden for each task family?
- How should verification grades combine evidence types without becoming a
  false universal ladder?
- When does externalized procedural memory outperform a narrow model update in
  usefulness, reversibility, privacy, and total lifecycle cost?
- Can a router estimate novelty and applicability under selection bias created
  by prior routing and tool availability?
- Which raw-trigger and semantic-log policy preserves rare causal precursors
  under storage, privacy, bandwidth, and real-time constraints?
- How should tool composition, shared dependencies, and retirement propagate
  invalidation without making the registry impossible to maintain?
