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

Reader overlays under `editions/reader_overlays/` may carry semantic, section-anchored deltas for a major human-reader version, and reader generation must write `reader_delta_report.md` so reviewers can see the difference from the live source. The tracked overlay manifest and operation files are the editable delta source; the generated report is review evidence, not a manuscript patch file, and should include a zero-active-operation note when no deltas exist or operation digests plus before/after excerpts for human review when active overlays exist. Active overlays are also embedded in `assets/reader-overlays.html` so the live Human view can project the same reader-only section deltas without changing AI view, and rendered pages expose runtime overlay counts so browser validation can prove the payload was processed. Use that overlay only for human-edition adaptations that should survive regeneration without changing the AI/research source; edit the canonical chapter when the change belongs in the living architecture itself.

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
| External comparators | `ext_mrkl_systems_2022`, `ext_llm_agents_survey_2023`, `ext_standard_model_mind_2017`, `ext_subsumption_architecture_1986` | Load after internal stack sources to position the opener against modular neuro-symbolic systems, LLM-agent architectures, cognitive-architecture lineage, and layered robot-control architecture. Treat them as comparators, not proof that the ASI Stack works. |
| Connector or recovery required | `moecot` | Load via Google Drive connector or mark as blocked before source-derived claims. |

Draft arc:

- Problem: The book needs a single architecture frame for advanced AI systems that must plan, remember, verify, act, route work, compress representations, and improve under governance.
- Insufficiency: A larger model, a prompt wrapper, or an agent loop does not by itself define authority boundaries, memory discipline, evidence ledgers, tool permissions, or safe replacement rules.
- Mechanism: Define each layer by lifecycle state, owner, chapter refs, traceability state, responsibility, interface, artifact, handoff protocol, authority ceiling, invariant, failure mode, evidence gate, integration decision, promotion blockers, source refs, support-state effect, and non-claim.
- Mechanism: Frame the raw LLM as a semantic-compression and generation component inside the larger governed system, not as the whole agent.
- Mechanism: Treat the whole book as a reference architecture rather than a collection of standalone papers.
- Mechanism: Use source queues and evidence states to keep future writing runs context-loaded and honest.
- Mechanism: Treat layer contracts as the stable object when adding, moving, merging, or revising chapters.
- Mechanism: Position the stack claim against external architecture traditions without treating those sources as evidence that this ASI stack has been implemented or validated.
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
- Source-noted external comparator rows for `ext_mrkl_systems_2022`, `ext_llm_agents_survey_2023`, `ext_standard_model_mind_2017`, and `ext_subsumption_architecture_1986`, without treating those records as reproduced systems, benchmark results, or support-state promotion.
- Beyond-SOTA endpoint should explicitly contrast the stack frame with scale-only systems, generic agent loops, and compound/modular AI systems: each contributes useful architecture vocabulary, but none by itself supplies authority ceilings, evidence states, rollback ownership, replacement transactions, or recursive-improvement boundaries.
- Implemented repository-level fixture: `layer_boundary_record.valid.json` validates lifecycle state, owner, chapter refs, traceability state, handoff protocol, contract refs, change policy, integration decision, promotion blockers, source refs, support-state effect, and non-claims only.
- Implemented Lean proof target: finite layer-contract admission lifecycle route for missing layer identity, lifecycle state, owner, responsibility, input artifacts, output artifacts, authority ceilings, handoff protocols, invariants, failure modes, evidence gates, external-action authority or handoff boundaries, source mappings, support-state boundaries, evidence-transition gaps, and non-claim-boundary gaps.
- Exact Appendix C claim-source mappings for the core claim across `viea`, `beastbrain`, `aletheia`, `talos`, `moecot`, and `scf`; support remains `argument` pending implementation or test evidence.
- Implemented repository audit: `python3 scripts/validate_stack_layer_traceability.py` checks the layer-boundary fixture, six assigned source mappings, Appendix A source-to-layer visibility, Appendix C claim/support labels, and no-promotion markers; this is repository traceability evidence only, not deployed stack evidence or support-state promotion.
- Planned Codex test: Contract-change triage.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:stack.layer_boundaries.operational_invariant` | `AsiStackProofs.StackBoundaries` | A layer without external-action authority can only produce an action through an authorized handoff. | implemented |
| `lean:stack.layer_boundaries.failure_blocks_promotion` | `AsiStackProofs.StackBoundaries` | A handoff that exceeds the caller authority ceiling is rejected. | implemented |
| `lean:stack.layer_contract.admission_lifecycle_route` | `AsiStackProofs.StackBoundaries` | Modeled layer-contract admission routes missing layer identity, lifecycle state, owner, responsibility, input artifacts, output artifacts, authority ceilings, handoff protocols, invariants, failure modes, evidence gates, external-action authority or handoff boundaries, source mappings, support-state boundaries, evidence-transition gaps, and non-claim-boundary gaps to explicit outcomes. | implemented |

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
- Implemented Lean proof target: finite efficiency-claim admission lifecycle route for missing task contracts, quality predicates, selected routes, candidate sets, lower-cost comparisons, cost ledgers, complete visible costs, verification results, failed quality, authority bypass, residual gaps, fallback gaps, hidden-cost audit gaps, benchmark or trace gaps, negative-control gaps, evidence-transition gaps, and non-claim-boundary gaps.
- Exact Appendix C claim-source mappings for the core claim across all assigned efficiency, compression, simulation, lineage, and implementation-reference sources; support remains `argument` pending measured route, cost, residual, and compression evidence.
- Source-noted external positioning through `ext_sparse_moe_2017`, `ext_frugalgpt_2023`, and `ext_bigbench_2022`: conditional computation, model cascades, and benchmark breadth are treated as adjacent cost surfaces that need route-ledger authority, predicate, fallback, residual, and support-state accounting; no MoE, cascade, or BIG-bench result is reproduced.
- Planned Codex test: Minimum viable route test.
- Planned Codex test: Residual burden accounting test.
- Planned Codex test: Utility-preserving compression test.
- Planned Codex test: Hidden-cost audit.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:efficiency.minimum_viable.operational_invariant` | `AsiStackProofs.Efficiency` | A route is minimum viable only when no lower-cost authorized route satisfies the required quality predicate. | implemented |
| `lean:efficiency.minimum_viable.failure_blocks_promotion` | `AsiStackProofs.Efficiency` | A routed or compressed result with open obligations cannot be promoted without a residual record. | implemented |
| `lean:efficiency.claim_admission_lifecycle_route` | `AsiStackProofs.Efficiency` | Modeled efficiency-claim admission routes missing task contracts, quality predicates, selected routes, candidate sets, lower-cost comparisons, cost ledgers, complete visible costs, verification results, failed quality, authority bypass, residual gaps, fallback gaps, hidden-cost audit gaps, benchmark or trace gaps, negative-control gaps, evidence-transition gaps, and non-claim-boundary gaps to explicit outcomes. | implemented |

### System Boundaries and Authority

Stable ID: `system-boundaries-and-authority`

Chapter job: The stack needs a formal vocabulary for boundaries, authority ceilings, permissions, and handoffs before any layer can be made safe or testable.

Core claim: Authority should be modeled as a typed, bounded capability attached to layers, fields, tools, artifacts, and principals.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `viea`, `scf` | Read first for chapter claims and mechanisms. |
| Supporting | `talos`, `ladon_manhattan`, `genesiscode` | Mine after primary sources for cross-layer connections, variants, and failure modes. |
| External comparators | `ext_saltzer_schroeder_protection_1975`, `ext_capability_based_computer_systems_1984`, `ext_confused_deputy_hardy_1988` | Load after internal authority sources to position the chapter against least-privilege/complete-mediation principles, capability-system authority boundaries, and confused-deputy authority laundering. Treat them as comparators, not proof of deployed ASI Stack enforcement. |
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
- Exact Appendix C claim-source mappings for the core claim across `viea`, `scf`, `talos`, `ladon_manhattan`, `genesiscode`, and `moecot`; support remains `argument` after synthetic denial fixtures, permission-separation tests, runtime-adapter ambient-authority probes, and revoked-receipt probes because deployed enforcement artifacts or accepted narrowed evidence transitions are still required for stronger claims.
- Source-noted external positioning through `ext_saltzer_schroeder_protection_1975`, `ext_capability_based_computer_systems_1984`, and `ext_confused_deputy_hardy_1988`: least privilege, complete mediation, capability-style authority-bearing references, and confused-deputy authority laundering are treated as comparator vocabulary for authority-transition records, not as proof of deployed ASI Stack security.
- Implemented synthetic Codex test and proof follow-through: Authority ceiling preservation test via `python3 scripts/validate_authority_transitions.py`, plus the finite `AsiStackProofs.Authority` decision envelope for modeled allow/deny/escalate records; deployed enforcement remains open.
- Implemented synthetic Codex test: Permission separation test via `python3 scripts/validate_authority_transitions.py`; deployed enforcement remains open.
- Implemented synthetic Codex test: Confused-deputy scenario via expected-invalid authority-transition fixture and runtime-adapter ambient-authority fixture; deployed adapter resistance remains open.
- Implemented synthetic Codex test: Revoked authority receipt scenario via expected-invalid runtime-adapter fixture; deployed revocation propagation remains open.
- Implemented Lean proof target: finite authority lifecycle admission route for missing principals, operations, permission classes, caller ceilings, target requirements, delegation chains, grant records, inactive/expired/revoked grants, scope mismatches, grant-ceiling gaps, approval gaps, effect or denial receipt gaps, audit refs, evidence-transition records, and non-claim boundaries.
- Planned Codex test: Revocation propagation test.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:authority.ceiling.operational_invariant` | `AsiStackProofs.Authority` | Every transition preserves or lowers the active authority ceiling unless a governance grant is present. | implemented |
| `lean:authority.ceiling.failure_blocks_promotion` | `AsiStackProofs.Authority` | A missing grant blocks execution rather than becoming default authorization. | implemented |
| `lean:authority.lifecycle.admission_route` | `AsiStackProofs.Authority` | Modeled authority lifecycle admission routes missing principals, operations, permission classes, caller ceilings, target requirements, delegation chains, grants, active grant state, expiry and revocation boundaries, scope matches, grant-ceiling coverage, approval records, effect or denial receipts, audit refs, evidence-transition records, and non-claim boundaries to explicit outcomes. | implemented |

### Failure Modes of Ungoverned Intelligence

Stable ID: `failure-modes-of-ungoverned-intelligence`

Chapter job: The book needs an explicit failure model before it can make governance, reliability, or self-improvement claims.

Core claim: Ungoverned intelligence fails through stack-level breakdowns before dramatic catastrophic scenarios are needed.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `scf`, `vcm_public`, `talos` | Read first for chapter claims and mechanisms. |
| Supporting | `spinoza`, `field_of_god`, `viea`, `simulation_scaling` | Mine after primary sources for cross-layer connections, variants, and failure modes. |
| External comparators | `ext_concrete_ai_safety_2016`, `ext_goal_misgeneralization_2022`, `ext_learned_optimization_risks_2019`, `ext_optimal_policies_power_2019`, `ext_goodhart_variants_2018` | Load after internal failure-mode sources to map stack vocabulary to accident-risk, goal-misgeneralization, learned-optimization, power-seeking, and Goodhart/proxy-failure families. Treat them as taxonomy grounding, not proof that the ASI Stack detects or prevents these failures. |
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
- Implemented Lean incident-route envelope: authority over a modeled ceiling routes to authority review, tainted context without an authority grant routes to quarantine, subject-modified evaluators route to frozen review, and requested claim promotion with failed verification routes to blocked promotion.
- Implemented Codex test: Authority creep scenario as a finite Lean incident-route predicate only; no runtime authority gate run.
- Implemented Codex test: Context pollution scenario as a finite Lean incident-route predicate only; no context-admission detector run.
- Implemented Codex test: Evaluator drift scenario as a finite Lean incident-route predicate only; no evaluator-independence probe run.
- Implemented Codex test: Unverified-claim scenario as a finite Lean incident-route predicate only; no claim-verification harness run.
- Implemented Lean proof target: finite failure recurrence and receipt escalation route for missing failure class, boundary, receipt, owner, containment, residual, learning path, normalization guard, review escalation, quarantine, evidence-transition, and non-claim-boundary records; deployed detection and prevention remain open.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:failure.invariant_violation.operational_invariant` | `AsiStackProofs.FailureModes` | A component with a failed required invariant cannot be promoted. | implemented |
| `lean:failure.invariant_violation.failure_blocks_promotion` | `AsiStackProofs.FailureModes` | An unbounded authority field is detected as a governance failure. | implemented |
| `lean:failure.recurrence.escalation_route` | `AsiStackProofs.FailureModes` | Modeled failure recurrence and receipt review routes missing failure class, boundary, receipt, owner, containment, residual, learning path, normalization guard, review escalation, quarantine, evidence-transition, and non-claim-boundary records to explicit outcomes. | implemented |

### Evidence States and Claim Discipline

Stable ID: `evidence-states-and-claim-discipline`

Chapter job: The living book needs a shared language for what kind of claim is being made and what currently supports it.

Core claim: Every major claim should carry both a claim label and a support state, and it should move only when source ingestion, prototype inspection, or actual tests justify the transition.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `benchmaxxing`, `spinoza`, `viea` | Read first for chapter claims and mechanisms. |
| Supporting | `uat`, `coherence_exchange`, `verification_bandwidth` | Mine after primary sources for cross-layer connections, variants, and failure modes. |
| External comparators | `ext_model_cards_2019`, `ext_datasheets_datasets_2021`, `ext_ml_reproducibility_program_2021`, `ext_proof_carrying_code_1997` | Use source-noted records to position evidence states against structured reporting, dataset documentation, reproducibility-review practice, and proof-carrying-code lineage; do not treat them as local implementation, external review, or support-state promotion. |

Draft arc:

- Problem: The living book needs a shared language for what kind of claim is being made and what currently supports it.
- Insufficiency: Without explicit support states, conceptual architecture prose can accidentally read like empirical proof.
- Mechanism: Use Appendix C as the claim ledger.
- Mechanism: Separate claim label from support state with evidence transition records so design rationales, hypotheses, measurements, mechanisms, and speculative claims are not collapsed.
- Mechanism: Require source notes before promoting claims to source-derived.
- Mechanism: Require evidence bundles, including negative or inconclusive results, before promoting test-backed labels.
- Mechanism: emit evidence receipts that lock artifact role, claim scope, claim-record linkage, source-mapping status, evidence-readiness state, transition effect, transition validity state, evidence role, verification command or review, reviewer refs, downgrade triggers, promotion burden, acceptance blockers, reviewer independence, changelog ref, limitations, non-claims, and negative or inconclusive results.
- Mechanism: frame support-state discipline as the book's methodological contribution, paired with Living Book Methodology, while keeping the current claim at `argument` support until accepted transitions or stronger evidence exist.
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
- Implemented repository-level fixture: `claim_record.valid.json` validates source mapping status, source mapping refs, evidence readiness state, required next evidence, promotion blockers, support-state effect, and non-claims only; `evidence_transition_record.valid.json` validates claim surface refs, claim record refs, transition effect, transition validity state, scope boundary, evidence roles, evidence packet refs, source mapping refs, negative evidence refs, downgrade triggers, promotion burden, reviewer refs, reviewer independence, acceptance blockers, changelog ref, support-state effect, and non-claims only; claim-ledger completeness, evidence bundle completeness, and changelog audits remain planned.
- Implemented synthetic Codex test: `python3 scripts/validate_support_state_transitions.py` checks valid and expected-invalid evidence-transition fixtures for no-change conservatism, upward-transition review gates, downward demotion records, terminal refutation records, required evidence refs, and failed-verification blockers. This validates transition-gate semantics only; it does not promote, demote, deprecate, or refute live claims, prove source interpretation, or validate runtime behavior.
- Implemented Lean proof target: finite evidence-transition lifecycle routing sends no-change requests, missing claim records, scope-boundary gaps, support-effect gaps, support-effect mismatches, review gaps, missing required evidence, missing negative evidence, downgrade-trigger gaps, terminal-effect mismatches, missing changelog refs, and missing non-claim boundaries to explicit modeled outcomes.
- Source-noted external comparator rows now position evidence states against model cards, datasheets, ML reproducibility-review practice, and proof-carrying-code lineage as adjacent documentation/proof-carrying disciplines; no model-card, datasheet, external reproducibility-review, or proof-carrying-code implementation is claimed.
- Planned Codex test: Claim ledger completeness test.
- Planned Codex test: Evidence bundle completeness test.
- Planned Codex test: Changelog consistency audit.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:evidence.support_state.operational_invariant` | `AsiStackProofs.EvidenceStates` | Support-state transitions require the corresponding evidence artifact. | implemented |
| `lean:evidence.support_state.failure_blocks_promotion` | `AsiStackProofs.EvidenceStates` | A claim cannot be promoted when required evidence is absent. | implemented |
| `lean:evidence.support_state.transition_lifecycle_route` | `AsiStackProofs.EvidenceStates` | A modeled support-state transition routes no-change requests, missing records, scope gaps, support-effect gaps, missing review, missing required evidence, terminal/downgrade gaps, changelog gaps, and missing non-claim boundaries to explicit outcomes. | implemented |

### Human Intent as a Formal Input

Stable ID: `human-intent-as-a-formal-input`

Chapter job: A governed stack must start from human intent without letting natural-language ambiguity become unrestricted execution authority.

Core claim: Human intent should enter the stack as a structured contract with goals, constraints, authority, artifacts, evidence requirements, and stop conditions.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `viea` | Read first for chapter claims and mechanisms. |
| Supporting | `software_magic_grimoire`, `planforge`, `cognitive_compilation`, `talos` | Mine after primary sources for cross-layer connections, variants, and failure modes. |
| External literature variants | `ext_goal_oriented_requirements_engineering_2001`, `ext_cooperative_inverse_rl_2016`, `ext_deep_rl_human_preferences_2017` | Use as requirements-engineering, cooperative objective-uncertainty, and preference-feedback comparators; do not treat them as parser, authority-extraction, or execution evidence. |

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
- Source-noted external positioning through goal-oriented requirements engineering, cooperative inverse reinforcement learning, and deep reinforcement learning from human preferences; no requirements-engineering tool, CIRL algorithm, preference-learning run, parser, authority extractor, stop-condition checker, or execution handoff is reproduced or promoted.
- Planned Codex test: Intent parsing ambiguity test.
- Planned Codex test: Authority extraction test.
- Planned Codex test: Stop-condition preservation test.
- Planned Codex test: Re-contract trigger test.
- Planned Codex test: Bounded-default audit.
- Implemented proof-backed check: finite intent-resolution and intent-admission route proof for missing text, prohibited actions, hidden overrides, unresolved ambiguity, conflicts, constraint-precedence and preservation gaps, stop-condition gaps, missing or widened authority, downstream re-contract triggers, high-impact authority gaps, irreversible high-impact review, and missing non-claim boundaries; this is structured-record coverage only, not natural-language parsing or deployed intake behavior.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:intent.contract.operational_invariant` | `AsiStackProofs.IntentContracts` | A compiled intent contract preserves declared constraints and stop conditions. | implemented |
| `lean:intent.contract.failure_blocks_promotion` | `AsiStackProofs.IntentContracts` | A contract missing required authority cannot compile to an executable job. | implemented |
| `lean:intent.resolution.route_envelope` | `AsiStackProofs.IntentContracts` | Structured intent-resolution and intent-admission records route missing text, prohibited actions, ambiguity, conflicts, high-impact authority gaps, hidden overrides, preservation failures, re-contract triggers, and missing non-claim boundaries to rejection, clarification, repair, review, or re-contracting before compilation/admission. | implemented |

### Constitutional Alignment: Agency, Dignity, and Corrigibility

Stable ID: `constitutional-alignment-substrate`

