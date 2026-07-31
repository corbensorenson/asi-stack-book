# Source Note: Cognitive Compilation

| Field | Value |
|---|---|
| Source ID | `cognitive_compilation` |
| Source family | Four-tab export: architecture draft; standalone-paper rewrite; conference-style rewrite plus Semantic Compiler Workbench build specification; reverse-compilation and semantic-merge addendum |
| Ingestion date | 2026-06-24; fidelity audit begun 2026-07-31 |
| Source version / URL | Google Docs inventory source: https://docs.google.com/document/d/1spEWiRnk1NUFuK3BLh3X80r_Up_SyebO1c3JSEzTUis |
| Canonical local cache | `sources/raw/google_docs/cognitive_compilation.txt`; raw text is not published by this note |
| Evidence boundary | Architecture, schemas, pseudocode, detailed product specification, worked code/story examples, evaluation plan, and implementation directions. No Semantic Compiler Workbench repository, compiler execution, validator trace, repair measurement, benchmark result, license review, or independent reproduction is present. |

## Thesis

Complex generative work should be compiled rather than emitted in one opaque
prompt. An accepted goal becomes a source plan, typed semantic IR, target IR,
artifact, validator result, and localized repair transaction. Explicit
obligations, stable identities, dependency graphs, capability routing,
multi-target lowering, trace bundles, and incremental recompilation aim to make
requirements, failures, costs, and provenance inspectable.

The later addendum makes the architecture bidirectional. Existing code and
documents can be lifted into provenance-bearing semantic claims, reconciled
under explicit merge policies, refactored at the IR layer, and recompiled. That
is a powerful mining mechanism, but a lifter recovers evidence and hypotheses,
not ground-truth authorial intent.

## Claim Boundary and Variant Status

Tabs 1–3 repeat and progressively formalize the same forward compiler. Tab 3
adds a prescriptive, commercial “Codex Build Document” for a Rust/Tauri local
product called Semantic Compiler Workbench (SCW). Tab 4 adds reverse
compilation. Repeated prose is one architecture lineage, not corroboration.

Statements such as “state of the art,” “complete production-grade,” “compiler
moat,” “must ship,” and “no MVP shortcuts” are product requirements, not
evidence. The source contains no SCW implementation or observed result. Example
Python and narrative outputs show a desired target shape, not validated
semantic preservation. Feature-comparison checkmarks and external references
need independent current passage review before novelty or support use.

## Conceptual Primitives

- **Source Plan.** Goals, audience, formats, hard/soft constraints, typed
  interfaces, acceptance validators, targets, budgets, privacy, risk, non-goals,
  and a canonical lock hash.
- **Semantic atom.** Stable obligation node with operation kind, typed inputs
  and outputs, constraints, dependencies, provenance, routing bounds, features,
  validators, authority, state, and repair policy.
- **S-IR.** Versioned semantic DAG plus plan hash, lints, features, and stable
  node identities.
- **T-IR.** Target-specific render units, artifact locations, trace anchors,
  and validator plan bound to the S-IR.
- **Trace Bundle.** Plan, S-IR, schedule, T-IRs, artifacts, span maps, validator
  results, router decisions, cost report, security/redaction report, and a
  content-hashed manifest.
- **Pass contract.** Input/output dialects, pre/postconditions, legality, loss,
  ambiguity, authority effects, dependencies, deterministic/nondeterministic
  inputs, costs, failure outputs, and reproducer bundle.
- **Localized repair.** Structured diagnostic to stable nodes and artifact
  ranges, declared patch scope, observed mutations, dependency-closed rebuild,
  revalidation, and residuals.
- **LS-IR.** Lifted S-IR node with origin kind/digest, exact source spans,
  confidence, lift method, license metadata, and fact/claim/guess class.
- **Semantic Knowledge Graph.** Persistent cross-run index of semantic nodes and
  relations; it supports retrieval but conveys neither truth nor reuse rights.
- **Merge Bundle.** Sources, fingerprints, merge policy, aliases, conflicts,
  decisions, rejected alternatives, result S-IR, and origin trace links.

## Mechanisms

### Forward compilation

