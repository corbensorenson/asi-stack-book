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
- What the beyond-state-of-the-art logical conclusion of each chapter looks like when the idea matures into a governed, evidence-bearing product surface.
- How the living book acts as an evidence ratchet instead of a static anthology.

## Audience and Edition Spine

Future writing runs should serve three audiences from one canonical source tree:

- AIs and writing agents need stable IDs, source queues, claim/evidence states, proof hooks, schemas, validation commands, and guardrails.
- Human researchers need the full technical argument plus traceable evidence machinery, known residuals, and frozen major-version review artifacts.
- Interested human readers need a coherent manuscript for EPUB, PDF, DOCX, e-reader, and audio consumption without repeated live-workflow scaffolding.

The ordinary chapter prose is the reader-facing spine. It must still make sense after live-only headings such as `Chapter status`, `Drafting guardrail`, `Codex test plan`, `Source crosswalk`, `Claim-source mapping status`, and `Formalization hooks` are stripped. Meaning-critical caveats, uncertainty, and support-state limits belong in the spine, not only in a stripped guardrail or source-crosswalk section.

Every chapter must include both `Minimum Viable Implementation` and `Beyond the State of the Art`. The minimal section defines the smallest public-safe artifact or validated slice that can start the chapter's idea honestly. The beyond-SOTA section defines the mature logical conclusion of the idea: the final product surface, operational contract, evidence flow, governance boundary, failure closure, and composition with the rest of the stack. The beyond-SOTA section is a target architecture, not a claim of current implementation; it must preserve the chapter's recorded support state until proof, test, source, benchmark, or runtime artifacts justify promotion.

Appendix K, `Implementation Horizons`, is generated from the same manifest fields and should be used as the book-wide build-horizon map during full-book writing runs. If a chapter is added, moved, merged, or split, update `book_structure.json`, rerun `python3 scripts/sync_scaffold.py`, and confirm the appendix still shows a precise minimum slice and mature endpoint for every chapter.

The live site exposes this separation through a reading-mode toggle. `AI view` shows the reader spine plus the live/research scaffold, raw core-claim markers, and repeated support-state boilerplate. `Human view` hides the same live-only headings used by the reader-release profile, hides raw claim markers while preserving claim text, and keeps the compact evidence boundary inline with the core claim instead of opening repeated support paragraphs. Each chapter must maintain exactly one `.asi-human-only` `Human Reading Path` bridge after `Drafting guardrail` and before `Problem` so interested readers get a concise orientation without turning the project into a second manuscript. The source heading is a machine-checkable marker; live Human view and generated reader editions present the bridge as unheaded lead-in prose and hide its page-TOC entry. `.asi-ai-only` and `.asi-live-only` fenced divs are reserved for AI/research scaffolding that should disappear from Human view and reader releases. Reader generation unwraps human-only blocks, removes AI-only blocks, strips raw claim markers, removes repeated support boilerplate while preserving inline evidence boundaries, and must preserve one reader-facing `Handoff` section per chapter so the stripped manuscript keeps the manifest-order argument.

Major-version reader and audio editions are derivatives of the live book, not parallel manuscripts. Use `editions/release_profiles.json` as the machine-readable contract for content layers, strip rules, release gates, target formats, generated manifests, human-consumption bundle gates, and non-claims.

When drafting or revising chapters, preserve a continuous reader-facing spine before the live-only sections do their audit work. A future writing goal should be able to strip status blocks, source crosswalks, proof hooks, and Codex test plans while still leaving a coherent EPUB/PDF/DOCX manuscript, live-site Human view, and narration-ready audio script path.

The generated reader spine must now pass section-level quality floors, not only a whole-chapter word count. `scripts/validate_reader_spine.py --check` verifies that every required reader section remains present, clears its minimum word count, and contains enough substantial prose paragraphs after live-only scaffolding is removed. This keeps the live Human view and reader editions from becoming a thin outline wrapped around hidden AI/research machinery.

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
- Mechanism: Define each layer by lifecycle state, owner, chapter refs, traceability state, responsibility, interface, artifact, handoff protocol, authority ceiling, invariant, failure mode, evidence gate, integration decision, promotion blockers, source refs, support-state effect, and non-claim.
- Mechanism: Frame the raw LLM as a semantic-compression and generation component inside the larger governed system, not as the whole agent.
- Mechanism: Treat the whole book as a reference architecture rather than a collection of standalone papers.
- Mechanism: Use source queues and evidence states to keep future writing runs context-loaded and honest.
- Mechanism: Treat layer contracts as the stable object when adding, moving, merging, or revising chapters.
- Interface: Alignment and governance constrain every downstream layer.
- Interface: Planning, memory, reasoning, execution, routing, compression, and evidence exchange typed artifacts.
- Interface: Recursive improvement is a governed transition, not an ambient property of intelligence.

Primary invariants:

- Layer boundaries remain explicit.
- Claims carry support states.
- Reasoning ability never implies execution authority.
- New capability evidence enters through layer contracts rather than narrative enthusiasm.

Failure modes to cover:

- Anthology drift.
- Monolith drift.
- Evidence inflation before source notes or tests exist.
- Chapter growth that adds ideas without assigning ownership, artifacts, invariants, or non-claims.

Draft deliverables:

- A stack map, layer boundary record schema and fixture, source crosswalk, and claim ledger that make the architecture navigable before prose is complete.
- Implemented repository-level fixture: `layer_boundary_record.valid.json` validates lifecycle state, owner, chapter refs, traceability state, handoff protocol, contract refs, change policy, integration decision, promotion blockers, source refs, support-state effect, and non-claims only; source-to-layer traceability and claim-support audits remain planned.
- Exact Appendix C claim-source mappings for the core claim across `viea`, `beastbrain`, `aletheia`, `talos`, `moecot`, and `scf`; support remains `argument` pending implementation or test evidence.
- Planned Codex test: Layer-boundary audit.
- Planned Codex test: Source-to-layer traceability review.
- Planned Codex test: Claim-support label audit.
- Planned Codex test: Contract-change triage.

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
- Mechanism: Classify route outcomes as adequate minimum, adequate overkill, cheap brittle, hidden cost, or unsafe saving.
- Mechanism: Account for model/runtime, context construction, verification, repair, human-review, regression, rollback, and residual costs together.
- Interface: Planning requests capability profiles.
- Interface: Routing selects specialists.
- Interface: Evidence decides whether efficiency claims survived quality and cost tests.

Primary invariants:

- Efficiency claims include quality and cost.
- Compression exposes residuals.
- Fallback routes remain available.
- Verification and repair costs remain attached to the route that made them necessary.
- No route may be called efficient by bypassing authority or approval gates.

Failure modes to cover:

- Cheap inference mistaken for intelligence.
- Critical context compressed away.
- Benchmark gains that increase hidden residual burden.

Draft deliverables:

- A costed route ledger with route state, task contract ref, quality predicates, outcome state, cost classes, hidden-cost checks, residual accounting, support-state effect, and fallback criteria.
- Implemented repository-level fixture: `costed_route_record.valid.json` validates route state, task contract ref, outcome state, cost classes, hidden-cost checks, support-state effect, and non-claims only; no route-search, residual-burden, or utility-preserving compression test exists yet.
- Exact Appendix C claim-source mappings for the core claim across all assigned efficiency, compression, simulation, lineage, and implementation-reference sources; support remains `argument` pending measured route, cost, residual, and compression evidence.
- Planned Codex test: Minimum viable route test.
- Planned Codex test: Residual burden accounting test.
- Planned Codex test: Utility-preserving compression test.
- Planned Codex test: Hidden-cost audit.

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
- Mechanism: Model grant lifecycle as requested, denied, granted, delegated, used, receipted, expired, or revoked.
- Mechanism: Distinguish read, transform, disclose, write, execute, and approve permissions.
- Mechanism: Preserve caller ceiling, target-required authority, delegation chain, expiry/review condition, audit receipts, and non-claims so a capable tool cannot launder broader permission through a lower-authority requester.
- Interface: Governance issues ceilings.
- Interface: Execution checks permissions.
- Interface: Evidence records authority-related failures.

Primary invariants:

- Authority never expands silently.
- Read permission is not write permission.
- Tool execution requires an explicit grant.
- Delegated authority can narrow but not silently widen the caller's ceiling.
- Approval authority is separate from execution authority.

Failure modes to cover:

- Authority creep.
- Confused-deputy tool calls.
- Memory access treated as action approval.
- Stale grants used after expiry or revocation.
- Replacement implementations inheriting handles that were qualified only for an older implementation.

Draft deliverables:

- A small authority schema and transition table used by chapter examples and future Lean proofs, including permission class, grant lifecycle state, caller ceiling, target-required authority, delegation chain, expiry/review condition, audit refs, and non-claims.
- Exact Appendix C claim-source mappings for the core claim across `viea`, `scf`, `talos`, `ladon_manhattan`, `genesiscode`, and `moecot`; support remains `argument` pending denial fixtures, permission-separation tests, confused-deputy probes, or deployed enforcement artifacts.
- Planned Codex test: Authority ceiling preservation test.
- Planned Codex test: Permission separation test.
- Planned Codex test: Confused-deputy scenario.
- Planned Codex test: Revocation propagation test.

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
- Mechanism: treat failures and near misses as boundary events with receipts, owners, containment actions, severity, recurrence, escape path, and downstream learning path.
- Mechanism: Preserve failure class, affected contract refs, boundary event state, severity, reversibility, recurrence count, receipt refs, promotion blocker, normalization guard, learning path, source refs, support-state effect, residual risk, and non-claims so near misses and repeated failures do not vanish into a narrower success narrative.
- Interface: Governance limits authority creep.
- Interface: VCM limits context pollution.
- Interface: Verification limits false certainty.
- Interface: Execution limits side effects.
- Interface: emit failure receipts for blocked and realized failures without treating blocked failures as solved safety properties.

Primary invariants:

- Every risk maps to at least one boundary.
- Evaluator integrity is protected.
- Negative evidence stays visible.
- Repeated failures do not become normal behavior by disappearing from records or routing around detectors.

Failure modes to cover:

- Evaluator capture.
- Memory poisoning.
- Tool/action overreach.
- Compression that hides residual complexity.
- Failure laundering: a run fails a boundary, then the narrative shifts to a narrower success metric while the denial or residual disappears.

Draft deliverables:

- A layered failure taxonomy tied to invariants, source queues, future tests, failure class, affected contracts, boundary event state, severity, reversibility, recurrence, receipts, promotion blockers, normalization guards, learning paths, source refs, support-state effect, residuals, and non-claims.
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
- Mechanism: emit evidence receipts that lock artifact role, claim scope, claim-record linkage, source-mapping status, evidence-readiness state, transition effect, transition validity state, evidence role, verification command or review, reviewer refs, downgrade triggers, promotion burden, acceptance blockers, reviewer independence, changelog ref, limitations, non-claims, and negative or inconclusive results.
- Mechanism: treat upward support movement as a burden and downward movement as mandatory when contradiction, missing evidence, failed verification, or scope mismatch appears.
- Interface: Drafting updates claims.
- Interface: Experiments update evidence.
- Interface: Changelog records evidence movement.
- Interface: distinguish lineage, motivation, terminology, direct support, contradiction, failed support, reproduced result, source-reported result, local fixture, formal predicate, and empirical measurement.

Primary invariants:

- No fabricated source support.
- No fabricated test results.
- Negative and inconclusive results remain visible.
- Evidence scope cannot expand through proximity to a source, proof module, benchmark, or neighboring chapter.

Failure modes to cover:

- Support-state inflation.
- Citation laundering.
- Silent removal of failed claims.
- Evidence smoothing: clearer prose removes caveats, failures, or open gaps while the support state remains unchanged.

Draft deliverables:

