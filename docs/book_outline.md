# Cohesive Book Outline

Working title: **The ASI Stack: A Systems Architecture for Governed, Efficient, Self-Improving AI**

Status: expanded source-of-truth drafting outline, updated 2026-06-25 after adding Personal Compute Hives and Artifact Steward Agents from public-safe browser-note triage. `book_structure.json` remains the ordering source of truth; Quarto generates displayed chapter numbers from the manifest.

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

## Audience and Edition Spine

Future writing runs should serve three audiences from one canonical source tree:

- AIs and writing agents need stable IDs, source queues, claim/evidence states, proof hooks, schemas, validation commands, and guardrails.
- Human researchers need the full technical argument plus traceable evidence machinery, known residuals, and frozen major-version review artifacts.
- Interested human readers need a coherent manuscript for EPUB, PDF, DOCX, e-reader, and audio consumption without repeated live-workflow scaffolding.

The ordinary chapter prose is the reader-facing spine. It must still make sense after live-only headings such as `Chapter status`, `Drafting guardrail`, `Codex test plan`, `Source crosswalk`, `Claim-source mapping status`, and `Formalization hooks` are stripped. Meaning-critical caveats, uncertainty, and support-state limits belong in the spine, not only in a stripped guardrail or source-crosswalk section.

Major-version reader and audio editions are derivatives of the live book, not parallel manuscripts. Use `editions/release_profiles.json` as the machine-readable contract for content layers, strip rules, release gates, target formats, generated manifests, human-consumption bundle gates, and non-claims.

When drafting or revising chapters, preserve a continuous reader-facing spine before the live-only sections do their audit work. A future writing goal should be able to strip status blocks, source crosswalks, proof hooks, and Codex test plans while still leaving a coherent EPUB/PDF/DOCX manuscript and a narration-ready audio script path.

