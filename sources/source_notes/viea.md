# Source Note: Verified Intent-to-Execution Architecture

| Field | Value |
|---|---|
| Source ID | `viea` |
| Source title | Verified Intent-to-Execution Architecture |
| Ingestion date | 2026-06-24 |
| Source version / URL | Public Release v1.0, May 2026; https://docs.google.com/document/d/1SDu8MWw4dOpFqwLqA8vpE1rV98O2_GeJgVlgb6R9GsM |
| Ingestion basis | Local raw cache inspected at `sources/raw/google_docs/viea.txt`; raw text is not published. |

## Thesis

VIEA frames advanced AI as an intent-to-execution system rather than a response generator. Human intent should become structured command contracts, durable artifacts, specialist-routed work, verified outputs, runtime execution, feedback, residuals, tools, benchmarks, and regression coverage.

The expanded paper makes a second, less obvious claim: closing the execution
loop requires governing the *interfaces between* those subsystems. Intent
drafting can create automation bias; artifact durability can create memory
bloat; modular specialists can create contextual shattering; verification can
collapse into self-agreement; human approval can become an exhausted
bottleneck; successful tools can rot; and a powerful online conductor can
become another monolith. VIEA therefore proposes friction gradients,
retention classes, epistemic diversity, qualified approval budgets,
transactional integration, and a fast-policy/slow-learning split.

## Claim Boundary and Status

- VIEA is an architecture proposal, object model, implementation sequence, and
  evaluation agenda. It is not a completed system or deployment report.
- It argues that consequential intent should cross explicit contracts,
  artifacts, permissions, verification, integration, runtime, and feedback
  boundaries. It does not claim that structure removes ambiguity, that
  specialists always outperform monoliths, or that verification is absolute.
- Its numerical thresholds, retention intervals, mastery floors, and example
  equations are design defaults, not empirical constants.
- Its physical, fabrication, organizational, and spatial runtimes are
  extensions of one interface pattern, not evidence that those runtimes are
  implemented or safe.

## Conceptual Primitives and Distinctions

- **Intent checksum:** a short human-readable statement of what the system
  believes the user wants.
- **Assumption diff:** material target, audience, output, tone, evidence, and
  authority assumptions inferred while compiling raw intent.
- **Friction gradient:** raw, one-line, quick, working, and full command modes
  that scale confirmation burden with consequence.
- **No silent hardening:** the system may infer structure, but not authority.
- **Artifact classes:** core, support, transient, archived, deprecated, and
  residual artifacts with different retention and retrieval behavior.
- **Preserve provenance, route relevance:** durable storage does not imply that
  every artifact enters every context.
- **Claim waiver:** an expiring low-risk reduction in tracking overhead that
  cannot provide evidence or flow into high-impact work without reactivation.
- **Epistemic collapse:** false confidence produced when generator,
  researcher, skeptic, and verifier share one model or evidence dependency.
- **Fast Router / Slow Conductor:** bounded online policy execution separated
  from asynchronous routing diagnosis and policy improvement.
- **Contextual shattering:** locally valid specialist outputs that are globally
  incompatible.
- **Tool maturity and rot:** compiled procedures move through candidate,
  draft, shadow, assisted, active, certified, and retired states, then lose
  trust as evidence, dependencies, environments, or residuals drift.

## Mechanisms

- Structured command layer with role, objective, context, constraints, procedure, output contract, verification, and failure behavior.
- Artifact graph for claims, requirements, critiques, releases, feedback, tools, benchmarks, and residuals.
- Claim and verification ledger that separates verified, speculative, unsupported, contradicted, and experiment-required statements.
- Orchestrator/router, specialist modules, workflow-to-tool compiler, evaluation ratchet, runtime adapters, and feedback loop.
- Rule of durability: important responses become artifacts, repeated work becomes tools, claims receive support states, failures become residuals, and mastered capabilities become regression coverage.
- Compile raw intent with a risk-scaled friction gradient. For medium and high
  consequence work, expose an intent checksum, assumption diff, one
  misalignment probe, and the fields requiring confirmation; never infer an
  execution authority from an ambiguous request.