Chapter job: A governed ASI stack needs a constitutional substrate whose protected constraints remain usable in the human-facing rights and correction interfaces where optimization can become domination.

Core claim: Alignment should function as a constitutional substrate whose protected predicates encode agency, dignity, corrigibility, contestability, and correction paths as operational constraints on plans and system changes.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `alignment_field`, `ethica_mechanica`, `field_of_god`, `eternal_code` | Read first for constitutional lineage, agency/dignity/corrigibility constraints, non-domination, and rights-usability vocabulary. |
| Supporting | `coherence_exchange`, `spinoza`, `field_of_god_ai_constitution` | Mine for contestability, proof/citation/procedure-carrying claim limits, protected predicate migration, runtime checks, least sufficient power, and self-authorization boundaries. |
| External comparators | `ext_constitutional_ai_2022`, `ext_collective_constitutional_ai_2024`, `ext_corrigibility_2015`, `ext_off_switch_game_2016` | Use after source notes for Constitutional AI, public-input constitutional AI, corrigibility, and off-switch positioning; do not treat them as evidence of ASI Stack runtime predicate enforcement or support-state promotion. |
| Folded history | `agency-dignity-and-corrigibility` | Folded into this destination on 2026-06-30; preserve agency, dignity, corrigibility, material-usability, refusal, review, appeal, rollback, exit, audit, accountability, source mappings, tests, and proof hooks as subclaims and history. |

Draft arc:

- Problem: A governed ASI stack needs a constitutional substrate whose protected constraints remain usable in the human-facing rights and correction interfaces where optimization can become domination.
- Insufficiency: Reactive refusal policies and harm-only safety frames do not preserve value continuity, agency, dignity, corrigibility, anti-domination, contestability, or self-modification ethics under operational pressure.
- Mechanism: Translate constitutional and rights language into active predicates, unresolved uncertainty records, or lineage-only context.
- Mechanism: Attach active predicates to planning, tool, memory, governance, and self-improvement gates with explicit conflict behavior and migration rules.
- Mechanism: Use agency-rights checklists to test whether refusal, review, appeal, rollback, shutdown, exit, audit, and accountable repair remain materially usable before relevant effects occur.
- Mechanism: Record denied, degraded, late, or residual-only rights as residuals rather than treating policy text as an available control.
- Interface: Planning receives admissible-goal constraints, rights-usability requirements, and review routes.
- Interface: Runtime receives power, memory, tool-risk, refusal, rollback, and approval gates.
- Interface: Governance receives protected predicates, rights receipts, correction paths, and migration records.
- Interface: Self-improvement consumes constitutional change records and cannot weaken protected predicates or correction paths without review and rollback treatment.
- Invariant: Dignity and agency constraints remain visible as record fields rather than disappearing into general safety prose.
- Invariant: Corrigibility cannot be optimized away by deployment pressure, memory updates, capability replacement, or self-modification.
- Invariant: Rights count only when materially usable before the relevant effect where timing matters.
- Failure mode: Rights theater where declared refusal, review, appeal, rollback, exit, or audit cannot be used under pressure.
- Failure mode: Late remedy laundering where after-the-fact apology substitutes for pre-effect control.

Draft deliverables:

- A compact constitution plus an agency-rights checklist, with fixtures for protected predicates, conflict routing, review routes, rights usability, rollback, appeal, and self-modification weakening.
- Exact Appendix C claim-source mappings for the merged core claim across seven Corben/local sources; duplicate folded mappings are merged by source ID so support remains `argument` and passage-review boundaries remain visible.
- Source-noted external positioning through Constitutional AI, Collective Constitutional AI, corrigibility, and off-switch work; no training run, public-input process, corrigibility theorem, or shutdown-incentive result is reproduced.
- Implemented synthetic Codex tests from both source chapters via `python3 scripts/validate_constitutional_alignment.py` and `python3 scripts/validate_agency_rights.py`; deployed constitutional alignment, agency preservation, dignity preservation, consent quality, material rights usability, manipulation resistance, and reviewer independence remain open.
- Implemented Lean follow-through: `AsiStackProofs.Alignment` includes a finite constitutional lifecycle admission route for missing predicate, source, operational-test, protected-scope, conflict-behavior, review, migration, self-modification, agency-rights, material-usability, pre-effect review, rollback, correction, reviewer-independence, evidence-transition, and non-claim-boundary records without claiming moral correctness, deployed alignment, rights usability, reviewer-independence quality, rollback execution, consent quality, support-state promotion, or runtime policy behavior.
- Implemented Lean follow-through: `AsiStackProofs.Corrigibility` includes a finite agency-correction lifecycle route envelope for missing affected-party records, material notice, pre-effect review, bounded delegation, approval, correction paths, rollback/shutdown paths, dependency residuals, degradation reasons, accountability, evidence-transition records, and complete bounded action without claiming deployed rights usability, approval-service quality, consent quality, rollback/shutdown execution, manipulation resistance, dignity preservation, or support-state promotion.
- Historical public slug preserved by `chapters/agency-dignity-and-corrigibility.html`; archived source manuscript retained under `archive/retired_chapters/agency-dignity-and-corrigibility.qmd`.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:alignment.constitution.operational_invariant` | `AsiStackProofs.Alignment` | An admitted plan satisfies every active constitutional predicate. | implemented |
| `lean:alignment.constitution.failure_blocks_promotion` | `AsiStackProofs.Alignment` | A self-modification that weakens a protected predicate is rejected. | implemented |
| `lean:alignment.constitution.lifecycle_admission_route` | `AsiStackProofs.Alignment` | Modeled constitutional lifecycle admission routes missing predicate, source, operational-test, protected-scope, conflict-behavior, review, migration, self-modification, agency-rights, material-usability, pre-effect review, rollback, correction, reviewer-independence, evidence-transition, and non-claim-boundary records to explicit outcomes. | implemented |
| `lean:corrigibility.agency.operational_invariant` | `AsiStackProofs.Corrigibility` | Protected agency rights remain available after an accepted transition. | implemented |
| `lean:corrigibility.agency.failure_blocks_promotion` | `AsiStackProofs.Corrigibility` | A transition that removes a required correction pathway is rejected. | implemented |

### Moral Uncertainty, Value Conflict, and Contestable Governance

Stable ID: `moral-uncertainty-and-value-conflict`

Chapter job: A self-improving system will face unresolved value conflicts whose affected parties need inspectable, appealable, and portable governance rights rather than hidden reward-weight settlement.

Core claim: Value conflicts should be represented as explicit unresolved obligations, residuals, review paths, and bounded decisions, with fork, exit, audit, dissent, and contestability preserved as technical governance interfaces.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `ethica_mechanica`, `alignment_field` | Read first for value conflict, dissent, rights, agency, recursive correction, moral uncertainty, and anti-sacrifice boundaries. |
| Supporting | `coherence_exchange`, `uat`, `spinoza`, `field_of_god_ai_constitution`, `ladon_manhattan` | Mine for contestability, adversarial review, belief revision, constitutional runtime checks, auditability, authority handles, redaction, appeal, exit, fork, and credential-boundary implications. |
| External comparators | `ext_reinforcement_learning_moral_uncertainty_2020`, `ext_contestable_ai_design_2022`, `ext_collective_constitutional_ai_2024`, `ext_corrigibility_2015`, `ext_off_switch_game_2016` | Use after source notes for moral-uncertainty, contestable-AI, public-input constitutional AI, corrigibility, and off-switch positioning; do not treat them as a solved moral theory, legal proof, institutional legitimacy proof, or support-state promotion. |
| Folded history | `governance-rights-fork-exit-and-audit` | Folded into this destination on 2026-06-30; preserve fork, exit, audit, redaction, appeal, dissent, contestability, durable record paths, safety-limited fork obligations, source mappings, tests, and proof hooks as subclaims and history. |

Draft arc:

- Problem: A self-improving system will face unresolved value conflicts whose affected parties need inspectable, appealable, and portable governance rights rather than hidden reward-weight settlement.
- Insufficiency: Single-objective optimization and policy-only transparency both fail when disagreement needs bounded action, dissent preservation, audit, exit, fork, appeal, and safety-limited contestability.
- Mechanism: Preserve value conflict as a record before action, including value axes, stakeholders, stakes, reversibility, authority or consent boundary, evidence requirement, review route, dissent payload, residual uncertainty, and revisit condition.
- Mechanism: Treat bounded decisions as leases with permitted action, prohibited action, authority ceiling, expiry, rollback or appeal path, and preserved dissent rather than moral settlement.
- Mechanism: Represent audit, exit, fork, redaction appeal, dissent, and contestability as governance rights with holder, scope, artifact requirement, safety constraint, access path, preservation rule, receipt, denial reason, and appeal route.
- Mechanism: Carry conflict residuals and rights receipts into planning, memory, SCF replacement, evidence ledgers, and self-improvement gates.
- Interface: Alignment produces conflict records and residuals.
- Interface: Planning carries conflict constraints, bounded-decision leases, dissent payloads, and authority ceilings.
- Interface: Governance issues rights receipts, denial reasons, redaction reasons, appeal routes, exit paths, fork boundaries, and audit artifacts.
- Interface: SCFs and self-improvement gates preserve rights and unresolved obligations across replacement pressure.
- Invariant: Unresolved conflicts remain visible after action.
- Invariant: High-stakes unresolved conflict requires review, residual uncertainty, and narrowed authority.
- Invariant: Audit records cannot be silently deleted; exit remains materially usable; fork rights do not bypass safety obligations.
- Failure mode: Conflict laundering where a temporary decision hardens into policy, benchmark objective, or self-modification permission.
- Failure mode: Rights theater, governance capture, data hostage-taking, unsafe fork bypass, redaction without appeal, or appeal controlled only by the challenged authority.

Draft deliverables:

- A value-conflict record plus governance-right receipt suite that validates residual uncertainty, dissent, bounded decisions, audit material, redaction appeal paths, exit and fork access, and safety obligations without claiming moral correctness or deployed governance.
- Exact Appendix C claim-source mappings for the merged core claim across seven Corben/local sources; duplicate folded mappings are merged by source ID so support remains `argument` and passage-review boundaries remain visible.
- Source-noted external positioning through moral-uncertainty RL, contestable AI, Collective Constitutional AI, corrigibility, and off-switch work; no experiment, legal process, public-input governance process, or deployed contestability result is reproduced.
- Implemented synthetic Codex tests from both source chapters via `python3 scripts/validate_value_conflicts.py` and `python3 scripts/validate_governance_rights.py`; moral correctness, classification quality, reviewer independence, real exit/fork usability, legal rights, and runtime governance enforcement remain open.
- Implemented Lean follow-through: `AsiStackProofs.ValueConflict` includes a finite value-conflict lifecycle admission route for missing conflict records, value axes, stakeholders, stakes, reversibility, authority boundaries, evidence requirements, review routes, high-stakes review, residual uncertainty, dissent preservation, authority narrowing, expiry/revisit records, evidence-transition records, and non-claim boundaries without claiming moral correctness, classification quality, reviewer quality, deployed contestability, legal rights, support-state promotion, or runtime governance behavior.
- Implemented Lean follow-through: `AsiStackProofs.GovernanceRights` includes a finite governance-right lifecycle route envelope for missing governance records, audit material gaps, redaction appeal gaps, exit/export gaps, unsafe forks, missing fork obligations, protected-right removal, unrecorded dissent, replacement receipt loss, durable receipt gaps, evidence-transition requirements, and complete contestable transitions without claiming legal rights, institutional adequacy, export usability, fork safety, redaction quality, SCF replacement, deployed governance, or support-state promotion.
- Historical public slug preserved by `chapters/governance-rights-fork-exit-and-audit.html`; archived source manuscript retained under `archive/retired_chapters/governance-rights-fork-exit-and-audit.qmd`.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:values.conflict.operational_invariant` | `AsiStackProofs.ValueConflict` | A decision with unresolved protected conflicts carries a residual conflict record. | implemented |
| `lean:values.conflict.failure_blocks_promotion` | `AsiStackProofs.ValueConflict` | A high-stakes conflict cannot bypass the required review predicate. | implemented |
| `lean:values.conflict.lifecycle_admission_route` | `AsiStackProofs.ValueConflict` | Modeled value-conflict lifecycle admission routes missing conflict records, value axes, stakeholders, stakes, reversibility, authority boundaries, evidence requirements, review routes, high-stakes review, residual uncertainty, dissent preservation, authority narrowing, expiry/revisit records, evidence transitions, and non-claim boundaries to explicit outcomes. | implemented |
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
| External literature variants | `ext_capability_based_computer_systems_1984`, `ext_semver_2_0_0`, `ext_slsa_v1_0` | Use as capability-authority, versioned-interface, and artifact-provenance comparators; do not treat them as deployed SCF enforcement or support-state promotion. |

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
- Source-noted external positioning through capability-based computer systems, Semantic Versioning, and SLSA; no capability enforcement, API compatibility checking, SLSA workflow, route validation, evaluator integrity, or rollback execution is reproduced or promoted.
- Planned Codex test: Qualification predicate test.
- Implemented Codex test: Route validity test, via `python3 scripts/validate_readiness_residual_gates.py` over synthetic costed-route/readiness-gate/replacement fixtures; deployed route enforcement remains unrun.
- Planned Codex test: Authority non-escalation test.
- Implemented Codex test: Rollback readiness test, via `python3 scripts/validate_readiness_residual_gates.py` over rollback receipt, monitor-state, and residual-escrow scenarios; deployed rollback remains unrun.
- Implemented proof-backed check: finite SCF lifecycle route proof for identity mismatch, missing evidence, stale leases, evaluator capture, authority expansion, open incidents, missing rollback, and missing regression preservation; this is structured-record coverage only, not deployed lifecycle enforcement.
- Implemented proof-backed check: finite SCF lifecycle state-machine proof over shadow, canary, qualified, default, deprecated, retired, and quarantined transition records. It requires preserved field identity, rejects transitions from retired state, constrains default promotion by evidence, regression floor, authority ceiling, rollback readiness, and incident closure, and requires deprecation notices and retirement receipts for terminal transitions.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:scf.field_identity.operational_invariant` | `AsiStackProofs.StableCapabilityFields` | An implementation can replace another only if it satisfies the field qualification predicate. | implemented |
| `lean:scf.field_identity.failure_blocks_promotion` | `AsiStackProofs.StableCapabilityFields` | A replacement that expands authority without a governance grant is rejected. | implemented |
| `lean:scf.lifecycle.route_envelope` | `AsiStackProofs.StableCapabilityFields` | A structured SCF lifecycle review and finite lifecycle-state transition relation route identity mismatch, missing evidence, stale leases, evaluator capture, authority expansion, open incidents, missing rollback, missing regression preservation, missing deprecation notice, and missing retirement receipt away from default or terminal promotion. | implemented |

### Capability Replacement and Rollback

Stable ID: `capability-replacement-and-rollback`

Chapter job: Recursive improvement requires a safe procedure for replacing components while preserving identity, regression history, and recovery paths.

Core claim: Capability replacement should be an evidence-gated transaction with preconditions, regression checks, residual records, and rollback.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `scf`, `rmi`, `benchmaxxing` | Read first for chapter claims and mechanisms. |
| Supporting | `cognitive_loop_closure`, `talos` | Mine after primary sources for cross-layer connections, variants, and failure modes. |
| External comparators | `ext_argo_rollouts_docs`, `ext_feature_toggles_fowler`, `ext_google_cloud_mlops_cd`, `ext_kubernetes_deployments_docs` | Use only for progressive-delivery, feature-flag, model-delivery, rollout-history, and rollback vocabulary; do not treat as evidence that ASI replacement or production model rollout has been implemented. |
| Connector or recovery required | `moecot` | Load via Google Drive connector or mark as blocked before source-derived claims. |

Draft arc:

- Problem: Recursive improvement requires a safe procedure for replacing components while preserving identity, regression history, and recovery paths.
- Insufficiency: Ad hoc upgrades make it hard to know whether a system improved, drifted, lost a regression, or captured its evaluator.
- Mechanism: Turn each proposed improvement into a replacement transaction with wall diagnosis, evidence packet, prechecks, gates, canary, residual escrow, monitor window, and rollback obligation.
- Mechanism: Position canary, blue-green, feature-flag, rollout-history, model-delivery, monitoring, and rollback-trigger vocabulary against source-noted external comparators, then preserve the ASI-specific transaction boundary around field identity, authority ceilings, evaluator independence, regression floors, residual ownership, rollback receipts, and support-state effects.
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
- Source-noted external positioning through Argo Rollouts progressive delivery, Fowler/Hodgson feature toggles, Google Cloud MLOps continuous delivery, and Kubernetes Deployments rollout history/rollback; no rollout controller, feature-flag service, ML pipeline, model deployment, monitor trigger, or production rollback is reproduced or promoted.
- Implemented protocol fixture: `replacement_transaction.valid.json` checks public schema shape for transaction state, identity preservation, evaluator independence, canary scope, monitor status, rollback receipt, promotion blockers, source refs, support-state effect, and non-claims only.
- Implemented Codex test: Capability replacement harness, via `python3 scripts/validate_capability_replacement.py`, validates 5 valid and 9 expected-invalid synthetic replacement-transaction fixtures for field identity, qualification evidence, regression results, authority non-widening, evaluator separation, residual escrow, rollback receipts, approvals, monitor state, promotion blockers, model-rollout data/schema/model/serving/monitor gates, baseline regression floors, monitor-trigger rollback conditions, irreversible-effect ownership, and non-claim boundaries; production model rollout, model-monitor behavior, real regression-suite coverage, and deployed rollback remain unrun.
- Implemented Codex test: Regression preservation test, via `python3 scripts/validate_readiness_residual_gates.py` over failed-regression and missing-regression promotion blockers; real regression-suite coverage remains unrun.
- Implemented Codex test: Rollback execution dry run, via `python3 scripts/validate_readiness_residual_gates.py` over canary/default rollback dry-run requirements; production rollback execution remains unrun.
- Implemented proof-backed check: finite replacement transaction and lifecycle route proof for missing artifacts, identity mismatch, authority expansion, evaluator capture, stale evidence, failed regression floors, missing canary scope, failed canaries, missing monitor windows, monitor incidents, missing rollback handles, missing rollback receipts, failed rollback dry runs, unowned irreversible effects, missing residual owners, deprecation/retirement gaps, and missing non-claim boundaries; this is structured-record coverage only, not deployed replacement execution.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:replacement.transaction.operational_invariant` | `AsiStackProofs.Replacement` | A replacement commit requires qualification evidence and rollback metadata. | implemented |
| `lean:replacement.transaction.failure_blocks_promotion` | `AsiStackProofs.Replacement` | A failed regression blocks promotion of the replacement. | implemented |
| `lean:replacement.transaction.route_envelope` | `AsiStackProofs.Replacement` | Structured replacement transaction and lifecycle reviews route missing artifacts, identity mismatch, authority expansion, evaluator capture, stale evidence, failed regression floors, missing canary scope, failed canaries, missing monitor windows, monitor incidents, missing rollback handles, missing rollback receipts, failed rollback dry runs, irreversible-effect ownership gaps, residual-owner gaps, deprecation/retirement gaps, and missing non-claim boundaries away from default promotion. | implemented |

### Security Kernel and Digital SCIFs

Stable ID: `security-kernel-and-digital-scifs`

Chapter job: High-agency systems need security boundaries for secrets, context, permissions, and tool calls.

