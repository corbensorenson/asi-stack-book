# Source Note: GenesisCode v0.2 paper, implementation guide, and style contract

| Field | Value |
|---|---|
| Source ID | `genesiscode` |
| Source title | GenesisCode v0.2 |
| Ingestion date | 2026-06-24 |
| Source version / URL | Three-tab Google Docs bundle: https://docs.google.com/document/d/1w4gKcF9a7oV6hsUECsWeEafblvc78ZusxaxdUTfLR2M |
| Ingestion basis | Complete local raw cache inspected at `sources/raw/google_docs/genesiscode.txt`; 7,785 words; raw text is not published. |

## Claim boundary and source topology

The source is a three-part design bundle:

1. a 3,252-word v0.2 paper/technical specification for a tiny pure calculus, hardened message protocol, capability effects, evidence-carrying packages, and AI-authored semantic patches;
2. a 2,633-word Rust implementation handoff with invariants, modules, file formats, CLI, tests, repository layout, and then-current Codex workflow suggestions;
3. a 2,072-word style guide specifying canonical formatting, qualified names, module metadata, explicit capabilities, error behavior, obligations, patch stability, and AI-authoring rules.

These are mutually supporting parts of one unimplemented architecture, not independent evidence. The implementation guide's statements about particular Codex models, desktop features, worktrees, instruction-file discovery, and skill conventions are dated workflow advice rather than durable GenesisCode semantics. The style guide repeatedly labels future behavior as if it existed; it is normative design only.

No GenesisCode repository, parser, evaluator, seal implementation, capability runner, effect log, replay checker, package verifier, semantic patch engine, typechecker, proof stack, optimizer, WASM target, test suite, benchmark, or security audit is present in this book repository. “Conforming,” “deterministic,” “unforgeable,” “replayable,” “evidence-carrying,” and “translation validated” therefore remain proposed properties with explicit missing proof and implementation obligations.

## Thesis

GenesisCode argues that an AI-native programming system should not put the model inside the trust boundary. AI proposes canonical program changes; a small deterministic semantic core, unforgeable control protocol, capability-mediated effect layer, evidence/obligation engine, provenance graph, and structural patch checker decide what can become executable or publishable software.

The durable stack lesson is **proposal is not protocol, protocol is not authority, authority is not effect, and an effect receipt is not evidence that the intended obligation was satisfied**. Each transition needs a distinct artifact and verifier.

The language proposal uses one canonical S-expression IR, a small call-by-value lambda calculus over immutable data, contracts as message-handling closures with explicit prototype delegation, sealed privileged results for `UNHANDLED`, `EFFECT`, and `ERROR`, and a free effect-program representation interpreted by a deny-by-default host runner. Packages carry obligation declarations and content-addressed evidence. AI changes become structural semantic patches whose application triggers validation and affected obligations.

## Mechanisms

### Trust strata and the pure kernel

The paper divides trust into:

- **TCB-A:** Gλ evaluator, total immutable primitives, and seal/unseal;
- **TCB-B:** capability runner, replay checker, and package/hash/signature/policy verifier;
- **non-TCB but validated:** optimizer, JIT, e-graph rewriter, compiler, WASM backend.

This is a useful starting decomposition, but each item still needs code identity, build/toolchain identity, semantic specification, test/proof evidence, dependency closure, and a consumer-relative threat model. “Small” is a measurable code/dependency/state claim, not a property conferred by a three-item list. TCB-B is not optional to claims about effects, replay, supply chain, or package acceptance.

The proposed Gλ kernel contains variables, unary lambda, application, quoted immutable data, total primitives, and seals. `if`, `let`, multi-argument calls, modules, and conveniences desugar outside the kernel. Evaluation is call-by-value with lexical scope. Host-language panics reachable from user input are forbidden; internal failures must become typed Rust errors and then a privileged language-level error at the boundary.

### Fresh-seal contradiction and authority minting

The most important unresolved design issue is that `seal()` creates a fresh unforgeable identity while TCB-A is described as pure and deterministic. Freshness requires state, randomness, a deterministic name supply bound to an initial state, or a host-provided token. Any of those is an effect or explicit state transition. Treating freshness as an ordinary pure primitive makes replay, equality, serialization, process restart, and canonical hashing underspecified.