- A claim record schema, evidence transition record schema, claim-label table, support-state transition table, evidence-bundle template, and validation check with source mapping status, source mapping refs, evidence readiness state, claim surface refs, claim record refs, transition validity state, evidence packet refs, source mapping refs, negative evidence refs, reviewer refs, acceptance blockers, support-state effect, and non-claims.
- Implemented repository-level fixture: `claim_record.valid.json` validates source mapping status, source mapping refs, evidence readiness state, required next evidence, promotion blockers, support-state effect, and non-claims only; `evidence_transition_record.valid.json` validates claim surface refs, claim record refs, transition effect, transition validity state, scope boundary, evidence roles, evidence packet refs, source mapping refs, negative evidence refs, downgrade triggers, promotion burden, reviewer refs, reviewer independence, acceptance blockers, changelog ref, support-state effect, and non-claims only; claim-ledger completeness, evidence bundle completeness, accepted transition review, and changelog audits remain planned.
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
- Mechanism: Track intent intake states: raw request, interpreted, bounded default, clarification required, authority pending, accepted contract, re-contract required, rejected or expired.
- Mechanism: Emit an intent receipt with confirmed assumptions, bounded defaults, unauthorized means, required approvals, re-contract triggers, review refs, and downstream contract refs.
- Interface: Alignment filters intent.
- Interface: Planning compiles accepted contracts.
- Interface: Execution consumes only authorized task contracts.

Primary invariants:

- Ambiguity triggers clarification or bounded defaults.
- Intent contracts expose authority limits.
- Stop conditions remain attached to the plan.
- Raw request context cannot override the accepted contract.
- Re-contracting is required when downstream work changes means, authority, affected parties, evidence, publication surface, or stop conditions.

Failure modes to cover:

- Goal misbinding.
- Scope creep.
- Implicit permission to act.
- Assumption laundering, where a helpful guess becomes execution authority.
- Review bypass, where urgency or trust language is treated as permission to skip evidence or approval.

Draft deliverables:

- An intent-contract schema and example transformations from request to governed task.
- Exact Appendix C claim-source mappings for the core claim across `viea`, `software_magic_grimoire`, `planforge`, `cognitive_compilation`, and `talos`; all five local mappings now have reviewed raw-cache passage references. Support remains `argument` pending parser, authority-extraction, stop-condition, or lowering tests.
- Planned Codex test: Intent parsing ambiguity test.
- Planned Codex test: Authority extraction test.
- Planned Codex test: Stop-condition preservation test.
- Planned Codex test: Re-contract trigger test.
- Planned Codex test: Bounded-default audit.

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
- Mechanism: Give predicates scope and conflict behavior so value conflicts route to narrowing, consent, tribunal review, residual preservation, or blocking rather than hidden optimizer choices.
- Mechanism: Treat changes to protected predicates as constitutional migrations with diff records, review, rollback, and residuals rather than ordinary refactors.
- Mechanism: Track predicate states such as speculative-lineage, partial, operational, protected, under-review, deprecated, and retired so lineage notes cannot authorize action.
- Mechanism: Require conflict behavior and migration policy on constitutional predicates before they can govern planning, tool use, memory, release, or self-improvement.
- Interface: Planning receives admissible-goal constraints.
- Interface: Runtime receives power, memory, and tool-risk gates.
- Interface: Governance receives protected constraints and non-weakenable predicates.
- Interface: Verification checks whether normative claims exceed evidence or translation status.

Primary invariants:

- Dignity and agency constraints remain visible.
- Corrigibility cannot be optimized away.
- Speculative metaphysics stays labeled.
- Predicate conflict behavior is explicit before a plan can proceed.
- Protected predicate changes require a migration record and rollback path.

Failure modes to cover:

- Mystical framing replacing technical constraints.
- Power without care.
- Self-modification weakening protected commitments.
- Predicate drift.
- Conflict-default capture.

Draft deliverables:

- A compact constitution with operational predicates, open moral uncertainties, and scenario tests.
- Exact Appendix C claim-source mappings for the core claim across alignment lineage, metaphysical variants, reasoning governance, connector synthesis, and the AI Constitution source; six mappings (`alignment_field`, `field_of_god`, `ethica_mechanica`, `eternal_code`, `spinoza`, `field_of_god_ai_constitution`) now have reviewed passage references, while `coherence_exchange` remains connector-only/source-note mapped. Support remains `argument` pending constitutional consistency, predicate-conflict routing, constitutional migration, self-modification ethics, power-without-care, runtime policy, or red-team evidence.
- Planned Codex test: Constitutional consistency test.
- Planned Codex test: Predicate-conflict routing test.
- Planned Codex test: Constitutional migration test.
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
- Mechanism: Track rights usability states such as available, available-but-costly, late, degraded, denied, residual-only, and not-applicable.
- Mechanism: Record material usability, timing requirement, and denial or degradation reason so a declared right cannot substitute for a reachable interface under pressure.
- Interface: Alignment defines agency predicates.
- Interface: Governance enforces rights and approval thresholds.
- Interface: Execution requires preserved review and correction paths before irreversible effects.

Primary invariants:

- Users retain meaningful refusal and review channels.
- Delegation does not erase accountability.
- Irreversible actions require stronger authorization.
- Rights count only when materially usable before the relevant effect where timing matters.
- Denied or degraded rights produce residuals rather than disappearing into policy prose.

Failure modes to cover:

- Dependency lock-in.
- Covert manipulation.
- Corrigibility collapse.
- Rights theater.
- Late remedy laundering.

Draft deliverables:

- A rights-and-corrigibility checklist attached to high-impact plans.
- Exact Appendix C claim-source mappings for the agency/corrigibility core claim across alignment lineage, recursive-agency governance, metaphysical variants, connector synthesis, and the AI Constitution source; five mappings (`alignment_field`, `ethica_mechanica`, `field_of_god`, `eternal_code`, `field_of_god_ai_constitution`) now have reviewed passage references, while `coherence_exchange` remains connector-only/source-note mapped. Support remains `argument` pending agency-preservation, material-usability, timing-before-effect, corrigibility-pathway, high-impact approval, manipulation-resistance, or runtime-policy evidence.
- Planned Codex test: Agency-preservation scenario.
- Planned Codex test: Material-usability rights test.
- Planned Codex test: Timing-before-effect test.
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
- Mechanism: treat bounded decisions as leases with permitted action, prohibited action, affected stakeholders, authority ceiling, expiry, revisit trigger, dissent payload, and rollback or appeal path.
- Mechanism: Track decision states such as unresolved, bounded decision, escalated review, deferred action, denied action, and deprecated premise with distinct authority effects.
- Mechanism: Preserve dissent payloads and unsupported premises so bounded decisions do not become permanent value claims, benchmark rewards, or self-modification permissions.
- Interface: Alignment produces conflict records.
- Interface: Planning carries conflict constraints with the plan.
- Interface: Governance decides review routes and authority boundaries.
- Interface: Evidence records review outcomes, dissent, unsupported premises, and residual uncertainty.
- Interface: distinguish unresolved conflict, bounded decision, escalated review, deferred action, denied action, and deprecated premise.

Primary invariants:

- Unresolved conflicts remain visible.
- High-stakes conflicts require stronger review.
- Speculative moral theory cannot silently authorize action.
- Unresolved high-stakes conflict narrows authority rather than broadening it for convenience.
- Decision states carry authority effects.
- Dissent payloads and unsupported premises survive bounded decisions.

Failure modes to cover:

- Value flattening.
- False consensus.
- Review theater without decision records.
- Conflict laundering: a bounded temporary decision hardens into policy, benchmark objective, or self-modification permission.
- Dissent deletion.
- Authority creep from temporary conflict leases.

Draft deliverables:

- A value-conflict record schema and scenario library.
- Exact Appendix C claim-source mappings for the value-conflict core claim across recursive-agency governance, alignment lineage, connector synthesis, UAT review mechanics, Spinoza belief revision, and the AI Constitution source; five mappings (`ethica_mechanica`, `alignment_field`, `uat`, `spinoza`, `field_of_god_ai_constitution`) now have reviewed passage references, while `coherence_exchange` remains connector-only/source-note mapped. Support remains `argument` pending value-conflict classification, decision-state routing, review-escalation, dissent preservation, residual-uncertainty preservation, reviewer-quality, or runtime-policy evidence.
- Planned Codex test: Value conflict classification test.
- Planned Codex test: Decision-state routing test.
- Planned Codex test: Review escalation test.
- Planned Codex test: Dissent preservation test.
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
- Mechanism: emit rights receipts that record request, holder, scope, material available, material withheld, denial/redaction reason, appeal path, expiry, and preservation obligation.
- Mechanism: Require challenged-party independence and receipt preservation so the authority being challenged is not the only keeper of the record, denial reason, appeal path, or export state.
- Interface: Governance issues rights.
- Interface: SCFs preserve rights across replacement.
- Interface: Memory/security/execution systems produce evidence for audit, export, revocation, and contestability.
- Interface: distinguish access failure, justified denial, redacted access, partial export, portable export, contested decision, and preserved dissent.

Primary invariants:

- Audit records cannot be silently deleted.
- Exit paths remain materially usable.
- Fork rights do not bypass safety constraints.
- The challenged authority cannot be the only keeper of the record, denial reason, or appeal path.

Failure modes to cover:

- Governance capture.
- Data hostage-taking.
- Opaque automated policy updates.
- Rights theater: policy text exists, but logs, exports, redaction rules, appeal channels, or preservation hooks fail when the right is inconvenient.

Draft deliverables:

- A governance-rights table with required artifacts, request states, material availability, withheld-material reasons, appeal paths, challenged-party independence, preservation obligations, receipt refs, authorities, and failure tests.
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
- Mechanism: Record qualification status and a qualification lease/status with epoch, expiry, review triggers, incidents, rollback obligations, and non-claims so qualified routes can age, downgrade, or force requalification.
- Mechanism: Pair broad route proposers with narrow validators that check field identity, claims, leases, profiles, grants, state paths, composition certificates, and authority ceilings.
- Mechanism: Treat the SCF as capability-identity memory: field identity, evaluator policy, regression floors, lifecycle history, incidents, and rollback obligations survive implementation replacement.
- Mechanism: Make qualification leases reviewable and aging: benchmark epoch, source corpus, hardware profile, threat model, incident triggers, field history refs, default-route blockers, and requalification duties can expire or downgrade route status.
- Interface: Planning sees semantic capability boundaries.
- Interface: Execution sees authorized routes.
- Interface: Evidence and governance see qualification claims, regressions, incidents, lifecycle state, evaluator policy, and recovery paths.
- Interface: Replacement and readiness gates consume the SCF lease, evaluator independence statement, rollback obligations, review triggers, and non-claims.

Primary invariants:

- Replacement cannot expand authority by default.
- Evaluator integrity is protected.
- Qualification context is explicit and time-bound.
- Rollback remains available after failed mutation.
- Qualification leases expire or downgrade when review triggers fire.

Failure modes to cover:

- Field identity drift.
- Evaluator capture.
- Authority expansion during replacement.

Draft deliverables:

- An SCF record schema with field identity, field version, owner, implementation versions, lifecycle state, qualification context/status, qualification lease/status, evaluator independence, evidence, route validity/scope, route permission effect, consumer policy, readiness gate refs, field history refs, source refs, support-state effect, incidents, review triggers, migration path, rollback obligations, default-route blockers, and non-claims.
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
- Mechanism: Keep candidate improvement, canary use, default promotion, monitor evidence/status, promotion blockers, and rollback obligation as separate transaction states.
- Mechanism: emit rollback receipts that record prior artifact, state migration status, reversible fields, irreversible effects, dry-run status, trigger conditions, and owner.
- Mechanism: require identity-preservation and evaluator-independence fields so the candidate cannot validate its own promotion or silently redefine the field it claims to improve.
- Mechanism: expose replacement decision states such as proposed, shadow, canary, default-candidate, default, rolled-back, quarantined, superseded, and retired.
- Interface: SCF ledger defines the field identity to preserve.
- Interface: Benchmark and evidence ledgers test frontier movement and regression preservation.
- Interface: Artifact graph and changelog record candidate artifacts, state migration, decision, residuals, and recovery state.
- Interface: security, runtime-adapter, policy-optimization, and governance layers inspect replacement transactions for authority, secret, evaluator, monitor, and rollback changes.
- Interface: readiness gates consume replacement receipts only within the field, workload family, freshness window, route permissions, and residual inheritance they declare.
- Exact Appendix C claim-source mappings for the core replacement claim across SCF field identity, RMI modular ratchets, Benchmaxxing benchmark lifecycle, Cognitive Loop Closure procedural lifecycle, Talos audit/replay context, and MoECOT runtime-reference context; five local mappings (`scf`, `rmi`, `benchmaxxing`, `cognitive_loop_closure`, `talos`) now have reviewed passage references, while `moecot` remains connector-only/source-note mapped. Support remains `argument` pending regression-preservation tests, rollback dry runs, monitor-window evidence, artifact replay, or deployed replacement evidence.