- Prevent artifact-graph overload with retention classes, hash-link survival
  rules, summarization/archive policies, and active-context selection by
  command, type, dependency distance, recency, support state, specialist,
  runtime, permission, and residual relevance.
- Allow explicitly scoped claim waivers for low-risk private artifacts, but
  re-extract and classify claims before the artifact supports a release,
  benchmark, deployment, fabrication packet, or other high-impact consumer.
- Cap model-only agreement below verified standing. High-impact claims require
  at least one external source, executable check, independent tool, qualified
  human, empirical result, formal proof, or real-world feedback, with automatic
  downgrade when support expires or is defeated.
- Treat qualified human review as a finite resource: bind approver identity,
  competence, authority, risk tier, queue, latency, fatigue, and budget; batch
  low-risk changes and block critical actions when no qualified approver is
  available.
- Split routing into a low-latency, policy-constrained Fast Router with hard
  call/token/compute/latency/cost/review caps and an asynchronous Slow
  Conductor that clusters routing residuals and proposes policy, specialist,
  and fallback changes outside the critical path.
- Preserve routing residuals by type: wrong or missing specialist, context
  under- or over-allocation, unresolved conflict, skipped verification,
  over-routing, under-routing, and permission mismatch.
- Require structured specialist outputs and an Integration Layer that checks
  global constraints, interfaces, invariants, runtime assumptions, budgets,
  and failure behavior before locally valid work becomes executable.
- Treat high-impact multi-specialist integration as a transaction: reject the
  whole candidate on incompatibility, preserve the failed bundle, restore the
  last known valid checkpoint, record the residual, and require a revised
  integrated candidate.
- Compile repeated trajectories only after recurrence across contexts,
  verification, and critical-failure checks; progress tools through maturity
  states and revalidate on time, dependency, environment, runtime, risk,
  verification-suite, or residual drift.

## Interfaces, Artifacts, and State Machines

- `IntentChecksum`, `AssumptionDiff`, `MisalignmentProbe`, and
  `RiskConfirmationReceipt` connect natural-language intake to command
  authority without treating a generated contract as user intent.
- `ArtifactRetentionPolicy`, `HashLink`, `ActivityState`, and
  `ContextSelectionReceipt` connect durable provenance to bounded retrieval.
- `ClaimWaiver` binds artifact, reason, risk tier, scope, expiry, and approver;
  a downstream-use transition either reactivates claim extraction or rejects
  the dependency.
- `ApprovalCapacityRecord` binds role, qualification, authority, queue,
  latency, fatigue, and remaining review budget.
- `RouteDecision` binds specialist calls, permissions, context, compute,
  latency, money, human-review requests, risk tier, and fallback behavior;
  `RoutingResidual` feeds the slow policy-update lane.
- `SpecialistOutputContract` carries result, confidence, assumptions, evidence,
  compatibility requirements, risks, residuals, verification, provenance,
  and cost.
- `IntegrationContract` binds global objective, shared constraints, interfaces,
  runtime, budgets, invariants, integration tests, failure boundaries, and
  rollback behavior.
- `ToolLifecycle` progresses candidate → draft → shadow → assisted → active →
  certified → retired; revalidation or decay can move a tool backward.

## Assumptions, Invariants, and Conditional Results

- Inferred structure never grants undeclared authority.
- A waiver reduces local process cost but creates no evidence and cannot be
  inherited by a higher-consequence consumer.
- Internal model consensus cannot by itself establish verified standing.
- Preserving an artifact does not authorize loading it into an unrelated or
  less-privileged context.
- Local specialist validity is insufficient for execution; the integrated
  state must satisfy the shared contract.
- The Slow Conductor proposes policy changes; it does not bypass the Fast
  Router's current policy, approval, or budget boundary.
- A previously successful tool retains no timeless entitlement to trust.
- Execution into shared reality requires the gate appropriate to its runtime
  and consequence tier.

## Algorithms and Implementation Program

1. Build the narrow text-only vertical slice: raw intent, drafted contract,
   checksum/diff confirmation, artifact graph, claim/critique ledger,
   specialist outputs, integration receipt, release manifest, and feedback
   plan.
2. Add risk-tiered permission and approval records before digital execution.
3. Add Fast Router budget enforcement and residual capture before adaptive
   routing.