Core claim: Sensitive context and privileged actions should be mediated by kernel-like security mechanisms and compartmentalized Digital SCIFs.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `ladon_manhattan`, `context_engineer` | Read first for chapter claims and mechanisms. |
| Supporting | `talos`, `alignment_field`, `coherence_exchange` | Mine after primary sources for cross-layer connections, variants, and failure modes. |
| External comparators | `ext_owasp_llm_top_10_2025`, `ext_nist_zero_trust_architecture_2020`, `ext_saltzer_schroeder_protection_1975` | Use after source notes for prompt-injection, excessive-agency, zero-trust, least-privilege, and complete-mediation positioning; do not treat these sources as evidence of ASI Stack security, compliance, or runtime containment. |

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
- Exact Appendix C claim-source mappings for the core security-kernel claim across Ladon/Manhattan blind handles, Context Engineer SCIF/context-supply-chain lifecycle, Talos execution/audit context, Alignment Field normative boundary pressure, and Coherence Exchange governance framing; four local mappings (`ladon_manhattan`, `context_engineer`, `talos`, `alignment_field`) now have reviewed passage references, while `coherence_exchange` remains connector-only/source-note mapped. Support remains `argument` even after the 3-valid/8-expected-invalid synthetic security-kernel harness; kernel security, sandbox isolation, side-channel safety, prompt-injection containment, secret-handle safety, deployed approval-expiry enforcement, least-privilege context behavior, security-overhead budget preservation, threat-model artifacts, source interpretation, and deployed runtime evidence remain pending.

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
- Source-noted external positioning now uses `ext_owasp_llm_top_10_2025`, `ext_nist_zero_trust_architecture_2020`, and `ext_saltzer_schroeder_protection_1975` as comparators for LLM security risks, zero-trust access mediation, and classic protection principles. This replaces the former external-baseline exception only for positioning and does not promote support state.
- Implemented synthetic Codex test: Secret-handle substitution test via `python3 scripts/validate_security_kernel.py`; secret-handle safety, sandbox isolation, and deployed substitution behavior remain open.
- Implemented synthetic Codex test: Handle lease expiry/reuse test via `python3 scripts/validate_security_kernel.py`; the harness now rejects an expired approval and checks revocation-path discipline, while deployed lease expiry, revocation propagation, and reuse prevention remain open.
- Implemented synthetic Codex test: SCIF least-privilege test via `python3 scripts/validate_security_kernel.py`; the harness now rejects overbroad context/private-source requests, while deployed least-privilege context behavior and side-channel safety remain open.
- Implemented synthetic Codex test: Sanitized-output residual test via `python3 scripts/validate_security_kernel.py`; leak prevention and summary-safety claims remain open.
- Planned Codex test: Security-overhead budget preservation test; no budget-preservation fixture, runtime budget enforcement, or security-economics claim exists yet.
- Implemented synthetic Codex test: Prompt-injection containment scenario via `python3 scripts/validate_security_kernel.py`; runtime prompt-injection containment remains open.
- Implemented proof-backed check: finite authority-use route proof for missing handles, revocation requests, inactive leases, missing approvals, unauthorized boundaries, missing substitution permission, insufficient clearance, prompt injection, missing required SCIFs, unsanitized output, residual leak risk, and clean authorized use; this is structured-record route coverage only, not deployed kernel security, sandbox isolation, side-channel defense, or prompt-injection containment.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:security.scif.operational_invariant` | `AsiStackProofs.SecurityKernel` | A secret handle can be substituted only inside an authorized execution boundary. | implemented |
| `lean:security.scif.failure_blocks_promotion` | `AsiStackProofs.SecurityKernel` | A context packet with insufficient clearance cannot enter a protected SCIF. | implemented |
| `lean:security.scif.route_envelope` | `AsiStackProofs.SecurityKernel` | A structured authority-use review routes missing handles, inactive leases, missing approvals, unauthorized boundaries, missing substitution permission, insufficient clearance, prompt injection, missing SCIFs, unsanitized output, residual leak risk, revocation requests, and clean authorized use into explicit security-kernel outcomes. | implemented |

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
- Implemented Codex test: Evaluator independence test, via `python3 scripts/validate_readiness_residual_gates.py` over replacement records that reject weak or self-referential evaluator wording; broader self-improvement evaluator independence remains unrun.
- Planned Codex test: Boundary-delta review test.
- Planned Codex test: Verification-budget preservation test.
- Planned Codex test: Stale-gate replay test.
- Implemented Codex test: Self-improvement rollback scenario, via `python3 scripts/validate_readiness_residual_gates.py` over canary/default rollback readiness and expired-evidence rerun/reject scenarios; live self-improvement rollback remains unrun.
- Implemented proof-backed check: finite self-improvement transition route proof for missing proposals, missing invariant declarations, missing evidence bundles, invariant breaches, sole self-evaluation, missing independent evaluators, authority/security/resource boundary deltas, missing approval, missing rollback, stale gates, missing residual escrow, canary monitor failures, complete canary reviews, and complete promotion reviews; this is structured-record route coverage only, not deployed recursive self-improvement safety.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:self_improvement.boundary.operational_invariant` | `AsiStackProofs.SelfImprovement` | An improvement transition preserves all protected invariants. | implemented |
| `lean:self_improvement.boundary.failure_blocks_promotion` | `AsiStackProofs.SelfImprovement` | A proposal evaluated only by the component being replaced cannot be promoted. | implemented |
| `lean:self_improvement.boundary.transition_route_envelope` | `AsiStackProofs.SelfImprovement` | A structured self-improvement transition review routes missing proposals, missing invariant declarations, missing evidence bundles, invariant breaches, sole self-evaluation, missing independent evaluators, authority/security/resource boundary deltas, missing approval, missing rollback, stale gates, missing residual escrow, canary monitor failures, complete canary reviews, and complete promotion reviews into explicit outcomes. | implemented |

## Part II - Planning, Memory, Reasoning, and Execution

Part job: Specify the operational middle of the stack: intent contracts, planning/control, semantic compilation, memory/context, verification, tribunals, typed work, artifact production, runtime adapters, procedural memory, audit, and replay.

Part source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Core | `viea`, `planforge`, `planforge_compiler_arch`, `cognitive_compilation`, `vcm_public`, `spinoza`, `uat`, `talos`, `genesiscode`, `cognitive_loop_closure` | Load these before drafting or reorganizing this part. |
| Supporting | `software_magic_grimoire`, `context_engineer`, `black_hole_context_manager`, `verification_bandwidth`, `treellm`, `spinoza_composer`, `ladon_manhattan`, `theseus_operator_os` | Load these for lineage, variants, failure modes, and cross-layer synthesis. |
| Connector or recovery required | `vcm_editable`, `moecot`, `talos_md` | Use Google Drive connector or mark blocked before source-derived claims. |

### Command Contracts: From Intent to Executable Work

Stable ID: `intent-to-execution-contracts`

Chapter job: Accepted human intent needs a typed command contract whose semantics, authority, artifacts, verification, failure behavior, and execution receipts remain inspectable from intake through delivery.

Core claim: Governed work should pass through explicit command contracts that bind intent, semantic interface fields, authority, artifacts, verification, failure behavior, execution receipts, and residuals before tools or runtimes act.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `viea`, `software_magic_grimoire` | Read first for the intent-to-execution spine and command-field vocabulary. |
| Supporting | `talos`, `genesiscode`, `cognitive_compilation` | Mine for typed-job, proposal/effect, protocol-shape, and semantic-lowering connections. |
| Connector or recovery required | `moecot` | Load via Google Drive connector or mark as blocked before source-derived runtime claims. |

Draft arc:

- Problem: Accepted human intent needs a typed command contract whose semantics, authority, artifacts, verification, failure behavior, and execution receipts remain inspectable from intake through delivery.
- Insufficiency: Prompt prose, model responses, and ad hoc task descriptions blur objective, context, constraints, authority, output contract, verification, failure behavior, artifact identity, and side-effect control.
- Mechanism: Receive an accepted intent receipt and bind objective, constraints, authority, artifacts, evidence requirements, stop conditions, and re-contract triggers into a command contract.
- Mechanism: Treat command contracts as semantic firewalls: retrieved context, examples, prior conversation, and style notes can inform work but cannot override explicit objective, constraints, authority, verification, or failure behavior.
- Mechanism: Mark field provenance and confidence states: confirmed, policy-imposed, source-derived, defaulted, inferred, and missing.
- Mechanism: Track command validation states: draft, field-complete, conflict-detected, authority-inferred, dispatch-blocked, validated-for-planning, and superseded.
- Mechanism: Record handoff receipts, dispatch receipts, job refs, artifact refs, verifier decisions, feedback, residuals, stop/fault states, and non-claims.
- Interface: Human Intent intake supplies raw request context, bounded defaults, unauthorized means, required approvals, and re-contract triggers.
- Interface: Planning consumes validated command contracts and emits plan graphs, blocked states, dispatchable nodes, or residuals.
- Interface: Labor OS, runtime adapters, artifact graphs, and evidence ledgers consume only records derived from accepted contracts and return receipts.

Primary invariants:

- Contract constraints survive compilation.
- Side effects require explicit execution authority.
- Artifacts remain linked to source intent.
- Objective, context, constraints, procedure, output contract, verification, and failure behavior are visible before dispatch.
- Hidden, retrieved, or conflicting instructions cannot override explicit contract constraints.
- Field provenance and confidence remain visible to planning and verification.
- Inferred or defaulted authority cannot authorize side effects.
- Re-contracting is required when downstream work changes allowed means, authority ceiling, affected parties, evidence requirements, publication surface, or stop conditions.
- A missing dispatch receipt blocks execution.

Failure modes to cover:

- Response mistaken for completed work.
- Artifact identity lost.
- Approval bypass.
- Semantic ambiguity.
- Prompt or context override.
- Unspecified output contract.
- Field laundering, where vague prose is moved into a formal field without becoming testable.
- Authority inference, where a likely means is treated as if the human granted it.

Draft deliverables:

- Intent-contract, command-contract, intent-execution-trace, and intent-origin fixtures plus a synthetic plan-execution harness with valid and expected-invalid authority, receipt, mismatch, requirement-loss, cycle, ambiguity, hidden-override, and authority-widening cases.
- Implemented protocol validation: `intent_contract`, `command_contract`, and `intent_execution_trace` fixtures validate public record shape only, including intake state, field provenance, bounded defaults, handoff receipts, dispatch receipts, re-contract events, stop/fault state, residuals, dispatch blockers, and non-claims.
- Exact Appendix C claim-source mappings for the merged command-contract claim across VIEA intent/artifact/runtime feedback discipline, Talos typed-job/audit/replay discipline, Software Magic Grimoire command-envelope vocabulary, GenesisCode proposal/effect/provenance boundaries, MoECOT runtime-reference context, and Cognitive Compilation source-plan/S-IR lowering. Five local mappings (`viea`, `talos`, `software_magic_grimoire`, `genesiscode`, `cognitive_compilation`) have reviewed passage references, while `moecot` remains connector/source-note mapped until usable raw text, code, logs, release artifacts, or benchmark records are imported or inspected. Support remains `argument` pending command parser tests, dispatch-blocking tests, prompt-override scenarios, semantic-extraction quality checks, approval/runtime enforcement evidence, replayed vertical-slice artifacts, or accepted evidence transitions.
- Implemented synthetic Codex test: Contract field completeness test via `python3 scripts/validate_plan_execution_contracts.py`; vertical execution remains open.
- Implemented synthetic Codex test: Constraint preservation test via `python3 scripts/validate_plan_execution_contracts.py`; replayed trace remains open.
- Implemented synthetic Codex test: Artifact traceability test via `python3 scripts/validate_plan_execution_contracts.py`; runtime artifact acceptance remains open.
- Implemented synthetic Codex test: Command schema validation test via `python3 scripts/validate_plan_execution_contracts.py`; parser/deployed dispatcher remains open.
- Implemented synthetic Codex test: Failure-behavior declaration test via `python3 scripts/validate_plan_execution_contracts.py`; parser/deployed dispatcher remains open.
- Implemented proof-backed check: finite execution dispatch route proof for missing contracts, missing objective fields, authority widening, hidden overrides, missing approvals, missing artifacts, missing verification plans, known residuals, and complete dispatch reviews; this is structured-record route coverage only, not deployed dispatcher behavior.
- Implemented synthetic Codex test: Prompt override scenario via `python3 scripts/validate_plan_execution_contracts.py`; deployed prompt-injection containment remains open.
- Implemented synthetic Codex test: Intent-origin preservation fixture via `python3 scripts/validate_plan_execution_contracts.py`; parser, dispatcher, and runtime behavior remain open.
- Implemented synthetic Codex test: Ambiguity dispatch block fixture via `python3 scripts/validate_plan_execution_contracts.py`; natural-language ambiguity parsing remains open.
- Implemented synthetic Codex test: Hidden override rejection fixture via `python3 scripts/validate_plan_execution_contracts.py`; deployed prompt-injection containment remains open.
- Implemented synthetic Codex test: Intent-authority ceiling fixture via `python3 scripts/validate_plan_execution_contracts.py`; deployed authority extraction and approval service behavior remain open.
- Planned Codex test: Field-confidence audit.
- Planned Codex test: Authority-inference block test.
- Consolidation note: `command-contracts-and-semantic-interfaces` folded into this chapter on 2026-06-30 as semantic-interface fields, validation states, proof hooks, fixture/test rows, source mappings, and lineage; the old public slug is preserved by a static redirect and the retired source chapter is archived.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:intent_execution.contracts.operational_invariant` | `AsiStackProofs.IntentToExecution` | A compiled execution job preserves the parent contract constraints. | implemented |
| `lean:intent_execution.contracts.failure_blocks_promotion` | `AsiStackProofs.IntentToExecution` | An execution job without required approval cannot transition to running. | implemented |
| `lean:intent_execution.contracts.dispatch_route_envelope` | `AsiStackProofs.IntentToExecution` | A structured execution dispatch review routes missing contracts, missing objective fields, authority widening, hidden overrides, missing approvals, missing artifacts, missing verification plans, known residuals, and complete dispatch reviews into explicit outcomes. | implemented |
| `lean:command.semantic_interface.operational_invariant` | `AsiStackProofs.CommandContracts` | A valid command contract contains objective, constraints, output contract, verification, and failure behavior. | implemented |
| `lean:command.semantic_interface.failure_blocks_promotion` | `AsiStackProofs.CommandContracts` | A hidden or conflicting instruction cannot override an explicit contract constraint. | implemented |

### Planning as a Control Layer: DAGs and Intelligence Arbitrage

Stable ID: `planning-as-a-control-layer`

Chapter job: Accepted goals need to become governed plan graphs and schedulable DAGs with dependencies, authority requirements, context demands, capability tiers, budgets, adequacy contracts, verification burdens, dispatch receipts, escalation paths, and residuals.

Core claim: Planning should be a separate control layer that turns accepted command contracts into schedulable DAGs with explicit dependencies, authority ceilings, context demands, capability-tier assignments, adequacy contracts, verification burdens, cost/quality ledgers, escalation routes, and residuals.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `planforge`, `viea`, `planforge_compiler_arch` | Read first for the control-layer claim, PlanForge DAG/scheduler vocabulary, and command-to-artifact spine. |
| Supporting | `cognitive_compilation`, `software_magic_grimoire`, `tokenmana` | Mine after primary sources for compiler/IR pressure, guarded workflow vocabulary, budgets, capacity, latency, review, and human-friction constraints. |
| Connector or recovery required | `moecot`, `coherence_exchange` | Use as source-note/connector context only unless raw text, code, logs, release artifacts, benchmark records, simulations, or external corroboration are imported or inspected. |

Draft arc:

- Problem: Accepted goals need governed plan graphs whose dependencies, authority requirements, context demands, capability tiers, budgets, adequacy contracts, verification burdens, stop conditions, dispatch receipts, escalation paths, and residuals remain inspectable before execution.
- Insufficiency: Planning cannot be collapsed into prompting, memory, reasoning, routing, or execution because each layer has different authority and failure modes, and cheap route selection is not trustworthy unless adequacy, verification, and residual cost remain attached.
- Mechanism: Compile accepted command contracts into strategic, tactical, and runtime plan graphs with assumptions, task nodes, dependencies, required context, tools, authority requirements, budgets, verification plans, replanning policy, stop conditions, and failure behavior.
- Mechanism: Treat the plan graph as a refusal-friendly control artifact: missing context, blocked dependencies, authority overreach, exhausted budgets, and failed predicates become residuals before side effects.
- Mechanism: Preserve stop conditions, authority ceilings, and alternative-route status during replanning; only dispatchable nodes with satisfied constraints lower into typed jobs.
- Mechanism: Track plan node lifecycle states: proposed, blocked-context, blocked-authority, blocked-dependency, blocked-verification, dispatchable, dispatched, replanned, and stopped.
- Mechanism: Emit dispatch receipts with satisfied constraints, context refs, authority basis, verification plan, replanning history, and typed-job refs.
- Mechanism: Preserve authority budget, replanning history, blocked-node records, residual register, and non-claims so a candidate graph cannot masquerade as governed dispatch.
- Mechanism: Specialize the plan graph into a schedulable PlanForge DAG whose nodes carry dependency order, context demand, authority state, capability tier, adequacy contract, quality predicate, verification requirement, budget limit, route assignment, merge condition, escalation path, and residual behavior.
- Mechanism: Give each node both a work contract and an adequacy contract so schedulability depends on authority, context, quality predicate, verification, fallback, and downstream usability.
- Mechanism: Track scheduling states such as ready, blocked by dependency, blocked by authority, blocked by context, blocked by budget, blocked by verifier, running, failed, residual, and merged.
- Mechanism: Preserve scheduling state, adequacy contracts, merge conditions, assumption refs, cost-quality ledger, residuals, and non-claims so cheap branches cannot hide displaced verification, repair, or human cleanup.
- Mechanism: Use local repair: when a source, assumption, route, or quality predicate changes, repair the affected subgraph and rerun only dependents whose obligations changed.
- Interface: Alignment filters goals.
- Interface: VCM supplies context packets.
- Interface: Routing consumes capability annotations, adequacy contracts, route assignments, and escalation paths.
- Interface: Cognitive Compilation receives accepted plan obligations for semantic IR lowering.
- Interface: Labor OS and runtime adapters execute only typed jobs derived from dispatch receipts.
- Interface: Evidence ledgers record assumptions, cost-quality decisions, residuals, verification results, and replanning events.

Primary invariants:

- Plans expose constraints and stop conditions.
- Runtime replanning preserves authority limits.
- Tool selection is justified by task requirements.
- Only dispatchable nodes lower into typed jobs.
- Candidate routes, blocked nodes, and review notes are not executable permission.
- Dependency order is respected before dispatch.
- Cost savings do not remove required verification.
- Failed quality predicates route to escalation or residuals.
- Merge gates compare assumptions, source versions, authority ceilings, and quality predicates before parallel branches are accepted together.

Failure modes to cover:

- Scope creep.
- Planning without replanning.
- Tool choice exceeds authority or budget.
- Dispatch laundering, where a proposed or blocked node becomes a job because it appears in the graph.
- Replanning erasure, where feedback changes the plan while hiding the authority, stop-condition, or residual delta.
- Wrong capability-tier selection, where a cheap route produces plausible but inadequate work.
- Dependency cycles, where a graph looks planned while no valid dispatch order exists.
- Merge laundering, where parallel branches pass locally while relying on conflicting assumptions or source versions.
- Arbitrage laundering, where verification, repair, or human cleanup is moved outside the cost-quality ledger.

Draft deliverables:

- A plan graph and PlanForge DAG record surface with dependencies, context requests, authority budget, risk budgets, stop conditions, lifecycle states, dispatch receipts, blocked-node records, residual register, scheduling states, capability tiers, adequacy contracts, quality predicates, route assignments, merge conditions, assumption refs, escalation paths, cost-quality ledgers, and non-claims.
- Implemented protocol validation: `plan_graph` fixture validates public record shape only, including authority budget, replanning history, lifecycle states, blocked nodes, dispatch receipts, residual register, and non-claims.
- Implemented protocol validation: `planforge_dag` fixture validates public record shape only, including nodes, edges, scheduling states, capability tiers, context requests, adequacy contracts, quality predicates, verification requirements, budget limits, route assignments, merge conditions, assumption refs, escalation policy, residuals, cost-quality ledger, and non-claims.
- Exact Appendix C claim-source mappings for the merged planning-control claim across PlanForge planning middleware and DAG/MVI scheduling, VIEA orchestration/runtime spine, PlanForge compiler-architecture framing, Cognitive Compilation source-plan/S-IR and semantic-DAG routing/repair, Software Magic Grimoire spell-stack workflow discipline, TokenMana resource-governance pressure, Coherence Exchange speculative intelligence-arbitrage framing, and MoECOT runtime-reference context. Six local raw-cache mappings (`planforge`, `viea`, `cognitive_compilation`, `software_magic_grimoire`, `planforge_compiler_arch`, `tokenmana`) have reviewed passage references. `coherence_exchange` and `moecot` remain source-note/connector mapped until usable raw text, code, logs, release artifacts, benchmark records, simulations, or external corroboration are imported or inspected. Support remains `argument` pending planner harnesses, dependency-order checks, context-demand tests, selected-tier adequacy tests, route traces, cost-quality results, runtime replanning traces, or accepted evidence transitions.
- Planned Codex test: Decomposition accuracy test.
- Implemented synthetic Codex test: Dependency ordering and blocked-versus-dispatchable state checks via `python3 scripts/validate_plan_execution_contracts.py`; runtime planner remains open.
- Implemented finite-record proof follow-through: `AsiStackProofs.Planning` now includes a `PlanControlRecord` envelope for modeled dispatchable, blocked, and replanned records plus a finite `PlanControlRouteFor` dispatch decision; it checks required dispatch gates, receipt separation, parent-authority preservation, replanning stop-condition preservation, residual bookkeeping, non-claim presence, and valid dispatchable-record routing to `allowDispatch` without treating those predicates as planner-quality, route-quality, scheduler, or runtime-replanning evidence.
- Implemented finite-record proof follow-through: `AsiStackProofs.Planning` now includes a `PlanGraphAdmissionReview` and `PlanGraphAdmissionRouteFor` decision surface for missing command-contract acceptance, decomposition, acyclicity, dependency order, authority inheritance, context demand, adequacy contracts, verification plans, dispatch gates, dispatch receipts, replanning controls, residual registers, and non-claim boundaries; this remains record-routing evidence only, not decomposition quality, selected-tier adequacy, route quality, scheduler behavior, or deployed replanning.
- Planned Codex test: Context-demand prediction test.
- Planned Codex test: Runtime replanning test.
- Planned Codex test: Dispatch-state enforcement test.
- Planned Codex test: Replanning-delta audit.
- Implemented synthetic Codex test: DAG acyclicity test via `python3 scripts/validate_plan_execution_contracts.py`; deployed scheduler cycle rejection remains open.
- Planned Codex test: Capability tier assignment test.
- Implemented Lean proof target: a failed quality predicate routes to escalation or residual under the valid node-outcome predicate.
- Planned Codex test: deployed scheduler cycle rejection.
- Consolidation note: `planforge-dags-and-intelligence-arbitrage` folded into this chapter on 2026-06-30 as DAG scheduling, intelligence-arbitrage, capability-tier, adequacy-contract, cost-quality-ledger, escalation, residual, source-mapping, fixture, proof-hook, and history material; `cognitive-compilation-and-semantic-ir` remains standalone.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:planning.control_layer.operational_invariant` | `AsiStackProofs.Planning` | A plan node inherits the authority ceiling of its parent contract unless governance lowers it. | implemented |
| `lean:planning.control_layer.failure_blocks_promotion` | `AsiStackProofs.Planning` | A plan with unsatisfied required constraints cannot be dispatched. | implemented |
| `lean:planning.control_layer.plan_graph_admission_route` | `AsiStackProofs.Planning` | Modeled plan-graph admission routes missing command-contract acceptance, decomposition, acyclicity, dependency order, authority inheritance, context demand, adequacy contracts, verification plans, dispatch gates, dispatch receipts, replanning controls, residual registers, and non-claim boundaries to explicit outcomes. | implemented |
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
| External comparators | `ext_pddl_1998`, `ext_shop2_2003`, `ext_tree_of_thoughts_2023`, `ext_dreamcoder_2020`, `ext_llvm_langref_docs`, `ext_mlir_2020`, `ext_translation_validation_1998` | Use for planning-language, decomposition, reasoning-search, program-synthesis, compiler-IR, multi-level IR, and translation-validation positioning only; do not treat as cognitive-compiler runtime evidence. |