A repaired architecture should separate:

1. a pure `seal(value, token)` / `unseal(value, token)` relation;
2. authority-token minting as an initialization or runtime effect with exact issuer, entropy/name-supply, epoch, scope, exportability, revocation, replay, and persistence policy;
3. logical protocol roles such as `UNHANDLED` from physical token identities;
4. cross-process reconstruction rules that do not accidentally make privileged tokens forgeable.

Unforgeability also depends on representation opacity, runtime memory safety, equality behavior, serialization exclusion or authenticated rehydration, FFI boundaries, debugger/reflection access, and secret/token leakage. A nominal `SealId` enum field is not by itself a security proof.

### Canonical CoreForm and stable identity

All surface syntax and DSLs lower to one canonical CoreForm S-expression AST. Stable parsing/printing and ordering are intended to support reproducible hashing, structural validation, compact model context, provenance, and patches. The implementation guide proposes immutable data, interned symbols, persistent environments, and BLAKE3 hashes over canonical forms and evidence artifacts.

Canonical syntax is not canonical semantics. Desugaring version, symbol normalization, numeric/byte encoding, map ordering, Unicode, source spans, macro expansion, dependencies, Prelude version, and arithmetic semantics must be bound. A stable source hash does not identify a closure unless code, captured environment, referenced cells, runtime semantics, and dependencies are also frozen. Runtime values containing fresh seals cannot be hashed reproducibly without an explicit identity treatment.

The style guide's durable constraints are useful for AI-produced artifacts: qualified operation names; explicit map payloads rather than ambiguous positions; stable key/definition ordering; one top-level definition per form; explicit exports; `:intent`, invariants, capabilities, obligations, tests, examples, error behavior, and cost notes; executable examples; no ambiguous `nil`; and shallow named helpers. These improve patchability and review but do not establish correctness.

### Contracts and privileged control results

A contract has a handler, optional prototype, metadata, and possible shape identity. It consumes a qualified `(msg op payload)` datum. Dispatch calls the handler and delegates to the prototype only when the result unseals under the trusted `S_UNHANDLED` token. Immutable extension installs an override handler and points to the base. `explain` returns a pure trace of contracts visited, matches, and final result.

Sealing privileged result variants prevents user data that merely resembles `(unhandled ...)`, `(effect ...)`, or `(error ...)` from being interpreted as control. This is a strong general lesson for agent protocols: control-plane variants require an authenticated or unforgeable type boundary, not a magic string.

But seal recognition alone does not authorize the requested effect. The dispatcher must distinguish data authenticity, protocol role, caller identity, delegated authority, target permission, and policy. Code holding a seal can construct privileged values; seal distribution therefore becomes capability distribution. The design needs issuance, custody, least privilege, revocation, rotation, and incident handling.

The `ERROR` design also needs a clear public handling interface. If only trusted Prelude code can unseal errors, ordinary programs need safe predicates and accessors that expose bounded error data without leaking authority. Unknown operations, seal mismatch, malformed messages, handler error, capability denial, and replay mismatch should remain distinct typed states rather than collapse to `nil`.

### Effects, capabilities, and replay

Effectful computation is represented as `Pure(v)` or `Perform(op, payload, k)`, and an actual request crosses the runner as a sealed `EFFECT`. The host injects capabilities for filesystem, network, time, randomness, AI calls, and other authority. The runner denies absent capability by default.

Each proposed log entry contains request hash, allow/deny decision, response hash, capability identity, and optional response/timestamp data. This is useful audit structure but insufficient for deterministic replay when the response payload is omitted. A digest can check a supplied value; it cannot regenerate that value. Replay therefore needs the complete response, a content-addressed immutable response reference with availability guarantees, or a declared non-replayable/verification-only grade.

