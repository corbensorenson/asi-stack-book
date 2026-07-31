# Source Note: Ratcheting Modular Intelligence

| Field | Value |
|---|---|
| Source ID | `rmi` |
| Source title | Ratcheting Modular Intelligence: A Unified Framework for Active Compression, Loop Closure, Benchmark Frontiers, and Routed Specialist Systems |
| Author / release | Corben Sorenson; public release v1.0, May 2026 |
| Ingestion basis | Complete local raw cache at `sources/raw/google_docs/rmi.txt`; section-family fidelity audit completed 2026-07-31 |
| Source status | Conceptual framework, AI-systems architecture proposal, and development methodology |
| Evidence boundary | Architecture prose, compact formal sketches, benchmark and tool policies, registry templates, heuristic thresholds, evaluation dimensions, failure modes, and an eight-phase implementation proposal. No RMI system, benchmark campaign, loop detector, synthesized tool, intervention comparison, routed arm, embodied logger, safety monitor, lifecycle transition, or independent reproduction is present. |

## Thesis

Ratcheting Modular Intelligence, or RMI, is a development methodology for
turning pressure into durable structure. A benchmark exposes a capability
deficit; routed specialists attempt the work; successes and failures are
logged; recurring successful trajectories may become verified tools; failures
become residual maps; an intervention ladder diagnoses whether the wall lies
in the benchmark, data, training, inference, procedure, curriculum, or
architecture; mastered behavior becomes a regression floor; and a harder
frontier supplies the next pressure.

Its central law is: **move the frontier while holding the floor**. Capability
growth is not a rising score alone. It is a state transition that preserves
prior obligations, keeps unsolved tails visible, turns repetition into
qualified procedural memory, and changes architecture only after cheaper and
less disruptive hypotheses have been tested. The system is modular so that
capabilities, tools, memories, benchmarks, permissions, and residuals can have
local owners and lifecycles rather than accumulating inside one opaque model.

RMI synthesizes five pillars: compact generative structure, active compression,
cognitive loop closure, benchmark ratcheting, and Octopus-style specialist
routing. The source's distinctive contribution is not any individual pillar.
It is the development loop joining them and the operational records that make
the loop inspectable.

## Claim Boundary and Cross-Paper Relationship

RMI overlaps substantially with the separately inventoried Octopus Router,
Cognitive Loop Closure, Benchmaxxing, and Compact Generative Systems papers.
Those papers are not independent confirmations of RMI. They are a related
author-side architecture lineage:

- Octopus Router supplies the most focused head/arm, registry, dynamic-loading,
  permission, memory, composition, and arm-lifecycle model.
- Cognitive Loop Closure owns the detailed trajectory-to-tool compiler,
  parameter-discovery process, verification, monitoring, and tool retirement.
- Benchmaxxing owns the detailed benchmark lifecycle, wall diagnosis,
  contamination, holdout, mutation, transfer, and anti-Goodhart program.
- Compact Generative Systems owns the seed/rules/memory/residual/verifier/
  governance abstraction as a representation family.
- RMI owns how those mechanisms form one governed capability-growth cycle,
  including the intervention ladder, three execution modes, ledgers, public
  calibration split, embodied logging, and phase order.

The source draws analogies to MDL, MoE, tool use, executable skill libraries,
liquid networks, KANs, HDC/VSA, active inference, WebAssembly, Rust, runtime
verification, and octopus neurobiology. These establish a design vocabulary,
not novelty or property transfer. The optional reference cognitive substrate
is a menu of candidate primitives, not an implemented architecture and not a
claim that the primitives compose cleanly.

RMI does not claim that monoliths, scaling, fine-tuning, or reasoning are
obsolete; that benchmarks perfectly measure intelligence; that every repeated
action should become a tool; that verification is absolute in open worlds;
that ordinary threshold decay is valid for critical failures; that routing is
easy; that more arms help; that humans are unnecessary; or that one topology
fits every deployment.

## Formal Object Model

At development cycle `t`, the source models the system as
`S_t = (H_t, A_t, R_t, M_t, T_t, B_t, G_t, E_t, V_t)`: head, arms, routing
policy, memory, tool registry, active benchmark frontier, regression suite,
residual escrow/failure map, and verification/safety layer. A task route
selects arms under context, budget, risk, and permissions; the head composes
their results; the verifier accepts, revises, expands, falls back, or refuses.