For major versions, the reader manuscript is the human source for EPUB, PDF, DOCX, reader HTML, and optional downstream e-reader conversions such as AZW3, MOBI, Markdown, or plain text. Audio is downstream of the reviewed reader manuscript, not the live book directly. MP3, M4B, and audio embedded in EPUB require their own script review, spoken-treatment review, package check, and edition release record.

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
- Exact Appendix C claim-source mappings for the core claim across `viea`, `beastbrain`, `aletheia`, `talos`, `moecot`, and `scf`; support remains `argument` pending implementation or test evidence.
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
- Exact Appendix C claim-source mappings for the core claim across all assigned efficiency, compression, simulation, lineage, and implementation-reference sources; support remains `argument` pending measured route, cost, residual, and compression evidence.
- Planned Codex test: Minimum viable route test.
- Planned Codex test: Residual burden accounting test.
- Planned Codex test: Utility-preserving compression test.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:efficiency.minimum_viable.operational_invariant` | `AsiStackProofs.Efficiency` | A route is minimum viable only when no lower-cost authorized route satisfies the required quality predicate. | implemented |
| `lean:efficiency.minimum_viable.failure_blocks_promotion` | `AsiStackProofs.Efficiency` | A routed or compressed result with open obligations cannot be promoted without a residual record. | implemented |

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
- Exact Appendix C claim-source mappings for the core claim across `viea`, `scf`, `talos`, `ladon_manhattan`, `genesiscode`, and `moecot`; support remains `argument` pending denial fixtures, permission-separation tests, confused-deputy probes, or deployed enforcement artifacts.
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
- Exact Appendix C claim-source mappings for the core claim across failure-boundary, context, execution, verification, governance-lineage, resource, VCM-variant, and implementation-reference sources; seven local mappings (`scf`, `vcm_public`, `talos`, `spinoza`, `field_of_god`, `viea`, `simulation_scaling`) now have reviewed raw-cache passage references, while `vcm_editable` and `moecot` remain connector-only/source-note mapped. Support remains `argument` pending scenario tests or deployed detector evidence.
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
- Mechanism: Treat the intent contract as a scoped authority lease: the raw request preserves human expression, while the structured contract controls what powers downstream layers may use.
- Mechanism: Require re-contracting when a plan changes allowed means, authority ceiling, publication surface, affected parties, evidence requirements, or stop conditions.
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
- Exact Appendix C claim-source mappings for the core claim across `viea`, `software_magic_grimoire`, `planforge`, `cognitive_compilation`, and `talos`; all five local mappings now have reviewed raw-cache passage references. Support remains `argument` pending parser, authority-extraction, stop-condition, or lowering tests.
- Planned Codex test: Intent parsing ambiguity test.
- Planned Codex test: Authority extraction test.
- Planned Codex test: Stop-condition preservation test.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:intent.contract.operational_invariant` | `AsiStackProofs.IntentContracts` | A compiled intent contract preserves declared constraints and stop conditions. | implemented |
| `lean:intent.contract.failure_blocks_promotion` | `AsiStackProofs.IntentContracts` | A contract missing required authority cannot compile to an executable job. | implemented |

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
- Mechanism: Treat the constitutional substrate as a translation layer from lineage-language to active predicates, open review obligations, and speculative/non-claim boundaries.
- Mechanism: Translate philosophical commitments into operational predicates where possible, while preserving uncertainty labels.
- Mechanism: Keep metaphysical claims labeled as interpretation unless separately supported.
- Mechanism: Attach active constitutional constraints to planning, tool/memory/power, and self-improvement gates.
- Interface: Planning receives admissible-goal constraints.
- Interface: Runtime receives power, memory, and tool-risk gates.
- Interface: Governance receives protected constraints and non-weakenable predicates.
- Interface: Verification checks whether normative claims exceed evidence or translation status.

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
- Exact Appendix C claim-source mappings for the core claim across alignment lineage, metaphysical variants, reasoning governance, connector synthesis, and the AI Constitution source; six mappings (`alignment_field`, `field_of_god`, `ethica_mechanica`, `eternal_code`, `spinoza`, `field_of_god_ai_constitution`) now have reviewed passage references, while `coherence_exchange` remains connector-only/source-note mapped. Support remains `argument` pending constitutional consistency, self-modification ethics, power-without-care, runtime policy, or red-team evidence.
- Planned Codex test: Constitutional consistency test.
- Planned Codex test: Self-modification ethics scenario.
- Planned Codex test: Power-without-care scenario.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:alignment.constitution.operational_invariant` | `AsiStackProofs.Alignment` | An admitted plan satisfies every active constitutional predicate. | implemented |
| `lean:alignment.constitution.failure_blocks_promotion` | `AsiStackProofs.Alignment` | A self-modification that weakens a protected predicate is rejected. | implemented |

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
- Mechanism: Attach an agency-rights checklist to high-impact plans with affected parties, stakes, consent/refusal route, review, appeal, rollback, accountability, dependency residual, and approval threshold.
- Mechanism: Represent agency constraints as limits on delegation, manipulation, coercive dependence, and irreversible effects.
- Mechanism: Define corrigibility as preserved update, correction, rollback, shutdown, and appeal pathways.
- Mechanism: Use contestability and audit rights as governance mechanisms.
- Mechanism: Distinguish declared rights from usable runtime affordances; refusal, review, appeal, audit, rollback, and exit count only when available under pressure and before irreversible effects where needed.
- Mechanism: Record agency residuals when rights exist only as policy text, arrive too late, require unreasonable cost, or disappear after deployment, automation, replacement, or self-improvement.
- Interface: Alignment defines agency predicates.
- Interface: Governance enforces rights and approval thresholds.
- Interface: Execution requires preserved review and correction paths before irreversible effects.

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
- Exact Appendix C claim-source mappings for the agency/corrigibility core claim across alignment lineage, recursive-agency governance, metaphysical variants, connector synthesis, and the AI Constitution source; five mappings (`alignment_field`, `ethica_mechanica`, `field_of_god`, `eternal_code`, `field_of_god_ai_constitution`) now have reviewed passage references, while `coherence_exchange` remains connector-only/source-note mapped. Support remains `argument` pending agency-preservation, corrigibility-pathway, high-impact approval, manipulation-resistance, or runtime-policy evidence.
- Planned Codex test: Agency-preservation scenario.
- Planned Codex test: Corrigibility pathway test.
- Planned Codex test: High-impact approval test.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:corrigibility.agency.operational_invariant` | `AsiStackProofs.Corrigibility` | Protected agency rights remain available after an accepted transition. | implemented |
| `lean:corrigibility.agency.failure_blocks_promotion` | `AsiStackProofs.Corrigibility` | A transition that removes a required correction pathway is rejected. | implemented |

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
- Mechanism: Preserve value conflict as evidence when a proposed action pulls protected commitments apart.
- Mechanism: Classify conflicts by value type, stakeholder, reversibility, authority/consent boundary, stakes, and evidence requirement.
- Mechanism: Escalate high-stakes or unresolved conflicts to tribunal or human review while preserving dissent and unsupported premises.
- Mechanism: Record bounded decisions, revisit conditions, and residual moral uncertainty.
- Mechanism: Treat moral residuals as control inputs that can narrow authority, require reversible action, set expiry, preserve dissent, or trigger review instead of being optimized away.
- Interface: Alignment produces conflict records.
- Interface: Planning carries conflict constraints with the plan.
- Interface: Governance decides review routes and authority boundaries.
- Interface: Evidence records review outcomes, dissent, unsupported premises, and residual uncertainty.

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
- Exact Appendix C claim-source mappings for the value-conflict core claim across recursive-agency governance, alignment lineage, connector synthesis, UAT review mechanics, Spinoza belief revision, and the AI Constitution source; five mappings (`ethica_mechanica`, `alignment_field`, `uat`, `spinoza`, `field_of_god_ai_constitution`) now have reviewed passage references, while `coherence_exchange` remains connector-only/source-note mapped. Support remains `argument` pending value-conflict classification, review-escalation, residual-uncertainty preservation, reviewer-quality, or runtime-policy evidence.
- Planned Codex test: Value conflict classification test.
- Planned Codex test: Review escalation test.
- Planned Codex test: Residual uncertainty preservation test.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:values.conflict.operational_invariant` | `AsiStackProofs.ValueConflict` | A decision with unresolved protected conflicts carries a residual conflict record. | implemented |
| `lean:values.conflict.failure_blocks_promotion` | `AsiStackProofs.ValueConflict` | A high-stakes conflict cannot bypass the required review predicate. | implemented |

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
- Mechanism: Represent audit, exit, fork, dissent, and contestability as capabilities with access paths, artifacts, preservation rules, safety constraints, and denial semantics.
- Mechanism: Attach audit artifacts and redaction/denial reasons to governance decisions.
- Mechanism: Treat fork/exit as preserved escape hatches against lock-in while preserving source, privacy, and safety obligations.
- Mechanism: Treat material usability and recorded denial semantics as part of the right, so an audit, exit, fork, or dissent path is not merely a declared policy aspiration.
- Interface: Governance issues rights.
- Interface: SCFs preserve rights across replacement.
- Interface: Memory/security/execution systems produce evidence for audit, export, revocation, and contestability.

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
- Exact Appendix C claim-source mappings for the governance-rights core claim across recursive governance, connector synthesis, alignment lineage, security-bound authority, Spinoza review discipline, UAT adversarial review, and the AI Constitution source; six mappings (`ethica_mechanica`, `alignment_field`, `ladon_manhattan`, `spinoza`, `uat`, `field_of_god_ai_constitution`) now have reviewed passage references, while `coherence_exchange` remains connector-only/source-note mapped. Support remains `argument` pending audit-record availability, exit-path preservation, fork-right safety, authority-boundary, or deployed governance evidence.
- Planned Codex test: Audit-record availability test.
- Planned Codex test: Exit-path preservation test.
- Planned Codex test: Fork-right safety test.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:governance.rights.operational_invariant` | `AsiStackProofs.GovernanceRights` | A governance transition preserves required audit and exit capabilities. | implemented |
| `lean:governance.rights.failure_blocks_promotion` | `AsiStackProofs.GovernanceRights` | A transition that removes a protected right is rejected or marked invalid. | implemented |

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
- Mechanism: Treat an SCF as the contract that separates requested capability, candidate implementation, and routable authority.
- Mechanism: Separate field identity from implementation artifacts, evaluator policy, and lifecycle state.
- Mechanism: Bind qualification claims to exact artifacts and scoped qualification contexts.
- Mechanism: Represent lifecycle states such as shadow, canary, qualified, default, deprecated, and retired.
- Mechanism: Attach qualification context such as epoch, domain, risk budget, hardware, authority tier, and benchmark state.
- Mechanism: Pair broad route proposers with narrow validators that check field identity, claims, leases, profiles, grants, state paths, composition certificates, and authority ceilings.
- Mechanism: Treat the SCF as capability-identity memory: field identity, evaluator policy, regression floors, lifecycle history, incidents, and rollback obligations survive implementation replacement.
- Mechanism: Make qualification leases reviewable and aging: benchmark epoch, source corpus, hardware profile, threat model, incident triggers, and requalification duties can expire or downgrade route status.
- Interface: Planning sees semantic capability boundaries.
- Interface: Execution sees authorized routes.
- Interface: Evidence and governance see qualification claims, regressions, incidents, lifecycle state, evaluator policy, and recovery paths.

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
- Exact Appendix C claim-source mappings for the stable-capability-field core claim across SCF identity/lifecycle semantics, VIEA artifact/evidence discipline, Talos job/proof-bundle discipline, Ladon/Manhattan authority-handle boundaries, and MoECOT implementation-reference context; four mappings (`scf`, `viea`, `talos`, `ladon_manhattan`) now have reviewed passage references, while `moecot` remains connector-only/source-note mapped. Support remains `argument` pending route-validity, evaluator-integrity, authority non-escalation, rollback-readiness, or deployed lifecycle evidence.
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
- Mechanism: Turn each proposed improvement into a replacement transaction with wall diagnosis, evidence packet, prechecks, gates, canary, residual escrow, monitor window, and rollback obligation.
- Mechanism: Run field-identity, authority, qualification, regression-floor, holdout, and residual checks before commit.
- Mechanism: Treat failed gates and benchmark transfer failures as residuals rather than disappearing work.
- Mechanism: Keep candidate improvement, canary use, default promotion, monitor evidence, and rollback obligation as separate transaction states.
- Interface: SCF ledger defines the field identity to preserve.
- Interface: Benchmark and evidence ledgers test frontier movement and regression preservation.
- Interface: Artifact graph and changelog record candidate artifacts, state migration, decision, residuals, and recovery state.
- Exact Appendix C claim-source mappings for the core replacement claim across SCF field identity, RMI modular ratchets, Benchmaxxing benchmark lifecycle, Cognitive Loop Closure procedural lifecycle, Talos audit/replay context, and MoECOT runtime-reference context; five local mappings (`scf`, `rmi`, `benchmaxxing`, `cognitive_loop_closure`, `talos`) now have reviewed passage references, while `moecot` remains connector-only/source-note mapped. Support remains `argument` pending regression-preservation tests, rollback dry runs, monitor-window evidence, artifact replay, or deployed replacement evidence.

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
- Mechanism: Split sensitive action into request, authorization, substitution, execution, sanitization, and audit.
- Mechanism: Use handles rather than exposing secrets; return handle status and decisions without secret bytes.
- Mechanism: Separate model-visible context from privileged substitution inside approved boundaries.
- Mechanism: Run high-risk tasks inside compartmentalized Digital SCIF context containers with lifecycle and residual leak-risk records.
- Interface: VCM supplies least-privilege context and clearance-scoped mission briefs.
- Interface: Execution checks tool permissions and performs substitution only at authorized runtime boundaries.
- Interface: Governance audits sensitive transitions through Authority Use Receipts.
- Exact Appendix C claim-source mappings for the core security-kernel claim across Ladon/Manhattan blind handles, Context Engineer SCIF/context-supply-chain lifecycle, Talos execution/audit context, Alignment Field normative boundary pressure, and Coherence Exchange governance framing; four local mappings (`ladon_manhattan`, `context_engineer`, `talos`, `alignment_field`) now have reviewed passage references, while `coherence_exchange` remains connector-only/source-note mapped. Support remains `argument` pending secret-handle substitution tests, SCIF least-privilege tests, prompt-injection containment scenarios, threat-model artifacts, side-channel analysis, or deployed runtime evidence.

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
- Mechanism: Compose SCF targets, replacement transactions, security-kernel boundaries, protected-invariant reviews, and evidence gates into a Self-Improvement Transition.
- Mechanism: Require a cheaper-intervention ladder and evidence packet before teacher edits, architecture edits, or parameter growth.
- Mechanism: Separate proposing, evaluating, approving, committing, monitoring, rollback, and retirement.
- Mechanism: Delay autonomous replacement until evaluators, readiness gates, governance logs, and rollback paths are credible.
- Interface: SCFs define replaceable units and authority ceilings.
- Interface: Evidence ratchets, readiness gates, and replacement transactions provide gates.
- Interface: Alignment and governance supply protected constraints, approval boundaries, and non-self-ratification rules.

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
- Exact Appendix C claim-source mappings for the core recursive-self-improvement claim across SCF stable fields, Benchmaxxing benchmark-ratchet discipline, RMI modular improvement loops, Alignment Field normative caution, VIEA durable artifact/feedback discipline, Talos typed jobs/audit/replay, MoECOT runtime-reference context, Field of God AI Constitution protected constraints, and Theseus self-evolution/readiness-gate notes; six local mappings (`scf`, `benchmaxxing`, `rmi`, `alignment_field`, `viea`, `talos`) now have reviewed passage references, while `moecot` remains connector-only/source-note mapped and the constitution/Theseus mappings remain public-project/source-note mapped until raw source is vendored or made durable in this project. Support remains `argument` pending protected-invariant tests, evaluator-independence scenarios, rollback/canary execution evidence, fresh Theseus report inspection, or accepted evidence transitions.
- Planned Codex test: Protected-invariant preservation test.
- Planned Codex test: Evaluator independence test.
- Planned Codex test: Self-improvement rollback scenario.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:self_improvement.boundary.operational_invariant` | `AsiStackProofs.SelfImprovement` | An improvement transition preserves all protected invariants. | implemented |
| `lean:self_improvement.boundary.failure_blocks_promotion` | `AsiStackProofs.SelfImprovement` | A proposal evaluated only by the component being replaced cannot be promoted. | implemented |

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
- Exact Appendix C claim-source mappings for the core intent-to-execution claim across VIEA intent/artifact/runtime feedback discipline, Talos typed-job/audit/replay discipline, Software Magic Grimoire command-envelope vocabulary, GenesisCode proposal/effect/provenance boundaries, and MoECOT runtime-reference context; four local mappings (`viea`, `talos`, `software_magic_grimoire`, `genesiscode`) now have reviewed passage references, while `moecot` remains connector/source-note mapped until usable raw text, code, logs, release artifacts, or benchmark records are imported or inspected. Support remains `argument` pending contract-completeness tests, constraint-preservation tests, artifact-traceability tests, approval/runtime enforcement evidence, replayed vertical-slice artifacts, or accepted evidence transitions.
- Planned Codex test: Contract field completeness test.
- Planned Codex test: Constraint preservation test.
- Planned Codex test: Artifact traceability test.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:intent_execution.contracts.operational_invariant` | `AsiStackProofs.IntentToExecution` | A compiled execution job preserves the parent contract constraints. | implemented |
| `lean:intent_execution.contracts.failure_blocks_promotion` | `AsiStackProofs.IntentToExecution` | An execution job without required approval cannot transition to running. | implemented |

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
- Exact Appendix C claim-source mappings for the core command-contract claim across Software Magic Grimoire command-envelope vocabulary, VIEA structured command layers, GenesisCode protocol/effect boundaries, Cognitive Compilation source-plan/S-IR lowering, and Talos typed-job contract discipline; all five local mappings (`software_magic_grimoire`, `viea`, `genesiscode`, `cognitive_compilation`, `talos`) now have reviewed passage references. Support remains `argument` pending command parser tests, dispatch-blocking tests, prompt-override scenarios, semantic-extraction quality checks, or accepted evidence transitions.
- Planned Codex test: Command schema validation test.
- Planned Codex test: Failure-behavior declaration test.
- Planned Codex test: Prompt override scenario.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:command.semantic_interface.operational_invariant` | `AsiStackProofs.CommandContracts` | A valid command contract contains objective, constraints, output contract, verification, and failure behavior. | implemented |
| `lean:command.semantic_interface.failure_blocks_promotion` | `AsiStackProofs.CommandContracts` | A hidden or conflicting instruction cannot override an explicit contract constraint. | implemented |

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
- Exact Appendix C claim-source mappings for the planning-control claim across PlanForge planning middleware, VIEA orchestration/runtime spine, Cognitive Compilation source-plan/S-IR pipeline, Software Magic Grimoire spell-stack workflow discipline, and MoECOT runtime-reference context; the four local mappings (`planforge`, `viea`, `cognitive_compilation`, `software_magic_grimoire`) now have reviewed passage references. `moecot` remains connector/source-note mapped until usable raw text, code, logs, release artifacts, or benchmark records are imported or inspected. Support remains `argument` pending planner harnesses, dependency-order checks, context-demand tests, runtime replanning traces, or accepted evidence transitions.
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
- Exact Appendix C claim-source mappings for the PlanForge DAG claim across PlanForge DAG/MVI scheduling, PlanForge compiler-architecture framing, Coherence Exchange speculative intelligence-arbitrage framing, Cognitive Compilation semantic-DAG routing/repair, TokenMana resource-governance pressure, and MoECOT runtime-reference context; the four local mappings (`planforge`, `planforge_compiler_arch`, `cognitive_compilation`, `tokenmana`) now have reviewed passage references. `coherence_exchange` and `moecot` remain connector/source-note mapped until usable raw text, code, logs, release artifacts, benchmark records, simulations, or external corroboration are imported or inspected. Support remains `argument` pending deployed scheduler runs, route traces, tier-adequacy tests, cost-quality results, or accepted evidence transitions.
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
- Exact Appendix C claim-source mappings for the Cognitive Compilation claim across Cognitive Compilation S-IR/repair architecture, PlanForge compiler-orchestration framing, GenesisCode evidence-carrying IR/provenance discipline, TreeLLM external semantic-substrate intuition, and VIEA intent-to-artifact ledger context; all five local mappings now have reviewed passage references. Support remains `argument` pending compiler traces, source-plan parsing, target-lowering preservation, validator adequacy, localized-repair results, quality/cost measurements, or accepted evidence transitions.
- Planned Codex test: Requirement preservation test.
- Planned Codex test: Incremental repair regression test.
- Planned Codex test: Target compilation audit.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:cognitive_compilation.ir.operational_invariant` | `AsiStackProofs.CognitiveCompilation` | A compiled artifact preserves all required IR obligations. | implemented |
| `lean:cognitive_compilation.ir.failure_blocks_promotion` | `AsiStackProofs.CognitiveCompilation` | A repair that invalidates an existing obligation cannot be accepted without updating the ledger. | implemented |

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
- Exact Appendix C claim-source mappings for the Virtual Context ABI claim across VCM public-v1 control-plane/ABI vocabulary, Context Engineer context-supply-chain pressure, Verification Bandwidth adequacy limits, VIEA context allocation and execution-spine integration, editable VCM refinement context, and MoECOT runtime-reference context; the four local mappings (`vcm_public`, `context_engineer`, `verification_bandwidth`, `viea`) now have reviewed passage references. `vcm_editable` and `moecot` remain connector/source-note mapped until usable raw text, code, logs, conformance artifacts, benchmark records, or external corroboration are imported or inspected. Support remains `argument` pending resolver behavior, adequacy classification, context compiler traces, VCM conformance artifacts, model-facing results, benchmark reproduction, or accepted evidence transitions.
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
- Exact Appendix C claim-source mappings for the Semantic Pages claim across VCM public-v1 context cells/semantic pages/representation certificates, Verification Bandwidth summary-loss pressure, Spinoza proof/citation/procedure-carrying claim records, Context Engineer structured mission briefs and clearance fields, and editable VCM refinement context; the four local mappings (`vcm_public`, `verification_bandwidth`, `spinoza`, `context_engineer`) now have reviewed passage references. `vcm_editable` remains connector/source-note mapped until usable raw text, conformance artifacts, certificate checker results, benchmark records, or external corroboration are imported or inspected. Support remains `argument` pending paired source/derived cells, summary-fidelity tests, omission-completeness checks, certificate truthfulness tests, open-domain formalization evidence, or accepted evidence transitions.
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
- Exact Appendix C claim-source mappings for the Context Transactions claim across VCM public-v1 transaction/snapshot/invalidation/deletion semantics, Ladon/Manhattan sensitive-compartment and handle boundaries, Context Engineer clearance-labeled mission contexts and Digital SCIF lifecycle, Black Hole Context Manager memory-budget/drift/freeze/evict patterns, and editable VCM refinement context; the four local mappings (`vcm_public`, `ladon_manhattan`, `context_engineer`, `black_hole_context_manager`) now have reviewed passage references. `vcm_editable` remains connector/source-note mapped until usable raw text, memory-store artifacts, conformance results, VCM-Bench records, or external corroboration are imported or inspected. Support remains `argument` pending memory-store behavior, mount-visibility tests, branch-isolation checks, deletion-closure harnesses, side-channel validation, context-manager execution, benchmark reproduction, or accepted evidence transitions.
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
- Exact Appendix C claim-source mappings for `verification-bandwidth-and-context-adequacy.core` across Verification Bandwidth, VCM public v1, Spinoza, TreeLLM, and editable VCM; four local raw-cache mappings are passage-reviewed, while `vcm_editable` remains connector/source-note mapped.
- Implemented protocol validation: `context_adequacy_record` fixture validates public record shape only.
- Planned Codex test: Distractor resistance test.
- Planned Codex test: Adequacy labeling test.
- Planned Codex test: Verification escalation test.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:verification_bandwidth.adequacy.operational_invariant` | `AsiStackProofs.VerificationBandwidth` | A context packet admitted for use may still be marked inadequate for a target claim. | implemented |
| `lean:verification_bandwidth.adequacy.failure_blocks_promotion` | `AsiStackProofs.VerificationBandwidth` | A high-risk claim with inadequate context cannot receive a verified support label. | implemented |

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
- Mechanism: Convert admitted context and generated prose into durable claim records with evidence refs, support state, uncertainty, contradiction refs, and revision history.
- Mechanism: Treat belief revision as support-state change, downgrade, split, merge, residual creation, or tribunal escalation rather than promotion-only bookkeeping.
- Handoff: Selected high-value claims flow to Spinoza for proof-, citation-, or procedure-carrying justification envelopes.
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
- Exact Appendix C claim-source mappings for `claim-ledgers-and-belief-revision.core` across Spinoza, VIEA, Coherence Exchange, Aletheia, and UAT; four local raw-cache mappings are passage-reviewed, while `coherence_exchange` remains connector/source-note mapped.
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
- Mechanism: Wrap selected ledger claims in proof-carrying or justification-carrying envelopes that include required tier, interpretation mapping, justification artifact, verifier result, limitations, downgrade rule, and residual route.
- Mechanism: Separate neural proposal from verifier judgment, so failed, timed-out, or mismatched verification lowers confidence or escalates instead of becoming a success story.
- Handoff: Claims whose mapping, stakes, or evidence conflict exceed one verifier move to UAT.
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
- Exact Appendix C claim-source mappings for `spinoza-verification-and-proof-carrying-claims.core` across Spinoza, GenesisCode, Coherence Exchange, Verification Bandwidth, and TreeLLM; four local raw-cache mappings are passage-reviewed, while `coherence_exchange` remains connector/source-note mapped.
- Implemented protocol validation: `proof_carrying_claim` fixture validates public record shape only.
- Planned Codex test: Proof artifact presence test.
- Planned Codex test: Tier assignment test.
- Planned Codex test: Formalization mismatch review.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:spinoza.proof_carrying.operational_invariant` | `AsiStackProofs.ProofCarryingClaims` | A claim at a formal support tier carries a valid proof or justification artifact reference. | implemented |
| `lean:spinoza.proof_carrying.failure_blocks_promotion` | `AsiStackProofs.ProofCarryingClaims` | A failed verifier result downgrades or blocks the claim rather than promoting it. | implemented |

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
- Mechanism: Escalate contested or high-risk claims into bounded tribunal records with dossier refs, reviewer roles, adversarial probes, evidence-linked findings, dissent, unresolved issues, verdict, and required actions.
- Mechanism: Preserve review boundaries by requiring dossier-scoped evidence, hard cycle caps, and human adjudication where risk or uncertainty remains.
- Handoff: Accepted or blocked outcomes flow back into the claim ledger and execution layers as tier decisions, residuals, required actions, or human sign-off.
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
- Exact Appendix C claim-source mappings for `unified-adaptive-tribunal-and-adversarial-review.core` across UAT, Spinoza, Coherence Exchange, Talos, and Verification Bandwidth; four local raw-cache mappings are passage-reviewed, while `coherence_exchange` remains connector/source-note mapped.
- Implemented protocol validation: `tribunal_review_record` fixture validates public record shape only.
- Planned Codex test: Adversarial review coverage test.
- Planned Codex test: Dissent preservation test.
- Planned Codex test: Consensus evidence test.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:tribunal.review.operational_invariant` | `AsiStackProofs.Tribunal` | A tribunal verdict includes reviewer roles, evidence references, and unresolved dissent. | implemented |
| `lean:tribunal.review.failure_blocks_promotion` | `AsiStackProofs.Tribunal` | A high-risk artifact cannot be accepted when required tribunal review is absent. | implemented |

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
- Mechanism: Convert accepted plans and required actions into typed job packets with contract lock, lifecycle state, permissions, approval gates, expected artifacts, failure behavior, audit trail, and replay expectations.
- Mechanism: Keep orchestration, workspace setup, access control, secret isolation, adapter invocation, adjudication, delivery, feedback, and replay as separate execution boundaries.
- Handoff: Delivered, failed, or blocked jobs flow into artifact graphs as durable work products and audit traces.
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
- Exact Appendix C claim-source mappings for `labor-os-and-typed-jobs.core` across Talos, VIEA, GenesisCode, Software Magic Grimoire, Talos Markdown, and MoECOT; four local raw-cache mappings are passage-reviewed, while `talos_md` and `moecot` remain connector/source-note mapped.
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
- Mechanism: Record artifacts as stable, versioned nodes with parent job, source/context/tool refs, claim/test links, audit events, replay metadata, environment assumptions, provenance status, and replay limits.
- Mechanism: Treat incomplete provenance as a residual while using verified and failed traces as inputs to evidence ledgers, regression suites, and procedural-memory candidates.
- Mechanism: Distinguish storage identity from evidential continuity: a path records where bytes live, while an artifact node records role, provenance, replay grade, residuals, and claim/test relevance.
- Mechanism: Treat replay as graded rather than binary: byte-for-byte replay, semantic replay, partial replay, and non-replayability must be declared before artifact reuse can affect evidence state.
- Handoff: Runtime adapters produce effect receipts and residuals that must return to the artifact graph before they become evidence.
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
- Passage-reviewed Appendix C mappings for six local raw-cache sources: `talos`, `viea`, `cognitive_compilation`, `spinoza_composer`, `genesiscode`, and `cognitive_loop_closure`; `moecot` remains connector/source-note mapped until durable runtime artifacts, ledgers, logs, benchmark records, or replay records are imported and inspected.
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
- Mechanism: Map typed jobs to runtime adapters with declared target type, capability, permission requirement, sandbox mode, authority handle, approval state, input/output contract, and effect receipt.
- Mechanism: Fail closed for high-impact actions without approval and return rollback handles or residuals for the artifact graph.
- Mechanism: Treat approval as a scoped, expiring, reviewable artifact and adapter execution as a narrow effect lease rather than ambient tool authority.
- Handoff: Repeated adapter traces and repair patterns become candidates for procedural memory only after evidence and regression checks exist.
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
- Exact Appendix C claim-source mappings for `runtime-adapters-tool-permissions-and-human-approval.core` across Talos, VIEA, Ladon/Manhattan, Software Magic Grimoire, GenesisCode, MoECOT, Field of God AI Constitution, and Theseus Operator OS; five local raw-cache mappings and two local public-project mappings are passage-reviewed, while `moecot` remains connector/source-note mapped.
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
- Mechanism: Use artifact traces to detect recurring loops only after enough comparable examples exist to avoid anecdotal toolification.
- Mechanism: Abstract invariant structure, discover parameters, record preconditions/postconditions, synthesize candidate tools, verify them, attach regressions and monitoring, then promote, quarantine, revise, or retire.
- Mechanism: Treat procedural memory as verified reuse, not habit: comparable successes, near misses, failures, negative examples, scope limits, and retirement criteria must travel with the tool card.
- Mechanism: Bind generated tools back to SCF boundaries and benchmark floors so tool promotion, routing, monitoring, and retirement remain governed by field identity and regression evidence.
- Handoff: Verified procedural tools become routable candidates for Part III, while failed or uncertain loops remain residuals.
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
- Exact Appendix C claim-source mappings for procedural memory: five local raw-cache mappings and three local public-project mappings are passage-reviewed, while `moecot` remains connector/source-note mapped only.
- Implemented protocol validation: `procedural_tool_record` fixture validates public record shape only.
- Planned Codex test: Loop detection test.
- Planned Codex test: Tool abstraction test.
- Planned Codex test: Verified tool regression test.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:procedural.loop_closure.operational_invariant` | `AsiStackProofs.ProceduralMemory` | A generated tool records its source traces, parameters, and verification result. | implemented |
| `lean:procedural.loop_closure.failure_blocks_promotion` | `AsiStackProofs.ProceduralMemory` | A tool with failed regression cannot be promoted to routable status. | implemented |

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
- Mechanism: Treat routing as a task-local authority lease over registered specialists with capability, cost, readiness, authority, memory, tool, fallback, residual, and evidence metadata.
- Mechanism: Select the smallest adequate specialist only after capability, authority, readiness, and fallback predicates are explicit.
- Handoff: Failed or uncertain routes flow to readiness gates, residual escrow, fallback routes, or tribunal/review rather than ordinary execution.
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
- Exact Appendix C claim-source mappings for routing heads: five local raw-cache mappings and two local public-project mappings are passage-reviewed, while `moecot` remains connector/source-note mapped only.
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
- Mechanism: Maintain lifecycle states and readiness gates that separate semantic fit from ordinary routability.
- Mechanism: Keep gate evidence, regression preservation, and residual escrow attached to modules through promotion, quarantine, split, merge, retirement, or retraining.
- Handoff: Runtime references such as MoECOT must emit the gate, replay, benchmark, residual, and promotion-blocker records that readiness decisions require.
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
- Exact Appendix C claim-source mappings for readiness gates: five local raw-cache mappings and three local public-project mappings are passage-reviewed, while `moecot` remains connector/source-note mapped only until runtime/source artifacts, readiness records, ledgers, replay logs, benchmark records, or external corroboration are imported and inspected.
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
- Mechanism: Treat MoECOT as a runtime evidence-packet target that binds command, route head, specialist cores, control-plane gates, ledgers, readiness refs, replay refs, handoff state, promotion blockers, residuals, and source-claim state.
- Mechanism: Keep direct MoECOT claims conservative until runtime artifacts, replay records, benchmark records, or reproduced local runs exist.
- Handoff: A concrete runtime must still land on an owned, leased, or project compute substrate whose reachability does not imply authority.
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
| `lean:moecot.runtime.operational_invariant` | `AsiStackProofs.MoECOTRuntime` | A runtime core promotion requires readiness, regression, and replay evidence references. | implemented |
| `lean:moecot.runtime.failure_blocks_promotion` | `AsiStackProofs.MoECOTRuntime` | A runtime claim sourced only from unavailable text cannot be promoted above argument state. | implemented |

