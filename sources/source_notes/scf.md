# Source Note: Stable Capability Fields

| Field | Value |
|---|---|
| Source ID | `scf` |
| Source title | Stable Capability Fields |
| Ingestion date | 2026-06-24 |
| Source version / URL | Public Release 1.0, 23 June 2026; https://docs.google.com/document/d/1hQ9LqEgpeHo2SAntUVk15Eegms_xRVfOhtndVM5TDS4 |
| Ingestion basis | Local raw cache inspected at `sources/raw/google_docs/scf.txt`; raw text is not published. |

## Thesis

SCF separates a capability's durable semantic identity from the replaceable machinery that realizes it. A field is a governed substitution boundary binding contracts, artifacts, profiles, state, evaluator policy, evidence, qualification, routing, authority, lifecycle events, and recovery paths.

Its deeper thesis is that recursive improvement is an authorization and
continuity problem, not merely candidate generation. A long-lived system must
be able to change models, prompts, tools, evaluators, state representations,
policies, and even parts of its governance without letting the machinery that
proposes an improvement redefine “better,” inherit undeclared authority,
invalidate its own evidence, or destroy the path back. SCF therefore makes
qualification a scoped, defeasible, expiring claim over exact artifacts,
consumers, profiles, state, evidence, and effects.

## Claim Boundary and Status

- SCF is a research synthesis, formal architecture, executable specification
  fragment, threat model, conditional-property argument, reference design, and
  empirical agenda—not evidence that governed recursive improvement works.
- It conditionally improves visibility, localization, contestability, and
  recovery when identity, enforcement, evidence, and governance premises hold.
  It does not solve alignment, strategic deception, objective selection,
  institutional legitimacy, covert channels, semantic contract completeness,
  or irreversible effects.
- “Stable” applies to a governed semantic boundary, not to frozen behavior,
  permanent implementations, one universal ontology, or proof that cognition
  is naturally modular.
- Source-reported companion checks are engineering sanity checks, not
  independent verification, production performance, or empirical AI-safety
  evidence.

## Conceptual Primitives and Distinctions

- **Field / implementation / route / qualification:** durable semantic and
  authority identity, one realizing artifact, one invocation choice, and one
  scoped permission to rely on evidence are four different objects.
- **Normalized lifecycle dimensions:** qualification verdict, deployment
  stage, route role, restrictions, incident state, evidence state, and
  lifecycle state remain orthogonal rather than collapsing into “active.”
- **Contract clause classes:** mechanically enforced, protocol, deterministic,
  statistical, calibration, runtime-monitorable, governance, aspirational,
  and explanatory clauses require different evidence and enforcement.
- **Contract debt:** incomplete or unknown behavior is a named, owned,
  expiring risk object rather than an omitted specification.
- **Goalpost firewall:** contract changes and implementation changes are
  separate transactions; a candidate cannot be retroactively certified merely
  because the norm was weakened to fit it.
- **Profile transfer witness:** evidence reuse is claim-, artifact-, property-,
  and profile-specific, not a global ranking between implementations.
- **Property-sensitive invalidation:** a dependency change invalidates claims
  along the properties on which they relied, while unknown reliance fails wide.
- **Migration solvency:** state movement is isomorphic, loss-bounded,
  dual-representation, replay-from-source, or non-solvent; schema compatibility
  alone does not establish semantic reversibility.
- **Independence vector:** evaluator separation is measured across model,
  provider, data, tools, operators, prompts, memory, organization, incentives,
  and lineage rather than asserted as a Boolean.
- **Consequence-bounded canary:** exposure is limited by maximum possible
  consequence, not merely by traffic percentage.
- **Adaptation epoch:** high-frequency updates occur under a pinned updater,
  data policy, authority/effect ceiling, risk budget, journal, sentinels,
  baseline, and revocable epoch token.
- **Effective TCB:** every clock, key service, broker, isolation boundary,
  derivation rule, policy checker, state service, and recovery path required by
  a property counts as trusted.

## Mechanisms

- Stable field identity with versioned contracts and exact content-bound implementation artifacts.
- Append-only evidence and consequence registry with deterministic views.
- Scoped, defeasible, expiring qualification claims.
- Untrusted route proposer paired with a narrow validator for claims, leases, profiles, grants, state paths, and composition certificates.
- State migration solvency, canary stages, online adaptation envelopes, federation, incidents, appeals, and constitutional governance controls.
- Bind contracts by content hash and cover inputs, outputs, protocols,
  invariants, effects, authority, state, resources, failures, uncertainty,
  observability, privacy, retention, and governance—not only schemas.