The request identity must bind more than operation and payload. Continuation identity is only stable if the canonical code, captured environment, dependency graph, semantics, runner, capability/policy version, initial state, and effect index are bound. For AI generation, model name and sampling parameters do not capture provider revision, system instructions, tool/context state, routing, hidden safety policy, prompt bytes, seed availability, or response custody. Pinning the returned artifact supports playback; it does not reproduce the remote model call.

The strong replay contract is thus: exact program/runtime/environment/input identity plus a complete ordered effect transcript yields the same pure reduction and terminal value, or a typed mismatch at the first divergent request. External side effects themselves may be irreversible and must not be replayed merely to reproduce computation. Playback, deterministic simulation, bounded reexecution, and live effect repetition are separate grades.

### Capability declarations and path coverage

One proposed obligation says declared capabilities must cover observed effect operations. This is necessary but not sufficient. A passing trace proves only that its observed operations fell within the declaration. It does not prove unexecuted branches, adversarial inputs, reflection, FFI, dependencies, or future code cannot request more.

Evidence should distinguish static effect-row/type coverage, whole-program or abstract analysis, runtime reference-monitor enforcement, observed-trace coverage, negative/fuzz testing, and OS/hardware enforcement. A declaration plus trace is an under-approximation unless the language and runner make all effects unforgeably mediate through the checked operation.

### Obligation Engine and evidence-carrying packages

Packages declare obligations such as unit/property tests, recorded seeds, coverage, determinism, capability bounds, resource budgets, typechecking, refinements, and translation validation. Evidence is content-addressed and the package hash covers code, obligations, evidence, dependency graph, and toolchain. Registry policy may impose additional minimums, signatures, and transparency logging.

The important distinction is between an **obligation declaration**, its **verification procedure**, an **evidence artifact**, a **verifier result**, a **policy decision**, and the **consumer claim** allowed by that result. Package-supplied obligations can be incomplete or self-serving. Registry-required obligations need independent ownership, version, scope, expiry, waiver, and challenge rules. A test log, coverage report, benchmark, SMT trace, interactive proof object, and compiler-equivalence result have different semantics and cannot be combined as generic green evidence.

“Evidence-carrying software” also needs custody and invalidation. Evidence must bind source, dependencies, environment, verifier, policy, model/tool versions, inputs, seeds, and exact artifact. Dependency or policy change should invalidate affected descendants. A content hash proves identity of retained bytes, not truth, test adequacy, proof soundness, or availability.

### Semantic patches and change acceptance

Instead of asking an AI to rewrite text, GenesisCode asks for structural operations such as replace-node, add/remove module, update dependency, update obligations, or attach evidence. Acceptance validates the patch schema, applies it to canonical ASTs, checks structural invariants and dependencies, reruns affected obligations, and records provenance.

A production semantic patch requires source artifact/version, semantic anchor, expected old hash or precondition, operation, declared intent/non-goals, authority, affected dependency closure, predicted obligation impact, target result hash, validation set, actual mutation set, inverse or compensation, conflicts, provenance, and residuals. Raw AST paths are brittle when neighboring edits shift positions; content-addressed anchors, stable semantic IDs, and ambiguity/conflict handling are needed. “Incremental” rechecking is safe only when dependency and effect closure is sound; otherwise the full gate must run.

AI provenance names the proposal route but does not make the patch correct. The accepter must remain independent enough from the proposer, and a patch that weakens its own obligations or verifier requires higher authority than an ordinary behavior change.

### Types, proofs, optimization, and translation validation

The optional type stack uses row-polymorphic contract interfaces and effect rows, with gradual unknowns and refinement obligations. This fits immutable extension and explicit effects, but the runtime message protocol, delegation, dynamic/unknown values, sealed variants, capability runner, and type erasure must share a precise soundness story. Effect rows express requirements only if every effect path is mediated.

Shapes and polymorphic inline caches can accelerate `(shape-id, op)` dispatch. E-graphs can normalize pure CoreForm and apply equational rewrites. Both sit outside the trusted kernel only if the output is checked against the source semantics. The paper's baseline of equivalence tests is useful evidence but is not full translation validation or proof of equivalence. A stronger route uses per-translation certificates, proof-producing rewrite traces checked by a small independent kernel, symbolic equivalence within a declared fragment, or runtime refinement under bounded observations.

