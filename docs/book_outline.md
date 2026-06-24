# Cohesive Book Outline

Working title: **The ASI Stack: A Systems Architecture for Governed, Efficient, Self-Improving AI**

Status: expanded source-of-truth drafting outline, updated 2026-06-24 after local Project Theseus and Circle Calculus mining. `book_structure.json` remains the ordering source of truth; Quarto generates displayed chapter numbers from the manifest.

## Drafting Thesis

The book argues that advanced AI should not be understood as one larger model, one agent loop, or one benchmark ladder. It should be specified as a governed stack whose layers transform intent into action through explicit boundaries: alignment, governance, planning, memory, reasoning, execution, routing, compression, evidence, and recursive self-improvement.

The stack is efficient because it routes work, compiles context, reuses artifacts, compresses representations, escalates only when needed, and records residual uncertainty. It is governable because each layer has an authority ceiling, an interface, an invariant set, a failure model, and an evidence record. It is self-improving only when replacement is bounded by stable capability fields, readiness gates, rollback paths, and evaluator integrity.

## How Future Writing Runs Should Use This Outline

- Use the part-level source queue to load broad context before drafting a part.
- Use the chapter-level source queue to load only the relevant papers for the chapter in scope.
- Treat primary sources as the first mining pass, supporting sources as synthesis/context, variants as version checks, and connector/recovery sources as blockers until actually loaded.
- Do not mark a claim `source-derived` until the actual source text has been read and a source note or equivalent mined record exists.
- Treat conversation-mined material as author intent, terminology, architecture lineage, deduplication help, and recovery guidance. It is not external evidence and should not be quoted verbatim unless explicitly approved.
- Treat local project mining from Theseus/Circle as source-discovery and architecture triage until a source note, proof build, or recorded test promotes the relevant claim boundary.
- Keep claim labels separate from support states. A chapter may contain `Design rationale + argument`, `Hypothesized + source-derived`, or `Measured + synthetic-test-backed` claims, but those dimensions should not be collapsed.
- Use drafting annotations in private notes when helpful: `[SOURCE]`, `[AUTHOR INTENT]`, `[SYNTHESIS]`, `[EXPERIMENT]`, and `[OPEN]`.
- Keep chapter IDs and filenames stable; Quarto handles displayed chapter numbering.

## Reader Promise

- Why ASI should be treated as a systems architecture, not a monolithic model.
- How each layer constrains the others without erasing its separate responsibilities.
- Which sources should be mined for each chapter and part.
- Which claims should become Lean proofs, executable specs, or tests.
- How a minimal implementation can grow from artifact graph to governed capability replacement.
- How the living book acts as an evidence ratchet instead of a static anthology.

## Book-Level Throughline

1. Define the stack, its boundaries, and why model scale alone is not an architecture.
2. Establish efficiency as governed selectivity across routing, compression, memory reuse, and verification effort.
3. Define the failure model and two-dimensional evidence discipline before making layer claims.
4. Specify the constitutional and governance substrate that bounds every layer.
5. Specify planning, memory, reasoning, and execution as separate operational layers.
6. Specify routing, compression, benchmarks, and self-improvement as governed growth mechanisms, including the seed/router/search/generator/verifier/residual loop.
7. Integrate the layers into a reference architecture, prototype roadmap, living workflow, and bibliography plan.

## Lean Proof Target Format

The outline is the source of truth for proof scope. Every chapter with a `Stable ID` must include a `Lean proof targets` table. These rows tell future drafting agents which claims should become executable Lean work, which module should contain them, and whether the target is only planned or already implemented.

| Field | Meaning |
|---|---|
| Tag | Stable proof identifier. Must start with `lean:` and remain stable across edits. |
| Lean module | Intended module under `lean/AsiStackProofs/`. |
| Formal target | The operational invariant, relation, transition rule, or schema property to formalize. |
| Status | `planned`, `scaffolded`, `implemented`, `blocked`, or `retired`. |

Rules: do not tag vague philosophical claims until they are operational predicates; do not describe a target as proven unless the Lean module exists and `lake build` passes; prefer small invariants over grand architecture theorems.

## Front Matter

### Landing Page

Purpose: give readers a current-state dashboard for the living book: thesis, architecture diagram, source/evidence status, warning labels, and links to matrices, schemas, tests, proof manifest, changelog, repository, and rendered site.

### Preface

Purpose: explain why the source papers are being synthesized into one architecture, how to read support states, how speculative material is labeled, and why Quarto/GitHub Pages make the book living.

### Author Intent and Architecture Lineage Appendix

Purpose: preserve public-safe author intent, terminology, deduplication decisions, and architecture lineage recovered from conversation-mined context while keeping that context separate from source-derived evidence.

## Part I - Foundations, Alignment, and Governance

Part job: Establish the first-principles frame: ASI as a governed stack, the efficiency hypothesis, the failure model, the evidence discipline, and the constitutional/governance substrate that bounds every later layer.

Part source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Core | `viea`, `scf`, `alignment_field`, `field_of_god`, `field_of_god_ai_constitution`, `ethica_mechanica`, `eternal_code`, `coherence_exchange`, `ladon_manhattan` | Load these before drafting or reorganizing this part. |
| Supporting | `beastbrain`, `beastbrain_timeless`, `aletheia`, `talos`, `spinoza`, `simulation_scaling` | Load these for lineage, variants, failure modes, and cross-layer synthesis. |
| Connector or recovery required | `moecot`, `vcm_editable` | Use Google Drive connector or mark blocked before source-derived claims. |

### ASI Is a Stack, Not a Model

Stable ID: `asi-is-a-stack-not-a-model`

Chapter job: The book needs a single architecture frame for advanced AI systems that must plan, remember, verify, act, route work, compress representations, and improve under governance.

Core claim: Efficient ASI should be modeled as a governed stack of cooperating layers rather than as one undifferentiated model.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `viea`, `beastbrain`, `aletheia` | Read first for chapter claims and mechanisms. |
| Supporting | `talos`, `moecot`, `scf` | Mine after primary sources for cross-layer connections, variants, and failure modes. |
| Connector or recovery required | `moecot` | Load via Google Drive connector or mark as blocked before source-derived claims. |

Draft arc:

- Problem: The book needs a single architecture frame for advanced AI systems that must plan, remember, verify, act, route work, compress representations, and improve under governance.
- Insufficiency: A larger model, a prompt wrapper, or an agent loop does not by itself define authority boundaries, memory discipline, evidence ledgers, tool permissions, or safe replacement rules.
- Mechanism: Define each layer by responsibility, interface, artifact, invariant, failure mode, evidence gate, and non-claim.
- Mechanism: Frame the raw LLM as a semantic-compression and generation component inside the larger governed system, not as the whole agent.
- Mechanism: Treat the whole book as a reference architecture rather than a collection of standalone papers.
- Mechanism: Use source queues and evidence states to keep future writing runs context-loaded and honest.
- Interface: Alignment and governance constrain every downstream layer.
- Interface: Planning, memory, reasoning, execution, routing, compression, and evidence exchange typed artifacts.
- Interface: Recursive improvement is a governed transition, not an ambient property of intelligence.

Primary invariants:

- Layer boundaries remain explicit.
- Claims carry support states.
- Reasoning ability never implies execution authority.

Failure modes to cover:

- Anthology drift.
- Monolith drift.
- Evidence inflation before source notes or tests exist.

Draft deliverables:

- A stack map, layer boundary record schema and fixture, source crosswalk, and claim ledger that make the architecture navigable before prose is complete.
- Planned Codex test: Layer-boundary audit.
- Planned Codex test: Source-to-layer traceability review.
- Planned Codex test: Claim-support label audit.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:stack.layer_boundaries.operational_invariant` | `AsiStackProofs.StackBoundaries` | A layer without external-action authority can only produce an action through an authorized handoff. | implemented |
| `lean:stack.layer_boundaries.failure_blocks_promotion` | `AsiStackProofs.StackBoundaries` | A handoff that exceeds the caller authority ceiling is rejected. | implemented |

### The Efficient ASI Hypothesis

Stable ID: `the-efficient-asi-hypothesis`

Chapter job: The architecture needs a non-scale-only theory for how capability can increase without using maximal cognition for every subtask.

Core claim: Capability improves when cognition is routed, compressed, reused, governed, and tested with visible residuals.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `viea`, `rmi`, `cgs` | Read first for chapter claims and mechanisms. |
| Supporting | `rankfold_neuralfold`, `bbvca_v9`, `simulation_scaling`, `beastbrain`, `beastbrain_timeless`, `aletheia` | Mine after primary sources for cross-layer connections, variants, and failure modes. |
| Connector or recovery required | `moecot` | Load via Google Drive connector or mark as blocked before source-derived claims. |

Draft arc:

- Problem: The architecture needs a non-scale-only theory for how capability can increase without using maximal cognition for every subtask.
- Insufficiency: Parameter count alone does not explain routing, context selectivity, procedural memory, compression, runtime targeting, or verification effort.
- Mechanism: Use minimum viable intelligence for subtasks.
- Mechanism: Turn repeated cognition into durable artifacts, tools, or procedural memory.
- Mechanism: Model efficiency through the seed/router/search/generator/verifier/residual loop plus memory and governance.
- Mechanism: Expose residual burden when routing or compression is incomplete.
- Interface: Planning requests capability profiles.
- Interface: Routing selects specialists.
- Interface: Evidence decides whether efficiency claims survived quality and cost tests.

Primary invariants:

- Efficiency claims include quality and cost.
- Compression exposes residuals.
- Fallback routes remain available.

Failure modes to cover:

- Cheap inference mistaken for intelligence.
- Critical context compressed away.
- Benchmark gains that increase hidden residual burden.

Draft deliverables:

- A costed route ledger with quality predicates, residual accounting, and fallback criteria.
- Planned Codex test: Minimum viable route test.
- Planned Codex test: Residual burden accounting test.
- Planned Codex test: Utility-preserving compression test.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:efficiency.minimum_viable.operational_invariant` | `AsiStackProofs.Efficiency` | A route is minimum viable only when no lower-cost authorized route satisfies the required quality predicate. | planned |
| `lean:efficiency.minimum_viable.failure_blocks_promotion` | `AsiStackProofs.Efficiency` | A routed or compressed result with open obligations cannot be promoted without a residual record. | planned |

### System Boundaries and Authority

Stable ID: `system-boundaries-and-authority`

Chapter job: The stack needs a formal vocabulary for boundaries, authority ceilings, permissions, and handoffs before any layer can be made safe or testable.

Core claim: Authority should be modeled as a typed, bounded capability attached to layers, fields, tools, artifacts, and principals.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `viea`, `scf` | Read first for chapter claims and mechanisms. |
| Supporting | `talos`, `ladon_manhattan`, `genesiscode` | Mine after primary sources for cross-layer connections, variants, and failure modes. |
| Connector or recovery required | `moecot` | Load via Google Drive connector or mark as blocked before source-derived claims. |

Draft arc:

- Problem: The stack needs a formal vocabulary for boundaries, authority ceilings, permissions, and handoffs before any layer can be made safe or testable.
- Insufficiency: Informal ownership boundaries let planning authority, memory access, tool use, and deployment authority blur into each other.
- Mechanism: Define principals, authorities, ceilings, grants, revocations, and handoff contracts.
- Mechanism: Separate knowledge access from action authority.
- Mechanism: Represent missing authority as a detectable failure rather than implicit permission.
- Interface: Governance issues ceilings.
- Interface: Execution checks permissions.
- Interface: Evidence records authority-related failures.

Primary invariants:

- Authority never expands silently.
- Read permission is not write permission.
- Tool execution requires an explicit grant.

Failure modes to cover:

- Authority creep.
- Confused-deputy tool calls.
- Memory access treated as action approval.

Draft deliverables:

- A small authority schema and transition table used by chapter examples and future Lean proofs.
- Planned Codex test: Authority ceiling preservation test.
- Planned Codex test: Permission separation test.
- Planned Codex test: Confused-deputy scenario.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:authority.ceiling.operational_invariant` | `AsiStackProofs.Authority` | Every transition preserves or lowers the active authority ceiling unless a governance grant is present. | implemented |
| `lean:authority.ceiling.failure_blocks_promotion` | `AsiStackProofs.Authority` | A missing grant blocks execution rather than becoming default authorization. | implemented |

### Failure Modes of Ungoverned Intelligence

Stable ID: `failure-modes-of-ungoverned-intelligence`

Chapter job: The book needs an explicit failure model before it can make governance, reliability, or self-improvement claims.

Core claim: Ungoverned intelligence fails through stack-level breakdowns before dramatic catastrophic scenarios are needed.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `scf`, `vcm_public`, `talos` | Read first for chapter claims and mechanisms. |
| Supporting | `spinoza`, `field_of_god`, `viea`, `simulation_scaling` | Mine after primary sources for cross-layer connections, variants, and failure modes. |
| Connector or recovery required | `vcm_editable`, `moecot` | Load via Google Drive connector or mark as blocked before source-derived claims. |

Draft arc:

- Problem: The book needs an explicit failure model before it can make governance, reliability, or self-improvement claims.
- Insufficiency: High-level safety language misses earlier engineering failures such as goal misbinding, context pollution, evaluator drift, authority creep, tool overreach, and residual hiding.
- Mechanism: Classify failures by layer.
- Mechanism: Map every failure to an invariant and a planned falsification test.
- Mechanism: Use failures to motivate boundaries in later chapters.
- Interface: Governance limits authority creep.
- Interface: VCM limits context pollution.
- Interface: Verification limits false certainty.
- Interface: Execution limits side effects.

Primary invariants:

- Every risk maps to at least one boundary.
- Evaluator integrity is protected.
- Negative evidence stays visible.

Failure modes to cover:

- Evaluator capture.
- Memory poisoning.
- Tool/action overreach.
- Compression that hides residual complexity.

Draft deliverables:

- A layered failure taxonomy tied to invariants, source queues, and future tests.
- Planned Codex test: Authority creep scenario.
- Planned Codex test: Context pollution scenario.
- Planned Codex test: Evaluator drift scenario.
- Planned Codex test: Unverified-claim scenario.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:failure.invariant_violation.operational_invariant` | `AsiStackProofs.FailureModes` | A component with a failed required invariant cannot be promoted. | implemented |
| `lean:failure.invariant_violation.failure_blocks_promotion` | `AsiStackProofs.FailureModes` | An unbounded authority field is detected as a governance failure. | implemented |

### Evidence States and Claim Discipline

Stable ID: `evidence-states-and-claim-discipline`

Chapter job: The living book needs a shared language for what kind of claim is being made and what currently supports it.

Core claim: Every major claim should carry both a claim label and a support state, and it should move only when source ingestion, prototype inspection, or actual tests justify the transition.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `benchmaxxing`, `spinoza`, `viea` | Read first for chapter claims and mechanisms. |
| Supporting | `uat`, `coherence_exchange`, `verification_bandwidth` | Mine after primary sources for cross-layer connections, variants, and failure modes. |

Draft arc:

- Problem: The living book needs a shared language for what kind of claim is being made and what currently supports it.
- Insufficiency: Without explicit support states, conceptual architecture prose can accidentally read like empirical proof.
- Mechanism: Use Appendix C as the claim ledger.
- Mechanism: Separate claim label from support state with evidence transition records so design rationales, hypotheses, measurements, mechanisms, and speculative claims are not collapsed.
- Mechanism: Require source notes before promoting claims to source-derived.
- Mechanism: Require evidence bundles, including negative or inconclusive results, before promoting test-backed labels.
- Interface: Drafting updates claims.
- Interface: Experiments update evidence.
- Interface: Changelog records evidence movement.

Primary invariants:

- No fabricated source support.
- No fabricated test results.
- Negative and inconclusive results remain visible.

Failure modes to cover:

- Support-state inflation.
- Citation laundering.
- Silent removal of failed claims.

Draft deliverables:

- A claim record schema, evidence transition record schema, claim-label table, support-state transition table, evidence-bundle template, and validation check.
- Planned Codex test: Support-state transition test.
- Planned Codex test: Claim ledger completeness test.
- Planned Codex test: Evidence bundle completeness test.
- Planned Codex test: Changelog consistency audit.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:evidence.support_state.operational_invariant` | `AsiStackProofs.EvidenceStates` | Support-state transitions require the corresponding evidence artifact. | implemented |
| `lean:evidence.support_state.failure_blocks_promotion` | `AsiStackProofs.EvidenceStates` | A claim cannot be promoted when required evidence is absent. | implemented |

### Human Intent as a Formal Input

Stable ID: `human-intent-as-a-formal-input`

Chapter job: A governed stack must start from human intent without letting natural-language ambiguity become unrestricted execution authority.

Core claim: Human intent should enter the stack as a structured contract with goals, constraints, authority, artifacts, evidence requirements, and stop conditions.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `viea` | Read first for chapter claims and mechanisms. |
| Supporting | `software_magic_grimoire`, `planforge`, `cognitive_compilation`, `talos` | Mine after primary sources for cross-layer connections, variants, and failure modes. |

Draft arc:

- Problem: A governed stack must start from human intent without letting natural-language ambiguity become unrestricted execution authority.
- Insufficiency: Prompt-only workflows blur request, requirements, permission, risk tolerance, and acceptance criteria.
- Mechanism: Parse intent into command contracts.
- Mechanism: Separate desired outcome from allowed means.
- Mechanism: Attach acceptance criteria and escalation conditions.
- Interface: Alignment filters intent.
- Interface: Planning compiles accepted contracts.
- Interface: Execution consumes only authorized task contracts.

Primary invariants:

- Ambiguity triggers clarification or bounded defaults.
- Intent contracts expose authority limits.
- Stop conditions remain attached to the plan.

Failure modes to cover:

- Goal misbinding.
- Scope creep.
- Implicit permission to act.

Draft deliverables:

- An intent-contract schema and example transformations from request to governed task.
- Planned Codex test: Intent parsing ambiguity test.
- Planned Codex test: Authority extraction test.
- Planned Codex test: Stop-condition preservation test.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:intent.contract.operational_invariant` | `AsiStackProofs.IntentContracts` | A compiled intent contract preserves declared constraints and stop conditions. | planned |
| `lean:intent.contract.failure_blocks_promotion` | `AsiStackProofs.IntentContracts` | A contract missing required authority cannot compile to an executable job. | planned |

### Constitutional Alignment Substrate

Stable ID: `constitutional-alignment-substrate`

Chapter job: The stack needs a normative substrate that constrains goals, plans, execution, and self-modification.

Core claim: Alignment should function as a constitutional substrate whose commitments are operationalized as constraints on plans and system changes.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `alignment_field`, `field_of_god`, `ethica_mechanica`, `eternal_code` | Read first for chapter claims and mechanisms. |
| Supporting | `coherence_exchange`, `spinoza`, `field_of_god_ai_constitution` | Mine after primary sources for cross-layer connections, variants, and failure modes. |

Draft arc:

- Problem: The stack needs a normative substrate that constrains goals, plans, execution, and self-modification.
- Insufficiency: Reactive refusal policies do not define value continuity, moral uncertainty, agency preservation, anti-domination, or self-modification ethics.
- Mechanism: Translate philosophical commitments into operational predicates where possible.
- Mechanism: Keep metaphysical claims labeled as interpretation unless separately supported.
- Mechanism: Attach constitutional constraints to planning and replacement gates.
- Interface: Planning receives admissible-goal constraints.
- Interface: Governance receives protected constraints.
- Interface: Verification checks whether normative claims exceed evidence.

Primary invariants:

- Dignity and agency constraints remain visible.
- Corrigibility cannot be optimized away.
- Speculative metaphysics stays labeled.

Failure modes to cover:

- Mystical framing replacing technical constraints.
- Power without care.
- Self-modification weakening protected commitments.

Draft deliverables:

- A compact constitution with operational predicates, open moral uncertainties, and scenario tests.
- Planned Codex test: Constitutional consistency test.
- Planned Codex test: Self-modification ethics scenario.
- Planned Codex test: Power-without-care scenario.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:alignment.constitution.operational_invariant` | `AsiStackProofs.Alignment` | An admitted plan satisfies every active constitutional predicate. | planned |
| `lean:alignment.constitution.failure_blocks_promotion` | `AsiStackProofs.Alignment` | A self-modification that weakens a protected predicate is rejected. | planned |

### Agency, Dignity, and Corrigibility

Stable ID: `agency-dignity-and-corrigibility`

Chapter job: The book needs a precise account of how human agency and dignity constrain powerful optimization.

Core claim: A governed ASI stack should preserve human agency, dignity, corrigibility, and contestability as engineering requirements.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `alignment_field`, `ethica_mechanica` | Read first for chapter claims and mechanisms. |
| Supporting | `field_of_god`, `eternal_code`, `coherence_exchange`, `field_of_god_ai_constitution` | Mine after primary sources for cross-layer connections, variants, and failure modes. |

Draft arc:

- Problem: The book needs a precise account of how human agency and dignity constrain powerful optimization.
- Insufficiency: Safety framed only as harm avoidance can miss domination, lock-in, coercive dependence, and loss of meaningful user control.
- Mechanism: Represent agency constraints as limits on delegation and manipulation.
- Mechanism: Define corrigibility as preserved update and shutdown pathways.
- Mechanism: Use contestability and audit rights as governance mechanisms.
- Interface: Alignment defines agency predicates.
- Interface: Governance enforces rights.
- Interface: Execution requires approvals for irreversible effects.

Primary invariants:

- Users retain meaningful refusal and review channels.
- Delegation does not erase accountability.
- Irreversible actions require stronger authorization.

Failure modes to cover:

- Dependency lock-in.
- Covert manipulation.
- Corrigibility collapse.

Draft deliverables:

- A rights-and-corrigibility checklist attached to high-impact plans.
- Planned Codex test: Agency-preservation scenario.
- Planned Codex test: Corrigibility pathway test.
- Planned Codex test: High-impact approval test.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:corrigibility.agency.operational_invariant` | `AsiStackProofs.Corrigibility` | Protected agency rights remain available after an accepted transition. | planned |
| `lean:corrigibility.agency.failure_blocks_promotion` | `AsiStackProofs.Corrigibility` | A transition that removes a required correction pathway is rejected. | planned |

### Moral Uncertainty and Value Conflict

Stable ID: `moral-uncertainty-and-value-conflict`

Chapter job: A self-improving system will face value conflicts that cannot be honestly collapsed into one scalar objective.

Core claim: Value conflicts should be represented as explicit unresolved obligations, review paths, and bounded decisions rather than hidden inside reward functions.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `ethica_mechanica`, `alignment_field` | Read first for chapter claims and mechanisms. |
| Supporting | `coherence_exchange`, `uat`, `spinoza`, `field_of_god_ai_constitution` | Mine after primary sources for cross-layer connections, variants, and failure modes. |

Draft arc:

- Problem: A self-improving system will face value conflicts that cannot be honestly collapsed into one scalar objective.
- Insufficiency: Single-objective optimization hides moral uncertainty and encourages premature resolution of contested values.
- Mechanism: Classify conflicts by value type, stakeholder, reversibility, and evidence requirement.
- Mechanism: Escalate unresolved conflicts to tribunal or human review.
- Mechanism: Record decisions and residual moral uncertainty.
- Interface: Alignment produces conflict records.
- Interface: Planning uses conflict constraints.
- Interface: Evidence records review outcomes.

Primary invariants:

- Unresolved conflicts remain visible.
- High-stakes conflicts require stronger review.
- Speculative moral theory cannot silently authorize action.

Failure modes to cover:

- Value flattening.
- False consensus.
- Review theater without decision records.

Draft deliverables:

- A value-conflict record schema and scenario library.
- Planned Codex test: Value conflict classification test.
- Planned Codex test: Review escalation test.
- Planned Codex test: Residual uncertainty preservation test.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:values.conflict.operational_invariant` | `AsiStackProofs.ValueConflict` | A decision with unresolved protected conflicts carries a residual conflict record. | planned |
| `lean:values.conflict.failure_blocks_promotion` | `AsiStackProofs.ValueConflict` | A high-stakes conflict cannot bypass the required review predicate. | planned |

### Governance Rights: Fork, Exit, and Audit

Stable ID: `governance-rights-fork-exit-and-audit`

Chapter job: Powerful AI infrastructure needs rights and mechanisms that prevent governance lock-in and hidden control.

Core claim: Fork, exit, audit, dissent, and contestability should be treated as technical governance interfaces, not only political ideals.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `ethica_mechanica`, `coherence_exchange` | Read first for chapter claims and mechanisms. |
| Supporting | `alignment_field`, `ladon_manhattan`, `spinoza`, `uat`, `field_of_god_ai_constitution` | Mine after primary sources for cross-layer connections, variants, and failure modes. |

Draft arc:

- Problem: Powerful AI infrastructure needs rights and mechanisms that prevent governance lock-in and hidden control.
- Insufficiency: Policy statements about transparency are weak if users cannot audit, contest, exit, or fork the system in practice.
- Mechanism: Represent rights as capabilities and required interfaces.
- Mechanism: Attach audit artifacts to governance decisions.
- Mechanism: Treat fork/exit as preserved escape hatches against lock-in.
- Interface: Governance issues rights.
- Interface: SCFs preserve rights across replacement.
- Interface: Execution logs evidence for audit.

Primary invariants:

- Audit records cannot be silently deleted.
- Exit paths remain materially usable.
- Fork rights do not bypass safety constraints.

Failure modes to cover:

- Governance capture.
- Data hostage-taking.
- Opaque automated policy updates.

Draft deliverables:

- A governance-rights table with required artifacts, authorities, and failure tests.
- Planned Codex test: Audit-record availability test.
- Planned Codex test: Exit-path preservation test.
- Planned Codex test: Fork-right safety test.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:governance.rights.operational_invariant` | `AsiStackProofs.GovernanceRights` | A governance transition preserves required audit and exit capabilities. | planned |
| `lean:governance.rights.failure_blocks_promotion` | `AsiStackProofs.GovernanceRights` | A transition that removes a protected right is rejected or marked invalid. | planned |

### Stable Capability Fields

Stable ID: `stable-capability-fields`

Chapter job: The stack needs stable semantic boundaries so implementations can improve without changing what a capability means.

Core claim: A stable capability field is a governed boundary with identity, interface, authority ceiling, qualification evidence, and rollback policy.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `scf` | Read first for chapter claims and mechanisms. |
| Supporting | `viea`, `talos`, `ladon_manhattan` | Mine after primary sources for cross-layer connections, variants, and failure modes. |
| Connector or recovery required | `moecot` | Load via Google Drive connector or mark as blocked before source-derived claims. |

Draft arc:

- Problem: The stack needs stable semantic boundaries so implementations can improve without changing what a capability means.
- Insufficiency: Plugin replacement and model swapping do not define identity, authority, qualification evidence, or rollback semantics.
- Mechanism: Separate field identity from implementation.
- Mechanism: Bind qualification claims to exact artifacts.
- Mechanism: Represent lifecycle states such as shadow, canary, qualified, default, deprecated, and retired.
- Mechanism: Attach qualification context such as epoch, domain, risk budget, hardware, authority tier, and benchmark state.
- Mechanism: Require route validity and evaluator integrity before promotion.
- Interface: Planning requests field capabilities.
- Interface: Execution invokes authorized routes.
- Interface: Evidence records qualification and regression results.

Primary invariants:

- Replacement cannot expand authority by default.
- Evaluator integrity is protected.
- Qualification context is explicit and time-bound.
- Rollback remains available after failed mutation.

Failure modes to cover:

- Field identity drift.
- Evaluator capture.
- Authority expansion during replacement.

Draft deliverables:

- An SCF record schema with field identity, implementation versions, lifecycle state, qualification context, evidence, route validity, migration path, and rollback metadata.
- Planned Codex test: Qualification predicate test.
- Planned Codex test: Route validity test.
- Planned Codex test: Authority non-escalation test.
- Planned Codex test: Rollback readiness test.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:scf.field_identity.operational_invariant` | `AsiStackProofs.StableCapabilityFields` | An implementation can replace another only if it satisfies the field qualification predicate. | implemented |
| `lean:scf.field_identity.failure_blocks_promotion` | `AsiStackProofs.StableCapabilityFields` | A replacement that expands authority without a governance grant is rejected. | implemented |

### Capability Replacement and Rollback

Stable ID: `capability-replacement-and-rollback`

Chapter job: Recursive improvement requires a safe procedure for replacing components while preserving identity, regression history, and recovery paths.

Core claim: Capability replacement should be an evidence-gated transaction with preconditions, regression checks, residual records, and rollback.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `scf`, `rmi`, `benchmaxxing` | Read first for chapter claims and mechanisms. |
| Supporting | `cognitive_loop_closure`, `talos` | Mine after primary sources for cross-layer connections, variants, and failure modes. |
| Connector or recovery required | `moecot` | Load via Google Drive connector or mark as blocked before source-derived claims. |

Draft arc:

- Problem: Recursive improvement requires a safe procedure for replacing components while preserving identity, regression history, and recovery paths.
- Insufficiency: Ad hoc upgrades make it hard to know whether a system improved, drifted, lost a regression, or captured its evaluator.
- Mechanism: Define replacement proposals as artifacts.
- Mechanism: Run qualification, regression, and authority checks.
- Mechanism: Commit only after evidence gates pass and rollback remains available.
- Interface: SCF defines the field.
- Interface: Benchmarks test behavior.
- Interface: Evidence and changelog record the transition.

Primary invariants:

- No replacement without prior and posterior artifacts.
- Regressions stay attached.
- Rollback metadata is required before promotion.

Failure modes to cover:

- Regression deletion.
- Rollback impossible after deployment.
- Self-judged replacement.

Draft deliverables:

- A replacement transaction schema with precheck, gate, commit, monitor, and rollback phases.
- Planned Codex test: Replacement transaction test.
- Planned Codex test: Regression preservation test.
- Planned Codex test: Rollback execution dry run.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:replacement.transaction.operational_invariant` | `AsiStackProofs.Replacement` | A replacement commit requires qualification evidence and rollback metadata. | implemented |
| `lean:replacement.transaction.failure_blocks_promotion` | `AsiStackProofs.Replacement` | A failed regression blocks promotion of the replacement. | implemented |

### Security Kernel and Digital SCIFs

Stable ID: `security-kernel-and-digital-scifs`

Chapter job: High-agency systems need security boundaries for secrets, context, permissions, and tool calls.

Core claim: Sensitive context and privileged actions should be mediated by kernel-like security mechanisms and compartmentalized Digital SCIFs.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `ladon_manhattan`, `context_engineer` | Read first for chapter claims and mechanisms. |
| Supporting | `talos`, `alignment_field`, `coherence_exchange` | Mine after primary sources for cross-layer connections, variants, and failure modes. |

Draft arc:

- Problem: High-agency systems need security boundaries for secrets, context, permissions, and tool calls.
- Insufficiency: Putting secrets or privileged context into model-visible text invites leakage, prompt injection, and authority confusion.
- Mechanism: Use handles rather than exposing secrets.
- Mechanism: Separate model-visible context from privileged substitution.
- Mechanism: Run high-risk tasks inside compartmentalized context containers.
- Interface: VCM supplies least-privilege context.
- Interface: Execution checks tool permissions.
- Interface: Governance audits sensitive transitions.

Primary invariants:

- Secrets are not directly model-visible.
- SCIF context is purpose-limited.
- Privilege substitution is auditable.

Failure modes to cover:

- Prompt injection extracting secrets.
- Privilege leakage through summaries.
- SCIF bypass.

Draft deliverables:

- A secure-handle workflow and SCIF lifecycle diagram.
- Planned Codex test: Secret-handle substitution test.
- Planned Codex test: SCIF least-privilege test.
- Planned Codex test: Prompt-injection containment scenario.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:security.scif.operational_invariant` | `AsiStackProofs.SecurityKernel` | A secret handle can be substituted only inside an authorized execution boundary. | implemented |
| `lean:security.scif.failure_blocks_promotion` | `AsiStackProofs.SecurityKernel` | A context packet with insufficient clearance cannot enter a protected SCIF. | implemented |

### Recursive Self-Improvement Boundaries

Stable ID: `recursive-self-improvement-boundaries`

Chapter job: The book needs to state when self-improvement is allowed, what it may modify, and which invariants it cannot weaken.

Core claim: Recursive self-improvement is allowed only as a bounded, evidence-gated, reversible transition over stable capability fields.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `scf`, `benchmaxxing`, `rmi` | Read first for chapter claims and mechanisms. |
| Supporting | `alignment_field`, `viea`, `talos`, `field_of_god_ai_constitution`, `theseus_self_evolution_system`, `theseus_architecture_gate` | Mine after primary sources for cross-layer connections, variants, and failure modes. |
| Connector or recovery required | `moecot` | Load via Google Drive connector or mark as blocked before source-derived claims. |

Draft arc:

- Problem: The book needs to state when self-improvement is allowed, what it may modify, and which invariants it cannot weaken.
- Insufficiency: Treating self-improvement as automatic capability growth ignores evaluator integrity, constitutional preservation, authority ceilings, and regression memory.
- Mechanism: Define improvement proposals, protected invariants, and evidence gates.
- Mechanism: Separate proposing, evaluating, approving, committing, and monitoring.
- Mechanism: Delay autonomous replacement until evaluators and governance are credible.
- Interface: SCFs define replaceable units.
- Interface: Evidence ratchets provide gates.
- Interface: Alignment supplies protected constraints.

Primary invariants:

- Self-improvement cannot weaken protected invariants.
- Evaluator independence is required.
- Every accepted change remains auditable.

Failure modes to cover:

- Recursive evaluator capture.
- Constitutional weakening.
- Irreversible flawed upgrades.

Draft deliverables:

- A self-improvement protocol that can reject, quarantine, roll back, or retire a proposed change.
- Planned Codex test: Protected-invariant preservation test.
- Planned Codex test: Evaluator independence test.
- Planned Codex test: Self-improvement rollback scenario.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:self_improvement.boundary.operational_invariant` | `AsiStackProofs.SelfImprovement` | An improvement transition preserves all protected invariants. | planned |
| `lean:self_improvement.boundary.failure_blocks_promotion` | `AsiStackProofs.SelfImprovement` | A proposal evaluated only by the component being replaced cannot be promoted. | planned |