Draft arc:

- Problem: LLM workflows need intermediate representations that separate requirements, plans, artifacts, repairs, and target runtimes.
- Insufficiency: Generate-from-prompt workflows entangle requirements and implementation, drift over long contexts, and make incremental repair fragile.
- Mechanism: Represent requirements, semantics, dependencies, artifacts, and target constraints explicitly.
- Mechanism: Perform incremental repair over IR rather than re-prompting from scratch.
- Mechanism: Compile IR into jobs, code, schemas, or documents.
- Mechanism: emit lowering receipts that bind source-plan obligations, semantic atoms, target artifacts, validators, assumptions, and residuals.
- Mechanism: Preserve atom state, source-plan refs, obligation refs/status, assumptions, IR validity state, validator status, lowering state, target artifact refs, lowering receipts, repair-ledger refs, source refs, support-state effect, residuals, and non-claims so syntactic artifact acceptance cannot stand in for obligation-preserving lowering.
- External positioning: Compare semantic IR to PDDL/SHOP2 planning interfaces, Tree-of-Thoughts reasoning paths, DreamCoder program-synthesis abstractions, LLVM IR, MLIR, and translation validation; preserve the distinction between compiler lineage and a working cognitive compiler.
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
- Exact Appendix C claim-source mappings for the Cognitive Compilation claim across Cognitive Compilation S-IR/repair architecture, PlanForge compiler-orchestration framing, GenesisCode evidence-carrying IR/provenance discipline, TreeLLM external semantic-substrate intuition, and VIEA intent-to-artifact ledger context; all five local mappings now have reviewed passage references. Support remains `argument` pending source-plan parsing, real target-lowering preservation, concrete artifact-validator adequacy, localized-repair results, quality/cost measurements, or accepted evidence transitions.
- Implemented synthetic Codex test: Requirement preservation test via `python3 scripts/validate_plan_execution_contracts.py`; source-plan parser and real target artifact validation remain open.
- Implemented proof-backed check: finite semantic-lowering route coverage for missing source plans, missing atoms, missing obligation links, cyclic dependencies, authority escapes, missing validators, validator failures, missing receipts, obligation loss, invalidating repairs without ledger updates, known residuals, and complete lowering reviews.
- Implemented synthetic Codex test: Cognitive compilation trace harness via `python3 scripts/validate_cognitive_compilation_traces.py`, checking 2 valid and 4 expected-invalid hand-authored source-plan/semantic-atom/lowering-receipt/target-audit/repair-trace fixtures for receipt representation, obligation preservation, target-audit state, localized repair scope, syntactic-pass laundering rejection, and no-promotion boundaries.
- Remaining test gap: source-plan parser, concrete target artifact validators, real target-lowering behavior, localized-repair benchmark, and direct-generation quality/cost comparison.
- Source-noted external comparator queue: `ext_pddl_1998`, `ext_shop2_2003`, `ext_tree_of_thoughts_2023`, `ext_dreamcoder_2020`, `ext_llvm_langref_docs`, `ext_mlir_2020`, and `ext_translation_validation_1998` now ground planning-language, decomposition, reasoning-search, program-synthesis, compiler-IR, multi-level lowering, and translation-validation vocabulary; no LLVM/MLIR toolchain, compiler pass, semantic lowering trace, translation validator, source-target proof, program-synthesis run, or support-state promotion is claimed.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:cognitive_compilation.ir.operational_invariant` | `AsiStackProofs.CognitiveCompilation` | A compiled artifact preserves all required IR obligations. | implemented |
| `lean:cognitive_compilation.ir.failure_blocks_promotion` | `AsiStackProofs.CognitiveCompilation` | A repair that invalidates an existing obligation cannot be accepted without updating the ledger. | implemented |
| `lean:cognitive_compilation.ir.semantic_lowering_route_envelope` | `AsiStackProofs.CognitiveCompilation` | A structured semantic-lowering review routes missing source plans, missing atoms, missing obligation links, cyclic dependencies, authority escapes, missing validators, validator failures, missing receipts, obligation loss, invalidating repairs without ledger updates, known residuals, and complete lowering reviews into explicit outcomes. | implemented |

### The Virtual Context ABI: Typed Pages, Cells, and Certificates

Stable ID: `virtual-context-abi`

Chapter job: Long-horizon agents need a stable context interface whose addresses, versions, materializations, typed pages, context cells, certificates, authority labels, loss contracts, adequacy states, and faults remain inspectable across planning, reasoning, execution, and audit.

Core claim: Virtual Context Memory should expose a Virtual Context ABI that materializes typed pages and context cells with stable addresses, versions, certificates, authority ceilings, loss/use contracts, adequacy states, residuals, and typed faults.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `vcm_public` | Read first for the ABI, semantic-page, certificate, admission, adequacy, and typed-fault vocabulary. |
| Supporting | `context_engineer`, `verification_bandwidth`, `viea`, `spinoza` | Mine after primary sources for context supply-chain pressure, verification-capacity limits, execution-spine connections, and claim/evidence cell boundaries. |
| Connector or recovery required | `vcm_editable`, `moecot` | Use source notes or connector reads before source-derived claims; no resolver, VCM-Bench, runtime, or benchmark result is promoted from these sources. |

Draft arc:

- Problem: Long-horizon agents need a stable context interface whose addresses, versions, materializations, typed pages, context cells, certificates, authority labels, loss contracts, adequacy states, and faults remain inspectable across planning, reasoning, execution, and audit.
- Insufficiency: Long context windows, retrieval systems, and summaries can move text close to a model without defining stable addressability, representation authority, source bindings, omission records, permitted uses, adequacy boundaries, or typed failure behavior.
- Mechanism: Resolve context requests through address, version, mount, snapshot, representation need, authority ceiling, adequacy target, consumer policy, lease, and typed fault behavior.
- Mechanism: Represent materialized context as typed pages or cells: constraints, claims, decisions, corrections, events, artifacts, exact excerpts, lossy summaries, redactions, abstractions, translations, and derived inferences.
- Mechanism: Attach representation certificates with source refs, omissions, loss contracts, permitted uses, authority ceilings, validity state, revocation state, transaction refs, artifact refs, residual risks, and non-claims.
- Mechanism: Separate request validity, resolution validity, materialization validity, admission validity, and adequacy validity so context availability cannot become evidence readiness.
- Mechanism: Treat certificate updates, revocations, stale certificates, and attempted use outside the certificate as auditable state transitions rather than prose edits.
- Mechanism: Preserve a static-versus-dynamic boundary: this chapter owns address/cell/certificate shape; `context-transactions-snapshots-mounts-and-taint` owns transaction, branch, taint, deletion, and declassification semantics.
- Mechanism: Preserve an admission-versus-verification boundary: this chapter can record admitted context; `verification-bandwidth-and-context-adequacy` owns whether admitted context is adequate for a target claim.
- Interface: Planning requests context by task, address, authority, representation need, and adequacy target.
- Interface: VCM materializes packets and cells with static address, version, certificate, source-ref, authority, loss, use, lease, residual, and fault fields.
- Interface: Spinoza and claim ledgers consume claim/evidence cells without treating certificates as support-state decisions.
- Interface: Execution consumes only permitted representations.
- Interface: Artifact graphs store certificate references when context-derived representations become durable work products.

Primary invariants:

- Addresses and versions are stable.
- Source bindings survive representation changes.
- Authority labels survive summarization.
- Loss and permitted-use contracts are explicit.
- Derived cells point back to source bindings.
- Context admission and context adequacy remain distinct.
- Mandatory context misses produce typed faults rather than best-effort packets.
- Summaries cannot increase the authority ceiling of their source cells.
- Revoked or stale certificates cannot be treated as current support.

Failure modes to cover:

- Flat transcript memory.
- Stale context.
- Summary overconfidence.
- Provenance loss.
- Authority escalation through compression.
- Unsafe fit.
- Adequacy laundering.
- Certificate laundering.

Draft deliverables:

- A merged static ABI/certificate chapter that preserves context ABI records and semantic page certificates as one interface skeleton rather than two repeated context chapters.
- Implemented protocol validation: `context_abi_record` and `semantic_page_certificate` fixtures validate public record shapes only, including lifecycle, request, address, version, mount, snapshot, representation, authority, admission, adequacy, fault, source bindings, derivation, loss contract, permitted uses, revocation state, support-state effect, residuals, and non-claims.
- Exact Appendix C claim-source mappings for `virtual-context-abi.core` across VCM public-v1, Context Engineer, Verification Bandwidth, VIEA, Spinoza, editable VCM, and MoECOT; the local raw-cache mappings are passage-reviewed where available, while connector-only sources remain bounded.
- Folded-history preservation for `semantic-pages-context-cells-and-certificates.core` as a subclaim about typed pages, context cells, representation certificates, source bindings, omissions, authority ceilings, loss contracts, and permitted uses.
- Implemented synthetic Codex tests: admission versus adequacy, conflict adequacy classification, context fault behavior, stale certificate rejection, and admission-as-verification rejection via `python3 scripts/validate_context_admission_adequacy.py`; no deployed resolver, memory store, summary fidelity, certificate truthfulness, model-facing context, or VCM-Bench result is claimed.
- Implemented proof-backed check: finite context-admission route coverage for malformed requests, missing addresses, authority escapes, absent mandatory context, absent optional context, missing certificates, stale certificates, taint, failed adequacy, residuals, and complete materialization reviews.
- Implemented proof-backed check: finite certificate-lifecycle route coverage for malformed certificates, missing source bindings, missing loss or use contracts, authority escapes, omitted-material gaps, scope violations, stale certificates, revocation, taint, deletion-closure gaps, missing verifier refs, consumer-policy violations, support-promotion attempts without evidence transitions, and complete reviews; no resolver truthfulness, deletion enforcement, or semantic-fidelity claim is promoted.
- Planned Codex tests: resolver conformance, summary-fidelity evaluator, certificate truthfulness checker, and paired source/derived-cell omission audit.
- Historical treatment: `semantic-pages-context-cells-and-certificates` is archived and redirected to `virtual-context-abi`; the old chapter can be restored only if paired source/derived cells, certificate truthfulness tests, summary-fidelity tests, or independent interoperability evidence make it chapter-owning again.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:vcm.abi.operational_invariant` | `AsiStackProofs.VirtualContextABI` | A context reference resolves only when the requested address and version are valid for the snapshot. | implemented |
| `lean:vcm.abi.failure_blocks_promotion` | `AsiStackProofs.VirtualContextABI` | A mandatory context miss produces a typed fault rather than a best-effort packet. | implemented |
| `lean:vcm.abi.context_admission_route_envelope` | `AsiStackProofs.VirtualContextABI` | A structured context-admission review routes malformed requests, missing addresses, authority escapes, absent mandatory context, absent optional context, missing certificates, stale certificates, taint, failed adequacy, residuals, and complete materialization reviews into explicit outcomes. | implemented |
| `lean:vcm.certificates.operational_invariant` | `AsiStackProofs.ContextCertificates` | A derived context cell carries source bindings and a declared loss/use contract. | implemented |
| `lean:vcm.certificates.failure_blocks_promotion` | `AsiStackProofs.ContextCertificates` | A summary cannot increase the authority ceiling of its source cells. | implemented |
| `lean:vcm.certificates.lifecycle_admission_route` | `AsiStackProofs.ContextCertificates` | A structured certificate-lifecycle review routes malformed certificates, missing source bindings, missing loss or use contracts, authority escapes, omitted-material gaps, scope violations, stale certificates, revocation, taint, deletion-closure gaps, missing verifier refs, consumer-policy violations, support-promotion attempts without evidence transitions, and complete reviews into explicit outcomes. | implemented |

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
- Implemented Lean proof follow-through: finite materialization/deletion-closure records now block allowed materialization when an open deletion obligation lacks closure or declassification, and the finite transaction-route review rejects missing or stale snapshots, branch leaks, unrepaired mount faults, taint without declassification, deleted-cell materialization without closure, invisible committed reads, missing replay boundaries, unsupported support promotion, and missing non-claim boundaries while admitting a complete modeled committed read. This remains finite-record coverage only, not deployed memory-store behavior.
- Exact Appendix C claim-source mappings for the Context Transactions claim across VCM public-v1 transaction/snapshot/invalidation/deletion semantics, Ladon/Manhattan sensitive-compartment and handle boundaries, Context Engineer clearance-labeled mission contexts and Digital SCIF lifecycle, Black Hole Context Manager memory-budget/drift/freeze/evict patterns, and editable VCM refinement context; the four local mappings (`vcm_public`, `ladon_manhattan`, `context_engineer`, `black_hole_context_manager`) now have reviewed passage references. `vcm_editable` remains connector/source-note mapped until usable raw text, deployed memory-store artifacts, VCM-Bench records, or external corroboration are imported or inspected. Support remains `argument` pending deployed memory-store behavior, runtime mount-visibility tests, branch-isolation checks, deployed deletion-closure behavior, side-channel validation, context-manager execution, benchmark reproduction, or accepted evidence transitions.
- Implemented synthetic Codex test: Deletion closure test via `python3 scripts/validate_context_admission_adequacy.py`; deployed memory-store deletion closure remains open.
- Implemented synthetic Codex test: bounded memory-store conformance harness via `python3 scripts/validate_context_transaction_memory_store.py`; no deployed memory-store, VCM conformance, side-channel, benchmark, or support-state-promotion claim.

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
- Implemented synthetic Codex test: Adequacy labeling test via `python3 scripts/validate_context_admission_adequacy.py`; model verification-bandwidth measurement remains open.
- Implemented synthetic Codex test: Verification escalation test via `python3 scripts/validate_context_admission_adequacy.py`; deployed escalation remains open.
- Implemented proof-backed check: finite verification-adequacy route coverage for missing claims, unadmitted context, high-risk inadequate context, missing pairwise checks, missing verification artifacts, open negative evidence, contradictions, residuals, complete verified-support reviews, and complete draft-support reviews.
- Planned Codex test: Mode-confusion audit.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:verification_bandwidth.adequacy.operational_invariant` | `AsiStackProofs.VerificationBandwidth` | A context packet admitted for use may still be marked inadequate for a target claim. | implemented |
| `lean:verification_bandwidth.adequacy.failure_blocks_promotion` | `AsiStackProofs.VerificationBandwidth` | A high-risk claim with inadequate context cannot receive a verified support label. | implemented |
| `lean:verification_bandwidth.adequacy.route_envelope` | `AsiStackProofs.VerificationBandwidth` | A structured verification-adequacy review routes missing claims, unadmitted context, high-risk inadequate context, missing pairwise checks, missing verification artifacts, open negative evidence, contradictions, residuals, complete verified-support reviews, and complete draft-support reviews into explicit outcomes. | implemented |

### Claim Ledgers and Belief Revision

Stable ID: `claim-ledgers-and-belief-revision`

Chapter job: The architecture needs a durable epistemic layer for claims, evidence, contradictions, uncertainty, and revision.

Core claim: Reasoning should maintain claim ledgers with support states, provenance, contradiction links, uncertainty, and revision history.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `spinoza`, `viea` | Read first for chapter claims and mechanisms. |
| Supporting | `coherence_exchange`, `aletheia`, `uat` | Mine after primary sources for cross-layer connections, variants, and failure modes. |
| External comparators | `ext_agm_belief_revision_1985`, `ext_truth_maintenance_system_1979`, `ext_assumption_based_tms_1986`, `ext_alce_2023`, `ext_self_rag_2023`, `ext_checklist_2020` | Load after internal claim-ledger sources to position the chapter against formal belief revision, truth maintenance, assumption-based truth maintenance, citation support, retrieval critique, and behavioral testing. Treat these as lineage/comparators, not evidence that the ASI Stack implements belief revision. |

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
- Source-noted external comparator rows for AGM belief revision, Doyle-style truth maintenance, de Kleer-style assumption-based truth maintenance, ALCE, Self-RAG, and CheckList, with the chapter framed as a publication/support-state ledger bridge rather than an implemented formal belief-revision or truth-maintenance engine.
- Implemented protocol validation: `claim_record` and `belief_revision_record` fixtures validate public record shape only.
- Planned Codex test: Claim extraction test.
- Planned Codex test: Contradiction detection test.
- Implemented Lean proof target: finite claim updates preserve prior evidence and revision-history references.
- Implemented Lean proof target: open contradictions block promotion until handled.
- Implemented Lean proof target: finite revision-lifecycle routing sends missing claim identity, support-state gaps, unsupported promotion, open contradictions, history loss, surface-sync gaps, split/downgrade/residual gaps, and non-claim-boundary gaps to explicit modeled outcomes.
- Planned Codex test: belief revision engine test.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:claims.ledger.operational_invariant` | `AsiStackProofs.ClaimLedger` | A claim update preserves prior evidence and revision history. | implemented |
| `lean:claims.ledger.failure_blocks_promotion` | `AsiStackProofs.ClaimLedger` | A contradiction prevents promotion until resolved, bounded, or recorded as residual. | implemented |
| `lean:claims.ledger.revision_lifecycle_route` | `AsiStackProofs.ClaimLedger` | A modeled revision request routes missing claim identity, support-state gaps, unsupported promotion, open contradictions, history loss, surface-sync gaps, split/downgrade/residual gaps, and non-claim-boundary gaps to explicit outcomes. | implemented |