### Personal Compute Hives and Federated Edge Intelligence

Stable ID: `personal-compute-hives-and-federated-edge-intelligence`

Chapter job: The architecture needs an owned compute-substrate chapter for phones, laptops, desktops, NAS devices, old machines, project runners, and rented nodes as policy-bounded participants in one personal or project hive.

Core claim: A Personal Compute Hive should turn trusted devices, portals, stores, workers, and temporary rented or project nodes into a federated, policy-bounded compute organism whose scheduler routes work by capability, locality, trust, cost, energy, and authority.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `vcm_public`, `talos`, `octopus_router`, `project_theseus_whitepaper` | Read first for governed context packets, typed jobs, routed specialists, and trusted-machine Hive/node framing. |
| Supporting | `field_of_god_ai_constitution`, `scf`, `planforge`, `rmi`, `tokenmana`, `theseus_operator_os`, `ladon_manhattan` | Mine after primary sources for consent, capability leases, scheduling, residuals, capacity accounting, operator surfaces, and secret-handle boundaries. |
| External source-note records | `ext_tailscale_docs_2025`, `ext_kubernetes_overview_docs`, `ext_k3s_docs_2026`, `ext_nomad_docs`, `ext_ray_core_docs_2026`, `ext_boinc_home_2026`, `ext_syncthing_home`, `ext_ipfs_docs`, `ext_akash_docs_2026`, `ext_golem_docs_2025`, `ext_github_self_hosted_runners_docs` | Load after internal sources to ground adjacent substrate/tooling patterns. Treat them as external context, not as proof that the personal hive exists or is safe. |
| Handoff or recovery notes | `sources/inbox/personal_compute_hives_browser_note_2026-06-25/` | Local-only author-intent context. Do not quote verbatim or promote claims from this packet. |
| Remaining external queue | secret-management systems, sandbox runtimes, family safety/tutoring systems, local-first databases, privacy-preserving computation | Add source records and source notes before citation or support-state promotion. |