- Record contract debt with affected behavior, uncertainty, evidence gap,
  severity, blast radius, monitor gap, owner, controls, expiry, and closure
  criterion; debt may narrow authority, shorten leases, or block promotion.
- Put synthesized contracts behind a goalpost firewall: freeze the motivating
  candidate, dual-run old and proposed contracts on anchors and
  counterexamples, compute a semantic/authority/state/evidence diff, disclose
  evaluator overlap, and forbid ordinary waivers from broadening authority.
- Use an append-only evidence and consequence graph with deterministic,
  versioned materialized views; operational caches bind source head,
  watermark, derivation hash, and view hash and never become independent
  authority.
- Apply property-sensitive invalidation to named reliance edges. Reliance
  annotations and compatibility witnesses are themselves qualified artifacts;
  missing or disputed edges expand the impact cone.
- Resolve routes through an untrusted optimizer and a smaller validator that
  checks declared identity, claim, lease, role, state, authority, consequence,
  and composition certificates at invocation time.
- Revalidate authority after approvals and before effects, bind caller,
  request, purpose, destination, quota, delegation, consequence, and expiry,
  and treat individually admissible but jointly toxic capabilities as a
  separate composition problem.
- Govern evaluator portfolios through explicit veto, statistical, tail-risk,
  disagreement, expiry, and update policies; dual-run evaluator changes and
  retain evidence debt when independence is limited.
- Execute improvement as propose → immutable register → impact cone → isolate
  → qualify → rehearse state/containment/recovery → shadow → canary →
  production → convergence observation → renewal/narrowing/expiry →
  containment/compensation/quarantine → retirement/revision/fork.
- Separate a minimal root, certified policy layer, governed intelligent
  meta-layer, and ordinary fields. Rich reasoning proposes certificates; the
  root checks bounded mechanics and can deny, revoke, or load a protected
  recovery route.
- Govern constitutional membership through predecessor-authorized fixed
  epochs, thresholds, diversity constraints, transparency inclusion, and
  timelocks. Emergency power may narrow, freeze, revoke, isolate, or recover;
  it may not silently broaden ordinary authority or rewrite history.

## Interfaces, Artifacts, and State Machines

- `FieldManifest` binds field identity, contract, implementation bundle,
  dependency closure, profiles, state relations, evaluator policy, authority,
  lifecycle, evidence, routes, incidents, recovery, and governance.
- `QualificationClaim` binds exact proposition, artifacts, relied properties,
  profile, evidence, assumptions, evaluator, issuer, trust domain, interval,
  defeaters, and expiry.
- `ProfileTransferWitness` states which claim and properties transfer between
  exact profiles and why; it cannot create a global total ordering.
- `RelianceAnnotation` and `CompatibilityWitness` carry provenance, negative
  tests, review, expiry, and incident history because impact-cone minimization
  is itself adversarial.
- `StateRelation` names source and destination state, transformation class,
  preserved and lost semantics, dual-run or replay path, privacy effects,
  fallback reachability, and insolvency.
- `RouteReceipt` binds proposal, validator/policy revision, caller, purpose,
  role, exact route, grants, leases, source-log/view identities, fallback,
  effect ceiling, and terminal outcome.
- `AdaptationEpoch` binds updater, data receipts, baseline, journal,
  sentinels, cumulative budgets, authority/effects, checkpoints, breach rules,
  and revocation token.
- `ConstitutionalEpoch` binds fixed members, roles, threshold/diversity,
  predecessor, transparency commitment, timelock, and effective interval.

## Assumptions, Invariants, and Conditional Results

- Exact identity, signatures, clocks, event derivation, isolation, brokers,
  revocation, and recovery roots must remain outside the candidate's unilateral
  control for the corresponding properties to hold.
- A field version never authorizes by human-readable alias alone.
- A candidate cannot inherit authority, evidence, state compatibility, or
  consumer trust from its predecessor without exact scoped witnesses.
- Aspirational clauses remain limitations; they cannot be laundered into hard
  guarantees by schema presence or review consensus.
- Invocation-time validity dominates stale stored routes.
- Unknown dependencies fail wide; a suspiciously small impact cone is not a
  success metric without low unsafe-reuse evidence.