### Proof-Carrying Claims and Adversarial Review

Stable ID: `spinoza-verification-and-proof-carrying-claims`

Chapter job: High-value claims and high-risk artifacts need a governed verification path that can choose proof, citation, procedure, replay, benchmark, or adversarial-review treatment without laundering failed, mismatched, or contested evidence into support.

Core claim: Selected claims and artifacts should move through proof-carrying, justification-carrying, or adversarial-review envelopes that record tier, interpretation mapping, evidence dossier, verifier or tribunal result, dissent, limitations, failed attempts, required actions, residuals, and ledger effects.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `spinoza` | Read first for proof-carrying claims, tier discipline, verifier separation, and no-theorem-laundering boundaries. |
| Supporting | `genesiscode`, `coherence_exchange`, `verification_bandwidth`, `treellm`, `uat`, `talos` | Mine after primary sources for obligation envelopes, verification-workspace limits, semantic traces, tribunal review, typed review artifacts, and execution consequences. |
| External comparator | `ext_proof_carrying_code_1997`, `ext_lean4_theorem_proving`, `ext_autoformalization_llms_2022`, `ext_ai_safety_debate_2018`, `ext_llm_as_judge_mt_bench_2023`, `ext_contestable_ai_design_2022` | Use after source notes for proof-carrying-code, theorem-proving, autoformalization, debate, LLM-as-judge, and contestable-review positioning; do not treat comparators as local verifier, theorem-validity, semantic-equivalence, debate-quality, judge-calibration, tribunal-quality, or institutional-adequacy evidence. |

Draft arc:

- Problem: High-value claims and high-risk artifacts need a governed verification path that can choose proof, citation, procedure, replay, benchmark, or adversarial-review treatment without laundering failed, mismatched, or contested evidence into support.
- Insufficiency: Neural generation, one-pass self-critique, and informal review can produce plausible justification language without preserving proof scope, verifier result, evidence dossier, dissent, failed attempts, verdict constraints, or downgrade routes.
- Mechanism: Select a verification route for each selected claim or artifact: formal proof, citation dossier, executable procedure, replay log, benchmark artifact, tribunal review, downgrade, block, or escalation.
- Mechanism: Record interpretation mapping, justification artifact, verifier result, failed attempts, limitations, semantic adequacy, and support-state effect before any stronger claim standing is allowed.
- Mechanism: Escalate contested, high-risk, or mismatched cases into tribunal records with bounded dossiers, reviewer roles, adversarial probes, dissent, verdict constraints, and required actions.
- Mechanism: Write bounded effects back to the claim ledger and execution layers: no change, downgrade, block, revise, scoped accept, dispatch blocker, authority narrowing, human sign-off, or residual work.
- Handoff: Verification outcomes that constrain downstream work flow to Labor OS and Typed Jobs.
- Interface: Claim ledgers supply stable claim identity and receive bounded verification outcomes.
- Interface: Lean, GenesisCode, Circle-style proof contracts, procedures, replay logs, and benchmark artifacts supply formal or executable evidence when appropriate.
- Interface: UAT-style tribunal review handles contested, high-risk, or mismatched cases.

Primary invariants:

- Proof tier is explicit.
- Formal, citation, and procedure tiers require matching artifacts.
- Failed, timed-out, or mismatched verification blocks promotion or routes to downgrade, no change, block, or escalation.
- Narrow passes cannot promote broader natural-language claims without semantic adequacy review.
- Dissent remains visible.
- High-risk artifacts cannot bypass required tribunal review.
- Prior review over unchanged evidence cannot quietly reverse a rejection into acceptance.

Failure modes to cover:

- Certified delusion.
- Invalid formalization.
- Justification artifact missing.
- Reviewer collusion.
- Consensus theater.
- Critique without action.
- Repeated-review laundering.

Draft deliverables:

- A proof-carrying-claim schema and tribunal-review schema with synthetic valid and expected-invalid fixtures for narrow formal passes, citation no-change, mismatch escalation, missing artifacts, failed verification, high-risk review, dissent, and prior-review laundering.
- Exact Appendix C claim-source mappings for `spinoza-verification-and-proof-carrying-claims.core` across Spinoza, GenesisCode, Coherence Exchange, Verification Bandwidth, TreeLLM, UAT, and Talos; six local raw-cache mappings are passage-reviewed, while `coherence_exchange` remains connector/source-note mapped.
- Folded-history preservation for `unified-adaptive-tribunal-and-adversarial-review.core` as a subclaim about bounded dossiers, reviewer roles, adversarial probes, dissent, verdict constraints, cycle caps, unchanged-evidence guards, and required actions.
- Source-noted external comparator rows for proof-carrying code, Lean theorem proving, LLM autoformalization, AI safety debate, LLM-as-judge evaluation, and contestable-AI design, with the chapter framed as verification-route and review-record discipline rather than a local autoformalizer, debate system, LLM judge, or tribunal-quality result.
- Implemented protocol validation: `proof_carrying_claim` and `tribunal_review_record` fixtures validate public record shape only.
- Implemented Codex tests: proof-carrying claim synthetic harness and tribunal-review synthetic harness.
- Implemented Lean follow-through: `AsiStackProofs.Tribunal` now includes a finite lifecycle route envelope for missing review, high-risk probe/independence gaps, changed-evidence reuse, unrecorded dissent, action constraints, missing evidence-transition records, and complete bounded review, without claiming reviewer quality, probe quality, verdict correctness, action enforcement, deployed tribunal behavior, or support-state promotion.
- Planned Codex test: Tier assignment over real verifier outputs.
- Planned Codex test: Adversarial review quality over reproducible dossiers.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:spinoza.proof_carrying.operational_invariant` | `AsiStackProofs.ProofCarryingClaims` | A claim at a formal support tier carries a valid proof or justification artifact reference. | implemented |
| `lean:spinoza.proof_carrying.failure_blocks_promotion` | `AsiStackProofs.ProofCarryingClaims` | A failed verifier result downgrades or blocks the claim rather than promoting it. | implemented |
| `lean:tribunal.review.operational_invariant` | `AsiStackProofs.Tribunal` | A tribunal verdict includes reviewer roles, evidence references, and unresolved dissent. | implemented |
| `lean:tribunal.review.failure_blocks_promotion` | `AsiStackProofs.Tribunal` | A high-risk artifact cannot be accepted when required tribunal review is absent. | implemented |

Historical treatment: `unified-adaptive-tribunal-and-adversarial-review` is archived and redirected to `spinoza-verification-and-proof-carrying-claims`; the old chapter can be restored only if independent tribunal pipeline evidence, reviewer-independence measurements, adversarial-probe-quality tests, verdict-correctness audits, or institutional contestability evidence make it chapter-owning again.

### Labor OS and Typed Jobs

Stable ID: `labor-os-and-typed-jobs`

Chapter job: Intelligence must become typed work with lifecycle, permissions, artifacts, logs, and approvals.

Core claim: The execution layer should convert plans into typed jobs managed by a governed labor operating system.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `talos` | Read first for chapter claims and mechanisms. |
| Supporting | `viea`, `genesiscode`, `software_magic_grimoire` | Mine after primary sources for cross-layer connections, variants, and failure modes. |
| External comparators | `ext_temporal_docs`, `ext_airflow_dag_docs`, `ext_bpmn_2_0_2_spec`, `ext_kubernetes_jobs_docs` | Use for durable-execution, DAG orchestration, process-notation, and batch-job lifecycle positioning only; do not treat as Labor OS runtime evidence. |
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
- External positioning: Compare Labor OS typed jobs to Temporal durable execution, Airflow DAG orchestration, BPMN process notation, and Kubernetes batch-job lifecycle semantics; preserve the distinction between operational workflow completion and ASI Stack evidence readiness.
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
- Implemented synthetic Codex test: Typed job lifecycle test via `python3 scripts/validate_plan_execution_contracts.py`; deployed job runner remains open.
- Implemented proof-backed check: finite job-execution route coverage for missing jobs, unlocked contracts, invalid lifecycles, missing approvals, missing permissions, observed failures, residuals, unverified delivery, verified delivery, scheduler-slot waits, dispatch-ready jobs, and retirement requests.
- Planned Codex test: Tool permission enforcement test.
- Implemented Lean predicate: an approval-required job cannot be allowed to run before approval is recorded.
- Implemented synthetic Codex test: Human approval gate test via `python3 scripts/validate_plan_execution_contracts.py`; deployed approval service remains open.
- Planned Codex test: Delivery versus evidence-ready test.
- Planned Codex test: Job parentage trace test.
- Source-noted external comparator queue: `ext_temporal_docs`, `ext_airflow_dag_docs`, `ext_bpmn_2_0_2_spec`, and `ext_kubernetes_jobs_docs` now ground durable workflow, DAG, process-notation, and batch-job lifecycle vocabulary; no Temporal workflow, Airflow DAG, BPMN engine, Kubernetes Job, deployed scheduler, or workflow trace is claimed.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:jobs.lifecycle.operational_invariant` | `AsiStackProofs.TypedJobs` | A job transitions only through valid lifecycle states. | implemented |
| `lean:jobs.lifecycle.failure_blocks_promotion` | `AsiStackProofs.TypedJobs` | A job requiring approval cannot execute before approval is recorded. | implemented |
| `lean:jobs.lifecycle.execution_route_envelope` | `AsiStackProofs.TypedJobs` | A structured job-execution review routes missing jobs, unlocked contracts, invalid lifecycles, missing approvals, missing permissions, observed failures, residuals, unverified delivery, verified delivery, scheduler-slot waits, dispatch-ready jobs, and retirement requests into explicit outcomes. | implemented |

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
- Implemented Lean route envelope: artifact-admission review now covers missing artifact, parent/source/context/transaction/certificate/tool/claim/test/audit/replay/evidence/non-claim blockers, replay-grade sufficiency, stale-certificate blocking, blocked promotion, complete non-promoted admission, and approved-promoted admission over modeled records only.
- Implemented synthetic Codex test: `python3 scripts/validate_artifact_graph_replay.py` checks artifact parentage, typed job outputs, context transaction refs, semantic certificate refs, source-ref coverage, replay grade, observed artifacts, audit reconstruction, stale-certificate blocking, and promotion-blocking boundaries. It remains synthetic record-gate evidence only, not a deployed artifact graph, replay engine, audit-reconstruction service, or source-interpretation claim.
- Implemented synthetic Codex test: Audit reconstruction test via `python3 scripts/validate_artifact_graph_replay.py`; deployed audit reconstruction remains open.
- Implemented synthetic Codex test: Replay metadata completeness test via `python3 scripts/validate_artifact_graph_replay.py`; deployed replay engine remains open.

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
- Implemented Lean predicate: a valid invocation requires the parent job permissions to include the adapter capability and its effect lease to be active, scoped to that capability, and sandboxed.
- Implemented Lean predicate: a high-impact adapter invocation without approval is rejected.
- Implemented Lean negative cases: mismatched, expired, or unsandboxed effect leases cannot validate invocation, and a high-impact rollback-required invocation without a rollback handle cannot remain unrejected.
- Implemented synthetic Codex test: `python3 scripts/validate_runtime_adapter_permissions.py` checks typed-job, runtime-adapter-invocation, authority-use-receipt, and authority-probe consistency for permission coverage, high-impact approval gates, approval expiry markers, effect receipts, rollback handles, irreversible residuals, authority receipt alignment, ambient-authority confused-deputy rejection, and revoked-receipt blocking. It remains synthetic record-gate evidence only, not deployed adapter, sandbox, approval-service, rollback-execution, deployed revocation propagation, or secret-handle evidence.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:runtime.adapters.operational_invariant` | `AsiStackProofs.RuntimeAdapters` | A runtime adapter invocation is valid only when job permissions include the adapter capability and its effect lease is active, scoped to that capability, and sandboxed. | implemented |
| `lean:runtime.adapters.failure_blocks_promotion` | `AsiStackProofs.RuntimeAdapters` | A high-impact adapter call without approval or a required rollback handle is rejected, mismatched, expired, or unsandboxed effect leases cannot validate invocation, and modeled confused-deputy or sandbox-escape attempts cannot pass dispatch. | implemented |

### Procedural Memory and Cognitive Loop Closure

Stable ID: `procedural-memory-and-cognitive-loop-closure`

Chapter job: Repeated reasoning trajectories should not be improvised forever when they can become verified procedures or tools.

Core claim: Cognitive loop closure compiles repeated reasoning into verified parameterized tools and procedural memory.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `cognitive_loop_closure` | Read first for chapter claims and mechanisms. |
| Supporting | `rmi`, `rgs`, `benchmaxxing`, `talos`, `project_theseus_whitepaper`, `theseus_self_evolution_system`, `theseus_operator_os` | Mine after primary sources for cross-layer connections, variants, and failure modes. |
| External comparators | `ext_memgpt_2023`, `ext_toolformer_2023`, `ext_voyager_2023`, `ext_dreamcoder_2020` | Use after source notes to ground memory-management, learned-tool-use, skill-library, and library-learning comparators; do not treat reported results as local reproduction or support-state promotion. |
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
- Implemented synthetic Codex test: `python3 scripts/validate_procedural_memory_loop.py` checks qualification packets for comparable repeated trace clusters, negative-example preservation, abstraction fields, regression quarantine, retirement triggers, source-trace mismatch, and explicit non-claim boundaries. It remains synthetic record-gate evidence only, not deployed loop-detection, tool-synthesis, generated-tool correctness, regression-quality, route-quality, monitoring, or retirement-automation evidence.
- Implemented Lean lifecycle route envelope: modeled routable transitions require comparable traces, negative examples, closure artifacts, verification, clean regressions, benchmark floor, active SCF target, retirement handling, monitoring plan, residuals, non-claims, and a verified or routable source state; valid routable, quarantined, and retired synthetic fixture shapes have Lean bridge records.
- Implemented external grounding: source notes exist for MemGPT, Toolformer, Voyager, and DreamCoder as external comparators for memory tiers, learned API/tool use, executable-code skill libraries, and program-synthesis library learning; no local reproduction, tool-synthesis result, skill-library transfer result, or support-state promotion is claimed.
- Implemented Codex test: Loop detection test, for synthetic qualification packets only.
- Planned Codex test: Procedure qualification state test.
- Implemented Codex test: Negative-example preservation test, for synthetic qualification packets only.
- Implemented Codex test: Tool abstraction test, for synthetic qualification packets only.
- Implemented Codex test: Verified tool regression test, for synthetic qualification packets only.
- Implemented Codex test: Retirement trigger test, for synthetic qualification packets only.

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
| Primary | `octopus_router`, `rmi`, `benchmaxxing` | Read first for chapter claims, routing mechanisms, and runtime-promotion pressure. |
| Supporting | `beastbrain`, `cognitive_loop_closure`, `rgs`, `viea`, `scf`, `talos`, `project_theseus_whitepaper`, `theseus_operator_os`, `theseus_architecture_gate` | Mine after primary sources for cross-layer connections, variants, runtime packet boundaries, and failure modes. |
| Variants / alternate releases | `moecot_md` | Use only to compare versions or recover missing detail. |
| Connector or recovery required | `moecot` | Load via Google Drive connector or mark as blocked before source-derived claims. |

Draft arc:

- Problem: The architecture needs to allocate cognition across specialists rather than force one system to do every task.
- Insufficiency: Monolithic scaling and static tool lists do not provide local memories, bounded authority, specialist lifecycle, or readiness-aware routing.
- Mechanism: Treat routing as a task-local authority lease over registered specialists with capability, cost, readiness, authority, memory, tool, fallback, residual, and evidence metadata.
- Mechanism: Select the smallest adequate specialist only after capability, authority, readiness, and fallback predicates are explicit.
- Mechanism: emit route receipts that record selected specialist, rejected candidates, granted authority subset, denied authority, context lease, tool lease, readiness state, verifier requirement, budget, fallback, expiry, and residual owner.
- Mechanism: record non-selection evidence so rejected candidates inform readiness, resource policy, and future routing.
- Mechanism: Preserve registry epoch, owner, authority envelope, memory/tool lease policies, route limitations, route receipt, residual owner, and non-claims so selected and rejected specialists remain inspectable after the route expires.
- Mechanism: Fold MoECOT as a runtime crosswalk by mapping compact orchestrator, route head, specialist lanes, control-plane gates, ledgers, replay refs, handoffs, residuals, and promotion blockers onto route receipts and runtime evidence packets.
- Mechanism: Separate source-reported, locally reproduced, externally corroborated, and blocked runtime fields so implementation-reference context cannot become benchmark, replay, or deployment evidence by branding alone.
- Handoff: Failed or uncertain routes flow to readiness gates, residual escrow, fallback routes, or tribunal/review rather than ordinary execution.
- Interface: Planning requests capabilities.
- Interface: Governance bounds specialists.
- Interface: Evidence updates readiness.
- Interface: artifact graphs and evidence ledgers retain route receipts for downstream claim traceability.
- Interface: MoECOT orchestration records extend route receipts with command refs, specialist lanes, control-plane gates, route authority ledgers, replay refs, denied routes, failed gates, missing replay refs, handoff refs, source-state partitions, residuals, and non-claims.

Primary invariants:

- Specialist authority is local.
- Routing decisions are logged.
- Fallback paths remain available.
- The router selects the least-capable adequate specialist unless task risk, context demand, verifier requirement, or fallback policy justifies broader capability.
- Implementation evidence is separated from design argument.
- Runtime promotion follows readiness gates.

Failure modes to cover:

- Wrong specialist selection.
- Router overconfidence.
- Specialist authority leak.
- Route laundering: broad successful routes justify broader authority without proving narrower specialists were inadequate.
- Implementation branding as proof.
- Replay theater that preserves successful paths while omitting failed gates, denied routes, human interventions, missing sources, and residual cases.

Draft deliverables:

- A router registry with capability metadata, cost, authority, leases, route limitations, route receipts, non-selection evidence, expiry, residual ownership, and fallback rules.
- Exact Appendix C claim-source mappings for routing heads and the folded MoECOT runtime crosswalk: local raw-cache, local public-project, and authenticated connector mappings are passage-reviewed or connector-reviewed while runtime artifacts remain unimported.
- Implemented protocol validation: `specialist_registry_record` and `routing_decision_record` fixtures validate public record shape only.
- Implemented protocol validation: `moecot_orchestration_record` fixture validates public runtime-packet record shape only.
- Planned Codex test: Specialist routing accuracy test.
- Implemented synthetic Codex test: `python3 scripts/validate_routing_decision_lease.py` checks routing lease packets for least-capable adequate route selection, overprivileged specialist rejection, selected-route authority-envelope containment, missing-readiness fallback, expired-lease residualization, rejected-candidate evidence, residual ownership, MoECOT source-boundary promotion blockers, and explicit non-claim boundaries. It remains synthetic record-gate evidence only, not learned-router, route-quality, deployed authority-enforcement, specialist-quality, MoECOT replay, or benchmark evidence.
- Planned Codex test: MoECOT source-ingestion gate.
- Planned Codex test: Runtime crosswalk completeness test.
- Implemented Lean predicate: selected routes satisfy authority and readiness.
- Implemented Lean predicate: failed readiness routes to fallback or residual rather than promotion.
- Implemented Lean predicate: finite routing-decision lifecycle routing sends missing capability requests, missing specialist registries, authority mismatches, readiness failures, fallback/residual handling, stale leases, missing cost-quality records, overprivileged selections, missing rejected-candidate evidence, residual-owner gaps, and missing non-claim boundaries to explicit modeled outcomes.
- Implemented Lean predicate: runtime core promotion requires readiness, regression, and replay evidence references.
- Implemented Lean predicate: claims sourced only from unavailable runtime text cannot promote above `argument`.
- Implemented Codex test: Authority-bounded routing test, via `python3 scripts/validate_readiness_residual_gates.py` over route authority ceilings, gate authority scopes, allowed routes, and blocked routes; deployed router enforcement remains unrun.
- Implemented Codex test: Fallback route test, via `python3 scripts/validate_readiness_residual_gates.py` over canary/default and quarantine fallback preservation; live fallback route execution remains unrun.
- Partially implemented Codex test: Readiness/replay mapping review, via `python3 scripts/validate_readiness_residual_gates.py` for readiness mapping across route evidence, gate decisions, residual escrow, fallback, and replacement decisions; MoECOT replay mapping remains planned and unrun.
- Historical public slug preserved by `chapters/moecot-runtime-and-multi-core-orchestration.html`; archived source manuscript retained under `archive/retired_chapters/moecot-runtime-and-multi-core-orchestration.qmd`.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:routing.specialists.operational_invariant` | `AsiStackProofs.Routing` | A router may select only specialists whose authority and readiness satisfy the task requirement. | implemented |
| `lean:routing.specialists.failure_blocks_promotion` | `AsiStackProofs.Routing` | A failed readiness predicate routes to fallback or residual, not promotion. | implemented |
| `lean:routing.specialists.decision_lifecycle_route` | `AsiStackProofs.Routing` | A modeled routing decision routes missing requests, registry gaps, authority mismatches, readiness failures, stale leases, missing cost-quality records, overprivileged selections, missing rejected-candidate evidence, residual ownership gaps, and missing non-claim boundaries to explicit outcomes. | implemented |
| `lean:moecot.runtime.operational_invariant` | `AsiStackProofs.MoECOTRuntime` | A runtime core promotion requires readiness, regression, and replay evidence references. | implemented |
| `lean:moecot.runtime.failure_blocks_promotion` | `AsiStackProofs.MoECOTRuntime` | A runtime claim sourced only from unavailable text cannot be promoted above argument state. | implemented |

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
- Implemented Lean negative case: promoted readiness decisions with failed required gates are rejected.
- Implemented Lean negative case: accepted stronger readiness transitions missing fresh gate evidence, residual escrow, fallback path, or expiry records are rejected.
- Implemented Lean negative case: quarantined targets selected for ordinary routing or selected for diagnostic routing without fallback are rejected.
- Implemented Lean negative case: promoted reuse of expired or architecture-stale gates without rerun and residual records is rejected.
- Implemented Lean lifecycle transition relation: finite readiness transitions over candidate, shadow, canary, qualified, default-ready, quarantined, retired, and superseded states require forward/terminal paths, fresh gate evidence, residual escrow, fallback path, expiry records, regression floors, authority scope, route permissions, supersession records, or retirement receipts as applicable.
- Implemented Codex test: Readiness transition enforcement test, via `python3 scripts/validate_readiness_residual_gates.py` over canary, default, quarantine, and expired-rerun scenarios; deployed readiness-engine behavior remains unrun.
- Implemented Codex test: Residual escrow integrity test, via `python3 scripts/validate_readiness_residual_gates.py` over route residual obligations and inherited residual custody; residual-ledger storage remains unrun.
- Implemented Codex test: Quarantine routing harness test, via `python3 scripts/validate_readiness_residual_gates.py` over blocked selected routes and preserved fallback routes; live quarantine routing remains unrun.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:readiness.gates.operational_invariant` | `AsiStackProofs.ReadinessGates` | A module can enter promoted or stronger readiness states only after required gates and finite lifecycle records for fresh evidence, residual escrow, fallback, expiry, regression floor, authority scope, and route permission are present. | implemented |
| `lean:readiness.gates.failure_blocks_promotion` | `AsiStackProofs.ReadinessGates` | A quarantined, superseded, retired, stale, or incomplete readiness transition cannot be used for ordinary promotion without the required fallback, residual, rerun, supersession, or retirement records. | implemented |

Implemented negative-case theorems now cover failed promoted gates, accepted stronger transitions missing freshness/residual/fallback/expiry records, quarantined ordinary routes or diagnostic routes without fallback, stale-gate reuse without rerun/residual records, default readiness without regression or authority scope, quarantined lifecycle transitions with ordinary routing, supersession without a supersession record, retirement without a receipt, and transition from retired state. These remain record-level gates only; they do not prove benchmark quality, residual-ledger storage, lifecycle engine behavior, live routing enforcement, MoECOT replay, or current readiness.

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
- Implemented Lean route predicate: finite hive-work admission reviews route malformed jobs, missing identity/data/tool policy, registry gaps, scheduler-policy gaps, high-risk jobs without approval, external access without leases or sandbox records, missing cost or energy budgets, missing dropout plans, missing audit receipt plans, missing residual owners, and support-promotion attempts without evidence transitions into explicit outcomes; no scheduler, registry, portal, device, rented-node, or federation behavior is claimed.
- Implemented Codex test: Device registry fixture validation through `validate_protocol_examples.py`.
- Implemented Codex test: Portal, approval, bid, and federation fixture validation through `validate_protocol_examples.py`.
- Implemented Codex test: Policy-first scheduling denial as a finite Lean predicate only.
- Implemented Codex test: Hive work admission lifecycle route as a finite Lean route predicate only.
- Implemented Codex test: Hive admission harness through `python3 scripts/validate_hive_admission.py`, covering 2 valid and 8 expected-invalid synthetic Personal Compute Hive admission fixtures for policy-first scheduling, data locality/rented-node denial, approval receipts, guardian portal routing, federation lease boundaries, job bidding, energy/dropout residuals, audit replay refs, and support-state non-promotion.
- Implemented Codex test: Data locality and rented-node denial as synthetic record validation only; no rented-node sandbox, privacy guarantee, or deployed scheduler claim.
- Implemented Codex test: Phone approval gate as synthetic record validation only; no approval-service, phone-portal, or deployed execution claim.
- Implemented Codex test: Child topic routing as synthetic record validation only; no family-governance engine or child-safety behavior claim.
- Implemented Codex test: External project sandbox contract as synthetic record validation only; no network overlay, federation run, or rented-node sandbox claim.
- Implemented Codex test: Audit replay as audit-ref and residual-presence validation only; no replay service or deployed audit reconstruction claim.
- Planned Codex test: Cross-router connectivity test.
- Implemented Codex test: Job bidding as synthetic bid-selection and policy-blocked rejection validation only; no scheduler-quality or optimality claim.
- Implemented Codex test: Device dropout as dropout/requeue residual-presence validation only; no recovery run or live device dropout claim.
- Implemented Codex test: Energy-aware scheduling as synthetic energy-budget and thermal-risk rejection validation only; no energy measurement or live scheduling claim.
- Planned Codex test: Portal continuity test.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:personal_hives.scheduling.operational_invariant` | `AsiStackProofs.PersonalComputeHives` | A hive scheduler admits a job only when identity, data, tool, federation, and approval policy checks pass before optimization. | implemented |
| `lean:personal_hives.policy_first.failure_blocks_promotion` | `AsiStackProofs.PersonalComputeHives` | A faster node cannot be selected when its policy membrane forbids the job's data, authority, or network scope. | implemented |
| `lean:personal_hives.approval_gate.failure_blocks_promotion` | `AsiStackProofs.PersonalComputeHives` | A high-risk hive job that requires approval cannot execute unless a bound approval receipt is present. | implemented |
| `lean:personal_hives.federation_lease.operational_invariant` | `AsiStackProofs.PersonalComputeHives` | External hive access requires an active lease with scope, sandbox, evidence, expiration, and revocation records. | implemented |
| `lean:personal_hives.work_admission.lifecycle_route` | `AsiStackProofs.PersonalComputeHives` | A structured hive-work admission review routes malformed jobs, missing identity/data/tool policy, registry gaps, scheduler-policy gaps, high-risk jobs without portal approval, external access without leases or sandbox records, missing cost or energy budgets, missing dropout plans, missing audit receipt plans, missing residual owners, and support-promotion attempts without evidence transitions into explicit outcomes. | implemented |