Draft arc:

- Problem: A governed ASI stack needs an owned substrate where personal, family, project, and rented devices can run work without collapsing reachability into authority.
- Insufficiency: Cloud assistants, single-device agents, home clusters, and generic schedulers do not preserve identity, privacy, family authority, data locality, physical-tool risk, federation boundaries, and evidence records as one governed layer.
- Mechanism: Define `DeviceResourceCard`, `PortalCard`, `HiveJobContract`, `HiveJobBid`, `HiveSchedulingDecision`, `HiveApprovalReceipt`, and `HiveFederationLease` records so portals, workers, stores, rented nodes, and project machines are represented without sharing one trust class.
- Mechanism: Reject nodes by identity, data, tool, network, approval, family, project, or federation policy before scoring speed, cost, locality, energy, or capability.
- Mechanism: Preserve family-sensitive, project-hive, rented-node, artifact-steward, and memory-placement flows as mediated contracts with approvals, data-placement decisions, residuals, revocation paths, and distinct retention rules.
- Handoff: The hive creates pressure for compact generation, but compression claims remain governed by residual burden, verification cost, fallback, and source/test evidence.
- Interface: VCM declares context, taint, adequacy, revocation, and data movement.
- Interface: Talos and PlanForge lower goals into typed jobs and dependency-aware schedules.
- Interface: Octopus/RMI routing and SCF leases define which capability on which node may be selected.
- Interface: TokenMana-style resource records account for compute, money, energy, human attention, and friction.
- Interface: Field-of-God and Ladon/Manhattan boundaries preserve consent, least sufficient power, family governance, and secret handles.

Primary invariants:

- Reachability is not authority.
- Policy filtering precedes optimization.
- A device must be eligible for the job's data, tool, network, and approval scope before it can bid.
- External work receives sandboxed leases, not private network access.
- Family and child-facing portals preserve dignity, consent boundaries, and guardian review for sensitive transitions.
- Secrets remain handles and approvals, not strings in model context.
- Temporary federation links expire and can be revoked.

Failure modes to cover:

- Personal hive becomes a botnet or malware execution surface.
- Family governance becomes surveillance.
- Rented or public project compute leaks private data.
- Wrong-device scheduling drains batteries, overheats machines, exposes data, or bypasses approvals.
- Identity confusion grants child, guest, agent, or project authority to the wrong principal.
- Hive memory becomes an ungoverned swamp of artifacts, logs, models, and personal data.

Draft deliverables:

- A full chapter with hive object records, policy-first scheduling diagram, job classes, federation modes, H2H protocol surface, implementation ladder, public-safe source boundary, and external-source-note queue.
- Implemented repository-level fixtures: `device_resource_card.valid.json`, `portal_card.valid.json`, `hive_job_contract.valid.json`, `hive_job_bid.valid.json`, `hive_scheduling_decision.valid.json`, `hive_approval_receipt.valid.json`, and `hive_federation_lease.valid.json` validate record shape only; no personal hive scheduler, device registry, rented-node sandbox, or federation protocol has been run.
- Implemented Lean predicate: admitted hive jobs require identity, data, tool, federation, and approval checks.
- Implemented Lean predicate: a faster node forbidden by policy cannot be selected.
- Implemented Lean predicate: high-risk hive jobs that require approval require a bound approval receipt before execution.
- Implemented Lean predicate: external hive access requires active lease, scope, sandbox, evidence, expiration, and revocation records.
- Implemented Codex test: Device registry fixture validation through `validate_protocol_examples.py`.
- Implemented Codex test: Portal, approval, bid, and federation fixture validation through `validate_protocol_examples.py`.
- Implemented Codex test: Policy-first scheduling denial as a finite Lean predicate only.
- Planned Codex test: Data locality and rented-node denial test.
- Planned Codex test: Phone approval gate test.
- Planned Codex test: Child topic routing test.
- Planned Codex test: External project sandbox contract test.
- Planned Codex test: Audit replay test.
- Planned Codex test: Cross-router connectivity test.
- Planned Codex test: Job bidding test.
- Planned Codex test: Device dropout test.
- Planned Codex test: Energy-aware scheduling test.
- Planned Codex test: Portal continuity test.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:personal_hives.scheduling.operational_invariant` | `AsiStackProofs.PersonalComputeHives` | A hive scheduler admits a job only when identity, data, tool, federation, and approval policy checks pass before optimization. | implemented |
| `lean:personal_hives.policy_first.failure_blocks_promotion` | `AsiStackProofs.PersonalComputeHives` | A faster node cannot be selected when its policy membrane forbids the job's data, authority, or network scope. | implemented |
| `lean:personal_hives.approval_gate.failure_blocks_promotion` | `AsiStackProofs.PersonalComputeHives` | A high-risk hive job that requires approval cannot execute unless a bound approval receipt is present. | implemented |
| `lean:personal_hives.federation_lease.operational_invariant` | `AsiStackProofs.PersonalComputeHives` | External hive access requires an active lease with scope, sandbox, evidence, expiration, and revocation records. | implemented |

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
- Mechanism: Treat compactness as a governed claim over seed, rule system, memory state, generator/decoder/controller, verifier, residual channel, fallback path, governance interface, and evidence/cost ledger.
- Mechanism: Use the seed/router/search/generator/verifier/residual loop to expose generation cost, verification cost, correction burden, hidden complexity, and authority limits before promotion.
- Handoff: Exact reconstruction claims flow to generate-verify-repair receipts, while time-domain acceleration claims flow to fast-generation records.
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
- Mechanism: Record a compression receipt with reconstruction contract, public law family, seed, generated regions, verification result, exact repair residual, fallback threshold, rate accounting, and non-claims.
- Mechanism: Separate proxy/search-rate estimates from final serialized costs, and record literal fallback or negative results when repair and metadata erase the saving.
- Handoff: The same draft/verify/repair accounting becomes accepted-output and verifier-cost accounting in fast generation.
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
| External literature variants | `ext_speculative_decoding_2022`, `ext_multi_token_prediction_2024`, `ext_medusa_2024`, `ext_eagle_2024`, `ext_lookahead_decoding_2024`, `ext_layerskip_2024`, `ext_pagedattention_vllm_2023`, `ext_mamba_2023`, `ext_llada_2025`, `ext_scaling_dllms_2026` | Read after internal sources to ground the method taxonomy; treat reported results as source-reported until reproduced or independently checked. |
| Handoff or recovery notes | `sources/inbox/fast_generation_browser_note_2026-06-24/` | Local-only author-intent and external-literature queue context. Do not quote verbatim or promote claims from this packet. |

External literature queue:

| Area | Expected role | Status |
|---|---|---|
| Multi-token prediction and future-token heads | Compare MTP as a draft/proposal mechanism for breaking strict one-token-per-step generation. | source-noted via `ext_multi_token_prediction_2024`; no local model or benchmark |
| Speculative decoding and speculative sampling | Compare draft-model proposal plus target-model verification to the stack's generate-verify-repair pattern. | source-noted via `ext_speculative_decoding_2022`; no local acceptance benchmark |
| Multi-head decoding and feature-level drafting | Compare Medusa/EAGLE-style internal drafting and latent-state proposal mechanisms. | source-noted via `ext_medusa_2024` and `ext_eagle_2024`; no local head or feature-draft run |
| Lookahead, trie retrieval, and branch verification | Compare cached branch proposal, retrieval, and verification as procedural-memory acceleration. | lookahead source-noted via `ext_lookahead_decoding_2024`; trie retrieval remains unmined |
| Diffusion language models and arbitrary-order generation | Compare parallel denoising, infilling, sketch-first decoding, and quality-speed controls. | source-noted via `ext_llada_2025` and `ext_scaling_dllms_2026`; no local diffusion benchmark |
| Early exit and self-speculative inference | Compare cheap intermediate exits with later-layer verification. | source-noted via `ext_layerskip_2024`; no local early-exit run |
| State-space and recurrent sequence models | Compare sequence-processing efficiency as a different speed axis from multi-token acceptance. | source-noted via `ext_mamba_2023`; no local substrate A/B run |
| KV-cache and serving-layer accelerators | Compare memory-bandwidth and throughput improvements separately from single-request latency. | source-noted via `ext_pagedattention_vllm_2023`; no local serving benchmark |

Draft arc:

- Problem: The stack needs to reduce serial token-generation latency without treating raw tokens per second as intelligence or bypassing verification.
- Insufficiency: Standard autoregressive decoding, raw throughput benchmarks, and isolated serving optimizations do not specify when a faster generation mode is acceptable, how it is verified, or how its failures block promotion.
- Mechanism: Treat fast generation as a governed mode route selected by PlanForge from task requirements, risk tier, latency budget, context shape, memory pressure, and verifier availability.
- Mechanism: Count proposed output separately from accepted output, include verifier cost, repair/fallback, useful solution per second, and promotion decision, and keep external method families source-reported until reproduced or promoted by evidence transition.
- Handoff: Accepted generation outputs become artifacts or compressed candidates; rejected work and serving/KV pressure flow to artifact and resource ledgers.
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
- Speculative, diffusion, MTP, and hybrid claims remain at argument level until source-specific tests, reproduced results, or accepted external-literature support justify promotion.

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
- Mechanism: Treat compressed artifacts as routed representation candidates with preserved full-artifact fallback, reconstruction contract, codec parameters, residual coding, probe plan, decode determinism, utility tests, and non-claims.
- Mechanism: Separate representation, reconstruction, compression-ratio, and downstream-utility claims so one passing property cannot promote the others.
- Mechanism: Keep compression, reconstruction, residual, utility, cost, and fallback ledgers separate so a smaller representation cannot silently become a stronger evidence object.
- Mechanism: Require compressed records to state the declared use envelope, probe boundary, fallback trigger, and non-claims before downstream agents can use the compressed form.
- Handoff: Semantic representation inherits the same probe discipline, but the risk shifts from bit-level reconstruction to grounding and hierarchy drift.
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
| `lean:compression.artifacts.operational_invariant` | `AsiStackProofs.ArtifactCompression` | A compressed artifact used for a task must pass that task probe or route to fallback. | implemented |
| `lean:compression.artifacts.failure_blocks_promotion` | `AsiStackProofs.ArtifactCompression` | A compression record cannot omit residual or fallback metadata. | implemented |

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
- Mechanism: Treat semantic nodes as scoped representation leases with concept labels, provenance, hierarchy/relation refs, tokenization contracts, grounding state, permitted uses, residual uncertainty, versioning, and evaluation refs.
- Mechanism: Use tree or graph structure for retrieval, planning, compilation, and explanation only where grounding, adequacy, interoperability, and baseline comparisons justify the route.
- Mechanism: Separate grounding, adequacy, and interoperability gates so hierarchy or compact semantic tokens cannot stand in for source support, task fit, or cross-layer usability.
- Mechanism: Preserve provenance and supersession links so semantic graphs remain indexes and working representations rather than unreviewed authority sources.
- Handoff: Resource economics decides when semantic compression is actually cheaper after verification burden, repair, and downstream failures are counted.
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
| `lean:representation.semantic_tree.operational_invariant` | `AsiStackProofs.SemanticRepresentation` | A semantic node marked grounded has at least one provenance link. | implemented |
| `lean:representation.semantic_tree.failure_blocks_promotion` | `AsiStackProofs.SemanticRepresentation` | A hierarchy update preserves prior node references or records supersession. | implemented |

### Resource Economics and Token Budgets

Stable ID: `resource-economics-and-token-budgets`

Chapter job: Compute, context, verification, and human attention are scarce resources that the architecture must allocate explicitly.

Core claim: The stack should account for token budgets, verification tax, load stability, and risk-adjusted inference value.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `tokenmana`, `planforge` | Read first for chapter claims and mechanisms. |
| Supporting | `coherence_exchange`, `simulation_scaling`, `viea`, `project_theseus_whitepaper`, `coilra_multicoil_rope` | Mine after primary sources for cross-layer connections, variants, and failure modes. |
| External literature variants | `ext_pagedattention_vllm_2023` | Read for KV-cache memory, batching, and serving-throughput accounting; treat reported serving results as source-reported until reproduced. |

Draft arc:

- Problem: Compute, context, verification, and human attention are scarce resources that the architecture must allocate explicitly.
- Insufficiency: Ignoring resource economics makes high-quality verification unaffordable and encourages synchronized overload or hidden cost shifts.
- Mechanism: Record value hypothesis, risk class, capacity pool, cost estimate, verification tax, serving pressure, protected gates, budget decision, escalation rule, residuals, and evidence refs.
- Mechanism: Let budgets choose dispatch, escalation, deferral, scope reduction, rejection, or residual accounting without disabling protected verification or safety gates.
- Handoff: Simulation, mathematical, cyclic, and search substrates enter only through resource, fidelity, baseline, and evidence contracts rather than elegance or apparent cheapness.
- Interface: Planning allocates budgets.
- Interface: Routing chooses costed specialists.
- Interface: Evidence measures cost-quality tradeoffs.
- Interface: Serving infrastructure reports memory and throughput costs without converting them into quality claims.

Primary invariants:

- Budgets do not override protected safety gates.
- High-risk tasks pay verification cost.
- Cost savings are recorded with quality results.
- Serving-throughput gains remain separate from verified-output and task-success claims.

Failure modes to cover:

- Cost-cutting verification away.
- Load-synchronized degradation.
- Resource hoarding by low-value tasks.
- Aggregate serving throughput mistaken for lower single-request risk or better answer quality.

Draft deliverables:

- A resource ledger with budget, risk, cost, quality, and verification tax fields.
- Implemented repository-level fixture: `resource_budget_record.valid.json` validates the budget-record shape only; no TokenMana simulation, PlanForge scheduler benchmark, or welfare/load study exists yet.
- Planned Codex test: Budget allocation test.
- Planned Codex test: Risk-adjusted verification test.
- Planned Codex test: Load stability scenario.
- Planned Codex test: KV-cache memory accounting scenario.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:resources.budgets.operational_invariant` | `AsiStackProofs.ResourceEconomics` | A task budget cannot disable required safety or verification gates. | implemented |
| `lean:resources.budgets.failure_blocks_promotion` | `AsiStackProofs.ResourceEconomics` | A high-risk task with insufficient verification budget is blocked or escalated. | implemented |

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
- Mechanism: Turn every simulator, synthetic benchmark, or nested-world scenario into a contract with declared scope, clockspeed, fidelity, temporal semantics, resource demand, approximation liberties, and supported-claim boundary.
- Mechanism: Use the contract to decide whether a simulation supports a unit invariant, a bounded benchmark, a roadmap constraint, or only a speculative scenario note.
- Mechanism: Route failed or under-specified simulation claims into residuals, reduced scope, or blocked status instead of treating approximate worlds as ground truth.
- Mechanism: Treat simulation as a translation problem whose results can travel back only along the declared variables, omissions, bottlenecks, and fidelity boundary.
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
| `lean:simulation.fidelity.operational_invariant` | `AsiStackProofs.SimulationFidelity` | A simulation claim includes declared scope, fidelity, and resource bounds. | implemented |
| `lean:simulation.fidelity.failure_blocks_promotion` | `AsiStackProofs.SimulationFidelity` | An experiment result cannot exceed the declared fidelity support of its simulation. | implemented |