Primary invariants:

- No replacement without prior and posterior artifacts.
- Regressions stay attached.
- Rollback metadata is required before promotion.
- Candidate-provided evidence cannot be the sole evaluator, gatekeeper, or rollback authority for its own promotion.
- Rollback receipts must name reversible fields, irreversible effects, trigger conditions, and owner before default promotion.

Failure modes to cover:

- Regression deletion.
- Rollback impossible after deployment.
- Self-judged replacement.
- Rollback theater: rollback fields exist without executable path, compatibility check, trigger condition, or owner.

Draft deliverables:

- A replacement transaction schema with transaction state, identity-preservation, precheck, gate, commit, canary scope, monitor status, evaluator-independence, rollback receipt, promotion blockers, source refs, support-state effect, residual, and non-claim fields.
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
- Mechanism: Bind handles to purpose, destination, action, time window, approval, logging, and revocation so authority cannot become ambient context or be reused after the lease expires.
- Mechanism: Treat sanitized outputs as security artifacts with removal notes and residual leak-risk records; summaries can still leak derived sensitive information.
- Mechanism: Track handle-lease states such as requested, denied, scoped, active, substituted, sanitized, zeroized, expired, revoked, and leak-residual-recorded.
- Mechanism: Emit a SCIF Commit Record with admitted context shards, memory masks, allowed tools, denied material, substitution event, sanitization decision, zeroization result, committed material, residual leak-risk class, and expiry or revocation event.
- Interface: VCM supplies least-privilege context and clearance-scoped mission briefs.
- Interface: Execution checks tool permissions and performs substitution only at authorized runtime boundaries.
- Interface: Governance audits sensitive transitions through Authority Use Receipts.
- Exact Appendix C claim-source mappings for the core security-kernel claim across Ladon/Manhattan blind handles, Context Engineer SCIF/context-supply-chain lifecycle, Talos execution/audit context, Alignment Field normative boundary pressure, and Coherence Exchange governance framing; four local mappings (`ladon_manhattan`, `context_engineer`, `talos`, `alignment_field`) now have reviewed passage references, while `coherence_exchange` remains connector-only/source-note mapped. Support remains `argument` pending secret-handle substitution tests, SCIF least-privilege tests, prompt-injection containment scenarios, threat-model artifacts, side-channel analysis, or deployed runtime evidence.

Primary invariants:

- Secrets are not directly model-visible.
- SCIF context is purpose-limited.
- Privilege substitution is auditable.
- Handle leases expire or revoke rather than becoming ambient authority.
- Sanitized commits record retained material and residual leak risk.

Failure modes to cover:

- Prompt injection extracting secrets.
- Privilege leakage through summaries.
- SCIF bypass.
- Ambient-handle drift.
- Security-cost laundering.

Draft deliverables:

- A secure-handle workflow and SCIF lifecycle diagram.
- Planned Codex test: Secret-handle substitution test.
- Planned Codex test: Handle lease expiry/reuse test.
- Planned Codex test: SCIF least-privilege test.
- Planned Codex test: Sanitized-output residual test.
- Planned Codex test: Security-overhead budget preservation test.
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
- Mechanism: Treat security and resource boundary changes as first-class governance questions: a self-improvement proposal cannot silently widen handles, weaken SCIF lifecycle, cut verification budget, relax rollback, or retire regressions.
- Mechanism: Record self-improvement transitions as chain-of-custody artifacts from residual/wall through authority used, budget spent, evidence collected, independent evaluation, protected-invariant result, approval, canary, rollback, and lifecycle state.
- Mechanism: Require a Boundary Delta Review naming authority, security, resource, evaluator, evidence, and rollback deltas before canary or promotion.
- Mechanism: Track transition states such as proposed, research-only, evidence-packet-ready, boundary-delta-blocked, canary, default-candidate, promoted, quarantined, rolled-back, superseded, and retired.
- Interface: SCFs define replaceable units and authority ceilings.
- Interface: Evidence ratchets, readiness gates, and replacement transactions provide gates.
- Interface: Alignment and governance supply protected constraints, approval boundaries, and non-self-ratification rules.

Primary invariants:

- Self-improvement cannot weaken protected invariants.
- Evaluator independence is required.
- Every accepted change remains auditable.
- Boundary deltas are explicit before promotion.
- Resource savings cannot spend security, verification, rollback, or human-review obligations unless governance separately changes those obligations.

Failure modes to cover:

- Recursive evaluator capture.
- Constitutional weakening.
- Irreversible flawed upgrades.
- Boundary delta laundering.
- Stale-gate promotion.

Draft deliverables:

- A self-improvement protocol that can reject, quarantine, roll back, or retire a proposed change.
- Exact Appendix C claim-source mappings for the core recursive-self-improvement claim across SCF stable fields, Benchmaxxing benchmark-ratchet discipline, RMI modular improvement loops, Alignment Field normative caution, VIEA durable artifact/feedback discipline, Talos typed jobs/audit/replay, MoECOT runtime-reference context, Field of God AI Constitution protected constraints, and Theseus self-evolution/readiness-gate notes; six local mappings (`scf`, `benchmaxxing`, `rmi`, `alignment_field`, `viea`, `talos`) now have reviewed passage references, while `moecot` remains connector-only/source-note mapped and the constitution/Theseus mappings remain public-project/source-note mapped until raw source is vendored or made durable in this project. Support remains `argument` pending protected-invariant tests, evaluator-independence scenarios, rollback/canary execution evidence, fresh Theseus report inspection, or accepted evidence transitions.
- Planned Codex test: Protected-invariant preservation test.
- Planned Codex test: Evaluator independence test.
- Planned Codex test: Boundary-delta review test.
- Planned Codex test: Verification-budget preservation test.
- Planned Codex test: Stale-gate replay test.
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
- Mechanism: Separate desire, authorization, means, and acceptance so helpful overrun becomes a re-contract request rather than silent execution authority.
- Mechanism: Preserve authority deltas and re-contract points when planning discovers missing approval, inadequate context, unverifiable output, budget pressure, or forbidden means.
- Mechanism: Record intake state, bounded defaults, handoff receipts, dispatch receipts, re-contract events, stop/fault state, residuals, and explicit non-claims so trace-shape validation is not mistaken for execution evidence.
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

- Intent-contract, command-contract, and intent-to-execution trace schemas with one public-safe intent-to-artifact trace shape.
- Implemented protocol validation: `intent_contract`, `command_contract`, and `intent_execution_trace` fixtures validate public record shape only, including intake state, bounded defaults, handoff receipts, dispatch receipts, re-contract events, stop/fault state, residuals, and non-claims.
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
- Mechanism: Treat command contracts as semantic firewalls: retrieved context, examples, prior conversation, and style notes can inform work but cannot override explicit objective, constraints, authority, verification, or failure behavior.
- Mechanism: Mark field confidence and missing/inferred authority so planning can distinguish authorized means from inferred defaults, draft-only routes, clarifications, and residuals.
- Mechanism: Track command validation states: draft, field-complete, conflict-detected, authority-inferred, dispatch-blocked, validated-for-planning, and superseded.
- Mechanism: Attach field provenance and confidence states: confirmed, policy-imposed, source-derived, defaulted, inferred, and missing.
- Mechanism: Preserve bounded defaults, authority basis, re-contract points, dispatch blockers, and non-claims as first-class fields so future parser and dispatcher tests can distinguish record shape from enforcement.
- Interface: Planning consumes structured commands.
- Interface: Execution enforces output contracts.
- Interface: Verification checks stated failure behavior.

Primary invariants:

- A command exposes output and verification requirements.
- Failure behavior is declared.
- Implicit instructions do not override explicit constraints.
- Field provenance and confidence remain visible to planning and verification.
- Inferred or defaulted authority cannot authorize side effects.

Failure modes to cover:

- Semantic ambiguity.
- Prompt injection through context.
- Unspecified output contract.
- Field laundering, where vague prose is moved into a formal field without becoming testable.
- Authority inference, where a likely means is treated as if the human granted it.

Draft deliverables:

- A canonical command-contract template used by future chapter drafting and experiment prompts.
- Implemented protocol validation: `command_contract` fixture validates public record shape only, including validation state, field provenance, field confidence, bounded defaults, authority basis, re-contract points, dispatch blockers, and non-claims.
- Exact Appendix C claim-source mappings for the core command-contract claim across Software Magic Grimoire command-envelope vocabulary, VIEA structured command layers, GenesisCode protocol/effect boundaries, Cognitive Compilation source-plan/S-IR lowering, and Talos typed-job contract discipline; all five local mappings (`software_magic_grimoire`, `viea`, `genesiscode`, `cognitive_compilation`, `talos`) now have reviewed passage references. Support remains `argument` pending command parser tests, dispatch-blocking tests, prompt-override scenarios, semantic-extraction quality checks, or accepted evidence transitions.
- Planned Codex test: Command schema validation test.
- Planned Codex test: Failure-behavior declaration test.
- Planned Codex test: Prompt override scenario.
- Planned Codex test: Field-confidence audit.
- Planned Codex test: Authority-inference block test.

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
- Mechanism: Treat the plan graph as a refusal-friendly control artifact: missing context, blocked dependencies, authority overreach, exhausted budgets, and failed predicates become residuals before side effects.
- Mechanism: Preserve stop conditions, authority ceilings, and alternative-route status during replanning; only dispatchable nodes with satisfied constraints lower into typed jobs.
- Mechanism: Track plan node lifecycle states: proposed, blocked-context, blocked-authority, blocked-dependency, blocked-verification, dispatchable, dispatched, replanned, and stopped.
- Mechanism: Emit dispatch receipts with satisfied constraints, context refs, authority basis, verification plan, replanning history, and typed-job refs.
- Mechanism: Preserve authority budget, replanning history, blocked-node records, residual register, and non-claims so a candidate graph cannot masquerade as governed dispatch.
- Interface: Alignment filters goals.
- Interface: VCM supplies context packets.
- Interface: Routing selects specialists.
- Interface: Execution runs typed jobs.

Primary invariants:

- Plans expose constraints and stop conditions.
- Runtime replanning preserves authority limits.
- Tool selection is justified by task requirements.
- Only dispatchable nodes lower into typed jobs.
- Candidate routes, blocked nodes, and review notes are not executable permission.

Failure modes to cover:

- Scope creep.
- Planning without replanning.
- Tool choice exceeds authority or budget.
- Dispatch laundering, where a proposed or blocked node becomes a job because it appears in the graph.
- Replanning erasure, where feedback changes the plan while hiding the authority, stop-condition, or residual delta.

Draft deliverables:

- A plan graph format with dependencies, context requests, authority budget, risk budgets, stop conditions, lifecycle states, dispatch receipts, blocked-node records, and residual register.
- Implemented protocol validation: `plan_graph` fixture validates public record shape only, including authority budget, replanning history, lifecycle states, blocked nodes, dispatch receipts, residual register, and non-claims.
- Exact Appendix C claim-source mappings for the planning-control claim across PlanForge planning middleware, VIEA orchestration/runtime spine, Cognitive Compilation source-plan/S-IR pipeline, Software Magic Grimoire spell-stack workflow discipline, and MoECOT runtime-reference context; the four local mappings (`planforge`, `viea`, `cognitive_compilation`, `software_magic_grimoire`) now have reviewed passage references. `moecot` remains connector/source-note mapped until usable raw text, code, logs, release artifacts, or benchmark records are imported or inspected. Support remains `argument` pending planner harnesses, dependency-order checks, context-demand tests, runtime replanning traces, or accepted evidence transitions.
- Planned Codex test: Decomposition accuracy test.
- Planned Codex test: Dependency ordering test.
- Planned Codex test: Context-demand prediction test.
- Planned Codex test: Runtime replanning test.
- Planned Codex test: Dispatch-state enforcement test.
- Planned Codex test: Replanning-delta audit.

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
- Mechanism: Give each node both a work contract and an adequacy contract so schedulability depends on authority, context, quality predicate, verification, and failure behavior.
- Mechanism: Track scheduling states such as ready, blocked by dependency, blocked by authority, blocked by context, blocked by budget, blocked by verifier, running, failed, residual, and merged.
- Mechanism: Preserve scheduling state, adequacy contracts, merge conditions, assumption refs, cost-quality ledger, residuals, and non-claims so cheap branches cannot hide displaced verification, repair, or human cleanup.
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

- A DAG schema with node-level capability, scheduling state, adequacy contracts, verification annotations, merge conditions, assumption refs, cost-quality ledger, residuals, and non-claims.
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
- Mechanism: emit lowering receipts that bind source-plan obligations, semantic atoms, target artifacts, validators, assumptions, and residuals.
- Mechanism: Preserve atom state, source-plan refs, obligation refs/status, assumptions, IR validity state, validator status, lowering state, target artifact refs, lowering receipts, repair-ledger refs, source refs, support-state effect, residuals, and non-claims so syntactic artifact acceptance cannot stand in for obligation-preserving lowering.
- Interface: Planning produces or consumes IR.
- Interface: Execution receives target-specific artifacts.
- Interface: Verification checks IR-to-output preservation.
- Interface: distinguish source-plan validity, semantic-IR validity, lowering validity, and target-artifact validation before reporting a successful compile.

Primary invariants:

- IR preserves declared requirements.
- Obligations may be refined, split, deferred, or rejected, but not silently erased.
- Repair changes are localized and auditable.
- Target compilation records assumptions.

Failure modes to cover:

- IR drift.
- Compiler hallucination.
- Repair that breaks earlier requirements.
- Compilation laundering through syntactic artifact acceptance without obligation-preserving lowering.

Draft deliverables:

- A semantic IR sketch and compile/verify/repair loop for one artifact type.
- Implemented protocol validation: `semantic_atom` fixture validates public record shape only, including atom state, source-plan refs, obligation refs/status, assumptions, IR validity state, validator status, lowering state, target artifact refs, lowering receipts, repair-ledger refs, source refs, support-state effect, residuals, and non-claims.
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
- Mechanism: Separate request validity, resolution validity, materialization validity, and adequacy validity so well-formed requests, resolved references, authorized packets, and verification-adequate packets remain distinct states.
- Mechanism: Emit context receipts with request, resolution, materialization, authority labels, support boundary, lease expiration, fault state, and residuals for replayable audits.
- Mechanism: Preserve request validity, resolution validity, materialization validity, support boundary, lease expiry, residuals, and non-claims so "context available" cannot collapse request, authority, and adequacy into one state.
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

- A context ABI table covering lifecycle state, request validity, address, version, mount scope, snapshot, resolution validity, resolver policy, representation, authority ceiling, materialization validity, adequacy requirement, consumer policy, support boundary, lease expiry, replay boundary, source refs, residuals, and fault operations.
- Implemented protocol validation: `context_abi_record` fixture validates public record shape, lifecycle state, resolver policy, mount scope, authority ceiling, adequacy requirement, replay boundary, source refs, support-state effect, and non-claims only.
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
- Mechanism: Distinguish exact carriage, lossy summary, redaction, abstraction, translation, and derived inference so each representation kind preserves its use boundary.
- Mechanism: Treat certificate updates, revocations, stale certificates, and attempted use outside the certificate as auditable state transitions rather than prose edits.
- Mechanism: link certificates to context transactions and artifact records so derived representations keep their creation/update boundary when they travel into plans, jobs, evidence, or reader editions.
- Interface: Spinoza consumes claim/evidence cells.
- Interface: Planning consumes constraints and decisions.
- Interface: Execution receives only permitted representations.
- Interface: Artifact graphs consume certificate references when context-derived representations become durable work products.

Primary invariants:

- Authority labels survive summarization.
- Loss contracts are explicit.
- A derived cell points back to source bindings.
- A derived cell points back to the transaction or artifact record that created the representation when that record exists.

Failure modes to cover:

- Summary overconfidence.
- Provenance loss.
- Authority escalation via compression.

Draft deliverables:

- A semantic-page schema with certificate fields and example source-to-summary derivation.
- Implemented protocol validation: `semantic_page_certificate` fixture validates public record shape, transaction refs, artifact refs, revocation state, and non-claims only.
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
- Mechanism: Distinguish view construction from view use: mounts, snapshot, clearance, branch, materialization, actual reads, derivatives, propagated taint, and deletion/declassification obligations.
- Mechanism: Fail closed with typed faults when mount visibility, snapshot coherence, taint propagation, or deletion closure cannot be established.
- Mechanism: record transaction validity state, isolation state, materialization state, derivative refs, declassification refs, consumer policy, verification refs, promotion blockers, replay boundary, and non-claims before a context view can feed a durable artifact.
- Interface: Planning receives consistent views.
- Interface: Security labels sensitive mounts.
- Interface: Evidence records contradictions and supersession.
- Interface: Artifact graphs reference context transactions so work products can recover the exact memory view they consumed.

Primary invariants:

- Snapshots are consistent.
- Taint propagates to derivatives.
- Deletion closure is enforced or faulted.
- Materialization state is explicit before a view is used by a downstream artifact or job.

Failure modes to cover:

- Memory poisoning.
- Stale or contradictory reads.
- Deleted data reappearing in derived summaries.

Draft deliverables:

- A transaction model for context reads, writes, branches, and deletion closure.
- Implemented protocol validation: `context_transaction_record` fixture validates public record shape, transaction state, transaction validity state, snapshot boundary, mount policy, isolation state, taint propagation, rollback/deletion closure, derivative refs, declassification refs, context ABI refs, source refs, materialization state, consumer policy, verification refs, promotion blockers, replay boundary, support-state effect, and non-claims only.
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
- Mechanism: Scope adequacy to a specific context, target claim, risk level, and verification mode.
- Mechanism: Use explicit adequacy states: absent, drafting-only, local-check, joint-check, summary-derived, escalated, or contradicted.
- Interface: VCM declares adequacy.
- Interface: Spinoza checks claims.
- Interface: Planning decides escalation when adequacy is insufficient.

Primary invariants:

- Adequacy is explicit.
- More context is not treated as proof.
- High-risk claims pay verification tax.
- Adequacy is scoped to a target claim and verification mode.
- Summary-derived support cannot exceed the declared loss and residual record.

Failure modes to cover:

- Attention interference.
- False confidence from large context.
- Verification skipped for cost reasons.
- Adequacy laundering, where a context packet adequate for drafting is reused as if it were adequate for support promotion.
- Mode confusion, where a local schema or proof check is treated as an empirical or deployment result.

Draft deliverables:

- A context adequacy rubric and verification-bandwidth warning states with claim scope, context scope, risk tier, negative evidence, verification artifact refs, audit refs, support-state effect, and non-claims.
- Exact Appendix C claim-source mappings for `verification-bandwidth-and-context-adequacy.core` across Verification Bandwidth, VCM public v1, Spinoza, TreeLLM, and editable VCM; four local raw-cache mappings are passage-reviewed, while `vcm_editable` remains connector/source-note mapped.
- Implemented protocol validation: `context_adequacy_record` fixture validates public record shape, claim scope, context packet ref, context scope, risk tier, negative evidence, verification artifact refs, audit refs, support-state effect, and non-claims only.
- Planned Codex test: Distractor resistance test.
- Planned Codex test: Adequacy labeling test.
- Planned Codex test: Verification escalation test.
- Planned Codex test: Mode-confusion audit.

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
- Mechanism: Track claim lifecycle states such as proposed, recorded, mapped, challenged, revised, downgraded, deprecated, split, merged, promoted, and retired.
- Mechanism: Preserve ledger identity across chapters, diagrams, appendices, release notes, and reader editions so confidence cannot drift through repetition.
- Mechanism: Record claim scope, surface refs, contradiction state, residual refs, changed surfaces, non-overwrite attestation, ledger effect, promotion blockers, and non-claims so repeated prose cannot launder confidence.
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

- A claim-record schema and belief-revision transition example with lifecycle state, surface identity, contradiction state, residual refs, non-overwrite attestation, ledger effect, promotion blockers, and non-claims.
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
- Mechanism: Match justification type to claim type: formal proof, citation dossier, executable procedure, replay log, benchmark artifact, or tribunal review.
- Mechanism: Record formalization mismatches, failed verification, missing artifacts, unsupported citations, and narrow successful proofs as evidence that bounds the claim rather than decorating it.
- Mechanism: Separate artifact validity from claim validity with semantic adequacy, consumer requirements, claim-validity effect, residual route, and non-claims, so a narrow proof cannot promote a broader natural-language claim.
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

- A tiered proof-carrying claim schema with one non-philosophical invariant example and explicit claim-scope, justification-type, interpretation-confidence, artifact-validity, semantic-adequacy, verifier-artifact, failed-attempt, formal-scope, consumer-requirement, claim-validity-effect, source-ref, support-state-effect, residual-route, and non-claim fields.
- Exact Appendix C claim-source mappings for `spinoza-verification-and-proof-carrying-claims.core` across Spinoza, GenesisCode, Coherence Exchange, Verification Bandwidth, and TreeLLM; four local raw-cache mappings are passage-reviewed, while `coherence_exchange` remains connector/source-note mapped.
- Implemented protocol validation: `proof_carrying_claim` fixture validates public record shape, claim scope, justification type, interpretation confidence, verifier artifact refs, failed-attempt refs, formal scope, source refs, support-state effect, and non-claims only.
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
- Mechanism: Treat tribunal review as a lifecycle: admission, dossier construction, role assignment, adversarial probing, finding capture, dissent preservation, verdict, required action, and ledger or execution update.
- Mechanism: Convert tribunal results into machine-readable constraints that can block dispatch, narrow authority, require source fetch, create residuals, or update claim state.
- Mechanism: Preserve review state, dossier boundary, reviewer independence note, cycle cap, prior review refs, unchanged-evidence guard, retrieval-expansion policy, constraint effects, and non-claims so repeated review cannot launder an unchanged evidence set into acceptance.
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

- A tribunal protocol for claim/artifact review with review lifecycle, dossier boundary, independence note, cycle cap, repeated-review guard, retrieval-expansion policy, reviewer roles, constraint effects, and output schema.
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
- Mechanism: Preserve job parentage from command contract to plan node, approval record, adapter, artifact, residual, and replay declaration so useful work cannot be laundered into governed execution without receipts.
- Mechanism: Separate delivery from evidence-ready completion: a job can produce output while still missing approval, verification, artifact capture, audit events, or replay metadata.
- Mechanism: Track lifecycle states: drafted, locked, awaiting-approval, approved, dispatchable, running, adjudicating, delivered, evidence-ready, failed/blocked, quarantined, replayed, and retired.
- Mechanism: Emit completion receipts with approval, permission, adapter, artifact, verification, audit, residual, replay/non-replay, delivery, and evidence-state fields.
- Handoff: Delivered, failed, or blocked jobs flow into artifact graphs as durable work products and audit traces.
- Interface: Planning dispatches jobs.
- Interface: Security mediates permissions.
- Interface: Artifact graph receives outputs.

Primary invariants:

- Every job has type and lifecycle state.
- Tool permissions are explicit.
- Human approval gates block high-impact jobs.
- Delivered output is not evidence-ready until verification, artifact capture, audit, residual, and replay/non-replay fields are present.
- Job parentage remains traceable to contract, plan node, approval, adapter, artifact, and residual.

