# Source Note: Deterministic Capability Compilation

| Field | Value |
|---|---|
| Source ID | `deterministic_capability_compilation` |
| Source title | Deterministic Capability Compilation: A Capability-Preserving Ladder from Executable Scaffolds to Governed Adaptive Agents |
| Author / date | Corben Sorenson; July 2026; conceptual architecture v1.0 |
| Ingestion date | 2026-07-18 |
| Canonical local text | `sources/raw/corben_papers/deterministic_capability_compilation/deterministic_capability_compilation.md`; SHA-256 `8306d2bd40662245f8d3f044b4ca11a61c0fb18ab7cb799ccfe64f5e8c8a80c1` |
| Supplied presentation copy | `sources/raw/corben_papers/deterministic_capability_compilation/deterministic_capability_compilation.docx`; SHA-256 `4c449720157e02bc7f5cd15ea7a50bb236554d94cc12275e31726db155502c34` |
| Storage boundary | Both supplied files are retained in the ignored local raw-source cache. This tracked note is public-safe; ingestion does not itself authorize publication of the raw paper. |
| Evidence boundary | The paper is an architecture and research program. It supplies design rationale, conditional propositions, artifact contracts, threats, experiments, baselines, and falsification criteria—not a working foundry, trained expert, linked neural object, benchmark result, safety result, or support-state promotion. |

## Thesis

An executable scaffold should be treated as a high-level capability
representation, not discarded as temporary demo code. A governed compiler can
decompose the scaffold into semantic capability fields, generate coverage from
the executable specification, train contract-bound learned replacements, link
those replacements through an explicit neural ABI, and admit them only through
candidate-specific translation validation. The teacher remains available as
oracle, verifier, residual owner, fallback, and recovery artifact while the
system progressively moves from deterministic execution toward learned and
environment-adapted implementations.

The paper's strongest contribution to the ASI Stack is a lifecycle join:

```text
capability charter
-> executable scaffold
-> semantic capability graph
-> coverage-directed corpus
-> contract-bound expert
-> neural capability object and linker
-> equivalence ratchet
-> shielded residual adaptation
-> governed transcendence
-> reification into a new explicit artifact
-> recursive foundry
```

The operative maxim is *program first, learn second, transcend third, preserve
always*. “Preserve” means preserving typed obligations, evidence, fallback,
authority ceilings, and recovery—not assuming behavioral cloning has captured
the capability.

## Core Mechanisms

1. **Capability charter and vector envelope.** A field declares input and
   output schemas, preconditions, postconditions, invariants, failure semantics,
   authority, cost, recovery, and observability. Coverage is a vector across
   behavioral, state, temporal, interface, environmental, recovery, and
   uncertainty dimensions rather than one percentage.
2. **Semantic decomposition with mass balance.** Decomposition follows the
   smallest semantically closed replaceable capability, not syntax. Every
   source obligation is marked preserved, revised, residualized, or rejected;
   no obligation may silently disappear.
3. **Coverage-directed learning.** The scaffold generates traces, boundary
   cases, failures, and counterexamples. Interactive collection, adversarial
   search, and learner-induced states address covariate shift and expose gaps
   hidden by a static corpus.
4. **Contract-bound micro-experts.** A learned component implements one field
   under a declared applicability region, failure channel, evidence package,
   and fallback path. Interface fit and authority are independent from task
   quality.
5. **Neural Capability Objects (NCOs).** An NCO packages a field identity,
   compatible base, owned parameter region, neural ABI, contract, evidence, and
   recovery. It is a lifecycle artifact, not merely a checkpoint delta.
6. **Neural ABI and linker.** The ABI separates tensor ownership, activation
   call/return/error lanes, capability contracts, and lifecycle metadata. The
   linker resolves identity, relocation, conflicts, adapters, router bindings,
   validation, and a signed link receipt. Sparse composition is the preservation
   baseline; densification is optional link-time optimization.
7. **Verifier-guided equivalence ratchet.** Each candidate receives a
   translation-validation disposition of pass, fail, or unknown across schema,
   unit, interface, composition, properties, adversarial cases, learner-induced
   states, environmental tests, independent evaluation, and natural monitoring.
   Counterexamples become durable training and regression memory.
8. **Proof-carrying training receipts.** Training records exact code, data,
   seeds, optimizer state, budgets, parameter changes, denominators, failures,
   authority, rollback, support effect, and non-claims. Verification bandwidth
   is allocated by novelty, consequence, and residual risk.
9. **Environmentalization without authority drift.** A dual-view world model
   preserves disagreement between top-down prediction and bottom-up
   measurement. Residual learning is gated, shielded, reversible where possible,
   and prohibited from expanding authority.
10. **Governed transcendence.** Candidate behavior that improves on the
    scaffold enters a tribunal that distinguishes student defect, specification
    defect, novelty, valid optimization, reward exploit, and unresolved cases.
    Accepted discoveries are reified into explicit specifications, tests, or
    new fields so improvement closes the loop instead of becoming opaque drift.