- Local conformance does not imply safe cross-field composition.
- Artifact availability is not state-migration solvency, and artifact rollback
  is not reversal of external effects.
- Emergency governance can reduce or recover authority but cannot expand the
  constitution through the emergency path.

## Algorithms and Implementation Program

1. Seed a few high-value fields with content-addressed contracts and candidates,
   route-proposal/validation separation, mediated tool grants, and signed
   lifecycle events.
2. Add profile-scoped claims, state relations, shadow/canary authorization,
   incidents, fallbacks, and verifiable materialized views.
3. Add evaluator fields, contract synthesis behind the goalpost firewall,
   adaptation epochs, multi-field impact cones, threshold governance,
   federation, and root dual-running.
4. Rehearse root replacement separately from ordinary field replacement using
   isolated builds, conformance/proof/fault tests, old/new dual-run, threshold
   authorization, dormant slots, narrow activation, and offline recovery.
5. Benchmark semantic preservation, unsafe reuse, evaluator capture, migration
   fidelity, composition, consequence-bounded canaries, recovery, useful
   throughput, and governance cost against simpler registries and canaries.

## Evidence

- The source is a research synthesis, formal architecture, executable specification fragment, and evaluation agenda.
- It includes conditional safety properties and proof sketches, but the note does not treat companion measurements as independent AI-safety evidence.
- Strong claims about production safety, global alignment, strategic deception, or reversibility remain explicitly out of scope.

## Evaluation, Falsifiers, and Competing Baselines

- Compare SCF with a flat registry, interface/SemVer checks, provenance-only
  admission, benchmark-only promotion, and conventional canary/rollback.
- Inject missing reliance edges, overly narrow property labels, false
  compatibility witnesses, behavior drift behind stable interfaces, candidate
  and analyzer collusion, evaluator overlap, stale views, lease expiry,
  migration corruption, toxic compositions, and recovery-path loss.
- Measure semantic and failure-contract preservation, unauthorized effects,
  unsafe evidence reuse, tail regressions, evaluator disagreement and capture,
  state/privacy loss, composition failure, effect coverage, recovery time,
  incident recurrence, useful throughput, missed help, latency, human labor,
  governance delay, and residual burden.
- The thesis narrows if a simpler boundary dominates the joint usefulness and
  safety frontier; if field boundaries cannot be specified or tested; if
  reliance metadata creates more unsafe reuse than it saves; if state cannot be
  migrated or recovered; if evaluator and governance capture remain
  indistinguishable; or if bureaucracy blocks useful improvement without
  lowering consequential failures.

## Failure Modes

- Capability slots laundering authority from one implementation to another.
- Contract drift, evaluator capture, state migration insolvency, dependency drift, bad reliance annotations, and recovery failure.
- Procedural self-ratification when candidates affect the evaluator or governance process that judges them.
- Goalpost movement that weakens the contract to fit the motivating candidate.
- Contract debt hidden behind a complete-looking schema.
- Evidence reuse through missing, false, or overly narrow reliance metadata.
- Stale or directly mutated materialized views used as route authority.
- Waivers relabeled as passes or transferred across profiles.
- Evaluator portfolios that share one model, provider, data, memory, toolchain,
  operator, or incentive and simulate independence.
- Canary scope measured by traffic while durable or irreversible consequence
  remains large.
- Online adaptation that drifts between promotions or exhausts sequential risk
  budgets before sentinel detection.
- Dangerous composition among individually admissible fields.
- A “small” TCB argument that omits clocks, keys, brokers, derivation rules,
  isolation, state, or recovery dependencies.
- Constitutional, registry, or recovery-root capture; denial of governance and
  incumbent protection through excessive assurance cost.

## Threats, Misuse, and Governance Costs

- A strategically aware candidate may game tests, reliance analysis,
  contract synthesis, evaluators, reviewers, canaries, or incident closure.
- Federation adds revocation latency, divergent interpretations, selective
  disclosure, and coordination races; centralization adds coercion and capture.
- Auditability conflicts with privacy, deletion, data minimization, and the
  right not to preserve sensitive traces indefinitely.
- Assurance can become a denial-of-service or political power mechanism. The
  system must measure proposal backlog, review delay, appeals, rejected useful
  work, operator burden, and who controls the trust roots.

## Book Chapters Supported