## Part II - Planning, Memory, Reasoning, and Execution

Part job: Specify the operational middle of the stack: intent contracts, planning/control, semantic compilation, memory/context, verification, tribunals, typed work, artifact production, runtime adapters, procedural memory, audit, and replay.

Part source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Core | `viea`, `planforge`, `planforge_compiler_arch`, `cognitive_compilation`, `vcm_public`, `spinoza`, `uat`, `talos`, `genesiscode`, `cognitive_loop_closure` | Load these before drafting or reorganizing this part. |
| Supporting | `software_magic_grimoire`, `context_engineer`, `black_hole_context_manager`, `verification_bandwidth`, `treellm`, `spinoza_composer`, `ladon_manhattan`, `theseus_operator_os` | Load these for lineage, variants, failure modes, and cross-layer synthesis. |
| Connector or recovery required | `vcm_editable`, `moecot`, `talos_md` | Use Google Drive connector or mark blocked before source-derived claims. |

### Intent-to-Execution Contracts

Stable ID: `intent-to-execution-contracts`

Chapter job: Human goals need a typed path into execution that preserves requirements, artifacts, verification, deployment, and feedback.

Core claim: The stack should transform intent into execution contracts before any tool or runtime action occurs.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `viea` | Read first for chapter claims and mechanisms. |
| Supporting | `talos`, `software_magic_grimoire`, `genesiscode` | Mine after primary sources for cross-layer connections, variants, and failure modes. |
| Connector or recovery required | `moecot` | Load via Google Drive connector or mark as blocked before source-derived claims. |

Draft arc:

- Problem: Human goals need a typed path into execution that preserves requirements, artifacts, verification, deployment, and feedback.
- Insufficiency: A model response is not an execution contract; it lacks lifecycle, acceptance, artifact identity, and side-effect control.
- Mechanism: Represent command contracts with inputs, constraints, artifacts, tools, evidence, approvals, and feedback.
- Mechanism: Route contracts through planning, memory, verification, and execution layers.
- Mechanism: Attach result artifacts back to the claim and evidence ledger.
- Interface: Intent contracts feed planning.
- Interface: Execution consumes typed jobs derived from contracts.
- Interface: Evidence records contract satisfaction.

Primary invariants:

- Contract constraints survive compilation.
- Side effects require explicit execution authority.
- Artifacts remain linked to source intent.

Failure modes to cover:

- Response mistaken for completed work.
- Artifact identity lost.
- Approval bypass.

Draft deliverables:

- A command-contract schema and one end-to-end intent-to-artifact trace.
- Implemented protocol validation: `command_contract` and `intent_execution_trace` fixtures validate public record shape only.
- Planned Codex test: Contract field completeness test.
- Planned Codex test: Constraint preservation test.
- Planned Codex test: Artifact traceability test.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:intent_execution.contracts.operational_invariant` | `AsiStackProofs.IntentToExecution` | A compiled execution job preserves the parent contract constraints. | planned |
| `lean:intent_execution.contracts.failure_blocks_promotion` | `AsiStackProofs.IntentToExecution` | An execution job without required approval cannot transition to running. | planned |

### Command Contracts and Semantic Interfaces

Stable ID: `command-contracts-and-semantic-interfaces`

Chapter job: The stack needs compact command language that is expressive enough for AI cooperation and precise enough for validation.

Core claim: Command contracts should use explicit semantic interfaces for objective, context, constraints, procedure, output, verification, and failure behavior.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `software_magic_grimoire`, `viea` | Read first for chapter claims and mechanisms. |
| Supporting | `genesiscode`, `cognitive_compilation`, `talos` | Mine after primary sources for cross-layer connections, variants, and failure modes. |

Draft arc:

- Problem: The stack needs compact command language that is expressive enough for AI cooperation and precise enough for validation.
- Insufficiency: Prompt prose often hides objectives, constraints, output contracts, and failure behavior in unstructured language.
- Mechanism: Turn recurring command patterns into reusable templates.
- Mechanism: Treat software words as coordination primitives.
- Mechanism: Bind semantic interfaces to schemas and tests.
- Interface: Planning consumes structured commands.
- Interface: Execution enforces output contracts.
- Interface: Verification checks stated failure behavior.

Primary invariants:

- A command exposes output and verification requirements.
- Failure behavior is declared.
- Implicit instructions do not override explicit constraints.

Failure modes to cover:

- Semantic ambiguity.
- Prompt injection through context.
- Unspecified output contract.

Draft deliverables:

- A canonical command-contract template used by future chapter drafting and experiment prompts.
- Implemented protocol validation: `command_contract` fixture validates public record shape only.
- Planned Codex test: Command schema validation test.
- Planned Codex test: Failure-behavior declaration test.
- Planned Codex test: Prompt override scenario.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:command.semantic_interface.operational_invariant` | `AsiStackProofs.CommandContracts` | A valid command contract contains objective, constraints, output contract, verification, and failure behavior. | planned |
| `lean:command.semantic_interface.failure_blocks_promotion` | `AsiStackProofs.CommandContracts` | A hidden or conflicting instruction cannot override an explicit contract constraint. | planned |

### Planning as a Control Layer

Stable ID: `planning-as-a-control-layer`

Chapter job: Goals need to become governed plans with dependencies, budgets, risk limits, tool choices, and stopping conditions.

Core claim: Planning is a separate control layer that converts accepted goals into governed action without owning memory, reasoning, or side effects.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `planforge`, `viea` | Read first for chapter claims and mechanisms. |
| Supporting | `cognitive_compilation`, `software_magic_grimoire` | Mine after primary sources for cross-layer connections, variants, and failure modes. |
| Connector or recovery required | `moecot` | Load via Google Drive connector or mark as blocked before source-derived claims. |

Draft arc:

- Problem: Goals need to become governed plans with dependencies, budgets, risk limits, tool choices, and stopping conditions.
- Insufficiency: Planning cannot be collapsed into memory, reasoning, or execution because each layer has different authority and failure modes.
- Mechanism: Compile goals into strategic, tactical, and runtime plans.
- Mechanism: Represent assumptions, task graph, dependency graph, required context, required tools, worker requirements, authority requirements, risk budget, compute budget, verification plan, replanning policy, stopping conditions, and failure behavior.
- Mechanism: Delegate execution through typed contracts.
- Interface: Alignment filters goals.
- Interface: VCM supplies context packets.
- Interface: Routing selects specialists.
- Interface: Execution runs typed jobs.

Primary invariants:

- Plans expose constraints and stop conditions.
- Runtime replanning preserves authority limits.
- Tool selection is justified by task requirements.

Failure modes to cover:

- Scope creep.
- Planning without replanning.
- Tool choice exceeds authority or budget.

Draft deliverables:

- A plan graph format with dependencies, context requests, risk budgets, and stop conditions.
- Implemented protocol validation: `plan_graph` fixture validates public record shape only.
- Planned Codex test: Decomposition accuracy test.
- Planned Codex test: Dependency ordering test.
- Planned Codex test: Context-demand prediction test.
- Planned Codex test: Runtime replanning test.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:planning.control_layer.operational_invariant` | `AsiStackProofs.Planning` | A plan node inherits the authority ceiling of its parent contract unless governance lowers it. | implemented |
| `lean:planning.control_layer.failure_blocks_promotion` | `AsiStackProofs.Planning` | A plan with unsatisfied required constraints cannot be dispatched. | implemented |

### PlanForge DAGs and Intelligence Arbitrage

Stable ID: `planforge-dags-and-intelligence-arbitrage`

Chapter job: Large tasks require decomposition, scheduling, tiered model selection, and cost-aware routing.

Core claim: PlanForge-style DAG planning can support intelligence arbitrage by assigning each node the minimum adequate capability and verification burden.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `planforge`, `planforge_compiler_arch` | Read first for chapter claims and mechanisms. |
| Supporting | `coherence_exchange`, `cognitive_compilation`, `tokenmana` | Mine after primary sources for cross-layer connections, variants, and failure modes. |
| Connector or recovery required | `moecot` | Load via Google Drive connector or mark as blocked before source-derived claims. |

Draft arc:

- Problem: Large tasks require decomposition, scheduling, tiered model selection, and cost-aware routing.
- Insufficiency: Uniformly applying the strongest model to every task wastes compute and can obscure which tasks require verification or escalation.
- Mechanism: Decompose goals into DAGs.
- Mechanism: Annotate nodes with capability tier, budget, context request, risk, and verification requirement.
- Mechanism: Merge redundant branches and escalate only when predicates fail.
- Interface: Routing consumes capability annotations.
- Interface: VCM consumes context requests.
- Interface: Evidence records cost/quality results.

Primary invariants:

- Dependency order is respected.
- Cost savings do not remove required verification.
- Escalation paths are explicit.

Failure modes to cover:

- Wrong tier selection.
- Dependency cycles.
- Economic optimization overriding safety.

Draft deliverables:

- A DAG schema with node-level capability and verification annotations.
- Implemented protocol validation: `planforge_dag` fixture validates public record shape only.
- Implemented Lean proof target: a dispatchable finite indexed plan-graph record carries an acyclicity certificate and ordered member dependency edges.
- Planned Codex test: Capability tier assignment test.
- Implemented Lean proof target: a failed quality predicate routes to escalation or residual under the valid node-outcome predicate.
- Planned Codex test: deployed scheduler cycle rejection.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:planforge.dag.operational_invariant` | `AsiStackProofs.PlanForge` | A dispatchable plan graph is acyclic and all dependencies precede dependents. | implemented |
| `lean:planforge.dag.failure_blocks_promotion` | `AsiStackProofs.PlanForge` | A node whose quality predicate fails must escalate or emit a residual. | implemented |

### Cognitive Compilation and Semantic IR

Stable ID: `cognitive-compilation-and-semantic-ir`

Chapter job: LLM workflows need intermediate representations that separate requirements, plans, artifacts, repairs, and target runtimes.

Core claim: Cognitive compilation should transform goals into semantic intermediate representations that can be optimized, verified, repaired, and targeted.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `cognitive_compilation` | Read first for chapter claims and mechanisms. |
| Supporting | `planforge_compiler_arch`, `genesiscode`, `treellm`, `viea` | Mine after primary sources for cross-layer connections, variants, and failure modes. |

Draft arc:

- Problem: LLM workflows need intermediate representations that separate requirements, plans, artifacts, repairs, and target runtimes.
- Insufficiency: Generate-from-prompt workflows entangle requirements and implementation, drift over long contexts, and make incremental repair fragile.
- Mechanism: Represent requirements, semantics, dependencies, artifacts, and target constraints explicitly.
- Mechanism: Perform incremental repair over IR rather than re-prompting from scratch.
- Mechanism: Compile IR into jobs, code, schemas, or documents.
- Interface: Planning produces or consumes IR.
- Interface: Execution receives target-specific artifacts.
- Interface: Verification checks IR-to-output preservation.

Primary invariants:

- IR preserves declared requirements.
- Repair changes are localized and auditable.
- Target compilation records assumptions.

Failure modes to cover:

- IR drift.
- Compiler hallucination.
- Repair that breaks earlier requirements.

Draft deliverables:

- A semantic IR sketch and compile/verify/repair loop for one artifact type.
- Implemented protocol validation: `semantic_atom` fixture validates public record shape only.
- Planned Codex test: Requirement preservation test.
- Planned Codex test: Incremental repair regression test.
- Planned Codex test: Target compilation audit.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:cognitive_compilation.ir.operational_invariant` | `AsiStackProofs.CognitiveCompilation` | A compiled artifact preserves all required IR obligations. | planned |
| `lean:cognitive_compilation.ir.failure_blocks_promotion` | `AsiStackProofs.CognitiveCompilation` | A repair that invalidates an existing obligation cannot be accepted without updating the ledger. | planned |

### Virtual Context ABI

Stable ID: `virtual-context-abi`

Chapter job: Long-horizon agents need a stable interface between durable memory and model-visible working context.

Core claim: Virtual Context Memory should expose a Virtual Context ABI with stable addresses, versions, mounts, snapshots, fault classes, representation contracts, and lifecycle operations.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `vcm_public` | Read first for chapter claims and mechanisms. |
| Supporting | `context_engineer`, `verification_bandwidth`, `viea` | Mine after primary sources for cross-layer connections, variants, and failure modes. |
| Connector or recovery required | `vcm_editable`, `moecot` | Load via Google Drive connector or mark as blocked before source-derived claims. |

Draft arc:

- Problem: Long-horizon agents need a stable interface between durable memory and model-visible working context.
- Insufficiency: Long context windows and ordinary retrieval do not define addressability, evidence, authority, adequacy, or fault behavior.
- Mechanism: Separate durable memory from active context.
- Mechanism: Compile task-relative context packets through an ABI.
- Mechanism: Report adequacy outcomes such as adequate, missing, conflicting, unsafe, unknown, or unsatisfiable.
- Mechanism: Expose unsafe, unknown, or unsatisfied context states rather than hiding them.
- Interface: Planning requests context.
- Interface: VCM compiles packets.
- Interface: Execution receives authority-appropriate context.

Primary invariants:

- Addresses and versions are stable.
- Context adequacy is distinct from admission.
- Faults are typed and visible.

Failure modes to cover:

- Flat transcript memory.
- Stale context.
- Silent unsafe fit.

Draft deliverables:

- A context ABI table covering address, version, mount, snapshot, representation, and fault operations.
- Implemented protocol validation: `context_abi_record` fixture validates public record shape only.
- Implemented Lean proof target: resolved finite context-reference records require matching address, version, and snapshot bindings.
- Planned Codex test: Admission vs adequacy test.
- Planned Codex test: Conflict adequacy classification test.
- Implemented Lean proof target: mandatory context misses produce typed faults instead of best-effort packets.
- Planned Codex test: deployed resolver conformance test.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:vcm.abi.operational_invariant` | `AsiStackProofs.VirtualContextABI` | A context reference resolves only when the requested address and version are valid for the snapshot. | implemented |
| `lean:vcm.abi.failure_blocks_promotion` | `AsiStackProofs.VirtualContextABI` | A mandatory context miss produces a typed fault rather than a best-effort packet. | implemented |

### Semantic Pages, Context Cells, and Certificates

Stable ID: `semantic-pages-context-cells-and-certificates`

Chapter job: Compiled context needs typed semantic units and proof-carrying summaries that preserve provenance and loss contracts.

Core claim: VCM should represent context as typed semantic pages or cells with evidence-carrying representation certificates.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `vcm_public` | Read first for chapter claims and mechanisms. |
| Supporting | `verification_bandwidth`, `spinoza`, `context_engineer` | Mine after primary sources for cross-layer connections, variants, and failure modes. |
| Connector or recovery required | `vcm_editable` | Load via Google Drive connector or mark as blocked before source-derived claims. |

Draft arc:

- Problem: Compiled context needs typed semantic units and proof-carrying summaries that preserve provenance and loss contracts.
- Insufficiency: Summaries can look authoritative while dropping source bindings, omissions, authority ceilings, or allowed-use limits.
- Mechanism: Classify pages as constraints, claims, decisions, corrections, events, artifacts, and other typed cells.
- Mechanism: Attach certificates with source bindings, omissions, validity, authority ceilings, and permitted uses.
- Mechanism: Use task-relative representation graphs instead of one linear compression ladder.
- Interface: Spinoza consumes claim/evidence cells.
- Interface: Planning consumes constraints and decisions.
- Interface: Execution receives only permitted representations.

Primary invariants:

- Authority labels survive summarization.
- Loss contracts are explicit.
- A derived cell points back to source bindings.

Failure modes to cover:

- Summary overconfidence.
- Provenance loss.
- Authority escalation via compression.

Draft deliverables:

- A semantic-page schema with certificate fields and example source-to-summary derivation.
- Implemented protocol validation: `semantic_page_certificate` fixture validates public record shape only.
- Implemented Lean proof target: valid derived cells carry source bindings, loss contracts, and permitted-use declarations.
- Implemented Lean proof target: summaries respecting source cells cannot increase source authority ceilings.
- Planned Codex test: Summary fidelity test.
- Planned Codex test: certificate truthfulness test.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:vcm.certificates.operational_invariant` | `AsiStackProofs.ContextCertificates` | A derived context cell carries source bindings and a declared loss/use contract. | implemented |
| `lean:vcm.certificates.failure_blocks_promotion` | `AsiStackProofs.ContextCertificates` | A summary cannot increase the authority ceiling of its source cells. | implemented |

### Context Transactions, Snapshots, Mounts, and Taint

Stable ID: `context-transactions-snapshots-mounts-and-taint`

Chapter job: Memory and context need runtime semantics for consistency, branches, contradiction, deletion, privacy, and taint.

Core claim: VCM should use transactional memory semantics: immutable events, versioned pages, snapshots, mounts, taint, temporal validity, and deletion closure.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `vcm_public` | Read first for chapter claims and mechanisms. |
| Supporting | `ladon_manhattan`, `context_engineer`, `black_hole_context_manager` | Mine after primary sources for cross-layer connections, variants, and failure modes. |
| Connector or recovery required | `vcm_editable` | Load via Google Drive connector or mark as blocked before source-derived claims. |

Draft arc:

- Problem: Memory and context need runtime semantics for consistency, branches, contradiction, deletion, privacy, and taint.
- Insufficiency: A retrieval store cannot guarantee read-your-writes behavior, copy-on-write experimentation, deletion closure, or taint propagation by itself.
- Mechanism: Record immutable memory events.
- Mechanism: Compile task snapshots with mounts and copy-on-write branches.
- Mechanism: Propagate taint and deletion obligations through derived context.
- Interface: Planning receives consistent views.
- Interface: Security labels sensitive mounts.
- Interface: Evidence records contradictions and supersession.

Primary invariants:

- Snapshots are consistent.
- Taint propagates to derivatives.
- Deletion closure is enforced or faulted.

Failure modes to cover:

- Memory poisoning.
- Stale or contradictory reads.
- Deleted data reappearing in derived summaries.

Draft deliverables:

- A transaction model for context reads, writes, branches, and deletion closure.
- Implemented protocol validation: `context_transaction_record` fixture validates public record shape only.
- Implemented Lean proof target: valid finite snapshot reads see committed events in their declared view.
- Implemented Lean proof target: tainted sources produce tainted derivatives unless declassification is authorized.
- Planned Codex test: Deletion closure test.
- Planned Codex test: memory-store conformance test.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:vcm.transactions.operational_invariant` | `AsiStackProofs.ContextTransactions` | A snapshot read sees the committed events in its declared view. | implemented |
| `lean:vcm.transactions.failure_blocks_promotion` | `AsiStackProofs.ContextTransactions` | A tainted source produces tainted derived context unless declassification is authorized. | implemented |

### Verification Bandwidth and Context Adequacy

Stable ID: `verification-bandwidth-and-context-adequacy`

Chapter job: Long context does not automatically provide long-range reasoning or enough verification capacity.

Core claim: Context systems must distinguish generation capacity from verification bandwidth and declare when context is inadequate.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `verification_bandwidth`, `vcm_public` | Read first for chapter claims and mechanisms. |
| Supporting | `spinoza`, `treellm` | Mine after primary sources for cross-layer connections, variants, and failure modes. |
| Connector or recovery required | `vcm_editable` | Load via Google Drive connector or mark as blocked before source-derived claims. |

Draft arc:

- Problem: Long context does not automatically provide long-range reasoning or enough verification capacity.
- Insufficiency: Adding tokens can increase distractors, attention interference, and unverified summary burden.
- Mechanism: Model verification as bounded by mutual information, representation quality, and attention budget.
- Mechanism: Require adequacy labels for context packets.
- Mechanism: Route high-risk claims to stronger verification instead of more context alone.
- Interface: VCM declares adequacy.
- Interface: Spinoza checks claims.
- Interface: Planning decides escalation when adequacy is insufficient.

Primary invariants:

- Adequacy is explicit.
- More context is not treated as proof.
- High-risk claims pay verification tax.

Failure modes to cover:

- Attention interference.
- False confidence from large context.
- Verification skipped for cost reasons.

Draft deliverables:

- A context adequacy rubric and verification-bandwidth warning states.
- Implemented protocol validation: `context_adequacy_record` fixture validates public record shape only.
- Planned Codex test: Distractor resistance test.
- Planned Codex test: Adequacy labeling test.
- Planned Codex test: Verification escalation test.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:verification_bandwidth.adequacy.operational_invariant` | `AsiStackProofs.VerificationBandwidth` | A context packet admitted for use may still be marked inadequate for a target claim. | planned |
| `lean:verification_bandwidth.adequacy.failure_blocks_promotion` | `AsiStackProofs.VerificationBandwidth` | A high-risk claim with inadequate context cannot receive a verified support label. | planned |

### Claim Ledgers and Belief Revision

Stable ID: `claim-ledgers-and-belief-revision`

Chapter job: The architecture needs a durable epistemic layer for claims, evidence, contradictions, uncertainty, and revision.

Core claim: Reasoning should maintain claim ledgers with support states, provenance, contradiction links, uncertainty, and revision history.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `spinoza`, `viea` | Read first for chapter claims and mechanisms. |
| Supporting | `coherence_exchange`, `aletheia`, `uat` | Mine after primary sources for cross-layer connections, variants, and failure modes. |

Draft arc:

- Problem: The architecture needs a durable epistemic layer for claims, evidence, contradictions, uncertainty, and revision.
- Insufficiency: A model can generate plausible prose without maintaining why it believes a claim or how new evidence changes prior beliefs.
- Mechanism: Extract claims into structured records.
- Mechanism: Attach evidence tier, provenance, and uncertainty.
- Mechanism: Revise beliefs when contradictions or stronger evidence appear.
- Interface: VCM supplies source context.
- Interface: Spinoza verifies claims.
- Interface: Evidence matrix records book-level claims.

Primary invariants:

- Claims are separable from prose.
- Contradictions remain linked.
- Revision history is not overwritten.

Failure modes to cover:

- Untracked assumptions.
- Belief inertia.
- Contradiction deletion.

Draft deliverables:

- A claim-record schema and belief-revision transition example.
- Implemented protocol validation: `claim_record` and `belief_revision_record` fixtures validate public record shape only.
- Planned Codex test: Claim extraction test.
- Planned Codex test: Contradiction detection test.
- Implemented Lean proof target: finite claim updates preserve prior evidence and revision-history references.
- Implemented Lean proof target: open contradictions block promotion until handled.
- Planned Codex test: belief revision engine test.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:claims.ledger.operational_invariant` | `AsiStackProofs.ClaimLedger` | A claim update preserves prior evidence and revision history. | implemented |
| `lean:claims.ledger.failure_blocks_promotion` | `AsiStackProofs.ClaimLedger` | A contradiction prevents promotion until resolved, bounded, or recorded as residual. | implemented |

### Spinoza Verification and Proof-Carrying Claims

Stable ID: `spinoza-verification-and-proof-carrying-claims`

Chapter job: The stack needs a way to move selected claims from generated prose toward auditable, proof-carrying objects.

Core claim: Spinoza-style verification should convert high-value claims into proof-carrying or justification-carrying artifacts with explicit tiers.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `spinoza` | Read first for chapter claims and mechanisms. |
| Supporting | `genesiscode`, `coherence_exchange`, `verification_bandwidth`, `treellm` | Mine after primary sources for cross-layer connections, variants, and failure modes. |

Draft arc:

- Problem: The stack needs a way to move selected claims from generated prose toward auditable, proof-carrying objects.
- Insufficiency: Neural generation alone cannot guarantee semantic consistency, source grounding, or formal validity.
- Mechanism: Separate heuristic proposal from symbolic or structured interrogation.
- Mechanism: Attach formal interpretation mappings, proof bundles, or citation-backed dossiers.
- Mechanism: Downgrade or escalate claims that cannot meet their required tier.
- Interface: Claim ledger stores proof status.
- Interface: GenesisCode and Lean provide formal hooks.
- Interface: UAT provides adversarial review.

Primary invariants:

- Proof tier is explicit.
- A justification artifact is required for promoted claims.
- Unsupported claims remain marked speculative or blocked.

Failure modes to cover:

- Certified delusion.
- Invalid formalization.
- Justification artifact missing.

Draft deliverables:

- A tiered proof-carrying claim schema with one non-philosophical invariant example.
- Implemented protocol validation: `proof_carrying_claim` fixture validates public record shape only.
- Planned Codex test: Proof artifact presence test.
- Planned Codex test: Tier assignment test.
- Planned Codex test: Formalization mismatch review.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:spinoza.proof_carrying.operational_invariant` | `AsiStackProofs.ProofCarryingClaims` | A claim at a formal support tier carries a valid proof or justification artifact reference. | planned |
| `lean:spinoza.proof_carrying.failure_blocks_promotion` | `AsiStackProofs.ProofCarryingClaims` | A failed verifier result downgrades or blocks the claim rather than promoting it. | planned |

### Unified Adaptive Tribunal and Adversarial Review

Stable ID: `unified-adaptive-tribunal-and-adversarial-review`

Chapter job: Complex claims and artifacts need adversarial review that is more structured than one model critique.

Core claim: A tribunal layer should coordinate multiple reviewers, adversarial probes, consensus rules, and documented uncertainty.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `uat` | Read first for chapter claims and mechanisms. |
| Supporting | `spinoza`, `coherence_exchange`, `talos`, `verification_bandwidth` | Mine after primary sources for cross-layer connections, variants, and failure modes. |

Draft arc:

- Problem: Complex claims and artifacts need adversarial review that is more structured than one model critique.
- Insufficiency: Single-pass self-review misses blind spots, evaluator drift, and consensus without evidence.
- Mechanism: Assign reviewer roles and critique objectives.
- Mechanism: Use adversarial checks for high-risk claims.
- Mechanism: Record dissent, unresolved issues, and human-adjudication points.
- Interface: Spinoza consumes tribunal results.
- Interface: Planning escalates risky nodes to tribunal.
- Interface: Evidence records reviewer outcomes.

Primary invariants:

- Dissent is preserved.
- Consensus requires evidence.
- High-risk reviews are reproducible enough to audit.

Failure modes to cover:

- Reviewer collusion.
- Consensus theater.
- Critique without action.

Draft deliverables:

- A tribunal protocol for claim/artifact review with reviewer roles and output schema.
- Implemented protocol validation: `tribunal_review_record` fixture validates public record shape only.
- Planned Codex test: Adversarial review coverage test.
- Planned Codex test: Dissent preservation test.
- Planned Codex test: Consensus evidence test.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:tribunal.review.operational_invariant` | `AsiStackProofs.Tribunal` | A tribunal verdict includes reviewer roles, evidence references, and unresolved dissent. | planned |
| `lean:tribunal.review.failure_blocks_promotion` | `AsiStackProofs.Tribunal` | A high-risk artifact cannot be accepted when required tribunal review is absent. | planned |

### Labor OS and Typed Jobs

Stable ID: `labor-os-and-typed-jobs`

Chapter job: Intelligence must become typed work with lifecycle, permissions, artifacts, logs, and approvals.

Core claim: The execution layer should convert plans into typed jobs managed by a governed labor operating system.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `talos` | Read first for chapter claims and mechanisms. |
| Supporting | `viea`, `genesiscode`, `software_magic_grimoire` | Mine after primary sources for cross-layer connections, variants, and failure modes. |
| Variants / alternate releases | `talos_md` | Use only to compare versions or recover missing detail. |
| Connector or recovery required | `moecot` | Load via Google Drive connector or mark as blocked before source-derived claims. |

Draft arc:

- Problem: Intelligence must become typed work with lifecycle, permissions, artifacts, logs, and approvals.
- Insufficiency: Chat outputs do not provide deterministic job lifecycle, tool isolation, auditability, or repeatable cognitive manufacturing.
- Mechanism: Represent jobs with type, inputs, tools, permissions, expected artifacts, approval gates, and failure behavior.
- Mechanism: Separate orchestration, secure workspace/logistics, security/access controls, secret isolation, and audit as explicit execution subfunctions.
- Mechanism: Isolate tools and runtime adapters.
- Mechanism: Record job lifecycle and evidence artifacts.
- Interface: Planning dispatches jobs.
- Interface: Security mediates permissions.
- Interface: Artifact graph receives outputs.

Primary invariants:

- Every job has type and lifecycle state.
- Tool permissions are explicit.
- Human approval gates block high-impact jobs.

Failure modes to cover:

- Tool overreach.
- Unlogged side effects.
- Infinite or chaotic agent swarms.

Draft deliverables:

- A typed-job schema with lifecycle states and permission checks.
- Implemented protocol validation: `typed_job` fixture validates public record shape only.
- Implemented Lean predicate: a transition record marked valid must use the declared finite lifecycle relation.
- Planned Codex test: Tool permission enforcement test.
- Implemented Lean predicate: an approval-required job cannot be allowed to run before approval is recorded.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:jobs.lifecycle.operational_invariant` | `AsiStackProofs.TypedJobs` | A job transitions only through valid lifecycle states. | implemented |
| `lean:jobs.lifecycle.failure_blocks_promotion` | `AsiStackProofs.TypedJobs` | A job requiring approval cannot execute before approval is recorded. | implemented |

### Artifact Graphs, Audit Logs, and Replay

Stable ID: `artifact-graphs-audit-logs-and-replay`

Chapter job: The stack needs durable artifacts and replayable traces so work can be inspected, reused, tested, and improved.

Core claim: Execution should produce an artifact graph with audit logs, provenance, replay metadata, and links to claims and tests.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `talos`, `viea` | Read first for chapter claims and mechanisms. |
| Supporting | `cognitive_compilation`, `spinoza_composer`, `genesiscode`, `cognitive_loop_closure` | Mine after primary sources for cross-layer connections, variants, and failure modes. |
| Connector or recovery required | `moecot` | Load via Google Drive connector or mark as blocked before source-derived claims. |

Draft arc:

- Problem: The stack needs durable artifacts and replayable traces so work can be inspected, reused, tested, and improved.
- Insufficiency: If outputs are not tied to inputs, tools, context, claims, and logs, later verification and improvement cannot know what happened.
- Mechanism: Record artifacts as nodes with source, job, context, tool, and evidence links.
- Mechanism: Capture replay metadata and environment assumptions.
- Mechanism: Use artifacts as memory and improvement substrate.
- Interface: VCM references artifacts.
- Interface: Evidence consumes logs.
- Interface: Procedural memory mines repeated traces.

Primary invariants:

- Artifacts have stable identities.
- Audit logs are append-only or versioned.
- Replay limits are declared.

Failure modes to cover:

- Untraceable output.
- Non-replayable workflow.
- Provenance gaps.

Draft deliverables:

- An artifact graph schema with job, source, context, and evidence edges.
- Implemented protocol validation: `artifact_graph_record` fixture validates public record shape only.
- Implemented Lean predicate: a produced artifact record must expose parent-job and source/context references.
- Implemented Lean predicate: missing required provenance blocks promoted-claim support.
- Planned Codex test: Audit reconstruction test.
- Planned Codex test: Replay metadata completeness test.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:artifacts.graph.operational_invariant` | `AsiStackProofs.ArtifactGraph` | Every produced artifact records its parent job and source/context references. | implemented |
| `lean:artifacts.graph.failure_blocks_promotion` | `AsiStackProofs.ArtifactGraph` | An artifact with missing required provenance cannot support a promoted claim. | implemented |

### Runtime Adapters, Tool Permissions, and Human Approval

Stable ID: `runtime-adapters-tool-permissions-and-human-approval`

Chapter job: Plans become real-world effects only through tools, runtimes, deployment adapters, and approval gates.

Core claim: Runtime adapters should enforce typed permissions, sandboxing, human approval, and post-action evidence capture.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `talos`, `viea` | Read first for chapter claims and mechanisms. |
| Supporting | `ladon_manhattan`, `software_magic_grimoire`, `genesiscode`, `field_of_god_ai_constitution`, `theseus_operator_os` | Mine after primary sources for cross-layer connections, variants, and failure modes. |
| Connector or recovery required | `moecot` | Load via Google Drive connector or mark as blocked before source-derived claims. |

Draft arc:

- Problem: Plans become real-world effects only through tools, runtimes, deployment adapters, and approval gates.
- Insufficiency: Tool calling without a permission and approval model turns reasoning errors into side effects.
- Mechanism: Map jobs to runtime adapters with declared capabilities.
- Mechanism: Cover document/software, API/service, firmware/hardware, CAD/fabrication, robotics, and organizational workflow targets where source support exists.
- Mechanism: Require permission checks and approval gates for high-impact actions.
- Mechanism: Record deployment evidence and rollback handles.
- Interface: Execution owns adapters.
- Interface: Security mediates secrets.
- Interface: Evidence records deployment outcomes.

Primary invariants:

- No adapter executes beyond granted scope.
- High-impact actions require approval.
- Rollback handles are captured when available.

Failure modes to cover:

- Tool overreach.
- Approval bypass.
- Irreversible deployment without rollback.

Draft deliverables:

- A runtime-adapter contract with permissions, approval requirements, and result evidence.
- Implemented protocol validation: `runtime_adapter_invocation` fixture validates public record shape only.
- Implemented Lean predicate: a valid invocation requires the parent job permissions to include the adapter capability.
- Implemented Lean predicate: a high-impact adapter invocation without approval is rejected.
- Planned Codex test: Rollback handle capture test.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:runtime.adapters.operational_invariant` | `AsiStackProofs.RuntimeAdapters` | A runtime adapter invocation is valid only when job permissions include the adapter capability. | implemented |
| `lean:runtime.adapters.failure_blocks_promotion` | `AsiStackProofs.RuntimeAdapters` | A high-impact adapter call without approval is rejected. | implemented |

### Procedural Memory and Cognitive Loop Closure

Stable ID: `procedural-memory-and-cognitive-loop-closure`

Chapter job: Repeated reasoning trajectories should not be improvised forever when they can become verified procedures or tools.

Core claim: Cognitive loop closure compiles repeated reasoning into verified parameterized tools and procedural memory.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `cognitive_loop_closure` | Read first for chapter claims and mechanisms. |
| Supporting | `rmi`, `rgs`, `benchmaxxing`, `talos`, `project_theseus_whitepaper`, `theseus_self_evolution_system`, `theseus_operator_os` | Mine after primary sources for cross-layer connections, variants, and failure modes. |
| Connector or recovery required | `moecot` | Load via Google Drive connector or mark as blocked before source-derived claims. |

Draft arc:

- Problem: Repeated reasoning trajectories should not be improvised forever when they can become verified procedures or tools.
- Insufficiency: Agents waste cognition and introduce inconsistency when recurring workflows are repeatedly reconstructed from scratch.
- Mechanism: Log safe execution traces.
- Mechanism: Detect recurring loops.
- Mechanism: Abstract invariant structure, discover parameters, verify, and publish tools.
- Interface: Artifact graph supplies traces.
- Interface: Routing selects new tools.
- Interface: Evidence tests utility and regressions.

Primary invariants:

- Only verified loops become tools.
- Parameters and assumptions are explicit.
- Tool promotion records residuals and regressions.

Failure modes to cover:

- Premature toolification.
- Hidden assumptions.
- Procedural memory poisoning.

Draft deliverables:

- A loop closure pipeline from trace detection to verified tool record.
- Implemented protocol validation: `procedural_tool_record` fixture validates public record shape only.
- Planned Codex test: Loop detection test.
- Planned Codex test: Tool abstraction test.
- Planned Codex test: Verified tool regression test.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:procedural.loop_closure.operational_invariant` | `AsiStackProofs.ProceduralMemory` | A generated tool records its source traces, parameters, and verification result. | planned |
| `lean:procedural.loop_closure.failure_blocks_promotion` | `AsiStackProofs.ProceduralMemory` | A tool with failed regression cannot be promoted to routable status. | planned |

## Part III - Routing, Compression, Representation, and Substrates

Part job: Define how the stack scales capability through modular routing, readiness gates, specialist cores, compression, semantic representation, resource budgets, simulation boundaries, mathematical substrates, and optional cyclic/coil lanes.

Part source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Core | `octopus_router`, `rmi`, `benchmaxxing`, `cgs`, `rgs`, `rankfold_neuralfold`, `bbvca_v9`, `treellm`, `tokenmana`, `simulation_scaling`, `genesiscode`, `circle_calculus_core`, `circle_ai_contract_suite`, `coil_attention_memory`, `coilra_multicoil_rope`, `rope_position_certifier` | Load these before drafting or reorganizing this part. |
| Supporting | `rankfold_compressor`, `bbvca_main`, `bugbrain`, `temporal_coil_research`, `project_theseus_whitepaper`, `theseus_circle_transfer`, `proof_carrying_circular_computation`, `circle_ai_architectures`, `viea`, `scf`, `vcm_public`, `planforge`, `talos`, `spinoza` | Load these for lineage, variants, failure modes, and cross-layer synthesis. |
| Connector or recovery required | `moecot`, `moecot_md`, `coilmoecot` | Use Google Drive connector or mark blocked before source-derived claims. |

### Routing Heads and Specialist Cores

Stable ID: `routing-heads-and-specialist-cores`

Chapter job: The architecture needs to allocate cognition across specialists rather than force one system to do every task.

Core claim: ASI scales through a lightweight routing head that selects bounded specialist cores with local tools, memory, and authority.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `octopus_router`, `rmi` | Read first for chapter claims and mechanisms. |
| Supporting | `beastbrain`, `cognitive_loop_closure`, `rgs`, `project_theseus_whitepaper`, `theseus_operator_os` | Mine after primary sources for cross-layer connections, variants, and failure modes. |
| Connector or recovery required | `moecot` | Load via Google Drive connector or mark as blocked before source-derived claims. |

Draft arc:

- Problem: The architecture needs to allocate cognition across specialists rather than force one system to do every task.
- Insufficiency: Monolithic scaling and static tool lists do not provide local memories, bounded authority, specialist lifecycle, or readiness-aware routing.
- Mechanism: Register specialists with capabilities, costs, readiness, authority, and memories.
- Mechanism: Route tasks to the smallest adequate specialist.
- Mechanism: Fallback or escalate when confidence and readiness are insufficient.
- Interface: Planning requests capabilities.
- Interface: Governance bounds specialists.
- Interface: Evidence updates readiness.

Primary invariants:

- Specialist authority is local.
- Routing decisions are logged.
- Fallback paths remain available.

Failure modes to cover:

- Wrong specialist selection.
- Router overconfidence.
- Specialist authority leak.

Draft deliverables:

- A router registry with capability metadata, cost, authority, and fallback rules.
- Implemented protocol validation: `specialist_registry_record` and `routing_decision_record` fixtures validate public record shape only.
- Planned Codex test: Specialist routing accuracy test.
- Implemented Lean predicate: selected routes satisfy authority and readiness.
- Implemented Lean predicate: failed readiness routes to fallback or residual rather than promotion.
- Planned Codex test: Runtime authority enforcement test.
- Planned Codex test: Fallback route execution test.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:routing.specialists.operational_invariant` | `AsiStackProofs.Routing` | A router may select only specialists whose authority and readiness satisfy the task requirement. | implemented |
| `lean:routing.specialists.failure_blocks_promotion` | `AsiStackProofs.Routing` | A failed readiness predicate routes to fallback or residual, not promotion. | implemented |

### Readiness Gates, Residual Escrow, and Quarantine

Stable ID: `readiness-gates-residual-escrow-and-quarantine`

Chapter job: Modules need a lifecycle for promotion, quarantine, retirement, split, merge, and residual tracking.

Core claim: Readiness gates and residual escrow should govern when modules are promoted, quarantined, split, merged, retired, or retrained.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `rmi`, `benchmaxxing`, `scf` | Read first for chapter claims and mechanisms. |
| Supporting | `octopus_router`, `cognitive_loop_closure`, `project_theseus_whitepaper`, `theseus_architecture_gate`, `theseus_self_evolution_system` | Mine after primary sources for cross-layer connections, variants, and failure modes. |
| Connector or recovery required | `moecot` | Load via Google Drive connector or mark as blocked before source-derived claims. |

Draft arc:

- Problem: Modules need a lifecycle for promotion, quarantine, retirement, split, merge, and residual tracking.
- Insufficiency: A benchmark score alone cannot decide whether a specialist is ready or whether unresolved residuals are being hidden.
- Mechanism: Maintain readiness states and promotion gates.
- Mechanism: Record residual failures in escrow.
- Mechanism: Quarantine modules with safety, regression, or scope failures.
- Interface: Routing reads readiness.
- Interface: Benchmarks update gates.
- Interface: SCFs govern replacement.

Primary invariants:

- Promotion requires gate evidence.
- Residuals are not deleted on promotion.
- Quarantine blocks ordinary routing.

Failure modes to cover:

- Premature promotion.
- Residual hiding.
- Untracked regression after merge.

Draft deliverables:

- A module lifecycle state machine and residual escrow ledger.
- Implemented protocol validation: `readiness_gate_record` fixture validates public record shape only.
- Implemented Lean predicate: promoted decisions require all required gates to pass.
- Implemented Lean predicate: quarantined targets cannot be selected for ordinary execution routes.
- Planned Codex test: Readiness transition enforcement test.
- Planned Codex test: Residual escrow integrity test.
- Planned Codex test: Quarantine routing harness test.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:readiness.gates.operational_invariant` | `AsiStackProofs.ReadinessGates` | A module can enter promoted state only after all required gates pass. | implemented |
| `lean:readiness.gates.failure_blocks_promotion` | `AsiStackProofs.ReadinessGates` | A quarantined module cannot be selected for ordinary execution routes. | implemented |

### MoECOT Runtime and Multi-Core Orchestration

Stable ID: `moecot-runtime-and-multi-core-orchestration`

Chapter job: The book needs a concrete implementation reference for governed multi-core orchestration, ledgers, replay, and benchmark promotion.

Core claim: MoECOT should be treated as the implementation-reference layer for a governed low-parameter multi-core ASI stack once its authenticated source is fully mined.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `octopus_router`, `rmi`, `benchmaxxing` | Read first for chapter claims and mechanisms. |
| Supporting | `beastbrain`, `viea`, `scf`, `talos`, `project_theseus_whitepaper`, `theseus_operator_os`, `theseus_architecture_gate` | Mine after primary sources for cross-layer connections, variants, and failure modes. |
| Variants / alternate releases | `moecot_md` | Use only to compare versions or recover missing detail. |
| Connector or recovery required | `moecot` | Load via Google Drive connector or mark as blocked before source-derived claims. |

Draft arc:

- Problem: The book needs a concrete implementation reference for governed multi-core orchestration, ledgers, replay, and benchmark promotion.
- Insufficiency: A purely abstract stack can fail to specify runtime state, registry boundaries, readiness gates, replay, and operational artifacts.
- Mechanism: Use MoECOT as a runtime crosswalk for router, specialist, ledger, benchmark, and replay concepts.
- Mechanism: Keep direct MoECOT claims conservative until the primary source is ingested.
- Mechanism: Map MoECOT mechanisms to other stack layers rather than making it a separate silo.
- Interface: Routing selects cores.
- Interface: SCFs govern replacement.
- Interface: Evidence and replay ledgers evaluate runtime changes.

Primary invariants:

- MoECOT claims stay at argument level until source notes exist.
- Implementation evidence is separated from design argument.
- Runtime promotion follows readiness gates.

Failure modes to cover:

- Overclaiming unavailable source content.
- Treating implementation branding as architecture proof.
- Losing cross-layer traceability.

Draft deliverables:

- A MoECOT crosswalk chapter with authenticated-source gap markers and runtime-interface tables.
- Implemented protocol validation: `moecot_orchestration_record` fixture validates public record shape only.
- Planned Codex test: MoECOT source-ingestion gate.
- Planned Codex test: Runtime crosswalk completeness test.
- Planned Codex test: Readiness/replay mapping review.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:moecot.runtime.operational_invariant` | `AsiStackProofs.MoECOTRuntime` | A runtime core promotion requires readiness, regression, and replay evidence references. | planned |
| `lean:moecot.runtime.failure_blocks_promotion` | `AsiStackProofs.MoECOTRuntime` | A runtime claim sourced only from unavailable text cannot be promoted above argument state. | planned |

### Compact Generative Systems and Residual Honesty

Stable ID: `compact-generative-systems-and-residual-honesty`

Chapter job: The architecture needs a theory of compact systems that generate useful behavior without hiding unresolved complexity.

Core claim: A compact generative system is useful only when compactness, generativity, governance, verification, and residual burden are all explicit.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `cgs`, `rgs` | Read first for chapter claims and mechanisms. |
| Supporting | `bugbrain`, `simulation_scaling`, `rmi`, `project_theseus_whitepaper` | Mine after primary sources for cross-layer connections, variants, and failure modes. |

Draft arc:

- Problem: The architecture needs a theory of compact systems that generate useful behavior without hiding unresolved complexity.
- Insufficiency: Compression can look efficient while moving burden into unmeasured reconstruction, verification, or human review work.
- Mechanism: Define compact generative cores and their residuals.
- Mechanism: Use the seed/router/search/generator/verifier/residual loop as the default compression-control model.
- Mechanism: Treat the raw LLM as a compressed generative engine, not as the entire intelligent system.
- Mechanism: Separate lawful generation from exact remainder.
- Mechanism: Record where compactness fails.
- Interface: Compression feeds memory and routing.
- Interface: Evidence tests downstream utility.
- Interface: Procedural memory turns repeated generation into tools.

Primary invariants:

- Lossy claims are labeled.
- Residual burden is visible.
- Fallback exists when compact generation fails.

Failure modes to cover:

- False lossless claims.
- Hidden residual complexity.
- Compactness that damages utility.

Draft deliverables:

- A compactness ledger with seed, router/index, search/planning, generator/decoder, verifier/critic, residual correction, memory/governance hooks, exact remainder, verification, and residual fields.
- Implemented repository-level fixture: `compact_generative_record.valid.json` validates the compact-generative record shape only; utility and residual-burden behavior remain planned tests.
- Planned Codex test: S/R/Q/G/V/E loop consistency test.
- Implemented Lean predicate: unresolved obligations require residual records.
- Implemented Lean predicate: lossy representations cannot be marked exact without verification evidence.
- Planned Codex test: Residual burden behavior test.
- Planned Codex test: Downstream utility test.
- Planned Codex test: Fallback behavior test.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:compression.cgs.operational_invariant` | `AsiStackProofs.CompactGenerativeSystems` | A compact representation with unresolved obligations carries residual records. | implemented |
| `lean:compression.cgs.failure_blocks_promotion` | `AsiStackProofs.CompactGenerativeSystems` | A lossy representation cannot be marked exact without verification evidence. | implemented |

### Generate-Verify-Repair Compression

Stable ID: `generate-verify-repair-compression`

Chapter job: Some representations may be compressed by storing a lawful generator plus exact repairs, but the book needs disciplined claims around this.

Core claim: Generate-verify-repair compression should store the smallest useful lawful explanation plus the cheapest exact remainder when generation fails.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `bbvca_v9`, `bbvca_main` | Read first for chapter claims and mechanisms. |
| Supporting | `cgs`, `rankfold_neuralfold` | Mine after primary sources for cross-layer connections, variants, and failure modes. |

Draft arc:

- Problem: Some representations may be compressed by storing a lawful generator plus exact repairs, but the book needs disciplined claims around this.
- Insufficiency: Compression narratives can overclaim exactness without bounded search, verification, repair accounting, and fallback criteria.
- Mechanism: Generate from seeded local laws.
- Mechanism: Verify against target.
- Mechanism: Repair mismatches with exact residual mechanisms and record rate discipline.
- Interface: Evidence measures reconstruction and utility.
- Interface: Routing chooses compressed or full representation.
- Interface: VCM uses summaries with loss contracts.

Primary invariants:

- Verification precedes exactness claims.
- Repair cost is counted.
- Search bounds are explicit.

Failure modes to cover:

- Unbounded search.
- Verification skipped.
- Repair larger than original data.

Draft deliverables:

- A compression record with generator, verification result, repair residual, and fallback threshold.
- Implemented repository-level fixture: `compression_receipt.valid.json` validates receipt fields only; no codec, reconstruction benchmark, or rate experiment exists yet.
- Implemented Lean predicate: exact reconstruction claims require generator output plus repair residual to equal the target in a finite record.
- Implemented Lean predicate: failed verification blocks exactness promotion.
- Planned Codex test: Reconstruction quality test.
- Planned Codex test: Repair-cost accounting test.
- Planned Codex test: Bounded-search failure test.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:compression.gvr.operational_invariant` | `AsiStackProofs.GenerateVerifyRepair` | An exact reconstruction claim requires generator output plus repair residual to equal the target. | implemented |
| `lean:compression.gvr.failure_blocks_promotion` | `AsiStackProofs.GenerateVerifyRepair` | A failed verification blocks exactness promotion. | implemented |

### Fast Generation Architectures

Stable ID: `fast-generation-architectures`

Chapter job: The stack needs to reduce serial token-generation latency without treating raw tokens per second as intelligence or bypassing verification.

Core claim: Fast generation should be treated as a governed, planner-selected choice among autoregressive, speculative, multi-token, diffusion, early-exit, state-space, KV-cache, and hybrid modes selected by task risk, quality target, latency budget, compute, memory, and verification burden.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `cgs`, `cognitive_loop_closure`, `benchmaxxing` | Read first for the compact-generation loop, procedural chunking intuition, and measurement discipline. |
| Supporting | `planforge`, `verification_bandwidth`, `tokenmana`, `talos`, `vcm_public`, `spinoza`, `rmi` | Mine after primary sources for planner selection, verifier capacity, budget accounting, artifactization, context packets, repair, and readiness routing. |
| Handoff or recovery notes | `sources/inbox/fast_generation_browser_note_2026-06-24/` | Local-only author-intent and external-literature queue context. Do not quote verbatim or promote claims from this packet. |

External literature queue:

| Area | Expected role | Status |
|---|---|---|
| Multi-token prediction and future-token heads | Compare MTP as a draft/proposal mechanism for breaking strict one-token-per-step generation. | queued; no source note yet |
| Speculative decoding and speculative sampling | Compare draft-model proposal plus target-model verification to the stack's generate-verify-repair pattern. | queued; no source note yet |
| Multi-head decoding and feature-level drafting | Compare Medusa/EAGLE-style internal drafting and latent-state proposal mechanisms. | queued; no source note yet |
| Lookahead, trie retrieval, and branch verification | Compare cached branch proposal, retrieval, and verification as procedural-memory acceleration. | queued; no source note yet |
| Diffusion language models and arbitrary-order generation | Compare parallel denoising, infilling, sketch-first decoding, and quality-speed controls. | queued; no source note yet |
| Early exit and self-speculative inference | Compare cheap intermediate exits with later-layer verification. | queued; no source note yet |
| State-space and recurrent sequence models | Compare sequence-processing efficiency as a different speed axis from multi-token acceptance. | queued; no source note yet |
| KV-cache and serving-layer accelerators | Compare memory-bandwidth and throughput improvements separately from single-request latency. | queued; no source note yet |

Draft arc:

- Problem: The stack needs to reduce serial token-generation latency without treating raw tokens per second as intelligence or bypassing verification.
- Insufficiency: Standard autoregressive decoding, raw throughput benchmarks, and isolated serving optimizations do not specify when a faster generation mode is acceptable, how it is verified, or how its failures block promotion.
- Mechanism: Separate raw generation speed from effective verified tokens per second and useful solution per second.
- Mechanism: Let PlanForge select a generation mode from task requirements, risk tier, latency budget, context shape, and verifier availability.
- Mechanism: Use draft, verify, repair, fallback, and benchmark records before promoting any accelerated mode.
- Mechanism: Route VCM context packets into the selected generator and route accepted outputs through Spinoza, Talos, Benchmaxxing, and SCF gates.
- Mechanism: Treat multi-seed diffusion and hybrid AR, MTP, and diffusion systems as research hypotheses until source notes and experiments exist.
- Interface: PlanForge chooses the generation mode.
- Interface: VCM supplies the bounded context packet.
- Interface: The generator emits draft tokens, sketches, spans, or candidates.
- Interface: Spinoza or a verifier checks acceptance predicates.
- Interface: Talos turns accepted output into artifacts.
- Interface: Benchmaxxing records speed-quality evidence.
- Interface: SCF governs whether a mode is promoted, quarantined, or left experimental.

Primary invariants:

- No fast generation mode is promoted on raw tokens per second alone.
- Every accelerated route names its generation mode, verifier, acceptance predicate, risk tier, and fallback.
- Accepted output is counted separately from proposed output.
- High-risk tasks can require slower verified generation even when a faster mode exists.
- Speculative, diffusion, MTP, and hybrid claims remain at argument level until source notes or tests justify promotion.

Failure modes to cover:

- Speed hides lower answer quality or higher repair cost.
- The verifier becomes the true bottleneck.
- Draft heads, diffusion sketches, or cached continuations drift out of distribution.
- Memory bandwidth, KV-cache pressure, or parallel sampling cost erases token-speed gains.
- Multi-seed generation increases sample count without improving useful solution per second.
- Fallback is omitted after rejection or uncertainty.

Draft deliverables:

- A generation-mode registry and benchmark record with task risk, latency budget, context packet, mode, draft source, verifier, acceptance predicate, accepted tokens, wall-clock time, quality or pass result, compute and memory notes, fallback, and promotion decision.
- Implemented repository-level fixture: `generation_mode_record.valid.json` validates generation-mode record shape only; no decoding benchmark, acceptance-rate test, or serving experiment has been run.
- Planned Codex test: Autoregressive baseline speed-quality test.
- Planned Codex test: Speculative decoding acceptance test.
- Planned Codex test: Multi-token draft-head acceptance test.
- Planned Codex test: Medusa-style internal-head comparison test.
- Planned Codex test: Diffusion small-model speed-quality curve.
- Planned Codex test: Multi-seed diffusion useful-solution-per-second test.
- Planned Codex test: Hybrid AR-to-diffusion repair test.
- Planned Codex test: Planner-selected generation-mode routing test.
- Planned Codex test: Risk-tiered decoding enforcement test.
- Planned Codex test: KV-cache throughput accounting test.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:fast_generation.mode_selection.operational_invariant` | `AsiStackProofs.FastGeneration` | A fast generation route records generation mode, verifier, acceptance predicate, risk tier, and fallback before promotion. | implemented |
| `lean:fast_generation.verified_speed.failure_blocks_promotion` | `AsiStackProofs.FastGeneration` | Raw tokens per second cannot promote a fast generation claim without accepted or verified token evidence, task-success evidence, and a baseline. | implemented |

### RankFold, NeuralFold, and Artifact Compression

Stable ID: `rankfold-neuralfold-and-artifact-compression`

Chapter job: The stack needs artifact-level and tensor-level compression strategies that remain honest about residuals and utility.

Core claim: RankFold/NeuralFold-style artifact compression belongs as a bounded implementation hypothesis with probe-route fallback and residual coding.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `rankfold_neuralfold`, `rankfold_compressor` | Read first for chapter claims and mechanisms. |
| Supporting | `bbvca_v9`, `cgs`, `bugbrain` | Mine after primary sources for cross-layer connections, variants, and failure modes. |

Draft arc:

- Problem: The stack needs artifact-level and tensor-level compression strategies that remain honest about residuals and utility.
- Insufficiency: Storage savings are not enough if compressed artifacts lose semantics, break downstream use, or require expensive fallback too often.
- Mechanism: Use low-rank residual coding or functional preprocessing where appropriate.
- Mechanism: Probe compressed artifacts before use.
- Mechanism: Route to full artifacts when probes fail.
- Interface: Artifact graph stores compressed and full references.
- Interface: Routing selects representation by task.
- Interface: Evidence records latency, ratio, and utility.

Primary invariants:

- Fallback path is known.
- Residual coding is measured.
- Downstream utility is tested.

Failure modes to cover:

- Compression damaging rare critical cases.
- Probe not representative.
- Latency gains erased by fallback.

Draft deliverables:

- A compressed artifact record with ratio, residual, probe, fallback, and utility fields.
- Implemented repository-level fixture: `compressed_artifact_record.valid.json` validates the artifact-compression record shape only; no decoder, corpus benchmark, or downstream utility probe exists yet.
- Planned Codex test: Compression ratio test.
- Planned Codex test: Probe-route fallback test.
- Planned Codex test: Downstream utility preservation test.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:compression.artifacts.operational_invariant` | `AsiStackProofs.ArtifactCompression` | A compressed artifact used for a task must pass that task probe or route to fallback. | planned |
| `lean:compression.artifacts.failure_blocks_promotion` | `AsiStackProofs.ArtifactCompression` | A compression record cannot omit residual or fallback metadata. | planned |

### Semantic Representation and Tree-Structured Models

Stable ID: `semantic-representation-and-tree-structured-models`

Chapter job: The book needs a place for explicit semantic representations that may improve grounding, explainability, and efficient reasoning.

Core claim: Tree-structured semantic representations should be treated as optional representation substrates that must prove grounding, utility, and interoperability.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `treellm` | Read first for chapter claims and mechanisms. |
| Supporting | `spinoza`, `verification_bandwidth`, `cognitive_compilation`, `cgs`, `circle_ai_architectures`, `coilra_multicoil_rope` | Mine after primary sources for cross-layer connections, variants, and failure modes. |

Draft arc:

- Problem: The book needs a place for explicit semantic representations that may improve grounding, explainability, and efficient reasoning.
- Insufficiency: Opaque token prediction does not by itself expose concept hierarchy, source grounding, or interpretable reasoning paths.
- Mechanism: Represent concepts hierarchically.
- Mechanism: Attach semantic tokens to provenance and use constraints.
- Mechanism: Compare tree structures against neural-only baselines.
- Interface: Spinoza uses semantic claims.
- Interface: VCM stores semantic pages.
- Interface: Compression tests representation efficiency.

Primary invariants:

- Semantic nodes are grounded or labeled speculative.
- Hierarchy changes are versioned.
- Representation claims require tests.

Failure modes to cover:

- Hand-built ontology brittleness.
- False explainability.
- Hierarchy drift.

Draft deliverables:

- A semantic-node schema and evaluation plan for one grounded domain.
- Implemented repository-level fixture: `semantic_node_record.valid.json` validates the semantic-node record shape only; no TreeLLM implementation, grounding benchmark, or hierarchy-revision harness exists yet.
- Planned Codex test: Grounding fidelity test.
- Planned Codex test: Hierarchy revision test.
- Planned Codex test: Representation utility benchmark.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:representation.semantic_tree.operational_invariant` | `AsiStackProofs.SemanticRepresentation` | A semantic node marked grounded has at least one provenance link. | planned |
| `lean:representation.semantic_tree.failure_blocks_promotion` | `AsiStackProofs.SemanticRepresentation` | A hierarchy update preserves prior node references or records supersession. | planned |

### Resource Economics and Token Budgets

Stable ID: `resource-economics-and-token-budgets`

Chapter job: Compute, context, verification, and human attention are scarce resources that the architecture must allocate explicitly.

Core claim: The stack should account for token budgets, verification tax, load stability, and risk-adjusted inference value.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `tokenmana`, `planforge` | Read first for chapter claims and mechanisms. |
| Supporting | `coherence_exchange`, `simulation_scaling`, `viea`, `project_theseus_whitepaper`, `coilra_multicoil_rope` | Mine after primary sources for cross-layer connections, variants, and failure modes. |

Draft arc:

- Problem: Compute, context, verification, and human attention are scarce resources that the architecture must allocate explicitly.
- Insufficiency: Ignoring resource economics makes high-quality verification unaffordable and encourages synchronized overload or hidden cost shifts.
- Mechanism: Track task value, uncertainty, cost of error, and inference cost.
- Mechanism: Use regenerative or budgeted capacity mechanisms where useful.
- Mechanism: Escalate verification when risk justifies the cost.
- Interface: Planning allocates budgets.
- Interface: Routing chooses costed specialists.
- Interface: Evidence measures cost-quality tradeoffs.

Primary invariants:

- Budgets do not override protected safety gates.
- High-risk tasks pay verification cost.
- Cost savings are recorded with quality results.

Failure modes to cover:

- Cost-cutting verification away.
- Load-synchronized degradation.
- Resource hoarding by low-value tasks.

Draft deliverables:

- A resource ledger with budget, risk, cost, quality, and verification tax fields.
- Implemented repository-level fixture: `resource_budget_record.valid.json` validates the budget-record shape only; no TokenMana simulation, PlanForge scheduler benchmark, or welfare/load study exists yet.
- Planned Codex test: Budget allocation test.
- Planned Codex test: Risk-adjusted verification test.
- Planned Codex test: Load stability scenario.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:resources.budgets.operational_invariant` | `AsiStackProofs.ResourceEconomics` | A task budget cannot disable required safety or verification gates. | planned |
| `lean:resources.budgets.failure_blocks_promotion` | `AsiStackProofs.ResourceEconomics` | A high-risk task with insufficient verification budget is blocked or escalated. | planned |

### Simulation Fidelity and Physical Constraints

Stable ID: `simulation-fidelity-and-physical-constraints`

Chapter job: The architecture needs a realism check on simulations, nested worlds, fidelity, clockspeed, and compute constraints.

Core claim: Simulation and fidelity claims should be bounded by resource constraints and used as design constraints rather than assumed unlimited substrates.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `simulation_scaling` | Read first for chapter claims and mechanisms. |
| Supporting | `cgs`, `rankfold_neuralfold`, `tokenmana`, `alignment_field` | Mine after primary sources for cross-layer connections, variants, and failure modes. |

Draft arc:

- Problem: The architecture needs a realism check on simulations, nested worlds, fidelity, clockspeed, and compute constraints.
- Insufficiency: Simulation-based claims can become unbounded if scope, fidelity, resource cost, and observer effects are not explicit.
- Mechanism: Define scope, clockspeed, fidelity, and resource demand.
- Mechanism: Use simulation limits to constrain roadmap and benchmark claims.
- Mechanism: Record liberties or approximations explicitly.
- Interface: Efficiency theory uses resource constraints.
- Interface: Benchmarks record fidelity limits.
- Interface: Alignment scenarios avoid unbounded simulation claims.

Primary invariants:

- Fidelity is declared.
- Resource bounds are explicit.
- Speculative simulation metaphysics stays separated from engineering claims.

Failure modes to cover:

- Overclaiming nested simulation feasibility.
- Ignoring resource ceilings.
- Treating approximate simulations as ground truth.

Draft deliverables:

- A simulation-fidelity checklist and cost/fidelity table for experiment design.
- Implemented repository-level fixture: `simulation_contract_record.valid.json` validates the simulation-contract record shape only; no feasibility calculator, simulation benchmark, or external physical-computation audit exists yet.
- Planned Codex test: Fidelity declaration test.
- Planned Codex test: Resource-bound sanity check.
- Planned Codex test: Simulation approximation audit.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:simulation.fidelity.operational_invariant` | `AsiStackProofs.SimulationFidelity` | A simulation claim includes declared scope, fidelity, and resource bounds. | planned |
| `lean:simulation.fidelity.failure_blocks_promotion` | `AsiStackProofs.SimulationFidelity` | An experiment result cannot exceed the declared fidelity support of its simulation. | planned |

### Mathematical and Search Substrates

Stable ID: `mathematical-and-search-substrates`

Chapter job: The source corpus contains exploratory mathematical/search substrates that may matter but must not be overclaimed.

Core claim: Coils, calculi, and geometric search belong in the stack as optional specialist substrates until tests show where they improve search, routing, or compression.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `genesiscode`, `temporal_coil_research` | Read first for chapter claims and mechanisms. |
| Supporting | `cognitive_compilation`, `treellm`, `simulation_scaling`, `circle_calculus_core`, `circle_ai_architectures`, `proof_carrying_circular_computation`, `theseus_circle_transfer` | Mine after primary sources for cross-layer connections, variants, and failure modes. |
| Connector or recovery required | `coilmoecot` | Load via Google Drive connector or mark as blocked before source-derived claims. |

Draft arc:

- Problem: The source corpus contains exploratory mathematical/search substrates that may matter but must not be overclaimed.
- Insufficiency: Novel substrates can become authority theater if they are not tied to baselines, adoption gates, and falsification criteria.
- Mechanism: Frame each substrate as a specialist core or IR option.
- Mechanism: Define expected advantage, baseline, and falsification condition.
- Mechanism: Route experiments through evidence gates before adoption.
- Interface: Routing treats substrate as specialist.
- Interface: Compression tests representation efficiency.
- Interface: Evidence compares against baselines.

Primary invariants:

- Exploratory claims stay exploratory.
- Baselines are recorded.
- Failed hypotheses remain visible.

Failure modes to cover:

- Performance overclaiming.
- Opaque math treated as proof.
- Adoption without regression tests.

Draft deliverables:

- A technical-substrate appendix plan with experiment matrix and adoption gates.
- Implemented repository-level fixture: `substrate_adoption_record.valid.json` validates the substrate-adoption record shape only; no A/B run, representation-efficiency benchmark, CoilMoECOT benchmark, or local Circle build exists yet.
- Planned Codex test: Baseline comparison test.
- Planned Codex test: Representation efficiency test.
- Planned Codex test: Falsification review.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:substrates.search.operational_invariant` | `AsiStackProofs.SearchSubstrates` | A substrate adoption record includes baseline, measured target, and falsification criterion. | planned |
| `lean:substrates.search.failure_blocks_promotion` | `AsiStackProofs.SearchSubstrates` | A substrate without passing evidence remains non-core. | planned |

### Circle Calculus and Proof-Carrying AI Contracts

Stable ID: `circle-calculus-and-proof-carrying-ai-contracts`

Chapter job: The stack needs a way to turn selected mathematical and AI-infrastructure claims into theorem-linked, machine-readable contracts without treating proofs as model-quality evidence.

Core claim: Proof-carrying AI contracts should package finite structural facts as theorem-linked receipts with deterministic fields, consumer gates, validation commands, and explicit non-claims.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `circle_calculus_core`, `circle_ai_contract_suite`, `rope_position_certifier` | Read first for chapter claims and mechanisms. |
| Supporting | `proof_carrying_circular_computation`, `circle_ai_architectures` | Mine after primary sources for cross-layer connections, variants, and failure modes. |

Draft arc:

- Problem: The stack needs a way to turn selected mathematical and AI-infrastructure claims into theorem-linked, machine-readable contracts without treating proofs as model-quality evidence.
- Insufficiency: Ordinary prose, tests, and diagrams can show intent, but they do not give downstream systems stable theorem IDs, proof status, receipt fingerprints, replay checks, and explicit non-claims.
- Mechanism: Model an engineering object as a finite circular address, schedule, window, or phase structure when that model is faithful.
- Mechanism: Attach theorem IDs, proof status, dictionary IDs, fingerprints, deterministic fields, receipt or replay checks, and non-claims.
- Mechanism: Require downstream workloads, ordinary baselines, negative controls, and metrics before any quality, runtime, memory, or transfer claim is promoted.
- Interface: Lean and proof manifests supply theorem status.
- Interface: Python or CLI tools emit receipts and validation reports.
- Interface: Theseus-style private experiments consume contracts without importing private results into public claims.
- Interface: The evidence matrix records claim boundaries and support states.

Primary invariants:

- Proof status is not a model-quality claim.
- Python tests and diagrams are evidence, not formal proof.
- Consumer readiness is not downstream success.
- Non-claims survive transfer into later chapters.

Failure modes to cover:

- Theorem laundering into quality claims.
- Stale or failed theorem IDs.
- Missing baseline or negative-control experiments.
- Exact finite models mistaken for real-valued deployment behavior.

Draft deliverables:

- A contract record with theorem IDs, proof status, content fingerprint, deterministic fields, validation commands, consumer check, ordinary baselines, and non-claims.
- Implemented repository-level fixture: `proof_target_record.valid.json` validates proof-record fields only; no Circle theorem-id resolver, receipt replay, fingerprint check, or vendored contract pack exists yet.
- Implemented Lean predicates: `AsiStackProofs.ProofCarryingContracts` proves local finite-record receipt-boundary and consumer-gate promotion requirements without claiming external Circle theorem replay.
- Planned Codex test: Contract schema validation test
- Planned Codex test: Theorem-id resolution test
- Planned Codex test: Non-claim preservation test
- Planned Codex test: Receipt replay and fingerprint test

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:circle_contracts.receipt_requires_boundary.operational_invariant` | `AsiStackProofs.ProofCarryingContracts` | A proof-carrying AI contract exposes theorem references, deterministic fields, and an explicit non-claim boundary before downstream use. | implemented |
| `lean:circle_contracts.consumer_gate.failure_blocks_promotion` | `AsiStackProofs.ProofCarryingContracts` | A downstream claim cannot be promoted solely from contract readiness without a workload, baseline, metric, and evidence artifact. | implemented |

### Coil Attention, Cyclic Memory, and Recurrence Contracts

Stable ID: `coil-attention-cyclic-memory-and-recurrence-contracts`

Chapter job: Memory, attention, and recurrence mechanisms need finite structural contracts for aliasing, coverage, freshness, active work, loop exits, and overthinking boundaries.

Core claim: Coil attention and memory contracts should be used as structural guardrails for cyclic memory, sparse coverage, recurrence schedules, and work-budget admission, not as claims of retrieval or reasoning quality.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `coil_attention_memory`, `circle_ai_contract_suite` | Read first for chapter claims and mechanisms. |
| Supporting | `theseus_circle_transfer`, `vcm_public`, `verification_bandwidth` | Mine after primary sources for cross-layer connections, variants, and failure modes. |

Draft arc:

- Problem: Memory, attention, and recurrence mechanisms need finite structural contracts for aliasing, coverage, freshness, active work, loop exits, and overthinking boundaries.
- Insufficiency: Long context, sparse attention, ring buffers, and recursive loops can silently hide stale reads, uncovered lags, duplicate slots, alias collisions, or unbounded work.
- Mechanism: Map memory slots, residue, winding, strides, windows, and recurrence schedules into finite circular structures.
- Mechanism: Expose alias, freshness, coverage, active-token, work-saving, and loop-exit fields as auditable contract outputs.
- Mechanism: Compare slot-only, slot-plus-winding, FIFO, LRU, content-gated, and ordinary attention or memory baselines before promoting performance claims.
- Interface: VCM context traces expose context adequacy and authority labels.
- Interface: Attention and memory modules consume contract fields as diagnostic guardrails.
- Interface: Benchmark adapters and Theseus transfer lanes decide whether structural facts survive actual workloads.
- Interface: Proof contracts define the finite boundary of the claim.

Primary invariants:

- Residue-only aliasing remains visible.
- Full structural coverage is not semantic coverage.
- Recurrence budgets include exits and guardrails.
- Stale reads fail closed or enter residual escrow.

Failure modes to cover:

- Alias hiding.
- Overthinking or non-terminating recurrence loops.
- Uncovered sparse-attention lags.
- Freshness facts treated as retrieval-quality evidence.
- No ordinary baseline controls.

Draft deliverables:

- A contract-backed memory and attention evaluation plan with slot, winding, coverage, freshness, active-token, loop-exit, work-budget, and baseline fields.
- Implemented repository-level fixture: `cyclic_memory_contract.valid.json` validates the cyclic-memory record shape only; no KV-cache freshness checker, sparse-coverage harness, recurrence benchmark, or learned-memory workload exists yet.
- Planned Codex test: Cyclic alias visibility test
- Planned Codex test: Sparse coverage gap test
- Planned Codex test: Recurrence budget and exit test
- Planned Codex test: Freshness stale-read rejection test

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:coil_memory.alias_boundary.operational_invariant` | `AsiStackProofs.CoilAttentionMemory` | A cyclic memory claim records residue and winding or marks aliasing as visible residual risk. | planned |
| `lean:coil_attention.coverage_not_quality.failure_blocks_promotion` | `AsiStackProofs.CoilAttentionMemory` | Sparse coverage or freshness facts alone cannot promote a retrieval-quality claim. | planned |

### CoilRA, MultiCoil RoPE, and Cyclic Mixers

Stable ID: `coilra-multicoil-rope-and-cyclic-mixers`

Chapter job: Position encodings, adapters, route heads, and mixers need a place for cyclic or block-cyclic structure that separates structural invariants from quality and runtime claims.

Core claim: CoilRA, MultiCoil RoPE, and cyclic mixers should be treated as optional specialist substrates whose structural guarantees must be paired with dense, LoRA, RoPE, learned, recurrent, or state-space baselines before adoption.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `coilra_multicoil_rope`, `rope_position_certifier` | Read first for chapter claims and mechanisms. |
| Supporting | `circle_ai_contract_suite`, `theseus_circle_transfer`, `circle_ai_architectures` | Mine after primary sources for cross-layer connections, variants, and failure modes. |

Draft arc:

- Problem: Position encodings, adapters, route heads, and mixers need a place for cyclic or block-cyclic structure that separates structural invariants from quality and runtime claims.
- Insufficiency: Parameter-count, equivariance, or exact phase facts can be mistaken for better model behavior unless baselines, hardware costs, alias and load diagnostics, and failure cases are separated.
- Mechanism: Represent adapter blocks, block-cyclic routes, multiphase features, residue and winding, relative RoPE, and circulant convolution as structural contracts.
- Mechanism: Attach alias, load, and parameter-accounting diagnostics before interpreting model behavior.
- Mechanism: Measure quality, runtime, memory, and parameter tradeoffs on ordinary baselines and negative controls before promoting the substrate.
- Interface: Semantic representation chapters define when cyclic structure is actually present.
- Interface: Routing heads or rankers may consume cyclic features only inside declared authority and evidence boundaries.
- Interface: Resource-economics chapters account for parameters, kernels, memory, and latency.
- Interface: Proof contracts and prototype experiments keep structural facts separate from performance results.

Primary invariants:

- Equivariance is not model quality.
- Parameter reduction is not an adoption proof.
- Winding is not discarded when it is required to avoid aliasing.
- Hardware-friendly sizes and kernel costs are recorded.
- Real-valued RoPE claims are separated from exact integer phase-bank claims.

Failure modes to cover:

- Mathematical elegance outruns kernels and baselines.
- Exact finite proofs are overclaimed for real-valued RoPE deployments.
- Lower parameter count comes with worse quality or runtime.
- Phase aliases are hidden by residue-only diagnostics.

Draft deliverables:

- A mixer and position-substrate experiment matrix with structural proof references, ordinary baselines, quality/runtime/memory/parameter metrics, alias and load diagnostics, and explicit non-claims.
- Implemented repository-level fixture: `cyclic_mixer_evaluation_record.valid.json` validates the cyclic-mixer evaluation record shape only; no RoPE certifier run, MLX experiment, hardware-kernel benchmark, or model-quality evaluation exists yet.
- Planned Codex test: RoPE receipt boundary test
- Planned Codex test: Cyclic mixer baseline matrix test
- Planned Codex test: Residue/winding alias diagnostic
- Planned Codex test: Parameter-quality-runtime separation test

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:cyclic_mixers.structural_not_quality.operational_invariant` | `AsiStackProofs.CyclicMixers` | A cyclic mixer claim records the structural invariant separately from quality, runtime, memory, and parameter claims. | planned |
| `lean:cyclic_mixers.baseline_required.failure_blocks_promotion` | `AsiStackProofs.CyclicMixers` | A cyclic substrate cannot be promoted without ordinary baselines and recorded tradeoff metrics. | planned |

## Part IV - Evidence, Implementation, and the Living Book

Part job: Turn the architecture into an accountable research program: executable specifications, Lean proof envelopes, benchmark ratchets, reference traces, implementation roadmap, living-book method, and bibliography discipline.

Part source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Core | `benchmaxxing`, `genesiscode`, `project_theseus_whitepaper`, `theseus_plan_compiler`, `theseus_self_evolution_system`, `theseus_architecture_gate`, `theseus_operator_os` | Load these before drafting or reorganizing this part. |
| Supporting | `road_to_agi`, `moecot`, `moecot_md`, `viea`, `scf`, `vcm_public`, `planforge`, `talos`, `spinoza`, `coherence_exchange` | Load these for lineage, variants, failure modes, and cross-layer synthesis. |
| Connector or recovery required | `road_to_agi`, `moecot`, `moecot_md` | Use Google Drive connector or mark blocked before source-derived claims. |

### Executable Specifications and Lean Proof Envelope

Stable ID: `executable-specifications-and-lean-proof-envelope`

Chapter job: The book needs to decide which architecture claims should become executable specs or Lean proofs.

Core claim: Lean proofs and executable specs should target small invariants: authority, support states, SCF replacement, job lifecycle, context adequacy, and residual records.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `genesiscode` | Read first for chapter claims and mechanisms. |
| Supporting | `spinoza`, `scf`, `talos`, `viea`, `circle_calculus_core`, `circle_ai_contract_suite`, `rope_position_certifier`, `proof_carrying_circular_computation` | Mine after primary sources for cross-layer connections, variants, and failure modes. |

Draft arc:

- Problem: The book needs to decide which architecture claims should become executable specs or Lean proofs.
- Insufficiency: Formal methods are ineffective when applied to vague philosophical claims instead of operational predicates and transitions.
- Mechanism: Maintain a proof target record for each proof/spec candidate.
- Mechanism: Keep proof manifest generated from the outline.
- Mechanism: Distinguish Lean proofs, executable specs, schema contracts, process contracts, research targets, blocked targets, and retired targets.
- Interface: Outline defines proof scope.
- Interface: Lean modules implement selected invariants.
- Interface: Validation checks proof-manifest consistency.

Primary invariants:

- No theorem is claimed proven without `lake build`.
- Proof tags remain stable.
- Broad claims are decomposed before formalization.

Failure modes to cover:

- Formalization theater.
- Unstable proof target names.
- Claiming proof from prose.

Draft deliverables:

- A proof manifest, Lean workspace, first invariant modules, and proof target record schema for support-state and authority checks.
- Implemented repository-level fixture: `proof_target_record.valid.json` validates proof-target record shape only; most targets still need Lean/schema/process/research triage.
- Implemented Lean predicates: `AsiStackProofs.ProofEnvelope` proves local finite-record implemented-target and non-operational routing requirements without claiming full proof-target coverage.
- Implemented generated audit: Appendix E summarizes all 100 proof targets by status, triage class, and recommended route from `proofs/proof_triage.json`.
- Planned Codex test: Proof manifest sync test.
- Planned Codex test: Lake build smoke test.
- Planned Codex test: Artifact-by-artifact target audit.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:proofs.envelope.operational_invariant` | `AsiStackProofs.ProofEnvelope` | A proof target marked implemented has an existing module and passes the build. | implemented |
| `lean:proofs.envelope.failure_blocks_promotion` | `AsiStackProofs.ProofEnvelope` | A proof target for a non-operational claim remains planned or blocked, not implemented. | implemented |

### Benchmark Ratchets and Anti-Goodhart Evidence

Stable ID: `benchmark-ratchets-and-anti-goodhart-evidence`

Chapter job: The architecture needs a way to move capability claims through evidence without overfitting to fixed benchmarks.

Core claim: Benchmark ratchets should preserve regressions, create harder frontiers, record residuals, and resist Goodhart pressure.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `benchmaxxing`, `rmi` | Read first for chapter claims and mechanisms. |
| Supporting | `cognitive_loop_closure`, `uat`, `coherence_exchange`, `tokenmana`, `project_theseus_whitepaper`, `theseus_architecture_gate`, `theseus_self_evolution_system`, `theseus_circle_transfer` | Mine after primary sources for cross-layer connections, variants, and failure modes. |
| Connector or recovery required | `moecot`, `road_to_agi` | Load via Google Drive connector or mark as blocked before source-derived claims. |

Draft arc:

- Problem: The architecture needs a way to move capability claims through evidence without overfitting to fixed benchmarks.
- Insufficiency: Benchmarks can saturate, be gamed, erase regressions, or fail to represent real requirements.
- Mechanism: Track benchmark mastery thresholds and saturation in a benchmark ratchet record.
- Mechanism: Generate regressions, holdout checks, transfer checks, and contamination checks.
- Mechanism: Move residual failures into escrow and new frontier tasks.
- Mechanism: Record negative and inconclusive results as evidence, not cleanup.
- Interface: Routing and SCFs use readiness gates.
- Interface: Evidence matrix records support movement.
- Interface: Changelog records evidence changes.

Primary invariants:

- No test success is claimed without execution.
- Synthetic and empirical evidence remain distinct.
- Regressions are preserved.

Failure modes to cover:

- Benchmark overfitting.
- Hidden regression deletion.
- Claim support inflation.

Draft deliverables:

- A benchmark ratchet record schema with frontier, mastery, residuals, regressions, promotion decisions, and anti-Goodhart checks.
- Implemented repository-level fixture: `benchmark_ratchet_record.valid.json` validates benchmark-ratchet record shape only; no benchmark run, contamination audit, hidden-transfer test, or regression-preservation test exists yet.
- Planned Codex test: Saturation detection test.
- Planned Codex test: Hidden benchmark transfer test.
- Planned Codex test: Regression preservation test.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:benchmarks.ratchet.operational_invariant` | `AsiStackProofs.BenchmarkRatchets` | A capability promotion requires benchmark evidence and preserved regression records. | planned |
| `lean:benchmarks.ratchet.failure_blocks_promotion` | `AsiStackProofs.BenchmarkRatchets` | A saturated benchmark cannot be the sole basis for higher readiness promotion. | planned |

### Integrated Reference Architecture

Stable ID: `integrated-reference-architecture`

Chapter job: Readers need to see how the layers operate as one machine from intent to governed action and improvement.