11. **Four planes and three clocks.** Specification, learning, runtime, and
    assurance remain separate. Fast local adaptation, medium capability
    compilation, and slow constitutional change use different authorities and
    evidence thresholds.
12. **Effect-complete recovery.** Rollback accounts for model, optimizer,
    scheduler, RNG, cache, backup, runtime, external effect, and descendant
    state. Restoring one checkpoint is not equivalent to restoring the system.

## Conditional Propositions

- A sparse graft can preserve an unchanged path only under explicit assumptions
  about parameter disjointness, routing isolation, deterministic execution, and
  compatible base state.
- Local linking reduces the conflict surface only when ownership and shared
  dependencies are accurately declared.
- An environmental learner cannot escalate authority if its output is mediated
  by an independent authority gate that it cannot rewrite or bypass.
- Capability conservation is meaningful only when the obligation inventory is
  complete enough to detect missing semantic mass.
- Model-state rollback is bounded by the captured state and cannot erase
  already realized external consequences.
- Passing a finite verifier establishes only the tested relation; it does not
  establish total semantic equivalence.

These are targets for formalization or experiment, not unconditional facts
established by the source.

## Proposed Artifact Family

- Capability Charter and Capability Field records.
- Semantic Capability Graph and obligation mass-balance ledger.
- Coverage Envelope and coverage-directed corpus manifest.
- Contract-bound expert package and applicability certificate.
- Neural Capability Object package and four-layer neural ABI.
- Link plan, conflict report, adapter plan, router binding, and link receipt.
- Translation-validation report with `pass`, `fail`, or `unknown`.
- Counterexample memory and residual escrow.
- Governed update lease and disagreement-tribunal record.
- Reification record connecting discovery back to an explicit artifact.
- Foundry artifact graph, stable registry, and proof-carrying training receipt.

## Evidence and Falsification Program

The paper proposes four deliberately different domains: transactional software,
n-link cart-pole control, contact-rich robotics, and verifiable reasoning/tool
use. A serious program must compare the full ladder against scratch RL,
end-to-end imitation, trace-free distillation, unrelated initialization,
checkpoint averaging and merge baselines, MoE without fields, sparse linking,
dense students, and full-policy residual learning. It must ablate traces,
counterexample memory, DAgger-style learner-state collection, shielding,
reification, and evaluator independence.

Measure atomic fidelity, compositional behavior, environmental adaptation,
authority violations, fallback and rollback success, residual burden,
verification cost, latency, useful throughput, and maintenance economics
together. The proposal is weakened if well-tuned simpler baselines match its
capability preservation and governance value at materially lower total cost, if
the capability graph misses consequential obligations, if linker isolation does
not survive realistic shared-state effects, or if verification repeatedly
approves candidates that fail under natural deployment states.

## Failure Modes

- Scaffold overinvestment that delays useful learning.
- Specification laundering: treating executable behavior as the full intent.
- Decomposition debt and missing semantic obligations.
- Synthetic-corpus monoculture and trace theater.
- Neural ABI ossification or hidden shared-state conflicts.
- Expert overlap, router collapse, and silent authority expansion.
- Densification amnesia after successful sparse linking.
- Verifier monoculture or candidate-owned evaluation.
- Reward and shield gaming, residual dominance, and self-confirming world models.
- False reification that canonizes an exploit or transient correlation.
- Governance capture and unaccounted irreversible effects.

## Book Chapters Supported