Freeze consumer, purpose, accepted command/plan version, source and target
languages, compiler/pass set, environment, evaluators, authority/rights
ceilings, budgets, and material-change triggers. Parse and canonicalize the
plan; index clauses; extract semantic atoms; normalize synonyms and shared
constraints; type inputs/outputs and insert explicit adapters; infer
dependencies; lint missing acceptance coverage, orphan nodes, contradictions,
and underspecification; eliminate only safely dead/common structure; compute
difficulty, ambiguity, novelty, blast radius, and validator-strength features.

Lower S-IR separately for code, documents, narrative, songs, or other targets.
Each backend maps operation kinds to target constructs, constructs an artifact
plan, provides trace anchors, and declares validators. Scheduling uses critical
path and slack plus a customer-owned route policy over deterministic tools and
model capability classes. Strict structured output, schema validation, retries,
fallbacks, budgets, privacy flags, and route decisions are explicit.

Validators attach structured diagnostics to node IDs and artifact ranges.
Repair proposes a semantic patch, freezes the affected subgraph, applies a
transactional target patch, computes actual mutation and invalidation closure,
reruns affected validators, and either commits a new artifact version or rolls
back. Cache keys bind all semantic and execution dependencies; a hit cannot
silently waive validation.

### Product blueprint retained as research objects

The SCW specification proposes a local Rust daemon, Tauri/React desktop app,
Rust CLI, Axum API, SQLite/content-addressed store, Petgraph DAG operations,
OS keychain, sandboxed validators, redacted exports, OpenRouter-first adapters,
offline operation, and optional MCP. It specifies versioned Plan, S-IR,
Schedule, T-IR, Trace, and claim schemas; a UI for plans, graphs, nodes,
artifacts, validators, costs, providers, license, and audit; CLI parity; Python,
Docs, Narrative, and Song backends; three golden fixtures; and nineteen groups
of acceptance/delivery requirements.

The source also specifies one-time/trial licensing, offline verification,
update entitlement, and non-destructive expiry behavior. Those are product
policy proposals, not book architecture defaults. A license mechanism cannot
erase user data, hide provenance, or grant rights over imported material.

The detailed build fields remain concrete implementation obligations:

| Family | Retained requirements and boundary |
|---|---|
| Plan/S-IR | Canonical JSON lock hashes; stable clause and node IDs; typed interfaces; hard/soft constraints; validators; provenance; lints; routing bounds; ambiguity, novelty, blast-radius, and validator-strength features. Hashing proves exact identity, not semantic completeness. |
| Schedule/T-IR | Policy version; critical/slack priority; assigned tier/engine/model and fallbacks; attempt/token/money/time budgets; sandbox; p50/p90 forecast; concurrency groups; target render units, paths, trace anchors, and validator plan. Forecasts are not outcomes. |
| Trace | Plans, IRs, artifacts, span maps, structured validator JSONL, route decisions, cost, redaction, and manifest hashes. A reproducible bundle can reproduce the wrong semantics. |
| Adapters/validators | OpenRouter-first plus optional direct adapters; strict structured responses; Python `ruff`/compile/tests/smoke, Docs lint and claim/code checks, Narrative continuity/constraint checks, and Song structure/meter heuristics. A validator's claimed scope and destructive controls remain explicit. |
| Repair/store | Node and diagnostic IDs, failed validators, frozen affected subgraph, patch operations, actual mutation set, dependency rebuild, rollback; SQLite index plus content-addressed artifacts and versioned run bundles. “Split on failure” does not prove semantic locality. |
| Security | OS keychain, no keys in prompts/logs, sandbox profiles, network/file/time limits, export redaction, and a redaction manifest. Local API and local storage do not by themselves establish confidentiality. |
| License | Signed trial/full status, offline checks and grace, update entitlement, non-destructive expiry, and always-available data export. Commercial enforcement is outside the book's evidence and rights authority. |
| Backends/fixtures | Python, Docs, Narrative, and Song target contracts; deterministic todo-CLI, mini-narrative, and song-structure fixtures; plan lock, stable IR, schedule, trace, structured failure, repair, export, key, and license acceptance checks. Passing fixtures would establish only their declared finite behavior. |