Core claim: The stack can be specified as an integrated reference architecture with typed handoffs, authority stops, artifacts, evidence updates, and self-improvement gates.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `viea`, `scf`, `vcm_public`, `planforge`, `talos`, `spinoza`, `octopus_router`, `rmi`, `benchmaxxing` | Read first for chapter claims and mechanisms. |
| Supporting | `alignment_field`, `cgs`, `cognitive_loop_closure`, `project_theseus_whitepaper`, `theseus_plan_compiler`, `theseus_self_evolution_system`, `theseus_architecture_gate`, `theseus_operator_os`, `theseus_circle_transfer` | Mine after primary sources for cross-layer connections, variants, and failure modes. |
| Connector or recovery required | `moecot`, `vcm_editable` | Load via Google Drive connector or mark as blocked before source-derived claims. |

Draft arc:

- Problem: Readers need to see how the layers operate as one machine from intent to governed action and improvement.
- Insufficiency: Layer chapters can still feel disconnected unless the book traces the complete control flow and artifacts.
- Mechanism: Trace user intent through constitution, governance, planning, VCM, routing, verification, execution, evidence, and improvement.
- Mechanism: Show the compression loop embedded inside the broader governance, memory, routing, and verification stack.
- Mechanism: Show which artifact each layer emits.
- Mechanism: Identify where authority can stop or reroute the process.
- Interface: All stack layers participate.
- Interface: Artifacts and evidence ledgers provide continuity.
- Interface: SCF gates control improvement.

Primary invariants:

- No layer bypasses governance.
- Artifacts remain traceable.
- Self-improvement follows evidence and authority gates.

Failure modes to cover:

- Untraceable handoffs.
- Planning/execution collapse.
- Self-improvement without evaluator integrity.

Draft deliverables:

- A reference flow diagram, interface table, and end-to-end trace example marked conceptual until implemented.
- Implemented repository-level fixture: `reference_trace_record.valid.json` validates reference-trace record shape only; no integrated runtime trace harness, artifact continuity audit, or authority stop-condition checker exists yet.
- Planned Codex test: End-to-end intent trace test.
- Planned Codex test: Artifact continuity audit.
- Planned Codex test: Authority stop-condition test.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:reference_architecture.trace.operational_invariant` | `AsiStackProofs.ReferenceArchitecture` | An end-to-end trace contains required artifacts for each layer handoff. | planned |
| `lean:reference_architecture.trace.failure_blocks_promotion` | `AsiStackProofs.ReferenceArchitecture` | A trace with a missing governance gate cannot be marked valid. | planned |

### Project Theseus as Report-First Implementation Reference

Stable ID: `project-theseus-as-report-first-implementation-reference`

Chapter job: The book needs a concrete implementation-reference chapter for how the ASI stack can be operated as report-first local machinery instead of only conceptual layer diagrams.

Core claim: Project Theseus should be mined as a report-first implementation reference for RMI, showing how pressure, residuals, gates, ledgers, operator work boards, checkpoints, and self-evolution governance can instantiate the ASI stack without promoting local results as general capability claims.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `project_theseus_whitepaper`, `theseus_plan_compiler`, `theseus_self_evolution_system` | Read first for chapter claims and mechanisms. |
| Supporting | `theseus_architecture_gate`, `theseus_operator_os`, `theseus_circle_transfer`, `rmi`, `cgs`, `benchmaxxing`, `cognitive_loop_closure`, `viea`, `vcm_public`, `scf` | Mine after primary sources for cross-layer connections, variants, and failure modes. |

Draft arc:

- Problem: The book needs a concrete implementation-reference chapter for how the ASI stack can be operated as report-first local machinery instead of only conceptual layer diagrams.
- Insufficiency: A prototype roadmap is not enough unless readers can see how goals, plans, arms, reports, gates, residuals, checkpoints, compute, and operator surfaces interact in a working research system.
- Mechanism: Treat reports and ledgers as the contract, with dashboards as surfaces over those artifacts.
- Mechanism: Use the loop pressure -> attempt -> residual -> diagnosis -> compression -> verification -> structure -> new pressure as implementation discipline.
- Mechanism: Gate heavy training and self-evolution through architecture, preflight, resource, and candidate-promotion checks.
- Mechanism: Route operator work through a durable work board, command vocabulary, node registry, hooks, and feedback reports.
- Mechanism: Keep sparse teacher use proposal-first and guarded by branches, checks, benchmark regressions, and review.
- Interface: The plan compiler supplies contracts, semantic IR DAGs, VCM slices, routes, claim targets, and replay traces.
- Interface: Octopus arms, SymLiquid CGS, SparkStream control, and Hive runtime map stack layers into reports and configs.
- Interface: Genesis-style artifact kernels preserve claims, critiques, benchmark results, tool promotions, architecture decisions, and feedback.
- Interface: Capability matrices and benchmark ledgers expose readiness and residuals without turning local reports into public empirical proof.

Primary invariants:

- The frontier moves while the regression floor holds.
- Promotion uses external-inference-zero evidence where the local gate requires it.
- Reports survive the run and are not replaced by dashboard prose.
- Private experiments and public calibration remain separated.
- Unknown task kinds are blocked rather than guessed.
- Architecture changes follow the intervention ladder.

Failure modes to cover:

- Latest-file report overwrites history.
- Benchmark overfit becomes capability evidence.
- Teacher dependence replaces local evidence.
- Architecture churn outruns residual diagnosis.
- Remote work proceeds without allowlists, TTLs, or kill switches.
- Local prototype results are overclaimed as public evidence.

Draft deliverables:

- An implementation-reference crosswalk table from ASI stack layer to Theseus report, config, or tool surface, with evidence state and public claim boundary for each row.
- Implemented repository-level fixture: `theseus_report_crosswalk_record.valid.json` validates report-crosswalk record shape only; no live Theseus report bundle, replay command, benchmark environment, or current gate output has been imported or rerun.
- Planned Codex test: Theseus report crosswalk completeness test
- Planned Codex test: Architecture gate mapping test
- Planned Codex test: Work-board improvement contract test
- Planned Codex test: Self-evolution intervention ladder audit

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:theseus.reference.report_contract.operational_invariant` | `AsiStackProofs.TheseusReference` | An implementation-reference claim names the report, config, or tool surface and does not rely on dashboard prose alone. | planned |
| `lean:theseus.reference.gate_before_promotion.failure_blocks_promotion` | `AsiStackProofs.TheseusReference` | A capability or self-evolution promotion is blocked when required gate reports are absent or failing. | planned |

### Prototype Roadmap

Stable ID: `prototype-roadmap`

Chapter job: The architecture needs a build sequence that does not introduce agency or self-improvement before auditability and governance are credible.

Core claim: The prototype should grow in staged increments from source matrix and artifact graph to governed capability replacement.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `viea`, `benchmaxxing`, `scf`, `vcm_public`, `planforge`, `beastbrain` | Read first for chapter claims and mechanisms. |
| Supporting | `beastbrain_timeless`, `bugbrain`, `project_theseus_whitepaper`, `theseus_plan_compiler`, `theseus_self_evolution_system`, `theseus_architecture_gate`, `theseus_operator_os`, `theseus_circle_transfer`, `circle_ai_contract_suite` | Mine after primary sources for cross-layer connections, variants, and failure modes. |
| Connector or recovery required | `moecot`, `moecot_md`, `road_to_agi`, `coherence_exchange` | Load via Google Drive connector or mark as blocked before source-derived claims. |

Draft arc:

- Problem: The architecture needs a build sequence that does not introduce agency or self-improvement before auditability and governance are credible.
- Insufficiency: A roadmap that jumps to autonomous improvement skips source matrices, artifact graphs, claim ledgers, tests, and authority controls.
- Mechanism: Start with source inventory, claim ledger, artifact graph, and validation.
- Mechanism: Represent each build phase with a prototype phase record.
- Mechanism: Add planner, VCM, typed execution, verification, benchmark ratchets, and SCF gates in order.
- Mechanism: Delay recursive self-improvement until evaluator and governance integrity are credible.
- Interface: Each phase unlocks a later layer.
- Interface: Evidence gates decide promotion.
- Interface: Changelog and releases document progress.

Primary invariants:

- Phases have acceptance criteria.
- Self-improvement is gated.
- Roadmap milestones are not test results.

Failure modes to cover:

- Building agency before auditability.
- Skipping verification because prototypes feel useful.
- Treating roadmap as evidence.

Draft deliverables:

- A prototype phase record schema with deliverables, gates, blockers, validation commands, evidence refs, and acceptance criteria.
- Implemented repository-level fixture: `prototype_phase_record.valid.json` validates prototype-phase record shape only; no phase completion or capability unlock is implied.
- Planned Codex test: Phase acceptance checklist.
- Planned Codex test: Dependency gate review.
- Planned Codex test: Prototype evidence-state audit.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:roadmap.phases.operational_invariant` | `AsiStackProofs.PrototypeRoadmap` | A roadmap phase can unlock a dependent phase only after acceptance gates pass. | planned |
| `lean:roadmap.phases.failure_blocks_promotion` | `AsiStackProofs.PrototypeRoadmap` | A phase milestone cannot promote a claim without evidence artifacts. | planned |

### Living Book Methodology

Stable ID: `living-book-methodology`

Chapter job: The book itself must remain a living technical system rather than a static anthology.

Core claim: The living book should model the ASI stack discipline through manifest-driven Quarto, source queues, claim/evidence matrices, proof manifests, tests, changelogs, and releases.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `benchmaxxing`, `viea` | Read first for chapter claims and mechanisms. |
| Supporting | `bugbrain`, `cognitive_loop_closure` | Mine after primary sources for cross-layer connections, variants, and failure modes. |
| Connector or recovery required | `moecot`, `moecot_md`, `road_to_agi` | Load via Google Drive connector or mark as blocked before source-derived claims. |

Draft arc:

- Problem: The book itself must remain a living technical system rather than a static anthology.
- Insufficiency: Static manuscripts cannot show source additions, claim-state movement, deprecations, proof updates, render status, or test history.
- Mechanism: Use `book_structure.json` for order and dynamic chapters.
- Mechanism: Use `docs/book_outline.md` for drafting, source queues, and Lean scope.
- Mechanism: Treat conversation-mined packets as author-intent and lineage context, not as independent evidence.
- Mechanism: Use drafting annotations such as [SOURCE], [AUTHOR INTENT], [SYNTHESIS], [EXPERIMENT], and [OPEN] in private notes or source notes when helpful.
- Mechanism: Require meaningful updates to sync scaffold, proof manifest, validation, render, and changelog.
- Interface: Source ingestion feeds source notes.
- Interface: Drafting feeds claim matrices.
- Interface: Tests feed support states.
- Interface: Releases feed GitHub Pages.

Primary invariants:

- No fabricated source content.
- No fabricated test results.
- Deprecated claims remain visible.

Failure modes to cover:

- Public site diverges from Quarto source.
- Outline and manifest drift.
- Readers cannot tell which claims are speculative.

Draft deliverables:

- A public Quarto repo with dynamic scaffold, source matrix, claim matrix, proof manifest, validation, GitHub Pages, and public release records.
- A public-safe author-intent and lineage appendix that preserves architecture intent without publishing private conversation text.
- Implemented repository-level validation: `living_book_release_record.valid.json` and tracked records in `release_records/` validate release-record shape only; render and validation checks prove publication hygiene, not manuscript quality or claim truth.
- Planned Codex test: Quarto render check.
- Planned Codex test: Manifest/outline consistency check.
- Planned Codex test: Changelog update check.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:living_book.methodology.operational_invariant` | `AsiStackProofs.LivingBook` | Every chapter in the manifest has outline proof targets and generated claim placeholders. | planned |
| `lean:living_book.methodology.failure_blocks_promotion` | `AsiStackProofs.LivingBook` | A structural update without regenerated scaffold/proof manifest is invalid. | planned |

### Open Research Agenda and Bibliography Plan

Stable ID: `open-research-agenda-and-bibliography-plan`

Chapter job: The book needs a managed research backlog and bibliography plan so new papers can be inserted without destabilizing the architecture.

Core claim: The bibliography and research agenda should map source families, external literature queues, missing papers, proof targets, experiment backlogs, and chapter insertion rules.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `verification_bandwidth`, `benchmaxxing` | Read first for chapter claims and mechanisms. |
| Supporting | `alignment_field`, `scf`, `planforge`, `vcm_public`, `spinoza`, `talos`, `rmi`, `cgs`, `genesiscode`, `simulation_scaling`, `field_of_god_ai_constitution`, `project_theseus_whitepaper`, `circle_calculus_core`, `circle_ai_contract_suite`, `theseus_circle_transfer` | Mine after primary sources for cross-layer connections, variants, and failure modes. |
| Connector or recovery required | `moecot`, `coilmoecot`, `road_to_agi`, `vcm_editable` | Load via Google Drive connector or mark as blocked before source-derived claims. |

Draft arc:

- Problem: The book needs a managed research backlog and bibliography plan so new papers can be inserted without destabilizing the architecture.
- Insufficiency: A pile of sources or ad hoc citations does not tell future writing agents what to load, compare, prove, test, or defer.
- Mechanism: Maintain source inventory, source notes, bibliography, and source-loading queues.
- Mechanism: Track recovered and missing items as research backlog records instead of treating them as evidence.
- Mechanism: Use triage rules to update chapters or add precise new ones.
- Interface: Appendix G lists corpus and external literature queue.
- Interface: Source notes support chapter drafting.
- Interface: Book outline tells future agents what to mine.

Primary invariants:

- Do not cite unread sources as support.
- Do not infer bibliographic metadata.
- New papers update inventory before chapter claims.

Failure modes to cover:

- Citation drift.
- Duplicate chapter creation for overlapping ideas.
- Missing sources treated as evidence.

Draft deliverables:

- A research backlog record schema with external literature areas, source-note state, claim-mapping state, proof/test backlog, and insertion/merge rules.
- Implemented repository-level fixture: `research_backlog_record.valid.json` validates backlog-record shape only; external-literature normalization, direct citation checks, and new-paper triage rehearsals remain incomplete.
- Planned Codex test: Source inventory validation test.
- Planned Codex test: Source-note backlog audit.
- Planned Codex test: New-paper triage scenario.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:bibliography.plan.operational_invariant` | `AsiStackProofs.BibliographyPlan` | A source-derived claim requires a source note or equivalent ingested-source artifact. | planned |
| `lean:bibliography.plan.failure_blocks_promotion` | `AsiStackProofs.BibliographyPlan` | A new source cannot be assigned to a non-existent chapter id. | planned |

## Bibliography and Source Corpus

Appendix G is the generated bibliography and source-corpus map. It should remain generated from `sources/source_inventory.json` and `book_structure.json`. External literature should be added only when bibliographic metadata is recorded and the source is actually used.

## Author Intent and Architecture Lineage

Appendix H is the curated, public-safe home for conversation-mined author intent, architecture lineage, terminology decisions, and recovery tasks. It should not quote private conversation wording verbatim and should not promote claims to source-derived support state.

## Missing or Recovery Source Queue

| Item | Current handling |
|---|---|
| `moecot` | Authenticated connector access and a source note exist; MoECOT-specific claims still need explicit Appendix C mapping before support-state promotion. |
| `vcm_editable` | Authenticated connector access and a source note exist; mine for VCM terminology and external-literature candidates without treating references as cited until recorded. |
| `coherence_exchange` | Authenticated connector access and a source note exist; treat speculative synthesis as bounded design context unless claims are separately supported. |
| `road_to_agi` | Authenticated connector access and a source note exist; benchmark claims remain source-reported until artifacts are independently ingested or reproduced. |
| `coilmoecot` | Authenticated connector access and a source note exist; treat as design/spec context, not performance evidence. |
| Field of God AI Constitution | Recovered as `field_of_god_ai_constitution` in the local/public Theseus repository; create a source note before promoting claims beyond `argument`. |
| Circle Calculus full paper set | Recovered in `/Users/corbensorenson/Documents/circle math` and public `circle-calculus`; source records now route proof contracts, RoPE, coil memory, cyclic mixers, and proof-carrying computation into precise chapters. |
| Genesis Engine / Genesis Foundry | Search Drive later; current proxies are GenesisCode, VIEA, Cognitive Compilation, and MoECOT-related docs. |
| SymLiquid / Project Theseus | Recovered in `/Users/corbensorenson/Documents/Theseus-Hive` and public `symliquid-rmi`; use the Project Theseus implementation-reference chapter while keeping public capability claims at `argument` until source notes/tests exist. |
| BBVCA detailed lineage | Current outline uses `bbvca_v9` and `bbvca_main`; recover detailed conversation/source context before making priority or empirical claims. |
| Spinoza development details | Current outline has the Spinoza architecture slot; recover fuller development notes before source-derived reasoning/verification claims. |
| VCM review conflicts | Resolve against the latest public VCM paper or durable source note before changing VCM claims. |
| Private empirical results | Do not include or cite until the exact artifact, command, environment, and publication permission are recorded. |