| Chapter | Contribution | Source locus | Boundary |
|---|---|---|---|
| `stable-capability-fields` | Extends a field into an executable compilation unit with a vector envelope, semantic mass balance, applicability, evidence, and recovery. | §§4–6, 10, 21 | Does not prove that a field decomposition is complete or stable. |
| `cognitive-compilation-and-semantic-ir` | Supplies the scaffold-to-capability-graph-to-expert lowering pipeline and bidirectional reification loop. | §§3–8, 17, 20 | Compiler and semantic-preservation claims remain unimplemented. |
| `capability-replacement-and-rollback` | Defines candidate-specific equivalence, fallback, sparse replacement, full-state recovery, and irreversible-effect accounting. | §§9–10, 15–17 | Finite verification is not total equivalence; rollback scope is bounded. |
| `routing-heads-and-specialist-cores` | Treats routes as leases over qualified fields and linked NCOs, with explicit applicability, fallback, and conflict handling. | §§7–9, 14 | Does not establish routing quality or linker isolation. |
| `runtime-adapters-tool-permissions-and-human-approval` | Keeps capability qualification separate from execution authority and places residual learning behind an independent gate. | §§5, 13–16 | No source-derived authority enforcement result. |
| `procedural-memory-and-cognitive-loop-closure` | Converts accepted discoveries and counterexamples into reusable explicit artifacts rather than opaque weight drift. | §§9, 16–17 | Reification quality and loop stability remain untested. |
| `recursive-self-improvement-boundaries` | Defines architectural RSI as governed improvement of specifications, fields, linkers, verifiers, and the foundry itself across three clocks. | §§16–21 | Does not establish recursive improvement, convergence, or safety. |
| `benchmark-ratchets-and-anti-goodhart-evidence` | Adds coverage vectors, candidate-specific translation validation, durable counterexamples, independent evaluation, and full-cost denominators. | §§9–10, 18–19 | A test suite can remain incomplete or self-confirming. |
| `data-engines-continual-learning-and-unlearning` | Adds learner-induced-state collection, residual-first updates, complete training state, and lineage-aware reification. | §§6, 12–17 | Does not establish forgetting, privacy erasure, or influence removal. |
| `integrated-reference-architecture` | Provides the Executable Capability Foundry as a joined lifecycle across specification, learning, runtime, and assurance planes. | §§3, 20–22 | Architecture proposal only; no end-to-end foundry exists here. |
| `intent-to-execution-contracts` | Turns accepted intent into a capability charter and preserves obligations through scaffold and learned lowering. | §§5.1–5.3, 15.1 | The scaffold remains defeasible evidence about intent. |
| `virtual-context-abi` | Treats context as a protected compilation packet carrying field, applicability, evidence, residual, fallback, and invalidation state. | §11.5 | No packet compiler or adequacy result. |
| `spinoza-verification-and-proof-carrying-claims` | Adds proof-carrying training receipts, evaluator dependencies, and pass/fail/unknown validation. | §7 | A receipt is not proof of semantic equivalence. |
| `labor-os-and-typed-jobs` | Decomposes the foundry into authority-separated typed jobs and runtime modes. | §§11, 14–15 | No foundry job runtime exists here. |
| `artifact-graphs-audit-logs-and-replay` | Preserves complete foundry lineage, counterexamples, failures, tribunal decisions, and reification. | §§7, 10, 14 | Graph completeness remains consumer-relative. |
| `readiness-gates-residual-escrow-and-quarantine` | Owns exact/compiled/shadow/residual/canary/fallback/quarantine modes and residual custody. | §9 | No calibrated readiness thresholds. |
| `compact-generative-systems-and-residual-honesty` | Treats learned hot paths as compression with retained teacher, verifier, fallback, and residual burden. | §§2, 6, 15.11, 20 | No total-cost compression advantage. |
| `replaceable-cognitive-substrates-beyond-transformer-monoculture` | Uses NCOs and adapters as proposed substrate-neutral capability link units. | §§6, 15.12, 20.5 | Does not prove cross-architecture substitutability. |
| `ai-supply-chain-integrity-and-lifecycle-provenance` | Adds NCO, ABI, link, training, densification, incident, and recovery artifacts to lifecycle provenance. | §§6–7, 14 | Provenance does not establish capability quality. |
| `project-theseus-as-report-first-implementation-reference` | Converts the foundry into a prospective report-first vertical slice. | §15.14 | Current Theseus does not inherit implementation claims. |
| `prototype-roadmap` | Supplies the staged charter-to-foundry research sequence. | §22 | Phase text is not phase completion. |
| `open-research-agenda-and-bibliography-plan` | Owns external comparator review and the unexecuted experiment program. | §§3, 16–18, 21–22 | Backlog presence is not evidence. |

The section-family closure ledger is
`docs/july_2026_two_paper_mining_completeness_audit.md`. It maps every
top-level section, subsection family, appendix, and reference role to prose,
source-note synthesis, research work, or an explicit boundary.

## Chapter Decision

Update the twenty-two existing owners. Do not add a paper-shaped chapter. Stable
Capability Fields already owns capability identity; Cognitive Compilation owns
lowering and reification; replacement, routing, runtime authority, memory,
evidence, labor, provenance, readiness, context, substrate, roadmap, learning,
RSI, and integration own the remaining lifecycle. A new
chapter would duplicate those boundaries. Reconsider only if an implemented
NCO linker and foundry expose a durable, otherwise unowned runtime authority or
reader job.

## Claims To Add Or Update

- Add the design rule that compilation must conserve a typed obligation ledger,
  not merely output behavior on a sampled dataset.
- Add the NCO as a proposed package joining parameter ownership, neural ABI,
  capability contract, evidence, and recovery.
- Add `unknown` as a first-class translation-validation result.
- Add the rule that sparse composition is the preservation baseline and dense
  consolidation is a separately qualified optimization.
- Add the dual-view world-model rule: prediction and observation disagreement
  remains visible until adjudicated.
- Add reification as the closure step by which accepted learned discoveries
  become explicit, testable, governed artifacts.
- Define architectural RSI as improvement of the foundry and its interfaces,
  not weight mutation alone.

## Open Questions

- Which bounded domain exposes real semantic mass loss rather than simple
  imitation error?
- Can parameter ownership and activation lanes remain isolated in realistic
  shared-base training and serving systems?
- What evidence makes an NCO link receipt independently meaningful?
- When does a sparse linked composite outperform a monolith after full router,
  verifier, fallback, and maintenance cost is charged?
- How should the tribunal detect specification gaming without laundering the
  teacher's own defects?
- Which effects, caches, descendants, and external actions must a foundry treat
  as non-rollbackable?