- ASI Is a Stack, Not a Model
- System Boundaries and Authority
- Failure Modes of Ungoverned Intelligence
- Stable Capability Fields
- Capability Replacement and Rollback
- Recursive Self-Improvement Boundaries
- Routing Heads and Specialist Cores
- `replaceable-cognitive-substrates-beyond-transformer-monoculture` (Replaceable Cognitive Substrates: Beyond Transformer Monoculture)
- Readiness Gates, Residual Escrow, and Quarantine
- Personal Compute Hives and Federated Edge Intelligence
- Executable Specifications and Lean Proof Envelope
- Policy Optimization and Learning from Feedback
- Artifact Steward Agents and Living Project Governance
- Integrated Reference Architecture
- Prototype Roadmap
- Open Research Agenda and Bibliography Plan
- `human-factors-and-meaningful-control-in-oversight`
- `governed-operations-incident-command-and-graceful-degradation`

## Claims To Add Or Update

- Use SCF as the core governed self-improvement substrate.
- Use SCF to define capability identity, authority ceilings, evaluator boundaries, and rollback constraints wherever the book discusses stack-level safety or replacement.
- Use SCF to govern whether policy updates are promoted, quarantined, rolled back, or kept experimental, especially when an update could affect authority, evaluator policy, or lifecycle state.
- Distinguish implementation updates from contract/evaluator/governance updates.
- Formalize exact identity binding, qualification, route validation, lifecycle ordering, and authority non-escalation as priority Lean/code targets.
- Add contract debt and the goalpost firewall wherever learned systems can
  change the tests, contracts, or policies that evaluate them.
- Add property-sensitive invalidation with fail-wide unknown dependencies and
  qualified reliance annotations.
- Replace vague evaluator independence with a disclosed overlap vector and
  dual-run change control.
- Distinguish traffic-limited canaries from consequence-bounded canaries.
- Count the effective TCB by claimed property rather than calling the kernel
  small after omitting its dependencies.
- Make emergency governance asymmetric: narrow, freeze, revoke, preserve, and
  recover are available; silent authority expansion is not.

## Cross-Paper Synthesis and Tensions

- VIEA supplies the intent-to-effect loop; SCF turns its specialists, tools,
  routers, evaluators, and adapters into replaceable but non-self-authorizing
  capability boundaries.
- RMI and Benchmark Ratchets supply improvement pressure; SCF prevents the
  optimizer from changing the meaning, denominator, or authority of the field
  it is trying to improve.
- Cognitive Loop Closure compiles traces into tools; SCF provides the field,
  qualification, state, incident, and retirement boundary those tools need.
- VCM and QCSA preserve semantic context; SCF adds exact profile transfer,
  reliance invalidation, and authority at invocation time.
- Talos supplies execution artifacts; SCF adds route eligibility, effect
  ceilings, state solvency, and recovery reachability.
- The Platonic World Model extends SCF-style replacement to semantic forms and
  world-model commitments; DCC extends it to compiled neural capability
  objects. Neither eliminates SCF's evaluator and governance regress.

## Section-Family Coverage

- §§1–4: problem, contribution, formal ontology, qualification and lifecycle
  predicates → Stable Capability Fields and System Boundaries.
- §§5–6: contract classes/debt/firewall, refinement, field boundaries, state,
  adaptation → SCF, Replacement, Policy Optimization, Data Engines.
- §§7–8: evidence graph, invalidation, views, federation, routing → Artifact
  Graphs, Claim Ledgers, Routing, Inter-Stack Protocols.
- §§9–10: authority, effects, toxic composition, evaluators, independence,
  sealed evaluation → Security, Runtime, Verification, Benchmark Ratchets.
- §§11–14: transactional improvement, composition, institutional evolution,
  constitutional governance, TCB, bootstrap/recovery → RSI Boundaries,
  Readiness, Operations, Institutions, Integrated Architecture.
- §§15–16: threat model and conditional properties → Failure Modes, Security,
  Executable Specifications. Conditional arguments are not promoted to
  deployed guarantees.
- §§17–19 and appendices: reference design, cost, worked cases, empirical
  agenda, manifests, pseudocode, event sketches, overlap records, executable
  fragment → Prototype Roadmap and research obligations.
- §§20–22: ASI implications, open questions, conclusion → RSI Boundaries and
  Open Research Agenda.

## Open Questions

- Which SCF executable fragment should be ported into the book repo first?
- Which qualification and route records should be represented as JSON Schemas?
- How should the public book distinguish SCF's own reported executable fragment from proofs implemented in this repo?