4. Add offline Slow Conductor recommendations with human/policy review before
   allowing routing-policy updates.
5. Add shadow tool compilation, maturity transitions, confidence decay, and
   revalidation before automatic procedural reuse.
6. Add digital runtime adapters and whole-system rollback before physical,
   fabrication, robotic, organizational, or spatial targets.

## Evidence

- The source is an architecture proposal and systems framework, not a completed deployment report.
- It supplies concrete subsystem definitions, vertical-slice implementation guidance, and repeated benchmark/residual discipline.
- Reported mechanisms should be treated as design sources until corresponding code, tests, or execution logs are added to the book repo.

## Evaluation, Falsifiers, and Competing Baselines

- Measure command correction rate, ambiguity reduction, and authority errors
  for free-form prompting versus checksum/diff confirmation.
- Compare typed retention and active-context selection against append-only
  conversation history and unfiltered retrieval on relevance, provenance
  retention, latency, privacy, and artifact-bloat rate.
- Compare monolithic execution, direct specialist composition, and
  integration-contract composition on whole-system failure and rollback rates.
- Compare one adaptive conductor against the fast/slow split on latency,
  runaway orchestration, routing accuracy, residual recurrence, and policy
  stability.
- Compare no tool compilation, immediate compilation, and maturity-gated
  compilation on total lifecycle cost, drift failures, and safe fallback.
- The design narrows if confirmation adds friction without reducing material
  intent error; if filtered artifact graphs lose necessary provenance; if
  integration gates reject useful work without lowering system failures; if
  the slow lane cannot improve routing safely; or if tool maintenance and
  verification cost exceed reuse value.

## Failure Modes

- Treating generated text as execution.
- Losing artifacts, constraints, source evidence, residuals, or deployment feedback across turns.
- Re-performing repeated workflows instead of compiling verified reusable tools.
- Claim support inflation when evidence is missing.
- Automation bias: a user approves a fluent but incorrect auto-drafted command.
- Silent authority hardening: the system converts ambiguity into permission.
- Artifact bloat, stale retrieval, or sensitive-context over-allocation.
- Waiver laundering from a low-risk draft into a consequential downstream use.
- Epistemic collapse through correlated models, tools, data, or incentives.
- Approval theater caused by unqualified reviewers, fatigue, excessive queues,
  or unavailable critical authority.
- Runaway orchestration and a Slow Conductor that becomes a privileged online
  monolith.
- Contextual shattering across locally correct specialists.
- Partial application after integration failure.
- Premature workflow compilation, tool proliferation, tool rot, and stale
  confidence after environment or dependency drift.

## Threats, Misuse, and Governance Costs

- Prompt injection and artifact poisoning can alter command, context, route,
  tool, or runtime decisions unless provenance and permission boundaries are
  enforced at consumption time.
- Review, storage, verification, residual reattempt, and tool-maintenance costs
  can dominate model inference; VIEA's benefits must be assessed on total
  lifecycle cost rather than generation quality alone.
- Human approval introduces capacity, labor, privacy, legitimacy, and capture
  risks; it is neither free nor automatically competent.
- Physical and organizational runtime adapters can create irreversible or
  distributed effects for which artifact rollback is insufficient.

## Book Chapters Supported

- ASI Is a Stack, Not a Model
- The Efficient ASI Hypothesis
- System Boundaries and Authority
- Failure Modes of Ungoverned Intelligence
- Evidence States and Claim Discipline
- Stable Capability Fields
- Recursive Self-Improvement Boundaries
- Human Intent as a Formal Input
- `intent-to-execution-contracts` (Command Contracts: From Intent to Executable Work; includes folded command-contract semantic-interface material)
- Planning as a Control Layer: DAGs and Intelligence Arbitrage
- Cognitive Compilation and Semantic IR
- The Virtual Context ABI: Typed Pages, Cells, and Certificates (`virtual-context-abi`)
- Claim Ledgers and Belief Revision
- Labor OS and Typed Jobs
- Artifact Graphs, Audit Logs, and Replay
- Runtime Adapters, Tool Permissions, and Human Approval
- Resource Economics and Token Budgets
- `embodied-agency-real-time-control-and-physical-safety` (Embodied Agency, Real-Time Control, and Physical Safety)
- Executable Specifications and Lean Proof Envelope
- `routing-heads-and-specialist-cores` (Routing Heads and Specialist Cores; includes folded MoECOT Runtime Crosswalk)
- Artifact Steward Agents and Living Project Governance
- Integrated Reference Architecture
- Prototype Roadmap
- Living Book Methodology
- `human-factors-and-meaningful-control-in-oversight`
- `governed-operations-incident-command-and-graceful-degradation`