### Mathematical and Search Substrates

Stable ID: `mathematical-and-search-substrates`

Chapter job: The source corpus contains exploratory mathematical/search substrates that may matter but must not be overclaimed.

Core claim: Coils, calculi, and geometric search belong in the stack as optional specialist substrates until tests show where they improve search, routing, or compression.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `genesiscode`, `temporal_coil_research` | Read first for chapter claims and mechanisms. |
| Supporting | `cognitive_compilation`, `treellm`, `simulation_scaling`, `circle_calculus_core`, `circle_ai_architectures`, `proof_carrying_circular_computation`, `theseus_circle_transfer` | Mine after primary sources for cross-layer connections, variants, and failure modes. |
| External literature variants | `ext_mamba_2023` | Read for state-space/recurrent sequence-substrate context; treat reported model results as source-reported until reproduced. |
| Connector or recovery required | `coilmoecot` | Load via Google Drive connector or mark as blocked before source-derived claims. |

Draft arc:

- Problem: The source corpus contains exploratory mathematical/search substrates that may matter but must not be overclaimed.
- Insufficiency: Novel substrates can become authority theater if they are not tied to baselines, adoption gates, and falsification criteria.
- Mechanism: Register each coil, calculus, geometric, graph, compiler-IR, or state-space substrate as an exploratory candidate with intended use, authority boundary, and adoption state.
- Mechanism: Require expected advantage, ordinary baselines, negative controls, proof boundary, workload, metric, report, and falsification condition before canary use.
- Mechanism: Route experiments through exploratory, canary, qualified, retired, or blocked evidence gates before broader adoption.
- Mechanism: Keep backbone efficiency, proof readiness, fast-generation acceleration, compression, search quality, routing quality, and downstream task quality as separate axes.
- Mechanism: Treat optionality as a positive adoption state so promising substrates can be tested through narrow routes without becoming load-bearing architecture before evidence exists.
- Interface: Routing treats substrate as specialist.
- Interface: Compression tests representation efficiency.
- Interface: Evidence compares against baselines.
- Interface: Fast-generation routes may consume substrate evidence, but adoption remains gated by substrate-specific A/B records.

Primary invariants:

- Exploratory claims stay exploratory.
- Baselines are recorded.
- Failed hypotheses remain visible.
- Backbone-efficiency claims do not imply search, routing, compression, or reasoning-quality gains.

Failure modes to cover:

- Performance overclaiming.
- Opaque math treated as proof.
- Adoption without regression tests.
- Sequence-model throughput treated as evidence for unrelated substrate quality.

Draft deliverables:

- A technical-substrate appendix plan with experiment matrix and adoption gates.
- Implemented repository-level fixture: `substrate_adoption_record.valid.json` validates the substrate-adoption record shape only; no A/B run, representation-efficiency benchmark, CoilMoECOT benchmark, or local Circle build exists yet.
- Planned Codex test: Baseline comparison test.
- Planned Codex test: Representation efficiency test.
- Planned Codex test: Falsification review.
- Planned Codex test: Sequence-substrate A/B comparison test.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:substrates.search.operational_invariant` | `AsiStackProofs.SearchSubstrates` | A substrate adoption record includes baseline, measured target, and falsification criterion. | implemented |
| `lean:substrates.search.failure_blocks_promotion` | `AsiStackProofs.SearchSubstrates` | A substrate without passing evidence remains non-core. | implemented |

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
- Mechanism: Admit a finite circular address, schedule, window, or phase model only when the engineering object is faithfully represented at that boundary.
- Mechanism: Emit a proof-carrying receipt with theorem IDs, proof status, dictionary IDs, fingerprints, deterministic fields, validation commands, replay checks, consumer gates, and explicit non-claims.
- Mechanism: Preserve the receipt boundary in downstream consumers and require workloads, ordinary baselines, negative controls, metrics, scripts, and evidence artifacts before any quality, runtime, memory, or transfer claim is promoted.
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
- Mechanism: Represent memory slots, residue, winding, provenance, strides, sparse windows, freshness windows, and recurrence schedules as finite structural contracts.
- Mechanism: Expose alias, freshness, coverage, active-token, work-saving, fallback, stale-read, and loop-exit fields as auditable outputs with explicit non-claims.
- Mechanism: Preserve VCM authority and adequacy labels while comparing slot-only, slot-plus-winding, FIFO, LRU, content-gated, ordinary attention, and ordinary memory baselines before promoting retrieval, reasoning, speed, or memory claims.
- Mechanism: Keep structural memory facts separate from useful-memory claims, so freshness, coverage, and exits become diagnostic guardrails rather than retrieval-quality evidence.
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
| `lean:coil_memory.alias_boundary.operational_invariant` | `AsiStackProofs.CoilAttentionMemory` | A cyclic memory claim records residue and winding or marks aliasing as visible residual risk. | implemented |
| `lean:coil_attention.coverage_not_quality.failure_blocks_promotion` | `AsiStackProofs.CoilAttentionMemory` | Sparse coverage or freshness facts alone cannot promote a retrieval-quality claim. | implemented |

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
- Mechanism: Treat adapter blocks, block-cyclic routes, multiphase features, residue and winding, relative RoPE, circulant convolution, and route heads as structural contracts only where cyclic structure is real.
- Mechanism: Attach receipt boundaries, alias diagnostics, load diagnostics, parameter accounting, hardware-kernel notes, and real-valued-versus-discretized limits before interpreting model behavior.
- Mechanism: Promote the substrate only after quality, runtime, memory, parameter, transfer, and failure-case tradeoffs are measured against ordinary baselines and negative controls.
- Mechanism: Keep structural, resource, and empirical ledgers separate so exact cyclic facts, parameter accounting, and measured workload behavior cannot spend evidence credit for one another.
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
| `lean:cyclic_mixers.structural_not_quality.operational_invariant` | `AsiStackProofs.CyclicMixers` | A cyclic mixer claim records the structural invariant separately from quality, runtime, memory, and parameter claims. | implemented |
| `lean:cyclic_mixers.baseline_required.failure_blocks_promotion` | `AsiStackProofs.CyclicMixers` | A cyclic substrate cannot be promoted without ordinary baselines and recorded tradeoff metrics. | implemented |

## Part IV - Evidence, Implementation, and the Living Book

Part job: Turn the architecture into an accountable research program: executable specifications, Lean proof envelopes, benchmark ratchets, governed policy-update records, artifact stewardship, integrated reference traces, implementation roadmap, living-book method, and bibliography discipline.

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
- Mechanism: Lower each formal-looking chapter claim into a Proof Target Record with tag, module or artifact path, formal target, verifier command/result, support-state effect, limitations, and non-claims.
- Mechanism: Keep `proofs/proof_manifest.json` generated from outline `lean:*` tags and require traceability through triage records, Lean modules, root imports, chapter hooks, limitation prose, and Appendix E before calling a target implemented.
- Mechanism: Route candidates to Lean predicates, executable schemas, fixture validators, process contracts, research targets, blocked targets, or retired targets according to what can actually be checked.
- Mechanism: Keep semantic proof adequacy as a separate review from build success, schema success, source interpretation, deployed enforcement, model quality, or benchmark evidence.
- Mechanism: Treat the proof envelope as a lane discipline: Lean proves finite predicates, schemas validate record shape, process validators check wiring, tests exercise behavior, and benchmarks measure performance without collapsing those artifacts into one support state.
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
- Implemented repository-level fixture: `proof_target_record.valid.json` validates proof-target record shape only.
- Implemented Lean predicates: `AsiStackProofs.ProofEnvelope` proves local finite-record implemented-target and non-operational routing requirements without claiming broad system proof, source correctness, model quality, or benchmark evidence.
- Implemented generated audit: Appendix E summarizes all 112 proof targets by status, triage class, and recommended route from `proofs/proof_triage.json`.
- Implemented generated audit: `docs/proof_artifact_audit.md` checks that all 112 proof targets are traceable through manifest, triage, Lean module, root import, chapter hook, limitation prose, and Appendix E coverage; this is not a semantic adequacy review.
- Implemented Codex test: Proof manifest sync test.
- Implemented Codex test: Lake build smoke test.
- Implemented Codex test: Proof artifact traceability audit.
- Planned Codex test: Semantic proof adequacy audit.

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
- Mechanism: Convert every benchmark result into a ratchet record with command/run refs, environment, baseline, frontier state, mastery threshold, saturation state, residual escrow, regression refs, anti-Goodhart checks, promotion decision, support-state effect, and negative results.
- Mechanism: Generate regression floors, holdout checks, transfer checks, mutation checks, contamination checks, and public-calibration notes before using a benchmark to move readiness or claim support.
- Mechanism: Move residual failures into escrow, convert saturated tasks into regression floors, and create harder frontier tasks only when the prior evidence boundary survives review.
- Mechanism: Record source-reported, synthetic, empirical, negative, and inconclusive results as distinct evidence states rather than cleanup notes.
- Mechanism: Separate book-build checks, schema fixtures, synthetic examples, source-reported results, reproduced benchmarks, and empirical capability results before allowing any support-state movement.
- Mechanism: Attach ratchets to SCF boundaries and procedural tools so benchmark history preserves field-specific floors, tool retirement pressure, and claim-specific evidence scope.
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
| `lean:benchmarks.ratchet.operational_invariant` | `AsiStackProofs.BenchmarkRatchets` | A capability promotion requires benchmark evidence and preserved regression records. | implemented |
| `lean:benchmarks.ratchet.failure_blocks_promotion` | `AsiStackProofs.BenchmarkRatchets` | A saturated benchmark cannot be the sole basis for higher readiness promotion. | implemented |

### Policy Optimization and Learning from Feedback

Stable ID: `policy-optimization-and-learning-from-feedback`

Chapter job: A governed stack needs to convert feedback, verification, benchmark pressure, and failure into better future behavior without allowing reward signals to bypass evidence, authority, or rollback boundaries.

Core claim: Policy optimization is the stack's learning actuator: it can update planners, routers, context selectors, verifiers, execution policies, and generators, but governance decides which feedback is admissible and whether any update may be promoted.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `benchmaxxing`, `rmi` | Read first for benchmark pressure, residual escrow, capability ratchets, and regression floors. |
| Supporting | `spinoza`, `verification_bandwidth`, `talos`, `vcm_public`, `planforge`, `octopus_router`, `scf`, `tokenmana`, `cognitive_loop_closure` | Mine after primary sources for verifier rewards, context adequacy, execution artifacts, planner/router policies, governance gates, cost signals, and procedural loop closure. |
| External variants | `ext_trpo_2015`, `ext_ppo_2017`, `ext_remax_2023`, `ext_dpo_2023`, `ext_ipo_preference_2023`, `ext_orpo_2024`, `ext_kto_2024`, `ext_simpo_2024`, `ext_reinforce_style_rlhf_2024`, `ext_deepseek_r1_2025`, `ext_dapo_2025`, `ext_gspo_2025`, `ext_s_grpo_2025`, `ext_longrlvr_2026`, `ext_rlhf_limitations_2023` | Source-noted external method-family context for policy gradients, PPO/TRPO, preference optimization, reasoning RL, context rewards, and RLHF limitations; do not treat as local reproduction. |
| Connector or recovery required | `moecot` | Use only as implementation-reference context unless artifacts are imported or reproduced. |
| Handoff or recovery notes | `sources/inbox/policy_optimization_browser_note_2026-06-24/` | Local-only author-intent and external-literature queue context. Do not quote verbatim or promote claims from this packet. |

Draft arc:

- Problem: Feedback, verification, benchmark pressure, and failures need a governed path into future behavior.
- Insufficiency: RLHF, preference optimization, and verifier rewards are often framed as model fine-tuning recipes rather than stack-wide update mechanisms.
- Mechanism: Classify the target policy: planner, VCM, router, generator, verifier, execution, governance, generation mode, or whole-stack policy.
- Mechanism: Record the feedback source, reward/preference signal, verifier refs, update constraint, drift bound, evaluation refs, governance gates, rollback plan, residuals, and non-claims.
- Mechanism: Choose a training/update family by the policy being optimized, the feedback available, and the failure mode that must be blocked.
- Mechanism: Keep REINFORCE/RLOO/ReMax-style policy gradients, TRPO/PPO-style trust-region updates, GRPO/DAPO/GSPO-style group or sequence updates, DPO/IPO/ORPO/KTO/SimPO-style offline preference optimization, RLVR, reasoning-budget RL, router-policy RL, and context-policy RL as method families, not unsupported result claims.
- Interface: Benchmarks and verifiers produce reward or preference signals.
- Interface: VCM and artifact graphs preserve training/evaluation context and evidence references.
- Interface: Talos records training, tool, and evaluation artifacts.
- Interface: Spinoza and UAT audit reward meaning, failed verifiers, and reward-hacking probes.
- Interface: SCF gates decide promotion, quarantine, rollback, or continued experiment status.

Primary invariants:

- Reward is not evidence unless the verifier and evaluation boundary are recorded.
- Policy updates cannot expand authority by training side effect.
- A faster or shorter policy is not promoted unless task success and regressions are preserved.
- Reward-hacking probes are part of the update record, not optional commentary.
- Rollback remains available for promoted updates.

Failure modes to cover:

- Reward hacking or verifier gaming.
- Over-optimization for preference style rather than truth or task success.
- Planner, router, or context policies learning hidden shortcuts.
- Latency rewards suppressing needed verification.
- Policy drift crossing SCF authority or readiness boundaries.

Draft deliverables:

- A policy optimization record schema with target layer, feedback source, reward signal, verifier refs, update constraint, drift bound, evaluation refs, governance gates, rollback plan, residuals, and non-claims.
- Implemented repository-level fixture: `policy_optimization_record.valid.json` validates policy-update record shape only; no PPO, DPO, GRPO, RLVR, router-policy, context-policy, or reasoning-budget experiment has been run.
- Public-safe ingestion report: `docs/policy_optimization_context_ingestion_report.md`.
- External literature queue: initial source records and conservative source notes now exist for TRPO, PPO, ReMax, DPO, IPO/preference-learning theory, ORPO, KTO, SimPO, REINFORCE-style RLHF, DeepSeek-R1, DAPO, GSPO, S-GRPO, LongRLVR, and RLHF limitation work; process-reward work beyond LongRLVR remains queued.
- Planned Codex test: DPO/offline preference baseline test.
- Planned Codex test: PPO online RL baseline test.
- Planned Codex test: GRPO/RLOO toy math reward test.
- Planned Codex test: Verifier reward loop test.
- Planned Codex test: Length and latency penalty study.
- Planned Codex test: Reward-source admissibility test.
- Planned Codex test: Reward hacking probe test.
- Planned Codex test: Router policy toy RL test.
- Planned Codex test: Context-policy grounding reward test.
- Planned Codex test: Reasoning-budget penalty test.
- Planned Codex test: Rollback and promotion gate test.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:policy_optimization.update.operational_invariant` | `AsiStackProofs.PolicyOptimization` | An admitted policy update records target layer, reward signal, update constraint, evaluation refs, governance gates, and rollback plan. | implemented |
| `lean:policy_optimization.reward_boundary.failure_blocks_promotion` | `AsiStackProofs.PolicyOptimization` | A policy update with unverified reward or missing governance gate cannot be promoted. | implemented |