The proposed ratchet condition requires frontier performance to improve by
more than `epsilon` while regression performance falls by no more than
`delta`. This is a useful minimal statement but not sufficient as an admission
rule. A scalar frontier and floor can hide subgroup collapse, critical
failures, contamination, evaluator drift, selection effects, uncertainty,
cost displacement, or changed task identity. The book should interpret the
equations as a vector, consumer-scoped gate whose components retain their own
thresholds and vetoes.

Compact capability is represented as `(seed, rules, memory, residual,
verification, generation/governance interface)`. A loop closure maps multiple
successful trajectories into a parameterized tool accepted above a proposed
verification threshold. Residual escrow is the set of benchmark cases the
current system misses. These are architectural sketches; none proves that the
description is compact, the parameterization is complete, the verifier is
valid, or the residual taxonomy is causal.

## Conceptual Primitives

- **Pressure surface.** A benchmark, live task family, incident, or acceptance
  predicate that exposes uncertainty or missing capability. It is temporary
  and claim-scoped, not a permanent definition of intelligence.
- **Attempt.** Versioned routed execution with inputs, context, tools, outputs,
  costs, effects, verification, and selection lineage.
- **Residual.** Preserved discrepancy between an obligation and the observed
  outcome, including task, evaluator, benchmark, tooling, data, training,
  inference, architecture, or safety defects.
- **Active compression.** Conversion of experience into reusable memory,
  procedure, policy, benchmark, residual map, routing rule, specialist, or
  architecture. Compression is useful only if future work and verification
  become cheaper without losing required semantics or authority.
- **Loop closure.** Governed transition from recurring trajectories to a
  parameterized, verified, registered, monitored, and retireable tool.
- **Benchmark frontier.** Current unsaturated measurement instrument used to
  create learning pressure.
- **Regression floor.** Previously accepted behavior that a successor must
  preserve or explicitly re-authorize changing.
- **Residual escrow.** Owned unresolved tail that survives graduation,
  reappears in diagnosis, and may become a future frontier or regression.
- **Public calibration track.** Standardized external comparison surface kept
  separate from private, live, diagnostic, and internal frontier instruments.
- **Intervention ladder.** Ordered hypothesis sequence from instrument repair
  through data, training, inference, proceduralization, bridge curriculum, and
  architecture change.
- **Interpreter / compiled-tool / reflex modes.** Novel deliberation,
  qualified procedural execution, and hard-latency safety behavior. These are
  different control paths, not simply “slow/fast/faster” model settings.
- **System, benchmark, tool, and residual ledgers.** Versioned memory of what
  was evaluated, preserved, proceduralized, failed, changed, or retired.

## Mechanisms

### Pressure-to-structure ratchet

The full loop is pressure, attempt, residual, compression, verification,
structure, and new pressure. It is important that success and failure have
different products. Repeated success may justify a procedural candidate;
failure creates diagnosis and residual custody. Neither automatically changes
the model, creates a tool, or promotes a claim. Verification decides whether a
candidate structure satisfies its exact contract, and readiness decides where
it may be used.

“The frontier moves; the floor holds” therefore needs four ledgers at minimum.
The benchmark ledger preserves instrument identity and lifecycle. The system
ledger preserves model, router, arms, data, inference, costs, safety, and
current wall. The tool registry preserves source trajectories, parameters,
pre/postconditions, verification, runtime/risk, use and failure history, and
retirement. Residual escrow preserves origin, type, cluster, severity,
recurrence, reattempt, promotion state, and owner. A score without these joins
cannot demonstrate ratcheting.

### Loop closure and active parameter discovery

The ten-stage procedure is trajectory logging, loop detection, abstraction,
active parameter discovery, tool synthesis, verification, registration,
routing, runtime monitoring, and revision or retirement. Active discovery is
the crucial anti-brittleness step. Observed constants—currency, package
manager, citation requirement, file format, jurisdiction—may be hidden
parameters rather than invariants. Historical variance, counterfactual replay,
synthetic and adversarial cases, environment interrogation, and named human or
supervisor questions probe the boundary.