Failure modes to cover:

- Tool overreach.
- Unlogged side effects.
- Infinite or chaotic agent swarms.
- Completion laundering, where output existence is treated as governed evidence.
- Parentage loss, where a job cannot be traced back to the command contract and dispatchable plan node that authorized it.

Draft deliverables:

- A typed-job schema with lifecycle states and permission checks.
- Exact Appendix C claim-source mappings for `labor-os-and-typed-jobs.core` across Talos, VIEA, GenesisCode, Software Magic Grimoire, Talos Markdown, and MoECOT; four local raw-cache mappings are passage-reviewed, while `talos_md` and `moecot` remain connector/source-note mapped.
- Implemented protocol validation: `typed_job` fixture validates public record shape only.
- Implemented Lean predicate: a transition record marked valid must use the declared finite lifecycle relation.
- Planned Codex test: Tool permission enforcement test.
- Implemented Lean predicate: an approval-required job cannot be allowed to run before approval is recorded.
- Planned Codex test: Delivery versus evidence-ready test.
- Planned Codex test: Job parentage trace test.

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
- Mechanism: link artifact nodes to context transaction refs and semantic certificate refs so artifact reuse preserves the memory and representation boundaries it inherited.
- Mechanism: require replay grade, evidence gate, residuals, and non-claims before an artifact can influence claim support, compression, procedural memory, or release records.
- Handoff: Runtime adapters produce effect receipts and residuals that must return to the artifact graph before they become evidence.
- Interface: VCM references artifacts.
- Interface: Evidence consumes logs.
- Interface: Procedural memory mines repeated traces.
- Interface: Reader and release editions consume artifact records only through declared replay grade and evidence gate.

Primary invariants:

- Artifacts have stable identities.
- Audit logs are append-only or versioned.
- Replay limits are declared.
- Replay grade and evidence gate are declared before artifact reuse can affect support state.

Failure modes to cover:

- Untraceable output.
- Non-replayable workflow.
- Provenance gaps.

Draft deliverables:

- An artifact graph schema with job, source, context, context-transaction, semantic-certificate, replay, and evidence edges.
- Passage-reviewed Appendix C mappings for six local raw-cache sources: `talos`, `viea`, `cognitive_compilation`, `spinoza_composer`, `genesiscode`, and `cognitive_loop_closure`; `moecot` remains connector/source-note mapped until durable runtime artifacts, ledgers, logs, benchmark records, or replay records are imported and inspected.
- Implemented protocol validation: `artifact_graph_record` fixture validates public record shape, context transaction refs, semantic certificate refs, replay grade, evidence gate, residuals, and non-claims only.
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
- Mechanism: Keep job request, approval decision, effect receipt, verification result, rollback handle, and irreversible residuals as separate artifacts.
- Mechanism: Treat approval as scoped to target, risk tier, expiration, permitted reuse, and revocation path.
- Handoff: Repeated adapter traces and repair patterns become candidates for procedural memory only after evidence and regression checks exist.
- Interface: Execution owns adapters.
- Interface: Security mediates secrets.
- Interface: Evidence records deployment outcomes.

Primary invariants:

- No adapter executes beyond granted scope.
- High-impact actions require approval.
- Rollback handles are captured when available.
- Approval scope expires and does not authorize unrelated reuse.
- Effect receipts separate request, approval, execution, verification, and rollback state.

Failure modes to cover:

- Tool overreach.
- Approval bypass.
- Irreversible deployment without rollback.
- Approval laundering, where a narrow human approval is reused as broad authorization.
- Receipt laundering, where a successful tool response is treated as verified task success.

Draft deliverables:

- A runtime-adapter contract with permissions, approval requirements, invocation state, impact class, risk tier, effect lease, pre/post state refs, external side effects, verification refs, rollback and irreversible residual fields, incident/audit refs, support-state effect, and non-claims.
- Exact Appendix C claim-source mappings for `runtime-adapters-tool-permissions-and-human-approval.core` across Talos, VIEA, Ladon/Manhattan, Software Magic Grimoire, GenesisCode, MoECOT, Field of God AI Constitution, and Theseus Operator OS; five local raw-cache mappings and two local public-project mappings are passage-reviewed, while `moecot` remains connector/source-note mapped.
- Implemented protocol validation: `runtime_adapter_invocation` fixture validates public record shape, invocation state, impact class, risk tier, approval scope/expiry, effect lease, pre/post state refs, external side effects, verification refs, irreversible residuals, incident/audit refs, support-state effect, and non-claims only.
- Implemented Lean predicate: a valid invocation requires the parent job permissions to include the adapter capability.
- Implemented Lean predicate: a high-impact adapter invocation without approval is rejected.
- Planned Codex test: Rollback handle capture test.
- Planned Codex test: Approval-scope expiry test.
- Planned Codex test: Effect-receipt completeness test.

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
- Mechanism: Track procedure-qualification states such as candidate trace, loop cluster, tool candidate, verified reuse, routable, quarantined, and retired so a useful trace cannot jump directly into reusable behavior.
- Mechanism: Emit a Procedure Qualification Packet with candidate traces, rejected traces, near misses, abstraction rationale, parameter-discovery notes, SCF target, benchmark floor, authority requirement, monitoring signal, retirement trigger, and explicit non-claims.
- Handoff: Verified procedural tools become routable candidates for Part III, while failed or uncertain loops remain residuals.
- Interface: Artifact graph supplies traces.
- Interface: Routing selects new tools.
- Interface: Evidence tests utility and regressions.

Primary invariants:

- Only verified loops become tools.
- Parameters and assumptions are explicit.
- Tool promotion records residuals and regressions.
- Negative examples stay attached to the reusable procedure.
- Retirement triggers are part of the tool definition.

Failure modes to cover:

- Premature toolification.
- Hidden assumptions.
- Procedural memory poisoning.
- Anecdote closure, where one appealing trace becomes a tool without a comparable trace cluster.
- Route drift outside the SCF, benchmark floor, or authority envelope.

Draft deliverables:

- A loop closure pipeline from trace detection to verified tool record.
- Exact Appendix C claim-source mappings for procedural memory: five local raw-cache mappings and three local public-project mappings are passage-reviewed, while `moecot` remains connector/source-note mapped only.
- Implemented protocol validation: `procedural_tool_record` fixture validates public record shape only.
- Planned Codex test: Loop detection test.
- Planned Codex test: Procedure qualification state test.
- Planned Codex test: Negative-example preservation test.
- Planned Codex test: Tool abstraction test.
- Planned Codex test: Verified tool regression test.
- Planned Codex test: Retirement trigger test.

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
- Mechanism: emit route receipts that record selected specialist, rejected candidates, granted authority subset, denied authority, context lease, tool lease, readiness state, verifier requirement, budget, fallback, expiry, and residual owner.
- Mechanism: record non-selection evidence so rejected candidates inform readiness, resource policy, and future routing.
- Mechanism: Preserve registry epoch, owner, authority envelope, memory/tool lease policies, route limitations, route receipt, residual owner, and non-claims so selected and rejected specialists remain inspectable after the route expires.
- Handoff: Failed or uncertain routes flow to readiness gates, residual escrow, fallback routes, or tribunal/review rather than ordinary execution.
- Interface: Planning requests capabilities.
- Interface: Governance bounds specialists.
- Interface: Evidence updates readiness.
- Interface: artifact graphs and evidence ledgers retain route receipts for downstream claim traceability.

Primary invariants:

- Specialist authority is local.
- Routing decisions are logged.
- Fallback paths remain available.
- The router selects the least-capable adequate specialist unless task risk, context demand, verifier requirement, or fallback policy justifies broader capability.

Failure modes to cover:

- Wrong specialist selection.
- Router overconfidence.
- Specialist authority leak.
- Route laundering: broad successful routes justify broader authority without proving narrower specialists were inadequate.

Draft deliverables:

- A router registry with capability metadata, cost, authority, leases, route limitations, route receipts, non-selection evidence, expiry, residual ownership, and fallback rules.
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
- Mechanism: record scoped lifecycle transitions with authority envelope, freshness window, workload family, fallback path, expiry, floor evidence, frontier evidence, and inherited residuals.
- Mechanism: expose allowed routes, blocked routes, fallback path, expiry, inherited residuals, and non-claims so canary or diagnostic permission cannot be mistaken for default readiness.
- Mechanism: Separate evidence state, floor evidence, frontier evidence, diagnostic permissions, and closure conditions so fixture validation, source-reported gates, and reproduced readiness cannot collapse into one status.
- Handoff: Runtime references such as MoECOT must emit the gate, replay, benchmark, residual, and promotion-blocker records that readiness decisions require.
- Interface: Routing reads readiness.
- Interface: Benchmarks update gates.
- Interface: SCFs govern replacement.
- Interface: expose lifecycle states such as draft, shadow, canary, qualified, default, diagnostic-only, quarantined, retired, and superseded for router/auditor consumption.
- Interface: artifact graphs and benchmark ledgers preserve gate records so renamed, wrapped, split, merged, or retired modules cannot shed old residual escrow.

Primary invariants:

- Promotion requires gate evidence.
- Residuals are not deleted on promotion.
- Quarantine blocks ordinary routing.
- Stronger readiness requires adequate added evidence or narrower permitted scope; readiness cannot increase by losing records.
- Inherited residuals survive rename, wrapper, split, merge, retirement, and retraining unless an explicit retirement record closes them.

Failure modes to cover:

- Premature promotion.
- Residual hiding.
- Untracked regression after merge.
- Gate laundering through rename, wrapper, merge, split, or retirement without inherited residual escrow.

Draft deliverables:

- A module lifecycle state machine and residual escrow ledger with evidence state, floor/frontier evidence, diagnostic permissions, closure conditions, inherited residuals, expiry, and non-claims.
- Exact Appendix C claim-source mappings for readiness gates: five local raw-cache mappings and three local public-project mappings are passage-reviewed, while `moecot` remains connector/source-note mapped only until runtime/source artifacts, readiness records, ledgers, replay logs, benchmark records, or external corroboration are imported and inspected.
- Implemented protocol validation: `readiness_gate_record` fixture validates public record shape, field identity, workload family, freshness window, route permissions, inherited residuals, fallback path, expiry, and non-claims only.
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
- Mechanism: separate source-reported, locally reproduced, externally corroborated, and blocked fields inside each runtime evidence packet.
- Mechanism: record cold-start-to-handoff traces, including denied routes, failed gates, missing replay refs, unresolved handoffs, and residual branches.
- Mechanism: Preserve runtime packet state, route authority ledger, denied routes, failed gates, missing replay refs, source-reported fields, locally reproduced fields, externally corroborated fields, blocked fields, and non-claims so a runtime name cannot stand in for replay or benchmark evidence.
- Handoff: A concrete runtime must still land on an owned, leased, or project compute substrate whose reachability does not imply authority.
- Interface: Routing selects cores.
- Interface: SCFs govern replacement.
- Interface: Evidence and replay ledgers evaluate runtime changes.
- Interface: route authority ledger records command authorization, specialist authority envelopes, tool and memory permissions, and denied authority changes.

Primary invariants:

- MoECOT claims stay at argument level until source notes exist.
- Implementation evidence is separated from design argument.
- Runtime promotion follows readiness gates.
- Runtime evidence states remain separate across design example, reproduced artifact, benchmark evidence, and blocked source field.

Failure modes to cover:

- Overclaiming unavailable source content.
- Treating implementation branding as architecture proof.
- Losing cross-layer traceability.
- Replay theater that preserves successful paths while omitting failed gates, denied routes, human interventions, missing sources, and residual cases.

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
- Mechanism: Treat compactness as a governed claim over seed, rule system, memory state, generator/decoder/controller, generation status, correction mechanism, verifier, verification status, verifier independence, residual channel, fallback path/status, residual-burden status, governance interface, authority boundary, use envelope, burden ledger, evidence/cost ledger, promotion blockers/state, source refs, support-state effect, and non-claims.
- Mechanism: Use the seed/router/search/generator/verifier/residual loop to expose generation cost, verification cost, correction burden, hidden complexity, and authority limits before promotion.
- Mechanism: Separate reconstruction burden, decision burden, and governance burden so compactness is judged by total recorded cost rather than seed size.
- Mechanism: Require verifier separation and use envelopes so compact cores cannot self-promote their own adequacy for evidence, runtime, or replacement claims.
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