### Artifact Steward Agents and Living Project Governance

Stable ID: `artifact-steward-agents-and-living-project-governance`

Chapter job: The living architecture needs a project-lifecycle layer for durable artifacts that must preserve mission, memory, roadmap, budget, contributors, compute, evidence, governance, and sunset criteria across many human and AI work cycles.

Core claim: Every durable artifact should be able to carry a bounded steward agent that preserves mission, memory, roadmap, budget, contributors, compute, evidence, governance, and sunset policy across the artifact lifecycle while acting only through explicit work contracts, verification gates, treasury limits, contribution ledgers, and governance rules.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `viea`, `talos`, `planforge`, `vcm_public` | Read first for artifact discipline, typed jobs, roadmap decomposition, and project memory. |
| Supporting | `spinoza`, `benchmaxxing`, `rmi`, `cognitive_loop_closure`, `tokenmana`, `coherence_exchange`, `project_theseus_whitepaper`, `theseus_operator_os`, `scf`, `field_of_god_ai_constitution` | Mine after primary sources for proof/evidence gates, benchmark pressure, residual escrow, procedural tools, resource budgets, fork/exit/audit, work boards, capability leases, and non-domination constraints. |
| External source-note records | `ext_github_webhooks_docs`, `ext_github_self_hosted_runners_docs`, `ext_openzeppelin_governor_docs`, `ext_open_collective_docs`, `ext_github_sponsors_docs`, `ext_agentic_workflow_injection_2026`, `ext_dao_delegation_fairness_2025`, `ext_akash_docs_2026`, `ext_golem_docs_2025` | Load after internal sources to ground event-driven automation, self-hosted compute, governance machinery, fiscal-hosted treasury context, sponsorship surfaces, workflow-injection risk, delegation concentration, and rented-compute context. |
| Connector or recovery required | `coherence_exchange` | Use as speculative governance/economic framing unless exact source-note mappings and support boundaries are recorded. |
| Handoff or recovery notes | `sources/inbox/artifact_steward_agents_browser_note_2026-06-25/` | Local-only author-intent context. Do not quote verbatim or promote claims from this packet. |
| Remaining external queue | grants, bounty platforms, package-maintainer sustainability, software supply-chain security, legal/tax treatment of stewarded treasuries | Add source records and source notes before citation or support-state promotion. |

Draft arc:

- Problem: Durable artifacts need continuity across planning, funding, work assignment, release, maintenance, governance, and eventual sunset without turning an AI manager into the owner of the project.
- Insufficiency: Issue trackers, CI systems, bots, funding pages, governance systems, and project-management tools each preserve only a slice of the artifact lifecycle.
- Mechanism: Define `ArtifactStewardCharter`, `ProjectWorkContract`, `ContributionLedgerEntry`, `TreasuryPolicyRecord`, `EventTaintRecord`, `StewardActionDecision`, and `SunsetReviewRecord`.
- Mechanism: Bind the steward to mission, non-goals, authority ceiling, evidence policy, budget policy, governance model, and sunset criteria.
- Mechanism: Run an explicit lifecycle from inception to bootstrap, build, release, maintenance, governance, decline, and archive.
- Mechanism: Keep autonomy modes explicit: manual, assisted, bounded autonomous, community governed, and sunset.
- Mechanism: Convert roadmap work into bounded contracts before dispatching humans, agents, hives, CI runners, rented compute, reviewers, or maintainers.
- Mechanism: Keep treasury modes explicit: manual treasury, budgeted autonomy, bounty escrow, recurring operations, compute rental, governed treasury, and emergency freeze.
- Mechanism: Separate reputation, governance rights, economic compensation, authorship, and evidence credit so one gameable score cannot capture the project.
- Mechanism: Treat webhooks, issues, pull requests, comments, worker outputs, benchmark artifacts, and release events as typed and tainted intake until reviewed.
- Mechanism: Treat the steward's normal action as proposal, evidence preparation, and coordination rather than unilateral ownership.
- Mechanism: Model project-to-project federation and artifact economies through work contracts, evidence bundles, contribution ledgers, and sunset reviews rather than ambient project trust.
- Mechanism: Pair with Personal Compute Hives by requesting owned or rented execution only through contracts that the hive can independently reject on data, tool, family, physical-world, budget, or federation-policy grounds.
- Interface: VIEA and Talos connect intent, work contracts, artifacts, evidence, audit, replay, and delivery.
- Interface: PlanForge lowers project goals into dependency-aware work packages.
- Interface: VCM preserves project memory, taint, revocation, source refs, and open questions.
- Interface: Spinoza, Benchmaxxing, RMI, and Appendix C determine whether submitted work changes support, readiness, or regression state.
- Interface: TokenMana, SCF, Field-of-God governance, and fork/exit/audit rights bound spending, compute, authority, consent, and appeal.