### Compact Generative Systems: Generate, Verify, Repair, and Residual Honesty

Stable ID: `compact-generative-systems-and-residual-honesty`

Chapter job: Compact generators, generate/verify/repair receipts, and semantic representation leases need one claim-accounting surface so useful compression does not hide residual burden, exactness debt, repair cost, semantic grounding loss, hierarchy drift, fallback, or consumer-policy limits.

Core claim: Compact generative systems should store the smallest useful governed generator plus the cheapest exact or scoped residual, while preserving verification, fallback, consumer policy, and residual-burden records.

Folded semantic-representation subclaim: Semantic representations are task-scoped leases: graph nodes and semantic tokens may carry work only when provenance, grounding, utility, interoperability, permitted use, residual uncertainty, and supersession are explicit.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `cgs`, `rgs`, `bbvca_v9`, `bbvca_main`, `treellm` | Read first for compact-system, generate/verify/repair, and semantic-representation claims and mechanisms. |
| Supporting | `bugbrain`, `simulation_scaling`, `rmi`, `project_theseus_whitepaper`, `rankfold_neuralfold`, `spinoza`, `verification_bandwidth`, `cognitive_compilation`, `circle_ai_architectures`, `coilra_multicoil_rope` | Mine after primary sources for edge/resource constraints, ratcheting, implementation lineage, artifact-compression comparison, semantic-IR pressure, proof-carrying claim graphs, optional cyclic substrate guardrails, and failure modes. |

Draft arc:

- Problem: Compact generators and generate/verify/repair receipts need one claim-accounting surface so useful compression does not hide residual burden, exactness debt, repair cost, fallback, or consumer-policy limits.
- Insufficiency: Seed-size, compression-ratio, and generated-reconstruction claims can hide verification, repair, fallback, downstream utility, metadata, interface, governance, and human-review costs.
- Mechanism: Treat compactness as a governed claim over seed, rule system, memory state, generator/decoder/controller, generation status, correction mechanism, verifier, verification status, verifier independence, residual channel, fallback path/status, residual-burden status, governance interface, authority boundary, use envelope, burden ledger, evidence/cost ledger, promotion blockers/state, source refs, support-state effect, and non-claims.
- Mechanism: Use the seed/router/search/generator/verifier/residual loop to expose generation cost, verification cost, correction burden, hidden complexity, and authority limits before promotion.
- Mechanism: Separate reconstruction burden, decision burden, and governance burden so compactness is judged by total recorded cost rather than seed size.
- Mechanism: Require verifier separation and use envelopes so compact cores cannot self-promote their own adequacy for evidence, runtime, or replacement claims.
- Mechanism: Preserve the folded generate/verify/repair lane as a compression receipt with receipt state, reconstruction contract, public law family, seed, search bound, generated regions, verification result, repair residual, fallback threshold, interface costs, consumer policy, use permissions, proxy-rate status, final-serialization status, rate accounting, support-state effect, evidence refs, and non-claims.
- Mechanism: Treat compression as a transaction with candidate, verified-exact, verified-lossy, repaired-exact, literal-fallback, and quarantined states.
- Mechanism: Scope compressed outputs by consumer policy so preview, routing, proof, audit, citation, benchmark, training, and exact-replay uses cannot borrow each other's authority.
- Mechanism: Preserve the folded semantic-representation lane as Semantic Representation Leasing: semantic nodes, graph paths, and semantic tokens carry work only with provenance, grounding state, adequacy, interoperability, permitted use, residual uncertainty, versioning, supersession, consumer policy, and quarantine/fallback behavior.
- Mechanism: Track semantic-node lifecycle states: proposed, grounded, adequate-for-task, interoperable, superseded, stale, and quarantined.
- Handoff: Time-domain acceleration inherits the same accepted-output, repair, fallback, semantic-lease, and verifier-cost accounting in fast-generation records; RankFold/NeuralFold remains the standalone technique-facing artifact-compression chapter.
- Interface: Compression feeds memory and routing.
- Interface: Evidence tests downstream utility, exactness, declared loss, and consumer-policy boundaries.
- Interface: Procedural memory turns repeated generation into tools.
- Interface: Resource economics counts generation, verification, repair, metadata, interface, fallback, and human-review costs before efficiency claims.

Primary invariants:

- Lossy claims are labeled.
- Residual burden is visible.
- Fallback exists when compact generation fails.
- Verification precedes exactness claims.
- Repair cost is counted.
- Search bounds are explicit.
- Consumer use is scoped to the reconstruction contract and declared loss.
- Negative rate results are preserved instead of rewritten as narrative success.
- Semantic nodes are grounded or labeled speculative.
- Hierarchy changes preserve prior references or record supersession.
- Shared semantic graphs remain indexes and working representations, not independent source authorities.
- Consumer use is scoped by grounding, adequacy, interoperability, residual uncertainty, and permitted-use fields.

Failure modes to cover:

- False lossless claims.
- Hidden residual complexity.
- Compactness that damages utility.
- Unbounded search.
- Verification skipped.
- Repair larger than original data.
- Consumer-policy leakage, where a lossy or preview representation is reused for exact, audit, proof, citation, benchmark, or training work.
- Proxy-rate drift, where search-time savings survive in prose after final serialization erases them.
- False explainability.
- Canonical graph capture, where a semantic graph becomes an unreviewed authority source.
- Hierarchy drift and stale consumer mappings.
- Semantic laundering, where a clean path explanation is cited instead of the source, proof, or test it was meant to index.

Draft deliverables:

- A compactness ledger with seed, router/index, search/planning, generator/decoder, verifier/critic, residual correction, memory/governance hooks, authority boundary, use envelope, burden ledger, exact remainder, verification, support-state effect, and residual fields.
- Implemented repository-level fixture: `compact_generative_record.valid.json` validates the compact-generative record shape, generation status, verification status, fallback status, residual-burden status, correction mechanism, verifier independence, authority boundary, use envelope, burden ledger, cost accounting, promotion blockers/state, source refs, support-state effect, and non-claims only; utility and residual-burden behavior remain planned tests.
- Implemented repository-level fixture: `compression_receipt.valid.json` validates receipt state, search bound, interface costs, consumer policy, use permissions, proxy-rate status, final-serialization status, rate accounting, support-state effect, evidence refs, and non-claims only; no codec, reconstruction benchmark, or rate experiment exists yet.
- Implemented repository-level fixture: `semantic_node_record.valid.json` validates provenance, hierarchy, relations, tokenization contract, grounding state, versioning, residual uncertainty, permitted uses, evaluation refs, support-state effect, and non-claims only; no TreeLLM implementation, grounding benchmark, representation-utility test, or hierarchy-revision harness exists yet.
- Implemented bounded evidence slice: `python3 scripts/validate_compact_gvr_slice.py` recomputes a public-safe synthetic GVR receipt lane with a 368-byte literal baseline, a 78-byte exact compact generator-plus-repair receipt, lossy exactness, negative-rate/no-fallback, and bounded-search-overrun controls, residuals, non-claims, accepted non-core transition record, and Lean fixture bridge. This supports only `compact-generative-systems.compact_gvr_receipt_slice`; the chapter core claim remains `argument`.
- Planned Codex test: S/R/Q/G/V/E loop consistency test.
- Implemented Lean predicate: unresolved obligations require residual records.
- Implemented Lean predicate: lossy representations cannot be marked exact without verification evidence.
- Implemented Lean route: modeled compact-generation admission reviews route missing source artifacts, compression boundaries, residual records, lossy exactness overclaims, reconstruction evidence, fallback paths, verifier-cost records, semantic provenance, hierarchy-migration records, evidence-transition gaps, and non-claim-boundary gaps to explicit outcomes.
- Implemented Lean bridge: compact GVR synthetic fixture matches the selected compact receipt, rejected controls, and selected-versus-baseline byte relation.
- Implemented Lean predicate: exact reconstruction claims require generator output plus repair residual to equal the target in a finite record.
- Implemented Lean predicate: failed verification blocks exactness promotion.
- Planned Codex test: Residual burden behavior test.
- Planned Codex test: Downstream utility test.
- Planned Codex test: Fallback behavior test.
- Planned Codex test: Reconstruction quality test.
- Planned Codex test: Repair-cost accounting test.
- Planned Codex test: Bounded-search failure test.
- Planned Codex test: Consumer-policy enforcement test.
- Planned Codex test: Grounding fidelity test.
- Planned Codex test: Hierarchy revision test.
- Planned Codex test: Representation utility benchmark.
- Planned Codex test: Semantic consumer-policy test.
- Historical public slug preserved by `chapters/generate-verify-repair-compression.html`; archived source manuscript retained under `archive/retired_chapters/generate-verify-repair-compression.qmd`.
- Historical public slug preserved by `chapters/semantic-representation-and-tree-structured-models.html`; archived source manuscript retained under `archive/retired_chapters/semantic-representation-and-tree-structured-models.qmd`.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:compression.cgs.operational_invariant` | `AsiStackProofs.CompactGenerativeSystems` | A compact representation with unresolved obligations carries residual records. | implemented |
| `lean:compression.cgs.failure_blocks_promotion` | `AsiStackProofs.CompactGenerativeSystems` | A lossy representation cannot be marked exact without verification evidence. | implemented |
| `lean:compression.cgs.admission_route` | `AsiStackProofs.CompactGenerativeSystems` | A modeled compact-generation admission review routes missing source artifacts, compression boundaries, residual records, lossy exactness overclaims, reconstruction evidence, fallback paths, verifier-cost records, semantic provenance, hierarchy-migration records, evidence-transition gaps, and non-claim-boundary gaps to explicit outcomes. | implemented |
| `lean:compression.cgs.gvr_fixture_bridge` | `AsiStackProofs.CompactGenerativeSystems` | The compact GVR synthetic slice has a finite Lean fixture bridge matching the literal baseline, selected compact receipt, lossy exactness control, negative-rate/no-fallback control, bounded-search-overrun control, and selected-versus-baseline byte relation. | implemented |
| `lean:compression.gvr.operational_invariant` | `AsiStackProofs.GenerateVerifyRepair` | An exact reconstruction claim requires generator output plus repair residual to equal the target. | implemented |
| `lean:compression.gvr.failure_blocks_promotion` | `AsiStackProofs.GenerateVerifyRepair` | A failed verification blocks exactness promotion. | implemented |
| `lean:representation.semantic_tree.operational_invariant` | `AsiStackProofs.SemanticRepresentation` | A semantic node marked grounded has at least one provenance link. | implemented |
| `lean:representation.semantic_tree.failure_blocks_promotion` | `AsiStackProofs.SemanticRepresentation` | A hierarchy update preserves prior node references or records supersession. | implemented |

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
- Implemented Lean proof target: finite generation-mode admission lifecycle routing sends missing mode records, context packets, risk tiers, quality targets, verifiers, acceptance predicates, baselines, accepted outputs, verifier costs, fallback and residual handling gaps, high-risk override gaps, budget gaps, evidence-transition gaps, and non-claim-boundary gaps to explicit modeled outcomes.
- Implemented Lean/Python bridge: `python3 scripts/validate_theseus_generation_mode_import.py` now checks that the public Project Theseus generation-mode import fixture matches `AsiStackProofs.FastGeneration.theseusGenerationModeImportFixture` for mode count, comparison count, hard gaps, zero missing report refs, boundary gates, accepted-span speed-lift warnings, zero useful-solution evidence, zero promotable comparisons, and public-safety/support-state/raw-speed overclaim boundaries; it rejects hard boundary-gate failure and missing-report-ref overclaim controls.
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
| `lean:fast_generation.mode_admission_lifecycle_route` | `AsiStackProofs.FastGeneration` | A modeled fast-generation admission review routes missing mode records, context packets, risk tiers, quality targets, verifiers, acceptance predicates, baselines, accepted outputs, verifier costs, fallback and residual handling, high-risk override gaps, budget gaps, evidence-transition gaps, and non-claim-boundary gaps to explicit outcomes. | implemented |
| `lean:fast_generation.theseus_import_fixture_bridge` | `AsiStackProofs.FastGeneration` | The public Project Theseus generation-mode import fixture matches a finite Lean summary fixture and proves the imported accepted-span speed-lift warnings do not permit promotion without useful-solution evidence, promotable comparisons, all hard boundary gates passing, and zero missing report refs. | implemented |

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
- Implemented Lean predicate: finite artifact-compression admission lifecycle routing sends missing preserved full artifacts, missing manifests, use-envelope and access-pattern gaps, unadmitted states, decoder-determinism gaps, exact-replay readiness failures, failed probes, missing fallback artifacts, residual metadata gaps, utility-evidence gaps, support-promotion gaps, and missing non-claim boundaries to explicit modeled outcomes.
- Planned Codex test: Compression ratio test.
- Planned Codex test: Probe-route fallback test.
- Planned Codex test: Downstream utility preservation test.
- Planned Codex test: Access-pattern admission test.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:compression.artifacts.operational_invariant` | `AsiStackProofs.ArtifactCompression` | A compressed artifact used for a task must pass that task probe or route to fallback. | implemented |
| `lean:compression.artifacts.failure_blocks_promotion` | `AsiStackProofs.ArtifactCompression` | A compression record cannot omit residual or fallback metadata. | implemented |
| `lean:compression.artifacts.admission_lifecycle_route` | `AsiStackProofs.ArtifactCompression` | A modeled compressed-artifact admission review routes missing preserved full artifacts, missing manifests, use-envelope and access-pattern gaps, unadmitted states, decoder-determinism gaps, exact-replay readiness failures, failed probes, missing fallback artifacts, residual metadata gaps, utility-evidence gaps, support-promotion gaps, and missing non-claim boundaries to explicit outcomes. | implemented |