- A compactness ledger with seed, router/index, search/planning, generator/decoder, verifier/critic, residual correction, memory/governance hooks, authority boundary, use envelope, burden ledger, exact remainder, verification, support-state effect, and residual fields.
- Implemented repository-level fixture: `compact_generative_record.valid.json` validates the compact-generative record shape, generation status, verification status, fallback status, residual-burden status, correction mechanism, verifier independence, authority boundary, use envelope, burden ledger, cost accounting, promotion blockers/state, source refs, support-state effect, and non-claims only; utility and residual-burden behavior remain planned tests.
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
- Mechanism: Record a compression receipt with receipt state, reconstruction contract, public law family, seed, search bound, generated regions, verification result, exact repair residual, fallback threshold, interface costs, consumer policy, use permissions, proxy-rate status, final-serialization status, rate accounting, support-state effect, evidence refs, and non-claims.
- Mechanism: Separate proxy/search-rate estimates from final serialized costs, and record literal fallback or negative results when repair and metadata erase the saving.
- Mechanism: Treat compression as a transaction with candidate, verified-exact, verified-lossy, repaired-exact, literal-fallback, and quarantined states.
- Mechanism: Scope compressed outputs by consumer policy so preview, routing, proof, audit, citation, benchmark, training, and exact-replay uses cannot borrow each other's authority.
- Handoff: The same draft/verify/repair accounting becomes accepted-output and verifier-cost accounting in fast generation.
- Interface: Evidence measures reconstruction and utility.
- Interface: Routing chooses compressed or full representation.
- Interface: VCM uses summaries with loss contracts.

Primary invariants:

- Verification precedes exactness claims.
- Repair cost is counted.
- Search bounds are explicit.
- Consumer use is scoped to the reconstruction contract and declared loss.
- Negative rate results are preserved instead of rewritten as narrative success.

Failure modes to cover:

- Unbounded search.
- Verification skipped.
- Repair larger than original data.
- Consumer-policy leakage, where a lossy or preview representation is reused for exact, audit, proof, or benchmark work.
- Proxy-rate drift, where search-time savings survive in prose after final serialization erases them.

Draft deliverables:

- A compression record with generator, verification result, repair residual, fallback threshold, consumer policy, use permissions, proxy/final-rate status, and support-state effect.
- Implemented repository-level fixture: `compression_receipt.valid.json` validates receipt state, search bound, interface costs, consumer policy, use permissions, proxy-rate status, final-serialization status, rate accounting, support-state effect, evidence refs, and non-claims only; no codec, reconstruction benchmark, or rate experiment exists yet.
- Implemented Lean predicate: exact reconstruction claims require generator output plus repair residual to equal the target in a finite record.
- Implemented Lean predicate: failed verification blocks exactness promotion.
- Planned Codex test: Reconstruction quality test.
- Planned Codex test: Repair-cost accounting test.
- Planned Codex test: Bounded-search failure test.
- Planned Codex test: Consumer-policy enforcement test.

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
- Mechanism: Treat compressed artifacts as routed representation candidates with preserved full-artifact fallback, task family, access pattern, admission state, reconstruction contract, declared use envelope, codec parameters, metadata costs, residual coding, probe plan, fallback trigger, decode determinism, exact-replay status, consumer policy, utility tests, support-state effect, evidence refs, and non-claims.
- Mechanism: Separate representation, reconstruction, compression-ratio, and downstream-utility claims so one passing property cannot promote the others.
- Mechanism: Keep compression, reconstruction, residual, utility, cost, and fallback ledgers separate so a smaller representation cannot silently become a stronger evidence object.
- Mechanism: Require compressed records to state the declared use envelope, probe boundary, fallback trigger, and non-claims before downstream agents can use the compressed form.
- Mechanism: Add artifact-admission states for not-admitted, cold-archive candidate, preview-only, task-probe-passed, exact-replay-ready, fallback-dominant, and decoder-quarantined compressed forms.
- Mechanism: Declare access patterns such as cold archive, warm retrieval, hot planning context, exact replay, semantic preview, benchmark input, and audit before choosing a compressed route.
- Handoff: Semantic representation inherits the same probe discipline, but the risk shifts from bit-level reconstruction to grounding and hierarchy drift.
- Interface: Artifact graph stores compressed and full references.
- Interface: Routing selects representation by task.
- Interface: Evidence records latency, ratio, and utility.

Primary invariants:

- Fallback path is known.
- Residual coding is measured.
- Downstream utility is tested.
- Admission state is task-relative and access-pattern-relative.
- A compressed artifact cannot replace the full artifact as evidence unless the exact replay or declared-use gate passed.

Failure modes to cover:

- Compression damaging rare critical cases.
- Probe not representative.
- Latency gains erased by fallback.
- Archive-policy leakage, where cold-storage assumptions are reused for hot-path reasoning.
- Evidence substitution, where a compressed preview is cited as if it were the preserved source artifact.

Draft deliverables:

- A compressed artifact record with task family, access pattern, admission state, ratio, metadata costs, residual, probe, fallback trigger, exact-replay status, consumer policy, support-state effect, and utility fields.
- Implemented repository-level fixture: `compressed_artifact_record.valid.json` validates the artifact-compression record shape, task family, access pattern, admission state, declared use envelope, metadata costs, fallback trigger, exact-replay status, consumer policy, support-state effect, evidence refs, and non-claims only; no decoder, corpus benchmark, or downstream utility probe exists yet.
- Planned Codex test: Compression ratio test.
- Planned Codex test: Probe-route fallback test.
- Planned Codex test: Downstream utility preservation test.
- Planned Codex test: Access-pattern admission test.

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
- Mechanism: Track semantic-node lifecycle states: proposed, grounded, adequate-for-task, interoperable, superseded, stale, and quarantined.
- Mechanism: Require consumer-specific policies for VCM, claim ledgers, planning, cognitive compilation, compression, and human-reader explanation.
- Handoff: Resource economics decides when semantic compression is actually cheaper after verification burden, repair, and downstream failures are counted.
- Interface: Spinoza uses semantic claims.
- Interface: VCM stores semantic pages.
- Interface: Compression tests representation efficiency.

Primary invariants:

- Semantic nodes are grounded or labeled speculative.
- Hierarchy changes are versioned.
- Representation claims require tests.
- Shared semantic graphs remain indexes and working representations, not independent source authorities.
- Consumer use is scoped by grounding, adequacy, interoperability, and permitted-use fields.

Failure modes to cover:

- Hand-built ontology brittleness.
- False explainability.
- Hierarchy drift.
- Graph migration debt, where downstream consumers keep using stale node meanings.
- Semantic laundering, where a clean path explanation is cited instead of the source, proof, or test it was meant to index.

Draft deliverables:

- A semantic-node schema and evaluation plan for one grounded domain.
- Implemented repository-level fixture: `semantic_node_record.valid.json` validates the semantic-node record shape only; no TreeLLM implementation, grounding benchmark, or hierarchy-revision harness exists yet.
- Planned Codex test: Grounding fidelity test.
- Planned Codex test: Hierarchy revision test.
- Planned Codex test: Representation utility benchmark.
- Planned Codex test: Consumer-policy test.

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
- Mechanism: Treat security overhead, approval overhead, replay cost, human review, repair burden, and non-action costs as budget fields rather than invisible externalities.
- Mechanism: Prevent efficiency laundering: cheaper routes that shift work into future debugging, hidden human repair, lost evidence, or unrecorded security risk must emit residual costs or be rejected.
- Mechanism: Track budget adjudication states such as proposed, priced, underfunded, protected-overhead-required, dispatchable, escalated, deferred, scope-reduced, rejected, and residualized.
- Mechanism: Record displaced costs from future debugging, reviewer burden, hidden context reconstruction, private-data exposure, benchmark contamination, rollback difficulty, or evidence loss before accepting a cheaper route.
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
- Protected overhead is budgeted explicitly and cannot be silently deleted.
- Displaced costs remain residuals until measured or accepted by a scoped evidence transition.

Failure modes to cover:

- Cost-cutting verification away.
- Load-synchronized degradation.
- Resource hoarding by low-value tasks.
- Aggregate serving throughput mistaken for lower single-request risk or better answer quality.
- Protected-overhead deletion.
- Review-capacity capture.

Draft deliverables:

- A resource ledger with budget, risk, cost, quality, and verification tax fields.
- Implemented repository-level fixture: `resource_budget_record.valid.json` validates the budget-record shape, including budget state, protected overhead, and displaced costs only; no TokenMana simulation, PlanForge scheduler benchmark, protected-overhead accounting test, displaced-cost residual test, or welfare/load study exists yet.
- Planned Codex test: Budget allocation test.
- Planned Codex test: Risk-adjusted verification test.
- Planned Codex test: Protected-overhead accounting test.
- Planned Codex test: Displaced-cost residual test.
- Planned Codex test: Review-capacity hoarding test.
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
- Mechanism: emit fidelity receipts that record contract version, claim class, fidelity state, assumptions, omitted variables, resource bill, observed result boundary, claim boundary, transfer decision, support-state effect, failure behavior, instrumentation effects, and non-claims.
- Interface: Efficiency theory uses resource constraints.
- Interface: Benchmarks record fidelity limits.
- Interface: Alignment scenarios avoid unbounded simulation claims.
- Interface: classify simulation results as invariant checks, benchmark comparisons, feasibility estimates, scenario explorations, safety rehearsals, or speculative thought experiments.

Primary invariants:

- Fidelity is declared.
- Resource bounds are explicit.
- Speculative simulation metaphysics stays separated from engineering claims.
- Simulation results do not transfer beyond the declared claim boundary by default.

Failure modes to cover:

- Overclaiming nested simulation feasibility.
- Ignoring resource ceilings.
- Treating approximate simulations as ground truth.
- Simulation laundering: clean synthetic results described as if omitted variables, bottlenecks, and transfer limits were irrelevant.

Draft deliverables:

- A simulation-fidelity checklist and cost/fidelity table for experiment design.
- Implemented repository-level fixture: `simulation_contract_record.valid.json` validates the simulation-contract record shape, claim class, fidelity state, transfer decision, support-state effect, failure behavior, instrumentation effects, and non-claims only; no feasibility calculator, simulation benchmark, or external physical-computation audit exists yet.
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
- Mechanism: Require expected advantage, ordinary baselines, negative controls, proof boundary, workload, metric, report, consumer gate, axis ledger, non-claims, and falsification condition before canary use.
- Mechanism: Route experiments through exploratory, canary, qualified, retired, or blocked evidence gates before broader adoption.
- Mechanism: Keep backbone efficiency, proof readiness, fast-generation acceleration, compression, search quality, routing quality, and downstream task quality as separate axes.
- Mechanism: Treat optionality as a positive adoption state so promising substrates can be tested through narrow routes without becoming load-bearing architecture before evidence exists.
- Mechanism: treat adoption records as routing permissions with operational states such as exploratory, structural-only, canary, qualified-for-scope, blocked, retired, or superseded, using machine-readable values such as `structural_only` and `qualified_for_scope`.
- Mechanism: maintain a four-lane adoption packet for structural facts, empirical workload evidence, consumer permissions, and retirement/falsification behavior.
- Interface: Routing treats substrate as specialist.
- Interface: Compression tests representation efficiency.
- Interface: Evidence compares against baselines.
- Interface: Fast-generation routes may consume substrate evidence, but adoption remains gated by substrate-specific A/B records.
- Interface: maintain an axis ledger for structure, speed, memory, routing quality, compression quality, search quality, verifier burden, and downstream task quality.
- Interface: require consumer gates, consumer policies, routing-permission effects, fallback substrates, and retirement/supersession paths so a substrate record can support structural discussion without supporting routing, compression, runtime, or model-quality promotion.