Candidate fields are classified as invariant, parameter, precondition, or
unknown assumption. The final class must remain unresolved until evidence
changes; it cannot be silently compiled as a default. The source's tool-value
rule weighs recurrence, savings, quality, and automation appropriateness
against creation, maintenance, risk, verification, and drift cost. The printed
formula is typographically incomplete and its variables are uncalibrated; it
should be retained as a decision-factor inventory, not an executable policy.

### Benchmark lifecycle, thresholds, and tail custody

Benchmarks move among frontier, diagnostic, graduated, regression, public
calibration, live, and retired states. This is not a monotone ladder: a
graduated or regression instrument can become contaminated, stale, noisy, or
invalid. Public calibration asks how the system compares under a shared
setting; private holdouts and live frontiers ask what generalizes and what to
improve next. Public scores should not directly select all internal changes,
or calibration becomes training data.

RMI proposes a high initial mastery threshold that may decay after stalled
cycles toward a floor for ordinary tasks. The source's 90%/70% examples and
decay equation are illustrative. Threshold decay is dangerous when it rewards
development impatience, changes the construct, hides subgroup tails, or makes
the system pass by waiting. Any decay needs prospective patience and slope,
stable task identity, uncertainty, subgroup floors, recurrence monitoring,
counterfactual comparison against continued work, and an explicit reason why
the residual cost is acceptable. Critical failures retain a veto or a
domain-specific near-zero bound; they never inherit ordinary decay.

Graduation moves every unsolved case into escrow. Items are clustered,
reattempted, promoted when recurrent, retired when the instrument is defective,
and added to regression only after consistent solution. “Preserve the tail” is
therefore stronger than keeping a list: descendants, bridge benchmarks, and
release decisions must inherit it.

### Diagnose before changing architecture

RMI's seven-level intervention ladder is the paper's most useful development
discipline:

1. audit labels, tests, solvability, contamination, construct validity, and
   transfer;
2. improve coverage, labels, curriculum, examples, and data quality;
3. change losses, optimizer, post-training, preference or reinforcement
   learning, distillation, and training allocation;
4. change retrieval, memory, search, planning, test-time compute, verification,
   tools, and decomposition;
5. close recurring successful loops into qualified procedures;
6. create bridge benchmarks when the learning jump is too large; and
7. change architecture only with a residual-specific mechanism hypothesis.

The order is not absolute—an unsafe or architecture-inexpressible target may
require immediate stop or redesign—but skipping earlier hypotheses must be
recorded. Each intervention changes one frozen factor or a declared bundle,
preserves rejected and null attempts, receives matched budget, and predicts a
causal signature. Architecture change is justified only when mechanism `X`
should improve residual class `B` while preserving floor `G`; a new model that
merely raises the same public score does not validate the diagnosis.

### Routed modular growth and lifecycle

RMI imports the Octopus head/arm architecture and attaches local frontiers,
regressions, residuals, tools, memories, permissions, and improvement loops.
Dynamic loading and memory/permission quarantine can reduce active footprint
and improve isolation, but these remain workload- and implementation-dependent
hypotheses. Add, split, merge, and retire signals are diagnostic inputs to
readiness and replacement transactions, not autonomous growth authority.

Independent arm improvement is valid only when shared router, memory, tool,
evaluator, data, and composition dependencies remain unchanged or are included
in the affected regression scope. A new arm can shift task difficulty and
selection across every incumbent; local scores alone do not show global
improvement.

### Three execution modes and runtime tiers

Interpreter mode handles novelty, ambiguity, creativity, underspecification,
and work outside known preconditions. Compiled-tool mode handles repeated,
parameterized, well-scoped work whose tests and risk are acceptable.
Reflex/failsafe mode handles hard latency, physical risk, deployment holds,
security/financial containment, tool failure, and boundary approach.

The source maps these onto text templates, structured workflows, typed
functions, sandboxes, memory-safe systems runtimes, and real-time reflex
controllers. The invariant is least-powerful-sufficient execution. A compiled
tool does not inherit open-ended reasoning authority, while a reflex must have
an independently testable trigger, deadline, safe action, override, monitor,
and post-event review.