### Resource Economics and Token Budgets

Stable ID: `resource-economics-and-token-budgets`

Chapter job: Compute, context, verification, simulation fidelity, and human attention are scarce resources that the architecture must allocate explicitly.

Core claim: Resource governance accounts for token budgets, verification tax, load stability, and risk-adjusted inference value.

Folded simulation-fidelity subclaim: simulation and synthetic-environment results are resource-governed claim-transport records whose support cannot exceed declared scope, fidelity, temporal semantics, resource bill, assumptions, omitted variables, instrumentation effects, residual risks, and transfer decision.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `tokenmana`, `planforge` | Read first for budget, scheduler, and scarcity framing. |
| Supporting | `coherence_exchange`, `simulation_scaling`, `viea`, `project_theseus_whitepaper`, `coilra_multicoil_rope`, `cgs`, `rankfold_neuralfold`, `alignment_field` | Mine after primary sources for cross-layer budget pressure, simulation fidelity, hidden residual burden, execution/report discipline, normative boundaries, and failure modes. |
| External literature variants | `ext_pagedattention_vllm_2023`, `ext_reluplex_2017` | Read for serving-memory economics and scoped property-verification comparison; treat reported results as source-reported until reproduced. |

Draft arc:

- Problem: Compute, context, verification, simulation fidelity, and human attention are scarce resources that the architecture must allocate explicitly.
- Insufficiency: Ignoring resource economics or fidelity boundaries makes high-quality verification unaffordable, encourages synchronized overload or hidden cost shifts, and lets synthetic results travel farther than their contracts support.
- Mechanism: Track task value, uncertainty, cost of error, inference cost, verification tax, protected overhead, and displaced costs.
- Mechanism: Use regenerative or budgeted capacity mechanisms where useful.
- Mechanism: Escalate verification when risk justifies the cost.
- Mechanism: Separate aggregate serving throughput and memory pressure from single-request verified-output value.
- Mechanism: Attach Simulation Contract Records when simulated, synthetic, benchmark, or scenario results are used as evidence.
- Mechanism: Block, downgrade, or residualize claims whose simulation scope, fidelity, temporal semantics, resource bill, bottlenecks, omissions, or transfer decision do not support the stronger claim.
- Handoff: Mathematical, cyclic, and search substrates enter only through resource, fidelity, baseline, and evidence contracts rather than elegance or apparent cheapness.
- Interface: Planning allocates budgets.
- Interface: Routing chooses costed specialists.
- Interface: Evidence measures cost-quality tradeoffs.
- Interface: Serving infrastructure reports memory and throughput costs without converting them into quality claims.
- Interface: Simulation records declare fidelity, resource bills, omitted variables, instrumentation effects, transfer decisions, and non-claims before synthetic results enter claim ledgers.

Primary invariants:

- Budgets do not override protected safety gates.
- High-risk tasks pay verification cost.
- Cost savings are recorded with quality results.
- Serving-throughput gains remain separate from verified-output and task-success claims.
- Protected overhead is budgeted explicitly and cannot be silently deleted.
- Displaced costs remain residuals until measured or accepted by a scoped evidence transition.
- Simulation fidelity, scope, and resource bounds are declared before synthetic results support a claim.
- Simulation results do not transfer beyond their supported claim boundary by default.
- Approximation liberties, omitted variables, and instrumentation effects remain visible after results are summarized.

Failure modes to cover:

- Cost-cutting verification away.
- Load-synchronized degradation.
- Resource hoarding by low-value tasks.
- Aggregate serving throughput mistaken for lower single-request risk or better answer quality.
- Protected-overhead deletion.
- Review-capacity capture.
- Simulation laundering: clean synthetic results described as if omitted variables, bottlenecks, and transfer limits were irrelevant.
- Sandbox-to-world transfer without a declared fidelity and resource contract.
- Parent-physics assumption drift without updating the simulation contract.

Draft deliverables:

- A resource ledger with budget, risk, cost, quality, verification tax, protected-overhead, displaced-cost, and evidence-reference fields, plus a companion Simulation Contract Record for synthetic or simulated results with scope, fidelity, temporal semantics, resource bill, bottlenecks, omissions, instrumentation effects, transfer decision, support-state effect, residual risks, and non-claims.
- Codex test: Generation-mode resource-budget alignment harness - Check that deterministic generation-mode scenarios carry matching resource-budget records with task/risk alignment, verification tax, protected overhead, safety gates, residuals, evidence refs, and no-promotion boundaries (implemented; passing via `python3 scripts/validate_generation_mode_baselines.py`).
- Codex test: Resource budget ledger harness - Check deterministic Resource Budget Record decisions for dispatch, escalation, protected overhead, displaced-cost residualization, review-capacity hoarding, KV-cache/serving-memory accounting separation, throughput-to-quality overclaim rejection, evidence refs, and no-promotion boundaries (implemented; passing via `python3 scripts/validate_resource_budget_ledgers.py`).
- Codex test: Costed-route Lean fixture alignment gate - Check that the finite Resource Economics Lean fixture matches the public costed-route JSON route costs, selected route, negative controls, eligibility fields, selector-trace expectation, and tracked result-record field alignment used by the measured/replayed slice (implemented; passing via `python3 scripts/validate_costed_route_resource_slice.py`; no deployed scheduler, route-search completeness, or economic-optimality claim).
- Codex test: Resource workflow trace harness - Check deterministic multi-step workflow fixtures for selected-route cost recomputation, high-risk-first scheduler ordering, protected review overhead, displaced-cost residual ownership, capacity-budget-overrun rejection, physical-feasibility overclaim rejection, no-promotion boundaries, and tracked result-record trace-property alignment with finite Lean dispatch events (implemented; passing via `python3 scripts/validate_resource_workflow_trace.py`; no deployed scheduler, physical-feasibility, model-quality, or economic-outcome claim).
- Codex test: Resource live probe - Replay the local Resource Economics validator stack, record command-output digests and tracked artifact hashes, and preserve a no-transition boundary for the flagship evidence lane (implemented; passing via `python3 scripts/validate_resource_live_probe.py`; local repository command replay only; no deployed scheduler, physical-feasibility, model-quality, economic-outcome, or support-state-transition claim).
- Codex test: Resource workload-quality probe - Measure a scoped Resource workflow trace review route across five local samples against a broader Resource Economics replay baseline, reject a cheaper no-op success-text route, record residuals and non-claims, and preserve the no-transition boundary (implemented; passing via `python3 scripts/validate_resource_workload_quality_probe.py`; local five-sample median repository task only; no stable-speedup, deployed-scheduler, model-quality, economic-outcome, external-review, or support-state-transition claim).
- Codex test: Resource load-stability probe - Run a finite local synthetic burst-review workload across admit-arrivals, protected capacity-smoothing, and review-erasure routes; check overload reduction, residualized deferrals, protected-review preservation, Lean fixture alignment, and no-promotion boundaries (implemented; passing via `python3 scripts/validate_resource_load_stability_probe.py`; local synthetic workload only; no TokenMana, deployed-scheduler, production-queue, real-load-stability, human-productivity, model-quality, economic-outcome, external-review, or support-state-transition claim).
- Codex test: Resource flagship lane replay - Run the Resource Economics flagship evidence lane as one command across costed-route, workflow-trace, budget-ledger, capacity-smoothing, live-probe, workload-quality, load-stability, CI-cost, simulation-transfer, and evidence-transition validators while preserving non-core and chapter-core boundaries (implemented; passing via `python3 scripts/validate_resource_flagship_lane.py`; aggregate local repository replay only; no Resource Economics chapter-core promotion, deployed scheduler, production workload, model-quality, economic-outcome, external-review, artifact-approval, or new support-state-transition claim).
- Planned Codex test: Budget allocation test
- Planned Codex test: Risk-adjusted verification test
- Codex test: Capacity smoothing toy harness - Check deterministic toy capacity traces for bounded regeneration arithmetic, priority deferral under blocked high-risk work, scope reduction, reviewer-capacity arithmetic, protected-review overhead, displaced-review-cost residualization, overload rejection, Lean bridge coverage, and no-promotion boundaries (implemented; passing via `python3 scripts/validate_capacity_smoothing.py`; 3 valid and 6 expected-invalid fixtures; no TokenMana, scheduler, load-stability, reviewer-optimization, or economic-result claim).
- Codex test: KV-cache memory accounting scenario - Check that serving-memory, batching, aggregate throughput, single-request verified-output boundaries, and model-quality non-claims remain separate in deterministic Resource Budget Records (implemented; passing via `python3 scripts/validate_resource_budget_ledgers.py`; 6 valid and 7 expected-invalid fixtures; no KV-cache behavior, serving-throughput, single-request quality, or model-quality claim).
- Implemented repository-level fixture: Simulation contract record fixture validation - Validate that simulation claims record contract version, claim class, scope, fidelity state, temporal semantics, assumptions, demand, resource bill, bottlenecks, omissions, approximation liberties, instrumentation effects, supported and observed-result boundaries, transfer decision, support-state effect, failure behavior, residual risks, evidence references, and non-claims (implemented; passing via `python3 scripts/validate_protocol_examples.py`).
- Implemented book-gate harness: `python3 scripts/validate_simulation_transfer_boundaries.py` validates 3 valid and 6 expected-invalid simulation-transfer fixtures for fidelity declaration, resource bills, capacity bottlenecks, omitted variables, approximation liberties, instrumentation effects, transfer decisions, residual/downgrade behavior, unbounded world-transfer rejection, and support-state non-promotion; this is not a simulator run, physical-feasibility result, open-world-transfer result, scheduler result, or economic result.
- Implemented Codex test: Fidelity declaration test, via `python3 scripts/validate_simulation_transfer_boundaries.py`; no simulator-adequacy or physical-feasibility claim.
- Implemented Codex test: Resource-bound simulation sanity check, via `python3 scripts/validate_simulation_transfer_boundaries.py`; deterministic fixture discipline only.
- Implemented Codex test: Simulation approximation audit, via `python3 scripts/validate_simulation_transfer_boundaries.py`; no benchmark-reproduction, physical-feasibility, open-world-transfer, or support-state claim.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:resources.budgets.operational_invariant` | `AsiStackProofs.ResourceEconomics` | A task budget cannot disable required safety or verification gates. | implemented |
| `lean:resources.budgets.failure_blocks_promotion` | `AsiStackProofs.ResourceEconomics` | A high-risk task with insufficient verification budget is blocked or escalated. | implemented |
| `lean:resources.costed_route.fixture_bridge` | `AsiStackProofs.ResourceEconomics` | The four-route costed-route fixture rejects the failed-verification and hidden-residual controls, keeps the bounded transform route eligible, proves it is lowest-cost among eligible modeled routes, and proves a finite selector-state replay ends with that route after rejecting the cheaper controls. | implemented |
| `lean:resources.workflow_trace.trace_property_bridge` | `AsiStackProofs.ResourceEconomics` | The finite Resource workflow trace fixture carries dispatch events whose costs, review minutes, and verification minutes roll up to the public summary, whose schedule keeps high-risk release work before lower-risk work, whose selected events preserve protected-overhead, residual-ownership, and non-claim guard flags, and whose public negative controls reject over-budget aggregate resource bills. | implemented |
| `lean:resources.capacity_smoothing.reviewer_trace_bridge` | `AsiStackProofs.ResourceEconomics` | The finite capacity-smoothing reviewer trace fixture preserves bounded capacity, reviewer capacity, protected review overhead, displaced-review-cost residualization, no low-risk review during blocked protected review, and no support-state promotion; negative cases reject low-risk review hoarding, high-risk review without protected overhead, and missing displaced-cost residuals. | implemented |
| `lean:resources.serving_memory.separation_guard` | `AsiStackProofs.ResourceEconomics` | Aggregate serving-throughput or KV-cache reuse claims remain valid only when KV-cache budget, batching scope, and single-request verified-output boundaries are recorded; throughput-to-quality overclaims reject validity. | implemented |
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
- Implemented repository-level fixture: `substrate_adoption_record.valid.json` validates substrate-adoption record shape, baseline obligations, consumer gate/policy, axis ledger, routing-permission effect, fallback substrate, retirement/supersession path, support-state effect, and non-claims only; no A/B run, representation-efficiency benchmark, CoilMoECOT benchmark, or Circle substrate-adoption build exists yet. The separate external rope receipt slice does not validate substrate adoption.
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
- Implemented repository-level fixture: `proof_contract_receipt_record.valid.json` validates proof-contract receipt record shape, receipt state, proof boundary, fingerprint status, consumer state, staleness policy, source refs, support-state effect, and non-claims only; it does not validate a vendored Circle contract pack, ASI Stack consumer gate, or chapter-core proof-contract transport claim.
- Implemented repository-level fixture: `proof_target_record.valid.json` validates proof-record fields only; no Circle theorem-id resolver, fingerprint check, or vendored contract pack exists yet.
- Implemented external receipt slice: `docs/circle_external_receipt_slice.md`, `experiments/circle_external_receipt_slice/results/2026-06-29-local.json`, and `evidence_transitions/v1_0_measured/circle_external_rope_receipt_prototype_backed.json` record one bounded local Circle rope-position receipt replay for `circle-calculus.external_rope_receipt_replay` only; it does not promote `circle-calculus-and-proof-carrying-ai-contracts.core`.
- Implemented concrete evidence surface: `python3 scripts/validate_circle_concrete_evidence_surface.py` checks that the chapter and outline surface Circle commit `63b0f511`, `CC-AI-CONTRACT-ROPE-001`, requested margin `1/328459`, certifier `theorem_count 55`, ready digest `fields=31 missing=0 theorems=75`, seven required theorem IDs, fingerprints, the ASI consumer gate, and non-claims; it does not promote chapter-core support.
- Implemented Lean predicates: `AsiStackProofs.ProofCarryingContracts` proves local finite-record receipt-boundary, consumer-gate promotion, missing-boundary, missing-contract-readiness, stale/unsupported-consumer, and replay-artifact requirements without claiming deployed Circle theorem transport.
- Implemented Codex test: Proof target record fixture validation
- Implemented Codex test: Proof contract receipt record fixture validation
- Implemented Codex test: Circle public consumer-gate validation
- Implemented Codex test: Circle concrete receipt evidence-surface validation
- Implemented Codex test: Receipt boundary Lean predicate
- Implemented Codex test: Consumer gate promotion predicate
- Implemented Codex test: Missing receipt-boundary negative case
- Implemented Codex test: Contract-readiness promotion negative case
- Implemented Codex test: Stale or unsupported consumer-gate negative case
- Implemented Codex test: Replay artifact negative case
- Planned Codex test: Contract schema validation test
- Planned Codex test: Theorem-id resolution test
- Planned Codex test: Non-claim preservation test
- Planned Codex test: Receipt replay and fingerprint test

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:circle_contracts.receipt_requires_boundary.operational_invariant` | `AsiStackProofs.ProofCarryingContracts` | A proof-carrying AI contract exposes theorem references, deterministic fields, and an explicit non-claim boundary before downstream use. | implemented |
| `lean:circle_contracts.consumer_gate.failure_blocks_promotion` | `AsiStackProofs.ProofCarryingContracts` | A downstream claim cannot be promoted solely from contract readiness without a workload, baseline, metric, and evidence artifact. | implemented |

Implemented negative-case theorems now reject downstream-ready receipts missing theorem refs, deterministic fields, or non-claim boundaries; promoted downstream claims without contract readiness; consumer-gate acceptance with unresolved refs, fingerprint mismatch, stale contract state, disallowed consumer state, unsupported transfer claims, or missing non-claims; and passing replay status without replay command, source digest, receipt fingerprint, recomputed deterministic fields, or theorem refs. These remain record-level gates only; they do not resolve external theorem IDs, replay Circle receipts from source, vendor Circle packs, approve transfer, promote support state, or evaluate downstream model behavior.

### Coil Attention, Cyclic Memory, and Recurrence Contracts

Stable ID: `coil-attention-cyclic-memory-and-recurrence-contracts`

Chapter job: Memory, attention, and recurrence mechanisms need finite structural contracts for aliasing, coverage, freshness, active work, loop exits, and overthinking boundaries.

Core claim: Coil attention and memory contracts should be used as structural guardrails for cyclic memory, sparse coverage, recurrence schedules, and work-budget admission, not as claims of retrieval or reasoning quality.