E-graph soundness depends on each rewrite's side conditions, arithmetic semantics, termination/resource behavior, effects, and extraction cost model. “Minimal-cost program” is relative to a calibrated cost function and can change latency, memory, numerical behavior, or denial-of-service exposure even when pure extensional output matches.

### Implementation and conformance artifacts

The handoff proposes six Rust crates plus CLI: CoreForm, kernel, Prelude, effects, obligations, patches, and command wiring. Milestones progress from kernel/Prelude through effects/replay, packages/obligations, patches, types, and optimization. Proposed commands cover format, evaluate, test, capability-run, replay, package, patch, and explain.

The test program is stronger than the old note recorded: golden semantics; protocol-spoof negatives; parser round trips; evaluator no-panic fuzzing; deterministic/replay tests; alpha-renaming and canonical-formatting metamorphic controls; obligation evidence; and a small locked normative spec. Conformance separates required kernel/Prelude/effect/audit/package/patch facilities from optional type/proof/optimization stacks.

The build guide's thread/worktree/AGENTS/skill advice is not a language requirement and should not be copied into the book as current product guidance. The durable process idea is spec-first change: update the normative rule and negative/golden tests before modifying semantics, keep kernel changes minimal, and make semantic changes explicit.

## Evidence

GenesisCode offers concrete syntax, value categories, dispatch pseudocode, effect-log fields, replay behavior, obligation families, package/artifact structure, semantic-patch operations, type signatures, optimization boundaries, Rust modules, CLI commands, test families, implementation phases, conformance requirements, and style rules. Those make it a rich architecture source.

It offers no executed artifact. There is no evidence that seals are unforgeable in an implementation, the evaluator is deterministic or total, effects cannot bypass mediation, logs are replay-complete, patches preserve semantics, obligation policies are adequate, hashes are portable, the compiler remains outside the TCB, e-graph rewrites are sound, or AI-authored code becomes safer or more productive.

A credible prototype needs at least: independent parser/printer canonicalization; cross-platform golden vectors; seal spoofing, leakage, serialization, restart, and FFI tests; pure-kernel determinism and no-panic fuzzing; capability-denial and bypass adversaries; complete-effect-log replay with deletion/missing-response controls; dependency invalidation; patch anchor/conflict/rollback tests; weak-obligation and malicious-evidence tests; translation-validation positive and mutation controls; and comparison with an ordinary typed language/toolchain using the same AI proposer and tasks.

## Failure Modes

- **Freshness hidden in purity:** `seal()` mints identity without explicit state/effect semantics.
- **Nominal unforgeability:** an opaque enum or convention is mistaken for a security proof.
- **Seal overreach:** authenticated protocol role is treated as authorization to execute.
- **Seal custody collapse:** broad distribution of Prelude tokens lets untrusted code mint privileged results.
- **Canonicalization theater:** stable syntax is mistaken for stable semantics or closure identity.
- **Replay by hash:** response digests are stored without the bytes/ref needed to reproduce reduction.
- **Remote-call playback laundering:** cached AI output is called reproduction of the model call.
- **Continuation ambiguity:** request hashes omit closure environment, runtime, policy, or initial state.
- **Observed-capability completeness:** passing traces are generalized to unexecuted branches.
- **Package self-grading:** weak package-declared obligations satisfy themselves.
- **Evidence flattening:** tests, proofs, benchmarks, and signatures become one undifferentiated green state.
- **Stale evidence:** dependency, toolchain, policy, or verifier drift does not invalidate descendants.
- **Brittle patch paths:** positional AST anchors apply to the wrong node after concurrent or neighboring edits.
- **Unsound incremental checks:** incomplete dependency closure skips obligations affected by a patch.
- **Self-weakening patch:** a proposal lowers its own test, capability, or verifier requirements.
- **Translation-validation inflation:** a finite equivalence test is called a proof over all inputs.
- **E-graph side-condition loss:** a rewrite preserves a simplified equation but violates arithmetic, resource, or effect semantics.
- **TCB list inflation:** components called “non-TCB” are accepted without an independent checker.
- **Error collapse:** unhandled, denial, malformed input, replay mismatch, and internal failure become `nil` or one opaque error.
- **Style-as-correctness:** explicit names and metadata improve review but are treated as discharged semantics.
- **Dated tooling prescription:** historical Codex workflow guidance is presented as a current or architectural requirement.