### Reverse compilation and merge

A repository lifter deterministically inventories files, languages, ASTs,
public interfaces, imports, routes, configurations, tests, and documentation,
then adds model-inferred semantics with lower confidence. Document/narrative
lifters segment structure, entities, events, temporal order, continuity, style,
and explicit constraints. Song lifters segment sections, motifs, rhyme/meter,
and structure. Every inferred node retains origin spans and method.

Merge policies may prefer stronger evidence, source priority, validator
strength, modernity requested by the user, lower complexity, or preservation of
both variants. Deterministic checks expose interface, schema, invariant,
ordering, and name conflicts; qualified review handles semantic conflicts.
Semantic refactoring edits a locked graph version, tracks fact/claim/guess
promotions, generates acceptance tests, and recompiles. The output checker looks
for obligation loss and leakage from rejected origins.

## Interfaces and State Machines

The source plan moves `draft -> linted -> locked -> superseded`; edits to a
locked plan create a new version. S-IR nodes move through extracted,
normalized, typed, dependency-checked, linted, scheduled, lowered, rendered,
validated, failed, repair-proposed, patched, revalidated, committed, rolled
back, or residualized states. Artifacts and trace bundles are append-only
versions rather than overwritten truth.

Intent owns goal meaning and authority; Planning owns obligation/dependency
selection; Cognitive Compilation owns translation contracts and IR; Routing
qualifies models/tools; Runtime owns effects and sandboxes; Validation judges
named predicates; Artifact Graphs own lineage; Security/Privacy/Rights own keys,
taint, imports, export, retention, and licenses; Evidence owners alone move
claims. The compiler can block, narrow, clarify, or residualize. It cannot
reinterpret intent, self-authorize execution, self-certify semantic adequacy,
or declare legal compliance.

## Assumptions and Invariants

- Structured syntax is not semantic preservation; every source obligation has
  a source-to-IR-to-target path and a requirement-specific validator.
- Stable identity is semantic and versioned, not line position, display name,
  embedding, hash equality, graph location, or storage address.
- Ambiguity is typed debt with resolution authority, not silently normalized
  whitespace.
- A semantic relation label is not an executable primitive without operands,
  environment, effects, authority, evidence, and recovery.
- Compiler generation and translation validation are separate enough for the
  claimed property; shared model, prompts, data, and incentives stay visible.
- Source, IR, target validity, artifact utility, external effects, and support
  movement are separate decisions.
- Repair locality is established by observed mutations and dependency closure,
  not the requested patch range.
- Nondeterministic model, tool, sampler, environment, and network inputs are
  recorded; reproducing a manifest does not imply identical semantics.
- Every retry, alternative, failure, discarded artifact, cache hit, repair,
  human intervention, validator, and backend cost stays in the denominator.
- Lifted facts, claims, and guesses never collapse by confidence alone;
  deterministic extraction can still be incomplete or misinterpreted.
- Alias and merge similarity proposes identity; exact effects, consumers,
  authority, rights, state, and conflict rules qualify it.
- Provenance preservation does not itself satisfy copyright, license, privacy,
  consent, attribution, or trade-secret obligations.
- Secret values never enter prompts or logs; taint and redaction events remain
  in exported manifests.

## Evidence

The paper family supplies an end-to-end architecture, pseudocode, schema fields,
compiler passes, route policy, UI/CLI/product specification, worked code and
story lowering, evaluator metrics, ablations, golden-fixture requirements, and
reverse-lifting acceptance criteria. These are valuable implementation and
falsification objects. No local compiler, trace bundle, schema implementation,
validator execution, node-local repair, reverse lift, semantic merge, license
enforcement, benchmark, or source-reported external result is reproduced.

A competent campaign spans code, documents, narrative, structured data, and
mixed artifacts with natural requirement changes, ambiguity, conflicting
sources, broken dependencies, hidden constraints, validators of varying power,
rights conflicts, and delayed outcomes. Baselines include direct prompting,
agent loops, human-authored artifacts/workflows, planning without S-IR, target
templates, retrieval/summary integration, parser-only lifting, full-source
editing, and global regeneration. Match models, tools, context, budgets,
authority, evaluators, retries, and time.