### Hierarchical embodied logging

Raw embodied streams are too large and semantically weak to send directly into
loop detection. RMI separates raw telemetry for replay and forensics, event
logs for salient transitions, semantic traces for objects and task state,
skill traces for the active controller/tool/arm, and residual logs for
surprises, monitor violations, failures, and recovery. Their joint storage must
fit a declared budget.

This hierarchy is a lossy evidence pipeline. Event extraction and semantic
compression can omit the precursor that later explains an accident. Retention
therefore needs prospective hazard and consumer analysis, synchronized clocks,
cross-layer trace IDs, trigger-based raw pre/post buffers, integrity and access
controls, deletion policy, missingness, and replay tests. “Enough to debug” is
an outcome to measure, not a property of the log taxonomy.

## Interfaces and State Machines

A development cycle moves through frontier selected, attempt authorized,
execution observed, verification complete, residual classified, intervention
selected, candidate change evaluated, floor checked, structure admitted or
rejected, benchmark transitioned, and next frontier chosen. Every failed,
inconclusive, bypassed, and superseded intervention remains in the same lineage.

Benchmarks move among candidate, diagnostic, frontier, live, public
calibration, graduated, regression, contamination review, quarantined,
retired, and historical. Tools move among candidate, parameter-discovery,
synthesized, verified, probationary, registered, routed, monitored, revised,
quarantined, and retired. Residuals move among observed, typed, clustered,
escrowed, scheduled, active diagnostic, bridge target, recurring, solved,
regression, benchmark-defect, retired, and reopened.

Benchmark Ratchets owns instruments and frontier/floor transitions. Procedural
Memory owns tool compilation and lifecycle. Routing owns capability leases.
Readiness owns qualification and quarantine. Policy Optimization owns update
leases. Stable Capability Fields and Replacement own identity and rollback.
Embodied Control owns physical trace adequacy. Claim/Evidence owners decide
what any result supports. RMI composes these owners; it does not supersede them.

## Evidence

The source provides a coherent synthesis, equations, subsystem list,
trajectory-to-tool pipeline, parameter taxonomy, benchmark states, illustrative
threshold policy, residual rules, public/internal evaluation split, seven-level
intervention ladder, optional substrate menu, execution/runtime tiers,
embodied-log hierarchy, four registries, multi-level metrics, ten failure
modes, and eight implementation phases.

It reports no experiment or implementation. External examples and citations
inside the paper require independent source ingestion before they can support
the book. The example threshold values, critical-failure categories, tool-value
factors, and optional substrate roles are proposed design inputs, not validated
universal settings.

## Evaluation and Falsifiers

A serious campaign compares RMI against a strong fixed generalist, ordinary
fine-tuning/post-training, static tool use, a workflow platform, a simple
benchmark curriculum, and modular routing without ratchet governance. Freeze
task populations, public/private exposure, candidate budget, tools, context,
authority, evaluator, horizon, and stopping policy. Report:

- useful task success, calibration, subgroup/tail behavior, critical failures,
  regressions, abstention, and delayed outcomes;
- benchmark construct validity, contamination, mutation, transfer, saturation,
  residual value, public-calibration leakage, and retirement decisions;
- number, recurrence, severity, age, reopen rate, and closure quality of
  residuals;
- loop-detection precision/recall, parameter completeness, tool usefulness,
  verification miss rate, drift, failure, overlap, maintenance, and retirement;
- router and arm utility, composition fidelity, interference, bloat, lifecycle
  churn, dynamic-loading cost, and quarantine errors;
- intervention-specific marginal gain and causal signature at matched total
  data, training, inference, engineering, and evaluation budget;
- floor preservation across every system/tool/router/arm/benchmark change;
- compute, memory, storage, latency, energy, human work, verification,
  governance, migration, monitoring, and recovery cost; and
- embodied-log storage, loss, incident-reconstruction recall, detection delay,
  privacy exposure, and replay fidelity.