## Claims To Add Or Update

- Use VIEA as the main execution spine connecting intent, artifacts, routing, verification, runtime adapters, and feedback.
- Use VIEA to ground the book's stack thesis in durable artifacts, support states, residuals, regression coverage, and intent-to-execution handoff boundaries.
- Use VIEA as connective architecture for planning, context handoff, claim ledgers, labor execution, runtime adapters, resource accounting, and executable-spec priorities without claiming those subsystems are implemented here.
- Keep any VIEA-derived claim at `source-derived` only after the specific source passage is mapped in Appendix C.
- Treat implementation and benchmark claims as unproven until matching artifacts exist in `experiments/`, `test_results/`, or inspected external repos.
- Add the intake invariant that structure may be inferred but authority may not.
- Add selective durability: provenance is preserved while relevance,
  permission, and consequence determine context activation.
- Add claim waivers as expiring overhead controls with mandatory downstream
  reactivation, not as a new support state.
- Add the Fast Router / Slow Conductor split and routing-residual taxonomy.
- Add contextual shattering and transactional integration as the recomposition
  complement to modular decomposition.
- Add tool maturity, confidence decay, and revalidation as core procedural
  memory lifecycle requirements.

## Cross-Paper Synthesis and Tensions

- VIEA supplies the whole-stack execution spine; SCF supplies stronger exact
  identity, qualification, lifecycle, and replacement rules for its tools and
  specialists.
- PlanForge supplies the task graph, while VIEA adds intake confirmation,
  integration, approval capacity, runtime, and feedback around it.
- Cognitive Loop Closure supplies trace-to-tool compilation; VIEA adds
  economic acceptance, maturity, rot, and revalidation.
- Octopus/MoECOT supply modular routing; VIEA corrects their monolith risk with
  a bounded fast policy and an offline learning conductor.
- Spinoza/UAT supply stronger verification and disagreement processes; VIEA
  adds the minimum rule that model consensus alone cannot create verification.
- VCM and QCSA can implement active context selection, but VIEA requires them
  to preserve provenance while respecting permission and relevance.
- Talos supplies typed job and execution custody; VIEA's Integration Contract
  is the whole-job boundary that prevents individually valid outputs from
  partially crossing into execution.

## Section-Family Coverage

- §§1–4: thesis, loop, principles, architecture → stack and integrated
  architecture owners.
- §§5–7: intent capture, automation-bias control, command contract → Human
  Intent and Command Contracts.
- §§8–9: artifact graph, retention, relevance → Artifact Graphs and Virtual
  Context ABI.
- §§10–12: claim states, waivers, epistemic-collapse control → Claim Ledgers
  and Proof-Carrying Claims.
- §§13–14: provenance, permissions, qualified approval capacity → Runtime
  Adapters and Human Factors.
- §§15–19: fast/slow routing, routing residuals, specialist contracts,
  transactional integration → Routing Heads and Integrated Architecture.
- §§20–22: workflow compiler, acceptance, maturity, rot, revalidation →
  Procedural Memory and Resource Economics.
- §§23–24: evaluation ratchet and operational metrics → Benchmark Ratchets.
- §§25–31: runtime adapters, budgets, economics, safety gates, workspace,
  threats, feedback → runtime, resource, security, operations, and integrated
  owners.
- §§32–38 and appendices: implementation sequence, claims/non-claims, object
  model, operating rules, and Codex handoff → Prototype Roadmap and source-note
  retention. No implementation result is inferred.

## Open Questions

- Which VIEA subsystems become executable schemas in Appendix D first?
- Which one vertical slice should be the first prototype-backed demonstration?
- Which runtime targets should remain speculative until source-backed examples exist?