## Cross-paper relationships and tensions

- `cognitive_compilation` owns the general source→semantic→target IR and translation-contract story. GenesisCode provides one code-oriented canonical IR and patch instance.
- `talos` owns typed job execution and delivery. GenesisCode packages and effects are substrate candidates, not a competing Labor OS.
- `spinoza` owns claim/evidence semantics and downgrade. GenesisCode's obligation engine should consume those distinctions rather than treating every artifact as proof.
- `scf` supplies capability identity, qualification, lifecycle, and no-self-ratification pressure missing from the seal/capability sketch.
- `ladon_manhattan` supplies secret-handle and compartment boundaries relevant to token custody.
- `deterministic_capability_compilation` generalizes candidate-specific preservation, foundry stages, fallback, and residual escrow; GenesisCode's compiler/patch pipeline is a possible substrate.
- Standard proof-carrying-code, capability-security, language-semantics, supply-chain, content-addressing, e-graph, type/effect, and translation-validation literature is needed before novelty or security positioning.

## Book Chapters Supported

- `executable-specifications-and-lean-proof-envelope`: trust strata, spec-first semantics, heterogeneous obligation/evidence lanes, translation-validation boundaries, and the fresh-seal contradiction.
- `runtime-adapters-tool-permissions-and-human-approval`: authenticated control variants versus authorization, token issuance/custody, capability enforcement, replay-complete effect transcripts, and observed-path limits.
- `artifact-graphs-audit-logs-and-replay`: content-bound packages, graded replay, effect response custody, semantic patch identity/preconditions/impact/rollback, evidence invalidation, and provenance.
- `cognitive-compilation-and-semantic-ir`: canonical IR, deterministic lowering, semantic anchors, patch-local repair, and the syntax-versus-semantics boundary.
- `system-boundaries-and-authority`, `intent-to-execution-contracts`, and `labor-os-and-typed-jobs` receive supporting distinctions only; the mature mechanism owners above should hold the prose.
- `spinoza-verification-and-proof-carrying-claims` receives the obligation-artifact and independently governed acceptance distinctions; GenesisCode does not establish evidence validity.
- `mathematical-and-search-substrates` may retain Gλ/e-graph ideas as candidate substrates, but GenesisCode supplies no mathematical or performance result.
- `open-research-agenda-and-bibliography-plan` owns the unresolved token, replay, capability-coverage, patch, type-soundness, and translation-validation experiments and external comparison work.

No new chapter is warranted. The source is a concrete programming substrate spanning existing specification, compilation, runtime, and artifact interfaces.

## Claims To Add Or Update

- Represent privileged control results with an authenticated/unforgeable type boundary, while keeping authentication separate from authorization.
- Treat token minting as explicit authority-bearing state/effect, not a pure primitive.
- Require replay transcripts to retain response bytes or durable immutable refs; hashes alone provide verification, not replay.
- Separate observed capability coverage, static effect coverage, runtime enforcement, and OS enforcement.
- Grade obligation evidence by artifact lane and bind registry policy independently of package self-declaration.
- Define semantic patches with stable anchors, preconditions, impact closure, revalidation, inverse/compensation, and self-weakening controls.
- Call test-based optimizer comparisons tests; reserve translation-validation/proof language for the exact checked relation.
- Keep canonical syntax, semantic identity, executable identity, and runtime state as distinct hashes/contracts.

## Open Questions