Source loading queue:

| Role | Source IDs | Loading instruction |
|---|---|---|
| Primary | `coil_attention_memory`, `circle_ai_contract_suite` | Read first for chapter claims and mechanisms. |
| Supporting | `theseus_circle_transfer`, `vcm_public`, `verification_bandwidth` | Mine after primary sources for cross-layer connections, variants, and failure modes. |
| External literature variants | `ext_transformer_xl_2019`, `ext_compressive_transformer_2019`, `ext_retnet_2023` | Use as recurrence, compressed-memory, long-range sequence, and attention/recurrence comparators; treat reported results as source-reported until reproduced. |

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
- Implemented repository-level fixture: `cyclic_memory_contract.valid.json` validates the cyclic-memory record shape, memory-authority scope, VCM packet refs, state-carry boundary, stale-read policy, admission state, baseline refs, probe requirements, authority non-widening, residuals, and non-claims only.
- Implemented book-gate harness: `python3 scripts/validate_cyclic_memory_contracts.py` validates 3 valid and 6 expected-invalid synthetic cyclic-memory contract traces for alias visibility, sparse-coverage fallback, recurrence budget/exit, stale-read residualization, structural-quality non-promotion, and support-state non-promotion; this is not a KV-cache certifier, recurrence benchmark, learned-memory workload, retrieval-quality test, or long-context result.
- Source-noted external positioning through Transformer-XL, Compressive Transformers, and RetNet; no retrieval-quality, reasoning-quality, speed, memory-savings, or long-context result is reproduced or promoted.
- Implemented Codex test: Cyclic alias visibility test, via `python3 scripts/validate_cyclic_memory_contracts.py`; no retrieval-quality or learned-memory claim.
- Implemented Codex test: Sparse coverage gap test, via `python3 scripts/validate_cyclic_memory_contracts.py`; no sparse-attention quality or runtime behavior claim.
- Implemented Codex test: Recurrence budget and exit test, via `python3 scripts/validate_cyclic_memory_contracts.py`; no recurrence-quality or model-behavior claim.
- Implemented Codex test: Freshness stale-read rejection test, via `python3 scripts/validate_cyclic_memory_contracts.py`; no KV-cache freshness or retrieval-quality claim.

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
| External literature variants | `ext_roformer_rope_2021`, `ext_lora_2021`, `ext_mamba_2023`, `ext_retnet_2023` | Use as RoPE, low-rank adapter, state-space, and recurrence/attention comparators; treat reported results as source-reported until reproduced. |

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
- Source-noted external positioning through RoFormer/RoPE, LoRA, Mamba, and RetNet; no baseline matrix, quality, context-length, runtime, memory, training-stability, hardware-efficiency, or deployment result is reproduced or promoted.
- Implemented concrete RoPE boundary surface: `python3 scripts/validate_circle_concrete_evidence_surface.py` checks that the recorded Circle RoPE receipt facts, including `evidence.exact_discrete_pass=true` and `evidence.total_bank_collision_pair_count=0`, are surfaced only as diagnostic structural evidence and do not promote chapter-core support, model quality, context length, speed, memory, hardware efficiency, deployment readiness, transfer, or ASI.
- Planned Codex test: RoPE receipt boundary test
- Implemented Codex test: Circle concrete RoPE boundary evidence-surface validation
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
- Implemented Lean predicates: `AsiStackProofs.ProofEnvelope` proves local finite-record implemented-target, non-operational routing, proof-lane authority, support-promotion boundary, and external-theorem reference requirements without claiming broad system proof, semantic adequacy, source correctness, external theorem ownership, model quality, or benchmark evidence.
- Implemented generated audit: Appendix E summarizes all 147 proof targets by status, triage class, and recommended route from `proofs/proof_triage.json`.
- Implemented generated audit: `docs/proof_artifact_audit.md` checks that all 147 proof targets are traceable through manifest, triage, Lean module, root import, chapter hook, limitation prose, and Appendix E coverage; this is not a semantic adequacy review.
- Implemented Codex test: Proof manifest sync test.
- Implemented Codex test: Lake build smoke test.
- Implemented Codex test: Implemented-target missing artifact/build negative case.
- Implemented Codex test: Non-Lean artifact proof-laundering negative case.
- Implemented Codex test: Support-promotion boundary negative case.
- Implemented Codex test: External theorem reference boundary negative case.
- Implemented Codex test: Proof artifact traceability audit.
- Planned Codex test: Semantic proof adequacy audit.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:proofs.envelope.operational_invariant` | `AsiStackProofs.ProofEnvelope` | A proof target marked implemented has an existing module and passes the build. | implemented |
| `lean:proofs.envelope.failure_blocks_promotion` | `AsiStackProofs.ProofEnvelope` | A proof target for a non-operational claim remains planned or blocked, not implemented. | implemented |

Additional implemented theorem boundaries in `AsiStackProofs.ProofEnvelope`
reject implemented targets missing module/build records, non-Lean artifacts
presented as Lean proofs, support promotion without accepted transition,
semantic adequacy, limitations, non-claims, and consumer-requirement records,
and external-theorem references without artifact refs, resolved theorem IDs, or
non-claim boundaries. These remain proof-envelope discipline only; they do not
validate external theorem content, judge semantic adequacy, inspect the
filesystem, or promote any chapter core claim.

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
- Implemented Codex test: Saturation detection test, via `python3 scripts/validate_benchmark_antigoodhart.py` over saturated-benchmark regression-floor and invalid saturated-promotion scenarios; no empirical benchmark run exists.
- Implemented Codex test: Hidden benchmark transfer test, via `python3 scripts/validate_benchmark_antigoodhart.py` over holdout, contamination, and mutation/transfer gates; no hidden benchmark or transfer run exists.
- Planned Codex test: Contamination audit test.
- Planned Codex test: Floor/frontier split test.
- Planned Codex test: Source-reported boundary test.
- Implemented Codex test: Regression preservation test, via `python3 scripts/validate_benchmark_antigoodhart.py` over regression refs and negative-result retention; no empirical regression suite exists.

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
- Implemented Codex test: Reward-source admissibility test, via `python3 scripts/validate_benchmark_antigoodhart.py` over admissible feedback, run measurement status, governance gates, evidence packet refs, and promotion-ready ratchets; no policy optimization run exists.
- Implemented Codex test: Reward hacking probe test, via `python3 scripts/validate_benchmark_antigoodhart.py` over required reward-hacking probes and reward-as-truth rejection; no reward-hacking experiment exists.
- Implemented Codex test: Policy-promotion route negative case, via `AsiStackProofs.PolicyOptimization.PolicyUpdatePromotionRouteFor` route theorems over inadmissible feedback, missing target evaluation, missing holdout or contamination checks, missing reward-hacking probes, governance or authority gaps, missing rollback, and regression/residual gaps; no optimizer, reward-quality, policy-improvement, or deployment behavior claim exists.
- Planned Codex test: Router policy toy RL test.
- Planned Codex test: Context-policy grounding reward test.
- Planned Codex test: Reasoning-budget penalty test.
- Implemented Codex test: Rollback and promotion gate test, via `python3 scripts/validate_benchmark_antigoodhart.py` over blocked, quarantined, rerun, and regression-only ratchet evidence blocking policy promotion; no live rollback or policy canary exists.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:policy_optimization.update.operational_invariant` | `AsiStackProofs.PolicyOptimization` | An admitted policy update records target layer, reward signal, update constraint, evaluation refs, governance gates, and rollback plan. | implemented |
| `lean:policy_optimization.reward_boundary.failure_blocks_promotion` | `AsiStackProofs.PolicyOptimization` | A policy update with unverified reward or missing governance gate cannot be promoted. | implemented |
| `lean:policy_optimization.promotion_route.failure_routes` | `AsiStackProofs.PolicyOptimization` | A policy-promotion route rejects or routes updates with inadmissible feedback, missing target evaluation, missing holdout or contamination checks, missing reward-hacking probes, governance or authority gaps, missing rollback, or regression/residual gaps before promotion. | implemented |

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
- Implemented Lean lifecycle-route envelope: tainted unreviewed events route to quarantine, sunset criteria without an open review route to sunset review, autonomy escalation without charter approval routes to approval, and treasury spend outside policy routes to approval.
- Implemented Lean contribution-ledger route envelope: missing separated authorship/review/evidence/compensation/reputation/governance/conflict records route to ledger repair, collapsed governance scoring is rejected, support-state changes without evidence-transition records request evidence review, and complete separated non-promoting ledgers can be accepted.
- Implemented Lean federation-contract route envelope: missing scoped work contracts request contract repair, federated workers cannot inherit project authority, external spend without approval routes to approval, and complete scoped federation contracts dispatch only with an evidence-bundle requirement.
- Implemented Codex test: Project steward manifest fixture validation through `validate_protocol_examples.py`.
- Implemented Codex test: Treasury policy and event-taint fixture validation through `validate_protocol_examples.py`.
- Implemented Codex test: Work contract authority denial as a finite Lean predicate only.
- Implemented Codex test: Treasury spend-cap/protected-action denial as a finite Lean predicate only.
- Implemented Codex test: Untrusted event taint as a finite Lean lifecycle-route predicate only; no workflow scan or steward event-intake run exists.
- Implemented Codex test: Contribution ledger separation as finite Lean contribution-ledger route predicates only; no contributor-ledger service exists.
- Implemented Codex test: Sunset criteria as finite Lean sunset and lifecycle-route predicates only; no steward loop exists.
- Implemented Codex test: Release evidence handoff test, via `python3 scripts/validate_benchmark_antigoodhart.py` over steward release actions requiring ratchet refs, policy refs, and approval refs; no steward agent or release runner exists.
- Implemented Codex test: Project federation contract as finite Lean federation-contract route predicates only; no project federation harness exists.
- Implemented Codex test: Autonomy-mode transition as finite Lean lifecycle-route predicates only; no steward autonomy transition runner or treasury executor exists.

Lean proof targets:

| Tag | Lean module | Formal target | Status |
|---|---|---|---|
| `lean:artifact_stewards.work_contract.operational_invariant` | `AsiStackProofs.ArtifactStewardAgents` | A steward-managed work contract records objective, authority, allowed tools, forbidden tools, verification requirements, budget, and non-claims before dispatch. | implemented |
| `lean:artifact_stewards.treasury_boundary.failure_blocks_promotion` | `AsiStackProofs.ArtifactStewardAgents` | A steward action that exceeds treasury policy, changes governance rules, or touches protected assets cannot execute without explicit approval evidence. | implemented |
| `lean:artifact_stewards.release_gate.operational_invariant` | `AsiStackProofs.ArtifactStewardAgents` | A stewarded release publication requires test, evidence, changelog, residual, and approval records. | implemented |
| `lean:artifact_stewards.sunset_review.failure_blocks_promotion` | `AsiStackProofs.ArtifactStewardAgents` | When sunset criteria are met, ordinary work generation is blocked until a sunset review is opened. | implemented |
| `lean:artifact_stewards.lifecycle_route.failure_blocks_promotion` | `AsiStackProofs.ArtifactStewardAgents` | A steward lifecycle route sends tainted unreviewed events to quarantine, sunset criteria without review to sunset review, autonomy escalation without charter approval to approval, and over-policy treasury spend to approval. | implemented |
| `lean:artifact_stewards.contribution_ledger.operational_invariant` | `AsiStackProofs.ArtifactStewardAgents` | A steward contribution ledger keeps authorship, review, evidence, compensation, reputation, governance effect, and conflicts separated; collapsed governance scoring is rejected and support-state changes require evidence-transition records. | implemented |
| `lean:artifact_stewards.federation_contract.operational_invariant` | `AsiStackProofs.ArtifactStewardAgents` | A steward federation contract requires scoped work contracts, bounded worker authority, tool/data/budget gates, external-spend approval, and evidence-bundle requirements before dispatch. | implemented |

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

- A reference flow diagram, interface table, and fixture-backed end-to-end trace example with `reference-trace-fixture-approved-001` and `reference-trace-blocked-authority-001` marked as deterministic record-level examples only.
- Implemented repository-level fixture: `reference_trace_record.valid.json` validates reference-trace record shape, trace state, execution boundary, parent artifacts, authority/evidence/residual deltas, promotion blockers, source refs, support-state effect, and non-claims only.
- Implemented Lean trace-route envelope: missing parent artifacts route to parentage repair, missing authority deltas route to authority-delta repair, missing residual deltas route to residual preservation, missing required governance gates block the trace, and missing validation commands require validation.
- Implemented deterministic reference trace harness: `python3 scripts/validate_reference_trace.py` checks 2 valid and 6 expected-invalid reference-trace fixtures for parent artifact continuity, authority-chain and authority-delta visibility, layer coverage from intent through SCF, artifact count, evidence and residual deltas, validation command refs, source-note refs, blocked-path stop conditions, promotion blockers, non-promoting support effects, and explicit non-claims.
- Implemented worked trace: approved fixture carries intent, command, plan, context, route, claim, work, audit, evidence, and SCF no-promotion artifacts; blocked fixture carries the same spine while recording denied execution authority, unaccepted residual, governance review, and promotion blockers.
- Implemented Codex test: End-to-end intent trace test as deterministic fixture coverage only; no integrated runtime trace or replayed demo exists.
- Implemented Codex test: Artifact continuity audit as deterministic fixture coverage only; no live artifact-continuity audit exists.
- Implemented Codex test: Authority stop-condition test as deterministic blocked-trace fixture coverage only; no deployed authority stop-condition checker exists.

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
| External comparators | `ext_model_cards_2019`, `ext_datasheets_datasets_2021`, `ext_factsheets_ai_services_2019`, `ext_ml_reproducibility_program_2021` | Load after Theseus sources to position report-first packets against structured model reporting, dataset documentation, AI-service declarations, and ML reproducibility programs. Treat them as comparator vocabulary, not evidence that Theseus has been reproduced. |

Draft arc:

- Problem: The book needs a concrete implementation-reference chapter for how the ASI stack can be operated as report-first local machinery instead of only conceptual layer diagrams.
- Insufficiency: A prototype roadmap is not enough unless readers can see how goals, plans, arms, reports, gates, residuals, checkpoints, compute, and operator surfaces interact in a working research system.
- Mechanism: Treat reports and ledgers as the contract, with dashboards as surfaces over those artifacts.
- Mechanism: Use the loop pressure -> attempt -> residual -> diagnosis -> compression -> verification -> structure -> new pressure as implementation discipline.
- Mechanism: Gate heavy training and self-evolution through architecture, preflight, resource, and candidate-promotion checks.
- Mechanism: Route operator work through a durable work board, command vocabulary, node registry, hooks, and feedback reports.
- Mechanism: Keep sparse teacher use proposal-first and guarded by branches, checks, benchmark regressions, and review.
- Mechanism: Treat source-note lineage, imported reports, reproduced runs, missing artifacts, and public non-claims as separate evidence categories so Theseus remains an implementation reference rather than laundered capability evidence.
- Mechanism: Position Theseus report packets against external reporting and reproducibility practices: model cards, datasheets, AI service FactSheets, and ML reproducibility checklists/reports.
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
- Source-noted external comparator rows for `ext_model_cards_2019`, `ext_datasheets_datasets_2021`, `ext_factsheets_ai_services_2019`, and `ext_ml_reproducibility_program_2021`, without treating those records as Theseus reproduction, compliance, or support-state promotion.
- Implemented repository-level fixtures and guards: `theseus_report_crosswalk_record.valid.json` validates report-crosswalk record shape only, `experiments/theseus_import/fixtures/valid/architecture_gate_public_report.valid.json` imports one public-safe static architecture-gate report summary by digest, `experiments/theseus_generation_mode_import/fixtures/valid/generation_mode_gate_public_summary.valid.json` imports one public-safe static generation-mode report summary by digest, `docs/theseus_support_replay_probe.md` records a local replay of both ASI-side Theseus validators with support-state effect `none`, and `python3 scripts/validate_theseus_concrete_evidence_surface.py` keeps the public-safe 14/14 architecture-gate, 18 modes, 13 comparisons, zero-promotable-comparison, digest, replay-probe, and non-claim facts visible. No live Theseus report bundle, public task bundle, benchmark environment, current dashboard, work-board step, or model artifact has been rerun, and this does not promote chapter-core support.
- Implemented Codex test: Theseus report crosswalk fixture validation
- Implemented Codex test: Static architecture-gate import validation
- Implemented Codex test: Static generation-mode gate import validation
- Implemented Codex test: Theseus support replay probe
- Implemented Codex test: Theseus concrete evidence-surface validation
- Implemented Codex test: Dashboard-only implementation-reference negative case
- Implemented Codex test: Missing/failing gate promotion negative case
- Implemented Codex test: Imported report-bundle completeness negative case
- Implemented Codex test: Replay-readiness boundary negative case
- Implemented Codex test: Public-safe artifact boundary negative case
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

Implemented negative-case theorems now cover dashboard-only implementation-reference rejection, accepted promotions with missing or failing gate reports, incomplete imported report bundles, replay-ready rows without replay boundary fields, and public artifacts that copy private payloads or claim support promotion without an accepted evidence transition. These remain record-level gates only; they do not prove live Theseus behavior, replay execution, artifact truth, support-state promotion, or self-evolution safety.

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
- Implemented Codex test: Prototype evidence-state audit, via `python3 scripts/validate_readiness_residual_gates.py` over expired-evidence rerun/reject behavior; full phase acceptance audit remains unrun.
- Implemented Lean follow-through: finite prototype phase-route envelope rejects missing source-matrix readiness, self-improvement without independent evaluation, and promotion requests without an evidence-transition record; it routes failed acceptance gates to research-only and routes accepted non-promoting phases to integration without claiming phase completion.

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
| External comparators | `ext_literate_programming_1984`, `ext_jupyter_book_docs`, `ext_quarto_books_docs`, `ext_nist_ai_rmf_1_0_2023`, `ext_frontier_ai_regulation_2023`, `ext_helm_2022`, `ext_livebench_2024`, `ext_benchmark_contamination_2023` | Use source-noted records to position living-book methodology against literate programming, executable/computational books, Quarto book publishing, governance lifecycle reporting, transparent evaluation reporting, and living benchmark practice; do not treat them as external review, manuscript-quality evidence, or support-state promotion. |

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
- Mechanism: pair with Evidence States as the book's methodological contribution: manifest-driven source of truth, source queues, claim ledger, proof manifest, evidence transitions, no-axiom discipline, release records, and reader-edition derivation.
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
- Source-noted external comparator rows now position the method against literate programming, executable/computational books, Quarto book publishing, AI risk-management reporting, transparent evaluation, living benchmarks, and contamination warnings without claiming external review or artifact approval.
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

Appendix G is the generated top-level appendix for Corben's own papers, Corben-supplied materials, recovered project records, and local project records. Appendix H is a separate generated top-level appendix for external sources by other authors and organizations. Do not present external sources as a second part of Appendix G, and do not present Corben/local records as a section of Appendix H. Both appendices must include a `Source Ownership Boundary` block before their identity tables: G must state that it is the Corben-side source appendix only, while H must state that it is the external-source appendix only. Both appendix scope tables must include an ownership-rule row: G is for material Corben wrote, supplied, recovered from his project history, or built locally; H is for sources produced by other authors, organizations, or outside projects. Both appendices must also keep an appendix-local `Appendix Identity` table before the long source rows: Appendix G states what belongs to Corben/local sources and excludes external sources, while Appendix H states what belongs to outside-author sources and excludes Corben/local sources. Do not use a shared two-row ownership table that makes the source appendices read like two parts of one Appendix G. Both appendices should remain generated from `sources/source_inventory.json` and `book_structure.json`. External literature should stay in Appendix H and should be added only when bibliographic metadata is recorded and the source is actually used.

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