The framework should be narrowed or rejected if residual escrow becomes a
graveyard; threshold decay promotes worse systems by waiting; tools cost more
to verify and maintain than repeated reasoning; the intervention ladder merely
delays a necessary redesign; bridge benchmarks teach the proxy rather than the
target; arms and tools proliferate without held-out utility; public calibration
contaminates internal development; floor preservation blocks valuable
replacement or fails to catch real regressions; or the whole governed loop
loses to a simpler baseline on quality-adjusted total cost.

## Failure Modes

- **Benchmark gaming:** score gains without target-capability gains.
- **Tail obsession:** one instrument's final cases freeze broader progress.
- **Tail erasure:** graduation hides the unresolved cases that still matter.
- **Residual graveyard:** escrow has no owner, recurrence trigger, schedule, or
  route back to active work.
- **Threshold patience gaming:** waiting lowers the bar without new evidence.
- **Tool bloat:** frequent but low-value procedures consume verification,
  maintenance, security, and routing capacity.
- **False loop closure:** hidden parameters, preconditions, or side effects are
  compiled as invariants.
- **Arm bloat and router monolith:** modular labels conceal renewed central or
  local blobs.
- **Bad routing and composition:** the right capability is not selected or its
  result is misrepresented.
- **Under/over-quarantine:** authority or context is either excessive or
  insufficient.
- **Reflex gap:** a slow reasoning path is assumed where hard deadlines require
  a separate controller.
- **Architecture churn:** novelty substitutes for residual-specific diagnosis.
- **Bridge-benchmark detour:** an intermediate task becomes a new proxy and
  never transfers to the blocked frontier.
- **False independence:** an arm or tool update changes shared dependencies and
  regresses unmeasured consumers.
- **Ledger theater:** complete-looking records are not causally connected to
  executed artifacts or decisions.
- **Logging blindness:** semantic/event compression discards the evidence
  needed to reconstruct rare physical failures.

## Book Chapters Supported

- `the-efficient-asi-hypothesis` (The Efficient ASI Hypothesis)
- `capability-replacement-and-rollback` (Capability Replacement and Rollback)
- `recursive-self-improvement-boundaries` (Recursive Self-Improvement Boundaries)
- `open-ended-improvement-engines` (Open-Ended Improvement Engines)
- `procedural-memory-and-cognitive-loop-closure` (Procedural Memory and Cognitive Loop Closure)
- `routing-heads-and-specialist-cores` (Routing Heads and Specialist Cores)
- `replaceable-cognitive-substrates-beyond-transformer-monoculture` (Replaceable Cognitive Substrates: Beyond Transformer Monoculture)
- `readiness-gates-residual-escrow-and-quarantine` (Readiness Gates, Residual Escrow, and Quarantine)
- `personal-compute-hives-and-federated-edge-intelligence` (Personal Compute Hives and Federated Edge Intelligence)
- `compact-generative-systems-and-residual-honesty` (Compact Generative Systems: Generate, Verify, Repair, and Residual Honesty)
- `fast-generation-architectures` (Fast Generation Architectures)
- `benchmark-ratchets-and-anti-goodhart-evidence` (Benchmark Ratchets and Anti-Goodhart Evidence)
- `adversarial-evaluation-sandbagging-and-training-time-deception` (Adversarial Evaluation, Sandbagging, and Training-Time Deception)
- `embodied-agency-real-time-control-and-physical-safety` (Embodied Agency, Real-Time Control, and Physical Safety)
- `policy-optimization-and-learning-from-feedback` (Policy Optimization and Learning from Feedback)
- `artifact-steward-agents-and-living-project-governance` (Artifact Steward Agents and Living Project Governance)
- `integrated-reference-architecture` (Integrated Reference Architecture)
- `open-research-agenda-and-bibliography-plan` (Open Research Agenda and Bibliography Plan)

## Claims To Add Or Update

- Treat pressure-to-structure ratcheting as a joined development transaction,
  not an inference from benchmark score or module count.
- Preserve distinct benchmark, system, tool, and residual ledgers with exact
  identity and causal joins to executed outputs and decisions.
- Add a prospectively ordered, residual-specific intervention ladder before
  architecture change, with explicit bypass reasons and causal predictions.
- Bound time-decayed mastery thresholds by construct stability, uncertainty,
  subgroup floors, critical vetoes, and residual inheritance; never reward
  waiting by itself.