1. What is the exact semantics of token minting, restart, serialization, revocation, and cross-process replay?
2. Can a tiny independent checker establish that every privileged variant originated from an authorized issuer without exposing its token?
3. What complete replay record is acceptable when effect responses contain secrets, personal data, large blobs, or expiring licensed content?
4. How are content-addressed response refs kept available, revoked, redacted, or privacy-deleted without falsifying replay grade?
5. Can all effect paths, including FFI and dependencies, be forced through the capability runner?
6. Which registry obligations are mandatory and independently governed rather than chosen by a package?
7. What semantic anchor survives canonical reformatting, refactoring, concurrent patches, and module moves?
8. How is affected-obligation closure computed and tested against omitted-dependency mutations?
9. Which Gλ fragment admits machine-checked translation validation for optimization and WASM lowering?
10. Does the added evidence/provenance burden improve defect rate, review time, patch locality, and recovery under matched real software tasks?

## Section-family closure ledger

| Source family | Disposition | Boundary |
|---|---|---|
| Tab 1 abstract, §§1–3 | AI-as-proposer thesis, contributions, goals/non-goals, and TCB strata integrated or retained here. | “Small,” “deterministic,” and “unforgeable” remain unimplemented targets. |
| Tab 1 §§4–5 | Canonical CoreForm, value model, Gλ syntax/evaluation, total-error boundary retained; canonical syntax/semantics distinction added. | No parser, evaluator, semantics proof, or cross-platform canonical vectors. |
| Tab 1 §6 and examples | Contract fields, qualified message, sealed protocol variants, delegation, immutable extension, introspection, and examples retained; authentication/authorization and seal-custody boundaries integrated. | Examples are illustrative; fresh-seal semantics are unresolved. |
| Tab 1 §7 | Free effect IR, sealed request, host capabilities, log fields, replay, and AI calls retained; response-custody and replay-grade repair integrated. | Hash-only logs cannot reproduce missing responses; no runner or replay exists. |
| Tab 1 §8 | Obligation types, evidence artifacts, package policy, content addressing, signatures/transparency retained; heterogeneous evidence and independent-policy boundaries integrated. | Obligation metadata is not discharged evidence; no verifier or registry exists. |
| Tab 1 §9 | Structural patch operations and acceptance pipeline integrated into semantic compilation/artifact boundaries. | Stable anchors, conflict, impact closure, and rollback are unspecified in source and added as obligations. |
| Tab 1 §§10–12 | Row/effect/refinement types, shapes/PICs, e-graphs, translation validation, WASM, and optional self-reference retained as research candidates. | Test equivalence is not proof; self-reference is explicitly non-essential; no implementation/result. |
| Tab 1 §§13–16 | Immutable-variable and AI-map examples, six implementation phases, conclusion, and conformance checklist retained or routed to research. | Promotional “beyond SOTA/near magical” language has no evidence effect. |
| Tab 2 §§0–10 | Non-negotiable invariants, deliverables, Rust workspace, AST/value/env choices, contracts, effects, packages, patches, CLI, test pyramid, and spec lock-in retained as implementation obligations. | Suggested types, BLAKE3, TOML, Rust, and module boundaries are design choices, not validated standards. |
| Tab 2 §§11–14 | Historical Codex parallelization, instruction, skill, and prompt templates retained only as lineage/process context. | Product/model claims are dated and not book architecture or current guidance. |
| Tab 3 §§1–4 | Canonical formatting, purity, seals, evidence, names, modules, exports, metadata retained as authoring constraints. | Style improves reviewability but does not prove semantics. |
| Tab 3 §§5–8 | Contract/error/effect/capability/test/obligation conventions retained; typed error and coverage limits added. | Capability declarations and tests do not establish full mediation. |
| Tab 3 §§9–14 and appendix | Patch-friendly ordering, documentation, namespaces, AI rules, formatter spec, module template, and early design decisions retained as proposed lint/format policy. | Names are placeholders; formatter, linter, language, and standard library do not exist. |

**Closure result:** all three tabs and every numbered section, implementation milestone, pseudocode/schema family, example, test class, style rule, template, and open design decision have an explicit disposition. No GenesisCode implementation, semantics proof, seal-security result, capability enforcement, replay, package acceptance, semantic-patch correctness, type soundness, translation validation, optimization result, benchmark, safety result, deployment, support, novelty, SOTA, AGI, or ASI claim is promoted.