Measure obligation/field preservation, semantic typing, dependency accuracy,
target validity, cross-target consistency, validator discrimination, repair
mutation radius and downstream rebuild, accepted utility, trace/provenance
completeness, lifted fact/claim calibration, conflict and alias precision/recall,
rejected-origin leakage, rights handling, latency, tokens, compute, money,
human effort, coordination, storage, security events, and total useful cost.

The architecture narrows when direct or manual baselines match outcomes at
lower total burden; S-IR omits or distorts requirements; validators share the
same error or fail destructive controls; routing degrades quality; multi-target
outputs diverge; local repair changes broad hidden state; traces cannot replay
material decisions; lifters hallucinate or miss interfaces; merge policies
launder conflicts, rights, or source expression; or transfer fails across
domains, models, languages, organizations, and time.

## Failure Modes

- Requirement extraction encodes an incomplete, biased, or unauthorized plan.
- Schema validity and graph acyclicity launder semantic underspecification.
- Node IDs drift across versions or repair is localized only by text adjacency.
- Hash equality is called semantic parity, or unequal hashes are called failure.
- Validators are scarce, weak, self-authored, proxy-only, or optimized against.
- Multi-pass overhead exceeds any accepted quality, repair, or reuse gain.
- Critical-path and routing estimates create parallelism or arbitrage theater.
- Global caches reuse stale semantics after source, policy, evaluator, or target
  drift.
- Reverse lifting elevates plausible guesses to facts and hides parser gaps.
- Semantic merge erases conflicts, rejected variants, provenance, licenses,
  personal data, or protected expression.
- “Local-first” claims hide provider calls, telemetry, key exposure, or
  nonportable sandboxes.
- Licensing enforcement bricks data, blocks export, or becomes a false security
  boundary.
- Product completeness language is mistaken for implementation or evidence.

## Cross-Paper Synthesis

- PlanForge owns source-plan obligation DAGs and schedules; Cognitive
  Compilation owns semantic/target lowering and translation validation.
- VIEA supplies accepted command contracts and durable artifact feedback;
  compiler success cannot grant authority.
- QCSA supplies stable semantic identities, versioned task-relative addresses,
  and question-compiled ambiguity resolution.
- Kernel English is a candidate semantic target language whose compiler,
  residual, renderer, and exact-object obligations must remain visible.
- RDC supplies typed relational IR and dimension-safe operator lowering;
  generic tensor dimensions cannot replace role semantics.
- Deterministic Capability Compilation supplies explicit-to-learned-to-explicit
  feedback and obligation conservation; reverse lifting supplies artifact-to-IR
  evidence, not automatic capability qualification.
- Artifact Graphs, Supply Chain, Privacy/Rights, and Claim Ledgers own the trace,
  origin, dependency, taint, license, and epistemic consequences of lifting and
  merge.

## Book Chapters Supported

- `human-intent-as-a-formal-input`
- `intent-to-execution-contracts`
- `planning-as-a-control-layer`
- `cognitive-compilation-and-semantic-ir`
- `artifact-graphs-audit-logs-and-replay`
- `compact-generative-systems-and-residual-honesty`
- `mathematical-and-search-substrates`
- `governed-world-models-and-reality-grounding`

## Claims To Add Or Update

- Treat intent-to-artifact work as a versioned, validator-bound translation
  pipeline with stable obligation identities and explicit loss.
- Keep compiler, evaluator, runtime, rights, and evidence authority separate.
- Require observed-mutation repair receipts and dependency-closed rebuilds.
- Preserve reverse-lift origin spans and fact/claim/guess states through merge
  and recompilation.
- Treat semantic merge as a governed conflict transaction, not smart copy/paste.
- Count SCW schemas, UI, CLI, licensing, backends, and acceptance lists as
  implementation requirements until actual artifacts are inspected and run.

## Open Questions

- Which semantic atom vocabulary is expressive without becoming an informal
  ontology or target-specific instruction set?
- How can natural-language obligation preservation be evaluated independently
  enough to catch shared interpretations?
- When does multi-pass compilation beat direct generation after full cost?
- Which artifact classes permit reliable lifted facts, and where must most
  nodes remain claims or guesses?