- Keep public calibration separate from private/live frontiers and record its
  exposure budget.
- Preserve interpreter, compiled-tool, and reflex paths as different authority,
  latency, verification, and failure contracts.
- Add hierarchical embodied logging with cross-layer trace identity,
  trigger-based raw buffers, loss accounting, incident-reconstruction tests,
  privacy, and retention governance.
- Test “independent improvement” against shared router, memory, tool,
  evaluator, data, and composition dependencies.

## Section-Family Closure Ledger

| Section family | Disposition |
|---|---|
| Executive synthesis, fragmentation problem, and pressure pattern | Thesis and complete joined ratchet retained here and integrated across Benchmark, Procedural Memory, Routing, and Readiness. |
| Benchmark-, tool-, and monolith-only objections | Preserved as distinct failure boundaries; no competing technique is declared obsolete. |
| Definition and seven core objects | Reconstructed in the object model and canonical owner split. |
| Formal system, route, verification, and frontier/floor equations | Retained as proposed sketches; scalar insufficiency and vector-gate obligations made explicit. |
| Five pillars | Cross-paper lineage reconciled; RMI owns the growth composition, not independent corroboration of its component papers. |
| Nine-subsystem architecture, head, arms, loading, quarantine, memory | Canonical in Routing and the deep Octopus audit; retained here only where the ratchet adds local frontier/residual/lifecycle meaning. |
| Ten-stage loop closure and parameter discovery | Canonical in Procedural Memory; deep note preserves active probes, four-way variable classification, and hidden-assumption residuals. |
| Tool acceptance rule | Retained as a cost-factor inventory; malformed/un-calibrated formula is not executable policy. |
| Benchmark lifecycle and public calibration | Canonical in Benchmark Ratchets; public/internal role separation and exposure boundary preserved. |
| Mastery, decay, critical veto, and escrow | Added to Benchmark Ratchets with anti-waiting, subgroup, uncertainty, and inheritance constraints. |
| Seven-level intervention ladder | Added directly to Benchmark Ratchets as residual-specific diagnosis before architecture change. |
| Optional liquid/reservoir/KAN/HDC/active-inference substrate | Retained as an untested candidate menu; Replaceable Substrates owns actual comparison. |
| Interpreter, compiled-tool, reflex modes and E0–E5 tiers | Canonical across Procedural Memory, Runtime, Fast Generation, and Embodied Control; no certification inferred. |
| High-bandwidth embodied logging | Added to Embodied Control with trace joins, raw-ring buffers, information-loss, privacy, and reconstruction obligations. |
| Arm lifecycle | Canonical in Routing/Readiness/Replacement; RMI adds ratchet-specific global-regression and false-independence conditions. |
| Four ledgers and registries | Fields retained here and distributed to Benchmark, Procedural Memory, Routing, Readiness, Artifact Graphs, and Integrated Architecture owners. |
| Five metric families | Converted into a joint evaluation program including total lifecycle and governance cost. |
| Ten failure modes | Preserved and expanded with residual graveyard, patience gaming, false closure, bridge detour, false independence, ledger theater, and logging blindness. |
| Eight implementation phases | Retained as dependency-aware obligations; no phase or goal is represented as completed by the paper. |
| Claims, non-claims, conclusion | Preserved in the source boundary; manifesto/public-summary repetitions create no new claim or chapter. |
| Selected references | Bibliographic leads only until independently ingested from primary sources. |

## Open Questions

- What multi-dimensional floor permits useful replacement without either
  freezing progress or hiding regressions behind aggregate tolerance?
- How should residual recurrence be estimated when routing and evaluator
  policies change which failures are observed?
- Can a prospectively ordered intervention ladder distinguish a genuine
  architecture wall from insufficient search over cheaper interventions?
- What prevents bridge benchmarks from becoming permanent proxy curricula?
- When does proceduralization reduce total cost after verification,
  maintenance, drift, security review, and retirement are included?
- How can public calibration remain comparable without becoming a direct
  optimization target or contamination source?
- Which logging abstraction retains rare causal precursors under strict
  storage, privacy, and real-time constraints?
- Can local arm ratchets improve global utility when router selection and
  shared dependencies create strong observational selection bias?