Primary invariants:

- The steward is not the owner.
- The steward has no authority not grounded in the charter, a work contract, or explicit governance approval.
- Spending is a bounded actuator governed by treasury policy.
- Untrusted issues, pull requests, comments, worker outputs, and external prompts remain tainted until reviewed.
- Reputation, governance rights, economic compensation, authorship, and evidence credit remain separate ledgers.
- Human-readable maps, decision logs, release notes, and appeal paths remain available.
- Projects that meet sunset criteria enter sunset review rather than manufacturing activity.

Failure modes to cover:

- Mission drift from optimizing activity rather than purpose.
- Treasury drain through low-value compute, bounty spam, or recurring costs.
- Contribution gaming and reputation capture.
- Governance capture by large holders, early maintainers, or steward-controlled scoring.
- Agentic workflow injection through untrusted repository event context.
- AI maintainer monopoly that makes the project opaque to humans.
- Zombie project continuation after user value disappears.

Draft deliverables:

- A full chapter with steward lifecycle diagram, project record definitions, autonomy and treasury modes, implementation ladder, public-safe source boundary, external source-note queue, project-federation boundary, and event-taint boundary.
- Implemented repository-level fixtures: `artifact_steward_charter.valid.json`, `project_work_contract.valid.json`, `contribution_ledger_entry.valid.json`, `treasury_policy_record.valid.json`, `event_taint_record.valid.json`, `steward_action_decision.valid.json`, and `sunset_review_record.valid.json` validate record shape only; no steward bot, treasury executor, event-taint workflow, governance runner, or contributor system has been run.
- Implemented Lean predicate: dispatched steward work contracts require objective, authority, allowed tools, forbidden tools, verification requirements, budget, and non-claims.
- Implemented Lean predicate: protected steward actions without explicit approval evidence cannot execute.
- Implemented Lean predicate: stewarded release publication requires test, evidence, changelog, residual, and approval records.
- Implemented Lean predicate: sunset criteria block ordinary work generation until a sunset review opens.
- Implemented Codex test: Project steward manifest fixture validation through `validate_protocol_examples.py`.
- Implemented Codex test: Treasury policy and event-taint fixture validation through `validate_protocol_examples.py`.
- Implemented Codex test: Work contract authority denial as a finite Lean predicate only.
- Implemented Codex test: Treasury spend-cap/protected-action denial as a finite Lean predicate only.
- Planned Codex test: Untrusted event taint test.
- Planned Codex test: Contribution ledger separation test.
- Planned Codex test: Sunset criteria test.
- Planned Codex test: Release evidence handoff test.
- Planned Codex test: Project federation contract test.
- Planned Codex test: Autonomy-mode transition test.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:artifact_stewards.work_contract.operational_invariant` | `AsiStackProofs.ArtifactStewardAgents` | A steward-managed work contract records objective, authority, allowed tools, forbidden tools, verification requirements, budget, and non-claims before dispatch. | implemented |
| `lean:artifact_stewards.treasury_boundary.failure_blocks_promotion` | `AsiStackProofs.ArtifactStewardAgents` | A steward action that exceeds treasury policy, changes governance rules, or touches protected assets cannot execute without explicit approval evidence. | implemented |
| `lean:artifact_stewards.release_gate.operational_invariant` | `AsiStackProofs.ArtifactStewardAgents` | A stewarded release publication requires test, evidence, changelog, residual, and approval records. | implemented |
| `lean:artifact_stewards.sunset_review.failure_blocks_promotion` | `AsiStackProofs.ArtifactStewardAgents` | When sunset criteria are met, ordinary work generation is blocked until a sunset review is opened. | implemented |

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
- Mechanism: Represent the integrated stack as a Reference Trace Record that names intent, authority chain, layer handoffs, emitted artifacts, evidence updates, stop conditions, missing contracts, validation commands, support-state effect, and non-claims.
- Mechanism: Trace user intent through constitution, governance, planning, VCM, routing, verification, execution, evidence, compression/procedural loop closure, and SCF improvement gates without collapsing layer boundaries.
- Mechanism: Show the artifact emitted by each layer: command contract, plan DAG, context packet, route decision, claim envelope, work order, audit log, benchmark ledger, residual, or capability-field transition.
- Mechanism: Identify where authority can stop, narrow, reroute, quarantine, rollback, or require review before downstream work proceeds.
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
| `lean:reference_architecture.trace.operational_invariant` | `AsiStackProofs.ReferenceArchitecture` | An end-to-end trace contains required artifacts for each layer handoff. | implemented |
| `lean:reference_architecture.trace.failure_blocks_promotion` | `AsiStackProofs.ReferenceArchitecture` | A trace with a missing governance gate cannot be marked valid. | implemented |

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
- Mechanism: Treat source-note lineage, imported reports, reproduced runs, missing artifacts, and public non-claims as separate evidence categories so Theseus remains an implementation reference rather than laundered capability evidence.
- Mechanism: Extend the report crosswalk to human-control artifacts: originating intent contract, approval receipt, agency checklist, rollback/shutdown path, operator work-board item, and review residual.
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
| `lean:theseus.reference.report_contract.operational_invariant` | `AsiStackProofs.TheseusReference` | An implementation-reference claim names the report, config, or tool surface and does not rely on dashboard prose alone. | implemented |
| `lean:theseus.reference.gate_before_promotion.failure_blocks_promotion` | `AsiStackProofs.TheseusReference` | A capability or self-evolution promotion is blocked when required gate reports are absent or failing. | implemented |

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
- Mechanism: Represent each build phase with a Prototype Phase Record naming deliverables, required artifacts, acceptance gates, blockers, validation commands, evidence refs, non-claims, and status.
- Mechanism: Start with source inventory, source notes, claim ledger, artifact graph, schemas, proof manifest, validation, and release discipline before introducing autonomous action.
- Mechanism: Add intent contracts, PlanForge DAGs, VCM context records, typed jobs, runtime adapters, audit/replay, procedural memory, routing, readiness gates, benchmark ratchets, and SCF replacement gates in dependency order.
- Mechanism: Delay recursive self-improvement until evaluator integrity, rollback, residual preservation, governance rights, and evidence-ledger behavior are credible.
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
| `lean:roadmap.phases.operational_invariant` | `AsiStackProofs.PrototypeRoadmap` | A roadmap phase can unlock a dependent phase only after acceptance gates pass. | implemented |
| `lean:roadmap.phases.failure_blocks_promotion` | `AsiStackProofs.PrototypeRoadmap` | A phase milestone cannot promote a claim without evidence artifacts. | implemented |

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
- Mechanism: Keep `book_structure.json` as the ordering source of truth for parts, stable chapter ids, chapter file paths, front matter, and appendices.
- Mechanism: Keep `docs/book_outline.md` as the drafting, source-queue, proof-scope, Lean-tag, and future-writing control surface.
- Mechanism: Treat conversation-mined packets as author-intent, terminology, lineage, and recovery context only, not as source-derived evidence.
- Mechanism: Maintain distinct live AI/research scaffolding, frozen research releases, stripped reader editions, companion notes, and audio-script workspaces derived from one validated source state.
- Mechanism: Require meaningful structural, evidence, proof, schema, source, or publication changes to sync scaffold, sync proof manifest, validate, render, update changelog, commit, push, and verify the public site.
- Interface: Source ingestion feeds source notes.
- Interface: Drafting feeds claim matrices.
- Interface: Tests feed support states.
- Interface: Releases feed GitHub Pages, major-version edition records, reader manuscripts, and audio-script candidates.

Primary invariants:

- No fabricated source content.
- No fabricated test results.
- Deprecated claims remain visible.

Failure modes to cover:

- Public site diverges from Quarto source.
- Outline and manifest drift.
- Readers cannot tell which claims are speculative.
- Reader or audio releases accidentally imply that target formats exist before render, review, or audio production.

Draft deliverables:

- A public Quarto repo with dynamic scaffold, source matrix, claim matrix, proof manifest, validation, GitHub Pages, and public release records.
- A public-safe author-intent and lineage appendix that preserves architecture intent without publishing private conversation text.
- Implemented repository-level validation: `living_book_release_record.valid.json` and tracked records in `release_records/` validate release-record shape only; render and validation checks prove publication hygiene, not manuscript quality or claim truth.
- A three-audience edition profile with live, research, reader, and audio paths; a reader-edition source generator; an audio-script generator; and an edition-release record schema for future EPUB, PDF, DOCX, MP3, M4B, and audio-embedded EPUB accountability.
- Planned Codex test: Quarto render check.
- Planned Codex test: Manifest/outline consistency check.
- Planned Codex test: Changelog update check.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:living_book.methodology.operational_invariant` | `AsiStackProofs.LivingBook` | Every chapter in the manifest has outline proof targets and generated claim placeholders. | implemented |
| `lean:living_book.methodology.failure_blocks_promotion` | `AsiStackProofs.LivingBook` | A structural update without regenerated scaffold/proof manifest is invalid. | implemented |

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
- Mechanism: Maintain source inventory, source notes, generated bibliography, chapter source queues, and direct-citation status before using a source as support.
- Mechanism: Track recovered, missing, private, connector-gated, external-literature, proof, experiment, and artifact-reproduction items as Research Backlog Records rather than evidence.
- Mechanism: Use triage rules to decide whether a new paper updates an existing boundary, requires a precise new chapter, belongs in an appendix, or should remain unassigned.
- Mechanism: Preserve merge/insertion rules so overlapping papers mine shared mechanisms without creating duplicate anthology chapters.
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
| `lean:bibliography.plan.operational_invariant` | `AsiStackProofs.BibliographyPlan` | A source-derived claim requires a source note or equivalent ingested-source artifact. | implemented |
| `lean:bibliography.plan.failure_blocks_promotion` | `AsiStackProofs.BibliographyPlan` | A new source cannot be assigned to a non-existent chapter id. | implemented |

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