Primary invariants:

- Exploratory claims stay exploratory.
- Baselines are recorded.
- Failed hypotheses remain visible.
- Backbone-efficiency claims do not imply search, routing, compression, or reasoning-quality gains.
- Negative controls remain attached after favorable results.
- A consumer may not rely on an unmeasured, blocked, or explicitly excluded substrate axis.

Failure modes to cover:

- Performance overclaiming.
- Opaque math treated as proof.
- Adoption without regression tests.
- Sequence-model throughput treated as evidence for unrelated substrate quality.
- Theorem spillover: structural proofs are used to imply speed, search, compression, or reasoning quality.

Draft deliverables:

- A technical-substrate appendix plan with experiment matrix and adoption gates.
- Implemented repository-level fixture: `substrate_adoption_record.valid.json` validates substrate-adoption record shape, baseline obligations, consumer gate/policy, axis ledger, routing-permission effect, fallback substrate, retirement/supersession path, support-state effect, and non-claims only; no A/B run, representation-efficiency benchmark, CoilMoECOT benchmark, or local Circle build exists yet.
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
- Mechanism: Separate proof authority from consumer authority: theorem-linked structural facts can be necessary for downstream use but never sufficient for substrate promotion.
- Mechanism: Record proof policy, source version, content fingerprint, resolver status, validation command, failure behavior, consumer requirements, and non-claims so stale references become visible residuals.
- Mechanism: treat proof-contract receipt states such as theorem-linked, dictionary-bound, fingerprinted, resolver-checked, consumer-gated, workload-blocked, and retired/superseded as transport states rather than model-quality states.
- Interface: Lean and proof manifests supply theorem status.
- Interface: Python or CLI tools emit receipts and validation reports.
- Interface: Theseus-style private experiments consume contracts without importing private results into public claims.
- Interface: The evidence matrix records claim boundaries and support states.
- Interface: `proof_contract_receipt_record` records receipt state, finite-model scope, proof boundary, theorem refs, proof status, source version, fingerprint field/status, deterministic fields, verifier state, resolver/replay state, consumer gate/state, staleness policy, failure behavior, source refs, support-state effect, evidence refs, and non-claims.

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

- A contract record with theorem IDs, receipt state, proof boundary, proof status, content fingerprint, fingerprint status, deterministic fields, validation commands, consumer check/state, ordinary baselines, resolver/replay states, staleness policy, support-state effect, and non-claims.
- Implemented repository-level fixture: `proof_contract_receipt_record.valid.json` validates proof-contract receipt record shape, receipt state, proof boundary, fingerprint status, consumer state, staleness policy, source refs, support-state effect, and non-claims only; no Circle theorem-id resolver, receipt replay, fingerprint check, external Lean build, or generated contract pack exists yet.
- Implemented repository-level fixture: `proof_target_record.valid.json` validates proof-record fields only; no Circle theorem-id resolver, receipt replay, fingerprint check, or vendored contract pack exists yet.
- Implemented Lean predicates: `AsiStackProofs.ProofCarryingContracts` proves local finite-record receipt-boundary and consumer-gate promotion requirements without claiming external Circle theorem replay.
- Implemented Codex test: Proof contract receipt schema validation test.
- Planned Codex test: Circle contract pack validation test
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
- Mechanism: treat cyclic and sparse memory contracts as admission-control structures with memory-authority scope, VCM packet chain-of-custody, state-carry boundaries, stale-read policy, recurrence work budgets, baseline obligations, non-widening authority, and workload-evaluation eligibility.
- Interface: VCM context traces expose context adequacy and authority labels.
- Interface: Attention and memory modules consume contract fields as diagnostic guardrails.
- Interface: Benchmark adapters and Theseus transfer lanes decide whether structural facts survive actual workloads.
- Interface: Proof contracts define the finite boundary of the claim.
- Interface: memory-contract records include baseline obligations before improvement claims are considered.

Primary invariants:

- Residue-only aliasing remains visible.
- Full structural coverage is not semantic coverage.
- Recurrence budgets include exits and guardrails.
- Stale reads fail closed or enter residual escrow.
- Mapping governed context into slots, recurrence traces, or compressed attention cannot widen authority, lease, permitted use, or adequacy.

Failure modes to cover:

- Alias hiding.
- Overthinking or non-terminating recurrence loops.
- Uncovered sparse-attention lags.
- Freshness facts treated as retrieval-quality evidence.
- No ordinary baseline controls.
- Structural adequacy laundering, where freshness, coverage, or loop-exit facts are treated as workload adequacy.

Draft deliverables:

- A contract-backed memory and attention evaluation plan with slot, winding, coverage, freshness, active-token, loop-exit, work-budget, and baseline fields.
- Implemented repository-level fixture: `cyclic_memory_contract.valid.json` validates the cyclic-memory record shape, memory-authority scope, VCM packet refs, state-carry boundary, stale-read policy, admission state, baseline refs, probe requirements, authority non-widening, residuals, and non-claims only; no KV-cache freshness checker, sparse-coverage harness, recurrence benchmark, or learned-memory workload exists yet.
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
- Mechanism: use cyclic tradeoff packets with structural receipts, workload target, receipt refs, baseline set, baseline-symmetry policy, negative controls, resource costs, metrics status, consumer policy, hardware refusal path, adoption rationale, and non-claims.
- Interface: Semantic representation chapters define when cyclic structure is actually present.
- Interface: Routing heads or rankers may consume cyclic features only inside declared authority and evidence boundaries.
- Interface: Resource-economics chapters account for parameters, kernels, memory, and latency.
- Interface: Proof contracts and prototype experiments keep structural facts separate from performance results.
- Interface: consumers can accept a structural receipt for diagnostics, reject it for quality promotion, or require benchmark evidence before canary routing.

Primary invariants:

- Equivariance is not model quality.
- Parameter reduction is not an adoption proof.
- Winding is not discarded when it is required to avoid aliasing.
- Hardware-friendly sizes and kernel costs are recorded.
- Real-valued RoPE claims are separated from exact integer phase-bank claims.
- Baseline symmetry is required before a cyclic tradeoff is called favorable.

Failure modes to cover:

- Mathematical elegance outruns kernels and baselines.
- Exact finite proofs are overclaimed for real-valued RoPE deployments.
- Lower parameter count comes with worse quality or runtime.
- Phase aliases are hidden by residue-only diagnostics.
- Cyclic favoritism: theorem language, tuned hyperparameters, or custom hardware assumptions benefit the cyclic candidate while baselines are weakened.

Draft deliverables:

- A mixer and position-substrate experiment matrix with structural proof references, ordinary baselines, quality/runtime/memory/parameter metrics, alias and load diagnostics, and explicit non-claims.
- Implemented repository-level fixture: `cyclic_mixer_evaluation_record.valid.json` validates the cyclic-mixer evaluation record shape, evaluation state, workload target, receipt refs, claim partition, hardware refusal path, baseline matrix refs, baseline symmetry, negative controls, failure-case refs, resource costs, metrics status, tradeoff packet ref, consumer policy, adoption rationale, source refs, support-state effect, and non-claims only; no RoPE certifier run, MLX experiment, hardware-kernel benchmark, or model-quality evaluation exists yet.
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
- Mechanism: Lower each formal-looking chapter claim into a Proof Target Record with tag, artifact lane, module or artifact path, formal target, verifier command/result, support-state effect, consumer requirements, semantic adequacy state, limitations, and non-claims.
- Mechanism: Keep `proofs/proof_manifest.json` generated from outline `lean:*` tags and require traceability through triage records, Lean modules, root imports, chapter hooks, limitation prose, and Appendix E before calling a target implemented.
- Mechanism: Route candidates to Lean predicates, executable schemas, fixture validators, process contracts, research targets, blocked targets, or retired targets according to what can actually be checked.
- Mechanism: Keep semantic proof adequacy as a separate review from build success, schema success, source interpretation, deployed enforcement, model quality, or benchmark evidence.
- Mechanism: Treat the proof envelope as a lane discipline: Lean proves finite predicates, schemas validate record shape, process validators check wiring, tests exercise behavior, and benchmarks measure performance without collapsing those artifacts into one support state.
- Mechanism: emit proof/spec receipts with command, artifact path, predicate or schema covered, consumer requirements, limitations, and explicit non-claims.
- Mechanism: route semantic proof drift into adequacy residuals when a valid finite predicate may not match the intended chapter boundary.
- Mechanism: keep `artifact_lane` separate from `target_kind` so schema, Lean, process validator, behavior test, benchmark, external-reference, and research-backlog receipts cannot borrow one another's authority.
- Interface: Outline defines proof scope.
- Interface: Lean modules implement selected invariants.
- Interface: Validation checks proof-manifest consistency.
- Interface: consumers may rely on a proof only when proof lane, command, artifact path, version, and non-claims match their required use.
- Interface: proof consumers must also respect semantic adequacy state before using a finite predicate to strengthen prose.

Primary invariants:

- No theorem is claimed proven without `lake build`.
- Proof tags remain stable.
- Broad claims are decomposed before formalization.
- Formal artifacts require semantic adequacy notes before strengthening prose beyond their finite predicates.

Failure modes to cover:

- Formalization theater.
- Unstable proof target names.
- Claiming proof from prose.
- Proof laundering: valid local predicates, external theorem ids, generated receipts, or schema passes promote broader claims whose semantics were not formalized.

Draft deliverables:

- A proof manifest, Lean workspace, first invariant modules, and proof target record schema for support-state and authority checks.
- Implemented repository-level fixture: `proof_target_record.valid.json` validates proof-target record shape, artifact lane, consumer requirements, semantic adequacy state, limitations, and non-claims only.
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
- Mechanism: Use explicit benchmark evidence states such as candidate metric, schema-fixture pass, synthetic probe, source-reported, locally reproduced, regression floor, frontier probe, contaminated, blocked, and retired so fixture/build/source status cannot masquerade as empirical capability evidence.
- Mechanism: Emit a Benchmark Ratchet Packet with evidence class, benchmark ownership, run command, environment, baseline, public-calibration boundary, contamination surface, hidden/transfer status, exact movable claim, exact non-claims, reviewer decision, residual escrow, and support-state effect.
- Interface: Routing and SCFs use readiness gates.
- Interface: Evidence matrix records support movement.
- Interface: Changelog records evidence changes.

Primary invariants:

- No test success is claimed without execution.
- Synthetic and empirical evidence remain distinct.
- Regressions are preserved.
- Source-reported, synthetic, fixture, reproduced, and empirical results remain separate evidence classes.
- Saturated benchmarks become regression floors rather than broad readiness claims.

Failure modes to cover:

- Benchmark overfitting.
- Hidden regression deletion.
- Claim support inflation.
- Evidence-class collapse.
- Floor/frontier inversion.

Draft deliverables:

- A benchmark ratchet record schema with frontier, mastery, residuals, regressions, promotion decisions, and anti-Goodhart checks.
- Implemented repository-level fixture: `benchmark_ratchet_record.valid.json` validates benchmark-ratchet record shape only; no benchmark run, contamination audit, hidden-transfer test, or regression-preservation test exists yet.
- Planned Codex test: Saturation detection test.
- Planned Codex test: Hidden benchmark transfer test.
- Planned Codex test: Contamination audit test.
- Planned Codex test: Floor/frontier split test.
- Planned Codex test: Source-reported boundary test.
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
- Mechanism: Record update state, policy delta, feedback source/admissibility, reward/preference signal, reward boundary, verifier refs, reward-hacking probes, update constraint, drift bound, holdouts, regressions, evaluation refs, governance gates, authority effect, rollback plan, monitor window, evidence packets, deployment scope, support-state effect, residuals, and non-claims.
- Mechanism: Choose a training/update family by the policy being optimized, the feedback available, and the failure mode that must be blocked.
- Mechanism: Keep REINFORCE/RLOO/ReMax-style policy gradients, TRPO/PPO-style trust-region updates, GRPO/DAPO/GSPO-style group or sequence updates, DPO/IPO/ORPO/KTO/SimPO-style offline preference optimization, RLVR, reasoning-budget RL, router-policy RL, and context-policy RL as method families, not unsupported result claims.
- Mechanism: treat policy updates as behavior-change leases with target layer, evaluation scope, drift bound, rollback condition, monitor window, and promotion gate.
- Mechanism: emit policy-delta receipts that record behavior changes, admissible feedback, reward boundary, reward-hacking probes, holdouts, regressions, unchanged authority boundary, monitor window, evidence packet, deployment scope, support-state effect, and rollback restoration path.
- Interface: Benchmarks and verifiers produce reward or preference signals.
- Interface: VCM and artifact graphs preserve training/evaluation context and evidence references.
- Interface: Talos records training, tool, and evaluation artifacts.
- Interface: Spinoza and UAT audit reward meaning, failed verifiers, and reward-hacking probes.
- Interface: SCF gates decide promotion, quarantine, rollback, or continued experiment status.
- Interface: distinguish training evidence, evaluation evidence, governance evidence, deployment evidence, rollback evidence, and long-term safety evidence.

Primary invariants:

- Reward is not evidence unless the verifier and evaluation boundary are recorded.
- Policy updates cannot expand authority by training side effect.
- A faster or shorter policy is not promoted unless task success and regressions are preserved.
- Reward-hacking probes are part of the update record, not optional commentary.
- Rollback remains available for promoted updates.
- Proxy improvement cannot promote the target claim without target-specific evaluation, residuals, and failure probes.

Failure modes to cover:

- Reward hacking or verifier gaming.
- Over-optimization for preference style rather than truth or task success.
- Planner, router, or context policies learning hidden shortcuts.
- Latency rewards suppressing needed verification.
- Policy drift crossing SCF authority or readiness boundaries.
- Reward laundering: proxy improvement is written up as task improvement while reward hacks, preference bias, verifier blind spots, or regression losses remain unresolved.

Draft deliverables:

- A policy optimization record schema with update state, target layer, policy delta, feedback source/admissibility, reward signal/boundary, verifier refs, reward-hacking probes, update constraint, drift bound, holdouts, regressions, evaluation refs, governance gates, authority effect, rollback plan, monitor window, evidence packet refs, deployment scope, support-state effect, residuals, and non-claims.
- Implemented repository-level fixture: `policy_optimization_record.valid.json` validates update state, policy delta summary, feedback admissibility, reward boundary, reward-hacking probes, holdouts, regressions, authority effect, monitor window, evidence packet refs, deployment scope, support-state effect, and non-claims only; no PPO, DPO, GRPO, RLVR, router-policy, context-policy, or reasoning-budget experiment has been run.
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
- Mechanism: Represent the integrated stack as a Reference Trace Record that names trace state, execution boundary, intent, parent artifacts, authority chain/deltas, layer handoffs, emitted artifacts, evidence updates/deltas, residual deltas, stop conditions, missing contracts, validation commands, promotion blockers, source refs, support-state effect, and non-claims.
- Mechanism: Trace user intent through constitution, governance, planning, VCM, routing, verification, execution, evidence, compression/procedural loop closure, and SCF improvement gates without collapsing layer boundaries.
- Mechanism: Show the artifact emitted by each layer: command contract, plan DAG, context packet, route decision, claim envelope, work order, audit log, benchmark ledger, residual, or capability-field transition.
- Mechanism: Identify where authority can stop, narrow, reroute, quarantine, rollback, or require review before downstream work proceeds.
- Mechanism: Record positive and negative checkpoints so approved paths and blocked paths are both inspectable.
- Mechanism: Track parentage, authority deltas, evidence deltas, and residual deltas instead of treating the trace as a chronological log.
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
- Implemented repository-level fixture: `reference_trace_record.valid.json` validates reference-trace record shape, trace state, execution boundary, parent artifacts, authority/evidence/residual deltas, promotion blockers, source refs, support-state effect, and non-claims only; no integrated runtime trace harness, artifact continuity audit, or authority stop-condition checker exists yet.
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
- Mechanism: Track Theseus report evidence states such as source-note-only, report-imported, artifact-missing, replay-ready, replay-failed, locally-reproduced, runtime-blocked, and archived-lineage.
- Mechanism: Emit a Theseus Report Packet with intent or benchmark pressure, plan/compiler contract hash, work-board item, node or arm route, report bundle path, gate report, residual ledger entry, replay command, environment notes, artifact checksum, reviewer decision, publication permission, missing artifacts, and non-claims.
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
- Latest-file status never overwrites report lineage.
- Current-state claims require current artifacts, not historical source-note lineage.

Failure modes to cover:

- Latest-file report overwrites history.
- Benchmark overfit becomes capability evidence.
- Teacher dependence replaces local evidence.
- Architecture churn outruns residual diagnosis.
- Remote work proceeds without allowlists, TTLs, or kill switches.
- Local prototype results are overclaimed as public evidence.
- Report-state drift.
- Missing-artifact smoothing.

Draft deliverables:

- An implementation-reference crosswalk table from ASI stack layer to Theseus report, config, or tool surface, with evidence state and public claim boundary for each row.
- Implemented repository-level fixture: `theseus_report_crosswalk_record.valid.json` validates report-crosswalk record shape only; no live Theseus report bundle, replay command, benchmark environment, or current gate output has been imported or rerun.
- Planned Codex test: Report-bundle completeness test
- Planned Codex test: Replay-readiness test
- Planned Codex test: Theseus report crosswalk completeness test
- Planned Codex test: Architecture gate mapping test
- Planned Codex test: Work-board improvement contract test
- Planned Codex test: Artifact-gap audit
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
- Mechanism: Give each phase entry criteria, exit criteria, dependency edges, phase debt, and retirement conditions so demos do not become accepted milestones.
- Mechanism: Prevent irreversible unlocks from provisional evidence; research use can proceed without default execution, promotion, self-improvement, or public capability claims.
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
- Mechanism: emit living-book change packets with affected chapters, sources, claims, proof tags, schema/fixture paths, validation commands, render result, release target, audience profile, derived-artifact boundary, support-state effect, public URL if published, and explicit non-claims.
- Mechanism: preserve three-audience derivation discipline: AI/research scaffold, human-research live site, and stripped reader/audio editions all derive from one governed source state.
- Interface: Source ingestion feeds source notes.
- Interface: Drafting feeds claim matrices.
- Interface: Tests feed support states.
- Interface: Releases feed GitHub Pages, major-version edition records, reader manuscripts, and audio-script candidates.
- Interface: reader-edition records carry source commit, stripped sections, retained diagrams, format targets, render commands, review state, accessibility notes, audio-script status, and non-claims.

Primary invariants:

- No fabricated source content.
- No fabricated test results.
- Deprecated claims remain visible.
- Stable IDs preserve lineage across part/chapter splits, merges, reorders, proof-target moves, and releases.

Failure modes to cover:

- Public site diverges from Quarto source.
- Outline and manifest drift.
- Readers cannot tell which claims are speculative.
- Reader or audio releases accidentally imply that target formats exist before render, review, or audio production.
- Publication laundering: successful builds, polished pages, or reader artifacts treated as evidence for source interpretation, architecture quality, or empirical claims.

Draft deliverables:

- A public Quarto repo with dynamic scaffold, source matrix, claim matrix, proof manifest, validation, GitHub Pages, and public release records.
- A public-safe author-intent and lineage appendix that preserves architecture intent without publishing private conversation text.
- Implemented repository-level validation: `living_book_release_record.valid.json` and tracked records in `release_records/` validate release-record shape, release state, audience scope, canonical scope, derived-artifact boundaries, support-state effect, and non-claims only; render and validation checks prove publication hygiene, not manuscript quality, claim truth, reader artifact production, or audio artifact production.
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
- Mechanism: Maintain source inventory, source notes, the generated appendix for Corben's own corpus and local projects, the separate generated external-literature appendix, chapter source queues, and direct-citation status before using a source as support.
- Mechanism: Track recovered, missing, private, connector-gated, external-literature, proof, experiment, and artifact-reproduction items as Research Backlog Records rather than evidence, including triage state, source storage policy, public-safety state, chapter action policy, chapter-decision refs, deduplication state, merge/split policy, boundary rationale, required pre-drafting work, evidence-transition preconditions, source refs, promotion blockers, support-state effect, and non-claims.
- Mechanism: Use triage rules to decide whether a new paper updates an existing boundary, requires a precise new chapter, belongs in an appendix, or should remain unassigned.
- Mechanism: Preserve merge/insertion rules so overlapping papers mine shared mechanisms without creating duplicate anthology chapters.
- Mechanism: Track source lifecycle states such as unread, inventoried, cached, source-noted, mapped, passage-reviewed, integrated, tested, mechanized, reproduced, deprecated, and refuted.
- Mechanism: Require a triage decision before prose changes when a future agent receives a new paper: update existing chapter, propose new chapter, route to appendix, backlog, or reject as out of scope.
- Interface: Appendix G is an independent top-level appendix for Corben's own papers, Corben-supplied materials, recovered project records, and local project records.
- Interface: Appendix H is an independent top-level appendix for external literature and third-party references by other authors.
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
- Private empirical results leaking into public claims.
- External references named by source documents becoming citations before direct verification.
- Backlog rot where vague future-work items never become executable source, citation, proof, fixture, benchmark, or chapter tasks.

Draft deliverables:

- A split Corben-source-corpus and external-literature plan plus a research backlog record schema with source storage policy, public-safety state, external literature areas, source-note state, claim-mapping state, deduplication state, chapter-decision refs, proof/test backlog, required pre-drafting work, promotion blockers, and insertion/merge rules.
- Implemented repository-level fixtures: `research_backlog_record.valid.json` validates backlog-record shape, triage state, source storage policy, public-safety state, chapter action policy, chapter-decision refs, deduplication state, merge/split policy, boundary rationale, required pre-drafting work, evidence-transition preconditions, source refs, promotion blockers, support-state effect, and non-claims only; `new_paper_triage_scenario.valid.json` validates synthetic update-existing, propose-new-chapter, defer-external-literature, and reject-duplicate intake decisions only. External-literature normalization, direct citation checks, evidence transitions, public-release permission checks, and live new-paper triage rehearsals remain incomplete.
- Planned Codex test: Source inventory validation test.
- Planned Codex test: Source-note backlog audit.
- Implemented Codex test: New-paper triage scenario fixture.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:bibliography.plan.operational_invariant` | `AsiStackProofs.BibliographyPlan` | A source-derived claim requires a source note or equivalent ingested-source artifact. | implemented |
| `lean:bibliography.plan.failure_blocks_promotion` | `AsiStackProofs.BibliographyPlan` | A new source cannot be assigned to a non-existent chapter id. | implemented |

## Source Corpus and External Literature

Appendix G is the generated top-level appendix for Corben's own papers, Corben-supplied materials, recovered project records, and local project records. Appendix H is a separate generated top-level appendix for external sources by other authors and organizations. Do not present external sources as a second part of Appendix G, and do not present Corben/local records as a section of Appendix H. Both appendix scope tables must include an ownership-rule row: G is for material Corben wrote, supplied, recovered from his project history, or built locally; H is for sources produced by other authors, organizations, or outside projects. Both appendices must also keep an appendix-local `Appendix Identity` table before the long source rows: Appendix G states what belongs to Corben/local sources and excludes external sources, while Appendix H states what belongs to outside-author sources and excludes Corben/local sources. Do not use a shared two-row ownership table that makes the source appendices read like two parts of one Appendix G. Both appendices should remain generated from `sources/source_inventory.json` and `book_structure.json`. External literature should stay in Appendix H and should be added only when bibliographic metadata is recorded and the source is actually used.

## Author Intent and Architecture Lineage

Appendix I is the curated, public-safe home for conversation-mined author intent, architecture lineage, terminology decisions, and recovery tasks. It should not quote private conversation wording verbatim and should not promote claims to source-derived support state.

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