- How can rejected-origin leakage and protected-expression reuse be tested?
- Which merge conflicts can be resolved mechanically, and which require rights,
  domain, or affected-party authority?
- Can localized repair remain local under hidden model and cache state?

## Section-Family Coverage

| Source section family | Actual owner or disposition |
|---|---|
| Tab 1 §§1–2 | Cognitive Compilation problem/core: direct-generation failure modes, three-stage overview, and explicit compiler boundary integrated. |
| Tab 1 §§3–5 | Human Intent, Planning, Cognitive Compilation: Source Plan, S-IR atoms/data/passes/errors, backend interface, target examples, and atomic lowering integrated. |
| Tab 1 §§6–8 | Planning, Routing, Verification, Security: DAG scheduling, capability classes, caching, validator layers, repair, injection/taint/sandbox concerns retained. |
| Tab 1 §§9–12 | source note and research owners: component sketch, pseudocode, evaluation, limitations, and conclusion retained as proposals. |
| Tab 2 §§1–4 | source note and chapter framing: contribution/related-work/three-stage/DAG rationale retained; external comparisons require independent review. |
| Tab 2 §§5–8 | Cognitive Compilation: exact Source Plan/S-IR/T-IR fields, passes, MVC, slack, incremental cache, validators, and localized repair integrated. |
| Tab 2 §9 | source note: todo CLI and story/explanation walkthrough retained as illustrative target shapes, not validation. |
| Tab 2 §§10–13 | implementation/evidence backlog: tooling, nondeterminism, trace bundles, benchmarks, baselines, metrics, ablations, limitations, conclusion retained. |
| Tab 3 §§1–13, Appendix A, references | duplicate/expanded standalone paper reconciled once; code/story examples, comparison table, and nineteen references retained without novelty or reproduction claims. |
| Tab 3 SCW §§0–3 | source note: product intent, non-negotiables, daemon/UI/CLI shape, end-to-end workflow, screens, and commands retained as unimplemented requirements. |
| Tab 3 SCW §§4–7 | Cognitive Compilation/Planning: Plan/S-IR/Schedule/T-IR/Trace schemas, op enum, passes, tiers, policy, scoring, scheduling, and accounting integrated or retained. |
| Tab 3 SCW §§8–13 | Runtime/Security/Rights owners: model adapters, structured outputs, validator interface, claim-native docs, repair, stores, reproducibility, keychain, sandbox, redaction, and licensing retained as proposals. |
| Tab 3 SCW §§14–19 | Prototype/evidence backlog: four backends, stack/repo layout, golden fixtures, acceptance criteria, build sequence, and deliverables retained; no artifact exists. |
| Tab 4 A1–A3 | Cognitive Compilation reverse path: LS-IR, SKG, merge bundle, repo/doc/story/song lifters, provenance/confidence classes integrated. |
| Tab 4 A4–A6 | Cognitive Compilation: merge policies, deterministic conflicts, aliases, provenance, semantic refactor, and recompilation integrated with authority/rights boundaries. |
| Tab 4 A7–A10 | source note and Prototype/Rights owners: UI, legal/IP metadata, CLI, and acceptance criteria retained as implementation obligations. |

## Closure Status

**Section-family audit complete as of 2026-07-31.** All three forward-compiler
variants, the nineteen-part SCW build specification, Appendix A, references,
and the ten-part reverse-compilation addendum terminate in manuscript
integration, public-safe note retention, a concrete implementation/evaluation
obligation, variant reconciliation, or an explicit non-claim. The detailed
schema, adapter, validator, repair, store, security, licensing, backend,
fixture, UI/CLI, acceptance, and delivery fields remain in this note because
repeating a commercial product specification would overload the book. Their
durable architectural consequences—translation contracts, stable identity,
trace bundles, observed repair locality, reverse lifting, governed merge,
origin/rights custody, and leakage checks—are reader-visible in Cognitive
Compilation and Artifact Graphs.

Closure establishes no compiler, lift, merge, trace, repair, cost, security,
licensing, deployment, support, or ASI result. Reopen on material source,
implementation-artifact, or receiving-chapter drift.
